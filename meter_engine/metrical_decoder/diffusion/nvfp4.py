# -*- coding: utf-8 -*-
"""
NVFP4 expert weights, kept packed and decoded on the GPU when a layer runs.

NVIDIA's Model Optimizer stores DiffusionGemma's mixture-of-experts weights —
22.8 of its 25.8 billion parameters — in NVFP4:

* every weight is a 4-bit float, E2M1 (sign, 2-bit exponent, 1-bit mantissa),
  i.e. one of ±{0, 0.5, 1, 1.5, 2, 3, 4, 6};
* two weights share a byte, the first in the **low** nibble:
  ``weight`` is ``uint8 [out, in / 2]``;
* each run of 16 consecutive inputs has an FP8 (E4M3) scale,
  ``weight_scale`` ``[out, in / 16]``, and each tensor one FP32 scale,
  ``weight_scale_2``:  ``w = e2m1 × weight_scale × weight_scale_2``;
* ``input_scale`` quantises activations for NVFP4 matrix kernels. Decoding to
  BF16 does not use it: the computation runs in BF16, as in the original model.

The layout was verified against the BF16 Gemma-4 26B-A4B checkpoint, from which
DiffusionGemma was initialised: a decoded expert has cosine similarity 0.92–0.97
with the same Gemma-4 expert, about 0.00 with the nibbles swapped and 0.01–0.02
with a different expert.

:class:`Nvfp4Experts` replaces ``DiffusionGemmaTextExperts``. It keeps a layer's
128 experts packed (about 4.5 bits a weight: 0.43 GB a layer instead of 1.5 GB)
and, when the layer runs, decodes them into one BF16 workspace shared by all
layers, then applies the experts with two grouped matrix products (the same
arithmetic as ``transformers``' ``grouped_mm`` experts). The model thus needs
about 19 GB instead of 52 GB, at the cost of decoding each layer's experts on
every pass.

Owns: :func:`decode_nvfp4`, :class:`Nvfp4Experts`.
"""
from __future__ import annotations

from typing import Callable, Optional

import torch
from torch import nn

E2M1_VALUES = (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, -0.0, -0.5, -1.0, -1.5, -2.0, -3.0, -4.0, -6.0)
BLOCK = 16                                   # inputs sharing one FP8 scale

_BYTE_TABLES: dict[tuple, torch.Tensor] = {}


def byte_table(dtype: torch.dtype, device: torch.device) -> torch.Tensor:
    """``[256, 2]``: the two E2M1 values packed in every byte, low nibble first."""
    key = (dtype, str(device))
    if key not in _BYTE_TABLES:
        values = torch.tensor(E2M1_VALUES, dtype=torch.float32)
        byte = torch.arange(256)
        _BYTE_TABLES[key] = torch.stack([values[byte & 0x0F], values[byte >> 4]], dim=-1).to(dtype=dtype, device=device)
    return _BYTE_TABLES[key]


def decode_nvfp4(packed: torch.Tensor, scale: torch.Tensor, scale2: torch.Tensor,
                 out: Optional[torch.Tensor] = None, dtype: torch.dtype = torch.bfloat16) -> torch.Tensor:
    """Decode NVFP4 weights to ``dtype``.

    ``packed``: ``uint8 [..., out, in/2]``; ``scale``: FP8 ``[..., out, in/16]``;
    ``scale2``: FP32 of shape ``[...]`` or ``[..., out]`` (one value per tensor,
    or per row). Writes into ``out`` (``[..., out, in]``) when given.

    >>> packed = torch.tensor([[0x21, 0x7F, 0, 0, 0, 0, 0, 0]], dtype=torch.uint8)   # codes 1,2 | 15,7 | 0…
    >>> scale = torch.full((1, 1), 2.0).to(torch.float8_e4m3fn)                      # one block of 16
    >>> decode_nvfp4(packed, scale, torch.tensor(0.5), dtype=torch.float32)[0, :4].tolist()
    [0.5, 1.0, -6.0, 6.0]
    """
    table = byte_table(dtype, packed.device)
    w = table[packed.int()].flatten(-2)                                   # [..., out, in]
    w = w.unflatten(-1, (-1, BLOCK)).mul_(scale.to(dtype).unsqueeze(-1)).flatten(-2)
    s2 = scale2.to(dtype)
    w.mul_(s2[..., None] if s2.dim() == w.dim() - 1 else s2[..., None, None])
    if out is not None:
        out.copy_(w)
        return out
    return w


class _Workspace:
    """One BF16 buffer per shape and device, reused by every layer (layers run one at a time)."""

    buffers: dict[tuple, torch.Tensor] = {}

    @classmethod
    def get(cls, shape: tuple, dtype: torch.dtype, device: torch.device) -> torch.Tensor:
        key = (shape, dtype, str(device))
        buf = cls.buffers.get(key)
        if buf is None:
            buf = cls.buffers[key] = torch.empty(shape, dtype=dtype, device=device)
        return buf


class Nvfp4Experts(nn.Module):
    """A layer's experts, packed in NVFP4, applied as BF16.

    Drop-in for ``DiffusionGemmaTextExperts`` (``forward(hidden_states, top_k_index,
    top_k_weights)``). Built empty; :meth:`load` fills it. One instance serves
    both the encoder and the decoder layer of the same depth, which share their
    weights.
    """

    def __init__(self, config, chunk_experts: int = 32):
        super().__init__()
        self.num_experts = config.num_experts
        self.hidden_dim = config.hidden_size
        self.intermediate_dim = config.moe_intermediate_size
        self.chunk_experts = chunk_experts
        from transformers.activations import ACT2FN
        self.act_fn: Callable = ACT2FN[config.hidden_activation]
        for name in ("gate_up_packed", "gate_up_scale", "gate_up_scale2", "down_packed", "down_scale", "down_scale2"):
            self.register_buffer(name, torch.empty(0), persistent=False)
        # The model's weight initialiser recognises this module as its experts class and initialises
        # ``gate_up_proj`` / ``down_proj``: empty placeholders make that a no-op (the real weights are packed).
        self.register_buffer("gate_up_proj", torch.empty(0), persistent=False)
        self.register_buffer("down_proj", torch.empty(0), persistent=False)

    def load(self, gate_up: tuple, down: tuple) -> None:
        """``gate_up`` = (packed ``[E, 2I, H/2]``, scale ``[E, 2I, H/16]``, scale2 ``[E, 2I]``);
        ``down`` = (packed ``[E, H, I/2]``, scale ``[E, H, I/16]``, scale2 ``[E]``)."""
        self.gate_up_packed, self.gate_up_scale, self.gate_up_scale2 = gate_up
        self.down_packed, self.down_scale, self.down_scale2 = down
        self.resident: dict[str, torch.Tensor] = {}

    def make_resident(self) -> None:
        """Decode the experts once and keep them in BF16, dropping the packed copies.

        Much faster (no decoding on every pass) for 1.5 GB a layer instead of 0.43 GB — about
        52 GB for the whole model instead of 19 GB. Numerically identical to decoding per pass."""
        for which in ("gate_up", "down"):
            packed = getattr(self, f"{which}_packed")
            E, rows, half = packed.shape
            out = torch.empty((E, rows, 2 * half), dtype=torch.bfloat16, device=packed.device)
            self.resident[which] = self._decode_into(which, out)
            for part in ("packed", "scale", "scale2"):
                setattr(self, f"{which}_{part}", torch.empty(0, device=packed.device))

    @property
    def weight_bytes(self) -> int:
        tensors = list(self.buffers()) + list(getattr(self, "resident", {}).values())
        return sum(t.numel() * t.element_size() for t in tensors)

    def _decode_into(self, which: str, out: torch.Tensor) -> torch.Tensor:
        """All experts of one projection decoded into ``out``, a chunk of experts at a time
        (so the temporaries stay small)."""
        packed, scale, scale2 = (getattr(self, f"{which}_packed"), getattr(self, f"{which}_scale"),
                                 getattr(self, f"{which}_scale2"))
        for e0 in range(0, packed.shape[0], self.chunk_experts):
            e1 = min(packed.shape[0], e0 + self.chunk_experts)
            decode_nvfp4(packed[e0:e1], scale[e0:e1], scale2[e0:e1], out=out[e0:e1])
        return out

    def _decoded(self, which: str) -> torch.Tensor:
        """All experts of one projection in BF16: resident, or decoded into the shared workspace."""
        if which in getattr(self, "resident", {}):
            return self.resident[which]
        packed = getattr(self, f"{which}_packed")
        E, rows, half = packed.shape
        return self._decode_into(which, _Workspace.get((E, rows, 2 * half), torch.bfloat16, packed.device))

    def forward(self, hidden_states: torch.Tensor, top_k_index: torch.Tensor,
                top_k_weights: torch.Tensor) -> torch.Tensor:
        num_tokens, top_k = top_k_index.shape
        # tokens sorted by expert, so that each expert's rows are contiguous (grouped products)
        expert_ids = top_k_index.reshape(-1)
        expert_sorted, order = torch.sort(expert_ids)
        x = hidden_states[order // top_k]
        counts = torch.bincount(expert_sorted, minlength=self.num_experts)
        offsets = torch.cumsum(counts, dim=0, dtype=torch.int32)

        gate_up = self._decoded("gate_up")                                   # [E, 2I, H]
        h = _grouped_mm(x, gate_up, offsets)                                 # [S, 2I]
        gate, up = h.chunk(2, dim=-1)
        h = self.act_fn(gate) * up
        down = self._decoded("down")                                         # [E, H, I]
        y = _grouped_mm(h, down, offsets)                                    # [S, H]
        y = y * top_k_weights.reshape(-1)[order].unsqueeze(-1).to(y.dtype)

        restored = torch.empty_like(y)
        restored[order] = y
        # sum the top-k contributions in fp32 (deterministic, unlike index_add_)
        return restored.view(num_tokens, top_k, -1).float().sum(dim=1).to(hidden_states.dtype)


def _grouped_mm(x: torch.Tensor, weight: torch.Tensor, offsets: torch.Tensor) -> torch.Tensor:
    """``x[S, in]`` times each group's ``weight[e]ᵀ`` (``weight`` is ``[E, out, in]``); rows of group e
    end at ``offsets[e]``."""
    if hasattr(torch.nn.functional, "grouped_mm") and x.is_cuda:
        return torch.nn.functional.grouped_mm(x.to(weight.dtype), weight.transpose(-2, -1), offs=offsets)
    out = x.new_empty((x.shape[0], weight.shape[1]), dtype=weight.dtype)      # fallback: one product per expert
    start = 0
    for e, end in enumerate(offsets.tolist()):
        if end > start:
            out[start:end] = x[start:end].to(weight.dtype) @ weight[e].T
        start = end
    return out

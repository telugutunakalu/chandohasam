# -*- coding: utf-8 -*-
"""
Load ``nvidia/diffusiongemma-26B-A4B-it-NVFP4`` into ``transformers``' DiffusionGemma,
with the experts kept in NVFP4.

Neither the installed ``transformers`` (no loader for Model Optimizer checkpoints)
nor the installed vLLM (no DiffusionGemma) can run this checkpoint, and the BF16
original (52 GB) does not fit beside the translation server. This loader fills
``transformers``' own model class from the checkpoint directly:

1. the model is built on the GPU, in BF16, with :class:`~.nvfp4.Nvfp4Experts` in
   place of the BF16 experts, so the 45 GB of BF16 expert weights is never
   allocated. Encoder layer *i* and decoder layer *i* share every weight, so they
   are given one and the same expert module;
2. every other tensor — attention, dense MLP, router, norms, embeddings,
   self-conditioning, vision tower and the 62 persistent buffers (``layer_scalar``
   of each encoder and decoder layer, among them) — is copied by name. Parameters
   tied between encoder and decoder share storage and are filled once;
3. each layer's experts are read expert by expert (``gate_proj``, ``up_proj``,
   ``down_proj``: packed weights, FP8 block scales, FP32 tensor scales), stacked
   in ``transformers``' ``gate_up`` / ``down`` layout (gate rows first) and moved
   to the GPU still packed.

Every tensor of the model must come from the checkpoint: loading raises if one
is left unfilled or if the checkpoint holds a tensor the model does not.

Owns: :func:`load_diffusiongemma_nvfp4`. Imports torch.
"""
from __future__ import annotations

import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Callable

import torch

from .nvfp4 import Nvfp4Experts

DEFAULT_MODEL = "nvidia/diffusiongemma-26B-A4B-it-NVFP4"
PROJECTIONS = ("gate_proj", "up_proj", "down_proj")


def _snapshot(model_id: str) -> Path:
    path = Path(model_id)
    if path.is_dir():
        return path
    from huggingface_hub import snapshot_download
    return Path(snapshot_download(model_id, local_files_only=True))


def load_diffusiongemma_nvfp4(model_id: str = DEFAULT_MODEL, device: str = "cuda", resident: bool = False,
                              log: Callable[[str], None] = print):
    """Returns ``(model, tokenizer)``: ``DiffusionGemmaForBlockDiffusion`` in eval mode on ``device``.

    ``resident=False`` keeps the experts packed (about 19 GB; each pass decodes them, about 4 s a
    pass on the GB10); ``resident=True`` decodes them once and keeps BF16 (about 52 GB; much faster)."""
    from safetensors import safe_open
    from transformers import AutoConfig, AutoTokenizer
    from transformers.models.diffusion_gemma import modeling_diffusion_gemma as mdg

    t0 = time.time()
    path = _snapshot(model_id)
    config = AutoConfig.from_pretrained(path)
    if hasattr(config, "quantization_config"):
        del config.quantization_config                 # the experts are handled here, not by a quantizer
    text = config.text_config

    # 1. build with empty NVFP4 expert modules (the layer classes look the experts class up at build time)
    original_experts = mdg.DiffusionGemmaTextExperts
    mdg.DiffusionGemmaTextExperts = Nvfp4Experts
    try:
        with torch.device(device):
            model = mdg.DiffusionGemmaForBlockDiffusion._from_config(config, dtype=torch.bfloat16)
    finally:
        mdg.DiffusionGemmaTextExperts = original_experts
    encoder_layers = model.model.encoder.language_model.layers
    decoder_layers = model.model.decoder.layers
    for enc, dec in zip(encoder_layers, decoder_layers):
        enc.experts = dec.experts                      # shared, like every other weight of the layer
    log(f"built on {device} in {time.time() - t0:.0f}s")

    weight_map: dict[str, str] = json.loads((path / "model.safetensors.index.json").read_text())["weight_map"]
    by_file: dict[str, list[str]] = defaultdict(list)
    for key, file in weight_map.items():
        by_file[file].append(key)
    handles = {file: safe_open(str(path / file), "pt", device="cpu") for file in by_file}

    # 2. every tensor but the experts, by name
    state = model.state_dict()
    filled, unexpected = set(), []
    for file, keys in by_file.items():
        for key in keys:
            if ".experts." in key:
                continue
            if key not in state:
                unexpected.append(key)
                continue
            tensor = handles[file].get_tensor(key)
            target = state[key]
            if tuple(tensor.shape) != tuple(target.shape):
                raise ValueError(f"{key}: checkpoint {tuple(tensor.shape)} vs model {tuple(target.shape)}")
            target.copy_(tensor.to(target.dtype))
            filled.add(key)
    filled_storage = {state[k].data_ptr() for k in filled}
    missing = [k for k, v in state.items() if k not in filled and v.data_ptr() not in filled_storage]
    if unexpected or missing:
        raise ValueError(f"checkpoint/model mismatch: unexpected {unexpected[:5]} ({len(unexpected)}), "
                         f"missing {missing[:5]} ({len(missing)})")
    log(f"{len(filled)} dense tensors loaded ({time.time() - t0:.0f}s)")

    # 3. the experts, packed
    E, I, H = text.num_experts, text.moe_intermediate_size, text.hidden_size

    def read(key: str) -> torch.Tensor:
        return handles[weight_map[key]].get_tensor(key)

    for i, layer in enumerate(decoder_layers):
        gate_up = (torch.empty(E, 2 * I, H // 2, dtype=torch.uint8),
                   torch.empty(E, 2 * I, H // 16, dtype=torch.float8_e4m3fn),
                   torch.empty(E, 2 * I, dtype=torch.float32))
        down = (torch.empty(E, H, I // 2, dtype=torch.uint8),
                torch.empty(E, H, I // 16, dtype=torch.float8_e4m3fn),
                torch.empty(E, dtype=torch.float32))
        for e in range(E):
            base = f"model.decoder.layers.{i}.experts.{e}"
            for proj, rows in (("gate_proj", slice(0, I)), ("up_proj", slice(I, 2 * I))):
                gate_up[0][e, rows] = read(f"{base}.{proj}.weight")
                gate_up[1][e, rows] = read(f"{base}.{proj}.weight_scale")
                gate_up[2][e, rows] = read(f"{base}.{proj}.weight_scale_2")
            down[0][e] = read(f"{base}.down_proj.weight")
            down[1][e] = read(f"{base}.down_proj.weight_scale")
            down[2][e] = read(f"{base}.down_proj.weight_scale_2")
        layer.experts.load(tuple(t.to(device) for t in gate_up), tuple(t.to(device) for t in down))
        if resident:
            layer.experts.make_resident()
        if (i + 1) % 10 == 0:
            log(f"experts of {i + 1}/{len(decoder_layers)} layers loaded ({time.time() - t0:.0f}s)")

    model.eval()
    # the checkpoint's own generation settings (end-of-text ids, temperature schedule, entropy bound):
    # a model built from its config alone would carry defaults instead
    model.generation_config = type(model).generation_config_class.from_pretrained(path)
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        log(f"ready in {time.time() - t0:.0f}s; GPU memory allocated {torch.cuda.memory_allocated() / 1e9:.1f} GB")
    tokenizer = AutoTokenizer.from_pretrained(path)
    return model, tokenizer

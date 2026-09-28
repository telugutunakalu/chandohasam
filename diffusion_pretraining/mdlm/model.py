"""Bidirectional transformer denoiser for MDLM.

Pre-norm blocks (RMSNorm, rotary attention, SwiGLU), no causal mask and no
timestep input: the absorbing-state denoiser's optimum does not depend on t
(Ou et al. 2024; Zheng et al. 2024), and LLaDA drops it too. Input and output
embeddings are tied; the vocabulary is padded to a multiple of 128 for tensor
cores, and the padding rows are never predicted.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import torch
import torch.nn.functional as F
from torch import nn


def _doc(default, text: str):
    return field(default=default, metadata={"doc": text})


@dataclass
class ModelConfig:
    vocab_size: int = _doc(45591, "Tokenizer vocabulary size (telugu_alldomain: 5 specials, 256 bytes, "
                                  "485 BPE pieces, 10 Telugu digits, 44,835 whole aksharas).")
    d_model: int = _doc(768, "Width of the residual stream, the token embeddings and every block's input/output.")
    n_layers: int = _doc(12, "Number of transformer blocks.")
    n_heads: int = _doc(12, "Attention heads per block; head_dim = d_model / n_heads (kept at 64 for growth).")
    mlp_hidden: int = _doc(2048, "SwiGLU hidden width per block (8/3 x d_model, so it scales exactly under growth).")
    max_len: int = _doc(512, "Canvas length in tokens; RoPE tables are built for this many positions.")
    rope_base: float = _doc(10000.0, "Rotary-embedding base frequency (kept fixed under growth).")
    norm_eps: float = _doc(1e-6, "RMSNorm epsilon.")
    init_std: float = _doc(0.02, "Std of the normal init for embeddings and linear layers; the two residual "
                                  "output projections per block use init_std / sqrt(2 x n_layers).")

    @property
    def head_dim(self) -> int:
        return self.d_model // self.n_heads

    @property
    def padded_vocab(self) -> int:
        return (self.vocab_size + 127) // 128 * 128


PRESETS = {
    "tiny": ModelConfig(d_model=384, n_layers=6, n_heads=6, mlp_hidden=1024),               # tests and debugging
    "small-512": ModelConfig(d_model=512, n_layers=12, n_heads=8, mlp_hidden=1408),         # not on the growth ladder
    # Growth ladder: head_dim 64, mlp_hidden = 8/3 d_model and widths that are whole multiples of the
    # previous stage, so every step can be initialised function-preservingly from the one before.
    "small-768": ModelConfig(d_model=768, n_layers=12, n_heads=12, mlp_hidden=2048),        # stage 0: 120M pilot
    "grow-1536x16": ModelConfig(d_model=1536, n_layers=16, n_heads=24, mlp_hidden=4096),    # stage 1: ~523M (width x2, +4 layers)
    "grow-1536x32": ModelConfig(d_model=1536, n_layers=32, n_heads=24, mlp_hidden=4096),    # stage 2: ~976M (depth x2)
    "grow-2304x16": ModelConfig(d_model=2304, n_layers=16, n_heads=36, mlp_hidden=6144),    # alt. 1B: ~1.12B (width x3 from stage 0)
}


class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.rms_norm(x, (x.shape[-1],), self.weight, self.eps)


def rope_tables(head_dim: int, max_len: int, base: float) -> tuple[torch.Tensor, torch.Tensor]:
    inv = 1.0 / base ** (torch.arange(0, head_dim, 2, dtype=torch.float32) / head_dim)
    ang = torch.outer(torch.arange(max_len, dtype=torch.float32), inv)
    return ang.cos(), ang.sin()


def apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    """x: (B, H, L, D); rotate channel pairs (x1, x2) by position-dependent angles."""
    x1, x2 = x[..., 0::2], x[..., 1::2]
    cos, sin = cos[: x.shape[-2]].to(x.dtype), sin[: x.shape[-2]].to(x.dtype)
    return torch.stack((x1 * cos - x2 * sin, x1 * sin + x2 * cos), dim=-1).flatten(-2)


class Block(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.n_heads = cfg.n_heads
        self.norm1 = RMSNorm(cfg.d_model, cfg.norm_eps)
        self.qkv = nn.Linear(cfg.d_model, 3 * cfg.d_model, bias=False)
        self.proj = nn.Linear(cfg.d_model, cfg.d_model, bias=False)
        self.norm2 = RMSNorm(cfg.d_model, cfg.norm_eps)
        self.gate_up = nn.Linear(cfg.d_model, 2 * cfg.mlp_hidden, bias=False)
        self.down = nn.Linear(cfg.mlp_hidden, cfg.d_model, bias=False)

    def forward(self, x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
        b, l, d = x.shape
        q, k, v = self.qkv(self.norm1(x)).view(b, l, 3, self.n_heads, d // self.n_heads).permute(2, 0, 3, 1, 4)
        q, k = apply_rope(q, cos, sin), apply_rope(k, cos, sin)
        att = F.scaled_dot_product_attention(q, k, v)               # bidirectional: no mask
        x = x + self.proj(att.transpose(1, 2).reshape(b, l, d))
        gate, up = self.gate_up(self.norm2(x)).chunk(2, dim=-1)
        return x + self.down(F.silu(gate) * up)


class Denoiser(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.cfg = cfg
        self.embed = nn.Embedding(cfg.padded_vocab, cfg.d_model)
        self.blocks = nn.ModuleList(Block(cfg) for _ in range(cfg.n_layers))
        self.norm = RMSNorm(cfg.d_model, cfg.norm_eps)
        cos, sin = rope_tables(cfg.head_dim, cfg.max_len, cfg.rope_base)
        self.register_buffer("cos", cos, persistent=False)
        self.register_buffer("sin", sin, persistent=False)
        for m in self.modules():
            if isinstance(m, (nn.Linear, nn.Embedding)):
                nn.init.normal_(m.weight, std=cfg.init_std)
        for blk in self.blocks:                                       # GPT-2 style residual scaling
            nn.init.normal_(blk.proj.weight, std=cfg.init_std / math.sqrt(2 * cfg.n_layers))
            nn.init.normal_(blk.down.weight, std=cfg.init_std / math.sqrt(2 * cfg.n_layers))

    def hidden(self, x: torch.Tensor) -> torch.Tensor:
        """(B, L) token ids -> (B, L, d_model) final hidden states."""
        h = self.embed(x)
        for blk in self.blocks:
            h = blk(h, self.cos, self.sin)
        return self.norm(h)

    def logits(self, h: torch.Tensor) -> torch.Tensor:
        """Hidden states -> logits over the padded vocabulary (tied output embedding)."""
        return h @ self.embed.weight.t()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.logits(self.hidden(x))

    def num_params(self, non_embedding: bool = True) -> int:
        n = sum(p.numel() for p in self.parameters())
        return n - self.embed.weight.numel() if non_embedding else n

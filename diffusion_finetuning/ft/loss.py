"""MDLM objective restricted by roles (PLAN §5.2).

Only positions whose role is TARGET or FILL are ever masked; GIVEN positions stay clean in the
input and carry no loss. Masked positions are scored with -log p / t (the MDLM ELBO). The
caller divides the returned sum by its normaliser: all canvas tokens in Stage 1 (as in
pretraining), the TARGET tokens of the whole optimizer step in Stage 2.
"""
from __future__ import annotations

import torch
from torch.utils.checkpoint import checkpoint

from mdlm.diffusion import CE_CHUNK, _ce_chunk, sample_t

from .canvas import FILL, TARGET


def role_nelbo(model, x: torch.Tensor, roles: torch.Tensor, mask_id: int, bias: torch.Tensor,
               t: torch.Tensor | None = None, generator: torch.Generator | None = None) -> dict:
    """x, roles: (B, L). Returns the weighted CE sum and per-masked-token details."""
    if t is None:
        t = sample_t(x.shape[0], x.device, generator)
    maskable = roles >= TARGET
    masked = (torch.rand(x.shape, device=x.device, generator=generator) < t[:, None]) & maskable
    xt = torch.where(masked, torch.full_like(x, mask_id), x)
    rows = masked.nonzero(as_tuple=True)[0]
    h, target = model.hidden(xt)[masked], x[masked]
    ce, correct = [], []
    for hc, tc in zip(h.split(CE_CHUNK), target.split(CE_CHUNK)):
        if torch.is_grad_enabled():
            c, ok = checkpoint(_ce_chunk, model.logits, hc, tc, bias, use_reentrant=False)
        else:
            c, ok = _ce_chunk(model.logits, hc, tc, bias)
        ce.append(c)
        correct.append(ok)
    ce = torch.cat(ce) if ce else h.new_zeros(0, dtype=torch.float32)
    weighted = ce / t[rows]
    row_sum = torch.zeros(x.shape[0], device=x.device).index_add_(0, rows, weighted.detach().float())
    return {"sum": weighted.sum(), "ce": ce.detach(), "t": t[rows].detach(), "row_sum": row_sum,
            "row_target": (roles == TARGET).sum(1),
            "correct": torch.cat(correct) if correct else ce.new_zeros(0, dtype=torch.bool),
            "fill": (roles[masked] == FILL).detach(),
            "n_target": int((roles == TARGET).sum()), "n_tokens": x.numel()}

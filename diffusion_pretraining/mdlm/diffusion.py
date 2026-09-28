"""MDLM objective: absorbing-state (masking) diffusion with the log-linear schedule.

Forward process: every token becomes <mask> independently with probability t
(alpha_t = 1 - t). With the SUBS parameterisation (<mask> is never predicted and
unmasked tokens are copied through), the continuous-time NELBO per token is

    L = E_{t ~ U(eps, 1)} [ (1/t) * sum_{i masked} -log p(x_i | x_t) ] / L_seq

and exp(L) upper-bounds perplexity. Logits are only computed at masked positions.
"""
from __future__ import annotations

import torch
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint

EPS = 1e-3


def invalid_bias(padded_vocab: int, vocab_size: int, never: list[int], device=None) -> torch.Tensor:
    """-inf for ids the model must never output (<mask>, <pad>, <unk>, vocabulary padding)."""
    bias = torch.zeros(padded_vocab, device=device)
    bias[vocab_size:] = float("-inf")
    bias[never] = float("-inf")
    return bias


def sample_t(batch: int, device, generator: torch.Generator | None = None) -> torch.Tensor:
    """Low-discrepancy (antithetic) times: one uniform offset, evenly spread over the batch."""
    u = torch.rand((), device=device, generator=generator)
    t = (u + torch.arange(batch, device=device) / batch) % 1.0
    return EPS + (1 - EPS) * t


def forward_mask(x0: torch.Tensor, t: torch.Tensor, mask_id: int,
                 generator: torch.Generator | None = None) -> tuple[torch.Tensor, torch.Tensor]:
    masked = torch.rand(x0.shape, device=x0.device, generator=generator) < t[:, None]
    return torch.where(masked, torch.full_like(x0, mask_id), x0), masked


CE_CHUNK = 2048      # masked positions per logits chunk: bounds the 45.7k-wide logits to ~0.4 GB


def _ce_chunk(logits_fn, h: torch.Tensor, target: torch.Tensor, bias: torch.Tensor):
    logits = logits_fn(h).float() + bias
    return F.cross_entropy(logits, target, reduction="none"), logits.argmax(-1) == target


def nelbo(model, x0: torch.Tensor, mask_id: int, bias: torch.Tensor, t: torch.Tensor | None = None,
          generator: torch.Generator | None = None) -> dict:
    """NELBO (nats/token) of a batch, plus per-masked-token CE, correctness and their row's t.

    The output layer runs in chunks of masked positions; under autograd each chunk's
    logits are recomputed in the backward pass instead of being kept in memory."""
    if t is None:
        t = sample_t(x0.shape[0], x0.device, generator)
    xt, masked = forward_mask(x0, t, mask_id, generator)
    rows = masked.nonzero(as_tuple=True)[0]
    h, target = model.hidden(xt)[masked], x0[masked]
    ce, correct = [], []
    for hc, tc in zip(h.split(CE_CHUNK), target.split(CE_CHUNK)):
        if torch.is_grad_enabled():
            c, ok = checkpoint(_ce_chunk, model.logits, hc, tc, bias, use_reentrant=False)
        else:
            c, ok = _ce_chunk(model.logits, hc, tc, bias)
        ce.append(c)
        correct.append(ok)
    ce = torch.cat(ce) if ce else h.new_zeros(0, dtype=torch.float32)
    loss = (ce / t[rows]).sum() / x0.numel()
    return {"loss": loss, "ce": ce.detach(), "t": t[rows].detach(),
            "correct": torch.cat(correct) if correct else ce.new_zeros(0, dtype=torch.bool)}

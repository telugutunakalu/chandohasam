"""Sampling from a trained MDLM.

ancestral   MDLM's sampler: going from t to s < t, each still-masked position is
            revealed with probability (t - s) / t, its token drawn from p(x0 | x_t).
            The denoiser has no time input, so when a step reveals nothing the
            previous forward pass is reused (MDLM's caching).
confidence  MaskGIT/LLaDA-style: each step reveals the masked positions whose
            sampled token has the highest probability, on a linear schedule.

Categorical draws use Gumbel noise in float64: float32 noise is truncated and
quietly lowers the sampling temperature (Zheng et al. 2024), which flatters
generative perplexity while reducing diversity.
"""
from __future__ import annotations

import torch


def _gumbel_draw(logits: torch.Tensor, generator: torch.Generator | None) -> tuple[torch.Tensor, torch.Tensor]:
    """Sample one id per row in float64; also return the sampled token's probability."""
    out, prob = [], []
    for chunk in logits.split(1024):
        lp = torch.log_softmax(chunk.double(), dim=-1)
        u = torch.rand(lp.shape, dtype=torch.float64, device=lp.device, generator=generator).clamp_(1e-300, 1.0)
        ids = (lp - torch.log(-torch.log(u))).argmax(-1)
        out.append(ids)
        prob.append(lp.gather(-1, ids[:, None]).squeeze(-1).exp())
    return torch.cat(out), torch.cat(prob)


@torch.no_grad()
def sample(model, n: int, length: int, steps: int, mask_id: int, bias: torch.Tensor,
           strategy: str = "ancestral", prefix: torch.Tensor | None = None,
           generator: torch.Generator | None = None, amp_dtype=torch.bfloat16) -> tuple[torch.Tensor, int]:
    """Generate ``n`` sequences of ``length`` tokens. Returns (ids, number of forward passes).

    ``prefix`` (n, k) fixes the first k tokens (kept unmasked throughout)."""
    device = bias.device
    x = torch.full((n, length), mask_id, dtype=torch.long, device=device)
    if prefix is not None:
        x[:, : prefix.shape[1]] = prefix
    ts = torch.linspace(1.0, 0.0, steps + 1, dtype=torch.float64)
    hidden, nfe = None, 0
    autocast = torch.autocast(device.type, dtype=amp_dtype, enabled=device.type == "cuda")
    for k in range(steps):
        masked = x == mask_id
        if not masked.any():
            break
        if hidden is None:
            with autocast:
                hidden = model.hidden(x)
            nfe += 1
        t, s = float(ts[k]), float(ts[k + 1])
        pos = masked.nonzero(as_tuple=True)
        ids, prob = [], []
        for h in hidden[pos].split(2048):                 # bound the 45.7k-wide logits in memory
            with autocast:
                logits = model.logits(h)
            i, p = _gumbel_draw(logits.float() + bias, generator)
            ids.append(i)
            prob.append(p)
        ids, prob = torch.cat(ids), torch.cat(prob)
        if strategy == "ancestral":
            reveal = torch.rand(ids.shape, device=device, generator=generator, dtype=torch.float64) < (t - s) / t
        elif strategy == "confidence":
            reveal = torch.zeros_like(ids, dtype=torch.bool)
            for row in range(n):
                sel = (pos[0] == row).nonzero(as_tuple=True)[0]
                if len(sel):
                    k_row = max(1, round(len(sel) * (t - s) / t))
                    reveal[sel[prob[sel].topk(min(k_row, len(sel))).indices]] = True
        else:
            raise ValueError(strategy)
        if reveal.any():
            x[pos[0][reveal], pos[1][reveal]] = ids[reveal]
            hidden = None                         # the input changed: recompute next step
    return x, nfe

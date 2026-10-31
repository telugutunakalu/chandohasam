"""A settled-commit variant of our constrained diffusion decoder (metrical_decoder.diffusion.decoding), for E6.

Our decoder (September) commits the token at the left edge of the open canvas on **every** denoising pass: its run of
accepted proposals always takes the first one, whatever its entropy. From a canvas that is still noise, that first
prediction is nearly uniform over the allowed aksharas (2026-10-21, the 48k adapter: entropy 3–5 nats at the first
commits, 96–99.8% of the mass on allowed tokens), so the poem is assembled from first-pass guesses — metrical
akshara soup. The model's own sampler instead commits its most confident positions anywhere on the canvas and lets
the rest keep denoising.

`SettledRun` keeps everything of `_Run` (checkpoints, backtracking, temperature schedule, masks, the forced line
ends, the trace) and adds one rule: the left edge **waits** — the canvas keeps denoising with the frozen prefix — until
the model's (temperature-scaled) prediction there has entropy ≤ `h_commit`, or `max_wait` passes have gone by; only
then does the pass accept proposals or let the constraint decide. Forced line ends are unchanged.

Owns: SettledRun, decode_settled (the decode_fn for metrical_decoder.runner.run_grid). Does not modify the shared
package.
"""
from __future__ import annotations

import time
from dataclasses import asdict

from metrical_decoder.diffusion import decoding as D

H_COMMIT, MAX_WAIT = 0.3, 16


class SettledRun(D._Run):
    def __init__(self, *args, h_commit: float = H_COMMIT, max_wait: int = MAX_WAIT, **kwargs):
        super().__init__(*args, **kwargs)
        self.h_commit, self.max_wait = h_commit, max_wait
        self.waited, self.waits = 0, 0

    def accept_proposals(self, p, tau, budget):
        pos = p.first
        if pos < self.canvas.canvas_length and p.entropy(pos) > self.h_commit and self.waited < self.max_wait:
            self.waited += 1                          # keep denoising: no commit and no decision on this pass
            self.waits += 1
            return True
        self.waited = 0
        return super().accept_proposals(p, tau, budget)

    def run(self) -> dict:
        out = super().run()
        out.update(n_waits=self.waits, h_commit=self.h_commit, max_wait=self.max_wait)
        return out


def decode_settled(enforcer, index, canvas, prompt_ids, mode: str, seed: int = 42,
                   cfg: D.DiffusionConfig = D.DiffusionConfig(), masks=None) -> dict:
    """metrical_decoder.diffusion.decoding.decode_diffusion with SettledRun for the constrained modes."""
    if mode == "baseline":
        return D.decode_diffusion(enforcer, index, canvas, prompt_ids, mode, seed, cfg, masks)
    masks = masks or D.MaskCache(enforcer, index)
    t0 = time.time()
    canvas.start(prompt_ids, seed)
    out = SettledRun(enforcer, index, canvas, mode, seed, cfg, masks).run()
    out.update(mode=mode, seed=seed, seconds=round(time.time() - t0, 3), config=asdict(cfg), decoder="settled")
    return out

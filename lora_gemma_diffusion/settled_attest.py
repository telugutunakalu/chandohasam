"""Layer B of the v2 constraint (word attestation, metrical_decoder.attestation) in the settled diffusion decoder, for
the full grid's v2 cells (full_grid_experiments/README.md decision 22).

The autoregressive decoder applies Layer B where it draws a token: the allowed tokens' probabilities × exp(weight ×
score), renormalised, where score is 2 when the word so far begins a corpus word, 1 when it occurs inside one, else 0
(`reweight`). With ``where="override"`` only where the model's own first choice is not allowed; with ``"all"`` at every
step. The diffusion decoder commits tokens in two ways, and `AttestedRun` reweights both:

- **the constraint decides** (`decide`: the model's proposal at the first open position is not allowed): the draw from
  the prediction restricted to the allowed tokens is reweighted — both settings;
- **a run of the model's proposals** (`accept_proposals`, ``"all"`` only): the run still ends where the model's own
  proposal is not allowed or the run stops being jointly confident (the model's acceptance rule, unchanged), but each
  accepted position commits a reweighted draw from its prediction restricted to the allowed tokens instead of the
  proposal itself. The positions of one pass are sampled independently given the canvas, so a redrawn token breaks no
  dependency the model's proposals had. The trace marks such a token ``how="attest"`` when it differs from the
  proposal.

Everything else is `settled.SettledRun` (the left edge waits until it is confident; checkpoints, backtracking, the
temperature schedule, forced line ends). Hybrid is not supported with ``"all"``. Layer A (the syllable inventory) is
the enforcer's, given to run_grid (``inventory=``). Does not modify the shared package or settled.py.

Owns: AttestedRun, decode_settled_attest (the decode_fn for metrical_decoder.runner.run_grid).
"""
from __future__ import annotations

import os
import time
from dataclasses import asdict

from metrical_decoder.attestation import load_attestation, reweight
from metrical_decoder.diffusion import decoding as D
from settled import SettledRun

# the T5 1B v2 A+B setting (t5_finetuning/runs/e6_t5g_1b_val_c_v2); overridable for tests
WEIGHT = float(os.environ.get("V2_ATTEST_WEIGHT", 2.0))
WHERE = os.environ.get("V2_ATTEST_WHERE", "all")
CORPUS = os.environ.get("V2_ATTEST_CORPUS", "padyarchana")


class AttestedRun(SettledRun):
    def __init__(self, *args, weight: float = WEIGHT, where: str = WHERE, corpus: str = CORPUS, **kwargs):
        super().__init__(*args, **kwargs)
        if where == "all" and self.mode == "hybrid":
            raise ValueError("hybrid with Layer B at every step is not supported")
        self.att = load_attestation(corpus)
        self.weight, self.where, self.corpus = weight, where, corpus
        self.n_attest, self.n_changed = 0, 0

    def attested(self, dist, valid, tau) -> tuple[int, float, int]:
        """A draw from the prediction restricted to the allowed tokens at ``tau``, × exp(weight × score)."""
        probs, scores = reweight(D._scaled(dist, valid, tau), self.state.word, self.index.texts, self.weight, self.att)
        slot, p_pick = D.draw(probs, self.rng)
        self.n_attest += 1
        return slot, p_pick, scores[slot]

    def accept_proposals(self, p, tau, budget):
        pos = p.first
        if pos < self.canvas.canvas_length and p.entropy(pos) > self.h_commit and self.waited < self.max_wait:
            self.waited += 1                          # settled.SettledRun: keep denoising, the left edge is not sure
            self.waits += 1
            return True
        self.waited = 0
        if self.where != "all":
            return D._Run.accept_proposals(self, p, tau, budget)
        cfg, index = self.cfg, self.index
        run, h_sum, h_max = 0, 0.0, 0.0
        while pos < self.canvas.canvas_length and len(self.out) < budget and not self.enf.poem_complete(self.state):
            tid, h = p.proposal(pos), p.entropy(pos)
            if run and (h_sum + h) - max(h_max, h) > cfg.entropy_bound:
                break
            slot = index.position(tid)
            valid = self.valid(self.state)
            if slot is None or slot not in valid:
                break
            pick, p_pick, score = self.attested(p.distribution(pos), valid, tau)
            self.n_changed += pick != slot
            self.commit(p, pos, index.ids[pick], "proposal" if pick == slot else "attest", p_pick, tau, valid, run)
            self.trace[-1]["attest"] = score
            run, h_sum, h_max, pos = run + 1, h_sum + h, max(h_max, h), pos + 1
        if run:
            self.consecutive = 0
        return run > 0

    def decide(self, p, tau):
        """decoding._Run.decide with the masked draw reweighted (hybrid: unchanged)."""
        cfg, pos = self.cfg, p.first
        valid = self.valid(self.state)
        dist = p.distribution(pos)
        vmass = D._mass(dist, valid) if valid else 0.0
        reason = None
        if not valid:
            reason = "empty"
        elif self.mode == "masking_backtrack":
            if len(valid) < cfg.min_valid:
                reason = "few_valid"
            elif vmass < cfg.min_valid_mass:
                reason = "mass_collapse"
            elif self.stall >= cfg.stall_limit:
                reason = "stall"
        if reason and self.mode != "masking_only" and self.ckpts and self.backtracks < cfg.max_backtracks:
            self.backtrack(reason, len(valid), vmass)
            return "backtracked"
        if not valid:
            return "dead_end"
        score = None
        if self.mode == "hybrid":
            pool, _ = self.preferred(p, pos, valid, tau)
            slot, p_pick = D.draw(pool, self.rng)
            how = "rerank"
        else:
            slot, p_pick, score = self.attested(dist, valid, tau)
            how = "masked"
        self.commit(p, pos, self.index.ids[slot], how, p_pick, tau, valid)
        if score is not None:
            self.trace[-1]["attest"] = score
        self.consecutive = 0
        return "committed"

    def run(self) -> dict:
        out = super().run()
        out.update(attest={"weight": self.weight, "where": self.where, "corpus": self.corpus,
                           "draws": self.n_attest, "changed_proposals": self.n_changed})
        return out


def decode_settled_attest(enforcer, index, canvas, prompt_ids, mode: str, seed: int = 42,
                          cfg: D.DiffusionConfig = D.DiffusionConfig(), masks=None) -> dict:
    """settled.decode_settled with AttestedRun for the constrained modes (free generation is unchanged)."""
    if mode == "baseline":
        return D.decode_diffusion(enforcer, index, canvas, prompt_ids, mode, seed, cfg, masks)
    masks = masks or D.MaskCache(enforcer, index)
    t0 = time.time()
    canvas.start(prompt_ids, seed)
    out = AttestedRun(enforcer, index, canvas, mode, seed, cfg, masks).run()
    out.update(mode=mode, seed=seed, seconds=round(time.time() - t0, 3), config=asdict(cfg), decoder="settled+attest")
    return out

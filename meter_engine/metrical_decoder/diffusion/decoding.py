# -*- coding: utf-8 -*-
"""
The three constrained strategies on a diffusion model: a frozen prefix that grows from the left.

The enforcer is exact for *prefixes*: every committed token must keep the poem
completable. A diffusion model, though, predicts every position of its block at
once and commits them in any order. The loop here reconciles the two (plan §13,
route 1): the block is decided left to right, and each denoising pass does as
much as the model's own predictions allow.

One pass (see :mod:`.canvas`) gives, for every open position, a token sampled
from the model's temperature-scaled prediction (its *proposal*) and that
prediction's entropy. Then, from the first open position:

1. **forced line end** — when the line cannot continue, the line break is
   committed (the model's own proposal, if it is the line break);
2. **the model's proposals**, left to right, while each one is allowed by the
   enforcer and the run stays jointly confident — the model's own acceptance
   rule, ``Σ entropy − max entropy ≤ entropy_bound`` (``EntropyBoundSampler``),
   applied to the contiguous run. The first proposal needs only to be allowed;
3. **otherwise the constraint decides** the first open position, by strategy:

   * ``masking_only`` — a draw from the model's prediction restricted to the
     allowed tokens (temperature-scaled, renormalised);
   * ``masking_backtrack`` — the same, unless the allowed set is nearly empty
     (< 3 tokens), the model gives it almost no mass (< 1e-3) or the line has
     stalled; then the last few committed tokens are unfrozen (returned to
     noise) and the temperature raised (+0.15 per consecutive backtrack, up to
     1.2, easing off over 6 tokens) — the paper's Alg. 5, where diffusion makes
     rewinding cheap: nothing is cached for the block, the next pass simply
     sees a shorter frozen prefix and fresh noise after it;
   * ``hybrid`` — the paper's Alg. 6: among the 100 most probable allowed
     tokens, prefer those that complete the line (up to 3), else the 10 most
     probable. In ``hybrid`` a proposal is also accepted in step 2 only if it
     is in that preferred set.

Every pass commits at least one token or backtracks, so the loop ends; with an
exact enforcer and :func:`~metrical_decoder.strategies.token_budget` tokens it
cannot miss the end of the poem. When the block is full it is encoded into the
context and a new block opens.

``baseline`` is free generation in the same loop, the constraint removed — the
diffusion counterpart of the autoregressive baseline: each pass keeps the
model's proposals from the first open position while the run is jointly
confident (the first one always), over the whole vocabulary; the model may end
its reply (end-of-text is never removed from its predictions here, whatever the
canvas's ``forbid_end``), and the reply ends at its first end token or after
3 × the meter's longest poem + 32 tokens. The enforcer only watches, as in the
autoregressive baseline: while the text is still in meter every record carries
the allowed set's size and mass, and the result says where the text left the
meter (``left_meter_at``) and whether it is a complete poem in meter.

The temperature follows the model's own schedule: 0.8 at a block's first pass,
falling linearly to 0.4 at pass 48 (``generation_config.json``), plus the
backtracking boost. No top-p (the model's sampler has none).

The trace has one record per committed token, with the same fields as the
autoregressive trace (``logp``, ``rank``, ``p_pick``, ``n_valid``,
``valid_mass``, ``H``, ``tau``, ``top``, ``line``, ``akshara``) and the
diffusion ones: ``block``, ``pass``, ``canvas_pos``, ``run`` (position in the
pass's accepted run) and ``how`` — ``proposal`` (the model's own sampled token),
``masked``, ``rerank`` or ``forced_nl``; plus one record per backtrack.

Owns: :class:`DiffusionConfig`, :func:`decode_diffusion`. Must not import torch.
"""
from __future__ import annotations

import math
import random
import time
from dataclasses import asdict, dataclass
from typing import Optional, Sequence

from ..enforcer import DecodeState, Enforcer
from ..sources import Distribution, draw
from ..strategies import MaskCache, token_budget
from ..vocab import TokenIndex
from .canvas import Canvas, Pass

CONSTRAINED = ("masking_only", "masking_backtrack", "hybrid")
MODES = ("baseline",) + CONSTRAINED


@dataclass(frozen=True)
class DiffusionConfig:
    # the model's own sampling recipe (DiffusionGemma's generation_config.json)
    t_max: float = 0.8                   # temperature at a block's first pass
    t_min: float = 0.4                   # … reached at pass ``schedule_passes``, kept after
    schedule_passes: int = 48
    entropy_bound: float = 0.1           # a run of proposals is kept while Σ H − max H ≤ bound
    # constrained decoding, as in the autoregressive strategies
    k_rerank: int = 100                  # hybrid: K_r
    max_tokens: Optional[int] = None     # default: strategies.token_budget (enough for any poem)
    checkpoint_every: int = 3            # passes between checkpoints (backtracking)
    checkpoint_cap: int = 15
    max_backtracks: int = 30
    tau_step: float = 0.15
    tau_max: float = 1.2
    tau_decay: int = 6
    min_valid: int = 3
    min_valid_mass: float = 1e-3
    stall_limit: int = 4
    force_nl: str = "must_end"           # or "on_accept"
    trace_top: int = 5
    # free generation (baseline), as in the autoregressive DecodeConfig
    baseline_max_tokens: Optional[int] = None   # default 3 × the meter's longest poem + 32
    watch_baseline: bool = True          # record the allowed set while the free text is still in meter


def scheduled_temperature(cfg: DiffusionConfig, passes_in_block: int) -> float:
    """The model's linear schedule: ``t_max`` at a block's first pass, ``t_min`` from pass ``schedule_passes``.

    >>> [round(scheduled_temperature(DiffusionConfig(), n), 3) for n in (0, 24, 48, 90)]
    [0.8, 0.6, 0.4, 0.4]
    """
    remaining = max(cfg.schedule_passes - passes_in_block, 0)
    return cfg.t_min + (cfg.t_max - cfg.t_min) * remaining / cfg.schedule_passes


def _mass(dist: Distribution, valid: Sequence[int]) -> float:
    return sum(math.exp(dist.slice_logits[i] - dist.lse) for i in valid)


def _scaled(dist: Distribution, valid: Sequence[int], tau: float) -> dict[int, float]:
    """The prediction restricted to ``valid`` slice positions, at temperature ``tau``, renormalised."""
    m = max(dist.slice_logits[i] for i in valid)
    w = {i: math.exp((dist.slice_logits[i] - m) / tau) for i in valid}
    tot = sum(w.values())
    return {i: x / tot for i, x in w.items()}


def decode_diffusion(enforcer: Enforcer, index: TokenIndex, canvas: Canvas, prompt_ids: Sequence[int],
                     mode: str, seed: int = 42, cfg: DiffusionConfig = DiffusionConfig(),
                     masks: Optional[MaskCache] = None) -> dict:
    """Generate one poem with a diffusion model; returns text, ids, status, statistics and the trace
    (the same row shape as :func:`metrical_decoder.strategies.decode`)."""
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}")
    masks = masks or MaskCache(enforcer, index)
    t0 = time.time()
    canvas.start(prompt_ids, seed)
    if mode == "baseline":
        forbid, canvas.forbid_end = canvas.forbid_end, False         # free generation may end its reply
        try:
            out = _Baseline(enforcer, index, canvas, seed, cfg, masks).run()
        finally:
            canvas.forbid_end = forbid
    else:
        out = _Run(enforcer, index, canvas, mode, seed, cfg, masks).run()
    out.update(mode=mode, seed=seed, seconds=round(time.time() - t0, 3), config=asdict(cfg))
    return out


class _Run:
    """One poem: the committed tokens, the open block's frozen prefix and the loop's counters."""

    def __init__(self, enf: Enforcer, index: TokenIndex, canvas: Canvas, mode: str, seed: int,
                 cfg: DiffusionConfig, masks: MaskCache):
        self.enf, self.index, self.canvas, self.mode, self.cfg, self.masks = enf, index, canvas, mode, cfg, masks
        self.rng = random.Random(seed)
        self.state: DecodeState = enf.initial()
        self.out: list[int] = []                      # committed token ids (the poem)
        self.block: list[int] = []                    # committed ids of the open block = its frozen prefix
        self.trace: list[dict] = []
        self.ckpts: list[tuple[int, int, DecodeState, float]] = []   # (len out, len block, state, boost)
        self.boost, self.decay_left = 0.0, 0
        self.backtracks, self.consecutive = 0, 0
        self.stall, self.progress = 0, (0, 0)
        self.passes, self.blocks = 0, 0
        self.n_masks, self.mask_seconds = 0, 0.0
        self.nl_id = index.ids[index.newline]

    # ------------------------------------------------------------ the loop
    def run(self) -> dict:
        cfg, enf = self.cfg, self.enf
        budget = token_budget(enf, cfg)
        status = "budget"
        while len(self.out) < budget and self.passes < (cfg.max_backtracks + 2) * budget:
            if enf.poem_complete(self.state):
                status = "complete"
                break
            if len(self.block) == self.canvas.canvas_length:          # the block is decided: next block
                self.canvas.close_block(self.block)
                self.block, self.blocks = [], self.blocks + 1
                self.ckpts.clear()                                    # a closed block cannot be rewound
            if self.mode != "masking_only" and self.passes % cfg.checkpoint_every == 0:
                self.ckpts.append((len(self.out), len(self.block), self.state, self.boost))
                del self.ckpts[:-cfg.checkpoint_cap]
            tau = self.temperature()
            p = self.canvas.denoise(self.block, tau)
            self.passes += 1
            if self.forced_line_end(p, tau) or self.accept_proposals(p, tau, budget):
                continue
            if self.decide(p, tau) == "dead_end":
                status = "dead_end"
                break
        if status == "budget" and enf.poem_complete(self.state):
            status = "complete"                                       # the budget's last token ended the poem
        texts = [self.index.texts[self.index.position(t)] for t in self.out]
        return {"status": status, "text": "".join(texts), "ids": list(self.out), "n_tokens": len(self.out),
                "n_passes": self.passes, "n_blocks": self.blocks + 1, "n_backtracks": self.backtracks,
                "tokens_per_pass": round(len(self.out) / max(self.passes, 1), 3),
                "n_masks": self.n_masks, "ms_per_mask": round(1000 * self.mask_seconds / max(self.n_masks, 1), 2),
                "mask_cache": {"hits": self.masks.hits, "misses": self.masks.misses}, "trace": self.trace}

    def temperature(self) -> float:
        tau = scheduled_temperature(self.cfg, self.canvas.passes_in_block)
        return min(tau + self.boost, self.cfg.tau_max) if self.boost else tau

    # ------------------------------------------------------------ the three steps of a pass
    def forced_line_end(self, p: Pass, tau: float) -> bool:
        """1. The line cannot continue: commit the line break."""
        enf = self.enf
        forced = enf.must_end_line(self.state) if self.cfg.force_nl == "must_end" else enf.line_complete(self.state)
        if not forced:
            return False
        pos = p.first
        how = "proposal" if p.proposal(pos) == self.nl_id else "forced_nl"
        self.commit(p, pos, self.nl_id, how, 1.0 if how == "forced_nl" else p.p_scaled(pos, self.nl_id), tau)
        self.consecutive = 0
        return True

    def accept_proposals(self, p: Pass, tau: float, budget: int) -> bool:
        """2. The model's own proposals, left to right, while allowed and jointly confident."""
        cfg, index = self.cfg, self.index
        pos, run, h_sum, h_max = p.first, 0, 0.0, 0.0
        while pos < self.canvas.canvas_length and len(self.out) < budget and not self.enf.poem_complete(self.state):
            tid, h = p.proposal(pos), p.entropy(pos)
            if run and (h_sum + h) - max(h_max, h) > cfg.entropy_bound:
                break
            slot = index.position(tid)
            valid = self.valid(self.state)
            if slot is None or slot not in valid:
                break
            if self.mode == "hybrid" and slot not in self.preferred(p, pos, valid, tau)[0]:
                break                                              # hybrid keeps only proposals it would pick
            self.commit(p, pos, tid, "proposal", p.p_scaled(pos, tid), tau, valid, run)
            run, h_sum, h_max, pos = run + 1, h_sum + h, max(h_max, h), pos + 1
        if run:
            self.consecutive = 0
        return run > 0

    def decide(self, p: Pass, tau: float) -> str:
        """3. The model's proposal at the first open position is not allowed: the constraint decides."""
        cfg, pos = self.cfg, p.first
        valid = self.valid(self.state)
        dist = p.distribution(pos)
        vmass = _mass(dist, valid) if valid else 0.0
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
        if self.mode == "hybrid":
            pool, completes = self.preferred(p, pos, valid, tau)
            slot, p_pick = draw(pool, self.rng)
            how = "rerank"
        else:
            slot, p_pick = draw(_scaled(dist, valid, tau), self.rng)
            how = "masked"
        self.commit(p, pos, self.index.ids[slot], how, p_pick, tau, valid)
        self.consecutive = 0
        return "committed"

    # ------------------------------------------------------------ helpers
    def valid(self, state: DecodeState) -> frozenset[int]:
        tm = time.time()
        v = self.masks.valid(state)
        self.mask_seconds += time.time() - tm
        self.n_masks += 1
        return frozenset(v)

    def preferred(self, p: Pass, pos: int, valid: frozenset[int], tau: float) -> tuple[dict[int, float], bool]:
        """Hybrid (Alg. 6): of the ``k_rerank`` most probable allowed tokens, the first 3 that complete the
        line, else the first 10; returned as a renormalised distribution, and whether they complete the line."""
        probs = _scaled(p.distribution(pos), valid, tau)
        accept: dict[int, float] = {}
        alive: dict[int, float] = {}
        for slot, q in sorted(probs.items(), key=lambda kv: -kv[1])[: self.cfg.k_rerank]:
            if q < 1e-8:
                break
            nxt = self.enf.step(self.state, self.index.texts[slot])
            if nxt is not None and self.enf.line_complete(nxt):
                accept[slot] = q
            alive[slot] = q
            if len(accept) >= 3 or (len(alive) >= 10 and not accept):
                break
        pool = accept or alive
        tot = sum(pool.values())
        return {s: q / tot for s, q in pool.items()}, bool(accept)

    def commit(self, p: Pass, pos: int, tid: int, how: str, p_pick: float, tau: float,
               valid: Optional[frozenset[int]] = None, run: int = 0) -> None:
        """Freeze ``tid`` at canvas position ``pos`` and record it."""
        index = self.index
        slot = index.position(tid)
        text = index.texts[slot]
        new = self.enf.step(self.state, text)
        if new is None:
            raise AssertionError(f"committed a token the enforcer rejects: {text!r}")
        if valid is None:
            valid = self.valid(self.state)
        dist = p.distribution(pos)
        rec = {
            "pos": len(self.out), "id": tid, "text": text, "how": how,
            "logp": round(dist.slice_logits[slot] - dist.lse, 6), "rank": p.rank(pos, tid),
            "p_pick": round(p_pick, 6), "n_valid": len(valid), "valid_mass": round(_mass(dist, valid), 6),
            "H": round(dist.entropy, 5), "tau": round(tau, 3),
            "top": [[t, self._text(t), round(math.exp(z - dist.lse), 6), self._ok(t, valid)]
                    for t, z in dist.top[: self.cfg.trace_top]],
            "line": new.lines, "akshara": self.enf.akshara(new),
            "block": self.blocks, "pass": self.passes, "canvas_pos": pos, "run": run,
        }
        self.trace.append(rec)
        self.out.append(tid)
        self.block.append(tid)
        self.state = new
        now = (new.lines, self.enf.akshara(new))
        self.stall = 0 if now != self.progress else self.stall + 1
        self.progress = now
        if self.decay_left:
            self.decay_left -= 1
            if not self.decay_left:
                self.boost = 0.0

    def backtrack(self, reason: str, n_valid: int, vmass: float) -> None:
        """Unfreeze back to a checkpoint: the tokens return to noise; the temperature rises."""
        cfg = self.cfg
        self.backtracks += 1
        self.consecutive += 1
        for _ in range(min(self.consecutive, len(self.ckpts)) - 1):
            self.ckpts.pop()
        keep, keep_block, state, boost = self.ckpts.pop()
        del self.out[keep:]
        del self.block[keep_block:]
        self.canvas.forget(keep_block)                 # the unfrozen positions return to noise
        self.state = state
        self.boost = min(boost + cfg.tau_step * self.consecutive, cfg.tau_max)
        self.decay_left = cfg.tau_decay
        self.stall, self.progress = 0, (state.lines, self.enf.akshara(state))
        self.trace.append({"how": "backtrack", "reason": reason, "to": keep, "boost": round(self.boost, 3),
                           "n_valid": n_valid, "valid_mass": round(vmass, 6), "pass": self.passes})

    def _text(self, tid: int) -> str:
        slot = self.index.position(tid)
        return self.index.texts[slot] if slot is not None else self.canvas.decode([tid])

    def _ok(self, tid: int, valid: frozenset[int]) -> bool:
        slot = self.index.position(tid)
        return slot is not None and slot in valid


class _Baseline:
    """Free generation: the loop of :class:`_Run` without the constraint; the enforcer only watches."""

    def __init__(self, enf: Enforcer, index: TokenIndex, canvas: Canvas, seed: int, cfg: DiffusionConfig,
                 masks: MaskCache):
        self.enf, self.index, self.canvas, self.cfg, self.masks = enf, index, canvas, cfg, masks
        self.end = set(index.eos_ids) | set(canvas.end_token_ids)
        self.state: Optional[DecodeState] = enf.initial()
        self.out: list[int] = []
        self.block: list[int] = []
        self.text = ""
        self.left_meter_at: Optional[int] = None
        self.trace: list[dict] = []
        self.passes, self.blocks = 0, 0
        self.n_masks, self.mask_seconds = 0, 0.0

    def run(self) -> dict:
        cfg, canvas = self.cfg, self.canvas
        budget = cfg.baseline_max_tokens or 3 * self.enf.max_aksharas() + 32
        status = "budget"
        while status == "budget" and len(self.out) < budget:
            if len(self.block) == canvas.canvas_length:           # the block is decided: next block
                canvas.close_block(self.block)
                self.block, self.blocks = [], self.blocks + 1
            tau = scheduled_temperature(cfg, canvas.passes_in_block)
            p = canvas.denoise(self.block, tau)
            self.passes += 1
            pos, run, h_sum, h_max = p.first, 0, 0.0, 0.0
            while pos < canvas.canvas_length and len(self.out) < budget:
                tid, h = p.proposal(pos), p.entropy(pos)
                if run and (h_sum + h) - max(h_max, h) > cfg.entropy_bound:
                    break
                if self.commit(p, pos, tid, tau, run):
                    status = "eos"
                    break
                run, h_sum, h_max, pos = run + 1, h_sum + h, max(h_max, h), pos + 1
        return {"status": status, "text": self.text, "ids": list(self.out), "n_tokens": len(self.out),
                "left_meter_at": self.left_meter_at,
                "complete_in_meter": self.state is not None and self.enf.poem_complete(self.state),
                "n_passes": self.passes, "n_blocks": self.blocks + 1,
                "tokens_per_pass": round(len(self.out) / max(self.passes, 1), 3),
                "n_masks": self.n_masks, "ms_per_mask": round(1000 * self.mask_seconds / max(self.n_masks, 1), 2),
                "mask_cache": {"hits": self.masks.hits, "misses": self.masks.misses}, "trace": self.trace}

    def commit(self, p: Pass, pos: int, tid: int, tau: float, run: int) -> bool:
        """Record the model's token at ``pos`` and, unless it ends the reply, append it. True at the end."""
        valid = None
        if self.state is not None and self.cfg.watch_baseline:
            tm = time.time()
            valid = frozenset(self.masks.valid(self.state))
            self.mask_seconds += time.time() - tm
            self.n_masks += 1
        dist = p.distribution(pos)
        ended = tid in self.end
        if ended:
            piece = self.canvas.decode([tid])
        else:
            new_text = self.canvas.decode(self.out + [tid])
            piece, self.text = new_text[len(self.text):], new_text
            if self.state is not None:
                nxt = self.enf.step(self.state, piece)
                if nxt is None:
                    self.left_meter_at = len(self.out)
                self.state = nxt
        rec = {
            "pos": len(self.out), "id": tid, "text": piece, "how": "eos" if ended else "proposal",
            "logp": round(p.logp(pos, tid), 6), "rank": p.rank(pos, tid), "p_pick": round(p.p_scaled(pos, tid), 6),
            "n_valid": None if valid is None else len(valid),
            "valid_mass": None if valid is None else round(_mass(dist, valid), 6),
            "H": round(dist.entropy, 5), "tau": round(tau, 3),
            "top": [[t, self._text(t), round(math.exp(z - dist.lse), 6),
                     None if valid is None else (self.index.position(t) is not None and self.index.position(t) in valid)]
                    for t, z in dist.top[: self.cfg.trace_top]],
            "block": self.blocks, "pass": self.passes, "canvas_pos": pos, "run": run,
        }
        if not ended and self.state is not None:
            rec["line"], rec["akshara"] = self.state.lines, self.enf.akshara(self.state)
        if not ended and self.state is None:
            rec["in_meter"] = False
        self.trace.append(rec)
        if not ended:
            self.out.append(tid)
            self.block.append(tid)
        return ended

    def _text(self, tid: int) -> str:
        slot = self.index.position(tid)
        return self.index.texts[slot] if slot is not None else self.canvas.decode([tid])

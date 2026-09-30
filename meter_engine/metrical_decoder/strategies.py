# -*- coding: utf-8 -*-
"""
The three IndicNeuroSym decoding strategies on the DAWG enforcer, and the
unconstrained baseline, each with a per-token trace.

====================  =====================================================================
``baseline``          sample the whole vocabulary (τ, top-p) until EOS; the enforcer only
                      watches, and the trace records where the text first leaves the meter
``masking_only``      paper Alg. 5 with backtracking off
``masking_backtrack`` paper Alg. 5: checkpoint every 3 tokens (ring of 15); backtrack when
                      ``|V| < 3``, when the valid mass falls below ε, or on a stall;
                      τ + 0.15 per consecutive backtrack (cap 1.2, decays over 6 tokens)
``hybrid``            paper Alg. 6: the same mask, then an accept-state re-ranking pass over
                      the top-K_r masked candidates that prefers line-completing tokens;
                      backtracking only as a last resort
====================  =====================================================================

The trace has one record per generated token (and one per backtrack): the
token's probability under the model over the whole vocabulary at T = 1
(``logp``), its rank there, the probability it was actually drawn with
(``p_pick``), the size and model probability of the valid set (``n_valid``,
``valid_mass``), the entropy, and the model's own top-k with each candidate's
validity. Together they show how far the model's distribution is from the
meter at every step.

Differences from the paper that the DAWG forces (none is tuning): the
"line longer than 15 syllables" trigger is gone (an exact mask cannot
overshoot), and ⏎ is forced only when the line cannot continue
(``force_nl="must_end"``; ``"on_accept"`` restores the paper's rule).

Owns: :class:`DecodeConfig`, :func:`decode`. Must not import torch.
"""
from __future__ import annotations

import math
import random
import time
from collections import OrderedDict
from dataclasses import asdict, dataclass
from typing import Optional, Sequence

from . import orthography as ortho
from .enforcer import DecodeState, Enforcer
from .sources import Distribution, LogitsSource, draw, top_p_filter
from .vocab import TokenIndex

MODES = ("baseline", "masking_only", "masking_backtrack", "hybrid")


@dataclass(frozen=True)
class DecodeConfig:
    temperature: float = 0.7
    top_p: float = 0.9
    k_rerank: int = 100                  # hybrid: K_r
    max_tokens: Optional[int] = None     # constrained budget; default: enough for any poem (token_budget)
    baseline_max_tokens: Optional[int] = None   # baseline budget; default 3 × longest poem + 32 (room for the poem, not for notes)
    checkpoint_every: int = 3
    checkpoint_cap: int = 15
    max_backtracks: int = 30
    tau_step: float = 0.15
    tau_max: float = 1.2
    tau_decay: int = 6
    min_valid: int = 3                   # paper's trigger
    min_valid_mass: float = 1e-3         # the model's mass on V collapsed
    stall_limit: int = 4                 # tokens in a row without a new syllable
    force_nl: str = "must_end"           # or "on_accept" (paper)
    trace_top: int = 5
    watch_baseline: bool = True          # baseline: compute masks while the text is still in the meter


class MaskCache:
    """Valid slice positions per enforcer state (LRU; states recur across seeds and backtracks)."""

    def __init__(self, enforcer: Enforcer, index: TokenIndex, maxsize: int = 4096):
        self.enforcer = enforcer
        self.index = index
        self.maxsize = maxsize
        self._cache: OrderedDict = OrderedDict()
        self.hits = 0
        self.misses = 0

    def valid(self, state: DecodeState) -> tuple[int, ...]:
        v = self._cache.get(state)
        if v is not None:
            self._cache.move_to_end(state)
            self.hits += 1
            return v
        self.misses += 1
        v = self._compute(state)
        self._cache[state] = v
        if len(self._cache) > self.maxsize:
            self._cache.popitem(last=False)
        return v

    def _compute(self, state: DecodeState) -> tuple[int, ...]:
        step = self.enforcer.step
        return tuple(i for i, t in enumerate(self.index.texts) if step(state, t) is not None)


def _mass(dist: Distribution, positions: Sequence[int]) -> float:
    return sum(math.exp(dist.slice_logits[i] - dist.lse) for i in positions)


def _probs(dist: Distribution, positions: Sequence[int], tau: float) -> dict[int, float]:
    m = max(dist.slice_logits[i] for i in positions)
    w = {i: math.exp((dist.slice_logits[i] - m) / tau) for i in positions}
    tot = sum(w.values())
    return {i: x / tot for i, x in w.items()}


class _Tracer:
    def __init__(self, source: LogitsSource, index: TokenIndex, enforcer: Enforcer, top: int):
        self.source, self.index, self.enforcer, self.top = source, index, enforcer, top
        self.records: list[dict] = []
        self._text: dict[int, str] = {}

    def text(self, tid: int) -> str:
        t = self._text.get(tid)
        if t is None:
            pos = self.index.position(tid)
            t = self.index.texts[pos] if pos is not None else self.source.decode([tid])
            self._text[tid] = t
        return t

    def token(self, pos_out: int, tid: int, how: str, dist: Distribution, p_pick: Optional[float],
              valid: Optional[frozenset], tau: float, after: Optional[DecodeState], alive: bool = True) -> None:
        slot = self.index.position(tid)
        logit = dist.slice_logits[slot] if slot is not None else self.source.logit(tid)

        def ok(t: int) -> Optional[bool]:
            if valid is None:
                return None
            p = self.index.position(t)
            return p is not None and p in valid

        rec = {
            "pos": pos_out, "id": tid, "text": self.text(tid), "how": how,
            "logp": round(logit - dist.lse, 6), "rank": self.source.rank(tid),
            "p_pick": None if p_pick is None else round(p_pick, 6),
            "n_valid": None if valid is None else len(valid),
            "valid_mass": None if valid is None else round(_mass(dist, valid), 6),
            "H": round(dist.entropy, 5), "tau": round(tau, 3),
            "top": [[t, self.text(t), round(math.exp(l - dist.lse), 6), ok(t)] for t, l in dist.top[: self.top]],
        }
        if after is not None:
            rec["line"], rec["akshara"] = after.lines, self.enforcer.akshara(after)
        if not alive:
            rec["in_meter"] = False
        self.records.append(rec)

    def event(self, **kw) -> None:
        self.records.append(kw)


def decode(enforcer: Enforcer, index: TokenIndex, source: LogitsSource, prompt_ids: Sequence[int],
           mode: str, seed: int = 42, cfg: DecodeConfig = DecodeConfig(),
           masks: Optional[MaskCache] = None) -> dict:
    """Generate one poem; returns text, token ids, status, statistics and the trace."""
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}")
    masks = masks or MaskCache(enforcer, index)
    source.start(prompt_ids)
    reseed = getattr(source, "reseed", None)            # the random control draws its logits per seed
    if reseed is not None:
        reseed(seed)
    t0 = time.time()
    if mode == "baseline":
        out = _baseline(enforcer, index, source, seed, cfg, masks)
    else:
        out = _constrained(enforcer, index, source, mode, seed, cfg, masks)
    out.update(mode=mode, seed=seed, seconds=round(time.time() - t0, 3), config=asdict(cfg))
    return out


# ----------------------------------------------------------------------------
# the three strategies
# ----------------------------------------------------------------------------
def token_budget(enf: Enforcer, cfg: DecodeConfig = DecodeConfig()) -> int:
    """The constrained strategies' token budget: ``cfg.max_tokens``, or by default the most tokens
    any poem of the meter can take, so that the budget never decides the outcome. The orthography
    filter bounds an akshara at ``MAX_AKSHARA_CHARS`` characters; with at most one space per
    akshara, a ⏎ per line and at least one character per token, a poem needs at most
    ``(MAX_AKSHARA_CHARS + 1) × aksharas + lines`` tokens. (A factor of 2 — enough on random
    logits — cut off 80 of 1,665 E4B poems, a median 94% of the way through: under the mask the
    model writes one character per token 72% of the time.) The loop's step limit, (backtracks + 2)
    × budget, likewise leaves every backtrack room to finish.

    >>> token_budget(Enforcer("utpalamala"))            # 4 lines of 20 aksharas
    1044
    """
    if cfg.max_tokens:
        return cfg.max_tokens
    return (ortho.MAX_AKSHARA_CHARS + 1) * enf.max_aksharas() + enf.n_lines


def _constrained(enf: Enforcer, index: TokenIndex, source: LogitsSource, mode: str, seed: int,
                 cfg: DecodeConfig, masks: MaskCache) -> dict:
    rng = random.Random(seed)
    tracer = _Tracer(source, index, enf, cfg.trace_top)
    budget = token_budget(enf, cfg)
    state = enf.initial()
    out: list[int] = []
    ckpts: list[tuple[int, DecodeState, float]] = []
    tau_c, backtracks, consecutive, decay_left = cfg.temperature, 0, 0, 0
    stall, progress = 0, (0, 0)
    n_masks, mask_seconds, steps = 0, 0.0, 0
    status = "budget"
    while len(out) < budget and steps < (cfg.max_backtracks + 2) * budget:
        steps += 1
        if enf.poem_complete(state):
            status = "complete"
            break
        forced = enf.must_end_line(state) if cfg.force_nl == "must_end" else enf.line_complete(state)
        if forced:
            dist = source.next()
            nl_id = index.ids[index.newline]
            state = enf.step(state, "\n")
            tracer.token(len(out), nl_id, "forced_nl", dist, 1.0, None, tau_c, state)
            out.append(nl_id)
            source.push(nl_id)
            consecutive = 0
            continue
        if mode != "masking_only" and steps % cfg.checkpoint_every == 0:
            ckpts.append((len(out), state, tau_c))
            del ckpts[:-cfg.checkpoint_cap]
        tm = time.time()
        valid = masks.valid(state)                     # CPU, while the model's forward pass runs (hf.py)
        mask_seconds += time.time() - tm
        n_masks += 1
        dist = source.next()
        vmass = _mass(dist, valid) if valid else 0.0
        reason = None
        if not valid:
            reason = "empty"
        elif mode == "masking_backtrack":
            if len(valid) < cfg.min_valid:
                reason = "few_valid"
            elif vmass < cfg.min_valid_mass:
                reason = "mass_collapse"
            elif stall >= cfg.stall_limit:
                reason = "stall"
        if reason and mode != "masking_only" and ckpts and backtracks < cfg.max_backtracks:
            backtracks += 1
            consecutive += 1
            for _ in range(min(consecutive, len(ckpts)) - 1):
                ckpts.pop()
            keep, state, ck_tau = ckpts.pop()
            del out[keep:]
            source.rollback(keep)
            tau_c = min(ck_tau + cfg.tau_step * consecutive, cfg.tau_max)
            decay_left = cfg.tau_decay
            rng.seed(seed + backtracks * 1337)
            stall, progress = 0, (state.lines, enf.akshara(state))
            tracer.event(how="backtrack", reason=reason, to=keep, tau=round(tau_c, 3), n_valid=len(valid),
                         valid_mass=round(vmass, 6))
            continue
        if not valid:
            status = "dead_end"
            break
        probs = _probs(dist, valid, tau_c)
        if mode == "hybrid":
            acc: dict[int, float] = {}
            alv: dict[int, float] = {}
            for pos, p in sorted(probs.items(), key=lambda kv: -kv[1])[: cfg.k_rerank]:
                if p < 1e-8:
                    break
                if enf.line_complete(enf.step(state, index.texts[pos])):
                    acc[pos] = p
                alv[pos] = p
                if len(acc) >= 3 or (len(alv) >= 10 and not acc):
                    break
            pool, how = (acc, "accept") if acc else (alv, "alive")
            choice, p_pick = draw(pool, rng)
        else:
            choice, p_pick = draw(top_p_filter(probs, cfg.top_p), rng)
            how = "sample"
        tid = index.ids[choice]
        state = enf.step(state, index.texts[choice])
        tracer.token(len(out), tid, how, dist, p_pick, frozenset(valid), tau_c, state)
        out.append(tid)
        source.push(tid)
        consecutive = 0
        if decay_left:
            decay_left -= 1
            if not decay_left:
                tau_c = cfg.temperature
        now = (state.lines, enf.akshara(state))
        stall = 0 if now != progress else stall + 1
        progress = now
    if status == "budget" and enf.poem_complete(state):
        status = "complete"                            # the budget's last token finished the poem
    text = "".join(index.texts[index.position(t)] for t in out)
    return {"status": status, "text": text, "ids": out, "n_tokens": len(out), "n_masks": n_masks,
            "n_backtracks": backtracks, "ms_per_mask": round(1000 * mask_seconds / max(n_masks, 1), 2),
            "mask_cache": {"hits": masks.hits, "misses": masks.misses}, "trace": tracer.records}


# ----------------------------------------------------------------------------
# baseline: the model writes freely, the enforcer watches
# ----------------------------------------------------------------------------
def _baseline(enf: Enforcer, index: TokenIndex, source: LogitsSource, seed: int, cfg: DecodeConfig,
              masks: MaskCache) -> dict:
    rng = random.Random(seed)
    tracer = _Tracer(source, index, enf, cfg.trace_top)
    state: Optional[DecodeState] = enf.initial()
    out: list[int] = []
    text_so_far = ""
    left_meter_at: Optional[int] = None
    status = "budget"
    eos = set(index.eos_ids)
    for _ in range(cfg.baseline_max_tokens or 3 * enf.max_aksharas() + 32):
        valid = None
        if state is not None and cfg.watch_baseline:
            valid = frozenset(masks.valid(state))      # CPU, while the model's forward pass runs (hf.py)
        dist = source.next()
        tid, p_pick = source.sample_full(cfg.temperature, cfg.top_p, rng)
        if tid in eos:
            tracer.token(len(out), tid, "eos", dist, p_pick, valid, cfg.temperature, state, alive=state is not None)
            status = "eos"
            break
        new_text = source.decode(out + [tid])
        piece, text_so_far = new_text[len(text_so_far):], new_text
        if state is not None:
            nxt = enf.step(state, piece)
            if nxt is None:
                left_meter_at = len(out)
            state = nxt
        # record before push: logp and rank must come from the distribution the token was drawn from
        tracer.token(len(out), tid, "sample", dist, p_pick, valid, cfg.temperature, state, alive=state is not None)
        out.append(tid)
        source.push(tid)
    return {"status": status, "text": text_so_far, "ids": out, "n_tokens": len(out),
            "left_meter_at": left_meter_at, "complete_in_meter": state is not None and enf.poem_complete(state),
            "mask_cache": {"hits": masks.hits, "misses": masks.misses}, "trace": tracer.records}

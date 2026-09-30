# -*- coding: utf-8 -*-
"""
Where the next-token distribution comes from.

A source is stateful: it holds the prompt and the tokens generated so far,
and it can roll back (backtracking). Each step it returns a
:class:`Distribution` — logits over the vocabulary slice for the strategies,
plus whole-vocabulary statistics for the traces (log-sum-exp, entropy, top-k),
so the probability a token had under the model is recorded even when the
model wanted a token outside the slice.

:class:`RandomLogits` is the EXP-12 control: standard-normal logits over the
slice, no model. The Hugging Face adapter lives in ``hf.py`` (torch).

Owns: the source protocol and the random control. Must not import torch.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Optional, Protocol, Sequence

from .vocab import TokenIndex


@dataclass
class Distribution:
    slice_logits: list[float]            # raw logits (T = 1) over the TokenIndex order
    lse: float                           # log-sum-exp over the whole vocabulary (T = 1)
    entropy: float                       # entropy of the whole distribution (T = 1), nats
    top: list[tuple[int, float]]         # whole-vocabulary top-k: (token id, logit)

    def logp(self, position: int) -> float:
        """log p(token at a slice position) under the whole distribution."""
        return self.slice_logits[position] - self.lse


class LogitsSource(Protocol):
    def start(self, prompt_ids: Sequence[int]) -> None: ...
    def next(self) -> Distribution: ...
    def logit(self, token_id: int) -> float: ...
    def rank(self, token_id: int) -> int: ...
    def sample_full(self, temperature: float, top_p: float, rng: random.Random) -> tuple[int, float]:
        """A token from the whole vocabulary (τ, top-p) and the probability it was drawn with."""
        ...
    def push(self, token_id: int) -> None: ...
    def rollback(self, n_generated: int) -> None: ...
    def decode(self, ids: Sequence[int]) -> str: ...


def logsumexp(xs: Sequence[float]) -> float:
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs))


def top_p_filter(probs: dict[int, float], top_p: float) -> dict[int, float]:
    """Smallest set of highest-probability keys whose mass reaches ``top_p``, renormalised.

    >>> top_p_filter({1: 0.5, 2: 0.3, 3: 0.2}, 0.7)
    {1: 0.625, 2: 0.37499999999999994}
    """
    keep: dict[int, float] = {}
    acc = 0.0
    for k, p in sorted(probs.items(), key=lambda kv: -kv[1]):
        keep[k] = p
        acc += p
        if acc >= top_p:
            break
    tot = sum(keep.values())
    return {k: p / tot for k, p in keep.items()}


def draw(probs: dict[int, float], rng: random.Random) -> tuple[int, float]:
    """One key drawn in proportion to its (normalised) weight, and that probability."""
    tot = sum(probs.values())
    r = rng.random() * tot
    last = None
    for k, p in probs.items():
        last = k
        r -= p
        if r <= 0:
            return k, p / tot
    return last, probs[last] / tot


class RandomLogits:
    """Standard-normal logits over the slice (the slice is the whole vocabulary here).

    >>> ix = TokenIndex.from_texts([(1, "క"), (2, "\\n")])
    >>> src = RandomLogits(ix, seed=0); src.start([])
    >>> d = src.next(); len(d.slice_logits), round(sum(math.exp(x - d.lse) for x in d.slice_logits), 6)
    (2, 1.0)
    """

    def __init__(self, index: TokenIndex, seed: int = 0, top_k: int = 5):
        self.index = index
        self.seed = seed
        self.top_k = top_k
        self._rng = random.Random(seed)
        self._current: Optional[Distribution] = None
        self.generated: list[int] = []

    def start(self, prompt_ids: Sequence[int]) -> None:
        self._rng = random.Random(self.seed)
        self.generated = []

    def reseed(self, seed: int) -> None:
        """Called by ``decode`` with the run's seed, so each seed gets its own logits."""
        self.seed = seed
        self._rng = random.Random(seed)

    def next(self) -> Distribution:
        z = [self._rng.gauss(0.0, 1.0) for _ in self.index.ids]
        lse = logsumexp(z)
        ent = -sum(math.exp(x - lse) * (x - lse) for x in z)
        top = sorted(((self.index.ids[i], x) for i, x in enumerate(z)), key=lambda t: -t[1])[: self.top_k]
        self._current = Distribution(z, lse, ent, top)
        return self._current

    def logit(self, token_id: int) -> float:
        pos = self.index.position(token_id)
        return self._current.slice_logits[pos] if pos is not None else float("-inf")

    def rank(self, token_id: int) -> int:
        x = self.logit(token_id)
        return 1 + sum(1 for y in self._current.slice_logits if y > x)

    def sample_full(self, temperature: float, top_p: float, rng: random.Random) -> tuple[int, float]:
        z = self._current.slice_logits
        m = max(z)
        probs = {i: math.exp((x - m) / temperature) for i, x in enumerate(z)}
        tot = sum(probs.values())
        pos, p = draw(top_p_filter({i: q / tot for i, q in probs.items()}, top_p), rng)
        return self.index.ids[pos], p

    def push(self, token_id: int) -> None:
        self.generated.append(token_id)

    def rollback(self, n_generated: int) -> None:
        del self.generated[n_generated:]

    def decode(self, ids: Sequence[int]) -> str:
        return "".join(self.index.texts[self.index.position(i)] for i in ids if self.index.position(i) is not None)

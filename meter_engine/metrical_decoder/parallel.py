# -*- coding: utf-8 -*-
"""
Masks computed by worker processes.

A mask steps the enforcer once per token of the vocabulary slice (1,749 for
Gemma-4): pure Python, 50–150 ms with the prāsa / yati registers. In the
model's process that work holds the GIL, and so does the Python side of the
model's forward pass, so a thread cannot overlap them (measured: 218 ms/token
either way). Worker processes each step a strided share of the slice with
their own enforcer and caches; the parent waits for them without the GIL, so
the forward pass started by ``HFCausalLM.push`` runs meanwhile.

The workers are started once (``spawn``: the parent holds a CUDA context, which
must not be forked) and keep one enforcer per configuration, so their caches
stay warm across a run's meters. The masks are exactly those of
:class:`~metrical_decoder.strategies.MaskCache`.

Owns: :func:`mask_pool`, :class:`ParallelMaskCache`. Must not import torch.
"""
from __future__ import annotations

import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from typing import Sequence

from .enforcer import DecodeState, Enforcer
from .strategies import MaskCache
from .vocab import TokenIndex

_TEXTS: tuple[str, ...] = ()
_ENFORCERS: dict[tuple, Enforcer] = {}


def _init(texts: Sequence[str]) -> None:
    global _TEXTS
    _TEXTS = tuple(texts)
    try:                                       # Linux: die with the parent (a SIGTERM'd run leaves no orphans)
        import ctypes
        import signal
        ctypes.CDLL("libc.so.6", use_errno=True).prctl(1, signal.SIGTERM)       # PR_SET_PDEATHSIG
    except (OSError, AttributeError):
        pass


def _share(config: tuple, state: DecodeState, k: int, n: int) -> list[int]:
    """Slice positions k, k+n, k+2n, … that keep ``state`` alive."""
    enf = _ENFORCERS.get(config)
    if enf is None:
        enf = _ENFORCERS[config] = Enforcer(**dict(config))
    step = enf.step
    return [i for i in range(k, len(_TEXTS), n) if step(state, _TEXTS[i]) is not None]


def mask_pool(index: TokenIndex, workers: int) -> ProcessPoolExecutor:
    """Worker processes for :class:`ParallelMaskCache`, one pool for a whole run."""
    return ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn"), initializer=_init,
                               initargs=(tuple(index.texts),))


class ParallelMaskCache(MaskCache):
    """A :class:`MaskCache` whose misses are computed by the ``workers`` processes of ``pool``."""

    def __init__(self, enforcer: Enforcer, index: TokenIndex, pool: ProcessPoolExecutor, workers: int,
                 maxsize: int = 4096):
        super().__init__(enforcer, index, maxsize)
        self.pool = pool
        self.workers = workers
        self._config = tuple(sorted(enforcer.config().items()))

    def _compute(self, state: DecodeState) -> tuple[int, ...]:
        futures = [self.pool.submit(_share, self._config, state, k, self.workers) for k in range(self.workers)]
        return tuple(sorted(i for f in futures for i in f.result()))

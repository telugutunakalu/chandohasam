# -*- coding: utf-8 -*-
"""
metrical_decoder — constrained decoding of Telugu padyams on the metrical DAWG.

IndicNeuroSym's three decoding strategies (masking-only, masking +
backtracking, hybrid mask + accept-state re-ranking) with the metrical DAWG
as the symbolic back end, for every meter of ``meter_rules.yaml``; plus the
unconstrained baseline, a per-token probability trace, and evaluation by the
existing engines. Plan and evidence: ``CONSTRAINED_DECODING_PLAN.md``.

Quick start (random-logit control, no model)::

    from metrical_decoder import Enforcer, TokenIndex, RandomLogits, decode
    ix = TokenIndex.from_texts([(1, "శ్రీ"), (2, " రా"), (3, "మ"), (4, "\\n")])
    r = decode(Enforcer("vidyunmala"), ix, RandomLogits(ix), [], "hybrid", seed=42)

With a model: ``python3 -m metrical_decoder run --model google/gemma-4-E4B-it --out RUN_DIR``.
The core never imports torch; ``metrical_decoder.hf`` does.
"""
from __future__ import annotations

from .enforcer import DecodeState, Enforcer, line_lengths              # noqa: F401
from .evaluate import evaluate, extract_poem                           # noqa: F401
from .incremental import split_word, word_weights                      # noqa: F401
from .orthography import is_well_formed                                # noqa: F401
from .prompts import TOPICS, build_messages, meter_rules               # noqa: F401
from .runner import run_grid, summarize                                # noqa: F401
from .sources import Distribution, RandomLogits                        # noqa: F401
from .strategies import MODES, DecodeConfig, MaskCache, decode         # noqa: F401
from .vocab import TokenIndex                                          # noqa: F401

__version__ = "0.1.0"

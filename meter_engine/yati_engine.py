#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yati_engine.py — compatibility entry point for the :mod:`yati` package.

The engine now lives in ``meter_engine/yati/`` (one module per stage: ruleset,
akshara, readings, pairing, verdict, line, stanza, fixtures, cli).  This file
re-exports the public API so that ``import yati_engine as ye`` keeps working,
and keeps the command line::

    python3 yati_engine.py check క గా
    python3 -m yati check క గా          # the same
"""
from __future__ import annotations

import sys

from yati import *                                   # noqa: F401,F403
from yati import (  # noqa: F401  — names the tests and older callers use
    PROFILE_ORDER, RANK_CONSTITUENT, RANK_DETACH, RANK_HIDDEN, RANK_SANDHI, RANK_UBHAYA, RANK_WRITTEN,
    _cli, _rs, _split_aksharas, _word_context, _words_from_syllables,
)
from yati.constants import DEFAULT_METER_RULES_PATH, DEFAULT_RULES_PATH, HERE, ENGINE_DIR   # noqa: F401
from yati.line import _prasa_yati, _syllable_texts, _weight                                     # noqa: F401
from yati.pairing import _consonant_rule, _vowel_bridge                                         # noqa: F401
from yati.stanza import _meter_flags                                                            # noqa: F401

if __name__ == "__main__":
    sys.exit(_cli())

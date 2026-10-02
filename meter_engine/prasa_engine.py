#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prasa_engine.py — compatibility entry point for the :mod:`prasa` package.

The engine now lives in ``meter_engine/prasa/`` (constants, aksharanusarika_loader,
akshara, ruleset, features, compare, stanza, lookup, cli).  This file re-exports
the public API so that ``import prasa_engine as pe`` keeps working and keeps
the command line::

    python3 prasa_engine.py check "పాదము 1" "పాదము 2" ...
    python3 -m prasa check ...          # the same
"""
from __future__ import annotations

import sys

from prasa import *                                          # noqa: F401,F403
from prasa import main                                       # noqa: F401
from prasa import (AksharaParts, OnsetOutcome, TrailEntry, PairVerdict, compare_onsets, compare_pair,   # noqa: F401
                   druta_sandhi_reading, intrinsic_weight, extract_line, LineFeatures)
from prasa.constants import (ANUSVARA, ARDHABINDU, CONSONANTS, DANTYA_MAP, DEFAULT_METER_RULES_PATH,   # noqa: F401
                             DEFAULT_RULES_PATH, HALANT, HERE, IGNORABLE, INDEPENDENT_VOWELS,
                             KHANDAKHANDA_RULES, LONG_VOWELS, MATRA_TO_VOWEL, NAKAARA_POLLU,
                             NEVER_ACCEPTED, PROJECT_ROOT, VISARGA, ZWSP)
from prasa.aksharanusarika_loader import _extend_aksharanusarika                              # noqa: F401
from prasa.ruleset import _meter_index, _rs                                                   # noqa: F401
from prasa.compare import (_bindu_special, _geminate_like, _khandakhanda_variant, _pair_scope,   # noqa: F401
                           _santa_identification)
from prasa.stanza import _compose_labels, _weight_rule                                        # noqa: F401
from prasa.cli import _print_result                                                           # noqa: F401
from prasa.features import _word_around                                                       # noqa: F401

if __name__ == "__main__":
    sys.exit(main())

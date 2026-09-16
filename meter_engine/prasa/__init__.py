# -*- coding: utf-8 -*-
"""
prasa — Telugu ప్రాస (second-akshara rhyme) engine with a provenance trail.

Data-driven by ``meter_engine/prasa_rules.yaml``; splits pādas into aksharas
with ``meter_engine/aksharanusarika.py``.

    from prasa import evaluate, lookup_pair
    res = evaluate(["పలికెడిది భాగవత మఁట", "పలికించెడివాడు రామభద్రుం డఁట, నేఁ", ...], profile="strict")
    res.matched, res.label_te, res.prasa_consonant, res.violations, res.trail

Modules (read them in this order):

    constants               — paths, Unicode building blocks, profiles
    aksharanusarika_loader  — import the akshara splitter by file path
    akshara                 — sanitize(), parse_akshara(): the anatomy of one akshara
    ruleset                 — Ruleset: the tables of prasa_rules.yaml; the meter index
    features                — extract_line(): everything the rules look at in one pāda
    compare                 — compare_pair(): two pādas, the rules that fired, the trail
    stanza                  — evaluate(): the stanza verdict (PrasaResult)
    lookup                  — lookup_pair(), maitri_matrix(), run_attested_examples()
    cli                     — the command line
"""
from __future__ import annotations

from .constants import PROFILE_ORDER, DANTYA_MAP                                              # noqa: F401
from .aksharanusarika_loader import load_aksharanusarika                                       # noqa: F401
from .akshara import AksharaParts, sanitize, parse_akshara, intrinsic_weight, render_onset     # noqa: F401
from .ruleset import Ruleset, load_ruleset                                                     # noqa: F401
from .features import LineFeatures, extract_line, druta_sandhi_reading                         # noqa: F401
from .compare import TrailEntry, OnsetOutcome, PairVerdict, compare_onsets, compare_pair       # noqa: F401
from .stanza import PrasaResult, evaluate                                                      # noqa: F401
from .lookup import lookup_pair, maitri_matrix, run_attested_examples                          # noqa: F401
from .cli import main                                                                          # noqa: F401

__all__ = [
    "Ruleset", "LineFeatures", "AksharaParts", "TrailEntry", "PairVerdict", "PrasaResult",
    "load_ruleset", "load_aksharanusarika", "sanitize", "parse_akshara", "extract_line",
    "evaluate", "lookup_pair", "maitri_matrix", "run_attested_examples", "render_onset", "PROFILE_ORDER",
]

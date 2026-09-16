# -*- coding: utf-8 -*-
"""
yati — Telugu యతి (yati) engine with a provenance trail.

Given the వళి (first akshara of a pāda) and the akshara at the యతిస్థానము,
the engine says which yati they satisfy, or by which NAMED rule they fail,
under a profile (strict / relaxed / historical).  It is data-driven by
``meter_engine/yati_rules.yaml``, whose rule ids are those of
``yathi_docs/yathi_compact.md``.

Quick start::

    from yati import check, evaluate_line, evaluate_stanza
    r = check("శ్రీ", "చె")            # -> YatiResult
    r.matched, r.rule, r.label_te      # True, 'YATI-VY-12', 'సరసయతి (శ-చ)'
    print(r.explain())

    evaluate_line(syllables, [(1, 10)], profile="relaxed")     # one pāda, its yati groups
    evaluate_stanza(text)                                       # meter + positions from the DAWG

Modules (read them in this order):

    constants  — characters, paths, reading ranks
    ruleset    — Ruleset: the tables of yati_rules.yaml
    akshara    — Akshara features and parse_akshara()
    readings   — Reading candidates of one akshara (సంయుక్త, ఋ, ubhaya, sandhi hypotheses)
    pairing    — pair_rule(): the lookup of two readings; lookup_pair / maitri_matrix
    verdict    — check(): the pair verdict (YatiResult)
    line       — evaluate_line(): a pāda's yati groups, బహుయతి, prāsa-yati fallback
    stanza     — prepare_stanza() / evaluate_stanza(): the whole poem via the DAWG
    fixtures   — run_attested_examples(): the fixtures embedded in the YAML
    cli        — the command line
"""
from __future__ import annotations

from .constants import PROFILE_ORDER, RANK_WRITTEN, RANK_CONSTITUENT, RANK_DETACH, RANK_UBHAYA, RANK_SANDHI, RANK_HIDDEN  # noqa: F401
from .ruleset import Ruleset, load_ruleset, _rs                                          # noqa: F401
from .akshara import Akshara, parse_akshara                                              # noqa: F401
from .readings import Reading, readings_for, _word_context, _split_aksharas              # noqa: F401
from .pairing import Match, pair_rule, lookup_pair, maitri_matrix                        # noqa: F401
from .verdict import YatiResult, check                                                   # noqa: F401
from .line import GroupYati, LineYati, evaluate_line, sandhi_evidence, _words_from_syllables   # noqa: F401
from .stanza import StanzaYati, StanzaPlan, prepare_stanza, plan_from_identification, plan_from_candidate, evaluate_plan, evaluate_stanza   # noqa: F401
from .fixtures import run_attested_examples                                              # noqa: F401
from .cli import main as _cli                                                            # noqa: F401

__all__ = [
    "Ruleset", "Akshara", "Reading", "Match", "YatiResult", "GroupYati", "LineYati", "StanzaYati", "StanzaPlan",
    "load_ruleset", "parse_akshara", "readings_for", "pair_rule", "check", "lookup_pair", "maitri_matrix",
    "sandhi_evidence", "evaluate_line", "prepare_stanza", "plan_from_identification", "plan_from_candidate", "evaluate_plan",
    "evaluate_stanza", "run_attested_examples", "PROFILE_ORDER",
]

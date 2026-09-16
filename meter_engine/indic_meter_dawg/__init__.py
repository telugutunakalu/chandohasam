# -*- coding: utf-8 -*-
"""
indic_meter_dawg — identify the chandassu of a Telugu poem from its
guru/laghu pattern, with a right-linear grammar per meter compiled into a
weighted directed acyclic word graph (DAWG).

Quick start::

    from indic_meter_dawg import identify
    res = identify(["UIIUIUIIIUIIUIIUIUIU"] * 4)
    res.best.meter          # 'utpalamala'
    print(res.explain())

    from indic_meter_dawg import identify_text, scan
    identify_text("శ్రీరాముని దయచేతను\n…").best.meter     # from Telugu text: scansion + identification
    scan("శ్రీరాముని దయచేతను")[0].format()             # aksharas | U/I | vikalpa positions

    from indic_meter_dawg import prosodic_grammar, format_prosodic_grammar, load_catalogue
    print(format_prosodic_grammar(prosodic_grammar(load_catalogue().get("kandamu"))))

Everything is built from ``meter_rules.yaml`` and ``ganas.yaml`` in the
parent folder; no per-meter code exists anywhere in the package.
"""
from __future__ import annotations

__version__ = "0.1.0"

from .symbols import normalize, normalize_lines, matras, NotationError          # noqa: F401
from .ganas import load_registry, Gana, GanaRegistry, GanaError                 # noqa: F401
from .catalogue import load_catalogue, Catalogue, MeterSpec, CatalogueError     # noqa: F401
from .grammar import gana_level_grammar, to_strict, derive, format_grammar      # noqa: F401
from .builder import build_line_dawg, default_dawg, LineDawg                    # noqa: F401
from .walker import walk, viable_prefix, WalkResult                             # noqa: F401
from .parser import segment, Segmentation                                       # noqa: F401
from .identify import identify, identify_text, IdentificationResult, Candidate  # noqa: F401
from .scansion import scan, scan_line, patterns, syllabify, LineScansion, Syllable, ScanPolicy   # noqa: F401
# the function is re-exported as ``prosodic_grammar`` so that ``indic_meter_dawg.prosody`` stays the module
from .prosody import prosodic_grammar, ProsodicGrammar, flatten as flatten_poem     # noqa: F401
from .prosody import prosodic_automaton, accepts_poem, format_prosodic_grammar           # noqa: F401

__all__ = [
    "identify", "identify_text", "IdentificationResult", "Candidate",
    "scan", "scan_line", "patterns", "syllabify", "LineScansion", "Syllable", "ScanPolicy",
    "build_line_dawg", "default_dawg", "LineDawg",
    "walk", "viable_prefix", "WalkResult", "segment", "Segmentation",
    "load_catalogue", "load_registry", "gana_level_grammar", "to_strict", "derive", "format_grammar",
    "prosodic_grammar", "ProsodicGrammar", "flatten_poem", "prosodic_automaton", "accepts_poem", "format_prosodic_grammar",
    "normalize", "normalize_lines", "matras",
    "Catalogue", "MeterSpec", "Gana", "GanaRegistry",
    "NotationError", "GanaError", "CatalogueError",
]

# -*- coding: utf-8 -*-
"""
Loader for ``aksharanusarika`` (the akshara splitter), shipped as ``meter_engine/aksharanusarika.py``
(v0.0.7a, the Python port of the JS version, synced on 2026-09-26 with the aksharanusarika repo:
ఁ attaches to the akshara before it, ZWNJ is stripped, and a dead-consonant cluster such as స్ట్
merges into the akshara before it).

The module is imported by file path and its character tables are EXTENDED (never altered)
so that ౘ/ౙ and ౢ/ౣ form aksharas.
"""
from __future__ import annotations

import importlib.util
import os
import sys
import types
from pathlib import Path
from typing import Optional

from .constants import DANTYA_MAP, HERE, PROJECT_ROOT


_AKSHARANUSARIKA = None


def load_aksharanusarika(path: Optional[str] = None):
    """Import aksharanusarika (a script with a dotted file name) as a module.

    Search order: explicit ``path`` -> ``$AKSHARANUSARIKA_PATH`` ->
    ``meter_engine/aksharanusarika.py`` (the copy shipped with the engine) ->
    ``<project root>/aksharanusarika*.py`` (highest version string first).
    The module's character tables are EXTENDED (never altered) so that the
    dental ౘ/ౙ and the vocalic-ḷ signs ౢ/ౣ form aksharas — see
    ``aksharanusarika_extensions`` in the YAML.
    """
    global _AKSHARANUSARIKA
    if _AKSHARANUSARIKA is not None and path is None:
        return _AKSHARANUSARIKA
    candidates: list[Path] = []
    if path:
        candidates.append(Path(path))
    env = os.environ.get("AKSHARANUSARIKA_PATH")
    if env:
        candidates.append(Path(env))
    candidates.append(HERE / "aksharanusarika.py")
    candidates.extend(sorted(PROJECT_ROOT.glob("aksharanusarika*.py"), key=lambda p: p.name, reverse=True))
    for cand in candidates:
        if not cand.is_file():
            continue
        if "pytz" not in sys.modules:           # older aksharanusarika copies import pytz only for their demo banner
            try:
                import pytz  # noqa: F401
            except ImportError:                 # pragma: no cover
                stub = types.ModuleType("pytz")
                stub.timezone = lambda name: None
                sys.modules["pytz"] = stub
        spec = importlib.util.spec_from_file_location("aksharanusarika", cand)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        _extend_aksharanusarika(module)
        module.__prasa_engine_path__ = str(cand)
        _AKSHARANUSARIKA = module
        return module
    raise ImportError(
        "aksharanusarika not found. Put aksharanusarika_v*.py in the project root, "
        "or set AKSHARANUSARIKA_PATH."
    )


def _extend_aksharanusarika(module) -> None:
    module.telugu_consonants.update(DANTYA_MAP.keys())
    module.dependent_to_independent.update({"ౢ": "ఌ", "ౣ": "ౡ"})
    module.long_vowels.add("ౣ")

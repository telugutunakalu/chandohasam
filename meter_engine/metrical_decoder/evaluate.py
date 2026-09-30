# -*- coding: utf-8 -*-
"""
Verdicts on a generated poem, from the existing engines only.

:func:`extract_poem` takes the poem out of a model's answer (a thought
channel, markdown, numbering and lines without Telugu are dropped); the
constrained modes produce the poem alone, the baseline may not.
:func:`evaluate` then reports

* ``gana_strict`` — the canonical scansion (no pādānta, no vikalpa: the rules
  the enforcer generates under) accepted by the meter's prosodic automaton;
* ``gana`` / ``prasa_*`` / ``yati_*`` — ``chandohasam.analyze`` with the meter
  forced, under ``strict`` + yati sandhi ``off`` and ``relaxed`` + ``hypothesis``;
* simple repetition measures (distinct-akshara ratio, duplicate lines).

The enforcer never judges its own output; this module is the independent
verifier. Owns: :func:`extract_poem`, :func:`evaluate`.
"""
from __future__ import annotations

import re
from typing import Optional

from .incremental import ENGINE_DIR  # noqa: F401  (puts meter_engine on sys.path)
from .prompts import n_lines

from chandohasam import analyze                                      # noqa: E402
from indic_meter_dawg import identify_text, patterns, scan           # noqa: E402
from indic_meter_dawg.prosody import accepts_poem                    # noqa: E402

TELUGU = re.compile(r"[ఀ-౿]")
_THOUGHT = re.compile(r"<\|channel>.*?<channel\|>", re.S)
_MARKUP = re.compile(r"[*#`>_|]")
_NUMBER = re.compile(r"^\s*(?:\d+|[౦-౯]+)\s*[.)]\s*")


def extract_poem(text: str) -> list[str]:
    """The lines of an answer that carry Telugu, without markup or numbering.

    >>> extract_poem("<|channel>thought\\n<channel|>**పద్యము**\\n1. శ్రీరాముని దయచేతను\\nThat is all.")
    ['పద్యము', 'శ్రీరాముని దయచేతను']
    """
    out = []
    for ln in _THOUGHT.sub("", text).splitlines():
        ln = _NUMBER.sub("", _MARKUP.sub("", ln)).strip()
        if TELUGU.search(ln):
            out.append(ln)
    return out


def _windows_ok(meter: str, lines: list[str], n: int) -> bool:
    for i in range(0, max(len(lines) - n + 1, 0)):
        pats = list(patterns(lines[i:i + n]))
        if len(pats) == n and accepts_poem(meter, pats):
            return True
    return False


def evaluate(text: str, meter: str, units: int = 1) -> dict:
    """Metrical verdicts on one generated text."""
    found = extract_poem(text)
    n = n_lines(meter, units)
    lines = found[:n]
    pats = list(patterns(lines)) if lines else []
    rec: dict = {"lines": lines, "n_lines_found": len(found), "patterns": pats,
                 "gana_strict": len(pats) == n and accepts_poem(meter, pats),
                 "gana_any_window": _windows_ok(meter, found, n)}
    rec.update(_repetition(lines))
    if len(lines) < 2:
        rec.update(identified_as=None, gana=False, prasa_strict=False, yati_strict=False,
                   prasa_relaxed=False, yati_relaxed=False, all_strict=False, all_relaxed=False)
        return rec
    res = identify_text(lines)
    strict = analyze(lines, profile="strict", yati_sandhi="off", meter=meter, identification=res)
    relaxed = analyze(lines, profile="relaxed", yati_sandhi="hypothesis", meter=meter, identification=res)
    gana = strict.identified and (strict.meter or "").split("+")[0] == meter
    rec.update(
        identified_as=res.best.meter if res.best else None,
        gana=gana,
        prasa_strict=gana and strict.prasa_matched, yati_strict=gana and strict.yati_matched,
        prasa_relaxed=gana and relaxed.prasa_matched, yati_relaxed=gana and relaxed.yati_matched,
    )
    rec["all_strict"] = rec["gana"] and rec["prasa_strict"] and rec["yati_strict"]
    rec["all_relaxed"] = rec["gana"] and rec["prasa_relaxed"] and rec["yati_relaxed"]
    return rec


def _repetition(lines: list[str]) -> dict:
    aks = [a for ln in scan(lines) for a in ln.aksharas] if lines else []
    return {"aksharas": len(aks),
            "distinct_akshara_ratio": round(len(set(aks)) / len(aks), 4) if aks else None,
            "duplicate_lines": len(lines) - len(set(lines))}

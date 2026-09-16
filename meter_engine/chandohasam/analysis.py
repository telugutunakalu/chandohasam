# -*- coding: utf-8 -*-
"""
End-to-end analysis of a Telugu poem: scansion → metre → gaṇa division →
prāsa → yati.

The three engines are wired here and nowhere else:

1. ``indic_meter_dawg.identify_text`` — guru/laghu scansion and metre
   identification (with the gaṇa segmentation and the yati positions);
2. ``prasa_engine.evaluate`` — the prāsa verdict of the pādas of each unit;
3. ``yati.plan_from_candidate`` / ``yati.evaluate_plan`` — the yati verdict of
   every yati group of every pāda.

The only public function is :func:`analyze`.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional, Sequence

ENGINE_DIR = Path(__file__).resolve().parent.parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

import prasa_engine                                                     # noqa: E402
import yati                                                             # noqa: E402
from indic_meter_dawg import identify_text, load_catalogue             # noqa: E402
from indic_meter_dawg import scansion as sc                             # noqa: E402

from .models import (AksharaCell, GanaCell, LineReport, PadyaAnalysis, PrasaReport, PrasaSeat,   # noqa: E402
                     UnitReport, YatiSeat)

_CATALOGUE = None


def _catalogue():
    global _CATALOGUE
    if _CATALOGUE is None:
        _CATALOGUE = load_catalogue()
    return _CATALOGUE


# -----------------------------------------------------------------------------
# 1. aksharas and gaṇas of one pāda
# -----------------------------------------------------------------------------
def _akshara_cells(syllables: Sequence[sc.Syllable]) -> list[AksharaCell]:
    return [AksharaCell(index=i, text=s.text, weight=s.weight, rules=list(s.rules), vikalpa=s.vikalpa)
            for i, s in enumerate(syllables, 1)]


def _gana_cells(segmentation, cells: list[AksharaCell]) -> list[GanaCell]:
    """Map the DAWG's gaṇa segments (1-based akshara ranges) onto the akshara cells."""
    out = []
    for seg in segmentation.segments:
        members = cells[seg.start - 1: seg.end]
        out.append(GanaCell(index=seg.index, name=seg.gana.name, telugu=seg.gana.telugu,
                            pattern=seg.pattern, aksharas=members))
    return out


def _line_report(line_no: int, syllables: Sequence[sc.Syllable], line_match, text: str) -> LineReport:
    cells = _akshara_cells(syllables)
    seg = line_match.segmentation
    return LineReport(line_no=line_no, text=text, pattern="".join(c.weight for c in cells),
                      aksharas=cells, ganas=_gana_cells(seg, cells), gana_names=list(seg.gana_names),
                      yati=[], padanta_laghu_as_guru=line_match.padanta_applied)


# -----------------------------------------------------------------------------
# 2. yati seats of one unit
# -----------------------------------------------------------------------------
def _yati_seats(plan: yati.StanzaPlan, profile: str, sandhi: str) -> list[list[YatiSeat]]:
    """Evaluate the plan and turn every yati group into a :class:`YatiSeat`."""
    res = yati.evaluate_plan(plan, profile, sandhi=sandhi)
    seats_per_line: list[list[YatiSeat]] = []
    for line_no, (line, syls) in enumerate(zip(res.lines, plan.padas), 1):
        seats = []
        for g in line.groups:
            aksharas = [syls[p - 1].text for p in g.positions if 0 < p <= len(syls)]
            first = g.results[0] if g.results else None
            if g.matched and g.rule == "YATI-PY-01":
                detail = (g.prasa_yati or {}).get("detail", "")
            elif first and first.best:
                b = first.best
                detail = f"{b.reading_a.show()} ↔ {b.reading_b.show()}" + (" via " + ", ".join(b.vidhana) if b.vidhana else "")
            else:
                detail = first.why if first else "; ".join(g.violations)
            seats.append(YatiSeat(line_no=line_no, positions=list(g.positions), aksharas=aksharas, matched=g.matched,
                                  rule=g.rule, label_te=g.label_te, detail=detail,
                                  hypothesis=bool(first and first.best and first.best.hypothesis and g.rule != "YATI-PY-01"),
                                  prasa_yati=g.rule == "YATI-PY-01", min_profile=first.min_profile if first else None,
                                  violations=list(g.violations)))
        seats_per_line.append(seats)
    return seats_per_line


# -----------------------------------------------------------------------------
# 3. prāsa of one unit
# -----------------------------------------------------------------------------
def _prasa_report(padas: list[str], meter: str, profile: str) -> Optional[PrasaReport]:
    """Run the prāsa engine on the pādas of a unit (joined half-lines for సీసము)."""
    spec = _catalogue().get(meter)
    if spec is None:
        return None
    res = prasa_engine.evaluate(padas, profile=profile, meter=meter)
    seats = []
    for ln in res.lines:
        if ln.get("error"):
            continue
        seats.append(PrasaSeat(line_no=ln["index"], purva=ln["purva"], purva_weight=ln["purva_weight_positional"],
                               prasa=ln["prasa"], consonant=prasa_engine.render_onset(ln["onset"]),
                               vowel=ln["vowel"], purnabindu_before=ln["purva_purnabindu"],
                               visarga_before=ln["purva_visarga"], ardhabindu_before=ln["ardhabindu_before"]))
    return PrasaReport(applicable=bool(spec.prasa) and res.applicable, matched=res.matched,
                       consonant=res.prasa_consonant, label_te=res.label_te, label_en=res.label_en,
                       min_profile=res.min_profile, seats=seats,
                       classifications=list(res.classifications), violations=list(res.violations))


# -----------------------------------------------------------------------------
# 4. one metrical unit (the head candidate, or its trailer)
# -----------------------------------------------------------------------------
def _unit_report(cand, scans: list[sc.LineScansion], offset: int, profile: str, yati_sandhi: str) -> UnitReport:
    plan = yati.plan_from_candidate(cand, scans, offset)
    seats = _yati_seats(plan, profile, yati_sandhi)
    halves = plan.halves
    lines: list[LineReport] = []
    padas_text: list[str] = []
    for k, (lm, syls) in enumerate(zip(cand.lines, plan.padas)):
        printed = scans[offset + k * halves: offset + (k + 1) * halves]
        text = " ".join(s.text.strip() for s in printed)
        padas_text.append(text)
        line = _line_report(k + 1, syls, lm, text)
        line.yati = seats[k] if k < len(seats) else []
        lines.append(line)
    return UnitReport(meter=cand.meter, name_te=cand.name_te, family=cand.family, lines=lines,
                      prasa=_prasa_report(padas_text, cand.meter, profile),
                      notes=list(cand.notes) + [n for n in plan.notes if not n.startswith("trailer")],
                      violations=list(cand.violations))


# -----------------------------------------------------------------------------
# 5. the public entry point
# -----------------------------------------------------------------------------
def analyze(text: str | Sequence[str], *, profile: str = "strict", yati_sandhi: str = "hypothesis",
            meter: Optional[str] = None, dawg: Any = None, identification: Any = None) -> PadyaAnalysis:
    """Analyse a poem end to end.

    ``text`` is the poem (one pāda per line, or the printed half-lines of a
    సీసము).  ``profile`` gates both prāsa and yati (strict / relaxed /
    historical); ``yati_sandhi`` is the yati engine's sandhi mode (off /
    hypothesis / acchu).  ``meter`` forces a candidate when the DAWG found
    several.  ``identification`` lets a caller reuse an ``identify_text``
    result (the slow step) across several profiles / sandhi modes.
    """
    if identification is not None:
        res = identification
    else:
        res = identify_text(text, dawg) if dawg is not None else identify_text(text)
    scans = list(res.scansions)
    raw = text if isinstance(text, str) else "\n".join(text)
    cand = None
    if meter:
        cand = next((c for c in res.candidates if c.meter == meter or c.label == meter), None)
    if cand is None:
        cand = res.best
    notes = list(res.notes)
    units: list[UnitReport] = []
    if cand is not None:
        head = _unit_report(cand, scans, 0, profile, yati_sandhi)
        units.append(head)
        if cand.trailer:
            spec = _catalogue().get(cand.meter)
            offset = len(cand.lines) * (spec.halves_per_line if spec else 1)
            units.append(_unit_report(cand.trailer, scans, offset, profile, yati_sandhi))
    return PadyaAnalysis(text=raw, profile=profile, yati_sandhi=yati_sandhi, identified=cand is not None,
                         ambiguous=res.ambiguous, meter=cand.label if cand else None,
                         name_te=(cand.name_te + ("+" + cand.trailer.name_te if cand.trailer else "")) if cand else None,
                         units=units, candidates=[c.label for c in res.candidates], notes=notes,
                         failures=[f.to_dict() for f in res.failures])

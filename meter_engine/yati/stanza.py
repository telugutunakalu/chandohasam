# -*- coding: utf-8 -*-
"""Yati of a whole stanza, with the meter and the yati positions taken from the
metrical DAWG.

:func:`prepare_stanza` runs the (slow) identification once and turns the
result into a :class:`StanzaPlan`; :func:`evaluate_plan` evaluates a plan under
a profile / sandhi mode; :func:`evaluate_stanza` does both.  A plan can also be
built from an identification result you already have
(:func:`plan_from_identification`).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from typing import Any, Optional, Sequence

import yaml

from .constants import DEFAULT_METER_RULES_PATH, ENGINE_DIR
from .ruleset import Ruleset, _rs
from .line import LineYati, evaluate_line


@dataclass
class StanzaYati:
    meter: Optional[str]
    lines: list[LineYati]
    notes: list[str]

    @property
    def matched(self) -> bool:
        return all(l.matched for l in self.lines)

    def to_dict(self) -> dict:
        return {"meter": self.meter, "matched": self.matched, "lines": [l.to_dict() for l in self.lines], "notes": self.notes}

    def explain(self) -> str:
        out = [f"meter: {self.meter}  yati: {'OK' if self.matched else 'FAIL'}"]
        for i, l in enumerate(self.lines, 1):
            for g in l.groups:
                pos = "-".join(str(p) for p in g.positions)
                if g.results:
                    r = g.results[0]
                    s = f"  pāda {i} [{pos}] {r.a.describe()} ↔ {r.b.describe()}: "
                    s += (f"{g.rule} {g.label_te}" if g.matched else f"NO — {r.why}")
                    if g.prasa_yati:
                        s += f"  (prāsa-yati: {g.prasa_yati.get('detail')})"
                else:
                    s = f"  pāda {i} [{pos}]: " + "; ".join(g.violations)
                if g.violations and g.results:
                    s += "  " + "; ".join(g.violations)
                out.append(s)
        out.extend("  note: " + n for n in self.notes)
        return "\n".join(out)


def _meter_flags(meter: str) -> dict:
    try:
        with open(DEFAULT_METER_RULES_PATH, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        for m in data["meters"]:
            if m["name"] == meter:
                st = m.get("structure", {})
                return {"prasa_yati": bool(m.get("prasa_yati")), "halves": int(st.get("halves_per_line", 1)),
                        "yati_ganas": list(st.get("yati_ganas", [])), "system": st.get("system", "")}
    except Exception:  # pragma: no cover
        pass
    return {"prasa_yati": False, "halves": 1, "yati_ganas": [], "system": ""}


@dataclass
class StanzaPlan:
    """Everything evaluate_stanza needs, computed once (the DAWG identification is the slow part)."""
    meter: Optional[str]
    padas: list[list[Any]]                 # syllables per pāda
    groups: list[list[tuple[int, ...]]]    # yati groups per pāda
    prev_dead: list[tuple[str, ...]]
    prev_aras: list[bool]
    prasa_yati: bool
    halves: int
    notes: list[str]
    identified: bool = True


def prepare_stanza(text: str | Sequence[str], meter: Optional[str] = None) -> StanzaPlan:
    """Identify the meter with the metrical DAWG (unless ``meter`` is given) and
    derive the yati groups of every pāda (see :func:`plan_from_identification`)."""
    sys.path.insert(0, str(ENGINE_DIR))
    from indic_meter_dawg import identify_text  # noqa: WPS433 (local import: the DAWG is optional for pair checks)
    return plan_from_identification(identify_text(text), meter)


def plan_from_identification(res: Any, meter: Optional[str] = None) -> StanzaPlan:
    """Turn an ``indic_meter_dawg.IdentificationResult`` into a :class:`StanzaPlan`
    for its best candidate (or for ``meter`` when that meter is among the candidates)."""
    cand = None
    if meter:
        cand = next((c for c in res.candidates if c.meter == meter), None)
    if cand is None:
        cand = res.best
    if cand is None:
        return StanzaPlan(meter, [], [], [], [], False, 1,
                          ["meter not identified; pass yati positions to evaluate_line instead"], False)
    return plan_from_candidate(cand, list(res.scansions))


def plan_from_candidate(cand: Any, scans: Sequence[Any], offset: int = 0) -> StanzaPlan:
    """Build a :class:`StanzaPlan` for one DAWG ``Candidate`` from the line
    scansions (``scans[offset:]`` belong to the candidate).

    Yati groups per pāda come from the candidate's segmentation: సీసము gives
    ``{1, g3}`` and ``{g5, g7}`` (the second half is its own domain); స్రగ్ధర-type
    meters give one group with all coordinates; కందము pādas 1 and 3 give none.
    Pādas printed as two half-lines are joined, keeping their word ids distinct.
    """
    meter = cand.meter
    flags = _meter_flags(meter)
    notes: list[str] = []
    scans = list(scans)[offset:]
    per_pada: list[list[Any]] = []
    # a half-line meter may still be printed one pāda per line (మానిని, లయగ్రాహి): only join when it was split
    halves = 2 if flags["halves"] == 2 and len(scans) >= 2 * len(cand.lines) else 1
    if halves == 2:
        for k in range(len(cand.lines)):
            first = list(scans[2 * k].syllables)
            shift = max((s.word for s in first), default=-1) + 1
            second = [replace(s, word=s.word + shift) for s in scans[2 * k + 1].syllables]   # keep word ids distinct
            per_pada.append(first + second)
        notes.append("pādas printed as half-lines were joined for yati")
    else:
        per_pada = [list(s.syllables) for s in scans[:len(cand.lines)]]
    groups_all: list[list[tuple[int, ...]]] = []
    prev_dead_all: list[tuple[str, ...]] = []
    prev_aras_all: list[bool] = []
    prev_dead: tuple[str, ...] = ()
    prev_aras = False
    for lm, syls in zip(cand.lines, per_pada):
        seg = lm.segmentation
        ys = list(seg.yati_aksharas)
        if flags["halves"] == 2 and len(ys) == 2 and len(seg.segments) >= 5:
            groups = [(1, ys[0]), (seg.segments[4].start, ys[1])]
        elif ys:
            # a fixed vritta's yati points form one బహుయతి group; prāsa-yati meters (లయగ్రాహి) need
            # separate (1, y) pairs because the prāsa-yati fallback compares one pair at a time
            one_group = flags["system"] == "fixed" and not flags["prasa_yati"] and len(ys) > 1
            groups = [tuple([1] + ys)] if one_group else [(1, y) for y in ys]
        else:
            groups = []
        groups_all.append(groups)
        prev_dead_all.append(prev_dead)
        prev_aras_all.append(prev_aras)
        last = syls[-1] if syls else None
        prev_dead = tuple(d for d in (getattr(last, "dead", ()) or ()) if d in ("న", "ల")) if last is not None else ()
        prev_aras = bool(getattr(last, "candrabindu", False)) if last is not None else False
    if cand.trailer:
        notes.append(f"trailer {cand.trailer.meter} not evaluated here; plan it with plan_from_candidate(trailer, scans, offset)")
    return StanzaPlan(meter, per_pada, groups_all, prev_dead_all, prev_aras_all, flags["prasa_yati"], halves, notes)


def evaluate_plan(plan: StanzaPlan, profile: str = "strict", *, sandhi: str = "hypothesis",
                  ruleset: Optional[Ruleset] = None) -> StanzaYati:
    rs = _rs(ruleset)
    lines = [evaluate_line(syls, groups, profile, prev_line_dead=pd, prev_line_ends_arasunna=pa, first_pada=(k == 0),
                           allow_prasa_yati=plan.prasa_yati, sandhi=sandhi, ruleset=rs,
                           seesam_halves=plan.halves == 2 and _meter_flags(plan.meter)["system"] != "fixed")
             for k, (syls, groups, pd, pa) in enumerate(zip(plan.padas, plan.groups, plan.prev_dead, plan.prev_aras))]
    return StanzaYati(plan.meter, lines, list(plan.notes))


def evaluate_stanza(text: str | Sequence[str], meter: Optional[str] = None, profile: str = "strict", *,
                    sandhi: str = "hypothesis", ruleset: Optional[Ruleset] = None) -> StanzaYati:
    """Identify the meter with the metrical DAWG (unless given), take the yati
    positions from its segmentation, and evaluate every pāda's yati groups."""
    return evaluate_plan(prepare_stanza(text, meter), profile, sandhi=sandhi, ruleset=ruleset)

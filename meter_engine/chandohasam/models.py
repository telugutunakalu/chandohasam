# -*- coding: utf-8 -*-
"""
Result objects of the end-to-end analysis.

Everything the tool reports is a plain dataclass, so a result can be turned
into a dictionary / JSON with ``to_dict()`` / ``to_json()`` or printed with
``render()``.  Read the classes top-down: an :class:`AksharaCell` sits in a
:class:`GanaCell`, ganas fill a :class:`LineReport`, lines fill a
:class:`UnitReport` (one metre — a సీసము and its గీతి trailer are two units),
and units fill the :class:`PadyaAnalysis` of the whole poem.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class AksharaCell:
    """One akshara of a pāda with its weight."""
    index: int          # 1-based position in the pāda
    text: str
    weight: str         # 'U' (guru) or 'I' (laghu)
    rules: list[str]    # guru rules that fired ('laghu' when none)
    vikalpa: str = ""   # why the other weight is also admissible ('' when not)


@dataclass
class GanaCell:
    """One gaṇa of the metre's template, with the aksharas that fill it."""
    index: int          # 1-based gaṇa position
    name: str           # e.g. 'bha', 'indra', 'm4'
    telugu: str         # e.g. 'భ', 'ఇం'
    pattern: str        # the U/I pattern actually read, e.g. 'UII'
    aksharas: list[AksharaCell]

    @property
    def text(self) -> str:
        return " ".join(a.text for a in self.aksharas)


@dataclass
class PrasaSeat:
    """The prāsa akshara (second akshara) of one pāda and its context."""
    line_no: int
    purva: str                  # first akshara (ప్రాసపూర్వాక్షరము)
    purva_weight: str           # its weight ('U'/'I') as the prāsa rule counts it
    prasa: str                  # the prāsa akshara as written
    consonant: str              # effective onset used for the comparison ('' for a bare vowel)
    vowel: str
    purnabindu_before: bool = False
    visarga_before: bool = False
    ardhabindu_before: bool = False


@dataclass
class PrasaReport:
    """Prāsa verdict of one metrical unit (all pādas compared pairwise)."""
    applicable: bool            # the metre requires prāsa
    matched: bool
    consonant: Optional[str]    # the prāsa consonant when it is uniform
    label_te: str
    label_en: str
    min_profile: Optional[str]  # least permissive profile under which it matches
    seats: list[PrasaSeat]
    classifications: list[dict]
    violations: list[dict]


@dataclass
class YatiSeat:
    """One yati group of a pāda: the వళి and its coordinate(s)."""
    line_no: int
    positions: list[int]        # 1-based akshara indices, first is the వళి
    aksharas: list[str]         # the aksharas at those positions
    matched: bool
    rule: Optional[str]
    label_te: Optional[str]
    detail: str                 # readings used, or why it failed
    hypothesis: bool = False    # the match rests on a sandhi hypothesis
    prasa_yati: bool = False    # satisfied by the ప్రాసయతి fallback
    min_profile: Optional[str] = None
    violations: list[str] = field(default_factory=list)


@dataclass
class LineReport:
    """One pāda: its aksharas, weights, gaṇa division and yati seats."""
    line_no: int
    text: str
    pattern: str                # U/I string of the whole pāda
    aksharas: list[AksharaCell]
    ganas: list[GanaCell]
    gana_names: list[str]       # Telugu gaṇa letters in order
    yati: list[YatiSeat]
    padanta_laghu_as_guru: bool = False

    @property
    def yati_matched(self) -> bool:
        return all(s.matched for s in self.yati)


@dataclass
class UnitReport:
    """One metre inside the poem (a plain stanza has one unit; సీసము + గీతి has two)."""
    meter: str
    name_te: str
    family: str
    lines: list[LineReport]
    prasa: Optional[PrasaReport]
    notes: list[str]
    violations: list[str]       # stanza rules the DAWG found broken

    @property
    def yati_matched(self) -> bool:
        return all(l.yati_matched for l in self.lines)

    @property
    def prasa_matched(self) -> bool:
        return self.prasa is None or not self.prasa.applicable or self.prasa.matched


@dataclass
class PadyaAnalysis:
    """The whole analysis of one poem."""
    text: str
    profile: str
    yati_sandhi: str
    identified: bool
    ambiguous: bool
    meter: Optional[str]        # catalogue name of the best candidate ('seesamu+tetagiti' for a composite)
    name_te: Optional[str]
    units: list[UnitReport]
    candidates: list[str]       # every candidate label, best first
    notes: list[str]
    failures: list[dict]        # DAWG failure points when nothing matched

    @property
    def yati_matched(self) -> bool:
        return self.identified and all(u.yati_matched for u in self.units)

    @property
    def prasa_matched(self) -> bool:
        return self.identified and all(u.prasa_matched for u in self.units)

    @property
    def matched(self) -> bool:
        """Metre identified, prāsa satisfied where required, every yati satisfied."""
        return self.identified and self.prasa_matched and self.yati_matched

    def to_dict(self) -> dict:
        d = asdict(self)
        d["matched"] = self.matched
        d["yati_matched"] = self.yati_matched
        d["prasa_matched"] = self.prasa_matched
        for u in d["units"]:
            for l in u["lines"]:
                l["yati_matched"] = all(s["matched"] for s in l["yati"])
        return d

    def to_json(self, **kw) -> str:
        kw.setdefault("ensure_ascii", False)
        kw.setdefault("indent", 2)
        return json.dumps(self.to_dict(), **kw)

    def render(self) -> str:
        from .report import render_text
        return render_text(self)

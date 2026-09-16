# -*- coding: utf-8 -*-
"""Pairing two readings: the lookup tables of the yati engine (YATI-EP-04).

* :func:`_consonant_rule` — consonant vs consonant: identity, generated
  vargaja, the conditional ము pairs, the bindu table, the explicit maitri /
  forbidden pairs of ``yati_rules.yaml``;
* :func:`_vowel_bridge` — vowel vs consonant: సరసయతి (అ-య, అ-హ), ఋ-రి, ఌ-లి;
* :func:`pair_rule` — the full decision for one reading pair, including the
  vowel-class check, returning a :class:`Match` (positive or a named failure);
* :func:`lookup_pair` / :func:`maitri_matrix` — table views for the CLI.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .ruleset import Ruleset, _rs
from .readings import Reading


@dataclass
class Match:
    rule: str
    status: str
    label_te: str
    reading_a: Reading
    reading_b: Reading
    vidhana: tuple[str, ...]
    rank: int
    hypothesis: bool
    detail: str
    positive: bool

    def to_dict(self) -> dict:
        return {"rule": self.rule, "status": self.status, "label_te": self.label_te,
                "reading_a": self.reading_a.show(), "reading_b": self.reading_b.show(),
                "vidhana": list(self.vidhana), "rank": self.rank, "hypothesis": self.hypothesis,
                "detail": self.detail, "positive": self.positive}


def _consonant_rule(rs: Ruleset, ra: Reading, rb: Reading) -> tuple[str, str]:
    """-> (rule, detail) for two consonant readings, before the vowel-class check."""
    x, y = ra.consonant, rb.consonant
    if x == y:
        if x in ("ర", "ఱ"):
            return "YATI-SP-07", f"{x}-{y} identity (ఏకతర)"
        return rs.identity_rule, f"{x}-{y} identity"
    # conditional (vowel-class bound) pairs
    ca, cb = rs.vclass(ra.vowel), rs.vclass(rb.vowel)
    for cp in rs.conditional:
        if frozenset(cp["consonants"]) == frozenset((x, y)) and ca == cb == cp["vowel_class"]:
            return cp["rule"], f"{x}-{y} in vowel class {cp['vowel_class']}"
    # bindu tables
    if ra.bindu or rb.bindu:
        for bt in rs.bindu_table:
            for (p, q) in ((ra, rb), (rb, ra)):
                if p.bindu and p.consonant in bt["bindu_side"] and q.consonant in bt["other"]:
                    if bt.get("both") and not q.bindu:
                        continue
                    return bt["rule"], f"ం{p.consonant} with {q.consonant}"
    # vargaja
    vx, vy = rs.varga_of.get(x), rs.varga_of.get(y)
    if vx and vx == vy:
        if x in rs.stops and y in rs.stops:
            return rs.vargaja_rule, f"{x}-{y} same varga ({vx})"
        return rs.stop_nasal_rule, f"{x}-{y}: stop with its class nasal without a preceding ం"
    rule = rs.pairs.get(frozenset((x, y)))
    if rule:
        return rule, f"{x}-{y} table"
    return rs.default_rule, f"{x}-{y}: no maitri"


def _vowel_bridge(rs: Ruleset, hal: Reading, sv: Reading) -> tuple[str, str]:
    c, cv = hal.consonant, rs.vclass(hal.vowel)
    v, vcl = sv.vowel, rs.vclass(sv.vowel)
    for br in rs.vowel_bridges:
        if br["consonant"] != c:
            continue
        if "vowel" in br and br["vowel"] != v:
            continue
        if "vowel_class" in br and br["vowel_class"] != vcl:
            continue
        if "vowel_classes" in br and (cv not in br["vowel_classes"] or cv != vcl):
            continue
        if "consonant_vowel_class" in br and br["consonant_vowel_class"] != cv:
            continue
        rule = br["rule"]
        if rule == "YATI-SV-05" and sv.detached == "bound":
            rule = "YATI-SV-05.2"
        return rule, f"{v} with {c}{hal.vowel} ({br.get('note', '')})".rstrip(" ()")
    if v == "ఋ" and c in ("ర", "ఱ") and cv == "U":
        return "YATI-RJ-10", f"ఋ with {c}{hal.vowel}"
    return "YATI-RJ-03", f"vowel {v} vs consonant {c}{hal.vowel}: a vowel cannot leave its consonant"


def pair_rule(ra: Reading, rb: Reading, ruleset: Optional[Ruleset] = None) -> Match:
    """Look one reading pair up and return a Match (positive or a named failure)."""
    rs = _rs(ruleset)
    via = tuple(dict.fromkeys(ra.via + rb.via))
    hyp = ra.hypothesis or rb.hypothesis
    rank = ra.rank + rb.rank
    ca, cb = rs.vclass(ra.vowel), rs.vclass(rb.vowel)
    if ra.track == "svara" and rb.track == "svara":
        if ca != cb:
            rule, detail = "YATI-RJ-04", f"vowels {ra.vowel}/{rb.vowel} are in classes {ca}/{cb}"
        else:
            det = {ra.detached, rb.detached} - {""}
            key = ra.vowel if ra.vowel in rs.detachable else rb.vowel
            if ra.detached == "bound" and rb.detached == "bound":
                rule = rs.detachable[key]["bound_vs_bound"]
            elif "bound" in det:
                rule = rs.detachable[key]["bare_vs_bound"]
            elif ra.detached == "bare" and rb.detached == "bare":
                rule = rs.detachable[key]["bare_vs_bare"]
            elif "bare" in det:
                rule = rs.detachable[key]["bare_vs_bare"]
            else:
                rule = "YATI-SV-01"
            # a sandhi / ubhaya reading names the vidhāna that produced it (YATI-SV-02, -02.2, -04, -08, UB-*)
            mech = max((r for r in (ra, rb) if r.via and not r.detached), key=lambda r: r.rank, default=None)
            if mech is not None and rule == "YATI-SV-01":
                rule = mech.via[0]
            detail = f"{ra.vowel}-{rb.vowel} (class {ca})"
    elif ra.track == "hal" and rb.track == "hal":
        rule, detail = _consonant_rule(rs, ra, rb)
        if rs.is_positive(rule) and ca != cb:
            detail = f"{detail}; but vowels {ra.vowel}/{rb.vowel} are in classes {ca}/{cb}"
            rule = "YATI-RJ-04"
        if rs.is_positive(rule):
            unit = ra.unit_rule or rb.unit_rule
            if unit:
                rule = unit
    else:
        hal, sv = (ra, rb) if ra.track == "hal" else (rb, ra)
        rule, detail = _vowel_bridge(rs, hal, sv)
        if rs.is_positive(rule) and rule in ("YATI-VY-09", "YATI-VY-10") and sv.via:
            via = tuple(dict.fromkeys(via))
    status = ra.status_override or rb.status_override or rs.status(rule)
    positive = rs.is_positive(rule)
    vid = tuple(v for v in via if v != rule)
    return Match(rule=rule, status=status, label_te=rs.label(rule), reading_a=ra, reading_b=rb,
                 vidhana=vid, rank=rank, hypothesis=hyp, detail=detail, positive=positive)


def lookup_pair(ca: str, cb: str, bindu_a: bool = False, bindu_b: bool = False,
                vowel_class: str = "A", ruleset: Optional[Ruleset] = None) -> dict:
    """The consonant-pair table entry (vowels assumed to be in one class)."""
    rs = _rs(ruleset)
    v = {"A": "అ", "I": "ఇ", "U": "ఉ"}[vowel_class]
    ra = Reading("hal", rs.norm_c(ca), v, bindu=bindu_a)
    rb = Reading("hal", rs.norm_c(cb), v, bindu=bindu_b)
    rule, detail = _consonant_rule(rs, ra, rb)
    status = rs.status(rule)
    return {"a": ca, "b": cb, "bindu_a": bindu_a, "bindu_b": bindu_b, "vowel_class": vowel_class,
            "rule": rule, "status": status, "positive": rs.is_positive(rule),
            "name_en": rs.name(rule, "en"), "name_te": rs.name(rule, "te"), "detail": detail,
            "min_profile": rs.min_profile(status) if rs.is_positive(rule) else None,
            "source": rs.rule(rule).get("src")}


def maitri_matrix(ruleset: Optional[Ruleset] = None, vowel_class: str = "A") -> list[dict]:
    """Every unordered pair of the 35 consonants (630 rows) without bindu."""
    rs = _rs(ruleset)
    out = []
    for i, x in enumerate(rs.consonants):
        for y in rs.consonants[i:]:
            out.append(lookup_pair(x, y, vowel_class=vowel_class, ruleset=rs))
    return out

# -*- coding: utf-8 -*-
"""The pair verdict: does akshara *a* (వళి) pair with akshara *b* (yati akshara)?

:func:`check` parses both sides, expands them into readings, pairs every
reading combination, and returns a :class:`YatiResult` with the best accepted
match, every positive candidate, every named failure, the least permissive
profile that would accept the pair, and a provenance trail.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Iterable, Optional

from .ruleset import Ruleset, _rs
from .akshara import Akshara, parse_akshara
from .readings import readings_for
from .pairing import Match, pair_rule


@dataclass
class YatiResult:
    a: Akshara
    b: Akshara
    profile: str
    matched: bool
    best: Optional[Match]
    candidates: list[Match]          # every positive pairing found, best first
    rejected: list[Match]            # named failures (deduplicated by rule)
    min_profile: Optional[str]
    why: str
    trail: list[dict] = field(default_factory=list)

    @property
    def rule(self) -> Optional[str]:
        return self.best.rule if self.best else None

    @property
    def label_te(self) -> Optional[str]:
        return self.best.label_te if self.best else None

    def to_dict(self) -> dict:
        return {"a": self.a.describe(), "b": self.b.describe(), "profile": self.profile, "matched": self.matched,
                "rule": self.rule, "label_te": self.label_te, "min_profile": self.min_profile, "why": self.why,
                "best": self.best.to_dict() if self.best else None,
                "candidates": [c.to_dict() for c in self.candidates],
                "rejected": [r.to_dict() for r in self.rejected], "trail": self.trail}

    def to_json(self, **kw) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, **kw)

    def explain(self) -> str:
        head = f"{self.a.describe()} ↔ {self.b.describe()} [{self.profile}]: "
        if self.matched and self.best:
            b = self.best
            s = head + f"YES — {b.rule} {b.label_te} ({b.reading_a.show()} ↔ {b.reading_b.show()})"
            if b.vidhana:
                s += " via " + ", ".join(b.vidhana)
            if b.hypothesis:
                s += " [sandhi hypothesis]"
            if b.status not in ("canonical", "canonical_subtype", "mandatory"):
                s += f" [status {b.status}]"
            return s
        s = head + "NO — " + self.why
        if self.min_profile:
            s += f" (would match under profile {self.min_profile})"
        return s


def check(a: Any, b: Any, profile: str = "strict", *, ruleset: Optional[Ruleset] = None,
          sandhi: str = "hypothesis", pre_bindu_a: bool = False, pre_bindu_b: bool = False,
          prev_dead_a: Optional[Iterable[str]] = None, prev_dead_b: Optional[Iterable[str]] = None,
          vowel_a: Iterable[str] | str = (), vowel_b: Iterable[str] | str = (),
          evidence_a: Iterable[tuple] = (), evidence_b: Iterable[tuple] = (),
          word_a: Optional[str] = None, word_b: Optional[str] = None,
          index_a: Optional[int] = None, index_b: Optional[int] = None) -> YatiResult:
    """Do aksharas ``a`` (వళి) and ``b`` (yati akshara) satisfy a yati?

    Steps: parse both sides, expand them into readings, pair every reading
    combination (a sandhi hypothesis may sit on one side only, unless
    ``sandhi="acchu"``), rank the positive candidates and keep the named
    failures.  See the module docstring for the parameters that add context.
    """
    rs = _rs(ruleset)
    if profile not in rs.profiles:
        raise ValueError(f"unknown profile {profile!r}; choose from {rs.profile_order}")
    A = parse_akshara(a, pre_bindu_a, prev_dead_a, rs)
    B = parse_akshara(b, pre_bindu_b, prev_dead_b, rs)
    RA = readings_for(A, rs, sandhi=sandhi, confirmed_vowels=_as_list(vowel_a), evidence_vowels=evidence_a,
                      word=word_a, index=index_a)
    RB = readings_for(B, rs, sandhi=sandhi, confirmed_vowels=_as_list(vowel_b), evidence_vowels=evidence_b,
                      word=word_b, index=index_b)
    trail = [{"rule": "YATI-EP-02", "outcome": "info",
              "detail": f"a={A.describe()} onset={A.onset} vowel={A.vowel}; b={B.describe()} onset={B.onset} vowel={B.vowel}"},
             {"rule": "YATI-EP-03", "outcome": "info",
              "detail": f"readings a: {[r.show() for r in RA]}; b: {[r.show() for r in RB]}"}]
    cands, rejected = _pair_all(RA, RB, rs, sandhi)
    accepted = [m for m in cands if rs.accepted(profile, m.status)]
    best = accepted[0] if accepted else None
    min_profile = _least_permissive_profile(cands, rs)
    why = _explain(best, cands, rejected, min_profile, trail)
    return YatiResult(A, B, profile, best is not None, best, cands, rejected, min_profile, why, trail)


def _as_list(v: Iterable[str] | str) -> list[str]:
    return [v] if isinstance(v, str) else list(v)


def _pair_all(RA: list, RB: list, rs: Ruleset, sandhi: str) -> tuple[list[Match], list[Match]]:
    """Pair every reading of A with every reading of B.

    Returns the positive candidates (best first) and the named failures (one
    per rule, lowest rank first).  Two hypotheses may only be paired in the
    ``acchu`` mode, where the match is relabelled YATI-SV-02.10 (అచ్చు-ఆధారిత):
    otherwise any two same-class aksharas would match.
    """
    cands: list[Match] = []
    rejects: list[Match] = []
    for ra in RA:
        for rb in RB:
            both_hypotheses = ra.hypothesis and rb.hypothesis
            if both_hypotheses and sandhi != "acchu":
                continue
            m = pair_rule(ra, rb, rs)
            if both_hypotheses and m.positive:
                m.rule, m.status, m.label_te = "YATI-SV-02.10", rs.status("YATI-SV-02.10"), rs.label("YATI-SV-02.10")
                m.rank += 2
                m.detail = "vowel classes agree; sandhi assumed on both sides (అచ్చు-ఆధారిత)"
            (cands if m.positive else rejects).append(m)
    cands.sort(key=lambda m: (m.rank, m.hypothesis, m.status != "canonical", m.rule))
    one_per_rule: dict[str, Match] = {}
    for m in sorted(rejects, key=lambda m: m.rank):
        one_per_rule.setdefault(m.rule, m)
    return cands, list(one_per_rule.values())


def _least_permissive_profile(cands: list[Match], rs: Ruleset) -> Optional[str]:
    """The least permissive profile that accepts at least one candidate."""
    best: Optional[str] = None
    for m in cands:
        mp = rs.min_profile(m.status)
        if mp and (best is None or rs.profile_order.index(mp) < rs.profile_order.index(best)):
            best = mp
    return best


def _explain(best: Optional[Match], cands: list[Match], rejected: list[Match], min_profile: Optional[str],
             trail: list[dict]) -> str:
    """Append the decisive trail entry and return the one-line reason for a failure ('' on success)."""
    if best:
        trail.append({"rule": best.rule, "outcome": "pass", "detail": best.detail, "data": best.to_dict()})
        return ""
    if cands:
        why = f"only under profile {min_profile}: {cands[0].rule} {cands[0].label_te} ({cands[0].detail})"
        trail.append({"rule": cands[0].rule, "outcome": "fail", "detail": why})
        return why
    if rejected:
        r0 = rejected[0]
        trail.append({"rule": r0.rule, "outcome": "fail", "detail": r0.detail})
        return f"{r0.rule} {r0.label_te}: {r0.detail}"
    return "no readings"

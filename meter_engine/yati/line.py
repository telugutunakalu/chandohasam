# -*- coding: utf-8 -*-
"""Yati of one pāda: every yati group (వళి + one or more coordinates).

:func:`evaluate_line` takes akshara strings or scansion ``Syllable`` objects
and 1-based yati groups such as ``[(1, 10)]``, ``[(1, 8, 15)]`` or, for
సీసము, ``[(1, g3), (g5, g7)]``.  It supplies the context each pair needs (the
preceding anusvāra / drutam, the previous line's drutam, printed-text sandhi
evidence), enforces బహుయతి నియతి for groups of three or more, and falls back
to ప్రాసయతి where the meter allows it.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any, Iterable, Optional, Sequence

from .constants import ENGINE_DIR, RANK_CONSTITUENT, RANK_DETACH
from .ruleset import Ruleset, _rs
from .akshara import Akshara, parse_akshara, _sanitize
from .verdict import YatiResult, check


@dataclass
class GroupYati:
    positions: tuple[int, ...]           # 1-based akshara indices of the yati group
    results: list[YatiResult]            # one per (vali, coordinate) pair
    matched: bool
    rule: Optional[str]
    label_te: Optional[str]
    violations: list[str]
    prasa_yati: Optional[dict] = None    # filled when the head yati failed and prāsa-yati was tried

    def to_dict(self) -> dict:
        return {"positions": list(self.positions), "matched": self.matched, "rule": self.rule, "label_te": self.label_te,
                "violations": self.violations, "pairs": [r.to_dict() for r in self.results], "prasa_yati": self.prasa_yati}


@dataclass
class LineYati:
    aksharas: list[str]
    groups: list[GroupYati]

    @property
    def matched(self) -> bool:
        return all(g.matched for g in self.groups)

    def to_dict(self) -> dict:
        return {"aksharas": self.aksharas, "matched": self.matched, "groups": [g.to_dict() for g in self.groups]}


def _syllable_texts(syllables: Sequence[Any]) -> list[str]:
    return [s if isinstance(s, str) else (getattr(s, "text", "") or "") for s in syllables]


def _words_from_syllables(syllables: Sequence[Any]) -> tuple[list[Optional[str]], list[Optional[int]]]:
    """Word text and akshara-index-in-word for each syllable (needs Syllable.word)."""
    words: list[Optional[str]] = [None] * len(syllables)
    idxs: list[Optional[int]] = [None] * len(syllables)
    if not syllables or isinstance(syllables[0], str) or not hasattr(syllables[0], "word"):
        return words, idxs
    groups: dict[int, list[int]] = {}
    for i, s in enumerate(syllables):
        groups.setdefault(s.word, []).append(i)
    for w, members in groups.items():
        text = "".join(_sanitize(syllables[i].text) for i in members)
        for k, i in enumerate(members):
            words[i] = text
            idxs[i] = k
    return words, idxs


def _weight(s: Any) -> Optional[str]:
    w = getattr(s, "weight", "") if not isinstance(s, str) else ""
    return w or None


def _prasa_yati(syllables: Sequence[Any], g: tuple[int, ...], rs: Ruleset) -> dict:
    """Prāsa-yati fallback: akshara 2 vs akshara (Y+1); weights of 1 and Y must agree (YATI-PY-03)."""
    p1, y = g[0], g[1]
    if y + 1 > len(syllables) or p1 + 1 > len(syllables):
        return {"matched": False, "rule": "YATI-PY-01", "detail": "no akshara after the yati position"}
    s2, sy1 = parse_akshara(syllables[p1], ruleset=rs), parse_akshara(syllables[y], ruleset=rs)
    w1, wy = _weight(syllables[p1 - 1]), _weight(syllables[y - 1])
    if w1 and wy and w1 != wy:
        return {"matched": False, "rule": "YATI-PY-03", "detail": f"preceding weights differ ({w1} vs {wy})"}
    try:
        if str(ENGINE_DIR) not in sys.path:
            sys.path.insert(0, str(ENGINE_DIR))
        import prasa_engine as pe  # noqa: WPS433 (local import: prāsa is optional for pair checks)
        prs = pe.load_ruleset()
        if s2.onset == sy1.onset:
            sub = "PRASA-SAMA-01"
        elif len(s2.onset) == 1 and len(sy1.onset) == 1:
            sub = prs.lookup_pair_rule(s2.onset[0], sy1.onset[0])
        else:
            sub = "PRASA-VAIRA-GENERIC"
        st = prs.status(sub)
        ok = st not in ("forbidden",)
        return {"matched": ok, "rule": "YATI-PY-01", "prasa_rule": sub, "prasa_status": st,
                "detail": f"{s2.text} ~ {sy1.text} by {sub}" + ("" if ok else " (no prāsa)")}
    except Exception as exc:  # pragma: no cover
        ok = s2.onset == sy1.onset
        return {"matched": ok, "rule": "YATI-PY-01", "prasa_rule": "PRASA-SAMA-01" if ok else None,
                "detail": f"prasa_engine unavailable ({exc}); identity check only"}


def sandhi_evidence(syllables: Sequence[Any], i: int, prev_line_ends_arasunna: bool = False,
                    first_pada: bool = False) -> list[tuple]:
    """Printed-text evidence that akshara ``i`` (1-based) is a sandhi product whose
    vowel is the second word's initial vowel (YATI-SV-02.3):

    * rank 1 — the akshara opens a printed word and the previous word (or the
      previous line) ends in ఁ: editions split ...రుఁ డెవ్వఁడు AFTER the sandhi,
      so the first consonant belongs to the previous word and the vowel is the
      word-initial vowel;
    * rank 2 — the akshara opens a printed word with a lone న / య onset: a
      drutam or యడాగమ glide (వాని నాత్మభవు = వానిన్ + ఆత్మభవు).
    """
    s = syllables[i - 1]
    if isinstance(s, str) or not hasattr(s, "word"):
        return []
    onset = tuple(getattr(s, "onset", ()) or ())
    vowel = getattr(s, "vowel", "") or ""
    if not onset or not vowel:
        return []
    word_initial = i == 1 or getattr(syllables[i - 2], "word", None) != s.word
    out: list[tuple] = []
    if not word_initial:
        # augments inside a word (YATI-DL-10): టుగాగమ (…పు + ట్ + V: గయ్యంపుటాయితము) and
        # నుగాగమ (…ు + న్ + V: విష్ణునాజ్ఞ, కలశంబునందు) — the augment consonant is not the
        # yati consonant; the vowel it carries is the second member's initial vowel.
        prev = syllables[i - 2]
        if len(onset) == 1 and onset[0] in ("ట", "న") and getattr(prev, "vowel", "") == "ఉ" and not getattr(prev, "anusvara", False):
            out.append((vowel, RANK_DETACH, "టుగాగమ" if onset[0] == "ట" else "నుగాగమ"))
        return out
    prev_arasunna = prev_line_ends_arasunna if i == 1 else bool(getattr(syllables[i - 2], "candrabindu", False))
    if prev_arasunna:
        out.append((vowel, RANK_CONSTITUENT, "printed split after ఁ"))
    if onset in (("న",), ("య",)) and not (i == 1 and first_pada):
        out.append((vowel, RANK_DETACH, "word-initial న/య (drutam / యడాగమ)"))
    return out


def evaluate_line(syllables: Sequence[Any], groups: Iterable[Iterable[int]], profile: str = "strict", *,
                  prev_line_dead: Optional[Iterable[str]] = None, prev_line_ends_arasunna: bool = False,
                  first_pada: bool = False, allow_prasa_yati: bool = False, seesam_halves: bool = False,
                  sandhi: str = "hypothesis", ruleset: Optional[Ruleset] = None) -> LineYati:
    """Evaluate every yati group of one pāda.

    ``syllables`` are akshara strings or scansion Syllable objects; ``groups`` are
    1-based index tuples such as ``[(1, 10)]`` (vritta), ``[(1, 8, 15)]``
    (స్రగ్ధర) or ``[(1, 3g), (5g, 7g)]`` (సీసము).  A preceding anusvāra / drutam
    is taken from the previous syllable; ``prev_line_dead`` supplies the drutam
    of the previous line for the వళి (YATI-SY-08); ``first_pada=True`` says
    there is no previous line at all (so a word-initial న/య at the వళి cannot
    be a drutam / glide); ``allow_prasa_yati`` enables the ప్రాసయతి fallback;
    ``seesam_halves`` exempts the line from బహుయతి నియతి.
    """
    rs = _rs(ruleset)
    n = len(syllables)
    context = _LineContext(syllables, tuple(prev_line_dead or ()), prev_line_ends_arasunna, first_pada, rs)
    out: list[GroupYati] = []
    for g in groups:
        g = tuple(int(x) for x in g)
        if len(g) < 2 or any(x < 1 or x > n for x in g):
            out.append(GroupYati(g, [], False, None, None, [f"positions {g} outside the line of {n} aksharas"]))
            continue
        out.append(_evaluate_group(g, context, profile, sandhi, allow_prasa_yati, seesam_halves, rs))
    return LineYati(_syllable_texts(syllables), out)


class _LineContext:
    """What every pair of a pāda needs to know about its neighbours: the word each
    akshara sits in, the preceding anusvāra / drutam, and printed-text sandhi evidence."""

    def __init__(self, syllables: Sequence[Any], prev_line_dead: tuple[str, ...], prev_line_ends_arasunna: bool,
                 first_pada: bool, rs: Ruleset):
        self.syllables = syllables
        self.prev_line_dead = prev_line_dead
        self.prev_arasunna = prev_line_ends_arasunna
        self.first_pada = first_pada
        self.rs = rs
        self.words, self.idxs = _words_from_syllables(syllables)

    def akshara(self, i: int) -> Akshara:
        """The i-th akshara (1-based) with its context flags (YATI-MOD-03, MOD-06)."""
        s = self.syllables[i - 1]
        if i == 1:
            return parse_akshara(s, False, self.prev_line_dead, self.rs)
        prev = self.syllables[i - 2]
        if isinstance(prev, str):
            prev = parse_akshara(prev, ruleset=self.rs)
        pre_bindu = bool(getattr(prev, "anusvara", False))
        prev_dead = tuple(d for d in (getattr(prev, "dead", ()) or ()) if d in ("న", "ల"))
        return parse_akshara(s, pre_bindu, prev_dead, self.rs)

    def evidence(self, i: int) -> list[tuple]:
        return sandhi_evidence(self.syllables, i, self.prev_arasunna, self.first_pada)

    def word(self, i: int) -> tuple[Optional[str], Optional[int]]:
        return self.words[i - 1], self.idxs[i - 1]


def _evaluate_group(g: tuple[int, ...], ctx: _LineContext, profile: str, sandhi: str, allow_prasa_yati: bool,
                    seesam_halves: bool, rs: Ruleset) -> GroupYati:
    """One yati group: the వళి against each coordinate, then బహుయతి నియతి and the prāsa-yati fallback."""
    vali = ctx.akshara(g[0])
    word_a, index_a = ctx.word(g[0])
    results: list[YatiResult] = []
    for y in g[1:]:
        word_b, index_b = ctx.word(y)
        results.append(check(vali, ctx.akshara(y), profile, ruleset=rs, sandhi=sandhi,
                             evidence_a=ctx.evidence(g[0]), evidence_b=ctx.evidence(y),
                             word_a=word_a, index_a=index_a, word_b=word_b, index_b=index_b))
    violations: list[str] = []
    matched = all(r.matched for r in results)
    if matched and len(g) > 2 and len(vali.onset) > 1 and not seesam_halves:
        if not _bahuyati_consistent(vali, results, profile, rs):
            violations.append("YATI-SY-11 బహుయతి నియతిభంగము: different constituents of the వళి used for different caesuras")
            if not rs.accepted(profile, rs.status("YATI-RJ-25")):
                matched = False
    first = results[0] if results else None
    rule = first.rule if first and first.best else None
    label = first.label_te if first and first.best else None
    prasa = None
    if not matched and allow_prasa_yati and len(g) == 2:
        prasa = _prasa_yati(ctx.syllables, g, rs)
        if prasa.get("matched"):
            matched, rule, label = True, "YATI-PY-01", rs.label("YATI-PY-01")
    return GroupYati(g, results, matched, rule, label, violations, prasa)


def _bahuyati_consistent(vali: Akshara, results: list[YatiResult], profile: str, rs: Ruleset) -> bool:
    """బహుయతి నియతి (YATI-SY-11): some ONE constituent of the conjunct వళి must be
    able to serve every caesura (a vowel reading, index None, serves any)."""
    def serves_all(idx: int) -> bool:
        return all(any(c.reading_a.index in (idx, None) and rs.accepted(profile, c.status) for c in r.candidates)
                   for r in results)
    return any(serves_all(i) for i in range(len(vali.onset)))

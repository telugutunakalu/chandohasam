# -*- coding: utf-8 -*-
"""Candidate readings of one akshara (YATI-EP-03).

The written consonant + vowel is only one way to *read* an akshara at a yati
coordinate.  :func:`readings_for` expands it into every reading the treatises
allow — each cluster constituent (సంయుక్త), ఋ / ఌ detachment, whole-cluster
equivalences (జ్ఞ, స్న), ubhaya vowels opened by the word the akshara sits in,
and svara-pradhāna sandhi hypotheses — ranked from the most literal (0) to the
most speculative (5).  :func:`_word_context` holds the lexical heuristics
(ubhaya triggers and blockers) that need the whole word.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from .constants import (ANUSVARA, ARDHABINDU, HALANT, RANK_CONSTITUENT, RANK_DETACH, RANK_SANDHI,
                        RANK_UBHAYA, RANK_WRITTEN, VISARGA)
from .ruleset import Ruleset, _rs
from .akshara import Akshara, _sanitize


@dataclass(frozen=True)
class Reading:
    track: str                      # 'hal' | 'svara'
    consonant: Optional[str]
    vowel: str
    bindu: bool = False             # a preceding anusvāra is available
    via: tuple[str, ...] = ()       # vidhāna / mechanism rule ids that produced this reading
    rank: int = 0
    index: Optional[int] = None     # onset constituent index (for బహుయతి)
    hypothesis: bool = False
    detached: str = ""              # '' | 'bare' | 'bound'  (ఋ/ఌ readings)
    unit_rule: str = ""             # whole-cluster equivalence rule (జ్ఞ, స్న)
    status_override: str = ""
    note: str = ""

    def show(self) -> str:
        core = (self.consonant or "") + self.vowel if self.track == "hal" else self.vowel
        tags = []
        if self.bindu:
            tags.append("ం-")
        if self.detached:
            tags.append("detached")
        if self.hypothesis:
            tags.append("hyp")
        return core + (" [" + ",".join(tags) + "]" if tags else "")


def _word_context(rs: Ruleset, ak: Akshara, word: Optional[str], index: Optional[int]) -> tuple[list[Reading], set[str]]:
    """Readings and blockers that follow from the WORD the akshara sits in.

    Returns ``(readings, blocked)``: ubhaya vowel readings opened by the lexical
    triggers of the ruleset (suffixes such as -ఇంచు / -ఏని, the prādi prefix
    table, the nitya-samāsa lexicon, name suffixes), plus the set of tracks a
    blocker closes (``hal_only`` / ``svara_only``).  Without a word nothing
    is known and both lists are empty.
    """
    if not word:
        return [], set()
    w = _sanitize(word)
    aks = _split_aksharas(w, rs)
    if index is None:
        index = next((i for i, a in enumerate(aks) if a == ak.text), None)
    if index is None or index >= len(aks):
        return [], set()
    after = "".join(aks[index + 1:])                  # the text after the akshara, inside the word
    blocked, readings = _apply_blockers(rs, ak, w, aks, index, after)
    readings += _ubhaya_triggers(rs, ak, w, aks, index, after)
    return readings, blocked


def _apply_blockers(rs: Ruleset, ak: Akshara, w: str, aks: list[str], index: int,
                    after: str) -> tuple[set[str], list[Reading]]:
    """Blockers close a track (YATI-EP-03.1).  Every condition written on a
    blocker entry must hold.  A ``svara_only`` blocker (augments, ద్విరుక్త ట)
    also SUPPLIES the vowel the augment carries, as a real reading."""
    blocked: set[str] = set()
    readings: list[Reading] = []
    for b in rs.blockers:
        conds: list[bool] = []
        if "akshara_vowel" in b:
            conds.append(ak.vowel == b["akshara_vowel"])
        if "after" in b:
            conds.append(after.startswith(b["after"]))
        if "word_endings" in b:
            exact = b.get("exact_word", False)
            conds.append(any((w == e) if exact else w.endswith(e) for e in b["word_endings"]))
            conds.append(index == len(aks) - 1 - b.get("index_from_end", 0))
        if "word_prefixes" in b:
            conds.append(any(w.startswith(p) for p in b["word_prefixes"]))
        if "index" in b:
            conds.append(index == b["index"])
        if not conds or not all(conds):
            continue
        blocked.add(b["kind"])
        blocked.add(b["rule"])
        if b["kind"] == "svara_only" and ak.vowel:
            readings.append(Reading("svara", None, ak.vowel, via=(b["rule"],), rank=RANK_DETACH, note=b.get("note", "")))
    return blocked, readings


def _ubhaya_triggers(rs: Ruleset, ak: Akshara, w: str, aks: list[str], index: int, after: str) -> list[Reading]:
    """Ubhaya vowel readings (rank 3) opened by the lexical triggers of the ruleset."""
    out: list[Reading] = []
    trig = rs.ubhaya

    def add(rule: str, vowel: str, note: str = "", override: str = "") -> None:
        out.append(Reading("svara", None, vowel, via=(rule,), rank=RANK_UBHAYA, note=note, status_override=override))

    # suffix triggers: the akshara itself (వowel / anusvāra / exact text) and what follows it
    for t in trig.get("suffix", []):
        if "akshara" in t and ak.text != t["akshara"]:
            continue
        if "akshara_vowel" in t and ak.vowel != t["akshara_vowel"]:
            continue
        if "akshara_anusvara" in t and bool(ak.anusvara) != bool(t["akshara_anusvara"]):
            continue
        if "after" in t and not after.startswith(t["after"]):
            continue
        if "after" not in t and "akshara" not in t:
            continue
        add(t["rule"], t["vowel"], t.get("note", ""))
    # ordinal -అవ: the akshara before the final వ
    ordn = trig.get("ordinal", {})
    if w in ordn.get("words", []) and index == len(aks) - 2:
        add(ordn["rule"], ordn["vowel"], "ordinal -అవ")
    # prefixes and the nitya-samāsa lexicon: the word starts with the fused form and the akshara is the junction
    for t in trig.get("prefix", []) + trig.get("lexicon", []):
        if w.startswith(t["form"]) and index == t["index"]:
            for v in t["vowels"]:
                add(t["rule"], v, t.get("note", ""), t.get("status_override", ""))
    # రాలు (rugāgama) and the honorific name suffixes
    for t in trig.get("suffix_ubhaya", []):
        if w.endswith(t["ending"]) and index == len(aks) - 1 - t["index_from_end"]:
            for v in t["vowels"]:
                add(t["rule"], v, t.get("note", ""))
    for t in trig.get("name_suffixes", []):
        suf_aks = _split_aksharas(t["suffix"], rs)
        # base + అయ్య -> …మయ్య: the base's last akshara carries the suffix vowel; it sits at len(aks) - len(suf_aks)
        junction = len(aks) - len(suf_aks)
        if junction > 0 and "".join(aks[junction + 1:]) == "".join(suf_aks[1:]) and index == junction:
            add("YATI-UB-17", t["vowel"], "నామాఖండ")
    return out


def _split_aksharas(word: str, rs: Ruleset) -> list[str]:
    """Light akshara splitter for word context (no weight logic)."""
    cons = set(rs.consonants) | set(rs.dantya)
    out: list[str] = []
    i, n = 0, len(word)
    while i < n:
        ch = word[i]
        if ch in cons:
            j = i + 1
            while j + 1 < n and word[j] == HALANT and word[j + 1] in cons:
                j += 2
            if j < n and word[j] in rs.matras:
                j += 1
            while j < n and word[j] in (ANUSVARA, VISARGA, ARDHABINDU):
                j += 1
            if j + 1 < n and word[j] in cons and word[j + 1] == HALANT and (j + 2 >= n or word[j + 2] not in cons):
                j += 2
            out.append(word[i:j]); i = j
        elif ch in rs.vowel_class:
            j = i + 1
            while j < n and word[j] in (ANUSVARA, VISARGA, ARDHABINDU):
                j += 1
            out.append(word[i:j]); i = j
        else:
            i += 1
    return out


def readings_for(ak: Akshara, ruleset: Optional[Ruleset] = None, *, sandhi: str = "hypothesis",
                 confirmed_vowels: Iterable[str] = (), evidence_vowels: Iterable[tuple] = (),
                 word: Optional[str] = None, index: Optional[int] = None) -> list[Reading]:
    """Expand one coordinate into ranked candidate readings (YATI-EP-03).

    ``sandhi`` is ``off`` / ``hypothesis`` / ``acchu`` (see the YAML);
    ``confirmed_vowels`` are underlying vowels the caller has established
    (rank 1); ``evidence_vowels`` are ``(vowel, rank, note)`` triples derived
    from the printed text (a word-initial akshara after a word ending in ఁ, a
    word-initial న/య, an augment): they are NOT hypotheses and may pair with a
    hypothesis on the other side.  ``word`` / ``index`` enable the lexical
    ubhaya triggers and blockers.
    """
    rs = _rs(ruleset)
    if not ak.vowel:
        return []
    out = _written_readings(ak, rs)
    out += _detachment_and_cluster_readings(ak, rs)
    word_readings, blocked = _word_context(rs, ak, word, index)
    out += word_readings
    out += _caller_vowel_readings(ak, confirmed_vowels, evidence_vowels)
    if sandhi in ("hypothesis", "acchu"):
        out += _sandhi_hypotheses(ak, rs)
    if "hal_only" in blocked:
        out = [r for r in out if r.track == "hal" or r.detached]
    if "svara_only" in blocked:
        out = [r for r in out if r.track == "svara"]
    return _dedupe(out)


def _written_readings(ak: Akshara, rs: Ruleset) -> list[Reading]:
    """Rank 0/1: the bare vowel, or every consonant of the onset with the akshara's vowel
    (the akshara's own first consonant is rank 0, other constituents and a fused
    predecessor rank 1 — సంయుక్త యతి, YATI-SY-01/03/05/08/09)."""
    out: list[Reading] = []
    V = ak.vowel
    if ak.bare_vowel:
        out.append(Reading("svara", None, V, rank=RANK_WRITTEN, detached="bare" if V in rs.detachable else ""))
    npre = len(ak.pre_dead)
    for i, c in enumerate(ak.onset):
        via: list[str] = []
        if i < npre:                                       # fused from the previous drutam / pollu
            via.append("YATI-SY-08" if c == "న" else "YATI-SY-09" if c == "ల" else "YATI-SY-01")
        elif len(ak.own_onset) > 1:                        # a genuine cluster
            via.append("YATI-SY-01")
            if ak.own_onset == ("క", "ష"):
                via.append("YATI-SY-05")
            if len(set(ak.own_onset)) == 1:
                via.append("YATI-SY-03")
        rank = RANK_WRITTEN if i == npre else RANK_CONSTITUENT
        out.append(Reading("hal", c, V, bindu=ak.pre_bindu, via=tuple(via), rank=rank, index=i))
    return out


def _detachment_and_cluster_readings(ak: Akshara, rs: Ruleset) -> list[Reading]:
    """Rank 2: ఋ / ఌ detached from the host consonant (YATI-SV-05.4) and the
    whole-cluster equivalences జ్ఞ -> న/ణ/క… and స్నా -> త (cluster_unit_table)."""
    out: list[Reading] = []
    V = ak.vowel
    if V in rs.detachable and ak.onset:
        out.append(Reading("svara", None, V, rank=RANK_DETACH, via=("YATI-SV-05.4",), detached="bound"))
    for cu in rs.cluster_units:
        if tuple(cu["cluster"]) == ak.own_onset and (not cu.get("vowel") or cu["vowel"] == V):
            for c in cu["as"]:
                out.append(Reading("hal", c, V, bindu=ak.pre_bindu, via=(cu["rule"],), rank=RANK_DETACH,
                                   index=len(ak.pre_dead), unit_rule=cu["rule"], note=cu.get("note", "")))
    return out


def _caller_vowel_readings(ak: Akshara, confirmed: Iterable[str], evidence: Iterable[tuple]) -> list[Reading]:
    """Vowels the caller established (rank 1) or found evidence for in the printed text."""
    out = [Reading("svara", None, v, rank=RANK_CONSTITUENT, via=("YATI-SV-02",), note="confirmed split") for v in confirmed]
    for v, rank, note in evidence:
        via = "YATI-SV-02.2" if ak.own_onset in (("న",), ("య",)) else "YATI-SV-02"
        out.append(Reading("svara", None, v, rank=int(rank), via=(via,), note=note))
    return out


def _sandhi_hypotheses(ak: Akshara, rs: Ruleset) -> list[Reading]:
    """Rank 4/5: the vowels the written vowel could hide under a sandhi (sandhi_readings
    table), plus the drutam+V / యడాగమ+V reading of a lone న / య (YATI-SV-02.2)."""
    if ak.bare_vowel or not ak.own_onset:
        return []
    out = [Reading("svara", None, v, rank=rank, via=(rule,), hypothesis=True)
           for v, rule, rank in rs.sandhi_readings.get(ak.vowel, [])]
    if ak.own_onset in (("న",), ("య",)):
        out.append(Reading("svara", None, ak.vowel, rank=RANK_SANDHI, via=("YATI-SV-02.2",), hypothesis=True,
                           note="ద్రుతము+V" if ak.own_onset == ("న",) else "యడాగమ+V"))
    return out


def _dedupe(readings: list[Reading]) -> list[Reading]:
    """Keep the lowest-ranked copy of each distinct reading; sort by rank, consonants first."""
    best: dict[tuple, Reading] = {}
    for r in readings:
        key = (r.track, r.consonant, r.vowel, r.bindu, r.detached, r.unit_rule, r.index if r.track == "hal" else None, r.via)
        if key not in best or r.rank < best[key].rank:
            best[key] = r
    return sorted(best.values(), key=lambda r: (r.rank, r.track != "hal", r.index or 0))

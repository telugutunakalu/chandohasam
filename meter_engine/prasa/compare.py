# -*- coding: utf-8 -*-
"""
Pairwise comparison of two pādas: onsets (``compare_onsets``) and the full pair verdict
(``compare_pair``) with the rules that fired and the trail entries.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .constants import DANTYA_MAP, LONG_VOWELS, NEVER_ACCEPTED
from .akshara import render_onset
from .ruleset import Ruleset
from .features import LineFeatures


@dataclass
class TrailEntry:
    rule: str
    status: str          # pass | fail | info | note | na
    scope: str           # line:N | pair:N-M | stanza
    detail: str
    data: dict = field(default_factory=dict)


@dataclass
class OnsetOutcome:
    kind: str                       # identity | maitri | structural | fail
    rules_used: list[str]
    classifications: list[str]
    fail_rule: Optional[str]
    detail: str
    trail: list[TrailEntry]


def _pair_scope(a: LineFeatures, b: LineFeatures) -> str:
    return f"pair:{a.index}-{b.index}"


def _geminate_like(onset: list[str], rs: Ruleset) -> bool:
    """A doubled consonant, or a two-consonant cluster whose members are maitri-related
    (ళ్ల counts as a geminate under ల-ళ abhēda; the element-wise step then prices the relaxation)."""
    if len(onset) != 2:
        return False
    if onset[0] == onset[1]:
        return True
    return rs.status(rs.lookup_pair_rule(onset[0], onset[1])) not in NEVER_ACCEPTED


def _santa_identification(oa: list[str], ob: list[str]) -> Optional[str]:
    """PRASA-DEFECT-SANTA is identification-only: shared first or last consonant
    between two DIFFERENT onsets where at least one is a cluster."""
    if oa == ob or (len(oa) < 2 and len(ob) < 2):
        return None
    if oa and ob and (oa[0] == ob[0] or oa[-1] == ob[-1]):
        shared = "first" if oa[0] == ob[0] else "last"
        return (f"the two onsets {render_onset(oa)} / {render_onset(ob)} share only their {shared} "
                f"consonant — the pattern the treatises call శాంతప్రాస (PRASA-DEFECT-SANTA), "
                f"an asamaprāsa that no profile accepts")
    return None


def compare_onsets(a: LineFeatures, b: LineFeatures, rs: Ruleset) -> OnsetOutcome:
    """Compare the effective prāsa onsets of two lines (rules PRASA-SAMA-01,
    PRASA-SAMYUKTA-*, the structural relaxations and the maitri table)."""
    scope = _pair_scope(a, b)
    oa, ob = a.onset, b.onset
    ta, tb = render_onset(oa) or a.vowel, render_onset(ob) or b.vowel
    trail: list[TrailEntry] = []

    def fail(rule: str, detail: str, extra: Optional[dict] = None) -> OnsetOutcome:
        data = {"onset_a": oa, "onset_b": ob}
        if extra:
            data.update(extra)
        trail.append(TrailEntry(rule, "fail", scope, detail, data))
        note = _santa_identification(oa, ob)
        if note:
            trail.append(TrailEntry("PRASA-DEFECT-SANTA", "note", scope, note))
        for x, y in ((a, b), (b, a)):
            if ((x.ardhabindu_before or x.purva_purnabindu) and len(x.onset) == 1 and x.onset[0] in rs.sarala
                    and len(y.onset) == 1 and rs.druta_sandhi_map.get(y.onset[0]) == x.onset[0]):
                sign = "ఁ" if x.ardhabindu_before else "ం"
                trail.append(TrailEntry("PRASA-SAMA-12", "note", scope,
                                        f"line {x.index} {x.onset[0]} after {sign} is probably the సరళాదేశ of "
                                        f"{y.onset[0]} (line {y.index}) produced by sandhi; the treatise judges the written "
                                        f"post-sandhi consonant, so {x.onset[0]} and {y.onset[0]} still differ"))
        return OnsetOutcome("fail", [], [], rule, detail, trail)

    def structural(rule: str, detail: str, extra: Optional[dict] = None) -> OnsetOutcome:
        data = {"onset_a": oa, "onset_b": ob, "status": rs.status(rule)}
        if extra:
            data.update(extra)
        trail.append(TrailEntry(rule, "pass", scope, detail, data))
        return OnsetOutcome("structural", [rule], [rule], None, detail, trail)

    # --- bare vowels in the prāsa slot ---------------------------------------
    if a.bare_vowel or b.bare_vowel:
        for x, y in ((a, b), (b, a)):
            if x.bare_vowel and x.vowel in ("ఋ", "ౠ") and y.onset == ["ర"]:
                return structural("PRASA-MAITRI-RU-RA",
                                  f"line {x.index} has the vocalic vowel {x.vowel} in the prāsa slot and line "
                                  f"{y.index} has ర: ఋ-ప్రాస (vowel ఋ rhymes with రేఫ)")
        if a.bare_vowel and b.bare_vowel:
            return fail("PRASA-SAMA-01", f"both prāsa aksharas are bare vowels ({a.prasa} / {b.prasa}); "
                                         f"there is no consonant to rhyme")
        x, y = (a, b) if a.bare_vowel else (b, a)
        return fail("PRASA-SAMA-01", f"line {x.index} has a bare vowel {x.prasa} in the prāsa slot but line "
                                     f"{y.index} has the consonant {y.onset_text}; only ఋ may stand for a consonant (ర)")

    # --- 1. krārakommu vs vaṭruvasuḍi: forbidden even though it sounds alike --
    for x, y in ((a, b), (b, a)):
        if (len(x.onset) == 2 and x.onset[1] == "ర" and x.vowel in ("ఉ", "ఊ")
                and len(y.onset) == 1 and y.vowel in ("ఋ", "ౠ") and y.onset[0] == x.onset[0]):
            return fail("PRASA-REPHAYUTA-KRARAKOMMU",
                        f"line {x.index} {x.prasa} is a krārakommu ({x.onset[0]}+ర+{x.vowel}) and line {y.index} "
                        f"{y.prasa} is the same consonant with vaṭruvasuḍi ({y.vowel}); they may not rhyme")

    # --- 2. identity (samaprāsa) ----------------------------------------------
    if oa == ob:
        return _identity_outcome(a, b, scope, trail)

    # --- 3. hal-saṁyuta ఋ: Cృ ~ C్ర (but not C్రు, handled in step 1) --------
    for x, y in ((a, b), (b, a)):
        if (len(x.onset) == 1 and x.vowel in ("ఋ", "ౠ") and len(y.onset) == 2
                and y.onset[1] == "ర" and y.onset[0] == x.onset[0]):
            return structural("PRASA-MAITRI-RU-HALSAMYUTA",
                              f"line {x.index} {x.prasa} ({x.onset[0]}+{x.vowel}) rhymes with line {y.index} "
                              f"{y.prasa} ({render_onset(y.onset)}+{y.vowel}): hal-saṁyuta ఋ-ప్రాస")

    # --- 4. vikalpa: [class-nasal, N] ~ [class-voiced-stop, N] -----------------
    if (len(oa) == 2 and len(ob) == 2 and oa[1] == ob[1] and oa[1] in rs.nasals
            and frozenset((oa[0], ob[0])) in rs.vikalpa_pairs):
        return structural("PRASA-MAITRI-VIKALPA",
                          f"{ta} (line {a.index}) and {tb} (line {b.index}) are the two sandhi doublets of a "
                          f"stop + nasal (class nasal vs class voiced stop); requires the sandhi to be between "
                          f"independent words — verify manually",
                          {"requires_manual_verification": True})

    # --- 5. same length: element-wise maitri --------------------------------
    if len(oa) == len(ob):
        return _elementwise_outcome(a, b, rs, scope, trail, fail)

    # --- 6. different length: saṁyuktāsaṁyukta (deprecated) -------------------
    for x, y in ((a, b), (b, a)):
        if (len(x.onset) == 1 and len(y.onset) == 2 and y.onset[0] == x.onset[0]
                and y.onset[1] in ("ర", "ల")):
            tri = x.onset[0] == "త" and y.vowel == "ఇ"
            detail = (f"simple {x.onset_text} (line {x.index}) vs conjunct {y.onset_text} (line {y.index}): "
                      f"సంయుక్తాసంయుక్త ప్రాస, a deprecated relaxation")
            if tri:
                detail += " — this is the numeral prefix త్రి, the only form Ananta admitted (త్రిప్రాసము)"
            return structural("PRASA-MAITRI-SAMYUKTASAMYUKTA", detail, {"triprasa": tri})

    # --- 7. adhika: one onset is a proper prefix of the other -------------------
    if oa[:len(ob)] == ob or ob[:len(oa)] == oa:
        long_, short_ = (a, b) if len(oa) > len(ob) else (b, a)
        return fail("PRASA-DEFECT-ADHIKA",
                    f"line {long_.index} carries the extra consonant(s) "
                    f"{render_onset(long_.onset[len(short_.onset):])} in its cluster {long_.onset_text} that line "
                    f"{short_.index} ({short_.onset_text}) lacks — అధికప్రాసము, an asamaprāsa")

    # --- 8. conjunct vs simple / mismatched clusters ----------------------------
    if min(len(oa), len(ob)) == 1:
        c, s = (a, b) if len(oa) > 1 else (b, a)
        detail = (f"line {c.index} has the conjunct {c.onset_text} but line {s.index} has the simple "
                  f"consonant {s.onset_text}; a conjunct prāsa must be a conjunct in every line")
        if c.fused_from_purva:
            detail += (f" (the cluster arose by saṁśleṣa of the dead consonant "
                       f"{render_onset(c.fused_from_purva)} from the pre-prāsa akshara {c.purva!r}, PRASA-POS-06; "
                       f"it may not be split off to claim a simple {s.onset_text} rhyme)")
        return fail("PRASA-SAMYUKTA-01", detail)
    return fail("PRASA-SAMYUKTA-02",
                f"clusters {ta} (line {a.index}) and {tb} (line {b.index}) differ in their constituent "
                f"consonants / order")


def _identity_outcome(a: LineFeatures, b: LineFeatures, scope: str, trail: list[TrailEntry]) -> OnsetOutcome:
    """Step 2 of compare_onsets: identical onsets (samaprāsa), naming the conjunct sub-types."""
    oa = a.onset
    classes = ["PRASA-SAMA-01"]
    detail = f"identical onset {render_onset(oa) or a.vowel} in lines {a.index} and {b.index}"
    if len(oa) >= 2:
        classes += ["PRASA-SAMYUKTA-01", "PRASA-SAMYUKTA-02"]
        if len(oa) == 2 and oa[0] == oa[1]:
            classes.append("PRASA-SAMYUKTA-03")
        if len(oa) >= 3:
            classes.append("PRASA-SAMYUKTA-04")
        if a.purva_purnabindu and b.purva_purnabindu:
            classes.append("PRASA-SAMYUKTA-06")
        fused = set(a.fused_from_purva) | set(b.fused_from_purva)
        if "న" in fused:
            classes.append("PRASA-SAMYUKTA-07")
        if "ల" in fused:
            classes.append("PRASA-SAMYUKTA-08")
        detail += f" (conjunct of {len(oa)} consonants, same order)"
    trail.append(TrailEntry("PRASA-SAMA-01", "pass", scope, detail, {"onset": oa}))
    return OnsetOutcome("identity", ["PRASA-SAMA-01"], classes, None, detail, trail)


def _elementwise_outcome(a: LineFeatures, b: LineFeatures, rs: Ruleset, scope: str, trail: list[TrailEntry],
                         fail) -> OnsetOutcome:
    """Step 5 of compare_onsets: onsets of equal length compared consonant by consonant
    through the maitri table (geminate must face geminate; a forbidden pair fails)."""
    oa, ob = a.onset, b.onset
    ta, tb = render_onset(oa) or a.vowel, render_onset(ob) or b.vowel
    gem_a, gem_b = _geminate_like(oa, rs), _geminate_like(ob, rs)
    if gem_a != gem_b:
        g, s_ = (a, b) if gem_a else (b, a)
        return fail("PRASA-SAMYUKTA-03",
                    f"line {g.index} has the geminate {render_onset(g.onset)} but line {s_.index} has the "
                    f"non-geminate cluster {render_onset(s_.onset)}")
    rules: list[str] = []
    positions: list[dict] = []
    failed: list[dict] = []
    for k, (x, y) in enumerate(zip(oa, ob)):
        if x == y:
            positions.append({"position": k + 1, "a": x, "b": y, "rule": "PRASA-SAMA-01"})
            continue
        rule = rs.lookup_pair_rule(x, y)
        entry = {"position": k + 1, "a": x, "b": y, "rule": rule, "status": rs.status(rule)}
        positions.append(entry)
        if rs.status(rule) in NEVER_ACCEPTED:
            failed.append(entry)
        else:
            rules.append(rule)
    if failed:
        f0 = failed[0]
        if sorted(oa) == sorted(ob):
            return fail("PRASA-SAMYUKTA-02",
                        f"{ta} (line {a.index}) and {tb} (line {b.index}) contain the same consonants in a "
                        f"different order (kramamu); the cluster order must be identical", {"positions": positions})
        return fail(f0["rule"], f"{ta} (line {a.index}) vs {tb} (line {b.index}): {f0['a']} and {f0['b']} have no "
                                f"prāsamaitri — {rs.name(f0['rule'])}", {"positions": positions})
    detail = (f"{ta} (line {a.index}) ~ {tb} (line {b.index}) by prāsamaitri: "
              + "; ".join(f"{p['a']}~{p['b']} via {p['rule']} [{p['status']}]" for p in positions if p["rule"] != "PRASA-SAMA-01"))
    for r in rs.sort_rules(rules):
        trail.append(TrailEntry(r, "pass", scope, detail, {"positions": positions, "status": rs.status(r)}))
    classes = rs.sort_rules(rules)
    if len(oa) >= 2:
        classes = classes + ["PRASA-SAMYUKTA-01"] + (["PRASA-SAMYUKTA-03"] if gem_a else [])
    return OnsetOutcome("maitri", rs.sort_rules(rules), classes, None, detail, trail)


@dataclass
class PairVerdict:
    lines: tuple[int, int]
    reading: str
    rules_used: list[str]
    statuses_used: list[str]
    hard_failures: list[dict]
    min_profile: Optional[str]
    classifications: list[str]
    trail: list[TrailEntry]

    @property
    def matched_ever(self) -> bool:
        return self.min_profile is not None


def _bindu_special(a: LineFeatures, b: LineFeatures, rs: Ruleset) -> Optional[dict]:
    """Pairs that are DEFINED by a pūrṇabindu asymmetry: PRASA-MAITRI-ANUNASIKA
    (న్న ~ ంన, మ్మ ~ ంమ), PRASA-MAITRI-MBA-MMA (ంబ ~ మ్మ) — both deprecated — and
    PRASA-MAITRI-BINDU-SAMSLESHA (ంద ~ న్ద, ంగ ~ న్క: the two spellings of a drutam
    before a stop) — an accepted relaxation."""
    for x, y in ((a, b), (b, a)):
        if x.purva_purnabindu and not y.purva_purnabindu:
            if len(x.onset) == 1 and x.onset[0] in ("న", "మ") and y.onset == [x.onset[0]] * 2:
                return {"rule": "PRASA-MAITRI-ANUNASIKA",
                        "detail": (f"line {y.index} geminate {y.onset_text} rhymes with line {x.index} "
                                   f"ం+{x.onset_text} (anunāsika prāsa — deprecated doublet spelling)")}
            if x.onset == ["బ"] and y.onset == ["మ", "మ"]:
                return {"rule": "PRASA-MAITRI-MBA-MMA",
                        "detail": (f"line {x.index} ంబ rhymes with line {y.index} మ్మ "
                                   f"(-ంబు/-మ్ము inflection doublets — deprecated)")}
            if (len(x.onset) == 1 and len(y.onset) == 2 and y.onset[0] == "న"
                    and (y.onset[1] == x.onset[0] or rs.druta_sandhi_map.get(y.onset[1]) == x.onset[0])):
                how = ("the same stop" if y.onset[1] == x.onset[0]
                       else f"the drutam-softened stop ({y.onset[1]} -> {x.onset[0]})")
                return {"rule": "PRASA-MAITRI-BINDU-SAMSLESHA",
                        "detail": (f"line {x.index} ం+{x.onset_text} and line {y.index} {y.onset_text} are the bindu "
                                   f"and the saṁśleṣa spellings of one nasal + {how}; accepted as a relaxation "
                                   f"(the treatise itself only says the drutam takes one of the two shapes)")}
    return None


def _khandakhanda_variant(line: LineFeatures, rs: Ruleset) -> tuple[str, str]:
    cons = line.onset[0] if line.onset else ""
    purva_vowel = line.purva_parts.get("vowel", "")
    within_ananta = cons in rs.khanda_ananta
    within_appakavi = cons in rs.parusha and purva_vowel in LONG_VOWELS
    if within_ananta:
        why = f"consonant {cons} is one of Ananta's ప/ట"
        if within_appakavi:
            why += " and also a paruṣa after a long vowel (Appakavi)"
        return "PRASA-PURVAKA-04A", why
    if within_appakavi:
        return "PRASA-PURVAKA-04B", f"consonant {cons} is a paruṣa following the long vowel {purva_vowel} (Appakavi)"
    return ("PRASA-PURVAKA-04C",
            f"consonant {cons} after vowel {purva_vowel or '-'} is outside both Ananta's (ప/ట) and Appakavi's "
            f"(paruṣa after long vowel) restrictions — attested only in wider classical usage")


class _PairLog:
    """Collects what a pair comparison finds: the rules that carried the match, the
    classifications, the hard failures and the trail entries."""

    def __init__(self, scope: str):
        self.scope = scope
        self.trail: list[TrailEntry] = []
        self.rules_used: list[str] = []
        self.classes: list[str] = []
        self.hard: list[dict] = []

    def passed(self, rule: str, detail: str, data: Optional[dict] = None) -> None:
        self.rules_used.append(rule)
        self.classes.append(rule)
        self.trail.append(TrailEntry(rule, "pass", self.scope, detail, data or {}))

    def note(self, rule: str, detail: str) -> None:
        self.trail.append(TrailEntry(rule, "note", self.scope, detail))

    def failed(self, rule: str, detail: str, data: Optional[dict] = None) -> None:
        self.hard.append({"rule": rule, "scope": self.scope, "detail": detail})
        self.trail.append(TrailEntry(rule, "fail", self.scope, detail, data or {}))


def _purnabindu_step(a: LineFeatures, b: LineFeatures, rs: Ruleset, log: _PairLog) -> Optional[dict]:
    """PRASA-PURVAKA-01: a ం before the prāsa akshara must appear in every line —
    unless the asymmetric pair fits one of the bindu specials (returned)."""
    if a.purva_purnabindu == b.purva_purnabindu:
        if a.purva_purnabindu:
            log.passed("PRASA-PURVAKA-01", f"both prāsa aksharas are preceded by ం ({a.purva} | {b.purva})")
        else:
            log.trail.append(TrailEntry("PRASA-PURVAKA-01", "pass", log.scope, "neither prāsa akshara is preceded by ం"))
        return None
    special = _bindu_special(a, b, rs)
    if special:
        log.passed(special["rule"], special["detail"], {"status": rs.status(special["rule"])})
        log.note("PRASA-PURVAKA-01", f"pūrṇabindu asymmetry tolerated only because the pair fits {special['rule']}")
        return special
    w, wo = (a, b) if a.purva_purnabindu else (b, a)
    log.failed("PRASA-PURVAKA-01",
               f"line {w.index}: prāsa akshara {w.prasa} is preceded by ం ({w.purva}) but line {wo.index} "
               f"({wo.purva} {wo.prasa}) is not; a pūrṇabindu before the prāsa must appear in every line")
    if wo.ardhabindu_before:
        log.failed("PRASA-DEFECT-PURNARDHABINDU",
                   f"line {w.index} has ం and line {wo.index} has ఁ before the prāsa akshara: "
                   f"పూర్ణార్ధబిందు ప్రాస is a recognised defect")
    return None


def _visarga_step(a: LineFeatures, b: LineFeatures, log: _PairLog) -> None:
    """PRASA-PURVAKA-02: a ః before the prāsa akshara must appear in every line."""
    if a.purva_visarga != b.purva_visarga:
        w, wo = (a, b) if a.purva_visarga else (b, a)
        log.failed("PRASA-PURVAKA-02",
                   f"line {w.index}: prāsa akshara {w.prasa} is preceded by ః ({w.purva}) but line {wo.index} "
                   f"({wo.purva} {wo.prasa}) is not; a visarga before the prāsa must appear in every line")
    elif a.purva_visarga:
        log.passed("PRASA-PURVAKA-02", f"both prāsa aksharas are preceded by ః ({a.purva} | {b.purva})")
    else:
        log.trail.append(TrailEntry("PRASA-PURVAKA-02", "pass", log.scope, "neither prāsa akshara is preceded by ః"))


def _ardhabindu_step(a: LineFeatures, b: LineFeatures, rs: Ruleset, log: _PairLog) -> None:
    """PRASA-PURVAKA-03 (both lines have ఁ) / 04A-C (only one has: ఖండాఖండ ప్రాస)."""
    if a.ardhabindu_before and b.ardhabindu_before:
        log.passed("PRASA-PURVAKA-03", "both prāsa aksharas are preceded by ఁ (uniform ardhabindu prāsa)")
    elif a.ardhabindu_before or b.ardhabindu_before:
        w = a if a.ardhabindu_before else b
        wo = b if w is a else a
        variant, why = _khandakhanda_variant(w, rs)
        log.passed(variant, f"line {w.index} has ఁ before the prāsa akshara and line {wo.index} has not "
                            f"(ఖండాఖండ ప్రాస): {why}", {"status": rs.status(variant)})


def _neutral_feature_notes(a: LineFeatures, b: LineFeatures, scope: str) -> list[TrailEntry]:
    """Informational trail entries: features that never change the verdict (PRASA-SAMA-02..11, POS-06)."""
    notes: list[TrailEntry] = []
    if a.vowel != b.vowel:
        notes.append(TrailEntry("PRASA-SAMA-02", "info", scope,
                                f"vowels differ ({a.vowel or '-'} / {b.vowel or '-'}): vowels never affect prāsa"))
    for ln in (a, b):
        where = f"line:{ln.index}"
        if ln.vowel in ("ఋ", "ౠ") and not ln.bare_vowel:
            notes.append(TrailEntry("PRASA-SAMA-03", "info", where,
                                    f"{ln.prasa} carries vaṭruvasuḍi ({ln.vowel}); it is a vowel, not a ర-conjunct"))
        if ln.vowel in ("ఌ", "ౡ"):
            notes.append(TrailEntry("PRASA-SAMA-04", "info", where, f"{ln.prasa} carries the vocalic vowel {ln.vowel}; neutral for prāsa"))
        if ln.trailing_anusvara:
            notes.append(TrailEntry("PRASA-SAMA-05", "info", where, f"{ln.prasa} is followed by ం (bindu-sahita); neutral for prāsa"))
        if ln.trailing_visarga:
            notes.append(TrailEntry("PRASA-SAMA-06", "info", where, f"{ln.prasa} is followed by ః (visarga-sahita); neutral for prāsa"))
        for c in ln.trailing_pollu:
            rule = "PRASA-SAMA-07" if c == "న" else "PRASA-SAMA-08"
            notes.append(TrailEntry(rule, "info", where, f"{ln.prasa} ends in the dead consonant {c}్ (trailing); neutral for prāsa"))
        if ln.dantya_forms:
            notes.append(TrailEntry("PRASA-SAMA-09", "info", where,
                                    f"{ln.prasa} uses the dental letter(s) {''.join(ln.dantya_forms)}; "
                                    f"read as {''.join(DANTYA_MAP[d] for d in ln.dantya_forms)} (savarṇa)"))
        if ln.fused_from_purva:
            notes.append(TrailEntry("PRASA-POS-06", "info", where,
                                    f"dead consonant {render_onset(ln.fused_from_purva)}్ at the end of the pre-prāsa "
                                    f"akshara {ln.purva} fuses with {ln.prasa}: effective onset {ln.onset_text}"))
        if ln.laghu_ya_hint:
            notes.append(TrailEntry("PRASA-SAMA-11", "info", where,
                                    f"{ln.prasa} begins a word after a vowel-final word: probably a yaḍāgama (laghu య); "
                                    f"laghu and alaghu య rhyme freely"))
    if a.prasa_weight != b.prasa_weight:
        notes.append(TrailEntry("PRASA-SAMA-10", "info", scope,
                                f"prāsa aksharas differ in weight ({a.prasa_weight} / {b.prasa_weight}); "
                                f"the weight rule binds the pre-prāsa akshara only"))
    return notes


def compare_pair(a: LineFeatures, b: LineFeatures, rs: Ruleset) -> PairVerdict:
    """Evaluate one pair of lines: the three pre-prāsa sign rules (ం, ః, ఁ), then
    the onsets, then the informational notes."""
    log = _PairLog(_pair_scope(a, b))
    special = _purnabindu_step(a, b, rs, log)
    _visarga_step(a, b, log)
    _ardhabindu_step(a, b, rs, log)
    if special is None:
        oc = compare_onsets(a, b, rs)
        log.trail.extend(oc.trail)
        log.rules_used.extend(oc.rules_used)
        log.classes.extend(oc.classifications)
        if oc.fail_rule:
            log.hard.append({"rule": oc.fail_rule, "scope": log.scope, "detail": oc.detail})
    for r in list(log.rules_used):          # superseded treatise rules: name them whenever a superseding rule carried the match
        sup = rs.rule(r).get("supersedes")
        if sup:
            log.note(sup, f"{sup} ({rs.name(sup)}) is superseded by {r} [{rs.status(r)}]; "
                          f"see that rule's statement for the reason and how to disable it")
    log.trail.extend(_neutral_feature_notes(a, b, log.scope))
    scope, trail, rules_used, classes, hard = log.scope, log.trail, log.rules_used, log.classes, log.hard
    statuses = [rs.status(r) for r in rules_used]
    min_profile = None if hard else rs.min_profile(statuses)
    return PairVerdict(lines=(a.index, b.index), reading=f"{a.reading}|{b.reading}",
                       rules_used=rs.sort_rules(rules_used), statuses_used=sorted(set(statuses)),
                       hard_failures=hard, min_profile=min_profile,
                       classifications=rs.sort_rules(classes), trail=trail)

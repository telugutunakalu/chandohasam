# -*- coding: utf-8 -*-
"""
Stanza evaluation: ``evaluate(padas, profile, meter)`` -> ``PrasaResult``.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Optional

from .constants import KHANDAKHANDA_RULES
from .akshara import render_onset
from .ruleset import Ruleset, load_ruleset, _meter_index
from .features import LineFeatures, extract_line, druta_sandhi_reading
from .compare import TrailEntry, PairVerdict, compare_pair, _pair_scope


@dataclass
class PrasaResult:
    profile: str
    matched: bool
    applicable: bool
    min_profile: Optional[str]
    would_match_under: Optional[str]
    prasa_consonant: Optional[str]
    label_te: str
    label_en: str
    classifications: list[dict]
    violations: list[dict]
    lines: list[dict]
    pairs: list[dict]
    trail: list[dict]
    ruleset: dict
    meter: Optional[dict]
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, **kw) -> str:
        kw.setdefault("ensure_ascii", False)
        kw.setdefault("indent", 2)
        return json.dumps(self.to_dict(), **kw)


def _weight_rule(lines: list[LineFeatures], rs: Ruleset, exempt_reason: Optional[str]) -> tuple[bool, list[TrailEntry], list[str]]:
    """PRASA-PURVAKSHARA-01: the FIRST akshara of every line must have one weight."""
    trail: list[TrailEntry] = []
    if exempt_reason:
        trail.append(TrailEntry("PRASA-PURVAKSHARA-01", "na", "stanza", exempt_reason))
        return True, trail, []
    pos = [ln.purva_weight_positional for ln in lines]
    view = {f"line {ln.index}": {"akshara": ln.purva, "positional": ln.purva_weight_positional,
                                 "intrinsic": ln.purva_weight_intrinsic} for ln in lines}
    if len(set(pos)) == 1:
        trail.append(TrailEntry("PRASA-PURVAKSHARA-01", "pass", "stanza",
                                f"pre-prāsa aksharas are uniformly {'guru' if pos[0] == 'U' else 'laghu'}: "
                                + ", ".join(f"{ln.purva}({ln.purva_weight_positional})" for ln in lines), view))
        lengthened = [ln for ln in lines if ln.purva_weight_positional == "U" and ln.purva_weight_intrinsic == "I"]
        if lengthened:
            trail.append(TrailEntry("PRASA-PURVAKSHARA-02", "info", "stanza",
                                    "short-vowel pre-prāsa akshara(s) count as guru because a conjunct follows: "
                                    + ", ".join(f"line {ln.index} {ln.purva}+{ln.prasa}" for ln in lengthened)))
        return True, trail, ["PRASA-PURVAKSHARA-01"]
    hinted = [ln for ln in lines if ln.light_cluster_hint]
    if hinted:
        eff = [ln.purva_weight_intrinsic if ln.light_cluster_hint else ln.purva_weight_positional for ln in lines]
        if len(set(eff)) == 1:
            trail.append(TrailEntry("PRASA-PURVAKSHARA-04", "pass", "stanza",
                                    "uniform only when the repha cluster(s) are read as LIGHT (Telugu krāravaḍi / "
                                    "laghudvitva): " + ", ".join(f"line {ln.index} {ln.prasa_word} [{ln.light_cluster_hint}]"
                                                                 for ln in hinted) + " — heuristic",
                                    {**view, "heuristic": True}))
            return True, trail, ["PRASA-PURVAKSHARA-04"]
    trail.append(TrailEntry("PRASA-PURVAKSHARA-01", "fail", "stanza",
                            "pre-prāsa aksharas mix guru and laghu: "
                            + ", ".join(f"line {ln.index} {ln.purva}({ln.purva_weight_positional})" for ln in lines), view))
    return False, trail, []


def _compose_labels(lines: list[LineFeatures], classes: list[str], rs: Ruleset) -> tuple[str, str, Optional[str]]:
    l1 = lines[0]
    onset = l1.onset
    core_te, core_en = "", ""
    maitri_rules = [c for c in classes if rs.rule(c).get("category") in ("maitri", "structural")]
    if maitri_rules:
        core_te = rs.label(maitri_rules[0], "te")
        core_en = rs.label(maitri_rules[0], "en")
    elif "PRASA-SAMA-01" in classes:
        if len(onset) == 1:
            special = rs.consonant_info.get(onset[0], {}).get("prasa_name")
            core_te = special or f"'{onset[0]}'కార ప్రాస"
            core_en = f"{onset[0]}-kāra prāsa (samaprāsa)"
        else:
            kind_te = "ద్విత్వాక్షర" if "PRASA-SAMYUKTA-03" in classes else "సంయుక్తాక్షర"
            kind_en = "dvitvākṣara (geminate)" if "PRASA-SAMYUKTA-03" in classes else "saṁyuktākṣara (conjunct)"
            core_te = f"'{render_onset(onset)}' {kind_te} ప్రాస"
            core_en = f"{render_onset(onset)} {kind_en} prāsa"
    prefixes_te, prefixes_en = [], []
    if "PRASA-PURVAKA-01" in classes:
        prefixes_te.append("పూర్ణబిందుపూర్వక"); prefixes_en.append("pūrṇabindu-pūrvaka")
    if "PRASA-PURVAKA-02" in classes:
        prefixes_te.append("విసర్గపూర్వక"); prefixes_en.append("visarga-pūrvaka")
    if "PRASA-PURVAKA-03" in classes:
        prefixes_te.append("అర్ధబిందు"); prefixes_en.append("ardhabindu")
    if any(c in KHANDAKHANDA_RULES for c in classes):
        prefixes_te.append("ఖండాఖండ"); prefixes_en.append("khaṇḍākhaṇḍa")
    label_te = " ".join(prefixes_te + [core_te]).strip()
    label_en = " ".join(prefixes_en + [core_en]).strip()
    cons = render_onset(onset) if onset else (l1.vowel or None)
    return label_te, label_en, cons


def evaluate(padas: list[str], profile: str = "strict", meter: Optional[str] = None,
             meter_class: Optional[str] = None, ruleset: Optional[Ruleset] = None,
             allow_druta_sandhi_reading: bool = True) -> PrasaResult:
    """Evaluate the prāsa of a stanza (list of pādas) under ``profile``.

    All pairs of lines are compared (an n-line stanza yields n(n-1)/2 pair
    verdicts); the stanza matches when every pair matches AND the pre-prāsa
    weight rule holds.  ``min_profile`` is the least permissive profile under
    which the stanza matches, independent of the requested ``profile``.
    """
    rs = ruleset or load_ruleset()
    if profile not in rs.profiles:
        raise ValueError(f"unknown profile {profile!r}; choose from {list(rs.profiles)}")
    rs_meta = {"path": str(rs.path) if rs.path else None, "schema_version": rs.version,
               "source": rs.data.get("metadata", {}).get("source")}
    trail: list[TrailEntry] = []
    meter_info, applicable, exempt_reason = _meter_context(meter, meter_class, rs, trail)

    if len(padas) < 2:
        return PrasaResult(profile, False, applicable, None, None, None, "", "", [], [], [], [],
                           [asdict(t) for t in trail], rs_meta, meter_info,
                           error="PRASA-POS-04: a stanza needs at least two pādas to carry a prāsa")
    lines = [extract_line(p, i + 1, rs) for i, p in enumerate(padas)]
    bad = [ln for ln in lines if ln.error]
    if bad:
        return PrasaResult(profile, False, applicable, None, None, None, "", "", [], [],
                           [asdict(ln) for ln in lines], [], [asdict(t) for t in trail], rs_meta, meter_info,
                           error="; ".join(f"line {ln.index}: {ln.error}" for ln in bad))
    trail.extend(_line_notes(lines))

    pairs, lines = _compare_all_pairs(lines, rs, allow_druta_sandhi_reading)
    trail.extend(t for pv in pairs for t in pv.trail)
    weight_ok, wtrail, wclasses = _weight_rule(lines, rs, exempt_reason)
    trail.extend(wtrail)
    trail.extend(_adhika_note(lines))

    classes = rs.sort_rules([c for pv in pairs for c in pv.classifications] + wclasses)
    pair_min = [pv.min_profile for pv in pairs]
    if any(m is None for m in pair_min) or not weight_ok:
        min_profile = None
    else:
        min_profile = max(pair_min, key=lambda m: rs.profile_order.index(m))
    violations = _violations_under(profile, pairs, wtrail, weight_ok, rs)
    matched = not violations
    would = min_profile if (not matched and min_profile is not None) else None
    label_te, label_en, cons = _compose_labels(lines, classes, rs)
    class_records = [{"rule": c, "name_te": rs.name(c, "te"), "name_en": rs.name(c, "en"), "status": rs.status(c)}
                     for c in classes]
    return PrasaResult(
        profile=profile, matched=matched, applicable=applicable, min_profile=min_profile,
        would_match_under=would, prasa_consonant=cons, label_te=label_te, label_en=label_en,
        classifications=class_records, violations=violations,
        lines=[asdict(ln) for ln in lines],
        pairs=[{"lines": list(pv.lines), "reading": pv.reading, "rules_used": pv.rules_used,
                "statuses_used": pv.statuses_used, "min_profile": pv.min_profile,
                "hard_failures": pv.hard_failures, "classifications": pv.classifications} for pv in pairs],
        trail=[asdict(t) for t in trail], ruleset=rs_meta, meter=meter_info,
    )


def _meter_context(meter: Optional[str], meter_class: Optional[str], rs: Ruleset,
                   trail: list[TrailEntry]) -> tuple[Optional[dict], bool, Optional[str]]:
    """-> (meter_info, prāsa applicable?, reason the weight rule is exempt)  (PRASA-POS-02)."""
    meter_info: Optional[dict] = None
    applicable = True
    exempt_reason: Optional[str] = None
    if meter:
        rec = _meter_index().get(meter)
        if rec is None:
            meter_info = {"name": meter, "known": False}
            trail.append(TrailEntry("PRASA-POS-02", "note", "stanza", f"meter {meter!r} not found in meter_rules.yaml"))
        else:
            meter_info = {"name": rec["name"], "name_te": rec.get("name_te"), "known": True,
                          "prasa_required": bool(rec.get("prasa")), "type": rec.get("type_of_chandassu")}
            applicable = bool(rec.get("prasa"))
            trail.append(TrailEntry("PRASA-POS-02", "pass" if applicable else "na", "stanza",
                                    f"meter {rec['name']}: lakṣaṇam says prāsa {'required' if applicable else 'absent'}"))
    if meter_class:
        if meter_info is None:
            meter_info = {"name": None, "known": False}
        meter_info["meter_class"] = meter_class
        if meter_class in rs.meter_eligibility.get("purvakshara_rule_exempt_meter_classes", []):
            exempt_reason = f"meter class {meter_class}: the pre-prāsa weight rule is not enforced (asama vṛtta exception)"
    return meter_info, applicable, exempt_reason


def _line_notes(lines: list[LineFeatures]) -> list[TrailEntry]:
    """PRASA-POS-01: one informational entry per line naming its pre-prāsa and prāsa aksharas."""
    return [TrailEntry("PRASA-POS-01", "info", f"line:{ln.index}",
                       f"pre-prāsa akshara {ln.purva!r} ({ln.purva_weight_positional}), prāsa akshara "
                       f"{ln.prasa!r} -> onset {ln.onset_text or ln.vowel}, vowel {ln.vowel or '-'}"
                       + (", ఁ before" if ln.ardhabindu_before else "")
                       + (", ం before" if ln.purva_purnabindu else "")
                       + (", ః before" if ln.purva_visarga else ""),
                       {"tokens": ln.tokens[:4]}) for ln in lines]


def _compare_all_pairs(lines: list[LineFeatures], rs: Ruleset,
                       allow_druta: bool) -> tuple[list[PairVerdict], list[LineFeatures]]:
    """Every pair of lines.  When the written reading fails or needs a relaxation and
    a druta-sandhi reading (PRASA-POS-07, Xన్ + stop -> Xం + sarala) does better,
    that reading is adopted for the line from then on.  Returns the verdicts and
    the (possibly re-read) lines."""
    pairs: list[PairVerdict] = []
    adopted: dict[int, LineFeatures] = {}
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            a, b = adopted.get(i, lines[i]), adopted.get(j, lines[j])
            pv = compare_pair(a, b, rs)
            if pv.min_profile != rs.profile_order[0] and allow_druta:
                alt_a = druta_sandhi_reading(a, rs) or a
                alt_b = druta_sandhi_reading(b, rs) or b
                if alt_a is not a or alt_b is not b:
                    alt_pv = compare_pair(alt_a, alt_b, rs)
                    if _better(alt_pv, pv, rs):
                        why = ("the written reading fails" if pv.min_profile is None
                               else f"the written reading needs profile '{pv.min_profile}'")
                        alt_pv.trail.insert(0, TrailEntry("PRASA-POS-07", "pass", _pair_scope(a, b),
                                                          f"{why}; matched under the druta-sandhi reading "
                                                          f"(Xన్ + paruṣa -> Xం + sarala)", {"reading": "druta_sandhi"}))
                        pv = alt_pv
                        if alt_a is not a:
                            adopted[i] = alt_a
                        if alt_b is not b:
                            adopted[j] = alt_b
            pairs.append(pv)
    if adopted:
        lines = [adopted.get(i, ln) for i, ln in enumerate(lines)]
    return pairs, lines


def _better(alt: PairVerdict, pv: PairVerdict, rs: Ruleset) -> bool:
    """Does the alternative reading need a less permissive profile than the written one?"""
    if alt.min_profile is None:
        return False
    return pv.min_profile is None or rs.profile_order.index(alt.min_profile) < rs.profile_order.index(pv.min_profile)


def _adhika_note(lines: list[LineFeatures]) -> list[TrailEntry]:
    """Surplus (dvyakṣara) prāsa: the 3rd aksharas rhyme too — informational only."""
    third = [ln.third_onset for ln in lines]
    if all(third) and len({tuple(t) for t in third}) == 1:
        return [TrailEntry("PRASA-DEFECT-ADHIKA", "info", "stanza",
                           f"the 3rd aksharas also share the onset {render_onset(third[0])} in every line "
                           f"(dvyakṣara prāsa) — surplus rhyme, not a requirement")]
    return []


def _violations_under(profile: str, pairs: list[PairVerdict], wtrail: list[TrailEntry], weight_ok: bool,
                      rs: Ruleset) -> list[dict]:
    """Hard failures, rules the profile does not accept, and the weight-rule failure."""
    violations: list[dict] = []
    for pv in pairs:
        violations.extend(pv.hard_failures)
        for r in pv.rules_used:
            st = rs.status(r)
            if not rs.accepted(profile, st):
                violations.append({"rule": r, "scope": f"pair:{pv.lines[0]}-{pv.lines[1]}",
                                   "detail": f"{rs.name(r)} has status '{st}'; profile '{profile}' does not accept it "
                                             f"(needs profile '{rs.min_profile([st])}')"})
    if not weight_ok:
        violations.extend({"rule": t.rule, "scope": t.scope, "detail": t.detail} for t in wtrail if t.status == "fail")
    return violations

# -*- coding: utf-8 -*-
"""
Lookup-table views (``lookup_pair``, ``maitri_matrix``) and the fixture replay (``run_attested_examples``).
"""
from __future__ import annotations

from typing import Optional

from .constants import DANTYA_MAP
from .ruleset import Ruleset, load_ruleset
from .stanza import evaluate


def lookup_pair(a: str, b: str, ruleset: Optional[Ruleset] = None) -> dict:
    """The consonant-pair lookup table entry for two single consonants."""
    rs = ruleset or load_ruleset()
    rule = rs.lookup_pair_rule(a, b)
    status = rs.status(rule)
    return {
        "a": a, "b": b, "rule": rule, "status": status,
        "name_en": rs.name(rule, "en"), "name_te": rs.name(rule, "te"),
        "accepted_in": [p for p in rs.profile_order if rs.accepted(p, status)],
        "min_profile": rs.min_profile([status]),
        "source": rs.rule(rule).get("source", {}).get("sections"),
    }


def maitri_matrix(ruleset: Optional[Ruleset] = None) -> list[dict]:
    """Every unordered pair (including identity) of the 35 base consonants: 630 rows."""
    rs = ruleset or load_ruleset()
    base = [c for c in rs.consonants if c not in DANTYA_MAP]
    out = []
    for i, x in enumerate(base):
        for y in base[i:]:
            out.append(lookup_pair(x, y, rs))
    return out


def run_attested_examples(ruleset: Optional[Ruleset] = None) -> list[dict]:
    """Run every ``attested_examples`` fixture from the YAML and report outcomes."""
    rs = ruleset or load_ruleset()
    report = []
    for ex in rs.examples:
        res = {p: evaluate(ex["padas"], profile=p, ruleset=rs, meter_class=ex.get("meter_class"))
               for p in rs.profile_order}
        exp = ex["expected"]
        ok = True
        problems = []
        for p in rs.profile_order:
            if p in exp and exp[p] != res[p].matched:
                ok = False
                problems.append(f"{p}: expected {exp[p]} got {res[p].matched}")
        r0 = res[rs.profile_order[0]]
        if "min_profile" in exp and exp["min_profile"] != r0.min_profile:
            ok = False
            problems.append(f"min_profile: expected {exp['min_profile']} got {r0.min_profile}")
        got_classes = {c["rule"] for c in r0.classifications}
        for c in exp.get("classifications_include", []):
            if c not in got_classes:
                ok = False
                problems.append(f"missing classification {c}")
        got_viol = {v["rule"] for v in r0.violations} | {t["rule"] for t in r0.trail if t["status"] == "fail"}
        for c in exp.get("failing_rules_include", []):
            if c not in got_viol:
                ok = False
                problems.append(f"missing failing rule {c}")
        if "prasa_consonant" in exp and exp["prasa_consonant"] != r0.prasa_consonant:
            ok = False
            problems.append(f"prasa_consonant: expected {exp['prasa_consonant']} got {r0.prasa_consonant}")
        report.append({"id": ex["id"], "ok": ok, "problems": problems, "label_te": r0.label_te,
                       "min_profile": r0.min_profile, "violations": [v["rule"] for v in r0.violations]})
    return report

# -*- coding: utf-8 -*-
"""Replay of the ``attested_examples`` fixtures embedded in ``yati_rules.yaml``.
"""
from __future__ import annotations

from typing import Optional

from .ruleset import Ruleset, _rs
from .verdict import check


def run_attested_examples(ruleset: Optional[Ruleset] = None) -> list[dict]:
    rs = _rs(ruleset)
    report = []
    for ex in rs.examples:
        exp = ex["expect"]
        kw = dict(sandhi=ex.get("sandhi", "hypothesis"), vowel_a=ex.get("vowel_a", ()), vowel_b=ex.get("vowel_b", ()),
                  prev_dead_a=ex.get("prev_dead_a"), prev_dead_b=ex.get("prev_dead_b"),
                  word_a=ex.get("word_a"), word_b=ex.get("word_b"), index_a=ex.get("index_a"), index_b=ex.get("index_b"))
        res = {p: check(ex["a"], ex["b"], p, ruleset=rs, **kw) for p in rs.profile_order}
        problems = []
        if "matched" in exp:
            for p in rs.profile_order:
                if res[p].matched != exp["matched"] and not (exp["matched"] is False and p == "historical" and res[p].best and res[p].best.status == "deprecated"):
                    problems.append(f"{p}: matched={res[p].matched}, expected {exp['matched']}")
        for p in rs.profile_order:
            if p in exp and res[p].matched != exp[p]:
                problems.append(f"{p}: matched={res[p].matched}, expected {exp[p]}")
        chosen = next((res[p] for p in rs.profile_order if res[p].matched), res["strict"])
        if "rule" in exp and chosen.rule != exp["rule"]:
            problems.append(f"rule={chosen.rule}, expected {exp['rule']}")
        if "rule_in" in exp and chosen.rule not in exp["rule_in"]:
            problems.append(f"rule={chosen.rule}, expected one of {exp['rule_in']}")
        if "min_profile" in exp and chosen.min_profile != exp["min_profile"]:
            problems.append(f"min_profile={chosen.min_profile}, expected {exp['min_profile']}")
        if "hypothesis" in exp and chosen.best and chosen.best.hypothesis != exp["hypothesis"]:
            problems.append(f"hypothesis={chosen.best.hypothesis}, expected {exp['hypothesis']}")
        for v in exp.get("vidhana_includes", []):
            if not chosen.best or v not in chosen.best.vidhana:
                problems.append(f"vidhana missing {v}: got {chosen.best.vidhana if chosen.best else None}")
        for r in exp.get("rejected_includes", []):
            if r not in {m.rule for m in res["strict"].rejected}:
                problems.append(f"rejected missing {r}: got {[m.rule for m in res['strict'].rejected]}")
        report.append({"id": ex["id"], "ok": not problems, "problems": problems,
                       "got": {p: (res[p].matched, res[p].rule) for p in rs.profile_order}})
    return report

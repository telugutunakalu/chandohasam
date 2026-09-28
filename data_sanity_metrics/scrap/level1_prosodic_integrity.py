"""Level 1 — Prosodic integrity (§5.1, Table 4 row 1).

Paper's metric: share of master couplets passing the chandas scanner (100%).
Because that same scanner is the inclusion filter, 100% holds by construction.
This script reproduces it and then adds what the metric cannot tell us on its
own: whether an *independent* scanner agrees.

    1. paper analyser on master                    (the paper's number)
    2. chandohasam (meter_engine, forced dvipada)  per-rule pass rates on master
    3. chandohasam on the 181 schema_a records the paper's analyser rejected
       (control: an agreeing scanner should reject most of them too)
    4. per-rule 2x2 agreement over schema_a, and which yati rule the paper's
       analyser used to accept each line (primary maitri vs fallbacks)

Writes outputs/level1_prosodic_integrity.json and
       outputs/cache/chandohasam_verdicts.json

Run:  python level1_prosodic_integrity.py [--workers 12]
"""
import argparse
import json
from collections import Counter
from multiprocessing import Pool

import config
from common.dataset import load_records, load_subset
from common.io import pct, print_table, save_result
from common.scanners import chandohasam_verdict

RULES = ["gana", "prasa", "yati_l1", "yati_l2", "valid"]
PROFILES = ("strict", "relaxed")


def _scan(item):
    rid, poem = item
    try:
        return rid, chandohasam_verdict(poem, PROFILES)
    except Exception as e:  # keep going; count failures
        return rid, {"error": f"{type(e).__name__}: {e}"}


def run_chandohasam(records, workers):
    cache = config.CACHE_DIR / "chandohasam_verdicts.json"
    done = json.loads(cache.read_text()) if cache.exists() else {}
    todo = [(r["id"], r["poem"]) for r in records if str(r["id"]) not in done]
    if todo:
        print(f"scanning {len(todo):,} couplets with chandohasam ({workers} workers)...")
        with Pool(workers) as pool:
            for k, (rid, v) in enumerate(pool.imap_unordered(_scan, todo, chunksize=64), 1):
                done[str(rid)] = v
                if k % 5000 == 0:
                    print(f"  {k:,}/{len(todo):,}")
        cache.write_text(json.dumps(done))
    return {int(k): v for k, v in done.items()}


def rule_value(v, profile, rule):
    """Flatten a chandohasam verdict to one boolean per rule."""
    if "error" in v:
        return False
    if rule == "gana":
        return bool(v["gana"])
    return bool(v[profile].get(rule))


def pass_rates(ids, ch, profile):
    return {rule: pct(sum(rule_value(ch[i], profile, rule) for i in ids), len(ids)) for rule in RULES}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()

    records = load_records()
    master = load_subset("master")
    schema_a = load_subset("schema_a")
    master_ids = {r["id"] for r in master}
    rejected = [r for r in schema_a if r["id"] not in master_ids]
    paper = json.loads((config.CACHE_DIR / "paper_analyser_verdicts.json").read_text())

    # 1. the paper's number
    paper_pass = pct(sum(paper[r["id"]]["valid"] for r in master), len(master))
    print(f"[1] paper analyser on master: {paper_pass:.1f}%  (paper: {config.PAPER['level1_pass_pct']}%)")

    # 2–3. independent scanner
    ch = run_chandohasam(schema_a, args.workers)
    errors = sum("error" in ch[r["id"]] for r in schema_a)
    result = {"n_master": len(master), "n_rejected": len(rejected), "paper_pass_pct": paper_pass,
              "chandohasam_errors": errors, "chandohasam": {}}
    rows = []
    for prof in PROFILES:
        m = pass_rates([r["id"] for r in master], ch, prof)
        rj = pass_rates([r["id"] for r in rejected], ch, prof)
        result["chandohasam"][prof] = {"master_pass_pct": m, "rejected_pass_pct": rj}
        for rule in RULES:
            rows.append([prof, rule, m[rule], rj[rule]])
    print(f"\n[2,3] chandohasam (forced dvipada), % passing; errors: {errors}")
    print_table(["profile", "rule", f"master n={len(master)}", f"paper-rejected n={len(rejected)}"], rows)

    # 4a. per-rule agreement over schema_a (paper vs chandohasam relaxed)
    agreement = {}
    rows = []
    for rule in RULES:
        c = Counter((bool(paper[r["id"]][rule]), rule_value(ch[r["id"]], "relaxed", rule)) for r in schema_a)
        agree = c[(True, True)] + c[(False, False)]
        agreement[rule] = {"both_pass": c[(True, True)], "paper_only": c[(True, False)],
                           "chandohasam_only": c[(False, True)], "both_fail": c[(False, False)],
                           "agreement_pct": pct(agree, len(schema_a))}
        rows.append([rule, c[(True, True)], c[(True, False)], c[(False, True)], c[(False, False)],
                     agreement[rule]["agreement_pct"]])
    result["agreement_schema_a_relaxed"] = agreement
    print(f"\n[4a] paper analyser vs chandohasam-relaxed over schema_a (n={len(schema_a)})")
    print_table(["rule", "both pass", "paper only", "chandohasam only", "both fail", "agree %"], rows)

    # 4b. which yati rule let each master line through in the paper's analyser
    yati_rules = Counter(rule for r in master for rule in paper[r["id"]]["yati_rule"])
    result["paper_yati_rule_usage_master_lines"] = dict(yati_rules)
    print("\n[4b] paper analyser: yati rule used per master line")
    print_table(["match_type", "lines", "%"],
                [[k, v, pct(v, 2 * len(master))] for k, v in yati_rules.most_common()])

    # 4c. where chandohasam's yati rejections come from: the paper's accepting rule
    cross = Counter()
    for r in master:
        v = ch[r["id"]]
        for line, key in enumerate(("yati_l1", "yati_l2")):
            cross[(paper[r["id"]]["yati_rule"][line], rule_value(v, "relaxed", key))] += 1
    by_rule = {}
    for rule in yati_rules:
        ok, bad = cross[(rule, True)], cross[(rule, False)]
        by_rule[rule] = {"lines": ok + bad, "chandohasam_rejects": bad, "reject_pct": pct(bad, ok + bad)}
    result["yati_rejects_by_paper_rule"] = by_rule
    print("\n[4c] chandohasam-relaxed yati rejections, by the rule the paper's analyser accepted with")
    print_table(["paper match_type", "lines", "chandohasam rejects", "%"],
                [[k, v["lines"], v["chandohasam_rejects"], v["reject_pct"]] for k, v in by_rule.items()])

    # syllables per line (the 11–15 window)
    syl = Counter(n for r in master for n in paper[r["id"]]["syllables"])
    result["syllables_per_line"] = dict(sorted(syl.items()))

    # examples of disagreement for manual adjudication
    examples = []
    for r in master:
        v = ch[r["id"]]
        if "error" in v or not v["relaxed"]["valid"]:
            failed = [rule for rule in RULES[:-1] if not rule_value(v, "relaxed", rule)]
            examples.append({"id": r["id"], "source": r.get("source"), "poem": r["poem"],
                             "chandohasam_failed": failed,
                             "paper_yati_rule": paper[r["id"]]["yati_rule"],
                             "chandohasam_candidates": v.get("candidates")})
    result["disagreement_count_master_relaxed"] = len(examples)
    result["disagreement_by_rule"] = dict(Counter(f for e in examples for f in e["chandohasam_failed"]))
    result["disagreement_examples"] = examples[:40]
    print(f"\nmaster couplets chandohasam-relaxed rejects: {len(examples):,}; by rule: "
          f"{result['disagreement_by_rule']}")

    save_result("level1_prosodic_integrity", result)


if __name__ == "__main__":
    main()

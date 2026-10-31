"""Runs the poetry_metrics suite (anuprasa v3, madhurya, ojas, prasada, chandas distance) on
study 2's 99 fine-tuned-model poems, gated by a word-attestation proxy (prasada's own
known_word_share -- NOT the project's full word-resolution pipeline, which needs padarchana.db
and isn't available in this environment; see poetry_metrics/anuprasa_v3.py and the README's
caveat on this).

    python3 study2_poetics.py
"""
import sys
from pathlib import Path
from collections import defaultdict
import statistics
import csv

REPO = Path(__file__).resolve().parent.parent
PM = REPO / "poetry_metrics"
sys.path.insert(0, str(PM))

import madhurya, ojas, prasada, anuprasa_v3  # noqa: E402
import chandas_distance as cd                # noqa: E402

from sc_common import HUMAN_EVALS, RESULTS_DIR, load_study2_pool  # noqa: E402

madhurya_baseline = madhurya.load_baseline()
ojas_baseline = ojas.load_baseline()
chandas_baseline = cd.load_baseline()
prasada_model = prasada.load_model()

pool = load_study2_pool()
import json
study2 = json.load(open(HUMAN_EVALS / "human_eval_poems_study2.json", encoding="utf-8"))["poems"]

rows = []
for p in study2:
    eval_id = p["eval_id"]
    lines = p["lines"]
    model = p["source_dataset"]
    meter = p["declared_meter"]

    anu3 = anuprasa_v3.score_poem(lines)
    mad = madhurya.score_poem(lines, madhurya_baseline)
    oj = ojas.score_poem(lines, ojas_baseline)
    pr = prasada.score_poem(lines, prasada_model)
    try:
        chd = cd.score_poem(lines, chandas_baseline, meter=meter)
    except Exception:
        chd = {}

    rows.append(dict(
        eval_id=eval_id, model=model, meter=meter,
        ref_corpus_coverage=pr.get("known_word_share"),
        anuprasa_v3=anu3["anuprasa"], anuprasa_v3_level=anu3["label"],
        madhurya=mad.get("madhurya"), madhurya_level=mad.get("label"),
        ojas=oj.get("ojas"), ojas_level=oj.get("label"),
        prasada_surprisal=pr.get("surprisal"), prasada_level=pr.get("label"),
        chandas_skill=chd.get("skill"),
    ))

out_path = RESULTS_DIR / "study2_poetics.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print(f"wrote {out_path}")


def summarize(items, label):
    print(f"\n=== {label}: n={len(items)} ===")
    by_model = defaultdict(list)
    for r in items:
        by_model[r["model"]].append(r)
    for model, m_items in sorted(by_model.items()):
        def mean(key):
            vals = [it[key] for it in m_items if it[key] is not None]
            return statistics.mean(vals) if vals else float("nan")
        print(f"  {model:14s} n={len(m_items):3d}  coverage={mean('ref_corpus_coverage'):.3f}  "
              f"anuprasa_v3={mean('anuprasa_v3'):.3f}  madhurya={mean('madhurya'):.3f}  "
              f"ojas={mean('ojas'):.2f}  prasada={mean('prasada_surprisal'):.3f}  "
              f"chandas_skill={mean('chandas_skill'):.3f}")


summarize(rows, "ALL study-2 poems (no gating)")
for thresh in (0.70, 0.85):
    gated = [r for r in rows if r["ref_corpus_coverage"] is not None and r["ref_corpus_coverage"] >= thresh]
    summarize(gated, f"ref.-corpus coverage >= {thresh}")

print("\nDONE")

"""Builds the pooled training table for Coherence/Adherence: every group-A (annotator, poem) rating
of study 1, joined to its poem and bhavam text.

Reads human_evals/results/study1/ratings.csv (committed, anonymised: annotator codes A1-A5, never
real usernames) and human_evals/annotation_app/data/poems.json (committed). Writes
data/pooled_study1.csv (gitignored — rebuild with this script; one row per (annotator, poem),
columns: annotator, eval_id, bhavam, poem_text, bhavam_text, source_dataset, source_id, meter).

    python3 build_dataset.py
"""
import csv

from sc_common import DATA_DIR, GROUP_A_CODES, HUMAN_EVALS, load_poem_pool

pool = load_poem_pool()
rows = list(csv.DictReader(open(HUMAN_EVALS / "results" / "study1" / "ratings.csv", encoding="utf-8")))
rows = [r for r in rows if r["group"] == "A" and r["annotator"] in GROUP_A_CODES and r["bhavam"]]

out_rows = []
missing = 0
for r in rows:
    p = pool.get(r["eval_id"])
    if p is None:
        missing += 1
        continue
    out_rows.append(dict(
        annotator=r["annotator"], eval_id=r["eval_id"], bhavam=r["bhavam"],
        poem_text=p["poem_text"], bhavam_text=p["bhavam_text"],
        source_dataset=p["source_dataset"], source_id=p["source_id"], meter=p["meter"],
    ))

out_path = DATA_DIR / "pooled_study1.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
    w.writeheader()
    w.writerows(out_rows)

print(f"{len(out_rows)} rows ({missing} ratings had no matching poem in the pool), "
      f"{len(set(r['eval_id'] for r in out_rows))} unique poems -> {out_path}")

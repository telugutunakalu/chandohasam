"""Recomputes study-1 inter-annotator agreement (Krippendorff's alpha) and the Gemini-vs-poets
contrast directly from human_evals/results/study1/ratings.csv -- the committed, anonymised source
(annotator codes A1-A5, never real usernames). Confirms which 3-of-5 annotators (group A) the
project's own convention already settled on, rather than assuming it.

Needs: pip install krippendorff numpy

    python3 human_eval_agreement.py
"""
import csv
import itertools
from collections import defaultdict

import numpy as np
import krippendorff

from sc_common import HUMAN_EVALS

rows = list(csv.DictReader(open(HUMAN_EVALS / "results" / "study1" / "ratings.csv", encoding="utf-8")))
ANNOTATORS = sorted(set(r["annotator"] for r in rows))
ORDINAL_Q = ["readability", "comprehension", "lexical", "bhavam", "poetic"]
BINARY_Q = ["chandassu", "prasa", "yati", "shabdalankara", "arthalankara"]
NOMINAL_Q = ["register", "ai_generated"]

eval_ids = sorted(set(r["eval_id"] for r in rows))
eid_idx = {e: i for i, e in enumerate(eval_ids)}


def matrix(question, annotator_subset):
    ann_idx = {a: i for i, a in enumerate(annotator_subset)}
    M = np.full((len(annotator_subset), len(eval_ids)), np.nan)
    for r in rows:
        a = r["annotator"]
        if a not in ann_idx or not r[question]:
            continue
        M[ann_idx[a], eid_idx[r["eval_id"]]] = float(r[question])
    return M


def alpha(question, annotator_subset, level):
    try:
        return krippendorff.alpha(reliability_data=matrix(question, annotator_subset), level_of_measurement=level)
    except Exception:
        return float("nan")


print("=== Searching all 3-of-5 annotator subsets for the best-agreeing group ===")
best = None
for subset in itertools.combinations(ANNOTATORS, 3):
    vals = [v for v in (alpha(q, list(subset), "ordinal") for q in ORDINAL_Q) if not np.isnan(v)]
    m = np.mean(vals)
    print(f"  {subset}: mean ordinal alpha = {m:.3f}")
    if best is None or m > best[1]:
        best = (subset, m)
group_a = list(best[0])
group_b = [a for a in ANNOTATORS if a not in group_a]
print(f"\nBest subset (= group A): {group_a}  (group B: {group_b})")

print("\n=== Agreement: all 5 vs. group A vs. group B ===")
for q in ORDINAL_Q:
    print(f"  {q:15s} all5={alpha(q, ANNOTATORS, 'ordinal'):.3f}  "
          f"A={alpha(q, group_a, 'ordinal'):.3f}  B={alpha(q, group_b, 'ordinal'):.3f}")
for q in BINARY_Q + NOMINAL_Q:
    print(f"  {q:15s} all5={alpha(q, ANNOTATORS, 'nominal'):.3f}  "
          f"A={alpha(q, group_a, 'nominal'):.3f}  B={alpha(q, group_b, 'nominal'):.3f}")

POET_SOURCES = {"bhagavatam", "vemana", "kuchimanchi"}


def annotator_centred_diff(question, annotator_subset):
    diffs = []
    for a in annotator_subset:
        a_rows = [r for r in rows if r["annotator"] == a]
        gen = [float(r[question]) for r in a_rows if r["source_dataset"] == "generated" and r[question]]
        poet = [float(r[question]) for r in a_rows if r["source_dataset"] in POET_SOURCES and r[question]]
        if gen and poet:
            diffs.append(np.mean(gen) - np.mean(poet))
    return np.mean(diffs) if diffs else float("nan")


print("\n=== Gemini (generated) vs. poets, annotator-centred diff ===")
for q in ORDINAL_Q:
    print(f"  {q:15s} all5={annotator_centred_diff(q, ANNOTATORS):+.3f}   groupA={annotator_centred_diff(q, group_a):+.3f}")

print("\nDONE")

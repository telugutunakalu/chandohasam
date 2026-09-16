"""Batch-level author attribution via MAUVE: how big must the batch be?

MAUVE cannot classify a single poem (it compares distributions, and is
unreliable below ~n=50/side). But it CAN attribute a BATCH: score the batch
against each poet's held-out reference corpus and pick the argmax.

Protocol: for each poet, draw `trials` disjoint-ish batches of size k from
one half of their corpus; references are the other halves of all three
corpora, subsampled to k (MAUVE needs equal n). Attribution is correct when
the true poet's reference wins. Uses cached EmbeddingGemma vectors.
"""

import json
import random
from pathlib import Path

import numpy as np

from run_mauve_experiment import mauve_score

HERE = Path(__file__).resolve().parent
POETS = ["pothana", "kuchimanchi", "vemana"]
PROMPT = "Clustering"
SIZES = [10, 25, 50, 100]
TRIALS = 12


def main():
    emb = {p: np.load(HERE / "embeddings_cache" / f"{p}_{PROMPT}.npy")
           for p in POETS}

    # split each corpus: first half = query pool, second half = reference
    pools, refs = {}, {}
    for p in POETS:
        idx = list(range(len(emb[p])))
        random.Random(42).shuffle(idx)
        half = len(idx) // 2
        pools[p] = emb[p][sorted(idx[:half])]
        refs[p] = emb[p][sorted(idx[half:])]

    results = {}
    print(f"{'batch k':>8} | {'accuracy':>9} | per-poet correct/trials")
    for k in SIZES:
        correct = 0
        per_poet = {}
        detail = []
        for p in POETS:
            ok = 0
            for t in range(TRIALS):
                rng = np.random.default_rng(1000 * k + t)
                batch = pools[p][rng.choice(len(pools[p]), k, replace=False)]
                scores = {}
                for r in POETS:
                    ref = refs[r][rng.choice(len(refs[r]), k, replace=False)]
                    scores[r], _ = mauve_score(batch, ref, seed=t)
                pred = max(scores, key=scores.get)
                ok += pred == p
                detail.append({"true": p, "pred": pred, "k": k,
                               "scores": {a: round(v, 4) for a, v in scores.items()}})
            per_poet[p] = ok
            correct += ok
        acc = correct / (len(POETS) * TRIALS)
        results[k] = {"accuracy": acc, "per_poet": per_poet, "trials": TRIALS}
        print(f"{k:>8} | {acc:>8.1%} | " +
              "  ".join(f"{p}:{per_poet[p]}/{TRIALS}" for p in POETS))

    (HERE / "results_batch_attribution.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")
    print("\nWrote results_batch_attribution.json")


if __name__ == "__main__":
    main()

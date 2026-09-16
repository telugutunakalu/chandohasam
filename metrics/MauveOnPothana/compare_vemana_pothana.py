"""MAUVE: Vemana vs Vemana, Pothana vs Pothana, Pothana vs Vemana.

All main comparisons run at the SAME n per side (582 = half the deduped
Vemana corpus), because MAUVE values are only comparable at matched sample
size and bucket count. 5 seeds each; embeddinggemma-300m, Clustering prompt.

Conditions
----------
1. vemana_vs_vemana     : 50/50 split of Vemana. Same-distribution baseline.
2. pothana_vs_pothana   : meter-stratified 50/50 split of Pothana, subsampled
                          to 582/side. Same-distribution baseline at matched n.
3. pothana_vs_vemana    : random 582 Pothana (mixed meters) vs 582 Vemana.
                          Cross-corpus: different author, era, register, AND
                          meter mix (Vemana is ~pure Ataveladi).
4. pothana_A_vs_vemana  : Pothana Ataveladi poems only (313) vs 313 Vemana.
                          Meter-controlled cross-corpus: isolates style/era
                          from meter mix. Smaller n — read against condition 5.
5. vemana_split_313     : Vemana 50/50 split subsampled to 313/side — the
                          same-distribution reference at the n of condition 4.
"""

import json
import random
from pathlib import Path

import numpy as np

from run_mauve_experiment import embed, get_model, mauve_score, stratified_split

HERE = Path(__file__).resolve().parent
SEEDS = [0, 1, 2, 3, 4]
PROMPT = "Clustering"


def subsample(idxs, n, seed):
    rng = random.Random(seed)
    return sorted(rng.sample(list(idxs), n))


def main():
    pothana = json.loads((HERE / "pothana_poems.json").read_text(encoding="utf-8"))
    vemana = json.loads((HERE / "vemana_poems.json").read_text(encoding="utf-8"))
    print(f"pothana: {len(pothana)}  vemana: {len(vemana)}")

    model = get_model()
    emb_p = embed(model, [p["text"] for p in pothana], f"pothana_{PROMPT}", PROMPT)
    emb_v = embed(model, [p["text"] for p in vemana], f"vemana_{PROMPT}", PROMPT)

    n_main = len(vemana) // 2  # 582
    results = {"model": "google/embeddinggemma-300m", "prompt_name": PROMPT,
               "n_main": n_main, "conditions": {}}

    def record(name, scores_ns, note):
        scores = [s for s, _ in scores_ns]
        results["conditions"][name] = {
            "mauve_mean": float(np.mean(scores)),
            "mauve_std": float(np.std(scores)),
            "scores": [float(s) for s in scores],
            "n_per_side": scores_ns[0][1],
            "note": note,
        }
        print(f"{name:22s} MAUVE = {np.mean(scores):.4f} ± {np.std(scores):.4f} "
              f"(n/side={scores_ns[0][1]})  {note}")

    # 1. Vemana vs Vemana split
    sc = []
    for s in SEEDS:
        rng = random.Random(s)
        idxs = list(range(len(vemana)))
        rng.shuffle(idxs)
        a, b = sorted(idxs[:n_main]), sorted(idxs[n_main : 2 * n_main])
        sc.append(mauve_score(emb_v[a], emb_v[b], seed=s))
    record("vemana_vs_vemana", sc, "same-distribution baseline")

    # 2. Pothana vs Pothana split, subsampled to matched n
    sc = []
    for s in SEEDS:
        a, b = stratified_split(pothana, s)
        a, b = subsample(a, n_main, s), subsample(b, n_main, s + 100)
        sc.append(mauve_score(emb_p[a], emb_p[b], seed=s))
    record("pothana_vs_pothana", sc, "same-distribution baseline (matched n)")

    # 3. Pothana (mixed meters) vs Vemana
    sc = []
    for s in SEEDS:
        pa = subsample(range(len(pothana)), n_main, s)
        va = subsample(range(len(vemana)), n_main, s + 100)
        sc.append(mauve_score(emb_p[pa], emb_v[va], seed=s))
    record("pothana_vs_vemana", sc, "cross-corpus, mixed meters")

    # 4. Pothana Ataveladi only vs Vemana (meter-controlled)
    poth_a = [i for i, p in enumerate(pothana) if p["meter"] == "ఆ."]
    n_small = len(poth_a)  # 313
    sc = []
    for s in SEEDS:
        va = subsample(range(len(vemana)), n_small, s)
        sc.append(mauve_score(emb_p[poth_a], emb_v[va], seed=s))
    record("pothana_A_vs_vemana", sc, "cross-corpus, both pure Ataveladi")

    # 5. Vemana split at the small n, as reference for condition 4
    sc = []
    for s in SEEDS:
        rng = random.Random(s)
        idxs = list(range(len(vemana)))
        rng.shuffle(idxs)
        a, b = sorted(idxs[:n_small]), sorted(idxs[n_small : 2 * n_small])
        sc.append(mauve_score(emb_v[a], emb_v[b], seed=s))
    record("vemana_split_313", sc, "same-distribution reference at small n")

    out = HERE / "results_vemana.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()

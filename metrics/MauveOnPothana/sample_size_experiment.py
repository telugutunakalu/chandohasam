"""How many poems per side does MAUVE need?

Sweeps n/side over {25, 50, 100, 200, 400, 800, 1600} for four conditions,
reusing the cached EmbeddingGemma vectors:

  split         : held-out Pothana vs Pothana  (true answer: same ~ 1)
  line_shuffle  : Pothana vs line-shuffled     (subtlest real degradation)
  word_shuffle  : Pothana vs word-shuffled     (moderate degradation)
  vs_vemana     : Pothana vs Vemana            (true answer: different ~ 0)

8 seeds per cell. MAUVE uses num_buckets='auto' (= n/10), so small n also
means few clusters — the finite-sample penalty pushes even same-distribution
scores below 1. The usable minimum is the n where split stays high, vs_vemana
stays low, and the two are separated by a wide, seed-stable margin.
"""

import json
import random
from pathlib import Path

import numpy as np

from run_mauve_experiment import mauve_score, stratified_split

HERE = Path(__file__).resolve().parent
NS = [25, 50, 100, 200, 400, 800, 1600]
SEEDS = list(range(8))
PROMPT = "Clustering"


def main():
    poems = json.loads((HERE / "pothana_poems.json").read_text(encoding="utf-8"))
    emb = np.load(HERE / "embeddings_cache" / f"pothana_{PROMPT}.npy")
    emb_l = np.load(HERE / "embeddings_cache" / f"line_shuffled_{PROMPT}.npy")
    emb_w = np.load(HERE / "embeddings_cache" / f"shuffled_{PROMPT}.npy")
    emb_v = np.load(HERE / "embeddings_cache" / f"vemana_{PROMPT}.npy")

    results = {"seeds": len(SEEDS), "grid": {}}
    print(f"{'n/side':>7} | {'split':>15} | {'line_shuffle':>15} | "
          f"{'word_shuffle':>15} | {'vs_vemana':>15}")

    for n in NS:
        cells = {}
        for cond in ["split", "line_shuffle", "word_shuffle", "vs_vemana"]:
            scores = []
            for s in SEEDS:
                a, b = stratified_split(poems, s)
                rng = random.Random(1000 * s + n)
                ai = sorted(rng.sample(a, n))
                if cond == "split":
                    q = emb[sorted(rng.sample(b, n))]
                elif cond == "line_shuffle":
                    q = emb_l[sorted(rng.sample(b, n))]
                elif cond == "word_shuffle":
                    q = emb_w[sorted(rng.sample(b, n))]
                else:
                    nv = min(n, len(emb_v))
                    ai = ai[:nv]
                    q = emb_v[sorted(rng.sample(range(len(emb_v)), nv))]
                scores.append(mauve_score(emb[ai], q, seed=s)[0])
            cells[cond] = {"mean": float(np.mean(scores)),
                           "std": float(np.std(scores))}
        results["grid"][n] = cells
        print(f"{n:>7} | " + " | ".join(
            f"{cells[c]['mean']:.3f} ± {cells[c]['std']:.3f}"
            for c in ["split", "line_shuffle", "word_shuffle", "vs_vemana"]))

    # simple separation stats
    print("\nGate margin (split − vs_vemana), and split−line_shuffle in σ units:")
    for n in NS:
        g = results["grid"][n]
        margin = g["split"]["mean"] - g["vs_vemana"]["mean"]
        pooled = (g["split"]["std"] ** 2 + g["line_shuffle"]["std"] ** 2) ** 0.5
        dsep = (g["split"]["mean"] - g["line_shuffle"]["mean"]) / max(pooled, 1e-9)
        results["grid"][n]["gate_margin"] = float(margin)
        results["grid"][n]["line_shuffle_sep_sigma"] = float(dsep)
        print(f"  n={n:<5} gate margin = {margin:.3f}   "
              f"line-shuffle separation = {dsep:.1f}σ")

    out = HERE / "results_sample_size.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()

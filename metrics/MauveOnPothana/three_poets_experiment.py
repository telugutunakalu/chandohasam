"""Three poets, two feature spaces: Pothana × Kuchimanchi Timmakavi × Vemana.

The three corpora triangulate register and era:
  Pothana (15th c.)      — Sanskritized bhakti epic (mixed meters)
  Kuchimanchi (18th c.)  — Sanskritized satakam vrittas (classical register)
  Vemana (17th c.?)      — plain-spoken aphoristic Ataveladi (folk register)

For BOTH feature spaces — EmbeddingGemma (768-d, opaque) and the
aksharatensor (33-d, interpretable orthography from aksharanusarika) — we run
the full MAUVE matrix at matched n/side = 582: each corpus's own 50/50 split
(diagonal, expect ~1) and all three pairwise crosses. Plus a 3-way logistic
regression on aksharatensors (5-fold CV) with per-pair accuracies and a
confusion matrix.

Prediction worth testing: Pothana–Kuchimanchi (same register, different
author/era) should sit far above Pothana–Vemana ≈ Kuchimanchi–Vemana
(register gap) — if it doesn't, MAUVE separates *authors*, not registers.
"""

import json
import random
from pathlib import Path

import numpy as np

from aksharatensor_experiment import FEATURE_NAMES, poem_vector, zscore
from run_mauve_experiment import embed, get_model, mauve_score

HERE = Path(__file__).resolve().parent
SEEDS = [0, 1, 2, 3, 4]
PROMPT = "Clustering"
N_MAIN = 582

POETS = ["pothana", "kuchimanchi", "vemana"]


def load_corpora():
    return {
        name: json.loads((HERE / f"{name}_poems.json").read_text(encoding="utf-8"))
        for name in POETS
    }


def split_score(feats, seed, n):
    rng = random.Random(seed)
    idx = list(range(len(feats)))
    rng.shuffle(idx)
    return mauve_score(feats[sorted(idx[:n])], feats[sorted(idx[n : 2 * n])], seed=seed)


def cross_score(fa, fb, seed, n):
    rng = np.random.default_rng(seed)
    a = fa[rng.choice(len(fa), n, replace=False)]
    b = fb[rng.choice(len(fb), n, replace=False)]
    return mauve_score(a, b, seed=seed)


def mauve_matrix(feats_by_poet, label):
    print(f"\n=== MAUVE matrix — {label} (n/side={N_MAIN}, 5 seeds) ===")
    out = {}
    for i, a in enumerate(POETS):
        for b in POETS[i:]:
            if a == b:
                sc = [split_score(feats_by_poet[a], s, N_MAIN) for s in SEEDS]
            else:
                sc = [cross_score(feats_by_poet[a], feats_by_poet[b], s, N_MAIN)
                      for s in SEEDS]
            scores = [s for s, _ in sc]
            out[f"{a}~{b}"] = {"mean": float(np.mean(scores)),
                               "std": float(np.std(scores))}
            print(f"  {a:12s} ~ {b:12s} MAUVE = {np.mean(scores):.4f} "
                  f"± {np.std(scores):.4f}")
    return out


def classification(X_by_poet):
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import confusion_matrix
    from sklearn.model_selection import StratifiedKFold, cross_val_predict
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    X = np.vstack([X_by_poet[p] for p in POETS])
    y = np.concatenate([[i] * len(X_by_poet[p]) for i, p in enumerate(POETS)])
    clf = make_pipeline(StandardScaler(),
                        LogisticRegression(max_iter=3000, C=1.0))
    cv = StratifiedKFold(5, shuffle=True, random_state=0)
    pred = cross_val_predict(clf, X, y, cv=cv)
    acc = float((pred == y).mean())
    cm = confusion_matrix(y, pred)
    print(f"\n=== 3-way classification, aksharatensor (33-d, LR, 5-fold) ===")
    print(f"  overall accuracy: {acc:.4f}")
    print(f"  confusion (rows=true {POETS}):\n{cm}")
    per_pair = {}
    for i, a in enumerate(POETS):
        for j, b in enumerate(POETS):
            if i < j:
                mask = (y == i) | (y == j)
                pa = float((pred[mask] == y[mask]).mean())
                per_pair[f"{a}~{b}"] = pa
                print(f"  {a} vs {b}: pairwise row accuracy = {pa:.4f}")
    return {"accuracy": acc, "confusion": cm.tolist(),
            "labels": POETS, "pairwise_row_accuracy": per_pair}


def main():
    corpora = load_corpora()
    for p in POETS:
        print(f"{p}: {len(corpora[p])} poems")

    # ---- EmbeddingGemma features (cached where possible) ----
    model = get_model()
    gemma = {
        p: embed(model, [x["text"] for x in corpora[p]], f"{p}_{PROMPT}", PROMPT)
        for p in POETS
    }

    # ---- aksharatensor features ----
    print("building aksharatensors ...")
    ak_raw = {
        p: np.array([v for x in corpora[p]
                     if (v := poem_vector(x["text"])) is not None])
        for p in POETS
    }
    Z = zscore(np.vstack([ak_raw[p] for p in POETS]))
    ak = {}
    off = 0
    for p in POETS:
        ak[p] = Z[off : off + len(ak_raw[p])]
        off += len(ak_raw[p])

    results = {
        "n_per_side": N_MAIN, "seeds": len(SEEDS),
        "corpus_sizes": {p: len(corpora[p]) for p in POETS},
        "mauve_gemma": mauve_matrix(gemma, "EmbeddingGemma 768-d"),
        "mauve_aksharatensor": mauve_matrix(ak, "aksharatensor 33-d"),
        "classification_aksharatensor": classification(ak_raw),
    }

    out = HERE / "results_three_poets.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()

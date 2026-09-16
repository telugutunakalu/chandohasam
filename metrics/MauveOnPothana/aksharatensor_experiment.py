"""Aksharatensor: interpretable orthographic poem vectors from aksharanusarika.

Instead of EmbeddingGemma's opaque 768 dims, represent each poem by ~30
interpretable dimensions derived from aksharanusarika's categorization of
every akshara (vargam, sthana/articulation place, deergha, samyukta/dvitva,
anusvara, parusha/sarala/sthira, ...), plus guru/laghu prosody and word-shape
statistics. Then ask:

  A. Can a linear classifier identify Pothana vs Vemana from these features
     alone — and which features carry the signal? (5-fold CV, full corpora
     AND meter-controlled: Pothana Ataveladi-only vs Vemana.)
  B. Does MAUVE still behave when run on aksharatensor features instead of
     Gemma embeddings? (pothana split ~1? vemana split ~1? pothana vs
     vemana ~0?)

Uses the downloaded gist aksharanusarika_v0.0.6a.py (verified identical to
the local ~/phd_workspace/aksharanusarika port on 3,256 corpus words):
split_aksharalu, categorize_aksharam, akshara_ganavibhajana.
"""

import importlib.util
import json
import random
from pathlib import Path

import numpy as np

_spec = importlib.util.spec_from_file_location(
    "aksharanusarika_v006a",
    Path(__file__).resolve().parent.parent / "aksharanusarika_v0.0.6a.py",
)
_ak = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ak)
split_aksharalu = _ak.split_aksharalu
categorize_aksharam = _ak.categorize_aksharam
akshara_ganavibhajana = _ak.akshara_ganavibhajana

HERE = Path(__file__).resolve().parent
SEEDS = [0, 1, 2, 3, 4]

CATEGORIES = [
    "అచ్చు", "హల్లు", "దీర్ఘ", "హ్రస్వాక్షరం", "అనుస్వారం", "విసర్గ అక్షరం",
    "సంయుక్తాక్షరం", "ద్విత్వాక్షరం",
    "సరళములు", "పరుషములు", "స్థిరములు", "ప్లుతములు",
    "క వర్గము", "చ వర్గము", "ట వర్గము", "త వర్గము", "ప వర్గము",
    "స్పర్శములు", "ఊష్మాలు", "అంతస్తములు", "అనునాసికములు",
    "కంఠ్యములు", "తాలవ్యములు", "మూర్ధన్యములు", "దంత్యములు", "ఓష్ఠ్యములు",
    "కంఠతాలవ్యములు", "కంఠోష్ఠ్యములు", "దంత్యోష్ఠ్యములు",
]
EXTRA = ["guru_fraction", "mean_word_len_aksharas", "max_word_len_aksharas",
         "mean_line_len_aksharas"]
FEATURE_NAMES = CATEGORIES + EXTRA


def poem_vector(text):
    """One interpretable vector per poem: category fractions + prosody + word shape."""
    cat_counts = np.zeros(len(CATEGORIES))
    n_aksharas = 0
    guru = 0
    marked = 0
    word_lens = []
    line_lens = []
    for line in text.split("\n"):
        line_aksharas = []
        for word in line.split():
            aks = [a for a in split_aksharalu(word) if a.strip()]
            if not aks:
                continue
            word_lens.append(len(aks))
            line_aksharas.extend(aks)
            for a in aks:
                n_aksharas += 1
                tags = set(categorize_aksharam(a))
                for j, c in enumerate(CATEGORIES):
                    if c in tags:
                        cat_counts[j] += 1
        if line_aksharas:
            line_lens.append(len(line_aksharas))
            for m in akshara_ganavibhajana(line_aksharas):
                if m:
                    marked += 1
                    guru += m == "U"
    if n_aksharas == 0:
        return None
    return np.concatenate([
        cat_counts / n_aksharas,
        [guru / max(marked, 1), float(np.mean(word_lens)),
         float(np.max(word_lens)), float(np.mean(line_lens))],
    ])


def zscore(X):
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1.0
    return (X - mu) / sd


def mauve_feat(p, q, seed):
    import mauve
    n = min(len(p), len(q))
    rng = np.random.default_rng(seed)
    a = p[rng.choice(len(p), n, replace=False)]
    b = q[rng.choice(len(q), n, replace=False)]
    return mauve.compute_mauve(p_features=a, q_features=b, seed=seed,
                               verbose=False).mauve, n


def crossval_lr(X, y, seeds=SEEDS):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, cross_val_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    accs = []
    for s in seeds:
        clf = make_pipeline(StandardScaler(),
                            LogisticRegression(max_iter=2000, C=1.0))
        cv = StratifiedKFold(5, shuffle=True, random_state=s)
        accs.extend(cross_val_score(clf, X, y, cv=cv, scoring="accuracy"))
    # fit once on all data for coefficients
    clf = make_pipeline(StandardScaler(),
                        LogisticRegression(max_iter=2000, C=1.0)).fit(X, y)
    coefs = clf[-1].coef_[0]
    return float(np.mean(accs)), float(np.std(accs)), coefs


def main():
    pothana = json.loads((HERE / "pothana_poems.json").read_text(encoding="utf-8"))
    vemana = json.loads((HERE / "vemana_poems.json").read_text(encoding="utf-8"))

    print("building aksharatensors ...")
    Xp = np.array([v for p in pothana if (v := poem_vector(p["text"])) is not None])
    Xv = np.array([v for p in vemana if (v := poem_vector(p["text"])) is not None])
    print(f"pothana {Xp.shape}, vemana {Xv.shape}, dims={len(FEATURE_NAMES)}")

    results = {"features": FEATURE_NAMES, "n_dims": len(FEATURE_NAMES),
               "classification": {}, "mauve": {}}

    # ---------- A. classification ----------
    X = np.vstack([Xp, Xv])
    y = np.array([0] * len(Xp) + [1] * len(Xv))
    acc, sd, coefs = crossval_lr(X, y)
    order = np.argsort(-np.abs(coefs))
    top = [(FEATURE_NAMES[i], round(float(coefs[i]), 3)) for i in order[:10]]
    results["classification"]["full"] = {
        "accuracy_mean": acc, "accuracy_std": sd, "n": [len(Xp), len(Xv)],
        "top_features_toward_vemana_positive": top,
    }
    print(f"\nA1  Pothana vs Vemana (full):        acc = {acc:.4f} ± {sd:.4f}")
    print("    top features (+ → Vemana):", top)

    # meter-controlled: Pothana Ataveladi vs equal-sized Vemana sample
    ata_idx = [i for i, p in enumerate(pothana) if p["meter"] == "ఆ."]
    Xpa = Xp[ata_idx]
    rng = random.Random(0)
    vs = sorted(rng.sample(range(len(Xv)), len(Xpa)))
    Xc = np.vstack([Xpa, Xv[vs]])
    yc = np.array([0] * len(Xpa) + [1] * len(Xpa))
    acc2, sd2, coefs2 = crossval_lr(Xc, yc)
    order2 = np.argsort(-np.abs(coefs2))
    top2 = [(FEATURE_NAMES[i], round(float(coefs2[i]), 3)) for i in order2[:10]]
    results["classification"]["meter_controlled"] = {
        "accuracy_mean": acc2, "accuracy_std": sd2, "n": [len(Xpa), len(Xpa)],
        "top_features_toward_vemana_positive": top2,
    }
    print(f"A2  Pothana ఆ. vs Vemana (both Ataveladi): acc = {acc2:.4f} ± {sd2:.4f}")
    print("    top features (+ → Vemana):", top2)

    # ---------- B. MAUVE on aksharatensor features ----------
    Z = zscore(np.vstack([Xp, Xv]))
    Zp, Zv = Z[: len(Xp)], Z[len(Xp):]
    n_main = len(Xv) // 2

    def record(name, scores_ns):
        scores = [s for s, _ in scores_ns]
        results["mauve"][name] = {
            "mauve_mean": float(np.mean(scores)), "mauve_std": float(np.std(scores)),
            "n_per_side": scores_ns[0][1]}
        print(f"B   {name:24s} MAUVE = {np.mean(scores):.4f} ± {np.std(scores):.4f} "
              f"(n/side={scores_ns[0][1]})")

    sc = []
    for s in SEEDS:
        rng = random.Random(s)
        idx = list(range(len(Zp))); rng.shuffle(idx)
        sc.append(mauve_feat(Zp[sorted(idx[:n_main])], Zp[sorted(idx[n_main:2*n_main])], s))
    record("pothana_split", sc)

    sc = []
    for s in SEEDS:
        rng = random.Random(s)
        idx = list(range(len(Zv))); rng.shuffle(idx)
        sc.append(mauve_feat(Zv[sorted(idx[:n_main])], Zv[sorted(idx[n_main:2*n_main])], s))
    record("vemana_split", sc)

    sc = [mauve_feat(Zp, Zv, s) for s in SEEDS]  # subsampled to n_main inside
    record("pothana_vs_vemana", sc)

    sc = [mauve_feat(Zp[ata_idx], Zv, s) for s in SEEDS]
    record("pothana_A_vs_vemana", sc)

    out = HERE / "results_aksharatensor.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()

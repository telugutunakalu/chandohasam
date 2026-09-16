"""Two ablations that decide what the aksharatensor result actually shows.

1. MAKUTA CONFOUND — Vemana ends every poem with a fixed refrain
   («విశ్వదాభిరామ వినర వేమ»), Kuchimanchi's satakams likewise
   («...పార్వతీవల్లభా!» / «...కుక్కుటేశ!»). A classifier could ride on the
   refrain alone. Ablation: drop the FINAL LINE of every poem in all three
   corpora and re-run the 3-way + pairwise classification.

2. CHAR N-GRAM BASELINE — authorship attribution via character n-grams is
   the standard stylometry baseline. If tf-idf char 2–4-grams beat the
   33-d aksharatensor, the contribution is interpretability, not accuracy —
   which must be claimed honestly.

Both run on the same 5-fold CV protocol as before.
"""

import json
from pathlib import Path

import numpy as np

from aksharatensor_experiment import poem_vector

HERE = Path(__file__).resolve().parent
POETS = ["pothana", "kuchimanchi", "vemana"]


def load(drop_last_line=False):
    texts, labels = [], []
    for i, p in enumerate(POETS):
        for x in json.loads((HERE / f"{p}_poems.json").read_text(encoding="utf-8")):
            lines = x["text"].split("\n")
            if drop_last_line:
                lines = lines[:-1]
            if lines:
                texts.append("\n".join(lines))
                labels.append(i)
    return texts, np.array(labels)


def eval_clf(X, y, name):
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import confusion_matrix
    from sklearn.model_selection import StratifiedKFold, cross_val_predict
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    clf = make_pipeline(StandardScaler(with_mean=not hasattr(X, "tocsr")),
                        LogisticRegression(max_iter=3000))
    pred = cross_val_predict(clf, X, y,
                             cv=StratifiedKFold(5, shuffle=True, random_state=0))
    acc = float((pred == y).mean())
    cm = confusion_matrix(y, pred)
    print(f"{name:44s} acc = {acc:.4f}")
    pair = {}
    for i in range(3):
        for j in range(i + 1, 3):
            m = (y == i) | (y == j)
            pair[f"{POETS[i]}~{POETS[j]}"] = float((pred[m] == y[m]).mean())
    return {"accuracy": acc, "confusion": cm.tolist(), "pairwise_row_acc": pair}


def aksharatensor_X(texts):
    return np.array([v if (v := poem_vector(t)) is not None else np.zeros(33)
                     for t in texts])


def ngram_X(texts):
    from sklearn.feature_extraction.text import TfidfVectorizer
    return TfidfVectorizer(analyzer="char", ngram_range=(2, 4),
                           max_features=20000, sublinear_tf=True
                           ).fit_transform(texts)


def main():
    results = {}
    for drop in [False, True]:
        tag = "makuta_stripped" if drop else "full_poems"
        texts, y = load(drop_last_line=drop)
        print(f"\n--- {tag} ({len(texts)} poems) ---")
        results[f"aksharatensor_{tag}"] = eval_clf(
            aksharatensor_X(texts), y, f"aksharatensor 33-d [{tag}]")
        results[f"char_ngram_{tag}"] = eval_clf(
            ngram_X(texts), y, f"char 2-4-gram tf-idf 20k [{tag}]")

    for k, v in results.items():
        print(f"{k:36s} acc={v['accuracy']:.4f}  pairwise={ {p: round(a,3) for p,a in v['pairwise_row_acc'].items()} }")

    (HERE / "results_ablations.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")
    print("\nWrote results_ablations.json")


if __name__ == "__main__":
    main()

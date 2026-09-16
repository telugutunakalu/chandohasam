"""Does Gemma + aksharatensor beat either alone for poet stylometry?

Feature sets, each under the same LR 5-fold CV, on full AND makuta-stripped
poems (stripped texts are re-embedded, so the control is real):

  gemma            768-d EmbeddingGemma
  aksharatensor    33-d interpretable orthography
  gemma+akshara    801-d concatenation (both z-scored)
  char_ngram       tf-idf char 2-4-grams (reference ceiling)

The delta (gemma+akshara − gemma) measures what orthographic features add
ON TOP of the embedding; (gemma − aksharatensor) measures the accuracy gap
interpretability currently costs.
"""

import json
from pathlib import Path

import numpy as np

from aksharatensor_experiment import poem_vector, zscore
from run_mauve_experiment import embed, get_model

HERE = Path(__file__).resolve().parent
POETS = ["pothana", "kuchimanchi", "vemana"]
PROMPT = "Clustering"


def load(drop_last_line):
    texts, y = [], []
    for i, p in enumerate(POETS):
        for x in json.loads((HERE / f"{p}_poems.json").read_text(encoding="utf-8")):
            lines = x["text"].split("\n")
            if drop_last_line:
                lines = lines[:-1]
            if lines:
                texts.append("\n".join(lines))
                y.append(i)
    return texts, np.array(y)


def eval_clf(X, y, name, results):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, cross_val_predict
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    sparse = hasattr(X, "tocsr")
    clf = make_pipeline(StandardScaler(with_mean=not sparse),
                        LogisticRegression(max_iter=3000))
    pred = cross_val_predict(clf, X, y,
                             cv=StratifiedKFold(5, shuffle=True, random_state=0))
    acc = float((pred == y).mean())
    pair = {}
    for i in range(3):
        for j in range(i + 1, 3):
            m = (y == i) | (y == j)
            pair[f"{POETS[i][:4]}~{POETS[j][:4]}"] = round(float((pred[m] == y[m]).mean()), 4)
    results[name] = {"accuracy": acc, "pairwise": pair}
    print(f"  {name:22s} acc = {acc:.4f}   {pair}")


def main():
    from sklearn.feature_extraction.text import TfidfVectorizer

    model = get_model()
    results = {}
    for drop in [False, True]:
        tag = "stripped" if drop else "full"
        texts, y = load(drop)
        print(f"\n--- {tag} ({len(texts)} poems) ---")

        G = embed(model, texts, f"three_poets_{tag}_{PROMPT}", PROMPT)
        A = np.array([v if (v := poem_vector(t)) is not None else np.zeros(33)
                      for t in texts])
        GA = np.hstack([zscore(G), zscore(A)])
        N = TfidfVectorizer(analyzer="char", ngram_range=(2, 4),
                            max_features=20000, sublinear_tf=True).fit_transform(texts)

        res = {}
        eval_clf(G, y, "gemma", res)
        eval_clf(A, y, "aksharatensor", res)
        eval_clf(GA, y, "gemma+aksharatensor", res)
        eval_clf(N, y, "char_ngram", res)
        results[tag] = res

    (HERE / "results_hybrid.json").write_text(json.dumps(results, indent=2),
                                              encoding="utf-8")
    print("\nWrote results_hybrid.json")


if __name__ == "__main__":
    main()

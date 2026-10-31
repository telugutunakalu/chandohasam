"""Scores study 2's 99 poems with the final Coherence/Adherence models refit on all 310 study-1
rows -- a genuine out-of-sample test, since study 2's generation paradigm (bhavam-reconstruction
by small fine-tuned models under a hard metrical constraint) is nothing like study 1's. Needs
embed.py's study1_rated_* and study2_* caches. Writes results/study2_scores.csv.

    python3 score_study2.py
"""
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from sc_common import BACKBONES, CACHE_DIR, DATA_DIR, RESULTS_DIR, load_study2_pool

C = 0.003


def expected_value(model, X):
    return model.predict_proba(X) @ model.classes_


pooled = pd.read_csv(DATA_DIR / "pooled_study1.csv")
train_ids = sorted(set(pooled["eval_id"]))
train_idx = {e: i for i, e in enumerate(train_ids)}
row_idx = pooled["eval_id"].map(train_idx).to_numpy()
y_int = pooled["bhavam"].to_numpy(dtype=int)

s2_pool = load_study2_pool()
s2_ids = list(s2_pool)
print(f"{len(s2_ids)} study-2 poems, models: "
      f"{pd.Series([s2_pool[e]['model'] for e in s2_ids]).value_counts().to_dict()}", flush=True)

out_rows = {e: dict(eval_id=e, model=s2_pool[e]["model"], gold_eval_id=s2_pool[e]["gold_eval_id"]) for e in s2_ids}

for name in BACKBONES:
    print(f"=== {name} ===", flush=True)
    train_poem = np.load(CACHE_DIR / f"study1_rated_{name}_poem.npy")
    train_bhavam = np.load(CACHE_DIR / f"study1_rated_{name}_bhavam.npy")
    s2_poem = np.load(CACHE_DIR / f"study2_{name}_poem.npy")
    s2_bhavam = np.load(CACHE_DIR / f"study2_{name}_bhavam.npy")

    X_coh = train_poem[row_idx]
    sc_coh = StandardScaler().fit(X_coh)
    coh_model = LogisticRegression(C=C, max_iter=2000).fit(sc_coh.transform(X_coh), y_int)
    coh_pred = np.clip(expected_value(coh_model, sc_coh.transform(s2_poem)), 1, 5)

    X_adh = (train_poem * train_bhavam)[row_idx]
    sc_adh = StandardScaler().fit(X_adh)
    adh_model = LogisticRegression(C=C, max_iter=2000).fit(sc_adh.transform(X_adh), y_int)
    adh_pred = np.clip(expected_value(adh_model, sc_adh.transform(s2_poem * s2_bhavam)), 1, 5)

    for i, e in enumerate(s2_ids):
        out_rows[e][f"coherence_{name}"] = float(coh_pred[i])
        out_rows[e][f"adherence_{name}"] = float(adh_pred[i])

out = pd.DataFrame(list(out_rows.values()))
out.to_csv(RESULTS_DIR / "study2_scores.csv", index=False)
print(f"wrote {RESULTS_DIR / 'study2_scores.csv'}")
print("\nDONE")

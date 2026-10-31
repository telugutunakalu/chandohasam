"""Refits the final Coherence and Adherence models on all 310 pooled (study-1, group-A) rows, and
scores every poem of the study-1 pool: the 116 rated and the 384 unrated (held out of annotation).
Needs embed.py's study1_rated_* and study1_unrated_* caches.

Coherence: poem embedding -> multinomial Logistic Regression (C=0.003), expected-value scoring.
Adherence: elementwise product (poem_emb * bhavam_emb) -> the same model. One poem (he_0096) has no
Telugu bhavam text and is excluded from Adherence only.

Writes results/coherence_per_poem.csv (rated + unrated, one table) and
results/adherence_per_poem.csv (rated + unrated with bhavam text, one table).

    python3 final_models.py
"""
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from sc_common import BACKBONES, CACHE_DIR, DATA_DIR, RESULTS_DIR, load_poem_pool

C = 0.003


def expected_value(model, X):
    return model.predict_proba(X) @ model.classes_


pooled = pd.read_csv(DATA_DIR / "pooled_study1.csv")
rated_ids = sorted(set(pooled["eval_id"]))
rated_idx = {e: i for i, e in enumerate(rated_ids)}
row_idx = pooled["eval_id"].map(rated_idx).to_numpy()
y_int = pooled["bhavam"].to_numpy(dtype=int)

pool = load_poem_pool()
unrated_ids = sorted(e for e in pool if e not in rated_idx)
print(f"{len(rated_ids)} rated poems, {len(unrated_ids)} unrated poems", flush=True)

coh_rows = {e: dict(eval_id=e, source_dataset=pool[e]["source_dataset"], rated=(e in rated_idx)) for e in pool}
adh_rows = {e: dict(eval_id=e, source_dataset=pool[e]["source_dataset"], rated=(e in rated_idx)) for e in pool
            if pool[e]["bhavam_text"].strip()}
print(f"{len(adh_rows)}/{len(pool)} poems have bhavam text (Adherence computable)", flush=True)

for name in BACKBONES:
    print(f"=== {name} ===", flush=True)
    rated_poem = np.load(CACHE_DIR / f"study1_rated_{name}_poem.npy")
    rated_bhavam = np.load(CACHE_DIR / f"study1_rated_{name}_bhavam.npy")
    unrated_poem = np.load(CACHE_DIR / f"study1_unrated_{name}_poem.npy")
    unrated_bhavam = np.load(CACHE_DIR / f"study1_unrated_{name}_bhavam.npy")

    # ---- Coherence: poem embedding only ----
    X_coh = rated_poem[row_idx]
    sc_coh = StandardScaler().fit(X_coh)
    coh_model = LogisticRegression(C=C, max_iter=2000).fit(sc_coh.transform(X_coh), y_int)
    for i, e in enumerate(rated_ids):
        coh_rows[e][f"coherence_{name}"] = float(np.clip(expected_value(coh_model, sc_coh.transform(rated_poem[i:i + 1])), 1, 5)[0])
    coh_pred_unrated = np.clip(expected_value(coh_model, sc_coh.transform(unrated_poem)), 1, 5)
    for i, e in enumerate(unrated_ids):
        coh_rows[e][f"coherence_{name}"] = float(coh_pred_unrated[i])

    # ---- Adherence: elementwise product of poem and bhavam embeddings ----
    X_adh = (rated_poem * rated_bhavam)[row_idx]
    sc_adh = StandardScaler().fit(X_adh)
    adh_model = LogisticRegression(C=C, max_iter=2000).fit(sc_adh.transform(X_adh), y_int)
    for i, e in enumerate(rated_ids):
        if e in adh_rows:
            prod = (rated_poem[i:i + 1] * rated_bhavam[i:i + 1])
            adh_rows[e][f"adherence_{name}"] = float(np.clip(expected_value(adh_model, sc_adh.transform(prod)), 1, 5)[0])
    unrated_prod = unrated_poem * unrated_bhavam
    adh_pred_unrated = np.clip(expected_value(adh_model, sc_adh.transform(unrated_prod)), 1, 5)
    for i, e in enumerate(unrated_ids):
        if e in adh_rows:
            adh_rows[e][f"adherence_{name}"] = float(adh_pred_unrated[i])

coh_df = pd.DataFrame(list(coh_rows.values()))
adh_df = pd.DataFrame(list(adh_rows.values()))
coh_df.to_csv(RESULTS_DIR / "coherence_per_poem.csv", index=False)
adh_df.to_csv(RESULTS_DIR / "adherence_per_poem.csv", index=False)
print(f"wrote {RESULTS_DIR / 'coherence_per_poem.csv'} ({len(coh_df)} rows)")
print(f"wrote {RESULTS_DIR / 'adherence_per_poem.csv'} ({len(adh_df)} rows)")
print("\nDONE")

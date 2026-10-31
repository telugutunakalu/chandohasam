"""Ablation: how Coherence and Adherence were chosen.

Coherence: Ridge regression vs. multinomial Logistic Regression vs. Ordinal Logistic (proportional
odds, PCA-reduced), on the poem embedding alone.
Adherence: cosine similarity (a single scalar) + Linear/Logistic, vs. the elementwise product
poem*bhavam ("learned similarity", a per-dimension-weighted generalisation of cosine) + Ridge/Logistic.

5-fold stratified CV x 5 seeds, out-of-fold predictions, Pearson r / Spearman rho / MAE.
Needs embed.py's study1_rated_* cache. Writes results/coherence_model_comparison.csv,
results/adherence_model_comparison.csv.

    python3 modeling_comparison.py
"""
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from statsmodels.miscmodels.ordinal_model import OrderedModel

from sc_common import BACKBONES, CACHE_DIR, DATA_DIR, RESULTS_DIR

N_SPLITS, SEEDS = 5, [0, 1, 2, 3, 4]


def corr_metrics(y, preds):
    return dict(pearson=pearsonr(y, preds)[0], spearman=spearmanr(y, preds).correlation,
                mae=float(np.mean(np.abs(y - preds))))


def cv_ridge(X, y, strata, alpha=300.0):
    all_preds = []
    for seed in SEEDS:
        skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
        preds = np.zeros(len(y), dtype=float)
        for tr, te in skf.split(X, strata):
            sc = StandardScaler().fit(X[tr])
            m = Ridge(alpha=alpha).fit(sc.transform(X[tr]), y[tr])
            preds[te] = m.predict(sc.transform(X[te]))
        all_preds.append(preds)
    return corr_metrics(y, np.mean(all_preds, axis=0))


def cv_logistic(X, y_int, strata, C=0.003):
    """Multinomial logistic regression; continuous score = E[class | x] = sum_k k * P(y=k|x)."""
    all_preds = []
    for seed in SEEDS:
        skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
        preds = np.zeros(len(y_int), dtype=float)
        for tr, te in skf.split(X, strata):
            sc = StandardScaler().fit(X[tr])
            m = LogisticRegression(C=C, max_iter=2000).fit(sc.transform(X[tr]), y_int[tr])
            proba = m.predict_proba(sc.transform(X[te]))
            preds[te] = proba @ m.classes_
        all_preds.append(preds)
    return corr_metrics(y_int.astype(float), np.mean(all_preds, axis=0))


def cv_ordinal(X, y_int, strata, n_components=12):
    """Ordinal logistic (proportional odds). PCA-reduce first: OrderedModel has no built-in
    regularisation and 768-dim raw features are numerically unusable at N~300."""
    from sklearn.decomposition import PCA
    all_preds = []
    for seed in SEEDS:
        skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
        preds = np.zeros(len(y_int), dtype=float)
        for tr, te in skf.split(X, strata):
            sc = StandardScaler().fit(X[tr])
            Xtr_s, Xte_s = sc.transform(X[tr]), sc.transform(X[te])
            pca = PCA(n_components=min(n_components, len(tr) - 1), random_state=0).fit(Xtr_s)
            Xtr_p, Xte_p = pca.transform(Xtr_s), pca.transform(Xte_s)
            try:
                res = OrderedModel(y_int[tr], Xtr_p, distr="logit").fit(method="lbfgs", disp=False, maxiter=200)
                preds[te] = Xte_p @ res.params[:Xte_p.shape[1]]
            except Exception:
                preds[te] = np.nan
        all_preds.append(preds)
    all_preds = np.array(all_preds)
    valid = ~np.isnan(all_preds).any(axis=0)
    return corr_metrics(y_int[valid].astype(float), np.mean(all_preds[:, valid], axis=0))


def cv_linear_1feat(x, y, strata):
    X = x.reshape(-1, 1)
    all_preds = []
    for seed in SEEDS:
        skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
        preds = np.zeros(len(y), dtype=float)
        for tr, te in skf.split(X, strata):
            m = LinearRegression().fit(X[tr], y[tr])
            preds[te] = m.predict(X[te])
        all_preds.append(preds)
    return corr_metrics(y, np.mean(all_preds, axis=0))


def cv_logistic_1feat(x, y_int, strata, C=1.0):
    X = x.reshape(-1, 1)
    all_preds = []
    for seed in SEEDS:
        skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
        preds = np.zeros(len(y_int), dtype=float)
        for tr, te in skf.split(X, strata):
            sc = StandardScaler().fit(X[tr])
            m = LogisticRegression(C=C, max_iter=2000).fit(sc.transform(X[tr]), y_int[tr])
            proba = m.predict_proba(sc.transform(X[te]))
            preds[te] = proba @ m.classes_
        all_preds.append(preds)
    return corr_metrics(y_int.astype(float), np.mean(all_preds, axis=0))


def cosine_sim(a, b):
    a_n = a / np.linalg.norm(a, axis=1, keepdims=True)
    b_n = b / np.linalg.norm(b, axis=1, keepdims=True)
    return (a_n * b_n).sum(axis=1)


# ---------------------------------------------------------------- data
pooled = pd.read_csv(DATA_DIR / "pooled_study1.csv")
unique_poems = pooled.drop_duplicates("eval_id")[["eval_id"]].reset_index(drop=True)
eval_id_to_idx = {e: i for i, e in enumerate(unique_poems["eval_id"])}
row_idx = pooled["eval_id"].map(eval_id_to_idx).to_numpy()

y_full = pooled["bhavam"].to_numpy(dtype=float)
y_full_int = pooled["bhavam"].to_numpy(dtype=int)
strata_full = pooled["bhavam"].to_numpy()

coherence_rows, adherence_rows = [], []
for name in BACKBONES:
    print(f"=== {name} ===", flush=True)
    poem_emb = np.load(CACHE_DIR / f"study1_rated_{name}_poem.npy")
    bhavam_emb = np.load(CACHE_DIR / f"study1_rated_{name}_bhavam.npy")
    X_poem = poem_emb[row_idx]

    ridge = cv_ridge(X_poem, y_full, strata_full)
    logistic = cv_logistic(X_poem, y_full_int, strata_full)
    ordinal = cv_ordinal(X_poem, y_full_int, strata_full)
    print(f"  Coherence Ridge:    {ridge}", flush=True)
    print(f"  Coherence Logistic: {logistic}", flush=True)
    print(f"  Coherence Ordinal:  {ordinal}", flush=True)
    coherence_rows += [dict(backbone=name, model="ridge", **ridge),
                        dict(backbone=name, model="logistic", **logistic),
                        dict(backbone=name, model="ordinal_logistic", **ordinal)]

    sim = cosine_sim(poem_emb, bhavam_emb)[row_idx]
    cos_linear = cv_linear_1feat(sim, y_full, strata_full)
    cos_logistic = cv_logistic_1feat(sim, y_full_int, strata_full)

    prod_feat = (poem_emb * bhavam_emb)[row_idx]  # elementwise product = learnable weighted dot product
    learned_ridge = cv_ridge(prod_feat, y_full, strata_full, alpha=300.0)
    learned_logistic = cv_logistic(prod_feat, y_full_int, strata_full, C=0.003)

    print(f"  Adherence cosine+Linear:      {cos_linear}", flush=True)
    print(f"  Adherence cosine+Logistic:    {cos_logistic}", flush=True)
    print(f"  Adherence learned-sim+Ridge:  {learned_ridge}", flush=True)
    print(f"  Adherence learned-sim+Logit:  {learned_logistic}", flush=True)
    adherence_rows += [dict(backbone=name, model="cosine_linear", **cos_linear),
                        dict(backbone=name, model="cosine_logistic", **cos_logistic),
                        dict(backbone=name, model="learned_sim_ridge", **learned_ridge),
                        dict(backbone=name, model="learned_sim_logistic", **learned_logistic)]

coh_df = pd.DataFrame(coherence_rows)
adh_df = pd.DataFrame(adherence_rows)
coh_df.to_csv(RESULTS_DIR / "coherence_model_comparison.csv", index=False)
adh_df.to_csv(RESULTS_DIR / "adherence_model_comparison.csv", index=False)
print("\nDONE")

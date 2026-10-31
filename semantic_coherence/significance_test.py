"""Statistical significance for the Coherence/Adherence CV results: raw per-coefficient p-values
aren't valid here (768 features, 310 rows, L2-regularised), so this computes the two legitimate
alternatives instead: a bootstrap 95% CI on Pearson r (resample (y, pred) pairs, 2000x) and a
permutation-test p-value (shuffle the labels, refit + 5-fold CV, 1000x; p = how often a shuffled
model beats the real one). Needs embed.py's study1_rated_* cache. Writes results/significance_tests.csv.

    python3 significance_test.py
"""
import warnings
warnings.filterwarnings("ignore")

import time

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

from sc_common import BACKBONES, CACHE_DIR, DATA_DIR, RESULTS_DIR

N_SPLITS, SEEDS = 5, [0, 1, 2, 3, 4]
C = 0.003
N_PERM = 1000
N_BOOT = 2000
RNG = np.random.default_rng(0)


def expected_value(model, X):
    return model.predict_proba(X) @ model.classes_


def cv_predict(X, y, strata, seeds=SEEDS):
    all_preds = []
    for seed in seeds:
        skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
        preds = np.zeros(len(y), dtype=float)
        for tr, te in skf.split(X, strata):
            sc = StandardScaler().fit(X[tr])
            m = LogisticRegression(C=C, max_iter=2000).fit(sc.transform(X[tr]), y[tr])
            preds[te] = expected_value(m, sc.transform(X[te]))
        all_preds.append(preds)
    return np.mean(all_preds, axis=0)


def cv_predict_single_seed(X, y, strata, seed=0):
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
    preds = np.zeros(len(y), dtype=float)
    for tr, te in skf.split(X, strata):
        sc = StandardScaler().fit(X[tr])
        m = LogisticRegression(C=C, max_iter=2000).fit(sc.transform(X[tr]), y[tr])
        preds[te] = expected_value(m, sc.transform(X[te]))
    return preds


def bootstrap_ci(y, preds, n_boot=N_BOOT, rng=RNG):
    n = len(y)
    rs = np.zeros(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        if np.std(y[idx]) == 0 or np.std(preds[idx]) == 0:
            rs[b] = np.nan
            continue
        rs[b] = pearsonr(y[idx], preds[idx])[0]
    rs = rs[~np.isnan(rs)]
    return np.percentile(rs, 2.5), np.percentile(rs, 97.5)


def permutation_pvalue(X, y, strata, observed_r, n_perm=N_PERM, rng=RNG):
    null_rs = np.zeros(n_perm)
    for b in range(n_perm):
        y_perm = rng.permutation(y)
        preds = cv_predict_single_seed(X, y_perm, strata, seed=0)
        null_rs[b] = pearsonr(y_perm, preds)[0]
    p = (np.sum(null_rs >= observed_r) + 1) / (n_perm + 1)
    return p, null_rs


pooled = pd.read_csv(DATA_DIR / "pooled_study1.csv")
unique_poems = pooled.drop_duplicates("eval_id")[["eval_id"]].reset_index(drop=True)
eval_id_to_idx = {e: i for i, e in enumerate(unique_poems["eval_id"])}
row_idx = pooled["eval_id"].map(eval_id_to_idx).to_numpy()
y_full_int = pooled["bhavam"].to_numpy(dtype=int)
strata_full = pooled["bhavam"].to_numpy()

rows = []
for name in BACKBONES:
    t0 = time.time()
    print(f"=== {name} ===", flush=True)
    poem_emb = np.load(CACHE_DIR / f"study1_rated_{name}_poem.npy")
    bhavam_emb = np.load(CACHE_DIR / f"study1_rated_{name}_bhavam.npy")

    for task, X in [("coherence", poem_emb[row_idx]), ("adherence", (poem_emb * bhavam_emb)[row_idx])]:
        preds_5seed = cv_predict(X, y_full_int, strata_full, seeds=SEEDS)
        r_5seed, rho_5seed = pearsonr(y_full_int, preds_5seed)[0], spearmanr(y_full_int, preds_5seed).correlation
        lo, hi = bootstrap_ci(y_full_int.astype(float), preds_5seed)

        preds_1seed = cv_predict_single_seed(X, y_full_int, strata_full, seed=0)
        r_1seed = pearsonr(y_full_int, preds_1seed)[0]
        p_val, null_rs = permutation_pvalue(X, y_full_int, strata_full, r_1seed)

        print(f"  {task}: r={r_5seed:.3f} (95% CI [{lo:.3f}, {hi:.3f}]), rho={rho_5seed:.3f}, "
              f"1-seed r={r_1seed:.3f}, permutation p={p_val:.4f} (null mean={null_rs.mean():.3f}, "
              f"null std={null_rs.std():.3f}), [{time.time()-t0:.0f}s]", flush=True)
        rows.append(dict(backbone=name, task=task, pearson=r_5seed, spearman=rho_5seed,
                          ci_lo=lo, ci_hi=hi, pearson_1seed=r_1seed, perm_p=p_val,
                          null_mean=null_rs.mean(), null_std=null_rs.std()))

out = pd.DataFrame(rows)
out.to_csv(RESULTS_DIR / "significance_tests.csv", index=False)
print("\nDONE")

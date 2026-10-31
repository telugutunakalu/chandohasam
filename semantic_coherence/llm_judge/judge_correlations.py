from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import cohen_kappa_score

HERE = Path(__file__).resolve().parent
SEMANTIC_DIR = HERE.parent  # semantic_coherence/
RESULTS_DIR = HERE / "results"

LIKERT_KEYS = ["readability", "comprehension", "lexical", "bhavam", "poetic"]
BINARY_KEYS = ["chandassu", "prasa", "yati", "shabdalankara", "arthalankara"]
ALL_KEYS = LIKERT_KEYS + BINARY_KEYS

MODELS = [
    ("gemma4_e2b", "Gemma 4 E2B"),
    ("llama3_2_3b", "Llama 3.2 3B"),
    ("qwen2_5_7b", "Qwen2.5 7B"),
    ("llama3_1_8b", "Llama 3.1 8B"),
    ("gemma3_12b", "Gemma 3 12B"),
]

ann = pd.read_csv(SEMANTIC_DIR.parent / "human_evals" / "results" / "study1" / "ratings.csv")
ann = ann[ann["group"] == "A"].copy()
for k in ALL_KEYS:
    ann[k] = pd.to_numeric(ann[k], errors="coerce")

rows_out = []
for key, label in MODELS:
    path = RESULTS_DIR / f"llm_judge_{key}.csv"
    if not path.exists():
        print(f"skip {label}: {path} not found")
        continue
    judge = pd.read_csv(path)
    merged = ann.merge(judge, on="eval_id", suffixes=("_human", "_judge"))
    print(f"{label}: {len(judge)} unique poems judged, {len(merged)} pooled rows merged "
          f"(parse_ok={merged['parse_ok'].mean():.1%})")

    for k in LIKERT_KEYS:
        h = merged[f"{k}_human"] if f"{k}_human" in merged else merged[k + "_human"]
        j = merged[f"{k}_judge"] if f"{k}_judge" in merged else merged[k + "_judge"]
        mask = h.notna() & j.notna()
        n = mask.sum()
        if n < 5:
            rows_out.append(dict(model=label, question=k, kind="likert", n=n, pearson=np.nan, spearman=np.nan, mae=np.nan))
            continue
        hv, jv = h[mask].to_numpy(float), j[mask].to_numpy(float)
        rows_out.append(dict(model=label, question=k, kind="likert", n=n,
                              pearson=pearsonr(hv, jv)[0], spearman=spearmanr(hv, jv).correlation,
                              mae=float(np.mean(np.abs(hv - jv)))))

    for k in BINARY_KEYS:
        h = merged[f"{k}_human"]
        j = merged[f"{k}_judge"]
        mask = h.notna() & j.notna()
        n = mask.sum()
        if n < 5:
            rows_out.append(dict(model=label, question=k, kind="binary", n=n, accuracy=np.nan, kappa=np.nan, pearson=np.nan))
            continue
        hv, jv = h[mask].to_numpy(int), j[mask].astype(int).to_numpy(int)
        acc = float((hv == jv).mean())
        try:
            kappa = cohen_kappa_score(hv, jv)
        except Exception:
            kappa = np.nan
        pear = pearsonr(hv, jv)[0] if hv.std() > 0 and jv.std() > 0 else np.nan
        rows_out.append(dict(model=label, question=k, kind="binary", n=n, accuracy=acc, kappa=kappa, pearson=pear))

out = pd.DataFrame(rows_out)
out.to_csv(RESULTS_DIR / "llm_judge_correlations.csv", index=False)

print("\n=== LIKERT questions: Pearson r (rows=model, cols=question) ===")
likert = out[out["kind"] == "likert"]
print(likert.pivot(index="model", columns="question", values="pearson").round(3))

print("\n=== LIKERT questions: Spearman rho ===")
print(likert.pivot(index="model", columns="question", values="spearman").round(3))

print("\n=== LIKERT questions: MAE ===")
print(likert.pivot(index="model", columns="question", values="mae").round(3))

print("\n=== BINARY questions: accuracy ===")
binary = out[out["kind"] == "binary"]
print(binary.pivot(index="model", columns="question", values="accuracy").round(3))

print("\n=== BINARY questions: Cohen's kappa ===")
print(binary.pivot(index="model", columns="question", values="kappa").round(3))

print("\nDONE")

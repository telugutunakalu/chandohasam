import warnings
warnings.filterwarnings("ignore")
from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score

HERE = Path(__file__).resolve().parent
SEMANTIC_DIR = HERE.parent  # semantic_coherence/
RESULTS_DIR = HERE / "results"

MODELS = [
    ("gemma4_e2b", "Gemma 4 E2B"),
    ("llama3_2_3b", "Llama 3.2 3B"),
    ("qwen2_5_7b", "Qwen2.5 7B"),
    ("llama3_1_8b", "Llama 3.1 8B"),
    ("gemma3_12b", "Gemma 3 12B"),
]

ann = pd.read_csv(SEMANTIC_DIR.parent / "human_evals" / "results" / "study1" / "ratings.csv")
ann = ann[ann["group"] == "A"].copy()
truth = ann.drop_duplicates("eval_id")[["eval_id", "register", "ai_generated", "source_dataset"]].copy()
truth["register"] = pd.to_numeric(truth["register"], errors="coerce")
truth["ai_generated"] = pd.to_numeric(truth["ai_generated"], errors="coerce")

rows = []
for key, label in MODELS:
    judge = pd.read_csv(RESULTS_DIR / f"llm_judge_extra_{key}.csv")
    m = truth.merge(judge[["eval_id", "classical_register", "ai_generated_guess"]], on="eval_id")

    for truth_col, pred_col, name in [("register", "classical_register", "register (classical/modern)"),
                                       ("ai_generated", "ai_generated_guess", "ai_generated (human/AI)")]:
        d = m.dropna(subset=[truth_col, pred_col])
        acc = (d[truth_col] == d[pred_col]).mean()
        try:
            kappa = cohen_kappa_score(d[truth_col], d[pred_col])
        except Exception:
            kappa = float("nan")
        # recall on the minority/positive class matters most here
        pos = d[d[truth_col] == 1]
        pos_recall = (pos[pred_col] == 1).mean() if len(pos) else float("nan")
        neg = d[d[truth_col] == 0]
        neg_recall = (neg[pred_col] == 0).mean() if len(neg) else float("nan")
        rows.append(dict(model=label, question=name, n=len(d), accuracy=acc, kappa=kappa,
                          recall_class1=pos_recall, recall_class0=neg_recall))

out = pd.DataFrame(rows)
pd.set_option("display.width", 200)
print(out.round(3).to_string(index=False))

print("\n=== ai_generated_guess: per-source mean (does it even separate generated from human sources?) ===")
for key, label in MODELS:
    judge = pd.read_csv(RESULTS_DIR / f"llm_judge_extra_{key}.csv")
    m = truth.merge(judge[["eval_id", "ai_generated_guess"]], on="eval_id")
    print(f"\n{label}:")
    print(m.groupby("source_dataset")["ai_generated_guess"].mean().round(3))

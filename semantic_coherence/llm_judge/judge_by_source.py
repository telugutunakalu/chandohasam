from pathlib import Path

import pandas as pd
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

HERE = Path(__file__).resolve().parent
SEMANTIC_DIR = HERE.parent  # semantic_coherence/
RESULTS_DIR = HERE / "results"

LIKERT_KEYS = ["readability", "comprehension", "lexical", "bhavam", "poetic"]
BINARY_KEYS = ["chandassu", "prasa", "yati", "shabdalankara", "arthalankara"]

MODELS = [
    ("gemma4_e2b", "Gemma 4 E2B"),
    ("llama3_2_3b", "Llama 3.2 3B"),
    ("qwen2_5_7b", "Qwen2.5 7B"),
    ("llama3_1_8b", "Llama 3.1 8B"),
    ("gemma3_12b", "Gemma 3 12B"),
]

ann = pd.read_csv(SEMANTIC_DIR.parent / "human_evals" / "results" / "study1" / "ratings.csv")
ann = ann[ann["group"] == "A"].copy()
for k in LIKERT_KEYS + BINARY_KEYS:
    ann[k] = pd.to_numeric(ann[k], errors="coerce")
actual_by_poem = ann.groupby(["eval_id", "source_dataset"])[LIKERT_KEYS + BINARY_KEYS].mean().reset_index()

judges = {}
for key, label in MODELS:
    path = RESULTS_DIR / f"llm_judge_{key}.csv"
    if path.exists():
        judges[label] = pd.read_csv(path)

print(f"Models included: {list(judges.keys())}\n")

for q in LIKERT_KEYS:
    print(f"\n=== {q} (mean), by source ===")
    tbl = actual_by_poem.groupby("source_dataset").agg(n=("eval_id", "count"), actual=(q, "mean"))
    for label, df in judges.items():
        m = actual_by_poem[["eval_id", "source_dataset"]].merge(df[["eval_id", q]], on="eval_id")
        tbl[label] = m.groupby("source_dataset")[q].mean()
    print(tbl.round(2).sort_values("actual", ascending=False))

for q in BINARY_KEYS:
    print(f"\n=== {q} (rate of 1), by source ===")
    tbl = actual_by_poem.groupby("source_dataset").agg(n=("eval_id", "count"), actual=(q, "mean"))
    for label, df in judges.items():
        m = actual_by_poem[["eval_id", "source_dataset"]].merge(df[["eval_id", q]], on="eval_id")
        tbl[label] = m.groupby("source_dataset")[q].mean()
    print(tbl.round(2).sort_values("actual", ascending=False))

print("\nDONE")

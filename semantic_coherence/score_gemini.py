"""Scores all 255 Gemini-generated poems (metrics/initial_evals/Outputs/chandas_dataset.json --
the source of study 1's 84-poem "generated" sample) with the final Coherence/Adherence models
(MuRIL, refit on all 310 study-1 group-A rows). Exact duplicates (18) are dropped; 3 poems with no
meaning_telugu get Coherence only.

    python3 score_gemini.py
"""
import json
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import torch
from transformers import AutoModel, AutoTokenizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from sc_common import CACHE_DIR, DATA_DIR, RESULTS_DIR, REPO

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
MODEL_NAME = "google/muril-base-cased"
C = 0.003


def mean_pool(last_hidden_state, attention_mask):
    mask = attention_mask.unsqueeze(-1).to(last_hidden_state.dtype)
    return (last_hidden_state * mask).sum(1) / mask.sum(1).clamp(min=1e-9)


def embed(texts: list[str], cache_key: str, batch_size: int = 16) -> np.ndarray:
    cache_path = CACHE_DIR / f"{cache_key}.npy"
    if cache_path.exists():
        arr = np.load(cache_path)
        if arr.shape[0] == len(texts):
            return arr
    tok = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME).to(DEVICE).eval()
    vecs = []
    with torch.no_grad():
        for i in range(0, len(texts), batch_size):
            enc = tok(texts[i:i + batch_size], padding=True, truncation=True, max_length=256,
                      return_tensors="pt").to(DEVICE)
            out = model(**enc)
            vecs.append(mean_pool(out.last_hidden_state, enc["attention_mask"]).cpu().numpy())
    arr = np.concatenate(vecs, axis=0)
    np.save(cache_path, arr)
    return arr


def expected_value(model, X):
    return model.predict_proba(X) @ model.classes_


data = json.load(open(REPO / "metrics/initial_evals/Outputs/chandas_dataset.json", encoding="utf-8"))
poems = [p for p in data["poems"] if not p.get("duplicate_exact")]
print(f"{len(data['poems'])} poems, {len(poems)} after dropping exact duplicates", flush=True)
has_bhavam = [bool(p.get("meaning_telugu")) for p in poems]
print(f"{sum(has_bhavam)} have meaning_telugu (Adherence computable)", flush=True)

pooled = pd.read_csv(DATA_DIR / "pooled_study1.csv")
train_ids = sorted(set(pooled["eval_id"]))
train_idx = {e: i for i, e in enumerate(train_ids)}
row_idx = pooled["eval_id"].map(train_idx).to_numpy()
y_int = pooled["bhavam"].to_numpy(dtype=int)

train_poem = np.load(CACHE_DIR / "study1_rated_muril_poem.npy")
train_bhavam = np.load(CACHE_DIR / "study1_rated_muril_bhavam.npy")

X_coh = train_poem[row_idx]
sc_coh = StandardScaler().fit(X_coh)
coh_model = LogisticRegression(C=C, max_iter=2000).fit(sc_coh.transform(X_coh), y_int)

X_adh = (train_poem * train_bhavam)[row_idx]
sc_adh = StandardScaler().fit(X_adh)
adh_model = LogisticRegression(C=C, max_iter=2000).fit(sc_adh.transform(X_adh), y_int)

poem_texts = ["\n".join(p["lines"]) for p in poems]
poem_emb = embed(poem_texts, "gemini_muril_poem")
coh_pred = np.clip(expected_value(coh_model, sc_coh.transform(poem_emb)), 1, 5)

bhavam_idx = [i for i, h in enumerate(has_bhavam) if h]
bhavam_texts = [poems[i]["meaning_telugu"] for i in bhavam_idx]
bhavam_emb = embed(bhavam_texts, "gemini_muril_bhavam")
adh_pred_subset = np.clip(expected_value(adh_model, sc_adh.transform(poem_emb[bhavam_idx] * bhavam_emb)), 1, 5)
adh_pred = np.full(len(poems), np.nan)
adh_pred[bhavam_idx] = adh_pred_subset

rows = [dict(source="generated_gemini", id=p["id"], meter=p.get("chandassu_id"),
             coherence_muril=float(c), adherence_muril=(float(a) if not np.isnan(a) else None))
        for p, c, a in zip(poems, coh_pred, adh_pred)]
out_df = pd.DataFrame(rows)
out_path = RESULTS_DIR / "gemini_scores_muril.csv"
out_df.to_csv(out_path, index=False)
print(f"wrote {out_path}", flush=True)
print(f"\nmean coherence={out_df['coherence_muril'].mean():.3f}  "
      f"mean adherence={out_df['adherence_muril'].mean():.3f} (n={out_df['adherence_muril'].notna().sum()})", flush=True)
print("\nDONE")

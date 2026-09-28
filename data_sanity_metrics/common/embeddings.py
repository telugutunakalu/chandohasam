"""Sentence-encoder helpers for level 3: cached encoding and pair scores.

Embeddings are L2-normalised, so cosine similarity is a dot product. They are
cached under outputs/cache/ per (model, field), keyed by a hash of the texts
themselves, so an edited bhavam is re-encoded and everything else is reused.
A model is loaded only when some field is missing from the cache.
"""
import hashlib
import json

import numpy as np

import config


def _cache_path(model_key: str, field: str, texts: list):
    digest = hashlib.sha1(json.dumps(texts, ensure_ascii=False).encode()).hexdigest()[:12]
    return config.CACHE_DIR / f"emb_{model_key}_{field}_{digest}.npy"


def encode_fields(model_key: str, texts_by_field: dict, batch_size: int = 128) -> dict:
    """{field: texts} -> {field: (n, d) float32 embeddings}, cached."""
    out, missing = {}, []
    for field, texts in texts_by_field.items():
        path = _cache_path(model_key, field, texts)
        if path.exists():
            out[field] = np.load(path)
        else:
            missing.append(field)
    if not missing:
        return out

    import torch
    from sentence_transformers import SentenceTransformer
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer(config.EMBEDDING_MODELS[model_key], device=device)
    config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    for field in missing:
        texts = texts_by_field[field]
        print(f"  encoding {field} ({len(texts):,} texts) on {device}", flush=True)
        emb = model.encode(texts, batch_size=batch_size, normalize_embeddings=True,
                           convert_to_numpy=True, show_progress_bar=False).astype(np.float32)
        np.save(_cache_path(model_key, field, texts), emb)
        out[field] = emb
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return out


def paired_cosine(a, b):
    """cos(a_i, b_i) for each row i."""
    return np.einsum("ij,ij->i", a, b)


def auc(pos, neg) -> float:
    """P(score of a true pair > score of a control pair), ties count half (ROC-AUC)."""
    from sklearn.metrics import roc_auc_score
    y = np.r_[np.ones(len(pos)), np.zeros(len(neg))]
    return float(roc_auc_score(y, np.r_[pos, neg]))


def retrieval(a, b, rows, ks=(1, 10)) -> dict:
    """For each row i in `rows`, rank b_i among b[rows] by similarity to a_i.
    Recall@k and mean reciprocal rank; chance recall@1 is 1/len(rows)."""
    sims = a[rows] @ b[rows].T
    true = np.diag(sims)
    ranks = (sims > true[:, None]).sum(axis=1) + 1
    out = {f"recall@{k}": float((ranks <= k).mean()) for k in ks}
    out["mrr"] = float((1.0 / ranks).mean())
    out["pool"] = len(rows)
    return out

"""Sentence-encoder helpers for Level 3: cached encoding and pairwise scores.

Embeddings are L2-normalised, so cosine similarity is a dot product. They are
cached per (model, field) under outputs/cache/ keyed by the record ids, so
re-running a script (or adding a control) does not re-encode. The model is
loaded only if some field is missing from the cache, and only once.
"""
import hashlib
import json

import numpy as np

import config


def _cache_path(model_key, field, ids):
    digest = hashlib.sha1(json.dumps(ids).encode()).hexdigest()[:10]
    return config.CACHE_DIR / f"emb_{model_key}_{field}_{digest}.npy"


def encode_fields(model_key, texts_by_field, ids, batch_size=128):
    """{field: texts} -> {field: (n, d) float32 embeddings}, cached."""
    out, missing = {}, []
    for field in texts_by_field:
        path = _cache_path(model_key, field, ids)
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
        print(f"  encoding {field} ({len(texts_by_field[field]):,} texts) on {device}")
        emb = model.encode(texts_by_field[field], batch_size=batch_size, normalize_embeddings=True,
                           convert_to_numpy=True, show_progress_bar=False).astype(np.float32)
        np.save(_cache_path(model_key, field, ids), emb)
        out[field] = emb
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return out


def paired_cosine(a, b):
    """cos(a_i, b_i) for each row i."""
    return np.einsum("ij,ij->i", a, b)


def auc(pos, neg):
    """P(score of a true pair > score of a control pair), ties count half
    (Mann–Whitney U / ROC-AUC)."""
    from sklearn.metrics import roc_auc_score
    y = np.r_[np.ones(len(pos)), np.zeros(len(neg))]
    return float(roc_auc_score(y, np.r_[pos, neg]))


def retrieval(a, b, sample_ids, ks=(1, 10)):
    """For each sampled row i, rank b_i among b[sample] by similarity to a_i.
    Returns recall@k and mean reciprocal rank (chance recall@1 = 1/len(sample))."""
    A, B = a[sample_ids], b[sample_ids]
    sims = A @ B.T
    true = np.diag(sims)
    ranks = (sims > true[:, None]).sum(axis=1) + 1
    out = {f"recall@{k}": float((ranks <= k).mean()) for k in ks}
    out["mrr"] = float((1.0 / ranks).mean())
    out["pool"] = len(sample_ids)
    return out

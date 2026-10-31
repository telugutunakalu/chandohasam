"""Embeds poem and bhavam text with all 6 frozen backbones, for the study-1 pool (rated + unrated)
and the study-2 pool. Caches every array under embeddings_cache/ (gitignored, ~1-2 GB total) so
later scripts never re-embed. CPU or Apple-Silicon MPS; no GPU required but much slower without.

    python3 embed.py                 # everything
    python3 embed.py --only rated    # one of: rated, unrated, study2
"""
import argparse

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer, MT5EncoderModel
from sentence_transformers import SentenceTransformer

from sc_common import BACKBONES, CACHE_DIR, HUMAN_EVALS, load_poem_pool, load_study2_pool

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

BACKBONE_SPECS = {
    "indicbert_v2": dict(kind="encoder", model_name="ai4bharat/IndicBERTv2-MLM-only", model_cls=AutoModel, hf_kwargs=dict(trust_remote_code=True)),
    "mbert": dict(kind="encoder", model_name="bert-base-multilingual-cased", model_cls=AutoModel, hf_kwargs={}),
    "mt5": dict(kind="encoder", model_name="google/mt5-base", model_cls=MT5EncoderModel, hf_kwargs={}),
    "embeddinggemma_2": dict(kind="st", model_name="google/embeddinggemma-2"),
    "labse": dict(kind="st", model_name="sentence-transformers/LaBSE"),
    "muril": dict(kind="encoder", model_name="google/muril-base-cased", model_cls=AutoModel, hf_kwargs={}),
}
_encoders, _st_models = {}, {}


def mean_pool(last_hidden_state, attention_mask):
    mask = attention_mask.unsqueeze(-1).to(last_hidden_state.dtype)
    return (last_hidden_state * mask).sum(1) / mask.sum(1).clamp(min=1e-9)


def embed(name: str, texts: list[str], cache_key: str, batch_size: int = 16) -> np.ndarray:
    cache_path = CACHE_DIR / f"{cache_key}.npy"
    if cache_path.exists():
        arr = np.load(cache_path)
        if arr.shape[0] == len(texts):
            return arr
    spec = BACKBONE_SPECS[name]
    if spec["kind"] == "st":
        if name not in _st_models:
            _st_models[name] = SentenceTransformer(spec["model_name"], device=DEVICE)
        arr = np.asarray(_st_models[name].encode(texts, batch_size=batch_size, normalize_embeddings=True))
    else:
        if name not in _encoders:
            tok = AutoTokenizer.from_pretrained(spec["model_name"], **spec["hf_kwargs"])
            model = spec["model_cls"].from_pretrained(spec["model_name"], **spec["hf_kwargs"]).to(DEVICE).eval()
            _encoders[name] = (tok, model)
        tok, model = _encoders[name]
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


def embed_pool(poem_rows: list[dict], key_prefix: str):
    poem_texts = [r["poem_text"] for r in poem_rows]
    bhavam_texts = [r["bhavam_text"] for r in poem_rows]
    for name in BACKBONES:
        embed(name, poem_texts, f"{key_prefix}_{name}_poem")
        embed(name, bhavam_texts, f"{key_prefix}_{name}_bhavam")
        print(f"  {key_prefix}: {name} done ({len(poem_texts)} poems)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["rated", "unrated", "study2"])
    args = ap.parse_args()

    pool = load_poem_pool()
    import csv
    rated_ids = set(r["eval_id"] for r in csv.DictReader(open(HUMAN_EVALS / "results" / "study1" / "ratings.csv"))
                     if r["group"] == "A")

    if args.only in (None, "rated"):
        rows = [dict(eval_id=k, **v) for k, v in pool.items() if k in rated_ids]
        print(f"rated: {len(rows)} poems")
        embed_pool(rows, "study1_rated")

    if args.only in (None, "unrated"):
        rows = [dict(eval_id=k, **v) for k, v in pool.items() if k not in rated_ids]
        print(f"unrated: {len(rows)} poems")
        embed_pool(rows, "study1_unrated")

    if args.only in (None, "study2"):
        s2 = load_study2_pool()
        rows = [dict(eval_id=k, **v) for k, v in s2.items()]
        print(f"study2: {len(rows)} poems")
        embed_pool(rows, "study2")

    print("DONE")

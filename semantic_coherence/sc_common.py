"""Shared paths and helpers for the semantic_coherence scripts.

Everything here reads from this repo's own committed, already-anonymised sources
(human_evals/results/study1/ratings.csv, which uses annotator codes A1-A5, never
the annotation app's real usernames) and writes into embeddings_cache/, data/ and
results/ next to this file. embeddings_cache/ and data/ are gitignored (large,
rebuildable); results/ is committed.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
HUMAN_EVALS = REPO / "human_evals"
CACHE_DIR = HERE / "embeddings_cache"
DATA_DIR = HERE / "data"
RESULTS_DIR = HERE / "results"
for d in (CACHE_DIR, DATA_DIR, RESULTS_DIR):
    d.mkdir(exist_ok=True)

BACKBONES = ["indicbert_v2", "mbert", "mt5", "embeddinggemma_2", "labse", "muril"]
GROUP_A_CODES = {"A1", "A3", "A5"}  # the reliable 3 of 5 (human_evals/README.md); A2/A4 excluded


def line_text(line: list[dict]) -> str:
    """One poem line's plain text from the annotation app's per-token structure."""
    return "".join(tok.get("t", "") for tok in line)


def poem_text(poem: dict) -> str:
    return "\n".join(line_text(line) for line in poem["lines"])


def load_poem_pool(pool_name: str = "poems.json") -> dict:
    """eval_id -> {poem_text, bhavam_text, source_dataset, source_id, meter} for the study-1 pool."""
    data = json.load(open(HUMAN_EVALS / "annotation_app" / "data" / pool_name, encoding="utf-8"))
    pool = {}
    for p in data["poems"]:
        bhavam = (p.get("bhavam") or {}).get("te") or ""
        pool[p["id"]] = dict(
            poem_text=poem_text(p),
            bhavam_text=bhavam,
            source_dataset=p["hidden"]["source_dataset"],
            source_id=p["hidden"]["source_id"],
            meter=p["meter"],
        )
    return pool


def load_study2_pool() -> dict:
    """eval_id -> {poem_text, bhavam_text (the grid's retold prompt), model, gold_eval_id} for study 2."""
    data = json.load(open(HUMAN_EVALS / "human_eval_poems_study2.json", encoding="utf-8"))
    study1_pool = load_poem_pool()
    pool = {}
    for p in data["poems"]:
        gold_eval_id = p["metadata"]["gold_eval_id"]
        bhavam = study1_pool.get(gold_eval_id, {}).get("bhavam_text", "")
        pool[p["eval_id"]] = dict(
            poem_text="\n".join(p["lines"]),
            bhavam_text=bhavam,
            model=p["source_dataset"],
            gold_eval_id=gold_eval_id,
            meter=p["declared_meter"],
        )
    return pool

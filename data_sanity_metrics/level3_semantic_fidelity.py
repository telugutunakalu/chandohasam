"""Level 3 — Semantic fidelity of the bhavam.

Metric: cosine similarity between sentence embeddings of three pairs,
    poem – Telugu bhavam,  poem – English bhavam,  Telugu – English bhavam,
where "poem" is the verse the bhavam explains. A pair passes at
cos >= 0.65 (config.SIMILARITY_THRESHOLD). The gate is LaBSE on Telugu –
English; the other pairs and encoders are diagnostics. Encoders: LaBSE,
multilingual mpnet (mSBERT), L3Cube IndicSBERT, and an English-only negative
control (config.EMBEDDING_MODELS). Only verse poems with a bhavam are measured.

Read Te–En with care: `bhavam_en` is a machine translation OF the Telugu
bhavam (dataset/CORRECTIONS.md), so it measures translation consistency, not
whether the bhavam fits the poem. Poem – Te is the pair that bears on that.

Sense checks, per corpus, encoder and pair:
    * shuffled and neighbour controls (common/controls.py): a threshold is
      meaningful only if wrong pairings mostly fail it
    * AUC, true vs control scores: does the score separate right from wrong
      pairings, whatever its absolute level?
    * retrieval: rank the true partner among up to 2,000 poems of the corpus
    * calibrated threshold: the 99th percentile of the shuffled scores (1% of
      wrong pairs accepted), instead of the fixed 0.65
    * negative-control encoder: what a model that cannot read Telugu "passes"

Encoders run on the GPU when there is one; embeddings are cached.

Writes outputs/level3_semantic_fidelity.json

Run:  python level3_semantic_fidelity.py [--models labse msbert ...] [--datasets ...]
"""
import argparse

import numpy as np

import config
from common.controls import corpus_seed, neighbour_index, shuffled_index
from common.dataset import add_dataset_argument, by_corpus, flat, load_poems, with_bhavam
from common.embeddings import auc, encode_fields, paired_cosine, retrieval
from common.io import pct, print_table, save_result

PAIRS = {"poem_te": ("poem", "te"), "poem_en": ("poem", "en"), "te_en": ("te", "en")}
BINS = [(0.0, 0.3), (0.3, 0.5), (0.5, 0.65), (0.65, 0.85), (0.85, 1.0001)]


def texts_of(poems) -> dict:
    return {"poem": [flat(p.bhavam_verse) for p in poems],
            "te": [p.bhavam for p in poems],
            "en": [p.bhavam_en for p in poems]}


def gate_scores(poems) -> dict:
    """{poem key: LaBSE Telugu–English cosine} for poems with a bhavam (used by cross_level_summary.py)."""
    poems = with_bhavam(poems)
    texts = texts_of(poems)
    emb = encode_fields(config.GATE_MODEL, {"te": texts["te"], "en": texts["en"]})
    scores = paired_cosine(emb["te"], emb["en"])
    return {p.key: float(s) for p, s in zip(poems, scores)}


def score_pair(a, b, idx, shuffled, neighbour, rng) -> dict:
    """True, shuffled and neighbour scores of one pair for the poems at `idx`."""
    thr = config.SIMILARITY_THRESHOLD
    true = paired_cosine(a[idx], b[idx])
    ctrl = paired_cosine(a[idx], b[shuffled[idx]])
    has_nb = neighbour[idx] >= 0
    nb = paired_cosine(a[idx][has_nb], b[neighbour[idx][has_nb]])
    calibrated = float(np.quantile(ctrl, 0.99))
    pool = rng.choice(idx, size=min(config.RETRIEVAL_POOL, len(idx)), replace=False)
    return {
        "mean": float(true.mean()), "median": float(np.median(true)),
        "pass_pct": pct(int((true >= thr).sum()), len(true)),
        "shuffled_pass_pct": pct(int((ctrl >= thr).sum()), len(ctrl)),
        "neighbour_pass_pct": pct(int((nb >= thr).sum()), len(nb)),
        "auc_vs_shuffled": auc(true, ctrl),
        "auc_vs_neighbour": auc(true[has_nb], nb) if len(nb) else None,
        "retrieval": retrieval(a, b, pool),
        "calibrated_threshold": calibrated,
        "calibrated_pass_pct": pct(int((true >= calibrated).sum()), len(true)),
        "bins": {f"{lo:.2f}-{min(hi, 1):.2f}": int(((true >= lo) & (true < hi)).sum()) for lo, hi in BINS},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=list(config.EMBEDDING_MODELS))
    add_dataset_argument(ap)
    args = ap.parse_args()

    poems = with_bhavam(load_poems(tuple(args.datasets)))
    texts = texts_of(poems)
    shuffled = shuffled_index(poems, config.SEED)
    neighbour = neighbour_index(poems)
    groups = {c: np.array([i for i, p in enumerate(poems) if p.corpus == c]) for c in by_corpus(poems)}

    result = {"threshold": config.SIMILARITY_THRESHOLD, "gate": f"{config.GATE_MODEL} te_en", "models": {}}
    for model in args.models:
        print(f"\n=== {model}: {config.EMBEDDING_MODELS[model]}", flush=True)
        emb = encode_fields(model, texts)
        result["models"][model] = {}
        rows = []
        for corpus, idx in groups.items():
            rng = np.random.default_rng(corpus_seed(config.SEED, corpus))     # the retrieval pool
            result["models"][model][corpus] = {}
            for pair, (fa, fb) in PAIRS.items():
                e = score_pair(emb[fa], emb[fb], idx, shuffled, neighbour, rng)
                result["models"][model][corpus][pair] = e
                rows.append([corpus, pair, e["mean"], e["pass_pct"], e["shuffled_pass_pct"],
                             e["neighbour_pass_pct"], e["auc_vs_shuffled"], e["auc_vs_neighbour"],
                             e["retrieval"]["recall@1"], e["calibrated_threshold"], e["calibrated_pass_pct"]])
        print_table(["corpus", "pair", "mean cos", "PASS %", "shuffled pass %", "neighbour pass %",
                     "AUC shuffled", "AUC neighbour", "R@1", "thr @1% FA", "pass % @thr"], rows)

    if config.GATE_MODEL in result["models"]:
        gate = result["models"][config.GATE_MODEL]
        print_table(["corpus", "poems", *(f"{lo:.2f}-{min(hi, 1):.2f}" for lo, hi in BINS)],
                    [[c, int(len(groups[c])), *gate[c]["te_en"]["bins"].values()] for c in groups],
                    f"Gate ({config.GATE_MODEL}, Telugu – English): distribution of cosine")
    save_result("level3_semantic_fidelity", result)


if __name__ == "__main__":
    main()

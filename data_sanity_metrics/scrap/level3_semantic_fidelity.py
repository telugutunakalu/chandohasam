"""Level 3 — Semantic fidelity (§5.3, Tables 15–17).

Paper's metric: cosine similarity between sentence embeddings of
    poem – Telugu meaning, poem – English meaning, Telugu – English meaning
under LaBSE, mSBERT-mpnet and L3Cube-IndicSBERT; "pass" = cos >= 0.65.
The gate is LaBSE Telugu–English (77.1% pass, mean 0.721); the rest are
reported as diagnostics. Fields are used as stored (Level 2 showed the paper
measured raw fields); "te_clean" also strips the "తెలుగు:" prefix.

Sense checks added, per model and pair:
    * shuffled control: cos(a_i, b_j) for a random j != i. A pass threshold is
      only meaningful if control pairs mostly fail it.
    * neighbour control: b from the previous couplet of the same source
      (same story, different content): a hard negative.
    * AUC of true vs control pairs: does the score separate right from wrong
      pairings, whatever its absolute level?
    * retrieval: rank the true partner among 2,000 random candidates.
    * negative-control encoder (all-MiniLM-L6-v2, English only): what pass
      rate a model that cannot read Telugu gets at the same threshold.
    * calibrated gate: threshold = 99th percentile of the shuffled-control
      scores (1% false-accept rate), per model and pair, instead of a fixed 0.65.
    * Te–En pass rate split by whether the Telugu field carries the
      "తెలుగు:"/"Telugu:" prompt prefix.

Writes outputs/level3_semantic_fidelity.json and outputs/cache/level3_scores.npz

Run:  python level3_semantic_fidelity.py [--models labse msbert indicsbert]
"""
import argparse

import numpy as np

import config
from common.dataset import clean_meaning, load_subset, poem_flat, source_of
from common.embeddings import auc, encode_fields, paired_cosine, retrieval
from common.io import pct, print_table, save_result

PAIRS = {"poem_te": ("poem", "te"), "poem_en": ("poem", "en"), "te_en": ("te", "en"),
         "te_clean_en": ("te_clean", "en")}
BINS = [(0.0, 0.3), (0.3, 0.5), (0.5, 0.7), (0.7, 0.85), (0.85, 1.0001)]


def neighbour_index(records):
    """Index of the previous record from the same source, or -1."""
    last, out = {}, []
    for i, r in enumerate(records):
        s = source_of(r)
        out.append(last.get(s, -1))
        last[s] = i
    return np.array(out)


def stats(x, thr):
    return {"mean": float(x.mean()), "median": float(np.median(x)),
            "pass_pct": pct(int((x >= thr).sum()), len(x))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=list(config.EMBEDDING_MODELS))
    ap.add_argument("--subset", default="master")
    args = ap.parse_args()

    records = load_subset(args.subset)
    ids = [r["id"] for r in records]
    texts = {
        "poem": [poem_flat(r) for r in records],
        "te": [r["telugu_meaning"].strip() for r in records],
        "te_clean": [clean_meaning(r["telugu_meaning"]) for r in records],
        "en": [r["english_meaning"].strip() for r in records],
    }
    thr = config.SIMILARITY_THRESHOLD
    rng = np.random.default_rng(config.SEED)
    n = len(records)
    shuffled = (np.arange(n) + rng.integers(1, n, size=n)) % n       # j != i
    neigh = neighbour_index(records)
    has_neigh = neigh >= 0
    sample = rng.choice(n, size=min(2000, n), replace=False)
    sources = np.array([source_of(r) for r in records])
    prefixed = np.array([t != c for t, c in zip(texts["te"], texts["te_clean"])])

    result = {"subset": args.subset, "n": n, "threshold": thr, "paper_reported": config.PAPER["level3"],
              "models": {}}
    per_record = {}
    for m in args.models:
        print(f"\n=== {m}: {config.EMBEDDING_MODELS[m]}")
        emb = encode_fields(m, texts, ids)
        result["models"][m] = {}
        rows = []
        for pair, (fa, fb) in PAIRS.items():
            a, b = emb[fa], emb[fb]
            true = paired_cosine(a, b)
            ctrl = paired_cosine(a, b[shuffled])
            nb = paired_cosine(a[has_neigh], b[neigh[has_neigh]])
            calibrated = float(np.quantile(ctrl, 0.99))
            entry = {
                "true": stats(true, thr),
                "shuffled": stats(ctrl, thr),
                "neighbour": stats(nb, thr),
                "auc_vs_shuffled": auc(true, ctrl),
                "auc_vs_neighbour": auc(true[has_neigh], nb),
                "retrieval_2000": retrieval(a, b, sample),
                "calibrated_threshold": calibrated,
                "calibrated_pass_pct": pct(int((true >= calibrated).sum()), n),
            }
            if pair == "te_en":
                entry["bins"] = {f"{lo:.2f}-{min(hi, 1):.2f}": int(((true >= lo) & (true < hi)).sum())
                                 for lo, hi in BINS}
                entry["pass_pct_by_source"] = {s: pct(int((true[sources == s] >= thr).sum()),
                                                      int((sources == s).sum()))
                                               for s in sorted(set(sources))}
                entry["pass_pct_by_prefix"] = {
                    "with_prefix": pct(int((true[prefixed] >= thr).sum()), int(prefixed.sum())),
                    "without_prefix": pct(int((true[~prefixed] >= thr).sum()), int((~prefixed).sum())),
                    "n_with_prefix": int(prefixed.sum())}
            result["models"][m][pair] = entry
            per_record[f"{m}__{pair}"] = true
            rp = config.PAPER["level3"].get(m, {}).get(pair.replace("te_clean_en", "te_en"), {})
            rows.append([pair, entry["true"]["mean"], rp.get("mean"), entry["true"]["pass_pct"],
                         rp.get("pass_pct"), entry["shuffled"]["mean"], entry["shuffled"]["pass_pct"],
                         entry["neighbour"]["pass_pct"], entry["auc_vs_shuffled"],
                         entry["auc_vs_neighbour"], entry["retrieval_2000"]["recall@1"],
                         calibrated, entry["calibrated_pass_pct"]])
        print_table(["pair", "mean", "paper mean", "pass %", "paper pass %", "shuf mean",
                     "shuf pass %", "neigh pass %", "AUC shuf", "AUC neigh", "R@1/2000",
                     "thr@1%FA", "pass % @thr"], rows)
        te_en = result["models"][m]["te_en"]
        print(f"Te–En pass % with / without the prompt prefix: "
              f"{te_en['pass_pct_by_prefix']['with_prefix']:.1f} / "
              f"{te_en['pass_pct_by_prefix']['without_prefix']:.1f}")

    np.savez_compressed(config.CACHE_DIR / "level3_scores.npz", ids=np.array(ids), **per_record)
    save_result("level3_semantic_fidelity", result)


if __name__ == "__main__":
    main()

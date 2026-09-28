"""Cross-level summary — every level on one table, and the poems that pass levels 1-3.

Per corpus:
    L1   prosodic integrity: valid under the relaxed and the strict profile
         (labelled verse poems; common/scansion.py)
    L2   length ratio inside [0.8, 2.5] (poems with a bhavam; level2_length_ratio.py)
    L3   LaBSE Telugu – English bhavam cosine >= 0.65 (poems with a bhavam;
         level3_semantic_fidelity.py)
    L4   mean per-poem word TTR and subword TTR (level4_*.py)
    L1-3 poems that pass L1 (relaxed), L2 and L3 together, among labelled
         poems that have a bhavam

The per-poem results come from the level modules' functions, which read the
scansion and embedding caches when present and compute them otherwise, so this
script runs on its own (slowly the first time).

Writes outputs/cross_level_summary.json

Run:  python cross_level_summary.py [--workers 12] [--datasets ...]
"""
import argparse
import statistics

from transformers import AutoTokenizer

import config
from common import lexical as lx
from common.dataset import add_dataset_argument, by_corpus, load_poems
from common.io import pct, print_table, save_result
from common.scansion import scan_poems
from common.telugu import words
from level2_length_ratio import length_ratios
from level3_semantic_fidelity import gate_scores

LO, HI = config.LENGTH_RATIO_BOUNDS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=12, help="for scanning poems missing from the cache")
    add_dataset_argument(ap)
    args = ap.parse_args()

    poems = load_poems(tuple(args.datasets))
    verdicts = scan_poems(poems, args.workers)
    ratios = length_ratios(poems)
    gate = gate_scores(poems)
    tok = AutoTokenizer.from_pretrained(config.TOKENIZER)

    def l1(p, profile):
        return verdicts[p.key][profile]["valid"]

    def l2(p):
        return LO <= ratios[p.key] <= HI

    def l3(p):
        return gate[p.key] >= config.SIMILARITY_THRESHOLD

    result, rows = {}, []
    for corpus, group in by_corpus(poems).items():
        labelled = [p for p in group if p.metre]
        annotated = [p for p in group if p.bhavam]
        both = [p for p in labelled if p.bhavam]
        subword = [tok(p.text, add_special_tokens=False)["input_ids"] for p in group]
        r = {
            "labelled": len(labelled), "with_bhavam": len(annotated), "labelled_with_bhavam": len(both),
            "L1_valid_relaxed_pct": pct(sum(l1(p, "relaxed") for p in labelled), len(labelled)),
            "L1_valid_strict_pct": pct(sum(l1(p, "strict") for p in labelled), len(labelled)),
            "L2_pass_pct": pct(sum(l2(p) for p in annotated), len(annotated)),
            "L3_pass_pct": pct(sum(l3(p) for p in annotated), len(annotated)),
            "L4_poem_ttr_mean": statistics.fmean(lx.ttr(words(p.text)) for p in group),
            "L4_poem_subword_ttr_mean": statistics.fmean(len(set(x)) / len(x) for x in subword if x),
            "L1_to_L3_pass_pct": pct(sum(l1(p, "relaxed") and l2(p) and l3(p) for p in both), len(both)),
            "L2_and_L3_pass_pct": pct(sum(l2(p) and l3(p) for p in both), len(both)),
        }
        result[corpus] = r
        rows.append([corpus, r["L1_valid_relaxed_pct"], r["L1_valid_strict_pct"], r["L2_pass_pct"],
                     r["L3_pass_pct"], r["L4_poem_ttr_mean"], r["L4_poem_subword_ttr_mean"],
                     r["L1_to_L3_pass_pct"]])
    print_table(["corpus", "L1 valid % (relaxed)", "L1 valid % (strict)", "L2 pass %", "L3 pass %",
                 "L4 poem TTR", "L4 poem subword TTR", "pass L1-L3 %"], rows,
                "Cross-level summary (levels 1-4; level 5, LLM-as-a-judge, not implemented)")
    save_result("cross_level_summary", result)


if __name__ == "__main__":
    main()

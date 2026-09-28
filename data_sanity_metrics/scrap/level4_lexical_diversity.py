"""Level 4a — Lexical diversity (§5.4, Table 18, word level).

Paper's metrics on the 27,881 master poems (179,812 tokens, 88,295 types):
    corpus:   TTR 0.491, MATTR(w=50) 0.501, Yule's K 3.497, Honoré's H 6164.7,
              hapax ratio 0.804, Sichel's S 0.091
    per poem: mean TTR 0.993, mean MATTR(w=2) 1.000, mean Yule's K 22.74,
              mean Honoré's H 2356.4
and the interpretation "TTR below the 0.70–0.80 of modern prose", "K < 100 is
the literary range", "H far above the 1,000–2,000 literary baseline".

Sense checks added:
    * control corpora measured the same way at the SAME token count: the
      corpus's own Telugu prose meanings (modern Telugu) and English meanings.
      TTR and H depend on N and on morphology, so a reference range only
      means something at equal N and in the same language.
    * TTR growth curve (TTR vs N) for all three.
    * MATTR over a range of windows, to see what a window-50 value should be.
    * per-poem degeneracy: poem length in words, share of poems with TTR = 1,
      poems where Honoré's H is undefined (every word a hapax).
    * MATTR on the tokens grouped by type (the order Counter.elements() gives),
      which is what reproduces the paper's 0.501.

Tokenisation: the paper's counts (179,812 tokens / 88,295 types) are
reproduced exactly by plain whitespace splitting of the poem ("paper"). The
controls use common.telugu.words (punctuation and ZWNJ stripped, English
lower-cased) for all three corpora so they are measured alike.

Writes outputs/level4_lexical_diversity.json

Run:  python level4_lexical_diversity.py
"""
import random
import statistics
from collections import Counter

import config
from common import lexical as lx
from common.dataset import clean_meaning, load_subset
from common.io import pct, print_table, save_result
from common.telugu import words

GROWTH_SIZES = [100, 1_000, 10_000, 50_000, 100_000, 179_812]
MATTR_WINDOWS = [2, 10, 50, 100, 500, 1_000, 5_000, 20_000, 50_000]


def english_words(text):
    return [w.lower().strip("'") for w in words(text) if w.strip("'")]


def equal_n_sample(docs, n, seed):
    """Tokens from randomly ordered documents, cut at exactly n tokens."""
    docs = list(docs)
    random.Random(seed).shuffle(docs)
    out = []
    for d in docs:
        out.extend(d)
        if len(out) >= n:
            break
    return out[:n]


def per_poem(docs):
    ttrs = [lx.ttr(d) for d in docs]
    hs = [lx.honore_h(d) for d in docs]
    ks = [lx.yule_k(d) for d in docs]
    defined_h = [h for h in hs if h is not None]
    return {
        "words_per_poem_mean": statistics.fmean(len(d) for d in docs),
        "words_per_poem_min_max": [min(len(d) for d in docs), max(len(d) for d in docs)],
        "ttr_mean": statistics.fmean(ttrs),
        "share_ttr_eq_1_pct": pct(sum(t == 1.0 for t in ttrs), len(docs)),
        f"mattr_w{config.MATTR_WINDOW_POEM}_mean":
            statistics.fmean(lx.mattr(d, config.MATTR_WINDOW_POEM) for d in docs),
        "yule_k_mean": statistics.fmean(ks),
        "share_yule_k_eq_0_pct": pct(sum(k == 0 for k in ks), len(docs)),
        "honore_h_mean_over_defined": statistics.fmean(defined_h) if defined_h else None,
        "honore_h_undefined_n": sum(h is None for h in hs),
        "honore_h_undefined_pct": pct(sum(h is None for h in hs), len(docs)),
    }


def main():
    master = load_subset("master")
    paper_docs = [r["poem"].split() for r in master]          # the paper's tokenisation
    poem_docs = [words(r["poem"]) for r in master]
    te_docs = [words(clean_meaning(r["telugu_meaning"])) for r in master]
    en_docs = [english_words(clean_meaning(r["english_meaning"])) for r in master]
    paper_tokens = [t for d in paper_docs for t in d]
    poem_tokens = [t for d in poem_docs for t in d]
    n = len(poem_tokens)
    w = config.MATTR_WINDOW_CORPUS

    # corpus-level: the paper's numbers, then controls at equal N
    corpora = {
        "poems (paper tok.)": paper_tokens,
        "poems (clean tok.)": poem_tokens,
        "telugu prose, equal N": equal_n_sample(te_docs, n, config.SEED),
        "english prose, equal N": equal_n_sample(en_docs, n, config.SEED),
    }
    corpus = {name: lx.all_measures(toks, w) for name, toks in corpora.items()}
    p = config.PAPER["level4"]
    keys = ["tokens", "types", "ttr", f"mattr_w{w}", "yule_k", "honore_h", "hapax_ratio", "sichel_s"]
    paper_vals = [p["tokens"], p["types"], p["ttr"], p["mattr_w50"], p["yule_k"], p["honore_h"],
                  p["hapax_ratio"], p["sichel_s"]]
    print(f"Corpus-level lexical measures (master, n={len(master)} poems)")
    print_table(["measure", "paper", *corpus],
                [[k, pv, *(corpus[c][k] for c in corpus)] for k, pv in zip(keys, paper_vals)])

    # MATTR across windows (poems in corpus order)
    mattr_curve = {win: lx.mattr(paper_tokens, win) for win in MATTR_WINDOWS}
    print("\nMATTR of the poem corpus by window (paper reports 0.501 at w=50):")
    print_table(["window", "MATTR"], list(mattr_curve.items()))
    grouped = list(Counter(paper_tokens).elements())          # identical tokens adjacent
    mattr_grouped = lx.mattr(grouped, w)
    print(f"MATTR(w={w}) on tokens grouped by type: {mattr_grouped:.3f}   <- reproduces the paper's 0.501")

    # TTR growth curves
    growth = {
        "poems": lx.ttr_growth(None, GROWTH_SIZES, config.SEED, shuffle_docs=poem_docs),
        "telugu prose": lx.ttr_growth(None, GROWTH_SIZES, config.SEED, shuffle_docs=te_docs),
        "english prose": lx.ttr_growth(None, GROWTH_SIZES, config.SEED, shuffle_docs=en_docs),
    }
    print("\nTTR vs corpus size N (documents shuffled):")
    print_table(["N", *growth], [[s, *(growth[c].get(s) for c in growth)] for s in GROWTH_SIZES])

    # per-poem measures
    poems = per_poem(paper_docs)
    print("\nPer-poem measures (paper: TTR 0.993, MATTR(w=2) 1.000, Yule's K 22.74, Honoré's H 2356.4)")
    print_table(["measure", "value"], list(poems.items()))

    save_result("level4_lexical_diversity", {
        "paper_reported": {k: v for k, v in p.items() if not k.startswith(("gemma", "poem_subword", "exact", "near"))},
        "corpus": corpus, "mattr_by_window": mattr_curve, "mattr_w50_grouped_tokens": mattr_grouped,
        "ttr_growth": growth, "per_poem": poems,
    })


if __name__ == "__main__":
    main()

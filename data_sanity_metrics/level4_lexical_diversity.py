"""Level 4a — Lexical diversity of the verse (word level).

Metrics on the words of the verse (whitespace words with punctuation and ZWNJ
stripped, common/telugu.words), per corpus and for all corpora together:
    corpus    TTR, MATTR (window 50), Yule's K, Honoré's H, hapax ratio V1/V,
              Sichel's S = V2/V          (definitions in common/lexical.py)
    per poem  mean TTR, mean MATTR (window 2), mean Yule's K, mean Honoré's H

Sense checks:
    * reference corpora at the SAME token count N: the poems' own Telugu
      bhavams (prose) and English bhavams. TTR and Honoré's H depend on N and
      on morphology, so a "literary range" means something only at equal N
      and in the same language.
    * TTR growth curve (TTR against N), with poems shuffled so it does not
      depend on file order.
    * MATTR over a range of windows.
    * per-poem degeneracy: words per poem, share of poems with TTR = 1, and
      poems where Honoré's H is undefined (every word a hapax).

Writes outputs/level4_lexical_diversity.json

Run:  python level4_lexical_diversity.py [--datasets ...]
"""
import argparse
import random
import statistics

import config
from common import lexical as lx
from common.dataset import add_dataset_argument, by_corpus, load_poems
from common.io import pct, print_table, save_result
from common.telugu import words

GROWTH_SIZES = [100, 1_000, 10_000, 50_000, 100_000, 200_000, 400_000]
MATTR_WINDOWS = [2, 10, 50, 100, 500, 1_000, 5_000]
MEASURES = ["tokens", "types", "ttr", f"mattr_w{config.MATTR_WINDOW_CORPUS}", "yule_k", "honore_h",
            "hapax_ratio", "sichel_s"]


def english_words(text) -> list:
    return [w.lower().strip("'") for w in words(text) if w.strip("'")]


def equal_n_sample(docs, n: int, seed: int) -> list:
    """Tokens of randomly ordered documents, cut at n tokens (fewer if the documents run out)."""
    docs = list(docs)
    random.Random(seed).shuffle(docs)
    out = []
    for d in docs:
        out.extend(d)
        if len(out) >= n:
            break
    return out[:n]


def per_poem(docs) -> dict:
    docs = [d for d in docs if d]
    ttrs = [lx.ttr(d) for d in docs]
    hs = [lx.honore_h(d) for d in docs]
    defined_h = [h for h in hs if h is not None]
    return {
        "poems": len(docs),
        "words_per_poem_mean": statistics.fmean(len(d) for d in docs),
        "ttr_mean": statistics.fmean(ttrs),
        "share_ttr_eq_1_pct": pct(sum(t == 1.0 for t in ttrs), len(docs)),
        f"mattr_w{config.MATTR_WINDOW_POEM}_mean":
            statistics.fmean(lx.mattr(d, config.MATTR_WINDOW_POEM) for d in docs),
        "yule_k_mean": statistics.fmean(lx.yule_k(d) for d in docs),
        "honore_h_mean_over_defined": statistics.fmean(defined_h) if defined_h else None,
        "honore_h_undefined_pct": pct(sum(h is None for h in hs), len(docs)),
    }


def main():
    ap = argparse.ArgumentParser()
    add_dataset_argument(ap)
    args = ap.parse_args()

    poems = load_poems(tuple(args.datasets))
    w = config.MATTR_WINDOW_CORPUS
    result = {"corpus": {}, "equal_n": {}, "per_poem": {}, "ttr_growth": {}, "mattr_by_window": {}}

    for corpus, group in by_corpus(poems).items():
        verse_docs = [words(p.text) for p in group]
        te_docs = [words(p.bhavam) for p in group if p.bhavam]
        en_docs = [english_words(p.bhavam_en) for p in group if p.bhavam_en]
        verse = [t for d in verse_docs for t in d]
        n = len(verse)

        result["corpus"][corpus] = lx.all_measures(verse, w)
        result["equal_n"][corpus] = {
            "n": n,
            "verse": lx.all_measures(verse, w),
            "telugu_bhavam": lx.all_measures(equal_n_sample(te_docs, n, config.SEED), w),
            "english_bhavam": lx.all_measures(equal_n_sample(en_docs, n, config.SEED), w),
        }
        result["per_poem"][corpus] = per_poem(verse_docs)
        result["ttr_growth"][corpus] = {
            "verse": lx.ttr_growth(None, GROWTH_SIZES, config.SEED, shuffle_docs=verse_docs),
            "telugu_bhavam": lx.ttr_growth(None, GROWTH_SIZES, config.SEED, shuffle_docs=te_docs),
            "english_bhavam": lx.ttr_growth(None, GROWTH_SIZES, config.SEED, shuffle_docs=en_docs),
        }
        result["mattr_by_window"][corpus] = {win: lx.mattr(verse, win) for win in MATTR_WINDOWS if win < n}

    corpora = list(result["corpus"])
    print_table(["measure", *corpora], [[m, *(result["corpus"][c][m] for c in corpora)] for m in MEASURES],
                "Level 4a — lexical diversity of the verse, per corpus")

    rows = []
    for c in corpora:
        e = result["equal_n"][c]
        for kind in ("verse", "telugu_bhavam", "english_bhavam"):
            m = e[kind]
            rows.append([c, kind, m["tokens"], m["ttr"], m[f"mattr_w{w}"], m["yule_k"], m["honore_h"]])
    print_table(["corpus", "text", "tokens", "TTR", f"MATTR w{w}", "Yule's K", "Honoré's H"], rows,
                "Sense check — verse against its own bhavams at the same token count")

    keys = list(result["per_poem"][corpora[0]])
    print_table(["measure", *corpora], [[k, *(result["per_poem"][c][k] for c in corpora)] for k in keys],
                "Per-poem measures")

    growth = result["ttr_growth"]
    print_table(["N", *(f"{c} {kind}" for c in corpora for kind in ("verse", "bhavam"))],
                [[s, *(growth[c][kind].get(s) for c in corpora for kind in ("verse", "telugu_bhavam"))]
                 for s in GROWTH_SIZES], "TTR growth, verse vs Telugu bhavam (poems shuffled)")
    save_result("level4_lexical_diversity", result)


if __name__ == "__main__":
    main()

"""Level 4c — Duplicates (§5.4, Table 18).

Paper: 0 exact duplicates; 160 poems in 79 groups are near-duplicates "under
normalisation" (the normalisation is not specified).

Measured here, on master:
    1. exact duplicates of the poem string
    2. duplicates after normalisation:
         "paper"  whitespace + punctuation removed (common.telugu.strip_space_punct);
                  reproduces 160 poems / 79 groups exactly, so the paper's
                  "near-duplicates" are the same poem spaced/punctuated differently
         "strong" also ZWNJ and arasunna removed (common.telugu.normalise_for_dedup)
    3. near-duplicates: character-3-gram Jaccard >= t on normalised text,
       found with MinHash-LSH and verified exactly, for t in 0.9 / 0.8 / 0.7
Sense checks added:
    4. line-level reuse: a pāda that occurs (normalised) in two or more
       different couplets. Formulaic lines are expected in oral-epic verse, but
       they matter for a train/test split and for "formulaic" claims.
    5. gloss reuse: the same Telugu or English meaning attached to different
       poems (an annotation problem the poem-level check cannot see).

Writes outputs/level4_duplicates.json

Run:  python level4_duplicates.py
"""
from collections import Counter, defaultdict

import numpy as np

import config
from common.dataset import clean_meaning, load_subset, poem_lines, source_of
from common.io import pct, print_table, save_result
from common.minhash import MinHasher, candidate_pairs, connected_groups, jaccard, shingles
from common.telugu import normalise_for_dedup, strip_space_punct

THRESHOLDS = [0.9, 0.8, 0.7]
K = 3


def exact_groups(keys):
    by_key = defaultdict(list)
    for i, k in enumerate(keys):
        by_key[k].append(i)
    return [g for g in by_key.values() if len(g) > 1]


def describe(groups):
    return {"groups": len(groups), "poems": sum(len(g) for g in groups),
            "largest": max((len(g) for g in groups), default=0)}


def main():
    master = load_subset("master")
    n = len(master)

    # 1–2. exact and normalised-exact
    exact = exact_groups([r["poem"].strip() for r in master])
    paper_norm = exact_groups([strip_space_punct(r["poem"]) for r in master])
    normed = [normalise_for_dedup(r["poem"]) for r in master]
    norm_exact = exact_groups(normed)

    def spans_sources(groups):
        return sum(len({source_of(master[i]) for i in g}) > 1 for g in groups)

    # 3. near-duplicates
    sh = [shingles(t, K) for t in normed]
    mh = MinHasher(num_perm=128, seed=config.SEED)
    sigs = np.stack([mh.signature(s) for s in sh])
    cands = candidate_pairs(sigs, bands=32)                  # ~0.42 candidate threshold
    scored = [(i, j, jaccard(sh[i], sh[j])) for i, j in cands]
    near = {t: connected_groups(n, [(i, j) for i, j, s in scored if s >= t]) for t in THRESHOLDS}

    criteria = {"exact poem string": exact, "normalised (paper: space+punct)": paper_norm,
                "normalised (strong)": norm_exact}
    criteria.update({f"3-gram Jaccard >= {t}": near[t] for t in THRESHOLDS})
    rows = [[name, *describe(g).values(), spans_sources(g), sum(len(x) - 1 for x in g)]
            for name, g in criteria.items()]
    print(f"Duplicate poems in master (n={n}); paper: 0 exact, 160 poems / 79 groups near-duplicate")
    print_table(["criterion", "groups", "poems", "largest group", "groups spanning sources",
                 "redundant records"], rows)

    def examples(groups, k=8):
        return [[{"id": master[i]["id"], "source": source_of(master[i]), "poem": master[i]["poem"]}
                 for i in g[:4]] for g in sorted(groups, key=len, reverse=True)[:k]]

    # 4. line-level reuse
    line_owner = defaultdict(set)
    for i, r in enumerate(master):
        for line in poem_lines(r):
            line_owner[normalise_for_dedup(line)].add(i)
    reused = {l: s for l, s in line_owner.items() if len(s) > 1 and len(l) >= 8}
    couplets_with_reused_line = len(set().union(*reused.values())) if reused else 0
    top_lines = sorted(reused.items(), key=lambda kv: -len(kv[1]))[:10]
    print(f"\nLine-level reuse: {len(reused):,} distinct pādas occur in >1 couplet; "
          f"{couplets_with_reused_line:,} couplets ({pct(couplets_with_reused_line, n):.1f}%) contain one")

    # 5. gloss reuse
    te_groups = exact_groups([clean_meaning(r["telugu_meaning"]) for r in master])
    en_groups = exact_groups([clean_meaning(r["english_meaning"]).lower() for r in master])
    print(f"Same Telugu meaning on different poems: {describe(te_groups)}")
    print(f"Same English meaning on different poems: {describe(en_groups)}")

    save_result("level4_duplicates", {
        "n": n, "shingle_k": K,
        "paper_reported": {"exact": 0, "near_poems": 160, "near_groups": 79},
        "criteria": {name: {**describe(g), "groups_spanning_sources": spans_sources(g),
                            "redundant_records": sum(len(x) - 1 for x in g)}
                     for name, g in criteria.items()},
        "paper_normalised_examples": examples(paper_norm),
        "near_0.8_examples": examples(near[0.8]),
        "line_reuse": {"distinct_reused_lines": len(reused),
                       "couplets_with_reused_line": couplets_with_reused_line,
                       "couplets_with_reused_line_pct": pct(couplets_with_reused_line, n),
                       "top": [{"line_normalised": l, "couplets": len(s)} for l, s in top_lines]},
        "gloss_reuse": {"telugu": describe(te_groups), "english": describe(en_groups),
                        "telugu_examples": [[master[i]["poem"] for i in g[:3]] for g in te_groups[:5]]},
    })


if __name__ == "__main__":
    main()

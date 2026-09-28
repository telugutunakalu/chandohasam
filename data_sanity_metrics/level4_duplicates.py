"""Level 4c — Duplicates within and across the corpora.

Metrics, over every verse poem of the four corpora together:
    1. exact duplicates of the verse
    2. duplicates after normalisation:
         "light"   whitespace and punctuation removed (common/telugu.strip_space_punct)
         "strong"  also ZWNJ/ZWJ and the arasunna/candrabindu, which editions
                   write inconsistently (common/telugu.normalise_for_dedup)
    3. near-duplicates: character 3-gram Jaccard >= t on the strong
       normalisation, for t in 0.9 / 0.8 / 0.7, found with MinHash-LSH and
       verified exactly (common/minhash.py)
For each: duplicate groups, poems in them, redundant poems (group size - 1),
and how many groups SPAN corpora. A poem that sits in two corpora leaks from
a training split into a test split if the corpora are split separately.

Sense checks:
    4. pāda reuse: a line (normalised, >= 8 characters) found in two or more
       different poems, within a corpus and across corpora.
    5. bhavam reuse: the same Telugu bhavam, or the same English bhavam, on
       different poems (an annotation problem the verse-level checks cannot see).

Writes outputs/level4_duplicates.json

Run:  python level4_duplicates.py [--datasets ...]
"""
import argparse
from collections import Counter, defaultdict

import numpy as np

import config
from common.dataset import add_dataset_argument, load_poems
from common.io import pct, print_table, save_result
from common.minhash import MinHasher, candidate_pairs, connected_groups, jaccard, shingles
from common.telugu import normalise_for_dedup, strip_space_punct

THRESHOLDS = [0.9, 0.8, 0.7]
SHINGLE = 3


def exact_groups(keys) -> list:
    """Groups (lists of indices, size >= 2) of equal, non-empty keys."""
    by_key = defaultdict(list)
    for i, k in enumerate(keys):
        if k:
            by_key[k].append(i)
    return [g for g in by_key.values() if len(g) > 1]


def near_groups(texts, threshold: float, scored_pairs) -> list:
    return connected_groups(len(texts), [(i, j) for i, j, s in scored_pairs if s >= threshold])


def describe(groups, poems) -> dict:
    """Group counts, and how the duplicates fall across corpora."""
    spanning = [g for g in groups if len({poems[i].corpus for i in g}) > 1]
    redundant = Counter()
    for g in groups:
        for i in sorted(g)[1:]:                      # the first poem of a group is the original
            redundant[poems[i].corpus] += 1
    return {"groups": len(groups), "poems": sum(len(g) for g in groups),
            "redundant": sum(len(g) - 1 for g in groups), "largest": max((len(g) for g in groups), default=0),
            "groups_spanning_corpora": len(spanning), "redundant_by_corpus": dict(redundant)}


def examples(groups, poems, k=6) -> list:
    return [[{"key": poems[i].key, "verse": poems[i].text} for i in g[:3]]
            for g in sorted(groups, key=len, reverse=True)[:k]]


def main():
    ap = argparse.ArgumentParser()
    add_dataset_argument(ap)
    args = ap.parse_args()

    poems = load_poems(tuple(args.datasets))
    strong = [normalise_for_dedup(p.text) for p in poems]

    # 1-2. exact and normalised
    criteria = {
        "exact verse": exact_groups([p.text for p in poems]),
        "normalised (light)": exact_groups([strip_space_punct(p.text) for p in poems]),
        "normalised (strong)": exact_groups(strong),
    }
    # 3. near-duplicates
    sh = [shingles(t, SHINGLE) for t in strong]
    hasher = MinHasher(num_perm=128, seed=config.SEED)
    signatures = np.stack([hasher.signature(s) for s in sh])
    scored = [(i, j, jaccard(sh[i], sh[j])) for i, j in candidate_pairs(signatures, bands=32)]
    for t in THRESHOLDS:
        criteria[f"3-gram Jaccard >= {t}"] = near_groups(strong, t, scored)

    result = {"poems": len(poems), "criteria": {}, "examples": {}}
    rows = []
    for name, groups in criteria.items():
        d = describe(groups, poems)
        result["criteria"][name] = d
        rows.append([name, d["groups"], d["poems"], d["redundant"], d["largest"], d["groups_spanning_corpora"],
                     d["redundant_by_corpus"]])
    print_table(["criterion", "groups", "poems", "redundant", "largest", "groups spanning corpora",
                 "redundant by corpus"], rows, f"Level 4c — duplicate poems (n={len(poems):,} verse poems)")
    result["examples"]["normalised_strong"] = examples(criteria["normalised (strong)"], poems)
    near = criteria["3-gram Jaccard >= 0.8"]
    result["examples"]["near_0.8_spanning_corpora"] = examples(
        [g for g in near if len({poems[i].corpus for i in g}) > 1], poems)

    # 4. pāda reuse
    owners = defaultdict(set)
    for i, p in enumerate(poems):
        for line in p.lines:
            norm = normalise_for_dedup(line)
            if len(norm) >= 8:
                owners[norm].add(i)
    reused = {line: s for line, s in owners.items() if len(s) > 1}
    cross = {line: s for line, s in reused.items() if len({poems[i].corpus for i in s}) > 1}
    with_reused = set().union(*reused.values()) if reused else set()
    result["pada_reuse"] = {
        "distinct_reused_padas": len(reused),
        "reused_across_corpora": len(cross),
        "poems_with_a_reused_pada": len(with_reused),
        "poems_with_a_reused_pada_pct": pct(len(with_reused), len(poems)),
        "by_corpus_pct": {c: pct(sum(poems[i].corpus == c for i in with_reused), n)
                          for c, n in Counter(p.corpus for p in poems).items()},
        "most_reused": [{"pada": line, "poems": len(s)} for line, s in
                        sorted(reused.items(), key=lambda kv: -len(kv[1]))[:10]],
    }
    print(f"\nPāda reuse: {len(reused):,} distinct pādas occur in more than one poem ({len(cross):,} across "
          f"corpora); {len(with_reused):,} poems ({pct(len(with_reused), len(poems)):.1f}%) contain one. "
          f"By corpus (%): { {c: round(v, 1) for c, v in result['pada_reuse']['by_corpus_pct'].items()} }")

    # 5. bhavam reuse
    for field, key in (("telugu", lambda p: p.bhavam), ("english", lambda p: p.bhavam_en.lower())):
        groups = exact_groups([key(p) for p in poems])
        result[f"{field}_bhavam_reuse"] = {**describe(groups, poems), "examples": examples(groups, poems, 4)}
        d = result[f"{field}_bhavam_reuse"]
        print(f"The same {field} bhavam on different poems: {d['groups']} groups, {d['poems']} poems, "
              f"{d['groups_spanning_corpora']} spanning corpora")
    save_result("level4_duplicates", result)


if __name__ == "__main__":
    main()

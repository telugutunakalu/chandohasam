"""Wrong pairings used as controls by levels 2 and 3.

A score that is meant to certify "this bhavam belongs to this poem" says
something only if wrong pairings score differently:

    shuffled   each poem paired with the bhavam of a random OTHER poem of the
               same corpus (an easy negative)
    neighbour  each poem paired with the bhavam of the previous poem of the same
               work (same story and style, different content: a hard negative)

Both return, for poem i, the index j of the poem whose bhavam it is paired with.

Random draws are seeded per dataset file (corpus_seed), so a file's numbers
are the same whether it is measured alone (--datasets) or with the others.
"""
from collections import defaultdict
import zlib

import numpy as np


def corpus_seed(seed: int, corpus: str) -> int:
    """A seed of its own for each dataset file."""
    return seed * 1_000_003 + zlib.crc32(corpus.encode())


def shuffled_index(poems, seed: int) -> np.ndarray:
    """For each poem, a random other poem of the same corpus."""
    by_corpus = defaultdict(list)
    for i, p in enumerate(poems):
        by_corpus[p.corpus].append(i)
    out = np.arange(len(poems))
    for corpus, members in by_corpus.items():
        rng = np.random.default_rng(corpus_seed(seed, corpus))
        members = np.array(members)
        n = len(members)
        if n < 2:
            continue
        shift = rng.integers(1, n, size=n)              # never 0, so never the poem itself
        out[members] = members[(np.arange(n) + shift) % n]
    return out


def neighbour_index(poems) -> np.ndarray:
    """For each poem, the previous poem of the same corpus and work; -1 when there is none."""
    last = {}
    out = np.full(len(poems), -1)
    for i, p in enumerate(poems):
        group = (p.corpus, p.work)
        out[i] = last.get(group, -1)
        last[group] = i
    return out

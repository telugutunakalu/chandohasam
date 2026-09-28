"""Small MinHash + LSH for near-duplicate search, numpy only.

Signature: for each of P hash functions h_j(x) = (a_j * crc32(x) + b_j) mod p,
the minimum over the text's character shingles. LSH splits the signature into
bands; texts sharing a whole band are candidate pairs, which are then verified
with the exact Jaccard similarity of their shingle sets.
"""
import zlib
from collections import defaultdict

import numpy as np

_PRIME = np.uint64((1 << 31) - 1)


def shingles(text: str, k: int) -> set:
    if len(text) <= k:
        return {text}
    return {text[i:i + k] for i in range(len(text) - k + 1)}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a or b else 1.0


class MinHasher:
    def __init__(self, num_perm: int = 128, seed: int = 0):
        rng = np.random.default_rng(seed)
        self.a = rng.integers(1, int(_PRIME), size=num_perm, dtype=np.uint64)
        self.b = rng.integers(0, int(_PRIME), size=num_perm, dtype=np.uint64)

    def signature(self, shingle_set: set) -> np.ndarray:
        h = np.fromiter((zlib.crc32(s.encode("utf-8")) for s in shingle_set), dtype=np.uint64)
        return ((np.outer(h, self.a) + self.b) % _PRIME).min(axis=0)


def candidate_pairs(signatures: np.ndarray, bands: int) -> set:
    """Pairs (i, j), i < j, that agree on at least one band."""
    n, p = signatures.shape
    rows = p // bands
    pairs = set()
    for b in range(bands):
        buckets = defaultdict(list)
        for i, row in enumerate(signatures[:, b * rows:(b + 1) * rows]):
            buckets[row.tobytes()].append(i)
        for members in buckets.values():
            if 1 < len(members) <= 500:          # skip degenerate mega-buckets
                for x in range(len(members)):
                    for y in range(x + 1, len(members)):
                        pairs.add((members[x], members[y]))
    return pairs


def connected_groups(n: int, edges) -> list:
    """Connected components (size >= 2) of an undirected graph, via union-find."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j in edges:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
    groups = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)
    return [g for g in groups.values() if len(g) > 1]

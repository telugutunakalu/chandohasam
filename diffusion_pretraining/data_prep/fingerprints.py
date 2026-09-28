"""Token-level fingerprints: rolling n-gram hashes, MinHash signatures, LSH near-duplicate clustering.

All hashing runs over the *content* tokens of a document (whitespace, ASCII
punctuation and digits removed), so spacing and line-break differences between
two copies of the same text do not matter.
"""
from __future__ import annotations

import functools

import numpy as np

NUM_PERM = 64
BANDS, ROWS = 8, 8                  # 8 bands x 8 rows: candidates from Jaccard ~0.75 up
_P = np.uint64(0x100000001B3)       # FNV-style odd multiplier for the rolling polynomial
_rng = np.random.default_rng(20260926)
_A = _rng.integers(1, 2**62, size=NUM_PERM, dtype=np.uint64) * np.uint64(2) + np.uint64(1)
_B = _rng.integers(0, 2**62, size=NUM_PERM, dtype=np.uint64)


def content_mask(tok) -> np.ndarray:
    """Per-id: True for tokens that carry text content (not whitespace, ASCII
    punctuation/digits, or special tokens)."""
    keep = np.zeros(tok.vocab_size, dtype=bool)
    for i, b in enumerate(tok.id_to_bytes):
        if b is None:
            continue
        s = b.decode("utf-8", "replace")
        keep[i] = not (s.isspace() or (len(b) == 1 and b[0] < 0x80 and not chr(b[0]).isalpha()))
    return keep


def _mix(h: np.ndarray) -> np.ndarray:
    """splitmix64 finaliser: spreads the rolling hash over all 64 bits."""
    h = h ^ (h >> np.uint64(30))
    h = h * np.uint64(0xBF58476D1CE4E5B9)
    h = h ^ (h >> np.uint64(27))
    h = h * np.uint64(0x94D049BB133111EB)
    return h ^ (h >> np.uint64(31))


@functools.lru_cache(maxsize=None)
def _powers(n: int) -> np.ndarray:
    """[P^(n-1), ..., P, 1] modulo 2^64."""
    powers = np.ones(n, dtype=np.uint64)
    with np.errstate(over="ignore"):
        for k in range(n - 2, -1, -1):
            powers[k] = powers[k + 1] * _P
    return powers


def window_hashes(ids: np.ndarray, n: int) -> np.ndarray:
    """64-bit hash of every length-n window of ``ids`` (empty if len(ids) < n)."""
    if len(ids) < n:
        return np.empty(0, dtype=np.uint64)
    powers = _powers(n)
    windows = np.lib.stride_tricks.sliding_window_view(ids.astype(np.uint64) + np.uint64(1), n)
    with np.errstate(over="ignore"):
        return _mix((windows * powers).sum(axis=1, dtype=np.uint64))


def minhash(shingles: np.ndarray) -> np.ndarray:
    """MinHash signature (NUM_PERM uint32 values) of a set of 64-bit shingle hashes."""
    if shingles.size == 0:
        return np.full(NUM_PERM, 0xFFFFFFFF, dtype=np.uint32)
    sig = np.full(NUM_PERM, np.iinfo(np.uint64).max, dtype=np.uint64)
    with np.errstate(over="ignore"):
        for chunk in np.array_split(shingles, max(1, shingles.size // 8192)):
            h = (chunk[:, None] * _A[None, :] + _B[None, :]) >> np.uint64(32)
            np.minimum(sig, h.min(axis=0), out=sig)
    return sig.astype(np.uint32)


def near_duplicate_clusters(sigs: np.ndarray, threshold: float = 0.8) -> np.ndarray:
    """Cluster rows of ``sigs`` (n x NUM_PERM) whose estimated Jaccard >= threshold.

    LSH banding proposes candidates; each candidate is verified against the
    first member of its bucket. Returns a root id per row (rows sharing a root
    are near-duplicates)."""
    n = len(sigs)
    parent = np.arange(n)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for b in range(BANDS):
        band = np.zeros(n, dtype=np.uint64)
        with np.errstate(over="ignore"):
            for j in range(b * ROWS, (b + 1) * ROWS):
                band = band * _P + sigs[:, j].astype(np.uint64)
        band = _mix(band)
        order = np.argsort(band, kind="stable")
        sorted_band = band[order]
        starts = np.flatnonzero(np.r_[True, sorted_band[1:] != sorted_band[:-1]])
        sizes = np.diff(np.r_[starts, n])
        for s, size in zip(starts[sizes > 1], sizes[sizes > 1]):
            members = order[s:s + size]
            head = members[0]
            sim = (sigs[members[1:]] == sigs[head]).mean(axis=1)
            for m in members[1:][sim >= threshold]:
                ra, rb = find(int(head)), find(int(m))
                if ra != rb:
                    parent[max(ra, rb)] = min(ra, rb)
    return np.array([find(i) for i in range(n)])

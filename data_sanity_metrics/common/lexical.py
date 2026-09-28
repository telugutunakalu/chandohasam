"""Lexical-diversity measures used in §5.4 / Table 18, as plain functions of a
token list. N = tokens, V = types, V_i = number of types seen exactly i times.

    TTR          V / N                                   (Templin 1957)
    MATTR(w)     mean TTR over every window of w tokens   (Covington & McFall 2010)
    Yule's K     1e4 * (sum_i i^2 V_i - N) / N^2          (Yule 1944)
    Honoré's H   100 ln N / (1 - V_1/V)                   (Honoré 1979)
    hapax ratio  V_1 / V
    Sichel's S   V_2 / V                                  (Sichel 1975)

Honoré's H is undefined when every type is a hapax (V_1 = V); the function
returns None then instead of dividing by zero.
"""
import math
import random
from collections import Counter


def spectrum(tokens) -> Counter:
    """Frequency spectrum {i: V_i}."""
    return Counter(Counter(tokens).values())


def ttr(tokens) -> float:
    return len(set(tokens)) / len(tokens) if tokens else float("nan")


def mattr(tokens, window: int) -> float:
    """Moving-average TTR. Falls back to plain TTR when the text is shorter
    than the window (the usual convention)."""
    n = len(tokens)
    if n == 0:
        return float("nan")
    if n <= window:
        return ttr(tokens)
    counts = Counter(tokens[:window])
    total = len(counts)
    for i in range(window, n):
        out, inc = tokens[i - window], tokens[i]
        counts[out] -= 1
        if counts[out] == 0:
            del counts[out]
        counts[inc] += 1
        total += len(counts)
    return total / ((n - window + 1) * window)


def yule_k(tokens) -> float:
    n = len(tokens)
    if n == 0:
        return float("nan")
    m2 = sum(i * i * v for i, v in spectrum(tokens).items())
    return 1e4 * (m2 - n) / (n * n)


def honore_h(tokens):
    n = len(tokens)
    counts = Counter(tokens)
    v = len(counts)
    v1 = sum(1 for c in counts.values() if c == 1)
    if n == 0 or v1 == v:
        return None
    return 100 * math.log(n) / (1 - v1 / v)


def hapax_ratio(tokens) -> float:
    counts = Counter(tokens)
    return sum(1 for c in counts.values() if c == 1) / len(counts) if counts else float("nan")


def sichel_s(tokens) -> float:
    counts = Counter(tokens)
    return sum(1 for c in counts.values() if c == 2) / len(counts) if counts else float("nan")


def all_measures(tokens, mattr_window: int) -> dict:
    return {
        "tokens": len(tokens),
        "types": len(set(tokens)),
        "ttr": ttr(tokens),
        f"mattr_w{mattr_window}": mattr(tokens, mattr_window),
        "yule_k": yule_k(tokens),
        "honore_h": honore_h(tokens),
        "hapax_ratio": hapax_ratio(tokens),
        "sichel_s": sichel_s(tokens),
    }


def ttr_growth(tokens, sizes, seed: int = 0, shuffle_docs=None) -> dict:
    """TTR of the first n tokens for each n in sizes. If shuffle_docs (a list of
    per-document token lists) is given, documents are shuffled first so the
    curve does not depend on corpus order."""
    if shuffle_docs is not None:
        docs = list(shuffle_docs)
        random.Random(seed).shuffle(docs)
        tokens = [t for d in docs for t in d]
    return {n: ttr(tokens[:n]) for n in sizes if n <= len(tokens)}

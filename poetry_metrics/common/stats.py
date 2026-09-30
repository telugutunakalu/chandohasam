"""Rank statistics used by the validation scripts (standard library only)."""
from __future__ import annotations

import math
import statistics


def ranks(values: list) -> list:
    """Mid-ranks (ties share the mean rank)."""
    order = sorted(range(len(values)), key=values.__getitem__)
    out, i = [0.0] * len(values), 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return out


def spearman(x: list, y: list) -> float:
    rx, ry = ranks(x), ranks(y)
    mx, my = statistics.fmean(rx), statistics.fmean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return round(num / den, 4) if den else 0.0


def auc(pos: list, neg: list) -> dict:
    """P(a random positive outscores a random negative), ties half; z from the Mann-Whitney normal approximation."""
    m, n = len(pos), len(neg)
    r = ranks(pos + neg)
    u = sum(r[:m]) - m * (m + 1) / 2
    z = (u - m * n / 2) / math.sqrt(m * n * (m + n + 1) / 12)
    return {"auc": round(u / (m * n), 4), "z": round(z, 2), "n_pos": m, "n_neg": n}


def summary(values: list) -> dict:
    """n, mean, sd, 10th percentile, median, 90th percentile."""
    values = [v for v in values if v is not None]
    qs = statistics.quantiles(values, n=10)
    return {"n": len(values), "mean": round(statistics.fmean(values), 4), "sd": round(statistics.pstdev(values), 4),
            "p10": round(qs[0], 4), "median": round(statistics.median(values), 4), "p90": round(qs[8], 4)}

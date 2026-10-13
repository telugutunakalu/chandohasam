# -*- coding: utf-8 -*-
"""
Inter-annotator agreement statistics, standard library only.

Data shapes
-----------
``units``    {unit_id: [value, value, …]}: the values one poem received, one per
             annotator. Missing ratings are simply absent; None values are dropped.
``ratings``  {unit_id: {annotator: value}}: the same data with the annotators kept,
             which the pairwise statistics need.

Every function returns ``None`` when the statistic is undefined, for example when
fewer than two values are pairable or when every value is the same (chance
agreement is then 1 and kappa is 0/0). It never raises on sparse data.

Statistics
----------
* Krippendorff's alpha, with the nominal, ordinal, interval and ratio metrics
  (Krippendorff 2011, "Computing Krippendorff's Alpha-Reliability"). Any number
  of annotators is allowed, and ratings may be missing.
* Fleiss' kappa. When poems have different numbers of ratings, each poem's
  agreement is averaged with equal weight, and the category proportions pool
  all ratings. With equal numbers this is Fleiss (1971) exactly.
* Gwet's AC1 for nominal data with any number of raters (Gwet 2008). It is
  robust to the high-prevalence "kappa paradox", for example when nearly every
  poem is rated "chandassu correct".
* Cohen's kappa for two annotators: unweighted, linear-weighted or
  quadratic-weighted.
* Pairwise agreement and agreement within ±1, averaged over pairs within each
  poem.
* Percentile bootstrap over poems, giving a confidence interval for any of the
  statistics above.
"""
from __future__ import annotations

import random
from collections import Counter, defaultdict
from itertools import combinations
from typing import Callable, Hashable, Iterable, Mapping, Optional, Sequence

Units = Mapping[Hashable, Sequence]
LEVELS = ("nominal", "ordinal", "interval", "ratio")


def _clean(units: Units) -> dict:
    """Drop None values and keep only units with at least two values (the pairable ones)."""
    out = {}
    for u, vals in units.items():
        vs = [v for v in vals if v is not None]
        if len(vs) >= 2:
            out[u] = vs
    return out


# -----------------------------------------------------------------------------
# Krippendorff's alpha
# -----------------------------------------------------------------------------
def coincidences(units: Units) -> dict:
    """The coincidence matrix o[(c, k)] of the pairable values (each unit weighted 1/(m_u - 1))."""
    o: dict = defaultdict(float)
    for vals in _clean(units).values():
        m = len(vals)
        counts = Counter(vals)
        for c, nc in counts.items():
            for k, nk in counts.items():
                pairs = nc * (nk - 1) if c == k else nc * nk
                if pairs:
                    o[(c, k)] += pairs / (m - 1)
    return dict(o)


def _delta2(level: str, marginals: dict, cats: list) -> Callable:
    if level == "nominal":
        return lambda c, k: 0.0 if c == k else 1.0
    if level == "interval":
        return lambda c, k: float(c - k) ** 2
    if level == "ratio":
        return lambda c, k: ((c - k) / (c + k)) ** 2 if (c + k) != 0 else 0.0
    if level == "ordinal":
        index = {c: i for i, c in enumerate(cats)}
        cumulative = [0.0]
        for c in cats:
            cumulative.append(cumulative[-1] + marginals.get(c, 0.0))

        def ordinal(c, k):
            i, j = sorted((index[c], index[k]))
            between = cumulative[j + 1] - cumulative[i]          # n_i + … + n_j
            return (between - (marginals[c] + marginals[k]) / 2.0) ** 2
        return ordinal
    raise ValueError(f"level must be one of {LEVELS}")


def alpha_from_coincidences(o: Mapping, level: str = "nominal") -> Optional[float]:
    marginals: dict = defaultdict(float)
    for (c, _k), v in o.items():
        marginals[c] += v
    n = sum(marginals.values())
    if n <= 1 or len(marginals) < 2:
        return None
    cats = sorted(marginals)
    d2 = _delta2(level, marginals, cats)
    observed = sum(v * d2(c, k) for (c, k), v in o.items())
    expected = sum(marginals[c] * marginals[k] * d2(c, k) for c in cats for k in cats)
    if expected == 0:
        return None
    return 1.0 - (n - 1) * observed / expected


def krippendorff_alpha(units: Units, level: str = "nominal") -> Optional[float]:
    """Krippendorff's alpha of ``units`` under the given level of measurement."""
    if level not in LEVELS:
        raise ValueError(f"level must be one of {LEVELS}")
    return alpha_from_coincidences(coincidences(units), level)


# -----------------------------------------------------------------------------
# multi-rater kappa-type coefficients
# -----------------------------------------------------------------------------
def percent_agreement(units: Units) -> Optional[float]:
    """Mean over units of the share of agreeing rater pairs (Fleiss' P-bar)."""
    shares = []
    for vals in _clean(units).values():
        m = len(vals)
        agree = sum(n * (n - 1) for n in Counter(vals).values())
        shares.append(agree / (m * (m - 1)))
    return sum(shares) / len(shares) if shares else None


def within_one_agreement(units: Units, tolerance: float = 1) -> Optional[float]:
    """Mean over units of the share of rater pairs whose values differ by at most ``tolerance``."""
    shares = []
    for vals in _clean(units).values():
        pairs = list(combinations(vals, 2))
        shares.append(sum(abs(a - b) <= tolerance for a, b in pairs) / len(pairs))
    return sum(shares) / len(shares) if shares else None


def fleiss_kappa(units: Units) -> Optional[float]:
    """Fleiss' kappa. When units have different numbers of raters, each unit counts with equal weight."""
    clean = _clean(units)
    if not clean:
        return None
    p_bar = percent_agreement(clean)
    totals: Counter = Counter()
    for vals in clean.values():
        totals.update(vals)
    n = sum(totals.values())
    p_e = sum((c / n) ** 2 for c in totals.values())
    if p_e >= 1.0:
        return None
    return (p_bar - p_e) / (1.0 - p_e)


def gwet_ac1(units: Units, categories: Optional[Iterable] = None) -> Optional[float]:
    """Gwet's AC1 (nominal), any number of raters, missing ratings allowed.

    ``categories`` is the full category set (for a yes/no item: [0, 1]); it fixes q,
    the number of categories, even when the data use only one of them.
    """
    rated = {u: [v for v in vals if v is not None] for u, vals in units.items()}
    rated = {u: v for u, v in rated.items() if v}
    pairable = {u: v for u, v in rated.items() if len(v) >= 2}
    if not pairable:
        return None
    cats = list(categories) if categories is not None else sorted({v for vs in rated.values() for v in vs})
    q = len(cats)
    if q < 2:
        return None
    p_a = sum(sum(n * (n - 1) for n in Counter(v).values()) / (len(v) * (len(v) - 1))
              for v in pairable.values()) / len(pairable)
    pi = {c: sum(Counter(v)[c] / len(v) for v in rated.values()) / len(rated) for c in cats}
    p_e = sum(p * (1 - p) for p in pi.values()) / (q - 1)
    if p_e >= 1.0:
        return None
    return (p_a - p_e) / (1.0 - p_e)


# -----------------------------------------------------------------------------
# two raters
# -----------------------------------------------------------------------------
def cohen_kappa(a: Sequence, b: Sequence, weights: Optional[str] = None,
                categories: Optional[Sequence] = None) -> Optional[float]:
    """Cohen's kappa between two aligned rating lists; ``weights`` None | 'linear' | 'quadratic'.

    Weighted kappa measures disagreement by the distance between category positions in
    ``categories`` (default: the sorted values seen), so pass the full scale, e.g. [1..5].
    """
    if len(a) != len(b):
        raise ValueError("rating lists differ in length")
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if not pairs:
        return None
    cats = list(categories) if categories is not None else sorted({v for p in pairs for v in p})
    index = {c: i for i, c in enumerate(cats)}
    k = len(cats)
    if k < 2:
        return None
    if weights is None:
        dist = lambda i, j: 0.0 if i == j else 1.0                           # noqa: E731
    elif weights == "linear":
        dist = lambda i, j: abs(i - j) / (k - 1)                             # noqa: E731
    elif weights == "quadratic":
        dist = lambda i, j: ((i - j) / (k - 1)) ** 2                         # noqa: E731
    else:
        raise ValueError("weights must be None, 'linear' or 'quadratic'")
    n = len(pairs)
    row, col, joint = Counter(), Counter(), Counter()
    for x, y in pairs:
        i, j = index[x], index[y]
        row[i] += 1
        col[j] += 1
        joint[(i, j)] += 1
    observed = sum(cnt * dist(i, j) for (i, j), cnt in joint.items()) / n
    expected = sum(row[i] * col[j] * dist(i, j) for i in row for j in col) / (n * n)
    if expected == 0:
        return None
    return 1.0 - observed / expected


def pairwise_cohen(ratings: Mapping[Hashable, Mapping[Hashable, object]], weights: Optional[str] = None,
                   categories: Optional[Sequence] = None, min_overlap: int = 5) -> dict:
    """Cohen's kappa for every annotator pair sharing at least ``min_overlap`` rated units.

    Returns {(a, b): {"kappa": float|None, "n": int}} with a < b.
    """
    shared: dict = defaultdict(list)
    for per_unit in ratings.values():
        present = sorted((r, v) for r, v in per_unit.items() if v is not None)
        for (ra, va), (rb, vb) in combinations(present, 2):
            shared[(ra, rb)].append((va, vb))
    out = {}
    for pair, vals in sorted(shared.items()):
        if len(vals) < min_overlap:
            continue
        xs, ys = zip(*vals)
        out[pair] = {"kappa": cohen_kappa(xs, ys, weights=weights, categories=categories), "n": len(vals)}
    return out


def mean_pairwise_kappa(pairs: Mapping) -> Optional[float]:
    """Unweighted mean of the defined pairwise kappas."""
    ks = [p["kappa"] for p in pairs.values() if p["kappa"] is not None]
    return sum(ks) / len(ks) if ks else None


# -----------------------------------------------------------------------------
# bootstrap
# -----------------------------------------------------------------------------
def bootstrap_ci(units: Units, statistic: Callable[[Units], Optional[float]], n_boot: int = 1000,
                 seed: int = 0, level: float = 0.95) -> Optional[tuple[float, float]]:
    """Percentile bootstrap CI of ``statistic`` over units (poems resampled with replacement)."""
    clean = _clean(units)
    keys = list(clean)
    if len(keys) < 2 or n_boot < 1:
        return None
    rng = random.Random(seed)
    stats = []
    for _ in range(n_boot):
        sample = {i: clean[rng.choice(keys)] for i in range(len(keys))}
        s = statistic(sample)
        if s is not None:
            stats.append(s)
    if len(stats) < max(10, n_boot // 2):
        return None
    stats.sort()
    lo = stats[int((1 - level) / 2 * (len(stats) - 1))]
    hi = stats[int((1 + level) / 2 * (len(stats) - 1))]
    return lo, hi


def bootstrap_alpha_ci(units: Units, level_of_measurement: str = "nominal", n_boot: int = 1000,
                       seed: int = 0, level: float = 0.95) -> Optional[tuple[float, float]]:
    """Fast bootstrap CI for Krippendorff's alpha: per-unit coincidences are computed once and summed."""
    per_unit = [coincidences({0: vals}) for vals in _clean(units).values()]
    if len(per_unit) < 2 or n_boot < 1:
        return None
    rng = random.Random(seed)
    stats = []
    for _ in range(n_boot):
        total: dict = defaultdict(float)
        for _i in range(len(per_unit)):
            for key, v in rng.choice(per_unit).items():
                total[key] += v
        a = alpha_from_coincidences(total, level_of_measurement)
        if a is not None:
            stats.append(a)
    if len(stats) < max(10, n_boot // 2):
        return None
    stats.sort()
    return stats[int((1 - level) / 2 * (len(stats) - 1))], stats[int((1 + level) / 2 * (len(stats) - 1))]

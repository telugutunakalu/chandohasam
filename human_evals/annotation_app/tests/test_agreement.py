# -*- coding: utf-8 -*-
"""Agreement statistics against published worked examples and sklearn / krippendorff reference values."""
import math

import pytest

from padya_eval import agreement as ag

# Krippendorff (2011), "Computing Krippendorff's Alpha-Reliability", the 4-coder x 12-unit example
K2011 = [
    [1, 2, 3, 3, 2, 1, 4, 1, 2, None, None, None],
    [1, 2, 3, 3, 2, 2, 4, 1, 2, 5, None, 3],
    [None, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, None],
    [1, 2, 3, 3, 2, 4, 4, 1, 2, 5, 1, None],
]
K2011_UNITS = {u: [row[u] for row in K2011] for u in range(12)}


@pytest.mark.parametrize("level, expected", [("nominal", 0.743), ("ordinal", 0.815),
                                             ("interval", 0.849), ("ratio", 0.797)])
def test_krippendorff_2011_worked_example(level, expected):
    assert round(ag.krippendorff_alpha(K2011_UNITS, level), 3) == expected


def test_alpha_perfect_agreement_is_one():
    units = {1: [1, 1, 1], 2: [3, 3], 3: [5, 5, 5], 4: [2, 2]}
    for level in ag.LEVELS:
        assert ag.krippendorff_alpha(units, level) == pytest.approx(1.0)


def test_alpha_undefined_cases():
    assert ag.krippendorff_alpha({}, "nominal") is None
    assert ag.krippendorff_alpha({1: [3], 2: [4]}, "nominal") is None          # nothing pairable
    assert ag.krippendorff_alpha({1: [1, 1], 2: [1, 1]}, "nominal") is None    # no variation
    assert ag.krippendorff_alpha({1: [None, 2], 2: [3, None]}, "nominal") is None


def test_alpha_rejects_unknown_level():
    with pytest.raises(ValueError):
        ag.krippendorff_alpha(K2011_UNITS, "cardinal")


def test_alpha_systematic_disagreement_is_negative():
    units = {i: [1, 2] for i in range(10)}                # raters never agree
    assert ag.krippendorff_alpha(units, "nominal") < 0


def test_ordinal_alpha_ignores_category_labels_but_not_order():
    a = {1: [1, 2], 2: [2, 2], 3: [3, 4], 4: [4, 4], 5: [1, 1]}
    b = {u: [{1: 10, 2: 20, 3: 70, 4: 90}[v] for v in vs] for u, vs in a.items()}   # monotone relabelling
    assert ag.krippendorff_alpha(a, "ordinal") == pytest.approx(ag.krippendorff_alpha(b, "ordinal"))


def test_coincidence_matrix_totals_pairable_values():
    o = ag.coincidences(K2011_UNITS)
    n = sum(o.values())
    assert n == pytest.approx(sum(len([v for v in vs if v is not None]) for vs in K2011_UNITS.values()
                                  if len([v for v in vs if v is not None]) >= 2))
    assert all(o[(c, k)] == pytest.approx(o[(k, c)]) for (c, k) in o)


# Fleiss (1971) example as tabulated on Wikipedia: 10 subjects, 14 raters, 5 categories -> kappa 0.210
FLEISS_TABLE = [
    [0, 0, 0, 0, 14], [0, 2, 6, 4, 2], [0, 0, 3, 5, 6], [0, 3, 9, 2, 0], [2, 2, 8, 1, 1],
    [7, 7, 0, 0, 0], [3, 2, 6, 3, 0], [2, 5, 3, 2, 2], [6, 5, 2, 1, 0], [0, 2, 2, 3, 7],
]
FLEISS_UNITS = {i: [c for c, n in enumerate(row, 1) for _ in range(n)] for i, row in enumerate(FLEISS_TABLE)}


def test_fleiss_kappa_textbook_example():
    assert round(ag.percent_agreement(FLEISS_UNITS), 3) == 0.378
    assert round(ag.fleiss_kappa(FLEISS_UNITS), 3) == 0.210


def test_fleiss_undefined_when_one_category():
    assert ag.fleiss_kappa({1: [1, 1], 2: [1, 1, 1]}) is None
    assert ag.fleiss_kappa({}) is None


def test_gwet_ac1_two_raters_by_hand():
    # 10 poems: 8 both yes, 1 split, 1 both no
    units = {i: [1, 1] for i in range(8)}
    units[8] = [1, 0]
    units[9] = [0, 0]
    p_a = 0.9
    pi_yes = (8 * 1 + 0.5 + 0) / 10
    p_e = pi_yes * (1 - pi_yes) + (1 - pi_yes) * pi_yes
    assert ag.gwet_ac1(units, categories=[0, 1]) == pytest.approx((p_a - p_e) / (1 - p_e))


def test_gwet_ac1_survives_the_prevalence_paradox():
    # 19 poems all "yes" by both raters, one split: kappa collapses, AC1 stays high
    units = {i: [1, 1] for i in range(19)}
    units[19] = [1, 0]
    assert ag.fleiss_kappa(units) < 0.1
    assert ag.gwet_ac1(units, categories=[0, 1]) > 0.9
    assert ag.gwet_ac1({1: [1, 1], 2: [1, 1]}, categories=[0, 1]) == pytest.approx(1.0)


def test_gwet_ac1_uses_single_ratings_for_prevalence():
    with_singles = {1: [1, 0], 2: [1, 1], 3: [0], 4: [0]}
    without = {1: [1, 0], 2: [1, 1]}
    assert ag.gwet_ac1(with_singles, [0, 1]) != pytest.approx(ag.gwet_ac1(without, [0, 1]))


def test_percent_and_within_one():
    units = {1: [1, 1, 2], 2: [3, 5], 3: [4, 4]}
    # unit1: 1 agreeing pair of 3; unit2: 0 of 1; unit3: 1 of 1
    assert ag.percent_agreement(units) == pytest.approx((1 / 3 + 0 + 1) / 3)
    # unit1: all 3 pairs within 1; unit2: 0; unit3: 1
    assert ag.within_one_agreement(units) == pytest.approx((1 + 0 + 1) / 3)
    assert ag.percent_agreement({1: [2]}) is None


# reference values from sklearn.metrics.cohen_kappa_score(a, b, weights=w, labels=[1..5])
A = [1, 2, 3, 4, 5, 3, 2, 4, 5, 1, 2, 3]
B = [1, 3, 3, 4, 4, 3, 2, 5, 5, 2, 2, 3]


@pytest.mark.parametrize("weights, expected", [(None, 0.5752212389380531), ("linear", 0.7647058823529411),
                                               ("quadratic", 0.8951965065502183)])
def test_cohen_kappa_matches_sklearn(weights, expected):
    assert ag.cohen_kappa(A, B, weights=weights, categories=[1, 2, 3, 4, 5]) == pytest.approx(expected, abs=1e-12)


def test_cohen_kappa_edge_cases():
    assert ag.cohen_kappa([1, 1], [1, 1]) is None
    assert ag.cohen_kappa([None], [1]) is None
    assert ag.cohen_kappa([0, 1, 0, 1], [0, 1, 0, 1], categories=[0, 1]) == pytest.approx(1.0)
    with pytest.raises(ValueError):
        ag.cohen_kappa([1], [1, 2])
    with pytest.raises(ValueError):
        ag.cohen_kappa([1, 2], [1, 2], weights="cubic")


def test_pairwise_cohen_respects_min_overlap():
    ratings = {f"p{i}": {"a": i % 2, "b": i % 2, "c": 1} for i in range(6)}
    ratings["p6"] = {"a": 1, "d": 0}
    pairs = ag.pairwise_cohen(ratings, categories=[0, 1], min_overlap=5)
    assert set(pairs) == {("a", "b"), ("a", "c"), ("b", "c")}
    assert pairs[("a", "b")] == {"kappa": pytest.approx(1.0), "n": 6}
    assert pairs[("a", "c")]["kappa"] == pytest.approx(0.0)
    assert ag.mean_pairwise_kappa(pairs) == pytest.approx((1 + 0 + 0) / 3)
    assert ag.mean_pairwise_kappa({}) is None


def test_bootstrap_ci_brackets_the_estimate_and_is_reproducible():
    point = ag.krippendorff_alpha(K2011_UNITS, "interval")
    ci = ag.bootstrap_alpha_ci(K2011_UNITS, "interval", n_boot=400, seed=3)
    assert ci[0] <= point <= ci[1]
    assert ci == ag.bootstrap_alpha_ci(K2011_UNITS, "interval", n_boot=400, seed=3)
    generic = ag.bootstrap_ci(K2011_UNITS, lambda u: ag.krippendorff_alpha(u, "interval"), n_boot=400, seed=3)
    assert generic[0] <= point <= generic[1]
    assert ag.bootstrap_alpha_ci({1: [1, 2]}, "nominal") is None


def test_statistics_ignore_none_values():
    with_none = {1: [1, None, 1], 2: [2, 2, None], 3: [None, 1, 2]}
    without = {1: [1, 1], 2: [2, 2], 3: [1, 2]}
    for f in (lambda u: ag.krippendorff_alpha(u, "nominal"), ag.percent_agreement, ag.fleiss_kappa):
        assert f(with_none) == pytest.approx(f(without))
    assert not math.isnan(ag.gwet_ac1(with_none, [1, 2]))

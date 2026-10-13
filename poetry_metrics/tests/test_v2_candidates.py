"""Tests of the version 2.0 candidates (anuprasa_v2, madhurya_v2, prasada_v2) and of compare_versions.

    cd poetry_metrics && python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import itertools
import json
import statistics
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import anuprasa as ap                       # noqa: E402
import anuprasa_v2 as ap2                   # noqa: E402
import compare_versions as cv               # noqa: E402
import degradation_protocol as dp           # noqa: E402
import madhurya as md                       # noqa: E402
import madhurya_v2 as md2                   # noqa: E402
import prasada as pr                        # noqa: E402
import prasada_v2 as pr2                    # noqa: E402
import validation_madhurya as vm            # noqa: E402
from common.phonology import Token          # noqa: E402

AP1, AP2 = ap.load_baseline(), ap2.load_baseline()
MD2 = md2.load_baseline()
MODEL2 = pr2.load_model()
EXEMPLARS = {e["id"]: e for e in vm.load_exemplars()}
LINES = ["కరికిఁ గరాగ్రస్థగిరికిఘనతరకిరికిన్.", "కళలు గలుగుఁ గాక; కమల తోడగుగాక;", "రామ రావణ యుద్ధము"]


def shifted(baseline: dict, path: tuple, by: float) -> dict:
    """A copy of the baseline whose reference quantiles at `path` are moved by `by`."""
    other = json.loads(json.dumps({k: v for k, v in baseline.items() if k != "level_probs"}))
    node = other
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = [v + by for v in node[path[-1]]]
    if "level_probs" in baseline:
        other["level_probs"] = baseline["level_probs"]
    return other


class AnuprasaV2(unittest.TestCase):
    def test_the_chance_model_is_the_language_references(self):
        counts, n_aksharas = ap2.language_counts()
        self.assertEqual(n_aksharas, MODEL2.meta["akshara_tokens"])            # every akshara of prasāda's reference
        probs = ap2.chance_probabilities(counts)
        self.assertAlmostEqual(sum(probs.values()), 1.0, places=9)
        self.assertEqual({s: round(p, 8) for s, p in probs.items()}, AP2["probabilities"])

    def test_with_version_1_frequencies_it_is_version_1(self):
        a, b = ap2.score_poem(LINES, AP1), ap.score_poem(LINES, AP1)
        self.assertEqual((a.pop("version"), b.pop("version")), ("2.0", "1.0"))
        self.assertEqual(json.dumps(a), json.dumps(b))

    def test_no_dataset_statistic_enters_the_score_or_the_label(self):
        other = shifted(AP2, ("reference", "varga", "poem_z"), 1.0)
        lines = ["మందార మకరందమాధుర్యమునఁ దేలు-", "మధుపంబు వోవునేమదనములకు?"]
        a, b = ap2.score_poem(lines, AP2), ap2.score_poem(lines, other)
        self.assertEqual((a["z"], a["score"], a["label"]), (b["z"], b["score"], b["label"]))
        self.assertNotEqual(a["varga"]["z_percentile"], b["varga"]["z_percentile"])

    def test_the_treatise_example_of_vrttyanuprasa(self):
        r = ap2.score_poem(cv.TREATISE_VRTTYANUPRASA["lines"], AP2)
        self.assertGreaterEqual(r["varna"]["z_percentile"], 95)
        self.assertEqual([l["varna"]["carriers"][0]["sound"] for l in r["lines"][:3]], ["ష"] * 3)


class OwnChanceModel(unittest.TestCase):
    """The rejected corpus-free candidate of compare_versions.py: its moments must still be exact."""

    def test_moments_are_exact_under_the_permutation(self):
        skeleton = [[0, 1, 1, 2, 4], [0, 2, 3, 3, 5]]                # akshara of each token; 1 and 3 are conjuncts
        sounds = list("aaabbcdabc")
        def deal(order):
            it = iter(order)
            return [tuple(Token(next(it), a, "") for a in line) for line in skeleton]

        def repeats(poem, window):
            return sum(1 for line in poem for i, j in itertools.combinations(range(len(line)), 2)
                       if line[i].akshara != line[j].akshara and line[i].char == line[j].char
                       and (window is None or line[j].akshara - line[i].akshara <= window))

        for window in (None, 2):
            # every distinct deal of the sounds is equally likely: the exact mean and variance of A
            a = [repeats(deal(order), window) for order in set(itertools.permutations(sounds))]
            expected = (repeats(deal(sounds), window) - statistics.fmean(a)) / statistics.pvariance(a) ** 0.5
            self.assertAlmostEqual(cv.own_chance_z(deal(sounds), lambda t: t.char, window)[0], expected, places=9)

    def test_a_poem_of_one_sound_has_no_excess(self):
        poem = [tuple(Token("m", a, "") for a in range(6)), tuple(Token("m", a, "") for a in range(5))]
        self.assertEqual(cv.own_chance_z(poem, lambda t: t.char)[0], 0.0)


class MadhuryaV2(unittest.TestCase):
    def test_the_rubric_is_symmetric_about_balance_and_anchored_to_4_62(self):
        cuts, anchor = md2.anchored_cuts()
        self.assertEqual(anchor["locus"], "4.62")
        self.assertEqual(cuts, [-anchor["madhurya"], -anchor["madhurya"] / 3, anchor["madhurya"] / 3, anchor["madhurya"]])
        self.assertEqual(MD2["cuts"], {"line": cuts, "poem": cuts})

    def test_the_index_is_version_1_1s(self):
        a, b = md2.score_poem(LINES, MD2), md.score_poem(LINES, md.load_baseline())
        self.assertEqual((a["madhurya"], a["inventory"], a["pileup"]), (b["madhurya"], b["inventory"], b["pileup"]))
        self.assertEqual(a["version"], "2.0")

    def test_the_texts_examples(self):
        cuts = MD2["cuts"]["poem"]
        m = {k: md.pooled(md.profile_poem(e["lines"])).index() for k, e in EXEMPLARS.items()}
        self.assertEqual(md.LABELS[md.level_of(m[md2.ANCHOR], cuts)], "soft")
        harsh = [k for k, e in EXEMPLARS.items() if e["pole"] == "harsh" and e["tier"] == "primary"]
        self.assertEqual(len(harsh), 5)
        self.assertTrue(all(md.level_of(m[k], cuts) == 0 for k in harsh))

    def test_no_corpus_statistic_enters_the_label(self):
        other = shifted(MD2, ("reference", "poem_index"), 0.5)
        a, b = md2.score_poem(LINES, MD2), md2.score_poem(LINES, other)
        self.assertEqual((a["madhurya"], a["label"]), (b["madhurya"], b["label"]))
        self.assertNotEqual(a["percentile"], b["percentile"])


class PrasadaV2(unittest.TestCase):
    def test_the_rubric_is_anchored_to_the_treatise(self):
        cuts, anchors = pr2.anchored_cuts(MODEL2)
        self.assertEqual((anchors["clear"]["locus"], anchors["obscure"]["locus"]), ("4.59", "4.15"))
        self.assertAlmostEqual(cuts[2] - cuts[1], (cuts[3] - cuts[0]) / 3, places=9)
        self.assertEqual(MODEL2.meta["cuts"], {"line": cuts, "poem": cuts})

    def test_both_form_defects_read_obscure(self):
        for eid in ("kas_4_5_aprayukta", "kas_4_15_apratita"):
            self.assertEqual(pr2.score_poem(EXEMPLARS[eid]["lines"], MODEL2)["label"], "obscure")
        self.assertEqual(pr2.score_poem(EXEMPLARS["kas_4_59_prasada"]["lines"], MODEL2)["label"], "leaning_clear")

    def test_the_surprisal_is_version_1s(self):
        self.assertEqual(pr2.score_poem(LINES, MODEL2)["surprisal"], pr.score_poem(LINES, pr.load_model())["surprisal"])

    def test_no_corpus_statistic_enters_the_label(self):
        meta = MODEL2.meta
        try:
            MODEL2.meta = {**meta, "reference": {**meta["reference"],
                                                 "poem_surprisal": [v + 1 for v in meta["reference"]["poem_surprisal"]]}}
            b = pr2.score_poem(LINES, MODEL2)
        finally:
            MODEL2.meta = meta
        a = pr2.score_poem(LINES, MODEL2)
        self.assertEqual((a["surprisal"], a["label"]), (b["surprisal"], b["label"]))
        self.assertNotEqual(a["percentile"], b["percentile"])


class Ladder(unittest.TestCase):
    def test_the_protocols_ladder_takes_any_metrics(self):
        rows = lambda values: [{"x": v} for v in values]                       # noqa: E731
        out = dp.ladder(rows([1.0] * 40), {1.0: rows([0.5] * 40)}, {"x": lambda r: r["x"]})
        self.assertEqual(out["x"]["verdict"], "declines")


if __name__ == "__main__":
    unittest.main()

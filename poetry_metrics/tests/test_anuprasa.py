"""Tests of the anuprāsa metric.

    cd poetry_metrics && python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import contextlib
import io
import json
import random
import statistics
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import anuprasa as ap                                               # noqa: E402
from common.phonology import Token, akshara_consonants, line_tokens  # noqa: E402

BASELINE = ap.load_baseline()


def line_z(text, level=ap.HEADLINE):
    return ap.line_stat(line_tokens(text)[1], ap.LEVELS[level], BASELINE["level_probs"][level]).z


class Phonology(unittest.TestCase):
    def test_homorganic_nasal_is_anusvara(self):
        self.assertEqual([t.char for t in line_tokens("సున్దర")[1]], [t.char for t in line_tokens("సుందర")[1]])

    def test_geminate_is_one_sound(self):
        self.assertEqual(akshara_consonants("ద్ద"), ("ద",))
        self.assertEqual(akshara_consonants("క్ష"), ("క", "ష"))

    def test_spaces_and_punctuation_do_not_matter(self):
        self.assertAlmostEqual(line_z("మందార మకరంద"), line_z("మందారమకరంద, !"))

    def test_arasunna_and_vowels_carry_no_token(self):
        self.assertEqual([t.char for t in line_tokens("ఆఁ ఇ ఉ")[1]], [])


class Statistic(unittest.TestCase):
    def test_moments_are_exact_under_the_chance_model(self):
        """E and V equal the simulated mean and variance of A for i.i.d. draws."""
        probs = {"a": 0.5, "b": 0.3, "c": 0.2}
        skeleton = [0, 1, 1, 2, 3, 3, 4, 5, 6, 7]         # akshara of each token; 1 and 3 are conjuncts
        stat = ap.line_stat([Token("a", a, "") for a in skeleton], lambda t: t.char, probs)
        rng = random.Random(0)
        draws = []
        for _ in range(40000):
            chars = rng.choices(list(probs), weights=list(probs.values()), k=len(skeleton))
            draws.append(ap.line_stat([Token(c, a, "") for c, a in zip(chars, skeleton)],
                                      lambda t: t.char, probs).observed)
        self.assertAlmostEqual(statistics.fmean(draws), stat.expected, delta=0.02 * stat.expected)
        self.assertAlmostEqual(statistics.pvariance(draws), stat.variance, delta=0.04 * stat.variance)

    def test_same_akshara_pairs_are_not_counted(self):
        stat = ap.line_stat([Token("a", 0, ""), Token("a", 0, "")], lambda t: t.char, {"a": 1.0})
        self.assertEqual((stat.pairs, stat.observed), (0, 0))
        self.assertIsNone(stat.z)

    def test_binomial_tail(self):
        self.assertAlmostEqual(ap.binomial_tail(2, 4, 0.5), 11 / 16)
        self.assertEqual(ap.binomial_tail(0, 4, 0.3), 1.0)


class Rubric(unittest.TestCase):
    def test_cut_points(self):
        self.assertEqual([ap.rubric(z) for z in (None, -1, 1.644, 1.645, 2.326, 3.09, 9)], [0, 0, 0, 1, 2, 3, 3])

    def test_heavy_alliteration_is_strong(self):
        # bhagavatam:6-33-క., a line in the corpus top ten (z = 8.61)
        self.assertGreaterEqual(line_z("కరికిఁ గరాగ్రస్థగిరికిఘనతరకిరికిన్."), 3.09)

    def test_no_repeats_is_none(self):
        z = line_z("కచటతప")
        self.assertLess(z, 0)
        self.assertEqual(ap.rubric(z), 0)

    def test_poem_score_is_the_mean_line_level(self):
        lines = ["కరికిఁ గరాగ్రస్థగిరికిఘనతరకిరికిన్.", "కచటతప", "రామ", "కళలు గలుగుఁ గాక; కమల తోడగుగాక;"]
        result = ap.score_poem(lines, BASELINE)
        levels = [l[ap.HEADLINE]["level"] for l in result["lines"]]
        self.assertAlmostEqual(result["score"], sum(levels) / len(levels), places=3)
        self.assertEqual(result["score"], result[ap.HEADLINE]["score"])

    def test_the_treatise_example_of_vrttyanuprasa(self):
        # Kāvyālaṅkārasaṅgrahamu 4.77 (1920 edition): క్ష carried through three lines
        lines = ["సమదవిపక్షశిక్షణవిచక్షణదక్షిణదోరనుక్షణ", "భ్రమదసిదుర్ణిరీక్షసమరక్షపితక్షితిపక్షతక్షర",
                 "త్సమధికశోణితక్షరకృతక్షణరక్షితపక్షిలోక నిన్", "గమలదళాక్షుఁ డేలు బలగౌరవసింహ నృసింహభూవరా."]
        result = ap.score_poem(lines, BASELINE)
        self.assertGreaterEqual(result["varna"]["z_percentile"], 95)
        self.assertEqual([l["varna"]["carriers"][0]["sound"] for l in result["lines"][:3]], ["ష"] * 3)

    def test_deterministic(self):
        lines = ["మందార మకరందమాధుర్యమునఁ దేలు-", "మధుపంబు వోవునేమదనములకు?"]
        self.assertEqual(json.dumps(ap.score_poem(lines, BASELINE)), json.dumps(ap.score_poem(lines, BASELINE)))


class Baseline(unittest.TestCase):
    def test_probabilities_sum_to_one(self):
        self.assertAlmostEqual(sum(BASELINE["probabilities"].values()), 1.0, places=5)
        for probs in BASELINE["level_probs"].values():
            self.assertAlmostEqual(sum(probs.values()), 1.0, places=5)

    def test_reference_quantiles_are_sorted(self):
        for level in ap.LEVELS:
            for qs in BASELINE["reference"][level].values():
                self.assertEqual(len(qs), 101)
                self.assertEqual(qs, sorted(qs))


class Cli(unittest.TestCase):
    def test_score_text(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            ap.main(["score", "--text", "కళలు గలుగుఁ గాక; కమల తోడగుగాక;\\nకచటతప", "--no-lines"])
        result = json.loads(out.getvalue())
        self.assertEqual(result["n_lines"], 2)
        self.assertIn(result["label"], ("none", "weak", "marked", "strong"))


if __name__ == "__main__":
    unittest.main()

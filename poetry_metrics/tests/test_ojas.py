"""Tests of the ojas metric.

    cd poetry_metrics && python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import ojas as oj                     # noqa: E402
import validation_ojas as vo          # noqa: E402

BASELINE = oj.load_baseline()
SCALE = BASELINE["scale"]


class Counts(unittest.TestCase):
    def test_words_aksharas_conjuncts_aspirates(self):
        c = oj.count_line("పక్షి రామభద్ర")
        self.assertEqual((c.words, c.word_aksharas, c.aksharas), (2, 6, 6))
        self.assertEqual(c.conjuncts, 2)                 # క్షి, ద్ర
        self.assertEqual(c.aspirates, 1)                 # భ
        self.assertEqual(c.word_length, 3.0)
        self.assertAlmostEqual(c.conjunct_rate, 100 * 2 / 6)

    def test_a_doubled_consonant_is_a_conjunct(self):
        self.assertEqual(oj.count_line("అక్క").conjuncts, 1)
        self.assertEqual(oj.count_line("అంద").conjuncts, 0)     # the anusvāra is a coda, not a conjunct

    def test_longest_words(self):
        c = oj.pooled(oj.count_poem(["మందారబిసకుంద రామ", "బృందారకాప్త"]))
        self.assertEqual(c.longest[0], (7, "మందారబిసకుంద"))
        self.assertEqual(len(c.longest), 3)

    def test_pooling_adds_counts(self):
        a, b = oj.count_line("పక్షి రామ"), oj.count_line("అక్క")
        t = a + b
        self.assertEqual((t.words, t.aksharas, t.conjuncts), (a.words + b.words, a.aksharas + b.aksharas, 2))


class Index(unittest.TestCase):
    def test_zero_at_the_reference_mean(self):
        c = oj.Counts(words=1000, word_aksharas=round(1000 * SCALE["word_length"]["mean"]),
                      aksharas=10000, conjuncts=round(100 * SCALE["conjunct_rate"]["mean"]))
        self.assertAlmostEqual(oj.index(c, SCALE), 0.0, places=2)

    def test_each_term_raises_it(self):
        base = oj.Counts(words=10, word_aksharas=40, aksharas=40, conjuncts=5)
        longer = oj.Counts(words=10, word_aksharas=60, aksharas=40, conjuncts=5)
        tighter = oj.Counts(words=10, word_aksharas=40, aksharas=40, conjuncts=15)
        self.assertGreater(oj.index(longer, SCALE), oj.index(base, SCALE))
        self.assertGreater(oj.index(tighter, SCALE), oj.index(base, SCALE))

    def test_one_standard_deviation_on_both_is_one(self):
        m, s = SCALE["word_length"], SCALE["conjunct_rate"]
        c = oj.Counts(words=1, word_aksharas=m["mean"] + m["sd"], aksharas=100, conjuncts=s["mean"] + s["sd"])
        self.assertAlmostEqual(oj.index(c, SCALE), 1.0)

    def test_empty(self):
        self.assertIsNone(oj.index(oj.Counts(), SCALE))

    def test_levels(self):
        cuts = [-1.0, -0.5, 0.5, 1.0]
        self.assertEqual([oj.level_of(v, cuts) for v in (-2, -1.0, 0, 0.5, 3)], [0, 1, 2, 3, 4])


class Classical(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mean = lambda t: sum(t) / len(t)
        cls.report = vo.contrasts_report(BASELINE, {"aspirate_rate": {
            "mean": mean(BASELINE["reference"]["poem_aspirate_rate"]), "sd": 3.0}})

    def test_every_contrast_is_in_the_texts_order(self):
        self.assertEqual(self.report["in_order"], "8/8")

    def test_compounds_without_tightness(self):
        # the treatise's ojas example: the longest words, almost no conjuncts
        ex = self.report["exemplars"]["kas_4_70_ojas"]
        self.assertGreater(ex["word_length"], 10)
        self.assertLess(ex["conjunct_rate"], 5)

    def test_aspirates_would_reverse_vamanas_pair(self):
        tight, slack = (oj.pooled(oj.count_poem(e["lines"])) for e in vo.vm.load_exemplars()
                        if e["id"] in ("vamana_3_1_5_gadha", "vamana_3_1_5_not"))
        self.assertGreater(oj.index(tight, SCALE), oj.index(slack, SCALE))
        self.assertLess(tight.aspirate_rate, slack.aspirate_rate)


class Output(unittest.TestCase):
    def test_poem(self):
        lines = ["మందారబిసకుందకుందాదినిధిబృంద,", "బృందారకాప్తశోభితయశుండు"]
        r = oj.score_poem(lines, BASELINE)
        self.assertEqual((r["label"], r["word_length"]), ("dense", 12.5))
        self.assertEqual(json.dumps(r), json.dumps(oj.score_poem(lines, BASELINE)))

    def test_baseline_is_consistent(self):
        for unit in ("line", "poem"):
            self.assertEqual(BASELINE["cuts"][unit], sorted(BASELINE["cuts"][unit]))
            self.assertEqual(len(BASELINE["reference"][f"{unit}_index"]), 101)
        self.assertAlmostEqual(BASELINE["reference"]["poem_index"][50], 0.0, delta=0.1)

    def test_cli(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            oj.main(["score", "--text", "నీ వాడిన నే నాడుదు\\nఅణిమాద్యష్టగుణప్రసిద్ధులు త్రిలోకారాధ్యు లుద్యద్వచో-"])
        result = json.loads(out.getvalue())
        self.assertEqual([l["label"] for l in result["lines"]], ["light", "dense"])


if __name__ == "__main__":
    unittest.main()

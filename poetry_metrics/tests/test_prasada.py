"""Tests of the prasāda metric (loading the model takes about two seconds).

    cd poetry_metrics && python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import contextlib
import io
import json
import math
import random
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import prasada as pr                       # noqa: E402
import validation_prasada as vp            # noqa: E402
from common.phonology import aksharas      # noqa: E402

MODEL = pr.load_model()
VERSE = ["పలికెడిది భాగవత మఁట,", "పలికించెడివాడు రామభద్రుం డఁట, నేఁ"]


def surprisal(lines):
    return pr.poem_figures(MODEL, lines)["surprisal"]


class Model(unittest.TestCase):
    def test_probabilities_sum_to_one(self):
        ids = list(MODEL.uni)
        h, g = MODEL.ids["ము"], MODEL.ids["రా"]
        for total in (sum(MODEL.p1(a) for a in ids) + MODEL.p1(None),
                      sum(MODEL.p2(h, a) for a in ids) + MODEL.p2(h, None),
                      sum(MODEL.p3(g, h, a) for a in ids) + MODEL.p3(g, h, None)):
            self.assertAlmostEqual(total, 1.0, places=6)

    def test_an_unseen_akshara_is_costly_but_finite(self):
        aks, bits = MODEL.bits("ఖ్ఫ్ఝృ")
        self.assertEqual(len(bits), len(aks))
        self.assertGreater(bits[0], 20)
        self.assertTrue(all(math.isfinite(b) for b in bits))

    def test_a_seen_context_lowers_surprisal(self):
        # ము after రా (as in రాముఁడు) is likelier than ము at large
        self.assertGreater(MODEL.p2(MODEL.ids["రా"], MODEL.ids["ము"]), MODEL.p1(MODEL.ids["ము"]))

    def test_order_of_the_model(self):
        line = "పలికెడిది భాగవత మఁట"
        means = [sum(MODEL.bits(line, order)[1]) / len(aksharas(line)) for order in (1, 2, 3)]
        self.assertEqual(means, sorted(means, reverse=True))          # each higher order predicts better

    def test_zipf(self):
        unseen = math.log10(1 / MODEL.word_scale) + 3
        self.assertAlmostEqual(MODEL.zipf("ఖ్ఫ్ఝృ"), unseen)
        self.assertGreater(MODEL.zipf("అని"), 5)                        # a very common word


class Clarity(unittest.TestCase):
    def test_spaces_do_not_matter(self):
        self.assertAlmostEqual(surprisal(["పలికెడిది భాగవత మఁట"]), surprisal(["పలికెడిదిభాగవతమఁట"]))

    def test_real_verse_is_clearer_than_its_shuffles(self):
        poem = type("P", (), {"lines": VERSE})
        rng = random.Random(0)
        real = surprisal(VERSE)
        self.assertLess(real, surprisal(vp.shuffled(poem, rng, "word")))
        self.assertLess(real, surprisal(vp.shuffled(poem, rng, "akshara")))

    def test_shuffles_keep_the_line_lengths(self):
        poem = type("P", (), {"lines": VERSE})
        out = vp.shuffled(poem, random.Random(0), "akshara")
        self.assertEqual([len(aksharas(l)) for l in out], [len(aksharas(l)) for l in VERSE])

    def test_nonsense_from_constrained_decoding_is_obscure(self):
        r = pr.score_poem(["మహ్యుగ్యున్రుత్య్య్మల్రుత్య్య్మల్రుత్", "కహ్యున్రుత్య్య్మల్ర్య్కల్రుత్య్య్మల్రుత్"], MODEL)
        self.assertEqual(r["label"], "obscure")
        self.assertEqual(r["known_word_share"], 0.0)

    def test_repetition_is_not_caught(self):
        """A language model is not surprised by repetition; this is a documented limit."""
        r = pr.score_poem(["మమమమమమమ మ జమమమమమ మ మమ మమమమము మమమమమ మమమమసమమును మ"], MODEL)
        self.assertNotEqual(r["label"], "obscure")

    def test_levels_run_from_obscure_to_clear(self):
        cuts = [5.0, 5.5, 6.5, 7.0]
        self.assertEqual([pr.level_of(h, cuts) for h in (4.0, 5.0, 6.0, 6.9, 7.0, 12.0)], [4, 3, 2, 1, 0, 0])
        self.assertIsNone(pr.level_of(None, cuts))


class Classical(unittest.TestCase):
    def test_every_contrast_is_in_the_texts_order(self):
        report = vp.contrasts_report(MODEL)
        self.assertEqual(report["in_order"], "5/5")
        self.assertEqual(report["exemplars"]["kas_4_5_aprayukta"]["label"], "obscure")


class Output(unittest.TestCase):
    def test_poem(self):
        r = pr.score_poem(VERSE, MODEL)
        self.assertEqual(json.dumps(r), json.dumps(pr.score_poem(VERSE, MODEL)))
        self.assertAlmostEqual(r["perplexity"], 2 ** r["surprisal"], delta=0.1)
        self.assertEqual(len(r["lines"][0]["hard_spots"]), 3)
        self.assertIn(r["label"], pr.LABELS)

    def test_baseline_is_consistent(self):
        meta = MODEL.meta
        self.assertEqual(meta["akshara_types"], len(MODEL.uni))
        self.assertEqual(meta["akshara_tokens"], sum(MODEL.uni.values()))
        for unit in ("line", "poem"):
            self.assertEqual(meta["cuts"][unit], sorted(meta["cuts"][unit]))

    def test_cli(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            pr.main(["score", "--text", "అని పలికి యంతకంతకుఁ\\nమహ్యుగ్యున్రుత్య్య్మల్రుత్య్య్మల్రుత్", "--no-lines"])
        result = json.loads(out.getvalue())
        self.assertEqual(result["n_lines"], 2)
        self.assertIn("surprisal", result)


if __name__ == "__main__":
    unittest.main()

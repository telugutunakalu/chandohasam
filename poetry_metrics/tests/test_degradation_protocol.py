"""Tests of the degradations and the verdict rule of the degradation protocol.

    cd poetry_metrics && python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import degradation_protocol as dp                   # noqa: E402
from indic_meter_dawg import scansion as sc         # noqa: E402

POEM = ["శ్రీరాముని దయచేతను", "నారూఢిగ సకల జనులు నౌరా యనగా", "ధారాళమైన నీతులు", "నోరూరగ జవులు పుట్ట నుడివెద సుమతీ"]


def aksharas(lines) -> int:
    return sum(len(sc.syllabify(line)) for line in lines)


class Degradations(unittest.TestCase):
    def test_word_shuffle_keeps_the_words_and_the_line_lengths(self):
        out = dp.word_shuffle(list(POEM), 1.0, random.Random(1))
        self.assertEqual(sorted(" ".join(out).split()), sorted(" ".join(POEM).split()))
        self.assertEqual([len(l.split()) for l in out], [len(l.split()) for l in POEM])
        self.assertNotEqual(out, POEM)

    def test_meter_break_edits_the_asked_share_of_aksharas(self):
        out = dp.meter_break(list(POEM), 0.10, random.Random(1))
        self.assertNotEqual(out, POEM)
        self.assertLessEqual(abs(aksharas(out) - aksharas(POEM)), round(0.10 * aksharas(POEM)))

    def test_vowel_length_changes(self):
        change = lambda text: dp.change_length(sc.syllabify(text)[0])       # noqa: E731
        self.assertEqual([change(t) for t in ("క", "కి", "కీ", "కా", "కం", "అ")], ["కా", "కీ", "కి", "క", "కాం", "ఆ"])
        self.assertIsNone(change("ఐ"))

    def test_filler_keeps_the_akshara_count_of_each_word(self):
        out = dp.filler(list(POEM), 1.0, random.Random(1))
        self.assertEqual(aksharas(out), aksharas(POEM))
        self.assertEqual(len(set("".join(out).replace(" ", ""))), 1)

    def test_synonym_swap_replaces_units_by_their_gloss(self):
        units = [("పుట్టన్", "పుట్టలో"), ("శరంబునన్", "రెల్లుపొదలో"), ("అంభస్", "జల"), ("యాన", "ప్రయాణ")]
        self.assertEqual(dp.synonym_swap(units, 2, 0, random.Random(1)), ["పుట్టన్ శరంబునన్", "అంభస్ యాన"])
        self.assertEqual(dp.synonym_swap(units, 2, 1.0, random.Random(1)), ["పుట్టలో రెల్లుపొదలో", "జల ప్రయాణ"])

    def test_gloss_units_drop_notes_in_brackets(self):
        record = {"teeka_pairs": [{"word": "పుట్ట", "meaning": "పుట్ట లేదు (వాల్మీకిని కాదు)"},
                                  {"word": "పాత్రంబునన్", "meaning": "సాధనములో - పడవలో"}, {"word": "x", "meaning": ""}]}
        self.assertEqual(dp.gloss_units(record), [("పుట్ట", "పుట్ట లేదు"), ("పాత్రంబునన్", "సాధనములో")])


class Verdict(unittest.TestCase):
    def rows(self, values):
        return [{"anuprasa_varga_z": v, "madhurya": v, "ojas": v, "surprisal": -v, "chandas_skill": v} for v in values]

    def test_a_metric_that_falls_at_every_step_declines(self):
        base = self.rows([1.0] * 40)
        out = dp.ladder(base, {0.5: self.rows([0.8] * 40), 1.0: self.rows([0.5] * 40)})
        self.assertEqual({m: v["verdict"] for m, v in out.items()}, {m: "declines" for m in dp.METRICS})
        self.assertEqual(out["chandas"]["steps"][-1]["lower_pct"], 100.0)

    def test_a_metric_that_goes_up_rises_and_an_unchanged_one_does_not_respond(self):
        base = self.rows([1.0] * 40)
        self.assertEqual(dp.ladder(base, {1.0: self.rows([2.0] * 40)})["ojas"]["verdict"], "rises")
        self.assertEqual(dp.ladder(base, {1.0: self.rows([1.0] * 40)})["ojas"]["verdict"], "no response")

    def test_a_fall_with_a_step_up_is_not_monotone(self):
        base = self.rows([1.0] * 40)
        out = dp.ladder(base, {0.5: self.rows([0.2] * 40), 1.0: self.rows([0.5] * 40)})
        self.assertEqual(out["madhurya"]["verdict"], "declines, not monotone")


if __name__ == "__main__":
    unittest.main()

"""Tests of the anuprāsa v3 metric (repeated consonant n-grams across the whole poem).

    cd poetry_metrics && python3 -m unittest tests.test_anuprasa_v3 -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import anuprasa_v3 as v3  # noqa: E402


class ConsonantSequence(unittest.TestCase):
    def test_vowels_are_skipped(self):
        # అ (vowel-only akshara) contributes no consonant symbol
        seq = v3.consonant_sequence(["అ క అ క"])
        self.assertEqual(seq, ["క", "క"])

    def test_spaces_do_not_matter(self):
        self.assertEqual(v3.consonant_sequence(["కల కల"]), v3.consonant_sequence(["కలకల"]))

    def test_whole_poem_not_per_line(self):
        # a pattern split across two lines still counts, unlike the per-line v1/v2 statistic
        together = v3.consonant_sequence(["కలకలమని", "కలకలమని"])
        self.assertEqual(len(together), 2 * len(v3.consonant_sequence(["కలకలమని"])))


class AnuprasaScore(unittest.TestCase):
    def test_no_repetition_scores_zero(self):
        s = v3.anuprasa_score(["రాముడు వనమున కేగెను", "సీతమ్మ వెంట నడచెను"])
        # distinct consonants throughout (if any pair happens to coincide, A stays small)
        self.assertLess(s["A"], v3.A_STAR / 3)

    def test_heavy_repetition_scores_strong(self):
        s = v3.anuprasa_score(["కలకలమని కలకలమని", "చెలరేగె చెలరేగె గాలి"])
        self.assertGreaterEqual(s["A"], v3.A_STAR)
        self.assertEqual(v3.level_of(s["A"]), 3)

    def test_longest_repeated_ngram_is_consistent(self):
        s = v3.anuprasa_score(["కలకలమని కలకలమని"])
        # K is the longest n with a repeat; no (K+1)-gram should repeat
        seq = v3.consonant_sequence(["కలకలమని కలకలమని"])
        from collections import Counter
        grams_next = Counter(tuple(seq[i:i + s["K"] + 1]) for i in range(len(seq) - s["K"]))
        self.assertTrue(all(c == 1 for c in grams_next.values()))

    def test_empty_poem(self):
        s = v3.anuprasa_score([])
        self.assertEqual(s, dict(A=0.0, K=0, n_c=0, repeats=[]))

    def test_each_extra_occurrence_counts_once(self):
        # sequence [క, గ, క]: only the 1-gram క repeats (c=2), contributing 1*(2-1)/3;
        # a different consonant in between keeps the 2-gram from also repeating
        s = v3.anuprasa_score(["క అ గ అ క"])
        self.assertAlmostEqual(s["A"], 1 / 3)
        self.assertEqual(s["K"], 1)


class Rubric(unittest.TestCase):
    def test_cuts_are_thirds_of_a_star(self):
        self.assertAlmostEqual(v3.CUTS[0], v3.A_STAR / 3)
        self.assertAlmostEqual(v3.CUTS[1], 2 * v3.A_STAR / 3)
        self.assertAlmostEqual(v3.CUTS[2], v3.A_STAR)

    def test_level_boundaries(self):
        self.assertEqual(v3.level_of(0.0), 0)
        self.assertEqual(v3.level_of(v3.CUTS[0]), 1)
        self.assertEqual(v3.level_of(v3.CUTS[1]), 2)
        self.assertEqual(v3.level_of(v3.CUTS[2]), 3)

    def test_score_poem_matches_level_label(self):
        result = v3.score_poem(["కలకలమని కలకలమని"])
        self.assertEqual(result["label"], v3.LABELS[result["level"]])
        self.assertEqual(result["score"], result["level"])


if __name__ == "__main__":
    unittest.main()

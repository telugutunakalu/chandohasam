# -*- coding: utf-8 -*-
"""symbols.py — alphabet and notation normalisation."""
import random
import unittest

from imd_support import imd
from indic_meter_dawg import symbols as sy


class TestNormalize(unittest.TestCase):
    CASES = {
        "UIIUIU": "UIIUIU",
        "UII UIU": "UIIUIU",
        "UII, UIU": "UIIUIU",
        "UII/UIU": "UIIUIU",
        "GLLGLG": "UIIUIU",
        "-uu-u-": "UIIUIU",
        "—˘˘—˘—": "UIIUIU",
        "గలలగలగ": "UIIUIU",
        "U||U|U": "UIIUIU",
        "SIISIS": "UIIUIU",
        "  U I I\tU I U \n": "UIIUIU",
        "": "",
    }

    def test_every_notation_normalises_to_canonical(self):
        for raw, want in self.CASES.items():
            with self.subTest(raw=raw):
                self.assertEqual(sy.normalize(raw), want)

    def test_unknown_symbol_raises(self):
        for bad in ("UIX", "UI2", "U.I", "ఉ", "UI?"):
            with self.subTest(bad=bad):
                with self.assertRaises(sy.NotationError):
                    sy.normalize(bad)

    def test_notation_error_is_value_error(self):
        self.assertTrue(issubclass(sy.NotationError, ValueError))

    def test_idempotent_on_canonical(self):
        rng = random.Random(7)
        for _ in range(500):
            s = "".join(rng.choice("UI") for _ in range(rng.randint(0, 30)))
            self.assertEqual(sy.normalize(s), s)
            self.assertTrue(sy.is_canonical(s))

    def test_normalize_lines_drops_empty(self):
        self.assertEqual(sy.normalize_lines(["UI U", "", "  ", "II I"]), ("UIU", "III"))
        self.assertEqual(sy.normalize_lines([]), ())

    def test_package_reexports(self):
        self.assertIs(imd.normalize, sy.normalize)
        self.assertIs(imd.NotationError, sy.NotationError)


class TestWeights(unittest.TestCase):
    def test_matras(self):
        for pat, want in (("U", 2), ("I", 1), ("UII", 4), ("UUU", 6), ("III", 3), ("", 0), ("IIIIU", 6)):
            with self.subTest(pat=pat):
                self.assertEqual(sy.matras(pat), want)

    def test_alphabet_constants(self):
        self.assertEqual(sy.ALPHABET, ("U", "I"))
        self.assertEqual(sy.MATRAS, {"U": 2, "I": 1, "\n": 0})
        self.assertEqual(sy.POEM_ALPHABET, ("U", "I", "\n"))
        self.assertEqual(sy.display("UI\nUI"), "UI⏎UI")

    def test_is_all_laghu(self):
        self.assertTrue(sy.is_all_laghu("III"))
        self.assertFalse(sy.is_all_laghu("IIU"))
        self.assertFalse(sy.is_all_laghu(""))

    def test_flip_final_laghu(self):
        self.assertEqual(sy.flip_final_laghu("UIUI"), "UIUU")
        self.assertEqual(sy.flip_final_laghu("UIUU"), "UIUU")
        self.assertEqual(sy.flip_final_laghu("I"), "U")
        self.assertEqual(sy.flip_final_laghu(""), "")

    def test_telugu_notation_roundtrip(self):
        rng = random.Random(3)
        for _ in range(200):
            s = "".join(rng.choice("UI") for _ in range(rng.randint(1, 20)))
            self.assertEqual(sy.normalize(sy.telugu_notation(s)), s)


class TestPatternsWithMatras(unittest.TestCase):
    def test_counts_follow_fibonacci(self):
        # number of U/I strings worth n matras is F(n+1): 1, 2, 3, 5, 8, 13, 21
        want = [1, 2, 3, 5, 8, 13, 21, 34]
        for n, w in enumerate(want, start=1):
            with self.subTest(n=n):
                self.assertEqual(len(sy.patterns_with_matras(n)), w)

    def test_every_pattern_has_the_right_weight_and_is_unique(self):
        for n in range(1, 9):
            pats = sy.patterns_with_matras(n)
            self.assertEqual(len(set(pats)), len(pats))
            for p in pats:
                self.assertEqual(sy.matras(p), n)

    def test_ordering_short_first(self):
        self.assertEqual(sy.patterns_with_matras(4), ("UU", "IIU", "IUI", "UII", "IIII"))

    def test_zero_and_negative(self):
        self.assertEqual(sy.patterns_with_matras(0), ())
        self.assertEqual(sy.patterns_with_matras(-1), ())


if __name__ == "__main__":
    unittest.main()

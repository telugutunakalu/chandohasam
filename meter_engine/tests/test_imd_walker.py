# -*- coding: utf-8 -*-
"""walker.py — acceptance, pādānta rule, death points, viable prefixes."""
import random
import unittest

from imd_support import dawg, imd, language, mutate
from indic_meter_dawg import grammar as gr
from indic_meter_dawg import walker as wk

D = dawg()


class TestAcceptance(unittest.TestCase):
    def test_random_lines_accepted_with_their_hypothesis(self):
        rng = random.Random(21)
        for h, g in D.grammars.items():
            for _ in range(60):
                line = gr.random_line(g, rng)
                r = wk.walk(line, D)
                with self.subTest(h=h, line=line):
                    self.assertIn(h, r.accepted)
                    self.assertNotIn(h, r.died)
                    self.assertEqual(r.line, line)

    def test_accepted_set_equals_slot_languages(self):
        rng = random.Random(22)
        for h, g in D.grammars.items():
            for _ in range(30):
                line = gr.random_line(g, rng)
                want = frozenset(k for k in D.hypotheses if line in language(*k))
                with self.subTest(h=h, line=line):
                    self.assertEqual(wk.walk(line, D, final_laghu_as_guru=False).accepted, want)

    def test_notation_is_normalised(self):
        r = wk.walk("గలల గలగ లలల గలల గలల గలగ లగ", D)
        self.assertIn(("utpalamala", "all"), r.accepted)

    def test_vritta_mutation_dies_at_the_mutated_akshara(self):
        rng = random.Random(23)
        for m in D.catalogue.concrete:
            if not m.is_fixed:
                continue
            g = D.grammars[(m.name, "all")]
            line = gr.canonical_line(g)
            for _ in range(10):
                i = rng.randrange(len(line))
                bad = line[:i] + ("U" if line[i] == "I" else "I") + line[i + 1:]
                r = wk.walk(bad, D, final_laghu_as_guru=False)
                with self.subTest(m=m.name, i=i):
                    self.assertNotIn((m.name, "all"), r.accepted)
                    self.assertEqual(r.died[(m.name, "all")], i)

    def test_prefix_of_a_line_dies_at_end(self):
        line = gr.canonical_line(D.grammars[("utpalamala", "all")])
        r = wk.walk(line[:-3], D)
        self.assertEqual(r.died[("utpalamala", "all")], len(line) - 3)

    def test_death_points_skipped_when_asked(self):
        r = wk.walk("UIUI", D, with_death_points=False)
        self.assertEqual(r.died, {})

    def test_meters_property(self):
        r = wk.walk("UUUUUUUU", D)
        self.assertEqual(r.meters, frozenset({"vidyunmala", "madhuragati_ragada"}))   # UU UU UU UU is also 4 x m4


class TestPadanta(unittest.TestCase):
    def test_final_laghu_read_as_guru_for_vrittas(self):
        for m in D.catalogue.concrete:
            if not m.is_fixed:
                continue
            h = (m.name, "all")
            line = gr.canonical_line(D.grammars[h])
            self.assertTrue(line.endswith("U"))
            r = wk.walk(line[:-1] + "I", D)
            with self.subTest(m=m.name):
                self.assertIn(h, r.padanta_accepted)
                self.assertNotIn(h, r.accepted)
                self.assertTrue(r.needs_padanta(h))
                self.assertIn(h, r.all_accepted)

    def test_padanta_can_be_switched_off(self):
        line = gr.canonical_line(D.grammars[("utpalamala", "all")])[:-1] + "I"
        r = wk.walk(line, D, final_laghu_as_guru=False)
        self.assertEqual(r.padanta_accepted, frozenset())
        self.assertNotIn(("utpalamala", "all"), r.all_accepted)

    def test_padanta_never_applies_to_lines_ending_in_guru(self):
        rng = random.Random(24)
        for h, g in D.grammars.items():
            for _ in range(20):
                line = gr.random_line(g, rng)
                if line.endswith("U"):
                    self.assertEqual(wk.walk(line, D).padanta_accepted, frozenset())

    def test_padanta_and_accepted_are_disjoint(self):
        rng = random.Random(25)
        for h, g in D.grammars.items():
            for _ in range(20):
                line = mutate(gr.random_line(g, rng), rng)
                r = wk.walk(line, D)
                self.assertFalse(r.accepted & r.padanta_accepted)


class TestLattice(unittest.TestCase):
    def test_as_options(self):
        self.assertEqual(wk.as_options("UI I"), ("U", "I", "I"))
        self.assertEqual(wk.as_options(["U", "IU", "UI"]), ("U", "IU", "UI"))
        self.assertEqual(wk.as_options(["G", "L"]), ("U", "I"))
        self.assertEqual(wk.canonical(("U", "IU", "UI")), "UIU")
        with self.assertRaises(Exception):
            wk.as_options(["U", "X"])
        with self.assertRaises(Exception):
            wk.as_options(["UU"])

    def test_plain_options_equal_walk(self):
        rng = random.Random(28)
        for h, g in D.grammars.items():
            for _ in range(10):
                line = gr.random_line(g, rng)
                a = wk.walk(line, D)
                b = wk.walk_options(list(line), D)
                with self.subTest(h=h, line=line):
                    self.assertEqual(a.accepted, b.accepted)
                    self.assertEqual(a.padanta_accepted, b.padanta_accepted)
                    self.assertEqual(b.witness[h], line)
                    self.assertEqual(b.pattern_for(h), line)

    def test_lattice_accepts_union_of_readings(self):
        import itertools
        rng = random.Random(29)
        for h, g in D.grammars.items():
            line = gr.random_line(g, rng)
            opts = [c + ("I" if c == "U" else "U") if rng.random() < 0.3 else c for c in line]
            r = wk.walk_options(opts, D, final_laghu_as_guru=False)
            readings = ["".join(p) for p in itertools.product(*opts)]
            union = frozenset().union(*(wk.walk(s, D, final_laghu_as_guru=False).accepted for s in readings))
            with self.subTest(h=h):
                self.assertEqual(r.accepted, union)
                self.assertIn(h, r.accepted)
                for hyp, pat in r.witness.items():
                    self.assertIn(pat, readings)
                    self.assertIn(hyp, wk.walk(pat, D, final_laghu_as_guru=False).accepted)

    def test_canonical_reading_wins_ties(self):
        r = wk.walk_options(["U", "UI", "U", "U", "U", "U", "U", "U"], D)
        self.assertEqual(r.witness[("vidyunmala", "all")], "UUUUUUUU")
        self.assertEqual(r.line, "UUUUUUUU")

    def test_padanta_in_lattice(self):
        line = gr.canonical_line(D.grammars[("sragvini", "all")])
        r = wk.walk_options(list(line[:-1]) + ["I"], D)
        self.assertIn(("sragvini", "all"), r.padanta_accepted)
        self.assertEqual(r.pattern_for(("sragvini", "all")), line)
        r = wk.walk_options(list(line[:-1]) + ["I"], D, final_laghu_as_guru=False)
        self.assertNotIn(("sragvini", "all"), r.all_accepted)

    def test_empty(self):
        self.assertEqual(wk.walk_options([], D).accepted, frozenset())


class TestViablePrefix(unittest.TestCase):
    def test_empty_prefix_keeps_everything(self):
        self.assertEqual(wk.viable_prefix("", D), frozenset(D.hypotheses))

    def test_every_prefix_of_a_valid_line_keeps_its_hypothesis(self):
        rng = random.Random(26)
        for h, g in D.grammars.items():
            line = gr.random_line(g, rng)
            for k in range(len(line) + 1):
                with self.subTest(h=h, k=k):
                    self.assertIn(h, wk.viable_prefix(line[:k], D))

    def test_monotone_shrinking(self):
        rng = random.Random(27)
        for _ in range(200):
            line = "".join(rng.choice("UI") for _ in range(37))
            prev = wk.viable_prefix("", D)
            for k in range(1, 38):
                cur = wk.viable_prefix(line[:k], D)
                self.assertTrue(cur <= prev)
                prev = cur

    def test_dead_prefix(self):
        self.assertEqual(wk.viable_prefix("I" * 37, D), frozenset())
        self.assertEqual(wk.next_symbols("I" * 37, D), {})

    def test_next_symbols_consistent(self):
        for prefix in ("", "U", "UI", "UUUUUUU", "IIII", "UIIUIU"):
            ns = wk.next_symbols(prefix, D)
            for a, hs in ns.items():
                with self.subTest(prefix=prefix, a=a):
                    self.assertEqual(hs, wk.viable_prefix(prefix + a, D))
            union = frozenset().union(*ns.values()) if ns else frozenset()
            self.assertEqual(union, wk.viable_prefix(prefix, D))

    def test_after_seven_gurus(self):
        vid, mad = ("vidyunmala", "all"), ("madhuragati_ragada", "all")
        self.assertEqual(wk.viable_prefix("UUUUUUU", D), frozenset({vid, mad}))
        ns = wk.next_symbols("UUUUUUU", D)
        self.assertEqual(ns["U"], frozenset({vid, mad}))          # UUUUUUUU: మ మ గా / గా గా గా గా
        self.assertEqual(ns["I"], frozenset({mad}))               # UUUUUUUI I: గా గా గా భ
        self.assertEqual(wk.viable_prefix("UUUUUUUII", D), frozenset({mad}))

    def test_reexports(self):
        self.assertIs(imd.walk, wk.walk)
        self.assertIs(imd.viable_prefix, wk.viable_prefix)


if __name__ == "__main__":
    unittest.main()

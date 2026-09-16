# -*- coding: utf-8 -*-
"""stanza.py — line counts, slot patterns, stanza constraints."""
import random
import unittest

from imd_support import dawg, random_stanza
from indic_meter_dawg import grammar as gr
from indic_meter_dawg import stanza as st
from indic_meter_dawg.walker import walk

D = dawg()
CAT = D.catalogue


def walks(lines):
    return [walk(ln, D) for ln in lines]


class TestLineSlots(unittest.TestCase):
    def test_fixed_count(self):
        self.assertEqual(st.line_slots(CAT.get("ataveladi"), 4), ("odd", "even", "odd", "even"))
        self.assertIsNone(st.line_slots(CAT.get("ataveladi"), 8))
        self.assertIsNone(st.line_slots(CAT.get("kandamu"), 3))
        self.assertIsNone(st.line_slots(CAT.get("kandamu"), 0))

    def test_repeatable(self):
        dv = CAT.get("dvipada")
        for n in (2, 4, 6, 10):
            self.assertEqual(st.line_slots(dv, n), ("all",) * n)
        for n in (1, 3, 5):
            self.assertIsNone(st.line_slots(dv, n))
        self.assertEqual(st.line_slots(CAT.get("turagagati_ragada"), 8), ("all",) * 8)


class TestMatchStanza(unittest.TestCase):
    def test_random_stanzas_match_their_meter(self):
        rng = random.Random(41)
        for m in CAT.concrete:
            for _ in range(30):
                lines = random_stanza(m.name, rng)
                sm = st.match_stanza(m, walks(lines))
                with self.subTest(m=m.name, lines=lines):
                    self.assertIsNotNone(sm)
                    self.assertEqual(sm.meter, m.name)
                    self.assertEqual(sm.slots, m.slot_pattern)
                    self.assertEqual(sm.units, 1)
                    self.assertEqual(sm.padanta_lines, ())
                    self.assertEqual(sm.violations, ())
                    self.assertIsNone(st.stanza_failure(m, walks(lines)))

    def test_repeatable_units(self):
        rng = random.Random(42)
        for name in ("dvipada", "madhuragati_ragada", "turagagati_ragada"):
            m = CAT.get(name)
            lines = random_stanza(name, rng, units=3)
            sm = st.match_stanza(m, walks(lines))
            self.assertIsNotNone(sm)
            self.assertEqual(sm.units, 3)
            self.assertEqual(len(sm.slots), 3 * m.padalu)

    def test_wrong_line_count(self):
        rng = random.Random(43)
        lines = random_stanza("tetagiti", rng)[:3]
        self.assertIsNone(st.match_stanza(CAT.get("tetagiti"), walks(lines)))
        f = st.stanza_failure(CAT.get("tetagiti"), walks(lines))
        self.assertEqual(f[0], 0)
        self.assertIsNone(f[1])
        self.assertIn("line count 3 is not 4", f[2])
        f = st.stanza_failure(CAT.get("dvipada"), walks(lines))
        self.assertIn("multiple of 2", f[2])

    def test_slot_pattern_enforced(self):
        # two ataveladi odd lines in even position: not ataveladi
        rng = random.Random(44)
        odd = gr.random_line(D.grammars[("ataveladi", "odd")], rng)
        while odd in {s for s, _ in __import__("indic_meter_dawg.automaton", fromlist=["x"]).enumerate_language(D.slot_dfas[("ataveladi", "even")])}:
            odd = gr.random_line(D.grammars[("ataveladi", "odd")], rng)
        self.assertIsNone(st.match_stanza(CAT.get("ataveladi"), walks([odd, odd, odd, odd])))
        f = st.stanza_failure(CAT.get("ataveladi"), walks([odd, odd, odd, odd]))
        self.assertEqual(f[0], 1)
        self.assertIn("slot even", f[2])

    def test_kanda_first_akshara_rule(self):
        # valid kanda lines: odd starts with U, even starts with I
        odd_u = "UU" + "UU" + "UU"                          # గా గా గా
        even_i = "IIII" + "IIII" + "IUI" + "IIII" + "IIU"    # నల నల జ నల స  (18)
        even_u = "UU" + "IIII" + "IUI" + "IIII" + "IIU"      # గా నల జ నల స   (16)
        clean = st.match_stanza(CAT.get("kandamu"), walks([odd_u, even_u, odd_u, even_u]))
        self.assertEqual(clean.violations, ())
        mixed = st.match_stanza(CAT.get("kandamu"), walks([odd_u, even_i, odd_u, even_u]))
        self.assertIsNotNone(mixed)                       # soft: matched, with the breach recorded
        self.assertEqual(len(mixed.violations), 1)
        self.assertIn("first_akshara_weight_uniform", mixed.violations[0])
        self.assertIsNone(st.stanza_failure(CAT.get("kandamu"), walks([odd_u, even_i, odd_u, even_u])))

    def test_padanta_lines_reported(self):
        line = gr.canonical_line(D.grammars[("sragvini", "all")])
        lines = [line, line[:-1] + "I", line, line[:-1] + "I"]
        sm = st.match_stanza(CAT.get("sragvini"), walks(lines))
        self.assertEqual(sm.padanta_lines, (1, 3))

    def test_failure_points_at_the_broken_akshara(self):
        line = gr.canonical_line(D.grammars[("utpalamala", "all")])
        bad = line[:7] + ("U" if line[7] == "I" else "I") + line[8:]
        f = st.stanza_failure(CAT.get("utpalamala"), walks([line, line, bad, line]))
        self.assertEqual(f[0], 2)
        self.assertEqual(f[1], 7)
        self.assertIn("breaks at akshara 8", f[2])

    def test_short_line_failure(self):
        line = gr.canonical_line(D.grammars[("utpalamala", "all")])
        f = st.stanza_failure(CAT.get("utpalamala"), walks([line, line[:-2], line, line]))
        self.assertEqual(f[0], 1)
        self.assertIn("ends too early", f[2])


if __name__ == "__main__":
    unittest.main()

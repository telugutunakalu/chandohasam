# -*- coding: utf-8 -*-
"""prosody.py — the hierarchical prosodic grammar, its flattening, and
the prosodic automaton, checked against the identifier's oracle."""
import random
import unittest

import indic_meter_dawg
from imd_support import dawg, mutate, oracle_meters, random_stanza
from indic_meter_dawg import automaton as au
from indic_meter_dawg import prosody as pgm
assert not callable(pgm), "indic_meter_dawg.prosody must be the module, not the function"
from indic_meter_dawg import symbols as sy
from indic_meter_dawg.grammar import derivation, is_right_linear, is_strict, to_strict

D = dawg()
CAT = D.catalogue
PG = {m.name: pgm.prosodic_grammar(m, D) for m in CAT.concrete}
FL = {m.name: pgm.flatten(m, D) for m in CAT.concrete}


class TestHierarchy(unittest.TestCase):
    def test_four_levels_and_start(self):
        for name, pg in PG.items():
            with self.subTest(m=name):
                self.assertEqual(pg.start, "Poem")
                self.assertEqual(list(pg.levels), ["poem", "line", "class", "gana"])
                self.assertIn("Poem", pg.levels["poem"])
                self.assertTrue(pg.levels["line"])
                self.assertTrue(pg.levels["gana"])
                self.assertEqual(pg.terminals, ("U", "I", "\n"))

    def test_grammar_is_closed(self):
        """Every symbol on a right-hand side is a terminal or has rules."""
        for name, pg in PG.items():
            nts = set(pg.nonterminals)
            for r in pg.rules:
                for s in r.rhs:
                    with self.subTest(m=name, rule=r.format()):
                        self.assertTrue(pg.is_terminal(s) or s in nts, s)
            self.assertTrue(all(pg.rules_of(nt) for nt in nts))

    def test_level_shapes(self):
        for name, pg in PG.items():
            with self.subTest(m=name):
                for nt in pg.levels["gana"]:
                    for r in pg.rules_of(nt):
                        self.assertTrue(all(s in ("U", "I") for s in r.rhs))
                        self.assertEqual("".join(r.rhs), D.registry.by_telugu.get(nt, D.registry.gana_for_pattern("".join(r.rhs))).pattern)
                for nt in pg.levels["class"]:
                    for r in pg.rules_of(nt):
                        self.assertEqual(len(r.rhs), 1)
                        self.assertIn(r.rhs[0], pg.levels["gana"])
                for nt in pg.levels["line"]:
                    for r in pg.rules_of(nt):
                        self.assertTrue(all(s in pg.levels["class"] or s in pg.levels["gana"] for s in r.rhs))
                        self.assertNotIn("\n", r.rhs)
                for nt in pg.levels["poem"]:
                    for r in pg.rules_of(nt):
                        self.assertTrue(all(s == "\n" or s in pg.levels["line"] or s in pg.levels["poem"] for s in r.rhs))

    def test_poem_rule_has_the_right_number_of_lines(self):
        for m in CAT.concrete:
            pg = PG[m.name]
            stanza_rules = [r for nt in pg.levels["poem"] for r in pg.rules_of(nt) if "\n" in r.rhs and "Poem" not in r.rhs]
            with self.subTest(m=m.name):
                self.assertTrue(stanza_rules)
                for r in stanza_rules:
                    self.assertEqual(r.rhs.count("\n"), m.padalu - 1)
                    self.assertEqual(len(r.rhs), 2 * m.padalu - 1)

    def test_tetagiti_reads_like_the_textbook(self):
        pg = PG["tetagiti"]
        self.assertEqual([r.format() for r in pg.rules_of("Poem")], ["Poem → Line ⏎ Line ⏎ Line ⏎ Line"])
        self.assertEqual([r.format() for r in pg.rules_of("Line")], ["Line → Surya Indra Indra Surya Surya"])
        self.assertEqual([r.rhs[0] for r in pg.rules_of("Surya")], ["న", "హ"])
        self.assertEqual([r.rhs[0] for r in pg.rules_of("Indra")], ["భ", "ర", "త", "నల", "నగ", "సల"])
        self.assertEqual([r.format() for r in pg.rules_of("భ")], ["భ → U I I"])

    def test_fixed_meter_has_no_classes(self):
        pg = PG["utpalamala"]
        self.assertEqual(pg.levels["class"], ())
        self.assertEqual([r.format() for r in pg.rules_of("Line")], ["Line → భ ర న భ భ ర వ"])

    def test_kanda_constraints_and_stanza_rule_in_names(self):
        pg = PG["kandamu"]
        self.assertEqual([r.rhs[0] for r in pg.rules_of("Poem")], ["Poem⟨U⟩", "Poem⟨I⟩"])
        self.assertIn("Line_even⟨U⟩", pg.levels["line"])
        self.assertEqual([r.format() for r in pg.rules_of("Line_even⟨U⟩")],
                         ["Line_even⟨U⟩ → Kanda⟨U⟩ Kanda−జ Kanda=జ|నల Kanda−జ Kanda$U"])
        self.assertEqual([r.rhs[0] for r in pg.rules_of("Kanda=జ|నల")], ["జ", "నల"])
        self.assertEqual([r.rhs[0] for r in pg.rules_of("Kanda$U")], ["స", "గా"])
        self.assertEqual([r.rhs[0] for r in pg.rules_of("Kanda⟨U⟩")], ["భ", "గా"])
        self.assertEqual([r.rhs[0] for r in pg.rules_of("Kanda−జ⟨I⟩")], ["స", "నల"])

    def test_seesamu_all_laghu_line(self):
        pg = PG["seesamu"]
        self.assertEqual([r.format() for r in pg.rules_of("Line_laghu")], ["Line_laghu → నలల నలల నలల నలల నలల నలల న న"])

    def test_repeatable_poem_is_right_recursive(self):
        pg = PG["dvipada"]
        self.assertEqual([r.format() for r in pg.rules_of("Poem")], ["Poem → Unit", "Poem → Unit ⏎ Poem"])
        self.assertEqual([r.format() for r in pg.rules_of("Unit")], ["Unit → Line ⏎ Line"])

    def test_matra_meter_classes(self):
        pg = PG["madhuragati_ragada"]
        self.assertEqual([r.format() for r in pg.rules_of("Line")], ["Line → M4 M4 M4 M4"])
        self.assertEqual(len(pg.rules_of("M4")), 5)

    def test_class_and_line_names(self):
        k = CAT.get("kandamu")
        self.assertEqual(pgm.class_name(k, "odd", 1), "Kanda−జ")
        self.assertEqual(pgm.class_name(k, "odd", 2), "Kanda")
        self.assertEqual(pgm.class_name(k, "even", 5, "I"), "Kanda$U⟨I⟩")
        self.assertIsNone(pgm.class_name(CAT.get("utpalamala"), "all", 1))
        self.assertEqual(pgm.line_name(k, "odd"), "Line_odd")
        self.assertEqual(pgm.line_name(CAT.get("tetagiti"), "all"), "Line")
        self.assertEqual(pgm.class_base_name("all_laghu(surya)"), "Surya_laghu")

    def test_format_has_level_headers(self):
        text = pgm.format_prosodic_grammar(PG["ataveladi"])
        for h in ("# poem", "# lines", "# gana classes", "# ganas → symbols"):
            self.assertIn(h, text)
        self.assertIn("Poem → Line_odd ⏎ Line_even ⏎ Line_odd ⏎ Line_even", text)


class TestDerivation(unittest.TestCase):
    def test_random_poems_are_accepted_by_the_identifier_and_oracle(self):
        rng = random.Random(61)
        for m in CAT.concrete:
            for _ in range(40):
                lines = pgm.random_poem(PG[m.name], rng)
                with self.subTest(m=m.name, lines=lines):
                    self.assertIn(m.name, oracle_meters(lines, final_laghu_as_guru=False))
                    self.assertTrue(pgm.accepts_poem(m.name, lines))
                    self.assertIsNotNone(derivation(FL[m.name], "\n".join(lines)))

    def test_random_poem_line_counts(self):
        rng = random.Random(62)
        for m in CAT.concrete:
            for _ in range(10):
                n = len(pgm.random_poem(PG[m.name], rng, max_units=3))
                with self.subTest(m=m.name):
                    if m.repeatable:
                        self.assertIn(n, {m.padalu, 2 * m.padalu, 3 * m.padalu})
                    else:
                        self.assertEqual(n, m.padalu)

    def test_derivation_steps(self):
        rng = random.Random(63)
        for m in CAT.concrete:
            lines = pgm.random_poem(PG[m.name], rng, max_units=1)
            steps = pgm.derivation_steps(PG[m.name], lines)
            with self.subTest(m=m.name):
                self.assertIsNotNone(steps)
                self.assertEqual(steps[0], "Poem")
                self.assertEqual(steps[-1].replace(" ", ""), sy.display("\n".join(lines)))
                self.assertGreater(len(steps), 3)

    def test_derivation_steps_rejects_non_member(self):
        self.assertIsNone(pgm.derivation_steps(PG["vidyunmala"], ["UUUUUUUU"] * 3))
        self.assertIsNone(pgm.derivation_steps(PG["vidyunmala"], ["UUUUUUUI"] * 4))


class TestFlattening(unittest.TestCase):
    def test_flat_grammar_is_right_linear_over_the_poem_alphabet(self):
        for name, fl in FL.items():
            with self.subTest(m=name):
                self.assertEqual(fl.alphabet, sy.POEM_ALPHABET)
                self.assertTrue(is_right_linear(fl))
                self.assertEqual(fl.start, "Poem")
                st = to_strict(fl)
                self.assertTrue(is_strict(st))
                self.assertTrue(all(p.comment for p in st.productions))

    def test_nonterminal_naming(self):
        fl = FL["tetagiti"]
        self.assertEqual(fl.nonterminals[:3], ("Poem", "L1.G2", "L1.G3"))
        self.assertIn("L4.G5", fl.nonterminals)
        self.assertNotIn("L1.G1", fl.nonterminals)          # Poem plays that role
        self.assertIn("L1.G1", FL["dvipada"].nonterminals)  # the loop target of a repeatable meter
        self.assertIn("⟨U⟩L1.G2", FL["kandamu"].nonterminals)

    def test_line_breaks_only_at_line_ends(self):
        for name, fl in FL.items():
            m = CAT.get(name)
            n_ganas = {slot: len(m.slots[slot]) for slot in m.slots}
            for p in fl.productions:
                with self.subTest(m=name, p=p.format()):
                    if "\n" in p.terminals:
                        self.assertTrue(p.terminals.endswith("\n"))
                        self.assertEqual(p.terminals.count("\n"), 1)
                        self.assertTrue(p.rhs is not None and p.rhs.endswith(".G1"))

    def test_vidyunmala_flat(self):
        self.assertEqual([p.format() for p in FL["vidyunmala"].productions][:3],
                         ["Poem → UUU L1.G2", "L1.G2 → UUU L1.G3", "L1.G3 → UU⏎ L2.G1"])
        self.assertEqual(FL["vidyunmala"].productions[-1].format(), "L4.G3 → UU")

    def test_repeatable_last_gana_may_loop(self):
        fl = FL["dvipada"]
        last = [p for p in fl.productions if p.lhs == "L2.G4"]
        self.assertTrue(any(p.rhs is None for p in last))
        self.assertTrue(any(p.rhs == "L1.G1" and p.terminals.endswith("\n") for p in last))


class TestPoemAutomaton(unittest.TestCase):
    def test_equals_oracle_on_random_mutated_and_junk(self):
        rng = random.Random(64)
        for m in CAT.concrete:
            for _ in range(30):
                lines = random_stanza(m.name, rng)
                if rng.random() < 0.5:
                    i = rng.randrange(len(lines))
                    lines[i] = mutate(lines[i], rng)
                with self.subTest(m=m.name, lines=lines):
                    self.assertEqual(pgm.accepts_poem(m.name, lines),
                                     m.name in oracle_meters(lines, final_laghu_as_guru=False))
        for _ in range(200):
            n = rng.choice([2, 4, 4, 6])
            lines = ["".join(rng.choice("UI") for _ in range(rng.randint(6, 30))) for _ in range(n)]
            want = oracle_meters(lines, final_laghu_as_guru=False)
            for m in CAT.concrete:
                self.assertEqual(pgm.accepts_poem(m.name, lines), m.name in want)

    def test_line_count(self):
        v = ["UUUUUUUU"]
        self.assertTrue(pgm.accepts_poem("vidyunmala", v * 4))
        self.assertFalse(pgm.accepts_poem("vidyunmala", v * 3))
        self.assertFalse(pgm.accepts_poem("vidyunmala", v * 5))
        rng = random.Random(65)
        for units in (1, 2, 3):
            self.assertTrue(pgm.accepts_poem("dvipada", random_stanza("dvipada", rng, units=units)))
        self.assertFalse(pgm.accepts_poem("dvipada", random_stanza("dvipada", rng, units=2)[:3]))

    def test_kanda_stanza_rule_is_inside_the_automaton(self):
        ok = ["UIIIUIUII", "UUIIIIIUIUUIIU", "UUIIIIUII", "UUUIIIUIUIIUU"]
        self.assertTrue(pgm.accepts_poem("kandamu", ok))
        mixed = ["IIUUIIUU"] + ok[1:]            # స భ గా: a valid odd line, but it starts with a laghu
        from imd_support import language
        self.assertTrue(all(ln in language("kandamu", s) for ln, s in zip(mixed, ("odd", "even", "odd", "even"))))
        self.assertFalse(pgm.accepts_poem("kandamu", mixed))
        even_i = "IIU" + "IIII" + "IUI" + "IIII" + "IIU"          # స నల జ నల స
        self.assertTrue(pgm.accepts_poem("kandamu", ["IIUUIIUU", even_i, "IIUUIIUU", even_i]))

    def test_minimal_and_cached(self):
        for m in CAT.concrete:
            d = pgm.prosodic_automaton(m.name)
            with self.subTest(m=m.name):
                self.assertIs(d, pgm.prosodic_automaton(m.name))
                self.assertEqual(d.alphabet, sy.POEM_ALPHABET)
                self.assertEqual(au.minimize(d, keep_labels=False).n_states, d.n_states)
                self.assertEqual(au.is_acyclic(d), not m.repeatable)

    def test_fixed_meter_prosodic_automaton_is_a_chain(self):
        d = pgm.prosodic_automaton("vidyunmala")
        self.assertEqual(d.n_states, 4 * 8 + 3 + 1)     # 32 symbols + 3 separators + start


if __name__ == "__main__":
    unittest.main()

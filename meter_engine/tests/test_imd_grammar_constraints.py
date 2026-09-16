# -*- coding: utf-8 -*-
"""grammar.py + constraints.py — right-linear grammars per meter, both forms."""
import itertools
import random
import unittest

from imd_support import dawg, expected_counts
from indic_meter_dawg import catalogue as ct
from indic_meter_dawg import constraints as cs
from indic_meter_dawg import ganas as gn
from indic_meter_dawg import grammar as gr
from indic_meter_dawg.catalogue import Constraint

CAT = ct.load_catalogue()
REG = gn.load_registry()
GRAMMARS = gr.all_grammars(CAT.concrete, REG)


class TestConstraints(unittest.TestCase):
    def test_kanda_alternatives(self):
        k = CAT.get("kandamu")
        self.assertEqual([len(a) for a in gr.slot_alternatives(k, "odd", REG)], [4, 5, 4])
        self.assertEqual([len(a) for a in gr.slot_alternatives(k, "even", REG)], [5, 4, 2, 4, 2])

    def test_kanda_rules_visible_in_grammar(self):
        odd = GRAMMARS[("kandamu", "odd")]
        even = GRAMMARS[("kandamu", "even")]
        self.assertNotIn("IUI", [p.terminals for p in odd.productions_of("G1")])
        self.assertNotIn("IUI", [p.terminals for p in odd.productions_of("G3")])
        self.assertIn("IUI", [p.terminals for p in odd.productions_of("G2")])
        self.assertNotIn("IUI", [p.terminals for p in even.productions_of("G2")])
        self.assertNotIn("IUI", [p.terminals for p in even.productions_of("G4")])
        self.assertEqual({p.terminals for p in even.productions_of("G3")}, {"IUI", "IIII"})
        self.assertEqual({p.terminals for p in even.productions_of("G5")}, {"IIU", "UU"})

    def test_seesamu_laghu_slot_uses_nalala(self):
        g = GRAMMARS[("seesamu", "laghu")]
        self.assertEqual([p.terminals for p in g.productions], ["IIIII"] * 6 + ["III"] * 2)
        self.assertEqual(gr.derive(g), {"I" * 36})

    def test_constraint_that_empties_a_position_raises(self):
        alts = [REG.resolve("kanda")] * 3
        c = Constraint(rule="require_gana", slot="odd", positions=(2,), ganas=("మ",))
        with self.assertRaises(cs.ConstraintError):
            cs.apply_constraints(alts, [c], "odd", REG)

    def test_unknown_rule_raises(self):
        with self.assertRaises(cs.ConstraintError):
            cs.apply_constraints([REG.resolve("kanda")], [Constraint(rule="x", slot="a")], "a", REG)
        with self.assertRaises(cs.ConstraintError):
            cs.check_stanza(["UI"], [Constraint(rule="x", slot="*")])

    def test_constraints_only_apply_to_their_slot(self):
        alts = [REG.resolve("kanda")] * 3
        c = Constraint(rule="forbid_gana", slot="even", positions=(1,), ganas=("జ",))
        self.assertEqual([len(a) for a in cs.apply_constraints(alts, [c], "odd", REG)], [5, 5, 5])

    def test_line_ends_with_laghu(self):
        alts = [REG.resolve("kanda")]
        c = Constraint(rule="line_ends_with", slot="a", weight="I")
        self.assertEqual({g.pattern for g in cs.apply_constraints(alts, [c], "a", REG)[0]}, {"UII", "IUI", "IIII"})

    def test_describe(self):
        self.assertEqual(cs.describe(Constraint(rule="forbid_gana", slot="odd", positions=(1, 3), ganas=("జ",))),
                         "in the odd lines, gana 1 and gana 3 may not be జ")
        self.assertEqual(cs.describe(Constraint(rule="require_gana", slot="even", positions=(3,), ganas=("జ", "నల"))),
                         "in the even lines, gana 3 must be జ or నల")
        self.assertEqual(cs.describe(Constraint(rule="line_ends_with", slot="all", weight="U")),
                         "in every line, the last akshara must be a guru")
        self.assertIn("same weight", cs.describe(Constraint(rule="first_akshara_weight_uniform", slot="*")))

    def test_check_stanza(self):
        c = Constraint(rule="first_akshara_weight_uniform", slot="*")
        self.assertEqual(cs.check_stanza(["UII", "UI", "UUU"], [c]), ())
        self.assertEqual(cs.check_stanza(["III", "IU"], [c]), ())
        msgs = cs.check_stanza(["UII", "II"], [c])
        self.assertEqual(len(msgs), 1)
        self.assertIn("first_akshara_weight_uniform", msgs[0])
        self.assertEqual(cs.check_stanza(["UII", "II"], []), ())


class TestGrammarForms(unittest.TestCase):
    def test_one_grammar_per_concrete_slot(self):
        want = {(m.name, s) for m in CAT.concrete for s in m.slots}
        self.assertEqual(set(GRAMMARS), want)
        self.assertEqual(len(GRAMMARS), 40)

    def test_every_grammar_is_right_linear_and_strict_form_is_strict(self):
        for h, g in GRAMMARS.items():
            with self.subTest(h=h):
                self.assertTrue(gr.is_right_linear(g))
                self.assertFalse(gr.is_strict(g) and any(len(p.terminals) > 1 for p in g.productions))
                s = gr.to_strict(g)
                self.assertTrue(gr.is_strict(s))
                self.assertEqual(s.form, "strict")
                self.assertEqual(s.start, g.start)
                self.assertIs(gr.to_strict(s), s)

    def test_nonterminal_naming(self):
        g = GRAMMARS[("tetagiti", "all")]
        self.assertEqual(g.nonterminals, ("G1", "G2", "G3", "G4", "G5"))
        self.assertEqual(g.start, "G1")
        s = gr.to_strict(g)
        self.assertIn("G2_UII_1", s.nonterminals)
        self.assertIn("G2_UII_2", s.nonterminals)
        self.assertNotIn("G2_UII_3", s.nonterminals)

    def test_last_gana_has_terminal_only_productions(self):
        for h, g in GRAMMARS.items():
            last = g.nonterminals[-1]
            with self.subTest(h=h):
                self.assertTrue(all(p.rhs is None for p in g.productions_of(last)))
                for nt in g.nonterminals[:-1]:
                    self.assertTrue(all(p.rhs is not None for p in g.productions_of(nt)))

    def test_strict_and_gana_level_derive_the_same_language(self):
        for h, g in GRAMMARS.items():
            with self.subTest(h=h):
                self.assertEqual(gr.derive(g), gr.derive(gr.to_strict(g)))

    def test_language_sizes_match_regression_fixture(self):
        sizes = expected_counts()["slot_language_sizes"]
        for (m, s), g in GRAMMARS.items():
            with self.subTest(h=(m, s)):
                self.assertEqual(len(gr.derive(g)), sizes[f"{m}/{s}"])

    def test_no_two_gana_sequences_spell_the_same_line(self):
        # product of alternative counts equals the number of distinct strings for every meter
        for h, g in GRAMMARS.items():
            with self.subTest(h=h):
                self.assertEqual(gr.language_size(g), len(gr.derive(g)))

    def test_fixed_meters_are_singletons(self):
        for m in CAT.concrete:
            if m.is_fixed:
                self.assertEqual(len(gr.derive(GRAMMARS[(m.name, "all")])), 1)

    def test_derive_brute_force_agrees(self):
        for h in (("tetagiti", "all"), ("ataveladi", "odd"), ("kandamu", "even"), ("utsahamu", "all")):
            g = GRAMMARS[h]
            brute = {"".join(x.pattern for x in combo) for combo in itertools.product(*g.gana_positions)}
            with self.subTest(h=h):
                self.assertEqual(gr.derive(g), brute)

    def test_derivation_reproduces_lines(self):
        rng = random.Random(11)
        for h, g in GRAMMARS.items():
            for _ in range(20):
                line = gr.random_line(g, rng)
                steps = gr.derivation(g, line)
                with self.subTest(h=h, line=line):
                    self.assertIsNotNone(steps)
                    self.assertEqual("".join(p.terminals for p in steps), line)
                    self.assertEqual(steps[0].lhs, g.start)
                    self.assertIsNone(steps[-1].rhs)
                    for a, b in zip(steps, steps[1:]):
                        self.assertEqual(a.rhs, b.lhs)

    def test_derivation_rejects_non_members(self):
        g = GRAMMARS[("vidyunmala", "all")]
        self.assertIsNone(gr.derivation(g, "UUUUUUUI"))
        self.assertIsNone(gr.derivation(g, "UUUUUUU"))
        self.assertIsNone(gr.derivation(g, "UUUUUUUUU"))

    def test_random_and_canonical_lines_are_members(self):
        rng = random.Random(5)
        for h, g in GRAMMARS.items():
            lang = gr.derive(g)
            with self.subTest(h=h):
                self.assertIn(gr.canonical_line(g), lang)
                for _ in range(50):
                    self.assertIn(gr.random_line(g, rng), lang)

    def test_format_grammar_lists_every_production(self):
        g = GRAMMARS[("dvipada", "all")]
        text = gr.format_grammar(g)
        self.assertEqual(len(text.splitlines()), len(g.productions))
        self.assertIn("# భ bha", text)
        grouped = gr.format_grammar_grouped(g)
        self.assertEqual(len(grouped.splitlines()), len(g.nonterminals))
        self.assertTrue(grouped.startswith("G1 → UII G2 | UIU G2"))

    def test_production_format(self):
        self.assertEqual(gr.Production("G1", "UII", "G2").format(), "G1 → UII G2")
        self.assertEqual(gr.Production("G3", "UU", None).format(), "G3 → UU")
        self.assertEqual(gr.Production("G3", "", None).format("->"), "G3 -> ε")

    def test_grammar_names(self):
        self.assertEqual(GRAMMARS[("kandamu", "odd")].name, "kandamu__odd")
        self.assertEqual(GRAMMARS[("kandamu", "odd")].terminals, ("U", "I"))

    def test_strict_productions_are_all_commented(self):
        s = gr.to_strict(GRAMMARS[("tetagiti", "all")])
        self.assertTrue(all(p.comment for p in s.productions))
        by = {p.lhs + "→" + p.terminals + "→" + str(p.rhs): p.comment for p in s.productions}
        self.assertEqual(by["G2_UUI_2→I→G3"], "త ta: symbol 3/3, complete → G3")
        self.assertEqual(by["G2→U→G2_UII_1"], "భ bha: symbol 1/3 read, 2 to go")
        self.assertEqual(s.productions_of("G2")[0].comment.split(":")[0], "భ bha")

    def test_dawg_holds_the_same_grammars(self):
        d = dawg()
        self.assertEqual(set(d.grammars), set(GRAMMARS))
        for h in GRAMMARS:
            self.assertEqual(d.grammars[h].productions, GRAMMARS[h].productions)


if __name__ == "__main__":
    unittest.main()

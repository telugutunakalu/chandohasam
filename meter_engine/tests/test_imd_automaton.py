# -*- coding: utf-8 -*-
"""automaton.py — NFA/DFA algebra on toy grammars and on every meter slot."""
import itertools
import unittest

from imd_support import dawg, expected_counts
from indic_meter_dawg import automaton as au
from indic_meter_dawg import catalogue as ct
from indic_meter_dawg import ganas as gn
from indic_meter_dawg import grammar as gr

CAT = ct.load_catalogue()
REG = gn.load_registry()


def toy(prods, start="S"):
    """Build a strict grammar from ``[(lhs, terminal, rhs_or_None), ...]``."""
    nts = []
    for lhs, _, rhs in prods:
        for x in (lhs, rhs):
            if x and x not in nts:
                nts.append(x)
    return gr.Grammar(meter="toy", slot="t", form="strict", start=start, nonterminals=tuple(nts),
                      productions=tuple(gr.Production(l, t, r) for l, t, r in prods))


class TestToyAutomata(unittest.TestCase):
    def setUp(self):
        # language {UI, UU}
        self.g = toy([("S", "U", "A"), ("A", "I", None), ("A", "U", None)])
        self.nfa = au.nfa_from_strict_grammar(self.g, "x")
        self.dfa = au.determinize(self.nfa)

    def test_nfa_shape(self):
        self.assertEqual(self.nfa.n_states, 3)
        self.assertEqual(len(self.nfa.edges), 3)
        self.assertEqual(self.nfa.start, {0})
        self.assertEqual(list(self.nfa.accept.values()), ["x"])
        self.assertEqual({e.weight for e in self.nfa.edges if e.symbol == "U"}, {2})
        self.assertEqual({e.weight for e in self.nfa.edges if e.symbol == "I"}, {1})

    def test_non_strict_grammar_rejected(self):
        bad = gr.Grammar(meter="toy", slot="t", form="gana", start="S", nonterminals=("S",),
                         productions=(gr.Production("S", "UI", None),))
        with self.assertRaises(ValueError):
            au.nfa_from_strict_grammar(bad, "x")
        with self.assertRaises(ValueError):
            au.nfa_from_strict_grammar(gr.Grammar(meter="t", slot="t", form="strict", start="S", nonterminals=("S",),
                                                  productions=(gr.Production("S", "UI", None),)), "x")

    def test_dfa_accepts_exactly_the_language(self):
        for s in ("UI", "UU"):
            self.assertTrue(au.accepts(self.dfa, s))
            self.assertEqual(au.labels_of(self.dfa, s), frozenset({"x"}))
        for s in ("", "U", "I", "UIU", "IU", "UUU"):
            self.assertFalse(au.accepts(self.dfa, s))
            self.assertEqual(au.labels_of(self.dfa, s), frozenset())

    def test_death_index(self):
        self.assertIsNone(au.death_index(self.dfa, "UI"))
        self.assertEqual(au.death_index(self.dfa, "IU"), 0)
        self.assertEqual(au.death_index(self.dfa, "UIU"), 2)
        self.assertEqual(au.death_index(self.dfa, "U"), 1)      # ran out of input in a non-accepting state

    def test_counts_and_enumeration(self):
        self.assertTrue(au.is_acyclic(self.dfa))
        self.assertEqual(au.count_paths(self.dfa), 2)
        self.assertEqual({s for s, _ in au.enumerate_language(self.dfa)}, {"UI", "UU"})
        self.assertEqual(au.max_depth(self.dfa), 2)

    def test_union_keeps_labels_apart(self):
        g2 = toy([("S", "I", "A"), ("A", "I", None)])          # {II}
        big = au.union([self.nfa, au.nfa_from_strict_grammar(g2, "y")])
        d = au.determinize(big)
        self.assertEqual(au.labels_of(d, "UI"), frozenset({"x"}))
        self.assertEqual(au.labels_of(d, "II"), frozenset({"y"}))
        self.assertEqual(au.count_paths(d), 3)
        self.assertEqual(au.coreachable_labels(d)[d.start], frozenset({"x", "y"}))

    def test_shared_string_gets_both_labels(self):
        g2 = toy([("S", "U", "A"), ("A", "I", None)])          # {UI}
        d = au.determinize(au.union([self.nfa, au.nfa_from_strict_grammar(g2, "y")]))
        self.assertEqual(au.labels_of(d, "UI"), frozenset({"x", "y"}))
        self.assertEqual(au.labels_of(d, "UU"), frozenset({"x"}))

    def test_minimize_merges_equivalent_states(self):
        # two branches spelling the same suffix: U I U and I I U -> after the first symbol the tails merge
        g = toy([("S", "U", "A"), ("S", "I", "B"), ("A", "I", "C"), ("B", "I", "D"), ("C", "U", None), ("D", "U", None)])
        d = au.determinize(au.nfa_from_strict_grammar(g, "x"))
        m = au.minimize(d)
        self.assertLess(m.n_states, d.n_states)
        self.assertEqual(m.n_states, 4)
        self.assertTrue(au.language_equal(d, m))

    def test_minimize_without_labels_merges_across_labels(self):
        g2 = toy([("S", "U", "A"), ("A", "U", None)])          # {UU}, label y; {UI,UU} label x
        d = au.determinize(au.union([self.nfa, au.nfa_from_strict_grammar(g2, "y")]))
        labeled = au.minimize(d, keep_labels=True)
        plain = au.minimize(d, keep_labels=False)
        self.assertLessEqual(plain.n_states, labeled.n_states)
        self.assertTrue(au.language_equal(d, plain, compare_labels=False))
        self.assertFalse(au.language_equal(d, plain, compare_labels=True))

    def test_trim_removes_dead_states(self):
        dead = au.Dfa(start=0, transitions={0: {"U": 1, "I": 2}, 1: {}, 2: {"U": 3}, 3: {}},
                      labels={0: frozenset(), 1: frozenset({"x"}), 2: frozenset(), 3: frozenset()}, n_states=4)
        t = au.trim(dead)
        self.assertEqual(t.n_states, 2)
        self.assertTrue(au.accepts(t, "U"))
        self.assertFalse(au.accepts(t, "IU"))

    def test_trim_empty_language(self):
        d = au.Dfa(start=0, transitions={0: {"U": 1}, 1: {}}, labels={0: frozenset(), 1: frozenset()}, n_states=2)
        t = au.trim(d)
        self.assertEqual(t.n_states, 1)
        self.assertEqual(au.count_paths(t), 0)

    def test_language_equal_negative(self):
        g2 = toy([("S", "U", "A"), ("A", "I", None)])
        d2 = au.determinize(au.nfa_from_strict_grammar(g2, "x"))
        self.assertFalse(au.language_equal(self.dfa, d2))
        self.assertFalse(au.language_equal(d2, self.dfa))

    def test_cyclic_dfa_detected(self):
        cyc = au.Dfa(start=0, transitions={0: {"U": 0, "I": 1}, 1: {}}, labels={0: frozenset(), 1: frozenset({"x"})}, n_states=2)
        self.assertFalse(au.is_acyclic(cyc))
        with self.assertRaises(ValueError):
            au.count_paths(cyc)
        self.assertEqual({s for s, _ in au.enumerate_language(cyc, max_len=3)}, {"I", "UI", "UUI"})
        m = au.minimize(cyc)
        self.assertEqual(m.n_states, 2)
        self.assertTrue(au.accepts(m, "UUUUI"))

    def test_edges_and_run(self):
        self.assertEqual(self.dfa.n_edges, 3)
        self.assertEqual(sorted((e.symbol, e.weight) for e in self.dfa.edges()), [("I", 1), ("U", 2), ("U", 2)])
        self.assertEqual(au.run(self.dfa, ""), self.dfa.start)
        self.assertIsNone(au.run(self.dfa, "I"))


class TestEverySlot(unittest.TestCase):
    """Determinize + minimize each slot and compare with the grammar."""

    def setUp(self):
        self.grammars = gr.all_grammars(CAT.concrete, REG)

    def test_dfa_language_equals_grammar_language(self):
        for h, g in self.grammars.items():
            d = au.determinize(au.nfa_from_strict_grammar(gr.to_strict(g), h))
            with self.subTest(h=h):
                self.assertTrue(au.is_acyclic(d))
                self.assertEqual({s for s, _ in au.enumerate_language(d)}, gr.derive(g))
                self.assertEqual(au.count_paths(d), len(gr.derive(g)))

    def test_minimized_slot_dfas_are_minimal_and_equivalent(self):
        d = dawg()
        for h, g in self.grammars.items():
            raw = au.determinize(au.nfa_from_strict_grammar(gr.to_strict(g), h))
            m = d.slot_dfas[h]
            with self.subTest(h=h):
                self.assertTrue(au.language_equal(raw, m, compare_labels=False))
                self.assertLessEqual(m.n_states, raw.n_states)
                self.assertEqual(au.minimize(m, keep_labels=False).n_states, m.n_states)
                self.assertTrue(_no_equivalent_pair(m))

    def test_state_sets_explain_determinized_states(self):
        g = self.grammars[("tetagiti", "all")]
        n = au.nfa_from_strict_grammar(gr.to_strict(g), "t")
        d = au.determinize(n)
        self.assertIsNotNone(d.state_sets)
        self.assertEqual(d.state_sets[d.start], frozenset(n.start))
        self.assertTrue(all(n.info[s].nonterminal for st in d.state_sets.values() for s in st))


def _no_equivalent_pair(dfa: au.Dfa) -> bool:
    """Brute-force check: every pair of states is distinguished by some string."""
    n = dfa.n_states
    dist = [[False] * n for _ in range(n)]
    for i, j in itertools.combinations(range(n), 2):
        if dfa.is_accepting(i) != dfa.is_accepting(j):
            dist[i][j] = dist[j][i] = True
    changed = True
    while changed:
        changed = False
        for i, j in itertools.combinations(range(n), 2):
            if dist[i][j]:
                continue
            for a in ("U", "I"):
                x, y = dfa.step(i, a), dfa.step(j, a)
                if (x is None) != (y is None) or (x is not None and dist[x][y]):
                    dist[i][j] = dist[j][i] = True
                    changed = True
                    break
    return all(dist[i][j] for i, j in itertools.combinations(range(n), 2))


if __name__ == "__main__":
    unittest.main()

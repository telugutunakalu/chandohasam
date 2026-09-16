# -*- coding: utf-8 -*-
"""builder.py — the compiled DAWG reproduces the regression numbers and
agrees with the per-slot automata (language equality, not sampling)."""
import collections
import itertools
import unittest
from functools import lru_cache

from imd_support import dawg, expected_counts, imd
from indic_meter_dawg import automaton as au
from indic_meter_dawg import builder as bd


@lru_cache(maxsize=1)
def full_language():
    """(string -> label set) for the whole DAWG; computed once."""
    return dict(au.enumerate_language(dawg().dfa))


class TestStats(unittest.TestCase):
    def test_headline_numbers_match_fixture(self):
        want = expected_counts()["stats"]
        got = dawg().stats()
        for k in ("meters", "hypotheses", "nfa_states", "dfa_states_unminimized", "dfa_states", "dfa_edges",
                  "distinct_lines", "acyclic", "max_line_length"):
            with self.subTest(k=k):
                self.assertEqual(got[k], want[k])

    def test_hypotheses_cover_every_slot(self):
        d = dawg()
        want = {(m.name, s) for m in d.catalogue.concrete for s in m.slots}
        self.assertEqual(set(d.hypotheses), want)
        self.assertEqual(set(d.slot_dfas), want)
        self.assertEqual(set(d.strict_grammars), want)

    def test_dawg_is_acyclic_and_minimal(self):
        d = dawg()
        self.assertTrue(au.is_acyclic(d.dfa))
        self.assertEqual(au.minimize(d.dfa).n_states, d.dfa.n_states)
        self.assertLess(d.dfa.n_states, d.unminimized_states)

    def test_default_dawg_is_cached(self):
        self.assertIs(bd.default_dawg(), bd.default_dawg())
        self.assertIs(imd.default_dawg, bd.default_dawg)

    def test_reachable_from_start_is_everything(self):
        d = dawg()
        self.assertEqual(d.reachable[d.dfa.start], frozenset(d.hypotheses))

    def test_every_state_is_live(self):
        d = dawg()
        for s in range(d.dfa.n_states):
            self.assertTrue(d.reachable[s], f"state {s} cannot reach an accept state")

    def test_spec_lookup(self):
        self.assertEqual(dawg().spec("kandamu").padalu, 4)


class TestLanguageAgreement(unittest.TestCase):
    def test_unminimized_and_minimized_accept_the_same_labelled_language(self):
        raw = bd.build_line_dawg(minimize=False)
        self.assertTrue(au.language_equal(raw.dfa, dawg().dfa, compare_labels=True))

    def test_slot_language_sizes(self):
        sizes = expected_counts()["slot_language_sizes"]
        for h, d in dawg().slot_dfas.items():
            with self.subTest(h=h):
                self.assertEqual(au.count_paths(d), sizes[f"{h[0]}/{h[1]}"])

    def test_labels_agree_with_slot_automata(self):
        """For every line of the DAWG, label h present <=> slot DFA h accepts."""
        d = dawg()
        lang = full_language()
        by_label = collections.Counter()
        for s, labels in lang.items():
            for h in labels:
                by_label[h] += 1
        for h, sd in d.slot_dfas.items():
            with self.subTest(h=h):
                self.assertEqual(by_label[h], au.count_paths(sd))
        # spot check the reverse direction on a sample of strings per slot
        for h, sd in d.slot_dfas.items():
            for s, _ in itertools.islice(au.enumerate_language(sd), 300):
                self.assertIn(h, lang[s])

    def test_total_and_ambiguity_counts(self):
        exp = expected_counts()
        lang = full_language()
        self.assertEqual(len(lang), exp["total_lines"])
        amb = sum(1 for labels in lang.values() if len({m for m, _ in labels}) > 1)
        self.assertEqual(amb, exp["ambiguous_lines"])

    def test_confusable_pairs(self):
        exp = expected_counts()["confusable_pairs"]
        pairs = collections.Counter()
        for labels in full_language().values():
            ms = sorted({m for m, _ in labels})
            for a, b in itertools.combinations(ms, 2):
                pairs[f"{a}|{b}"] += 1
        self.assertEqual(dict(pairs), exp)

    def test_seesam_taruvoja_is_the_dominant_confusion(self):
        exp = expected_counts()["confusable_pairs"]
        top = max(exp, key=exp.get)
        self.assertEqual(top, "seesamu|taruvoja")

    def test_vrittas_never_collide_with_each_other(self):
        d = dawg()
        fixed = {m.name for m in d.catalogue.concrete if m.is_fixed}
        for s, labels in full_language().items():
            ms = {m for m, _ in labels if m in fixed}
            self.assertLessEqual(len(ms), 1, s)

    def test_max_line_length_is_36(self):
        self.assertEqual(max(len(s) for s in full_language()), 36)       # sarvalaghu seesam: 6 నలల + 2 న


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""The DAWG demo must show what the engine does: same accept sets, same
pādānta, same verdict as ``chandohasam.analyze``.

    cd webapp && .venv/bin/python -m unittest test_dawg_demo -v
"""
from __future__ import annotations

import unittest

import dawg_demo as dd
from indic_meter_dawg import default_dawg
from indic_meter_dawg.walker import walk_options
from meter_engine.chandohasam import analyze

BROKEN = "పలికెడిది భాగవత మఁట,\nపలికించెడివాడు రామభద్రుం డఁట, నేఁ\nబలికిన భవహర మగునఁట,\nపలికెద వేఱొండు గాథ"


class GraphTest(unittest.TestCase):
    def test_every_edge_points_forward(self):
        g = dd.graph_payload()
        depth = {n["id"]: n["depth"] for n in g["nodes"]}
        self.assertEqual(len(g["nodes"]), default_dawg().dfa.n_states)
        self.assertTrue(all(depth[d] > depth[s] for s, _, d in g["edges"]))

    def test_start_reaches_every_hypothesis(self):
        g = dd.graph_payload()
        self.assertEqual(len(g["nodes"][g["start"]]["reach"]), len(g["hypotheses"]))


class TraceTest(unittest.TestCase):
    def check(self, text):
        dawg = default_dawg()
        hyps = dawg.hypotheses
        tr = dd.trace_payload(text)
        for u in tr["units"]:
            w = walk_options(tuple(a["options"] for a in u["aksharas"]), dawg=dawg)
            self.assertEqual({hyps[i] for i in u["accepted"]}, set(w.accepted), u["text"])
            pad = {hyps[i] for i in u["padanta"]["accepted"]} if u["padanta"] else set()
            self.assertEqual(pad, set(w.padanta_accepted), u["text"])
            # each step moves along real DFA edges
            for st in u["steps"]:
                for s, sym, d in st["edges"]:
                    self.assertEqual(dawg.dfa.step(s, sym), d)
        a = analyze(text)
        self.assertEqual(tr["verdict"]["best"]["label"] if tr["verdict"]["best"] else None, a.meter)
        return tr

    def test_examples_match_the_engine(self):
        for ex in dd.EXAMPLES:
            with self.subTest(ex["id"]):
                tr = self.check(ex["text"])
                self.assertTrue(tr["verdict"]["identified"])

    def test_seesam_half_lines_are_joined(self):
        ex = next(e for e in dd.EXAMPLES if e["id"] == "seesamu")
        tr = dd.trace_payload(ex["text"])
        self.assertEqual([u["printed_lines"] for u in tr["units"][:4]], [[0, 1], [2, 3], [4, 5], [6, 7]])
        self.assertEqual(tr["verdict"]["best"]["label"], "seesamu+ataveladi")

    def test_padanta_rescues_a_line_that_dies_on_its_last_laghu(self):
        ex = next(e for e in dd.EXAMPLES if e["id"] == "sardula")
        u = dd.trace_payload(ex["text"])["units"][0]
        self.assertEqual(u["death_step"], len(u["aksharas"]))
        self.assertTrue(u["padanta"]["accepted"])

    def test_v2_layers_read_the_poem_as_the_decoder_does(self):
        from metrical_decoder.analysis import _telugu_words
        inv, att = dd.v2_layers()
        for ex in dd.EXAMPLES:
            with self.subTest(ex["id"]):
                tr = dd.trace_payload(ex["text"], "v2")
                words = [v["word"] for u in tr["units"] for v in u["v2"] if v["ends_word"]]
                self.assertEqual(words, [w for ln in tr["printed"] for w in _telugu_words(ln)])
                for u in tr["units"]:
                    for a, v in zip(u["aksharas"], u["v2"]):
                        self.assertEqual(v["inventory"], a["text"] in inv)
                        self.assertEqual(v["partial"], att.partial(v["word"]))
        gen = dd.trace_payload(next(e for e in dd.EXAMPLES if e["id"] == "generated-v1")["text"], "v2")
        self.assertEqual(gen["v2"]["outside_inventory"], ["చ్యె", "డ్యె", "త్యె", "న్యె"])

    def test_unidentified_poem(self):
        tr = self.check(BROKEN)
        self.assertFalse(tr["verdict"]["identified"])
        self.assertTrue(tr["verdict"]["failures"])


if __name__ == "__main__":
    unittest.main()

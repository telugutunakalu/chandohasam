# -*- coding: utf-8 -*-
"""metrical_decoder.strategies — the three strategies and the baseline on random logits (EXP-12 control)."""
import doctest
import importlib
import unittest

from dec_support import test_vocab
from indic_meter_dawg import patterns
from indic_meter_dawg.prosody import accepts_poem
from metrical_decoder import DecodeConfig, Enforcer, MaskCache, RandomLogits, decode, evaluate, extract_poem
from metrical_decoder.prompts import build_messages, meter_rules, n_lines

IX = test_vocab()
METERS = ("utpalamala", "kandamu", "dvipada", "ataveladi", "seesamu", "madhuragati_ragada", "mattakokilamu")
CONSTRAINED = ("masking_only", "masking_backtrack", "hybrid")


def run(meter, mode, seed=42, cfg=DecodeConfig()):
    enf = Enforcer(meter)
    return enf, decode(enf, IX, RandomLogits(IX), [], mode, seed=seed, cfg=cfg, masks=MaskCache(enf, IX))


class TestConstrained(unittest.TestCase):
    def test_every_strategy_yields_a_strictly_valid_poem(self):
        for meter in METERS:
            for mode in CONSTRAINED:
                enf, r = run(meter, mode)
                pats = list(patterns(r["text"]))
                with self.subTest(meter=meter, mode=mode):
                    self.assertEqual(r["status"], "complete")
                    self.assertTrue(accepts_poem(meter, pats), (r["text"], pats))

    def test_trace_records_the_probability_of_every_chosen_token(self):
        _, r = run("kandamu", "hybrid")
        toks = [t for t in r["trace"] if t.get("how") in ("sample", "accept", "alive", "forced_nl")]
        self.assertEqual(len(toks), r["n_tokens"])
        for t in toks:
            self.assertLessEqual(t["logp"], 0.0)
            self.assertGreaterEqual(t["rank"], 1)
            self.assertTrue(0 < t["p_pick"] <= 1)
            if t["how"] != "forced_nl":
                self.assertTrue(0 < t["valid_mass"] <= 1 + 1e-9)
                self.assertGreater(t["n_valid"], 0)
            self.assertEqual(len(t["top"]), 5)

    def test_a_poem_finished_by_the_budgets_last_token_is_complete(self):
        """Regression (E4B grid, 4 poems): the loop left on the budget before looking at the last token."""
        _, r = run("dvipada", "masking_only", seed=5)
        self.assertEqual(r["status"], "complete")
        _, exact = run("dvipada", "masking_only", seed=5, cfg=DecodeConfig(max_tokens=r["n_tokens"]))
        self.assertEqual((exact["status"], exact["text"]), ("complete", r["text"]))
        _, short = run("dvipada", "masking_only", seed=5, cfg=DecodeConfig(max_tokens=r["n_tokens"] - 1))
        self.assertEqual(short["status"], "budget")

    def test_seeded_runs_repeat(self):
        _, a = run("dvipada", "masking_only", seed=7)
        _, b = run("dvipada", "masking_only", seed=7)
        _, c = run("dvipada", "masking_only", seed=8)
        self.assertEqual(a["ids"], b["ids"])
        self.assertNotEqual(a["ids"], c["ids"])

    def test_backtracking_is_recorded_and_still_ends_in_meter(self):
        cfg = DecodeConfig(min_valid=10 ** 6, max_backtracks=5)       # trigger at every checkpoint
        _, r = run("utpalamala", "masking_backtrack", cfg=cfg)
        events = [t for t in r["trace"] if t.get("how") == "backtrack"]
        self.assertEqual(r["n_backtracks"], 5)
        self.assertEqual(len(events), 5)
        self.assertTrue(all(e["reason"] == "few_valid" for e in events))
        self.assertTrue(accepts_poem("utpalamala", list(patterns(r["text"]))))


class TestBaseline(unittest.TestCase):
    def test_baseline_samples_freely_and_the_enforcer_only_watches(self):
        _, r = run("utpalamala", "baseline", cfg=DecodeConfig(baseline_max_tokens=60))
        self.assertEqual(r["n_tokens"], 60)                  # random logits never emit EOS
        self.assertIsNotNone(r["left_meter_at"])
        self.assertTrue(any(t.get("in_meter") is False for t in r["trace"]))


class TestPromptsAndEvaluation(unittest.TestCase):
    def test_rules_for_every_meter(self):
        from indic_meter_dawg import default_dawg
        for spec in default_dawg().catalogue.concrete:
            if spec.abstract:
                continue
            text = meter_rules(spec.name)
            with self.subTest(meter=spec.name):
                self.assertIn(f"Lines (పాదాలు): {n_lines(spec.name)}.", text)
                self.assertIn("Yati", text)
                self.assertIn("Prāsa", text)
        self.assertIn("UII UIU III UII UII UIU IU", meter_rules("utpalamala"))
        msgs = build_messages("kandamu", "తల్లి ప్రేమ")
        self.assertEqual([m["role"] for m in msgs], ["system", "user"])
        self.assertIn("తల్లి ప్రేమ", msgs[1]["content"])

    def test_evaluation_of_a_classic_and_of_a_chatty_answer(self):
        kandam = "ఇందు గలఁ డందు లేఁ డని\nసందేహము వలదు చక్రి సర్వోపగతుం\nడెందెందు వెదకి చూచిన\nనందందే కలఁడు దానవాగ్రణి వింటే"
        ev = evaluate("Sure! Here it is:\n\n" + kandam + "\n\nHope you like it.", "kandamu")
        self.assertTrue(ev["gana_strict"] and ev["gana"] and ev["prasa_strict"])
        self.assertEqual(extract_poem("**శీర్షిక**\n1. రామ"), ["శీర్షిక", "రామ"])


def load_tests(loader, tests, ignore):
    for name in ("incremental", "orthography", "enforcer", "registers", "strategies", "sources", "vocab", "prompts", "evaluate"):
        tests.addTests(doctest.DocTestSuite(importlib.import_module(f"metrical_decoder.{name}")))
    return tests


if __name__ == "__main__":
    unittest.main()

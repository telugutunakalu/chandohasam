# -*- coding: utf-8 -*-
"""metrical_decoder.diffusion — NVFP4 decoding, the three strategies and free generation on a random-logit canvas (no model)."""
import doctest
import importlib
import types
import unittest

import torch

from dec_support import test_vocab
from indic_meter_dawg import patterns
from indic_meter_dawg.prosody import accepts_poem
from metrical_decoder import Enforcer, MaskCache, evaluate
from metrical_decoder.diffusion.canvas import RandomCanvas
from metrical_decoder.diffusion.decoding import CONSTRAINED, DiffusionConfig, decode_diffusion
from metrical_decoder.diffusion.nvfp4 import E2M1_VALUES, Nvfp4Experts, decode_nvfp4

IX = test_vocab()


def run(meter, mode, seed=42, cfg=DiffusionConfig(), canvas_length=32, **enforce):
    enf = Enforcer(meter, **enforce)
    canvas = RandomCanvas(IX, canvas_length=canvas_length)
    return enf, decode_diffusion(enf, IX, canvas, [], mode, seed=seed, cfg=cfg, masks=MaskCache(enf, IX))


class TestNvfp4(unittest.TestCase):
    def test_every_code_and_the_nibble_order(self):
        codes = torch.arange(16, dtype=torch.uint8)
        packed = (codes[1::2] << 4 | codes[0::2]).reshape(1, 8)             # element 2k in the low nibble
        w = decode_nvfp4(packed, torch.ones(1, 1).to(torch.float8_e4m3fn), torch.tensor(1.0), dtype=torch.float32)
        self.assertEqual(w[0].tolist(), list(E2M1_VALUES))

    def test_block_and_tensor_scales(self):
        packed = torch.full((2, 16), 0x22, dtype=torch.uint8)                # every value 1.0, 32 per row
        scale = torch.tensor([[1.0, 2.0], [4.0, 0.5]]).to(torch.float8_e4m3fn)
        w = decode_nvfp4(packed, scale, torch.tensor([10.0, 1.0]), dtype=torch.float32)   # one scale2 per row
        self.assertEqual(w[:, ::16].tolist(), [[10.0, 20.0], [4.0, 0.5]])

    def test_experts_match_a_loop_over_the_decoded_weights(self):
        cfg = types.SimpleNamespace(num_experts=4, hidden_size=32, moe_intermediate_size=16,
                                    hidden_activation="gelu_pytorch_tanh")
        ex = Nvfp4Experts(cfg)
        g = torch.Generator().manual_seed(0)
        gate_up = (torch.randint(0, 256, (4, 32, 16), dtype=torch.uint8, generator=g),
                   (torch.rand(4, 32, 2, generator=g) + 0.5).to(torch.float8_e4m3fn), torch.rand(4, 32, generator=g))
        down = (torch.randint(0, 256, (4, 32, 8), dtype=torch.uint8, generator=g),
                (torch.rand(4, 32, 1, generator=g) + 0.5).to(torch.float8_e4m3fn), torch.rand(4, generator=g))
        ex.load(gate_up, down)
        x = torch.randn(6, 32, generator=g, dtype=torch.float32).to(torch.bfloat16)
        idx = torch.tensor([[0, 1], [2, 3], [1, 1], [3, 0], [2, 2], [0, 3]])
        wts = torch.full((6, 2), 0.5)
        fast = ex(x, idx, wts.to(torch.bfloat16)).float()
        gu, dn = ex._decoded("gate_up").float(), ex._decoded("down").float()
        ref = torch.zeros(6, 32)
        for t in range(6):
            for k in range(2):
                gate, up = (x[t].float() @ gu[idx[t, k]].T).chunk(2)
                ref[t] += 0.5 * ((ex.act_fn(gate) * up) @ dn[idx[t, k]].T)
        self.assertLess(float((fast - ref).norm() / ref.norm()), 2e-2)
        ex.make_resident()                                                     # decoded once, same arithmetic
        self.assertTrue(torch.allclose(ex(x, idx, wts.to(torch.bfloat16)).float(), fast))


class TestDiffusionStrategies(unittest.TestCase):
    """The random-logit control for diffusion: exactness does not depend on where the tokens come from."""

    def test_every_strategy_completes_in_meter(self):
        for meter in ("utpalamala", "kandamu", "dvipada", "ataveladi", "seesamu", "madhuragati_ragada"):
            for mode in CONSTRAINED:
                enf, r = run(meter, mode)
                with self.subTest(meter=meter, mode=mode):
                    self.assertEqual(r["status"], "complete")
                    self.assertTrue(accepts_poem(meter, list(patterns(r["text"]))), r["text"])

    def test_prasa_and_yati_are_enforced(self):
        for mode in CONSTRAINED:
            _, r = run("utpalamala", mode, prasa=True, yati=True)
            ev = evaluate(r["text"], "utpalamala")
            with self.subTest(mode=mode):
                self.assertEqual(r["status"], "complete")
                self.assertTrue(ev["gana_strict"] and ev["prasa_strict"] and ev["yati_strict"], r["text"])

    def test_the_poem_crosses_blocks(self):
        _, r = run("utpalamala", "masking_only", canvas_length=8)
        self.assertEqual(r["status"], "complete")
        self.assertGreater(r["n_blocks"], 5)
        self.assertEqual({t["block"] for t in r["trace"] if "block" in t}, set(range(r["n_blocks"])))

    def test_trace_records_every_committed_token(self):
        for mode in CONSTRAINED:
            _, r = run("kandamu", mode)
            toks = [t for t in r["trace"] if t.get("how") != "backtrack"]
            with self.subTest(mode=mode):
                if r["n_backtracks"]:                  # unfrozen tokens stay in the trace, as in the AR traces
                    self.assertGreater(len(toks), r["n_tokens"])
                else:
                    self.assertEqual(len(toks), r["n_tokens"])
                for t in toks:
                    self.assertIn(t["how"], ("proposal", "masked", "rerank", "forced_nl"))
                    self.assertLessEqual(t["logp"], 0.0)
                    self.assertTrue(0 < t["p_pick"] <= 1 + 1e-9)
                    self.assertGreater(t["n_valid"], 0)
                    self.assertEqual(len(t["top"]), 5)
                # every pass commits at least one token, unless it backtracks
                self.assertGreaterEqual(len(toks), r["n_passes"] - r["n_backtracks"])

    def test_backtracking_unfreezes_and_still_ends_in_meter(self):
        cfg = DiffusionConfig(min_valid=10 ** 6, max_backtracks=5)               # trigger at every decision
        _, r = run("utpalamala", "masking_backtrack", cfg=cfg)
        events = [t for t in r["trace"] if t.get("how") == "backtrack"]
        self.assertEqual(r["n_backtracks"], 5)
        self.assertEqual(len(events), 5)
        self.assertEqual(r["status"], "complete")
        self.assertTrue(accepts_poem("utpalamala", list(patterns(r["text"]))))

    def test_seeded_runs_repeat(self):
        _, a = run("dvipada", "hybrid", seed=7)
        _, b = run("dvipada", "hybrid", seed=7)
        _, c = run("dvipada", "hybrid", seed=8)
        self.assertEqual(a["ids"], b["ids"])
        self.assertNotEqual(a["ids"], c["ids"])


class _EndingCanvas(RandomCanvas):
    """A random canvas whose model ends its reply at canvas position 10, set to forbid ends (as the
    constrained runs are) — free generation must lift that for its poem and restore it after."""
    END = 99_999
    end_token_ids = (END,)
    forbid_end = True

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.forbid_seen = []

    def denoise(self, frozen, temperature):
        self.forbid_seen.append(self.forbid_end)
        p = super().denoise(frozen, temperature)
        propose = p.proposal
        p.proposal = lambda pos: self.END if pos >= 10 else propose(pos)
        return p


class TestDiffusionBaseline(unittest.TestCase):
    """Free generation: the same loop without the constraint; the enforcer only watches."""

    def test_free_text_is_watched_until_it_leaves_the_meter(self):
        enf, r = run("utpalamala", "baseline", cfg=DiffusionConfig(baseline_max_tokens=60))
        self.assertEqual(r["status"], "budget")                  # the random canvas never ends its reply
        self.assertEqual(r["n_tokens"], 60)
        self.assertEqual(len(r["trace"]), 60)
        self.assertTrue(all(t["how"] == "proposal" for t in r["trace"]))
        left = r["left_meter_at"]
        self.assertIsNotNone(left)                               # random text leaves the meter …
        self.assertFalse(r["complete_in_meter"])
        for t in r["trace"][: left + 1]:                         # … and is watched up to that token
            self.assertGreater(t["n_valid"], 0)
        for t in r["trace"][left + 1:]:
            self.assertIsNone(t["n_valid"])
            self.assertFalse(t["in_meter"])

    def test_the_default_budget_is_the_autoregressive_baselines(self):
        enf, r = run("kandamu", "baseline")
        self.assertEqual(r["n_tokens"], 3 * enf.max_aksharas() + 32)

    def test_the_model_may_end_its_reply(self):
        enf = Enforcer("kandamu")
        canvas = _EndingCanvas(IX, canvas_length=32)
        r = decode_diffusion(enf, IX, canvas, [], "baseline", seed=3, masks=MaskCache(enf, IX))
        self.assertEqual(r["status"], "eos")
        self.assertEqual(r["n_tokens"], 10)
        self.assertEqual(r["trace"][-1]["how"], "eos")
        self.assertEqual(len(r["trace"]), 11)
        self.assertEqual(set(canvas.forbid_seen), {False})      # ends allowed during free generation …
        self.assertTrue(canvas.forbid_end)                      # … and the canvas's setting restored

    def test_seeded_runs_repeat(self):
        cfg = DiffusionConfig(baseline_max_tokens=30)
        _, a = run("dvipada", "baseline", seed=7, cfg=cfg)
        _, b = run("dvipada", "baseline", seed=7, cfg=cfg)
        self.assertEqual(a["ids"], b["ids"])


def load_tests(loader, tests, ignore):
    for name in ("nvfp4", "canvas", "decoding"):
        tests.addTests(doctest.DocTestSuite(importlib.import_module(f"metrical_decoder.diffusion.{name}")))
    return tests


if __name__ == "__main__":
    unittest.main()

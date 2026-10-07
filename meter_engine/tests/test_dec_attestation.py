# -*- coding: utf-8 -*-
"""metrical_decoder.attestation — Layer B reorders the allowed tokens and never changes them."""
import unittest

from dec_support import test_vocab
from indic_meter_dawg import patterns
from indic_meter_dawg.prosody import accepts_poem
from metrical_decoder import DecodeConfig, Enforcer, MaskCache, RandomLogits, decode, evaluate
from metrical_decoder.analysis import _telugu_words
from metrical_decoder.attestation import Attestation, load_attestation
from metrical_decoder.inventory import units

IX = test_vocab()


def run(meter, mode, cfg, seed=3):
    enf = Enforcer(meter, prasa=True, yati=True, inventory="verse")
    return decode(enf, IX, RandomLogits(IX), [], mode, seed=seed, cfg=cfg, masks=MaskCache(enf, IX))


class TestAttestation(unittest.TestCase):
    def test_scores(self):
        a = Attestation(["తల్లి", "ప్రేమ", "త"])
        self.assertEqual(a.score("", "తల్"), 2)               # begins తల్లి
        self.assertEqual(a.score("", "ల్లి"), 1)              # inside తల్లి
        self.assertEqual(a.score("తల్లి", " ప్రే"), 2)        # judged by the word it ends, తల్లి
        self.assertEqual(a.score("తల్", "ఱ"), 0)
        self.assertEqual(a.score("త", " "), 0)                # a single akshara is not a word here
        self.assertEqual(a.score("జు", " త"), 0)              # ending junk to begin a word earns nothing
        self.assertFalse(a.inside("లిప్రే"))                 # words are kept apart

    def test_the_corpus_has_its_words(self):
        a = load_attestation()
        for w in ("తల్లి", "ప్రేమ", "రాముడు", "లంక"):
            with self.subTest(word=w):
                self.assertEqual(a.finished(w), 2)


class TestLayerB(unittest.TestCase):
    """On random logits the model has no preference, so Layer B decides: the words get more real,
    and every poem still completes in meter (the allowed set is untouched)."""

    def test_poems_stay_in_meter_and_words_get_more_real(self):
        lex = load_attestation().words
        with_b = DecodeConfig(attest_weight=3.0, attest_where="all")
        for meter in ("kandamu", "utpalamala"):
            for mode in ("masking_only", "masking_backtrack", "hybrid"):
                plain, b = run(meter, mode, DecodeConfig()), run(meter, mode, with_b)
                ev = evaluate(b["text"], meter)
                real = [sum(w in lex for w in _telugu_words(r["text"])) / max(len(_telugu_words(r["text"])), 1)
                        for r in (plain, b)]
                with self.subTest(meter=meter, mode=mode):
                    self.assertEqual(b["status"], "complete")
                    self.assertTrue(accepts_poem(meter, list(patterns(b["text"]))))
                    self.assertTrue(ev["gana_strict"] and ev["prasa_strict"] and ev["yati_strict"])
                    self.assertTrue(all("attest" in t for t in b["trace"] if t.get("how") in ("sample", "accept", "alive")))
                    self.assertGreater(real[1], real[0])
                    words = _telugu_words(b["text"])
                    self.assertLess(sum(len(units(w)) == 1 for w in words), 0.25 * len(words))   # no filler


if __name__ == "__main__":
    unittest.main()

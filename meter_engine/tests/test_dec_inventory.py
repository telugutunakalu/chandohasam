# -*- coding: utf-8 -*-
"""metrical_decoder.inventory — only attested syllables, and liveness stays exact."""
import unittest

from dec_support import test_vocab
from indic_meter_dawg import patterns
from indic_meter_dawg.prosody import accepts_poem
from metrical_decoder import DecodeConfig, Enforcer, MaskCache, RandomLogits, decode, evaluate
from metrical_decoder.analysis import _telugu_words
from metrical_decoder.inventory import Inventory, load_inventory, units
from metrical_decoder.registers import continuations

IX = test_vocab()


class TestInventory(unittest.TestCase):
    def test_the_verse_inventory_holds_the_corpus_syllables(self):
        inv = load_inventory("verse")
        self.assertGreater(len(inv), 3000)
        for word in ("తల్లి", "ప్రేమ", "హనుమంతుడు", "శ్రీరాముడు", "వచ్చెన్"):
            with self.subTest(word=word):
                self.assertTrue(inv.all_known(word))
        for invented in ("ల్రు", "న్యె", "ల్య్య్మ"):     # written by the v1 decoder, never in real verse
            with self.subTest(invented=invented):
                self.assertNotIn(invented, inv)

    def test_the_tokenizer_inventory_is_broader(self):
        verse, tok = load_inventory("verse"), load_inventory("tokenizer")
        self.assertGreater(len(tok), len(verse))
        self.assertGreater(len(verse.units & tok.units) / len(verse), 0.99)
        self.assertIn("ల్రు", tok)                         # modern text has it; verse does not

    def test_units_are_the_scanners_syllables(self):
        self.assertEqual(units("సత్యము"), ("స", "త్య", "ము"))
        self.assertEqual(units("పూసెన్"), ("పూ", "సెన్"))

    def test_an_inventory_reloads_by_name(self):
        import pickle
        inv = load_inventory("verse")
        self.assertIs(pickle.loads(pickle.dumps(inv)), inv)


class TestEnforcerWithInventory(unittest.TestCase):
    def test_unattested_syllables_are_refused(self):
        e = Enforcer("utpalamala", prasa=True, yati=True, inventory="verse")
        s = e.initial()
        self.assertIsNone(e.step(s, "ల్రు"))                 # no attested syllable starts so
        self.assertIsNotNone(e.step(s, "ల్ర"))               # ల్ర, ల్రా … are attested
        self.assertIsNotNone(e.step(s, "తల్లి"))
        free = Enforcer("utpalamala", prasa=True, yati=True)
        self.assertIsNotNone(free.step(free.initial(), "ల్రు"))

    def test_a_word_ends_only_on_attested_syllables(self):
        inv = Inventory(["క", "కా", "రా", "ము"], "toy")
        e = Enforcer("vidyunmala", inventory=inv)             # every akshara guru
        s = e.step(e.initial(), "రా")
        self.assertIsNotNone(s)
        self.assertIsNone(e.step(s, "రీ"))                   # not in the toy inventory
        self.assertIsNotNone(e.step(s, "కా"))

    def test_continuations_carry_attested_completions(self):
        inv = load_inventory("verse")
        kinds = {c.kind: c for c in continuations("సత్య", inv=inv)}
        self.assertEqual(set(kinds), {"keep"})                # nothing attested grows త్య, and సత్య్ is not a word end
        keep = kinds["keep"]
        self.assertTrue(keep.descs[-1].options <= inv.units)
        self.assertTrue(all(u.startswith("త్య") for u in keep.descs[-1].options))
        free = {c.kind for c in continuations("సత్య")}
        self.assertEqual(free, {"keep", "grow", "die"})


class TestGuruRoutes(unittest.TestCase):
    def test_an_attested_light_conjunct_may_be_guru_through_the_next_conjunct(self):
        """Regression (random-logit control, లలిత, verse inventory): line 1's prāsa akshara న్స్మ is attested
        only light and was guru through the conjunct after it; line 2 must be allowed to do the same,
        although other completions of న are guru by themselves."""
        e = Enforcer("lalita", prasa=True, yati=True, inventory="verse")
        s = e.initial()
        for t in (" ఛ", "న్స్", "మర్శ", "ఠ", "ంజ", " అను", " గ్ర", "జ్", "వర", "ాను", " వ", "త", "్", "\n", "ట్లా", " "):
            s = e.step(s, t)
            self.assertIsNotNone(s)
        self.assertIsNotNone(e.step(s, "న"))
        self.assertIsNotNone(e.step(s, "న్స్మ"))

    def test_each_weight_and_route_is_its_own_class(self):
        inv = load_inventory("verse")
        routes = {(c.kind, c.weights, c.u_by_conjunct) for c in continuations("న", inv=inv)}
        self.assertIn(("keep", ("U",), False), routes)        # guru by itself (నా, నం …)
        self.assertIn(("keep", ("U",), True), routes)         # light, guru through a conjunct that follows
        self.assertIn(("keep", ("I",), False), routes)
        for c in continuations("న", inv=inv):
            light = all(not Inventory.guru(u) for u in c.descs[-1].options)
            self.assertEqual(light, c.weights[0][-1] == "I" or c.u_by_conjunct)

class TestSoundnessWithInventory(unittest.TestCase):
    """The random-logit control with an inventory: every poem completes, in meter, attested only."""

    def test_every_strategy_completes_with_attested_syllables(self):
        for name in ("verse", "tokenizer"):
            inv = load_inventory(name)
            for meter in ("utpalamala", "kandamu", "ataveladi"):
                for mode in ("masking_only", "masking_backtrack", "hybrid"):
                    enf = Enforcer(meter, prasa=True, yati=True, inventory=name)
                    r = decode(enf, IX, RandomLogits(IX), [], mode, seed=7, cfg=DecodeConfig(),
                               masks=MaskCache(enf, IX))
                    ev = evaluate(r["text"], meter)
                    words = [w for ln in r["text"].splitlines() for w in _telugu_words(ln)]
                    with self.subTest(inventory=name, meter=meter, mode=mode):
                        self.assertEqual(r["status"], "complete")
                        self.assertTrue(accepts_poem(meter, list(patterns(r["text"]))))
                        self.assertTrue(ev["gana_strict"] and ev["prasa_strict"] and ev["yati_strict"])
                        self.assertTrue(all(inv.all_known(w) for w in words), r["text"])


if __name__ == "__main__":
    unittest.main()

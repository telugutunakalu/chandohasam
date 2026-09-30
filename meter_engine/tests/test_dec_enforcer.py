# -*- coding: utf-8 -*-
"""metrical_decoder.enforcer — real poems are never rejected, dead text always is."""
import random
import unittest

from dec_support import classics
from indic_meter_dawg import patterns
from indic_meter_dawg.prosody import accepts_poem
from metrical_decoder import Enforcer, line_lengths


def _chunks(text: str, rng: random.Random) -> list[str]:
    out, i = [], 0
    while i < len(text):
        k = rng.randint(1, 4)
        out.append(text[i:i + k])
        i += k
    return out


class TestCompleteness(unittest.TestCase):
    def test_classical_stanzas_stay_alive_in_any_chunking(self):
        """Every hand-scanned classic whose canonical scansion is in its meter passes, token boundaries anywhere."""
        rng = random.Random(3)
        checked = 0
        for st in classics():
            text = st["text"].strip()
            lines = text.splitlines()
            if not accepts_poem(st["meter"], list(patterns(lines))):
                continue                                   # needs pādānta / vikalpa: not a generation-time poem
            checked += 1
            enf = Enforcer(st["meter"], orthography=False)  # the corpus keeps ZWNJ and punctuation runs
            for trial in range(20):
                s = enf.initial()
                for piece in _chunks(text, rng):
                    s = enf.step(s, piece)
                    if s is None:
                        break
                with self.subTest(stanza=st["id"], trial=trial):
                    self.assertIsNotNone(s)
                    self.assertTrue(enf.poem_complete(s))
        self.assertGreater(checked, 3)


class TestRejection(unittest.TestCase):
    def test_wrong_weight_dies_once_the_word_is_finished(self):
        e = Enforcer("vidyunmala")                          # all guru
        s = e.step(e.initial(), "రామా")
        self.assertIsNotNone(e.step(s, "ము"))               # ముం / ముల్ could still be guru
        self.assertIsNone(e.step(s, "ము "))
        self.assertIsNone(e.step(e.initial(), "\n"))        # no empty line

    def test_no_newline_before_the_line_is_complete(self):
        e = Enforcer("utpalamala")
        s = e.step(e.initial(), "ఎవ్వనిచే ")                # UIIU: a legal start of భ ర …
        self.assertIsNotNone(s)
        self.assertIsNone(e.step(s, "\n"))
        self.assertIsNone(e.step(e.initial(), "శ్రీకైవల్య"))  # UU…: శార్దూలము's opening, not ఉత్పలమాల's

    def test_states_are_hashable_values(self):
        e = Enforcer("dvipada")
        a, b = e.step(e.initial(), "శ్రీ"), e.step(e.initial(), "శ్రీ")
        self.assertEqual(a, b)
        self.assertEqual(len({a, b}), 1)


class TestLineEnds(unittest.TestCase):
    def test_seesamu_thirty_laghus_may_end_or_continue(self):
        e = Enforcer("seesamu", orthography=False)
        s = e.step(e.initial(), "న" * 30)
        self.assertTrue(e.line_complete(s))
        self.assertFalse(e.must_end_line(s))                # the sarvalaghu form continues to 36

    def test_vritta_line_must_end(self):
        e = Enforcer("vidyunmala", orthography=False)
        s = e.step(e.initial(), "రా" * 8)
        self.assertTrue(e.must_end_line(s))

    def test_lengths(self):
        self.assertEqual(line_lengths("dvipada", "all"), (11, 15))
        self.assertEqual(Enforcer("utpalamala").max_aksharas(), 80)
        self.assertEqual(Enforcer("dvipada", units=2).max_aksharas(), 60)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""metrical_decoder.incremental and .orthography — weights of unfinished text, well-formedness."""
import random
import unicodedata
import unittest

from dec_support import corpus_lines, sc
from metrical_decoder import incremental as inc
from metrical_decoder import orthography as ortho


def _prefix_ok(line: str, cut: int) -> bool:
    """The committed/pending property for one prefix of one line (probe B of the plan)."""
    full = sc.classify(sc.syllabify(line))
    prefix = unicodedata.normalize("NFC", line[:cut])
    # finished words and the unfinished one
    last_boundary = max((i for i, ch in enumerate(prefix) if inc.is_boundary(ch)), default=-1)
    finished, word = prefix[:last_boundary + 1], prefix[last_boundary + 1:]
    got = "".join(s.weight for s in sc.classify(sc.syllabify(finished)))
    committed, options, _ = inc.split_word(word) if word else ("", ("",), 0)
    got += committed
    expected = "".join(s.weight for s in full if s.start < len(prefix))
    return expected.startswith(got) and expected[len(got):] in options


class TestIncremental(unittest.TestCase):
    def test_committed_weights_never_change_and_pending_options_cover_the_truth(self):
        lines = corpus_lines()[::40]                        # ~160 lines, every character prefix
        bad = [(ln, i) for ln in lines for i in range(1, len(ln) + 1) if not _prefix_ok(ln, i)]
        self.assertEqual(bad[:5], [])

    def test_word_weights_equal_line_weights(self):
        for ln in corpus_lines()[::97]:
            words = [w for w in ln.replace(",", " ").split() if w]
            line_w = "".join(s.weight for s in sc.scan_line(ln).syllables)
            joined = "".join(inc.word_weights(w) for w in words)
            with self.subTest(line=ln):
                self.assertEqual(joined, line_w)

    def test_full_cluster_cannot_grow_or_die(self):
        grown = inc.split_word("సక్ష్మ్య")                  # 3 viramas: the orthography limit
        stuck = inc.split_word("సక్ష్మ్య", cluster_can_grow=False)
        self.assertIn("U", grown.options)                   # dies as a pollu -> one guru
        self.assertNotIn("U", stuck.options)
        self.assertTrue(set(stuck.options) < set(grown.options))

    def test_long_vowel_is_final(self):
        self.assertEqual(inc.split_word("రా").options, ("U",))


class TestOrthography(unittest.TestCase):
    def test_corpus_lines_are_well_formed(self):
        typos = {"దీనవదనుఁ డగుచుదేహి  యీ దేహంబు",               # double space in the source
                 "డింద్రియ పరవశుఁడు భక్తియెడ మధ్యముంఁడౌ"}      # ం followed by ఁ
        bad = []
        for ln in corpus_lines():
            text = "".join(ch for ch in ln if ch not in "​‌‍﻿")
            if not ortho.is_well_formed(text) and text not in typos:
                bad.append(text)
        self.assertEqual(bad, [])

    def test_malformed_sequences_are_rejected(self):
        for text in ("ా", "క్ా", "కాా", "క్్", "కంం", "క  ఖ", "క‌ఖ", " ్రీ", "అా", "క్ష్మ్య్ర", "న్ ", "క్ష్\n"):
            with self.subTest(text=text):
                self.assertFalse(ortho.is_well_formed(text))

    def test_well_formed_sequences_are_accepted(self):
        for text in ("శ్రీ", "సెన్ ", "క్ష్మ్య", "కై", "ఆఁక", "తపః ఫలము", "న్"):
            with self.subTest(text=text):
                self.assertTrue(ortho.is_well_formed(text))

    def test_akshara_length_is_bounded(self):
        """Random well-formed strings never go more than ten characters without a new syllable."""
        rng = random.Random(5)
        alphabet = "కగనరమస్ాిీుూెేైొోౌంఃఁఅఆ "
        for _ in range(3000):
            s, text = ortho.START, ""
            for _ in range(40):
                ch = rng.choice(alphabet)
                nxt = ortho.step(s, ch)
                if nxt is not None:
                    s, text = nxt, text + ch
            for word in text.split():
                syls = sc.syllabify(word)
                self.assertLessEqual(len(word), 10 * max(len(syls), 1), word)


if __name__ == "__main__":
    unittest.main()

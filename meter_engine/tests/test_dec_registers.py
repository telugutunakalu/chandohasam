# -*- coding: utf-8 -*-
"""The prāsa / yati registers: their shortcuts decide exactly as the engines do."""
from __future__ import annotations

import random
import unittest
from unittest import mock

from dec_support import corpus_lines

from metrical_decoder import Enforcer
from metrical_decoder import registers as R

import prasa_engine                                              # noqa: E402  (on sys.path via metrical_decoder)
import yati as yati_engine                                       # noqa: E402
from yati import line as yati_line                               # noqa: E402

CONSONANTS = tuple("కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరఱలళవశషసహ")


def _prev(vowel="అ", anus=False, cb=False, dead=()):
    return R.replace(R._syllables("క")[0], text="", onset=(), vowel=vowel, anusvara=anus, candrabindu=cb, dead=dead)


CONTEXTS = [(None, True)] + [(p, wi) for p in (_prev(), _prev("ఉ"), _prev(anus=True), _prev(dead=("న",)),
                                               _prev(cb=True)) for wi in (True, False)]


class TestShortcuts(unittest.TestCase):
    def test_class_vowels_decide_like_every_vowel(self):
        """With consonants on both sides, some vowel of the weight is in maitri with the vaḷi
        exactly when one of CLASS_VOWELS is (checked over 2.1M cases offline; a sample here)."""
        rng = random.Random(5)
        lines = [ln for ln in corpus_lines() if len(R._syllables(ln)) > 10]
        valis = []
        for ln in rng.sample(lines, 12):
            syls = R._syllables(ln)
            for i in (1, 9):
                side = R._line_side(syls, i, (), False, False)
                if side[0].onset:
                    valis.append(side)
        onsets = [(c,) for c in CONSONANTS] + [("క", "ష"), ("స", "త"), ("ద", "ర"), ("న", "న"), ("ప", "ర")]
        for vali in valis:
            for onset in onsets:
                for weight in ("I", "U"):
                    vowels = R.ALL_VOWELS if weight == "U" else R.SHORT_VOWELS
                    marks = ("", "ం") if weight == "U" else ("",)
                    for prev, wi in CONTEXTS:
                        passing = [v for v in vowels if any(
                            R._pair_ok(vali, R._side(prev, R._syllables(R.VIRAMA.join(onset) + R.MATRA[v] + mk)[0],
                                                     wi, (), False, False), "strict") for mk in marks)]
                        with self.subTest(vali=vali[0].text, onset=onset, weight=weight):
                            self.assertEqual(bool(passing), any(v in R.CLASS_VOWELS[weight] for v in passing))

    def test_canonical_previous_syllable_keeps_the_verdict(self):
        """The engine reads of the syllable before a yati akshara only what _canon_prev keeps."""
        checked = 0
        for ln in corpus_lines()[:400]:
            syls = R._syllables(ln)
            vali = R._line_side(syls, 1, (), False, False)
            for i in range(2, len(syls) + 1):
                prev, s = syls[i - 2], syls[i - 1]
                wi = prev.word != s.word
                full = R._pair_ok(vali, R._side(R._canon(prev), s, wi, (), False, False), "strict")
                coarse = R._pair_ok(vali, R._side(R._canon_prev(prev), s, wi, (), False, False), "strict")
                self.assertEqual(full, coarse, (ln, i))
                checked += 1
        self.assertGreater(checked, 4000)

    def test_prasa_yati_mirror_matches_the_engine(self):
        """_prasa_yati_holds is yati.line._prasa_yati, for every pair (P, Y) of real lines."""
        rs = yati_engine._rs(None)
        checked = 0
        with mock.patch.object(prasa_engine, "load_ruleset", lambda path=None: R._prasa_rules()):
            for ln in corpus_lines()[:300]:
                syls = list(R._syllables(ln))
                for p1 in (1, 3):
                    for y in range(p1 + 2, len(syls)):
                        g = (p1, y)
                        self.assertEqual(R._prasa_yati_holds(syls, g),
                                         yati_line._prasa_yati(syls, g, rs)["matched"], (ln, g))
                        checked += 1
        self.assertGreater(checked, 3000)

    def test_fallback_feasible(self):
        self.assertTrue(R._fallback_feasible(("క", "ర"), ("క",), True))      # క్ + ర grows into క్ర
        self.assertFalse(R._fallback_feasible(("మ",), ("క",), True))         # a conjunct never rhymes with మ
        self.assertTrue(R._fallback_feasible(("స",), ("శ",), False))         # స ~ శ (PRASA-MAITRI-SA-SHA)
        self.assertFalse(R._fallback_feasible(("మ",), ("ర",), False))


class TestBahuyati(unittest.TestCase):
    def test_one_constituent_must_serve_every_caesura(self):
        """మానిని, group (1, 7, 13, 19), vaḷi బ్రి: వి at 7 is matched through బ; at 13 a ఝ can
        only be matched through ర (ఝృ), and akshara 12 must stay laghu, so no conjunct can save
        it — బహుయతి నియతి (YATI-SY-11) fails. Regression: this used to die only at akshara 19."""
        text = " బ్రిస్య అరుణ్రియ వివ్యటమిన్నిహుఝ"
        enf = Enforcer("manini", prasa=True, yati=True)
        s = enf.initial()
        for ch in text[:-1]:
            s = enf.step(s, ch)
            self.assertIsNotNone(s)
        self.assertIsNone(enf.step(s, text[-1]))

    def test_serving_constituents(self):
        syls = R._syllables("బ్రిస్య అరుణ్రియ వివ్యటమిన్నిహుఝృక్కు")
        vali = R._line_side(syls, 1, (), False, True)
        self.assertEqual(R._pair_serves(vali, R._line_side(syls, 7, (), False, True), "strict"), frozenset({0}))
        self.assertEqual(R._pair_serves(vali, R._line_side(syls, 13, (), False, True), "strict"), frozenset({1}))


class TestWordEnds(unittest.TestCase):
    def test_no_word_ends_in_two_dead_consonants(self):
        """వన్స్: the prāsa engine makes న్స్ an akshara of its own, the scanner keeps one syllable
        వన్స్; the filter forbids such endings (none in the corpus). Regression: a సృగ్ధర whose
        line 1 opened with వన్స్ had no way to write line 2's prāsa."""
        from metrical_decoder.incremental import split_word
        enf = Enforcer("sragdhara", prasa=True, yati=True)
        s = enf.initial()
        for ch in "వన్స్":
            s = enf.step(s, ch)
            self.assertIsNotNone(s)
        self.assertIsNone(enf.step(s, " "))
        self.assertIsNotNone(enf.step(s, "ట"))            # the cluster may still open a syllable
        self.assertFalse(enf.line_complete(s))
        self.assertNotIn("U", split_word("వన్స్", long_pollu=False).options)
        self.assertIn("U", split_word("కన్", long_pollu=False).options)

    def test_no_word_is_dead_consonants_alone(self):
        """న్ as a word of its own scans as an akshara with neither onset nor vowel, which no akshara
        can meet in yati (none in the corpus). Regression: DiffusionGemma opened the last line of an
        ఇంద్రవజ్ర with న్ and reached a state with no allowed token (indravajra|T2|masking_only|63)."""
        enf = Enforcer("indravajra", prasa=True, yati=True)
        s = enf.initial()
        for ch in "కంజర్యముంచెడ్రవి జ్వ్వ్కమ్రమగ్యమ్\nమొంజుగ్యటెల్వర్రు మముళ్యమున్యుస్\nముం జట్ర లత్యాన్ని చి జ్య్ట్వోమతిక్యుజ్\nన్":
            s = enf.step(s, ch)
            self.assertIsNotNone(s)
        self.assertIsNone(enf.step(s, " "))                # న్ may not stand alone …
        self.assertIsNotNone(enf.step(s, "చ"))            # … but may still open a conjunct
        self.assertFalse(enf.line_complete(s))

        def kinds(word, **kw):
            return {c.kind for c in R.continuations(word, **kw)}
        self.assertEqual(kinds("న్"), {"grow", "lone"})
        self.assertEqual(kinds("న్", bare_pollu=False), {"grow"})
        self.assertEqual(kinds("క", bare_pollu=False), {"grow", "keep"})           # a first syllable cannot die
        self.assertEqual(kinds("సత్య", bare_pollu=False), {"grow", "keep", "die"})  # a later one can (సత్య్)


class TestAnalysis(unittest.TestCase):
    def test_positions(self):
        from metrical_decoder.analysis import _position, _yati_targets
        targets = _yati_targets("utpalamala", ["UIIUIUIIIUIIUIIUIUIU"])
        self.assertEqual(targets, {0: {10}})
        pos = [_position({"line": 0, "akshara": a}, True, targets) for a in (1, 2, 10, 11)]
        self.assertEqual(pos, ["line_start", "prasa", "yati", "other"])
        self.assertEqual(_position({"line": 0, "akshara": 2}, False, targets), "other")   # no prāsa in the meter

    def test_corpus_lexicon(self):
        from metrical_decoder.analysis import corpus_lexicon
        lex = corpus_lexicon()
        self.assertGreater(len(lex), 10_000)
        self.assertIn("రామ", lex)


class TestLastLine(unittest.TestCase):
    def test_the_last_line_is_checked_whole_before_the_poem_is_complete(self):
        """The last line ends at EOS, not ⏎: poem_complete must run the whole-line check itself."""
        enf = Enforcer("kandamu", prasa=True, yati=True)
        closes = []
        real = enf.registers.close_line
        with mock.patch.object(enf.registers, "close_line", side_effect=lambda st: closes.append(st) or real(st)):
            s = enf.initial()
            enf.line_complete(s._replace(line_pat="UU", line_text="రామా", lines=enf.n_lines - 1))
        self.assertEqual(len(closes), 0)                    # not a complete line: no whole-line check
        with mock.patch.object(enf.registers, "close_line", return_value=None):
            self.assertFalse(enf.poem_complete(_complete_last_line(enf)))
        self.assertTrue(Enforcer("kandamu").poem_complete(_complete_last_line(Enforcer("kandamu"))))


def _complete_last_line(enf):
    """A state on the last line of a kandamu whose gaṇas are complete."""
    from indic_meter_dawg import default_dawg
    grammar = default_dawg().grammars[("kandamu", "even")]
    pattern = next(iter(grammar.gana_positions and [_one_line(grammar)]))
    q = enf.dfa.start
    for ln in range(enf.n_lines - 1):
        q = enf.run(q, _one_line(default_dawg().grammars[("kandamu", "odd" if ln % 2 == 0 else "even")]) + "\n")
    return enf.initial()._replace(q=enf.run(q, pattern), lines=enf.n_lines - 1, line_pat=pattern,
                                  line_text="క" * len(pattern))


def _one_line(grammar) -> str:
    return "".join(choices[0].pattern for choices in grammar.gana_positions)


if __name__ == "__main__":
    unittest.main()

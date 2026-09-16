# -*- coding: utf-8 -*-
"""scansion.py — codepoint classes, syllable assembly, the five guru rules,
vikalpa bookkeeping, and text → meter end to end."""
import contextlib
import io
import random
import unicodedata
import unittest

import yaml

from imd_support import FIXTURES, HERE, dawg, imd
from indic_meter_dawg import scansion as sc
from indic_meter_dawg.identify import identify_text

FIX = yaml.safe_load(open(FIXTURES / "classics.yaml", encoding="utf-8"))["stanzas"]


def texts(line):
    return [s.text for s in sc.syllabify(line)]


def pat(line, **policy):
    return sc.scan_line(line, sc.ScanPolicy(**policy) if policy else sc.DEFAULT_POLICY).pattern


class TestClassifyChar(unittest.TestCase):
    def test_every_telugu_codepoint_has_a_category(self):
        known = {sc.CONSONANT, sc.VOWEL, sc.MATRA, sc.VIRAMA, sc.ANUSVARA, sc.VISARGA, sc.CANDRABINDU,
                 sc.LENGTH, sc.AVAGRAHA, sc.ZW, sc.SPACE, sc.NEWLINE, sc.OTHER}
        for cp in range(0x0C00, 0x0C80):
            self.assertIn(sc.classify_char(chr(cp)), known)

    def test_ranges(self):
        for ch in "కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరలవశషసహళఱౘౙ":
            self.assertEqual(sc.classify_char(ch), sc.CONSONANT, ch)
        for ch in "అఆఇఈఉఊఋౠఎఏఐఒఓఔ":
            self.assertEqual(sc.classify_char(ch), sc.VOWEL, ch)
        for ch in "ాిీుూృౄెేైొోౌ":
            self.assertEqual(sc.classify_char(ch), sc.MATRA, ch)
        self.assertEqual(sc.classify_char("్"), sc.VIRAMA)
        self.assertEqual(sc.classify_char("ం"), sc.ANUSVARA)
        self.assertEqual(sc.classify_char("ః"), sc.VISARGA)
        self.assertEqual(sc.classify_char("ఁ"), sc.CANDRABINDU)
        self.assertEqual(sc.classify_char("ఽ"), sc.AVAGRAHA)
        self.assertEqual(sc.classify_char("‌"), sc.ZW)
        self.assertEqual(sc.classify_char("\n"), sc.NEWLINE)
        self.assertEqual(sc.classify_char("\t"), sc.SPACE)
        for ch in "a1;,.-౧":
            self.assertEqual(sc.classify_char(ch), sc.OTHER, ch)

    def test_matra_table_covers_every_sign(self):
        self.assertEqual(set(sc.MATRA_TO_VOWEL.values()) <= sc.INDEPENDENT_VOWELS, True)


class TestSyllabify(unittest.TestCase):
    def test_report_worked_examples(self):
        self.assertEqual(texts("నమస్కారం"), ["న", "మ", "స్కా", "రం"])
        self.assertEqual(texts("పూసెన్"), ["పూ", "సెన్"])
        self.assertEqual(texts("తెలుగు భాష"), ["తె", "లు", "గు", "భా", "ష"])
        self.assertEqual(texts("స్త్రీ"), ["స్త్రీ"])
        self.assertEqual(texts("మంచి"), ["మం", "చి"])

    def test_structure_fields(self):
        s = sc.syllabify("స్త్రీ")[0]
        self.assertEqual(s.onset, ("స", "త", "ర"))
        self.assertEqual(s.vowel, "ఈ")
        self.assertTrue(s.is_conjunct and s.is_repha_conjunct)
        s = sc.syllabify("రం")[0]
        self.assertTrue(s.anusvara)
        self.assertEqual(s.vowel, "అ")
        s = sc.syllabify("పూసెన్")[1]
        self.assertEqual(s.dead, ("న",))
        self.assertEqual(s.text, "సెన్")
        self.assertEqual(sc.syllabify("అంబ")[0].text, "అం")
        self.assertEqual(sc.syllabify("దుఃఖము")[0].text, "దుః")
        self.assertTrue(sc.syllabify("దుఃఖము")[0].visarga)

    def test_pollu_merges_only_within_the_word(self):
        self.assertEqual(texts("దన్ లోక"), ["దన్", "లో", "క"])
        self.assertEqual([s.word for s in sc.syllabify("దన్ లోక")], [0, 1, 1])
        self.assertEqual(texts("సెన్‌క"), ["సెన్", "క"])       # explicit non-joiner: pollu, not conjunct
        self.assertEqual(texts("సెన్క"), ["సె", "న్క"])             # without it: న్క is a conjunct

    def test_word_of_a_dead_consonant_alone(self):
        s = sc.syllabify("న్")
        self.assertEqual(len(s), 1)
        self.assertEqual(s[0].dead, ("న",))
        self.assertEqual(s[0].vowel, "")
        self.assertEqual(pat("న్"), "U")

    def test_independent_vowel_inside_a_word(self):
        self.assertEqual(texts("కునై"), ["కు", "నై"])
        self.assertEqual([s.word for s in sc.syllabify("కునై")], [0, 0])

    def test_arasunna_attaches_without_weight(self):
        s = sc.syllabify("గలఁ")
        self.assertEqual([x.text for x in s], ["గ", "లఁ"])
        self.assertTrue(s[1].candrabindu)
        self.assertEqual(pat("గలఁ"), "II")

    def test_punctuation_and_digits_are_boundaries(self):
        s = sc.syllabify("జగ; మెవ్వని 12 లో")
        self.assertEqual([x.text for x in s], ["జ", "గ", "మె", "వ్వ", "ని", "లో"])
        self.assertEqual([x.word for x in s], [0, 0, 1, 1, 1, 2])

    def test_stray_marks(self):
        self.assertEqual(texts("ాక"), ["క"])
        self.assertEqual(texts("క ం"), ["క"])
        s = sc.syllabify("కంం")
        self.assertEqual(len(s), 1)
        self.assertTrue(s[0].anusvara)

    def test_offsets_reconstruct_the_text(self):
        for line in ("శ్రీకైవల్య పదంబుఁ జేరుటకునైచింతించెదన్ లోక ర", "ఎవ్వనిచే జనించు జగ; మెవ్వని లోపల నుండు లీనమై;"):
            syl = sc.syllabify(line)
            for a, b in zip(syl, syl[1:]):
                self.assertLessEqual(a.end, b.start)
            for s in syl:
                self.assertEqual(sc._clean(line[s.start:s.end]), s.text)
            self.assertEqual("".join(s.text for s in syl), "".join(ch for ch in line if sc.classify_char(ch)
                                                                    not in (sc.SPACE, sc.OTHER, sc.NEWLINE, sc.ZW)))

    def test_empty_and_foreign(self):
        self.assertEqual(sc.syllabify(""), ())
        self.assertEqual(sc.syllabify("hello world 42"), ())
        self.assertEqual(sc.scan("hello"), ())

    def test_agrees_with_aksharanusarika(self):
        """Cross-check against the project's older splitter on real lines."""
        import sys
        sys.path.insert(0, str(HERE.parent))
        try:
            import prasa_engine as pe
            ak = pe.load_aksharanusarika()
        except Exception as e:                       # pragma: no cover
            self.skipTest(f"aksharanusarika not loadable: {e}")
        lines = [ln for st in FIX for ln in (st.get("text") or "").splitlines() if ln.strip()]
        lines += ["నమస్కారం", "పూసెన్", "స్త్రీ", "దుఃఖము", "కృష్ణుఁడు", "సర్వోపగతుండు"]
        for line in lines:
            theirs = [t.replace("ఁ", "") for t in ak.split_aksharalu(line)
                      if any(sc.classify_char(ch) in (sc.CONSONANT, sc.VOWEL) for ch in t)]
            ours = [s.text.replace("ఁ", "") for s in sc.syllabify(line)]
            with self.subTest(line=line):
                self.assertEqual(ours, theirs)


class TestGuruRules(unittest.TestCase):
    def test_each_rule(self):
        cases = {
            "రా": ("U", "deergha"), "కీ": ("U", "deergha"), "ఆ": ("U", "deergha"), "ఏ": ("U", "deergha"),
            "కై": ("U", "sandhyakshara"), "ఔ": ("U", "sandhyakshara"),
            "సం": ("U", "anusvara"), "నః": ("U", "visarga"),
            "క": ("I", "laghu"), "కి": ("I", "laghu"), "కృ": ("I", "laghu"), "అ": ("I", "laghu"), "ఋ": ("I", "laghu"),
        }
        for text, (w, rule) in cases.items():
            s = sc.scan_line(text).syllables[0]
            with self.subTest(text=text):
                self.assertEqual(s.weight, w)
                self.assertIn(rule, s.rules)

    def test_pollu(self):
        s = sc.scan_line("పూసెన్").syllables
        self.assertEqual([x.weight for x in s], ["U", "U"])
        self.assertIn("pollu", s[1].rules)

    def test_samyukta_within_word(self):
        self.assertEqual(pat("సత్యము"), "UII")
        self.assertEqual(pat("అమ్మ"), "UI")
        self.assertEqual(pat("పుట్ట"), "UI")
        self.assertEqual(pat("కృష్ణ"), "UI")          # ృ is short, but the following conjunct lengthens it
        self.assertIn("samyukta", sc.scan_line("సత్యము").syllables[0].rules)

    def test_samyukta_blocked_by_space_and_newline(self):
        self.assertEqual(pat("స త్యము"), "III")
        self.assertEqual([s.pattern for s in sc.scan("స\nత్యము")], ["I", "II"])
        self.assertEqual(pat("తనుము ళ్ళరాస్తుంది"), "IIIIUUI")      # the report's worked example

    def test_word_initial_conjunct_is_a_vikalpa(self):
        s = sc.scan_line("స త్యము").syllables[0]
        self.assertEqual(s.weight, "I")
        self.assertEqual(s.vikalpa, sc.VIKALPA_WORD_INITIAL)
        self.assertEqual(s.alternative_weight, "U")
        self.assertEqual(pat("స త్యము", word_initial_conjunct="guru"), "UII")
        s2 = sc.scan_line("స త్యము", sc.ScanPolicy(word_initial_conjunct="guru")).syllables[0]
        self.assertEqual(s2.vikalpa, sc.VIKALPA_WORD_INITIAL)

    def test_repha_conjunct_is_a_vikalpa(self):
        s = sc.scan_line("చక్రి").syllables[0]
        self.assertEqual((s.weight, s.vikalpa), ("U", sc.VIKALPA_REPHA))
        self.assertEqual(pat("చక్రి", repha_conjunct="laghu"), "II")
        self.assertEqual(pat("ప్రస్తుతం"), "UIU")           # ప్ర before స్తు; స్తు itself is short
        self.assertEqual(pat("వాగ్రణి"), "UII")            # వా is long anyway: no vikalpa
        self.assertEqual(sc.scan_line("వాగ్రణి").syllables[0].vikalpa, "")

    def test_vikalpa_cleared_when_another_rule_applies(self):
        s = sc.scan_line("సం క్షమ").syllables[0]
        self.assertEqual(s.weight, "U")
        self.assertEqual(s.vikalpa, "")

    def test_bad_policy(self):
        with self.assertRaises(ValueError):
            sc.ScanPolicy(word_initial_conjunct="maybe")

    def test_last_syllable_never_gets_rule_5(self):
        self.assertEqual(pat("లోక ర"), "UII")


class TestLineScansion(unittest.TestCase):
    def test_pattern_matches_syllables(self):
        rng = random.Random(3)
        pool = "కఖగచజటడణతదనపబమయరలవశసహళ" + "ాిీుూెేైొోౌ" + "్ంఁః" + "   "
        for _ in range(300):
            line = "".join(rng.choice(pool) for _ in range(rng.randint(1, 40)))
            ls = sc.scan_line(line)
            self.assertEqual(len(ls.pattern), len(ls.syllables))
            self.assertTrue(set(ls.pattern) <= {"U", "I"})
            for s in ls.syllables:
                self.assertIn(s.weight, ("U", "I"))
                self.assertTrue(s.rules)

    def test_variants(self):
        ls = sc.scan_line("స త్యము చ క్రి")                 # స త్య ము చ క్రి
        self.assertEqual(ls.vikalpa_positions, (0, 3))
        v = ls.variants()
        self.assertEqual(v[0], ls.pattern)
        self.assertEqual(len(v), 4)
        self.assertEqual(len(set(v)), 4)
        self.assertEqual(sc.scan_line("రామ").variants(), ("UI",))
        self.assertEqual(len(sc.scan_line("స త్య స త్య స త్య స త్య").variants(limit=5)), 5)

    def test_format_and_dict(self):
        ls = sc.scan_line("శ్రీరాముని దయచేతను")
        self.assertEqual(ls.format(), "శ్రీ రా ము ని ద య చే త ను | UUIIIIUII | vikalpa@-")
        d = ls.to_dict()
        self.assertEqual(d["pattern"], "UUIIIIUII")
        self.assertEqual(len(d["syllables"]), 9)
        self.assertEqual(d["variants"], ["UUIIIIUII"])

    def test_split_lines_and_scan(self):
        self.assertEqual(sc.split_lines("a\n\n b \n"), ("a", "b"))
        self.assertEqual(sc.split_lines(["x", "", " y"]), ("x", "y"))
        self.assertEqual(sc.patterns("శ్రీరాముని దయచేతను\nధారాళమైన నీతులు"), ("UUIIIIUII", "UUIUIUII"))
        self.assertEqual(sc.patterns(["శ్రీరాముని దయచేతను", "ధారాళమైన నీతులు"]), ("UUIIIIUII", "UUIUIUII"))

    def test_nfc_normalisation(self):
        composed = "కై"
        decomposed = unicodedata.normalize("NFD", composed)
        self.assertNotEqual(composed, decomposed)
        self.assertEqual(sc.patterns(decomposed), sc.patterns(composed))

    def test_stanza_variants(self):
        scans = sc.scan("స త్యము\nరామ")
        v = sc.stanza_variants(scans)
        self.assertEqual(v[0], ("III", "UI"))
        self.assertEqual(len(v), 2)


class TestClassicsFromText(unittest.TestCase):
    def test_scanner_reproduces_the_hand_scansion(self):
        for st in FIX:
            if not st.get("text"):
                continue
            lines = [ln for ln in st["text"].splitlines() if ln.strip()]
            if len(lines) != len(st["lines"]):
                continue
            got = list(sc.patterns(lines))
            with self.subTest(id=st["id"]):
                self.assertEqual(got, st["lines"], "\n".join(s.format() for s in sc.scan(lines)))

    def test_identify_text_on_the_classics(self):
        for st in FIX:
            if not st.get("text") or len(st["text"].splitlines()) < 2:
                continue
            res = identify_text(st["text"], dawg())
            with self.subTest(id=st["id"]):
                self.assertTrue(res.identified, res.explain())
                self.assertEqual(res.best.meter, st["meter"], res.explain())
                self.assertEqual(len(res.scansions), len(st["lines"]))
                self.assertIn("scan 1.", res.explain())
                self.assertEqual(res.notes, ())
                self.assertIn("scansions", res.to_dict())

    def test_compound_boundary_reading(self):
        # Pothana 10.1-126.1-ఆ.: జొరఁగవ్యక్త is written without a space; the గ before వ్య must be laghu
        verse = ["సూక్ష్మభూతమందుఁజొరగఁ నా భూతంబు", "ప్రకృతిలోనఁ జొరఁగఁబ్రకృతి పోయి",
                 "వ్యక్తమందుఁ జొరఁగవ్యక్త మడంగను", "శేషసంజ్ఞ నీవుచెలువ మగుదు."]
        res = identify_text(verse, dawg())
        self.assertTrue(res.identified, res.explain())
        self.assertEqual(res.best.meter, "ataveladi")
        self.assertEqual(len(res.notes), 1)
        self.assertIn("compound-boundary", res.notes[0])
        self.assertIn("line 3 akshara 7 (గ)", res.notes[0])
        self.assertIn("line 2 akshara 8 (గఁ)", res.notes[0])
        self.assertEqual(res.best.lines[2].line, "UIUIIIIUIIUII")
        self.assertFalse(identify_text(verse, dawg(), try_variants=False).identified)

    def test_reading_options(self):
        from indic_meter_dawg.identify import reading_options
        scans = sc.scan("సత్యము చ క్రి")          # స త్య ము | చ | క్రి: చ is before a word-initial ర-vattu conjunct
        self.assertEqual(reading_options(scans, "canonical"), (("U", "I", "I", "I", "I"),))
        self.assertEqual(reading_options(scans, "vikalpa"), (("U", "I", "I", "IU", "I"),))
        self.assertEqual(reading_options(scans, "compound"), (("UI", "I", "I", "IU", "I"),))
        scans = sc.scan("సత్యము చక్రి")
        self.assertEqual(reading_options(scans, "canonical"), (("U", "I", "I", "U", "I"),))
        self.assertEqual(reading_options(scans, "vikalpa"), (("U", "I", "I", "UI", "I"),))
        with self.assertRaises(ValueError):
            reading_options(scans, "loose")

    def test_vikalpa_rescues_a_word_initial_conjunct(self):
        utp = next(st for st in FIX if st["id"] == "pothana-evvanice")["text"].splitlines()
        broken = list(utp)
        broken[0] = broken[0].replace("మెవ్వని", "మె వ్వని")     # the space blocks rule 5: canonical scan fails
        res = identify_text(broken, dawg())
        self.assertTrue(res.identified, res.explain())
        self.assertEqual(res.best.meter, "utpalamala")
        self.assertEqual(len(res.notes), 1)
        self.assertIn("vikalpa", res.notes[0])
        self.assertIn("line 1 akshara 10 (మె)", res.notes[0])
        res2 = identify_text(broken, dawg(), try_variants=False)
        self.assertFalse(res2.identified)
        res3 = identify_text(broken, dawg(), policy=sc.ScanPolicy(word_initial_conjunct="guru"))
        self.assertTrue(res3.identified)
        self.assertEqual(res3.notes, ())

    def test_identify_text_accepts_string_or_list(self):
        st = next(st for st in FIX if st["id"] == "sumati-sriramuni")
        a = identify_text(st["text"], dawg())
        b = identify_text(st["text"].splitlines(), dawg())
        self.assertEqual(a.lines, b.lines)
        self.assertEqual(a.best.meter, "kandamu")

    def test_reexports(self):
        self.assertIs(imd.identify_text, identify_text)
        self.assertIs(imd.scan, sc.scan)
        self.assertIs(imd.ScanPolicy, sc.ScanPolicy)


class TestCliScan(unittest.TestCase):
    def run_cli(self, argv):
        from indic_meter_dawg import cli
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue()

    def test_scan(self):
        code, out = self.run_cli(["scan", "శ్రీరాముని దయచేతను"])
        self.assertEqual(code, 0)
        self.assertIn("UUIIIIUII", out)
        code, out = self.run_cli(["scan", "--rules", "చక్రి"])
        self.assertIn("repha_conjunct", out)
        code, out = self.run_cli(["scan", "--json", "రామ"])
        import json
        self.assertEqual(json.loads(out)[0]["pattern"], "UI")
        code, out = self.run_cli(["scan", "--repha-conjunct", "laghu", "చక్రి"])
        self.assertIn("| II |", out)

    def test_identify_text(self):
        st = next(st for st in FIX if st["id"] == "sumati-sriramuni")
        code, out = self.run_cli(["identify", "--text", *st["text"].splitlines()])
        self.assertEqual(code, 0)
        self.assertIn("kandamu", out)
        self.assertIn("scan 1.", out)


if __name__ == "__main__":
    unittest.main()

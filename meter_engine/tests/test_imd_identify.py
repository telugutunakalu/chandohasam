# -*- coding: utf-8 -*-
"""identify.py — end-to-end identification against a brute-force oracle."""
import json
import random
import unittest

from imd_support import dawg, imd, mutate, oracle_meters, random_stanza
from indic_meter_dawg import grammar as gr
from indic_meter_dawg.identify import Candidate, Failure, IdentificationResult, identify

D = dawg()
CAT = D.catalogue


def cand_meters(res):
    return {c.meter for c in res.candidates}


class TestRandomStanzas(unittest.TestCase):
    def test_every_meter_is_recovered(self):
        rng = random.Random(51)
        for m in CAT.concrete:
            for _ in range(100):
                lines = random_stanza(m.name, rng)
                res = identify(lines, D)
                with self.subTest(m=m.name, lines=lines):
                    self.assertTrue(res.identified)
                    self.assertIn(m.name, cand_meters(res))
                    best = res.best
                    if not res.ambiguous:
                        self.assertTrue(best.meter == m.name or best.is_variant_of == m.name
                                        or m.is_variant_of == best.meter)

    def test_candidates_equal_oracle(self):
        rng = random.Random(52)
        for m in CAT.concrete:
            for _ in range(40):
                lines = random_stanza(m.name, rng)
                res = identify(lines, D)
                with self.subTest(m=m.name, lines=lines):
                    self.assertEqual(cand_meters(res), oracle_meters(lines, soft_stanza=True))

    def test_mutated_stanzas_equal_oracle(self):
        rng = random.Random(53)
        for m in CAT.concrete:
            for _ in range(40):
                lines = random_stanza(m.name, rng)
                i = rng.randrange(len(lines))
                lines[i] = mutate(lines[i], rng)
                res = identify(lines, D)
                with self.subTest(m=m.name, lines=lines):
                    self.assertEqual(cand_meters(res), oracle_meters(lines, soft_stanza=True))
                    if not res.identified:
                        self.assertTrue(res.failures)

    def test_random_junk_equals_oracle(self):
        rng = random.Random(54)
        for _ in range(300):
            n = rng.choice([2, 4, 4, 4, 6, 8])
            lines = ["".join(rng.choice("UI") for _ in range(rng.randint(6, 30))) for _ in range(n)]
            self.assertEqual(cand_meters(identify(lines, D)), oracle_meters(lines, soft_stanza=True))

    def test_padanta_off_equals_oracle_off(self):
        rng = random.Random(55)
        for m in CAT.concrete:
            lines = random_stanza(m.name, rng)
            lines[0] = lines[0][:-1] + "I"
            res = identify(lines, D, final_laghu_as_guru=False)
            self.assertEqual(cand_meters(res), oracle_meters(lines, final_laghu_as_guru=False, soft_stanza=True))

    def test_vritta_mutation_failure_names_line_and_akshara(self):
        rng = random.Random(56)
        for m in CAT.concrete:
            if not m.is_fixed:
                continue
            line = gr.canonical_line(D.grammars[(m.name, "all")])
            k = rng.randrange(2)
            i = rng.randrange(len(line) - 1)
            bad = line[:i] + ("U" if line[i] == "I" else "I") + line[i + 1:]
            lines = [line] * 4
            lines[k] = bad
            res = identify(lines, D)
            with self.subTest(m=m.name):
                self.assertNotIn(m.name, cand_meters(res))
                if not res.identified:
                    f = next(f for f in res.failures if f.meter == m.name)
                    self.assertEqual(f.line_no, k + 1)
                    self.assertEqual(f.akshara, i + 1)
                    self.assertEqual(f.lines_survived, k)


class TestRankingAndAmbiguity(unittest.TestCase):
    def test_all_laghu_30_is_ambiguous_between_seesam_and_taruvoja(self):
        res = identify(["I" * 30] * 4, D)
        self.assertTrue(res.ambiguous)
        self.assertEqual(cand_meters(res), {"seesamu", "taruvoja"})
        self.assertIn("AMBIGUOUS", res.explain())
        res = identify(["I" * 36] * 4, D)
        self.assertEqual(res.best.meter, "seesamu")                # all-laghu form: 6 నలల + 2 న, Pothana 11-72
        self.assertEqual(res.best.lines[0].slot, "laghu")
        self.assertFalse(res.ambiguous)
        res = identify(["I" * 20, "I" * 16] * 4, D)                # printed as halves
        self.assertEqual(res.best.meter, "seesamu")

    def test_seesamu_forms_do_not_mix(self):
        regular = "UII" * 6 + "UI" * 2                             # 6 భ + 2 హ
        self.assertEqual(identify([regular] * 4, D).best.lines[0].slot, "all")
        self.assertNotIn("seesamu", cand_meters(identify([regular, "I" * 36, regular, "I" * 36], D)))

    def test_stanza_layer_separates_ataveladi_from_tetagiti(self):
        res = identify(["I" * 17] * 4, D)
        self.assertEqual(res.best.meter, "tetagiti")
        self.assertFalse(res.ambiguous)
        res = identify(["I" * 17, "I" * 15, "I" * 17, "I" * 15], D)
        self.assertEqual(res.best.meter, "ataveladi")
        self.assertFalse(res.ambiguous)

    def test_exact_ranks_above_padanta(self):
        vid = "UUUUUUUU"
        res = identify([vid[:-1] + "I"] * 4, D)
        self.assertEqual({c.meter for c in res.candidates}, {"vidyunmala", "madhuragati_ragada"})
        self.assertTrue(all(c.uses_padanta for c in res.candidates))
        self.assertTrue(res.ambiguous)
        res = identify([vid] * 4, D)
        self.assertEqual(res.best.meter, "vidyunmala")

    def test_seesam_with_gita_trailer(self):
        rng = random.Random(57)
        for gita in ("tetagiti", "ataveladi"):
            lines = random_stanza("seesamu", rng) + random_stanza(gita, rng)
            res = identify(lines, D)
            with self.subTest(gita=gita):
                self.assertTrue(res.identified)
                labels = {c.label for c in res.candidates}
                self.assertIn(f"seesamu+{gita}", labels)
                c = next(c for c in res.candidates if c.label == f"seesamu+{gita}")
                self.assertEqual(len(c.lines), 4)
                self.assertEqual(c.trailer.meter, gita)
                self.assertEqual([lm.line_no for lm in c.trailer.lines], [5, 6, 7, 8])
                self.assertIn("followed by", res.explain())

    def test_seesam_printed_as_half_lines(self):
        from indic_meter_dawg.parser import segment
        rng = random.Random(59)
        for _ in range(20):
            padas = random_stanza("seesamu", rng)
            halves = []
            for ln in padas:
                seg = segment("seesamu", "all", ln, D)[0]
                cut = seg.segments[4].start - 1              # the 5th gana starts the second half
                halves += [ln[:cut], ln[cut:]]
            res = identify(halves, D)
            with self.subTest(padas=padas):
                self.assertIn("seesamu", cand_meters(res))
                c = next(c for c in res.candidates if c.meter == "seesamu")
                self.assertEqual(len(c.lines), 4)
                self.assertTrue(any("half-lines" in n for n in c.notes))
                self.assertEqual([lm.line for lm in c.lines], padas)
            gita = random_stanza("tetagiti", rng)
            res = identify(halves + gita, D)
            self.assertIn("seesamu+tetagiti", {c.label for c in res.candidates})
            self.assertEqual(next(c for c in res.candidates if c.label == "seesamu+tetagiti").trailer.lines[0].line_no, 9)
            self.assertIn("seesamu", cand_meters(identify(padas, D)))       # whole padas still work

    def test_halves_do_not_apply_to_other_meters(self):
        rng = random.Random(60)
        lines = random_stanza("kandamu", rng)
        halves = [ln[:len(ln) // 2] for ln in lines] + [ln[len(ln) // 2:] for ln in lines]
        self.assertEqual(cand_meters(identify(halves, D)), oracle_meters(halves, soft_stanza=True))

    def test_repeatable_units(self):
        rng = random.Random(58)
        lines = random_stanza("dvipada", rng, units=4)
        res = identify(lines, D)
        self.assertIn("dvipada", cand_meters(res))
        c = next(c for c in res.candidates if c.meter == "dvipada")
        self.assertEqual(c.units, 4)
        self.assertEqual(len(c.lines), 8)

    def test_option_lines(self):
        line = gr.canonical_line(D.grammars[("utpalamala", "all")])
        opts = [c + ("I" if c == "U" else "U") if i % 5 == 0 else c for i, c in enumerate(line)]
        res = identify([opts] * 4, D)
        self.assertEqual(res.best.meter, "utpalamala")
        self.assertEqual([lm.line for lm in res.best.lines], [line] * 4)
        self.assertEqual(res.lines, tuple("".join(o[0] for o in opts) for _ in range(4)))
        res = identify([["UI"] * 5] * 4, D)
        self.assertFalse(res.identified)
        res = identify([tuple("I" * 15), tuple("I" * 15)] * 4, D)
        self.assertIn("seesamu", cand_meters(res))

    def test_stanza_rule_breach_is_reported_not_fatal(self):
        # Pothana 3-616-క.: a valid kanda whose lines start I, I, I, U
        lines = ["IIUIIIIUU", "IIUIIUIUIIIIIUU", "IIIIIIIIUU", "UIIUIIIIIIUIIUU"]
        res = identify(lines, D)
        self.assertEqual(res.best.meter, "kandamu")
        self.assertEqual(len(res.best.violations), 1)
        self.assertIn("first_akshara_weight_uniform", res.best.violations[0])
        self.assertTrue(any("stanza rule broken" in n for n in res.best.notes))
        self.assertIn("stanza rule broken", res.explain())
        self.assertEqual(res.to_dict()["candidates"][0]["violations"], list(res.best.violations))
        clean = ["UUUUUU", "UU" + "IIII" + "IUI" + "IIII" + "IIU", "UUUUUU", "UU" + "IIII" + "IUI" + "IIII" + "IIU"]
        self.assertEqual(identify(clean, D).best.violations, ())

    def test_empty_input(self):
        res = identify([], D)
        self.assertFalse(res.identified)
        self.assertEqual(res.lines, ())

    def test_failures_sorted_most_informative_first(self):
        line = gr.canonical_line(D.grammars[("utpalamala", "all")])
        bad = line[:15] + ("U" if line[15] == "I" else "I") + line[16:]
        res = identify([line, line, line, bad], D)
        self.assertFalse(res.identified)
        self.assertEqual(res.failures[0].meter, "utpalamala")
        self.assertEqual(res.failures[0].lines_survived, 3)
        self.assertTrue(all(f.akshara is not None for f in res.failures if f.lines_survived == 3))


class TestResultApi(unittest.TestCase):
    def test_line_matches_carry_ganas_and_yati(self):
        res = identify(["UIIUIUIIIUIIUIIUIUIU"] * 4, D)
        c = res.best
        self.assertIsInstance(c, Candidate)
        self.assertEqual(c.name_te, "ఉత్పలమాల")
        self.assertEqual(c.family, "vrutta")
        self.assertEqual([lm.line_no for lm in c.lines], [1, 2, 3, 4])
        self.assertEqual(c.lines[0].segmentation.gana_names, ("భ", "ర", "న", "భ", "భ", "ర", "వ"))
        self.assertEqual(c.lines[0].segmentation.yati_aksharas, (10,))
        self.assertEqual(c.lines[0].n_parses, 1)

    def test_to_dict_and_json_roundtrip(self):
        res = identify(["UIIUIUIIIUIIUIIUIUIU"] * 4, D)
        d = res.to_dict()
        self.assertEqual(d["best"], "utpalamala")
        self.assertTrue(d["identified"])
        self.assertFalse(d["ambiguous"])
        self.assertEqual(d["candidates"][0]["lines"][0]["yati_aksharas"], [10])
        self.assertEqual(json.loads(res.to_json())["best"], "utpalamala")
        res2 = identify(["UIUI"] * 4, D)
        d2 = res2.to_dict()
        self.assertIsNone(d2["best"])
        self.assertTrue(d2["failures"])
        json.loads(res2.to_json())

    def test_explain_mentions_meter_and_ganas(self):
        text = identify(["UIIUIUIIIUIIUIIUIUIU"] * 4, D).explain()
        self.assertIn("utpalamala", text)
        self.assertIn("భ ర న భ భ ర వ", text)
        self.assertIn("yati@10", text)

    def test_notation_tolerant(self):
        res = identify(["గలల గలగ లలల గలల గలల గలగ లగ"] * 4, D)
        self.assertEqual(res.best.meter, "utpalamala")

    def test_reexports(self):
        self.assertIs(imd.identify, identify)
        self.assertIs(imd.IdentificationResult, IdentificationResult)
        self.assertIs(imd.Candidate, Candidate)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""ganas.py — registry integrity and token resolution."""
import unittest

import yaml

from imd_support import HERE, imd
from indic_meter_dawg import ganas as gn
from indic_meter_dawg import symbols as sy

REG = gn.load_registry()
RAW = yaml.safe_load(open(HERE.parent / "ganas.yaml", encoding="utf-8"))


class TestRegistryIntegrity(unittest.TestCase):
    def test_every_pattern_unique(self):
        pats = [g.pattern for g in REG.ganas]
        self.assertEqual(len(pats), len(set(pats)))

    def test_matras_and_aksharas_consistent_with_pattern(self):
        for g in REG.ganas:
            with self.subTest(g=g.name):
                self.assertEqual(g.matras, sy.matras(g.pattern))
                self.assertEqual(g.aksharas, len(g.pattern))

    def test_yaml_matras_agree_with_pattern(self):
        sections = [RAW[k]["ganas"] for k in ("ekakshara_ganas", "dvyakshara_ganas", "trika_ganas")]
        sections += [RAW["upaganas"][k]["ganas"] for k in ("surya_ganas", "indra_ganas", "chandra_ganas", "kanda_ganas")]
        for recs in sections:
            for rec in recs:
                with self.subTest(g=rec["name"]):
                    self.assertEqual(rec["matras"], sy.matras(rec["pattern"]))
                    self.assertEqual(rec["aksharas"], len(rec["pattern"]))

    def test_eight_trika_ganas_cover_all_three_letter_patterns(self):
        trika = {g.pattern for g in REG.ganas if g.group == "trika"}
        self.assertEqual(trika, {a + b + c for a in "UI" for b in "UI" for c in "UI"})

    def test_class_memberships(self):
        self.assertEqual({g.pattern for g in REG.classes["surya"]}, {"III", "UI"})
        self.assertEqual({g.pattern for g in REG.classes["indra"]}, {"UII", "UIU", "UUI", "IIII", "IIIU", "IIUI"})
        self.assertEqual({g.pattern for g in REG.classes["kanda"]}, {"UII", "IUI", "IIU", "IIII", "UU"})
        self.assertEqual(len(REG.classes["chandra"]), 13)

    def test_every_kanda_gana_is_four_matras(self):
        for g in REG.classes["kanda"]:
            self.assertEqual(g.matras, 4)

    def test_surya_and_indra_disjoint(self):
        self.assertFalse(set(REG.classes["surya"]) & set(REG.classes["indra"]))

    def test_by_telugu_and_by_name_point_to_same_objects(self):
        for name, telugu in (("bha", "భ"), ("ja", "జ"), ("sa", "స"), ("na", "న"), ("ya", "య"),
                             ("ra", "ర"), ("ta", "త"), ("ma", "మ"), ("nala", "నల"), ("gaa", "గా"), ("va", "వ"), ("ha", "హ")):
            with self.subTest(name=name):
                self.assertIs(REG.by_name[name], REG.by_telugu[telugu])

    def test_single_letters(self):
        self.assertEqual(REG.by_telugu["గ"].pattern, "U")
        self.assertEqual(REG.by_telugu["ల"].pattern, "I")

    def test_gana_is_hashable_and_ordered(self):
        s = {REG.by_name["bha"], REG.by_name["bha"], REG.by_name["ja"]}
        self.assertEqual(len(s), 2)
        self.assertLess(sorted(s)[0], sorted(s)[1])

    def test_cached_loader(self):
        self.assertIs(gn.load_registry(), REG)
        self.assertIs(imd.load_registry, gn.load_registry)


class TestResolveToken(unittest.TestCase):
    def pats(self, tok):
        return [g.pattern for g in REG.resolve(tok)]

    def test_literal_trika_and_dvyakshara(self):
        for tok, want in (("భ", "UII"), ("ర", "UIU"), ("న", "III"), ("వ", "IU"), ("గా", "UU"), ("హ", "UI"),
                          ("గ", "U"), ("ల", "I"), ("bha", "UII"), ("gaa", "UU"), ("laga", "IU"), ("gaga", "UU")):
            with self.subTest(tok=tok):
                self.assertEqual(self.pats(tok), [want])

    def test_classes(self):
        self.assertEqual(self.pats("surya"), ["III", "UI"])
        self.assertEqual(len(self.pats("indra")), 6)
        self.assertEqual(len(self.pats("kanda")), 5)
        self.assertEqual(self.pats("సూర్య"), self.pats("surya"))
        self.assertEqual(self.pats("ఇంద్ర"), self.pats("indra"))

    def test_matra_tokens(self):
        self.assertEqual(self.pats("m3"), ["IU", "UI", "III"])
        self.assertEqual(self.pats("m4"), ["UU", "IIU", "IUI", "UII", "IIII"])
        self.assertEqual(len(self.pats("m5")), 8)
        for g in REG.resolve("m5"):
            self.assertEqual(g.matras, 5)

    def test_matra_tokens_keep_known_names(self):
        names = {g.pattern: g.telugu for g in REG.resolve("m4")}
        self.assertEqual(names["UII"], "భ")
        self.assertEqual(names["IIII"], "నల")
        self.assertEqual(names["UU"], "గా")

    def test_matra_token_synthesises_unknown(self):
        g = REG.gana_for_pattern("IUIIU")
        self.assertTrue(g.name.startswith("m7:"))    # 1+2+1+1+2 matras
        self.assertEqual(g.telugu, "లగలలగ")

    def test_all_laghu(self):
        self.assertEqual(self.pats("all_laghu(indra)"), ["IIII"])
        self.assertEqual(self.pats("all_laghu(surya)"), ["III"])
        self.assertEqual(self.pats("all_laghu(kanda)"), ["IIII"])
        self.assertEqual(self.pats("all_laghu(m3)"), ["III"])

    def test_all_laghu_empty_raises(self):
        with self.assertRaises(gn.GanaError):
            REG.resolve("all_laghu(భ)")

    def test_canonical_pattern_token(self):
        self.assertEqual(self.pats("UIU"), ["UIU"])
        self.assertEqual(REG.resolve("UIU")[0].telugu, "ర")

    def test_unknown_tokens_raise(self):
        for bad in ("foo", "m", "mx", "ఐ", "", "all_laghu(", "surya2"):
            with self.subTest(bad=bad):
                with self.assertRaises(gn.GanaError):
                    REG.resolve(bad)

    def test_whitespace_tolerated(self):
        self.assertEqual(self.pats(" భ "), ["UII"])

    def test_class_of(self):
        self.assertEqual(gn.class_of(REG, REG.by_telugu["న"]), ("surya",))
        self.assertEqual(gn.class_of(REG, REG.by_telugu["భ"]), ("indra", "kanda"))
        self.assertEqual(gn.class_of(REG, REG.by_telugu["మ"]), ())

    def test_describe(self):
        self.assertEqual(REG.describe(REG.by_telugu["భ"]), "భ (bha) UII")


if __name__ == "__main__":
    unittest.main()

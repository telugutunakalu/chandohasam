# -*- coding: utf-8 -*-
"""catalogue.py — meter_rules.yaml is structurally sound and typed correctly."""
import copy
import tempfile
import unittest
from pathlib import Path

import yaml

from imd_support import HERE, imd
from indic_meter_dawg import catalogue as ct
from indic_meter_dawg import ganas as gn

CAT = ct.load_catalogue()
REG = gn.load_registry()
RAW = yaml.safe_load(open(HERE.parent / "meter_rules.yaml", encoding="utf-8"))


class TestLoad(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(CAT.meters), 37)
        self.assertEqual(len(CAT.concrete), 37)
        self.assertEqual([m.name for m in CAT.meters if m.abstract], [])

    def test_ids_and_names_unique_and_ordered(self):
        ids = [m.id for m in CAT.meters]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(set(ids)), len(ids))
        self.assertEqual(len({m.name for m in CAT.meters}), len(ids))

    def test_families_from_meters_txt(self):
        fam = {}
        for m in CAT.meters:
            fam[m.family] = fam.get(m.family, 0) + 1
        self.assertEqual(fam, {"vrutta": 26, "jati": 8, "upajati": 3})

    def test_telugu_names_present(self):
        self.assertEqual(CAT.get("utpalamala").name_te, "ఉత్పలమాల")
        self.assertEqual(CAT.get("kandamu").name_te, "కందము")

    def test_variants(self):
        self.assertEqual(CAT.get("hayapracara_ragada").is_variant_of, "turagagati_ragada")
        self.assertIsNone(CAT.get("turagagati_ragada").is_variant_of)
        self.assertEqual([m.name for m in CAT.variants_of("turagagati_ragada")], ["hayapracara_ragada"])
        self.assertEqual(CAT.variant_depth("turagagati_ragada"), 0)
        self.assertEqual(CAT.variant_depth("hayapracara_ragada"), 1)

    def test_seesamu_has_the_all_laghu_alternative(self):
        s = CAT.get("seesamu")
        self.assertEqual(s.slot_patterns, (("all",) * 4, ("laghu",) * 4))
        self.assertEqual(s.slots["laghu"], ("నలల",) * 6 + ("న",) * 2)
        self.assertEqual(s.aksharalu, (22, 36))

    def test_get_unknown(self):
        with self.assertRaises(ct.CatalogueError):
            CAT.get("nope")

    def test_every_concrete_meter_has_structure(self):
        for m in CAT.concrete:
            with self.subTest(m=m.name):
                self.assertIn(m.system, ct.SYSTEMS)
                self.assertTrue(m.slots)
                self.assertEqual(len(m.slot_pattern), m.padalu)
                for s in m.slot_pattern:
                    self.assertIn(s, m.slots)

    def test_fixed_meters_are_the_vrittas(self):
        for m in CAT.concrete:
            with self.subTest(m=m.name):
                self.assertEqual(m.is_fixed, m.family == "vrutta")

    def test_fixed_meter_length_matches_aksharalu(self):
        for m in CAT.concrete:
            if not m.is_fixed:
                continue
            n = sum(len(REG.resolve(t)[0].pattern) for t in m.slots["all"])
            with self.subTest(m=m.name):
                self.assertEqual(m.aksharalu, (n, n))

    def test_fixed_meter_ganas_match_ganalu_column(self):
        for m in CAT.concrete:
            if not m.is_fixed:
                continue
            with self.subTest(m=m.name):
                self.assertEqual(list(m.slots["all"]), [t.strip() for t in m.ganalu_text.split(",")])

    def test_yati_lists_match_legacy_yati_column(self):
        raw = {r["name"]: r for r in RAW["meters"]}
        for m in CAT.concrete:
            legacy = raw[m.name]["yati"]
            with self.subTest(m=m.name):
                if m.is_fixed:
                    self.assertEqual(m.yati_aksharas["all"], tuple(p for p in legacy[0] if p > 1))
                else:
                    for i, slot in enumerate(m.slot_pattern):
                        self.assertEqual(m.yati_for(slot), tuple(p for p in legacy[i] if p > 1))

    def test_slot_patterns(self):
        self.assertEqual(CAT.get("kandamu").slot_pattern, ("odd", "even", "odd", "even"))
        self.assertEqual(CAT.get("ataveladi").slot_pattern, ("odd", "even", "odd", "even"))
        self.assertEqual(CAT.get("dvipada").slot_pattern, ("all", "all"))
        self.assertTrue(CAT.get("dvipada").repeatable)
        self.assertFalse(CAT.get("kandamu").repeatable)
        self.assertEqual(CAT.get("seesamu").followed_by, ("ataveladi", "tetagiti"))
        self.assertEqual(CAT.get("seesamu").halves_per_line, 2)
        self.assertEqual(CAT.get("kandamu").halves_per_line, 1)

    def test_kanda_constraints(self):
        k = CAT.get("kandamu")
        rules = [(c.rule, c.slot, c.positions, c.ganas) for c in k.constraints]
        self.assertIn(("forbid_gana", "odd", (1, 3), ("జ",)), rules)
        self.assertIn(("forbid_gana", "even", (2, 4), ("జ",)), rules)
        self.assertIn(("require_gana", "even", (3,), ("జ", "నల")), rules)
        self.assertIn(("line_ends_with", "even", (), ()), rules)
        self.assertEqual([c.rule for c in k.stanza_constraints], ["first_akshara_weight_uniform"])

    def test_prasa_flags_preserved(self):
        self.assertTrue(CAT.get("utpalamala").prasa)
        self.assertFalse(CAT.get("seesamu").prasa)
        self.assertTrue(CAT.get("seesamu").prasa_yati)

    def test_validate_clean(self):
        self.assertEqual(ct.validate_catalogue(CAT, REG), [])

    def test_loader_cached_and_reexported(self):
        self.assertIs(ct.load_catalogue(), CAT)
        self.assertIs(imd.load_catalogue, ct.load_catalogue)


class TestValidationCatchesCorruption(unittest.TestCase):
    """Write a corrupted copy of the yaml and make sure the loader refuses it."""

    def _load_with(self, mutate):
        data = copy.deepcopy(RAW)
        mutate(data)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "meter_rules.yaml"
            p.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
            return ct.load_catalogue(str(p), str(HERE.parent / "meters.txt"))

    def _expect_error(self, mutate, fragment):
        with self.assertRaises(ct.CatalogueError) as cm:
            self._load_with(mutate)
        self.assertIn(fragment, str(cm.exception))

    def _meter(self, data, name):
        return next(m for m in data["meters"] if m["name"] == name)

    def test_missing_structure(self):
        self._expect_error(lambda d: self._meter(d, "tetagiti").pop("structure"), "no structure block")

    def test_wrong_padalu(self):
        self._expect_error(lambda d: self._meter(d, "tetagiti").__setitem__("padalu", 3), "padalu is 3")

    def test_unknown_token(self):
        self._expect_error(lambda d: self._meter(d, "tetagiti")["structure"]["slots"].__setitem__("all", ["surya", "bogus"]),
                           "unknown gana token")

    def test_undefined_slot_in_pattern(self):
        self._expect_error(lambda d: self._meter(d, "ataveladi")["structure"].__setitem__("slot_pattern", ["odd", "x", "odd", "even"]),
                           "undefined slot")

    def test_yati_out_of_range(self):
        self._expect_error(lambda d: self._meter(d, "tetagiti")["structure"].__setitem__("yati_ganas", [9]), "outside 1..5")
        self._expect_error(lambda d: self._meter(d, "vidyunmala")["structure"].__setitem__("yati_aksharas", [9]), "outside 1..8")

    def test_unknown_constraint_rule(self):
        self._expect_error(lambda d: self._meter(d, "kandamu")["structure"]["constraints"].append({"rule": "magic", "slot": "odd"}),
                           "unknown constraint rule")

    def test_unknown_stanza_rule(self):
        self._expect_error(lambda d: self._meter(d, "kandamu")["structure"]["stanza_constraints"].append({"rule": "magic"}),
                           "unknown stanza rule")

    def test_bad_variant_link(self):
        self._expect_error(lambda d: self._meter(d, "hayapracara_ragada")["structure"].__setitem__("is_variant_of", "ghost"),
                           "is_variant_of unknown")

    def test_bad_alt_slot_pattern(self):
        self._expect_error(lambda d: self._meter(d, "seesamu")["structure"].__setitem__("alt_slot_patterns", [["laghu", "ghost", "laghu", "laghu"]]),
                           "undefined slot")
        self._expect_error(lambda d: self._meter(d, "seesamu")["structure"].__setitem__("alt_slot_patterns", [["laghu"]]),
                           "padalu is 4")

    def test_bad_followed_by(self):
        self._expect_error(lambda d: self._meter(d, "seesamu")["structure"].__setitem__("followed_by", ["ghost"]),
                           "followed_by unknown")

    def test_aksharalu_mismatch(self):
        self._expect_error(lambda d: self._meter(d, "utpalamala").__setitem__("aksharalu", {"min": 19, "max": 20}),
                           "aksharalu.min 19")

    def test_bad_halves(self):
        self._expect_error(lambda d: self._meter(d, "seesamu")["structure"].__setitem__("halves_per_line", 0), "halves_per_line")
        self._expect_error(lambda d: self._meter(d, "dvipada")["structure"].__setitem__("halves_per_line", 2), "repeatable")

    def test_class_token_in_fixed_meter(self):
        self._expect_error(lambda d: self._meter(d, "vidyunmala")["structure"]["slots"].__setitem__("all", ["surya", "మ", "గా"]),
                           "class token")

    def test_validate_false_skips_checks(self):
        data = copy.deepcopy(RAW)
        self._meter(data, "tetagiti")["padalu"] = 3
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "m.yaml"
            p.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
            cat = ct.load_catalogue(str(p), str(HERE.parent / "meters.txt"), validate=False)
        self.assertEqual(cat.get("tetagiti").padalu, 3)
        self.assertTrue(ct.validate_catalogue(cat, REG))


if __name__ == "__main__":
    unittest.main()

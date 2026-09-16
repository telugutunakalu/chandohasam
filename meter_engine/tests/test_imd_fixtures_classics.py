# -*- coding: utf-8 -*-
"""Hand-scanned classical stanzas (tests/fixtures/classics.yaml)."""
import unittest

import yaml

from imd_support import FIXTURES, dawg
from indic_meter_dawg.identify import identify
from indic_meter_dawg.parser import segment

D = dawg()
FIX = yaml.safe_load(open(FIXTURES / "classics.yaml", encoding="utf-8"))["stanzas"]


class TestClassics(unittest.TestCase):
    def test_fixture_file_is_well_formed(self):
        self.assertGreaterEqual(len(FIX), 4)
        for st in FIX:
            self.assertIn(st["meter"], D.catalogue.by_name)
            self.assertEqual(len(st["lines"]), D.spec(st["meter"]).padalu)

    def test_each_stanza_identifies_as_expected(self):
        for st in FIX:
            res = identify(st["lines"], D)
            with self.subTest(id=st["id"]):
                self.assertTrue(res.identified, res.explain())
                self.assertIn(st["meter"], {c.meter for c in res.candidates}, res.explain())
                self.assertEqual(res.best.meter, st["meter"], res.explain())
                self.assertFalse(res.best.uses_padanta)

    def test_gana_segmentation_matches_hand_analysis(self):
        for st in FIX:
            if "ganas" not in st:
                continue
            spec = D.spec(st["meter"])
            for i, (line, ganas, slot) in enumerate(zip(st["lines"], st["ganas"], spec.slot_pattern)):
                segs = segment(st["meter"], slot, line, D)
                names = [tuple(s.gana_names) for s in segs]
                with self.subTest(id=st["id"], line=i + 1):
                    self.assertIn(tuple(ganas), names)

    def test_kanda_stanzas_pass_the_uniform_first_akshara_rule(self):
        for st in FIX:
            if st["meter"] == "kandamu":
                self.assertEqual(len({ln[0] for ln in st["lines"]}), 1)


if __name__ == "__main__":
    unittest.main()

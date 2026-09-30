"""Tests of the mādhurya metric.

    cd poetry_metrics && python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import madhurya as md                                                  # noqa: E402
import validation_madhurya as vm                                       # noqa: E402
from common.phonology import SONORITY, line_aksharas, parse_akshara    # noqa: E402
from common.translit import iast_to_telugu                             # noqa: E402

BASELINE = md.load_baseline()


def classes(text: str) -> list:
    """[(akshara, class, rules)] of a line."""
    out, prev = [], None
    for a in line_aksharas(text):
        cls, rules = md.classify(a, md.closes_with_nasal(prev, a))
        out.append((a.text, cls, rules))
        prev = a
    return out


def cls(text: str, which: int = -1) -> str:
    return classes(text)[which][1]


class Parsing(unittest.TestCase):
    def test_onset_vowel_coda(self):
        a = parse_akshara("స్త్రీ")
        self.assertEqual((a.onset, a.vowel, a.coda), (("స", "త", "ర"), "ఈ", ()))
        a = parse_akshara("దన్")
        self.assertEqual((a.onset, a.vowel, a.coda), (("ద",), "అ", ("న",)))
        a = parse_akshara("సం")
        self.assertEqual((a.onset, a.vowel, a.coda), (("స",), "అ", ("ం",)))
        a = parse_akshara("ఐ")
        self.assertEqual((a.onset, a.vowel, a.coda), ((), "ఐ", ()))

    def test_vowelless_chunk_is_not_scored(self):
        a = parse_akshara("న్")
        self.assertEqual((a.onset, a.vowel, a.coda), ((), "", ("న",)))
        self.assertEqual(md.classify(a), (None, []))

    def test_transliteration(self):
        self.assertEqual(iast_to_telugu("śāntāparacintanāni"), "శాన్తాపరచిన్తనాని")
        self.assertEqual(iast_to_telugu("kṛṣṇaḥ"), "కృష్ణః")
        self.assertEqual(iast_to_telugu("yat prayāsaḥ"), "యత్ ప్రయాసః")


class Classes(unittest.TestCase):
    def test_madhura_after_the_anusvara(self):               # M1
        self.assertEqual(classes("చందన")[1], ("ద", "madhura", ["M1"]))
        self.assertEqual(cls("అంకము", 1), "madhura")
        self.assertEqual(cls("సున్దర", 1), "madhura")          # the class nasal written as a conjunct
        self.assertEqual(cls("రుచిం దగ", 2), "madhura")        # across a space
        self.assertEqual(cls("చెదన్ దలచి", 2), "madhura")      # a final న్ before its own varga

    def test_doubled_nasal_is_madhura(self):
        self.assertEqual(classes("అన్న")[1], ("న్న", "madhura", ["M1"]))
        self.assertEqual(cls("అమ్మ"), "madhura")

    def test_light_ra_and_na(self):                          # M2
        self.assertEqual(classes("రవి")[0], ("ర", "madhura", ["M2"]))
        self.assertEqual(cls("గుణ"), "madhura")
        self.assertEqual(cls("రామ", 0), "sonorant")            # a long vowel
        self.assertEqual(cls("రంగు", 0), "sonorant")           # a coda

    def test_parusha_rules(self):
        self.assertEqual(classes("బుద్ధి")[1][1:], ("parusha", ["P1"]))
        self.assertEqual(classes("ప్రభ")[0][1:], ("parusha", ["P2"]))
        self.assertEqual(classes("అర్క")[1][1:], ("parusha", ["P2"]))
        self.assertEqual(classes("అక్క")[1][1:], ("parusha", ["P3"]))
        self.assertEqual(classes("కోటి")[1][1:], ("parusha", ["P4"]))
        self.assertEqual(classes("శివ")[0][1:], ("parusha", ["P5"]))
        self.assertEqual(classes("పక్షి")[1][1:], ("parusha", ["P5"]))
        self.assertEqual(classes("గట్టి")[1][1:], ("parusha", ["P3", "P4"]))

    def test_retroflex_stop_is_harsh_even_after_the_anusvara(self):
        self.assertEqual(cls("కొండ"), "parusha")
        self.assertEqual(cls("గంట"), "parusha")

    def test_middle_classes_follow_the_sonority_scale(self):
        self.assertEqual([cls(t, 0) for t in ("మ", "ల", "వ", "య", "అ")], ["sonorant"] * 5)
        self.assertEqual([cls(t, 0) for t in ("గ", "జ", "ద", "బ", "ధ")], ["voiced"] * 5)
        self.assertEqual([cls(t, 0) for t in ("క", "చ", "త", "ప", "స", "హ")], ["voiceless"] * 6)
        self.assertEqual(cls("మల్లె"), "sonorant")              # a doubled sonorant keeps its class
        self.assertEqual([cls(t) for t in ("అస్త", "సత్య", "విద్య")], ["conjunct"] * 3)


class Inventory(unittest.TestCase):
    def test_weighted_mean(self):
        # చం voiceless, ద M1, న sonorant, ము sonorant -> (-0.5 + 1 + 0.5 + 0.5) / 4
        prof = md.profile_line("చందనము")
        self.assertAlmostEqual(prof.inventory, 0.375)
        self.assertEqual(prof.n, 4)

    def test_sonority_score(self):
        # మ (7) అ (17) న (7) అ (17)
        self.assertAlmostEqual(md.profile_line("మన").sonority, 12.0)
        self.assertEqual((SONORITY["అ"], SONORITY["య"], SONORITY["ం"], SONORITY["క"]), (17, 12, 7, 1))

    def test_adjacency_runs_through_the_poem(self):
        profiles = md.profile_poem(["పొందికం", "జెందె"])
        self.assertEqual(profiles[1].rules["M1"], 2)            # జె after the line-final ం, and దె
        self.assertEqual(md.profile_line("జెందె").rules["M1"], 1)


class Sequence(unittest.TestCase):
    """Harsh aksharas next to each other cost more than the same aksharas apart."""

    def test_no_pileup_when_harsh_aksharas_stand_apart(self):
        prof = md.profile_line("కమకమకమ")                       # voiceless, sonorant, ...
        self.assertEqual(prof.pileup, 0.0)
        self.assertEqual(prof.index(), prof.inventory)
        self.assertEqual(prof.runs, [])

    def test_the_same_aksharas_together_score_lower(self):
        apart, together = md.profile_line("కమకమకమ"), md.profile_line("కకకమమమ")
        self.assertEqual(apart.inventory, together.inventory)
        self.assertLess(together.index(), apart.index())
        # the run క క క carries 0 + 0.5 + 1.0 to its three aksharas
        self.assertAlmostEqual(together.pileup, 1.5 / 6)

    def test_each_further_harsh_akshara_costs_more(self):
        costs = []
        for n in (1, 2, 3, 4):
            prof = md.profile_line("ట" * n)
            costs.append(-(prof.weight_sum - prof.pileup_sum))   # total charge of the run
        self.assertEqual(costs, [1, 3, 6, 10])                   # 1, 1+2, 1+2+3, ...
        steps = [b - a for a, b in zip(costs, costs[1:])]
        self.assertEqual(steps, sorted(steps))
        self.assertEqual(len(set(steps)), len(steps))

    def test_any_other_akshara_ends_the_run(self):
        for breaker in ("మ", "గ", "అ"):                         # sonorant, voiced, vowel
            prof = md.profile_line("టట" + breaker + "టట")
            self.assertAlmostEqual(prof.pileup_sum, 2.0, msg=breaker)   # 1 carried in each pair
            self.assertEqual([r.load for r in prof.runs], [2.0, 2.0])

    def test_runs_cross_line_ends(self):
        profiles = md.profile_poem(["మట", "టమ"])
        self.assertEqual(profiles[0].pileup_sum, 0.0)
        self.assertEqual(profiles[1].pileup_sum, 1.0)            # the second ట carries the first
        self.assertEqual(len(profiles[0].runs), 1)               # filed under the line it began in
        self.assertEqual("".join(profiles[0].runs[0].aksharas), "టట")

    def test_matches_the_validation_formula(self):
        line = "దుర్వారోద్యమ బాహువిక్రమ రసాస్తోక ప్రతాపస్ఫుర"
        prof = md.profile_line(line)
        seq = vm.class_sequence([line])
        self.assertAlmostEqual(prof.index(), vm.run_index(seq, md.WEIGHTS))
        self.assertAlmostEqual(prof.pileup, vm.pileup(seq, md.WEIGHTS))

    def test_runs_test(self):
        self.assertLess(vm.runs_z([True] * 6 + [False] * 6), -2)         # clumped
        self.assertGreater(vm.runs_z([True, False] * 6), 2)             # alternating
        self.assertIsNone(vm.runs_z([True, False, False]))

    def test_levels(self):
        cuts = [-0.2, 0.0, 0.2, 0.3]
        self.assertEqual([md.level_of(v, cuts) for v in (-0.5, -0.2, -0.1, 0.0, 0.25, 0.3, 0.9)],
                         [0, 1, 1, 2, 3, 4, 4])
        self.assertIsNone(md.level_of(None, cuts))


class Exemplars(unittest.TestCase):
    """The classical texts' own examples come out on the side the texts put them."""

    @classmethod
    def setUpClass(cls):
        cls.scores = {e["id"]: md.score_poem(e["lines"], BASELINE) for e in vm.load_exemplars()}
        cls.poles = {e["id"]: e["pole"] for e in vm.load_exemplars()}

    def unit(self, eid):
        r = self.scores[eid]
        return r if r["n_lines"] > 1 else r["lines"][0]

    def test_every_soft_exemplar_is_above_every_harsh_one(self):
        soft = [self.unit(e)["madhurya"] for e, p in self.poles.items() if p == "soft"]
        harsh = [self.unit(e)["madhurya"] for e, p in self.poles.items() if p == "harsh"]
        self.assertEqual((len(soft), len(harsh)), (4, 6))
        self.assertGreater(min(soft), max(harsh))

    def test_the_examples_reach_the_poles(self):
        self.assertEqual(self.scores["kas_4_62_saukumarya"]["label"], "soft")
        self.assertEqual(self.unit("kas_4_21_parusha")["label"], "harsh")
        self.assertEqual(self.unit("kd_1_72_krcchrodya")["label"], "harsh")
        self.assertEqual(self.scores["kp_8_75_ojas"]["label"], "harsh")

    def test_the_sequence_separates_what_the_inventory_ties(self):
        # Daṇḍin's tender example and the commentator's dense one have the same inventory
        tender, dense = self.scores["kd_1_70_sukumara"], self.scores["kasc_tikkana_gadha"]
        self.assertEqual(tender["inventory"], dense["inventory"])
        self.assertLess(tender["pileup"], dense["pileup"])
        self.assertGreater(tender["madhurya"], dense["madhurya"])

    def test_the_slack_example_has_no_harsh_run(self):
        slack = self.unit("kd_1_43_sithila")
        self.assertEqual(slack["pileup"], 0.0)
        self.assertEqual(slack["label"], "soft")


class Output(unittest.TestCase):
    def test_deterministic(self):
        lines = ["మందార మకరందమాధుర్యమునఁ దేలు-", "మధుపంబు వోవునేమదనములకు?"]
        self.assertEqual(json.dumps(md.score_poem(lines, BASELINE)), json.dumps(md.score_poem(lines, BASELINE)))

    def test_index_is_inventory_minus_pileup(self):
        result = md.score_poem(["దుర్వారోద్యమ బాహువిక్రమ రసాస్తోక ప్రతాపస్ఫుర"], BASELINE)
        self.assertAlmostEqual(result["madhurya"], result["inventory"] - result["pileup"], places=3)
        self.assertEqual(result["harshest_run"], {"aksharas": "సాస్తోకప్రతాపస్ఫు", "length": 7, "load": 4.0})

    def test_baseline_is_consistent(self):
        self.assertAlmostEqual(sum(BASELINE["class_shares"].values()), 1.0, places=3)
        self.assertAlmostEqual(BASELINE["mean_index"], BASELINE["mean_inventory"] - BASELINE["mean_pileup"], places=4)
        for unit in ("line", "poem"):
            self.assertEqual(BASELINE["cuts"][unit], sorted(BASELINE["cuts"][unit]))
            self.assertEqual(len(BASELINE["reference"][f"{unit}_index"]), 101)

    def test_cli(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            md.main(["score", "--text", "నందం బనంగ నందలి\\nభ్రష్టు భ్రష్టగు గాక శిష్టుండు గాడు"])
        result = json.loads(out.getvalue())
        self.assertEqual(result["n_lines"], 2)
        self.assertEqual([l["label"] for l in result["lines"]], ["soft", "harsh"])
        self.assertEqual(result["lines"][1]["harsh"][0], {"akshara": "భ్ర", "rules": ["P2"]})
        self.assertEqual(result["lines"][1]["harsh_runs"][0]["aksharas"], "భ్రష్టుభ్రష్ట")


if __name__ == "__main__":
    unittest.main()

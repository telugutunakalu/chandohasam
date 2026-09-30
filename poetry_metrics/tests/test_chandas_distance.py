"""Tests of the chandas distance (metric 8).

    cd poetry_metrics && python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import chandas_distance as cd                       # noqa: E402
import validation_chandas_distance as vc            # noqa: E402

BASELINE = cd.load_baseline()
UTPALAMALA = "UIIUIUIIIUIIUIIUIUIU"
KANDAMU = ["శ్రీరాముని దయచేతను", "నారూఢిగ సకల జనులు నౌరా యనగా",
           "ధారాళమైన నీతులు", "నోరూరగ జవులు పుట్ట నుడివెద సుమతీ"]


def line(pattern: str) -> cd.Scanned:
    return cd.Scanned("", (), tuple(pattern), pattern)


def poem(*patterns: str) -> tuple:
    return tuple(line(p) for p in patterns)


class OneLine(unittest.TestCase):
    def test_a_line_of_the_meter_is_at_zero(self):
        d = cd.slot("utpalamala", "all").distance(tuple(UTPALAMALA))
        self.assertEqual((d.distance, d.target, d.edits), (0, UTPALAMALA, ()))

    def test_each_kind_of_edit_costs_one(self):
        slot = cd.slot("utpalamala", "all")
        wrong_weight = "I" + UTPALAMALA[1:]
        self.assertEqual([e.op for e in slot.distance(tuple(wrong_weight)).edits], ["substitute"])
        self.assertEqual([e.op for e in slot.distance(tuple(UTPALAMALA[:5] + UTPALAMALA[6:])).edits], ["insert"])
        self.assertEqual([e.op for e in slot.distance(tuple(UTPALAMALA[:5] + "U" + UTPALAMALA[5:])).edits], ["delete"])

    def test_the_edit_names_the_akshara_and_the_weight_needed(self):
        aksharas = tuple(f"a{k}" for k in range(20))
        d = cd.slot("utpalamala", "all").distance(tuple("UIIUIUIIIUIIUIIUIUUU"), aksharas)
        self.assertEqual([e.to_dict() for e in d.edits],
                         [{"op": "substitute", "position": 19, "akshara": "a18", "needs": "I"}])

    def test_an_empty_line_costs_the_shortest_line_of_the_slot(self):
        self.assertEqual(cd.slot("utpalamala", "all").distance(()).distance, 20)
        self.assertEqual(cd.slot("kandamu", "odd").shortest, 6)

    def test_a_final_laghu_is_read_as_guru(self):
        d = cd.slot("utpalamala", "all").distance(tuple(UTPALAMALA[:-1] + "I"))
        self.assertEqual((d.distance, d.padanta), (0, True))
        self.assertEqual(cd.slot("utpalamala", "all").distance(tuple(UTPALAMALA[:-1] + "I"), padanta=False).distance, 1)

    def test_an_open_reading_is_free(self):
        options = ("UI",) + tuple(UTPALAMALA[1:])
        self.assertEqual(cd.slot("utpalamala", "all").distance(options).distance, 0)
        self.assertEqual(cd.slot("champakamala", "all").distance(("IU",) + options).distance, 0)

    def test_the_nearest_line_of_a_meter_with_many_lines(self):
        # kandamu's odd pāda is three four-mātrā gaṇas: seven gurus are one akshara too many
        d = cd.slot("kandamu", "odd").distance(tuple("UUUUUUU"))
        self.assertEqual(d.distance, 1)
        self.assertEqual(len(d.target), 6)


class WholePoem(unittest.TestCase):
    def test_a_real_kandamu(self):
        row = cd.score_poem(KANDAMU, BASELINE, "kandamu")
        self.assertEqual((row["distance"], row["label"], row["skill"]), (0, "exact", 1.0))
        self.assertEqual((row["weight_edits"], row["yati_edits"], row["prasa_edits"]), (0, 0, 0))
        self.assertTrue(vc.engine_accepts(KANDAMU, "kandamu"))

    def test_utpalamala_is_two_edits_a_line_from_champakamala(self):
        pd = cd.poem_distance(poem(*[UTPALAMALA] * 4), "champakamala")
        self.assertEqual(pd.distance, 8)            # U -> I I at the head of each pāda
        self.assertEqual(pd.operations(), {"substitute": 4, "insert": 4, "delete": 0})

    def test_a_missing_line_costs_its_aksharas(self):
        pd = cd.poem_distance(poem(*[UTPALAMALA] * 3), "utpalamala")
        self.assertEqual((pd.distance, pd.n_padas, pd.target_aksharas), (20, 4, 80))

    def test_an_extra_line_costs_its_aksharas(self):
        pd = cd.poem_distance(poem(UTPALAMALA, "UUU", UTPALAMALA, UTPALAMALA, UTPALAMALA), "utpalamala")
        self.assertEqual(pd.distance, 3)
        self.assertEqual([p.meter for p in pd.padas], ["utpalamala", None, "utpalamala", "utpalamala", "utpalamala"])

    def test_a_pada_printed_as_two_half_lines(self):
        manini = "UII" * 7 + "U"
        self.assertEqual(cd.poem_distance(poem(*[manini[:11], manini[11:]] * 4), "manini").distance, 0)

    def test_a_repeatable_meter_takes_any_number_of_units(self):
        dvipada = "UIIUIIUIIUI"                     # three ఇంద్ర gaṇas (భ భ భ) and a సూర్య gaṇa (గల)
        self.assertEqual(cd.poem_distance(poem(*[dvipada] * 6), "dvipada").distance, 0)

    def test_the_rate_is_on_the_longer_of_poem_and_target(self):
        pd = cd.poem_distance(poem(*[UTPALAMALA] * 3), "utpalamala")
        self.assertAlmostEqual(pd.rate, 20 / 80)


class ClosingLaghu(unittest.TestCase):
    """A laghu that closes a pāda is guru only when the next pāda opens with a conjunct."""
    BROKEN = ["ఛందము యతియుం దప్పిన", "ఛందోయతి భంగములగు సంగతి నితఁడు",
              "కుందేందువిశద యశుఁడై", "ముందుగఁ బూజించినాఁడు నరహరి ననఁగన్."]

    def test_the_treatise_example_has_one_weight_fault_and_one_yati_fault(self):
        """The commentary: the meter breaks in the second pāda and the yati in the fourth."""
        row = cd.score_poem(self.BROKEN, BASELINE, "kandamu")
        self.assertEqual((row["weight_edits"], row["yati_edits"], row["prasa_edits"]), (1, 1, 0))
        self.assertEqual((row["distance"], row["label"]), (2, "slip"))
        self.assertEqual(row["lines"][1]["edits"], [{"op": "substitute", "position": 15, "akshara": "డు", "needs": "U"}])
        self.assertEqual([(e["op"], e["akshara"]) for e in row["lines"][3]["edits"]], [("yati", "న")])

    def test_the_engine_reads_any_closing_laghu_as_guru(self):
        self.assertEqual(cd.poem_distance(self.BROKEN, "kandamu", cd.Reading(padanta="engine")).weights, 0)
        self.assertTrue(vc.engine_accepts(self.BROKEN, "kandamu"))

    def test_a_conjunct_opening_the_next_pada_makes_the_closing_laghu_heavy(self):
        lines = cd.scan(["సకల జనుల", "ప్రభువు"])
        self.assertEqual([l.heavy_by_next for l in lines], [True, False])
        self.assertEqual([l.heavy_by_next for l in cd.scan(["సకల జనుల", "విభువు"])], [False, False])

    def test_the_fixture_examples_are_located(self):
        for row in vc.broken_meter_exemplars(BASELINE):
            self.assertGreater(row["distance"], 0, row["id"])
            self.assertTrue(row["located"], row["id"])


class YatiAndPrasa(unittest.TestCase):
    def test_a_spoiled_prasa_akshara_is_one_edit(self):
        lines = [vc.unrhymed(KANDAMU[0])] + KANDAMU[1:]
        pd = cd.poem_distance(lines, "kandamu")
        self.assertEqual((pd.weights, pd.prasa), (0, 1))
        edit = next(e for p in pd.padas for e in p.sound if e.op == "prasa")
        self.assertEqual((edit.position, edit.akshara), (2, "కా"))      # the odd pāda out is the one to change

    def test_two_spoiled_padas_of_four_are_two_edits(self):
        lines = [vc.unrhymed(KANDAMU[0], 0), vc.unrhymed(KANDAMU[1], 1)] + KANDAMU[2:]
        self.assertEqual(cd.poem_distance(lines, "kandamu").prasa, 2)

    def test_weights_only_leaves_the_sound_out(self):
        lines = [vc.unrhymed(KANDAMU[0])] + KANDAMU[1:]
        pd = cd.poem_distance(lines, "kandamu", cd.WEIGHTS_ONLY)
        self.assertEqual((pd.distance, pd.prasa, pd.yati), (0, 0, 0))

    def test_a_meter_without_prasa_has_no_prasa_edits(self):
        row = cd.score_poem(KANDAMU, BASELINE, "ataveladi")
        self.assertEqual(row["prasa_edits"], 0)

    def test_an_akshara_that_a_weight_edit_rewrites_is_free_for_the_sound(self):
        d = cd.slot("utpalamala", "all").distance(tuple("I" + UTPALAMALA[1:]))
        self.assertIsNone(d.akshara_at(1))          # rewritten: its sound can be chosen with its weight
        self.assertEqual(d.akshara_at(2), 1)
        short = cd.slot("utpalamala", "all").distance(tuple(UTPALAMALA[1:]))
        self.assertIsNone(short.akshara_at(1))      # inserted
        self.assertEqual(short.akshara_at(2), 0)

    def test_the_yati_groups_of_a_pada(self):
        from indic_meter_dawg.parser import segment
        spec = cd.default_dawg().spec("utpalamala")
        self.assertEqual(cd.yati_groups(spec, segment("utpalamala", "all", UTPALAMALA)[0]), [(1, 10)])
        sragdhara = cd.default_dawg().spec("sragdhara")
        line = "UUUUIUUIIIIIIUUIUUIUU"
        self.assertEqual(cd.yati_groups(sragdhara, segment("sragdhara", "all", line)[0]), [(1, 8, 15)])


class Rubric(unittest.TestCase):
    def test_levels(self):
        self.assertEqual(cd.level_of(0, 4, 0.0, 20.0), 4)
        self.assertEqual(cd.level_of(3, 4, 4.0, 20.0), 3)       # at most one edit a pāda
        self.assertEqual(cd.level_of(6, 4, 8.0, 20.0), 2)       # below half the chance cut
        self.assertEqual(cd.level_of(10, 4, 12.0, 20.0), 1)
        self.assertEqual(cd.level_of(16, 4, 20.0, 20.0), 0)
        self.assertEqual(cd.level_of(1, 4, 2.1, 2.0), 0)        # a meter that prose is already near

    def test_the_chance_rate_is_tailored_to_the_meter(self):
        meters = BASELINE["meters"]
        for kind in ("all", "weights"):
            self.assertGreater(meters["utpalamala"][kind]["rate_mean"], 1.3 * meters["kandamu"][kind]["rate_mean"])
        self.assertEqual(len(meters), 37)

    def test_unmetered_text_scores_near_zero_skill(self):
        prose = ["అని పలికిన రాజు మునితో ఇట్లనెను మహాత్మా నీవు చెప్పిన", "విధమున నేను నడచుకొందును నాకు ధర్మము తెలుపుము అని",
                 "అడుగగా ఆ ముని రాజుతో ఇట్లు చెప్పసాగెను వినుము రాజా", "లోకమున ధర్మమే గొప్పది దానిని విడువరాదు ఎప్పుడును"]
        row = cd.score_poem(prose, BASELINE, "utpalamala")
        self.assertEqual(row["label"], "unmetered")
        self.assertLess(row["skill"], 0.3)


class Nearest(unittest.TestCase):
    def test_the_nearest_meter_of_a_poem_in_meter(self):
        self.assertEqual(cd.score_poem(KANDAMU, BASELINE)["meter"], "kandamu")

    def test_nearest_is_by_skill_not_by_raw_edits(self):
        broken = poem(*[UTPALAMALA] * 3, UTPALAMALA[:9] + "UU" + UTPALAMALA[11:])
        self.assertEqual(cd.nearest(broken, BASELINE).meter, "utpalamala")


class Validation(unittest.TestCase):
    def test_k_edits_never_cost_more_than_k(self):
        import random
        rng = random.Random(7)
        lines = cd.scan(KANDAMU)
        for k in (1, 2, 3, 5, 8):
            for _ in range(20):
                self.assertLessEqual(cd.poem_distance(vc.edited(lines, k, rng), "kandamu").distance, k)

    def test_chance_lines_have_the_lengths_of_the_meter(self):
        self.assertEqual(vc.chance_lengths("utpalamala"), [20, 20, 20, 20])
        self.assertEqual(len(vc.chance_lengths("dvipada")), 4)


if __name__ == "__main__":
    unittest.main()

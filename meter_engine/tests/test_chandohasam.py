# -*- coding: utf-8 -*-
"""
End-to-end tests of the chandohasam tool: poem -> metre, గణవిభజన, ప్రాస, యతి.

    python3 -m unittest tests.test_chandohasam -v
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from chandohasam import analyze, PadyaAnalysis          # noqa: E402
from chandohasam.cli import main as cli_main             # noqa: E402

CLASSICS = yaml.safe_load((HERE / "fixtures" / "classics.yaml").read_text(encoding="utf-8"))["stanzas"]

KANDAM = """పలికెడిది భాగవత మఁట,
పలికించెడివాడు రామభద్రుం డఁట, నేఁ
బలికిన భవహర మగునఁట,
పలికెద, వేఱొండు గాథ బలుకఁగ నేలా?"""            # Pōtana 1-18

SEESAM_GITA = """విష్ణుండు విశ్వంబు, విష్ణునికంటెను-
వేఱేమియును లేదు విశ్వమునకు
భవవృద్ధిలయము లా పరమేశుచే నగు-
నీ వెఱుంగుదు కాదె నీ ముఖమున
నెఱిఁగింప బడ్డది యేక దేశమున నీ-
భువన భద్రమునకై పుట్టినట్టి
హరికళాజాతుండ వని విచారింపుము,-
రమణతో హరిపరాక్రమము లెల్ల
నేను విడిచి పోక యింట నుండితినయ్య,
మోహిఁగాక, యెఱుక మోసపోక,
మాఱు చింత లేక, మౌనినై యేనేండ్ల
వాఁడ నగుచుఁ గొన్ని వాసరములు."""                # Pōtana 1-102


def text_of(st: dict) -> str:
    return st.get("text") or "\n".join(st["lines"])


class TestStructure(unittest.TestCase):
    def test_utpalamala_full_report(self):
        st = next(s for s in CLASSICS if s["meter"] == "utpalamala")
        a = analyze(text_of(st), profile="relaxed")
        self.assertIsInstance(a, PadyaAnalysis)
        self.assertTrue(a.identified); self.assertEqual(a.meter, "utpalamala"); self.assertEqual(a.name_te, "ఉత్పలమాల")
        self.assertEqual(len(a.units), 1)
        u = a.units[0]
        self.assertEqual(len(u.lines), 4)
        for line in u.lines:
            self.assertEqual(line.gana_names, ["భ", "ర", "న", "భ", "భ", "ర", "వ"])
            self.assertEqual(line.pattern, "UIIUIUIIIUIIUIIUIUIU")
            self.assertEqual(sum(len(g.aksharas) for g in line.ganas), 20)
            self.assertEqual("".join(g.pattern for g in line.ganas), line.pattern)
            self.assertEqual([s.positions for s in line.yati], [[1, 10]])
            self.assertTrue(line.yati[0].matched)
        # ప్రాస: the second akshara of every pāda, వ్వ
        self.assertTrue(u.prasa.applicable and u.prasa.matched)
        self.assertEqual([s.prasa for s in u.prasa.seats], ["వ్వ"] * 4)
        self.assertEqual(u.prasa.consonant, "వ్వ")
        self.assertTrue(a.matched)

    def test_kandam_prasa_and_yati(self):
        a = analyze(KANDAM)
        self.assertEqual(a.meter, "kandamu")
        u = a.units[0]
        self.assertEqual([len(l.yati) for l in u.lines], [0, 1, 0, 1])       # pādas 1, 3 carry no yati
        self.assertTrue(u.prasa.applicable and u.prasa.matched)
        self.assertEqual(u.prasa.consonant, "ల")
        self.assertEqual([s.prasa for s in u.prasa.seats], ["లి", "లి", "లి", "లి"])
        self.assertTrue(a.matched)

    def test_seesam_with_gita_trailer(self):
        a = analyze(SEESAM_GITA, profile="relaxed")
        self.assertEqual(a.meter, "seesamu+ataveladi")
        self.assertEqual([u.meter for u in a.units], ["seesamu", "ataveladi"])
        seesam, gita = a.units
        self.assertEqual(len(seesam.lines), 4); self.assertEqual(len(gita.lines), 4)
        self.assertEqual([len(l.yati) for l in seesam.lines], [2, 2, 2, 2])   # {1,g3} and {g5,g7}
        self.assertEqual(seesam.lines[0].yati[0].positions[0], 1)
        self.assertGreater(seesam.lines[0].yati[1].positions[0], 1)
        self.assertFalse(seesam.prasa.applicable)                             # సీసము has no prāsa
        self.assertTrue(a.yati_matched, a.render())
        self.assertTrue(a.matched)

    def test_ataveladi_prasa_yati_fallback(self):
        st = next(s for s in CLASSICS if s["meter"] == "ataveladi")
        a = analyze(text_of(st), profile="relaxed")
        seats = [s for l in a.units[0].lines for s in l.yati]
        self.assertTrue(any(s.prasa_yati for s in seats))
        self.assertTrue(a.matched)

    def test_all_classics_match(self):
        for st in CLASSICS:
            a = analyze(text_of(st), profile="relaxed")
            self.assertEqual(a.meter, st["meter"], st["id"])
            self.assertTrue(a.matched, f"{st['id']}\n{a.render()}")

    def test_unidentified_and_failure(self):
        a = analyze("క\nక\nక")
        self.assertFalse(a.identified); self.assertFalse(a.matched); self.assertEqual(a.units, [])
        self.assertIn("NOT IDENTIFIED", a.render())
        # a real utpalamala with one yati broken: swap the 10th akshara's line
        st = next(s for s in CLASSICS if s["meter"] == "utpalamala")
        lines = text_of(st).split("\n")
        broken = lines[0].replace("మెవ్వని", "కెవ్వని")
        a = analyze("\n".join([broken] + lines[1:]), yati_sandhi="off")
        self.assertTrue(a.identified)
        self.assertFalse(a.units[0].lines[0].yati[0].matched)
        self.assertFalse(a.yati_matched); self.assertFalse(a.matched)

    def test_profiles_and_sandhi_modes_are_passed_through(self):
        st = next(s for s in CLASSICS if s["meter"] == "utpalamala")
        strict_off = analyze(text_of(st), profile="strict", yati_sandhi="off")
        self.assertFalse(strict_off.yati_matched)             # the two-sided sandhi pāda needs hypotheses
        acchu = analyze(text_of(st), profile="relaxed", yati_sandhi="acchu")
        self.assertTrue(acchu.yati_matched)
        self.assertEqual(acchu.profile, "relaxed"); self.assertEqual(acchu.yati_sandhi, "acchu")


class TestSerialisation(unittest.TestCase):
    def test_json_round_trip(self):
        a = analyze(KANDAM)
        d = json.loads(a.to_json())
        self.assertEqual(d["meter"], "kandamu"); self.assertTrue(d["matched"])
        line = d["units"][0]["lines"][1]
        self.assertEqual(line["line_no"], 2)
        self.assertIn("ganas", line); self.assertIn("aksharas", line["ganas"][0])
        self.assertEqual(line["ganas"][0]["aksharas"][0]["weight"] in ("U", "I"), True)
        self.assertIn("seats", d["units"][0]["prasa"])
        self.assertTrue(line["yati"][0]["matched"])
        self.assertEqual(d["units"][0]["lines"][0]["yati"], [])

    def test_render_mentions_everything(self):
        a = analyze(KANDAM)
        text = a.render()
        for needle in ("కందము", "గణాలు", "యతి", "ప్రాస", "pāda 4"):
            self.assertIn(needle, text)


class TestCli(unittest.TestCase):
    def run_cli(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cli_main(list(args))
        return code, buf.getvalue()

    def test_padas_and_json(self):
        code, out = self.run_cli(*KANDAM.split("\n"), "--json")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["meter"], "kandamu")
        code, out = self.run_cli(*KANDAM.split("\n"))
        self.assertEqual(code, 0); self.assertIn("ప్రాస", out)

    def test_file_input(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
            fh.write(SEESAM_GITA)
        code, out = self.run_cli("--file", fh.name, "--profile", "relaxed")
        self.assertEqual(code, 0); self.assertIn("seesamu+ataveladi", out)


if __name__ == "__main__":
    unittest.main()

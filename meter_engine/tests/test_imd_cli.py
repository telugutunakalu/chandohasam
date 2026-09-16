# -*- coding: utf-8 -*-
"""cli.py — every subcommand runs and returns the documented exit code."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from imd_support import dawg
from indic_meter_dawg import cli

UTP = "UIIUIUIIIUIIUIIUIUIU"


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = cli.main(argv)
    return code, out.getvalue(), err.getvalue()


class TestCli(unittest.TestCase):
    def test_identify_text(self):
        code, out, _ = run(["identify", UTP, UTP, UTP, UTP])
        self.assertEqual(code, 0)
        self.assertIn("utpalamala", out)

    def test_identify_json(self):
        code, out, _ = run(["identify", "--json", UTP, UTP, UTP, UTP])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["best"], "utpalamala")

    def test_identify_unknown_exit_code(self):
        code, out, _ = run(["identify", "UIUI", "UIUI"])
        self.assertEqual(code, 1)
        self.assertIn("No meter matches", out)

    def test_identify_from_file_and_flags(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "poem.txt"
            p.write_text("\n".join(["UUUUUUUI"] * 4) + "\n", encoding="utf-8")
            code, out, _ = run(["identify", "--file", str(p)])
            self.assertEqual(code, 0)
            self.assertIn("vidyunmala", out)
            code, out, _ = run(["identify", "--file", str(p), "--no-padanta"])
            self.assertEqual(code, 1)

    def test_identify_no_lines(self):
        code, _, err = run(["identify"])
        self.assertEqual(code, 2)
        self.assertIn("no lines", err)

    def test_walk(self):
        code, out, _ = run(["walk", UTP])
        self.assertEqual(code, 0)
        self.assertIn("utpalamala/all", out)
        code, out, _ = run(["walk", "--json", UTP[:-1] + "I"])
        d = json.loads(out)
        self.assertEqual(d["padanta_accepted"], [["utpalamala", "all"]])

    def test_prefix(self):
        code, out, _ = run(["prefix", "UUUUUUU"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "madhuragati_ragada/all, vidyunmala/all")
        code, out, _ = run(["prefix", "I" * 37])
        self.assertIn("no meter", out)

    def test_grammar_levels(self):
        code, out, _ = run(["grammar", "kandamu"])
        self.assertEqual(code, 0)
        self.assertIn("Poem → Poem⟨U⟩ | Poem⟨I⟩", out)
        self.assertIn("Kanda=జ|నల → జ | నల", out)
        code, out, _ = run(["grammar", "kandamu", "--level", "line", "--slot", "even"])
        self.assertIn("G3 → IUI G4 | IIII G4", out)
        code, out, _ = run(["grammar", "vidyunmala", "--strict"])
        self.assertIn("G1_UUU_1", out)
        self.assertIn("symbol 1/3", out)
        code, out, _ = run(["grammar", "ataveladi", "--level", "line"])
        self.assertIn("# ataveladi / odd", out)
        self.assertIn("# ataveladi / even", out)
        code, out, _ = run(["grammar", "tetagiti", "--level", "flat"])
        self.assertIn("L4.G5 → III | UI", out)
        self.assertIn("L1.G5 → III⏎ L2.G1 | UI⏎ L2.G1", out)

    def test_stats(self):
        code, out, _ = run(["stats", "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["dfa_states"], dawg().dfa.n_states)
        code, out, _ = run(["stats"])
        self.assertIn("distinct_lines", out)

    def test_enumerate(self):
        code, out, _ = run(["enumerate", "vidyunmala", "all"])
        self.assertEqual(out.split(), ["UUUUUUUU"])
        code, out, _ = run(["enumerate", "tetagiti", "all", "--limit", "5"])
        self.assertEqual(len(out.split()), 5)

    def test_writers(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = run(["grammars", "--out", tmp + "/g"])
            self.assertEqual(code, 0)
            self.assertIn("37 grammar files", out)
            code, out, _ = run(["docs", "--out", tmp + "/d"])
            self.assertIn("38 doc pages", out)
            code, out, _ = run(["diagrams", "--out", tmp + "/x", "--no-svg"])
            self.assertEqual(code, 0)
            self.assertTrue((Path(tmp) / "x" / "README.md").is_file())

    def test_help_parses(self):
        with self.assertRaises(SystemExit) as cm:
            run(["--help"])
        self.assertEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main()

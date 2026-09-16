# -*- coding: utf-8 -*-
"""
Deterministic verification of meter_engine/yati_rules.yaml and yati_engine.py.

    python3 -m unittest discover -s meter_engine/tests -p "test_yati*" -v

  1. ruleset integrity  — ids, statuses, cross-references to yathi_docs/yathi_compact.md
  2. the lookup table   — symmetry, vargaja generation, bindu table, named failures
  3. akshara parsing    — prefixes (ం, C్+), Syllable objects, marks
  4. readings           — saṁyukta constituents, ఋ detachment, hypotheses, blockers, ubhaya triggers
  5. fixtures           — every attested_examples entry gives the documented verdict
  6. pair verdicts      — ranking, profiles, hypothesis policy, provenance trail
  7. line / stanza      — groups, bahu-yati niyati, prāsa-yati fallback, DAWG integration
  8. CLI                — JSON round trip
"""
from __future__ import annotations

import contextlib
import io
import json
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent.parent))

import yati_engine as ye  # noqa: E402

RS = ye.load_ruleset()
COMPACT = HERE.parent / "yathi_docs" / "yathi_compact.md"
VALID_STATUSES = {"canonical", "canonical_subtype", "mandatory", "accepted_relaxation",
                  "orthographic_relaxation", "deprecated", "forbidden", "informational"}
ID_RE = re.compile(r"^YATI-[A-Z]{2,3}-\d{2}(\.\d{1,2})?$")


def compact_rules() -> dict[str, dict]:
    out = {}
    for line in COMPACT.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- id="):
            continue
        d = dict(f.split("=", 1) for f in line[2:].split(" | "))
        out[d["id"]] = d
    return out


# =============================================================================
# 1. ruleset integrity
# =============================================================================
class TestRulesetIntegrity(unittest.TestCase):
    def test_sections(self):
        for k in ("profiles", "profile_order", "alphabet", "maitri_table", "bindu_table", "vowel_bridges",
                  "sandhi_readings", "ubhaya_triggers", "rules", "attested_examples"):
            self.assertIn(k, RS.data)

    def test_rule_ids_and_statuses(self):
        for rid, r in RS.rules.items():
            self.assertRegex(rid, ID_RE)
            self.assertIn(r["status"], VALID_STATUSES, rid)
            self.assertIn("te", r["names"]); self.assertIn("en", r["names"])

    def test_ids_exist_in_compact_with_same_status(self):
        comp = compact_rules()
        self.assertGreater(len(comp), 250)
        for rid, r in RS.rules.items():
            if r.get("compact") is False:
                continue
            self.assertIn(rid, comp, f"{rid} missing from yathi_compact.md")
            self.assertEqual(comp[rid]["status"], r["status"], rid)

    def test_every_referenced_rule_is_catalogued(self):
        refs = set(RS.pairs.values()) | {RS.identity_rule, RS.default_rule, RS.vargaja_rule, RS.stop_nasal_rule}
        refs |= {b["rule"] for b in RS.bindu_table} | {c["rule"] for c in RS.conditional}
        refs |= {c["rule"] for c in RS.cluster_units} | {b["rule"] for b in RS.vowel_bridges}
        refs |= {v for d in RS.detachable.values() for v in d.values()}
        refs |= {r[1] for lst in RS.sandhi_readings.values() for r in lst}
        for key in ("suffix", "prefix", "lexicon", "suffix_ubhaya"):
            refs |= {t["rule"] for t in RS.ubhaya.get(key, [])}
        refs.add(RS.ubhaya["ordinal"]["rule"]); refs.add("YATI-UB-17")
        refs |= {b["rule"] for b in RS.blockers}
        missing = sorted(refs - set(RS.rules))
        self.assertEqual(missing, [], f"referenced but not catalogued: {missing}")

    def test_profiles_are_nested(self):
        o = RS.profile_order
        for a, b in zip(o, o[1:]):
            self.assertTrue(RS.profiles[a] <= RS.profiles[b])
        self.assertNotIn("forbidden", RS.profiles["historical"])

    def test_vowel_classes_partition(self):
        seen = {}
        for cls, vs in RS.data["alphabet"]["vowel_classes"].items():
            for v in vs:
                self.assertNotIn(v, seen); seen[v] = cls
        self.assertEqual(len(seen), 16)


# =============================================================================
# 2. the lookup table
# =============================================================================
class TestLookupTable(unittest.TestCase):
    def test_symmetric(self):
        for x in RS.consonants:
            for y in RS.consonants:
                self.assertEqual(ye.lookup_pair(x, y)["rule"], ye.lookup_pair(y, x)["rule"], (x, y))

    def test_matrix_size_and_identity(self):
        rows = ye.maitri_matrix()
        self.assertEqual(len(rows), 35 * 36 // 2)
        for r in rows:
            if r["a"] == r["b"]:
                self.assertIn(r["rule"], ("YATI-VY-01", "YATI-SP-07"))

    def test_vargaja_is_generated(self):
        self.assertEqual(ye.lookup_pair("క", "ఘ")["rule"], "YATI-VY-02.1")
        self.assertEqual(ye.lookup_pair("ప", "భ")["rule"], "YATI-VY-02.1")
        self.assertEqual(ye.lookup_pair("చ", "ఝ")["rule"], "YATI-VY-02.1")
        n = sum(1 for r in ye.maitri_matrix() if r["rule"] == "YATI-VY-02.1")
        self.assertEqual(n, 30)          # 6 per varga × 5 (ౘ/ౙ fold into చ/జ)

    def test_stop_nasal_needs_bindu(self):
        self.assertEqual(ye.lookup_pair("త", "న")["rule"], "YATI-RJ-05")
        self.assertEqual(ye.lookup_pair("త", "న", bindu_a=True)["rule"], "YATI-VY-03")
        self.assertEqual(ye.lookup_pair("న", "త", bindu_b=True)["rule"], "YATI-VY-03")
        self.assertEqual(ye.lookup_pair("ట", "న", bindu_a=True)["rule"], "YATI-VY-05")
        self.assertEqual(ye.lookup_pair("ద", "ట", bindu_a=True, bindu_b=True)["rule"], "YATI-VY-06")
        self.assertEqual(ye.lookup_pair("ద", "ట", bindu_a=True)["rule"], "YATI-RJ-00")
        self.assertEqual(ye.lookup_pair("య", "మ", bindu_a=True)["rule"], "YATI-SP-03")

    def test_named_failures_and_relaxations(self):
        self.assertEqual(ye.lookup_pair("మ", "వ")["rule"], "YATI-RJ-07")
        self.assertEqual(ye.lookup_pair("మ", "వ", vowel_class="U")["rule"], "YATI-DL-06")
        self.assertEqual(ye.lookup_pair("ప", "మ", vowel_class="U")["rule"], "YATI-VY-16")
        self.assertEqual(ye.lookup_pair("ర", "ఱ")["status"], "orthographic_relaxation")
        self.assertEqual(ye.lookup_pair("ద", "డ")["min_profile"], "relaxed")
        self.assertEqual(ye.lookup_pair("ల", "ఢ")["rule"], "YATI-RJ-13")
        self.assertFalse(ye.lookup_pair("క", "చ")["positive"])
        self.assertEqual(ye.lookup_pair("ౘ", "జ")["rule"], "YATI-VY-02.1")


# =============================================================================
# 3. parsing
# =============================================================================
class TestParsing(unittest.TestCase):
    def test_prefixes(self):
        a = ye.parse_akshara("ంతా")
        self.assertTrue(a.pre_bindu); self.assertEqual(a.onset, ("త",)); self.assertEqual(a.vowel, "ఆ")
        b = ye.parse_akshara("న్+సా")
        self.assertEqual(b.pre_dead, ("న",)); self.assertEqual(b.onset, ("న", "స")); self.assertEqual(b.own_onset, ("స",))
        c = ye.parse_akshara("క్ష్మా")
        self.assertEqual(c.onset, ("క", "ష", "మ"))
        d = ye.parse_akshara("ఋ")
        self.assertTrue(d.bare_vowel); self.assertEqual(d.vowel, "ఋ")
        e = ye.parse_akshara("మున్")
        self.assertEqual(e.dead, ("న",)); self.assertEqual(e.vowel, "ఉ")
        f = ye.parse_akshara("ౙా")
        self.assertEqual(f.onset, ("జ",)); self.assertEqual(f.onset_raw, ("ౙ",))

    def test_syllable_object(self):
        from indic_meter_dawg import scansion as sc
        syl = sc.scan_line("శ్రీరాముఁడు").syllables[0]
        a = ye.parse_akshara(syl)
        self.assertEqual(a.onset, ("శ", "ర")); self.assertEqual(a.vowel, "ఈ")

    def test_ardhabindu_and_marks_ignored(self):
        self.assertTrue(ye.check("ఁక", "గ").matched)
        self.assertTrue(ye.check("కం", "గ").matched)
        self.assertTrue(ye.check("క", "గః").matched)


# =============================================================================
# 4. readings
# =============================================================================
class TestReadings(unittest.TestCase):
    def shows(self, text, **kw):
        return [r.show() for r in ye.readings_for(ye.parse_akshara(text), RS, **kw)]

    def test_constituents(self):
        r = ye.readings_for(ye.parse_akshara("శ్రీ"), RS, sandhi="off")
        hal = [(x.consonant, x.rank, x.via) for x in r if x.track == "hal"]
        self.assertIn(("శ", 0, ("YATI-SY-01",)), hal); self.assertIn(("ర", 1, ("YATI-SY-01",)), hal)

    def test_detachment_only_for_ru_lu(self):
        self.assertTrue(any(x.detached == "bound" for x in ye.readings_for(ye.parse_akshara("కృ"), RS, sandhi="off")))
        self.assertFalse(any(x.detached for x in ye.readings_for(ye.parse_akshara("కి"), RS, sandhi="off")))

    def test_hypotheses_off_and_on(self):
        self.assertFalse(any(x.hypothesis for x in ye.readings_for(ye.parse_akshara("దా"), RS, sandhi="off")))
        hyp = [x for x in ye.readings_for(ye.parse_akshara("దా"), RS) if x.hypothesis]
        self.assertEqual({x.vowel for x in hyp}, {"అ", "ఆ"})
        hidden = [x for x in ye.readings_for(ye.parse_akshara("సో"), RS) if x.hypothesis and x.vowel == "అ"]
        self.assertEqual(hidden[0].via, ("YATI-SV-04",)); self.assertEqual(hidden[0].rank, 5)

    def test_cluster_units(self):
        r = ye.readings_for(ye.parse_akshara("జ్ఞా"), RS, sandhi="off")
        self.assertEqual({x.consonant for x in r if x.unit_rule == "YATI-SP-01"}, {"న", "ణ"})
        self.assertEqual({x.consonant for x in r if x.unit_rule == "YATI-SP-02"}, {"క", "ఖ", "గ", "ఘ"})

    def test_ubhaya_trigger_and_blocker(self):
        r = ye.readings_for(ye.parse_akshara("ప్రా"), RS, sandhi="off", word="ప్రాప్తి", index=0)
        self.assertTrue(any(x.via == ("YATI-UB-10",) and x.vowel == "ఆ" for x in r))
        r = ye.readings_for(ye.parse_akshara("కె"), RS, word="పలికెడు", index=2)
        self.assertFalse(any(x.track == "svara" for x in r))      # verbal -ఎడు: consonant only
        r = ye.readings_for(ye.parse_akshara("ట్ట"), RS, sandhi="off", word="కట్టలుక", index=1)
        self.assertFalse(any(x.track == "hal" for x in r))        # ద్విరుక్త ట: vowel only


# =============================================================================
# 5. fixtures
# =============================================================================
class TestFixtures(unittest.TestCase):
    def test_all_fixtures_pass(self):
        rep = ye.run_attested_examples(RS)
        bad = [(r["id"], r["problems"]) for r in rep if not r["ok"]]
        self.assertEqual(bad, [])
        self.assertGreaterEqual(len(rep), 100)


# =============================================================================
# 6. pair verdicts
# =============================================================================
class TestPairVerdicts(unittest.TestCase):
    def test_ranking_prefers_written_reading(self):
        r = ye.check("శ్రీ", "శి")
        self.assertEqual(r.rule, "YATI-VY-01"); self.assertEqual(r.best.reading_a.consonant, "శ")
        r = ye.check("శ్రీ", "రి")
        self.assertEqual(r.rule, "YATI-SP-07"); self.assertIn("YATI-SY-01", r.best.vidhana)

    def test_profiles(self):
        r = ye.check("ర", "ఱ", "strict", sandhi="off")
        self.assertFalse(r.matched); self.assertEqual(r.min_profile, "relaxed")
        self.assertTrue(ye.check("ర", "ఱ", "relaxed", sandhi="off").matched)
        self.assertTrue(ye.check("ర", "ఱ", "historical", sandhi="off").matched)
        with self.assertRaises(ValueError):
            ye.check("క", "గ", "loose")

    def test_hypothesis_never_on_both_sides(self):
        r = ye.check("ర", "ఱ", "strict")           # both would need a sandhi hypothesis
        self.assertFalse(r.matched)
        r = ye.check("అ", "దా", "strict")
        self.assertTrue(r.matched); self.assertTrue(r.best.hypothesis)
        r = ye.check("దా", "అ", "strict")
        self.assertTrue(r.matched); self.assertTrue(r.best.hypothesis)

    def test_acchu_mode_is_additive_and_flagged(self):
        r = ye.check("బె", "డె", "relaxed", sandhi="acchu")
        self.assertTrue(r.matched); self.assertEqual(r.rule, "YATI-SV-02.10"); self.assertTrue(r.best.hypothesis)
        self.assertFalse(ye.check("బె", "డె", "strict", sandhi="acchu").matched)      # accepted_relaxation
        self.assertFalse(ye.check("బె", "డు", "relaxed", sandhi="acchu").matched)     # classes still differ
        self.assertEqual(ye.check("క", "గా", "relaxed", sandhi="acchu").rule, "YATI-VY-02.1")   # never overrides a real rule

    def test_evidence_pairs_with_hypothesis(self):
        r = ye.check("బె", "డె", "strict", evidence_a=[("ఎ", 1, "printed split after ఁ")])
        self.assertTrue(r.matched); self.assertEqual(r.rule, "YATI-SV-02")
        self.assertFalse(ye.check("బె", "డె", "strict").matched)

    def test_vowel_class_named(self):
        r = ye.check("క", "కి", sandhi="off")
        self.assertFalse(r.matched); self.assertEqual(r.rejected[0].rule, "YATI-RJ-04")
        self.assertIn("YATI-RJ-04", r.why)

    def test_trail_and_json(self):
        r = ye.check("ంత", "న")
        self.assertEqual(r.trail[0]["rule"], "YATI-EP-02"); self.assertEqual(r.trail[-1]["outcome"], "pass")
        d = json.loads(r.to_json())
        self.assertEqual(d["rule"], "YATI-VY-03"); self.assertTrue(d["matched"])

    def test_determinism(self):
        a = ye.check("క్ష్మా", "ంప").to_dict(); b = ye.check("క్ష్మా", "ంప").to_dict()
        self.assertEqual(a, b)


# =============================================================================
# 7. line / stanza
# =============================================================================
class TestLineAndStanza(unittest.TestCase):
    def test_line_with_strings(self):
        ly = ye.evaluate_line(["క", "మ", "లా", "క్షా"], [(1, 4)])
        self.assertTrue(ly.matched); self.assertEqual(ly.groups[0].rule, "YATI-VY-01")     # క ↔ క్షా via YATI-SY-05
        self.assertIn("YATI-SY-05", ly.groups[0].results[0].best.vidhana)
        ly = ye.evaluate_line(["కా", "మ", "ల", "కు"], [(1, 4)], sandhi="off")
        self.assertFalse(ly.matched)       # కా(A) vs కు(U)
        ly = ye.evaluate_line(["కా", "మ"], [(1, 5)])
        self.assertFalse(ly.matched); self.assertTrue(ly.groups[0].violations)

    def test_previous_syllable_bindu_and_drutam(self):
        from indic_meter_dawg import scansion as sc
        syls = list(sc.scan_line("నలినీ దళంబుల సంతస").syllables)
        # వళి న (1) vs త (9th akshara, preceded by సం) — బిందు యతి
        ly = ye.evaluate_line(syls, [(1, 9)], first_pada=True)
        self.assertTrue(ly.matched); self.assertEqual(ly.groups[0].rule, "YATI-VY-03")
        self.assertFalse(ye.evaluate_line(syls, [(1, 7)], first_pada=True, sandhi="off").matched)   # న vs ల
        syls = list(sc.scan_line("సాధువు మాన్యమౌ").syllables)
        self.assertFalse(ye.evaluate_line(syls, [(1, 5)], sandhi="off").matched)
        ly = ye.evaluate_line(syls, [(1, 5)], sandhi="off", prev_line_dead=["న"])
        self.assertTrue(ly.matched); self.assertIn("YATI-SY-08", ly.groups[0].results[0].best.vidhana)

    def test_bahuyati_niyati(self):
        # క్ష్మా opens; caesuras on కా (క), సం (ష) — switching constituents breaks the niyati
        aks = ["క్ష్మా", "ధ", "రం", "బా", "త", "ప", "త్రం", "కా", "ధ", "రిం", "చె", "వా", "ని", "గా", "సం"]
        ok = ye.evaluate_line(aks, [(1, 8, 14)])          # కా(క) and గా(క): consistent
        self.assertTrue(ok.matched)
        bad = ye.evaluate_line(aks, [(1, 8, 15)])         # కా(క) then సం(ష): switch
        self.assertFalse(bad.matched); self.assertTrue(any("YATI-SY-11" in v for v in bad.groups[0].violations))
        hist = ye.evaluate_line(aks, [(1, 8, 15)], "historical")
        self.assertTrue(hist.matched)                     # identified, not accepted, in the historical profile
        seesam = ye.evaluate_line(aks, [(1, 8, 15)], seesam_halves=True)
        self.assertTrue(seesam.matched)

    def test_augment_evidence_and_blockers(self):
        from indic_meter_dawg import scansion as sc
        # టుగాగమ: గయ్యంపు + ట్ + ఆయితము -> the ట carries the second member's ఆ; హ ↔ ఆ by సరసయతి
        syls = list(sc.scan_line("హర్ష మిగురొత్తఁ గయ్యంపుటాయితమునఁ").syllables)
        ly = ye.evaluate_line(syls, [(1, 10)], first_pada=True)
        self.assertTrue(ly.matched); self.assertEqual(ly.groups[0].rule, "YATI-VY-10")
        self.assertEqual(ye.sandhi_evidence(syls, 10), [("ఆ", 2, "టుగాగమ")])
        # ద్విరుక్త ట: కట్టాయితము -> ట్టా supplies ఆ (not a hypothesis); ప్రత్యేక blocker only for the exact words
        r = ye.readings_for(ye.parse_akshara("ట్టా"), RS, sandhi="off", word="కట్టాయితములు", index=1)
        self.assertEqual([(x.track, x.vowel) for x in r], [("svara", "ఆ")])
        r = ye.readings_for(ye.parse_akshara("నా"), RS, sandhi="off", word="పతనాది", index=2)
        self.assertTrue(any(x.track == "hal" for x in r))            # ...ఆది is not the ప్రత్యేక నాది
        r = ye.readings_for(ye.parse_akshara("ది"), RS, word="నాది", index=1)
        self.assertFalse(any(x.track == "svara" for x in r))         # the elided అది: consonant only
        r = ye.readings_for(ye.parse_akshara("రా"), RS, word="కుమారాయితము", index=2)
        self.assertFalse(any(x.track == "svara" for x in r))         # క్యచ్ lexicon
        r = ye.readings_for(ye.parse_akshara("టా"), RS, word="గయ్యంపుటాయితము", index=3)
        self.assertTrue(any(x.track == "hal" for x in r))            # not క్యచ్

    def test_prasa_yati_fallback(self):
        from indic_meter_dawg import scansion as sc
        syls = list(sc.scan_line("చూడ చూడ రుచుల జాడ వేరు").syllables)
        no = ye.evaluate_line(syls, [(1, 8)], sandhi="off")
        self.assertFalse(no.matched)
        yes = ye.evaluate_line(syls, [(1, 8)], sandhi="off", allow_prasa_yati=True)
        self.assertTrue(yes.matched); self.assertEqual(yes.groups[0].rule, "YATI-PY-01")
        self.assertEqual(yes.groups[0].prasa_yati["prasa_rule"], "PRASA-SAMA-01")

    def test_stanza_via_dawg(self):
        import yaml
        fx = yaml.safe_load((HERE / "fixtures" / "classics.yaml").read_text(encoding="utf-8"))["stanzas"]
        for st in fx:
            text = st.get("text") or "\n".join(st["lines"])
            res = ye.evaluate_stanza(text, profile="relaxed")
            self.assertEqual(res.meter, st["meter"], st["id"])
            self.assertTrue(res.matched, f"{st['id']}: {res.explain()}")
        plan = ye.prepare_stanza(fx[0].get("text") or "\n".join(fx[0]["lines"]))
        self.assertTrue(plan.identified); self.assertEqual(plan.meter, "utpalamala")
        self.assertEqual([g for gs in plan.groups for g in gs], [(1, 10)] * 4)
        self.assertTrue(ye.evaluate_plan(plan, "relaxed").matched)
        kanda = next(s for s in fx if s["meter"] == "kandamu")
        res = ye.evaluate_stanza(kanda.get("text") or "\n".join(kanda["lines"]))
        self.assertEqual([len(l.groups) for l in res.lines], [0, 1, 0, 1])     # pādas 1, 3 carry no yati


# =============================================================================
# 8. CLI
# =============================================================================
class TestCli(unittest.TestCase):
    def run_cli(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = ye._cli(list(args))
        return code, buf.getvalue()

    def test_check_json(self):
        code, out = self.run_cli("check", "క", "గా", "--json")
        self.assertEqual(code, 0); self.assertEqual(json.loads(out)["rule"], "YATI-VY-02.1")
        code, out = self.run_cli("check", "క", "చ", "--sandhi", "off")
        self.assertEqual(code, 1); self.assertIn("YATI-RJ-00", out)

    def test_other_commands(self):
        self.assertEqual(self.run_cli("lookup", "శ", "చ")[0], 0)
        code, out = self.run_cli("matrix", "--tsv")
        self.assertEqual(code, 0); self.assertEqual(len(out.strip().splitlines()), 631)
        self.assertEqual(self.run_cli("rules")[0], 0)
        self.assertEqual(self.run_cli("examples")[0], 0)
        code, out = self.run_cli("line", "పుణ్యుఁడు రామచంద్రుఁ డట పోయి ముదంబునఁ గాంచె దండకా", "--yati", "1,10")
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()

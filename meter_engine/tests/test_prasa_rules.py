# -*- coding: utf-8 -*-
"""
Deterministic verification of meter_engine/prasa_rules.yaml and prasa_engine.py.

Run with either
    python3 -m unittest discover -s meter_engine/tests -v
    python3 -m pytest meter_engine/tests            (if pytest is installed)

The suite checks, in this order:
  1. ruleset integrity   — every id / status / cross-reference in the YAML is sound
  2. the lookup table    — every consonant pair resolves to exactly one named rule,
                           symmetrically, with the profile gating the YAML declares
  3. akshara features    — aksharanusarika-based decomposition of the prāsa akshara
  4. attested examples   — every fixture embedded in the YAML gives the documented
                           verdict under strict / relaxed / historical
  5. decision procedure  — targeted scenarios for rule ordering and naming
  6. provenance trail    — shape, determinism, permutation invariance, labels
  7. CLI                 — JSON round trip, matrix, examples command
"""
from __future__ import annotations

import contextlib
import io
import itertools
import json
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import prasa_engine as pe  # noqa: E402

RS = pe.load_ruleset()
PROFILES = RS.profile_order
VALID_STATUSES = {"canonical", "canonical_subtype", "mandatory", "accepted_relaxation",
                  "orthographic_relaxation", "deprecated", "forbidden", "informational"}
BASE_CONSONANTS = [c for c in RS.consonants if c not in pe.DANTYA_MAP]
RULE_ID_RE = re.compile(r"^PRASA-[A-Z]+-[A-Z0-9-]+$")


def ex_by_id(ex_id: str) -> dict:
    for ex in RS.examples:
        if ex["id"] == ex_id:
            return ex
    raise KeyError(ex_id)


def profile_index(p: str) -> int:
    return PROFILES.index(p)


# =============================================================================
# 1. ruleset integrity
# =============================================================================
class TestRulesetIntegrity(unittest.TestCase):
    def test_top_level_sections_present(self):
        for key in ("schema_version", "metadata", "profiles", "profile_order", "alphabet", "akshara_model",
                    "meter_eligibility", "light_repha_lexicon", "rules", "maitri_table", "appakavi_17",
                    "samaprasa_corpus", "evaluation_pipeline", "trail_schema", "attested_examples"):
            self.assertIn(key, RS.data, key)

    def test_rule_ids_unique_and_well_formed(self):
        ids = [r["id"] for r in RS.data["rules"]]
        self.assertEqual(len(ids), len(set(ids)))
        for rid in ids:
            self.assertRegex(rid, RULE_ID_RE)

    def test_rule_count_covers_the_catalogue(self):
        families = {rid.split("-")[1] for rid in RS.rules}
        self.assertEqual(families, {"POS", "SAMA", "SAMYUKTA", "PURVAKA", "PURVAKSHARA", "MAITRI",
                                    "REPHAYUTA", "VAIRA", "DEFECT"})
        self.assertGreaterEqual(len(RS.rules), 60)

    def test_every_rule_has_required_fields(self):
        for rid, r in RS.rules.items():
            with self.subTest(rule=rid):
                self.assertIn("en", r["names"])
                self.assertIn("te", r["names"])
                self.assertIn(r["status"], VALID_STATUSES)
                self.assertIn("category", r)
                self.assertIn("sections", r["source"])
                self.assertTrue(r["source"]["sections"])
                self.assertTrue(r.get("statement") or r.get("condition"))

    def test_profiles_are_nested_monotonically(self):
        s, r, h = (RS.profiles[p] for p in ("strict", "relaxed", "historical"))
        self.assertTrue(s < r < h)
        for p in PROFILES:
            self.assertNotIn("forbidden", RS.profiles[p])
        self.assertIn("accepted_relaxation", r)
        self.assertNotIn("accepted_relaxation", s)
        self.assertIn("deprecated", h)
        self.assertNotIn("deprecated", r)

    def test_maitri_table_references_are_sound(self):
        seen = set()
        for pair in RS.data["maitri_table"]["pairs"]:
            key = frozenset(pair["consonants"])
            self.assertEqual(len(key), 2, pair)
            for c in key:
                self.assertIn(c, RS.consonants, c)
            self.assertIn(pair["rule"], RS.rules, pair["rule"])
            self.assertNotIn(key, seen, f"duplicate pair {pair}")
            seen.add(key)
        self.assertIn(RS.maitri_default, RS.rules)
        self.assertEqual(RS.status(RS.maitri_default), "forbidden")
        for rid in RS.data["maitri_table"]["structural_rules"]:
            self.assertIn(rid, RS.rules)

    def test_maitri_statuses_are_only_relaxation_deprecated_or_forbidden(self):
        for rid in set(RS.maitri.values()):
            self.assertIn(RS.status(rid), {"accepted_relaxation", "orthographic_relaxation", "deprecated", "forbidden"}, rid)

    def test_examples_ids_unique_and_rules_exist(self):
        ids = [ex["id"] for ex in RS.examples]
        self.assertEqual(len(ids), len(set(ids)))
        for ex in RS.examples:
            with self.subTest(example=ex["id"]):
                self.assertIn(ex["rule"], RS.rules)
                self.assertGreaterEqual(len(ex["padas"]), 2)
                self.assertIn(ex["input_kind"], {"full_padas", "pada_initial_slice", "synthetic"})
                for rid in ex["expected"].get("classifications_include", []):
                    self.assertIn(rid, RS.rules)
                for rid in ex["expected"].get("failing_rules_include", []):
                    self.assertIn(rid, RS.rules)
                if "min_profile" in ex["expected"] and ex["expected"]["min_profile"] is not None:
                    self.assertIn(ex["expected"]["min_profile"], PROFILES)

    def test_rules_examples_pointers_exist(self):
        ex_ids = {ex["id"] for ex in RS.examples}
        for rid, r in RS.rules.items():
            for ex_id in r.get("examples", []):
                self.assertIn(ex_id, ex_ids, f"{rid} points at unknown example {ex_id}")

    def test_appakavi_17_complete_and_mapped(self):
        entries = RS.data["appakavi_17"]["entries"]
        self.assertEqual([e["n"] for e in entries], list(range(1, 18)))
        for e in entries:
            for rid in e["rules"]:
                self.assertIn(rid, RS.rules, f"Appakavi #{e['n']} -> {rid}")
        for rid in RS.data["appakavi_17"]["beyond_the_17"]:
            self.assertIn(rid, RS.rules)

    def test_engine_rule_literals_exist_in_yaml(self):
        src = (HERE.parent / "prasa_engine.py").read_text(encoding="utf-8")
        for rid in sorted(set(re.findall(r"PRASA-[A-Z]+-[A-Z0-9]+(?:-[A-Z0-9]+)*", src))):
            self.assertIn(rid, RS.rules, f"engine uses {rid} which the YAML does not define")

    def test_pipeline_rule_references_exist(self):
        for step in RS.data["evaluation_pipeline"]:
            for rid in step.get("rules", []):
                self.assertIn(rid, RS.rules)
            for item in step.get("rules_in_order", []):
                for rid in re.findall(r"PRASA-[A-Z]+-[A-Z0-9]+(?:-[A-Z0-9]+)*", item):
                    self.assertIn(rid, RS.rules)

    def test_alphabet_complete(self):
        self.assertEqual(len(BASE_CONSONANTS), 35)
        self.assertEqual(set(BASE_CONSONANTS), set("కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరఱలళవశషసహ"))
        self.assertEqual(set(RS.consonants) - set(BASE_CONSONANTS), {"ౘ", "ౙ"})
        self.assertEqual(len(RS.vargas), 5)
        for name, members in RS.vargas.items():
            self.assertEqual(len(members), 5, name)
        self.assertEqual(RS.parusha, set("కచటతప"))
        self.assertEqual(RS.sarala, set("గజడదబ"))
        self.assertEqual(RS.nasals, set("ఙఞణనమ"))
        self.assertEqual(RS.druta_sandhi_map, {"క": "గ", "చ": "జ", "ట": "డ", "త": "ద", "ప": "బ"})

    def test_samaprasa_corpus_rows_are_consistent(self):
        for row in RS.data["samaprasa_corpus"]:
            with self.subTest(consonant=row["consonant"]):
                self.assertIn(row["consonant"], BASE_CONSONANTS)
                for syl in row["syllables"]:
                    parts = pe.parse_akshara(syl)
                    self.assertEqual(parts.onset, [row["consonant"]], syl)


# =============================================================================
# 2. the lookup table
# =============================================================================
class TestLookupTable(unittest.TestCase):
    def test_identity_for_every_consonant(self):
        for c in RS.consonants:
            entry = pe.lookup_pair(c, c, RS)
            self.assertEqual(entry["rule"], "PRASA-SAMA-01")
            self.assertEqual(entry["min_profile"], "strict")
            self.assertEqual(entry["accepted_in"], PROFILES)

    def test_dantya_letters_are_identity_with_their_palatals(self):
        self.assertEqual(pe.lookup_pair("ౘ", "చ", RS)["rule"], "PRASA-SAMA-01")
        self.assertEqual(pe.lookup_pair("ౙ", "జ", RS)["rule"], "PRASA-SAMA-01")
        self.assertEqual(pe.lookup_pair("ౘ", "జ", RS)["rule"], "PRASA-VAIRA-GENERIC")

    def test_symmetry(self):
        for a, b in itertools.combinations(RS.consonants, 2):
            self.assertEqual(pe.lookup_pair(a, b, RS)["rule"], pe.lookup_pair(b, a, RS)["rule"], (a, b))

    def test_matrix_is_complete_and_deterministic(self):
        m1 = pe.maitri_matrix(RS)
        m2 = pe.maitri_matrix(RS)
        self.assertEqual(m1, m2)
        self.assertEqual(len(m1), 35 * 36 // 2)
        for row in m1:
            self.assertIn(row["rule"], RS.rules)
            status = RS.status(row["rule"])
            expected_min = RS.min_profile([status])
            self.assertEqual(row["min_profile"], expected_min, row)
            self.assertEqual(row["accepted_in"], [p for p in PROFILES if RS.accepted(p, status)])

    def test_accepted_relaxations(self):
        for a, b, rule in (("స", "శ", "PRASA-MAITRI-SA-SHA"), ("థ", "ధ", "PRASA-MAITRI-THA-DHA"),
                           ("న", "ణ", "PRASA-MAITRI-NA-NNA"), ("ల", "ళ", "PRASA-MAITRI-LA-LLA")):
            e = pe.lookup_pair(a, b, RS)
            self.assertEqual(e["rule"], rule)
            self.assertEqual(e["status"], "accepted_relaxation")
            self.assertEqual(e["min_profile"], "relaxed")
            self.assertEqual(e["accepted_in"], ["relaxed", "historical"])

    def test_deprecated_pairs(self):
        for a, b, rule in (("స", "ష", "PRASA-MAITRI-SA-SSA"), ("ల", "డ", "PRASA-MAITRI-LA-DA"),
                           ("ళ", "డ", "PRASA-MAITRI-LA-DA"), ("ద", "ధ", "PRASA-MAITRI-DA-DHA")):
            e = pe.lookup_pair(a, b, RS)
            self.assertEqual(e["rule"], rule)
            self.assertEqual(e["status"], "deprecated")
            self.assertEqual(e["accepted_in"], ["historical"])

    def test_forbidden_pairs_are_named(self):
        named = {("ట", "డ"): "PRASA-VAIRA-TA-DA", ("ద", "డ"): "PRASA-VAIRA-DA-DDA",
                 ("డ", "ఢ"): "PRASA-VAIRA-DDA-DDHA", ("ర", "ల"): "PRASA-VAIRA-RA-LA"}
        for pair in (("క", "ఖ"), ("గ", "ఘ"), ("చ", "ఛ"), ("ట", "ఠ"), ("ప", "ఫ"), ("బ", "భ")):
            named[pair] = "PRASA-VAIRA-SVAVARGAJA-EXT"
        for (a, b), rule in named.items():
            e = pe.lookup_pair(a, b, RS)
            self.assertEqual(e["rule"], rule, (a, b))
            self.assertEqual(e["status"], "forbidden")
            self.assertEqual(e["accepted_in"], [])
            self.assertIsNone(e["min_profile"])

    def test_orthographic_relaxation_ra_rra(self):
        e = pe.lookup_pair("ర", "ఱ", RS)
        self.assertEqual(e["rule"], "PRASA-MAITRI-RA-RRA-ORTHO")
        self.assertEqual(e["status"], "orthographic_relaxation")
        self.assertEqual(e["min_profile"], "relaxed")
        self.assertEqual(e["accepted_in"], ["relaxed", "historical"])
        self.assertEqual(RS.rule("PRASA-MAITRI-RA-RRA-ORTHO")["supersedes"], "PRASA-VAIRA-RA-RRA")
        self.assertEqual(RS.rule("PRASA-VAIRA-RA-RRA")["superseded_by"], "PRASA-MAITRI-RA-RRA-ORTHO")
        self.assertEqual(RS.status("PRASA-VAIRA-RA-RRA"), "forbidden")     # the treatise statement is kept verbatim

    def test_generic_default(self):
        for a, b in (("క", "గ"), ("మ", "ర"), ("శ", "ష"), ("హ", "య"), ("ప", "వ"), ("ద", "న")):
            e = pe.lookup_pair(a, b, RS)
            self.assertEqual(e["rule"], "PRASA-VAIRA-GENERIC", (a, b))
            self.assertEqual(e["accepted_in"], [])

    def test_pair_counts_by_status(self):
        rows = pe.maitri_matrix(RS)
        by_status: dict[str, int] = {}
        for r in rows:
            by_status[r["status"]] = by_status.get(r["status"], 0) + 1
        self.assertEqual(by_status["canonical"], 35)            # identity rows
        self.assertEqual(by_status["accepted_relaxation"], 4)
        self.assertEqual(by_status["deprecated"], 4)
        self.assertEqual(by_status["orthographic_relaxation"], 1)
        self.assertEqual(by_status["forbidden"], 630 - 35 - 4 - 4 - 1)
        named_forbidden = sum(1 for r in rows if r["status"] == "forbidden" and r["rule"] != "PRASA-VAIRA-GENERIC")
        self.assertEqual(named_forbidden, 10)

    def test_sibilants_are_not_transitive(self):
        self.assertEqual(pe.lookup_pair("స", "శ", RS)["min_profile"], "relaxed")
        self.assertEqual(pe.lookup_pair("స", "ష", RS)["min_profile"], "historical")
        self.assertIsNone(pe.lookup_pair("శ", "ష", RS)["min_profile"])


# =============================================================================
# 3. akshara features (aksharanusarika-based)
# =============================================================================
class TestAksharaFeatures(unittest.TestCase):
    def test_parse_simple_and_vowel(self):
        p = pe.parse_akshara("తో")
        self.assertEqual((p.onset, p.vowel, p.bare_vowel), (["త"], "ఓ", False))
        self.assertEqual(pe.parse_akshara("త").vowel, "అ")

    def test_parse_conjunct_geminate_three(self):
        self.assertEqual(pe.parse_akshara("క్రి").onset, ["క", "ర"])
        self.assertEqual(pe.parse_akshara("ర్క").onset, ["ర", "క"])
        self.assertEqual(pe.parse_akshara("క్క").onset, ["క", "క"])
        self.assertEqual(pe.parse_akshara("స్త్ర").onset, ["స", "త", "ర"])

    def test_parse_trailing_signs(self):
        p = pe.parse_akshara("తిన్")
        self.assertEqual((p.onset, p.vowel, p.trailing_pollu), (["త"], "ఇ", ["న"]))
        self.assertEqual(pe.parse_akshara("వుల్").trailing_pollu, ["ల"])
        self.assertTrue(pe.parse_akshara("కం").anusvara)
        self.assertTrue(pe.parse_akshara("హః").visarga)
        self.assertTrue(pe.parse_akshara("దుః").visarga)

    def test_parse_bare_vowel_and_vocalic(self):
        p = pe.parse_akshara("ఋ")
        self.assertTrue(p.bare_vowel)
        self.assertEqual(p.vowel, "ఋ")
        self.assertEqual(pe.parse_akshara("కృ").vowel, "ఋ")
        self.assertEqual(pe.parse_akshara("కౢ").vowel, "ఌ")
        self.assertEqual(pe.parse_akshara("అం").vowel, "అ")

    def test_parse_dantya(self):
        p = pe.parse_akshara("ౘా")
        self.assertEqual(p.onset, ["చ"])
        self.assertEqual(p.onset_raw, ["ౘ"])
        self.assertEqual(p.dantya, ["ౘ"])

    def test_sanitize(self):
        self.assertEqual(pe.sanitize('"లా వొక్కింతయు, లేదు!"'), "లా వొక్కింతయు లేదు")
        self.assertEqual(pe.sanitize("రామోఽహం"), "రామోహం")
        self.assertEqual(pe.sanitize("క‌ష"), "కష")
        self.assertEqual(pe.sanitize("నిౝ కని"), "నిన్ కని")
        self.assertEqual(pe.sanitize("కై"), "కై")     # decomposed ai recomposed by NFC

    def test_extract_positions_and_samslesha(self):
        ln = pe.extract_line("నిన్ వదలి", 4, RS)
        self.assertEqual((ln.purva, ln.prasa), ("నిన్", "వ"))
        self.assertEqual(ln.fused_from_purva, ["న"])
        self.assertEqual(ln.onset, ["న", "వ"])
        self.assertTrue(ln.space_between)
        ln2 = pe.extract_line("నిన్వదలి", 4, RS)
        self.assertEqual(ln2.onset, ["న", "వ"])
        self.assertEqual(ln2.fused_from_purva, [])

    def test_extract_signs_before(self):
        self.assertTrue(pe.extract_line("వాఁడు", 1, RS).ardhabindu_before)
        self.assertFalse(pe.extract_line("వాడు", 1, RS).ardhabindu_before)
        self.assertTrue(pe.extract_line("నిండు", 1, RS).purva_purnabindu)
        self.assertTrue(pe.extract_line("దుఃఖము", 1, RS).purva_visarga)
        ln = pe.extract_line("ఇందుఁగలఁడందు", 1, RS)
        self.assertTrue(ln.purva_purnabindu)
        self.assertFalse(ln.ardhabindu_before)
        self.assertTrue(ln.ardhabindu_after)

    def test_extract_weights(self):
        ln = pe.extract_line("కుక్షిని", 1, RS)
        self.assertEqual((ln.purva_weight_positional, ln.purva_weight_intrinsic), ("U", "I"))
        ln = pe.extract_line("రాక్షస", 1, RS)
        self.assertEqual((ln.purva_weight_positional, ln.purva_weight_intrinsic), ("U", "U"))
        ln = pe.extract_line("అకట", 1, RS)
        self.assertEqual(ln.purva_weight_positional, "I")
        self.assertEqual(pe.extract_line("గావిం", 1, RS).prasa_weight, "U")
        self.assertEqual(pe.extract_line("గావు", 1, RS).prasa_weight, "I")

    def test_hints(self):
        self.assertEqual(pe.extract_line("ఎద్రిచిన", 1, RS).light_cluster_hint, "lexicon")
        self.assertEqual(pe.extract_line("ఈ క్రార", 1, RS).light_cluster_hint, "lexicon")      # క్రార is listed
        self.assertEqual(pe.extract_line("ఈ క్రమము", 1, RS).light_cluster_hint, "word_initial_kraravadi")
        self.assertIsNone(pe.extract_line("చక్రిని", 1, RS).light_cluster_hint)
        self.assertTrue(pe.extract_line("ఈ యున్న", 1, RS).laghu_ya_hint)
        self.assertFalse(pe.extract_line("బోయి", 1, RS).laghu_ya_hint)

    def test_druta_sandhi_reading(self):
        ln = pe.extract_line("నిన్ కని", 1, RS)
        alt = pe.druta_sandhi_reading(ln, RS)
        self.assertIsNotNone(alt)
        self.assertEqual((alt.onset, alt.purva_purnabindu, alt.reading), (["గ"], True, "druta_sandhi"))
        self.assertIsNone(pe.druta_sandhi_reading(pe.extract_line("నిన్ వదలి", 1, RS), RS))

    def test_insufficient_aksharas(self):
        ln = pe.extract_line("క", 1, RS)
        self.assertIsNotNone(ln.error)
        res = pe.evaluate(["క", "కమల"], ruleset=RS)
        self.assertFalse(res.matched)
        self.assertIn("PRASA-POS-01", res.error)
        res = pe.evaluate(["కమల"], ruleset=RS)
        self.assertIn("PRASA-POS-04", res.error)


# =============================================================================
# 4. attested examples (data-driven from the YAML)
# =============================================================================
class TestAttestedExamples(unittest.TestCase):
    def test_every_example_behaves_as_documented(self):
        for ex in RS.examples:
            with self.subTest(example=ex["id"]):
                exp = ex["expected"]
                results = {p: pe.evaluate(ex["padas"], profile=p, ruleset=RS, meter_class=ex.get("meter_class"))
                           for p in PROFILES}
                for p in PROFILES:
                    if p in exp:
                        self.assertEqual(results[p].matched, exp[p], f"{ex['id']} under {p}: {results[p].violations}")
                r0 = results["strict"]
                self.assertIsNone(r0.error, r0.error)
                if "min_profile" in exp:
                    self.assertEqual(r0.min_profile, exp["min_profile"])
                got = {c["rule"] for c in r0.classifications}
                for rid in exp.get("classifications_include", []):
                    self.assertIn(rid, got, f"{ex['id']} lacks classification {rid}; has {sorted(got)}")
                failing = {v["rule"] for v in r0.violations} | {t["rule"] for t in r0.trail if t["status"] == "fail"}
                for rid in exp.get("failing_rules_include", []):
                    self.assertIn(rid, failing, f"{ex['id']} lacks failing rule {rid}; has {sorted(failing)}")
                if "prasa_consonant" in exp:
                    self.assertEqual(r0.prasa_consonant, exp["prasa_consonant"])

    def test_min_profile_is_consistent_with_matched(self):
        for ex in RS.examples:
            with self.subTest(example=ex["id"]):
                for p in PROFILES:
                    res = pe.evaluate(ex["padas"], profile=p, ruleset=RS, meter_class=ex.get("meter_class"))
                    expect = res.min_profile is not None and profile_index(p) >= profile_index(res.min_profile)
                    self.assertEqual(res.matched, expect, f"{ex['id']} {p}: min={res.min_profile}")
                    if not res.matched and res.min_profile is not None:
                        self.assertEqual(res.would_match_under, res.min_profile)

    def test_run_attested_examples_helper_agrees(self):
        report = pe.run_attested_examples(RS)
        self.assertEqual(len(report), len(RS.examples))
        bad = [r for r in report if not r["ok"]]
        self.assertEqual(bad, [])


# =============================================================================
# 5. decision procedure — targeted scenarios
# =============================================================================
class TestDecisionProcedure(unittest.TestCase):
    def test_purnabindu_asymmetry_names_both_lines(self):
        res = pe.evaluate(["నిండుమనసున", "పాదములు"], ruleset=RS)
        v = [x for x in res.violations if x["rule"] == "PRASA-PURVAKA-01"]
        self.assertEqual(len(v), 1)
        self.assertEqual(v[0]["scope"], "pair:1-2")
        self.assertIn("line 1", v[0]["detail"])
        self.assertIn("line 2", v[0]["detail"])

    def test_anunasika_exception_is_pattern_bound(self):
        ok = pe.evaluate(["మిన్నేఱు", "సంనుతి"], profile="historical", ruleset=RS)
        self.assertTrue(ok.matched)
        self.assertIn("PRASA-MAITRI-ANUNASIKA", [c["rule"] for c in ok.classifications])
        self.assertTrue(any(t["rule"] == "PRASA-PURVAKA-01" and t["status"] == "note" for t in ok.trail))
        bad = pe.evaluate(["మనసు", "సంనుతి"], profile="historical", ruleset=RS)   # simple న, no geminate
        self.assertFalse(bad.matched)
        self.assertIn("PRASA-PURVAKA-01", [v["rule"] for v in bad.violations])

    def test_krarakommu_is_checked_before_halsamyuta(self):
        bad = pe.evaluate(["ఆ క్రుంకె", "ఆ కృపను"], profile="historical", ruleset=RS)
        self.assertFalse(bad.matched)
        self.assertIn("PRASA-REPHAYUTA-KRARAKOMMU", [v["rule"] for v in bad.violations])
        good = pe.evaluate(["ఆ క్రాలు", "ఆ కృపను"], profile="relaxed", ruleset=RS)
        self.assertTrue(good.matched)
        self.assertEqual(good.min_profile, "relaxed")
        self.assertIn("PRASA-MAITRI-RU-HALSAMYUTA", [c["rule"] for c in good.classifications])

    def test_permuted_clusters_are_named_by_the_order_rule(self):
        res = pe.evaluate(["తర్కము", "చక్రిని"], ruleset=RS)
        self.assertEqual([v["rule"] for v in res.violations], ["PRASA-SAMYUKTA-02"])

    def test_adhika_versus_samyuktasamyukta(self):
        adhika = pe.evaluate(["ఆస్త్రము", "శాస్తము"], profile="historical", ruleset=RS)
        self.assertFalse(adhika.matched)
        self.assertIn("PRASA-DEFECT-ADHIKA", [v["rule"] for v in adhika.violations])
        dep = pe.evaluate(["ఆ క్రొక్కారను", "ఆ కాలము"], profile="historical", ruleset=RS)
        self.assertTrue(dep.matched)
        self.assertEqual(dep.min_profile, "historical")

    def test_triprasa_is_flagged(self):
        res = pe.evaluate(["ఆ త్రిపురము", "మా తిరము"], profile="historical", ruleset=RS)
        self.assertTrue(res.matched)
        notes = [t for t in res.trail if t["rule"] == "PRASA-MAITRI-SAMYUKTASAMYUKTA"]
        self.assertTrue(notes and notes[0]["data"].get("triprasa") is True)

    def test_santa_pattern_is_identified_but_never_accepted(self):
        for p in PROFILES:
            res = pe.evaluate(["దేవర", "నిన్ వదలి"], profile=p, ruleset=RS)
            self.assertFalse(res.matched)
            self.assertTrue(any(t["rule"] == "PRASA-DEFECT-SANTA" and t["status"] == "note" for t in res.trail))
            self.assertTrue(any(t["rule"] == "PRASA-POS-06" for t in res.trail))

    def test_druta_sandhi_reading_is_flagged_and_optional(self):
        padas = ex_by_id("EX-DRUTA-SANDHI-READING")["padas"]
        res = pe.evaluate(padas, ruleset=RS)
        self.assertTrue(res.matched)
        self.assertTrue(any(t["rule"] == "PRASA-POS-07" and t["status"] == "pass" for t in res.trail))
        self.assertEqual(res.lines[0]["reading"], "druta_sandhi")
        self.assertEqual(res.prasa_consonant, "గ")
        off = pe.evaluate(padas, ruleset=RS, allow_druta_sandhi_reading=False)
        self.assertFalse(off.matched)                       # strict profile: the written reading only reaches 'relaxed'
        self.assertEqual(off.min_profile, "relaxed")        # via PRASA-MAITRI-BINDU-SAMSLESHA (ంగ ~ న్క)
        self.assertIn("PRASA-MAITRI-BINDU-SAMSLESHA", [v["rule"] for v in off.violations])
        self.assertEqual(off.lines[0]["reading"], "as_written")

    def test_weight_rule_exempt_for_asama_vritta(self):
        padas = ex_by_id("EX-WEIGHT-FAIL")["padas"]
        self.assertFalse(pe.evaluate(padas, ruleset=RS).matched)
        res = pe.evaluate(padas, ruleset=RS, meter_class="asama_vritta")
        self.assertTrue(res.matched)
        self.assertTrue(any(t["rule"] == "PRASA-PURVAKSHARA-01" and t["status"] == "na" for t in res.trail))

    def test_weight_rule_reports_every_line(self):
        res = pe.evaluate(ex_by_id("EX-WEIGHT-FAIL")["padas"], ruleset=RS)
        fail = [t for t in res.trail if t["rule"] == "PRASA-PURVAKSHARA-01" and t["status"] == "fail"][0]
        self.assertEqual(fail["scope"], "stanza")
        for i in range(1, 5):
            self.assertIn(f"line {i}", fail["data"])
        self.assertIn("PRASA-SAMA-01", [c["rule"] for c in res.classifications])   # consonant did match

    def test_light_cluster_rescue_path(self):
        a = pe.extract_line("ఎద్రిచిన", 1, RS)
        b = pe.extract_line("పద్రిచిన", 2, RS)
        b.purva_weight_positional = "I"        # force a non-uniform positional view
        ok, trail, classes = pe._weight_rule([a, b], RS, None)
        self.assertTrue(ok)
        self.assertEqual(classes, ["PRASA-PURVAKSHARA-04"])
        self.assertTrue(trail[-1]["data"]["heuristic"] if isinstance(trail[-1], dict) else trail[-1].data["heuristic"])

    def test_meter_eligibility(self):
        padas = ex_by_id("EX-SAMA-KA")["padas"]
        self.assertTrue(pe.evaluate(padas, ruleset=RS, meter="utpalamala").applicable)
        res = pe.evaluate(padas, ruleset=RS, meter="seesamu")
        self.assertFalse(res.applicable)
        self.assertTrue(any(t["rule"] == "PRASA-POS-02" and t["status"] == "na" for t in res.trail))
        self.assertTrue(pe.evaluate(padas, ruleset=RS, meter="కందము").applicable)
        unknown = pe.evaluate(padas, ruleset=RS, meter="no-such-meter")
        self.assertTrue(unknown.applicable)
        self.assertFalse(unknown.meter["known"])

    def test_dvyakshara_is_informational(self):
        res = pe.evaluate(["కమలము", "విమలము"], ruleset=RS)
        self.assertTrue(res.matched)
        self.assertTrue(any(t["rule"] == "PRASA-DEFECT-ADHIKA" and t["status"] == "info" for t in res.trail))

    def test_bare_vowels(self):
        self.assertFalse(pe.evaluate(["అఇట", "కఈము"], profile="historical", ruleset=RS).matched)
        self.assertFalse(pe.evaluate(["అఇట", "కమము"], profile="historical", ruleset=RS).matched)
        self.assertFalse(pe.evaluate(["బా ఋభు", "కా క్రమ"], profile="historical", ruleset=RS).matched)

    def test_khandakhanda_variants(self):
        self.assertEqual(pe.evaluate(["లఁట", "వట"], ruleset=RS).classifications[1]["rule"], "PRASA-PURVAKA-04A")
        self.assertIn("PRASA-PURVAKA-04B", [c["rule"] for c in pe.evaluate(["బాఁకిడిన", "దాకారిత"], ruleset=RS).classifications])
        wide = pe.evaluate(["వాఁడు", "పాడు"], ruleset=RS)
        self.assertFalse(wide.matched)
        self.assertEqual(wide.min_profile, "relaxed")

    def test_maitri_inside_clusters_and_geminate_guard(self):
        self.assertEqual(pe.evaluate(["అర్థము", "సర్ధము"], ruleset=RS).min_profile, "relaxed")     # ర్థ ~ ర్ధ
        self.assertEqual(pe.evaluate(["అస్సలు", "వశ్శల"], ruleset=RS).min_profile, "relaxed")     # స్స ~ శ్శ
        bad = pe.evaluate(["అస్సలు", "వస్తల"], profile="historical", ruleset=RS)             # geminate vs unrelated cluster
        self.assertFalse(bad.matched)
        self.assertIn("PRASA-SAMYUKTA-03", [v["rule"] for v in bad.violations])

    def test_geminate_under_abheda(self):
        res = pe.evaluate(["అల్లము", "కళ్లము"], ruleset=RS)                                   # ల్ల ~ ళ్ల
        self.assertEqual(res.min_profile, "relaxed")
        self.assertIn("PRASA-MAITRI-LA-LLA", [c["rule"] for c in res.classifications])
        self.assertIn("PRASA-SAMYUKTA-03", [c["rule"] for c in res.classifications])

    def test_bindu_samslesha_spellings(self):
        same = pe.evaluate(["ఎందు", "చున్దర్పము"], ruleset=RS)                                 # ంద ~ న్ద
        self.assertEqual(same.min_profile, "relaxed")
        self.assertIn("PRASA-MAITRI-BINDU-SAMSLESHA", [c["rule"] for c in same.classifications])
        soft = pe.evaluate(["చెంగని", "నిన్కని"], ruleset=RS)                                  # ంగ ~ న్క
        self.assertEqual(soft.min_profile, "relaxed")
        other = pe.evaluate(["ఎందు", "చున్మతి"], profile="historical", ruleset=RS)             # న్మ is not ంద
        self.assertFalse(other.matched)
        self.assertIn("PRASA-PURVAKA-01", [v["rule"] for v in other.violations])

    def test_ra_rra_trail_names_the_superseded_rule(self):
        res = pe.evaluate(["సారము", "పేఱు"], profile="relaxed", ruleset=RS)
        self.assertTrue(res.matched)
        self.assertEqual(res.min_profile, "relaxed")
        self.assertIn("PRASA-MAITRI-RA-RRA-ORTHO", [c["rule"] for c in res.classifications])
        self.assertTrue(any(t["rule"] == "PRASA-VAIRA-RA-RRA" and t["status"] == "note" for t in res.trail))
        strict = pe.evaluate(["సారము", "పేఱు"], profile="strict", ruleset=RS)
        self.assertFalse(strict.matched)
        self.assertEqual(strict.would_match_under, "relaxed")

    def test_saraladesa_note_is_identification_only(self):
        res = pe.evaluate(ex_by_id("EX-SARALADESA-NOTE")["padas"], profile="historical", ruleset=RS)
        self.assertFalse(res.matched)
        self.assertTrue(any(t["rule"] == "PRASA-SAMA-12" and t["status"] == "note" for t in res.trail))

    def test_vikalpa_requires_nasal_second_member(self):
        self.assertEqual(pe.evaluate(["అగ్ని", "భుఙ్ని"], ruleset=RS).min_profile, "relaxed")
        self.assertIsNone(pe.evaluate(["అగ్ర", "భుఙ్ర"], ruleset=RS).min_profile)


# =============================================================================
# 6. provenance trail
# =============================================================================
class TestProvenanceTrail(unittest.TestCase):
    SCOPE_RE = re.compile(r"^(line:\d+|pair:\d+-\d+|stanza)$")

    def test_trail_entries_well_formed(self):
        for ex in RS.examples[:40]:
            res = pe.evaluate(ex["padas"], profile="relaxed", ruleset=RS)
            for t in res.trail:
                self.assertIn(t["rule"], RS.rules)
                self.assertIn(t["status"], {"pass", "fail", "info", "note", "na"})
                self.assertRegex(t["scope"], self.SCOPE_RE)
                self.assertTrue(t["detail"])
            for v in res.violations:
                self.assertIn(v["rule"], RS.rules)
                self.assertRegex(v["scope"], self.SCOPE_RE)

    def test_pair_count_and_scopes(self):
        res = pe.evaluate(ex_by_id("EX-SAMA-KA")["padas"], ruleset=RS)
        self.assertEqual([p["lines"] for p in res.pairs], [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]])

    def test_determinism(self):
        for ex_id in ("EX-SAMA-KA", "EX-ANUNASIKA", "EX-DRUTAM-FUSION-FAIL", "EX-MAITRI-RU-RA"):
            padas = ex_by_id(ex_id)["padas"]
            self.assertEqual(pe.evaluate(padas, ruleset=RS).to_json(), pe.evaluate(padas, ruleset=RS).to_json())

    def test_permutation_invariance_of_verdict(self):
        for ex_id in ("EX-SAMA-KA", "EX-MAITRI-SA-SHA", "EX-PURNABINDU-DA", "EX-VAIRA-RA-RRA", "EX-KHANDAKHANDA-WIDE"):
            padas = ex_by_id(ex_id)["padas"]
            base = pe.evaluate(padas, profile="historical", ruleset=RS)
            for perm in itertools.permutations(padas):
                res = pe.evaluate(list(perm), profile="historical", ruleset=RS)
                self.assertEqual((res.matched, res.min_profile), (base.matched, base.min_profile), (ex_id, perm))
                self.assertEqual({c["rule"] for c in res.classifications} - {"PRASA-PURVAKA-04A", "PRASA-PURVAKA-04B", "PRASA-PURVAKA-04C"},
                                 {c["rule"] for c in base.classifications} - {"PRASA-PURVAKA-04A", "PRASA-PURVAKA-04B", "PRASA-PURVAKA-04C"})

    def test_result_round_trips_through_json(self):
        res = pe.evaluate(ex_by_id("EX-PURNABINDU-HA-VISARGA")["padas"], ruleset=RS)
        data = json.loads(res.to_json())
        self.assertEqual(data["matched"], True)
        self.assertEqual(data["ruleset"]["schema_version"], RS.version)
        self.assertEqual(len(data["lines"]), 4)

    def test_labels(self):
        self.assertTrue(pe.evaluate(ex_by_id("EX-PURNABINDU-DA")["padas"], ruleset=RS).label_te.startswith("పూర్ణబిందుపూర్వక"))
        self.assertIn("స-శ", pe.evaluate(ex_by_id("EX-MAITRI-SA-SHA")["padas"], ruleset=RS).label_te)
        self.assertEqual(pe.evaluate(ex_by_id("EX-SAMA-RRA")["padas"], ruleset=RS).label_te, "శకటరేఫ ప్రాస")
        self.assertEqual(pe.evaluate(ex_by_id("EX-SAMA-RA-REAL")["padas"], ruleset=RS).label_te, "రేఫ ప్రాస")
        self.assertIn("ద్విత్వాక్షర", pe.evaluate(ex_by_id("EX-DVITVA-KKA")["padas"], ruleset=RS).label_te)
        self.assertTrue(pe.evaluate(ex_by_id("EX-VISARGA-PURVAKA")["padas"], ruleset=RS).label_en.startswith("visarga-pūrvaka"))

    def test_classifications_carry_names_and_status(self):
        res = pe.evaluate(ex_by_id("EX-MAITRI-THA-DHA-BINDU")["padas"], ruleset=RS)
        rules = {c["rule"]: c for c in res.classifications}
        self.assertEqual(rules["PRASA-MAITRI-THA-DHA"]["status"], "accepted_relaxation")
        self.assertTrue(rules["PRASA-MAITRI-THA-DHA"]["name_te"])
        self.assertIn("PRASA-PURVAKA-01", rules)

    def test_violation_under_strict_points_to_needed_profile(self):
        res = pe.evaluate(ex_by_id("EX-MAITRI-SA-SHA")["padas"], profile="strict", ruleset=RS)
        self.assertFalse(res.matched)
        self.assertEqual(res.would_match_under, "relaxed")
        self.assertTrue(all("relaxed" in v["detail"] for v in res.violations))


# =============================================================================
# 7. CLI
# =============================================================================
class TestCLI(unittest.TestCase):
    def _run(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = pe.main(argv)
        return code, buf.getvalue()

    def test_check_json(self):
        code, out = self._run(["check", "--json", "--profile", "relaxed"] + ex_by_id("EX-MAITRI-SA-SHA")["padas"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertTrue(data["matched"])
        self.assertEqual(data["min_profile"], "relaxed")

    def test_check_text(self):
        code, out = self._run(["check"] + ex_by_id("EX-DRUTAM-FUSION-FAIL")["padas"])
        self.assertEqual(code, 0)
        self.assertIn("PRASA-SAMYUKTA-01", out)
        self.assertIn("matched      : False", out)

    def test_lookup_and_matrix(self):
        code, out = self._run(["lookup", "ర", "ఱ"])
        self.assertEqual(json.loads(out)["rule"], "PRASA-MAITRI-RA-RRA-ORTHO")
        code, out = self._run(["lookup", "ట", "డ"])
        self.assertEqual(json.loads(out)["rule"], "PRASA-VAIRA-TA-DA")
        code, out = self._run(["matrix", "--tsv"])
        self.assertEqual(len(out.strip().split("\n")), 631)

    def test_examples_and_rules_commands(self):
        code, out = self._run(["examples"])
        self.assertEqual(code, 0)
        self.assertIn(f"{len(RS.examples)}/{len(RS.examples)} attested examples", out)
        code, out = self._run(["rules"])
        self.assertEqual(len(out.strip().split("\n")), len(RS.rules))


if __name__ == "__main__":
    unittest.main(verbosity=2)

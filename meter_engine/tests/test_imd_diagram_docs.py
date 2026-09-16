# -*- coding: utf-8 -*-
"""diagram.py, render.py, docs.py — text well-formed, one artifact per meter."""
import re
import tempfile
import unittest
from pathlib import Path

from imd_support import HERE, dawg
from indic_meter_dawg import diagram as dg
from indic_meter_dawg import docs as dc
from indic_meter_dawg import render as rd
from indic_meter_dawg.constraints import describe
from indic_meter_dawg.grammar import derive, to_strict

D = dawg()
CAT = D.catalogue
EDGE = re.compile(r'^\s*"([^"]+)"\s*->\s*"([^"]+)"')
NODE = re.compile(r'^\s*"([^"]+)"\s*(\[|;)')


def dot_ok(text):
    """Balanced braces; every edge endpoint declared as a node."""
    assert text.count("{") == text.count("}"), "unbalanced braces"
    nodes, edges = set(), []
    for line in text.splitlines():
        m = NODE.match(line)
        if m:
            nodes.add(m.group(1))
        m = EDGE.match(line)
        if m:
            edges.append((m.group(1), m.group(2)))
    missing = [e for e in edges if e[0] not in nodes or e[1] not in nodes]
    assert not missing, f"edges to undeclared nodes: {missing[:3]}"
    return len(nodes), len(edges)


class TestRuleCards(unittest.TestCase):
    def test_dot_well_formed_for_every_meter(self):
        for m in CAT.concrete:
            with self.subTest(m=m.name):
                text = dg.rule_card_dot(m, D)
                n_nodes, n_edges = dot_ok(text)
                n_ganas = sum(len(m.slots[s]) for s in m.slots)
                self.assertEqual(n_nodes, n_ganas + 2 * len(m.slots))
                self.assertEqual(n_edges, n_ganas + len(m.slots))
                self.assertIn(m.name_te, text)
                for slot in m.slots:
                    self.assertIn(f'cluster_{slot}', text)

    def test_yati_marks(self):
        self.assertIn("యతి", dg.rule_card_dot(CAT.get("tetagiti"), D))
        self.assertIn("యతి @ akshara 10", dg.rule_card_dot(CAT.get("utpalamala"), D))
        text = dg.rule_card_dot(CAT.get("kandamu"), D)
        self.assertEqual(text.count("యతి (gana start)"), 1)     # even slot only

    def test_constraints_visible_in_card(self):
        text = dg.rule_card_dot(CAT.get("kandamu"), D)
        g3 = next(l for l in text.splitlines() if '"even_G3"' in l and "label=" in l)
        self.assertIn("జ IUI", g3)
        self.assertIn("నల IIII", g3)
        self.assertNotIn("భ UII", g3)

    def test_mermaid_well_formed(self):
        for m in CAT.concrete:
            with self.subTest(m=m.name):
                text = dg.rule_card_mermaid(m, D)
                lines = text.splitlines()
                self.assertEqual(lines[0], "flowchart LR")
                self.assertEqual(sum(l.strip().startswith("subgraph") for l in lines),
                                 sum(l.strip() == "end" for l in lines))
                self.assertEqual(text.count("-->"), sum(len(m.slots[s]) for s in m.slots) + len(m.slots))
                self.assertIn("classDef yati", text)


class TestTrieAndDfa(unittest.TestCase):
    def test_unique_from(self):
        self.assertEqual(dg.unique_from({"a": "UUI", "b": "UIU", "c": "III"}), {"a": 2, "b": 2, "c": 1})
        # "UU" is a proper prefix of "UUU": after two symbols only b can *continue*, a is complete
        self.assertEqual(dg.unique_from({"a": "UU", "b": "UUU"}), {"a": 2, "b": 2})

    def test_vritta_trie_lists_every_fixed_meter(self):
        text = dg.vritta_trie_dot(D)
        dot_ok(text)
        for m in CAT.concrete:
            if m.is_fixed:
                self.assertIn(m.name, text)
        pats = dg.fixed_patterns(D)
        self.assertEqual(len(pats), 26)
        uniq = dg.unique_from(pats)
        self.assertEqual(uniq["vidyunmala"], 6)
        self.assertEqual(uniq["utpalamala"], 6)         # మానిని భ భ and భ జ స న meters share its UIIUI opening
        for name, k in uniq.items():
            self.assertLessEqual(k, len(pats[name]))

    def test_dfa_dot(self):
        d = D.slot_dfas[("vidyunmala", "all")]
        text = dg.dfa_dot(d, "vidyunmala")
        n_nodes, n_edges = dot_ok(text)
        self.assertEqual(n_edges, d.n_edges + 1)
        self.assertIn("doublecircle", text)
        self.assertIn("(2)", text)
        big = dg.dfa_dot(D.dfa, "all", max_states=10)
        self.assertIn("too many to draw", big)

    def test_index_markdown(self):
        text = dg.index_markdown(D)
        for m in CAT.meters:
            self.assertIn(f"`{m.name}`", text)
        self.assertIn("370,315", text)


class TestDocs(unittest.TestCase):
    def test_every_meter_doc_mentions_its_rules(self):
        for m in CAT.concrete:
            text = dc.meter_doc_markdown(m, D)
            with self.subTest(m=m.name):
                self.assertTrue(text.startswith(f"# {m.name_te} · {m.name}"))
                self.assertIn("## The rules, one by one", text)
                self.assertIn("## The prosodic grammar", text)
                self.assertIn("## The same grammar, right-linear", text)
                self.assertIn("## One worked derivation", text)
                self.assertIn("Poem →", text)
                self.assertIn("L1.G2", text)
                self.assertIn("symbols already read", text)
                self.assertEqual(text.count("## The same grammar, right-linear"), 1)
                self.assertNotIn("### Each line", text)
                for c in m.constraints:
                    self.assertIn(describe(c).capitalize(), text)
                for c in m.stanza_constraints:
                    self.assertIn(describe(c).capitalize(), text)
                if m.is_variant_of:
                    self.assertIn(m.is_variant_of, text)
                if m.followed_by:
                    self.assertIn("followed by", text)
                self.assertIn(f"grammars/{m.name}.rlg", text)

    def test_worked_derivation_ends_with_a_valid_poem(self):
        from indic_meter_dawg.prosody import accepts_poem
        for m in CAT.concrete:
            text = dc.meter_doc_markdown(m, D)
            block = text.split("The result, one line per row:")[1].split("```")[1].strip()
            lines = block.splitlines()
            with self.subTest(m=m.name):
                self.assertEqual(len(lines), m.padalu)
                self.assertTrue(accepts_poem(m.name, lines))

    def test_describe_token(self):
        self.assertEqual(dc.describe_token("surya", D.registry), "a సూర్యగణము (surya gana): న III or హ UI")
        self.assertEqual(dc.describe_token("భ", D.registry), "భ (bha) UII")
        self.assertIn("4 matras", dc.describe_token("m4", D.registry))
        self.assertIn("all-laghu", dc.describe_token("all_laghu(indra)", D.registry))

    def test_primer(self):
        text = dc.primer_markdown(D)
        self.assertIn("right-linear", text)
        self.assertIn("## Gana glossary", text)
        for m in CAT.concrete:
            self.assertIn(f"]({m.name}.md)", text)

    def test_grammar_file_text(self):
        spec = CAT.get("tetagiti")
        text = dc.grammar_file_text(spec, D)
        for section in ("# ===== 1.", "# ===== 2.", "# ===== 3."):
            self.assertIn(section, text)
        self.assertNotIn("# ===== 4.", text)
        self.assertIn("Poem → Line ⏎ Line ⏎ Line ⏎ Line", text)
        self.assertIn("Line → Surya Indra Indra Surya Surya", text)
        self.assertIn("L1.G5 → III⏎ L2.G1 | UI⏎ L2.G1", text)
        from indic_meter_dawg.prosody import flatten
        for p in to_strict(flatten(spec, D)).productions:
            self.assertIn(p.format(), text)
            self.assertIn(p.comment, text)
        self.assertNotIn("\nG1 →", text)          # the per-line pieces are not repeated
        k = dc.grammar_file_text(CAT.get("kandamu"), D)
        self.assertIn("Poem → Poem⟨U⟩ | Poem⟨I⟩", k)


class TestWriters(unittest.TestCase):
    def test_write_grammars_docs_diagrams_to_temp(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            gfiles = dc.write_grammars(root / "g", D)
            self.assertEqual(len(gfiles), 37)
            self.assertTrue(all(p.suffix == ".rlg" for p in gfiles))
            dfiles = dc.write_docs(root / "d", D)
            self.assertEqual(len(dfiles), 38)
            self.assertTrue((root / "d" / "README.md").is_file())
            files = rd.write_diagrams(root / "x", D, svg=False, include_slot_dfas=False)
            names = {p.name for p in files}
            for m in CAT.concrete:
                self.assertIn(f"{m.name}.dot", names)
                self.assertIn(f"{m.name}.md", names)
            self.assertIn("vritta_trie.dot", names)
            self.assertIn("README.md", names)
            self.assertFalse(any(p.suffix == ".svg" for p in files))

    def test_committed_artifacts_are_current(self):
        """grammars/, docs/grammars/ and diagrams/*.dot in the repo equal a fresh generation."""
        root = HERE.parent
        for m in CAT.concrete:
            p = root / "grammars" / f"{m.name}.rlg"
            with self.subTest(file=p.name):
                self.assertTrue(p.is_file(), "run: python3 -m indic_meter_dawg grammars")
                self.assertEqual(p.read_text(encoding="utf-8"), dc.grammar_file_text(m, D))
        self.assertFalse(list((root / "grammars").glob("*__*.rlg")), "stale per-slot grammar files")
        for m in CAT.concrete:
            p = root / "docs" / "grammars" / f"{m.name}.md"
            with self.subTest(file=p.name):
                self.assertTrue(p.is_file(), "run: python3 -m indic_meter_dawg docs")
                self.assertEqual(p.read_text(encoding="utf-8"), dc.meter_doc_markdown(m, D))
            p = root / "diagrams" / "meters" / f"{m.name}.dot"
            with self.subTest(file=p.name):
                self.assertTrue(p.is_file(), "run: python3 -m indic_meter_dawg diagrams")
                self.assertEqual(p.read_text(encoding="utf-8"), dg.rule_card_dot(m, D))

    @unittest.skipUnless(rd.dot_available(), "graphviz dot not installed")
    def test_render_svg(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "v.svg"
            self.assertTrue(rd.render_dot(dg.rule_card_dot(CAT.get("vidyunmala"), D), out))
            self.assertTrue(out.is_file())
            self.assertIn("<svg", out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

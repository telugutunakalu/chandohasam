# -*- coding: utf-8 -*-
"""parser.py — gana segmentation and yati akshara positions."""
import random
import unittest

from imd_support import dawg, imd, language
from indic_meter_dawg import grammar as gr
from indic_meter_dawg import parser as ps
from indic_meter_dawg import symbols as sy

D = dawg()


class TestSegment(unittest.TestCase):
    def test_segmentation_matches_generating_ganas(self):
        rng = random.Random(31)
        for (m, slot), g in D.grammars.items():
            for _ in range(40):
                chosen = [rng.choice(ganas) for ganas in g.gana_positions]
                line = "".join(x.pattern for x in chosen)
                segs = ps.segment(m, slot, line, D)
                with self.subTest(h=(m, slot), line=line):
                    self.assertTrue(segs)
                    self.assertIn(tuple(x.pattern for x in chosen), [tuple(s.pattern for s in sg.segments) for sg in segs])
                    for sg in segs:
                        self.assertEqual("".join(s.pattern for s in sg.segments), line)
                        self.assertEqual(sg.segments[0].start, 1)
                        self.assertEqual(sg.segments[-1].end, len(line))
                        for a, b in zip(sg.segments, sg.segments[1:]):
                            self.assertEqual(a.end + 1, b.start)
                            self.assertEqual(b.index, a.index + 1)
                        self.assertEqual(sg.matras, sy.matras(line))
                        self.assertFalse(sg.padanta_applied)

    def test_segmentations_are_distinct_and_deterministic(self):
        rng = random.Random(32)
        for (m, slot), g in D.grammars.items():
            line = gr.random_line(g, rng)
            a = ps.segment(m, slot, line, D)
            b = ps.segment(m, slot, line, D)
            self.assertEqual(a, b)
            keys = [tuple(s.pattern for s in sg.segments) for sg in a]
            self.assertEqual(len(keys), len(set(keys)))

    def test_canonical_first_follows_grammar_order(self):
        # kanda even line all-laghu but ending in స: IIII IIII IIII IIII IIU has a unique parse;
        # a line with two parses must list the earlier-alternative parse first
        segs = ps.segment("madhyakkara", "all", "UII" + "UII" + "III" + "UII" + "UII" + "III", D)
        self.assertEqual(segs[0].gana_names, ("భ", "భ", "న", "భ", "భ", "న"))

    def test_non_member_returns_empty(self):
        self.assertEqual(ps.segment("vidyunmala", "all", "UUUUUUU", D), ())
        self.assertEqual(ps.segment("kandamu", "odd", "IUIIUIIUI", D), ())

    def test_every_line_of_a_slot_segments(self):
        for h in (("kandamu", "odd"), ("kandamu", "even"), ("ataveladi", "even"), ("utsahamu", "all")):
            for line in language(*h):
                with self.subTest(h=h, line=line):
                    self.assertTrue(ps.segment(h[0], h[1], line, D))

    def test_padanta_reading(self):
        segs = ps.segment("utpalamala", "all", "UIIUIUIIIUIIUIIUIUII", D)
        self.assertTrue(segs)
        self.assertTrue(all(s.padanta_applied for s in segs))
        self.assertEqual(segs[0].line, "UIIUIUIIIUIIUIIUIUIU")
        self.assertEqual(ps.segment("utpalamala", "all", "UIIUIUIIIUIIUIIUIUII", D, final_laghu_as_guru=False), ())

    def test_unflipped_reading_preferred(self):
        # utsahamu: 7 surya + guru. "…UI" + "I" flipped would also parse; the plain reading wins when it exists
        line = "UI" * 7 + "U"
        segs = ps.segment("utsahamu", "all", line, D)
        self.assertFalse(segs[0].padanta_applied)

    def test_reexport(self):
        self.assertIs(imd.segment, ps.segment)


class TestYati(unittest.TestCase):
    def test_fixed_meters_take_catalogue_positions(self):
        for m in D.catalogue.concrete:
            if not m.is_fixed:
                continue
            line = gr.canonical_line(D.grammars[(m.name, "all")])
            seg = ps.segment(m.name, "all", line, D)[0]
            with self.subTest(m=m.name):
                self.assertEqual(seg.yati_aksharas, m.yati_aksharas["all"])

    def test_gana_meters_take_gana_starts(self):
        rng = random.Random(33)
        for m in D.catalogue.concrete:
            if m.is_fixed:
                continue
            for slot in m.slots:
                g = D.grammars[(m.name, slot)]
                for _ in range(20):
                    line = gr.random_line(g, rng)
                    for seg in ps.segment(m.name, slot, line, D):
                        starts = {s.index: s.start for s in seg.segments}
                        want = tuple(starts[k] for k in m.yati_ganas[slot])
                        with self.subTest(m=m.name, slot=slot, line=line):
                            self.assertEqual(seg.yati_aksharas, want)

    def test_known_positions(self):
        self.assertEqual(ps.segment("tetagiti", "all", "I" * 17, D)[0].yati_aksharas, (12,))
        self.assertEqual(ps.segment("ataveladi", "odd", "I" * 17, D)[0].yati_aksharas, (10,))
        self.assertEqual(ps.segment("ataveladi", "even", "I" * 15, D)[0].yati_aksharas, (10,))
        self.assertEqual(ps.segment("kandamu", "even", "UUUUIUIUUUU", D)[0].yati_aksharas, (8,))
        self.assertEqual(ps.segment("kandamu", "odd", "UUUUUU", D)[0].yati_aksharas, ())
        self.assertEqual(ps.segment("seesamu", "all", "I" * 30, D)[0].yati_aksharas, (9, 25))
        self.assertEqual(ps.segment("sragdhara", "all", gr.canonical_line(D.grammars[("sragdhara", "all")]), D)[0].yati_aksharas, (8, 15))
    def test_format(self):
        seg = ps.segment("vidyunmala", "all", "UUUUUUUU", D)[0]
        self.assertEqual(seg.format(), "UUU UUU UU | మ మ గా | yati@5")
        seg = ps.segment("kandamu", "odd", "UUUUUU", D)[0]
        self.assertTrue(seg.format().endswith("yati@-"))


if __name__ == "__main__":
    unittest.main()

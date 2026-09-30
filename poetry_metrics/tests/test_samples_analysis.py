"""Tests of the scoring used on the generated samples (the 480 MB of sample files are not loaded).

    cd poetry_metrics && python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import madhurya as md              # noqa: E402
import prasada as pr               # noqa: E402
import samples_analysis as sa      # noqa: E402

BASELINES = sa.load_baselines()
VERSE = ["పలికెడిది భాగవత మఁట,", "పలికించెడివాడు రామభద్రుం డఁట, నేఁ"]


class Score(unittest.TestCase):
    def test_a_real_verse(self):
        vocabulary = frozenset(sa.words_of(VERSE))
        row = sa.score(VERSE, BASELINES, vocabulary)
        self.assertEqual(row["real_word_share"], 1.0)
        self.assertEqual(row["n_lines"], 2)
        self.assertAlmostEqual(row["madhurya"], row["inventory"] - row["pileup"])
        self.assertAlmostEqual(sum(row[f"{c}_share"] for c in md.CLASSES), 1.0)

    def test_filler_fools_the_sound_metrics(self):
        """A line of one sonorant is 'strongly alliterative' and 'soft': those metrics measure sound only."""
        filler = ["మమమమమమమమ మమమమమమమమ", "మమమమమమమమ మమమమమమమమ"]
        row = sa.score(filler, BASELINES, frozenset())
        self.assertGreater(row["anuprasa_varga_z"], 3.09)
        self.assertEqual(md.LABELS[row["level"]], "soft")
        self.assertEqual(row["real_word_share"], 0.0)
        self.assertEqual(row["pileup"], 0.0)

    def test_nonsense_clusters_are_harsh_dense_and_obscure(self):
        row = sa.score(["మహ్యుగ్యున్రుత్య్య్మల్రుత్య్య్మల్రుత్"], BASELINES, frozenset())
        self.assertEqual(md.LABELS[row["level"]], "harsh")
        self.assertGreater(row["pileup"], 1.0)
        self.assertGreater(row["rules"].get("P2", 0), 0)
        self.assertEqual(pr.LABELS[row["prasada_level"]], "obscure")
        self.assertGreater(row["ojas"], 2.0)

    def test_one_akshara_words(self):
        row = sa.score(["క క రామ"], BASELINES, frozenset(["రామ"]))
        self.assertAlmostEqual(row["one_akshara_word_share"], 2 / 3)
        self.assertEqual(row["real_word_share"], 1.0)


class Summaries(unittest.TestCase):
    def test_chance_of_outscoring(self):
        self.assertEqual(sa.above([2, 3], [0, 1]), 1.0)
        self.assertEqual(sa.above([1, 1], [1, 1]), 0.5)
        self.assertIsNone(sa.above([], [1]))

    def test_prasada_gate_counts_what_passes(self):
        def row(level, z, repeated=0):
            return {"prasada_level": level, "anuprasa_varga_z": z, "duplicate_lines": repeated, "model": "m",
                    "meter_class": "vrutta", "real_word_share": 0.5}
        gate = sa.prasada_gate([row(0, 9.0), row(2, 1.0, repeated=1), row(4, 0.0), row(None, None)], top=2)
        self.assertEqual(gate["ordinary_or_clearer"], 2)
        self.assertEqual(gate["with_a_repeated_line"], 1)
        self.assertEqual(gate["most_alliterative"], {"n": 2, "obscure": 1, "leaning_obscure": 0, "ordinary": 1,
                                                     "leaning_clear": 0, "clear": 0})

    def test_meter_names_map_to_the_sample_ids(self):
        self.assertEqual(sa.NAME_MAP["aataveladi"], "ataveladi")
        self.assertEqual(sa.NAME_MAP["shardulavikriditamu"], "sardulavikriditamu")


if __name__ == "__main__":
    unittest.main()

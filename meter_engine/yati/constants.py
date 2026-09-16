# -*- coding: utf-8 -*-
"""Shared characters, paths and reading ranks of the yati package.

Reading ranks (see ``readings`` in yati_rules.yaml, rule YATI-EP-03): the lower
the rank, the closer a reading is to the written text; the best accepted match
is the one with the lowest rank sum.
"""
from __future__ import annotations

import re
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent.parent      # …/meter_engine
HERE = ENGINE_DIR                                        # kept for callers of the old module
DEFAULT_RULES_PATH = ENGINE_DIR / "yati_rules.yaml"
DEFAULT_METER_RULES_PATH = ENGINE_DIR / "meter_rules.yaml"

HALANT = "్"            # virama / pollu
ANUSVARA = "ం"          # pūrṇabindu
VISARGA = "ః"
ARDHABINDU = "ఁ"        # arasunna — no effect on yati (YATI-MOD-01)
NAKAARA_POLLU = "ౝ"     # Unicode-14 letter for the drutam న్
PROFILE_ORDER = ["strict", "relaxed", "historical"]
NEVER_ACCEPTED = {"forbidden", "mandatory_fail"}
_DROP = re.compile("[ఽౕౖ\u200c\u200d\u200b\ufeff]")      # avagraha, length marks, zero-width characters

# reading ranks (mirror readings.ranks in the YAML)
RANK_WRITTEN, RANK_CONSTITUENT, RANK_DETACH, RANK_UBHAYA, RANK_SANDHI, RANK_HIDDEN = 0, 1, 2, 3, 4, 5



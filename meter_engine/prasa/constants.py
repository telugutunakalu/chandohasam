# -*- coding: utf-8 -*-
"""
Shared constants of the prāsa package: paths, Unicode building blocks, the profile order.
"""
from __future__ import annotations

from pathlib import Path


HERE = Path(__file__).resolve().parent.parent      # …/meter_engine
ENGINE_DIR = HERE
PROJECT_ROOT = HERE.parent
DEFAULT_RULES_PATH = HERE / "prasa_rules.yaml"
DEFAULT_METER_RULES_PATH = HERE / "meter_rules.yaml"

# --- Unicode building blocks -------------------------------------------------
HALANT = "్"        # ్  virama / pollu
ANUSVARA = "ం"      # ం  pūrṇabindu
VISARGA = "ః"       # ః
ARDHABINDU = "ఁ"    # ఁ  arasunna / ardhabindu (candrabindu)
AVAGRAHA = "ఽ"      # ఽ
ZWSP = "​"
NAKAARA_POLLU = "ౝ"  # ౝ (Unicode 14) — written form of the drutam న్
DANTYA_MAP = {"ౘ": "చ", "ౙ": "జ"}   # ౘ → చ, ౙ → జ  (savarṇa, rule PRASA-SAMA-09)
CONSONANTS = set("కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరఱలళవశషసహ") | set(DANTYA_MAP)
INDEPENDENT_VOWELS = set("అఆఇఈఉఊఋౠఌౡఎఏఐఒఓఔ")
MATRA_TO_VOWEL = {
    "ా": "ఆ", "ి": "ఇ", "ీ": "ఈ", "ు": "ఉ", "ూ": "ఊ", "ృ": "ఋ", "ౄ": "ౠ",
    "ౢ": "ఌ", "ౣ": "ౡ", "ె": "ఎ", "ే": "ఏ", "ై": "ఐ", "ొ": "ఒ", "ో": "ఓ", "ౌ": "ఔ",
}
LONG_VOWELS = set("ఆఈఊౠౡఏఐఓఔ")
IGNORABLE = {" ", "\n", ARDHABINDU, ZWSP}
PROFILE_ORDER = ["strict", "relaxed", "historical"]
NEVER_ACCEPTED = {"forbidden"}
KHANDAKHANDA_RULES = ("PRASA-PURVAKA-04A", "PRASA-PURVAKA-04B", "PRASA-PURVAKA-04C")

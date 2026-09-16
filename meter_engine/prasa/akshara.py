# -*- coding: utf-8 -*-
"""
Text normalisation and the anatomy of one akshara (``AksharaParts``).
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from .constants import (ANUSVARA, CONSONANTS, DANTYA_MAP, HALANT, INDEPENDENT_VOWELS, LONG_VOWELS,
                        MATRA_TO_VOWEL, NAKAARA_POLLU, VISARGA)


_DROP = re.compile("[ఽౕౖ౦-౯౸-౿‌‍]")
_NON_TELUGU = re.compile(r"[^ఀ-౿\s​]+")


def sanitize(text: str) -> str:
    """NFC-normalise, map ౝ to న్, drop avagraha/length-marks/digits/ZWJ, replace
    every non-Telugu run (punctuation, Latin, quotes) by a space, collapse spaces."""
    t = unicodedata.normalize("NFC", text)
    t = t.replace(NAKAARA_POLLU, "న" + HALANT)
    t = _DROP.sub("", t)
    t = _NON_TELUGU.sub(" ", t)
    t = re.sub(r"[\s​]+", " ", t).strip()
    return t


@dataclass
class AksharaParts:
    """Decomposition of ONE akshara string as produced by aksharanusarika."""
    text: str
    onset: list[str]            # consonant sequence with ౘ/ౙ normalised to చ/జ
    onset_raw: list[str]        # consonant sequence as written
    vowel: str                  # independent-vowel form ('అ' = inherent); '' when none
    bare_vowel: bool            # akshara is an independent vowel (no consonant)
    anusvara: bool              # trailing ం
    visarga: bool               # trailing ః
    trailing_pollu: list[str]   # consonants written with a final virama (తిన్ -> ['న'])
    dantya: list[str]           # ౘ/ౙ letters that were present


def parse_akshara(text: str) -> AksharaParts:
    onset_raw: list[str] = []
    trailing: list[str] = []
    vowel = ""
    bare = False
    anusvara = False
    visarga = False
    i, n = 0, len(text)
    while i < n and text[i] in CONSONANTS:
        onset_raw.append(text[i])
        i += 1
        if i < n and text[i] == HALANT:
            i += 1
            if i < n and text[i] in CONSONANTS:
                continue
            trailing.append(onset_raw.pop())      # C + virama at the end = dead consonant
            break
        break
    if onset_raw:
        vowel = "అ"
    elif i < n and text[i] in INDEPENDENT_VOWELS:
        vowel = text[i]
        bare = True
        i += 1
    while i < n:
        ch = text[i]
        if ch in MATRA_TO_VOWEL and onset_raw:
            vowel = MATRA_TO_VOWEL[ch]
            i += 1
        elif ch == ANUSVARA:
            anusvara = True
            i += 1
        elif ch == VISARGA:
            visarga = True
            i += 1
        elif ch in CONSONANTS and i + 1 < n and text[i + 1] == HALANT:
            trailing.append(ch)
            i += 2
        else:
            i += 1
    return AksharaParts(
        text=text,
        onset=[DANTYA_MAP.get(c, c) for c in onset_raw],
        onset_raw=list(onset_raw),
        vowel=vowel,
        bare_vowel=bare,
        anusvara=anusvara,
        visarga=visarga,
        trailing_pollu=trailing,
        dantya=[c for c in onset_raw if c in DANTYA_MAP],
    )


def intrinsic_weight(parts: AksharaParts) -> str:
    """Guru/laghu of an akshara on its own (no conjunct retro-lengthening)."""
    if parts.vowel in LONG_VOWELS or parts.anusvara or parts.visarga or parts.trailing_pollu:
        return "U"
    return "I"


def render_onset(onset: list[str]) -> str:
    return HALANT.join(onset) if onset else ""

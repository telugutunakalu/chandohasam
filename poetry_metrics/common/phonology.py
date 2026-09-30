"""Telugu consonant phonology shared by the poetry metrics.

A line is split into aksharas with the project's splitter
(meter_engine/aksharanusarika.py, the same one the prosody engine uses), and
each akshara yields its consonant tokens. The normalisations follow
Barbadikar & Kulkarni (2024, §5), adapted to Telugu script:

- Spaces are ignored: distances are counted in aksharas across word boundaries.
- Vowels (independent and dependent) carry no consonant token.
- A homorganic nasal written as a conjunct is the anusvāra: న్ద is ంద, మ్ప is ంప.
  The anusvāra ం is one token of its own, with no place of articulation.
- A geminate is one sound held longer, so క్క yields one క.
- The visarga ః is a token (kaṇṭhya, after the Pāṇinīya śikṣā).
- The arasunna ఁ, ZWNJ/ZWJ, digits and punctuation are dropped.

Two consonant groupings:
- VARGA_SERIES merges the four stops of one varga that differ only in voicing
  and aspiration (k/kh/g/gh, c/ch/j/jh, ...); every other consonant (nasals,
  semivowels, sibilants, h, ం, ః) is its own group.
- STHANA is the place of articulation (Pāṇinīya śikṣā, as tabulated by
  Barbadikar & Kulkarni 2024 for śrutyanuprāsa, and by aksharanusarika). v is
  dantoṣṭhya, so it is a class of its own rather than a member of two classes.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "meter_engine"))
import aksharanusarika as _ak  # noqa: E402

HALANT = "్"
ANUSVARA = "ం"
VISARGA = "ః"

# sthāna class -> consonants (the anusvāra is its own class)
STHANA = {
    "kanthya":     "కఖగఘఙహ" + VISARGA,
    "talavya":     "చఛజఝఞయశ",
    "murdhanya":   "టఠడఢణషరఱళ",
    "dantya":      "తథదధనలసౘౙ",
    "oshthya":     "పఫబభమ",
    "dantoshthya": "వ",
    "anusvara":    ANUSVARA,
}
CLASS_OF = {ch: cls for cls, chars in STHANA.items() for ch in chars}
CONSONANTS = frozenset(ch for ch in CLASS_OF if ch not in (ANUSVARA, VISARGA))
SOUNDS = tuple(CLASS_OF)            # every token symbol: consonants, ం, ః

# stop series: one group per varga, nasal excluded; everything else stands alone
_SERIES = ("కఖగఘ", "చఛజఝ", "టఠడఢ", "తథదధ", "పఫబభ")
SERIES_OF = {ch: "/".join(group) for group in _SERIES for ch in group}


def series(ch: str) -> str:
    """The varga-series group of a token symbol (k/kh/g/gh -> 'క/ఖ/గ/ఘ'), else the symbol."""
    return SERIES_OF.get(ch, ch)

# nasal + halant + a stop of the same varga is written ం + stop
_HOMORGANIC = re.compile(r"ఙ్(?=[కఖగఘ])|ఞ్(?=[చఛజఝ])|ణ్(?=[టఠడఢ])|న్(?=[తథదధ])|మ్(?=[పఫబభ])")
_DROP = re.compile(r"[ఁఀ‌‍౦-౯]")
_NON_TELUGU = re.compile(r"[^ఀ-౿\s]+")


def normalise(line: str) -> str:
    """NFC, Telugu block and whitespace only, homorganic nasals as anusvāra."""
    line = unicodedata.normalize("NFC", line)
    line = _NON_TELUGU.sub(" ", line)
    line = _DROP.sub("", line)
    return _HOMORGANIC.sub(ANUSVARA, line)


@lru_cache(maxsize=65536)
def akshara_consonants(akshara: str) -> tuple:
    """Consonant tokens of one akshara, in written order (geminates collapsed)."""
    tokens = []
    prev_was_halant_after = None      # the consonant a halant just closed, for geminate detection
    for ch in akshara:
        if ch in CONSONANTS:
            if prev_was_halant_after == ch:
                prev_was_halant_after = None
                continue              # the second half of a geminate
            tokens.append(ch)
            prev_was_halant_after = None
        elif ch == HALANT:
            prev_was_halant_after = tokens[-1] if tokens else None
        elif ch in (ANUSVARA, VISARGA):
            tokens.append(ch)
            prev_was_halant_after = None
        else:
            prev_was_halant_after = None
    return tuple(tokens)


@dataclass(frozen=True)
class Token:
    char: str        # the consonant (or ం / ః)
    akshara: int     # index of its akshara in the line, spaces not counted
    cls: str         # sthāna class


def aksharas(line: str) -> list:
    """The line's aksharas, spaces and empty chunks removed."""
    return [a for a in _ak.split_aksharalu(normalise(line)) if a.strip()]


def line_tokens(line: str) -> tuple:
    """(aksharas, consonant tokens) of one printed line."""
    aks = aksharas(line)
    tokens = [Token(c, i, CLASS_OF[c]) for i, a in enumerate(aks) for c in akshara_consonants(a)]
    return aks, tuple(tokens)


# ---------------------------------------------------------------------------
# akshara structure: onset cluster, vowel, coda
# ---------------------------------------------------------------------------

VOWEL_OF_SIGN = {
    "ా": "ఆ", "ి": "ఇ", "ీ": "ఈ", "ు": "ఉ", "ూ": "ఊ", "ృ": "ఋ", "ౄ": "ౠ", "ౢ": "ఌ", "ౣ": "ౡ",
    "ె": "ఎ", "ే": "ఏ", "ై": "ఐ", "ొ": "ఒ", "ో": "ఓ", "ౌ": "ఔ",
}
INDEPENDENT_VOWELS = frozenset("అఆఇఈఉఊఋౠఌౡఎఏఐఒఓఔ")
SHORT_VOWELS = frozenset("అఇఉఋఌఎఒ")

# the five vargas: four stops and the class nasal (the sparśa consonants)
VARGAS = ("కఖగఘఙ", "చఛజఝఞ", "టఠడఢణ", "తథదధన", "పఫబభమ")
SPARSHA = frozenset("".join(VARGAS))
CLASS_NASALS = frozenset(v[4] for v in VARGAS)
STOPS = SPARSHA - CLASS_NASALS
# unaspirated + aspirated of one varga and one voicing: క్ఖ గ్ఘ చ్ఛ జ్ఝ ట్ఠ డ్ఢ త్థ ద్ధ ప్ఫ బ్భ
ASPIRATE_PAIRS = frozenset((v[i], v[i + 1]) for v in VARGAS for i in (0, 2))


@dataclass(frozen=True)
class Akshara:
    text: str
    onset: tuple     # consonants before the vowel, as written (a geminate is two)
    vowel: str       # independent form; 'అ' when inherent; '' for a vowel-less chunk
    coda: tuple      # ం, ః and pollu consonants after the vowel


@lru_cache(maxsize=65536)
def parse_akshara(akshara: str) -> Akshara:
    """Onset, vowel and coda of one akshara as the splitter returns it."""
    onset, vowel, coda = [], "", []
    i, n = 0, len(akshara)
    if akshara[0] in INDEPENDENT_VOWELS:
        vowel, i = akshara[0], 1
    else:
        closed = False                       # the cluster ended in a halant: no vowel
        while i < n and akshara[i] in CONSONANTS:
            onset.append(akshara[i])
            i += 1
            if i < n and akshara[i] == HALANT:
                i += 1
                if not (i < n and akshara[i] in CONSONANTS):
                    closed = True
                    break
            else:
                break
        if closed:
            onset, coda = [], onset          # a vowel-less pollu chunk
        elif onset:
            if i < n and akshara[i] in VOWEL_OF_SIGN:
                vowel, i = VOWEL_OF_SIGN[akshara[i]], i + 1
            else:
                vowel = "అ"
    coda += [ch for ch in akshara[i:] if ch in CONSONANTS or ch in (ANUSVARA, VISARGA)]
    return Akshara(akshara, tuple(onset), vowel, tuple(coda))


def line_aksharas(line: str) -> list:
    """The line's aksharas, parsed."""
    return [parse_akshara(a) for a in aksharas(line)]


# ---------------------------------------------------------------------------
# sonority (Parker 2008): 17 ordered classes, 17 = most sonorous
# ---------------------------------------------------------------------------
# low vowels > mid vowels > high vowels > (ə) > (ɨ) > glides > rhotic approximants >
# flaps > laterals > trills > nasals > voiced fricatives > voiced affricates >
# voiced stops > voiceless fricatives and /h/ > voiceless affricates > voiceless stops.
# Telugu: ర is a flap and ఱ a trill; వ is the approximant [ʋ]; చ/జ are affricates;
# an aspirate has the class of its unaspirated counterpart (the scale has no
# aspiration contrast); ఋ is read as it is pronounced in Telugu, with a high vowel.

SONORITY = {}
for _chars, _rank in (("అఆ", 17), ("ఎఏఒఓఐఔ", 16), ("ఇఈఉఊఋౠఌౡ", 15), ("యవ", 12), ("ర", 10),
                      ("లళ", 9), ("ఱ", 8), ("ఙఞణనమ" + ANUSVARA, 7), ("జఝౙ", 5), ("గఘడఢదధబభ", 4),
                      ("శషసహ" + VISARGA, 3), ("చఛౘ", 2), ("కఖటఠతథపఫ", 1)):
    for _ch in _chars:
        SONORITY[_ch] = _rank

# the major classes of the scale, for consonants
SONORANTS = frozenset(ch for ch in CONSONANTS if SONORITY[ch] >= 7)
VOICED_OBSTRUENTS = frozenset(ch for ch in CONSONANTS if 4 <= SONORITY[ch] <= 6)
VOICELESS_OBSTRUENTS = frozenset(ch for ch in CONSONANTS if SONORITY[ch] <= 3)


def segments(a: Akshara) -> tuple:
    """The akshara's sound segments in order: onset consonants, vowel, coda."""
    return a.onset + ((a.vowel,) if a.vowel else ()) + a.coda

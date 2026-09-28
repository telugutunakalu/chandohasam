"""Telugu text units: words, aksharas and normalisation.

The akshara segmenter is a regex over the Telugu block: a (virama-joined)
consonant cluster with its matra and nasal/visarga marks, or an independent
vowel with its marks; a word-final pollu (consonant + virama not followed by a
consonant) attaches to the preceding akshara. That is enough for counting and
for locating akshara boundaries; guru/laghu weights come from the scanners.
"""
import re

_C = "[క-హౘ-ౚ]"          # consonants
_V = "[అ-ఔౠౡ]"           # independent vowels
_M = "[ా-ౌౕౖౢౣ]"  # vowel signs
_MOD = "[ఀ-ఄ]"                      # candrabindu, arasunna, anusvara, visarga
_VIR = "్"
_ZW = "[‌‍]"

AKSHARA = re.compile(
    rf"(?:(?:{_C}{_VIR}{_ZW}?)*{_C}(?!{_VIR}){_M}?{_MOD}*|{_V}{_MOD}*)"
    rf"(?:{_C}{_VIR}{_ZW}?(?!{_C}))?"
)

_NON_WORD = re.compile(r"[^ఀ-౿‌‍a-zA-Z']+")
_ZW_CHARS = re.compile(_ZW)


def words(text: str) -> list:
    """Whitespace words with punctuation/digits stripped; ZWNJ/ZWJ removed."""
    out = []
    for raw in text.split():
        w = _ZW_CHARS.sub("", _NON_WORD.sub("", raw))
        if w:
            out.append(w)
    return out


def aksharas(text: str) -> list:
    return AKSHARA.findall(text)


def akshara_spans(text: str) -> list:
    """(start, end) character offsets of each akshara."""
    return [m.span() for m in AKSHARA.finditer(text)]


def strip_space_punct(text: str) -> str:
    """Whitespace and ASCII punctuation/digits removed. This is the normalisation
    that reproduces the paper's near-duplicate count (160 poems, 79 groups)."""
    return re.sub(r"[\s,.;:!?'\"()\[\]\-–—0-9]", "", text)


def normalise_for_dedup(text: str) -> str:
    """Drop whitespace, punctuation, zero-width joiners and the arasunna/candrabindu
    marks that editions write inconsistently (ఁ U+0C01, ఀ U+0C00)."""
    text = re.sub(r"[ఀఁ‌‍]", "", text)
    return re.sub(r"[^ం-౿]", "", text)


def non_space_chars(text: str) -> int:
    return sum(1 for ch in text if not ch.isspace())

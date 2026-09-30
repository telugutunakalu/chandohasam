"""IAST -> Telugu script, for Sanskrit verses quoted from romanised editions.

Sanskrit e and o are long, so they map to ఏ and ఓ. A consonant not followed by
a vowel takes a halant. The avagraha and any other character pass through
unchanged (the metrics drop everything outside the Telugu block).
"""
from __future__ import annotations

_CONSONANTS = {
    "kh": "ఖ", "gh": "ఘ", "ch": "ఛ", "jh": "ఝ", "ṭh": "ఠ", "ḍh": "ఢ", "th": "థ", "dh": "ధ", "ph": "ఫ", "bh": "భ",
    "k": "క", "g": "గ", "ṅ": "ఙ", "c": "చ", "j": "జ", "ñ": "ఞ", "ṭ": "ట", "ḍ": "డ", "ṇ": "ణ",
    "t": "త", "d": "ద", "n": "న", "p": "ప", "b": "బ", "m": "మ", "y": "య", "r": "ర", "l": "ల", "v": "వ",
    "ś": "శ", "ṣ": "ష", "s": "స", "h": "హ",
}
_VOWELS = {     # IAST -> (independent, sign)
    "ai": ("ఐ", "ై"), "au": ("ఔ", "ౌ"), "ā": ("ఆ", "ా"), "ī": ("ఈ", "ీ"), "ū": ("ఊ", "ూ"), "ṝ": ("ౠ", "ౄ"),
    "ṛ": ("ఋ", "ృ"), "ḷ": ("ఌ", "ౢ"), "a": ("అ", ""), "i": ("ఇ", "ి"), "u": ("ఉ", "ు"), "e": ("ఏ", "ే"),
    "o": ("ఓ", "ో"),
}
_MARKS = {"ṃ": "ం", "ṁ": "ం", "ḥ": "ః"}
_HALANT = "్"


def _match(text: str, i: int, table: dict):
    for size in (2, 1):
        key = text[i:i + size]
        if len(key) == size and key in table:
            return key
    return None


def iast_to_telugu(text: str) -> str:
    text = text.lower()
    out, i, pending = [], 0, False            # pending: a consonant still waiting for its vowel
    while i < len(text):
        c = _match(text, i, _CONSONANTS)
        v = None if c else _match(text, i, _VOWELS)
        if c:
            if pending:
                out.append(_HALANT)
            out.append(_CONSONANTS[c])
            pending, i = True, i + len(c)
        elif v:
            out.append(_VOWELS[v][1] if pending else _VOWELS[v][0])
            pending, i = False, i + len(v)
        else:
            if pending:
                out.append(_HALANT)
                pending = False
            out.append(_MARKS.get(text[i], text[i]))
            i += 1
    if pending:
        out.append(_HALANT)
    return "".join(out)

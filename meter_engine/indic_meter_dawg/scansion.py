# -*- coding: utf-8 -*-
"""
Guru/laghu marking of Telugu text: Unicode → aksharas (syllables) → U/I.

Re-implementation, for this package, of the three-stage pipeline in the
Indic NeuroSym mid-project report (Phase 5, §3):

1. **codepoint classifier** — every character gets a category
   (consonant, vowel, matra, virama, anusvara, visarga, …);
2. **syllable assembler** — consonant clusters (C(్C)*), a vowel sign,
   trailing anusvara/visarga; a word-final dead consonant (pollu) merges
   backward into the previous syllable;
3. **guru/laghu classifier** — the five guru rules of classical Telugu
   chandassu (Chandodarpanam), a syllable of one-syllable lookahead for
   rule 5, and word-boundary suppression of rule 5.

Guru rules (a syllable is guru when any holds; otherwise laghu):

| id | Telugu | condition |
|---|---|---|
| deergha | దీర్ఘము | long vowel: ఆ ఈ ఊ ౠ ఏ ఓ ౡ or their signs |
| sandhyakshara | సంధ్యక్షరము | diphthong ఐ ఔ / ై ౌ |
| anusvara | అనుస్వారము | full sunna ం (not the arasunna ఁ) |
| visarga | విసర్గ | ః |
| pollu | పొల్లు | the syllable ends in a dead consonant (C్) |
| samyukta | సంయుక్తాక్షర పూర్వము | the next syllable of the same word begins with a conjunct or double consonant |

Two readings the tradition leaves open are recorded as *vikalpa* on the
syllable instead of being decided silently: a laghu before a conjunct that
begins the *next word* (report: rule 5 does not fire across a space), and a
syllable before a ర-vattu conjunct (క్ర, ప్ర …), which "frequently remains
laghu". :func:`scan_line` returns the canonical pattern under the chosen
policy and :attr:`LineScansion.variants` lists the alternative readings, so
the identifier can try them when the canonical one matches no meter.

Owns: text → syllables → weights. Must not know about meters.
"""
from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field, replace
from itertools import product
from typing import Iterable, Optional, Sequence

from . import symbols

# --------------------------------------------------------------------------
# 1. codepoint classifier
# --------------------------------------------------------------------------
CONSONANT = "CONSONANT"
VOWEL = "VOWEL"            # independent vowel letter
MATRA = "MATRA"            # dependent vowel sign
VIRAMA = "VIRAMA"
ANUSVARA = "ANUSVARA"
VISARGA = "VISARGA"
CANDRABINDU = "CANDRABINDU"   # ఁ arasunna: attaches, adds no weight
LENGTH = "LENGTH"          # ౕ ౖ length marks: attach to the syllable
AVAGRAHA = "AVAGRAHA"      # ఽ: ignored
ZW = "ZW"                  # zero-width (non-)joiner
SPACE = "SPACE"
NEWLINE = "NEWLINE"
OTHER = "OTHER"            # punctuation, digits, foreign script: a boundary, no syllable

VIRAMA_CHAR = "్"
ANUSVARA_CHARS = frozenset("ంఄ")     # ం and the combining anusvara above
VISARGA_CHAR = "ః"
CANDRABINDU_CHARS = frozenset("ఀఁ")  # combining candrabindu above, ఁ
LENGTH_CHARS = frozenset("ౕౖ")
AVAGRAHA_CHAR = "ఽ"

MATRA_TO_VOWEL = {
    "ా": "ఆ", "ి": "ఇ", "ీ": "ఈ", "ు": "ఉ", "ూ": "ఊ", "ృ": "ఋ", "ౄ": "ౠ",
    "ె": "ఎ", "ే": "ఏ", "ై": "ఐ", "ొ": "ఒ", "ో": "ఓ", "ౌ": "ఔ",
    "ౢ": "ఌ", "ౣ": "ౡ",
}
INDEPENDENT_VOWELS = frozenset("అఆఇఈఉఊఋౠఌౡఎఏఐఒఓఔ")
LONG_VOWELS = frozenset("ఆఈఊౠఏఓౡ")
DIPHTHONGS = frozenset("ఐఔ")
CONSONANTS = frozenset(chr(c) for c in range(0x0C15, 0x0C3A)) | frozenset("ౘౙౚ")   # క…హ + ౘ ౙ ౚ
RA = "ర"


def classify_char(ch: str) -> str:
    """Category of one character.

    >>> classify_char("క"), classify_char("ా"), classify_char("్"), classify_char("ం"), classify_char(" ")
    ('CONSONANT', 'MATRA', 'VIRAMA', 'ANUSVARA', 'SPACE')
    >>> classify_char("ఁ"), classify_char("అ"), classify_char("1"), classify_char("\\n")
    ('CANDRABINDU', 'VOWEL', 'OTHER', 'NEWLINE')
    """
    if ch in CONSONANTS:
        return CONSONANT
    if ch in INDEPENDENT_VOWELS:
        return VOWEL
    if ch in MATRA_TO_VOWEL:
        return MATRA
    if ch == VIRAMA_CHAR:
        return VIRAMA
    if ch in ANUSVARA_CHARS:
        return ANUSVARA
    if ch == VISARGA_CHAR:
        return VISARGA
    if ch in CANDRABINDU_CHARS:
        return CANDRABINDU
    if ch in LENGTH_CHARS:
        return LENGTH
    if ch == AVAGRAHA_CHAR:
        return AVAGRAHA
    if ch in ("‌", "‍", "​", "﻿"):
        return ZW
    if ch == "\n":
        return NEWLINE
    if ch.isspace():
        return SPACE
    return OTHER


# --------------------------------------------------------------------------
# 2. syllable assembler
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class Syllable:
    """One akshara with what the weight rules need to know about it."""
    text: str
    onset: tuple[str, ...]            # consonants of the cluster, in order ('' vowel-initial)
    vowel: str                        # independent-vowel letter; 'అ' for the inherent vowel; '' for a bare dead consonant
    anusvara: bool
    visarga: bool
    candrabindu: bool
    dead: tuple[str, ...]             # trailing dead consonant(s) merged in (pollu)
    word: int                         # 0-based word index within the line
    start: int                        # char offset of the syllable in the line
    end: int                          # char offset one past its last character
    weight: str = ""                  # 'U' | 'I' once classified
    rules: tuple[str, ...] = ()       # guru rules that fired ('laghu' when none)
    vikalpa: str = ""                 # why the other reading is also admissible ('' = none)

    @property
    def is_conjunct(self) -> bool:
        """Starts with two or more consonants (సంయుక్త / ద్విత్వ)."""
        return len(self.onset) >= 2

    @property
    def is_repha_conjunct(self) -> bool:
        """A conjunct whose last member is ర (ర-వత్తు: క్ర, ప్ర, స్త్ర …)."""
        return self.is_conjunct and self.onset[-1] == RA

    @property
    def alternative_weight(self) -> str:
        return ("I" if self.weight == "U" else "U") if self.vikalpa else self.weight

    @property
    def first_sound(self) -> str:
        """The onset consonant or the vowel: what yati looks at."""
        return self.onset[0] if self.onset else self.vowel


_ZW_CHARS = "\u200C\u200D\u200B\uFEFF"


def _clean(text: str) -> str:
    """Drop zero-width characters from a syllable's text."""
    return "".join(ch for ch in text if ch not in _ZW_CHARS)


def syllabify(line: str) -> tuple[Syllable, ...]:
    """Split one line into aksharas (weights not yet assigned).

    >>> [s.text for s in syllabify("నమస్కారం")]
    ['న', 'మ', 'స్కా', 'రం']
    >>> [s.text for s in syllabify("పూసెన్ తెలుగు")]
    ['పూ', 'సెన్', 'తె', 'లు', 'గు']
    >>> [(s.text, s.word) for s in syllabify("స్త్రీ, అమ్మ")]
    [('స్త్రీ', 0), ('అ', 1), ('మ్మ', 1)]
    """
    out: list[Syllable] = []
    n = len(line)
    i = 0
    word = 0
    in_word = False

    def attach_trailing(i: int, anus: bool, vis: bool, cb: bool):
        while i < n:
            cat = classify_char(line[i])
            if cat == ANUSVARA:
                anus = True
            elif cat == VISARGA:
                vis = True
            elif cat == CANDRABINDU:
                cb = True
            elif cat == LENGTH:
                pass
            else:
                break
            i += 1
        return i, anus, vis, cb

    while i < n:
        ch = line[i]
        cat = classify_char(ch)
        if cat in (SPACE, NEWLINE, OTHER, AVAGRAHA):
            if in_word:
                word += 1
                in_word = False
            i += 1
            continue
        if cat == ZW:
            i += 1
            continue
        start = i
        if cat == CONSONANT:
            onset = [ch]
            i += 1
            dead = False
            while i < n and line[i] == VIRAMA_CHAR:
                j = i + 1
                if j < n and classify_char(line[j]) == ZW:      # explicit non-joiner: virama is a pollu
                    j += 1
                    dead = True
                    i = j
                    break
                if j < n and classify_char(line[j]) == CONSONANT:
                    onset.append(line[j])
                    i = j + 1
                    continue
                dead = True                                       # C్ at the end of a word: pollu
                i = j
                break
            if dead:
                if out and out[-1].word == word and in_word:
                    prev = out[-1]
                    out[-1] = replace(prev, text=_clean(line[prev.start:i]), dead=prev.dead + tuple(onset), end=i)
                else:                                             # a word made of a dead consonant only
                    out.append(Syllable(text=_clean(line[start:i]), onset=(), vowel="", anusvara=False, visarga=False,
                                        candrabindu=False, dead=tuple(onset), word=word, start=start, end=i))
                    in_word = True
                continue
            vowel = "అ"
            if i < n and classify_char(line[i]) == MATRA:
                vowel = MATRA_TO_VOWEL[line[i]]
                i += 1
            i, anus, vis, cb = attach_trailing(i, False, False, False)
            out.append(Syllable(text=_clean(line[start:i]), onset=tuple(onset), vowel=vowel, anusvara=anus, visarga=vis,
                                candrabindu=cb, dead=(), word=word, start=start, end=i))
            in_word = True
            continue
        if cat == VOWEL:
            i += 1
            i, anus, vis, cb = attach_trailing(i, False, False, False)
            out.append(Syllable(text=_clean(line[start:i]), onset=(), vowel=ch, anusvara=anus, visarga=vis,
                                candrabindu=cb, dead=(), word=word, start=start, end=i))
            in_word = True
            continue
        # a stray combining mark (matra/virama/anusvara … with no base): attach to the previous
        # syllable of the same word when there is one, otherwise drop it
        if out and in_word and out[-1].word == word:
            prev = out[-1]
            anus, vis, cb = prev.anusvara, prev.visarga, prev.candrabindu
            if cat == ANUSVARA:
                anus = True
            elif cat == VISARGA:
                vis = True
            elif cat == CANDRABINDU:
                cb = True
            out[-1] = replace(prev, text=_clean(line[prev.start:i + 1]), anusvara=anus, visarga=vis, candrabindu=cb, end=i + 1)
        i += 1
    return tuple(out)


# --------------------------------------------------------------------------
# 3. guru / laghu classifier
# --------------------------------------------------------------------------
RULE_NAMES = {
    "deergha": "దీర్ఘము",
    "sandhyakshara": "సంధ్యక్షరము",
    "anusvara": "అనుస్వారము",
    "visarga": "విసర్గ",
    "pollu": "పొల్లు",
    "samyukta": "సంయుక్తాక్షర పూర్వము",
    "laghu": "లఘువు",
}
VIKALPA_WORD_INITIAL = "word_initial_conjunct"   # next word begins with a conjunct
VIKALPA_REPHA = "repha_conjunct"                  # next syllable is a ర-vattu conjunct


@dataclass(frozen=True)
class ScanPolicy:
    """How the two open readings are decided in the canonical pattern."""
    word_initial_conjunct: str = "laghu"   # 'laghu' (report: a space blocks rule 5) | 'guru'
    repha_conjunct: str = "guru"           # 'guru' (rule 5 as written) | 'laghu' (the licence)

    def __post_init__(self):
        for f in ("word_initial_conjunct", "repha_conjunct"):
            if getattr(self, f) not in ("laghu", "guru"):
                raise ValueError(f"{f} must be 'laghu' or 'guru'")


DEFAULT_POLICY = ScanPolicy()


def self_rules(s: Syllable) -> tuple[str, ...]:
    """Guru rules 1–4, which depend on the syllable alone.

    >>> self_rules(syllabify("రా")[0]), self_rules(syllabify("సం")[0]), self_rules(syllabify("క")[0])
    (('deergha',), ('anusvara',), ())
    """
    rules = []
    if s.vowel in LONG_VOWELS:
        rules.append("deergha")
    if s.vowel in DIPHTHONGS:
        rules.append("sandhyakshara")
    if s.anusvara:
        rules.append("anusvara")
    if s.visarga:
        rules.append("visarga")
    if s.dead:
        rules.append("pollu")
    return tuple(rules)


def classify(syllables: Sequence[Syllable], policy: ScanPolicy = DEFAULT_POLICY) -> tuple[Syllable, ...]:
    """Assign weights (rules 1–5 plus the vikalpa bookkeeping).

    >>> [s.weight for s in classify(syllabify("సత్యము"))]
    ['U', 'I', 'I']
    >>> [s.weight for s in classify(syllabify("స త్యము"))]
    ['I', 'I', 'I']
    >>> [(s.weight, s.vikalpa) for s in classify(syllabify("చక్రి"))]
    [('U', 'repha_conjunct'), ('I', '')]
    """
    out: list[Syllable] = []
    for k, s in enumerate(syllables):
        rules = list(self_rules(s))
        vikalpa = ""
        nxt = syllables[k + 1] if k + 1 < len(syllables) else None
        if nxt is not None and nxt.is_conjunct:
            same_word = nxt.word == s.word
            repha = nxt.is_repha_conjunct
            if same_word:
                if repha:
                    if policy.repha_conjunct == "guru":
                        rules.append("samyukta")
                    vikalpa = VIKALPA_REPHA
                else:
                    rules.append("samyukta")
            else:
                if policy.word_initial_conjunct == "guru" and not (repha and policy.repha_conjunct == "laghu"):
                    rules.append("samyukta")
                vikalpa = VIKALPA_WORD_INITIAL if not repha else f"{VIKALPA_WORD_INITIAL}+{VIKALPA_REPHA}"
        weight = symbols.GURU if rules else symbols.LAGHU
        # the vikalpa only matters when rule 5 is the *only* reason for a guru (or the reason for a laghu)
        if vikalpa and any(r != "samyukta" for r in rules):
            vikalpa = ""
        out.append(replace(s, weight=weight, rules=tuple(rules) or ("laghu",), vikalpa=vikalpa))
    return tuple(out)


# --------------------------------------------------------------------------
# line / stanza API
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class LineScansion:
    text: str
    syllables: tuple[Syllable, ...]
    policy: ScanPolicy = DEFAULT_POLICY

    @property
    def pattern(self) -> str:
        """The canonical U/I string."""
        return "".join(s.weight for s in self.syllables)

    @property
    def aksharas(self) -> tuple[str, ...]:
        return tuple(s.text for s in self.syllables)

    @property
    def vikalpa_positions(self) -> tuple[int, ...]:
        """0-based syllable indices whose weight may be read the other way."""
        return tuple(i for i, s in enumerate(self.syllables) if s.vikalpa)

    def variants(self, limit: int = 64) -> tuple[str, ...]:
        """Every admissible pattern, canonical first (at most ``limit``)."""
        pos = self.vikalpa_positions
        if not pos:
            return (self.pattern,)
        base = list(self.pattern)
        out = []
        for flips in product((False, True), repeat=len(pos)):
            p = list(base)
            for flag, i in zip(flips, pos):
                if flag:
                    p[i] = self.syllables[i].alternative_weight
            out.append("".join(p))
            if len(out) >= limit:
                break
        return tuple(dict.fromkeys(out))

    def format(self) -> str:
        """``శ్రీ కై వ ల్య … | UUUI… | vikalpa@3``"""
        marks = ",".join(str(i + 1) for i in self.vikalpa_positions) or "-"
        return f"{' '.join(self.aksharas)} | {self.pattern} | vikalpa@{marks}"

    def to_dict(self) -> dict:
        return {
            "text": self.text, "pattern": self.pattern,
            "syllables": [{"text": s.text, "weight": s.weight, "rules": list(s.rules), "word": s.word,
                           "vikalpa": s.vikalpa} for s in self.syllables],
            "variants": list(self.variants()),
        }


def scan_line(text: str, policy: ScanPolicy = DEFAULT_POLICY) -> LineScansion:
    """Syllabify and weigh one line.

    >>> scan_line("శ్రీరాముని దయచేతను").pattern
    'UUIIIIUII'
    >>> scan_line("ఇందు గలఁ డందు లేఁ డని").format()
    'ఇం దు గ లఁ డం దు లేఁ డ ని | UIIIUIUII | vikalpa@-'
    """
    return LineScansion(text=text, syllables=classify(syllabify(text), policy), policy=policy)


def split_lines(text: str | Iterable[str]) -> tuple[str, ...]:
    """Lines of a stanza: a string is split on newlines; blanks are dropped."""
    if isinstance(text, str):
        parts = text.splitlines()
    else:
        parts = list(text)
    return tuple(p for p in (unicodedata.normalize("NFC", x).strip() for x in parts) if p)


def scan(text: str | Iterable[str], policy: ScanPolicy = DEFAULT_POLICY) -> tuple[LineScansion, ...]:
    """Scan every line of a stanza.

    >>> [s.pattern for s in scan("శ్రీరాముని దయచేతను\\nధారాళమైన నీతులు")]
    ['UUIIIIUII', 'UUIUIUII']
    """
    scans = tuple(scan_line(ln, policy) for ln in split_lines(text))
    return tuple(s for s in scans if s.syllables)          # lines with no Telugu syllable carry no metre


def patterns(text: str | Iterable[str], policy: ScanPolicy = DEFAULT_POLICY) -> tuple[str, ...]:
    """Just the U/I strings, one per line."""
    return tuple(s.pattern for s in scan(text, policy))


def stanza_variants(scans: Sequence[LineScansion], limit: int = 64) -> tuple[tuple[str, ...], ...]:
    """Cartesian product of the per-line variants, canonical stanza first,
    capped at ``limit`` stanzas."""
    per_line = [s.variants() for s in scans]
    out: list[tuple[str, ...]] = []
    for combo in product(*per_line):
        out.append(tuple(combo))
        if len(out) >= limit:
            break
    return tuple(out)

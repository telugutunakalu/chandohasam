# -*- coding: utf-8 -*-
"""
Guru/laghu of text that is still being written.

A decoder sees the poem one token at a time, and a token may end inside an
akshara (the tokenizer splits శ్రీ as ``శ`` + ``్రీ``). Weights are not final
until the word is: rule 5 looks one syllable ahead, and a trailing dead
consonant can still merge back into the syllable before it (pollu). Under the
default :class:`~indic_meter_dawg.scansion.ScanPolicy` a space blocks rule 5,
so a word boundary is a stable point.

:func:`split_word` divides an unfinished word into

* **committed** syllables — no continuation can change them, and
* **pending options** — every U/I string that the syllables starting inside
  the text may still turn into, over every continuation.

Everything here calls ``scansion.syllabify`` / ``classify`` / ``self_rules``;
no weight rule is implemented twice, so the decoder and the verifier cannot
disagree. Checked on every character prefix of the corpus (2,310,052
prefixes of 49,661 lines, 0 violations; ``tests/test_dec_incremental.py``).

Owns: the committed/pending split. Must not know about meters or tokens.
"""
from __future__ import annotations

import sys
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

ENGINE_DIR = Path(__file__).resolve().parent.parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from indic_meter_dawg import scansion as sc      # noqa: E402

BOUNDARY = frozenset((sc.SPACE, sc.NEWLINE, sc.OTHER, sc.AVAGRAHA))


class WordSplit(NamedTuple):
    committed: str                  # U/I of the syllables no continuation can change
    options: tuple[str, ...]        # U/I strings the pending syllables may still become
    syllables: int                  # syllables of the word as written so far


def is_boundary(ch: str) -> bool:
    """A character that ends a word (space, newline, punctuation, digits …).

    >>> is_boundary(" "), is_boundary(","), is_boundary("క"), is_boundary("్")
    (True, True, False, False)
    """
    return sc.classify_char(ch) in BOUNDARY


def _syllables(word: str) -> tuple[sc.Syllable, ...]:
    return sc.classify(sc.syllabify(unicodedata.normalize("NFC", word)))


@lru_cache(maxsize=200_000)
def word_weights(word: str) -> str:
    """Final weights of a finished word (the same as inside its line).

    >>> word_weights("సత్యము"), word_weights("పూసెన్")
    ('UII', 'UU')
    """
    return "".join(s.weight for s in _syllables(word))


def _open_cluster(s: sc.Syllable, text: str) -> bool:
    """A consonant syllable with nothing after its cluster yet: C(్C)*."""
    if not s.onset or s.dead:
        return False
    return len(sc._clean(text[s.start:s.end])) == 2 * len(s.onset) - 1


@lru_cache(maxsize=400_000)
def split_word(word: str, cluster_can_grow: bool = True, long_pollu: bool = True) -> WordSplit:
    """Committed weights and pending options of an unfinished word.

    ``cluster_can_grow=False`` says no further virama may follow the word's
    final consonant cluster (the orthography filter's limit): an open cluster
    can then neither grow into a longer conjunct nor die as a pollu, and the
    options that need either are dropped. Without this the enforcer could keep
    a state whose only live option is unwritable (found by the random-logit
    control). ``long_pollu=False`` says the word may not end in two or more dead
    consonants (the filter's other word-final rule): the pollu options that
    would need that are dropped too.

    ``a`` is the second-to-last syllable, ``b`` the last; ``w(a)`` is U when
    ``a`` is guru by rules 1–4 or ``b`` begins with a conjunct:

    * ``C్`` with no vowel (word-initial dead consonant): {U, I};
    * ``…V C్`` (``b`` has a vowel and a merged dead consonant):
      {w(a)U, w(a)UU, w(a)UI} — pollu now, or samyukta after a split plus a new syllable;
    * open cluster ``C(్C)*``: {xU, xI : x ∈ {w(a), U}} ∪ {U} — the onset may grow,
      and ``b`` may still die as a pollu;
    * closed syllable: {w(a)U} when ``b`` is already guru, else {w(a)U, w(a)I}.

    >>> split_word("సత్యము")          # స is final (guru before త్య); త్య ము may still change
    WordSplit(committed='U', options=('II', 'IU'), syllables=3)
    >>> split_word("సత్య").options     # త్య may still grow a matra, a conjunct, or die as a pollu
    ('U', 'UI', 'UU')
    >>> split_word("రా").options       # a long vowel is guru whatever follows
    ('U',)
    """
    if not word:
        return WordSplit("", ("",), 0)
    text = unicodedata.normalize("NFC", word)
    syls = _syllables(text)
    if not syls:
        return WordSplit("", ("",), 0)
    m = len(syls)
    k = max(0, m - 2)
    b = syls[-1]
    a = syls[-2] if m >= 2 else None

    def w_a(next_is_conjunct: bool) -> str:
        return "U" if (sc.self_rules(a) or next_is_conjunct) else "I"

    opts: set[str] = set()
    ends_virama = text.endswith(sc.VIRAMA_CHAR)
    if ends_virama and not b.vowel:
        opts |= {"U", "I"}
    elif ends_virama or (b.dead and sc.classify_char(text[-1]) == sc.ZW):
        head = w_a(b.is_conjunct) if a is not None else ""
        opts |= {head + "UU", head + "UI"}
        if long_pollu or len(b.dead) < 2:
            opts.add(head + "U")
    elif _open_cluster(b, text):
        if cluster_can_grow:
            heads = [""] if a is None else sorted({w_a(b.is_conjunct), "U"})
        else:
            heads = [""] if a is None else [w_a(b.is_conjunct)]
        for h in heads:
            opts |= {h + "U", h + "I"}
        if cluster_can_grow and (long_pollu or len(b.onset) < 2):
            opts.add("U")
    else:
        head = w_a(b.is_conjunct) if a is not None else ""
        opts |= {head + "U"} if sc.self_rules(b) else {head + "U", head + "I"}
    return WordSplit("".join(s.weight for s in syls[:k]), tuple(sorted(opts)), m)

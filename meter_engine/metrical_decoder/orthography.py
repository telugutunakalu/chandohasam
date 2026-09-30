# -*- coding: utf-8 -*-
"""
Well-formed Telugu, as a small automaton over character categories.

The scanner absorbs malformed text without complaint — a stray vowel sign
attaches to the previous syllable, a chain of viramas never opens a new one —
so a decoder that checks only the meter can emit tokens forever without adding
a syllable (probe D in CONSTRAINED_DECODING_PLAN.md: ``ౌళ్ెంట్హ్న్స్ార్ేష్…``).
This filter rejects exactly those sequences:

* a dependent sign (vowel sign, virama, ం ః ఁ, length mark) at the start of a word;
* anything but a consonant or a word boundary after a virama;
* a second vowel sign, or a sign after ం / ః / ఁ;
* more than three viramas in one consonant cluster;
* a word that ends in two or more dead consonants (వన్స్, ఫ్రెండ్స్: transliterations only,
  never in the corpus; the prāsa engine splits their final cluster into an akshara of its
  own, which the scanner does not);
* a word of dead consonants alone (న్, క్ష్): no word of the corpus (49,661 lines) is one.
  The scanner reads it as an akshara with neither consonant onset nor vowel, which no
  yati or prāsa partner can match: DiffusionGemma opened two lines with ``న్`` and the
  line's yati could then never be met (plan §15);
* two spaces in a row; zero-width characters.

Every akshara is then at most ten characters long, so tokens cannot stall.
On the corpus the rules never fire except on two typos (``్రోృచ``, ``ముంఁడ``)
and on the ZWNJ that marks an explicit pollu, which generation does not need.
A ``ె`` may take the length mark ``ౖ`` / ``ౕ`` (NFC composes it to ``ై`` / ``ే``).

State: a small int (``VOWELED`` when the current word has a vowel, + kind × 4 + viramas in
the current cluster). Owns the character-level well-formedness check; must not know about
weights or meters.
"""
from __future__ import annotations

from typing import Optional

from .incremental import sc

BOUND, BOUND_SPACE, CONS, HALANT, VSIGN, VSIGN_E, VOWEL, MARK = range(8)
MAX_CLUSTER_VIRAMAS = 3
MAX_FINAL_POLLU = 1                  # dead consonants a word may end in
# The longest akshara the filter lets through: a cluster of 4 consonants and 3 viramas, a vowel
# sign with its length mark (ె + ౖ), one of ం ః ఁ, and a word-final pollu (C + ్).
MAX_AKSHARA_CHARS = (MAX_CLUSTER_VIRAMAS + 1) + MAX_CLUSTER_VIRAMAS + 2 + 1 + 2 * MAX_FINAL_POLLU
START = BOUND * 4
VOWELED = 32                         # flag: the current word has a vowel (inherent or written)

_MARKS = (sc.ANUSVARA, sc.VISARGA, sc.CANDRABINDU)
_E_SIGN = "ె"


def step(state: Optional[int], ch: str) -> Optional[int]:
    """Next state after ``ch``, or None when ``ch`` makes the text malformed.

    >>> s = START
    >>> for ch in "శ్రీ రామ": s = step(s, ch)
    >>> s is not None
    True
    >>> step(START, "ా") is None, step(step(START, "క"), "్") is not None
    (True, True)
    """
    if state is None:
        return None
    voweled, (kind, n) = state & VOWELED, divmod(state & ~VOWELED, 4)
    cat = sc.classify_char(ch)
    if cat in (sc.SPACE, sc.NEWLINE, sc.OTHER, sc.AVAGRAHA):
        if not can_end(state):
            return None
        if cat == sc.SPACE:
            return None if kind == BOUND_SPACE else BOUND_SPACE * 4
        return BOUND * 4
    if cat == sc.ZW:
        return None
    if kind == CONS and cat in (sc.CONSONANT, sc.MATRA) + _MARKS:
        voweled = VOWELED                             # the consonant before keeps a vowel (inherent or this sign)
    if cat == sc.CONSONANT:
        return voweled | CONS * 4 + (n if kind == HALANT else 0)
    if kind == HALANT:
        return None                                   # only a consonant or a boundary may follow a virama
    if cat == sc.VOWEL:
        return VOWELED | VOWEL * 4
    if kind in (BOUND, BOUND_SPACE):
        return None                                   # a dependent sign cannot start a word
    if cat == sc.VIRAMA:
        return voweled | HALANT * 4 + n + 1 if kind == CONS and n < MAX_CLUSTER_VIRAMAS else None
    if cat == sc.MATRA:
        return voweled | (VSIGN_E if ch == _E_SIGN else VSIGN) * 4 if kind == CONS else None
    if cat == sc.LENGTH:
        return voweled | VSIGN * 4 if kind == VSIGN_E else None
    if cat in _MARKS:
        return voweled | MARK * 4 if kind in (CONS, VSIGN, VSIGN_E, VOWEL) else None
    return None


def can_end(state: int) -> bool:
    """A word may end here: it has a vowel and does not close on two or more dead consonants.

    >>> can_end(feed(START, "కన్")), can_end(feed(START, "వన్స్")), can_end(feed(START, "వన్స్ట"))
    (True, False, True)
    >>> can_end(feed(START, "న్")), can_end(feed(START, "క్ష్")), can_end(feed(START, "క్ష"))
    (False, False, True)
    """
    kind, n = divmod(state & ~VOWELED, 4)
    return not (kind == HALANT and (n > MAX_FINAL_POLLU or not state & VOWELED))


def full_cluster(state: int) -> bool:
    """The current consonant cluster holds the most viramas allowed: it can take no other.

    >>> full_cluster(feed(START, "క్ష్మ్య")), full_cluster(feed(START, "క్ష్మ"))
    (True, False)
    """
    return state & ~VOWELED == CONS * 4 + MAX_CLUSTER_VIRAMAS


def feed(state: Optional[int], text: str) -> Optional[int]:
    """Run ``step`` over a string.

    >>> feed(START, "పలికెడిది భాగవత") is not None, feed(START, "క్ా") is None
    (True, True)
    """
    for ch in text:
        state = step(state, ch)
        if state is None:
            return None
    return state


def is_well_formed(text: str) -> bool:
    """True when every character of ``text`` keeps the automaton alive.

    >>> is_well_formed("ఇందు గలఁ డందు లేఁ డని"), is_well_formed("క  ఖ")
    (True, False)
    """
    return feed(START, text) is not None

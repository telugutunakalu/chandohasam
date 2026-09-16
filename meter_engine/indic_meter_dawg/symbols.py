# -*- coding: utf-8 -*-
"""
Alphabet of the metrical DAWG and notation normalisation.

Owns: the two terminal symbols (guru ``U``, laghu ``I``), their matra weights,
and the conversion of every common scansion notation into that alphabet.
Must not know about ganas, meters or automata.
"""
from __future__ import annotations

from typing import Iterable

GURU = "U"
LAGHU = "I"
NEWLINE = "\n"                      # line separator terminal of the prosodic-level grammars
NEWLINE_DISPLAY = "⏎"
ALPHABET: tuple[str, str] = (GURU, LAGHU)
POEM_ALPHABET: tuple[str, str, str] = (GURU, LAGHU, NEWLINE)

MATRAS: dict[str, int] = {GURU: 2, LAGHU: 1, NEWLINE: 0}

# Every accepted spelling of the two symbols. Upper/lower case matters:
# in the breve/macron tradition ``u`` is the laghu and ``U`` (the yaml
# convention, the Telugu textbook half-moon) is the guru.
GURU_SPELLINGS: frozenset[str] = frozenset("U G S - — – ˉ ¯ గ".split())
LAGHU_SPELLINGS: frozenset[str] = frozenset("I L l i u | ˘ ల".split())
SEPARATORS: frozenset[str] = frozenset(" \t\n\r,/·:;")


class NotationError(ValueError):
    """Raised when a scansion string contains a character that is neither a
    guru, a laghu, nor a separator."""


def normalize(text: str) -> str:
    """Return ``text`` rewritten over the canonical alphabet ``{U, I}``.

    >>> normalize("UII UIU")
    'UIIUIU'
    >>> normalize("గలల గలగ")
    'UIIUIU'
    >>> normalize("U|| U|U")          # textbook notation: | is a laghu mark
    'UIIUIU'
    >>> normalize("-uu -u-")
    'UIIUIU'
    """
    out: list[str] = []
    for ch in text:
        if ch in GURU_SPELLINGS:
            out.append(GURU)
        elif ch in LAGHU_SPELLINGS:
            out.append(LAGHU)
        elif ch in SEPARATORS:
            continue
        else:
            raise NotationError(f"unknown scansion symbol {ch!r} in {text!r}")
    return "".join(out)


def normalize_lines(lines: Iterable[str]) -> tuple[str, ...]:
    """Normalise every line of a stanza; empty lines are dropped.

    >>> normalize_lines(["UI U", "", "II I"])
    ('UIU', 'III')
    """
    result = []
    for line in lines:
        s = normalize(line)
        if s:
            result.append(s)
    return tuple(result)


def is_canonical(pattern: str, alphabet: tuple[str, ...] = ALPHABET) -> bool:
    """True when ``pattern`` uses only the symbols of ``alphabet`` (U and I
    by default; pass ``POEM_ALPHABET`` to allow the line separator).

    >>> is_canonical("UIU"), is_canonical("UIX"), is_canonical("UI\\nUI"), is_canonical("UI\\nUI", POEM_ALPHABET)
    (True, False, False, True)
    """
    return all(ch in alphabet for ch in pattern)


def display(text: str) -> str:
    """Render a string over the poem alphabet with a visible line separator.

    >>> display("UII\\nUI")
    'UII⏎UI'
    """
    return text.replace(NEWLINE, NEWLINE_DISPLAY)


def matras(pattern: str) -> int:
    """Matra (mora) count of a canonical pattern: guru 2, laghu 1.

    >>> matras("UII")
    4
    """
    return sum(MATRAS.get(ch, 0) for ch in pattern)


def is_all_laghu(pattern: str) -> bool:
    """True when every symbol is a laghu.

    >>> is_all_laghu("III"), is_all_laghu("IIU")
    (True, False)
    """
    return bool(pattern) and all(ch == LAGHU for ch in pattern)


def flip_final_laghu(pattern: str) -> str:
    """Apply the pādānta rule: a line-final laghu may be read as guru.

    Returns the pattern unchanged when it does not end in a laghu.

    >>> flip_final_laghu("UIUI"), flip_final_laghu("UIUU")
    ('UIUU', 'UIUU')
    """
    if pattern.endswith(LAGHU):
        return pattern[:-1] + GURU
    return pattern


def patterns_with_matras(total: int) -> tuple[str, ...]:
    """Every canonical pattern whose matra count is ``total``, sorted by
    length then lexicographically (so ``UU`` comes before ``IIII``).

    >>> patterns_with_matras(3)
    ('IU', 'UI', 'III')
    """
    found: list[str] = []

    def grow(prefix: str, remaining: int) -> None:
        if remaining == 0:
            found.append(prefix)
            return
        if remaining >= 2:
            grow(prefix + GURU, remaining - 2)
        grow(prefix + LAGHU, remaining - 1)

    if total > 0:
        grow("", total)
    return tuple(sorted(found, key=lambda p: (len(p), p)))


def telugu_notation(pattern: str) -> str:
    """Render a canonical pattern with the Telugu letters గ / ల.

    >>> telugu_notation("UII")
    'గలల'
    """
    return "".join("గ" if ch == GURU else "ల" for ch in pattern)

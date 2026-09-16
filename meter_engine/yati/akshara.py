# -*- coding: utf-8 -*-
"""Akshara features for the yati engine.

An :class:`Akshara` is what the rules look at: the consonant cluster (onset),
the vowel, the marks on the akshara, and two pieces of *context* — whether the
preceding akshara ends in an anusvāra (``pre_bindu``, YATI-MOD-03) and which
dead consonants of the preceding drutam / pollu are fused into the onset
(``pre_dead``, YATI-SY-08 / SY-09).  :func:`parse_akshara` builds it from a
string (with the ``ం`` and ``C్+`` prefixes) or from a scansion ``Syllable``.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Any, Iterable, Optional

from .constants import ANUSVARA, ARDHABINDU, HALANT, NAKAARA_POLLU, VISARGA, _DROP
from .ruleset import Ruleset, _rs


@dataclass
class Akshara:
    text: str
    onset: tuple[str, ...]          # consonants incl. fused pre_dead at the front (ౘ/ౙ folded)
    onset_raw: tuple[str, ...]
    vowel: str                      # independent-vowel letter ('అ' inherent); '' for a bare dead consonant
    bare_vowel: bool
    anusvara: bool
    visarga: bool
    candrabindu: bool
    dead: tuple[str, ...]           # trailing dead consonants (ignored for pairing)
    pre_bindu: bool = False         # the preceding akshara ends in ం
    pre_dead: tuple[str, ...] = ()  # consonants fused from the preceding drutam / pollu (already in onset)

    @property
    def own_onset(self) -> tuple[str, ...]:
        return self.onset[len(self.pre_dead):]

    def describe(self) -> str:
        s = ("ం" if self.pre_bindu else "") + ("".join(c + HALANT for c in self.pre_dead) + "+" if self.pre_dead else "") + self.text
        return s


def _sanitize(text: str) -> str:
    t = unicodedata.normalize("NFC", text)
    t = t.replace(NAKAARA_POLLU, "న" + HALANT)
    t = _DROP.sub("", t)
    return t.strip()


def _parse_string(text: str, rs: Ruleset) -> tuple[list[str], str, bool, bool, bool, bool, list[str]]:
    """-> onset_raw, vowel, bare, anusvara, visarga, candrabindu, trailing_dead"""
    cons = set(rs.consonants) | set(rs.dantya)
    onset: list[str] = []
    dead: list[str] = []
    vowel, bare, anus, vis, cb = "", False, False, False, False
    i, n = 0, len(text)
    while i < n and text[i] in cons:
        onset.append(text[i])
        i += 1
        if i < n and text[i] == HALANT:
            i += 1
            if i < n and text[i] in cons:
                continue
            dead.append(onset.pop())
            break
        break
    if onset:
        vowel = "అ"
    elif i < n and text[i] in rs.vowel_class:
        vowel = text[i]
        bare = True
        i += 1
    while i < n:
        ch = text[i]
        if ch in rs.matras and onset:
            vowel = rs.matras[ch]
            i += 1
        elif ch == ANUSVARA:
            anus = True; i += 1
        elif ch == VISARGA:
            vis = True; i += 1
        elif ch == ARDHABINDU or ch == "ఀ":
            cb = True; i += 1
        elif ch in cons and i + 1 < n and text[i + 1] == HALANT:
            dead.append(ch); i += 2
        else:
            i += 1
    return onset, vowel, bare, anus, vis, cb, dead


def parse_akshara(obj: Any, pre_bindu: bool = False, prev_dead: Optional[Iterable[str]] = None,
                  ruleset: Optional[Ruleset] = None) -> Akshara:
    """Build an :class:`Akshara` from a string (see module docstring for the
    ``ం`` / ``C్+`` prefixes) or from a scansion Syllable-like object."""
    rs = _rs(ruleset)
    prev = tuple(prev_dead or ())
    if isinstance(obj, Akshara):
        return obj
    if isinstance(obj, str):
        t = _sanitize(obj)
        if t.startswith(ANUSVARA):
            pre_bindu = True
            t = t[1:]
        m = re.match(r"^((?:[క-హౘౙ]్)+)\+(.+)$", t)
        if m:
            prev = prev + tuple(ch for ch in m.group(1) if ch != HALANT)
            t = m.group(2)
        had_cb = ARDHABINDU in t
        t = t.replace(ARDHABINDU, "")          # ఁ has no effect on yati (YATI-MOD-01)
        onset_raw, vowel, bare, anus, vis, cb, dead = _parse_string(t, rs)
        cb = cb or had_cb
        text = t
    else:  # Syllable-like
        onset_raw = list(getattr(obj, "onset", ()) or ())
        vowel = getattr(obj, "vowel", "") or ""
        bare = not onset_raw and bool(vowel)
        anus = bool(getattr(obj, "anusvara", False))
        vis = bool(getattr(obj, "visarga", False))
        cb = bool(getattr(obj, "candrabindu", False))
        dead = list(getattr(obj, "dead", ()) or ())
        text = getattr(obj, "text", "") or ""
    full = tuple(prev) + tuple(onset_raw)
    return Akshara(text=text, onset=tuple(rs.norm_c(c) for c in full), onset_raw=full, vowel=vowel,
                   bare_vowel=bare, anusvara=anus, visarga=vis, candrabindu=cb, dead=tuple(dead),
                   pre_bindu=pre_bindu, pre_dead=tuple(prev))

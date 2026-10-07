# -*- coding: utf-8 -*-
"""
Layer B of the v2 constraint: prefer, among the allowed tokens, those that keep the words real.

The meter's mask decides *which* tokens may follow; where the model's own first choice is not among
them, the draw falls to tokens it barely wanted, and those words are 60–67% junk (plan §17). This
module scores each allowed token by what it does to the word being written, against the words of two
aksharas or more in the verse of ``dataset/*.json``:

* a token that ends a word is judged by that word alone: 2 if it is a real word, else 0;
* a token that continues a word: 2 if the word so far begins a real word, 1 if it occurs inside one
  (sandhi fuses words, so a real word often sits inside a longer one), else 0.

Single aksharas do not count as words, and ending a word earns nothing by itself: a first version
scored every finished word and every word begun, and the model then ended a word after almost every
akshara (త మ్మ త్త గ …, single aksharas being "words" of the corpus) — single-akshara words rose from
4% to 37–46% and real words fell (E4B trial, 2026-10-07, ``runs/2026-10-07_e4b_v2_verse_attest2_override``).

:func:`reweight` multiplies each allowed token's probability by ``exp(weight × score)`` and
renormalises. Nothing is removed, so the set of allowed tokens — and with it the guarantee that every
poem finishes in meter — is exactly what it was.

"Occurs inside a real word" is answered by a suffix automaton (Blumer et al.'s DAWG — the structure of
arXiv 2307.01428) over the characters of the corpus words, words kept apart by a separator.

Owns: :class:`Attestation`, :func:`load_attestation`, :func:`reweight`. Must not import torch.
"""
from __future__ import annotations

import math
from functools import lru_cache
from typing import Iterable, Sequence

SEPARATOR = "\x00"
BOUNDARY = frozenset(" \n")


class Attestation:
    """The words of two aksharas or more of a corpus, their prefixes, and every factor of them
    (suffix automaton).

    >>> a = Attestation(["తల్లి", "ప్రేమ", "ప్రేరణ", "త"])
    >>> a.partial("ప్రే"), a.partial("రణ"), a.partial("ల్రు")       # begins a word / inside one / neither
    (2, 1, 0)
    >>> a.finished("ప్రేమ"), a.finished("ప్రే"), a.finished("త")    # a real word / not one / a single akshara
    (2, 0, 0)
    >>> a.score("ప్రే", "మ"), a.score("ప్రే", "ల్ర"), a.score("ప్రేమ", " త"), a.score("త", " ")
    (2, 0, 2, 0)
    """

    def __init__(self, words: Iterable[str]):
        from .inventory import units
        self.words = frozenset(w for w in words if w and len(units(w)) >= 2)
        self.prefixes = frozenset(w[:i] for w in self.words for i in range(1, len(w) + 1))
        self._next: list[dict[str, int]] = [{}]
        self._link: list[int] = [-1]
        self._len: list[int] = [0]
        self._last = 0
        for w in sorted(self.words):
            for ch in w:
                self._add(ch)
            self._add(SEPARATOR)

    def _add(self, c: str) -> None:
        nxt, link, ln = self._next, self._link, self._len
        cur = len(ln)
        nxt.append({})
        link.append(0)
        ln.append(ln[self._last] + 1)
        p = self._last
        while p != -1 and c not in nxt[p]:
            nxt[p][c] = cur
            p = link[p]
        if p != -1:
            q = nxt[p][c]
            if ln[p] + 1 == ln[q]:
                link[cur] = q
            else:
                clone = len(ln)
                nxt.append(dict(nxt[q]))
                link.append(link[q])
                ln.append(ln[p] + 1)
                while p != -1 and nxt[p].get(c) == q:
                    nxt[p][c] = clone
                    p = link[p]
                link[q] = link[cur] = clone
        self._last = cur

    def inside(self, s: str) -> bool:
        """``s`` occurs inside some corpus word."""
        v = 0
        for ch in s:
            v = self._next[v].get(ch)
            if v is None:
                return False
        return True

    def partial(self, word: str) -> int:
        """2: begins a corpus word; 1: occurs inside one; 0: neither."""
        return 2 if word in self.prefixes else 1 if self.inside(word) else 0

    def finished(self, word: str) -> int:
        """2: a corpus word (of two aksharas or more); 0: not."""
        return 2 if word in self.words else 0

    def score(self, word: str, text: str) -> int:
        """The score of writing ``text`` after the unfinished ``word`` (the text since the last boundary):
        a token that ends a word is judged by that word alone; one that continues it, by the word so far."""
        cur = word
        for ch in text:
            if ch in BOUNDARY:
                return self.finished(cur) if cur else 0
            cur += ch
        return self.partial(cur)


@lru_cache(maxsize=None)
def load_attestation(corpus: str = "all") -> Attestation:
    """Built once per process from the verse of ``dataset/*.json``: ``all`` of it
    (``analysis.corpus_lexicon``), or ``train90`` — the words of 90% of the poems only, for checking the
    preference against words it has never seen (the split of :func:`verse_split`)."""
    if corpus == "all":
        from .analysis import corpus_lexicon
        return Attestation(corpus_lexicon())
    if corpus == "train90":
        from .analysis import _telugu_words
        train, _ = verse_split()
        return Attestation({w for p in train for ln in p for w in _telugu_words(ln)})
    raise ValueError(f"unknown attestation corpus {corpus!r}: all | train90")


def verse_split(held: float = 0.1, seed: int = 0) -> tuple[list[list[str]], list[list[str]]]:
    """(train, held-out) poems of ``dataset/*.json``: the files in name order, their poems with verse in
    file order, shuffled with ``random.Random(seed)``; the first ``held`` share is held out (the split of
    ``experiments/scripts/measure_absent_words.py``)."""
    import json
    import random
    import unicodedata
    from .analysis import DATASET
    poems = []
    for path in sorted(DATASET.glob("*.json")):
        for rec in json.loads(path.read_text(encoding="utf-8")):
            verse = [unicodedata.normalize("NFC", ln) for ln in rec.get("verse") or [] if ln.strip()]
            if verse:
                poems.append(verse)
    order = list(range(len(poems)))
    random.Random(seed).shuffle(order)
    cut = int(len(poems) * held)
    return [poems[i] for i in order[cut:]], [poems[i] for i in order[:cut]]


def reweight(probs: dict[int, float], word: str, texts: Sequence[str], weight: float,
             att: Attestation) -> tuple[dict[int, float], dict[int, int]]:
    """``probs`` (slice position → probability of an allowed token) × exp(weight × score),
    renormalised; also the scores.

    >>> a = Attestation(["ప్రేమ"])
    >>> p, s = reweight({0: 0.6, 1: 0.4}, "ప్రే", ["ల్ర", "మ"], 2.0, a)
    >>> s, round(p[1], 3)
    ({0: 0, 1: 2}, 0.973)
    """
    scores = {i: att.score(word, texts[i]) for i in probs}
    w = {i: p * math.exp(weight * scores[i]) for i, p in probs.items()}
    tot = sum(w.values())
    return {i: x / tot for i, x in w.items()}, scores

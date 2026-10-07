# -*- coding: utf-8 -*-
"""
The aksharas a generated poem may use: an inventory of attested syllables.

Under the constraint the models invent aksharas real Telugu never writes (ల్రు, న్యె, వ్రి …): in the
grids of 2026-09 they were in 21–30% of the constrained words, against 0.3% of held-out real verse
and ≤ 1.1% of the models' free text (plan §17, ``experiments/runs/2026-10-05_absent_words``). An
inventory closes that door: every syllable the poem writes, as the scanner cuts it (onset cluster,
vowel, marks and a merged word-final pollu: ``రా``, ``త్య``, ``కన్``), must be one of a fixed set.

Two inventories:

* ``verse`` — every syllable of the verse in ``dataset/*.json`` (15,415 poems; 3,879 syllables), stored
  in ``inventories/verse.txt`` (``python -m metrical_decoder inventory`` rebuilds it);
* ``tokenizer`` — the atomic syllables of the syllable-aware Telugu tokenizer
  (``diffusion_pretraining/tokenizer/telugu_alldomain.tokenizer.json``, 44,835): the aksharas of modern
  all-domain Telugu. Its segmentation agrees with the scanner's on 99.998% of the corpus's words.

Only syllables the orthography filter can write — and end a word with — are kept: the tokenizer's
list has transliterations such as చంద్ర్ (two dead consonants) and malformed ones such as చంం, which
the filter never lets through; counted as completions they promised continuations that do not exist
(random-logit control, కందము: a dead end).

With a model, only syllables its vocabulary can write are kept (``alphabet``: the characters that are
tokens of their own): Gemma has no token for ఁ, so where మ్రేఁ was a verse syllable's only attested
completion (మ్రే alone is not attested) the decoder was promised a form it could not write (random-logit
control, శాలిని and స్రగ్ధర: three dead ends).

The enforcer uses an inventory both as a filter (no syllable outside it is ever finished) and in
its liveness test: where a pending syllable could still become guru or laghu, or a yati or prāsa
partner, only its attested completions count (``registers.continuations``). A completion counts as
guru only by its own rules (long vowel, diphthong, ం, ః, pollu), never by a conjunct that might
follow — a stricter test than the free one, so that it cannot promise a completion that is not there.

Owns: :class:`Inventory`, :func:`load_inventory`. Must not import torch.
"""
from __future__ import annotations

import json
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Optional

from .incremental import ENGINE_DIR, sc

HERE = Path(__file__).resolve().parent
VERSE_FILE = HERE / "inventories" / "verse.txt"
TOKENIZER_FILE = ENGINE_DIR.parent / "diffusion_pretraining" / "tokenizer" / "telugu_alldomain.tokenizer.json"
NAMES = ("verse", "tokenizer")


@lru_cache(maxsize=200_000)
def units(word: str) -> tuple[str, ...]:
    """The word's syllables as the scanner cuts them (the units of an inventory).

    >>> units("సత్యము"), units("వచ్చెన్")
    (('స', 'త్య', 'ము'), ('వ', 'చ్చెన్'))
    """
    return tuple(s.text for s in sc.syllabify(unicodedata.normalize("NFC", word)))


def _writable(unit: str) -> bool:
    """The orthography filter can write ``unit`` as one syllable and end a word with it."""
    from . import orthography as ortho
    state = ortho.feed(ortho.START, unit)
    return state is not None and ortho.can_end(state) and _info(unit) is not None


@lru_cache(maxsize=None)
def _info(unit: str):
    syls = sc.syllabify(unit)
    return syls[0] if len(syls) == 1 else None


class Inventory:
    """A set of syllables with the lookups the liveness test needs.

    >>> inv = Inventory(["క", "కా", "కన్", "క్ష", "రా"], "toy")
    >>> "కా" in inv, "కీ" in inv
    (True, False)
    >>> sorted(inv.with_onset(("క",))), sorted(inv.growing(("క",)))
    (['క', 'కన్', 'కా'], ['క్ష'])
    >>> inv.weights(inv.with_onset(("క",))), inv.weights(["క్ష"])
    (('I', 'U'), ('I',))
    """

    def __init__(self, syllables: Iterable[str], name: str, alphabet: Optional[frozenset] = None):
        self.name = name
        self.alphabet = alphabet
        self.units = frozenset(u for u in (unicodedata.normalize("NFC", x) for x in syllables if x and x.strip())
                               if _writable(u) and (alphabet is None or set(u) <= alphabet))
        onset: dict[tuple[str, ...], set[str]] = {}
        for u in self.units:
            s = _info(u)
            if s is not None:
                onset.setdefault(tuple(s.onset), set()).add(u)
        # one frozenset object per key, reused: the decoder's caches then compare them by identity
        self._onset: dict[tuple[str, ...], frozenset] = {k: frozenset(v) for k, v in onset.items()}
        self._grow_cache: dict[tuple[str, ...], frozenset] = {}
        self._ext_cache: dict[str, frozenset] = {}

    def __contains__(self, unit: str) -> bool:
        return unit in self.units

    def __len__(self) -> int:
        return len(self.units)

    def __repr__(self) -> str:
        return f"Inventory({self.name!r}, {len(self.units)} syllables)"

    def __reduce__(self):                       # worker processes reload it by name
        if self.name in NAMES:                  # the same call as the original, so the same cached object
            return (load_inventory, (self.name,) if self.alphabet is None else (self.name, self.alphabet))
        return (Inventory, (sorted(self.units), self.name, self.alphabet))

    def with_onset(self, onset: tuple[str, ...]) -> frozenset[str]:
        """The syllables whose consonant cluster is exactly ``onset`` (() for a vowel-initial one)."""
        return self._onset.get(tuple(onset), frozenset())

    def extending(self, text: str, onset: tuple[str, ...]) -> frozenset[str]:
        """The syllables with cluster ``onset`` that begin with ``text`` (a written syllable that may
        still take a mark or a word-final pollu)."""
        got = self._ext_cache.get(text)
        if got is None:
            got = self._ext_cache[text] = frozenset(u for u in self.with_onset(onset) if u.startswith(text))
        return got

    def growing(self, onset: tuple[str, ...]) -> frozenset[str]:
        """The syllables whose cluster begins with ``onset`` and is longer (the cluster still grows)."""
        onset = tuple(onset)
        got = self._grow_cache.get(onset)
        if got is None:
            n = len(onset)
            got = self._grow_cache[onset] = frozenset(
                u for o, us in self._onset.items() if len(o) > n and o[:n] == onset for u in us)
        return got

    def conjuncts(self) -> frozenset[str]:
        """The syllables that open with a conjunct."""
        got = self._grow_cache.get(None)
        if got is None:
            got = self._grow_cache[None] = frozenset(u for o, us in self._onset.items() if len(o) >= 2 for u in us)
        return got

    def all_known(self, word: str) -> bool:
        """Every syllable of ``word`` is in the inventory."""
        return all(u in self.units for u in units(word))

    @staticmethod
    def guru(unit: str) -> bool:
        """Guru by its own rules (long vowel, diphthong, ం, ః, pollu)."""
        s = _info(unit)
        return bool(s is not None and sc.self_rules(s))

    @classmethod
    def weights(cls, options: Iterable[str]) -> tuple[str, ...]:
        """The weights the syllables in ``options`` can take: I when one is light by its own rules,
        U when one is guru by them."""
        out = set()
        for u in options:
            out.add("U" if cls.guru(u) else "I")
            if len(out) == 2:
                break
        return tuple(sorted(out))


def build_verse_inventory(dataset_dir: Optional[Path] = None) -> list[str]:
    """Every syllable of the verse in ``dataset/*.json``, sorted."""
    from .analysis import _telugu_words
    dataset_dir = dataset_dir or ENGINE_DIR.parent / "dataset"
    found: set[str] = set()
    for path in sorted(dataset_dir.glob("*.json")):
        for rec in json.loads(path.read_text(encoding="utf-8")):
            for ln in rec.get("verse") or []:
                for w in _telugu_words(unicodedata.normalize("NFC", ln)):
                    found.update(units(w))
    return sorted(found)


@lru_cache(maxsize=None)
def load_inventory(name: str, alphabet: Optional[frozenset] = None) -> Inventory:
    """``verse`` (from ``inventories/verse.txt``) or ``tokenizer``; with ``alphabet``, only the
    syllables written entirely in it (a model's single-character tokens)."""
    if name == "verse":
        return Inventory(VERSE_FILE.read_text(encoding="utf-8").split("\n"), "verse", alphabet)
    if name == "tokenizer":
        return Inventory(json.loads(TOKENIZER_FILE.read_text(encoding="utf-8"))["atomic_aksharas"], "tokenizer", alphabet)
    raise ValueError(f"unknown inventory {name!r}; choose from {', '.join(NAMES)}")

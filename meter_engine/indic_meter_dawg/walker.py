# -*- coding: utf-8 -*-
"""
Run one line through the DAWG.

Owns: acceptance labels, the pādānta (line-final laghu read as guru)
variant, per-hypothesis death points, and viable-prefix queries. Must not
know about stanzas.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from . import automaton as au
from . import symbols
from .builder import Hypothesis, LineDawg, default_dawg


Options = tuple[str, ...]      # one entry per akshara: 'U', 'I', 'UI' (canonical U, alt I) or 'IU'


def as_options(line) -> Options:
    """Normalise a line given as a U/I string or as per-akshara options.

    >>> as_options("UII"), as_options(["U", "IU", "I"])
    (('U', 'I', 'I'), ('U', 'IU', 'I'))
    """
    if isinstance(line, str):
        return tuple(symbols.normalize(line))
    out = []
    for opt in line:
        o = symbols.normalize(opt)
        if o not in ("U", "I", "UI", "IU"):
            raise symbols.NotationError(f"akshara option must be U, I, UI or IU, not {opt!r}")
        out.append(o)
    return tuple(out)


def canonical(options: Options) -> str:
    """The first choice at every position."""
    return "".join(o[0] for o in options)


@dataclass(frozen=True)
class WalkResult:
    line: str                                   # canonical line as walked
    accepted: frozenset                          # hypotheses accepting the line as given
    padanta_accepted: frozenset                  # hypotheses accepting only with the final laghu read as guru
    died: dict                                   # hypothesis -> death index (see automaton.death_index)
    witness: dict = None                         # hypothesis -> the concrete pattern that was accepted
    options: Options = ()                        # the per-akshara options walked (empty = plain string)

    def pattern_for(self, h: Hypothesis) -> str:
        """The accepted pattern for a hypothesis (the line itself for a plain walk)."""
        if self.witness and h in self.witness:
            return self.witness[h]
        return self.line

    @property
    def all_accepted(self) -> frozenset:
        return self.accepted | self.padanta_accepted

    def needs_padanta(self, h: Hypothesis) -> bool:
        return h in self.padanta_accepted and h not in self.accepted

    @property
    def meters(self) -> frozenset:
        return frozenset(m for m, _ in self.all_accepted)


def walk(line: str, dawg: Optional[LineDawg] = None, final_laghu_as_guru: bool = True,
         with_death_points: bool = True) -> WalkResult:
    """Accept labels for one line.

    >>> r = walk("UUUUUUUU")
    >>> sorted(m for m, s in r.accepted)
    ['madhuragati_ragada', 'vidyunmala']
    >>> walk("UUUUUUUI").needs_padanta(("vidyunmala", "all"))
    True
    """
    dawg = dawg or default_dawg()
    s = symbols.normalize(line)
    accepted = au.labels_of(dawg.dfa, s)
    padanta: frozenset = frozenset()
    if final_laghu_as_guru and s.endswith(symbols.LAGHU):
        flipped = symbols.flip_final_laghu(s)
        padanta = au.labels_of(dawg.dfa, flipped) - accepted
    died: dict = {}
    if with_death_points:
        for h, d in dawg.slot_dfas.items():
            if h in accepted or h in padanta:
                continue
            idx = au.death_index(d, s)
            if idx is not None:
                died[h] = idx
    return WalkResult(line=s, accepted=accepted, padanta_accepted=padanta, died=died,
                      witness={h: s for h in accepted} | {h: symbols.flip_final_laghu(s) for h in padanta},
                      options=tuple(s))


def _lattice(dawg: LineDawg, options: Options) -> dict[int, str]:
    """Simulate the DFA over the lattice: reachable state -> first witness pattern."""
    frontier: dict[int, str] = {dawg.dfa.start: ""}
    for opt in options:
        nxt: dict[int, str] = {}
        for state, path in frontier.items():
            for sym in opt:
                d = dawg.dfa.step(state, sym)
                if d is not None and d not in nxt:
                    nxt[d] = path + sym
        frontier = nxt
        if not frontier:
            break
    return frontier


def walk_options(options, dawg: Optional[LineDawg] = None, final_laghu_as_guru: bool = True) -> WalkResult:
    """Walk a line whose aksharas may each be read two ways. ``accepted``
    holds every hypothesis some choice of readings satisfies; ``witness``
    gives one such pattern per hypothesis (choices taken in the order given,
    so the canonical reading wins ties).

    >>> r = walk_options(["U", "UI", "U", "U", "U", "U", "U", "U"])
    >>> sorted(m for m, _ in r.accepted), r.witness[("vidyunmala", "all")]
    (['madhuragati_ragada', 'vidyunmala'], 'UUUUUUUU')
    >>> sorted(m for m, _ in walk_options(["IU", "I", "I", "I", "U", "I", "U", "I", "I"]).accepted)
    ['kandamu']
    """
    dawg = dawg or default_dawg()
    opts = as_options(options)
    if not opts:
        return WalkResult(line="", accepted=frozenset(), padanta_accepted=frozenset(), died={}, witness={}, options=())
    final = _lattice(dawg, opts)
    accepted: dict = {}
    for state, path in final.items():
        for h in dawg.dfa.labels.get(state, frozenset()):
            accepted.setdefault(h, path)
    padanta: dict = {}
    last = opts[-1]
    if final_laghu_as_guru and "I" in last and "U" not in last:
        final2 = _lattice(dawg, opts[:-1] + ("U",))
        for state, path in final2.items():
            for h in dawg.dfa.labels.get(state, frozenset()):
                if h not in accepted:
                    padanta.setdefault(h, path)
    return WalkResult(line=canonical(opts), accepted=frozenset(accepted), padanta_accepted=frozenset(padanta),
                      died={}, witness={**accepted, **padanta}, options=opts)


def viable_prefix(prefix: str, dawg: Optional[LineDawg] = None) -> frozenset:
    """Hypotheses that can still complete after reading ``prefix`` (empty
    frozenset when no meter can). This is the generation-time query.

    >>> sorted(m for m, s in viable_prefix("UUUUUUUII"))
    ['madhuragati_ragada']
    >>> viable_prefix("I" * 37)
    frozenset()
    """
    dawg = dawg or default_dawg()
    s = au.run(dawg.dfa, symbols.normalize(prefix))
    if s is None:
        return frozenset()
    return dawg.reachable.get(s, frozenset())


def next_symbols(prefix: str, dawg: Optional[LineDawg] = None) -> dict[str, frozenset]:
    """Which symbol may come next and which hypotheses survive each choice.

    >>> {k: sorted(m for m, _ in v) for k, v in next_symbols("UUUUUUUI").items()}
    {'I': ['madhuragati_ragada']}
    """
    dawg = dawg or default_dawg()
    s = au.run(dawg.dfa, symbols.normalize(prefix))
    if s is None:
        return {}
    out = {}
    for a in symbols.ALPHABET:
        d = dawg.dfa.step(s, a)
        if d is not None and dawg.reachable.get(d):
            out[a] = dawg.reachable[d]
    return out

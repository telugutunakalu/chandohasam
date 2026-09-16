# -*- coding: utf-8 -*-
"""
Compile the catalogue into the line-level DAWG.

Pipeline: MeterSpec → gana-level grammar → strict grammar → NFA (per slot)
→ union → labeled DFA → minimized. Also keeps one small unlabeled minimized
DFA per (meter, slot) for death-point diagnostics and diagrams.

Owns: the :class:`LineDawg` bundle and the cached default instance.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from . import automaton as au
from .catalogue import Catalogue, MeterSpec, load_catalogue
from .ganas import GanaRegistry, load_registry
from .grammar import Grammar, all_grammars, to_strict

Hypothesis = tuple[str, str]     # (meter name, slot name)


@dataclass(frozen=True)
class LineDawg:
    catalogue: Catalogue
    registry: GanaRegistry
    grammars: dict[Hypothesis, Grammar]            # gana-level
    strict_grammars: dict[Hypothesis, Grammar]
    nfa: au.Nfa                                    # union of all slots
    dfa: au.Dfa                                    # labeled, minimized: the identification automaton
    slot_dfas: dict[Hypothesis, au.Dfa]            # per (meter, slot), unlabeled, minimized
    reachable: dict[int, frozenset]                # dfa state -> hypotheses that can still complete
    unminimized_states: int

    @property
    def hypotheses(self) -> tuple[Hypothesis, ...]:
        return tuple(self.grammars)

    def spec(self, meter: str) -> MeterSpec:
        return self.catalogue.get(meter)

    @property
    def n_states(self) -> int:
        return self.dfa.n_states

    def stats(self) -> dict:
        """Headline numbers (states, edges, language size, ambiguity)."""
        total = au.count_paths(self.dfa) if au.is_acyclic(self.dfa) else None
        return {
            "meters": len(self.catalogue.concrete),
            "hypotheses": len(self.grammars),
            "nfa_states": self.nfa.n_states,
            "dfa_states_unminimized": self.unminimized_states,
            "dfa_states": self.dfa.n_states,
            "dfa_edges": self.dfa.n_edges,
            "distinct_lines": total,
            "acyclic": au.is_acyclic(self.dfa),
            "max_line_length": au.max_depth(self.dfa) if au.is_acyclic(self.dfa) else None,
        }


def build_line_dawg(catalogue: Optional[Catalogue] = None, registry: Optional[GanaRegistry] = None,
                    minimize: bool = True) -> LineDawg:
    """Build the DAWG for every concrete meter of the catalogue.

    >>> d = build_line_dawg()
    >>> ("utpalamala", "all") in d.hypotheses, d.dfa.n_states > 0
    (True, True)
    """
    catalogue = catalogue or load_catalogue()
    registry = registry or load_registry()
    grammars = all_grammars(catalogue.concrete, registry)
    strict = {h: to_strict(g) for h, g in grammars.items()}
    nfas = {h: au.nfa_from_strict_grammar(g, h) for h, g in strict.items()}
    big = au.union(nfas.values())
    dfa = au.determinize(big)
    unmin = dfa.n_states
    if minimize:
        dfa = au.minimize(dfa, keep_labels=True)
    slot_dfas = {}
    for h, n in nfas.items():
        d = au.determinize(n)
        slot_dfas[h] = au.minimize(d, keep_labels=False) if minimize else d
    reach = au.coreachable_labels(dfa)
    return LineDawg(catalogue=catalogue, registry=registry, grammars=grammars, strict_grammars=strict,
                    nfa=big, dfa=dfa, slot_dfas=slot_dfas, reachable=reach, unminimized_states=unmin)


@lru_cache(maxsize=1)
def default_dawg() -> LineDawg:
    """The DAWG of the default catalogue, built once per process."""
    return build_line_dawg()

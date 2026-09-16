# -*- coding: utf-8 -*-
"""
Finite automata over {U, I}: NFA from a strict right-linear grammar, union,
subset construction, Moore minimization, language enumeration and counting.

Owns: the generic automaton algebra. Must not know what a meter is; labels
are opaque hashable objects (the builder uses ``(meter, slot)`` tuples).

Weights: every edge carries the matra weight of its symbol (guru 2, laghu 1),
so a path's weight is the line's matra count. This is the "weighted" in the
weighted DAWG; later phases add mismatch costs on top of the same field.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Hashable, Iterable, Iterator, Optional

from .grammar import Grammar
from . import symbols

Label = Hashable


@dataclass(frozen=True)
class Edge:
    src: int
    symbol: str
    dst: int
    weight: int


@dataclass(frozen=True)
class NfaStateInfo:
    """What an NFA state means, for explanations and diagrams."""
    nonterminal: str
    label: Label


@dataclass
class Nfa:
    n_states: int = 0
    start: set[int] = field(default_factory=set)
    edges: list[Edge] = field(default_factory=list)
    accept: dict[int, Label] = field(default_factory=dict)      # accepting state -> label
    info: dict[int, NfaStateInfo] = field(default_factory=dict)

    def transitions(self) -> dict[int, dict[str, set[int]]]:
        t: dict[int, dict[str, set[int]]] = {}
        for e in self.edges:
            t.setdefault(e.src, {}).setdefault(e.symbol, set()).add(e.dst)
        return t


@dataclass
class Dfa:
    """Deterministic automaton. ``labels[s]`` is the (possibly empty) set of
    labels accepted at ``s``; a state is accepting iff its label set is
    non-empty (or, for unlabeled acceptors, iff it is in ``accepting``)."""
    start: int
    transitions: dict[int, dict[str, int]]
    labels: dict[int, frozenset]
    n_states: int
    state_sets: Optional[dict[int, frozenset[int]]] = None    # DFA state -> NFA states (pre-minimization)
    alphabet: tuple[str, ...] = symbols.ALPHABET

    def is_accepting(self, state: int) -> bool:
        return bool(self.labels.get(state))

    def step(self, state: int, symbol: str) -> Optional[int]:
        return self.transitions.get(state, {}).get(symbol)

    def edges(self) -> Iterator[Edge]:
        for s, row in self.transitions.items():
            for sym, d in row.items():
                yield Edge(s, sym, d, symbols.MATRAS.get(sym, 0))

    @property
    def n_edges(self) -> int:
        return sum(len(r) for r in self.transitions.values())


# --------------------------------------------------------------------------
# grammar -> NFA
# --------------------------------------------------------------------------
def nfa_from_strict_grammar(grammar: Grammar, label: Label) -> Nfa:
    """Nonterminal = state; ``A → aB`` = edge; ``A → a`` = edge into a fresh
    accepting state carrying ``label``.

    >>> from .catalogue import load_catalogue; from .ganas import load_registry
    >>> from .grammar import gana_level_grammar, to_strict
    >>> g = to_strict(gana_level_grammar(load_catalogue().get("vidyunmala"), "all", load_registry()))
    >>> n = nfa_from_strict_grammar(g, ("vidyunmala", "all")); n.n_states, len(n.edges)
    (9, 8)
    """
    if grammar.form != "strict":
        raise ValueError("nfa_from_strict_grammar needs the strict form; call to_strict first")
    ids = {nt: i for i, nt in enumerate(grammar.nonterminals)}
    nfa = Nfa(n_states=len(ids) + 1)
    final = len(ids)
    nfa.start = {ids[grammar.start]}
    nfa.accept[final] = label
    nfa.info[final] = NfaStateInfo("ACCEPT", label)
    for nt, i in ids.items():
        nfa.info[i] = NfaStateInfo(nt, label)
    for p in grammar.productions:
        if len(p.terminals) != 1:
            raise ValueError(f"production {p.format()} is not strict")
        dst = ids[p.rhs] if p.rhs is not None else final
        nfa.edges.append(Edge(ids[p.lhs], p.terminals, dst, symbols.MATRAS.get(p.terminals, 0)))
    return nfa


def union(nfas: Iterable[Nfa]) -> Nfa:
    """Disjoint union: states renumbered, all start states kept (an NFA may
    have several)."""
    out = Nfa()
    for n in nfas:
        off = out.n_states
        out.n_states += n.n_states
        out.start |= {s + off for s in n.start}
        out.edges.extend(Edge(e.src + off, e.symbol, e.dst + off, e.weight) for e in n.edges)
        out.accept.update({s + off: lab for s, lab in n.accept.items()})
        out.info.update({s + off: inf for s, inf in n.info.items()})
    return out


# --------------------------------------------------------------------------
# NFA -> DFA
# --------------------------------------------------------------------------
def determinize(nfa: Nfa, alphabet: tuple[str, ...] = symbols.ALPHABET) -> Dfa:
    """Subset construction (no epsilon edges exist in our NFAs).

    >>> from .catalogue import load_catalogue; from .ganas import load_registry
    >>> from .grammar import gana_level_grammar, to_strict
    >>> g = to_strict(gana_level_grammar(load_catalogue().get("tetagiti"), "all", load_registry()))
    >>> d = determinize(nfa_from_strict_grammar(g, "t")); count_paths(d)
    288
    """
    trans = nfa.transitions()
    start = frozenset(nfa.start)
    ids: dict[frozenset[int], int] = {start: 0}
    order: list[frozenset[int]] = [start]
    dtrans: dict[int, dict[str, int]] = {}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        row: dict[str, int] = {}
        for sym in alphabet:
            nxt: set[int] = set()
            for s in cur:
                nxt |= trans.get(s, {}).get(sym, set())
            if not nxt:
                continue
            key = frozenset(nxt)
            if key not in ids:
                ids[key] = len(order)
                order.append(key)
                queue.append(key)
            row[sym] = ids[key]
        dtrans[ids[cur]] = row
    labels = {ids[st]: frozenset(nfa.accept[s] for s in st if s in nfa.accept) for st in order}
    return Dfa(start=0, transitions=dtrans, labels=labels, n_states=len(order),
               state_sets={ids[st]: st for st in order}, alphabet=alphabet)


# --------------------------------------------------------------------------
# minimization (Moore partition refinement; works on cyclic DFAs too)
# --------------------------------------------------------------------------
def minimize(dfa: Dfa, keep_labels: bool = True) -> Dfa:
    """Merge indistinguishable states. With ``keep_labels`` the accept
    label *sets* must agree for two states to merge (identification DFA);
    without, only accepting/non-accepting matters (plain acceptor).

    >>> from .catalogue import load_catalogue; from .ganas import load_registry
    >>> from .grammar import gana_level_grammar, to_strict
    >>> g = to_strict(gana_level_grammar(load_catalogue().get("seesamu"), "all", load_registry()))
    >>> d = determinize(nfa_from_strict_grammar(g, "s")); m = minimize(d)
    >>> d.n_states > m.n_states and count_paths(d) == count_paths(m)
    True
    """
    dfa = trim(dfa)
    alphabet = dfa.alphabet
    states = list(range(dfa.n_states))
    if keep_labels:
        block = {s: dfa.labels.get(s, frozenset()) for s in states}
    else:
        block = {s: bool(dfa.labels.get(s)) for s in states}
    # map block keys to small ints
    keys = {k: i for i, k in enumerate(sorted(set(block.values()), key=repr))}
    part = {s: keys[block[s]] for s in states}
    while True:
        sig = {s: (part[s], tuple(part.get(dfa.step(s, a), -1) for a in alphabet)) for s in states}
        new_keys = {k: i for i, k in enumerate(sorted(set(sig.values())))}
        new_part = {s: new_keys[sig[s]] for s in states}
        if len(new_keys) == len(set(part.values())):
            part = new_part
            break
        part = new_part
    # renumber so that the start block is 0 and numbering follows BFS order
    rep: dict[int, int] = {}
    order: list[int] = []
    queue = deque([dfa.start])
    rep[part[dfa.start]] = 0
    order.append(part[dfa.start])
    while queue:
        s = queue.popleft()
        for a in alphabet:
            d = dfa.step(s, a)
            if d is None:
                continue
            b = part[d]
            if b not in rep:
                rep[b] = len(order)
                order.append(b)
                queue.append(d)
    trans: dict[int, dict[str, int]] = {}
    labels: dict[int, frozenset] = {}
    for s in states:
        b = rep[part[s]]
        row = trans.setdefault(b, {})
        for a in alphabet:
            d = dfa.step(s, a)
            if d is not None:
                row[a] = rep[part[d]]
        labels[b] = dfa.labels.get(s, frozenset()) if keep_labels else \
            (frozenset({True}) if dfa.labels.get(s) else frozenset())
    return Dfa(start=0, transitions=trans, labels=labels, n_states=len(order), alphabet=alphabet)


def trim(dfa: Dfa) -> Dfa:
    """Drop states that cannot reach an accepting state (or are unreachable)."""
    reach = _reachable(dfa)
    rev: dict[int, set[int]] = {}
    for s in reach:
        for a, d in dfa.transitions.get(s, {}).items():
            rev.setdefault(d, set()).add(s)
    live: set[int] = {s for s in reach if dfa.labels.get(s)}
    queue = deque(live)
    while queue:
        s = queue.popleft()
        for p in rev.get(s, ()):
            if p not in live:
                live.add(p)
                queue.append(p)
    if dfa.start not in live:
        return Dfa(start=0, transitions={0: {}}, labels={0: frozenset()}, n_states=1, alphabet=dfa.alphabet)
    keep = sorted(live)
    new = {s: i for i, s in enumerate(keep)}
    trans = {new[s]: {a: new[d] for a, d in dfa.transitions.get(s, {}).items() if d in live} for s in keep}
    labels = {new[s]: dfa.labels.get(s, frozenset()) for s in keep}
    sets = {new[s]: dfa.state_sets[s] for s in keep} if dfa.state_sets else None
    return Dfa(start=new[dfa.start], transitions=trans, labels=labels, n_states=len(keep), state_sets=sets,
               alphabet=dfa.alphabet)


def _reachable(dfa: Dfa) -> set[int]:
    seen = {dfa.start}
    queue = deque([dfa.start])
    while queue:
        s = queue.popleft()
        for d in dfa.transitions.get(s, {}).values():
            if d not in seen:
                seen.add(d)
                queue.append(d)
    return seen


# --------------------------------------------------------------------------
# queries
# --------------------------------------------------------------------------
def run(dfa: Dfa, string: str) -> Optional[int]:
    """Final state after reading ``string``, or None if the walk died."""
    s: Optional[int] = dfa.start
    for ch in string:
        s = dfa.step(s, ch)
        if s is None:
            return None
    return s


def accepts(dfa: Dfa, string: str) -> bool:
    s = run(dfa, string)
    return s is not None and dfa.is_accepting(s)


def labels_of(dfa: Dfa, string: str) -> frozenset:
    """Accept labels of ``string`` (empty when rejected)."""
    s = run(dfa, string)
    return dfa.labels.get(s, frozenset()) if s is not None else frozenset()


def death_index(dfa: Dfa, string: str) -> Optional[int]:
    """0-based index of the symbol on which the walk dies; ``len(string)``
    when the whole string is read but the state is not accepting; None when
    accepted."""
    s: Optional[int] = dfa.start
    for i, ch in enumerate(string):
        s = dfa.step(s, ch)
        if s is None:
            return i
    return None if dfa.is_accepting(s) else len(string)


def is_acyclic(dfa: Dfa) -> bool:
    color: dict[int, int] = {}

    def visit(s: int) -> bool:
        color[s] = 1
        for d in dfa.transitions.get(s, {}).values():
            c = color.get(d, 0)
            if c == 1 or (c == 0 and not visit(d)):
                return False
        color[s] = 2
        return True

    return visit(dfa.start)


def topological_order(dfa: Dfa) -> list[int]:
    order: list[int] = []
    seen: set[int] = set()

    def visit(s: int) -> None:
        seen.add(s)
        for d in dfa.transitions.get(s, {}).values():
            if d not in seen:
                visit(d)
        order.append(s)

    visit(dfa.start)
    return order[::-1]


def count_paths(dfa: Dfa) -> int:
    """Number of accepted strings (acyclic DFA only)."""
    if not is_acyclic(dfa):
        raise ValueError("count_paths needs an acyclic DFA")
    ways = {dfa.start: 1}
    total = 0
    for s in topological_order(dfa):
        w = ways.get(s, 0)
        if dfa.is_accepting(s):
            total += w
        for d in dfa.transitions.get(s, {}).values():
            ways[d] = ways.get(d, 0) + w
    return total


def enumerate_language(dfa: Dfa, max_len: int = 64) -> Iterator[tuple[str, frozenset]]:
    """Yield ``(string, labels)`` for every accepted string up to ``max_len``."""
    stack: list[tuple[int, str]] = [(dfa.start, "")]
    while stack:
        s, prefix = stack.pop()
        if dfa.is_accepting(s):
            yield prefix, dfa.labels[s]
        if len(prefix) >= max_len:
            continue
        for a in reversed(dfa.alphabet):
            d = dfa.step(s, a)
            if d is not None:
                stack.append((d, prefix + a))


def coreachable_labels(dfa: Dfa) -> dict[int, frozenset]:
    """For every state, the union of labels of accepting states reachable
    from it (fixpoint; works with cycles). This is the per-state "which
    meters can still complete" mask used for viable-prefix queries."""
    result = {s: frozenset(dfa.labels.get(s, frozenset())) for s in range(dfa.n_states)}
    changed = True
    while changed:
        changed = False
        for s in range(dfa.n_states):
            acc = result[s]
            for d in dfa.transitions.get(s, {}).values():
                acc = acc | result[d]
            if acc != result[s]:
                result[s] = acc
                changed = True
    return result


def language_equal(a: Dfa, b: Dfa, compare_labels: bool = True) -> bool:
    """Product-construction language equality (labels compared per string
    when ``compare_labels``, else just acceptance)."""
    seen = {(a.start, b.start)}
    queue = deque([(a.start, b.start)])
    while queue:
        x, y = queue.popleft()
        la, lb = a.labels.get(x, frozenset()), b.labels.get(y, frozenset())
        if compare_labels:
            if la != lb:
                return False
        elif bool(la) != bool(lb):
            return False
        for sym in a.alphabet:
            dx, dy = a.step(x, sym), b.step(y, sym)
            if (dx is None) != (dy is None):
                # one side dies: fine only if the other side can never accept from here
                alive = dx if dx is not None else dy
                side = a if dx is not None else b
                if coreachable_labels(side).get(alive):
                    return False
                continue
            if dx is None:
                continue
            if (dx, dy) not in seen:
                seen.add((dx, dy))
                queue.append((dx, dy))
    return True


def max_depth(dfa: Dfa) -> int:
    """Length of the longest accepted string (acyclic only)."""
    depth = {dfa.start: 0}
    best = 0
    for s in topological_order(dfa):
        d = depth.get(s, 0)
        if dfa.is_accepting(s):
            best = max(best, d)
        for t in dfa.transitions.get(s, {}).values():
            depth[t] = max(depth.get(t, 0), d + 1)
    return best

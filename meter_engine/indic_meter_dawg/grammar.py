# -*- coding: utf-8 -*-
"""
Right-linear grammars over {U, I}, one per (meter, slot).

Two forms of the same grammar:

* **gana-level** — ``G2 → UII G3 | UIU G3 | ...``: one production per allowed
  gana at each position; readable, this is what the documentation shows.
* **strict** — ``A → aB`` and ``A → a`` only: one terminal per production;
  this is a finite automaton written as rules and is what the NFA is built
  from.

Both are right-linear (Hopcroft–Ullman: ``A → wB`` or ``A → w`` with
``w ∈ Σ*``), so they generate a regular language, which is why a DAWG can
represent every meter exactly.

Owns: building, converting, formatting and *deriving* (enumerating) grammars.
Must not know about DFAs.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, Optional

from .catalogue import MeterSpec
from .constraints import Alternatives, apply_constraints
from .ganas import Gana, GanaRegistry
from . import symbols


@dataclass(frozen=True)
class Production:
    """``lhs → terminals rhs`` (``rhs`` None means the production ends the
    derivation: ``lhs → terminals``)."""
    lhs: str
    terminals: str
    rhs: Optional[str] = None
    comment: str = ""

    def format(self, arrow: str = "→") -> str:
        w = symbols.display(self.terminals)
        body = f"{w} {self.rhs}" if self.rhs else (w or "ε")
        return f"{self.lhs} {arrow} {body}"


@dataclass(frozen=True)
class Grammar:
    meter: str
    slot: str
    form: str                          # "gana" | "strict"
    start: str
    nonterminals: tuple[str, ...]
    productions: tuple[Production, ...]
    gana_positions: tuple[tuple[Gana, ...], ...] = ()   # allowed ganas per position (gana form)
    alphabet: tuple[str, ...] = symbols.ALPHABET         # POEM_ALPHABET for whole-prosodic grammars

    @property
    def name(self) -> str:
        return f"{self.meter}__{self.slot}"

    @property
    def terminals(self) -> tuple[str, ...]:
        return self.alphabet

    def productions_of(self, nonterminal: str) -> tuple[Production, ...]:
        return tuple(p for p in self.productions if p.lhs == nonterminal)


def nonterminal_name(gana_index: int) -> str:
    """Nonterminal for "about to read gana k" (1-based)."""
    return f"G{gana_index}"


def slot_alternatives(spec: MeterSpec, slot: str, registry: GanaRegistry) -> Alternatives:
    """Allowed ganas per position of a slot, after the meter's constraints.

    >>> from .catalogue import load_catalogue; from .ganas import load_registry
    >>> cat, reg = load_catalogue(), load_registry()
    >>> [len(a) for a in slot_alternatives(cat.get("kandamu"), "even", reg)]
    [5, 4, 2, 4, 2]
    """
    tokens = spec.slots[slot]
    alts: Alternatives = [registry.resolve(tok) for tok in tokens]
    return apply_constraints(alts, spec.constraints, slot, registry)


def gana_level_grammar(spec: MeterSpec, slot: str, registry: GanaRegistry) -> Grammar:
    """The readable right-linear grammar of one slot.

    >>> from .catalogue import load_catalogue; from .ganas import load_registry
    >>> g = gana_level_grammar(load_catalogue().get("tetagiti"), "all", load_registry())
    >>> [p.format() for p in g.productions_of("G1")]
    ['G1 → III G2', 'G1 → UI G2']
    """
    alts = slot_alternatives(spec, slot, registry)
    n = len(alts)
    nts = tuple(nonterminal_name(k) for k in range(1, n + 1))
    prods: list[Production] = []
    for k, ganas in enumerate(alts, start=1):
        lhs = nonterminal_name(k)
        rhs = nonterminal_name(k + 1) if k < n else None
        for g in ganas:
            prods.append(Production(lhs=lhs, terminals=g.pattern, rhs=rhs, comment=f"{g.telugu} {g.name}"))
    return Grammar(meter=spec.name, slot=slot, form="gana", start=nts[0], nonterminals=nts,
                   productions=tuple(prods), gana_positions=tuple(alts))


def to_strict(grammar: Grammar) -> Grammar:
    """Split every ``A → a1a2…an B`` into a chain of one-terminal productions.

    Intermediate nonterminals are named ``A_<pattern>_<i>``: "inside the
    alternative ``<pattern>`` of ``A``, ``i`` symbols already read". So
    ``G3_UUI_2`` means: gana 3, alternative UUI (త), two of its three
    symbols consumed. Every strict production carries a comment saying so.

    >>> from .catalogue import load_catalogue; from .ganas import load_registry
    >>> g = to_strict(gana_level_grammar(load_catalogue().get("vidyunmala"), "all", load_registry()))
    >>> [p.format() for p in g.productions][:3]
    ['G1 → U G1_UUU_1', 'G1_UUU_1 → U G1_UUU_2', 'G1_UUU_2 → U G2']
    >>> g.productions[2].comment
    'మ ma: symbol 3/3, complete → G2'
    """
    if grammar.form == "strict":
        return grammar
    prods: list[Production] = []
    nts: list[str] = list(grammar.nonterminals)
    for p in grammar.productions:
        w = p.terminals
        n = len(w)
        who = p.comment or symbols.display(w)
        done = f"complete → {p.rhs}" if p.rhs else "complete, line ends"
        if n <= 1:
            prods.append(Production(p.lhs, w, p.rhs, f"{who}: symbol 1/1, {done}"))
            continue
        prev = p.lhs
        key = symbols.display(w).replace("⏎", "NL")
        for i, ch in enumerate(w[:-1], start=1):
            nxt = f"{p.lhs}_{key}_{i}"
            nts.append(nxt)
            prods.append(Production(prev, ch, nxt, f"{who}: symbol {i}/{n} read, {n - i} to go"))
            prev = nxt
        prods.append(Production(prev, w[-1], p.rhs, f"{who}: symbol {n}/{n}, {done}"))
    return Grammar(meter=grammar.meter, slot=grammar.slot, form="strict", start=grammar.start,
                   nonterminals=tuple(nts), productions=tuple(prods), gana_positions=grammar.gana_positions,
                   alphabet=grammar.alphabet)


def is_right_linear(grammar: Grammar) -> bool:
    """Every production is ``A → wB`` or ``A → w`` with ``w`` over {U, I}."""
    nts = set(grammar.nonterminals)
    return all(symbols.is_canonical(p.terminals, grammar.alphabet) and p.lhs in nts
               and (p.rhs is None or p.rhs in nts) for p in grammar.productions)


def is_strict(grammar: Grammar) -> bool:
    """Every production has exactly one terminal."""
    return is_right_linear(grammar) and all(len(p.terminals) == 1 for p in grammar.productions)


def derive(grammar: Grammar, max_len: int = 64) -> set[str]:
    """Every terminal string the grammar generates (breadth-first over
    sentential forms; ``max_len`` guards cyclic grammars).

    >>> from .catalogue import load_catalogue; from .ganas import load_registry
    >>> g = gana_level_grammar(load_catalogue().get("dvipada"), "all", load_registry())
    >>> len(derive(g))
    432
    """
    by_lhs: dict[str, list[Production]] = {}
    for p in grammar.productions:
        by_lhs.setdefault(p.lhs, []).append(p)
    out: set[str] = set()
    frontier: list[tuple[str, str]] = [("", grammar.start)]
    while frontier:
        nxt: list[tuple[str, str]] = []
        for prefix, nt in frontier:
            for p in by_lhs.get(nt, ()):
                s = prefix + p.terminals
                if len(s) > max_len:
                    continue
                if p.rhs is None:
                    out.add(s)
                else:
                    nxt.append((s, p.rhs))
        frontier = nxt
    return out


def derivation(grammar: Grammar, line: str) -> Optional[list[Production]]:
    """The first leftmost derivation of ``line`` (productions in order), or
    None if the grammar does not generate it.

    >>> from .catalogue import load_catalogue; from .ganas import load_registry
    >>> g = gana_level_grammar(load_catalogue().get("vidyunmala"), "all", load_registry())
    >>> [p.format() for p in derivation(g, "UUUUUUUU")]
    ['G1 → UUU G2', 'G2 → UUU G3', 'G3 → UU']
    """
    by_lhs: dict[str, list[Production]] = {}
    for p in grammar.productions:
        by_lhs.setdefault(p.lhs, []).append(p)

    def go(pos: int, nt: str) -> Optional[list[Production]]:
        for p in by_lhs.get(nt, ()):
            end = pos + len(p.terminals)
            if line[pos:end] != p.terminals:
                continue
            if p.rhs is None:
                if end == len(line):
                    return [p]
                continue
            rest = go(end, p.rhs)
            if rest is not None:
                return [p] + rest
        return None

    return go(0, grammar.start)


def random_line(grammar: Grammar, rng: Optional[random.Random] = None) -> str:
    """One random string of a gana-level grammar (uniform per position).

    >>> from .catalogue import load_catalogue; from .ganas import load_registry
    >>> g = gana_level_grammar(load_catalogue().get("tetagiti"), "all", load_registry())
    >>> s = random_line(g, random.Random(1)); s in derive(g)
    True
    """
    rng = rng or random
    return "".join(rng.choice(ganas).pattern for ganas in grammar.gana_positions)


def canonical_line(grammar: Grammar) -> str:
    """The string built from the first alternative at every position."""
    return "".join(ganas[0].pattern for ganas in grammar.gana_positions)


def language_size(grammar: Grammar) -> int:
    """Number of strings, counted from the alternatives (not enumerated).
    Equals ``len(derive(g))`` only when no two gana sequences spell the same
    string; the DFA path count is the exact figure."""
    n = 1
    for ganas in grammar.gana_positions:
        n *= len(ganas)
    return n


def format_grammar(grammar: Grammar, arrow: str = "→", with_comments: bool = True) -> str:
    """Multi-line text, alternatives of one nonterminal grouped together.

    >>> from .catalogue import load_catalogue; from .ganas import load_registry
    >>> print(format_grammar(gana_level_grammar(load_catalogue().get("vidyunmala"), "all", load_registry())))
    G1 → UUU G2   # మ ma
    G2 → UUU G3   # మ ma
    G3 → UU       # గా gaa
    """
    lines = []
    width = max((len(p.format(arrow)) for p in grammar.productions), default=0) + 2
    for p in grammar.productions:
        text = p.format(arrow)
        if with_comments and p.comment:
            text = f"{text:<{width}} # {p.comment}"
        lines.append(text)
    return "\n".join(lines)


def format_grammar_grouped(grammar: Grammar, arrow: str = "→", sep: str = " | ") -> str:
    """One line per nonterminal: ``G1 → III G2 | UI G2``."""
    lines = []
    for nt in grammar.nonterminals:
        ps = grammar.productions_of(nt)
        if not ps:
            continue
        body = sep.join((f"{symbols.display(p.terminals)} {p.rhs}" if p.rhs else (symbols.display(p.terminals) or "ε")) for p in ps)
        lines.append(f"{nt} {arrow} {body}")
    return "\n".join(lines)


def all_grammars(specs: Iterable[MeterSpec], registry: GanaRegistry) -> dict[tuple[str, str], Grammar]:
    """Gana-level grammars for every (meter, slot) of the concrete meters."""
    out: dict[tuple[str, str], Grammar] = {}
    for spec in specs:
        if spec.abstract:
            continue
        for slot in spec.slots:
            out[(spec.name, slot)] = gana_level_grammar(spec, slot, registry)
    return out

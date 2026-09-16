# -*- coding: utf-8 -*-
"""
The prosodic grammar of a meter, written the way a poem is built::

    Poem      → Line_odd ⏎ Line_even ⏎ Line_odd ⏎ Line_even
    Line_odd  → Kanda−జ Kanda Kanda−జ
    Kanda     → భ | జ | స | నల | గా
    భ         → U I I

Four levels: poem → lines → ganas (classes) → symbols; ``⏎`` is the line
separator terminal. This is the readable, hierarchical form. Because no
nonterminal is recursive except the poem itself (right-recursion for
repeatable meters), the language is regular, and :func:`flatten` rewrites
the whole poem as one right-linear grammar over {U, I, ⏎}; its strict form
is the *prosodic automaton* (:func:`prosodic_automaton`), which accepts exactly the
stanzas the identifier accepts for that meter.

Naming: the *prosodic grammar* is the grammar (of the meter's prosody); a
*poem* is a string it generates, so ``Poem`` is its start symbol and
``random_poem`` / ``accepts_poem`` speak of poems. There is no separate
"poem grammar".

Owns: the hierarchical grammar, its flattening, poem derivation, and the
prosodic automaton. Reuses grammar.py for the right-linear machinery.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Optional

from . import automaton as au
from . import symbols
from .builder import LineDawg, default_dawg
from .catalogue import Constraint, MeterSpec
from .ganas import Gana, GanaRegistry
from .grammar import Grammar, Production, to_strict

NL = symbols.NEWLINE
CLASS_DISPLAY = {"surya": "Surya", "indra": "Indra", "chandra": "Chandra", "kanda": "Kanda"}


@dataclass(frozen=True)
class Rule:
    """``lhs → rhs`` where ``rhs`` is a sequence of terminals and nonterminals."""
    lhs: str
    rhs: tuple[str, ...]
    comment: str = ""

    def format(self, arrow: str = "→") -> str:
        body = " ".join(symbols.display(s) for s in self.rhs) or "ε"
        return f"{self.lhs} {arrow} {body}"


@dataclass(frozen=True)
class ProsodicGrammar:
    meter: str
    start: str
    rules: tuple[Rule, ...]
    levels: dict[str, tuple[str, ...]] = field(default_factory=dict)   # poem | line | class | gana
    terminals: tuple[str, ...] = symbols.POEM_ALPHABET

    @property
    def nonterminals(self) -> tuple[str, ...]:
        seen: list[str] = []
        for r in self.rules:
            if r.lhs not in seen:
                seen.append(r.lhs)
        return tuple(seen)

    def rules_of(self, nt: str) -> tuple[Rule, ...]:
        return tuple(r for r in self.rules if r.lhs == nt)

    def is_terminal(self, sym: str) -> bool:
        return sym in self.terminals


# --------------------------------------------------------------------------
# naming
# --------------------------------------------------------------------------
def class_base_name(token: str) -> Optional[str]:
    """Display name of a class token; None for a literal gana token.

    >>> class_base_name("surya"), class_base_name("all_laghu(indra)"), class_base_name("m4"), class_base_name("భ")
    ('Surya', 'Indra_laghu', 'M4', None)
    """
    if token.startswith("all_laghu(") and token.endswith(")"):
        inner = class_base_name(token[len("all_laghu("):-1])
        return f"{inner}_laghu" if inner else None
    if token in CLASS_DISPLAY:
        return CLASS_DISPLAY[token]
    if token.startswith("m") and token[1:].isdigit():
        return f"M{token[1:]}"
    return None


def _constraint_suffix(c: Constraint, position: int, n_positions: int) -> str:
    if c.rule == "forbid_gana" and position in c.positions:
        return "−" + "|".join(c.ganas)
    if c.rule == "require_gana" and position in c.positions:
        return "=" + "|".join(c.ganas)
    if c.rule == "line_ends_with" and position == n_positions:
        return "$" + symbols.normalize(c.weight or "U")
    return ""


def class_name(spec: MeterSpec, slot: str, position: int, first_symbol: Optional[str] = None) -> Optional[str]:
    """Nonterminal for the gana class at a position, with the constraints
    that narrow it spelled into the name (``Kanda−జ``, ``Kanda=జ|నల``,
    ``Kanda$U``) and, for the first-akshara stanza rule, ``⟨U⟩``/``⟨I⟩``.

    >>> from .catalogue import load_catalogue
    >>> k = load_catalogue().get("kandamu")
    >>> class_name(k, "even", 1), class_name(k, "even", 3), class_name(k, "even", 5), class_name(k, "odd", 1, "U")
    ('Kanda', 'Kanda=జ|నల', 'Kanda$U', 'Kanda−జ⟨U⟩')
    """
    base = class_base_name(spec.slots[slot][position - 1])
    if base is None:
        return None
    n = len(spec.slots[slot])
    suffix = "".join(_constraint_suffix(c, position, n) for c in spec.constraints if c.slot == slot)
    if first_symbol:
        suffix += f"⟨{first_symbol}⟩"
    return base + suffix


def line_name(spec: MeterSpec, slot: str, first_symbol: Optional[str] = None) -> str:
    name = "Line" if list(spec.slots) == ["all"] else f"Line_{slot}"
    return name + (f"⟨{first_symbol}⟩" if first_symbol else "")


def gana_name(g: Gana) -> str:
    return g.telugu


def _first_symbol_variants(spec: MeterSpec, dawg: LineDawg) -> tuple[Optional[str], ...]:
    """(None,) normally; the feasible subset of ('U', 'I') when the
    uniform-first-akshara stanza rule applies (sarvalaghu kandamu has no
    line starting with a guru, so only the ⟨I⟩ branch survives)."""
    if not any(c.rule == "first_akshara_weight_uniform" for c in spec.stanza_constraints):
        return (None,)
    out = []
    for v in ("U", "I"):
        if all(any(g.pattern.startswith(v) for g in dawg.grammars[(spec.name, slot)].gana_positions[0])
               for slot in spec.slots):
            out.append(v)
    return tuple(out)


# --------------------------------------------------------------------------
# hierarchical grammar
# --------------------------------------------------------------------------
def prosodic_grammar(spec: MeterSpec, dawg: Optional[LineDawg] = None) -> ProsodicGrammar:
    """The four-level prosodic grammar of one meter.

    >>> pg = prosodic_grammar(default_dawg().spec("tetagiti"))
    >>> [r.format() for r in pg.rules_of("Poem")]
    ['Poem → Line ⏎ Line ⏎ Line ⏎ Line']
    >>> [r.format() for r in pg.rules_of("Line")]
    ['Line → Surya Indra Indra Surya Surya']
    >>> [r.format() for r in pg.rules_of("Surya")]
    ['Surya → న', 'Surya → హ']
    >>> [r.format() for r in pg.rules_of("హ")]
    ['హ → U I']
    """
    dawg = dawg or default_dawg()
    variants = _first_symbol_variants(spec, dawg)
    poem_rules: list[Rule] = []
    line_rules: list[Rule] = []
    class_rules: dict[str, list[Rule]] = {}
    gana_rules: dict[str, Rule] = {}

    def add_gana(g: Gana) -> str:
        n = gana_name(g)
        gana_rules.setdefault(n, Rule(n, tuple(g.pattern), f"{g.name}, {g.matras} matras"))
        return n

    def add_class(name: str, ganas: tuple[Gana, ...], comment: str) -> None:
        if name in class_rules:
            return
        class_rules[name] = [Rule(name, (add_gana(g),), comment if i == 0 else "") for i, g in enumerate(ganas)]

    # lines and classes, once per (slot, variant)
    for v in variants:
        for slot in spec.slots:
            g = dawg.grammars[(spec.name, slot)]
            rhs: list[str] = []
            for k, allowed in enumerate(g.gana_positions, start=1):
                fs = v if k == 1 else None
                if fs:
                    allowed = tuple(x for x in allowed if x.pattern.startswith(fs))
                cname = class_name(spec, slot, k, fs)
                if cname is None:                       # literal gana (fixed meters, utsahamu's final గ)
                    rhs.append(add_gana(allowed[0]))
                    continue
                tok = spec.slots[slot][k - 1]
                note = f"class {tok}"
                if fs:
                    note += f", first akshara {fs} (stanza rule)"
                add_class(cname, allowed, note)
                rhs.append(cname)
            line_rules.append(Rule(line_name(spec, slot, v), tuple(rhs), f"slot {slot}: {len(rhs)} ganas"))

    # poem: one rule per slot pattern (alternative patterns are whole-stanza forms, never mixed)
    def stanza_rhs(v: Optional[str], pattern: tuple[str, ...]) -> tuple[str, ...]:
        parts: list[str] = []
        for i, slot in enumerate(pattern):
            if i:
                parts.append(NL)
            parts.append(line_name(spec, slot, v))
        return tuple(parts)

    def form_comment(j: int) -> str:
        return f"{spec.padalu} lines" if j == 0 else f"or {spec.padalu} lines of the alternative form"

    if variants != (None,):
        for j, v in enumerate(variants):
            poem_rules.append(Rule("Poem", (f"Poem⟨{v}⟩",),
                                   "stanza rule: every line starts with the same weight" if j == 0 else ""))
        for v in variants:
            for j, pattern in enumerate(spec.slot_patterns):
                poem_rules.append(Rule(f"Poem⟨{v}⟩", stanza_rhs(v, pattern), form_comment(j)))
    elif spec.repeatable:
        poem_rules.append(Rule("Poem", ("Unit",), "one unit"))
        poem_rules.append(Rule("Poem", ("Unit", NL, "Poem"), "or a unit followed by more"))
        for j, pattern in enumerate(spec.slot_patterns):
            poem_rules.append(Rule("Unit", stanza_rhs(None, pattern), form_comment(j)))
    else:
        for j, pattern in enumerate(spec.slot_patterns):
            poem_rules.append(Rule("Poem", stanza_rhs(None, pattern), form_comment(j)))

    rules = tuple(poem_rules + line_rules + [r for rs in class_rules.values() for r in rs] + list(gana_rules.values()))
    levels = {
        "poem": tuple(dict.fromkeys(r.lhs for r in poem_rules)),
        "line": tuple(dict.fromkeys(r.lhs for r in line_rules)),
        "class": tuple(class_rules),
        "gana": tuple(gana_rules),
    }
    return ProsodicGrammar(meter=spec.name, start="Poem", rules=rules, levels=levels)


def format_prosodic_grammar(pg: ProsodicGrammar, arrow: str = "→", with_comments: bool = True) -> str:
    """Grouped text, one block per level, alternatives joined with ``|``."""
    out: list[str] = []
    titles = {"poem": "poem", "line": "lines", "class": "gana classes", "gana": "ganas → symbols"}
    for level, nts in pg.levels.items():
        if not nts:
            continue
        out.append(f"# {titles[level]}")
        for nt in nts:
            rs = pg.rules_of(nt)
            body = " | ".join(" ".join(symbols.display(s) for s in r.rhs) for r in rs)
            line = f"{nt} {arrow} {body}"
            comment = next((r.comment for r in rs if r.comment), "")
            if with_comments and comment:
                line = f"{line:<48} # {comment}"
            out.append(line)
        out.append("")
    return "\n".join(out).rstrip("\n")


# --------------------------------------------------------------------------
# derivation
# --------------------------------------------------------------------------
def random_poem(pg: ProsodicGrammar, rng: Optional[random.Random] = None, max_units: int = 3) -> list[str]:
    """Lines of a random poem generated top-down (uniform choice per
    nonterminal; the repeatable ``Poem → Unit ⏎ Poem`` loop is cut after
    ``max_units``).

    >>> lines = random_poem(prosodic_grammar(default_dawg().spec("vidyunmala")))
    >>> lines
    ['UUUUUUUU', 'UUUUUUUU', 'UUUUUUUU', 'UUUUUUUU']
    """
    rng = rng or random
    out: list[str] = []
    units = 0

    def expand(sym: str) -> None:
        nonlocal units
        if pg.is_terminal(sym):
            out.append(sym)
            return
        rs = pg.rules_of(sym)
        if sym == pg.start and any("Unit" in r.rhs for r in rs):
            units += 1
            stop = units >= max_units or rng.random() < 0.5
            rs = tuple(r for r in rs if (len(r.rhs) == 1) == stop)   # Unit  vs  Unit ⏎ Poem
        r = rng.choice(rs)
        for s in r.rhs:
            expand(s)

    expand(pg.start)
    return "".join(out).split(NL)


def derivation_steps(pg: ProsodicGrammar, lines: list[str], max_steps: int = 400) -> Optional[list[str]]:
    """A leftmost derivation of the poem (list of sentential forms, rendered
    with ⏎), or None if the grammar does not generate it."""
    target = NL.join(symbols.normalize(ln) for ln in lines)

    def parse(sym: str, pos: int):
        """Return (end_pos, [rules used in leftmost order]) or None."""
        if pg.is_terminal(sym):
            return (pos + 1, []) if target.startswith(sym, pos) else None
        for r in pg.rules_of(sym):
            p = pos
            used = [r]
            ok = True
            for s in r.rhs:
                res = parse(s, p)
                if res is None:
                    ok = False
                    break
                p, sub = res
                used.extend(sub)
            if ok:
                return p, used
        return None

    res = parse(pg.start, 0)
    if res is None or res[0] != len(target):
        return None
    forms = [[pg.start]]
    cur = [pg.start]
    for r in res[1]:
        i = next(i for i, s in enumerate(cur) if not pg.is_terminal(s))
        assert cur[i] == r.lhs
        cur = cur[:i] + list(r.rhs) + cur[i + 1:]
        forms.append(list(cur))
        if len(forms) > max_steps:
            break
    return [" ".join(symbols.display(s) for s in f) for f in forms]


# --------------------------------------------------------------------------
# flattening to one right-linear grammar over {U, I, ⏎}
# --------------------------------------------------------------------------
def flatten(spec: MeterSpec, dawg: Optional[LineDawg] = None) -> Grammar:
    """The whole poem as a right-linear grammar. Nonterminal ``L2.G3`` =
    "line 2, about to read gana 3"; ``⟨U⟩L2.G3`` the same inside the
    all-lines-start-with-U variant of a kanda. The last gana of a line emits
    ``⏎`` and hands over to the next line; the last gana of the last line
    ends the poem (and, for repeatable meters, may instead emit ``⏎`` and
    return to ``L1.G1``).

    >>> g = flatten(default_dawg().spec("vidyunmala"))
    >>> [p.format() for p in g.productions]
    ['Poem → UUU L1.G2', 'L1.G2 → UUU L1.G3', 'L1.G3 → UU⏎ L2.G1', 'L2.G1 → UUU L2.G2', 'L2.G2 → UUU L2.G3', 'L2.G3 → UU⏎ L3.G1', 'L3.G1 → UUU L3.G2', 'L3.G2 → UUU L3.G3', 'L3.G3 → UU⏎ L4.G1', 'L4.G1 → UUU L4.G2', 'L4.G2 → UUU L4.G3', 'L4.G3 → UU']
    """
    dawg = dawg or default_dawg()
    variants = _first_symbol_variants(spec, dawg)
    prods: list[Production] = []
    nts: list[str] = ["Poem"]
    patterns = spec.slot_patterns

    def nt(v: Optional[str], p: int, line: int, gana: int) -> str:
        # F1./F2. name the stanza form when the meter has alternative slot patterns (సీసము's all-laghu form)
        form = f"F{p + 1}." if len(patterns) > 1 else ""
        return f"⟨{v}⟩{form}L{line}.G{gana}" if v else f"{form}L{line}.G{gana}"

    for v in variants:
        for p, pattern in enumerate(patterns):
            n_lines = len(pattern)
            for i, slot in enumerate(pattern, start=1):
                g = dawg.grammars[(spec.name, slot)]
                n_ganas = len(g.gana_positions)
                for k, allowed in enumerate(g.gana_positions, start=1):
                    if k == 1 and v:
                        allowed = tuple(x for x in allowed if x.pattern.startswith(v))
                    lhs = nt(v, p, i, k)
                    if not (i == 1 and k == 1):
                        nts.append(lhs)
                    last_gana, last_line = k == n_ganas, i == n_lines
                    for x in allowed:
                        w = x.pattern
                        comment = f"{x.telugu} {x.name}"
                        if not last_gana:
                            targets = [(w, nt(v, p, i, k + 1))]
                        elif not last_line:
                            targets = [(w + NL, nt(v, p, i + 1, 1))]
                        else:
                            targets = [(w, None)]
                            if spec.repeatable:
                                targets.append((w + NL, nt(v, p, 1, 1)))
                        for terminals, rhs in targets:
                            if i == 1 and k == 1:
                                prods.append(Production("Poem", terminals, rhs, comment))
                            if not (i == 1 and k == 1) or spec.repeatable:
                                prods.append(Production(lhs, terminals, rhs, comment))
    if spec.repeatable:
        nts.append(nt(variants[0], 0, 1, 1))
    # keep nonterminal list unique and in first-use order
    order = list(dict.fromkeys(["Poem"] + [p.lhs for p in prods] + [p.rhs for p in prods if p.rhs]))
    return Grammar(meter=spec.name, slot="poem", form="gana", start="Poem", nonterminals=tuple(order),
                   productions=tuple(prods), alphabet=symbols.POEM_ALPHABET)


# --------------------------------------------------------------------------
# prosodic automaton
# --------------------------------------------------------------------------
@lru_cache(maxsize=None)
def prosodic_automaton(meter: str) -> au.Dfa:
    """Minimal DFA over {U, I, ⏎} accepting exactly the poems of ``meter``
    (built from the strict form of :func:`flatten`; cached per meter).

    >>> d = prosodic_automaton("vidyunmala")
    >>> au.accepts(d, "\\n".join(["UUUUUUUU"] * 4)), au.accepts(d, "\\n".join(["UUUUUUUU"] * 3))
    (True, False)
    """
    dawg = default_dawg()
    g = to_strict(flatten(dawg.spec(meter), dawg))
    nfa = au.nfa_from_strict_grammar(g, (meter, "poem"))
    return au.minimize(au.determinize(nfa, alphabet=symbols.POEM_ALPHABET), keep_labels=False)


def accepts_poem(meter: str, lines: list[str]) -> bool:
    """True when the prosodic automaton of ``meter`` accepts these lines.

    >>> accepts_poem("kandamu", ["UIIIUIUII", "UUIIIIIUIUUIIU", "UUIIIIUII", "UUUIIIUIUIIUU"])
    True
    >>> accepts_poem("kandamu", ["IIIIUIUII", "UUIIIIIUIUUIIU", "UUIIIIUII", "UUUIIIUIUIIUU"])   # mixed first aksharas
    False
    """
    return au.accepts(prosodic_automaton(meter), NL.join(symbols.normalize(ln) for ln in lines))

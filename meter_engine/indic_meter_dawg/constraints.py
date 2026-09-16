# -*- coding: utf-8 -*-
"""
Named rules that narrow a meter's gana alternatives (positional constraints)
or bind the lines of a stanza together (stanza constraints).

Owns: what each rule *means*, in code and in plain words. Must not know how
grammars or automata are built — it only filters alternative lists and
checks stanzas.
"""
from __future__ import annotations

from typing import Callable, Sequence

from .catalogue import Constraint
from .ganas import Gana, GanaRegistry
from . import symbols

Alternatives = list[tuple[Gana, ...]]     # one tuple of allowed ganas per gana position


# --------------------------------------------------------------------------
# positional constraints: narrow the alternatives of one slot
# --------------------------------------------------------------------------
def _forbid_gana(alts: Alternatives, c: Constraint, registry: GanaRegistry) -> Alternatives:
    banned = {g.pattern for tok in c.ganas for g in registry.resolve(tok)}
    out = list(alts)
    for p in c.positions:
        out[p - 1] = tuple(g for g in out[p - 1] if g.pattern not in banned)
    return out


def _require_gana(alts: Alternatives, c: Constraint, registry: GanaRegistry) -> Alternatives:
    allowed = {g.pattern for tok in c.ganas for g in registry.resolve(tok)}
    out = list(alts)
    for p in c.positions:
        out[p - 1] = tuple(g for g in out[p - 1] if g.pattern in allowed)
    return out


def _line_ends_with(alts: Alternatives, c: Constraint, registry: GanaRegistry) -> Alternatives:
    w = symbols.normalize(c.weight or "U")
    out = list(alts)
    out[-1] = tuple(g for g in out[-1] if g.pattern.endswith(w))
    return out


POSITIONAL_RULES: dict[str, Callable[[Alternatives, Constraint, GanaRegistry], Alternatives]] = {
    "forbid_gana": _forbid_gana,
    "require_gana": _require_gana,
    "line_ends_with": _line_ends_with,
}


class ConstraintError(ValueError):
    """A constraint emptied a gana position or names an unknown rule."""


def apply_constraints(alts: Alternatives, constraints: Sequence[Constraint], slot: str,
                      registry: GanaRegistry) -> Alternatives:
    """Apply every constraint that targets ``slot`` to the alternatives list.

    >>> from .ganas import load_registry
    >>> reg = load_registry()
    >>> alts = [reg.resolve("kanda")] * 3
    >>> c = Constraint(rule="forbid_gana", slot="odd", positions=(1, 3), ganas=("జ",))
    >>> [len(a) for a in apply_constraints(alts, [c], "odd", reg)]
    [4, 5, 4]
    """
    out = list(alts)
    for c in constraints:
        if c.slot != slot:
            continue
        fn = POSITIONAL_RULES.get(c.rule)
        if fn is None:
            raise ConstraintError(f"unknown constraint rule {c.rule!r}")
        out = fn(out, c, registry)
    for i, a in enumerate(out, start=1):
        if not a:
            raise ConstraintError(f"slot {slot}: constraints leave no gana at position {i}")
    return out


def describe(c: Constraint) -> str:
    """Plain-English sentence for a constraint.

    >>> describe(Constraint(rule="forbid_gana", slot="odd", positions=(1, 3), ganas=("జ",)))
    'in the odd lines, gana 1 and gana 3 may not be జ'
    """
    pos = " and ".join(f"gana {p}" for p in c.positions)
    ganas = " or ".join(c.ganas)
    slot = "every line" if c.slot in ("all", "*") else f"the {c.slot} lines"
    if c.rule == "forbid_gana":
        return f"in {slot}, {pos} may not be {ganas}"
    if c.rule == "require_gana":
        return f"in {slot}, {pos} must be {ganas}"
    if c.rule == "line_ends_with":
        w = "a guru" if symbols.normalize(c.weight or "U") == "U" else "a laghu"
        return f"in {slot}, the last akshara must be {w}"
    if c.rule == "first_akshara_weight_uniform":
        return "the first akshara of every line has the same weight (all guru or all laghu)"
    return c.rule


# --------------------------------------------------------------------------
# stanza constraints: look at all lines at once
# --------------------------------------------------------------------------
def _first_akshara_weight_uniform(lines: Sequence[str]) -> str | None:
    firsts = {ln[0] for ln in lines if ln}
    if len(firsts) > 1:
        return "lines do not all start with the same weight (first aksharas: " + \
            ", ".join(ln[0] for ln in lines) + ")"
    return None


STANZA_RULES: dict[str, Callable[[Sequence[str]], str | None]] = {
    "first_akshara_weight_uniform": _first_akshara_weight_uniform,
}


def check_stanza(lines: Sequence[str], constraints: Sequence[Constraint]) -> tuple[str, ...]:
    """Every violated stanza constraint, as a message. Empty tuple = all pass.

    >>> c = Constraint(rule="first_akshara_weight_uniform", slot="*")
    >>> check_stanza(["UII", "UI"], [c]), bool(check_stanza(["UII", "II"], [c]))
    ((), True)
    """
    out = []
    for c in constraints:
        fn = STANZA_RULES.get(c.rule)
        if fn is None:
            raise ConstraintError(f"unknown stanza rule {c.rule!r}")
        msg = fn(lines)
        if msg:
            out.append(f"{c.rule}: {msg}")
    return tuple(out)

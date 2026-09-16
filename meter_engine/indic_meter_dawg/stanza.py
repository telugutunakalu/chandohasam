# -*- coding: utf-8 -*-
"""
Stanza layer: line count, slot pattern per line, repeatable units, stanza
constraints. Turns per-line walk results into per-meter stanza matches.

Owns: :class:`StanzaMatch`. Must not rank meters or explain — that is
identify.py's job.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from .catalogue import MeterSpec
from .constraints import check_stanza
from .walker import WalkResult


@dataclass(frozen=True)
class StanzaMatch:
    meter: str
    slots: tuple[str, ...]                 # slot of each line
    padanta_lines: tuple[int, ...]         # 0-based lines accepted only via the pādānta rule
    units: int                             # how many repeats of the unit (1 unless repeatable)
    violations: tuple[str, ...] = ()       # stanza rules broken (reported, not fatal: Pothana 3-151, 3-616)


def line_slots(spec: MeterSpec, n_lines: int, pattern: Optional[Sequence[str]] = None) -> Optional[tuple[str, ...]]:
    """Slot of each of ``n_lines`` lines under ``pattern`` (default: the main
    slot pattern), or None when the count does not fit.

    >>> from .catalogue import load_catalogue
    >>> cat = load_catalogue()
    >>> line_slots(cat.get("ataveladi"), 4)
    ('odd', 'even', 'odd', 'even')
    >>> line_slots(cat.get("dvipada"), 6)
    ('all', 'all', 'all', 'all', 'all', 'all')
    >>> line_slots(cat.get("kandamu"), 3) is None
    True
    """
    pattern = tuple(spec.slot_pattern if pattern is None else pattern)
    unit = len(pattern)
    if unit == 0 or n_lines == 0:
        return None
    if spec.repeatable:
        if n_lines % unit:
            return None
        return pattern * (n_lines // unit)
    return pattern if n_lines == unit else None


def _match_pattern(spec: MeterSpec, walks: Sequence[WalkResult], pattern: Sequence[str]) -> Optional[StanzaMatch]:
    slots = line_slots(spec, len(walks), pattern)
    if slots is None:
        return None
    padanta: list[int] = []
    for i, (slot, w) in enumerate(zip(slots, walks)):
        h = (spec.name, slot)
        if h in w.accepted:
            continue
        if h in w.padanta_accepted:
            padanta.append(i)
            continue
        return None
    violations = check_stanza([w.line for w in walks], spec.stanza_constraints)
    units = len(walks) // len(pattern)
    return StanzaMatch(meter=spec.name, slots=slots, padanta_lines=tuple(padanta), units=units, violations=violations)


def match_stanza(spec: MeterSpec, walks: Sequence[WalkResult]) -> Optional[StanzaMatch]:
    """A :class:`StanzaMatch` when every line is accepted in the slot the
    meter assigns to it, under one of the meter's slot patterns (all lines
    follow the same pattern); broken stanza rules are recorded in
    ``violations`` (the identifier ranks such a match below a clean one)."""
    if spec.abstract:
        return None
    for pattern in spec.slot_patterns:
        sm = _match_pattern(spec, walks, pattern)
        if sm is not None:
            return sm
    return None


def stanza_failure(spec: MeterSpec, walks: Sequence[WalkResult]) -> Optional[tuple[int, Optional[int], str]]:
    """Why the stanza is not this meter: ``(line_no, akshara_index, reason)``.
    ``line_no`` is 0-based; ``akshara_index`` is 0-based or None when the
    problem is not inside a line. None when the meter actually matches.
    The reason is given against the main slot pattern."""
    if spec.abstract:
        return (0, None, "abstract family entry")
    if match_stanza(spec, walks) is not None:
        return None
    slots = line_slots(spec, len(walks))
    if slots is None:
        unit = len(spec.slot_pattern)
        how = f"a multiple of {unit}" if spec.repeatable else str(unit)
        return (0, None, f"line count {len(walks)} is not {how}")
    for i, (slot, w) in enumerate(zip(slots, walks)):
        h = (spec.name, slot)
        if h in w.accepted or h in w.padanta_accepted:
            continue
        idx = w.died.get(h)
        if idx is None:
            return (i, None, f"line {i + 1} rejected as slot {slot}")
        if idx >= len(w.line):
            return (i, idx, f"line {i + 1} ends too early for slot {slot} (needs more aksharas)")
        return (i, idx, f"line {i + 1} breaks at akshara {idx + 1} for slot {slot}")
    return None

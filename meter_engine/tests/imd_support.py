# -*- coding: utf-8 -*-
"""Shared helpers for the indic_meter_dawg test suite (not a test module)."""
from __future__ import annotations

import random
import sys
from functools import lru_cache
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import indic_meter_dawg as imd                      # noqa: E402
from indic_meter_dawg import automaton as au        # noqa: E402
from indic_meter_dawg import grammar as gr          # noqa: E402

FIXTURES = HERE / "fixtures"


@lru_cache(maxsize=1)
def dawg():
    return imd.default_dawg()


@lru_cache(maxsize=1)
def expected_counts() -> dict:
    with open(FIXTURES / "expected_counts.yaml", "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@lru_cache(maxsize=None)
def language(meter: str, slot: str) -> frozenset[str]:
    """Every line of a (meter, slot), enumerated from the slot DFA."""
    d = dawg()
    return frozenset(s for s, _ in au.enumerate_language(d.slot_dfas[(meter, slot)]))


def random_stanza(meter: str, rng: random.Random, units: int = 1) -> list[str]:
    """A random valid stanza of ``meter`` (``units`` repeats for repeatable meters)."""
    d = dawg()
    spec = d.spec(meter)
    lines = []
    for _ in range(units if spec.repeatable else 1):
        for slot in spec.slot_pattern:
            lines.append(gr.random_line(d.grammars[(meter, slot)], rng))
    if spec.stanza_constraints:
        # kanda: force a uniform first akshara by regenerating until it holds
        tries = 0
        while len({ln[0] for ln in lines}) > 1 and tries < 200:
            tries += 1
            lines = [gr.random_line(d.grammars[(meter, slot)], rng) for slot in spec.slot_pattern]
    return lines


def oracle_meters(lines: list[str], final_laghu_as_guru: bool = True, soft_stanza: bool = False) -> set[str]:
    """Brute-force identification: a meter matches iff every line is in the
    language of its slot (or, with the pādānta rule, the flipped line is)
    and the stanza constraints hold. Independent of walker/stanza/identify."""
    from indic_meter_dawg import symbols
    from indic_meter_dawg.constraints import check_stanza
    from indic_meter_dawg.stanza import line_slots
    d = dawg()
    out = set()
    for spec in d.catalogue.concrete:
        for pattern in spec.slot_patterns:
            slots = line_slots(spec, len(lines), pattern)
            if slots is None:
                continue
            ok = True
            for ln, slot in zip(lines, slots):
                lang = language(spec.name, slot)
                if ln in lang:
                    continue
                if final_laghu_as_guru and ln.endswith("I") and symbols.flip_final_laghu(ln) in lang:
                    continue
                ok = False
                break
            if ok and (soft_stanza or not check_stanza(lines, spec.stanza_constraints)):
                out.add(spec.name)
    return out


def mutate(line: str, rng: random.Random) -> str:
    i = rng.randrange(len(line))
    return line[:i] + ("U" if line[i] == "I" else "I") + line[i + 1:]

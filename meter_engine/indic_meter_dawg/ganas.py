# -*- coding: utf-8 -*-
"""
Gana registry: the named syllable groups of Telugu prosody, read from
``ganas.yaml``, and the resolution of the gana *tokens* used by the meter
catalogue (``భ``, ``surya``, ``kanda``, ``m4``, ``all_laghu(indra)``).

Owns: which patterns a token stands for. Must not know about meters.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

import yaml

from . import symbols

HERE = Path(__file__).resolve().parent
DEFAULT_GANAS_PATH = HERE.parent / "ganas.yaml"

# yaml section -> group name used in Gana.group and in the class tokens
_GROUP_SECTIONS = {
    "ekakshara_ganas": "ekakshara",
    "dvyakshara_ganas": "dvyakshara",
    "trika_ganas": "trika",
}
_CLASS_SECTIONS = {
    "surya_ganas": "surya",
    "indra_ganas": "indra",
    "chandra_ganas": "chandra",
    "kanda_ganas": "kanda",
}
_CLASS_ALIASES = {
    "సూర్య": "surya", "సూర్యగణము": "surya",
    "ఇంద్ర": "indra", "ఇంద్రగణము": "indra",
    "చంద్ర": "chandra", "చంద్రగణము": "chandra",
    "కంద": "kanda",
}
_LATIN_NAME_ALIASES = {"la": "l", "ga": "g", "guruvu": "g", "laghuvu": "l", "laga": "va", "gala": "ha", "gaga": "gaa"}

_MATRA_TOKEN = re.compile(r"^m(\d+)$")
_ALL_LAGHU_TOKEN = re.compile(r"^all_laghu\((.+)\)$")


class GanaError(KeyError):
    """Raised for an unknown gana token."""


@dataclass(frozen=True, order=True)
class Gana:
    """One named syllable group.

    ``pattern`` is canonical (``U``/``I``); ``group`` is where the gana is
    defined (``trika``, ``dvyakshara``, ``ekakshara``, ``surya`` ...). A gana
    that belongs to several classes keeps the group of its first definition;
    class membership is asked from the registry, not from the gana.
    """
    pattern: str
    name: str
    telugu: str
    group: str

    @property
    def matras(self) -> int:
        return symbols.matras(self.pattern)

    @property
    def aksharas(self) -> int:
        return len(self.pattern)

    @property
    def is_all_laghu(self) -> bool:
        return symbols.is_all_laghu(self.pattern)


@dataclass(frozen=True)
class GanaRegistry:
    ganas: tuple[Gana, ...]
    classes: dict[str, tuple[Gana, ...]]
    by_telugu: dict[str, Gana]
    by_name: dict[str, Gana]
    by_pattern: dict[str, Gana]

    def resolve(self, token: str) -> tuple[Gana, ...]:
        """The ganas a catalogue token stands for, in a stable order.

        >>> reg = load_registry()
        >>> [g.pattern for g in reg.resolve("surya")]
        ['III', 'UI']
        >>> [g.telugu for g in reg.resolve("భ")]
        ['భ']
        >>> [g.pattern for g in reg.resolve("m3")]
        ['IU', 'UI', 'III']
        >>> [g.pattern for g in reg.resolve("all_laghu(indra)")]
        ['IIII']
        """
        return resolve_token(self, token)

    def gana_for_pattern(self, pattern: str, matra_total: Optional[int] = None) -> Gana:
        """The named gana for a pattern, or a synthetic one (``m4:IIIU``) when
        the catalogue has no name for it."""
        g = self.by_pattern.get(pattern)
        if g is not None:
            return g
        total = matra_total if matra_total is not None else symbols.matras(pattern)
        return Gana(pattern=pattern, name=f"m{total}:{pattern}", telugu=symbols.telugu_notation(pattern),
                    group=f"matra{total}")

    def describe(self, gana: Gana) -> str:
        """Human label like ``భ (bha) UII``."""
        return f"{gana.telugu} ({gana.name}) {gana.pattern}"


def _read_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _gana_from_record(rec: dict, group: str) -> Gana:
    pattern = symbols.normalize(rec["pattern"])
    return Gana(pattern=pattern, name=str(rec["name"]), telugu=str(rec["telugu"]), group=group)


@lru_cache(maxsize=None)
def load_registry(path: Optional[str] = None) -> GanaRegistry:
    """Read ``ganas.yaml`` into a :class:`GanaRegistry` (cached per path).

    >>> reg = load_registry()
    >>> reg.by_telugu["న"].pattern, len(reg.classes["indra"])
    ('III', 6)
    """
    data = _read_yaml(Path(path) if path else DEFAULT_GANAS_PATH)
    ganas: list[Gana] = []
    by_telugu: dict[str, Gana] = {}
    by_name: dict[str, Gana] = {}
    by_pattern: dict[str, Gana] = {}

    def register(g: Gana) -> Gana:
        # Keep the first definition of a pattern as canonical; later duplicates
        # (surya/indra re-list trika ganas) map onto the same object.
        if g.pattern in by_pattern:
            existing = by_pattern[g.pattern]
            by_telugu.setdefault(g.telugu, existing)
            by_name.setdefault(g.name, existing)
            return existing
        ganas.append(g)
        by_pattern[g.pattern] = g
        by_telugu.setdefault(g.telugu, g)
        by_name.setdefault(g.name, g)
        return g

    for section, group in _GROUP_SECTIONS.items():
        for rec in data[section]["ganas"]:
            register(_gana_from_record(rec, group))
    classes: dict[str, tuple[Gana, ...]] = {}
    for section, cls in _CLASS_SECTIONS.items():
        recs = data["upaganas"][section]["ganas"]
        classes[cls] = tuple(register(_gana_from_record(rec, cls)) for rec in recs)
    # single-akshara Telugu letters used in ganalu strings: గ (guru) and ల (laghu)
    by_telugu.setdefault("గ", by_pattern["U"])
    by_telugu.setdefault("ల", by_pattern["I"])
    by_name.setdefault("g", by_pattern["U"])
    by_name.setdefault("l", by_pattern["I"])
    return GanaRegistry(ganas=tuple(ganas), classes=classes, by_telugu=by_telugu,
                        by_name=by_name, by_pattern=by_pattern)


def resolve_token(registry: GanaRegistry, token: str) -> tuple[Gana, ...]:
    """Resolve one catalogue token to its ganas. See :meth:`GanaRegistry.resolve`."""
    tok = token.strip()
    m = _ALL_LAGHU_TOKEN.match(tok)
    if m:
        inner = resolve_token(registry, m.group(1))
        out = tuple(g for g in inner if g.is_all_laghu)
        if not out:
            raise GanaError(f"all_laghu({m.group(1)}) is empty")
        return out
    m = _MATRA_TOKEN.match(tok)
    if m:
        total = int(m.group(1))
        return tuple(registry.gana_for_pattern(p, total) for p in symbols.patterns_with_matras(total))
    cls = _CLASS_ALIASES.get(tok, tok)
    if cls in registry.classes:
        return registry.classes[cls]
    if tok in registry.by_telugu:
        return (registry.by_telugu[tok],)
    name = _LATIN_NAME_ALIASES.get(tok, tok)
    if name in registry.by_name:
        return (registry.by_name[name],)
    if symbols.is_canonical(tok) and tok:
        return (registry.gana_for_pattern(tok),)
    raise GanaError(f"unknown gana token {token!r}")


def class_of(registry: GanaRegistry, gana: Gana) -> tuple[str, ...]:
    """Every class (``surya``, ``indra``, ...) that lists this gana.

    >>> reg = load_registry()
    >>> class_of(reg, reg.by_telugu["న"])
    ('surya',)
    """
    return tuple(cls for cls, members in registry.classes.items() if gana in members)

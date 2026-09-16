# -*- coding: utf-8 -*-
"""
Typed view of ``meter_rules.yaml`` (+ ``meters.txt`` for family and Telugu
names). Owns: the :class:`MeterSpec` record, loading, and structural
validation of the ``structure`` block every meter carries.

Must not build grammars or automata; it only says what the meter *is*.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Optional

import yaml

from . import ganas as ganas_mod

HERE = Path(__file__).resolve().parent
DEFAULT_METER_RULES_PATH = HERE.parent / "meter_rules.yaml"
DEFAULT_METERS_TXT_PATH = HERE.parent / "meters.txt"

SYSTEMS = ("fixed", "gana", "matra")
CONSTRAINT_RULES = ("forbid_gana", "require_gana", "line_ends_with")
STANZA_RULES = ("first_akshara_weight_uniform",)


class CatalogueError(ValueError):
    """Raised when the catalogue is structurally unsound."""


@dataclass(frozen=True)
class Constraint:
    """A positional rule on one slot of a meter, e.g. kanda's forbidden జ."""
    rule: str
    slot: str
    positions: tuple[int, ...] = ()
    ganas: tuple[str, ...] = ()
    weight: Optional[str] = None
    why: str = ""


@dataclass(frozen=True)
class MeterSpec:
    id: int
    name: str
    name_te: str
    family: str                      # vrutta | jati | upajati
    padalu: int
    system: str                      # fixed | gana | matra
    slots: dict[str, tuple[str, ...]]          # slot name -> gana tokens
    slot_pattern: tuple[str, ...]              # slot of each line of one unit
    yati_ganas: dict[str, tuple[int, ...]]     # slot -> 1-based gana indices
    yati_aksharas: dict[str, tuple[int, ...]]  # slot -> 1-based akshara indices (fixed meters)
    constraints: tuple[Constraint, ...] = ()
    stanza_constraints: tuple[Constraint, ...] = ()
    repeatable: bool = False
    halves_per_line: int = 1                   # >1 when a pada is conventionally printed as that many lines
    followed_by: tuple[str, ...] = ()
    is_variant_of: Optional[str] = None
    abstract: bool = False
    prasa: bool = True
    prasa_yati: bool = False
    aksharalu: tuple[Optional[int], Optional[int]] = (None, None)
    notes: str = ""
    udaharana: str = ""
    ganalu_text: str = ""
    alt_slot_patterns: tuple[tuple[str, ...], ...] = ()   # whole-stanza alternatives (సీసము's all-laghu form)

    @property
    def slot_names(self) -> tuple[str, ...]:
        return tuple(self.slots)

    @property
    def slot_patterns(self) -> tuple[tuple[str, ...], ...]:
        """The main slot pattern first, then any alternatives; a stanza follows exactly one of them."""
        return (self.slot_pattern,) + self.alt_slot_patterns

    @property
    def is_fixed(self) -> bool:
        return self.system == "fixed"

    def yati_for(self, slot: str) -> tuple[int, ...]:
        """Yati positions for a slot: akshara indices for fixed meters, gana
        indices otherwise (both 1-based)."""
        if self.is_fixed:
            return self.yati_aksharas.get(slot, ())
        return self.yati_ganas.get(slot, ())


@dataclass(frozen=True)
class Catalogue:
    meters: tuple[MeterSpec, ...]
    path: Optional[Path] = None
    by_name: dict[str, MeterSpec] = field(default_factory=dict)

    def get(self, name: str) -> MeterSpec:
        try:
            return self.by_name[name]
        except KeyError:
            raise CatalogueError(f"unknown meter {name!r}") from None

    @property
    def concrete(self) -> tuple[MeterSpec, ...]:
        """Meters that can be identified (the abstract family entries excluded)."""
        return tuple(m for m in self.meters if not m.abstract)

    def variants_of(self, name: str) -> tuple[MeterSpec, ...]:
        return tuple(m for m in self.meters if m.is_variant_of == name)

    def variant_depth(self, name: str) -> int:
        """0 for a base meter, 1 for a variant of a base meter, ..."""
        depth, cur = 0, self.by_name[name]
        while cur.is_variant_of:
            depth += 1
            cur = self.by_name[cur.is_variant_of]
        return depth


def _read_meters_txt(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        rows = {}
        for line in fh:
            if not line.strip():
                continue
            cols = line.rstrip("\n").split("\t")
            row = dict(zip(header, cols))
            rows[row["name"]] = row
    return rows


def _as_tuple(v) -> tuple:
    if v is None:
        return ()
    if isinstance(v, (list, tuple)):
        return tuple(v)
    return (v,)


def _per_slot(value, slot_names: tuple[str, ...]) -> dict[str, tuple[int, ...]]:
    """``[4]`` applies to every slot; ``{odd: [], even: [4]}`` is explicit."""
    if isinstance(value, dict):
        return {s: tuple(int(x) for x in _as_tuple(value.get(s, ()))) for s in slot_names}
    return {s: tuple(int(x) for x in _as_tuple(value)) for s in slot_names}


def _constraint(rec: dict, default_slot: Optional[str]) -> Constraint:
    return Constraint(
        rule=str(rec["rule"]),
        slot=str(rec.get("slot", default_slot or "")),
        positions=tuple(int(p) for p in _as_tuple(rec.get("positions"))),
        ganas=tuple(str(g) for g in _as_tuple(rec.get("gana"))),
        weight=rec.get("weight"),
        why=str(rec.get("why", "")),
    )


def meter_from_record(rec: dict, extra: Optional[dict] = None) -> MeterSpec:
    """Build a :class:`MeterSpec` from one yaml entry (+ its ``meters.txt`` row)."""
    extra = extra or {}
    st = rec.get("structure")
    if st is None:
        raise CatalogueError(f"meter {rec.get('name')!r} has no structure block")
    slots = {str(k): tuple(str(t) for t in v) for k, v in (st.get("slots") or {}).items()}
    slot_names = tuple(slots)
    ak = rec.get("aksharalu") or {}
    variant = st.get("is_variant_of") or (extra.get("is_variant_of") or None)
    if variant:
        variant = str(variant).strip() or None
    return MeterSpec(
        id=int(rec["id"]),
        name=str(rec["name"]),
        name_te=str(extra.get("name_in_telugu") or rec.get("name_te") or rec["name"]),
        family=str(extra.get("type_of_chandassu") or rec.get("family") or "unknown"),
        padalu=int(rec["padalu"]),
        system=str(st["system"]),
        slots=slots,
        slot_pattern=tuple(str(s) for s in st.get("slot_pattern") or ()),
        yati_ganas=_per_slot(st.get("yati_ganas", ()), slot_names),
        yati_aksharas=_per_slot(st.get("yati_aksharas", ()), slot_names),
        constraints=tuple(_constraint(c, None) for c in st.get("constraints") or ()),
        stanza_constraints=tuple(_constraint(c, "*") for c in st.get("stanza_constraints") or ()),
        repeatable=bool(st.get("repeatable", False)),
        halves_per_line=int(st.get("halves_per_line", 1)),
        followed_by=tuple(str(x) for x in st.get("followed_by") or ()),
        is_variant_of=variant,
        abstract=bool(st.get("abstract", False)),
        prasa=bool(rec.get("prasa", True)),
        prasa_yati=bool(rec.get("prasa_yati", False)),
        aksharalu=(ak.get("min"), ak.get("max")),
        notes=str(st.get("notes", "")),
        udaharana=str(rec.get("udaharana", "") or ""),
        ganalu_text=str(rec.get("ganalu", "") or ""),
        alt_slot_patterns=tuple(tuple(str(s) for s in p) for p in st.get("alt_slot_patterns") or ()),
    )


@lru_cache(maxsize=None)
def load_catalogue(path: Optional[str] = None, meters_txt: Optional[str] = None,
                   validate: bool = True) -> Catalogue:
    """Load and (by default) validate the meter catalogue. Cached per path.

    >>> cat = load_catalogue()
    >>> cat.get("tetagiti").slots["all"]
    ('surya', 'indra', 'indra', 'surya', 'surya')
    """
    p = Path(path) if path else DEFAULT_METER_RULES_PATH
    with open(p, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    rows = _read_meters_txt(Path(meters_txt) if meters_txt else DEFAULT_METERS_TXT_PATH)
    # meters.txt has an is_variant_of column holding the parent *id*; translate to a name
    id_to_name = {int(m["id"]): m["name"] for m in data["meters"]}
    meters = []
    for rec in data["meters"]:
        row = dict(rows.get(rec["name"], {}))
        v = row.get("is_variant_of", "")
        if v.strip().isdigit():
            row["is_variant_of"] = id_to_name[int(v)]
        meters.append(meter_from_record(rec, row))
    cat = Catalogue(meters=tuple(meters), path=p, by_name={m.name: m for m in meters})
    if validate:
        problems = validate_catalogue(cat)
        if problems:
            raise CatalogueError("\n".join(problems))
    return cat


def validate_catalogue(cat: Catalogue, registry: Optional[ganas_mod.GanaRegistry] = None) -> list[str]:
    """Every structural problem found, as human-readable strings (empty = sound).

    Checks: systems and rule names known, slot pattern length = padalu,
    every slot in the pattern defined, tokens resolvable, yati positions in
    range, constraint positions in range, variant / followed_by links resolve,
    fixed meters' length equals ``aksharalu``.
    """
    registry = registry or ganas_mod.load_registry()
    problems: list[str] = []
    names = set(cat.by_name)
    for m in cat.meters:
        where = f"[{m.id} {m.name}]"
        if m.system not in SYSTEMS:
            problems.append(f"{where} unknown system {m.system!r}")
        if m.abstract:
            continue
        for pattern in m.slot_patterns:
            if len(pattern) != m.padalu:
                problems.append(f"{where} slot_pattern has {len(pattern)} lines, padalu is {m.padalu}")
            for s in pattern:
                if s not in m.slots:
                    problems.append(f"{where} slot_pattern names undefined slot {s!r}")
        used = {s for pattern in m.slot_patterns for s in pattern}
        for s in m.slots:
            if s not in used:
                problems.append(f"{where} slot {s!r} is defined but never used")
        lengths: dict[str, tuple[int, int]] = {}
        for s, tokens in m.slots.items():
            lo = hi = 0
            for tok in tokens:
                try:
                    gs = registry.resolve(tok)
                except ganas_mod.GanaError as e:
                    problems.append(f"{where} slot {s}: {e}")
                    continue
                lo += min(g.aksharas for g in gs)
                hi += max(g.aksharas for g in gs)
                if m.is_fixed and len(gs) != 1:
                    problems.append(f"{where} fixed meter uses class token {tok!r}")
            lengths[s] = (lo, hi)
            for k in m.yati_ganas.get(s, ()):
                if not 1 <= k <= len(tokens):
                    problems.append(f"{where} slot {s}: yati gana {k} outside 1..{len(tokens)}")
            for a in m.yati_aksharas.get(s, ()):
                if not 1 <= a <= lo:
                    problems.append(f"{where} slot {s}: yati akshara {a} outside 1..{lo}")
        for c in m.constraints:
            if c.rule not in CONSTRAINT_RULES:
                problems.append(f"{where} unknown constraint rule {c.rule!r}")
            if c.slot not in m.slots:
                problems.append(f"{where} constraint on undefined slot {c.slot!r}")
            else:
                n = len(m.slots[c.slot])
                for p in c.positions:
                    if not 1 <= p <= n:
                        problems.append(f"{where} constraint position {p} outside 1..{n} in slot {c.slot}")
            for g in c.ganas:
                try:
                    registry.resolve(g)
                except ganas_mod.GanaError as e:
                    problems.append(f"{where} constraint: {e}")
        for c in m.stanza_constraints:
            if c.rule not in STANZA_RULES:
                problems.append(f"{where} unknown stanza rule {c.rule!r}")
        if m.halves_per_line < 1:
            problems.append(f"{where} halves_per_line must be >= 1")
        if m.halves_per_line > 1 and m.repeatable:
            problems.append(f"{where} halves_per_line is not supported together with repeatable")
        if m.is_variant_of and m.is_variant_of not in names:
            problems.append(f"{where} is_variant_of unknown meter {m.is_variant_of!r}")
        for f in m.followed_by:
            if f not in names:
                problems.append(f"{where} followed_by unknown meter {f!r}")
        lo_all = min((v[0] for v in lengths.values()), default=None)
        hi_all = max((v[1] for v in lengths.values()), default=None)
        amin, amax = m.aksharalu
        if amin is not None and lo_all is not None and amin != lo_all:
            problems.append(f"{where} aksharalu.min {amin} but grammar gives {lo_all}")
        if amax is not None and hi_all is not None and amax != hi_all:
            problems.append(f"{where} aksharalu.max {amax} but grammar gives {hi_all}")
    return problems

"""Metre labels, engine identification and the canonical one-pāda-per-line layout.

Editions print poems in many layouts (Padyarchana: a sīsa as 12 half-lines, as 6 lines
with "|" between halves, gīti pādas two to a line, kanda pādas two to a line with no
separator ...). ``canonicalise`` tries the printed lines, then the lines split at the
separators, then (for a known metre printed two pādas to a line) every word-boundary split,
and keeps the first layout the engine identifies.

The target layout is one pāda per line, except the sīsa: its pādas stay as two half-lines,
the way editions print them, because the yati engine only checks a sīsa printed in halves
(measured on 59 Bhagavatam sīsas: yati passes 49 with halves on separate lines, 0 when
each pāda is one line). A sīsa printed with whole pādas is split at the end of its 4th gaṇa.
"""
from __future__ import annotations

import functools
import itertools
from dataclasses import dataclass

from indic_meter_dawg import default_dawg, identify_text

from tokenizer.akshara import aksharas, normalize

from .text import clean_poem, split_pieces

UNKNOWN_LABELS = {"", "Unknown", None}
PADAS = {"dvipada": 2}                  # pādas per stanza when not 4 (the metres we split-search)
MAX_SPLIT_COMBOS = 400


@functools.lru_cache(maxsize=1)
def dawg():
    return default_dawg()


ALIASES = {"గీతము": ("tetagiti", "ataveladi")}   # a gīti printed without saying which: the engine decides


def _name_key(name: str) -> str:
    """Spelling-insensitive key: కందం = కందము, మత్తకోకిల = మత్తకోకిలము, స్రగ్విణీ = స్రగ్విణి."""
    k = name.replace("_", " ").strip()
    for suffix in ("ము", "ం", "మ్"):
        if k.endswith(suffix):
            k = k[: -len(suffix)]
            break
    return k[:-1] + "ి" if k.endswith("ీ") else k


@functools.lru_cache(maxsize=1)
def te_to_catalogue() -> dict[str, str]:
    """Telugu metre name (as editions print it, spelling-normalised) -> catalogue name."""
    out = {}
    for name, spec in dawg().catalogue.by_name.items():
        if spec.name_te:
            out[_name_key(spec.name_te)] = name
    return out


def parse_label(label: str | None) -> tuple[frozenset, str | None]:
    """(allowed catalogue names for the main metre, catalogue name of a named ettugīti or None).

    "సీసము + తేటగీతి" -> ({seesamu}, tetagiti); "ఆటవెలది/తేటగీతి" -> ({ataveladi, tetagiti}, None);
    a label outside the catalogue -> (frozenset(), None)."""
    if label in UNKNOWN_LABELS:
        return frozenset(), None
    table = te_to_catalogue()
    main, _, trailer = label.partition("+")
    names = set()
    for p in main.split("/"):
        p = p.strip()
        names.update(ALIASES.get(p, ()))
        if _name_key(p) in table:
            names.add(table[_name_key(p)])
    return frozenset(names), table.get(_name_key(trailer)) if trailer else None


def catalogue_label(name: str | None) -> str | None:
    """Roman catalogue name -> the Telugu name used in headers."""
    if not name:
        return None
    spec = dawg().catalogue.by_name.get(name)
    return spec.name_te.replace("_", " ") if spec else None


@dataclass(frozen=True)
class Option:
    meter: str                  # main metre (catalogue name)
    label: str                  # composite label, e.g. "seesamu+tetagiti"
    name_te: str                # e.g. "సీసము+తేటగీతి"
    n_lines: int                # lines of the main unit as the engine counts them
    n_trailer: int              # lines of the ettugīti unit (0 if none)
    variant_of: str | None
    half_ends: tuple = ()       # sīsa only: aksharas in the first half of each pāda (end of gaṇa 4)


@dataclass
class Ident:
    options: tuple              # every candidate, the engine's best first

    @property
    def meter(self) -> str | None:
        return self.options[0].meter if self.options else None

    def pick(self, allowed: frozenset) -> Option | None:
        """The best candidate whose metre (or the metre it is a variant of) is allowed."""
        for o in self.options:
            if o.meter in allowed or o.variant_of in allowed:
                return o
        return None


def _option(c) -> Option:
    name_te = (c.name_te + ("+" + c.trailer.name_te if c.trailer else "")).replace("_", " ")
    ends = ()
    if c.meter == "seesamu":
        ends = tuple(lm.segmentation.segments[3].end if lm.segmentation and len(lm.segmentation.segments) > 4 else 0
                     for lm in c.lines)
    return Option(c.meter, c.label, name_te, len(c.lines), len(c.trailer.lines) if c.trailer else 0,
                  c.is_variant_of, ends)


def identify(lines: list[str]) -> Ident:
    res = identify_text(lines, dawg())
    if res.best is None:
        return Ident(())
    rest = [c for c in res.candidates if c is not res.best]
    return Ident(tuple(_option(c) for c in [res.best, *rest]))


def _agrees(ident: Ident, allowed: frozenset) -> bool:
    return ident.pick(allowed) is not None


def _split_search(lines: list[str], allowed: frozenset) -> tuple[list[str], Ident] | None:
    """Lines printed two pādas each with no separator: try every word-boundary split."""
    options = []
    for ln in lines:
        words = ln.split(" ")
        options.append([(" ".join(words[:k]), " ".join(words[k:])) for k in range(1, len(words))])
    n = 1
    for o in options:
        n *= max(1, len(o))
    if not all(options) or n > MAX_SPLIT_COMBOS:
        return None
    mid = [len(o) // 2 for o in options]              # try splits near the middle first
    ordered = [sorted(range(len(o)), key=lambda k, m=m: abs(k - m)) for o, m in zip(options, mid)]
    for choice in itertools.product(*ordered):
        cand = [p for o, k in zip(options, choice) for p in o[k]]
        ident = identify(cand)
        if _agrees(ident, allowed):
            return cand, ident
    return None


def _split_after(line: str, k: int) -> tuple[str, str] | None:
    """Split a printed line after its k-th Telugu akshara (punctuation and spaces don't count)."""
    seen, pos = 0, 0
    for piece in aksharas(normalize(line)):
        pos += len(piece)
        if "\u0C00" <= piece[0] <= "\u0C7F":
            seen += 1
            if seen == k:
                a, b = line[:pos].strip(), line[pos:].strip(" -|।")
                return (a, b) if a and b else None
    return None


def _seesa_halves(lines: list[str], opt: Option) -> list[str]:
    """A sīsa printed with whole pādas: split each into its two halves."""
    if opt.meter != "seesamu" or not opt.half_ends:
        return lines
    main = len(lines) - opt.n_trailer
    if main != opt.n_lines or len(opt.half_ends) != main or not all(opt.half_ends):
        return lines                                           # already in halves (or unknown)
    out = []
    for ln, k in zip(lines[:main], opt.half_ends):
        parts = _split_after(ln, k)
        if parts is None:
            return lines
        out += parts
    return out + lines[main:]


@dataclass
class Canon:
    lines: list[str]            # cleaned target lines (one pāda, or sīsa half, per line)
    status: str                 # agree | engine-only | label-only | none
    meter: str | None           # catalogue name of the main metre when status is agree/engine-only
    label: str | None           # composite catalogue label
    name_te: str | None         # Telugu header name
    layout: str                 # raw | split | search | -
    roundtrip: bool | None      # cleaned canonical text identifies as the same metre (None if not identified)


def canonicalise(printed: list[str], label: str | None) -> Canon:
    allowed, _trailer = parse_label(label)
    unknown = label in UNKNOWN_LABELS
    layouts = [("raw", printed)]
    pieces = split_pieces(printed)
    if pieces != printed:
        layouts.append(("split", pieces))
    chosen = None
    for kind, lines in layouts:
        ident = identify(lines)
        if (allowed and _agrees(ident, allowed)) or (unknown and ident.meter):
            chosen = (kind, lines, ident)
            break
    if chosen is None and allowed:
        expected = max(PADAS.get(a, 4) for a in allowed)
        if len(pieces) * 2 == expected:
            found = _split_search(pieces, allowed)
            if found:
                chosen = ("search", found[0], found[1])
    if chosen is None:
        status = "label-only" if allowed else "none"
        return Canon(clean_poem(pieces), status, None, None, None, "-", None)

    kind, lines, ident = chosen
    opt = ident.pick(allowed) if allowed else ident.options[0]
    status = "agree" if allowed else "engine-only"
    canonical = _seesa_halves(lines, opt)
    cleaned = clean_poem(canonical)
    same = frozenset({opt.meter})
    ok = identify(cleaned).pick(same) is not None
    if not ok and canonical is not lines:                       # the split broke it: keep whole pādas
        cleaned = clean_poem(lines)
        ok = identify(cleaned).pick(same) is not None
    return Canon(cleaned, status, opt.meter, opt.label, opt.name_te, kind, ok)

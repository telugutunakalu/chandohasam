# -*- coding: utf-8 -*-
"""
Recover the gana segmentation of a line under one (meter, slot), and from
it the akshara positions of the meter's yati checkpoints.

Owns: :class:`Segmentation`. This is the hook the yati engine will consume.
Must not decide *which* meter applies; the walker/identifier do that.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from . import symbols
from .builder import LineDawg, default_dawg
from .catalogue import MeterSpec
from .ganas import Gana


@dataclass(frozen=True)
class GanaSegment:
    index: int          # 1-based gana position
    gana: Gana
    start: int          # 1-based akshara index of the gana's first akshara
    end: int            # 1-based akshara index of its last akshara

    @property
    def pattern(self) -> str:
        return self.gana.pattern


@dataclass(frozen=True)
class Segmentation:
    meter: str
    slot: str
    line: str
    segments: tuple[GanaSegment, ...]
    yati_aksharas: tuple[int, ...]          # 1-based akshara indices where yati must hold
    padanta_applied: bool = False

    @property
    def gana_names(self) -> tuple[str, ...]:
        return tuple(s.gana.telugu for s in self.segments)

    @property
    def matras(self) -> int:
        return symbols.matras(self.line)

    def format(self) -> str:
        """``UII UIU III | భ ర న | yati@10``"""
        pats = " ".join(s.pattern for s in self.segments)
        names = " ".join(self.gana_names)
        yati = ",".join(str(y) for y in self.yati_aksharas) or "-"
        return f"{pats} | {names} | yati@{yati}"


def _all_segmentations(alts, line: str) -> list[list[Gana]]:
    out: list[list[Gana]] = []

    def go(pos: int, k: int, acc: list[Gana]) -> None:
        if k == len(alts):
            if pos == len(line):
                out.append(list(acc))
            return
        for g in alts[k]:
            end = pos + len(g.pattern)
            if line[pos:end] == g.pattern:
                acc.append(g)
                go(end, k + 1, acc)
                acc.pop()

    go(0, 0, [])
    return out


def yati_positions(spec: MeterSpec, slot: str, segments: tuple[GanaSegment, ...]) -> tuple[int, ...]:
    """Akshara indices of the yati checkpoints: the catalogue's akshara list
    for fixed meters, the first akshara of gana k for gana-yati meters."""
    if spec.is_fixed:
        return tuple(spec.yati_aksharas.get(slot, ()))
    starts = {s.index: s.start for s in segments}
    return tuple(starts[k] for k in spec.yati_ganas.get(slot, ()) if k in starts)


def segment(meter: str, slot: str, line: str, dawg: Optional[LineDawg] = None,
            final_laghu_as_guru: bool = True) -> tuple[Segmentation, ...]:
    """Every gana segmentation of ``line`` under ``(meter, slot)``, the
    canonical one (grammar alternative order) first; empty when the line is
    not in the slot's language.

    >>> segs = segment("utpalamala", "all", "UIIUIUIIIUIIUIIUIUIU")
    >>> segs[0].gana_names, segs[0].yati_aksharas
    (('భ', 'ర', 'న', 'భ', 'భ', 'ర', 'వ'), (10,))
    >>> segment("tetagiti", "all", "I" * 17)[0].yati_aksharas
    (12,)
    """
    dawg = dawg or default_dawg()
    spec = dawg.spec(meter)
    grammar = dawg.grammars[(meter, slot)]
    s = symbols.normalize(line)
    candidates = [(s, False)]
    if final_laghu_as_guru and s.endswith(symbols.LAGHU):
        candidates.append((symbols.flip_final_laghu(s), True))
    result: list[Segmentation] = []
    for text, flipped in candidates:
        for ganas in _all_segmentations(grammar.gana_positions, text):
            segs = []
            pos = 1
            for i, g in enumerate(ganas, start=1):
                segs.append(GanaSegment(index=i, gana=g, start=pos, end=pos + len(g.pattern) - 1))
                pos += len(g.pattern)
            segs_t = tuple(segs)
            result.append(Segmentation(meter=meter, slot=slot, line=text, segments=segs_t,
                                       yati_aksharas=yati_positions(spec, slot, segs_t), padanta_applied=flipped))
        if result:
            break      # prefer the un-flipped reading
    return tuple(result)

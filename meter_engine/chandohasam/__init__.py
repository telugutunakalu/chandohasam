# -*- coding: utf-8 -*-
"""
chandohasam — end-to-end Telugu ఛందస్సు analysis of a poem.

Wires the three engines of ``meter_engine`` together:

* ``indic_meter_dawg`` — scansion (guru/laghu) and metre identification,
* ``prasa_engine``     — ప్రాస (second-akshara rhyme) verification,
* ``yati``             — యతి (caesura maitri) verification,

and returns one structured result: the metre, the గణవిభజన of every pāda
(gaṇas → aksharas → weights), the prāsa aksharas and verdict, and the yati
aksharas and verdict of every yati group.

    from chandohasam import analyze
    a = analyze(poem_text)                     # PadyaAnalysis
    a.meter, a.matched, a.prasa_matched, a.yati_matched
    a.units[0].lines[0].ganas[0].aksharas      # గణవిభజన
    a.units[0].prasa.seats                     # ప్రాస aksharas per pāda
    a.units[0].lines[0].yati                   # యతి seats per pāda
    print(a.render()); a.to_json()

    python3 -m chandohasam --file poem.txt [--json]
"""
from __future__ import annotations

from .analysis import analyze                                                              # noqa: F401
from .models import (AksharaCell, GanaCell, LineReport, PadyaAnalysis, PrasaReport, PrasaSeat,   # noqa: F401
                     UnitReport, YatiSeat)
from .report import render_text                                                            # noqa: F401

__all__ = ["analyze", "PadyaAnalysis", "UnitReport", "LineReport", "GanaCell", "AksharaCell",
           "PrasaReport", "PrasaSeat", "YatiSeat", "render_text"]

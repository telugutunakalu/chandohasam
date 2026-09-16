# -*- coding: utf-8 -*-
"""
Command line: ``python3 -m chandohasam [--file poem.txt | PADA ...] [--json] [--profile P] [--yati-sandhi M] [--meter NAME]``
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional

from .analysis import analyze


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="chandohasam",
                                 description="Telugu ఛందస్సు analysis: metre, గణవిభజన, ప్రాస and యతి of a poem")
    ap.add_argument("padas", nargs="*", help="the pādas (one argument each); or use --file")
    ap.add_argument("--file", help="text file, one pāda per line (blank line = end of poem)")
    ap.add_argument("--profile", default="strict", choices=["strict", "relaxed", "historical"])
    ap.add_argument("--yati-sandhi", default="hypothesis", choices=["off", "hypothesis", "acchu"])
    ap.add_argument("--meter", help="force this catalogue metre when several candidates match")
    ap.add_argument("--json", action="store_true", help="print the full structured result as JSON")
    ns = ap.parse_args(argv)
    if ns.file:
        text = open(ns.file, encoding="utf-8").read().strip()
    elif ns.padas:
        text = "\n".join(ns.padas)
    else:
        text = sys.stdin.read().strip()
    if not text:
        ap.error("no poem given")
    res = analyze(text, profile=ns.profile, yati_sandhi=ns.yati_sandhi, meter=ns.meter)
    print(res.to_json() if ns.json else res.render())
    return 0 if res.matched else 1

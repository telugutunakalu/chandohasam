# -*- coding: utf-8 -*-
"""Command line of the yati engine (``python3 -m yati …`` or ``python3 yati_engine.py …``).
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Optional

from .constants import ENGINE_DIR
from .ruleset import load_ruleset
from .verdict import check
from .pairing import lookup_pair, maitri_matrix
from .line import evaluate_line
from .stanza import evaluate_stanza
from .fixtures import run_attested_examples


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="yati", description="Telugu యతి engine — pair, line and stanza checks with a provenance trail")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="check one akshara pair (leading ం = preceding anusvāra; న్+సా = fused drutam)")
    c.add_argument("a"); c.add_argument("b")
    c.add_argument("--profile", default="strict", choices=["strict", "relaxed", "historical"])
    c.add_argument("--sandhi", default="hypothesis", choices=["off", "hypothesis", "acchu"])
    c.add_argument("--vowel-a", default="", help="confirmed underlying vowel of a"); c.add_argument("--vowel-b", default="")
    c.add_argument("--word-a", help="the word a sits in (for ubhaya triggers)"); c.add_argument("--word-b")
    c.add_argument("--index-a", type=int, help="akshara index of a inside --word-a"); c.add_argument("--index-b", type=int)
    c.add_argument("--prev-dead-a", help="dead consonant(s) of the previous line, e.g. న"); c.add_argument("--json", action="store_true")
    l = sub.add_parser("lookup", help="consonant-pair table entry")
    l.add_argument("a"); l.add_argument("b"); l.add_argument("--bindu-a", action="store_true"); l.add_argument("--bindu-b", action="store_true")
    l.add_argument("--vowel-class", default="A", choices=["A", "I", "U"])
    m = sub.add_parser("matrix", help="all consonant pairs"); m.add_argument("--tsv", action="store_true"); m.add_argument("--vowel-class", default="A")
    sub.add_parser("rules", help="rule catalogue")
    sub.add_parser("examples", help="replay the fixtures")
    ln = sub.add_parser("line", help="evaluate one pāda"); ln.add_argument("pada")
    ln.add_argument("--yati", required=True, help="yati groups, e.g. 1,10 or 1,8,15 or 1,7/13,19")
    ln.add_argument("--profile", default="strict"); ln.add_argument("--prev-dead"); ln.add_argument("--json", action="store_true")
    st = sub.add_parser("stanza", help="identify the meter with the DAWG and evaluate every yati")
    st.add_argument("--file"); st.add_argument("--meter"); st.add_argument("--profile", default="strict"); st.add_argument("--json", action="store_true")
    st.add_argument("padas", nargs="*")
    return ap


def _cmd_check(ns, rs) -> int:
    r = check(ns.a, ns.b, ns.profile, ruleset=rs, sandhi=ns.sandhi, vowel_a=ns.vowel_a or (), vowel_b=ns.vowel_b or (),
              word_a=ns.word_a, word_b=ns.word_b, index_a=ns.index_a, index_b=ns.index_b,
              prev_dead_a=list(ns.prev_dead_a) if ns.prev_dead_a else None)
    if ns.json:
        print(r.to_json(indent=2))
        return 0 if r.matched else 1
    print(r.explain())
    for m in r.candidates[:6]:
        print(f"   candidate: {m.rule} {m.label_te} ({m.reading_a.show()} ↔ {m.reading_b.show()}) rank={m.rank} status={m.status}")
    for m in r.rejected[:6]:
        print(f"   rejected : {m.rule} {m.label_te}: {m.detail}")
    return 0 if r.matched else 1


def _cmd_lookup(ns, rs) -> int:
    print(json.dumps(lookup_pair(ns.a, ns.b, ns.bindu_a, ns.bindu_b, ns.vowel_class, rs), ensure_ascii=False, indent=2))
    return 0


def _cmd_matrix(ns, rs) -> int:
    rows = maitri_matrix(rs, ns.vowel_class)
    if ns.tsv:
        print("a\tb\trule\tstatus\tpositive")
        for r in rows:
            print(f"{r['a']}\t{r['b']}\t{r['rule']}\t{r['status']}\t{r['positive']}")
    else:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
    return 0


def _cmd_rules(ns, rs) -> int:
    for r in rs.data["rules"]:
        print(f"{r['id']:<16} {r['status']:<24} {r['kind']:<10} {r['names'].get('te', '')}  — {r['names']['en']}  [{r.get('src')}]")
    return 0


def _cmd_examples(ns, rs) -> int:
    rep = run_attested_examples(rs)
    bad = [r for r in rep if not r["ok"]]
    for r in rep:
        print(("OK   " if r["ok"] else "FAIL ") + r["id"] + ("" if r["ok"] else "  " + "; ".join(r["problems"])))
    print(f"{len(rep) - len(bad)}/{len(rep)} fixtures pass")
    return 0 if not bad else 1


def _cmd_line(ns, rs) -> int:
    sys.path.insert(0, str(ENGINE_DIR))
    from indic_meter_dawg import scansion as sc
    syls = list(sc.scan_line(ns.pada).syllables)
    groups = [tuple(int(x) for x in g.split(",")) for g in ns.yati.split("/")]
    ly = evaluate_line(syls, groups, ns.profile, prev_line_dead=list(ns.prev_dead) if ns.prev_dead else None, ruleset=rs)
    if ns.json:
        print(json.dumps(ly.to_dict(), ensure_ascii=False, indent=2))
    else:
        for g in ly.groups:
            for r in g.results:
                print(r.explain())
            for v in g.violations:
                print("   " + v)
    return 0 if ly.matched else 1


def _cmd_stanza(ns, rs) -> int:
    text = open(ns.file, encoding="utf-8").read() if ns.file else "\n".join(ns.padas)
    sy = evaluate_stanza(text, ns.meter, ns.profile, ruleset=rs)
    print(json.dumps(sy.to_dict(), ensure_ascii=False, indent=2) if ns.json else sy.explain())
    return 0 if sy.matched else 1


_COMMANDS = {"check": _cmd_check, "lookup": _cmd_lookup, "matrix": _cmd_matrix, "rules": _cmd_rules,
             "examples": _cmd_examples, "line": _cmd_line, "stanza": _cmd_stanza}


def main(argv: Optional[list[str]] = None) -> int:
    ns = _build_parser().parse_args(argv)
    return _COMMANDS[ns.cmd](ns, load_ruleset())

# -*- coding: utf-8 -*-
"""
Command line of the prāsa engine (``python3 -m prasa …`` / ``python3 prasa_engine.py …``).
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Optional

from .constants import PROFILE_ORDER
from .akshara import render_onset
from .ruleset import load_ruleset
from .stanza import PrasaResult, evaluate
from .lookup import lookup_pair, maitri_matrix, run_attested_examples


def _print_result(res: PrasaResult) -> None:
    print(f"profile      : {res.profile}")
    print(f"matched      : {res.matched}" + ("" if res.applicable else "   (meter does not require prāsa)"))
    print(f"min_profile  : {res.min_profile}")
    if res.error:
        print(f"error        : {res.error}")
        return
    print(f"prāsa        : {res.label_te}  |  {res.label_en}")
    print(f"consonant    : {res.prasa_consonant}")
    print("lines        :")
    for ln in res.lines:
        print(f"  {ln['index']}: {ln['purva']!s:>6} [{ln['purva_weight_positional']}]  {ln['prasa']!s:<6} "
              f"onset={render_onset(ln['onset']) or ln['vowel']}  vowel={ln['vowel'] or '-'}"
              + ("  ం-before" if ln['purva_purnabindu'] else "") + ("  ః-before" if ln['purva_visarga'] else "")
              + ("  ఁ-before" if ln['ardhabindu_before'] else ""))
    print("classification:")
    for c in res.classifications:
        print(f"  {c['rule']:<34} {c['status']:<20} {c['name_te']}")
    if res.violations:
        print("violations   :")
        for v in res.violations:
            print(f"  {v['rule']:<34} {v['scope']:<10} {v['detail']}")
    if res.would_match_under:
        print(f"would match under profile: {res.would_match_under}")
    print("trail        :")
    for t in res.trail:
        print(f"  [{t['status']:<4}] {t['rule']:<34} {t['scope']:<10} {t['detail']}")


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="prasa", description="Telugu prāsa validator with provenance trail")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="evaluate a stanza")
    c.add_argument("padas", nargs="*")
    c.add_argument("--file", help="text file, one pāda per line; blank line separates stanzas")
    c.add_argument("--profile", default="strict", choices=PROFILE_ORDER)
    c.add_argument("--meter")
    c.add_argument("--meter-class")
    c.add_argument("--json", action="store_true")
    lk = sub.add_parser("lookup", help="consonant-pair lookup")
    lk.add_argument("a")
    lk.add_argument("b")
    mx = sub.add_parser("matrix", help="print the full pairwise lookup table")
    mx.add_argument("--tsv", action="store_true")
    sub.add_parser("rules", help="list rules")
    sub.add_parser("examples", help="run the attested examples embedded in the YAML")
    return ap


def _stanzas_from_args(args, ap: argparse.ArgumentParser) -> list[list[str]]:
    """Stanzas from ``--file`` (blank line = new stanza) and/or the positional pādas."""
    stanzas: list[list[str]] = []
    if args.file:
        cur: list[str] = []
        with open(args.file, "r", encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    cur.append(line.rstrip("\n"))
                elif cur:
                    stanzas.append(cur)
                    cur = []
        if cur:
            stanzas.append(cur)
    if args.padas:
        stanzas.append(list(args.padas))
    if not stanzas:
        ap.error("give pādas as arguments or --file")
    return stanzas


def _cmd_check(args, rs, ap) -> int:
    for st in _stanzas_from_args(args, ap):
        res = evaluate(st, profile=args.profile, meter=args.meter, meter_class=args.meter_class, ruleset=rs)
        if args.json:
            print(res.to_json())
        else:
            _print_result(res)
            print()
    return 0


def _cmd_lookup(args, rs, ap) -> int:
    print(json.dumps(lookup_pair(args.a, args.b, rs), ensure_ascii=False, indent=2))
    return 0


def _cmd_matrix(args, rs, ap) -> int:
    rows = maitri_matrix(rs)
    if args.tsv:
        print("a\tb\trule\tstatus\tmin_profile\tname_en")
        for r in rows:
            print(f"{r['a']}\t{r['b']}\t{r['rule']}\t{r['status']}\t{r['min_profile']}\t{r['name_en']}")
    else:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
    return 0


def _cmd_rules(args, rs, ap) -> int:
    for r in rs.data["rules"]:
        print(f"{r['id']:<34} {r['status']:<20} {r['names']['en']}  /  {r['names'].get('te', '')}")
    return 0


def _cmd_examples(args, rs, ap) -> int:
    rep = run_attested_examples(rs)
    bad = [r for r in rep if not r["ok"]]
    for r in rep:
        flag = "ok " if r["ok"] else "BAD"
        print(f"[{flag}] {r['id']:<40} min_profile={r['min_profile']!s:<10} {r['label_te']}"
              + (f"   problems: {r['problems']}" if r["problems"] else ""))
    print(f"\n{len(rep) - len(bad)}/{len(rep)} attested examples behave as documented")
    return 1 if bad else 0


_COMMANDS = {"check": _cmd_check, "lookup": _cmd_lookup, "matrix": _cmd_matrix, "rules": _cmd_rules, "examples": _cmd_examples}


def main(argv: Optional[list[str]] = None) -> int:
    ap = _build_parser()
    args = ap.parse_args(argv)
    return _COMMANDS[args.cmd](args, load_ruleset(), ap)


if __name__ == "__main__":
    sys.exit(main())

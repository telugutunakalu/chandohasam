# -*- coding: utf-8 -*-
"""
Command line: ``python3 -m indic_meter_dawg <command>``.

  identify  LINE [LINE ...] | --file F     identify a stanza (one line per argument or file line)
            --text                         … from Telugu text instead of U/I (scans first)
  scan      LINE [LINE ...] | --file F     guru/laghu marking of Telugu text
  walk      LINE                           accept labels and death points of one line
  prefix    PREFIX                          hypotheses that can still complete
  grammar   METER [--level poem|line|flat|strict] [--slot S]   print a grammar
  grammars  [--out DIR]                     write every .rlg file
  docs      [--out DIR]                     write the plain-language docs
  diagrams  [--out DIR] [--no-svg]          write DOT/Mermaid/SVG diagrams
  stats                                     headline numbers of the DAWG
  enumerate METER SLOT [--limit N]          list the slot's lines
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from . import automaton as au
from . import docs as docs_mod
from .prosody import (prosodic_grammar as build_prosodic_grammar, flatten as flatten_poem, prosodic_automaton,
                           format_prosodic_grammar, random_poem, derivation_steps)
from . import render
from .builder import default_dawg
from .grammar import format_grammar, format_grammar_grouped, to_strict
from .identify import identify, identify_text
from .scansion import DEFAULT_POLICY, ScanPolicy, scan
from .walker import viable_prefix, walk

HERE = Path(__file__).resolve().parent.parent   # meter_engine/


def _read_lines(args) -> list[str]:
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
        return [ln for ln in text.splitlines() if ln.strip()]
    return list(args.lines)


def _policy(args) -> ScanPolicy:
    return ScanPolicy(word_initial_conjunct=getattr(args, "word_initial_conjunct", None) or DEFAULT_POLICY.word_initial_conjunct,
                      repha_conjunct=getattr(args, "repha_conjunct", None) or DEFAULT_POLICY.repha_conjunct)


def cmd_identify(args) -> int:
    lines = _read_lines(args)
    if not lines:
        print("no lines given", file=sys.stderr)
        return 2
    if args.text:
        res = identify_text(lines, policy=_policy(args), try_variants=not args.no_variants,
                            final_laghu_as_guru=not args.no_padanta, include_parents=not args.no_parents)
    else:
        res = identify(lines, final_laghu_as_guru=not args.no_padanta, include_parents=not args.no_parents)
    print(res.to_json() if args.json else res.explain())
    return 0 if res.identified else 1


def cmd_scan(args) -> int:
    lines = _read_lines(args)
    if not lines:
        print("no lines given", file=sys.stderr)
        return 2
    scans = scan(lines, _policy(args))
    if args.json:
        print(json.dumps([s.to_dict() for s in scans], ensure_ascii=False, indent=2))
        return 0
    for i, s in enumerate(scans, start=1):
        print(f"{i}. {s.format()}")
        if args.rules:
            for syl in s.syllables:
                print(f"     {syl.text:6s} {syl.weight}  {', '.join(syl.rules)}" + (f"  [vikalpa: {syl.vikalpa}]" if syl.vikalpa else ""))
    return 0


def cmd_walk(args) -> int:
    w = walk(args.line, final_laghu_as_guru=not args.no_padanta)
    if args.json:
        print(json.dumps({"line": w.line, "accepted": sorted(map(list, w.accepted)),
                          "padanta_accepted": sorted(map(list, w.padanta_accepted)),
                          "died": {f"{m}/{s}": i for (m, s), i in sorted(w.died.items())}}, ensure_ascii=False, indent=2))
        return 0
    print(f"line: {w.line} ({len(w.line)} aksharas)")
    print("accepted:", ", ".join(f"{m}/{s}" for m, s in sorted(w.accepted)) or "–")
    print("accepted with pādānta laghu→guru:", ", ".join(f"{m}/{s}" for m, s in sorted(w.padanta_accepted)) or "–")
    for (m, s), i in sorted(w.died.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  died: {m}/{s} at akshara {i + 1}" if i < len(w.line) else f"  died: {m}/{s} (line too short)")
    return 0


def cmd_prefix(args) -> int:
    hs = viable_prefix(args.prefix)
    print(", ".join(f"{m}/{s}" for m, s in sorted(hs)) or "– (no meter can complete this prefix)")
    return 0


def cmd_grammar(args) -> int:
    d = default_dawg()
    spec = d.spec(args.meter)
    level = "strict" if args.strict else args.level
    if level == "poem":
        print(f"# {spec.name_te} · {spec.name} — prosodic grammar")
        print(format_prosodic_grammar(build_prosodic_grammar(spec, d)))
        return 0
    if level == "flat":
        print(f"# {spec.name} — whole poem, right-linear over {{U, I, ⏎}}")
        print(format_grammar_grouped(flatten_poem(spec, d)))
        return 0
    for slot in ([args.slot] if args.slot else list(spec.slots)):
        g = d.grammars[(spec.name, slot)]
        print(f"# {spec.name} / {slot}")
        print(format_grammar(to_strict(g)) if level == "strict" else format_grammar_grouped(g))
        print()
    return 0


def cmd_grammars(args) -> int:
    files = docs_mod.write_grammars(args.out or HERE / "grammars")
    print(f"wrote {len(files)} grammar files to {Path(files[0]).parent}")
    return 0


def cmd_docs(args) -> int:
    files = docs_mod.write_docs(args.out or HERE / "docs" / "grammars")
    print(f"wrote {len(files)} doc pages to {Path(files[0]).parent}")
    return 0


def cmd_diagrams(args) -> int:
    files = render.write_diagrams(args.out or HERE / "diagrams", svg=not args.no_svg)
    svgs = sum(1 for f in files if f.suffix == ".svg")
    print(f"wrote {len(files)} files ({svgs} svg) under {Path(args.out or HERE / 'diagrams')}")
    if not args.no_svg and not render.dot_available():
        print("graphviz 'dot' not found: svg files skipped", file=sys.stderr)
    return 0


def cmd_stats(args) -> int:
    st = default_dawg().stats()
    print(json.dumps(st, indent=2) if args.json else "\n".join(f"{k:26s} {v}" for k, v in st.items()))
    return 0


def cmd_enumerate(args) -> int:
    d = default_dawg()
    dfa = d.slot_dfas[(args.meter, args.slot)]
    n = 0
    for s, _ in au.enumerate_language(dfa):
        print(s)
        n += 1
        if args.limit and n >= args.limit:
            break
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="indic_meter_dawg", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("identify", help="identify the meter of a stanza")
    s.add_argument("lines", nargs="*", help="guru/laghu lines (U/I, గ/ల, -/u ...)")
    s.add_argument("--file", help="read lines from a file instead")
    s.add_argument("--json", action="store_true")
    s.add_argument("--no-padanta", action="store_true", help="do not read a line-final laghu as guru")
    s.add_argument("--no-parents", action="store_true", help="hide a parent meter when its variant matches")
    s.add_argument("--text", action="store_true", help="the lines are Telugu text: scan them to U/I first")
    s.add_argument("--no-variants", action="store_true", help="with --text: do not try alternative (vikalpa) readings")
    s.add_argument("--word-initial-conjunct", choices=["laghu", "guru"], dest="word_initial_conjunct")
    s.add_argument("--repha-conjunct", choices=["laghu", "guru"], dest="repha_conjunct")
    s.set_defaults(fn=cmd_identify)

    s = sub.add_parser("scan", help="guru/laghu marking of Telugu text")
    s.add_argument("lines", nargs="*", help="Telugu lines")
    s.add_argument("--file", help="read lines from a file instead")
    s.add_argument("--json", action="store_true")
    s.add_argument("--rules", action="store_true", help="show which rule made each akshara guru")
    s.add_argument("--word-initial-conjunct", choices=["laghu", "guru"], dest="word_initial_conjunct")
    s.add_argument("--repha-conjunct", choices=["laghu", "guru"], dest="repha_conjunct")
    s.set_defaults(fn=cmd_scan)

    s = sub.add_parser("walk", help="accept labels of one line")
    s.add_argument("line")
    s.add_argument("--json", action="store_true")
    s.add_argument("--no-padanta", action="store_true")
    s.set_defaults(fn=cmd_walk)

    s = sub.add_parser("prefix", help="hypotheses alive after a prefix")
    s.add_argument("prefix")
    s.set_defaults(fn=cmd_prefix)

    s = sub.add_parser("grammar", help="print a meter's grammar")
    s.add_argument("meter")
    s.add_argument("--level", choices=["poem", "line", "flat", "strict"], default="poem",
                   help="poem = hierarchical prosodic grammar (default); line = per-slot right-linear; "
                        "flat = whole poem right-linear; strict = one symbol per production")
    s.add_argument("--slot", help="restrict line/strict output to one slot")
    s.add_argument("--strict", action="store_true", help="same as --level strict")
    s.set_defaults(fn=cmd_grammar)

    for name, fn, helptext in (("grammars", cmd_grammars, "write .rlg files"),
                               ("docs", cmd_docs, "write the plain-language docs")):
        s = sub.add_parser(name, help=helptext)
        s.add_argument("--out")
        s.set_defaults(fn=fn)

    s = sub.add_parser("diagrams", help="write diagrams")
    s.add_argument("--out")
    s.add_argument("--no-svg", action="store_true")
    s.set_defaults(fn=cmd_diagrams)

    s = sub.add_parser("stats", help="DAWG statistics")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_stats)

    s = sub.add_parser("enumerate", help="list every line of a (meter, slot)")
    s.add_argument("meter")
    s.add_argument("slot")
    s.add_argument("--limit", type=int, default=0)
    s.set_defaults(fn=cmd_enumerate)
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""
Diagrams as text: Graphviz DOT and Mermaid.

* rule card per meter — a railroad-style row of gana nodes per slot, yati
  nodes highlighted, footer with the stanza facts;
* the vritta trie — all fixed meters as one prefix tree, tails collapsed
  from the akshara where a meter becomes unique;
* any DFA — for the per-slot acceptors and the family views.

Owns: text generation only. No files are written here (see render.py).
"""
from __future__ import annotations

from typing import Iterable, Optional

from . import automaton as au
from . import symbols
from .builder import LineDawg
from .catalogue import MeterSpec
from .ganas import Gana

YATI_FILL = "#ffe082"
GANA_FILL = "#f4f4f4"
FIXED_FILL = "#e3f2fd"
FONT = "Helvetica,Arial,sans-serif"


def _esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _gana_lines(ganas: Iterable[Gana], per_line: int = 2) -> list[str]:
    items = [f"{g.telugu} {g.pattern}" for g in ganas]
    return ["  ·  ".join(items[i:i + per_line]) for i in range(0, len(items), per_line)]


def _yati_gana_indices(spec: MeterSpec, slot: str, ganas_per_pos) -> dict[int, str]:
    """Which gana positions carry a yati mark and the mark's text."""
    marks: dict[int, str] = {}
    if spec.is_fixed:
        pos = 1
        for k, ganas in enumerate(ganas_per_pos, start=1):
            length = len(ganas[0].pattern)
            for a in spec.yati_aksharas.get(slot, ()):
                if pos <= a < pos + length:
                    marks[k] = f"యతి @ akshara {a}"
            pos += length
    else:
        for k in spec.yati_ganas.get(slot, ()):
            marks[k] = "యతి (gana start)"
    return marks


def _footer(spec: MeterSpec) -> str:
    lo, hi = spec.aksharalu
    span = f"{lo}" if lo == hi else f"{lo}–{hi}"
    bits = [
        f"{spec.name_te}  ·  {spec.name}  ·  {spec.family}",
        f"{spec.padalu} lines per unit, slot pattern: {' | '.join(' '.join(p) for p in spec.slot_patterns)}"
        + ("  (repeatable)" if spec.repeatable else ""),
        f"aksharas per line: {span}  ·  prāsa: {'yes' if spec.prasa else 'no'}"
        f"  ·  prāsa-yati: {'allowed' if spec.prasa_yati else 'no'}",
    ]
    if spec.is_variant_of:
        bits.append(f"variant of {spec.is_variant_of}")
    if spec.followed_by:
        bits.append("followed by: " + " / ".join(spec.followed_by))
    for c in spec.stanza_constraints:
        bits.append(f"stanza rule: {c.rule}")
    return "\\n".join(_esc(b) for b in bits)


def rule_card_dot(spec: MeterSpec, dawg: LineDawg) -> str:
    """Graphviz rule card for one meter.

    >>> from .builder import default_dawg
    >>> d = default_dawg(); s = rule_card_dot(d.spec("tetagiti"), d)
    >>> s.startswith('digraph "tetagiti"') and "యతి" in s
    True
    """
    out = [f'digraph "{_esc(spec.name)}" {{',
           f'  rankdir=LR; fontname="{FONT}"; labelloc=b; fontsize=11;',
           f'  label="{_footer(spec)}";',
           f'  node [shape=box, style="rounded,filled", fontname="{FONT}", fontsize=10, fillcolor="{GANA_FILL}"];',
           '  edge [color="#607d8b", arrowsize=0.7];']
    for slot in spec.slots:
        g = dawg.grammars[(spec.name, slot)]
        marks = _yati_gana_indices(spec, slot, g.gana_positions)
        out.append(f'  subgraph "cluster_{_esc(slot)}" {{')
        out.append(f'    label="slot {_esc(slot)}  (lines {", ".join(str(i) for i in sorted({i + 1 for p in spec.slot_patterns for i, s in enumerate(p) if s == slot}))})"; '
                   'style="rounded,dashed"; color="#90a4ae"; fontsize=10;')
        out.append(f'    "{slot}_start" [shape=circle, label="", width=0.18, fillcolor="#37474f"];')
        out.append(f'    "{slot}_end" [shape=doublecircle, label="", width=0.18, fillcolor="#37474f"];')
        prev = f"{slot}_start"
        for k, ganas in enumerate(g.gana_positions, start=1):
            nid = f"{slot}_G{k}"
            body = "\\n".join(_esc(x) for x in _gana_lines(ganas))
            title = f"G{k}"
            fill = FIXED_FILL if len(ganas) == 1 else GANA_FILL
            extra = ""
            if k in marks:
                fill = YATI_FILL
                extra = f"\\n◆ {_esc(marks[k])}"
            out.append(f'    "{nid}" [label="{title}\\n{body}{extra}", fillcolor="{fill}"];')
            out.append(f'    "{prev}" -> "{nid}";')
            prev = nid
        out.append(f'    "{prev}" -> "{slot}_end";')
        out.append("  }")
    out.append("}")
    return "\n".join(out)


def rule_card_mermaid(spec: MeterSpec, dawg: LineDawg) -> str:
    """Mermaid flowchart with the same content as :func:`rule_card_dot`.

    >>> from .builder import default_dawg
    >>> d = default_dawg(); rule_card_mermaid(d.spec("vidyunmala"), d).splitlines()[0]
    'flowchart LR'
    """
    out = ["flowchart LR"]
    for slot in spec.slots:
        g = dawg.grammars[(spec.name, slot)]
        marks = _yati_gana_indices(spec, slot, g.gana_positions)
        out.append(f'  subgraph {slot}["slot {slot}"]')
        out.append("    direction LR")
        prev = f"{slot}_start"
        out.append(f"    {prev}(( ))")
        for k, ganas in enumerate(g.gana_positions, start=1):
            nid = f"{slot}_G{k}"
            body = "<br/>".join(x.replace("·", "/") for x in _gana_lines(ganas))
            mark = f"<br/>◆ {marks[k]}" if k in marks else ""
            out.append(f'    {nid}["G{k}<br/>{body}{mark}"]')
            out.append(f"    {prev} --> {nid}")
            prev = nid
        out.append(f"    {slot}_end((( )))")
        out.append(f"    {prev} --> {slot}_end")
        out.append("  end")
    yati_nodes = [f"{slot}_G{k}" for slot in spec.slots
                  for k in _yati_gana_indices(spec, slot, dawg.grammars[(spec.name, slot)].gana_positions)]
    out.append(f"  classDef yati fill:{YATI_FILL},stroke:#f9a825;")
    if yati_nodes:
        out.append("  class " + ",".join(yati_nodes) + " yati;")
    return "\n".join(out)


# --------------------------------------------------------------------------
# vritta trie
# --------------------------------------------------------------------------
def fixed_patterns(dawg: LineDawg) -> dict[str, str]:
    """meter name -> its single line pattern, for every fixed meter."""
    out = {}
    for spec in dawg.catalogue.concrete:
        if spec.is_fixed:
            g = dawg.grammars[(spec.name, "all")]
            out[spec.name] = "".join(x[0].pattern for x in g.gana_positions)
    return out


def unique_from(patterns: dict[str, str]) -> dict[str, int]:
    """For each meter, the length of its shortest prefix that no *other*
    pattern continues past (a pattern that is a proper prefix of another is
    "complete", not "continuing", so it does not block).

    >>> unique_from({"a": "UUI", "b": "UIU", "c": "III"})
    {'a': 2, 'b': 2, 'c': 1}
    """
    out = {}
    for name, pat in patterns.items():
        others = [p for n, p in patterns.items() if n != name]
        k = 0
        while any(o[:k] == pat[:k] and (len(o) > k or len(o) == len(pat)) for o in others) and k < len(pat):
            k += 1
        out[name] = k if k else 1
    return out


def vritta_trie_dot(dawg: LineDawg) -> str:
    """The prefix tree of every fixed meter; a meter's tail after the point
    where it becomes unique is collapsed into one labelled node.

    >>> from .builder import default_dawg
    >>> "utpalamala" in vritta_trie_dot(default_dawg())
    True
    """
    pats = fixed_patterns(dawg)
    uniq = unique_from(pats)
    out = ['digraph "vritta_trie" {',
           f'  rankdir=LR; fontname="{FONT}"; labelloc=t; fontsize=12;',
           f'  label="Fixed (vritta) meters as one trie over U/I — {len(pats)} meters; a tail is collapsed from the akshara where the meter is unique";',
           f'  node [shape=circle, style=filled, fillcolor="{GANA_FILL}", fontname="{FONT}", fontsize=9, width=0.3, fixedsize=true, label=""];',
           '  edge [fontname="Helvetica", fontsize=10];',
           '  "" [shape=point];']
    seen: set[str] = set()
    for name, pat in sorted(pats.items(), key=lambda kv: kv[1]):
        k = uniq[name]
        shared = pat[:k]
        prev = ""
        for i in range(1, len(shared) + 1):
            node = shared[:i]
            if node not in seen:
                seen.add(node)
                style = "" if i < k else f', shape=box, fixedsize=false, style="rounded,filled", fillcolor="{FIXED_FILL}", label="{_esc(dawg.spec(name).name_te)}\\n{_esc(name)}\\nunique at akshara {k} of {len(pat)}\\n{_esc(pat[k:] or "(end)")}"'
                out.append(f'  "{node}" [{style.lstrip(", ")}];' if style else f'  "{node}";')
                out.append(f'  "{prev}" -> "{node}" [label="{node[-1]}"];')
            prev = node
    out.append("}")
    return "\n".join(out)


# --------------------------------------------------------------------------
# generic DFA
# --------------------------------------------------------------------------
def dfa_dot(dfa: au.Dfa, title: str = "", show_labels: bool = False, max_states: int = 400) -> str:
    """Graphviz picture of a DFA: circles, accepting = double circle, guru
    edges solid, laghu edges dashed, edge label = symbol (matra weight in
    parentheses).

    >>> from .builder import default_dawg
    >>> d = default_dawg(); s = dfa_dot(d.slot_dfas[("vidyunmala", "all")], "vidyunmala")
    >>> s.count("->")                  # 8 transitions + the start arrow
    9
    """
    out = [f'digraph "{_esc(title) or "dfa"}" {{', f'  rankdir=LR; fontname="{FONT}"; labelloc=t;',
           f'  label="{_esc(title)}  ·  {dfa.n_states} states, {dfa.n_edges} edges";',
           f'  node [shape=circle, style=filled, fillcolor="{GANA_FILL}", fontname="{FONT}", fontsize=9];',
           '  edge [fontname="Helvetica", fontsize=9];', '  "__start" [shape=point];', f'  "__start" -> "{dfa.start}";']
    if dfa.n_states > max_states:
        out.append(f'  "too_big" [shape=box, label="{dfa.n_states} states: too many to draw (limit {max_states})"];')
        out.append("}")
        return "\n".join(out)
    for s in range(dfa.n_states):
        labs = dfa.labels.get(s, frozenset())
        if labs:
            text = "\\n".join(sorted(str(l) for l in labs)) if show_labels else str(s)
            out.append(f'  "{s}" [shape=doublecircle, label="{_esc(text)}"];')
        else:
            out.append(f'  "{s}" [label="{s}"];')
    for e in dfa.edges():
        style = "solid" if e.symbol == symbols.GURU else "dashed"
        out.append(f'  "{e.src}" -> "{e.dst}" [label="{e.symbol} ({e.weight})", style={style}];')
    out.append("}")
    return "\n".join(out)


# --------------------------------------------------------------------------
# index page
# --------------------------------------------------------------------------
def index_markdown(dawg: LineDawg, stats: Optional[dict] = None) -> str:
    """Markdown table of every meter with links to its card and doc page."""
    stats = stats or dawg.stats()
    rows = ["# Meter diagrams", "",
            f"Built from `meter_rules.yaml` — {stats['meters']} meters, {stats['hypotheses']} line slots, "
            f"{stats['dfa_states']} DAWG states, {stats['distinct_lines']:,} distinct legal lines.", "",
            "Overview: [vritta trie](vritta_trie.svg) · [primer on the grammars](../docs/grammars/README.md)", "",
            "| id | meter | family | lines | slot pattern | aksharas | yati | prāsa | lines in language | card | grammar doc |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    for spec in dawg.catalogue.meters:
        if spec.abstract:
            rows.append(f"| {spec.id} | {spec.name_te} `{spec.name}` | {spec.family} | – | family entry | – | – | – | – | – | – |")
            continue
        lo, hi = spec.aksharalu
        span = f"{lo}" if lo == hi else f"{lo}–{hi}"
        yati = "; ".join(f"{s}: " + (",".join(map(str, spec.yati_for(s))) or "–") for s in spec.slots)
        yati += " (akshara)" if spec.is_fixed else " (gana)"
        sizes = "; ".join(f"{s}: {au.count_paths(dawg.slot_dfas[(spec.name, s)]):,}" for s in spec.slots)
        prasa = "yes" if spec.prasa else ("prāsa-yati" if spec.prasa_yati else "no")
        rows.append(f"| {spec.id} | {spec.name_te} `{spec.name}` | {spec.family} | {spec.padalu}"
                    f"{' (repeat)' if spec.repeatable else ''} | {' '.join(spec.slot_pattern)} | {span} | {yati} | {prasa} | "
                    f"{sizes} | [svg](meters/{spec.name}.svg) · [mermaid](meters/{spec.name}.md) | "
                    f"[doc](../docs/grammars/{spec.name}.md) |")
    return "\n".join(rows) + "\n"

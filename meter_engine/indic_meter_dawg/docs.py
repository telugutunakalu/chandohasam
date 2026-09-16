# -*- coding: utf-8 -*-
"""
Plain-language documentation of every meter's grammar, plus the grammar
files themselves (``.rlg``) and a primer.

Owns: markdown/text generation and writing for docs and grammars.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from . import automaton as au
from . import symbols
from .builder import LineDawg, default_dawg
from .catalogue import MeterSpec
from .constraints import describe as describe_constraint
from .ganas import GanaRegistry
from .grammar import Grammar, canonical_line, derivation, format_grammar, format_grammar_grouped, to_strict
from .prosody import (prosodic_grammar as build_prosodic_grammar, flatten as flatten_poem, prosodic_automaton,
                           format_prosodic_grammar, random_poem, derivation_steps)

CLASS_WORDS = {
    "surya": ("a సూర్యగణము (surya gana)", "the two 3-matra ganas"),
    "indra": ("an ఇంద్రగణము (indra gana)", "the six 4- or 5-matra ganas"),
    "chandra": ("a చంద్రగణము (chandra gana)", "the extended ganas"),
    "kanda": ("a కంద గణము (kanda gana)", "the five 4-matra ganas"),
}


def _list(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " or " + items[-1]


def describe_token(token: str, registry: GanaRegistry) -> str:
    """Plain words for a catalogue gana token.

    >>> from .ganas import load_registry
    >>> describe_token("surya", load_registry())
    'a సూర్యగణము (surya gana): న III or హ UI'
    >>> describe_token("భ", load_registry())
    'భ (bha) UII'
    """
    ganas = registry.resolve(token)
    members = _list([f"{g.telugu} {g.pattern}" for g in ganas])
    if token.startswith("all_laghu("):
        inner = token[len("all_laghu("):-1]
        return f"the all-laghu member of {inner}: {members}"
    if token.startswith("m") and token[1:].isdigit():
        return f"any syllable group worth {token[1:]} matras: {members}"
    if token in CLASS_WORDS:
        return f"{CLASS_WORDS[token][0]}: {members}"
    g = ganas[0]
    return f"{g.telugu} ({g.name}) {g.pattern}"


def _ordinal(n: int) -> str:
    return {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh",
            8: "eighth", 9: "ninth", 10: "tenth"}.get(n, f"{n}th")


def _recipe(spec: MeterSpec, slot: str, grammar: Grammar, registry: GanaRegistry) -> list[str]:
    tokens = spec.slots[slot]
    lines = []
    for k, (tok, allowed) in enumerate(zip(tokens, grammar.gana_positions), start=1):
        base = describe_token(tok, registry)
        full = registry.resolve(tok)
        if len(allowed) < len(full):
            narrowed = _list([f"{g.telugu} {g.pattern}" for g in allowed])
            base += f" — but here only {narrowed} (a constraint removes the rest)"
        lines.append(f"{k}. {base}")
    return lines


def _slot_lines(spec: MeterSpec, slot: str) -> str:
    idx = [str(i) for i in sorted({i + 1 for p in spec.slot_patterns for i, s in enumerate(p) if s == slot})]
    if spec.repeatable:
        return "line " + ", ".join(idx) + " of every unit"
    return "line " + ", ".join(idx)


def meter_doc_markdown(spec: MeterSpec, dawg: LineDawg) -> str:
    """The "dumbed down" page for one meter."""
    reg = dawg.registry
    lo, hi = spec.aksharalu
    span = f"exactly {lo}" if lo == hi else f"between {lo} and {hi}"
    md = [f"# {spec.name_te} · {spec.name}", "",
          f"*{spec.family}* · {spec.padalu} lines{' per unit, repeatable' if spec.repeatable else ''} · "
          f"{span} aksharas per line · prāsa {'required' if spec.prasa else 'not required'}"
          f"{' · prāsa-yati allowed' if spec.prasa_yati else ''}", ""]
    if spec.is_variant_of:
        md += [f"A variant of **{spec.is_variant_of}**: the same rules, with the restriction described below.", ""]
    if spec.udaharana:
        md += ["Example from the catalogue:", "", f"> {spec.udaharana.strip()}", ""]

    # ---- the poem as a grammar
    pg = build_prosodic_grammar(spec, dawg)
    md += ["## The prosodic grammar", "",
           "Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; "
           "a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed "
           "to generate every valid stanza of this meter.", "", "```", format_prosodic_grammar(pg), "```", ""]
    legend = ["`⏎` — line separator (a terminal, like `U` and `I`);",
              "`|` — alternatives; a comment after `#` explains the rule;"]
    if any("−" in nt or "=" in nt or "$" in nt for nt in pg.levels["class"]):
        legend.append("`Kanda−జ` — the class *minus* జ (a constraint removed it); `Kanda=జ|నల` — only జ or నల allowed "
                      "there; `Kanda$U` — only members ending in a guru;")
    if any("⟨" in nt for nt in pg.levels["poem"]):
        legend.append("`Poem⟨U⟩` / `Kanda⟨U⟩` — the copy of the grammar in which every line starts with a guru; "
                      "the stanza rule (uniform first akshara) becomes two branches instead of a side condition;")
    if spec.repeatable:
        legend.append("`Poem → Unit | Unit ⏎ Poem` — the poem is any number of units (right recursion keeps it regular);")
    md += ["Legend:", ""] + [f"- {x}" for x in legend] + [""]

    # ---- in one sentence
    md += ["## In one sentence", ""]
    if spec.is_fixed:
        g = dawg.grammars[(spec.name, "all")]
        pat = canonical_line(g)
        names = " ".join(x[0].telugu for x in g.gana_positions)
        md += [f"Every line is the same fixed sequence of {len(g.gana_positions)} ganas, **{names}**, "
               f"i.e. the {len(pat)}-akshara pattern `{pat}`. There is no choice anywhere in the line; "
               f"the four lines are identical in weight."]
    else:
        parts = []
        for slot in spec.slots:
            n = len(spec.slots[slot])
            where = ("every line" if len(spec.slots) == 1
                     else f"a line of slot *{slot}*" if spec.alt_slot_patterns else _slot_lines(spec, slot))
            parts.append(f"{where} has {n} ganas ({', '.join(spec.slots[slot])})")
        md += ["; ".join(parts).capitalize() + ". Each gana is chosen from a class, so the line length varies."]
    md += [""]

    # ---- rules
    md += ["## The rules, one by one", ""]
    n = 1
    unit = "unit" if spec.repeatable else "stanza"
    md += [f"{n}. **Line count.** A {unit} has {spec.padalu} lines"
           + (f"; a poem is any number of such units in a row." if spec.repeatable else ".")]
    n += 1
    if spec.alt_slot_patterns:
        forms = " or ".join(f"*{' '.join(p)}*" for p in spec.slot_patterns)
        md += [f"{n}. **Alternative stanza forms.** The lines follow {forms}; one stanza keeps one form "
               "throughout, the forms are never mixed."]
        n += 1
    elif len(spec.slots) > 1:
        md += [f"{n}. **Two kinds of line.** Lines follow the pattern {' '.join(spec.slot_pattern)}: "
               + "; ".join(f"slot *{s}* is {_slot_lines(spec, s)}" for s in spec.slots) + "."]
        n += 1
    for slot in spec.slots:
        g = dawg.grammars[(spec.name, slot)]
        head = "Line recipe" if len(spec.slots) == 1 else f"Recipe for slot *{slot}*"
        md += [f"{n}. **{head}.** In order:"]
        md += ["    " + r for r in _recipe(spec, slot, g, reg)]
        n += 1
    for c in spec.constraints:
        why = f" *({c.why})*" if c.why else ""
        md += [f"{n}. **Constraint.** {describe_constraint(c).capitalize()}.{why}"]
        n += 1
    for c in spec.stanza_constraints:
        why = f" *({c.why})*" if c.why else ""
        md += [f"{n}. **Stanza rule.** {describe_constraint(c).capitalize()}.{why} The identifier reports a "
               "breach of this rule as a violation rather than rejecting the stanza (Pothana 3-151 and 3-616 "
               "are otherwise valid kandas that break it); the prosodic grammar below keeps the rule as written."]
        n += 1
    # yati
    if spec.is_fixed:
        ys = spec.yati_aksharas.get("all", ())
        if ys:
            md += [f"{n}. **Yati.** The akshara at position {_list([str(y) for y in ys])} must be in yati-maitri "
                   f"(sound agreement) with the first akshara of the line. The grammar only *locates* this "
                   f"position; the sound check is a separate engine."]
        else:
            md += [f"{n}. **Yati.** This meter prescribes no yati."]
    else:
        bits = []
        for slot in spec.slots:
            ks = spec.yati_ganas.get(slot, ())
            where = "" if len(spec.slots) == 1 else f" in slot *{slot}*"
            bits.append((f"at the first akshara of gana {_list([str(k) for k in ks])}{where}") if ks
                        else f"none{where}")
        md += [f"{n}. **Yati.** " + "; ".join(bits) + ". Because gana lengths vary, the akshara index of the "
               "yati depends on the ganas actually used; the parser reports it per line."]
    n += 1
    md += [f"{n}. **Prāsa.** " + ("The second akshara of every line must rhyme (checked by the prāsa engine, not here)."
                                  if spec.prasa else "Not required."
                                  + (" Prāsa-yati (rhyme at the yati position) is allowed instead of yati-maitri." if spec.prasa_yati else ""))]
    n += 1
    md += [f"{n}. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier)."]
    n += 1
    if spec.halves_per_line > 1:
        md += [f"{n}. **Printing.** Each pada is conventionally printed as {spec.halves_per_line} half-lines; "
               f"the identifier joins them, so a {spec.padalu * spec.halves_per_line}-line text is read as "
               f"{spec.padalu} padas."]
        n += 1
    if spec.followed_by:
        md += [f"{n}. **What follows.** The stanza is normally followed by a {' or '.join(spec.followed_by)} "
               f"(the gīta), identified separately."]
        n += 1
    if spec.notes:
        md += ["", f"Note: {spec.notes}"]
    md += [""]

    # ---- right-linear form
    fl = flatten_poem(spec, dawg)
    stp = to_strict(fl)
    md += ["## The same grammar, right-linear (what the automaton is built from)", "",
           "A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. "
           "Flattening the hierarchy above gives one such grammar for the whole poem. "
           "`L2.G3` = \"line 2, about to read gana 3\". The last gana of a line emits `⏎` and hands over to the "
           "next line; the last gana of the last line ends the poem"
           + (" — or, for this repeatable meter, emits `⏎` and returns to `L1.G1`." if spec.repeatable else ".")
           + (" `⟨U⟩L1.G2` is the same state inside the all-lines-start-with-U branch." if any("⟨" in n for n in fl.nonterminals) else "")
           + (" `F1.` / `F2.` prefix the states of the two stanza forms." if spec.alt_slot_patterns else ""),
           "", "```", format_grammar_grouped(fl), "```", ""]
    md += ["### Strict form (one symbol per production = one automaton edge)", "",
           "Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal "
           "`A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: "
           "line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. "
           f"First productions (all {len(stp.productions)}, each with such a comment, are in "
           f"[`grammars/{spec.name}.rlg`](../../grammars/{spec.name}.rlg)):", "", "```",
           format_grammar(gr_slice(stp, 8)), "…", "```", "",
           f"The strict grammar has {len(stp.nonterminals) + 1} states; minimized, the prosodic automaton has "
           f"{prosodic_automaton(spec.name).n_states} states.", ""]

    # ---- worked derivation
    md += ["## One worked derivation", ""]
    rng = __import__("random").Random(spec.id)
    lines = random_poem(pg, rng, max_units=1)
    steps = derivation_steps(pg, lines) or []
    shown = steps[:10] + (["…"] if len(steps) > 11 else []) + (steps[-1:] if len(steps) > 10 else [])
    md += [f"A poem of {len(lines)} lines, derived top-down from `Poem` ({len(steps) - 1} rewriting steps; "
           "the leftmost nonterminal is rewritten each time):", "", "```"]
    md += [f"⇒ {s}" if i else s for i, s in enumerate(shown)]
    md += ["```", "", "The result, one line per row:", "", "```"] + lines + ["```", ""]

    # ---- what is not checked
    md += ["## What this grammar does not check", "",
           "- the *sounds* at the yati positions (yati-maitri) — only their location;",
           "- prāsa (the second-akshara rhyme);",
           "- the scansion itself: the grammar trusts the U/I string it is given;",
           "- meaning, sandhi, word boundaries.", ""]

    # ---- numbers
    md += ["## Numbers", "", "| slot | ganas | aksharas | distinct lines | DFA states |", "|---|---|---|---|---|"]
    for slot in spec.slots:
        d = dawg.slot_dfas[(spec.name, slot)]
        g = dawg.grammars[(spec.name, slot)]
        lo_s = sum(min(len(x.pattern) for x in a) for a in g.gana_positions)
        hi_s = sum(max(len(x.pattern) for x in a) for a in g.gana_positions)
        span_s = f"{lo_s}" if lo_s == hi_s else f"{lo_s}–{hi_s}"
        md += [f"| {slot} | {len(g.gana_positions)} | {span_s} | {au.count_paths(d):,} | {d.n_states} |"]
    md += ["", f"Whole-prosodic automaton (over U, I, ⏎): {prosodic_automaton(spec.name).n_states} states.",
           "", f"Grammar file: [`grammars/{spec.name}.rlg`](../../grammars/{spec.name}.rlg)."]
    md += ["", f"Diagram: [rule card](../../diagrams/meters/{spec.name}.svg) · "
               f"[mermaid](../../diagrams/meters/{spec.name}.md) · "
               + " · ".join(f"[DFA {s}](../../diagrams/dfa/{spec.name}__{s}.svg)" for s in spec.slots), ""]
    return "\n".join(md)


def primer_markdown(dawg: LineDawg) -> str:
    reg = dawg.registry
    md = ["# Reading the meter grammars", "",
          "Every Telugu meter in `meter_rules.yaml` is written here as a **right-linear grammar** over two "
          "letters: `U` (guru, a heavy syllable, 2 matras) and `I` (laghu, a light syllable, 1 matra). "
          "This page explains the notation once; each meter then has its own page.", "",
          "## What a grammar is", "",
          "A grammar is a list of rewriting rules. Start from `Poem` and keep replacing a nonterminal by "
          "the right-hand side of one of its rules until only the terminals `U`, `I` and `⏎` remain. Every "
          "text you can reach this way is a legal poem of the meter; nothing else is.", "",
          "```", "Poem  → Line ⏎ Line ⏎ Line ⏎ Line        # four lines separated by ⏎",
          "Line  → Surya Indra Indra Surya Surya   # five ganas, by class",
          "Surya → న | హ                           # a class is a choice of ganas",
          "న     → I I I                           # a gana is its symbols", "```", "",
          "`|` separates alternatives; a comment after `#` explains the rule. Four levels: poem, lines, "
          "gana classes, ganas. A constraint that removes a gana at one position shows up in the class name "
          "(`Kanda−జ`), and a stanza-wide rule shows up as two branches of `Poem` (`Poem⟨U⟩ | Poem⟨I⟩`).", "",
          "## From the hierarchy to a right-linear grammar", "",
          "The hierarchy is only for reading. Because no nonterminal calls itself except `Poem` (and only at "
          "the far right, `Poem → Unit ⏎ Poem`, for repeatable meters), the whole thing flattens into one "
          "**right-linear** grammar: `L1.G1 → III L1.G2 | UI L1.G2`, …, `L1.G5 → III⏎ L2.G1`, …, `L4.G5 → III`. "
          "Each meter's page shows both, and the `.rlg` file shows the strict form too, where `A_UUI_2` "
          "means *inside alternative UUI of A, two symbols already read*.", "",
          "## Why right-linear", "",
          "In the flattened form every rule has the nonterminal, if any, as the **last** thing on the right (`A → wB` or `A → w`). "
          "Grammars of that shape generate exactly the regular languages, and they are finite automata in "
          "disguise: nonterminal = state, `A → aB` = an edge labelled `a`, `A → a` = an edge into the "
          "accept state. The strict form (`.rlg` files, second half) makes that one-to-one: one letter per rule.", "",
          "Because the automaton of every meter is regular, the union of all of them is regular too, and a "
          "single minimized deterministic automaton — the **DAWG** (directed acyclic word graph; acyclic "
          "because every line has bounded length) — recognises every meter at once. Each edge carries the "
          "matra weight of its letter, so a path's weight is the line's matra count.", "",
          "## How the identifier uses it", "",
          "1. Each line is walked through the DAWG; the accepting state says which (meter, slot) pairs accept it.",
          "2. The stanza layer checks the line count and the slot pattern (odd/even lines) and any stanza-wide rule.",
          "3. For every surviving meter the parser recovers the gana split and the yati akshara positions.",
          "4. Ties are reported as ambiguity; yati and prāsa engines break them later.", "",
          "## Constraints", "",
          "A positional rule (Kandamu: no జ at odd ganas, జ or నల at the sixth, guru at the end) is applied "
          "when the rules are written: the forbidden alternative is simply absent from that `Gk` rule. So "
          "the constraint is visible in the grammar itself. Stanza-wide rules (the first akshara of every "
          "line has the same weight) cannot live in a per-line grammar and are listed separately.", "",
          "## Gana glossary", "", "| gana | name | pattern | matras | classes |", "|---|---|---|---|---|"]
    for g in sorted(reg.ganas, key=lambda x: (x.aksharas, x.pattern)):
        classes = ", ".join(c for c, members in reg.classes.items() if g in members) or "–"
        md.append(f"| {g.telugu} | {g.name} | `{g.pattern}` | {g.matras} | {classes} |")
    md += ["", "Class tokens used in the catalogue: `surya`, `indra`, `chandra`, `kanda`; `m3`/`m4`/`m5` = any "
               "group worth that many matras; `all_laghu(X)` = the laghu-only members of class X.", "",
           "## Meters", ""]
    for spec in dawg.catalogue.meters:
        if spec.abstract:
            md.append(f"- {spec.name_te} `{spec.name}` — family entry, not identified directly")
        else:
            md.append(f"- [{spec.name_te} `{spec.name}`]({spec.name}.md) — {spec.family}")
    return "\n".join(md) + "\n"


def gr_slice(grammar: Grammar, n: int) -> Grammar:
    """The first ``n`` productions of a grammar (for excerpts)."""
    return Grammar(meter=grammar.meter, slot=grammar.slot, form=grammar.form, start=grammar.start,
                   nonterminals=grammar.nonterminals, productions=grammar.productions[:n],
                   gana_positions=grammar.gana_positions, alphabet=grammar.alphabet)


def grammar_file_text(spec: MeterSpec, dawg: Optional[LineDawg] = None) -> str:
    """The ``.rlg`` text of one meter: the hierarchical prosodic grammar, the
    per-line right-linear grammars, the whole-poem right-linear grammar, and
    the strict (automaton) form with every nonterminal explained."""
    dawg = dawg or default_dawg()
    pg = build_prosodic_grammar(spec, dawg)
    fl = flatten_poem(spec, dawg)
    lo, hi = spec.aksharalu
    stp = to_strict(fl)
    out = [f"# {spec.name_te} · {spec.name} — prosodic grammar ({spec.family}, {spec.padalu} lines"
           f"{', repeatable' if spec.repeatable else ''}, {lo if lo == hi else f'{lo}–{hi}'} aksharas per line)",
           "# generated from meter_rules.yaml by indic_meter_dawg; do not edit by hand",
           "#",
           "# One grammar, three forms: (1) hierarchical, for reading; (2) right-linear, the same language flattened;",
           "# (3) strict, one symbol per production = the prosodic automaton. All three generate exactly the same poems.",
           "#",
           "# Terminals: U = guru (2 matras), I = laghu (1 matra), ⏎ = line separator.",
           "# Nonterminals: Poem, Unit, Line_<slot>, gana classes (Surya, Indra, Kanda, M4 …), ganas (భ, ర, …).",
           "#   Kanda−జ  = the class minus జ (a constraint removed it)   Kanda=జ|నల = only జ or నల allowed",
           "#   Kanda$U  = only members ending in a guru                   X⟨U⟩ = inside the branch where every line starts with U",
           "#   L2.G3    = line 2, about to read gana 3 (forms 2 and 3)",
           "#   A_UUI_2  = inside alternative UUI of A, 2 symbols already read (form 3 only)",
           "",
           "# ===== 1. Hierarchical: Poem → lines → gana classes → ganas → symbols",
           format_prosodic_grammar(pg),
           "",
           "# ===== 2. Right-linear (A → wB | w) over {U, I, ⏎}: the hierarchy flattened",
           format_grammar_grouped(fl),
           "",
           f"# ===== 3. Strict (A → aB | a): {len(stp.productions)} productions, {len(stp.nonterminals) + 1} states;",
           f"# minimized prosodic automaton: {prosodic_automaton(spec.name).n_states} states. Every production is commented.",
           format_grammar(stp)]
    return "\n".join(out) + "\n"


def write_grammars(out_dir: str | Path, dawg: Optional[LineDawg] = None) -> list[Path]:
    """One ``<meter>.rlg`` per concrete meter; stale per-slot files are removed."""
    dawg = dawg or default_dawg()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for stale in out.glob("*__*.rlg"):
        stale.unlink()
    written = []
    for spec in dawg.catalogue.concrete:
        p = out / f"{spec.name}.rlg"
        p.write_text(grammar_file_text(spec, dawg), encoding="utf-8")
        written.append(p)
    return written


def write_docs(out_dir: str | Path, dawg: Optional[LineDawg] = None) -> list[Path]:
    dawg = dawg or default_dawg()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for spec in dawg.catalogue.concrete:
        p = out / f"{spec.name}.md"
        p.write_text(meter_doc_markdown(spec, dawg), encoding="utf-8")
        written.append(p)
    p = out / "README.md"
    p.write_text(primer_markdown(dawg), encoding="utf-8")
    written.append(p)
    return written

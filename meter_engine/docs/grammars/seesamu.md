# సీసము · seesamu

*upajati* · 4 lines · between 22 and 36 aksharas per line · prāsa not required · prāsa-yati allowed

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line_all ⏎ Line_all ⏎ Line_all ⏎ Line_all | Line_laghu ⏎ Line_laghu ⏎ Line_laghu ⏎ Line_laghu # 4 lines

# lines
Line_all → Indra Indra Indra Indra Indra Indra Surya Surya # slot all: 8 ganas
Line_laghu → నలల నలల నలల నలల నలల నలల న న         # slot laghu: 8 ganas

# gana classes
Indra → భ | ర | త | నల | నగ | సల                 # class indra
Surya → న | హ                                    # class surya

# ganas → symbols
భ → U I I                                        # bha, 4 matras
ర → U I U                                        # ra, 5 matras
త → U U I                                        # ta, 5 matras
నల → I I I I                                     # nala, 4 matras
నగ → I I I U                                     # naga, 5 matras
సల → I I U I                                     # sala, 5 matras
న → I I I                                        # na, 3 matras
హ → U I                                          # ha, 3 matras
నలల → I I I I I                                  # nalala, 5 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

A line of slot *all* has 8 ganas (indra, indra, indra, indra, indra, indra, surya, surya); a line of slot *laghu* has 8 ganas (నలల, నలల, నలల, నలల, నలల, నలల, న, న). Each gana is chosen from a class, so the line length varies.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Alternative stanza forms.** The lines follow *all all all all* or *laghu laghu laghu laghu*; one stanza keeps one form throughout, the forms are never mixed.
3. **Recipe for slot *all*.** In order:
    1. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    2. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    3. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    4. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    5. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    6. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    7. a సూర్యగణము (surya gana): న III or హ UI
    8. a సూర్యగణము (surya gana): న III or హ UI
4. **Recipe for slot *laghu*.** In order:
    1. నలల (nalala) IIIII
    2. నలల (nalala) IIIII
    3. నలల (nalala) IIIII
    4. నలల (nalala) IIIII
    5. నలల (nalala) IIIII
    6. నలల (nalala) IIIII
    7. న (na) III
    8. న (na) III
5. **Yati.** at the first akshara of gana 3 or 7 in slot *all*; at the first akshara of gana 3 or 7 in slot *laghu*. Because gana lengths vary, the akshara index of the yati depends on the ganas actually used; the parser reports it per line.
6. **Prāsa.** Not required. Prāsa-yati (rhyme at the yati position) is allowed instead of yati-maitri.
7. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).
8. **Printing.** Each pada is conventionally printed as 2 half-lines; the identifier joins them, so a 8-line text is read as 4 padas.
9. **What follows.** The stanza is normally followed by a ataveladi or tetagiti (the gīta), identified separately.

Note: the all-laghu form (సర్వలఘు సీసము, Pothana 11-72) is the alternative slot pattern of this meter

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem. `F1.` / `F2.` prefix the states of the two stanza forms.

```
Poem → UII F1.L1.G2 | UIU F1.L1.G2 | UUI F1.L1.G2 | IIII F1.L1.G2 | IIIU F1.L1.G2 | IIUI F1.L1.G2 | IIIII F2.L1.G2
F1.L1.G2 → UII F1.L1.G3 | UIU F1.L1.G3 | UUI F1.L1.G3 | IIII F1.L1.G3 | IIIU F1.L1.G3 | IIUI F1.L1.G3
F1.L1.G3 → UII F1.L1.G4 | UIU F1.L1.G4 | UUI F1.L1.G4 | IIII F1.L1.G4 | IIIU F1.L1.G4 | IIUI F1.L1.G4
F1.L1.G4 → UII F1.L1.G5 | UIU F1.L1.G5 | UUI F1.L1.G5 | IIII F1.L1.G5 | IIIU F1.L1.G5 | IIUI F1.L1.G5
F1.L1.G5 → UII F1.L1.G6 | UIU F1.L1.G6 | UUI F1.L1.G6 | IIII F1.L1.G6 | IIIU F1.L1.G6 | IIUI F1.L1.G6
F1.L1.G6 → UII F1.L1.G7 | UIU F1.L1.G7 | UUI F1.L1.G7 | IIII F1.L1.G7 | IIIU F1.L1.G7 | IIUI F1.L1.G7
F1.L1.G7 → III F1.L1.G8 | UI F1.L1.G8
F1.L1.G8 → III⏎ F1.L2.G1 | UI⏎ F1.L2.G1
F1.L2.G1 → UII F1.L2.G2 | UIU F1.L2.G2 | UUI F1.L2.G2 | IIII F1.L2.G2 | IIIU F1.L2.G2 | IIUI F1.L2.G2
F1.L2.G2 → UII F1.L2.G3 | UIU F1.L2.G3 | UUI F1.L2.G3 | IIII F1.L2.G3 | IIIU F1.L2.G3 | IIUI F1.L2.G3
F1.L2.G3 → UII F1.L2.G4 | UIU F1.L2.G4 | UUI F1.L2.G4 | IIII F1.L2.G4 | IIIU F1.L2.G4 | IIUI F1.L2.G4
F1.L2.G4 → UII F1.L2.G5 | UIU F1.L2.G5 | UUI F1.L2.G5 | IIII F1.L2.G5 | IIIU F1.L2.G5 | IIUI F1.L2.G5
F1.L2.G5 → UII F1.L2.G6 | UIU F1.L2.G6 | UUI F1.L2.G6 | IIII F1.L2.G6 | IIIU F1.L2.G6 | IIUI F1.L2.G6
F1.L2.G6 → UII F1.L2.G7 | UIU F1.L2.G7 | UUI F1.L2.G7 | IIII F1.L2.G7 | IIIU F1.L2.G7 | IIUI F1.L2.G7
F1.L2.G7 → III F1.L2.G8 | UI F1.L2.G8
F1.L2.G8 → III⏎ F1.L3.G1 | UI⏎ F1.L3.G1
F1.L3.G1 → UII F1.L3.G2 | UIU F1.L3.G2 | UUI F1.L3.G2 | IIII F1.L3.G2 | IIIU F1.L3.G2 | IIUI F1.L3.G2
F1.L3.G2 → UII F1.L3.G3 | UIU F1.L3.G3 | UUI F1.L3.G3 | IIII F1.L3.G3 | IIIU F1.L3.G3 | IIUI F1.L3.G3
F1.L3.G3 → UII F1.L3.G4 | UIU F1.L3.G4 | UUI F1.L3.G4 | IIII F1.L3.G4 | IIIU F1.L3.G4 | IIUI F1.L3.G4
F1.L3.G4 → UII F1.L3.G5 | UIU F1.L3.G5 | UUI F1.L3.G5 | IIII F1.L3.G5 | IIIU F1.L3.G5 | IIUI F1.L3.G5
F1.L3.G5 → UII F1.L3.G6 | UIU F1.L3.G6 | UUI F1.L3.G6 | IIII F1.L3.G6 | IIIU F1.L3.G6 | IIUI F1.L3.G6
F1.L3.G6 → UII F1.L3.G7 | UIU F1.L3.G7 | UUI F1.L3.G7 | IIII F1.L3.G7 | IIIU F1.L3.G7 | IIUI F1.L3.G7
F1.L3.G7 → III F1.L3.G8 | UI F1.L3.G8
F1.L3.G8 → III⏎ F1.L4.G1 | UI⏎ F1.L4.G1
F1.L4.G1 → UII F1.L4.G2 | UIU F1.L4.G2 | UUI F1.L4.G2 | IIII F1.L4.G2 | IIIU F1.L4.G2 | IIUI F1.L4.G2
F1.L4.G2 → UII F1.L4.G3 | UIU F1.L4.G3 | UUI F1.L4.G3 | IIII F1.L4.G3 | IIIU F1.L4.G3 | IIUI F1.L4.G3
F1.L4.G3 → UII F1.L4.G4 | UIU F1.L4.G4 | UUI F1.L4.G4 | IIII F1.L4.G4 | IIIU F1.L4.G4 | IIUI F1.L4.G4
F1.L4.G4 → UII F1.L4.G5 | UIU F1.L4.G5 | UUI F1.L4.G5 | IIII F1.L4.G5 | IIIU F1.L4.G5 | IIUI F1.L4.G5
F1.L4.G5 → UII F1.L4.G6 | UIU F1.L4.G6 | UUI F1.L4.G6 | IIII F1.L4.G6 | IIIU F1.L4.G6 | IIUI F1.L4.G6
F1.L4.G6 → UII F1.L4.G7 | UIU F1.L4.G7 | UUI F1.L4.G7 | IIII F1.L4.G7 | IIIU F1.L4.G7 | IIUI F1.L4.G7
F1.L4.G7 → III F1.L4.G8 | UI F1.L4.G8
F1.L4.G8 → III | UI
F2.L1.G2 → IIIII F2.L1.G3
F2.L1.G3 → IIIII F2.L1.G4
F2.L1.G4 → IIIII F2.L1.G5
F2.L1.G5 → IIIII F2.L1.G6
F2.L1.G6 → IIIII F2.L1.G7
F2.L1.G7 → III F2.L1.G8
F2.L1.G8 → III⏎ F2.L2.G1
F2.L2.G1 → IIIII F2.L2.G2
F2.L2.G2 → IIIII F2.L2.G3
F2.L2.G3 → IIIII F2.L2.G4
F2.L2.G4 → IIIII F2.L2.G5
F2.L2.G5 → IIIII F2.L2.G6
F2.L2.G6 → IIIII F2.L2.G7
F2.L2.G7 → III F2.L2.G8
F2.L2.G8 → III⏎ F2.L3.G1
F2.L3.G1 → IIIII F2.L3.G2
F2.L3.G2 → IIIII F2.L3.G3
F2.L3.G3 → IIIII F2.L3.G4
F2.L3.G4 → IIIII F2.L3.G5
F2.L3.G5 → IIIII F2.L3.G6
F2.L3.G6 → IIIII F2.L3.G7
F2.L3.G7 → III F2.L3.G8
F2.L3.G8 → III⏎ F2.L4.G1
F2.L4.G1 → IIIII F2.L4.G2
F2.L4.G2 → IIIII F2.L4.G3
F2.L4.G3 → IIIII F2.L4.G4
F2.L4.G4 → IIIII F2.L4.G5
F2.L4.G5 → IIIII F2.L4.G6
F2.L4.G6 → IIIII F2.L4.G7
F2.L4.G7 → III F2.L4.G8
F2.L4.G8 → III
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 697, each with such a comment, are in [`grammars/seesamu.rlg`](../../grammars/seesamu.rlg)):

```
Poem → U Poem_UII_1         # భ bha: symbol 1/3 read, 2 to go
Poem_UII_1 → I Poem_UII_2   # భ bha: symbol 2/3 read, 1 to go
Poem_UII_2 → I F1.L1.G2     # భ bha: symbol 3/3, complete → F1.L1.G2
Poem → U Poem_UIU_1         # ర ra: symbol 1/3 read, 2 to go
Poem_UIU_1 → I Poem_UIU_2   # ర ra: symbol 2/3 read, 1 to go
Poem_UIU_2 → U F1.L1.G2     # ర ra: symbol 3/3, complete → F1.L1.G2
Poem → U Poem_UUI_1         # త ta: symbol 1/3 read, 2 to go
Poem_UUI_1 → U Poem_UUI_2   # త ta: symbol 2/3 read, 1 to go
…
```

The strict grammar has 569 states; minimized, the prosodic automaton has 291 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (37 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line_laghu ⏎ Line_laghu ⏎ Line_laghu ⏎ Line_laghu
⇒ నలల నలల నలల నలల నలల నలల న న ⏎ Line_laghu ⏎ Line_laghu ⏎ Line_laghu
⇒ I I I I I నలల నలల నలల నలల నలల న న ⏎ Line_laghu ⏎ Line_laghu ⏎ Line_laghu
⇒ I I I I I I I I I I నలల నలల నలల నలల న న ⏎ Line_laghu ⏎ Line_laghu ⏎ Line_laghu
⇒ I I I I I I I I I I I I I I I నలల నలల నలల న న ⏎ Line_laghu ⏎ Line_laghu ⏎ Line_laghu
⇒ I I I I I I I I I I I I I I I I I I I I నలల నలల న న ⏎ Line_laghu ⏎ Line_laghu ⏎ Line_laghu
⇒ I I I I I I I I I I I I I I I I I I I I I I I I I నలల న న ⏎ Line_laghu ⏎ Line_laghu ⏎ Line_laghu
⇒ I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I న న ⏎ Line_laghu ⏎ Line_laghu ⏎ Line_laghu
⇒ I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I న ⏎ Line_laghu ⏎ Line_laghu ⏎ Line_laghu
⇒ …
⇒ I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I ⏎ I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I ⏎ I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I ⏎ I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I I
```

The result, one line per row:

```
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 8 | 22–30 | 186,624 | 37 |
| laghu | 8 | 36 | 1 | 37 |

Whole-prosodic automaton (over U, I, ⏎): 291 states.

Grammar file: [`grammars/seesamu.rlg`](../../grammars/seesamu.rlg).

Diagram: [rule card](../../diagrams/meters/seesamu.svg) · [mermaid](../../diagrams/meters/seesamu.md) · [DFA all](../../diagrams/dfa/seesamu__all.svg) · [DFA laghu](../../diagrams/dfa/seesamu__laghu.svg)

# లయవిభాతి · layavibhati

*vrutta* · 4 lines · exactly 34 aksharas per line · prāsa required · prāsa-yati allowed

Example from the catalogue:

> అలికులము నీలముల చెలువము వహింప నవడళముల హరిన్మణుల పొలుపు నదలిర్పన్

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → న స న న స న న స న న స గురువు              # slot all: 12 ganas

# ganas → symbols
న → I I I                                        # na, 3 matras
స → I I U                                        # sa, 4 matras
గురువు → U                                       # guruvu, 2 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 12 ganas, **న స న న స న న స న న స గురువు**, i.e. the 34-akshara pattern `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. న (na) III
    2. స (sa) IIU
    3. న (na) III
    4. న (na) III
    5. స (sa) IIU
    6. న (na) III
    7. న (na) III
    8. స (sa) IIU
    9. న (na) III
    10. న (na) III
    11. స (sa) IIU
    12. గురువు (guruvu) U
3. **Yati.** The akshara at position 10, 19 or 28 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).
6. **Printing.** Each pada is conventionally printed as 2 half-lines; the identifier joins them, so a 8-line text is read as 4 padas.

Note: the yati points take ప్రాసయతి (the second akshara of each segment rhymes with the pāda's prāsa), not yati-maitri; Pothana prints each pāda as two half-lines

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → III L1.G2
L1.G2 → IIU L1.G3
L1.G3 → III L1.G4
L1.G4 → III L1.G5
L1.G5 → IIU L1.G6
L1.G6 → III L1.G7
L1.G7 → III L1.G8
L1.G8 → IIU L1.G9
L1.G9 → III L1.G10
L1.G10 → III L1.G11
L1.G11 → IIU L1.G12
L1.G12 → U⏎ L2.G1
L2.G1 → III L2.G2
L2.G2 → IIU L2.G3
L2.G3 → III L2.G4
L2.G4 → III L2.G5
L2.G5 → IIU L2.G6
L2.G6 → III L2.G7
L2.G7 → III L2.G8
L2.G8 → IIU L2.G9
L2.G9 → III L2.G10
L2.G10 → III L2.G11
L2.G11 → IIU L2.G12
L2.G12 → U⏎ L3.G1
L3.G1 → III L3.G2
L3.G2 → IIU L3.G3
L3.G3 → III L3.G4
L3.G4 → III L3.G5
L3.G5 → IIU L3.G6
L3.G6 → III L3.G7
L3.G7 → III L3.G8
L3.G8 → IIU L3.G9
L3.G9 → III L3.G10
L3.G10 → III L3.G11
L3.G11 → IIU L3.G12
L3.G12 → U⏎ L4.G1
L4.G1 → III L4.G2
L4.G2 → IIU L4.G3
L4.G3 → III L4.G4
L4.G4 → III L4.G5
L4.G5 → IIU L4.G6
L4.G6 → III L4.G7
L4.G7 → III L4.G8
L4.G8 → IIU L4.G9
L4.G9 → III L4.G10
L4.G10 → III L4.G11
L4.G11 → IIU L4.G12
L4.G12 → U
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 139, each with such a comment, are in [`grammars/layavibhati.rlg`](../../grammars/layavibhati.rlg)):

```
Poem → I Poem_III_1           # న na: symbol 1/3 read, 2 to go
Poem_III_1 → I Poem_III_2     # న na: symbol 2/3 read, 1 to go
Poem_III_2 → I L1.G2          # న na: symbol 3/3, complete → L1.G2
L1.G2 → I L1.G2_IIU_1         # స sa: symbol 1/3 read, 2 to go
L1.G2_IIU_1 → I L1.G2_IIU_2   # స sa: symbol 2/3 read, 1 to go
L1.G2_IIU_2 → U L1.G3         # స sa: symbol 3/3, complete → L1.G3
L1.G3 → I L1.G3_III_1         # న na: symbol 1/3 read, 2 to go
L1.G3_III_1 → I L1.G3_III_2   # న na: symbol 2/3 read, 1 to go
…
```

The strict grammar has 140 states; minimized, the prosodic automaton has 140 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (53 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ న స న న స న న స న న స గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I స న న స న న స న న స గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I U న న స న న స న న స గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I U I I I న స న న స న న స గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I U I I I I I I స న న స న న స గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I U I I I I I I I I U న న స న న స గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I U I I I I I I I I U I I I న స న న స గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I U I I I I I I I I U I I I I I I స న న స గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ I I I I I U I I I I I I I I U I I I I I I I I U I I I I I I I I U U ⏎ I I I I I U I I I I I I I I U I I I I I I I I U I I I I I I I I U U ⏎ I I I I I U I I I I I I I I U I I I I I I I I U I I I I I I I I U U ⏎ I I I I I U I I I I I I I I U I I I I I I I I U I I I I I I I I U U
```

The result, one line per row:

```
IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU
IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU
IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU
IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 12 | 34 | 1 | 35 |

Whole-prosodic automaton (over U, I, ⏎): 140 states.

Grammar file: [`grammars/layavibhati.rlg`](../../grammars/layavibhati.rlg).

Diagram: [rule card](../../diagrams/meters/layavibhati.svg) · [mermaid](../../diagrams/meters/layavibhati.md) · [DFA all](../../diagrams/dfa/layavibhati__all.svg)

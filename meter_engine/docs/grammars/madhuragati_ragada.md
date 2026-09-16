# మధురగతి_రగడ · madhuragati_ragada

*jati* · 2 lines per unit, repeatable · between 8 and 16 aksharas per line · prāsa required · prāsa-yati allowed

Example from the catalogue:

> శ్రీవనితాధిపుఁ జేరి భజింపుఁడు

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Unit | Unit ⏎ Poem                        # one unit
Unit → Line ⏎ Line                               # 2 lines

# lines
Line → M4 M4 M4 M4                               # slot all: 4 ganas

# gana classes
M4 → గా | స | జ | భ | నల                         # class m4

# ganas → symbols
గా → U U                                         # gaa, 4 matras
స → I I U                                        # sa, 4 matras
జ → I U I                                        # ja, 4 matras
భ → U I I                                        # bha, 4 matras
నల → I I I I                                     # nala, 4 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;
- `Poem → Unit | Unit ⏎ Poem` — the poem is any number of units (right recursion keeps it regular);

## In one sentence

Every line has 4 ganas (m4, m4, m4, m4). Each gana is chosen from a class, so the line length varies.

## The rules, one by one

1. **Line count.** A unit has 2 lines; a poem is any number of such units in a row.
2. **Line recipe.** In order:
    1. any syllable group worth 4 matras: గా UU, స IIU, జ IUI, భ UII or నల IIII
    2. any syllable group worth 4 matras: గా UU, స IIU, జ IUI, భ UII or నల IIII
    3. any syllable group worth 4 matras: గా UU, స IIU, జ IUI, భ UII or నల IIII
    4. any syllable group worth 4 matras: గా UU, స IIU, జ IUI, భ UII or నల IIII
3. **Yati.** at the first akshara of gana 3. Because gana lengths vary, the akshara index of the yati depends on the ganas actually used; the parser reports it per line.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem — or, for this repeatable meter, emits `⏎` and returns to `L1.G1`.

```
Poem → UU L1.G2 | IIU L1.G2 | IUI L1.G2 | UII L1.G2 | IIII L1.G2
L1.G1 → UU L1.G2 | IIU L1.G2 | IUI L1.G2 | UII L1.G2 | IIII L1.G2
L1.G2 → UU L1.G3 | IIU L1.G3 | IUI L1.G3 | UII L1.G3 | IIII L1.G3
L1.G3 → UU L1.G4 | IIU L1.G4 | IUI L1.G4 | UII L1.G4 | IIII L1.G4
L1.G4 → UU⏎ L2.G1 | IIU⏎ L2.G1 | IUI⏎ L2.G1 | UII⏎ L2.G1 | IIII⏎ L2.G1
L2.G1 → UU L2.G2 | IIU L2.G2 | IUI L2.G2 | UII L2.G2 | IIII L2.G2
L2.G2 → UU L2.G3 | IIU L2.G3 | IUI L2.G3 | UII L2.G3 | IIII L2.G3
L2.G3 → UU L2.G4 | IIU L2.G4 | IUI L2.G4 | UII L2.G4 | IIII L2.G4
L2.G4 → UU | UU⏎ L1.G1 | IIU | IIU⏎ L1.G1 | IUI | IUI⏎ L1.G1 | UII | UII⏎ L1.G1 | IIII | IIII⏎ L1.G1
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 160, each with such a comment, are in [`grammars/madhuragati_ragada.rlg`](../../grammars/madhuragati_ragada.rlg)):

```
Poem → U Poem_UU_1          # గా gaa: symbol 1/2 read, 1 to go
Poem_UU_1 → U L1.G2         # గా gaa: symbol 2/2, complete → L1.G2
L1.G1 → U L1.G1_UU_1        # గా gaa: symbol 1/2 read, 1 to go
L1.G1_UU_1 → U L1.G2        # గా gaa: symbol 2/2, complete → L1.G2
Poem → I Poem_IIU_1         # స sa: symbol 1/3 read, 2 to go
Poem_IIU_1 → I Poem_IIU_2   # స sa: symbol 2/3 read, 1 to go
Poem_IIU_2 → U L1.G2        # స sa: symbol 3/3, complete → L1.G2
L1.G1 → I L1.G1_IIU_1       # స sa: symbol 1/3 read, 2 to go
…
```

The strict grammar has 120 states; minimized, the prosodic automaton has 34 states.

## One worked derivation

A poem of 2 lines, derived top-down from `Poem` (20 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Unit
⇒ Line ⏎ Line
⇒ M4 M4 M4 M4 ⏎ Line
⇒ స M4 M4 M4 ⏎ Line
⇒ I I U M4 M4 M4 ⏎ Line
⇒ I I U గా M4 M4 ⏎ Line
⇒ I I U U U M4 M4 ⏎ Line
⇒ I I U U U నల M4 ⏎ Line
⇒ I I U U U I I I I M4 ⏎ Line
⇒ …
⇒ I I U U U I I I I I U I ⏎ I I U I I U U U I I I I
```

The result, one line per row:

```
IIUUUIIIIIUI
IIUIIUUUIIII
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 4 | 8–16 | 625 | 17 |

Whole-prosodic automaton (over U, I, ⏎): 34 states.

Grammar file: [`grammars/madhuragati_ragada.rlg`](../../grammars/madhuragati_ragada.rlg).

Diagram: [rule card](../../diagrams/meters/madhuragati_ragada.svg) · [mermaid](../../diagrams/meters/madhuragati_ragada.md) · [DFA all](../../diagrams/dfa/madhuragati_ragada__all.svg)

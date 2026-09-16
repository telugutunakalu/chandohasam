# మహాస్రగ్ధర · mahasragdhara

*vrutta* · 4 lines · exactly 22 aksharas per line · prāsa required

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → స త త న స ర ర గురువు                      # slot all: 8 ganas

# ganas → symbols
స → I I U                                        # sa, 4 matras
త → U U I                                        # ta, 5 matras
న → I I I                                        # na, 3 matras
ర → U I U                                        # ra, 5 matras
గురువు → U                                       # guruvu, 2 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 8 ganas, **స త త న స ర ర గురువు**, i.e. the 22-akshara pattern `IIUUUIUUIIIIIIUUIUUIUU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. స (sa) IIU
    2. త (ta) UUI
    3. త (ta) UUI
    4. న (na) III
    5. స (sa) IIU
    6. ర (ra) UIU
    7. ర (ra) UIU
    8. గురువు (guruvu) U
3. **Yati.** The akshara at position 9 or 16 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → IIU L1.G2
L1.G2 → UUI L1.G3
L1.G3 → UUI L1.G4
L1.G4 → III L1.G5
L1.G5 → IIU L1.G6
L1.G6 → UIU L1.G7
L1.G7 → UIU L1.G8
L1.G8 → U⏎ L2.G1
L2.G1 → IIU L2.G2
L2.G2 → UUI L2.G3
L2.G3 → UUI L2.G4
L2.G4 → III L2.G5
L2.G5 → IIU L2.G6
L2.G6 → UIU L2.G7
L2.G7 → UIU L2.G8
L2.G8 → U⏎ L3.G1
L3.G1 → IIU L3.G2
L3.G2 → UUI L3.G3
L3.G3 → UUI L3.G4
L3.G4 → III L3.G5
L3.G5 → IIU L3.G6
L3.G6 → UIU L3.G7
L3.G7 → UIU L3.G8
L3.G8 → U⏎ L4.G1
L4.G1 → IIU L4.G2
L4.G2 → UUI L4.G3
L4.G3 → UUI L4.G4
L4.G4 → III L4.G5
L4.G5 → IIU L4.G6
L4.G6 → UIU L4.G7
L4.G7 → UIU L4.G8
L4.G8 → U
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 91, each with such a comment, are in [`grammars/mahasragdhara.rlg`](../../grammars/mahasragdhara.rlg)):

```
Poem → I Poem_IIU_1           # స sa: symbol 1/3 read, 2 to go
Poem_IIU_1 → I Poem_IIU_2     # స sa: symbol 2/3 read, 1 to go
Poem_IIU_2 → U L1.G2          # స sa: symbol 3/3, complete → L1.G2
L1.G2 → U L1.G2_UUI_1         # త ta: symbol 1/3 read, 2 to go
L1.G2_UUI_1 → U L1.G2_UUI_2   # త ta: symbol 2/3 read, 1 to go
L1.G2_UUI_2 → I L1.G3         # త ta: symbol 3/3, complete → L1.G3
L1.G3 → U L1.G3_UUI_1         # త ta: symbol 1/3 read, 2 to go
L1.G3_UUI_1 → U L1.G3_UUI_2   # త ta: symbol 2/3 read, 1 to go
…
```

The strict grammar has 92 states; minimized, the prosodic automaton has 92 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (37 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ స త త న స ర ర గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I U త త న స ర ర గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I U U U I త న స ర ర గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I U U U I U U I న స ర ర గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I U U U I U U I I I I స ర ర గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I U U U I U U I I I I I I U ర ర గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I U U U I U U I I I I I I U U I U ర గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I U U U I U U I I I I I I U U I U U I U గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ I I U U U I U U I I I I I I U U I U U I U U ⏎ I I U U U I U U I I I I I I U U I U U I U U ⏎ I I U U U I U U I I I I I I U U I U U I U U ⏎ I I U U U I U U I I I I I I U U I U U I U U
```

The result, one line per row:

```
IIUUUIUUIIIIIIUUIUUIUU
IIUUUIUUIIIIIIUUIUUIUU
IIUUUIUUIIIIIIUUIUUIUU
IIUUUIUUIIIIIIUUIUUIUU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 8 | 22 | 1 | 23 |

Whole-prosodic automaton (over U, I, ⏎): 92 states.

Grammar file: [`grammars/mahasragdhara.rlg`](../../grammars/mahasragdhara.rlg).

Diagram: [rule card](../../diagrams/meters/mahasragdhara.svg) · [mermaid](../../diagrams/meters/mahasragdhara.md) · [DFA all](../../diagrams/dfa/mahasragdhara__all.svg)

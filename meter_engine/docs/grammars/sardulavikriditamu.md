# శార్దూలవిక్రీడితము · sardulavikriditamu

*vrutta* · 4 lines · exactly 19 aksharas per line · prāsa required

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → మ స జ స త త గురువు                        # slot all: 7 ganas

# ganas → symbols
మ → U U U                                        # ma, 6 matras
స → I I U                                        # sa, 4 matras
జ → I U I                                        # ja, 4 matras
త → U U I                                        # ta, 5 matras
గురువు → U                                       # guruvu, 2 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 7 ganas, **మ స జ స త త గురువు**, i.e. the 19-akshara pattern `UUUIIUIUIIIUUUIUUIU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. మ (ma) UUU
    2. స (sa) IIU
    3. జ (ja) IUI
    4. స (sa) IIU
    5. త (ta) UUI
    6. త (ta) UUI
    7. గురువు (guruvu) U
3. **Yati.** The akshara at position 13 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → UUU L1.G2
L1.G2 → IIU L1.G3
L1.G3 → IUI L1.G4
L1.G4 → IIU L1.G5
L1.G5 → UUI L1.G6
L1.G6 → UUI L1.G7
L1.G7 → U⏎ L2.G1
L2.G1 → UUU L2.G2
L2.G2 → IIU L2.G3
L2.G3 → IUI L2.G4
L2.G4 → IIU L2.G5
L2.G5 → UUI L2.G6
L2.G6 → UUI L2.G7
L2.G7 → U⏎ L3.G1
L3.G1 → UUU L3.G2
L3.G2 → IIU L3.G3
L3.G3 → IUI L3.G4
L3.G4 → IIU L3.G5
L3.G5 → UUI L3.G6
L3.G6 → UUI L3.G7
L3.G7 → U⏎ L4.G1
L4.G1 → UUU L4.G2
L4.G2 → IIU L4.G3
L4.G3 → IUI L4.G4
L4.G4 → IIU L4.G5
L4.G5 → UUI L4.G6
L4.G6 → UUI L4.G7
L4.G7 → U
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 79, each with such a comment, are in [`grammars/sardulavikriditamu.rlg`](../../grammars/sardulavikriditamu.rlg)):

```
Poem → U Poem_UUU_1           # మ ma: symbol 1/3 read, 2 to go
Poem_UUU_1 → U Poem_UUU_2     # మ ma: symbol 2/3 read, 1 to go
Poem_UUU_2 → U L1.G2          # మ ma: symbol 3/3, complete → L1.G2
L1.G2 → I L1.G2_IIU_1         # స sa: symbol 1/3 read, 2 to go
L1.G2_IIU_1 → I L1.G2_IIU_2   # స sa: symbol 2/3 read, 1 to go
L1.G2_IIU_2 → U L1.G3         # స sa: symbol 3/3, complete → L1.G3
L1.G3 → I L1.G3_IUI_1         # జ ja: symbol 1/3 read, 2 to go
L1.G3_IUI_1 → U L1.G3_IUI_2   # జ ja: symbol 2/3 read, 1 to go
…
```

The strict grammar has 80 states; minimized, the prosodic automaton has 80 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (33 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ మ స జ స త త గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U U U స జ స త త గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U U U I I U జ స త త గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U U U I I U I U I స త త గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U U U I I U I U I I I U త త గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U U U I I U I U I I I U U U I త గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U U U I I U I U I I I U U U I U U I గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U U U I I U I U I I I U U U I U U I U ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ U U U I I U I U I I I U U U I U U I U ⏎ U U U I I U I U I I I U U U I U U I U ⏎ U U U I I U I U I I I U U U I U U I U ⏎ U U U I I U I U I I I U U U I U U I U
```

The result, one line per row:

```
UUUIIUIUIIIUUUIUUIU
UUUIIUIUIIIUUUIUUIU
UUUIIUIUIIIUUUIUUIU
UUUIIUIUIIIUUUIUUIU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 7 | 19 | 1 | 20 |

Whole-prosodic automaton (over U, I, ⏎): 80 states.

Grammar file: [`grammars/sardulavikriditamu.rlg`](../../grammars/sardulavikriditamu.rlg).

Diagram: [rule card](../../diagrams/meters/sardulavikriditamu.svg) · [mermaid](../../diagrams/meters/sardulavikriditamu.md) · [DFA all](../../diagrams/dfa/sardulavikriditamu__all.svg)

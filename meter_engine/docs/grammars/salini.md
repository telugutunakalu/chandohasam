# శాలిని · salini

*vrutta* · 4 lines · exactly 11 aksharas per line · prāsa required

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → మ త త గా                                  # slot all: 4 ganas

# ganas → symbols
మ → U U U                                        # ma, 6 matras
త → U U I                                        # ta, 5 matras
గా → U U                                         # gaa, 4 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 4 ganas, **మ త త గా**, i.e. the 11-akshara pattern `UUUUUIUUIUU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. మ (ma) UUU
    2. త (ta) UUI
    3. త (ta) UUI
    4. గా (gaa) UU
3. **Yati.** The akshara at position 7 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → UUU L1.G2
L1.G2 → UUI L1.G3
L1.G3 → UUI L1.G4
L1.G4 → UU⏎ L2.G1
L2.G1 → UUU L2.G2
L2.G2 → UUI L2.G3
L2.G3 → UUI L2.G4
L2.G4 → UU⏎ L3.G1
L3.G1 → UUU L3.G2
L3.G2 → UUI L3.G3
L3.G3 → UUI L3.G4
L3.G4 → UU⏎ L4.G1
L4.G1 → UUU L4.G2
L4.G2 → UUI L4.G3
L4.G3 → UUI L4.G4
L4.G4 → UU
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 47, each with such a comment, are in [`grammars/salini.rlg`](../../grammars/salini.rlg)):

```
Poem → U Poem_UUU_1           # మ ma: symbol 1/3 read, 2 to go
Poem_UUU_1 → U Poem_UUU_2     # మ ma: symbol 2/3 read, 1 to go
Poem_UUU_2 → U L1.G2          # మ ma: symbol 3/3, complete → L1.G2
L1.G2 → U L1.G2_UUI_1         # త ta: symbol 1/3 read, 2 to go
L1.G2_UUI_1 → U L1.G2_UUI_2   # త ta: symbol 2/3 read, 1 to go
L1.G2_UUI_2 → I L1.G3         # త ta: symbol 3/3, complete → L1.G3
L1.G3 → U L1.G3_UUI_1         # త ta: symbol 1/3 read, 2 to go
L1.G3_UUI_1 → U L1.G3_UUI_2   # త ta: symbol 2/3 read, 1 to go
…
```

The strict grammar has 48 states; minimized, the prosodic automaton has 48 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (21 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ మ త త గా ⏎ Line ⏎ Line ⏎ Line
⇒ U U U త త గా ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U U I త గా ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U U I U U I గా ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U U I U U I U U ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U U I U U I U U ⏎ మ త త గా ⏎ Line ⏎ Line
⇒ U U U U U I U U I U U ⏎ U U U త త గా ⏎ Line ⏎ Line
⇒ U U U U U I U U I U U ⏎ U U U U U I త గా ⏎ Line ⏎ Line
⇒ …
⇒ U U U U U I U U I U U ⏎ U U U U U I U U I U U ⏎ U U U U U I U U I U U ⏎ U U U U U I U U I U U
```

The result, one line per row:

```
UUUUUIUUIUU
UUUUUIUUIUU
UUUUUIUUIUU
UUUUUIUUIUU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 4 | 11 | 1 | 12 |

Whole-prosodic automaton (over U, I, ⏎): 48 states.

Grammar file: [`grammars/salini.rlg`](../../grammars/salini.rlg).

Diagram: [rule card](../../diagrams/meters/salini.svg) · [mermaid](../../diagrams/meters/salini.md) · [DFA all](../../diagrams/dfa/salini__all.svg)

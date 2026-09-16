# కవిరాజవిరాజితము · kavirajavirajitamu

*vrutta* · 4 lines · exactly 23 aksharas per line · prāsa required

Example from the catalogue:

> కమలదళంబులకైవడిఁ జెన్నగు కన్నులు జారుముఖప్రభలున్‌

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → న జ జ జ జ జ జ వ                           # slot all: 8 ganas

# ganas → symbols
న → I I I                                        # na, 3 matras
జ → I U I                                        # ja, 4 matras
వ → I U                                          # va, 3 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 8 ganas, **న జ జ జ జ జ జ వ**, i.e. the 23-akshara pattern `IIIIUIIUIIUIIUIIUIIUIIU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. న (na) III
    2. జ (ja) IUI
    3. జ (ja) IUI
    4. జ (ja) IUI
    5. జ (ja) IUI
    6. జ (ja) IUI
    7. జ (ja) IUI
    8. వ (va) IU
3. **Yati.** The akshara at position 8, 14 or 20 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → III L1.G2
L1.G2 → IUI L1.G3
L1.G3 → IUI L1.G4
L1.G4 → IUI L1.G5
L1.G5 → IUI L1.G6
L1.G6 → IUI L1.G7
L1.G7 → IUI L1.G8
L1.G8 → IU⏎ L2.G1
L2.G1 → III L2.G2
L2.G2 → IUI L2.G3
L2.G3 → IUI L2.G4
L2.G4 → IUI L2.G5
L2.G5 → IUI L2.G6
L2.G6 → IUI L2.G7
L2.G7 → IUI L2.G8
L2.G8 → IU⏎ L3.G1
L3.G1 → III L3.G2
L3.G2 → IUI L3.G3
L3.G3 → IUI L3.G4
L3.G4 → IUI L3.G5
L3.G5 → IUI L3.G6
L3.G6 → IUI L3.G7
L3.G7 → IUI L3.G8
L3.G8 → IU⏎ L4.G1
L4.G1 → III L4.G2
L4.G2 → IUI L4.G3
L4.G3 → IUI L4.G4
L4.G4 → IUI L4.G5
L4.G5 → IUI L4.G6
L4.G6 → IUI L4.G7
L4.G7 → IUI L4.G8
L4.G8 → IU
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 95, each with such a comment, are in [`grammars/kavirajavirajitamu.rlg`](../../grammars/kavirajavirajitamu.rlg)):

```
Poem → I Poem_III_1           # న na: symbol 1/3 read, 2 to go
Poem_III_1 → I Poem_III_2     # న na: symbol 2/3 read, 1 to go
Poem_III_2 → I L1.G2          # న na: symbol 3/3, complete → L1.G2
L1.G2 → I L1.G2_IUI_1         # జ ja: symbol 1/3 read, 2 to go
L1.G2_IUI_1 → U L1.G2_IUI_2   # జ ja: symbol 2/3 read, 1 to go
L1.G2_IUI_2 → I L1.G3         # జ ja: symbol 3/3, complete → L1.G3
L1.G3 → I L1.G3_IUI_1         # జ ja: symbol 1/3 read, 2 to go
L1.G3_IUI_1 → U L1.G3_IUI_2   # జ ja: symbol 2/3 read, 1 to go
…
```

The strict grammar has 96 states; minimized, the prosodic automaton has 96 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (37 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ న జ జ జ జ జ జ వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I I జ జ జ జ జ జ వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I U I జ జ జ జ జ వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I U I I U I జ జ జ జ వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I U I I U I I U I జ జ జ వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I U I I U I I U I I U I జ జ వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I U I I U I I U I I U I I U I జ వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I U I I U I I U I I U I I U I I U I వ ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ I I I I U I I U I I U I I U I I U I I U I I U ⏎ I I I I U I I U I I U I I U I I U I I U I I U ⏎ I I I I U I I U I I U I I U I I U I I U I I U ⏎ I I I I U I I U I I U I I U I I U I I U I I U
```

The result, one line per row:

```
IIIIUIIUIIUIIUIIUIIUIIU
IIIIUIIUIIUIIUIIUIIUIIU
IIIIUIIUIIUIIUIIUIIUIIU
IIIIUIIUIIUIIUIIUIIUIIU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 8 | 23 | 1 | 24 |

Whole-prosodic automaton (over U, I, ⏎): 96 states.

Grammar file: [`grammars/kavirajavirajitamu.rlg`](../../grammars/kavirajavirajitamu.rlg).

Diagram: [rule card](../../diagrams/meters/kavirajavirajitamu.svg) · [mermaid](../../diagrams/meters/kavirajavirajitamu.md) · [DFA all](../../diagrams/dfa/kavirajavirajitamu__all.svg)

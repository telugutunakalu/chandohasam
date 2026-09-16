# స్రగ్విణి · sragvini

*vrutta* · 4 lines · exactly 12 aksharas per line · prāsa required

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → ర ర ర ర                                   # slot all: 4 ganas

# ganas → symbols
ర → U I U                                        # ra, 5 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 4 ganas, **ర ర ర ర**, i.e. the 12-akshara pattern `UIUUIUUIUUIU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. ర (ra) UIU
    2. ర (ra) UIU
    3. ర (ra) UIU
    4. ర (ra) UIU
3. **Yati.** The akshara at position 7 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → UIU L1.G2
L1.G2 → UIU L1.G3
L1.G3 → UIU L1.G4
L1.G4 → UIU⏎ L2.G1
L2.G1 → UIU L2.G2
L2.G2 → UIU L2.G3
L2.G3 → UIU L2.G4
L2.G4 → UIU⏎ L3.G1
L3.G1 → UIU L3.G2
L3.G2 → UIU L3.G3
L3.G3 → UIU L3.G4
L3.G4 → UIU⏎ L4.G1
L4.G1 → UIU L4.G2
L4.G2 → UIU L4.G3
L4.G3 → UIU L4.G4
L4.G4 → UIU
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 51, each with such a comment, are in [`grammars/sragvini.rlg`](../../grammars/sragvini.rlg)):

```
Poem → U Poem_UIU_1           # ర ra: symbol 1/3 read, 2 to go
Poem_UIU_1 → I Poem_UIU_2     # ర ra: symbol 2/3 read, 1 to go
Poem_UIU_2 → U L1.G2          # ర ra: symbol 3/3, complete → L1.G2
L1.G2 → U L1.G2_UIU_1         # ర ra: symbol 1/3 read, 2 to go
L1.G2_UIU_1 → I L1.G2_UIU_2   # ర ra: symbol 2/3 read, 1 to go
L1.G2_UIU_2 → U L1.G3         # ర ra: symbol 3/3, complete → L1.G3
L1.G3 → U L1.G3_UIU_1         # ర ra: symbol 1/3 read, 2 to go
L1.G3_UIU_1 → I L1.G3_UIU_2   # ర ra: symbol 2/3 read, 1 to go
…
```

The strict grammar has 52 states; minimized, the prosodic automaton has 52 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (21 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ ర ర ర ర ⏎ Line ⏎ Line ⏎ Line
⇒ U I U ర ర ర ⏎ Line ⏎ Line ⏎ Line
⇒ U I U U I U ర ర ⏎ Line ⏎ Line ⏎ Line
⇒ U I U U I U U I U ర ⏎ Line ⏎ Line ⏎ Line
⇒ U I U U I U U I U U I U ⏎ Line ⏎ Line ⏎ Line
⇒ U I U U I U U I U U I U ⏎ ర ర ర ర ⏎ Line ⏎ Line
⇒ U I U U I U U I U U I U ⏎ U I U ర ర ర ⏎ Line ⏎ Line
⇒ U I U U I U U I U U I U ⏎ U I U U I U ర ర ⏎ Line ⏎ Line
⇒ …
⇒ U I U U I U U I U U I U ⏎ U I U U I U U I U U I U ⏎ U I U U I U U I U U I U ⏎ U I U U I U U I U U I U
```

The result, one line per row:

```
UIUUIUUIUUIU
UIUUIUUIUUIU
UIUUIUUIUUIU
UIUUIUUIUUIU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 4 | 12 | 1 | 13 |

Whole-prosodic automaton (over U, I, ⏎): 52 states.

Grammar file: [`grammars/sragvini.rlg`](../../grammars/sragvini.rlg).

Diagram: [rule card](../../diagrams/meters/sragvini.svg) · [mermaid](../../diagrams/meters/sragvini.md) · [DFA all](../../diagrams/dfa/sragvini__all.svg)

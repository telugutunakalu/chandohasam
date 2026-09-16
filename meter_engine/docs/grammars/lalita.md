# లలిత · lalita

*vrutta* · 4 lines · exactly 12 aksharas per line · prāsa required

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → త భ జ ర                                   # slot all: 4 ganas

# ganas → symbols
త → U U I                                        # ta, 5 matras
భ → U I I                                        # bha, 4 matras
జ → I U I                                        # ja, 4 matras
ర → U I U                                        # ra, 5 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 4 ganas, **త భ జ ర**, i.e. the 12-akshara pattern `UUIUIIIUIUIU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. త (ta) UUI
    2. భ (bha) UII
    3. జ (ja) IUI
    4. ర (ra) UIU
3. **Yati.** The akshara at position 9 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → UUI L1.G2
L1.G2 → UII L1.G3
L1.G3 → IUI L1.G4
L1.G4 → UIU⏎ L2.G1
L2.G1 → UUI L2.G2
L2.G2 → UII L2.G3
L2.G3 → IUI L2.G4
L2.G4 → UIU⏎ L3.G1
L3.G1 → UUI L3.G2
L3.G2 → UII L3.G3
L3.G3 → IUI L3.G4
L3.G4 → UIU⏎ L4.G1
L4.G1 → UUI L4.G2
L4.G2 → UII L4.G3
L4.G3 → IUI L4.G4
L4.G4 → UIU
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 51, each with such a comment, are in [`grammars/lalita.rlg`](../../grammars/lalita.rlg)):

```
Poem → U Poem_UUI_1           # త ta: symbol 1/3 read, 2 to go
Poem_UUI_1 → U Poem_UUI_2     # త ta: symbol 2/3 read, 1 to go
Poem_UUI_2 → I L1.G2          # త ta: symbol 3/3, complete → L1.G2
L1.G2 → U L1.G2_UII_1         # భ bha: symbol 1/3 read, 2 to go
L1.G2_UII_1 → I L1.G2_UII_2   # భ bha: symbol 2/3 read, 1 to go
L1.G2_UII_2 → I L1.G3         # భ bha: symbol 3/3, complete → L1.G3
L1.G3 → I L1.G3_IUI_1         # జ ja: symbol 1/3 read, 2 to go
L1.G3_IUI_1 → U L1.G3_IUI_2   # జ ja: symbol 2/3 read, 1 to go
…
```

The strict grammar has 52 states; minimized, the prosodic automaton has 52 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (21 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ త భ జ ర ⏎ Line ⏎ Line ⏎ Line
⇒ U U I భ జ ర ⏎ Line ⏎ Line ⏎ Line
⇒ U U I U I I జ ర ⏎ Line ⏎ Line ⏎ Line
⇒ U U I U I I I U I ర ⏎ Line ⏎ Line ⏎ Line
⇒ U U I U I I I U I U I U ⏎ Line ⏎ Line ⏎ Line
⇒ U U I U I I I U I U I U ⏎ త భ జ ర ⏎ Line ⏎ Line
⇒ U U I U I I I U I U I U ⏎ U U I భ జ ర ⏎ Line ⏎ Line
⇒ U U I U I I I U I U I U ⏎ U U I U I I జ ర ⏎ Line ⏎ Line
⇒ …
⇒ U U I U I I I U I U I U ⏎ U U I U I I I U I U I U ⏎ U U I U I I I U I U I U ⏎ U U I U I I I U I U I U
```

The result, one line per row:

```
UUIUIIIUIUIU
UUIUIIIUIUIU
UUIUIIIUIUIU
UUIUIIIUIUIU
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

Grammar file: [`grammars/lalita.rlg`](../../grammars/lalita.rlg).

Diagram: [rule card](../../diagrams/meters/lalita.svg) · [mermaid](../../diagrams/meters/lalita.md) · [DFA all](../../diagrams/dfa/lalita__all.svg)

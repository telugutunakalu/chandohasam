# తరళము · taralamu

*vrutta* · 4 lines · exactly 19 aksharas per line · prāsa required

Example from the catalogue:

> పరమపావన! విశ్వభావన! బాంధవప్రకరావనా! (భాగవతము 3-1053)

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → న భ ర స జ జ గురువు                        # slot all: 7 ganas

# ganas → symbols
న → I I I                                        # na, 3 matras
భ → U I I                                        # bha, 4 matras
ర → U I U                                        # ra, 5 matras
స → I I U                                        # sa, 4 matras
జ → I U I                                        # ja, 4 matras
గురువు → U                                       # guruvu, 2 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 7 ganas, **న భ ర స జ జ గురువు**, i.e. the 19-akshara pattern `IIIUIIUIUIIUIUIIUIU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. న (na) III
    2. భ (bha) UII
    3. ర (ra) UIU
    4. స (sa) IIU
    5. జ (ja) IUI
    6. జ (ja) IUI
    7. గురువు (guruvu) U
3. **Yati.** The akshara at position 12 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → III L1.G2
L1.G2 → UII L1.G3
L1.G3 → UIU L1.G4
L1.G4 → IIU L1.G5
L1.G5 → IUI L1.G6
L1.G6 → IUI L1.G7
L1.G7 → U⏎ L2.G1
L2.G1 → III L2.G2
L2.G2 → UII L2.G3
L2.G3 → UIU L2.G4
L2.G4 → IIU L2.G5
L2.G5 → IUI L2.G6
L2.G6 → IUI L2.G7
L2.G7 → U⏎ L3.G1
L3.G1 → III L3.G2
L3.G2 → UII L3.G3
L3.G3 → UIU L3.G4
L3.G4 → IIU L3.G5
L3.G5 → IUI L3.G6
L3.G6 → IUI L3.G7
L3.G7 → U⏎ L4.G1
L4.G1 → III L4.G2
L4.G2 → UII L4.G3
L4.G3 → UIU L4.G4
L4.G4 → IIU L4.G5
L4.G5 → IUI L4.G6
L4.G6 → IUI L4.G7
L4.G7 → U
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 79, each with such a comment, are in [`grammars/taralamu.rlg`](../../grammars/taralamu.rlg)):

```
Poem → I Poem_III_1           # న na: symbol 1/3 read, 2 to go
Poem_III_1 → I Poem_III_2     # న na: symbol 2/3 read, 1 to go
Poem_III_2 → I L1.G2          # న na: symbol 3/3, complete → L1.G2
L1.G2 → U L1.G2_UII_1         # భ bha: symbol 1/3 read, 2 to go
L1.G2_UII_1 → I L1.G2_UII_2   # భ bha: symbol 2/3 read, 1 to go
L1.G2_UII_2 → I L1.G3         # భ bha: symbol 3/3, complete → L1.G3
L1.G3 → U L1.G3_UIU_1         # ర ra: symbol 1/3 read, 2 to go
L1.G3_UIU_1 → I L1.G3_UIU_2   # ర ra: symbol 2/3 read, 1 to go
…
```

The strict grammar has 80 states; minimized, the prosodic automaton has 80 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (33 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ న భ ర స జ జ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I భ ర స జ జ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I U I I ర స జ జ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I U I I U I U స జ జ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I U I I U I U I I U జ జ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I U I I U I U I I U I U I జ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I U I I U I U I I U I U I I U I గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I U I I U I U I I U I U I I U I U ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ I I I U I I U I U I I U I U I I U I U ⏎ I I I U I I U I U I I U I U I I U I U ⏎ I I I U I I U I U I I U I U I I U I U ⏎ I I I U I I U I U I I U I U I I U I U
```

The result, one line per row:

```
IIIUIIUIUIIUIUIIUIU
IIIUIIUIUIIUIUIIUIU
IIIUIIUIUIIUIUIIUIU
IIIUIIUIUIIUIUIIUIU
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

Grammar file: [`grammars/taralamu.rlg`](../../grammars/taralamu.rlg).

Diagram: [rule card](../../diagrams/meters/taralamu.svg) · [mermaid](../../diagrams/meters/taralamu.md) · [DFA all](../../diagrams/dfa/taralamu__all.svg)

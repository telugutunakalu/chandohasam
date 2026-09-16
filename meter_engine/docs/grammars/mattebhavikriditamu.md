# మత్తేభవిక్రీడితము · mattebhavikriditamu

*vrutta* · 4 lines · exactly 20 aksharas per line · prāsa required

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → స భ ర న మ య వ                             # slot all: 7 ganas

# ganas → symbols
స → I I U                                        # sa, 4 matras
భ → U I I                                        # bha, 4 matras
ర → U I U                                        # ra, 5 matras
న → I I I                                        # na, 3 matras
మ → U U U                                        # ma, 6 matras
య → I U U                                        # ya, 5 matras
వ → I U                                          # va, 3 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 7 ganas, **స భ ర న మ య వ**, i.e. the 20-akshara pattern `IIUUIIUIUIIIUUUIUUIU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. స (sa) IIU
    2. భ (bha) UII
    3. ర (ra) UIU
    4. న (na) III
    5. మ (ma) UUU
    6. య (ya) IUU
    7. వ (va) IU
3. **Yati.** The akshara at position 14 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → IIU L1.G2
L1.G2 → UII L1.G3
L1.G3 → UIU L1.G4
L1.G4 → III L1.G5
L1.G5 → UUU L1.G6
L1.G6 → IUU L1.G7
L1.G7 → IU⏎ L2.G1
L2.G1 → IIU L2.G2
L2.G2 → UII L2.G3
L2.G3 → UIU L2.G4
L2.G4 → III L2.G5
L2.G5 → UUU L2.G6
L2.G6 → IUU L2.G7
L2.G7 → IU⏎ L3.G1
L3.G1 → IIU L3.G2
L3.G2 → UII L3.G3
L3.G3 → UIU L3.G4
L3.G4 → III L3.G5
L3.G5 → UUU L3.G6
L3.G6 → IUU L3.G7
L3.G7 → IU⏎ L4.G1
L4.G1 → IIU L4.G2
L4.G2 → UII L4.G3
L4.G3 → UIU L4.G4
L4.G4 → III L4.G5
L4.G5 → UUU L4.G6
L4.G6 → IUU L4.G7
L4.G7 → IU
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 83, each with such a comment, are in [`grammars/mattebhavikriditamu.rlg`](../../grammars/mattebhavikriditamu.rlg)):

```
Poem → I Poem_IIU_1           # స sa: symbol 1/3 read, 2 to go
Poem_IIU_1 → I Poem_IIU_2     # స sa: symbol 2/3 read, 1 to go
Poem_IIU_2 → U L1.G2          # స sa: symbol 3/3, complete → L1.G2
L1.G2 → U L1.G2_UII_1         # భ bha: symbol 1/3 read, 2 to go
L1.G2_UII_1 → I L1.G2_UII_2   # భ bha: symbol 2/3 read, 1 to go
L1.G2_UII_2 → I L1.G3         # భ bha: symbol 3/3, complete → L1.G3
L1.G3 → U L1.G3_UIU_1         # ర ra: symbol 1/3 read, 2 to go
L1.G3_UIU_1 → I L1.G3_UIU_2   # ర ra: symbol 2/3 read, 1 to go
…
```

The strict grammar has 84 states; minimized, the prosodic automaton has 84 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (33 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ స భ ర న మ య వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I U భ ర న మ య వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I U U I I ర న మ య వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I U U I I U I U న మ య వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I U U I I U I U I I I మ య వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I U U I I U I U I I I U U U య వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I U U I I U I U I I I U U U I U U వ ⏎ Line ⏎ Line ⏎ Line
⇒ I I U U I I U I U I I I U U U I U U I U ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ I I U U I I U I U I I I U U U I U U I U ⏎ I I U U I I U I U I I I U U U I U U I U ⏎ I I U U I I U I U I I I U U U I U U I U ⏎ I I U U I I U I U I I I U U U I U U I U
```

The result, one line per row:

```
IIUUIIUIUIIIUUUIUUIU
IIUUIIUIUIIIUUUIUUIU
IIUUIIUIUIIIUUUIUUIU
IIUUIIUIUIIIUUUIUUIU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 7 | 20 | 1 | 21 |

Whole-prosodic automaton (over U, I, ⏎): 84 states.

Grammar file: [`grammars/mattebhavikriditamu.rlg`](../../grammars/mattebhavikriditamu.rlg).

Diagram: [rule card](../../diagrams/meters/mattebhavikriditamu.svg) · [mermaid](../../diagrams/meters/mattebhavikriditamu.md) · [DFA all](../../diagrams/dfa/mattebhavikriditamu__all.svg)

# తురగగతి_రగడ · turagagati_ragada

*jati* · 4 lines per unit, repeatable · between 16 and 24 aksharas per line · prāsa required · prāsa-yati allowed

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Unit | Unit ⏎ Poem                        # one unit
Unit → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → M3 M3 M3 M3 M3 M3 M3 M3                   # slot all: 8 ganas

# gana classes
M3 → వ | హ | న                                   # class m3

# ganas → symbols
వ → I U                                          # va, 3 matras
హ → U I                                          # ha, 3 matras
న → I I I                                        # na, 3 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;
- `Poem → Unit | Unit ⏎ Poem` — the poem is any number of units (right recursion keeps it regular);

## In one sentence

Every line has 8 ganas (m3, m3, m3, m3, m3, m3, m3, m3). Each gana is chosen from a class, so the line length varies.

## The rules, one by one

1. **Line count.** A unit has 4 lines; a poem is any number of such units in a row.
2. **Line recipe.** In order:
    1. any syllable group worth 3 matras: వ IU, హ UI or న III
    2. any syllable group worth 3 matras: వ IU, హ UI or న III
    3. any syllable group worth 3 matras: వ IU, హ UI or న III
    4. any syllable group worth 3 matras: వ IU, హ UI or న III
    5. any syllable group worth 3 matras: వ IU, హ UI or న III
    6. any syllable group worth 3 matras: వ IU, హ UI or న III
    7. any syllable group worth 3 matras: వ IU, హ UI or న III
    8. any syllable group worth 3 matras: వ IU, హ UI or న III
3. **Yati.** at the first akshara of gana 5. Because gana lengths vary, the akshara index of the yati depends on the ganas actually used; the parser reports it per line.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem — or, for this repeatable meter, emits `⏎` and returns to `L1.G1`.

```
Poem → IU L1.G2 | UI L1.G2 | III L1.G2
L1.G1 → IU L1.G2 | UI L1.G2 | III L1.G2
L1.G2 → IU L1.G3 | UI L1.G3 | III L1.G3
L1.G3 → IU L1.G4 | UI L1.G4 | III L1.G4
L1.G4 → IU L1.G5 | UI L1.G5 | III L1.G5
L1.G5 → IU L1.G6 | UI L1.G6 | III L1.G6
L1.G6 → IU L1.G7 | UI L1.G7 | III L1.G7
L1.G7 → IU L1.G8 | UI L1.G8 | III L1.G8
L1.G8 → IU⏎ L2.G1 | UI⏎ L2.G1 | III⏎ L2.G1
L2.G1 → IU L2.G2 | UI L2.G2 | III L2.G2
L2.G2 → IU L2.G3 | UI L2.G3 | III L2.G3
L2.G3 → IU L2.G4 | UI L2.G4 | III L2.G4
L2.G4 → IU L2.G5 | UI L2.G5 | III L2.G5
L2.G5 → IU L2.G6 | UI L2.G6 | III L2.G6
L2.G6 → IU L2.G7 | UI L2.G7 | III L2.G7
L2.G7 → IU L2.G8 | UI L2.G8 | III L2.G8
L2.G8 → IU⏎ L3.G1 | UI⏎ L3.G1 | III⏎ L3.G1
L3.G1 → IU L3.G2 | UI L3.G2 | III L3.G2
L3.G2 → IU L3.G3 | UI L3.G3 | III L3.G3
L3.G3 → IU L3.G4 | UI L3.G4 | III L3.G4
L3.G4 → IU L3.G5 | UI L3.G5 | III L3.G5
L3.G5 → IU L3.G6 | UI L3.G6 | III L3.G6
L3.G6 → IU L3.G7 | UI L3.G7 | III L3.G7
L3.G7 → IU L3.G8 | UI L3.G8 | III L3.G8
L3.G8 → IU⏎ L4.G1 | UI⏎ L4.G1 | III⏎ L4.G1
L4.G1 → IU L4.G2 | UI L4.G2 | III L4.G2
L4.G2 → IU L4.G3 | UI L4.G3 | III L4.G3
L4.G3 → IU L4.G4 | UI L4.G4 | III L4.G4
L4.G4 → IU L4.G5 | UI L4.G5 | III L4.G5
L4.G5 → IU L4.G6 | UI L4.G6 | III L4.G6
L4.G6 → IU L4.G7 | UI L4.G7 | III L4.G7
L4.G7 → IU L4.G8 | UI L4.G8 | III L4.G8
L4.G8 → IU | IU⏎ L1.G1 | UI | UI⏎ L1.G1 | III | III⏎ L1.G1
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 250, each with such a comment, are in [`grammars/turagagati_ragada.rlg`](../../grammars/turagagati_ragada.rlg)):

```
Poem → I Poem_IU_1     # వ va: symbol 1/2 read, 1 to go
Poem_IU_1 → U L1.G2    # వ va: symbol 2/2, complete → L1.G2
L1.G1 → I L1.G1_IU_1   # వ va: symbol 1/2 read, 1 to go
L1.G1_IU_1 → U L1.G2   # వ va: symbol 2/2, complete → L1.G2
Poem → U Poem_UI_1     # హ ha: symbol 1/2 read, 1 to go
Poem_UI_1 → I L1.G2    # హ ha: symbol 2/2, complete → L1.G2
L1.G1 → U L1.G1_UI_1   # హ ha: symbol 1/2 read, 1 to go
L1.G1_UI_1 → I L1.G2   # హ ha: symbol 2/2, complete → L1.G2
…
```

The strict grammar has 182 states; minimized, the prosodic automaton has 100 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (70 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Unit
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ M3 M3 M3 M3 M3 M3 M3 M3 ⏎ Line ⏎ Line ⏎ Line
⇒ వ M3 M3 M3 M3 M3 M3 M3 ⏎ Line ⏎ Line ⏎ Line
⇒ I U M3 M3 M3 M3 M3 M3 M3 ⏎ Line ⏎ Line ⏎ Line
⇒ I U న M3 M3 M3 M3 M3 M3 ⏎ Line ⏎ Line ⏎ Line
⇒ I U I I I M3 M3 M3 M3 M3 M3 ⏎ Line ⏎ Line ⏎ Line
⇒ I U I I I హ M3 M3 M3 M3 M3 ⏎ Line ⏎ Line ⏎ Line
⇒ I U I I I U I M3 M3 M3 M3 M3 ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ I U I I I U I I U U I I U I U U I ⏎ I U U I I U I I I I I I I U I U I I I ⏎ I I I I I I I I I I U U I I U U I I U ⏎ U I I U U I I I I I U I U U I I I I
```

The result, one line per row:

```
IUIIIUIIUUIIUIUUI
IUUIIUIIIIIIIUIUIII
IIIIIIIIIIUUIIUUIIU
UIIUUIIIIIUIUUIIII
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 8 | 16–24 | 6,561 | 25 |

Whole-prosodic automaton (over U, I, ⏎): 100 states.

Grammar file: [`grammars/turagagati_ragada.rlg`](../../grammars/turagagati_ragada.rlg).

Diagram: [rule card](../../diagrams/meters/turagagati_ragada.svg) · [mermaid](../../diagrams/meters/turagagati_ragada.md) · [DFA all](../../diagrams/dfa/turagagati_ragada__all.svg)

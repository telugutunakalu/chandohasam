# ద్విపద · dvipada

*jati* · 2 lines per unit, repeatable · between 11 and 15 aksharas per line · prāsa required

Example from the catalogue:

> శ్రీకామినీనాధుజితదైత్యనాధు లోకరక్షణకృత్యులోకైకనిత్యు

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Unit | Unit ⏎ Poem                        # one unit
Unit → Line ⏎ Line                               # 2 lines

# lines
Line → Indra Indra Indra Surya                   # slot all: 4 ganas

# gana classes
Indra → భ | ర | త | నల | నగ | సల                 # class indra
Surya → న | హ                                    # class surya

# ganas → symbols
భ → U I I                                        # bha, 4 matras
ర → U I U                                        # ra, 5 matras
త → U U I                                        # ta, 5 matras
నల → I I I I                                     # nala, 4 matras
నగ → I I I U                                     # naga, 5 matras
సల → I I U I                                     # sala, 5 matras
న → I I I                                        # na, 3 matras
హ → U I                                          # ha, 3 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;
- `Poem → Unit | Unit ⏎ Poem` — the poem is any number of units (right recursion keeps it regular);

## In one sentence

Every line has 4 ganas (indra, indra, indra, surya). Each gana is chosen from a class, so the line length varies.

## The rules, one by one

1. **Line count.** A unit has 2 lines; a poem is any number of such units in a row.
2. **Line recipe.** In order:
    1. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    2. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    3. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    4. a సూర్యగణము (surya gana): న III or హ UI
3. **Yati.** at the first akshara of gana 3. Because gana lengths vary, the akshara index of the yati depends on the ganas actually used; the parser reports it per line.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem — or, for this repeatable meter, emits `⏎` and returns to `L1.G1`.

```
Poem → UII L1.G2 | UIU L1.G2 | UUI L1.G2 | IIII L1.G2 | IIIU L1.G2 | IIUI L1.G2
L1.G1 → UII L1.G2 | UIU L1.G2 | UUI L1.G2 | IIII L1.G2 | IIIU L1.G2 | IIUI L1.G2
L1.G2 → UII L1.G3 | UIU L1.G3 | UUI L1.G3 | IIII L1.G3 | IIIU L1.G3 | IIUI L1.G3
L1.G3 → UII L1.G4 | UIU L1.G4 | UUI L1.G4 | IIII L1.G4 | IIIU L1.G4 | IIUI L1.G4
L1.G4 → III⏎ L2.G1 | UI⏎ L2.G1
L2.G1 → UII L2.G2 | UIU L2.G2 | UUI L2.G2 | IIII L2.G2 | IIIU L2.G2 | IIUI L2.G2
L2.G2 → UII L2.G3 | UIU L2.G3 | UUI L2.G3 | IIII L2.G3 | IIIU L2.G3 | IIUI L2.G3
L2.G3 → UII L2.G4 | UIU L2.G4 | UUI L2.G4 | IIII L2.G4 | IIIU L2.G4 | IIUI L2.G4
L2.G4 → III | III⏎ L1.G1 | UI | UI⏎ L1.G1
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 166, each with such a comment, are in [`grammars/dvipada.rlg`](../../grammars/dvipada.rlg)):

```
Poem → U Poem_UII_1           # భ bha: symbol 1/3 read, 2 to go
Poem_UII_1 → I Poem_UII_2     # భ bha: symbol 2/3 read, 1 to go
Poem_UII_2 → I L1.G2          # భ bha: symbol 3/3, complete → L1.G2
L1.G1 → U L1.G1_UII_1         # భ bha: symbol 1/3 read, 2 to go
L1.G1_UII_1 → I L1.G1_UII_2   # భ bha: symbol 2/3 read, 1 to go
L1.G1_UII_2 → I L1.G2         # భ bha: symbol 3/3, complete → L1.G2
Poem → U Poem_UIU_1           # ర ra: symbol 1/3 read, 2 to go
Poem_UIU_1 → I Poem_UIU_2     # ర ra: symbol 2/3 read, 1 to go
…
```

The strict grammar has 128 states; minimized, the prosodic automaton has 38 states.

## One worked derivation

A poem of 2 lines, derived top-down from `Poem` (20 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Unit
⇒ Line ⏎ Line
⇒ Indra Indra Indra Surya ⏎ Line
⇒ ర Indra Indra Surya ⏎ Line
⇒ U I U Indra Indra Surya ⏎ Line
⇒ U I U ర Indra Surya ⏎ Line
⇒ U I U U I U Indra Surya ⏎ Line
⇒ U I U U I U సల Surya ⏎ Line
⇒ U I U U I U I I U I Surya ⏎ Line
⇒ …
⇒ U I U U I U I I U I U I ⏎ I I I I U I I I I I I U I
```

The result, one line per row:

```
UIUUIUIIUIUI
IIIIUIIIIIIUI
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 4 | 11–15 | 432 | 19 |

Whole-prosodic automaton (over U, I, ⏎): 38 states.

Grammar file: [`grammars/dvipada.rlg`](../../grammars/dvipada.rlg).

Diagram: [rule card](../../diagrams/meters/dvipada.svg) · [mermaid](../../diagrams/meters/dvipada.md) · [DFA all](../../diagrams/dfa/dvipada__all.svg)

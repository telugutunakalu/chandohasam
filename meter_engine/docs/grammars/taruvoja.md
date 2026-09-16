# తరువోజ · taruvoja

*jati* · 4 lines · between 22 and 30 aksharas per line · prāsa required

Example from the catalogue:

> ఏ నెల్ల ప్రొద్దు నా యెడ లోనఁ దలఁతు నీయభిప్రాయంబ యిది దారుణంబు

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → Indra Indra Indra Surya Indra Indra Indra Surya # slot all: 8 ganas

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

## In one sentence

Every line has 8 ganas (indra, indra, indra, surya, indra, indra, indra, surya). Each gana is chosen from a class, so the line length varies.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    2. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    3. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    4. a సూర్యగణము (surya gana): న III or హ UI
    5. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    6. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    7. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    8. a సూర్యగణము (surya gana): న III or హ UI
3. **Yati.** at the first akshara of gana 3, 5 or 7. Because gana lengths vary, the akshara index of the yati depends on the ganas actually used; the parser reports it per line.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → UII L1.G2 | UIU L1.G2 | UUI L1.G2 | IIII L1.G2 | IIIU L1.G2 | IIUI L1.G2
L1.G2 → UII L1.G3 | UIU L1.G3 | UUI L1.G3 | IIII L1.G3 | IIIU L1.G3 | IIUI L1.G3
L1.G3 → UII L1.G4 | UIU L1.G4 | UUI L1.G4 | IIII L1.G4 | IIIU L1.G4 | IIUI L1.G4
L1.G4 → III L1.G5 | UI L1.G5
L1.G5 → UII L1.G6 | UIU L1.G6 | UUI L1.G6 | IIII L1.G6 | IIIU L1.G6 | IIUI L1.G6
L1.G6 → UII L1.G7 | UIU L1.G7 | UUI L1.G7 | IIII L1.G7 | IIIU L1.G7 | IIUI L1.G7
L1.G7 → UII L1.G8 | UIU L1.G8 | UUI L1.G8 | IIII L1.G8 | IIIU L1.G8 | IIUI L1.G8
L1.G8 → III⏎ L2.G1 | UI⏎ L2.G1
L2.G1 → UII L2.G2 | UIU L2.G2 | UUI L2.G2 | IIII L2.G2 | IIIU L2.G2 | IIUI L2.G2
L2.G2 → UII L2.G3 | UIU L2.G3 | UUI L2.G3 | IIII L2.G3 | IIIU L2.G3 | IIUI L2.G3
L2.G3 → UII L2.G4 | UIU L2.G4 | UUI L2.G4 | IIII L2.G4 | IIIU L2.G4 | IIUI L2.G4
L2.G4 → III L2.G5 | UI L2.G5
L2.G5 → UII L2.G6 | UIU L2.G6 | UUI L2.G6 | IIII L2.G6 | IIIU L2.G6 | IIUI L2.G6
L2.G6 → UII L2.G7 | UIU L2.G7 | UUI L2.G7 | IIII L2.G7 | IIIU L2.G7 | IIUI L2.G7
L2.G7 → UII L2.G8 | UIU L2.G8 | UUI L2.G8 | IIII L2.G8 | IIIU L2.G8 | IIUI L2.G8
L2.G8 → III⏎ L3.G1 | UI⏎ L3.G1
L3.G1 → UII L3.G2 | UIU L3.G2 | UUI L3.G2 | IIII L3.G2 | IIIU L3.G2 | IIUI L3.G2
L3.G2 → UII L3.G3 | UIU L3.G3 | UUI L3.G3 | IIII L3.G3 | IIIU L3.G3 | IIUI L3.G3
L3.G3 → UII L3.G4 | UIU L3.G4 | UUI L3.G4 | IIII L3.G4 | IIIU L3.G4 | IIUI L3.G4
L3.G4 → III L3.G5 | UI L3.G5
L3.G5 → UII L3.G6 | UIU L3.G6 | UUI L3.G6 | IIII L3.G6 | IIIU L3.G6 | IIUI L3.G6
L3.G6 → UII L3.G7 | UIU L3.G7 | UUI L3.G7 | IIII L3.G7 | IIIU L3.G7 | IIUI L3.G7
L3.G7 → UII L3.G8 | UIU L3.G8 | UUI L3.G8 | IIII L3.G8 | IIIU L3.G8 | IIUI L3.G8
L3.G8 → III⏎ L4.G1 | UI⏎ L4.G1
L4.G1 → UII L4.G2 | UIU L4.G2 | UUI L4.G2 | IIII L4.G2 | IIIU L4.G2 | IIUI L4.G2
L4.G2 → UII L4.G3 | UIU L4.G3 | UUI L4.G3 | IIII L4.G3 | IIIU L4.G3 | IIUI L4.G3
L4.G3 → UII L4.G4 | UIU L4.G4 | UUI L4.G4 | IIII L4.G4 | IIIU L4.G4 | IIUI L4.G4
L4.G4 → III L4.G5 | UI L4.G5
L4.G5 → UII L4.G6 | UIU L4.G6 | UUI L4.G6 | IIII L4.G6 | IIIU L4.G6 | IIUI L4.G6
L4.G6 → UII L4.G7 | UIU L4.G7 | UUI L4.G7 | IIII L4.G7 | IIIU L4.G7 | IIUI L4.G7
L4.G7 → UII L4.G8 | UIU L4.G8 | UUI L4.G8 | IIII L4.G8 | IIIU L4.G8 | IIUI L4.G8
L4.G8 → III | UI
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 550, each with such a comment, are in [`grammars/taruvoja.rlg`](../../grammars/taruvoja.rlg)):

```
Poem → U Poem_UII_1         # భ bha: symbol 1/3 read, 2 to go
Poem_UII_1 → I Poem_UII_2   # భ bha: symbol 2/3 read, 1 to go
Poem_UII_2 → I L1.G2        # భ bha: symbol 3/3, complete → L1.G2
Poem → U Poem_UIU_1         # ర ra: symbol 1/3 read, 2 to go
Poem_UIU_1 → I Poem_UIU_2   # ర ra: symbol 2/3 read, 1 to go
Poem_UIU_2 → U L1.G2        # ర ra: symbol 3/3, complete → L1.G2
Poem → U Poem_UUI_1         # త ta: symbol 1/3 read, 2 to go
Poem_UUI_1 → U Poem_UUI_2   # త ta: symbol 2/3 read, 1 to go
…
```

The strict grammar has 423 states; minimized, the prosodic automaton has 148 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (69 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ Indra Indra Indra Surya Indra Indra Indra Surya ⏎ Line ⏎ Line ⏎ Line
⇒ భ Indra Indra Surya Indra Indra Indra Surya ⏎ Line ⏎ Line ⏎ Line
⇒ U I I Indra Indra Surya Indra Indra Indra Surya ⏎ Line ⏎ Line ⏎ Line
⇒ U I I నల Indra Surya Indra Indra Indra Surya ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I I I I Indra Surya Indra Indra Indra Surya ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I I I I నగ Surya Indra Indra Indra Surya ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I I I I I I I U Surya Indra Indra Indra Surya ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I I I I I I I U న Indra Indra Indra Surya ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ U I I I I I I I I I U I I I U U I U I I I I I U I I I ⏎ I I U I I I I I I I I U U I U I U I I I U I I U I I I I ⏎ I I I U I I U I I I I U U I I I U I I I I U I I U I I I I ⏎ I I U I I I I U U I I U I I I I U I I I U I I I U I I I
```

The result, one line per row:

```
UIIIIIIIIIUIIIUUIUIIIIIUIII
IIUIIIIIIIIUUIUIUIIIUIIUIIII
IIIUIIUIIIIUUIIIUIIIIUIIUIIII
IIUIIIIUUIIUIIIIUIIIUIIIUIII
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 8 | 22–30 | 186,624 | 37 |

Whole-prosodic automaton (over U, I, ⏎): 148 states.

Grammar file: [`grammars/taruvoja.rlg`](../../grammars/taruvoja.rlg).

Diagram: [rule card](../../diagrams/meters/taruvoja.svg) · [mermaid](../../diagrams/meters/taruvoja.md) · [DFA all](../../diagrams/dfa/taruvoja__all.svg)

# తేటగీతి · tetagiti

*upajati* · 4 lines · between 12 and 17 aksharas per line · prāsa not required · prāsa-yati allowed

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → Surya Indra Indra Surya Surya             # slot all: 5 ganas

# gana classes
Surya → న | హ                                    # class surya
Indra → భ | ర | త | నల | నగ | సల                 # class indra

# ganas → symbols
న → I I I                                        # na, 3 matras
హ → U I                                          # ha, 3 matras
భ → U I I                                        # bha, 4 matras
ర → U I U                                        # ra, 5 matras
త → U U I                                        # ta, 5 matras
నల → I I I I                                     # nala, 4 matras
నగ → I I I U                                     # naga, 5 matras
సల → I I U I                                     # sala, 5 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line has 5 ganas (surya, indra, indra, surya, surya). Each gana is chosen from a class, so the line length varies.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. a సూర్యగణము (surya gana): న III or హ UI
    2. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    3. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    4. a సూర్యగణము (surya gana): న III or హ UI
    5. a సూర్యగణము (surya gana): న III or హ UI
3. **Yati.** at the first akshara of gana 4. Because gana lengths vary, the akshara index of the yati depends on the ganas actually used; the parser reports it per line.
4. **Prāsa.** Not required. Prāsa-yati (rhyme at the yati position) is allowed instead of yati-maitri.
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → III L1.G2 | UI L1.G2
L1.G2 → UII L1.G3 | UIU L1.G3 | UUI L1.G3 | IIII L1.G3 | IIIU L1.G3 | IIUI L1.G3
L1.G3 → UII L1.G4 | UIU L1.G4 | UUI L1.G4 | IIII L1.G4 | IIIU L1.G4 | IIUI L1.G4
L1.G4 → III L1.G5 | UI L1.G5
L1.G5 → III⏎ L2.G1 | UI⏎ L2.G1
L2.G1 → III L2.G2 | UI L2.G2
L2.G2 → UII L2.G3 | UIU L2.G3 | UUI L2.G3 | IIII L2.G3 | IIIU L2.G3 | IIUI L2.G3
L2.G3 → UII L2.G4 | UIU L2.G4 | UUI L2.G4 | IIII L2.G4 | IIIU L2.G4 | IIUI L2.G4
L2.G4 → III L2.G5 | UI L2.G5
L2.G5 → III⏎ L3.G1 | UI⏎ L3.G1
L3.G1 → III L3.G2 | UI L3.G2
L3.G2 → UII L3.G3 | UIU L3.G3 | UUI L3.G3 | IIII L3.G3 | IIIU L3.G3 | IIUI L3.G3
L3.G3 → UII L3.G4 | UIU L3.G4 | UUI L3.G4 | IIII L3.G4 | IIIU L3.G4 | IIUI L3.G4
L3.G4 → III L3.G5 | UI L3.G5
L3.G5 → III⏎ L4.G1 | UI⏎ L4.G1
L4.G1 → III L4.G2 | UI L4.G2
L4.G2 → UII L4.G3 | UIU L4.G3 | UUI L4.G3 | IIII L4.G3 | IIIU L4.G3 | IIUI L4.G3
L4.G3 → UII L4.G4 | UIU L4.G4 | UUI L4.G4 | IIII L4.G4 | IIIU L4.G4 | IIUI L4.G4
L4.G4 → III L4.G5 | UI L4.G5
L4.G5 → III | UI
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 234, each with such a comment, are in [`grammars/tetagiti.rlg`](../../grammars/tetagiti.rlg)):

```
Poem → I Poem_III_1           # న na: symbol 1/3 read, 2 to go
Poem_III_1 → I Poem_III_2     # న na: symbol 2/3 read, 1 to go
Poem_III_2 → I L1.G2          # న na: symbol 3/3, complete → L1.G2
Poem → U Poem_UI_1            # హ ha: symbol 1/2 read, 1 to go
Poem_UI_1 → I L1.G2           # హ ha: symbol 2/2, complete → L1.G2
L1.G2 → U L1.G2_UII_1         # భ bha: symbol 1/3 read, 2 to go
L1.G2_UII_1 → I L1.G2_UII_2   # భ bha: symbol 2/3 read, 1 to go
L1.G2_UII_2 → I L1.G3         # భ bha: symbol 3/3, complete → L1.G3
…
```

The strict grammar has 183 states; minimized, the prosodic automaton has 80 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (45 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ Surya Indra Indra Surya Surya ⏎ Line ⏎ Line ⏎ Line
⇒ హ Indra Indra Surya Surya ⏎ Line ⏎ Line ⏎ Line
⇒ U I Indra Indra Surya Surya ⏎ Line ⏎ Line ⏎ Line
⇒ U I సల Indra Surya Surya ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I Indra Surya Surya ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I సల Surya Surya ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I I I U I Surya Surya ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I I I U I హ Surya ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ U I I I U I I I U I U I U I ⏎ U I I I I U U I I U I I I I ⏎ U I U I U I I U I I I I I I I ⏎ I I I I I I U I I I U U I I I I
```

The result, one line per row:

```
UIIIUIIIUIUIUI
UIIIIUUIIUIIII
UIUIUIIUIIIIIII
IIIIIIUIIIUUIIII
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 5 | 12–17 | 288 | 20 |

Whole-prosodic automaton (over U, I, ⏎): 80 states.

Grammar file: [`grammars/tetagiti.rlg`](../../grammars/tetagiti.rlg).

Diagram: [rule card](../../diagrams/meters/tetagiti.svg) · [mermaid](../../diagrams/meters/tetagiti.md) · [DFA all](../../diagrams/dfa/tetagiti__all.svg)

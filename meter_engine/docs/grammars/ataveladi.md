# ఆటవెలది · ataveladi

*upajati* · 4 lines · between 10 and 17 aksharas per line · prāsa not required · prāsa-yati allowed

Example from the catalogue:

> ఇనగణత్రయంబునింద్రద్వయంబును హంసపంచకంబు నాటి వెలది

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line_odd ⏎ Line_even ⏎ Line_odd ⏎ Line_even # 4 lines

# lines
Line_odd → Surya Surya Surya Indra Indra         # slot odd: 5 ganas
Line_even → Surya Surya Surya Surya Surya        # slot even: 5 ganas

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

Line 1, 3 has 5 ganas (surya, surya, surya, indra, indra); line 2, 4 has 5 ganas (surya, surya, surya, surya, surya). Each gana is chosen from a class, so the line length varies.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Two kinds of line.** Lines follow the pattern odd even odd even: slot *odd* is line 1, 3; slot *even* is line 2, 4.
3. **Recipe for slot *odd*.** In order:
    1. a సూర్యగణము (surya gana): న III or హ UI
    2. a సూర్యగణము (surya gana): న III or హ UI
    3. a సూర్యగణము (surya gana): న III or హ UI
    4. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
    5. an ఇంద్రగణము (indra gana): భ UII, ర UIU, త UUI, నల IIII, నగ IIIU or సల IIUI
4. **Recipe for slot *even*.** In order:
    1. a సూర్యగణము (surya gana): న III or హ UI
    2. a సూర్యగణము (surya gana): న III or హ UI
    3. a సూర్యగణము (surya gana): న III or హ UI
    4. a సూర్యగణము (surya gana): న III or హ UI
    5. a సూర్యగణము (surya gana): న III or హ UI
5. **Yati.** at the first akshara of gana 4 in slot *odd*; at the first akshara of gana 4 in slot *even*. Because gana lengths vary, the akshara index of the yati depends on the ganas actually used; the parser reports it per line.
6. **Prāsa.** Not required. Prāsa-yati (rhyme at the yati position) is allowed instead of yati-maitri.
7. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → III L1.G2 | UI L1.G2
L1.G2 → III L1.G3 | UI L1.G3
L1.G3 → III L1.G4 | UI L1.G4
L1.G4 → UII L1.G5 | UIU L1.G5 | UUI L1.G5 | IIII L1.G5 | IIIU L1.G5 | IIUI L1.G5
L1.G5 → UII⏎ L2.G1 | UIU⏎ L2.G1 | UUI⏎ L2.G1 | IIII⏎ L2.G1 | IIIU⏎ L2.G1 | IIUI⏎ L2.G1
L2.G1 → III L2.G2 | UI L2.G2
L2.G2 → III L2.G3 | UI L2.G3
L2.G3 → III L2.G4 | UI L2.G4
L2.G4 → III L2.G5 | UI L2.G5
L2.G5 → III⏎ L3.G1 | UI⏎ L3.G1
L3.G1 → III L3.G2 | UI L3.G2
L3.G2 → III L3.G3 | UI L3.G3
L3.G3 → III L3.G4 | UI L3.G4
L3.G4 → UII L3.G5 | UIU L3.G5 | UUI L3.G5 | IIII L3.G5 | IIIU L3.G5 | IIUI L3.G5
L3.G5 → UII⏎ L4.G1 | UIU⏎ L4.G1 | UUI⏎ L4.G1 | IIII⏎ L4.G1 | IIIU⏎ L4.G1 | IIUI⏎ L4.G1
L4.G1 → III L4.G2 | UI L4.G2
L4.G2 → III L4.G3 | UI L4.G3
L4.G3 → III L4.G4 | UI L4.G4
L4.G4 → III L4.G5 | UI L4.G5
L4.G5 → III | UI
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 178, each with such a comment, are in [`grammars/ataveladi.rlg`](../../grammars/ataveladi.rlg)):

```
Poem → I Poem_III_1           # న na: symbol 1/3 read, 2 to go
Poem_III_1 → I Poem_III_2     # న na: symbol 2/3 read, 1 to go
Poem_III_2 → I L1.G2          # న na: symbol 3/3, complete → L1.G2
Poem → U Poem_UI_1            # హ ha: symbol 1/2 read, 1 to go
Poem_UI_1 → I L1.G2           # హ ha: symbol 2/2, complete → L1.G2
L1.G2 → I L1.G2_III_1         # న na: symbol 1/3 read, 2 to go
L1.G2_III_1 → I L1.G2_III_2   # న na: symbol 2/3 read, 1 to go
L1.G2_III_2 → I L1.G3         # న na: symbol 3/3, complete → L1.G3
…
```

The strict grammar has 143 states; minimized, the prosodic automaton has 72 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (45 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line_odd ⏎ Line_even ⏎ Line_odd ⏎ Line_even
⇒ Surya Surya Surya Indra Indra ⏎ Line_even ⏎ Line_odd ⏎ Line_even
⇒ న Surya Surya Indra Indra ⏎ Line_even ⏎ Line_odd ⏎ Line_even
⇒ I I I Surya Surya Indra Indra ⏎ Line_even ⏎ Line_odd ⏎ Line_even
⇒ I I I న Surya Indra Indra ⏎ Line_even ⏎ Line_odd ⏎ Line_even
⇒ I I I I I I Surya Indra Indra ⏎ Line_even ⏎ Line_odd ⏎ Line_even
⇒ I I I I I I న Indra Indra ⏎ Line_even ⏎ Line_odd ⏎ Line_even
⇒ I I I I I I I I I Indra Indra ⏎ Line_even ⏎ Line_odd ⏎ Line_even
⇒ I I I I I I I I I భ Indra ⏎ Line_even ⏎ Line_odd ⏎ Line_even
⇒ …
⇒ I I I I I I I I I U I I I I I U ⏎ U I I I I I I I I I I I I I ⏎ U I I I I I I I U I I U I I ⏎ I I I U I U I U I I I I
```

The result, one line per row:

```
IIIIIIIIIUIIIIIU
UIIIIIIIIIIIII
UIIIIIIIUIIUII
IIIUIUIUIIII
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| odd | 5 | 12–17 | 288 | 20 |
| even | 5 | 10–15 | 32 | 16 |

Whole-prosodic automaton (over U, I, ⏎): 72 states.

Grammar file: [`grammars/ataveladi.rlg`](../../grammars/ataveladi.rlg).

Diagram: [rule card](../../diagrams/meters/ataveladi.svg) · [mermaid](../../diagrams/meters/ataveladi.md) · [DFA odd](../../diagrams/dfa/ataveladi__odd.svg) · [DFA even](../../diagrams/dfa/ataveladi__even.svg)

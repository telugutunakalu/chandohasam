# లయగ్రాహి · layagrahi

*vrutta* · 4 lines · exactly 30 aksharas per line · prāsa required · prāsa-yati allowed

Example from the catalogue:

> కమ్మని లతంతముల కుమ్మొనసి వచ్చు మధు పమ్ముల సుగీతనిన దమ్ములెసఁగెం జూ

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → భ జ స న భ జ స న భ య                       # slot all: 10 ganas

# ganas → symbols
భ → U I I                                        # bha, 4 matras
జ → I U I                                        # ja, 4 matras
స → I I U                                        # sa, 4 matras
న → I I I                                        # na, 3 matras
య → I U U                                        # ya, 5 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 10 ganas, **భ జ స న భ జ స న భ య**, i.e. the 30-akshara pattern `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. భ (bha) UII
    2. జ (ja) IUI
    3. స (sa) IIU
    4. న (na) III
    5. భ (bha) UII
    6. జ (ja) IUI
    7. స (sa) IIU
    8. న (na) III
    9. భ (bha) UII
    10. య (ya) IUU
3. **Yati.** The akshara at position 9, 17 or 25 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).
6. **Printing.** Each pada is conventionally printed as 2 half-lines; the identifier joins them, so a 8-line text is read as 4 padas.

Note: the yati points take ప్రాసయతి (the second akshara of each segment rhymes with the pāda's prāsa), not yati-maitri; Pothana prints each pāda as two half-lines

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → UII L1.G2
L1.G2 → IUI L1.G3
L1.G3 → IIU L1.G4
L1.G4 → III L1.G5
L1.G5 → UII L1.G6
L1.G6 → IUI L1.G7
L1.G7 → IIU L1.G8
L1.G8 → III L1.G9
L1.G9 → UII L1.G10
L1.G10 → IUU⏎ L2.G1
L2.G1 → UII L2.G2
L2.G2 → IUI L2.G3
L2.G3 → IIU L2.G4
L2.G4 → III L2.G5
L2.G5 → UII L2.G6
L2.G6 → IUI L2.G7
L2.G7 → IIU L2.G8
L2.G8 → III L2.G9
L2.G9 → UII L2.G10
L2.G10 → IUU⏎ L3.G1
L3.G1 → UII L3.G2
L3.G2 → IUI L3.G3
L3.G3 → IIU L3.G4
L3.G4 → III L3.G5
L3.G5 → UII L3.G6
L3.G6 → IUI L3.G7
L3.G7 → IIU L3.G8
L3.G8 → III L3.G9
L3.G9 → UII L3.G10
L3.G10 → IUU⏎ L4.G1
L4.G1 → UII L4.G2
L4.G2 → IUI L4.G3
L4.G3 → IIU L4.G4
L4.G4 → III L4.G5
L4.G5 → UII L4.G6
L4.G6 → IUI L4.G7
L4.G7 → IIU L4.G8
L4.G8 → III L4.G9
L4.G9 → UII L4.G10
L4.G10 → IUU
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 123, each with such a comment, are in [`grammars/layagrahi.rlg`](../../grammars/layagrahi.rlg)):

```
Poem → U Poem_UII_1           # భ bha: symbol 1/3 read, 2 to go
Poem_UII_1 → I Poem_UII_2     # భ bha: symbol 2/3 read, 1 to go
Poem_UII_2 → I L1.G2          # భ bha: symbol 3/3, complete → L1.G2
L1.G2 → I L1.G2_IUI_1         # జ ja: symbol 1/3 read, 2 to go
L1.G2_IUI_1 → U L1.G2_IUI_2   # జ ja: symbol 2/3 read, 1 to go
L1.G2_IUI_2 → I L1.G3         # జ ja: symbol 3/3, complete → L1.G3
L1.G3 → I L1.G3_IIU_1         # స sa: symbol 1/3 read, 2 to go
L1.G3_IIU_1 → I L1.G3_IIU_2   # స sa: symbol 2/3 read, 1 to go
…
```

The strict grammar has 124 states; minimized, the prosodic automaton has 124 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (45 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ భ జ స న భ జ స న భ య ⏎ Line ⏎ Line ⏎ Line
⇒ U I I జ స న భ జ స న భ య ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I స న భ జ స న భ య ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I I I U న భ జ స న భ య ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I I I U I I I భ జ స న భ య ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I I I U I I I U I I జ స న భ య ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I I I U I I I U I I I U I స న భ య ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I I I U I I I U I I I U I I I U న భ య ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ U I I I U I I I U I I I U I I I U I I I U I I I U I I I U U ⏎ U I I I U I I I U I I I U I I I U I I I U I I I U I I I U U ⏎ U I I I U I I I U I I I U I I I U I I I U I I I U I I I U U ⏎ U I I I U I I I U I I I U I I I U I I I U I I I U I I I U U
```

The result, one line per row:

```
UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU
UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU
UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU
UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 10 | 30 | 1 | 31 |

Whole-prosodic automaton (over U, I, ⏎): 124 states.

Grammar file: [`grammars/layagrahi.rlg`](../../grammars/layagrahi.rlg).

Diagram: [rule card](../../diagrams/meters/layagrahi.svg) · [mermaid](../../diagrams/meters/layagrahi.md) · [DFA all](../../diagrams/dfa/layagrahi__all.svg)

# మంగళమహాశ్రీ · mangalamahasri

*vrutta* · 4 lines · exactly 26 aksharas per line · prāsa required

Example from the catalogue:

> చిత్తములఁ జూపులను జిత్తజుని తండ్రిపయిఁ జెంది గజదంతియతు లొందన్‌

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → భ జ స న భ జ స న గా                        # slot all: 9 ganas

# ganas → symbols
భ → U I I                                        # bha, 4 matras
జ → I U I                                        # ja, 4 matras
స → I I U                                        # sa, 4 matras
న → I I I                                        # na, 3 matras
గా → U U                                         # gaa, 4 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 9 ganas, **భ జ స న భ జ స న గా**, i.e. the 26-akshara pattern `UIIIUIIIUIIIUIIIUIIIUIIIUU`. There is no choice anywhere in the line; the four lines are identical in weight.

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
    9. గా (gaa) UU
3. **Yati.** The akshara at position 9 or 17 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

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
L1.G9 → UU⏎ L2.G1
L2.G1 → UII L2.G2
L2.G2 → IUI L2.G3
L2.G3 → IIU L2.G4
L2.G4 → III L2.G5
L2.G5 → UII L2.G6
L2.G6 → IUI L2.G7
L2.G7 → IIU L2.G8
L2.G8 → III L2.G9
L2.G9 → UU⏎ L3.G1
L3.G1 → UII L3.G2
L3.G2 → IUI L3.G3
L3.G3 → IIU L3.G4
L3.G4 → III L3.G5
L3.G5 → UII L3.G6
L3.G6 → IUI L3.G7
L3.G7 → IIU L3.G8
L3.G8 → III L3.G9
L3.G9 → UU⏎ L4.G1
L4.G1 → UII L4.G2
L4.G2 → IUI L4.G3
L4.G3 → IIU L4.G4
L4.G4 → III L4.G5
L4.G5 → UII L4.G6
L4.G6 → IUI L4.G7
L4.G7 → IIU L4.G8
L4.G8 → III L4.G9
L4.G9 → UU
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 107, each with such a comment, are in [`grammars/mangalamahasri.rlg`](../../grammars/mangalamahasri.rlg)):

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

The strict grammar has 108 states; minimized, the prosodic automaton has 108 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (41 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ భ జ స న భ జ స న గా ⏎ Line ⏎ Line ⏎ Line
⇒ U I I జ స న భ జ స న గా ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I స న భ జ స న గా ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I I I U న భ జ స న గా ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I I I U I I I భ జ స న గా ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I I I U I I I U I I జ స న గా ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I I I U I I I U I I I U I స న గా ⏎ Line ⏎ Line ⏎ Line
⇒ U I I I U I I I U I I I U I I I U I I I U న గా ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ U I I I U I I I U I I I U I I I U I I I U I I I U U ⏎ U I I I U I I I U I I I U I I I U I I I U I I I U U ⏎ U I I I U I I I U I I I U I I I U I I I U I I I U U ⏎ U I I I U I I I U I I I U I I I U I I I U I I I U U
```

The result, one line per row:

```
UIIIUIIIUIIIUIIIUIIIUIIIUU
UIIIUIIIUIIIUIIIUIIIUIIIUU
UIIIUIIIUIIIUIIIUIIIUIIIUU
UIIIUIIIUIIIUIIIUIIIUIIIUU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 9 | 26 | 1 | 27 |

Whole-prosodic automaton (over U, I, ⏎): 108 states.

Grammar file: [`grammars/mangalamahasri.rlg`](../../grammars/mangalamahasri.rlg).

Diagram: [rule card](../../diagrams/meters/mangalamahasri.svg) · [mermaid](../../diagrams/meters/mangalamahasri.md) · [DFA all](../../diagrams/dfa/mangalamahasri__all.svg)

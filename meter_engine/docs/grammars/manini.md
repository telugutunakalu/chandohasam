# మానిని · manini

*vrutta* · 4 lines · exactly 22 aksharas per line · prāsa required

Example from the catalogue:

> కొన్నెలపువ్వును గోఱలపాఁగయుఁ గూర్చిన కెంజడ కొప్పునకున్‌

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → భ భ భ భ భ భ భ గురువు                      # slot all: 8 ganas

# ganas → symbols
భ → U I I                                        # bha, 4 matras
గురువు → U                                       # guruvu, 2 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 8 ganas, **భ భ భ భ భ భ భ గురువు**, i.e. the 22-akshara pattern `UIIUIIUIIUIIUIIUIIUIIU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. భ (bha) UII
    2. భ (bha) UII
    3. భ (bha) UII
    4. భ (bha) UII
    5. భ (bha) UII
    6. భ (bha) UII
    7. భ (bha) UII
    8. గురువు (guruvu) U
3. **Yati.** The akshara at position 7, 13 or 19 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).
6. **Printing.** Each pada is conventionally printed as 2 half-lines; the identifier joins them, so a 8-line text is read as 4 padas.

Note: Pothana prints each pāda as two half-lines (10.1-214); both printings are identified

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → UII L1.G2
L1.G2 → UII L1.G3
L1.G3 → UII L1.G4
L1.G4 → UII L1.G5
L1.G5 → UII L1.G6
L1.G6 → UII L1.G7
L1.G7 → UII L1.G8
L1.G8 → U⏎ L2.G1
L2.G1 → UII L2.G2
L2.G2 → UII L2.G3
L2.G3 → UII L2.G4
L2.G4 → UII L2.G5
L2.G5 → UII L2.G6
L2.G6 → UII L2.G7
L2.G7 → UII L2.G8
L2.G8 → U⏎ L3.G1
L3.G1 → UII L3.G2
L3.G2 → UII L3.G3
L3.G3 → UII L3.G4
L3.G4 → UII L3.G5
L3.G5 → UII L3.G6
L3.G6 → UII L3.G7
L3.G7 → UII L3.G8
L3.G8 → U⏎ L4.G1
L4.G1 → UII L4.G2
L4.G2 → UII L4.G3
L4.G3 → UII L4.G4
L4.G4 → UII L4.G5
L4.G5 → UII L4.G6
L4.G6 → UII L4.G7
L4.G7 → UII L4.G8
L4.G8 → U
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 91, each with such a comment, are in [`grammars/manini.rlg`](../../grammars/manini.rlg)):

```
Poem → U Poem_UII_1           # భ bha: symbol 1/3 read, 2 to go
Poem_UII_1 → I Poem_UII_2     # భ bha: symbol 2/3 read, 1 to go
Poem_UII_2 → I L1.G2          # భ bha: symbol 3/3, complete → L1.G2
L1.G2 → U L1.G2_UII_1         # భ bha: symbol 1/3 read, 2 to go
L1.G2_UII_1 → I L1.G2_UII_2   # భ bha: symbol 2/3 read, 1 to go
L1.G2_UII_2 → I L1.G3         # భ bha: symbol 3/3, complete → L1.G3
L1.G3 → U L1.G3_UII_1         # భ bha: symbol 1/3 read, 2 to go
L1.G3_UII_1 → I L1.G3_UII_2   # భ bha: symbol 2/3 read, 1 to go
…
```

The strict grammar has 92 states; minimized, the prosodic automaton has 92 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (37 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ భ భ భ భ భ భ భ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U I I భ భ భ భ భ భ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U I I U I I భ భ భ భ భ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U I I U I I U I I భ భ భ భ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U I I U I I U I I U I I భ భ భ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U I I U I I U I I U I I U I I భ భ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U I I U I I U I I U I I U I I U I I భ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ U I I U I I U I I U I I U I I U I I U I I గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ U I I U I I U I I U I I U I I U I I U I I U ⏎ U I I U I I U I I U I I U I I U I I U I I U ⏎ U I I U I I U I I U I I U I I U I I U I I U ⏎ U I I U I I U I I U I I U I I U I I U I I U
```

The result, one line per row:

```
UIIUIIUIIUIIUIIUIIUIIU
UIIUIIUIIUIIUIIUIIUIIU
UIIUIIUIIUIIUIIUIIUIIU
UIIUIIUIIUIIUIIUIIUIIU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 8 | 22 | 1 | 23 |

Whole-prosodic automaton (over U, I, ⏎): 92 states.

Grammar file: [`grammars/manini.rlg`](../../grammars/manini.rlg).

Diagram: [rule card](../../diagrams/meters/manini.svg) · [mermaid](../../diagrams/meters/manini.md) · [DFA all](../../diagrams/dfa/manini__all.svg)

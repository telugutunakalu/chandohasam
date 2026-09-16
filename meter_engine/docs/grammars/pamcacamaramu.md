# పంచచామరము · pamcacamaramu

*vrutta* · 4 lines · exactly 16 aksharas per line · prāsa required

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → జ ర జ ర జ గురువు                          # slot all: 6 ganas

# ganas → symbols
జ → I U I                                        # ja, 4 matras
ర → U I U                                        # ra, 5 matras
గురువు → U                                       # guruvu, 2 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 6 ganas, **జ ర జ ర జ గురువు**, i.e. the 16-akshara pattern `IUIUIUIUIUIUIUIU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. జ (ja) IUI
    2. ర (ra) UIU
    3. జ (ja) IUI
    4. ర (ra) UIU
    5. జ (ja) IUI
    6. గురువు (guruvu) U
3. **Yati.** The akshara at position 10 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → IUI L1.G2
L1.G2 → UIU L1.G3
L1.G3 → IUI L1.G4
L1.G4 → UIU L1.G5
L1.G5 → IUI L1.G6
L1.G6 → U⏎ L2.G1
L2.G1 → IUI L2.G2
L2.G2 → UIU L2.G3
L2.G3 → IUI L2.G4
L2.G4 → UIU L2.G5
L2.G5 → IUI L2.G6
L2.G6 → U⏎ L3.G1
L3.G1 → IUI L3.G2
L3.G2 → UIU L3.G3
L3.G3 → IUI L3.G4
L3.G4 → UIU L3.G5
L3.G5 → IUI L3.G6
L3.G6 → U⏎ L4.G1
L4.G1 → IUI L4.G2
L4.G2 → UIU L4.G3
L4.G3 → IUI L4.G4
L4.G4 → UIU L4.G5
L4.G5 → IUI L4.G6
L4.G6 → U
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 67, each with such a comment, are in [`grammars/pamcacamaramu.rlg`](../../grammars/pamcacamaramu.rlg)):

```
Poem → I Poem_IUI_1           # జ ja: symbol 1/3 read, 2 to go
Poem_IUI_1 → U Poem_IUI_2     # జ ja: symbol 2/3 read, 1 to go
Poem_IUI_2 → I L1.G2          # జ ja: symbol 3/3, complete → L1.G2
L1.G2 → U L1.G2_UIU_1         # ర ra: symbol 1/3 read, 2 to go
L1.G2_UIU_1 → I L1.G2_UIU_2   # ర ra: symbol 2/3 read, 1 to go
L1.G2_UIU_2 → U L1.G3         # ర ra: symbol 3/3, complete → L1.G3
L1.G3 → I L1.G3_IUI_1         # జ ja: symbol 1/3 read, 2 to go
L1.G3_IUI_1 → U L1.G3_IUI_2   # జ ja: symbol 2/3 read, 1 to go
…
```

The strict grammar has 68 states; minimized, the prosodic automaton has 68 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (29 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ జ ర జ ర జ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I U I ర జ ర జ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I U I U I U జ ర జ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I U I U I U I U I ర జ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I U I U I U I U I U I U జ గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I U I U I U I U I U I U I U I గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I U I U I U I U I U I U I U I U ⏎ Line ⏎ Line ⏎ Line
⇒ I U I U I U I U I U I U I U I U ⏎ జ ర జ ర జ గురువు ⏎ Line ⏎ Line
⇒ …
⇒ I U I U I U I U I U I U I U I U ⏎ I U I U I U I U I U I U I U I U ⏎ I U I U I U I U I U I U I U I U ⏎ I U I U I U I U I U I U I U I U
```

The result, one line per row:

```
IUIUIUIUIUIUIUIU
IUIUIUIUIUIUIUIU
IUIUIUIUIUIUIUIU
IUIUIUIUIUIUIUIU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 6 | 16 | 1 | 17 |

Whole-prosodic automaton (over U, I, ⏎): 68 states.

Grammar file: [`grammars/pamcacamaramu.rlg`](../../grammars/pamcacamaramu.rlg).

Diagram: [rule card](../../diagrams/meters/pamcacamaramu.svg) · [mermaid](../../diagrams/meters/pamcacamaramu.md) · [DFA all](../../diagrams/dfa/pamcacamaramu__all.svg)

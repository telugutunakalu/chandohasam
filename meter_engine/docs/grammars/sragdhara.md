# స్రగ్ధర · sragdhara

*vrutta* · 4 lines · exactly 21 aksharas per line · prāsa required

Example from the catalogue:

> కూలున్ గుఱ్ఱంబు లేనుంగులు ధరఁ గెడయుం గుప్పలై నుగ్గునూచై వ్రాలున్ దేరుల్ హతంబై వడిఁబడు సుభటవ్రాతముల్...

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → మ ర భ న య య య                             # slot all: 7 ganas

# ganas → symbols
మ → U U U                                        # ma, 6 matras
ర → U I U                                        # ra, 5 matras
భ → U I I                                        # bha, 4 matras
న → I I I                                        # na, 3 matras
య → I U U                                        # ya, 5 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 7 ganas, **మ ర భ న య య య**, i.e. the 21-akshara pattern `UUUUIUUIIIIIIUUIUUIUU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. మ (ma) UUU
    2. ర (ra) UIU
    3. భ (bha) UII
    4. న (na) III
    5. య (ya) IUU
    6. య (ya) IUU
    7. య (ya) IUU
3. **Yati.** The akshara at position 8 or 15 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → UUU L1.G2
L1.G2 → UIU L1.G3
L1.G3 → UII L1.G4
L1.G4 → III L1.G5
L1.G5 → IUU L1.G6
L1.G6 → IUU L1.G7
L1.G7 → IUU⏎ L2.G1
L2.G1 → UUU L2.G2
L2.G2 → UIU L2.G3
L2.G3 → UII L2.G4
L2.G4 → III L2.G5
L2.G5 → IUU L2.G6
L2.G6 → IUU L2.G7
L2.G7 → IUU⏎ L3.G1
L3.G1 → UUU L3.G2
L3.G2 → UIU L3.G3
L3.G3 → UII L3.G4
L3.G4 → III L3.G5
L3.G5 → IUU L3.G6
L3.G6 → IUU L3.G7
L3.G7 → IUU⏎ L4.G1
L4.G1 → UUU L4.G2
L4.G2 → UIU L4.G3
L4.G3 → UII L4.G4
L4.G4 → III L4.G5
L4.G5 → IUU L4.G6
L4.G6 → IUU L4.G7
L4.G7 → IUU
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 87, each with such a comment, are in [`grammars/sragdhara.rlg`](../../grammars/sragdhara.rlg)):

```
Poem → U Poem_UUU_1           # మ ma: symbol 1/3 read, 2 to go
Poem_UUU_1 → U Poem_UUU_2     # మ ma: symbol 2/3 read, 1 to go
Poem_UUU_2 → U L1.G2          # మ ma: symbol 3/3, complete → L1.G2
L1.G2 → U L1.G2_UIU_1         # ర ra: symbol 1/3 read, 2 to go
L1.G2_UIU_1 → I L1.G2_UIU_2   # ర ra: symbol 2/3 read, 1 to go
L1.G2_UIU_2 → U L1.G3         # ర ra: symbol 3/3, complete → L1.G3
L1.G3 → U L1.G3_UII_1         # భ bha: symbol 1/3 read, 2 to go
L1.G3_UII_1 → I L1.G3_UII_2   # భ bha: symbol 2/3 read, 1 to go
…
```

The strict grammar has 88 states; minimized, the prosodic automaton has 88 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (33 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ మ ర భ న య య య ⏎ Line ⏎ Line ⏎ Line
⇒ U U U ర భ న య య య ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U I U భ న య య య ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U I U U I I న య య య ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U I U U I I I I I య య య ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U I U U I I I I I I U U య య ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U I U U I I I I I I U U I U U య ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U I U U I I I I I I U U I U U I U U ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ U U U U I U U I I I I I I U U I U U I U U ⏎ U U U U I U U I I I I I I U U I U U I U U ⏎ U U U U I U U I I I I I I U U I U U I U U ⏎ U U U U I U U I I I I I I U U I U U I U U
```

The result, one line per row:

```
UUUUIUUIIIIIIUUIUUIUU
UUUUIUUIIIIIIUUIUUIUU
UUUUIUUIIIIIIUUIUUIUU
UUUUIUUIIIIIIUUIUUIUU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 7 | 21 | 1 | 22 |

Whole-prosodic automaton (over U, I, ⏎): 88 states.

Grammar file: [`grammars/sragdhara.rlg`](../../grammars/sragdhara.rlg).

Diagram: [rule card](../../diagrams/meters/sragdhara.svg) · [mermaid](../../diagrams/meters/sragdhara.md) · [DFA all](../../diagrams/dfa/sragdhara__all.svg)

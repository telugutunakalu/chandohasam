# భుజంగప్రయాతము · bhujangaprayatamu

*vrutta* · 4 lines · exactly 12 aksharas per line · prāsa required

Example from the catalogue:

> హరించుం గలిప్రేరితాఘంబు లెల్లన్ భరించున్ ధరన్ రామభధ్రుండుఁ బోలెన్ జరించున్ సదా వేదశాస్త్రానువృత్తిన్ వరించున్ విశేషించి వైకుంఠుభక్తిన్.

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → య య య య                                   # slot all: 4 ganas

# ganas → symbols
య → I U U                                        # ya, 5 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 4 ganas, **య య య య**, i.e. the 12-akshara pattern `IUUIUUIUUIUU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. య (ya) IUU
    2. య (ya) IUU
    3. య (ya) IUU
    4. య (ya) IUU
3. **Yati.** The akshara at position 8 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → IUU L1.G2
L1.G2 → IUU L1.G3
L1.G3 → IUU L1.G4
L1.G4 → IUU⏎ L2.G1
L2.G1 → IUU L2.G2
L2.G2 → IUU L2.G3
L2.G3 → IUU L2.G4
L2.G4 → IUU⏎ L3.G1
L3.G1 → IUU L3.G2
L3.G2 → IUU L3.G3
L3.G3 → IUU L3.G4
L3.G4 → IUU⏎ L4.G1
L4.G1 → IUU L4.G2
L4.G2 → IUU L4.G3
L4.G3 → IUU L4.G4
L4.G4 → IUU
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 51, each with such a comment, are in [`grammars/bhujangaprayatamu.rlg`](../../grammars/bhujangaprayatamu.rlg)):

```
Poem → I Poem_IUU_1           # య ya: symbol 1/3 read, 2 to go
Poem_IUU_1 → U Poem_IUU_2     # య ya: symbol 2/3 read, 1 to go
Poem_IUU_2 → U L1.G2          # య ya: symbol 3/3, complete → L1.G2
L1.G2 → I L1.G2_IUU_1         # య ya: symbol 1/3 read, 2 to go
L1.G2_IUU_1 → U L1.G2_IUU_2   # య ya: symbol 2/3 read, 1 to go
L1.G2_IUU_2 → U L1.G3         # య ya: symbol 3/3, complete → L1.G3
L1.G3 → I L1.G3_IUU_1         # య ya: symbol 1/3 read, 2 to go
L1.G3_IUU_1 → U L1.G3_IUU_2   # య ya: symbol 2/3 read, 1 to go
…
```

The strict grammar has 52 states; minimized, the prosodic automaton has 52 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (21 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ య య య య ⏎ Line ⏎ Line ⏎ Line
⇒ I U U య య య ⏎ Line ⏎ Line ⏎ Line
⇒ I U U I U U య య ⏎ Line ⏎ Line ⏎ Line
⇒ I U U I U U I U U య ⏎ Line ⏎ Line ⏎ Line
⇒ I U U I U U I U U I U U ⏎ Line ⏎ Line ⏎ Line
⇒ I U U I U U I U U I U U ⏎ య య య య ⏎ Line ⏎ Line
⇒ I U U I U U I U U I U U ⏎ I U U య య య ⏎ Line ⏎ Line
⇒ I U U I U U I U U I U U ⏎ I U U I U U య య ⏎ Line ⏎ Line
⇒ …
⇒ I U U I U U I U U I U U ⏎ I U U I U U I U U I U U ⏎ I U U I U U I U U I U U ⏎ I U U I U U I U U I U U
```

The result, one line per row:

```
IUUIUUIUUIUU
IUUIUUIUUIUU
IUUIUUIUUIUU
IUUIUUIUUIUU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 4 | 12 | 1 | 13 |

Whole-prosodic automaton (over U, I, ⏎): 52 states.

Grammar file: [`grammars/bhujangaprayatamu.rlg`](../../grammars/bhujangaprayatamu.rlg).

Diagram: [rule card](../../diagrams/meters/bhujangaprayatamu.svg) · [mermaid](../../diagrams/meters/bhujangaprayatamu.md) · [DFA all](../../diagrams/dfa/bhujangaprayatamu__all.svg)

# విద్యున్మాల · vidyunmala

*vrutta* · 4 lines · exactly 8 aksharas per line · prāsa required

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → మ మ గా                                    # slot all: 3 ganas

# ganas → symbols
మ → U U U                                        # ma, 6 matras
గా → U U                                         # gaa, 4 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 3 ganas, **మ మ గా**, i.e. the 8-akshara pattern `UUUUUUUU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. మ (ma) UUU
    2. మ (ma) UUU
    3. గా (gaa) UU
3. **Yati.** The akshara at position 5 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → UUU L1.G2
L1.G2 → UUU L1.G3
L1.G3 → UU⏎ L2.G1
L2.G1 → UUU L2.G2
L2.G2 → UUU L2.G3
L2.G3 → UU⏎ L3.G1
L3.G1 → UUU L3.G2
L3.G2 → UUU L3.G3
L3.G3 → UU⏎ L4.G1
L4.G1 → UUU L4.G2
L4.G2 → UUU L4.G3
L4.G3 → UU
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 35, each with such a comment, are in [`grammars/vidyunmala.rlg`](../../grammars/vidyunmala.rlg)):

```
Poem → U Poem_UUU_1             # మ ma: symbol 1/3 read, 2 to go
Poem_UUU_1 → U Poem_UUU_2       # మ ma: symbol 2/3 read, 1 to go
Poem_UUU_2 → U L1.G2            # మ ma: symbol 3/3, complete → L1.G2
L1.G2 → U L1.G2_UUU_1           # మ ma: symbol 1/3 read, 2 to go
L1.G2_UUU_1 → U L1.G2_UUU_2     # మ ma: symbol 2/3 read, 1 to go
L1.G2_UUU_2 → U L1.G3           # మ ma: symbol 3/3, complete → L1.G3
L1.G3 → U L1.G3_UUNL_1          # గా gaa: symbol 1/3 read, 2 to go
L1.G3_UUNL_1 → U L1.G3_UUNL_2   # గా gaa: symbol 2/3 read, 1 to go
…
```

The strict grammar has 36 states; minimized, the prosodic automaton has 36 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (17 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ మ మ గా ⏎ Line ⏎ Line ⏎ Line
⇒ U U U మ గా ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U U U గా ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U U U U U ⏎ Line ⏎ Line ⏎ Line
⇒ U U U U U U U U ⏎ మ మ గా ⏎ Line ⏎ Line
⇒ U U U U U U U U ⏎ U U U మ గా ⏎ Line ⏎ Line
⇒ U U U U U U U U ⏎ U U U U U U గా ⏎ Line ⏎ Line
⇒ U U U U U U U U ⏎ U U U U U U U U ⏎ Line ⏎ Line
⇒ …
⇒ U U U U U U U U ⏎ U U U U U U U U ⏎ U U U U U U U U ⏎ U U U U U U U U
```

The result, one line per row:

```
UUUUUUUU
UUUUUUUU
UUUUUUUU
UUUUUUUU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 3 | 8 | 1 | 9 |

Whole-prosodic automaton (over U, I, ⏎): 36 states.

Grammar file: [`grammars/vidyunmala.rlg`](../../grammars/vidyunmala.rlg).

Diagram: [rule card](../../diagrams/meters/vidyunmala.svg) · [mermaid](../../diagrams/meters/vidyunmala.md) · [DFA all](../../diagrams/dfa/vidyunmala__all.svg)

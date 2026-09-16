# మాలిని · malini

*vrutta* · 4 lines · exactly 15 aksharas per line · prāsa required

Example from the catalogue:

> సకల నిగమవేద్యున్‌ సంసృతివ్యాధివైద్యున్‌ మకుటవిమలమూర్తిన్‌ మాలినీవృత్త పూర్తిన్‌

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → న న మ య య                                 # slot all: 5 ganas

# ganas → symbols
న → I I I                                        # na, 3 matras
మ → U U U                                        # ma, 6 matras
య → I U U                                        # ya, 5 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line is the same fixed sequence of 5 ganas, **న న మ య య**, i.e. the 15-akshara pattern `IIIIIIUUUIUUIUU`. There is no choice anywhere in the line; the four lines are identical in weight.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. న (na) III
    2. న (na) III
    3. మ (ma) UUU
    4. య (ya) IUU
    5. య (ya) IUU
3. **Yati.** The akshara at position 9 must be in yati-maitri (sound agreement) with the first akshara of the line. The grammar only *locates* this position; the sound check is a separate engine.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → III L1.G2
L1.G2 → III L1.G3
L1.G3 → UUU L1.G4
L1.G4 → IUU L1.G5
L1.G5 → IUU⏎ L2.G1
L2.G1 → III L2.G2
L2.G2 → III L2.G3
L2.G3 → UUU L2.G4
L2.G4 → IUU L2.G5
L2.G5 → IUU⏎ L3.G1
L3.G1 → III L3.G2
L3.G2 → III L3.G3
L3.G3 → UUU L3.G4
L3.G4 → IUU L3.G5
L3.G5 → IUU⏎ L4.G1
L4.G1 → III L4.G2
L4.G2 → III L4.G3
L4.G3 → UUU L4.G4
L4.G4 → IUU L4.G5
L4.G5 → IUU
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 63, each with such a comment, are in [`grammars/malini.rlg`](../../grammars/malini.rlg)):

```
Poem → I Poem_III_1           # న na: symbol 1/3 read, 2 to go
Poem_III_1 → I Poem_III_2     # న na: symbol 2/3 read, 1 to go
Poem_III_2 → I L1.G2          # న na: symbol 3/3, complete → L1.G2
L1.G2 → I L1.G2_III_1         # న na: symbol 1/3 read, 2 to go
L1.G2_III_1 → I L1.G2_III_2   # న na: symbol 2/3 read, 1 to go
L1.G2_III_2 → I L1.G3         # న na: symbol 3/3, complete → L1.G3
L1.G3 → U L1.G3_UUU_1         # మ ma: symbol 1/3 read, 2 to go
L1.G3_UUU_1 → U L1.G3_UUU_2   # మ ma: symbol 2/3 read, 1 to go
…
```

The strict grammar has 64 states; minimized, the prosodic automaton has 64 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (25 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ న న మ య య ⏎ Line ⏎ Line ⏎ Line
⇒ I I I న మ య య ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I I మ య య ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I I U U U య య ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I I U U U I U U య ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I I U U U I U U I U U ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I I U U U I U U I U U ⏎ న న మ య య ⏎ Line ⏎ Line
⇒ I I I I I I U U U I U U I U U ⏎ I I I న మ య య ⏎ Line ⏎ Line
⇒ …
⇒ I I I I I I U U U I U U I U U ⏎ I I I I I I U U U I U U I U U ⏎ I I I I I I U U U I U U I U U ⏎ I I I I I I U U U I U U I U U
```

The result, one line per row:

```
IIIIIIUUUIUUIUU
IIIIIIUUUIUUIUU
IIIIIIUUUIUUIUU
IIIIIIUUUIUUIUU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 5 | 15 | 1 | 16 |

Whole-prosodic automaton (over U, I, ⏎): 64 states.

Grammar file: [`grammars/malini.rlg`](../../grammars/malini.rlg).

Diagram: [rule card](../../diagrams/meters/malini.svg) · [mermaid](../../diagrams/meters/malini.md) · [DFA all](../../diagrams/dfa/malini__all.svg)

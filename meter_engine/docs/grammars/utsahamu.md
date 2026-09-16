# ఉత్సాహము · utsahamu

*jati* · 4 lines · between 15 and 22 aksharas per line · prāsa required

Example from the catalogue:

> సాహచర్య మమర సప్త సవితృవర్గమతి సము త్సాహ మెక్క నొక్క గురుఁడు చరణములు భజింపఁగా

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Line ⏎ Line ⏎ Line ⏎ Line                 # 4 lines

# lines
Line → Surya Surya Surya Surya Surya Surya Surya గురువు # slot all: 8 ganas

# gana classes
Surya → న | హ                                    # class surya

# ganas → symbols
న → I I I                                        # na, 3 matras
హ → U I                                          # ha, 3 matras
గురువు → U                                       # guruvu, 2 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;

## In one sentence

Every line has 8 ganas (surya, surya, surya, surya, surya, surya, surya, గ). Each gana is chosen from a class, so the line length varies.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Line recipe.** In order:
    1. a సూర్యగణము (surya gana): న III or హ UI
    2. a సూర్యగణము (surya gana): న III or హ UI
    3. a సూర్యగణము (surya gana): న III or హ UI
    4. a సూర్యగణము (surya gana): న III or హ UI
    5. a సూర్యగణము (surya gana): న III or హ UI
    6. a సూర్యగణము (surya gana): న III or హ UI
    7. a సూర్యగణము (surya gana): న III or హ UI
    8. గురువు (guruvu) U
3. **Yati.** at the first akshara of gana 5. Because gana lengths vary, the akshara index of the yati depends on the ganas actually used; the parser reports it per line.
4. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
5. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem.

```
Poem → III L1.G2 | UI L1.G2
L1.G2 → III L1.G3 | UI L1.G3
L1.G3 → III L1.G4 | UI L1.G4
L1.G4 → III L1.G5 | UI L1.G5
L1.G5 → III L1.G6 | UI L1.G6
L1.G6 → III L1.G7 | UI L1.G7
L1.G7 → III L1.G8 | UI L1.G8
L1.G8 → U⏎ L2.G1
L2.G1 → III L2.G2 | UI L2.G2
L2.G2 → III L2.G3 | UI L2.G3
L2.G3 → III L2.G4 | UI L2.G4
L2.G4 → III L2.G5 | UI L2.G5
L2.G5 → III L2.G6 | UI L2.G6
L2.G6 → III L2.G7 | UI L2.G7
L2.G7 → III L2.G8 | UI L2.G8
L2.G8 → U⏎ L3.G1
L3.G1 → III L3.G2 | UI L3.G2
L3.G2 → III L3.G3 | UI L3.G3
L3.G3 → III L3.G4 | UI L3.G4
L3.G4 → III L3.G5 | UI L3.G5
L3.G5 → III L3.G6 | UI L3.G6
L3.G6 → III L3.G7 | UI L3.G7
L3.G7 → III L3.G8 | UI L3.G8
L3.G8 → U⏎ L4.G1
L4.G1 → III L4.G2 | UI L4.G2
L4.G2 → III L4.G3 | UI L4.G3
L4.G3 → III L4.G4 | UI L4.G4
L4.G4 → III L4.G5 | UI L4.G5
L4.G5 → III L4.G6 | UI L4.G6
L4.G6 → III L4.G7 | UI L4.G7
L4.G7 → III L4.G8 | UI L4.G8
L4.G8 → U
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 147, each with such a comment, are in [`grammars/utsahamu.rlg`](../../grammars/utsahamu.rlg)):

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

The strict grammar has 120 states; minimized, the prosodic automaton has 92 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (65 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Line ⏎ Line ⏎ Line ⏎ Line
⇒ Surya Surya Surya Surya Surya Surya Surya గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ న Surya Surya Surya Surya Surya Surya గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I Surya Surya Surya Surya Surya Surya గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I న Surya Surya Surya Surya Surya గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I I Surya Surya Surya Surya Surya గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I I హ Surya Surya Surya Surya గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I I U I Surya Surya Surya Surya గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ I I I I I I U I న Surya Surya Surya గురువు ⏎ Line ⏎ Line ⏎ Line
⇒ …
⇒ I I I I I I U I I I I I I I I I I I I I U ⏎ U I I I I I I I U I I I I U I U I U ⏎ I I I I I I U I U I I I I U I I I I U ⏎ I I I U I I I I U I I I I U I I I I U
```

The result, one line per row:

```
IIIIIIUIIIIIIIIIIIIIU
UIIIIIIIUIIIIUIUIU
IIIIIIUIUIIIIUIIIIU
IIIUIIIIUIIIIUIIIIU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| all | 8 | 15–22 | 128 | 23 |

Whole-prosodic automaton (over U, I, ⏎): 92 states.

Grammar file: [`grammars/utsahamu.rlg`](../../grammars/utsahamu.rlg).

Diagram: [rule card](../../diagrams/meters/utsahamu.svg) · [mermaid](../../diagrams/meters/utsahamu.md) · [DFA all](../../diagrams/dfa/utsahamu__all.svg)

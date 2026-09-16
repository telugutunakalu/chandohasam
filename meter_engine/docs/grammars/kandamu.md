# కందము · kandamu

*jati* · 4 lines · between 6 and 20 aksharas per line · prāsa required

Example from the catalogue:

> భూథలనాథుఁడు రాముఁడు ప్రీతుండై పెండ్లియాడెఁ బృథుగుణమణి సంఘాతన్ భాగ్యోపేతన్ సీతన్ ముఖకాంతివిజిత సితఖద్యోతన్.

## The prosodic grammar

Read top-down: a **Poem** is lines separated by `⏎`; a **Line** is a sequence of gana classes; a **class** is a choice of ganas; a **gana** is its guru/laghu symbols. Nothing else is needed to generate every valid stanza of this meter.

```
# poem
Poem → Poem⟨U⟩ | Poem⟨I⟩                         # stanza rule: every line starts with the same weight
Poem⟨U⟩ → Line_odd⟨U⟩ ⏎ Line_even⟨U⟩ ⏎ Line_odd⟨U⟩ ⏎ Line_even⟨U⟩ # 4 lines
Poem⟨I⟩ → Line_odd⟨I⟩ ⏎ Line_even⟨I⟩ ⏎ Line_odd⟨I⟩ ⏎ Line_even⟨I⟩ # 4 lines

# lines
Line_odd⟨U⟩ → Kanda−జ⟨U⟩ Kanda Kanda−జ           # slot odd: 3 ganas
Line_even⟨U⟩ → Kanda⟨U⟩ Kanda−జ Kanda=జ|నల Kanda−జ Kanda$U # slot even: 5 ganas
Line_odd⟨I⟩ → Kanda−జ⟨I⟩ Kanda Kanda−జ           # slot odd: 3 ganas
Line_even⟨I⟩ → Kanda⟨I⟩ Kanda−జ Kanda=జ|నల Kanda−జ Kanda$U # slot even: 5 ganas

# gana classes
Kanda−జ⟨U⟩ → భ | గా                              # class kanda, first akshara U (stanza rule)
Kanda → భ | జ | స | నల | గా                      # class kanda
Kanda−జ → భ | స | నల | గా                        # class kanda
Kanda⟨U⟩ → భ | గా                                # class kanda, first akshara U (stanza rule)
Kanda=జ|నల → జ | నల                              # class kanda
Kanda$U → స | గా                                 # class kanda
Kanda−జ⟨I⟩ → స | నల                              # class kanda, first akshara I (stanza rule)
Kanda⟨I⟩ → జ | స | నల                            # class kanda, first akshara I (stanza rule)

# ganas → symbols
భ → U I I                                        # bha, 4 matras
గా → U U                                         # gaa, 4 matras
జ → I U I                                        # ja, 4 matras
స → I I U                                        # sa, 4 matras
నల → I I I I                                     # nala, 4 matras
```

Legend:

- `⏎` — line separator (a terminal, like `U` and `I`);
- `|` — alternatives; a comment after `#` explains the rule;
- `Kanda−జ` — the class *minus* జ (a constraint removed it); `Kanda=జ|నల` — only జ or నల allowed there; `Kanda$U` — only members ending in a guru;
- `Poem⟨U⟩` / `Kanda⟨U⟩` — the copy of the grammar in which every line starts with a guru; the stanza rule (uniform first akshara) becomes two branches instead of a side condition;

## In one sentence

Line 1, 3 has 3 ganas (kanda, kanda, kanda); line 2, 4 has 5 ganas (kanda, kanda, kanda, kanda, kanda). Each gana is chosen from a class, so the line length varies.

## The rules, one by one

1. **Line count.** A stanza has 4 lines.
2. **Two kinds of line.** Lines follow the pattern odd even odd even: slot *odd* is line 1, 3; slot *even* is line 2, 4.
3. **Recipe for slot *odd*.** In order:
    1. a కంద గణము (kanda gana): భ UII, జ IUI, స IIU, నల IIII or గా UU — but here only భ UII, స IIU, నల IIII or గా UU (a constraint removes the rest)
    2. a కంద గణము (kanda gana): భ UII, జ IUI, స IIU, నల IIII or గా UU
    3. a కంద గణము (kanda gana): భ UII, జ IUI, స IIU, నల IIII or గా UU — but here only భ UII, స IIU, నల IIII or గా UU (a constraint removes the rest)
4. **Recipe for slot *even*.** In order:
    1. a కంద గణము (kanda gana): భ UII, జ IUI, స IIU, నల IIII or గా UU
    2. a కంద గణము (kanda gana): భ UII, జ IUI, స IIU, నల IIII or గా UU — but here only భ UII, స IIU, నల IIII or గా UU (a constraint removes the rest)
    3. a కంద గణము (kanda gana): భ UII, జ IUI, స IIU, నల IIII or గా UU — but here only జ IUI or నల IIII (a constraint removes the rest)
    4. a కంద గణము (kanda gana): భ UII, జ IUI, స IIU, నల IIII or గా UU — but here only భ UII, స IIU, నల IIII or గా UU (a constraint removes the rest)
    5. a కంద గణము (kanda gana): భ UII, జ IUI, స IIU, నల IIII or గా UU — but here only స IIU or గా UU (a constraint removes the rest)
5. **Constraint.** In the odd lines, gana 1 and gana 3 may not be జ. *(జగణము బేసి గణములలో (1,3,5,7) రాకూడదు)*
6. **Constraint.** In the even lines, gana 2 and gana 4 may not be జ. *(జగణము బేసి గణములలో (1,3,5,7) రాకూడదు — even line ganas 2,4 are half-ganas 5,7)*
7. **Constraint.** In the even lines, gana 3 must be జ or నల. *(ఆరవ గణము జగణము లేదా నలము)*
8. **Constraint.** In the even lines, the last akshara must be a guru. *(పాదాంతమున (అర్ధభాగాంతమున) గురువు)*
9. **Stanza rule.** The first akshara of every line has the same weight (all guru or all laghu). *(మొదటి అక్షరము గురువైన అన్ని పాదములలో గురువు, లఘువైన లఘువు — verify against Appakaviyamu)* The identifier reports a breach of this rule as a violation rather than rejecting the stanza (Pothana 3-151 and 3-616 are otherwise valid kandas that break it); the prosodic grammar below keeps the rule as written.
10. **Yati.** none in slot *odd*; at the first akshara of gana 4 in slot *even*. Because gana lengths vary, the akshara index of the yati depends on the ganas actually used; the parser reports it per line.
11. **Prāsa.** The second akshara of every line must rhyme (checked by the prāsa engine, not here).
12. **Pādānta laghu.** A line-final laghu may be read as guru (default on in the identifier).

## The same grammar, right-linear (what the automaton is built from)

A grammar whose rules are all `A → wB` or `A → w` is right-linear, so its language is regular. Flattening the hierarchy above gives one such grammar for the whole poem. `L2.G3` = "line 2, about to read gana 3". The last gana of a line emits `⏎` and hands over to the next line; the last gana of the last line ends the poem. `⟨U⟩L1.G2` is the same state inside the all-lines-start-with-U branch.

```
Poem → UII ⟨U⟩L1.G2 | UU ⟨U⟩L1.G2 | IIU ⟨I⟩L1.G2 | IIII ⟨I⟩L1.G2
⟨U⟩L1.G2 → UII ⟨U⟩L1.G3 | IUI ⟨U⟩L1.G3 | IIU ⟨U⟩L1.G3 | IIII ⟨U⟩L1.G3 | UU ⟨U⟩L1.G3
⟨U⟩L1.G3 → UII⏎ ⟨U⟩L2.G1 | IIU⏎ ⟨U⟩L2.G1 | IIII⏎ ⟨U⟩L2.G1 | UU⏎ ⟨U⟩L2.G1
⟨U⟩L2.G1 → UII ⟨U⟩L2.G2 | UU ⟨U⟩L2.G2
⟨U⟩L2.G2 → UII ⟨U⟩L2.G3 | IIU ⟨U⟩L2.G3 | IIII ⟨U⟩L2.G3 | UU ⟨U⟩L2.G3
⟨U⟩L2.G3 → IUI ⟨U⟩L2.G4 | IIII ⟨U⟩L2.G4
⟨U⟩L2.G4 → UII ⟨U⟩L2.G5 | IIU ⟨U⟩L2.G5 | IIII ⟨U⟩L2.G5 | UU ⟨U⟩L2.G5
⟨U⟩L2.G5 → IIU⏎ ⟨U⟩L3.G1 | UU⏎ ⟨U⟩L3.G1
⟨U⟩L3.G1 → UII ⟨U⟩L3.G2 | UU ⟨U⟩L3.G2
⟨U⟩L3.G2 → UII ⟨U⟩L3.G3 | IUI ⟨U⟩L3.G3 | IIU ⟨U⟩L3.G3 | IIII ⟨U⟩L3.G3 | UU ⟨U⟩L3.G3
⟨U⟩L3.G3 → UII⏎ ⟨U⟩L4.G1 | IIU⏎ ⟨U⟩L4.G1 | IIII⏎ ⟨U⟩L4.G1 | UU⏎ ⟨U⟩L4.G1
⟨U⟩L4.G1 → UII ⟨U⟩L4.G2 | UU ⟨U⟩L4.G2
⟨U⟩L4.G2 → UII ⟨U⟩L4.G3 | IIU ⟨U⟩L4.G3 | IIII ⟨U⟩L4.G3 | UU ⟨U⟩L4.G3
⟨U⟩L4.G3 → IUI ⟨U⟩L4.G4 | IIII ⟨U⟩L4.G4
⟨U⟩L4.G4 → UII ⟨U⟩L4.G5 | IIU ⟨U⟩L4.G5 | IIII ⟨U⟩L4.G5 | UU ⟨U⟩L4.G5
⟨U⟩L4.G5 → IIU | UU
⟨I⟩L1.G2 → UII ⟨I⟩L1.G3 | IUI ⟨I⟩L1.G3 | IIU ⟨I⟩L1.G3 | IIII ⟨I⟩L1.G3 | UU ⟨I⟩L1.G3
⟨I⟩L1.G3 → UII⏎ ⟨I⟩L2.G1 | IIU⏎ ⟨I⟩L2.G1 | IIII⏎ ⟨I⟩L2.G1 | UU⏎ ⟨I⟩L2.G1
⟨I⟩L2.G1 → IUI ⟨I⟩L2.G2 | IIU ⟨I⟩L2.G2 | IIII ⟨I⟩L2.G2
⟨I⟩L2.G2 → UII ⟨I⟩L2.G3 | IIU ⟨I⟩L2.G3 | IIII ⟨I⟩L2.G3 | UU ⟨I⟩L2.G3
⟨I⟩L2.G3 → IUI ⟨I⟩L2.G4 | IIII ⟨I⟩L2.G4
⟨I⟩L2.G4 → UII ⟨I⟩L2.G5 | IIU ⟨I⟩L2.G5 | IIII ⟨I⟩L2.G5 | UU ⟨I⟩L2.G5
⟨I⟩L2.G5 → IIU⏎ ⟨I⟩L3.G1 | UU⏎ ⟨I⟩L3.G1
⟨I⟩L3.G1 → IIU ⟨I⟩L3.G2 | IIII ⟨I⟩L3.G2
⟨I⟩L3.G2 → UII ⟨I⟩L3.G3 | IUI ⟨I⟩L3.G3 | IIU ⟨I⟩L3.G3 | IIII ⟨I⟩L3.G3 | UU ⟨I⟩L3.G3
⟨I⟩L3.G3 → UII⏎ ⟨I⟩L4.G1 | IIU⏎ ⟨I⟩L4.G1 | IIII⏎ ⟨I⟩L4.G1 | UU⏎ ⟨I⟩L4.G1
⟨I⟩L4.G1 → IUI ⟨I⟩L4.G2 | IIU ⟨I⟩L4.G2 | IIII ⟨I⟩L4.G2
⟨I⟩L4.G2 → UII ⟨I⟩L4.G3 | IIU ⟨I⟩L4.G3 | IIII ⟨I⟩L4.G3 | UU ⟨I⟩L4.G3
⟨I⟩L4.G3 → IUI ⟨I⟩L4.G4 | IIII ⟨I⟩L4.G4
⟨I⟩L4.G4 → UII ⟨I⟩L4.G5 | IIU ⟨I⟩L4.G5 | IIII ⟨I⟩L4.G5 | UU ⟨I⟩L4.G5
⟨I⟩L4.G5 → IIU | UU
```

### Strict form (one symbol per production = one automaton edge)

Every multi-symbol production `A → UUI B` is split into a chain. The intermediate nonterminal `A_UUI_2` means: *inside alternative UUI of A, 2 symbols already read*. So `L1.G3_UUI_2 → I L1.G4` reads: line 1, gana 3, alternative త (UUI), the third and last symbol is I, gana 3 is complete, go to gana 4. First productions (all 326, each with such a comment, are in [`grammars/kandamu.rlg`](../../grammars/kandamu.rlg)):

```
Poem → U Poem_UII_1                 # భ bha: symbol 1/3 read, 2 to go
Poem_UII_1 → I Poem_UII_2           # భ bha: symbol 2/3 read, 1 to go
Poem_UII_2 → I ⟨U⟩L1.G2             # భ bha: symbol 3/3, complete → ⟨U⟩L1.G2
Poem → U Poem_UU_1                  # గా gaa: symbol 1/2 read, 1 to go
Poem_UU_1 → U ⟨U⟩L1.G2              # గా gaa: symbol 2/2, complete → ⟨U⟩L1.G2
⟨U⟩L1.G2 → U ⟨U⟩L1.G2_UII_1         # భ bha: symbol 1/3 read, 2 to go
⟨U⟩L1.G2_UII_1 → I ⟨U⟩L1.G2_UII_2   # భ bha: symbol 2/3 read, 1 to go
⟨U⟩L1.G2_UII_2 → I ⟨U⟩L1.G3         # భ bha: symbol 3/3, complete → ⟨U⟩L1.G3
…
```

The strict grammar has 256 states; minimized, the prosodic automaton has 109 states.

## One worked derivation

A poem of 4 lines, derived top-down from `Poem` (38 rewriting steps; the leftmost nonterminal is rewritten each time):

```
Poem
⇒ Poem⟨U⟩
⇒ Line_odd⟨U⟩ ⏎ Line_even⟨U⟩ ⏎ Line_odd⟨U⟩ ⏎ Line_even⟨U⟩
⇒ Kanda−జ⟨U⟩ Kanda Kanda−జ ⏎ Line_even⟨U⟩ ⏎ Line_odd⟨U⟩ ⏎ Line_even⟨U⟩
⇒ గా Kanda Kanda−జ ⏎ Line_even⟨U⟩ ⏎ Line_odd⟨U⟩ ⏎ Line_even⟨U⟩
⇒ U U Kanda Kanda−జ ⏎ Line_even⟨U⟩ ⏎ Line_odd⟨U⟩ ⏎ Line_even⟨U⟩
⇒ U U భ Kanda−జ ⏎ Line_even⟨U⟩ ⏎ Line_odd⟨U⟩ ⏎ Line_even⟨U⟩
⇒ U U U I I Kanda−జ ⏎ Line_even⟨U⟩ ⏎ Line_odd⟨U⟩ ⏎ Line_even⟨U⟩
⇒ U U U I I గా ⏎ Line_even⟨U⟩ ⏎ Line_odd⟨U⟩ ⏎ Line_even⟨U⟩
⇒ U U U I I U U ⏎ Line_even⟨U⟩ ⏎ Line_odd⟨U⟩ ⏎ Line_even⟨U⟩
⇒ …
⇒ U U U I I U U ⏎ U I I U U I I I I I I U U U ⏎ U I I I I I I I I U ⏎ U I I U I I I I I I I I I I I I U
```

The result, one line per row:

```
UUUIIUU
UIIUUIIIIIIUUU
UIIIIIIIIU
UIIUIIIIIIIIIIIIU
```

## What this grammar does not check

- the *sounds* at the yati positions (yati-maitri) — only their location;
- prāsa (the second-akshara rhyme);
- the scansion itself: the grammar trusts the U/I string it is given;
- meaning, sandhi, word boundaries.

## Numbers

| slot | ganas | aksharas | distinct lines | DFA states |
|---|---|---|---|---|
| odd | 3 | 6–12 | 80 | 13 |
| even | 5 | 11–19 | 320 | 20 |

Whole-prosodic automaton (over U, I, ⏎): 109 states.

Grammar file: [`grammars/kandamu.rlg`](../../grammars/kandamu.rlg).

Diagram: [rule card](../../diagrams/meters/kandamu.svg) · [mermaid](../../diagrams/meters/kandamu.md) · [DFA odd](../../diagrams/dfa/kandamu__odd.svg) · [DFA even](../../diagrams/dfa/kandamu__even.svg)

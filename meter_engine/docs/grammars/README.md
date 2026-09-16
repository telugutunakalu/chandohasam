# Reading the meter grammars

Every Telugu meter in `meter_rules.yaml` is written here as a **right-linear grammar** over two letters: `U` (guru, a heavy syllable, 2 matras) and `I` (laghu, a light syllable, 1 matra). This page explains the notation once; each meter then has its own page.

## What a grammar is

A grammar is a list of rewriting rules. Start from `Poem` and keep replacing a nonterminal by the right-hand side of one of its rules until only the terminals `U`, `I` and `⏎` remain. Every text you can reach this way is a legal poem of the meter; nothing else is.

```
Poem  → Line ⏎ Line ⏎ Line ⏎ Line        # four lines separated by ⏎
Line  → Surya Indra Indra Surya Surya   # five ganas, by class
Surya → న | హ                           # a class is a choice of ganas
న     → I I I                           # a gana is its symbols
```

`|` separates alternatives; a comment after `#` explains the rule. Four levels: poem, lines, gana classes, ganas. A constraint that removes a gana at one position shows up in the class name (`Kanda−జ`), and a stanza-wide rule shows up as two branches of `Poem` (`Poem⟨U⟩ | Poem⟨I⟩`).

## From the hierarchy to a right-linear grammar

The hierarchy is only for reading. Because no nonterminal calls itself except `Poem` (and only at the far right, `Poem → Unit ⏎ Poem`, for repeatable meters), the whole thing flattens into one **right-linear** grammar: `L1.G1 → III L1.G2 | UI L1.G2`, …, `L1.G5 → III⏎ L2.G1`, …, `L4.G5 → III`. Each meter's page shows both, and the `.rlg` file shows the strict form too, where `A_UUI_2` means *inside alternative UUI of A, two symbols already read*.

## Why right-linear

In the flattened form every rule has the nonterminal, if any, as the **last** thing on the right (`A → wB` or `A → w`). Grammars of that shape generate exactly the regular languages, and they are finite automata in disguise: nonterminal = state, `A → aB` = an edge labelled `a`, `A → a` = an edge into the accept state. The strict form (`.rlg` files, second half) makes that one-to-one: one letter per rule.

Because the automaton of every meter is regular, the union of all of them is regular too, and a single minimized deterministic automaton — the **DAWG** (directed acyclic word graph; acyclic because every line has bounded length) — recognises every meter at once. Each edge carries the matra weight of its letter, so a path's weight is the line's matra count.

## How the identifier uses it

1. Each line is walked through the DAWG; the accepting state says which (meter, slot) pairs accept it.
2. The stanza layer checks the line count and the slot pattern (odd/even lines) and any stanza-wide rule.
3. For every surviving meter the parser recovers the gana split and the yati akshara positions.
4. Ties are reported as ambiguity; yati and prāsa engines break them later.

## Constraints

A positional rule (Kandamu: no జ at odd ganas, జ or నల at the sixth, guru at the end) is applied when the rules are written: the forbidden alternative is simply absent from that `Gk` rule. So the constraint is visible in the grammar itself. Stanza-wide rules (the first akshara of every line has the same weight) cannot live in a per-line grammar and are listed separately.

## Gana glossary

| gana | name | pattern | matras | classes |
|---|---|---|---|---|
| లఘువు | laghuvu | `I` | 1 | – |
| గురువు | guruvu | `U` | 2 | – |
| లల | lala | `II` | 2 | – |
| వ | va | `IU` | 3 | – |
| హ | ha | `UI` | 3 | surya |
| గా | gaa | `UU` | 4 | kanda |
| న | na | `III` | 3 | surya |
| స | sa | `IIU` | 4 | kanda |
| జ | ja | `IUI` | 4 | kanda |
| య | ya | `IUU` | 5 | – |
| భ | bha | `UII` | 4 | indra, kanda |
| ర | ra | `UIU` | 5 | indra |
| త | ta | `UUI` | 5 | indra |
| మ | ma | `UUU` | 6 | – |
| నల | nala | `IIII` | 4 | indra, kanda |
| నగ | naga | `IIIU` | 5 | indra |
| సల | sala | `IIUI` | 5 | indra |
| భల | bhala | `UIII` | 5 | chandra |
| భగురు | bhaguru | `UIIU` | 6 | chandra |
| రల | rala | `UIUI` | 6 | chandra |
| రగురు | raguru | `UIUU` | 7 | chandra |
| తల | tala | `UUII` | 6 | chandra |
| తగ | taga | `UUIU` | 7 | chandra |
| మలఘు | malaghu | `UUUI` | 7 | chandra |
| నలల | nalala | `IIIII` | 5 | chandra |
| నవ | nava | `IIIIU` | 6 | chandra |
| నహ | naha | `IIIUI` | 6 | chandra |
| నగగ | nagaga | `IIIUU` | 7 | chandra |
| సవ | sava | `IIUIU` | 7 | chandra |
| సహ | saha | `IIUUI` | 7 | chandra |

Class tokens used in the catalogue: `surya`, `indra`, `chandra`, `kanda`; `m3`/`m4`/`m5` = any group worth that many matras; `all_laghu(X)` = the laghu-only members of class X.

## Meters

- [ఉత్పలమాల `utpalamala`](utpalamala.md) — vrutta
- [చంపకమాల `champakamala`](champakamala.md) — vrutta
- [మత్తేభవిక్రీడితము `mattebhavikriditamu`](mattebhavikriditamu.md) — vrutta
- [శార్దూలవిక్రీడితము `sardulavikriditamu`](sardulavikriditamu.md) — vrutta
- [స్రగ్ధర `sragdhara`](sragdhara.md) — vrutta
- [మహాస్రగ్ధర `mahasragdhara`](mahasragdhara.md) — vrutta
- [తోటకము `totakamu`](totakamu.md) — vrutta
- [భుజంగప్రయాతము `bhujangaprayatamu`](bhujangaprayatamu.md) — vrutta
- [మత్తకోకిలము `mattakokilamu`](mattakokilamu.md) — vrutta
- [పంచచామరము `pamcacamaramu`](pamcacamaramu.md) — vrutta
- [వసంతతిలకము `vasamtatilakamu`](vasamtatilakamu.md) — vrutta
- [ఇంద్రవజ్ర `indravajra`](indravajra.md) — vrutta
- [ఉపేంద్రవజ్ర `upendravajra`](upendravajra.md) — vrutta
- [శాలిని `salini`](salini.md) — vrutta
- [రథోద్ధత `rathoddhata`](rathoddhata.md) — vrutta
- [స్రగ్విణి `sragvini`](sragvini.md) — vrutta
- [విద్యున్మాల `vidyunmala`](vidyunmala.md) — vrutta
- [లలిత `lalita`](lalita.md) — vrutta
- [కందము `kandamu`](kandamu.md) — jati
- [ఉత్సాహము `utsahamu`](utsahamu.md) — jati
- [తరువోజ `taruvoja`](taruvoja.md) — jati
- [ద్విపద `dvipada`](dvipada.md) — jati
- [మధ్యాక్కర `madhyakkara`](madhyakkara.md) — jati
- [మధురగతి_రగడ `madhuragati_ragada`](madhuragati_ragada.md) — jati
- [తురగగతి_రగడ `turagagati_ragada`](turagagati_ragada.md) — jati
- [హయప్రచార_రగడ `hayapracara_ragada`](hayapracara_ragada.md) — jati
- [సీసము `seesamu`](seesamu.md) — upajati
- [ఆటవెలది `ataveladi`](ataveladi.md) — upajati
- [తేటగీతి `tetagiti`](tetagiti.md) — upajati
- [తరళము `taralamu`](taralamu.md) — vrutta
- [మాలిని `malini`](malini.md) — vrutta
- [మానిని `manini`](manini.md) — vrutta
- [కవిరాజవిరాజితము `kavirajavirajitamu`](kavirajavirajitamu.md) — vrutta
- [వనమయూరము `vanamayuramu`](vanamayuramu.md) — vrutta
- [మంగళమహాశ్రీ `mangalamahasri`](mangalamahasri.md) — vrutta
- [లయగ్రాహి `layagrahi`](layagrahi.md) — vrutta
- [లయవిభాతి `layavibhati`](layavibhati.md) — vrutta

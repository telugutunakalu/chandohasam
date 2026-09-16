# Metrical DAWG — plan

> **Status (2026-09-13): phases 0–4 implemented.** Package `indic_meter_dawg/`,
> 35 grammars in `grammars/`, docs in `docs/grammars/`, diagrams in
> `diagrams/`, 255 tests in `tests/test_imd_*.py` (all green, ~6 s).
> Usage: `METER_DAWG_README.md`. Remaining: the "later" row of section 9
> (yati/prāsa engines consuming `Segmentation.yati_aksharas`; weighted
> nearest-meter search).

Goal: given a poem as a list of lines, each line a guru/laghu string, identify
the chandassu. Weight pattern only; yati and prāsa are later engines that plug
into hooks this design leaves open. Everything lives in `meter_engine/`.

Companion to `meter_rules.yaml`, `ganas.yaml`, and the prāsa engine already in
this folder. The prāsa engine is not touched.

---

## 1. Scope

**In scope**

- Input: a stanza as `["UIIUIU…", "UIIUIU…", …]`, in any of the usual
  notations (`U/I`, `G/L`, `-/u`, `గ/ల`, `|`-separated ganas, spaces ignored).
- Output: a ranked list of candidate meters with, for each, the line-slot
  assignment, the gana segmentation of every line, the akshara index of every
  yati checkpoint the meter prescribes (so the yati engine later knows where
  to look), and a plain-language explanation. When nothing matches, a per-meter
  failure report: which line, which akshara, which hypothesis died there.
- A line-level weighted acyclic acceptor (the DAWG) over `{U, I}` covering all
  33 meters in `meter_rules.yaml`, built from data, not per-meter code.
- A stanza-level layer: line count, odd/even slot patterns, kanda's cross-line
  rules, dvipada streams, seesam + gīta composites.
- Diagrams: every meter as a rule card (railroad-style gana diagram with yati
  marks), the vritta trie, family views of the DAWG, index page. DOT and
  Mermaid, rendered to SVG with the system `dot`.
- A large standard-library `unittest` suite; runs with pytest too if present.

**Out of scope for this iteration**

- ~~Scansion (text → U/I). Assumed given, with line breaks.~~ Added in phase 5 (`scansion.py`).
- Yati-maitri and prāsa verdicts. Hooks only.
- Nearest-meter repair (weighted edit paths). Edge weights are in the data
  model from day one, the search is a later phase.
- The generic `ragada` (id 26) family entry: it is abstract; its three concrete
  sub-types are identified.

---

## 2. Facts that shaped the design

From the probe run on 2026-09-13 (script kept in the session scratchpad; it
becomes `tests/test_language_counts.py`):

| Measure | Value |
|---|---|
| Distinct legal line patterns, 30 modelled meters | 370,307 |
| Patterns accepted by more than one meter | 16,979 (4.6%) |
| Of those, separable by yati akshara position | 16,563 (97.5%) |
| Left for line-count / slot-pattern / prāsa-flag | 416 |
| Trie states over all patterns | 1,417,190 |
| Minimal DAWG states | 1,314 |

Consequences:

1. Weight-only identification is nearly complete. The residue (mostly
   seesam vs taruvoja) must be *reported as ambiguity*, not resolved by guessing.
2. Minimization matters for memory, but labels kill it: the vritta-only trie
   (213 states) does not shrink at all when accept states carry meter labels,
   because indravajra and upendravajra cannot share their identical tail.
   So the design keeps **two** objects: a minimized unlabeled acceptor per
   meter family for fast reachability, and a labeled determinized DFA for
   identification. Both are derived from the same NFA and are tested to accept
   the same language.
3. The jati grammars are not machine-readable yet. `ganalu` for variable
   meters is Telugu prose. The first real task is data entry.

---

## 3. Data: a structured `structure` block per meter

Added to every entry of `meter_rules.yaml` (existing fields stay untouched;
the prāsa engine only reads `name`, `prasa`, `prasa_yati`, `padalu`).

```yaml
- id: 32
  name: ataveladi
  # …existing fields…
  structure:
    system: gana                      # gana | matra | fixed
    slots:
      odd:  [surya, surya, surya, indra, indra]
      even: [surya, surya, surya, surya, surya]
    slot_pattern: [odd, even, odd, even]
    yati_ganas: [4]                   # 1-based gana index per line; [] = none
```

```yaml
- id: 20
  name: kandamu
  structure:
    system: gana
    slots:
      odd:  [kanda, kanda, kanda]
      even: [kanda, kanda, kanda, kanda, kanda]
    slot_pattern: [odd, even, odd, even]
    yati_ganas: {odd: [], even: [4]}
    constraints:                      # names resolve to functions in constraints.py
      - {rule: forbid_gana, slot: odd,  positions: [1, 3], gana: ja}
      - {rule: forbid_gana, slot: even, positions: [2, 4], gana: ja}
      - {rule: require_gana, slot: even, positions: [3], gana: [ja, nala]}
      - {rule: line_ends_with, slot: even, weight: U}
    stanza_constraints:
      - {rule: first_akshara_weight_uniform}   # verify against Appakavīyamu before trusting
```

```yaml
- id: 1
  name: utpalamala
  structure:
    system: fixed
    slots: {all: [భ, ర, న, భ, భ, ర, వ]}
    slot_pattern: [all, all, all, all]
    yati_aksharas: [10]
```

```yaml
- id: 27
  name: madhuragati_ragada
  structure:
    system: matra
    slots: {all: [m4, m4, m4, m4]}    # m4 = any pattern totalling 4 matras
    slot_pattern: [all, all]
    yati_ganas: [3]
```

Gana tokens resolve through `ganas.yaml`:

| token | resolves to |
|---|---|
| a trika/dvyakshara/ekakshara name (`భ`, `వ`, `గా`, `గ`, `ల`) | one literal pattern |
| `surya`, `indra`, `chandra` | the class in `upaganas` |
| `kanda` | `{భ, జ, స, నల, గా}` (new `kanda_ganas` class in `ganas.yaml`) |
| `m3`, `m4`, `m5` | every U/I string with that matra total |
| `all_laghu(X)` | class X restricted to laghu-only members (sarvalaghu variants) |

Other structural fields: `repeatable: true` (dvipada, ragada: the stanza is a
stream of units), `followed_by: [ataveladi, tetagiti]` (seesam's gīta),
`variant_of: kandamu` (already in `meters.txt`, moved into the yaml as
`is_variant_of`), `final_laghu_as_guru: true` (line-final laghu may scan
as guru; default true for vrittas, off for jati).

---

## 3b. Theory layer: one prosodic grammar per meter

*(revised 2026-09-13 after review: the grammar must read like a poem.)*

Every meter is first written as a four-level **prosodic grammar** over the
terminals {U, I, ⏎}:

```
Poem      → Line_odd ⏎ Line_even ⏎ Line_odd ⏎ Line_even      # poem = lines separated by ⏎
Line_odd  → Kanda−జ Kanda Kanda−జ                              # line = gana classes
Kanda     → భ | జ | స | నల | గా                                 # class = choice of ganas
భ         → U I I                                              # gana = symbols
```

Constraints are spelled into the class names (`Kanda−జ`, `Kanda=జ|నల`,
`Kanda$U`); the kanda stanza rule becomes `Poem → Poem⟨U⟩ | Poem⟨I⟩`;
repeatable meters use `Poem → Unit | Unit ⏎ Poem`. Because no nonterminal
is recursive except that right recursion, the grammar **flattens** into one
right-linear grammar over {U, I, ⏎} (`L2.G3` = line 2, about to read gana
3), whose strict form is the *prosodic automaton* — one DFA per meter that
accepts exactly that meter's stanzas (module `prosody.py`, artifacts
`grammars/<meter>.rlg`, tests `test_imd_prosody.py`). The per-line
right-linear grammars below are the pieces this flattening is made of and
what the line DAWG is built from.

Every `(meter, slot)` is written as a **right-linear grammar** over the
terminal alphabet Σ = {U, I}: productions of the form `A → wB` or `A → w`,
with `w ∈ Σ*` (Hopcroft–Ullman form). Right-linear grammars generate exactly
the regular languages, and the strict form (`A → aB | a | ε`, one terminal per
production) is a finite automaton written as rules: nonterminal = state,
`A → aB` = edge, `A → a` = edge into the accept state. That is the theorem
the whole implementation rests on, and it is checked mechanically:

```
grammar (gana-level)  ──to_strict──▶  grammar (strict)  ──grammar_to_nfa──▶  NFA
      │                                                                        │
      └── enumerate derivations ──────────────── equal sets ──── enumerate paths ┘
```

**Gana-level form** (what a human reads; nonterminal `Gk` = "about to read
gana k"):

```
tetagiti, slot all
G1 → III G2 | UI G2            # surya
G2 → UII G3 | UIU G3 | UUI G3 | IIII G3 | IIIU G3 | IIUI G3   # indra
G3 → UII G4 | …                # indra
G4 → III G5 | UI G5            # surya
G5 → III | UI                  # surya, last gana: terminal-only production
```

**Strict form** (what the automaton is built from): `G2 → U G2_UII_1`,
`G2_UII_1 → I G2_UII_2`, `G2_UII_2 → I G3`, … — `A_<pattern>_<i>` means
"inside alternative `<pattern>` of `A`, `i` symbols already read", and every
strict production carries a comment saying which gana, which symbol of it,
and where it leads.

Positional constraints (kanda's forbidden జ at odd ganas, the required
జ/నల at gana 6, the guru at the half's end) are applied *when the productions
are written*, by removing alternatives at that position. So the constraint
is visible in the grammar itself, not hidden in code. The only cross-line
rule (kanda's uniform first akshara) is a stanza rule and is documented as
such.

Artifacts:

- `grammars/<meter>.rlg` — one file per meter, one grammar in three forms:
  (1) hierarchical, (2) right-linear over {U, I, ⏎}, (3) strict with every
  nonterminal explained; regenerated by `python3 -m indic_meter_dawg grammars`.
- `docs/grammars/<meter>.md` — the "dumbed down" explanation per meter: what
  the meter is, the line recipe in plain words, the rules one by one, the
  productions with commentary, one worked derivation, the yati positions,
  what the grammar deliberately does not check (yati sounds, prāsa), language
  size, and a link to the diagram.
- `docs/grammars/README.md` — a primer: what a right-linear grammar is, how to
  read the notation, why it is the same thing as the DAWG, and a glossary of
  the gana names.

Modules added to the package: `grammar.py` gains `Grammar`, `Production`,
`gana_level_grammar(spec, slot)`, `to_strict(grammar)`, `derive(grammar,
max_len)`, `format_grammar(grammar)`; `docs.py` writes the markdown.

Tests added: every grammar is right-linear by construction (checked
syntactically), strict ≡ gana-level by enumeration, grammar ≡ NFA ≡ DFA by
enumeration, kanda constraints visible as missing alternatives, every meter
has a `.rlg` and a doc page, docs mention every rule the yaml declares.

## 4. Package layout

```
meter_engine/
├── meter_rules.yaml            + structure blocks           (data)
├── ganas.yaml                  + kanda_ganas class          (data)
├── indic_meter_dawg/                 the package  (import indic_meter_dawg)
│   ├── __init__.py             public API re-exports, __version__
│   ├── symbols.py              alphabet, notation normalisation, matra weights
│   ├── ganas.py                GanaRegistry: patterns, classes, token resolution
│   ├── catalogue.py            MeterSpec / SlotSpec dataclasses, YAML loader, validation
│   ├── grammar.py              right-linear Grammar (gana-level + strict), derivations, formatting
│   ├── prosody.py         hierarchical prosodic grammar (Poem → lines → classes → ganas), flattening, prosodic automaton
│   ├── constraints.py          named constraint functions (forbid_gana, require_gana, …)
│   ├── automaton.py            NFA, DFA, State, Edge; union, determinize, minimize, enumerate, count
│   ├── builder.py              MeterSpec → line NFA per slot → LineDawg (labeled DFA + family acceptors)
│   ├── walker.py               feed one line: accept labels, live hypotheses, death points, viable-prefix
│   ├── parser.py               segment a line under one (meter, slot): ganas + yati akshara indices
│   ├── stanza.py               StanzaAutomaton: slot patterns, repeats, composites, stanza constraints
│   ├── identify.py             identify(lines, …) → IdentificationResult; ranking; explanations
│   ├── diagram.py              DOT + Mermaid emitters: rule cards, tries, family views, index
│   ├── render.py               call system `dot` if present; write diagrams/
│   ├── docs.py                 per-meter plain-language grammar documentation (markdown)
│   └── cli.py                  python3 -m indic_meter_dawg identify|diagram|enumerate|stats
├── grammars/                   generated .rlg grammar files, one per meter
├── docs/grammars/              generated plain-language documentation + primer
├── diagrams/                   generated (svg, dot, md) — committed, regenerable
├── tests/
│   ├── test_prasa_rules.py     existing, untouched
│   ├── test_symbols.py
│   ├── test_ganas.py
│   ├── test_catalogue.py
│   ├── test_grammar_constraints.py
│   ├── test_automaton.py
│   ├── test_builder_language.py
│   ├── test_walker.py
│   ├── test_parser.py
│   ├── test_stanza.py
│   ├── test_identify.py
│   ├── test_fixtures_classics.py
│   ├── test_diagram.py
│   ├── test_cli.py
│   └── fixtures/               golden stanzas (yaml), ambiguity fixtures
├── METER_DAWG_PLAN.md          this file
└── METER_DAWG_README.md        usage, written in phase 4
```

Rules for the code:

- Every module is functions plus small frozen dataclasses. No class holds
  behaviour that a function could hold; classes exist for typed records
  (`MeterSpec`, `State`, `Edge`, `LineMatch`, `IdentificationResult`).
- Nothing imports outside the standard library except `yaml`.
- Each public function has a docstring with one example. Module docstrings
  say what the module owns and what it must not know about.
- Importable two ways, like the prāsa engine: `import indic_meter_dawg` with
  `meter_engine/` on `sys.path`, or `from meter_engine import indic_meter_dawg`
  from the project root (add an empty `meter_engine/__init__.py`).

---

## 5. Core data model

```
Edge      = (src: int, symbol: 'U'|'I', dst: int, weight: int)     # weight = matras (1|2)
NfaState  = (meter, slot, gana_index, offset_in_gana, gana_pattern) # fully explains itself
Nfa       = start states, edges, accept states
Dfa       = states are frozensets of NfaState; accept label = frozenset[(meter, slot)]
LineDawg  = labeled Dfa + per-family minimized acceptors + index: meter → slots → dfa state ids
Hypothesis = (meter, slot)
LineMatch  = (meter, slot, ganas: [pattern…], gana_names, yati_aksharas: [int…], matras)
Candidate  = (meter, slot_assignment: [slot per line], line_matches, score, notes)
IdentificationResult = (candidates ranked, ambiguous: bool, unknown_report | None)
```

Pipeline:

```
meter_rules.yaml + ganas.yaml
        │ catalogue.load_catalogue()
        ▼
   [MeterSpec…]  ──grammar.line_grammar(spec, slot)──▶ LineGrammar
        │                                                  │ builder.grammar_to_nfa()
        │                                                  ▼
        │                        union over all (meter, slot) ──▶ Nfa ──determinize──▶ labeled Dfa
        │                                                                     │ minimize (per family, unlabeled)
        ▼                                                                     ▼
 stanza.build(spec)                                                       LineDawg
        │                                                                     │
        └──────────────── identify.identify(lines) ◀── walker.walk(line) ◀────┘
                                   │
                                   ├─ parser.segment(meter, slot, line)   (gana split + yati indices)
                                   └─ IdentificationResult
```

Why the NFA is built compositionally instead of by string enumeration:
seesam alone is 186,624 strings; concatenating gana-choice sub-automata is a
few hundred NFA states and scales to dandakas (which need a cycle) and to
every new meter someone adds.

---

## 6. Algorithms

**Line acceptor.** For each `(meter, slot)`: chain of gana positions; at
position k an NFA branch per allowed pattern; constraints filter the branch
set per position (they are all positional, so they compile away before
determinization; the only genuinely cross-line one, kanda's uniform first
akshara, lives at stanza level). Union all `(meter, slot)` NFAs under one start
state. Subset construction gives a DFA whose states are sets of NFA states;
accept label = the `(meter, slot)` pairs present. Because `{U, I}` is binary
and lines are ≤ 30 aksharas, this is small (expected low thousands of states).

**Minimization.** Moore partition refinement (handles the cyclic dandaka case
later; on acyclic input equals signature hashing). Applied to unlabeled
per-family copies used for viable-prefix queries and diagrams. Test: language
equality with the labeled DFA by full enumeration (finite, ~370k strings, a
few seconds).

**Walker.** `walk(dawg, line) → WalkResult(accepted: set[Hypothesis],
died: {Hypothesis: akshara_index}, viable_prefix: bool)`. Death points come
from running the labeled DFA and, on rejection, replaying per-hypothesis (a
cheap second pass over the single meter's NFA). `final_laghu_as_guru` is
implemented as a second walk with the last symbol flipped; both outcomes are
recorded, so the result says "accepted under the pādānta rule".

**Parser.** Given `(meter, slot, line)` recover the gana sequence by DFS over
that slot's grammar (at most a handful of alternatives; return all, mark the
first as canonical, deterministic ordering). Yati akshara index for gana k =
1 + sum of lengths of ganas before k. This is the hook the yati engine uses.

**Stanza.** For each meter: line count (or `repeatable` unit length), slot
pattern, optional composite. `identify` intersects per-line hypothesis sets
under the slot pattern, applies stanza constraints, applies `variant_of`
(report `sarvalaghu_kandamu` in preference to `kandamu` when both hold, but
list both), and ranks: exact matches first, then by specificity (variant over
parent), then by catalogue id as a stable tie-break. Ambiguity is a first-class
field, never silently broken.

**Unknown report.** If no meter survives: for every meter, the first line
that failed and the akshara at which its last hypothesis died, plus the
longest-surviving meter. This is the diagnostic the proposal's near-miss
analysis needs, and it costs nothing extra.

---

## 7. Diagrams

`diagram.py` is pure: it returns DOT / Mermaid text. `render.py` does I/O.

1. **Rule card per meter** (`diagrams/meters/<name>.svg` + `.md` with the
   Mermaid). Railroad style: one node per gana position, the allowed patterns
   inside the node (`భ UII | ర UIU | …`), a marked node border at yati
   positions, one row per slot, the slot pattern and prāsa/prāsa-yati flags in
   a footer. Reads like the ASCII sketch in the brainstorm.
2. **Vritta trie** (`diagrams/vritta_trie.svg`): all fixed meters, edges
   labeled U/I, leaves labeled with the meter; branch points annotated with
   the akshara index at which the meter becomes unique.
3. **Family DAWGs** (`diagrams/family_<jati|upajati|ragada>.svg`): the
   minimized acceptor; gana boundaries drawn as clusters.
4. **Index** (`diagrams/README.md`): table of every meter linking its card,
   with akshara range, line count, slot pattern, yati positions, language size.
5. Optional full DAWG dump in DOT for tooling, not for reading.

All generated by `python3 -m indic_meter_dawg diagram --out diagrams/`. Tests check
the DOT is syntactically balanced and every meter has a card; rendering tests
skip when `dot` is absent.

---

## 8. Tests

Standard library `unittest`, `subTest` for parametrisation, seeded `random`
for property-style loops (no hypothesis dependency). Target: several thousand
executed cases across ~15 files, a few seconds total, all runnable with

```
python3 -m unittest discover -s meter_engine/tests -v
```

| File | What it pins down |
|---|---|
| `test_symbols` | every notation normalises to the same string; invalid symbols raise; matra totals |
| `test_ganas` | registry integrity: patterns unique, matras = 2·U + I, aksharas = len; class memberships exactly as `ganas.yaml`; token resolution incl. `m3/m4/m5`, `all_laghu` |
| `test_catalogue` | every meter has a `structure`; `padalu` = len(slot_pattern); fixed meters' length = `aksharalu`; yati positions inside range; variant links resolve; unknown tokens fail loudly |
| `test_grammar_constraints` | each named constraint on hand-built cases; kanda rules reproduce the textbook list; constraints compile to the same language as a brute-force filter |
| `test_automaton` | union/determinize/minimize on toy NFAs; minimality (no equivalent state pair); enumerate/count agree; acyclicity |
| `test_builder_language` | per (meter, slot): language size equals the itertools count (tetagiti 288, ataveladi odd 288/even 32, seesam 186,624, …); every fixed meter is a singleton; labeled DFA ≡ minimized family acceptors by full enumeration; total distinct strings and ambiguity counts match the probe table (regression guard) |
| `test_walker` | every generated line accepted with the exact label set; one-symbol mutations of vritta lines rejected; death index correct; viable-prefix monotone; pādānta flag behaviour |
| `test_parser` | segmentation returns the generating gana sequence (or contains it when ambiguous); yati akshara indices match the closed form; deterministic ordering |
| `test_stanza` | slot patterns; dvipada 2/4/6 lines; seesam + gīta; kanda uniform-first-akshara; wrong line count rejected with the right reason |
| `test_identify` | for every meter, 200 seeded random valid stanzas → that meter is the top candidate; mutate a random akshara → not identified as that meter, unknown report names the right line and index; the 16 known ambiguous pairs report `ambiguous=True` with both meters |
| `test_fixtures_classics` | hand-scanned golden stanzas in `fixtures/classics.yaml` (Pothana utpalamala/champakamala/mattebha/sardula/kandam/seesam/tetagiti/ataveladi, Vemana ataveladi, Sumati kandam), each with its expected meter; kept small and reviewed |
| `test_diagram` | DOT balanced, all nodes referenced by edges declared, one card per meter, Mermaid parses by a simple grammar check, index lists all meters; rendering test skipped without `dot` |
| `test_cli` | JSON round trip for identify; diagram command writes files; exit codes |

Regression guard: the probe numbers in section 2 are asserted, so any edit to
the yaml that changes the language of a meter fails a test and must be
acknowledged by updating the expected count.

---

## 9. Phases and order

| Phase | Deliverable | Gate |
|---|---|---|
| 0 ✔ | `structure` blocks for all 33 meters, `kanda_ganas` in `ganas.yaml`, empty `meter_engine/__init__.py`; `grammar.py` gana-level + strict right-linear grammars, `grammars/*.rlg`, `docs/grammars/*.md` | strict ≡ gana-level by enumeration (test_imd_grammar_constraints) |
| 1 ✔ | `symbols`, `ganas`, `catalogue` + their tests | green |
| 2 ✔ | `grammar`, `constraints`, `automaton`, `builder` + language tests | probe counts reproduced exactly (370,308 lines incl. sarvalaghu seesam; 16,979 ambiguous; 1,340 states) |
| 3 ✔ | `walker`, `parser`, `stanza`, `identify`, `cli` + tests + classics fixtures | identification ≡ brute-force oracle on random, mutated and junk stanzas |
| 4 ✔ | `diagram`, `render`, `docs`, `diagrams/`, `METER_DAWG_README.md` | one card + one doc page per meter, index, committed artifacts checked against fresh generation |
| 5 ✔ (2026-09-14) | `scansion.py`: Telugu text → aksharas → U/I (report's 3-stage pipeline, five guru rules, vikalpa for the two open readings), `identify_text`, CLI `scan` / `identify --text`, `docs/scansion.md`, `test_imd_scansion.py` | report's worked examples and the hand-scanned classics reproduced; classics identified from raw text |
| 6 ✔ (2026-09-14) | full-corpus run (`scripts/corpus_run.py`, report in `reports/`): 7,317 of 10,066 Pothana records have a catalogued label; 7,307 (99.86%) identified as labelled, 0 as another meter, 10 unmatched (text faults or padas that break the gana rules; listed in the report for manual review). Along the way: 25 corpus mislabels corrected (`scripts/corpus_fix.py`, logged in `dataset/CORRECTIONS.md`); seesam padas printed as half-lines handled (`halves_per_line`); sarvalaghu seesam redefined as 6 నలల + 2 న from Pothana 11-72; the kanda uniform-first-akshara rule made a reported violation, not a rejection (Pothana 3-151, 3-616). Readings used: 6,883 canonical, 410 vikalpa, 14 compound-boundary. | — |
| later | yati engine (updates pending) and prāsa consume `LineMatch.yati_aksharas` / `Syllable.first_sound`; weighted nearest-meter search over the same `Edge.weight` | — |

Phases 1–4 are one sitting each; nothing in 3 or 4 changes the data model of 2.

---

## 10. Decisions (recorded 2026-09-13)

1. **Kanda rules — confirmed.** Ganas {భ, జ, స, నల, గా}; జ forbidden at odd
   gana positions of the half (1, 3, 5, 7); 6th gana జ or నల; the half ends in
   a guru; yati at gana 4 of lines 2/4; first akshara weight uniform across
   lines (stanza rule, still marked "verify against Appakavīyamu" in the docs).
2. **Pādānta laghu — default on** for every meter; per-call override.
3. **Seesam — confirmed.** Four 8-gana lines are the unit; the gīta is managed
   separately (identified on its own as ataveladi/tetagiti when lines follow).
4. **Ragada sub-types — confirmed** as pure matra ganas; generic `ragada` abstract.
5. **Utsahamu — confirmed** as 7 surya + one guru, yati at gana 5.
6. **Package name — `indic_meter_dawg`.**
7. **Theory first — added.** Right-linear grammars per meter (section 3b) are
   written and verified before the automaton is trusted; phase 0 now covers
   the structure blocks *and* the grammar generator + docs.

# indic_meter_dawg — Telugu meter identification from guru/laghu

Identify the chandassu of a poem given only its weight pattern, one line per
string. Every meter in `meter_rules.yaml` is written as a **prosodic grammar**
that reads like a poem — `Poem → Line ⏎ Line ⏎ Line ⏎ Line`, `Line → Surya
Indra Indra Surya Surya`, `Surya → న | హ`, `న → I I I` — flattened into a
**right-linear grammar** over `{U, I, ⏎}`, and compiled into one minimized
**weighted directed acyclic word graph** (DAWG) that the identifier walks.
Yati and prāsa are not checked here; the parser reports *where* they must
hold so the later engines can check them. A scanner (`scansion.py`) turns
Telugu text into U/I first, so `identify_text` goes from raw verse to meter.

| Piece | Where |
|---|---|
| package | `indic_meter_dawg/` (standard library + PyYAML) |
| data | `meter_rules.yaml` (`structure:` block per meter), `ganas.yaml` |
| grammars | `grammars/<meter>.rlg` — one prosodic grammar per meter in three forms: hierarchical, right-linear, strict (every nonterminal explained) |
| plain-language docs | `docs/grammars/<meter>.md`, primer in `docs/grammars/README.md`, scansion rules in `docs/scansion.md` |
| diagrams | `diagrams/meters/*.svg` rule cards, `diagrams/vritta_trie.svg`, `diagrams/dfa/*.svg`, index `diagrams/README.md` |
| tests | `tests/test_imd_*.py` (+ `tests/fixtures/`) |
| plan | `METER_DAWG_PLAN.md` |

## Quick start

```bash
cd meter_engine
python3 -m indic_meter_dawg identify UIIUIUIIIUIIUIIUIUIU UIIUIUIIIUIIUIIUIUIU UIIUIUIIIUIIUIIUIUIU UIIUIUIIIUIIUIIUIUIU
python3 -m indic_meter_dawg identify --file poem.txt --json     # one U/I line per file line
python3 -m indic_meter_dawg identify --text --file verse.txt     # Telugu lines: scan to U/I, then identify
python3 -m indic_meter_dawg scan --rules "శ్రీరాముని దయచేతను"     # aksharas, U/I, and the rule behind each guru
python3 -m indic_meter_dawg walk UUIIIIIUIUUIIU                  # who accepts this line, who dies where
python3 -m indic_meter_dawg prefix UIIUIU                        # meters that can still complete
python3 -m indic_meter_dawg grammar kandamu                      # the prosodic grammar: Poem → lines → classes → ganas
python3 -m indic_meter_dawg grammar kandamu --level line --slot even   # one line, right-linear (G1 → …)
python3 -m indic_meter_dawg grammar kandamu --level flat         # the whole poem, right-linear over {U, I, ⏎}
python3 -m indic_meter_dawg grammar kandamu --level strict       # one symbol per production, every state explained
python3 -m indic_meter_dawg stats
python3 -m indic_meter_dawg grammars && python3 -m indic_meter_dawg docs && python3 -m indic_meter_dawg diagrams
```

```python
import sys; sys.path.insert(0, "meter_engine")
from indic_meter_dawg import identify, walk, viable_prefix, segment

# Pothana, "ఇందు గలఁ డందు లేఁ డని…" (tests/fixtures/classics.yaml)
res = identify(["UIIIUIUII", "UUIIIIIUIUUIIU", "UUIIIIUII", "UUUIIIUIUIIUU"])
res.best.meter                       # 'kandamu'
res.ambiguous                        # False
res.best.lines[1].segmentation.gana_names     # ('గా', 'నల', 'జ', 'గా', 'స')
res.best.lines[1].segmentation.yati_aksharas  # (10,)  -> the yati engine checks akshara 10 against akshara 1
print(res.explain())

walk("UUUUUUUU").accepted            # {('vidyunmala','all'), ('madhuragati_ragada','all')}

from indic_meter_dawg import identify_text, scan
identify_text("శ్రీరాముని దయచేతను\nనారూఢిగ సకల జనులు నౌరా యనగా\nధారాళమైన నీతులు\nనోరూరగ జవులు పుట్ట నుడివెద సుమతీ").best.meter   # 'kandamu'
scan("చక్రి")[0].format()             # 'చ క్రి | UI | vikalpa@1'  — the ర-vattu reading is recorded, not guessed
viable_prefix("UUUUUUU")             # hypotheses still alive: the generation-time query
```

Accepted notations: `U/I`, `G/L`, `-/u`, `—/˘`, `S/I`, Telugu `గ/ల`, and the
textbook `U` / `|`; spaces, commas and slashes are ignored.

## What the identifier returns

`IdentificationResult` — `candidates` ranked best first, `ambiguous` (two
unrelated meters tie; yati/prāsa needed), `failures` (when nothing matches:
for every meter the line and akshara where its last hypothesis died),
`explain()`, `to_dict()`, `to_json()`. Each `Candidate` carries the meter,
its Telugu name and family, the slot of every line, the gana segmentation
and yati akshara indices per line, whether the pādānta rule (line-final laghu
read as guru) was needed, and a `trailer` for seesam + gīta.

Ranking: exact matches before pādānta matches; a variant (sarvalaghu kandamu)
above its parent; then catalogue order. Ambiguity is never resolved by
guessing. A line may also be given as per-akshara options (`"UI"` = guru,
laghu admissible); the walker then simulates the DAWG over a lattice and
the result reports the pattern actually accepted. Seesam padas printed as
two half-lines (the corpus convention) are joined automatically.

## The grammar of a meter

`python3 -m indic_meter_dawg grammar kandamu` prints (abridged):

```
# poem
Poem → Poem⟨U⟩ | Poem⟨I⟩                          # stanza rule: every line starts with the same weight
Poem⟨U⟩ → Line_odd⟨U⟩ ⏎ Line_even⟨U⟩ ⏎ Line_odd⟨U⟩ ⏎ Line_even⟨U⟩
# lines
Line_odd⟨U⟩ → Kanda−జ⟨U⟩ Kanda Kanda−జ            # slot odd: 3 ganas
Line_even⟨U⟩ → Kanda⟨U⟩ Kanda−జ Kanda=జ|నల Kanda−జ Kanda$U
# gana classes
Kanda → భ | జ | స | నల | గా
Kanda−జ → భ | స | నల | గా                          # the class minus జ (constraint)
Kanda=జ|నల → జ | నల                                # only జ or నల allowed there
Kanda$U → స | గా                                   # only members ending in a guru
# ganas → symbols
భ → U I I
```

Four levels: poem → lines (⏎ between them) → gana classes → ganas → symbols.
Constraints are spelled into the class names; the kanda stanza rule becomes
two branches of `Poem`. The same grammar flattened (`--level flat`) is
right-linear: `Poem → UII ⟨U⟩L1.G2 | …`, `⟨U⟩L1.G3 → UII⏎ ⟨U⟩L2.G1 | …`.
Its strict form (`A_UUI_2` = inside alternative UUI of A, two symbols read)
is the prosodic automaton, which accepts exactly the stanzas of that meter.

## From text to U/I

`scansion.py` (rules in `docs/scansion.md`): Unicode → categories →
aksharas (conjuncts kept together, word-final dead consonants merged
back) → weights by the five guru rules of Chandodarpanam, with the two
open readings (laghu before a word-initial conjunct, syllable before a
ర-vattu conjunct) recorded as *vikalpa* rather than decided. `identify_text`
identifies the canonical scansion and, if nothing matches, lets the DAWG
walk a lattice of the admissible alternative readings (declared vikalpa,
then compound-boundary readings before a conjunct) and reports which
aksharas were read the other way.

## How it is built

```
meter_rules.yaml + ganas.yaml
  → catalogue.MeterSpec                (typed, validated)
  → prosody.prosodic_grammar           Poem → Line ⏎ Line … (hierarchical, for reading)
  → grammar.gana_level_grammar          G1 → III G2 | UI G2 …   (per line, right-linear)
  → prosody.flatten                L1.G5 → III⏎ L2.G1 …    (whole poem, right-linear over U, I, ⏎)
  → grammar.to_strict                   G1 → I G1_III_1 …       (one terminal per rule = automaton)
  → automaton.nfa_from_strict_grammar   nonterminal = state
  → automaton.union → determinize → minimize (labels kept)     the DAWG
  → walker (per line) → stanza (line count, odd/even slots, stanza rules) → identify (rank, explain)
  → parser.segment (gana split + yati positions, the hook for yati/prāsa)
  → prosody.prosodic_automaton         one DFA per meter over {U, I, ⏎}; accepts_poem(meter, lines)
```

Positional constraints (kandamu's జ rules, the final guru) are applied when
the productions are written, so they are visible in the grammar text and in
the rule card. The only cross-line rule (uniform first akshara in kandamu) is
a stanza rule.

Headline numbers for the current catalogue (pinned in
`tests/fixtures/expected_counts.yaml`):

| | |
|---|---|
| meters / line slots | 37 / 40 |
| NFA states | 1,171 |
| DFA states, minimized (unminimized) | 1,431 (1,573) |
| distinct legal lines | 370,315 |
| lines accepted by more than one meter | 16,979 (seesamu vs taruvoja: 16,416) |
| longest line | 36 aksharas |

## Adding a meter

Add an entry to `meter_rules.yaml` with a `structure:` block (see the plan,
section 3, or any existing entry), run the tests, regenerate grammars, docs
and diagrams. No code changes. The regression fixture will fail on the
changed counts; update it deliberately.

## Tests

```bash
python3 -m unittest discover -s meter_engine/tests -p "test_imd_*.py" -v
```

Standard library only (`pytest` also works). Every grammar is checked to be
right-linear and to derive the same language in both forms; every slot
automaton is checked against its grammar by full enumeration; the labeled
DAWG is checked against the unminimized one by product construction; the
identifier is checked against a brute-force oracle on random valid stanzas,
mutated stanzas and random junk; random poems derived top-down from every
hierarchical grammar are accepted by the identifier, by the flattened
grammar and by the prosodic automaton, and the prosodic automaton agrees with the
oracle on mutated and junk stanzas; hand-scanned classical stanzas (Pothana,
Sumati, Vemana) are in `tests/fixtures/classics.yaml`; the committed
grammars, docs and diagrams are checked to equal a fresh generation.

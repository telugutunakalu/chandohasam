# Constrained decoding on the metrical DAWG — plan

> **Status (2026-09-25): prāsa + yati enforced exactly; E4B constrained grid done (§14).**
>
> * **Decided:** models Gemma-4 E4B first, then DiffusionGemma 26B-A4B (the
>   translategemma vLLM server is stopped for that run); no head-to-head with the
>   IndicNeuroSym code (EXP-37 dropped); package `meter_engine/metrical_decoder/`;
>   constrained runs wait until prāsa and yati are enforced exactly.
> * **Program:** for every meter, (1) a *baseline* — the meter's rules and a topic
>   in the prompt, free generation; (2) the three constrained strategies on the
>   same prompts. Every generated token is logged with its probability (§5.8).
>   Existing models only; fine-tuned and larger models later.
> * **Built** (`metrical_decoder/`, 53 tests): incremental scanner, orthography
>   filter, enforcer, prāsa + yati registers judged by the engines, the three
>   strategies + baseline with per-token traces, random-logit and Hugging Face
>   sources, parallel masks, rule-generated prompts, evaluation by the engines,
>   grid runner with resume, CLI.
> * **Done:** E4B baseline grid, 37 meters × 3 topics × 5 seeds
>   (`experiments/runs/2026-09-24_e4b_baseline/`): 555 poems, 0 in meter.
>   Random-logit control with gaṇa + prāsa + yati over all 37 meters
>   (`experiments/runs/2026-09-24_control_final/`, 3 strategies × 5 seeds):
>   every completed poem accepted by the engines; the one dead end (సీసము) fixed
>   and rerun (§12).
> * **Done:** E4B constrained grid, gaṇa + prāsa + yati (strict), the
>   baseline's prompts, topics, seeds and config: 37 × 3 × 5 × 3 strategies =
>   1,665 poems (`experiments/runs/2026-09-24_e4b_constrained/`, launcher
>   `experiments/scripts/run_e4b_constrained.sh`): **100% in meter by the
>   engines for all three strategies** (after the token budget was set to the
>   provable bound, §14); chosen-token logp −2.2 to −2.35 against −0.84 free,
>   lexical rate 17–20% against 41%. Next: DiffusionGemma (§13).
>
> Findings of the day that changed the design are in §12.

Goal: generate Telugu padyams in **any of the 37 catalogued meters**, with
gaṇa structure guaranteed by the DAWG and prāsa / yati enforced by the
existing engines' rules, using the three IndicNeuroSym strategies as the
decoding loops. The DAWG replaces the hand-built dvipada FST + NFA enforcer;
the strategies stay algorithmically the same.

Scope is the three benchmarked strategies only. Out of scope: Alg. 4
(stateless rejection sampling), the adapted-Chandomitra baseline, dataset
curation and LoRA fine-tuning (paper §4–6), Kannada ragale.

---

## 1. What IndicNeuroSym contributes, and what it needs from a back end

The paper's Symbolic Enforcer (Fig. 1, Table 13) is a chain of
codepoint classifier → syllable assembler (4-state Mealy FST) → guru/laghu
classifier (2-state, one-syllable delay) → position tracker → three parallel
NFAs (gaṇa ~69 states, prāsa 7, yati 4) → dead-state detection (Alg. 1) →
token mask. It is written for dvipada (and, with a smaller gaṇa NFA, ragale).

All three strategies call the enforcer through **four primitives** and
nothing else:

| primitive | used by | meaning |
|---|---|---|
| `snapshot / clone` | all (Alg. 3 per candidate, Alg. 5–6 checkpoints) | copy the composite state |
| `feed(token_text)` | all | advance the FST + NFAs over the token's characters |
| `is_alive()` | all (BuildGanaMask, Alg. 3) | the prefix can still become a valid poem |
| `has_accept()` | force-NL rule (Alg. 5–6), hybrid re-ranking (Alg. 6) | the current line is complete |

Any back end that provides these four, exactly, runs the three strategies
unchanged. The DAWG provides all four, for every meter, from data.

---

## 2. Component mapping

| IndicNeuroSym | on the DAWG | what changes |
|---|---|---|
| Stage 0 codepoint classifier | `scansion.classify_char` | same categories (scansion.py is already a re-implementation of this pipeline) |
| Stage 1 syllable assembler + `prev_syllable` buffer | `scansion.syllabify` on the unfinished word + committed/pending split (§5.2) | parity with the verifier by construction: one implementation of the rules |
| Stage 2 guru/laghu classifier, `PENDING_I` delay | `scansion.classify` + pending option sets (§5.2) | validated on 2.3 M corpus prefixes |
| position tracker (line, syllable, line count) | the automaton state + an akshara-in-line counter | no separate controller |
| gaṇa NFA (~69 states, branch sets) | `prosody.prosodic_automaton(meter)`: minimal DFA over {U, I, ⏎} (dvipada: 38 states) | deterministic; all 37 meters; stanza rules (line count, odd/even slots, kanda first-akshara) included |
| dead-state detection, Alg. 1 (`min_dist`/`max_dist` closed forms for 11–15 syllables) | the automaton is trimmed: a missing transition *is* a dead state | exact and meter-agnostic; no per-meter constants |
| prāsa NFA (7 states, consonant as data variable) | prāsa register + a compatibility table compiled from `prasa_rules.yaml` (§5.4) | the engine's rules, not a 3-group approximation |
| yati NFA (4 states, 11 maitri groups) | yati register + role annotations on automaton edges + a table compiled from the yati engine (§5.4) | gaṇa-yati, akshara-yati, సీసము's second vali, bahuyati, prāsa-yati fallback |
| `CompositeState` clone | an immutable tuple (§5.5) | O(1) snapshots and checkpoints; hashable, so memoisable |
| BuildGanaMask, Alg. 3 | same loop over the Telugu vocabulary slice | successor states are kept for the hybrid pass |
| "force NL on ACCEPT" | `must_end_line` (default) or `line_complete` (paper-parity mode) | see §4.3 |
| "filter spurious newlines" | ⏎ is in the mask only when the automaton has a ⏎ edge after flushing the word | automatic |

What IndicNeuroSym has that the DAWG path does not (yet): the Kannada
ragale scanner and gaṇa NFA. The automaton layer is script-agnostic (it sees
only U/I/⏎); only the scanner and the catalogue would need Kannada entries.

---

## 3. Facts that shaped the design

Six probes, run 2026-09-24 in `.venv` (Python 3.12, PyYAML; torch 2.13.0+cu130
and transformers 5.15.0 installed but no model loaded — the GPU was serving
vLLM). Scripts in the session scratchpad; §11 says how to re-run them.

**A. The automata are small, live and deterministic.**

| measure | value |
|---|---|
| whole-poem prosodic DFA per meter | 26 (hayapracara ragada) – 291 (సీసము) states; 3,018 over all 37 meters; dvipada 38, kandamu 109, utpalamala 84 |
| trimmed (every state can reach an accept) | all 37 → `alive ⇔ transition exists` |
| legal lines with more than one gaṇa segmentation | **0 of 387,294** (per-slot languages summed) |
| automaton transitions whose yati role is ambiguous | **0** |

So the yati position of every syllable is known the moment it is read, from
the transition alone. IndicNeuroSym needed NFA branch sets for this; the
DAWG path needs none.

**B. Guru/laghu is prefix-stable under a committed/pending model.** For every
character prefix of every corpus line (Pothana, Vemana, Kūcimañci; 49,661
lines, **2,310,052 prefixes**): the syllables declared committed never
changed, and the final weights of the pending region were always among the
predicted options — **0 violations** of either kind. Pending option sets
have 1, 2, 3 or 5 members (24% / 33% / 21% / 23% of prefixes).

**C. The vocabulary slice.** Gemma-4 (E2B/E4B share it): 262,144 tokens,
**1,784 contain Telugu**, all pure Telugu with an optional leading space (864).
Syllables per token: 0 (20), 1 (835), 2 (680), 3 (201), 4 (43), 5 (5). Only
878 tokens start and end on akshara boundaries: 560 end on a bare consonant,
239 start with a dependent sign, 107 end in a virama — so the scanner must
carry pending state across tokens (which B makes safe). The tokenizer's own
split of శ్రీ is `శ` + `్రీ`: a token that starts with a virama is ordinary.
63 of the corpus's 65 Telugu codepoints have a single-character token; **ఁ
appears in no token at all** (byte fallback only), ఽ likewise. 10.5% of
corpus akshara types (82.2% of occurrences) are single tokens (cf. EXP-11).

**D. The three strategies work on the DAWG.** Random logits (EXP-12
protocol) over the 1,784 Telugu tokens + space + ⏎, τ = 0.7, top-p = 0.9,
all 37 meters × 3 strategies × 4 seeds, every output re-verified by the batch
pipeline (`accepts_poem` on `patterns(text)`, and `identify_text`):

| strategy | strictly valid | enforcer ≠ verifier | median tok/poem | median s/poem | median ms/mask (p95) | backtracks |
|---|---|---|---|---|---|---|
| masking-only | 147/148 | 0 | 56 | 1.76 | 31.8 (48.1) | — |
| masking + backtracking | 147/148 | 0 | 56 | 1.74 | 27.8 (46.9) | 0.00 |
| hybrid | **148/148** | 0 | 49 | 1.46 | 24.8 (44.4) | 0.00 |

`identify_text` named the target meter for every valid output. The single
failure (same seed, S1 and S2, పంచచామరము) exhausted the 400-token budget: line 3
was a chain of malformed signs (`ౌళ్ెంట్హ్న్స్ార్ేష్…`) that the scanner absorbs
without creating a syllable. Every token kept the state alive; none made
progress. Backtracking never fired because with an exact mask the valid set
never drops below 3. Both observations change the design (§4.1, §5.3).

**E. Tokenizer decode parity.** `tokenizer.decode` equals the enforcer's
token texts for all 1,786 tokens and for 3,000 random token sequences
(0 mismatches). EOS set for Gemma-4-it: `<eos>`, `<turn|>`, `<|tool_response>`.

**F. Prāsa splitter parity.** The prāsa engine splits aksharas with
`aksharanusarika`, not `scansion.py`. Ignoring ఁ and zero-width characters
(the prāsa engine drops ఁ), the two agree on the pūrva and prāsa aksharas in
**49,659 of 49,661** lines; both exceptions are an explicit ZWNJ after a
virama (`ల్‌`, `త్‌`), which generation will not emit (§5.3).

Also: of all 3,018 automaton states, exactly **one** (సీసము) is both a legal
line end and extendable — a 30-laghu line completes the regular form and
continues into the sarvalaghu form. Forcing ⏎ at the first accept (the
paper's rule) makes sarvalaghu సీసము unreachable.

---

## 4. What changes in the three algorithms

### 4.1 Exact liveness moves the failure modes

In the paper, masking-only reaches only 31.4% poem accuracy on dvipada-base,
partly because the alive predicate is approximate: it guarantees only that the next token keeps
the NFA reachable, and dead-state detection uses closed-form bounds. On the
DAWG, liveness is exact, so a metrical dead end cannot occur. What remains:

1. **no progress** — tokens that are alive but add no syllable (probe D);
2. **probability-mass collapse** — the model puts almost no mass on the
   valid set, so sampling is forced into its low-probability tail
   (degenerate or garbled text; EXP-13's collapse);
3. **token budget** — a long meter at ~1.1–1.3 syllables per token needs
   more than the paper's 150 tokens (లయవిభాతి: 4 × 36 aksharas).

The strategy loops keep the paper's structure; their triggers are adjusted
to these failure modes.

### 4.2 The three strategies on the DAWG

**S1 masking-only** (Alg. 5, backtracking off): unchanged. Adds the progress
guard (§5.3) and a budget derived from the meter: `max_tokens =
c × max_aksharas(meter)`, configurable. Random logits averaged 1.1–1.3
syllables per token, so c = 2 leaves headroom; EXP-36 measures a real model.

**S2 masking + backtracking** (Alg. 5): checkpoint every 3 tokens into a
ring buffer of 15 (a checkpoint is the state tuple + output length + τ),
temperature escalation +0.15 per consecutive backtrack (cap 1.2, decay over
6 tokens), reseed `seed + b·1337`, at most 30 backtracks — all as in the
paper. Triggers:

| trigger | status |
|---|---|
| `|V_valid| < 3` | kept for paper parity; rarely fires on the DAWG |
| line > 15 syllables | removed: a line cannot overshoot an exact mask |
| valid mass `Σ_{t∈V} π(t) < ε` (default 1e-3) | **new**: the DAWG-era analogue of "the alive set collapsed" |
| `stall ≥ k` tokens without a committed syllable (default 4) | **new**: catches probe D's failure |

Rollback also crops the model's KV cache to the checkpoint length.

**S3 hybrid** (Alg. 6): the masked distribution's top-K_r (100) candidates,
in probability order; `V_acc` = candidates after which the line is complete,
`V_alv` = all alive candidates; stop when `|V_acc| ≥ 3` or `|V_alv| ≥ 10` with
`V_acc` empty; sample from `V_acc` if non-empty, else `V_alv`; backtrack as a
last resort. Difference from the paper: the successor state of every
candidate is already computed by the mask pass, so the re-ranking pass is a
lookup, not a re-simulation (paper: `O(|V_tel| + K_r)` feeds per step; here
`O(|V_tel|)`).

### 4.3 End-of-line policy

`force_nl = "must_end"` (default): ⏎ is in the mask whenever the flushed
state has a ⏎ edge, and is forced only when no U/I edge remains.
`force_nl = "on_accept"`: the paper's rule, kept for the replication
(EXP-37). The two coincide on 36 of 37 meters (§3); they differ only on సీసము.
The hybrid's `V_acc` preference still pulls lines toward their earliest
legal end; for variable-length meters (dvipada 11–15, kandamu) EXP-39
measures the resulting line-length distribution against the corpus.

### 4.4 New capability: meter-family decoding

The union line DAWG (`default_dawg().dfa`, 1,431 states, with `reachable`
per state) supports masks of the form "some meter in this family can still
complete" (`walker.viable_prefix` is already this query). A poem-level
version is the union of the family's prosodic automata. This allows "any
vritta" or "kandamu or its sarvalaghu variant" generation, which the
dvipada-specific enforcer cannot express. Later phase (§8).

---

## 5. Architecture

A new package next to the engines, same conventions as `indic_meter_dawg`
(functions plus small frozen dataclasses; the core imports only the standard
library, `yaml` and the sibling engines; torch only in the model adapter).
Working name `metrical_decoder` (decision 1).

```
meter_engine/
├── metrical_decoder/
│   ├── __init__.py        public API
│   ├── automaton.py       annotated decoding DFA per meter (§5.1)
│   ├── incremental.py     committed/pending scanner over text chunks (§5.2)
│   ├── orthography.py     well-formedness filter + progress guard (§5.3)
│   ├── registers.py       prāsa and yati registers, tables compiled from the engines (§5.4)
│   ├── enforcer.py        Enforcer, DecodeState, TokenIndex, mask building (§5.5)
│   ├── strategies.py      masking_only / masking_backtrack / hybrid over a LogitsSource (§5.6)
│   ├── sources.py         LogitsSource protocol; RandomLogits (control); HFModel (torch, optional) (§5.7)
│   ├── evaluate.py        verification via chandohasam.analyze + lexicality/repetition metrics (§5.8)
│   └── cli.py             python3 -m metrical_decoder generate | control | bench
├── tests/test_dec_*.py
└── CONSTRAINED_DECODING_PLAN.md   this file
```

### 5.1 Decoding automaton

Built per meter from `prosody.flatten(spec)` → `to_strict` → NFA →
determinize → minimize, like `prosodic_automaton`, with every edge
annotated from its strict nonterminal (`L2.G3_UII_1` = line 2, gaṇa 3,
alternative UII, one symbol read):

| annotation | source |
|---|---|
| `line`, `gana`, `offset` | the nonterminal name |
| `prasa`: `anchor` / `check` | the edge leaving `L1.G1_*_1` / `Lk.G1_*_1` (akshara 2 of a line) when `spec.prasa` |
| `yati`: `vali` / `vali2` / `target(k)` | gaṇa-yati: edges leaving `Lk.G1` / `Lk.G5` (సీసము) / `Lk.G{y}`; fixed meters: akshara index `y` along the line's single path |

Minimization treats the annotation as part of the edge label (a Mealy
machine), so the result stays deterministic *and* annotated; probe A shows
the annotations are functional. Options: `units` (repeatable meters:
exactly n units; dvipada default 1 couplet), `trailer` (సీసము + ఆటవెలది / తేటగీతి
by concatenation), `padanta` (add line-final I edges where U is required; off
for generation), `meters=[…]` (union, §4.4). Compiled to flat arrays
`trans[q][sym] → q' | -1` and `ann[q][sym]`.

### 5.2 Incremental scanner

Under the default `ScanPolicy` (rule 5 does not cross a space) a word
boundary is a stable point: every syllable of a finished word has its final
weight. Inside the unfinished word with syllables `s1 … sm`, `s1 … s(m−2)`
are committed; `a = s(m−1)` and `b = sm` are pending. Let
`w(a) = U` if `a` is guru by rules 1–4 or `b` begins with a conjunct, else `I`.

| the text ends with | pending options (drop the `a` part when m = 1) |
|---|---|
| `C్` and `b` has no vowel (word-initial dead consonant) | `{U, I}` |
| `…V C్` (`b` has a vowel and a merged dead consonant) | `{w(a)·U, w(a)·UU, w(a)·UI}` — pollu now, or samyukta after a split plus a new syllable |
| an open cluster `C(్C)*` (no vowel sign yet) | `{x·U, x·I : x ∈ {w(a), U}} ∪ {U}` — onset may still grow; `b` may still die as a pollu |
| a closed syllable | `{w(a)·U}` if `b` is guru by rules 1–4, else `{w(a)·U, w(a)·I}` |

These rules call `scansion.syllabify / classify / self_rules`; they
implement no weight rule of their own, so the decoder and the verifier
cannot drift apart. NFC is applied to the word (a token boundary can split
`ె` + `ౖ`). A UTF-8 accumulator holds incomplete byte-fallback sequences
(needed only if ఁ is enabled, decision 7). Probe B is the acceptance test.

### 5.3 Orthography filter and progress guard

A small DFA over codepoint categories that accepts every corpus line and
rejects malformed sequences: a dependent sign after a boundary or after
another dependent sign of the same kind, two vowel signs in a row, a sign
after a virama, zero-width characters (removes probe F's two exceptions).
It composes with the scanner (product state), and it bounds the characters
per akshara, which bounds tokens per syllable, which guarantees progress.
A `stall` counter (tokens since the last committed syllable) remains as a
belt-and-braces trigger for S2 (§4.2). Gate: 100% of corpus lines accepted.
A word may not end in two dead consonants, nor consist of dead consonants
alone (§12, §15): neither occurs in the corpus, and each misled a register.

### 5.4 Prāsa and yati registers

**Principle — strict generation, lenient verification.** The decoder's
predicates must accept a *subset* of what the engines accept under the
chosen profile, so everything generated passes `chandohasam.analyze`. The
decoder may be stricter than necessary; it may never be looser. Every table
is compiled from the engines' own rule files and property-tested against
them. The final verdict always comes from the engines.

- **Prāsa.** At the `anchor` edge (line 1, akshara 2) store the onset and the
  pūrva (akshara 1) weight. At each `check` edge require an onset that
  `prasa_rules.yaml` accepts under the profile (table from
  `Ruleset.lookup_pair_rule`, all consonant pairs) and the same pūrva weight
  (the engine's pre-prāsa weight rule). While the pending akshara's onset is
  still open, require only that it can still become compatible (prefix
  test). `prasa=False` gives manjari dvipada.
- **Yati.** At a `vali` edge store the akshara (onset, vowel class, bindu);
  at a `target` edge require a positive verdict from the yati engine's
  pair rules under `sandhi="off"` (tables from `yati.pairing.pair_rule` over
  consonant × consonant × vowel class × bindu). While the target akshara is
  pending, require that some completion can match. Groups of three or more
  (స్రగ్ధర 1-8-15) carry the conjunct constituent used so far (బహుయతి నియతి).
  Where the meter allows ప్రాసయతి, a failed maitri leaves a one-step
  obligation on akshara `Y+1`. సీసము's second vali uses the `vali2` register.

Registers are data variables, as in the paper; the automaton does not grow.

### 5.5 Enforcer

```python
DecodeState = (q, word, utf8, line, akshara, ortho, stall, prasa_reg, yati_reg)   # hashable

class Enforcer:
    def initial(self) -> DecodeState
    def step(self, s, token_text) -> DecodeState | None     # feed; None = dead
    def line_complete(self, s) -> bool                      # has_accept
    def must_end_line(self, s) -> bool
    def poem_complete(self, s) -> bool
    def explain(self, s) -> str                             # where we are: line, gaṇa, pending options, registers

class TokenIndex:     # the vocabulary slice, texts from tokenizer.decode, static mask
    def mask(self, s) -> (bitset, {token: successor})
```

`step` walks the token's characters; each boundary finalises the word
(`word_weights`, memoised) and ⏎ feeds the automaton. `alive` = orthography
ok ∧ the committed part of the word keeps `q` live ∧ some pending option
does ∧ the registers are satisfiable. Static slice: Telugu tokens, space,
⏎, EOS (+ punctuation and byte tokens as options).

### 5.6 Strategies

`generate(enforcer, index, source, strategy, seed, τ, top_p, K_r, …)`,
shared across the three strategies as in the prototype, with §4.2's
triggers. The strategies depend only on the enforcer's primitives and
`LogitsSource`, so the same code runs the random-logit control and a real
model.

### 5.7 Model adapters

`LogitsSource`: `next_logits(ids) → vector` with an incremental KV cache and
`rollback(n)`. `RandomLogits` (control) needs no torch. `HFModel` wraps
transformers 5.15 with an incremental cache. Rollback crops the cache
(`DynamicCache.crop(n)`) where the cache class allows it; Gemma's
sliding-window layers may not, in which case the fallback re-prefills from
the checkpoint (poems are short, so this is cheap) — verify in phase 6. Masks are
applied as boolean tensors on the device (`masked_fill(~mask, -inf)`),
Gemma-4 chat template for the -it models, EOS set from probe E. S1 is also
offered as a `LogitsProcessor` for `model.generate`; S2 and S3 need the
manual loop (backtracking, re-ranking). vLLM is later: its logits processors
are batch-level, and the S2/S3 loops need per-request state.

### 5.8 Verification and metrics

Verifier: `chandohasam.analyze(text, profile, yati_sandhi="off", meter=target)`,
independent of the enforcer. Metrics: the paper's (poem accuracy with
gaṇa / prāsa / yati separately, line accuracy, tokens, masks, backtracks,
s/poem), plus what EXP-13/14 showed is needed to catch degenerate output:
real-word rate against a corpus lexicon built from `dataset/*.json`,
distinct-akshara ratio, duplicate lines, single-akshara fragments, and the
mean valid mass Σπ(valid) — how hard the model fights the mask, the
model-level analogue of EXP-15's attempts-to-valid.

Built: `python -m metrical_decoder report RUN_DIR … --out report.md`
(`metrical_decoder/analysis.py`) — by strategy, by meter and by position
(line start, prāsa akshara, yati aksharas, other): mean log-probability of the
chosen token, share at rank 1, share of steps where the model's own first
choice was forbidden ("overridden"), valid mass, entropy, and the lexical rate
(words found in the corpora). First E4B numbers (the grid's first 23 poems
against the whole baseline): chosen-token log-probability −0.84 free vs
−2.5 constrained; the model's first choice is overridden at 67–78% of yati
aksharas against 33–42% elsewhere; lexical rate 41% free vs 8–19% constrained
— metrically exact text that is much less often made of real words.

---

## 6. Tests

`meter_engine/tests/test_dec_*.py`, standard-library `unittest` like the
other suites.

| file | what it pins down |
|---|---|
| `test_dec_automaton` | per meter: annotated DFA ≡ `prosodic_automaton` (`language_equal`); annotations functional; yati / prāsa roles ≡ `parser.segment(...).yati_aksharas` on random lines; `units`, `trailer`, `padanta`, union options; state counts in `fixtures/expected_counts.yaml` |
| `test_dec_incremental` | probe B on a fixed 2,000-line sample (full corpus as a script); fuzzing with random concatenations of real vocabulary tokens; NFC across token boundaries; UTF-8 accumulation |
| `test_dec_orthography` | every corpus line accepted; a list of malformed sequences rejected; a bound on characters per akshara |
| `test_dec_enforcer` | **completeness**: every corpus poem whose *canonical* scansion `accepts_poem` accepts in its labelled meter (no pādānta, no vikalpa reading — the generation-time rules), fed through random re-chunkings and through the real tokenizer's segmentation when present, stays alive and ends `poem_complete`. **Soundness**: random-logit generation for every meter passes the verifier. Snapshots restore exactly |
| `test_dec_registers` | decoder tables ⊆ engine verdicts, exhaustively over consonant pairs × vowel classes × bindu; on corpus poems that pass prāsa / yati under `strict`, the registers never reject |
| `test_dec_strategies` | seeded determinism; backtracking restores state, output and cache length; hybrid samples from `V_acc` when non-empty; the stall and mass triggers fire on constructed cases |

---

## 7. Experiments (new register entries, same replication-spec format)

| # | experiment | question |
|---|---|---|
| EXP-35 | DAWG enforcer random-logit control, all meters | do gaṇa, then +prāsa, then +yati reach 100% with random logits? (EXP-12 protocol; probe D is its first run) |
| EXP-36 | three strategies × 37 meters on Gemma-4 E2B / E4B | validity, lexicality, repetition, s/poem per meter family |
| EXP-37 | head-to-head with IndicNeuroSym on dvipada | same model, prompts (the paper's T1–T3), seeds (42 + 7k), τ, top-p, token budget; `force_nl="on_accept"` for parity |
| EXP-38 | backtracking-trigger ablation | `|V|<3` vs valid mass vs stall, on a real model |
| EXP-39 | end-of-line policy | `on_accept` vs `must_end`: సీసము reachability; line-length distributions for dvipada / kandamu against the corpus |
| EXP-40 | meter-family decoding | "any vritta" via the union automaton: which meters does the model drift into? |

Order: EXP-35 before any model run (it isolates harness bugs, as EXP-12
did), EXP-36 on two meters as a smoke test, then the rest.

---

## 8. Phases

| phase | deliverable | gate |
|---|---|---|
| 0 | decisions in §10 recorded here | — |
| 1 | `automaton.py` + `test_dec_automaton` | language equality with `prosodic_automaton` for all 37 meters; roles ≡ `parser.segment` |
| 2 | `incremental.py`, `orthography.py` + tests | 0 prefix violations on the corpus; 100% of corpus lines pass the orthography filter |
| 3 | `enforcer.py` (gaṇa only) + `TokenIndex` + tests | completeness on every corpus poem whose canonical scansion is in its meter; EXP-35 gaṇa arm at 100% on all meters |
| 4 | `strategies.py`, `sources.RandomLogits`, CLI `control` | the three strategies reproduce probe D; no budget failures with the progress guard |
| 5 | `registers.py` (prāsa, yati) + tables + tests | tables ⊆ engines; EXP-35 at 100% on gaṇa + prāsa + yati for every meter that has them |
| 6 | `sources.HFModel`, CLI `generate`, `evaluate.py` | smoke test on Gemma-4-E2B: dvipada, kandamu, utpalamala × 3 strategies × 3 seeds, all verifier-valid |
| 7 | EXP-36 – EXP-39 + register entries | results written as `experiments/EXP-3x-*.md` |
| 8 | performance: token trie + char-level scanner, per-state mask cache (after a space the mask depends only on `q` and the registers), bitset masks on the device | ≤ 5 ms/mask median (prototype: 25–32 ms) |
| later | meter-family decoding (EXP-40); a "generate" tab in `webapp/`; LoRA adapters per meter family (paper §6); akshara-aligned tokenizer (EXP-25/26) | — |

Phases 1–5 need no GPU. Phase 6 onward needs the GPU; check `nvidia-smi`
first, since the GB10 is shared with the vLLM translategemma server.

---

## 9. Risks

| risk | why it matters | mitigation |
|---|---|---|
| degenerate or repetitive text under a hard mask | EXP-13: 16/16 valid lines with real-word rate 15.9%; the paper's `nati nUta nUta nUta…` | soft repetition penalties (EXP-14), hybrid, the valid-mass trigger, lexicality metrics always reported |
| the model can spell only 10.5% of akshara types as one token | EXP-11: syllables arrive in fragments, so words break | the enforcer is character-level and handles this for meter; quality is the model's problem (fine-tuning, EXP-25/26 tokenizer) |
| decoder–verifier drift if `scansion.py` changes | a silent parity break reproduces EXP-12's "sampler and validator bucketing differently" bug | the decoder calls `scansion.py` directly; `test_dec_incremental` and `test_dec_enforcer` run in the suite |
| prāsa / yati rules are richer than the tables | profiles, sandhi, readings, the weight rule | strict subset, property-tested; final verdict from the engines; per-constraint pass rates reported |
| mid-word line breaks | forcing ⏎ can split a word (Pothana's printing does the same) | allowed by the verifier; optional soft bias toward word-final line ends |
| ఁ only through byte fallback | classical orthography uses it heavily; it carries no weight | decision 7 |
| Python overhead | 25–32 ms per mask today | phase 8; the LM forward pass dominates for 2B+ models anyway |
| GPU contention | loading a model beside the vLLM server on unified memory | schedule model runs; phases 1–5 are CPU-only |

---

## 10. Decisions needed

1. **Package name and place**: `meter_engine/metrical_decoder/`?
2. **Models**: Gemma-4 E2B / E4B (cached locally) or also Gemma 3 1B and the
   paper's LoRA adapters (not local) for a like-for-like replication?
3. **Replication**: is EXP-37 against the IndicNeuroSym code itself needed?
   That requires its repository
   (`github.com/samvarankashyap/indicnuerosym`); otherwise we compare with the
   paper's tables only.
4. **Generation profile**: prāsa / yati tables for `strict` with
   `sandhi="off"` (recommended), or `relaxed`?
5. **End-of-line policy default**: `must_end` (recommended) or the paper's
   `on_accept`?
6. **Pādānta at generation time**: off (recommended: the output then does not
   depend on the licence).
7. **ఁ**: support byte-fallback tokens so the model can write it, or generate
   without it?
8. **Repeatable meters and సీసము**: one dvipada couplet by default? సీసము with
   its gīta trailer as one generation, or the సీసము alone?

---

## 11. Reproducing the probes

Prototype and probes (session scratchpad, to be folded into phases 1–4):
`incscan.py` (§5.2 rules), `dawg_enforcer.py`, `strategies.py`,
`probe_a_automata.py`, `probe_b_full.py`, `probe_c_vocab.py`,
`probe_d_random.py`. Run with `.venv/bin/python`; B uses 16 processes
(~2 min), D uses 18 (~15 min for all meters). A and C take seconds.

---

## 12. Findings of 2026-09-24 that changed the design

| finding | evidence | consequence |
|---|---|---|
| An empty thinking-channel prefill makes Gemma-4 E4B analyse the rules in English instead of writing the poem | first-step probability mass on meter-valid tokens 0.025–0.13 with the prefill (5 variants, 3 meters) vs **0.999** with the plain chat template; with the prefill the answer starts "The user wants me to compose…" | `HFCausalLM(prefill=None)` by default; the prompt stays "rules + topic", no prefill |
| DiffusionGemma is not a masked (absorbing) diffusion model | transformers `EntropyBoundSampler`: the canvas starts as uniform-random tokens, every position is re-predicted each step, the accepted set is recomputed from scratch and everything else re-randomised | the three strategies need a custom denoising loop that *freezes* a validated left prefix; see §13 |
| Liveness must be joint over gaṇa × orthography × prāsa × yati | random-logit control: (a) a 4-consonant cluster whose only live option was a pollu the orthography forbids; (b) a yati akshara written before its position was known (the position lags the text by the pending syllables); (c) a conjunct that would have saved yati but broke the gaṇa; (d) a short pūrva that could never become guru the way prāsa allows; (e) an ఁ before the prāsa akshara (ఖండాఖండ) | `split_word(cluster_can_grow=…)`; `registers.continuations` (keep / grow / die / pollu / split, each with weight strings and syllable descriptors); feasibility tested per class and weight string, through the engines |
| `prasa.evaluate` re-parses `prasa_rules.yaml` on every call unless given a ruleset | 274 of 278 s of a profiled run were YAML loading | the registers pass one cached ruleset |
| The yati engine reads word context even with sandhi `off` (lexical ubhaya triggers, blockers such as ద్విరుక్త ట) | `yati.readings._word_context`; over the corpus (Vemana + Bhagavatam, 21,874 yati pairs of the catalogued meters) context changes **46 verdicts (0.21%), all fail → pass** (UB-01 -ఇంచు 13, VY-09 10, UB-10 7, UB-19/12/17 4 each, VY-10 4); no blocker changed any verdict | pairs are judged without context while a line is written and re-verified whole, with context, when it ends: the decoder is at worst slightly *stricter* than the engines (it masks e.g. మురారి, నారాయణ at a yati position whose match needs the deity-name reading) and never looser |
| The paper's backtracking trigger fires on legitimately narrow states | with an exact mask, `|V| < 3` also means "only the right consonant fits" | kept for parity; every backtrack records its reason in the trace |
| Register masks took 27–70 s at yati steps | per-step replay of one ఆటవెలది: the wrapper keyed its caches on whole previous syllables and prefixes, and the engine's ప్రాసయతి fallback (`yati.line._prasa_yati`) re-parses `prasa_rules.yaml` (110 ms) on every call | coarse keys holding exactly what the engine reads — the previous syllable only through its bindu, drutam, ఁ and "is ఉ"; a pending vowel one per yati class plus ఋ; the fallback on normalised onsets with the ruleset parsed once. Checked against the engine: 2,082,600 vowel-class cases, 4,010 fallback cases, 26,112 live target verdicts, 0 mismatches. The same ఆటవెలది poem: **5.6 s**, mean mask 83 ms |
| The last line was never checked whole | it ends at EOS, not ⏎, and `poem_complete` looked at the gaṇas only | `Enforcer.line_complete` runs the whole-line check (both for ⏎ and for the last line) |
| సీసము's second yati group (gaṇa 5, gaṇa 7) has its own ప్రాసయతి | `yati.line._prasa_yati` compares aksharas P+1 and Y+1 of the group, not 2 and Y+1 | the fallback is generic in P |
| బహుయతి నియతి (YATI-SY-11) couples the caesuras of a group | random-logit control over the 37 meters (Gemma slice, 3 strategies × 2 seeds): 217/222 complete and engine-accepted, **0 enforcer/engine disagreements**, 5 dead ends — all in the meters with a group of 3+ aksharas (మానిని, కవిరాజవిరాజితము, మంగళమహశ్రీ): with a conjunct vaḷi (బ్రి) each target was checked alone, so వి at 7 (through బ) and ఝృ at 13 (through ర) both passed, and the group failed only at 19; YATI-RJ-25 is `deprecated`, so the switch fails under strict and relaxed alike | the registers track, per target, which constituents of the vaḷi serve the match (the engine's candidates) and require one common constituent, as `yati.line._bahuyati_consistent` does |
| A word ending in two dead consonants splits differently in the prāsa engine | a సృగ్ధర whose line 1 opened with వన్స్ (random logits, seed 70) dead-ended at line 2's first akshara: the prāsa engine takes న్స్ (ఫ్రెండ్స్ → డ్స్) as line 1's second akshara, the scanner one syllable వన్స్; 0 of 49,661 corpus lines end a word in two dead consonants | the orthography filter allows at most one dead consonant at a word end (`MAX_FINAL_POLLU`), and the scanner's options drop the endings it forbids (`split_word(long_pollu=False)`), so liveness stays exact |
| An all-laghu సీసము prefix fits two slots that place the yati differently | final control, సీసము masking-only seed 49: line 2 reached 30 laghus — a whole 'all' line (yati 1–9, 17–25) and six short of a 'laghu' line (1–11, 21–31); groups were checked only where the slots agreed, so neither slot's yati was ever enforced; and the 'laghu' slot was still offered although line 1 had fixed the poem to 'all' lines | liveness is a disjunction over the slots still possible (`slot_groups`), and the possible slots follow from the lines already written (`slots_for`); 15/15 సీసము poems then complete |
| A thread cannot overlap the mask with the forward pass | E4B, cold caches: 218 ms/token synchronous, 231 ms/token with the forward on a thread — both are Python holding the GIL (the model's kernel dispatch, the enforcer) | masks in worker processes (`parallel.ParallelMaskCache`, `--mask-workers`): identical masks, 1.96× faster alone (cold caches, 4 workers), and the parent waits without the GIL, so the forward pass runs meanwhile; on the grid 266 → ~175 ms/token (masking-only). Fresh workers and cleared caches per meter keep memory bounded (a worker reached 0.9 GB within one meter); workers die with the parent (`PR_SET_PDEATHSIG`) |
| Corpus completeness and soundness | two samples of corpus poems, cleaned to what the model's slice can write, each fed in 2 random chunkings: 40 per meter over 24 meters (423 poems), then 120 each of సీసము (half-lines rejoined), ఆటవెలది, తేటగీతి (360). **No poem the engines reject reaches `poem_complete`**; of the engine-accepted poems (149 + 179) all but 3 stay alive to the end, and those 3 need an ubhaya reading (-ఇంచు, మురారి, నారాయణ) | the known gap above; no other disagreement |

## 13. DiffusionGemma (next)

The model (transformers `DiffusionGemmaForBlockDiffusion`, 26B-A4B, canvas 256,
≤ 48 denoising steps, entropy-bounded sampler, linear temperature 0.8 → 0.4)
denoises a whole canvas in parallel and in any order. A prefix enforcer applies
through a custom loop: keep a validated left prefix of the canvas frozen (never
re-randomised); at each step, apply the enforcer's mask to the logits of the
first unfrozen position and freeze it, then continue left-to-right while the
entropy-bound criterion holds for the masked distributions; the rest of the
canvas is re-randomised as usual. The three strategies carry over: masking-only
freezes the masked sample; masking + backtracking unfreezes a suffix (which the
sampler's renoising does naturally); hybrid re-ranks the first position by line
completion. The trace records the same per-token probabilities. Any-order
constrained unmasking (a feasibility oracle over a canvas with holes) is a later
research step.

## 14. Results: Gemma-4 E4B, gaṇa + prāsa + yati enforced (2026-09-25)

Run `experiments/runs/2026-09-24_e4b_constrained/` (37 meters × T1–T3 × 5
seeds × 3 strategies = 1,665 poems; the baseline's prompts, seeds and config;
strict profile, yati sandhi off; 4 mask workers). Report: `report.md` there
(`python -m metrical_decoder report` over the baseline and this run).

| strategy | in meter (engines, strict) | tokens / poem | s / poem | chosen-token logp | model's first choice overridden | lexical rate | poems repeating a line |
|---|---|---|---|---|---|---|---|
| baseline (free) | 0 / 555 | 65 | 11.7 | −0.84 | – | 41% | 1% |
| masking-only | **555 / 555** | 107 | 21 | −2.18 | 31% | 17% | 20% |
| masking + backtracking | **555 / 555** | 161 | 35 | −2.29 | 35% | 20% | 22% |
| hybrid | **555 / 555** | 101 | 20 | −2.34 | 32% | 19% | 17% |

* **Exactness held on the model:** no dead end, and every poem is accepted by
  the engines — the design's guarantee, for all three strategies (plain
  masking included: an exact mask cannot lead into a dead end).
* **The token budget, not the method, first cost 80 poems.** With a budget of
  2 × aksharas + 16 (calibrated on random logits, 1.1–1.3 aksharas per token)
  80 poems stopped a median 94% of the way through: under the mask the model
  writes one character per token 72% of the time (pollu, virama, matra), most
  of all in విద్యున్మాల (all guru), సృగ్ధర, మహాసృగ్ధర, మానిని. The budget is now
  the most tokens any poem can take, (MAX_AKSHARA_CHARS + 1) × aksharas + lines
  (`strategies.token_budget`; ఉత్పలమాల 1,044), and the backtracking step limit
  (backtracks + 2) × budget. A larger budget cannot change a poem that finished
  (the cap only truncates), so only the 80 were rerun: all 80 reproduced their
  first trace exactly up to the old cut-off and completed (median 144 tokens,
  at most 293). The superseded rows are kept in `superseded_budget_*.jsonl`;
  4 of them had in fact been complete (a status off-by-one, fixed).
* **Where the constraint bites:** the model's first choice is overridden at
  50–54% of yati aksharas and 42–47% of prāsa aksharas, against 27–32%
  elsewhere; the chosen token's log-probability there is −3.3 to −3.8.
* **Metrically exact, rarely real words:** the median accepted poem has 14%
  of its words in the corpora; a fifth repeat a line, which satisfies prāsa
  trivially. The better poems come from backtracking (e.g. a మధ్యాక్కర with
  refrain తల్లి … దైవమై నిలిచెను గాన).

## 15. DiffusionGemma: integration (2026-09-25)

Package `metrical_decoder/diffusion/` — an independent decoding loop for the
diffusion model; the constraint side (enforcer, prāsa/yati registers, masks,
parallel mask workers, runner, evaluation, traces) is shared with the
autoregressive runs. CLI: `python -m metrical_decoder diffusion …`; launcher
`experiments/scripts/run_diffusion_constrained.sh`.

**Model.** The only complete DiffusionGemma checkpoint on this machine is
NVIDIA's NVFP4 build of `google/diffusiongemma-26B-A4B-it` (18.9 GB). Neither
`transformers` 5.15 (no Model Optimizer loader) nor the installed vLLM (no
DiffusionGemma) runs it, so `diffusion/loader.py` builds `transformers`' own
`DiffusionGemmaForBlockDiffusion` and fills it from the checkpoint:

| piece | evidence |
|---|---|
| NVFP4 format (E2M1 in the low nibble first, FP8 scale per 16 inputs, FP32 scale per tensor) | decoded experts vs the BF16 Gemma-4 26B-A4B experts DiffusionGemma was initialised from: cosine 0.92–0.97 (swapped nibbles 0.00, another expert 0.01–0.02), same spread |
| grouped expert arithmetic (`nvfp4.Nvfp4Experts`) | vs a per-expert loop over the same weights: relative difference 1.7e-3 (BF16 rounding) |
| every tensor filled | 987 dense tensors by name (parameters tied between encoder and decoder filled once; all 62 buffers present), 30 × 128 experts; loading raises on any gap |
| the model runs | its own `generate`: fluent English and Telugu |
| speed / memory | experts decoded per pass: 19 GB, ~4 s a pass; decoded once (`--resident`): 52 GB, **264 ms a pass** — the resident mode needs the translategemma server stopped |

**Canvas** (`diffusion/canvas.py`). A block of 256 positions: a frozen prefix of
committed tokens, pinned in the self-conditioning signal (one-hot), and the
model's draft after it, updated after every pass by the model's own
`EntropyBoundSampler` rule (keep the jointly confident samples, renoise the
rest). A first version renoised the whole open part every pass: its poems
were clearly worse (lexical rate on the same 9 poems rose from roughly E4B's
level to 33–81% with the draft kept).

**Prefill.** DiffusionGemma opens every reply with an empty thinking channel
(`<|channel>thought\n<channel|>`), even with thinking off. Without it in the
prompt the model puts probability 1.0 on `<|channel>` at the first position and
0.000 on meter-valid tokens; with it, 0.98–1.00 (కందము, ఉత్పలమాల, ఆటవెలది).
E4B is the opposite (0.999 without, English analysis with), so each model has
its measured setting.

**Loop** (`diffusion/decoding.py`), per pass, from the first open position:
forced line end; else the model's own proposals, left to right, while each is
allowed by the enforcer and the run stays jointly confident (the model's
entropy rule applied to the contiguous run); else the strategy decides the
position — masked draw, backtracking (unfreeze to a checkpoint: the positions
return to noise, the temperature rises), or hybrid re-ranking (and in hybrid a
proposal is kept only if it is among the preferred candidates). Temperature:
the model's schedule, 0.8 → 0.4 over 48 passes of a block. Every pass commits
at least one token or backtracks; the budget is `token_budget`, so no poem can
end unfinished. Random-logit control (`RandomCanvas`, CPU): every strategy
completes in meter across block boundaries, with prāsa and yati enforced.

**First observations** (కందము, ఉత్పలమాల, ఆటవెలది; T1, seed 42): all 9 poems
complete and engine-accepted; 16–68 s a poem; the model's own proposal is kept
for roughly a quarter to three quarters of the tokens. Long lines still end in
filler (… క క క క): the model wants to stop (its mass goes to end-of-text) while
the meter needs more aksharas — the mass-collapse failure seen in the E4B
traces too. The report's "1-akshara words" column tracks it.

**Trial 1 and the end-of-text fix** (37 meters × 3 strategies, T1, seed 42;
`experiments/runs/2026-09-25_diffusion_trial/`). 111/111 complete and accepted
by the engines, but half the words were single aksharas (48–61% by strategy;
real verse 4.0%, E4B 3–5%). The traces said why: of the tokens the constraint
had to choose, 52% were chosen where the model's first choice was `<eos>` (6% a
line break), the constraint's share rose from 39% of the tokens in line 1 to
84% in line 4, and at those choices the model's mass on allowed tokens had a
median of 0.000 at a median temperature of 0.40. Block diffusion plans where
its reply ends: it drafts a short free-verse reply, fills the rest of the block
with `<eos>` and keeps it (confidently), while the meter needs about twice the
length. Fix (`DiffusionGemmaCanvas(forbid_end=True)`, default; `--allow-end`
restores trial 1): end-of-text tokens are removed from the model's predictions
everywhere in the block before they reach its proposals, draft and
self-conditioning — the poem cannot end before the enforcer says so; the traces
keep the raw predictions. Trial 2 (`…_diffusion_trial_noeos/`): first poems
80% → 27% and 57% → 21% single-akshara words — but the words that replace the
filler are mostly not real words either; the constraint and the model's
vocabulary of fitting words are the limit, which fine-tuning addresses. The
full grid (`…_diffusion_constrained/`) runs with the fix; its T1/seed-42 cells
are trial 2's rows (identical code).

**Full grid and the dead-consonant word (2026-09-26).** The full grid
(1,665 poems, `…_diffusion_constrained/`; the machine crashed hard 40 s into
its first model load, cause unproven, and the relaunch loaded cleanly) ended
with 2 masking-only dead ends (ఇంద్రవజ్ర and శాలిని, T2, seed 63) — which an
exact mask should never produce. In both the model opened the last line with
``న్ `` — a dead consonant as a word of its own. The scanner reads it as an
akshara with neither consonant onset nor vowel, which became the line's vaḷi;
no akshara can meet it in yati. Liveness at a word boundary does not look at
yati aksharas not yet written, on the assumption that some akshara can always
match a vaḷi — true of every real vaḷi, not of this empty one; so the state
stayed "alive" until only a space was allowed, after which nothing was. The
strategies that backtrack escaped it. Evidence: 0 of 49,661 corpus lines has a
word of dead consonants alone; the generated poems had them (E4B 10 / 1,665,
DiffusionGemma 20). Fix: the orthography filter forbids a word of dead
consonants alone (a vowel flag in its state; ``న్`` may still open a conjunct),
and the registers' liveness drops the continuations that would end such a word
(`continuations(bare_pollu=False)`: no ``lone`` word-initial ``C్``, no
``die`` of a word's first syllable). Regression test from the dead-end poem;
67 tests, corpus checks included. `experiments/scripts/audit_rule_change.py`
replayed all 3,330 constrained poems of both grids through the fixed enforcer
and flagged each poem where an input of some decision could differ — a token
now forbidden (E4B 5), a different number of allowed tokens at some step (42 /
46), a poem no longer complete (1 / 2), or, in hybrid, an allowed token whose
line-end verdict the rule changed (372 / 375; conservative: the trace does not
keep the re-ranked shortlist). The 420 + 423 flagged poems were moved to
`superseded_vowel_*.jsonl` and generated again with the same prompts, seeds and
settings; the other 1,245 + 1,242 are what the fixed code produces.

## 16. Three models, same program (2026-09-26)

Each model: free baseline + the three strategies, 37 meters × T1–T3 × 5 seeds
(2,220 poems), the same prompts, gaṇa + prāsa + yati enforced (strict).
Runs: E4B `2026-09-24_e4b_baseline` + `…_e4b_constrained`; Gemma-4 26B-A4B in
BF16 `2026-09-26_g26b` (launcher `run_hf_grid.sh`, trial `…_g26b_trial`);
DiffusionGemma `2026-09-26_diffusion_baseline` + `…_diffusion_constrained`.
The diffusion baseline is free generation in the same loop (`decoding._Baseline`:
no mask, the model may end its reply, the enforcer watches). Figures are
token-weighted (`analysis.collect`); *real words* = share of words that have
≥ 2 aksharas and occur in the corpora. Constrained cells: masking only /
masking + backtracking / hybrid.

| | Gemma-4 E4B | Gemma-4 26B-A4B | DiffusionGemma 26B-A4B |
|---|---|---|---|
| free: in meter | 0 / 555 | 0 / 555 | 0 / 555 (1 with the gaṇas right) |
| free: chosen-token logp | −0.84 | −0.48 | −0.47 |
| free: real words | 41% | 41% | 36% |
| free: poems repeating a line | 0.7% | 10.8% | 2.5% |
| constrained: in meter | 555 / 555 each | 555 / 555 each | 555 / 555 each |
| constrained: chosen-token logp | −2.18 / −2.29 / −2.34 | −1.68 / −1.94 / −1.87 | −3.84 / −3.13 / −3.49 |
| constrained: first choice overridden | 31 / 35 / 32% | 22 / 28 / 23% | 47 / 36 / 47% |
| constrained: mass on allowed tokens | 0.67 / 0.63 / 0.66 | 0.77 / 0.71 / 0.76 | 0.49 / 0.61 / 0.50 |
| constrained: real words | 13 / 15 / 14% | 17 / 21 / 18% | 9 / 9 / 10% |
| constrained: single-akshara words (verse 4.0%) | 9.2 / 9.3 / 7.9% | 16.1 / 12.0 / 14.1% | 28.7 / 25.0 / 26.5% |
| constrained: poems repeating a line | 20 / 21 / 17% | 42 / 30 / 29% | 3.8 / 2.2 / 2.9% |

* **Exactness is model-independent:** 4,995 constrained poems (3 × 1,665), all
  complete and in meter, no dead end after the dead-consonant fix (§15). Free
  generation is never in meter for any model.
* **The larger autoregressive model fits the meter better** — fewer overrides,
  more mass on allowed tokens, more real words — and the gain holds on the poems
  that repeat no line (logp −2.00 to −2.08 against −2.41 to −2.55; overridden
  25–30% against 34–37%; real words 16–22% against 14–16%). It is largest at
  prāsa (overridden ~15% against ~50%, repeated-line poems excluded): 26B opens
  lines with matching syllables (తల్లి / మల్లి). But it repeats lines twice as
  often (even free: 10.8%) and pads with more single aksharas.
* **DiffusionGemma writes as fluently as 26B when free** (logp −0.47) but loses
  the most under the left-to-right constraint (−3.1 to −3.8): the frozen-prefix
  loop overrides the block it plans (§15); a constraint that works with the
  model's own order of commitment is the open problem.

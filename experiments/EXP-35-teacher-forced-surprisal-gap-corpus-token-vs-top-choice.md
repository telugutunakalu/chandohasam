# EXP-35 — Teacher-forced surprisal gap: corpus token vs the model's own top choice

| | |
|---|---|
| **Category** | C. Behavioural capability |
| **Origin** | chandohasam (G8 / NH26, NH21; G6b / NH18, formerly EXP-10); NH27 proposed here |
| **Depends on** | EXP-01 (akshara grid, yati and prāsa seats), EXP-08 (shares the NLL quantity), EXP-19 (free-running traces, for NH18) |
| **Status** | pipeline run fails gate 2 (missing `<bos>`); **replication done** (2026-09-29, 200 poems): gates 1–6 pass; NH21 supported; NH26 and NH27 not supported |
| **Cost** | minutes; one forward pass per text × condition, no generation |

## Question
Under teacher forcing on genuine padyams, how far is the corpus's actual next
token from the model's own best guess, and where in the metrical structure is
that distance concentrated?

## Why it matters
EXP-05 asks whether weight is *represented*, and EXP-19 asks what the model does
when it *writes*. This experiment asks what the model *expects* while it *reads*
real verse. The prefix is always the true text, so exposure bias is excluded by
construction; whatever gap remains is a mismatch between the model's prior and
the poem. Aligning each token to the metrical grid shows whether that mismatch
sits at metrically constrained seats (pāda starts, yati, prāsa) or is spread
evenly.

Named precedent: GLTR (Gehrmann, Strobelt & Rush, 2019), which records the
true token's probability, rank and the distribution's entropy under teacher
forcing. GLTR does not compute the probability ratio below, so cite it as the
precedent for the method, not as a source of the statistics.

## Definitions
For target token `x_j` with true prefix `x_<j` and vocabulary size `V`:

```
p_true(j)   = p(x_j | x_<j)
p_max(j)    = max_w p(w | x_<j)                 # the model's own argmax
s_true(j)   = -log p_true(j)                    # surprisal of the corpus token
s_model(j)  = -log p_max(j)                     # surprisal of the model's own pick
gap(j)      = s_true(j) - s_model(j) = log(p_max / p_true) >= 0    # the probability ratio
rank(j)     = 1 + #{w : p(w | x_<j) > p_true(j)}                  # 1 = argmax
pct(j)      = 1 - (rank(j) - 1) / V
H(j)        = -sum_w p(w | x_<j) log p(w | x_<j)                  # entropy of the whole distribution
top1(j)     = [argmax == x_j]                                     # gap = 0 exactly when top1 (up to ties)
```

`s_true` and `s_model` are **surprisals** (one token's self-information), not
entropy. Entropy is a property of the whole distribution (`H`). The mean of
`s_true` over a text is exactly that text's teacher-forced NLL (EXP-08).
`ratio_to_min` from the original design is dropped: it is numerically unstable
and adds nothing.

## Inputs
1. **Sample.** Metre-balanced, as in EXP-05: `form == "verse"`, non-empty
   `verse` and `bhavam`, metres with ≥ 25 such records, 25 drawn per metre with
   a fixed seed, then shuffled. On `dataset/bhagavatam.json` this gives 8
   metres and 200 poems (kandamu 2607, tetagiti 1051, aataveladi 715,
   mattebhavikriditamu 586, champakamala 490, utpalamala 471,
   shardulavikriditamu 289, mattakokila 41 eligible records). Record the drawn
   ids in the run record. To compare record-for-record with the pipeline run,
   reuse the ids in `pipeline/data/bhagavatam_balanced_sample.jsonl` rather
   than redrawing.
2. **Poem text.** Take the lines from
   `indic_meter_dawg.scansion.scan(record["verse"])` (`LineScansion.text`),
   which NFC-normalises and strips each line, and join them with `"\n"`. Score
   *this* string, not the raw corpus lines. Akshara offsets refer to the
   normalised text: on raw lines, 233 of 19,291 akshara spans (1.2%, 300-poem
   check) are misplaced because decomposed ై (U+0C46 U+0C56) is composed by
   NFC.
3. **Bhavam text.** NFC, stripped, truncated to the first 2,000 characters (as
   EXP-07/21). Some bhavams quote the verse (record `1-1-శా.` quotes all six of
   its epithets). Flag any bhavam that shares a ≥ 3-word n-gram with its poem,
   and report NH21 with and without those pairs.
4. **Model input.** `[<bos>] + tokenizer(text, add_special_tokens=False).input_ids`,
   with no chat template in the primary condition. **Prepend `<bos>`
   explicitly.** The Gemma-4-E2B-it tokenizer under transformers 5.15 does not
   add it: `tokenizer(text)` starts `[237897, 42665, …]`, while the
   gemma-3-1b-it tokenizer starts `[2, 237897, …]` (checked 2026-09-24).
   Gemma models are not meant to be run without `<bos>`.
5. **Model.** `google/gemma-4-E2B-it` (the pipeline's base model), weights in
   bf16. Logits are cast to float32 before `log_softmax`. Record the snapshot
   commit.

## Conditions

| condition | prefix | role |
|---|---|---|
| `bos` | `<bos>` | **primary**; every hypothesis test uses this condition |
| `nobos` | none; token 0 is unscored | diagnostic: reproduces the presumed pipeline setup |
| `chat` | chat template with a fixed user turn, the text scored as the model turn | optional: robustness check for an instruction-tuned model's native register |
| random weights | `<bos>`, same tokenizer, randomly initialised model | harness reference: measures the uniform floor instead of assuming it |

Poem and bhavam run under every condition, so NH21 and the prose controls are
always available.

## Methodology
1. **One forward pass per (text, condition).** With prefix length `P` and
   target length `T`, logits rows `P-1 … P+T-2` predict target tokens `0 … T-1`.
   Under `nobos` (`P = 0`), token 0 has no prediction and is recorded as null.
   Compute `log_softmax` in row chunks: `V = 262,144`, so one float32 row is
   1 MB and a 700-token bhavam is 0.7 GB per full-width tensor.
2. **Per scored token, record** the id, piece, character offsets (tokenizer
   offset mapping), `s_true`, `s_model`, `rank`, `H` and argmax id. `gap` and
   `pct` are derived from these.
3. **Per text, record the off-by-one diagnostic**
   `mean_j -log p(x_{j-1} | x_<j)`, the probability the model gives to the
   token it has just read. If the headline numbers match this value rather
   than the aligned one, logits and targets are shifted by one position.
4. **Per poem, record the akshara grid** from
   `chandohasam.analyze(lines, profile="relaxed")`. For every akshara: global
   start/end offsets, pāda, 1-based index in the pāda, pāda length in
   aksharas, weight (U/I), word index, a yati-seat flag and a prāsa-seat flag.
   - **Yati seat** = `YatiSeat.positions[1:]`. `positions[0]` is the vaḷi,
     which is always pāda-initial and would confound yati with pāda start.
   - **Prāsa seat** = akshara 2, and only when the unit's `PrasaReport` is
     applicable, so ఆటవెలది and తేటగీతి get no seat.
   - Also record the engine's identified metre and `matched`. Group by the
     corpus label; the engine result is a covariate.
5. **Persist the per-position arrays.** Write one JSONL row per (text,
   condition), not just the means. Alignment is derived from these rows at
   analysis time, so the rules below can change without rerunning the model.

## Alignment rules (token → metrical grid)
- **Anchor character**: the first non-whitespace character in the token's span.
  **Anchor akshara**: the akshara containing that character.
- **Kinds**:
  - `text`: the anchor lies in an akshara.
  - `newline`: the pāda break.
  - `punct`.
  - `byte_cont`: a byte-fallback continuation, recognised by having the same
    offsets as the previous token. ఁ, for example, is three tokens
    `<0xE0><0xB0><0x81>` sharing one character span. Only the first counts as
    `text`.
- **Token flags**:
  - `word_initial`: the anchor is at the start of a line or follows whitespace.
  - `pada_first`: the first `text` token of a pāda.
  - `mid_akshara`: the anchor is past its akshara's start (శ + ్రీ is split
    across two tokens).
- **Akshara-level values**: spread each token's `s_true` and `gap` uniformly
  over its non-space characters. An akshara's value is the sum over its
  characters. This stays robust to tokenisation, sums to the text total, and
  is defined for every akshara, including one that shares a token with its
  neighbour.
- **Prose**: `word_initial` as above. `sentence_first` is the first
  word-initial token of the text, or the first after `.` `?` `!` `।`.

## Aggregations
- **Figure 6, position-wise.** For each token index `j`: mean `s_true`,
  `s_model` and `gap` over the texts that reach `j`, with `n` alongside. Read
  only the region with `n ≥ 10`.
- **Figure 6b, poem-level.** One point per poem: mean `s_true` (x; equal to
  EXP-08's `nll_true`) against mean `s_model` (y). Report Pearson and Spearman
  correlations; poems are independent, so ordinary p-values are valid.
- **Figure 6c, metrical profile (new).** Akshara-level mean `s_true` and `gap`
  by relative position in the pāda (deciles of `(idx-1)/(n-1)`), by pāda
  (1–4), and by (metre, akshara index). This is the pāda-relative breakdown the
  pipeline run lacked.
- **GLTR tiers.** Share of true tokens at rank 1, 2–10, 11–100, 101–1000 and
  above 1000, for poem and bhavam.

## Tests
The unit of analysis is the **text**. Tokens within one text are not
independent, so no test pools tokens across texts as if they were.

- **NH26 (primary): the gap concentrates at pāda starts.** For each poem,
  `d_i = mean gap(pada_first) − mean gap(other word-initial text tokens)`.
  Comparing only word-initial tokens removes the generic word-start effect,
  since the first subword of any word is harder to predict. Run a Wilcoxon
  signed-rank test on `d_i` and a bootstrap 95% CI (10,000 resamples of
  poems).
  - **Prose control.** Compute the same statistic on the bhavam, with
    `sentence_first` in place of `pada_first`. The metrical excess is
    `Δ_i = d_i(poem) − d_i(bhavam)`, tested with a paired Wilcoxon.
  - NH26 needs both `d > 0` and `Δ > 0`. An effect of the same size at prose
    sentence starts is a boundary effect, not a metrical one.
- **NH21 (secondary): prose sits closer to the model's prior than verse.** For
  each pair, take the mean `gap` over matched token indices
  `j < min(T_poem, T_bhavam)` and run a paired Wilcoxon; poem > bhavam is
  predicted. Also report `pct` medians and quartiles per register.
- **NH27 (proposed here): the model anticipates the metre's own constraints.**
  Prāsa and yati are the only seats where the metre, not the language, makes an
  akshara partly determined by earlier text. If the model uses those
  constraints while reading, those seats should be *less* surprising than
  matched free seats.
  - **(a) Prāsa.** Prāsa-applicable metres only (6 of the 8, 150 poems), using
    akshara-level `s_true` `S(pāda, idx)`.
    `x_i = mean_{p ≥ 2} S(p, 2) − S(1, 2)` is the change at the prāsa seat once
    pāda 1 has fixed it. The control `y_i` is the same quantity at akshara 3,
    which is constrained in weight but not in consonant. The statistic is
    `did_i = x_i − y_i`; prediction: `did < 0`.
  - **Prāsa placebo.** The same `did_i` on ఆటవెలది and తేటగీతి, which have no
    prāsa, should be about 0.
  - **(b) Yati.** For each poem: mean `S` at word-initial yati-seat aksharas
    minus mean `S` at other word-initial aksharas inside the pāda, excluding
    pāda-first ones. Prediction: `< 0`.
  - Wilcoxon and bootstrap CI as above. A null result here, together with
    EXP-05's positive probe, is the "represented but not used" pattern the
    README flags for EXP-05 vs EXP-09.
- **NH18 (secondary, formerly EXP-10): teacher forcing vs free running.** This
  asks how much of the metrical failure is exposure bias. It needs no extra run.
  - **Teacher-forced satisfaction at slot k:** whether the akshara the model's
    argmax starts (this experiment's `argmax` field, from the true prefix)
    satisfies the template weight at slot `k+1`.
  - **Free-running satisfaction at slot k:** the same check on EXP-19's
    generations, `poem` field only.
  - **Comparison:** the per-slot rates and their gap as a function of slot
    index, pooled within metre.
  - **Weight resolution:** a candidate's weight can depend on the next akshara
    (a following conjunct makes it guru). Resolve it with the true following
    text under teacher forcing, or the model's next token when free running;
    otherwise count only self-determined weights (EXP-05 step 5).
  - **Expected:** free running is lower. For Gemma the question is already
    largely answered by EXP-09: it fails even when given the true context. A
    small gap here would confirm that exposure bias is not the main cause.

## Sanity gates
All six must pass before any result is interpreted.

| # | gate | pass condition | what a failure means |
|---|---|---|---|
| 1 | invariant | `s_model ≤ s_true + 1e-4` at every scored position | a scoring bug; `p_max` cannot be below `p_true` |
| 2 | **uniform bound** | mean `s_true` < `ln V` = ln 262,144 = **12.48** nats | the model does worse than a uniform guess, so the input is out of distribution (missing `<bos>`) or targets are misaligned; this says nothing about verse |
| 3 | prose control | mean `s_true`(bhavam) < mean `s_true`(poem) under `bos` | if modern prose is no easier than archaic verse, the pipeline, not the register, is setting the numbers |
| 4 | BOS / alignment | report `bos` vs `nobos`, and the off-by-one diagnostic vs the aligned mean | tells the bug class apart if gate 2 fails |
| 5 | random-weights reference | `s_true` ≈ ln V + σ²/2, entropy ≈ ln V − σ²/2 and `gap` ≈ σ·E[max of V standard normals], with σ = initializer_range·√hidden_size (for gemma-4-E2B-it: 12.78, 12.17 and 3.60 nats)¹ | an untrained model misses the floor, so the harness is broken (the EXP-12 logic) |
| 6 | NLL cross-check | per-poem mean `s_true` equals EXP-08's `nll_true` for the same poem and condition | the two experiments are not measuring the same thing |

¹ Amended 2026-09-29. The original condition was `s_true` ≈ 12.48 and `gap` ≈ 0,
an exactly uniform output. A randomly initialised model does not produce one:
the final RMSNorm gives the last hidden state norm √hidden_size, and the output
rows are drawn from N(0, initializer_range²), so the logits are approximately
N(0, σ²). The expected values above follow from that; the replication run
matches them to within 0.02 nats.

## Output record
- `run.json`: model id and snapshot commit, dtype, device, seed, sampled ids,
  conditions, transformers/torch versions, date.
- `traces.jsonl`: one row per (text, condition), keyed
  `"{id}|{poem|bhavam}|{condition}"`, and resumable on that key. Each row holds:
  - `id`, `metre`, `kind`, `condition`, `text`, `prefix_len`
  - `tokens`, `pieces`, `offsets`
  - `s_true`, `s_model`, `entropy`, `rank`, `argmax` (null where unscored)
  - `offby1_mean`
  - poems only: `engine_meter`, `matched`, and `aksharas` as
    `[start, end, pada, idx, n, weight, word, yati, prasa]`
- `summary.json`, holding the gates, the aggregations and the tests above.
- `fig6_positionwise.csv`, `fig6b_poemlevel.csv`, `fig6c_pada_profile.csv`.

## Expected result / baseline
- **Gates**: all pass. In particular, `s_true` stays well under 12.48 for both
  registers, and bhavam comes out below poem.
- **NH26**: `d > 0` and `Δ > 0`.
- **NH21**: the poem gap exceeds the bhavam gap at matched positions.
- **NH27**: `did < 0` for prāsa (the placebo about 0) and a negative yati
  contrast, if the model uses the constraints while reading. A null result is
  informative, not a failure.

## Observed
**Pipeline run, 2026-09-24** (`common/phase8_surprisal.py`, `scripts/run_phase8.py`):
`gemma-4-E2B-it`, 102 poems, poem side only. The run resumed from an
interrupted attempt that had checkpointed 102, so the extra poems were kept.

| quantity | value |
|---|---|
| invariant `s_model ≤ s_true` | 0 violations |
| cross-check vs Phase-1 `nll_true` | differences of 0.002–0.50 per poem |
| poem-level mean `s_true` | 13.15 (median 13.03) |
| poem-level mean `s_model` | 0.41 (median 0.42) |
| mean gap | 12.74 (median 12.62; min 9.83, max 15.66) |
| position-wise curves | `s_model` flat at ~0.1–0.8; `s_true` ~11–15 with no trend over positions 0–115 (`n ≥ 10`) |
| poem-level correlation | Pearson r = −0.290 (p = 0.003); Spearman r = −0.276 (p = 0.005) |
| NH26 | not confirmed by raw position; not broken down by pāda |

**This run fails gate 2 and should not be cited.** A mean `s_true` of 13.15 is
above `ln V` = 12.48:
- the geometric-mean probability of the true token is e^−13.15 ≈ 1.9×10⁻⁶,
  against 1/262,144 ≈ 3.8×10⁻⁶ for a uniform guess;
- meanwhile the model puts e^−0.41 ≈ 0.66 on its own argmax.

A model that is confidently wrong at every position, on every poem, is the
signature of a broken input, not of archaic vocabulary. The leading
explanation is a missing `<bos>`:
- the pipeline's Figure 1 methodology states "no chat template, no special
  tokens";
- this tokenizer does not add `<bos>` even when special tokens are allowed.

An off-by-one between logits and targets is the other candidate; gate 4
separates the two. The same `_nll()` path produced EXP-08's numbers, so they
inherit the problem (see EXP-08). The negative correlation and the "≈ 3×10⁵×
more probable" reading are therefore artifacts until this is rerun.

**Replication, sanity gates (2026-09-29).** `experiments/scripts/exp35_surprisal.py`,
`gemma-4-E2B-it` (snapshot `905e84b5`, bf16, transformers 5.17), seed 42. The
sample rule reproduces the eligible counts above exactly. The first 10 poems of
the shuffled 200-poem sample were scored with their bhavams, under three
conditions: 6,814 scored positions in all. The tokenizer still does not add
`<bos>` (`tokenizer(text)` starts `[237897, 42665, …]`).

| condition | text | mean `s_true` | mean `s_model` | mean gap | top-1 | off-by-one |
|---|---|---|---|---|---|---|
| `bos` | poem | **6.26** | 0.92 | 5.35 | 17.3% | 9.77 |
| `bos` | bhavam | **5.39** | 0.51 | 4.89 | 30.5% | 15.58 |
| `nobos` | poem | **13.21** | 0.50 | 12.72 | 9.3% | 12.58 |
| `nobos` | bhavam | 11.79 | 0.59 | 11.20 | 7.4% | 12.78 |
| random weights | poem | 12.78 | 9.16 | 3.62 | 0.0% | 10.42 |
| random weights | bhavam | 12.79 | 9.18 | 3.61 | 0.0% | 10.41 |

| gate | result |
|---|---|
| 1 invariant | **pass**: 0 violations in 6,814 positions |
| 2 uniform bound | **pass**: 6.26 (poem) and 5.39 (bhavam), against ln V = 12.48 |
| 3 prose control | **pass**: bhavam below poem in 10 of 10 pairs |
| 4 BOS / alignment | **pass**: under `bos` the aligned surprisal is far below the off-by-one value (6.26 vs 9.77; 5.39 vs 15.58), so targets are not shifted |
| 5 random weights | **pass** against the amended condition: 12.78 / 12.17 / 3.61 measured, 12.78 / 12.17 / 3.60 expected |
| 6 NLL cross-check | **pass** (added after the EXP-08 rerun, 2026-09-29): EXP-08's `NLL(genuine)` equals the mean `s_true` here for all 10 poems, under `bos` and `nobos` |

**The missing `<bos>` is confirmed as the cause of the pipeline result.**
Without `<bos>`, the poem side gives mean `s_true` 13.21, `s_model` 0.50 and gap
12.72. This reproduces the pipeline's 13.15, 0.41 and 12.74 on a different
sample. With `<bos>`, the same poems give 6.26, and gates 1–5 pass. The
pipeline's poem-side numbers, and EXP-08's, should be replaced by `bos` reruns.

The harness splits the model across devices to fit an 8 GB GPU. The per-layer
embedding table (4.7 GB) stays in CPU RAM and is passed to the model as
`per_layer_inputs`. As a smoke test, English text scores mean `s_true` 2.95
(top-1 71%), and greedy decoding completes "The capital of France is" with
"Paris.".

The akshara grid is not computed yet, and none of NH26, NH21, NH27 or NH18 has
been tested; the next step is the full 200-poem run.


**Replication, full run (2026-09-29).** `experiments/scripts/exp35_surprisal.py --n 200`
(scoring), then `experiments/scripts/exp35_tests.py` (akshara grid, alignment,
aggregations, tests); all 200 poems and bhavams, `bos` for every test.
- **Engine.** It identifies all 200 poems. 188 are `matched` under the relaxed
  profile, and 175 are identified as their corpus label.
- **Gates 1–6 pass.** Gate 6: EXP-08's `NLL(genuine)` equals the mean `s_true`
  here for all 200 poems under both conditions (largest difference 5×10⁻⁶).

| | poem | bhavam |
|---|---|---|
| mean `s_true` (`bos`) | **6.40** | **5.35** |
| mean `s_model` / gap | 0.92 / 5.48 | 0.49 / 4.86 |
| true token at rank 1 / rank > 1,000 | 16.3% / 6.9% | 32.3% / 3.3% |
| mean `s_true` (`nobos`) | 13.45 (pipeline: 13.15) | 11.80 |
| bhavam below poem (gate 3) | | 186 of 200 pairs |

| test | statistic (mean, 95% CI) | share in predicted direction | one-sided Wilcoxon p | verdict |
|---|---|---|---|---|
| NH26 `d` (pāda-first − other word-initial gap) | −0.31 (−0.57 to −0.06) | 40.5% | 0.99 | **not supported** (opposite sign) |
| NH26 Δ vs prose (sentence-first) | −3.59 (−4.11 to −3.10) | 15.5% | 1.00 | not supported |
| NH21 gap, poem − bhavam, matched indices | **+0.50 (0.39 to 0.61)** | 74.5% | **5×10⁻¹⁵** | **supported** |
| NH27a prāsa difference-in-differences (150 poems) | +0.39 (−1.10 to 1.90) | 48.7% | 0.69 | not supported |
| NH27a placebo, aataveladi + tetagiti (50) | −3.02 (−5.78 to −0.43); median −1.47 | — | two-sided 0.079 | not clean |
| NH27b yati seat − other word-initial aksharas (61 poems) | +1.05 (0.24 to 1.92) | 42.6% | 0.97 | **not supported** (opposite sign) |

- **NH26.** Pāda starts are *less* surprising than other word starts, not
  more. The first token after `<bos>` is unusually hard; left out, `d` becomes
  −2.20 (−2.53 to −1.88). This check is not in the spec.
- **NH21 holds.** Verse sits further from the model's prior than its own prose
  paraphrase. No bhavam in this sample shares a 3-word n-gram with its poem.
- **NH27 is not supported.**
  - Prāsa seats are not easier once pāda 1 has fixed them.
  - The placebo is not about 0, so this difference-in-differences has an offset
    of its own. The pāda-1 terms fall at akshara 2 and 3 right after `<bos>`,
    where tokens straddle aksharas.
  - Word-initial yati seats are *more* surprising than other word-initial
    aksharas. Only 128 of 750 yati seats (17%) start a word, because Pōtana
    puts most of them inside compounds, so this test rests on 61 poems.
- **Memorisation check.** Without the lowest decile by mean `s_true` (20
  poems), none of the NH26 or NH27 verdicts changes.
- **Figure 6b.** At poem level, mean `s_true` and mean `s_model` correlate
  *positively* (Pearson 0.250, p = 3.6×10⁻⁴; Spearman 0.284). The pipeline's
  negative correlation (−0.29) came from the broken input.
- **Tokens.** 4,228 poem tokens split an akshara (`mid_akshara`), and 1,468 are
  byte-fallback continuations.
- **NH18** (after the EXP-19 rerun; `experiments/exp19/2026-09-29_generation/nh18_by_slot.csv`).
  The measure is per-slot agreement with the template weight, over the 5
  fixed-pattern metres.
  - **Teacher-forced: 68.4%** (4,273 aksharas). The weight is that of the
    argmax token's first akshara, resolved inside the token or else from the
    true next akshara.
  - **Free-running: 51.0%** (6,152 aksharas of EXP-19's clean poems), about
    chance.
  - Free-running is lower in 69 of 93 slots (Wilcoxon over slots,
    p = 1.1×10⁻⁹).
  - Caveat: the two sides differ in context (Pōtana's text vs the model's own
    poem from a bhavam), so the 17-point gap bounds exposure bias from above
    rather than measuring it. Even with the true prefix, the argmax misses the
    template weight in about a third of slots.

## Replication notes
- **Order matters.** Run the gates first on 5–10 poems (`bos`, `nobos`, random
  weights), then the full sample.
- **Tokens are not the unit.** Byte-fallback continuations (ఁ) are near-certain
  and dilute token means, and tokens split aksharas. Report token-level values
  for comparability with NLL, and akshara-level values for every metrical
  claim.
- **Memorisation confound.** Pōtana's Bhāgavatam is widely published online,
  and famous padyams (the opening శ్రీకైవల్య…) may be memorised, giving
  abnormally low `s_true`. List the lowest-decile poems, and report NH26/NH27
  with and without them, with skandha as a covariate.
- **Register.** An instruction-tuned model scoring raw text is off its native
  register. If `chat` and `bos` disagree on the direction of any test, report
  both.
- **Ties.** `rank` counts strictly greater probabilities, so ties resolve in
  the true token's favour. Ties are rare in float32 but can occur after bf16
  logits.
- **A fine-tuned checkpoint** (METRICALARGS) would be the natural second model;
  none exists (see EXP-05).

## Artifacts
- Pipeline run (fails gate 2): `pipeline/data/phase8_surprisal_traces.jsonl`
  (chandohasam repo).
- Replication, sanity gates on 10 poems (2026-09-29): `experiments/exp35/2026-09-29_gates/`
  (`run.json`, `traces.jsonl`, `summary.json`); script `experiments/scripts/exp35_surprisal.py`.
- Replication, full run (2026-09-29): `experiments/exp35/2026-09-29_full/` (`traces.jsonl`, `summary.json`,
  `akshara_grid.jsonl`, `tests.json`, `fig6_*.csv`, `fig6_surprisal.png`); script `experiments/scripts/exp35_tests.py`.

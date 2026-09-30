# EXP-38 — Synthetic tight-contrast set for a metre-specific direction

| | |
|---|---|
| **Category** | G. Steering |
| **Origin** | chandohasam (G4b, §4.5 amendment) |
| **Depends on** | EXP-01, EXP-04 (validator), EXP-22 |
| **Status** | **done** (2026-09-29): no metre-specific direction; break and preserve directions are largely parallel |
| **Cost** | hours to build the pair set, minutes to extract |

## Question
Can we build pairs that hold content and register fixed and differ only in
metrical correctness, so that a diff-in-means direction isolates metre rather
than register?

## Why it matters
EXP-22's coarse contrast (poem vs its own bhavam) confounds metre with register.
Its coherence peaks at only 0.322, and EXP-07 shows register separates
perfectly by L7. The natural tight contrast (compliant vs non-compliant corpus
poems of the same metre) could not be computed: only 13 of the 200 sampled
poems are non-compliant, spread over 8 metres. Constructing the negatives is
the only way to get a metre-specific direction at useful sample sizes.

## Methodology
1. **Sources.** Validator-certified compliant poems (`matched = True`,
   EXP-04). Each metre's pool comes from the full corpus, not just the
   200-poem sample.
2. **Metre-breaking edits.** Make one minimal edit per variant, of one of two
   types:
   - replace one word with a same-meaning word of a different weight
     pattern (the teeka glosses in `teeka_pairs` are a candidate source of
     synonyms);
   - make a small word-order change that is legal in Telugu.
   Keep a variant only if the validator now rejects it on gaṇa/weight
   grounds.
3. **Matched control edits.** Make the same kind and size of edit, but choose
   the replacement so the metre is **preserved** (same weight pattern). Keep a
   variant only if the validator still accepts it.
4. **Content check.** Every variant must keep the original's meaning. Compare
   each against the source bhavam (for example, with the EXP-23 fidelity
   metric) and drop variants whose similarity falls outside the
   original's range.
5. **Directions.** For each layer `l`:
   ```
   d_break    = mean_i[h_l(original_i) − h_l(break_i)]
   d_preserve = mean_i[h_l(original_i) − h_l(preserve_i)]
   d_metre    = d_break − d_preserve
   ```
   Subtracting `d_preserve` removes the effect of "any edit at this position";
   what remains is metrical correctness.
6. **Coherence check.** Compute EXP-22's coherence check on the per-pair
   diffs, per layer.

## Inputs
- Compliant poems per metre, and the validator.
- A synonym source with weight patterns (teeka glosses plus the EXP-01
  scanner).
- Hidden states pooled as in EXP-22.

## Metrics
- Pair yield per metre (candidates tried → validator-confirmed breaks and
  preserves).
- Per-layer coherence of `d_break`, `d_preserve` and `d_metre`.
- Coherence compared with EXP-22's coarse contrast (0.322) and its
  chandas-vs-chandas contrast (0.5–0.65).

## Expected result / baseline
NH14: the tight contrast gives a more coherent and more metre-specific
direction than the coarse one. If `d_break` and `d_preserve` are nearly
parallel, the "metre" direction is really an edit direction.

## Observed
**Run, 2026-09-29.** `experiments/scripts/exp38_tight_contrast.py`
(`gemma-4-E2B-it`, `<bos>`, last-token states as in EXP-22).
- **Sources.** Bhāgavatam poems of the 8 balanced-sample metres that the
  engine accepts (relaxed profile, sandhi hypothesis).
- **Edits.**
  - Synonym: the verse word replaced by its single-word teeka gloss (10,581
    such glosses occur verbatim in the verses; 712 keep the weight pattern).
  - Swap: two adjacent words in one line exchanged.
- **Roles.** A break is a variant whose target metre is no longer among the
  DAWG's candidates. A preserve is a variant the engine still accepts. Each
  source poem contributes at most one triple, and at most 25 per metre and
  edit kind.

| | synonym | swap |
|---|---|---|
| triples (8 metres) | 171 | 190 |
| pass the content check | 169 | 188 |

- **Yield.** It was limited by the cap, except for mattakokila (4 synonym and
  15 swap triples, from 41 poems) and śārdūlavikrīḍitamu (17 synonym). Every
  metre yielded triples, including kandamu.
- **Content check.** IndicSBERT cosine with the bhavam, with no variant more
  than 0.05 below its source. The median drop is 0.003; 357 of 361 triples
  pass.

| | all 357 | synonym 169 | swap 188 |
|---|---|---|---|
| peak coherence, `d_break` (source − break) | 0.138 (L0) | 0.023 (L4) | 0.138 (L0) |
| peak coherence, `d_preserve` | 0.135 (L0) | 0.012 (L35) | 0.151 (L0) |
| peak coherence, `d_metre` (per triple: preserve − break) | **0.011** (L0); ≤ 0.002 at L1–L35 | 0.008 (L2) | 0.011 (L0) |
| sign-flip null for `d_metre`, 95th / 99th percentile | 0.034 / 0.059 | 0.005 / 0.008 | 0.035 / 0.057 |
| cos(`d_break`, `d_preserve`) over layers, median (range) | **0.72** (0.58–0.91) | 0.40 (0.04–0.82) | **0.74** (0.59–0.89) |

- **No metre-specific direction.** Across triples, the per-triple metre
  difference (preserve − break) has no consistent direction at any layer. Its
  coherence is at or below the sign-flip null everywhere, except a negligible
  0.008 in the synonym subset.
- **The break and preserve directions are largely parallel**, especially for
  swaps (median cosine 0.74). By the spec's own criterion, what the tight
  contrast isolates is "this text was edited", not metrical correctness.
- **NH14 is not supported.** The tight contrast is no more coherent than the
  coarse one (0.475, EXP-22) or the chandas pairs (max 0.158).
- **Consequence for EXP-23.** Together with EXP-22, no coherent metre
  direction is available to steer with.

## Replication notes
- **The metre-preserving control is the load-bearing part.** Without it, a
  coherent `d_break` could simply encode "this text was edited".
- **Change one word per variant.** Multi-word edits drift in content faster
  than they break metre.
- **Report the yield per metre.** Some metres, such as kandamu with its
  variable gaṇas, admit many weight-equivalent substitutions and will yield
  few breaks.

## Artifacts
- Run (2026-09-29): `experiments/exp38/2026-09-29_tight/` (`triples.jsonl`, `kept.jsonl`, `build.json`,
  `extract.json`, `summary.json`); script `experiments/scripts/exp38_tight_contrast.py`. The pooled
  activations (`pooled_*.npy`, 75 MB each) are not committed; `exp38_tight_contrast.py extract` rebuilds them

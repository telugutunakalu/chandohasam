# EXP-38 — Synthetic tight-contrast set for a metre-specific direction

| | |
|---|---|
| **Category** | G. Steering |
| **Origin** | chandohasam (G4b, §4.5 amendment) |
| **Depends on** | EXP-01, EXP-04 (validator), EXP-22 |
| **Status** | TBD |
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
Not yet run.

## Replication notes
- **The metre-preserving control is the load-bearing part.** Without it, a
  coherent `d_break` could simply encode "this text was edited".
- **Change one word per variant.** Multi-word edits drift in content faster
  than they break metre.
- **Report the yield per metre.** Some metres, such as kandamu with its
  variable gaṇas, admit many weight-equivalent substitutions and will yield
  few breaks.

## Artifacts
—

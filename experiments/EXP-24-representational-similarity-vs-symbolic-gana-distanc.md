# EXP-24 — Representational similarity vs symbolic gana distance

| | |
|---|---|
| **Category** | G. Steering |
| **Origin** | chandohasam (G4c / NH20) |
| **Depends on** | EXP-22 |
| **Status** | TBD |
| **Cost** | minutes |

## Question
Does the geometry of per-metre activation differences mirror the symbolic distance between metres?

## Why it matters
A strong test of genuinely metrical representation: if the model merely encoded 'poeticness', per-metre directions would cluster without reflecting gana structure.

## Methodology
1. Extract a centered diff-in-means vector per chandas.
2. Compute pairwise representational distances between them.
3. Compute symbolic Levenshtein distance between the metres' gana patterns.
4. Correlate the two, **partialling out a shared poem-vs-bhavam component**.

## Inputs
Per-metre paired activations; gana pattern strings; a balanced per-metre sample.

## Metrics
Correlation between representational and symbolic distance, before and after partialling.

## Expected result / baseline
NH20: correlation survives after the shared 'poeticness' component is removed.

## Observed
Not yet run.

## Replication notes
Needs a metre-balanced sample with enough examples per metre; with unequal counts the distances are dominated by sample size.

## Artifacts
—

# EXP-22 — Chandas direction extraction (diff-in-means / CAA)

| | |
|---|---|
| **Category** | G. Steering |
| **Origin** | chandohasam (G4 / NH13) |
| **Depends on** | EXP-07,21 |
| **Status** | TBD (base only) |
| **Cost** | minutes |

## Question
Is there a linear direction in activation space corresponding to metrical form?

## Why it matters
If one exists, metre becomes steerable at inference without retraining — a fundamentally different lever from logit constraints, because it could shift what the model *wants* to say rather than filtering what it may.

## Methodology
1. Build paired activations: poem versus its bhavam, matched for content.
2. Compute the centered difference in means per layer — the candidate direction.
3. Measure coherence as mean pairwise cosine agreement across examples, per layer.
4. **Control for a generic 'poeticness' direction**, which the pairing would otherwise recover instead of a chandas-specific one.

## Inputs
(poem, bhavam) pairs; per-layer pooled activations.

## Metrics
Per-layer direction coherence; agreement with the EXP-21 divergence layer.

## Expected result / baseline
NH13: peak coherence at the peak-divergence layer.

## Observed
Not yet run on a fine-tuned checkpoint (none exists). Base-model half pending.

## Replication notes
The poem-vs-bhavam contrast confounds metre with register; EXP-07 shows register is trivially separable by L7, so without a control this recovers register, not chandas.

## Artifacts
—

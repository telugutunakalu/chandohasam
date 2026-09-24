# EXP-06 — Embedding-table lookup control

| | |
|---|---|
| **Category** | B. Representation probes |
| **Origin** | chandohasam (G1b / NH22) |
| **Depends on** | EXP-05 |
| **Status** | TBD |
| **Cost** | minutes, no forward pass |

## Question
Is L0's guru/laghu decodability a learned representation, or a surface lookup?

## Why it matters
EXP-05 found peak decodability at layer 0 — before any contextualisation. If a probe on the raw embedding table does as well, the signal is orthographic lookup, not prosodic knowledge, and the apparent competence is illusory.

## Methodology
1. Take the raw input-embedding matrix, with zero transformer layers applied.
2. Train the same probe on embeddings of the same tokens, same folds.
3. Compare to the L0 hidden-state accuracy from EXP-05.

## Inputs
Embedding table; the EXP-05 token set and labels.

## Metrics
Probe accuracy on raw embeddings vs L0 hidden states.

## Expected result / baseline
NH22: comparable accuracy, supporting a surface-lookup account. Telugu orthography marks vowel length explicitly, so a token's identity largely determines its weight — a lookup is the null hypothesis and should be tested first.

## Observed
Not yet run.

## Replication notes
**Run this before interpreting any layer-0 probe result on any model.** For abugidas the lookup account is strong a priori.

## Artifacts
—

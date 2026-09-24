# EXP-08 — Metrical-order NLL contrast against shuffle and prose controls

| | |
|---|---|
| **Category** | B. Representation probes |
| **Origin** | chandohasam (G1c / NH23) |
| **Depends on** | EXP-07 |
| **Status** | TBD |
| **Cost** | minutes |

## Question
Does the model assign lower loss to genuine metrical word order than to reorderings of the same words?

## Why it matters
A direct test of implicit metrical sensitivity that needs no probe. If genuine order scores *worse* than shuffle, the model actively disprefers metrical arrangement — which would explain a great deal of downstream failure.

## Methodology
1. For each poem, build two controls with identical vocabulary: a random shuffle, and a natural-prose reordering.
2. Compute NLL of all three under teacher forcing.
3. Report deltas per example and aggregated.

## Inputs
Poems; a shuffle generator; a prose-reordering procedure.

## Metrics
NLL(genuine) − NLL(shuffle); NLL(genuine) − NLL(prose-order).

## Expected result / baseline
NH23: genuine metrical order scores **worse** than both controls. The prose control is the load-bearing one — beating only a random shuffle proves nothing beyond fluency.

## Observed
Not yet run.

## Replication notes
Include the prose-reordering control. Shuffle alone is too weak a baseline to support any conclusion.

## Artifacts
—

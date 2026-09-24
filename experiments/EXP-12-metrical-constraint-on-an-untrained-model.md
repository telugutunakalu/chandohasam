# EXP-12 — Metrical constraint on an untrained model

| | |
|---|---|
| **Category** | D. Constrained decoding |
| **Origin** | ours (E5) |
| **Depends on** | EXP-01,04 |
| **Status** | done |
| **Cost** | minutes, CPU |

## Question
Can sampling-time constraints alone guarantee metrical validity?

## Why it matters
Separates 'do the constraints hold?' from 'has the model learned the language?'. Using random weights removes the model as a variable entirely.

## Methodology
1. Instantiate a model with **random weights**.
2. Sample with and without the constraint; hold seeds fixed.
3. Score both arms with the validator.
4. The output is semantic nonsense in both arms — that is intended and is what isolates the question.

## Inputs
Random-weight model; constraint module; validator.

## Metrics
Gana, yati, prasa and fully-valid rates in each arm.

## Expected result / baseline
Unconstrained ≈ 0. Constrained should approach 100% if the constraint machinery is correct; anything less indicates a bug, not a model limitation.

## Observed
**0/20 → 20/20 fully valid.** Four bugs surfaced, each invisible without an independent verifier: missing successor coupling (gana 0/20); sampler and validator bucketing prasa differently (prasa 0/20); a top-k fallback overwriting already-committed positions; and slot tokens exporting codas rightward on render (yati/prasa 12/20).

## Replication notes
Run with random weights before any trained model. Every bug found here would otherwise be misattributed to the model.

## Artifacts
`padyam/prosody/constraints.py`, `scripts/demo_constrained_decoding.py`

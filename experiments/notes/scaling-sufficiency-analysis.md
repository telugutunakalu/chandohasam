# Scaling sufficiency analysis (formerly EXP-33)

| | |
|---|---|
| **Category** | J. Data |
| **Origin** | ours (E18) |
| **Depends on** | [throughput benchmark](training-throughput-benchmark.md), EXP-32 |
| **Status** | done |
| **Cost** | seconds |

## Question
How large a model does this corpus support?

## Why it matters
Prevents both over- and under-building. For diffusion LMs the data-repetition tolerance is far higher than for autoregressive models, so the usual intuition misleads.

## Methodology
1. Calibrate the compute-optimal law on a published reference point.
2. For each candidate size, compute the data required and the epochs that implies over the unique corpus.
3. Separately compute the **epoch tolerance** from the data-constrained law.
4. The largest supported model is where required epochs still fall below tolerated epochs.

## Inputs
Unique token count; published scaling coefficients; measured throughput from the [throughput benchmark](training-throughput-benchmark.md).

## Metrics
Data required, epochs required, epochs tolerated, wall-clock — per candidate size.

## Expected result / baseline
Tolerance falls with model size while requirement rises; they cross.

## Observed
70M unique tokens:

| model | data required | epochs required | epochs tolerated | GB10 time |
|---|---|---|---|---|
| 39M | 3.12B tok | 45 | **557** ✓ | 18.6 h |
| 111M | 8.88B tok | 127 | **313** ✓ | 53 h |
| 320M | 25.6B tok | 366 | **175** ✗ | 153 h |

Supports models up to ~150M parameters.

## Replication notes
The tolerance law is extrapolated below its fitted range — trust the ordering, treat magnitudes as indicative. State that when quoting the number.

## Artifacts
`docs/10-padyarchana.md`

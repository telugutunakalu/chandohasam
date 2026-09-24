# EXP-14 — Repetition penalties and priority-ordered constraint relaxation

| | |
|---|---|
| **Category** | D. Constrained decoding |
| **Origin** | ours (E7; E8 rejection sampling, formerly EXP-15) |
| **Depends on** | EXP-13 |
| **Status** | done |
| **Cost** | ~30 min |

## Question
Can the degeneracy of EXP-13 be fixed without weakening the metre?

## Why it matters
Establishes that constrained decoding can reach high lexical diversity, and that when constraints conflict the resolution order must be explicit rather than accidental.

## Methodology
1. Order the constraints by priority; on conflict drop the lowest first and **never** the primary one. Instrument how often each is relaxed.
2. Add three soft repetition penalties, subtracted from logits so they bias without making the metre unsatisfiable: same index in another line; within a local window in this line; proportional to frequency across the canvas.
3. Make the conflicting-constraint check one-directional where a two-way check can oscillate.
4. **Rejection sampling** (formerly EXP-15): generate up to N candidates per prompt and stop at the first the validator accepts. With an exact verifier this makes validity unconditional, so the informative number is **attempts to first acceptance**.

## Inputs
EXP-13 setup plus penalty weights; a per-prompt attempt budget.

## Metrics
Relaxation counts per constraint; real-word rate; distinct-akshara ratio; duplicate-line count; mean attempts to first acceptance.

## Expected result / baseline
The primary constraint should relax zero times. Diversity should recover to at least the unconstrained baseline.

## Observed
Primary (gana) relaxed **0 times**; yati 15–33; prasa 0. Diversity **15.9% → 70.0%**, above the unconstrained baseline of 62.2%. Duplicate lines 6 → 0. Real-word rate 15.9% → 41.5%.

Rejection sampling: **4/4 valid**, five generations for four valid padyams (attempts 1, 2, 1, 1).

## Replication notes
Instrument the relaxation counters — without them a fallback can silently discard the constraint you care about most, which is exactly what the first implementation did.

Track attempts-to-valid as a headline metric across models. It should fall toward 1.0 as a model internalises the constraint, and it separates "the sampler is doing the work" from "the model has learned it".

## Artifacts
`scripts/gemma_constrained.py::MeterLogitsProcessor`, `scripts/gemma_constrained.py --best-of N`

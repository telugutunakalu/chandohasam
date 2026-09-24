# EXP-15 — Rejection sampling against the deterministic verifier

| | |
|---|---|
| **Category** | D. Constrained decoding |
| **Origin** | ours (E8) |
| **Depends on** | EXP-14 |
| **Status** | done |
| **Cost** | minutes |

## Question
Can validity be made unconditional?

## Why it matters
With an exact verifier, resampling until acceptance guarantees correctness — nothing can be fooled into passing. It also yields attempts-to-valid, a cheap proxy for how much the model has internalised versus how much the sampler carries.

## Methodology
1. Generate up to N candidates, scoring each with the validator; stop at the first acceptance.
2. Record attempts used per prompt.
3. Report validity and mean attempts together.

## Inputs
EXP-14 setup; a per-prompt attempt budget.

## Metrics
Fully-valid rate; mean attempts to first acceptance.

## Expected result / baseline
Validity should reach 100% within a small budget. **Mean attempts is the more informative number** — it should fall toward 1.0 as a model internalises the constraint.

## Observed
**4/4 valid.** Five generations produced four valid padyams (attempts: 1, 2, 1, 1).

## Replication notes
Track attempts-to-valid as a headline metric across models; it separates 'the sampler is doing the work' from 'the model has learned it'.

## Artifacts
`scripts/gemma_constrained.py --best-of N`

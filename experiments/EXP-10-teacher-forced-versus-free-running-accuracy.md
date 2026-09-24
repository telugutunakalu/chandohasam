# EXP-10 — Teacher-forced versus free-running accuracy

| | |
|---|---|
| **Category** | C. Behavioural capability |
| **Origin** | chandohasam (G7 / NH18, NH21) |
| **Depends on** | EXP-09 |
| **Status** | TBD |
| **Cost** | minutes |

## Question
How much of metrical failure is exposure bias rather than absent knowledge?

## Why it matters
Separates 'does not know' from 'knows but drifts'. EXP-09 answers the first behaviourally; this quantifies the second, and the two together localise the failure.

## Methodology
1. Teacher-force the model through genuine padyams; record the rank and probability of the true next token at each position.
2. Free-run generation from the same prefixes; score outputs with the validator.
3. Compare accuracy at matched positions.
4. Repeat on prose (bhavam) as a register control.

## Inputs
Padyams and their bhavam; identical prefixes for both regimes.

## Metrics
Token rank percentile; ratio to max probability; accuracy gap at matched positions; poem-vs-prose delta.

## Expected result / baseline
NH18: free-running significantly below teacher-forced. NH21: the true token sits at a higher percentile in prose than in verse at matched positions.

## Observed
Not yet run. Related evidence from EXP-09: teacher-forced restoration succeeds at 97.9% for a trained realiser while free composition fails, which is the same gap in a different form.

## Replication notes
The prose control is what turns this from a generic exposure-bias result into a statement about metre specifically.

## Artifacts
—

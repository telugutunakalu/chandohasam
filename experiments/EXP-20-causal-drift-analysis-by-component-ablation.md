# EXP-20 — Causal drift analysis by component ablation

| | |
|---|---|
| **Category** | F. Generation mechanics |
| **Origin** | chandohasam (G6 / NH16–NH19) |
| **Depends on** | EXP-05,19 |
| **Status** | TBD |
| **Cost** | hours |

## Question
Is the probe-identified weight representation *causally* responsible for metrical compliance?

## Why it matters
EXP-05 establishes correlation. Ablation establishes dependence — the difference between a representation the model uses and one that merely exists.

## Methodology
1. Ablate the probe-identified guru/laghu-carrying component during generation.
2. Compare the resulting drift pattern to unmodified generation.
3. Characterise drift shape: smooth positional decay versus sharp trigger-localised drops.
4. Compare free-running against teacher-forced accuracy at matched positions.
5. Test targeted threshold-triggered steering against constant steering at matched compliance.

## Inputs
EXP-05 probe directions; a generation loop with intervention hooks; the validator.

## Metrics
Drift curve shape; compliance under ablation vs baseline; free vs teacher-forced gap; intervention magnitude at matched compliance.

## Expected result / baseline
NH16 sharp trigger-localised drops; NH17 ablation reproduces observed drift; NH18 free-running well below teacher-forced; NH19 targeted steering matches constant steering at lower magnitude.

## Observed
Not yet run.

## Replication notes
Gate on EXP-06 first. If L0 decodability is surface lookup, ablating it tests a lookup, not a prosodic representation, and the causal claim does not follow.

## Artifacts
—

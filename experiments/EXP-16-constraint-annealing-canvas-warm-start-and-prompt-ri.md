# EXP-16 — Constraint annealing, canvas warm-start, and prompt richness

| | |
|---|---|
| **Category** | D. Constrained decoding |
| **Origin** | ours (E9) |
| **Depends on** | EXP-14 |
| **Status** | done (negative) |
| **Cost** | ~2 h, 5 arms × 4 topics |

## Question
Do softer constraint schedules, better initialisation, or richer prompts improve meaning?

## Why it matters
These are the obvious interventions. Recording that all three fail — and how — prevents their being retried, and the failure pattern points at the real cause.

## Methodology
1. **Annealing:** grid-only → soft penalty ramp → hard mask, instead of hard from step 0.
2. **Warm-start:** seed the canvas with a free draft instead of random tokens.
3. **Prompt richness:** condition on per-line prose meanings instead of a one-word topic.
4. Run all arms on identical prompts and seeds; score metre and lexicality.

## Inputs
EXP-14 setup; free drafts; per-line meaning annotations.

## Metrics
Valid rate; real-word rate; attempts; for annealing, the realised phase counts.

## Expected result / baseline
Each is plausible. Measure rather than assume.

## Observed
All three failed.

| arm | valid | real-words |
|---|---|---|
| free | 0/4 | 62.9% |
| hard | 4/4 | 41.5% |
| annealing | 4/4 | 35.9% ✗ |
| warm-start | 4/4 | 30.1% ✗ |

The informative result is an **inversion**: richer prompts raised free generation (55.7% → 71.9%) and lowered every constrained arm. A vague prompt lets the model drift toward available syllables; a specific one makes it attempt words it cannot express.

## Replication notes
Assert that the anneal schedule actually fires — the first implementation read progress backwards (`cur_step` counts **down**, and adaptive stopping truncates the loop), so annealing was silently inert and identical to the hard arm.

## Artifacts
`scripts/gemma_constrained.py --arms ...`, `experiments/gemma_v4_arms_topicprompt.json`, `gemma_v5_arms_richprompt.json`

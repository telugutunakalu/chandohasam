# EXP-17 — Recursive context expansion across iterations

| | |
|---|---|
| **Category** | E. Iteration and alphabet |
| **Origin** | ours (E10) |
| **Depends on** | EXP-15 |
| **Status** | done (saturates) |
| **Cost** | ~1 h, 5 iterations × 4 topics |

## Question
Does accumulating prior attempts plus machine-checked feedback keep improving output?

## Why it matters
Tests whether the bottleneck is *information*. The model is given the meaning, every prior attempt, and an exact diagnosis of each failure. If it still does not improve, the limit is not knowledge.

## Methodology
1. Iteration 0: context = meaning only. Generate a free draft and a constrained poem.
2. Iteration k: context = meaning + all prior free drafts, each annotated with the validator's exact diagnosis.
3. Repeat for 5 iterations; iteration 0 doubles as the baseline.
4. Report **per-topic trajectories**, not only means — the mean can hide that topics peak at different iterations.

## Inputs
Meaning annotations; validator diagnoses; a constrained sampler.

## Metrics
Per-iteration real-word rate and validity, constrained and free; context length; per-topic trajectory; standard deviation across topics.

## Expected result / baseline
If feedback helps cumulatively, a monotone trend. If it is one-shot, a step at iteration 1 then noise.

## Observed
| iter | context | free real-words | free gana | free line len | constrained real-words |
|---|---|---|---|---|---|
| 0 | 280 tok | 73.7% | 0/16 | 14.6 | 32.3% |
| 1 | 551 tok | 70.5% | 0/16 | 15.2 | **40.8%** |
| 2–4 | → 1,215 tok | ~73% | **0/16** | 15.1–15.4 | 40.9 / 30.9 / 39.4 |

**Saturates at one draft.** Iterations 1–4 mean 38.0%, sd **10.3** — variance swamps any trend. Context grew 4.3× for nothing.

The free arm never improved: **0/16 gana at every iteration**, mean line length 14.6 → 15.4 against a target of 20, while being shown up to four annotated attempts.

## Replication notes
Report the cross-topic standard deviation. With four topics, a 10-point sd makes any apparent trend below ~15 points uninterpretable.

## Artifacts
`scripts/gemma_iterative.py`, `experiments/gemma_v7_iterative.json`

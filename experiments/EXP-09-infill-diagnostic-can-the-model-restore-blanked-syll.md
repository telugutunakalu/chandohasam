# EXP-09 — Infill diagnostic — can the model restore blanked syllables?

| | |
|---|---|
| **Category** | C. Behavioural capability |
| **Origin** | ours (E12) ★ |
| **Depends on** | EXP-01 |
| **Status** | done |
| **Cost** | ~10 min + model load |

## Question
Given an already-correct padyam with k% of its syllables blanked, can the model restore them?

## Why it matters
The easiest possible version of the task — no invention, no topic, no planning. If a model fails here, no prompting, constraint or decoding strategy will rescue it, and the cause is representational rather than a capacity limit. This is the single most diagnostic experiment in the set and should be run **first** on any new model.

## Methodology
1. Select padyams a validator certifies metrically perfect.
2. Blank a random k% of aksharas, marking each blank explicitly; state the required count in the prompt.
3. Ask the model to restore them.
4. **Check line-length preservation first.** If the output has the wrong number of aksharas, nothing is positionally comparable and no other metric is meaningful.
5. On aligned outputs, score restored positions for correct weight and exact recovery.
6. Compare against two baselines: syllables drawn uniformly from the corpus inventory, and from its frequency distribution.

## Inputs
Certified padyams; a corpus akshara inventory with frequencies.

## Metrics
Line-length preservation rate; weight accuracy at blanks; exact-recovery rate; both baselines.

## Expected result / baseline
A model that represents syllables should preserve length near 100% and beat the frequency baseline (~57%) substantially. Scores near baseline indicate the units are not perceived.

## Observed
**DiffusionGemma 26B:**

| blanked | length preserved | weight correct | freq baseline |
|---|---|---|---|
| 10% | **10.4%** | 60.0% (n=10) | 57.3% |
| 25% | **0.0%** | — (n=0) | 55.8% |
| 50% | **0.0%** | — (n=0) | 51.2% |

On the identical protocol, a 39M-parameter akshara-aligned realiser restores 96–99% of weights at every rate; see **EXP-26** for its table. A model ~600× smaller solves what the larger cannot attempt.

This also settles the teacher-forced vs free-running question (formerly EXP-10) for this model family: Gemma fails even when given the true context, so its metrical failure is not mainly exposure bias.

## Replication notes
Report the frequency baseline alongside — at ~57% it is high, and a naive reading of 60% as 'above chance' is wrong. Report n at each rate; when alignment fails, n collapses to zero and the weight column is vacuous.

## Artifacts
`scripts/gemma_infill.py`, `experiments/gemma_v9_infill.json`

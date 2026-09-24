# EXP-27 — Realise a padyam from a bag of words

| | |
|---|---|
| **Category** | H. Training |
| **Origin** | ours (E15) |
| **Depends on** | EXP-26 |
| **Status** | done (partial) |
| **Cost** | minutes |

## Question
Can the realiser compose from an empty canvas, not merely restore a partial one?

## Why it matters
Distinguishes infilling from composition. They share an objective but are different problems, and the gap between them measures what remains.

## Methodology
1. Prompt: a shuffled, partially-dropped bag of the target padyam's own words plus a metre marker.
2. Canvas: fully masked.
3. Run two content sources — held-out gold words (upper bound: the words demonstrably fit) and a planner model's draft words (the deployment case).
4. Score metre and lexicality.

## Inputs
Trained realiser; held-out padyams; planner drafts.

## Metrics
Fully-valid rate; real-word rate.

## Expected result / baseline
Lexicality should be high since the words are supplied. Metrical validity is the open question.

## Observed
| content source | valid | real-words |
|---|---|---|
| gold padyam words | 0/30 | 47.5% |
| planner draft words | 0/30 | **61.3%** |

Semantics work — 61.3% exceeds the 54% that seven rounds of inference-time work on a 26B model could not pass, and output visibly reuses prompt words. Metrical validity **0/30**: restoring a mostly-correct canvas and composing one are different problems, and 20 minutes on 4,900 unique padyams addresses only the first.

## Replication notes
Report both content sources. Gold-word input is an upper bound; planner-word input is the number that matters operationally.

## Artifacts
`scripts/eval_realiser.py`

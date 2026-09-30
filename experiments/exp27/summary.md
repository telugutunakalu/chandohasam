# EXP-27: realise a padyam from a bag of words — summary

Full specification: [`../EXP-27-realise-a-padyam-from-a-bag-of-words.md`](../EXP-27-realise-a-padyam-from-a-bag-of-words.md).
**Status:** done (partial).

## Question
Can the realiser (EXP-26) compose a padyam on an empty canvas, not merely restore a partial one?

## Method
- The prompt is a shuffled, partly dropped bag of the target padyam's own words plus a metre marker. The
  canvas starts fully masked.
- There are two content sources: the held-out gold words (an upper bound) and a planner model's draft
  words (the deployment case).

## Findings

| content source | valid | real words |
|---|---|---|
| gold padyam words | **0/30** | 47.5% |
| planner draft words | **0/30** | 61.3% (spec) |

- **The words come through, but the metre does not.** The output reuses prompt words, but no poem is
  metrically valid.
- Restoring a mostly correct canvas and composing one are different problems. Twenty minutes of
  training on about 4,900 padyams addresses only the first.

## Evidence
- [`../realiser_eval.log`](../realiser_eval.log), "TASK 2": the gold-words row (valid 0/30, real words
  47.5%) with sample outputs.
- The planner-words row is not in that log and is the spec's.
- The script (`scripts/eval_realiser.py`) is not in this repository.

# EXP-09: infill diagnostic (can the model restore blanked syllables?) — summary

Full specification: [`../EXP-09-infill-diagnostic-can-the-model-restore-blanked-syll.md`](../EXP-09-infill-diagnostic-can-the-model-restore-blanked-syll.md).
**Status:** done.

## Question
Given a correct padyam with k% of its aksharas blanked, can the model restore them? This is the easiest
form of the task: no topic, no planning, no invention.

## Method
- Model: DiffusionGemma 26B. The input is a certified padyam with k% of aksharas blanked and marked.
- First check: does each output line keep its length? If it does not, nothing is positionally comparable.
- On aligned lines, the restored positions are scored for correct weight, against a baseline that draws
  syllables from the corpus frequency distribution.

## Findings (48 lines per rate)

| blanked | lines keeping their length | weight correct at blanks | frequency baseline |
|---|---|---|---|
| 10% | **5 / 48 (10.4%)** | 6 / 10 (60.0%) | 57.3% |
| 25% | **0 / 48** | — (no aligned line) | 55.8% |
| 50% | **0 / 48** | — (no aligned line) | 51.2% |

- The model almost never keeps a line's length, so it cannot restore syllables in place. The 60% at
  10% rests on 10 blanks and is about the frequency baseline.
- On the same protocol, the 39M-parameter akshara-aligned realiser restores 96–99% of weights (EXP-26).
- Gemma fails even with the true context, so its metrical failure is not mainly exposure bias.

## Evidence
- [`../gemma_v9_infill.json`](../gemma_v9_infill.json): per rate, `lines`, `aligned`, `holes`, `w_ok` (weight
  correct), `exact`, and the baselines (`b_freq`, `b_uni` out of `b_holes`). The table above is computed
  from it.
- The script (`scripts/gemma_infill.py`) is not in this repository.

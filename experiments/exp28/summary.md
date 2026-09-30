# EXP-28: diffusion objective ablation (masked vs uniform vs continuous) — summary

Full specification: [`../EXP-28-diffusion-objective-ablation-masked-vs-uniform-vs-co.md`](../EXP-28-diffusion-objective-ablation-masked-vs-uniform-vs-co.md).
**Status:** done.

## Question
Which corruption process is best for this task at matched compute?

## Method
- Backbone (40.9M parameters), tokenizer, data, steps (3,000), batch and learning rate are held fixed.
  Only the corruption and the loss vary.
- Training losses are **not** compared, because they are not commensurable:
  - masked scores only the corrupted positions;
  - uniform scores all positions;
  - continuous is an embedding MSE.
- All three are scored on the EXP-09 infill task instead.

## Findings

| objective | weight@15% | exact@15% | weight@35% | exact@35% | weight@60% | exact@60% | minutes |
|---|---|---|---|---|---|---|---|
| masked | 79.8% | 16.7% | **71.1%** | 10.1% | 52.2% | 2.9% | 9.7 |
| uniform | **80.1%** | **21.5%** | 70.7% | **13.6%** | **57.1%** | **6.1%** | 10.5 |
| continuous | 61.9% | 0.6% | 46.7% | 1.1% | 17.9% | 0.8% | 22.2 |

- **The loss would have misled.** Uniform ends training at CE 2.41 and masked at 4.71, although uniform
  has the harder task.
- **Continuous is rejected.** Its loss rose early in training, and at 60% corruption its weight accuracy
  (17.9%) is far below the 57% chance baseline, at half the throughput.
- **Masked was selected** despite uniform's small edge, for architectural reasons. Uniform corruption has
  no mask symbol, so "which positions are still open" is undefined. The constraint, the anchor-ordered
  sampler and the infill benchmark all need it.
- Caveat: uniform gets about twice the supervised positions per step, and 3,000 steps measure early
  training only.

## Evidence
- [`../ablation.json`](../ablation.json): the table above (`ablation_continuous.json` repeats the
  continuous row).
- [`../ablate_masked.log`](../ablate_masked.log), [`../ablate_uniform.log`](../ablate_uniform.log) and
  [`../ablate_continuous.log`](../ablate_continuous.log): the training logs, with the losses quoted above.
- The code (`padyam/objectives.py`, `scripts/ablate.py`) is not in this repository.

# EXP-19: generation-time tracking — summary

Full specification and discussion: [`../EXP-19-generation-time-tracking.md`](../EXP-19-generation-time-tracking.md).

## Question
When the model writes a poem freely, what distinguishes the steps that break the metre from those
that keep it? Does drift build up smoothly with length, or does it happen at specific points?

## Setup
- Model: `google/gemma-4-E2B-it`, chat template. The prompt is the project's own rule-bearing prompt
  for the metre (`experiments/runs/2026-09-24_e4b_baseline/prompts.jsonl`), with the poem's bhavam in
  place of the topic.
- Sample: EXP-35's 200 poems. Output is plain text (the four pādas); the earlier run asked for JSON.
- Decoding: greedy (argmax), at most 1,000 tokens. Every step logs its entropy and its hidden
  state's cosine with EXP-22's coarse poem − bhavam direction.
- Step-level outcome: whether the written akshara has the template weight for its slot. This is
  measured for the 5 fixed-pattern metres, on poems with clean pādas.
- Regression: logistic, with cluster-robust standard errors by generation.

## Findings
- **Compliance: 0 of 200 poems are in any known metre**, and none is valid in its target metre under
  either profile. No generation is truncated (mean 70 tokens), and 172 of 200 have exactly 4 lines.
  The earlier JSON run also had 0 of 189.
- **Regression** (99 clean poems, 6,542 steps; within the template's length, 5,550 steps):

| predictor | all steps: coef (p) | within the template: coef (p) |
|---|---|---|
| absolute position | +0.03 (0.35) | −0.02 (0.37) |
| position in the pāda | **+1.24 (10⁻²⁴)** | +0.08 (0.024) |
| aksharas since the last word junction | −0.08 (0.011) | −0.03 (0.37) |
| next-token entropy | +0.01 (0.69) | +0.04 (0.19) |
| rare token (fewer than 10 occurrences in the tokenised Bhāgavatam verses) | +0.48 (1.7×10⁻⁴) | **+0.57 (1.8×10⁻⁷)** |

- Across all steps, position in the pāda dominates, but mostly by construction: aksharas beyond the
  template's length count as violations, and they come late in the line.
- Within the template, the violation rate is **50.8%**, about what chance gives. The only clear
  predictor is a rare token.
- **NH12 is not supported:** neither entropy nor distance from a sandhi junction predicts a violation.
- **Decay curve (NH16): no smooth decay, but sharp changes at pāda starts.**
  - The per-poem slope is +0.017 per 100 steps at L6 and −0.001 at L35.
  - At pāda-initial steps, the cosine drops by 0.049 at L6 (p = 10⁻³¹) and rises by 0.275 at L35
    (p = 10⁻³⁴).
  - Caveat: these steps follow a newline, so the effect cannot be separated from the token type.
  - At L35, the generation states point towards the prose side of the direction (cosine about −0.55).
- **NH18 (with EXP-35):** the argmax matches the template weight in 68.4% of slots under teacher forcing,
  against 51.0% in free running (6,152 aksharas); free running is lower in 69 of 93 slots.

## Files
- `2026-09-29_generation/`:
  - `generations.jsonl`: one row per poem, with the text and per-step statistics.
  - `validation.jsonl`: the engine's verdict per poem.
  - `summary.json`: the validator, the regression, the decay curve and NH18.
  - `decay_by_step.csv`, `nh18_by_slot.csv`, `fig_exp19.png`: the curves and the figure.
  - `run.json`: the run record.

## Reproduce
```bash
diffusion_pretraining/.venv/bin/python experiments/scripts/exp19_generate.py OUT_DIR
diffusion_pretraining/.venv/bin/python experiments/scripts/exp19_analyse.py OUT_DIR
python3 experiments/scripts/exp19_analyse.py --plot OUT_DIR
```
The analysis reads `../exp35/2026-09-29_full/` and `../exp24/2026-09-29_bos/` by default.

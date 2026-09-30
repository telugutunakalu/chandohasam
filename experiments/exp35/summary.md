# EXP-35: teacher-forced surprisal gap — summary

Full specification and discussion: [`../EXP-35-teacher-forced-surprisal-gap-corpus-token-vs-top-choice.md`](../EXP-35-teacher-forced-surprisal-gap-corpus-token-vs-top-choice.md).

## Question
The model reads real verse with the true prefix (teacher forcing). How far is the corpus token from
the model's own best guess, and is that distance larger at metrically constrained seats (pāda
starts, yati, prāsa)?

## Setup
- Model: `google/gemma-4-E2B-it` (bf16, snapshot `905e84b5`, transformers 5.17), on an 8 GB laptop GPU.
- Sample: 200 Bhāgavatam poems, 25 from each of the 8 metres with at least 25 usable records (seed 42).
  Each poem is scored with its prose meaning (bhavam).
- Input: `<bos>` + text, no chat template. The tokenizer does not add `<bos>` by itself, so it is
  added explicitly. `nobos` (no `<bos>`) and a randomly initialised model are run as diagnostics.
- Per token: surprisal of the true token (`s_true`), of the model's argmax (`s_model`), their gap,
  rank and entropy. Tokens are then aligned to the akshara grid of the metre engine.

## Findings
- **The earlier pipeline result came from a missing `<bos>`.** Without `<bos>`, mean `s_true` on the
  poems is 13.45 nats, above the uniform bound ln V = 12.48 (the pipeline reported 13.15). With `<bos>`
  it is 6.40. All six sanity gates pass with `<bos>`.
- **Verse is harder than its prose paraphrase.** Mean `s_true` is 6.40 for poems and 5.35 for bhavams;
  the bhavam is easier in 186 of 200 pairs. The true token is the model's first choice for 16.3% of
  poem tokens and 32.3% of bhavam tokens.

| hypothesis | statistic (mean, 95% CI) | one-sided p | verdict |
|---|---|---|---|
| NH21: the gap is larger for verse than for prose | poem − bhavam gap +0.50 (0.39 to 0.61) | 5×10⁻¹⁵ | **supported** |
| NH26: the gap concentrates at pāda starts | −0.31 (−0.57 to −0.06) | 0.99 | not supported (opposite sign) |
| NH27a: prāsa seats get easier once pāda 1 fixes them | +0.39 (−1.10 to 1.90) | 0.69 | not supported |
| NH27b: word-initial yati seats are easier | +1.05 (0.24 to 1.92), 61 poems | 0.97 | not supported (opposite sign) |
| NH18: teacher-forced vs free-running weight agreement | 68.4% vs 51.0% per slot | 1.1×10⁻⁹ (over 93 slots) | free running is lower |

- Pāda starts are *less* surprising than other word starts, not more. The model does not appear to
  use prāsa or yati to predict the next akshara while it reads.
- The prāsa placebo (metres without prāsa) is not near 0 (−3.02), so the prāsa test has an offset of
  its own. Only 128 of 750 yati seats start a word, so NH27b rests on 61 poems.
- Dropping the 20 least surprising poems (a memorisation check) changes no verdict.
- At the poem level, mean `s_true` and mean `s_model` correlate positively (Pearson 0.25). The
  pipeline's negative correlation (−0.29) came from the broken input.
- NH18 compares different contexts (Pōtana's text vs the model's own poem), so its 17-point gap is an
  upper bound on exposure bias. Even with the true prefix, the argmax misses the template weight in
  about a third of slots.

## Files
- `2026-09-29_gates/`: the gate run on 10 poems (`bos`, `nobos`, random weights): `run.json`,
  `traces.jsonl`, `summary.json`.
- `2026-09-29_full/`: the full 200-poem run.
  - `traces.jsonl`: one row per text × condition, with every per-token value.
  - `summary.json`: the gates.
  - `akshara_grid.jsonl`, `tests.json`: the alignment and the hypothesis tests.
  - `fig6_positionwise.csv`, `fig6b_poemlevel.csv`, `fig6c_pada_profile.csv`, `fig6_surprisal.png`: the figures.
- NH18's per-slot table is in `../exp19/2026-09-29_generation/nh18_by_slot.csv`.

## Reproduce
```bash
diffusion_pretraining/.venv/bin/python experiments/scripts/exp35_surprisal.py --n 200 OUT_DIR
diffusion_pretraining/.venv/bin/python experiments/scripts/exp35_tests.py OUT_DIR --exp08 experiments/exp08/2026-09-29_shuffle
python3 experiments/scripts/exp35_tests.py --plot OUT_DIR
```
Use `--n 10` for the gate run.

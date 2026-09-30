# EXP-08: metrical-order NLL contrast — summary

Full specification and discussion: [`../EXP-08-metrical-order-nll-contrast-against-shuffle-and-pros.md`](../EXP-08-metrical-order-nll-contrast-against-shuffle-and-pros.md).

## Question
Does the model give a lower loss (NLL) to a poem's genuine word order than to other orders of the
same words? The pipeline run had reported the opposite (the shuffle preferred in 144 of 200 poems),
but its input lacked `<bos>` (see EXP-35).

## Setup
- Model: `google/gemma-4-E2B-it`, with EXP-35's scorer and EXP-35's 200-poem sample (8 metres × 25, seed 42).
- NLL = mean surprisal per scored token. `<bos>` is the primary condition; `nobos` is a diagnostic.
- Shuffle: the poem's own words are permuted across the whole poem and put back into the lines, so
  each line keeps its word count. The word multiset is checked.
- Prose control: the model was asked to put each poem's words into natural prose order, and a reply
  counts only if it uses exactly the same words.

## Findings

| | with `<bos>` | without `<bos>` | pipeline |
|---|---|---|---|
| mean NLL, genuine / shuffle | 6.40 / 6.51 | 13.45 / 13.34 | — |
| mean NLL(genuine) − NLL(shuffle) | **−0.111** (95% CI −0.164 to −0.059) | +0.111 (−0.031 to +0.260) | +0.571 |
| shuffle preferred | **78 of 200** | 105 of 200 | 144 of 200 |
| Wilcoxon p | 2.6×10⁻⁴ | 0.25 | — |
| Pearson r, genuine vs shuffle NLL | 0.766 | 0.507 | 0.556 |

- **With a valid input, the model prefers the genuine order** in 122 of 200 poems. The effect is
  significant but small: 0.11 nats per token, about 1.7% of the mean NLL.
- **NH23 (the model disprefers metrical order) is not supported** by the shuffle contrast.
- **Shared difficulty dominates.** Genuine and shuffled NLL correlate at r = 0.77. The spread between
  poems (genuine NLL from 4.9 to 8.2) is much larger than the order effect.
- **The earlier "extremes versus middle" pattern is a sorting artefact.** The delta contains the
  genuine NLL, so sorting by genuine NLL builds in a correlation. Against the mean of the two NLLs,
  the delta has no trend (Spearman ρ = 0.007, p = 0.93).
- Per metre (25 poems each, descriptive), the genuine order is preferred most in tetagiti (−0.245)
  and kandamu (−0.204), and hardly at all in mattebhavikriditamu (−0.002) and mattakokila (+0.011).
- **The prose control could not be built with this model.** 0 of 200 replies were usable: 83 repeated
  the poem unchanged and 117 changed, dropped or added words. This control is still open and needs a
  stronger reorderer (a larger local model, or a rule-based reordering).
- Cross-check: NLL(genuine) equals EXP-35's mean `s_true` for the same poems (EXP-35 gate 6).

## Files
- `2026-09-29_shuffle/`: the shuffle contrast.
  - `run.json`, `summary.json`.
  - `traces.jsonl`: per-token values for each poem × order × condition.
  - `per_poem.csv`, `fig_shared_difficulty.png`: the per-poem deltas and the figure.
- `2026-09-29_prose/`: the attempted prose control: `reorderings.jsonl` (the model's replies), `run.json`,
  `summary.json`, `traces.jsonl`.

## Reproduce
```bash
diffusion_pretraining/.venv/bin/python experiments/scripts/exp08_order_contrast.py OUT_DIR
python3 experiments/scripts/exp08_order_contrast.py --plot OUT_DIR
diffusion_pretraining/.venv/bin/python experiments/scripts/exp08_prose_control.py PROSE_DIR --exp08 OUT_DIR
```

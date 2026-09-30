# EXP-22: chandas direction extraction (diff-in-means) — summary

Full specification and discussion: [`../EXP-22-chandas-direction-extraction-diff-in-means-caa.md`](../EXP-22-chandas-direction-extraction-diff-in-means-caa.md).

## Question
Is there a linear direction in the model's activations that corresponds to metrical form, and is any
metre-vs-metre direction coherent enough to steer with (EXP-23)?

## Setup
- Model: `google/gemma-4-E2B-it`, `<bos>` + text. EXP-35's 200-poem sample (8 metres × 25) and their bhavams.
- States: the last token's hidden state at all 36 hidden-state indices. L0 is the embedding output, and
  L35 is the final-norm output.
- Coarse contrast: poem − bhavam for each of the 200 pairs.
- Metre pairs: all 28 pairs of the 8 metres. Coherence is the mean pairwise cosine of
  `c_k = diff_a,k − diff_b,k` over a seeded random matching of the two metres' poems.
- A pair counts as usable only if its coherence reaches 0.322 (fixed before the run). The null comes
  from 560 random 25/25 splits.

## Findings

| | result |
|---|---|
| coarse (poem vs bhavam) | peak **0.475 at L35**; 0.411 at L6 |
| metre-vs-metre peaks | **all 28 below 0.322** (range 0.003–0.158, median 0.064) |
| null (random splits) | 95th percentile 0.068, 99th 0.128 |
| pairs above the null's 95th percentile | 13 of 28; the best is kandamu vs tetagiti, 0.158 at L1 |
| kandamu vs mattakokila, L8–L35 | 0.025–0.068 (the pipeline reported 0.5–0.65) |

- **No metre-vs-metre direction is coherent enough to steer.** Every pair is below the threshold.
- Most pair peaks sit at L0–L3 (17 of 28), where a last-token state is close to the embedding of that
  token. At L0, 106 of the 200 poem − bhavam differences are exactly zero, because both texts end in the
  same token. These early peaks cannot be read as metre.
- **The pipeline's 0.5–0.65 is not reproduced**, with or without `<bos>`. Without `<bos>` the coarse
  contrast does match the pipeline (0.310 at L4 vs 0.322). Two other plausible definitions also stay
  low (0.03–0.11 and 0.25–0.32), so the pipeline must have defined pair coherence differently.
- **Consequence:** EXP-23 (steering) has no coherent metre direction to use. EXP-38 tried a tighter
  contrast and also found none.

## Files
- `2026-09-29_pairs/`: the `<bos>` run.
  - `directions.npz`: the per-layer directions. EXP-19 uses the coarse one.
  - `coherence_by_layer.csv`, `summary.json`, `fig_coherence.png`: the coherence results.
  - `meta.json`, `run.json`: the sample and the run record.
- `2026-09-29_pairs_nobos/`: the same without `<bos>` (diagnostic).
- The pooled states (`pooled_poem.npy`, `pooled_bhavam.npy`, 42 MB each) are not in git. EXP-07 and
  EXP-24 read them; `extract` rebuilds them in about 30 seconds on the GPU.

## Reproduce
```bash
diffusion_pretraining/.venv/bin/python experiments/scripts/exp22_directions.py extract OUT_DIR   # GPU
diffusion_pretraining/.venv/bin/python experiments/scripts/exp22_directions.py analyse OUT_DIR   # CPU
python3 experiments/scripts/exp22_directions.py plot OUT_DIR
```
Add `--no-bos` to `extract` for the diagnostic.

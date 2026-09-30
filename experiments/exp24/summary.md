# EXP-24: representational similarity vs symbolic gaṇa distance — summary

Full specification and discussion: [`../EXP-24-representational-similarity-vs-symbolic-gana-distanc.md`](../EXP-24-representational-similarity-vs-symbolic-gana-distanc.md).

## Question
Does the geometry of the per-metre activation directions mirror the symbolic distance between the
metres' weight patterns (NH20)?

## Setup
- Input: EXP-22's last-token states (`gemma-4-E2B-it`, `<bos>`), 25 poems per metre, 8 metres.
- Per metre and layer: the mean poem − bhavam difference `d_c`. The activation distance between two
  metres is 1 − cos(`d_i`, `d_j`). It is compared with `D_struct`, the Levenshtein distance between the
  metres' canonical U/I strings, by Spearman r over the 28 metre pairs.
- Canonical string: the most common whole-poem pattern over all eligible corpus poems of the metre.
  - For the five vṛttas this covers 43–56% of poems.
  - For kandamu, aataveladi and tetagiti it covers only 0.10–0.35%.
  - A sensitivity variant therefore joins the most common pattern of each pāda position.
- Mantel test, one-sided, 999 permutations. "Centred" removes the mean direction across metres first.

## Findings

| layer | r, raw | p, raw | r, centred | p, centred |
|---|---|---|---|---|
| L0 | 0.217 | 0.149 | 0.160 | 0.190 |
| L8 | 0.630 | 0.006 | 0.728 | 0.002 |
| L10 (centred peak) | 0.601 | 0.006 | **0.745** | 0.001 |
| L16 (raw peak) | **0.773** | 0.002 | 0.677 | 0.007 |
| L33 | 0.609 | 0.008 | 0.578 | 0.007 |

- **NH20 holds, more strongly than in the pipeline run.** The raw correlation is significant at
  **34 of 36** layers (pipeline: 26), and the centred one at 33. L8 reproduces the pipeline's peak
  (0.630 / 0.728 against 0.617 / 0.702). L0, the embedding output, shows no relationship.
- **The pipeline's late-layer "centred collapse" does not replicate.** At L33 the centred r is 0.578,
  against the pipeline's 0.123. That pattern was probably caused by the missing `<bos>`.
- **Robust to the choice of canonical pattern.** With per-pāda patterns, 31 of 36 layers are
  significant both raw and centred.
- Reading with EXP-22: metres that are closer in weight pattern have more similar mean directions, but
  no single metre-vs-metre direction is consistent across poems. The structure is visible in the
  averages, not in a steerable direction.

## Files
- `2026-09-29_bos/summary.json`: canonical patterns, `D_struct`, and per-layer Mantel results for both
  variants, with the pipeline's numbers for comparison.

## Reproduce
Needs the pooled states of `../exp22/2026-09-29_pairs/` (rebuilt by `exp22_directions.py extract`).
```bash
diffusion_pretraining/.venv/bin/python experiments/scripts/exp24_rsa.py experiments/exp22/2026-09-29_pairs OUT_DIR
```

# EXP-07: poem-vs-bhavam register probe — summary

Full specification and discussion: [`../EXP-07-poem-vs-bhavam-register-probe.md`](../EXP-07-poem-vs-bhavam-register-probe.md).

## Question
Does the model linearly separate metrical verse from its prose paraphrase, and from which layer on?

## Setup
- Input: EXP-22's last-token states (`gemma-4-E2B-it`, `<bos>`) for EXP-35's 200 poems and their 200
  bhavams, so 400 examples per layer.
- Probe: logistic regression (scikit-learn 1.9) per layer, 5-fold cross-validation.
- Baselines: chance 0.5, and a probe on text length alone (0.565).

## Findings
- **L0 (embedding output): 0.588**, close to the length-only baseline. The last token is usually the
  same full stop in both registers.
- **L1: 0.978**, and every layer from L2 on is at 0.98 or above. The first layer at 1.000 is L24 (also
  L25, L26 and L32).
- **The conclusion holds with `<bos>`:** register (verse vs prose) is separable almost from the first
  decoder layer. The pipeline run without `<bos>` peaked at L7 with 1.000; the exact peak layer moved,
  but accuracy is at or above 0.98 from L2 on either way.
- This separation is a register signal, not a metre signal. EXP-22 and EXP-38 found no coherent
  direction for metre itself.

## Files
- `2026-09-29_bos/summary.json`: accuracy for each of the 36 layers, the peak and the baselines.

## Reproduce
Needs the pooled states of `../exp22/2026-09-29_pairs/` (rebuilt by `exp22_directions.py extract`).
```bash
<env with scikit-learn>/bin/python experiments/scripts/exp07_register_probe.py experiments/exp22/2026-09-29_pairs OUT_DIR
```

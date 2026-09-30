# EXP-07 — Poem-vs-bhavam register probe

| | |
|---|---|
| **Category** | B. Representation probes |
| **Origin** | chandohasam (G1) |
| **Depends on** | EXP-05 |
| **Status** | done (base model); **rerun with `<bos>`** (2026-09-29): conclusion holds |
| **Cost** | minutes |

## Question
Does the model linearly separate metrical verse from prose paraphrase?

## Why it matters
It establishes whether "poeticness" is represented at all, and at which depth.
That is a precondition for extracting a chandas direction (EXP-22), and a
confound to control for there.

## Methodology
1. **Pairs.** Take each of the 200 balanced-sample records that has a bhavam.
   The poem text is the joined pādas; the bhavam is truncated to 2,000
   characters.
2. **Pooled vectors.** Pool each text's hidden state at every layer with
   last-real-token pooling (attention-mask aware), labelled `poem` / `bhavam`.
   This gives 400 examples per layer.
3. **Probe.** Train one logistic-regression probe per layer with 5-fold
   stratified cross-validation, and report the mean fold accuracy against the
   layer index.

## Inputs
(poem, bhavam) pairs; pooled hidden states per layer.

## Metrics
- Per-layer binary accuracy, and the peak layer.
- A length-only baseline: the same probe on character or token length alone.

## Expected result / baseline
Separability well above chance, peaking in shallow-to-mid layers. Near-perfect
accuracy indicates that register is a surface property, not deep structure.

## Observed
The probe peaks at **L7 with accuracy 1.000** (400 examples per layer): register
is cleanly, almost trivially separable by the 7th decoder layer's output.


**Rerun with `<bos>` (2026-09-29).** `experiments/scripts/exp07_register_probe.py`,
on EXP-22's last-token states (200 poems + 200 bhavams, 400 examples per
layer); scikit-learn 1.9.
- L0 (embedding output): **0.588**, close to the length-only baseline of
  **0.565**. The last token is usually the same full stop in both registers.
- **L1: 0.978**; every layer from L2 on is at 0.98 or above. The first layer
  at **1.000** is L24 (also L25, L26 and L32).

Register is separable almost from the first decoder layer, so the conclusion
holds with `<bos>`. The exact peak layer moves (L7 before, L24 now), but
accuracy is at or above 0.98 from L2 on either way.

## Replication notes
- **Accuracy of 1.000 is a warning, not a triumph.** A 2,000-character bhavam
  against a roughly 150-character poem makes length alone a likely separator.
- **Report the length-only baseline, and a vocabulary-only baseline** (bag of
  tokens), before concluding anything representational.
- **Same `<bos>` caveat as EXP-05.** Pooled states from a forward pass without
  `<bos>` may be degraded.

## Artifacts
`pipeline/data/phase1_bhavam_probe.json` (chandohasam repo)
- Rerun with `<bos>` (2026-09-29): `experiments/exp07/2026-09-29_bos/summary.json`;
  script `experiments/scripts/exp07_register_probe.py`

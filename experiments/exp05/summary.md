# EXP-05: per-layer linear probe for guru/laghu — summary

Full specification and discussion: [`../EXP-05-per-layer-linear-probe-for-guru-laghu.md`](../EXP-05-per-layer-linear-probe-for-guru-laghu.md).

## Question
At which layer, if any, can syllable weight (guru/laghu) be read linearly from the hidden states?
Does any layer recover the part of weight that looking up the token alone cannot see?

## Setup
- Model: `google/gemma-4-E2B-it`, `<bos>` + one pāda per forward pass.
- Data: the first 10 poems of each metre in EXP-35's sample (80 poems, 320 pādas).
- Tokens: 6,102 tokens lie inside a single akshara and are kept. 839 span several aksharas and 231
  span none; both are left out.
- Labels: the scanner's weights, canonical reading (42.8% guru).
- Probe: logistic regression (scikit-learn 1.9) per layer, 5-fold cross-validation.
- Subsets:
  - *self-determined*: the akshara is heavy on its own (2,164 tokens);
  - *context-determined*: the weight depends on the next akshara (3,938 tokens).
- Lookup baselines:
  - A: weight from the akshara alone;
  - B: A plus whether the next akshara starts with a conjunct.

## Findings

| | all | self-determined | context-determined |
|---|---|---|---|
| baseline A (lookup) | **0.927** | 1.000 | **0.887** |
| baseline B (A + next akshara) | 0.994 | 1.000 | 0.991 |
| best probe, L0 (embeddings) | 0.777 | 0.648 | 0.847 |
| probe, L18 (lowest) | 0.655 | 0.619 | 0.675 |
| probe, L25 | 0.749 | 0.748 | 0.750 |

- **No layer beats the lookup baseline**, overall or on the context-determined subset. The best probe
  (0.847 at L0) is below that subset's own majority rate (0.887). A rule that also sees the next
  akshara reaches 0.991.
- The best layer is L0, the embedding output, so the strongest signal is token identity. Deeper layers
  are lower (0.655–0.771 for L1–L35).
- **Conclusion:** by the spec's criterion, weight is looked up, not computed from context. This
  matches the model's behavioural failure in EXP-09. EXP-20's condition for running (a layer that
  beats the lookup on context-determined weights) is not met.
- The pipeline run without `<bos>` had the same shape (best at L0, 0.796).

## Files
- `2026-09-29_probe/`:
  - `labels.jsonl`: one row per token, with its akshara, weight and subset.
  - `summary.json`: the baselines and the per-layer accuracies.
  - `run.json`: the run record.
- The hidden states (`states.npy`, 644 MB) are not in git; `extract` rebuilds them.

## Reproduce
```bash
diffusion_pretraining/.venv/bin/python experiments/scripts/exp05_probe.py extract OUT_DIR   # GPU
<env with scikit-learn>/bin/python experiments/scripts/exp05_probe.py probe OUT_DIR         # CPU
```

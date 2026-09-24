# EXP-05 — Per-layer linear probe for guru/laghu

| | |
|---|---|
| **Category** | B. Representation probes |
| **Origin** | chandohasam (G1 / NH11) |
| **Depends on** | EXP-01 |
| **Status** | done (base model) |
| **Cost** | minutes, 1 forward pass per example |

## Question
At which layer, if any, is syllable weight linearly decodable from hidden states?

## Why it matters
Meter is a property of syllable weight. If the model does not represent weight, no prompting or constraint can make it obey meter — it is the representational precondition for everything else.

## Methodology
1. Draw a **metre-balanced** sample (fixed N poems per metre; drop metres with too few examples rather than padding).
2. Forward-pass each poem with `output_hidden_states=True`; cache per-layer, per-position states.
3. Label each akshara position guru/laghu using the EXP-01 engine.
4. Train a cross-validated linear probe per layer; report accuracy vs layer index.

## Inputs
Balanced poem sample; hidden states at every layer; gold weight labels from EXP-01.

## Metrics
Probe accuracy per layer; the layer of peak decodability.

## Expected result / baseline
NH11 predicts weight is *not* decodable early and becomes so mid-network. A fine-tuned prosody checkpoint should show it earlier.

## Observed
**Contradicts NH11's framing.** On `google/gemma-4-E2B-it`, n=300 aksharas, 36 layers: **L0 is highest (0.796)**, accuracy dips through L6–L11 (~0.64–0.66) and partially recovers by L24–29 (~0.73–0.74), never regaining L0. Fine-tuned comparison not run (no checkpoint exists).

## Replication notes
Balanced sampling matters: a sequential prefix of a skandha-ordered corpus is metre-skewed and confounds metre with era. A peak at L0 demands the EXP-06 control before interpretation.

## Artifacts
`pipeline/data/phase1_guru_laghu_probe.json` (chandohasam repo)

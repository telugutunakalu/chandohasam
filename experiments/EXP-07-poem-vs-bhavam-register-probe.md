# EXP-07 — Poem-vs-bhavam register probe

| | |
|---|---|
| **Category** | B. Representation probes |
| **Origin** | chandohasam (G1) |
| **Depends on** | EXP-05 |
| **Status** | done (base model) |
| **Cost** | minutes |

## Question
Does the model linearly separate metrical verse from prose paraphrase?

## Why it matters
Establishes whether 'poeticness' is represented at all, and at which depth — a precondition for extracting a chandas direction (EXP-22) and a confound to control for there.

## Methodology
1. Pair each poem with its bhavam (prose gist of the same content).
2. Cache pooled hidden states per layer for both.
3. Train a per-layer binary probe; report accuracy vs layer.

## Inputs
(poem, bhavam) pairs; hidden states per layer.

## Metrics
Per-layer binary accuracy; peak layer.

## Expected result / baseline
Separability well above chance, peaking in shallow-to-mid layers. Near-perfect accuracy indicates register is a surface property, not deep structure.

## Observed
Peaks at **L7 with accuracy 1.000** (n=200 pairs) — register is cleanly, almost trivially separable by a shallow-mid layer.

## Replication notes
Accuracy of 1.000 is a warning, not a triumph: check that vocabulary or length alone does not separate the classes before concluding anything representational.

## Artifacts
chandohasam `pipeline/`

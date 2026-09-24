# EXP-29 — Training throughput benchmark

| | |
|---|---|
| **Category** | H. Training |
| **Origin** | ours (E21) |
| **Depends on** | — |
| **Status** | done |
| **Cost** | minutes |

## Question
What is the real tokens-per-second on this hardware, and what limits it?

## Why it matters
Every wall-clock estimate is (tokens needed)/(tokens per second). The denominator is the number people guess wrong, and guessing produces plans that are wrong by an order of magnitude.

## Methodology
1. Time full training steps (forward, backward, optimiser) at several model sizes and batch shapes.
2. Report effective TFLOP/s under 6ND accounting, not just tokens/s.
3. **Vary sequence length and batch shape.** If throughput is flat across all of them, the bottleneck is not attention.
4. Measure with and without compilation.

## Inputs
The training loop; several configurations.

## Metrics
Tokens/s; effective TFLOP/s; peak memory; projected wall-clock at target token counts.

## Expected result / baseline
Throughput should vary with batch shape. Flatness is diagnostic.

## Observed
| config | tokens/s | TFLOP/s | peak memory |
|---|---|---|---|
| 140M, uncompiled | 16,814 | 10.2 | 20.0 GiB |
| 140M, compiled | 32,850 | 19.8 | 14.7 GiB |
| 320M, compiled | **16,740** | **27.2** | 21.8 GiB |

Two findings. Compilation is worth **2×**. And throughput was flat across every batch shape until the vocabulary head was fixed: masked diffusion supervises only masked positions, so projecting the full sequence materialised a (B, T, V) logit tensor mostly discarded — 6.3 GB in fp32 at batch 16 × 2048. Projecting only masked positions is numerically identical and removed the cap.

## Replication notes
The flat-throughput signature is the tell. If tokens/s does not move with batch shape, look outside attention — usually the vocabulary projection or the loss.

## Artifacts
`scripts/bench_gb10.py`

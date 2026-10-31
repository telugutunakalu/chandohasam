# Step 2: training speed (2026-10-18)

finetune.py, the real loop: 128 examples per step (random E6 draws), micro-batches of ≤ 8,192 padded tokens cut by
dynamic programming (7.8% padding), bf16 autocast over fp32 weights, AdamW, EMA. Measured after
the first 10 steps (compilation).

| | tokens/s (real) | examples/s | peak memory | one epoch (2,350 steps) |
|---|---|---|---|---|
| torch.compile (each decoder layer) | **12,521** | 77.7 | 11.1 GB | **1.08 h** |
| eager | 8,879 | 54.6 | 13.7 GB | 1.53 h |

Pass (≤ 1.5 h per epoch): yes, with compile (the default). Compiled and eager runs give the same loss at the same
steps (4.8970 / 4.8970 at step 10), so batches are deterministic and compilation changes nothing numerically.
Micro-batches of 16,384 tokens were no faster. Resume checked (step 30 → 45, the other slot).

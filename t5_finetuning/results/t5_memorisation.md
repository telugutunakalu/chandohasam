# Memorisation of the T5Gemma 2 E6 val poems (2026-10-23; the 270M constrained and the 4B runs added 2026-10-31)

../diffusion_finetuning/memorisation.py --train-records data/e6/records/train.jsonl (365,679 training poems): the share of poems whose longest akshara run shared with any one training poem reaches N; verbatim lines (refrain = a line in ≥ 5 training poems). For comparison (same script): MDLM 523M free 79.8 / 7.9 / 0.0 at N = 6 / 8 / 12, constrained 61.4 / 0.9 / 0.0.

## e6_t5g_270m_val

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 63.2 | 4.4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## e6_t5g_1b_val

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 67.5 | 6.1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## e6_t5g_1b_val_c

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 114 | 65.8 | 5.3 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## e6_t5g_1b_val_c_v2

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 114 | 61.4 | 3.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## e6_t5g_270m_val_c

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 114 | 57.9 | 1.8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## e6_t5g_4b_val

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 67.5 | 0.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## e6_t5g_4b_48k_val

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 59.6 | 1.8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

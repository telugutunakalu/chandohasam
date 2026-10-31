# Memorisation of the DiffusionGemma E6 val poems (2026-10-31)

../diffusion_finetuning/memorisation.py --train-records data/e6/records/train.jsonl (the E6 training poems): the share of poems whose longest akshara run shared with any one training poem reaches N; verbatim lines (refrain = a line in ≥ 5 training poems). The one free poem at ≥ 12 in every run, the base model's included, answers the same prompt (dataset/bhagavatam:1-89-ఉ.): the base never saw the training poems, so the shared run comes from the prompt, not from fine-tuning.

## base, free (`e6_dg_base_val_free`)

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 98.2 | 22.8 | 0.9 | 0.0 | 0.0 | 0.0 | 0.1 | 0.0 | 0.0 |

## 24k, free (`e6_dg_24k_val_free`)

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 67.5 | 7.9 | 0.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## 48k, free (`e6_dg_48k_val_free`)

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 67.5 | 6.1 | 0.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## whole pool, free (`e6_dg_full_val_free`)

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 74.6 | 6.1 | 0.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## base, constrained (`e6_dg_base_val_constrained`)

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 114 | 9.6 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## 48k, constrained (`e6_dg_48k_val_constrained`)

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 114 | 15.8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

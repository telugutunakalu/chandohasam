# Memorisation: `e3_e2_pretrained_10ep`

Shares of poems whose longest akshara run shared with a training poem reaches N; verbatim lines: refrain = a line found in ≥ 5 training poems.

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 555 | 86.7 | 6.7 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| masking_only | 555 | 34.2 | 2.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| masking_backtrack | 555 | 38.0 | 4.3 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| hybrid | 555 | 31.5 | 3.4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

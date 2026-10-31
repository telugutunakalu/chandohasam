# Memorisation: `e3_e5_tagged_10ep`

Shares of poems whose longest akshara run shared with a training poem reaches N; verbatim lines: refrain = a line found in ≥ 5 training poems.

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 555 | 80.4 | 11.5 | 0.4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.1 | 0.4 |
| masking_only | 555 | 38.2 | 4.7 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| masking_backtrack | 555 | 44.3 | 4.3 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| hybrid | 555 | 38.6 | 2.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

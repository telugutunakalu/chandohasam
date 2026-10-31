# Memorisation: `e6_523m_t1_val`

Shares of poems whose longest akshara run shared with a training poem reaches N; verbatim lines: refrain = a line found in ≥ 5 training poems.

| strategy | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | run ≥ 16 | run ≥ 24 | run ≥ 32 | refrain lines % | other verbatim lines % | poems copying an ordinary line % |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 79.8 | 7.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| masking_only | 114 | 57.9 | 1.8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| masking_backtrack | 114 | 61.4 | 0.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| hybrid | 114 | 54.4 | 1.8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

# Token choices under the constraint

Runs: `e6_523m_t1_val`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 0 | 0 | 90 | -0.955 | 76 | 6 | 0.932 | 1.851 | 58 | 9 | 0 | 0.0 |
| masking_only | 114 | 100 | 100 | 108 | -2.335 | 56 | 24 | 0.738 | 2.445 | 50 | 19 | 0 | 0.0 |
| masking_backtrack | 114 | 100 | 100 | 116 | -1.524 | 64 | 12 | 0.855 | 2.050 | 56 | 11 | 0 | 11.1 |
| hybrid | 114 | 100 | 100 | 103 | -2.315 | 55 | 23 | 0.753 | 2.456 | 46 | 12 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 188 | -1.303 | 45 | 0 | 0.989 |
| baseline | prasa | 131 | -0.850 | 87 | 1 | 0.967 |
| baseline | yati | 32 | -1.273 | 62 | 0 | 0.843 |
| baseline | other | 1464 | -0.918 | 78 | 1 | 0.975 |
| masking_only | line_start | 524 | -1.838 | 56 | 6 | 0.902 |
| masking_only | prasa | 493 | -1.222 | 76 | 12 | 0.815 |
| masking_only | yati | 1077 | -4.578 | 32 | 58 | 0.386 |
| masking_only | other | 10194 | -2.177 | 58 | 22 | 0.763 |
| masking_backtrack | line_start | 516 | -1.577 | 57 | 3 | 0.952 |
| masking_backtrack | prasa | 499 | -1.001 | 79 | 10 | 0.859 |
| masking_backtrack | yati | 1291 | -2.375 | 52 | 31 | 0.592 |
| masking_backtrack | other | 10967 | -1.445 | 65 | 10 | 0.881 |
| hybrid | line_start | 508 | -1.802 | 59 | 6 | 0.918 |
| hybrid | prasa | 484 | -1.326 | 74 | 15 | 0.797 |
| hybrid | yati | 1090 | -4.623 | 30 | 58 | 0.380 |
| hybrid | other | 9625 | -2.130 | 57 | 20 | 0.784 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 0 / -0.88 / 73 | 100 / -1.44 / 69 | 100 / -1.20 / 75 | 100 / -1.41 / 64 |
| bhujangaprayatamu | 0 / -0.81 / 44 | 100 / -3.87 / 33 | 100 / -3.41 / 11 | 100 / -3.56 / 32 |
| champakamala | 0 / -0.91 / 61 | 100 / -2.09 / 53 | 100 / -1.36 / 57 | 100 / -2.22 / 49 |
| kandamu | 0 / -0.93 / 59 | 100 / -1.95 / 57 | 100 / -1.56 / 62 | 100 / -1.72 / 52 |
| malini | 0 / -0.93 / 41 | 100 / -3.43 / 15 | 100 / -1.64 / 19 | 100 / -2.96 / 26 |
| mattakokilamu | 0 / -0.98 / 67 | 100 / -2.42 / 52 | 100 / -1.35 / 65 | 100 / -2.49 / 46 |
| mattebhavikriditamu | 0 / -1.03 / 53 | 100 / -3.08 / 34 | 100 / -1.67 / 42 | 100 / -2.88 / 35 |
| sardulavikriditamu | 0 / -1.09 / 48 | 100 / -2.67 / 39 | 100 / -1.64 / 46 | 100 / -2.92 / 32 |
| seesamu | 0 / -0.97 / 59 | 100 / -2.11 / 57 | 100 / -1.98 / 61 | 100 / -2.40 / 56 |
| tetagiti | 0 / -0.89 / 57 | 100 / -1.90 / 63 | 100 / -1.97 / 62 | 100 / -1.80 / 53 |
| utpalamala | 0 / -0.88 / 57 | 100 / -2.00 / 50 | 100 / -1.18 / 56 | 100 / -1.98 / 48 |

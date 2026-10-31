# Token choices under the constraint

Runs: `e6_nandi_s4000_val`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 4 | 4 | 75 | -1.043 | 75 | 5 | 0.939 | 1.940 | 47 | 7 | 0 | 0.0 |
| masking_only | 114 | 100 | 100 | 76 | -1.615 | 68 | 10 | 0.891 | 2.078 | 47 | 9 | 0 | 0.0 |
| masking_backtrack | 114 | 100 | 100 | 91 | -1.379 | 68 | 8 | 0.913 | 2.034 | 47 | 8 | 0 | 6.6 |
| hybrid | 114 | 100 | 100 | 72 | -1.726 | 64 | 9 | 0.901 | 2.149 | 46 | 8 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 212 | -1.040 | 60 | 0 | 0.989 |
| baseline | prasa | 150 | -0.935 | 81 | 0 | 0.978 |
| baseline | yati | 82 | -0.972 | 83 | 1 | 0.933 |
| baseline | other | 1784 | -1.118 | 74 | 1 | 0.976 |
| masking_only | line_start | 390 | -1.253 | 68 | 3 | 0.963 |
| masking_only | prasa | 409 | -1.050 | 80 | 6 | 0.913 |
| masking_only | yati | 632 | -4.079 | 46 | 41 | 0.555 |
| masking_only | other | 7271 | -1.452 | 69 | 8 | 0.915 |
| masking_backtrack | line_start | 403 | -1.191 | 67 | 1 | 0.975 |
| masking_backtrack | prasa | 407 | -0.911 | 80 | 5 | 0.925 |
| masking_backtrack | yati | 1040 | -2.259 | 55 | 28 | 0.672 |
| masking_backtrack | other | 8471 | -1.303 | 68 | 6 | 0.939 |
| hybrid | line_start | 394 | -1.298 | 65 | 2 | 0.973 |
| hybrid | prasa | 384 | -0.976 | 82 | 4 | 0.927 |
| hybrid | yati | 613 | -4.161 | 42 | 43 | 0.554 |
| hybrid | other | 6842 | -1.575 | 65 | 7 | 0.926 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 7 / -1.03 / 58 | 100 / -1.67 / 57 | 100 / -1.43 / 59 | 100 / -1.88 / 60 |
| bhujangaprayatamu | 0 / -0.74 / 27 | 100 / -1.65 / 31 | 100 / -1.26 / 14 | 100 / -2.15 / 12 |
| champakamala | 0 / -0.98 / 48 | 100 / -1.63 / 46 | 100 / -1.15 / 51 | 100 / -1.59 / 47 |
| kandamu | 20 / -0.99 / 53 | 100 / -1.63 / 48 | 100 / -1.25 / 50 | 100 / -1.62 / 49 |
| malini | 0 / -0.95 / 7 | 100 / -1.54 / 12 | 100 / -1.19 / 7 | 100 / -1.48 / 4 |
| mattakokilamu | 0 / -1.05 / 48 | 100 / -1.49 / 53 | 100 / -1.21 / 50 | 100 / -1.66 / 50 |
| mattebhavikriditamu | 0 / -1.08 / 42 | 100 / -1.78 / 43 | 100 / -1.48 / 41 | 100 / -1.83 / 36 |
| sardulavikriditamu | 0 / -1.13 / 42 | 100 / -1.47 / 40 | 100 / -1.46 / 40 | 100 / -1.78 / 38 |
| seesamu | 0 / -1.00 / 67 | 100 / -3.22 / 48 | 100 / -2.89 / 44 | 100 / -3.39 / 56 |
| tetagiti | 10 / -1.08 / 56 | 100 / -1.60 / 53 | 100 / -1.44 / 45 | 100 / -1.73 / 47 |
| utpalamala | 0 / -1.02 / 47 | 100 / -1.44 / 52 | 100 / -1.35 / 49 | 100 / -1.53 / 48 |

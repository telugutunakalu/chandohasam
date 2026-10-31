# Token choices under the constraint

Runs: `e6_nandi_val`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 2 | 4 | 77 | -0.809 | 83 | 5 | 0.946 | 1.503 | 48 | 8 | 0 | 0.0 |
| masking_only | 114 | 100 | 100 | 76 | -1.380 | 76 | 9 | 0.907 | 1.616 | 46 | 10 | 0 | 0.0 |
| masking_backtrack | 114 | 100 | 100 | 91 | -1.118 | 76 | 7 | 0.922 | 1.541 | 47 | 9 | 0 | 7.6 |
| hybrid | 114 | 100 | 100 | 73 | -1.572 | 71 | 9 | 0.906 | 1.651 | 45 | 8 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 227 | -0.772 | 74 | 0 | 0.995 |
| baseline | prasa | 154 | -0.602 | 91 | 1 | 0.974 |
| baseline | yati | 76 | -0.645 | 88 | 0 | 0.948 |
| baseline | other | 1979 | -0.834 | 83 | 1 | 0.980 |
| masking_only | line_start | 418 | -0.919 | 81 | 1 | 0.976 |
| masking_only | prasa | 395 | -0.830 | 86 | 7 | 0.914 |
| masking_only | yati | 597 | -3.894 | 53 | 36 | 0.616 |
| masking_only | other | 7278 | -1.230 | 77 | 7 | 0.926 |
| masking_backtrack | line_start | 430 | -0.885 | 81 | 1 | 0.983 |
| masking_backtrack | prasa | 429 | -0.794 | 83 | 9 | 0.898 |
| masking_backtrack | yati | 1012 | -1.809 | 66 | 22 | 0.741 |
| masking_backtrack | other | 8545 | -1.064 | 76 | 5 | 0.942 |
| hybrid | line_start | 401 | -1.142 | 73 | 2 | 0.969 |
| hybrid | prasa | 399 | -0.871 | 81 | 6 | 0.919 |
| hybrid | yati | 615 | -4.188 | 52 | 38 | 0.589 |
| hybrid | other | 6955 | -1.406 | 72 | 7 | 0.930 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 7 / -0.85 / 61 | 100 / -1.71 / 54 | 100 / -1.06 / 60 | 100 / -1.69 / 59 |
| bhujangaprayatamu | 0 / -0.58 / 25 | 100 / -1.65 / 25 | 100 / -1.68 / 20 | 100 / -1.82 / 0 |
| champakamala | 13 / -0.79 / 51 | 100 / -1.18 / 51 | 100 / -1.03 / 49 | 100 / -1.25 / 47 |
| kandamu | 7 / -0.73 / 48 | 100 / -1.37 / 46 | 100 / -1.01 / 46 | 100 / -1.66 / 48 |
| malini | 0 / -0.70 / 19 | 100 / -1.19 / 7 | 100 / -0.87 / 11 | 100 / -1.44 / 7 |
| mattakokilamu | 0 / -0.81 / 45 | 100 / -1.58 / 44 | 100 / -1.12 / 46 | 100 / -1.86 / 46 |
| mattebhavikriditamu | 0 / -0.84 / 44 | 100 / -1.23 / 43 | 100 / -1.04 / 44 | 100 / -1.56 / 39 |
| sardulavikriditamu | 0 / -0.82 / 44 | 100 / -1.25 / 41 | 100 / -1.24 / 42 | 100 / -1.62 / 40 |
| seesamu | 0 / -0.95 / 46 | 100 / -2.82 / 58 | 100 / -3.30 / 56 | 100 / -3.09 / 51 |
| tetagiti | 0 / -0.80 / 59 | 100 / -1.55 / 55 | 100 / -1.13 / 56 | 100 / -1.91 / 49 |
| utpalamala | 0 / -0.81 / 47 | 100 / -1.34 / 42 | 100 / -0.97 / 45 | 100 / -1.29 / 41 |

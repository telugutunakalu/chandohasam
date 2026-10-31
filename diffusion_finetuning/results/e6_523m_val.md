# Token choices under the constraint

Runs: `e6_523m_val`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 1 | 1 | 91 | -0.941 | 77 | 7 | 0.923 | 1.843 | 58 | 8 | 0 | 0.0 |
| masking_only | 114 | 98 | 98 | 108 | -2.346 | 56 | 24 | 0.736 | 2.496 | 50 | 21 | 0 | 0.0 |
| masking_backtrack | 114 | 100 | 100 | 116 | -1.538 | 63 | 13 | 0.852 | 2.085 | 56 | 11 | 0 | 10.9 |
| hybrid | 114 | 100 | 100 | 100 | -2.199 | 57 | 20 | 0.775 | 2.386 | 46 | 12 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 154 | -1.519 | 34 | 0 | 0.986 |
| baseline | prasa | 114 | -0.751 | 93 | 2 | 0.968 |
| baseline | yati | 21 | -1.048 | 76 | 5 | 0.891 |
| baseline | other | 1285 | -0.883 | 80 | 1 | 0.972 |
| masking_only | line_start | 520 | -1.879 | 57 | 6 | 0.899 |
| masking_only | prasa | 491 | -1.269 | 75 | 14 | 0.800 |
| masking_only | yati | 1082 | -4.543 | 27 | 62 | 0.351 |
| masking_only | other | 10241 | -2.189 | 58 | 21 | 0.765 |
| masking_backtrack | line_start | 518 | -1.568 | 61 | 3 | 0.952 |
| masking_backtrack | prasa | 509 | -0.924 | 78 | 9 | 0.860 |
| masking_backtrack | yati | 1261 | -2.558 | 43 | 37 | 0.588 |
| masking_backtrack | other | 10972 | -1.447 | 64 | 11 | 0.877 |
| hybrid | line_start | 517 | -1.854 | 59 | 7 | 0.909 |
| hybrid | prasa | 477 | -1.359 | 73 | 14 | 0.807 |
| hybrid | yati | 1005 | -4.455 | 31 | 58 | 0.392 |
| hybrid | other | 9407 | -2.019 | 59 | 18 | 0.807 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 0 / -0.87 / 75 | 100 / -1.61 / 78 | 100 / -1.48 / 79 | 100 / -1.64 / 72 |
| bhujangaprayatamu | 0 / -0.85 / 42 | 100 / -3.01 / 19 | 100 / -2.77 / 11 | 100 / -3.77 / 0 |
| champakamala | 0 / -0.88 / 65 | 93 / -2.40 / 47 | 100 / -1.28 / 59 | 100 / -1.84 / 47 |
| kandamu | 0 / -0.88 / 64 | 100 / -1.81 / 59 | 100 / -1.56 / 58 | 100 / -1.82 / 49 |
| malini | 0 / -0.96 / 12 | 100 / -3.26 / 21 | 100 / -1.83 / 29 | 100 / -3.10 / 28 |
| mattakokilamu | 0 / -0.88 / 64 | 100 / -2.76 / 52 | 100 / -1.36 / 60 | 100 / -2.26 / 46 |
| mattebhavikriditamu | 0 / -1.01 / 49 | 100 / -3.00 / 34 | 100 / -1.69 / 42 | 100 / -2.90 / 30 |
| sardulavikriditamu | 0 / -1.06 / 53 | 100 / -2.75 / 39 | 100 / -1.57 / 45 | 100 / -2.58 / 38 |
| seesamu | 0 / -1.14 / 65 | 100 / -1.94 / 58 | 100 / -2.27 / 55 | 100 / -2.32 / 60 |
| tetagiti | 0 / -0.86 / 60 | 100 / -1.60 / 61 | 100 / -1.79 / 62 | 100 / -1.74 / 55 |
| utpalamala | 7 / -0.95 / 50 | 93 / -1.76 / 49 | 100 / -1.34 / 54 | 100 / -1.84 / 46 |

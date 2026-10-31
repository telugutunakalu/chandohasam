# Token choices under the constraint

Runs: `e6_120m_val`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 0 | 0 | 91 | -1.236 | 70 | 9 | 0.897 | 2.291 | 63 | 10 | 0 | 0.0 |
| masking_only | 114 | 100 | 100 | 115 | -2.816 | 50 | 27 | 0.685 | 2.993 | 50 | 16 | 0 | 0.0 |
| masking_backtrack | 114 | 100 | 100 | 141 | -2.219 | 52 | 21 | 0.759 | 2.561 | 54 | 12 | 0 | 18.3 |
| hybrid | 114 | 100 | 100 | 111 | -2.797 | 49 | 26 | 0.696 | 2.970 | 46 | 13 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 146 | -1.571 | 37 | 0 | 0.987 |
| baseline | prasa | 102 | -0.865 | 89 | 0 | 0.961 |
| baseline | yati | 12 | -1.635 | 75 | 8 | 0.882 |
| baseline | other | 958 | -1.165 | 73 | 2 | 0.954 |
| masking_only | line_start | 530 | -2.261 | 51 | 8 | 0.892 |
| masking_only | prasa | 487 | -1.182 | 77 | 9 | 0.822 |
| masking_only | yati | 1277 | -4.889 | 29 | 58 | 0.335 |
| masking_only | other | 10770 | -2.672 | 51 | 25 | 0.710 |
| masking_backtrack | line_start | 552 | -2.049 | 50 | 10 | 0.894 |
| masking_backtrack | prasa | 552 | -1.207 | 74 | 12 | 0.811 |
| masking_backtrack | yati | 1808 | -3.400 | 32 | 52 | 0.440 |
| masking_backtrack | other | 13135 | -2.106 | 54 | 18 | 0.795 |
| hybrid | line_start | 526 | -2.251 | 50 | 9 | 0.885 |
| hybrid | prasa | 478 | -1.309 | 78 | 9 | 0.800 |
| hybrid | yati | 1336 | -5.050 | 29 | 59 | 0.323 |
| hybrid | other | 10332 | -2.602 | 51 | 23 | 0.729 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 0 / -1.05 / 80 | 100 / -1.88 / 77 | 100 / -2.01 / 73 | 100 / -1.95 / 70 |
| bhujangaprayatamu | 0 / -1.15 / 46 | 100 / -2.67 / 0 | 100 / -2.96 / 10 | 100 / -3.38 / 0 |
| champakamala | 0 / -1.19 / 59 | 100 / -2.75 / 43 | 100 / -1.93 / 56 | 100 / -2.67 / 45 |
| kandamu | 0 / -1.22 / 71 | 100 / -2.09 / 64 | 100 / -1.69 / 67 | 100 / -2.10 / 62 |
| malini | 0 / -1.36 / 29 | 100 / -3.51 / 26 | 100 / -3.02 / 26 | 100 / -3.57 / 25 |
| mattakokilamu | 0 / -1.25 / 63 | 100 / -2.92 / 47 | 100 / -2.72 / 49 | 100 / -3.10 / 38 |
| mattebhavikriditamu | 0 / -1.35 / 55 | 100 / -3.43 / 32 | 100 / -2.72 / 37 | 100 / -3.48 / 32 |
| sardulavikriditamu | 0 / -1.37 / 57 | 100 / -3.40 / 35 | 100 / -2.43 / 43 | 100 / -3.19 / 35 |
| seesamu | 0 / -1.61 / 71 | 100 / -2.24 / 58 | 100 / -2.45 / 63 | 100 / -2.21 / 50 |
| tetagiti | 0 / -1.14 / 69 | 100 / -1.92 / 71 | 100 / -1.72 / 66 | 100 / -2.02 / 53 |
| utpalamala | 0 / -1.16 / 62 | 100 / -2.82 / 47 | 100 / -1.75 / 53 | 100 / -2.64 / 44 |

# Token choices under the constraint

Runs: `e6_120m_t1_val`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 0 | 0 | 92 | -1.220 | 71 | 8 | 0.905 | 2.257 | 62 | 10 | 0 | 0.0 |
| masking_only | 114 | 100 | 100 | 116 | -2.846 | 50 | 27 | 0.686 | 2.965 | 48 | 19 | 0 | 0.0 |
| masking_backtrack | 114 | 100 | 100 | 133 | -2.068 | 54 | 19 | 0.786 | 2.503 | 57 | 12 | 0 | 16.0 |
| hybrid | 114 | 100 | 100 | 110 | -2.798 | 50 | 26 | 0.698 | 2.927 | 47 | 12 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 144 | -1.643 | 32 | 0 | 0.991 |
| baseline | prasa | 111 | -0.891 | 90 | 0 | 0.964 |
| baseline | yati | 7 | -1.180 | 86 | 0 | 0.891 |
| baseline | other | 974 | -1.168 | 73 | 1 | 0.962 |
| masking_only | line_start | 539 | -2.578 | 47 | 9 | 0.869 |
| masking_only | prasa | 496 | -1.157 | 78 | 9 | 0.827 |
| masking_only | yati | 1211 | -5.028 | 28 | 60 | 0.337 |
| masking_only | other | 10974 | -2.695 | 51 | 25 | 0.709 |
| masking_backtrack | line_start | 545 | -2.233 | 50 | 5 | 0.925 |
| masking_backtrack | prasa | 523 | -1.037 | 79 | 7 | 0.853 |
| masking_backtrack | yati | 1593 | -3.121 | 31 | 50 | 0.471 |
| masking_backtrack | other | 12468 | -1.970 | 56 | 16 | 0.817 |
| hybrid | line_start | 522 | -2.224 | 48 | 8 | 0.889 |
| hybrid | prasa | 496 | -1.367 | 77 | 11 | 0.804 |
| hybrid | yati | 1309 | -5.302 | 28 | 62 | 0.312 |
| hybrid | other | 10191 | -2.576 | 51 | 23 | 0.733 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 0 / -1.23 / 76 | 100 / -1.85 / 79 | 100 / -1.75 / 83 | 100 / -2.05 / 68 |
| bhujangaprayatamu | 0 / -0.90 / 57 | 100 / -3.49 / 7 | 100 / -3.69 / 14 | 100 / -3.77 / 9 |
| champakamala | 0 / -1.15 / 59 | 100 / -2.65 / 46 | 100 / -1.73 / 56 | 100 / -2.60 / 47 |
| kandamu | 0 / -1.10 / 66 | 100 / -2.19 / 66 | 100 / -1.88 / 73 | 100 / -2.18 / 62 |
| malini | 0 / -1.23 / 46 | 100 / -3.77 / 16 | 100 / -3.15 / 26 | 100 / -3.79 / 9 |
| mattakokilamu | 0 / -1.18 / 60 | 100 / -3.21 / 35 | 100 / -2.68 / 44 | 100 / -3.01 / 45 |
| mattebhavikriditamu | 0 / -1.29 / 57 | 100 / -3.49 / 27 | 100 / -2.19 / 40 | 100 / -3.37 / 36 |
| sardulavikriditamu | 0 / -1.31 / 60 | 100 / -3.40 / 36 | 100 / -2.12 / 46 | 100 / -3.50 / 30 |
| seesamu | 0 / -1.33 / 46 | 100 / -2.27 / 71 | 100 / -2.09 / 78 | 100 / -2.14 / 47 |
| tetagiti | 0 / -1.22 / 70 | 100 / -1.97 / 70 | 100 / -1.94 / 63 | 100 / -2.12 / 66 |
| utpalamala | 0 / -1.21 / 63 | 100 / -2.71 / 45 | 100 / -1.81 / 54 | 100 / -2.35 / 48 |

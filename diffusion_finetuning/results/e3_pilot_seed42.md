# Token choices under the constraint

Runs: `e3_pilot_seed42`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 111 | 0 | 0 | 472 | -0.770 | 79 | 10 | 0.741 | 1.374 | 35 | 10 | 0 | 0.0 |
| masking_only | 111 | 100 | 100 | 158 | -1.848 | 61 | 27 | 0.655 | 2.184 | 40 | 25 | 8 | 0.0 |
| masking_backtrack | 111 | 100 | 100 | 202 | -2.199 | 53 | 30 | 0.626 | 2.406 | 43 | 25 | 5 | 25.7 |
| hybrid | 111 | 100 | 100 | 138 | -2.074 | 57 | 28 | 0.649 | 2.237 | 40 | 17 | 13 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 141 | -2.264 | 37 | 0 | 0.872 |
| baseline | prasa | 6 | -3.066 | 0 | 50 | 0.843 |
| baseline | other | 39 | -1.679 | 54 | 3 | 0.913 |
| masking_only | line_start | 771 | -3.177 | 40 | 29 | 0.568 |
| masking_only | prasa | 852 | -2.168 | 61 | 37 | 0.514 |
| masking_only | yati | 2878 | -2.514 | 51 | 42 | 0.503 |
| masking_only | other | 13025 | -1.602 | 65 | 23 | 0.704 |
| masking_backtrack | line_start | 873 | -3.364 | 37 | 28 | 0.564 |
| masking_backtrack | prasa | 980 | -2.279 | 56 | 41 | 0.475 |
| masking_backtrack | yati | 3466 | -2.872 | 40 | 44 | 0.480 |
| masking_backtrack | other | 17134 | -2.000 | 56 | 27 | 0.667 |
| hybrid | line_start | 712 | -3.120 | 41 | 26 | 0.593 |
| hybrid | prasa | 855 | -1.987 | 61 | 38 | 0.542 |
| hybrid | yati | 2502 | -2.769 | 47 | 44 | 0.485 |
| hybrid | other | 11232 | -1.859 | 61 | 24 | 0.697 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 0 / -0.77 / 36 | 100 / -1.55 / 71 | 100 / -1.66 / 68 | 100 / -1.47 / 52 |
| bhujangaprayatamu | 0 / -0.77 / 36 | 100 / -2.01 / 40 | 100 / -2.63 / 29 | 100 / -2.24 / 30 |
| champakamala | 0 / -0.77 / 36 | 100 / -1.90 / 34 | 100 / -2.12 / 33 | 100 / -2.31 / 38 |
| dvipada | 0 / -0.77 / 32 | 100 / -2.53 / 62 | 100 / -2.28 / 80 | 100 / -2.36 / 55 |
| hayapracara_ragada | 0 / -0.77 / 32 | 100 / -2.04 / 62 | 100 / -2.04 / 62 | 100 / -1.77 / 29 |
| indravajra | 0 / -0.77 / 36 | 100 / -1.95 / 14 | 100 / -2.61 / 13 | 100 / -2.10 / 16 |
| kandamu | 0 / -0.77 / 36 | 100 / -1.65 / 74 | 100 / -2.11 / 75 | 100 / -2.08 / 61 |
| kavirajavirajitamu | 0 / -0.77 / 36 | 100 / -1.56 / 36 | 100 / -1.81 / 31 | 100 / -2.08 / 37 |
| lalita | 0 / -0.77 / 36 | 100 / -2.19 / 30 | 100 / -2.72 / 10 | 100 / -2.23 / 12 |
| layagrahi | 0 / -0.77 / 36 | 100 / -1.39 / 21 | 100 / -2.03 / 36 | 100 / -1.64 / 36 |
| layavibhati | 0 / -0.77 / 36 | 100 / -1.54 / 68 | 100 / -1.72 / 70 | 100 / -1.85 / 60 |
| madhuragati_ragada | 0 / -0.77 / 32 | 100 / -2.13 / 59 | 100 / -2.04 / 69 | 100 / -2.08 / 46 |
| madhyakkara | 0 / -0.77 / 36 | 100 / -2.23 / 73 | 100 / -1.88 / 75 | 100 / -2.13 / 54 |
| mahasragdhara | 0 / -0.77 / 36 | 100 / -1.85 / 26 | 100 / -1.72 / 29 | 100 / -2.17 / 26 |
| malini | 0 / -0.77 / 36 | 100 / -1.85 / 44 | 100 / -2.15 / 28 | 100 / -2.11 / 28 |
| mangalamahasri | 0 / -0.77 / 36 | 100 / -1.60 / 26 | 100 / -1.97 / 40 | 100 / -1.98 / 44 |
| manini | 0 / -0.77 / 36 | 100 / -1.55 / 45 | 100 / -2.10 / 28 | 100 / -1.86 / 33 |
| mattakokilamu | 0 / -0.77 / 36 | 100 / -1.86 / 15 | 100 / -2.57 / 30 | 100 / -2.14 / 54 |
| mattebhavikriditamu | 0 / -0.77 / 36 | 100 / -1.90 / 19 | 100 / -1.82 / 31 | 100 / -2.04 / 35 |
| pamcacamaramu | 0 / -0.77 / 36 | 100 / -1.89 / 44 | 100 / -2.27 / 27 | 100 / -2.42 / 35 |
| rathoddhata | 0 / -0.77 / 36 | 100 / -2.02 / 24 | 100 / -2.50 / 42 | 100 / -2.31 / 47 |
| salini | 0 / -0.77 / 36 | 100 / -2.18 / 18 | 100 / -2.75 / 2 | 100 / -2.22 / 11 |
| sardulavikriditamu | 0 / -0.77 / 36 | 100 / -1.94 / 20 | 100 / -2.52 / 33 | 100 / -2.16 / 27 |
| seesamu | 0 / -0.77 / 36 | 100 / -1.95 / 49 | 100 / -2.15 / 50 | 100 / -1.96 / 53 |
| sragdhara | 0 / -0.77 / 36 | 100 / -1.79 / 11 | 100 / -2.31 / 17 | 100 / -2.20 / 43 |
| sragvini | 0 / -0.77 / 36 | 100 / -1.62 / 22 | 100 / -2.28 / 14 | 100 / -1.69 / 24 |
| taralamu | 0 / -0.77 / 36 | 100 / -2.22 / 22 | 100 / -1.97 / 36 | 100 / -2.27 / 37 |
| taruvoja | 0 / -0.77 / 36 | 100 / -1.84 / 50 | 100 / -1.90 / 64 | 100 / -2.11 / 48 |
| tetagiti | 0 / -0.77 / 36 | 100 / -2.05 / 66 | 100 / -1.87 / 67 | 100 / -1.70 / 46 |
| totakamu | 0 / -0.77 / 36 | 100 / -2.23 / 26 | 100 / -2.30 / 24 | 100 / -1.69 / 50 |
| turagagati_ragada | 0 / -0.77 / 36 | 100 / -1.59 / 71 | 100 / -1.59 / 71 | 100 / -1.46 / 43 |
| upendravajra | 0 / -0.77 / 36 | 100 / -2.06 / 20 | 100 / -3.03 / 34 | 100 / -2.40 / 20 |
| utpalamala | 0 / -0.77 / 36 | 100 / -1.58 / 18 | 100 / -2.46 / 44 | 100 / -1.86 / 29 |
| utsahamu | 0 / -0.77 / 36 | 100 / -1.87 / 78 | 100 / -2.23 / 72 | 100 / -2.23 / 55 |
| vanamayuramu | 0 / -0.77 / 36 | 100 / -1.91 / 18 | 100 / -2.55 / 34 | 100 / -2.53 / 38 |
| vasamtatilakamu | 0 / -0.77 / 36 | 100 / -2.31 / 23 | 100 / -2.40 / 17 | 100 / -2.33 / 20 |
| vidyunmala | 0 / -0.77 / 36 | 100 / -2.03 / 0 | 100 / -2.64 / 26 | 100 / -2.34 / 42 |

# Token choices under the constraint

Runs: `2026-09-25_diffusion_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_only | 555 | 100 | 100 | 102 | -3.837 | 38 | 47 | 0.493 | 2.364 | 32 | 29 | 4 | 0.0 |
| masking_backtrack | 555 | 100 | 100 | 194 | -3.128 | 50 | 36 | 0.606 | 1.783 | 28 | 25 | 2 | 25.8 |
| hybrid | 555 | 100 | 100 | 98 | -3.495 | 42 | 47 | 0.499 | 2.131 | 32 | 26 | 3 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_only | line_start | 3498 | -2.519 | 54 | 28 | 0.655 |
| masking_only | prasa | 2541 | -4.066 | 34 | 55 | 0.353 |
| masking_only | yati | 8039 | -5.532 | 21 | 73 | 0.236 |
| masking_only | other | 42726 | -3.612 | 39 | 44 | 0.537 |
| masking_backtrack | line_start | 6766 | -2.072 | 63 | 22 | 0.745 |
| masking_backtrack | prasa | 4509 | -3.496 | 45 | 45 | 0.483 |
| masking_backtrack | yati | 15752 | -4.555 | 35 | 58 | 0.372 |
| masking_backtrack | other | 80763 | -2.918 | 52 | 32 | 0.646 |
| hybrid | line_start | 3370 | -2.435 | 54 | 29 | 0.658 |
| hybrid | prasa | 2480 | -4.121 | 31 | 58 | 0.339 |
| hybrid | yati | 8156 | -5.419 | 23 | 74 | 0.234 |
| hybrid | other | 40421 | -3.157 | 45 | 43 | 0.550 |

## By meter

| meter | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|
| ataveladi | 100 / -3.43 / 45 | 100 / -2.24 / 45 | 100 / -2.47 / 47 |
| bhujangaprayatamu | 100 / -3.98 / 9 | 100 / -3.25 / 14 | 100 / -3.81 / 6 |
| champakamala | 100 / -3.93 / 25 | 100 / -3.37 / 23 | 100 / -3.50 / 23 |
| dvipada | 100 / -3.86 / 44 | 100 / -2.37 / 39 | 100 / -3.50 / 47 |
| hayapracara_ragada | 100 / -3.44 / 59 | 100 / -3.15 / 56 | 100 / -2.67 / 55 |
| indravajra | 100 / -4.15 / 15 | 100 / -3.48 / 11 | 100 / -4.23 / 20 |
| kandamu | 100 / -3.82 / 52 | 100 / -2.42 / 46 | 100 / -3.13 / 49 |
| kavirajavirajitamu | 100 / -4.07 / 29 | 100 / -4.02 / 24 | 100 / -3.79 / 22 |
| lalita | 100 / -4.07 / 14 | 100 / -3.62 / 10 | 100 / -3.80 / 19 |
| layagrahi | 100 / -3.86 / 25 | 100 / -3.78 / 25 | 100 / -3.79 / 24 |
| layavibhati | 100 / -3.73 / 37 | 100 / -2.83 / 33 | 100 / -3.23 / 43 |
| madhuragati_ragada | 100 / -3.43 / 55 | 100 / -2.81 / 52 | 100 / -2.36 / 57 |
| madhyakkara | 100 / -3.03 / 47 | 100 / -2.13 / 41 | 100 / -2.27 / 42 |
| mahasragdhara | 100 / -4.35 / 18 | 100 / -3.97 / 19 | 100 / -4.18 / 23 |
| malini | 100 / -4.03 / 35 | 100 / -3.37 / 30 | 100 / -3.74 / 29 |
| mangalamahasri | 100 / -4.12 / 24 | 100 / -3.50 / 22 | 100 / -3.54 / 24 |
| manini | 100 / -3.96 / 22 | 100 / -3.45 / 22 | 100 / -3.80 / 29 |
| mattakokilamu | 100 / -4.12 / 19 | 100 / -3.29 / 16 | 100 / -4.01 / 19 |
| mattebhavikriditamu | 100 / -4.02 / 22 | 100 / -3.42 / 17 | 100 / -3.89 / 16 |
| pamcacamaramu | 100 / -3.99 / 17 | 100 / -3.43 / 12 | 100 / -3.84 / 19 |
| rathoddhata | 100 / -3.87 / 29 | 100 / -3.34 / 23 | 100 / -3.57 / 25 |
| salini | 100 / -4.35 / 7 | 100 / -3.97 / 12 | 100 / -4.18 / 12 |
| sardulavikriditamu | 100 / -4.15 / 17 | 100 / -3.26 / 14 | 100 / -4.16 / 15 |
| seesamu | 100 / -2.66 / 43 | 100 / -1.57 / 39 | 100 / -1.87 / 49 |
| sragdhara | 100 / -4.16 / 20 | 100 / -3.94 / 13 | 100 / -3.84 / 20 |
| sragvini | 100 / -4.23 / 10 | 100 / -3.66 / 14 | 100 / -3.75 / 13 |
| taralamu | 100 / -3.83 / 29 | 100 / -3.01 / 22 | 100 / -3.64 / 23 |
| taruvoja | 100 / -3.29 / 43 | 100 / -2.52 / 38 | 100 / -3.21 / 54 |
| tetagiti | 100 / -3.35 / 64 | 100 / -2.49 / 57 | 100 / -2.47 / 44 |
| totakamu | 100 / -3.98 / 22 | 100 / -3.27 / 21 | 100 / -3.85 / 33 |
| turagagati_ragada | 100 / -2.76 / 44 | 100 / -2.08 / 43 | 100 / -2.09 / 44 |
| upendravajra | 100 / -4.25 / 22 | 100 / -3.34 / 11 | 100 / -3.79 / 18 |
| utpalamala | 100 / -4.21 / 22 | 100 / -3.40 / 20 | 100 / -3.66 / 23 |
| utsahamu | 100 / -3.07 / 38 | 100 / -2.42 / 34 | 100 / -2.90 / 36 |
| vanamayuramu | 100 / -3.81 / 24 | 100 / -3.17 / 23 | 100 / -3.28 / 26 |
| vasamtatilakamu | 100 / -3.94 / 17 | 100 / -3.14 / 19 | 100 / -3.95 / 19 |
| vidyunmala | 100 / -3.83 / 4 | 100 / -3.46 / 5 | 100 / -3.53 / 11 |

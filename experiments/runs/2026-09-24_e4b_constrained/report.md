# Token choices under the constraint

Runs: `2026-09-24_e4b_baseline`, `2026-09-24_e4b_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 555 | 0 | 0 | 65 | -0.839 | 77 | 22 | 0.778 | 1.453 | 41 | 1 | 0.0 |
| masking_only | 555 | 100 | 100 | 107 | -2.181 | 59 | 31 | 0.666 | 1.513 | 17 | 20 | 0.0 |
| masking_backtrack | 555 | 100 | 100 | 161 | -2.292 | 51 | 35 | 0.626 | 1.703 | 20 | 22 | 26.1 |
| hybrid | 555 | 100 | 100 | 101 | -2.338 | 56 | 32 | 0.658 | 1.599 | 19 | 17 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 576 | -1.267 | 54 | 5 | 0.959 |
| baseline | prasa | 420 | -0.500 | 94 | 1 | 0.942 |
| baseline | yati | 1 | -0.947 | 100 | 0 | 0.877 |
| baseline | other | 1016 | -0.811 | 80 | 2 | 0.938 |
| masking_only | line_start | 3059 | -2.430 | 46 | 28 | 0.701 |
| masking_only | prasa | 2428 | -3.420 | 53 | 45 | 0.523 |
| masking_only | yati | 8582 | -3.659 | 46 | 50 | 0.472 |
| masking_only | other | 45105 | -1.817 | 63 | 27 | 0.708 |
| masking_backtrack | line_start | 4677 | -2.442 | 42 | 29 | 0.673 |
| masking_backtrack | prasa | 3006 | -2.773 | 54 | 42 | 0.550 |
| masking_backtrack | yati | 13309 | -3.273 | 38 | 54 | 0.439 |
| masking_backtrack | other | 68278 | -2.069 | 54 | 32 | 0.663 |
| hybrid | line_start | 3085 | -2.592 | 43 | 28 | 0.696 |
| hybrid | prasa | 2519 | -3.504 | 50 | 47 | 0.500 |
| hybrid | yati | 8875 | -3.817 | 44 | 52 | 0.457 |
| hybrid | other | 41694 | -1.934 | 60 | 27 | 0.707 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 0 / -0.88 / 40 | 100 / -2.86 / 29 | 100 / -2.29 / 33 | 100 / -3.20 / 30 |
| bhujangaprayatamu | 0 / -0.88 / 41 | 100 / -2.09 / 3 | 100 / -2.25 / 10 | 100 / -2.22 / 2 |
| champakamala | 0 / -0.82 / 41 | 100 / -2.04 / 13 | 100 / -2.31 / 14 | 100 / -2.56 / 15 |
| dvipada | 0 / -0.89 / 41 | 100 / -2.74 / 48 | 100 / -2.17 / 48 | 100 / -3.30 / 43 |
| hayapracara_ragada | 0 / -0.93 / 40 | 100 / -3.29 / 33 | 100 / -2.44 / 31 | 100 / -4.01 / 27 |
| indravajra | 0 / -0.84 / 40 | 100 / -2.40 / 5 | 100 / -2.57 / 9 | 100 / -2.81 / 9 |
| kandamu | 0 / -0.86 / 36 | 100 / -2.25 / 29 | 100 / -2.30 / 32 | 100 / -2.67 / 35 |
| kavirajavirajitamu | 0 / -0.84 / 40 | 100 / -2.22 / 18 | 100 / -2.25 / 13 | 100 / -2.08 / 18 |
| lalita | 0 / -0.83 / 46 | 100 / -2.23 / 4 | 100 / -2.53 / 8 | 100 / -2.55 / 10 |
| layagrahi | 0 / -0.83 / 47 | 100 / -1.83 / 4 | 100 / -2.01 / 22 | 100 / -1.83 / 11 |
| layavibhati | 0 / -0.85 / 38 | 100 / -1.80 / 11 | 100 / -1.85 / 21 | 100 / -1.78 / 11 |
| madhuragati_ragada | 0 / -0.85 / 36 | 100 / -2.87 / 26 | 100 / -2.33 / 37 | 100 / -3.33 / 25 |
| madhyakkara | 0 / -0.85 / 37 | 100 / -2.40 / 30 | 100 / -2.06 / 36 | 100 / -2.32 / 35 |
| mahasragdhara | 0 / -0.76 / 39 | 100 / -1.61 / 15 | 100 / -2.03 / 16 | 100 / -1.73 / 19 |
| malini | 0 / -0.88 / 46 | 100 / -2.15 / 13 | 100 / -2.54 / 22 | 100 / -2.34 / 14 |
| mangalamahasri | 0 / -0.82 / 33 | 100 / -2.48 / 9 | 100 / -2.19 / 11 | 100 / -2.39 / 13 |
| manini | 0 / -0.73 / 43 | 100 / -2.03 / 10 | 100 / -2.42 / 6 | 100 / -2.10 / 18 |
| mattakokilamu | 0 / -0.88 / 39 | 100 / -2.18 / 18 | 100 / -2.38 / 25 | 100 / -2.71 / 13 |
| mattebhavikriditamu | 0 / -0.78 / 43 | 100 / -2.12 / 8 | 100 / -2.55 / 9 | 100 / -2.20 / 12 |
| pamcacamaramu | 0 / -0.78 / 43 | 100 / -1.96 / 12 | 100 / -2.13 / 9 | 100 / -2.05 / 12 |
| rathoddhata | 0 / -0.85 / 47 | 100 / -2.60 / 31 | 100 / -2.54 / 22 | 100 / -2.88 / 34 |
| salini | 0 / -0.84 / 39 | 100 / -2.17 / 10 | 100 / -2.34 / 8 | 100 / -2.40 / 12 |
| sardulavikriditamu | 0 / -0.79 / 39 | 100 / -2.24 / 2 | 100 / -2.55 / 8 | 100 / -2.26 / 5 |
| seesamu | 0 / -0.77 / 39 | 100 / -2.63 / 26 | 100 / -2.37 / 30 | 100 / -2.76 / 23 |
| sragdhara | 0 / -0.79 / 41 | 100 / -1.64 / 4 | 100 / -2.20 / 6 | 100 / -1.82 / 6 |
| sragvini | 0 / -0.86 / 41 | 100 / -2.36 / 17 | 100 / -2.34 / 11 | 100 / -2.45 / 15 |
| taralamu | 0 / -0.85 / 42 | 100 / -1.93 / 17 | 100 / -2.25 / 24 | 100 / -2.19 / 22 |
| taruvoja | 0 / -0.89 / 38 | 100 / -2.49 / 23 | 100 / -2.35 / 23 | 100 / -2.43 / 24 |
| tetagiti | 0 / -0.87 / 41 | 100 / -2.49 / 35 | 100 / -2.22 / 33 | 100 / -2.95 / 30 |
| totakamu | 0 / -0.74 / 47 | 100 / -2.26 / 31 | 100 / -2.55 / 24 | 100 / -2.43 / 26 |
| turagagati_ragada | 0 / -0.92 / 40 | 100 / -2.50 / 30 | 100 / -2.02 / 29 | 100 / -2.62 / 28 |
| upendravajra | 0 / -0.93 / 44 | 100 / -1.91 / 11 | 100 / -2.22 / 6 | 100 / -2.22 / 11 |
| utpalamala | 0 / -0.83 / 39 | 100 / -2.61 / 8 | 100 / -2.56 / 14 | 100 / -2.30 / 11 |
| utsahamu | 0 / -0.86 / 37 | 100 / -2.66 / 26 | 100 / -2.39 / 31 | 100 / -2.61 / 30 |
| vanamayuramu | 0 / -0.85 / 45 | 100 / -1.98 / 11 | 100 / -2.29 / 21 | 100 / -2.67 / 20 |
| vasamtatilakamu | 0 / -0.81 / 47 | 100 / -2.10 / 12 | 100 / -2.54 / 16 | 100 / -2.75 / 18 |
| vidyunmala | 0 / -0.95 / 43 | 100 / -1.94 / 12 | 100 / -1.88 / 4 | 100 / -2.17 / 18 |

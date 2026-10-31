# Token choices under the constraint

Runs: `e3_e2_pretrained_10ep`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 555 | 0 | 0 | 87 | -0.921 | 76 | 18 | 0.766 | 1.575 | 85 | 2 | 7 | 0.0 |
| masking_only | 555 | 100 | 100 | 146 | -2.503 | 53 | 30 | 0.628 | 2.704 | 48 | 40 | 13 | 0.0 |
| masking_backtrack | 555 | 100 | 100 | 187 | -2.793 | 43 | 32 | 0.613 | 2.958 | 50 | 36 | 9 | 24.6 |
| hybrid | 555 | 100 | 100 | 141 | -2.531 | 52 | 30 | 0.628 | 2.678 | 45 | 31 | 7 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 480 | -3.665 | 0 | 2 | 0.914 |
| baseline | prasa | 461 | -1.770 | 63 | 8 | 0.845 |
| baseline | yati | 2 | -3.268 | 0 | 0 | 0.877 |
| baseline | other | 1408 | -1.684 | 61 | 3 | 0.890 |
| masking_only | line_start | 3488 | -3.412 | 41 | 28 | 0.637 |
| masking_only | prasa | 3890 | -2.391 | 56 | 36 | 0.537 |
| masking_only | yati | 12016 | -3.913 | 35 | 58 | 0.364 |
| masking_only | other | 61790 | -2.184 | 57 | 25 | 0.684 |
| masking_backtrack | line_start | 3720 | -3.589 | 35 | 24 | 0.668 |
| masking_backtrack | prasa | 4147 | -2.546 | 52 | 36 | 0.521 |
| masking_backtrack | yati | 15383 | -3.709 | 31 | 53 | 0.394 |
| masking_backtrack | other | 80258 | -2.593 | 46 | 28 | 0.657 |
| hybrid | line_start | 4418 | -2.651 | 54 | 23 | 0.682 |
| hybrid | prasa | 3899 | -2.381 | 57 | 34 | 0.559 |
| hybrid | yati | 12526 | -3.929 | 32 | 61 | 0.344 |
| hybrid | other | 57320 | -2.226 | 55 | 24 | 0.691 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 0 / -0.92 / 85 | 100 / -1.85 / 83 | 100 / -1.75 / 83 | 100 / -1.81 / 82 |
| bhujangaprayatamu | 0 / -0.92 / 85 | 100 / -2.93 / 21 | 100 / -3.52 / 16 | 100 / -2.91 / 22 |
| champakamala | 0 / -0.92 / 85 | 100 / -2.56 / 43 | 100 / -2.25 / 59 | 100 / -2.68 / 35 |
| dvipada | 0 / -0.92 / 85 | 100 / -2.39 / 68 | 100 / -1.91 / 75 | 100 / -2.26 / 65 |
| hayapracara_ragada | 0 / -0.92 / 85 | 100 / -2.29 / 78 | 100 / -2.24 / 77 | 100 / -2.48 / 65 |
| indravajra | 0 / -0.92 / 85 | 100 / -2.82 / 26 | 100 / -3.55 / 20 | 93 / -2.42 / 15 |
| kandamu | 0 / -0.92 / 85 | 100 / -2.09 / 70 | 100 / -2.08 / 75 | 100 / -1.82 / 68 |
| kavirajavirajitamu | 0 / -0.92 / 85 | 100 / -2.42 / 50 | 100 / -2.86 / 53 | 100 / -2.76 / 46 |
| lalita | 0 / -0.92 / 85 | 100 / -2.87 / 24 | 100 / -3.21 / 22 | 93 / -2.40 / 14 |
| layagrahi | 0 / -0.92 / 85 | 100 / -2.19 / 38 | 100 / -2.51 / 48 | 100 / -2.45 / 43 |
| layavibhati | 0 / -0.92 / 85 | 100 / -1.97 / 74 | 100 / -2.29 / 70 | 100 / -2.13 / 72 |
| madhuragati_ragada | 0 / -0.92 / 85 | 100 / -2.26 / 80 | 100 / -2.27 / 76 | 100 / -2.35 / 67 |
| madhyakkara | 0 / -0.92 / 85 | 100 / -2.21 / 83 | 100 / -1.77 / 83 | 100 / -1.98 / 71 |
| mahasragdhara | 0 / -0.92 / 85 | 100 / -2.81 / 25 | 100 / -3.01 / 24 | 100 / -2.82 / 32 |
| malini | 0 / -0.92 / 85 | 100 / -2.85 / 33 | 100 / -3.00 / 30 | 100 / -3.00 / 34 |
| mangalamahasri | 0 / -0.92 / 85 | 100 / -2.65 / 55 | 100 / -2.81 / 51 | 100 / -2.63 / 52 |
| manini | 0 / -0.92 / 85 | 100 / -2.74 / 43 | 100 / -3.01 / 46 | 100 / -2.69 / 39 |
| mattakokilamu | 0 / -0.92 / 85 | 100 / -2.63 / 27 | 100 / -3.10 / 40 | 100 / -2.43 / 32 |
| mattebhavikriditamu | 0 / -0.92 / 85 | 100 / -2.63 / 27 | 100 / -2.92 / 27 | 100 / -2.85 / 29 |
| pamcacamaramu | 0 / -0.92 / 85 | 100 / -2.32 / 25 | 100 / -2.95 / 24 | 100 / -2.50 / 29 |
| rathoddhata | 0 / -0.92 / 85 | 100 / -2.81 / 38 | 100 / -2.88 / 35 | 100 / -2.98 / 43 |
| salini | 0 / -0.92 / 85 | 100 / -2.71 / 20 | 100 / -3.48 / 18 | 100 / -2.89 / 26 |
| sardulavikriditamu | 0 / -0.92 / 85 | 100 / -2.63 / 18 | 100 / -3.13 / 21 | 100 / -2.69 / 21 |
| seesamu | 0 / -0.92 / 85 | 100 / -1.68 / 85 | 100 / -1.82 / 84 | 100 / -1.76 / 78 |
| sragdhara | 0 / -0.92 / 85 | 100 / -2.63 / 25 | 100 / -3.24 / 18 | 100 / -2.73 / 28 |
| sragvini | 0 / -0.92 / 85 | 100 / -2.55 / 16 | 100 / -3.16 / 15 | 100 / -2.69 / 21 |
| taralamu | 0 / -0.92 / 85 | 100 / -2.76 / 38 | 100 / -2.92 / 43 | 100 / -2.82 / 36 |
| taruvoja | 0 / -0.92 / 85 | 100 / -2.35 / 78 | 100 / -2.09 / 82 | 100 / -2.29 / 65 |
| tetagiti | 0 / -0.92 / 85 | 100 / -2.04 / 79 | 100 / -2.04 / 78 | 100 / -1.83 / 79 |
| totakamu | 0 / -0.92 / 85 | 100 / -3.11 / 42 | 100 / -3.08 / 43 | 100 / -2.88 / 42 |
| turagagati_ragada | 0 / -0.92 / 85 | 100 / -1.84 / 81 | 100 / -1.96 / 79 | 100 / -1.82 / 71 |
| upendravajra | 0 / -0.92 / 85 | 100 / -2.78 / 22 | 100 / -3.69 / 24 | 100 / -2.87 / 26 |
| utpalamala | 0 / -0.92 / 85 | 100 / -2.58 / 37 | 100 / -2.84 / 46 | 100 / -2.56 / 32 |
| utsahamu | 0 / -0.92 / 85 | 100 / -2.12 / 70 | 100 / -2.24 / 78 | 100 / -2.02 / 74 |
| vanamayuramu | 0 / -0.92 / 85 | 100 / -2.72 / 47 | 100 / -2.91 / 44 | 100 / -2.51 / 54 |
| vasamtatilakamu | 0 / -0.92 / 85 | 100 / -2.88 / 28 | 100 / -3.15 / 32 | 100 / -2.93 / 31 |
| vidyunmala | 0 / -0.92 / 85 | 100 / -2.57 / 11 | 100 / -3.50 / 11 | 100 / -2.66 / 16 |

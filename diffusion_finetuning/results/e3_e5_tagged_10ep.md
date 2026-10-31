# Token choices under the constraint

Runs: `e3_e5_tagged_10ep`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 555 | 3 | 3 | 136 | -0.962 | 76 | 8 | 0.893 | 1.699 | 78 | 8 | 8 | 0.0 |
| masking_only | 555 | 100 | 100 | 130 | -2.480 | 56 | 26 | 0.668 | 2.626 | 47 | 25 | 17 | 0.0 |
| masking_backtrack | 555 | 99 | 99 | 165 | -2.689 | 47 | 27 | 0.655 | 2.919 | 51 | 23 | 10 | 21.1 |
| hybrid | 555 | 100 | 100 | 122 | -2.491 | 55 | 26 | 0.673 | 2.611 | 48 | 20 | 11 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 723 | -2.908 | 24 | 1 | 0.942 |
| baseline | prasa | 541 | -1.527 | 68 | 3 | 0.888 |
| baseline | yati | 111 | -1.420 | 54 | 1 | 0.924 |
| baseline | other | 4649 | -1.566 | 61 | 1 | 0.956 |
| masking_only | line_start | 4097 | -2.834 | 54 | 22 | 0.690 |
| masking_only | prasa | 3402 | -2.259 | 60 | 32 | 0.587 |
| masking_only | yati | 9677 | -4.031 | 38 | 52 | 0.399 |
| masking_only | other | 54749 | -2.193 | 59 | 21 | 0.719 |
| masking_backtrack | line_start | 4733 | -2.731 | 51 | 19 | 0.726 |
| masking_backtrack | prasa | 4067 | -2.244 | 58 | 31 | 0.575 |
| masking_backtrack | yati | 12458 | -3.691 | 32 | 47 | 0.433 |
| masking_backtrack | other | 70487 | -2.535 | 48 | 24 | 0.694 |
| hybrid | line_start | 3152 | -3.118 | 47 | 24 | 0.683 |
| hybrid | prasa | 3461 | -2.199 | 62 | 28 | 0.612 |
| hybrid | yati | 9905 | -4.074 | 36 | 54 | 0.389 |
| hybrid | other | 51336 | -2.167 | 58 | 20 | 0.732 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 0 / -1.34 / 89 | 100 / -1.81 / 79 | 100 / -1.78 / 83 | 100 / -1.71 / 82 |
| bhujangaprayatamu | 0 / -0.68 / 64 | 100 / -3.04 / 15 | 93 / -3.78 / 15 | 100 / -2.98 / 23 |
| champakamala | 27 / -1.41 / 66 | 100 / -1.83 / 60 | 100 / -1.46 / 62 | 100 / -1.35 / 60 |
| dvipada | 27 / -1.74 / 77 | 100 / -2.46 / 66 | 100 / -1.83 / 72 | 100 / -2.22 / 65 |
| hayapracara_ragada | 0 / -1.43 / 79 | 100 / -2.55 / 77 | 100 / -2.49 / 73 | 100 / -2.35 / 61 |
| indravajra | 0 / -1.03 / 45 | 93 / -2.58 / 15 | 100 / -3.57 / 16 | 100 / -2.96 / 20 |
| kandamu | 0 / -1.50 / 72 | 100 / -2.06 / 72 | 100 / -1.87 / 74 | 100 / -1.74 / 68 |
| kavirajavirajitamu | 0 / -0.92 / 87 | 100 / -2.72 / 41 | 100 / -2.78 / 45 | 100 / -2.81 / 45 |
| lalita | 0 / -1.11 / 85 | 100 / -3.03 / 23 | 100 / -3.20 / 16 | 100 / -3.13 / 30 |
| layagrahi | 0 / -0.93 / 79 | 100 / -2.25 / 37 | 100 / -2.33 / 38 | 100 / -2.38 / 38 |
| layavibhati | 0 / -0.61 / 90 | 100 / -1.91 / 59 | 100 / -2.33 / 66 | 100 / -2.14 / 62 |
| madhuragati_ragada | 0 / -0.64 / 88 | 100 / -2.56 / 74 | 100 / -2.63 / 73 | 100 / -2.40 / 62 |
| madhyakkara | 0 / -0.93 / 92 | 100 / -1.89 / 83 | 100 / -1.73 / 89 | 100 / -1.85 / 80 |
| mahasragdhara | 0 / -1.02 / 65 | 100 / -2.88 / 21 | 100 / -3.36 / 18 | 100 / -2.89 / 21 |
| malini | 0 / -1.28 / 83 | 100 / -2.88 / 29 | 100 / -3.09 / 29 | 100 / -2.76 / 34 |
| mangalamahasri | 0 / -0.58 / 89 | 100 / -2.32 / 32 | 93 / -2.55 / 33 | 100 / -2.40 / 40 |
| manini | 0 / -0.64 / 88 | 100 / -2.73 / 42 | 100 / -2.86 / 43 | 100 / -2.78 / 41 |
| mattakokilamu | 0 / -1.29 / 74 | 100 / -2.60 / 49 | 100 / -2.29 / 70 | 100 / -2.77 / 43 |
| mattebhavikriditamu | 0 / -1.28 / 62 | 100 / -2.11 / 54 | 100 / -1.62 / 52 | 100 / -2.18 / 47 |
| pamcacamaramu | 0 / -0.94 / 90 | 100 / -2.65 / 31 | 100 / -2.94 / 40 | 100 / -2.67 / 18 |
| rathoddhata | 0 / -1.07 / 83 | 100 / -2.95 / 29 | 100 / -3.04 / 41 | 100 / -3.05 / 38 |
| salini | 0 / -1.07 / 72 | 100 / -3.06 / 13 | 93 / -3.23 / 12 | 100 / -2.85 / 20 |
| sardulavikriditamu | 7 / -1.18 / 61 | 100 / -2.15 / 47 | 100 / -1.91 / 51 | 100 / -2.18 / 45 |
| seesamu | 0 / -0.91 / 76 | 100 / -1.97 / 80 | 100 / -2.04 / 82 | 100 / -1.88 / 72 |
| sragdhara | 0 / -0.81 / 62 | 100 / -2.87 / 29 | 100 / -3.46 / 23 | 100 / -2.87 / 29 |
| sragvini | 0 / -0.98 / 79 | 100 / -2.57 / 20 | 93 / -3.13 / 15 | 100 / -2.66 / 30 |
| taralamu | 0 / -0.89 / 79 | 100 / -2.83 / 36 | 100 / -2.56 / 58 | 100 / -3.01 / 40 |
| taruvoja | 0 / -0.70 / 86 | 100 / -2.35 / 77 | 100 / -2.39 / 76 | 100 / -2.37 / 66 |
| tetagiti | 0 / -1.46 / 83 | 100 / -1.98 / 75 | 100 / -1.76 / 81 | 100 / -1.97 / 72 |
| totakamu | 0 / -1.01 / 63 | 100 / -2.80 / 36 | 100 / -3.02 / 52 | 100 / -2.78 / 41 |
| turagagati_ragada | 0 / -1.24 / 87 | 100 / -1.85 / 85 | 100 / -2.07 / 85 | 100 / -1.79 / 70 |
| upendravajra | 0 / -0.77 / 66 | 100 / -3.20 / 15 | 100 / -3.37 / 20 | 100 / -3.22 / 23 |
| utpalamala | 33 / -1.36 / 63 | 100 / -1.81 / 65 | 100 / -1.80 / 64 | 100 / -1.67 / 61 |
| utsahamu | 0 / -0.72 / 90 | 100 / -2.08 / 82 | 100 / -1.96 / 84 | 100 / -1.93 / 80 |
| vanamayuramu | 0 / -0.82 / 81 | 93 / -2.15 / 24 | 100 / -2.78 / 39 | 100 / -2.90 / 43 |
| vasamtatilakamu | 0 / -1.22 / 79 | 100 / -3.11 / 26 | 100 / -3.15 / 22 | 100 / -2.59 / 27 |
| vidyunmala | 0 / -0.87 / 89 | 100 / -2.81 / 13 | 100 / -3.87 / 14 | 100 / -2.72 / 24 |

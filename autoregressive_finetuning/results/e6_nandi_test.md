# Token choices under the constraint

Runs: `e6_nandi_test`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 183 | 4 | 5 | 83 | -0.760 | 83 | 5 | 0.939 | 1.408 | 45 | 6 | 1 | 0.0 |
| masking_only | 183 | 100 | 100 | 82 | -1.786 | 70 | 16 | 0.839 | 1.525 | 42 | 13 | 0 | 0.0 |
| masking_backtrack | 183 | 100 | 100 | 107 | -1.442 | 71 | 13 | 0.863 | 1.443 | 43 | 12 | 0 | 11.8 |
| hybrid | 183 | 100 | 100 | 79 | -1.968 | 66 | 16 | 0.839 | 1.549 | 41 | 11 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 304 | -0.783 | 72 | 1 | 0.991 |
| baseline | prasa | 200 | -0.568 | 87 | 2 | 0.972 |
| baseline | yati | 110 | -0.698 | 90 | 2 | 0.951 |
| baseline | other | 2703 | -0.774 | 84 | 1 | 0.981 |
| masking_only | line_start | 652 | -1.028 | 77 | 3 | 0.961 |
| masking_only | prasa | 581 | -1.009 | 80 | 10 | 0.874 |
| masking_only | yati | 1303 | -4.845 | 45 | 47 | 0.515 |
| masking_only | other | 12393 | -1.540 | 72 | 13 | 0.865 |
| masking_backtrack | line_start | 658 | -0.974 | 77 | 3 | 0.964 |
| masking_backtrack | prasa | 591 | -0.768 | 83 | 7 | 0.911 |
| masking_backtrack | yati | 2306 | -2.451 | 58 | 31 | 0.660 |
| masking_backtrack | other | 16065 | -1.341 | 72 | 11 | 0.886 |
| hybrid | line_start | 643 | -1.150 | 72 | 3 | 0.958 |
| hybrid | prasa | 599 | -0.997 | 82 | 10 | 0.883 |
| hybrid | yati | 1329 | -5.130 | 42 | 49 | 0.493 |
| hybrid | other | 11795 | -1.705 | 68 | 13 | 0.870 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 13 / -0.67 / 58 | 100 / -1.35 / 59 | 100 / -1.10 / 61 | 100 / -1.49 / 55 |
| bhujangaprayatamu | 0 / -0.68 / 39 | 100 / -1.55 / 31 | 100 / -0.75 / 38 | 100 / -1.48 / 17 |
| champakamala | 0 / -0.76 / 53 | 100 / -1.26 / 45 | 100 / -0.87 / 48 | 100 / -1.13 / 44 |
| indravajra | 0 / -0.92 / 24 | 100 / -2.46 / 29 | 100 / -1.32 / 20 | 100 / -3.03 / 29 |
| kandamu | 27 / -0.78 / 48 | 100 / -1.09 / 45 | 100 / -1.12 / 45 | 100 / -1.27 / 46 |
| kavirajavirajitamu | 0 / -0.59 / 34 | 100 / -3.28 / 15 | 100 / -1.92 / 25 | 100 / -3.38 / 20 |
| layagrahi | 0 / -0.70 / 24 | 100 / -3.09 / 20 | 100 / -2.28 / 32 | 100 / -3.02 / 20 |
| layavibhati | 0 / -0.58 / 30 | 100 / -3.15 / 21 | 100 / -2.17 / 23 | 100 / -2.55 / 19 |
| madhuragati_ragada | 0 / -0.67 / 39 | 100 / -1.93 / 57 | 100 / -1.32 / 59 | 100 / -2.38 / 45 |
| mahasragdhara | 0 / -0.97 / 27 | 100 / -1.96 / 14 | 100 / -1.45 / 38 | 100 / -2.51 / 21 |
| malini | 0 / -0.63 / 7 | 100 / -1.38 / 7 | 100 / -0.98 / 6 | 100 / -1.31 / 1 |
| manini | 0 / -0.74 / 24 | 100 / -3.51 / 17 | 100 / -2.65 / 21 | 100 / -2.87 / 37 |
| mattakokilamu | 7 / -0.77 / 52 | 100 / -1.30 / 39 | 100 / -1.03 / 39 | 100 / -1.68 / 39 |
| mattebhavikriditamu | 0 / -0.68 / 39 | 100 / -1.44 / 35 | 100 / -0.98 / 37 | 100 / -1.70 / 33 |
| pamcacamaramu | 0 / -0.89 / 26 | 100 / -1.24 / 39 | 100 / -1.05 / 52 | 100 / -2.04 / 52 |
| sardulavikriditamu | 0 / -0.81 / 36 | 100 / -1.36 / 34 | 100 / -1.23 / 36 | 100 / -1.51 / 42 |
| seesamu | 0 / -0.91 / 54 | 100 / -3.04 / 55 | 100 / -2.61 / 51 | 100 / -3.21 / 51 |
| sragdhara | 0 / -0.67 / 27 | 100 / -2.48 / 9 | 100 / -1.76 / 27 | 100 / -2.97 / 28 |
| sragvini | 0 / -0.77 / 52 | 100 / -2.12 / 43 | 100 / -1.30 / 46 | 100 / -2.36 / 17 |
| tetagiti | 7 / -0.75 / 56 | 100 / -1.69 / 51 | 100 / -1.14 / 55 | 100 / -1.91 / 49 |
| totakamu | 0 / -0.72 / 18 | 100 / -1.18 / 22 | 100 / -0.86 / 10 | 100 / -2.25 / 39 |
| upendravajra | 0 / -0.67 / 35 | 100 / -2.66 / 33 | 100 / -1.27 / 31 | 100 / -2.69 / 36 |
| utpalamala | 7 / -0.71 / 52 | 100 / -0.95 / 47 | 100 / -0.88 / 45 | 100 / -1.25 / 44 |
| utsahamu | 0 / -0.62 / 46 | 100 / -1.18 / 51 | 100 / -1.25 / 46 | 100 / -1.77 / 47 |
| vanamayuramu | 0 / -0.64 / 53 | 100 / -2.57 / 40 | 100 / -1.00 / 19 | 100 / -2.98 / 35 |

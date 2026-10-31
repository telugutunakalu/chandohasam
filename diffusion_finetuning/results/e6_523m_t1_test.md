# Token choices under the constraint

Runs: `e6_523m_t1_test`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 183 | 1 | 1 | 100 | -0.963 | 75 | 6 | 0.924 | 1.845 | 57 | 7 | 0 | 0.0 |
| masking_only | 183 | 99 | 99 | 113 | -2.362 | 56 | 25 | 0.717 | 2.453 | 48 | 19 | 0 | 0.0 |
| masking_backtrack | 183 | 100 | 100 | 135 | -1.887 | 58 | 19 | 0.781 | 2.178 | 52 | 13 | 1 | 16.2 |
| hybrid | 183 | 100 | 100 | 106 | -2.268 | 56 | 23 | 0.743 | 2.416 | 47 | 13 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 281 | -1.267 | 49 | 0 | 0.982 |
| baseline | prasa | 184 | -0.632 | 93 | 1 | 0.967 |
| baseline | yati | 54 | -1.089 | 72 | 6 | 0.880 |
| baseline | other | 2140 | -0.890 | 78 | 1 | 0.974 |
| masking_only | line_start | 890 | -2.235 | 51 | 13 | 0.836 |
| masking_only | prasa | 749 | -1.285 | 75 | 16 | 0.780 |
| masking_only | yati | 2189 | -4.406 | 34 | 55 | 0.389 |
| masking_only | other | 16851 | -2.152 | 58 | 23 | 0.751 |
| masking_backtrack | line_start | 988 | -2.017 | 52 | 11 | 0.881 |
| masking_backtrack | prasa | 844 | -1.108 | 75 | 14 | 0.783 |
| masking_backtrack | yati | 3155 | -2.831 | 43 | 36 | 0.572 |
| masking_backtrack | other | 19794 | -1.764 | 60 | 17 | 0.809 |
| hybrid | line_start | 846 | -1.901 | 57 | 9 | 0.888 |
| hybrid | prasa | 744 | -1.313 | 74 | 13 | 0.801 |
| hybrid | yati | 2095 | -4.300 | 34 | 54 | 0.406 |
| hybrid | other | 15736 | -2.063 | 58 | 20 | 0.778 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 0 / -0.83 / 69 | 100 / -1.61 / 73 | 100 / -1.65 / 73 | 100 / -1.65 / 64 |
| bhujangaprayatamu | 0 / -1.25 / 39 | 100 / -3.83 / 25 | 100 / -3.06 / 5 | 100 / -3.85 / 30 |
| champakamala | 0 / -0.94 / 56 | 100 / -2.16 / 51 | 100 / -1.28 / 61 | 100 / -1.81 / 50 |
| indravajra | 0 / -1.16 / 39 | 100 / -3.11 / 30 | 100 / -2.80 / 32 | 100 / -3.21 / 34 |
| kandamu | 0 / -0.92 / 66 | 100 / -1.82 / 57 | 100 / -1.59 / 62 | 100 / -1.54 / 52 |
| kavirajavirajitamu | 0 / -1.19 / 55 | 100 / -2.70 / 37 | 100 / -2.80 / 30 | 100 / -2.65 / 27 |
| layagrahi | 0 / -1.16 / 46 | 100 / -2.42 / 28 | 100 / -2.44 / 27 | 100 / -2.52 / 35 |
| layavibhati | 0 / -0.81 / 56 | 100 / -1.94 / 28 | 100 / -2.16 / 59 | 100 / -2.80 / 50 |
| madhuragati_ragada | 0 / -0.85 / 63 | 100 / -2.42 / 54 | 100 / -2.48 / 49 | 100 / -2.15 / 59 |
| mahasragdhara | 0 / -1.30 / 54 | 100 / -3.33 / 26 | 100 / -3.04 / 32 | 100 / -3.65 / 18 |
| malini | 10 / -0.76 / 23 | 100 / -2.95 / 24 | 100 / -1.89 / 10 | 100 / -2.82 / 21 |
| manini | 0 / -0.95 / 69 | 0 / -2.86 / 48 | 100 / -2.73 / 35 | 100 / -2.84 / 44 |
| mattakokilamu | 0 / -0.86 / 61 | 100 / -2.69 / 48 | 100 / -2.12 / 48 | 100 / -2.47 / 47 |
| mattebhavikriditamu | 0 / -0.96 / 48 | 100 / -2.96 / 34 | 100 / -1.76 / 41 | 100 / -2.72 / 37 |
| pamcacamaramu | 0 / -0.93 / 71 | 100 / -2.01 / 59 | 100 / -1.23 / 63 | 100 / -1.59 / 50 |
| sardulavikriditamu | 0 / -1.12 / 50 | 100 / -2.66 / 38 | 100 / -1.52 / 42 | 100 / -2.43 / 37 |
| seesamu | 0 / -1.05 / 60 | 100 / -1.95 / 56 | 100 / -1.88 / 60 | 100 / -2.13 / 57 |
| sragdhara | 0 / -1.39 / 42 | 100 / -3.56 / 28 | 100 / -2.85 / 26 | 100 / -3.59 / 22 |
| sragvini | 0 / -1.25 / 59 | 100 / -3.39 / 33 | 100 / -2.62 / 33 | 100 / -2.75 / 30 |
| tetagiti | 0 / -0.76 / 65 | 100 / -1.58 / 66 | 100 / -1.57 / 67 | 100 / -1.83 / 57 |
| totakamu | 0 / -0.43 / 60 | 100 / -2.40 / 55 | 100 / -1.94 / 58 | 100 / -1.94 / 57 |
| upendravajra | 0 / -1.16 / 36 | 100 / -2.25 / 38 | 100 / -3.92 / 6 | 100 / -3.29 / 42 |
| utpalamala | 0 / -0.91 / 60 | 100 / -1.63 / 48 | 100 / -1.37 / 55 | 100 / -1.41 / 49 |
| utsahamu | 0 / -1.02 / 68 | 100 / -2.12 / 70 | 100 / -1.94 / 62 | 100 / -2.07 / 61 |
| vanamayuramu | 0 / -1.06 / 50 | 100 / -3.27 / 41 | 100 / -2.15 / 41 | 100 / -2.93 / 35 |

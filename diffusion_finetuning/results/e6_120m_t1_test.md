# Token choices under the constraint

Runs: `e6_120m_t1_test`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 183 | 0 | 0 | 98 | -1.203 | 71 | 9 | 0.887 | 2.231 | 61 | 8 | 0 | 0.0 |
| masking_only | 183 | 99 | 99 | 122 | -2.879 | 50 | 29 | 0.659 | 2.963 | 47 | 16 | 0 | 0.0 |
| masking_backtrack | 183 | 99 | 99 | 150 | -2.377 | 50 | 24 | 0.725 | 2.634 | 50 | 13 | 0 | 19.3 |
| hybrid | 183 | 99 | 99 | 115 | -2.789 | 50 | 27 | 0.682 | 2.908 | 44 | 12 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 208 | -1.647 | 30 | 1 | 0.982 |
| baseline | prasa | 159 | -0.835 | 89 | 1 | 0.960 |
| baseline | yati | 12 | -1.252 | 83 | 0 | 0.827 |
| baseline | other | 1414 | -1.115 | 74 | 2 | 0.950 |
| masking_only | line_start | 851 | -2.426 | 46 | 11 | 0.854 |
| masking_only | prasa | 769 | -1.528 | 72 | 16 | 0.767 |
| masking_only | yati | 2552 | -4.846 | 31 | 57 | 0.340 |
| masking_only | other | 18243 | -2.681 | 51 | 27 | 0.690 |
| masking_backtrack | line_start | 902 | -2.286 | 47 | 10 | 0.872 |
| masking_backtrack | prasa | 824 | -1.365 | 71 | 15 | 0.775 |
| masking_backtrack | yati | 3602 | -3.402 | 35 | 46 | 0.471 |
| masking_backtrack | other | 22048 | -2.251 | 52 | 21 | 0.758 |
| hybrid | line_start | 862 | -2.438 | 48 | 12 | 0.848 |
| hybrid | prasa | 761 | -1.565 | 72 | 16 | 0.756 |
| hybrid | yati | 2590 | -4.689 | 34 | 55 | 0.350 |
| hybrid | other | 16878 | -2.571 | 52 | 24 | 0.721 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 0 / -1.10 / 75 | 100 / -1.85 / 72 | 100 / -1.87 / 74 | 100 / -1.83 / 67 |
| bhujangaprayatamu | 0 / -1.47 / 57 | 100 / -4.04 / 17 | 100 / -3.86 / 10 | 100 / -3.89 / 12 |
| champakamala | 0 / -1.20 / 59 | 100 / -2.98 / 47 | 100 / -1.64 / 50 | 100 / -2.66 / 44 |
| indravajra | 0 / -1.33 / 52 | 100 / -3.55 / 23 | 100 / -3.70 / 42 | 100 / -3.73 / 32 |
| kandamu | 0 / -1.15 / 69 | 100 / -2.06 / 67 | 100 / -1.90 / 68 | 100 / -2.01 / 52 |
| kavirajavirajitamu | 0 / -0.89 / 31 | 100 / -2.95 / 22 | 100 / -3.10 / 24 | 100 / -3.01 / 25 |
| layagrahi | 0 / -1.17 / 53 | 75 / -2.89 / 13 | 75 / -3.00 / 22 | 75 / -2.96 / 12 |
| layavibhati | 0 / -1.29 / 47 | 100 / -2.48 / 51 | 100 / -2.23 / 23 | 100 / -2.48 / 40 |
| madhuragati_ragada | 0 / -0.82 / 72 | 100 / -2.23 / 67 | 100 / -2.08 / 67 | 100 / -2.43 / 58 |
| mahasragdhara | 0 / -1.65 / 45 | 100 / -3.54 / 18 | 100 / -3.52 / 20 | 100 / -3.77 / 17 |
| malini | 0 / -1.33 / 41 | 100 / -3.52 / 28 | 100 / -2.90 / 27 | 100 / -3.53 / 22 |
| manini | 0 / -1.26 / 46 | 100 / -2.99 / 10 | 100 / -3.02 / 21 | 100 / -2.93 / 15 |
| mattakokilamu | 0 / -1.12 / 67 | 100 / -3.28 / 40 | 100 / -2.52 / 47 | 100 / -3.06 / 41 |
| mattebhavikriditamu | 0 / -1.12 / 50 | 100 / -3.59 / 27 | 100 / -2.47 / 36 | 100 / -3.50 / 29 |
| pamcacamaramu | 0 / -1.54 / 62 | 100 / -3.78 / 33 | 100 / -2.10 / 54 | 100 / -2.70 / 53 |
| sardulavikriditamu | 0 / -1.34 / 54 | 100 / -3.47 / 34 | 100 / -2.38 / 43 | 100 / -3.36 / 34 |
| seesamu | 0 / -1.35 / 65 | 100 / -2.16 / 65 | 100 / -2.23 / 64 | 100 / -2.04 / 62 |
| sragdhara | 0 / -1.68 / 46 | 100 / -3.76 / 22 | 100 / -3.72 / 24 | 100 / -3.65 / 27 |
| sragvini | 0 / -1.11 / 70 | 100 / -3.42 / 23 | 100 / -3.17 / 23 | 100 / -3.46 / 16 |
| tetagiti | 0 / -1.03 / 72 | 100 / -1.77 / 65 | 100 / -1.90 / 67 | 100 / -1.91 / 62 |
| totakamu | 0 / -0.56 / 91 | 100 / -2.87 / 33 | 100 / -1.95 / 47 | 100 / -2.87 / 47 |
| upendravajra | 0 / -1.08 / 50 | 100 / -3.96 / 17 | 100 / -3.67 / 6 | 100 / -3.41 / 14 |
| utpalamala | 0 / -1.09 / 61 | 100 / -2.39 / 52 | 100 / -1.48 / 51 | 100 / -2.35 / 49 |
| utsahamu | 0 / -1.49 / 68 | 100 / -2.48 / 65 | 100 / -2.46 / 63 | 100 / -2.49 / 57 |
| vanamayuramu | 0 / -1.16 / 67 | 100 / -3.78 / 28 | 100 / -3.18 / 32 | 100 / -3.62 / 19 |

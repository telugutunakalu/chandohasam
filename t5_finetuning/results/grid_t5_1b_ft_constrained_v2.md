# Token choices under the constraint

Runs: `grid_t5_1b_ft_constrained_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 100 | 100 | 100 | 99 | -1.597 | 62 | 12 | 0.861 | 2.154 | 49 | 5 | 1 | 7.3 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 537 | -1.514 | 63 | 4 | 0.935 |
| masking_backtrack | prasa | 362 | -1.250 | 75 | 12 | 0.823 |
| masking_backtrack | yati | 1077 | -2.324 | 47 | 34 | 0.610 |
| masking_backtrack | other | 7883 | -1.520 | 64 | 9 | 0.892 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.17 / 66 |
| bhujangaprayatamu | 100 / -2.94 / 28 |
| champakamala | 100 / -1.10 / 56 |
| indravajra | 100 / -3.11 / 11 |
| kandamu | 100 / -1.21 / 55 |
| layagrahi | 100 / -2.71 / 30 |
| layavibhati | 100 / -2.62 / 42 |
| madhuragati_ragada | 100 / -2.38 / 59 |
| mahasragdhara | 100 / -1.73 / 26 |
| malini | 100 / -1.74 / 25 |
| manini | 100 / -3.47 / 19 |
| mattakokilamu | 100 / -1.29 / 56 |
| mattebhavikriditamu | 100 / -1.21 / 46 |
| pamcacamaramu | 100 / -1.36 / 46 |
| sardulavikriditamu | 100 / -1.36 / 39 |
| seesamu | 100 / -2.21 / 48 |
| sragdhara | 100 / -1.80 / 41 |
| sragvini | 100 / -2.16 / 31 |
| tetagiti | 100 / -1.31 / 59 |
| totakamu | 100 / -2.46 / 23 |
| upendravajra | 100 / -3.30 / 0 |
| utpalamala | 100 / -1.11 / 54 |
| utsahamu | 100 / -1.54 / 42 |
| vanamayuramu | 100 / -3.20 / 12 |

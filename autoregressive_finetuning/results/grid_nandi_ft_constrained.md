# Token choices under the constraint

Runs: `grid_nandi_ft_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 183 | 100 | 100 | 106 | -1.469 | 70 | 13 | 0.858 | 1.506 | 42 | 12 | 0 | 11.3 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 710 | -1.092 | 75 | 4 | 0.946 |
| masking_backtrack | prasa | 652 | -0.841 | 82 | 8 | 0.900 |
| masking_backtrack | yati | 2370 | -2.278 | 62 | 28 | 0.682 |
| masking_backtrack | other | 15645 | -1.390 | 70 | 12 | 0.879 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -0.96 / 51 |
| bhujangaprayatamu | 100 / -1.15 / 29 |
| champakamala | 100 / -0.88 / 46 |
| indravajra | 100 / -1.21 / 15 |
| kandamu | 100 / -0.98 / 50 |
| kavirajavirajitamu | 100 / -2.37 / 29 |
| layagrahi | 100 / -1.94 / 27 |
| layavibhati | 100 / -2.65 / 12 |
| madhuragati_ragada | 100 / -1.92 / 26 |
| mahasragdhara | 100 / -1.64 / 32 |
| malini | 100 / -1.04 / 6 |
| manini | 100 / -2.34 / 17 |
| mattakokilamu | 100 / -1.05 / 40 |
| mattebhavikriditamu | 100 / -1.01 / 38 |
| pamcacamaramu | 100 / -1.01 / 28 |
| sardulavikriditamu | 100 / -1.24 / 42 |
| seesamu | 100 / -2.64 / 52 |
| sragdhara | 100 / -1.90 / 21 |
| sragvini | 100 / -1.46 / 25 |
| tetagiti | 100 / -1.10 / 48 |
| totakamu | 100 / -1.00 / 9 |
| upendravajra | 100 / -1.33 / 36 |
| utpalamala | 100 / -1.00 / 44 |
| utsahamu | 100 / -1.09 / 39 |
| vanamayuramu | 100 / -1.21 / 27 |

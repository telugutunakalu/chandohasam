# Token choices under the constraint

Runs: `grid_nandi_ft_constrained_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 100 | 100 | 100 | 91 | -1.294 | 71 | 11 | 0.886 | 1.565 | 45 | 6 | 0 | 7.8 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 430 | -1.317 | 71 | 10 | 0.903 |
| masking_backtrack | prasa | 384 | -0.901 | 80 | 7 | 0.914 |
| masking_backtrack | yati | 969 | -1.740 | 61 | 27 | 0.699 |
| masking_backtrack | other | 7360 | -1.254 | 72 | 9 | 0.909 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.18 / 57 |
| bhujangaprayatamu | 100 / -1.35 / 29 |
| champakamala | 100 / -1.01 / 48 |
| indravajra | 100 / -2.24 / 31 |
| kandamu | 100 / -1.03 / 56 |
| layagrahi | 100 / -2.06 / 34 |
| layavibhati | 100 / -2.37 / 50 |
| madhuragati_ragada | 100 / -1.91 / 21 |
| mahasragdhara | 100 / -1.14 / 40 |
| malini | 100 / -1.16 / 18 |
| manini | 100 / -2.05 / 25 |
| mattakokilamu | 100 / -1.07 / 49 |
| mattebhavikriditamu | 100 / -1.02 / 36 |
| pamcacamaramu | 100 / -0.93 / 42 |
| sardulavikriditamu | 100 / -1.09 / 44 |
| seesamu | 100 / -2.72 / 41 |
| sragdhara | 100 / -1.36 / 23 |
| sragvini | 100 / -1.55 / 22 |
| tetagiti | 100 / -1.27 / 54 |
| totakamu | 100 / -1.10 / 38 |
| upendravajra | 100 / -2.46 / 26 |
| utpalamala | 100 / -1.00 / 46 |
| utsahamu | 100 / -1.15 / 51 |
| vanamayuramu | 100 / -1.91 / 56 |

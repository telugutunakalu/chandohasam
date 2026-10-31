# Token choices under the constraint

Runs: `grid_gemma4_26b_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 34 | 100 | 100 | 160 | -1.897 | 59 | 30 | 0.686 | 1.353 | 20 | 11 | 38 | 26.4 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 178 | -1.247 | 65 | 13 | 0.865 |
| masking_backtrack | prasa | 194 | -1.261 | 78 | 19 | 0.731 |
| masking_backtrack | yati | 716 | -2.888 | 46 | 46 | 0.513 |
| masking_backtrack | other | 4361 | -1.789 | 60 | 29 | 0.704 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| bhujangaprayatamu | 100 / -1.95 / 12 |
| champakamala | 100 / -1.46 / 50 |
| indravajra | 100 / -1.96 / 17 |
| layagrahi | 100 / -1.41 / 11 |
| layavibhati | 100 / -1.13 / 38 |
| madhuragati_ragada | 100 / -2.12 / 25 |
| mahasragdhara | 100 / -2.07 / 28 |
| malini | 100 / -2.01 / 13 |
| manini | 100 / -0.36 / 62 |
| mattakokilamu | 100 / -1.86 / 22 |
| mattebhavikriditamu | 100 / -1.65 / 9 |
| pamcacamaramu | 100 / -2.10 / 0 |
| sardulavikriditamu | 100 / -2.87 / 14 |
| sragdhara | 100 / -1.79 / 9 |
| sragvini | 100 / -2.08 / 38 |
| totakamu | 100 / -2.68 / 24 |
| upendravajra | 100 / -2.15 / 0 |
| utsahamu | 100 / -2.72 / 23 |
| vanamayuramu | 100 / -2.12 / 8 |

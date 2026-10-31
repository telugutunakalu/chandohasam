# Token choices under the constraint

Runs: `grid_t5_4b_base_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 34 | 100 | 100 | 162 | -2.773 | 42 | 41 | 0.545 | 3.179 | 17 | 20 | 26 | 21.2 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 257 | -3.319 | 30 | 37 | 0.432 |
| masking_backtrack | prasa | 163 | -3.359 | 35 | 60 | 0.309 |
| masking_backtrack | yati | 748 | -3.225 | 36 | 56 | 0.387 |
| masking_backtrack | other | 4340 | -2.640 | 44 | 38 | 0.588 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| bhujangaprayatamu | 100 / -3.46 / 0 |
| champakamala | 100 / -2.80 / 14 |
| indravajra | 100 / -2.56 / 0 |
| layagrahi | 100 / -2.19 / 14 |
| layavibhati | 100 / -2.11 / 17 |
| madhuragati_ragada | 100 / -2.87 / 41 |
| mahasragdhara | 100 / -2.11 / 0 |
| malini | 100 / -3.28 / 10 |
| manini | 100 / -2.88 / 40 |
| mattakokilamu | 100 / -3.08 / 18 |
| mattebhavikriditamu | 100 / -3.10 / 14 |
| pamcacamaramu | 100 / -2.43 / 8 |
| sardulavikriditamu | 100 / -3.13 / 14 |
| sragdhara | 100 / -2.22 / 12 |
| sragvini | 100 / -3.29 / 12 |
| totakamu | 100 / -3.30 / 7 |
| upendravajra | 100 / -1.90 / 22 |
| utsahamu | 100 / -2.77 / 11 |
| vanamayuramu | 100 / -2.97 / 21 |

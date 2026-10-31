# Token choices under the constraint

Runs: `grid_t5_1b_base_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 183 | 100 | 100 | 156 | -2.944 | 40 | 40 | 0.556 | 3.379 | 18 | 13 | 21 | 22.9 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 1287 | -3.581 | 21 | 43 | 0.493 |
| masking_backtrack | prasa | 676 | -3.567 | 33 | 65 | 0.281 |
| masking_backtrack | yati | 4194 | -3.584 | 32 | 57 | 0.387 |
| masking_backtrack | other | 22458 | -2.769 | 43 | 36 | 0.599 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -3.27 / 29 |
| bhujangaprayatamu | 100 / -2.21 / 0 |
| champakamala | 100 / -3.10 / 16 |
| indravajra | 100 / -3.05 / 2 |
| kandamu | 100 / -2.73 / 27 |
| kavirajavirajitamu | 100 / -2.83 / 9 |
| layagrahi | 100 / -2.46 / 5 |
| layavibhati | 100 / -2.95 / 3 |
| madhuragati_ragada | 100 / -3.55 / 44 |
| mahasragdhara | 100 / -3.12 / 4 |
| malini | 100 / -2.95 / 3 |
| manini | 100 / -3.44 / 20 |
| mattakokilamu | 100 / -2.86 / 14 |
| mattebhavikriditamu | 100 / -3.10 / 12 |
| pamcacamaramu | 100 / -3.27 / 14 |
| sardulavikriditamu | 100 / -3.08 / 8 |
| seesamu | 100 / -2.51 / 20 |
| sragdhara | 100 / -2.91 / 13 |
| sragvini | 100 / -3.71 / 12 |
| tetagiti | 100 / -2.76 / 34 |
| totakamu | 100 / -3.09 / 4 |
| upendravajra | 100 / -2.16 / 0 |
| utpalamala | 100 / -3.06 / 18 |
| utsahamu | 100 / -3.13 / 19 |
| vanamayuramu | 100 / -2.86 / 19 |

# Token choices under the constraint

Runs: `grid_gemma4_26b_constrained_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 100 | 100 | 100 | 154 | -2.058 | 59 | 30 | 0.685 | 1.299 | 34 | 7 | 29 | 26.3 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 494 | -0.986 | 73 | 7 | 0.924 |
| masking_backtrack | prasa | 405 | -1.203 | 78 | 19 | 0.787 |
| masking_backtrack | yati | 2029 | -2.848 | 47 | 47 | 0.516 |
| masking_backtrack | other | 12504 | -2.000 | 60 | 28 | 0.700 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -2.05 / 48 |
| bhujangaprayatamu | 100 / -2.11 / 6 |
| champakamala | 100 / -2.03 / 33 |
| indravajra | 100 / -1.46 / 25 |
| kandamu | 100 / -1.54 / 56 |
| layagrahi | 100 / -1.22 / 28 |
| layavibhati | 100 / -2.37 / 35 |
| madhuragati_ragada | 100 / -1.84 / 61 |
| mahasragdhara | 100 / -0.65 / 20 |
| malini | 100 / -2.47 / 13 |
| manini | 100 / -0.22 / 75 |
| mattakokilamu | 100 / -2.37 / 19 |
| mattebhavikriditamu | 100 / -1.78 / 27 |
| pamcacamaramu | 100 / -2.93 / 0 |
| sardulavikriditamu | 100 / -2.01 / 17 |
| seesamu | 100 / -1.94 / 44 |
| sragdhara | 100 / -1.56 / 0 |
| sragvini | 100 / -2.14 / 15 |
| tetagiti | 100 / -2.44 / 50 |
| totakamu | 100 / -2.27 / 29 |
| upendravajra | 100 / -2.09 / 0 |
| utpalamala | 100 / -2.68 / 29 |
| utsahamu | 100 / -1.75 / 40 |
| vanamayuramu | 100 / -2.77 / 17 |

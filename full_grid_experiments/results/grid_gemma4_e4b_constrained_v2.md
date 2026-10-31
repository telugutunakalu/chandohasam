# Token choices under the constraint

Runs: `grid_gemma4_e4b_constrained_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 100 | 100 | 100 | 160 | -2.507 | 46 | 40 | 0.582 | 1.826 | 25 | 5 | 17 | 26.5 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 1138 | -2.772 | 41 | 36 | 0.613 |
| masking_backtrack | prasa | 382 | -4.518 | 33 | 63 | 0.353 |
| masking_backtrack | yati | 1799 | -3.208 | 37 | 54 | 0.436 |
| masking_backtrack | other | 12698 | -2.323 | 48 | 38 | 0.607 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -2.22 / 45 |
| bhujangaprayatamu | 100 / -3.08 / 0 |
| champakamala | 100 / -2.68 / 24 |
| indravajra | 100 / -2.84 / 25 |
| kandamu | 100 / -2.65 / 38 |
| layagrahi | 100 / -2.17 / 7 |
| layavibhati | 100 / -2.80 / 25 |
| madhuragati_ragada | 100 / -1.52 / 58 |
| mahasragdhara | 100 / -3.05 / 4 |
| malini | 100 / -2.81 / 13 |
| manini | 100 / -2.91 / 0 |
| mattakokilamu | 100 / -2.55 / 17 |
| mattebhavikriditamu | 100 / -2.52 / 8 |
| pamcacamaramu | 100 / -2.88 / 13 |
| sardulavikriditamu | 100 / -2.36 / 4 |
| seesamu | 100 / -1.91 / 53 |
| sragdhara | 100 / -2.09 / 8 |
| sragvini | 100 / -2.00 / 23 |
| tetagiti | 100 / -2.12 / 40 |
| totakamu | 100 / -2.70 / 12 |
| upendravajra | 100 / -2.56 / 20 |
| utpalamala | 100 / -2.94 / 18 |
| utsahamu | 100 / -2.31 / 33 |
| vanamayuramu | 100 / -2.27 / 25 |

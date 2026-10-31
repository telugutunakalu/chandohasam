# Token choices under the constraint

Runs: `grid_t5_4b_48k_constrained_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 100 | 100 | 100 | 122 | -2.444 | 46 | 25 | 0.700 | 3.022 | 46 | 6 | 1 | 12.1 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 652 | -2.298 | 48 | 8 | 0.840 |
| masking_backtrack | prasa | 543 | -1.670 | 65 | 25 | 0.650 |
| masking_backtrack | yati | 1097 | -3.082 | 35 | 49 | 0.429 |
| masking_backtrack | other | 9887 | -2.425 | 46 | 24 | 0.723 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.91 / 72 |
| bhujangaprayatamu | 100 / -3.81 / 8 |
| champakamala | 100 / -1.79 / 50 |
| indravajra | 100 / -3.32 / 7 |
| kandamu | 100 / -1.85 / 51 |
| layagrahi | 100 / -2.93 / 32 |
| layavibhati | 100 / -2.74 / 32 |
| madhuragati_ragada | 100 / -2.84 / 65 |
| mahasragdhara | 100 / -3.31 / 24 |
| malini | 100 / -3.29 / 22 |
| manini | 100 / -2.97 / 27 |
| mattakokilamu | 100 / -2.98 / 27 |
| mattebhavikriditamu | 100 / -2.04 / 43 |
| pamcacamaramu | 100 / -3.04 / 13 |
| sardulavikriditamu | 100 / -2.24 / 34 |
| seesamu | 100 / -0.33 / 97 |
| sragdhara | 100 / -2.95 / 14 |
| sragvini | 100 / -3.28 / 16 |
| tetagiti | 100 / -2.04 / 62 |
| totakamu | 100 / -3.40 / 25 |
| upendravajra | 100 / -3.78 / 0 |
| utpalamala | 100 / -1.92 / 50 |
| utsahamu | 100 / -2.36 / 46 |
| vanamayuramu | 100 / -3.19 / 45 |

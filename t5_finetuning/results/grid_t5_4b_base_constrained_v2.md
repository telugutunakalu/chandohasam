# Token choices under the constraint

Runs: `grid_t5_4b_base_constrained_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 100 | 100 | 100 | 143 | -2.589 | 45 | 37 | 0.581 | 3.010 | 25 | 7 | 37 | 17.6 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 789 | -3.494 | 28 | 42 | 0.457 |
| masking_backtrack | prasa | 414 | -3.119 | 40 | 58 | 0.331 |
| masking_backtrack | yati | 1536 | -2.910 | 41 | 49 | 0.466 |
| masking_backtrack | other | 11557 | -2.466 | 47 | 34 | 0.614 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -2.73 / 38 |
| bhujangaprayatamu | 100 / -2.50 / 0 |
| champakamala | 100 / -2.63 / 17 |
| indravajra | 100 / -2.37 / 0 |
| kandamu | 100 / -2.70 / 35 |
| layagrahi | 100 / -2.39 / 25 |
| layavibhati | 100 / -0.92 / 0 |
| madhuragati_ragada | 100 / -3.67 / 47 |
| mahasragdhara | 100 / -2.20 / 14 |
| malini | 100 / -2.66 / 35 |
| manini | 100 / -2.82 / 9 |
| mattakokilamu | 100 / -2.46 / 12 |
| mattebhavikriditamu | 100 / -2.50 / 18 |
| pamcacamaramu | 100 / -2.71 / 14 |
| sardulavikriditamu | 100 / -2.68 / 13 |
| seesamu | 100 / -2.11 / 12 |
| sragdhara | 100 / -2.82 / 6 |
| sragvini | 100 / -2.56 / 0 |
| tetagiti | 100 / -2.94 / 40 |
| totakamu | 100 / -2.73 / 19 |
| upendravajra | 100 / -3.19 / 0 |
| utpalamala | 100 / -2.35 / 16 |
| utsahamu | 100 / -2.67 / 33 |
| vanamayuramu | 100 / -3.04 / 6 |

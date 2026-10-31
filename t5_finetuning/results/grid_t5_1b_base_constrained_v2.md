# Token choices under the constraint

Runs: `grid_t5_1b_base_constrained_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 100 | 100 | 100 | 140 | -3.006 | 38 | 43 | 0.529 | 3.442 | 27 | 6 | 26 | 19.4 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 776 | -3.636 | 22 | 45 | 0.462 |
| masking_backtrack | prasa | 425 | -3.625 | 31 | 71 | 0.256 |
| masking_backtrack | yati | 1472 | -3.573 | 28 | 59 | 0.359 |
| masking_backtrack | other | 11353 | -2.866 | 41 | 40 | 0.566 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -3.10 / 43 |
| bhujangaprayatamu | 100 / -2.76 / 14 |
| champakamala | 100 / -2.90 / 16 |
| indravajra | 100 / -2.16 / 0 |
| kandamu | 100 / -3.28 / 33 |
| layagrahi | 100 / -2.08 / 29 |
| layavibhati | 100 / -1.72 / 12 |
| madhuragati_ragada | 100 / -3.51 / 54 |
| mahasragdhara | 100 / -3.94 / 0 |
| malini | 100 / -2.85 / 15 |
| manini | 100 / -3.19 / 28 |
| mattakokilamu | 100 / -2.70 / 23 |
| mattebhavikriditamu | 100 / -3.03 / 18 |
| pamcacamaramu | 100 / -3.66 / 0 |
| sardulavikriditamu | 100 / -2.91 / 10 |
| seesamu | 100 / -2.34 / 59 |
| sragdhara | 100 / -3.45 / 9 |
| sragvini | 100 / -3.53 / 6 |
| tetagiti | 100 / -3.27 / 44 |
| totakamu | 100 / -3.65 / 14 |
| upendravajra | 100 / -3.33 / 25 |
| utpalamala | 100 / -2.97 / 11 |
| utsahamu | 100 / -3.25 / 32 |
| vanamayuramu | 100 / -3.69 / 33 |

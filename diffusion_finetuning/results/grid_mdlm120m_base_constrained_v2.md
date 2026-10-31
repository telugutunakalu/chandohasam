# Token choices under the constraint

Runs: `grid_mdlm120m_base_constrained_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 100 | 100 | 100 | 185 | -2.369 | 48 | 35 | 0.581 | 2.443 | 40 | 10 | 8 | 26.1 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 633 | -3.325 | 35 | 26 | 0.592 |
| masking_backtrack | prasa | 573 | -2.534 | 50 | 45 | 0.458 |
| masking_backtrack | yati | 2185 | -3.082 | 35 | 51 | 0.415 |
| masking_backtrack | other | 15087 | -2.219 | 50 | 32 | 0.610 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.96 / 71 |
| bhujangaprayatamu | 100 / -3.28 / 0 |
| champakamala | 100 / -2.39 / 37 |
| indravajra | 100 / -3.43 / 7 |
| kandamu | 100 / -2.03 / 63 |
| layagrahi | 100 / -2.16 / 27 |
| layavibhati | 100 / -2.41 / 66 |
| madhuragati_ragada | 100 / -2.14 / 65 |
| mahasragdhara | 100 / -2.53 / 35 |
| malini | 100 / -2.64 / 28 |
| manini | 100 / -2.23 / 40 |
| mattakokilamu | 100 / -2.47 / 32 |
| mattebhavikriditamu | 100 / -2.43 / 21 |
| pamcacamaramu | 100 / -2.72 / 18 |
| sardulavikriditamu | 100 / -2.58 / 12 |
| seesamu | 100 / -1.22 / 59 |
| sragdhara | 100 / -2.45 / 27 |
| sragvini | 100 / -2.81 / 12 |
| tetagiti | 100 / -1.93 / 53 |
| totakamu | 100 / -2.79 / 44 |
| upendravajra | 100 / -2.44 / 0 |
| utpalamala | 100 / -2.38 / 39 |
| utsahamu | 100 / -2.48 / 40 |
| vanamayuramu | 100 / -2.71 / 6 |

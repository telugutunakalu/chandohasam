# Token choices under the constraint

Runs: `grid_mdlm120m_base_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 183 | 89 | 89 | 206 | -2.222 | 52 | 30 | 0.631 | 2.349 | 48 | 27 | 7 | 26.1 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 1402 | -3.093 | 39 | 23 | 0.610 |
| masking_backtrack | prasa | 1112 | -2.332 | 56 | 42 | 0.479 |
| masking_backtrack | yati | 5049 | -2.798 | 42 | 42 | 0.510 |
| masking_backtrack | other | 30205 | -2.082 | 55 | 28 | 0.657 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -2.23 / 66 |
| bhujangaprayatamu | 100 / -2.51 / 4 |
| champakamala | 93 / -2.41 / 45 |
| indravajra | 100 / -2.74 / 30 |
| kandamu | 100 / -2.18 / 67 |
| kavirajavirajitamu | 100 / -1.98 / 36 |
| layagrahi | 25 / -1.87 / 48 |
| layavibhati | 100 / -2.18 / 47 |
| madhuragati_ragada | 100 / -2.18 / 65 |
| mahasragdhara | 50 / -2.32 / 26 |
| malini | 100 / -2.19 / 50 |
| manini | 100 / -2.00 / 62 |
| mattakokilamu | 100 / -2.34 / 38 |
| mattebhavikriditamu | 60 / -2.19 / 31 |
| pamcacamaramu | 100 / -2.36 / 19 |
| sardulavikriditamu | 47 / -2.32 / 23 |
| seesamu | 100 / -1.88 / 67 |
| sragdhara | 67 / -2.22 / 24 |
| sragvini | 100 / -2.64 / 28 |
| tetagiti | 100 / -1.93 / 65 |
| totakamu | 100 / -2.69 / 51 |
| upendravajra | 100 / -2.91 / 7 |
| utpalamala | 93 / -2.29 / 31 |
| utsahamu | 100 / -2.06 / 71 |
| vanamayuramu | 100 / -2.46 / 32 |

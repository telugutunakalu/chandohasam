# Token choices under the constraint

Runs: `grid_t5_270m_base_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 183 | 100 | 100 | 156 | -2.718 | 51 | 40 | 0.568 | 2.903 | 16 | 11 | 39 | 23.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 1621 | -3.362 | 38 | 36 | 0.433 |
| masking_backtrack | prasa | 748 | -3.582 | 36 | 67 | 0.297 |
| masking_backtrack | yati | 4009 | -3.235 | 42 | 53 | 0.443 |
| masking_backtrack | other | 22234 | -2.549 | 54 | 37 | 0.609 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -3.26 / 22 |
| bhujangaprayatamu | 100 / -2.90 / 14 |
| champakamala | 100 / -2.87 / 10 |
| indravajra | 100 / -3.02 / 12 |
| kandamu | 100 / -2.82 / 27 |
| kavirajavirajitamu | 100 / -1.81 / 5 |
| layagrahi | 100 / -2.42 / 13 |
| layavibhati | 100 / -2.94 / 12 |
| madhuragati_ragada | 100 / -3.29 / 29 |
| mahasragdhara | 100 / -2.68 / 17 |
| malini | 100 / -2.98 / 10 |
| manini | 100 / -2.84 / 9 |
| mattakokilamu | 100 / -2.71 / 9 |
| mattebhavikriditamu | 100 / -2.69 / 8 |
| pamcacamaramu | 100 / -3.24 / 19 |
| sardulavikriditamu | 100 / -2.77 / 11 |
| seesamu | 100 / -2.45 / 22 |
| sragdhara | 100 / -2.30 / 6 |
| sragvini | 100 / -2.80 / 35 |
| tetagiti | 100 / -2.68 / 19 |
| totakamu | 100 / -3.00 / 24 |
| upendravajra | 100 / -3.24 / 0 |
| utpalamala | 100 / -2.55 / 17 |
| utsahamu | 100 / -2.47 / 19 |
| vanamayuramu | 100 / -3.04 / 6 |

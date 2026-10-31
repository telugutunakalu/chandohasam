# Token choices under the constraint

Runs: `grid_t5_4b_ft_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 34 | 97 | 97 | 124 | -2.108 | 53 | 22 | 0.744 | 2.574 | 34 | 11 | 0 | 12.3 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 230 | -1.689 | 54 | 7 | 0.880 |
| masking_backtrack | prasa | 187 | -1.691 | 61 | 30 | 0.626 |
| masking_backtrack | yati | 645 | -2.961 | 40 | 45 | 0.482 |
| masking_backtrack | other | 3165 | -1.989 | 55 | 18 | 0.794 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| bhujangaprayatamu | 100 / -2.19 / 17 |
| champakamala | 100 / -1.18 / 50 |
| indravajra | 100 / -1.97 / 0 |
| layagrahi | 50 / -2.41 / 16 |
| layavibhati | 100 / -2.95 / 33 |
| madhuragati_ragada | 100 / -2.29 / 61 |
| mahasragdhara | 100 / -2.76 / 32 |
| malini | 100 / -1.73 / 0 |
| manini | 100 / -3.00 / 14 |
| mattakokilamu | 100 / -1.27 / 47 |
| mattebhavikriditamu | 100 / -1.47 / 41 |
| pamcacamaramu | 100 / -1.29 / 42 |
| sardulavikriditamu | 100 / -1.18 / 37 |
| sragdhara | 100 / -2.42 / 14 |
| sragvini | 100 / -2.37 / 38 |
| totakamu | 100 / -2.66 / 35 |
| upendravajra | 100 / -3.11 / 8 |
| utsahamu | 100 / -1.09 / 71 |
| vanamayuramu | 100 / -3.09 / 0 |

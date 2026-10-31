# Token choices under the constraint

Runs: `grid_t5_4b_48k_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 34 | 100 | 100 | 172 | -3.095 | 37 | 39 | 0.559 | 3.249 | 24 | 12 | 0 | 25.4 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 221 | -2.279 | 42 | 12 | 0.828 |
| masking_backtrack | prasa | 237 | -2.186 | 60 | 40 | 0.531 |
| masking_backtrack | yati | 947 | -4.069 | 23 | 66 | 0.318 |
| masking_backtrack | other | 4429 | -2.976 | 39 | 35 | 0.598 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| bhujangaprayatamu | 100 / -3.76 / 0 |
| champakamala | 100 / -2.20 / 20 |
| indravajra | 100 / -4.16 / 0 |
| layagrahi | 100 / -2.81 / 18 |
| layavibhati | 100 / -2.76 / 34 |
| madhuragati_ragada | 100 / -2.65 / 59 |
| mahasragdhara | 100 / -3.30 / 19 |
| malini | 100 / -3.43 / 26 |
| manini | 100 / -2.97 / 23 |
| mattakokilamu | 100 / -2.98 / 27 |
| mattebhavikriditamu | 100 / -2.26 / 40 |
| pamcacamaramu | 100 / -3.14 / 0 |
| sardulavikriditamu | 100 / -1.73 / 35 |
| sragdhara | 100 / -3.43 / 3 |
| sragvini | 100 / -3.84 / 12 |
| totakamu | 100 / -3.47 / 29 |
| upendravajra | 100 / -3.71 / 18 |
| utsahamu | 100 / -2.34 / 25 |
| vanamayuramu | 100 / -3.06 / 24 |

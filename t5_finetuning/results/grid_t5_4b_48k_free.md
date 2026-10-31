# Token choices under the constraint

Runs: `grid_t5_4b_48k_free`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 34 | 0 | 0 | 89 | -1.579 | 63 | 22 | 0.749 | 2.875 | 37 | 7 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 31 | -2.016 | 16 | 6 | 0.920 |
| baseline | prasa | 20 | -1.592 | 70 | 10 | 0.845 |
| baseline | other | 63 | -1.551 | 70 | 3 | 0.862 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| bhujangaprayatamu | 0 / -1.63 / 19 |
| champakamala | 0 / -1.38 / 43 |
| indravajra | 0 / -1.72 / 17 |
| layagrahi | 0 / -1.67 / 27 |
| layavibhati | 0 / -1.66 / 39 |
| madhuragati_ragada | 0 / -1.44 / 53 |
| mahasragdhara | 0 / -1.88 / 50 |
| malini | 0 / -1.44 / 23 |
| manini | 0 / -1.83 / 42 |
| mattakokilamu | 0 / -1.53 / 34 |
| mattebhavikriditamu | 0 / -1.58 / 39 |
| pamcacamaramu | 0 / -1.54 / 48 |
| sardulavikriditamu | 0 / -1.68 / 32 |
| sragdhara | 0 / -1.86 / 36 |
| sragvini | 0 / -1.38 / 59 |
| totakamu | 0 / -1.68 / 16 |
| upendravajra | 0 / -1.56 / 62 |
| utsahamu | 0 / -1.80 / 56 |
| vanamayuramu | 0 / -1.45 / 15 |

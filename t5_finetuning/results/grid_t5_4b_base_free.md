# Token choices under the constraint

Runs: `grid_t5_4b_base_free`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 34 | 0 | 0 | 79 | -0.866 | 79 | 68 | 0.471 | 1.641 | 46 | 9 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 8 | -2.821 | 12 | 75 | 0.589 |
| baseline | prasa | 5 | -1.603 | 80 | 20 | 0.765 |
| baseline | other | 3 | -0.421 | 67 | 0 | 0.974 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| bhujangaprayatamu | 0 / -1.32 / 45 |
| champakamala | 0 / – / – |
| indravajra | 0 / – / – |
| layagrahi | 0 / -0.55 / 55 |
| layavibhati | 0 / -0.57 / 42 |
| madhuragati_ragada | 0 / -0.54 / 43 |
| mahasragdhara | 0 / -1.16 / – |
| malini | 0 / -1.07 / 44 |
| manini | 0 / -1.18 / – |
| mattakokilamu | 0 / -1.00 / 44 |
| mattebhavikriditamu | 0 / -1.31 / 24 |
| pamcacamaramu | 0 / – / – |
| sardulavikriditamu | 0 / -1.03 / 100 |
| sragdhara | 0 / -1.04 / 34 |
| sragvini | 0 / -1.03 / – |
| totakamu | 0 / -0.66 / 73 |
| upendravajra | 0 / – / – |
| utsahamu | 0 / – / – |
| vanamayuramu | 0 / – / – |

# Token choices under the constraint

Runs: `grid_gemma4_e4b_free`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 34 | 0 | 0 | 76 | -0.712 | 81 | 35 | 0.657 | 1.268 | 44 | 5 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 32 | -1.054 | 53 | 3 | 0.948 |
| baseline | prasa | 18 | -0.458 | 100 | 0 | 0.921 |
| baseline | other | 22 | -1.135 | 68 | 14 | 0.820 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| bhujangaprayatamu | 0 / -1.27 / 7 |
| champakamala | 0 / -0.95 / 59 |
| indravajra | 0 / -0.83 / 48 |
| layagrahi | 0 / -0.34 / 33 |
| layavibhati | 0 / -0.60 / 36 |
| madhuragati_ragada | 0 / -0.58 / 33 |
| mahasragdhara | 0 / -0.50 / 42 |
| malini | 0 / -0.65 / 56 |
| manini | 0 / -0.75 / 43 |
| mattakokilamu | 0 / -0.66 / 50 |
| mattebhavikriditamu | 0 / -0.75 / 51 |
| pamcacamaramu | 0 / -0.60 / 17 |
| sardulavikriditamu | 0 / -0.91 / 42 |
| sragdhara | 0 / -0.87 / 31 |
| sragvini | 0 / -1.09 / 60 |
| totakamu | 0 / -0.58 / 48 |
| upendravajra | 0 / -0.79 / 52 |
| utsahamu | 0 / -0.67 / 47 |
| vanamayuramu | 0 / -1.05 / 28 |

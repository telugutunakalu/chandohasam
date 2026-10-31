# Token choices under the constraint

Runs: `grid_gemma4_26b_free`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 34 | 0 | 0 | 67 | -0.546 | 85 | 32 | 0.675 | 1.030 | 52 | 4 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 32 | -0.828 | 53 | 9 | 0.926 |
| baseline | prasa | 17 | -0.227 | 100 | 0 | 0.948 |
| baseline | other | 31 | -0.420 | 87 | 6 | 0.910 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| bhujangaprayatamu | 0 / -0.77 / 71 |
| champakamala | 0 / -0.58 / 59 |
| indravajra | 0 / -0.62 / 71 |
| layagrahi | 0 / -0.50 / 42 |
| layavibhati | 0 / -0.27 / 41 |
| madhuragati_ragada | 0 / -0.71 / 64 |
| mahasragdhara | 0 / -0.37 / 29 |
| malini | 0 / -0.48 / 61 |
| manini | 0 / -0.53 / 47 |
| mattakokilamu | 0 / -0.60 / 55 |
| mattebhavikriditamu | 0 / -0.49 / 50 |
| pamcacamaramu | 0 / -0.86 / 48 |
| sardulavikriditamu | 0 / -0.58 / 50 |
| sragdhara | 0 / -0.47 / 38 |
| sragvini | 0 / -0.47 / 59 |
| totakamu | 0 / -0.84 / 60 |
| upendravajra | 0 / -0.59 / 53 |
| utsahamu | 0 / -0.45 / 47 |
| vanamayuramu | 0 / -0.41 / 50 |

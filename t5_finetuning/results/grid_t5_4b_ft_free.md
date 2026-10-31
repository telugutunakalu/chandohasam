# Token choices under the constraint

Runs: `grid_t5_4b_ft_free`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 34 | 0 | 0 | 84 | -1.241 | 71 | 7 | 0.911 | 2.195 | 45 | 7 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 49 | -1.520 | 43 | 4 | 0.950 |
| baseline | prasa | 37 | -0.827 | 86 | 0 | 0.955 |
| baseline | yati | 13 | -1.297 | 77 | 0 | 0.876 |
| baseline | other | 314 | -1.263 | 68 | 0 | 0.978 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| bhujangaprayatamu | 0 / -1.32 / 50 |
| champakamala | 0 / -1.16 / 62 |
| indravajra | 0 / -0.41 / 80 |
| layagrahi | 0 / -1.27 / 42 |
| layavibhati | 0 / -1.12 / 56 |
| madhuragati_ragada | 0 / -1.39 / 54 |
| mahasragdhara | 0 / -1.47 / 32 |
| malini | 0 / -1.57 / 21 |
| manini | 0 / -1.47 / 56 |
| mattakokilamu | 0 / -1.03 / 52 |
| mattebhavikriditamu | 0 / -1.05 / 47 |
| pamcacamaramu | 0 / -1.30 / 49 |
| sardulavikriditamu | 0 / -1.20 / 30 |
| sragdhara | 0 / -1.24 / 32 |
| sragvini | 0 / -1.58 / 25 |
| totakamu | 0 / -1.27 / 45 |
| upendravajra | 0 / -1.46 / 71 |
| utsahamu | 0 / -1.18 / 55 |
| vanamayuramu | 0 / -0.95 / 42 |

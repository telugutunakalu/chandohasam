# Token choices under the constraint

Runs: `grid_t5_1b_base_free`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 366 | 0 | 0 | 228 | -0.616 | 87 | 62 | 0.535 | 1.208 | 42 | 9 | 11 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 83 | -2.251 | 46 | 48 | 0.634 |
| baseline | prasa | 38 | -2.291 | 58 | 29 | 0.758 |
| baseline | other | 131 | -1.686 | 71 | 6 | 0.838 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -0.63 / 41 |
| bhujangaprayatamu | 0 / -0.75 / 42 |
| champakamala | 0 / -0.85 / 42 |
| indravajra | 0 / -0.42 / 23 |
| kandamu | 0 / -0.47 / 46 |
| kavirajavirajitamu | 0 / -0.49 / 35 |
| layagrahi | 0 / -0.64 / 22 |
| layavibhati | 0 / -0.62 / 60 |
| madhuragati_ragada | 0 / -0.62 / 48 |
| mahasragdhara | 0 / -0.57 / 27 |
| malini | 0 / -0.55 / 63 |
| manini | 0 / -0.57 / 33 |
| mattakokilamu | 0 / -0.53 / 30 |
| mattebhavikriditamu | 0 / -0.59 / 45 |
| pamcacamaramu | 0 / -0.86 / 51 |
| sardulavikriditamu | 0 / -0.88 / 47 |
| seesamu | 0 / -0.68 / 32 |
| sragdhara | 0 / -0.35 / 41 |
| sragvini | 0 / -0.60 / 22 |
| tetagiti | 0 / -0.52 / 48 |
| totakamu | 0 / -0.56 / 59 |
| upendravajra | 0 / -1.08 / 25 |
| utpalamala | 0 / -0.76 / 41 |
| utsahamu | 0 / -0.56 / 34 |
| vanamayuramu | 0 / -0.27 / 46 |

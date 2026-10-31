# Token choices under the constraint

Runs: `grid_t5_270m_base_free`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 366 | 0 | 0 | 252 | -0.351 | 94 | 86 | 0.192 | 0.772 | 40 | 6 | 23 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 676 | -0.377 | 93 | 88 | 0.114 |
| baseline | prasa | 8 | -1.090 | 100 | 25 | 0.726 |
| baseline | other | 104 | -1.612 | 76 | 40 | 0.590 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -0.42 / 37 |
| bhujangaprayatamu | 0 / -0.35 / 9 |
| champakamala | 0 / -0.48 / 35 |
| indravajra | 0 / -0.28 / 26 |
| kandamu | 0 / -0.30 / 43 |
| kavirajavirajitamu | 0 / -0.25 / 48 |
| layagrahi | 0 / -0.19 / 26 |
| layavibhati | 0 / -0.56 / 22 |
| madhuragati_ragada | 0 / -0.28 / 37 |
| mahasragdhara | 0 / -0.26 / 11 |
| malini | 0 / -0.21 / 76 |
| manini | 0 / -0.67 / 21 |
| mattakokilamu | 0 / -0.36 / 50 |
| mattebhavikriditamu | 0 / -0.40 / 35 |
| pamcacamaramu | 0 / -0.34 / 68 |
| sardulavikriditamu | 0 / -0.44 / 40 |
| seesamu | 0 / -0.34 / 34 |
| sragdhara | 0 / -0.23 / 24 |
| sragvini | 0 / -0.28 / 60 |
| tetagiti | 0 / -0.30 / 36 |
| totakamu | 0 / -0.20 / 17 |
| upendravajra | 0 / -0.31 / 27 |
| utpalamala | 0 / -0.51 / 35 |
| utsahamu | 0 / -0.31 / 40 |
| vanamayuramu | 0 / -0.23 / 36 |

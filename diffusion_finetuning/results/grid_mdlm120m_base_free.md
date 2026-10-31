# Token choices under the constraint

Runs: `grid_mdlm120m_base_free`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 366 | 0 | 0 | 281 | -0.755 | 81 | 29 | 0.642 | 1.377 | 50 | 7 | 3 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 767 | -1.966 | 49 | 31 | 0.605 |
| baseline | prasa | 214 | -1.573 | 80 | 20 | 0.692 |
| baseline | other | 760 | -1.307 | 75 | 8 | 0.837 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -0.66 / 42 |
| bhujangaprayatamu | 0 / -0.58 / 50 |
| champakamala | 0 / -0.85 / 47 |
| indravajra | 0 / -0.75 / 51 |
| kandamu | 0 / -0.64 / 53 |
| kavirajavirajitamu | 0 / -0.79 / 44 |
| layagrahi | 0 / -0.80 / 53 |
| layavibhati | 0 / -0.84 / 43 |
| madhuragati_ragada | 0 / -0.69 / 44 |
| mahasragdhara | 0 / -0.89 / 45 |
| malini | 0 / -0.77 / 56 |
| manini | 0 / -0.98 / 48 |
| mattakokilamu | 0 / -0.81 / 57 |
| mattebhavikriditamu | 0 / -0.77 / 52 |
| pamcacamaramu | 0 / -0.61 / 59 |
| sardulavikriditamu | 0 / -0.95 / 48 |
| seesamu | 0 / -0.77 / 56 |
| sragdhara | 0 / -0.76 / 25 |
| sragvini | 0 / -0.51 / 39 |
| tetagiti | 0 / -0.65 / 50 |
| totakamu | 0 / -0.75 / 50 |
| upendravajra | 0 / -0.58 / 33 |
| utpalamala | 0 / -0.87 / 51 |
| utsahamu | 0 / -0.70 / 34 |
| vanamayuramu | 0 / -0.74 / 31 |

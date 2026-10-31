# Token choices under the constraint

Runs: `grid_mdlm120m_ft_free`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 366 | 0 | 0 | 98 | -1.164 | 71 | 8 | 0.899 | 2.178 | 60 | 7 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 457 | -1.511 | 60 | 0 | 0.981 |
| baseline | prasa | 327 | -0.739 | 94 | 0 | 0.960 |
| baseline | yati | 35 | -1.225 | 71 | 0 | 0.875 |
| baseline | other | 3096 | -1.067 | 76 | 1 | 0.958 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -1.13 / 76 |
| bhujangaprayatamu | 0 / -1.36 / 46 |
| champakamala | 3 / -1.14 / 59 |
| indravajra | 0 / -1.24 / 41 |
| kandamu | 0 / -1.11 / 70 |
| kavirajavirajitamu | 0 / -0.96 / 52 |
| layagrahi | 0 / -1.25 / 46 |
| layavibhati | 0 / -1.15 / 58 |
| madhuragati_ragada | 0 / -0.76 / 70 |
| mahasragdhara | 0 / -1.64 / 45 |
| malini | 0 / -1.32 / 50 |
| manini | 0 / -0.78 / 78 |
| mattakokilamu | 0 / -1.10 / 60 |
| mattebhavikriditamu | 0 / -1.21 / 52 |
| pamcacamaramu | 0 / -1.41 / 63 |
| sardulavikriditamu | 0 / -1.38 / 50 |
| seesamu | 0 / -1.14 / 65 |
| sragdhara | 0 / -1.60 / 44 |
| sragvini | 0 / -0.99 / 75 |
| tetagiti | 0 / -1.13 / 68 |
| totakamu | 0 / -1.12 / 85 |
| upendravajra | 0 / -1.34 / 54 |
| utpalamala | 0 / -1.05 / 59 |
| utsahamu | 0 / -1.10 / 68 |
| vanamayuramu | 0 / -1.26 / 41 |

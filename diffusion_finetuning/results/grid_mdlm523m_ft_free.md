# Token choices under the constraint

Runs: `grid_mdlm523m_ft_free`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 366 | 1 | 1 | 101 | -0.967 | 75 | 7 | 0.920 | 1.847 | 58 | 7 | 1 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 497 | -1.280 | 63 | 0 | 0.987 |
| baseline | prasa | 358 | -0.596 | 94 | 0 | 0.970 |
| baseline | yati | 64 | -1.205 | 72 | 6 | 0.890 |
| baseline | other | 3822 | -0.864 | 80 | 1 | 0.973 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -0.87 / 74 |
| bhujangaprayatamu | 0 / -1.30 / 49 |
| champakamala | 0 / -0.97 / 60 |
| indravajra | 0 / -0.74 / 65 |
| kandamu | 3 / -0.94 / 63 |
| kavirajavirajitamu | 0 / -0.95 / 61 |
| layagrahi | 0 / -1.08 / 49 |
| layavibhati | 0 / -1.13 / 52 |
| madhuragati_ragada | 0 / -0.57 / 83 |
| mahasragdhara | 0 / -1.36 / 41 |
| malini | 0 / -0.93 / 20 |
| manini | 0 / -0.74 / 31 |
| mattakokilamu | 0 / -0.90 / 64 |
| mattebhavikriditamu | 0 / -0.98 / 47 |
| pamcacamaramu | 25 / -0.90 / 48 |
| sardulavikriditamu | 0 / -1.14 / 45 |
| seesamu | 0 / -1.02 / 61 |
| sragdhara | 0 / -1.02 / 59 |
| sragvini | 0 / -1.10 / 51 |
| tetagiti | 0 / -0.81 / 62 |
| totakamu | 0 / -0.76 / 58 |
| upendravajra | 0 / -1.05 / 63 |
| utpalamala | 0 / -0.91 / 62 |
| utsahamu | 0 / -1.23 / 70 |
| vanamayuramu | 0 / -0.96 / 58 |

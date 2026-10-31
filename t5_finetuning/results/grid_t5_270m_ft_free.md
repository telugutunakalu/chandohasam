# Token choices under the constraint

Runs: `grid_t5_270m_ft_free`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 366 | 8 | 8 | 91 | -1.164 | 80 | 4 | 0.954 | 2.061 | 45 | 5 | 1 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 945 | -1.033 | 80 | 0 | 0.992 |
| baseline | prasa | 458 | -0.771 | 91 | 1 | 0.963 |
| baseline | yati | 390 | -1.162 | 80 | 3 | 0.921 |
| baseline | other | 7141 | -1.139 | 81 | 1 | 0.984 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 30 / -1.07 / 58 |
| bhujangaprayatamu | 0 / -1.42 / 36 |
| champakamala | 0 / -1.10 / 48 |
| indravajra | 0 / -1.37 / 33 |
| kandamu | 37 / -1.08 / 51 |
| kavirajavirajitamu | 0 / -1.12 / 34 |
| layagrahi | 0 / -1.36 / 36 |
| layavibhati | 0 / -1.38 / 43 |
| madhuragati_ragada | 0 / -1.24 / 42 |
| mahasragdhara | 0 / -1.23 / 44 |
| malini | 0 / -1.38 / 7 |
| manini | 0 / -1.32 / 26 |
| mattakokilamu | 10 / -1.10 / 49 |
| mattebhavikriditamu | 10 / -1.06 / 40 |
| pamcacamaramu | 0 / -1.22 / 43 |
| sardulavikriditamu | 0 / -1.18 / 38 |
| seesamu | 0 / -1.14 / 51 |
| sragdhara | 0 / -1.61 / 26 |
| sragvini | 0 / -1.23 / 51 |
| tetagiti | 13 / -1.03 / 48 |
| totakamu | 0 / -1.51 / 20 |
| upendravajra | 0 / -1.07 / 42 |
| utpalamala | 0 / -1.09 / 49 |
| utsahamu | 10 / -1.23 / 49 |
| vanamayuramu | 0 / -1.44 / 33 |

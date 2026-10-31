# Token choices under the constraint

Runs: `grid_t5_1b_ft_free`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 366 | 7 | 7 | 90 | -1.002 | 74 | 4 | 0.953 | 1.825 | 45 | 6 | 1 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 878 | -0.992 | 72 | 0 | 0.992 |
| baseline | prasa | 425 | -0.661 | 88 | 1 | 0.975 |
| baseline | yati | 331 | -1.120 | 68 | 1 | 0.940 |
| baseline | other | 6670 | -0.990 | 76 | 0 | 0.985 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 30 / -0.95 / 57 |
| bhujangaprayatamu | 0 / -1.20 / 44 |
| champakamala | 3 / -1.00 / 48 |
| indravajra | 0 / -1.25 / 35 |
| kandamu | 23 / -0.98 / 51 |
| kavirajavirajitamu | 0 / -1.04 / 33 |
| layagrahi | 0 / -1.02 / 42 |
| layavibhati | 0 / -1.07 / 30 |
| madhuragati_ragada | 0 / -1.03 / 52 |
| mahasragdhara | 0 / -1.12 / 30 |
| malini | 0 / -0.94 / 19 |
| manini | 0 / -1.12 / 34 |
| mattakokilamu | 3 / -0.98 / 40 |
| mattebhavikriditamu | 0 / -0.90 / 41 |
| pamcacamaramu | 0 / -1.32 / 48 |
| sardulavikriditamu | 3 / -1.02 / 39 |
| seesamu | 0 / -1.03 / 54 |
| sragdhara | 0 / -1.06 / 28 |
| sragvini | 0 / -1.36 / 48 |
| tetagiti | 17 / -0.88 / 50 |
| totakamu | 0 / -1.03 / 36 |
| upendravajra | 0 / -1.06 / 52 |
| utpalamala | 3 / -0.97 / 52 |
| utsahamu | 0 / -1.08 / 55 |
| vanamayuramu | 0 / -1.16 / 45 |

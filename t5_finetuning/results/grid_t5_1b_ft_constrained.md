# Token choices under the constraint

Runs: `grid_t5_1b_ft_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 183 | 99 | 99 | 109 | -1.725 | 62 | 15 | 0.833 | 2.133 | 41 | 6 | 1 | 9.6 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 831 | -1.559 | 60 | 3 | 0.948 |
| masking_backtrack | prasa | 586 | -1.190 | 73 | 10 | 0.853 |
| masking_backtrack | yati | 2837 | -2.615 | 50 | 36 | 0.583 |
| masking_backtrack | other | 15673 | -1.592 | 63 | 11 | 0.871 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.15 / 56 |
| bhujangaprayatamu | 100 / -2.66 / 20 |
| champakamala | 100 / -1.10 / 52 |
| indravajra | 100 / -2.83 / 11 |
| kandamu | 100 / -1.06 / 53 |
| kavirajavirajitamu | 100 / -3.32 / 14 |
| layagrahi | 100 / -2.78 / 7 |
| layavibhati | 100 / -2.44 / 14 |
| madhuragati_ragada | 100 / -2.05 / 29 |
| mahasragdhara | 100 / -2.58 / 33 |
| malini | 100 / -1.42 / 7 |
| manini | 100 / -3.37 / 26 |
| mattakokilamu | 93 / -1.08 / 44 |
| mattebhavikriditamu | 100 / -1.27 / 36 |
| pamcacamaramu | 100 / -1.46 / 40 |
| sardulavikriditamu | 100 / -1.46 / 36 |
| seesamu | 100 / -2.21 / 42 |
| sragdhara | 100 / -2.34 / 17 |
| sragvini | 100 / -2.70 / 31 |
| tetagiti | 100 / -1.19 / 52 |
| totakamu | 100 / -2.80 / 21 |
| upendravajra | 100 / -3.29 / 23 |
| utpalamala | 100 / -1.18 / 50 |
| utsahamu | 100 / -1.45 / 52 |
| vanamayuramu | 100 / -3.28 / 0 |

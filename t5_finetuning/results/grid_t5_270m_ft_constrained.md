# Token choices under the constraint

Runs: `grid_t5_270m_ft_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 183 | 100 | 100 | 107 | -1.789 | 68 | 15 | 0.837 | 2.173 | 42 | 6 | 1 | 8.7 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 877 | -1.627 | 71 | 3 | 0.950 |
| masking_backtrack | prasa | 618 | -1.141 | 85 | 11 | 0.852 |
| masking_backtrack | yati | 2421 | -2.805 | 48 | 41 | 0.548 |
| masking_backtrack | other | 15624 | -1.666 | 70 | 11 | 0.875 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.20 / 56 |
| bhujangaprayatamu | 100 / -2.34 / 23 |
| champakamala | 100 / -1.17 / 54 |
| indravajra | 100 / -2.08 / 22 |
| kandamu | 100 / -1.09 / 50 |
| kavirajavirajitamu | 100 / -3.17 / 19 |
| layagrahi | 100 / -2.56 / 15 |
| layavibhati | 100 / -3.06 / 31 |
| madhuragati_ragada | 100 / -2.09 / 44 |
| mahasragdhara | 100 / -2.08 / 43 |
| malini | 100 / -1.78 / 4 |
| manini | 100 / -2.84 / 34 |
| mattakokilamu | 100 / -1.34 / 48 |
| mattebhavikriditamu | 100 / -1.27 / 39 |
| pamcacamaramu | 100 / -1.43 / 50 |
| sardulavikriditamu | 100 / -1.49 / 36 |
| seesamu | 100 / -2.56 / 38 |
| sragdhara | 100 / -2.47 / 17 |
| sragvini | 100 / -1.87 / 14 |
| tetagiti | 100 / -1.23 / 57 |
| totakamu | 100 / -2.95 / 26 |
| upendravajra | 100 / -2.38 / 10 |
| utpalamala | 100 / -1.35 / 48 |
| utsahamu | 100 / -1.47 / 41 |
| vanamayuramu | 100 / -2.06 / 23 |

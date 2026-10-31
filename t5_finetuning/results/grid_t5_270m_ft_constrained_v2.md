# Token choices under the constraint

Runs: `grid_t5_270m_ft_constrained_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 100 | 100 | 100 | 95 | -1.607 | 71 | 10 | 0.883 | 2.283 | 51 | 5 | 2 | 5.6 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 550 | -1.709 | 70 | 7 | 0.912 |
| masking_backtrack | prasa | 388 | -1.248 | 79 | 13 | 0.834 |
| masking_backtrack | yati | 948 | -2.003 | 63 | 29 | 0.658 |
| masking_backtrack | other | 7618 | -1.569 | 71 | 7 | 0.911 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.36 / 69 |
| bhujangaprayatamu | 100 / -2.53 / 10 |
| champakamala | 100 / -1.20 / 57 |
| indravajra | 100 / -2.63 / 42 |
| kandamu | 100 / -1.23 / 60 |
| layagrahi | 100 / -2.10 / 38 |
| layavibhati | 100 / -2.91 / 31 |
| madhuragati_ragada | 100 / -2.35 / 67 |
| mahasragdhara | 100 / -2.00 / 45 |
| malini | 100 / -1.54 / 6 |
| manini | 100 / -2.44 / 42 |
| mattakokilamu | 100 / -1.55 / 52 |
| mattebhavikriditamu | 100 / -1.34 / 47 |
| pamcacamaramu | 100 / -1.49 / 42 |
| sardulavikriditamu | 100 / -1.37 / 45 |
| seesamu | 100 / -2.23 / 62 |
| sragdhara | 100 / -2.04 / 25 |
| sragvini | 100 / -2.42 / 32 |
| tetagiti | 100 / -1.53 / 55 |
| totakamu | 100 / -2.50 / 32 |
| upendravajra | 100 / -2.73 / 27 |
| utpalamala | 100 / -1.10 / 59 |
| utsahamu | 100 / -1.89 / 40 |
| vanamayuramu | 100 / -2.27 / 33 |

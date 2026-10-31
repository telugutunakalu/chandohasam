# Token choices under the constraint

Runs: `grid_t5_4b_ft_constrained_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 100 | 100 | 100 | 98 | -1.686 | 60 | 12 | 0.853 | 2.305 | 49 | 6 | 0 | 5.9 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 571 | -1.657 | 58 | 6 | 0.923 |
| masking_backtrack | prasa | 411 | -1.214 | 73 | 16 | 0.789 |
| masking_backtrack | yati | 1061 | -2.512 | 43 | 36 | 0.573 |
| masking_backtrack | other | 7789 | -1.600 | 61 | 9 | 0.890 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.59 / 61 |
| bhujangaprayatamu | 100 / -2.09 / 23 |
| champakamala | 100 / -1.38 / 54 |
| indravajra | 100 / -2.04 / 0 |
| kandamu | 100 / -1.49 / 57 |
| layagrahi | 100 / -2.90 / 40 |
| layavibhati | 100 / -2.98 / 40 |
| madhuragati_ragada | 100 / -2.11 / 56 |
| mahasragdhara | 100 / -2.55 / 41 |
| malini | 100 / -1.75 / 8 |
| manini | 100 / -2.37 / 26 |
| mattakokilamu | 100 / -1.31 / 54 |
| mattebhavikriditamu | 100 / -1.33 / 43 |
| pamcacamaramu | 100 / -1.43 / 57 |
| sardulavikriditamu | 100 / -1.21 / 47 |
| seesamu | 100 / -1.31 / 42 |
| sragdhara | 100 / -1.92 / 22 |
| sragvini | 100 / -2.46 / 13 |
| tetagiti | 100 / -1.40 / 59 |
| totakamu | 100 / -2.44 / 42 |
| upendravajra | 100 / -3.49 / 27 |
| utpalamala | 100 / -1.31 / 56 |
| utsahamu | 100 / -1.21 / 45 |
| vanamayuramu | 100 / -3.08 / 11 |

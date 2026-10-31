# Token choices under the constraint

Runs: `grid_mdlm120m_ft_constrained_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 100 | 100 | 100 | 143 | -2.399 | 50 | 25 | 0.710 | 2.688 | 56 | 5 | 0 | 18.7 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 454 | -2.399 | 43 | 10 | 0.870 |
| masking_backtrack | prasa | 497 | -1.444 | 73 | 11 | 0.801 |
| masking_backtrack | yati | 1440 | -3.587 | 32 | 54 | 0.412 |
| masking_backtrack | other | 11958 | -2.296 | 51 | 23 | 0.736 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.84 / 80 |
| bhujangaprayatamu | 100 / -3.67 / 8 |
| champakamala | 100 / -1.69 / 56 |
| indravajra | 100 / -3.26 / 40 |
| kandamu | 100 / -1.85 / 67 |
| layagrahi | 100 / -3.38 / 21 |
| layavibhati | 100 / -2.34 / 40 |
| madhuragati_ragada | 100 / -2.23 / 75 |
| mahasragdhara | 100 / -3.80 / 28 |
| malini | 100 / -3.26 / 33 |
| manini | 100 / -3.13 / 42 |
| mattakokilamu | 100 / -2.14 / 53 |
| mattebhavikriditamu | 100 / -2.83 / 41 |
| pamcacamaramu | 100 / -2.54 / 49 |
| sardulavikriditamu | 100 / -2.84 / 51 |
| seesamu | 100 / -1.38 / 98 |
| sragdhara | 100 / -3.66 / 23 |
| sragvini | 100 / -3.27 / 36 |
| tetagiti | 100 / -1.75 / 81 |
| totakamu | 100 / -2.60 / 31 |
| upendravajra | 100 / -2.24 / 19 |
| utpalamala | 100 / -1.41 / 53 |
| utsahamu | 100 / -2.48 / 70 |
| vanamayuramu | 100 / -3.26 / 21 |

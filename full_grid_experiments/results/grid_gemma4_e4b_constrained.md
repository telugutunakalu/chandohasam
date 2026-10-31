# Token choices under the constraint

Runs: `grid_gemma4_e4b_constrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 34 | 100 | 100 | 180 | -2.558 | 45 | 43 | 0.559 | 1.859 | 19 | 8 | 3 | 29.4 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 476 | -2.710 | 46 | 36 | 0.575 |
| masking_backtrack | prasa | 180 | -4.643 | 31 | 69 | 0.274 |
| masking_backtrack | yati | 775 | -3.015 | 42 | 53 | 0.443 |
| masking_backtrack | other | 4697 | -2.387 | 46 | 40 | 0.588 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| bhujangaprayatamu | 100 / -1.99 / 0 |
| champakamala | 100 / -2.79 / 24 |
| indravajra | 100 / -2.00 / 8 |
| layagrahi | 100 / -2.43 / 28 |
| layavibhati | 100 / -2.59 / 33 |
| madhuragati_ragada | 100 / -1.49 / 65 |
| mahasragdhara | 100 / -1.91 / 6 |
| malini | 100 / -2.71 / 16 |
| manini | 100 / -2.93 / 22 |
| mattakokilamu | 100 / -2.68 / 11 |
| mattebhavikriditamu | 100 / -2.99 / 5 |
| pamcacamaramu | 100 / -2.89 / 0 |
| sardulavikriditamu | 100 / -3.08 / 8 |
| sragdhara | 100 / -2.37 / 0 |
| sragvini | 100 / -2.04 / 26 |
| totakamu | 100 / -2.78 / 14 |
| upendravajra | 100 / -2.82 / 29 |
| utsahamu | 100 / -2.63 / 35 |
| vanamayuramu | 100 / -2.38 / 35 |

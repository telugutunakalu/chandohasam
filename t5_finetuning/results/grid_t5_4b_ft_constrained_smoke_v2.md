# Token choices under the constraint

Runs: `grid_t5_4b_ft_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 72 | -1.292 | 67 | 4 | 0.915 | 2.131 | 53 | 8 | 0 | 6.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 7 | -1.110 | 71 | 0 | 0.971 |
| masking_backtrack | prasa | 6 | -0.601 | 100 | 0 | 0.932 |
| masking_backtrack | yati | 16 | -1.946 | 38 | 12 | 0.651 |
| masking_backtrack | other | 116 | -1.248 | 69 | 3 | 0.947 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -1.87 / 40 |
| mattakokilamu | 100 / -1.13 / 58 |

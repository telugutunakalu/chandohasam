# Token choices under the constraint

Runs: `grid_t5_4b_base_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 131 | -3.354 | 37 | 51 | 0.449 | 3.503 | 18 | 18 | 0 | 30.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 17 | -3.502 | 29 | 53 | 0.362 |
| masking_backtrack | prasa | 13 | -5.219 | 15 | 85 | 0.102 |
| masking_backtrack | yati | 34 | -4.386 | 24 | 76 | 0.433 |
| masking_backtrack | other | 198 | -3.041 | 42 | 44 | 0.481 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -3.70 / 50 |
| mattakokilamu | 100 / -3.18 / 0 |

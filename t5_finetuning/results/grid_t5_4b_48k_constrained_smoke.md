# Token choices under the constraint

Runs: `grid_t5_4b_48k_constrained_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 114 | -3.043 | 37 | 37 | 0.558 | 3.351 | 36 | 11 | 0 | 15.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 14 | -2.640 | 29 | 0 | 0.806 |
| masking_backtrack | prasa | 11 | -2.315 | 45 | 45 | 0.407 |
| masking_backtrack | yati | 36 | -4.463 | 17 | 78 | 0.216 |
| masking_backtrack | other | 167 | -2.819 | 42 | 31 | 0.621 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -1.71 / 50 |
| mattakokilamu | 100 / -3.24 / 30 |

# Token choices under the constraint

Runs: `grid_t5_4b_48k_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 118 | -2.862 | 38 | 31 | 0.596 | 3.304 | 39 | 6 | 0 | 15.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 25 | -3.141 | 24 | 4 | 0.862 |
| masking_backtrack | prasa | 16 | -2.154 | 56 | 44 | 0.405 |
| masking_backtrack | yati | 15 | -4.134 | 20 | 60 | 0.340 |
| masking_backtrack | other | 179 | -2.779 | 40 | 31 | 0.598 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -2.33 / 56 |
| mattakokilamu | 100 / -2.95 / 32 |

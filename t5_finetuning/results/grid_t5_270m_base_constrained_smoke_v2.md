# Token choices under the constraint

Runs: `grid_t5_270m_base_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 114 | -3.220 | 46 | 47 | 0.465 | 3.349 | 9 | 0 | 0 | 15.5 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 30 | -3.967 | 40 | 33 | 0.353 |
| masking_backtrack | prasa | 19 | -4.511 | 26 | 74 | 0.217 |
| masking_backtrack | yati | 17 | -3.266 | 47 | 59 | 0.308 |
| masking_backtrack | other | 162 | -2.925 | 50 | 45 | 0.531 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -3.09 / 25 |
| mattakokilamu | 100 / -3.24 / 0 |

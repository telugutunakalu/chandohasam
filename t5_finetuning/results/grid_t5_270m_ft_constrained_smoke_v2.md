# Token choices under the constraint

Runs: `grid_t5_270m_ft_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 98 | -1.947 | 62 | 17 | 0.802 | 2.324 | 63 | 14 | 0 | 18.5 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 57 | -2.740 | 47 | 46 | 0.526 |
| masking_backtrack | prasa | 8 | -1.050 | 75 | 0 | 0.915 |
| masking_backtrack | yati | 18 | -2.316 | 56 | 17 | 0.713 |
| masking_backtrack | other | 114 | -1.555 | 70 | 4 | 0.946 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -2.45 / 44 |
| mattakokilamu | 100 / -1.39 / 69 |

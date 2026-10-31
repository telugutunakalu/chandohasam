# Token choices under the constraint

Runs: `grid_mdlm523m_ft_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 78 | -1.300 | 66 | 10 | 0.882 | 2.041 | 72 | 5 | 0 | 4.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 10 | -1.542 | 50 | 10 | 0.796 |
| masking_backtrack | prasa | 10 | -1.174 | 80 | 10 | 0.870 |
| masking_backtrack | yati | 8 | -1.048 | 75 | 12 | 0.691 |
| masking_backtrack | other | 129 | -1.307 | 66 | 9 | 0.901 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -1.65 / 83 |
| mattakokilamu | 100 / -1.15 / 68 |

# Token choices under the constraint

Runs: `grid_mdlm120m_ft_constrained_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 110 | -1.537 | 58 | 11 | 0.882 | 2.262 | 69 | 17 | 0 | 8.5 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 8 | -2.641 | 12 | 0 | 0.983 |
| masking_backtrack | prasa | 10 | -0.650 | 80 | 0 | 0.961 |
| masking_backtrack | yati | 13 | -2.662 | 8 | 54 | 0.495 |
| masking_backtrack | other | 188 | -1.459 | 63 | 10 | 0.900 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| kandamu | 100 / -1.76 / 91 |
| utpalamala | 100 / -1.40 / 50 |

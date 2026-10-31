# Token choices under the constraint

Runs: `grid_t5_270m_ft_constrained_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 84 | -1.317 | 75 | 6 | 0.934 | 1.974 | 57 | 3 | 0 | 3.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 10 | -1.290 | 80 | 0 | 0.989 |
| masking_backtrack | prasa | 8 | -0.639 | 88 | 0 | 0.992 |
| masking_backtrack | yati | 13 | -3.330 | 38 | 54 | 0.452 |
| masking_backtrack | other | 138 | -1.169 | 78 | 2 | 0.972 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| kandamu | 100 / -0.69 / 56 |
| utpalamala | 100 / -1.64 / 57 |

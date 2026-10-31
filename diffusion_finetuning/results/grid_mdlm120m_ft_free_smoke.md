# Token choices under the constraint

Runs: `grid_mdlm120m_ft_free_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 4 | 0 | 0 | 86 | -0.976 | 76 | 8 | 0.900 | 1.936 | 61 | 6 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 7 | -0.882 | 86 | 0 | 0.978 |
| baseline | prasa | 5 | -0.527 | 100 | 0 | 0.996 |
| baseline | other | 36 | -0.986 | 81 | 0 | 0.965 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| kandamu | 0 / -1.08 / 69 |
| utpalamala | 0 / -0.91 / 55 |

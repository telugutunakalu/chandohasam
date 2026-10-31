# Token choices under the constraint

Runs: `grid_t5_270m_ft_free_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 4 | 0 | 0 | 81 | -1.133 | 81 | 4 | 0.951 | 2.000 | 57 | 9 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 9 | -1.232 | 78 | 0 | 0.997 |
| baseline | prasa | 6 | -0.239 | 100 | 0 | 0.995 |
| baseline | yati | 1 | -1.892 | 100 | 0 | 0.966 |
| baseline | other | 53 | -0.839 | 85 | 0 | 0.986 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| kandamu | 0 / -1.02 / 71 |
| utpalamala | 0 / -1.20 / 46 |

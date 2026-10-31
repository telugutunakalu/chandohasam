# Token choices under the constraint

Runs: `grid_nandi_ft_free_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 4 | 0 | 25 | 72 | -0.703 | 84 | 7 | 0.925 | 1.286 | 47 | 7 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 9 | -0.765 | 78 | 0 | 0.997 |
| baseline | prasa | 7 | -0.366 | 86 | 0 | 0.998 |
| baseline | yati | 5 | -0.212 | 100 | 40 | 0.559 |
| baseline | other | 58 | -0.834 | 81 | 0 | 0.984 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| kandamu | 0 / -0.74 / 54 |
| utpalamala | 50 / -0.68 / 42 |

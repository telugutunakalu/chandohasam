# Token choices under the constraint

Runs: `grid_t5_1b_ft_free_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 4 | 25 | 25 | 77 | -0.936 | 76 | 2 | 0.969 | 1.665 | 60 | 6 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 11 | -0.727 | 100 | 0 | 0.996 |
| baseline | prasa | 8 | -0.799 | 75 | 0 | 0.971 |
| baseline | yati | 3 | -0.910 | 67 | 0 | 0.981 |
| baseline | other | 99 | -0.911 | 77 | 0 | 0.994 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| kandamu | 50 / -0.91 / 65 |
| utpalamala | 0 / -0.95 / 57 |

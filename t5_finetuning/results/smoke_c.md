# Token choices under the constraint

Runs: `smoke_c`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 2 | 0 | 0 | 78 | -1.111 | 83 | 8 | 0.921 | 1.957 | 43 | 3 | 0 | 0.0 |
| masking_backtrack | 2 | 100 | 100 | 73 | -1.437 | 75 | 5 | 0.934 | 2.208 | 45 | 11 | 0 | 1.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 1 | -2.101 | 0 | 0 | 0.999 |
| baseline | prasa | 3 | -1.043 | 100 | 0 | 0.998 |
| baseline | other | 20 | -1.126 | 85 | 0 | 0.990 |
| masking_backtrack | line_start | 7 | -1.663 | 57 | 0 | 0.978 |
| masking_backtrack | prasa | 11 | -0.751 | 100 | 0 | 0.991 |
| masking_backtrack | yati | 7 | -1.635 | 71 | 14 | 0.816 |
| masking_backtrack | other | 121 | -1.474 | 74 | 6 | 0.933 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % |
|---|---|---|
| kandamu | 0 / -1.03 / 30 | 100 / -1.60 / 21 |
| utpalamala | 0 / -1.16 / 48 | 100 / -1.32 / 58 |

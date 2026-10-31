# Token choices under the constraint

Runs: `grid_gemma4_e4b_free_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 2 | 0 | 0 | 56 | -0.760 | 79 | 33 | 0.724 | 1.419 | 58 | 6 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 2 | -1.266 | 50 | 0 | 0.998 |
| baseline | prasa | 2 | -0.465 | 100 | 0 | 0.997 |
| baseline | other | 3 | -0.331 | 100 | 33 | 0.748 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 0 / -0.76 / 44 |
| mattakokilamu | 0 / -0.76 / 64 |

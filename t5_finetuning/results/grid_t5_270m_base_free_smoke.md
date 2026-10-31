# Token choices under the constraint

Runs: `grid_t5_270m_base_free_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 4 | 0 | 0 | 218 | -0.348 | 95 | 100 | 0.212 | 0.786 | 9 | 0 | 25 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| kandamu | 0 / -0.06 / 5 |
| utpalamala | 0 / -1.10 / 45 |

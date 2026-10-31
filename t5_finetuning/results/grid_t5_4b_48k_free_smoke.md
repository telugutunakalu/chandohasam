# Token choices under the constraint

Runs: `grid_t5_4b_48k_free_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 2 | 0 | 0 | 85 | -1.621 | 64 | 15 | 0.836 | 2.948 | 39 | 0 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 2 | -2.519 | 0 | 0 | 0.982 |
| baseline | prasa | 2 | -1.818 | 50 | 0 | 0.889 |
| baseline | other | 7 | -0.429 | 100 | 0 | 0.965 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 0 / -1.62 / 43 |
| mattakokilamu | 0 / -1.62 / 38 |

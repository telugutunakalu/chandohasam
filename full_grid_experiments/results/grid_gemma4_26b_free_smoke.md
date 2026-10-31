# Token choices under the constraint

Runs: `grid_gemma4_26b_free_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 2 | 0 | 0 | 42 | -0.667 | 79 | 38 | 0.684 | 1.286 | 50 | 9 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 2 | -0.783 | 50 | 0 | 1.000 |
| baseline | prasa | 2 | -0.027 | 100 | 0 | 0.982 |
| baseline | other | 2 | -0.015 | 100 | 50 | 0.503 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 0 / -0.66 / 57 |
| mattakokilamu | 0 / -0.67 / 47 |

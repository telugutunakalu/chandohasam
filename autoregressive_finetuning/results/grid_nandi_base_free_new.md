# Token choices under the constraint

Runs: `grid_nandi_base_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 0 | 0 | 251 | -0.907 | 82 | 29 | 0.635 | 1.764 | 43 | 6 | 8 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 79 | -3.394 | 4 | 9 | 0.716 |
| baseline | prasa | 35 | -3.312 | 34 | 20 | 0.749 |
| baseline | other | 85 | -2.746 | 41 | 22 | 0.754 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -0.76 / 40 |
| champakamala | 0 / -1.05 / 42 |
| kandamu | 0 / -0.66 / 59 |
| mattakokilamu | 0 / -0.71 / 14 |
| mattebhavikriditamu | 0 / -0.98 / 47 |
| sardulavikriditamu | 0 / -0.97 / 32 |
| seesamu | 0 / -0.89 / 18 |
| tetagiti | 0 / -1.04 / 40 |
| utpalamala | 0 / -1.28 / 41 |
| utsahamu | 0 / -0.67 / 43 |

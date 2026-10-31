# Token choices under the constraint

Runs: `grid_t5_4b_ft_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 11 | 11 | 79 | -1.093 | 73 | 3 | 0.967 | 1.979 | 46 | 5 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 225 | -1.017 | 64 | 0 | 0.992 |
| baseline | prasa | 86 | -0.864 | 79 | 1 | 0.966 |
| baseline | yati | 99 | -1.127 | 74 | 0 | 0.956 |
| baseline | other | 1610 | -1.137 | 72 | 0 | 0.989 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 36 / -1.14 / 56 |
| champakamala | 11 / -1.09 / 39 |
| kandamu | 9 / -1.16 / 52 |
| mattakokilamu | 0 / -0.95 / 39 |
| mattebhavikriditamu | 0 / -1.07 / 39 |
| sardulavikriditamu | 0 / -1.05 / 42 |
| seesamu | 0 / -1.15 / 71 |
| tetagiti | 10 / -1.05 / 48 |
| utpalamala | 0 / -1.11 / 43 |
| utsahamu | 0 / -1.06 / 38 |

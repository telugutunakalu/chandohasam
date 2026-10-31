# Token choices under the constraint

Runs: `grid_t5_1b_ft_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 12 | 12 | 78 | -1.045 | 74 | 3 | 0.967 | 1.882 | 47 | 5 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 208 | -1.126 | 64 | 0 | 0.997 |
| baseline | prasa | 80 | -0.732 | 89 | 0 | 0.987 |
| baseline | yati | 92 | -1.023 | 76 | 0 | 0.950 |
| baseline | other | 1506 | -1.112 | 72 | 0 | 0.989 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 36 / -1.07 / 50 |
| champakamala | 11 / -0.95 / 49 |
| kandamu | 18 / -1.06 / 49 |
| mattakokilamu | 0 / -1.03 / 45 |
| mattebhavikriditamu | 0 / -1.10 / 38 |
| sardulavikriditamu | 0 / -1.07 / 35 |
| seesamu | 0 / -1.24 / 67 |
| tetagiti | 10 / -1.05 / 56 |
| utpalamala | 0 / -1.01 / 47 |
| utsahamu | 0 / -1.10 / 29 |

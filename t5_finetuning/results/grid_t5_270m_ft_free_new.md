# Token choices under the constraint

Runs: `grid_t5_270m_ft_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 8 | 8 | 80 | -1.115 | 81 | 3 | 0.964 | 2.001 | 47 | 5 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 219 | -1.033 | 77 | 0 | 0.995 |
| baseline | prasa | 81 | -0.707 | 89 | 0 | 0.986 |
| baseline | yati | 98 | -1.131 | 87 | 3 | 0.921 |
| baseline | other | 1654 | -1.180 | 80 | 1 | 0.987 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 9 / -1.09 / 60 |
| champakamala | 0 / -1.09 / 39 |
| kandamu | 18 / -1.16 / 53 |
| mattakokilamu | 0 / -0.87 / 25 |
| mattebhavikriditamu | 0 / -1.16 / 42 |
| sardulavikriditamu | 0 / -1.12 / 34 |
| seesamu | 0 / -1.16 / 69 |
| tetagiti | 10 / -1.13 / 60 |
| utpalamala | 12 / -1.06 / 42 |
| utsahamu | 0 / -1.34 / 35 |

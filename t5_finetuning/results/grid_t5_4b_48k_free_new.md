# Token choices under the constraint

Runs: `grid_t5_4b_48k_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 0 | 0 | 84 | -1.561 | 63 | 9 | 0.892 | 2.803 | 46 | 7 | 2 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 83 | -1.781 | 30 | 1 | 0.957 |
| baseline | prasa | 41 | -0.928 | 85 | 2 | 0.926 |
| baseline | yati | 12 | -0.899 | 92 | 0 | 0.926 |
| baseline | other | 565 | -1.480 | 65 | 2 | 0.947 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -1.60 / 57 |
| champakamala | 0 / -1.49 / 45 |
| kandamu | 0 / -1.47 / 44 |
| mattakokilamu | 0 / -1.53 / 32 |
| mattebhavikriditamu | 0 / -1.66 / 38 |
| sardulavikriditamu | 0 / -1.71 / 39 |
| seesamu | 0 / -1.69 / 33 |
| tetagiti | 0 / -1.46 / 56 |
| utpalamala | 0 / -1.52 / 45 |
| utsahamu | 0 / -1.72 / 40 |

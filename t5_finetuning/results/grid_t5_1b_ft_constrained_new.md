# Token choices under the constraint

Runs: `grid_t5_1b_ft_constrained_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 66 | 100 | 100 | 85 | -1.196 | 71 | 4 | 0.944 | 1.943 | 44 | 5 | 2 | 3.3 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 342 | -1.376 | 64 | 2 | 0.955 |
| masking_backtrack | prasa | 192 | -0.821 | 84 | 7 | 0.897 |
| masking_backtrack | yati | 448 | -1.842 | 57 | 18 | 0.784 |
| masking_backtrack | other | 4654 | -1.136 | 72 | 3 | 0.960 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.18 / 50 |
| champakamala | 100 / -1.06 / 42 |
| kandamu | 100 / -1.20 / 44 |
| mattakokilamu | 100 / -1.28 / 50 |
| mattebhavikriditamu | 100 / -1.22 / 42 |
| sardulavikriditamu | 100 / -1.17 / 39 |
| seesamu | 100 / -2.22 / 71 |
| tetagiti | 100 / -0.99 / 48 |
| utpalamala | 100 / -1.24 / 38 |
| utsahamu | 100 / -1.40 / 12 |

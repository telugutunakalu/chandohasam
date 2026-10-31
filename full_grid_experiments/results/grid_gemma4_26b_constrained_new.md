# Token choices under the constraint

Runs: `grid_gemma4_26b_constrained_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 66 | 100 | 100 | 155 | -2.195 | 57 | 32 | 0.669 | 1.336 | 34 | 8 | 26 | 27.4 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 311 | -1.042 | 68 | 5 | 0.936 |
| masking_backtrack | prasa | 222 | -1.319 | 76 | 21 | 0.760 |
| masking_backtrack | yati | 1429 | -3.374 | 40 | 53 | 0.457 |
| masking_backtrack | other | 8251 | -2.058 | 59 | 29 | 0.693 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -2.43 / 44 |
| champakamala | 100 / -2.05 / 25 |
| kandamu | 100 / -2.02 / 48 |
| mattakokilamu | 100 / -1.99 / 6 |
| mattebhavikriditamu | 100 / -1.91 / 10 |
| sardulavikriditamu | 100 / -2.36 / 7 |
| seesamu | 100 / -1.29 / 44 |
| tetagiti | 100 / -2.19 / 54 |
| utpalamala | 100 / -2.64 / 30 |
| utsahamu | 100 / -1.29 / 42 |

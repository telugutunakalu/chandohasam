# Token choices under the constraint

Runs: `grid_nandi_base_constrained_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 66 | 100 | 100 | 137 | -3.616 | 33 | 43 | 0.532 | 4.340 | 30 | 22 | 29 | 19.1 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 422 | -3.822 | 15 | 30 | 0.528 |
| masking_backtrack | prasa | 214 | -3.453 | 42 | 54 | 0.349 |
| masking_backtrack | yati | 943 | -4.298 | 24 | 65 | 0.319 |
| masking_backtrack | other | 7479 | -3.522 | 35 | 40 | 0.565 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -3.68 / 47 |
| champakamala | 100 / -3.79 / 8 |
| kandamu | 100 / -3.56 / 43 |
| mattakokilamu | 100 / -3.55 / 5 |
| mattebhavikriditamu | 100 / -3.77 / 24 |
| sardulavikriditamu | 100 / -3.62 / 23 |
| seesamu | 100 / -4.30 / 38 |
| tetagiti | 100 / -3.48 / 39 |
| utpalamala | 100 / -3.15 / 18 |
| utsahamu | 100 / -4.90 / 21 |

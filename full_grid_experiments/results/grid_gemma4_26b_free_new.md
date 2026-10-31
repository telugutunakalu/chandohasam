# Token choices under the constraint

Runs: `grid_gemma4_26b_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 0 | 0 | 73 | -0.494 | 87 | 23 | 0.771 | 0.950 | 53 | 6 | 8 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 59 | -0.750 | 58 | 3 | 0.966 |
| baseline | prasa | 31 | -0.537 | 84 | 6 | 0.897 |
| baseline | other | 149 | -0.606 | 88 | 3 | 0.953 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -0.50 / 55 |
| champakamala | 0 / -0.50 / 57 |
| kandamu | 0 / -0.54 / 49 |
| mattakokilamu | 0 / -0.59 / 48 |
| mattebhavikriditamu | 0 / -0.41 / 69 |
| sardulavikriditamu | 0 / -0.67 / 50 |
| seesamu | 0 / -0.53 / 38 |
| tetagiti | 0 / -0.52 / 55 |
| utpalamala | 0 / -0.54 / 46 |
| utsahamu | 0 / -0.15 / 14 |

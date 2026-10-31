# Token choices under the constraint

Runs: `grid_nandi_ft_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 6 | 8 | 75 | -0.776 | 84 | 4 | 0.953 | 1.456 | 50 | 6 | 3 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 154 | -0.802 | 81 | 1 | 0.987 |
| baseline | prasa | 93 | -0.679 | 84 | 0 | 0.988 |
| baseline | yati | 63 | -1.050 | 75 | 3 | 0.945 |
| baseline | other | 1384 | -0.834 | 83 | 1 | 0.981 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 9 / -0.76 / 57 |
| champakamala | 11 / -0.80 / 50 |
| kandamu | 18 / -0.86 / 51 |
| mattakokilamu | 0 / -0.66 / 35 |
| mattebhavikriditamu | 0 / -0.81 / 37 |
| sardulavikriditamu | 0 / -0.83 / 42 |
| seesamu | 0 / -0.58 / 71 |
| tetagiti | 10 / -0.77 / 50 |
| utpalamala | 0 / -0.76 / 53 |
| utsahamu | 0 / -0.11 / 100 |

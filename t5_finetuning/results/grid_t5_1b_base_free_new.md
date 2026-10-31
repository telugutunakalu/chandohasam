# Token choices under the constraint

Runs: `grid_t5_1b_base_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 0 | 0 | 203 | -0.702 | 84 | 66 | 0.527 | 1.309 | 37 | 7 | 21 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 10 | -2.539 | 10 | 80 | 0.671 |
| baseline | prasa | 3 | -1.851 | 67 | 0 | 0.769 |
| baseline | other | 22 | -1.943 | 59 | 14 | 0.863 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -0.58 / 27 |
| champakamala | 0 / -1.16 / 39 |
| kandamu | 0 / -0.42 / 31 |
| mattakokilamu | 0 / – / – |
| mattebhavikriditamu | 0 / -0.71 / 55 |
| sardulavikriditamu | 0 / -1.10 / 34 |
| seesamu | 0 / -0.45 / 71 |
| tetagiti | 0 / -0.70 / 30 |
| utpalamala | 0 / -0.68 / 47 |
| utsahamu | 0 / -1.63 / 33 |

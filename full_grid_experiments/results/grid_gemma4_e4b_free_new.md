# Token choices under the constraint

Runs: `grid_gemma4_e4b_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 0 | 0 | 73 | -0.783 | 80 | 27 | 0.733 | 1.392 | 44 | 4 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 68 | -1.380 | 37 | 9 | 0.934 |
| baseline | prasa | 27 | -0.677 | 89 | 4 | 0.937 |
| baseline | other | 116 | -0.883 | 78 | 5 | 0.890 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -0.82 / 41 |
| champakamala | 0 / -0.75 / 39 |
| kandamu | 0 / -0.94 / 43 |
| mattakokilamu | 0 / -1.29 / 24 |
| mattebhavikriditamu | 0 / -0.77 / 49 |
| sardulavikriditamu | 0 / -0.76 / 43 |
| seesamu | 0 / -0.73 / 44 |
| tetagiti | 0 / -0.73 / 47 |
| utpalamala | 0 / -0.64 / 46 |
| utsahamu | 0 / -0.59 / 48 |

# Token choices under the constraint

Runs: `grid_t5_270m_base_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 0 | 0 | 234 | -0.389 | 94 | 95 | 0.174 | 0.835 | 30 | 4 | 14 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 27 | -3.121 | 22 | 100 | 0.095 |
| baseline | prasa | 1 | -1.808 | 100 | 100 | 0.710 |
| baseline | other | 2 | -0.736 | 100 | 0 | 0.821 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -0.48 / 21 |
| champakamala | 0 / -0.54 / 23 |
| kandamu | 0 / -0.22 / 23 |
| mattakokilamu | 0 / -0.62 / 100 |
| mattebhavikriditamu | 0 / -0.59 / 37 |
| sardulavikriditamu | 0 / -0.38 / 34 |
| seesamu | 0 / -0.16 / 98 |
| tetagiti | 0 / -0.38 / 21 |
| utpalamala | 0 / -0.35 / 26 |
| utsahamu | 0 / -0.25 / 48 |

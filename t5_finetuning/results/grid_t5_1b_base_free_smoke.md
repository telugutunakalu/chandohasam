# Token choices under the constraint

Runs: `grid_t5_1b_base_free_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 4 | 0 | 0 | 278 | -0.776 | 83 | 100 | 0.439 | 1.482 | 43 | 2 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 1 | -2.349 | 0 | 100 | 0.699 |
| baseline | prasa | 2 | -3.797 | 0 | 100 | 0.612 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| kandamu | 0 / -0.56 / 39 |
| utpalamala | 0 / -1.06 / 46 |

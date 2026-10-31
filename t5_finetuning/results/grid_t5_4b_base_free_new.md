# Token choices under the constraint

Runs: `grid_t5_4b_base_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 0 | 0 | 28 | -0.749 | 84 | 58 | 0.545 | 1.480 | 42 | 3 | 2 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 4 | -2.399 | 50 | 75 | 0.711 |
| baseline | prasa | 2 | -1.807 | 50 | 0 | 0.865 |
| baseline | other | 9 | -1.915 | 44 | 22 | 0.778 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -1.48 / 20 |
| champakamala | 0 / -0.97 / 18 |
| kandamu | 0 / -0.12 / 62 |
| mattakokilamu | 0 / – / – |
| mattebhavikriditamu | 0 / -0.64 / 21 |
| sardulavikriditamu | 0 / -0.70 / 44 |
| seesamu | 0 / -1.97 / 40 |
| tetagiti | 0 / -0.90 / 43 |
| utpalamala | 0 / -0.72 / 0 |
| utsahamu | 0 / – / – |

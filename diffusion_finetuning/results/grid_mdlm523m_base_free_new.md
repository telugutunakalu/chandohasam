# Token choices under the constraint

Runs: `grid_mdlm523m_base_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 0 | 0 | 269 | -0.614 | 84 | 28 | 0.677 | 1.123 | 42 | 6 | 21 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 69 | -2.912 | 6 | 4 | 0.833 |
| baseline | prasa | 34 | -1.816 | 62 | 32 | 0.697 |
| baseline | other | 154 | -1.426 | 68 | 19 | 0.752 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -0.35 / 48 |
| champakamala | 0 / -0.70 / 37 |
| kandamu | 0 / -0.60 / 40 |
| mattakokilamu | 0 / -1.23 / 44 |
| mattebhavikriditamu | 0 / -0.82 / 51 |
| sardulavikriditamu | 0 / -0.60 / 30 |
| seesamu | 0 / -0.70 / 51 |
| tetagiti | 0 / -0.72 / 43 |
| utpalamala | 0 / -0.58 / 41 |
| utsahamu | 0 / -0.22 / 24 |

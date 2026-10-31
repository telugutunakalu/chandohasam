# Token choices under the constraint

Runs: `grid_t5_270m_base_constrained_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 66 | 100 | 100 | 149 | -2.938 | 47 | 43 | 0.536 | 3.133 | 19 | 14 | 26 | 21.9 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 573 | -3.578 | 36 | 35 | 0.431 |
| masking_backtrack | prasa | 255 | -3.535 | 37 | 65 | 0.284 |
| masking_backtrack | yati | 1272 | -3.672 | 37 | 61 | 0.371 |
| masking_backtrack | other | 7710 | -2.750 | 50 | 40 | 0.580 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -3.30 / 33 |
| champakamala | 100 / -3.09 / 15 |
| kandamu | 100 / -2.72 / 24 |
| mattakokilamu | 100 / -3.29 / 0 |
| mattebhavikriditamu | 100 / -3.01 / 7 |
| sardulavikriditamu | 100 / -2.75 / 8 |
| seesamu | 100 / -2.75 / 34 |
| tetagiti | 100 / -2.53 / 23 |
| utpalamala | 100 / -3.01 / 16 |
| utsahamu | 100 / -3.27 / 19 |

# Token choices under the constraint

Runs: `grid_mdlm523m_ft_free_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 66 | 2 | 2 | 87 | -0.900 | 77 | 5 | 0.938 | 1.759 | 59 | 6 | 0 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 120 | -1.359 | 45 | 0 | 0.982 |
| baseline | prasa | 69 | -0.586 | 94 | 0 | 0.979 |
| baseline | yati | 21 | -1.406 | 57 | 0 | 0.905 |
| baseline | other | 998 | -0.930 | 76 | 1 | 0.976 |

## By meter

| meter | baseline in meter % / logp / lexical % |
|---|---|
| ataveladi | 0 / -0.85 / 74 |
| champakamala | 0 / -0.94 / 49 |
| kandamu | 0 / -0.88 / 60 |
| mattakokilamu | 0 / -0.95 / 71 |
| mattebhavikriditamu | 0 / -1.00 / 55 |
| sardulavikriditamu | 0 / -0.96 / 47 |
| seesamu | 0 / -1.07 / 84 |
| tetagiti | 0 / -0.77 / 67 |
| utpalamala | 12 / -0.89 / 54 |
| utsahamu | 0 / -0.79 / 74 |

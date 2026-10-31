# Token choices under the constraint

Runs: `grid_t5_270m_base_constrained_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 100 | 100 | 100 | 141 | -2.627 | 53 | 39 | 0.566 | 2.883 | 20 | 7 | 42 | 19.9 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 842 | -3.493 | 39 | 35 | 0.434 |
| masking_backtrack | prasa | 466 | -3.435 | 39 | 61 | 0.328 |
| masking_backtrack | yati | 1456 | -3.004 | 47 | 48 | 0.451 |
| masking_backtrack | other | 11370 | -2.482 | 55 | 37 | 0.601 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -2.94 / 37 |
| bhujangaprayatamu | 100 / -2.78 / 0 |
| champakamala | 100 / -2.84 / 19 |
| indravajra | 100 / -2.94 / 0 |
| kandamu | 100 / -2.65 / 27 |
| layagrahi | 100 / -1.96 / 3 |
| layavibhati | 100 / -1.07 / 28 |
| madhuragati_ragada | 100 / -3.52 / 21 |
| mahasragdhara | 100 / -3.22 / 8 |
| malini | 100 / -3.11 / 5 |
| manini | 100 / -1.31 / 0 |
| mattakokilamu | 100 / -2.75 / 15 |
| mattebhavikriditamu | 100 / -2.56 / 12 |
| pamcacamaramu | 100 / -3.00 / 40 |
| sardulavikriditamu | 100 / -2.59 / 0 |
| seesamu | 100 / -2.91 / 34 |
| sragdhara | 100 / -1.91 / 0 |
| sragvini | 100 / -2.91 / 24 |
| tetagiti | 100 / -2.52 / 30 |
| totakamu | 100 / -3.85 / 19 |
| upendravajra | 100 / -4.03 / 18 |
| utpalamala | 100 / -2.27 / 10 |
| utsahamu | 100 / -2.97 / 21 |
| vanamayuramu | 100 / -3.04 / 33 |

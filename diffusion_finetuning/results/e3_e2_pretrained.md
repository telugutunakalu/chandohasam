# Token choices under the constraint

Runs: `e3_e2_pretrained`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 111 | 0 | 0 | 35 | -2.013 | 46 | 22 | 0.772 | 2.896 | 74 | 4 | 0 | 0.0 |
| masking_only | 111 | 100 | 100 | 149 | -2.434 | 51 | 31 | 0.616 | 2.950 | 52 | 42 | 9 | 0.0 |
| masking_backtrack | 111 | 100 | 100 | 194 | -2.724 | 42 | 31 | 0.607 | 3.131 | 55 | 38 | 4 | 26.6 |
| hybrid | 111 | 99 | 99 | 147 | -2.419 | 50 | 31 | 0.614 | 2.912 | 48 | 33 | 6 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 100 | -2.662 | 0 | 11 | 0.884 |
| baseline | prasa | 96 | -2.407 | 41 | 16 | 0.838 |
| baseline | yati | 1 | -1.197 | 100 | 0 | 0.522 |
| baseline | other | 292 | -1.891 | 55 | 7 | 0.903 |
| masking_only | line_start | 830 | -3.365 | 34 | 34 | 0.566 |
| masking_only | prasa | 729 | -2.431 | 57 | 37 | 0.518 |
| masking_only | yati | 2448 | -3.494 | 35 | 55 | 0.378 |
| masking_only | other | 12569 | -2.166 | 55 | 26 | 0.671 |
| masking_backtrack | line_start | 771 | -3.281 | 31 | 28 | 0.632 |
| masking_backtrack | prasa | 806 | -2.582 | 56 | 37 | 0.505 |
| masking_backtrack | yati | 3342 | -3.457 | 32 | 47 | 0.418 |
| masking_backtrack | other | 16662 | -2.559 | 44 | 28 | 0.649 |
| hybrid | line_start | 1106 | -2.647 | 44 | 35 | 0.574 |
| hybrid | prasa | 700 | -2.171 | 54 | 37 | 0.503 |
| hybrid | yati | 2483 | -3.514 | 34 | 55 | 0.378 |
| hybrid | other | 12042 | -2.186 | 54 | 25 | 0.673 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 0 / -2.01 / 74 | 100 / -1.72 / 91 | 100 / -2.03 / 86 | 100 / -1.52 / 81 |
| bhujangaprayatamu | 0 / -2.01 / 74 | 100 / -2.67 / 8 | 100 / -3.88 / 12 | 100 / -2.29 / 23 |
| champakamala | 0 / -2.01 / 74 | 100 / -2.23 / 20 | 100 / -2.60 / 61 | 100 / -2.28 / 24 |
| dvipada | 0 / -2.01 / 74 | 100 / -2.80 / 76 | 100 / -2.17 / 83 | 100 / -2.72 / 61 |
| hayapracara_ragada | 0 / -2.01 / 74 | 100 / -2.99 / 75 | 100 / -2.80 / 70 | 100 / -2.43 / 77 |
| indravajra | 0 / -2.01 / 74 | 100 / -2.91 / 23 | 100 / -3.09 / 23 | 100 / -2.69 / 43 |
| kandamu | 0 / -2.01 / 74 | 100 / -1.52 / 68 | 100 / -1.74 / 80 | 100 / -2.01 / 66 |
| kavirajavirajitamu | 0 / -2.01 / 74 | 100 / -2.27 / 47 | 100 / -2.86 / 43 | 100 / -2.16 / 43 |
| lalita | 0 / -2.01 / 74 | 100 / -2.74 / 18 | 100 / -2.91 / 20 | 100 / -2.66 / 43 |
| layagrahi | 0 / -2.01 / 74 | 100 / -2.14 / 58 | 100 / -2.38 / 53 | 100 / -2.12 / 43 |
| layavibhati | 0 / -2.01 / 74 | 100 / -1.93 / 62 | 100 / -2.33 / 74 | 100 / -2.10 / 68 |
| madhuragati_ragada | 0 / -2.01 / 74 | 100 / -2.64 / 76 | 100 / -1.89 / 64 | 100 / -2.43 / 77 |
| madhyakkara | 0 / -2.01 / 74 | 100 / -2.26 / 89 | 100 / -2.09 / 83 | 100 / -2.24 / 75 |
| mahasragdhara | 0 / -2.01 / 74 | 100 / -2.89 / 21 | 100 / -2.90 / 29 | 100 / -2.84 / 20 |
| malini | 0 / -2.01 / 74 | 100 / -2.55 / 32 | 100 / -2.73 / 21 | 100 / -2.99 / 36 |
| mangalamahasri | 0 / -2.01 / 74 | 100 / -2.49 / 46 | 100 / -2.42 / 37 | 100 / -2.55 / 34 |
| manini | 0 / -2.01 / 74 | 100 / -2.81 / 44 | 100 / -2.53 / 48 | 100 / -2.53 / 52 |
| mattakokilamu | 0 / -2.01 / 74 | 100 / -2.72 / 44 | 100 / -2.90 / 34 | 100 / -2.95 / 25 |
| mattebhavikriditamu | 0 / -2.01 / 74 | 100 / -2.72 / 30 | 100 / -2.64 / 28 | 100 / -2.74 / 18 |
| pamcacamaramu | 0 / -2.01 / 74 | 100 / -2.18 / 26 | 100 / -2.48 / 26 | 100 / -2.21 / 24 |
| rathoddhata | 0 / -2.01 / 74 | 100 / -3.07 / 42 | 100 / -3.33 / 50 | 100 / -3.07 / 44 |
| salini | 0 / -2.01 / 74 | 100 / -2.68 / 16 | 100 / -3.62 / 21 | 100 / -2.62 / 22 |
| sardulavikriditamu | 0 / -2.01 / 74 | 100 / -2.72 / 17 | 100 / -3.37 / 13 | 100 / -2.61 / 14 |
| seesamu | 0 / -2.01 / 74 | 100 / -1.64 / 88 | 100 / -1.86 / 86 | 100 / -1.81 / 82 |
| sragdhara | 0 / -2.01 / 74 | 100 / -2.38 / 30 | 100 / -3.36 / 26 | 67 / -2.38 / 10 |
| sragvini | 0 / -2.01 / 74 | 100 / -2.43 / 36 | 100 / -3.28 / 30 | 100 / -2.48 / 16 |
| taralamu | 0 / -2.01 / 74 | 100 / -2.62 / 25 | 100 / -2.61 / 45 | 100 / -2.56 / 35 |
| taruvoja | 0 / -2.01 / 74 | 100 / -2.30 / 79 | 100 / -2.08 / 81 | 100 / -2.17 / 81 |
| tetagiti | 0 / -2.01 / 74 | 100 / -2.13 / 75 | 100 / -2.51 / 82 | 100 / -1.72 / 81 |
| totakamu | 0 / -2.01 / 74 | 100 / -2.51 / 56 | 100 / -3.08 / 34 | 100 / -3.15 / 50 |
| turagagati_ragada | 0 / -2.01 / 74 | 100 / -1.82 / 82 | 100 / -2.24 / 91 | 100 / -1.95 / 84 |
| upendravajra | 0 / -2.01 / 74 | 100 / -2.88 / 25 | 100 / -3.08 / 9 | 100 / -2.68 / 35 |
| utpalamala | 0 / -2.01 / 74 | 100 / -2.80 / 51 | 100 / -2.56 / 45 | 100 / -2.25 / 29 |
| utsahamu | 0 / -2.01 / 74 | 100 / -2.01 / 81 | 100 / -2.58 / 70 | 100 / -1.86 / 86 |
| vanamayuramu | 0 / -2.01 / 74 | 100 / -2.78 / 49 | 100 / -2.76 / 49 | 100 / -2.68 / 45 |
| vasamtatilakamu | 0 / -2.01 / 74 | 100 / -2.50 / 36 | 100 / -3.16 / 37 | 100 / -2.55 / 54 |
| vidyunmala | 0 / -2.01 / 74 | 100 / -2.39 / 10 | 100 / -3.54 / 8 | 100 / -2.54 / 11 |

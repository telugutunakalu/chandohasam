Same 111 poems in every run. Words of 2+ aksharas: 170211 in the corpus, 155530 in the 90% (known), 14681 only in the held-out 10%.

| run | strategy | in meter | real | known | held-out only | 1-akshara | logp | repeated line |
|---|---|---|---|---|---|---|---|---|
| v1 | masking_only | 37/37 | 23.1% | 23.1% | 0.00% | 4.7% | -2.19 | 9/37 |
| v1 | masking_backtrack | 37/37 | 24.3% | 24.3% | 0.00% | 2.9% | -2.05 | 9/37 |
| v1 | hybrid | 37/37 | 24.0% | 24.0% | 0.00% | 3.9% | -2.09 | 11/37 |
| A | masking_only | 37/37 | 23.4% | 23.4% | 0.00% | 4.3% | -2.10 | 7/37 |
| A | masking_backtrack | 37/37 | 23.1% | 23.1% | 0.00% | 6.4% | -2.23 | 8/37 |
| A | hybrid | 37/37 | 25.4% | 25.4% | 0.00% | 3.1% | -2.26 | 9/37 |
| A+B all (full corpus) | masking_only | 37/37 | 30.3% | 30.0% | 0.33% | 3.3% | -2.11 | 8/37 |
| A+B all (full corpus) | masking_backtrack | 37/37 | 37.1% | 35.6% | 1.46% | 5.0% | -2.10 | 11/37 |
| A+B all (full corpus) | hybrid | 37/37 | 33.2% | 32.5% | 0.68% | 3.1% | -2.28 | 10/37 |
| A+B all (90% corpus) | masking_only | 37/37 | 29.6% | 29.6% | 0.00% | 3.4% | -2.16 | 8/37 |
| A+B all (90% corpus) | masking_backtrack | 37/37 | 36.6% | 36.3% | 0.31% | 6.3% | -2.05 | 14/37 |
| A+B all (90% corpus) | hybrid | 37/37 | 32.5% | 32.2% | 0.34% | 3.2% | -2.32 | 9/37 |

Per poem against v1 (paired bootstrap, 5,000 resamples, 95% interval):

- A, real: +0.61 points [-1.55, +2.71]
- A, held-out only: +0.00 points [+0.00, +0.00]
- A+B all (full corpus), real: +8.93 points [+6.00, +12.05]
- A+B all (full corpus), held-out only: +0.99 points [+0.29, +1.90]
- A+B all (90% corpus), real: +8.17 points [+5.34, +11.17]
- A+B all (90% corpus), held-out only: +0.23 points [+0.03, +0.49]

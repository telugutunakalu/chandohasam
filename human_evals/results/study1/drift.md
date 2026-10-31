```
ratings 509 latest 2026-10-29T10:56:10+00:00
by annotator Counter({'A4': 133, 'A3': 103, 'A5': 101, 'A1': 101, 'A2': 71})

A. ordinal alpha, cumulative by creation date (current answers)
cutoff     n_ratings poems>=2 readabil comprehe  lexical   bhavam   poetic
2026-10-13         9        0      –        –        –        –        –  
2026-10-15        12        1      –     +0.000      –        –     +0.000
2026-10-16        14        3   +0.778   +0.167   +0.773   +0.571   +0.167
2026-10-18        56        5   +0.600   +0.100   +0.658   +0.550   +0.361
2026-10-19        78       16   +0.604   +0.226   +0.628   +0.573   +0.496
2026-10-21        93       16   +0.540   +0.294   +0.508   +0.411   +0.511
2026-10-23       132       25   +0.169   +0.123   +0.377   +0.023   +0.132
2026-10-24       141       25   +0.071   +0.029   +0.252   +0.003   +0.151
2026-10-26       220       45   +0.109   +0.180   +0.277   +0.097   +0.145
2026-10-27       257       65   +0.129   +0.225   +0.311   +0.048   +0.119
2026-10-28       508      101   +0.162   +0.209   +0.314   +0.116   +0.039
2026-10-29       509      102   +0.159   +0.209   +0.311   +0.117   +0.046

B. alpha by subset
subset              readabil comprehe  lexical   bhavam   poetic
all                   +0.159   +0.209   +0.311   +0.117   +0.046
calibration 25        +0.120   +0.141   +0.259   +0.031   +0.184
without A5        +0.127   +0.142   +0.329   +0.036   +0.024
without A3      +0.036   +0.130   +0.233   +0.034   -0.117
without A1         +0.131   +0.150   +0.246   +0.020   -0.053
without A4        +0.142   +0.297   +0.396   +0.261   +0.292
without A2         +0.286   +0.261   +0.327   +0.188   +0.042
real poets only       +0.168   +0.245   +0.357   +0.032   +0.078
real+textbook         +0.112   +0.171   +0.270   +0.023   +0.065
real+gemini           +0.202   +0.259   +0.366   +0.127   +0.046

C. ceiling and between-poem variance share (one-way ICC(1) on poems with >=2 ratings)
readability    n=509 mean=4.42 sd=0.78 >=4: 84.7% =5: 58.5%  ICC(1)=+0.159  MSB=0.980 MSW=0.527
comprehension  n=509 mean=3.87 sd=1.01 >=4: 64.4% =5: 33.8%  ICC(1)=+0.203  MSB=1.765 MSW=0.819
lexical        n=509 mean=4.18 sd=0.84 >=4: 80.0% =5: 41.7%  ICC(1)=+0.292  MSB=1.472 MSW=0.512
bhavam         n=509 mean=4.52 sd=0.83 >=4: 87.6% =5: 68.8%  ICC(1)=+0.194  MSB=1.233 MSW=0.590
poetic         n=509 mean=3.98 sd=0.91 >=4: 71.7% =5: 33.0%  ICC(1)=+0.080  MSB=1.060 MSW=0.759

D. rater drift: mean residual (rating - other raters' poem mean), first vs second half of each annotator's ratings
A5    readab +0.44->+0.10 (n 50/51) | compre -0.04->-0.77 (n 50/51) | lexica +0.41->-0.09 (n 50/51) | bhavam +0.29->-0.13 (n 50/51) | poetic -0.29->-0.95 (n 50/51)
A3  readab -0.42->-0.35 (n 51/50) | compre -0.37->-0.68 (n 51/50) | lexica -0.49->-0.43 (n 51/50) | bhavam -0.22->-0.65 (n 51/50) | poetic -0.15->-0.39 (n 51/50)
A1     readab -0.53->-0.60 (n 41/48) | compre -0.53->-0.29 (n 41/48) | lexica -0.37->-0.17 (n 41/48) | bhavam -0.46->+0.06 (n 41/48) | poetic +0.07->+0.17 (n 41/48)
A4    readab -0.15->+0.43 (n 63/39) | compre +0.54->+1.18 (n 63/39) | lexica +0.09->+0.80 (n 63/39) | bhavam -0.12->+0.52 (n 63/39) | poetic +0.35->+1.30 (n 63/39)
A2     readab +0.98->+0.57 (n 35/36) | compre +0.94->+0.47 (n 35/36) | lexica +0.44->+0.03 (n 35/36) | bhavam +0.69->+0.41 (n 35/36) | poetic +0.23->-0.05 (n 35/36)

E. re-rating: the earlier answer (annotation_history) vs the current one, same annotator and poem
readability    pairs=567 unchanged=91.2% mean|diff|=0.09
comprehension  pairs=567 unchanged=91.9% mean|diff|=0.09
lexical        pairs=567 unchanged=93.8% mean|diff|=0.06
bhavam         pairs=364 unchanged=67.3% mean|diff|=0.50
poetic         pairs=567 unchanged=76.0% mean|diff|=0.30
chandassu      pairs=567 unchanged=100.0% mean|diff|=0.00
prasa          pairs=426 unchanged=100.0% mean|diff|=0.00
yati           pairs=567 unchanged=99.8% mean|diff|=0.00
shabdalankara  pairs=567 unchanged=91.5% mean|diff|=0.08
arthalankara   pairs=567 unchanged=93.7% mean|diff|=0.06
register       pairs=433 unchanged=97.7% mean|diff|=0.02
ai_generated   pairs=433 unchanged=97.0% mean|diff|=0.03
history rows 567 rubric versions in history Counter({'2': 433, '1': 134})

F. binary questions: agreement vs alpha vs AC1
chandassu      poems=102 %agree=1.000 alpha=  –   AC1=  –   yes=1.000
prasa          poems= 76 %agree=1.000 alpha=  –   AC1=  –   yes=1.000
yati           poems=102 %agree=0.992 alpha=-0.002 AC1=+0.992 yes=0.996
shabdalankara  poems=102 %agree=0.451 alpha=-0.093 AC1=-0.097 yes=0.494
arthalankara   poems=102 %agree=0.473 alpha=-0.049 AC1=-0.052 yes=0.515
register       poems=102 %agree=0.793 alpha=+0.314 AC1=+0.705 yes=0.821
ai_generated   poems=102 %agree=0.873 alpha=+0.260 AC1=+0.847 yes=0.091

G. first rating date per annotator, and ratings per day
{'A1': '2026-10-13T14:46', 'A3': '2026-10-15T09:23', 'A4': '2026-10-16T17:04', 'A2': '2026-10-23T15:59', 'A5': '2026-10-26T09:46'}
[(('2026-10-13', 'A1'), 9), (('2026-10-15', 'A3'), 3), (('2026-10-16', 'A4'), 2), (('2026-10-18', 'A1'), 42), (('2026-10-19', 'A3'), 13), (('2026-10-19', 'A1'), 9), (('2026-10-21', 'A1'), 10), (('2026-10-21', 'A4'), 5), (('2026-10-23', 'A4'), 23), (('2026-10-23', 'A2'), 16), (('2026-10-24', 'A4'), 5), (('2026-10-24', 'A2'), 4), (('2026-10-26', 'A5'), 44), (('2026-10-26', 'A3'), 10), (('2026-10-26', 'A4'), 24), (('2026-10-26', 'A2'), 1), (('2026-10-27', 'A4'), 7), (('2026-10-27', 'A2'), 30), (('2026-10-28', 'A5'), 57), (('2026-10-28', 'A3'), 76), (('2026-10-28', 'A1'), 31), (('2026-10-28', 'A4'), 67), (('2026-10-28', 'A2'), 20), (('2026-10-29', 'A3'), 1)]

H. pairwise: Spearman rho and mean residual gap per annotator pair (>=15 common poems)
A5-A3 n=100: readab rho +0.43 gap +0.51 | compre rho +0.47 gap +0.08 | lexica rho +0.42 gap +0.48 | bhavam rho +0.60 gap +0.40 | poetic rho +0.54 gap -0.26
A5-A1 n=89: readab rho +0.28 gap +0.70 | compre rho +0.46 gap +0.03 | lexica rho +0.34 gap +0.36 | bhavam rho +0.50 gap +0.22 | poetic rho +0.28 gap -0.54
A5-A4 n=101: readab rho +0.18 gap +0.17 | compre rho +0.16 gap -0.92 | lexica rho +0.12 gap -0.15 | bhavam rho -0.19 gap -0.03 | poetic rho -0.45 gap -1.03
A5-A2 n=71: readab rho   –   gap -0.41 | compre rho +0.21 gap -0.90 | lexica rho +0.31 gap -0.04 | bhavam rho +0.02 gap -0.37 | poetic rho +0.28 gap -0.46
A3-A1 n=89: readab rho +0.51 gap +0.13 | compre rho +0.56 gap -0.10 | lexica rho +0.67 gap -0.17 | bhavam rho +0.42 gap -0.19 | poetic rho +0.44 gap -0.30
A3-A4 n=101: readab rho +0.37 gap -0.35 | compre rho +0.26 gap -1.01 | lexica rho +0.35 gap -0.63 | bhavam rho -0.09 gap -0.43 | poetic rho -0.21 gap -0.75
A3-A2 n=71: readab rho   –   gap -0.93 | compre rho +0.20 gap -0.96 | lexica rho +0.39 gap -0.55 | bhavam rho +0.11 gap -0.75 | poetic rho +0.22 gap -0.31
A1-A4 n=89: readab rho +0.29 gap -0.48 | compre rho +0.33 gap -0.91 | lexica rho +0.42 gap -0.47 | bhavam rho +0.07 gap -0.22 | poetic rho +0.01 gap -0.40
A1-A2 n=64: readab rho   –   gap -1.19 | compre rho +0.23 gap -1.03 | lexica rho +0.31 gap -0.45 | bhavam rho +0.08 gap -0.62 | poetic rho +0.05 gap +0.02
A4-A2 n=71: readab rho   –   gap -0.65 | compre rho +0.19 gap +0.00 | lexica rho +0.15 gap +0.06 | bhavam rho -0.18 gap -0.45 | poetic rho -0.15 gap +0.42
```

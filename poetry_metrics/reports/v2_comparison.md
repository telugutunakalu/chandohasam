# Versions 2.0 of anuprāsa, mādhurya and prasāda: a score that no poet moves

Date: 2026-10-01. Candidates: anuprāsa 2.0, mādhurya 2.0 and prasāda 2.0, beside
the defaults anuprāsa 1.0, mādhurya 1.1 and prasāda 1.0.
Script: [`compare_versions.py`](../compare_versions.py) (about 75 s, seed 42).
Numbers: [`outputs/v2_comparison.json`](../outputs/v2_comparison.json).
Version 1 stays the default in every script, report and in the paper until a
decision is made.

## The question

If a new poet is put into the reference, does the score of anyone's poem change?
A version-1 metric that takes a constant from the four dataset files scores
every poem relative to whoever is in those files (58% of their poems are
Pothana's). Version 2 of each metric puts no statistic of those files into a
score or a label. The percentile printed beside each score is still against the
four files, and says so.

Ojas already moved to 2.0 in place (spec 04, §10) and is not compared here. The
chandas distance keeps its chance rate, which belongs to each meter.

## The answer

| | taken from the four files in version 1 | version 2 instead | score | labels kept | a new poet relabels, version 1 |
|---|---|---|---|---|---|
| **anuprāsa** | the chance model's consonant frequencies | the frequencies of the language reference: the crawled verse that prasāda's model was built from (362,247 poems, none from the four files), frozen | z falls by 0.07 on average; Spearman 0.9999 | 99.1% of lines, 98.9% of poems | 0.05–0.32% of lines |
| **mādhurya** | the rubric's cut points (10th, 30th, 70th, 90th percentiles) | cuts symmetric about M = 0, the outer ones at the M of the treatise's example of saukumārya (4.62) | the same number | 66.4% of poems, 84.6% of lines | 1.2–4.4% of poems |
| **prasāda** | the rubric's cut points (10th, 30th, 70th, 90th percentiles) | the treatise's example of prasāda (4.59) and of a word found only in śāstras (apratīta, 4.15), in thirds | the same number, from the same frozen model | 62.1% of poems, 36.1% of lines | 4.9–23.5% of poems |

"A new poet relabels": each corpus in turn is left out of the reference,
version 1 is rebuilt from the other three, and its poems are scored again.
Version 2 rebuilt the same way relabels none, for all three metrics: none of its
constants has an input from the four files.

In short:
1. **Anuprāsa cannot be made free of every corpus.** "Repetition beyond chance"
   needs the language's sound frequencies. Taken from the poem itself, the
   treatise's own example of vṛttyanuprāsa scores z = 0.17 (§1.5). Version 2
   takes them from the language instead, and every check gives the same answer
   as version 1.
2. **Mādhurya and prasāda only change their labels.** Their scores were already
   free of the four files. The new rubrics are anchored to the treatise:
   mādhurya's ten soft and harsh examples keep their labels, and prasāda's two
   examples of unfamiliar words both read obscure.
3. **Prasāda keeps a corpus by definition.** The treatise defines it by
   well-known words (4.57); the frozen model is the record of what is well
   known, and version 2 never rebuilds it.

## 1. Anuprāsa

### 1.1 What changes

Only q and r, the chances that two (three) consonants drawn independently are
the same sound. They are now computed from the akshara counts of prasāda's
model (`baselines/prasada_ngrams.tsv.gz`: 21,165,312 aksharas, 24,717,850
consonant tokens) with version 1.0's pseudo-count. Splitting the four dataset
files word by word, as that model was built, gives the same count of every
consonant (1,044,872 tokens in all) as splitting them line by line, as
anuprāsa does.

| level | q, version 1 | q, version 2 | r, version 1 | r, version 2 |
|---|---:|---:|---:|---:|
| varga (headline) | 0.078937 | 0.079706 | 0.007154 | 0.007327 |
| varna | 0.057581 | 0.058638 | 0.004182 | 0.004399 |

The statistic, the rubric (the one-sided 5%, 1% and 0.1% points of the
standard normal) and the output are version 1.0's.

### 1.2 Agreement

Spearman between the versions' z is 0.9999, for poems and for lines. q is 1%
higher, so z is a little lower (by 0.07 for the mean poem), and every change of
level is one step down: 276 lines from weak to none, 192 from marked to weak, 86
from strong to marked, out of 61,227. Lines at or above "weak": Bhāgavatamu
8.27% → 7.82%, Vemana 9.29% → 8.77%, Kuchimanchi 11.87% → 11.50%, Chandassu
9.78% → 9.31%.

### 1.3 The checks the metric was admitted with

| check | version 1 | version 2 |
|---|---|---|
| words shuffled, mean z at 0 / 10 / 25 / 50 / 100% | 0.69, 0.65, 0.56, 0.42, 0.33: declines | 0.62, 0.58, 0.49, 0.36, 0.27: declines |
| meter broken | rises (sign z 7.25) | rises (7.25) |
| filler | rises (64.5 at full strength) | rises (63.8) |
| synonyms swapped | declines (−9.45) | declines (−9.56) |
| nonsense control: chance a constrained poem scores above a real one | 0.684–0.947 | 0.684–0.947 |
| pilot grid, sound figures against meaning figures (AUC) | varga 0.776, varna 0.808 | varga 0.776, varna 0.808 |
| treatise 4.77 (vṛttyanuprāsa), varna | z 3.18, 96.6th percentile, weak; ష carries lines 1–3 | z 2.97, 96.4th percentile, weak; ష carries lines 1–3 |
| Kāvyādarśa 1.72 (క్ష repeated), varna | z 2.41, marked | z 2.29, weak |

The version-1 column reproduces `outputs/degradation_protocol.json` and
`outputs/samples_analysis.json` exactly (checked by the script).

### 1.4 A new poet

| corpus as the new poet | its share of the reference | q without it | version 1: lines relabelled | version 1: poems relabelled |
|---|---:|---:|---:|---:|
| bhagavatam | 58.0% | 0.07946 | 0.28% | 0.38% |
| vemana | 9.2% | 0.07902 | 0.32% | 0.17% |
| kuchimanchi_timmakavi | 12.9% | 0.07881 | 0.05% | 0.18% |
| chandassu | 19.9% | 0.07890 | 0.08% | 0.08% |

Version 1's dependence on the reference was already small: consonant
frequencies are a property of the language more than of a poet, and the score
uses only two numbers made from them.

### 1.5 Why the frequencies cannot come from the poem itself

The one way to need no corpus at all is to make the poem its own chance model:
deal the poem's own consonants at random over its consonant slots and ask
whether a line repeats more than that deal would. Two forms were tried, with the
exact mean and variance of the permutation (tested against full enumeration in
`tests/test_v2_candidates.py`): pairs anywhere in a line, and pairs at most 5
aksharas apart, the nearness that Daṇḍin asks of anuprāsa (1.55,
*pūrvānubhavasaṃskārabodhinī yady adūratā*; 1.58) and the distance that
Barbadikar & Kulkarni (2024, §5) allow a single letter's repeat.

| check | version 1 | poem's own sounds, whole line | poem's own sounds, within 5 aksharas |
|---|---|---|---|
| treatise 4.77, poem z | 1.83 (varga) | 0.17 | 0.46 |
| pilot grid AUC, sound against meaning figures | 0.776 | 0.606 | 0.268 |
| real beats word salad, four corpora | 62.5–78.4% | 50.8–75.0% | 40.4–58.9% |
| Spearman with version 1 (poems) | 1 | 0.63 | 0.42 |
| words shuffled | declines | declines | no response |
| meter broken | rises | no response | rises |
| filler | rises | **no response** | rises |
| synonyms swapped | declines | no response | no response |

With the whole line as the window, the poem's own sounds give a metric that
filler cannot fool: a poem of one sound repeats exactly as much as its own
sounds predict. But it cannot see a sound carried through the whole poem, which
is how the treatise defines vṛttyanuprāsa ("ఒక్కవర్ణంబు కడదాక నుద్ధరింపఁ",
4.76): its own example reads as no anuprāsa, and the swap of the poet's words
for their glosses, the suite's best evidence that anuprāsa measures the poet's
choice, no longer registers. The window of 5 aksharas fails outright. Telugu
avoids the same consonant in adjacent syllables (spec 01, §6.4), and a window
that short gives adjacent syllables much of its weight.

## 2. Mādhurya

### 2.1 The rubric

M = I − P is unchanged, so every check on the score is unchanged: 24 of 24
soft/harsh pairs of the texts in order, tender above fierce poems (AUC
0.61–0.68), the degradation verdicts and the nonsense control.

| | harsh | leaning harsh | balanced | leaning soft | soft |
|---|---|---|---|---|---|
| version 1, poems | < −0.283 | −0.283 to −0.123 | −0.123 to 0.049 | 0.049 to 0.156 | ≥ 0.156 |
| version 1, lines | < −0.464 | −0.464 to −0.158 | −0.158 to 0.125 | 0.125 to 0.300 | ≥ 0.300 |
| version 2, lines and poems | < −0.394 | −0.394 to −0.131 | −0.131 to 0.131 | 0.131 to 0.394 | ≥ 0.394 |

Version 2 uses the scale's own zero: the class weights are symmetric (+1, +½, 0,
−½, −1), so at M = 0 the soft and the harsh weights cancel. The outer cuts are
the M of the treatise's example of saukumārya (4.62, M = 0.394) and its mirror;
the inner cuts are a third of the way.

### 2.2 Labels

| corpus | version 1 (harsh … soft) | version 2 (harsh … soft) |
|---|---|---|
| bhagavatam | 10.2 / 20.4 / 40.3 / 19.8 / 9.3 | 4.4 / 24.6 / 58.1 / 12.8 / 0.1 |
| vemana | 7.1 / 15.0 / 32.5 / 27.1 / 18.3 | 3.7 / 17.4 / 54.9 / 23.7 / 0.3 |
| kuchimanchi_timmakavi | 10.8 / 21.3 / 39.7 / 18.3 / 9.9 | 4.6 / 25.8 / 56.0 / 13.6 / 0.0 |
| chandassu | 10.0 / 20.5 / 42.1 / 18.5 / 8.9 | 4.5 / 24.5 / 59.0 / 11.9 / 0.0 |
| all lines | 9.7 / 20.3 / 38.5 / 21.3 / 10.2 | 12.9 / 20.4 / 36.8 / 27.2 / 2.8 |

Percent of poems (last row: of lines). Under version 2 most verse is balanced,
and "soft" is kept for texture at least as soft as the treatise's showcase,
which only 8 of the 12,704 poems reach (version 1 called the softest tenth
soft). Vemana stays the softest corpus.

### 2.3 The texts' examples

All ten soft and harsh examples keep their version-1 labels: the treatise's
4.62 soft; 4.21, Daṇḍin 1.72 and Mammaṭa's three harsh examples harsh; the
commentary's Tikkana verse leaning harsh; Mammaṭa's 8.74, Daṇḍin's 1.70 and the
commentary's Peddana verse balanced in both versions. Of the six examples
scored for information, three move one step: the treatise's 4.61 from leaning
soft to balanced, Mammaṭa's 8.76 from harsh to leaning harsh, Daṇḍin's slack
1.43 from soft to leaning soft.

### 2.4 A new poet

Version 1 rebuilt without each corpus relabels 4.4% of the Bhāgavatamu's poems,
2.8% of Vemana's, 1.2% of Kuchimanchi's and 1.7% of Chandassu's (lines: 1.7–4.3%).

### 2.5 Rubrics considered and not taken

| rubric | poems (harsh … soft) | harsh examples of the texts read balanced or softer |
|---|---|---|
| version 2: symmetric about 0, outer cuts ±M(4.62) | 4.4 / 24.1 / 57.7 / 13.8 / 0.1 | none |
| thirds between the treatise's harsh (4.21) and soft (4.62) examples, as ojas 2.0 does | 0.0 / 0.4 / 24.4 / 75.1 / 0.1 | 4 of 6: Mammaṭa's three, Tikkana |
| four anchors: 4.21, Tikkana, Peddana, 4.62 | 0.0 / 12.7 / 24.4 / 62.9 / 0.1 | Tikkana |

The treatise's harsh example is one compound built to show the defect (M =
−1.25), harsher than all but 3 of the 12,704 poems; a cut there leaves those 3
in the harsh band.

### 2.6 Generated poems

Of the 4,995 constrained poems, version 1 calls 35.5% harsh and 11.9% soft;
version 2 calls 26.9% harsh and 0.7% soft (real verse: 4.4% and 0.1%).

## 3. Prasāda

### 3.1 The rubric

H and the model are unchanged, so every check on the score is unchanged: the 5
contrasts of the texts in order, the degradation verdicts, and the chance that
a constrained poem is clearer than a real one (0.005–0.08).

| | obscure | leaning obscure | ordinary | leaning clear | clear |
|---|---|---|---|---|---|
| version 1, poems | ≥ 7.06 | 6.33 to 7.06 | 5.54 to 6.33 | 5.12 to 5.54 | < 5.12 |
| version 1, lines | ≥ 7.62 | 6.49 to 7.62 | 5.26 to 6.49 | 4.59 to 5.26 | < 4.59 |
| version 2, lines and poems | ≥ 6.56 | 6.14 to 6.56 | 5.73 to 6.14 | 5.31 to 5.73 | < 5.31 |

Bits per akshara; lower is clearer. The clear end is the treatise's example of
prasāda (4.59, H = 5.31), which itself reads "leaning clear", as in version 1.
The obscure end is its example of apratīta, a word found only in the śāstras
and purāṇas (4.15, H = 6.56). Of the four word defects set against prasāda
(spec 05, §1), apratīta and aprayukta (a word poets do not use, 4.5) lie in the
form of the word, which the model can see; the cut is at the clearer of the
two, so both read obscure.

### 3.2 Labels

| corpus | version 1 (obscure … clear) | version 2 (obscure … clear) |
|---|---|---|
| bhagavatam | 8.4 / 15.1 / 40.6 / 23.1 / 12.8 | 17.4 / 13.2 / 21.9 / 25.7 / 21.8 |
| vemana | 1.0 / 10.0 / 42.3 / 29.7 / 17.0 | 5.5 / 12.2 / 22.9 / 30.2 / 29.3 |
| kuchimanchi_timmakavi | 18.1 / 35.9 / 37.0 / 7.5 / 1.5 | 41.0 / 24.0 / 20.6 / 10.8 / 3.6 |
| chandassu | 13.5 / 28.5 / 39.0 / 14.8 / 4.2 | 31.0 / 19.7 / 21.4 / 18.6 / 9.4 |
| all poems | 10 / 20 / 40 / 20 / 10 | 22.1 / 15.8 / 21.7 / 22.8 / 17.6 |
| all lines | 10 / 20 / 40 / 20 / 10 | 28.1 / 11.5 / 14.2 / 14.5 / 31.7 |

The order of the corpora is the same (Vemana clearest, Kuchimanchi hardest).
The version-2 bands are narrower than version 1's middle band (0.42 bits each),
so more poems sit in the outer bands, and lines, which vary more than poems,
more still.

### 3.3 The texts' examples

| example | H | version 1 | version 2 |
|---|---:|---|---|
| treatise 4.59, prasāda | 5.31 | leaning clear | leaning clear |
| 4.8, asamartha (sense) | 5.68 | ordinary | leaning clear |
| 4.17, kliṣṭa (sense) | 6.04 | ordinary | ordinary |
| 4.15, apratīta (form) | 6.56 | leaning obscure | obscure |
| 4.5, aprayukta (form) | 8.82 | obscure | obscure |
| Daṇḍin 1.45, prasāda (Sanskrit) | 9.47 | obscure | obscure |
| Daṇḍin 1.46, learned and not current (Sanskrit) | 13.25 | obscure | obscure |

### 3.4 The gate on nonsense

The reports use "ordinary or clearer" as prasāda's gate on generated text.

| | version 1 | version 2 |
|---|---:|---:|
| constrained poems passing (of 4,995) | 200 | 139 |
| real poems passing | 70.0% | 62.1% |
| constrained poems rated obscure | 90.8% | 94.6% |

### 3.5 A new poet

Version 1 rebuilt without each corpus relabels 23.5% of the Bhāgavatamu's poems
(its cuts move from 5.12–7.06 to 5.26–7.17 bits), 4.9% of Vemana's, 9.7% of
Kuchimanchi's and 8.2% of Chandassu's. Not measured: rebuilt for a new poet,
version 1 would also retrain its model without that poet's poems; version 2
never retrains.

### 3.6 The anchor considered and not taken

With aprayukta (4.5, H = 8.82) as the obscure end, the bands are 1.17 bits
wide: 0.3% of real poems are obscure and 57.5% leaning clear, the treatise's
apratīta example reads "ordinary", and 711 constrained poems pass the gate.

## What follows

1. **Anuprāsa: replace.** Every check gives the same answer, labels move for
   1% of lines, and the dependence on the reference goes from small to none. The
   carriers (Benner's per-sound test) use the same frozen frequencies.
2. **Mādhurya: replace, if a label that means the same for every poet matters
   more than version 1's fixed shares of verse in each band (10, 20, 40, 20,
   10%).** The score is unchanged, and the texts' ten examples keep their labels.
   The cost is that "soft" becomes rare.
3. **Prasāda: replace.** The score is unchanged, both form defects of the
   treatise now read obscure, and the gate rejects more of the nonsense. Version
   1's rubric was the most corpus-bound of the three (23.5% of the
   Bhāgavatamu relabelled).
4. **If replaced,** the version-2 code moves into `anuprasa.py`, `madhurya.py`
   and `prasada.py` as ojas 2.0 did, and these follow: `samples_analysis.py`,
   `degradation_protocol.py` and their reports (the gate's 200 becomes 139); the
   README and specs 01, 03, 05; and in the paper the metric table's rubric
   column, the gate figure and the results appendix.

## Limits

- **Each anchor is one example.** A verse or a line chosen by the treatise to
  show a quality; another example of the same quality would move the cuts. The
  bands are descriptions, not grades.
- **Version 2 gives lines the poems' cuts.** Lines vary more, so more of them
  fall in the outer bands (prasāda: 28% of lines obscure, 32% clear).
- **The language reference is crawled verse,** a third of it modern. For
  anuprāsa, "chance" is now Telugu verse at large rather than the four files;
  for prasāda, "well known" was already that.
- **A poet who is in the crawl is seen by prasāda's model.** Version 1 removes
  the dataset's own poems from the model when it is rebuilt; version 2 does not
  rebuild, so a new poet's poems that are in the crawl stay in its counts.
- **None of this is validated against human ratings,** in either version.

## References

- Barbadikar, A. V. & Kulkarni, A. (2024). Anuprāsa Identifier and Classifier: A computational tool to analyze Sanskrit figure of sound. *Proc. 7th International Sanskrit Computational Linguistics Symposium*, 102–112.
- Daṇḍin. *Kāvyādarśa*, pariccheda 1 (1.55, 1.58). GRETIL e-text.
- Rāmarājabhūṣaṇuḍu (Bhaṭṭumūrti). *Kāvyālaṅkārasaṅgrahamu*, āśvāsa 4 (4.5, 4.15, 4.21, 4.57–62, 4.76–77), 1920 edition, Telugu Wikisource.

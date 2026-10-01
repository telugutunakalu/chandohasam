# Metric 5 — *prasāda* (clarity index)

| | |
|---|---|
| Script | [`prasada.py`](../prasada.py) (version 1.0) |
| Shared code | [`common/phonology.py`](../common/phonology.py), [`common/corpus.py`](../common/corpus.py) |
| Baseline | [`baselines/prasada_baseline.json`](../baselines/prasada_baseline.json), [`prasada_ngrams.tsv.gz`](../baselines/prasada_ngrams.tsv.gz) (4.7 MB), [`prasada_words.tsv.gz`](../baselines/prasada_words.tsv.gz) (1.7 MB), built by `python3 prasada.py build-baseline` |
| Validation | [`outputs/prasada_validation.json`](../outputs/prasada_validation.json), built by `python3 prasada.py validate` ([`validation_prasada.py`](../validation_prasada.py)) |
| Exemplars | [`fixtures/classical_exemplars.json`](../fixtures/classical_exemplars.json): 5 contrasts the classical texts draw |
| Tests | [`tests/test_prasada.py`](../tests/test_prasada.py): 15 tests |
| Proposal | Section 6 and Appendix E.1 (Tier 1), `proposal/chandohasam_full_proposal_v3.md` |

## 1. What it measures

How readily the text is recognised as known language. The proposal asks for:

> How easily the text parses. Proxies: average word frequency, and perplexity under a language
> model — how surprised a trained model is by the text; lower surprise indicates plainer text.
> (Appendix E.1)

**What the classical texts call prasāda:**

| source | definition |
|---|---|
| The treatise, 4.57 | "ప్రసిద్ధపదంబుల నలఘూక్తి ప్రసాదము": an expression in well-known words |
| Daṇḍin, *Kāvyādarśa* 1.45 | *prasādavat prasiddhārtham … pratītisubhagaṃ vacaḥ*: of well-known meaning, pleasing because understood at once |
| Mammaṭa, *Kāvyaprakāśa* 8.76 | *śrutimātreṇa … arthapratyayaḥ*: the meaning is grasped on hearing alone; the quality common to all rasas |
| Vāmana, *Kāvyālaṅkārasūtra* 3.2.3 | *arthavaimalyaṃ prasādaḥ*: clearness of meaning |

Its opposites in the treatise are word defects: a word poets do not use
(*aprayukta*, 4.5), an unestablished usage (*asamartha*, 4.8), a word found
only in śāstras (*apratīta*, 4.15), a far-fetched expression (*kliṣṭa*, 4.17).

Both of the proposal's proxies are computed. The headline is the second, on
aksharas, because it does not depend on how words are spaced or fused (§3).

## 2. Sources, and what each contributes

| Source | What is taken from it |
|---|---|
| Rāmarājabhūṣaṇuḍu, *Kāvyālaṅkārasaṅgrahamu*, 4.5, 4.8, 4.15, 4.17, 4.57, 4.59 (1920 edition) | Prasāda as well-known words, its example (4.59), and the examples of the four word defects that are its opposite (§7.1). |
| Daṇḍin 1.45–46; Mammaṭa 8.76; Vāmana 3.2.3 (GRETIL) | The definitions above. Daṇḍin's pair: the well-known (1.45) against the "learned but not current" (*nātirūḍham*, 1.46). Mammaṭa's statement that prasāda suits every rasa, which lets the rubric grade (§4). |
| Hale (2001), *A probabilistic Earley parser as a psycholinguistic model*, NAACL | **Surprisal**, −log P of a unit given what came before, as the measure of the effort of taking it in. |
| Smith & Levy (2013), *The effect of word predictability on reading time is logarithmic*, Cognition 128 | The evidence: reading time is linear in surprisal. This is what makes mean surprisal a measure of how easily a text is read. |
| Witten & Bell (1991), *The zero-frequency problem*, IEEE Trans. Inf. Theory 37; Chen & Goodman (1999), *An empirical study of smoothing techniques for language modeling*, Computer Speech & Language 13 | The probability model: counts, with the mass reserved for unseen events set by the number of distinct continuations, and lower orders interpolated in. |
| van Heuven, Mandera, Keuleers & Brysbaert (2014), *SUBTLEX-UK*, Q. J. Exp. Psychol. 67 | The **Zipf scale** of word frequency: log10 of frequency per billion words, with counts + 1 so that unseen words have a value. |
| Dale & Chall (1948), *A formula for predicting readability* | The share of words on a list of familiar words as a predictor of difficulty: the treatise's "well-known words" as a count. |
| Kao & Jurafsky (2012), *A computational analysis of style, affect, and imagery in contemporary poetry*, CLfL | Average log word frequency as a feature of a poem's diction, "a measure of difficulty". |

## 3. Algorithm

### 3.1 The reference: verse the scored text is not in

The model is built from a collection of 367,627 Telugu poems
(`diffusion_finetuning/data/records/train.jsonl`, the Padyarchana training
split; the Bhāgavatamu is held out of it). Poems that are also in the four
dataset files are removed by matching first lines, which leaves **362,247
poems**: 21,165,312 aksharas of 9,828 types, and 5,711,615 words of 1,700,762
types. So every poem scored here, real or generated, is new to the model.

### 3.2 Headline: surprisal under an akshara trigram model

A line is read as a stream of aksharas with the spaces taken out. Each akshara
is predicted from the two before it; the first two of a line are predicted from
the line start.

```
H = −(1/N) · Σ_t log2 P(a_t | a_(t−2), a_(t−1))          bits per akshara
perplexity = 2^H
```

P is a count model with Witten–Bell interpolation:

```
P(a | g,h) = λ3 · c(g,h,a)/c(g,h) + (1 − λ3) · P(a | h)        λ3 = c(g,h) / (c(g,h) + T(g,h))
P(a | h)   = λ2 · c(h,a)/c(h)     + (1 − λ2) · P(a)            λ2 = c(h)   / (c(h)   + T(h))
P(a)       = λ1 · c(a)/N          + (1 − λ1) / (V + 1)         λ1 = N / (N + V)
```

c counts occurrences in the reference. T(·) is the number of distinct aksharas
seen after a context: a context followed by many different aksharas keeps more
mass for the unseen. N and V are the akshara tokens and types. An akshara never
seen gets 1/(V + 1) of the reserved mass.

To keep the files small, bigrams seen once and trigrams seen fewer than three
times are not stored (209,769 bigrams and 920,179 trigrams are). The model is
computed from the stored counts, so it is a proper distribution.

**Why aksharas and not words.** Verse fuses words by sandhi and compounds, and
editions space them differently. The reference has 1.7 million word types in
5.7 million tokens, and a third of the words of real verse are not in it at
all (§7.5). Akshara sequences do not have this problem: a fused or unspaced
word is still made of familiar stretches.

### 3.3 Second number: word frequency

For each printed word w:

```
Zipf(w) = log10( (c(w) + 1) / ((T + W) / 10^6) ) + 3
```

T and W are the word tokens and types of the reference. A word seen once per
million words has Zipf 3; an unseen word has Zipf 2.13 here. Words seen once in
the reference are stored as unseen. Reported per poem: the mean Zipf (the
proposal's "average word frequency") and the share of words found in the
reference (the familiar-word share).

### 3.4 Poem, and explanation

The poem's H is the mean over all its aksharas. For each line the output names
the three aksharas with the highest surprisal, with the two aksharas before
each, and the words not found in the reference.

## 4. Rubric

On H, against the four dataset corpora (their 10th, 30th, 70th and 90th
percentiles). Lower H is clearer.

| level | label | share of reference | line H (bits) | poem H (bits) |
|---:|---|---|---|---|
| 4 | clear | clearest 10% | < 4.59 | < 5.12 |
| 3 | leaning clear | 10–30% | 4.59 to 5.26 | 5.12 to 5.54 |
| 2 | ordinary | 30–70% | 5.26 to 6.49 | 5.54 to 6.33 |
| 1 | leaning obscure | 70–90% | 6.49 to 7.62 | 6.33 to 7.06 |
| 0 | obscure | hardest 10% | ≥ 7.62 | ≥ 7.06 |

**Here a higher level is better.** Mammaṭa calls prasāda the quality common to
every rasa (8.76), unlike mādhurya and ojas, which suit some and not others.

For scale: the mean over real verse is 6.0 bits (perplexity 64). A poem with
its aksharas shuffled is at 11.5 bits.

## 5. Output

`python3 prasada.py score --text "…"` prints one JSON object per poem:

| field | meaning |
|---|---|
| `score`, `label` | rubric level 0–4 of the poem, and its label |
| `surprisal`, `perplexity` | H in bits per akshara, and 2^H |
| `percentile` | place among reference poems by clarity; 100 is the clearest |
| `zipf`, `known_word_share` | mean Zipf of the printed words; share found in the reference |
| `lines[]` | the same per line, plus `hard_spots[]` (akshara, the two before it, its bits) and `unknown_words[]` |

## 6. Validation

All numbers come from `outputs/prasada_validation.json` (seed 42) and, for
generated poems, `outputs/samples_analysis.json`.

### 6.1 The contrasts the classical texts draw

| clear | obscure | who says so | H, clear | H, obscure | in order |
|---|---|---|---:|---:|---|
| Treatise 4.59, prasāda | 4.5, a word poets do not use | the treatise | 5.31 | 8.82 | yes |
| Treatise 4.59 | 4.15, words found only in śāstras | the treatise | 5.31 | 6.56 | yes |
| Treatise 4.59 | 4.17, a far-fetched expression | the treatise | 5.31 | 6.04 | yes |
| Treatise 4.59 | 4.8, an unestablished usage | the treatise | 5.31 | 5.68 | yes |
| Kāvyādarśa 1.45, well-known | 1.46, learned but not current | Daṇḍin | 9.47 | 13.25 | yes |

All 5 are in order. The treatise's prasāda example is at the 82nd percentile
of reference poems (leaning clear); its unused-word example is at the 1st
(obscure). The last two treatise rows are close, and they should be: those
defects lie in the sense the word is given, which a model of forms cannot see.
Daṇḍin's pair is Sanskrit, scored with the Telugu model, so both read as
obscure in absolute terms; only their order is meaningful.

### 6.2 Degradation controls: the metric declines when the verse is degraded

The proposal admits a metric only if it does (Appendix E). Each control keeps
the number of words or aksharas in every line.

| corpus | real | words shuffled | aksharas shuffled | real clearer than word-shuffled | real clearer than akshara-shuffled |
|---|---:|---:|---:|---:|---:|
| bhagavatam | 5.90 | 6.46 | 11.50 | 96.2% | 100% |
| vemana | 5.64 | 6.06 | 10.77 | 91.8% | 100% |
| kuchimanchi_timmakavi | 6.47 | 7.07 | 11.27 | 96.1% | 100% |
| chandassu | 6.22 | 6.77 | 11.67 | 98.0% | 100% |

These are two of the proposal's degradations. The run of all four, at four
strengths, is in [`reports/degradation_protocol.md`](../reports/degradation_protocol.md):
prasāda declines under the shuffle, a broken meter and filler, and rises when
words are replaced by their glosses, which are plainer.
Word shuffling is detected although every word is kept, because the aksharas
across the new word boundaries are unfamiliar.

### 6.3 Generated poems: the nonsense control

The constrained-decoding poems of `samples/json` are in meter and mostly not
made of real words. The proposal requires such a control to be rejected.

| | real verse | E4B | 26B-A4B | DiffusionGemma |
|---|---:|---:|---:|---:|
| constrained: mean H (bits) | 6.01 | 10.6 – 11.2 | 10.6 – 11.4 | 11.9 – 12.6 |
| constrained: poems in the "obscure" band | 10% | 84 – 91% | 83 – 91% | 94 – 99% |
| constrained: chance a generated poem is harder than a real one | — | 0.94 – 0.97 | 0.92 – 0.96 | 0.98 – 0.995 |
| free baseline: mean H | 6.01 | 5.63 | 5.38 | 6.72 |

Of 4,995 constrained poems, 200 (4%) are "ordinary" or clearer. Within the
constrained poems H falls as the share of real words rises (Spearman −0.55 to
−0.63). Free text from the two autoregressive models is clearer than classical
verse: it is plain modern Telugu.

**What it does not catch.** A language model is not surprised by repetition. A
generated line that is almost all మ scores 6.96 bits, only "leaning obscure"
on the line scale. Of the 500 most alliterative constrained poems, 463 (93%)
are rated obscure and 15 are "ordinary" or clearer; of the 200 constrained
poems that are "ordinary" or clearer, 42 repeat a whole line. These need the
repetition defect of metric 7.

### 6.4 The order of the model

| model | mean H, bhagavatam | real clearer than word-shuffled |
|---|---:|---:|
| unigram | 7.94 | 0% |
| bigram | 6.46 | 80 – 91% |
| **trigram** | 5.90 | 94 – 98% |

A unigram model cannot see order at all. The trigram separates best. (The
percentages are over the four corpora, with a shuffle drawn separately from
that of §6.2.)

### 6.5 Why the word-level numbers are secondary

| corpus | mean Zipf | words found in the reference |
|---|---:|---:|
| bhagavatam | 3.40 | 62% |
| vemana | 3.47 | 69% |
| kuchimanchi_timmakavi | 3.54 | 73% |
| chandassu | 3.38 | 64% |

A third of the printed words of real verse are not in a reference of 5.7
million words: they are fused, inflected or spaced differently. The treatise's
own prasāda example has 47% of its words found, because the 1920 edition
prints its words joined. H and mean Zipf agree only loosely (Spearman −0.24 to
−0.37).

### 6.6 The corpora, and relations to the other metrics

| corpus | mean H | obscure | leaning obscure | ordinary | leaning clear | clear |
|---|---:|---:|---:|---:|---:|---:|
| vemana | 5.64 | 1.0% | 10.0% | 42.3% | 29.7% | 17.0% |
| bhagavatam | 5.90 | 8.4% | 15.1% | 40.6% | 23.1% | 12.8% |
| chandassu | 6.22 | 13.5% | 28.5% | 39.0% | 14.8% | 4.2% |
| kuchimanchi_timmakavi | 6.47 | 18.1% | 35.9% | 37.0% | 7.5% | 1.5% |

Vemana is the clearest. Kuchimanchi's pure-Telugu verse is the hardest for the
model: it avoids the Sanskrit vocabulary that most verse shares.

Spearman of H with the other metrics (poems): conjunct rate 0.25 to 0.42; ojas
0.08 to 0.28 (ojas 2.0); mādhurya −0.11 to −0.22; anuprāsa z −0.06 to 0.04. Dense and
harsh verse is somewhat harder; alliteration is unrelated.

### 6.7 Lines for reading

| clearest lines | H | hardest lines | H |
|---|---:|---|---:|
| హస్తముల్ మొగిచి యిట్లనియె బ్రీతి | 2.90 | ల్మగల్‌ గ్రమ్మఱ న్వాలి మన్ఱేని మెట్టున్‌ | 14.44 |
| అనియిట్లు విన్నవించిన | 3.06 | తీపైన బేషక్ మఠా పఠాన్ తురకి క | 13.15 |
| అని పలికి యంతకంతకుఁ | 3.21 | మాలిన్వాలిన్ దశాస్యమానోన్మూలిన్. | 13.12 |
| తలిదండ్రు లన్నదమ్ములు | 3.31 | యేదగాండ్లంటరో యీండ్లింట పొగవెల్ల | 13.02 |
| అరిషడ్వర్గంబులచే | 3.52 | ఒడల బూడ్దెపూత యొంటిరోఁత | 10.82 |

The clearest are the stock phrases of narrative verse. The hardest are dialect,
loanwords and rare formations.

## 7. Decisions and limitations

1. **Familiar form, not meaning.** H says whether the sound sequences are those of known Telugu verse. It cannot tell a word used in a strange sense (§6.1), and it cannot tell sense from fluent nonsense made of real words.
2. **"Well known" means well known in verse.** The reference is a verse collection, two-thirds classical and one-third modern. A word common in today's prose and absent from verse reads as unfamiliar. A second reference from modern prose (the Wikipedia and Sangraha text in `pretraining_datasets`) is a possible addition.
3. **Repetition is not penalised** (§6.3).
4. **Spaces are ignored in H** and used in the word numbers.
5. **Pruned counts.** Rare bigrams and trigrams are dropped. In a check during development (not among the outputs), keeping every n-gram lowered the mean H of real verse by 0.3 bits and moved the chance figures of §6.3 by about 0.01.
6. **Rebuilding needs the verse collection**, which is not tracked in git (1 GB). The three baseline files are what scoring needs.
7. **The reference excludes the dataset poems by first line.** A poem whose first line differs between editions would not be removed.
8. **Not yet validated against human ratings.** Items 2 and 3 of the proposal's rubric (understood at once; words understood) are the ones to correlate it with.

## 8. References

See [`../references.bib`](../references.bib) (keys in brackets).

- Chen, S. F. & Goodman, J. (1999). An empirical study of smoothing techniques for language modeling. *Computer Speech & Language* 13(4), 359–394. [`chen1999smoothing`]
- Dale, E. & Chall, J. S. (1948). A formula for predicting readability. *Educational Research Bulletin* 27. [`dale1948readability`]
- Daṇḍin. *Kāvyādarśa*, pariccheda 1. GRETIL e-text. [`dandin_kavyadarsa`]
- Hale, J. (2001). A probabilistic Earley parser as a psycholinguistic model. *Proceedings of NAACL 2001*. ACL Anthology N01-1021. [`hale2001earley`]
- Kao, J. & Jurafsky, D. (2012). A computational analysis of style, affect, and imagery in contemporary poetry. *Proceedings of the NAACL-HLT 2012 Workshop on Computational Linguistics for Literature*. ACL Anthology W12-2502. [`kao2012style`]
- Mammaṭa. *Kāvyaprakāśa*, ullāsa 8. GRETIL e-text. [`mammata_kavyaprakasa`]
- Rāmarājabhūṣaṇuḍu (Bhaṭṭumūrti). *Kāvyālaṅkārasaṅgrahamu* (*Narasabhūpālīyamu*), 1920 edition, Telugu Wikisource. [`ramarajabhushana_kas1920`]
- Smith, N. J. & Levy, R. (2013). The effect of word predictability on reading time is logarithmic. *Cognition* 128(3), 302–319. [`smith2013predictability`]
- van Heuven, W. J. B., Mandera, P., Keuleers, E. & Brysbaert, M. (2014). SUBTLEX-UK: A new and improved word frequency database for British English. *The Quarterly Journal of Experimental Psychology* 67(6), 1176–1190. [`vanheuven2014subtlex`]
- Vāmana. *Kāvyālaṅkārasūtra* with the author's gloss. GRETIL e-text. [`vamana_kavyalankarasutra`]
- Witten, I. H. & Bell, T. C. (1991). The zero-frequency problem: Estimating the probabilities of novel events in adaptive text compression. *IEEE Transactions on Information Theory* 37(4), 1085–1094. [`witten1991zero`]

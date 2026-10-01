# Metric 4 — *ojas* (word-density index)

| | |
|---|---|
| Script | [`ojas.py`](../ojas.py) (version 2.0; §10 gives the change from 1.0) |
| Shared code | [`common/phonology.py`](../common/phonology.py), [`common/corpus.py`](../common/corpus.py) |
| Baseline | [`baselines/ojas_baseline.json`](../baselines/ojas_baseline.json), built by `python3 ojas.py build-baseline`: the rubric's anchored cuts and the reference distributions for the percentile. The score itself needs no baseline. |
| Validation | [`outputs/ojas_validation.json`](../outputs/ojas_validation.json), built by `python3 ojas.py validate` ([`validation_ojas.py`](../validation_ojas.py)) |
| Exemplars | [`fixtures/classical_exemplars.json`](../fixtures/classical_exemplars.json): 8 contrasts the classical texts draw |
| Tests | [`tests/test_ojas.py`](../tests/test_ojas.py): 17 tests |
| Proposal | Section 6 and Appendix E.1 (Tier 1), `proposal/chandohasam_full_proposal_v3.md` |

## 1. What it measures

How long the words are and how tightly the syllables are bound. The proposal
asks for:

> Long compounds, heavy conjunct clusters, aspirated stops: average compound length and conjunct
> clusters per syllable. (Appendix E.1)

**What the classical texts call ojas.** They give it two sources, and the
proposal's two terms are these two:

| source | definition | term here |
|---|---|---|
| Daṇḍin, *Kāvyādarśa* 1.80 | *ojaḥ samāsabhūyastvam etad gadyasya jīvitam*: ojas is abundance of compounds, the life of prose | word length L |
| The treatise, 4.69 | "విలసితసమాసభరితోజ్జ్వలబంధం బోజము": a bright texture filled with compounds | word length L |
| Mammaṭa, *Kāvyaprakāśa* 8.75 | the harsh letters, and *vṛttidairghyam*: long compounds | word length L |
| Vāmana, *Kāvyālaṅkārasūtra* 3.1.5 | *gāḍhabandhatvam ojaḥ*: ojas is a tight texture | conjunct rate J |
| The 1945 commentary on 4.69 | tightness comes from conjuncts, doubled consonants and compounds; "compounds alone are not ojas" | conjunct rate J |

The commentator keeps the two apart with examples. The treatise's own example
(4.70) "has an abundance of compounds but no tightness of texture"; a verse of
Tikkana's has the tightness. Both terms are therefore reported, and the index
is their mean.

## 2. Sources, and what each contributes

| Source | What is taken from it |
|---|---|
| Rāmarājabhūṣaṇuḍu, *Kāvyālaṅkārasaṅgrahamu*, 4.60, 4.69–70 (1920 edition); the 1945 commentary | Ojas as a texture full of compounds, and its example. Its opposite: the treatise's mādhurya, words standing apart (4.60, example 4.61). The commentator's distinction between compounds and tightness. |
| Daṇḍin, *Kāvyādarśa* 1.80–84 (GRETIL) | Ojas as abundance of compounds. Two examples: the heavy ojas of the easterners (1.82) and the "unconfused" ojas others want (1.84). The claim that ojas is the life of prose (§7.4). |
| Vāmana, *Kāvyālaṅkārasūtra* 3.1.5, 3.1.21 (GRETIL) | Ojas as tightness, with his own pair of lines, one tight and one not (§7.1). Mādhurya as words apart, "meant to exclude long compounds". |
| Mammaṭa, *Kāvyaprakāśa* 8.69–70, 8.74–75 (GRETIL) | Long compounds for ojas, none or middling for mādhurya. Ojas belongs to the heroic rasa, and more of it to the repulsive and the furious (§7.4). |
| Sinha, Sharma, Dasgupta & Basu (2012), *New Readability Measures for Bangla and Hindi Texts*, COLING | **The formula's form.** Their models predict how hard readers find a text from average word length and the number of conjuncts (jukta-akshars), e.g. 0.211 + 1.37·AWL + 0.005·JUK for Hindi. The conjunct count was the feature most correlated with judged hardness in both languages (Spearman 0.45 and 0.87). |
| Flesch (1948), *A new readability yardstick*, J. Applied Psychology 32 | The older form of the same idea: a weighted sum with syllables per word as the word-length term. |

## 3. Algorithm

**Words.** A word is what stands between spaces in the normalised line. Its
length is its number of aksharas.

**Aksharas.** As for metric 3: each akshara is parsed into onset, vowel and
coda. An akshara "begins with a conjunct" when its onset has two or more
consonants, doubled ones included (క్క, స్త, ప్ర, త్స్న).

**The two terms**, for a line or a poem, both percentages of its aksharas:

```
W = 100 · (aksharas in words − words) / aksharas in words = 100 · (1 − 1/L)    bound share
J = 100 · aksharas beginning with a conjunct / aksharas                        conjunct rate
```

L is the mean word length in aksharas. W is the share of aksharas that continue
a word rather than start one: 0 when every akshara is a word of its own, near
100 for one long compound. J is the share that open with a cluster.

**The index.**

```
O = (W + J) / 2
```

O is a percentage of the poem's own aksharas. **No constant in it comes from a
corpus**, so a poem's O does not depend on which poets the reference holds, and
a new poet is scored on the same scale as every other (version 1.0 standardised
L and J on the reference corpus; §10).

**Why this combination.** Sinha et al. fit a weighted sum of word length and
conjunct count to readers' judgements of Hindi and Bangla prose. Their weights
belong to those languages and to their units (conjuncts per 50 sentences), so
they cannot be carried over. Here both terms are shares of the same aksharas,
so they need no coefficient, and they are weighted equally. They also spread
about equally across poems (standard deviations 4.7 and 5.1 points over the
12,704 reference poems) and are unrelated (Spearman 0.01), so neither dominates
the index, and neither stands in for the other.

**Reported beside O, not in it:** the aspirate rate A, aspirated consonants per
100 aksharas. §7.3 gives the reason.

**Baseline.** The reference is all verse of the four dataset files (12,704
poems, 239,494 words). O needs none of it. The baseline stores the rubric's cut
points, which come from the treatise's examples (§4), and the reference
distributions, from which the percentile reported beside O is read.

## 4. Rubric

On O, anchored to the treatise's own two examples rather than to a corpus. The
light cut is the O of its example of words standing apart, the opposite of ojas
(mādhurya, 4.60, example 4.61); the dense cut is the O of its example of ojas
(4.69, example 4.70). The interval between them is split into three. Lines and
poems share the cuts.

| level | label | O | share of the reference poems |
|---:|---|---|---:|
| 0 | light | below 39.29, the treatise's words-apart example (4.61) | 17.0% |
| 1 | leaning light | 39.29 to 42.02 | 26.9% |
| 2 | moderate | 42.02 to 44.76 | 30.9% |
| 3 | leaning dense | 44.76 to 47.50 | 16.7% |
| 4 | dense | at least 47.50, the treatise's ojas example (4.70) | 8.5% |

The shares are those of the 12,704 reference poems
(`outputs/samples_analysis.json`, `real.all`). They are a description of these
corpora, not part of the rubric: a new poet who writes in long compounds can be
"dense" in every poem.

**The rubric describes; it does not grade.** Mammaṭa places ojas in the heroic
and furious rasas, not everywhere.

## 5. Output

`python3 ojas.py score --text "…"` prints one JSON object per poem:

| field | meaning |
|---|---|
| `score`, `label` | rubric level 0–4 of the poem, and its label |
| `ojas`, `percentile` | O, and its place among the reference poems (the only field relative to the reference) |
| `bound_share`, `conjunct_rate` | W and J |
| `word_length` | L, the mean word length behind W |
| `aspirate_rate` | A (not in O) |
| `longest_words` | the three longest words, with their length in aksharas |
| `lines[]` | the same per line |

## 6. Limitation to know first: printed words stand in for compounds

Word length measures compound length only as far as an edition prints a
compound as one word. The 1920 edition of the treatise does
(మందారబిసకుందకుందాదినిధిబృంద); the Bhāgavatamu edition in the dataset often
prints the members apart (భక్త పాలన కళాసంరంభకున్). The same verse would score
lower in the second style. So:
- comparisons within one edition or one source are sound;
- comparisons across editions carry this bias;
- true compound length needs the sandhi and compound splitter of metric 6, and L should be replaced by it when that exists.

§7.2 measures how far printed words do track the units of a gloss.

## 7. Validation

All numbers come from `outputs/ojas_validation.json`.

### 7.1 The contrasts the classical texts draw

Each row is a pair that one text sets against the other as more and less ojas.
Both verses of a pair come from the same source, so they are printed alike.

| more ojas | less ojas | who says so | O, more | O, less | in order |
|---|---|---|---:|---:|---|
| Treatise 4.70, ojas | Treatise 4.61, mādhurya (words apart) | the treatise | 47.5 | 39.3 | yes |
| KP 8.75, ojas | KP 8.74, mādhurya | Mammaṭa | 57.1 | 44.3 | yes |
| KP 8.77, Bhīma's speech | KP 8.74 | Mammaṭa | 56.5 | 44.3 | yes |
| KP 8.77, Kumbhakarṇa's head | KP 8.74 | Mammaṭa | 56.0 | 44.3 | yes |
| Vāmana 3.1.5, the tight line | Vāmana 3.1.5, "not thus" | Vāmana | 50.0 | 46.7 | yes |
| Kāvyādarśa 1.82, the easterners' ojas | Kāvyādarśa 1.84, the unconfused ojas | Daṇḍin | 64.1 | 46.9 | yes |
| Kāvyādarśa 1.84 | Kāvyādarśa 1.70, "not forceful" | Daṇḍin | 46.9 | 43.8 | yes |
| Tikkana's verse (tight) | Treatise 4.70 (compounds, not tight) | the 1945 commentary, on J | 26.3 | 3.0 | yes |

All 8 are in the texts' order. The last row is on the conjunct rate alone, as
the commentator's remark is. It shows why the index needs both terms: 4.70 has
the longest words of any example (L = 12.5, W = 92) and almost no conjuncts (J = 3.0).

### 7.2 The gloss check: do printed words track compound units?

The Bhāgavatamu edition glosses each verse word by word, with compounds and
sandhi taken apart. For 5,266 verses:

| | |
|---|---:|
| aksharas per printed word (L) | 3.93 |
| gloss units per printed word | 1.41 |
| aksharas per gloss unit | 2.97 |
| Spearman, L against gloss units per printed word (poems) | 0.71 |

A printed word holds 1.4 gloss units on average, and poems with longer printed
words do hold more units per word. L tracks fused units, imperfectly.

### 7.3 Aspirates are left out, on Vāmana's evidence

The proposal lists aspirated stops under ojas. With the aspirate rate as a
third share, 6 of the 7 index contrasts stay in order and Vāmana's
own pair reverses. His tight line is *vilulitamakarandā mañjarīr nartayanti*
(conjuncts nd, ñj, rn, nt; no aspirate). The line he gives as not tight is
*vilulitamadhudhārā mañjarīr lolayanti* (two aspirates, fewer conjuncts). For
Vāmana the aspirates are on the slack side. The aspirate rate is reported, and
it is not in O.

| variant | Spearman with headline (12,704 poems) | index contrasts in order |
|---|---:|---:|
| **headline** (W and J) | 1.000 | 7/7 |
| W, J and aspirates | 0.932 | 6/7 |
| bound share W alone | 0.661 | — |
| conjunct rate J alone | 0.724 | — |
| version 1.0 (L and J standardised on the reference) | 0.994 | 7/7 |

The mean word length and the share of words of six or more aksharas agree
closely (Spearman 0.74–0.85), so the choice of the mean matters little.

### 7.4 Known groups

**Meters (Bhāgavatamu).** The Sanskrit vṛttas are the densest, kandamu the
lightest:

| kandamu | āṭaveladi | champakamāla | utpalamāla | tēṭagīti | sīsamu | mattēbha | śārdūla |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 41.9 | 43.0 | 43.1 | 43.2 | 43.5 | 43.9 | 45.0 | 45.5 |

**Corpora.** Most of Kuchimanchi's corpus is his *Accha-Telugu Rāmāyaṇamu*, a
work in pure Telugu (1,353 poems of that source in the verse collection match
it by first line). It is the lightest by a wide margin:

| corpus | L | W | J | A | mean O | light | dense |
|---|---:|---:|---:|---:|---:|---:|---:|
| bhagavatam | 3.99 | 74.2 | 12.0 | 4.6 | 43.1 | 11.9% | 9.1% |
| chandassu | 3.80 | 73.0 | 13.3 | 4.0 | 43.1 | 12.2% | 11.4% |
| vemana | 3.73 | 72.8 | 10.6 | 3.3 | 41.7 | 19.8% | 2.6% |
| kuchimanchi_timmakavi | 3.32 | 68.9 | 11.3 | 1.4 | 40.1 | 45.1% | 5.4% |

**Two classical claims the data do not confirm.**
- *Ojas is the life of prose* (Daṇḍin 1.80). Pothana's prose passages (1,871 of 20 aksharas or more) are barely denser than his verse: chance that a prose passage outscores a verse 0.54. The edition's spacing of compounds (§6) may hide a difference.
- *Ojas belongs to the heroic and furious rasas* (KP 8.69–70). Fierce poems outscore tender ones with chance 0.50 in bhagavatam, 0.59 in chandassu and 0.38 in kuchimanchi. The conjunct rate alone does a little better (0.53, 0.65, 0.47); word length runs the other way (0.46, 0.46, 0.39). The groups are the keyword groups of metric 3.

### 7.5 Relations to the other metrics (Spearman, poems)

| corpus | O with mādhurya M | J with M | L with M | O with anuprāsa z | O with poem length |
|---|---:|---:|---:|---:|---:|
| bhagavatam | −0.33 | −0.42 | −0.01 | −0.04 | 0.18 |
| vemana | −0.24 | −0.30 | 0.01 | −0.06 | −0.11 |
| kuchimanchi_timmakavi | −0.34 | −0.30 | −0.16 | 0.10 | 0.37 |
| chandassu | −0.42 | −0.46 | −0.10 | −0.05 | 0.05 |

Ojas and mādhurya pull against each other, as Mammaṭa's scheme has it, through
the conjunct term. Word length is unrelated to mādhurya: it is what this metric
adds.

### 7.6 Order does not matter

O is computed from counts, so shuffling a poem's words leaves it unchanged. The
proposal's degradation protocol cannot admit or reject it.

### 7.7 Lines for reading

| densest lines (Bhāgavatamu) | O | lightest lines | O |
|---|---:|---|---:|
| క్షేత్రజ్ఞుతోఁ గూర్చి, క్షేత్రజ్ఞునాత్మలో- | 70.8 | ఓ ఱేఁడ! నీకు మది వే (Kuchimanchi) | 18.8 |
| ద్ధనయోన్నిద్రఁ బ్రపూర్ణసద్గుణసముద్రన్భద్ర నక్షుద్ర నా | 67.5 | తే పో ధారుణిఁ గామా | 21.4 |
| ప్రాకామ్యస్తవ మొప్పఁ జెప్పె శుభకృత్ప్రవ్యక్తవర్షంబునన్ (Chandassu) | 63.2 | నీ వాడిన నే నాడుదు (Vemana) | 25.0 |

### 7.8 A new poet does not move the scale

Each corpus in turn plays a new poet: the reference is rebuilt from the other
three, and its poems are scored again (`reference_dependence` in the output).

| corpus as the new poet | its share of the reference | version 1.0: poems relabelled | version 1.0: rank order kept (Spearman) | version 2.0: poems relabelled |
|---|---:|---:|---:|---:|
| bhagavatam | 58.0% | 23.9% | 0.997 | 0 |
| chandassu | 19.9% | 4.1% | 0.9997 | 0 |
| kuchimanchi_timmakavi | 12.9% | 13.0% | 0.9999 | 0 |
| vemana | 9.2% | 2.6% | 0.9998 | 0 |

Under version 1.0 the order of a poet's poems barely moved, but the labels did,
most for the poet that dominates the reference: without the Bhāgavatamu, the
mean word length falls from 3.84 to 3.64 and its poems look denser. Version 2.0
has no corpus constant, so its scores and labels cannot move.

## 8. Decisions and limitations

1. **Printed words for compounds** (§6). This is the main limitation.
2. **Equal weights.** The two shares count equally. No source gives a weight for Telugu verse; they spread about equally (§3), so neither dominates.
3. **Every conjunct counts**, doubled consonants included. Metric 3 sorts conjuncts into soft and harsh; here only their number matters.
4. **Aspirates are out of the index** (§7.3), against the proposal's wording.
5. **No sequence term.** Two long words in a row count as two long words.
6. **The scale is fixed, the percentile is not.** O and its label use no corpus statistic (§7.8). The percentile reported beside them is relative to the four dataset files, 58% of whose poems are Pothana's.
7. **Not yet validated against human ratings.** The two rasa-linked predictions of §7.4 did not hold on keyword groups.

## 9. References

See [`../references.bib`](../references.bib) (keys in brackets).

- Daṇḍin. *Kāvyādarśa*, pariccheda 1. GRETIL e-text. [`dandin_kavyadarsa`]
- Flesch, R. (1948). A new readability yardstick. *Journal of Applied Psychology* 32(3), 221–233. [`flesch1948readability`]
- Mammaṭa. *Kāvyaprakāśa*, ullāsa 8. GRETIL e-text. [`mammata_kavyaprakasa`]
- Rāmarājabhūṣaṇuḍu (Bhaṭṭumūrti). *Kāvyālaṅkārasaṅgrahamu* (*Narasabhūpālīyamu*), 1920 and 1945 editions, Telugu Wikisource. [`ramarajabhushana_kas1920`, `ramarajabhushana_kas1945`]
- Sinha, M., Sharma, S., Dasgupta, T. & Basu, A. (2012). New readability measures for Bangla and Hindi texts. *Proceedings of COLING 2012: Posters*, 1141–1150. ACL Anthology C12-2111. [`sinha2012readability`]
- Vāmana. *Kāvyālaṅkārasūtra* with the author's gloss. GRETIL e-text. [`vamana_kavyalankarasutra`]

## 10. Versions

- **2.0** (1 October 2026): O = (W + J) / 2, a fixed formula of the poem alone, with the rubric anchored to
  the treatise's examples 4.61 and 4.70. The scores no longer depend on the reference corpus (§7.8).
- **1.0** (30 September 2026): O = ½ · [(L − 3.844)/0.730 + (J − 12.04)/5.12], with μ and σ the mean and
  standard deviation over the 12,704 reference poems, and cuts at the reference's 10th, 30th, 70th and
  90th percentiles. It ranks poems almost as 2.0 does (Spearman 0.994) and puts the same 8 contrasts in
  order, but its scale and labels moved when the reference changed.

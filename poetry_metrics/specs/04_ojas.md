# Metric 4 — *ojas* (word-density index)

| | |
|---|---|
| Script | [`ojas.py`](../ojas.py) (version 1.0) |
| Shared code | [`common/phonology.py`](../common/phonology.py), [`common/corpus.py`](../common/corpus.py) |
| Baseline | [`baselines/ojas_baseline.json`](../baselines/ojas_baseline.json), built by `python3 ojas.py build-baseline` |
| Validation | [`outputs/ojas_validation.json`](../outputs/ojas_validation.json), built by `python3 ojas.py validate` ([`validation_ojas.py`](../validation_ojas.py)) |
| Exemplars | [`fixtures/classical_exemplars.json`](../fixtures/classical_exemplars.json): 8 contrasts the classical texts draw |
| Tests | [`tests/test_ojas.py`](../tests/test_ojas.py): 15 tests |
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

**The two terms**, for a line or a poem:

```
L = aksharas in words / words                          word length
J = 100 · aksharas beginning with a conjunct / aksharas   conjunct rate
```

**The index.**

```
O = ½ · [ (L − μ_L) / σ_L  +  (J − μ_J) / σ_J ]
```

μ and σ are the mean and standard deviation of L and J over the 12,704 poems
of the reference corpus: μ_L = 3.844, σ_L = 0.730, μ_J = 12.04, σ_J = 5.12.
They are frozen in the baseline. O = 0 is a poem of average word length and
average conjunct rate. O = +1 is one standard deviation denser on both, or two
on one.

**Why this combination.** Sinha et al. fit a weighted sum of word length and
conjunct count to readers' judgements of Hindi and Bangla prose. Their weights
belong to those languages and to their units (conjuncts per 50 sentences), so
they cannot be carried over. Here each term is put on the scale of Telugu verse
by standardising it, and the two are weighted equally. In the reference corpus
the two terms are unrelated (Spearman −0.09 to 0.06), so neither stands in for
the other.

**Reported beside O, not in it:** the aspirate rate A, aspirated consonants per
100 aksharas. §7.3 gives the reason.

**Baseline.** The reference is all verse of the four dataset files (12,704
poems, 239,494 words). The baseline stores μ, σ, the quantiles and the cut
points.

## 4. Rubric

On O, against the reference corpus (its 10th, 30th, 70th and 90th percentiles).

| level | label | share of reference | line O | poem O |
|---:|---|---|---|---|
| 0 | light | bottom 10% | < −1.29 | < −0.87 |
| 1 | leaning light | 10–30% | −1.29 to −0.55 | −0.87 to −0.39 |
| 2 | moderate | 30–70% | −0.55 to 0.66 | −0.39 to 0.30 |
| 3 | leaning dense | 70–90% | 0.66 to 1.73 | 0.30 to 0.92 |
| 4 | dense | top 10% | ≥ 1.73 | ≥ 0.92 |

**The rubric describes; it does not grade.** Mammaṭa places ojas in the heroic
and furious rasas, not everywhere.

## 5. Output

`python3 ojas.py score --text "…"` prints one JSON object per poem:

| field | meaning |
|---|---|
| `score`, `label` | rubric level 0–4 of the poem, and its label |
| `ojas`, `percentile` | O, and its place among reference poems |
| `word_length`, `conjunct_rate` | L and J |
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
| Treatise 4.70, ojas | Treatise 4.61, mādhurya (words apart) | the treatise | 5.05 | −0.59 | yes |
| KP 8.75, ojas | KP 8.74, mādhurya | Mammaṭa | 4.50 | 0.43 | yes |
| KP 8.77, Bhīma's speech | KP 8.74 | Mammaṭa | 5.59 | 0.43 | yes |
| KP 8.77, Kumbhakarṇa's head | KP 8.74 | Mammaṭa | 4.79 | 0.43 | yes |
| Vāmana 3.1.5, the tight line | Vāmana 3.1.5, "not thus" | Vāmana | 2.63 | 1.98 | yes |
| Kāvyādarśa 1.82, the easterners' ojas | Kāvyādarśa 1.84, the unconfused ojas | Daṇḍin | 7.16 | 0.85 | yes |
| Kāvyādarśa 1.84 | Kāvyādarśa 1.70, "not forceful" | Daṇḍin | 0.85 | 0.15 | yes |
| Tikkana's verse (tight) | Treatise 4.70 (compounds, not tight) | the 1945 commentary, on J | 26.3 | 3.0 | yes |

All 8 are in the texts' order. The last row is on the conjunct rate alone, as
the commentator's remark is. It shows why the index needs both terms: 4.70 has
the longest words of any example (L = 12.5) and almost no conjuncts (J = 3.0).

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
third standardised term, 6 of the 7 index contrasts stay in order and Vāmana's
own pair reverses. His tight line is *vilulitamakarandā mañjarīr nartayanti*
(conjuncts nd, ñj, rn, nt; no aspirate). The line he gives as not tight is
*vilulitamadhudhārā mañjarīr lolayanti* (two aspirates, fewer conjuncts). For
Vāmana the aspirates are on the slack side. The aspirate rate is reported, and
it is not in O.

| variant | Spearman with headline (12,704 poems) | index contrasts in order |
|---|---:|---:|
| **headline** (L and J) | 1.000 | 7/7 |
| L, J and aspirates | 0.868 | 6/7 |
| word length alone | 0.658 | — |
| conjunct rate alone | 0.719 | — |

The mean word length and the share of words of six or more aksharas agree
closely (Spearman 0.74–0.85), so the choice of the mean matters little.

### 7.4 Known groups

**Meters (Bhāgavatamu).** The Sanskrit vṛttas are the densest, kandamu the
lightest:

| kandamu | champakamāla | utpalamāla | āṭaveladi | tēṭagīti | sīsamu | mattēbha | śārdūla |
|---:|---:|---:|---:|---:|---:|---:|---:|
| −0.15 | 0.08 | 0.09 | 0.10 | 0.19 | 0.28 | 0.47 | 0.57 |

**Corpora.** Most of Kuchimanchi's corpus is his *Accha-Telugu Rāmāyaṇamu*, a
work in pure Telugu (1,353 poems of that source in the verse collection match
it by first line). It is the lightest by a wide margin:

| corpus | L | J | A | mean O | light | dense |
|---|---:|---:|---:|---:|---:|---:|
| bhagavatam | 3.99 | 12.0 | 4.6 | +0.10 | 6.7% | 11.2% |
| chandassu | 3.80 | 13.3 | 4.0 | +0.09 | 7.1% | 12.2% |
| vemana | 3.73 | 10.6 | 3.3 | −0.22 | 10.7% | 2.9% |
| kuchimanchi_timmakavi | 3.32 | 11.3 | 1.4 | −0.43 | 28.9% | 6.0% |

**Two classical claims the data do not confirm.**
- *Ojas is the life of prose* (Daṇḍin 1.80). Pothana's prose passages (1,871 of 20 aksharas or more) are no denser than his verse: chance that a prose passage outscores a verse 0.52. The edition's spacing of compounds (§6) may hide a difference.
- *Ojas belongs to the heroic and furious rasas* (KP 8.69–70). Fierce poems outscore tender ones with chance 0.49 in bhagavatam, 0.59 in chandassu and 0.38 in kuchimanchi. The conjunct rate alone does a little better (0.53, 0.65, 0.47); word length runs the other way (0.46, 0.46, 0.39). The groups are the keyword groups of metric 3.

### 7.5 Relations to the other metrics (Spearman, poems)

| corpus | O with mādhurya M | J with M | L with M | O with anuprāsa z | O with poem length |
|---|---:|---:|---:|---:|---:|
| bhagavatam | −0.32 | −0.42 | −0.01 | −0.04 | 0.18 |
| vemana | −0.24 | −0.30 | 0.01 | −0.06 | −0.13 |
| kuchimanchi_timmakavi | −0.36 | −0.30 | −0.16 | 0.09 | 0.35 |
| chandassu | −0.41 | −0.46 | −0.10 | −0.05 | 0.05 |

Ojas and mādhurya pull against each other, as Mammaṭa's scheme has it, through
the conjunct term. Word length is unrelated to mādhurya: it is what this metric
adds.

### 7.6 Order does not matter

O is computed from counts, so shuffling a poem's words leaves it unchanged. The
proposal's degradation protocol cannot admit or reject it.

### 7.7 Lines for reading

| densest lines | O | lightest lines | O |
|---|---:|---|---:|
| క్షేత్రజ్ఞుతోఁ గూర్చి, క్షేత్రజ్ఞునాత్మలో- | 5.44 | ఓ ఱేఁడ! నీకు మది వే | −2.71 |
| న్నుతులధ్యాత్మ విదుల్మహాభుజులు మాన్యుల్ధర్మమార్గుల్సము | 5.15 | తే పో ధారుణిఁ గామా | −2.61 |
| అణిమాద్యష్టగుణప్రసిద్ధులు త్రిలోకారాధ్యు లుద్యద్వచో- | 4.66 | జాలిఁ బడ నేల? నా శర | −2.58 |
| తనగేహభ్రమఁగిన్నినాళ్ళు ఘనవృద్ధప్రాప్తిఁ గొన్నేళ్ళుఁబా | 4.66 | నీ వాడిన నే నాడుదు | −2.44 |

## 8. Decisions and limitations

1. **Printed words for compounds** (§6). This is the main limitation.
2. **Equal weights.** The two terms count equally after standardising. No source gives a weight for Telugu verse.
3. **Every conjunct counts**, doubled consonants included. Metric 3 sorts conjuncts into soft and harsh; here only their number matters.
4. **Aspirates are out of the index** (§7.3), against the proposal's wording.
5. **No sequence term.** Two long words in a row count as two long words.
6. **The reference sets the scale.** μ and σ come from the four dataset files, 58% of whose poems are Pothana's.
7. **Not yet validated against human ratings.** The two rasa-linked predictions of §7.4 did not hold on keyword groups.

## 9. References

See [`../references.bib`](../references.bib) (keys in brackets).

- Daṇḍin. *Kāvyādarśa*, pariccheda 1. GRETIL e-text. [`dandin_kavyadarsa`]
- Flesch, R. (1948). A new readability yardstick. *Journal of Applied Psychology* 32(3), 221–233. [`flesch1948readability`]
- Mammaṭa. *Kāvyaprakāśa*, ullāsa 8. GRETIL e-text. [`mammata_kavyaprakasa`]
- Rāmarājabhūṣaṇuḍu (Bhaṭṭumūrti). *Kāvyālaṅkārasaṅgrahamu* (*Narasabhūpālīyamu*), 1920 and 1945 editions, Telugu Wikisource. [`ramarajabhushana_kas1920`, `ramarajabhushana_kas1945`]
- Sinha, M., Sharma, S., Dasgupta, T. & Basu, A. (2012). New readability measures for Bangla and Hindi texts. *Proceedings of COLING 2012: Posters*, 1141–1150. ACL Anthology C12-2111. [`sinha2012readability`]
- Vāmana. *Kāvyālaṅkārasūtra* with the author's gloss. GRETIL e-text. [`vamana_kavyalankarasutra`]

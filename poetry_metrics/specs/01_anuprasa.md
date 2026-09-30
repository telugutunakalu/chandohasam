# Metric 1 — *anuprāsa* (alliteration density), with *vṛttyanuprāsa*

| | |
|---|---|
| Script | [`anuprasa.py`](../anuprasa.py) (version 1.0) |
| Shared code | [`common/phonology.py`](../common/phonology.py), [`common/corpus.py`](../common/corpus.py) |
| Baseline | [`baselines/anuprasa_baseline.json`](../baselines/anuprasa_baseline.json), built by `python3 anuprasa.py build-baseline` |
| Validation | [`outputs/anuprasa_validation.json`](../outputs/anuprasa_validation.json), built by `python3 anuprasa.py validate` ([`validation_anuprasa.py`](../validation_anuprasa.py)) |
| Tests | [`tests/test_anuprasa.py`](../tests/test_anuprasa.py): 16 tests |
| Proposal | Section 6 and Appendix E.1 (Tier 1), `proposal/chandohasam_full_proposal_v3.md` |

## 1. What it measures

*Anuprāsa* is the repetition of consonants. The vowels between them may change
(Barbadikar & Kulkarni 2024, §2). The proposal asks for:

> Repetition of consonants beyond what chance predicts. Convert text to phonemes, group similar
> consonants into classes (k/kh/g/gh together, etc.), count each class per line, and score the
> deviation from expected counts as a z-score against corpus frequencies. The baseline matters:
> frequent consonants such as t/n/r repeat naturally, and raw counts reward that noise.
> (Appendix E.1)

The metric scores each line, then the poem, at two levels:

| level | a repeat is | classical name | role |
|---|---|---|---|
| `varga` | two consonants from one varga series: k/kh/g/gh, c/ch/j/jh, ṭ/ṭh/ḍ/ḍh, t/th/d/dh, p/ph/b/bh. Every other consonant stands alone (nasals, y r l v, ś ṣ s h, ḷ, ṟ), as do the anusvāra and the visarga | the proposal's "consonant-class recurrence" | **headline** |
| `varna` | the same consonant | *vṛttyanuprāsa*: "one or many consonants repeated in any order" (Viśvanātha, as given by Barbadikar & Kulkarni 2024, §4) | second component |

The other sound figures are out of scope here. *Chekānuprāsa*, *yamaka* and
*muktapadagrasta* are Tier 2 in the proposal (Appendix E.2). *Antyānuprāsa*
(end rhyme) sits closer to prāsa, which is metric 2.

## 2. Sources, and what each contributes

| Source | What is taken from it |
|---|---|
| Barbadikar & Kulkarni (2024), *Anuprāsa Identifier and Classifier*, ISCLS | The definition and the types of anuprāsa. Anuprāsa counts consonants only. Spaces are ignored. A homorganic nasal is normalised to the anusvāra. The place-of-articulation classes of *śrutyanuprāsa*, tested here as an ablation. |
| Skinner (1939), *The alliteration in Shakespeare's sonnets* | Alliteration is judged against a chance model, in which sounds occur independently at their overall frequencies. Skinner's own verdict for Shakespeare was that the repetition was at chance level. |
| Benner (2014), *The Sounds of the Psalter*, LLC 29(3) | Soundplay is measured against corpus-wide phoneme frequencies with a binomial model, so that "artistic soundplay" can be told apart from "chance and a limited phonemic inventory". The metric uses his per-sound binomial test to name the sounds that carry a line's repetition (`carriers`). The method is described in the ADHO 2013 abstract of the same study. |
| Simpson (1949), *Measurement of diversity*, Nature 163 | The statistic. The number of same-sound pairs over all pairs is Simpson's index of the line's consonants. The chance value of that index is Σp² over the corpus frequencies. |
| Blain (1987), *A mathematical model for alliteration*, Style 21(4); Belouadi & Eger (2023), ByGPT5, ACL, eq. 1 | The distance-weighted pair statistic (weight 1/distance), which the ByGPT5 paper uses to label alliteration. It was tested here as an ablation and rejected (§6.3). |
| Frisch, Pierrehumbert & Broe (2004), *Similarity avoidance and the OCP*, NLLT 22 | Languages avoid similar consonants in adjacent positions. The effect is measured as an observed/expected ratio, which is the `lift` used here. It explains why the distance-weighted statistic fails on Telugu (§6.4). |
| Leavitt (1976), *On the measurement of alliteration in poetry*, CHum 10(6) | An early precedent for weighting sound types by their frequency in the corpus when measuring alliteration. |

**The treatise's own definitions** (added 2026-09-30; text from Telugu
Wikisource, 1920 edition, āśvāsa 4, where the sound figures follow the guṇas):

| figure | the treatise | here |
|---|---|---|
| *vṛttyanuprāsa* (4.76) | "ఒక్కవర్ణంబు కడదాక నుద్ధరింపఁ": one letter carried through to the end | the `varna` level |
| *chekānuprāsa* (the 74th verse, printed as 75) | "ఎడ లేక రెండు రెం డక్షరంబు, లెనయు": letters pairing two by two with no gap | Tier 2 |
| *lāṭānuprāsa* (4.76) | a repeated word with a different purport | Tier 2 |
| *yamaka*, *muktapadagrasta* (4.79–82) | defined after these | Tier 2 |

The treatise's example of vṛttyanuprāsa (4.77, క్ష repeated through three
lines) scores `varna` z = 3.18 (97th percentile of reference poems) and poem
score 1.25 (99th percentile). Its lines are labelled weak, marked, marked,
none. The carrier test names ష in each of the first three lines (p from
3 × 10⁻⁶ to 8 × 10⁻⁵). **Open decision:** the rubric labels this textbook
example only "weak" to "marked", because the pair count dilutes one repeated
sound among the 30 consonants of a long line. A rubric on the strongest single
sound (the carrier test) would follow the treatise's wording, "one letter
carried through", more closely.

## 3. Algorithm

**Unit.** A line is a printed pāda. A sīsa pāda printed on one line with
` - ` between its halves is split into the two half-lines, the way meter_engine
reads it ([`common/corpus.py`](../common/corpus.py)).

**Consonant tokens** ([`common/phonology.py`](../common/phonology.py)):
1. Text is converted to NFC. Everything outside the Telugu block becomes a space. The arasunna ఁ, ZWNJ/ZWJ and digits are removed.
2. A nasal followed by a stop of its own varga becomes the anusvāra, so న్ద and ంద read the same (after Barbadikar & Kulkarni 2024, §5).
3. The line is split into aksharas with the project's splitter (`meter_engine/aksharanusarika.py`). Spaces are not counted.
4. Each consonant letter in an akshara is one token, and so are the anusvāra ం and the visarga ః. A geminate (క్క) is one token. Vowels carry no token.

**Statistic, per line.** Let n be the number of tokens and x_s the count of
sound s. Pairs of tokens inside one akshara (a conjunct) are not counted,
because their co-occurrence is phonotactics, not the poet's choice.

```
M = number of token pairs in different aksharas
A = number of those pairs that are the same sound            (A/M = Simpson's index of the line)
q = Σ_s p_s² ,  r = Σ_s p_s³                                (p = reference-corpus frequencies)
E = q·M
V = M·(q − q²) + K·(r − q²)       K = Σ_t d_t(d_t − 1), d_t = number of counted pairs token t is in
z = (A − E) / √V
lift = (A/M) / q
```

Suppose each consonant of the line were drawn independently at its corpus
frequency. Then E and V are the exact mean and variance of A. The unit test
`test_moments_are_exact_under_the_chance_model` checks both against 40,000
simulated draws. The `lift` is the observed/expected repeat rate.

**Poem.** The poem's `score` is the mean rubric level of its lines (§4), on a
0–3 scale. Its `z` pools the lines, since A, E and V add over lines. This z
measures the evidence that the poem as a whole repeats beyond chance, and it
grows with the number of lines. `lift` gives the size of the excess.

**Carriers.** For each over-represented sound with at least two tokens, the
script reports its count, the expected count n·p_s, and the binomial tail
P(X ≥ x_s) (Benner 2014). The three most surprising are listed, with the
aksharas they occur in.

**Baseline.** p is estimated from all verse lines of the four dataset files:
12,704 poems, 61,227 lines and 1,044,872 consonant tokens, with a 0.5
pseudo-count on every symbol. The baseline also stores 101 quantiles of the
reference line z, poem z and poem score. A result's `percentile` is its place
in that reference distribution. Scoring is deterministic given the baseline
file.

## 4. Rubric

Per line, on the `varga` z. The cut points are the one-sided 5%, 1% and 0.1%
points of the standard normal, so no corpus data was used to set them.

| level | label | line z | meaning |
|---:|---|---|---|
| 0 | none | < 1.645 | no more repetition than the chance model allows |
| 1 | weak | 1.645 – 2.326 | repetition beyond chance, in the top 5% under the model |
| 2 | marked | 2.326 – 3.090 | clear anuprāsa, in the top 1% |
| 3 | strong | ≥ 3.090 | dense anuprāsa, in the top 0.1%, e.g. కరికిఁ గరాగ్రస్థగిరికిఘనతరకిరికిన్ (`bhagavatam:6-33-క.`, z = 8.61) |

**Poem score** = mean line level, from 0 to 3. The poem label rounds the score
to the nearest level.

**Base rates in real verse** (share of lines at or above each level, `varga`):

| corpus | weak | marked | strong |
|---|---:|---:|---:|
| bhagavatam | 8.27% | 3.77% | 1.62% |
| vemana | 9.29% | 4.68% | 2.11% |
| kuchimanchi_timmakavi | 11.87% | 6.33% | 3.18% |
| chandassu | 9.78% | 4.64% | 1.89% |

Most lines of real verse score 0. In the reference corpus the median poem
scores 0, the 90th percentile 0.5, the 95th 0.75 and the 99th 1.25.

## 5. Output

`python3 anuprasa.py score --text "…"` prints one JSON object per poem:

| field | meaning |
|---|---|
| `score`, `label`, `z` | headline (`varga`): poem score 0–3, its label, pooled z |
| `varga`, `varna` | per level: `score`, `label`, `z`, `lift`, `z_percentile`, `score_percentile`, `lines_with_anuprasa` |
| `lines[]` | per line and level: `z`, `lift`, `level`, `label`, `percentile`, `repeats` (A), `pairs` (M), `expected_repeats` (E), `carriers[]` |

## 6. Validation

All numbers come from `outputs/anuprasa_validation.json` (seed 42).

### 6.1 Degradation controls

The proposal (Appendix E) admits a metric only if it declines when the verse
is degraded. Two controls keep the poem's words or its line lengths and take
away the poet's choices:
- `word_shuffle` permutes the poem's words across its lines.
- `word_salad` rebuilds each line from random words of the same corpus.

Median poem z (`varga`), and the share of poems whose real z beats their own control's:

| corpus | real | word_shuffle | word_salad | real > shuffle | real > salad |
|---|---:|---:|---:|---:|---:|
| bhagavatam | 0.177 | 0.064 | −0.266 | 55.0% | 62.5% |
| vemana | 0.750 | 0.011 | −0.242 | 77.1% | 78.4% |
| kuchimanchi_timmakavi | 0.673 | 0.373 | −0.004 | 59.4% | 69.2% |
| chandassu | 0.413 | 0.185 | −0.257 | 58.4% | 66.8% |

In all four corpora the score falls in the order real > word_shuffle >
word_salad. Word salad removes most of the effect: in bhagavatam, lines at or
above "weak" drop from 8.27% to 5.31%, and at or above "strong" from 1.62% to
0.83%.

A third control, `consonant_shuffle`, permutes the poem's consonants over its
own consonant slots. It does **not** lower the score: real beats it in only
44–65% of poems. The shuffle also undoes something the language does. Telugu
avoids similar consonants in adjacent syllables (§6.4), so shuffling creates
more adjacent repeats than real text has. This control is reported but is not
used to admit the metric.

### 6.2 Known groups: the pilot grid

The 108-poem pilot grid (`metrics/initial_evals/Outputs/chandas_dataset.json`)
asked Gemini for one alaṅkāra per poem, 12 poems each. Two groups are compared:
- sound figures (*śabdālaṅkāra*): vṛttyanuprāsa, chekānuprāsa, antyānuprāsa, yamaka and muktapadagrasta, 60 poems;
- meaning figures (*arthālaṅkāra*): upamā, rūpaka, śleṣa and atiśayokti, 48 poems.

The labels are weak. They record what the model was asked for, not what an
expert found.

| statistic | AUC, sound vs meaning figures |
|---|---:|
| `varga` (headline) | 0.776 |
| `varna` | 0.808 |
| ablation: sthāna classes | 0.709 |
| ablation: Blain distance weighting | 0.518 |

Median poem z (`varga`) is 2.82–3.19 for the five sound figures and 1.90–2.18
for the four meaning figures.

### 6.3 Ablations: why whole-line Simpson, and why the varga series

Share of poems whose real z beats word salad:

| variant | bhagavatam | vemana | kuchimanchi | chandassu |
|---|---:|---:|---:|---:|
| `varga` (headline) | 62.5% | 78.4% | 69.2% | 66.8% |
| `varna` | 63.3% | 76.6% | 69.8% | 67.3% |
| sthāna classes (śrutyanuprāsa) | 54.7% | 65.2% | 58.9% | 55.2% |
| Blain 1/d weighting within 8 aksharas | 51.6% | 59.9% | 55.2% | 53.5% |

The place-of-articulation classes are too coarse: dantya alone is 33% of all
tokens, so a repeat within it is common by chance. Blain's distance weighting
puts the most weight on adjacent syllables, which is where Telugu avoids
repeats (§6.4). Under it, the median real poem falls below chance (−0.57 in
bhagavatam).

### 6.4 Observed/expected repeats by distance (all four corpora)

| akshara distance | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `varga` lift | 0.66 | 1.10 | 1.07 | 1.05 | 1.07 | 1.15 | 1.22 | 1.20 |
| `varna` lift | 0.67 | 1.12 | 1.09 | 1.06 | 1.10 | 1.18 | 1.26 | 1.24 |

Same-sound consonants in adjacent aksharas occur at two-thirds of the chance
rate. This is the similarity avoidance that Frisch et al. (2004) describe as
the OCP. At distances 2–8, repeats run above chance.

### 6.5 Top lines (for reading)

The highest `varga` z lines are textbook sound play:

| line | z |
|---|---:|
| మనుమనుమని మను మను మని | 10.11 |
| కరికిఁ గరాగ్రస్థగిరికిఘనతరకిరికిన్. | 8.61 |
| కళలు గలుగుఁ గాక; కమల తోడగుగాక; | 8.59 |
| ధాతవు, భారతశ్రుతివిధాతవు, వేదపదార్థజాతవి | 8.18 |
| విశ్వాత్ముని విశ్వవేద్యు విశ్వు నవిశ్వున్ | 7.25 |
| త్రేతా ద్వాపరసంధి నుద్ధతమదాంధీభూత ధాత్రీధవ | 10.31 |
| నిన్ను న్నమ్మినరీతినమ్మనొరులన్‌, నీకన్న నాకెన్నలే | 9.86 |

The last two come from chandassu, the others from bhagavatam. In Vemana, the
refrain విశ్వదాభిరామ వినర వేమ is itself a వ-anuprāsa. That is why 29% of
Vemana's lines reach "weak" at the `varna` level.

## 7. Limitations

- **Script, not sound.** Tokens are letters after the normalisations above. The dental allophones of చ/జ are not modelled, and ఱ and ర stay distinct.
- **The normal cut points are approximate.** The right tail of A is heavier than a normal's. Under word salad, 5.3% of bhagavatam lines reach "weak" (nominal 5%), 2.1% "marked" (nominal 1%) and 0.8% "strong" (nominal 0.1%). Read the labels as graded bands, not as exact p-values.
- **Poem z grows with length.** The poem `score` (mean line level) and `lift` do not, so use them to compare poems of different lengths.
- **Sequence repetition is not counted.** The statistic counts single sounds. A repeated cluster or syllable sequence, such as the -ంద- chime of మందార మకరంద, is chekānuprāsa or yamaka (Tier 2). The famous line మందార మకరందమాధుర్యమునఁ దేలు- scores `varga` z = 1.51 (89th percentile of reference lines, just under "weak"). Its మ carrier is 4 of 17 consonants against 1.19 expected (p = 0.027).
- **Not yet validated against human ratings.** The proposal's rubric (Appendix E.3) has no anuprāsa item. The known-groups check uses machine-generated poems and weak labels.

## 8. References

See [`../references.bib`](../references.bib) (keys in brackets).

- Barbadikar, A. V. & Kulkarni, A. (2024). Anuprāsa Identifier and Classifier: A computational tool to analyze Sanskrit figure of sound. *Proc. 7th International Sanskrit Computational Linguistics Symposium*, 102–112. ACL Anthology 2024.iscls-1.8. [`barbadikar2024anuprasa`]
- Belouadi, J. & Eger, S. (2023). ByGPT5: End-to-End Style-conditioned Poetry Generation with Token-free Language Models. *Proc. ACL 2023*. arXiv:2212.10474. [`belouadi2023bygpt5`]
- Benner, D. C. (2014). The Sounds of the Psalter: Computational Analysis of Soundplay. *Literary and Linguistic Computing* 29(3), 361–378. doi:10.1093/llc/fqu024. [`benner2014psalter`]
- Benner, D. C. (2013). The Sounds of the Psalter: Computational Analysis of Phonological Parallelism in Biblical Hebrew Poetry. *Digital Humanities 2013* (ADHO), abstract. [`benner2013psalter`]
- Blain, D. R. (1987). A mathematical model for alliteration. *Style* 21(4), 607–625. JSTOR 42945665. [`blain1987alliteration`]
- Frisch, S. A., Pierrehumbert, J. B. & Broe, M. B. (2004). Similarity avoidance and the OCP. *Natural Language & Linguistic Theory* 22(1), 179–228. doi:10.1023/B:NALA.0000005557.78535.3c. [`frisch2004ocp`]
- Leavitt, J. A. (1976). On the measurement of alliteration in poetry. *Computers and the Humanities* 10(6), 333–342. doi:10.1007/BF02402557. [`leavitt1976alliteration`]
- Rāmarājabhūṣaṇuḍu (Bhaṭṭumūrti). *Kāvyālaṅkārasaṅgrahamu* (*Narasabhūpālīyamu*), 1920 edition, āśvāsa 4. Telugu Wikisource. [`ramarajabhushana_kas1920`]
- Simpson, E. H. (1949). Measurement of diversity. *Nature* 163, 688. doi:10.1038/163688a0. [`simpson1949diversity`]
- Skinner, B. F. (1939). The alliteration in Shakespeare's sonnets: a study in literary behavior. *The Psychological Record* 3, 186–192. [`skinner1939alliteration`]

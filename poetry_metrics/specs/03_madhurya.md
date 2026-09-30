# Metric 3 — *mādhurya* (euphony index)

| | |
|---|---|
| Script | [`madhurya.py`](../madhurya.py) (version 1.1) |
| Shared code | [`common/phonology.py`](../common/phonology.py) (akshara structure, sonority scale), [`common/translit.py`](../common/translit.py) |
| Baseline | [`baselines/madhurya_baseline.json`](../baselines/madhurya_baseline.json), built by `python3 madhurya.py build-baseline` |
| Validation | [`outputs/madhurya_validation.json`](../outputs/madhurya_validation.json), built by `python3 madhurya.py validate` ([`validation_madhurya.py`](../validation_madhurya.py)) |
| Exemplars | [`fixtures/classical_exemplars.json`](../fixtures/classical_exemplars.json): 27 verses the classical texts quote, 16 of them soft, harsh or for information on this metric |
| Tests | [`tests/test_madhurya.py`](../tests/test_madhurya.py): 28 tests |
| Proposal | Section 6 and Appendix E.1 (Tier 1), `proposal/chandohasam_full_proposal_v3.md` |

Version 1.1 (2026-09-30) made the index sensitive to sequence: harsh aksharas
that stand together cost more than the same aksharas apart (§4). Version 1.0
was the inventory I alone.

## 1. What it measures

How soft or harsh a poem sounds. The proposal asks for:

> Proportion of soft sounds — nasals, y/r/l/v, unaspirated stops, few consonant clusters — as a
> weighted phoneme score averaged over the poem. (Appendix E.1)

The index has two steps. Every akshara falls in one of six classes by its
consonants, and each class has a weight from +1 (soft) to −1 (harsh); the mean
weight is the proposal's weighted proportion (§3). Then harsh aksharas in an
unbroken run are charged for the run they stand in, so a pile of harsh sounds
costs more than the same sounds scattered among soft ones (§4).

**What the treatise calls this quality.** The proposal names the index
*mādhurya*. That is the name in Mammaṭa's scheme of three guṇas (mādhurya,
ojas, prasāda). The *Kāvyālaṅkārasaṅgrahamu* keeps the older scheme of ten
guṇas, and there the names fall differently (āśvāsa 4, verse 60):

> సరసము లగువాక్యంబులు, వరుసను వేర్వేఱ మించువగ మాధుర్యం
> బరయఁగ బొట్లు పిఱుందుల, నరు దగునది సౌకుమార్య మది యె ట్లన్నన్.

| the treatise's guṇa | its definition | in this suite |
|---|---|---|
| *saukumārya* (4.60) | letters with a bindu before them. The 1945 commentary glosses "సున్నలు ముందుగల యక్షరములు" and adds Vāmana's wider "absence of harshness" | **this metric** |
| *mādhurya* (4.60) | charming words standing apart, which the commentary reads as no long compounds | needs compound splitting: belongs with metric 4 |
| *ojas* (4.69) | a texture full of compounds | metric 4 |
| *prasāda* (4.57) | well-known words ("ప్రసిద్ధపదంబుల") | metric 5 |
| *paruṣa* defect (4.21) | words harsh to the ear ("శ్రుతికటువు లైనపదములు") | the harsh pole of this metric, and metric 7 |

So this metric is Mammaṭa's mādhurya on its sound side, which is the treatise's
saukumārya. The translation of 4.60 above is mine; the commentary's gloss is
quoted in the table.

## 2. Sources, and what each contributes

| Source | What is taken from it |
|---|---|
| Rāmarājabhūṣaṇuḍu, *Kāvyālaṅkārasaṅgrahamu* (*Narasabhūpālīyamu*), āśvāsa 4. Text: Telugu Wikisource, 1920 edition. Commentary: 1945 edition, Sannidhānam Sūryanārāyaṇaśāstri | The soft pole: letters with a bindu before them (4.60) and its example (4.62). The harsh pole: the paruṣa word defect and its example (4.21). The commentary's statement that harsh words are a defect in the tender rasas (śṛṅgāra, karuṇa, śānta) and a merit in the fierce ones (raudra, vīra, bhayānaka), which sets the known-groups check (§7.2). |
| Mammaṭa, *Kāvyaprakāśa* 8.74–75, with his own gloss (GRETIL e-text) | The two sound lists, rule by rule (§3). 8.74, mādhurya: *mūrdhni vargāntyagāḥ sparśā aṭavargā raṇau laghū*. 8.75, ojas: *yoga ādyatṛtīyābhyām antyayo reṇa tulyayoḥ / ṭādiḥ śaṣau*. His example verses (§7.1). |
| Daṇḍin, *Kāvyādarśa* 1.43, 1.47, 1.69–72 (GRETIL e-text) | **The sequence.** A tender texture is one made *mostly* of non-harsh letters: *aniṣṭhurākṣaraprāyaṃ sukumāram* (1.69). Its opposite is named by how the sounds follow one another: *kṛcchrodyam*, "hard to utter" (1.72). Textures "arise from the arrangement of soft, harsh and mixed letters" (*varṇavinyāsa*, 1.47). An all-soft texture is slack, which he counts a fault (1.43, 1.69). His example verses (§7.1). |
| Page (1954), *Continuous inspection schemes*, Biometrika 41 | **The run load.** The cumulative sum: add up successive deviations, so that a sustained shift registers while isolated ones do not. Here the sum of harshness restarts at each non-harsh akshara. |
| Wald & Wolfowitz (1940), *On a test whether two samples are from the same population*, Ann. Math. Statist. 11 | The runs test: whether a two-valued sequence has fewer runs than chance, i.e. whether one kind clumps. Used in §7.4 to ask whether poets clump harsh aksharas. |
| Sandhan, Barbadikar et al. (2025), *Aesthetics of Sanskrit Poetry from the Perspective of Computational Linguistics*, CSDH-WSC | Mammaṭa's two lists stated for computation, and the claim that identifying the style from them "can be considered a deterministic process". They also note that "currently no computational system exists" for it. |
| Parker (2008), *Sound level protrusions as physical correlates of sonority*, J. Phonetics 36; Parker (2011), *Sonority*, Blackwell Companion to Phonology | The sonority scale: 17 ordered classes of sounds, from low vowels down to voiceless stops, tested against measured sound intensity (mean correlation .91). Its three major consonant classes grade the aksharas the classical lists do not mention. |
| Jacobs (2017), *Quantifying the Beauty of Words*, Front. Hum. Neurosci. 11:622; Jacobs (2018), English Poetry Corpus paper, Appendix A | The **sonority score**: the mean sonority rank of a word's letters, and for a poem the mean over words. Words rated beautiful score higher than words rated ugly (3.12 vs 2.9, p < .033). It is reported here as the second number (§4). |
| Fónagy (1961), *Communication in poetry*, Word 17 | The design of §7.2: count classes of sounds in tender and in aggressive poems. He found more /l, m, n/ in tender poems and more /k, t, r/ in aggressive ones. |
| Auracher et al. (2011), *P is for happiness, N is for sadness*, Discourse Processes 48 | A poem-level score from the relative frequency of two sound classes (plosives against nasals), the same form as the inventory I. |
| Whissell (1999), *Phonosymbolism and the emotional nature of sounds*, Percept. Mot. Skills 89 | Phonemes grouped by emotional character, one group named Softness, and texts profiled by which groups they favour. |
| Kraxenberger & Menninghaus (2016), *Mimological Reveries?*, Front. Psychol. 7:1779 | The caution. On 48 German poems they could not confirm that plosive or nasal frequency predicts the emotion readers perceive. Hence the index is reported as a description of texture, not as a measure of emotion or quality. |
| Birkhoff (1933), *Aesthetic Measure* | The oldest formula of this kind. For verse, order O = aa + 2r + 2m − 2ae − 2ce, where m counts musical sounds and ce an excess of consonants, and the measure is O over complexity. Cited as precedent only. |

## 3. Step 1: the sounds of Telugu, class by class

An akshara's class is decided by its onset, the consonants written before its
vowel. The harsh rules are tried first, then the soft ones, then the middle.

| class | weight | an akshara is in this class when | source |
|---|---:|---|---|
| **madhura** | +1 | **M1.** Its onset is one stop or class nasal, not ట ఠ డ ఢ, and the sound before it is the anusvāra or its own class nasal: ంక ంగ ంచ ంజ ంత ంద ంప ంబ. A doubled nasal counts: న్న మ్మ. | KP 8.74 *mūrdhni vargāntyagāḥ sparśā aṭavargāḥ*; gloss: all of k…m but ṭ ṭh ḍ ḍh, "joined on the head with the last of their own varga". Treatise 4.60 |
| | | **M2.** Its onset is ర or ణ alone, its vowel is short, and it has no coda. | KP 8.74 *raṇau laghū*; gloss: "separated by short vowels" |
| **sonorant** | +½ | Its onset is one nasal or one of య ర ల వ ళ ఱ, single or doubled. Or it has no consonant (a vowel akshara). | Sonority classes 7–17 (nasals, liquids, glides, vowels) |
| **voiced** | 0 | Its onset is one voiced stop or affricate: గ ఘ జ ఝ ద ధ బ భ. | Sonority classes 4–6 |
| **voiceless** | −½ | Its onset is one voiceless stop, affricate or fricative: క ఖ చ ఛ త థ ప ఫ స హ. | Sonority classes 1–3 |
| **conjunct** | −½ | Its onset is any other conjunct: క్త త్య స్త ద్వ జ్ఞ … | Proposal ("few consonant clusters"); the 1945 commentary on ojas: conjuncts make the texture dense |
| **paruṣa** | −1 | **P1.** Unaspirated + aspirated stop of one varga: క్ఖ గ్ఘ చ్ఛ ద్ధ బ్భ. | KP 8.75 *yoga ādyatṛtīyābhyām antyayoḥ* |
| | | **P2.** A conjunct with ర, above or below: ప్ర త్ర ర్క ర్థ. | KP 8.75 *reṇa* |
| | | **P3.** A doubled stop: క్క గ్గ చ్చ త్త ద్ద ప్ప. | KP 8.75 *tulyayoḥ* |
| | | **P4.** ట ఠ డ ఢ, alone or in a conjunct. ణ is not harsh. | KP 8.75 *ṭādiḥ*; gloss: "the ṭa-varga, that is, without ṇ" |
| | | **P5.** శ or ష, alone or in a conjunct (so క్ష). | KP 8.75 *śaṣau* |

Three points about the table:
- **The poles are the texts' lists and nothing else.** Every +1 and −1 comes from a rule of KP 8.74–75.
- **The middle is phonetics.** The classical lists are silent on a plain మ, గ or క. These are graded by the three major classes of the sonority scale: sonorants, voiced obstruents, voiceless obstruents. Telugu grammar has the same order in its own terms: క చ ట త ప are the *paruṣamulu* ("harsh") and గ జ డ ద బ the *saraḷamulu* ("gentle").
- **Where the traditions disagree.** Fónagy counts /r/ with the hard sounds; Mammaṭa counts a light ర with the sweet ones, and the sonority scale ranks it high. The index follows Mammaṭa.

In the reference corpus, of 897,463 aksharas:

| madhura | sonorant | voiced | voiceless | conjunct | paruṣa |
|---:|---:|---:|---:|---:|---:|
| 11.9% | 39.1% | 14.2% | 18.1% | 3.0% | 13.7% |

Per 100 aksharas the rules fire: M1 6.9, M2 4.9, P1 0.2, P2 3.5, P3 2.4, P4 6.3, P5 2.4.

## 4. Step 2: the sequence, and the formula

**Aksharas.** Text is normalised as for metric 1 (NFC, Telugu block only,
arasunna dropped, a class nasal before its own stop written as the anusvāra).
The project's splitter gives the aksharas. Each is parsed into onset, vowel and
coda (the anusvāra, the visarga, a final pollu consonant). A chunk with no
vowel is not scored.

**Harsh runs.** An akshara is harsh when its weight w is negative, and its
harshness is h = −w: ½ for the voiceless and conjunct classes, 1 for paruṣa. A
harsh run is a stretch of harsh aksharas with nothing else between them. Along
a run the harshness adds up into the run load R:

```
R_t = R_(t−1) + h_t     if akshara t is harsh
R_t = 0                 otherwise
```

**The index.** A harsh akshara is charged the load of its run so far, not only
its own weight. With N scored aksharas:

```
w*_t = w_t       if akshara t is not harsh
w*_t = −R_t      if it is

M = (1/N) · Σ_t w*_t  =  I − P

I = (1/N) · Σ_t w_t                       inventory: the plain weighted proportion, −1 ≤ I ≤ +1
P = (1/N) · Σ_{harsh t} R_(t−1)           pile-up: the load carried into each harsh akshara, P ≥ 0
```

What this gives:
- **A harsh akshara among soft ones costs its own weight.** P = 0 and M = I whenever no two harsh aksharas are adjacent.
- **Each further harsh akshara in a run costs more than the one before.** A run of three paruṣa aksharas is charged 1 + 2 + 3, not 3.
- **The same aksharas together never score above the same aksharas apart.** కమకమకమ has I = M = 0; కకకమమమ has the same I and M = −0.25.
- **Any non-harsh akshara ends the run:** a voiced stop, a sonorant, a vowel.
- **M has no lower bound.** A long unbroken run can take a line well below −1. Real lines reach −4.5 (§7.7).

**Through the poem.** Rule M1 and the runs look across spaces and line ends. A
line that ends in an anusvāra makes the next line's first stop madhura
(పొందికం / జెందె), and a run may continue from one line into the next. A run
is reported under the line it begins in.

**Poem.** The poem's M is the mean of w* over all its aksharas.

**Sonority score (second number).** Every segment (onset consonants, vowel,
coda) has a rank on Parker's scale, 17 for అ down to 1 for క:

| 17 | 16 | 15 | 12 | 10 | 9 | 8 | 7 | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| అ ఆ | ఎ ఏ ఒ ఓ ఐ ఔ | ఇ ఈ ఉ ఊ ఋ | య వ | ర | ల ళ | ఱ | ఙ ఞ ణ న మ ం | జ ఝ | గ ఘ డ ఢ ద ధ బ భ | శ ష స హ ః | చ ఛ | క ఖ ట ఠ త థ ప ఫ |

```
S = (1/n) · Σ_segments rank(segment)
```

This is Jacobs's sonority score on Parker's scale. It is blind to the classical
lists and to sequence, so it serves as an independent check (§7.3). It is not
part of M.

**Baseline.** The reference is all verse of the four dataset files: 12,704
poems, 61,227 lines. Its mean M is −0.060, with I = 0.071 and P = 0.132. The
baseline stores 101 quantiles of M, I, P and S, for lines and for poems, and
the rubric cut points. Scoring is deterministic given the baseline file.

## 5. Rubric

On M, against the reference corpus. The cut points are its 10th, 30th, 70th and
90th percentiles.

| level | label | share of reference | line M | poem M |
|---:|---|---|---|---|
| 0 | harsh (*paruṣa*) | bottom 10% | < −0.464 | < −0.283 |
| 1 | leaning harsh | 10–30% | −0.464 to −0.158 | −0.283 to −0.123 |
| 2 | balanced | 30–70% | −0.158 to 0.125 | −0.123 to 0.049 |
| 3 | leaning soft | 70–90% | 0.125 to 0.300 | 0.049 to 0.156 |
| 4 | soft (*sukumāra*) | top 10% | ≥ 0.300 | ≥ 0.156 |

**The rubric describes; it does not grade.** A higher level is softer, not
better. The treatise's commentary on 4.21 says harsh words are a defect in the
tender rasas and a merit in the fierce ones, and Daṇḍin counts an all-soft
texture slack (1.43). To judge a generated poem, compare its level with what
its subject calls for, or with the reference distribution.

## 6. Output

`python3 madhurya.py score --text "…"` prints one JSON object per poem:

| field | meaning |
|---|---|
| `score`, `label` | rubric level 0–4 of the poem, and its label |
| `madhurya`, `percentile` | M, and its place among reference poems |
| `inventory`, `pileup`, `pileup_percentile` | I and P; M = I − P |
| `sonority`, `sonority_percentile` | S, and its place among reference poems |
| `classes` | aksharas per class |
| `rules` | aksharas per rule M1–P5 |
| `harshest_run` | the harsh run with the highest load: its aksharas, length and load |
| `lines[]` | the same per line, plus `soft[]` and `harsh[]` (each marked akshara with its rule) and `harsh_runs[]` (every run of two or more aksharas that begins in the line) |

## 7. Validation

All numbers come from `outputs/madhurya_validation.json` (seed 42).

### 7.1 The classical texts' own examples

The treatise, the Kāvyaprakāśa and the Kāvyādarśa quote verses as examples of
a soft or a harsh texture. The index should place them as the texts do.
Sanskrit verses are written in Telugu script and scored like any other line.
Percentiles are against the Telugu reference poems (for a one-line example,
against reference lines).

| example | the text calls it | M | percentile | label | I | P |
|---|---|---:|---:|---|---:|---:|
| Treatise 4.62, saukumārya | soft | 0.394 | 99.7 | soft | 0.419 | 0.025 |
| KP 8.74, mādhurya | soft | 0.023 | 63.5 | balanced | 0.193 | 0.171 |
| Kāvyādarśa 1.70, sukumāra | soft | −0.031 | 50.0 | balanced | 0.000 | 0.031 |
| Treatise 4.21, paruṣa phrase | harsh | −1.250 | 1.0 | harsh | −0.536 | 0.714 |
| Kāvyādarśa 1.72, "hard to utter" | harsh | −1.500 | 0.9 | harsh | −0.393 | 1.107 |
| KP 8.75, ojas | harsh | −0.476 | 2.5 | harsh | −0.137 | 0.339 |
| KP 8.77, Bhīma's speech | harsh | −0.548 | 1.5 | harsh | −0.149 | 0.399 |
| KP 8.77, Kumbhakarṇa's head | harsh | −0.554 | 1.5 | harsh | −0.036 | 0.518 |
| 1945 commentary: Tikkana, dense texture | harsh | −0.250 | 13.0 | leaning harsh | 0.000 | 0.250 |
| 1945 commentary: Peddana, "not harsh" | soft | −0.088 | 37.1 | balanced | 0.063 | 0.150 |

- **M orders every pair correctly:** each soft example is above each harsh one, 15 of 15 pairs among the root texts' examples and 24 of 24 with the commentary's.
- **The sequence does real work.** Daṇḍin's tender verse (1.70) and the commentator's dense verse (Tikkana) have the same inventory, I = 0.000. The first has its few harsh letters scattered (P = 0.031); the second has them in runs such as సాస్తోకప్రతాపస్ఫు (P = 0.250). The inventory alone orders 23 of 24 pairs; M orders all 24. This is Daṇḍin's "mostly of non-harsh letters" in numbers.
- **The sonority score alone orders 12 of 15 and 17 of 24.** It ranks the treatise's soft example in the bottom tenth, because a nasal before a stop lowers mean sonority.
- **The Sanskrit soft examples read only "balanced".** Sanskrit has more conjuncts than Telugu, so Sanskrit verses read low against a Telugu reference.

Six more verses were scored for information:

| example | M | percentile | note |
|---|---:|---:|---|
| Kāvyādarśa 1.43, the slack texture (*śithila*) | 0.318 | 92.0 | all soft, P = 0. Daṇḍin counts it a fault |
| Kāvyādarśa 1.59, first half | −0.250 | 22.0 | 1.60 says the verse shows "harshness of texture and slackness"; the first half is usually read as the harsh one |
| Kāvyādarśa 1.59, second half | −0.125 | 34.0 | usually read as the slack one |
| Treatise 4.61, its own mādhurya (words standing apart) | 0.089 | 78.5 | |
| Treatise 4.70, ojas by compounds | 0.015 | 61.4 | the 1945 commentator remarks that its texture is not dense |
| KP 8.76, prasāda | −0.368 | 5.4 | Sanskrit against a Telugu reference |

### 7.2 Known groups: tender and fierce poems

The commentary on 4.21 predicts that fierce poems sound harsher than tender
ones. This is Fónagy's design. Groups are drawn from the English meaning of
each poem: *fierce* has at least two words from a battle-and-anger list and
none from a love-and-beauty list; *tender* is the reverse. The lists are in the
validation file.

| corpus | tender | fierce | mean M, tender | mean M, fierce | AUC (M) | AUC (I) | AUC (S) |
|---|---:|---:|---:|---:|---:|---:|---:|
| bhagavatam | 845 | 616 | −0.033 | −0.104 | 0.615 | 0.617 | 0.559 |
| kuchimanchi_timmakavi | 154 | 374 | −0.019 | −0.079 | 0.613 | 0.632 | 0.578 |
| chandassu | 600 | 147 | −0.014 | −0.114 | 0.679 | 0.687 | 0.610 |
| vemana | 35 | 22 | — | — | too few | — | — |

AUC is the chance that a tender poem outscores a fierce one. It is above 0.5 in
all three corpora (Mann–Whitney z from 4.1 to 7.5). The effect is modest, and
the grouping is rough: keywords in a machine-translated meaning. **The sequence
term does not help here:** M separates the groups no better than the inventory,
and slightly worse in one corpus.

### 7.3 Sensitivity to the choices

Each row changes one choice. ρ is the Spearman correlation with the headline M
over all 12,704 poems.

| variant | ρ with headline | exemplar pairs ordered | AUC tender vs fierce (bhagavatam) |
|---|---:|---:|---:|
| **headline** | 1.000 | 24/24 | 0.615 |
| *other sequence rules* | | | |
| no sequence term (inventory I, version 1.0) | 0.940 | 23/24 | 0.617 |
| a cumulative sum that soft sounds drain (Page's scheme, reference value ¼) | 0.979 | 24/24 | 0.620 |
| adjacent pairs only (a harsh akshara after a harsh one costs double) | 0.976 | 24/24 | 0.617 |
| runs of paruṣa aksharas only | 0.943 | 22/24 | 0.625 |
| *other weights* | | | |
| middle weights ±¼ instead of ±½ | 0.971 | 24/24 | 0.628 |
| middle weights ±¾ | 0.988 | 24/24 | 0.602 |
| conjunct class at 0 instead of −½ | 0.968 | 24/24 | 0.629 |
| the two poles alone (middle weights 0) | 0.694 | 21/24 | 0.623 |
| *other readings of the rules* | | | |
| visarga counted as harsh | 0.998 | 24/24 | 0.615 |
| every doubled consonant harsh | 0.927 | 24/24 | 0.598 |
| *phonetics alone* | | | |
| sonority score S | 0.587 | 17/24 | 0.559 |

Three sequence rules order all 24 pairs and agree with each other (ρ ≥ 0.976).
The headline rule is the one with no parameter. Limiting runs to paruṣa
aksharas loses two pairs: a dense texture is made of plain voiceless and
conjunct aksharas as well.

### 7.4 Do poets clump harsh aksharas?

The runs test on each poem's harsh / not-harsh sequence, and the pile-up of the
real order against the same classes in shuffled order:

| corpus | mean runs-test z | poems with clumped harsh aksharas (5% by chance) | pile-up, real | pile-up, classes shuffled |
|---|---:|---:|---:|---:|
| bhagavatam | +0.04 | 5.0% | 0.129 | 0.134 |
| kuchimanchi_timmakavi | +0.02 | 6.5% | 0.127 | 0.130 |
| chandassu | +0.09 | 5.2% | 0.133 | 0.137 |
| vemana | −0.25 | 10.7% | 0.110 | 0.092 |

**In classical verse the order of harsh and soft aksharas is what chance would
give.** Three corpora show neither clumping nor spreading. Vemana clumps a
little. So on real verse the pile-up mostly follows from how many harsh
aksharas a poem has, which is why M and I agree so closely (ρ = 0.94). The
sequence term matters where order departs from chance: the classical examples
of §7.1, which were chosen for their texture, and generated text
([`reports/generated_samples.md`](../reports/generated_samples.md)).

Two shuffles of the text itself:
- **Words shuffled within the poem.** M changes by 0.03 on average. Real verse does not beat its word-shuffled self: it scores higher in only 27–46% of poems. So the proposal's degradation protocol (Appendix E) still cannot admit or reject this metric.
- **Aksharas shuffled within the poem.** M falls in 55–76% of poems (bhagavatam: mean −0.057 to −0.110), because a stop no longer follows its nasal.

### 7.5 Relations to other measures (Spearman, poems)

| corpus | inventory I | pile-up P | sonority score S | share of harsh aksharas | poem length | anuprāsa z |
|---|---:|---:|---:|---:|---:|---:|
| bhagavatam | 0.94 | −0.90 | 0.58 | −0.89 | −0.12 | 0.07 |
| vemana | 0.95 | −0.91 | 0.63 | −0.91 | 0.08 | 0.06 |
| kuchimanchi_timmakavi | 0.94 | −0.91 | 0.62 | −0.91 | −0.18 | −0.04 |
| chandassu | 0.94 | −0.91 | 0.56 | −0.91 | −0.04 | 0.06 |

M agrees moderately with the phonetic score, barely depends on length, and is
independent of metric 1.

### 7.6 A check the corpus does not pass

If poets who use the classical soft configurations also preferred the more
sonorous plain consonants, the corpus would confirm the order of the middle
classes. It does not. For each of 25 plain consonants, the classical balance of
the rest of its line was compared with its sonority rank: ρ = 0.01. The order
of the middle classes rests on phonetics and on the grammar's terms, not on
corpus evidence.

### 7.7 The corpora, and lines for reading

| corpus | mean poem M | mean I | mean P | harsh | leaning harsh | balanced | leaning soft | soft |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| bhagavatam | −0.057 | 0.072 | 0.129 | 10.2% | 20.4% | 40.3% | 19.8% | 9.3% |
| vemana | −0.002 | 0.109 | 0.110 | 7.1% | 15.0% | 32.5% | 27.1% | 18.3% |
| kuchimanchi_timmakavi | −0.059 | 0.068 | 0.127 | 10.8% | 21.3% | 39.7% | 18.3% | 9.9% |
| chandassu | −0.059 | 0.074 | 0.133 | 10.0% | 20.5% | 42.1% | 18.5% | 8.9% |

Vemana is the softest: 45.8% of its aksharas are in the sonorant class, against
38–40% in the other three. The prose of the Bhāgavatamu (2,700 passages) is
softer than its verse: mean M 0.012 against −0.057.

| softest lines | M | harshest lines | M |
|---|---:|---|---:|
| నందం బనంగ నందలి | 0.750 | సత్త్వుఁడై సర్వాతిశాయి యగుచుఁ, | −4.455 |
| గని యెందు నిందు నందును | 0.722 | సర్వజ్ఞుఁ డీశుండుసర్వాత్ముఁ డవ్యయుం- | −4.250 |
| జరయందు మరణమందును | 0.700 | వ్యాళాధీశ్వర శర్వ షణ్ముఖ శుకాద్యస్తోత్ర సత్పాత్ర గో | −3.684 |
| వారి వారివారివారిఁ జేరినవారి | 0.692 | పాతపొత్తపుకట్ట సేత పట్టుకవచ్చి | −3.429 |
| నందంద వందనంబాచరించి | 0.650 | చచ్చిపుట్టుచుండు సహజముగను | −2.708 |

The heaviest harsh runs in the corpus:

| run | aksharas | load | poem |
|---|---:|---:|---|
| సితుండైశుద్ధసత్త్వుడైసర్వాతిశా | 12 | 9.5 | bhagavatam:1-62-సీ. |
| శర్వషణ్ముఖశుకాద్యస్తోత్రసత్పాత్ర | 13 | 9.5 | chandassu:chandassu-devakinandana-47-శా. |
| తోద్దండప్రతాపోత్కటస్ఫుటకోపా | 12 | 8.5 | chandassu:chandassu-sarveswara-121-మ. |
| పాతపొత్తపుకట్టసేతపట్టుక | 12 | 7.5 | kuchimanchi_timmakavi:kuchimanchi-131 |

## 8. Decisions and limitations

Decisions that a reader of the sources could make differently:

1. **The run rule.** A run is built by every akshara of negative weight and ended by any other. Its charge grows with the square of its length. The gentler rules of §7.3 (soft sounds drain the load; adjacent pairs only) rank poems almost identically (ρ ≥ 0.976). The headline rule was chosen because it has no parameter and states the requirement directly: each further harsh akshara costs more.
2. **Doubled consonants.** KP 8.75 *tulyayoḥ* can be read as any doubled consonant. Here only doubled stops are harsh (the 1945 commentary lists క్క చ్చ గ్గ). A doubled nasal is madhura under 8.74, and a doubled ల య వ keeps its class. The strict reading was tested (§7.3).
3. **Middle weights.** ±½ puts the middle classes halfway to the poles. The texts give no number. §7.3 shows the ranking barely moves.
4. **Aspirates.** The sonority scale has no aspiration contrast, so ఖ counts with క and ధ with ద. The proposal calls only unaspirated stops soft. KP marks aspirates as harsh only in the conjuncts of P1.
5. **హ and స.** Parker puts /h/ with the voiceless fricatives; Telugu హ is often voiced. Both count as voiceless, so they build runs: సహసా is a run of three.
6. **Compounds.** Both KP verses also name compound length (none or middling for mādhurya, long for ojas). That needs a compound splitter and is left to metric 4.
7. **Visarga.** Only the 1945 commentary lists it as dense. It is not counted; counting it changes nothing (§7.3).

Limitations:

- **Script, not sound.** Classes are read from letters. The dental variants of చ జ and the modern [f] of ఫ are not modelled.
- **Texture, not quality.** A nonsense line can be soft: a line of మ alone scores at the soft end ([`reports/generated_samples.md`](../reports/generated_samples.md)). The index needs the lexical metrics beside it before it can serve as a reward.
- **The emotion literature is mixed.** Kraxenberger & Menninghaus (2016) could not replicate the sound–emotion findings. §7.2 shows a modest effect here, on a rough grouping.
- **Sanskrit against a Telugu reference.** Sanskrit verses have more conjuncts, so their percentiles read low (§7.1).
- **The numbering of the sonority classes.** Parker's order of the 17 classes is confirmed from the 2011 chapter and its summaries. The numbers 17 to 1 follow that order. The 2008 paper itself is paywalled and was not read. Page (1954) is also paywalled; the cumulative-sum scheme is taken from its standard description.
- **The 1945 commentary is an OCR transcription.** Its two verses were corrected by hand where the OCR was plainly wrong.
- **Not yet validated against human ratings.**

## 9. References

See [`../references.bib`](../references.bib) (keys in brackets).

- Auracher, J., Albers, S., Zhai, Y., Gareeva, G. & Stavniychuk, T. (2011). P is for happiness, N is for sadness: Universals in sound iconicity to detect emotions in poetry. *Discourse Processes* 48(1), 1–25. [`auracher2011sound`]
- Birkhoff, G. D. (1933). *Aesthetic Measure*. Harvard University Press. [`birkhoff1933aesthetic`]
- Daṇḍin. *Kāvyādarśa*, pariccheda 1. GRETIL e-text, after the edition of Rangacharya Raddi Shastri (BORI, 1938). [`dandin_kavyadarsa`]
- Fónagy, I. (1961). Communication in poetry. *Word* 17(2), 194–218. [`fonagy1961communication`]
- Jacobs, A. M. (2017). Quantifying the beauty of words: A neurocognitive poetics perspective. *Frontiers in Human Neuroscience* 11:622. [`jacobs2017beauty`]
- Jacobs, A. M. (2018). Explorations in an English poetry corpus: A neurocognitive poetics perspective. arXiv:1801.02054. Published as: The Gutenberg English Poetry Corpus: Exemplary quantitative narrative analyses. *Frontiers in Digital Humanities* 5:5. [`jacobs2018gepc`]
- Kraxenberger, M. & Menninghaus, W. (2016). Mimological reveries? Disconfirming the hypothesis of phono-emotional iconicity in poetry. *Frontiers in Psychology* 7:1779. [`kraxenberger2016mimological`]
- Mammaṭa. *Kāvyaprakāśa*, ullāsa 8. GRETIL e-text. [`mammata_kavyaprakasa`]
- Page, E. S. (1954). Continuous inspection schemes. *Biometrika* 41(1–2), 100–115. [`page1954continuous`]
- Parker, S. (2008). Sound level protrusions as physical correlates of sonority. *Journal of Phonetics* 36(1), 55–90. [`parker2008sonority`]
- Parker, S. (2011). Sonority. In M. van Oostendorp, C. J. Ewen, E. Hume & K. Rice (eds.), *The Blackwell Companion to Phonology*, ch. 49. [`parker2011sonority`]
- Rāmarājabhūṣaṇuḍu (Bhaṭṭumūrti). *Kāvyālaṅkārasaṅgrahamu* (*Narasabhūpālīyamu*). 1920 edition and 1945 edition with the commentary of Sannidhānam Sūryanārāyaṇaśāstri, Telugu Wikisource. [`ramarajabhushana_kas1920`, `ramarajabhushana_kas1945`]
- Sandhan, J., Barbadikar, A., Maity, M., Satuluri, P., Sandhan, T., Gupta, R. M., Goyal, P. & Behera, L. (2025). Aesthetics of Sanskrit poetry from the perspective of computational linguistics: A case study analysis on Śikṣāṣṭaka. *Computational Sanskrit and Digital Humanities — World Sanskrit Conference 2025*, 15–36. ACL Anthology 2025.wsc-csdh.2. [`sandhan2025aesthetics`]
- Wald, A. & Wolfowitz, J. (1940). On a test whether two samples are from the same population. *The Annals of Mathematical Statistics* 11(2), 147–162. [`wald1940runs`]
- Whissell, C. (1999). Phonosymbolism and the emotional nature of sounds: Evidence of the preferential use of particular phonemes in texts of differing emotional tone. *Perceptual and Motor Skills* 89(1), 19–48. [`whissell1999phonosymbolism`]

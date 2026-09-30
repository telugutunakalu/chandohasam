# Metric 8 — chandas distance (*ఛందోభంగము*, *యతిభంగము* and *ప్రాసభంగము* as a count)

| | |
|---|---|
| Script | [`chandas_distance.py`](../chandas_distance.py) (version 1.1) |
| Shared code | [`../meter_engine`](../../meter_engine): `indic_meter_dawg` (scansion, the automaton of every meter), `yati` and `prasa` (the two sound engines); [`common/corpus.py`](../common/corpus.py) |
| Baseline | [`baselines/chandas_distance_baseline.json`](../baselines/chandas_distance_baseline.json), built by `python3 chandas_distance.py build-baseline` (about 75 s) |
| Validation | [`outputs/chandas_distance_validation.json`](../outputs/chandas_distance_validation.json), built by `python3 chandas_distance.py validate` ([`validation_chandas_distance.py`](../validation_chandas_distance.py), about 4 min) |
| Exemplars | [`fixtures/classical_exemplars.json`](../fixtures/classical_exemplars.json), key `broken_meter`: 2 verses the treatise's commentary gives as broken in meter, one of them also in yati |
| Tests | [`tests/test_chandas_distance.py`](../tests/test_chandas_distance.py): 31 tests |
| Proposal | Section 6 and Appendix E.1 (Tier 1, "rhythm profile"), `proposal/chandohasam_full_proposal_v3.md` |

Version 1.1 counts yati and prāsa edits as well as weight edits. Version 1.0
counted the weights only; `--weights-only` still does.

## 1. What it measures

How many aksharas must be added, removed or replaced for the poem to keep every
rule of its meter: the weight pattern of each pāda, the yati, and the prāsa.
meter_engine says whether a poem keeps them; this says how far it is when it
does not, and which aksharas are at fault.

The proposal's Tier-1 item is:

> Rhythm profile (*laya*). Gradient metrical quality instead of binary pass/fail: represent each
> line as a heavy/light (guru/laghu) string, compute edit distance (Hamming/Levenshtein) to the
> target meter pattern for partial credit, and compute regularity statistics — autocorrelation,
> entropy rate — of that string for rhythmic texture. (Appendix E.1)

This metric is the first half of that item, made exact for every meter of the
catalogue and extended to the two sound rules. The regularity statistics are
not built.

**What the classical texts call the faults.** The treatise lists them among the
defects of a sentence:

| source | definition |
|---|---|
| The treatise, 4.36 | "ఛందము యతియుం దప్పిన ఛందోయతిభంగము లగు": when the meter and the yati are missed, there is *chandobhaṅga* and *yatibhaṅga* |
| Vāmana, *Kāvyālaṅkārasūtra* 2.2.2–3 | *svalakṣaṇacyutavṛttaṃ bhinnavṛttam*: a verse fallen from its own definition is "broken-metred"; *virasavirāmaṃ yatibhraṣṭam*: a verse with a jarring pause has "lost its yati" |
| The 1945 commentary on 4.36 | Names the pāda where the meter breaks and the pāda where the yati breaks, in the treatise's example and in one of its own (§7.3) |

The texts treat each fault as present or absent. The count of edits is this
suite's addition.

## 2. Sources, and what each contributes

| Source | What is taken from it |
|---|---|
| Rāmarājabhūṣaṇuḍu, *Kāvyālaṅkārasaṅgrahamu* 4.36, with the 1945 commentary | The faults, and two example verses with the broken pādas named. They are the validation fixture (§7.3), and the first of them fixes how a closing laghu is read (§3.5). |
| meter_engine (`indic_meter_dawg`, `yati`, `prasa`), this repository | The rules themselves: the automaton of every meter, the yati points, and the yati and prāsa engines with their rule sets and profiles. Nothing about a meter, a yati class or a prāsa class is restated here. |
| Levenshtein (1966), *Binary codes capable of correcting deletions, insertions, and reversals* | The distance: the least number of insertions, deletions and substitutions that turn one string into another. |
| Wagner & Fischer (1974), *The string-to-string correction problem*, JACM 21 | The dynamic program that computes it, and the edit script read back from the table. |
| Wagner (1974), *Order-n correction for regular languages*, CACM 17 | **The distance from a string to a language.** For a regular language L and an input α, the string of L nearest to α in edit operations is found in time proportional to the length of α. A meter is such a language, so this gives the distance to a meter with many valid lines without listing them. |
| Mohri (2003), *Edit-distance of weighted automata*, IJFCS 14 | The general statement: the edit distance between the languages of two automata is a shortest path in their composition with an edit transducer. The table of §3.2 is that shortest path for a one-string automaton. |
| Terdalkar & Bhattacharya (2023), *Chandojñānam*, WSC-CSDH | **The precedent in Sanskrit prosody.** The Levenshtein distance between a line's laghu-guru string and every known meter pattern, summed over the lines of a verse; similarity = 1 − distance / length; the edit operations shown as suggested corrections (their §2.4.2). This metric keeps that design, replaces the list of patterns by the meter's automaton, and adds the two sound rules of Telugu. |
| Rajagopalan (2018), *A user-friendly tool for metrical analysis of Sanskrit verse*, WSC-CSDH | Aligning an erroneous verse to its meter by dynamic programming, showing where the yati falls in the aligned verse, and the use of this for finding errors in digital texts. |
| Manurung (2004), *An evolutionary algorithm approach to poetry generation*, PhD thesis, Edinburgh, §6.3 | The edit distance between a generated line's stress pattern and the target meter as the measure of metrical quality of generated poetry, normalised to a score in [0, 1]. |
| Mahmudi & Veisi (2023), *Automatic meter classification of Kurdish poems*, PLOS ONE 18 | The same distance on syllable-weight strings, with a maximum acceptable distance, in another quantitative meter system. |
| Cohen (1960), *A coefficient of agreement for nominal scales* | The form of the skill score: (observed − chance) / (perfect − chance). |
| Yujian & Bo (2007), *A normalized Levenshtein distance metric*, IEEE TPAMI 29 | The caution that a length-normalised edit distance is not a metric in the strict sense. The rate here is used only to compare poems against one meter. |

## 3. Algorithm

    D = weight edits + yati edits + prāsa edits

| kind | edit | meaning |
|---|---|---|
| weight | substitute | the akshara must have the other weight |
| weight | insert | an akshara of the given weight is missing here |
| weight | delete | this akshara is one too many |
| sound | yati | the akshara at a yati point does not agree with its వళి and must be replaced |
| sound | prasa | the second akshara of a pāda does not rhyme with the others and must be replaced |

Every edit costs 1.

### 3.1 The line as the engine reads it

`indic_meter_dawg.scansion` splits each printed line into aksharas and gives
each a weight, guru (`U`) or laghu (`I`). Where the tradition leaves a reading
open, the akshara carries both weights and either is free. These are the
engine's own open readings, at its most permissive level:

- an akshara before a ర-conjunct (క్ర, ప్ర …);
- a laghu before a conjunct that opens the next word;
- a guru that is guru only because a conjunct follows, since the conjunct may open a compound member.

### 3.2 Weights: one pāda against one meter

Each meter's pāda is a set of weight strings L, the language of an automaton
that meter_engine builds from `meter_rules.yaml`: one string for a vṛtta, 80
and 320 for the two pādas of kandamu, 186,624 for a sīsa pāda. The weight
distance of a line x is

    d(x, L) = min over y in L of lev(x, y)

It is computed exactly by a table over (aksharas read, state of the
automaton). Reading an akshara along an edge costs 0 if the edge's weight is
one the akshara may have and 1 otherwise; staying in the state costs 1
(delete); moving along an edge without reading costs 1 (insert). The smallest
value at an accepting state after the last akshara is d. The path that reaches
it gives the nearest valid line, the edits, and for each akshara of that line
the akshara of the poem that stands there. The cost is the number of aksharas
times the number of edges, and the largest automaton has 37 states.

### 3.3 Weights: the poem

Printed lines are matched to the pādas of the meter in order. A line may match
a pāda, or be left over, or a pāda may have no line:

    weight edits = Σ d(pāda, its slot's language)
                   + the aksharas of a printed line that matches no pāda
                   + the shortest line of a pāda that no printed line matches

The pāda sequence follows the catalogue: the slot pattern (kandamu: odd, even,
odd, even), alternative patterns (sīsamu's all-laghu form), half-lines (a sīsa
pāda printed as two lines), the gīti that follows a sīsamu, and any number of
units for a repeatable meter (dvipada, the ragadas). The smallest total over
these is kept.

### 3.4 Yati and prāsa: the right weight and the wrong sound

Once a pāda is aligned to its nearest valid line, its yati points are known:
the catalogue gives them by akshara for a vṛtta and by gaṇa for the other
meters, and the gaṇa division is that of the nearest line.

- **Yati.** For each yati point, the akshara standing there and the వళి (the first akshara of the pāda, or of the half for a sīsamu) are given to meter_engine's yati engine. A point that does not agree is one edit. A meter that allows prāsa-yati in place of yati is given that way out by the engine.
- **Prāsa.** For a meter that requires it, the pādas of a unit are given to meter_engine's prāsa engine, which compares every pair. The count is the fewest pādas that must change so that every pāda rhymes with one of them. The engine's rule that the first aksharas of the pādas have one weight is counted the same way.
- **No double charge.** An akshara that a weight edit already replaces or inserts costs nothing more: that edit can choose the sound as well as the weight. So D counts aksharas touched, and a poem far from its meter has few sound edits left to count.
- **The division that needs the fewest.** A pāda of a jāti meter with an open reading may be divided into gaṇas in more than one way at the same weight distance, and the yati point moves with the division. The division with the fewest yati edits is taken.

**Which reading of yati and prāsa.** meter_engine has three profiles (strict,
relaxed, historical) and three sandhi modes for yati (off, hypothesis, acchu).
The default here is `relaxed` with `acchu`: the reading under which the verse
of the corpus holds. Of 500 real poems in meter:

| reading (profile / yati sandhi) | poems with a yati edit | poems with a prāsa edit |
|---|---:|---:|
| strict / hypothesis | 7.8% | 1.8% |
| relaxed / hypothesis | 6.6% | 0.4% |
| **relaxed / acchu** | 0.6% | 0.4% |

`--profile` and `--yati-sandhi` choose another reading; the baseline is built
for the default one.

### 3.5 The end of a pāda

A laghu that closes a pāda is read as guru **when the next pāda opens with a
conjunct**. The conjunct makes it heavy across the pāda break, as it would
inside a line.

meter_engine is more lenient: it reads any closing laghu as guru. Two things
decide for the narrower rule.

- In verse the engine accepts, a closing laghu is read as guru 3,012 times. In 2,990 of them the next pāda opens with a conjunct: all 1,847 in the Bhāgavatamu and all 332 in Kuchimanchi. The other 22 are in the Vemana and chandassu files.
- The treatise's own example of a broken meter (4.36) has exactly this fault: its second pāda closes on a laghu, and the next opens with కుం. The engine's rule accepts that verse. The narrower rule puts the fault at the akshara the commentator names (§7.3).

`--padanta engine` applies the engine's rule. Then the weight edits are 0
exactly when the engine accepts the poem (§7.1).

### 3.6 Three numbers, and why the third is needed

    rate       r = D / max(n, N)          n = aksharas of the poem, N = of the nearest valid poem
    closeness  C = 1 − r
    skill      S = 1 − r / r_chance(meter)

**r_chance** is the mean rate of text written without the meter: Pothana's
prose (2,700 passages), cut without regard to words into 1,000 poems of the
meter's line lengths. A line's length is the mean length of the lines its slot
accepts. It is frozen per meter in the baseline:

| family | meters | chance rate, edits per 100 aksharas | chance cut (5th percentile) | chance rate on weights alone | yati edits in a chance poem | prāsa edits |
|---|---:|---:|---:|---:|---:|---:|
| vṛtta | 26 | 28.8 – 58.7 | 23.8 – 46.9 | 27.2 – 57.4 | 0.9 | 0.4 |
| upajāti (sīsamu, āṭaveladi, tēṭagīti) | 3 | 11.6 – 18.8 | 7.7 – 11.5 | 8.5 – 16.3 | 1.9 | 0 (no prāsa) |
| jāti (kandamu, dvipada, the ragadas …) | 8 | 13.7 – 23.0 | 8.3 – 16.7 | 8.5 – 18.8 | 1.9 | 1.7 |

Prose cut to length is already within 12 edits per 100 aksharas of a sīsamu
and within 29 of an utpalamāla. A meter that accepts many lines is easy to be
near. So the same D means different things in different meters, and D or C
alone cannot be compared across them. S can: it is 1 for a poem in meter, 0
for a poem no nearer than prose cut to length, and negative for a poem farther
than that, which happens when the lines have the wrong lengths. This is what
"tailored per meter" comes to: the edits are per meter through its automaton
and its yati and prāsa rules, and the scale is per meter through its chance
rate.

The sound rules matter most where the weights say least. On weights alone 10
of the 37,000 chance poems were valid as cut, all for two of the ragadas. With
yati and prāsa counted none is.

### 3.7 No meter given

Without a target, the poem is measured against all 37 meters on its weights
and the meter with the highest weight skill is chosen, not the one with the
fewest edits (§7.6). The full distance to that meter is then reported.

## 4. Rubric

On D, and on r against the meter's chance cut (the 5th percentile of the rate
of chance text):

| level | label | condition | reading |
|---:|---|---|---|
| 4 | exact | D = 0 | every rule kept |
| 3 | slip | r below the cut and D ≤ number of pādas | at most one edit a pāda on average |
| 2 | partial | r below half the cut | nearer the meter than unmetered text ever is |
| 1 | weak | r below the cut | nearer than 95% of unmetered text |
| 0 | unmetered | r at or above the cut | cannot be told from prose cut to length |

**Here a higher level is better.** The cut depends on the meter, so the middle
bands are wide for a vṛtta and narrow for a permissive meter. For
madhuragati ragada the cut is 8.3 per 100 aksharas: four edits in a 48-akshara
poem reach it.

"One edit a pāda" is a convention. It is where real verse with faults sits:
of the 767 labelled real poems not at 0, 570 are at 1 or 2 edits (§7.4).

## 5. Output

`python3 chandas_distance.py score --meter kandamu --text "…"` prints one JSON
object per poem:

| field | meaning |
|---|---|
| `score`, `label` | rubric level 0–4 and its label |
| `meter`, `meter_given` | the meter measured against; whether it was given or found as the nearest |
| `distance` | D, the number of akshara edits |
| `weight_edits`, `yati_edits`, `prasa_edits` | D by rule |
| `substitutions`, `insertions`, `deletions` | the weight edits by kind |
| `edits_per_100_aksharas`, `closeness`, `skill` | 100·r, C and S |
| `chance_rate_mean`, `chance_rate_cut` | the meter's chance figures, per 100 aksharas |
| `n_aksharas`, `target_aksharas`, `n_padas` | the poem, its nearest valid poem, the pādas matched |
| `reading` | how the closing laghu, the yati and the prāsa were read |
| `lines[]` | per pāda: `text`, `slot`, `pattern` (as scanned), `target` (the nearest valid line), `distance`, `padanta`, and `edits[]` |
| `lines[].edits[]` | `op` (substitute, insert, delete, yati, prasa, prasa_weight), `position` (1-based akshara of the pāda), `akshara`, `needs` (the weight the meter needs), `why` (for a sound edit) |

For a dataset (`--dataset`) each poem is measured against its own label.

## 6. Speed

About 3 ms a poem against one meter, and 0.02 s to find the nearest of 37.

meter_engine's prāsa-yati check reads `prasa_rules.yaml` from disk on every
call (0.5 s). This script reads it once.

## 7. Validation

All numbers come from `outputs/chandas_distance_validation.json` (seed 42)
and, for generated poems, `outputs/samples_analysis.json`.

### 7.1 Weights: agreement with meter_engine

12,672 poems of the four dataset files carry a label that is a meter of the
catalogue. With the engine's reading of a closing laghu, the weight edits are
0 exactly when the engine accepts the poem in that meter, in all 12,672. With
the default reading:

| corpus | no weight edit, engine accepts | weight edits, engine rejects | weight edits, engine accepts | no weight edit, engine rejects |
|---|---:|---:|---:|---:|
| bhagavatam | 7,355 | 10 | 0 | 0 |
| vemana | 1,004 | 149 | 11 | 0 |
| kuchimanchi_timmakavi | 1,555 | 56 | 0 | 0 |
| chandassu | 2,142 | 379 | 11 | 0 |

The 22 poems of the third column are the closing laghus that no conjunct
follows (§3.5). Each has one weight edit.

### 7.2 Yati and prāsa: agreement with meter_engine

For 300 poems in meter, read with the engine's closing laghu, the yati edits
are 0 exactly when the engine's own tool (`chandohasam.analyze`) reports the
yati as kept, in all 300; and the same for prāsa, in all 300. The yati points, the grouping of several points
and the prāsa units are therefore those of the engine.

### 7.3 The texts' own examples of broken meter and broken yati

| verse | meter | pāda the text names | edits found |
|---|---|---|---|
| The treatise's example, 4.36, as the commentary reads it | kandamu | meter: 2; yati: 4 | pāda 2, akshara 15 "డు" must be guru; pāda 4, akshara 9 "న" has no yati with "ముం" |
| Raṅgācārya's verse, quoted by the commentary | tēṭagīti | meter: 3 | pāda 3, akshara 7 "న" must be guru |

Every edit is in the pāda the commentator names, and no other pāda has one. Of
the first verse he says: "the last akshara of a kandamu's second pāda must be
guru; here it is laghu", and "in the fourth pāda the yati is broken". Those
are the two edits found. meter_engine accepts the first verse on its weights
and rejects the second.

A third example in the commentary is a single sīsa line whose OCR text is
damaged; it is not used.

### 7.4 The four corpora against their labels

| corpus | poems | exact | slip | partial | weak | unmetered | mean D | mean S |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| bhagavatam | 7,365 | 99.57% | 0.39% | 0.01% | 0 | 0.03% | 0.008 | 0.9994 |
| kuchimanchi_timmakavi | 1,611 | 94.91% | 5.03% | 0.06% | 0 | 0 | 0.068 | 0.9967 |
| vemana | 1,164 | 84.36% | 14.18% | 0 | 0 | 1.46% | 0.364 | 0.9638 |
| chandassu | 2,532 | 81.40% | 13.03% | 0.67% | 1.82% | 3.08% | 2.969 | 0.8429 |

By rule:

| corpus | poems with no weight edit | of these, with a yati edit | with a prāsa edit | mean weight edits | mean yati edits | mean prāsa edits |
|---|---:|---:|---:|---:|---:|---:|
| bhagavatam | 7,355 | 13 (0.18%) | 9 (0.12%) | 0.004 | 0.003 | 0.001 |
| kuchimanchi_timmakavi | 1,555 | 25 (1.61%) | 1 (0.06%) | 0.048 | 0.019 | 0.001 |
| vemana | 1,004 | 17 (1.69%) | 5 (0.50%) | 0.318 | 0.040 | 0.007 |
| chandassu | 2,142 | 60 (2.80%) | 21 (0.98%) | 2.862 | 0.096 | 0.012 |

Pothana's text keeps every rule almost without exception. The labels of the
Vemana and Kuchimanchi files were assigned by meter_engine, so their figures
are not independent of it; the Bhāgavatamu and chandassu labels come from the
editions.

138 poems of the chandassu file have six or more weight edits, 96 of them
sīsamu. In 122 of the 138 the printing is at fault, not the verse: 68 have a
line longer than any pāda of the meter, and 54 have a number of lines the
meter does not have (§8, item 2).

Real poems one edit from their meter, with the edit the metric reports:

| poem | line | edit |
|---|---|---|
| bhagavatam 3-800 (kandamu) | డగునతనికి స్వాంతరంగము | delete akshara 1 "డ" |
| bhagavatam 10.1-1509 (kandamu) | నంధుండవుగావు ప్రోవనర్హుండ వెందున్. | akshara 10 "ర్హుం" must be laghu |
| bhagavatam 10.2-621 (sīsamu) | సకలార్థసంవేదియొయింటిలోపలఁ- జెలితోడ ముచ్చటల్‌సెప్పుచుండు | akshara 8 "యొ" must be guru |
| bhagavatam 10.2-825 (kandamu) | బులుగల చోటనుం జేలం | akshara 5 "చో" must be laghu |

These are places to check the edition's text, which is the use Rajagopalan
(2018) and Terdalkar & Bhattacharya (2023) report for Sanskrit.

### 7.5 The ladders: the distance follows the damage

**Weights.** k random edits (delete, insert, change of weight) are made to the
weight pattern of 1,000 real poems that are in meter.

| k edits made | mean weight edits | ≤ k | = k | > 0 | mean: vṛtta | jāti | upajāti |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.89 | 100% | 89.2% | 89.2% | 1.00 | 0.88 | 0.83 |
| 2 | 1.68 | 100% | 72.1% | 96.2% | 1.94 | 1.62 | 1.56 |
| 3 | 2.46 | 100% | 58.5% | 99.4% | 2.90 | 2.34 | 2.28 |
| 5 | 3.73 | 100% | 30.9% | 99.8% | 4.70 | 3.42 | 3.35 |
| 8 | 5.18 | 100% | 10.7% | 99.9% | 7.00 | 4.44 | 4.61 |
| 13 | 7.34 | 100% | 1.8% | 100% | 10.58 | 5.90 | 6.41 |
| 21 | 9.72 | 100% | 0% | 100% | 14.68 | 7.41 | 8.41 |

- The count never exceeds the number of edits made. This is the property that makes it a minimum.
- It rises with k at every step.
- It falls below k as k grows, because later edits undo earlier ones or land on another valid line. In the jāti and upajāti meters one single edit in six to eight leaves the poem valid: the edited line is another line of the meter.

**Prāsa.** In 500 four-line poems that keep every rule, the consonant of the
prāsa akshara of k pādas is replaced by another, a different one in each pāda.

| k pādas spoiled | mean prāsa edits | poems with a prāsa edit | ≤ k |
|---:|---:|---:|---:|
| 1 | 1.00 | 99.6% | 100% |
| 2 | 1.99 | 100% | 100% |
| 3 | 2.86 | 100% | 100% |

### 7.6 The nearest meter, under error

300 poems in meter, k weight edits made, then measured against all 37 meters:

| k | labelled meter is nearest by skill | by raw edits |
|---:|---:|---:|
| 0 | 100% | 100% |
| 1 | 99.7% | 99.3% |
| 2 | 100% | 98.0% |
| 3 | 100% | 97.3% |
| 5 | 98.0% | 89.7% |

Choosing by raw edits favours the permissive meters. Choosing by skill does
not. For comparison, Chandojñānam reports the correct meter found in 98.2% of
erroneous Sanskrit verses.

### 7.7 Meters against each other

Mean weight edits per 100 aksharas of 200 poems of the row's meter against the
column's meter:

| poems of ↓ against → | āṭaveladi | champaka | kandamu | mattēbha | śārdūla | sīsamu | tēṭagīti | utpala |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| āṭaveladi | 0 | 40.2 | 25.4 | 41.9 | 42.0 | 42.0 | 11.1 | 37.5 |
| champakamāla | 24.8 | 0 | 29.6 | 28.4 | 33.1 | 12.5 | 20.3 | 9.5 |
| kandamu | 23.1 | 43.8 | 0 | 44.7 | 45.8 | 45.0 | 20.4 | 41.8 |
| mattēbha | 28.7 | 26.2 | 31.5 | 0 | 10.0 | 17.4 | 24.9 | 30.5 |
| śārdūla | 30.1 | 28.4 | 32.6 | 9.0 | 0 | 17.6 | 25.7 | 27.8 |
| sīsamu | 55.8 | 77.4 | 59.5 | 77.3 | 77.3 | 0 | 55.6 | 74.3 |
| tēṭagīti | 10.2 | 35.5 | 20.0 | 39.9 | 42.4 | 36.7 | 0 | 33.3 |
| utpalamāla | 24.9 | 8.3 | 28.6 | 33.1 | 29.8 | 13.0 | 20.6 | 0 |

The pairs the tradition treats as siblings are the near ones: utpalamāla and
champakamāla (the first guru of one is two laghus in the other: two edits a
pāda), mattēbha and śārdūla (the same relation), āṭaveladi and tēṭagīti.

### 7.8 The degradation protocol

[`reports/degradation_protocol.md`](../reports/degradation_protocol.md) runs
the proposal's four degradations on every metric. The skill S falls at every
step of all four:

| degradation | S at strengths 0, 1, 2, 3, 4 | poems lower at full strength |
|---|---|---:|
| words shuffled (10, 25, 50, 100% of words) | 0.95, 0.83, 0.58, 0.23, −0.14 | 99.7% |
| meter broken (2, 5, 10, 25% of aksharas edited) | 0.95, 0.86, 0.75, 0.58, 0.26 | 99.6% |
| filler (10, 25, 50, 100% of words) | 0.95, 0.81, 0.62, 0.38, 0.06 | 99.1% |
| synonym swap (10, 25, 50, 100% of units) | −0.61, −0.66, −0.73, −0.86, −1.07 | 88.9% |

### 7.9 Generated poems

| | real verse | E4B | 26B-A4B | DiffusionGemma |
|---|---:|---:|---:|---:|
| constrained: D | — | 0 in all 1,665 | 0 in all 1,665 | 0 in all 1,665 |
| unconstrained: mean D | 0.64 | 26.0 | 24.4 | 25.8 |
| of which weight / yati / prāsa edits | 0.61 / 0.03 / 0.00 | 25.0 / 0.68 / 0.31 | 24.0 / 0.35 / 0.06 | 25.4 / 0.25 / 0.19 |
| unconstrained: edits per 100 aksharas | 0.50 | 35.0 | 34.3 | 38.0 |
| unconstrained: mean S | 0.96 | −0.22 | −0.20 | −0.33 |
| unconstrained: rated "unmetered" | 0.8% | 97.3% | 93.3% | 96.0% |

The constrained poems keep the weights, the yati and the prāsa, as the decoder
was built to make them. Asked for a meter and left free, the three models
write text that is farther from the meter than prose cut to the meter's line
lengths (S below 0). The lines do not have the meter's lengths: 47–60% of the
weight edits are insertions, against 14% on average for the chance text. Their
sound edits are few because the weight edits already rewrite most of the
aksharas at the yati and prāsa seats.

## 8. Decisions and limitations

1. **Sound edits are counted after the weights.** The nearest line is found on weights alone, and the sound edits are then the fewest for that line (and, for a pāda with no weight edit, for any reading of it). A line one weight edit farther that saved two sound edits would not be found. D is therefore an upper bound on the true joint minimum, and exact for a poem in meter.
2. **Printed lines are taken as pādas.** A poem whose weights are right and whose lines are broken in the wrong places scores far (§7.4). A variant that ignores line breaks is possible.
3. **An edit is a weight or a sound class, not a word.** The metric says which akshara must change. It does not say that a word exists which makes the change.
4. **The nearest line is not unique.** The weight edits reported are one smallest set. Ties go to a substitution, then a deletion, then an insertion.
5. **All edits cost 1.** A substitution is not charged as a deletion and an insertion, and a sound edit costs the same as a weight edit.
6. **A yati group with several points** (sragdhara's 1, 8, 15) is charged one edit for each point that fails against the వళి. If the వళి is the akshara at fault, one edit would do; the count is then too high by one or two.
7. **The reading of yati and prāsa** is the most permissive of the engine's readings that were tried (§3.4). Under `strict` with `hypothesis`, 7.8% of real poems in meter have a yati edit.
8. **The closing laghu** (§3.5) is read more narrowly than meter_engine reads it. The engine's rule is one flag away.
9. **The chance text** is Pothana's prose with the right line lengths. For a poem of more units than the chance poem had (a long dvipada, a sīsamu with its gīti) the cut is conservative.
10. **S has no lower bound.** A poem with a missing pāda can be far below 0.
11. **The regularity statistics** of the proposal's item (autocorrelation, entropy rate of the weight string) are not built.
12. **Not yet validated against human ratings.** Items 4–6 of the proposal's rubric ("Is the chandassu, the prāsa, the yati correct?") are binary; the levels here are finer than they can confirm.

## 9. References

See [`../references.bib`](../references.bib) (keys in brackets).

- Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement* 20(1), 37–46. [`cohen1960coefficient`]
- Levenshtein, V. I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. *Soviet Physics Doklady* 10(8), 707–710. [`levenshtein1966binary`]
- Mahmudi, A. & Veisi, H. (2023). Automatic meter classification of Kurdish poems. *PLOS ONE* 18(2), e0280263. [`mahmudi2023kurdish`]
- Manurung, H. M. (2004). *An evolutionary algorithm approach to poetry generation*. PhD thesis, University of Edinburgh. [`manurung2004evolutionary`]
- Mohri, M. (2003). Edit-distance of weighted automata: General definitions and algorithms. *International Journal of Foundations of Computer Science* 14(6), 957–982. [`mohri2003edit`]
- Rajagopalan, S. (2018). A user-friendly tool for metrical analysis of Sanskrit verse. *Computational Sanskrit & Digital Humanities: Selected papers presented at the 17th World Sanskrit Conference*, 113–142. [`rajagopalan2018user`]
- Rāmarājabhūṣaṇuḍu (Bhaṭṭumūrti). *Kāvyālaṅkārasaṅgrahamu* (*Narasabhūpālīyamu*), 1920 edition, and the 1945 edition with commentary, Telugu Wikisource. [`ramarajabhushana_kas1920`, `ramarajabhushana_kas1945`]
- Terdalkar, H. & Bhattacharya, A. (2023). Chandojñānam: A Sanskrit meter identification and utilization system. *Computational Sanskrit & Digital Humanities: Selected papers presented at the 18th World Sanskrit Conference*, 113–127. ACL Anthology 2023.wsc-csdh.8. [`terdalkar2023chandojnanam`]
- Vāmana. *Kāvyālaṅkārasūtra* with the author's gloss. GRETIL e-text. [`vamana_kavyalankarasutra`]
- Wagner, R. A. (1974). Order-n correction for regular languages. *Communications of the ACM* 17(5), 265–268. [`wagner1974order`]
- Wagner, R. A. & Fischer, M. J. (1974). The string-to-string correction problem. *Journal of the ACM* 21(1), 168–173. [`wagner1974string`]
- Yujian, L. & Bo, L. (2007). A normalized Levenshtein distance metric. *IEEE Transactions on Pattern Analysis and Machine Intelligence* 29(6), 1091–1095. [`yujian2007normalized`]

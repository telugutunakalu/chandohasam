# poetry_metrics

Deterministic metrics of poetic quality for Telugu padyams: the Tier-1 core
poetics suite of the proposal (Section 6; Appendix E.1 of
`proposal/chandohasam_full_proposal_v3.md`). The suite operationalises the
*Kāvyālaṅkārasaṅgrahamu*.

Every metric follows the same contract:
- **One script per metric.** `score`, `build-baseline` (where the metric needs
  corpus statistics) and `validate` are subcommands of that script.
- **Deterministic.** There is no sampling at scoring time. Corpus statistics are
  frozen in `baselines/*.json`, and every control is seeded.
- **A rubric.** A graded level per line and per poem, with the cut points and
  their justification written down.
- **Research-backed.** Each metric has a spec in `specs/`: definition, sources
  and what is taken from each, algorithm, rubric, validation and limitations.
  Entries are in `references.bib`. Open-access PDFs and the primary texts are in
  `../reference_papers/poetry_metrics_refs/` (untracked, like all PDFs).
- **Validated before it is admitted** (Appendix E), by whichever of these
  applies: the score declines when the verse is degraded; it separates known
  groups; it places the classical texts' own examples where the texts put them.

## The suite

| # | metric | classical name | script | status |
|---:|---|---|---|---|
| 1 | Alliteration density | *anuprāsa* / *vṛttyanuprāsa* | [`anuprasa.py`](anuprasa.py) | **done**: [spec](specs/01_anuprasa.md) |
| 2 | Rhyme / caesura compliance | *prāsa*, *yati* | [`../meter_engine`](../meter_engine) | not rebuilt here: meter_engine's prāsa and yati engines are the metric; metric 8 counts their failures as edits |
| 3 | Euphony index | *mādhurya* | [`madhurya.py`](madhurya.py) | **done**: [spec](specs/03_madhurya.md) |
| 4 | Word-density index | *ojas* | [`ojas.py`](ojas.py) | **done**: [spec](specs/04_ojas.md) |
| 5 | Clarity index | *prasāda* | [`prasada.py`](prasada.py) | **done**: [spec](specs/05_prasada.md) |
| 6 | Word-resolution rate | — | — | planned |
| 7 | Defect penalties | *doṣa* | — | planned |
| 8 | Chandas distance (the edit-distance half of the *laya* item) | *chandobhaṅga* | [`chandas_distance.py`](chandas_distance.py) | **done**: [spec](specs/08_chandas_distance.md) |

**The treatise.** Its text is on Telugu Wikisource: the 1920 edition
(`నరసభూపాలీయము`) and the 1945 edition with commentary (`కావ్యాలంకారసంగ్రహము`).
Āśvāsa 4 holds the defects (verses 2–55), the ten guṇas (56–71) and the figures
of sound (72 onward). Āśvāsa 5 holds the figures of meaning. The treatise
follows Vāmana's ten guṇas, so its names do not match the proposal's triad one
to one; [specs/03_madhurya.md](specs/03_madhurya.md) §1 has the mapping.

### 1. anuprāsa: summary

Each line's consonants are tested against a chance model. Under that model,
consonants occur independently at their frequencies in the four dataset files.
The statistic is the number of same-sound pairs (Simpson's index), turned into
a z-score with its exact mean and variance under the chance model.

Two levels are scored:
- `varga` (headline): k/kh/g/gh count as one sound.
- `varna`: identical consonants only, i.e. *vṛttyanuprāsa*.

Rubric per line: none < 1.645 ≤ weak < 2.326 ≤ marked < 3.090 ≤ strong. The
poem score is the mean line level, 0–3.

Validation (all four corpora):
- The score falls in the order real > word-shuffled > word salad.
- Real poems beat their word-salad control in 62–78% of cases.
- Sound-figure pilot poems are separated from meaning-figure ones with AUC 0.78.

### 3. mādhurya: summary

Every akshara is put in one of six classes by its consonants, with a weight
from −1 (harsh) to +1 (soft):

| madhura +1 | sonorant +½ | voiced 0 | voiceless −½ | conjunct −½ | paruṣa −1 |
|---|---|---|---|---|---|
| ంక ంద ంప న్న, light ర ణ | మ న య ర ల వ, vowels | గ జ ద బ | క చ త ప స హ | క్త త్య స్త | ట డ శ ష, ప్ర ర్క, క్క ద్ధ |

The two poles are the sound lists of Kāvyaprakāśa 8.74–75, which match the
treatise's saukumārya and paruṣa. The middle classes are the major classes of
the sonority scale (Parker 2008).

The index is sensitive to sequence (version 1.1). A harsh akshara is charged
the summed harshness of the unbroken harsh run it stands in, so M = I − P:
the plain weighted proportion I minus a pile-up P that is zero when no two
harsh aksharas are adjacent. This follows Daṇḍin's definition of a tender
texture as one made *mostly* of non-harsh letters (Kāvyādarśa 1.69), and the
run load is a cumulative sum in the sense of Page (1954). A second number, the
sonority score (Jacobs 2017), is reported as a phonetic cross-check.

Rubric: five bands on M against the reference corpus (harsh, leaning harsh,
balanced, leaning soft, soft). The rubric describes texture; softer is not
better.

Validation:
- The classical texts' own soft examples all score above their harsh examples (24 of 24 pairs). The inventory alone orders 23, the sonority score alone 17.
- Tender poems score softer than fierce ones in three corpora (AUC 0.61–0.68).
- Poem rankings are stable under other weights and other sequence rules (ρ ≥ 0.92).
- In classical verse harsh aksharas fall in chance order, so there the sequence term adds little; it matters on generated text.

### 4. ojas: summary

The classical texts give ojas two sources, and the proposal asks for both
("average compound length and conjunct clusters per syllable"):

| term | what is counted | classical source |
|---|---|---|
| L, word length | aksharas per printed word | abundance of compounds: Daṇḍin 1.80, the treatise 4.69, Kāvyaprakāśa 8.75 |
| J, conjunct rate | aksharas that begin with a conjunct, per 100 | a tight texture: Vāmana 3.1.5 |

    O = ½ · [ (L − 3.844) / 0.730 + (J − 12.04) / 5.12 ]

The constants are the mean and standard deviation of L and J over the poems of
the four dataset files. The form, word length plus a second count, is that of
the readability formulas (Flesch 1948). Sinha et al. (2012) fitted the same two
features, average word length and conjuncts, to readers' judgements of Hindi
and Bangla text. Their coefficients are for prose in their units, so here each
term is standardised on Telugu verse and the two count equally.

Rubric: five bands on O against the reference corpus (light, leaning light,
moderate, leaning dense, dense). The rubric describes; denser is not better.

Validation:
- All 8 pairs that the classical texts set against each other as more and less ojas are in the texts' order.
- Printed word length tracks compound units: Spearman 0.71 with gloss units per printed word, over 5,266 Bhāgavatamu verses.
- Aspirated stops are reported and left out of O. With them in, Vāmana's own tight / not-tight pair reverses.
- Two classical claims are not confirmed on the data: prose is no denser than verse (0.52), and fierce poems are not denser than tender ones (0.49, 0.59, 0.38).

Main limitation: word length stands in for compound length, so an edition that
prints compound members apart scores lower. Metric 6's splitter should replace
it.

### 5. prasāda: summary

The proposal asks for "average word frequency, and perplexity under a language
model". Both are computed. The headline is the second, on aksharas, so that it
does not depend on how words are spaced or fused:

    H = −(1/N) · Σ log₂ P(aᵢ | aᵢ₋₂ aᵢ₋₁)      bits per akshara; perplexity = 2^H

P is an akshara trigram model with Witten–Bell interpolation. It is trained on
362,247 poems of the Padyarchana verse collection (21.2 million aksharas), with
every poem of the four dataset files removed. The classical definition is "an
expression in well-known words" (the treatise 4.57); surprisal is the measure
of how expected a text is to a reader (Hale 2001; Smith and Levy 2013).

Second numbers: the mean Zipf frequency of the words (van Heuven et al. 2014)
and the share of words found in the reference (Dale and Chall 1948).

Rubric: five bands on H against the reference corpus (obscure, leaning obscure,
ordinary, leaning clear, clear). Here a higher level is better: Mammaṭa calls
prasāda the quality common to every rasa (8.76).

Validation:
- All 5 clear / obscure pairs of the classical texts are in order.
- Real verse is clearer than its word-shuffled self in 92–98% of poems, and than its akshara-shuffled self in 100%.
- 83–99% of constrained-decoding poems are rated obscure, against 10% of real verse.

Main limitations: it measures familiar form, not meaning; "well known" means
well known in verse; repetition is not penalised.

Rebuilding the prasāda baseline needs
`../diffusion_finetuning/data/records/train.jsonl` (untracked, 1 GB). Scoring
needs only the three files in `baselines/`.

### 8. chandas distance: summary

How many aksharas must be added, removed or replaced for the poem to keep every
rule of its meter: the weights, the yati and the prāsa. meter_engine says
whether a poem keeps them; this says how far it is when it does not, and which
aksharas are at fault.

    d(line, meter) = min over the lines y the meter accepts of Levenshtein(line, y)
    D = weight edits (sum of d over the pādas, plus unmatched lines and pādas)
        + yati edits (yati points whose akshara does not agree with its వళి)
        + prāsa edits (the fewest pādas to change so that all rhyme)
    skill S = 1 − (D / aksharas) / chance rate of the meter

- **Per meter, with no per-meter code.** The target is the set of lines that meter_engine's automaton accepts: one line for a vṛtta, 186,624 for a sīsa pāda. The distance to the whole set is found exactly by dynamic programming over the automaton (Wagner 1974). The design follows Chandojñānam (Terdalkar & Bhattacharya 2023), which does this for Sanskrit with a list of patterns.
- **Yati and prāsa by meter_engine's own engines**, at the yati points of the nearest valid line. An akshara that a weight edit already rewrites is charged once.
- **Scaled per meter.** Prose cut to length is 29–59 edits per 100 aksharas from a vṛtta and 12–23 from a jāti or upajāti meter. S divides by that chance rate, so 1 is in meter and 0 is no nearer than prose.
- **Rubric:** exact (D = 0), slip (at most one edit a pāda), partial, weak, unmetered (not told apart from prose cut to length). Higher is better.

Validation:
- With the engine's reading of a closing laghu, the weight edits are 0 exactly when meter_engine accepts the poem: 12,672 of 12,672 labelled poems.
- The yati and prāsa edits are 0 exactly when the engine's own tool says they hold: 300 of 300 poems for each.
- The treatise's example of a broken meter (4.36) has one weight edit in the second pāda and one yati edit in the fourth, the two pādas the commentator names.
- k random weight edits never cost more than k, and the count rises with k at every step. Spoiling the prāsa of 1, 2 and 3 pādas gives 1.00, 1.99 and 2.86 prāsa edits on average.
- After 5 random edits the labelled meter is still the nearest of 37 in 98.0% of poems.

One departure from meter_engine: a laghu that closes a pāda is read as guru
only when the next pāda opens with a conjunct. The engine reads any closing
laghu as guru, and so accepts the treatise's own example of a broken meter.
`--padanta engine` gives the engine's reading; `--weights-only` leaves yati
and prāsa out.

## The degradation protocol

[`reports/degradation_protocol.md`](reports/degradation_protocol.md) runs the
proposal's admission test on all five metrics (`python3 degradation_protocol.py`,
about 2 min): words shuffled, meter broken, filler injected, synonyms swapped,
each at four strengths, and the nonsense control. In short:
- The chandas distance declines at every step of all four. It is the one metric that passes the rule as written.
- Prasāda declines under three and rejects the nonsense control. Under the synonym swap it rises, as a clarity metric should: the glosses are plainer words.
- Anuprāsa falls under the shuffle and the swap, and rises without limit under filler.
- Mādhurya and ojas describe texture and do not respond to order.

## The metrics on generated poems

[`reports/generated_samples.md`](reports/generated_samples.md) runs the five
metrics over the 6,660 constrained-decoding poems of `../samples/json`
(`python3 samples_analysis.py`, about 2 min). In short:
- The constraint produces heavy repetition: 23–79% of constrained poems reach the "strong" anuprāsa level that 2.7% of real poems reach.
- The two 26B models turn harsh under the constraint: 39–51% of their poems fall in the harshest tenth of real verse. The cause is conjuncts with ్ర and ్య, used to make heavy syllables, and it is concentrated in the vṛttas.
- A line of మ alone scores as strongly alliterative and soft. Neither sound metric can be a reward without the lexical metrics beside it.
- Prasāda rejects the nonsense: 200 of the 4,995 constrained poems are "ordinary" or clearer. Repetition gets through it (42 of those 200 repeat a line).
- Constrained poems are dense through conjuncts (22–27 per 100 aksharas against 12), not through longer words.
- Left free, the models are farther from the requested meter than prose cut to its line lengths (mean skill −0.20 to −0.33); 93–97% of their poems are rated unmetered. Every constrained poem keeps the weights, the yati and the prāsa.

## Running

System `python3` (3.12), standard library only. The chandas distance also
imports `../meter_engine`, which needs PyYAML.

```bash
cd poetry_metrics
python3 madhurya.py score --text "నందం బనంగ నందలి\nభ్రష్టు భ్రష్టగు గాక శిష్టుండు గాడు"
python3 anuprasa.py score --text "కళలు గలుగుఁ గాక; కమల తోడగుగాక;\nకచటతప"
python3 ojas.py score --text "మందారబిసకుందకుందాదినిధిబృంద"
python3 prasada.py score --text "అని పలికి యంతకంతకుఁ"
python3 chandas_distance.py score --meter kandamu --file poem.txt    # without --meter: the nearest meter
python3 <metric>.py score --file poem.txt                 # one line per pāda
python3 <metric>.py score --jsonl poems.jsonl --field lines --no-lines --out scores.jsonl
python3 <metric>.py score --dataset vemana --no-lines --out outputs/<metric>_vemana.jsonl
python3 <metric>.py build-baseline                        # 5–10 s; chandas_distance and prasada about 75 s
python3 <metric>.py validate                              # 25–35 s; chandas_distance about 4 min
python3 samples_analysis.py                               # the metrics on ../samples/json, ~2 min
python3 degradation_protocol.py                           # the admission test on every metric, ~2 min
python3 -m unittest discover -s tests -v                  # 121 tests
```

## Layout

```
poetry_metrics/
  README.md
  references.bib           every cited work, checked against its publisher record
  common/
    phonology.py           aksharas, consonant tokens, varga series, akshara structure, sonority scale
    corpus.py              the four dataset files as (poem, lines, English meaning)
    scoring.py             shared input/output and reference-quantile helpers
    translit.py            IAST -> Telugu script, for Sanskrit verses
    stats.py               ranks, Spearman, AUC
  anuprasa.py              metric 1
  validation_anuprasa.py   its controls, ablations and known-groups check
  madhurya.py              metric 3
  validation_madhurya.py   its exemplar, known-groups, sensitivity and order checks
  ojas.py                  metric 4
  validation_ojas.py       its contrasts, gloss check, known groups and sensitivity
  prasada.py               metric 5
  validation_prasada.py    its contrasts, degradation controls and model-order check
  chandas_distance.py      metric 8
  validation_chandas_distance.py   its chance baseline, engine agreement, ladders and nearest-meter checks
  samples_analysis.py      the five metrics on the generated poems of ../samples/json
  degradation_protocol.py  the proposal's degradations applied to every metric
  fixtures/                classical_exemplars.json: verses the classical texts quote, the pairs they contrast, their broken-meter examples
  baselines/               frozen corpus statistics, one JSON per metric; the prasāda model (two .tsv.gz)
  outputs/                 validation and analysis results (JSON)
  reports/                 written findings
  specs/                   one spec per metric
  tests/
```

The unit of scoring is the printed line (pāda). A sīsa pāda printed on one line
with ` - ` between its halves is split into its two half-lines, as meter_engine
reads it.

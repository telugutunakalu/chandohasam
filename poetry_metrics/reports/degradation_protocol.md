# Do the metrics follow the degradation protocol?

Date: 2026-09-30. Metrics: anuprāsa 1.0, mādhurya 1.1, ojas 1.0, prasāda 1.0, chandas distance 1.1.
Script: [`degradation_protocol.py`](../degradation_protocol.py) (about 2 min, seed 42).
Numbers: [`outputs/degradation_protocol.json`](../outputs/degradation_protocol.json).

## The rule being tested

The proposal (Evaluation Plans) admits a metric only if it passes this:

> each metric is scored on canonical verse against systematically degraded versions
> (word-shuffled, synonym-swapped, meter-broken, filler-injected) and admitted only if it
> declines monotonically; a metrically valid nonsense control must be rejected by every
> meaning metric.

## The answer

**One metric of five passes the rule as written: the chandas distance.** Prasāda
passes three of the four degradations and rejects the nonsense control; on the
fourth it goes up, and it should. The three sound metrics do not pass.

| | words shuffled | meter broken | filler injected | synonyms swapped | nonsense control |
|---|---|---|---|---|---|
| **chandas distance** (skill S) | declines | declines | declines | declines | in meter by construction; not a meaning metric |
| **prasāda** (clarity, −H) | declines | declines | declines | **rises** | rejected |
| **anuprāsa** (z) | declines | **rises** | **rises** | declines | scores above real verse |
| **mādhurya** (M) | no response | declines | **rises** | declines | about level with real verse |
| **ojas** (O) | no response | no response | declines | **rises** | scores above real verse |

"Declines" means the mean falls at every one of four strengths and, at full
strength, more poems fall than rise by a sign test at z ≤ −3.09. "Rises" is the
same test the other way: the metric rewards the degradation.

## How it was run

1,600 real poems: 400 from each of the four dataset files, drawn from the poems
whose label is a meter of the catalogue. Each degradation is applied at four
strengths and all five metrics are scored on every version.

| degradation | what is done | strengths |
|---|---|---|
| words shuffled | a share of the poem's words change places; every line keeps its word count | 10, 25, 50, 100% of words |
| meter broken | a share of the aksharas are edited: deleted, given another akshara of the poem as a new neighbour, or changed in vowel length | 2, 5, 10, 25% of aksharas |
| filler injected | a share of the words are replaced by one akshara repeated to the word's length (మ, న, ల, ర or త, one per poem). This is the filler found in the constrained poems | 10, 25, 50, 100% of words |
| synonyms swapped | a share of the verse's units are replaced by their gloss from the edition. Bhāgavatamu only, 343 verses. The ladder starts from the verse as its glossed units, with sandhi and compounds taken apart | 10, 25, 50, 100% of units |

The nonsense control is the 4,995 constrained-decoding poems of `samples/json`:
in meter, and mostly not made of real words.

## The ladders

Mean of each metric at each strength. "Lower" is the share of poems whose score
at full strength is below that of the original.

### Words shuffled

| metric | original | 10% | 25% | 50% | 100% | lower | verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| chandas S | 0.953 | 0.826 | 0.580 | 0.232 | −0.136 | 99.7% | declines |
| prasāda −H | −6.057 | −6.119 | −6.242 | −6.426 | −6.591 | 96.6% | declines |
| anuprāsa z | 0.690 | 0.649 | 0.557 | 0.421 | 0.331 | 63.8% | declines |
| mādhurya M | −0.042 | −0.043 | −0.042 | −0.041 | −0.040 | 39.8% | no response |
| ojas O | −0.112 | −0.112 | −0.112 | −0.112 | −0.112 | 0% | no response |

Ojas is built from counts that a shuffle cannot change. Mādhurya's sequence
term sees only adjacent aksharas, so moving words barely moves it.

### Meter broken

| metric | original | 2% | 5% | 10% | 25% | lower | verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| chandas S | 0.953 | 0.861 | 0.747 | 0.584 | 0.264 | 99.6% | declines |
| prasāda −H | −6.057 | −6.290 | −6.604 | −7.121 | −8.535 | 100% | declines |
| mādhurya M | −0.042 | −0.044 | −0.045 | −0.045 | −0.052 | 55.7% | declines |
| ojas O | −0.112 | −0.111 | −0.108 | −0.107 | −0.090 | 43.5% | no response |
| anuprāsa z | 0.690 | 0.701 | 0.717 | 0.747 | 0.823 | 40.9% | rises |

Prasāda falls because a broken akshara also breaks a word. Anuprāsa rises a
little: an inserted akshara is a copy of another in the poem, which adds a
repeated sound.

### Filler injected

| metric | original | 10% | 25% | 50% | 100% | lower | verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| chandas S | 0.953 | 0.810 | 0.621 | 0.382 | 0.065 | 99.1% | declines |
| ojas O | −0.112 | −0.224 | −0.409 | −0.689 | −1.261 | 99.5% | declines |
| prasāda −H | −6.057 | −6.191 | −6.358 | −6.545 | −6.611 | 73.1% | declines |
| mādhurya M | −0.042 | −0.023 | −0.014 | −0.098 | −3.212 | 21.4% | rises |
| anuprāsa z | 0.690 | 2.24 | 6.48 | 18.60 | 64.50 | 0% | rises |

- **Anuprāsa rewards filler without limit.** Every poem scores higher, and a poem of pure filler is at z = 64.
- **Mādhurya rises in 79% of poems**, those whose filler is a soft akshara. Its mean falls at full strength only because one of the five fillers, త, is a voiceless stop, and a line of it is one long harsh run.
- **Prasāda declines, weakly.** A poem of pure filler is still clearer than the real poem in 27% of cases. A language model is not surprised by repetition.
- **The chandas distance catches it** because a repeated short akshara is all laghus.

### Synonyms swapped

| metric | verse as units | 10% | 25% | 50% | 100% | lower | verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| chandas S | −0.608 | −0.661 | −0.727 | −0.856 | −1.074 | 88.9% | declines |
| anuprāsa z | 1.123 | 0.863 | 0.580 | 0.304 | 0.084 | 75.5% | declines |
| mādhurya M | −0.047 | −0.051 | −0.059 | −0.071 | −0.130 | 61.5% | declines |
| ojas O | −0.759 | −0.693 | −0.582 | −0.437 | −0.147 | 11.7% | rises |
| prasāda −H | −7.706 | −7.475 | −7.206 | −6.734 | −5.980 | 2.0% | rises |

A gloss keeps the meaning and replaces the poet's word by a plain modern one.

- **Prasāda rises, and that is the right answer.** The glossed text is clearer than the verse. For a clarity metric a synonym swap is not a degradation.
- **Anuprāsa declines.** The alliteration was in the poet's choice of words, and the swap removes it. This is the best evidence in the suite that anuprāsa measures something the poet did.
- **Ojas rises** because glosses are longer words.

The ladder starts below the printed verse for the chandas distance (the printed
verses are at S = 1.0), because taking the sandhi apart already breaks the meter.

### The nonsense control

The chance that a constrained-decoding poem scores above a real poem, over the
nine model and strategy cells:

| metric | chance of scoring above real verse | reading |
|---|---:|---|
| prasāda (clarity) | 0.005 – 0.08 | **rejected** |
| mādhurya | 0.25 – 0.53 | not told apart |
| chandas S | 0.53 | level: both are in meter |
| ojas | 0.65 – 0.75 | scores higher |
| anuprāsa | 0.68 – 0.95 | scores higher |

The rule asks only meaning metrics to reject the control. Prasāda is the one
metric here that reads anything like meaning, and it does reject it.

## What follows

1. **The chandas distance is admitted** under the rule as written.
2. **Prasāda should be admitted.** Its one rise is on the degradation that makes a text clearer.
3. **Anuprāsa cannot be admitted as it stands.** It responds to the poet's choices (it falls under the shuffle and the swap) and it is defeated by filler. It needs the repetition defect of metric 7 in front of it.
4. **Mādhurya and ojas are descriptions of texture, and the rule was not written for them.** Neither has a "worse" direction: the classical texts assign soft and dense textures to different rasas. They do not decline under a shuffle because they do not measure order.
5. **The rule itself needs one change.** As written, no metric that measures a single property can pass, since each degradation attacks a different property. A rule the suite can be held to:
   - each metric names the degradations that attack what it measures, and must decline monotonically under those;
   - no metric may rise under filler or under the nonsense control, unless it is reported only for poems that pass the gates (prasāda "ordinary" or clearer, chandas distance 0).

   Under this rule the chandas distance and prasāda are admitted outright, and anuprāsa, mādhurya and ojas are admitted behind the gates.

## Limits of this check

- **The synonym swap is a gloss swap.** The repository has no synonym dictionary. The glosses exist for the Bhāgavatamu only, they are modern prose words, and the ladder starts from the verse with its sandhi taken apart.
- **The filler is one akshara repeated.** Filler made of real particles or stock words is not tested.
- **One seed, 400 poems a corpus.** The sign tests are far from their thresholds except for ojas under a broken meter (z = 3.09, at the threshold).
- **Monotone is judged on means.** A step that reverses by less than sampling error would still fail it; none of the "declines" verdicts is close.
- **The proposal also requires correlation with human ratings.** Nothing here replaces that.

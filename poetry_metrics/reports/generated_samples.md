# The poetry metrics on the constrained-decoding poems

Date: 2026-09-30. Metrics: anuprāsa 1.0, mādhurya 1.1, ojas 1.0, prasāda 1.0, chandas distance 1.1.
Script: [`samples_analysis.py`](../samples_analysis.py) (about 2 min).
Numbers: [`outputs/samples_analysis.json`](../outputs/samples_analysis.json); one row per poem in `outputs/samples_scores.jsonl`.

## What was measured

The 6,660 poems of [`samples/json`](../../samples/json/): three models, four
ablations each, 555 poems per cell (37 meters × 3 topics × 5 seeds).

| model | decoding |
|---|---|
| Gemma-4 E4B | autoregressive |
| Gemma-4 26B-A4B | autoregressive |
| DiffusionGemma 26B-A4B | block diffusion |

The ablations are the free baseline (no constraint; no poem in meter, bar one)
and three constrained strategies (masking only, masking + backtracking,
hybrid), whose poems are all in meter. The reference is the real verse of the
four dataset files (12,704 poems), scored by the same code.

Anuprāsa, mādhurya and ojas measure sound and word shape only. Prasāda measures
whether the akshara sequences are those of known Telugu verse. The chandas
distance counts the akshara edits between a poem and its meter: weights, yati and prāsa. None of the
five reads meaning, and most words of the constrained poems are not real words
([`samples/README.md`](../../samples/README.md)).

Findings 1–8 are from the two sound metrics. Findings 9 and 10 add prasāda and
ojas. Finding 11 adds the chandas distance.

## Findings

### 1. The constraint, not the model, produces heavy repetition

Anuprāsa z of the poem (`varga` level). "Strong" is z ≥ 3.09.

| | real verse | E4B | 26B-A4B | DiffusionGemma |
|---|---:|---:|---:|---:|
| free baseline: mean z | 0.47 | −0.20 | 1.13 | 1.38 |
| constrained: mean z | — | 2.2 – 2.8 | 4.0 – 4.4 | 4.2 – 9.1 |
| free baseline: poems at "strong" | 2.7% | 0.4% | 9.9% | 19.1% |
| constrained: poems at "strong" | — | 23 – 34% | 48 – 49% | 47 – 79% |
| constrained: chance a generated poem outscores a real one | — | 0.68 – 0.73 | 0.82 – 0.83 | 0.84 – 0.95 |

- Without the constraint, E4B alliterates less than real verse and 26B-A4B about as much (chance of outscoring a real poem 0.33 and 0.50).
- Under the constraint, a quarter to four-fifths of the poems reach a level that 2.7% of real poems reach.
- This is recycling, not craft. Anuprāsa z rises as the share of distinct aksharas in the poem falls (Spearman −0.50, −0.42, −0.62 for the three models).
- Whole repeated lines are only part of it. DiffusionGemma repeats a line in 2–4% of its constrained poems (26B-A4B: 29–42%) and still has the highest z: its repetition is inside the line.

### 2. The two large models turn harsh under the constraint; E4B does not

Mādhurya M of the poem, and the share of poems in the "harsh" band, which holds
10% of real poems.

| | real verse | E4B | 26B-A4B | DiffusionGemma |
|---|---:|---:|---:|---:|
| free baseline: median M | −0.03 | 0.00 | 0.02 | 0.02 |
| constrained: median M | — | −0.03 – 0.00 | −0.23 – −0.19 | −0.29 – −0.23 |
| free baseline: poems in the harsh band | 10% | 2% | 13% | 8% |
| constrained: poems in the harsh band | — | 16 – 18% | 39 – 45% | 46 – 51% |
| constrained: mean pile-up P | 0.13 | 0.14 – 0.15 | 0.28 – 0.33 | 0.30 – 0.31 |

Free text from all three models is a little softer than classical verse. Under
the constraint, close to half the poems of the two 26B models land in the
harshest tenth of real verse, and their harsh aksharas pile up twice as much.

### 3. How it happens: heavy syllables are made with ్ర and ్య, not the way Telugu makes them

Per 100 aksharas:

| | real verse | E4B constrained | 26B-A4B constrained | DiffusionGemma constrained |
|---|---:|---:|---:|---:|
| aksharas with a conjunct onset | 12.3 | 20.7 – 23.4 | 22.9 – 25.3 | 24.1 – 25.5 |
| conjuncts with ర (rule P2) | 3.5 | 7.4 – 8.6 | 11.8 – 14.0 | 11.7 – 12.2 |
| doubled stops (rule P3) | 2.4 | 0.4 | 0.2 – 0.3 | 0.4 – 0.5 |
| stop after a nasal (rule M1, soft) | 6.9 | 4.7 – 4.9 | 3.0 – 3.4 | 2.1 – 2.6 |

- The commonest conjuncts of real verse are doubled consonants and a few Sanskrit clusters: న్న ట్ట ల్ల క్క చ్చ ప్ర క్ష.
- The commonest conjuncts of constrained text are న్ర ల్ర మ్ర మ్య ల్య న్య క్ర త్ర. Several hardly occur in real verse: న్ర 0.003 per 100 aksharas against up to 1.8 in constrained text, ల్ర 0.001 against up to 1.7, మ్య 0.011 against up to 3.5.
- A conjunct makes the syllable before it heavy. When the meter needs a guru, the decoders reach for a consonant plus ్ర or ్య. Real verse gets its gurus from doubled consonants, long vowels and nasal-plus-stop, and the last of these is the soft configuration the classical texts praise.
- The free baselines have no such excess (5.5 – 10.8 conjunct onsets per 100).

### 4. The damage is in the vṛttas

Mean M of constrained poems by meter class, with the share of real words
(two or more aksharas, found in the dataset verse):

| meter class | E4B: M | real words | 26B-A4B: M | real words | DiffusionGemma: M | real words |
|---|---:|---:|---:|---:|---:|---:|
| jāti | 0.09 | 30% | −0.01 | 43% | 0.02 | 25% |
| upajāti | 0.10 | 31% | 0.03 | 40% | 0.07 | 26% |
| vṛtta | −0.16 | 9% | −0.49 | 13% | −0.52 | 7% |

In the eight meters that the datasets also hold in number:

| meter | real verse | E4B | 26B-A4B | DiffusionGemma |
|---|---:|---:|---:|---:|
| kandamu | −0.02 | 0.08 | −0.02 | 0.02 |
| āṭaveladi | −0.03 | 0.11 | 0.04 | 0.01 |
| tēṭagīti | −0.04 | 0.08 | 0.00 | 0.08 |
| sīsamu | −0.08 | 0.11 | 0.04 | 0.12 |
| champakamāla | −0.04 | 0.01 | −0.36 | −0.31 |
| utpalamāla | −0.08 | −0.04 | −0.31 | −0.35 |
| mattēbhavikrīḍitamu | −0.10 | −0.18 | −0.73 | −0.47 |
| śārdūlavikrīḍitamu | −0.11 | −0.19 | −0.57 | −0.55 |

In the native meters, where the poet chooses among gaṇas, the generated texture
is as soft as real verse or softer. In the vṛttas, where every syllable's
weight is fixed, it collapses, and so does the share of real words. Real vṛttas
are only slightly harsher than real native meters.

### 5. Harshness tracks how much of the text is not Telugu

Spearman correlations over each model's 1,665 constrained poems:

| M against | E4B | 26B-A4B | DiffusionGemma |
|---|---:|---:|---:|
| share of real words | 0.34 | 0.53 | 0.46 |
| share of tokens the constraint overrode | −0.07 | −0.15 | −0.55 |
| mean log-probability of the chosen tokens | −0.09 | 0.01 | 0.48 |

The softer poems are the ones with more real words. For DiffusionGemma, M also
falls as the constraint overrides more of the model's choices.

### 6. Filler fools both metrics

The highest anuprāsa poem and the softest poem of the whole set are strings of
one letter:

> మమమమమమమ మ జమమమమమ మ మమ మమమమము మమమమమ మమమమసమమును మ …
> (DiffusionGemma, sīsamu, hybrid; anuprāsa z = 110)

> మమమమమమమమమమమమమమమమమముమమమమమ్ …
> (DiffusionGemma, utsāhamu, hybrid; M = 0.52, the soft band)

Both are in meter. మ is a sonorant, so a line of it is "soft", and it repeats,
so it is "alliterative". The proposal's admission rule requires a metrically
valid nonsense control to be rejected by every meaning metric; these two are
sound metrics and they reward it. At the other end the metric behaves as it
should:

> మహ్యుగ్యున్రుత్య్య్మల్రుత్య్య్మల్రుత్ …
> (E4B, vidyunmāla, masking only; M = −11.4, against −4.5 for the harshest real line)

The sonority score is fooled more broadly. It rates constrained text above real
verse (chance 0.60 – 0.82), because of the మ and య filler, while M rates it
below.

### 7. The large models match sound to topic when free; the constraint weakens this

Topic T1 is a mother's love; T2 and T3 are Hanumān's and Rāma's journeys to
Laṅkā. The figure is the chance that a T1 poem is softer than a T2 or T3 poem.
In real verse, tender poems are softer than fierce ones with chance 0.61 – 0.68
([spec §7.2](../specs/03_madhurya.md)).

| | E4B | 26B-A4B | DiffusionGemma |
|---|---:|---:|---:|
| free baseline | 0.48 | 0.80 | 0.67 |
| masking only | 0.45 | 0.63 | 0.56 |
| masking + backtracking | 0.50 | 0.59 | 0.52 |
| hybrid | 0.51 | 0.62 | 0.56 |

The two 26B models, left free, write the tender topic in softer sounds. The
constraint cuts the effect by more than half. E4B shows none. One caution: the
poems reuse the words of their prompts (అమ్మ, ప్రేమ; సముద్రము, శ్రీరాముడు,
రక్షించు), and those words differ in texture, so part of the effect is the
prompt's own vocabulary.

### 8. Strategies

Backtracking lowers the repetition a little for E4B (mean z 2.2 against 2.5 –
2.8) and a lot for DiffusionGemma (4.2 against 7.0 and 9.1). It has no consistent
effect on the texture. Hybrid decoding with DiffusionGemma repeats the most.

### 9. Prasāda rejects what the sound metrics reward

Surprisal H under the akshara trigram model, in bits per akshara. Lower is
clearer. The "obscure" band holds the hardest 10% of real verse.

| | real verse | E4B | 26B-A4B | DiffusionGemma |
|---|---:|---:|---:|---:|
| free baseline: mean H | 6.01 | 5.63 | 5.38 | 6.72 |
| constrained: mean H | — | 10.6 – 11.2 | 10.6 – 11.4 | 11.9 – 12.6 |
| constrained: poems in the obscure band | 10% | 84 – 91% | 83 – 91% | 94 – 99% |
| constrained: chance a generated poem is harder than a real one | — | 0.94 – 0.97 | 0.92 – 0.96 | 0.98 – 0.995 |

- **The metrically valid nonsense is rejected.** Of 4,995 constrained poems, 200 (4%) are "ordinary" or clearer. For comparison, a real poem with its aksharas shuffled is at 11.5 bits: the constrained poems are about as unfamiliar as shuffled verse.
- **Free text is clear.** The two autoregressive models, unconstrained, write plainer Telugu than classical verse.
- **It follows the real words.** H falls as the share of real words rises (Spearman −0.61, −0.63, −0.55).
- **The vṛttas again.** Mean H of constrained poems:

| meter class | real verse (by meter) | E4B | 26B-A4B | DiffusionGemma |
|---|---:|---:|---:|---:|
| native meters (jāti, upajāti) | 5.7 – 5.9 | 7.2 – 7.7 | 7.6 – 7.8 | 8.1 – 9.1 |
| vṛttas | 5.9 – 7.2 | 12.3 | 12.3 | 13.8 |

- **Who passes.** Of the 200, 117 are from 26B-A4B, 73 from E4B and 10 from DiffusionGemma; 194 are in the native meters and 6 in vṛttas. Their mean share of real words is 0.43, against 0.15 for the rest.
- **Its blind spot is repetition.** A language model is not surprised by a repeated akshara. The first line of the మ poem of finding 6 is at 6.96 bits, "leaning obscure" on the line scale; the whole poem is at 7.19 bits, just inside the obscure band (the cut is 7.06). Of the 500 most alliterative constrained poems, 463 (93%) are rated obscure and 15 are "ordinary" or clearer. Of the 200 poems that pass, 42 repeat a whole line.

### 10. Generated text is dense through conjuncts, not through long words

| | real verse | E4B | 26B-A4B | DiffusionGemma |
|---|---:|---:|---:|---:|
| constrained: word length L (aksharas) | 3.84 | 4.35 – 4.52 | 3.83 – 4.17 | 3.70 – 4.20 |
| constrained: conjunct rate J (per 100 aksharas) | 12.0 | 22.2 – 24.5 | 24.4 – 26.6 | 25.7 – 27.1 |
| constrained: poems in the "dense" band | 10% | 49 – 58% | 46 – 53% | 57 – 60% |
| free baseline: mean ojas O | 0.00 | −0.28 | −0.38 | −1.10 |

The conjunct rate doubles while word length barely moves. In classical verse a
dense texture comes with long compounds; here it comes from the ్ర / ్య
clusters of finding 3. In the vṛttas the mean O is +2.3 to +2.5; in the native
meters it is −0.3 to −1.4, below the real-verse mean of 0. Free text is lighter than
classical verse, DiffusionGemma's most of all (72% of its baseline poems are in
the "light" band).

### 11. Left free, the models are farther from the meter than prose

The chandas distance of each poem to the meter it was asked for: the akshara
edits needed for the weights, the yati and the prāsa. The skill S is 1 for a
poem in meter and 0 for one no nearer the meter than prose cut to the meter's
line lengths.

| | real verse | E4B | 26B-A4B | DiffusionGemma |
|---|---:|---:|---:|---:|
| constrained: edits to the meter | — | 0 in all 1,665 | 0 in all 1,665 | 0 in all 1,665 |
| unconstrained: mean edits D | 0.64 | 26.0 | 24.4 | 25.8 |
| of which weight / yati / prāsa edits | 0.61 / 0.03 / 0.00 | 25.0 / 0.68 / 0.31 | 24.0 / 0.35 / 0.06 | 25.4 / 0.25 / 0.19 |
| unconstrained: edits per 100 aksharas | 0.50 | 35.0 | 34.3 | 38.0 |
| unconstrained: mean skill S | 0.96 | −0.22 | −0.20 | −0.33 |
| unconstrained: rated "unmetered" | 0.8% | 97.3% | 93.3% | 96.0% |

- **The constrained poems keep all three rules.** No weight edit, no yati edit and no prāsa edit in any of the 4,995.
- **The free text has no usable meter in it.** About a third of its aksharas would have to change. Mean skill is below 0: the poems are farther from the meter than prose cut to the right lengths.
- **The lines have the wrong lengths.** 47–60% of the weight edits are insertions of a missing akshara. In prose cut to the meter's lengths insertions are 14% of the edits on average. The poems of the two 26B models are 12% and 15% shorter than the nearest poem in meter.
- **Few sound edits are left to count.** The weight edits already rewrite most of the aksharas at the yati and prāsa seats, and an akshara is charged once.
- **The native meters are not easier for the models.** Their raw distances are smaller (13–18 edits against 28–31 for the vṛttas), but those meters accept many lines, and prose is already near them. On skill the native meters are worse: −0.23 to −0.90, against −0.12 to −0.23 for the vṛttas.
- **No partial credit to build on.** Between 0 and 8% of unconstrained poems in any class of meter have a skill above 0.5. The models do not get most of a line right and miss a little; the constraint supplies all of the meter.

## What this means for the project

1. **No sound metric can be a reward on its own, and prasāda is the first gate.** A decoder or a reward that maximised anuprāsa or softness would converge on మమమమ. Reading the sound metrics only for poems that are at least "ordinary" on prasāda removes 96% of the constrained poems. Repetition passes that gate (42 of the 200 poems that pass repeat a line), so the repetition defect (metric 7) is still needed, and the word-resolution rate (metric 6) would make the gate lexical.
2. **As diagnostics of constraint damage they already work.** Anuprāsa "strong" rates of 23–79% against 2.7%, conjunct onsets at twice the real rate, the ్ర / ్య clusters, and surprisal near that of shuffled verse point to the same fault from four sides, without a dictionary.
3. **The fault to fix is how the decoder makes a guru.** Penalising or masking consonant + ్ర / ్య continuations that do not complete a known word, or preferring doubled consonants, long vowels and nasal-plus-stop at guru positions, would attack the harshness at its source. The lexical gate planned for the diffusion decoder addresses this.
4. **Evaluate vṛttas and native meters separately.** Pooled numbers hide that the native meters come out with a normal texture and the vṛttas do not.
5. **The sequence term of mādhurya earns its place here.** On real verse it adds little, because poets' harsh sounds fall in chance order. On generated text the pile-up doubles.
6. **The chandas distance is the gradient the binary check lacks.** "In meter: 0 of 555" says nothing about how far. The distance shows the free models are at chance or below, and that the first thing missing is line length. It is also the number to track while fine-tuning: it can fall before any poem is fully in meter.

## Cautions

- The comparison is against classical verse. Free modern text differs from it for reasons that are not faults: fewer Sanskrit compounds, more sonorants.
- Each cell has 15 poems per meter, so the per-meter figures in §4 are means of 45 poems per model (three strategies pooled).
- "Real words" means words of two or more aksharas found in the verse of the four dataset files. A correct modern word that is absent from them counts as not real; this is why the free baselines reach only 42–48%.
- The generated poems were not read for meaning here.

# EXP-22 — Chandas direction extraction (diff-in-means / CAA)

| | |
|---|---|
| **Category** | G. Steering |
| **Origin** | chandohasam (G4 / NH13, NH14; G4c, formerly EXP-39) |
| **Depends on** | EXP-07; EXP-24's per-metre vectors for the all-pairs step |
| **Status** | coarse contrast and **all 28 pairs rerun with `<bos>`** (2026-09-29): no pair is coherent enough to steer; tight contrast in EXP-38 |
| **Cost** | minutes |

## Question
Is there a linear direction in activation space that corresponds to metrical
form? Which chandas-vs-chandas directions are coherent enough to steer with?

## Why it matters
If one exists, metre becomes steerable at inference without retraining. That is
a fundamentally different lever from logit constraints, because it could shift
what the model *wants* to say rather than filter what it may say. EXP-23 steers
with a chandas-vs-chandas direction, so it needs to know which pairs are
coherent before choosing any.

## Methodology
1. **Pooled vectors.** Use last-real-token pooling at every layer (`L0`–`L35`),
   with `<bos>` prepended.
2. **Three contrasts**, each giving a direction per layer:
   - **coarse**: poem vs its own bhavam,
     `d^(l) = mean_i h_l(poem_i) − mean_i h_l(bhavam_i)`;
   - **tight**: metrically correct vs broken poems of the same metre, with
     content and register held fixed. Built synthetically in **EXP-38**, because
     natural negatives are too scarce;
   - **chandas-vs-chandas**: one metre's per-poem diffs against another's.
3. **Coherence check before trusting any direction.** Take the mean pairwise
   cosine of the individual per-pair diff vectors, per layer. Low agreement
   predicts an unreliable steering vector.
4. **All 28 chandas-vs-chandas pairs** (formerly EXP-39).
   - **Directions come free.** The direction for pair `(a, b)` is
     `d_ab = d_a − d_b`, where `d_c = mean_{i∈c}(h(poem_i) − h(bhavam_i))` are
     the 8 per-metre vectors EXP-24 already computes. No new forward passes are
     needed.
   - **Coherence is the new work.** Use the definition behind the existing
     కందము/మత్తకోకిల number; **read it from
     `pipeline/common/phase4_direction.py` before extending it**. If that code
     does not already define it this way, use: pair poems across the two metres
     by a seeded random matching, form `c_k = diff_{a,k} − diff_{b,k}`, and take
     the mean pairwise cosine of the `c_k`.
   - **Flag weak pairs.** Mark every pair whose peak coherence falls below a
     threshold fixed in advance (for example, the coarse contrast's 0.322) as
     unfit for steering.

## Inputs
(poem, bhavam) pairs; per-layer pooled activations; metre labels.

## Metrics
- Per-layer coherence for each contrast type, and the vector norm per layer.
- The distribution of coherence across the 28 pairs, each pair's peak layer,
  and the flagged pairs.
- Optional: whether pair coherence tracks EXP-24's gaṇa-pattern distance
  `D_struct`.

## Expected result / baseline
- NH14: the coarse contrast is dominated by register and vocabulary; the tight
  and chandas-vs-chandas contrasts are more coherent and more metre-specific.
- NH13: peak coherence at the peak-divergence layer (EXP-21).

## Observed
Base `gemma-4-E2B-it`, 200-poem balanced sample.

| contrast | result |
|---|---|
| coarse (poem vs bhavam) | low-to-moderate coherence throughout, peak **0.322 at L4** (`n_pairs = 100`); consistent with NH14's register reading |
| tight | **not computed**: only 13 of 200 sampled poems are `matched=False`, spread too thin across 8 metres; see EXP-38 |
| chandas-vs-chandas (కందము vs మత్తకోకిల, 1 of 28 pairs) | **consistently 0.5–0.65** across mid-to-late layers, the most coherent contrast in the project |

The direction vectors are saved with the per-layer data. There is no
fine-tuned comparison, because no checkpoint exists.


**Rerun with `<bos>`, all 28 pairs (2026-09-29).** `experiments/scripts/exp22_directions.py`,
EXP-35's 200-poem sample (25 poems per metre), last-token states at all 36
hidden-state indices. L0 is the embedding output, and transformers returns the
final-norm output as L35; both were checked. The pipeline's
`phase4_direction.py` is not available here, so pair coherence uses the spec's
fallback: a seeded random matching of the two metres' poems, then the mean
pairwise cosine of `c_k = diff_a,k − diff_b,k`. The flag threshold was fixed
before the run at 0.322. A null comes from 20 random 25/25 splits of each
pair's 50 poems (560 splits).

| | result |
|---|---|
| coarse (poem vs bhavam, n = 200) | peak **0.475 at L35** (final norm); intermediate peak 0.411 at L6; 0.332 at L4 |
| chandas-vs-chandas peaks | **all 28 below 0.322** (range 0.003–0.158, median 0.064) |
| null peak (random splits) | 95th percentile 0.068, 99th 0.128 |
| pairs above the null's 95th percentile | 13 of 28; the strongest are kandamu vs tetagiti 0.158, champakamala vs tetagiti 0.125, aataveladi vs kandamu 0.113 (all at L1) |
| peak layers | 17 of 28 at L0–L3 (10 at L1) |
| kandamu vs mattakokila, L8–L35 | **0.025–0.068** (pipeline: 0.5–0.65) |
| stability over 20 matchings | peak sd ≤ 0.013 for every pair |

- **No chandas-vs-chandas direction is coherent enough to steer.** Every pair
  is flagged under the spec's rule. Most peaks sit at L0–L3, where a
  last-token state is close to the embedding of that token. At L0, 106 of the
  200 poem−bhavam differences are exactly zero, because the poem and its
  bhavam end in the same token. These early peaks therefore cannot be read as
  metre.
- **The pipeline's 0.5–0.65 is not reproduced.** Without `<bos>`, the coarse
  contrast matches the pipeline (0.310 at L4, against 0.322), but kandamu vs
  mattakokila stays at 0.016–0.055. Two other plausible definitions fall short
  too: poem states without bhavam subtraction give 0.03–0.11, and each `c_k`'s
  cosine to the pair direction gives 0.25–0.32. The pipeline must have
  computed pair coherence another way, which its code would settle.
- **Consequence for EXP-23.** With this definition, its primary run (steering
  with a chandas-vs-chandas direction) has no coherent direction to use.

## Replication notes
- **The poem-vs-bhavam contrast confounds metre with register.** EXP-07 shows
  register is trivially separable by L7, so this contrast recovers register,
  not chandas. Prefer a chandas-vs-chandas or tight direction for steering
  (EXP-23).
- **mattakokila is the least stable metre.** It has only 41 eligible records in
  the whole corpus, so its 25-poem sample is near the floor. Report n per metre.
- **Rerun with `<bos>`** (EXP-35) and confirm the existing pair's 0.5–0.65
  before extending to all 28.

## Artifacts
`pipeline/data/phase4_chandas_direction.json` (chandohasam repo)
- Rerun with `<bos>` (2026-09-29): `experiments/exp22/2026-09-29_pairs/` (`directions.npz`,
  `coherence_by_layer.csv`, `summary.json`, `fig_coherence.png`); no-`<bos>` diagnostic:
  `experiments/exp22/2026-09-29_pairs_nobos/`; script `experiments/scripts/exp22_directions.py`.
  The pooled activations (`pooled_*.npy`, 42 MB each) are not committed; `exp22_directions.py extract`
  rebuilds them

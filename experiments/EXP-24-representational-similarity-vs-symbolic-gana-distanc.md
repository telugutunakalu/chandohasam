# EXP-24 — Representational similarity vs symbolic gana distance

| | |
|---|---|
| **Category** | G. Steering |
| **Origin** | chandohasam (G7 / NH20, §7) |
| **Depends on** | EXP-22's diff-in-means construction only (its per-metre vectors also feed EXP-22's all-pairs step) |
| **Status** | done (base model); NH20 holds; **rerun with `<bos>`** (2026-09-29): NH20 holds more strongly |
| **Cost** | minutes |

## Question
Does the geometry of per-metre activation differences mirror the symbolic
distance between metres?

## Why it matters
It is a strong test of genuinely metrical representation. If the model encoded
only "poeticness", per-metre directions would cluster without reflecting gaṇa
structure.

This is Representational Similarity Analysis (Kriegeskorte, Mur & Bandettini,
2008).

## Methodology
1. **Per-metre direction.** For each of the 8 balanced-sample metres (25 poems
   each) and each layer, pair every poem with its own bhavam:
   `d_c^(l) = mean_{i∈c} h_l(poem_i) − mean_{i∈c} h_l(bhavam_i)`, using
   last-real-token pooling.
   - Pairing within a poem cancels that poem's topic.
   - It does *not* cancel register shared by all verse; step 3 handles that.
2. **`D_struct`.** Pairwise Levenshtein distance between canonical guru/laghu
   pattern strings: one 8×8 matrix, computed once. For the variable-gaṇa
   metres (kandamu, tetagiti, aataveladi) the "canonical" pattern is the
   plurality-mode pattern in the corpus.
3. **`D_act` per layer**: `1 − cos(d_i, d_j)`, both
   - **raw**, and
   - **centred**: `d_c' = d_c − mean_c d_c`, which removes the shared verse
     offset.
4. **Statistic.** The Spearman correlation between the 28 upper-triangle
   entries of `D_struct` and `D_act`. Significance comes from a **999-permutation
   Mantel test**, permuting the metre labels; the entries of a distance matrix
   are not independent observations.
5. **Output.** `r` and `p`, for raw and centred, at each of the 36 layers.

## Inputs
Pooled per-layer activations for poem and bhavam; gaṇa pattern strings; the
balanced per-metre sample.

## Metrics
- Spearman r and Mantel p, raw and centred, per layer.
- The number of significant layers.
- The raw-minus-centred gap, a diagnostic for how much the shared offset
  dominates.

## Expected result / baseline
NH20: the correlation survives once the shared poem-vs-bhavam component is
removed.

## Observed
**NH20 holds, robustly.**
- The raw correlation is significant (p < 0.05) at **26 of 36 layers**, peaking
  at **L8 (r = 0.617, p = 0.005)**.
- L0 shows no relationship (r = −0.071, p = 0.733), consistent with L0 being
  the embedding lookup (EXP-05).
- Centring **sharpens** the signal at L7–L15, peaking at L8 (r = 0.702,
  p = 0.004), as predicted.
- Centring **reverses in late layers**. At L33 the raw correlation is still
  significant (r = 0.500, p = 0.007), but the centred one collapses (r = 0.123,
  p = 0.517). The centred r is negative at L23, L24 and L27–29.

In late layers, the across-metre mean direction carries chandas-relevant
information rather than only diluting it. The "shared poeticness offset" story
holds only for the early-to-mid layers.

| layer | r, raw | p, raw | r, centred | p, centred |
|---|---|---|---|---|
| L0 | −0.071 | 0.733 | 0.028 | 0.911 |
| L7 | 0.432 | 0.017 | 0.554 | 0.007 |
| **L8** | **0.617** | **0.005** | **0.702** | **0.004** |
| L9 | 0.519 | 0.010 | 0.536 | 0.016 |
| L15 | 0.485 | 0.007 | 0.433 | 0.031 |
| L33 | 0.500 | 0.007 | 0.123 (n.s.) | 0.517 |


**Rerun with `<bos>` (2026-09-29).** `experiments/scripts/exp24_rsa.py`, on EXP-22's
last-token states (25 poems per metre).
- `D_struct` is the Levenshtein distance between canonical U/I strings. The
  canonical string of every metre is the plurality-mode whole-poem pattern
  over all its eligible corpus poems.
- For the five vṛttas, this mode covers 43–56% of poems. For kandamu,
  aataveladi and tetagiti it covers only 0.10–0.35%, so it is nearly
  arbitrary. A sensitivity variant therefore concatenates the mode of each pāda
  position.
- Mantel tests: one-sided, 999 permutations.

| layer | r, raw | p, raw | r, centred | p, centred |
|---|---|---|---|---|
| L0 | 0.217 | 0.149 | 0.160 | 0.190 |
| L7 | 0.584 | 0.008 | 0.711 | 0.001 |
| **L8** | **0.630** | **0.006** | **0.728** | **0.002** |
| L10 (centred peak) | 0.601 | 0.006 | **0.745** | **0.001** |
| L16 (raw peak) | **0.773** | **0.002** | 0.677 | 0.007 |
| L33 | 0.609 | 0.008 | 0.578 | 0.007 |

- **NH20 holds, more strongly than before.** The raw correlation is
  significant at **34 of 36** layers (the pipeline found 26), and the centred
  one at 33. L8 reproduces the pipeline's peak (0.630 / 0.728, against
  0.617 / 0.702). L0 again shows no relationship.
- **The late-layer centred collapse does not replicate.** At L33 the centred
  r is 0.578 (p = 0.007), against the pipeline's 0.123. That pattern was
  probably an effect of the missing `<bos>`.
- **Sensitivity.** With per-pāda modes, 31 of 36 layers are significant raw
  and centred, and L8 gives 0.618 / 0.723. The conclusion does not depend on
  the choice of canonical pattern.

## Replication notes
- **Needs a metre-balanced sample** with enough examples per metre. With
  unequal counts, the distances are dominated by sample size.
- **Report raw and centred side by side.** They diverge in late layers, and
  either one alone misleads.
- **The canonical pattern of a variable metre is a choice.** Record it (the
  `gana_patterns` key) and test sensitivity to it.
- **Rerun with `<bos>`** if the pipeline's forward passes omitted it (EXP-35).
  The L8 peak should survive if it is real.

## Artifacts
- `pipeline/data/phase7_rsa.json`, `pipeline/common/phase7_rsa.py` and
  `pipeline/scripts/run_phase7.py` (chandohasam repo)
- Figure 5 in `Chandohasam_Gemma_Experiments.docx`
- Rerun with `<bos>` (2026-09-29): `experiments/exp24/2026-09-29_bos/summary.json` (both variants, every layer);
  script `experiments/scripts/exp24_rsa.py`

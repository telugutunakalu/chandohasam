# EXP-21 — Poem–bhavam layer alignment heatmap

| | |
|---|---|
| **Category** | F. Generation mechanics |
| **Origin** | chandohasam (G3, G3b / NH13, NH24) |
| **Depends on** | EXP-07 |
| **Status** | **closed**: full-token version done (base model); content-only variant (G3b) not pursued |
| **Cost** | minutes |

## Question
At which layer do a poem and its prose meaning align most, and at which do they
diverge most?

## Why it matters
It locates where the model separates form from content, which is the natural
place to look for, and to inject, a chandas direction.

## Methodology
1. **Token states.** For each of the 200 balanced-sample pairs, run the poem
   (joined pādas) and the bhavam (truncated to 2,000 characters) through
   separate forward passes with `output_hidden_states=True`. **Keep every
   token's vector**; do not pool.
2. **BERTScore per poem and layer.** L2-normalise every token vector and build
   the `n_poem × n_bhavam` cosine matrix. Then:
   - **precision** = the mean over poem tokens of each token's best bhavam match;
   - **recall** = the mean over bhavam tokens of each token's best poem match;
   - **F1** = their harmonic mean.
3. **Output.** A 200 (poems) × 36 (layers) F1 matrix, one value per cell with no
   further averaging. Identify the layers of peak alignment and peak
   divergence.
4. **Content-only variant (G3b).** Repeat after removing function words,
   particles and case markers (vibhakti) from both sides, and keep everything
   else identical. Function-word overlap inflates similarity uniformly.

## Inputs
(poem, bhavam) pairs; per-layer token representations; a content-word or
stopword filter.

## Metrics
- Per-layer P/R/F1.
- The peak-alignment and peak-divergence layers.
- The full-token and content-only curves compared: monotone or noisy, and
  whether a single peak or divergence layer emerges.

## Expected result / baseline
- NH13: peak divergence coincides with the layer where the chandas direction is
  most coherent (EXP-22).
- NH24: the content-only heatmap is cleaner and more monotone.

## Observed
**Full-token version**, base `gemma-4-E2B-it`, 200 poems:
- F1 is high almost everywhere (0.6–0.96).
- The exception is **L0, the raw embedding output, at 0.518**, the weakest
  layer.
- Peaks at L1 (0.957), L19 (0.950) and L29 (0.956). The curve is noisy, not a
  clean single peak.

L0 is the *strongest* layer for guru/laghu (EXP-05) and the *weakest* for
poem–bhavam alignment. That fits L0 carrying raw token identity only: semantic
alignment across texts needs at least one layer of contextual integration.

The high plateau is also consistent with shared surface vocabulary between a
poem and its own bhavam, which is what G3b tests. The sample raw matrices were
lost to a stale Modal volume and have not been regenerated.

## Why it is closed (2026-09-24)
The heatmap's purpose was choosing a layer for the chandas direction. That is
no longer needed: EXP-22 and EXP-24 sweep all 36 layers directly, and EXP-24
found its L8 peak without the heatmap. The content-only variant (G3b / NH24)
would only clean up a curve nothing downstream depends on, so it is not
pursued. NH13 can still be checked from EXP-22's coherence curve against the
F1 values above, without a new run.

## Replication notes
- **Function-word overlap is a large, uniform confound.** If this is ever
  reopened, run the content-only variant before drawing conclusions from the
  curve's shape.
- **Persist a few raw similarity matrices** per run for the heatmap figure.
  Summary F1 alone cannot be re-plotted as a heatmap.
- **Same `<bos>` caveat as EXP-05**, if the pipeline's passes omitted it.

## Artifacts
- `pipeline/data/phase3_heatmap_summary.jsonl` (chandohasam repo)
- Figure 4 in `Chandohasam_Gemma_Experiments.docx`

# EXP-21 — Poem–bhavam layer alignment heatmap

| | |
|---|---|
| **Category** | F. Generation mechanics |
| **Origin** | chandohasam (G3, G3b / NH13, NH24) |
| **Depends on** | EXP-07 |
| **Status** | done (base model) |
| **Cost** | minutes |

## Question
At which layer do a poem and its prose meaning align most, and diverge most?

## Why it matters
Locates where the model separates form from content — the natural place to look for, and to inject, a chandas direction.

## Methodology
1. Compute per-layer cosine-similarity matrices between poem and bhavam token representations.
2. Report BERTScore-style precision/recall/F1 per layer; identify peak alignment and peak divergence.
3. Repeat restricted to **content words only**, since function-word overlap inflates similarity uniformly and flattens the curve.

## Inputs
(poem, bhavam) pairs; per-layer token representations; a content-word filter.

## Metrics
Per-layer P/R/F1; peak-alignment and peak-divergence layers; full-token vs content-only curves.

## Expected result / baseline
NH13: peak divergence coincides with the layer where the chandas direction is most coherent (EXP-22). NH24: the content-only heatmap is cleaner and more monotonic.

## Observed
Full-token version run on the base model. Content-only variant (G3b) not yet run.

## Replication notes
Run the content-only variant before drawing conclusions — function-word overlap is a large uniform confound.

## Artifacts
chandohasam `pipeline/`

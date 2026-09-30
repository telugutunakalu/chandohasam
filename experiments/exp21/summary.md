# EXP-21: poem–bhavam layer alignment heatmap — summary

Full specification: [`../EXP-21-poem-bhavam-layer-alignment-heatmap.md`](../EXP-21-poem-bhavam-layer-alignment-heatmap.md).
**Status:** closed. The full-token version was done in the earlier pipeline; the content-only variant was
not pursued. It has not been rerun with `<bos>`.

## Question
At which layer do a poem and its prose meaning (bhavam) align most, and at which do they diverge most?

## Method
- `gemma-4-E2B-it`, 200 balanced-sample pairs, every token's hidden state at every layer.
- Per poem and layer: BERTScore-style F1 between the poem's and the bhavam's token vectors (best-match
  cosine in each direction).

## Findings (pipeline run, without `<bos>`)
- F1 is high almost everywhere (0.6–0.96).
- The exception is **L0, the embedding output, at 0.518**.
- Peaks at L1 (0.957), L19 (0.950) and L29 (0.956). The curve is noisy, with no single peak.
- L0 is the strongest layer for guru/laghu (EXP-05) and the weakest for poem–bhavam alignment, which fits
  L0 carrying token identity only.
- The high plateau may partly reflect vocabulary that a poem shares with its own bhavam.

## Why it is closed
The heatmap was meant for choosing a layer for the chandas direction. EXP-22 and EXP-24 now sweep all 36
layers directly, so nothing downstream depends on it.

## Evidence
The numbers are the pipeline's, as reported in the spec. That run lacked `<bos>` (see EXP-35), so treat its
curve shape as provisional. Its data (`pipeline/data/phase3_heatmap_summary.jsonl`) is in the chandohasam
repository, not here, and the raw similarity matrices were lost.

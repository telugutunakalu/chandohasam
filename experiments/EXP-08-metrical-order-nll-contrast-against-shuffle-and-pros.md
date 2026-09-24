# EXP-08 — Metrical-order NLL contrast against shuffle and prose controls

| | |
|---|---|
| **Category** | B. Representation probes |
| **Origin** | chandohasam (G1 NLL contrast, G1c / NH23, G1d formerly EXP-36) |
| **Depends on** | EXP-07; gated by EXP-35's sanity gates |
| **Status** | partial: shuffle contrast and shared-difficulty check run (suspect input); prose control TBD |
| **Cost** | minutes |

## Question
Does the model assign lower loss to genuine metrical word order than to
reorderings of the same words?

## Why it matters
It is a direct test of implicit metrical sensitivity that needs no probe. If
genuine order scores *worse* than a shuffle, the model actively disprefers
metrical arrangement, which would explain a great deal of downstream failure.

## Methodology
1. **Conditions per poem**, all sharing the poem's own words:
   - **genuine**: the joined pādas;
   - **random shuffle**: `random.shuffle` of the poem's own words, fixed
     seed;
   - **natural-prose reordering**: a canonical SOV-leaning order, produced by
     rule or by an LLM prompted to "reorder into natural prose word order,
     changing nothing else". Verify the word multiset is unchanged.
2. **Score** the teacher-forced NLL of each condition,
   `-mean_t log p(x_t | x_<t)`, with EXP-35's scorer and inputs (`<bos>`
   prepended, NFC-normalised text). The genuine condition is then EXP-35's
   `s_true` trace. Keep per-position values, not just the mean.
3. **Report** deltas per example and aggregated, and win rates for each pair of
   conditions.
4. **Shared per-poem difficulty** (formerly EXP-36).
   - Rank poems by ascending `NLL(genuine)`, plot it as a monotone line, and
     overlay each control's NLL at the same x.
   - Colour each point by the preferred condition.
   - Report the Pearson and Spearman correlations across poems; poems are
     independent, so ordinary p-values are valid.

   A positive correlation means both conditions share a per-poem difficulty
   factor (vocabulary rarity, tokenisation cost). Interpret the deltas in step
   3 only after accounting for it: report them alongside the correlation, not
   alone.

## Inputs
Poems; a shuffle generator; a prose-reordering procedure; EXP-35's scorer.

## Metrics
- `NLL(genuine) − NLL(shuffle)` and `NLL(genuine) − NLL(prose-order)`.
- Mean, median, and pairwise win rates across the three conditions.
- Pearson and Spearman correlation between the genuine and control NLL across
  poems.

## Expected result / baseline
NH23: genuine metrical order scores **worse** than both controls. The prose
control is the load-bearing one: beating only a random shuffle proves nothing
beyond fluency.

## Observed
**Shuffle contrast only**, base `gemma-4-E2B-it`, 200 balanced poems:
- mean `NLL(genuine) − NLL(shuffle)` = **+0.571** nats;
- the model preferred the shuffle in **144 of 200** poems (72%).

**Shared difficulty** (Figure 2b): genuine and shuffled NLL are strongly
correlated:
- Pearson r = **0.556** (p = 1.4×10⁻¹⁷)
- Spearman ρ = 0.503 (p = 3.4×10⁻¹⁴)

Genuine-preferred poems cluster at both extremes of the sorted range, and
shuffle-preferred poems dominate the middle; this is not yet explained. The
prose-reordering condition has not been run.

**Suspect input:** these NLLs come from the pipeline's `_nll()`. Its per-token
re-derivation in EXP-35 averages 13.15 nats, above the uniform bound ln V =
12.48, most likely because `<bos>` was missing. Do not interpret the 72%, or
the correlation, until the run is repeated behind EXP-35's gates.

## Replication notes
- **Include the prose-reordering control.** A shuffle alone is too weak a
  baseline to support any conclusion.
- **Run EXP-35's gates 2 and 3 first.** A model that does worse than uniform on
  every text cannot rank word orders meaningfully.
- **Report the correlation, not just the sorted plot.**
- **Follow-up:** explain the extremes-vs-middle pattern, for example by poem
  length or by metre.

## Artifacts
- `pipeline/data/phase1_nll_contrast.jsonl` (chandohasam repo)
- Figures 2 and 2b in `Chandohasam_Gemma_Experiments.docx`

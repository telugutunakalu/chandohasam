# EXP-08 — Metrical-order NLL contrast against shuffle and prose controls

| | |
|---|---|
| **Category** | B. Representation probes |
| **Origin** | chandohasam (G1 NLL contrast, G1c / NH23, G1d formerly EXP-36) |
| **Depends on** | EXP-07; gated by EXP-35's sanity gates |
| **Status** | partial: shuffle contrast and shared-difficulty check **rerun with `<bos>`** (2026-09-29, 200 poems); prose control TBD |
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

**Rerun with `<bos>`, 2026-09-29.** `experiments/scripts/exp08_order_contrast.py`,
EXP-35's scorer and inputs, and EXP-35's 200-poem balanced sample (seed 42). The
EXP-35 gates had passed on this scorer. The shuffle permutes the poem's own
words across the whole poem and puts them back into the lines, so each line
keeps its word count; only the order changes. The word multiset is checked.
NLL is the mean surprisal per scored token.

| | with `<bos>` (primary) | without `<bos>` (diagnostic) | pipeline |
|---|---|---|---|
| mean NLL, genuine / shuffle | 6.40 / 6.51 | 13.45 / 13.34 | — |
| mean `NLL(genuine) − NLL(shuffle)` | **−0.111** (95% CI −0.164 to −0.059) | +0.111 (CI −0.031 to +0.260) | +0.571 |
| median delta | −0.103 | +0.054 | — |
| shuffle preferred | **78 / 200** (39%) | 105 / 200 | 144 / 200 |
| Wilcoxon signed-rank p | **2.6×10⁻⁴** | 0.25 | — |
| Pearson r, genuine vs shuffle NLL | **0.766** (p = 8.5×10⁻⁴⁰) | 0.507 | 0.556 |
| Spearman ρ | 0.758 (p = 1.3×10⁻³⁸) | 0.485 | 0.503 |

- **With a valid input, the model prefers the genuine order.** It gives the
  genuine order a lower NLL in 122 of 200 poems, by 0.11 nats per token on
  average (about 1.7% of the mean NLL). The effect is significant but small.
  The pipeline's result (shuffle preferred in 72% of poems, +0.571) does not
  hold.
  - The same holds for total NLL per poem (mean difference −11.7 nats; shuffle
    lower in 70 of 200). Token counts differ between orders by −0.35 on average
    (range −5 to +5), because a word at a line start has no leading-space
    marker.
- **Without `<bos>`, the pipeline's numbers are not reproduced either** (105 of
  200, +0.11, not significant). The pipeline's sample ids and shuffle procedure
  are in the chandohasam repo, which is not available here, so the remaining
  difference cannot be traced.
- **Shared difficulty dominates.** Genuine and shuffled NLL correlate at
  r = 0.77, and the spread between poems (genuine NLL from 4.9 to 8.2) is much
  larger than the order effect. Deltas are reported together with this
  correlation, as step 4 asks.
- **The "extremes versus middle" pattern is a sorting artefact.** Sorted by
  genuine NLL, the shuffle is preferred in 14 of 67 poems in the lowest third
  and in 36 of 66 in the highest third. But the delta contains the genuine NLL
  itself, so sorting on it builds in this correlation (regression to the mean).
  Against the average of the two NLLs, the delta shows no trend (Spearman
  ρ = 0.007, p = 0.93; shuffle preferred in 21, 29 and 28 poems per third).
- **Per metre** (25 poems each; descriptive only), the genuine order is
  preferred most in tetagiti (−0.245), kandamu (−0.204), champakamala (−0.191)
  and utpalamala (−0.173), and hardly at all in mattebhavikriditamu (−0.002),
  mattakokila (+0.011) and aataveladi (−0.032).
- **Cross-check (EXP-35 gate 6).** For the 10 poems scored in EXP-35's gates
  run, `NLL(genuine)` equals EXP-35's mean `s_true` exactly, under both
  conditions (largest difference 0.0).

**NH23 is not supported by the shuffle contrast:** genuine order scores better,
not worse. The prose-reordering control, the load-bearing one, is still to run.

**Prose control, attempted with `gemma-4-E2B-it` (2026-09-29).**
`experiments/scripts/exp08_prose_control.py`.
- **Method.** The model was asked, with greedy decoding, to put each poem's
  words into natural prose order without changing any word. A reply was
  accepted only if its words were exactly the poem's words as a multiset.
- **Yield: 0 of 200 usable.** 83 replies repeated the poem in its original
  order, which passes the multiset check but is no reordering. The other 117
  changed, dropped or added words.
- **Consequence.** E2B cannot produce this control, and a stronger reorderer is
  needed: a larger model or a rule-based SOV reordering. The control is still
  outstanding. Artifacts: `experiments/exp08/2026-09-29_prose/`
  (`reorderings.jsonl`, `summary.json`).
A model that beats only a shuffle has shown fluency, not metrical sensitivity.

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
- Rerun with `<bos>` (2026-09-29): `experiments/exp08/2026-09-29_shuffle/` (`run.json`, `traces.jsonl`,
  `per_poem.csv`, `summary.json`, `fig_shared_difficulty.png`); script `experiments/scripts/exp08_order_contrast.py`

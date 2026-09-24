# EXP-18 — Multi-akshara span placement

| | |
|---|---|
| **Category** | E. Iteration and alphabet |
| **Origin** | ours (E11) |
| **Depends on** | EXP-11,14 |
| **Status** | done (negative) |
| **Cost** | ~1 h |

## Question
Does enlarging the admissible alphabet with multi-syllable tokens improve output?

## Why it matters
EXP-11 showed the alphabet is the suspected bottleneck. This tests that directly — multi-syllable tokens are morphemes, so words would arrive partly assembled rather than spelled out.

## Methodology
1. Admit tokens of m syllables, placed as spans occupying m canvas slots (first holds the token, rest hold padding that decodes to nothing).
2. Precompute per-token: internal weight pattern (fixed), final-syllable weight (depends on successor), and whether the onset closes the preceding syllable.
3. Propagate the pairwise coupling: a span whose final syllable is not intrinsically heavy imposes a requirement on the next token.
4. **Validate with random logits first** — that isolates mechanism from model behaviour.
5. Then run with the real model and measure how often spans are actually chosen.

## Inputs
Vocabulary with syllable segmentation; the constraint machinery.

## Metrics
Placeable inventory size; fraction of placements that are multi-syllable, under random logits and under the model; real-word rate.

## Expected result / baseline
A larger alphabet should raise lexicality — unless the model assigns little probability to the layout.

## Observed
Inventory 562 → **1,424**. Mechanically correct: 5/6 random-logit trials fully valid, real words appearing unprompted.

| driven by | multi-syllable placements |
|---|---|
| random logits | **39.4%** |
| DiffusionGemma | **6.8%** |

Real-word rate unchanged. The model declined to use the capability: placing a morpheme then padding the slots behind it is a layout it never saw in training.

## Replication notes
The random-logit control is what distinguishes 'the mechanism is broken' from 'the model won't use it'. Without it this reads as an implementation failure.

## Artifacts
`padyam/prosody/spans.py`, `scripts/gemma_span.py`, `experiments/gemma_v8_span.json`

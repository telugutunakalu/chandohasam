# EXP-13 — Metrical constraint on a large pretrained model

| | |
|---|---|
| **Category** | D. Constrained decoding |
| **Origin** | ours (E6) |
| **Depends on** | EXP-12 |
| **Status** | done |
| **Cost** | ~1 h incl. model load |

## Question
Does the constraint transfer to a model that actually knows the language?

## Why it matters
Tests whether form and meaning can be separated in practice: the sampler supplies form, the model supplies meaning.

## Methodology
1. Attach the constraint as a logits processor to the model's own sampling loop.
2. If the model is not absorbing-state diffusion, restate the constraint as a mean-field restriction: use the model's current argmax as the estimate of each position's neighbours.
3. Run free and constrained arms on the same prompts and seeds.
4. Score metre with the validator and lexicality with a corpus-lexicon word-membership rate.

## Inputs
A pretrained generative model; the constraint; a large word lexicon for the lexicality metric.

## Metrics
Valid lines and padyams; real-word rate; distinct-akshara ratio (repetition proxy).

## Expected result / baseline
Form should transfer. Watch lexicality closely — a hard constraint over a small admissible alphabet is trivially satisfied by repetition.

## Observed
Form transferred completely: **0/16 → 16/16 valid lines**. Content collapsed: real-word rate 55.7% → 15.9%, distinct-akshara ratio 15.9%, with lines 2–4 identical in three of four topics.

## Replication notes
Always pair a metrical metric with a lexicality and a repetition metric. Metrical validity alone will report success on degenerate output.

## Artifacts
`scripts/gemma_constrained.py`, `experiments/gemma_constrained_results.json`

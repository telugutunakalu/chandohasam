# EXP-31 — Bigram prior and in-beam neural rescoring

| | |
|---|---|
| **Category** | I. Composition |
| **Origin** | ours (E17) |
| **Depends on** | EXP-30 |
| **Status** | done (partial) |
| **Cost** | minutes |

## Question
Can better scoring turn metrically valid word sequences into sentences?

## Why it matters
EXP-30 guarantees form and lexicality; all remaining quality is the scoring function. This tests how far sequence-level scoring gets.

## Methodology
1. Replace the frequency prior with a word-**bigram** prior; penalise unattested pairings.
2. Score partial lines with a trained model inside the beam — mask a fraction of placed words and read the log-probability of the truth — rather than reranking finished candidates.
3. Restrict the lexicon to frequent words to suppress corpus-specific junk.
4. Penalise repetition within and across lines.
5. **Exempt the planner's content words from any frequency cap.**

## Inputs
Corpus bigram model; a trained scorer; planner content words.

## Metrics
Valid rate; planner words used; fragment count; qualitative syntactic judgement.

## Expected result / baseline
Sequence-level scoring should improve word order over frequency alone.

## Observed
Word LM: 942,965 unigrams, 183,421 bigrams. Planner-word usage across development: **0/20 → 10/24 → 20/29.**

Two bugs, both instructive: frequency capping deleted the planner's words entirely (0/20 until exempted); and restricting the lexicon fixed junk vocabulary but dropped content usage to 3/28 until the content bonus was raised. **Form, lexicality and relevance pull against one another** and the weights are the dial.

**Unsolved:** outputs remain well-formed word *sequences*, not sentences. A bigram cannot enforce agreement across a line.

## Replication notes
Expose the weights as flags — the balance is corpus-specific. Next step is span-level scoring inside the beam rather than a one-word window.

## Artifacts
`padyam/lattice.py::bigram_scorer`, `experiments/composer_tuned.log`

# EXP-32 — Corpus ingestion and quality audit

| | |
|---|---|
| **Category** | J. Data |
| **Origin** | ours (E18) |
| **Depends on** | EXP-01,04 |
| **Status** | done |
| **Cost** | ~1 min ingest |

## Question
What does the corpus contain, and at what quality bar should each part be used?

## Why it matters
Different downstream uses need different thresholds. Applying one bar to everything either discards most of the corpus or poisons the supervised targets.

## Methodology
1. Enumerate fields and coverage; do not assume the documented schema matches reality.
2. Emit separate artifacts at **different quality bars**: everything for pretraining, exact-metre only for supervised grid targets.
3. Verify the strict bar is severe rather than the corpus unreliable — compare whole-item exact match against per-position agreement.
4. Audit register: compare the vocabulary of the prose annotations against the verse.

## Inputs
The raw corpus; the EXP-01 engine; the EXP-04 validator.

## Metrics
Per-field coverage; counts at each quality bar; type-level vocabulary overlap between sub-corpora.

## Expected result / baseline
Annotation coverage is usually far below 100% and unevenly distributed.

## Observed
382,052 poems. **33,253** exact-metre grid padyams (previously 4,245 — 7.8×), **168,371** (meaning, poem) pairs, **767,226** glossed words with **351,991** sandhi decompositions, 70.0M pretraining tokens.

Strict matching is severe, not the corpus unreliable: of 25,637 correctly-shaped utpalamala, 15,480 match at all 80 positions — and 0.99⁸⁰ ≈ 45%, closely matching what is observed.

**Register finding:** only **12.8%** of prose-annotation vocabulary appears in the verse; 81,530 word types occur only in prose. A model trained on classical verse alone will write classical Telugu, not the contemporary register the project targets.

## Replication notes
Emit multiple artifacts at different bars from one pass. The register audit is cheap and changes what you include.

## Artifacts
`scripts/ingest_padyarchana.py`, `scripts/mine_padyams.py`

# EXP-01 — Prosody engine validation against gold annotation

| | |
|---|---|
| **Category** | A. Ground truth |
| **Origin** | ours (E1) |
| **Depends on** | — |
| **Status** | done |
| **Cost** | seconds, CPU |

## Question
Does rule-based akshara segmentation and laghu/guru scansion reproduce expert annotation?

## Why it matters
Every later experiment uses this as ground truth — as an RL reward, a rejection filter, an evaluation metric and a label source. If it is wrong, all four inherit the error. It must be validated before anything is built on it.

## Methodology
1. Load a gold corpus carrying per-akshara laghu/guru labels.
2. Segment each padyam with the rule engine; compare the akshara list against gold, element-wise.
3. On exactly-matching segmentations, compare the laghu/guru string position by position.
4. Tabulate the most frequent disagreements by (akshara, following akshara) so failures cluster into nameable rules rather than a single accuracy number.
5. Fix rules, re-run, repeat until disagreement is indistinguishable from annotation noise.

## Inputs
`BodduSriPavan111/chandassu` — 4,651 padyams with gold `lg_data`.

## Metrics
Segmentation exact-match rate (per padyam); laghu/guru accuracy (per akshara); fully-correct padyam rate.

## Expected result / baseline
Published baseline for the same task: 99.43% syllable counting, 93.82% gana sequence. A rule engine should beat this — the rules are closed and decidable.

## Observed
**99.87%** segmentation, **99.9984%** laghu/guru (5 errors in 320,159), 99.89% padyams perfect. Residual errors are malformed gold (OCR artefacts).

Four bugs found only by measurement: word-final pollu attachment; geminate `ఱ్ఱ` misread as ra-vattu; line breaks as cluster barriers (spaces are **not**); onset cluster hidden behind a trailing coda.

## Replication notes
Language-independent in structure. For another abugida, replace the akshara regex and the heavy/light rules; the measurement protocol is unchanged. Do not skip step 4 — the aggregate number hides which rule is wrong.

## Artifacts
`padyam/prosody/akshara.py`, `tests/test_prosody.py`

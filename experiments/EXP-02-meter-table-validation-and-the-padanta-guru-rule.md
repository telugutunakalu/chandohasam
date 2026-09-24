# EXP-02 — Meter table validation and the padanta-guru rule

| | |
|---|---|
| **Category** | A. Ground truth |
| **Origin** | ours (E2) |
| **Depends on** | EXP-01 |
| **Status** | done |
| **Cost** | seconds, CPU |

## Question
Do the tabulated gana sequences reproduce the observed scansion of real padyams?

## Why it matters
The meter table is what constrained decoding enforces. An error here silently produces confidently-wrong poems.

## Methodology
1. For each meter, build the required laghu/guru string from its gana sequence.
2. Scan every line of every gold padyam of that meter; compare to the required string.
3. Restrict to padyams a reference scanner certifies metrically perfect, isolating table error from source deviation.
4. Tabulate mismatches **by position** — systematic errors cluster at one index, noise does not.
5. Independently enumerate a variable-length meter's line grammar and check the count against a published figure.

## Inputs
Gold padyams grouped by labelled meter; an independent reference scanner for certification.

## Metrics
Per-position agreement; exact whole-line agreement; positional error histogram.

## Expected result / baseline
On certified-perfect padyams, a correct table should agree at ~100% of positions. Anything systematically lower indicates a wrong gana or a missing convention.

## Observed
**100.0% of positions** on certified padyams, all four vruttams. Dwipada enumeration produced exactly **432 strings**, matching the independent figure.

The positional histogram revealed **పాదాంత గురువు** — a line-final light syllable scans heavy — concentrated entirely at the last index and accounting for 13–17% of all line disagreements. Adding it moved exact agreement from 63–77% to 77–90%.

## Replication notes
Step 3 is essential: without certification you cannot distinguish a wrong table from a poet's licence. Step 4 is what surfaces missing conventions.

## Artifacts
`padyam/prosody/meters.py`

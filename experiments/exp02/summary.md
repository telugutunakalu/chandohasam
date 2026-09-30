# EXP-02: metre table validation and the padanta-guru rule — summary

Full specification: [`../EXP-02-meter-table-validation-and-the-padanta-guru-rule.md`](../EXP-02-meter-table-validation-and-the-padanta-guru-rule.md).
**Status:** done.

## Question
Do the tabulated gaṇa sequences reproduce the observed scansion of real padyams?

## Method
- Each metre's required laghu/guru string is built from its gaṇa sequence.
- Every line of every gold padyam of that metre is scanned and compared with it, restricted to padyams
  that a reference scanner certifies as metrically perfect.
- Mismatches are counted by position, and the line grammar of a variable-length metre (dvipada) is
  enumerated.

## Findings
- **100.0% of positions** agree on certified padyams, for all four vṛttas.
- The dvipada enumeration gives exactly **432 strings**, matching an independent count.
- The positional histogram found **పాదాంత గురువు**: a line-final light syllable scans heavy. It sits
  entirely at the last position and accounts for 13–17% of all line disagreements. Adding the rule
  raised exact line agreement from 63–77% to 77–90%.

## Evidence
The numbers are as reported in the spec. The metre table (`padyam/prosody/meters.py`) is not in this
repository, and there are no result files for this experiment.

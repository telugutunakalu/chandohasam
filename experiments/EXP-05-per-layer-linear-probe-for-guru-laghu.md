# EXP-05 — Per-layer linear probe for guru/laghu

| | |
|---|---|
| **Category** | B. Representation probes |
| **Origin** | chandohasam (G1 / NH11; G1b / NH22, formerly EXP-06) |
| **Depends on** | EXP-01 |
| **Status** | probe **rerun with `<bos>`** and **lookup control done** (2026-09-29): no layer beats the lookup |
| **Cost** | minutes, 1 forward pass per example; the lookup control needs no forward pass |

## Question
At which layer, if any, is syllable weight linearly decodable from hidden
states? And does any layer recover the part of weight that a token lookup
*cannot* see?

## Why it matters
Metre is a property of syllable weight. If the model does not represent weight,
no prompting or constraint can make it obey metre. This is the
representational precondition for everything else.

A probe can succeed by looking a token up rather than by computing anything.
Only the lookup control (steps 5–7) separates the two.

## Methodology
**Probe**
1. **Sample.** Draw a **metre-balanced** sample: a fixed N poems per metre, and
   drop metres with too few examples rather than padding them.
2. **Forward pass.** Run each pāda with `output_hidden_states=True`, with no
   chat template, and with `<bos>` prepended (see the replication notes).
   Cache the per-layer, per-token states.
   - Layer indexing is the HF `hidden_states[n]` convention: **`L0` is the
     embedding output, before any decoder layer**, and `L1`–`L35` are the
     outputs of the 35 decoder layers of `gemma-4-E2B-it`.
3. **Labels.** Map each token to its akshara with
   `akshara_align.align_tokens_to_aksharas` and label it guru (`U`) or laghu
   (`I`) with the EXP-01 engine. Exclude tokens without a clean akshara span;
   do not guess their labels.
4. **Probe.** Train one logistic-regression probe per layer (scikit-learn,
   `max_iter=1000`) with 5-fold stratified cross-validation. The value per
   layer is the mean accuracy over the folds.

**Lookup control** (formerly EXP-06)

The original control probed the raw embedding table. It is answered by
construction: `L0` is `hidden_states[0]`, so an L0 vector is the token's
embedding-table row up to Gemma's fixed embedding scale (check this in the
model code). The L0 signal is a lookup by definition, which confirms NH22.

The useful control asks whether any *later* layer adds what a lookup cannot.

5. **Split** the labelled aksharas by the EXP-01 rule that fixes their weight
   (`Syllable.rules`):
   - **self-determined**: long vowel sign, anusvara, visarga, pollu. The
     token's own characters decide the weight.
   - **context-determined**: guru because a conjunct follows. The weight
     depends on the *next* akshara, which is usually in the next token.
6. **Rule baselines.**
   - **A (lookup):** predict weight from the token's own characters only. This
     is the ceiling for any context-free reader.
   - **B (next-akshara oracle):** baseline A plus the following akshara's
     conjunct status.
7. **Report per-layer accuracy on each subset**, from the step-4 probes and
   folds, alongside both baselines and each subset's size.

## Inputs
Balanced poem sample; hidden states at every layer; gold weight labels and rule
traces from EXP-01.

## Metrics
- Probe accuracy per layer, and the layer of peak decodability.
- The majority-class (guru share) rate, reported alongside as the chance level.
- Accuracy per layer on the self-determined and context-determined subsets,
  against baselines A and B.

## Expected result / baseline
- NH11 predicts weight is *not* decodable early and becomes decodable
  mid-network. A fine-tuned prosody checkpoint should show it earlier.
- For the lookup control: L0 ≈ baseline A on both subsets.
  - A layer that *represents* weight must beat baseline A **on the
    context-determined subset**, because only integration of the following
    token can do that.
  - If no layer does, weight is looked up and never computed, which fits
    EXP-09's behavioural failure.

## Observed
**Contradicts NH11's framing.** On `google/gemma-4-E2B-it`: **6,696 labelled
token examples per layer**, from the first 300 pādas encountered, across 36
layer indices. (An earlier version of this file said "n=300 aksharas"; 300 is
the pāda count.)

| layer | accuracy |
|---|---|
| **L0 (embeddings)** | **0.796**, the highest of any layer |
| L7 | 0.667 |
| L10 (trough) | 0.644 |
| L27 (late plateau) | 0.735 |

The curve dips through L6–L11 (about 0.64–0.66) and partially recovers by
L24–29 (about 0.73–0.74), never regaining L0's level. The fine-tuned comparison
was not run: no METRICALARGS checkpoint exists in either repo.

L0 is the raw embedding output, so the peak is a token-identity signal, not
integration.

The lookup control (steps 5–7) has not been run.


**Rerun with `<bos>`, and the lookup control (2026-09-29).**
`experiments/scripts/exp05_probe.py`.
- **Sample.** The first 10 poems of each metre in EXP-35's balanced sample:
  80 poems, 320 pādas, one forward pass per pāda.
- **Tokens.** 7,172 tokens; **6,102** have a clean span inside a single
  akshara. 839 cover several aksharas and 231 cover none; both are left out.
- **Labels.** Scanner weights, canonical reading: 42.8% guru, majority-class
  rate 57.2%.
- **Probes.** scikit-learn 1.9, default settings, `max_iter=1000`. Some layers
  hit the iteration cap (up to 5 warnings over the 5 folds).

| | all | self-determined (2,164) | context-determined (3,938) |
|---|---|---|---|
| guru share | 42.8% | 100% | 11.4% |
| baseline A (lookup) | **0.927** | 1.000 | **0.887** |
| baseline B (A + next akshara's conjunct) | 0.994 | 1.000 | 0.991 |
| probe L0 (best layer) | **0.777** | 0.648 | **0.847** |
| probe L18 (trough) | 0.655 | 0.619 | 0.675 |
| probe L25 (late plateau) | 0.749 | 0.748 | 0.750 |

- **The curve's shape survives `<bos>`.** L0 is highest (0.777, against the
  pipeline's 0.796). Accuracy then dips twice: to 0.662 at L9, back up to
  0.751 at L14, and down to 0.655 at L18. From L24 on it stays at
  0.71–0.75. The mid-layer dip is not an input artifact.
- **The lookup control is decisive.** No layer beats baseline A on the
  context-determined subset. The best is 0.847 at L0, below the subset's own
  majority rate of 0.887, while the next-akshara oracle reaches 0.991. No
  layer reaches baseline A overall either.
- By the spec's criterion, weight is looked up, not computed, which matches
  EXP-09's behavioural failure. EXP-20's unpark condition (a layer that beats
  the lookup on context-determined weights) is not met.

## Replication notes
- **Balanced sampling matters.** A sequential prefix of the skandha-ordered
  corpus covers only 9 of about 27 metres and confounds metre with era.
- **Report the chance level.** Without the majority-class rate, the 0.64 trough
  cannot be read.
- **Run the lookup control before interpreting any L0 result on any model.**
  For abugidas the lookup account is strong a priori, because the script
  writes vowel length explicitly.
- **`<bos>` caveat.** The pipeline ran the probe with "no chat template, no
  special tokens". The Gemma-4-E2B-it tokenizer does not add `<bos>` in any
  case (EXP-35).
  - L0 involves no attention, so it is the one layer a missing `<bos>` cannot
    affect.
  - The mid-layer trough could therefore be partly an input artifact. Rerun
    with `<bos>` before interpreting the curve's shape or running the lookup
    control.

## Artifacts
`pipeline/data/phase1_guru_laghu_probe.json` (chandohasam repo)
- Rerun with `<bos>` + lookup control (2026-09-29): `experiments/exp05/2026-09-29_probe/` (`labels.jsonl`,
  `summary.json`, `run.json`; `states.npy` is 675 MB and is not committed; `exp05_probe.py` rebuilds it); script
  `experiments/scripts/exp05_probe.py`

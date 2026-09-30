# EXP-19 — Generation-time tracking

| | |
|---|---|
| **Category** | F. Generation mechanics |
| **Origin** | chandohasam (G2 / NH12; G2b / NH25, formerly EXP-37; G6a / NH16, formerly EXP-40) |
| **Depends on** | EXP-09; EXP-22 for the decay curve |
| **Status** | **rerun 2026-09-29** (`<bos>` via chat template, plain-text output): generation, regression and decay curve done; NH12 not supported |
| **Cost** | minutes per sample; the analyses are seconds on the existing traces |

## Question
What distinguishes generation steps that violate the metre from those that do
not? Does drift build up smoothly with length, or is it triggered at specific
structural points?

## Why it matters
It moves from "the model fails" to "it fails here, for this reason". The two
drift shapes call for different fixes:
- **smooth decay** points to representational fading, and the fix is a
  positional steering boost;
- **sharp drops at pāda boundaries or sandhi junctions** point to a trigger,
  and the fix is a targeted controller.

## Methodology
**Generation**
1. **Generate** (bhavam → poem) completions for the 200-poem balanced sample.
   - The prompt is chat-template-wrapped, with the full structural rules and
     reference data, and asks for a JSON answer (`poem`,
     `chandassu_analysis`, meaning).
   - Decoding is a **manual greedy loop**, `next = argmax(raw logits)`, not
     `model.generate()` and not sampling, with `max_new_tokens = 1000`.
2. **Log per-step metrics**: the entropy `H_t` over the full 262,144-token
   vocabulary from raw logits, the top-k margin, the position, the per-step
   guru/laghu-satisfaction flag, and the distance to the nearest sandhi junction
   and pāda boundary.
   - For the decay curve, also log the cosine between the step's hidden state
     at the chosen layer and the chandas direction (EXP-22). The current traces
     do not store this.
3. **Score each output with the validator**: pass/fail plus violation
   locations.

**Content-only steps** (formerly EXP-37)

4. **Find the JSON preamble from the generated text itself**, not from the
   entropy values. Every poem opens with
   `` ```json\n{\n  "poem": [\n    " ``. In this run the preamble occupies steps
   0–12 for all 200 poems, and entropy is exactly 0 from step 3 on.
   - Detect the preamble per poem, structurally, rather than with a fixed global
     index, in case its length varies with metre or prompt.
5. **Segment by field.** Label each step with the JSON field it falls in, and
   aggregate per field. At each step, the mean covers only the poems still
   generating at that step; plot that count alongside. Every analysis below
   uses **`poem`-field steps only**.

**Regression and decay curve** (formerly EXP-40)

6. **Regression.** Fit a logistic regression of per-step violation on:
   - absolute position;
   - position in the pāda;
   - distance since the last sandhi junction;
   - local next-token entropy;
   - a rare-word flag (for example, the token's corpus frequency below a fixed
     percentile).

   Cluster standard errors by generation. The **null model is absolute position
   alone**; report each predictor's coefficient, p-value and drop in deviance
   over it.
7. **Decay curve.** Plot the step's cosine to the chandas direction against
   absolute step and against position in the pāda (akshara index), with pāda
   boundaries marked. Classify the shape as smooth decay or sharp, localised
   drops.

## Inputs
(bhavam, poem) pairs; a generation loop exposing per-step distributions and
hidden states; the validator; EXP-22's direction, for step 7.

## Metrics
- Run health: the truncation rate and the pāda-extraction rate.
- Content-region per-step mean entropy and per-field entropy.
- Regression coefficients, significance, and deviance over the position-only
  null.
- The decay-curve shape classification.

## Expected result / baseline
- **NH12**: violation correlates with entropy spikes and sandhi proximity
  **more than with position alone**.
- **NH16**: drift shows sharp drops at junctions and pāda boundaries rather than
  smooth decay.
- **NH25**: with the preamble excluded, entropy shows structure tied to position
  in the pāda.

## Observed
Base `gemma-4-E2B-it`, rerun 2026-09-24 with the 1,000-token budget.

**Run health**

| check | 600-token first pass | 1,000-token rerun |
|---|---|---|
| truncated generations | 24% | **5% (10/200)** |
| clean pāda extraction | 76% | **94% (189/200)** |

**Compliance.** **0 of 189** cleanly extracted poems match *any* known metre,
including their own target. The pādas are well-formed Telugu verse (spot
checked), but gaṇa, yati and prāsa never align together. The result survived
growing the clean sample from 152 to 189, so truncation does not explain it.

**Entropy, unfiltered.** The mean is 0.311 over 114,729 steps; the median is
**0.0106**. That is a bimodal mix dominated by the JSON preamble.

**Entropy, content only (`step ≥ 13`, Figure 3b)**:
- It rises sharply at step 13, where the content begins.
- It peaks near **step 30**, at a mean of about **0.79**.
- It declines through steps 300–400 and settles into a noisier band of about
  0.15–0.25.
- Beyond about step 500, fewer than 100 poems are still generating, so that
  region is small-n noise.

The shape follows the **JSON fields**: poem lines carry the real word-choice
uncertainty, and `chandassu_analysis` is templated prose
(`గణవిభజన: … యతి: … సరిపోతుంది. ప్రాస: …` for each pāda). **NH25 is partially
confirmed**: the curve has structure, but field type drives it, not pāda
position. The per-field segmentation (step 5) has not been done yet.

**Not yet run:**
- **NH12 and NH16:** the regression (step 6) can run on the existing traces.
- **The decay curve** (step 7) needs a rerun that logs hidden states.


**Rerun, 2026-09-29.** `experiments/scripts/exp19_generate.py`, then
`experiments/scripts/exp19_analyse.py`: `gemma-4-E2B-it`, EXP-35's 200-poem
sample.
- **Prompt.** The project's own rule-bearing prompt for each metre
  (`runs/2026-09-24_e4b_baseline/prompts.jsonl`), with the bhavam in place of
  the topic, in the chat template. Output is plain text (the four pādas), as
  the notes above recommend; the earlier run asked for JSON.
- **Decoding.** A manual greedy loop over the raw logits, with a KV cache and
  at most 1,000 tokens.
- **Operational choices the spec leaves open** (all recorded in
  `summary.json`):
  - per-step outcome: the 5 fixed-pattern metres only, clean poems;
  - template: the corpus's plurality pattern per pāda, i.e. the catalogue
    pattern;
  - pāda-final slot: free;
  - sandhi junction: a word boundary in the scanner's word index;
  - rare word: seen fewer than 10 times in the tokenised corpus;
  - standard errors: cluster-robust, by generation.

**Run health and compliance.** 0 of 200 generations are truncated (mean 70
tokens), and 172 give exactly 4 lines. **0 of 200 match any known metre**, and
0 are valid in their target metre under either profile, as in the earlier run
(0 of 189).

**Regression** (99 clean poems of the fixed metres, 6,542 steps). Continuous
predictors are standardised; p values come from cluster-robust z.

| predictor | all steps: coef (p) | within the template: coef (p) | deviance gain when added, within the template |
|---|---|---|---|
| absolute position (null) | +0.03 (0.35) | −0.02 (0.37) | 0.6 |
| position in the pāda | **+1.24 (10⁻²⁴)** | +0.08 (0.024) | 6.9 |
| aksharas since the last junction | −0.08 (0.011) | −0.03 (0.37) | 0.9 |
| next-token entropy | +0.01 (0.69) | +0.04 (0.19) | 1.8 |
| rare word | +0.48 (1.7×10⁻⁴) | **+0.57 (1.8×10⁻⁷)** | **22.8** |

- **All steps.** The violation rate is 58%. Position in the pāda dominates,
  but mostly by construction: an akshara beyond the template's length counts
  as a violation, and those come late in the line.
- **Within the template** (5,550 steps). The violation rate is **50.8%**, about
  what a coin toss would give. The full model gains only 36.4 deviance over the
  position-only null.
- **NH12 is not supported.** Neither entropy nor distance from a sandhi
  junction predicts a violation; the only clear predictor is a rare word.

**Decay curve (step 7).** Cosine of each step's state with EXP-22's coarse
direction (poem − bhavam) (`fig_exp19.png`):
- **No smooth decay.** The per-poem slope over steps is +0.017 per 100 steps at
  L6 and −0.001 at L35.
- **Sharp change at pāda starts.** At a pāda-initial step, the cosine drops by
  0.049 at L6 relative to other steps (p = 10⁻³¹), and rises by 0.275 at L35
  (p = 10⁻³⁴).
- **Caveat.** These steps are produced by the state that reads the newline, so
  the effect cannot be separated from the token type.
- **Orientation.** At L35 the generation states point *against* the poem side
  of the direction (cosine about −0.55), towards prose.

The NH16 classification is therefore "localised changes at pāda boundaries, no
smooth decay", with the token-type caveat. The direction used is the coarse
one, because EXP-22 found no coherent chandas-vs-chandas direction.

## Replication notes
- **Include raw position as an explicit competing predictor.** Otherwise any
  correlation with "later in the line" will pass for a linguistic finding.
- **Use a per-step outcome.** With 0/189 compliant, poem-level pass/fail has no
  variance, so use per-step guru/laghu satisfaction.
- **Look at the generated text before reading an entropy curve.** The zeros in
  steps 0–12 were the prompt's JSON instruction working as intended, not a
  confident model.
  - Entropy here comes from raw logits in a manual loop, not from
    `generate(output_scores=True)`, so a truncated sampling distribution cannot
    explain it.
- **A plain-text output format avoids the problem entirely.** The JSON schema
  front-loads zero-entropy tokens and mixes analysis prose into the trace.
- **Fix the sandhi-junction detection rule before running the regression**,
  from the scanner's word and akshara boundaries, and record it. It is NH12's
  key predictor.

## Artifacts
- `pipeline/data/phase2_generation_traces.jsonl` (chandohasam repo)
- Figures 3 and 3b in `Chandohasam_Gemma_Experiments.docx`
- Rerun (2026-09-29): `experiments/exp19/2026-09-29_generation/` (`generations.jsonl` with per-step logs,
  `validation.jsonl`, `summary.json`, `decay_by_step.csv`, `nh18_by_slot.csv`, `fig_exp19.png`); scripts
  `experiments/scripts/exp19_generate.py`, `experiments/scripts/exp19_analyse.py`

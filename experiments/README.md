# Experiment Register

One file per experiment, written as a **replication spec**: question,
methodology, metrics, expected result, and what was observed. The purpose is to
re-run the same experiments on a different model and get comparable numbers, so
each file states what must be held fixed and what legitimately varies.

Numbering is sequential and stable: a retired number is never reused (see
[Retired numbers](#retired-numbers)). Result artifacts (`*.json`, `*.log`) live
in this directory alongside the specs. Engineering and planning records that
are not model experiments live in [`notes/`](notes/).

## Sources consolidated

| source | active specs | character |
|---|---|---|
| this project (`docs/12-experiment-register.md`) | 19 | **system-building** — does it work, and can it be made to work |
| `chandohasam_gemma_experiments.md` (2026-09-24 revision: G1–G8, NH11–NH26) | 12 (2 parked) | **mechanistic interpretability** — where in the network, and why |

How the 2026-09-24 revision of that document maps onto the register:

| source item | spec |
|---|---|
| G1d (sorted NLL) | step 4 of EXP-08 |
| G1b (L0 lookup test) | lookup control in EXP-05 |
| G2b (entropy without boilerplate) | EXP-19 |
| G6a (decay curve and regression) | EXP-19 |
| G4b (synthetic tight contrast) | EXP-38 |
| G4c (all chandas-vs-chandas pairs) | EXP-22 |
| G6b (teacher-forced vs free running) | NH18 in EXP-35 |
| G6c (ablation) | EXP-20, parked |
| G6d (targeted steering) | EXP-41, parked |
| G8 (teacher-forced surprisal) | EXP-35 |

The two sources are largely complementary. Four genuine overlaps were merged
rather than duplicated:

| overlap | this project | chandohasam | resolution |
|---|---|---|---|
| does the model represent syllable weight? | EXP-09 behavioural (infill) | EXP-05 probing (per-layer) | both kept — they answer it at different levels and **disagree productively** |
| why does the model drift from metre? | EXP-16, EXP-17 behavioural | EXP-19 mechanistic (EXP-20 parked) | both kept, cross-referenced |
| teacher-forced vs free generation | EXP-09 (restoration vs composition) | EXP-35 (surprisal gap + NH18) | for Gemma, EXP-09 already shows failure under the true context; EXP-35 quantifies it per slot |
| deterministic prosody validator | EXP-01–04 (this engine) | "Phase 7" in that document | **one engine** — `padyam/prosody/` serves both |

The most interesting overlap is the first. Probing finds guru/laghu is linearly
decodable at **layer 0 with 0.796 accuracy**; the behavioural test finds the
same model preserves line length **0.0%** of the time at 25% blanking. Both are
correct. A surface signal exists and does not drive generation.

The source document has since confirmed that L0 *is* the embedding output, so
the L0 signal is a lookup by definition. EXP-05's lookup control asks the
remaining question: does any later layer recover the part of weight that a
lookup cannot see? Run it before any layer-0 result is interpreted.

## Known input issue: `<bos>` (2026-09-24)

The chandohasam pipeline's Section 8 run (EXP-35) reports a mean true-token
surprisal of **13.15 nats**. That is above ln V = ln 262,144 = **12.48**, the
surprisal of a uniform guess: a model doing worse than chance on every poem,
while putting about 0.66 on its own argmax. That signature means a broken
input, not a finding about verse.

The leading explanation is a missing `<bos>`:
- the pipeline's probe methodology states "no special tokens";
- the `gemma-4-E2B-it` tokenizer under transformers 5.15 does not add `<bos>`
  anyway.

The same `_nll()` produced EXP-08's numbers. Every hidden-state experiment run
the same way (EXP-05, 07, 21, 22, 24) may also be affected; L0 is the
exception, since it involves no attention. Until reruns exist:
- treat EXP-08 and EXP-35 numbers as unvalidated;
- read the shapes of the EXP-05, 21 and 24 curves as provisional.

EXP-35 specifies sanity gates that catch this class of fault.

## Index

| # | Experiment | Category | Origin | Status |
|---|---|---|---|---|
| [01](EXP-01-prosody-engine-validation-against-gold-annotation.md) | Prosody engine validation | A. Ground truth | ours | done |
| [02](EXP-02-meter-table-validation-and-the-padanta-guru-rule.md) | Meter table + padanta-guru | A. Ground truth | ours | done |
| [03](EXP-03-yati-rule-selection-with-a-false-positive-control.md) | Yati rule selection | A. Ground truth | ours | done |
| [04](EXP-04-end-to-end-validator-accept-reject.md) | End-to-end validator | A. Ground truth | ours | done |
| [05](EXP-05-per-layer-linear-probe-for-guru-laghu.md) | Per-layer guru/laghu probe + lookup control | B. Probes | chandohasam | probe done (base) ⚠ no `<bos>`; lookup control TBD |
| [07](EXP-07-poem-vs-bhavam-register-probe.md) | Register probe | B. Probes | chandohasam | done (base) |
| [08](EXP-08-metrical-order-nll-contrast-against-shuffle-and-pros.md) | Metrical-order NLL contrast + shared difficulty | B. Probes | chandohasam | partial (shuffle only) ⚠ input |
| [09](EXP-09-infill-diagnostic-can-the-model-restore-blanked-syll.md) | **Infill diagnostic ★** | C. Capability | ours | done |
| [11](EXP-11-tokenizer-syllable-coverage-audit.md) | **Tokenizer coverage audit ★** | C. Capability | ours | done |
| [12](EXP-12-metrical-constraint-on-an-untrained-model.md) | Constraint, untrained model | D. Decoding | ours | done |
| [13](EXP-13-metrical-constraint-on-a-large-pretrained-model.md) | Constraint, pretrained model | D. Decoding | ours | done |
| [14](EXP-14-repetition-penalties-and-priority-ordered-constraint.md) | Penalties, relaxation order, rejection sampling | D. Decoding | ours | done |
| [16](EXP-16-constraint-annealing-canvas-warm-start-and-prompt-ri.md) | Annealing / warm-start / prompts | D. Decoding | ours | done (negative) |
| [17](EXP-17-recursive-context-expansion-across-iterations.md) | Recursive context expansion | E. Iteration | ours | done (saturates) |
| [18](EXP-18-multi-akshara-span-placement.md) | Multi-akshara spans | E. Iteration | ours | done (negative) |
| [19](EXP-19-generation-time-tracking.md) | Generation-time tracking, decay + regression | F. Mechanics | chandohasam | generated (base); regression + decay TBD |
| [20](EXP-20-causal-drift-analysis-by-component-ablation.md) | Causal drift ablation | F. Mechanics | chandohasam | **parked** |
| [21](EXP-21-poem-bhavam-layer-alignment-heatmap.md) | Poem–bhavam heatmap | F. Mechanics | chandohasam | **closed** (full-token only) |
| [22](EXP-22-chandas-direction-extraction-diff-in-means-caa.md) | Chandas direction extraction, all pairs | G. Steering | chandohasam | partial (coarse + 1/28 pairs) |
| [23](EXP-23-activation-steering-with-controls.md) | Activation steering | G. Steering | chandohasam | TBD (redesigned) |
| [24](EXP-24-representational-similarity-vs-symbolic-gana-distanc.md) | RSA vs gana distance | G. Steering | chandohasam | done (base) — NH20 holds |
| [25](EXP-25-akshara-aligned-tokenizer-construction-and-round-tri.md) | **Akshara tokenizer ★** | H. Training | ours | done |
| [26](EXP-26-realiser-training-and-the-infill-benchmark.md) | **Realiser training ★** | H. Training | ours | done |
| [27](EXP-27-realise-a-padyam-from-a-bag-of-words.md) | Realise from word bag | H. Training | ours | partial |
| [28](EXP-28-diffusion-objective-ablation-masked-vs-uniform-vs-co.md) | Objective ablation | H. Training | ours | done |
| [30](EXP-30-word-lattice-composition.md) | Word-lattice composition | I. Composition | ours | done |
| [31](EXP-31-bigram-prior-and-in-beam-neural-rescoring.md) | Bigram + in-beam rescoring | I. Composition | ours | partial |
| [32](EXP-32-corpus-ingestion-and-quality-audit.md) | Corpus ingestion + audit | J. Data | ours | done |
| [35](EXP-35-teacher-forced-surprisal-gap-corpus-token-vs-top-choice.md) | **Teacher-forced surprisal gap** | C. Capability | chandohasam | run once, **fails gate 2** — respecified |
| [38](EXP-38-synthetic-tight-contrast-set-for-a-metre-specific-direction.md) | Synthetic tight contrast | G. Steering | chandohasam | TBD |
| [41](EXP-41-targeted-threshold-triggered-steering.md) | Targeted steering | G. Steering | chandohasam | **parked** (future arm of EXP-23) |

## Retired numbers

Each of these was merged into the experiment whose data it used, or moved out of
the register. Its content now lives at the destination.

| # | was | now | reason |
|---|---|---|---|
| 06 | Embedding-lookup control | EXP-05 (lookup control) | L0 is the embedding output, so the original test holds by construction; the remaining control is an analysis of EXP-05's own probes |
| 10 | Teacher-forced vs free running | EXP-35 (NH18) | the teacher-forced side is EXP-35's `argmax` field and the free side is EXP-19's traces; for Gemma, EXP-09 already answers it |
| 15 | Rejection sampling | EXP-14 | validity is guaranteed by construction; attempts-to-valid is an EXP-14 metric |
| 29 | Throughput benchmark | [`notes/`](notes/training-throughput-benchmark.md) | a hardware benchmark, not a model experiment |
| 33 | Scaling sufficiency | [`notes/`](notes/scaling-sufficiency-analysis.md) | a planning calculation |
| 34 | Instruction dataset | [`notes/`](notes/multi-task-instruction-dataset-construction.md) | a dataset build |
| 36 | Sorted NLL / shared difficulty | EXP-08 (step 4) | one correlation on EXP-08's numbers |
| 37 | Entropy, boilerplate excluded | EXP-19 | a corrected aggregation of EXP-19's traces |
| 39 | All chandas-vs-chandas pairs | EXP-22 (step 4) | pair directions are `d_a − d_b` of EXP-24's per-metre vectors |
| 40 | Positional decay + regression | EXP-19 | its regression was EXP-19's own step 4 |

## Recommended order for a new model

**Cheap and decisive first.** These cost minutes and predict most of the rest:

1. **EXP-11** — tokenizer syllable coverage. No model forward pass; predicts
   EXP-09.
2. **EXP-09** — infill diagnostic. The single most informative experiment in
   the set.
3. **EXP-35 gates 2–5** on 5–10 poems (`<bos>`, no-`<bos>`, random weights) —
   verifies the model input before any NLL or hidden-state result is trusted.
4. **EXP-05 with its lookup control.** Never the probe alone.
5. **EXP-12** — constraint on random weights, to verify the harness before
   blaming any model.

Then, depending on what those show:
- coverage low and infill failing: the limit is representational, and
  EXP-25/26 is the path;
- coverage high and infill succeeding: go to EXP-27 and the composition track.

## Controls that changed a conclusion

Recorded because in each case the naive version of the experiment gave the
wrong answer:

| experiment | control | what it prevented |
|---|---|---|
| EXP-03 | random-pair acceptance rate | adopting a rule with 100% recall that accepts half of all random pairs |
| EXP-05 | lookup control (L0 = embedding output) | reading a layer-0 orthographic lookup as prosodic knowledge |
| EXP-08 | prose reordering, not just shuffle | concluding metrical sensitivity from a fluency effect |
| EXP-09 | corpus frequency baseline (~57%) | reading 60% as "above chance" |
| EXP-12 | random weights | attributing harness bugs to the model |
| EXP-18 | random logits | reading "the model won't use it" as "the mechanism is broken" |
| EXP-23 | random direction at matched norm | reading a perturbation-norm effect as a semantic one |
| EXP-24 | raw *and* centred `D_act` | reading the centred result alone, which collapses in late layers where the shared direction carries signal |
| EXP-25 | metrical round trip | training on targets that are silently 50% corrupt |
| EXP-28 | downstream task, not loss | ranking objectives by an incommensurable number |
| EXP-35 | uniform bound ln V = 12.48 (pending rerun) | reading a worse-than-uniform, broken-input result as "the model confidently expects something else" |

# Experiment Register

One file per experiment, written as a **replication spec**: question,
methodology, metrics, expected result, and what was observed. The purpose is to
re-run the same experiments on a different model and get comparable numbers, so
each file states what must be held fixed and what legitimately varies.

Numbering is sequential and stable. Result artifacts (`*.json`, `*.log`) live in
this directory alongside the specs.

## Sources consolidated

| source | contributes | character |
|---|---|---|
| this project (`docs/12-experiment-register.md`) | 22 experiments | **system-building** — does it work, and can it be made to work |
| `chandohasam_gemma_experiments.pdf` (G1–G7, NH11–NH24) | 12 experiments | **mechanistic interpretability** — where in the network, and why |

The two are largely complementary. Four genuine overlaps were merged rather
than duplicated:

| overlap | this project | chandohasam | resolution |
|---|---|---|---|
| does the model represent syllable weight? | EXP-09 behavioural (infill) | EXP-05 probing (per-layer) | both kept — they answer it at different levels and **disagree productively** |
| why does the model drift from metre? | EXP-16, EXP-17 behavioural | EXP-19, EXP-20 mechanistic | both kept, cross-referenced |
| teacher-forced vs free generation | EXP-09 (restoration vs composition) | EXP-10 (token-rank) | EXP-10 marked as depending on EXP-09 |
| deterministic prosody validator | EXP-01–04 (this engine) | "Phase 7" in that document | **one engine** — `padyam/prosody/` serves both |

The most interesting overlap is the first. Probing finds guru/laghu is linearly
decodable at **layer 0 with 0.796 accuracy**; the behavioural test finds the
same model preserves line length **0.0%** of the time at 25% blanking. Both are
correct. A surface signal exists and does not drive generation — which is
exactly what EXP-06 (embedding-table lookup control) is designed to adjudicate,
and why it should be run before any layer-0 result is interpreted.

## Index

| # | Experiment | Category | Origin | Status |
|---|---|---|---|---|
| [01](EXP-01-prosody-engine-validation-against-gold-annotation.md) | Prosody engine validation | A. Ground truth | ours | done |
| [02](EXP-02-meter-table-validation-and-the-padanta-guru-rule.md) | Meter table + padanta-guru | A. Ground truth | ours | done |
| [03](EXP-03-yati-rule-selection-with-a-false-positive-control.md) | Yati rule selection | A. Ground truth | ours | done |
| [04](EXP-04-end-to-end-validator-accept-reject.md) | End-to-end validator | A. Ground truth | ours | done |
| [05](EXP-05-per-layer-linear-probe-for-guru-laghu.md) | Per-layer guru/laghu probe | B. Probes | chandohasam | done (base) |
| [06](EXP-06-embedding-table-lookup-control.md) | Embedding-lookup control | B. Probes | chandohasam | **TBD — gates 05** |
| [07](EXP-07-poem-vs-bhavam-register-probe.md) | Register probe | B. Probes | chandohasam | done (base) |
| [08](EXP-08-metrical-order-nll-contrast-against-shuffle-and-pros.md) | Metrical-order NLL contrast | B. Probes | chandohasam | TBD |
| [09](EXP-09-infill-diagnostic-can-the-model-restore-blanked-syll.md) | **Infill diagnostic ★** | C. Capability | ours | done |
| [10](EXP-10-teacher-forced-versus-free-running-accuracy.md) | Teacher-forced vs free | C. Capability | chandohasam | TBD |
| [11](EXP-11-tokenizer-syllable-coverage-audit.md) | **Tokenizer coverage audit ★** | C. Capability | ours | done |
| [12](EXP-12-metrical-constraint-on-an-untrained-model.md) | Constraint, untrained model | D. Decoding | ours | done |
| [13](EXP-13-metrical-constraint-on-a-large-pretrained-model.md) | Constraint, pretrained model | D. Decoding | ours | done |
| [14](EXP-14-repetition-penalties-and-priority-ordered-constraint.md) | Penalties + relaxation order | D. Decoding | ours | done |
| [15](EXP-15-rejection-sampling-against-the-deterministic-verifie.md) | Rejection sampling | D. Decoding | ours | done |
| [16](EXP-16-constraint-annealing-canvas-warm-start-and-prompt-ri.md) | Annealing / warm-start / prompts | D. Decoding | ours | done (negative) |
| [17](EXP-17-recursive-context-expansion-across-iterations.md) | Recursive context expansion | E. Iteration | ours | done (saturates) |
| [18](EXP-18-multi-akshara-span-placement.md) | Multi-akshara spans | E. Iteration | ours | done (negative) |
| [19](EXP-19-generation-time-tracking.md) | Generation-time tracking | F. Mechanics | chandohasam | done (base) |
| [20](EXP-20-causal-drift-analysis-by-component-ablation.md) | Causal drift ablation | F. Mechanics | chandohasam | TBD |
| [21](EXP-21-poem-bhavam-layer-alignment-heatmap.md) | Poem–bhavam heatmap | F. Mechanics | chandohasam | partial |
| [22](EXP-22-chandas-direction-extraction-diff-in-means-caa.md) | Chandas direction extraction | G. Steering | chandohasam | TBD |
| [23](EXP-23-activation-steering-with-controls.md) | Activation steering | G. Steering | chandohasam | TBD |
| [24](EXP-24-representational-similarity-vs-symbolic-gana-distanc.md) | RSA vs gana distance | G. Steering | chandohasam | TBD |
| [25](EXP-25-akshara-aligned-tokenizer-construction-and-round-tri.md) | **Akshara tokenizer ★** | H. Training | ours | done |
| [26](EXP-26-realiser-training-and-the-infill-benchmark.md) | **Realiser training ★** | H. Training | ours | done |
| [27](EXP-27-realise-a-padyam-from-a-bag-of-words.md) | Realise from word bag | H. Training | ours | partial |
| [28](EXP-28-diffusion-objective-ablation-masked-vs-uniform-vs-co.md) | Objective ablation | H. Training | ours | done |
| [29](EXP-29-training-throughput-benchmark.md) | Throughput benchmark | H. Training | ours | done |
| [30](EXP-30-word-lattice-composition.md) | Word-lattice composition | I. Composition | ours | done |
| [31](EXP-31-bigram-prior-and-in-beam-neural-rescoring.md) | Bigram + in-beam rescoring | I. Composition | ours | partial |
| [32](EXP-32-corpus-ingestion-and-quality-audit.md) | Corpus ingestion + audit | J. Data | ours | done |
| [33](EXP-33-scaling-sufficiency-analysis.md) | Scaling sufficiency | J. Data | ours | done |
| [34](EXP-34-multi-task-instruction-dataset-construction.md) | Instruction dataset | J. Data | ours | built |

## Recommended order for a new model

**Cheap and decisive first.** These four cost minutes and predict most of the rest:

1. **EXP-11** — tokenizer syllable coverage. No model forward pass; predicts EXP-09.
2. **EXP-09** — infill diagnostic. The single most informative experiment in the set.
3. **EXP-05 + EXP-06** — probe, *with* the embedding-lookup control. Never EXP-05 alone.
4. **EXP-12** — constraint on random weights, to verify the harness before blaming any model.

Then, depending on what those show: if coverage is low and infill fails, the
limit is representational and EXP-25/26 is the path. If coverage is high and
infill succeeds, go to EXP-27 and the composition track.

## Controls that changed a conclusion

Recorded because in each case the naive version of the experiment gave the
wrong answer:

| experiment | control | what it prevented |
|---|---|---|
| EXP-03 | random-pair acceptance rate | adopting a rule with 100% recall that accepts half of all random pairs |
| EXP-06 | probe on raw embeddings | reading a layer-0 orthographic lookup as prosodic knowledge |
| EXP-08 | prose reordering, not just shuffle | concluding metrical sensitivity from a fluency effect |
| EXP-09 | corpus frequency baseline (~57%) | reading 60% as "above chance" |
| EXP-12 | random weights | attributing harness bugs to the model |
| EXP-18 | random logits | reading "the model won't use it" as "the mechanism is broken" |
| EXP-23 | random direction at matched norm | reading a perturbation-norm effect as a semantic one |
| EXP-25 | metrical round trip | training on targets that are silently 50% corrupt |
| EXP-28 | downstream task, not loss | ranking objectives by an incommensurable number |

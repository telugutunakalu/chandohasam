# semantic_coherence

Learns two metrics from human judgement — **Coherence** (does the poem make sense on its own) and
**Adherence** (does it keep the given bhāvaṃ) — from frozen sentence embeddings, since neither has
a deterministic check the way metre does. Also runs the LLM-as-judge comparison and the
poetics-suite cross-check on study 2. Status 2026-10-31: both metrics modeled and validated on
study 1; scored out-of-sample on study 2 (does not yet generalise there, reported honestly below).

## What is where

| what | where | in git |
|---|---|---|
| code | `sc_common.py`, `build_dataset.py`, `embed.py`, `modeling_comparison.py`, `final_models.py`, `significance_test.py`, `score_study2.py`, `study2_poetics.py`, `llm_judge/` | yes |
| results | `results/`, `llm_judge/results/` (numbers only, no poem text beyond what `human_evals/` already publishes) | yes |
| training data | `data/pooled_study1.csv`: built by `build_dataset.py` from `../human_evals/results/study1/ratings.csv` (committed, anonymised) and `../human_evals/annotation_app/data/poems.json` (committed) | no (gitignored, one command to rebuild) |
| embeddings | `embeddings_cache/*.npy`: built by `embed.py` | no (gitignored, ~1-2 GB, one command to rebuild) |

Nothing here needs the confidential crawled corpus: study 1's pool and study 2's pool are both
already published, in full, under `../human_evals/`.

## Definitions

For poem $i$: poem text $p_i$, bhāvaṃ text $b_i$, a frozen embedding backbone $f_\theta$ (never
fine-tuned — an earlier attempt to fine-tune mBERT with a contrastive loss was tried and dropped;
frozen embeddings generalise better at this sample size):
$$e_i^{(p)} = f_\theta(p_i) \in \mathbb{R}^{768}, \qquad e_i^{(b)} = f_\theta(b_i) \in \mathbb{R}^{768}$$
Mask-weighted mean pool of the last hidden state for BERT-style encoders (IndicBERT v2, mBERT,
mT5-encoder, MuRIL); the model's own `.encode()` for the SentenceTransformer-native backbones
(EmbeddingGemma-2, LaBSE). $y_i \in \{1,...,5\}$ is the human `bhavam` rating for row $i$ (one row
per (annotator, poem) pair; a poem rated by 3 group-A annotators contributes 3 rows sharing one
embedding).

**Coherence** — the poem embedding alone, standardised, multinomial logistic regression over the
five rating levels:
$$P(y_i=k\mid z_i)=\frac{\exp(w_k^\top z_i+c_k)}{\sum_{k'}\exp(w_{k'}^\top z_i+c_{k'})},\qquad
\hat y_i=\sum_{k=1}^5 k\cdot P(y_i=k\mid z_i)$$
fit by L2-penalised multinomial cross-entropy, $C=0.003$ (`modeling_comparison.py`,
`final_models.py`).

**Adherence** — the elementwise (Hadamard) product of the poem and bhāvaṃ embeddings:
$$x_i^{\text{adh}} = e_i^{(p)} \odot e_i^{(b)}, \qquad x^{\text{adh}}_{i,j} = e^{(p)}_{i,j}\cdot e^{(b)}_{i,j}$$
then the same model. This is a **learnable generalisation of cosine similarity**: cosine is
$\sum_j \hat e^{(p)}_j\hat e^{(b)}_j$ — the same per-dimension products, but with *uniform,
untrained* weights. The logistic model instead computes $\sum_j w_j\,e^{(p)}_{i,j}e^{(b)}_{i,j}$,
with $w_j$ fit to the human ratings, so dimensions that carry real alignment signal get
up-weighted and noisy ones down-weighted.

## Why these choices, not the obvious alternatives

Both tested directly, same data, same 5-fold × 5-seed stratified CV (`modeling_comparison.py`):

- **Cosine similarity does not work for Adherence.** cosine + Linear/Logistic gives Pearson r =
  0.02–0.20, and is *negative* for LaBSE (−0.09 to −0.15). Swapping to the elementwise-product
  feature is what fixes it (r jumps to 0.62–0.67); swapping only the head (Ridge → Logistic) on
  top of cosine barely moves the number. The feature, not the classifier, was the bottleneck.
- **Logistic Regression beats Ridge** on every one of 6 backbones for Coherence (+0.01–0.03 r).
  An ordinal-logit (proportional-odds) model, PCA-reduced to be numerically usable at n≈310, was
  also tried and did *worse* than both (treating the 5 levels as unordered classes and reading off
  the expected value apparently handles this small, noisy a sample better than the "textbook
  correct" ordinal treatment does).

## Results

### Modeling (study 1, group A only — see `../human_evals/README.md` for why A2/A4 are excluded)

5-fold stratified CV × 5 seeds, out-of-fold predictions, 310 pooled rows / 116 unique poems
(`results/coherence_model_comparison.csv`, `results/adherence_model_comparison.csv`,
`results/significance_tests.csv`):

| backbone | Coherence r | Adherence r |
|---|---|---|
| MuRIL | ~0.66 | ~0.67 |
| IndicBERT v2 | ~0.66 | ~0.66 |
| LaBSE | ~0.65 | ~0.63 |
| mBERT | ~0.65 | ~0.64 |
| mT5 | ~0.64 | ~0.67 |
| EmbeddingGemma-2 | ~0.64 | ~0.64 |

(Run `significance_test.py` for exact current numbers — small CV-seed noise moves these by ±0.01
from run to run.) All 12 (backbone × task): permutation p = 0.001 (1000/1000 label-shuffles beaten),
bootstrap 95% CI excludes 0 by a wide margin. Raw per-coefficient p-values are **not** reported:
with 768 features and ~310 rows, standard MLE asymptotics don't apply and L2 regularisation
deliberately biases the coefficients, so a per-dimension significance test would be meaningless —
the permutation/bootstrap pair above is the valid alternative.

### Scored on the whole pool (`final_models.py` → `results/coherence_per_poem.csv`,
`results/adherence_per_poem.csv`)

The final model (refit on all 310 rows) scores all 500 study-1 poems: the 116 rated, and the 384
held out of annotation. Every source split, rated and unrated alike, cleanly separates
Gemini-generated poems (≈3.1–3.7) from all four human-authored sources (≈4.5–4.9) — the single
most consistent signal in the whole approach.

### Does it generalise to study 2? No — and this is reported, not smoothed over

Scored out-of-sample on study 2's 99 fine-tuned-model poems (`score_study2.py` →
`results/study2_scores.csv`), against the real study-2 human ratings as they come in
(`../human_evals/results/study2/`): correlation is at noise level (roughly −0.19 to +0.21 across
backbones, against 0.62–0.67 in-distribution on study 1), and the model predicts near-ceiling
scores (4.3–4.5) against a real human ceiling of 1.6–2.1, ranking the three fine-tuned models
*backwards* relative to what the annotators say. Study 1 is free/topic-prompted generation from
mostly fluent sources; study 2 is bhāvaṃ-reconstruction by small fine-tuned models under a hard
metrical constraint — different enough that this model does not transfer, and a new model trained
with study-2 data was tried and also abandoned (pooling raises the *pooled* r by inflating
between-study separability, not within-study accuracy — see git history for that exploration).

### Poetics suite cross-check on study 2 (`study2_poetics.py` → `results/study2_poetics.csv`)

Runs `../poetry_metrics`'s anuprāsa v3 / mādhurya / ojas / prasāda / caṃdomiti on the same 99
poems, gated by a **ref.-corpus token coverage** proxy (`known_word_share` from
`poetry_metrics/prasada.py`'s 362k-poem reference table — not the project's full word-resolution
pipeline, which needs `padarchana.db` and isn't available in this environment; see
`../poetry_metrics/anuprasa_v3.py`'s docstring). MDLM-523M has the highest coverage and strongest
alliteration; Nandi is weakest on both — but MDLM-523M is only mid-ranked by real humans on
coherence/bhāvaṃ, so lexical realism (by this proxy) tracks alliteration but not meaning.

### LLM-as-judge (`llm_judge/`)

Five local models (Gemma-4 E2B, Llama 3.2 3B, Qwen2.5 7B, Llama 3.1 8B, Gemma 3 12B; Aya Expanse
8B was dropped before completion) rate every study-1 poem on the same 10-question rubric, zero-shot,
greedy decoding. Correlation with the human mean varies sharply by question
(`llm_judge/results/llm_judge_correlations.csv`, `llm_judge/judge_by_source.py` for the per-source
breakdown): readability/comprehension/lexical reach r≈0.25–0.45 for the stronger models, but
**bhāvaṃ fidelity — the one question that matters for Coherence/Adherence — is at chance or worse
for every model** (r = −0.19 to +0.10; two models give constant/degenerate output on it). This is
the sharpest evidence that the learned embedding metric (r=0.62–0.67 on the same target) is doing
something zero-shot LLM judging is not.

## Commands

```bash
cd semantic_coherence
python3 build_dataset.py                 # -> data/pooled_study1.csv

# needs torch, transformers, sentence-transformers (a venv with Apple-Silicon MPS or a GPU)
python3 embed.py                         # -> embeddings_cache/*.npy (~15-20 min on MPS)

# needs scikit-learn, scipy, pandas, statsmodels
python3 modeling_comparison.py           # -> results/*_model_comparison.csv
python3 final_models.py                  # -> results/{coherence,adherence}_per_poem.csv
python3 significance_test.py             # -> results/significance_tests.csv (~15-20 min)
python3 score_study2.py                  # -> results/study2_scores.csv

# needs krippendorff, numpy
python3 human_eval_agreement.py          # recomputes study-1 agreement from the committed source

# needs poetry_metrics' own dependencies (PyYAML; Python 3.12+ for its f-string syntax)
python3 study2_poetics.py                # -> results/study2_poetics.csv

# needs mlx-lm (Apple Silicon only) -- see llm_judge/README conventions above; already run,
# results committed, so this is for reproduction only
cd llm_judge && python3 run_all_judges.py && python3 judge_correlations.py
```

## Known limits

- **Study 2 generalisation failure** is unresolved (see above) — the honest next step is a model
  trained once study 2's annotations are complete, with its own CV protocol, not a patch on the
  study-1 model.
- **The ref.-corpus coverage proxy used in `study2_poetics.py`** is not the project's word
  resolution system. If `padarchana.db` and the BiLSTM/ByT5 resolver become available in this
  environment, that gating should be redone with the real pipeline.
- **One poem (he_0096)** has no Telugu bhāvaṃ text and is excluded from Adherence only.
- Coefficients are extractable (`LogisticRegression.coef_`) but not individually interpretable:
  a mean-pooled embedding dimension has no fixed semantic meaning, so a per-dimension "this
  dimension means X" reading would be invented, not measured.

# Semantic Coherence & Adherence in Telugu Metrical Poetry

A research report on building and evaluating automatic metrics for two human-judged qualities of generated/authored Telugu *padyams* (metrical poems): **Coherence** (does the poem convey a coherent idea, judged from the text alone) and **Adherence** (how faithfully the poem expresses its intended meaning, the *bhavam*).

---

## 1. Definitions

- **Coherence**: internal textual coherence of a poem, judged on the poem alone, with no reference to any intended meaning.
- **Adherence**: the fit between a poem and its *bhavam* (the stated intended meaning) — how faithfully the poem conveys that specific meaning.
- Both are ultimately anchored to the human `bhavam` rubric rating ("how close is the poem to the bhavam?", 1–5), since that is the only rating that explicitly ties the poem back to a reference meaning.

---

## 2. Human Evaluations

### 2.1 Rubric

The annotation app (`human_evals/annotation_app`) scores every poem on a fixed **10-question rubric** (`rubric.py`):

| # | Key | Scale | Question |
|---|---|---|---|
| 1 | `readability` | 1–5 | How easy is it to read? |
| 2 | `comprehension` | 1–5 | How easy is it to understand immediately after reading (before seeing the bhavam)? |
| 3 | `lexical` | 1–5 | How easy is it to recognize and understand the words? |
| 4 | `bhavam` | 1–5 | How close is the poem to the bhavam? |
| 5 | `chandassu` | 0/1 | Is the meter (gaṇas, guru/laghu, pāda count) correct? |
| 6 | `prasa` | 0/1 | Is prāsa correct? (only asked for meters with a prāsa rule) |
| 7 | `yati` | 0/1 | Is yati correct? |
| 8 | `shabdalankara` | 0/1 | Any sound figures identifiable? |
| 9 | `arthalankara` | 0/1 | Any figures of meaning identifiable? |
| 10 | `poetic` | 1–5 | How poetic is it overall? |

Two further per-poem metadata fields exist in the export but are **not** annotator judgments (constant per poem, not rated per-annotator): `calibration` (is this poem in the shared calibration set) and `register` (classical/elevated vs. modern/colloquial diction, 1=classical).

### 2.2 Data

- **Pool**: 500 poems (`human_evals/annotation_app/data/poems.json`), spanning 5 sources: `bhagavatam`, `vemana`, `kuchimanchi`, `reference`, and `generated` (AI-authored, flagged `ai_generated=1`).
- **Annotators used for modeling**: `shyam`, `mahesh`, `samvaran` — 305 pooled ratings over **116 unique poems** (each poem rated by up to 3 annotators, kept as separate rows, not averaged).
- `bhagavatam`: 35, `vemana`/`reference`/`kuchimanchi`: 20 each, `generated`: 21 (rated); 384 further poems in the pool are unrated.

---

## 3. Embedding-Based Modeling

### 3.1 Methodology

**Notation.** For poem $i$, let $p_i$ be its poem text and $b_i$ its bhavam text (where one exists). A frozen embedding backbone $f_\theta$ maps text to a fixed-size vector:

$$e_i^{(p)} = f_\theta(p_i) \in \mathbb{R}^{768}, \qquad e_i^{(b)} = f_\theta(b_i) \in \mathbb{R}^{768}$$

$f_\theta$ is never fine-tuned. For BERT-style encoders (mBERT, IndicBERT v2, MuRIL, mT5-encoder) it is a mask-weighted mean pool of the last hidden state:
$$f_\theta(\text{text}) = \frac{\sum_t m_t \cdot h_t}{\sum_t m_t}, \quad h_t = \text{last\_hidden\_state}_t,\ m_t = \text{attention\_mask}_t$$
For SentenceTransformer-native backbones (EmbeddingGemma-2, LaBSE) it is the model's own `.encode()` (L2-normalized pooled output).

$y_i \in \{1,2,3,4,5\}$ is the human `bhavam` rating for row $i$ (one row per (annotator, poem) pair; a poem rated by 3 annotators contributes 3 rows sharing the same embedding).

**Coherence — features, model, training.**
- Feature vector: the poem embedding alone, $x_i^{\text{coh}} = e_i^{(p)} \in \mathbb{R}^{768}$. No bhavam is used — Coherence is judged from the poem text only.
- Standardize per-dimension (mean/std fit on the training fold only): $z_i = (x_i^{\text{coh}} - \mu)/\sigma$.
- Model: **multinomial logistic regression**, L2-regularized, treating the five rating levels as classes:
$$P(y_i = k \mid z_i) = \frac{\exp(w_k^\top z_i + c_k)}{\sum_{k'=1}^{5}\exp(w_{k'}^\top z_i + c_{k'})}, \qquad k \in \{1,\dots,5\}$$
fit by minimizing the L2-penalized multinomial cross-entropy over the training rows:
$$\min_{W,\,c}\ \sum_i -\log P(y_i \mid z_i)\ +\ \frac{1}{2C}\sum_{k}\lVert w_k\rVert_2^2, \qquad C = 0.003$$
- Scoring (continuous, for correlation against the 1–5 scale): the **expected value** of the predicted class distribution,
$$\hat y_i^{\text{coh}} = \mathbb{E}[y \mid z_i] = \sum_{k=1}^{5} k \cdot P(y_i = k \mid z_i)$$

**Adherence — features, model, training.**
- Feature vector: the **elementwise (Hadamard) product** of the poem and bhavam embeddings,
$$x_i^{\text{adh}} = e_i^{(p)} \odot e_i^{(b)} \in \mathbb{R}^{768}, \qquad x_{i,j}^{\text{adh}} = e^{(p)}_{i,j}\cdot e^{(b)}_{i,j}$$
  This is a **learnable generalization of cosine similarity**. Cosine similarity is $\cos(e^{(p)}, e^{(b)}) = \sum_j \hat e^{(p)}_j\,\hat e^{(b)}_j$ (dot product of the L2-normalized vectors) — an *unweighted* sum across the 768 dimensions, with no training. Feeding $x_i^{\text{adh}}$ into a linear-in-the-features model $w^\top x_i^{\text{adh}} = \sum_j w_j\, e^{(p)}_{i,j}e^{(b)}_{i,j}$ gives a **per-dimension-weighted** dot product instead — the weights $w_j$ are fit to the human `bhavam` labels, so dimensions that carry real semantic-alignment signal can be up-weighted and noisy ones down-weighted, rather than trusting the raw embedding geometry.
- Standardize and fit exactly as for Coherence — same multinomial logistic regression, same $C=0.003$, with $x^{\text{adh}}$ in place of $x^{\text{coh}}$:
$$P(y_i = k \mid z_i^{\text{adh}}) = \frac{\exp(w_k^\top z_i^{\text{adh}} + c_k)}{\sum_{k'}\exp(w_{k'}^\top z_i^{\text{adh}} + c_{k'})}, \qquad \hat y_i^{\text{adh}} = \sum_{k=1}^{5} k\cdot P(y_i=k\mid z_i^{\text{adh}})$$

**Why logistic regression over linear/Ridge regression, and why a learned similarity over raw cosine.** Both were tested directly, same data, same CV protocol:
- Ridge regression (treating $y$ as continuous) was the original choice; multinomial logistic beat it on every one of the 6 backbones for Coherence (Pearson r higher by ~0.01–0.03). An ordinal-logit model (proportional-odds, the "textbook-correct" treatment of an ordinal target) was also tried and did *worse* than both — its linear proportional-odds assumption appears too restrictive for this data, so it was not used.
- Raw cosine similarity (a single scalar feature) fed into linear regression was the original Adherence pipeline; it is weak (Pearson r = 0.03–0.20, even *negative* for one backbone). Replacing it with the elementwise-product feature above and logistic regression raises every backbone's Adherence correlation to r ≈ 0.62–0.67 — matching Coherence. This is the modeling choice reported in §3.2 below.

**Ablation: cosine similarity vs. the learned (elementwise-product) similarity, crossed with the regression head.** Same CV protocol, same 6 backbones, isolating the two factors (feature choice, head choice):

| Backbone | cosine + Linear | cosine + Logistic | learned-sim + Ridge | **learned-sim + Logistic (used)** |
|---|---|---|---|---|
| IndicBERT v2 | 0.197 | 0.181 | 0.643 | **0.665** |
| mT5 | 0.169 | 0.171 | 0.643 | **0.668** |
| MuRIL | 0.153 | 0.146 | 0.636 | **0.666** |
| mBERT | 0.169 | 0.192 | 0.618 | **0.629** |
| EmbeddingGemma-2 | 0.031 | 0.010 | 0.619 | **0.635** |
| LaBSE | -0.147 | -0.092 | 0.619 | **0.620** |

The gain is almost entirely from the **feature** (cosine → elementwise product: +0.42 to +0.59 Pearson), not from the classifier swap (Ridge → Logistic on the same feature: a further +0.01–0.03, same pattern as the Coherence ablation above). Swapping only the head while keeping cosine similarity (cosine+Linear → cosine+Logistic) barely moves the number, and sometimes makes it slightly worse — confirming that a fixed, untrained scalar similarity is the real bottleneck, not the choice of regression vs. classification on top of it.

**Evaluation protocol.** 305 pooled (annotator, poem) rows, 116 unique poems. 5-fold stratified cross-validation (stratified on the integer `bhavam` label) × 5 random seeds (0–4); in each (seed, fold) the standardizer and the logistic model are fit on the training folds only and applied to the held-out fold. Out-of-fold predictions are averaged across the 5 seeds to give one prediction per row, then compared to the true $y_i$ with Pearson r, Spearman ρ, and MAE — no further calibration. For the per-source tables (§3.2), one final model per backbone is refit on **all** 305 pooled rows and applied to score every rated poem and every unrated poem, for both Coherence and Adherence — 499/500 poems in the full pool (including 383/384 unrated ones) have Telugu bhavam text available, so $x_i^{\text{adh}}$ can be formed for almost the entire unrated set too (one poem, he_0096, lacks bhavam text and is excluded from the Adherence-unrated table only).

### 3.2 Results

**Correlation (5-fold × 5-seed cross-validated, out-of-fold predictions, 305 pooled rows, 116 unique poems):**

| Backbone | Coherence r | Coherence ρ | Adherence r | Adherence ρ |
|---|---|---|---|---|
| MuRIL | 0.657 | 0.465 | 0.666 | 0.455 |
| IndicBERT v2 | 0.657 | 0.452 | 0.665 | 0.464 |
| LaBSE | 0.643 | 0.491 | 0.620 | 0.438 |
| mBERT | 0.640 | 0.494 | 0.629 | 0.467 |
| mT5 | 0.625 | 0.440 | **0.668** | 0.458 |
| EmbeddingGemma-2 | 0.628 | 0.441 | 0.635 | 0.441 |

Both tasks land in the same tight r≈0.62–0.67 band, on every backbone — Adherence is no longer weaker than Coherence.

**Per-source breakdown — Coherence, rated poems (116 unique)** — actual mean `bhavam` vs. predicted:

| source | n | actual | IndicBERTv2 | mBERT | mT5 | EmbeddingGemma2 | LaBSE | MuRIL |
|---|---|---|---|---|---|---|---|---|
| vemana | 20 | 4.892 | 4.748 | 4.761 | 4.691 | 4.705 | 4.735 | 4.745 |
| reference | 20 | 4.683 | 4.623 | 4.573 | 4.606 | 4.617 | 4.616 | 4.592 |
| kuchimanchi | 20 | 4.642 | 4.518 | 4.461 | 4.498 | 4.493 | 4.520 | 4.542 |
| bhagavatam | 35 | 4.581 | 4.626 | 4.611 | 4.609 | 4.581 | 4.566 | 4.598 |
| **generated** | 21 | **3.087** | 3.279 | 3.446 | 3.406 | 3.431 | 3.403 | 3.337 |

**Per-source breakdown — Coherence, unrated poems (384)** — predicted only:

| source | n | IndicBERTv2 | mBERT | mT5 | EmbeddingGemma2 | LaBSE | MuRIL |
|---|---|---|---|---|---|---|---|
| bhagavatam | 192 | 4.684 | 4.690 | 4.635 | 4.590 | 4.617 | 4.678 |
| **generated** | 63 | 3.426 | 3.615 | 3.634 | 3.692 | 3.717 | 3.511 |
| kuchimanchi | 50 | 4.585 | 4.551 | 4.556 | 4.509 | 4.501 | 4.657 |
| reference | 52 | 4.629 | 4.556 | 4.613 | 4.551 | 4.540 | 4.615 |
| vemana | 27 | 4.673 | 4.693 | 4.607 | 4.560 | 4.450 | 4.680 |

**Per-source breakdown — Adherence, rated poems (116 unique)** — actual mean `bhavam` vs. predicted:

| source | n | actual | IndicBERTv2 | mBERT | mT5 | EmbeddingGemma2 | LaBSE | MuRIL |
|---|---|---|---|---|---|---|---|---|
| vemana | 20 | 4.892 | 4.788 | 4.749 | 4.719 | 4.732 | 4.720 | 4.753 |
| reference | 20 | 4.683 | 4.657 | 4.602 | 4.644 | 4.617 | 4.615 | 4.635 |
| kuchimanchi | 20 | 4.642 | 4.579 | 4.518 | 4.577 | 4.562 | 4.549 | 4.591 |
| bhagavatam | 35 | 4.581 | 4.570 | 4.583 | 4.572 | 4.531 | 4.538 | 4.571 |
| **generated** | 21 | **3.087** | 3.246 | 3.406 | 3.313 | 3.414 | 3.434 | 3.299 |

**Per-source breakdown — Adherence, unrated poems (383/384 — 499/500 of the full pool has Telugu bhavam text; one unrated poem, he_0096, lacks it and is excluded)** — predicted only:

| source | n | IndicBERTv2 | mBERT | mT5 | EmbeddingGemma2 | LaBSE | MuRIL |
|---|---|---|---|---|---|---|---|
| vemana | 27 | 4.710 | 4.737 | 4.696 | 4.644 | 4.528 | 4.685 |
| reference | 52 | 4.658 | 4.596 | 4.666 | 4.582 | 4.569 | 4.638 |
| kuchimanchi | 50 | 4.661 | 4.585 | 4.648 | 4.572 | 4.569 | 4.641 |
| bhagavatam | 192 | 4.613 | 4.663 | 4.650 | 4.573 | 4.589 | 4.627 |
| **generated** | 62 | 3.492 | 3.590 | 3.540 | 3.828 | 3.844 | 3.517 |

**Every single backbone, on Coherence and Adherence alike, rated and unrated, cleanly separates `generated` (≈3.2–3.8) from all four human-authored sources (≈4.5–4.9).** This is the clearest, most consistent signal found across the whole embedding-based approach.

---

## 4. LLM-as-a-Judge

### 4.1 Methodology

Zero-shot: each model is shown a poem (+ bhavam, for the `bhavam` question) and asked to return a single JSON object scoring **all 10 rubric questions** at once. Run via `mlx-lm` on-device (Apple M4, 16GB unified memory), 4-bit quantized. Same 116 unique poems as the embedding work; judged once per poem, broadcast to the 305 pooled rows for comparison. **Greedy decoding (temp=0)**, no calibration — raw judge output compared directly to raw human scores.

**Models**: Gemma 4 E2B, Gemma 3 12B (largest Gemma 3 safely loadable), Llama 3.2 3B, Llama 3.1 8B, Qwen2.5 7B. Aya Expanse 8B was tried and dropped — its documented 23 supported languages don't include Telugu (only Hindi among Indic languages).

Two issues were found and fixed before the results below were trustworthy: Gemma 4 emits a native chain-of-thought block (`<|channel>thought...<channel|>`) before any answer, which needed a much larger token budget (6000 vs. 500 for the other models) to ever reach the JSON; and every model's default generation config samples stochastically (`do_sample=True`), which was overridden with greedy decoding (`temp=0`) for reproducibility.

### 4.2 Results

**Likert items — Pearson r / Spearman ρ** (n=302–305 pooled rows):

| Model | bhavam | readability | comprehension | lexical | poetic |
|---|---|---|---|---|---|
| Gemma 3 12B | -0.008 / -0.025 | 0.349 / 0.375 | 0.403 / 0.394 | **0.446 / 0.438** | 0.133 / 0.079 |
| Gemma 4 E2B | -0.065 / -0.086 | 0.362 / 0.366 | 0.395 / 0.401 | 0.257 / 0.295 | 0.153 / 0.177 |
| Qwen2.5 7B | 0.097 / 0.111 | 0.008 / -0.001 | 0.100 / 0.103 | 0.116 / 0.104 | 0.004 / 0.002 |
| Llama 3.2 3B | undefined (constant 5) | -0.057 / -0.077 | -0.100 / -0.091 | undefined (constant 5) | 0.118 / 0.132 |
| Llama 3.1 8B | undefined (constant 5 on *every* Likert item) | | | | |

**Binary items — accuracy / Cohen's κ:**

| Model | chandassu | prasa | yati | shabdalankara | arthalankara |
|---|---|---|---|---|---|
| Gemma 3 12B | 0.938/κ=0.0 | 0.974/κ=0.0 | 0.682/κ=0.014 | 0.482/κ=0.055 | 0.505/κ=0.061 |
| Gemma 4 E2B | 0.897/κ=0.0 | 0.812/κ=0.0 | 0.818/κ=-0.007 | 0.606/κ=0.146 | 0.566/κ=0.124 |
| Qwen2.5 7B | 1.000/κ=undef | 0.947/κ=0.0 | 0.957/κ=-0.006 | 0.570/κ=0.025 | 0.541/κ=0.022 |
| Llama 3.2 3B | 1.000/κ=undef | 1.000/κ=undef | 0.997/κ=0.0 | 0.439/κ=0.0 | 0.469/κ=0.0 |
| Llama 3.1 8B | 1.000/κ=undef | 1.000/κ=undef | 0.997/κ=0.0 | 0.626/κ=0.197 | 0.557/κ=0.130 |

High accuracy on chandassu/prasa/yati is vacuous — it comes from always predicting the (near-universal) majority class "correct," not genuine meter-rule checking; κ≈0 confirms chance-level agreement almost everywhere.

**Per-source breakdown (bhavam)** — actual mean vs. each model's mean:

| source | n | actual | Gemma4 E2B | Llama3.2 3B | Qwen2.5 7B | Llama3.1 8B | Gemma3 12B |
|---|---|---|---|---|---|---|---|
| vemana | 20 | 4.89 | 4.50 | 5.0 | 4.05 | 5.0 | 4.00 |
| reference | 20 | 4.68 | 4.16 | 5.0 | 4.60 | 5.0 | 3.20 |
| kuchimanchi | 20 | 4.64 | 4.10 | 5.0 | 3.55 | 5.0 | 3.45 |
| bhagavatam | 35 | 4.58 | 4.17 | 5.0 | 4.29 | 5.0 | 3.43 |
| **generated** | 21 | **3.09** | **4.57** | 5.0 | 4.10 | 5.0 | **3.95** |

Humans separate `generated` (3.09) cleanly from every human source (4.58–4.89) on bhavam-faithfulness — the same pattern §3.2 showed every embedding backbone reproduces, on both Coherence and Adherence. **None of the 5 LLM judges reproduce it; Gemma 4 E2B and Gemma 3 12B actually invert it**, rating AI-generated poems as *more* faithful to their stated meaning than classical human-authored poems. Qwen2.5 and both Llamas show no separation at all (the Llamas' being vacuous/constant).

### 4.3 Bottom line

Zero-shot LLM-as-judge, at the 2–12B scale reachable on this hardware, is worse than the embedding-based approach on every axis measured — weaker correlations, several completely degenerate (constant-output) models, vacuous binary accuracy, and on the one question that matters most (AI-vs-human faithfulness), two of five models get the direction backwards.

# Chandohasam — Compiled Evaluation Results

Compiled 2026-10-31 from primary source files in this repository and in the `semantic_coherence/`
subproject (§6 lists every script and result file). Every number here is either read directly from
a committed result file or computed fresh from a committed raw-data file by the scripts named in
each section; none is taken from any earlier draft of the paper.

**Update:** Samvaran has pushed the poetics suite and real word resolution (the actual resolver,
not a proxy) run on every source in this project's own grid, including the full Gemini set
(`poetry_metrics/score_sources.py`, `word_resolution_sources.py`). §5 below is now the complete,
unified grid: Coherence, Adherence, the full poetics suite, and real word-resolution coverage,
side by side, per source. One loose end: his Gemini dedup kept 246 of 255 poems, mine (for
Coherence/Adherence) kept 237 — different duplicate criteria, 9-poem difference, not chased down
further; the Coherence/Adherence numbers on that row are marked with an asterisk for this reason.

**§1's 90.78% / 93.00% / 96.27%** are a separate measurement from §5's word-resolution column:
§1 is the resolver's own validation on the much larger Padyarchana corpus (382,052 poems, with
judged-verdict precision figures); §5 is the same resolver run on this project's own poems. Both
are the real system now — nothing in this report uses a proxy any more.

---

## 1. Word Resolution

### 1.1 Methodology

**Task.** Attach every word occurrence of the Padyarchana corpus to a dictionary headword in
`padarchana.db`, so that definitions, grammar and meanings can be shown for any word of any poem,
and so that a poem's words can be checked for well-formedness beyond simple string lookup.

**Corpus.** 382,052 poems, 5,483,449 word occurrences (pipeline tokens), 2,004,820 distinct word
types. 99.6% of poems carry a word-by-word glossary (editorial, human-made, 169,606 poems; or
machine, Gemini-3.5-flash-lite, 378,758 poems) used only as *evidence*, never as an answer.

**Dictionary (`padarchana.db`, 1.61 GB, 50 Telugu dictionaries merged):**

| table | rows | contents |
|---|---|---|
| entries | 133,539 | one row per headword spelling |
| definitions | 367,100 | one per (entry, dictionary) |
| meanings | 608,520 | numbered senses |
| variants | 110,801 | alternate spellings of a headword |
| `paradigm_forms.db` | - (3.4 GB) | every headword's generated inflected forms (the wordform layer) |
| `padyarchana_forms` (glossary, evidence only) | 4,766,005 | editorial + machine glossary of the corpus itself |

Largest constituent dictionaries: వావిళ్ల నిఘంటువు (40,563 definitions), శ్రీహరి (28,810),
శంకరనారాయణ (28,177), శబ్దరత్నాకరము (25,823), బ్రౌణ్య (24,739), విజయ (17,555), తెలుగు నిఘంటువు
(16,380); Sanskrit-Telugu: ఆంధ్ర-సంస్కృత కోశము (14,384); verb-form dictionary క్రియాస్వరూప
మణిదీపిక (7,308, verb roots loaded directly); పురాణనామచంద్రిక (1,029 names). 7 more dictionaries
were tested in Oct 2026 and measured one at a time on the gold set before being admitted; most
bulk digital editions (DSAL బ్రౌణ్య, Telugu Wiktionary) **raised coverage but lowered held-out
precision** (0.645→0.620) and were rejected. Only a small crawl-fix (47 definitions) and
309 judge-confirmed headwords were kept in.

**Pipeline (7 stages, `bilstm/run_pipeline_v28.sh`, ≈1h45m over the whole corpus):**
1. Tokenisation, with line-end and spacing joins repairing the edition's broken words.
2. Dictionary pass: guaranteed-answer table first, then the lexicon's whole-word reading, then
   competing candidates (editorial split, BiLSTM splits at 3 thresholds, unsplit).
3. Attestation: promotes partial/unresolved words whose form occurs in dictionary text or a
   glossary.
4. Final stage: a meaning resolver (string similarity + embedding cosine gate), the distilled
   ByT5 resolver (4 beams), gloss support.
5. Context joins and fragment scan: repairs words the edition broke across a line or space.
6. Merge of gloss-supported readings.
7. Context pass: per-poem majority vote over a glossed poem's homograph readings.

**Inflected words / wordforms.** The single largest resolved class (33.5% of occurrences). The
lexicon strips, in order: plural `-లు`, oblique `-ల`, case endings, `-ంబు/-ము`, `-ఁడు/-డు`, the
drutam, verb endings, converbs, particles (`-యు -తో -ను -అని -ఏ -ఐ -ఓ`), then falls back to
**`paradigm_forms.db`** (every headword's precomputed inflections) to confirm or complete what the
rule-based stripper can't reach. Last-resort rules: syncope, Sanskrit consonant-stem/visarga
rules, త్రిక splits, initial-sandhi undoing.

**Evaluation.** Two independent measures: (a) *coverage* - the token-weighted share of
occurrences in each confidence band, over the whole corpus; (b) *precision* - judged verdicts
(14,129 verdicts on 6,348 words, 78 by hand, the rest by an external model, cross-checked by a
second reading) scored under the **full-word rule** (a piece is scored on the pipeline's reading
of its full word, never a fragment) on a **held-out 30% split by word hash**, fixed before any
verdict existed.

### 1.2 Results (v28)

| band | occurrences | share |
|---|---|---|
| resolved to a headword | 4,977,000 | **90.78%** |
| + gloss-based evidence | ≈5,099,600 | 93.00% |
| + attested (no headword, but vouched for) | ≈5,279,000 | 96.27% |
| open | ≈204,400 | 3.73% |

By shape: single word (headword or inflected) 3,198,170 (58.3%); sandhi split (letters changed at
the seam) 1,131,310 (20.6%); plain concatenation 648,638 (11.8%).

| precision test | n | right / wrong / none | precision |
|---|---|---|---|
| fair held-out judged words (full-word rule) | 1,309 | 0.472 / 0.224 / 0.304 | **0.678 ± 0.03** |
| symbolic baseline (lexicon + sandhi rules only, no model) | 1,309 | 0.269 / 0.387 / 0.344 | 0.410 |
| random sample, headword level, corpus-wide | 478 judged | - | 0.696, 95% CI [0.65, 0.74] |

Per-poem (382,049 poems): macro mean resolved 0.903, median 0.929; 36.3% of poems fully resolved,
62.1% at 90%+. By glossary layer: human-glossed poems 0.908 resolved, machine-only 0.899.

Lesson for the benchmark: **coverage alone overstates correctness** - roughly a quarter of what's
"resolved" by weak classes is wrong, which is why precision is reported beside coverage throughout
this document rather than coverage alone.

---

## 2. Human Evaluations

Both studies report **group A only** (A1, A3, A5) throughout this document - this is the
project's own committed convention (`human_evals/README.md`): group B (A2, A4) disagreed with
each other (α below 0 on readability, bhāvaṃ, poetic in study 1) and their poem means did not
track group A's.

### 2.1 Study 1 - design

500-poem pool, stratified across 33 canonical metres and verified by the exact metre scanner:
Bhāgavatam 227, Gemini-generated 84, textbook examples 72, Kūcimañci Timmakavi 70, Vemana 47.
Annotators rate blind to source; a 25-poem calibration set first, then a 100-poem phase 1, then
the rest. **Rubric v2**, 12 questions: readability, comprehension, lexical ease, bhāvaṃ-closeness
(1-5); chandassu/prāsa/yati correct (yes/no); śabdālaṅkāra/arthālaṅkāra present (yes/no); poetic
(1-5); register - grānthika/ādhunika (yes/no); AI-generated (yes/no). Live 2026-10-13, rubric v2
from 10-26, complete 2026-10-30.

### 2.2 Study 1 - results, per source

Group A: 310 ratings on 116 poems (94 rated by all 3, 6 by 2, 16 by 1).

| question | α | mean (all sources) |
|---|---|---|
| readability | 0.333 | 4.24 |
| comprehension | 0.485 | 3.50 |
| lexical | 0.442 | 4.02 |
| bhāvaṃ | 0.432 | 4.36 |
| poetic | 0.342 | 3.75 |
| register | 0.331 | 78% grānthika |
| AI-generated | 0.529 | 14% yes |
| chandassu / prāsa | - (constant) | 100% / 100% yes |
| yati | 0.000 | 99.7% yes |
| śabdālaṅkāra / arthālaṅkāra | ≈0 | ≈45% / ≈52% |

**Mean rating per source (poem means):**

| question | bhagavatam (35) | vemana (20) | kuchimanchi (20) | textbook (20) | generated/Gemini (21) |
|---|---|---|---|---|---|
| readability | 3.93 | 4.82 | 3.88 | 3.94 | 4.78 |
| comprehension | 3.27 | 4.28 | 2.97 | 3.10 | 4.13 |
| lexical | 3.89 | 4.77 | 3.48 | 3.55 | 4.54 |
| bhāvaṃ | 4.58 | 4.89 | 4.64 | 4.67 | **3.13** |
| poetic | 4.19 | 3.92 | 3.97 | 3.71 | **3.00** |
| grānthika | 83% | | | 97% | 48% |
| judged AI | 0.6% | | | 6.8% | **62.3%** |

Gemini vs. poets, annotator-centred (95% CI, ✱=excludes 0): readability +0.57✱, comprehension
+0.67✱, lexical +0.50✱, **bhāvaṃ −1.57✱**, poetic −1.00✱.

### 2.3 Study 2 - design

The three best fine-tuned grid models (MDLM-523M, T5Gemma-2-1B, Nandi-150M), each with the v2
metrical decoder, write the same 33 prompts → 99 poems (`he2_0001`-`he2_0099`). Prompts: study-1
gold poems with ≥4 raters (44 eligible), top-ranked by z(gold's study-1 score) + z(separability);
12 Vemana + 11 Kuchimanchi + 10 Bhāgavatam taken. **Rubric v3** adds Q13, "how meaningful
(coherent) is the poem" - a *separate* question from Q4 bhāvaṃ-closeness. Engine verdicts are
hidden (study 1 showed them); **not blind** - annotators know every poem is model-generated. In
progress: 220/297 possible ratings (80, 79, 62 of 99 for A5/A3/A1) as of 2026-10-31.

### 2.4 Study 2 - results, per model

| model | n ratings / poems | readability | comprehension | lexical | coherence (Q13) | bhāvaṃ | poetic | AI-flagged |
|---|---|---|---|---|---|---|---|---|
| MDLM-523M | 62 / 23 | 3.62 | 2.19 | 3.30 | 1.88 | 1.77 | 1.67 | 99% |
| T5Gemma-2-1B | 84 / 30 | 3.56 | 2.19 | 3.12 | **2.07** | **1.99** | **1.91** | 95% |
| Nandi-150M | 74 / 27 | 3.36 | 2.01 | 3.06 | 1.80 | 1.64 | 1.69 | 95% |
| the same 33 golds, study 1 | | 4.27 | 3.49 | 4.11 | - | 4.71 | 4.02 | - |

Each model against its own prompt's gold (bootstrap 95% CI, ✱=excludes 0), all three models:
**bhāvaṃ −2.90✱, poetic −2.24✱, comprehension −1.37✱, lexical −0.98✱, readability −0.78✱.**
T5Gemma-2-1B beats the other two on coherence/bhāvaṃ/poetic (+0.25/+0.32/+0.22 vs. the mean of
the other two, CI excludes 0); Nandi trails on the same three; MDLM-523M is within noise of the
mean. Agreement is low (α 0.22-0.28, below 0 on comprehension/coherence/poetic) - most ratings
sit at 1-2.

---

## 3. Semantic Coherence & Adherence - Definitions and Modeling

### 3.1 Definitions

For poem $i$: poem text $p_i$, bhāvaṃ text $b_i$, frozen embedding backbone $f_\theta$ (never
fine-tuned - an earlier attempt to fine-tune mBERT with a contrastive loss was tried and dropped;
frozen embeddings generalise better at this sample size). 6 backbones evaluated: IndicBERT v2,
mBERT, mT5, EmbeddingGemma-2, LaBSE, MuRIL.
$$e_i^{(p)} = f_\theta(p_i) \in \mathbb{R}^{768}, \qquad e_i^{(b)} = f_\theta(b_i) \in \mathbb{R}^{768}$$
Mask-weighted mean pool of the last hidden state for BERT-style encoders; the model's own
`.encode()` for EmbeddingGemma-2/LaBSE.

**Coherence** - poem embedding alone, standardized, multinomial logistic regression over the 5
rating levels:
$$P(y_i=k\mid z_i)=\frac{\exp(w_k^\top z_i+c_k)}{\sum_{k'}\exp(w_{k'}^\top z_i+c_{k'})},\qquad
\hat y_i=\sum_{k=1}^5 k\cdot P(y_i=k\mid z_i)$$
fit by L2-penalized multinomial cross-entropy, $C=0.003$. Target $y_i$ = the human `bhāvaṃ`
rating (study 1 has no separate coherence question, so the same number is the ground truth for
both Coherence and Adherence there).

**Adherence** - elementwise (Hadamard) product of the two embeddings:
$$x_i^{\text{adh}} = e_i^{(p)} \odot e_i^{(b)}, \qquad x^{\text{adh}}_{i,j} = e^{(p)}_{i,j}\cdot e^{(b)}_{i,j}$$
same model, same $C$. This is a **learnable generalization of cosine similarity**: cosine is
$\sum_j \hat e^{(p)}_j\hat e^{(b)}_j$, the same per-dimension products with *uniform, untrained*
weights; the logistic model computes $\sum_j w_j\,e^{(p)}_{i,j}e^{(b)}_{i,j}$ instead, with $w_j$
fit to the human ratings - dimensions that carry real alignment signal get up-weighted, noisy ones
down-weighted.

**Why not cosine - measured directly**, same data, same CV:

| backbone | cosine + Linear | cosine + Logistic | learned-sim + Logistic (used) |
|---|---|---|---|
| IndicBERT v2 | 0.197 | 0.181 | 0.665 |
| mT5 | 0.169 | 0.171 | 0.668 |
| MuRIL | 0.153 | 0.146 | **0.671** |
| mBERT | 0.169 | 0.192 | 0.629 |
| EmbeddingGemma-2 | 0.031 | 0.010 | 0.635 |
| LaBSE | −0.147 | −0.092 | 0.620 |

The gain is almost entirely the feature (cosine → elementwise product: +0.42 to +0.59 r), not the
classifier (Ridge → Logistic on the same feature: a further +0.01-0.03 only).

**Why multinomial Logistic over Ridge regression**: tested directly, same data/CV - Logistic beats
Ridge on every one of 6 backbones for Coherence (+0.01-0.03 r). An ordinal-logit
(proportional-odds) model was also tried and did *worse* than both.

### 3.2 Modeling results and the choice of backbone

5-fold stratified CV × 5 seeds, out-of-fold predictions, 310 pooled (annotator, poem) rows / 116
unique rated poems, group A only (rebuilt from the anonymised `ratings.csv`):

| backbone | Coherence r | Adherence r |
|---|---|---|
| **MuRIL** | **0.664** | **0.671** |
| IndicBERT v2 | 0.656 | 0.664 |
| mBERT | 0.649 | 0.637 |
| LaBSE | 0.646 | 0.632 |
| mT5 | 0.636 | 0.668 |
| EmbeddingGemma-2 | 0.635 | 0.643 |

All 12 (backbone × task): permutation p = 0.001 (0/1000 label-shuffles beat the real model),
bootstrap 95% CI excludes 0 by a wide margin (e.g. MuRIL coherence [0.577, 0.739]).

**MuRIL is the headline model** - it is the only backbone that is simultaneously #1 on Coherence
*and* #1 on Adherence, so it is the one used for every result in §5. (MuRIL is Google's encoder
built specifically for Indian languages, trained with transliteration augmentation across 17
Indian languages including Telugu - unlike the other backbones, which are either general
multilingual or not India-specific.)

(Note: pooling study-2's real ratings into training was tried and abandoned. It raises the
*pooled* r to 0.73-0.80, but that gain is almost entirely between-study separability - study-2
poems cluster at 1-2, study-1 at 3-5 - and *within-study* r actually drops for study 1 and stays
near noise for study 2; it also still gets the study-2 model ranking backwards. So every result
below uses the clean study-1-only model, scored out-of-sample where noted.)

---

## 4. Poetry Fine-tuning

### 4.1 Methodology

Recipe "E6 + T1", the same for every model. **Data**: a crawled corpus of Telugu poems with
meanings; every poem of this project's own four benchmark corpora is held out whole (no
evaluation poem is in the fine-tuning data), leaving 365,680 training poems, of which 300,763
have an engine-confirmed metre and a meaning (the task-T1 pool: metre + bhāvaṃ → poem).
**Stages**: continued pretraining on poem+meaning documents (stage 1), a 6-task multi-task mix -
metre+bhāvaṃ→poem 50%, span infilling 15%, poem→bhāvaṃ 15%, metre→poem 10%, word glosses 10% -
(stage 2), then one pass over the full T1 pool (the T1 phase). **Decoding**: the deterministic
metrical controller is a hard constraint throughout; **v2** adds two lexical layers to it (an
attested-syllable inventory, and a preference among allowed tokens for real words), recovering
most of the real-word cost of the constraint. **Held out**: 183-1,000+ test prompts per model
depending on the evaluation; the paper's grid uses 100 prompts (90 from the four benchmark works,
retold by Gemma-4 26B so no model can recall a seen pairing, + 10 Gemini poems).

Models: **MDLM-120M/523M** (this project's own masked diffusion LMs, trained from scratch on
4.98B/10.49B tokens of Telugu, one token per akṣara), **Nandi-150M** (`FrontiersMind/Nandi-Mini-150M`,
autoregressive, the size-matched AR partner of the 120M), **T5Gemma-2 270M/1B/4B** (`google/t5gemma-2-*`,
encoder-decoder, full fine-tuning for 270M/1B, LoRA r128 for 4B). No memorization in any model,
any mode: 0% of grid poems share a 12-akṣara run with a training poem or copy a line.

### 4.2 Results - the paper's grid (100 prompts, constrained + v2)

| model | in metre | real words | recognized |
|---|---|---|---|
| MDLM-120M fine-tuned | 100% | 81.6% | 63% |
| MDLM-523M fine-tuned | 100% | **85.4%** | 76% |
| Nandi-150M fine-tuned | 100% | 79.1% | 61% |
| T5Gemma-2-270M fine-tuned | 100% | 82.9% | 66% |
| T5Gemma-2-1B fine-tuned | 100% | 82.3% | 72% |
| T5Gemma-2-4B LoRA fine-tuned | 100% | 79.7% | 70% |
| *the 100 source poems* | 53% | 85.7% | 63% |

(Untuned bases, for reference, same grid cell: MDLM-523M 67.0%, Nandi 53.3%, T5Gemma-1B 50.2% real
words - fine-tuning adds 15-30 points on every model.)

**What the results say.** MDLM-523M has the most real words of any fine-tuned model and nearly
matches the source poems (85.4% vs. 85.7%). Encoder-decoders and Nandi learn metrical rhythm far
better unaided than the masked-diffusion models (free vṛtta-line pattern-match 68-77% vs. MDLM-120M's
12%), because left-to-right order itself carries metrical structure that a random-mask objective
has to learn indirectly - but once the deterministic controller is doing the enforcing, that
advantage mostly disappears and the MDLMs keep slightly more real words instead. T5Gemma-2-4B's
LoRA adapter does **not** beat the much smaller full-fine-tuned 1B (val loss 2.003 vs. 1.776) -
scale alone did not help here.

---

## 5. The Final Grid - Every Metric, Every Source

MuRIL's Coherence/Adherence models (§3, refit on all 310 study-1 rows) plus the full poetics
suite and real word resolution (Samvaran's `poetry_metrics/score_sources.py`,
`word_resolution_sources.py` - the actual resolver, not a proxy), on the same sources throughout.
Poetics/resolution figures are medians (a few outlier poems pull means far off: two textbook
examples reach anuprāsa A = 50 and 176) over the **whole** source (study 1's split is rated/unrated
for Coherence/Adherence only - poetics and resolution don't need a human label, so they're reported
once per source, combined).

| source | n | MuRIL coherence | MuRIL adherence | human coherence | human adherence | anuprāsa 3.0 (median) | mādhurya (median) | ojas (median) | prasāda surprisal (median) | caṃdomiti skill (median) | word resolution (real) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Study 1, bhagavatam | 227 | 4.663 | 4.617 | 4.58 | 4.58 | 1.096 | −0.066 | 43.75 | 6.164 | 1.000 | 85.8% |
| Study 1, vemana | 47 | 4.711 | 4.718 | 4.89 | 4.89 | 1.120 | 0.030 | 41.51 | 5.696 | 1.000 | 90.1% |
| Study 1, kuchimanchi | 70 | 4.621 | 4.626 | 4.64 | 4.64 | 1.095 | −0.081 | 41.25 | 6.794 | 1.000 | 86.6% |
| Study 1, reference (textbook) | 72 | 4.601 | 4.629 | 4.67 | 4.67 | 1.083 | −0.093 | 45.16 | 6.257 | 1.000 | 77.7% |
| Study 1, generated (Gemini sample) | 84 | 3.478 | 3.474 | **3.13** | **3.13** | 1.113 | −0.041 | 37.27 | 6.042 | 1.000 | **96.5%** |
| Study 2, mdlm523m_ft | 33 | 4.360 | 4.547 | **1.88** | **1.77** | 1.143 | −0.028 | 37.04 | 6.239 | 1.000 | 85.6% |
| Study 2, t5_1b_ft | 33 | 4.405 | 4.577 | **2.07** | **1.99** | 1.048 | −0.031 | 41.30 | 6.245 | 1.000 | 84.4% |
| Study 2, nandi_ft | 33 | 4.619 | 4.600 | **1.80** | **1.64** | 1.133 | −0.068 | 41.07 | 6.425 | 1.000 | 79.2% |
| Study 2, the 33 golds | 33 | - | - | - | 4.71 | - | - | - | - | - | - |
| Full corpus, bhagavatam | 7,366 | 4.673 | 4.615 | - | - | 1.038 | −0.036 | 43.13 | 5.770 | 1.000 | 86.7% |
| Full corpus, vemana | 1,164 | 4.748 | 4.708 | - | - | 1.000 | 0.030 | 41.51 | 5.593 | 1.000 | 87.2% |
| Full corpus, kuchimanchi | 1,642 | 4.590 | 4.599 | - | - | 1.071 | −0.038 | 39.66 | 6.391 | 1.000 | 88.5% |
| Full corpus, chandassu | 2,532 | 4.657 | 4.685 | - | - | 1.197 | −0.038 | 42.86 | 6.158 | 1.000 | 87.2% |
| Gemini, full set | 246 | 3.675* | 3.584* | only 84 rated, above | only 84 rated, above | 1.188 | −0.026 | 38.30 | 6.307 | 0.963 | **96.1%** |

Caṃdomiti skill = 1.000 everywhere real poets or constrained decoders were measured - not a
coincidence: the benchmark corpora are pre-filtered to validly-metered poems and the fine-tuned
models write under a hard metrical controller, so both are in metre by construction. The one
exception is the Gemini set (0.963, median) - these are free zero-shot generations under no
metrical controller, so a few fall slightly short of their declared meter, which the deterministic
caṃdomiti metric correctly catches.

**Study 2 vs. the gold poems of the same 33 prompts** (Samvaran's `reports/sources.md`,
`reports/word_resolution_sources.md`; mean difference, model minus gold):

| model | anuprāsa 3.0 Δ | mādhurya Δ | ojas Δ | prasāda surprisal Δ | word resolution Δ (points) |
|---|---|---|---|---|---|
| mdlm523m_ft | +0.600 | −0.007 | −3.307 | +0.223 (more obscure) | −2.0 |
| t5_1b_ft | +0.140 | −0.030 | −0.229 | +0.386 (more obscure) | −3.2 |
| nandi_ft | −0.054 | −0.067 | −0.568 | +0.630 (more obscure) | −8.5 |

**Full-corpus bhāvaṃ note**: Adherence covers 11,656/12,704 full-corpus poems (91.8%) - the
remaining 1,048 are Bhāgavatam sīsamu-parent records whose bhāvaṃ sits on the child record, not
joined here. Bhāgavatam's own bhāvaṃ is the edition's; Vemana/Kuchimanchi/Chandassu's is
machine-generated (`generated.bhavam`, Gemini-3.5-flash-lite), found in every verse record of
those three files.

**What the grid says, read across its columns.** Coherence/Adherence (in distribution: study 1,
full corpus) and the real word-resolution figure agree on the headline finding - Gemini's sample
scores *highest* on word resolution (96.5%, fluent, dictionary-real vocabulary) while scoring
*lowest* on human-judged bhāvaṃ fidelity (3.13) and mid-table on MuRIL's in-distribution
prediction (3.48/3.47) - a direct demonstration that lexical realism and semantic faithfulness are
different axes, exactly the gap Coherence/Adherence exist to catch. On study 2 (out of
distribution for the Coherence/Adherence model), word resolution and the poetics suite rank the
three fine-tuned models consistently with each other (T5Gemma-2-1B and MDLM-523M close together
around 84-86% resolved, Nandi lowest at 79.2% and worst against its own gold by the largest margin,
−8.5 points) - but MuRIL's Coherence/Adherence prediction gets this ranking backwards (Nandi
predicted *highest*), and the real human ratings (1.64-2.07, §2.4) agree with the poetics/
resolution ranking, not MuRIL's. So on study 2, the deterministic poetics+resolution metrics
degraded gracefully and stayed informative; the learned Coherence/Adherence metric, scored
out-of-sample, did not.

---

## 6. Source files

All paths below are relative to this file's directory (`compilation/`). Scripts, training data
and per-poem results for Coherence/Adherence live in `../semantic_coherence/` (its own README
explains the full pipeline); this section just points at them.

| content | file |
|---|---|
| word resolution report (primary source, supplied directly, not committed here) | `word_resolution_report.pdf` |
| study-1 raw ratings | `../human_evals/results/study1/ratings.csv`, `results.md` |
| study-2 raw ratings | `../human_evals/results/study2/ratings.csv`, `results.md` |
| coherence/adherence pooled training data (study 1, anonymised) | `../semantic_coherence/build_dataset.py` → `data/pooled_study1.csv` (gitignored, one command) |
| coherence/adherence CV results | `../semantic_coherence/results/coherence_model_comparison.csv`, `adherence_model_comparison.csv`, `significance_tests.csv` |
| per-poem scores, study-1 rated + unrated | `../semantic_coherence/results/coherence_per_poem.csv`, `adherence_per_poem.csv` |
| per-poem scores, study 2 (out-of-sample) | `../semantic_coherence/results/study2_scores.csv` |
| per-poem scores, full benchmark corpus (MuRIL) | `../semantic_coherence/results/full_corpus_scores_muril.csv`, `score_full_corpus.py` |
| per-poem scores, full Gemini set (MuRIL) | `../semantic_coherence/results/gemini_scores_muril.csv`, `score_gemini.py` |
| fine-tuning READMEs (methodology + full results) | `../diffusion_finetuning/README.md`, `../autoregressive_finetuning/README.md`, `../t5_finetuning/README.md` |
| anuprāsa v3 implementation (integrated, with baseline/tests) | `../poetry_metrics/anuprasa_v3.py`, `baselines/anuprasa_v3_baseline.json`, `tests/test_anuprasa_v3.py` |
| poetics suite, every source (Samvaran) | `../poetry_metrics/score_sources.py`, `outputs/sources/*.json`, `reports/sources.md` |
| real word resolution, every source (Samvaran; resolver code in `../word_resolution_metric/`, database not committed) | `../poetry_metrics/word_resolution_sources.py`, `outputs/word_resolution/*.json`, `reports/word_resolution_sources.md` |
| word-resolution resolver code (database and ByT5 weights not committed; ByT5 released on Hugging Face) | `../word_resolution_metric/` |
| superseded: my preliminary poetics run on study-2 only, proxy word-attestation | `../semantic_coherence/results/study2_poetics.csv` |
| LLM-as-judge pipeline and results | `../semantic_coherence/llm_judge/` |
| human-eval agreement, recomputed from the committed source | `../semantic_coherence/human_eval_agreement.py` |

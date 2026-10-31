# Chandohasam — Compiled Evaluation Results

Compiled 2026-10-31 from primary source files in this repository and in the semantic-coherence
project (`../../Semantic Coherence/` on the author's machine; CSVs referenced below are produced
there and mirrored under `compilation/data/` in this repo — see §5). Every number here is either
read directly from a committed result file or computed fresh from a committed raw-data file by the
scripts listed in each section; none is taken from any earlier draft of the paper.

**⚠ Two different numbers are both called "attestation" in this document — they are not
comparable and must not be read as the same measurement:**

- **§1's 90.78% / 93.00% / 96.27%** come from the real word-resolution system: a 50-dictionary
  headword lexicon + BiLSTM/ByT5 splitter + inflection/sandhi handling + dictionary/glossary
  attestation, run on the separate, much larger **Padyarchana corpus** (382,052 poems). That
  resolver is not available as code/models in this environment, so it was **not** run on anything
  in §4.
- **§4's "ref.-corpus token coverage" (`known_word_share`)** is a *proxy* I substituted because
  of that unavailability: literal exact-string lookup of each word against
  `poetry_metrics/prasada.py`'s own 362,247-poem reference word-frequency table — no headword
  mapping, no inflection stripping, no sandhi splitting. That reference table is also built with
  the §4 corpora (the benchmark's own four files, and anything derived from the same fine-tuning
  pool) **held out of it**, so even a correctly-spelled classical word is penalized for being
  excluded, not for being wrong — §4.3's finding that the real human corpus scores *lower* on this
  proxy (64.5%) than a small fine-tuned model's output (83.7%) is a direct consequence of that, not
  evidence the model is "more correct." This proxy is renamed "ref.-corpus token coverage"
  everywhere below, specifically so it is never misread as the §1 figure.

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
| `paradigm_forms.db` | — (3.4 GB) | every headword's generated inflected forms (the wordform layer) |
| `padyarchana_forms` (glossary, evidence only) | 4,766,005 | editorial + machine glossary of the corpus itself |

Largest constituent dictionaries: వావిళ్ల నిఘంటువు (40,563 definitions), శ్రీహరి (28,810),
శంకరనారాయణ (28,177), శబ్దరత్నాకరము (25,823), బ్రౌణ్య (24,739), విజయ (17,555), తెలుగు నిఘంటువు
(16,380); Sanskrit–Telugu: ఆంధ్ర-సంస్కృత కోశము (14,384); verb-form dictionary క్రియాస్వరూప
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

**Evaluation.** Two independent measures: (a) *coverage* — the token-weighted share of
occurrences in each confidence band, over the whole corpus; (b) *precision* — judged verdicts
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
| random sample, headword level, corpus-wide | 478 judged | — | 0.696, 95% CI [0.65, 0.74] |

Per-poem (382,049 poems): macro mean resolved 0.903, median 0.929; 36.3% of poems fully resolved,
62.1% at 90%+. By glossary layer: human-glossed poems 0.908 resolved, machine-only 0.899.

Lesson for the benchmark: **coverage alone overstates correctness** — roughly a quarter of what's
"resolved" by weak classes is wrong, which is why precision is reported beside coverage throughout
this document rather than coverage alone.

---

## 2. Human Evaluations

Both studies report **group A only** (A1, A3, A5) throughout this document — this is the
project's own committed convention (`human_evals/README.md`): group B (A2, A4) disagreed with
each other (α below 0 on readability, bhāvaṃ, poetic in study 1) and their poem means did not
track group A's.

### 2.1 Study 1 — design

500-poem pool, stratified across 33 canonical metres and verified by the exact metre scanner:
Bhāgavatam 227, Gemini-generated 84, textbook examples 72, Kūcimañci Timmakavi 70, Vemana 47.
Annotators rate blind to source; a 25-poem calibration set first, then a 100-poem phase 1, then
the rest. **Rubric v2**, 12 questions: readability, comprehension, lexical ease, bhāvaṃ-closeness
(1–5); chandassu/prāsa/yati correct (yes/no); śabdālaṅkāra/arthālaṅkāra present (yes/no); poetic
(1–5); register — grānthika/ādhunika (yes/no); AI-generated (yes/no). Live 2026-10-13, rubric v2
from 10-26, complete 2026-10-30.

### 2.2 Study 1 — results, per source

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
| chandassu / prāsa | – (constant) | 100% / 100% yes |
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

### 2.3 Study 2 — design

The three best fine-tuned grid models (MDLM-523M, T5Gemma-2-1B, Nandi-150M), each with the v2
metrical decoder, write the same 33 prompts → 99 poems (`he2_0001`–`he2_0099`). Prompts: study-1
gold poems with ≥4 raters (44 eligible), top-ranked by z(gold's study-1 score) + z(separability);
12 Vemana + 11 Kuchimanchi + 10 Bhāgavatam taken. **Rubric v3** adds Q13, "how meaningful
(coherent) is the poem" — a *separate* question from Q4 bhāvaṃ-closeness. Engine verdicts are
hidden (study 1 showed them); **not blind** — annotators know every poem is model-generated. In
progress: 220/297 possible ratings (80, 79, 62 of 99 for A5/A3/A1) as of 2026-10-31.

### 2.4 Study 2 — results, per model

| model | n ratings / poems | readability | comprehension | lexical | coherence (Q13) | bhāvaṃ | poetic | AI-flagged |
|---|---|---|---|---|---|---|---|---|
| MDLM-523M | 62 / 23 | 3.62 | 2.19 | 3.30 | 1.88 | 1.77 | 1.67 | 99% |
| T5Gemma-2-1B | 84 / 30 | 3.56 | 2.19 | 3.12 | **2.07** | **1.99** | **1.91** | 95% |
| Nandi-150M | 74 / 27 | 3.36 | 2.01 | 3.06 | 1.80 | 1.64 | 1.69 | 95% |
| *the same 33 golds, study 1* | | 4.27 | 3.49 | 4.11 | – | 4.71 | 4.02 | – |

Each model against its own prompt's gold (bootstrap 95% CI, ✱=excludes 0), all three models:
**bhāvaṃ −2.90✱, poetic −2.24✱, comprehension −1.37✱, lexical −0.98✱, readability −0.78✱.**
T5Gemma-2-1B beats the other two on coherence/bhāvaṃ/poetic (+0.25/+0.32/+0.22 vs. the mean of
the other two, CI excludes 0); Nandi trails on the same three; MDLM-523M is within noise of the
mean. Agreement is low (α 0.22–0.28, below 0 on comprehension/coherence/poetic) — most ratings
sit at 1–2.

---

## 3. Semantic Coherence & Adherence — Modeling (Study 1 only, per your instruction)

### 3.1 Definitions

For poem $i$: poem text $p_i$, bhāvaṃ text $b_i$, frozen embedding backbone $f_\theta$ (never
fine-tuned, 6 backbones: IndicBERT v2, mBERT, mT5, EmbeddingGemma-2, LaBSE, MuRIL):
$$e_i^{(p)} = f_\theta(p_i) \in \mathbb{R}^{768}, \qquad e_i^{(b)} = f_\theta(b_i) \in \mathbb{R}^{768}$$
Mask-weighted mean pool of the last hidden state for BERT-style encoders; the model's own
`.encode()` for EmbeddingGemma-2/LaBSE.

**Coherence** — poem embedding alone, standardized, multinomial logistic regression over the 5
rating levels:
$$P(y_i=k\mid z_i)=\frac{\exp(w_k^\top z_i+c_k)}{\sum_{k'}\exp(w_{k'}^\top z_i+c_{k'})},\qquad
\hat y_i=\sum_{k=1}^5 k\cdot P(y_i=k\mid z_i)$$
fit by L2-penalized multinomial cross-entropy, $C=0.003$. Target $y_i$ = the human `bhāvaṃ`
rating (study 1 has no separate coherence question).

**Adherence** — elementwise (Hadamard) product of the two embeddings:
$$x_i^{\text{adh}} = e_i^{(p)} \odot e_i^{(b)}, \qquad x^{\text{adh}}_{i,j} = e^{(p)}_{i,j}\cdot e^{(b)}_{i,j}$$
same model, same $C$. This is a **learnable generalization of cosine similarity**: cosine is
$\sum_j \hat e^{(p)}_j\hat e^{(b)}_j$, the same per-dimension products with *uniform, untrained*
weights; the logistic model computes $\sum_j w_j\,e^{(p)}_{i,j}e^{(b)}_{i,j}$ instead, with $w_j$
fit to the human ratings — dimensions that carry real alignment signal get up-weighted, noisy ones
down-weighted.

**Why not cosine — measured directly**, same data, same CV:

| backbone | cosine + Linear | cosine + Logistic | learned-sim + Logistic (used) |
|---|---|---|---|
| IndicBERT v2 | 0.197 | 0.181 | **0.665** |
| mT5 | 0.169 | 0.171 | **0.668** |
| MuRIL | 0.153 | 0.146 | **0.666** |
| mBERT | 0.169 | 0.192 | **0.629** |
| EmbeddingGemma-2 | 0.031 | 0.010 | **0.635** |
| LaBSE | **−0.147** | **−0.092** | **0.620** |

The gain is almost entirely the feature (cosine → elementwise product: +0.42 to +0.59 r), not the
classifier (Ridge → Logistic on the same feature: a further +0.01–0.03 only).

**Why multinomial Logistic over Ridge regression**: tested directly, same data/CV — Logistic beats
Ridge on every one of 6 backbones for Coherence (+0.01–0.03 r). An ordinal-logit
(proportional-odds) model was also tried and did *worse* than both.

### 3.2 Modeling results (study 1 only)

5-fold stratified CV × 5 seeds, out-of-fold predictions, 305 pooled (annotator, poem) rows / 116
unique rated poems:

| backbone | Coherence r (ρ) | Adherence r (ρ) |
|---|---|---|
| MuRIL | 0.657 (0.465) | 0.666 (0.455) |
| IndicBERT v2 | 0.657 (0.452) | 0.665 (0.464) |
| LaBSE | 0.643 (0.491) | 0.620 (0.438) |
| mBERT | 0.640 (0.494) | 0.629 (0.467) |
| mT5 | 0.625 (0.440) | **0.668** (0.458) |
| EmbeddingGemma-2 | 0.628 (0.441) | 0.635 (0.441) |

All 12: permutation p = 0.001 (0/1000 label-shuffles beat the real model); bootstrap 95% CI
excludes 0 by a wide margin (e.g. IndicBERTv2 coherence [0.556, 0.738]).

(Note, explicitly per your instruction: pooling study-2's real ratings into training was tried and
abandoned for the numbers used here. It raises the *pooled* r to 0.73–0.80, but that gain is
almost entirely between-study separability — study-2 poems cluster at 1–2, study-1 at 3–5 — and
*within-study* r actually drops for study 1 (to 0.48–0.58) and stays near noise for study 2
(0.04–0.26); it also still gets the study-2 model ranking backwards. So §4 below uses the clean
study-1-only model, scored out-of-sample on study 2.)

---

## 4. Automatic Scoring — Study 1 Rated, Study 1 Unrated, and the Entire Study 2

The study-1-only Coherence/Adherence models (§3) refit on all 305 pooled rows, scored on every
poem of each pool (clipped to [1, 5], expected-value scoring, mean over the 6 backbones below
unless a backbone is named).

### 4.1 Study 1 rated (n=116) — per source, with correlation

Correlation against the true human mean is the CV result of §3.2 (r = 0.625–0.657 Coherence,
0.620–0.668 Adherence, all backbones, all p=0.001).

| source | n | Coherence (avg of 6 backbones) | Adherence (avg of 6 backbones) |
|---|---|---|---|
| bhagavatam | 35 | 4.598 | 4.561 |
| generated (Gemini) | 21 | **3.384** | **3.352** |
| kuchimanchi | 20 | 4.505 | 4.563 |
| reference | 20 | 4.604 | 4.628 |
| vemana | 20 | 4.731 | 4.744 |

### 4.2 Study 1 unrated (n=384) — per source

No ground truth exists for these poems (held out of annotation); scores below are model
predictions only.

| source | n | Coherence (avg of 6 backbones) | Adherence (avg of 6 backbones) |
|---|---|---|---|
| bhagavatam | 192 | 4.649 | 4.619 |
| generated (Gemini) | 63 | **3.599** | **3.638** |
| kuchimanchi | 50 | 4.560 | 4.613 |
| reference | 52 | 4.584 | 4.618 |
| vemana | 27 | 4.611 | 4.667 |

Every source split (rated and unrated alike) cleanly separates Gemini-generated poems
(≈3.1–3.7) from all four human-authored sources (≈4.5–4.9) — the single most consistent signal
across the whole embedding approach.

### 4.3 Study 2, entire pool (n=99) — per model, with out-of-sample correlation and poetics suite

**Correlation of the study-1-only model against the REAL study-2 human ratings** (80 poems
currently rated, group A): this is a genuine out-of-distribution test — the model was never
trained on anything like study 2's generation paradigm.

| backbone | Coherence r (vs. real Q13) | Adherence r (vs. real bhāvaṃ) |
|---|---|---|
| IndicBERT v2 | −0.112 | +0.214 |
| mBERT | −0.187 | +0.103 |
| mT5 | −0.174 | −0.030 |
| EmbeddingGemma-2 | +0.099 | +0.044 |
| LaBSE | +0.042 | −0.061 |
| MuRIL | −0.079 | +0.130 |

**The study-1 model does not generalize to study 2** — correlations are at noise level (some
negative), a sharp contrast with the 0.62–0.67 it achieves in-distribution on study 1.

**Average predicted scores per model (study-1-only model, all 99 poems) vs. real human means (80
rated so far):**

| model | predicted Coherence | predicted Adherence | real coherence (Q13) | real bhāvaṃ |
|---|---|---|---|---|
| MDLM-523M | 4.354 | 4.532 | 1.88 | 1.77 |
| T5Gemma-2-1B | 4.389 | 4.535 | **2.07** | **1.99** |
| Nandi-150M | **4.497** | 4.557 | 1.80 (worst) | 1.64 (worst) |

The model predicts near-ceiling scores for all three (4.35–4.50) against a real human ceiling of
1.6–2.1, and ranks Nandi *highest* when humans rate it *worst* — both the scale and the ranking
are wrong. This is reported as a finding, not smoothed over: the embedding-based metric trained on
study 1 (free/topic-prompted generation, mostly fluent sources) does not transfer to study 2's very
different generation task (bhāvaṃ-reconstruction by small fine-tuned models under a hard metrical
constraint).

**Poetics suite** — new anuprāsa formula implemented exactly as specified:
$$A = \sum_{n=1}^{K} \sum_{g:\,c(g)>1} \frac{n\,(c(g)-1)}{N_c}$$
($g$: a consonant $n$-gram across the whole poem, vowels skipped; $c(g)$: its count; $K$: the
longest repeated $n$-gram; $N_c$: consonant akṣaras in the poem; rubric anchored at the treatise's
own example, $A^*=1.33$: none $<A^*/3\le$ weak $<2A^*/3\le$ marked $<A^*\le$ strong).
Run with mādhurya / ojas / prasāda / caṃdomiti (skill) — the project's own `score_poem` functions
— gated by **ref.-corpus token coverage** (the proxy described in the warning at the top of this
document; `known_word_share` from `prasada.py`'s 362k-poem reference, *not* the full §1 resolver —
do not compare this column to §1's 90.78%/93.00%/96.27%):

| gate | model | n | ref.-corpus coverage | anuprāsa (new) | mādhurya | ojas | prasāda (bits/akṣara) | caṃdomiti skill |
|---|---|---|---|---|---|---|---|---|
| none | MDLM-523M | 33 | 0.837 | 1.818 (strong) | −0.063 | 39.1 | 6.73 (obscure) | 1.000 |
| none | T5Gemma-2-1B | 33 | 0.716 | 1.359 (strong) | −0.086 | 42.1 | 6.89 (obscure) | 1.000 |
| none | Nandi-150M | 33 | **0.639** | 1.164 (marked) | −0.123 | 41.8 | 7.14 (obscure) | 1.000 |
| ≥0.70 | MDLM-523M | 27 | 0.894 | 1.907 | −0.030 | 37.1 | 6.32 | 1.000 |
| ≥0.70 | T5Gemma-2-1B | 18 | 0.884 | 1.188 | −0.023 | 39.2 | 5.91 | 1.000 |
| ≥0.70 | Nandi-150M | 10 | 0.823 | 1.103 | −0.019 | 40.3 | 5.93 | 1.000 |
| ≥0.85 | MDLM-523M | 19 | 0.942 | 1.166 | 0.002 | 36.9 | 5.79 | 1.000 |
| ≥0.85 | T5Gemma-2-1B | 11 | 0.931 | 1.233 | −0.018 | 38.7 | 5.81 | 1.000 |
| ≥0.85 | Nandi-150M | 4 | 0.900 | 1.098 | 0.023 | 39.5 | 5.75 | 1.000 |

caṃdomiti skill = 1.000 for every poem at every gate (expected: all are v2-decoder-constrained,
confirms the controller). MDLM-523M has the highest ref.-corpus coverage and strongest
alliteration; Nandi is weakest on both — but MDLM-523M is only mid-ranked by real humans on
coherence/bhāvaṃ, and Nandi is worst on everything (coverage, alliteration, *and* human ratings
agree on Nandi). Lexical realism (by this proxy) and alliteration density track each other but do
not track human-perceived meaning.

---

## 5. Source files

All paths below are relative to this file's directory (`compilation/`). The Coherence/Adherence
code, training data and results now live as their own subproject, `../semantic_coherence/`
(README there explains the full pipeline); this section just points at it rather than keeping a
second copy.

| content | file |
|---|---|
| word resolution report (primary source, supplied directly, not committed here) | `word_resolution_report.pdf` |
| study-1 raw ratings | `../human_evals/results/study1/ratings.csv`, `results.md` |
| study-2 raw ratings | `../human_evals/results/study2/ratings.csv`, `results.md` |
| coherence/adherence pooled training data (study 1, rebuilt from the anonymised `ratings.csv`, never raw usernames) | `../semantic_coherence/build_dataset.py` → `data/pooled_study1.csv` (gitignored, one command) |
| coherence/adherence CV results (study 1 only) | `../semantic_coherence/results/coherence_model_comparison.csv`, `adherence_model_comparison.csv`, `significance_tests.csv` |
| per-poem scores, study-1 rated + unrated | `../semantic_coherence/results/coherence_per_poem.csv`, `adherence_per_poem.csv` |
| per-poem scores, study 2 (study-1-only model, out-of-sample) | `../semantic_coherence/results/study2_scores.csv` |
| anuprāsa v3 implementation (integrated, with baseline/tests) | `../poetry_metrics/anuprasa_v3.py`, `baselines/anuprasa_v3_baseline.json`, `tests/test_anuprasa_v3.py` |
| poetics suite on study-2 poems | `../semantic_coherence/results/study2_poetics.csv` |
| LLM-as-judge pipeline and results | `../semantic_coherence/llm_judge/` |
| human-eval agreement, recomputed from the committed source | `../semantic_coherence/human_eval_agreement.py` |

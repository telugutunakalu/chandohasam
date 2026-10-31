# human_evals

The human evaluation of the project's poems: two studies in which annotators rate poems with one rubric in the
annotation app, and an LLM judge tested against them. Status 2026-10-31: study 1 is complete (2026-10-30); study 2
is in progress.

| | study 1 | study 2 |
|---|---|---|
| poems | 500 (`human_eval_poems_strict.json`): the poets, textbook examples, Gemini | 99 (`human_eval_poems_study2.json`): three of our fine-tuned models, 33 prompts each |
| questions | 12 (rubric v2) | 13 (rubric v3: + coherence) |
| ratings | 544 by 5 annotators; reported: group A, 310 ratings on 116 poems | 220 by the 3 group-A annotators, on 80 of the 99 poems so far |
| app | `/` | `/study2` |
| results | [`results/study1/`](results/study1/) | [`results/study2/`](results/study2/) |

**Annotators** appear only as codes, A1–A5. The username → code mapping is in `annotation_app/instance/` and never
committed. The user's rule for reporting: **group A (A1, A3, A5) only**. Group B (A2, A4) is counted once and left out
of every result: its two annotators disagreed with each other (α below 0 on readability, bhāvam and poetic), and their
poem means did not follow group A's on bhāvam and poetic (ρ ≈ 0; `annotation_app/state_analysis.py`, 2026-10-29).
All ratings of both groups are in `results/*/ratings.csv`.

## What is where

| what | where | in git |
|---|---|---|
| the poem pools | `human_eval_poems_{strict,relaxed,historical}.json` (study 1; the app uses strict), `human_eval_poems_study2.json` | yes |
| the annotation app | `annotation_app/` ([its README](annotation_app/README.md)): code, `data/` and `data_study2/` (the poems as shown), tests, deploy units | yes |
| the results, with codes | `results/`: every rating, and the reports of both studies and the LLM judge | yes |
| the LLM judge | `llm_judge/` ([its README](llm_judge/README.md)): prompt, runner, comparison, the judge's replies | yes |
| the ratings themselves | `annotation_app/instance/annotations.db`, `annotations_study2.db` (live), with `users.json`, `hosting.env`, `backups/`, `pseudonyms.json` | no |
| reports with usernames | `annotation_app/reports/`, `llm_judge/results/*_vs_human*` | no |

**Bhāvams from the crawled corpus.** 98 of the 500 study-1 poems show a bhāvam taken from the crawled corpus export:
the textbook examples and the Bhāgavatam సీసము heads, which have none in the repo's own corpora
(`annotation_app/data/bhavam_padyarchana.json`, `backfill_bhavam.py`). They are committed as part of what the
annotators rated (user decision 2026-10-31). Study 2's bhāvams are all the grid's retold prompts.

## Study 1: the poets, textbook poems and Gemini

### What we did

1. **The pool** (`build_human_eval_sample.py`, 2026-09-24): 500 poems, stratified across the 33 canonical metres of
   `meter_engine/meters.txt`. Every poem is an exact metre match by the engine's DAG scanner; the strict profile also
   requires prāsa and yati.

   | source | poems |
   |---|---|
   | Pothana's Bhāgavatam (`dataset/`) | 227 |
   | Gemini-generated (`metrics/initial_evals`) | 84 |
   | textbook examples (prosody textbooks) | 72 |
   | Kūcimañci Timmakavi (`dataset/`) | 70 |
   | Vemana (`dataset/`) | 47 |

   The relaxed and historical pools are near-identical draws under looser metre profiles (226 Bhāgavatam poems
   instead of 227, and so on).
2. **The app** (`annotation_app/build_data.py`): each poem with its gaṇa table, the yati and prāsa aksharas marked,
   the engine's ✔ per line, and a bhāvam hidden until question 4. Rating is blind to the source.
3. **The rubric:**
   1. readability;
   2. comprehension on first reading;
   3. lexical (recognising the words);
   4. closeness to the bhāvam;
   5. chandassu correct (yes/no);
   6. prāsa correct (yes/no);
   7. yati correct (yes/no);
   8. a śabdālaṅkāra found (yes/no);
   9. an arthālaṅkāra found (yes/no);
   10. poetic;
   11. grānthika or ādhunika (from rubric v2, 2026-10-26);
   12. AI-generated (yes/no; from rubric v2).

   The 1–5 scales are questions 1–4 and 10.
4. **The order:**
   - a calibration set of 25 poems first, for everyone;
   - then phase 1: 100 poems, 20 per source (`build_active_pool.py`, 2026-10-26);
   - then the rest.
5. **Timeline:**
   - live from 2026-10-13, hosted for the annotators;
   - rubric v2 on 10-26, older ratings served again for questions 11–12;
   - A3's and A5's question-4 answers cleared on 10-29 for a fresh pass (the old ones kept in `annotation_history`);
   - complete on 10-30.

### Results (`results/study1/results.md`: the paper's analysis, group A, frozen snapshot of 2026-10-30)

Group A rated 116 poems; 94 by all three, 6 by two, 16 by one.

**Agreement** (Krippendorff's α, poems with ≥ 2 raters; 95% bootstrap CI over poems):

| question | α | 95% CI | mean | reliability of the mean of 3 |
|---|---|---|---|---|
| readability | 0.33 | 0.20 – 0.45 | 4.24 | 0.60 |
| comprehension | 0.49 | 0.35 – 0.59 | 3.50 | 0.74 |
| lexical | 0.44 | 0.31 – 0.57 | 4.02 | 0.70 |
| bhāvam | 0.43 | 0.26 – 0.56 | 4.36 | 0.69 |
| poetic | 0.34 | 0.20 – 0.46 | 3.75 | 0.61 |
| register (grānthika) | 0.33 | 0.19 – 0.47 | 78% yes | |
| AI-generated | 0.53 | 0.35 – 0.68 | 14% yes | |

The metre questions (5–7) are answered "yes" on nearly every poem: every pool poem is in metre. The alaṅkāra questions
have α ≈ 0.

**Sources** (each annotator's own mean removed; poem means; 95% bootstrap over poems; ✱ = the interval excludes 0):

| question | Gemini − poets | textbook − poets |
|---|---|---|
| readability | **+0.57** ✱ | −0.26 ✱ |
| comprehension | **+0.67** ✱ | −0.35 ✱ |
| lexical | **+0.50** ✱ | −0.47 ✱ |
| bhāvam | **−1.57** ✱ | −0.02 |
| poetic | **−1.00** ✱ | −0.30 |

| mean as rated | Bhāgavatam | Vemana | Kūcimañci | textbook | Gemini |
|---|---|---|---|---|---|
| readability | 3.93 | 4.82 | 3.88 | 3.94 | 4.78 |
| comprehension | 3.27 | 4.28 | 2.97 | 3.10 | 4.13 |
| lexical | 3.89 | 4.77 | 3.48 | 3.55 | 4.54 |
| bhāvam | 4.58 | 4.89 | 4.64 | 4.67 | 3.13 |
| poetic | 4.19 | 3.92 | 3.97 | 3.71 | 3.00 |
| grānthika | 83% (poets) | | | 97% | 48% |
| judged AI | 0.6% (poets) | | | 6.8% | 62% |

- **Gemini's poems** read more easily than the poets' but keep less of their own bhāvam and are less poetic. The
  annotators flag 62% of them as AI (38 of 61 ratings) against 2% of the others; a majority flags 15 of 21.
- **Question 4 is unstable on re-rating.** A5 gave the same answer on 63% of 101 poems (quadratic κ 0.36), A3 on 35%
  of 102 (κ −0.04).
- **Drift:** A5 grows harsher over their ratings (residual against the others −0.3 to −0.8 from the first to the
  second half); A1 grows more lenient on comprehension, lexical and bhāvam (+0.4 to +0.6). See
  `results/study1/drift.md`.

## Study 2: our fine-tuned models' poems

### What we did

1. **The pool** (`annotation_app/build_study2_pool.py`, 2026-10-30; the user's design):
   - the three best fine-tuned grid models, each with the v2 metrical decoder: MDLM 523M, T5Gemma 2 1B and
     Nandi-Mini-150M;
   - 33 prompts, each written by all three, so 99 poems (`he2_0001`–`he2_0099`);
   - AI poems only: the gold poems keep their study-1 ratings.
   - **Choosing the prompts:** the poets' grid prompts whose gold poem has ≥ 4 study-1 raters (44 eligible). Within
     each source they are ranked by z(the gold's annotator-centred study-1 score) + z(the three poems' out-of-fold
     p(real), `../final_report_metrics/separability.py`). The top 12 Vemana, 11 Kūcimañci and 10 Bhāgavatam were
     taken (`results/study2/selection.md`).
2. **The app:**
   - the bhāvam shown is the grid's retold prompt, the one the models wrote from;
   - question 13, "How meaningful (coherent) is the poem?" (1–5), follows question 3;
   - the engine's verdicts are hidden; the gaṇa table stays;
   - a calibration set of 6;
   - the three group-A annotators.
3. **Timeline:** live from 2026-10-30 11:03. As of the last rating (2026-10-30 22:32): A3 79, A5 79, A1 62 ratings.

### Results so far (`results/study2/results.md`, `study2_results.py`)

| model | ratings / poems | readability | comprehension | lexical | coherence | bhāvam | poetic | judged AI |
|---|---|---|---|---|---|---|---|---|
| MDLM 523M | 62 / 23 | 3.62 | 2.19 | 3.30 | 1.88 | 1.77 | 1.67 | 99% |
| T5Gemma 2 1B | 84 / 30 | 3.56 | 2.19 | 3.12 | 2.07 | 1.99 | 1.91 | 95% |
| Nandi-Mini-150M | 74 / 27 | 3.36 | 2.01 | 3.06 | 1.80 | 1.64 | 1.69 | 95% |
| *the 33 golds (study 1, the same annotators)* | | 4.27 | 3.49 | 4.11 | | 4.71 | 4.02 | |

- **Far below the poets on the same prompts.** For each annotator and prompt we took the model poem's rating minus
  that annotator's own study-1 rating of the gold. Averaged over the three models: readability −0.78, comprehension
  −1.37, lexical −0.98, bhāvam −2.90, poetic −2.24, every interval excluding 0. The poems are in metre and readable
  but say little and keep little of the bhāvam.
- **T5Gemma 2 1B is ahead of the other two** on coherence (+0.25), bhāvam (+0.32) and poetic (+0.22), annotator-
  centred and on the same prompts; intervals exclude 0. Nandi trails on the same three. The MDLM is within noise of
  the mean.
- **Agreement is low:** α 0.28 readability, 0.26 lexical, 0.22 bhāvam, and below 0 on comprehension, coherence and
  poetic (`results/study2/agreement.md`). Most answers sit at 1–2, so there is little spread to agree on.
- **Read with care:**
  - not blind: the annotators know every study-2 poem is a model's (95–99% flagged);
  - study 1 showed the engine's verdicts, study 2 does not;
  - the golds were rated with their own bhāvam, the model poems with the retelling;
  - 19 of the 99 poems are not yet rated.

## The LLM judge (`llm_judge/`)

Gemma-4 26B-A4B, served by vLLM, answers the same rubric in the same two turns (questions 1–3, then the bhāvam and
4–12).

- **Admission test:** its scores must follow the annotator-centred human mean as well as the annotators follow one
  another. The paper uses the like-for-like version, in which both are correlated with the same others' means
  (`results/llm_judge/paper_tables.md`, Table 5).

| study 1 (group A) | judge ρ | annotators' ρ (median) | passes |
|---|---|---|---|
| readability | 0.64 | 0.56 | yes |
| comprehension | 0.62 | 0.58 | yes |
| lexical | 0.76 | 0.64 | yes |
| bhāvam | 0.17 | 0.50 | no: it gives 5 to 139 of 148 poems |
| poetic | 0.44 | 0.46 | no |

- **Study 2:** it falls short on every scale, and it rates the model poems far above the annotators (bhāvam 4.4–4.8
  against 1.5–2.0).
- **AI flag:** it flags 90% of Gemini's poems (annotators 62%).
- **Not admissible** for the paper's numbers: Gemma-4 26B also generated grid poems and wrote the retold prompts.

Details: [`llm_judge/README.md`](llm_judge/README.md).

## Scripts

Each script on its own: what it is for, what it reads, what it writes.

| script | purpose | reads | writes |
|---|---|---|---|
| `build_human_eval_sample.py` | Draws study 1's 500-poem pool, stratified over the metres and sources, each poem verified by the DAG scanner, under three compliance profiles | `dataset/*.json`, `metrics/initial_evals/Outputs/chandas_dataset.json`, the prosody textbook examples | `human_eval_poems_{strict,relaxed,historical}.json` |
| `annotation_app/build_data.py` | Turns a pool into what the app shows: gaṇa division, guru/laghu, yati and prāsa positions (static, computed once with `meter_engine`), and each poem's bhāvam | a pool file, `meter_engine`, the corpora's bhāvams | `data/` or `data_study2/` (`poems.json`, `reference.json`) |
| `annotation_app/backfill_bhavam.py` | Finds bhāvams for the pool poems the corpora lack, in the crawled export | the export (not in git) | `data/bhavam_padyarchana.json` |
| `annotation_app/build_active_pool.py` | Picks phase 1's 100 poems (20 per source, calibration included) | `data/`, the study-1 DB (read-only) | `data/active_pool.json` |
| `annotation_app/build_study2_pool.py` | Picks study 2's 33 prompts and 99 poems | the grid's poems and prompts, the study-1 DB (read-only), the separability features | `human_eval_poems_study2.json`, `data_study2/bhavam_overrides.json`, `reports/study2/selection.*` |
| `annotation_app/padya_eval/` | The app (Flask): login, queue, form, reference, admin, agreement statistics (`report.py`, also a CLI with `--study 2`) | `data*/`, `instance/` | `instance/*.db` |
| `annotation_app/run.sh`, `wsgi.py`, `deploy/` | Run the app locally; the gunicorn entry point (both studies); the systemd units of the live deployment | | |
| `annotation_app/phase1_results.py` | Phase 1's results: progress, agreement and source contrasts on the 100 poems | the study-1 DB (read-only copy) | `reports/phase1/` |
| `annotation_app/state_analysis.py` | Agreement, consistency, straight-lining, AI detection, the question-4 re-rating and the group A / B ablation on every study-1 rating | the study-1 DB (read-only copy) | `reports/state/` |
| `annotation_app/study2_results.py` | Study 2's results: progress, agreement, means per model, each model against the others, and against the golds' study-1 ratings | both DBs (read-only copies), `human_eval_poems_study2.json` | `reports/study2_results/` |
| `llm_judge/judge_prompt.py` | Renders the rubric as the judge's two-turn prompt, word for word from `rubric.py`, and validates replies | `annotation_app/data*/` | prompts (stdout or JSONL) |
| `llm_judge/run_judge.py` | Runs the judge on a poem set through an OpenAI-compatible vLLM server, JSON-schema constrained, greedy, resumable | prompts, the server | `llm_judge/results/<model>_<set>.jsonl` |
| `llm_judge/judge_vs_human.py` | The admission test and the yes/no and per-source comparisons, both studies; `--raters` restricts to group A | the judge's replies, both DBs (read-only) | `llm_judge/results/*_vs_human*` (with usernames, gitignored) |
| `publish_results.py` | Copies the current reports to `results/` with codes for usernames, exports every rating, and stops if any name is left | the reports above, `../paper/analysis/human_eval_*.md`, both DBs (read-only) | `results/` |

The paper's own analyses, published here with codes, are `../paper/analysis/human_eval_study1.py` (study 1, group A),
`human_eval_drift.py` (drift and agreement diagnostics) and `llm_judge_vs_human.py` (Table 5).

## Reproduce the results

```bash
cd human_evals/annotation_app
.venv/bin/python study2_results.py          # → reports/study2_results/ (≈ 2 s)
.venv/bin/python state_analysis.py          # → reports/state/ (≈ 3 s; not published)
cd .. && annotation_app/.venv/bin/python publish_results.py      # → results/ (codes; checks no name is left)
```

Each script copies the live databases read-only first; none of them writes to a database.
`publish_results.py` writes one file outside `results/`, the mapping `instance/pseudonyms.json` (mode 0600), when
someone new has rated. The study-1 report comes from the paper's
`../paper/analysis/human_eval_study1.py` (`annotation_app/.venv/bin/python …`), which reads a frozen snapshot.

## Results files

| file | what |
|---|---|
| `results/study1/ratings.csv`, `results/study2/ratings.csv` | every rating (current answers): annotator code, group, poem, metre, source, every question, comments, time, rubric version |
| `results/study1/results.md` | the final study-1 analysis (group A): data, agreement, sources, AI detection, question-4 re-rating, drift |
| `results/study1/drift.md` | agreement and drift diagnostics: α by date, subsets, ceiling, ICC, re-rating stability, pairs |
| `results/study2/results.md`, `.json` | study 2 so far: progress, means per model, model contrasts, gaps to the golds |
| `results/study2/agreement.md`, `.json` | study 2's agreement statistics, Q13 included |
| `results/study2/selection.md`, `.json` | how the 33 prompts were chosen |
| `results/llm_judge/paper_tables.md` | the paper's judge tables (both ρ tests; Table 5 is the like-for-like one) |
| `results/llm_judge/gemma4-26b_vs_human*.{md,json}` | `judge_vs_human.py`: the pilot (all raters), group A (`_3raters`), and the paper's run (`_paper`) |

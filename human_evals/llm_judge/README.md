# LLM as judge, on the human-evaluation rubric

`judge_prompt.py` builds the prompt that puts the study's rubric (the 12 questions of
`../annotation_app/padya_eval/rubric.py`, RUBRIC_VERSION 2) to a model, poem by poem, the way the annotation app puts
it to a person. It writes prompts only; it calls no model.

```bash
python3 judge_prompt.py he2_0005                                     # one study-2 poem, printed
python3 judge_prompt.py he_0001 --data ../annotation_app/data        # a study-1 poem
python3 judge_prompt.py --all --out prompts_study2.jsonl             # every poem: {eval_id, system, turn1, turn2}
python3 judge_prompt.py --all --data ../annotation_app/data --out prompts_study1.jsonl
python3 judge_prompt.py he2_0005 --check reply1.json reply2.json     # validate a judge's two replies
```

## The conversation

| message | content |
|---|---|
| system | the role (an expert reader of Telugu verse, one of the study's annotators), the study's own instructions to annotators (the rubric guide's closing note, verbatim), the two-step protocol, JSON only |
| turn 1 (user) | the metre's name; the poem as printed; the engine's reading (gaṇa division, guru/laghu of every akshara, yati and prāsa aksharas); the Rules page as text (this metre's card, guru/laghu, gaṇas, yati maitri, prāsa rules); questions 1–3 |
| turn 2 (user) | the bhāvam; "your answers to 1–3 stand"; questions 4–12 |

Send turn 1, take the reply, then send turn 2 in the same conversation. Each question carries its English and
Telugu text, its scale and anchors, and its guide, exactly as in `rubric.py`. Replies:

```json
{"reasons": {"readability": "<one sentence>", "...": "..."}, "answers": {"readability": 4, "...": 0}}
```

Likert questions take 1–5, the others 0/1 (register: 0 = ఆధునికం · modern, 1 = గ్రాంథికం · archaic); a question
that does not apply is `null` (prāsa when the metre has none, as the app shows it). `check()` / `--check` rejects
anything else.

## Parity with the annotators

| | annotator (app) | judge (this prompt) |
|---|---|---|
| questions, scales, anchors, guides | `rubric.py` | the same, read from `rubric.py` |
| bhāvam | hidden until 1–3 are answered | sent in turn 2, after the turn-1 answers |
| aids | gaṇa table, yati/prāsa underlines, Rules dialog | the same as text |
| engine verdicts (✔, rule names) | study 1 shown, study 2 hidden | hidden; `--show-checks` shows them as study 1 did |
| poem id, source, author, model | never shown | never shown |
| comments | optional free text | one-sentence reason per question (`--no-reasons` drops them) |

Each prompt is ≈ 14k characters (median; the Rules text is most of it).

## Before using its scores (the paper's App. "LLM-judge validation")

- **Judge model:** not a grid generator and not the model that wrote the retellings (Gemma-4 26B did both). Gemini
  wrote 22 of study 1's poems, so a Gemini judge rates its own family's work there.
- **Admit it only if** on the study-1 poems with ≥ 2 human ratings its scores correlate with the annotator-centred
  human means at least as well as the annotators correlate with each other, and it ranks gold poems above
  akṣara-shuffled and bhāvam-mismatched controls (the controls are not built yet).

## Pilot: Gemma-4 26B-A4B-it on vLLM (2026-10-30)

*All annotators; superseded for reporting by the next section, which uses the three raters the user reports.*

`run_judge.py` against the `vllm-judge-gemma4` container (vllm/vllm-openai:gemma-aarch64-cu130, BF16,
`--no-async-scheduling`: with async scheduling this nightly crashes on JSON-schema decoding); temperature 0, reasons on,
engine verdicts hidden. 148 study-1 poems with human ratings + the 99 study-2 poems, 0 invalid replies, ≈ 11 s per
poem at 6 in parallel. `judge_vs_human.py` → `results/gemma4-26b_vs_human.md`:
- 1–5 scales: passes the paper's test (its ρ with the annotator-centred human mean ≥ the median annotator's ρ with
  the others) on readability 0.66 (humans 0.47), comprehension 0.66 (0.50), lexical 0.75 (0.50), poetic 0.53 (0.33);
  fails on bhāvam fidelity 0.20 (0.48): it gives 5 to 139 of 148 poems. Harsher than the annotators on readability
  and comprehension, so α with it added does not rise: use its scores as rankings, not levels.
- Yes/no: metre questions carry nothing (humans ≈ 100% yes, judge 96–100%); śabdālaṅkāra yes on 93% (humans 50%);
  arthālaṅkāra κ 0.18; register κ 0.46; AI flag κ 0.28, but it flags 91% of Gemini's poems (humans 36%).
- Study 2: lower than the poems' golds on every scale (poetic 3.2–3.7 against 4.3); AI flag MDLM-523M 33%,
  T5Gemma 1B 27%, Nandi 9%, golds 0%. The golds were judged with their own bhāvam, the model poems with the retelling.
- Not admissible for the paper's numbers: Gemma-4 26B is a grid generator and wrote the retellings. The controls
  (akṣara-shuffled, bhāvam-mismatched) are not run.

## Gemma-4 26B against the three reported raters (2026-10-30)

The user's rule for reporting human evaluations: the three annotators of group A only (A1, A3, A5; A2 and A4 left
out; codes as in `../results/`). The same judge replies as the pilot, compared with those three raters' current
ratings in both studies:

```
python3 judge_vs_human.py results/gemma4-26b_study1.jsonl --study2 results/gemma4-26b_study2.jsonl \
    --raters "$(cd ../annotation_app && .venv/bin/python -c 'import state_analysis as s; print(",".join(s.GROUP_A))')" \
    --tag 3raters        # → results/gemma4-26b_vs_human_3raters.{md,json} (with usernames: gitignored)
../annotation_app/.venv/bin/python ../publish_results.py   # → ../results/llm_judge/, the same with codes
```

The judge: Gemma-4 26B-A4B-it served by vLLM (setup in the pilot section above), temperature 0, judge_prompt.py's
two-turn conversation (Q1–3, then the bhāvam and Q4–12). Study 2's Q13 (coherence) is not asked of it.

**Study 1** (148 poems judged; 100 with ratings from at least two of the three raters):

| scale | judge ρ with the human mean | median rater ρ (range) | passes |
|---|---|---|---|
| readability | 0.67 | 0.56 (0.46–0.61) | yes |
| comprehension | 0.67 | 0.58 (0.51–0.61) | yes |
| lexical | 0.77 | 0.64 (0.44–0.65) | yes |
| bhāvam (Q4) | 0.21 | 0.50 (0.45–0.61) | **no**: it gives 5 to 139 of 148 poems |
| poetic | 0.47 | 0.46 (0.39–0.61) | yes, barely |

- **Yes/no questions:**
  - AI flag: agreement 0.90, κ 0.68. The raters flag 62% of Gemini's poems, the judge 91%.
  - register: κ 0.39.
  - arthālaṅkāra: κ 0.28.
  - śabdālaṅkāra: κ 0.05; the judge says yes on 93%, the raters on 45%.
  - Metre questions: near-constant yes on both sides.
- **Gemini − poets:**

  | | readability | comprehension | lexical | bhāvam | poetic |
  |---|---|---|---|---|---|
  | raters (centred) | +0.57 | +0.67 | +0.50 | −1.57 | −1.00 |
  | judge | +0.50 | +0.66 | +0.63 | −0.01 | −0.41 |

  The judge follows the raters on the surface scales but does not see the bhāvam gap.

**Study 2** (99 poems judged; 64 rated so far by the three raters, 45 by at least two):

| scale | judge ρ with the human mean | median rater ρ (range) | passes |
|---|---|---|---|
| readability | 0.44 | 0.34 (0.26–0.62) | yes |
| comprehension | 0.49 | 0.38 (0.35–0.58) | yes |
| lexical | 0.51 | 0.56 (0.54–0.63) | no |
| bhāvam (Q4) | 0.12 | 0.59 (0.53–0.62) | **no** |
| poetic | 0.21 | 0.42 (0.37–0.43) | **no** |

- **Levels:** the raters judge our models' poems far below the judge.

  | model | bhāvam, raters / judge | poetic, raters / judge | AI flag, raters / judge |
  |---|---|---|---|
  | MDLM 523M FT | 1.71 / 4.39 | 1.61 / 3.18 | 97% / 33% |
  | Nandi FT | 1.58 / 4.76 | 1.58 / 3.70 | 96% / 9% |
  | T5Gemma 1B FT | 2.06 / 4.61 | 1.77 / 3.46 | 96% / 27% |

  Adding the judge as a rater lowers α on bhāvam (0.35 → −0.22) and poetic (0.06 → −0.27).
- **Yes/no:** AI flag agreement 0.24, κ 0.02; śabdālaṅkāra: judge 81% yes, raters 20%.
- **Caution:** study 2 is still being rated, and the raters themselves agree weakly on some scales (α comprehension
  0.08, poetic 0.06). These numbers will move.

**Verdict:**
- **Where the judge holds up:** readability and comprehension in both studies, lexical in study 1 only.
- **Where it fails, in both studies:** the questions that need judgement against the meaning (bhāvam fidelity), and
  on our models' poems also poetic and AI-likeness. It rates our models' poems as nearly faithful and fairly poetic
  where the raters see neither, which is the failure documented in the pilot: grand-sounding non-words read as
  poetic.
- Not admissible for the paper's bhāvam, poetic or AI numbers.

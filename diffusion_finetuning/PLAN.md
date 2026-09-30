# Fine-tuning plan: Telugu MDLM → metrical poems

Status: plan, 2026-09-29. Nothing here is implemented yet. The open decisions
were answered the same day (§12). Nothing in the plan spends money: every judge
and baseline runs locally.

## 0. Summary

We start from the 120M pretrained masked-diffusion model (`pilot120m`) and teach
it to write a Telugu padyam in a chosen metre from a Telugu meaning (bhāvam).
The meter engines guarantee the form, and the model supplies the language and
the meaning.

| stage | what | where it runs | gate |
|---|---|---|---|
| 0 | Data: labels, group-level splits, dedup, leakage audit, round-trip check | laptop CPU | G0 |
| 1 | Poetic continued pretraining: same objective on poem + meaning documents, 15% general replay | laptop, ~4 h | G1 |
| 2 | Conditional multi-task SFT: meaning → poem is the main task, plus explainer, glosses and infill | laptop, ~5–7 h per run | G2 |
| 3 | Engine-constrained decoding: automaton over syllable weights, prāsa/yati, soft word lexicon, particle search | inference | G3 |
| 4 | Rejection-sampling self-training, with guards against reward hacking | laptop, ~5–6 h per round | G4 |
| — | Evaluation that never reuses a training or reranking signal | laptop; Spark for the 27B judge | — |

The recipe is developed on 120M on the laptop. With the data and evaluation held
fixed, it is then re-run on the grown models (§10).

---

## 1. Starting point (checked 2026-09-29)

### 1.1 Base model

- Preset `small-768`: 120M parameters and a 512-token canvas. It trained for
  76,000 steps (4.98B tokens), mixing Sangraha, IndicCorp and Wikipedia 75/20/5.
- Final validation: NELBO 1.7465 and PPL bound 5.735 per token, where a token is
  about one akshara.
- Samples are well formed locally and incoherent overall:

  | metric | pilot samples | real Telugu | word-shuffled Telugu |
  |---|---|---|---|
  | judge gen-PPL | 63–69 | 16.9 | 64.9 |
  | known-word share | 0.77–0.81 | 0.887 | — |

- Pretraining removed every document that overlapped a known poem, so the base
  model has **not seen classical verse**.
- **Start from the EMA weights** in `runs/pilot120m/ckpt_b.pt`. `mdlm.train
  --init-from` loads the file's `"model"` entry, and in a run checkpoint that
  entry holds the raw weights, not the EMA. Export the EMA first with an
  identity growth:

  ```
  uv run python -m mdlm.grow --from runs/pilot120m --to small-768 --out runs/pilot120m/export/ema_76000.pt
  ```

### 1.2 Tokenizer: one token per akshara

- `telugu_alldomain` has 45,591 entries:

  | kind | count | role |
  |---|---|---|
  | akshara tokens | 44,835 | one token per akshara |
  | digit tokens | 10 | one token per digit |
  | byte tokens | 256 | spaces, punctuation, other scripts |
  | byte-level BPE merges | 485 | spell rare aksharas only |
  | special tokens | 5 | |

- BPE runs inside a single akshara piece and never merges across aksharas.
  Four BPE entries span two aksharas (ఆర్ట, వక్ఫ, హిజ్బ, హమ్ద), but no input
  can ever produce them.
- There are **no multi-akshara (subword) tokens**. On the Bhagavatam verses,
  1,100,046 pieces (aksharas, spaces, punctuation) become 1,102,622 tokens
  (fertility 1.002). The extra 0.2% are rare aksharas spelled out in bytes.
- Consequences for this plan:
  - **A canvas position is not a syllable position.** Spaces, newlines and
    punctuation are tokens of their own, and a line's number of spaces is not
    known in advance.
  - **Syllable weight is pairwise.** A light akshara becomes guru before a
    conjunct or doubled consonant, and that includes across a space or a line
    break (e.g. `లోక ర⏎క్షైకా…`).
  - **New control tokens are possible without new tensors.** 105 embedding rows
    are unused (padded vocab 45,696), so tokens can be added without changing
    tensor shapes. Plain-text headers are enough, so the plan below adds none.

### 1.3 Data

| source | poems | Telugu meaning | word glosses | English | metre |
|---|---|---|---|---|---|
| `padyarchana_exports/padyarchana_poems_v2.jsonl` | 382,052 | 379,825 (edition 168,373; Gemini 376,802) | 2.30M edition rows + 5.64M Gemini rows | — | 384 metre names |
| `dataset/*.json` | 15,415 (12.7k metrical) | edition 9,018 (Bhagavatam); Gemini 5,338 | same split | 14,356 (Gemini run6) | engine-checked |

- **Catalogue coverage.** 317,276 poems (83%) carry a metre name that maps to
  the engine catalogue:

  | metre | poems |
  |---|---|
  | dvipada | 96,732 |
  | kandamu | 84,774 |
  | tetagiti | 33,066 |
  | utpalamala | 26,659 |
  | champakamala | 19,391 |
  | ataveladi | 18,041 |
  | seesamu | 17,284 (+2.3k labelled "సీసము + ettugeeti") |
  | mattebhavikriditamu | 12,241 |
  | sardulavikriditamu | 7,818 |
  | each other catalogue metre | < 500 |

  Outside the catalogue: `Unknown` 34,084, vachanamu 22,012, gītamu 3,235.
- **Two sources dominate.**
  - The modern online Śaṅkarābharaṇam poems make up 31% (118,262): 99,530
    samasyāpūraṇa, 10,837 padya-racana, and 7,895 others. 118,155 of them have
    a meaning.
    - In samasyāpūraṇa many poets complete the same given line. 31% of these
      poems end in a line shared with ≥ 5 other poems; the largest group shares
      one line across 232 poems.
    - Metres: kanda 36.9k, tēṭagīti 17.2k, utpalamāla 12.8k, āṭaveladi 9.7k,
      campakamāla 5.6k, mattēbha 3.2k, śārdūla 2.9k, `Unknown` 28.7k.
  - Dvipada makes up 25.3%.
- **Lengths**, from a 3% sample (11,527 poems) measured with our tokenizer:

  | part | p50 | p95 | p99 |
  |---|---|---|---|
  | poem | 66 | 195 | 245 |
  | meaning | 111 | 272 | — |
  | poem + meaning + headers | 192 | 480 | 613 |

  The poems total about 29M tokens. 3.5% of poem + meaning pairs exceed 512
  tokens.
- **Overlap.** `dataset/*.json` is contained in Padyarchana. For example, all
  10,066 Bhagavatam poems are in it.
- **Engine reliability.**
  - Metre identification agrees with the corpus label on 99.86% of the 7,317
    catalogue-labelled Bhagavatam poems.
  - Yati and prāsa are weaker; the recorded yati baseline is 270/300.
  - Stage 0 re-measures all three on the new splits.

---

## 2. What was wrong with the first draft, and the fix

| # | flaw | consequence | fix |
|---|---|---|---|
| 1 | It assumed canvas position = syllable. | Spaces and punctuation are tokens, so a fixed per-position layout cannot exist. Jāti and upajāti metres (kanda, dvipada, āṭaveladi, tēṭagīti, sīsa; 79% of catalogue poems) also have variable syllable counts. | Decode each line left to right against an automaton over syllable weights. Separators do not advance the automaton, and variable-length metres come for free (§6). |
| 2 | It gave each token a fixed weight. | A light akshara before a conjunct is guru, so per-token masks are wrong. | Carry a "pending weight" in the constraint state and resolve it when the next onset is chosen (§6.2). |
| 3 | It invented a decoding layout the model never trained on. | EXP-18: the model ignores layouts it has not seen. | Decode in the natural text layout used in training. Any other layout (§6.7) must be trained in Stages 1–2. |
| 4 | It split train and test by poem. | 99.5k samasyāpūraṇa poems share their given line, the same poem appears in several editions, and the test poems sit inside Padyarchana. | Split by group, remove 8-gram near-duplicates, and audit leakage (§3.2). |
| 5 | It used the model's own poem → meaning likelihood both to rerank and to evaluate. | That is circular: the metric rewards what the reranker already optimised. | Evaluation uses only engines, external judges and people (§8). |
| 6 | It measured known-word share against a modern-prose lexicon. | Archaic and sandhi-joined forms get penalised. | Poetic word forms from the 7.9M gloss rows go into a soft decoding lexicon (§6.3). Evaluation uses a separate lexicon plus a hand-checked non-word audit, always next to the real-poem ceiling (§8.2, §8.3). |
| 7 | It treated the engines as ground truth. | Yati accepts about 90% of gold poems, so hard constraints would forbid legitimate text, and pass rates would have no ceiling to compare against. | Constrain with the relaxed profiles, report with the strict ones, and always report next to the real-poem ceiling (§6.4, §8). |
| 8 | It trained only full-bhāvam → poem. | A bhāvam is a near-paraphrase, so this teaches versification, while users give short briefs. | Paid brief generation was declined. v1 is scoped as versification from a full meaning, and short prompts are out of scope until free briefs exist (§5.1). |
| 9 | It ignored where meanings come from. | 99% of meanings are Gemini-written, and testing on them rewards Gemini's style. | Tag the meaning source in the header, and test on edition meanings (§5.1, §8.1). |
| 10 | It sampled all data uniformly. | Dvipada (25%) and online Śaṅkarābharaṇam (31%) would dominate metre and register. | Cap dvipada. Use Śaṅkarābharaṇam in full, as decided, but tag each poem's register and give shared samasya lines as a condition so they are not memorised (§3.4, §5.1). |
| 11 | It reused pretraining's EMA and learning-rate settings. | EMA 0.9999 averages over about 10k steps, longer than the fine-tuning runs themselves. | Set EMA 0.999 and a short re-warm (§4, §5.5). |
| 12 | `--init-from` loads raw weights. | Fine-tuning would start from the noisier non-EMA weights. | Export the EMA first (§1.1). |
| 13 | It had no baseline that tests composition. | Retrieving the nearest training poem is metrically valid and often on topic, which can fake success. | A retrieval baseline is mandatory (§8.4). |
| 14 | Self-training rewarded the reranker score. | The model could copy the meaning's words or write safe, repetitive poems. | Guard copy rate and diversity, audit each round with the external judge, and replay gold data (§7). |
| 15 | It used fixed 512-token canvases for examples of about 200 tokens. | About 60% of compute is spent on padding. | Use length buckets (§5.4). |
| 16 | It truncated meanings that did not fit. | A truncated meaning teaches the model to write content the condition does not contain. | Drop over-length examples from the meaning tasks instead (§5.3). |

---

## 3. Stage 0: data

### 3.1 Normalise and label

- **Normalise** poem and meaning text with the tokenizer's normaliser: NFC, with
  ZWJ/ZWNJ stripped and ఁ attached as in aksharanusarika.
- **Punctuation (decided: strip).**
  - Poem *targets* lose all punctuation, including the line-continuation "-";
    only aksharas, single spaces and newlines remain.
  - Meanings keep their punctuation, since they are conditions.
  - The round-trip check in §3.3 confirms that stripping leaves every poem's
    scansion unchanged.
- **Metre.**
  - Map Padyarchana metre names to the catalogue through its Telugu names.
    "సీసము + తేటగీతి/ఆటవెలది" becomes seesamu with its ettugeeti.
  - Run identification on all 382k poems.
  - Record `metre_status` as one of: `agree`, `engine-only` (the recovered
    `Unknown` poems), `label-only`, `none`.
  - At the Bhagavatam run's speed (7.3k poems in 5 s), all 382k take about 5 minutes.
- **Layout (implemented 2026-09-29).** Every poem is put into one layout: one pāda
  per line, except a sīsa, which keeps its two half-lines.
  - Why the sīsa exception: the yati engine only checks a sīsa printed in
    halves. On 59 Bhagavatam sīsas, yati passed 49 with the halves on separate
    lines and 0 with each pāda on one line.
  - How editions' layouts are repaired, in order:
    1. the printed lines as they are;
    2. the lines split at "|", "।", "॥", " - " and "- ";
    3. for a known metre printed two pādas to a line, every word-boundary split
       (17.7k poems);
    4. a sīsa printed with whole pādas is split at the end of its 4th gaṇa.
- **Prāsa and yati.** Both engines run with the relaxed and strict profiles, on
  eval poems only, at about 1 s per poem. Training poems are optional
  (`--prosody-train`), because sampling does not use their flags. The verdicts
  are cached, so rebuilds reuse them.

### 3.2 Splits (before anything else)

- **Pothana's Bhagavatam is held out completely (decided).** All 10,066 poems,
  their Padyarchana copies (source "శ్రీమదాంధ్ర మహాభాగవతం") and their
  near-duplicates are removed from Stages 1–4, including their glosses. It is
  the best evaluation work we have: edition meanings, English meanings and 99.86%
  engine agreement. Holding it out whole makes every test an unseen-work test.
- **Val:** skandhas 1, 2 and 7. That is 1,049 metrical poems, 908 of them with
  edition meanings. Every development decision is made on val.
- **Test:** all other skandhas: 6,319 metrical poems, 5,412 with edition meanings.
  - A fixed stratified subset of 1,000 is used for routine comparisons.
  - The full set is used for the final report.
  - The `bhavam_en` field is kept for judging.
- **Test-seen (secondary):** the Sabhā and Virāṭa parvams of the Mahābhārata,
  held out from a work that *is* in training. That is 2,242 poems, 1,577 of them
  metrical, all with edition meanings. (Raṅganātha Rāmāyaṇam was not used: it is
  all dvipada.) The gap between Test-seen and Test measures how much the model
  leans on having seen a work.
- **Counts as built.** Each sīsa and its gīti, stored as parent + child in
  bhagavatam.json, is one poem.
  - Val: 906 poems, 891 metrical.
  - Test: 5,411 poems, 5,342 metrical.
  - All of them have edition meanings.
- **Grouping.** Classical works split by (work, kāṇḍa or skandha); online
  samasyāpūraṇa splits by the samasya line, so poems that share a samasya stay
  on one side.
- **Near-duplicates.** Remove any training poem containing ≥ 50% of a
  val/test poem's character 8-grams, or the reverse. This reuses the
  `import_chandassu.py` matcher across all 382k poems.
  - Only **metrical** eval poems are indexed. Short prose formulas of
    Test-seen ("అని మఱియు…") otherwise matched 3,000 unrelated training texts.
  - 2,114 poems dropped. Most are another edition of the Virāṭa/Udyōga parvams
    (1,213) and anthology quotations.
- **Leakage audit.** Hash 20-token windows of test poems and meanings against
  the pretraining token corpus, with the `data_prep/poems.py` fingerprints.
  Report the hits and drop affected test items.
  - Result (2026-09-29): only 3 eval poems occur in the pretraining corpus.
  - 297 Bhagavatam meanings do (≥ 5 of their windows, mostly Sangraha web pages
    carrying the edition's commentary).
  - Rule: those items are excluded from T2 (poem → meaning) reporting and kept
    for T1, since the model saw the prose but not the poem.
  - The 3 poems are excluded everywhere. The list is `data/leakage.json`.

### 3.3 Round-trip check (lesson of EXP-25)

- Every training poem goes through encode → decode → engine.
- Metre identification must survive for ≥ 99.5% of the poems the engine
  accepted before encoding.
- Also run **teacher-forced acceptance**: feed each gold poem token by token
  through the §6.2 constraint state machine. Every gold poem the engine accepts
  must be accepted. If not, the constraints are too strict.

### 3.4 Sampling weights

- **Metre-conditioned tasks** (§5) use only poems with `metre_status ∈ {agree,
  engine-only}`.
- **Dvipada** ≤ 10% of meaning → poem examples.
- **Rare catalogue metres** (< 500 poems) are upsampled at most 5×.
- **Śaṅkarābharaṇam: used in full, no cap (decided 2026-09-29).**
  - That is roughly 35–45% of meaning → poem examples, and more once engine
    labelling recovers its 28.7k `Unknown` poems.
  - Two measures keep it from taking over the output:
    - **Register tag.** Every header carries `శైలి: ప్రాచీన` (classical works) or
      `శైలి: ఆధునిక` (Śaṅkarābharaṇam, a 21st-century online forum). Inference
      defaults to ప్రాచీన; the tag's effect is ablated (§8.5).
    - **Shared samasya lines are given, not learned.** A last line of a
      metrical training poem, at least 12 letters long, shared by ≥ 2
      Śaṅkarābharaṇam poems (`సమస్య: …`) or by ≥ 5 classical poems (a śataka
      makuṭam, `మకుటం: …`), goes into the header. Shorter shared endings are prose
      formulas ("అనిన", "మఱియును") and stay ordinary text.
      As built: 58.4k samasya poems and 4.3k makuṭam poems. In the poem slot it
      is fixed: never masked, no loss. That is what samasyāpūraṇa is, it stops
      the model memorising a line repeated up to 232 times, and it adds a
      "complete a poem around a given line" ability.
    - The same per-token loss mask applies in Stage 1.
- **Stage 1** uses every training poem, including `none` poems and vachanamu,
  because they still carry the classical register.

### 3.5 Outputs

- `diffusion_finetuning/data/stage1/<split>.bin`: packed tokens, the same format
  as pretraining.
- `diffusion_finetuning/data/stage2/<split>.jsonl` plus token arrays with a role
  per token (condition / target / pad).
- `DATA_CARD.md` with every count from this section.

**Gate G0:**
- split report and leakage audit reviewed;
- round-trip ≥ 99.5%;
- teacher-forced acceptance ≥ the engine's own acceptance on the same poems.

---

## 4. Stage 1: poetic continued pretraining

- **Initialisation:** the exported EMA from §1.1.
- **Why continued pretraining, and not the alternatives:**
  - **Poems-only from scratch** would see 29M poem tokens, 0.6% of the pilot's
    5B. That is too little to learn Telugu, and the model has to understand
    modern prose inputs. EXP-26/27 show the pattern: a 39M poem-only model
    restored syllables well but composed 0/30 valid poems.
  - **Redoing base pretraining with poems mixed in** would cost about 2.7
    laptop-days for roughly the effect this stage gets in hours. Revisit it only
    if the base is ever retrained (vocabulary pruning, §13). Then mix in
    non-Bhagavatam poems at 2–5% from the start.
- **Data: poem + meaning documents**, not poems alone.
  - Each document is the header (`ఛందస్సు:`, `శైలి:`, and `సమస్య:` when shared),
    then the poem and its meaning (`భావం: …`), in random order (poem first or
    meaning first).
  - The MDLM objective masks random positions, so these documents teach the
    classical register *and* both directions between poem and meaning before
    Stage 2 specialises.
  - Poems without a meaning, and vachanamu, go in as they are.
  - Documents are packed into 512-token windows as in pretraining, with a
    per-token loss-mask file for the fixed samasya lines (§3.4).
  - About 86M tokens per epoch as built: 367.6k documents.
  - 15% of each batch replays the general corpus (75/20/5) to limit forgetting.
- **Schedule:**
  - 3 epochs plus replay: about 300M tokens, or about 4,600 steps at 65,536
    tokens per step. No more than 3–4 epochs, or the model starts memorising
    poems.
  - Warm up over 200 steps to 1e-4 (a third of the pretraining peak), then
    cosine to 1e-5.
  - EMA 0.999. `--seed` ≠ 0, so batches don't replay the pilot's order.
- **Time:** about 1.3 hours per epoch on the laptop, about 4 hours in total.

**Gate G1:**
- Poem val NELBO clearly below the base model's; general val NELBO up by less than 2%.
- **Infill benchmark** (EXP-09/26 protocol: blank 10/25/50% of syllables in val
  poems) — syllable-weight accuracy and exact recovery, against the 39M realiser
  (97.9% / 90.3% at 25%).
- **Unconstrained metre pass rate** of samples prompted only with a metre
  header. This shows how much metre the model has absorbed on its own.

---

## 5. Stage 2: conditional multi-task SFT

### 5.1 Canvas format and tasks

The headers are plain Telugu, so no new tokens are needed:

```
<bos>ఛందస్సు: ఉత్పలమాల
శైలి: ప్రాచీన                  ← or ఆధునిక (Śaṅkarābharaṇam), §3.4
సమస్య: …                      ← only when the last line is a shared samasya
భావం (గ్రంథం): …              ← or భావం (యంత్రం): for Gemini meanings
పద్యం:
<poem lines>                   ← a given samasya line is fixed here (no loss)
<eos><eos>…                   ← fills the rest of the bucket
```

| task | given → target | share | purpose |
|---|---|---|---|
| T1 | metre + meaning → poem | 40% | the main task (versification) |
| T2 | poem → meaning | 20% | explainer; reranker in §6.5 (never an evaluation metric) |
| T3 | poem → glosses (`పదం = అర్థం` rows) | 10% | archaic vocabulary ↔ modern meaning |
| T4 | gloss meanings → poetic words | 5% | poetic vocabulary for composition |
| T5 | metre + meaning + poem with words/lines masked → the masked spans | 15% | repair and editing, used in §6 for dead ends |
| T0 | metre + empty meaning → poem | 10% | unconditional branch for classifier-free guidance |

- **Why the mix is 40/20/10/5/15/10** (revised 2026-09-29; it was 50/15/10/5/10/10). T2 and T5 each gained 5 points,
  taken from T1.
  - T5 is T1 with part of the poem already given, so meaning → poem training is 55% of examples (T1 + T5).
  - T0 stays at 10% condition dropout for classifier-free guidance.
  - The old mix is kept as an ablation (§8.5).

- **No paid brief generation (decided).** v1 turns a full meaning into a poem.
  If short prompts are wanted later, briefs can be made for free by a local
  model (§8.2 judge candidates) and added as a new task. That would be a
  separate, measured change.

### 5.2 Loss

- **Target region:** masked at rate t ~ U(0,1), and the per-token cross-entropy
  on masked positions is weighted by 1/t. This is the MDLM ELBO restricted to
  the target, as in LLaDA's SFT.
- **Condition tokens** are never masked and carry no loss.
- **The `<eos>` fill** after the poem is part of the target, so the model learns
  where the poem ends.

### 5.3 Length

- Examples longer than 512 tokens (3.5% for T1/T2) are **dropped**, not truncated.
- T3/T4 gloss lists are chunked into canvases ≤ 512 tokens.

### 5.4 Batching

- Length buckets of 128 / 256 / 384 / 512 tokens, each padded with `<eos>` in the target.
  The 128 bucket holds most T0 and T4 canvases.
- RoPE handles shorter canvases, but check it: val NELBO of the same poems in a
  256-token and a 512-token canvas should match within noise.

### 5.5 Hyperparameters (120M)

| setting | value |
|---|---|
| learning rate | sweep 3e-5 / 6e-5 / 1e-4 on val |
| warmup | 100 steps, then cosine to 10% |
| batch | 128 |
| weight decay | 0.1 |
| EMA | 0.999 |
| length | 2–3 epochs over the capped T1 set, early stopping on T1 val loss |

An epoch still means one pass over the T1 set. The measured T1 pool is 299.5k poems,
so an epoch is about 5,850 steps of 128 canvases. That is about 200M tokens with bucket
padding, or about 2.5–3 hours on the laptop. The earlier estimate of 85 minutes assumed
fewer, shorter canvases.
- **Recommended sweep:** one epoch (~2.7 h) per learning rate, then 2–2.5 epochs only
  for the chosen one. That comes to about 13–15 hours.

**Gate G2:**
- T1 val NELBO on the poem below Stage 1's NELBO on the same poems without a
  meaning, i.e. the condition is being used.
- Unconstrained metre pass rate ≥ Stage 1's.
- T2 explanations on val rated by the external judge (§8.2).

---

## 6. Stage 3: engine-constrained decoding

### 6.1 Order

- The condition stays fixed.
- The poem is generated line by line. Within a line, positions are unmasked
  **left to right**, one position per step or a small block followed by a check.
- Later positions stay masked but visible, so every step still sees the whole
  meaning and the remaining space in both directions.
- Once the last line is accepted, the rest of the budget becomes `<eos>`.

### 6.2 Constraint state

The state is compiled from the engines. Per-token features are precomputed as
vectors over all 45.6k tokens: intrinsic weight, onset class (vowel / single
consonant / cluster or doubled), consonant identity for prāsa, and yati-maitri
group. Each step's allowed-token mask is then a few vector operations.

- **Weights and lines.** Use `indic_meter_dawg.prosody.prosodic_automaton(metre)`,
  a minimal DFA over {U, I, ⏎} for whole poems of the metre, including the line
  count.
  - Add the line-final laghu-as-guru relaxation that `identify` uses.
  - Separator tokens (space, punctuation) do not advance the DFA. They are not
    allowed at the start of a line, nor twice in a row.
  - A syllable token is allowed only if some weight reading keeps a path to
    acceptance.
  - A light syllable stays *pending* until the next onset is chosen. A cluster
    onset makes it guru; anything else makes it laghu.
- **Line and poem ends.** Newline is allowed only in states that accept a
  complete line. `<eos>` is allowed only after the last line.
- **Prāsa.** The 2nd syllable of every line must share line 1's prāsa consonant,
  under the relaxed equivalences from `prasa_rules.yaml`.
- **Yati.** The syllable at the yati point must be in maitri with the line's
  first syllable, or prāsa-yati where the metre allows it.
  - The minimal DFA discards gana boundaries, so the yati point needs a
    non-minimised automaton built from `flatten()`, whose states carry the gana
    index.
  - Fallback: check yati when each line closes and let §6.5 resample the line.

### 6.3 Word constraint: soft lexicon

**Why.** Measured on the pilot's `final_eval` samples, 2026-09-29:
- Against a word list built from about 100M training tokens plus the validation
  word list, 85.1% of sampled words are listed, against 94.6% for real test text.
- A hand check of 60 unlisted words found about half real (new inflections,
  compounds, names, words run together) and half non-words.
- So about 7–8% of generated words are non-words.
- Revealing fewer tokens per step barely helps (84.4% → 85.1% from 2 to 0.5
  tokens per step). The errors come from the model, not the sampler.

**Lexicon.** Built only from training-split sources. Bhagavatam is excluded
(§3.2), because its word forms would leak test vocabulary.
- **Prose word forms:** from the pretraining train split, kept if seen ≥ 3
  times. The threshold drops typos.
- **Poem word forms:**
  - the `word` field of the edition and Gemini gloss rows, which keep the forms
    as they stand in the poem, sandhi-joined;
  - the pieces of those rows' `split` field;
  - every word of the training poems.
- **Normalisation:** exactly like poem targets (§3.1): NFC, ZWJ/ZWNJ stripped,
  ఁ attached, punctuation stripped.

**Trie over token ids.**
- Each lexicon word becomes its akshara-token sequence.
- The trie stores, at each node, its children and whether a word may end there.
- The state is the current node. It resets to the root after a space or newline.

**How it is applied at each syllable position:**
- **Soft penalty.** Tokens that continue some lexicon word are unpenalised.
  All others get −λ added to their logit.
- **Word ends.** A separator or newline is unpenalised only at a node where a
  word can end.
- **Compounds and sandhi.** At a word-end node, the next akshara may also start
  a new lexicon word without a space, with a smaller penalty λ₂. This covers
  compounds and space-less joins (e.g. పట్టంకూడా).
  - Vowel sandhi that changes the boundary aksharas (రాముడు + అనె → రాముడనె)
    is covered only where the gloss rows contain the joined form.
- **Soft, not hard.** About half of unlisted generated words are legitimate. A
  hard ban (λ = ∞) would block them and could empty the allowed set when
  combined with the metre constraint. Tune λ and λ₂ on val, with ablations at
  λ ∈ {0, 2, 5, ∞}.
- **With the metre constraint.** The metre constraint is hard and the word
  constraint is soft. If none of the metre-allowed tokens continues a lexicon
  word, the penalty applies to all of them equally, so the metre still decides.
  - Count these **lexicon fallbacks** as a diagnostic.
  - Words that can't be finished inside the metre are left to particle
    resampling (§6.5). The trie doesn't look ahead at weights.

**Coverage check before use (teacher-forced).**
- Run the trie over real poems and measure the share of words it would penalise.
- **Training poems:** close to 0% by construction.
- **Bhagavatam val poems (unseen):** this share shows how many words of a real
  unseen poem the lexicon misses. That is the upper bound on what a hard
  constraint would wrongly block, and it guides λ.

**Keeping evaluation honest.** The decoding lexicon must not be the evaluation
lexicon (§8.2), or decoding with it trivially inflates the metric.

### 6.4 Strictness

- **Constraints** use the relaxed profiles. **Reporting** uses the strict ones.
- An over-strict constraint silently removes legitimate poems. The
  teacher-forced acceptance test in §3.3 is what catches that.

### 6.5 Search

- **Particles.** Decode K particles in one batch (K = 16 to start). This is
  sequential Monte Carlo, as in Loula et al. 2025.
- **Resampling.** After each line, resample particles by the model's constrained
  log-probability of that line.
- **Dead ends.** If no token is allowed, the particle dies, or a T5 infill
  repairs the last word.
- **Choosing the prāsa consonant.** Line 1's prāsa consonant is limited to the
  consonants that are frequent in that metre's corpus. A rare one strands lines 2–4.
- **Final rerank:** T2 reverse likelihood log p(meaning | poem), plus the
  guidance scale.
- **Classifier-free guidance.** logits = uncond + w·(cond − uncond), where uncond
  is the T0 branch (Schiff et al. 2024). Tune w on val.

### 6.6 Diagnostic: allowed mass

- **Allowed mass** is the probability the model puts on allowed tokens before
  masking, averaged over positions.
- Low mass means the constraints are fighting the model, which is the failure
  mode behind EXP-16 (valid form, 41.5% real words).
- Report it for base, Stage 1, Stage 2 and Stage 4, separately for the metre
  constraint alone and for metre + lexicon.
- Report the lexicon fallback rate (§6.3) alongside.

### 6.7 Alternative if G3 fails: slotted layout

- Each syllable slot is followed by a boundary slot holding a space,
  punctuation, or a new "no-boundary" token (one of the spare embedding rows).
- This allows any-order decoding with exact per-slot constraints.
- It must be trained in Stages 1–2 (EXP-18), so it costs a second training run.
  It also roughly doubles poem length, so long sīsa poems together with their
  meanings would no longer fit in 512. Measure how many before choosing it.

**Gate G3** (200 val meanings, K = 16, about 20–30 minutes on the laptop):
- metre pass (engine) ≥ 99%; the constraints make it 100% when the engine and
  the automaton agree;
- prāsa and yati pass (strict) within 5 points of the real-poem ceiling;
- allowed mass ≥ 0.5 (metre constraint alone);
- non-word rate from the §8.2 audit ≤ 3%, against about 7–8% for the
  unconstrained pilot;
- evaluation-lexicon share (§8.2) not below unconstrained decoding;
- lexicon fallback rate reported;
- dead-end rate < 5% of particles.

---

## 7. Stage 4: rejection-sampling self-training

- **Generate:** K = 8 constrained poems for each of 5k training meanings per
  round.
  - Decoding is about 100 sequential forward passes per poem, and a
    bidirectional model has no KV cache.
  - So 5k meanings take about 4–5 hours on the laptop. 20k would take about
    18 hours and belong on the Spark.
- **Keep:** the best candidate by T2 reverse likelihood, if it passes the strict
  engines and all three guards:
  - copy rate (share of the poem's 4-grams that also appear in the meaning)
    ≤ the gold 95th percentile;
  - distinct-2 ≥ the gold 5th percentile;
  - no repeated line.
- **Fine-tune** one epoch at low learning rate on the kept poems plus an equal
  amount of gold data (replay).
- **Repeat** for at most 3 rounds.
- **Stopping rule:** stop when the *external* judge score on val stops improving,
  never on the reranker score.
- **Later option:** diffusion RL (diffu-GRPO, d1) with engine and judge rewards,
  only if rejection sampling plateaus.

**Gate G4:** the judge's meaning score on val goes up, with copy rate and
diversity inside the guards.

---

## 8. Evaluation

### 8.1 Sets

- **Val** (Bhagavatam skandhas 1, 2, 7) is used for every development decision.
- **Test** (the other skandhas) and **Test-seen** are used once per model version.
- **Meaning faithfulness** is judged against edition meanings. Every
  Bhagavatam val/test item has one or is skipped.

### 8.2 Metrics

- **Form:** metre, prāsa and yati pass (strict profiles), each next to the
  real-poem ceiling on the same set.
- **Language:**
  - **Evaluation-lexicon share.** The lexicon comes only from sources the
    decoding lexicon (§6.3) does not use: words of the pretraining val and test
    splits.
    - Poetic forms are rare there, so the absolute value is low for real poems
      too. It is read only next to the real-poem ceiling on the same Bhagavatam
      set.
  - **Non-word audit.** For each system, 100 random words not in the evaluation
    lexicon are labelled real or non-word. A person labels them, or the §8.2
    judge if it validates on a labelled seed set. The non-word rate is the share
    of all words, extrapolated from the audit.
  - Judge gen-PPL.
- **Meaning:**
  - **Round trip, all local and free.** A local instruction model writes a
    bhāvam for the generated poem (the run2/run5 prompt, adapted). It then
    rates it against the input meaning (Telugu) and `bhavam_en` (English) on a
    1–5 rubric.
  - **Embedding similarity** from LaBSE or embeddinggemma-300m (both in the HF
    cache) is reported alongside.
  - **Judge candidates** in the HF cache: gemma-3-27b-it (on the Spark),
    gemma-3-12b-it, gemma-4-E4B-it.
  - **Validate the judge first.** On real val poems, matched and mismatched
    meanings must separate with AUC ≥ 0.9. Use the smallest candidate that
    passes. If none passes, meaning is judged by embeddings and human
    evaluation only.
- **Diversity:** distinct-n, self-BLEU across the K samples, and copy rate from
  the meaning.
- **Human evaluation:** 100 blind items (ours / retrieval / gold / local-LLM
  baseline), rated for metre, meaning and poeticness, in `human_evals/`.

### 8.3 Calibration

Every metric is also computed on real held-out poems (the ceiling) and on
word-shuffled poems (the floor). A number without both references is not
reported.

### 8.4 Baselines

1. **Retrieval:** the training poem in the same metre whose meaning is closest by
   embedding. It is valid by construction, and **our model must beat it on
   meaning**.
2. **Local LLM:** gemma-3-27b-it (or the judge model), few-shot, with engine
   filtering and best-of-N. It is the same kind of baseline as the earlier
   DiffusionGemma experiments.
3. **Earlier results:** DiffusionGemma with hard constraints (EXP-16: 4/4 valid,
   41.5% real words) and the 39M realiser (EXP-27: 0/30 valid).
4. **Base pilot + §6 decoding:** isolates what fine-tuning adds.
5. **Stage 1 only + §6 decoding:** isolates what SFT adds.

### 8.5 Ablations

- Stage 1 on/off, and poems-only vs poem + meaning documents.
- Register tag on/off (and ప్రాచీన vs ఆధునిక at inference).
- Auxiliary tasks T2–T5 off.
- Task mix 40/20/10/5/15/10 (chosen) vs 50/15/10/5/10/10 (original).
- Meaning-source tag on/off.
- Guidance scale.
- K particles.
- Relaxed vs strict constraint profiles.
- Word constraint: off, soft (tuned λ, λ₂), hard (λ = ∞).

---

## 9. Engineering work

| piece | location | notes |
|---|---|---|
| data builder | `diffusion_finetuning/build_data.py` | §3: labels, register tags, samasya groups, splits, dedup, leakage audit, round-trip, Stage 1 documents + loss masks, Stage 2 canvases, data card |
| SFT training | `mdlm/train.py --task sft` (or a thin `diffusion_finetuning/train_sft.py` reusing it) | example canvases with roles, loss on the target, buckets, EMA/LR settings; Stage 1 reads a per-token loss-mask file beside the packed tokens |
| constraint compiler | `diffusion_finetuning/constraints.py` | token feature tables, DFA + pending weight + prāsa/yati state, allowed-mask per step |
| lexicon | `diffusion_finetuning/lexicon.py` | §6.3: build from training-split sources only, trie over token ids, per-step penalty vector, teacher-forced coverage report |
| sampler | `diffusion_finetuning/decode.py` | fixed conditions, left-to-right line decoding, metre mask + lexicon penalty, SMC, guidance, T5 repair |
| evaluation | `diffusion_finetuning/evaluate.py` + local judge prompts | §8, with the calibration built in; no API calls |
| tests | `diffusion_finetuning/tests/` | teacher-forced acceptance, trie accepts every lexicon word, no Bhagavatam-only forms in the lexicon, loss masking, bucket collation, split disjointness |

## 10. Scale-up

With the data, prompts, decoding and evaluation frozen, repeat Stages 1–4 on the
grown 523M model (`grow-1536x16`) on a DGX Spark or a cloud GPU. Compare against
the 120M results on the same test sets. The size ladder beyond that is decided by
whether 523M clears the gates with a margin.

## 11. Timeline (laptop, 120M)

| step | effort |
|---|---|
| Stage 0 | ~1 day of code; ~1 h of compute |
| Stage 1 | ~4 h |
| Stage 2 | ~13–15 h with the learning-rate sweep (1 epoch per point, then 2–2.5 epochs) |
| Stage 3 | ~2–3 days of code (constraint compiler, lexicon trie, sampler); ~20–30 min per 200-meaning evaluation |
| Stage 4 | ~4–5 h of generation plus ~1 h of training per round (5k meanings) |
| money | none: judges and baselines run locally (laptop, or the Spark for gemma-3-27b-it) |

## 12. Decisions (2026-09-29)

1. **No paid brief generation, and no paid services anywhere.** T1b and
   Test-brief are dropped, and judges and baselines are local (§5.1, §8).
2. **Online Śaṅkarābharaṇam poems:** used in full, uncapped (revised 2026-09-29). A register tag and fixed samasya lines apply (§3.4).
3. **Dvipada:** used in the conditional tasks, capped at 10% (§3.4).
4. **Held-out work:** Pothana's Bhagavatam, whole. Val is skandhas 1, 2, 7; Test
   is the rest (§3.2).
5. **Punctuation:** stripped from poem targets (§3.1).

## 13. Tokenizer: why the plan keeps one token per akshara

Measured on 2026-09-29. The scripts are in the session scratchpad; the numbers are
recorded here.

**Merging aksharas into subwords makes the vocabulary bigger, not smaller.** An
akshara-level BPE was trained on 8.7M words of the pretraining mix, with merges
only inside words. It gives:

| merges | vocab | prose val tokens | Bhagavatam poem tokens |
|---|---|---|---|
| 8,000 | 53.6k | −35% | −17% |
| 16,000 | 61.6k | −39% | −21% |
| 32,000 | 77.6k | −42% | −25% |

- **Poems gain half as much as prose.** Their sandhi-joined, archaic word forms
  don't match merges learned from prose.
- **Some of the saving goes back into the output layer.** The bigger vocabulary
  makes it cost more per token: 6 · d · V FLOPs per token, which is already 28%
  of the 120M model's compute.
- **Net compute per unit of text** at 16k merges: about 33% lower on prose and
  about 13% lower on poems.

**What it would cost:**
- Re-pretraining from scratch, because the vocabulary is baked into the pilot and
  into the growth ladder.
- Coarser metre control. Prāsa and yati syllables would often sit inside a token.
  Syllable-level infill and repair also become span-level.

**Shrinking the vocabulary is a different change: pruning rare aksharas.**
- In a 28M-akshara prose sample only 19,610 of the 44,835 akshara tokens occur.
  16,786 types cover 99.99%.
- Poems use even fewer: 4,412 types in 1.1M aksharas.
- Keeping the top 16,384 prose aksharas, plus the poem-only ones, leaves
  essentially nothing to byte fallback.
- The vocabulary would drop to about 17k. At 120M that saves about 22M embedding
  parameters and about 17% of compute per token. At 523M it saves about 8%.
- Pruning keeps one akshara per token. Only the dropped rare aksharas would be
  spelled in bytes.
- It can be applied to the existing model by deleting embedding rows and
  remapping ids, followed by a short continued training.

**Decision:**
- Keep the tokenizer for this plan.
- Consider pruning when the model is grown.
- Treat akshara-BPE as a separate ablation for a future pretraining. First
  measure whether sampling neighbouring aksharas independently costs real words:
  compare known-word share at 1 vs 2–8 tokens revealed per step. That probe takes
  about 5 minutes on a free GPU.

## 14. Implementation status (2026-09-29)

All stages have code: `ft/` (see README.md for the module list and commands; 49 tests).
Nothing has been trained yet; Stage 1 waits for the G0 review.

Where the implementation differs from the text above, or fills in a detail:

- **§6.2 weights.** The rules are the engine's own (`indic_meter_dawg.scansion`).
  - A light syllable stays pending until the next token.
  - A ర-vattu conjunct in the same word, or a conjunct after a space, allows both
    readings, as the engine's vikalpa does.
  - A pāda-final laghu may count as guru.
  - `DecodeConfig(vikalpa=False)` settles pending weights canonically instead (the grids' reading).
- **§6.2 NFA.** Built from `prosody.flatten`; its states carry line, gaṇa and offset.
  - The ettugīti is a second unit, entered through the ⏎ after the sīsa.
  - A sīsa half-break comes exactly at the start of gaṇa 5 and is required: the second half
    cannot start without it (the yati engine needs half-lines; its head is reset there).
  - No pāda may start after the last unit's `padalu` pādas. The couplet metres (dvipada, the
    ragaḍas) chain couplets in the grammar, and an untrained model never chose <eos>.
- **§6.2 prāsa.** The key is the 2nd syllable's consonant cluster, under the relaxed
  equivalences (స~శ, న~ణ, ల~ళ, ర~ఱ, థ~ధ); `DecodeConfig(prasa_relaxed=False)` drops them.
  - The first syllable's bindu must match line 1's (bindu-pūrvaka prāsa).
  - A pollu on a pāda's first akshara fuses into the prāsa onset (PRASA-POS-06: తమ్ + వ reads
    మ్వ). The onsets compared are the fused ones: a later head's pollu must be a prefix of line 1's
    fused onset, and its prāsa akshara supplies the rest.
  - Line 1's prāsa akshara may not be a bare vowel unless the head's pollu supplies the consonant
    (PRASA-SAMA-01: no consonant, no prāsa).
  - Pre-prāsa weight (PRASA-PURVAKSHARA-01, mandatory in every profile; chandohasam passes no
    metre class, so the asama-vṛtta exemption never applies). The prāsa engine counts the head guru
    when it is guru by itself or the prāsa akshara is a conjunct, across a word break too. So with
    a single-consonant prāsa every head matches line 1's; with a conjunct prāsa any head passes.
  - Each pāda head looks one step ahead, so a prāsa syllable can always follow.
  - Random walks through the constraints never dead-end: 140 of 140 across seven
    metres.
- **§6.2 yati (soft), revised 2026-09-29.** Maitri is `ft/yati_oracle.py`: the yati engine's own verdict
  for each syllable token at the seat, in the left context the decoder knows.
  - The context covers the previous syllable's bindu and pollu న/ల, and the printed-text sandhi
    evidence: after ఁ, a word-initial న/య, or a ట/న augment.
  - The profile and sandhi mode are `DecodeConfig.yati_profile` / `yati_sandhi`, relaxed /
    hypothesis by default (§6.4).
  - It equals `yati.check` with the same context (a test compares them). The lexical word context
    is left out, because the word is not written yet; on 919 gold seats, leaving it out never
    accepted what the engine rejected.
  - The yati is checked wherever some live parse puts a seat.
  - Seats are grouped as the yati engine's stanza planner groups them:
    - a half-line metre with two yati points (సీసము) pairs its second seat with the second half's
      first syllable;
    - a fixed vṛtta without ప్రాసయతి and with several seats forms one బహుయతి group, where one
      constituent of a conjunct head must serve every seat (YATI-SY-11), so the decoder carries the
      live constituents from seat to seat;
    - otherwise every seat pairs with the pāda head (మానిని and లయగ్రాహి keep it across their
      half-lines).
  - **Why it changed.** The first version keyed a 505 × 505 table by (first sound, vowel),
    built it with `yati.check`'s default sandhi hypothesis out of context, and widened it with
    pairs gold poems use at least 3 times. It accepted pairs no poem context supports (త–య, త–హ,
    త–బ): 67% of its pairs fail with sandhi off. On the base pilot, even a hard yati penalty then
    left 0 of 18 poems passing strict yati (experiments/pilot_grid/README.md).
  - **Gold agreement, oracle relaxed / hypothesis.** 96.4% (val), 91.7% (test) and 89.5%
    (Test-seen) of yati positions are in maitri; 88.2%, 78.2% and 77.2% of poems have every yati
    in maitri. The engine's corpus ceiling is 90–92%.
  - The penalty weight defaults to 3; a large weight makes it hard.
- **§3.3 teacher-forced acceptance (G0).** 99.7% (val), 99.3% (test), 99.6% (Test-seen)
  of the gold poems the engine accepts. These figures are unchanged by the 2026-09-29 rule fixes: a
  first version of the pre-prāsa rule and of the poem end rejected 26 gold poems the engine accepts,
  and both were relaxed to the engine's reading. `python -m ft.constraints` writes
  `data/constraints_report.json`.
- **§6.3 lexicon.** 3.0M words (2.77M from training poems and glosses, 339k prose
  words seen ≥ 3 times in 100M tokens), 6.7M trie nodes. λ = 2, λ₂ = 0.5.
- **§6.4 search.**
  - SMC resamples when ESS < 0.5 K, not at line ends. Particles reach line ends at
    different steps, so ESS is the natural trigger.
  - A dead particle is dropped at resampling. The T5 repair is not used yet.
  - Guidance is implemented but off by default.
  - About 7 s per poem at K = 16 on the laptop.
- **§6 canvas.** The poem budget per metre is 1.5 × the longest pāda in syllables, plus
  line breaks.
  - A sīsa + gīti with a meaning over ~170 tokens does not fit in 512 tokens (a
    model limit).
  - The samasya / makuṭam line is trained as given but not yet forced during
    decoding.
- **§7 Stage 4.**
  - Rounds default to 1,000 meanings (~2 h of decoding), not 5,000.
  - A round's training set is `data/rft/<round>/records`, trained with
    `--mix '{"T1": 1.0}'`.
- **§8 evaluation.**
  - The retrieval baseline uses TF-IDF over meaning words (no embedding model needed).
  - Judge validation on 60 val poems: direct LaBSE similarity gives AUC 0.88. The LLM
    round trip needs gemma-3-12b/27b-it on the Spark (bf16 does not fit the laptop:
    `accelerate` is not installed, so the model loads on one device).
  - The local-LLM few-shot baseline (§8.4 item 2) is not written yet.

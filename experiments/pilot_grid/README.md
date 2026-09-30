# The base pilot120m on the Gemma decoding grid

**Question.** Under the same grid, constraints and evaluation as the Gemma runs in
[`../runs/`](../runs/README.md), what does our own 120M masked-diffusion model do before any
fine-tuning? Its one-token-per-akshara tokenizer lets the constraint act on single syllables.

**Script:** [`../scripts/pilot_grid.py`](../scripts/pilot_grid.py) (`generate`, `evaluate`, `metrics`).
**Runs:** `2026-09-29/` (first run, the decoder as it was, with workarounds) and `2026-09-29_ft-fixed/` (after the `ft` rule fixes)
- `results.jsonl`: one row per poem, with its engine verdict (`eval`) and per-step statistics (`stats`);
- `run.json`: grid, modes and rule set;
- `metrics.json`: the Table 8 measures for every model, plus judge perplexity;
- `yati_maitri_*.npy`: the pairwise yati tables.

## What is matched, and what is not

| | Gemma grids (`../runs/`) | this run |
|---|---|---|
| grid | 37 metres × T1–T3 × seeds 42, 49, 56, 63, 70 = 555 per mode | same |
| task input | chat prompt: the metre's rules + the topic | the topic as the meaning line of the decoder's canvas. The base pilot cannot read instructions: it is pretrained on poem-free prose. |
| decoder | `metrical_decoder` (not in this repository) | `diffusion_finetuning/ft/decode.py`, with a tracing subclass |
| evaluation | engines, metre forced, strict profile, yati sandhi off; "in meter" = canonical gaṇa ∧ prāsa ∧ yati | same definitions (`evaluate`) |
| word-level measures | attested words (Chandassu-held-out lexicon), single-akshara words, poems repeating a line | same code (`writeups/scripts/compute_generation_metrics.py`) |
| step-level measures | chosen-token log-prob, first choice not allowed, allowed mass, per subword token | same definitions, per akshara (or space) token: comparable across modes, **not** in magnitude across models |
| model size and data | 4B–26B, general | 120M, Telugu prose only |

**Modes.**
- **`free`**: one sample at temperature 0.7, no constraint. Counterpart of `baseline`.
- **`masking`**: one sample at temperature 0.7, no lexicon, with the grids' strict rule set as far as
  the pilot decoder can hold it. Counterpart of `masking_only`.
  - canonical weights (no vikalpa readings);
  - hard prāsa without the relaxed equivalences;
  - hard yati, using the yati engine's strict, sandhi-off pairwise table, checked wherever any live
    parse puts a yati.
- **`own`**: the decoder's defaults (PLAN §6), with no Gemma counterpart:
  - 16 particles, temperature 1.0;
  - soft lexicon (λ = 2, λ₂ = 0.5) and soft yati (weight 3) with the decoder's own table;
  - engine and likelihood rerank.

`metrical_decoder` also has backtracking and hybrid modes. They have no counterpart here; a true
strategy-for-strategy comparison needs a pilot adapter in `metrical_decoder` on the Spark.

## Finding on the way: the decoder's yati table is far too permissive

The first smoke tests did not reach the grids' strict yati:
- with the decoder's default soft yati, **0 of 18** constrained poems passed;
- with a hard yati penalty but the decoder's own table, 3 of 30 passed under the relaxed profile.

The cause is in `ft/constraints.py`. `_maitri_row` builds the pairwise table with
`yati.check(a, b, "relaxed")`, and `check` defaults to `sandhi="hypothesis"`. Out of context, a
sandhi can always be hypothesised, so the table accepts pairs that no poem context supports. The
gold-pair widening (PLAN §14) then adds more.

| pair | strict, sandhi off | decoder table |
|---|---|---|
| త–య | rejected | accepted (YATI-VY-09) |
| త–హ | rejected | accepted (YATI-VY-10) |
| త–బ | rejected | accepted (gold-pair widening) |

| table (505 × 505 yati keys) | share of pairs accepted |
|---|---|
| decoder, widened (relaxed + hypothesis + gold pairs) | 18.6% |
| decoder, base (relaxed, sandhi hypothesis) | 17.6% |
| relaxed, sandhi off | 6.1% |
| strict, sandhi off (the grids' verdict) | 5.8% |

67% of the decoder table's pairs (31,815 of 47,313) are rejected with sandhi off. With the strict
sandhi-off table, canonical weights and "any parse" seats, a smoke test reached 24 of 30 poems in
metre under the grids' strict definition. All 6 failures were seesamu: the decoder resets the yati
head of a sīsa's second half only after a half-break newline, and the model wrote whole pādas on
one line.

**Why it is not simply "use the sandhi-off table".** Real verse needs sandhi. Pōtana's poems pass
strict / sandhi-off yati at 63.6%, and relaxed / hypothesis at 91.4% (the write-up's §5). The fix for
the fine-tuning plan (Stage 3, gate G3) is a context-aware check: grant a sandhi hypothesis only
where the preceding word supports it (`yati.check`'s `prev_dead_*`, `word_*` and `vowel_*`
arguments). That is a decision for the plan; it was not changed here.

## Results of the first run (2026-09-29/, before the `ft` fixes)

All 1,665 poems (3 modes × 555) were generated on the laptop. Scoring files:
- `pilot_grid.py evaluate`: the engine verdicts;
- `pilot_grid.py metrics`: `metrics.json`;
- `copy_diversity.json`: the copying and diversity check below.

The Gemma rows' step-level columns come from `writeups/data/generation_metrics.json`, computed with
the same definitions. Columns marked * are per decoding step: an akshara or space for the pilot, a
subword for Gemma. They compare modes within a model, not magnitudes across models.

| model | mode | in metre (strict) | attested words | single-akshara words | poems repeating a line | judge PPL | chosen-token log-prob* | first choice not allowed* | allowed mass* |
|---|---|---|---|---|---|---|---|---|---|
| pilot120m (base) | free | 0 / 555 | 20.6% | 5.9% | 212 / 555 | 3.5 | -0.55 | — | — |
| pilot120m (base) | masking | 425 / 555 | 31.3% | 21.5% | 273 / 555 | 26.1 | -1.66 | 20.8% | 0.74 |
| pilot120m (base) | own | 15 / 555 | 37.3% | 15.0% | 173 / 555 | 26.6 | -2.34 | 23.8% | 0.71 |
| gemma-4-E4B-it | free | 0 / 555 | 37.9% | 0.4% | 4 / 555 | 30.0 | -0.84 | 22.0% | 0.78 |
| gemma-4-E4B-it | masking | 555 / 555 | 12.4% | 9.2% | 111 / 555 | 24.0 | -2.18 | 31.4% | 0.67 |
| gemma-4-E4B-it | backtracking | 555 / 555 | 13.8% | 9.3% | 119 / 555 | 25.1 | -2.29 | 35.4% | 0.63 |
| gemma-4-E4B-it | hybrid | 555 / 555 | 13.0% | 7.9% | 96 / 555 | 29.2 | -2.34 | 31.9% | 0.66 |
| gemma-4-26B-A4B-it | free | 0 / 555 | 38.4% | 2.0% | 60 / 555 | 19.2 | -0.48 | 24.0% | 0.75 |
| gemma-4-26B-A4B-it | masking | 555 / 555 | 16.6% | 16.1% | 231 / 555 | 12.7 | -1.68 | 21.9% | 0.77 |
| gemma-4-26B-A4B-it | backtracking | 555 / 555 | 20.3% | 12.0% | 168 / 555 | 15.8 | -1.94 | 27.8% | 0.71 |
| gemma-4-26B-A4B-it | hybrid | 555 / 555 | 16.6% | 14.1% | 158 / 555 | 16.5 | -1.87 | 22.8% | 0.76 |
| diffusiongemma-26B-A4B-it | free | 0 / 555 | 34.5% | 4.4% | 14 / 555 | 48.3 | -0.47 | 18.8% | 0.77 |
| diffusiongemma-26B-A4B-it | masking | 555 / 555 | 8.3% | 28.7% | 21 / 555 | 104.3 | -3.84 | 47.2% | 0.49 |
| diffusiongemma-26B-A4B-it | backtracking | 555 / 555 | 8.9% | 25.0% | 12 / 555 | 159.8 | -3.13 | 35.9% | 0.61 |
| diffusiongemma-26B-A4B-it | hybrid | 555 / 555 | 9.7% | 26.5% | 16 / 555 | 84.3 | -3.49 | 47.2% | 0.50 |
| real verse, unseen (Chandassu, 555 poems) | | | 33.3% | 5.6% | | 113.3 | | | |
| the same, words shuffled | | | | | | 149.7 | | | |

**Copying and diversity** (`copy_diversity.json`). A high attested-word share could come from
copying the topic or from repetition, so both are measured.

| model | mode | words copied from the topic | attested words, topic words excluded | type/token per poem | distinct attested words |
|---|---|---|---|---|---|
| pilot120m (base) | free | 8.0% | 17.9% | 0.402 | 183 |
| pilot120m (base) | masking | 2.9% | **37.9%** | 0.502 | **773** |
| pilot120m (base) | own | 3.0% | **42.2%** | 0.577 | **1,404** |
| gemma-4-E4B-it | free / masking | 12.9% / 4.0% | 33.7% / 10.7% | 0.915 / 0.776 | 490 / 323 |
| gemma-4-26B-A4B-it | free / masking | 10.3% / 3.3% | 37.2% / 16.9% | 0.833 / 0.620 | 545 / 375 |
| diffusiongemma-26B-A4B-it | free / masking | 10.0% / 0.2% | 34.4% / 11.5% | 0.826 / 0.870 | 485 / 333 |
| real verse (Chandassu, 555 poems) | | | | 0.975 | |

### What the comparison shows

1. **Free generation: 0 of 555 in metre, as for every Gemma model.** The base pilot rarely
   stops: 459 of 555 poems run out of budget. It is repetitive (type/token 0.40; 212 poems repeat
   a line) and uses fewer real words than Gemma (20.6% attested, against 34.5–38.4%).
2. **Under a matched constraint, the pilot keeps its words; Gemma does not.**
   - Masking cuts Gemma's attested words (topic words excluded) from 33.7–37.2% to **10.7–16.9%**.
     The pilot keeps **37.9%**, which is Gemma's *unconstrained* level. With its own decoder
     (particles and soft lexicon), it reaches 42.2%.
   - It also uses 2–4× more distinct real words (773 and 1,404, against 323–375). Topic copying
     is small (2.9%), so it does not explain this.
   - This is what the one-token-per-akshara design predicts (PLAN §13). The mask removes whole
     syllables, not multi-akshara subwords, so the model can still finish the words it starts.
3. **But its words are fragmented and repetitive.**
   - Single-akshara words make up 21.5% of words in masking mode, against 5.6% in real verse.
   - Type/token is 0.50, against 0.62–0.87 for Gemma masking and 0.975 for real verse.
   - 273 of 555 masked poems repeat a line (Gemma: 21–231).
   - It has form and vocabulary without composition, which is the base model's expected state
     before fine-tuning.
4. **In-metre rates are not comparable, because of the decoder.**
   - Under the grids' strict definition: masking **425 / 555** (76.6%) and own **15 / 555**,
     against 555 / 555 for every `metrical_decoder` mode.
   - Every masking failure is a known rule gap in `ft/`:
     - 69 run out of budget, including every dvipada and ragaḍa poem (60 / 60);
     - 40 fail prāsa: bare-vowel prāsa is allowed (PRASA-SAMA-01, 132 pair violations), and the
       pūrvākṣara weight is not held uniform (PRASA-PURVAKSHARA-01, 20);
     - 14 fail yati: a seesamu's second-half head;
     - 7 fail gaṇa.
   - The own mode's 15 is the soft, over-permissive yati described above: yati strict 33 / 555,
     relaxed 124.
5. **Judge perplexity is not a usable signal on verse.** The Gemma-3-1B judge rates real unseen
   verse at 113.3 and the same verse with shuffled words at 149.7. That is a 1.3× gap, against
   3.8× on prose (16.9 vs 64.9, pilot120m report). Repetitive outputs score far *better* than real
   verse (pilot free 3.5; Gemma-26B masking 12.7). The column is reported, but no conclusion rests
   on it.

**Still needed for a strategy-for-strategy comparison:** a pilot adapter in `metrical_decoder` on
the Spark, which would give an exact strict enforcer plus backtracking and hybrid modes. Also the
five decoder rule gaps above, fixed in `ft/` with tests.


## After the `ft` rule fixes (`2026-09-29_ft-fixed/`)

The rule gaps above were fixed in `diffusion_finetuning/ft/` on 2026-09-29 (49 tests; PLAN §14):
- **Yati.** A new `ft/yati_oracle.py` gives the yati engine's exact verdict for each syllable token in
  the known left context, with a chosen profile and sandhi mode.
  - The seats are grouped as the engine's stanza planner groups them, including బహుయతి constituent
    consistency.
  - A yati is checked wherever some live parse puts a seat.
- **Pādas.** A sīsa half-break is required, and no pāda may follow the last one.
- **Prāsa.** A head's pollu fuses into the prāsa onset; a bare vowel carries no prāsa; the pre-prāsa
  weight is uniform.
- **Budget.** The token budget is 2× the longest pāda.
- **Rule set as configuration.** The matched rule set is now `DecodeConfig` options (`yati_profile`,
  `yati_sandhi`, `prasa_relaxed`, `vikalpa`) instead of workarounds in this script.
- **G0.** Teacher-forced acceptance of gold poems is unchanged: 99.7%, 99.3% and 99.6%.

The free rows are the first run's, since the constraint code does not touch free generation. Both
constrained modes were rerun.

| model | mode | in metre (strict) | attested words | single-akshara words | poems repeating a line | judge PPL | chosen-token log-prob* | first choice not allowed* | allowed mass* |
|---|---|---|---|---|---|---|---|---|---|
| pilot120m (base) | free | 0 / 555 | 20.6% | 5.9% | 212 / 555 | 3.5 | -0.55 | — | — |
| pilot120m (base) | masking | 555 / 555 | 31.1% | 19.7% | 248 / 555 | 28.7 | -1.76 | 22.0% | 0.73 |
| pilot120m (base) | own | 35 / 555 | 38.6% | 17.8% | 173 / 555 | 27.1 | -2.38 | 23.7% | 0.71 |
| gemma-4-E4B-it | free | 0 / 555 | 37.9% | 0.4% | 4 / 555 | 30.0 | -0.84 | 22.0% | 0.78 |
| gemma-4-E4B-it | masking | 555 / 555 | 12.4% | 9.2% | 111 / 555 | 24.0 | -2.18 | 31.4% | 0.67 |
| gemma-4-E4B-it | backtracking | 555 / 555 | 13.8% | 9.3% | 119 / 555 | 25.1 | -2.29 | 35.4% | 0.63 |
| gemma-4-E4B-it | hybrid | 555 / 555 | 13.0% | 7.9% | 96 / 555 | 29.2 | -2.34 | 31.9% | 0.66 |
| gemma-4-26B-A4B-it | free | 0 / 555 | 38.4% | 2.0% | 60 / 555 | 19.2 | -0.48 | 24.0% | 0.75 |
| gemma-4-26B-A4B-it | masking | 555 / 555 | 16.6% | 16.1% | 231 / 555 | 12.7 | -1.68 | 21.9% | 0.77 |
| gemma-4-26B-A4B-it | backtracking | 555 / 555 | 20.3% | 12.0% | 168 / 555 | 15.8 | -1.94 | 27.8% | 0.71 |
| gemma-4-26B-A4B-it | hybrid | 555 / 555 | 16.6% | 14.1% | 158 / 555 | 16.5 | -1.87 | 22.8% | 0.76 |
| diffusiongemma-26B-A4B-it | free | 0 / 555 | 34.5% | 4.4% | 14 / 555 | 48.3 | -0.47 | 18.8% | 0.77 |
| diffusiongemma-26B-A4B-it | masking | 555 / 555 | 8.3% | 28.7% | 21 / 555 | 104.3 | -3.84 | 47.2% | 0.49 |
| diffusiongemma-26B-A4B-it | backtracking | 555 / 555 | 8.9% | 25.0% | 12 / 555 | 159.8 | -3.13 | 35.9% | 0.61 |
| diffusiongemma-26B-A4B-it | hybrid | 555 / 555 | 9.7% | 26.5% | 16 / 555 | 84.3 | -3.49 | 47.2% | 0.50 |
| real verse, unseen (Chandassu, 555 poems) | | | 33.3% | 5.6% | | 113.3 | | | |
| the same, words shuffled | | | | | | 149.7 | | | |

| mode | in metre, strict (grids' definition) | relaxed profile (the plan's constraint profile) | yati strict / relaxed | attested words, topic excluded | distinct attested words | type/token |
|---|---|---|---|---|---|---|
| masking, first run | 425 / 555 | 425 / 555 | 468 / 468 | 37.9% | 773 | 0.502 |
| **masking, after the fixes** | **555 / 555** | **555 / 555** | 555 / 555 | 36.9% | 757 | 0.549 |
| own, first run | 15 / 555 | 121 / 555 | 33 / 124 | 42.2% | 1,404 | 0.577 |
| **own, after the fixes** | **35 / 555** | **313 / 555** | 78 / 314 | 45.6% | 1,451 | 0.587 |

- **Every rule gap is closed.** With the grids' strict rule set, the base pilot's decoder writes all 555
  poems in metre, as `metrical_decoder` does. Every poem finishes; gaṇa, prāsa and yati pass on all
  555.
- **The word-level finding stands.** Under the matched constraint the pilot keeps 36.9% attested words
  (topic excluded), against 10.7–16.9% for Gemma masking, with 757 distinct real words against 323–375.
  Its words are still fragmented (19.7% single-akshara) and repetitive (type/token 0.55; 248 poems repeat
  a line).
- **The own mode is where the plan's design choice shows.** Its yati is soft (weight 3) under the relaxed
  profile, and the untrained model pays the penalty often: 314 of 555 poems pass relaxed yati.
  - The fix raised it from 124, because the penalty now points at the right pairs.
  - A hard yati, or a larger weight, would make it 555, as the masking mode shows. Whether to keep yati
    soft is a decision for the plan (PLAN §6.4).

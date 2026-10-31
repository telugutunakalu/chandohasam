# autoregressive_finetuning — plan (v2)

Fine-tune a small autoregressive (AR) model on the same poems and the same task as our masked diffusion model
(`../diffusion_finetuning/`, E6), and evaluate both identically, so the two families can be compared at a matched size.

- **Status, 2026-10-31:** steps 1–4 done. The final run (`runs/nandi-t1`, step 8,225) is released as
  `nandi-150m-padyam` on huggingface.co/samvaran/chandohasam. [README.md](README.md) has the commands and results.
  Of §12: decisions 1 (the sweep, plus an edge rate of 1.35e-3) and 3 were carried out; control C1 (decision 2) and
  the override split of decision 4 were not.
- **Status, 2026-10-18:** **step 1 done and passed** (`results/step1_checks.md`). **Step 2's speed test done**
  (`results/step2_speed.md`: 12.5k tokens/s compiled, 1.08 h per epoch, 11 GB). **Steps 2–3 queued and running**
  since 12:32 as the user service `nandi-ft` (`run_nandi.sh`): leakage probe (~40 min), the 3-rate sweep (~3.4 h),
  the 3.5-epoch final run (~3.9 h); expected done ~21:00. **Step 4 queued behind it** (user service `nandi-eval`,
  `deploy/nandi_eval_queue.sh`): the E6 evaluation of the final EMA on the MDLM rows' 114 val poems, then
  memorisation; the base model's row (`e6_nandi_base_val`) runs now, beside the training. Step 1's finding changes
  §3 (a length cap) and §6 (partial-byte tokens in the constrained modes; decision 4 in §12).
- **What changed from v1 (2026-10-05):** v1 fine-tuned Gemma-4 E2B/E4B. The user dropped that on 2026-10-18: we
  have the resources neither to fine-tune Gemma nor to pretrain an AR model from scratch. v2 uses
  **FrontiersMind/Nandi-Mini-150M**. §11 lists what else in v1 was out of date and how v2 fixes it.

## Contents

1. [The model](#1-the-model)
2. [What the comparison controls](#2-what-the-comparison-controls)
3. [Data and format](#3-data-and-format)
4. [Steps](#4-steps)
5. [Training details](#5-training-details)
6. [Decoding with metrical_decoder](#6-decoding-with-metrical_decoder)
7. [RLVR (later)](#7-rlvr-later)
8. [Tooling](#8-tooling)
9. [Compute](#9-compute)
10. [Known asymmetries and risks](#10-known-asymmetries-and-risks)
11. [Review of v1: what was out of date](#11-review-of-v1-what-was-out-of-date)
12. [Open decisions](#12-open-decisions)

## 1. The model

`FrontiersMind/Nandi-Mini-150M`, the **base** model (an instruct version exists; we do not use it), revision
`31c8aceaa16e2611a5773bbefc6564db39043370`, pinned (downloaded 2026-10-18; SHA-256 of the weights checked against the Hub).

| | |
|---|---|
| licence | Apache-2.0, not gated |
| pretraining | from scratch, 525B tokens, English + Hindi, Marathi, Tamil, **Telugu**, Kannada, Malayalam, Bengali, Punjabi, Gujarati, Odia. The data mix is not published |
| architecture | decoder-only Transformer: RoPE (θ 1e5), RMSNorm, SwiGLU, grouped-query attention (16 heads, 4 KV), tied embeddings |
| size | hidden 832, MLP 2,496; 16 layers, each used twice (**layer sharing: 32 layer passes per token**); vocabulary 131,072 with **factorised embeddings** (rank 196). **153.4M** unique parameters (25.7M of them the embedding), but compute per token like ~280M |
| context | 2,048 tokens |
| weights | `model.safetensors`, 306.8 MB (bf16) |
| code | custom (`modeling_nandi.py`, `configuration_nandi.py`, `tokenization_nandi.py`): needs `trust_remote_code=True` and is reviewed before running (step 1) |

**Tokenizer** (byte-level BPE, NFC normalisation; measured on 400 E6 val poems and their bhāvams):

| | our akshara tokenizer | Nandi | Gemma-4 (v1) |
|---|---|---|---|
| poems: tokens per akshara-token | 1.00 | **0.80** | 1.02 |
| bhāvams: tokens per akshara-token | 1.00 | **0.59** | 0.73 |
| ఁ | its own token | **its own token** | 3 byte tokens |

- Tokens cut across aksharas (`ప | ుట్ట | ంబ | ుట్ట | శర | ంబున | న్`), as Gemma's did.
- **Two quirks the code must handle:**
  1. **The `<|im_start|>` prefix.** The tokenizer's `__call__` and `encode` both prepend `"<|im_start|> "` to every text, to match the model's pretraining. Encoding a prompt and a poem separately and concatenating the ids would put a stray `<|im_start|>` in the middle. So every example is encoded once, as one string, and the poem span is found by character offsets.
  2. **Byte-level vocabulary entries.** A newline is `Ċ`, a space `Ġ`, and Telugu letters are byte-mapped characters. `metrical_decoder`'s `TokenIndex.from_tokenizer` recognises Telugu tokens by their raw vocabulary text, so it would find none, and no newline token (§6). Also, **1,329 ids are partial UTF-8 characters**: in
     classical poems some byte boundaries fall inside a character (ఱ after a vowel sign, `ూఁ`, `ుంభ`), giving two
     ids that only decode together: 1.1% of held-out poem tokens (§6, §10).

## 2. What the comparison controls

The comparison: **Nandi fine-tuned on meaning → poem** against **our 120M MDLM after E6 and its meaning → poem phase**
(`runs/e6-t1-120m`).

| matched | how |
|---|---|
| poems and split | E6's: train = Padyarchana v3 minus anything inside `dataset/*.json` (365,680 poems); val = Bhagavatam skandhas 1, 2, 7 (906); test = the rest of `dataset/` (10,749); the leaked poems of `data/e6/leakage.json` excluded from evaluation |
| task and prompt | metre + meaning → poem, in E6's T1 layout, the same Telugu text (§3) |
| optimisation | 2,350 optimizer steps per epoch (128 examples per step; one epoch = one pass over the 300,763 T1 poems, as for our T1 phase); a 3-rate sweep, then **3.5 epochs** at the best rate: the same number of meaning → poem examples the MDLM partner saw (2.5 passes inside E6, where T1 was half of 11,748 steps × 128, plus its 1-epoch T1 phase) |
| evaluation | **exactly E6's**: the same held-out poem ids, free + three constrained strategies through `metrical_decoder` (strict profile, same `DecodeConfig`, seed 42), the same report, the same memorisation and copy measures, likelihood in nats per MDLM token |
| size | ~150M against 120M: close, the main reason for choosing Nandi |

| not matched | consequence |
|---|---|
| pretraining | Nandi: 525B multilingual tokens, mix unknown, not decontaminated of our poems. MDLM: ~15B tokens of Telugu prose (the pilot's 5B, then the 523M's 10.5B for that model), decontaminated of ~767k poems. Step 2 measures contamination |
| objective | AR next-token likelihood (exact) against the MDLM's NELBO (an upper bound): AR likelihoods look better by construction; compare generation (step 4) first |
| tokenizer | 0.80 tokens per akshara against 1.00; Nandi's tokens cut aksharas |
| fine-tuning recipe | Nandi: meaning → poem only. MDLM: stage 1 (poem + meaning documents) + six tasks + a meaning → poem epoch. To remove this difference, the optional control C1 (§4, step 3) trains our 120M on meaning → poem alone from its stage 1 |

The comparison therefore answers: *given the same poems, task and evaluation, how does a Telugu-capable AR model of
our size compare with our diffusion model?* With C1 it also separates the recipe from the model family.

## 3. Data and format

**Source:** `../diffusion_finetuning/data/e6/records/{train,val,test}.jsonl` (built by `ft.build_data`, audited:
`DATA_CARD.md`, `leakage.json`). No new split is made, and nothing is decoded from token files (v1 did that for the
old E-series split).

**One example** (T1, the text of `ft.canvas`'s headers):

```
<|im_start|> ఛందస్సు: ఉత్పలమాల
శైలి: ప్రాచీన
[సమస్య: … / మకుటం: …]           (only when the poem's last line is a shared line; given, never a target)
భావం (గ్రంథం): <meaning>          (or భావం (యంత్రం): for a Gemini meaning)
పద్యం:
<poem lines><|endoftext|>
```

- **Encoding:** the whole string is encoded once with the raw `tokenizers` file plus the BOS id (§1, quirk 1). The poem span comes from character offsets.
- **Loss mask:** loss on the poem tokens and the final `<|endoftext|>`, so the model learns where the poem ends. No loss on the header or the meaning. A given shared line carries no loss, as in E6.
- **Which records:** the T1 pool of E6: poems whose metre the engine accepts (`agree` / `engine-only`), that have a meaning (300,763). The same dvipada cap and rare-metre upsampling as `ft.canvas`'s pools, so the draws match E6's.
- **Length:** one example has a median of 150 Nandi tokens (p99 412; meaning ~73, poem ~60, header ~12). A few are far longer (max 2,377, past the 2,048 context): **examples over 1,024 tokens are dropped** (8 of 21,596 measured, 0.04%). (The MDLM's 512-token canvas forced E6 to drop ~3%; the shared evaluation set already excludes those poems.)
- **Batches:** 128 examples per optimizer step, padded to the batch's longest (no packing across examples, so each sees only its own prompt).

## 4. Steps

Each step ends with a check that must pass before the next.

### Step 1: download the model and review its code (CPU, ~1 h)

- Download revision `31c8ace…` into the HF cache, then load with `local_files_only=True` from then on.
- **Read** `modeling_nandi.py`, `configuration_nandi.py` and `tokenization_nandi.py`. Look for: network calls; file writes; layer sharing (are the shared layers the same parameters, so their gradients add up?); the factorised embedding; how padding and attention masks are handled; anything that breaks `torch.compile` or bf16 autocast.
- **Tokenizer checks:**
  - the prefix quirk (§1), and whether `decode` drops the prefix;
  - the newline and space tokens;
  - **coverage:** every Telugu character in the E6 corpus must be producible by whole tokens, not only by partial UTF-8 byte tokens, which the constrained decoder cannot use (§6);
  - **round trip:** encode → decode of 10k training poems gives the same text after NFC.
- **Model checks:** load in bf16 and fp32; logits finite on 10 prompts; generate a few continuations of a Telugu line.
- **Pass:** no network or file access in the custom code; tokenizer coverage ≥ 99.9% of corpus characters; round trip exact.
- **Result (2026-10-18): passed.** No network or file access; round trip 10,000 / 10,000; 99.993% of held-out
  Telugu characters spellable by whole tokens (ఝ, ఙ, ఽ are not: 114 of 11,655 poems); the T1 prompt is a token
  prefix of its example in 21,596 / 21,596 records; 153.4M parameters, tied output, finite logits and gradients,
  right padding exact. Zero-shot, the base model only repeats itself. But **1.1% of the poems' own tokens are
  partial-byte ids** outside the decoder's slice (§6). Details: `results/step1_checks.md`.

### Step 2: leakage probe and real training speed (GPU, ~1 h)

- **Leakage probe** (the base model, zero-shot): for each held-out val and test poem, greedy continuation from its first line. Measure the longest run of aksharas shared with the real poem beyond the prompt.
  - Report the share of poems reproduced for ≥ 12 and ≥ 24 aksharas, by corpus (Bhagavatam, Vemana, Kuchimanchi, chandassu).
  - Run the same probe on the E6 leakage list (the Venugopāla śatakam etc.) as a positive control: those are on the web.
  - Poems the base model reproduces are added to the exclusion list for every model's evaluation, so both families are scored on the same clean set.
- **Zero-shot likelihood:** nats per MDLM token of val poems given their T1 prompt, and of val bhāvams as plain prose. These are the AR counterpart of E1 and the "before" row.
- **Speed:** 50 optimizer steps of the real training loop (bf16 autocast, the real batch shape), with and without `torch.compile`. Record tokens/s and peak memory.
- **Pass:** the speed puts one epoch at ≤ 1.5 h (otherwise revisit batch and compile), and the leakage report is written.

### Step 3: fine-tune meaning → poem on the E6 split, with a 3-rate sweep (GPU, ~4–6 h)

- **Sweep:** learning rates 5e-5, 1.5e-4, 4.5e-4 (×3 apart), 1 epoch each (2,350 steps), from the base model. If the best is at an edge, add one rate beyond it.
- **Selection:** the lowest val loss of the poem given metre + meaning (nats per MDLM token, the E6 selection rule).
- **Final run:** from the base model at the best rate, **3.5 epochs** (8,225 steps). That equals the meaning → poem exposure of the MDLM partner: 2.5 passes inside E6 (T1 half of 11,748 steps × 128 examples) plus its 1-epoch T1 phase. The MDLM also saw related tasks (stage 1's documents; the repair and metre-only tasks); C1 removes that difference.
- **Validation every 250 steps:** the poem given metre + meaning, and given metre only (an empty `భావం:` line) — the AR counterparts of T1 and T0. The gap shows whether the model uses the meaning, as for the MDLM (120M: 2.253 / 2.803).
- **Optional control C1** (GPU, ~1–2 h): our 120M trained on meaning → poem only (`ft.train --stage 2 --mix '{"T1": 1.0}'`) from `runs/e6-s1-120m`, same steps and rate rule. It removes the recipe difference of §2.

### Step 4: evaluate exactly as E6 (GPU + CPU, ~2–3 h)

- **The same poems:** the poem ids of `runs/e6_120m_val/run.json` (11 metres, up to 15 per metre, seed 42), minus any added by step 2's leakage list (and the MDLM rows recomputed on the same reduced set).
- **The same decoding:** `metrical_decoder.run_grid`, modes baseline (free), masking_only, masking_backtrack and hybrid; strict profile; the same `DecodeConfig`; the prompt of §3, ending after `పద్యం:⏎`.
- **The same report:**
  - `metrical_decoder.analysis.report`: in metre; logp; overridden; mass on allowed; real words; single-akshara words; repeated lines;
  - copy rate from the bhāvam (real poems 2.5%);
  - `memorisation.py --train-records ../diffusion_finetuning/data/e6/records/train.jsonl`.
- **Reference rows:** the base Nandi (zero-shot, same prompts); our 120M E6 and E6 + meaning → poem; the 523M E6 and E6 + meaning → poem.
- **Then test:** the same on ~1,000 test poems, for the final numbers.

## 5. Training details

| setting | value | why |
|---|---|---|
| parameters trained | all (full fine-tuning) | 150M fits easily (§9) |
| optimizer | AdamW β (0.9, 0.98), weight decay 0.1, gradient clip 1.0 | as E6 |
| schedule | 100 warm-up steps, cosine to 10% of the peak | as E6's stage 2 |
| batch | 128 examples per step, each drawn with E6's metre weights (rare metres upsampled, dvipada capped at 10%), with replacement; cut into micro-batches of ≤ 8,192 padded tokens by dynamic programming (7.8% padding) | as E6 (2,350 steps per epoch). One epoch of draws covers 58.6% of the distinct examples, the final 3.5 epochs 89.2% (the dvipada cap is most of the gap), exactly as E6 samples |
| precision | bf16 autocast, fp32 weights and optimizer | |
| weights evaluated | an EMA (decay 0.999) of the weights, as E6 evaluates | parity with `ft.train` |
| loss | next-token cross-entropy on the poem tokens + `<|endoftext|>` | |
| reported likelihood | total nats ÷ the poem's tokens in our akshara tokenizer (nats per MDLM token), the unit of E6's NELBO | |
| checkpoints | two slots every 15 min + one per epoch; resume on restart | like the other trainers |
| seed | fixed, recorded | |

## 6. Decoding with metrical_decoder

`metrical_decoder` is shared code, used by running jobs, and is not edited from here. A subclass in this folder adapts it:

- **Loading:** `AutoModelForCausalLM` / `AutoTokenizer` with `trust_remote_code=True` and the pinned revision. `hf.HFCausalLM` passes neither, and resolves the architecture from `transformers`, which has no `NandiForCausalLM`.
- **Token index:** built with `TokenIndex.from_texts`, not `from_tokenizer` (`nandi.token_index`). Every id is decoded with the byte-level decoder; ids whose text is Telugu (an optional leading space included) are kept, plus newline (188) and space (210): 7,394 ids. Partial-UTF-8 ids, which decode to `�`, are excluded. Step 1 found that this costs more than v2 assumed: characters are almost all spellable (99.993%), but **1.14% of held-out poems' canonical tokens, in 31.7% of the poems, are partial ids** (the MDLM's slice misses 0.06%). In the constrained modes those words (mostly ఱ after a vowel sign) must be spelled in a tokenization the model never trained on, and ఝ / ఙ not at all. Step 4 measures the cost: the "overridden" count split into *first choice a partial id* and *first choice broke a rule*. If the first is material, **pair entries** fix it: each partial-id pair seen in training becomes one slice entry with the pair's text, scored log p(a) + log p(b | a) and pushed as two tokens (decision 4).
- **Prompts:** `prompt_ids` returns the §3 prompt for the poem id, encoded as in §3, instead of a chat template.
- **End of poem:** `eos_ids` = `<|endoftext|>` (id 0).
- **Cache:** an ordinary KV cache. Generation is fast; the constrained modes' cost is the masks on the CPU, as for every model.

## 7. RLVR (later)

The reward module of `../diffusion_finetuning/RLVR_PLAN.md` applies unchanged: metre by default with partial credit,
meaning, coherence, word quality, guards. It scores text, not models. For an AR policy, GRPO is the standard
algorithm: the log-probabilities of a sample are exact and cheap (one forward pass), unlike the MDLM's ELBO
surrogate. So the RLVR comparison across families can use the same rewards and the same evaluation. It is planned
there, after step 4 here.

## 8. Tooling

Everything lives in this folder. It reads `../diffusion_finetuning/data/e6/` and imports `metrical_decoder` and
`../diffusion_finetuning/memorisation.py`, without modifying them.

| file | purpose | step |
|---|---|---|
| `nandi.py` ✔ | pinned loading (model + tokenizer, `trust_remote_code`), the one-string encoding with the poem span, the byte-level `TokenIndex`, the `HFCausalLM` subclass | 1, 4 |
| `check_nandi.py` ✔ | the step-1 checks (code review notes, tokenizer coverage and round trip, load, logits, sample generations) | 1 |
| `leakage_probe.py` ✔ | first-line continuation of held-out poems (fp32, batches of equal prompt length: exact); longest shared run; zero-shot likelihoods | 2 |
| `finetune.py` ✔ | meaning → poem training (§5): sweep and final runs, val every 250 steps (T1 / T0), resume | 2 (speed), 3 |
| `run_nandi.sh` ✔ (+ `deploy/nandi-ft.service`) | the chain of steps 2–3 (step 4 to be added), as `run_e6.sh` does for the MDLM: each step resumable, the best rate chosen automatically | 2–4 |
| `constrained_sample.py` ✔ (+ `deploy/nandi_eval_queue.sh`, `nandi-eval.service`) | the E6 evaluation for Nandi: the (metre, poem id) pairs, config, budgets and modes of `../diffusion_finetuning/runs/e6_120m_val`, an `HFCausalLM` subclass with the custom code, the report | 4 |

Not committed: `runs/`, model weights (the HF cache), generated poems. `results/` holds numbers only.

## 9. Compute

Estimates, to be replaced by step 2's measurement. The GB10 has 121.7 GB of unified memory and 20 cores.

| | |
|---|---|
| memory, training | **measured 11.1 GB** (micro-batches of 8,192 tokens; the vocabulary projection only at the loss positions) |
| FLOPs per token, training | ≈ 6 × ~280M ≈ 1.7 GFLOPs (layer sharing doubles the compute of the 16 stored layers) |
| speed | **measured 12.5k tokens/s** compiled (8.9k eager), ~21 TFLOP/s |
| one epoch | 300,762 examples, 42.7M tokens → **1.08 h** measured |
| step 2 | leakage probe ~20–30 min (greedy, cached); speed test ~10 min |
| step 3 | sweep 3 × 1 epoch ≈ 3.4 h; final 3.5 epochs ≈ 3.9 h; **≈ 7.3 h** (+1.1 h if the best rate is at an edge) |
| step 4 | val: ~1.5–2 h (CPU masks dominate, as for E6: 456 poems in ~1.3 h on 4 shards); test ~1,000 poems: ~3–4 h |
| **total** | **~1 day of GPU time** spread over steps 2–4, plus ~1 day of engineering (steps 1, §6, §8) |

It can share the GPU with other work, but the RLVR runs of the MDLM come first when both are ready.

## 10. Known asymmetries and risks

1. **Contamination.** Nandi's pretraining data is unknown, and the held-out works are on the web (the Venugopāla śatakam was found in Sangraha). Step 2 measures it, and contaminated poems leave every model's evaluation set.
2. **Likelihoods are not comparable as levels.** Exact AR NLL is not the MDLM's NELBO bound. Gaps (T1 vs T0) and generation metrics are the comparison.
3. **Recipe.** Meaning → poem only (3.5 epochs) against E6's stage 1, six tasks and one meaning → poem epoch: the same meaning → poem exposure, but the MDLM also learned from related tasks. The control C1 removes this.
4. **Tokens cut aksharas, and sometimes characters.** The constrained decoder handles cut aksharas (as for Gemma), but its masks see more, smaller steps. Overrides and logp are per token: compare per-poem measures (in metre, real words, filler) first. Tokens that cut a character (1.1% of poem tokens) are outside the slice: see §6 and decision 4.
5. **Custom code.** Reviewed in step 1 and pinned. An update of the Hub repo cannot change our runs.
6. **The base model has seen no instruction format.** The first epoch partly teaches the layout. The sweep's 1-epoch runs therefore understate the final run more than for the MDLM, whose stage 1 had already taught the layout.

## 11. Review of v1: what was out of date

| v1 (2026-10-05) | why it was wrong now | v2 |
|---|---|---|
| Gemma-4 E2B/E4B, LoRA, 25 GB download, 25–50 h for E4B | no resources for Gemma fine-tuning (the user, 2026-10-18); 10–30× our size, so not a size match | Nandi-Mini-150M, full fine-tuning, 0.3 GB, ~1 day |
| mirrored E1–E5 on the **old E-series split** (the MDLM's token files) | the diffusion side moved to **E6** on the new split (Padyarchana minus `dataset/`), and E2/E5 trained on today's test poems | E6's records, task and evaluation (§2–§4) |
| E3 grid with 3 fixed topics as prompts | E6 evaluates with **held-out poems' own meanings** | the same poem ids as `e6_120m_val` |
| "Gemma has no ఁ token" as the main decoding asymmetry | Nandi has a ఁ token | replaced by the byte-level vocabulary and prefix quirks (§1, §6) |
| a size-matched control (Gemma-3-270M) and an AR model from scratch, both optional | no resources; Nandi is the size-matched model | dropped |
| matched **passes** (10, as E2) | E6 matches steps per epoch and a 2.5-epoch final run | §2, §5 |
| E4 memorisation against the E-series train split | E6 has its own train split | `memorisation.py --train-records data/e6/records/train.jsonl` (added 2026-10-16) |
| RLVR with its own GRPO design | `RLVR_PLAN.md` now defines the rewards for both families | §7 |
| decisions: Gemma base download, `peft`, E4B passes | moot | §12 |

## 12. Open decisions

1. **Sweep rates:** 5e-5 / 1.5e-4 / 4.5e-4 (proposed).
2. **Control C1** (our 120M on meaning → poem only, ~1–2 GPU-hours): include it, so the comparison separates the recipe from the model family? Proposed: yes.
3. **Timing:** step 1 done; the 523M E6 queue finished its evaluations at 11:32 (2026-10-18), so the GPU is free for steps 2–4, before or after RLVR Stage 0 on the 120M.
4. **Partial-byte tokens in the constrained modes** (§6): proposed, run step 4 with the whole-token slice first and split the overrides; add pair entries only if partial ids are a material share of the model's first choices.

# RLVR plan: metre by default, meaning and coherence

Status: plan, 2026-10-17. Nothing is implemented. The GPU is busy with the 523M's E6 queue until about
2026-10-18 13:00. The CPU-side work (§9, step 1) can start before that.

## 0. Summary

After E6, both models write poems in metre only because the constrained decoder forces it, and their poems follow
the meaning loosely. This plan improves three properties with reinforcement learning:

| property | how it is rewarded | how it is judged |
|---|---|---|
| **metre by default**: the model's own output in metre, without the constrained decoder | exact: the metre engines, with partial credit per pāda, prāsa and yati | exact: free generation in metre; the decoder's override rate |
| **meaning**: the poem says what the bhāvam says | cheap judges: LaBSE similarity, and a frozen copy of E6 scoring the bhāvam given the poem | independent judges: Gemma-4 26B round trip, human ratings |
| **coherence**: the lines hold one thought | a cheap judge: how much each line is predicted by its own poem's other lines rather than another poem's | independent judges: a Gemma-4 26B rating, human ratings |

Word quality (real words, no filler, no copying) is rewarded throughout. Two rules keep the results honest:

1. **A judge is used only after it passes a validation test** (§4).
2. **No signal used as a reward is ever used to report results** (§5).

The order is cheapest first:

- **Stage 0:** decoding-time levers, no training.
- **Stage A:** rejection-sampling fine-tuning.
- **Stage B:** GRPO with these rewards.

Each runs first on the 120M, then on the 523M.

---

## 1. Starting point

| | 120M E6 (val, 114 poems per strategy) | 523M E6 |
|---|---|---|
| constrained: in metre | 100% | (queue) |
| constrained: single-akshara filler (real verse 4–5%) | 12–16% | |
| constrained: first choice overridden | 21–27% | |
| constrained: mass on allowed aksharas | 0.69–0.76 | |
| free generation: fully in metre | **0%** | |
| free generation: mass on allowed aksharas | 0.897 | |
| words copied from the bhāvam (real poems 2.5%) | 2.7–3.6% | |
| val loss of the poem: given metre + meaning (T1) / metre only (T0) | 2.253 / 2.803 | sweep at 1 epoch: 2.085 / 2.665 |

- **Starting checkpoints:** E6 plus the T1-only phase, `runs/e6-t1-120m` and `runs/e6-t1-523m`.
- **The frozen copy** of each starting checkpoint is the reference model for the KL term and the reverse-likelihood judge (§3.2).

## 2. Rollouts: how the policy writes during training

| mode | used for | cost |
|---|---|---|
| **free** | the metre reward and Stage B. Commits one akshara at a time, left to right, at temperature 1.0 and top-p 0.95, with no constraint — how the model would write "by default" | GPU only: one forward pass per akshara over the canvas, many poems in parallel |
| **constrained** | Stage A candidates and Stage 0 best-of-N. Same commitment order, but restricted to aksharas that keep the poem in metre, prāsa and yati | masks dominate. `metrical_decoder` computes them on the CPU, ~10 s per poem per shard (E6 evaluation: 456 poems in ~1.3 h on 4 shards). `ft/decode.py` computes them in batches on the GPU (PLAN §14: ~7 s per poem at 16 particles on the laptop; faster here) |

- **Canvas trimming:** canvases are trimmed to the prompt plus the metre's longest poem, not the full 512 tokens. A bidirectional model has no cache, so this cuts the cost of every free rollout step roughly in half.
- **Estimate, unmeasured** (free rollouts, 256 poems of ~100 aksharas in parallel, trimmed canvases): ~1–2 min for the 120M and ~4–8 min for the 523M. §9 measures it.

## 3. Rewards

Every component is a number in [0, 1] per poem. In Stage B each component is normalised within the prompt's group of
samples (GRPO), then the components are weighted.

### 3.1 Metre: exact

Computed with the engines (`indic_meter_dawg`, `chandohasam`) on the poem as written.

| component | definition | weight (initial) |
|---|---|---|
| gaṇa | share of pādas whose weight pattern fits the requested metre. Vṛttas: the pāda's fixed template, with the line-final laghu-as-guru relaxation. Jāti metres (kanda, āṭaveladi, tēṭagīti, sīsa, dvipada): the metre's line automaton accepts the line. Times 1 if the number of pādas is right, else times 0.5 | 0.20 |
| prāsa | share of lines 2…n whose prāsa matches line 1's, strict profile | 0.08 |
| yati | share of yati seats in maitri, strict profile | 0.08 |
| whole poem | 1 if the engine identifies the requested metre with prāsa and yati, strict profile (the E3 verdict) | 0.04 |

- **Partial credit is essential.** Free generation is 0% fully in metre today, so in an all-or-nothing reward every sample in a group would score 0, and GRPO would learn nothing.
- **The engines' ceilings** on the real val poems are prāsa 98.4% and yati 92.1% (strict). The reward cannot exceed them, and evaluation is read against them.
- **The data is already there:** `metrical_decoder.evaluate` gives the per-line verdicts (`eval.patterns`) the gaṇa component needs.

### 3.2 Meaning: judges, validated first (§4)

| component | definition | weight |
|---|---|---|
| similarity | LaBSE cosine between the poem and the input bhāvam (`ft/judge.py`, "direct LaBSE"; AUC 0.88 on 60 val items so far) | 0.12 |
| reverse likelihood | log p(bhāvam \| poem) under the **frozen** starting model's T2 head, as a per-token NELBO, minus the same for a mismatched bhāvam (a contrast, so a poem cannot score well by being generic) | 0.13 |

- **Why the frozen model:** it keeps the policy from moving its own judge. The contrast against a mismatched bhāvam removes a generic poem's head start.

### 3.3 Coherence: judges, validated first (§4)

| component | definition | weight |
|---|---|---|
| cross-line coherence | for each line i: log p(line i \| the poem's other lines) − log p(line i \| the other lines of a random real poem in the same metre), averaged over lines. Scored by Gemma-4 E2B (10 GB; an external model, so the policy cannot move it), as the mean NLL of the line's tokens | 0.15 |
| judge fluency | Gemma-4 E2B perplexity of the poem (the coherence judge of the 523M's pretraining) | 0.05 |

- **Gaming risk:** fluency alone rewards bland and repetitive text. It is kept small and guarded (§3.5).
- **What cross-line coherence targets:** our models' known failure, lines that are each fluent but do not hang together.

### 3.4 Word quality

| component | definition | weight |
|---|---|---|
| real words | share of words of ≥ 2 aksharas in the E6 training lexicon (`data/e6/lexicon`, 2.99M forms; training split only) | 0.08 |
| no filler | 1 − (excess of single-akshara words over the real-verse rate) | 0.07 |

### 3.5 Guards: a hard zero, not a weight

A sample gets reward 0 if it does any of these:

- repeats a line;
- copies from the bhāvam more than the real poems' 95th percentile;
- shares a run of ≥ 12 aksharas with a training poem (the memorisation check of `memorisation.py --train-records`, as a hash lookup);
- is shorter than the metre's minimum or longer than its maximum.

Guards are cheap and make the common reward hacks pointless.

**Weights.** The initial weights sum to 1: metre 0.40, meaning 0.25, coherence 0.20, words 0.15. They are tuned on val in
Stage 0 (§6) by how well the combined score picks the best of N against the independent judges.

## 4. Validating the judges (gate before any training)

Built from val poems (Bhagavatam skandhas 1, 2, 7; never trained on):

| set | what it is | the judge must |
|---|---|---|
| **meaning pairs** | each real poem with its own bhāvam, and with the bhāvam of another real poem in the same metre | separate them: AUC ≥ 0.90 for each meaning component |
| **patchwork poems** | 4 lines taken from 4 different real poems in the same metre: metrically valid, fluent line by line, incoherent as a whole | rank real above patchwork: AUC ≥ 0.85 for cross-line coherence |
| **shuffled poems** | the real poem's words shuffled | rank patchwork above shuffled, and real above shuffled (AUC ≥ 0.95) |
| **model poems** | the E6 val outputs | sit between real and patchwork; this is the headroom the reward can exploit |

- **A failing component** gets its weight moved to the passing ones, or a better scorer is tried. For meaning that would be the LaBSE round trip through the frozen T2 head; for coherence, Gemma-4 E4B as the scorer.
- **Measuring the floor:** the gap between real and patchwork poems is the size of the coherence signal.

## 5. Signals used for reward against signals used for evaluation

| | reward (cheap; called ~10⁵–10⁶ times) | evaluation (expensive; never rewarded) |
|---|---|---|
| metre | engines, partial credit | engines, strict whole-poem verdict, on **free** and constrained generation; override rate; mass on allowed aksharas |
| meaning | LaBSE; frozen-T2 reverse likelihood | **Gemma-4 26B round trip**: it writes a bhāvam for the poem, compared with the input bhāvam (LaBSE) and, for the Bhagavatam, with the edition's English bhāvam (`bhavam_en`); human ratings |
| coherence | cross-line PMI and fluency under Gemma-4 E2B | **Gemma-4 26B rating** (1–5, rubric) on the poem alone; human ratings |
| words | training lexicon; filler | an evaluation lexicon disjoint from the training one (pretraining val words) plus a hand-checked non-word audit, as PLAN §8.2 |
| copying | guards | `memorisation.py --train-records`; copy rate from the bhāvam |

- **The 26B is the evaluation judge,** so it must stay out of the reward. If the policy were trained to please it, the strongest independent measure we have would be lost.
- **Human ratings:** the `human_evals/` annotation app is running, for 100 blind items per model version.

## 6. Stage 0: decoding-time levers (no training)

1. **Classifier-free guidance.** E6 trained T0, the same poem with an empty meaning (10% of canvases). At each step: logits = uncond + w · (cond − uncond), with w ∈ {1, 1.5, 2, 3}.
   - Two forward passes per step: with the bhāvam, and with `భావం:` empty.
   - Expected effect: the poem follows the bhāvam more closely.
   - Implementation: in `constrained_sample.py`'s E6 mode, a second prompt per poem.
2. **Best-of-N.** N = 8 constrained candidates per prompt, ranked by the combined reward of §3. This also tunes the weights, with the independent judges of §5 as the target.

- **Measured on:** the E6 val set (114 poems per strategy), for both sizes.
- **Cost:** ~2–4 GPU-hours for the 120M with N = 8 (the masks dominate). For the 523M, about twice that.
- **What it tells us:** how much meaning and coherence is recoverable at all before any RL.

## 7. Stage A: rejection-sampling fine-tuning

The simplest RLVR (expert iteration; PLAN §7; `ft/rft.py` exists).

1. **Prompts:** 1,000–2,000 training-split prompts per round (metre + bhāvam), balanced over metres with rare metres upsampled. Never val or test.
2. **Candidates:** K = 8 constrained (masking + backtracking, the best E6 strategy) per prompt, plus K = 8 free.
3. **Selection:** the constrained candidate with the highest combined reward, if it passes the guards. Also any free candidate with full metre credit; these are rare at first.
4. **Training:** 1 epoch of T1 on the kept poems plus an equal number of gold poems (replay), at the T1-phase rate (0.3× the stage-2 rate).
5. **Rounds:** at most 3. Stop when the independent judges (§5) stop improving on val, never on the training reward.

**Why it also teaches metre by default.** Training on constrained outputs distils the constrained decoder into the model's own distribution. The free model should move toward the aksharas the metre allows, so free in-metre rates and overrides measure it directly.

- **Cost per round:** generation dominates. 1,000 prompts × 8 constrained candidates is 8,000 poems, ~6–10 h on `metrical_decoder` (CPU masks) or ~2–3 h through `ft/decode.py` (GPU masks). Free candidates add ~10 min (120M). Training on ~2,000 canvases plus replay takes minutes.
- **Decoder for generation:** `ft/decode.py`'s constraints accepted 99.7% of gold val poems. Its strictness differs from `metrical_decoder`'s, so a candidate it accepts is rescored with the strict engines before selection.

## 8. Stage B: GRPO with the §3 rewards

- **Rollouts:** free (§2). B = 32 prompts × G = 8 samples per step, temperature 1.0.
- **Advantage:** each reward component is z-normalised within the group, then weighted (§3). Guard failures get the group's minimum.
- **Policy gradient for a masked diffusion model.** The exact log-probability of a left-to-right sample costs one forward pass per akshara, too much for training. Instead, the poem's ELBO (the SFT loss on the T1 canvas, at sampled mask levels) stands in for its log-probability:
  - loss = −A · ELBO(poem | prompt), with a PPO-style clip on exp(ELBO_new − ELBO_old) and a KL penalty β · (ELBO_ref − ELBO_new) to the frozen start;
  - **variance reduction** (coupled-GRPO, DiffuCoder 2025): each sample is scored at a masking rate t and its complement 1 − t;
  - related estimators: diffu-GRPO (d1, Zhao et al. 2025), VRPO (LLaDA 1.5).
- **Hyperparameters to start:** lr 1e-6–5e-6 (120M), β = 0.05, clip 0.2, 1 inner update per batch, 200–500 steps, evaluation every 50 steps on a fixed probe set.
- **Monitoring:** reward components, KL, free in-metre rate, filler, copy rate, memorisation guard hits. **Stop** if the independent judges fall while the reward rises (reward hacking).
- **Cost (estimate):** 120M ~1.5–3 min per step (rollouts ~1–2 min, rewards ~20–40 s on CPU and GPU, update seconds), so 300 steps ≈ 8–15 h. 523M ~3–4× that.

## 9. Resources, and running the Gemma-4 26B in parallel

**What the machine has** (measured 2026-10-17):

| | |
|---|---|
| unified memory | 121.7 GB, shared by CPU and GPU. CUDA counts page cache as used: 27.6 GB "free" with 84 GB available; evicting the cache recovers it (`mdlm/checkpoint_eval.py`'s eviction) |
| CPU | 20 cores |
| disk | 2.7 TB free |
| running now | the 523M E6 queue (~16 GB GPU) until ~2026-10-18 13:00 |

| model (HF cache) | on disk | role here |
|---|---|---|
| Gemma-4 26B-A4B-it, bf16 | 49 GB (+ ~5 GB working memory) | the evaluation judge (§5) |
| Gemma-4 26B-A4B NVFP4 (nvidia / RedHat builds) | 18 / 16 GB | a smaller copy of the evaluation judge, if it loads and agrees with bf16 |
| Gemma-4 12B-it / E4B-it / E2B-it | 23 / 15 / 10 GB | E2B: the coherence reward judge; E4B: fallback |
| LaBSE; indic-sentence-bert-nli | 1.9 / 1.8 GB | the meaning reward |

**Measured speed of the 26B** (bf16, Hugging Face, one sequence at a time): median 4.1 s for a 62-token poem in the
2026-09-26 grid (`experiments/runs/2026-09-26_g26b`), about 15 tokens/s. Batched generation and prefill-only
scoring are faster; how much faster is measured in §10, step 2.

**Running the 26B in parallel with RLVR training, case by case:**

| how the 26B would be used | memory beside the policy | time per use | verdict |
|---|---|---|---|
| **per-step reward, round trip** (write a bhāvam for each of 256 rollouts) | 120M: ~27 GB + 54 GB ≈ 81 GB; 523M: ~95 GB, too tight | 256 × ~150 tokens: ~40 min at 15 tokens/s, maybe 5–10 min batched, **per RL step** | **no**: too slow. It would also put the evaluation judge in the reward (§5) |
| **per-step reward, scoring only** (likelihoods, one forward pass) | as above | ~256 × 400 tokens of prefill; unmeasured, roughly 0.5–2 min per step | **no**, for the §5 reason. On speed alone it would be possible for the 120M |
| **periodic auditor**: a fixed 64-prompt probe every ~50–100 RL steps, round trip and rating; loaded only for the audit | 54 GB at audit time; the policy keeps running or pauses | ~5–15 min per audit | **yes, recommended**: early warning of reward hacking from an independent judge, without slowing every step |
| **final evaluation** after each stage | the GPU to itself | val: 456 poems ~1–2 h batched | **yes** |
| NVFP4 26B in any of the roles above | 16–18 GB | similar compute | yes, if it loads with transformers or our NVFP4 loader (written for DiffusionGemma, validated against bf16 experts) and agrees with bf16 on the §4 sets |
| **the 26B as the RL policy** (RLVR on Gemma-4 26B itself, the AR comparison at scale) | 49 GB + LoRA, activations and rollout memory ≈ 75–85 GB: the whole machine | rollouts at ~15 tokens/s per sequence: a 256-sample step takes several minutes even batched; days per experiment | **not in parallel**. Possible alone, later, as part of `autoregressive_finetuning/` |

**Memory budget of the recommended set-up** (estimates; checked in §10, step 2):

| process | 120M policy | 523M policy |
|---|---|---|
| policy training + rollout buffers | ~15 GB | ~28 GB |
| frozen reference (KL, reverse likelihood), bf16 | ~0.3 GB | ~1 GB |
| LaBSE + Gemma-4 E2B judges | ~13 GB | ~13 GB |
| reward workers (engines, CPU) | RAM only | RAM only |
| **sum during training** | **~29 GB** | **~42 GB** |
| + 26B bf16 auditor, while auditing | ~83 GB | ~96 GB (tight: audit with the policy paused, or use NVFP4 ~60 GB) |

- **Conclusion:** the per-step loop runs on small judges. The 26B is loaded only to audit and to evaluate, which fits our memory.
- **The 523M:** bf16 audits run with the policy paused, or with the NVFP4 26B.
- **Nothing else runs on the GPU meanwhile.** In particular no vLLM server.

## 10. Steps and time

| step | where | time |
|---|---|---|
| 1. CPU now: the reward module (metre partial credit, words, guards, the batched engine pool), the §4 calibration sets, classifier-free guidance in `constrained_sample.py`, Stage A generation with E6 prompts | CPU | ~1 day of engineering |
| 2. After the 523M queue: validate the judges (§4); benchmark the 26B (batched generation, prefill speed, peak memory; bf16 and NVFP4); measure free-rollout speed | GPU | ~2–3 h |
| 3. Stage 0 on the 120M (guidance sweep, best-of-8) | GPU | ~3–4 h |
| 4. Stage A on the 120M, 2–3 rounds, an audit after each | GPU + CPU | ~1–1.5 days |
| 5. Stage B on the 120M, 200–500 steps, audits every 50–100 steps | GPU | ~1–2 days |
| 6. The best of 3–5 on the 523M | GPU | ~3–5 days |
| 7. Final evaluation: val and test, free and constrained; 26B judges; human ratings (100 blind items) | GPU + people | ~1 day + annotation |

## 11. Decisions for the user

1. **Reward weights to start:** metre 0.40, meaning 0.25, coherence 0.20, words 0.15. Raise metre if "metre by default" is the priority.
2. **The 26B's role:** evaluation judge and periodic auditor only, never in the reward (recommended).
3. **Stage A's decoder for generation:** `ft/decode.py` (GPU masks, ~3× faster, slightly different constraints), with every candidate rescored by the strict engines (recommended); or `metrical_decoder` (the E3/E6 decoder, slower).
4. **Order:** the full sequence on the 120M first, then only the stages that paid off on the 523M (recommended); or both sizes in parallel.

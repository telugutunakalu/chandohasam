> [!IMPORTANT]
> **Team Chandohasam**
>
> - Samvaran Rallabandi (samvaran.rallabandi@research.iiit.ac.in)
> - Mahesh Emani (mahesh.emani@research.iiit.ac.in)
> - Radhe Shyam Salopanthula (radheshyam.s@research.iiit.ac.in)
>
> 1. **Code.** This repository, development branch:
>    https://github.com/telugutunakalu/chandohasam/tree/dev
> 2. **Datasets.** The four verse corpora of [`dataset/`](dataset/):
>    https://huggingface.co/datasets/samvaran/chandohasam
> 3. **Models.** Every released model, with its card and an inference script:
>    https://huggingface.co/samvaran/chandohasam

# Chandohasam: Telugu metrical poetry generation with text diffusion

The project generates classical Telugu verse (padyam) in metre (ఛందస్సు) from a metre and a bhāvam, the poem's
meaning in prose. A padyam must meet three positional rules in every line: the gaṇa pattern, yati (caesura) and
prāsa (rhyme). The repository holds:

1. **The prosody engines.** Scansion and metre identification on a DAWG of 37 metres, plus the గణవిభజన, ప్రాస and యతి
   checks.
2. **The metrical controller** (`meter_engine/metrical_decoder`). It makes any language model write in metre by
   masking the tokens that cannot complete the poem.
   - **v1** = masking + backtracking.
   - **v2** = v1 + an inventory of attested syllables + attestation reweighting.
3. **The models.**
   - Our masked diffusion language models (MDLM, 120M and 523M), with a tokenizer that gives every akshara its own
     token. They are pretrained on general Telugu and fine-tuned on poems.
   - Autoregressive, encoder-decoder and large diffusion baselines fine-tuned on the same poems.
4. **The evaluation.**
   - One grid of every model, free and under the controller, on the same 100 prompts.
   - Deterministic poetics metrics and word resolution.
   - MAUVE.
   - Two human studies and learned coherence and adherence scores.
5. **The papers and the seminar deck.**

The fine-tuning poems come from a crawled corpus of over 300k Telugu poems with meanings. It is confidential, so it
is not in this repository, and nothing built from it is committed (see [Not in this repository](#not-in-this-repository)).

## Results in brief

From [full_grid_experiments/](full_grid_experiments/README.md#the-findings-in-short): 17 model rows × 100 prompts.

- **No model writes in metre on its own.** The best free rows are T5Gemma 2 270M and 1B fine-tuned, with 8% of
  poems in metre; every base model has 0%. The source poems themselves pass the strict check 53% of the time.
- **Under the metrical controller, 99–100% of poems are in metre** for every fine-tuned row. No finished poem is out
  of metre; the few misses ran out of their token budget.
- **Fine-tuning is what makes the constrained poems real.** Under the controller it adds +18 to +36 points of real
  words over the base model, in every family but DiffusionGemma.
- **The best cell is MDLM 523M fine-tuned with controller v2:**
  - 85.4% real words, against the source poems' 85.7%;
  - 76% of poems recognised against their prompt;
  - 100% in metre.

Per-model numbers: each training folder's README. The paper's tables: [paper/](paper/).

## What is where

The code and experiment folders each have a README with the method, the results and the commands to run their scripts.

### Prosody engines and tools

| folder | what it holds |
|---|---|
| [meter_engine/](meter_engine/README.md) | The engines everything else imports. `indic_meter_dawg` (scansion and metre identification on a DAWG built from `meter_rules.yaml`, 37 metres), `prasa`, `yati`, `chandohasam` (poem → metre, గణవిభజన, ప్రాస, యతి) and `metrical_decoder` (constrained decoding, v1 and v2). Rules are YAML files beside the code; right-linear grammars in `grammars/`; tests in `tests/`. |
| [webapp/](webapp/README.md) | A local Flask front end over `chandohasam`: paste a poem, get its full analysis. |

### Data

| folder | what it holds |
|---|---|
| [dataset/](dataset/) | The four verse corpora: 15,415 records, 12,704 of them verse. Pothana's Bhāgavatamu (7,366 verse), Vemana (1,164), Kūcimañci Timmakavi (1,642) and `chandassu.json`, 2,532 padyams of 25 śatakams from the open-source Kaggle Chandassu dataset (MIT). The machine annotations (`generated`, `bhavam_en`) are from Gemini. Every change since the first commit is logged in [CORRECTIONS.md](dataset/CORRECTIONS.md). |

### Models

| folder | what it holds | released as |
|---|---|---|
| [diffusion_pretraining/](diffusion_pretraining/README.md) | Stage 1 of the MDLM, on general Telugu (Wikipedia + AI4Bharat). `pilot120m` (120M, 76,000 steps, 4.98B tokens) is grown function-preservingly to `stage1-523m` (523M, 160,000 steps, 10.49B tokens). Also the akshara tokenizer (`tokenizer/`). | `pilot120m` (the Hub root), `mdlm-523m` |
| [diffusion_finetuning/](diffusion_finetuning/README.md) | Stage 2: full fine-tuning of both MDLMs to write a padyam from a metre and a bhāvam (the E6 + T1 recipe), and their evaluation. | `mdlm-120m-padyam`, `mdlm-523m-padyam` |
| [autoregressive_finetuning/](autoregressive_finetuning/README.md) | Nandi-Mini-150M, the size-matched autoregressive partner of the 120M MDLM, fully fine-tuned on the same poems and prompts. | `nandi-150m-padyam` |
| [t5_finetuning/](t5_finetuning/README.md) | T5Gemma 2 (encoder-decoder): bhāvam → poem as translation. The 270M and 1B are fully fine-tuned; the 4B trains LoRA r 128. | `t5gemma2-270m-padyam`, `t5gemma2-1b-padyam`, `t5gemma2-4b-padyam-lora` |
| [lora_gemma_diffusion/](lora_gemma_diffusion/README.md) | LoRA r 16 on DiffusionGemma 26B-A4B, a block-diffusion mixture-of-experts model, and its evaluation beside the other models. | `diffusiongemma-26b-padyam-lora` (to follow) |

### Experiments

| folder | what it holds |
|---|---|
| [full_grid_experiments/](full_grid_experiments/README.md) | The paper's main experiment. Every model, fine-tuned and base, free and under controller v1 and v2, on one set of 100 prompts, scored by one scorer: 5,472 scored poems, with paired tests. Prompts, raw runs, per-poem scores and the design decisions. |
| [experiments/](experiments/README.md) | The experiment register: 31 replication specs (EXP-01–41, retired numbers never reused) and their results. Also the constrained-decoding runs of the controller (`runs/`), the base pilot's decoding grid (`pilot_grid/`) and the GPU queue scripts (`scripts/`). |
| [samples/](samples/README.md) | Sample poems from constrained decoding: two poems in metre for each of the 37 metres and each of the 3 decoding strategies, from Gemma 4 E4B and DiffusionGemma 26B-A4B, with each chosen token's probability. |

### Evaluation

| folder | what it holds |
|---|---|
| [data_sanity_metrics/](data_sanity_metrics/README.md) | Corpus validation of `dataset/`, levels 1–4: prosodic integrity, length ratio, semantic fidelity, duplicates, lexical diversity, subword coverage. Report: [data_sanity_metrics_report.md](data_sanity_metrics/data_sanity_metrics_report.md). |
| [poetry_metrics/](poetry_metrics/README.md) | The deterministic poetics suite: anuprāsa (v1–v3), mādhurya, ojas, prasāda and chandas distance, each with a spec, a rubric and its validation. Scored on every poem source (the four corpora, both human studies, the Gemini poems), with one JSON per source. |
| [word_resolution_metric/](word_resolution_metric/README.md) | Word resolution for classical Telugu: a word as it stands in a poem → its dictionary headwords, through the lexicon and then a distilled ByT5. The paper uses it as a metric: the share of a poem's words that resolve. |
| [metrics/](metrics/) | The first MAUVE gate, on Pothana's Bhāgavatamu (`MauveOnPothana/`); the first report on coherence and adherence metrics (`SemanticCoherence/`); and the first 255 Gemini poems with their prosody check (`initial_evals/`). |
| [human_evals/](human_evals/README.md) | The two human studies. Study 1: 500 poems (the poets, textbook examples, Gemini). Study 2: 99 poems from three of our fine-tuned models. Also the annotation app, the LLM judge and the results. Annotators appear only as codes. |
| [semantic_coherence/](semantic_coherence/README.md) | Coherence and adherence metrics learned from the human ratings on frozen sentence embeddings, with significance tests, the LLM-as-judge comparison and scores on study 2 and the corpora. |
| [compilation/](compilation/RESULTS.md) | `RESULTS.md`: the evaluation results compiled from the committed result files, with all metrics side by side for each source. |

### Writing

| folder | what it holds |
|---|---|
| [paper/](paper/) | The papers in ACL format, built with XeLaTeX (`make`). `main.tex` is the mid-submission paper, `final.tex` the final paper (in progress). Tables in `tables/`, figures in `figures/`. |
| [presentation/](presentation/) | The progress seminar: `chandohasam_seminar.pptx` and `.pdf` (28 slides), speaker notes in `notes.md`, the deck's figures and its build scripts. |
| [Notes/](Notes/) | Working notes: a catalogue of the 33 metres of the Bhāgavatamu, ప్రాస rules, and notes on metrics. |

### Utilities

| folder | what it holds |
|---|---|
| [gcloud_agent_platform/](gcloud_agent_platform/) | Two scripts that list or probe the models an API key can reach on Google's Gemini Enterprise Agent Platform. The key itself is never committed. |

## Released models

All of them live in one public repository, [samvaran/chandohasam](https://huggingface.co/samvaran/chandohasam), one
model per subfolder. Each card gives the training, the results and the commands to generate.

| subfolder | model |
|---|---|
| (root) | `pilot120m`: the 120M MDLM base, pretrained on general Telugu |
| `mdlm-523m` | the 523M MDLM base |
| `mdlm-120m-padyam`, `mdlm-523m-padyam` | the two MDLMs, fine-tuned |
| `nandi-150m-padyam` | Nandi-Mini-150M, fine-tuned |
| `t5gemma2-270m-padyam`, `t5gemma2-1b-padyam` | T5Gemma 2 270M and 1B, fine-tuned |
| `t5gemma2-4b-padyam-lora` | T5Gemma 2 4B, LoRA adapter |
| `byt5-small-word-analysis` | the distilled ByT5 behind word resolution |
| `diffusiongemma-26b-padyam-lora` | DiffusionGemma 26B-A4B, LoRA adapter (to follow) |

## Quick start

The engines need only Python 3 and PyYAML:

```bash
cd meter_engine
python3 -m chandohasam --file poem.txt          # readable report
python3 -m chandohasam --file poem.txt --json   # structured result
python3 -m unittest discover -s tests           # test suite
```

As a library:

```python
import sys; sys.path.insert(0, "meter_engine")
from chandohasam import analyze

a = analyze(poem_text, profile="relaxed")
a.meter, a.name_te, a.matched    # 'seesamu+ataveladi', 'సీసము+ఆటవెలది', True
print(a.render())
```

The web app:

```bash
cd webapp && ./run.sh            # creates .venv on the first run; http://127.0.0.1:5000/
```

To write a poem with a released model, see each training folder's "Write a poem" section, for example
[diffusion_finetuning/](diffusion_finetuning/README.md#write-a-poem-with-the-released-models). The model paths
(training, generation, the controller's model back ends) need torch, transformers, safetensors and
huggingface_hub. The project venv (`.venv`, Python 3.12, torch 2.13 + CUDA 13) has all of them.

## Not in this repository

Deliberately untracked (see [.gitignore](.gitignore)):

- **The confidential poem corpus** (`padyarchana_exports/`) and everything built from it: training data, run folders,
  checkpoints, lexicon caches, MAUVE references, the decoder v2 inventories, and word resolution's database and
  tables. The engines and the released models need none of it; each folder's README says which of its scripts do.
- **Model weights.** They are on [Hugging Face](https://huggingface.co/samvaran/chandohasam), not in git.
- **PDFs**: third-party scans and papers (`*.pdf`; `resources/`, `reference_papers/`, `proposal/`).
- **Secrets**: `gcloud_agent_platform/api_key.txt` and any `.env` or credentials file.
- **Regenerable artifacts**: `pretraining_datasets/`, embedding caches, `dataset/backup/`, virtualenvs, `__pycache__`.

Some READMEs refer to folders that are not committed yet: `final_report_metrics/`, `metrics/mauve_padyarchana/`
(MAUVE of every generated set), `RL/`, `poetry_diffusion/`, `adherence_metric/`, `longest_coherent_subsequence/` and
`hf_release/`.

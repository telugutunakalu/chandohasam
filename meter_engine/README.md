# meter_engine — Telugu ఛందస్సు tooling

The engines the rest of the repository is built on: scansion and metre identification, prāsa, yati, the end-to-end
analyser, and the constrained decoder that makes a language model write in metre. Every metric, fine-tuning and grid
folder imports one of these packages. (Until 2026-09-14 this folder was `metrical_dag`; the package
`indic_meter_dawg` inside it is the metrical DAWG itself.)

| package | what it does | entry point | docs |
|---|---|---|---|
| `indic_meter_dawg/` | scansion (guru/laghu) and metre identification on a DAWG built from `meter_rules.yaml` (37 metres) | `python3 -m indic_meter_dawg identify --text …` | [METER_DAWG_README.md](METER_DAWG_README.md), `docs/`, `diagrams/` |
| `prasa/` | ప్రాస: compares the pādas' second aksharas under `prasa_rules.yaml` | `python3 -m prasa check …` | [PRASA_README.md](PRASA_README.md) |
| `yati/` | యతి: checks every yati group of a pāda under `yati_rules.yaml` | `python3 -m yati check …` | [YATI_README.md](YATI_README.md), `yathi_docs/` |
| `chandohasam/` | the three in order: poem → metre, గణవిభజన, ప్రాస, యతి | `python3 -m chandohasam --file poem.txt` | below |
| `metrical_decoder/` | constrained decoding: a model writes a padyam that the engines accept (masking, backtracking, hybrid; v2 inventory + attestation) | `python3 -m metrical_decoder …` | below, [CONSTRAINED_DECODING_PLAN.md](CONSTRAINED_DECODING_PLAN.md) |

Run everything from this folder (`cd meter_engine`): the packages import each other as top-level modules. From
elsewhere, put it on the path first: `sys.path.insert(0, "meter_engine")`.

**Requirements.** The engines need only Python 3 (3.12 in the project venv) and PyYAML. `metrical_decoder`'s model paths (`run`,
`diffusion`, `control`, `hf.py`) also need torch, transformers, safetensors and huggingface_hub; its core never
imports torch. The project venv (`../.venv`) has all of them.

## The analyser

```bash
python3 -m chandohasam --file poem.txt                 # readable report; exit 0 when the metre matches
python3 -m chandohasam --file poem.txt --json          # structured result
python3 -m chandohasam "పాదము 1" "పాదము 2" ... --profile relaxed --yati-sandhi acchu
```

```python
import sys; sys.path.insert(0, "meter_engine")
from chandohasam import analyze
a = analyze(poem_text, profile="relaxed")     # PadyaAnalysis
a.meter, a.name_te, a.matched                 # 'seesamu+ataveladi', 'సీసము+ఆటవెలది', True
u = a.units[0]                                # one metrical unit (సీసము); a.units[1] is the గీతి trailer
line = u.lines[0]
line.pattern                                  # 'UIIUIUIII…'
[(g.telugu, g.pattern, [x.text for x in g.aksharas]) for g in line.ganas]   # గణవిభజన
[(s.line_no, s.purva, s.prasa) for s in u.prasa.seats], u.prasa.matched      # ప్రాస aksharas + verdict
[(s.positions, s.aksharas, s.rule, s.matched) for s in line.yati]           # యతి aksharas + verdict
a.to_json(); print(a.render())
```

The result is a tree of dataclasses (`chandohasam/models.py`): `PadyaAnalysis` → `UnitReport` (one metre) →
`LineReport` (one pāda) → `GanaCell` → `AksharaCell`, with `PrasaReport`/`PrasaSeat` per unit and `YatiSeat` per
pāda.

How the pieces connect:

1. `indic_meter_dawg.identify_text` scans the text into aksharas with weights and identifies the metre; each
   candidate carries a per-pāda gaṇa segmentation and the yati positions.
2. `prasa.evaluate` compares the second aksharas of the pādas under the prāsa rules.
3. `yati.plan_from_candidate` turns the candidate into yati groups (`{1, 10}`, `{1, 8, 15}`, సీసము `{1, g3}, {g5, g7}`)
   and `yati.evaluate_plan` checks every group with the yati rules.
4. `chandohasam.analyze` runs the three in order and assembles the report.

Profiles `strict` / `relaxed` / `historical` gate both prāsa and yati. The yati sandhi mode (`off` / `hypothesis` /
`acchu`) controls how freely a sandhi may be assumed at a yati coordinate.

## The constrained decoder

`metrical_decoder` runs IndicNeuroSym's three strategies with the metrical DAWG as the symbolic back end, for every
metre of the catalogue. At each step the enforcer allows only the tokens that keep the poem completable in its metre
(gaṇa, and prāsa and yati through the engines themselves); `evaluate.py` then judges every poem with the engines,
never with the enforcer.

| mode | what it does |
|---|---|
| `baseline` | free sampling; the enforcer only watches |
| `masking_only` | sample from the allowed tokens |
| `masking_backtrack` | the same, with checkpoints and backtracking when the allowed mass collapses (the grid's default since 2026-10-28) |
| `hybrid` | the mask, then an accept-state re-ranking of the top candidates |

**v2 (the grid's `v2 A+B` rows).** Two additions to the mask, both off by default:
- **A, inventory** (`--inventory verse|padyarchana|tokenizer`): every syllable written must be attested.
- **B, attestation** (`--attest-weight W --attest-corpus all|train90|padyarchana`): among the allowed tokens, prefer
  those that keep the word a real word. It reweights and never removes a token, so every poem still ends in metre.

Use `padyarchana` for both when evaluating on `dataset/` poems: it holds none of their own syllables or words.

```bash
python3 -m metrical_decoder rules kandamu                       # the rules text the model is given
python3 -m metrical_decoder control --tokenizer google/gemma-4-E4B-it --out RUN_DIR   # random logits, CPU only
python3 -m metrical_decoder run --model google/gemma-4-E4B-it --out RUN_DIR \
    --meters utpalamala,kandamu --modes baseline,masking_backtrack --seeds 42 [--mask-workers 4]
python3 -m metrical_decoder diffusion --out RUN_DIR [--resident]  # DiffusionGemma (NVFP4 checkpoint)
python3 -m metrical_decoder summarize RUN_DIR                   # per-metre × per-mode table
python3 -m metrical_decoder report RUN_DIR [RUN_DIR …] --out report.md   # token choices and probabilities
python3 -m metrical_decoder inventory                           # rebuild inventories/ (≈ 75 s)
```

A run directory holds `run.json` (configuration), `prompts.jsonl`, `results.jsonl` (one row per poem with its
evaluation) and `traces.jsonl` (per-token trace). An interrupted run resumes where it stopped. The model folders
(`diffusion_finetuning/`, `autoregressive_finetuning/`, `t5_finetuning/`, `lora_gemma_diffusion/`, `RL/`,
`full_grid_experiments/`) import the package and plug their own models in as the logits source.

**Inventories.** `inventories/verse.txt` (3,879 syllables of `dataset/`) is committed. `padyarchana.txt` (6,131
syllables) and `padyarchana_words.txt` (212,422 words) come from the Padyarchana E6 train split, so they are
gitignored. `python3 -m metrical_decoder inventory` rebuilds all three from
`../diffusion_finetuning/data/e6/records/train.jsonl` and `../dataset/`; on 2026-10-30 the rebuild was byte-identical
to the files in use.

**Before editing this package**, check that no job imports it (`ps -eo pid,etime,cmd | grep -E
"metrical_decoder|constrained_sample|run_grid|grid.py"`). Sharded runs spawn workers that re-import it from disk,
so an edit mid-run mixes two versions in one run. Edit in a git worktree instead.

| module | role |
|---|---|
| `enforcer.py` | the decode state and `Enforcer.step`: the metre's minimal DFA over {U, I, ⏎} plus the unfinished word |
| `incremental.py` | guru/laghu of a word still being written (committed syllables, pending options) |
| `registers.py` | prāsa and yati during decoding, asked of the engines on text |
| `orthography.py` | well-formed Telugu as a small automaton (no stray signs or virama chains) |
| `inventory.py`, `attestation.py` | v2 layers A and B |
| `strategies.py` | the four modes and the per-token trace |
| `vocab.py`, `sources.py`, `hf.py` | the vocabulary slice, the logits-source protocol (+ the random control), a Hugging Face causal LM |
| `parallel.py` | masks computed in worker processes (`--mask-workers`) |
| `diffusion/` | DiffusionGemma: NVFP4 loader, canvas, the left-to-right frozen-prefix loop |
| `prompts.py`, `runner.py`, `evaluate.py`, `analysis.py`, `cli.py` | prompts, the grid runner, verdicts, the trace report, the command line |

## Corpus scripts

Each reads a corpus in the `../dataset/` record layout ([../dataset/README.md](../dataset/README.md)).

| script | what it does | writes |
|---|---|---|
| `scripts/corpus_run.py` | scansion + DAWG identification over the Bhāgavatam, outcome per poem | `reports/corpus_run_<date>.{md,json}` |
| `scripts/yati_corpus_run.py` | the yati engine over the Bhāgavatam under several configurations | `reports/yati_run_<date>.{md,json}` |
| `scripts/eval_corpus.py CORPUS --name NAME` | the analyser over any corpus: identification, label agreement, prāsa and yati per metre | `reports/eval_<name>_<date>.{md,json}` |
| `run_corpus.py --dataset … --out …` | prāsa over a corpus | `corpus_runs/<name>_{results.jsonl,results.csv,summary.md}` |
| `scripts/make_datasets.py`, `import_chandassu.py`, `label_with_engine.py`, `corpus_fix.py`, `fix_script_mixing.py`, `fix_verse.py` | build and correct the `dataset/` files | `../dataset/` (see its README) |

`reports/` and `corpus_runs/` hold the 2026-09-14 runs (`yati_run_2026-09-14_v1.*` is the earlier of two runs that
day). They cite `dataset/` record ids, which is one reason those ids never change.

## Reference material

- `meter_rules.yaml` (the metre catalogue: gaṇas, yati positions, prāsa flags), `ganas.yaml`, `meters.txt`.
- `grammars/<metre>.rlg`: each metre as a prosodic and a right-linear grammar. `docs/grammars/<metre>.md` explains
  them in plain language (primer: `docs/grammars/README.md`); `docs/scansion.md` gives the scansion rules.
- `diagrams/`: a rule card per metre, the vṛtta trie and the DFAs (index: [diagrams/README.md](diagrams/README.md)).
- `yathi_docs/`: the yati rule extraction; `yathi_compact.md` is the table the engine parses.
- [METER_DAWG_PLAN.md](METER_DAWG_PLAN.md), [CONSTRAINED_DECODING_PLAN.md](CONSTRAINED_DECODING_PLAN.md): design and
  evidence, §17 for v2.
- `aksharanusarika.py`: the akshara splitter (v0.0.7a, bundled). `prasa_engine.py` and `yati_engine.py` are
  compatibility entry points for the packages.

## Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"     # 562 tests, ≈ 6 min, CPU only
python3 -m unittest discover -s tests -p "test_dec_*.py" # the decoder only
```

`test_imd_*` cover the DAWG, `test_prasa_rules` / `test_yati_rules` the rule files and their fixtures,
`test_chandohasam` the analyser, and `test_dec_*` the decoder (random-logit sources, no model). The suite must be
discovered from `tests/` (`-s tests`), because the helpers `dec_support` and `imd_support` live there.

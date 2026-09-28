# data_sanity_metrics

Corpus-validation ("data sanity") metrics for the four corpora in
[`../dataset/`](../dataset/): `bhagavatam.json`, `vemana.json`,
`kuchimanchi_timmakavi.json` and `chandassu.json`. The metrics are levels 1–4 of
the corpus-validation pipeline of IndicNeuroSym §5. Level 5, LLM-as-a-judge, is
not implemented. Each metric comes with sense checks that test whether its
number means what it claims.

Scansion is done by this repo's [`meter_engine`](../meter_engine/). The findings
are in [data_sanity_metrics_report.md](data_sanity_metrics_report.md).

## The data

All four files share one record layout ([`dataset/CORRECTIONS.md`](../dataset/CORRECTIONS.md)).
[`common/dataset.py`](common/dataset.py) reads them into one `Poem` shape:

| corpus | verse poems | Telugu bhavam + gloss | English `bhavam_en` | metre label |
|---|---|---|---|---|
| `bhagavatam` | 7,366 (+2,700 prose) | the edition (`bhavam`, `teeka_pairs`) | machine | the edition |
| `vemana` | 1,164 | machine (`generated`) | machine | heuristic |
| `kuchimanchi_timmakavi` | 1,642 (+11 prose) | machine (`generated`) | machine | mostly `meter_engine` itself |
| `chandassu` | 2,532 | machine (`generated`) | machine | the Kaggle corpus |

**Every metric is reported per dataset file.** A corpus is named by its file
stem, and there are no pooled all-files numbers. The one cross-file view is
duplicates *across* files (level 4c).

The metrics measure verse poems. Two layout details are handled explicitly:
- **Bhagavatam's seesa poems are split into two records**: a parent (the seesa
  lines) and a child (the closing geeti and the bhavam of the whole poem). A
  child's bhavam is compared with the parent's lines followed by its own.
- **meter_engine reads a seesa pāda as two half-lines**, the way Bhagavatam
  and Kuchimanchi write it. Chandassu writes its seesa pādas on one line with
  ` - ` between the halves; for scansion only, those lines are split at the
  separator (also written `X- Y`, `X -Y`, or `X- - Y` for a word running across
  the halves; a dash that ends a line is not a separator). Level 0 counts them,
  and level 1 reports how many were split.

## The metrics

| script | level | metric | sense checks |
|---|---|---|---|
| `level0_inventory.py` | 0 | size, structure (incl. line counts vs the metre, seesa layout, parent/child links), labels, annotation coverage, provenance of machine annotation, script purity | — (it is the check) |
| `level1_prosodic_integrity.py` | 1 | share of labelled poems that satisfy their metre on gaṇa, prāsa and yati (`meter_engine`, strict and relaxed profiles) | agreement by label source (engine-made labels agree by construction); how yati passes (rule, sandhi hypothesis, prāsa-yati); failing poems |
| `level1_chance_pass_rates.py` | 1 | — | prāsa and yati pass rates for material from unrelated poems of the same metre |
| `level2_length_ratio.py` | 2 | \|bhavam\| / \|verse\| in non-space characters, pass if 0.8 ≤ r ≤ 2.5 | units (words, aksharas); shuffled and neighbour controls; too short vs too long |
| `level3_semantic_fidelity.py` | 3 | cosine of poem–Te, poem–En, Te–En under LaBSE, mSBERT, IndicSBERT; gate: LaBSE Te–En ≥ 0.65 | shuffled and neighbour controls, AUC, retrieval@1, calibrated threshold, English-only negative-control encoder |
| `level4_lexical_diversity.py` | 4 | TTR, MATTR(50), Yule's K, Honoré's H, hapax ratio, Sichel's S; per-poem means | Telugu and English bhavams at equal token count, TTR growth, MATTR by window, per-poem degeneracy |
| `level4_subword_coverage.py` | 4 | Gemma Telugu vocabulary coverage, per-poem subword TTR | fertility (tokens per word / akshara), akshara-split rate |
| `level4_duplicates.py` | 4 | exact, normalised and near (3-gram Jaccard) duplicate poems, within and across corpora | pāda reuse, bhavam reuse |
| `cross_level_summary.py` | 1–4 | every level on one table; poems passing levels 1–3 together | — |


## Running

From this folder, with the repo's `.venv`:

```bash
cd data_sanity_metrics
PY=../.venv/bin/python

$PY level0_inventory.py                      # seconds
$PY level1_prosodic_integrity.py --workers 16 # ~25 min the first time (scansion), then seconds
$PY level1_chance_pass_rates.py --workers 16 # ~5 min; reuses the scansion cache
$PY level2_length_ratio.py                   # seconds
$PY level3_semantic_fidelity.py              # ~15 min on a GPU the first time (4 encoders), then seconds
$PY level4_lexical_diversity.py              # ~1 min
$PY level4_subword_coverage.py               # ~1 min
$PY level4_duplicates.py                     # ~1 min
$PY cross_level_summary.py                   # seconds once the caches exist

bash run_all.sh                              # everything, in the order above
```

**Every script runs on its own.** None of them needs another's output:
- the scansion (`common/scansion.py`) and the embeddings
  (`common/embeddings.py`) are computed on demand and cached in
  `outputs/cache/`;
- a script that needs them computes whatever is missing;
- `cross_level_summary.py` calls the level modules' per-poem functions.

Options:
- `--datasets STEM ...`: measure only the given files, on every script
  (for example `--datasets vemana chandassu`);
- `--workers N`: parallel scansion in the level-1 scripts and the summary;
- `--models ...`: a subset of encoders in level 3;
- `--tokenizer ID`: another tokenizer in level 4b.

**Caches are keyed by content.** A poem whose lines or label change is
rescanned; a text that changes is re-encoded. After a dataset edit, just rerun.

**Outputs.** Each script prints its tables and writes `outputs/<script>.json`.
`outputs/cache/` is gitignored.

## Layout

```
data_sanity_metrics/
├── config.py              paths, corpora, thresholds, encoders, tokenizer
├── common/
│   ├── dataset.py         the four corpora as Poem records
│   ├── scansion.py        meter_engine verdict per poem, parallel and cached
│   ├── controls.py        shuffled and neighbour pairings (levels 2, 3)
│   ├── embeddings.py      cached sentence encoding, AUC, retrieval
│   ├── lexical.py         TTR, MATTR, Yule's K, Honoré's H, hapax, Sichel's S
│   ├── minhash.py         MinHash-LSH near-duplicate search
│   ├── telugu.py          words, aksharas, normalisation
│   └── io.py              JSON output, console tables
├── level0_inventory.py ... level4_duplicates.py, cross_level_summary.py
├── run_all.sh
├── outputs/               one JSON per script (outputs/cache/ is gitignored)
├── data_sanity_metrics_report.md
└── scrap/                 the earlier implementation on the IndicNeuroSym dwipada dataset,
                           with its report and outputs; kept for reference, not run
```

## Requirements

- The repo `.venv` (torch, transformers, numpy, scikit-learn) plus
  `sentence-transformers`.
- Models from the Hugging Face cache, downloaded once:
  - `sentence-transformers/LaBSE`
  - `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
  - `l3cube-pune/indic-sentence-bert-nli`
  - `sentence-transformers/all-MiniLM-L6-v2`
  - the Gemma 4 tokenizer (`google/gemma-4-E2B-it`). Gemma 3's
    (`unsloth/gemma-3-1b-it`) is the same text tokenizer: the same 1,784
    Telugu tokens, and identical token ids for every verse and bhavam of the
    four files. Only the special tokens differ, so coverage is the same under
    either.

  Set `HF_HUB_OFFLINE=1` to use the cache without contacting the Hub.
- A GPU for level 3 (about 2 GB). The CPU works, only slower.

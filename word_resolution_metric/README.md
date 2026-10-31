# word_resolution_metric

**Word resolution for classical Telugu:** a word as it stands in a poem → the dictionary headword(s) it stands for,
and the dictionaries' definitions. The project uses it as a metric (the paper's §5, "Resolving Words with a Distilled
ByT5"): the share of a poem's words that resolve to dictionary headwords, which a list of known words cannot measure
for compounds and sandhi forms it has not seen.

This folder is the self-contained setup of the separate word-resolution pipeline (version v28, 2026-10-28): the
resolver's code, its rules, its database, its precomputed table and its distilled ByT5. The pipeline itself is not in
this repository; its report is, in [`reports/`](reports/).

Status 2026-10-31:
- **In use:** `../final_report_metrics/score_resolution.py` scores every poem of the evaluation with it; the paper
  reports the gated reading (below).
- **The ByT5 is released** on Hugging Face as
  [`samvaran/chandohasam/byt5-small-word-analysis`](https://huggingface.co/samvaran/chandohasam/tree/main/byt5-small-word-analysis),
  with an inference script.

## Contents

1. [What is where](#what-is-where)
2. [How a word is resolved](#how-a-word-is-resolved)
3. [The distilled ByT5](#the-distilled-byt5)
4. [Install and use](#install-and-use)
5. [As a metric in this project](#as-a-metric-in-this-project)
6. [What to expect](#what-to-expect)
7. [The database](#the-database)
8. [Options](#options)
9. [Scripts](#scripts)
10. [Provenance and limits](#provenance-and-limits)

## What is where

| what | where | in git |
|---|---|---|
| the API and CLI | `resolve.py` (`WordResolver`) | yes |
| the resolver code, copied from the pipeline | `resolver/`: `lexicon.py`, `corpus_lines.py`, `byt5_splitter.py`, `sandhi_data.py` | yes |
| the guaranteed answers | `rules/guaranteed.tsv`: 1,803 words with their analysis, headword, source and confidence (1,621 agreed by two judge readings, 39 by a person, 143 closed-class rules: pronouns, particles, verb forms) | yes |
| the report | `reports/word_resolution_report.md` (also `.html`), `reports/figures/` | yes; the `.pdf` is local, as every PDF in the repository |
| the database | `db/padarchana_min.db` (1.4 GB): 50 dictionaries, and the crawled corpus's word-by-word glossary | no: the glossary comes from the confidential corpus |
| the corpus table | `data/resolved_words_v28.tsv.gz` (50 MB): every word type of the corpus, resolved (2.0M types); `data/line_join_decisions.json` | no |
| the model | `models/byt5_distill_v2/` (572 MB) | no: on Hugging Face (below) |

The database and the table are not distributed. To fill `models/` from the release:

```bash
cd word_resolution_metric
../.venv/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('samvaran/chandohasam', allow_patterns=['byt5-small-word-analysis/*'], local_dir='models/hub')"
ln -s hub/byt5-small-word-analysis models/byt5_distill_v2
```

The released folder holds the same weights; its `config.json` sets `tie_word_embeddings` to false, as ByT5-small's
own, and loads identically (Δlogit 0 under transformers 5.15).

## How a word is resolved

1. **The precomputed table** (`data/resolved_words_v28.tsv.gz`): if the word is one of the corpus's 2.0M types, its
   pipeline answer is returned at once (class, analysis, confidence, source, corpus count). This is the full
   pipeline's result: models, attestation, glossary evidence, joins and the per-poem context pass included.
2. **The guaranteed table** (`rules/guaranteed.tsv`): closed-class words and answers confirmed by two judge readings
   or a person.
3. **The lexicon** (`resolver/lexicon.py` over `db/padarchana_min.db`):
   - a headword, variant, redirect or synonym as it stands;
   - inflections stripped from the end (plural, oblique, case endings, -ంబు/-ము, -ఁడు, the drutam, verb endings,
     converbs);
   - the particles -యు -తో -ను -అని -ఏ -ఐ -ఓ;
   - a bare stem as used in a compound;
   - the sandhi rules: initial voicing and యడాగమ undone, syncope పల్కు → పలుకు, Sanskrit consonant stems జగత్ →
     జగత్తు, ఓ-stems మనో → మనస్సు, సద్ → సత్, త్రిక ఇవ్విధంబున → ఈ + విధంబున, యతని → అతడు.
4. **The ByT5 fallback** (`models/byt5_distill_v2`): four beams of the distilled model; the first analysis whose
   parts all carry a headword is accepted (`resolved-by-byt5`, confidence 0.79 for the first beam, 0.70 for a later
   one). Generations are cached in `data/byt5_cache*.json`.
5. Otherwise `unresolved`.

The result's `class` is the pipeline's class (`headword`, `inflected`, `split-all-known`, `annotated-all-known`,
`resolved-by-byt5`, …, `partial`, `unresolved`); `resolved` is true for the strong classes. In `parts`, a part with
an arrow carries the headword the pipeline chose; a part without one is read through the lexicon when you ask, and
its `status` says how (`headword`, `inflected`, `stem`, or `unknown`). A `stem` reading is a guess (వేమన → వేమము);
treat it as weaker than the others.

## The distilled ByT5

From the report, §13.3 and §15.2:
- **Model:** ByT5-small (byte-level T5: 12 encoder and 4 decoder layers, d_model 1,472, 6 heads, a byte vocabulary
  of 384; 299,637,760 parameters).
- **Strategy:** full fine-tuning (supervised, sequence-to-sequence cross-entropy on the analysis), no adapter. Checked
  against google/byt5-small: 169 of its 170 tensors moved by more than 0.1% (the last, a position-bias table, by
  0.07%), and the weight changes are of full rank.
- **Task:** the word alone (no context), as UTF-8 bytes → its analysis: parts joined by `+`, and `→headword` where
  the headword differs from the part (చదివాను→చదువు, రాముడు+అతడు). It learns resolution, not only segmentation.
- **Data, by distillation from the pipeline:** 337,864 (word, analysis) pairs (`data_distill_v2`):
  - the pipeline's strong classes at high confidence;
  - generated paradigm forms of dictionary headwords;
  - same-lexeme pairs from the corpus glossary and the Annamayya glossary.

  Dev: 4,000 pairs. The 931 hand-annotated gold pairs are held out and never trained on.
- **Optimisation:**
  - Adafactor, learning rate 5e-4, batch 16;
  - bf16 with gradient checkpointing, on one GPU;
  - the first model ran 3 epochs (62,274 steps, 5.5 h, on 332,128 pairs); the current one ran 21,116 further steps
    from that checkpoint, on the 337,864;
  - output budget: 2.5 × the word's bytes + 24.
- **Results:**
  - dev: exact analysis 0.788, headword level 0.842;
  - on the gold pairs it names the gold headword 0.726 of the time (the generator-backed lexicon 0.508);
  - the dictionary gate accepts 0.78 of greedy analyses at 0.794 precision and 0.879 of four-beam lists at 0.721;
  - in the corpus it resolves 10.1% of occurrences, and on the random sample its class scores 0.67 at the headword
    level.

## Install and use

Python 3.10+ with the standard library is enough for the lexicon, the table and the CLI. The ByT5 fallback needs
`torch` and `transformers` (`pip install -r requirements.txt`); without them the resolver runs without the model and
says so once on stderr.

```
python resolve.py లోకములోనఁ వేమననగ కుతూహలావతీర్ణ        # one line per word: class, analysis, headwords, source
python resolve.py --line "పూజలిడిన యంత, భుక్తి ముక్తుల నిచ్చు" --meanings
python resolve.py --json --no-table కల్గుచు              # JSON; --no-table exercises the live resolver only
python resolve.py --no-byt5 …                            # never load the model
```

```python
from resolve import WordResolver
r = WordResolver()                       # the table loads on first use (~4 s); the model only when a word needs it
r.resolve("కుతూహలావతీర్ణ")
# {'word': 'కుతూహలావతీర్ణ', 'class': 'split-all-known', 'resolved': True, 'analysis': 'కుతూహల+అవతీర్ణ',
#  'parts': [{'surface': 'కుతూహల', 'headword': 'కుతూహలము', 'status': 'stem'}, {'surface': 'అవతీర్ణ', 'headword': 'అవతీర్ణము', 'status': 'stem'}],
#  'headwords': ['కుతూహలము', 'అవతీర్ణము'], 'confidence': 0.703, 'source': 'table:model@config', 'corpus_count': 107}
r.resolve_line("వేమననగ యోగి వెలసె లోకములోనఁ")   # the line's tokens, each resolved
r.resolve_poem(["line 1", "line 2", …])         # the pipeline's tokens across line ends
r.meanings("లోకము")                              # [{'dictionary': …, 'grammar': …, 'meaning': …}, …]
r.glossary("వెలసె")                              # the poems' glossary entries for the form: gloss, split, layer, attestations
```

`WordResolver(glossary=True)` (the default) also loads the editorial glosses into the lexicon as attestation and gloss
evidence, the way the pipeline's attestation and final stages use them; `--glossary` on the CLI prints the glossary
entries of each word.

## As a metric in this project

`../final_report_metrics/score_resolution.py` (≈ 15–20 min, ByT5 on the GPU) runs `WordResolver` as it is, on every
poem, and writes four readings per poem (shares of its tokens):

| reading | what counts as resolved |
|---|---|
| `wr_resolved` | the resolver's `resolved` flag, the corpus table first |
| `wr_resolved_verified` | the same, with a ByT5 analysis accepted only when every headword it names is a lexicon entry and no part is a stray single akshara |
| `wr_resolved_strict` | the same without the two guesses: a ByT5 analysis and a bare-stem reading |
| `wr_resolved_live`, `…_live_verified`, `…_live_strict` | the live path only (no corpus table), for every poem alike |

**Read it without the table and with the gate.** The corpus table holds the words of the benchmark's own poems, so
the paper reads the live path (`--table-free` in `../final_report_metrics`). And `resolve()` accepts a ByT5 part
written `surface→headword` without looking the headword up, so only the verified reading separates words from
nonsense. On the 90 poets' source poems of the evaluation and their akshara-shuffled copies
(`../final_report_metrics/results/poems_all_metrics.jsonl`):

| live reading | source poems | shuffled copies |
|---|---|---|
| ungated (`wr_resolved_live`) | 99.2% | 94.1% |
| **gated (`wr_resolved_live_verified`; *resolved* in the paper)** | **86.3%** | **27.1%** |
| dictionary only (`wr_resolved_live_strict`) | 41.5% | 10.6% |

The dictionary-only reading is low because long compounds need the splitter.

`../poetry_metrics/word_resolution_sources.py` runs the same readings on every poem source, the four dataset files
and both human-evaluation studies, one JSON per source (`../poetry_metrics/outputs/word_resolution/`,
`../poetry_metrics/reports/word_resolution_sources.md`).

## What to expect

On the corpus (v28):
- **Coverage:** 90.8% of word occurrences resolve to a headword; 96.3% are at least attested.
- **Precision:**
  - on a random sample of full words, the headword-level precision of resolved words is 0.70 to 0.84 (the judge's
    two readings disagree);
  - on hard held-out words, 0.68.
- **By class:** inflected forms and direct headwords are the most reliable (0.77 to 0.79 on the sample), splits into
  known parts the least (0.53).
- **Broken words:** words broken by the edition's spaces or line ends are resolved as pieces unless the join rules
  merge them; `resolve_poem` applies the recorded line-end joins.

## The database

`db/padarchana_min.db` holds every table of the pipeline's full dictionary database that has words, definitions or
glossary data, with the same row counts: dictionaries (50), entries (133,539), definitions (367,100), meanings
(608,520), grammar (36,500), variants (110,801), token_redirects (3,728), tokens (641,544), token_dicts, sources,
comments, thesaurus, synonym_lists, meta, annamayya_forms (131,910) and the corpus glossary (4,766,005 forms:
1,330,486 editorial + 3,435,519 machine-generated).

Still absent, deliberately:
- **The full-text search index:** `fts` (with its shadow tables), `fulltext_post` (1,769,995 rows) and `search_keys`
  (2,257,278 rows). These serve the dictionary web app's search box and are derived from the other tables. The
  lexicon and the resolver do not read them.
- **`examples`** (98,333 rows): the example sentences attached to entries. The definitions they illustrate are all
  there.

For resolution, glossary lookup and meanings the full database answers identically; the difference is size (1.61 GB
against 1.49 GB). A copy of the full database placed at `db/padarchana_min.db` works unchanged.

## Options

- `WordResolver(use_byt5=False)` or `--no-byt5`: never load the model.
- `resolve(word, use_table=False)` or `--no-table`: skip the precomputed table (to see what the live resolver does).
- **The paradigm index** (`paradigm_forms.db`, 3.4 GB, generated forms of every headword) is not included. Copy it to
  `db/paradigm_forms.db` (or set `LEXICON_FORMS_DB`) to let the lexicon confirm inflections against it. That raises the
  confidence of inflected readings from 0.6 to 0.95 and reads some forms the stripper cannot.
- `LEXICON_EXCLUDE_DICTS` (default `47,48,49,50`) keeps the uncurated dictionaries out of the lexicon; set it to
  `47,48,50` to allow the idiom dictionary, etc.

## Scripts

| script | purpose |
|---|---|
| `resolve.py` | `WordResolver`, the API (`resolve`, `resolve_line`, `resolve_poem`, `meanings`, `glossary`) and the CLI: the order table → guaranteed rules → lexicon → ByT5 |
| `resolver/lexicon.py` | the dictionary lexicon over the database: normalisation (ౘ→చ, ౙ→జ, ఁ removed, ఱ→ర), headwords, variants, redirects, inflection stripping, particles, sandhi rules |
| `resolver/corpus_lines.py` | the pipeline's one tokenisation of poem lines, with the recorded line-end joins (a word a pāda breaks is re-joined) |
| `resolver/byt5_splitter.py` | the distilled ByT5 behind the pipeline's splitter interface: greedy and n-best analyses, cached per word; the length-scaled output budget |
| `resolver/sandhi_data.py` | the split notation's helpers: the word-start check, cleaning, and per-character split labels (the BiLSTM tagger's) |
| `reports/figures/make_charts.py` | the report's charts (numbers at the top of each chart) |
| `reports/figures/md2html.py` | the report's Markdown → HTML converter, for the PDF (`reports/README.md` has the commands) |

## Provenance and limits

- **Built** 2026-10-28 from pipeline version v28. The design, metrics and results are in
  [`reports/word_resolution_report.md`](reports/word_resolution_report.md) (sections 12–15 added 30–31 October: the
  metric, the training mechanisms, the datasets, definitions for reuse). The report's companion files
  (`../bilstm/README.md`, `../gemini_design/EVALUATION.md`) and its reproduction commands belong to the pipeline's
  own repository, not this one.
- **No poem text:** the table, the rules and the database hold words and definitions only. The glossary inside the
  database is still drawn from the confidential corpus, so the database stays out of git.
- **The ByT5** was distilled from the pipeline's own analyses and the editors' splits.
- **The dictionaries:** the database merges fifty published dictionaries plus the project's additions
  (dictionaries 45, 46; 47–50 present but excluded by default).

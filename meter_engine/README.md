# meter_engine — Telugu ఛందస్సు tooling

One folder, four engines, one end-to-end tool. (This folder was called
`metrical_dag` until 2026-09-14; the *package* `indic_meter_dawg` inside it is
the metrical DAWG itself. The rename removes that confusion.)

```
meter_engine/
├── chandohasam/        end-to-end tool: poem → metre, గణవిభజన, ప్రాస, యతి   (python3 -m chandohasam)
├── indic_meter_dawg/   scansion (guru/laghu) + metre identification with a DAWG (python3 -m indic_meter_dawg)
├── prasa/              ప్రాస engine (python3 -m prasa)          ← data: prasa_rules.yaml
├── yati/               యతి engine  (python3 -m yati)           ← data: yati_rules.yaml
├── aksharanusarika.py  the akshara splitter the prāsa engine uses (bundled v0.0.7a)
├── meter_rules.yaml    the metre catalogue (gaṇas, yati positions, prāsa flags)  · ganas.yaml
├── grammars/ docs/ diagrams/   generated right-linear grammars, docs and diagrams of every metre
├── yathi_docs/         the yati rule extraction (yathi_compact.md is the parsable table)
├── scripts/            corpus runs (corpus_run.py, yati_corpus_run.py, eval_corpus.py), make_datasets.py, corpus_fix.py · run_corpus.py (prāsa)
├── reports/ corpus_runs/   outputs of the corpus runs
├── tests/              unittest suites for every engine and the tool (python3 -m unittest discover -s tests)
└── prasa_engine.py, yati_engine.py   thin compatibility entry points for the packages
```

## The tool

```bash
cd meter_engine
python3 -m chandohasam --file poem.txt                 # readable report
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

The result is a tree of dataclasses (`chandohasam/models.py`): `PadyaAnalysis` →
`UnitReport` (one metre) → `LineReport` (one pāda) → `GanaCell` → `AksharaCell`,
with `PrasaReport`/`PrasaSeat` per unit and `YatiSeat` per pāda.

## How the pieces connect

1. `indic_meter_dawg.identify_text` scans the text into aksharas with weights and
   identifies the metre; each candidate carries a per-pāda gaṇa segmentation and
   the yati positions (`docs/`, `METER_DAWG_README.md`).
2. `prasa.evaluate` compares the second aksharas of the pādas under the
   prāsa rules (`PRASA_README.md`).
3. `yati.plan_from_candidate` turns the candidate into yati groups (`{1, 10}`,
   `{1, 8, 15}`, సీసము `{1, g3}, {g5, g7}`) and `yati.evaluate_plan` checks every
   group with the yati rules (`YATI_README.md`).
4. `chandohasam.analyze` runs the three in order and assembles the report.

Profiles `strict` / `relaxed` / `historical` gate both prāsa and yati; the yati
sandhi mode (`off` / `hypothesis` / `acchu`) controls how freely a sandhi may be
assumed at a yati coordinate.

## Corpora and evaluation

`../dataset/bhagavatam.json` (Pōtana, labelled), `../dataset/vemana.json` (1,164
poems, labelled ఆటవెలది / సీసము) and `../dataset/kuchimanchi_timmakavi.json`
(1,653 blocks of the అచ్చతెలుఁగు రామాయణము, unlabelled) share one record layout;
`scripts/make_datasets.py` builds the last two from the raw text files.
`scripts/eval_corpus.py CORPUS --name NAME` identifies every poem once and
reports identification rate, label agreement, prāsa and yati pass rates per
metre under two yati sandhi modes, writing `reports/eval_<name>_<date>.{md,json}`.

## Tests

```bash
cd meter_engine && python3 -m unittest discover -s tests -p "test_*.py"
```

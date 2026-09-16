# Telugu Chandassu — computational analysis of Telugu metrical poetry

Tooling and experiments for analysing classical Telugu verse (ఛందస్సు): metre
identification, గణవిభజన (foot division), ప్రాస (rhyme) and యతి (caesura)
verification, plus evaluation metrics for machine-generated verse.

## Layout

| Path | What it is |
|---|---|
| [meter_engine/](meter_engine/) | The core engines. `chandohasam` (end-to-end poem → analysis), `indic_meter_dawg` (scansion + metre ID via a DAWG), `prasa` (ప్రాస), `yati` (యతి). Rules live in YAML next to the code. |
| [webapp/](webapp/) | Flask front-end over `chandohasam` — paste a poem, get the full analysis. |
| [dataset/](dataset/) | Source corpora: Pothana's Andhra Mahabhagavatamu, Vemana, Kuchimanchi Timmakavi. |
| [metrics/](metrics/) | Evaluation experiments, chiefly the MAUVE sanity gate on Pothana. |
| [human_evals/](human_evals/) | Sampling scripts and poem sets for human rating. |
| [Notes/](Notes/) | Working notes on metres and ప్రాస. |
| [gcloud_agent_platform/](gcloud_agent_platform/) | Small scripts for listing/checking models on the GCloud agent platform. |

Each subproject has its own README with usage details — start with
[meter_engine/README.md](meter_engine/README.md).

## Quick start

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

Web app:

```bash
cd webapp && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=.. python app.py      # http://127.0.0.1:5000/
```

## Not in this repo

Deliberately untracked (see [.gitignore](.gitignore)):

- **PDFs** — `resources/`, `reference_papers/`, `proposal/` hold third-party
  scans and papers (~200MB) that are not redistributed here.
- **`telugu_prosody_engine/`** — superseded by `meter_engine/`.
- **Secrets** — `gcloud_agent_platform/api_key.txt`.
- **Regenerable artifacts** — `metrics/MauveOnPothana/embeddings_cache/`,
  `dataset/backup/`, virtualenvs, `__pycache__`.

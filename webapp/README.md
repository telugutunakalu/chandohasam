# తెలుగు ఛందస్సు విశ్లేషణ — Telugu Meter Analyzer

A minimalist Flask web app for analyzing Telugu poems. Paste a poem, get its full metrical analysis: identified metre, గణవిభజన (foot division), ప్రాస (rhyme) and యతి (caesura) verdicts, rendered with beautiful typography.

## Install

```bash
cd webapp
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

From the `webapp` directory:

```bash
PYTHONPATH=.. source .venv/bin/activate && python app.py
```

Or, more simply, from the parent `anlp_project` directory:

```bash
cd webapp && PYTHONPATH=.. source .venv/bin/activate && python app.py
```

Then open **http://127.0.0.1:5000/** in your browser.

The `PYTHONPATH=..` tells Python to find the `meter_engine` package in the parent directory. The metre catalogue and DAWG are built once on first request and cached for the life of the process — keep the same `python app.py` process running rather than restarting per request for optimal speed.

## Features

- **Single-purpose tool**: one page, paste a poem, get instant analysis.
- **Clean metrics table**: gaṇa division per pāda in a visual table matching traditional typesetting conventions.
- **Yati verdicts**: caesura checkpoints with position, matched rule, and detailed evidence.
- **Prāsa analysis**: rhyme (alliteration) consonant matching and per-pāda breakdown.
- **Multiple profiles**: analyse under strict, relaxed, or historical rules.
- **Raw report**: plaintext output for detailed diagnostics.
- **Responsive design**: works on desktop and mobile.
- **Beautiful Telugu rendering**: Noto Sans Telugu font with proper line-height and letter-spacing for conjuncts.

## Example

Paste the opening of Pōtana's Bhāgavatam (4 pādas, kandamu metre) to see all features in action:

```
పలికెడిది భాగవత మఁట,
పలికించెడివాడు రామభద్రుం డఁట, నేఁ
బలికిన భవహర మగునఁట,
పలికెద, వేఱొండు గాథ బలుకఁగ నేలా?
```

## Architecture

- **Backend**: Flask + `meter_engine.chandohasam` (native Python engine for metres, prāsa, yati, gana division)
- **Frontend**: plain HTML + CSS (no JS, no framework)
- **Fonts**: Google Fonts Noto Sans Telugu + Inter
- **Dependencies**: `flask`, `pyyaml`, `pytz` (via `meter_engine`)

See `app.py` for the single route and `templates/index.html` for the result rendering logic.

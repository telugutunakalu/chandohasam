# తెలుగు ఛందస్సు విశ్లేషణ — Telugu Meter Analyzer

A minimalist Flask web app for analyzing Telugu poems. Paste a poem, get its full metrical analysis: identified metre, గణవిభజన (foot division), ప్రాస (rhyme) and యతి (caesura) verdicts, rendered with beautiful typography.

## Run

```bash
cd webapp && ./run.sh                  # first run creates .venv and installs requirements.txt (flask, pyyaml)
```

or by hand:

```bash
cd webapp
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python app.py                       # http://127.0.0.1:5000/
PORT=12345 .venv/bin/python app.py            # another port
```

`app.py` puts the repository root on `sys.path` itself, so `meter_engine` is found from any working directory. The
server listens on 127.0.0.1 only, in Flask's debug mode; it is a local tool and is not hosted (the hosted app is
`human_evals/annotation_app`). The metre catalogue and DAWG are built on the first request and kept for the life of
the process.

## Features

- **Single-purpose tool**: one page, paste a poem, get instant analysis.
- **Clean metrics table**: gaṇa division per pāda in a visual table matching traditional typesetting conventions.
- **Yati verdicts**: caesura checkpoints with position, matched rule, and detailed evidence.
- **Prāsa analysis**: rhyme (alliteration) consonant matching and per-pāda breakdown.
- **Multiple profiles**: analyse under strict, relaxed, or historical rules.
- **Raw report**: plaintext output for detailed diagnostics.
- **Responsive design**: works on desktop and mobile.
- **Beautiful Telugu rendering**: Noto Sans Telugu font with proper line-height and letter-spacing for conjuncts.
- **DAWG demo** (`/dawg`, the "▶ DAWG demo" button): a three.js walk-through of the metre DAWG reading the poem one akshara per click. See below.

## DAWG demo

The "▶ DAWG demo" button (or `/dawg`) opens the poem in a 3D view of the line-level metre DAWG of
`meter_engine/indic_meter_dawg` (1,431 states, 2,514 edges, 37 metres / 40 slots), laid out by depth
from START. **Next** (→ / Space) reads one akshara: the walker takes the guru or laghu edge, the part of
the DAWG it can no longer reach fades, and the right-hand list shows which (metre, slot) hypotheses are
still alive, where each one stands in its gaṇa template, and at which akshara the others died. Each pāda
ends with the accept labels (and the pādānta reading of a final laghu), and the last step is the stanza
layer: which metre accepts every pāda in its slot pattern, and the gaṇa division of the winner.
**Change poem** loads one of the bundled examples (kandam, utpalamala, śārdūla, champakamala, tētagīti,
sīsam + āṭaveladi, a vikalpa reading, a v1-generated poem) or any pasted text.

The **v1 / v2** toggle switches to the v2 constraint of `meter_engine/metrical_decoder` (plan §17,
commit c93ee08). The metre DAWG is unchanged; under it the page reads the two corpus layers akshara by
akshara: **Layer A**, the akshara inventory (3,874 syllables attested in `dataset/*.json`; a ring at the
walker, a red badge on the poem), and **Layer B**, the suffix automaton (word DAWG) over the 170,211
corpus words of two aksharas or more (the lane under the graph: begins a real word / inside one / in
none, and a verdict at each word's end). Poems from the corpus are attested by construction; the
v1-generated example shows what the layers catch. Layer B is built on the first v2 request (about 6 s,
about 1 GB of memory) and kept for the life of the process.

Everything shown comes from the engines: `dawg_demo.py` steps `default_dawg().dfa`, takes liveness from
`dawg.reachable`, uses the reading level and half-line grouping `identify_text` used, and reports the
verdict `chandohasam.analyze` reports. `test_dawg_demo.py` checks the per-pāda accept and pādānta sets
against `walker.walk_options`, the verdict against `analyze`, and the v2 words against the corpus
tokenizer:

```bash
cd webapp && ../.venv/bin/python -m unittest test_dawg_demo -v     # 7 tests, ≈ 10 s; needs no Flask
```

three.js 0.160.0 is loaded from the jsDelivr CDN, so the demo page needs network access (as the fonts do).

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
- **Frontend**: plain HTML + CSS for the analyzer (no JS); the DAWG demo is `templates/dawg_demo.html` + `static/js/dawg_demo.js` (three.js, ES modules)
- **DAWG demo data**: `dawg_demo.py` (graph layout, akshara-by-akshara trace, v2 layers), served at `/api/dawg/graph` and `/api/dawg/trace`
- **Fonts**: Google Fonts Noto Sans Telugu + Inter
- **Dependencies**: `flask`, `pyyaml`

See `app.py` for the routes and `templates/index.html` for the result rendering logic.

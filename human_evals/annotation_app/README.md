# Padya-eval: human evaluation app for the Chandohasam poems

A small Flask app for rating the 500 poems of the human-evaluation pool
(`../human_eval_poems_strict.json`) with a ten-question rubric. It is built so
that the ratings support inter-annotator agreement. It works on phones and on
desktops.

For every poem an annotator sees:

- the poem, with the **yati** aksharas (purple, double underline) and the
  **prāsa** akshara (orange, single underline) marked;
- beside each line (below it on phones), that line's **prāsa akshara** and its
  **yati aksharas with the yati rule**, e.g. `ప్రాస ప · యతి త – ద – వర్గజ యతి`;
- under the poem, a summary of the prāsa aksharas (`ప · పం · పం · ప — 'ప'కార ప్రాస`);
- the **గణవిభజన** (gaṇa division) as a table. Each pāda takes three rows: the
  gaṇa names, the guru/laghu marks (`U` / `|`), and the aksharas grouped by
  gaṇa. A ✔ marks every pāda that fits the meter;
- a **📖 నియమాలు / Rules** button. It opens the ruleset reference: this poem's
  meter card, the guru/laghu rules, the gaṇa tables, yati-maitri, the prāsa
  rules and the rubric guide;
- the **evaluation form**: the ten questions, then a comments box.

The gaṇa division, the guru/laghu marks and the yati/prāsa positions are
**static**. `build_data.py` computes them once with `meter_engine` (the
indic_meter_dawg DAG scanner, plus the prāsa and yati engines), and the app
only reads the resulting JSON. Every annotator therefore sees exactly the same
analysis, and the server needs nothing but Flask.

Ratings are stored in **one SQLite file**, `instance/annotations.db`. The pages
are light by default. The ☾/☀ button in the top bar switches to dark mode, and
each device remembers the choice.

---

## 1. Run it on your machine

```bash
cd human_evals/annotation_app
./run.sh
```

Then open <http://127.0.0.1:5000>, pick a username and start rating.

- On first use, `run.sh` creates `.venv` and installs Flask.
- The admin dashboard is at <http://127.0.0.1:5000/admin>. Its password is
  `admin` unless you set `HE_ADMIN_PASSWORD`.
- `HE_DEBUG=1 ./run.sh` turns on auto-reload. Use it only on your own machine,
  because the debugger allows code execution.
- To try the app from a phone on the same Wi-Fi, use gunicorn (see section 2)
  with `-b 0.0.0.0:8000`, then open `http://<your-laptop-ip>:8000` on the phone.

Manual setup, if you prefer:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt     # flask, gunicorn, pyyaml, pytest
.venv/bin/flask --app wsgi run
```

## 2. Host it for the annotators

```bash
cd human_evals/annotation_app
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
export HE_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
export HE_ACCESS_CODE="something-you-share-with-annotators"
export HE_ADMIN_PASSWORD="something-only-you-know"
.venv/bin/gunicorn -w 2 -b 0.0.0.0:8000 wsgi:app
```

Put it behind HTTPS (nginx, Caddy, or a platform's proxy). Then also set
`HE_BEHIND_PROXY=1` and `HE_SECURE_COOKIES=1`. Health check: `GET /healthz`.

| Variable | Default | Meaning |
|---|---|---|
| `HE_SECRET_KEY` | random, kept in `instance/secret_key` | Signs the session cookies. Set it explicitly when hosting. |
| `HE_ACCESS_CODE` | none | When set, annotators need this code to log in. |
| `HE_ADMIN_PASSWORD` | none (admin disabled) | Password for `/admin`. |
| `HE_DATABASE` | `instance/annotations.db` | The SQLite file holding all ratings. |
| `HE_RATINGS_PER_POEM` | `all` | `all`: every annotator rates all 500 poems. A number k: share the poems out until each has k ratings. |
| `HE_CALIBRATION_SIZE` | `25` | Poems that every annotator rates first. Fixed in the DB on first start. |
| `HE_CLAIM_TTL_MINUTES` | `30` | How long a served poem stays reserved for its annotator. |
| `HE_SHOW_ENGINE_CHECKS` | `1` | `0` hides the engine's verdicts: the ✔ column, the yati rule names and the prāsa label (see section 4). |
| `HE_BEHIND_PROXY` / `HE_SECURE_COOKIES` | off | Set both to `1` behind an HTTPS proxy. |
| `HE_DATA_DIR`, `HE_INSTANCE_DIR` | `data/`, `instance/` | Where the poem JSON and the instance files live. |

**Backups.** The whole study is one file. To copy it safely while the app is
running:

```bash
sqlite3 instance/annotations.db ".backup 'annotations-$(date +%F).db'"
```

**Annotators** log in with a username: 2–40 letters, digits, `.`, `-` or `_`.
They must use the same username on every device so their ratings stay
together. Sessions last 30 days.

## 3. How the poems are assigned (inter-annotator agreement design)

**Default: everyone rates all 500 poems** (`HE_RATINGS_PER_POEM=all`). The
design is fully crossed, which is the strongest design for agreement.

1. **Calibration set first.** Every annotator starts with the same 25 poems.
   The set is stratified by source and spread across meters. Agreement on it
   can be checked on `/admin` early, before the long pass.
2. **Then the other 475.** Each annotator gets them in their own fixed
   pseudo-random order. This spreads fatigue and order effects, and the order
   stays stable across reloads and devices.

**Alternative: k ratings per poem** (`HE_RATINGS_PER_POEM=3`), for when there
are too many annotators for everyone to do all 500.

3. **Shared out.** After the calibration set, a poem is served until it has k
   ratings.
4. **Depth-first.** Poems that already have ratings are completed first, so if
   annotation stops early you still have fully rated poems.
5. **Claims.** A served poem is reserved for its annotator for 30 minutes, so
   people working at the same time do not all receive the same poem.

**In both modes:**
- **Skip.** "Skip" sends a poem to someone else. An annotator never sees a
  poem again once they have rated or skipped it. A skipped poem stays listed
  under *Mine*, where it can still be rated.
- **Blind rating.** Annotators never see the source, author, title or
  generator of a poem. The admin export joins those fields back in.

**Rubric** (`padya_eval/rubric.py`; edit the wording there):

1. How easy is it to read? (1–5)
2. How easy is it to understand immediately after reading? (1–5)
3. How easy is it to recognize and understand the words in the poem? (1–5)
4. How close is the poem with the bhavam? (1–5)
5. Is chandassu correct? (0/1)
6. Is prasa correct? (0/1)
7. Is yathi correct? (0/1)
8. Were you able to identify any shabda alankaras? (0/1)
9. Were you able to identify any artha alankaras? (0/1)
10. How poetic is it? (1–5)

Then an optional comments box.

- The bhavam sits inside question 4 and stays hidden until the annotator
  clicks it, so questions 1–3 measure first-pass understanding.
- Question 4 is shown as *not applicable* when a poem has no bhavam.
- Question 6 is *not applicable* when the meter has no prāsa (సీసము, తేటగీతి,
  ఆటవెలది).
- *Not applicable* answers are stored as `null` and left out of the agreement
  statistics.

**Agreement statistics.** They are on `/admin`, and in
`agreement.json` / `agreement.md`, for all poems and separately for the
calibration set:

- **Krippendorff's α**: ordinal for the 1–5 questions, nominal for the yes/no
  ones. It handles missing ratings and any number of annotators. It is checked
  against the `krippendorff` package and against the worked example in
  Krippendorff (2011).
- **Agreement shares**: the % of rater pairs that agree, and (for 1–5
  questions) the % within ±1.
- **Yes/no questions**: Fleiss' κ, and Gwet's AC1. AC1 stays meaningful when
  nearly every answer is "yes"; κ does not (the prevalence paradox).
- **Mean pairwise Cohen's κ**: quadratic-weighted for the 1–5 questions. It is
  checked against `sklearn`.
- **Bootstrap 95% CIs** for α: on `/admin`, click *add bootstrap 95% CIs*.
- **Per-annotator diagnostics**:
  - workload and median seconds per poem;
  - leave-one-out Δα: a clearly positive value means the others agree better
    without that annotator;
  - mean κ with the other annotators.

**Exports** (admin): `annotations.csv` (one row per annotator × poem, with
source columns), `annotations.json`, `agreement.json`, `agreement.md`. From
the command line:

```bash
.venv/bin/python -m padya_eval.report --db instance/annotations.db --out reports/ --bootstrap 1000
```

## 4. The poem data

`data/poems.json` and `data/reference.json` are generated. Rebuild them after
`meter_engine` changes, or to use another pool:

```bash
.venv/bin/python build_data.py                  # strict pool (default): every poem passes meter + prāsa + yati
.venv/bin/python build_data.py --pool relaxed   # or historical
```

- The build stops without writing anything if any poem fails to analyse or its
  aksharas do not line up with the printed text.
- `tests/test_data.py` re-runs the engine on a sample of poems and fails if the
  shipped JSON is stale.
- A database remembers which pool it was created for. Use a new `HE_DATABASE`
  after switching pools.

**Bhavam coverage (strict pool).** It comes from the corpora:

| Source | Poems | Where the bhavam comes from |
|---|---|---|
| Bhāgavatam | 198 | `bhavam` field of `dataset/bhagavatam.json` |
| Vemana, Kūcimañci | 117 | LLM gloss from batch run5 (`generated.bhavam`) |
| Generated poems | 84 | The poem's `meaning_telugu` |
| Bhāgavatam | 29 | None |
| Textbook reference examples | 72 | None |

The 101 poems with no bhavam show question 4 as not applicable. To fill them,
put a `data/bhavam_overrides.json` of the form
`{"he_0005": {"te": "…", "en": "…", "source": "manual"}}` and rebuild.

**Note on the engine's verdicts.** Three things show the engine's verdict: the
✔ beside each pāda, the yati rule names beside each line, and the prāsa label.
In the strict pool every poem passes, so annotators see a "correct" reading on
every poem, which can anchor answers to questions 5–7. Set
`HE_SHOW_ENGINE_CHECKS=0` to keep the aksharas and underlines but hide the
verdicts.

## 5. Tests

```bash
.venv/bin/python -m pytest          # 103 tests, about 8 s
```

They cover:

- the agreement statistics, against published examples and sklearn/krippendorff values;
- the queue: calibration, k, claims, skips, and a full simulated study;
- the integrity of the data: lossless text, gaṇa and marks, freshness against `meter_engine`;
- every route: login, access code, CSRF, blind rating, *not applicable*
  handling, validation, edits, skips, reference, admin, exports;
- the report CLI.

## 6. Files

```
annotation_app/
├── build_data.py          offline: meter_engine → data/poems.json, data/reference.json
├── data/                  generated poem and ruleset data (static, preloaded)
├── padya_eval/
│   ├── __init__.py        create_app() and configuration
│   ├── views.py           annotator pages (login, queue, poem form, reference)
│   ├── admin.py           dashboard and exports
│   ├── assignment.py      calibration set, k-redundant depth-first queue, claims
│   ├── agreement.py       α, κ, AC1, bootstrap (standard library only)
│   ├── report.py          agreement report, CSV/Markdown export, CLI
│   ├── rubric.py          the ten questions
│   ├── db.py              SQLite schema and queries
│   ├── store.py           read-only access to data/*.json
│   ├── security.py        sessions, CSRF, guards
│   ├── templates/         Jinja templates (_gana.html is the gaṇa table)
│   └── static/            app.css, app.js (progressive enhancement only)
├── tests/
├── wsgi.py                gunicorn entry point
└── run.sh                 local server
```

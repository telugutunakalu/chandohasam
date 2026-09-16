# Telugu prāsa (ప్రాస) ruleset — `meter_engine/prasa_rules.yaml`

A programmable, exhaustively documented lookup table and rule catalogue for the
Telugu second-syllable rhyme (prāsa), distilled from `Notes/Prasa.md`, plus a
reference engine that returns a **provenance trail** for every verdict.

| File | Role |
|---|---|
| `prasa_rules.yaml` | The ruleset: profiles, alphabet, akshara model, 62 rules, consonant-pair lookup table, Appakavi's 17 cross-reference, decision procedure, trail schema, 87 attested fixtures |
| `prasa_engine.py` | Reference implementation (reads the YAML; splits pādas with `aksharanusarika_v0.0.6a.py` from the project root) |
| `tests/test_prasa_rules.py` | Deterministic verification of the table, the rules and the fixtures |
| `run_corpus.py` | Runs the engine over a poems corpus (`dataset/bhagavatam.json` layout) and writes JSONL + CSV results and a Markdown summary |
| `corpus_runs/bhagavatam_*` | The full Bhāgavatam run: every poem's verdict, label, classifications, violations (`_results.jsonl`, `_results.csv`) and the aggregate report (`_summary.md`) |

## Quick start

```bash
cd meter_engine
python3 prasa_engine.py check --profile strict "పొందింప" "బృందావన" "బిందీవరాక్షి" "నందన"
python3 prasa_engine.py check --json --profile relaxed --meter kandamu "జలధర గభీర రవమున" "నళినదళాక్షుండు దమ్మునామాంకములం" "బిలిచిన విని ప్రతిఘోషణ" "ములుజేయుచుఁ బసులు దిరిగెముదమున నధిపా!"
python3 prasa_engine.py lookup స శ          # one consonant pair
python3 prasa_engine.py matrix --tsv        # all 630 pairs
python3 prasa_engine.py rules               # the catalogue
python3 prasa_engine.py examples            # replay the fixtures
```

```python
import sys; sys.path.insert(0, "meter_engine")
import prasa_engine as pe
res = pe.evaluate(["బిసరుహ", "మసకపుఁ", "దశరథసూను", "పశుపతి"], profile="strict")
res.matched            # False
res.min_profile        # 'relaxed'  -> would match under the relaxed profile
res.label_te           # 'స-శ ప్రాసము (ప్రాసమైత్రి)'
res.violations         # [{'rule': 'PRASA-MAITRI-SA-SHA', 'scope': 'pair:1-3', 'detail': ...}, ...]
res.trail              # ordered rule-by-rule evaluation with pass/fail/info and data
```

## Profiles

| Profile | Accepts | Meaning |
|---|---|---|
| `strict` | canonical, canonical_subtype, mandatory | tulyākṣara niyamamu: identity of the effective onset + all binding context rules (ం/ః before the prāsa, conjunct identity and order, dead-consonant fusion, pre-prāsa weight) |
| `relaxed` | + accepted_relaxation, orthographic_relaxation | + prāsamaitri the lākṣaṇikas sanction: స~శ, థ~ధ, న~ణ, ల~ళ, ఋ~ర, Cృ~C్ర, vikalpa, wide khaṇḍākhaṇḍa, the bindu ~ saṁśleṣa spellings of one drutam (ంద ~ న్ద); plus the orthographic relaxation ర~ఱ, a project decision because printed corpora do not distinguish the two (the treatise rule is kept and named in the trail as superseded) |
| `historical` | + deprecated | + apraśasta forms for identification: స~ష, ల/ళ~డ, ద~ధ, saṁyuktāsaṁyukta, anunāsika, ంబ~మ్మ |

Forbidden pairs (ట≠డ, ద≠డ, డ≠ఢ, ర≠ల, క≠ఖ … and every unlisted pair) and
the named defects (pūrṇārdhabindu, adhika, śānta) fail under every profile but
are **named** in the trail.

## How a verdict is produced

1. Each pāda is sanitised and split into aksharas with aksharanusarika; the 1st
   akshara is the pre-prāsa akshara, the 2nd the prāsa akshara.
2. The prāsa akshara is decomposed into onset consonants / vowel / trailing
   signs; a dead consonant on the 1st akshara fuses into the onset
   (నిన్ వదలి → న్వ); ౘ/ౙ are read as చ/జ.
3. Every pair of pādas is compared: pūrṇabindu and visarga before the prāsa
   must agree; ardhabindu is classified (uniform / mixed by authority); then the
   onset comparison runs in a fixed order (ఋ~ర, krārakommu block, identity,
   Cృ~C్ర, vikalpa, element-wise maitri table, saṁyuktāsaṁyukta, adhika,
   conjunct-vs-simple).
4. The pre-prāsa weight rule is checked at stanza level (skipped for
   `meter_class="asama_vritta"`).
5. `min_profile` is the least permissive profile whose accepted statuses cover
   every rule the match used; `violations` lists what the requested profile
   rejects, with the pair and the reason.

The full procedure is written out in the YAML under `evaluation_pipeline`; the
shape of the output under `trail_schema`.

## Extending

* New consonant equivalence: add a `{consonants: [a, b], rule: …}` row to
  `maitri_table.pairs` and, if needed, a rule with the right `status`.
* New profile: add it to `profiles` and `profile_order`.
* New light-repha words: append to `light_repha_lexicon.stems`.
* New fixture: append to `attested_examples`; the test suite replays it.

## Corpus run

```bash
python3 meter_engine/run_corpus.py --dataset dataset/bhagavatam.json --out meter_engine/corpus_runs/bhagavatam
```

Prose records are skipped; every verse record is evaluated. Metres without a
prāsa rule (సీసము, తేటగీతి, ఆటవెలది) are reported separately as "incidental".
The metre table at the top of `run_corpus.py` records, per metre, whether prāsa
is required and how the corpus prints the pādas (సీసము as 8 half-lines,
లయగ్రాహి / లయవిభాతి / మానిని as 8 lines for 4 pādas). The JSONL output is
byte-identical across runs of the same inputs (its sha256 is printed in the
summary), so it can serve as a regression baseline.

Two poems that the run exposed as mislabelled (9-198 and 10.1-322, printed as
కందము but scanning as ఆటవెలది) were relabelled in `dataset/bhagavatam.json` and
`.txt`; the change is logged in `dataset/CORRECTIONS.md` and the originals are
kept in `dataset/backup/`.

## Tests

```bash
python3 -m unittest discover -s meter_engine/tests -v     # standard library only
python3 -m pytest meter_engine/tests                      # if pytest is available
```

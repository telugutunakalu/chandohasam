# Telugu యతి (yati) engine — `meter_engine/yati_engine.py`

A pair-level yati matcher with a provenance trail, data-driven by
`yati_rules.yaml`, whose rule ids are those of `yathi_docs/yathi_compact.md`
(the parsable distillation of పద్యవిద్య ch. 6). It is the yati counterpart of
the prāsa ruleset (`prasa_rules.yaml` / `prasa_engine.py`) and is meant to be
called from the metrical DAWG once a meter and its yati positions are known.

| File | Role |
|---|---|
| `yati_rules.yaml` | profiles, alphabet, the consonant-pair lookup table, bindu table, vowel bridges, ఋ/ఌ detachment, sandhi readings, ubhaya triggers, blockers, 91-rule catalogue, 107 fixtures |
| `yati_engine.py` | `check(a, b)` for a pair, `evaluate_line(...)` for a pāda, `evaluate_stanza(...)` through the DAWG, `lookup_pair` / `maitri_matrix` table views, CLI |
| `tests/test_yati_rules.py` | 34 tests: ruleset integrity (ids/statuses cross-checked against `yathi_compact.md`), table symmetry, parsing, readings, fixtures, verdict policy, line/stanza, CLI |

## Quick start

```bash
cd meter_engine
python3 yati_engine.py check క గా                  # YATI-VY-02.1 వర్గజ యతి
python3 yati_engine.py check ంత న                  # YATI-VY-03 బిందు యతి  (leading ం = preceding anusvāra)
python3 yati_engine.py check న్+సా న్య              # YATI-VY-01 via YATI-SY-08 (fused drutam of the previous line)
python3 yati_engine.py check అ దా                  # YATI-SV-02 [sandhi hypothesis]  (వేద+అర్థ)
python3 yati_engine.py check అ దా --sandhi off     # NO — YATI-RJ-03
python3 yati_engine.py check ర ఱ --profile relaxed # YATI-SP-08 (orthographic relaxation)
python3 yati_engine.py check అ ప్రా --word-b ప్రాప్తి --index-b 0 --sandhi off   # YATI-UB-10 ప్రాది యతి
python3 yati_engine.py lookup శ చ ; python3 yati_engine.py matrix --tsv
python3 yati_engine.py line "పుణ్యుఁడు రామచంద్రుఁ డట పోయి ముదంబునఁ గాంచె దండకా" --yati 1,10
python3 yati_engine.py stanza --file poem.txt        # identify with the DAWG, then check every yati
python3 yati_engine.py examples                      # replay the fixtures
```

```python
import sys; sys.path.insert(0, "meter_engine")
import yati_engine as ye
r = ye.check("శ్రీ", "చె")           # both aksharas as strings (or scansion Syllable objects)
r.matched, r.rule, r.label_te        # True, 'YATI-VY-12', 'సరసయతి (శ-చ)'
r.best.vidhana                       # ('YATI-SY-01',)  — శ్రీ read as శీ
r.candidates, r.rejected             # every positive pairing / every named failure
r.min_profile                        # 'strict' | 'relaxed' | 'historical' | None
r.explain(); r.to_json()

ly = ye.evaluate_line(syllables, [(1, 10)], profile="relaxed", prev_line_dead=["న"])
st = ye.evaluate_stanza(text)        # uses indic_meter_dawg.identify_text for positions
```

## How a verdict is produced

1. **Parse** each side (`YATI-EP-02`): onset, vowel, marks; ఁ and marks *on* the
   akshara are ignored; a *preceding* ం is a flag (adds బిందు pairs); a preceding
   dead న్/ల్ joins the onset (సంశ్లేషము).
2. **Readings** (`YATI-EP-03`), ranked 0–5: the written consonant + vowel (0);
   every other cluster constituent, a fused predecessor, a confirmed sandhi
   split (1); ఋ/ఌ detachment and whole-cluster equivalences జ్ఞ / స్న (2); an
   ubhaya vowel opened by a word-context trigger (3); a svara-pradhāna sandhi
   hypothesis from the written vowel alone (4); hidden-vowel hypotheses (5).
   Blockers close a track (verbal -ఎడు, క్యచ్, elided అది, augments).
3. **Lookup** (`YATI-EP-04`): svara×svara by vowel class; hal×hal by the pair
   table (identity, generated vargaja, bindu table, conditional ము-pairs,
   explicit relaxations and forbidden pairs); svara×hal by the vowel bridges
   (అ-య, అ-హ, ఋ-రి, ఌ-లి). Vowel classes must agree.
4. **Rank**: the accepted candidate with the lowest rank sum wins; failures are
   kept by name (`YATI-RJ-*`).

**Sandhi modes.** `off` (nothing hypothesised), `hypothesis` (default), and
`acchu` — the vowel-only acceptance path borrowed from
`telugu_prosody_engine` (`experimental_sandhi` / worldtree `sandhi=True`):
two coordinates whose vowels share a class pair even without evidence of a
sandhi on either side (`YATI-SV-02.10`, accepted_relaxation, always flagged as
a hypothesis). The legacy checker applied it as an *override* of the consonant
verdict; here it is additive only. Two other legacy paths were reviewed and
NOT borrowed because the book rejects them: "two aksharas both carrying ం pair
on the bindu" (YATI-MOD-02 says ం on the akshara has no effect) and the
"ల ళ డ ర" super-group (ర-డ is an unsanctioned transitive bridge, YATI-RJ-02).

**Sandhi policy.** A hypothesis (rank ≥ 4) is allowed on *one* side only;
otherwise any two same-class aksharas would match. At line level,
`sandhi_evidence` promotes readings that the printed text supports (a word
opening after a word ending in ఁ → rank 1; a word-initial lone న/య → rank 2), so
two-sided cases like బె ↔ డె (బు+ఎవ్వఁడు ↔ డు+ఎవ్వఁడు) still pass. Every
hypothesis match is flagged (`best.hypothesis`, "[sandhi hypothesis]").

## Profiles

Same contract as the prāsa ruleset: `strict` (canonical / mandatory),
`relaxed` (+ accepted_relaxation: ర-ల, ద-డ generalised, స్నా-త, విశ్వామిత్ర vowel;
+ orthographic_relaxation ర-ఱ), `historical` (+ identifies deprecated forms such
as a బహుయతి constituent switch). Forbidden pairs never match and are named.

## Line and stanza level

`evaluate_line` takes akshara strings or `indic_meter_dawg.scansion.Syllable`
objects and yati **groups** (`[(1,10)]`, `[(1,8,15)]`, సీసము `[(1,g3),(g5,g7)]`).
It applies the preceding anusvāra / drutam of the previous syllable, the
previous line's drutam (`prev_line_dead`), బహుయతి నియతి for groups of three or
more (`seesam_halves=True` exempts), and the prāsa-yati fallback
(`allow_prasa_yati=True`, reusing `prasa_engine.lookup_pair`, with the
ప్రాసపూర్వాక్షర weight check). `evaluate_stanza` gets the meter and positions
from the DAWG (`identify_text`), rebuilds సీసము pādas from printed half-lines,
and reads `prasa_yati` / `halves_per_line` from `meter_rules.yaml`.

Full Pothana corpus (7,317 catalogued poems, `reports/yati_run_2026-09-14.md`):
strict/off 63.6%, strict/hypothesis 90.7%, relaxed/hypothesis 91.5%,
relaxed/acchu 99.9% (10 poems fail). `telugu_prosody_engine` passes the
remainder only through its vowel-only override or its "both aksharas carry ం"
quirk; the ten residual poems are vowel-class breaches on identical or
same-varga consonants (చ్చ↔చీ, నె↔నొ, మృ↔ము, బ్బు↔ప, ల↔ళిం) and pairs with no
maitri (డొ↔జం, త్రి↔బ్ర, డి↔హ్లా), i.e. edition/text issues or genuine lapses,
not missing rules.

`scripts/yati_corpus_run.py` runs the whole Pothana corpus (identify once,
evaluate under strict/off, strict/hypothesis, relaxed/hypothesis and
relaxed/acchu) and writes `reports/yati_run_<date>.{json,md}` with per-meter
pass/fail counts, the rules that satisfied each group, the named failure
reasons and every failing poem.

## Known limits

- Ubhaya triggers are a lexical heuristic (suffixes, the prādi prefix table, a
  nitya-samāsa lexicon, name suffixes); they need the word and the akshara index.
- §6.25 ముకార యతి is reconstructed (its body is missing from `yathi.md`);
  the engine folds it into the conditional ము-pairs (`YATI-VY-16`).
- Prāsa-yati fallback compares single onset consonants or identical clusters
  only; cluster-level prāsa subtleties stay in `prasa_engine`.

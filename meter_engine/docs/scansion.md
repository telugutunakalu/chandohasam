# Guru/laghu marking (scansion) — `indic_meter_dawg.scansion`

Turns Telugu text into the U/I lines the DAWG identifies. Re-implemented
from the Indic NeuroSym mid-project report (Phase 5, §3: codepoint
classifier → syllable assembler → guru/laghu classifier), rules grounded in
Chandodarpanam. Only the Telugu marker is taken from that project; its
dwipada NFAs are not needed here because the DAWG covers every meter.

```
text ──classify_char──▶ categories ──syllabify──▶ aksharas ──classify──▶ U/I (+ rules, vikalpa)
```

## The rules

A syllable is **guru (U)** when any of these holds, else **laghu (I)**:

| id | Telugu | condition | example |
|---|---|---|---|
| `deergha` | దీర్ఘము | long vowel ఆ ఈ ఊ ౠ ఏ ఓ ౡ (or the sign) | రా |
| `sandhyakshara` | సంధ్యక్షరము | diphthong ఐ ఔ / ై ౌ | కై |
| `anusvara` | అనుస్వారము | full sunna ం (the arasunna ఁ adds nothing) | సం |
| `visarga` | విసర్గ | ః | నః |
| `pollu` | పొల్లు | the syllable ends in a dead consonant (C్), which is merged into it | సెన్ |
| `samyukta` | సంయుక్తాక్షర పూర్వము | the **next** syllable of the **same word** begins with a conjunct or double consonant | స in సత్యము |

Everything else is laghu, including ఋ/ృ and short vowels before a conjunct
that starts the next word.

## Two readings the tradition leaves open (vikalpa)

The scanner never decides these silently. It picks the reading the policy
says and records the other one on the syllable, so the identifier can try
it when the canonical pattern matches no meter.

| vikalpa | situation | default (`ScanPolicy`) | switch |
|---|---|---|---|
| `word_initial_conjunct` | a laghu before a conjunct that begins the next word (`స త్యము`) | laghu — a space blocks rule 5, as in the report | `word_initial_conjunct="guru"` |
| `repha_conjunct` | a syllable before a ర-vattu conjunct (`చక్రి`, `ప్రస్తుతం`) | guru — rule 5 as written | `repha_conjunct="laghu"` |

A newline always blocks rule 5; a line-final laghu that the meter wants as
guru is covered by the pādānta rule in the identifier, not by the scanner.

## How the identifier uses the open readings

Instead of enumerating combinations, `identify_text` hands the DAWG a
**lattice**: each akshara offers one symbol or two (`'UI'` = canonical
guru, laghu admissible), and the walker simulates the automaton over sets of
states, so every combination is tried at once and the accepted pattern per
meter is recovered as a witness. Three reading levels are tried in order,
and the level that succeeds is written into `result.notes` with the exact
aksharas that were read the other way:

| level | what may be read the other way |
|---|---|
| `canonical` | nothing: the scanner's weights |
| `vikalpa` | the two open readings above, where the scanner recorded them |
| `compound` | additionally, any guru that is guru *only* because a conjunct follows — the conjunct may begin a word inside a compound written without a space (Pothana 10.1-126.1: జొరఁగవ్యక్త, where the గ before వ్య is laghu) |

`identify` itself accepts such option lines directly (`identify([["U","IU","I", …], …])`),
and `LineScansion.variants()` still enumerates the vikalpa patterns for
inspection.

## What the scanner does with the rest

- punctuation, digits, Latin text: boundaries, no syllable;
- zero-width joiner/non-joiner: a `్` followed by ZWNJ is a pollu, not a conjunct;
- a stray vowel sign or anusvara with no base letter: attached to the previous syllable of the word, or dropped;
- input is NFC-normalised, so decomposed ై / ౌ scan the same as composed ones.

## Use

```bash
python3 -m indic_meter_dawg scan "శ్రీరాముని దయచేతను"            # aksharas | U/I | vikalpa positions
python3 -m indic_meter_dawg scan --rules "చక్రి"                   # which rule fired per akshara
python3 -m indic_meter_dawg identify --text --file poem.txt        # Telugu lines → meter
python3 -m indic_meter_dawg identify --text --repha-conjunct laghu --file poem.txt
```

```python
from indic_meter_dawg import scan, identify_text, ScanPolicy
scan("ఇందు గలఁ డందు లేఁ డని")[0].format()
# 'ఇం దు గ లఁ డం దు లేఁ డ ని | UIIIUIUII | vikalpa@-'
res = identify_text(poem_text)                       # res.best.meter, res.scansions, res.notes
res = identify_text(poem_text, policy=ScanPolicy(word_initial_conjunct="guru"))
```

Each `Syllable` carries `text`, `onset` (the consonant cluster), `vowel`,
`anusvara`/`visarga`/`candrabindu`, `dead` (merged pollu), `word`,
`start`/`end` offsets, `weight`, `rules` and `vikalpa`; `first_sound` is what
the yati engine will look at.

## Checked against

- every worked example in the report (నమస్కారం, పూసెన్, తెలుగు భాష, స్త్రీ, మంచి, తనుము ళ్ళరాస్తుంది);
- the hand-scanned classics in `tests/fixtures/classics.yaml` (Pothana utpalamala and kandam, Sumati, Vemana): scanner output equals the hand scansion and `identify_text` returns the expected meter;
- the older splitter `aksharanusarika` in the project root, on the same lines (syllable boundaries agree);
- the full Pothana corpus run is scheduled next (see plan).

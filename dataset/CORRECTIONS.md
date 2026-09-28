# Corpus corrections

Backups of the untouched files are in `dataset/backup/`.

## 2026-09-13 — two poems relabelled కందము → ఆటవెలది

| old id | new id | reason |
|---|---|---|
| 9-198-క. | 9-198-ఆ. | lines scan as ఆటవెలది (prosody engine 100%); no 2nd-akshara prāsa; found by the meter_engine prāsa corpus run |
| 10.1-322-క. | 10.1-322-ఆ. | same |

Fields changed in `bhagavatam.json`: `id`, `metre_code`, `metre`, `metre_roman`; the original
values are kept in a new `metre_corrected` object on each record (edited textually, so every
other byte of the file is unchanged). The matching header lines in `bhagavatam.txt` were renamed.
No other record references these ids.

## 2026-09-14 — two poems relabelled (found by the scansion + metrical DAWG corpus sample)

| old id | new id | reason |
|---|---|---|
| 10.1-1322-ఉ. | 10.1-1322-శా. | all four lines scan as శార్దూలవిక్రీడితము (4 × 19 aksharas, మ స జ స త త గ); ఉత్పలమాల dies at akshara 1 |
| 10.2-966.1-ఆ. | 10.2-966.1-తే. | all four lines scan as తేటగీతి (హ + 2 indra + హ హ); ఆటవెలది dies in every line |

Same procedure as above: `id`, `metre_code`, `metre`, `metre_roman` changed textually, originals kept
in `metre_corrected`; header lines in `bhagavatam.txt` renamed. The seesam parent 10.2-966-సీ. carried
`child_id: 10.2-966.1-ఆ.`, updated to the new id. Reviewed against the scansion output
(`python3 -m indic_meter_dawg identify --text`), not against the printed source.

## 2026-09-14 — 23 poems relabelled (scansion + metrical DAWG full-corpus run)

| old id | new id | from → to | reason |
|---|---|---|---|
| 1-259-ఉ. | 1-259-మ. | utpalamala → mattebhavikriditamu | all 4 lines scan as mattebhavikriditamu (meter_engine identify_text); utpalamala does not fit (record inserted into the json; no header line in bhagavatam.txt) |
| 4-890.1-తే. | 4-890.1-ఆ. | tetagiti → aataveladi | all 4 lines scan as ataveladi (meter_engine identify_text); tetagiti does not fit |
| 5.1-149.1-తే. | 5.1-149.1-ఆ. | tetagiti → aataveladi | all 4 lines scan as ataveladi (meter_engine identify_text); tetagiti does not fit |
| 8-629.1-తే. | 8-629.1-ఆ. | tetagiti → aataveladi | all 4 lines scan as ataveladi (meter_engine identify_text); tetagiti does not fit |
| 9-564-ఉ. | 9-564-మ. | utpalamala → mattebhavikriditamu | all 4 lines scan as mattebhavikriditamu (meter_engine identify_text); utpalamala does not fit |
| 9-688-తే. | 9-688-ఆ. | tetagiti → aataveladi | all 4 lines scan as ataveladi (meter_engine identify_text); tetagiti does not fit |
| 9-731.1-ఆ. | 9-731.1-తే. | aataveladi → tetagiti | all 4 lines scan as tetagiti (meter_engine identify_text); ataveladi does not fit |
| 10.1-87.1-తే. | 10.1-87.1-ఆ. | tetagiti → aataveladi | all 4 lines scan as ataveladi (meter_engine identify_text, alternative reading needed); tetagiti does not fit |
| 10.1-129-తే. | 10.1-129-ఆ. | tetagiti → aataveladi | all 4 lines scan as ataveladi (meter_engine identify_text); tetagiti does not fit |
| 10.1-194.1-తే. | 10.1-194.1-ఆ. | tetagiti → aataveladi | all 4 lines scan as ataveladi (meter_engine identify_text); tetagiti does not fit |
| 10.1-248.1-తే. | 10.1-248.1-ఆ. | tetagiti → aataveladi | all 4 lines scan as ataveladi (meter_engine identify_text); tetagiti does not fit |
| 10.1-414-తే. | 10.1-414-ఆ. | tetagiti → aataveladi | all 4 lines scan as ataveladi (meter_engine identify_text); tetagiti does not fit |
| 10.1-474-మ. | 10.1-474-ఉ. | mattebhavikriditamu → utpalamala | all 4 lines scan as utpalamala (meter_engine identify_text); mattebhavikriditamu does not fit |
| 10.1-478-ఉ. | 10.1-478-చ. | utpalamala → champakamala | all 4 lines scan as champakamala (meter_engine identify_text); utpalamala does not fit |
| 10.1-698-మ. | 10.1-698-చ. | mattebhavikriditamu → champakamala | all 4 lines scan as champakamala (meter_engine identify_text); mattebhavikriditamu does not fit |
| 10.1-1298.1-తే. | 10.1-1298.1-ఆ. | tetagiti → aataveladi | all 4 lines scan as ataveladi (meter_engine identify_text); tetagiti does not fit |
| 10.1-1319-మ. | 10.1-1319-ఉ. | mattebhavikriditamu → utpalamala | all 4 lines scan as utpalamala (meter_engine identify_text); mattebhavikriditamu does not fit |
| 10.1-1461-శా. | 10.1-1461-మ. | shardulavikriditamu → mattebhavikriditamu | all 4 lines scan as mattebhavikriditamu (meter_engine identify_text); sardulavikriditamu does not fit |
| 10.1-1533-మ. | 10.1-1533-శా. | mattebhavikriditamu → shardulavikriditamu | all 4 lines scan as sardulavikriditamu (meter_engine identify_text); mattebhavikriditamu does not fit |
| 10.2-110-మ. | 10.2-110-ఉ. | mattebhavikriditamu → utpalamala | all 4 lines scan as utpalamala (meter_engine identify_text); mattebhavikriditamu does not fit |
| 10.2-115-ఉ. | 10.2-115-చ. | utpalamala → champakamala | all 4 lines scan as champakamala (meter_engine identify_text); utpalamala does not fit |
| 10.2-183.1-తే. | 10.2-183.1-ఆ. | tetagiti → aataveladi | all 4 lines scan as ataveladi (meter_engine identify_text); tetagiti does not fit |
| 10.2-456-ఉ. | 10.2-456-చ. | utpalamala → champakamala | all 4 lines scan as champakamala (meter_engine identify_text, alternative reading needed); utpalamala does not fit |

Same procedure as above (textual edit, originals in `metre_corrected`, txt headers renamed; `child_id` references of seesam parents updated).

## 2026-09-26 — metre labels added to `kuchimanchi_timmakavi.json`

The source text carried no metre labels, so every record had `metre` = null. Labels were filled by
`meter_engine/scripts/label_with_engine.py` (backup of the untouched file:
`dataset/backup/kuchimanchi_timmakavi.json.orig-2026-09-26`). Only the label fields changed
(`metre_code`, `metre`, `metre_roman`, `expected_lines`, `allowed_lines`, `label_source`); ids, text and
every other field are unchanged, and the 11 prose records are untouched.

| `label_source` | poems | meaning |
|---|---|---|
| `engine` | 1,555 | identified by the metre engine (scansion + metrical DAWG) |
| `chandassu` | 53 | not identified, but the poem is in the Kaggle Chandassu dataset, whose label is used |
| `engine-partial` | 3 | not identified; one metre scans at least 3 of 4 lines |
| (null) | 31 | left unlabelled |

Check against an independent source: 236 of the engine-labelled poems are also in the Kaggle Chandassu
dataset, and all 236 engine labels agree with its labels. Metre names, codes and line counts follow
`bhagavatam.json` (seesa poems with their ettugeeti: సీసము, 12 lines, allowed [8, 12]); మధురగతి రగడ,
absent from `bhagavatam.json`, uses the metre catalogue's name and no code.

## 2026-09-26 — machine prathipadartham + bhavam added to vemana, kuchimanchi and chandassu

None of these three files carried a gloss or a bhavam. Every verse record now has a word-by-word
gloss (prathipadartham) and a bhavam written by Gemini, in a new `generated` field. They were produced
by the batch pipeline in `gcloud_agent_platform/prompts/`, with the same prompt as the Padyarchana
runs; the run is called run5, and its README section gives the full command sequence.

The editorial fields `teeka`, `teeka_pairs` and `bhavam` are unchanged and still empty: the machine
annotation lives only in `generated`, shaped like `padyarchana_poems_v2`'s:

```json
"generated": {"run": "run5", "model": "gemini-3.5-flash-lite", "rescued": false,
              "bhavam": "…",
              "prathipadartham": [{"word": "<as it stands in the poem>", "split": "a + b" or null,
                                   "meaning": "…"}]}
```

Prose records get `"generated": null`. Only this field was added: with it removed, each file is
byte-identical to its backup (`dataset/backup/vemana.json.orig-2026-09-26`,
`kuchimanchi_timmakavi.json.labelled-2026-09-26`, `chandassu.json.orig-2026-09-26`).

| file | poems annotated | gloss rows | answered by gemini-3.8-flash (`rescued`) | with `problems` |
|---|---|---|---|---|
| `vemana.json` | 1,164 of 1,164 | 15,381 | 11 | 0 |
| `kuchimanchi_timmakavi.json` | 1,642 of 1,653 (11 prose) | 33,419 | 24 | 4 |
| `chandassu.json` | 2,532 of 2,532 | 57,222 | 24 | 1 |

These annotations are machine output and nobody has reviewed them. Every poem has a bhavam. What
the pipeline's automatic checks found:

- **Spelling of the glossed word.** 86.5% of first-column words match the poem's own spelling,
  measured after the pipeline's sarala-ādeśa repair. A repaired row keeps the model's original
  spelling in `model_word`.
- **Retry on the stronger model.** 62 poems went to `gemini-3.8-flash` because the first answer had
  no bhavam, covered less than half the poem, or rewrote more than half its words.
- **Flagged poems.** 5 poems failed that check with both models. They keep the better of the two
  answers, with the reason in `generated.problems`. In each case the model gives the dictionary form
  where the poem has the sandhi form (ఇడు for నిడు, అతని for యతని).
- **Splits for long compounds.** 197 rows glossed a compound of more than 8 aksharas without
  splitting it. They got their `split` from a follow-up batch, one request per word
  (gemini-3.8-flash), and are marked `split_source: "word_batch"`.

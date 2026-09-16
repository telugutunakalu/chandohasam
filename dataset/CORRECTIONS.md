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

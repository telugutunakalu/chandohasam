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

## 2026-09-28 — English meanings added as `bhavam_en` (all four files)

Every record that has a Telugu bhavam now also has its meaning in English, in a new field
`bhavam_en` on the line after `bhavam`. The meanings were written by Gemini through the batch
pipeline in `gcloud_agent_platform/prompts/` (run6). Each request gave the poem and its Telugu
bhavam and asked for the meaning in English and nothing else: no notes, labels, markdown or
transliteration, following the bhavam faithfully.

| file | records with `bhavam_en` | Telugu bhavam translated |
|---|---|---|
| `bhagavatam.json` | 9,018 of 10,066 | the edition's `bhavam` |
| `vemana.json` | 1,164 of 1,164 | run5's `generated.bhavam` |
| `kuchimanchi_timmakavi.json` | 1,642 of 1,653 | run5's `generated.bhavam` |
| `chandassu.json` | 2,532 of 2,532 | run5's `generated.bhavam` |

Records without a Telugu bhavam have `"bhavam_en": null`. These are the 11 Kuchimanchi prose
records and the 1,048 Bhagavatam seesa parents, whose bhavam sits on the child record (the
ettugeeti or kanda that closes the poem). For those poems the English meaning is on the child too.
It was made from the parent's lines followed by the child's, because the child's bhavam covers the
whole poem.

- **Model.** gemini-3.5-flash-lite wrote every answer except two.
- **Checks.** Every answer finished normally. Two answers contained a word in Indic script
  ("दक्षिणा"); they were regenerated on gemini-3.8-flash.
- **Short meanings are real.** Very short prose connectives get a short English meaning:
  `అంత.` → "Then.", `మఱియును.` → "Furthermore."
- **Commentary is dropped.** Some of the edition's Telugu bhavams continue past the meaning into
  commentary (notes on prāsa and alankāra, a vyākhya). The English keeps only the meaning, as the
  prompt asks.
- **Unreviewed.** This is machine output that nobody has reviewed.

The field was added as one line per record: with those lines removed, each file is byte-identical
to the previous commit.

## 2026-09-28 — letters of other scripts removed from the machine annotation

The `generated` gloss and bhavam of some poems had letters of other scripts inside Telugu words
(`సాధಿಸಿ`, `ఒక్కటாகி`, `విतानములు`), stray characters of unrelated scripts (`ఎ红నని`) and English
glosses. Fixed by `meter_engine/scripts/fix_script_mixing.py`, in this order: the manual table
`dataset/script_fixes.tsv`; for `word`/`split`, the one poem word the token matches; otherwise the
Telugu letter of the same Unicode name, kept only when the resulting word is attested elsewhere in the
corpora. Only the fixed strings changed; every change (field, from, to, rule) is kept in the record's
`generated.script_fixes`. Backups: `dataset/backup/<file>.pre-script-fix-2026-09-28`.

The manual rows were decided one by one, in context, by Claude (AI assistant): words of another
language translated into Telugu, glitch characters read from context, English glosses dropped, leaked
`<bos>`/`<br>` markup removed, headwords set to the poem's own spelling. Nobody has reviewed them yet;
`rule: "manual"` in `script_fixes` marks them.

| file | records fixed | manual | verse | translit |
|---|---|---|---|---|
| `vemana.json` | 151 | 61 | 67 | 40 |
| `kuchimanchi_timmakavi.json` | 180 | 122 | 8 | 80 |
| `chandassu.json` | 333 | 227 | 5 | 158 |

## 2026-09-28 — Latin letters in the Bhāgavatam teeka and bhavam

Typos where a Latin letter sat inside a Telugu word, fixed textually in `bhagavatam.json` and
`bhagavatam.txt` (every other byte unchanged; backups `dataset/backup/bhagavatam.{json,txt}.pre-script-fix-2026-09-28`):

| from | to | occurrences (json / txt) | records |
|---|---|---|---|
| `సోzహ` | `సోఽహ` (`z` typed for the avagraha) | 6 / 3 | 4-359.1-తే. |
| `వినుముa` | `వినుము` | 2 / 1 | 4-672-క. |
| `కాయనd` | `కాయన` | 2 / 1 | 9-309-ఆ. |
| `స్వభాaవము` | `స్వభావము` | 2 / 1 | 9-730-క. |
| `3.6X6`, `14x30`, `60x8` | `3.6×6`, `14×30`, `60×8` (multiplication sign) | 7 / 4 | 10.1-230.1-తే., 7-405-వ., 10.2-1220-వ. |

Left as they are, being deliberate: `X` for "versus" (`{జడము X చైతన్యము}`), the English gloss `space`
(2-16-వ.), and source reference codes (`-I465`, `.H2560`, `X.i_537`).

## 2026-09-28 — verse, layout and labels fixed after the data-sanity run

Problems found by `data_sanity_metrics/` and fixed by `meter_engine/scripts/fix_verse.py`. Backups:
`dataset/backup/<file>.pre-verse-fix-2026-09-28`. Running the script again changes nothing.

How the changes are recorded:
- **Verse.** A record whose verse changed keeps its original lines and the reasons in a new `verse_corrected`
  object (`from_verse`, `date`, `reasons`, `corrected_by`). `line_count` follows the new lines.
- **Labels.** A relabelled record keeps its old label in `metre_corrected` (`from_metre_code`, `from_metre`,
  `from_metre_roman`, `from_label_source`, `date`, `reason`, `corrected_by`), as for the Bhāgavatam relabels above.

Besides those fields, only these changed: `complete`, `expected_lines`/`allowed_lines`, `label_source`, and, for the
backslash, `generated.prathipadartham`.

| fix | file | records |
|---|---|---|
| a backslash inside a word removed: `నల్పునకు\న్‌` → `నల్పునకున్‌`. It stands before న్ all 409 times, a conversion artifact of the Kaggle source; also removed from 42 gloss fields | `chandassu.json`, `vemana.json` | 236, 1 |
| seesa separator written `X‌- Y` (a ZWNJ before the dash, which the importer's `seesa_line()` misses) set to ` - ` | `chandassu.json` | 4 |
| ettugeeti lines holding two pādas joined by ` - ` split into one pāda per line (the importer's `split_padas()` does not split at ` - `) | `chandassu.json` (Narasimha) | 99 |
| seesa records re-segmented by scansion (below): pāda breaks lost in the source (Madanagopala 66, Taadimallaraajagopaala 37), or a pāda printed without its separator (Aandhranaayaka 3, Narasimha 1) | `chandassu.json` | 107 |
| a variant reading printed inside the verse, in parentheses, removed (sumathi-53, a కందము printed on five lines) | `chandassu.json` | 1 |
| relabelled from the heuristic ఆటవెలది to the metre the engine identifies: కందము 132, తేటగీతి 5, ఉత్పలమాల 3, చంపకమాల 2 | `vemana.json` | 142 |
| typos (table below) | all four | 6 |
| `allowed_lines` [8] → [4, 8]: this లయగ్రాహి is printed as four whole pādas, which the engine reads as well as the eight half-lines of `bhagavatam.json` | `kuchimanchi_timmakavi.json` (kuchimanchi-1220) | 1 |

**Relabels keep their ids.** For example, `vemana-22-ఆ.` is now a కందము. `human_evals/` and `meter_engine/reports/`
cite Vemana ids, so renaming them would break those references. `label_source` is now `engine` for these 142.

**Re-segmentation by scansion.**
- **Search.** For each record, every segmentation into four seesa pādas and four geeti pādas that keeps the printed
  line breaks and separators was tried.
- **Half-lines.** A seesa pāda's halves break after its fourth gaṇa, as the gaṇa parse places it.
- **Acceptance.** A record was changed only when exactly one segmentation scans. That held for all 107 records
  changed, and their yati also holds in 77.
- **Printing.** A word running across the halves is printed `X- - Y`, as elsewhere in the file, for example
  `సాష్టాంగ- - దండము`. Pāda breaks lost in the source had glued the words together (`…శరణుసురయక్ష…` →
  `…శరణు` / `సురయక్ష…`).
- **Flags.** Re-segmented records get `complete: true`.

| typo | from | to | evidence |
|---|---|---|---|
| vemana-86-ఆ. | `మొసఁగుకన్నแ` | `మొసఁగుకన్నఁ` | Thai แ typed for ఁ; line 1 has the same word |
| vemana-1162-ఆ. | `మఱiలింగ` | `మఱిలింగ` | Latin i typed for the vowel sign ి |
| kuchimanchi-11 | `త్క్రరు` | `త్క్రతు` | prāsa: the other three pādas have త; స\|త్క్రతు is సత్క్రతు |
| kuchimanchi-56 | `మినునొక్కప్పుడుఁ` | `మిమునొక్కప్పుడుఁ` | prāsa: the other three pādas have మ; మిము నొక్కప్పుడుఁ గొల్వనేరక, not worshipping you even once |
| chandassu-naarayana-94-మ. | `నవలం బారిన` | `ననలం బారిన` | prāsa: the other three pādas have న; ననలం బారిన భూతి, ash where the fire (అనలము) went out |
| bhagavatam 6-523-క. | `వా డేర్వు` | `వా డేడ్వు` | the edition's own teeka reads ఏడ్వురు (seven). Fixed textually in `bhagavatam.json` and `bhagavatam.txt` |

The prāsa of 6-523 still does not hold, since its line 1 has డే where the others have ర. `వా రేడ్వు` (వారు ఏడ్వురు) would
hold, but only the printed edition can settle it.

The other 29 poems that scan but fail prāsa under the relaxed profile were left unchanged:
- **Pairs the relaxed profile rejects** (25):
  - ద~ధ: 7;
  - spellings త్ర~త్త్ర, త్వ~త్త్వ, న్య~న్న్య, ద్జ్ఞ~జ్ఞ: 5;
  - a geminate against a cluster (ప్ప~ర్ప, ల్ల~ర్ల): 3;
  - ర~ల: 2;
  - ద~థ, ట~ఠ, డ~ఢ, ప~బ: 4;
  - a pūrṇabindu before the prāsa in some pādas only: 2;
  - an extra య in a cluster (ర~ర్య): 1;
  - pre-prāsa aksharas mixing guru and laghu: 1.
- **Possible typos with no certain correction** (4): kuchimanchi-255 `వెకవరి`, chandassu-bhaktamandaara-99 `జయమొప్పార`,
  chandassu-vrushadhipa-55 `అస్తగణ` and chandassu-vrushadhipa-87 `దీవ్రము`.

**Left as printed.** These are not conversion errors, or the repo cannot decide them:
- **Gaps in the source** (`... ...`): 9 seesa records, Madanagopala 8 and Taadimallaraajagopaala 1.
- **Lost pāda breaks that cannot be recovered:** 53 seesa records, Madanagopala 26 and Taadimallaraajagopaala 27. No
  segmentation of them scans, so their text has other errors as well.
- **Five-line ettugeeti:** 31 Venugopaala seesa records. The ettugeeti's own lines are followed by the two-line makuta
  (మదరిపువిఫాల… / వేణుగోపాల…).
- **Five seesa pādas:** 3 Laavanya seesa records.
- **Five pādas (పంచపాది):** 21 vruttams, Dāśarathi 7, Maaruthi 13 and Venkateswara 1. Each line has the metre's full
  length and the five lines share the prāsa, as in భండనభీముఁ డార్తజనబాంధవుఁ… (daasarathi-34). `meter_engine` does not
  accept five pādas, so these fail level 1 of the data-sanity metrics.

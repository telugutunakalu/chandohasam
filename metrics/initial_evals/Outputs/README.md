# Outputs — combined dataset

`chandas_dataset.json` (2.1 MB) merges the three raw `.txt` dumps in this folder into
one structured file. `combine_outputs.py` regenerates it from those dumps
(`python3 combine_outputs.py`); it is deterministic and safe to re-run.

The raw `.txt` files are untouched.

## What the three source files are

| File | Role |
|---|---|
| `Prompt templates for various chandas (1).txt` | **Prompt inputs.** 10 chandas × 4 topics × 3 input tiers (word / single line / full bhavam). Prose, not JSON. |
| `Prompt templates for various chandas (2).txt` | **31 generated poems**, one uniform schema. |
| `Prompt templates for various chandas.txt` | **224 generated poems** in two batches, 7 schema variants, JSON both fenced and bare. |

So file (1) is the input side and the other two are the output side — that relationship
is represented in the combined JSON rather than left implicit.

## Top-level structure

```
dataset, description, combined_on
provenance[]      one entry per source file: sha256 prefix, bytes, lines, role
summary{}         counts and data-quality tallies (see below)
prompt_inputs{}   the 10 × 4 × 3 input spec, parsed into nested objects
batch_design{}    declared design of the 108-poem batch, parsed from its preamble
poems[]           255 normalised records
```

## Poem record

Aliases across the source schemas are unified: `poem_lines` / `poem` (list) /
`poem.lines` → `lines`; `telugu_meaning` / `meaning_telugu` → `meaning_telugu`;
`chandassu_name` / `chandassu` / `poem.meter` / `poem.vruttam` → `chandassu_raw`.

| Field | Notes |
|---|---|
| `id` | `poem_0001` … stable across reruns |
| `source` | `{file, line}` — where the record came from, so anything can be traced back |
| `batch`, `contributor`, `section_header` | provenance within the dump |
| `poem_number`, `title`, `topic` | as given |
| `chandassu_id`, `chandassu` | **canonical** slug + Telugu name |
| `chandassu_raw`, `chandassu_source` | as written, and how it was determined |
| `alankaram_id`, `alankaram`, `alankaram_raw` | same treatment for the figure of speech |
| `lines`, `line_count` | whitespace-normalised, NFC |
| `meaning_telugu`, `meaning_english` | string, or `null` |
| `meaning_*_variants` | dict of readings when the poem has more than one (śleṣa) |
| `chandassu_analysis` | `{shape, raw}` |
| `alankara_analysis` | `{keys, raw}` or `null` |
| `duplicate_exact`, `duplicate_shared_first_line` | ids of related records |
| `extra_fields` | any source key not otherwise mapped; `null` normally |

### Why the analyses are kept raw

`chandassu_analysis` comes in 5 genuinely different shapes and `alankara_analysis` in
17, because each figure of speech carries its own evidence key (`yamaka_pairs`,
`upama_components`, `shlesha_meanings`, `metaphorical_identities`, …). Forcing them
into one schema would mean discarding the figure-specific evidence, which is the
part worth having. So each is preserved verbatim under `.raw`, with a `shape` /
`keys` tag next to it so you can filter before parsing.

`shape` values: `per_line_keys` (139), `line_breakdowns` (51), `lines_analysis` (26),
`breakdown_meter_rule` (26), `breakdown_meter_scheme` (13).

## Contents

- **255 poems**, 246 distinct texts.
- **By batch:** 108 (alankara batch, Radhe) · 31 (uniform file) · 116 across 9
  chandas sections (Samvaran, 12–13 each).
- **By contributor:** Samvaran 116, Radhe 108, unattributed 31.
- **The 108 batch** is a full 4 chandas × 9 alankaras × 3 topics grid — verified
  complete, 12 poems per alankara, 36 per topic.
- **Meanings:** every poem has both Telugu and English; 3 śleṣa poems carry two
  readings each.
- **Line counts:** 242 four-line, 13 eight-line (the Seesam set).

## Two inferences, both flagged

Every poem ends up with a meter, but 58 did not state one. `chandassu_source`
records how each was resolved — `record` (171), `section_header` (26),
`gana_signature` (31), `batch_position` (27). The two inferred cases:

**`gana_signature` — the 31 poems of file (2).** A gana sequence is the meter's
signature, so it identifies the meter directly. Three sequences appear, matching
Utpalamala (13 poems), Champakamala (12) and Shardulavikriditam (6).

**`batch_position` — poems 1–27 of the 108 batch.** That batch is numbered 1–108 and
emitted in the order its preamble declares. Poems 28–108 state their meter and fall
into exact 27-blocks in declaration order 2, 3, 4; the unlabelled 1–27 is therefore
declaration order 1, Utpalamala. The script asserts this block structure before
applying it and warns rather than guessing if it ever fails to hold.

Anything relying on meter labels should check `chandassu_source` first.

## Duplicates — kept, not merged

13 groups, at two strengths, because both kinds are present and they mean different
things:

- **`duplicate_exact`** (18 poems, 8 groups) — byte-identical texts, the same verse
  emitted twice under different alankara labels.
- **`duplicate_shared_first_line`** (12 poems, 5 groups) — same opening line,
  divergent afterwards: genuine regenerated variants.

Nothing was dropped. Collapsing these would erase real variation in the 108 batch,
but the exact-duplicate set is worth knowing about before computing per-alankara
statistics.

## Caveats

- **`chandassu_raw` spelling varies** in the sources (`శార్దూలవిక్రీడితం` vs
  `శార్దూలవిక్రీడితము`, some with an English gloss appended). Use `chandassu_id`
  for grouping; `chandassu_raw` is retained only for audit.
- **The 31-poem file has no contributor** stated anywhere in it, so
  `contributor` is `null` for those. Not inferred.
- **`batch` slugs for the 9 chandas sections come from their section headers**, whose
  spellings are the authors' (`Mattenham`, `Atavelladi`, `Tetageethi`). The slugs are
  normalised but the headers are preserved in `section_header`.
- **Section header counts don't always match reality**: the header says
  `10 OUTPUTS` but the sections hold 12–13 poems each. The counts here are actual,
  not declared.
- **No metrical validation was performed.** The gana/yati/prasa analyses are
  reproduced as the generating model wrote them; they are claims, not verified facts.
  Checking them against a real validator is a separate job.

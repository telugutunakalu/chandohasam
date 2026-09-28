# Data sanity metrics — `dataset/*.json`

Run on 2026-09-28 over the four dataset files:
- `bhagavatam.json`
- `vemana.json`
- `kuchimanchi_timmakavi.json`
- `chandassu.json`

The files are measured after the fixes recorded in `dataset/CORRECTIONS.md` ("verse, layout and labels fixed after the
data-sanity run"). The first run of these metrics found those problems; [Fixes applied](#fixes-applied) says what
changed.

**Scope and method.**
- Levels 1–4 of the IndicNeuroSym §5 corpus-validation pipeline, plus a level-0 inventory. Level 5 (LLM-as-a-judge)
  is not implemented.
- Scansion by `meter_engine`.
- Every number is **per dataset file**.
- How to rerun: [README.md](README.md). Raw numbers: `outputs/*.json`.

## Summary

| file | L1 prosodic integrity (relaxed / strict) | L2 length ratio | L3 LaBSE Te–En | L4 poem TTR / subword TTR | pass L1–L3 |
|---|---|---|---|---|---|
| `bhagavatam` | 91.2% / 88.7% | 96.2% | 90.2% | 0.992 / 0.705 | **80.4%** |
| `vemana` | 83.5% / 82.6% | 84.5% | 98.4% | 0.977 / 0.733 | **69.8%** |
| `kuchimanchi_timmakavi` | 90.6% / 88.7% | 98.1% | 97.7% | 0.993 / 0.659 | **86.7%** |
| `chandassu` | 74.0% / 69.9% | 97.6% | 96.4% | 0.976 / 0.689 | **69.4%** |

Before the fixes:

| file | level 1 (relaxed) | pass L1–L3 |
|---|---|---|
| `vemana` | 72.4% | 60.8% |
| `chandassu` | 63.8% | 59.5% |

Denominators:
- L1 is over the labelled verse poems.
- L2 and L3 are over verse poems with a bhavam.
- "Pass L1–L3" is over labelled poems that have a bhavam.

**"Pass L1–L3" adds little.** It is close to the product of the three rates: for Kuchimanchi, 90.6% × 98.1% × 97.7% ≈
86.8%. So failures at different levels are nearly independent. Kuchimanchi ranks first only because its labels were
made by the engine that level 1 uses (finding 4).

## Main findings

1. **Bhāgavatam is the reference.**
   - 99.9% of its 7,366 poems scan as the edition's label.
   - Of the 636 poems that scan but fail, 627 fail on yati.
   - The text is canonical, so these are more likely gaps in the engine's yati rules than faulty verse. For example,
     1-10 అమ్మలఁ గన్నయమ్మ has its yati seat on an akshara made by sandhi: ముగు**ర**మ్మ, from ముగురు + అమ్మ.
2. **Chandassu is now 74.0% valid (relaxed). Most of what remains is in the source text.**
   - **Correction.** The first run blamed its failures mostly on line segmentation. That was wrong: the records that
     scanned 0% for layout reasons were about a quarter of its failures.
   - **What the fixes did.** Valid rose from 63.8% to 74.0%, and poems that scan as their label rose from 72.4% to
     85.0%.
     - A backslash inside words (`నల్పునకు\న్‌`) was a conversion artifact in 236 poems. 220 of them now scan.
     - 107 seesa records whose pāda breaks were lost in the source were re-segmented by scansion. All scan, and 77 are
       valid.
     - 103 records printed separators or ettugeeti pādas off-convention; they were normalised.
   - **The 658 poems still not valid:**

     | kind | poems | note |
     |---|---|---|
     | fit no metre, with the right number of lines | 250 | the raw Kaggle CSV has the same text; typically one akshara differs, e.g. `నిట్టీ` for `నిట్టి` (aandhranaayaka-17) |
     | scan, but fail yati or prāsa | 279 | |
     | left as printed: line count not the metre's | 117 | 21 five-pāda vruttams (పంచపాది); 34 seesa poems with a five-line ettugeeti or five seesa pādas; 53 seesa records whose lost pāda breaks no segmentation recovers; 9 with gaps in the source (`... ...`) |
     | fit another metre | 12 | |

   - The five-pāda poems are genuine: every line has the metre's full length, and the five lines share the prāsa, as in
     భండనభీముఁ డార్తజనబాంధవుఁ… (daasarathi-34). `meter_engine` does not accept five pādas. The first run misread these
     as segmentation errors.
3. **Vemana: 142 labels corrected.**
   - A heuristic had labelled every Vemana poem ఆటవెలది. 142 scan as another metre: 132 కందము, 5 తేటగీతి, 3 ఉత్పలమాల
     and 2 చంపకమాల.
   - The కందము poems have the kanda shape and end in "…వేమా", not in the ఆటవెలది makuta "విశ్వదాభిరామ వినర వేమ".
   - They now carry the engine's label, with `label_source: engine`. Valid rose from 72.4% to 83.5%.
   - 149 poems still fit no metre. 79 of them contain the ఆటవెలది makuta, so they are ఆటవెలది with text errors, not
     mislabelled poems.
4. **Engine-made labels agree by construction.**
   - 1,555 of Kuchimanchi's labels were made by `meter_engine` and agree 100%. So do the 142 relabelled Vemana poems.
   - Kuchimanchi's 53 labels taken from the Kaggle corpus and its 3 "partial" labels are exactly the poems the engine
     could not identify: 0% scan.
5. **The prosodic rules are hard to satisfy by chance, so the rates mean something.**

   | rule | chance | real |
   |---|---|---|
   | yati, per seat | 14–18% | 73–93% |
   | prāsa, per stanza | 0.0–3.7% | 93–100% |

   A single yati seat passes by chance about one time in six, so per-seat yati rates should be read against that
   floor. The whole yati of a poem, over four or more seats, almost never passes by chance.
6. **Prāsa failures are mostly the poets' prāsa, not typos.** 33 poems scan but fail prāsa under the relaxed profile.
   - 4 were typos and are now fixed, e.g. kuchimanchi-11 `త్క్రరు` → `త్క్రతు`. In Bhāgavatam 6-523 the fix comes from
     the edition's own teeka and still leaves the prāsa unmatched.
   - 25 use prāsa the relaxed profile does not accept:

     | prāsa | poems |
     |---|---|
     | ద~ధ | 7 |
     | spellings such as త్ర~త్త్ర | 5 |
     | ప్ప~ర్ప and ల్ల~ర్ల | 3 |
     | ర~ల | 2 |
     | other rejected pairs and bindu or pre-prāsa rules | 8 |

   - 4 look like typos, but the correction is not certain.
7. **The level-3 gate (Te–En ≥ 0.65) measures translation consistency, not fidelity to the poem.**
   - `bhavam_en` was translated from the Telugu bhavam. It passes 90–98%; shuffled pairs pass ≤ 0.1%, with AUC 1.000.
   - The pair that bears on fidelity is the poem with its Telugu bhavam. It scores far lower: LaBSE mean cosine
     0.34–0.47, and 0.7–5.3% above 0.65.
   - It still separates right from wrong pairings: AUC 0.85–0.94.
8. **A fixed 0.65 threshold is meaningless for Telugu–Telugu pairs under some encoders.** An English-only encoder that
   cannot read Telugu "passes" 94–99% of poem–bhavam pairs, and 85–97% of *shuffled* pairs.
9. **Machine bhavams for Vemana run long.**
   - 15.5% exceed 2.5× the verse length, against 1.9–2.7% in the other files.
   - Where lengths are uniform, the length gate cannot tell a right bhavam from a wrong one: for Chandassu, 97.4% of
     neighbour pairings pass.
10. **No poem appears in two files**, even at 3-gram Jaccard ≥ 0.7. Within files there are only 13 near-duplicate
    pairs.
    - Refrain lines (makuta) repeat heavily: 77% of Vemana poems and 25% of Chandassu poems share a pāda with another
      poem.
    - That is also why Vemana's Yule's K is 99.9, against 1.4–4.1 for the others.

## Level 0 — inventory and structure (`level0_inventory.py`)

| | bhagavatam | vemana | kuchimanchi_timmakavi | chandassu |
|---|---|---|---|---|
| records (verse / prose) | 10,066 (7,366 / 2,700) | 1,164 (1,164 / 0) | 1,653 (1,642 / 11) | 2,532 (2,532 / 0) |
| duplicate ids, empty verse, `line_count` mismatch | 0 | 0 | 0 | 0 |
| line count outside the metre's `allowed_lines` | 0 | 0 | 0 | **117** |
| seesa pādas on one line (` - ` between halves) | 0 | 3 | 0 | 518 |
| seesa parent / child links, broken | 1,051 / 1,055, 0 broken | — | — | — |
| unlabelled verse poems | 0 | 0 | 31 | 0 |
| label source | edition | heuristic 1,022 · engine 142 | engine 1,555 · Kaggle 53 · partial 3 | Kaggle corpus |
| verse with a Telugu bhavam | 6,318 (edition) | 1,164 (machine) | 1,642 (machine) | 2,532 (machine) |
| with `bhavam_en` / with a gloss | 6,318 / 6,318 | 1,164 / 1,164 | 1,642 / 1,642 | 2,532 / 2,532 |
| gloss rows (per glossed poem) | 174,407 (27.6) | 15,381 (13.2) | 33,419 (20.4) | 57,222 (22.6) |
| machine: rescued / with problems / script-fixed | — | 11 / 0 / 151 | 24 / 4 / 180 | 24 / 1 / 333 |
| letters of another script, Telugu fields | 2 | 0 | 0 | 0 |
| Indic letters in `bhavam_en` | 0 | 0 | 0 | 0 |

Notes on the table:
- **Bhāgavatam's 1,048 verse poems without a bhavam** are the seesa parents; their bhavam is on the child record.
- **The 2 Bhāgavatam script hits** are source reference codes (`-I465`, `.H2560`) in prose records.
- **Chandassu's 117 records outside `allowed_lines`** are the layouts left as printed (finding 2).
- **Seesa layout in Chandassu.** It prints each seesa pāda on one line (` - ` between halves) in 518 records, up from
  418, now that the re-segmented records follow that layout.
- **Kuchimanchi-1220** (లయగ్రాహి) is printed as four whole pādas, which the engine reads as well as eight half-lines. It
  now allows 4 or 8 lines.

## Level 1 — prosodic integrity (`level1_prosodic_integrity.py`)

The share of labelled verse poems that satisfy their metre on every rule:
- **Gaṇa:** the labelled metre is among those the lines fit.
- **Prāsa:** checked where the metre requires it.
- **Profiles:** `meter_engine`'s strict and relaxed, with yati sandhi mode `hypothesis`.

| file | poems | identified | scans as label | prāsa (rel) | yati (rel) | **valid (rel)** | valid (strict) |
|---|---|---|---|---|---|---|---|
| `bhagavatam` | 7,366 | 99.9% | 99.9% | 99.8% | 91.4% | **91.2%** | 88.7% |
| `vemana` | 1,164 | 87.2% | 87.2% | 95.6% | 96.4% | **83.5%** | 82.6% |
| `kuchimanchi_timmakavi` | 1,611 | 96.5% | 96.5% | 99.9% | 93.9% | **90.6%** | 88.7% |
| `chandassu` | 2,532 | 85.5% | 85.0% | 98.8% | 87.9% | **74.0%** | 69.9% |

**Per metre**, valid under the relaxed profile:
- **`bhagavatam`:**
  - కందము 94.7% (2,608 poems)
  - మత్తేభ 95.2%
  - ఆటవెలది 91.8%
  - చంపకమాల 90.0%
  - తేటగీతి 89.6%
  - శార్దూల 88.9%
  - ఉత్పలమాల 86.6%
  - సీసము 85.1%
- **`vemana`:**
  - ఆటవెలది 82.8% (1,018 poems)
  - కందము 91.7% (132)
  - Of the 10 other relabelled poems, 8 are valid.
- **`kuchimanchi_timmakavi`:**
  - తేటగీతి 96.2%
  - కందము 95.9%
  - మత్తేభ 61.0%
  - శార్దూల 58.8%
  - The two low vruttams are its Kaggle-labelled poems: 0 of 38 scan, against 78 of 78 engine-labelled ones.
- **`chandassu`:**
  - కందము 88.2%
  - చంపకమాల 81.4%
  - మత్తేభ 76.4%
  - శార్దూల 74.8%
  - ఉత్పలమాల 72.4%
  - సీసము 55.4%; 71.2% scan

**Agreement by label source.**

| label source | poems | scans as label |
|---|---|---|
| edition (bhagavatam) | 7,366 | 99.9% |
| heuristic (vemana) | 1,022 | 85.4% |
| engine (vemana, relabelled) | 142 | 100%, by construction |
| Kaggle corpus (chandassu) | 2,532 | 85.0% |
| engine (kuchimanchi) | 1,555 | 100%, by construction |
| Kaggle via kuchimanchi | 53 | 0% |
| engine-partial (kuchimanchi) | 3 | 0% |

The 31 unlabelled Kuchimanchi poems stay unidentified. That is why they are unlabelled.

**How yati passes (relaxed).**

| file | yati seats | matched | of matched: needs a sandhi hypothesis | of matched: prāsa-yati fallback |
|---|---|---|---|---|
| `bhagavatam` | 28,450 | 97.6% | 11.1% | 4.7% |
| `vemana` | 3,804 | 99.0% | 4.5% | 4.6% |
| `kuchimanchi_timmakavi` | 7,020 | 98.6% | 9.5% | **19.3%** |
| `chandassu` | 10,892 | 97.3% | 8.6% | 6.9% |

**Chance pass rates** (`level1_chance_pass_rates.py`).
- The material comes from unrelated poems of the same metre; every seat and every stanza is checked.
- The real yati rates here are re-checked out of context, so they are lower than level 1's in-context rates.
- Kuchimanchi's larger gap is mostly its prāsa-yati share (19.3%), which an out-of-context check cannot use.

| file | yati real / **chance** (strict) | yati real / **chance** (relaxed) | prāsa stanzas | prāsa real / **chance** (strict) | prāsa real / **chance** (relaxed) |
|---|---|---|---|---|---|
| `bhagavatam` | 88.2% / **17.0%** | 88.5% / **17.3%** | 4,519 | 96.7% / **0.3%** | 99.8% / **0.2%** |
| `vemana` | 92.3% / **17.7%** | 92.5% / **16.6%** | 132 | 93.2% / **0.0%** | 95.5% / **0.0%** |
| `kuchimanchi_timmakavi` | 73.2% / **14.0%** | 73.5% / **14.1%** | 775 | 97.7% / **3.7%** | 99.9% / **3.7%** |
| `chandassu` | 87.1% / **15.5%** | 87.4% / **16.4%** | 1,742 | 93.7% / **0.2%** | 98.8% / **0.1%** |

## Level 2 — length ratio (`level2_length_ratio.py`)

- **Definition.** r = |bhavam| / |verse| in non-space characters; a poem passes when 0.8 ≤ r ≤ 2.5.
- **The verse measured** is the lines the bhavam explains, so a Bhāgavatam seesa child counts its parent's lines too.

| file | poems | mean r | median r | **pass** | too short | too long | shuffled pass | neighbour pass |
|---|---|---|---|---|---|---|---|---|
| `bhagavatam` | 6,318 | 1.43 | 1.33 | **96.2%** | 1.2% | 2.7% | 62.3% | 64.1% |
| `vemana` | 1,164 | 2.08 | 2.03 | **84.5%** | 0.0% | 15.5% | 82.6% | 82.6% |
| `kuchimanchi_timmakavi` | 1,642 | 1.69 | 1.64 | **98.1%** | 0.0% | 1.9% | 66.6% | 78.5% |
| `chandassu` | 2,532 | 1.69 | 1.63 | **97.6%** | 0.04% | 2.4% | 67.3% | **97.4%** |

- **Only the edition bhavams (Bhāgavatam) include extreme lengths.** 31 have r > 5 and 73 have r < 0.8. Some edition
  bhavams continue into commentary.
- **Vemana's machine bhavams are verbose.** Its short ఆటవెలది verses get bhavams twice their length on average.
- **The gate barely discriminates.** Wrong pairings pass 62–83% of the time, and for Chandassu a neighbour's bhavam
  passes as often as the poem's own.
- **The unit changes the rate by 0.5–5 points:**

  | file | characters | words | aksharas |
  |---|---|---|---|
  | `bhagavatam` | 96.2% | 92.7% | 95.5% |
  | `vemana` | 84.5% | 80.7% | 87.5% |
  | `kuchimanchi_timmakavi` | 98.1% | 97.6% | 98.2% |
  | `chandassu` | 97.6% | 93.6% | 98.1% |

## Level 3 — semantic fidelity (`level3_semantic_fidelity.py`)

Cosine similarity of sentence embeddings; a pair passes at ≥ 0.65. **The gate is LaBSE, Telugu–English.**

| file | pair | mean cos | pass | shuffled pass | AUC vs shuffled | AUC vs neighbour | recall@1 (pool) | pass at a 1%-false-accept threshold |
|---|---|---|---|---|---|---|---|---|
| `bhagavatam` | **Te–En** | 0.747 | **90.2%** | 0.0% | 1.000 | 0.998 | 0.99 (2,000) | 99.8% (thr 0.47) |
| | poem–Te | 0.440 | 4.8% | 0.0% | 0.925 | 0.867 | 0.30 | 46.5% (thr 0.46) |
| `vemana` | **Te–En** | 0.798 | **98.4%** | 0.09% | 1.000 | 1.000 | 1.00 (1,164) | 100% (thr 0.53) |
| | poem–Te | 0.430 | 3.7% | 0.0% | 0.937 | 0.913 | 0.38 | 58.8% (thr 0.41) |
| `kuchimanchi_timmakavi` | **Te–En** | 0.790 | **97.7%** | 0.0% | 1.000 | 0.999 | 0.99 (1,642) | 100% (thr 0.52) |
| | poem–Te | 0.338 | 0.7% | 0.0% | 0.853 | 0.772 | 0.15 | 26.7% (thr 0.43) |
| `chandassu` | **Te–En** | 0.771 | **96.4%** | 0.04% | 1.000 | 0.997 | 0.99 (2,000) | 99.8% (thr 0.55) |
| | poem–Te | 0.474 | 5.3% | 0.0% | 0.930 | 0.846 | 0.32 | 46.8% (thr 0.49) |

**Te–En is near perfect because `bhavam_en` was translated from the bhavam.** Bhāgavatam's 90% is the lowest: its
English drops the edition's commentary (as `dataset/CORRECTIONS.md` records), and LaBSE truncates long texts.

**Poem–Te** is the pair that bears on whether a bhavam fits its poem:
- **Its absolute cosine is low** (archaic verse against modern prose), so 0.65 is the wrong threshold.
- **It still separates right from wrong pairings** (AUC 0.85–0.94).
- **Kuchimanchi is hardest**, with neighbour AUC 0.77 and recall@1 0.15. Plausibly this is because much of it is
  అచ్చతెలుఁగు (pure-Telugu) verse, whose vocabulary is far from the prose's; this was not tested.

**Other encoders, poem–Te pass versus shuffled pass:**

| encoder | bhagavatam | vemana | kuchimanchi_timmakavi | chandassu | AUC vs shuffled |
|---|---|---|---|---|---|
| IndicSBERT | 63.6% vs 7.9% | 66.1% vs 6.4% | 36.8% vs 5.7% | 84.9% vs 23.9% | 0.77–0.90 |
| mSBERT | 69.7% vs 51.3% | 57.7% vs 45.6% | 58.0% vs 45.7% | 79.2% vs 69.4% | 0.59–0.65 |
| English-only MiniLM | 98.5% vs 86.5% | 93.6% vs 93.6% | 94.1% vs 84.5% | 98.5% vs 96.6% | 0.51–0.77 |

**MiniLM cannot read Telugu, yet it clears 0.65 on almost every Telugu pair**, right or wrong. For Telugu–Telugu
pairs, a fixed threshold is not a quality gate.

## Level 4 — lexical diversity, subword coverage, duplicates

**Lexical diversity of the verse** (`level4_lexical_diversity.py`):

| | bhagavatam | vemana | kuchimanchi_timmakavi | chandassu |
|---|---|---|---|---|
| tokens / types | 123,517 / 77,417 | 16,097 / 9,581 | 36,901 / 21,905 | 61,662 / 39,178 |
| TTR | 0.627 | 0.595 | 0.594 | 0.635 |
| MATTR (w=50) | 0.986 | **0.857** | 0.974 | 0.937 |
| Yule's K | 1.43 | **99.9** | 2.07 | 4.06 |
| Honoré's H | 7,934 | 6,563 | 5,141 | 8,275 |
| hapax ratio / Sichel's S | 0.852 / 0.074 | 0.852 / 0.081 | 0.795 / 0.101 | 0.867 / 0.072 |
| per poem: words / TTR / Yule's K | 16.8 / 0.992 / 11.1 | 13.8 / 0.977 / 37.3 | 22.5 / 0.993 / 8.4 | 24.4 / 0.976 / 28.8 |
| poems where Honoré's H is undefined (every word a hapax) | 89.6% | 77.8% | 89.2% | 70.6% |

- **At the same token count, the verse is always more diverse than its prose.** Telugu bhavam TTR is 0.36–0.45
  against the verse's 0.59–0.64, and the English bhavam's is 0.07–0.16. A "literary range" for these measures only
  holds at equal N within one language.
- **Per-poem measures are near-degenerate.** Most poems repeat no word at all, so the per-poem TTR (≈ 0.98–0.99) and
  Honoré's H carry little information.

**Subword coverage** (`level4_subword_coverage.py`).
- The Gemma 4 tokenizer was used.
- Gemma 3's is the same text tokenizer, with identical Telugu tokens and ids for every text here.

| | bhagavatam | vemana | kuchimanchi_timmakavi | chandassu |
|---|---|---|---|---|
| Telugu tokens used, of 1,784 | 1,246 (69.8%) | 1,011 (56.7%) | 1,085 (60.8%) | 1,246 (69.8%) |
| verse: tokens per word / per akshara | 5.23 / 1.33 | 4.54 / 1.23 | 4.51 / 1.36 | 4.71 / 1.26 |
| verse: token boundaries inside an akshara | 21.8% | 15.5% | 20.1% | 21.1% |
| bhavam: tokens per word / split rate | 3.43 / 19.6% | 3.26 / 14.4% | 3.59 / 15.6% | 3.53 / 15.6% |

- **One token boundary in five falls inside an akshara.** No single token then carries that akshara, so the model
  must compose it across tokens. Its guru/laghu weight also depends on the next akshara: a conjunct after it makes it
  guru. So metrical units and tokens do not line up.
- **Verse costs about 40% more tokens per word than prose.**

**Duplicates** (`level4_duplicates.py`), over all 12,704 verse poems:
- **No cross-file duplicates, and no exact duplicates at all.**
- **Normalised duplicates:** 2 pairs (Vemana 1, Kuchimanchi 1).
- **Near-duplicates** (3-gram Jaccard): 6 pairs at ≥ 0.9, 8 at ≥ 0.8 and 13 at ≥ 0.7 (Vemana 7, Bhāgavatam 4,
  Kuchimanchi 1, Chandassu 1).
- **Pāda reuse:** 139 distinct pādas occur in more than one poem, 4 of them across files. The share of poems containing
  one is Bhāgavatam 1.1%, Vemana 77.1%, Kuchimanchi 11.8% and Chandassu 25.3%, dominated by refrain lines (makuta).
- **Bhavam reuse:** one Telugu bhavam is shared by two poems (Bhāgavatam 8-194 and 8-197, in the edition); no English
  bhavam is shared.

## Fixes applied

The first run of these metrics found the problems below. They were fixed on 2026-09-28 by
`meter_engine/scripts/fix_verse.py`; the details are in `dataset/CORRECTIONS.md`. Every changed record keeps its
original verse, or its original label, in `verse_corrected` or `metre_corrected`.

| fix | records | level-1 effect |
|---|---|---|
| backslash inside words removed (Chandassu 236, Vemana 1) | 237 | 220 of the Chandassu poems now scan as their label |
| Chandassu seesa records re-segmented by scansion, applied only where exactly one segmentation scans | 107 | all scan; 77 valid |
| Chandassu separators (`X‌- Y`) and ettugeeti lines printed off-convention | 103 | 91 scan; 84 valid |
| Vemana relabelled from ఆటవెలది to the metre the engine identifies | 142 | 129 valid |
| typos: letters of other scripts in the Vemana verse; prāsa typos; Bhāgavatam 6-523 from the edition's teeka | 6 | |
| a variant reading printed inside the verse (sumathi-53) | 1 | |
| kuchimanchi-1220 `allowed_lines` [8] → [4, 8] | 1 | |

The scansion now also splits a seesa pāda printed `X- Y` or `X -Y`. A dash that ends a line is not a separator.

## What remains

1. **Chandassu, 250 poems that fit no metre.** Their text differs from the metre, typically by one akshara, and the raw
   Kaggle CSV has the same text. The engine points to the failing akshara, but correcting them needs the printed
   sources.
2. **Chandassu, 117 layouts left as printed:**
   - gaps in the source;
   - lost pāda breaks that no segmentation recovers;
   - genuine five-pāda forms, which `meter_engine` does not accept (పంచపాది, five-line ettugeeti).
3. **Vemana, 149 poems that fit no metre.** Their labels stay heuristic.
4. **Bhāgavatam.**
   - The 627 yati failures on canonical text point to the engine's sandhi-yati handling (1-10).
   - The prāsa of 6-523 needs the printed edition.
5. **Label sources.** Keep the label source visible in any evaluation. Engine-made labels cannot validate the engine,
   and Kuchimanchi's 56 non-engine labels do not scan.
6. **Level 3.** Do not use Te–En ≥ 0.65 as a fidelity gate. Report poem–bhavam AUC and recall with LaBSE or IndicSBERT,
   or a threshold calibrated on shuffled pairs.
7. **Splits.** Keep poems that share a makuta (Vemana, the śatakas) in one split, or refrain lines will leak between
   train and test.

## Reproduce

```bash
cd data_sanity_metrics && HF_HUB_OFFLINE=1 WORKERS=16 bash run_all.sh
```

- **From scratch:** about 45 minutes on this machine, most of it level-1 scansion and level-3 encoding.
- **With warm caches** (`outputs/cache/`): about 10 minutes.
- **Single scripts:** any script also runs alone, and `--datasets` restricts it to chosen files.

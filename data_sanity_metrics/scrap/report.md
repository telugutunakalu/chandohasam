# Do the IndicNeuroSym data-sanity metrics make sense?

Re-implementation and audit of the corpus-validation metrics in
*IndicNeuroSym* (`Notes/indic_nuerosym.pdf`, §5, Tables 3–4 and 14–18) on the
paper's own dataset. LLM-as-a-judge (Level 5) is excluded. Every number below
comes from a script in this folder; the JSON behind each is in `outputs/`.

## Summary

Nearly every number in §5 reproduces, most of them exactly, once the undocumented
choices are recovered: character units, the prompt prefix, the half-open
window, whitespace tokenisation. What the numbers *mean* holds up much less
well. Each metric was also run on control data it ought to reject. Only a few
of them do.

| Level | Metric | Reproduced? | Does it measure what the paper says? |
|---|---|---|---|
| 1 | Prosodic integrity 100% | exactly | **Partly.** True by construction. An independent scanner passes 90.2%. The paper's yati check passes 55% of *random* akshara pairs because of its svara-yati fallback. Gaṇa and prāsa discriminate; yati barely does. |
| 2 | Length ratio 99.1% | exactly (bins, pass count, top-5) | **No.** A poem paired with a random other couplet's gloss passes 99.0%. The gate cannot tell a right gloss from a wrong one. About a quarter of its failures are a field-parsing bug, not bad translations. |
| 3 | LaBSE Te↔En ≥ 0.65 (77.1%) | yes: mean 0.721 exact, 76.9% on master | **It checks translation consistency, not fidelity to the poem.** It never looks at the verse: it compares two glosses from the same LLM response. Its "failures" are mostly a formatting artifact: glosses with the `తెలుగు:` prompt label pass 47%, those without pass 93%. |
| 4 | TTR 0.491, Yule's K 3.50, Honoré's H 6,165, hapax 0.804, Sichel's S 0.091 | exactly | **Values right, interpretation wrong.** At equal token count the verse is *more* diverse than the corpus's own Telugu prose (TTR 0.49 vs 0.20). The "0.70–0.80 modern prose" and "1,000–2,000 literary" references are English, short-text norms. |
| 4 | MATTR(w=50) 0.501 | **no: correct value is 0.983** | Bug. 0.501 is reproduced only by computing MATTR over tokens grouped by type (e.g. `Counter.elements()` order). |
| 4 | Per-poem TTR / MATTR(w=2) / Yule's K / Honoré's H | yes except H | **Degenerate.** 95.7% of poems have no repeated word (TTR = 1, K = 0, H undefined). The H mean depends entirely on how the undefined cases are handled. |
| 4 | Gemma 3 "coverage" 74.4% | 1,784 vocab and 804,671 tokens exact; 1,319 vs 1,328 used | **Mislabelled.** It is vocabulary *utilisation*. The tokenizer-fit numbers are: 18.5% of token boundaries fall inside an akshara; 4.5 tokens per word. |
| 4 | 0 exact / 160 near-duplicates in 79 groups | exactly | **The "near" duplicates are true duplicates**: the same couplet with different word spacing. 81 redundant records remain in the "deduplicated" corpus. |
| 1–3 | Pass all levels 1–3: 68.9% | **no: 76.3% on master** | Mixed denominators (L3 on 29,343, the rest on 27,881). With the prompt prefix stripped it is 92.3%. The failing records are still in the 27,881-couplet training corpus (§6). |

## Data and reproduction of the corpus

- Dataset: `dwipada_consolidated.json`, sha256 `4f63ed94…cdab99` (matches the
  Git LFS pointer in the paper repo), 34,134 records. The paper's 27,881
  "master" corpus is not stored separately. It is the 28,062 Schema-A records
  that pass the paper's own analyser (`dwipada_analyser.analyze_dwipada`).
  `build_subsets.py` rebuilds it, and every per-source count in Table 3 matches:

  | source | schema A | master (ours) | master (paper) |
  |---|---|---|---|
  | Ranganatha Ramayanamu | 21,895 | 21,828 | 21,828 |
  | Basavapuranamu | 1,871 | 1,859 | 1,859 |
  | Dvipada Bhagavatamu | 2,014 | 2,002 | 2,002 |
  | Palanati Vira Charitra | 66 | 65 | 65 |
  | Srirama Parinayamu | 377 | 374 | 374 |
  | Synthetic (Gemini) | 1,839 | 1,753 | 1,753 |
  | **total** | 28,062 | **27,881** | **27,881** |

- Not reconstructable: the 29,343-record "augmented" set that Level 3 was
  computed on (the consolidated file keeps one copy of each poem). Level 3 is
  therefore measured on the 27,881 master couplets.
- Table 3's *raw* counts (36,578) and purity rates come from pre-dedup files
  that are no longer in the repo, so they cannot be checked.

---

## Level 1 — Prosodic integrity (paper: 100%)

**Reproduced: 100.0%** (27,881/27,881). This is true by construction: the same
scanner defines membership in the corpus. On its own it therefore tests only
that the filter ran.

### Independent scanner

This repo's `meter_engine/chandohasam`, with the metre forced to dvipada, was
run over all 28,062 Schema-A couplets (`level1_prosodic_integrity.py`).

| rule | master pass (relaxed) | master pass (strict) | the 181 couplets the paper rejected |
|---|---|---|---|
| gaṇa + 11–15 aksharas | 100.0% | 100.0% | 23.8% |
| prāsa | 99.2% | 98.4% | 23.2% |
| yati, line 1 | 93.0% | 92.9% | 20.4% |
| yati, line 2 | 97.6% | 97.4% | 23.2% |
| **all rules** | **90.2%** | **89.1%** | 19.9% |

- **Gaṇa: full agreement.** Every master couplet parses as Indra³·Sūrya
  under both scanners, and chandohasam also rejects 76% of the couplets the
  paper's scanner rejected. The gaṇa component is solid.
- **Yati: almost all of the disagreement.** Grouping chandohasam's yati
  rejections by the rule the paper's analyser used to *accept* the line:

  | paper's accepting rule | master lines | chandohasam rejects |
  |---|---|---|
  | exact letter match | 27,985 (50.2%) | 0.6% |
  | varga (maitri group) match | 14,656 (26.3%) | 0.5% |
  | **svara yati** (vowel-only fallback) | **13,110 (23.5%)** | **17.9% (2,346 lines)** |

  The paper's analyser falls back to `check_svara_yati` whenever the
  consonants are not in maitri. It accepts the pair if the two aksharas'
  *vowels* share a group. There are only three vowel families (a/ā/ai/au,
  i/ī/e/ē, u/ū/o/ō), so any two aksharas carrying the inherent *a* pass,
  whatever their consonants. Examples chandohasam rejects:

  | line | yati aksharas | consonant groups (paper's Table 10) |
  |---|---|---|
  | కీ రాదె నీ నాక మేల యిచ్చెదవు | కీ ~ మే | velar vs labial nasal |
  | నప్పుడు గోవిందు డఖలసైనికులు | న ~ డ | nasal vs retroflex |
  | ననిన రాఘవుడుదశాననుచంద | న ~ శా | nasal vs palatal-sibilant |

- **Prāsa: 210 couplets (0.75%)**, all failing classical rules the paper's
  analyser does not implement. It only compares the base consonant of the
  second akshara. chandohasam also requires a uniform weight for the
  pre-prāsa akshara (నా (U) vs తి (I)), a consistent pūrṇabindu before the prāsa
  (కొం|ద vs మ|ది), and no *adhika-prāsa* (న్నె vs ను).

### How often would each rule pass by chance?

`level1_chance_pass_rates.py` scores akshara pairs taken from *unrelated* lines
with the paper's own functions:

| check | real pairs | random pairs |
|---|---|---|
| prāsa (line 1 of couplet i vs line 2 of couplet j) | 100% | **9.3%** |
| yati, full cascade (paper) | 100% | **55.3%**: 40.8 points of it via svara-yati |
| yati, cascade without svara-yati | 79.0% | 15.2% |

**Verdict.** Gaṇa and prāsa are meaningful constraints; prāsa passes 9% by
chance. The yati check as implemented passes more than half of random pairs,
so "100% yati" certifies little. With the fallback removed, yati becomes
discriminative (15% chance), but only 79% of master lines satisfy it. Whether
svara yati is admissible when the consonants are not in maitri is a question
of prosody, and yours to settle. Either way the paper should report the rule
set, per-rule pass rates and chance rates, not a single "100%". Note also that
§3.1 and Table 10 describe maitri-group matching only; the svara fallback is
mentioned only for the decoder's yati NFA (§7.4).

---

## Level 2 — Length ratio (paper: 99.1%)

**Reproduced exactly**: 27,633/27,881 pass, mean 1.634, median 1.608, all five
Table 14 bins (1 / 78 / 9,333 / 15,449 / 3,020), and the five extremes
5.11 4.73 4.71 4.65 4.36. The paper leaves the definition out. It is:
**non-whitespace characters, the Telugu meaning taken raw, window [0.8, 2.5)**
with the upper bound excluded. "Raw" means the `తెలుగు:` / `Telugu:` prompt
prefix is counted in the 9,916 records that carry it.

| variant | pass (true pairs) | **pass (poem + random other gloss)** | pass (poem + previous couplet's gloss) |
|---|---|---|---|
| paper (chars, raw) | 99.11% | **98.98%** | 99.05% |
| chars, prefix stripped | 99.43% | 99.32% | 99.36% |
| words | 88.68% | 87.01% | 86.87% |
| aksharas | 99.87% | 99.82% | 99.87% |

- **The gate cannot detect a misaligned gloss.** Mismatched pairs pass as
  often as true ones. The ratio only constrains the gloss's *length*, and
  Telugu glosses of two-line couplets all have about the same length.
- **What it does catch is a bug.** 61 master records have the *English* gloss
  inside the `telugu_meaning` field (`తెలుగు: … \nEnglish: …`). 59 of them are
  among the 248 failures, including the most extreme ratio (5.11). The paper
  calls these "suspect translations rather than valid couplets"; they are
  parsing defects of the LLM output.
- The failing records are not removed: §6 trains on all 27,881.

**Verdict.** Useful as a formatting lint (truncated, duplicated or merged
fields), not as evidence of prose–verse alignment. Report it as such, and fix
the 61 merged fields.

---

## Level 3 — Semantic fidelity (paper: LaBSE Te↔En ≥ 0.65 on 77.1%)

**Reproduced** with LaBSE on the 27,881 master couplets: Telugu↔English mean
**0.721** (paper 0.721), 76.9% ≥ 0.65 (paper 77.1% on its 29,343 set). The
Table 17 shares also match: 2.0 / 36.4 / 55.3 / 6.2% in the 0.3–0.5 / 0.5–0.7 /
0.7–0.85 / 0.85–1.0 bins, against the paper's 2.0 / 36.2 / 55.5 / 6.3%.

### 1. The gate never looks at the poem

The gate compares the Telugu gloss with the English gloss. The dataset has
**no human English translations**: `english_meaning` (non-empty in all 27,881
records) is an English bhāvam the LLM wrote in **the same response** as the
Telugu one. The stored prompt asks for the bhāvam "in single line in telugu
and English" in one call. Agreement between them is expected by
construction. As a translation-consistency check it works very well: AUC
against shuffled pairs is 1.000, and the true English gloss is the nearest of
2,000 candidates 99.4% of the time. But it says nothing about whether either
gloss explains the verse.

### 2. The 23% "failures" are mostly a formatting artifact

9,916 Telugu glosses begin with the prompt's label `తెలుగు:` (9,559) or
`Telugu:` (357). LaBSE sees the label as content:

| Telugu gloss | n | LaBSE Te↔En ≥ 0.65 |
|---|---|---|
| with the label | 9,916 | **47.2%** |
| without the label | 17,965 | **93.4%** |
| all, label stripped | 27,881 | 93.2% |

The same artifact creates the apparent quality gap between sources. Synthetic
glosses never carry the label and pass 94.2%. The classical sources pass
69–77% raw, but 90–93% once the label is stripped. The gate is also blind to
the 61 merged-field records from Level 2: their "Telugu" field contains the
English gloss verbatim, so all 61 pass (mean 0.77).

### 3. A fixed 0.65 means different things for different encoders and pairs

Per encoder and pair: the pass rate at 0.65, the same for shuffled (wrong)
pairs, the AUC of true vs shuffled pairs, recall@1 when retrieving the true
partner among 2,000 candidates (chance 0.05%), and the pass rate at a
threshold calibrated to let only 1% of shuffled pairs through.

| encoder | pair | pass @0.65 (paper) | shuffled pass @0.65 | AUC vs shuffled | R@1 / 2,000 | calibrated threshold → pass |
|---|---|---|---|---|---|---|
| LaBSE | poem ↔ Te | 1.4% | 0.0% | 0.910 | 30.5% | 0.269 → 50.5% |
| LaBSE | poem ↔ En | 0.7% | 0.0% | 0.911 | 30.1% | 0.270 → 50.1% |
| LaBSE | Te ↔ En | 76.9% (77.1%) | 0.0% | 1.000 | 99.4% | 0.389 → 99.8% |
| LaBSE | Te ↔ En, label stripped | 93.2% | 0.0% | 1.000 | 99.7% | 0.402 → 99.99% |
MSBERT_INDIC_ROWS| MiniLM (English-only, **negative control**) | poem ↔ Te | **89.7%** | **89.4%** | 0.506 | 0.3% | 0.929 → 0.5% |
| MiniLM (English-only, **negative control**) | Te ↔ En | 0.2% | 0.0% | 0.519 | 0.4% | 0.233 → 1.9% |

- The negative control shows what the absolute threshold is worth. An
  encoder that cannot read Telugu script "passes" 89.7% of verse↔Telugu-gloss
  pairs, and passes shuffled pairs just as often. Its AUC is 0.5. The
  threshold says nothing until it is calibrated against wrong pairs.
- LaBSE's low verse↔gloss scores (mean 0.28) hide real signal. It ranks the
  right gloss first among 2,000 candidates 30% of the time, 600× chance. The
  paper's reading, that "low poem-to-meaning similarities are expected and
  reflect genre distance", is right about the level but wrong to conclude the
  score is uninformative.
MSBERT_INDIC_NOTES
**Verdict.** Reported as "semantic fidelity", this level certifies
translation consistency between two glosses from one LLM call. That is worth
checking, and with the label stripped 93% pass. It does not measure how
faithful the glosses are to the verse. For that, use the verse↔gloss pairs,
report AUC or retrieval, and flag records against a threshold calibrated on
shuffled pairs. At 1% false accept, about half the corpus clears LaBSE's
verse↔gloss bar. The other half is not proof of misalignment, since archaic
verse is hard for LaBSE, but it is where a human check should start.

---

## Level 4 — Lexical diversity

### Corpus-level measures

The paper's tokenisation is plain whitespace splitting of the poem, which
reproduces N = 179,812 and V = 88,295 exactly. The controls are the corpus's
own Telugu prose meanings and English meanings, cut to the **same N**, with
punctuation stripped and English lower-cased.

| measure | paper | verse | Telugu prose (same N) | English prose (same N) |
|---|---|---|---|---|
| TTR | 0.491 | 0.491 | 0.200 | 0.053 |
| **MATTR (w=50)** | **0.501** | **0.983** | 0.958 | 0.843 |
| Yule's K | 3.497 | 3.497 | 19.03 | 109.98 |
| Honoré's H | 6,164.7 | 6,164.7 | 3,095.5 | 1,967.3 |
| hapax ratio | 0.804 | 0.804 | 0.609 | 0.385 |
| Sichel's S | 0.091 | 0.091 | 0.141 | 0.141 |

- **MATTR is wrong in the paper.** With a 50-token window it is 0.983. A value
  near 0.5 needs a window over 50,000 tokens (0.618 at 50k). 0.501 is
  reproduced (0.500) by running MATTR on the tokens *grouped by type*, the
  order `Counter.elements()` or a sorted list produces. Identical tokens then
  sit next to each other, and the moving average collapses to about V/N.
- **The TTR comparison runs the wrong way.** TTR falls with N (growth curve
  below). The "0.70–0.80 typical of modern prose" range is what 100–1,000-token
  English texts score; the English meanings here score 0.76 at N = 100. At the
  corpus's N, the verse (0.49) is 2.5× *more* type-rich than its Telugu prose
  (0.20). That contradicts "consistent with the formulaic repetition inherent
  to metrical verse".

  | N | verse | Telugu prose | English prose |
  |---|---|---|---|
  | 100 | 0.980 | 0.930 | 0.760 |
  | 1,000 | 0.910 | 0.764 | 0.521 |
  | 10,000 | 0.769 | 0.503 | 0.244 |
  | 100,000 | 0.548 | 0.249 | 0.075 |
  | 179,812 | 0.491 | 0.200 | 0.053 |

- **The Yule's K and Honoré's H references are English norms.** The English
  glosses land at K = 110, *outside* "the literary range (K < 100)", and at
  H = 1,967, inside "the 1,000–2,000 literary baseline". The Telugu glosses,
  plain modern prose, already reach H = 3,096. Telugu's agglutinative
  morphology inflates type counts. Verse inflates them further: a whitespace
  token in the verse averages 4.0 aksharas against 3.5 in the prose (sandhi
  fusion), and word boundaries are placed inconsistently across editions (see
  Duplicates). High H here is not evidence of "exceptional vocabulary
  richness".

### Per-poem measures (paper: TTR 0.993, MATTR(w=2) 1.000, K 22.74, H 2,356.4)

A couplet has 6.4 whitespace tokens on average (range 2–12).
**95.7% of couplets contain no repeated token.** For those, TTR = 1, Yule's
K = 0 and Honoré's H is undefined (division by zero, V₁ = V). The reproduced
means (TTR 0.993, K 22.74) come from the remaining 4.3%. The paper's H mean of
2,356.4 cannot be reproduced. Over the 1,203 couplets where H is defined it is
1,285, and substituting a small epsilon for the zero gives anything from
3,500 to 175,000. MATTR with window 2 only asks whether a token repeats its
neighbour. These four per-poem numbers carry no information about the corpus
and should be dropped.

### Gemma 3 subword statistics (`level4_subword_coverage.py`)

Reproduced with the Gemma 3 tokenizer: 1,784 Telugu tokens in the vocabulary,
804,671 tokens over the verse, per-poem subword TTR 0.897. The verse uses
**1,319** of the 1,784 (73.9%), not 1,328 (74.4%). Master, Schema A and all
records give 1,319, 1,322 and 1,340, so the paper's count was probably taken
on the 29,343 augmented set while the token total came from master.

"Coverage" here is *utilisation*: how much of the tokenizer's Telugu inventory
the corpus touches. A byte-fallback tokenizer covers every string, so this
says nothing about fit. The measures that bear on the paper's own motivation
(§1: subword tokenizers fragment aksharas) are:

| | verse | Telugu prose |
|---|---|---|
| tokens per whitespace word | 4.48 | 3.19 |
| tokens per akshara | 1.12 | 0.92 |
| token boundaries falling *inside* an akshara | **18.5%** | 16.9% |

Table 4's "Lexical diversity (TTR) 0.90 avg" is the per-poem *subword* TTR
(0.897), not a word TTR (per-poem word TTR is 0.993).

### Duplicates (`level4_duplicates.py`)

| criterion | groups | poems | redundant records |
|---|---|---|---|
| exact poem string | 0 | 0 | 0 |
| whitespace + punctuation removed (**= the paper's 79 / 160**) | 79 | 160 | 81 |
| also ZWNJ and arasunna removed | 80 | 162 | 82 |
| character-3-gram Jaccard ≥ 0.9 | 95 | 193 | 98 |
| Jaccard ≥ 0.8 | 141 | 285 | 144 |
| Jaccard ≥ 0.7 | 182 | 374 | 192 |

- The paper's "near-duplicates under normalisation" are exact duplicates once
  spaces and punctuation are removed. They are the same couplet split into
  words differently (`ఇది యసంఖ్యాత…` / `ఇదియ సంఖ్యాత…` / `ఇది యసంఖ్యాతమాహేశ్వరదివ్య`),
  i.e. repeated scrapes or editions. 81 of them should have been removed by the
  dedup step. All groups fall within a single source.
- 510 distinct pādas recur in more than one couplet (897 couplets, 3.2%), up
  to five times each (`విన్ననై వదనారవిందంబు వాంచి`). This is expected formulaic
  reuse in oral-epic verse, but it matters for a random train/test split. The
  split files (`train.jsonl`/`eval.jsonl`) are LFS pointers locally, so
  leakage could not be checked.
- Glosses are not recycled: one pair of poems shares an identical Telugu gloss.

---

## Cross-level summary (Table 4 on one denominator, n = 27,881)

`cross_level_summary.py`:

| level | check | paper | ours |
|---|---|---|---|
| 1 | prosodic integrity, paper's analyser | 100.0% | 100.0% |
| 1′ | prosodic integrity, chandohasam (relaxed) | — | 90.2% |
| 2 | length ratio in [0.8, 2.5) | 99.1% | 99.1% |
| 3 | LaBSE Te↔En ≥ 0.65 | 77.1% | 76.9% |
| 3* | same, prompt label stripped | — | 93.2% |
| 4 | "Lexical diversity (TTR) 0.90 avg" = per-poem subword TTR | 0.90 | 0.897 |
| 1–3 | pass all of levels 1–3 | **68.9%** | **76.3%** |
| 1–3* | pass all, label stripped for L3 | — | 92.3% |
| 1′–3 | pass all, chandohasam as L1 | — | 68.9% |

- The paper's 68.9% does not reproduce on the master set (76.3%). It
  presumably mixes the 29,343-record L3 denominator with the 27,881-record
  L1/L2 ones. Using chandohasam as Level 1 happens to give 68.9%. As far as I
  can tell that is a coincidence, since the paper used its own analyser.
- A "pass all levels" figure implies the levels are filters, but none of the
  failures were removed: the 27,881 couplets used for fine-tuning (§6)
  include every Level 2 and Level 3 failure.
- The Level 4 row reports an average, not a pass rate, and is labelled TTR
  though it is the subword TTR.

---

## Recommendations for the paper

1. **Level 1**: report per-rule pass rates and chance pass rates, name the
   yati rule set, and decide on svara yati. An independent scanner (e.g.
   chandohasam at 90.2%) is a stronger claim than a circular 100%.
2. **Level 2**: present it as a formatting check, not an alignment check;
   state the unit; strip the prompt prefix; fix the 61 merged Telugu/English
   fields.
3. **Level 3**: strip the prompt label before encoding (77.1% → 93.2%); call
   the Te↔En gate what it is, translation consistency; for fidelity to the
   verse, report AUC or retrieval of verse↔gloss pairs and flag records
   against a threshold calibrated on shuffled pairs, not a fixed 0.65.
4. **Level 4**: fix MATTR (0.983); drop the English reference ranges and
   compare against a Telugu prose baseline at equal N instead; drop the
   per-poem TTR, MATTR(w=2), K and H; relabel "coverage" as utilisation and
   add fertility and akshara-split rate; remove the 81 spacing variants.
5. **Table 4**: use one denominator throughout, and say whether failing
   records were filtered. Currently they are not.

## Caveats

- chandohasam is a second implementation, not ground truth. Where the two
  scanners disagree (svara yati, the extra prāsa rules), the correct answer is
  a prosody decision.
- The paper does not name the L3Cube checkpoint.
  `l3cube-pune/indic-sentence-bert-nli` (the paper's "IndicSBERT") is used
  here. The paper gives no threshold for mSBERT or IndicSBERT; 0.65 is assumed.
- Level 3 runs on the 27,881 master couplets, not the unreconstructable
  29,343 augmented set.
- Fine-tuning splits were not available locally (LFS pointers), so
  train/test leakage from the duplicates and reused pādas is unmeasured.

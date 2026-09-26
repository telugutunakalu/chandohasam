# Sample poems — DiffusionGemma 26B-A4B, constrained decoding

Sample poems from the **DiffusionGemma 26B-A4B** constrained-decoding grid: two metrically perfect poems
for each of the 37 meters and each of the three decoding strategies, with the prompt and the
probability of every chosen token.

| | |
|---|---|
| model | `nvidia/diffusiongemma-26B-A4B-it-NVFP4` — NVIDIA's NVFP4 build of `google/diffusiongemma-26B-A4B-it` (block diffusion), loaded by this project's own loader with the experts decoded once to BF16 |
| run | `experiments/runs/2026-09-25_diffusion_constrained` — 37 meters × 3 topics × 5 seeds × 3 strategies = 1,665 poems, **all complete and accepted by the engines** |
| constraint | gaṇa + prāsa + yati enforced exactly on the metrical DAWG (strict profile, yati sandhi off), with the orthography filter — the same enforcer as the E4B runs |
| decoding | a 256-token canvas whose left part is frozen once validated; each denoising pass keeps the model's own proposals, left to right, while they are allowed and jointly confident (entropy bound 0.1); otherwise the strategy decides the first open position. Temperature follows the model's schedule, 0.8 → 0.4 over 48 passes. End-of-text is removed from the canvas so the poem ends only when the meter does |
| strategies | **masking only** — a masked draw at the first open position; **masking + backtracking** — the same, unfreezing back to a checkpoint when the allowed set collapses; **hybrid** — the same mask, preferring allowed tokens that complete the line (a proposal is kept only if it is among them) |
| prompt | the same system and user messages as the E4B runs, followed by the model's empty thinking channel (`<\|channel>thought\n<channel\|>`), which DiffusionGemma needs in order to answer at all |

### How the samples were chosen

Every poem shown is **metrically perfect**: complete, and accepted by the repository's engines for
gaṇa, prāsa and yati under the strict profile (the engines judge the poem; the decoder only enforces).
Within each meter and strategy (15 poems: 3 topics × 5 seeds) the two shown are the best by, in order:

1. no line repeated (a repeated line satisfies prāsa trivially);
2. the share of words that have two or more aksharas **and** occur in the verse corpora of this
   repository (`dataset/*.json`) — single aksharas are left out because filler such as క క క is in
   the lexicon;
3. the mean log-probability of the chosen tokens.

Metrically perfect is not the same as good Telugu. The constraint keeps every poem in meter, but most
of the words are not real words — the "corpus words" figure under each poem says how many are.

### Reading a sample

* **gaṇa pattern** — the engines' scansion of each line: `U` guru, `I` laghu.
* **Token probabilities** (click to expand) — every token of the poem in order, with the model's
  probability of that token over its whole vocabulary at temperature 1, recorded when the token was
  chosen. `␣` marks a token that begins with a space, `⏎` a line break.
* **✱** — the model's own first choice was not allowed by the meter; the constraint chose this token.
* **forced** — a line break imposed because the line was complete and could not be extended.
* Summary line: *mean token probability* is the geometric mean over the poem; *first choice kept* is
  the share of tokens that were the model's most probable token; *constraint overrode* is the share
  of tokens where the model's first choice was not allowed.

## Meters

| # | meter | |
|---|---|---|
| 1 | ఉత్పలమాల (utpalamala) | [samples](#utpalamala) |
| 2 | చంపకమాల (champakamala) | [samples](#champakamala) |
| 3 | మత్తేభవిక్రీడితము (mattebhavikriditamu) | [samples](#mattebhavikriditamu) |
| 4 | శార్దూలవిక్రీడితము (sardulavikriditamu) | [samples](#sardulavikriditamu) |
| 5 | స్రగ్ధర (sragdhara) | [samples](#sragdhara) |
| 6 | మహాస్రగ్ధర (mahasragdhara) | [samples](#mahasragdhara) |
| 7 | తోటకము (totakamu) | [samples](#totakamu) |
| 8 | భుజంగప్రయాతము (bhujangaprayatamu) | [samples](#bhujangaprayatamu) |
| 9 | మత్తకోకిలము (mattakokilamu) | [samples](#mattakokilamu) |
| 10 | పంచచామరము (pamcacamaramu) | [samples](#pamcacamaramu) |
| 11 | వసంతతిలకము (vasamtatilakamu) | [samples](#vasamtatilakamu) |
| 12 | ఇంద్రవజ్ర (indravajra) | [samples](#indravajra) |
| 13 | ఉపేంద్రవజ్ర (upendravajra) | [samples](#upendravajra) |
| 14 | శాలిని (salini) | [samples](#salini) |
| 15 | రథోద్ధత (rathoddhata) | [samples](#rathoddhata) |
| 16 | స్రగ్విణి (sragvini) | [samples](#sragvini) |
| 17 | విద్యున్మాల (vidyunmala) | [samples](#vidyunmala) |
| 18 | లలిత (lalita) | [samples](#lalita) |
| 19 | కందము (kandamu) | [samples](#kandamu) |
| 20 | ఉత్సాహము (utsahamu) | [samples](#utsahamu) |
| 21 | తరువోజ (taruvoja) | [samples](#taruvoja) |
| 22 | ద్విపద (dvipada) | [samples](#dvipada) |
| 23 | మధ్యాక్కర (madhyakkara) | [samples](#madhyakkara) |
| 24 | మధురగతి రగడ (madhuragati_ragada) | [samples](#madhuragati_ragada) |
| 25 | తురగగతి రగడ (turagagati_ragada) | [samples](#turagagati_ragada) |
| 26 | హయప్రచార రగడ (hayapracara_ragada) | [samples](#hayapracara_ragada) |
| 27 | సీసము (seesamu) | [samples](#seesamu) |
| 28 | ఆటవెలది (ataveladi) | [samples](#ataveladi) |
| 29 | తేటగీతి (tetagiti) | [samples](#tetagiti) |
| 30 | తరళము (taralamu) | [samples](#taralamu) |
| 31 | మాలిని (malini) | [samples](#malini) |
| 32 | మానిని (manini) | [samples](#manini) |
| 33 | కవిరాజవిరాజితము (kavirajavirajitamu) | [samples](#kavirajavirajitamu) |
| 34 | వనమయూరము (vanamayuramu) | [samples](#vanamayuramu) |
| 35 | మంగళమహాశ్రీ (mangalamahasri) | [samples](#mangalamahasri) |
| 36 | లయగ్రాహి (layagrahi) | [samples](#layagrahi) |
| 37 | లయవిభాతి (layavibhati) | [samples](#layavibhati) |

---

<a id="utpalamala"></a>

## 1. ఉత్పలమాల (utpalamala)

```text
Meter: ఉత్పలమాల (utpalamala), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: భ ర న భ భ ర వ, i.e. UII UIU III UII UII UIU IU (20 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 10th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T2; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter ఉత్పలమాల (utpalamala).

Meter: ఉత్పలమాల (utpalamala), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: భ ర న భ భ ర వ, i.e. UII UIU III UII UII UIU IU (20 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 10th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 125 tokens · 32.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాయమ సిమ్య చక్క జగ మ్రల్య నమున్ జయ లంకముశ్రమాయ్ | `UIIUIUIIIUIIUIIUIUIU` |
| 2 | మాయ నమర్వరన్ జల ల ల్య్య్మమ్య లముక్ష్న యశోరరామమమ్ | `UIIUIUIIIUIIUIIUIUIU` |
| 3 | జాయమ ల్యమ్యమున్న్మమ సి మ్య్య్శమ్రలణైముము జయ్య లాయ్ ట్టిలుత్ | `UIIUIUIIIUIIUIIUIUIU` |
| 4 | వాయన నన్య నిమ్యమ మ్య మ్య్య్వర్వర భర్ర భ భర్వరల్యుడుక్ | `UIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.017 · model's first choice kept 26% · constraint overrode 59% · backtracks 0

<details><summary>Token probabilities (125 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.20 · `య` 0.02 · `మ` 0.02 · `␣సి` 3.4e-3 · `మ` 0.02✱ · `్య` 7.8e-4✱ · `␣చక్క` 3.6e-4 · `␣జ` 0.06 · `గ` 0.02 · `␣మ` 1.4e-3✱ · `్ర` 3.5e-3✱ · `ల` 0.02✱ · `్య` 1.7e-4✱ · `␣న` 0.01 · `ము` 0.10 · `న్` 0.08✱ · `␣జ` 0.15 · `య` 0.35 · `␣ల` 0.03✱ · `ంక` 0.73 · `ము` 8.5e-3✱ · `శ` 0.06✱ · `్ర` 3.1e-3✱ · `మ` 0.11✱ · `ాయ` 0.02✱ · `్` 6.5e-5✱ · `⏎` 0.52 |
| 2 | `మ` 0.16 · `ాయ` 0.69 · `␣న` 0.01 · `మ` 0.03 · `ర` 0.03 · `్వర` 9.2e-5✱ · `న్` 0.02✱ · `␣జ` 0.23 · `ల` 0.06 · `␣ల` 0.04 · `␣ల` 0.04✱ · `్య` 1.1e-3✱ · `్య` 5.5e-3✱ · `్` 3.7e-5✱ · `మ` 0.03✱ · `మ` 0.04✱ · `్య` 6.6e-3✱ · `␣ల` 0.06 · `ము` 0.26 · `క్ష్` 0.02✱ · `న` 0.58 · `␣య` 3.6e-3✱ · `శ` 0.14✱ · `ో` 0.04✱ · `ర` 0.03✱ · `రా` 0.23 · `మ` 0.18 · `మ` 0.47 · `మ` 0.16 · `్` 3.6e-5✱ · `⏎` 0.40 |
| 3 | `జ` 0.10 · `ాయ` 0.03✱ · `మ` 0.03 · `␣ల` 0.26 · `్య` 0.65 · `మ` 0.11 · `్య` 6.3e-3✱ · `ము` 0.39 · `న్` 0.38 · `న్` 0.02✱ · `మ` 0.64 · `మ` 0.01✱ · `␣సి` 0.04✱ · `␣మ` 4.1e-3✱ · `్య` 0.98 · `్య` 4.2e-4✱ · `్` 8.5e-5✱ · `శ` 1.9e-4✱ · `మ` 4.8e-3✱ · `్ర` 0.97 · `ల` 0.99 · `ణ` 2.9e-3✱ · `ై` 1.8e-3✱ · `ము` 0.95 · `ము` 7.0e-3✱ · `␣జ` 0.90 · `య` 0.85 · `్య` 3.3e-3✱ · `␣ల` 0.54 · `ాయ` 0.86 · `్` 0.46 · `␣` 7.7e-4✱ · `ట్టి` 1.9e-5✱ · `లు` 2.6e-4✱ · `త` 1.7e-5✱ · `్` 1.2e-5✱ · `⏎` 6.5e-3✱ forced |
| 4 | `వా` 2.6e-3✱ · `య` 3.2e-4✱ · `న` 0.01✱ · `␣న` 0.04✱ · `న` 0.01✱ · `్య` 8.3e-3✱ · `␣ని` 0.02✱ · `మ` 0.04✱ · `్య` 5.7e-3✱ · `మ` 0.01✱ · `␣మ` 0.03✱ · `్య` 0.02✱ · `␣మ` 0.13✱ · `్య` 0.03✱ · `్య` 0.05✱ · `్వర` 1.4e-5✱ · `్వర` 7.4e-4✱ · `␣భ` 0.88 · `ర` 0.05✱ · `్ర` 2.1e-4✱ · `␣భ` 0.44 · `␣భ` 0.65 · `ర` 0.61 · `్వర` 3.5e-4✱ · `ల` 5.9e-4✱ · `్య` 9.0e-3✱ · `ు` 0.09 · `డు` 0.01✱ · `క` 1.3e-4✱ · `్` 1.2e-5✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 128 tokens · 33.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మంగ నగెళ్ల లయ్యము స స్ర్ర్మల్యము వన్రవమంగశంకమంగ్ | `UIIUIUIIIUIIUIIUIUIU` |
| 2 | గంగ నగెళ్ళ లయ్య్య సము స్ర్ర్గల్యము వన్రవమమ్ర లమ్యమున్ | `UIIUIUIIIUIIUIIUIUIU` |
| 3 | మౌంగ మ లగ్య ల్యల్యము వనవ్రమమశ్రమమున్ ర్వనన్ము వవ్ | `UIIUIUIIIUIIUIIUIUIU` |
| 4 | కైం గరమాల ఇర్ర మయు ల్య్య్కల్యము వన్రుము చెప్పగాభ రిన్ | `UIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.020 · model's first choice kept 35% · constraint overrode 54% · backtracks 0

<details><summary>Token probabilities (128 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.45 · `ంగ` 5.6e-3 · `␣న` 5.2e-3 · `గ` 0.02 · `ె` 3.2e-3✱ · `ళ్ల` 3.1e-3✱ · `␣ల` 9.7e-3 · `య` 0.06 · `్య` 3.7e-4✱ · `ము` 0.17 · `␣స` 0.03 · `␣స` 0.01✱ · `్ర` 1.5e-3✱ · `్ర` 1.5e-3✱ · `్` 7.3e-8✱ · `మ` 0.01✱ · `ల` 0.03✱ · `్య` 3.9e-4✱ · `ము` 0.26 · `␣వ` 6.9e-3 · `న` 0.10 · `్ర` 7.0e-4✱ · `వ` 4.3e-3✱ · `మ` 0.88 · `ంగ` 0.86 · `శ` 5.1e-3✱ · `ంక` 3.3e-3 · `మ` 0.06✱ · `ంగ` 0.05✱ · `్` 5.1e-6✱ · `⏎` 0.44 forced |
| 2 | `గ` 0.01 · `ంగ` 0.54 · `␣న` 0.14 · `గ` 0.07 · `ె` 0.24 · `ళ్ళ` 5.0e-3✱ · `␣ల` 0.17 · `య` 0.29 · `్య` 0.36 · `్య` 0.06 · `␣స` 0.25 · `ము` 0.39 · `␣స` 0.01✱ · `్ర` 8.0e-3✱ · `్ర` 0.03✱ · `్` 0.33✱ · `గ` 1.5e-4✱ · `ల` 0.72 · `్య` 0.75 · `ము` 0.83 · `␣వ` 0.75 · `న` 0.61 · `్ర` 0.13 · `వ` 0.48 · `మ` 0.21 · `మ` 0.41 · `్ర` 5.6e-4✱ · `␣ల` 0.05✱ · `మ` 0.05✱ · `్య` 2.1e-3✱ · `ము` 0.07✱ · `న` 0.06✱ · `్` 1.3e-4✱ · `⏎` 0.75 |
| 3 | `మ` 0.46 · `ౌ` 8.1e-4✱ · `ంగ` 3.0e-4✱ · `␣మ` 0.31 · `␣ల` 0.02 · `గ` 0.24 · `్య` 0.03✱ · `␣ల` 0.27 · `్య` 0.10✱ · `ల` 0.22 · `్య` 0.30 · `ము` 0.51 · `␣వ` 0.20 · `న` 0.28 · `వ` 0.05✱ · `్ర` 2.3e-3✱ · `మ` 0.45 · `మ` 0.17✱ · `శ` 0.11 · `్ర` 0.01✱ · `మ` 0.11 · `ము` 0.11✱ · `న` 0.02✱ · `్` 2.4e-3✱ · `␣` 4.2e-3✱ · `ర్` 3.2e-4✱ · `వ` 8.7e-4✱ · `న` 0.03✱ · `న్` 2.1e-3✱ · `ము` 5.0e-3✱ · `␣వ` 1.1e-3✱ · `వ` 4.3e-3✱ · `్` 2.0e-3✱ · `⏎` 0.30 |
| 4 | `క` 0.03✱ · `ై` 0.02✱ · `ం` 1.6e-3✱ · `␣` 6.6e-4✱ · `గర` 7.3e-5✱ · `మాల` 0.92 · `␣ఇ` 0.01✱ · `ర` 5.1e-4✱ · `్ర` 5.6e-3✱ · `␣మ` 0.02✱ · `యు` 0.18 · `␣ల` 2.8e-3✱ · `్య` 7.9e-3✱ · `్య` 0.52 · `్` 2.9e-6✱ · `క` 2.7e-4✱ · `ల` 0.01✱ · `్య` 3.3e-4✱ · `ము` 0.19✱ · `␣వ` 0.22 · `న` 0.78 · `్రు` 2.7e-4✱ · `ము` 0.96 · `␣చెప్ప` 0.59 · `గా` 1.4e-4✱ · `భ` 0.39 · `␣ర` 0.31 · `ిన` 4.5e-3✱ · `్` 6.8e-6✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 109 tokens · 49.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాము భడర్వరన్ శమన స్రహ్మమముస్రహమల్రవామురజ్ | `UIIUIUIIIUIIUIIUIUIU` |
| 2 | ల్యా మున దీరసడ్రియ నయన్ జయనున్కమొడన్న్లడర్వనుబ్ | `UIIUIUIIIUIIUIIUIUIU` |
| 3 | మౌ మున డుల్లనిత్యమును మల్రవనిత్తపలాలలాడుగెడ్ | `UIIUIUIIIUIIUIIUIUIU` |
| 4 | సౌ మున సీతనిన్ ర రచు జయ్వరమాల గయమ్రమున్రుగడ్ | `UIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 20% · repeated lines 0 · mean token probability (geometric) 0.028 · model's first choice kept 40% · constraint overrode 50% · backtracks 30

<details><summary>Token probabilities (109 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.96 · `ము` 0.15 · `␣భ` 0.95 · `డ` 0.95 · `ర` 0.98 · `్వర` 2.6e-4✱ · `న్` 0.03✱ · `␣శ` 0.96 · `మన` 3.2e-3 · `␣స` 0.01✱ · `్రహ్` 2.4e-6✱ · `మ` 0.58 · `మ` 0.07 · `ము` 0.52 · `స` 1.4e-3✱ · `్రహ` 1.2e-7✱ · `మ` 0.13 · `ల` 5.5e-3✱ · `్ర` 4.4e-5✱ · `వా` 1.3e-3 · `ము` 0.03✱ · `ర` 0.03 · `జ` 0.73 · `్` 2.3e-5✱ · `⏎` 3.8e-4✱ forced |
| 2 | `ల` 0.87 · `్యా` 0.89 · `␣` 4.1e-5✱ · `ము` 0.04✱ · `న` 2.8e-3 · `␣దీ` 0.58 · `ర` 0.94 · `స` 1.5e-3 · `డ` 0.97 · `్రియ` 0.93 · `␣న` 0.40 · `యన్` 0.10✱ · `␣జ` 0.97 · `య` 0.94 · `ను` 0.25 · `న్` 0.02✱ · `క` 0.81 · `మ` 0.92 · `ొ` 0.33 · `డ` 0.05 · `న్` 0.20 · `న్` 0.24 · `ల` 0.92 · `డ` 0.99 · `ర` 0.98 · `్వ` 2.6e-5✱ · `ను` 0.03✱ · `బ్` 4.0e-8✱ · `⏎` 0.01✱ forced |
| 3 | `మ` 8.9e-3✱ · `ౌ` 6.3e-3✱ · `␣` 0.02✱ · `ము` 3.9e-3✱ · `న` 0.13✱ · `␣` 0.57 · `డు` 0.02✱ · `ల్ల` 2.8e-3✱ · `ని` 0.09✱ · `త` 0.01✱ · `్య` 1.4e-4✱ · `ము` 0.06✱ · `ను` 0.03✱ · `␣మ` 0.08 · `ల` 0.24 · `్ర` 1.8e-3✱ · `వ` 0.03✱ · `ని` 0.03✱ · `త్త` 0.02✱ · `ప` 0.72 · `ల` 0.92 · `ాల` 8.6e-3✱ · `లా` 8.9e-4✱ · `డు` 0.03✱ · `గ` 0.02✱ · `ె` 0.03✱ · `డ` 0.02✱ · `్` 3.4e-7✱ · `⏎` 0.08✱ forced |
| 4 | `స` 0.06✱ · `ౌ` 0.05✱ · `␣` 0.48 · `ము` 6.2e-3✱ · `న` 0.28 · `␣సీ` 0.13 · `త` 0.79 · `ని` 0.13 · `న్` 0.04✱ · `␣ర` 0.81 · `␣ర` 1.1e-4✱ · `చు` 0.05✱ · `␣జ` 1.3e-3✱ · `య` 0.08 · `్వర` 6.2e-5✱ · `మాల` 0.89 · `␣గ` 0.91 · `య` 0.96 · `మ` 0.68 · `్ర` 3.4e-3✱ · `ము` 0.11 · `న` 0.22 · `్రు` 2.4e-6✱ · `గ` 0.99 · `డ` 0.99 · `్` 3.6e-4✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 107 tokens · 57.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ్రి నిరచ్రి లక్ష్మణమొగట్రు జెతియ్యనిసత్రిశత్రువున్ | `UIIUIUIIIUIIUIIUIUIU` |
| 2 | వమ్రెతి దక్రమాని నిరవస్రతనుండటకిల్లెతిశ్రమౌ | `UIIUIUIIIUIIUIIUIUIU` |
| 3 | రమ్రి జయమ్యడడ్యళె స క్ష్రమ్రమ లేదు ప ఉన్న ఇచ్చినప్ | `UIIUIUIIIUIIUIIUIUIU` |
| 4 | దమ్రి ఉ ఉత్పలాల అను వ్ర్వ్దయ్రు ఇడన్ము ఉఉత్పలాలముభ్ | `UIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 14% · repeated lines 0 · mean token probability (geometric) 0.014 · model's first choice kept 47% · constraint overrode 49% · backtracks 30

<details><summary>Token probabilities (107 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.98 · `మ` 0.97 · `్రి` 4.9e-6✱ · `␣ని` 0.01 · `ర` 0.98 · `చ` 0.76 · `్రి` 0.77 · `␣ల` 0.99 · `క్ష్` 1.00 · `మణ` 0.99 · `మ` 0.76 · `ొ` 0.99 · `గ` 0.95 · `ట` 0.99 · `్రు` 0.31✱ · `␣జ` 0.95 · `ె` 0.96 · `తి` 0.91 · `య` 8.4e-5✱ · `్య` 6.6e-6✱ · `ని` 0.05 · `స` 8.1e-3 · `త` 9.1e-3 · `్రి` 0.59 · `శ` 0.12 · `త్ర` 1.00 · `ు` 1.00 · `వు` 0.96 · `న్` 0.98 · `⏎` 2.2e-3✱ forced |
| 2 | `వ` 5.9e-5✱ · `మ` 3.8e-3✱ · `్ర` 3.2e-4✱ · `ె` 0.67 · `తి` 0.93 · `␣ద` 4.1e-3✱ · `క` 0.83 · `్రమ` 1.2e-5✱ · `ాని` 0.93 · `␣ని` 0.98 · `ర` 0.99 · `వ` 5.3e-3✱ · `స` 0.09✱ · `్ర` 2.3e-6✱ · `త` 1.00 · `ను` 1.00 · `ండ` 3.9e-5✱ · `ట` 1.00 · `కి` 0.98 · `ల్ల` 4.1e-5✱ · `ె` 0.93 · `తి` 0.80 · `శ` 9.3e-4✱ · `్ర` 2.6e-5✱ · `మ` 0.90 · `ౌ` 0.01✱ · `⏎` 0.08✱ forced |
| 3 | `ర` 0.88 · `మ` 0.04✱ · `్రి` 0.02✱ · `␣జ` 0.99 · `య` 0.98 · `మ` 2.2e-3✱ · `్య` 2.5e-5✱ · `డ` 0.97 · `డ` 7.7e-5✱ · `్య` 4.7e-4✱ · `ళ` 8.9e-3✱ · `ె` 0.43 · `␣స` 1.6e-3✱ · `␣క్ష` 7.8e-5✱ · `్రమ` 4.0e-6✱ · `్రమ` 7.4e-5✱ · `␣లేదు` 0.01✱ · `␣ప` 0.90 · `␣ఉన్న` 4.1e-5✱ · `␣ఇచ్చిన` 0.58 · `ప` 9.4e-5✱ · `్` 1.1e-9✱ · `⏎` 5.1e-6✱ forced |
| 4 | `ద` 0.22 · `మ` 3.0e-4✱ · `్రి` 4.4e-5✱ · `␣ఉ` 7.5e-3✱ · `␣ఉత్ప` 0.56 · `ల` 0.98 · `ాల` 4.2e-4✱ · `␣అను` 1.00 · `␣వ` 9.3e-4✱ · `్ర` 1.2e-7✱ · `్వ` 3.4e-5✱ · `్` 1.4e-5✱ · `దయ` 5.9e-5✱ · `్రు` 1.7e-6✱ · `␣ఇ` 0.42 · `డ` 1.00 · `న్` 0.95 · `ము` 0.02✱ · `␣` 2.2e-8✱ · `ఉ` 5.6e-3✱ · `ఉ` 0.86 · `త్ప` 0.92 · `ల` 0.81 · `ాల` 4.2e-3✱ · `ము` 0.04✱ · `భ` 0.01✱ · `్` 1.2e-6✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 130 tokens · 34.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాము ల శక్రివే శ మత శ్ర్ర్మల్రియ లక్రి లయన్రిరామమా | `UIIUIUIIIUIIUIIUIUIU` |
| 2 | జై మత జల్రి శ్రియ్రి శ మసన్ లక లయ్యన లత్రి లన్జసీ | `UIIUIUIIIUIIUIIUIUIU` |
| 3 | తై మత శ్రియ్రి శల్య ల ల ల్య్య్తయ్య యతిమ్యత మత్యలల్రి శ్రీ | `UIIUIUIIIUIIUIIUIUIU` |
| 4 | మ్యే మత లక్రియయ్య ల ల ల్య్య్యీ ల ల్య్య్య ల్య్య్యల్య్య్య లయయ్య రణ్య భం | `UIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 15% · single-akshara words 38% · repeated lines 0 · mean token probability (geometric) 0.026 · model's first choice kept 23% · constraint overrode 65% · backtracks 0

<details><summary>Token probabilities (130 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.01 · `ము` 0.08 · `␣ల` 0.04 · `␣శ` 0.02 · `క` 0.03 · `్రి` 0.07✱ · `వే` 0.02 · `␣శ` 0.13 · `␣మ` 0.03 · `త` 0.02 · `␣శ` 0.02✱ · `్ర` 0.01✱ · `్ర` 8.5e-4✱ · `్` 4.8e-5✱ · `మ` 0.06✱ · `ల` 0.17✱ · `్రియ` 5.6e-5✱ · `␣ల` 0.12✱ · `క` 0.13✱ · `్రి` 1.7e-3✱ · `␣ల` 0.05✱ · `య` 0.04✱ · `న` 4.3e-3✱ · `్రి` 6.1e-5✱ · `రా` 0.47 · `మ` 0.54 · `మా` 4.5e-3✱ · `⏎` 0.63 |
| 2 | `జ` 0.04 · `ై` 0.04✱ · `␣మ` 0.04✱ · `త` 0.05 · `␣జ` 0.15 · `ల` 0.03✱ · `్రి` 3.7e-4✱ · `␣శ` 0.07 · `్రి` 0.15 · `య` 0.05✱ · `్రి` 3.0e-4✱ · `␣శ` 0.09 · `␣మ` 0.08 · `స` 0.02✱ · `న్` 0.02✱ · `␣ల` 0.66 · `క` 0.49 · `␣ల` 0.02✱ · `య` 0.02✱ · `్య` 2.5e-3✱ · `న` 0.59 · `␣ల` 0.23✱ · `త` 6.2e-3✱ · `్రి` 1.6e-3✱ · `␣ల` 0.07✱ · `న్` 0.01✱ · `జ` 0.10✱ · `సీ` 0.01✱ · `⏎` 0.07 forced |
| 3 | `త` 0.83 · `ై` 8.1e-3✱ · `␣మ` 7.4e-3✱ · `త` 0.66 · `␣శ` 0.76 · `్రి` 0.64 · `య` 0.76 · `్రి` 0.17✱ · `␣శ` 0.79 · `ల` 8.3e-4✱ · `్య` 5.5e-5✱ · `␣ల` 0.09✱ · `␣ల` 0.56 · `␣ల` 0.20✱ · `్య` 0.06✱ · `్య` 0.07✱ · `్` 4.2e-4✱ · `త` 5.0e-3✱ · `య` 0.11✱ · `్య` 1.5e-3✱ · `␣య` 0.80 · `తి` 0.93 · `మ` 1.1e-3✱ · `్య` 1.7e-4✱ · `త` 0.05✱ · `␣మ` 0.67 · `త` 0.64 · `్య` 1.8e-4✱ · `ల` 0.77 · `ల` 6.5e-3✱ · `్రి` 6.6e-3✱ · `␣శ్రీ` 0.03✱ · `⏎` 0.02 forced |
| 4 | `మ` 0.04✱ · `్య` 2.2e-3✱ · `ే` 3.4e-4✱ · `␣మ` 1.2e-3✱ · `త` 0.02✱ · `␣ల` 0.79 · `క` 0.75 · `్రి` 6.5e-4✱ · `య` 0.58 · `య` 0.06✱ · `్య` 0.05✱ · `␣ల` 0.31 · `␣ల` 0.16✱ · `␣ల` 5.5e-3✱ · `్య` 5.3e-3✱ · `్య` 7.5e-3✱ · `్య` 1.1e-3✱ · `ీ` 3.2e-5✱ · `␣ల` 7.5e-3✱ · `␣ల` 0.03✱ · `్య` 0.05✱ · `్య` 0.02✱ · `్య` 0.04✱ · `␣ల` 8.6e-3✱ · `్య` 0.04✱ · `్య` 0.06✱ · `్య` 0.04✱ · `ల` 0.02✱ · `్య` 8.3e-3✱ · `్య` 0.15 · `్య` 0.16 · `␣ల` 0.10✱ · `య` 0.08 · `య` 0.04✱ · `్య` 8.8e-3✱ · `␣ర` 0.67 · `ణ` 9.2e-3✱ · `్య` 3.9e-3✱ · `␣భ` 0.93 · `ం` 7.4e-4✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 121 tokens · 34.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాతిల సక్రి శత్రువు ల ల్రమ్రమనుస్రహమత్రియమ్య సీ | `UIIUIUIIIUIIUIIUIUIU` |
| 2 | తా తన నడ్రనున్ జమ జ జ్య్య్తత్రియ నడ్యడు శ్రీరమయ్యమున్ | `UIIUIUIIIUIIUIIUIUIU` |
| 3 | మౌ తడెనై న్తనే న్న్రచను ల్ల్య్నవ్యరపుప్రమమాల లేదు భర్ | `UIIUIUIIIUIIUIIUIUIU` |
| 4 | భ్ర్ర్రౌతితితియ్యమవ్య్యయవవవ్రలలల్య ర నల్ర్ర వల్య లౌ | `UIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 31% · repeated lines 0 · mean token probability (geometric) 0.011 · model's first choice kept 20% · constraint overrode 71% · backtracks 0

<details><summary>Token probabilities (121 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.29 · `తి` 0.02 · `ల` 0.04 · `␣స` 0.02 · `క` 0.05✱ · `్రి` 5.5e-3✱ · `␣శ` 0.03 · `త్ర` 0.30 · `ు` 0.96 · `వు` 0.09 · `␣ల` 0.34 · `␣ల` 0.35 · `్రమ` 9.7e-5✱ · `్రమ` 1.8e-4✱ · `ను` 0.08✱ · `స` 9.8e-5✱ · `్రహ` 2.2e-6✱ · `మ` 0.59 · `త` 0.08 · `్రియ` 6.3e-5✱ · `మ` 0.02✱ · `్య` 5.8e-4✱ · `␣సీ` 0.11 · `⏎` 0.05 forced |
| 2 | `తా` 0.08 · `␣తన` 1.5e-3✱ · `␣న` 0.04 · `డ` 0.91 · `్ర` 3.7e-4✱ · `ను` 0.03✱ · `న్` 0.02✱ · `␣జ` 9.6e-3✱ · `మ` 0.71 · `␣జ` 0.68 · `␣జ` 0.01✱ · `్య` 5.6e-4✱ · `్య` 3.2e-3✱ · `్` 4.8e-7✱ · `త` 1.7e-3✱ · `త` 0.69 · `్రియ` 3.6e-5✱ · `␣న` 0.93 · `డ` 0.99 · `్య` 5.2e-5✱ · `డు` 3.1e-3✱ · `␣శ్రీ` 0.97 · `ర` 2.8e-3✱ · `మ` 0.96 · `య` 1.5e-3✱ · `్య` 6.8e-3✱ · `ము` 0.51 · `న్` 1.3e-3✱ · `⏎` 1.3e-3✱ forced |
| 3 | `మ` 0.90 · `ౌ` 3.1e-4✱ · `␣` 3.7e-5✱ · `త` 1.1e-3✱ · `డ` 0.98 · `ె` 0.97 · `న` 4.1e-3✱ · `ై` 6.7e-4✱ · `␣` 1.3e-3✱ · `న్` 1.9e-3✱ · `త` 2.8e-4✱ · `నే` 1.3e-3✱ · `␣` 7.8e-3✱ · `న్న` 9.4e-3✱ · `్ర` 6.3e-4✱ · `చ` 7.0e-3✱ · `ను` 0.02✱ · `␣` 0.04✱ · `ల్ల` 0.01✱ · `్య` 2.4e-4✱ · `్` 3.5e-6✱ · `న` 4.0e-3✱ · `వ` 2.7e-3✱ · `్య` 1.2e-3✱ · `ర` 0.02✱ · `పు` 0.06✱ · `ప` 0.04 · `్రమ` 1.6e-3✱ · `మాల` 0.59 · `␣లేదు` 8.2e-3✱ · `␣` 7.4e-3✱ · `భ` 0.16✱ · `ర` 0.28✱ · `్` 8.8e-7✱ · `⏎` 2.6e-3✱ forced |
| 4 | `␣భ` 0.19 · `్ర` 0.01✱ · `్ర` 9.2e-4✱ · `్ర` 7.7e-3✱ · `ౌ` 4.8e-4✱ · `తి` 5.0e-3✱ · `తి` 0.03✱ · `తి` 0.04✱ · `య` 0.04✱ · `్య` 7.8e-3✱ · `మ` 4.9e-3✱ · `వ` 9.3e-3✱ · `్య` 0.01✱ · `్య` 0.03✱ · `య` 0.03✱ · `వ` 7.5e-3✱ · `వ` 0.03✱ · `వ` 0.04✱ · `్ర` 2.8e-3✱ · `ల` 6.4e-3✱ · `ల` 0.07✱ · `ల` 0.08✱ · `్య` 1.4e-3✱ · `␣ర` 0.49 · `␣న` 0.33 · `ల` 0.01✱ · `్ర` 3.9e-3✱ · `్ర` 0.11 · `␣వ` 0.74 · `ల` 0.05✱ · `్య` 0.01✱ · `␣ల` 0.02✱ · `ౌ` 8.9e-4✱ |

</details>

[↑ meters](#meters)

---

<a id="champakamala"></a>

## 2. చంపకమాల (champakamala)

```text
Meter: చంపకమాల (champakamala), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: న జ భ జ జ జ ర, i.e. III IUI UII IUI IUI IUI UIU (21 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 11th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter చంపకమాల (champakamala).

Meter: చంపకమాల (champakamala), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: న జ భ జ జ జ ర, i.e. III IUI UII IUI IUI IUI UIU (21 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 11th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 109 tokens · 31.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నిమమ ని నిమ్వరించమ మ మ్ర్మ్నృత్రు లలిల్రినినిమ్రమమ్రమల్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 2 | ము మక మతిమ్రమద్రు మ లమొన్రతి ప్రేమము లోక నీతి మమ్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 3 | మమ మమమమ్రతిమ్రు లక మమ్యతి ఏమిటి లేదు లేదుకో | `IIIIUIUIIIUIIUIIUIUIU` |
| 4 | మమలము వన్య మమ్మక మమమ్య జ భక్రమ జర్రమమ్య మమ్ | `IIIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 23% · repeated lines 0 · mean token probability (geometric) 0.020 · model's first choice kept 37% · constraint overrode 55% · backtracks 0

<details><summary>Token probabilities (109 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ని` 0.03 · `మ` 0.09 · `మ` 0.05 · `␣ని` 0.13 · `␣ని` 0.13 · `మ` 0.15 · `్వర` 1.3e-4✱ · `ించ` 2.3e-3✱ · `మ` 0.12 · `␣మ` 0.33 · `␣మ` 0.11 · `్ర` 4.0e-3✱ · `్` 4.8e-5✱ · `మ` 0.21 · `్` 7.6e-7✱ · `న` 0.04✱ · `ృత` 3.0e-4✱ · `్రు` 3.0e-4✱ · `␣ల` 6.3e-3 · `లి` 0.04 · `ల` 0.01✱ · `్రి` 7.9e-6✱ · `ని` 0.29✱ · `ని` 0.32 · `మ` 0.60 · `్ర` 1.0e-4✱ · `మ` 0.50 · `మ` 0.23 · `్రమ` 3.4e-5✱ · `ల` 0.05✱ · `్` 6.2e-10✱ · `⏎` 1.5e-3✱ forced |
| 2 | `ము` 0.75 · `␣మ` 1.2e-5✱ · `క` 0.83 · `␣మ` 7.1e-3✱ · `తి` 0.91 · `మ` 9.0e-3✱ · `్ర` 6.5e-4✱ · `మ` 0.31 · `ద` 0.86 · `్రు` 1.8e-4✱ · `␣మ` 0.06 · `␣ల` 0.14 · `మ` 0.30 · `ొ` 5.6e-3✱ · `న` 0.15 · `్ర` 7.7e-4✱ · `తి` 0.53 · `␣ప్రేమ` 0.98 · `ము` 0.98 · `␣లో` 1.00 · `క` 0.99 · `␣నీ` 0.96 · `తి` 0.85 · `␣మ` 5.8e-3✱ · `మ` 0.03✱ · `్` 4.8e-6✱ · `⏎` 0.02✱ forced |
| 3 | `మ` 0.84 · `మ` 0.30✱ · `␣మ` 0.18 · `మ` 0.81 · `మ` 0.42 · `మ` 0.41 · `్ర` 4.7e-3✱ · `తి` 0.65 · `మ` 0.05✱ · `్రు` 1.3e-3✱ · `␣ల` 0.01✱ · `క` 0.68 · `␣మ` 0.03✱ · `మ` 0.16✱ · `్య` 5.4e-4✱ · `తి` 0.83 · `␣ఏమి` 7.6e-4✱ · `టి` 7.3e-3✱ · `␣లేదు` 8.5e-3✱ · `␣లేదు` 0.02✱ · `క` 2.9e-3✱ · `ో` 1.7e-3✱ · `⏎` 0.03✱ forced |
| 4 | `మ` 0.01✱ · `మ` 0.21 · `ల` 0.03✱ · `ము` 0.29 · `␣వ` 9.7e-3✱ · `న` 1.1e-3✱ · `్య` 1.1e-4✱ · `␣మ` 0.02✱ · `మ్మ` 0.03✱ · `క` 0.41 · `␣మ` 0.07 · `మ` 0.10✱ · `మ` 0.05✱ · `్య` 2.2e-3✱ · `␣జ` 0.57 · `␣భ` 0.86 · `క` 2.5e-4✱ · `్రమ` 6.5e-4✱ · `␣జ` 0.59 · `ర` 0.02✱ · `్ర` 5.8e-4✱ · `మ` 0.14 · `మ` 0.10✱ · `్య` 4.1e-3✱ · `␣మ` 0.13 · `మ` 0.10✱ · `్` 3.8e-4✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 133 tokens · 30.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మమమ సిమర్రి సామ స మ మల్ర లముక్రి లకుట్యమయ్యమర్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 2 | మ మల మలల్రముక్రి లకు మమ్యయ సిమ్రి సి సామ మమ్యలల్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 3 | క్రిమయున మమ్య సిమ్ర్రిమమ స్లెల్రు లముక్రి లకుక్య్య్య ట్టిట్టి ట్టిచ్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 4 | వ మ ల ల లల్య లక్రి లకు ల్య్య్వవ్య లకుమ్యరజజ్రజజ్య్య్య ల్య్య్యల్ | `IIIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 29% · repeated lines 0 · mean token probability (geometric) 0.029 · model's first choice kept 37% · constraint overrode 56% · backtracks 0

<details><summary>Token probabilities (133 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.61 · `మ` 0.15 · `మ` 0.06 · `␣సి` 3.3e-3 · `మ` 0.05 · `ర` 0.35 · `్రి` 2.8e-5✱ · `␣సా` 6.5e-3 · `మ` 0.13 · `␣స` 0.03 · `␣మ` 0.05 · `␣మ` 0.02✱ · `ల` 0.05✱ · `్ర` 2.2e-3✱ · `␣ల` 0.32 · `ము` 0.06 · `క` 0.07✱ · `్రి` 6.4e-4✱ · `␣ల` 0.52 · `కు` 0.02 · `ట` 1.4e-4✱ · `్య` 2.5e-4✱ · `మ` 0.89 · `య` 0.04 · `్య` 1.0e-4✱ · `మ` 0.87 · `ర` 0.81 · `్` 1.2e-5✱ · `⏎` 1.8e-4✱ forced |
| 2 | `మ` 0.83 · `␣మ` 0.05✱ · `ల` 0.08 · `␣మ` 0.78 · `ల` 0.91 · `ల` 0.05✱ · `్ర` 3.2e-4✱ · `ము` 0.71 · `క` 0.86 · `్రి` 0.48 · `␣ల` 0.73 · `కు` 0.33 · `␣మ` 0.04✱ · `మ` 0.91 · `్య` 2.0e-3✱ · `య` 0.79 · `␣సి` 0.41 · `మ` 0.59 · `్రి` 3.5e-3✱ · `␣సి` 0.04✱ · `␣సా` 0.83 · `మ` 0.86 · `␣మ` 0.44 · `మ` 0.52 · `్య` 1.0e-3✱ · `ల` 0.68 · `ల` 0.06✱ · `్` 6.6e-5✱ · `⏎` 0.48 |
| 3 | `క` 0.71 · `్రి` 0.33 · `మ` 0.01✱ · `యు` 0.06 · `న` 0.09✱ · `␣మ` 0.82 · `మ` 0.96 · `్య` 0.02✱ · `␣సి` 0.99 · `మ` 0.99 · `్ర` 8.5e-5✱ · `్రి` 0.58 · `మ` 4.8e-4✱ · `మ` 0.92 · `␣స` 0.74 · `్` 2.3e-6✱ · `ల` 0.05✱ · `ెల` 3.9e-3✱ · `్రు` 3.7e-4✱ · `␣ల` 0.96 · `ము` 0.97 · `క` 0.99 · `్రి` 0.98 · `␣ల` 0.98 · `కు` 0.91 · `క` 1.9e-4✱ · `్య` 8.0e-5✱ · `్య` 3.8e-3✱ · `్య` 3.3e-3✱ · `␣` 7.1e-5✱ · `ట్టి` 7.8e-4✱ · `ట్టి` 5.2e-3✱ · `␣` 1.2e-3✱ · `ట్టి` 1.4e-3✱ · `చ` 3.3e-4✱ · `్` 8.9e-4✱ · `⏎` 0.34 |
| 4 | `వ` 8.5e-3✱ · `␣మ` 5.3e-3✱ · `␣ల` 0.03✱ · `␣ల` 0.05✱ · `␣ల` 0.06✱ · `ల` 8.9e-3✱ · `్య` 1.5e-3✱ · `␣ల` 0.03✱ · `క` 0.08✱ · `్రి` 0.03✱ · `␣ల` 0.12✱ · `కు` 0.47 · `␣ల` 0.01✱ · `్య` 0.01✱ · `్య` 0.08✱ · `్` 1.6e-3✱ · `వ` 5.0e-3✱ · `వ` 0.03✱ · `్య` 0.01✱ · `␣ల` 0.02✱ · `కు` 0.17✱ · `మ` 4.7e-3✱ · `్య` 7.2e-3✱ · `ర` 0.01✱ · `జ` 0.97 · `జ` 0.03✱ · `్ర` 3.0e-3✱ · `జ` 0.92 · `జ` 0.78 · `్య` 8.8e-5✱ · `్య` 5.8e-3✱ · `్య` 0.01✱ · `␣ల` 7.7e-4✱ · `్య` 7.3e-3✱ · `్య` 0.08✱ · `్య` 0.05✱ · `ల` 8.5e-3✱ · `్` 2.7e-3✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 117 tokens · 52.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమలగుశల్య నిశ్రశక మ్ర్న్గల్యితముమ్వర వేల్లడగ్రిచజ్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 2 | జముమము కాకనల్యముగ జగ్వర లోకమమందు లోనముక్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 3 | లమశలలయ్యతన్ మతి మ మ్య్య్లమ్రు మమమ్రతిముమ్యవవ్రి మువ్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 4 | నమ లతి లేదు లేదు మ మ మ్య్యమ్య మ మవ్రు మమమ్య మాలుముశ్ | `IIIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 19% · repeated lines 0 · mean token probability (geometric) 0.016 · model's first choice kept 33% · constraint overrode 59% · backtracks 30

<details><summary>Token probabilities (117 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.98 · `మ` 0.91 · `ల` 0.96 · `గు` 0.46 · `శ` 0.48 · `ల` 0.83 · `్య` 0.88 · `␣ని` 0.85 · `శ` 0.95 · `్ర` 0.81 · `శ` 0.12 · `క` 0.21 · `␣మ` 0.86 · `్ర` 4.2e-5✱ · `్` 3.6e-5✱ · `న` 0.80 · `్` 7.1e-6✱ · `గ` 7.6e-3✱ · `ల` 0.09 · `్య` 1.4e-4✱ · `ిత` 0.94 · `ము` 0.01 · `మ` 0.64 · `్వర` 0.33 · `␣వే` 0.89 · `ల్ల` 0.02 · `డ` 0.99 · `గ` 0.95 · `్రి` 8.8e-6✱ · `చ` 1.9e-4✱ · `జ` 0.19✱ · `్` 1.7e-7✱ · `⏎` 0.02✱ |
| 2 | `జ` 0.23 · `ము` 6.3e-3✱ · `మ` 0.03 · `ము` 0.01 · `␣కా` 2.6e-3 · `క` 0.40 · `న` 0.04 · `ల` 0.02✱ · `్య` 2.4e-3✱ · `ము` 0.16 · `గ` 0.23 · `␣జగ` 0.98 · `్వర` 2.5e-5✱ · `␣లో` 0.98 · `క` 0.99 · `మ` 0.54 · `మ` 0.12✱ · `ందు` 0.02✱ · `␣లో` 0.03✱ · `న` 0.16 · `ము` 0.44 · `క` 0.01✱ · `్` 4.0e-6✱ · `⏎` 1.8e-3✱ forced |
| 3 | `ల` 0.71 · `మ` 9.6e-5✱ · `శ` 0.97 · `ల` 0.96 · `ల` 0.03✱ · `య` 0.08✱ · `్య` 8.0e-4✱ · `త` 0.96 · `న్` 0.01✱ · `␣మ` 0.91 · `తి` 0.59 · `␣మ` 0.03✱ · `␣మ` 0.09✱ · `్య` 1.1e-4✱ · `్య` 1.2e-4✱ · `్` 4.0e-7✱ · `ల` 0.03✱ · `మ` 0.03✱ · `్రు` 2.6e-3✱ · `␣మ` 0.72 · `మ` 0.68 · `మ` 3.5e-3✱ · `్ర` 6.6e-5✱ · `తి` 3.1e-4✱ · `ము` 7.8e-4✱ · `మ` 7.3e-3✱ · `్య` 9.7e-4✱ · `వ` 4.5e-3✱ · `వ` 9.2e-3✱ · `్రి` 2.0e-5✱ · `␣ము` 2.9e-5✱ · `వ` 4.4e-4✱ · `్` 4.9e-4✱ · `⏎` 0.15✱ forced |
| 4 | `న` 2.5e-3✱ · `మ` 5.5e-4✱ · `␣ల` 0.02✱ · `తి` 1.2e-3✱ · `␣లేదు` 0.01✱ · `␣లేదు` 0.05✱ · `␣మ` 0.04✱ · `␣మ` 0.01✱ · `␣మ` 9.5e-3✱ · `్య` 3.1e-5✱ · `్య` 0.04✱ · `మ` 0.04✱ · `్య` 0.02✱ · `␣మ` 0.32 · `␣మ` 0.19 · `వ` 0.21 · `్రు` 4.5e-4✱ · `␣మ` 0.12✱ · `మ` 0.11✱ · `మ` 0.04✱ · `్య` 7.8e-3✱ · `␣మ` 0.11✱ · `ాలు` 0.03✱ · `ము` 0.13✱ · `శ` 1.1e-5✱ · `్` 1.0e-4✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 127 tokens · 53.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మణిలల శిఖ్రి జాన జ సుమల్యము లన్కకు చేటరిన్న్మణిగ్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 2 | ఖ్రి ణణ సముద్ర మధ్రి పటినృష్మణిగల్రిఖి జాన జుంతుతుడ్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 3 | ల్లెణను మణిగ్రి శిఖ్రి జను జ్ర్ర్లీయము చూడెను డుత్యకున్యతియ్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 4 | వణ ల లతివ్రి ణిజ్రి మణి మ్వర్రమమున్రుననన్ననన్ననమ్ | `IIIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.026 · model's first choice kept 50% · constraint overrode 46% · backtracks 30

<details><summary>Token probabilities (127 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.96 · `ణి` 0.96 · `ల` 0.33 · `ల` 0.04 · `␣శి` 0.07 · `ఖ` 0.65 · `్రి` 0.97 · `␣జ` 0.87 · `ాన` 0.97 · `␣జ` 0.92 · `␣సు` 0.96 · `మ` 0.84 · `ల` 0.88 · `్య` 0.92 · `ము` 0.37 · `␣ల` 0.88 · `న్` 0.52 · `క` 0.95 · `కు` 0.43 · `␣చే` 0.99 · `ట` 0.95 · `రి` 1.00 · `న్` 0.92 · `న్` 2.5e-4✱ · `మ` 0.99 · `ణి` 0.99 · `గ` 0.93 · `్` 7.2e-10✱ · `⏎` 3.8e-5✱ forced |
| 2 | `ఖ` 1.00 · `్రి` 0.93 · `␣` 1.0e-4✱ · `ణ` 2.3e-3✱ · `ణ` 0.05 · `␣స` 0.96 · `ము` 0.94 · `ద్ర` 0.98 · `␣మ` 0.92 · `ధ` 0.72 · `్రి` 0.93 · `␣ప` 0.79 · `టి` 0.94 · `న` 0.95 · `ృష్` 2.8e-8✱ · `మ` 0.55 · `ణి` 0.83 · `గ` 0.57 · `ల` 0.69 · `్రి` 2.4e-3✱ · `ఖ` 0.68 · `ి` 0.04✱ · `␣జ` 0.75 · `ాన` 0.84 · `␣జ` 0.57 · `ు` 7.7e-4✱ · `ం` 1.6e-3✱ · `తు` 0.17 · `తు` 0.61 · `డ` 0.99 · `్` 1.5e-9✱ · `⏎` 1.0e-4✱ forced |
| 3 | `ల్ల` 0.94 · `ె` 0.87 · `ణ` 1.6e-3✱ · `ను` 0.85 · `␣మ` 0.97 · `ణి` 0.98 · `గ` 0.94 · `్రి` 3.0e-4✱ · `␣శి` 1.00 · `ఖ` 1.00 · `్రి` 0.98 · `␣జ` 1.00 · `ను` 8.3e-5✱ · `␣జ` 0.99 · `్ర` 8.2e-6✱ · `్ర` 4.5e-6✱ · `్` 1.1e-6✱ · `ల` 0.03✱ · `ీయ` 5.1e-7✱ · `ము` 0.99 · `␣చూ` 0.99 · `డ` 0.99 · `ె` 1.00 · `ను` 0.98 · `␣` 1.7e-5✱ · `డు` 2.0e-4✱ · `త` 1.8e-4✱ · `్య` 1.0e-4✱ · `కు` 6.6e-3✱ · `న` 9.5e-4✱ · `్య` 1.6e-4✱ · `తి` 1.7e-3✱ · `య` 4.1e-4✱ · `్` 1.8e-5✱ · `⏎` 0.10✱ forced |
| 4 | `వ` 1.5e-3✱ · `ణ` 2.2e-3✱ · `␣ల` 6.0e-4✱ · `␣ల` 0.04✱ · `తి` 3.7e-3✱ · `వ` 8.9e-4✱ · `్రి` 4.5e-4✱ · `␣` 0.31 · `ణి` 0.04✱ · `జ` 0.09✱ · `్రి` 5.2e-3✱ · `␣మ` 0.11 · `ణి` 0.47 · `␣మ` 0.02✱ · `్వర` 9.4e-5✱ · `్రమ` 2.6e-4✱ · `ము` 0.49 · `న` 7.8e-3✱ · `్రు` 3.7e-6✱ · `న` 5.0e-4✱ · `న` 2.3e-3✱ · `న` 0.02✱ · `్` 4.4e-4✱ · `న` 0.01✱ · `న` 0.02✱ · `న` 0.02✱ · `్` 3.2e-4✱ · `న` 0.02✱ · `న` 0.21✱ · `మ` 0.03✱ · `్` 6.8e-5✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 135 tokens · 32.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మణిత శృతత్రి శ్రియ్వర మృమల్యమునమ్వర లమ్యముక్రిమమ్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 2 | మణిమ మముద్రమున్న్టి మల ల్య్య్మమ్యమమన్మమణిత్యుకట్య చూ | `IIIIUIUIIIUIIUIIUIUIU` |
| 3 | లొణిమమనుమ్యనుమ్యమనులొమ్య హనుంజతు వేడు లక్యనున్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 4 | జ్యుణమమమమ్య్య్య నాకు ప్రుని ల్య్య్యుమ్యమమమ్య్యు ల్య్య మమ్రుణిమ్య శృత్ | `IIIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 14% · repeated lines 0 · mean token probability (geometric) 0.017 · model's first choice kept 34% · constraint overrode 59% · backtracks 0

<details><summary>Token probabilities (135 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.52 · `ణి` 0.14✱ · `త` 0.13 · `␣శ` 0.04 · `ృ` 6.5e-3✱ · `త` 0.02✱ · `త` 0.01✱ · `్రి` 3.6e-3✱ · `␣శ` 0.04 · `్రి` 0.01 · `య` 0.15 · `్వర` 1.1e-4✱ · `␣మ` 0.42 · `ృ` 0.02✱ · `మ` 0.02✱ · `ల` 0.06 · `్య` 3.4e-4✱ · `ము` 0.14 · `న` 0.03✱ · `మ` 0.02✱ · `్వర` 1.4e-4✱ · `␣ల` 1.0e-2✱ · `మ` 0.30 · `్య` 0.01✱ · `ము` 0.10✱ · `క` 0.04 · `్రి` 9.9e-4✱ · `మ` 0.18✱ · `మ` 0.34 · `్` 5.8e-6✱ · `⏎` 0.51 |
| 2 | `మ` 0.76 · `ణి` 0.06✱ · `మ` 0.51 · `␣మ` 0.10 · `ము` 0.18 · `ద్ర` 0.77 · `ము` 0.30 · `న్` 0.04✱ · `న్` 0.02✱ · `టి` 0.64 · `␣మ` 0.48 · `ల` 0.04 · `␣ల` 0.06 · `్య` 1.8e-3✱ · `్య` 8.7e-3✱ · `్` 3.1e-7✱ · `మ` 0.14 · `మ` 0.22 · `్య` 3.0e-3✱ · `మ` 0.53 · `మ` 0.86 · `న్` 0.93 · `మ` 0.01✱ · `మ` 0.97 · `ణి` 0.96 · `త` 0.92 · `్య` 5.0e-5✱ · `ు` 4.8e-4✱ · `క` 0.90 · `ట` 2.5e-4✱ · `్య` 3.3e-4✱ · `␣చూ` 0.01 · `⏎` 9.8e-3✱ forced |
| 3 | `ల` 0.19 · `ొ` 1.0e-3✱ · `ణి` 2.7e-3✱ · `మ` 0.47 · `మ` 0.72 · `ను` 0.38 · `మ` 0.30 · `్య` 1.4e-3✱ · `ను` 0.67 · `మ` 0.49 · `్య` 1.6e-3✱ · `మ` 0.87 · `ను` 0.01✱ · `ల` 0.02✱ · `ొ` 1.8e-4✱ · `మ` 1.9e-3✱ · `్య` 3.1e-5✱ · `␣హ` 0.99 · `ను` 0.97 · `ంజ` 1.1e-4✱ · `తు` 0.96 · `␣వే` 1.00 · `డు` 0.94 · `␣ల` 0.91 · `క` 0.02✱ · `్య` 9.9e-5✱ · `ను` 0.90 · `న్` 3.9e-3✱ · `⏎` 8.0e-4✱ forced |
| 4 | `␣జ` 0.32 · `్య` 0.01✱ · `ు` 6.1e-3✱ · `ణ` 3.5e-4✱ · `మ` 0.74 · `మ` 0.82 · `మ` 1.8e-3✱ · `మ` 3.7e-3✱ · `్య` 1.4e-4✱ · `్య` 6.8e-4✱ · `్య` 4.6e-4✱ · `␣నాకు` 1.2e-4✱ · `␣ప్ర` 2.9e-3✱ · `ు` 4.7e-3✱ · `ని` 8.7e-3✱ · `␣ల` 5.2e-3✱ · `్య` 5.0e-5✱ · `్య` 2.4e-3✱ · `్య` 3.1e-3✱ · `ు` 2.2e-4✱ · `మ` 9.7e-3✱ · `్య` 0.04✱ · `మ` 0.03✱ · `మ` 0.10✱ · `మ` 5.9e-3✱ · `్య` 4.7e-4✱ · `్య` 0.01✱ · `ు` 0.02✱ · `␣ల` 1.8e-3✱ · `్య` 9.8e-3✱ · `్య` 2.8e-3✱ · `␣` 9.8e-3✱ · `మ` 0.02✱ · `మ` 9.2e-3✱ · `్రు` 8.6e-7✱ · `ణి` 0.86 · `మ` 4.8e-3✱ · `్య` 3.2e-5✱ · `␣శ` 0.98 · `ృ` 0.93 · `త` 0.93 · `్` 4.1e-6✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 124 tokens · 33.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమల శమల్రి శత్రి సము ద్ర్ర్గమ్య హనుమ్రుతి మక్రిలమ్రి హం | `IIIIUIUIIIUIIUIIUIUIU` |
| 2 | మము లకనున్న్రునుక్రిల శమల్రి శతమ్రిముదద్ర్గమల్య హన్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 3 | మమకతితిన్రిచద్రిముతిమత్మలకక్రిల లం లకుల్రుతిం | `IIIIUIUIIIUIIUIIUIUIU` |
| 4 | తిమ కమలల్రిలల్రితమ మ్ర్ర్దిత్రి గగమ్య హ హమ్రుతిక్రిలం | `IIIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.033 · model's first choice kept 35% · constraint overrode 57% · backtracks 0

<details><summary>Token probabilities (124 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.04 · `మ` 0.42 · `ల` 0.44 · `␣శ` 0.02 · `మ` 0.02✱ · `ల` 0.20 · `్రి` 1.6e-4✱ · `␣శ` 0.05 · `త` 0.06 · `్రి` 2.5e-3✱ · `␣స` 0.11 · `ము` 0.84 · `␣ద` 9.7e-4✱ · `్ర` 0.16 · `్ర` 1.5e-4✱ · `్` 5.8e-7✱ · `గ` 0.18 · `మ` 0.07✱ · `్య` 5.0e-4✱ · `␣హ` 0.30 · `ను` 0.37 · `మ` 0.39✱ · `్రు` 2.0e-4✱ · `తి` 0.87 · `␣మ` 6.3e-4✱ · `క` 0.33 · `్రి` 1.4e-3✱ · `ల` 0.59 · `మ` 0.01✱ · `్రి` 2.1e-3✱ · `␣హ` 0.61 · `ం` 3.1e-3✱ · `⏎` 0.03 forced |
| 2 | `మ` 0.22 · `ము` 2.9e-3✱ · `␣ల` 0.76 · `క` 0.61 · `ను` 0.71 · `న్` 0.02✱ · `న్` 0.30✱ · `రు` 0.15✱ · `ను` 0.77 · `క` 0.02✱ · `్రి` 6.8e-5✱ · `ల` 0.98 · `␣శ` 0.90 · `మ` 0.98 · `ల` 0.98 · `్రి` 0.96 · `␣శ` 0.99 · `త` 0.99 · `మ` 8.2e-4✱ · `్రి` 0.01✱ · `ము` 0.91 · `ద` 0.02✱ · `ద` 0.02✱ · `్ర` 0.99 · `్` 0.93 · `గ` 0.99 · `మ` 0.98 · `ల్య` 9.6e-4✱ · `␣హ` 0.96 · `న్` 4.1e-3✱ · `⏎` 1.4e-3✱ forced |
| 3 | `మ` 4.6e-3✱ · `మ` 1.2e-3✱ · `క` 2.6e-3✱ · `తి` 4.7e-3✱ · `తి` 0.01✱ · `న` 2.3e-3✱ · `్రి` 2.1e-4✱ · `చ` 0.03✱ · `ద` 0.01✱ · `్రి` 5.0e-3✱ · `ము` 0.03✱ · `తి` 5.4e-3✱ · `మ` 5.5e-3✱ · `త్మ` 4.9e-3✱ · `ల` 4.7e-3✱ · `క` 0.02✱ · `క` 0.05✱ · `్రి` 0.01✱ · `ల` 0.07✱ · `␣ల` 2.4e-3✱ · `ం` 0.01✱ · `␣ల` 0.06✱ · `కు` 0.10 · `ల` 0.04✱ · `్రు` 4.0e-4✱ · `తి` 0.14 · `ం` 1.2e-3✱ · `⏎` 0.02✱ forced |
| 4 | `తి` 0.54 · `మ` 0.10✱ · `␣క` 0.24 · `మ` 0.74 · `ల` 0.71 · `ల` 0.02✱ · `్రి` 5.2e-5✱ · `ల` 0.94 · `ల` 0.10✱ · `్రి` 2.6e-3✱ · `త` 0.88 · `మ` 0.76 · `␣మ` 3.7e-3✱ · `్ర` 1.4e-5✱ · `్ర` 5.6e-4✱ · `్` 1.0e-3✱ · `ద` 0.01✱ · `ిత` 2.1e-3✱ · `్రి` 0.02✱ · `␣గ` 0.07 · `గ` 0.21 · `మ` 0.15✱ · `్య` 0.38 · `␣హ` 0.94 · `␣హ` 0.55 · `మ` 0.37✱ · `్రు` 0.60 · `తి` 0.38 · `క` 0.21✱ · `్రి` 6.6e-3✱ · `ల` 0.37 · `ం` 1.5e-3✱ |

</details>

[↑ meters](#meters)

---

<a id="mattebhavikriditamu"></a>

## 3. మత్తేభవిక్రీడితము (mattebhavikriditamu)

```text
Meter: మత్తేభవిక్రీడితము (mattebhavikriditamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: స భ ర న మ య వ, i.e. IIU UII UIU III UUU IUU IU (20 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 14th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter మత్తేభవిక్రీడితము (mattebhavikriditamu).

Meter: మత్తేభవిక్రీడితము (mattebhavikriditamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: స భ ర న మ య వ, i.e. IIU UII UIU III UUU IUU IU (20 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 14th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 127 tokens · 33.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మనతగ్రిమ్యపుమన్మగద్రమును దాట్య్య్మక్రిమ్యశల్యమ్య జమ్ | `IIUUIIUIUIIIUUUIUUIU` |
| 2 | తి నకన్ చేరగెనుమ్రమమ్రునతగమ్య్య్తీయమ్యజన్రుమ్యటమ్ | `IIUUIIUIUIIIUUUIUUIU` |
| 3 | మ్రి నిమత్యశ్య్యమమమ్యతిల్యకను చూవ్వ్రిస్రమ్రియక్రియ్య్యదిర్ | `IIUUIIUIUIIIUUUIUUIU` |
| 4 | తి నలల్లల్లయ లేదు లేదు స భరన్య్య్తిమ్యన్యగమ్య్యమ్యమమ్ | `IIUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 33% · repeated lines 0 · mean token probability (geometric) 0.008 · model's first choice kept 26% · constraint overrode 67% · backtracks 0

<details><summary>Token probabilities (127 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.44 · `న` 0.03 · `త` 0.04 · `గ` 0.02 · `్రి` 4.7e-3✱ · `మ` 0.03✱ · `్య` 1.3e-3✱ · `పు` 0.02 · `మ` 0.03 · `న్` 0.02✱ · `మ` 0.12 · `గ` 0.03 · `ద్ర` 0.03✱ · `ము` 0.55 · `ను` 0.19 · `␣దా` 0.59 · `ట` 0.08✱ · `్య` 3.0e-3✱ · `్య` 9.6e-4✱ · `్` 1.7e-5✱ · `మ` 0.20✱ · `క` 0.01 · `్రి` 4.3e-3✱ · `మ` 0.22✱ · `్య` 1.7e-3✱ · `శ` 9.9e-3✱ · `ల` 0.04✱ · `్య` 0.02✱ · `మ` 0.06✱ · `్య` 2.1e-3✱ · `␣జ` 0.02✱ · `మ` 0.19 · `్` 4.6e-5✱ · `⏎` 0.02✱ forced |
| 2 | `తి` 0.24 · `␣న` 5.3e-4✱ · `క` 0.02✱ · `న్` 3.2e-3✱ · `␣చే` 1.00 · `ర` 5.1e-3✱ · `గ` 0.91 · `ె` 0.99 · `ను` 0.18 · `మ` 0.01✱ · `్రమ` 3.5e-4✱ · `మ` 6.0e-3✱ · `్రు` 4.0e-5✱ · `న` 0.92 · `త` 0.90 · `గ` 0.98 · `మ` 3.3e-3✱ · `్య` 4.3e-5✱ · `్య` 0.96 · `్` 2.0e-6✱ · `త` 5.2e-3✱ · `ీయ` 4.0e-4✱ · `మ` 6.5e-3✱ · `్య` 4.8e-6✱ · `జ` 0.83 · `న` 0.98 · `్రు` 2.5e-4✱ · `మ` 0.21✱ · `్య` 1.3e-6✱ · `ట` 0.96 · `మ` 0.69 · `్` 3.7e-6✱ · `⏎` 0.01✱ forced |
| 3 | `మ` 0.90 · `్రి` 4.2e-4✱ · `␣ని` 1.9e-4✱ · `మ` 1.00 · `త్య` 3.0e-3✱ · `శ` 0.99 · `్య` 1.7e-3✱ · `్య` 0.97 · `మ` 0.98 · `మ` 5.0e-3✱ · `మ` 3.9e-3✱ · `్య` 2.7e-3✱ · `తి` 0.97 · `ల` 4.9e-4✱ · `్య` 2.8e-6✱ · `క` 0.98 · `ను` 0.95 · `␣చూ` 0.99 · `వ్వ` 1.8e-4✱ · `్రి` 7.4e-6✱ · `స` 2.3e-3✱ · `్రమ` 3.3e-5✱ · `్రియ` 8.5e-5✱ · `క` 1.3e-5✱ · `్రియ` 1.8e-4✱ · `్య` 1.6e-4✱ · `్య` 0.02✱ · `ది` 9.5e-4✱ · `ర` 4.5e-4✱ · `్` 1.2e-4✱ · `⏎` 0.15✱ forced |
| 4 | `తి` 6.3e-3✱ · `␣న` 1.4e-3✱ · `ల` 8.7e-4✱ · `ల్ల` 1.7e-3✱ · `ల్ల` 5.0e-3✱ · `య` 9.6e-3✱ · `␣లేదు` 0.04✱ · `␣లేదు` 0.07✱ · `␣స` 0.55 · `␣భ` 0.87 · `ర` 0.75 · `న` 0.02✱ · `్య` 8.2e-5✱ · `్య` 0.02✱ · `్` 7.7e-7✱ · `తి` 2.7e-4✱ · `మ` 2.6e-3✱ · `్య` 2.7e-3✱ · `న` 0.80 · `్య` 4.3e-4✱ · `గ` 0.81 · `మ` 9.9e-3✱ · `్య` 0.02✱ · `్య` 0.40 · `మ` 0.02✱ · `్య` 2.2e-4✱ · `మ` 1.2e-3✱ · `మ` 0.83 · `్` 3.0e-7✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 131 tokens · 31.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మమమమ్రమ్రయు మమ్యుమున్ మది ల లంక్వడ్రున్మమమ్యమ్రయున్ | `IIUUIIUIUIIIUUUIUUIU` |
| 2 | యుమునున్ జ్రిల్య జడై మమమ్యమమయున్యుమ్యున్ మదిం శయ్యమమ్ | `IIUUIIUIUIIIUUUIUUIU` |
| 3 | మ్యమమజ్రమ్య్యుమునుమ్యరిజ్యడడడై నా లోతకువ్యావకువ్ | `IIUUIIUIUIIIUUUIUUIU` |
| 4 | మమమస్రర్ర మయవ్రి న్యమ్యమమమమ్యమ్యమ్యమాయీదియయ్ | `IIUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.026 · model's first choice kept 33% · constraint overrode 58% · backtracks 0

<details><summary>Token probabilities (131 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.46 · `మ` 0.15 · `మ` 0.05 · `మ` 0.03 · `్రమ` 4.9e-4✱ · `్ర` 4.5e-4✱ · `యు` 8.5e-3 · `␣మ` 0.09 · `మ` 0.10 · `్య` 8.8e-3✱ · `ు` 0.06 · `ము` 0.07 · `న్` 0.06✱ · `␣మ` 0.12 · `ది` 3.9e-3 · `␣ల` 0.02 · `␣ల` 0.03 · `ంక` 0.05 · `్వ` 1.6e-5✱ · `డ` 9.9e-3✱ · `్రు` 1.8e-4✱ · `న్` 2.4e-4✱ · `మ` 0.75 · `మ` 0.98 · `మ` 0.91 · `్య` 6.6e-4✱ · `మ` 0.11✱ · `్ర` 0.36 · `యు` 0.95 · `న` 2.4e-4✱ · `్` 1.1e-5✱ · `⏎` 4.1e-5✱ forced |
| 2 | `యు` 0.01✱ · `ము` 0.95 · `ను` 0.01✱ · `న్` 2.0e-3✱ · `␣జ` 0.14 · `్రి` 2.8e-3✱ · `ల` 0.03✱ · `్య` 4.7e-4✱ · `␣జ` 0.01 · `డ` 0.70 · `ై` 0.57 · `␣మ` 0.23✱ · `మ` 0.92 · `మ` 0.90 · `్య` 8.3e-3✱ · `మ` 0.41 · `మ` 0.53 · `యు` 0.44 · `న` 0.15✱ · `్య` 2.2e-3✱ · `ు` 9.2e-3✱ · `మ` 0.24 · `్య` 0.03✱ · `ు` 0.05✱ · `న్` 0.94 · `␣మ` 0.92 · `ది` 0.85 · `ం` 6.6e-4✱ · `␣శ` 2.3e-3✱ · `య` 0.28 · `్య` 6.5e-3✱ · `మ` 0.01✱ · `మ` 0.75 · `్` 1.2e-5✱ · `⏎` 0.12✱ forced |
| 3 | `మ` 0.96 · `్య` 0.94 · `మ` 1.4e-3✱ · `మ` 0.11✱ · `జ` 0.98 · `్ర` 5.5e-4✱ · `మ` 0.13✱ · `్య` 2.5e-3✱ · `్య` 0.61 · `ు` 0.85 · `ము` 0.79 · `ను` 0.04✱ · `మ` 2.5e-3✱ · `్య` 3.8e-4✱ · `రి` 0.69 · `జ` 6.9e-3✱ · `్య` 0.01✱ · `డ` 0.32 · `డ` 0.80 · `డ` 0.01✱ · `ై` 0.07✱ · `␣` 9.4e-4✱ · `నా` 1.3e-4✱ · `␣లో` 1.8e-4✱ · `త` 9.4e-4✱ · `కు` 2.1e-3✱ · `వ` 1.5e-3✱ · `్యా` 5.6e-4✱ · `వ` 0.02✱ · `కు` 0.01✱ · `వ` 3.4e-3✱ · `్` 1.0e-4✱ · `⏎` 0.17✱ forced |
| 4 | `మ` 0.02✱ · `మ` 6.5e-3✱ · `మ` 0.20✱ · `స` 0.50 · `్ర` 1.6e-3✱ · `ర` 0.34 · `్ర` 1.6e-3✱ · `␣మ` 0.75 · `య` 0.73 · `వ` 0.03✱ · `్రి` 7.4e-5✱ · `␣` 4.6e-3✱ · `న్య` 0.02✱ · `మ` 0.29 · `్య` 0.02✱ · `మ` 0.66 · `మ` 0.61 · `మ` 0.26 · `మ` 0.89 · `్య` 8.2e-3✱ · `మ` 0.68 · `్య` 6.7e-3✱ · `మ` 0.61 · `్య` 0.01✱ · `మ` 0.10✱ · `ాయ` 2.4e-3✱ · `ీ` 0.02✱ · `ది` 0.01✱ · `య` 0.10✱ · `య` 0.01✱ · `్` 0.02✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 124 tokens · 56.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కలిమక్రా అ సమస్య లోగల శ్రిమంత్య్ర్కయ్యం హకైనక్రిమెన్ | `IIUUIIUIUIIIUUUIUUIU` |
| 2 | కుల సమ్తెండగడుమ్యరవ్రుమహముడ్య్వ్నొక్రిప్ర జగ్రత్యఔ | `IIUUIIUIUIIIUUUIUUIU` |
| 3 | వ ల మక్యం మతిలోత తల్లి ల మకమ్య్య్వర్రిమ్య అంత్య్రౌ మయమ్ | `IIUUIIUIUIIIUUUIUUIU` |
| 4 | మ లతిమ్యో మతి లేదు లేదు మతి లే బ్య్య్మయ్ లక్ష్తినిన్సభ్ర నమ్ | `IIUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 21% · single-akshara words 29% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 41% · constraint overrode 52% · backtracks 30

<details><summary>Token probabilities (124 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.53 · `లి` 0.76 · `మ` 1.00 · `క` 0.84 · `్రా` 0.99 · `␣అ` 0.90 · `␣సమ` 0.77 · `స` 0.98 · `్య` 0.86 · `␣లో` 1.00 · `గ` 0.89 · `ల` 0.96 · `␣శ` 1.00 · `్రి` 0.99 · `మ` 0.97 · `ంత` 0.96 · `్య` 8.0e-6✱ · `్ర` 2.0e-4✱ · `్` 2.8e-7✱ · `క` 1.5e-5✱ · `య` 0.89 · `్యం` 2.1e-4✱ · `␣హ` 1.7e-5✱ · `క` 0.90 · `ైన` 0.98 · `క` 0.03✱ · `్రి` 1.8e-4✱ · `మె` 3.0e-3 · `న్` 0.02 · `⏎` 0.97 |
| 2 | `కు` 3.0e-3 · `ల` 0.04✱ · `␣స` 7.5e-3 · `మ్` 0.03 · `త` 0.20 · `ెం` 2.9e-5✱ · `డ` 0.81 · `గ` 0.01 · `డు` 2.7e-3✱ · `మ` 8.0e-5✱ · `్య` 4.6e-6✱ · `ర` 0.99 · `వ` 0.91 · `్రు` 3.0e-5✱ · `మ` 0.68 · `హ` 0.83 · `ము` 0.96 · `డ` 6.4e-6✱ · `్య` 1.1e-4✱ · `్వ` 8.2e-5✱ · `్` 3.7e-5✱ · `న` 6.6e-4✱ · `ొ` 8.7e-6✱ · `క` 0.99 · `్రి` 1.6e-5✱ · `ప్ర` 1.2e-3✱ · `␣జగ` 0.44 · `్ర` 3.4e-4✱ · `త` 0.22 · `్య` 4.9e-6✱ · `ఔ` 2.5e-3✱ · `⏎` 8.1e-5 forced |
| 3 | `వ` 0.52 · `␣ల` 1.4e-3✱ · `␣మ` 0.61 · `క` 0.84 · `్యం` 1.1e-3✱ · `␣మ` 4.4e-3✱ · `తి` 0.93 · `లో` 0.03✱ · `త` 0.83 · `␣తల్లి` 3.5e-3✱ · `␣ల` 0.67 · `␣మ` 0.49 · `క` 0.55 · `మ` 7.6e-4✱ · `్య` 2.3e-4✱ · `్య` 6.2e-6✱ · `్వర` 3.0e-5✱ · `్రి` 4.4e-5✱ · `మ` 0.06✱ · `్య` 5.0e-3✱ · `␣అంత` 1.7e-4✱ · `్య` 0.99 · `్ర` 0.98 · `ౌ` 0.93 · `␣మ` 8.7e-3✱ · `య` 0.97 · `మ` 0.73 · `్` 2.2e-6✱ · `⏎` 8.6e-4✱ forced |
| 4 | `మ` 0.79 · `␣ల` 4.0e-4✱ · `తి` 0.99 · `మ` 0.02✱ · `్య` 2.1e-3✱ · `ో` 3.3e-3✱ · `␣మ` 3.4e-3✱ · `తి` 0.06✱ · `␣లేదు` 0.34 · `␣లేదు` 0.08 · `␣మ` 0.45 · `తి` 0.61 · `␣లే` 0.05✱ · `␣` 0.92 · `బ` 2.9e-5✱ · `్య` 2.0e-4✱ · `్య` 5.0e-4✱ · `్` 2.5e-3✱ · `మ` 1.3e-3✱ · `య` 0.04✱ · `్` 3.7e-3✱ · `␣ల` 4.3e-3✱ · `క్ష్` 0.02✱ · `తి` 0.06✱ · `ని` 0.02✱ · `న` 8.1e-3✱ · `్` 4.9e-5✱ · `స` 0.67 · `భ` 4.3e-3✱ · `్ర` 1.1e-3✱ · `␣న` 0.68 · `మ` 0.11✱ · `్` 3.2e-6✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 140 tokens · 66.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | లమ నిల్యాము జ శివ్వరన్ ల కృము లగ్య్చ్లశ్యమ్యలల్వజ్వరన్ | `IIUUIIUIUIIIUUUIUUIU` |
| 2 | చమ త్రల్యగ్య్చ్లశశమ్యలల్వజవనల్య్య్చల్యగ్య్చ్లలల్రమ్రిలల్ | `IIUUIIUIUIIIUUUIUUIU` |
| 3 | శిమవన్ లక్యలగయ్య్చలల్యలలలల్య్య్యీ నేను ప్రవ్రమ్రమమ్ | `IIUUIIUIUIIIUUUIUUIU` |
| 4 | భి మరేడిత్య యితస్ర రన్యయ వలల్ల్య్వృవ్రీమముమ్రీమయమ్ | `IIUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.025 · model's first choice kept 48% · constraint overrode 49% · backtracks 30

<details><summary>Token probabilities (140 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ల` 1.1e-3 · `మ` 0.99 · `␣ని` 0.99 · `ల` 0.99 · `్యా` 0.99 · `ము` 0.94 · `␣జ` 0.94 · `␣శ` 0.69 · `ి` 0.99 · `వ` 0.98 · `్వర` 0.71 · `న్` 0.99 · `␣ల` 0.72 · `␣కృ` 5.4e-3 · `ము` 0.04 · `␣ల` 0.73 · `గ` 0.96 · `్య` 0.94 · `్` 2.1e-4✱ · `చ` 2.5e-3✱ · `్` 1.2e-5✱ · `ల` 7.8e-4✱ · `శ` 1.9e-5✱ · `్య` 1.3e-4✱ · `మ` 0.76 · `్య` 5.9e-5✱ · `ల` 0.74 · `ల` 0.04✱ · `్వ` 7.8e-6✱ · `జ` 0.04✱ · `్వర` 0.16 · `న్` 0.40 · `⏎` 0.52 |
| 2 | `చ` 1.8e-3 · `మ` 0.57 · `␣త` 0.94 · `్ర` 0.49 · `ల` 0.07✱ · `్య` 2.0e-3✱ · `గ` 0.95 · `్య` 0.86 · `్` 0.75 · `చ` 0.80 · `్` 0.58 · `ల` 0.96 · `శ` 0.64 · `శ` 1.7e-4✱ · `మ` 0.73 · `్య` 0.75 · `ల` 0.76 · `ల` 0.86 · `్వ` 0.73 · `జ` 0.86 · `వ` 0.70 · `న` 0.87 · `ల` 0.62 · `్య` 1.9e-4✱ · `్య` 0.03✱ · `్` 7.7e-4✱ · `చ` 0.20 · `ల` 0.67 · `్య` 7.2e-4✱ · `గ` 0.85 · `్య` 0.72 · `్` 0.53 · `చ` 0.72 · `్` 0.33 · `ల` 0.90 · `ల` 3.6e-3✱ · `ల` 0.97 · `్రమ` 4.6e-7✱ · `్రి` 5.9e-4✱ · `ల` 0.91 · `ల` 0.03✱ · `్` 1.1e-6✱ · `⏎` 0.01✱ forced |
| 3 | `␣శ` 0.46 · `ి` 0.81 · `మ` 2.3e-4✱ · `వ` 0.09✱ · `న్` 0.93 · `␣ల` 0.88 · `క` 1.0e-3✱ · `్య` 2.4e-4✱ · `ల` 0.25 · `గ` 0.74 · `య్య` 3.9e-4✱ · `్` 0.50 · `చ` 0.32 · `ల` 0.89 · `ల` 0.68 · `్య` 4.4e-4✱ · `ల` 0.01✱ · `ల` 9.7e-3✱ · `ల` 0.21✱ · `ల` 0.08✱ · `్య` 6.9e-4✱ · `్య` 3.8e-3✱ · `్య` 4.0e-4✱ · `ీ` 9.7e-5✱ · `␣నేను` 3.5e-3✱ · `␣ప్ర` 1.3e-3✱ · `వ` 9.4e-3✱ · `్రమ` 7.0e-4✱ · `్రమ` 2.6e-4✱ · `మ` 0.43 · `్` 5.7e-6✱ · `⏎` 0.20✱ forced |
| 4 | `భ` 0.85 · `ి` 5.7e-3✱ · `␣మ` 6.1e-4✱ · `రే` 3.0e-3✱ · `డి` 0.99 · `త` 0.99 · `్య` 5.8e-5✱ · `␣య` 0.58 · `ిత` 5.8e-5✱ · `స` 0.01✱ · `్ర` 1.7e-5✱ · `␣ర` 0.81 · `న` 0.01✱ · `్య` 2.6e-6✱ · `య` 0.97 · `␣వ` 0.94 · `ల` 2.5e-3✱ · `ల్ల` 5.4e-4✱ · `్య` 7.1e-5✱ · `్` 4.6e-3✱ · `వ` 4.7e-4✱ · `ృ` 7.2e-4✱ · `వ` 2.8e-3✱ · `్రీ` 7.3e-4✱ · `మ` 1.1e-3✱ · `ము` 0.06✱ · `మ` 5.4e-3✱ · `్రీ` 1.5e-3✱ · `మ` 0.25 · `య` 0.06✱ · `మ` 0.10✱ · `్` 2.0e-4✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 114 tokens · 29.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | అమృతత్యామమ మమ్రకప్రియమతిప్ర్వ్యన్రుత్రిమున్రీమనీ | `IIUUIIUIUIIIUUUIUUIU` |
| 2 | అమృతత్యామమ మమ్రకమ్యనతికమ్యమ్రక్యమమ్యమ్యఆ | `IIUUIIUIUIIIUUUIUUIU` |
| 3 | మమమమ్రుల్యమతిక్రమట్రుదిమమమ్యమ్యమ్యమల్యమ్యఈ | `IIUUIIUIUIIIUUUIUUIU` |
| 4 | కమ కంటే అతిడమ్యముల్లము ల లస్య్య్కక్యమ్య మేభయ్రిలే | `IIUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 9% · repeated lines 0 · mean token probability (geometric) 0.019 · model's first choice kept 40% · constraint overrode 53% · backtracks 0

<details><summary>Token probabilities (114 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `అ` 0.03 · `మ` 0.11✱ · `ృత` 0.68 · `త` 0.15 · `్యా` 1.9e-3✱ · `మ` 0.28 · `మ` 0.16 · `␣మ` 0.10 · `మ` 0.45 · `్ర` 4.5e-4✱ · `క` 0.09 · `ప` 0.01✱ · `్రియ` 0.17 · `మ` 0.13 · `తి` 0.07 · `ప` 0.03✱ · `్ర` 6.1e-4✱ · `్వ` 1.3e-5✱ · `్య` 4.3e-4✱ · `న` 3.1e-3✱ · `్రు` 1.6e-4✱ · `త` 0.25 · `్రి` 1.4e-4✱ · `ము` 8.0e-3✱ · `న` 0.01✱ · `్రీ` 4.3e-5✱ · `మ` 0.07✱ · `నీ` 5.1e-3✱ · `⏎` 0.62 |
| 2 | `అ` 0.24 · `మ` 0.77 · `ృత` 0.18 · `త` 0.21 · `్యా` 0.46 · `మ` 0.85 · `మ` 0.74 · `␣మ` 0.37 · `మ` 0.46 · `్ర` 0.11✱ · `క` 0.68 · `మ` 0.38 · `్య` 1.2e-3✱ · `న` 0.02 · `తి` 0.10✱ · `క` 0.10 · `మ` 0.10✱ · `్య` 5.8e-3✱ · `మ` 0.12✱ · `్ర` 3.4e-3✱ · `క` 0.41 · `్య` 9.3e-6✱ · `మ` 0.34 · `మ` 0.57 · `్య` 0.06✱ · `మ` 0.01✱ · `్య` 2.0e-3✱ · `ఆ` 7.1e-3 · `⏎` 0.13 forced |
| 3 | `మ` 0.28 · `మ` 0.50 · `మ` 0.46 · `మ` 0.49 · `్రు` 4.3e-5✱ · `ల` 0.89 · `్య` 5.5e-7✱ · `మ` 0.79 · `తి` 0.57 · `క` 0.88 · `్రమ` 5.8e-8✱ · `ట` 0.02✱ · `్రు` 2.1e-5✱ · `ది` 0.69 · `మ` 0.03✱ · `మ` 0.76 · `మ` 0.02✱ · `్య` 1.2e-3✱ · `మ` 0.79 · `్య` 0.01✱ · `మ` 0.56 · `్య` 3.3e-3✱ · `మ` 0.25 · `ల` 0.86 · `్య` 0.51 · `మ` 0.54 · `్య` 1.6e-3✱ · `ఈ` 0.04✱ · `⏎` 0.08✱ forced |
| 4 | `క` 0.61 · `మ` 0.81 · `␣కంటే` 3.3e-4✱ · `␣అతి` 1.3e-3✱ · `డ` 0.99 · `మ` 0.98 · `్య` 1.6e-4✱ · `ము` 5.4e-3✱ · `ల్ల` 2.0e-4✱ · `ము` 8.2e-4✱ · `␣ల` 0.01✱ · `␣ల` 0.04✱ · `స` 2.1e-4✱ · `్య` 2.0e-4✱ · `్య` 1.6e-3✱ · `్` 3.4e-6✱ · `క` 8.6e-4✱ · `క` 0.04✱ · `్య` 6.4e-4✱ · `మ` 0.05✱ · `్య` 0.09✱ · `␣మ` 0.46 · `ే` 0.83 · `భ` 0.78 · `య` 3.0e-4✱ · `్రి` 3.1e-7✱ · `లే` 9.9e-5✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 112 tokens · 29.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మహతౌకమ్యము సక్రి సక్రియుముముట్య్య్మమ్యామమమ్రాశగస్ | `IIUUIIUIUIIIUUUIUUIU` |
| 2 | మహ సాగర్యమునుండిటిన్వర లతన్ ప్ర్శ్మమ్యాహనుమ్యాడు ఆ | `IIUUIIUIUIIIUUUIUUIU` |
| 3 | న్క్రి హ జెచ్చేను మమగ్య లంకనునుసిమ్రిర్రున్రయక్రిప్రియచ్ | `IIUUIIUIUIIIUUUIUUIU` |
| 4 | క్ష్యు హు పైనిన్య పదాలలో గణణ పొర్యూ లేదు లేదుమ్రమీ | `IIUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 10% · single-akshara words 24% · repeated lines 0 · mean token probability (geometric) 0.009 · model's first choice kept 31% · constraint overrode 59% · backtracks 0

<details><summary>Token probabilities (112 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.34 · `హ` 0.05 · `త` 0.04✱ · `ౌ` 0.30 · `క` 0.05 · `మ` 0.04✱ · `్య` 2.7e-3✱ · `ము` 0.83 · `␣స` 0.07 · `క` 0.03✱ · `్రి` 7.8e-3✱ · `␣స` 0.09 · `క` 7.6e-3✱ · `్రి` 1.8e-3✱ · `యు` 0.02 · `ము` 0.25 · `ము` 0.08 · `ట` 0.03✱ · `్య` 2.9e-4✱ · `్య` 3.8e-3✱ · `్` 3.0e-6✱ · `మ` 0.16✱ · `మ` 0.17✱ · `్యా` 2.4e-4✱ · `మ` 0.27 · `మ` 0.23✱ · `మ` 0.21 · `్రా` 6.9e-4✱ · `శ` 0.02✱ · `గ` 0.03 · `స` 0.02 · `్` 1.7e-7✱ · `⏎` 0.17✱ forced |
| 2 | `మ` 0.28 · `హ` 0.33 · `␣సా` 0.04✱ · `గర` 0.28 · `్య` 5.3e-5✱ · `ము` 0.95 · `ను` 0.78 · `ండి` 6.6e-4✱ · `టి` 0.90 · `న` 5.7e-3✱ · `్వర` 7.6e-5✱ · `␣ల` 0.09 · `త` 0.03 · `న్` 7.4e-3✱ · `␣ప్ర` 0.99 · `్` 6.5e-7✱ · `శ` 0.85 · `్` 3.2e-7✱ · `మ` 1.7e-3✱ · `మ` 0.26✱ · `్యా` 3.7e-4✱ · `హ` 0.59 · `ను` 0.88 · `మ` 0.01✱ · `్యా` 1.8e-4✱ · `డు` 0.96 · `␣ఆ` 0.03✱ · `⏎` 7.7e-3 forced |
| 3 | `న్` 0.70 · `క` 0.98 · `్రి` 1.1e-5✱ · `␣హ` 3.0e-4✱ · `␣జ` 0.89 · `ె` 0.77 · `చ్చే` 0.04✱ · `ను` 0.98 · `␣మ` 0.01✱ · `మ` 0.70 · `గ` 0.01 · `్య` 1.7e-4✱ · `␣ల` 0.03✱ · `ంక` 0.12✱ · `ను` 0.99 · `ను` 4.1e-4✱ · `సి` 0.98 · `మ` 0.02✱ · `్రి` 2.1e-5✱ · `ర` 0.94 · `్రు` 1.1e-4✱ · `న` 0.01✱ · `్ర` 6.9e-5✱ · `య` 1.2e-4✱ · `క` 0.99 · `్రి` 5.3e-5✱ · `ప` 4.8e-3✱ · `్రియ` 7.8e-7✱ · `చ్` 1.1e-3✱ · `⏎` 6.0e-3✱ forced |
| 4 | `క్ష` 0.09✱ · `్య` 9.2e-4✱ · `ు` 1.2e-5✱ · `␣` 4.5e-5✱ · `హు` 1.2e-5✱ · `␣ప` 1.00 · `ైన` 1.00 · `ిన` 9.4e-5✱ · `్య` 3.6e-7✱ · `␣పద` 4.1e-4✱ · `ాలలో` 1.8e-4✱ · `␣గణ` 1.00 · `ణ` 1.00 · `␣పొ` 1.00 · `ర` 0.99 · `్యూ` 1.2e-6✱ · `␣లేదు` 2.9e-3✱ · `␣లేదు` 0.01✱ · `మ` 1.2e-4✱ · `్రమ` 2.5e-6✱ · `ీ` 0.92 |

</details>

[↑ meters](#meters)

---

<a id="sardulavikriditamu"></a>

## 4. శార్దూలవిక్రీడితము (sardulavikriditamu)

```text
Meter: శార్దూలవిక్రీడితము (sardulavikriditamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: మ స జ స త త గురువు, i.e. UUU IIU IUI IIU UUI UUI U (19 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 13th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter శార్దూలవిక్రీడితము (sardulavikriditamu).

Meter: శార్దూలవిక్రీడితము (sardulavikriditamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: మ స జ స త త గురువు, i.e. UUU IIU IUI IIU UUI UUI U (19 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 13th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 124 tokens · 33.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మామల్రిమ్రద మవ్రిదిల్య మలధర్వ్య్మద్బుత్రియౌమామముమ్ | `UUUIIUIUIIIUUUIUUIU` |
| 2 | మౌమల్యమ్రదకమ్రిపుణ్య జగ ధమ్యమ్యౌమమన్మమ్యటిక్ | `UUUIIUIUIIIUUUIUUIU` |
| 3 | ఏమిగ్యంవని లోక మౌన మతు మమ్రృమ్రగ్రి జయ్వర్రుముత్ | `UUUIIUIUIIIUUUIUUIU` |
| 4 | డ్రామమ్యంచెని ప్రేమముమ్యము ల్య మమ్య్య్రద్రున్ముముమ్శశ్రముత్ | `UUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.012 · model's first choice kept 30% · constraint overrode 61% · backtracks 0

<details><summary>Token probabilities (124 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.20 · `మ` 0.11 · `ల` 0.05 · `్రి` 1.1e-4✱ · `మ` 0.04✱ · `్ర` 1.5e-3✱ · `ద` 0.37 · `␣మ` 0.11 · `వ` 0.02✱ · `్రి` 7.4e-4✱ · `ది` 2.6e-3 · `ల` 0.02✱ · `్య` 1.2e-4✱ · `␣మ` 0.35 · `ల` 0.01 · `ధ` 7.1e-3 · `ర` 0.15 · `్వ` 1.0e-6✱ · `్య` 3.8e-4✱ · `్` 9.1e-7✱ · `మ` 0.10✱ · `ద్` 2.2e-4✱ · `బు` 0.10 · `త` 0.33 · `్రియ` 8.1e-5✱ · `ౌ` 0.03✱ · `మా` 0.02✱ · `మ` 0.06✱ · `ము` 0.05✱ · `మ` 0.01✱ · `్` 1.4e-5✱ · `⏎` 0.26 forced |
| 2 | `మ` 0.41 · `ౌ` 0.02✱ · `మ` 0.03✱ · `ల` 0.12 · `్య` 2.3e-3✱ · `మ` 0.25✱ · `్ర` 8.0e-4✱ · `ద` 0.22 · `క` 0.07 · `మ` 0.04✱ · `్రి` 3.0e-5✱ · `పు` 0.93 · `ణ` 0.11✱ · `్య` 0.58 · `␣జగ` 0.04 · `␣ధ` 0.05 · `మ` 0.08 · `్య` 0.02✱ · `మ` 0.22✱ · `్య` 8.3e-4✱ · `ౌ` 0.58 · `మ` 0.18✱ · `మ` 0.72 · `న్` 0.03✱ · `మ` 8.4e-3✱ · `మ` 0.78 · `్య` 1.1e-5✱ · `టి` 0.02✱ · `క` 0.03✱ · `్` 4.0e-7✱ · `⏎` 0.86 |
| 3 | `ఏ` 0.70 · `మి` 1.9e-5✱ · `గ` 4.2e-4✱ · `్యం` 2.2e-5✱ · `వ` 0.58 · `ని` 0.84 · `␣లో` 0.98 · `క` 0.98 · `␣మ` 0.61 · `ౌ` 0.88 · `న` 0.89 · `␣మ` 0.33 · `తు` 0.80 · `␣మ` 0.36 · `మ` 0.51 · `్ర` 1.2e-5✱ · `ృ` 1.9e-3✱ · `మ` 0.98 · `్ర` 1.1e-5✱ · `గ` 0.99 · `్రి` 1.3e-3✱ · `␣జ` 1.00 · `య` 0.99 · `్వర` 2.4e-5✱ · `్రు` 5.6e-5✱ · `ము` 0.29 · `త` 0.96 · `్` 1.5e-7✱ · `⏎` 0.51 |
| 4 | `డ` 0.46 · `్రా` 5.0e-6✱ · `మ` 0.03✱ · `మ` 1.1e-3✱ · `్యం` 1.1e-3✱ · `చె` 0.12 · `ని` 0.02✱ · `␣ప్రేమ` 0.85 · `ము` 0.21✱ · `మ` 2.1e-3✱ · `్య` 4.8e-4✱ · `ము` 7.9e-3✱ · `␣ల` 0.03✱ · `్య` 0.02✱ · `␣మ` 0.04✱ · `మ` 0.02✱ · `్య` 3.0e-4✱ · `్య` 0.01✱ · `్ర` 7.4e-5✱ · `ద` 5.3e-3✱ · `్రు` 4.9e-4✱ · `న్` 3.7e-4✱ · `ము` 3.4e-3✱ · `ము` 0.03✱ · `మ` 0.02✱ · `్` 3.8e-3✱ · `శ` 1.3e-3✱ · `శ` 0.01✱ · `్రమ` 1.2e-3✱ · `ు` 0.01✱ · `త` 0.01✱ · `్` 8.0e-3✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 154 tokens · 28.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మమ్యుమ్రువ్యమమక్తలమ్ర సన ముగ్య్య్మమ్రోమమమ్రున్రుకుక్ | `UUUIIUIUIIIUUUIUUIU` |
| 2 | టెమ్యెయ్ మమ్యుమశువ్యమమ్యలమమన్న్య్డెమ్రోమమమ్రున్రుకుక్ | `UUUIIUIUIIIUUUIUUIU` |
| 3 | నమ్యెయ్ మమ్యుమశువ్యమమ్యలమమన్న్న్యాయగ్యెమోమమ్లునౌ | `UUUIIUIUIIIUUUIUUIU` |
| 4 | క్మమ్యయ్యయ్ మమయుమ్యువవ్యమమలమ్యన్న్న్యాయజడ్రమ్యమమ్ | `UUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.086 · model's first choice kept 60% · constraint overrode 34% · backtracks 0

<details><summary>Token probabilities (154 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.82 · `మ` 0.21 · `్య` 2.2e-3✱ · `ు` 0.19 · `మ` 0.09 · `్ర` 1.2e-3✱ · `ు` 0.07 · `వ` 8.4e-3 · `్య` 1.7e-3✱ · `మ` 0.21 · `మ` 0.07 · `క్త` 1.8e-3 · `ల` 0.02 · `మ` 0.04✱ · `్ర` 4.5e-3✱ · `␣స` 0.06✱ · `న` 0.03 · `␣ము` 7.4e-3 · `గ` 0.05 · `్య` 6.8e-3✱ · `్య` 4.8e-4✱ · `్` 2.9e-8✱ · `మ` 0.08✱ · `మ` 0.49 · `్రో` 1.4e-4✱ · `మ` 0.24 · `మ` 0.17 · `మ` 0.22 · `్ర` 1.2e-3✱ · `ు` 0.13 · `న` 0.02✱ · `్రు` 1.9e-5✱ · `కు` 4.6e-3✱ · `క` 0.92 · `్` 6.6e-7✱ · `⏎` 1.4e-4✱ forced |
| 2 | `ట` 0.87 · `ె` 0.94 · `మ` 1.1e-3✱ · `్య` 2.6e-4✱ · `ె` 0.30 · `య` 0.38 · `్` 7.3e-4✱ · `␣మ` 0.97 · `మ` 0.99 · `్య` 0.99 · `ు` 0.99 · `మ` 0.99 · `శ` 2.7e-3✱ · `ు` 0.78 · `వ` 0.83 · `్య` 0.49 · `మ` 0.72 · `మ` 0.73 · `్య` 3.8e-4✱ · `ల` 0.78 · `మ` 0.74 · `మ` 0.10✱ · `న` 0.02✱ · `్` 6.5e-4✱ · `న` 0.10✱ · `్య` 1.0e-4✱ · `్` 0.02✱ · `డ` 0.02✱ · `ె` 5.1e-3✱ · `మ` 0.85 · `్రో` 0.77 · `మ` 0.79 · `మ` 0.89 · `మ` 0.89 · `్ర` 0.89 · `ు` 0.94 · `న` 0.88 · `్రు` 0.63 · `కు` 0.67 · `క` 0.76 · `్` 0.81 · `⏎` 0.99 |
| 3 | `న` 0.86 · `మ` 0.99 · `్య` 0.99 · `ె` 0.94 · `య` 0.98 · `్` 3.2e-3✱ · `␣మ` 1.00 · `మ` 1.00 · `్య` 1.00 · `ు` 1.00 · `మ` 1.00 · `శ` 0.97 · `ు` 0.99 · `వ` 1.00 · `్య` 0.93 · `మ` 0.99 · `మ` 0.99 · `్య` 0.98 · `ల` 0.99 · `మ` 0.93 · `మ` 0.90 · `న్` 0.97 · `న్` 0.02✱ · `న` 0.62 · `్య` 0.98 · `ాయ` 9.4e-5✱ · `గ` 0.94 · `్య` 1.3e-3✱ · `ె` 0.89 · `మ` 0.97 · `ో` 0.01✱ · `మ` 0.94 · `మ` 0.97 · `్` 1.5e-4✱ · `ల` 0.02✱ · `ు` 0.41 · `న` 0.77 · `ౌ` 0.03✱ · `⏎` 9.8e-4✱ forced |
| 4 | `క` 0.85 · `్` 0.44 · `మ` 1.6e-4✱ · `మ` 0.25✱ · `్య` 0.07✱ · `య` 0.08✱ · `్య` 2.0e-3✱ · `య` 0.80 · `్` 0.83 · `␣మ` 0.86 · `మ` 0.98 · `య` 3.1e-5✱ · `ు` 0.99 · `మ` 1.00 · `్య` 5.3e-4✱ · `ు` 0.94 · `వ` 0.95 · `వ` 0.03✱ · `్య` 6.0e-3✱ · `మ` 0.97 · `మ` 0.08✱ · `ల` 0.60 · `మ` 0.30 · `్య` 4.8e-4✱ · `న్` 0.99 · `న్` 0.07✱ · `న` 0.84 · `్య` 0.98 · `ాయ` 0.98 · `జ` 0.95 · `డ` 0.99 · `్ర` 5.3e-4✱ · `మ` 0.97 · `్య` 4.8e-5✱ · `మ` 0.97 · `మ` 0.99 · `్` 0.98 |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 116 tokens · 53.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మత్ర్యజ్యత్మశమర్ర హానుమతుడన్ ప్ర్ర్మగ్యామనుమ్రాంధకిమ్ | `UUUIIUIUIIIUUUIUUIU` |
| 2 | లత్ర్యర్యాడి మహాశ శక్తి మ మయున్ లంకన్ జడించడ్రి నమ్ | `UUUIIUIUIIIUUUIUUIU` |
| 3 | ద్రుత్ర్యించిత్రమదేవినిత్వరకిడెన్న్క్దుత్యా మమగ్వవ్రి దిత్ | `UUUIIUIUIIIUUUIUUIU` |
| 4 | మౌత్ర్యర్యక్తి డు లేదు లేదు లలిచిం వానుంబ లేదువ్ మయున్ | `UUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.007 · model's first choice kept 32% · constraint overrode 63% · backtracks 30

<details><summary>Token probabilities (116 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.88 · `త్ర` 2.6e-3 · `్య` 0.94 · `జ` 0.17 · `్య` 2.7e-3✱ · `త్మ` 0.80 · `శ` 0.04 · `మ` 0.94 · `ర` 0.95 · `్` 0.96 · `ర` 0.91 · `␣హ` 0.99 · `ాను` 0.43✱ · `మ` 0.35✱ · `తు` 1.00 · `డ` 0.94 · `న్` 0.67 · `␣ప్ర` 1.00 · `్ర` 5.8e-7✱ · `్` 4.1e-6✱ · `మ` 0.93 · `గ` 0.04✱ · `్యా` 5.7e-5✱ · `మ` 0.30✱ · `ను` 4.1e-3 · `మ` 0.32 · `్రా` 7.9e-4✱ · `ంధ` 5.7e-4 · `కి` 4.3e-3 · `మ` 0.04✱ · `్` 5.8e-8✱ · `⏎` 0.06✱ forced |
| 2 | `ల` 2.7e-3✱ · `త` 1.5e-3✱ · `్ర` 4.3e-8✱ · `్య` 1.1e-5✱ · `ర` 0.97 · `్యా` 5.6e-5✱ · `డి` 0.99 · `␣మ` 0.35 · `హా` 0.52 · `శ` 0.98 · `␣శక్తి` 5.4e-6✱ · `␣మ` 6.8e-4✱ · `␣మ` 0.94 · `యు` 2.8e-3✱ · `న్` 0.95 · `␣ల` 0.98 · `ం` 0.97 · `క` 0.99 · `న్` 1.6e-3✱ · `␣జ` 1.00 · `డ` 1.00 · `ించ` 1.00 · `డ` 0.99 · `్రి` 1.0e-5✱ · `␣న` 1.1e-3✱ · `మ` 5.4e-3✱ · `్` 1.3e-6✱ · `⏎` 0.17✱ forced |
| 3 | `ద్ర` 0.27 · `ు` 3.7e-4✱ · `త్` 3.1e-4✱ · `ర్య` 9.7e-6✱ · `ించి` 0.91 · `త` 8.4e-6✱ · `్రమ` 4.1e-6✱ · `దే` 0.95 · `వి` 1.00 · `ని` 0.98 · `త` 1.4e-6✱ · `్వర` 1.2e-4✱ · `కి` 0.99 · `డ` 1.00 · `ె` 0.99 · `న్` 0.99 · `న్` 8.7e-3✱ · `క` 2.0e-4✱ · `్` 1.5e-6✱ · `దు` 9.6e-5✱ · `త` 5.9e-4✱ · `్యా` 7.3e-4✱ · `␣మ` 2.4e-3✱ · `మ` 0.08✱ · `గ` 1.5e-4✱ · `్` 4.8e-4✱ · `వ` 1.3e-4✱ · `వ` 1.3e-4✱ · `్రి` 7.1e-5✱ · `␣ది` 9.2e-4✱ · `త` 2.8e-3✱ · `్` 1.4e-5✱ · `⏎` 0.04✱ forced |
| 4 | `మ` 3.8e-3✱ · `ౌ` 0.02✱ · `త్` 2.4e-3✱ · `ర్య` 0.05✱ · `ర్య` 0.02✱ · `క్తి` 3.6e-3✱ · `␣` 8.3e-3✱ · `డు` 1.7e-3✱ · `␣లేదు` 3.8e-3✱ · `␣లేదు` 4.7e-3✱ · `␣ల` 6.6e-4✱ · `లి` 8.4e-5✱ · `చి` 1.9e-3✱ · `ం` 6.8e-3✱ · `␣వ` 2.3e-3✱ · `ాను` 3.0e-3✱ · `ంబ` 2.9e-4✱ · `␣లేదు` 0.01✱ · `వ` 3.0e-3✱ · `్` 1.7e-3✱ · `␣మ` 0.02✱ · `యు` 0.03✱ · `న్` 5.8e-3✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 127 tokens · 58.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మామఛ్యా దితనన్వరల్య మధురమ్యభ్రమ్యమన్ రామ మా | `UUUIIUIUIIIUUUIUUIU` |
| 2 | మౌమల్యృమ్యక ప్రత్వ పద్రియ సశధ్య్య్మంకన్ శశౌరవ్రమమ్ | `UUUIIUIUIIIUUUIUUIU` |
| 3 | రైమల్యమ్యభమమ్యమన్ జయ మముత్రావవ్రముద్రమ్రినవ్ | `UUUIIUIUIIIUUUIUUIU` |
| 4 | మ్య్య్రైమమ్యత్రియముమ్య్య్యయయ్య్య్యయతితియ్య్య్యయ్య్యమ్యసజ్రస్రతత్ | `UUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.021 · model's first choice kept 47% · constraint overrode 49% · backtracks 30

<details><summary>Token probabilities (127 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.25 · `మ` 0.24 · `ఛ` 2.4e-4 · `్యా` 0.49 · `␣ద` 0.50 · `ిత` 0.76 · `న` 0.07 · `న` 0.33 · `్వర` 0.11✱ · `ల` 0.97 · `్య` 0.90 · `␣మ` 0.93 · `ధు` 0.98 · `ర` 0.95 · `మ` 0.95 · `్య` 0.84 · `భ` 0.98 · `్ర` 0.83 · `మ` 0.99 · `్య` 0.76 · `మ` 0.87 · `న్` 0.98 · `␣రామ` 0.84 · `␣` 0.30 · `మా` 0.81 · `⏎` 0.91 |
| 2 | `మ` 0.70 · `ౌ` 0.93 · `మ` 0.78 · `ల` 0.88 · `్య` 3.2e-6✱ · `ృ` 0.02✱ · `మ` 0.99 · `్య` 0.98 · `క` 0.98 · `␣ప్ర` 0.93 · `త` 0.90 · `్వ` 1.0e-4✱ · `␣ప` 1.9e-5✱ · `ద` 0.02 · `్రియ` 4.7e-5✱ · `␣స` 0.04 · `శ` 0.55 · `ధ్య` 3.4e-7 · `్య` 0.76 · `్` 4.4e-11✱ · `మ` 4.5e-5✱ · `ంక` 0.99 · `న్` 0.98 · `␣శ` 1.9e-3✱ · `శ` 0.82 · `ౌ` 0.88 · `ర` 0.47 · `వ` 0.70 · `్రమ` 2.6e-4✱ · `మ` 0.27✱ · `్` 5.7e-8✱ · `⏎` 0.06✱ forced |
| 3 | `ర` 0.78 · `ై` 2.1e-4✱ · `మ` 1.8e-4✱ · `ల్య` 2.1e-3✱ · `మ` 0.04✱ · `్య` 5.0e-6✱ · `భ` 0.95 · `మ` 0.01✱ · `మ` 0.92 · `్య` 0.70 · `మ` 0.73 · `న్` 0.68 · `␣జ` 0.96 · `య` 0.89 · `␣మ` 2.0e-4✱ · `ము` 0.10 · `త` 1.5e-3✱ · `్రా` 6.5e-3✱ · `వ` 0.96 · `వ` 1.1e-3✱ · `్ర` 1.1e-4✱ · `ము` 0.61 · `ద్ర` 0.58 · `మ` 0.03✱ · `్రి` 8.6e-7✱ · `న` 0.55 · `వ` 0.92 · `్` 5.3e-9✱ · `⏎` 0.01✱ forced |
| 4 | `మ` 0.76 · `్య` 4.1e-7✱ · `్య` 6.4e-3✱ · `్ర` 0.69 · `ై` 3.9e-5✱ · `మ` 0.02✱ · `మ` 0.71 · `్య` 1.7e-3✱ · `త` 3.4e-3✱ · `్రియ` 7.4e-5✱ · `ము` 1.1e-3✱ · `మ` 6.6e-4✱ · `్య` 3.1e-3✱ · `్య` 0.01✱ · `్య` 0.01✱ · `య` 2.3e-3✱ · `య` 2.7e-3✱ · `్య` 2.0e-3✱ · `్య` 1.9e-3✱ · `్య` 0.02✱ · `య` 8.1e-4✱ · `తి` 7.5e-4✱ · `తి` 3.0e-3✱ · `య` 1.0e-2✱ · `్య` 0.05✱ · `్య` 0.03✱ · `్య` 0.02✱ · `య` 3.6e-3✱ · `్య` 0.03✱ · `్య` 0.04✱ · `మ` 0.16✱ · `్య` 0.01✱ · `స` 0.81 · `జ` 0.11✱ · `్ర` 6.5e-5✱ · `స` 0.36✱ · `్ర` 5.5e-5✱ · `త` 0.73 · `త` 0.83 · `్` 5.8e-5✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 126 tokens · 31.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జగ్రమ్రిక్రితి మమ్యమగ్యముమమమ్ర్య్జప్యమ్రలౌమమ్రిమా | `UUUIIUIUIIIUUUIUUIU` |
| 2 | మృగ్రుక్యం మమ మమ్యమమ్యమమమమ్య్యేమత్యనుమ్యమ్యమా | `UUUIIUIUIIIUUUIUUIU` |
| 3 | మృగ్రుస్రుక్రుమతిస్రమమ్యమతమున్మృమ్యాసమమ్రిమ్రమౌ | `UUUIIUIUIIIUUUIUUIU` |
| 4 | మౌగ్రిమ్రిమ్రిమమండిమశ్రదశలల్య్య్మగ్యణ్య మస్రస్ర తై | `UUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.018 · model's first choice kept 32% · constraint overrode 61% · backtracks 0

<details><summary>Token probabilities (126 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.45 · `గ` 0.41 · `్రమ` 1.5e-4✱ · `్రి` 2.0e-3✱ · `క` 0.01 · `్రి` 7.8e-4✱ · `తి` 0.03 · `␣మ` 0.15 · `మ` 0.06✱ · `్య` 4.8e-4✱ · `మ` 0.12 · `గ` 0.02 · `్య` 2.4e-3✱ · `ము` 0.19 · `మ` 0.07 · `మ` 0.09 · `మ` 0.04 · `్ర` 2.5e-3✱ · `్య` 1.9e-3✱ · `్` 4.2e-7✱ · `జ` 0.14✱ · `ప` 0.01 · `్య` 0.01✱ · `మ` 0.19✱ · `్ర` 1.4e-3✱ · `ల` 0.04✱ · `ౌ` 0.03✱ · `మ` 0.08✱ · `మ` 0.14✱ · `్రి` 9.1e-4✱ · `మా` 0.01✱ · `⏎` 0.39 |
| 2 | `మ` 0.54 · `ృ` 7.1e-3✱ · `గ` 8.1e-3✱ · `్రు` 3.2e-4✱ · `క` 0.01✱ · `్యం` 1.4e-4✱ · `␣మ` 0.29 · `మ` 0.17 · `␣మ` 0.19 · `మ` 0.14 · `్య` 5.1e-3✱ · `మ` 0.35 · `మ` 0.23 · `్య` 0.08✱ · `మ` 0.30 · `మ` 0.39 · `మ` 0.28 · `మ` 0.20 · `్య` 6.9e-3✱ · `్య` 0.02✱ · `ే` 2.6e-3✱ · `మ` 0.79 · `త` 0.86 · `్య` 1.8e-3✱ · `ను` 0.82 · `మ` 6.3e-3✱ · `్య` 3.4e-5✱ · `మ` 0.39 · `్య` 8.4e-4✱ · `మా` 0.02✱ · `⏎` 0.49 forced |
| 3 | `మ` 0.58 · `ృ` 0.01✱ · `గ` 8.0e-4✱ · `్రు` 1.4e-4✱ · `స` 0.05✱ · `్రు` 3.0e-4✱ · `క` 0.01✱ · `్రు` 1.4e-4✱ · `మ` 0.77 · `తి` 0.70 · `స` 0.02✱ · `్రమ` 1.5e-4✱ · `మ` 0.02✱ · `్య` 1.8e-4✱ · `మ` 0.77 · `త` 0.94 · `ము` 0.95 · `న్` 0.02✱ · `మ` 6.3e-3✱ · `ృ` 2.4e-3✱ · `మ` 0.05✱ · `్యా` 6.2e-5✱ · `స` 0.44 · `మ` 0.94 · `మ` 5.2e-3✱ · `్రి` 2.4e-3✱ · `మ` 0.88 · `్రమ` 4.6e-5✱ · `ౌ` 2.0e-3✱ · `⏎` 0.09 forced |
| 4 | `మ` 0.10✱ · `ౌ` 3.4e-3✱ · `గ` 6.8e-3✱ · `్రి` 1.1e-3✱ · `మ` 0.81 · `్రి` 0.43 · `మ` 0.01✱ · `్రి` 1.0e-4✱ · `మ` 0.02✱ · `మ` 0.68 · `ండి` 0.02✱ · `మ` 4.9e-3✱ · `శ` 0.05✱ · `్ర` 9.8e-5✱ · `ద` 0.94 · `శ` 3.0e-3✱ · `ల` 0.85 · `ల` 6.1e-3✱ · `్య` 3.8e-4✱ · `్య` 9.1e-4✱ · `్` 1.5e-4✱ · `మ` 0.02✱ · `గ` 0.81 · `్య` 0.04✱ · `ణ` 0.67 · `్య` 5.5e-3✱ · `␣మ` 0.50 · `స` 0.73 · `్ర` 2.8e-4✱ · `స` 0.17✱ · `్ర` 1.1e-3✱ · `␣త` 0.56 · `ై` 5.1e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 111 tokens · 29.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మామల్రోకటి మమ్రవక్రియముమమ్యావయ్వెనుత్యామమా | `UUUIIUIUIIIUUUIUUIU` |
| 2 | త్యామత్యామతృమమ్య దమ్రుతవమమ్యన్యుయ్యమమ్యామకాయ్ | `UUUIIUIUIIIUUUIUUIU` |
| 3 | లోమమ్రద్ర మలక్రు లోన మణినమ్ర్ర్లోనమ్రమమ్యంకమున్ | `UUUIIUIUIIIUUUIUUIU` |
| 4 | మౌమన్రుక్తితితివ్వరవ్వరవతివ్వ్వ్నన్రియ్రియవ్రియ్రియౌ | `UUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 32% · constraint overrode 59% · backtracks 0

<details><summary>Token probabilities (111 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.20 · `మ` 0.11 · `ల` 0.05 · `్రో` 3.4e-5✱ · `క` 0.05 · `టి` 0.14 · `␣మ` 0.31 · `మ` 0.41 · `్ర` 2.9e-4✱ · `వ` 0.21 · `క` 0.10✱ · `్రియ` 5.6e-5✱ · `ము` 0.20 · `మ` 0.05 · `మ` 0.07 · `్యా` 1.8e-3✱ · `వ` 0.02✱ · `య` 0.01✱ · `్వ` 4.0e-5✱ · `ె` 0.05✱ · `ను` 0.02✱ · `త` 0.05 · `్యా` 1.8e-4✱ · `మ` 0.03✱ · `మా` 0.02✱ · `⏎` 0.58 |
| 2 | `త` 0.36 · `్యా` 0.03✱ · `మ` 0.06✱ · `త` 0.15 · `్యా` 0.04✱ · `మ` 0.44 · `త` 0.06 · `ృ` 3.7e-3✱ · `మ` 0.22 · `మ` 0.25 · `్య` 2.3e-3✱ · `␣ద` 0.05 · `మ` 0.09 · `్రు` 4.0e-3✱ · `త` 0.35 · `వ` 0.04 · `మ` 0.06 · `మ` 0.06 · `్య` 0.01✱ · `న్` 6.5e-3✱ · `యు` 0.25 · `య` 0.04 · `్య` 8.2e-4✱ · `మ` 0.77 · `మ` 0.03✱ · `్యా` 0.02✱ · `మ` 2.9e-3✱ · `క` 0.95 · `ాయ` 1.00 · `్` 1.0e-4✱ · `⏎` 0.04✱ forced |
| 3 | `లో` 0.03✱ · `మ` 1.1e-3✱ · `మ` 0.51 · `్ర` 3.5e-5✱ · `ద్ర` 7.3e-3✱ · `␣మ` 0.89 · `ల` 0.98 · `క` 0.99 · `్రు` 4.1e-5✱ · `␣లో` 0.95 · `న` 0.98 · `␣మ` 0.99 · `ణి` 5.3e-6✱ · `న` 0.60 · `మ` 0.89 · `్ర` 5.3e-5✱ · `్ర` 9.4e-4✱ · `్` 1.7e-7✱ · `లో` 1.3e-3✱ · `న` 0.02✱ · `మ` 0.24✱ · `్రమ` 2.6e-4✱ · `మ` 0.12✱ · `్యం` 4.6e-4✱ · `క` 0.66 · `ము` 0.97 · `న్` 0.99 · `⏎` 0.83 |
| 4 | `మ` 0.97 · `ౌ` 1.00 · `మన` 1.1e-3✱ · `్రు` 2.0e-5✱ · `క్తి` 2.4e-5✱ · `తి` 3.7e-4✱ · `తి` 0.01✱ · `వ` 3.6e-3✱ · `్వర` 2.2e-3✱ · `వ` 1.9e-3✱ · `్వర` 1.4e-4✱ · `వ` 6.9e-3✱ · `తి` 0.05✱ · `వ` 0.02✱ · `్వ` 1.6e-4✱ · `్` 7.1e-5✱ · `వ` 8.5e-4✱ · `్` 4.3e-5✱ · `న` 4.0e-4✱ · `న` 5.4e-3✱ · `్రియ` 4.5e-4✱ · `్రియ` 0.02✱ · `వ` 0.01✱ · `్రియ` 4.4e-3✱ · `్రియ` 2.4e-3✱ · `ౌ` 8.1e-4✱ |

</details>

[↑ meters](#meters)

---

<a id="sragdhara"></a>

## 5. స్రగ్ధర (sragdhara)

```text
Meter: స్రగ్ధర (sragdhara), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: మ ర భ న య య య, i.e. UUU UIU UII III IUU IUU IUU (21 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 8th and the 15th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter స్రగ్ధర (sragdhara).

Meter: స్రగ్ధర (sragdhara), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: మ ర భ న య య య, i.e. UUU UIU UII III IUU IUU IUU (21 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 8th and the 15th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 170 tokens · 44.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మక్రిమ్యమ్యుగ్యమర్రిమ్రమ మత ల లరన్ర్ర్మక్రిమమ్యుగ్య్యమమ్రిమ్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 2 | మక్రిల్రన్రమ్రి మిమ్య్యుగ్య్య్మమమమమత లల్య్య్మమ్రికమ్యమ్యుమగ్యమ్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 3 | మక్రిమ్రహ్యల్రనమ్రిమ్ ల్య్మయయయయయవయ్మయ్మమమ్యుమ్యరభ్రయ్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 4 | ఉక్రిమ్యుమ్య్రగ్ధరర్రర్ర్ర్యు గణ మ ర భ నయ్యుయ్యయయ్యుయ్యయయ్యుయ్ | `UUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 27% · repeated lines 0 · mean token probability (geometric) 0.031 · model's first choice kept 34% · constraint overrode 56% · backtracks 0

<details><summary>Token probabilities (170 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.54 · `క` 0.02 · `్రి` 1.8e-3✱ · `మ` 0.32 · `్య` 9.5e-4✱ · `మ` 0.30 · `్య` 2.9e-3✱ · `ు` 0.04 · `గ` 0.02 · `్య` 0.01✱ · `మ` 0.37 · `ర` 0.03 · `్రి` 1.4e-5✱ · `మ` 0.22 · `్ర` 3.6e-3✱ · `మ` 0.17 · `␣మ` 0.13 · `త` 0.02 · `␣ల` 0.04 · `␣ల` 0.04 · `ర` 0.02 · `న` 0.02 · `్ర` 5.0e-6✱ · `్ర` 1.3e-4✱ · `్` 3.1e-4✱ · `మ` 0.12✱ · `క` 0.30 · `్రి` 0.15✱ · `మ` 0.68 · `మ` 0.74 · `్య` 0.63 · `ు` 0.79 · `గ` 0.56 · `్య` 0.45 · `్య` 0.09 · `మ` 0.15 · `మ` 0.22 · `్రి` 0.11✱ · `మ` 0.25 · `్` 0.03✱ · `⏎` 3.6e-3✱ forced |
| 2 | `మ` 0.20 · `క` 2.9e-3✱ · `్రి` 0.02✱ · `ల` 0.13✱ · `్ర` 1.2e-3✱ · `న` 0.68 · `్ర` 1.3e-4✱ · `మ` 0.76 · `్రి` 7.3e-4✱ · `␣మ` 0.22 · `ి` 3.9e-3 · `మ` 0.36 · `్య` 4.4e-3✱ · `్య` 0.85 · `ు` 0.88 · `గ` 0.82 · `్య` 0.73 · `్య` 2.5e-3✱ · `్` 2.0e-4✱ · `మ` 0.43 · `మ` 0.72 · `మ` 0.29 · `మ` 0.73 · `మ` 0.15 · `త` 0.65 · `␣ల` 0.59 · `ల` 0.03✱ · `్య` 1.7e-3✱ · `్య` 6.8e-3✱ · `్` 1.4e-7✱ · `మ` 0.11✱ · `మ` 0.09✱ · `్రి` 5.7e-3✱ · `క` 0.67 · `మ` 0.20✱ · `్య` 2.5e-3✱ · `మ` 0.53 · `్య` 0.03✱ · `ు` 0.61 · `మ` 0.21 · `గ` 0.50 · `్య` 0.63 · `మ` 0.76 · `్` 5.6e-4✱ · `⏎` 0.08✱ forced |
| 3 | `మ` 0.86 · `క` 0.81 · `్రి` 0.95 · `మ` 0.78 · `్రహ` 1.2e-5✱ · `్య` 4.5e-3✱ · `ల` 0.98 · `్ర` 1.0e-3✱ · `న` 0.94 · `మ` 0.53 · `్రి` 0.02✱ · `మ` 7.2e-5✱ · `్` 2.9e-4✱ · `␣ల` 5.3e-4✱ · `్య` 3.6e-4✱ · `్` 2.3e-3✱ · `మ` 0.10✱ · `య` 0.01✱ · `య` 2.3e-3✱ · `య` 0.11✱ · `య` 0.05✱ · `య` 0.03✱ · `వ` 1.9e-3✱ · `య` 0.01✱ · `్` 2.6e-3✱ · `మ` 8.7e-3✱ · `య` 0.07✱ · `్` 2.4e-3✱ · `మ` 1.8e-3✱ · `మ` 6.0e-3✱ · `మ` 0.02✱ · `్య` 8.2e-3✱ · `ు` 0.30 · `మ` 0.05✱ · `్య` 2.1e-3✱ · `ర` 0.92 · `భ` 9.1e-3✱ · `్ర` 5.7e-3✱ · `య` 0.99 · `్` 1.6e-5✱ · `⏎` 0.03✱ forced |
| 4 | `␣` 0.25 · `ఉ` 4.4e-4✱ · `క` 2.9e-3✱ · `్రి` 5.7e-4✱ · `మ` 6.4e-4✱ · `్య` 4.3e-3✱ · `ు` 0.19 · `మ` 0.42 · `్య` 5.3e-3✱ · `్ర` 0.25✱ · `గ్` 0.98 · `ధ` 0.97 · `ర` 0.98 · `ర` 2.2e-3✱ · `్ర` 1.1e-3✱ · `ర` 0.07✱ · `్ర` 0.01✱ · `్ర` 0.03✱ · `్య` 2.6e-3✱ · `ు` 0.15✱ · `␣గ` 0.02✱ · `ణ` 0.30 · `␣మ` 0.95 · `␣ర` 0.87 · `␣భ` 0.97 · `␣న` 0.86 · `య` 9.0e-3✱ · `్య` 2.9e-5✱ · `ు` 3.6e-4✱ · `య` 0.02✱ · `్య` 0.05✱ · `య` 0.57 · `య` 0.12✱ · `్య` 5.9e-3✱ · `ు` 0.15✱ · `య` 0.04✱ · `్య` 0.34 · `య` 0.21✱ · `య` 0.72 · `్య` 0.06✱ · `ు` 0.35✱ · `య` 0.08✱ · `్` 2.4e-4✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 160 tokens · 48.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రా సీమల్రూ మ జల్యమ్రమ న యల జెడుశ్రామలంద్రూ మ జల్యల్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 2 | న్య్య్యే సీరా సీమలల్రల్య్య్యి వమ న యల జెడ్య్ర్రీలలూ మల్య్యలక్ష్ల్లిణ్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 3 | ల్ల్నే సుగ్యల్లల్యణణ్యస్ర్ధ్నినినితితితితింటిన్య్య్య లల్యల్య నుల్యణ్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 4 | మ్ర్ర్రో సిల్ మల్యం లలల్య్యల్ల్య్మొడుడు పుల మయుశ్స్మ్యోరధర్రహ్ అకల్యా | `UUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 32% · repeated lines 0 · mean token probability (geometric) 0.009 · model's first choice kept 25% · constraint overrode 66% · backtracks 0

<details><summary>Token probabilities (160 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.09 · `␣సీ` 0.06 · `మ` 0.03 · `ల` 0.11 · `్ర` 8.7e-5✱ · `ూ` 1.3e-3 · `␣మ` 0.02 · `␣జ` 0.04 · `ల` 0.14 · `్య` 2.5e-4✱ · `మ` 0.07✱ · `్ర` 5.3e-3✱ · `మ` 0.03 · `␣న` 0.11 · `␣య` 0.12 · `ల` 0.03 · `␣జ` 0.01 · `ె` 0.05 · `డు` 8.8e-4✱ · `శ` 7.1e-3✱ · `్రా` 1.6e-4✱ · `మ` 0.93 · `ల` 0.95 · `ంద్ర` 3.0e-3✱ · `ూ` 0.73 · `␣మ` 0.96 · `␣జ` 0.98 · `ల` 0.98 · `్య` 0.99 · `ల` 0.02 · `్` 3.9e-6✱ · `⏎` 2.1e-4✱ forced |
| 2 | `న` 0.53 · `్య` 1.5e-3✱ · `్య` 5.0e-4✱ · `్య` 1.2e-3✱ · `ే` 9.4e-3✱ · `␣సీ` 0.01✱ · `రా` 0.20 · `␣సీ` 0.76 · `మ` 0.68 · `ల` 0.79 · `ల` 6.2e-4✱ · `్ర` 1.7e-3✱ · `ల` 6.9e-3✱ · `్య` 4.3e-4✱ · `్య` 3.6e-3✱ · `్య` 0.47 · `ి` 5.2e-4✱ · `␣వ` 0.04✱ · `మ` 0.82 · `␣న` 0.84 · `␣య` 0.69 · `ల` 0.90 · `␣జ` 0.93 · `ె` 0.88 · `డ` 2.3e-4✱ · `్య` 4.2e-3✱ · `్ర` 0.01✱ · `్ర` 1.6e-4✱ · `ీల` 5.8e-4✱ · `ల` 1.9e-3✱ · `ూ` 0.97 · `␣మ` 0.99 · `ల` 3.1e-3✱ · `్య` 7.8e-4✱ · `్య` 0.90 · `ల` 0.89 · `క్ష్` 0.98 · `ల్ల` 1.3e-5✱ · `ి` 6.7e-5✱ · `ణ` 1.6e-3✱ · `్` 0.04✱ · `⏎` 0.10✱ |
| 3 | `␣` 0.58 · `ల్ల` 1.0e-4✱ · `్` 4.1e-4✱ · `నే` 5.2e-4✱ · `␣` 9.0e-5✱ · `సు` 1.5e-4✱ · `గ` 4.4e-5✱ · `్య` 8.0e-6✱ · `ల్ల` 8.5e-3✱ · `ల` 1.0e-3✱ · `్య` 2.2e-3✱ · `ణ` 0.44 · `ణ` 0.04✱ · `్య` 0.01✱ · `స` 0.03✱ · `్ర` 0.76 · `్` 3.3e-4✱ · `ధ` 0.97 · `్` 1.4e-6✱ · `ని` 2.3e-4✱ · `ని` 4.1e-3✱ · `ని` 0.06✱ · `తి` 5.8e-3✱ · `తి` 0.08✱ · `తి` 0.83 · `తి` 0.25 · `ంటి` 1.3e-4✱ · `న` 1.2e-3✱ · `్య` 1.0e-4✱ · `్య` 0.20 · `్య` 0.19✱ · `␣` 6.8e-3✱ · `ల` 2.5e-3✱ · `ల` 0.05✱ · `్య` 2.5e-3✱ · `ల` 0.02✱ · `్య` 7.2e-4✱ · `␣` 0.03✱ · `ను` 3.4e-4✱ · `ల` 0.05✱ · `్య` 0.13 · `ణ` 0.64 · `్` 3.9e-3✱ · `⏎` 0.97 |
| 4 | `మ` 0.99 · `్ర` 5.9e-5✱ · `్ర` 1.9e-4✱ · `్ర` 3.5e-3✱ · `ో` 6.7e-5✱ · `␣` 1.4e-3✱ · `సి` 7.7e-4✱ · `ల` 0.01✱ · `్` 1.9e-4✱ · `␣మ` 0.01✱ · `ల` 2.6e-3✱ · `్యం` 1.9e-3✱ · `␣ల` 7.2e-3✱ · `ల` 0.02✱ · `ల` 6.5e-3✱ · `్య` 1.3e-3✱ · `్య` 0.14 · `ల్ల` 4.3e-5✱ · `్య` 5.7e-3✱ · `్` 4.9e-5✱ · `మ` 3.0e-3✱ · `ొ` 8.0e-6✱ · `డు` 6.1e-3✱ · `డు` 0.51 · `␣పు` 8.6e-4✱ · `ల` 0.06✱ · `␣మ` 9.1e-3✱ · `యు` 0.13✱ · `శ్` 9.2e-5✱ · `స్` 2.2e-3✱ · `మ` 1.6e-3✱ · `్య` 4.6e-3✱ · `ో` 4.1e-3✱ · `ర` 0.01✱ · `ధ` 0.98 · `ర` 1.00 · `్రహ్` 1.6e-6✱ · `␣` 0.98 · `అ` 3.6e-5✱ · `క` 7.2e-3✱ · `ల` 7.3e-3✱ · `్యా` 5.4e-5✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 150 tokens · 64.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ్రాంతశ్రీ శలల్లడ్ర్వ్గలనుమవ శమమ్య్య్కల్యళం విత్రివర్శార్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 2 | శమ్రాగానేస సంద్రద్ర్ర్జడెను జమలరశ్యమ్యమమ్రాముముమ్యమ్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 3 | లౌమ్రన్ మమ్రామగమ్యమ్య్య్లమును జయమరన్ ల్లల్ల నేనుల్లకుల్లల్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 4 | స్రమ్రర్ర్ర్రల్ర్రర్ర రభ్రయ్య్య్లమునిన మయుగమ్య్య్లమ్ ట్టిగా వల్ల వార్డుల్ | `UUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.009 · model's first choice kept 29% · constraint overrode 62% · backtracks 30

<details><summary>Token probabilities (150 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.96 · `మ` 0.99 · `్రా` 1.1e-5✱ · `ంత` 0.05 · `శ` 9.7e-3✱ · `్రీ` 9.8e-3✱ · `␣శ` 0.03 · `ల` 0.04✱ · `ల్ల` 7.5e-3✱ · `డ` 0.90 · `్ర` 2.4e-4✱ · `్వ` 2.0e-3✱ · `్` 2.3e-5✱ · `గ` 0.09✱ · `ల` 2.9e-3 · `ను` 0.88 · `మ` 0.44 · `వ` 2.3e-3 · `␣శ` 2.2e-4 · `మ` 0.18 · `మ` 0.88 · `్య` 0.97 · `్య` 2.8e-4✱ · `్` 1.5e-5✱ · `క` 0.78 · `ల` 0.82 · `్య` 2.4e-5✱ · `ళ` 7.1e-4✱ · `ం` 0.04 · `␣వ` 6.5e-3 · `ిత` 4.8e-3 · `్రి` 0.76 · `వర్` 0.99 · `శ` 1.0e-2 · `ార్` 2.0e-4 · `⏎` 0.85 |
| 2 | `శ` 0.85 · `మ` 0.89 · `్రా` 0.94 · `గానే` 3.8e-5 · `స` 1.3e-3 · `␣స` 0.42 · `ంద్ర` 8.5e-4✱ · `ద్ర` 0.85 · `్ర` 4.2e-6✱ · `్` 4.0e-7✱ · `జ` 7.8e-3✱ · `డ` 0.99 · `ె` 1.00 · `ను` 0.80 · `␣జ` 0.32 · `మ` 0.74 · `ల` 3.7e-4✱ · `ర` 0.96 · `శ` 9.6e-3✱ · `్య` 2.8e-4✱ · `మ` 0.75 · `్య` 4.4e-5✱ · `మ` 0.59 · `మ` 0.04✱ · `్రా` 3.0e-5✱ · `ము` 0.37 · `ము` 0.28 · `మ` 0.14✱ · `్య` 2.1e-4✱ · `మ` 0.06✱ · `్` 3.0e-7✱ · `⏎` 0.02✱ forced |
| 3 | `ల` 4.0e-3✱ · `ౌ` 5.3e-4✱ · `మ` 2.2e-4✱ · `్ర` 3.1e-5✱ · `న్` 0.98 · `␣మ` 0.82 · `మ` 0.76 · `్రా` 1.1e-4✱ · `మ` 0.98 · `గ` 1.00 · `మ` 2.3e-3✱ · `్య` 1.3e-4✱ · `మ` 7.3e-3✱ · `్య` 1.1e-4✱ · `్య` 1.4e-7✱ · `్` 9.6e-6✱ · `ల` 5.2e-3✱ · `ము` 0.99 · `ను` 0.99 · `␣జ` 0.94 · `య` 0.83 · `మ` 0.94 · `ర` 0.99 · `న్` 2.9e-3✱ · `␣` 2.4e-5✱ · `ల్ల` 4.7e-4✱ · `ల్ల` 3.2e-3✱ · `␣` 1.4e-3✱ · `నే` 6.4e-4✱ · `ను` 0.02✱ · `ల్ల` 9.4e-4✱ · `కు` 0.01✱ · `ల్ల` 0.01✱ · `ల` 9.6e-3✱ · `్` 2.8e-4✱ · `⏎` 0.57 |
| 4 | `స` 0.05✱ · `్ర` 1.4e-3✱ · `మ` 0.02✱ · `్ర` 2.5e-4✱ · `ర` 0.94 · `్ర` 5.6e-5✱ · `్ర` 0.04✱ · `్ర` 0.05✱ · `ల` 7.1e-3✱ · `్ర` 4.8e-3✱ · `్ర` 0.07 · `ర` 0.11✱ · `్ర` 4.5e-4✱ · `␣ర` 0.49 · `భ` 3.0e-3✱ · `్ర` 9.9e-3✱ · `య` 0.11✱ · `్య` 1.0e-3✱ · `్య` 0.03✱ · `్` 5.2e-4✱ · `ల` 0.05✱ · `ము` 0.26✱ · `ని` 5.8e-3✱ · `న` 0.02✱ · `␣మ` 0.02✱ · `యు` 0.27 · `గ` 0.03✱ · `మ` 0.01✱ · `్య` 0.13✱ · `్య` 8.3e-3✱ · `్` 1.5e-3✱ · `ల` 3.0e-3✱ · `మ` 0.85 · `్` 8.1e-3✱ · `␣` 1.4e-4✱ · `ట్టి` 1.2e-6✱ · `గా` 4.7e-4✱ · `␣` 1.0e-3✱ · `వ` 1.7e-5✱ · `ల్ల` 9.7e-4✱ · `␣` 2.3e-4✱ · `వా` 9.3e-3✱ · `ర్` 1.1e-3✱ · `డు` 2.5e-3✱ · `ల` 0.01✱ · `్` 6.2e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 144 tokens · 54.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిత్యాగమ్యయుప్రాంతముణికలొ నిడల్య్వ్తస్రవమ్యూతియెక్యం | `UUUUIUUIIIIIIUUIUUIUU` |
| 2 | కల్లీ మూర్చమ్రగక్రుడ్య్య్గతిముకతమ ప్రేమ్య్య్గయ్రదిన్లే కమమ్యా | `UUUUIUUIIIIIIUUIUUIUU` |
| 3 | మల్లేలో మించినద్యాడ్ర్ర్మ కము క్షమమముప్య్ర్మమ్యతిందుప్య ఉన్నన్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 4 | గౌ ల్లడ్రిన్ర్రగ్ధరవ్రత్య్య్గ య మ గతిని ఖచ్చ్ర్గాటి చేస్తిన్రు పద్యం | `UUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 16% · repeated lines 0 · mean token probability (geometric) 0.005 · model's first choice kept 43% · constraint overrode 53% · backtracks 30

<details><summary>Token probabilities (144 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.95 · `ల్లి` 0.96 · `త` 0.99 · `్యా` 1.00 · `గ` 1.00 · `మ` 0.97 · `్య` 0.85 · `యు` 3.4e-3 · `ప` 0.82 · `్రా` 0.65 · `ంత` 0.96 · `ము` 0.75 · `ణ` 4.8e-4 · `ిక` 0.87 · `ల` 0.74 · `ొ` 0.05✱ · `␣ని` 0.94 · `డ` 0.99 · `ల` 0.96 · `్య` 0.98 · `్వ` 5.0e-5✱ · `్` 2.5e-6✱ · `త` 0.02✱ · `స` 2.6e-3✱ · `్ర` 0.33 · `వ` 1.00 · `మ` 0.88 · `్యూ` 2.2e-6✱ · `తి` 0.98 · `య` 0.93 · `ె` 0.94 · `క` 0.01✱ · `్యం` 2.4e-7✱ · `⏎` 0.05✱ forced |
| 2 | `క` 0.95 · `ల్` 0.84 · `లీ` 0.87 · `␣మ` 0.16 · `ూర్` 0.97 · `చ` 0.65 · `మ` 0.06 · `్ర` 2.4e-6✱ · `గ` 0.96 · `క` 0.02✱ · `్రు` 4.2e-6✱ · `డ` 0.09✱ · `్య` 1.9e-3✱ · `్య` 1.4e-5✱ · `్` 2.6e-9✱ · `గ` 4.6e-3✱ · `తి` 0.97 · `ము` 0.44 · `క` 1.9e-3✱ · `త` 0.85 · `మ` 0.71 · `␣ప్రేమ` 0.96 · `్య` 1.1e-5✱ · `్య` 1.2e-5✱ · `్` 1.2e-7✱ · `గ` 4.7e-3✱ · `య` 1.7e-3✱ · `్ర` 9.9e-6✱ · `ది` 0.77 · `న్` 2.3e-5✱ · `లే` 0.87 · `␣` 0.52 · `క` 1.6e-3✱ · `మ` 0.86 · `మ` 4.4e-4✱ · `్యా` 4.9e-5✱ · `⏎` 0.04 forced |
| 3 | `మ` 0.92 · `ల్` 1.3e-5✱ · `లే` 2.4e-4✱ · `లో` 0.77 · `␣మ` 0.96 · `ించిన` 0.99 · `ద` 5.9e-5✱ · `్యా` 3.4e-6✱ · `డ` 2.3e-3✱ · `్ర` 1.3e-5✱ · `్ర` 4.8e-6✱ · `్` 1.8e-7✱ · `మ` 6.8e-4✱ · `␣` 0.67 · `క` 2.0e-3✱ · `ము` 2.4e-3✱ · `␣క్ష` 0.05✱ · `మ` 1.00 · `మ` 2.9e-3✱ · `ము` 2.0e-3✱ · `ప` 0.01✱ · `్య` 1.6e-7✱ · `్ర` 3.3e-7✱ · `్` 4.4e-4✱ · `మ` 6.7e-4✱ · `మ` 2.4e-3✱ · `్య` 2.7e-3✱ · `తి` 0.93 · `ందు` 1.1e-5✱ · `ప` 0.77 · `్య` 3.6e-4✱ · `␣ఉన్న` 0.91 · `న` 2.8e-3✱ · `్` 1.4e-9✱ · `⏎` 0.07✱ forced |
| 4 | `గ` 0.04✱ · `ౌ` 1.1e-3✱ · `␣` 1.2e-5✱ · `ల` 3.0e-3✱ · `్` 9.2e-10✱ · `ల` 1.5e-4✱ · `డ` 6.5e-5✱ · `్ర` 4.7e-5✱ · `ిన` 0.97 · `్ర` 2.3e-4✱ · `్ర` 0.94 · `గ్` 0.94 · `ధ` 0.91 · `ర` 0.97 · `వ` 2.2e-4✱ · `్ర` 2.0e-4✱ · `త` 0.05✱ · `్య` 2.9e-6✱ · `్య` 1.5e-3✱ · `్` 1.3e-6✱ · `గ` 2.2e-4✱ · `␣య` 0.46 · `␣మ` 2.7e-4✱ · `␣గ` 0.97 · `తి` 1.00 · `ని` 0.99 · `␣ఖ` 1.00 · `చ్చ` 1.00 · `్ర` 6.7e-8✱ · `్` 7.6e-12✱ · `గా` 1.3e-7✱ · `టి` 0.98 · `␣చేస్త` 3.3e-4✱ · `ిన` 1.2e-3✱ · `్రు` 1.8e-4✱ · `␣ప` 0.97 · `ద్య` 0.97 · `ం` 0.85 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 135 tokens · 40.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నిమ్రిమ్రమ్యమ్రమమ్రమ్య్య్ని మమత మముముత్య్మ్నిమ్య తమ్యమ్య్య ముల్యా | `UUUUIUUIIIIIIUUIUUIUU` |
| 2 | త్యామ్రిమ్రిమ్రిమ్య తవ్యంమ్య మమత మము లోక్యం మమమ్రిత్రిమమ్యా | `UUUUIUUIIIIIIUUIUUIUU` |
| 3 | త్రిమ్రత్య్యంమ్యమ్యతమ్యమ్య్య్యృతగమనికకుస్ర్రించరఛ్యస్సు మమ్యా | `UUUUIUUIIIIIIUUIUUIUU` |
| 4 | నమ్రయ్యమ్యాలతో కూడ్యలకలు అడిగిన్యాల క్రమ్రమ్ర మారా | `UUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.020 · model's first choice kept 38% · constraint overrode 57% · backtracks 0

<details><summary>Token probabilities (135 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ని` 0.05 · `మ` 0.09 · `్రి` 3.9e-4✱ · `మ` 0.10✱ · `్ర` 3.1e-3✱ · `మ` 0.24 · `్య` 2.1e-3✱ · `మ` 0.20 · `్ర` 5.5e-3✱ · `మ` 0.38 · `మ` 0.17 · `్ర` 7.3e-3✱ · `మ` 0.78 · `్య` 0.02✱ · `్య` 1.8e-3✱ · `్` 5.4e-6✱ · `ని` 0.04✱ · `␣మ` 0.47 · `మ` 0.20 · `త` 0.44 · `␣మ` 0.13 · `ము` 0.17 · `ము` 7.3e-4✱ · `త` 7.2e-3✱ · `్య` 5.1e-7✱ · `్` 3.3e-6✱ · `మ` 0.91 · `్` 7.6e-4✱ · `ని` 1.8e-3✱ · `మ` 0.50 · `్య` 4.0e-3✱ · `␣త` 0.30 · `మ` 0.73 · `్య` 2.1e-3✱ · `మ` 0.11✱ · `్య` 0.02✱ · `్య` 0.68 · `␣మ` 0.33 · `ు` 0.79 · `ల` 6.1e-4✱ · `్యా` 5.4e-5✱ · `⏎` 3.5e-4 forced |
| 2 | `త` 0.82 · `్యా` 3.1e-3✱ · `మ` 1.7e-3✱ · `్రి` 1.8e-4✱ · `మ` 0.03✱ · `్రి` 9.6e-3✱ · `మ` 0.86 · `్రి` 9.8e-4✱ · `మ` 0.93 · `్య` 1.5e-3✱ · `␣త` 0.23 · `వ` 0.63 · `్యం` 3.4e-3✱ · `మ` 0.68 · `్య` 0.37✱ · `␣మ` 0.44 · `మ` 0.83 · `త` 0.19✱ · `␣మ` 0.83 · `ము` 0.81 · `␣లో` 8.6e-3✱ · `క` 0.80 · `్యం` 4.4e-4✱ · `␣మ` 0.02✱ · `మ` 0.14 · `మ` 0.21✱ · `్రి` 0.04✱ · `త` 0.24 · `్రి` 8.2e-3✱ · `మ` 0.82 · `మ` 0.93 · `్యా` 1.5e-3✱ · `⏎` 3.8e-3 forced |
| 3 | `త్రి` 0.10✱ · `మ` 0.96 · `్ర` 6.3e-6✱ · `త` 0.02✱ · `్య` 1.1e-5✱ · `్యం` 0.84 · `మ` 0.95 · `్య` 0.90 · `మ` 3.3e-3✱ · `్య` 1.7e-5✱ · `త` 0.77 · `మ` 0.06✱ · `్య` 2.5e-3✱ · `మ` 0.04✱ · `్య` 0.41 · `్య` 2.3e-3✱ · `్య` 1.7e-4✱ · `ృత` 2.1e-8✱ · `గ` 0.60 · `మని` 0.92 · `క` 0.96 · `కు` 1.4e-3✱ · `స` 2.3e-3✱ · `్ర` 0.96 · `్ర` 1.5e-3✱ · `ించ` 6.1e-5✱ · `ర` 0.94 · `ఛ` 0.01✱ · `్య` 6.7e-5✱ · `స్సు` 0.38 · `␣మ` 1.2e-3✱ · `మ` 0.93 · `్యా` 5.2e-4✱ · `⏎` 2.2e-3✱ forced |
| 4 | `న` 0.70 · `మ` 0.04✱ · `్ర` 1.0e-3✱ · `య` 0.12✱ · `్య` 5.4e-3✱ · `మ` 0.42 · `్య` 1.0e-3✱ · `ాలతో` 0.77 · `␣కూ` 0.97 · `డ` 3.9e-3✱ · `్య` 1.3e-3✱ · `ల` 0.02✱ · `క` 8.7e-3✱ · `లు` 2.6e-3✱ · `␣అ` 0.96 · `డి` 0.97 · `గిన` 0.90 · `్య` 6.4e-8✱ · `ాల` 0.99 · `␣క్ర` 0.99 · `మ` 1.2e-3✱ · `్ర` 9.2e-4✱ · `మ` 0.01✱ · `్ర` 7.7e-4✱ · `␣మ` 2.2e-3✱ · `ారా` 4.7e-3✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 148 tokens · 40.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ్రిల్రున్ కమ్రిలౌ సమ్ర్ర్క మ మమ యటునుక్యమ్రిలౌన్ కమ్రిలౌ సే | `UUUUIUUIIIIIIUUIUUIUU` |
| 2 | స్ర్కమ్రమ్యట్రుక్యమమ్రిల్య్య్గ లల ల సమసస్కమ్రమల్యట్రునక్యా | `UUUUIUUIIIIIIUUIUUIUU` |
| 3 | మమ్రిన్ కమ్రిల్య సమ్ర్ర్కమ్రమమమ ము ల్య్య మమ్యల్యు ఈలౌన సమ్మం | `UUUUIUUIIIIIIUUIUUIUU` |
| 4 | శ్రీమ్రమ్రభ్రయ్రియయ్రియ్రియయయయయయయ్య్య్యృయ్యయశ్యున్ననంగా | `UUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 10% · single-akshara words 24% · repeated lines 0 · mean token probability (geometric) 0.026 · model's first choice kept 39% · constraint overrode 53% · backtracks 0

<details><summary>Token probabilities (148 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.06 · `మ` 0.16 · `్రి` 2.4e-5✱ · `ల` 0.10 · `్రు` 9.5e-5✱ · `న్` 0.04 · `␣క` 0.10 · `మ` 0.31 · `్రి` 1.5e-4✱ · `ల` 0.70 · `ౌ` 0.03 · `␣స` 0.03 · `మ` 0.27✱ · `్ర` 7.3e-4✱ · `్ర` 1.8e-4✱ · `్` 1.9e-7✱ · `క` 7.4e-3✱ · `␣మ` 0.12 · `␣మ` 0.05 · `మ` 0.07 · `␣య` 0.19 · `ట` 0.08 · `ు` 0.52 · `ను` 0.02✱ · `క` 2.5e-3✱ · `్య` 3.9e-5✱ · `మ` 0.88 · `్రి` 0.67 · `ల` 0.81 · `ౌ` 0.68 · `న్` 0.63 · `␣క` 0.56 · `మ` 0.90 · `్రి` 0.50 · `ల` 0.87 · `ౌ` 0.89 · `␣సే` 2.3e-3 · `⏎` 1.0e-3 forced |
| 2 | `స` 0.29 · `్ర` 0.63 · `్` 0.37 · `క` 0.80 · `మ` 0.07✱ · `్ర` 1.3e-4✱ · `మ` 0.85 · `్య` 4.2e-3✱ · `ట` 0.97 · `్రు` 1.2e-3✱ · `క` 5.3e-3✱ · `్య` 1.3e-3✱ · `మ` 0.47 · `మ` 0.89 · `్రి` 0.21✱ · `ల` 0.77 · `్య` 7.1e-5✱ · `్య` 0.03✱ · `్` 4.5e-3✱ · `గ` 8.7e-3✱ · `␣ల` 0.06 · `ల` 0.54 · `␣ల` 0.03✱ · `␣స` 0.44 · `మ` 0.92 · `స` 0.94 · `స` 1.6e-4✱ · `్` 0.95 · `క` 0.97 · `మ` 0.91 · `్ర` 0.93 · `మ` 0.98 · `ల్య` 8.9e-4✱ · `ట` 0.99 · `్రు` 0.78 · `న` 0.45 · `క` 0.77 · `్యా` 0.03✱ · `⏎` 1.6e-3 forced |
| 3 | `మ` 0.58 · `మ` 5.5e-3✱ · `్రి` 8.5e-5✱ · `న్` 0.99 · `␣క` 0.59 · `మ` 0.98 · `్రి` 0.44 · `ల` 0.98 · `్య` 4.9e-6✱ · `␣స` 0.78 · `మ` 0.99 · `్ర` 2.7e-5✱ · `్ర` 0.99 · `్` 0.99 · `క` 0.98 · `మ` 0.90 · `్ర` 0.99 · `మ` 0.99 · `మ` 2.2e-4✱ · `మ` 4.8e-3✱ · `␣` 0.60 · `ము` 4.4e-5✱ · `␣` 5.8e-3✱ · `ల` 5.1e-4✱ · `్య` 6.4e-3✱ · `్య` 0.02✱ · `␣మ` 0.01✱ · `మ` 0.03✱ · `్య` 0.02✱ · `ల` 1.5e-3✱ · `్య` 5.5e-4✱ · `ు` 2.3e-3✱ · `␣ఈ` 9.4e-3✱ · `ల` 4.4e-3✱ · `ౌ` 0.08✱ · `న` 1.8e-3✱ · `␣స` 2.7e-3✱ · `మ్మ` 0.05✱ · `ం` 5.9e-4✱ · `⏎` 0.20✱ forced |
| 4 | `శ` 0.02✱ · `్రీ` 0.31 · `మ` 0.59 · `్రమ` 1.0e-4✱ · `్ర` 6.0e-4✱ · `భ` 5.9e-3✱ · `్ర` 3.9e-3✱ · `య` 0.10✱ · `్రియ` 8.4e-4✱ · `య` 0.11✱ · `్రియ` 2.1e-3✱ · `్రియ` 6.8e-4✱ · `య` 0.04✱ · `య` 0.03✱ · `య` 0.16✱ · `య` 0.12✱ · `య` 0.17✱ · `య` 6.4e-3✱ · `్య` 1.2e-4✱ · `్య` 8.2e-3✱ · `్య` 0.03✱ · `ృ` 1.4e-5✱ · `య` 9.4e-3✱ · `్య` 0.01✱ · `య` 0.96 · `శ` 5.1e-5✱ · `్య` 9.7e-4✱ · `ు` 4.0e-3✱ · `న్న` 1.1e-3✱ · `న` 5.0e-3✱ · `ంగా` 1.2e-3✱ |

</details>

[↑ meters](#meters)

---

<a id="mahasragdhara"></a>

## 6. మహాస్రగ్ధర (mahasragdhara)

```text
Meter: మహాస్రగ్ధర (mahasragdhara), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas: స త త న స ర ర గురువు, i.e. IIU UUI UUI III IIU UIU UIU U (22 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th and the 16th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter మహాస్రగ్ధర (mahasragdhara).

Meter: మహాస్రగ్ధర (mahasragdhara), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas: స త త న స ర ర గురువు, i.e. IIU UUI UUI III IIU UIU UIU U (22 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th and the 16th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 160 tokens · 53.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మల్యుశ్రుగ్య పౌరన్ర్య్క శకము గెలుచుట్య్య్కమ్య హన్ విభ్రమల్యా | `IIUUUIUUIIIIIIUUIUUIUU` |
| 2 | కమ లక్ష్మిక్రిమ్య సీతన్ జ్య్య్కమును జెవణెడుడ్య్య్కక్ష్మకమ్య్యత్యనుర్యుట్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 3 | డుము ట్టిత్రియ్యయ్యయయ్యయ్య్య్లు ఇ వ్ర స స త తన్ర్ర్లుల్రలల్రల్యముఘ్యం | `IIUUUIUUIIIIIIUUIUUIUU` |
| 4 | ఉ మనం ఉల్లల్ల్య ల్యర్దయ్యునునునునునునున్య్నుమ్రమత్తస్రగధ్రై | `IIUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 29% · repeated lines 0 · mean token probability (geometric) 0.008 · model's first choice kept 19% · constraint overrode 74% · backtracks 0

<details><summary>Token probabilities (160 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.03✱ · `మ` 0.21 · `␣మ` 0.01 · `ల` 0.57 · `్య` 7.4e-4✱ · `ు` 0.02✱ · `శ` 8.6e-3✱ · `్రు` 0.01✱ · `గ` 0.01 · `్య` 6.9e-3✱ · `␣ప` 6.5e-3 · `ౌ` 0.08✱ · `ర` 0.14 · `న` 0.03✱ · `్ర` 1.5e-4✱ · `్య` 7.9e-4✱ · `్` 2.6e-7✱ · `క` 0.02✱ · `␣శ` 0.05 · `క` 0.01✱ · `ము` 0.04 · `␣గ` 4.2e-3✱ · `ె` 0.15 · `లు` 0.43 · `చు` 0.40 · `ట` 7.7e-4✱ · `్య` 8.8e-6✱ · `్య` 2.9e-4✱ · `్` 1.8e-4✱ · `క` 0.05✱ · `మ` 0.09✱ · `్య` 1.3e-3✱ · `␣హ` 9.2e-3 · `న్` 0.02 · `␣విభ` 2.9e-3 · `్రమ` 1.6e-3✱ · `ల` 0.03✱ · `్యా` 1.5e-3✱ · `⏎` 0.42 |
| 2 | `క` 0.06 · `మ` 0.82 · `␣ల` 0.28 · `క్ష్` 0.13 · `మి` 0.23 · `క` 0.05✱ · `్రి` 3.0e-3✱ · `మ` 0.43 · `్య` 1.3e-3✱ · `␣సీ` 0.99 · `త` 0.99 · `న్` 0.03✱ · `␣జ` 0.97 · `్య` 1.3e-3✱ · `్య` 2.2e-4✱ · `్` 1.3e-6✱ · `క` 0.09✱ · `ము` 0.93 · `ను` 0.94 · `␣జ` 0.93 · `ె` 4.2e-3✱ · `వ` 0.99 · `ణ` 0.97 · `ె` 1.4e-3✱ · `డు` 0.11✱ · `డ` 0.04✱ · `్య` 1.5e-3✱ · `్య` 4.9e-4✱ · `్` 0.02✱ · `క` 0.37 · `క్ష్` 0.19 · `మ` 0.30 · `క` 0.55 · `మ` 0.14✱ · `్య` 3.5e-3✱ · `్య` 0.17✱ · `త` 9.2e-3✱ · `్య` 3.2e-4✱ · `ను` 0.58 · `ర` 0.03✱ · `్య` 9.3e-5✱ · `ు` 0.02✱ · `ట` 7.5e-4✱ · `్` 2.0e-8✱ · `⏎` 3.9e-4✱ forced |
| 3 | `డు` 0.41 · `ము` 3.9e-3✱ · `␣` 3.0e-4✱ · `ట్టి` 3.4e-4✱ · `త` 4.6e-4✱ · `్రి` 1.8e-4✱ · `య` 4.4e-4✱ · `్య` 3.2e-4✱ · `య` 7.5e-3✱ · `్` 3.8e-3✱ · `య` 0.03✱ · `య` 0.03✱ · `య` 0.13✱ · `్య` 9.0e-3✱ · `య` 0.07✱ · `్య` 4.9e-4✱ · `్య` 1.4e-3✱ · `్` 4.0e-5✱ · `లు` 4.5e-4✱ · `␣ఇ` 1.6e-3✱ · `␣వ` 4.4e-3✱ · `్ర` 0.01✱ · `␣స` 0.06✱ · `␣స` 0.77 · `␣త` 0.96 · `␣త` 0.92 · `న` 9.9e-4✱ · `్ర` 2.4e-3✱ · `్ర` 0.09✱ · `్` 2.7e-3✱ · `ల` 1.9e-3✱ · `ు` 1.2e-3✱ · `ల` 1.3e-3✱ · `్ర` 3.5e-4✱ · `ల` 0.01✱ · `ల` 8.5e-3✱ · `్ర` 3.3e-3✱ · `ల` 0.06✱ · `్య` 3.4e-3✱ · `ము` 6.2e-4✱ · `ఘ` 1.6e-4✱ · `్యం` 1.4e-3✱ · `⏎` 7.7e-3✱ forced |
| 4 | `ఉ` 0.03✱ · `␣మన` 3.6e-5✱ · `ం` 3.2e-3✱ · `␣ఉ` 0.17✱ · `ల్ల` 3.5e-4✱ · `ల్ల` 0.02✱ · `్య` 1.1e-3✱ · `␣ల` 0.05✱ · `్య` 0.02✱ · `ర్` 1.7e-4✱ · `ద` 8.7e-3✱ · `య` 0.01✱ · `్య` 2.9e-5✱ · `ు` 7.0e-4✱ · `ను` 0.03✱ · `ను` 1.5e-3✱ · `ను` 0.04✱ · `ను` 3.8e-3✱ · `ను` 0.01✱ · `ను` 9.4e-4✱ · `న` 8.5e-4✱ · `్య` 9.2e-4✱ · `్` 1.8e-3✱ · `ను` 1.4e-3✱ · `మ` 0.03✱ · `్రమ` 3.5e-4✱ · `త్త` 5.6e-3✱ · `స` 0.82 · `్ర` 0.93 · `గ` 1.3e-3✱ · `ధ` 0.99 · `్ర` 4.7e-4✱ · `ై` 1.8e-4✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 152 tokens · 34.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సమమద్రిన్యుగ్యు తర్వన్ర్వ్జ మమ లనుకనున్ర్వ్జక్రమమ్యంముసమ్యమ్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 2 | మమమన్మక్రిమ్య మమ్యమ్య మ లనుకను మల్ర్ర్మమ్య మమ్యస్రమమ్రుమ్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 3 | మమమమ్యమ్యాలనుక్రియ్య్య్మ సముముముడడమ్యమ్య జంఘిమ్రుమజ్యమ్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 4 | మమ లన్కన్ దాటె జంరఘ్వ్వ్మ న్యమమమమమమ్రమ్రమమ్రుమ్నఇం ణణ్ | `IIUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 16% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.024 · model's first choice kept 35% · constraint overrode 55% · backtracks 0

<details><summary>Token probabilities (152 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 5.6e-3 · `మ` 0.14 · `మ` 0.05 · `ద` 0.06 · `్రి` 0.06✱ · `న్` 4.3e-3✱ · `యు` 7.4e-3 · `గ` 0.05 · `్య` 6.6e-4✱ · `ు` 0.04 · `␣తర` 1.2e-3 · `్వ` 3.3e-5✱ · `న` 0.03 · `్ర` 5.6e-5✱ · `్వ` 3.4e-4✱ · `్` 1.2e-5✱ · `జ` 0.04✱ · `␣మ` 0.05 · `మ` 0.04 · `␣ల` 0.02✱ · `ను` 3.4e-3✱ · `క` 0.74 · `ను` 0.11✱ · `న` 0.01✱ · `్ర` 9.0e-4✱ · `్వ` 9.5e-3✱ · `్` 4.1e-4✱ · `జ` 0.93 · `క` 3.1e-3✱ · `్రమ` 2.6e-4✱ · `మ` 0.10✱ · `్యం` 4.1e-5✱ · `ము` 2.5e-3✱ · `స` 0.63 · `మ` 0.68 · `్య` 1.8e-3✱ · `మ` 0.11✱ · `్` 9.8e-6✱ · `⏎` 0.07✱ forced |
| 2 | `మ` 0.23 · `మ` 0.71 · `మ` 0.28 · `న్` 0.01 · `మ` 0.10 · `క` 0.02 · `్రి` 1.7e-3✱ · `మ` 0.15✱ · `్య` 0.01✱ · `␣మ` 0.27 · `మ` 0.44 · `్య` 3.6e-4✱ · `మ` 0.46 · `్య` 0.02✱ · `␣మ` 0.12 · `␣ల` 0.73 · `ను` 0.67 · `క` 0.71 · `ను` 0.81 · `␣మ` 0.38 · `ల` 3.3e-3✱ · `్ర` 2.2e-6✱ · `్ర` 1.3e-3✱ · `్` 9.7e-4✱ · `మ` 0.18✱ · `మ` 0.51 · `్య` 4.5e-3✱ · `␣మ` 0.23 · `మ` 0.62 · `్య` 2.8e-3✱ · `స` 0.70 · `్రమ` 5.2e-5✱ · `మ` 0.12✱ · `్రు` 4.0e-4✱ · `మ` 0.11✱ · `్` 4.2e-4✱ · `⏎` 0.65 |
| 3 | `మ` 0.61 · `మ` 0.90 · `మ` 0.65 · `మ` 0.54 · `్య` 6.6e-4✱ · `మ` 0.52 · `్య` 0.14✱ · `ాల` 4.4e-3✱ · `ను` 0.78 · `క` 0.77 · `్రియ` 9.7e-5✱ · `్య` 1.2e-4✱ · `్య` 3.6e-4✱ · `్` 3.1e-4✱ · `మ` 9.0e-3✱ · `␣స` 0.67 · `ము` 0.69 · `ము` 0.16✱ · `ము` 0.60 · `డ` 0.41 · `డ` 0.25 · `మ` 0.39 · `్య` 2.8e-3✱ · `మ` 0.36 · `్య` 0.01✱ · `␣జ` 0.82 · `ం` 0.99 · `ఘ` 0.72 · `ి` 0.86 · `మ` 0.01✱ · `్రు` 5.9e-3✱ · `మ` 0.12✱ · `జ` 0.72 · `్య` 6.0e-4✱ · `మ` 0.04✱ · `్` 7.2e-4✱ · `⏎` 0.83 |
| 4 | `మ` 0.85 · `మ` 0.94 · `␣ల` 0.84 · `న్` 0.03✱ · `క` 1.00 · `న్` 2.4e-4✱ · `␣దా` 0.93 · `ట` 0.98 · `ె` 0.97 · `␣జ` 0.92 · `ం` 0.92 · `ర` 0.91 · `ఘ` 0.72 · `్వ` 3.1e-5✱ · `్వ` 5.1e-5✱ · `్` 2.9e-6✱ · `మ` 0.37✱ · `␣` 1.1e-4✱ · `న్య` 3.7e-3✱ · `మ` 0.01✱ · `మ` 5.3e-3✱ · `మ` 0.08✱ · `మ` 0.06✱ · `మ` 0.18 · `మ` 0.17✱ · `్రమ` 5.2e-4✱ · `్రమ` 6.0e-4✱ · `మ` 0.30 · `్ర` 2.0e-3✱ · `ు` 0.08✱ · `మ` 0.08✱ · `్` 4.5e-3✱ · `న` 4.2e-3✱ · `ఇ` 8.7e-3✱ · `ం` 0.01✱ · `␣` 0.02✱ · `ణ` 0.04✱ · `ణ` 0.12✱ · `్` 1.1e-3✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 145 tokens · 80.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శమ రత్వల్యొడ్రితిమ్యశ్రమిన లకముడిశ్రమ్రశమ్రేద నిశ్యన్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 2 | శమరావణ్యస్రమమ్యశ్రయ మతను గవల్వ్ర్జల్రునేశమ్యతిశ్రమ్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 3 | సములెచ్యడ్రన్ ధిమయ్రంన్య్య్శమరము జయ లంక్య్య్శమ్యముగ్కున్నుసస్ర్రధ్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 4 | మము లైయంగాను వస్తున్న్ర్మమమమమస తత్ర్ర్మమ్రమాతిత్వముస్రగ్ | `IIUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.010 · model's first choice kept 30% · constraint overrode 63% · backtracks 30

<details><summary>Token probabilities (145 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.97 · `మ` 0.96 · `␣ర` 0.07 · `త్వ` 4.4e-4 · `ల` 0.76 · `్య` 3.5e-3✱ · `ొ` 8.5e-4✱ · `డ` 0.02 · `్రి` 2.3e-3✱ · `తి` 9.3e-4 · `మ` 0.04✱ · `్య` 7.6e-3✱ · `శ` 0.51 · `్ర` 0.66 · `మి` 0.82 · `న` 0.53 · `␣ల` 0.85 · `క` 0.77 · `ము` 0.79 · `డి` 4.9e-5✱ · `శ` 0.67 · `్రమ` 1.1e-3✱ · `్ర` 0.20✱ · `శ` 0.81 · `మ` 0.92 · `్ర` 0.03✱ · `ే` 1.5e-3✱ · `ద` 0.02 · `␣ని` 0.01 · `శ` 0.69 · `్య` 0.97 · `న్` 0.67 · `⏎` 0.62 forced |
| 2 | `శ` 0.19 · `మ` 0.47 · `రా` 0.60 · `వ` 0.67 · `ణ` 0.06 · `్య` 1.7e-3✱ · `స` 0.05✱ · `్రమ` 1.9e-3✱ · `మ` 0.69 · `్య` 0.99 · `శ` 0.97 · `్ర` 7.9e-5✱ · `య` 3.8e-4✱ · `␣మ` 1.0e-4✱ · `త` 1.00 · `ను` 0.99 · `␣గ` 0.05 · `వల` 0.97 · `్వ` 2.6e-6✱ · `్ర` 1.3e-6✱ · `్` 1.1e-5✱ · `జ` 2.8e-3✱ · `ల` 1.00 · `్రు` 5.6e-4✱ · `నే` 3.3e-3✱ · `శ` 0.42 · `మ` 0.87 · `్య` 1.7e-3✱ · `తి` 0.85 · `శ` 0.90 · `్ర` 9.2e-6✱ · `మ` 0.03✱ · `్` 9.9e-8✱ · `⏎` 0.02✱ forced |
| 3 | `స` 0.69 · `ము` 0.94 · `లె` 4.2e-5✱ · `చ` 5.3e-4✱ · `్య` 1.3e-7✱ · `డ` 0.99 · `్ర` 1.2e-4✱ · `న్` 0.97 · `␣ధ` 1.00 · `ి` 1.5e-4✱ · `మ` 0.01✱ · `య` 9.6e-5✱ · `్ర` 6.7e-6✱ · `ం` 3.8e-3✱ · `న` 3.0e-4✱ · `్య` 2.8e-5✱ · `్య` 3.1e-4✱ · `్` 1.2e-3✱ · `శ` 1.2e-3✱ · `మ` 0.09✱ · `ర` 0.04✱ · `ము` 0.15 · `␣జ` 0.07 · `య` 0.58 · `␣ల` 0.05✱ · `ంక` 0.75 · `్య` 3.9e-4✱ · `్య` 2.4e-4✱ · `్` 3.6e-6✱ · `శ` 2.0e-4✱ · `మ` 0.75 · `్య` 0.01✱ · `ము` 0.21✱ · `గ` 1.1e-3✱ · `్` 3.3e-3✱ · `కు` 5.4e-3✱ · `న` 3.6e-3✱ · `్` 2.1e-5✱ · `ను` 0.02✱ · `స` 0.02✱ · `స` 0.09✱ · `్ర` 9.9e-3✱ · `్ర` 0.05 · `ధ` 0.06✱ · `్` 2.2e-4✱ · `⏎` 0.03✱ forced |
| 4 | `మ` 0.10✱ · `ము` 0.06✱ · `␣లై` 1.0e-3✱ · `య` 0.05✱ · `ంగా` 7.3e-3✱ · `ను` 4.6e-4✱ · `␣వ` 0.08✱ · `స్తున్న` 6.0e-4✱ · `్ర` 5.7e-5✱ · `్` 2.4e-3✱ · `మ` 1.5e-5✱ · `మ` 0.02✱ · `మ` 0.07✱ · `మ` 0.05✱ · `మ` 0.01✱ · `స` 0.71 · `␣త` 0.90 · `త` 1.7e-3✱ · `్ర` 3.1e-4✱ · `్ర` 0.02✱ · `్` 1.7e-3✱ · `మ` 5.9e-3✱ · `మ` 1.4e-3✱ · `్ర` 1.7e-3✱ · `మా` 7.1e-4✱ · `తి` 8.0e-3✱ · `త్వ` 6.5e-3✱ · `ము` 3.0e-3✱ · `స` 2.1e-3✱ · `్ర` 0.02✱ · `గ` 0.03✱ · `్` 3.3e-5✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 169 tokens · 67.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జలరభ్వా నమ్రగన్ జెల్ల్ర్జ హనుమతును చిల్ర్వ్జడ్యుగన్ జెల్ల్ర్జ లంకన్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 2 | జలశౌమన్య్రగ్య జెల్ల్ర్జమ్య్య్జమర మమతి జెల్ల్ర్జడ్యుగన్ మధ్రముల్ ట్టిం | `IIUUUIUUIIIIIIUUIUUIUU` |
| 3 | సుల క్షన్య్య్యయ్జ్మర్రితిత్వవ్ర్ర్జువవతితివనహ్య్య్జోమ సద్రద్ర దాటివ్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 4 | వలుడున్య్యీ లేదు లేదుక్ర్ర్వ గముముముముముల్ర్ర్వల్రిదిస్థోమమహ్ర్రగ్ | `IIUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 5% · repeated lines 0 · mean token probability (geometric) 0.022 · model's first choice kept 40% · constraint overrode 59% · backtracks 30

<details><summary>Token probabilities (169 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.61 · `ల` 1.00 · `ర` 0.91 · `భ` 0.87 · `్వ` 0.98 · `ా` 0.89 · `␣న` 0.17 · `మ` 0.58 · `్ర` 0.67 · `గ` 0.48 · `న్` 0.93 · `␣జ` 0.95 · `ె` 0.91 · `ల్ల` 0.98 · `్ర` 2.5e-6✱ · `్` 3.3e-7✱ · `జ` 5.3e-4✱ · `␣హ` 0.97 · `ను` 0.99 · `మ` 0.14✱ · `తు` 0.96 · `ను` 0.12✱ · `␣` 0.01✱ · `చి` 2.2e-4 · `ల` 0.99 · `్ర` 3.7e-3✱ · `్వ` 5.4e-6✱ · `్` 2.1e-6✱ · `జ` 0.40 · `డ` 6.4e-3✱ · `్య` 6.8e-4✱ · `ు` 0.50 · `గ` 0.88 · `న్` 0.94 · `␣జ` 0.98 · `ె` 0.94 · `ల్ల` 0.99 · `్ర` 0.81 · `్` 0.97 · `జ` 0.97 · `␣ల` 0.99 · `ం` 0.96 · `క` 0.99 · `న్` 0.02✱ · `⏎` 0.76 |
| 2 | `జ` 0.79 · `ల` 0.86 · `శ` 0.91 · `ౌ` 1.00 · `మ` 0.62 · `న` 0.14✱ · `్య` 2.6e-4✱ · `్ర` 0.62 · `గ` 0.88 · `్య` 8.2e-5✱ · `␣జ` 0.96 · `ె` 0.96 · `ల్ల` 0.98 · `్ర` 0.83 · `్` 0.91 · `జ` 0.98 · `మ` 1.4e-3✱ · `్య` 3.1e-6✱ · `్య` 6.1e-5✱ · `్` 1.9e-7✱ · `జ` 0.03✱ · `మ` 0.05✱ · `ర` 6.0e-3✱ · `␣మ` 0.62 · `మ` 0.61 · `తి` 0.90 · `␣జ` 0.97 · `ె` 0.95 · `ల్ల` 0.98 · `్ర` 0.90 · `్` 0.82 · `జ` 0.99 · `డ` 0.99 · `్య` 0.99 · `ు` 1.00 · `గ` 0.99 · `న్` 0.99 · `␣మ` 0.99 · `ధ` 3.1e-3✱ · `్ర` 1.2e-4✱ · `ము` 0.03✱ · `ల్` 5.7e-5✱ · `␣` 1.9e-3✱ · `ట్టి` 3.2e-5✱ · `ం` 5.2e-4✱ · `⏎` 0.06✱ forced |
| 3 | `సు` 2.7e-3✱ · `ల` 5.0e-4✱ · `␣క్ష` 0.14✱ · `న` 8.9e-3✱ · `్య` 1.5e-3✱ · `్య` 0.03✱ · `్య` 0.02✱ · `య` 4.9e-3✱ · `్` 0.01✱ · `జ్` 0.03✱ · `మ` 0.08✱ · `ర` 0.07✱ · `్రి` 9.1e-7✱ · `తి` 5.3e-3✱ · `త్వ` 6.6e-4✱ · `వ` 0.01✱ · `్ర` 9.4e-4✱ · `్ర` 0.03✱ · `్` 3.3e-4✱ · `జ` 0.22 · `ు` 3.9e-4✱ · `వ` 3.0e-3✱ · `వ` 3.5e-3✱ · `తి` 0.02✱ · `తి` 0.04✱ · `వ` 3.8e-3✱ · `న` 0.06✱ · `హ` 0.30✱ · `్య` 1.9e-5✱ · `్య` 7.7e-5✱ · `్` 2.9e-6✱ · `జ` 6.7e-3✱ · `ో` 9.7e-5✱ · `మ` 0.16 · `␣స` 5.9e-4✱ · `ద్ర` 0.18✱ · `ద్ర` 0.19✱ · `␣దా` 0.38 · `టి` 0.59 · `వ` 2.1e-6✱ · `్` 9.3e-5✱ · `⏎` 0.01✱ forced |
| 4 | `వ` 6.1e-3✱ · `లు` 5.6e-4✱ · `డు` 0.02✱ · `న` 5.5e-4✱ · `్య` 1.4e-4✱ · `్య` 0.04✱ · `ీ` 9.1e-3✱ · `␣లేదు` 9.3e-3✱ · `␣లేదు` 0.21✱ · `క` 5.2e-4✱ · `్ర` 3.7e-4✱ · `్ర` 0.01✱ · `్` 0.01✱ · `వ` 2.8e-3✱ · `␣గ` 8.7e-3✱ · `ము` 0.01✱ · `ము` 0.02✱ · `ము` 0.05✱ · `ము` 0.38 · `ము` 0.06✱ · `ల` 3.2e-4✱ · `్ర` 2.0e-3✱ · `్ర` 3.6e-3✱ · `్` 1.8e-4✱ · `వ` 0.03✱ · `ల` 0.02✱ · `్రి` 3.0e-5✱ · `ది` 2.3e-3✱ · `స్థ` 3.1e-3✱ · `ో` 6.7e-3✱ · `మ` 0.07✱ · `మ` 0.83 · `హ` 0.02✱ · `్ర` 1.8e-4✱ · `్ర` 0.99 · `గ్` 0.99 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 149 tokens · 40.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మన్రిత్రై మమత్యా మ్ర్ధ్కత మనసకకక్రామమమ్రుమ్రిమమ్రా | `IIUUUIUUIIIIIIUUIUUIUU` |
| 2 | తమ మమ్యం మమ్రుమన్రుమ్ర్ర్ధమమమ మమమమ్ర్ర్ధమ్రమమ్యమ్యకమ్యం | `IIUUUIUUIIIIIIUUIUUIUU` |
| 3 | తమ మమ్యం మమ్రుమమ్రుమ్ర్ధమమమమమనిం తం మమమ్రిమ్యమమ్రా | `IIUUUIUUIIIIIIUUIUUIUU` |
| 4 | మమమమ్యమ్యమ్యమమ్రధ్ర్ధ్మ త న స ర ర గుర్ర్ర్మర్రధర్ర్రున్రతిన్రా | `IIUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 29% · repeated lines 0 · mean token probability (geometric) 0.020 · model's first choice kept 38% · constraint overrode 58% · backtracks 0

<details><summary>Token probabilities (149 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.09✱ · `మ` 0.12 · `␣మ` 0.06 · `న` 0.02✱ · `్రి` 1.6e-4✱ · `త` 0.04✱ · `్ర` 4.7e-5✱ · `ై` 0.06✱ · `␣మ` 0.21 · `మ` 0.27 · `త` 0.18 · `్యా` 4.8e-4✱ · `␣మ` 0.44 · `్ర` 4.7e-4✱ · `్` 6.4e-5✱ · `ధ` 0.01 · `్` 2.0e-4✱ · `క` 0.02✱ · `త` 0.05 · `␣మ` 0.15 · `న` 0.01 · `స` 0.19 · `క` 0.05✱ · `క` 0.16✱ · `క` 0.25 · `్రా` 6.4e-5✱ · `మ` 0.26 · `మ` 0.11✱ · `మ` 0.07✱ · `్రు` 1.7e-4✱ · `మ` 0.17 · `్రి` 4.8e-4✱ · `మ` 0.06✱ · `మ` 0.17 · `్రా` 7.8e-5✱ · `⏎` 0.29 |
| 2 | `త` 0.17 · `మ` 0.41 · `␣మ` 0.12 · `మ` 0.09 · `్యం` 3.8e-4✱ · `␣మ` 0.17 · `మ` 0.15 · `్రు` 4.6e-4✱ · `మ` 0.42 · `న` 0.55 · `్రు` 3.6e-3✱ · `మ` 0.31 · `్ర` 3.9e-3✱ · `్ర` 1.3e-3✱ · `్` 2.0e-3✱ · `ధ` 0.14✱ · `మ` 0.53 · `మ` 0.42 · `మ` 0.25 · `␣మ` 0.12 · `మ` 0.44 · `మ` 0.22 · `మ` 0.47 · `్ర` 1.7e-3✱ · `్ర` 0.01✱ · `్` 7.7e-3✱ · `ధ` 0.55 · `మ` 0.66 · `్ర` 4.1e-4✱ · `మ` 0.47 · `మ` 0.76 · `్య` 8.1e-4✱ · `మ` 0.48 · `్య` 3.1e-3✱ · `క` 0.79 · `మ` 0.76 · `్యం` 1.3e-3✱ · `⏎` 0.82 |
| 3 | `త` 0.84 · `మ` 0.90 · `␣మ` 0.76 · `మ` 0.81 · `్యం` 1.3e-3✱ · `␣మ` 0.94 · `మ` 0.93 · `్రు` 6.6e-3✱ · `మ` 0.86 · `మ` 0.44 · `్రు` 2.0e-3✱ · `మ` 0.94 · `్ర` 6.4e-4✱ · `్` 0.01✱ · `ధ` 0.81 · `మ` 0.78 · `మ` 0.22✱ · `మ` 2.0e-3✱ · `మ` 3.0e-3✱ · `మని` 8.6e-5✱ · `ం` 6.4e-7✱ · `␣` 4.5e-5✱ · `త` 2.6e-3✱ · `ం` 1.8e-3✱ · `␣మ` 0.01✱ · `మ` 0.02✱ · `మ` 0.02✱ · `్రి` 6.7e-3✱ · `మ` 5.8e-3✱ · `్య` 2.5e-3✱ · `మ` 0.07✱ · `మ` 5.4e-3✱ · `్రా` 5.1e-3✱ · `⏎` 0.12✱ forced |
| 4 | `మ` 3.6e-4✱ · `మ` 0.07✱ · `మ` 0.08✱ · `మ` 0.16 · `్య` 3.5e-3✱ · `మ` 0.13✱ · `్య` 0.08✱ · `మ` 0.16 · `్య` 0.05✱ · `మ` 0.29 · `మ` 0.07✱ · `్ర` 1.3e-3✱ · `ధ` 0.12✱ · `్ర` 0.04✱ · `్` 1.3e-4✱ · `ధ` 0.46 · `్` 4.8e-5✱ · `మ` 4.0e-4✱ · `␣త` 0.78 · `␣న` 0.73 · `␣స` 0.83 · `␣ర` 0.79 · `␣ర` 0.83 · `␣గు` 0.78 · `ర` 8.2e-4✱ · `్ర` 2.4e-4✱ · `్ర` 8.3e-4✱ · `్` 4.1e-3✱ · `మ` 8.0e-3✱ · `ర` 3.1e-3✱ · `్ర` 3.2e-3✱ · `ధ` 0.09✱ · `ర` 0.38 · `్ర` 1.6e-5✱ · `్ర` 4.2e-4✱ · `ు` 2.2e-3✱ · `న` 3.8e-3✱ · `్ర` 2.0e-4✱ · `తి` 7.2e-4✱ · `న` 4.6e-3✱ · `్రా` 3.6e-5✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 152 tokens · 46.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జకరప్యమ్యత్రి జల్రవ్య్య్జముడె జలధి లల్ర్య్శక్రిలమ్రిహ్రముగ్యా | `IIUUUIUUIIIIIIUUIUUIUU` |
| 2 | క్రికమయ్యల్యమ్య మమ్రిమ్య్య్యృమమమను మమగ్య్రియ్రిచుల్యాగనున్రీ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 3 | తికమహ్రమ్రిల్రునుంజుడ్య్య్తృకుటి ల లను చేర్వ్య్తృల్రియశ్రీకకవ్యా | `IIUUUIUUIIIIIIUUIUUIUU` |
| 4 | సకు తర్రస్రర్రుకల్యయ్య్య్జమమము మహసస్ర్రర్రడుగ్యుఘ్రముగ్రీ | `IIUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.007 · model's first choice kept 20% · constraint overrode 72% · backtracks 0

<details><summary>Token probabilities (152 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.10 · `క` 0.02 · `ర` 0.02 · `ప` 0.01✱ · `్య` 2.9e-3✱ · `మ` 0.19 · `్య` 1.7e-3✱ · `త` 7.9e-3✱ · `్రి` 3.6e-4✱ · `␣జ` 0.10 · `ల` 0.63 · `్ర` 2.0e-5✱ · `వ` 0.03✱ · `్య` 6.2e-5✱ · `్య` 2.2e-4✱ · `్` 7.9e-5✱ · `జ` 0.23 · `మ` 0.04 · `ు` 0.02 · `డ` 0.11 · `ె` 0.06✱ · `␣జ` 0.11 · `ల` 0.18 · `ధి` 0.36 · `␣ల` 0.02 · `ల` 0.04✱ · `్ర` 1.8e-3✱ · `్య` 6.2e-5✱ · `్` 3.0e-8✱ · `శ` 1.4e-3✱ · `క` 0.81 · `్రి` 6.7e-4✱ · `ల` 0.69 · `మ` 0.03✱ · `్రి` 1.8e-5✱ · `హ` 0.63 · `్ర` 8.9e-4✱ · `ము` 0.78 · `గ` 0.91 · `్యా` 1.4e-4✱ · `⏎` 0.05✱ forced |
| 2 | `క` 0.09 · `్రి` 2.1e-3✱ · `క` 5.0e-3✱ · `మ` 0.17 · `య` 0.02 · `్య` 1.5e-3✱ · `ల` 0.05✱ · `్య` 1.4e-3✱ · `మ` 0.14✱ · `్య` 9.4e-3✱ · `␣మ` 0.35 · `మ` 6.6e-3✱ · `్రి` 6.6e-5✱ · `మ` 0.15✱ · `్య` 2.5e-3✱ · `్య` 3.3e-4✱ · `్య` 6.1e-4✱ · `ృ` 6.9e-5✱ · `మ` 0.27 · `మ` 0.15 · `మ` 0.28 · `ను` 0.76 · `␣మ` 0.03✱ · `మ` 0.41 · `గ` 0.30 · `్య` 4.9e-3✱ · `్రియ` 1.6e-4✱ · `్రి` 3.2e-5✱ · `చు` 0.98 · `ల` 0.02✱ · `్యా` 4.4e-4✱ · `గ` 0.02✱ · `ను` 0.58 · `న` 3.2e-3✱ · `్రీ` 3.1e-4✱ · `⏎` 0.43 |
| 3 | `తి` 0.89 · `క` 2.2e-4✱ · `మ` 0.81 · `హ` 0.51 · `్ర` 9.1e-3✱ · `మ` 0.02✱ · `్రి` 6.4e-4✱ · `ల` 0.01✱ · `్రు` 1.2e-5✱ · `ను` 0.53 · `ంజ` 7.8e-3✱ · `ు` 0.03✱ · `డ` 2.6e-3✱ · `్య` 3.3e-4✱ · `్య` 8.8e-3✱ · `్` 4.0e-6✱ · `త` 2.0e-3✱ · `ృ` 8.9e-6✱ · `కు` 1.4e-3✱ · `టి` 0.97 · `␣ల` 0.98 · `␣ల` 5.7e-4✱ · `ను` 0.84 · `␣చే` 0.98 · `ర్` 4.4e-4✱ · `వ` 0.02✱ · `్య` 3.8e-8✱ · `్` 2.1e-6✱ · `త` 4.7e-4✱ · `ృ` 1.8e-4✱ · `ల` 0.03✱ · `్రియ` 4.8e-4✱ · `శ` 2.4e-3✱ · `్రీ` 8.5e-3✱ · `క` 7.6e-4✱ · `క` 0.11✱ · `వ` 5.7e-3✱ · `్యా` 6.6e-5✱ · `⏎` 0.07✱ forced |
| 4 | `స` 0.04✱ · `కు` 2.5e-3✱ · `␣త` 0.84 · `ర` 2.4e-3✱ · `్ర` 2.6e-3✱ · `స` 0.02✱ · `్ర` 4.8e-4✱ · `ర` 0.10✱ · `్రు` 3.2e-3✱ · `క` 4.4e-4✱ · `ల` 3.0e-3✱ · `్య` 4.2e-3✱ · `య` 0.02✱ · `్య` 2.8e-4✱ · `్య` 6.2e-3✱ · `్` 1.3e-3✱ · `జ` 2.2e-4✱ · `మ` 0.03✱ · `మ` 0.13✱ · `ము` 0.05✱ · `␣మహ` 7.0e-3✱ · `స` 0.93 · `స` 5.2e-3✱ · `్ర` 0.04✱ · `్ర` 3.6e-3✱ · `ర` 0.01✱ · `్ర` 3.4e-3✱ · `డు` 7.4e-3✱ · `గ` 3.7e-3✱ · `్య` 1.8e-3✱ · `ు` 0.04✱ · `ఘ` 8.7e-3✱ · `్ర` 4.3e-3✱ · `ము` 0.08✱ · `గ` 0.01✱ · `్రీ` 0.02✱ |

</details>

[↑ meters](#meters)

---

<a id="totakamu"></a>

## 7. తోటకము (totakamu)

```text
Meter: తోటకము (totakamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: స స స స, i.e. IIU IIU IIU IIU (12 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter తోటకము (totakamu).

Meter: తోటకము (totakamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: స స స స, i.e. IIU IIU IIU IIU (12 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 71 tokens · 8.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మల్యము జల్రి కొకన్రి సముక్ | `IIUIIUIIUIIU` |
| 2 | కమ లుక్ష్మిముముల్రి మగన్రి సముక్ | `IIUIIUIIUIIU` |
| 3 | కమ మక్రి జలారి వొకన్రి సముక్ | `IIUIIUIIUIIU` |
| 4 | కమ మాయము జల్రి నగన్రి సముక్ | `IIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 21% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.131 · model's first choice kept 63% · constraint overrode 18% · backtracks 0

<details><summary>Token probabilities (71 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.02✱ · `మ` 0.25 · `␣మ` 0.01 · `ల` 0.46 · `్య` 2.9e-4✱ · `ము` 0.11 · `␣జ` 0.02 · `ల` 0.12 · `్రి` 4.2e-5✱ · `␣క` 0.02 · `ొ` 3.4e-3✱ · `క` 0.02✱ · `న` 6.6e-3✱ · `్రి` 5.7e-5✱ · `␣స` 0.02 · `ము` 0.04 · `క` 0.08✱ · `్` 9.7e-9✱ · `⏎` 0.76 |
| 2 | `క` 0.90 · `మ` 0.98 · `␣లు` 1.3e-3 · `క్ష్` 0.05 · `మి` 0.43 · `ము` 0.27 · `ము` 0.01 · `ల` 0.46 · `్రి` 0.39 · `␣మ` 0.14 · `గ` 0.04✱ · `న` 0.71 · `్రి` 0.81 · `␣స` 0.94 · `ము` 0.90 · `క` 0.94 · `్` 0.82 · `⏎` 0.99 |
| 3 | `క` 0.94 · `మ` 0.99 · `␣మ` 0.04 · `క` 0.15 · `్రి` 5.4e-3✱ · `␣జ` 0.95 · `ల` 0.91 · `ారి` 0.02✱ · `␣వ` 0.09 · `ొ` 0.75 · `క` 0.51 · `న` 0.73 · `్రి` 0.78 · `␣స` 0.90 · `ము` 0.98 · `క` 0.98 · `్` 0.43 · `⏎` 0.96 |
| 4 | `క` 0.93 · `మ` 0.98 · `␣మ` 0.75 · `ాయ` 0.46 · `ము` 0.46 · `␣జ` 0.83 · `ల` 0.79 · `్రి` 0.20✱ · `␣న` 0.47 · `గ` 0.71 · `న` 0.89 · `్రి` 0.95 · `␣స` 0.98 · `ము` 0.99 · `క` 0.99 · `్` 0.38 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 78 tokens · 18.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మల్రు మ మక్రిమ మ్ర్వ్గా కమ వల్ | `IIUIIUIIUIIU` |
| 2 | మమ మమ్య మ మమ్య మ మ్యమ్యమ మల్ | `IIUIIUIIUIIU` |
| 3 | మమనుల్యతనుమ్యతమమ్య వ లయ్ | `IIUIIUIIUIIU` |
| 4 | తమ మల్యను మమ్యను మ్య్య్తై మలయౌ | `IIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 41% · repeated lines 0 · mean token probability (geometric) 0.025 · model's first choice kept 44% · constraint overrode 46% · backtracks 0

<details><summary>Token probabilities (78 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.10 · `మ` 0.15 · `␣మ` 0.09 · `ల` 0.60 · `్రు` 7.6e-5✱ · `␣మ` 0.16 · `␣మ` 0.04 · `క` 0.06✱ · `్రి` 3.4e-4✱ · `మ` 0.07 · `␣మ` 0.21 · `్ర` 2.9e-4✱ · `్వ` 2.5e-5✱ · `్` 2.0e-5✱ · `గా` 0.01✱ · `␣క` 0.12 · `మ` 0.16 · `␣వ` 2.3e-3 · `ల` 0.19 · `్` 1.1e-7✱ · `⏎` 0.11✱ forced |
| 2 | `మ` 0.76 · `మ` 0.62 · `␣మ` 0.19 · `మ` 0.10 · `్య` 5.5e-4✱ · `␣మ` 0.31 · `␣మ` 0.44 · `మ` 0.22 · `్య` 5.8e-3✱ · `␣మ` 0.70 · `␣మ` 0.58 · `్య` 0.03 · `మ` 0.15✱ · `్య` 0.02✱ · `మ` 0.16 · `␣మ` 0.16 · `ల` 0.45 · `్` 8.7e-6✱ · `⏎` 0.98 |
| 3 | `మ` 0.92 · `మ` 2.1e-3✱ · `ను` 0.90 · `ల` 4.4e-3✱ · `్య` 2.9e-4✱ · `త` 0.97 · `ను` 0.90 · `మ` 3.5e-3✱ · `్య` 0.03✱ · `త` 0.90 · `మ` 3.7e-3✱ · `మ` 0.03✱ · `్య` 0.08✱ · `␣వ` 0.49 · `␣ల` 0.49 · `య` 0.93 · `్` 1.6e-5✱ · `⏎` 0.36✱ forced |
| 4 | `త` 0.94 · `మ` 0.22✱ · `␣మ` 0.94 · `ల` 0.02✱ · `్య` 8.4e-3✱ · `ను` 0.63 · `␣మ` 0.73 · `మ` 0.03✱ · `్య` 0.08✱ · `ను` 0.76 · `␣మ` 0.74 · `్య` 2.4e-3✱ · `్య` 2.4e-3✱ · `్` 2.4e-6✱ · `త` 8.7e-5✱ · `ై` 1.4e-3✱ · `␣మ` 3.1e-3✱ · `ల` 0.27 · `య` 0.42 · `ౌ` 1.2e-6✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 71 tokens · 40.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మరి సాగి మెరై రి సొమల్రియెలిట్ | `IIUIIUIIUIIU` |
| 2 | జరినస్రకుటాన జొసగ్రులిచిన్ | `IIUIIUIIUIIU` |
| 3 | సరిముద్రము దాటి ల ల్య్వ్నమ్రి లకక్ | `IIUIIUIIUIIU` |
| 4 | దరి హంతుతినిక్షమతాయ పడైన్ | `IIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 27% · single-akshara words 13% · repeated lines 0 · mean token probability (geometric) 0.015 · model's first choice kept 49% · constraint overrode 42% · backtracks 30

<details><summary>Token probabilities (71 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.85 · `రి` 0.95 · `␣సా` 0.97 · `గి` 0.94 · `␣మె` 1.5e-3 · `ర` 0.95 · `ై` 0.74 · `␣రి` 1.7e-4 · `␣స` 0.20 · `ొ` 0.60 · `మ` 0.18✱ · `ల` 0.92 · `్రియ` 8.0e-6✱ · `ె` 0.96 · `లి` 0.90 · `ట` 0.98 · `్` 5.2e-7✱ · `⏎` 0.07✱ forced |
| 2 | `జ` 0.97 · `రి` 0.97 · `న` 5.2e-3 · `స` 1.4e-6✱ · `్ర` 4.5e-7✱ · `కు` 0.95 · `ట` 0.99 · `ాన` 1.00 · `␣జ` 8.5e-3 · `ొ` 0.92 · `స` 0.76 · `గ` 0.99 · `్రు` 5.9e-6✱ · `లి` 1.00 · `చి` 0.98 · `న` 0.07✱ · `్` 5.9e-7✱ · `⏎` 0.98 |
| 3 | `స` 0.99 · `రి` 5.8e-5✱ · `ము` 0.05✱ · `ద్ర` 0.05✱ · `ము` 0.65 · `␣దా` 0.95 · `టి` 0.94 · `␣ల` 0.98 · `␣ల` 5.0e-3✱ · `్య` 1.6e-7✱ · `్వ` 6.5e-6✱ · `్` 6.6e-8✱ · `న` 1.0e-3✱ · `మ` 0.80 · `్రి` 1.8e-3✱ · `␣ల` 6.4e-3✱ · `క` 0.82 · `క` 0.01✱ · `్` 8.6e-9✱ · `⏎` 0.30✱ forced |
| 4 | `ద` 0.12 · `రి` 0.31 · `␣హ` 0.99 · `ం` 3.1e-4✱ · `తు` 0.10✱ · `తి` 0.54 · `ని` 0.03✱ · `క్ష` 0.58 · `మ` 0.99 · `త` 1.6e-4✱ · `ాయ` 6.3e-3✱ · `␣ప` 0.98 · `డ` 1.4e-5✱ · `ైన` 0.03✱ · `్` 6.8e-10✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 78 tokens · 37.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కొల మమ్రతకక్యధు ర్య్య్కుస్రిబకమ్ | `IIUIIUIIUIIU` |
| 2 | మొల రీవకునాలి మమొల్ల లకమ్ | `IIUIIUIIUIIU` |
| 3 | తొల నివ్వల మల్లి లతొర్రమతిక్ | `IIUIIUIIUIIU` |
| 4 | తొలనాలి మలున్కమతొమ్రియ గగ్ | `IIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 21% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.029 · model's first choice kept 51% · constraint overrode 41% · backtracks 30

<details><summary>Token probabilities (78 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.14 · `ొ` 0.09✱ · `ల` 0.08 · `␣మ` 0.18 · `మ` 0.23 · `్ర` 3.6e-3✱ · `త` 0.11 · `క` 0.11 · `క` 0.04✱ · `్య` 6.4e-6✱ · `ధు` 0.96 · `␣ర` 0.45 · `్య` 5.6e-5✱ · `్య` 9.1e-4✱ · `్` 5.9e-6✱ · `క` 0.04✱ · `ు` 2.7e-4✱ · `స` 1.3e-3✱ · `్రి` 0.76 · `బ` 0.38 · `క` 0.63 · `మ` 0.60 · `్` 1.1e-5✱ · `⏎` 0.55 |
| 2 | `మ` 0.24 · `ొ` 0.91 · `ల` 0.92 · `␣రీ` 0.83 · `వ` 0.79 · `కు` 2.8e-3 · `న` 0.83 · `ాలి` 0.95 · `␣మ` 0.82 · `మ` 0.92 · `ొ` 0.71 · `ల్ల` 0.27 · `␣ల` 4.5e-4✱ · `క` 0.99 · `మ` 0.94 · `్` 1.8e-5✱ · `⏎` 0.99 |
| 3 | `త` 0.97 · `ొ` 0.99 · `ల` 0.97 · `␣ని` 0.99 · `వ` 0.97 · `్వ` 1.0e-5✱ · `ల` 9.8e-4✱ · `␣మ` 0.97 · `ల్లి` 0.96 · `␣ల` 7.9e-5✱ · `త` 3.0e-3✱ · `ొ` 5.7e-6✱ · `ర` 0.18 · `్ర` 7.9e-5✱ · `మ` 0.89 · `తి` 0.96 · `క` 1.1e-3✱ · `్` 3.4e-6✱ · `⏎` 0.34✱ forced |
| 4 | `త` 0.42 · `ొ` 0.19✱ · `ల` 4.8e-3✱ · `న` 0.90 · `ాలి` 1.00 · `␣మ` 1.00 · `లు` 1.1e-3✱ · `న్` 4.8e-5✱ · `క` 0.99 · `మ` 0.99 · `త` 5.4e-3✱ · `ొ` 6.1e-4✱ · `మ` 0.97 · `్రియ` 1.7e-4✱ · `␣` 5.8e-4✱ · `గ` 0.01✱ · `గ` 0.89 · `్` 2.1e-6✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 63 tokens · 16.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జకమించిన దై దము జగ్రమలో | `IIUIIUIIUIIU` |
| 2 | కకలిమ్రియ లేయ మ మ్ర్మ్కమ్రిలలో | `IIUIIUIIUIIU` |
| 3 | తక ప్రేమ మకట్రకతక్రితృ ఏ | `IIUIIUIIUIIU` |
| 4 | తకదిక్రమముల్యమ ల్ర్య్దయ్ ప పలో | `IIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 31% · repeated lines 0 · mean token probability (geometric) 0.010 · model's first choice kept 27% · constraint overrode 59% · backtracks 0

<details><summary>Token probabilities (63 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.19 · `క` 0.07 · `మ` 0.05 · `ించిన` 0.20 · `␣ద` 0.04 · `ై` 0.70 · `␣ద` 0.03 · `ము` 0.19 · `␣జగ` 0.03 · `్రమ` 6.3e-6✱ · `లో` 0.06 · `⏎` 0.01✱ forced |
| 2 | `క` 0.18 · `క` 0.18 · `లి` 0.04 · `మ` 0.04✱ · `్రియ` 1.7e-5✱ · `␣లే` 0.55 · `య` 0.02✱ · `␣మ` 0.13 · `␣మ` 0.07✱ · `్ర` 4.2e-3✱ · `్` 7.5e-5✱ · `మ` 0.05 · `్` 1.0e-6✱ · `క` 0.02✱ · `మ` 0.07✱ · `్రి` 2.2e-4✱ · `లలో` 7.5e-3✱ · `⏎` 0.52 |
| 3 | `త` 0.59 · `క` 4.1e-3✱ · `␣ప్రేమ` 0.93 · `␣మ` 2.9e-3✱ · `క` 0.92 · `ట` 8.8e-3✱ · `్ర` 8.0e-5✱ · `క` 0.89 · `త` 5.4e-4✱ · `క` 0.01✱ · `్రి` 3.4e-5✱ · `త` 0.68 · `ృ` 0.63 · `␣ఏ` 8.1e-4✱ · `⏎` 0.01✱ forced |
| 4 | `త` 0.03✱ · `క` 0.07✱ · `ది` 0.78 · `క` 3.0e-3✱ · `్రమ` 3.9e-5✱ · `ము` 0.56 · `ల` 4.7e-4✱ · `్య` 8.8e-5✱ · `మ` 0.05✱ · `␣ల` 0.01✱ · `్ర` 1.1e-5✱ · `్య` 4.7e-5✱ · `్` 8.3e-5✱ · `దయ` 3.7e-4✱ · `్` 1.1e-4✱ · `␣ప` 0.39 · `␣ప` 1.0e-3✱ · `లో` 0.04✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 71 tokens · 17.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | దమతక్యము మన్యు జెదప్వర సీ | `IIUIIUIIUIIU` |
| 2 | న్మమరక్యము లక్రి న జ్వ్వ్నం లసమా | `IIUIIUIIUIIU` |
| 3 | క్యము సీమతనుట్యపునక్యమమా | `IIUIIUIIUIIU` |
| 4 | మము లక్రమనుడ్రవి జ్య్య్మాను లమున్ | `IIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 20% · repeated lines 0 · mean token probability (geometric) 0.010 · model's first choice kept 34% · constraint overrode 52% · backtracks 0

<details><summary>Token probabilities (71 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ద` 0.01✱ · `మ` 0.17 · `త` 0.12 · `క` 0.03✱ · `్య` 4.8e-4✱ · `ము` 0.57 · `␣మ` 0.02 · `న్` 0.05✱ · `యు` 0.52 · `␣జ` 0.03 · `ె` 0.07✱ · `ద` 4.8e-3✱ · `ప` 0.67 · `్వర` 1.8e-5✱ · `␣సీ` 0.02 · `⏎` 4.2e-3 forced |
| 2 | `న్` 0.16 · `మ` 0.13✱ · `మ` 0.20 · `ర` 0.03 · `క` 0.11✱ · `్య` 0.02✱ · `ము` 0.86 · `␣ల` 0.47 · `క` 0.09 · `్రి` 1.4e-3✱ · `␣న` 0.07 · `␣జ` 3.4e-3✱ · `్వ` 0.01✱ · `్వ` 7.8e-4✱ · `్` 2.3e-6✱ · `నం` 2.0e-3✱ · `␣ల` 1.6e-3✱ · `స` 0.82 · `మా` 2.9e-3 · `⏎` 0.09 forced |
| 3 | `క` 0.65 · `్య` 0.51 · `ము` 0.61 · `␣సీ` 0.93 · `మ` 0.95 · `త` 0.97 · `ను` 0.98 · `ట` 5.8e-4✱ · `్య` 7.0e-6✱ · `ప` 0.30 · `ు` 3.4e-5✱ · `న` 1.7e-3✱ · `క` 1.4e-3✱ · `్య` 5.7e-5✱ · `మ` 0.62 · `మా` 1.1e-3✱ · `⏎` 0.11 forced |
| 4 | `మ` 0.34 · `ము` 0.76 · `␣ల` 0.82 · `క` 0.69 · `్రమ` 5.8e-6✱ · `ను` 0.99 · `డ` 2.5e-4✱ · `్ర` 1.9e-6✱ · `వి` 3.6e-4✱ · `␣జ` 9.9e-6✱ · `్య` 4.7e-6✱ · `్య` 4.2e-5✱ · `్` 5.5e-7✱ · `మా` 1.0e-3✱ · `ను` 5.6e-3✱ · `␣ల` 0.01✱ · `ము` 0.02✱ · `న్` 7.2e-4✱ |

</details>

[↑ meters](#meters)

---

<a id="bhujangaprayatamu"></a>

## 8. భుజంగప్రయాతము (bhujangaprayatamu)

```text
Meter: భుజంగప్రయాతము (bhujangaprayatamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: య య య య, i.e. IUU IUU IUU IUU (12 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 8th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter భుజంగప్రయాతము (bhujangaprayatamu).

Meter: భుజంగప్రయాతము (bhujangaprayatamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: య య య య, i.e. IUU IUU IUU IUU (12 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 8th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 82 tokens · 20.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | లతన్ లంక చూడుగ్య క్ర్లాంతమ్రగళ్వర్ | `IUUIUUIUUIUU` |
| 2 | తతత్రియ్య వేగగ్య శ్త్రమ్రమ్రకమ్యా | `IUUIUUIUUIUU` |
| 3 | శతంతంతటగ్యభ్యసమ్రహ్రి రర్రహ్ | `IUUIUUIUUIUU` |
| 4 | త తానున్యుగల్యత్రు భ్ర్వ్తర్రమ్యముభ్రుజ్ | `IUUIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.003 · model's first choice kept 26% · constraint overrode 68% · backtracks 0

<details><summary>Token probabilities (82 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ల` 0.02 · `త` 0.03✱ · `న్` 0.05 · `␣ల` 0.17 · `ం` 3.2e-3✱ · `క` 0.06 · `␣చూ` 2.7e-4 · `డు` 0.10 · `గ` 9.5e-3✱ · `్య` 1.1e-4✱ · `␣క` 6.2e-3 · `్ర` 1.5e-4✱ · `్లా` 1.6e-4✱ · `ంత` 0.26 · `మ` 0.01✱ · `్ర` 1.4e-3✱ · `గ` 6.9e-3✱ · `ళ` 3.3e-3✱ · `్వర` 9.5e-4✱ · `్` 5.1e-7✱ · `⏎` 0.08✱ forced |
| 2 | `త` 0.59 · `త` 0.03✱ · `త` 0.02✱ · `్రి` 1.1e-3✱ · `య` 8.5e-3✱ · `్య` 2.2e-4✱ · `␣వే` 0.50 · `గ` 0.41 · `గ` 0.16✱ · `్య` 0.02✱ · `␣శ` 0.89 · `్` 1.3e-3✱ · `త్ర` 0.43 · `మ` 0.33 · `్రమ` 1.0e-5✱ · `్ర` 3.1e-5✱ · `క` 7.6e-4✱ · `మ` 0.55 · `్యా` 1.4e-4✱ · `⏎` 1.00 |
| 3 | `శ` 1.6e-3✱ · `త` 0.92 · `ంత` 2.1e-4✱ · `ంత` 3.2e-3✱ · `ట` 0.97 · `గ` 0.97 · `్య` 0.98 · `భ` 1.1e-4✱ · `్య` 9.4e-6✱ · `స` 0.01✱ · `మ` 0.97 · `్రహ` 3.5e-5✱ · `్రి` 3.0e-5✱ · `␣ర` 1.4e-4✱ · `ర` 0.91 · `్రహ` 5.9e-7✱ · `్` 1.2e-4✱ · `⏎` 5.9e-3✱ forced |
| 4 | `త` 0.06✱ · `␣తాను` 4.2e-4✱ · `న్` 5.5e-5✱ · `య` 0.98 · `ు` 6.7e-5✱ · `గ` 0.97 · `ల్య` 5.6e-4✱ · `త` 9.3e-5✱ · `్రు` 3.2e-4✱ · `␣భ` 0.03✱ · `్ర` 1.2e-4✱ · `్వ` 6.2e-8✱ · `్` 1.0e-6✱ · `త` 3.6e-5✱ · `ర` 7.4e-4✱ · `్ర` 4.5e-7✱ · `మ` 0.93 · `్య` 4.5e-4✱ · `ము` 0.10✱ · `భ` 3.7e-3✱ · `్రు` 3.3e-4✱ · `జ` 0.95 · `్` 1.7e-10✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 86 tokens · 22.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తతివ్రల్రు మాతృమ్ర మ్ర్య్తమ్యజ్వరమ్యమ్ | `IUUIUUIUUIUU` |
| 2 | జతిమ్రమ్రకమ్యాతి ధ్ర్వ్జజ్యమ్య లోకమ్ | `IUUIUUIUUIUU` |
| 3 | మతిమ్రో మతిమ్రో దమైవమ్ర దేడన్ | `IUUIUUIUUIUU` |
| 4 | మతిన్ ట్టిం ల లేదుమ్య మమ్రత్రియై డుక్ | `IUUIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 6% · single-akshara words 19% · repeated lines 0 · mean token probability (geometric) 0.007 · model's first choice kept 29% · constraint overrode 64% · backtracks 0

<details><summary>Token probabilities (86 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.20 · `తి` 0.02 · `వ` 0.04 · `్ర` 1.1e-3✱ · `ల` 0.02 · `్రు` 5.8e-5✱ · `␣మ` 0.13 · `ాత` 0.14 · `ృ` 0.38 · `మ` 0.36 · `్ర` 8.2e-4✱ · `␣మ` 0.02✱ · `్ర` 2.6e-4✱ · `్య` 4.0e-4✱ · `్` 1.3e-7✱ · `త` 0.01✱ · `మ` 0.02✱ · `్య` 6.9e-4✱ · `జ` 1.3e-3✱ · `్వర` 1.2e-3✱ · `మ` 1.8e-3✱ · `్య` 6.6e-4✱ · `మ` 0.02✱ · `్` 2.3e-6✱ · `⏎` 0.30 forced |
| 2 | `జ` 0.10 · `తి` 0.22✱ · `మ` 0.31 · `్రమ` 6.0e-5✱ · `్ర` 3.2e-6✱ · `క` 0.97 · `మ` 1.6e-3✱ · `్యా` 6.4e-5✱ · `తి` 8.5e-3✱ · `␣ధ` 2.1e-3✱ · `్ర` 6.0e-5✱ · `్వ` 9.8e-5✱ · `్` 7.5e-6✱ · `జ` 4.0e-3✱ · `జ` 0.58 · `్య` 7.9e-4✱ · `మ` 0.59 · `్య` 0.04✱ · `␣లో` 0.80 · `క` 0.78 · `మ` 6.3e-3✱ · `్` 1.5e-7✱ · `⏎` 0.37✱ forced |
| 3 | `మ` 0.87 · `తి` 0.86 · `మ` 0.05✱ · `్రో` 4.2e-4✱ · `␣మ` 0.84 · `తి` 0.74 · `మ` 0.87 · `్రో` 2.2e-3✱ · `␣ద` 0.98 · `మై` 9.7e-6✱ · `వ` 0.99 · `మ` 0.98 · `్ర` 1.0e-4✱ · `␣ద` 0.93 · `ే` 0.99 · `డ` 0.99 · `న్` 9.2e-4✱ · `⏎` 2.1e-3✱ forced |
| 4 | `మ` 0.83 · `తి` 0.86 · `న్` 0.78 · `␣` 5.7e-4✱ · `ట్టి` 2.5e-3✱ · `ం` 6.0e-4✱ · `␣ల` 5.5e-3✱ · `␣లేదు` 1.1e-3✱ · `మ` 6.9e-4✱ · `్య` 0.02✱ · `␣మ` 0.01✱ · `మ` 0.21 · `్ర` 4.4e-4✱ · `త` 5.5e-3✱ · `్రియ` 2.9e-5✱ · `ై` 8.7e-3✱ · `␣` 3.1e-3✱ · `డు` 0.02✱ · `క` 1.3e-3✱ · `్` 3.5e-7✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 89 tokens · 36.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | లతించిప్రియిత్రిన్గె లంకన్ శరమ్రిన్ | `IUUIUUIUUIUU` |
| 2 | మతమ్రిక్యనోహత్యు జ్య్య్మయ్యెల్రునున్ వగ్ | `IUUIUUIUUIUU` |
| 3 | మతిమ్రేవియుడ్యాము జ్ర్ర్మడ్రన్ సమోతిర్ | `IUUIUUIUUIUU` |
| 4 | సొతిడ్యన్ ల్మణుప్రెన్ల సోమంచముప్రియ్ | `IUUIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.023 · model's first choice kept 60% · constraint overrode 37% · backtracks 30

<details><summary>Token probabilities (89 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ల` 0.55 · `త` 0.36 · `ించి` 6.0e-3 · `ప` 0.51 · `్రియ` 0.94 · `ిత` 0.75 · `్రి` 0.46 · `న్` 0.82 · `గ` 0.95 · `ె` 0.82 · `␣ల` 0.94 · `ంక` 0.96 · `న్` 0.57 · `␣శ` 0.94 · `ర` 0.98 · `మ` 0.96 · `్రి` 0.98 · `న్` 0.92 · `⏎` 0.98 |
| 2 | `మ` 0.98 · `త` 0.93 · `మ` 0.92 · `్రి` 0.99 · `క` 0.96 · `్య` 3.7e-6✱ · `నో` 0.98 · `హ` 0.99 · `త్య` 1.00 · `ు` 0.98 · `␣జ` 0.99 · `్య` 0.98 · `్య` 9.0e-6✱ · `్` 7.0e-7✱ · `మయ్య` 1.00 · `ె` 0.97 · `ల` 0.97 · `్రు` 4.2e-6✱ · `ను` 0.05✱ · `న్` 2.6e-3✱ · `␣వ` 1.8e-4 · `గ` 0.88 · `్` 6.1e-6✱ · `⏎` 6.0e-3✱ forced |
| 3 | `మ` 0.96 · `తి` 0.12 · `మ` 0.92 · `్రే` 2.0e-5✱ · `వి` 0.99 · `యు` 1.00 · `డ` 0.99 · `్యా` 9.0e-6✱ · `ము` 0.72 · `␣జ` 2.5e-3✱ · `్ర` 2.6e-7✱ · `్ర` 9.0e-6✱ · `్` 3.5e-7✱ · `మ` 3.0e-4✱ · `డ` 0.98 · `్ర` 2.3e-5✱ · `న్` 0.97 · `␣స` 0.99 · `మ` 0.99 · `ోతి` 1.2e-3✱ · `ర` 3.6e-4✱ · `్` 1.1e-7✱ · `⏎` 0.16✱ forced |
| 4 | `స` 0.61 · `ొ` 1.8e-3✱ · `తి` 0.99 · `డ` 1.00 · `్య` 3.0e-5✱ · `న్` 0.99 · `␣ల` 0.99 · `్` 5.8e-5✱ · `మణ` 0.89 · `ు` 9.2e-5✱ · `ప` 0.04✱ · `్ర` 1.6e-6✱ · `ె` 0.99 · `న్` 0.87 · `ల` 1.3e-4✱ · `␣స` 9.5e-3✱ · `ో` 1.2e-7✱ · `మ` 1.00 · `ంచ` 1.9e-3✱ · `ము` 0.43 · `ప` 7.7e-3✱ · `్రియ` 2.5e-5✱ · `్` 3.3e-5✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 79 tokens · 51.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జలంగ్రివ్య రూమించె సంద్రాల శిల్రా | `IUUIUUIUUIUU` |
| 2 | ములవ్రిశ్రమమ్రిశ్వు హ్ర్ర్వో చేర్చెతమ్యో | `IUUIUUIUUIUU` |
| 3 | గలెంవగ్య లంకన్ నగర్రుడ్యవస్రుత్ | `IUUIUUIUUIUU` |
| 4 | మలప్యంచుకొన్నహ్రుమత్రియ్యడున్ అం | `IUUIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.007 · model's first choice kept 37% · constraint overrode 56% · backtracks 30

<details><summary>Token probabilities (79 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.79 · `లం` 0.01 · `గ` 0.87 · `్రి` 0.95 · `వ` 0.91 · `్య` 3.1e-5✱ · `␣రూ` 6.1e-4 · `మి` 9.5e-4 · `ంచ` 1.00 · `ె` 0.95 · `␣స` 0.83 · `ంద్ర` 0.84 · `ాల` 0.83 · `␣శి` 0.30 · `ల` 0.89 · `్రా` 8.0e-4✱ · `⏎` 1.5e-6 forced |
| 2 | `ము` 3.5e-4✱ · `ల` 0.05✱ · `వ` 0.04 · `్రి` 2.8e-4✱ · `శ` 0.11 · `్రమ` 1.6e-3✱ · `మ` 0.22✱ · `్రి` 0.98 · `శ` 8.8e-4✱ · `్వ` 3.4e-6✱ · `ు` 1.6e-5✱ · `␣హ` 1.8e-4✱ · `్ర` 1.2e-4✱ · `్ర` 1.4e-6✱ · `్వ` 1.3e-6✱ · `ో` 1.1e-4✱ · `␣చే` 0.80 · `ర్చ` 0.90 · `ె` 0.58 · `త` 0.03✱ · `మ` 0.57 · `్య` 3.7e-3✱ · `ో` 0.21✱ · `⏎` 0.06✱ forced |
| 3 | `గ` 0.79 · `లె` 2.1e-3✱ · `ం` 8.8e-6✱ · `వ` 1.7e-4✱ · `గ` 0.99 · `్య` 3.2e-4✱ · `␣ల` 0.99 · `ంక` 0.92 · `న్` 1.8e-4✱ · `␣నగ` 0.99 · `ర` 0.99 · `్రు` 1.2e-6✱ · `డ` 1.00 · `్య` 3.4e-4✱ · `వ` 9.2e-3✱ · `స` 0.98 · `్రు` 2.7e-5✱ · `త` 0.98 · `్` 2.7e-8✱ · `⏎` 0.03✱ forced |
| 4 | `మ` 0.48 · `ల` 0.02✱ · `ప` 7.7e-3✱ · `్యం` 4.7e-7✱ · `చు` 1.00 · `కొ` 0.94 · `న్న` 1.6e-4✱ · `హ` 4.8e-5✱ · `్రు` 5.8e-7✱ · `మ` 0.99 · `త` 1.6e-3✱ · `్రియ` 1.5e-6✱ · `్య` 2.5e-4✱ · `డు` 6.0e-4✱ · `న్` 9.0e-3✱ · `␣` 4.2e-3✱ · `అ` 3.1e-4✱ · `ం` 2.8e-3✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 83 tokens · 26.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమల్యావతత్యుశ్యు న్ర్ర్కక్రీడు లక్యా | `IUUIUUIUUIUU` |
| 2 | నమత్రియ్రిటై రాము జ్యాసస్రసస్రా | `IUUIUUIUUIUU` |
| 3 | సమున్నింటెనున్వన్రి వ్వ్య్జజ్యంచుడుమ్యా | `IUUIUUIUUIUU` |
| 4 | సమున్ నాకు గన్నడ్రు శై యా వకుంటూ | `IUUIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 14% · repeated lines 0 · mean token probability (geometric) 0.006 · model's first choice kept 24% · constraint overrode 69% · backtracks 0

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.02✱ · `మ` 0.24 · `ల` 0.67 · `్యా` 5.8e-4✱ · `వ` 0.08 · `త` 0.17 · `త` 0.03✱ · `్య` 2.6e-4✱ · `ు` 0.17 · `శ` 0.02 · `్య` 0.01✱ · `ు` 0.06✱ · `␣న` 4.1e-3✱ · `్ర` 2.2e-5✱ · `్ర` 2.7e-4✱ · `్` 7.4e-7✱ · `క` 0.02✱ · `క` 9.2e-3✱ · `్రీ` 1.2e-3✱ · `డు` 0.08✱ · `␣ల` 3.5e-3✱ · `క` 0.23 · `్యా` 5.9e-4✱ · `⏎` 0.03 forced |
| 2 | `న` 0.11 · `మ` 0.01✱ · `త` 0.07✱ · `్రియ` 4.0e-4✱ · `్రి` 2.2e-6✱ · `ట` 0.90 · `ై` 2.1e-3✱ · `␣రా` 0.99 · `ము` 0.92 · `␣జ` 3.9e-4✱ · `్యా` 2.8e-5✱ · `స` 0.78 · `స` 0.29 · `్ర` 1.5e-4✱ · `స` 0.44 · `స` 0.28 · `్రా` 2.3e-4✱ · `⏎` 0.03 forced |
| 3 | `స` 0.27 · `ము` 0.81 · `న్ని` 0.91 · `ం` 1.1e-4✱ · `ట` 0.99 · `ె` 0.99 · `ను` 0.98 · `న` 3.7e-3✱ · `్వ` 1.3e-5✱ · `న` 0.73 · `్రి` 3.7e-5✱ · `␣వ` 0.02✱ · `్వ` 1.6e-4✱ · `్య` 4.2e-5✱ · `్` 9.1e-8✱ · `జ` 7.2e-4✱ · `జ` 0.10✱ · `్యం` 6.4e-5✱ · `చు` 0.84 · `డు` 0.84 · `మ` 2.4e-5✱ · `్యా` 1.6e-5✱ · `⏎` 0.14✱ forced |
| 4 | `స` 4.4e-3✱ · `ము` 0.01✱ · `న్` 2.9e-3✱ · `␣నాకు` 2.1e-3✱ · `␣గ` 6.3e-3✱ · `న్న` 0.02✱ · `డ` 8.7e-3✱ · `్రు` 2.1e-4✱ · `␣` 0.01✱ · `శ` 3.7e-4✱ · `ై` 1.5e-3✱ · `␣` 3.2e-3✱ · `య` 1.3e-3✱ · `ా` 1.1e-3✱ · `␣` 2.6e-3✱ · `వ` 2.6e-3✱ · `కు` 5.3e-3✱ · `ంటూ` 0.02✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 80 tokens · 13.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నిమమ్రత్రియుల్యా మ మ్య్య్నే మమ్య మమ్యా | `IUUIUUIUUIUU` |
| 2 | నిమమ్రత్రియుల్యా మమృద్యమ్య మమ్యా | `IUUIUUIUUIUU` |
| 3 | నిమమ్రత్రియుల్యా మమృత్యమ్యమమ్యా | `IUUIUUIUUIUU` |
| 4 | నిమమ్రత్రియుల్యా మమృత్యమ్య మమ్యా | `IUUIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 0% · single-akshara words 15% · repeated lines 0 · mean token probability (geometric) 0.144 · model's first choice kept 66% · constraint overrode 30% · backtracks 0

<details><summary>Token probabilities (80 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ని` 0.07 · `మ` 0.14 · `మ` 0.05✱ · `్ర` 2.9e-3✱ · `త` 0.13✱ · `్రి` 7.1e-6✱ · `యు` 0.02 · `ల` 0.14✱ · `్యా` 4.4e-4✱ · `␣మ` 0.21 · `␣మ` 0.04✱ · `్య` 1.8e-3✱ · `్య` 1.4e-3✱ · `్` 5.5e-6✱ · `న` 0.08✱ · `ే` 9.5e-4✱ · `␣మ` 0.20 · `మ` 0.09 · `్య` 5.1e-4✱ · `␣మ` 0.05 · `మ` 0.16 · `్యా` 0.01✱ · `⏎` 0.47 |
| 2 | `ని` 0.57 · `మ` 0.56 · `మ` 0.20 · `్ర` 0.07✱ · `త` 0.81 · `్రి` 0.68 · `యు` 0.76 · `ల` 0.76 · `్యా` 0.46 · `␣మ` 0.61 · `మ` 0.25 · `ృ` 6.5e-4✱ · `ద` 0.27 · `్య` 0.03✱ · `మ` 0.06✱ · `్య` 0.02✱ · `␣మ` 0.49 · `మ` 0.29✱ · `్యా` 5.1e-3✱ · `⏎` 0.37 |
| 3 | `ని` 0.96 · `మ` 0.94 · `మ` 0.95 · `్ర` 0.92 · `త` 0.99 · `్రి` 0.97 · `యు` 0.99 · `ల` 0.98 · `్యా` 0.96 · `␣మ` 0.97 · `మ` 0.95 · `ృత` 2.2e-3✱ · `్య` 0.39 · `మ` 0.91 · `్య` 0.39 · `మ` 0.49 · `మ` 0.95 · `్యా` 0.71 · `⏎` 0.99 |
| 4 | `ని` 1.00 · `మ` 0.99 · `మ` 0.98 · `్ర` 0.98 · `త` 1.00 · `్రి` 0.99 · `యు` 0.99 · `ల` 1.00 · `్యా` 0.98 · `␣మ` 0.98 · `మ` 0.97 · `ృత` 3.9e-3✱ · `్య` 0.99 · `మ` 0.97 · `్య` 0.17✱ · `␣మ` 0.77 · `మ` 1.00 · `్యా` 1.00 |

</details>

[↑ meters](#meters)

---

<a id="mattakokilamu"></a>

## 9. మత్తకోకిలము (mattakokilamu)

```text
Meter: మత్తకోకిలము (mattakokilamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 6 gaṇas: ర స జ జ భ ర, i.e. UIU IIU IUI IUI UII UIU (18 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 11th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter మత్తకోకిలము (mattakokilamu).

Meter: మత్తకోకిలము (mattakokilamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 6 gaṇas: ర స జ జ భ ర, i.e. UIU IIU IUI IUI UII UIU (18 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 11th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 126 tokens · 27.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ్రవే మమగల్యమున్ మధు జ్య్వ్గర్ర సంద్రరమున్కమల్ | `UIUIIUIUIIUIUIIUIU` |
| 2 | మమ్రియుత్ మధు జ్య్వ్గర్ర సంద్రరళన్యమగ్యమమగ్యమమ్ | `UIUIIUIUIIUIUIIUIU` |
| 3 | మమ్రియుల్యవ సంద్రమున్కమ ల్య్య్మల్యమున్ మధు జ్య్వ్గర్ర సంజ్ | `UIUIIUIUIIUIUIIUIU` |
| 4 | న్యుమ్ ర లం మలులగ్యమున్ మమయుత్య వౌ మపులుల్యు మఠ్ | `UIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 26% · repeated lines 0 · mean token probability (geometric) 0.020 · model's first choice kept 38% · constraint overrode 54% · backtracks 0

<details><summary>Token probabilities (126 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.02 · `మ` 0.19 · `్ర` 1.4e-4✱ · `వే` 0.02 · `␣మ` 0.03 · `మ` 0.05 · `గ` 0.03 · `ల` 0.03✱ · `్య` 6.8e-4✱ · `ము` 0.23 · `న్` 0.01 · `␣మ` 0.11 · `ధు` 0.04✱ · `␣జ` 8.9e-4✱ · `్య` 1.4e-3✱ · `్వ` 5.5e-4✱ · `్` 7.1e-5✱ · `గర` 3.1e-3✱ · `్ర` 4.7e-4✱ · `␣స` 0.05 · `ంద్ర` 0.06✱ · `ర` 0.31 · `ము` 0.22 · `న` 5.7e-3✱ · `్` 4.9e-7✱ · `క` 0.72 · `మ` 0.87 · `ల` 0.34 · `్` 1.7e-5✱ · `⏎` 2.7e-3✱ forced |
| 2 | `మ` 0.91 · `మ` 8.0e-3✱ · `్రి` 1.8e-6✱ · `యు` 0.07✱ · `త` 3.6e-3✱ · `్` 4.6e-5✱ · `␣మ` 0.79 · `ధు` 0.82 · `␣జ` 0.94 · `్య` 0.99 · `్వ` 0.66 · `్` 0.86 · `గర` 0.92 · `్ర` 0.37 · `␣స` 0.90 · `ంద్ర` 0.88 · `ర` 0.90 · `ళ` 3.9e-4✱ · `న` 0.92 · `్య` 7.2e-5✱ · `మ` 0.28 · `గ` 0.04✱ · `్య` 3.1e-4✱ · `మ` 0.37 · `మ` 0.75 · `గ` 0.50 · `్య` 0.01✱ · `మ` 0.06 · `మ` 0.06✱ · `్` 2.7e-4✱ · `⏎` 0.23✱ |
| 3 | `మ` 0.28 · `మ` 0.35 · `్రి` 3.4e-3✱ · `యు` 0.83 · `ల` 0.46 · `్య` 1.9e-3✱ · `వ` 0.96 · `␣స` 0.38 · `ంద్ర` 0.33 · `ము` 0.14 · `న` 0.43 · `్` 7.9e-4✱ · `క` 0.97 · `మ` 0.98 · `␣ల` 7.4e-4✱ · `్య` 1.4e-4✱ · `్య` 2.4e-3✱ · `్` 2.3e-6✱ · `మ` 0.06✱ · `ల` 0.98 · `్య` 0.98 · `ము` 0.97 · `న్` 0.92 · `␣మ` 0.93 · `ధు` 0.95 · `␣జ` 0.93 · `్య` 0.95 · `్వ` 0.86 · `్` 0.93 · `గర` 0.97 · `్ర` 3.3e-3✱ · `␣స` 0.89 · `ంజ` 0.01✱ · `్` 2.3e-6✱ · `⏎` 0.02✱ forced |
| 4 | `న్` 0.76 · `యు` 7.3e-3✱ · `మ` 1.2e-4✱ · `్` 2.6e-4✱ · `␣ర` 7.8e-5✱ · `␣ల` 2.4e-3✱ · `ం` 3.5e-3✱ · `␣మ` 4.1e-3✱ · `లు` 2.1e-3✱ · `ల` 1.4e-3✱ · `గ` 9.5e-4✱ · `్య` 0.01✱ · `ము` 0.63 · `న్` 0.18✱ · `␣మ` 2.4e-3✱ · `మ` 0.03✱ · `యు` 4.0e-4✱ · `త` 0.01✱ · `్య` 1.2e-3✱ · `␣వ` 0.01✱ · `ౌ` 8.9e-3✱ · `␣మ` 9.1e-3✱ · `పు` 0.07✱ · `లు` 0.04✱ · `ల` 7.3e-4✱ · `్య` 4.9e-4✱ · `ు` 0.02✱ · `␣మ` 4.6e-3✱ · `ఠ` 3.7e-3✱ · `్` 1.5e-7✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 115 tokens · 28.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మామురా జనె స్రీ వధున్ చరిమర్రలన్ జటలోము రామ్ | `UIUIIUIUIIUIUIIUIU` |
| 2 | శ్రీమమల్యము సూర్తనుజ్యము శీఘరమ్య లకున్ లశం | `UIUIIUIUIIUIUIIUIU` |
| 3 | మౌము సీతను మట్రచుట్రు ధ ధ్య్య్మమ్య లమ్రియనుల్రియన్ | `UIUIIUIUIIUIUIIUIU` |
| 4 | రౌ మడెన్న్ముడు ట్టిట్టి నేను ల ల్య్య్రల్రియన్ ట్టివవన్ని లమ్ | `UIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 23% · repeated lines 0 · mean token probability (geometric) 0.014 · model's first choice kept 28% · constraint overrode 57% · backtracks 0

<details><summary>Token probabilities (115 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.01 · `ము` 0.09 · `రా` 0.02 · `␣జన` 5.4e-3 · `ె` 1.4e-3 · `␣స` 0.02 · `్రీ` 6.7e-4✱ · `␣వ` 8.4e-3 · `ధ` 0.07✱ · `ు` 0.10 · `న్` 0.05✱ · `␣చ` 0.01 · `రి` 4.0e-3 · `మ` 0.03✱ · `ర` 0.05 · `్ర` 2.6e-4✱ · `ల` 0.03 · `న్` 0.17 · `␣జ` 0.14 · `ట` 0.07 · `ల` 0.07✱ · `ో` 0.01✱ · `ము` 0.04✱ · `␣` 9.1e-4✱ · `రా` 0.94 · `మ` 0.80 · `్` 4.8e-8✱ · `⏎` 0.93 |
| 2 | `శ` 0.63 · `్రీ` 0.71 · `మ` 0.15 · `మ` 0.15 · `ల` 0.12 · `్య` 1.1e-3✱ · `ము` 0.16 · `␣స` 0.04 · `ూర్` 0.03✱ · `త` 0.24 · `ను` 6.9e-3✱ · `జ` 6.0e-4✱ · `్య` 0.07✱ · `ము` 0.06✱ · `␣శ` 0.17 · `ీ` 8.6e-3✱ · `ఘ` 0.57 · `ర` 0.07 · `మ` 0.09✱ · `్య` 0.01✱ · `␣ల` 5.6e-3✱ · `కు` 0.91 · `న్` 0.93 · `␣ల` 0.02✱ · `శ` 0.88 · `ం` 2.6e-3✱ · `⏎` 0.14 |
| 3 | `మ` 0.92 · `ౌ` 4.3e-5✱ · `ము` 0.33 · `␣సీ` 0.99 · `త` 1.00 · `ను` 0.99 · `␣మ` 0.98 · `ట` 0.85 · `్ర` 1.8e-6✱ · `చు` 0.99 · `ట` 0.98 · `్రు` 2.0e-4✱ · `␣ధ` 1.00 · `␣ధ` 1.8e-5✱ · `్య` 1.5e-3✱ · `్య` 1.1e-3✱ · `్` 1.7e-6✱ · `మ` 5.7e-3✱ · `మ` 0.06✱ · `్య` 0.01✱ · `␣ల` 0.11✱ · `మ` 0.44 · `్రియ` 6.5e-4✱ · `ను` 4.6e-4✱ · `ల` 0.65 · `్రియ` 5.2e-4✱ · `న` 0.02✱ · `్` 1.4e-6✱ · `⏎` 0.02✱ forced |
| 4 | `ర` 8.0e-3✱ · `ౌ` 1.5e-5✱ · `␣మ` 9.8e-5✱ · `డ` 1.00 · `ె` 0.82 · `న్` 2.3e-3✱ · `న్` 1.8e-3✱ · `ము` 0.61 · `డు` 0.71 · `␣` 4.4e-3✱ · `ట్టి` 2.9e-4✱ · `ట్టి` 3.1e-4✱ · `␣` 3.0e-3✱ · `నే` 1.2e-3✱ · `ను` 0.01✱ · `␣ల` 0.05✱ · `␣ల` 0.06✱ · `్య` 0.01✱ · `్య` 0.01✱ · `్ర` 7.2e-5✱ · `ల` 0.04✱ · `్రియ` 2.2e-4✱ · `న్` 9.0e-4✱ · `␣` 8.7e-4✱ · `ట్టి` 1.9e-4✱ · `వ` 2.7e-3✱ · `వ` 0.01✱ · `న్ని` 1.0e-3✱ · `␣ల` 5.0e-3✱ · `మ` 5.4e-3✱ · `్` 6.4e-4✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 113 tokens · 56.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నిల్వచున్ జయ మేమతన్ మమ క్య్ర్ణీయతవ్రయడిల్రడట్ | `UIUIIUIUIIUIUIIUIU` |
| 2 | కాల్వ కన్నులుగుల్వరమ్రిరకచ్రముత్యల ప్రేమ నీమ్ | `UIUIIUIUIIUIUIIUIU` |
| 3 | కైల్వి మజ్రమరించి జల్రడె మ్గత్రు తీరపడన్ స్త సత్ | `UIUIIUIUIIUIUIIUIU` |
| 4 | తై ల్వరమ్రి మమల్వరమ్రిము మ్య్య్తస్ర జభ్వరపుల్వరమ్ | `UIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 19% · repeated lines 0 · mean token probability (geometric) 0.006 · model's first choice kept 32% · constraint overrode 64% · backtracks 30

<details><summary>Token probabilities (113 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ని` 0.88 · `ల` 1.00 · `్వ` 2.7e-5✱ · `చు` 0.88 · `న్` 0.83 · `␣జ` 0.45 · `య` 0.12✱ · `␣మే` 0.98 · `మ` 0.89 · `త` 0.98 · `న్` 0.94 · `␣మ` 0.68 · `మ` 0.93 · `␣క` 0.90 · `్య` 2.5e-5✱ · `్ర` 6.2e-4✱ · `్` 1.2e-6✱ · `ణ` 0.10✱ · `ీయ` 0.86 · `త` 0.93 · `వ` 0.06✱ · `్ర` 9.2e-7✱ · `య` 3.0e-3 · `డి` 3.4e-3 · `ల` 0.05✱ · `్ర` 1.0e-4✱ · `డ` 0.11✱ · `ట` 0.44 · `్` 7.1e-10✱ · `⏎` 0.09✱ forced |
| 2 | `కా` 0.93 · `ల` 2.6e-4✱ · `్వ` 1.9e-5✱ · `␣క` 4.4e-3 · `న్ను` 9.8e-4✱ · `లుగు` 3.3e-4 · `ల` 0.37 · `్వర` 1.2e-4✱ · `మ` 0.32✱ · `్రి` 6.8e-7✱ · `ర` 0.95 · `క` 1.8e-5✱ · `చ` 1.3e-4✱ · `్ర` 5.8e-5✱ · `ము` 2.4e-3✱ · `త` 0.17✱ · `్య` 2.2e-6✱ · `ల` 0.05✱ · `␣ప్రేమ` 0.54 · `␣నీ` 0.30 · `మ` 0.60 · `్` 2.7e-7✱ · `⏎` 3.2e-3✱ forced |
| 3 | `క` 0.87 · `ై` 1.7e-3✱ · `ల్` 7.1e-5✱ · `వి` 2.6e-4✱ · `␣మ` 0.03✱ · `జ` 0.49 · `్ర` 3.8e-4✱ · `మ` 1.00 · `రించి` 4.4e-4✱ · `␣జ` 1.00 · `ల` 1.00 · `్ర` 5.1e-5✱ · `డ` 1.00 · `ె` 0.98 · `␣మ` 0.99 · `్` 6.6e-9✱ · `గ` 0.05✱ · `త` 0.01✱ · `్రు` 3.6e-7✱ · `␣తీ` 0.98 · `ర` 1.00 · `ప` 1.00 · `డ` 1.00 · `న్` 0.99 · `␣` 5.2e-3✱ · `స్త` 1.4e-3✱ · `␣` 2.3e-3✱ · `స` 7.1e-5✱ · `త` 5.8e-4✱ · `్` 1.1e-4✱ · `⏎` 0.21✱ forced |
| 4 | `త` 7.9e-3✱ · `ై` 0.02✱ · `␣` 4.0e-3✱ · `ల` 0.01✱ · `్వర` 9.7e-4✱ · `మ` 0.07✱ · `్రి` 0.01✱ · `␣మ` 0.22 · `మ` 0.06 · `ల` 0.01✱ · `్వర` 1.1e-5✱ · `మ` 0.02✱ · `్రి` 3.0e-3✱ · `ము` 9.1e-3✱ · `␣మ` 0.02✱ · `్య` 5.8e-5✱ · `్య` 3.1e-4✱ · `్` 1.6e-7✱ · `త` 1.4e-4✱ · `స` 0.05✱ · `్ర` 9.4e-4✱ · `␣జ` 0.87 · `భ` 0.04✱ · `్వర` 2.3e-4✱ · `పు` 5.9e-4✱ · `ల` 0.03✱ · `్వర` 1.9e-5✱ · `మ` 0.11✱ · `్` 1.4e-3✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 108 tokens · 51.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ్రుకన్ నిడపోల్లెచడ్య్యు కకాలమమ్యముయుప్రుతమ్ | `UIUIIUIUIIUIUIIUIU` |
| 2 | డమ్రిటచ్యమమల్యతిమ్యమలయ్యమాతి నిడల్లొడడ్ | `UIUIIUIUIIUIUIIUIU` |
| 3 | కుమ్రమమ్యమయుల్యతిమ్యమ డ్య్య్గూవకుమ్యమముక్యముత్ | `UIUIIUIUIIUIUIIUIU` |
| 4 | వామ్ర లీ సరి దిద్దు బట్టి ది పాట నియ్రమమర్ర జడ్ | `UIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 19% · repeated lines 0 · mean token probability (geometric) 0.012 · model's first choice kept 34% · constraint overrode 57% · backtracks 30

<details><summary>Token probabilities (108 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.99 · `మ` 0.99 · `్రు` 3.3e-7✱ · `క` 0.05 · `న్` 0.82 · `␣ని` 0.92 · `డ` 0.05 · `పో` 5.5e-4 · `ల్ల` 0.68 · `ె` 0.03 · `చ` 3.6e-3✱ · `డ` 0.01 · `్య` 7.1e-5✱ · `్య` 0.98 · `ు` 0.97 · `␣క` 0.02✱ · `కాల` 9.6e-6✱ · `మ` 0.20 · `మ` 0.68 · `్య` 0.52 · `ము` 0.58 · `యు` 2.6e-3✱ · `ప` 0.02✱ · `్రు` 4.3e-5✱ · `త` 0.31 · `మ` 0.32 · `్` 1.2e-6✱ · `⏎` 1.7e-4✱ forced |
| 2 | `డ` 0.55 · `మ` 0.02✱ · `్రి` 3.9e-6✱ · `ట` 0.01 · `చ` 0.17 · `్య` 4.3e-6✱ · `మ` 0.93 · `మ` 1.9e-3✱ · `ల` 0.18 · `్య` 1.7e-6✱ · `తి` 0.81 · `మ` 0.08✱ · `్య` 1.2e-3✱ · `మ` 0.58 · `ల` 0.01✱ · `య` 6.8e-3✱ · `్య` 6.9e-6✱ · `మా` 0.79 · `తి` 0.73 · `␣ని` 0.78 · `డ` 0.96 · `ల్ల` 2.2e-3✱ · `ొ` 1.1e-3✱ · `డ` 0.13✱ · `డ` 0.41✱ · `్` 2.8e-5✱ · `⏎` 3.0e-3✱ forced |
| 3 | `క` 0.28✱ · `ు` 0.28 · `మ` 0.21✱ · `్ర` 1.9e-3✱ · `మ` 0.28 · `మ` 0.62 · `్య` 0.06✱ · `మ` 0.85 · `యు` 0.48 · `ల` 0.95 · `్య` 1.3e-4✱ · `తి` 0.98 · `మ` 2.6e-3✱ · `్య` 1.9e-5✱ · `మ` 0.09✱ · `␣డ` 1.4e-4✱ · `్య` 0.02✱ · `్య` 0.04✱ · `్` 4.8e-5✱ · `గ` 4.0e-4✱ · `ూ` 1.3e-5✱ · `వ` 0.02 · `కు` 0.22 · `మ` 0.76 · `్య` 8.1e-4✱ · `మ` 0.97 · `ము` 0.84 · `క` 2.3e-5✱ · `్య` 4.4e-4✱ · `ము` 3.3e-3✱ · `త` 1.0e-3✱ · `్` 8.5e-4✱ · `⏎` 0.30✱ forced |
| 4 | `వా` 1.3e-3✱ · `మ` 6.6e-3✱ · `్ర` 4.9e-5✱ · `␣ల` 2.5e-3✱ · `ీ` 6.2e-3✱ · `␣సరి` 0.06✱ · `␣ది` 0.03✱ · `ద్దు` 0.51 · `␣బ` 0.07 · `ట్టి` 0.22✱ · `␣ది` 0.02✱ · `␣పాట` 2.1e-3✱ · `␣నియ` 0.11 · `్రమ` 1.2e-4✱ · `మ` 1.7e-3✱ · `ర` 0.83 · `్ర` 1.2e-3✱ · `␣జ` 0.89 · `డ` 3.4e-3✱ · `్` 2.7e-8✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 105 tokens · 28.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీరముర్రి శతక్రి సఘ్రము ల్య్రిందు వెళ్ళెను శ్రీమతీ | `UIUIIUIUIIUIUIIUIU` |
| 2 | మారి మత్రి మకల్రి లందు వె శ్య్య్మాకమక్తికమారి మా | `UIUIIUIUIIUIUIIUIU` |
| 3 | తారకధ్రి లుడున్ళ్ళెనుల్రక మ్ర్ర్దమ్రినిమ్రిల లల్ల వెన్ | `UIUIIUIUIIUIUIIUIU` |
| 4 | మౌరమాలిము రాము లందు వెనల్యముల్య లలల్రిరీ | `UIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 22% · single-akshara words 13% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 30% · constraint overrode 62% · backtracks 0

<details><summary>Token probabilities (105 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.25 · `్రీ` 0.76 · `ర` 0.22✱ · `ము` 0.42 · `ర` 8.6e-3✱ · `్రి` 4.2e-4✱ · `␣శ` 0.08 · `త` 0.26 · `క` 0.12 · `్రి` 0.01✱ · `␣స` 0.03 · `ఘ` 2.2e-3✱ · `్ర` 0.06✱ · `ము` 0.37 · `␣ల` 0.57 · `్య` 6.2e-4✱ · `్రి` 8.3e-6✱ · `ందు` 1.4e-3✱ · `␣వె` 0.97 · `ళ్ళ` 0.93 · `ె` 0.97 · `ను` 0.97 · `␣` 1.4e-3✱ · `శ` 0.98 · `్రీ` 0.98 · `మ` 0.85 · `తీ` 5.1e-4 · `⏎` 2.0e-4✱ forced |
| 2 | `మ` 0.49 · `ారి` 0.06✱ · `␣మ` 0.18 · `త` 0.03✱ · `్రి` 6.9e-5✱ · `␣మ` 0.08 · `క` 0.09 · `ల` 0.13✱ · `్రి` 3.2e-3✱ · `␣ల` 0.31 · `ందు` 0.26 · `␣వె` 0.91 · `␣శ` 1.7e-6✱ · `్య` 9.7e-5✱ · `్య` 1.9e-4✱ · `్` 6.6e-7✱ · `మా` 1.2e-3✱ · `క` 0.87 · `మ` 0.45 · `క్తి` 1.6e-3✱ · `క` 2.1e-3✱ · `మ` 0.22 · `ారి` 2.9e-3✱ · `␣మా` 6.8e-4 · `⏎` 1.0e-3 forced |
| 3 | `త` 0.02✱ · `ార` 8.9e-3✱ · `క` 0.43 · `ధ` 0.27 · `్రి` 0.26 · `␣ల` 0.76 · `ుడు` 3.8e-3✱ · `న్` 8.3e-5✱ · `ళ్ళ` 0.99 · `ె` 0.96 · `ను` 0.99 · `ల` 4.9e-5✱ · `్ర` 4.2e-6✱ · `క` 0.93 · `␣మ` 0.03✱ · `్ర` 1.1e-4✱ · `్ర` 9.9e-5✱ · `్` 2.2e-5✱ · `ద` 7.4e-3✱ · `మ` 9.6e-3✱ · `్రి` 1.2e-5✱ · `ని` 0.01✱ · `మ` 0.20✱ · `్రి` 8.2e-4✱ · `ల` 0.89 · `␣ల` 0.15✱ · `ల్ల` 0.08✱ · `␣వె` 0.02✱ · `న్` 7.4e-3✱ · `⏎` 1.6e-3✱ forced |
| 4 | `మ` 0.04✱ · `ౌ` 2.0e-4✱ · `ర` 3.3e-4✱ · `మ` 0.99 · `ాలి` 3.6e-4✱ · `ము` 2.2e-4✱ · `␣రా` 2.8e-3✱ · `ము` 0.02✱ · `␣ల` 0.06✱ · `ందు` 0.19✱ · `␣వె` 0.26 · `న` 0.03✱ · `ల` 2.6e-3✱ · `్య` 1.3e-4✱ · `ము` 6.4e-3✱ · `ల` 9.4e-4✱ · `్య` 1.0e-3✱ · `␣ల` 0.02✱ · `ల` 9.3e-3✱ · `ల` 3.2e-3✱ · `్రి` 1.2e-3✱ · `రీ` 2.2e-3✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 118 tokens · 30.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జన్తమున్రతకమ్రదమ్య మ మ్ర్య్జక్రురుణ్యమ నిల్వొలగ్ | `UIUIIUIUIIUIUIIUIU` |
| 2 | విన్ తరవ్రి మ తృత్వమున్ మమ క్ర్వ్వీల రూపము లోల లో | `UIUIIUIUIIUIUIIUIU` |
| 3 | కైన్తముక్రి మమోతి యద్రివ వ్వ్య్కక్రఈ ప ప లో గతిప్ | `UIUIIUIUIIUIUIIUIU` |
| 4 | కాన్తసిమ్రహి రాయనుంతతి జ్న్ర్కత్యనమ్ మమ వన్రుపున్ | `UIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 15% · single-akshara words 27% · repeated lines 0 · mean token probability (geometric) 0.005 · model's first choice kept 30% · constraint overrode 63% · backtracks 0

<details><summary>Token probabilities (118 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.45 · `న్` 0.25 · `త` 0.04 · `ము` 0.06 · `న` 0.05✱ · `్ర` 7.4e-5✱ · `త` 0.03 · `క` 0.08 · `మ` 0.15 · `్ర` 1.5e-3✱ · `ద` 0.05 · `మ` 0.16 · `్య` 5.4e-3✱ · `␣మ` 0.13 · `␣మ` 0.04✱ · `్ర` 2.1e-3✱ · `్య` 1.2e-4✱ · `్` 2.1e-7✱ · `జ` 0.01✱ · `క` 7.0e-3✱ · `్రు` 4.0e-6✱ · `రుణ` 0.37 · `్య` 0.01✱ · `మ` 0.10 · `␣ని` 0.20 · `ల` 0.23 · `్వ` 5.7e-5✱ · `ొ` 0.61 · `ల` 0.63 · `గ` 0.06 · `్` 4.0e-6✱ · `⏎` 8.4e-6✱ forced |
| 2 | `వ` 0.85 · `ిన` 2.3e-3✱ · `్` 7.7e-7✱ · `␣తర` 9.0e-4✱ · `వ` 0.80 · `్రి` 4.0e-5✱ · `␣మ` 0.56 · `␣త` 0.97 · `ృ` 0.98 · `త్వ` 0.99 · `ము` 0.80 · `న్` 0.01✱ · `␣మ` 0.32 · `మ` 0.11 · `␣క` 0.11✱ · `్ర` 2.6e-4✱ · `్వ` 4.9e-6✱ · `్వ` 3.3e-5✱ · `ీల` 3.8e-4✱ · `␣రూప` 0.97 · `ము` 0.13✱ · `␣లో` 0.23✱ · `ల` 0.52 · `␣లో` 0.02✱ · `⏎` 0.13✱ forced |
| 3 | `క` 0.98 · `ై` 4.6e-4✱ · `న` 4.2e-3✱ · `్` 9.2e-9✱ · `త` 2.0e-4✱ · `ము` 0.98 · `క` 4.0e-4✱ · `్రి` 1.0e-4✱ · `␣మ` 0.51 · `మ` 0.77 · `ోతి` 6.6e-3✱ · `␣య` 0.89 · `ద` 2.6e-3✱ · `్రి` 4.6e-4✱ · `వ` 0.87 · `␣వ` 5.0e-3✱ · `్వ` 2.0e-5✱ · `్య` 2.2e-5✱ · `్` 1.1e-7✱ · `క` 4.3e-3✱ · `క` 0.02✱ · `్ర` 7.8e-6✱ · `ఈ` 5.4e-3✱ · `␣ప` 0.99 · `␣ప` 1.0e-3✱ · `␣లో` 0.05✱ · `␣గ` 0.81 · `తి` 1.00 · `ప` 3.8e-3✱ · `్` 2.3e-8✱ · `⏎` 0.02✱ forced |
| 4 | `కా` 1.7e-3✱ · `న` 0.04✱ · `్` 1.1e-8✱ · `త` 5.5e-5✱ · `సి` 0.97 · `మ` 9.1e-4✱ · `్రహ` 4.2e-6✱ · `ి` 2.7e-3✱ · `␣రాయ` 0.98 · `ను` 6.1e-3✱ · `ంత` 3.3e-5✱ · `తి` 0.88 · `␣జ` 6.8e-5✱ · `్` 1.8e-3✱ · `న` 0.02✱ · `్ర` 9.0e-6✱ · `్` 8.9e-7✱ · `క` 1.4e-5✱ · `త` 0.97 · `్య` 1.0e-4✱ · `న` 0.72 · `మ` 6.4e-3✱ · `్` 3.4e-5✱ · `␣మ` 0.03✱ · `మ` 0.16✱ · `␣వ` 0.02✱ · `న` 0.10 · `్రు` 6.5e-4✱ · `పు` 0.03✱ · `న్` 0.01 |

</details>

[↑ meters](#meters)

---

<a id="pamcacamaramu"></a>

## 10. పంచచామరము (pamcacamaramu)

```text
Meter: పంచచామరము (pamcacamaramu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 6 gaṇas: జ ర జ ర జ గురువు, i.e. IUI UIU IUI UIU IUI U (16 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 10th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter పంచచామరము (pamcacamaramu).

Meter: పంచచామరము (pamcacamaramu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 6 gaṇas: జ ర జ ర జ గురువు, i.e. IUI UIU IUI UIU IUI U (16 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 10th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 101 tokens · 25.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కరుణ్రు లం మనిక్రు లమ్య ద్ర్ర్కక్రికల్రిమమ్య యమ్ | `IUIUIUIUIUIUIUIU` |
| 2 | కరిల్రు లం జగన్నికై ల ల్య్య్ఘవ్రిజగ్రిమమ్య యమ్ | `IUIUIUIUIUIUIUIU` |
| 3 | ఇ రాత పైన ఉన్న ఉన్న త్యించమర్య ఇచ్చినయ్ | `IUIUIUIUIUIUIUIU` |
| 4 | అరింత రాసినప్యమున్న్న వ్ర్ర్యజ్ర రజ్ర జుర్రరమ్ | `IUIUIUIUIUIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 25% · repeated lines 0 · mean token probability (geometric) 0.011 · model's first choice kept 27% · constraint overrode 67% · backtracks 0

<details><summary>Token probabilities (101 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.06 · `రుణ` 0.17 · `్రు` 1.0e-4✱ · `␣ల` 0.01 · `ం` 2.5e-3✱ · `␣మ` 0.10 · `ని` 0.01 · `క` 0.01✱ · `్రు` 2.4e-5✱ · `␣ల` 0.26 · `మ` 0.04✱ · `్య` 6.8e-3✱ · `␣ద` 0.10✱ · `్ర` 3.6e-3✱ · `్ర` 6.5e-5✱ · `్` 4.6e-6✱ · `క` 0.05✱ · `క` 0.03✱ · `్రి` 3.4e-4✱ · `క` 0.05✱ · `ల` 0.05✱ · `్రి` 2.2e-4✱ · `మ` 0.12✱ · `మ` 0.05✱ · `్య` 5.9e-5✱ · `␣య` 2.2e-3✱ · `మ` 0.92 · `్` 2.9e-7✱ · `⏎` 0.70 |
| 2 | `క` 0.76 · `రి` 9.1e-4✱ · `ల` 0.04 · `్రు` 1.1e-3✱ · `␣ల` 8.5e-3✱ · `ం` 0.09✱ · `␣జగ` 0.04 · `న్ని` 2.0e-3✱ · `క` 0.57 · `ై` 0.19 · `␣ల` 0.72 · `␣ల` 4.8e-3✱ · `్య` 0.97 · `్య` 1.5e-3✱ · `్` 3.4e-3✱ · `ఘ` 4.6e-4✱ · `వ` 0.85 · `్రి` 1.6e-5✱ · `జ` 0.97 · `గ` 0.82 · `్రి` 0.03✱ · `మ` 0.12 · `మ` 0.84 · `్య` 0.83 · `␣య` 0.87 · `మ` 0.94 · `్` 0.78 · `⏎` 2.9e-3✱ forced |
| 3 | `ఇ` 0.96 · `␣ర` 8.0e-7✱ · `ాత` 1.2e-4✱ · `␣ప` 0.06✱ · `ైన` 0.65 · `␣ఉన్న` 0.06✱ · `␣ఉన్న` 0.14✱ · `␣త` 0.01✱ · `్య` 5.9e-3✱ · `ించ` 1.4e-3✱ · `మ` 0.28 · `ర` 0.02✱ · `్య` 9.0e-4✱ · `␣ఇచ్చిన` 0.41 · `య` 1.2e-5✱ · `్` 7.9e-8✱ · `⏎` 0.12✱ forced |
| 4 | `అ` 6.6e-3✱ · `రి` 8.2e-3✱ · `ంత` 1.2e-3✱ · `␣రా` 0.98 · `సిన` 0.99 · `ప` 1.1e-3✱ · `్య` 5.8e-4✱ · `ము` 0.96 · `న్` 4.5e-3✱ · `న్` 1.4e-3✱ · `న` 0.03✱ · `␣వ` 0.01✱ · `్ర` 9.0e-4✱ · `్ర` 2.7e-4✱ · `్య` 2.2e-4✱ · `జ` 0.02✱ · `్ర` 2.9e-3✱ · `␣ర` 0.65 · `జ` 0.02✱ · `్ర` 1.6e-3✱ · `␣జ` 0.74 · `ు` 1.3e-3✱ · `ర` 5.4e-3✱ · `్ర` 3.2e-5✱ · `ర` 0.05✱ · `మ` 0.03✱ · `్` 4.1e-4✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 115 tokens · 22.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కడగ్య సంములర్రి శం గ జ్ర్ర్కల్రు రామ భైముడై | `IUIUIUIUIUIUIUIU` |
| 2 | మడల్య మౌ తనగ్ జునక్ర్రు ల్య్య్మండెడన్టవడ్య్య మౌ | `IUIUIUIUIUIUIUIU` |
| 3 | న డుజ్రునక్ర్రు శౌభ్యనుడ్రనాయవడ్య మౌయనన్ | `IUIUIUIUIUIUIUIU` |
| 4 | జుడక్ర్రు జేయ హుమ్రుడున్రు క్ష్యోపపైన ఇచ్చినప్ | `IUIUIUIUIUIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 23% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 43% · constraint overrode 45% · backtracks 0

<details><summary>Token probabilities (115 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.04 · `డ` 0.02 · `గ` 0.02 · `్య` 3.3e-4✱ · `␣సం` 6.7e-3 · `ము` 0.06 · `ల` 0.03 · `ర` 0.14 · `్రి` 1.6e-4✱ · `␣శ` 0.07 · `ం` 0.03 · `␣గ` 8.7e-3 · `␣జ` 0.06✱ · `్ర` 3.1e-4✱ · `్ర` 9.2e-4✱ · `్` 8.5e-5✱ · `క` 7.6e-3✱ · `ల` 0.03✱ · `్ర` 7.6e-4✱ · `ు` 0.24 · `␣రామ` 1.1e-3 · `␣భ` 0.13 · `ై` 0.07 · `ము` 0.04 · `డ` 0.27 · `ై` 0.07✱ · `⏎` 0.54 |
| 2 | `మ` 0.47 · `డ` 0.08✱ · `ల` 0.37 · `్య` 3.8e-5✱ · `␣మ` 0.45 · `ౌ` 0.25 · `␣త` 3.9e-3 · `న` 0.18 · `గ` 0.09✱ · `్` 1.1e-5✱ · `␣జ` 0.27 · `ు` 0.49 · `న` 0.06✱ · `క` 0.53 · `్ర` 8.1e-4✱ · `్ర` 0.53 · `ు` 0.86 · `␣ల` 0.98 · `్య` 1.3e-6✱ · `్య` 1.2e-5✱ · `్` 1.3e-10✱ · `మ` 8.4e-5✱ · `ండె` 0.02✱ · `డ` 0.97 · `న్` 0.97 · `ట` 3.9e-4✱ · `వ` 0.88 · `డ` 0.98 · `్య` 3.6e-5✱ · `్య` 0.99 · `␣మ` 0.98 · `ౌ` 0.99 · `⏎` 9.5e-6✱ forced |
| 3 | `న` 0.98 · `␣` 1.3e-6✱ · `డు` 0.03✱ · `జ` 2.0e-4✱ · `్రు` 3.6e-4✱ · `న` 0.95 · `క` 0.98 · `్ర` 3.2e-6✱ · `్ర` 0.90 · `ు` 0.96 · `␣శ` 1.00 · `ౌ` 0.99 · `భ` 0.99 · `్య` 0.99 · `ను` 0.96 · `డ` 3.5e-5✱ · `్ర` 1.4e-4✱ · `న` 0.01✱ · `ాయ` 4.5e-4✱ · `వ` 0.87 · `డ` 0.93 · `్య` 7.0e-3✱ · `␣మ` 0.40 · `ౌ` 0.08✱ · `య` 9.2e-4✱ · `న` 0.13✱ · `న` 0.67 · `్` 3.7e-6✱ · `⏎` 0.13✱ forced |
| 4 | `␣జ` 0.63 · `ు` 0.92 · `డ` 1.5e-4✱ · `క` 0.99 · `్ర` 2.1e-7✱ · `్ర` 0.99 · `ు` 0.95 · `␣జ` 1.00 · `ే` 1.00 · `య` 0.96 · `␣హ` 1.00 · `ు` 6.4e-4✱ · `మ` 6.5e-4✱ · `్రు` 1.4e-6✱ · `డు` 0.99 · `న` 5.7e-5✱ · `్రు` 1.2e-5✱ · `␣క్ష` 5.6e-4✱ · `్య` 1.4e-6✱ · `ో` 1.6e-5✱ · `ప` 6.0e-3✱ · `ప` 0.98 · `ైన` 0.99 · `␣ఇచ్చిన` 0.79 · `ప` 1.5e-4✱ · `్` 2.0e-9✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 103 tokens · 57.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమల్రరణ్య రామణుడ్రి వ్వ్స్గన్ మసమ్వరస్రుతా | `IUIUIUIUIUIUIUIU` |
| 2 | సిమంగచిట్ర కుల్లెరజ్రి జేతరామముస్రమధ్ | `IUIUIUIUIUIUIUIU` |
| 3 | శ్రముట్లు నాశ తుంచు ఆప వ్య్య్రత్రి రక్షుటన్ లొకడ్ | `IUIUIUIUIUIUIUIU` |
| 4 | ట్టి ముట్టి ముశ్యమున్డు వేడు గ్య్వ్టించుచుప్పుడుప్పుడుజ్ | `IUIUIUIUIUIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 16% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.008 · model's first choice kept 38% · constraint overrode 56% · backtracks 30

<details><summary>Token probabilities (103 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.99 · `మ` 0.79 · `ల` 0.94 · `్ర` 2.0e-5✱ · `ర` 1.9e-3 · `ణ` 0.95 · `్య` 0.96 · `␣రా` 0.20 · `మణ` 0.99 · `ు` 0.99 · `డ` 0.04 · `్రి` 0.61 · `␣వ` 0.89 · `్వ` 0.94 · `్` 0.93 · `స` 0.02 · `్` 5.9e-10✱ · `గ` 6.5e-4✱ · `న్` 0.98 · `␣మ` 0.76 · `స` 0.99 · `మ` 0.90 · `్వర` 1.9e-6✱ · `స` 1.0e-3✱ · `్రు` 4.4e-7✱ · `తా` 0.07 · `⏎` 0.96 |
| 2 | `సి` 0.98 · `మ` 0.96 · `ంగ` 1.00 · `చి` 0.14✱ · `ట` 3.2e-4✱ · `్ర` 9.1e-5✱ · `␣కు` 0.08 · `ల్ల` 1.0e-5✱ · `ె` 1.1e-3✱ · `ర` 1.00 · `జ` 1.5e-4✱ · `్రి` 1.8e-6✱ · `␣జ` 0.99 · `ే` 6.3e-4✱ · `త` 7.2e-3✱ · `రా` 0.96 · `మ` 0.92 · `ము` 0.01✱ · `స` 0.70 · `్రమ` 6.9e-4✱ · `ధ` 0.04✱ · `్` 9.9e-5✱ · `⏎` 0.13✱ forced |
| 3 | `శ` 0.70 · `్రమ` 1.6e-4✱ · `ు` 0.56 · `ట్లు` 8.4e-6✱ · `␣నా` 0.98 · `శ` 1.00 · `␣తు` 4.3e-5✱ · `ం` 0.01✱ · `చు` 1.00 · `␣ఆ` 0.83 · `ప` 0.99 · `␣వ` 3.5e-4✱ · `్య` 2.5e-5✱ · `్య` 3.3e-6✱ · `్ర` 3.2e-6✱ · `త` 0.99 · `్రి` 2.6e-6✱ · `␣ర` 0.98 · `క్ష` 1.00 · `ు` 1.9e-3✱ · `ట` 0.99 · `న్` 0.96 · `␣ల` 0.32 · `ొ` 1.1e-4✱ · `క` 0.14✱ · `డ` 1.00 · `్` 1.7e-10✱ · `⏎` 4.7e-3✱ forced |
| 4 | `␣` 5.2e-4✱ · `ట్టి` 1.4e-4✱ · `␣` 4.0e-4✱ · `ము` 9.4e-7✱ · `ట్టి` 8.3e-5✱ · `␣ము` 3.2e-3✱ · `శ` 5.0e-3✱ · `్య` 0.03✱ · `ము` 0.35 · `న్` 0.05✱ · `డు` 3.7e-4✱ · `␣వే` 0.02✱ · `డు` 3.4e-3✱ · `␣గ` 1.2e-4✱ · `్య` 2.5e-3✱ · `్వ` 1.2e-4✱ · `్` 8.7e-6✱ · `ట` 3.9e-4✱ · `ించ` 5.5e-3✱ · `ు` 0.06✱ · `చు` 0.13✱ · `ప్పుడు` 5.2e-3✱ · `ప్పుడు` 8.0e-3✱ · `జ` 0.01✱ · `్` 1.8e-5✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 102 tokens · 55.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నిమస్ర రమ్యమత్రి లోక నేరవన్డు ధధ్వజల్ | `IUIUIUIUIUIUIUIU` |
| 2 | నిమల్వరమ్య లోక లోమజృడ్య ఏడతిమ్వరమ్ | `IUIUIUIUIUIUIUIU` |
| 3 | తిమక్యడమ్య ఏడతిమ్యతిమ్యమత్రికత్యమల్ | `IUIUIUIUIUIUIUIU` |
| 4 | తిమల్య్లుతిత్వముమ్ మముల్య మ్య్య్లెల్వరర్రముమ్రుమౌ | `IUIUIUIUIUIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 36% · constraint overrode 58% · backtracks 30

<details><summary>Token probabilities (102 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ని` 0.57 · `మ` 0.70 · `స` 0.01 · `్ర` 0.95 · `␣ర` 1.6e-3 · `మ` 0.10 · `్య` 1.00 · `మ` 0.53 · `త` 0.98 · `్రి` 0.94 · `␣లో` 1.00 · `క` 0.92 · `␣నే` 1.7e-4 · `ర` 0.97 · `వ` 0.86 · `న్` 1.1e-3✱ · `డు` 0.93 · `␣ధ` 2.3e-3 · `ధ` 0.51 · `్వ` 5.1e-6✱ · `జ` 0.87 · `ల` 0.93 · `్` 1.4e-7✱ · `⏎` 2.0e-5✱ forced |
| 2 | `ని` 0.17 · `మ` 0.29 · `ల` 0.02✱ · `్వర` 1.9e-5✱ · `మ` 0.04✱ · `్య` 3.7e-4✱ · `␣లో` 0.65 · `క` 0.59 · `␣లో` 0.08 · `మ` 0.42 · `జ` 3.3e-3✱ · `ృ` 1.2e-4✱ · `డ` 0.99 · `్య` 1.4e-3✱ · `␣ఏ` 0.22 · `డ` 0.78 · `తి` 0.72 · `మ` 0.05✱ · `్వర` 1.8e-5✱ · `మ` 0.33 · `్` 3.8e-6✱ · `⏎` 0.16✱ forced |
| 3 | `తి` 0.48 · `మ` 1.1e-3✱ · `క` 0.79 · `్య` 4.0e-7✱ · `డ` 0.94 · `మ` 0.79 · `్య` 2.1e-3✱ · `␣ఏ` 0.99 · `డ` 0.98 · `తి` 0.85 · `మ` 0.02✱ · `్య` 8.9e-5✱ · `తి` 0.57 · `మ` 0.04✱ · `్య` 0.02✱ · `మ` 0.84 · `త` 0.01✱ · `్రి` 0.04✱ · `క` 0.35 · `త` 1.9e-4✱ · `్య` 1.2e-4✱ · `మ` 0.84 · `ల` 0.01✱ · `్` 5.4e-6✱ · `⏎` 0.01✱ forced |
| 4 | `తి` 0.57 · `మ` 2.0e-3✱ · `ల` 1.8e-3✱ · `్య` 9.2e-4✱ · `్` 8.2e-3✱ · `లు` 5.7e-4✱ · `తి` 9.9e-3✱ · `త్వ` 2.5e-3✱ · `ము` 0.04✱ · `మ` 2.8e-3✱ · `్` 9.3e-5✱ · `␣` 9.5e-3✱ · `మ` 0.01✱ · `ము` 0.02✱ · `ల` 3.9e-3✱ · `్య` 9.5e-4✱ · `␣మ` 4.1e-3✱ · `్య` 1.5e-4✱ · `్య` 4.8e-4✱ · `్` 3.7e-5✱ · `ల` 4.3e-3✱ · `ెల` 5.2e-4✱ · `్వర` 1.8e-4✱ · `ర` 0.01✱ · `్ర` 1.0e-4✱ · `ము` 9.6e-4✱ · `మ` 1.5e-3✱ · `్ర` 6.5e-3✱ · `ు` 8.7e-3✱ · `మ` 0.02✱ · `ౌ` 1.7e-3✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 99 tokens · 26.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మకర్రిముగ్యమౌ మదిత్రు న్వ్య్మమ్యహీమముమ్య సా | `IUIUIUIUIUIUIUIU` |
| 2 | సకల్రి దాటి సక్రి నన్ ము చక్కనున్మరియ్య జే | `IUIUIUIUIUIUIUIU` |
| 3 | జకుల్యముద్రమమ్యడున్య హ్య్య్జగ్యమాని లంకలో | `IUIUIUIUIUIUIUIU` |
| 4 | రృ కుట్లునుర్యడున్యడున్రరేరమయ్యముమ్య సా | `IUIUIUIUIUIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 35% · repeated lines 0 · mean token probability (geometric) 0.010 · model's first choice kept 26% · constraint overrode 60% · backtracks 0

<details><summary>Token probabilities (99 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.45 · `క` 0.03 · `ర` 0.03 · `్రి` 6.2e-6✱ · `ము` 0.08 · `గ` 0.09 · `్య` 3.4e-4✱ · `మ` 0.16 · `ౌ` 0.01✱ · `␣మ` 0.14 · `ది` 0.02✱ · `త` 0.02 · `్ర` 3.7e-5✱ · `ు` 0.10✱ · `␣న` 0.04 · `్వ` 7.6e-5✱ · `్య` 1.4e-5✱ · `్` 9.8e-7✱ · `మ` 0.04✱ · `మ` 6.2e-3✱ · `్య` 9.2e-5✱ · `హ` 0.69 · `ీ` 0.77 · `మ` 0.53 · `ము` 0.08✱ · `మ` 0.14 · `్య` 3.8e-4✱ · `␣సా` 0.02✱ · `⏎` 0.12 forced |
| 2 | `స` 0.24 · `క` 0.02✱ · `ల` 0.24 · `్రి` 2.8e-4✱ · `␣దా` 0.13 · `టి` 0.52 · `␣స` 0.13 · `క` 0.03✱ · `్రి` 2.4e-3✱ · `␣న` 0.03 · `న్` 0.04✱ · `␣ము` 0.01 · `␣చక్క` 9.7e-4✱ · `ను` 0.88 · `న్` 2.3e-4✱ · `మ` 0.94 · `రి` 0.98 · `య` 1.4e-3✱ · `్య` 4.6e-4✱ · `␣జ` 0.95 · `ే` 0.96 · `⏎` 2.7e-4✱ forced |
| 3 | `␣జ` 0.90 · `కుల` 3.8e-5✱ · `్య` 4.1e-5✱ · `ము` 0.80 · `ద్ర` 0.95 · `మ` 0.90 · `మ` 1.1e-3✱ · `్య` 7.6e-3✱ · `డు` 0.25 · `న` 0.02✱ · `్య` 1.4e-5✱ · `␣హ` 0.25✱ · `్య` 1.9e-3✱ · `్య` 2.0e-4✱ · `్` 7.8e-7✱ · `జ` 4.6e-3✱ · `గ` 0.86 · `్య` 4.4e-4✱ · `మ` 0.17 · `ాని` 0.02✱ · `␣ల` 0.98 · `ంక` 0.89 · `లో` 1.1e-3 · `⏎` 2.1e-5✱ forced |
| 4 | `ర` 2.2e-3✱ · `ృ` 3.0e-5✱ · `␣` 0.01✱ · `కు` 2.1e-5✱ · `ట్లు` 5.8e-4✱ · `ను` 2.3e-4✱ · `ర` 1.8e-4✱ · `్య` 3.2e-4✱ · `డు` 0.07✱ · `న` 5.4e-3✱ · `్య` 1.5e-3✱ · `డు` 0.84 · `న్` 3.5e-4✱ · `ర` 9.8e-3✱ · `ర` 4.6e-3✱ · `ే` 1.0e-3✱ · `ర` 0.03✱ · `మ` 0.60 · `య` 0.15✱ · `్య` 9.8e-4✱ · `ము` 0.22 · `మ` 1.0e-3✱ · `్య` 0.01✱ · `␣సా` 0.01 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 106 tokens · 25.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమల్రియుల్వెనిక్రిముడ్ర య్ర్య్గా లకన్ జ లక్రియో | `IUIUIUIUIUIUIUIU` |
| 2 | మమత్రియుమ్ర జక్రిమున్న్న్క ల్య్య్మల్రియుమ్రిమల్రియుల్ | `IUIUIUIUIUIUIUIU` |
| 3 | క్రిముడ్య లల్య్యమల్రి ల్రిమ్రికెక్ముడడ్యతన్ లకన్ | `IUIUIUIUIUIUIUIU` |
| 4 | ల మయ్య లుల్ల లేదు డువ్రి న్నందు పంచచామరం | `IUIUIUIUIUIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 16% · repeated lines 0 · mean token probability (geometric) 0.024 · model's first choice kept 37% · constraint overrode 52% · backtracks 0

<details><summary>Token probabilities (106 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.01✱ · `మ` 0.16 · `ల` 0.64 · `్రి` 1.1e-4✱ · `యు` 0.02 · `ల` 0.20✱ · `్వ` 2.0e-4✱ · `ె` 0.03 · `ని` 0.03 · `క` 0.04✱ · `్రి` 1.3e-3✱ · `ము` 0.05 · `డ` 0.06 · `్ర` 4.0e-4✱ · `␣య` 0.01 · `్ర` 2.4e-4✱ · `్య` 3.9e-4✱ · `్` 4.3e-7✱ · `గా` 0.01✱ · `␣ల` 0.25 · `క` 0.14 · `న్` 0.31 · `␣జ` 0.02 · `␣ల` 0.01✱ · `క` 0.13 · `్రియ` 1.1e-4✱ · `ో` 5.3e-3✱ · `⏎` 0.50 |
| 2 | `మ` 0.20 · `మ` 0.40 · `త` 0.47 · `్రి` 7.2e-5✱ · `యు` 0.17 · `మ` 0.05 · `్ర` 1.9e-3✱ · `␣జ` 0.06 · `క` 0.04✱ · `్రి` 0.02✱ · `ము` 0.22 · `న్` 0.14 · `న్` 0.09 · `న్` 0.07✱ · `క` 0.31 · `␣ల` 0.28✱ · `్య` 5.7e-4✱ · `్య` 2.8e-3✱ · `్` 1.2e-4✱ · `మ` 0.03✱ · `ల` 0.04✱ · `్రి` 5.6e-4✱ · `యు` 0.13✱ · `మ` 0.11✱ · `్రి` 8.3e-3✱ · `మ` 0.16 · `ల` 0.02✱ · `్రి` 2.1e-3✱ · `యు` 0.28 · `ల్` 0.01 · `⏎` 0.09✱ forced |
| 3 | `క` 0.78 · `్రి` 0.53 · `ము` 0.61 · `డ` 0.47 · `్య` 1.4e-3✱ · `␣ల` 0.23 · `ల` 0.06✱ · `్య` 0.02✱ · `్య` 0.49 · `మ` 0.53 · `ల` 0.48 · `్రి` 0.23✱ · `␣ల` 0.30 · `్రి` 0.37 · `మ` 8.9e-3✱ · `్రి` 0.04✱ · `క` 0.94 · `ెక్` 1.9e-4✱ · `ము` 0.96 · `డ` 0.86 · `డ` 1.6e-4✱ · `్య` 9.4e-6✱ · `త` 0.88 · `న్` 0.75 · `␣ల` 0.79 · `క` 0.82 · `న్` 0.85 · `⏎` 2.7e-3✱ forced |
| 4 | `␣ల` 0.70 · `␣మ` 1.3e-3✱ · `య` 0.96 · `్య` 9.1e-5✱ · `␣` 0.69 · `లు` 4.1e-4✱ · `ల్ల` 3.1e-4✱ · `␣లేదు` 3.8e-4✱ · `␣` 1.7e-4✱ · `డు` 1.0e-3✱ · `వ` 1.3e-3✱ · `్రి` 1.0e-3✱ · `␣` 5.1e-3✱ · `న్న` 2.0e-3✱ · `ందు` 3.8e-3✱ · `␣పంచ` 0.23✱ · `చ` 0.88 · `ామ` 0.85 · `రం` 0.04 |

</details>

[↑ meters](#meters)

---

<a id="vasamtatilakamu"></a>

## 11. వసంతతిలకము (vasamtatilakamu)

```text
Meter: వసంతతిలకము (vasamtatilakamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 5 gaṇas: త భ జ జ గా, i.e. UUI UII IUI IUI UU (14 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 8th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T2; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter వసంతతిలకము (vasamtatilakamu).

Meter: వసంతతిలకము (vasamtatilakamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 5 gaṇas: త భ జ జ గా, i.e. UUI UII IUI IUI UU (14 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 8th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 98 tokens · 19.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాముత్రి దాల్స లము ధ్వ్వ్మత్వ మపన్రు నిల్యా | `UUIUIIIUIIUIUU` |
| 2 | మామత్రి దాల్స లము జ్వ్వ్మల్యమునున్రతట్రా | `UUIUIIIUIIUIUU` |
| 3 | త్రా మాల్స లధ్వ్వ్వమమ మ్య్య్రన్రడనున్మమాత్రిమ్ | `UUIUIIIUIIUIUU` |
| 4 | ల్యా మాయ మ్మల్యమును వ్ర్ర్యల్రమముండిమాక్షమ్ | `UUIUIIIUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.021 · model's first choice kept 35% · constraint overrode 48% · backtracks 0

<details><summary>Token probabilities (98 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.03 · `ము` 0.06 · `త` 0.06✱ · `్రి` 7.3e-4✱ · `␣ద` 0.02 · `ాల్` 5.0e-3 · `స` 0.03 · `␣ల` 0.02 · `ము` 0.06 · `␣ధ` 0.01✱ · `్వ` 0.01✱ · `్వ` 6.4e-3✱ · `్` 1.6e-6✱ · `మ` 9.9e-3✱ · `త్వ` 1.3e-3 · `␣మ` 0.08 · `ప` 5.0e-3 · `న` 0.02✱ · `్రు` 6.0e-5✱ · `␣ని` 9.9e-3✱ · `ల` 0.06 · `్యా` 2.1e-3✱ · `⏎` 0.50 |
| 2 | `మా` 0.20 · `మ` 0.18 · `త` 0.22 · `్రి` 0.82 · `␣ద` 0.50 · `ాల్` 0.25 · `స` 0.47 · `␣ల` 0.40 · `ము` 0.59 · `␣జ` 0.10 · `్వ` 0.19 · `్వ` 3.7e-3✱ · `్` 2.8e-3✱ · `మ` 0.01✱ · `ల` 0.08 · `్య` 5.0e-4✱ · `ము` 0.04 · `ను` 0.02 · `న` 0.39 · `్ర` 1.3e-4✱ · `త` 1.2e-3✱ · `ట` 9.5e-4✱ · `్రా` 9.6e-5✱ · `⏎` 0.04 forced |
| 3 | `త` 0.62 · `్రా` 0.03✱ · `␣మ` 0.02✱ · `ాల్` 0.51 · `స` 0.44 · `␣ల` 0.68 · `ధ` 3.8e-4✱ · `్వ` 6.7e-3✱ · `్వ` 0.55 · `్వ` 0.30✱ · `మ` 0.15✱ · `మ` 0.83 · `␣మ` 0.03✱ · `్య` 5.1e-4✱ · `్య` 3.2e-4✱ · `్ర` 1.8e-3✱ · `న` 0.07✱ · `్ర` 3.2e-4✱ · `డ` 0.92 · `ను` 0.04✱ · `న్` 5.5e-3✱ · `మ` 0.05✱ · `మా` 0.12✱ · `త` 0.52 · `్రి` 0.40 · `మ` 0.18✱ · `్` 2.1e-4✱ · `⏎` 0.17✱ forced |
| 4 | `ల` 0.71 · `్యా` 1.2e-3✱ · `␣మ` 0.03✱ · `ాయ` 0.06 · `␣మ` 0.20 · `్` 0.36 · `మ` 0.71 · `ల` 0.84 · `్య` 0.96 · `ము` 0.95 · `ను` 0.75 · `␣వ` 0.94 · `్ర` 3.9e-6✱ · `్ర` 1.7e-3✱ · `్య` 2.1e-5✱ · `ల` 0.89 · `్రమ` 6.1e-6✱ · `ము` 0.84 · `ండి` 3.4e-6✱ · `మా` 6.5e-4✱ · `క్ష` 1.00 · `మ` 0.91 · `్` 1.2e-6✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 88 tokens · 19.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కత్రా నరై నలర ల్ర్య్కల్రయుసల్రి లంకన్ | `UUIUIIIUIIUIUU` |
| 2 | సత్రా మతర్వరల జల్వరలల్రుసల్రిడ్ | `UUIUIIIUIIUIUU` |
| 3 | జత్రా మతర్వరల జల్రియనల్యసల్రిట్ | `UUIUIIIUIIUIUU` |
| 4 | మత్రా మతర్వరల జ్ర్య్మన్ర్యసలయ్రడన్ క్కడ్ | `UUIUIIIUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.024 · model's first choice kept 47% · constraint overrode 42% · backtracks 0

<details><summary>Token probabilities (88 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.01 · `త` 0.27 · `్రా` 0.01✱ · `␣న` 8.1e-3 · `ర` 0.18 · `ై` 0.04 · `␣న` 0.02 · `ల` 0.03 · `ర` 0.03 · `␣ల` 0.04✱ · `్ర` 3.0e-4✱ · `్య` 1.5e-3✱ · `్` 1.0e-6✱ · `క` 0.03✱ · `ల` 0.03✱ · `్ర` 4.9e-4✱ · `యు` 9.8e-3 · `స` 9.9e-3 · `ల` 0.02✱ · `్రి` 2.9e-4✱ · `␣ల` 0.08✱ · `ంక` 0.39 · `న్` 0.09✱ · `⏎` 0.87 |
| 2 | `స` 0.14 · `త` 0.82 · `్రా` 0.01✱ · `␣మ` 0.24 · `త` 0.09 · `ర` 0.13 · `్వర` 7.6e-5✱ · `ల` 0.23 · `␣జ` 0.07 · `ల` 0.05 · `్వర` 7.8e-5✱ · `ల` 0.15 · `ల` 0.01✱ · `్రు` 9.1e-4✱ · `స` 0.42 · `ల` 0.17✱ · `్రి` 0.04✱ · `డ` 0.03✱ · `్` 1.7e-7✱ · `⏎` 0.99 |
| 3 | `జ` 0.99 · `త` 0.99 · `్రా` 0.86 · `␣మ` 0.79 · `త` 0.80 · `ర` 0.96 · `్వర` 1.1e-3✱ · `ల` 0.98 · `␣జ` 0.98 · `ల` 0.99 · `్రియ` 3.4e-5✱ · `న` 0.95 · `ల` 0.93 · `్య` 9.5e-3✱ · `స` 0.73 · `ల` 0.78 · `్రి` 0.71 · `ట` 0.06✱ · `్` 9.3e-8✱ · `⏎` 0.02✱ forced |
| 4 | `మ` 0.46 · `త` 0.82 · `్రా` 0.39 · `␣మ` 0.81 · `త` 0.64 · `ర` 0.70 · `్వర` 0.08✱ · `ల` 1.00 · `␣జ` 0.96 · `్ర` 6.4e-7✱ · `్య` 3.2e-3✱ · `్` 3.7e-7✱ · `మన` 1.6e-4✱ · `్ర` 1.5e-4✱ · `్య` 0.96 · `స` 0.98 · `ల` 0.98 · `య` 4.6e-3✱ · `్ర` 5.8e-5✱ · `డ` 1.00 · `న్` 0.98 · `␣` 0.99 · `క్కడ` 4.1e-5✱ · `్` 1.3e-7✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 94 tokens · 46.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శత్రాఘ్రమున్ ధధురశౌర్యము వన్ధచున్ లంక్ | `UUIUIIIUIIUIUU` |
| 2 | చెత్రాముతివ్వరజజే నతి ముజ్యమున్ జీత్ | `UUIUIIIUIIUIUU` |
| 3 | కోత్రన్నమగ్యయతి జ్య్య్కోయతితిర్ర్లయన్డెన్ | `UUIUIIIUIIUIUU` |
| 4 | నత్రియ్యతిన్ జయతి జ్యయ్యడ శత్రుజాలెన్ | `UUIUIIIUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 14% · repeated lines 0 · mean token probability (geometric) 0.046 · model's first choice kept 59% · constraint overrode 36% · backtracks 30

<details><summary>Token probabilities (94 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.93 · `త` 0.47 · `్రా` 0.49 · `ఘ` 0.94 · `్ర` 0.49 · `ము` 0.89 · `న్` 0.89 · `␣ధ` 0.85 · `ధు` 0.03 · `ర` 0.89 · `శ` 0.91 · `ౌ` 0.99 · `ర్య` 0.99 · `ము` 0.94 · `␣వ` 0.02✱ · `న్` 0.82 · `ధ` 1.2e-3 · `చు` 0.84 · `న్` 0.64 · `␣ల` 1.00 · `ంక` 0.99 · `్` 1.2e-9✱ · `⏎` 6.3e-6✱ forced |
| 2 | `చె` 0.87 · `త` 4.9e-5✱ · `్రా` 1.1e-3✱ · `ము` 0.17✱ · `తి` 0.48 · `వ` 4.2e-4✱ · `్వర` 7.1e-5✱ · `జ` 0.03 · `జ` 0.35 · `ే` 0.49 · `␣న` 8.5e-3 · `తి` 0.75 · `␣ము` 3.1e-3 · `జ` 0.06✱ · `్య` 0.97 · `ము` 0.96 · `న్` 0.89 · `␣జ` 0.99 · `ీ` 0.99 · `త` 0.90 · `్` 1.8e-8✱ · `⏎` 1.1e-5✱ forced |
| 3 | `కో` 0.66 · `త` 2.9e-5✱ · `్ర` 2.4e-5✱ · `న్` 0.04✱ · `న` 3.5e-3✱ · `మ` 0.98 · `గ` 0.01✱ · `్య` 5.0e-4✱ · `య` 0.98 · `తి` 0.97 · `␣జ` 1.5e-3✱ · `్య` 2.8e-4✱ · `్య` 3.0e-3✱ · `్` 1.8e-6✱ · `క` 3.0e-6✱ · `ో` 1.6e-4✱ · `య` 1.00 · `తి` 0.98 · `తి` 3.7e-3✱ · `ర్` 2.0e-4✱ · `ర్` 0.72 · `ల` 0.92 · `య` 0.96 · `న్` 5.4e-3✱ · `డ` 0.99 · `ె` 0.99 · `న్` 0.02✱ · `⏎` 0.99 |
| 4 | `న` 0.98 · `త` 3.4e-4✱ · `్రియ` 9.3e-5✱ · `్య` 1.5e-3✱ · `తి` 0.98 · `న్` 0.93 · `␣జ` 0.96 · `య` 0.96 · `తి` 0.83 · `␣జ` 2.7e-3✱ · `్య` 0.08✱ · `య` 0.89 · `్య` 3.4e-4✱ · `డ` 1.8e-4✱ · `␣శ` 1.00 · `త్ర` 1.00 · `ు` 1.00 · `జ` 0.98 · `ాల` 1.00 · `ె` 0.99 · `న్` 0.98 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 95 tokens · 59.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మయ్వర్ర కిణ్వమసి జ్వ్వ్మయ్యవలట్రనుమ్రహ్ | `UUIUIIIUIIUIUU` |
| 2 | ద్రుయ్వట్య లంకకుర మ్రోననుశించిమశ్రమ్ | `UUIUIIIUIIUIUU` |
| 3 | కాయ్వయ్రహమ్రు జతు జ్వ్వ్కత్యమనుచ్రెనుక్నగ్ | `UUIUIIIUIIUIUU` |
| 4 | చూయ్వమ్యచూడెను మజో డును లే డుయయ్రవ్ | `UUIUIIIUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.005 · model's first choice kept 26% · constraint overrode 69% · backtracks 30

<details><summary>Token probabilities (95 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.95 · `య` 0.98 · `్వర` 9.6e-5✱ · `్ర` 3.9e-5✱ · `␣కి` 1.9e-3 · `ణ` 0.83 · `్వ` 0.27✱ · `మ` 0.83 · `సి` 0.72 · `␣జ` 0.95 · `్వ` 0.67 · `్వ` 0.08✱ · `్` 1.9e-5✱ · `మయ్య` 1.3e-5✱ · `వల` 1.7e-3 · `ట` 2.6e-3 · `్ర` 8.4e-5✱ · `ను` 2.4e-3✱ · `మ` 0.02✱ · `్రహ` 9.1e-6✱ · `్` 3.2e-6✱ · `⏎` 0.16✱ forced |
| 2 | `ద్ర` 0.66 · `ు` 2.1e-3✱ · `య` 8.6e-5✱ · `్వ` 1.1e-8✱ · `ట` 0.01✱ · `్య` 7.2e-4✱ · `␣ల` 0.13✱ · `ంక` 0.09✱ · `కు` 0.08✱ · `ర` 0.95 · `␣మ` 0.25 · `్రో` 0.01✱ · `న` 0.11 · `ను` 0.03✱ · `శ` 0.72 · `ించి` 0.98 · `మ` 2.4e-5✱ · `శ` 0.80 · `్రమ` 1.4e-4✱ · `్` 2.2e-5✱ · `⏎` 0.25✱ forced |
| 3 | `క` 0.87 · `ాయ` 2.1e-4✱ · `్వ` 4.8e-7✱ · `య` 0.98 · `్రహ` 1.4e-4✱ · `మ` 9.1e-3✱ · `్రు` 4.7e-5✱ · `␣జ` 0.11✱ · `తు` 0.34 · `␣జ` 0.01✱ · `్వ` 1.8e-4✱ · `్వ` 2.1e-3✱ · `్` 7.5e-5✱ · `క` 9.2e-5✱ · `త` 7.5e-5✱ · `్య` 2.9e-4✱ · `మ` 0.01✱ · `ను` 0.95 · `చ` 2.5e-3✱ · `్ర` 1.7e-5✱ · `ె` 0.99 · `ను` 0.01✱ · `క` 7.1e-6✱ · `్` 2.8e-4✱ · `న` 7.5e-3✱ · `గ` 9.6e-3✱ · `్` 3.2e-5✱ · `⏎` 0.12✱ forced |
| 4 | `␣చూ` 0.17 · `య` 1.4e-3✱ · `్వ` 2.1e-4✱ · `మ` 0.34 · `్య` 2.9e-5✱ · `చ` 0.81 · `ూ` 0.85 · `డ` 1.00 · `ె` 0.96 · `ను` 0.97 · `␣మ` 3.2e-3✱ · `జ` 4.1e-4✱ · `ో` 4.5e-3✱ · `␣` 6.9e-4✱ · `డు` 9.4e-3✱ · `ను` 3.8e-4✱ · `␣లే` 0.12✱ · `␣` 9.5e-5✱ · `డు` 0.02✱ · `య` 1.9e-3✱ · `య` 9.9e-3✱ · `్ర` 3.2e-3✱ · `వ` 0.02✱ · `్` 2.1e-4✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 88 tokens · 21.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మయ్యామమత్రి మమ ల్ర్వ్మగ్రి లకైమునుమ్యా | `UUIUIIIUIIUIUU` |
| 2 | మ్యాయ్యాత మ్రిమ్య సము స్ర్ర్యామమయమ్యమత్యా | `UUIUIIIUIIUIUU` |
| 3 | మాయ్యవ్రి లక్యమును ల్య్య్మమ్రి మమజ్వనిన్నిన్ | `UUIUIIIUIIUIUU` |
| 4 | మాయ్యాన్ని చేరి దనుమండినుపైన పద్యం | `UUIUIIIUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.022 · model's first choice kept 39% · constraint overrode 55% · backtracks 0

<details><summary>Token probabilities (88 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.49 · `య` 0.02 · `్యా` 1.1e-4✱ · `మ` 0.25 · `మ` 0.07 · `త` 0.05 · `్రి` 1.1e-3✱ · `␣మ` 0.17 · `మ` 0.08 · `␣ల` 0.02✱ · `్ర` 4.6e-4✱ · `్వ` 8.3e-4✱ · `్` 2.1e-3✱ · `మ` 0.08✱ · `గ` 0.20 · `్రి` 9.5e-4✱ · `␣ల` 0.06 · `క` 0.04✱ · `ై` 0.03✱ · `ము` 0.07 · `ను` 4.0e-3✱ · `మ` 0.69 · `్యా` 5.7e-4✱ · `⏎` 5.1e-3 forced |
| 2 | `మ` 0.70 · `్యా` 0.04✱ · `య` 0.02✱ · `్యా` 0.02✱ · `త` 0.14 · `␣మ` 0.31 · `్రి` 0.32 · `మ` 0.10✱ · `్య` 1.1e-4✱ · `␣స` 0.23✱ · `ము` 0.35 · `␣స` 0.02✱ · `్ర` 1.1e-3✱ · `్ర` 3.6e-4✱ · `్యా` 3.1e-6✱ · `మ` 3.5e-3✱ · `మ` 0.80 · `య` 0.80 · `మ` 0.13✱ · `్య` 2.8e-3✱ · `మ` 0.82 · `త` 0.79 · `్యా` 6.4e-3 · `⏎` 0.03✱ forced |
| 3 | `మ` 0.94 · `ాయ` 2.9e-4✱ · `్య` 2.4e-5✱ · `వ` 0.82 · `్రి` 8.0e-6✱ · `␣ల` 0.94 · `క` 0.91 · `్య` 2.2e-5✱ · `ము` 0.97 · `ను` 0.92 · `␣ల` 3.5e-3✱ · `్య` 3.2e-4✱ · `్య` 4.5e-3✱ · `్` 4.2e-5✱ · `మ` 0.87 · `మ` 0.76 · `్రి` 1.9e-3✱ · `␣మ` 0.10✱ · `మ` 0.88 · `జ` 1.2e-3✱ · `్వ` 4.6e-3✱ · `ని` 0.46 · `న్ని` 4.9e-3✱ · `న్` 4.2e-4✱ · `⏎` 0.01✱ forced |
| 4 | `మ` 0.04✱ · `ాయ` 4.5e-3✱ · `్యాన్ని` 2.5e-4✱ · `␣చే` 0.98 · `రి` 0.97 · `␣ద` 0.65 · `ను` 2.9e-4✱ · `మ` 0.96 · `ండి` 0.02✱ · `ను` 0.01✱ · `ప` 0.26 · `ైన` 0.94 · `␣ప` 0.93 · `ద్య` 0.88 · `ం` 6.0e-4✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 94 tokens · 21.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాముత్యమమ్య సము ద్ర్ర్మమ్య ల లక్య యమ్రా | `UUIUIIIUIIUIUU` |
| 2 | మామత్యమమ్య సము ద్ర్ర్మమ్య ల లక్య యమ్రా | `UUIUIIIUIIUIUU` |
| 3 | సీముత్రియన్ జమము ల్య్య్సిత్వలముప్రరారా | `UUIUIIIUIIUIUU` |
| 4 | మీముమ్యమమ్య లస ల్య్య్మిత్యముముప్పపస్రా | `UUIUIIIUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.032 · model's first choice kept 39% · constraint overrode 51% · backtracks 0

<details><summary>Token probabilities (94 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.03 · `ము` 0.06 · `త` 0.06✱ · `్య` 5.2e-5✱ · `మ` 0.12 · `మ` 0.03 · `్య` 3.1e-3✱ · `␣స` 0.03 · `ము` 0.92 · `␣ద` 3.2e-3✱ · `్ర` 0.15✱ · `్ర` 0.01✱ · `్` 3.1e-7✱ · `మ` 0.04✱ · `మ` 0.05✱ · `్య` 2.4e-3✱ · `␣ల` 0.19 · `␣ల` 0.10 · `క` 0.38 · `్య` 1.2e-4✱ · `␣య` 9.5e-3✱ · `మ` 0.11✱ · `్రా` 1.3e-3✱ · `⏎` 0.09✱ forced |
| 2 | `మా` 0.39 · `మ` 4.8e-3✱ · `త` 0.25 · `్య` 0.32✱ · `మ` 0.84 · `మ` 0.68 · `్య` 0.93 · `␣స` 0.22 · `ము` 0.66 · `␣ద` 0.17 · `్ర` 0.36✱ · `్ర` 5.7e-3✱ · `్` 0.35 · `మ` 0.91 · `మ` 0.90 · `్య` 0.74 · `␣ల` 0.60 · `␣ల` 0.01✱ · `క` 0.89 · `్య` 0.86 · `␣య` 0.69 · `మ` 0.91 · `్రా` 0.58 · `⏎` 0.90 |
| 3 | `సీ` 0.24 · `ము` 0.21 · `త` 0.30 · `్రియ` 7.1e-4✱ · `న్` 0.05✱ · `␣జ` 0.23 · `మ` 0.03 · `ము` 0.07 · `␣ల` 0.09 · `్య` 7.3e-4✱ · `్య` 0.01✱ · `్` 1.8e-6✱ · `స` 3.7e-3✱ · `ిత` 3.1e-3✱ · `్వ` 2.2e-3✱ · `ల` 0.95 · `ము` 0.95 · `ప్ర` 9.0e-6✱ · `రా` 0.33✱ · `రా` 5.1e-3 · `⏎` 9.5e-5 forced |
| 4 | `మ` 0.01✱ · `ీ` 7.6e-4✱ · `ము` 9.9e-3✱ · `మ` 0.17✱ · `్య` 0.06✱ · `మ` 0.05 · `మ` 0.34 · `్య` 0.33 · `␣ల` 0.14 · `స` 0.04 · `␣ల` 0.13 · `్య` 0.06✱ · `్య` 0.02✱ · `్` 1.8e-4✱ · `మ` 3.5e-3✱ · `ిత` 1.4e-3✱ · `్య` 0.04✱ · `ము` 0.54 · `ము` 0.06✱ · `ప` 4.9e-3✱ · `్` 1.8e-6✱ · `ప` 0.12✱ · `ప` 0.10✱ · `స` 0.01✱ · `్రా` 5.4e-4✱ |

</details>

[↑ meters](#meters)

---

<a id="indravajra"></a>

## 12. ఇంద్రవజ్ర (indravajra)

```text
Meter: ఇంద్రవజ్ర (indravajra), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: త త జ గా, i.e. UUI UUI IUI UU (11 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 8th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter ఇంద్రవజ్ర (indravajra).

Meter: ఇంద్రవజ్ర (indravajra), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: త త జ గా, i.e. UUI UUI IUI UU (11 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 8th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 84 tokens · 23.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పళ్లమ్రమించే కల మ్ర్వల్రిపైతట్ | `UUIUUIIUIUU` |
| 2 | కళ్లన్రవల్యం మ మృ మ్ర్ర్కట్ర్నమక్యం | `UUIUUIIUIUU` |
| 3 | లౌ ళ్లల్రిపైతట్ మత మ్ర్ర్లమ్ర్వలత్రిప్ | `UUIUUIIUIUU` |
| 4 | హే ళ్లైన పైనద్య పదృష్ అశర్రమ్ | `UUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 25% · repeated lines 0 · mean token probability (geometric) 0.006 · model's first choice kept 27% · constraint overrode 62% · backtracks 0

<details><summary>Token probabilities (84 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.03 · `ళ్ల` 1.3e-3 · `మ` 0.05 · `్ర` 3.6e-4✱ · `మ` 0.10 · `ించే` 2.5e-3✱ · `␣క` 0.04 · `ల` 0.09 · `␣మ` 0.02✱ · `్ర` 7.5e-4✱ · `్వ` 6.6e-6✱ · `ల` 0.30 · `్రి` 1.3e-5✱ · `పై` 2.7e-3 · `త` 0.03✱ · `ట` 5.2e-3✱ · `్` 5.5e-7✱ · `⏎` 0.20 forced |
| 2 | `క` 0.34 · `ళ్ల` 0.04✱ · `న` 0.01✱ · `్ర` 8.6e-5✱ · `వ` 0.19 · `ల` 0.13 · `్యం` 1.8e-4✱ · `␣మ` 0.74 · `␣మ` 0.47 · `ృ` 0.08✱ · `␣మ` 0.01✱ · `్ర` 2.7e-5✱ · `్ర` 4.4e-3✱ · `్` 6.2e-5✱ · `క` 3.6e-3✱ · `ట` 0.58 · `్ర` 6.6e-4✱ · `్` 0.06✱ · `న` 5.3e-3✱ · `మ` 0.16 · `క` 0.01 · `్యం` 8.1e-4✱ · `⏎` 5.9e-3✱ forced |
| 3 | `ల` 0.46 · `ౌ` 2.8e-4✱ · `␣` 3.6e-3✱ · `ళ్ల` 2.5e-4✱ · `ల` 0.62 · `్రి` 0.30 · `పై` 0.71 · `త` 0.84 · `ట` 0.85 · `్` 3.3e-4✱ · `␣మ` 5.1e-3✱ · `త` 0.84 · `␣మ` 2.1e-4✱ · `్ర` 4.6e-5✱ · `్ర` 2.9e-4✱ · `్` 5.1e-4✱ · `ల` 0.98 · `మ` 2.3e-3✱ · `్ర` 0.99 · `్వ` 0.80 · `ల` 0.98 · `త్రి` 9.3e-4✱ · `ప` 0.05✱ · `్` 6.1e-6✱ · `⏎` 5.8e-5✱ forced |
| 4 | `హ` 0.04✱ · `ే` 0.08✱ · `␣` 0.02✱ · `ళ` 2.1e-5✱ · `్` 2.0e-7✱ · `ల` 5.4e-3✱ · `ైన` 3.6e-3✱ · `␣ప` 0.98 · `ైన` 0.96 · `ద్య` 3.1e-4✱ · `␣పద` 7.3e-4✱ · `ృష్` 4.9e-8✱ · `␣అ` 0.99 · `శ` 3.7e-5✱ · `ర` 0.99 · `్ర` 2.3e-5✱ · `మ` 3.5e-4✱ · `్` 2.3e-6✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 74 tokens · 18.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శక్రిమ్య పృథ్విచ్రి న సాగరమ్రంచ్ | `UUIUUIIUIUU` |
| 2 | నుక్రత్రివైనంత మనొక్రి లంకన్ | `UUIUUIIUIUU` |
| 3 | వెక్రిన్రశత్రా శశునెల్లు లణ్యత్ | `UUIUUIIUIUU` |
| 4 | ఏక్రిడ్రి సీతాడవి నిర్రచుట్రన్ | `UUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.011 · model's first choice kept 28% · constraint overrode 59% · backtracks 0

<details><summary>Token probabilities (74 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.25 · `క` 0.03 · `్రి` 0.02✱ · `మ` 0.06✱ · `్య` 3.5e-3✱ · `␣ప` 7.8e-3 · `ృ` 5.4e-3 · `థ` 0.92 · `్` 0.10✱ · `వి` 0.98 · `చ` 8.9e-3✱ · `్రి` 1.6e-3✱ · `␣న` 0.02 · `␣సా` 6.7e-3 · `గర` 0.41 · `మ` 0.07✱ · `్ర` 3.0e-3✱ · `ంచ` 0.04 · `్` 4.2e-8✱ · `⏎` 7.6e-5✱ forced |
| 2 | `ను` 0.89 · `క` 6.0e-4✱ · `్ర` 2.5e-4✱ · `త` 0.93 · `్రి` 5.0e-4✱ · `వ` 0.06 · `ైన` 0.04✱ · `ంత` 1.2e-4✱ · `␣మ` 0.06 · `న` 0.01 · `ొ` 8.0e-4✱ · `క` 0.48 · `్రి` 2.7e-3✱ · `␣ల` 0.93 · `ంక` 0.79 · `న్` 0.01✱ · `⏎` 7.3e-4✱ forced |
| 3 | `␣వె` 0.45 · `క` 9.3e-4✱ · `్రి` 4.0e-3✱ · `న` 5.5e-3✱ · `్ర` 2.7e-5✱ · `శ` 0.88 · `త` 0.84 · `్రా` 0.40 · `␣శ` 0.04✱ · `శ` 0.31 · `ు` 1.8e-4✱ · `న` 3.9e-3✱ · `ె` 7.1e-5✱ · `ల్ల` 1.4e-3✱ · `ు` 0.62 · `␣ల` 0.49 · `ణ` 9.7e-3 · `్య` 2.4e-3✱ · `త` 4.4e-3✱ · `్` 3.6e-7✱ · `⏎` 3.6e-6✱ forced |
| 4 | `ఏ` 0.01✱ · `క` 3.7e-3✱ · `్రి` 1.1e-3✱ · `డ` 0.18✱ · `్రి` 4.2e-4✱ · `␣సీ` 0.90 · `తా` 0.81 · `డ` 6.2e-4✱ · `వి` 1.00 · `␣ని` 1.8e-3✱ · `ర` 4.9e-3✱ · `్ర` 6.6e-9✱ · `చు` 0.08✱ · `ట` 0.99 · `్ర` 6.1e-4✱ · `న్` 0.15✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 78 tokens · 40.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిభ్రమర్లాపర మ్ర్ల్దన్యముద్యువ్ | `UUIUUIIUIUU` |
| 2 | తల్లోని మౌడశ్రయ మ్ర్ర్ధమ్యముందే | `UUIUUIIUIUU` |
| 3 | లోల్లాందు ఏదీ జగ మ్య్వ్లొందులోమమ్ | `UUIUUIIUIUU` |
| 4 | ముల్లద్రియోక్షమ్యవవుక్రి ఇంద్రవ్ | `UUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.004 · model's first choice kept 40% · constraint overrode 54% · backtracks 30

<details><summary>Token probabilities (78 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.84 · `ల్లి` 0.92 · `భ` 3.2e-5 · `్ర` 0.29 · `మ` 0.86 · `ర` 2.1e-3 · `్లా` 1.0e-6✱ · `ప` 0.25 · `ర` 0.02 · `␣మ` 0.97 · `్ర` 1.8e-5✱ · `్` 4.7e-6✱ · `ల` 0.94 · `్` 9.8e-10✱ · `దన` 2.7e-4✱ · `్య` 1.1e-4✱ · `ము` 0.96 · `ద్య` 0.83 · `ు` 0.91 · `వ` 0.69 · `్` 7.6e-7✱ · `⏎` 0.21 forced |
| 2 | `త` 0.09 · `ల` 0.33 · `్` 1.3e-7✱ · `లోని` 8.7e-4✱ · `␣మ` 0.33 · `ౌ` 0.74 · `డ` 0.27 · `శ` 0.15✱ · `్ర` 0.04✱ · `య` 0.98 · `␣మ` 0.03✱ · `్ర` 2.5e-4✱ · `్ర` 3.1e-6✱ · `్` 1.5e-7✱ · `ధ` 6.5e-3✱ · `మ` 0.13✱ · `్య` 6.3e-5✱ · `ము` 2.7e-3✱ · `ందే` 5.3e-4✱ · `⏎` 0.52 |
| 3 | `లో` 0.90 · `ల` 6.8e-4✱ · `్లా` 5.3e-10✱ · `ందు` 1.00 · `␣ఏ` 1.00 · `దీ` 0.88 · `␣జగ` 5.6e-3✱ · `␣మ` 0.30 · `్య` 9.0e-6✱ · `్వ` 3.0e-5✱ · `్` 1.0e-5✱ · `ల` 0.18✱ · `ొ` 1.3e-3✱ · `ందు` 0.13 · `లో` 6.9e-4✱ · `మ` 0.59 · `మ` 0.01✱ · `్` 7.1e-8✱ · `⏎` 0.05✱ forced |
| 4 | `ము` 0.84 · `ల్ల` 1.7e-5✱ · `ద` 0.03✱ · `్రియ` 5.2e-4✱ · `ో` 7.5e-3✱ · `క్ష` 0.93 · `మ` 0.97 · `్య` 2.4e-8✱ · `వ` 5.2e-4✱ · `వ` 9.5e-3✱ · `ు` 1.5e-4✱ · `క` 0.95 · `్రి` 5.5e-4✱ · `␣ఇ` 0.84 · `ంద్ర` 0.77 · `వ` 0.79 · `్` 5.6e-8✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 71 tokens · 38.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాముమ్యు నిల్యా జర స్య్రవ్రియర్చుయ్ | `UUIUUIIUIUU` |
| 2 | రామిత్య లంకండ జెరగ్రురాడుద్ | `UUIUUIIUIUU` |
| 3 | దేమన్రియల్రియ్య మ న్య్ర్దేవ శత్రుల్ | `UUIUUIIUIUU` |
| 4 | శ్రూమడ్యమువ్వర్రియచుయ్లులేదియ్ | `UUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.008 · model's first choice kept 45% · constraint overrode 52% · backtracks 30

<details><summary>Token probabilities (71 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.99 · `ము` 0.94 · `మ` 0.01 · `్య` 0.98 · `ు` 0.57 · `␣ని` 0.98 · `ల` 0.98 · `్యా` 0.71 · `␣జ` 0.90 · `ర` 0.97 · `␣స` 0.92 · `్య` 5.4e-7✱ · `్ర` 3.4e-3✱ · `వ` 0.83 · `్రియ` 3.3e-5✱ · `ర్చు` 5.0e-7✱ · `య` 2.1e-4✱ · `్` 2.5e-8✱ · `⏎` 0.59 |
| 2 | `రా` 1.00 · `మ` 0.83 · `ిత` 0.98 · `్య` 0.95 · `␣ల` 0.98 · `ం` 0.95 · `క` 0.97 · `ండ` 0.91 · `␣జ` 0.48 · `ె` 0.99 · `రగ` 0.97 · `్రు` 6.0e-5✱ · `రా` 0.49 · `డు` 1.00 · `ద్` 2.6e-7✱ · `⏎` 0.06✱ forced |
| 3 | `దే` 0.74 · `మన` 0.01✱ · `్రియ` 5.5e-4✱ · `ల` 2.5e-5✱ · `్రియ` 6.1e-5✱ · `్య` 1.8e-5✱ · `␣మ` 4.8e-3✱ · `␣న` 1.6e-4✱ · `్య` 1.1e-6✱ · `్ర` 2.2e-6✱ · `్` 9.0e-7✱ · `దే` 0.95 · `వ` 0.98 · `␣శ` 0.99 · `త్ర` 1.00 · `ు` 1.00 · `ల్` 4.0e-6✱ · `⏎` 1.8e-3✱ forced |
| 4 | `శ` 0.14 · `్ర` 8.9e-5✱ · `ూ` 2.8e-4✱ · `మ` 0.05✱ · `డ` 4.4e-3✱ · `్య` 6.9e-6✱ · `ము` 1.2e-4✱ · `వ` 1.6e-3✱ · `్వర` 2.1e-4✱ · `్రియ` 1.1e-4✱ · `చు` 0.07✱ · `య` 0.97 · `్` 0.03✱ · `లు` 3.1e-5✱ · `లే` 1.1e-4✱ · `ది` 3.2e-4✱ · `య` 9.2e-4✱ · `్` 1.9e-3✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 77 tokens · 23.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కల్లిక్రియే జగ్రమ మ్ర్జ్గమ్యకత్యా | `UUIUUIIUIUU` |
| 2 | మల్లిమ్రదమ్యం మమ క్వ్య్మత్యముక్యం | `UUIUUIIUIUU` |
| 3 | కల్లిక్రియేతిమ్య మ త్ర్ర్కమ్రిధిన్లే | `UUIUUIIUIUU` |
| 4 | కల్లిక్రియేయత్యము మ్ర్ర్గర్యమున్రో | `UUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 9% · repeated lines 0 · mean token probability (geometric) 0.008 · model's first choice kept 19% · constraint overrode 71% · backtracks 0

<details><summary>Token probabilities (77 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.10 · `ల్లి` 0.05 · `క` 0.03✱ · `్రియ` 3.1e-4✱ · `ే` 0.01✱ · `␣జగ` 0.06 · `్రమ` 4.0e-5✱ · `␣మ` 0.02✱ · `్ర` 3.3e-3✱ · `్` 4.4e-5✱ · `జ` 0.10 · `్` 2.2e-5✱ · `గ` 3.9e-3✱ · `మ` 0.19✱ · `్య` 1.6e-3✱ · `క` 0.36 · `త` 0.01✱ · `్యా` 5.4e-3✱ · `⏎` 0.65 |
| 2 | `మ` 0.17 · `ల్లి` 0.43 · `మ` 0.10 · `్ర` 1.0e-3✱ · `ద` 0.30 · `మ` 0.12✱ · `్యం` 1.9e-4✱ · `␣మ` 0.21✱ · `మ` 0.05 · `␣క` 0.02✱ · `్వ` 3.7e-5✱ · `్య` 2.5e-4✱ · `్` 8.3e-10✱ · `మ` 0.14✱ · `త` 0.18✱ · `్య` 9.6e-4✱ · `ము` 0.25✱ · `క` 4.2e-3✱ · `్యం` 5.6e-7✱ · `⏎` 0.21✱ |
| 3 | `క` 0.12 · `ల్లి` 0.09✱ · `క` 0.04✱ · `్రియ` 5.8e-3✱ · `ే` 0.15 · `తి` 0.87 · `మ` 0.03✱ · `్య` 8.6e-4✱ · `␣మ` 0.03✱ · `␣త` 0.01✱ · `్ర` 1.4e-4✱ · `్ర` 3.7e-4✱ · `్` 7.9e-7✱ · `క` 0.64 · `మ` 0.04✱ · `్రి` 3.8e-6✱ · `ధి` 0.71 · `న్` 7.4e-4✱ · `లే` 3.2e-5✱ · `⏎` 6.9e-3✱ forced |
| 4 | `క` 8.6e-3✱ · `ల్లి` 0.16 · `క` 0.50 · `్రియ` 0.24 · `ే` 0.18✱ · `య` 0.02✱ · `త` 3.7e-3✱ · `్య` 5.5e-3✱ · `ము` 0.28 · `␣మ` 0.20 · `్ర` 1.9e-4✱ · `్ర` 6.0e-3✱ · `్` 8.2e-4✱ · `గర` 4.2e-3✱ · `్య` 4.4e-4✱ · `ము` 0.91 · `న` 0.01✱ · `్రో` 2.0e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 76 tokens · 18.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మ్మక్యా మమత్యా మక మమ్యముత్యా | `UUIUUIIUIUU` |
| 2 | తౌక్యా మమత్యా మమ మ్య్య్తక్రి లోకా | `UUIUUIIUIUU` |
| 3 | కక్యాల మమ్యుత్రి మ జ్య్య్గత్రియమ్యా | `UUIUUIIUIUU` |
| 4 | మ్యుక్యామమక్షమ్యగ ముర్య్యవజ్రా | `UUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 7% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.026 · model's first choice kept 41% · constraint overrode 53% · backtracks 0

<details><summary>Token probabilities (76 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ్మ` 0.03 · `క` 0.05 · `్యా` 4.7e-5✱ · `␣మ` 0.36 · `మ` 0.57 · `త` 0.85 · `్యా` 4.7e-4✱ · `␣మ` 0.43 · `క` 0.06 · `␣మ` 0.02✱ · `మ` 0.18 · `్య` 3.5e-4✱ · `ము` 0.14 · `త` 2.7e-3✱ · `్యా` 5.6e-3✱ · `⏎` 0.78 |
| 2 | `త` 0.95 · `ౌ` 4.2e-6✱ · `క` 0.84 · `్యా` 0.05✱ · `␣మ` 0.70 · `మ` 0.38 · `త` 0.40 · `్యా` 0.79 · `␣మ` 0.75 · `మ` 0.75 · `␣మ` 0.02✱ · `్య` 0.03✱ · `్య` 0.02✱ · `్` 4.0e-7✱ · `త` 0.01✱ · `క` 0.12✱ · `్రి` 5.3e-4✱ · `␣లో` 0.02✱ · `కా` 0.01✱ · `⏎` 0.51 |
| 3 | `క` 0.13 · `క` 0.12✱ · `్యా` 3.3e-4✱ · `ల` 2.6e-3✱ · `␣మ` 0.79 · `మ` 0.90 · `్య` 0.86 · `ు` 0.09✱ · `త` 0.96 · `్రి` 9.1e-4✱ · `␣మ` 0.12✱ · `␣జ` 4.1e-4✱ · `్య` 1.5e-4✱ · `్య` 4.6e-4✱ · `్` 1.3e-5✱ · `గ` 3.8e-3✱ · `త` 0.91 · `్రియ` 3.8e-5✱ · `మ` 0.42 · `్యా` 0.01✱ · `⏎` 0.05✱ forced |
| 4 | `మ` 0.94 · `్య` 0.95 · `ు` 0.19✱ · `క` 3.7e-4✱ · `్యా` 0.82 · `మ` 0.05 · `మ` 0.36 · `క్ష` 0.17 · `మ` 0.21✱ · `్య` 1.4e-4✱ · `గ` 0.84 · `␣మ` 7.2e-3✱ · `ు` 9.3e-4✱ · `ర` 0.01✱ · `్య` 1.5e-4✱ · `్య` 7.5e-3✱ · `వ` 0.95 · `జ` 0.98 · `్రా` 5.9e-3 |

</details>

[↑ meters](#meters)

---

<a id="upendravajra"></a>

## 13. ఉపేంద్రవజ్ర (upendravajra)

```text
Meter: ఉపేంద్రవజ్ర (upendravajra), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: జ త జ గా, i.e. IUI UUI IUI UU (11 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 8th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter ఉపేంద్రవజ్ర (upendravajra).

Meter: ఉపేంద్రవజ్ర (upendravajra), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: జ త జ గా, i.e. IUI UUI IUI UU (11 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 8th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 70 tokens · 19.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జగత్తు నిల్వర్వర మ్ర్య్శాకమల్యా | `IUIUUIIUIUU` |
| 2 | జగత్తు నృమ్రిక్రి మ మ్య్య్శాకమత్యా | `IUIUUIIUIUU` |
| 3 | ల్లగాతనుల్లండి చె మ్ర్య్లమ్యముమ్యం | `IUIUUIIUIUU` |
| 4 | మగత్రునాయక్రతి మమ్యజత్యా | `IUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.009 · model's first choice kept 24% · constraint overrode 69% · backtracks 0

<details><summary>Token probabilities (70 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.13 · `గ` 0.25 · `త్తు` 0.10✱ · `␣ని` 0.11✱ · `ల` 0.04✱ · `్వర` 6.0e-4✱ · `్వర` 5.4e-4✱ · `␣మ` 0.35 · `్ర` 2.0e-3✱ · `్య` 7.4e-6✱ · `్` 1.1e-6✱ · `శా` 3.0e-4✱ · `క` 0.01✱ · `మ` 0.11✱ · `ల` 0.02 · `్యా` 1.3e-3✱ · `⏎` 0.07✱ forced |
| 2 | `జ` 0.35 · `గ` 0.08✱ · `త్తు` 0.11 · `␣న` 0.02 · `ృ` 0.02 · `మ` 0.07 · `్రి` 2.6e-4✱ · `క` 0.09✱ · `్రి` 2.1e-4✱ · `␣మ` 0.20 · `␣మ` 0.11 · `్య` 1.3e-3✱ · `్య` 7.3e-3✱ · `్` 6.2e-6✱ · `శా` 7.5e-3✱ · `క` 0.67 · `మ` 0.52 · `త` 0.02✱ · `్యా` 9.4e-5✱ · `⏎` 0.08✱ forced |
| 3 | `ల్ల` 2.9e-3✱ · `గా` 7.9e-4✱ · `త` 2.1e-4✱ · `ను` 0.07✱ · `ల్ల` 4.4e-3✱ · `ండి` 4.3e-3✱ · `␣చె` 0.02✱ · `␣మ` 6.1e-3✱ · `్ర` 5.4e-3✱ · `్య` 2.9e-3✱ · `్` 1.5e-4✱ · `ల` 8.4e-4✱ · `మ` 0.49 · `్య` 3.1e-4✱ · `ము` 0.12 · `మ` 0.13 · `్యం` 1.7e-3✱ · `⏎` 0.73 |
| 4 | `మ` 0.83 · `గ` 8.4e-4✱ · `త` 5.5e-3✱ · `్రు` 2.3e-4✱ · `న` 0.78 · `ాయ` 7.0e-4✱ · `క` 0.01✱ · `్ర` 3.6e-5✱ · `తి` 0.86 · `␣మ` 0.92 · `మ` 1.8e-3✱ · `్య` 4.9e-5✱ · `జ` 0.53 · `త` 0.04✱ · `్యా` 0.04✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 85 tokens · 22.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మకర్రిసించిన్రు లమల్యముండక్ | `IUIUUIIUIUU` |
| 2 | మకల్యముగ్యున్ లము జ్వ్వ్మల్యముంచెన్ | `IUIUUIIUIUU` |
| 3 | మకత్రి గమ్యన్ సము గ్వ్వ్నమ్యనుజ్యం | `IUIUUIIUIUU` |
| 4 | మ్ర్రు కడ్వెనల్యవ్వ శరొత్యమువ్ వవ్ | `IUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 15% · single-akshara words 15% · repeated lines 0 · mean token probability (geometric) 0.006 · model's first choice kept 33% · constraint overrode 56% · backtracks 0

<details><summary>Token probabilities (85 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `␣మ` 9.0e-3 · `క` 0.04 · `ర` 0.02✱ · `్రి` 4.5e-5✱ · `స` 1.8e-3 · `ించిన` 4.8e-4✱ · `్రు` 3.1e-4✱ · `␣ల` 0.02 · `మ` 0.08 · `ల` 0.04✱ · `్య` 7.3e-4✱ · `ము` 0.17 · `ండ` 6.6e-3✱ · `క` 0.07 · `్` 7.5e-10✱ · `⏎` 0.19 forced |
| 2 | `మ` 0.44 · `క` 0.02✱ · `ల` 0.48 · `్య` 6.6e-4✱ · `ము` 0.35 · `గ` 0.11 · `్య` 5.5e-4✱ · `ు` 0.24 · `న్` 0.16 · `␣ల` 0.11 · `ము` 0.03 · `␣జ` 0.05✱ · `్వ` 0.02✱ · `్వ` 3.4e-3✱ · `్` 1.1e-4✱ · `మ` 0.02✱ · `ల` 0.13 · `్య` 4.2e-3✱ · `ము` 0.25 · `ంచ` 0.03 · `ె` 0.54 · `న్` 0.31 · `⏎` 0.96 |
| 3 | `మ` 0.92 · `క` 0.37 · `త` 0.06 · `్రి` 7.7e-4✱ · `␣గ` 0.02 · `మ` 0.06 · `్య` 0.03✱ · `న్` 0.58 · `␣స` 0.91 · `ము` 0.84 · `␣గ` 3.8e-4✱ · `్వ` 5.1e-3✱ · `్వ` 4.8e-5✱ · `్` 1.2e-3✱ · `న` 0.02✱ · `మ` 0.95 · `్య` 6.0e-6✱ · `ను` 2.6e-4✱ · `జ` 1.4e-4✱ · `్యం` 8.9e-5✱ · `⏎` 1.00 |
| 4 | `మ` 1.00 · `్ర` 4.1e-6✱ · `్ర` 0.77 · `ు` 0.29✱ · `␣` 3.3e-5✱ · `క` 1.5e-4✱ · `డ` 1.00 · `్వ` 6.8e-7✱ · `ె` 0.98 · `న` 1.4e-3✱ · `ల` 1.4e-3✱ · `్య` 1.6e-4✱ · `వ` 7.2e-5✱ · `్వ` 7.6e-5✱ · `␣శ` 0.97 · `ర` 5.7e-4✱ · `ొ` 4.6e-7✱ · `త్య` 3.1e-3✱ · `ము` 2.7e-3✱ · `వ` 6.1e-7✱ · `్` 7.9e-5✱ · `␣` 3.7e-4✱ · `వ` 4.2e-3✱ · `వ` 2.0e-3✱ · `్` 8.5e-7✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 68 tokens · 33.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శకర్రి నర్రహ్గుల శౌర కార్యక్ | `IUIUUIIUIUU` |
| 2 | మకశ్రిణిల్రిన్ మరుమల్య మాయన్ | `IUIUUIIUIUU` |
| 3 | నకర్రి లంకుక్రిచు నైకమున్ ప్రస్ | `IUIUUIIUIUU` |
| 4 | సకమ్రి జయ్రహ్రహ జల్లనుబ్లువ్ | `IUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 7% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.014 · model's first choice kept 57% · constraint overrode 35% · backtracks 30

<details><summary>Token probabilities (68 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.97 · `క` 0.66 · `ర` 0.86 · `్రి` 2.2e-4✱ · `␣న` 0.01 · `ర` 0.73 · `్రహ్` 3.1e-5✱ · `గు` 1.8e-3 · `ల` 1.00 · `␣శ` 1.00 · `ౌ` 1.00 · `ర` 0.99 · `␣కార్య` 2.4e-5 · `క` 0.98 · `్` 6.4e-8✱ · `⏎` 1.6e-3✱ forced |
| 2 | `మ` 1.00 · `క` 0.99 · `శ` 0.99 · `్రి` 1.00 · `ణి` 1.00 · `ల` 6.1e-5✱ · `్రి` 6.1e-6✱ · `న్` 0.98 · `␣మ` 0.98 · `రు` 0.94 · `మ` 0.97 · `ల` 0.97 · `్య` 3.4e-7✱ · `␣మ` 0.04 · `ాయ` 0.11 · `న్` 0.94 · `⏎` 0.98 |
| 3 | `న` 0.99 · `క` 0.97 · `ర` 0.99 · `్రి` 1.2e-5✱ · `␣ల` 1.00 · `ంక` 1.00 · `ు` 8.0e-5✱ · `క` 7.3e-6✱ · `్రి` 6.1e-8✱ · `చు` 0.98 · `␣న` 0.75 · `ై` 0.94 · `క` 0.88 · `ము` 0.95 · `న్` 0.81 · `␣ప్ర` 1.00 · `స` 0.99 · `్` 7.2e-8✱ · `⏎` 0.99 |
| 4 | `స` 0.98 · `క` 3.9e-4✱ · `మ` 9.4e-4✱ · `్రి` 1.6e-8✱ · `␣జ` 1.00 · `య` 1.00 · `్రహ` 1.2e-6✱ · `్రహ` 1.7e-6✱ · `␣జ` 2.0e-4✱ · `ల్ల` 2.4e-3✱ · `ను` 0.99 · `బ` 2.3e-6✱ · `్` 7.1e-5✱ · `లు` 1.6e-3✱ · `వ` 6.9e-3✱ · `్` 1.1e-4✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 76 tokens · 37.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సమద్ర్రి హూరావని హ్ర్ద్జమ్రి తంచెన్ | `IUIUUIIUIUU` |
| 2 | సమిత్య లంకన్గను జర్చెనున్మహ్ | `IUIUUIIUIUU` |
| 3 | మమఘ్రు గట్యం జెలు మగ్వరగ్వాన్ | `IUIUUIIUIUU` |
| 4 | జమంతుడెన్ జయ్వర మ్ర్ర్నన్రు వేగా | `IUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 7% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.050 · model's first choice kept 58% · constraint overrode 32% · backtracks 30

<details><summary>Token probabilities (76 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 0.65 · `మ` 0.76 · `ద్ర` 0.19 · `్రి` 0.97 · `␣హ` 0.66 · `ూ` 0.67 · `రా` 0.01 · `వ` 0.45 · `ని` 9.9e-3 · `␣హ` 9.7e-3 · `్ర` 0.92 · `్` 0.98 · `ద` 0.86 · `్` 1.9e-6✱ · `జ` 0.05✱ · `మ` 0.97 · `్రి` 0.97 · `␣త` 0.86 · `ంచ` 1.00 · `ె` 0.99 · `న్` 0.96 · `⏎` 1.00 |
| 2 | `స` 0.97 · `మ` 0.99 · `ిత` 0.99 · `్య` 0.99 · `␣ల` 0.95 · `ంక` 0.74 · `న్` 0.82 · `గ` 0.97 · `ను` 0.92 · `␣జ` 0.99 · `ర్చ` 0.33 · `ె` 0.99 · `ను` 0.95 · `న్` 3.8e-5✱ · `మ` 0.99 · `హ` 0.98 · `్` 7.0e-8✱ · `⏎` 0.02✱ forced |
| 3 | `మ` 0.93 · `మ` 0.05 · `ఘ` 0.03 · `్రు` 0.64 · `␣గ` 0.93 · `ట` 0.95 · `్యం` 7.2e-6✱ · `␣జ` 8.1e-5✱ · `ె` 0.99 · `లు` 0.98 · `␣మ` 0.96 · `గ` 7.0e-3 · `్వర` 1.3e-6✱ · `గ` 0.06✱ · `్వ` 0.94 · `ాన` 0.04 · `్` 1.7e-6✱ · `⏎` 0.04✱ forced |
| 4 | `జ` 0.12 · `మం` 0.68 · `తు` 0.96 · `డ` 0.99 · `ె` 0.86 · `న్` 0.04✱ · `␣జ` 3.4e-4✱ · `య` 2.7e-3✱ · `్వర` 1.2e-4✱ · `␣మ` 0.05✱ · `్ర` 1.5e-4✱ · `్ర` 3.1e-6✱ · `్` 6.5e-4✱ · `న` 4.5e-3✱ · `న` 0.01✱ · `్రు` 1.6e-5✱ · `␣వే` 2.7e-3✱ · `గా` 8.4e-3✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 67 tokens · 16.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | స సీమమున్నిన్ జయ శగ్రివమ్రో | `IUIUUIIUIUU` |
| 2 | ససత్రిమున్నన్ జయ ల్య్ర్జల్రిముస్రా | `IUIUUIIUIUU` |
| 3 | ససన్ని లై లంకక మ్ర్వ్జమ్రుముస్రా | `IUIUUIIUIUU` |
| 4 | య సీత సీతివ్ సట నాకు ట్టింగా | `IUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 24% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.019 · model's first choice kept 30% · constraint overrode 58% · backtracks 0

<details><summary>Token probabilities (67 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 0.02 · `␣సీ` 0.05 · `మ` 0.02 · `ము` 0.05 · `న్ని` 0.08✱ · `న్` 0.02✱ · `␣జ` 0.17✱ · `య` 0.40 · `␣శ` 0.01✱ · `గ` 0.02✱ · `్రి` 3.3e-3✱ · `వ` 0.76 · `మ` 6.0e-3✱ · `్రో` 1.2e-4✱ · `⏎` 0.03✱ forced |
| 2 | `స` 0.73 · `స` 0.05 · `త` 0.09 · `్రి` 1.8e-3✱ · `ము` 0.16 · `న్న` 0.03 · `న్` 0.78 · `␣జ` 0.88 · `య` 0.75 · `␣ల` 0.50 · `్య` 4.9e-4✱ · `్ర` 2.4e-4✱ · `్` 9.9e-7✱ · `జ` 0.19✱ · `ల` 0.07 · `్రి` 1.3e-4✱ · `ము` 0.07✱ · `స` 0.13✱ · `్రా` 1.4e-4✱ · `⏎` 0.12 forced |
| 3 | `స` 0.35 · `స` 0.01✱ · `న్ని` 0.68 · `␣ల` 0.02✱ · `ై` 0.01✱ · `␣ల` 0.28 · `ంక` 0.23✱ · `క` 0.65 · `␣మ` 0.04✱ · `్ర` 8.6e-4✱ · `్వ` 1.9e-6✱ · `్` 7.5e-6✱ · `జ` 0.69 · `మ` 0.02✱ · `్రు` 1.6e-4✱ · `ము` 0.09✱ · `స` 0.25✱ · `్రా` 3.5e-3✱ · `⏎` 0.41 |
| 4 | `య` 0.27 · `␣సీ` 0.76 · `త` 0.69 · `␣సీ` 0.27 · `తి` 0.49 · `వ` 7.3e-3✱ · `్` 9.5e-5✱ · `␣స` 6.8e-3✱ · `ట` 0.03✱ · `␣నాకు` 8.2e-3✱ · `␣` 0.01✱ · `ట్టి` 1.0e-4✱ · `ంగా` 3.0e-4✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 73 tokens · 19.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మమల్రుచున్ సమ్రిము ధ్వ్వ్మై యమన్ముమ్ | `IUIUUIIUIUU` |
| 2 | లముమ్ములల్యన్ శర హ్లాంజతుడ్యా | `IUIUUIIUIUU` |
| 3 | మమమ్రుచున్ మల్య ప జ్ర్ర్మాయమమ్యా | `IUIUUIIUIUU` |
| 4 | న్మమంకనున్ జల్లచునంముడున్రీ | `IUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 15% · repeated lines 0 · mean token probability (geometric) 0.007 · model's first choice kept 27% · constraint overrode 66% · backtracks 0

<details><summary>Token probabilities (73 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.47 · `మ` 0.15 · `ల` 0.31 · `్రు` 4.6e-5✱ · `చు` 0.07 · `న్` 7.1e-3✱ · `␣స` 0.30 · `మ` 3.9e-3✱ · `్రి` 4.6e-4✱ · `ము` 0.27 · `␣ధ` 2.5e-3✱ · `్వ` 4.1e-4✱ · `్వ` 1.2e-3✱ · `్` 1.3e-6✱ · `మ` 9.3e-4✱ · `ై` 3.5e-3✱ · `␣య` 0.02 · `మ` 0.52 · `న్` 0.05✱ · `ము` 5.2e-4✱ · `మ్` 1.5e-3 · `⏎` 0.02✱ forced |
| 2 | `ల` 0.66 · `ము` 0.05✱ · `మ్ము` 5.8e-4✱ · `ల` 0.06✱ · `ల` 3.4e-3✱ · `్య` 6.1e-4✱ · `న్` 4.9e-3✱ · `␣శ` 6.0e-3✱ · `ర` 0.99 · `␣హ` 0.89 · `్లా` 1.7e-6✱ · `ంజ` 0.02✱ · `తు` 0.98 · `డ` 0.02✱ · `్యా` 1.3e-3✱ · `⏎` 0.32 |
| 3 | `మ` 0.77 · `మ` 8.3e-3✱ · `మ` 0.01✱ · `్రు` 3.6e-3✱ · `చు` 0.13✱ · `న్` 2.9e-3✱ · `␣మ` 0.21 · `ల` 0.74 · `్య` 3.1e-5✱ · `␣ప` 4.8e-4✱ · `␣జ` 3.3e-5✱ · `్ర` 1.2e-7✱ · `్ర` 2.5e-4✱ · `్` 1.3e-7✱ · `మ` 3.9e-3✱ · `ాయ` 0.04✱ · `మ` 0.13 · `మ` 0.43 · `్యా` 3.7e-5✱ · `⏎` 0.01✱ forced |
| 4 | `న్` 0.28 · `మ` 0.05✱ · `మ` 2.7e-3✱ · `ం` 0.53 · `క` 0.89 · `ను` 0.95 · `న్` 1.8e-3✱ · `␣జ` 0.02✱ · `ల్ల` 0.93 · `చు` 0.80 · `నం` 3.7e-4✱ · `ము` 4.8e-5✱ · `డు` 6.2e-4✱ · `న` 1.0e-3✱ · `్రీ` 3.5e-4✱ |

</details>

[↑ meters](#meters)

---

<a id="salini"></a>

## 14. శాలిని (salini)

```text
Meter: శాలిని (salini), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: మ త త గా, i.e. UUU UUI UUI UU (11 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 7th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter శాలిని (salini).

Meter: శాలిని (salini), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: మ త త గా, i.e. UUU UUI UUI UU (11 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 7th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 79 tokens · 18.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మామల్రిమ్రద్రువ్రిమత్యామముక్యా | `UUUUUIUUIUU` |
| 2 | త్రామమ్రిమ్రద్రువ్రితత్యామవమ్మత్ | `UUUUUIUUIUU` |
| 3 | మ్ర్రైమువ్రిమ్యా లోన య్య్య్రామల్రిమమ్రువ్ | `UUUUUIUUIUU` |
| 4 | మ్యామమ్యా మఛ్యస్సు మశ్లేషణైనశ్ | `UUUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.021 · model's first choice kept 41% · constraint overrode 51% · backtracks 0

<details><summary>Token probabilities (79 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.17 · `మ` 0.15 · `ల` 0.05✱ · `్రి` 3.6e-5✱ · `మ` 0.03✱ · `్ర` 1.1e-3✱ · `ద` 0.45 · `్రు` 1.4e-4✱ · `వ` 0.34 · `్రి` 4.6e-5✱ · `మ` 0.14 · `త` 0.06 · `్యా` 7.6e-3✱ · `మ` 0.23 · `ము` 0.11 · `క` 0.03 · `్యా` 8.7e-4✱ · `⏎` 0.46 forced |
| 2 | `త` 0.16 · `్రా` 1.6e-4✱ · `మ` 0.14✱ · `మ` 0.15 · `్రి` 1.2e-3✱ · `మ` 0.34 · `్ర` 3.0e-3✱ · `ద` 0.30 · `్రు` 0.98 · `వ` 0.95 · `్రి` 0.75 · `త` 1.2e-3✱ · `త` 0.80 · `్యా` 0.60 · `మ` 0.42 · `వ` 0.05 · `మ్` 0.01✱ · `మ` 3.1e-4✱ · `త` 0.28✱ · `్` 9.5e-6✱ · `⏎` 9.5e-3✱ forced |
| 3 | `మ` 0.31✱ · `్ర` 3.3e-4✱ · `్ర` 0.40 · `ై` 1.8e-3✱ · `ము` 0.02✱ · `వ` 0.72 · `్రి` 0.52 · `మ` 0.92 · `్యా` 9.5e-4✱ · `␣లో` 0.13✱ · `న` 0.91 · `␣య` 8.6e-4✱ · `్య` 1.2e-5✱ · `్య` 3.4e-5✱ · `్రా` 2.6e-4✱ · `మ` 0.54 · `ల` 0.74 · `్రి` 0.41 · `మ` 0.91 · `మ` 0.09✱ · `్రు` 2.1e-3✱ · `వ` 7.8e-3✱ · `్` 9.3e-6✱ · `⏎` 0.06✱ forced |
| 4 | `మ` 0.75 · `్యా` 1.8e-3✱ · `మ` 0.29 · `మ` 0.76 · `్యా` 3.1e-3✱ · `␣మ` 5.5e-3✱ · `ఛ` 0.52 · `్య` 3.8e-4✱ · `స్సు` 0.71 · `␣మ` 2.1e-3✱ · `శ్` 0.98 · `లే` 0.98 · `షణ` 0.15 · `ైన` 1.2e-3✱ · `శ` 0.81 · `్` 1.1e-8✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 74 tokens · 21.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రా సీమత్యా రర్వ జ్య్వ్రమ్రార సర్యా | `UUUUUIUUIUU` |
| 2 | రా సాకల్యం లంక శ్రమ్రన్ జరన్రా | `UUUUUIUUIUU` |
| 3 | స్రాసం దాటిజ్యమ్వరన్ రార సీతన్ | `UUUUUIUUIUU` |
| 4 | రై సీయమ్యర్యాము ల్ల్య్నయ్వర్వరయ్యయ్ | `UUUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 35% · constraint overrode 59% · backtracks 0

<details><summary>Token probabilities (74 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.31 · `␣సీ` 0.06 · `మ` 0.02 · `త` 0.10 · `్యా` 2.7e-3✱ · `␣ర` 0.11 · `ర` 0.10 · `్వ` 2.4e-4✱ · `␣జ` 0.10 · `్య` 7.4e-4✱ · `్వ` 1.0e-3✱ · `్ర` 1.7e-4✱ · `మ` 0.02✱ · `్రా` 1.1e-4✱ · `ర` 0.02✱ · `␣స` 6.0e-3✱ · `ర` 0.11✱ · `్యా` 1.6e-4✱ · `⏎` 0.46 |
| 2 | `రా` 0.95 · `␣సా` 2.0e-3✱ · `క` 0.10 · `ల` 0.14 · `్యం` 7.3e-4✱ · `␣ల` 0.40 · `ంక` 0.70 · `␣శ` 0.40 · `్రమ` 2.7e-4✱ · `్ర` 1.3e-4✱ · `న్` 0.94 · `␣జ` 0.85 · `ర` 0.48 · `న్` 0.01✱ · `రా` 5.6e-4✱ · `⏎` 0.02✱ forced |
| 3 | `␣స` 0.82 · `్రా` 1.6e-5✱ · `స` 0.01✱ · `ం` 0.06✱ · `␣దా` 0.95 · `టి` 0.94 · `జ` 5.7e-4✱ · `్య` 4.2e-3✱ · `మ` 1.6e-3✱ · `్వ` 3.1e-5✱ · `ర` 0.93 · `న్` 0.80 · `␣రా` 4.1e-3✱ · `ర` 0.04✱ · `␣సీ` 0.58 · `త` 0.73 · `న్` 0.87 · `⏎` 0.21✱ forced |
| 4 | `ర` 0.71 · `ై` 0.01✱ · `␣సీ` 3.1e-3✱ · `య` 0.94 · `మ` 5.4e-3✱ · `్య` 1.4e-3✱ · `ర` 0.96 · `్యా` 1.1e-3✱ · `ము` 0.21 · `␣` 2.1e-3✱ · `ల్ల` 6.4e-3✱ · `్య` 1.6e-3✱ · `్` 7.3e-4✱ · `న` 1.6e-4✱ · `య` 2.9e-3✱ · `్వర` 3.3e-4✱ · `్వర` 9.6e-5✱ · `య` 0.93 · `్య` 7.4e-5✱ · `య` 1.7e-4✱ · `్` 1.9e-4✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 91 tokens · 50.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సిగ్రివ్రిజ్రై అయ్య శింప్రిజ్యమున్ సర్ | `UUUUUIUUIUU` |
| 2 | రూగ్రివ్యాటెడ్యమ్రు స్ర్యున్ ఉన్నకట్యున్ | `UUUUUIUUIUU` |
| 3 | వెగ్రంకన్ జడ్రెన్రి మ్చ్ర్నిజ్రల్లకిక్రా | `UUUUUIUUIUU` |
| 4 | తీగ్రెన్రిన్గన్నారు క్య్య్తిన్రాణినిఛ్యున్ | `UUUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 43% · constraint overrode 53% · backtracks 30

<details><summary>Token probabilities (91 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `సి` 0.84 · `గ` 0.99 · `్రి` 1.00 · `వ` 0.85 · `్రి` 4.2e-5✱ · `జ` 3.4e-3✱ · `్ర` 4.6e-3✱ · `ై` 0.05✱ · `␣అయ్య` 1.0e-4 · `␣శి` 5.2e-3 · `ం` 0.46 · `ప` 0.90 · `్రి` 0.96 · `జ` 1.00 · `్య` 0.99 · `ము` 0.94 · `న్` 0.97 · `␣సర్` 0.07 · `⏎` 1.00 |
| 2 | `రూ` 6.7e-6 · `గ` 1.00 · `్రి` 1.00 · `వ` 1.00 · `్యా` 0.98 · `ట` 0.89 · `ె` 1.00 · `డ` 1.00 · `్య` 0.99 · `మ` 0.95 · `్రు` 3.9e-5✱ · `␣స` 0.81 · `్ర` 0.99 · `్య` 1.8e-6✱ · `ు` 0.02✱ · `న్` 0.03✱ · `␣ఉన్న` 2.3e-5✱ · `క` 0.94 · `ట` 0.98 · `్య` 9.8e-4✱ · `ు` 0.04✱ · `న` 0.63 · `్` 2.1e-8✱ · `⏎` 1.8e-3✱ forced |
| 3 | `వె` 0.22✱ · `గ` 4.0e-5✱ · `్ర` 1.3e-5✱ · `ం` 0.90 · `క` 0.62 · `న్` 4.0e-3✱ · `␣జ` 0.98 · `డ` 1.00 · `్ర` 2.9e-5✱ · `ె` 0.93 · `న` 2.2e-3✱ · `్రి` 4.7e-6✱ · `␣మ` 0.02✱ · `్` 5.3e-5✱ · `చ` 1.00 · `్ర` 1.3e-4✱ · `్` 3.5e-6✱ · `ని` 2.1e-3✱ · `జ` 0.90 · `్ర` 8.7e-6✱ · `ల్ల` 1.00 · `కి` 0.96 · `క` 5.8e-4✱ · `్రా` 9.0e-6✱ · `⏎` 0.01✱ forced |
| 4 | `తీ` 0.29 · `గ` 3.6e-3✱ · `్ర` 5.7e-6✱ · `ె` 0.87 · `న` 8.9e-3✱ · `్రి` 0.04✱ · `న్` 2.6e-4✱ · `గ` 0.90 · `న్నారు` 1.3e-4✱ · `␣క` 5.1e-3✱ · `్య` 1.9e-4✱ · `్య` 4.4e-3✱ · `్` 6.7e-7✱ · `త` 0.02✱ · `ిన` 7.2e-4✱ · `్రా` 1.3e-4✱ · `ణి` 0.05✱ · `ని` 0.43 · `ఛ` 0.01✱ · `్య` 3.9e-4✱ · `ు` 0.02✱ · `న` 2.1e-3✱ · `్` 3.0e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 81 tokens · 54.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | క్రామన్ లోగల్ మాతృ మ్రవ్యం వికాసమ్ | `UUUUUIUUIUU` |
| 2 | యామెన్నాపంతిన్ ల ల్యడ్యం మతృమ్యం | `UUUUUIUUIUU` |
| 3 | కై మాదిశ్యమ్రమ్రుకత్యాకమున్ న్నా | `UUUUUIUUIUU` |
| 4 | తా మవ్యం లేదుశ్యు మ్య్య్దద్యానమాన్న్దిన్ | `UUUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 6% · single-akshara words 25% · repeated lines 0 · mean token probability (geometric) 0.008 · model's first choice kept 25% · constraint overrode 63% · backtracks 30

<details><summary>Token probabilities (81 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.14 · `్రా` 0.06 · `మ` 0.97 · `న్` 0.76 · `␣లో` 0.99 · `గ` 0.86 · `ల్` 5.2e-4 · `␣మ` 0.03 · `ాత` 1.00 · `ృ` 1.00 · `␣మ` 0.46 · `్ర` 0.66 · `వ` 0.92 · `్యం` 0.50 · `␣వి` 0.96 · `కా` 0.94 · `స` 0.36 · `మ` 0.05✱ · `్` 7.2e-6✱ · `⏎` 0.82 |
| 2 | `యా` 1.2e-3 · `మె` 0.01 · `న్నా` 8.0e-3 · `పం` 2.4e-5 · `తి` 0.07 · `న్` 0.01✱ · `␣ల` 5.2e-5✱ · `␣ల` 6.0e-4✱ · `్య` 4.6e-5✱ · `డ` 1.2e-3✱ · `్యం` 2.7e-4✱ · `␣` 8.7e-4✱ · `మ` 5.0e-3✱ · `త` 0.86 · `ృ` 0.93 · `మ` 0.07✱ · `్యం` 1.1e-3✱ · `⏎` 0.03✱ forced |
| 3 | `క` 0.84 · `ై` 2.2e-3✱ · `␣మా` 8.2e-4✱ · `ది` 0.97 · `శ` 1.7e-4✱ · `్య` 2.9e-3✱ · `మ` 3.1e-3✱ · `్రమ` 2.0e-8✱ · `్రు` 2.7e-3✱ · `క` 4.4e-4✱ · `త` 1.4e-3✱ · `్యా` 3.1e-5✱ · `క` 0.96 · `ము` 0.99 · `న్` 0.89 · `␣` 0.05✱ · `న్నా` 1.2e-3✱ · `⏎` 0.05✱ forced |
| 4 | `␣` 9.2e-5✱ · `త` 7.2e-5✱ · `ా` 4.9e-6✱ · `␣` 4.5e-4✱ · `మ` 2.7e-3✱ · `వ` 5.7e-3✱ · `్యం` 6.8e-3✱ · `␣లేదు` 0.12✱ · `శ` 1.8e-3✱ · `్య` 3.3e-3✱ · `ు` 4.7e-3✱ · `␣మ` 3.5e-3✱ · `్య` 9.8e-4✱ · `్య` 0.01✱ · `్` 4.3e-5✱ · `ద` 1.8e-4✱ · `ద` 0.02✱ · `్యా` 2.2e-3✱ · `న` 9.0e-3✱ · `మా` 0.03✱ · `న్` 0.01✱ · `న్` 0.04✱ · `ది` 0.01✱ · `న` 9.8e-3✱ · `్` 8.3e-5✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 71 tokens · 19.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పమ్యమ్రుత్యా ప్రేమ మ్ర్య్వర్యం తమత్యం | `UUUUUIUUIUU` |
| 2 | త్యా మ్యా ప్రేమించమ్యతత్యమ్రుతక్యం | `UUUUUIUUIUU` |
| 3 | తమ్యమ్రుత్యా మమ్య్రుతక్యాకమున్ ఏ | `UUUUUIUUIUU` |
| 4 | లే మ్యమ్యా లవ్యల్య లే లేదు లేదుక్ | `UUUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 31% · repeated lines 0 · mean token probability (geometric) 0.014 · model's first choice kept 34% · constraint overrode 58% · backtracks 0

<details><summary>Token probabilities (71 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.03 · `మ` 0.18 · `్య` 7.5e-4✱ · `మ` 0.28 · `్రు` 4.2e-4✱ · `త` 0.18 · `్యా` 4.3e-3✱ · `␣ప్రేమ` 0.12 · `␣మ` 0.14✱ · `్ర` 4.6e-4✱ · `్య` 2.5e-6✱ · `్వర` 4.5e-5✱ · `్యం` 6.9e-5✱ · `␣` 7.3e-5✱ · `త` 0.40 · `మ` 0.97 · `త్య` 3.6e-4✱ · `ం` 1.3e-3 · `⏎` 2.5e-3✱ forced |
| 2 | `త` 0.48 · `్యా` 0.39 · `␣మ` 2.9e-5✱ · `్యా` 1.1e-5✱ · `␣ప్రేమ` 0.13 · `ించ` 1.7e-3✱ · `మ` 0.14✱ · `్య` 3.2e-4✱ · `త` 0.57 · `త` 0.08 · `్య` 0.30✱ · `మ` 0.76 · `్రు` 0.82 · `త` 0.90 · `క` 0.03✱ · `్యం` 1.3e-4✱ · `⏎` 0.56 |
| 3 | `త` 0.07 · `మ` 0.28 · `్య` 0.01✱ · `మ` 0.06✱ · `్రు` 0.16 · `త` 0.16✱ · `్యా` 0.32 · `␣మ` 0.71 · `మ` 0.31 · `్య` 4.1e-3✱ · `్రు` 0.90 · `త` 0.98 · `క` 3.8e-3✱ · `్యా` 5.7e-6✱ · `క` 0.80 · `ము` 0.98 · `న్` 0.90 · `␣ఏ` 1.00 · `⏎` 3.8e-4✱ forced |
| 4 | `లే` 0.77 · `␣` 1.5e-3✱ · `మ` 3.1e-5✱ · `్య` 2.4e-3✱ · `మ` 4.1e-3✱ · `్యా` 3.2e-3✱ · `␣ల` 4.0e-3✱ · `వ` 0.01✱ · `్య` 1.0e-4✱ · `ల` 5.7e-3✱ · `్య` 1.4e-3✱ · `␣లే` 3.7e-3✱ · `␣లేదు` 7.3e-3✱ · `␣లేదు` 7.8e-3✱ · `క` 4.7e-3✱ · `్` 1.1e-5✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 75 tokens · 17.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జక్రాకల్యానమ్రు మ్ర్జన్రత్రి మమ్యా | `UUUUUIUUIUU` |
| 2 | కక్రావక్రావమ్రు కక్రావకమ్యా | `UUUUUIUUIUU` |
| 3 | మ్యాక్రుక్యాతక్రువ్యమల్యామమక్యా | `UUUUUIUUIUU` |
| 4 | జ్ర్య్యాక్రియ్యానమ్యాక మ్యా మమ్య లోకం | `UUUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 10% · single-akshara words 10% · repeated lines 0 · mean token probability (geometric) 0.025 · model's first choice kept 44% · constraint overrode 45% · backtracks 0

<details><summary>Token probabilities (75 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.14 · `క` 0.05 · `్రా` 2.4e-3✱ · `క` 0.03 · `ల` 0.16 · `్యా` 5.7e-4✱ · `న` 0.13 · `మ` 0.06✱ · `్రు` 1.5e-3✱ · `␣మ` 0.08✱ · `్ర` 8.2e-4✱ · `్` 1.3e-5✱ · `జ` 0.10✱ · `న` 0.43 · `్ర` 1.5e-5✱ · `త` 0.05 · `్రి` 7.8e-4✱ · `␣మ` 0.20 · `మ` 0.37 · `్యా` 6.4e-4✱ · `⏎` 0.28 |
| 2 | `క` 0.18 · `క` 0.30 · `్రా` 1.2e-3✱ · `వ` 0.08 · `క` 0.15 · `్రా` 9.8e-4✱ · `వ` 0.10 · `మ` 0.23 · `్రు` 0.06✱ · `␣క` 0.22 · `క` 0.16 · `్రా` 1.3e-3✱ · `వ` 0.64 · `క` 0.13 · `మ` 0.09 · `్యా` 4.5e-3✱ · `⏎` 4.2e-3✱ forced |
| 3 | `మ` 0.58 · `్యా` 0.18 · `క` 8.2e-3✱ · `్రు` 8.0e-5✱ · `క` 0.04✱ · `్యా` 4.1e-3✱ · `త` 0.86 · `క` 0.12 · `్రు` 2.4e-4✱ · `వ` 0.16 · `్య` 4.8e-4✱ · `మ` 0.97 · `ల` 3.1e-4✱ · `్యా` 4.5e-3✱ · `మ` 0.66 · `మ` 0.01✱ · `క` 0.88 · `్యా` 9.1e-4✱ · `⏎` 0.25 forced |
| 4 | `జ` 0.08✱ · `్ర` 5.5e-4✱ · `్య` 2.8e-4✱ · `్యా` 0.56 · `క` 7.2e-4✱ · `్రియ` 1.5e-5✱ · `్యా` 0.37 · `న` 0.96 · `మ` 0.87 · `్యా` 0.83 · `క` 0.54 · `␣మ` 3.6e-3✱ · `్యా` 0.87 · `␣మ` 0.79 · `మ` 0.83 · `్య` 9.9e-4✱ · `␣లో` 1.00 · `కం` 1.4e-3 |

</details>

[↑ meters](#meters)

---

<a id="rathoddhata"></a>

## 15. రథోద్ధత (rathoddhata)

```text
Meter: రథోద్ధత (rathoddhata), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: ర న ర వ, i.e. UIU III UIU IU (11 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 7th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter రథోద్ధత (rathoddhata).

Meter: రథోద్ధత (rathoddhata), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: ర న ర వ, i.e. UIU III UIU IU (11 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 7th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 79 tokens · 18.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కంజ మల్రము జ శ్వ్వ్గన్రయన్ లకమ్ | `UIUIIIUIUIU` |
| 2 | మృం జలమ్రి తల ప్ర్రియ్యమున్నమల్ | `UIUIIIUIUIU` |
| 3 | నృంజ లన్య జల సృద్ర లమ్యసస్ | `UIUIIIUIUIU` |
| 4 | క్షోంజయమ్ర అడిగుథ్యుతఛ్యొసయ్ | `UIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.009 · model's first choice kept 28% · constraint overrode 65% · backtracks 0

<details><summary>Token probabilities (79 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.08 · `ంజ` 0.02✱ · `␣మ` 0.03 · `ల` 0.11 · `్ర` 3.9e-4✱ · `ము` 0.05 · `␣జ` 0.06 · `␣శ` 6.6e-3✱ · `్వ` 6.5e-4✱ · `్వ` 1.7e-3✱ · `్` 5.0e-5✱ · `గ` 0.01✱ · `న` 2.4e-3✱ · `్ర` 1.5e-4✱ · `య` 0.02 · `న్` 0.01✱ · `␣ల` 1.8e-3✱ · `క` 0.68 · `మ` 0.02✱ · `్` 5.1e-8✱ · `⏎` 0.03✱ forced |
| 2 | `మ` 0.36 · `ృ` 1.6e-3✱ · `ం` 7.4e-3✱ · `␣జ` 0.21 · `ల` 0.68 · `మ` 0.02✱ · `్రి` 5.8e-3✱ · `␣త` 0.11 · `ల` 0.26 · `␣ప` 0.01 · `్ర` 8.0e-4✱ · `్రియ` 1.1e-4✱ · `్య` 4.6e-5✱ · `ము` 0.28✱ · `న్` 0.03✱ · `న` 0.58 · `మ` 0.65 · `ల` 0.02✱ · `్` 2.4e-7✱ · `⏎` 0.25✱ forced |
| 3 | `న` 0.47 · `ృ` 5.0e-3✱ · `ంజ` 0.04✱ · `␣ల` 0.43 · `న` 0.72 · `్య` 2.8e-4✱ · `␣జ` 0.93 · `ల` 0.97 · `␣స` 0.91 · `ృ` 3.2e-4✱ · `ద్ర` 0.94 · `␣ల` 0.45 · `మ` 0.04✱ · `్య` 3.2e-4✱ · `స` 0.24✱ · `స` 0.26 · `్` 2.9e-6✱ · `⏎` 0.12✱ forced |
| 4 | `క్ష` 0.19✱ · `ో` 7.5e-3✱ · `ం` 2.3e-6✱ · `జయ` 2.6e-3✱ · `మ` 6.9e-3✱ · `్ర` 3.0e-4✱ · `␣అ` 0.83 · `డి` 0.89 · `గ` 9.7e-3✱ · `ు` 3.1e-4✱ · `థ` 0.21✱ · `్య` 4.1e-5✱ · `ు` 0.05✱ · `త` 0.99 · `ఛ` 1.2e-5✱ · `్య` 1.5e-4✱ · `ొ` 4.1e-4✱ · `స` 6.2e-3✱ · `య` 0.68 · `్` 3.7e-6✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 75 tokens · 18.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాము లొక్రి లను న్ర్వ్మత్రి జన్వరన్ | `UIUIIIUIUIU` |
| 2 | రాము దాత లతు నర్వరృమ్రి మ్వర్ | `UIUIIIUIUIU` |
| 3 | సీమ మత్రిను న్ర్వ్మ త్ర్ర్జిన్రియయ్రమల్ | `UIUIIIUIUIU` |
| 4 | రై మమత్రి మ్వర లత్న్ల లర్మువే | `UIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 16% · single-akshara words 16% · repeated lines 0 · mean token probability (geometric) 0.010 · model's first choice kept 29% · constraint overrode 56% · backtracks 0

<details><summary>Token probabilities (75 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.02 · `ము` 0.08 · `␣ల` 0.06 · `ొ` 0.02 · `క` 0.33 · `్రి` 2.7e-4✱ · `␣ల` 0.21 · `ను` 0.02 · `␣న` 0.02✱ · `్ర` 5.5e-4✱ · `్వ` 5.5e-4✱ · `్` 9.1e-6✱ · `మ` 0.01✱ · `త` 5.8e-3✱ · `్రి` 3.1e-4✱ · `␣జన` 1.1e-3 · `్వర` 1.4e-3✱ · `న్` 4.9e-3✱ · `⏎` 0.91 |
| 2 | `రా` 0.74 · `ము` 0.72 · `␣ద` 0.03 · `ాత` 4.8e-3 · `␣ల` 0.11 · `తు` 2.0e-3 · `␣న` 0.37 · `ర` 0.13 · `్వర` 9.0e-5✱ · `ృ` 5.5e-4✱ · `మ` 0.02✱ · `్రి` 1.8e-3✱ · `␣మ` 0.08 · `్వర` 0.24 · `్` 3.0e-6✱ · `⏎` 0.99 |
| 3 | `సీ` 0.98 · `మ` 5.6e-4✱ · `␣మ` 0.84 · `త` 1.2e-3✱ · `్రి` 3.3e-3✱ · `ను` 0.58 · `␣న` 0.83 · `్ర` 1.1e-3✱ · `్వ` 0.05✱ · `్` 0.97 · `మ` 0.96 · `␣త` 6.8e-4✱ · `్ర` 4.3e-5✱ · `్ర` 1.1e-3✱ · `్` 4.1e-4✱ · `జ` 6.4e-3✱ · `ిన` 2.9e-4✱ · `్రియ` 1.7e-5✱ · `య` 0.03✱ · `్రమ` 3.3e-5✱ · `ల` 0.17✱ · `్` 2.2e-7✱ · `⏎` 0.14✱ forced |
| 4 | `ర` 0.74 · `ై` 4.0e-5✱ · `␣మ` 0.41 · `మ` 0.38 · `త` 0.83 · `్రి` 0.62 · `␣మ` 0.60 · `్వర` 0.28 · `␣ల` 6.4e-3✱ · `త` 4.3e-3✱ · `్` 5.3e-4✱ · `న్` 1.1e-3✱ · `ల` 1.5e-3✱ · `␣ల` 8.9e-3✱ · `ర్` 1.7e-3✱ · `ము` 0.01✱ · `వే` 0.02✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 70 tokens · 36.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లితన్మరపు మ్ధ్వాల లేదుతమ్ | `UIUIIIUIUIU` |
| 2 | తల్లి గుణ్యపుత తల్యె మెడ్రు లోక్ | `UIUIIIUIUIU` |
| 3 | తల్లి దేవత వ వ్ర్ర్తత్రమత్రుతమ్ | `UIUIIIUIUIU` |
| 4 | వల్ లదిక్రమము ద్ర్వర్రమల్రుకౌ | `UIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 20% · repeated lines 0 · mean token probability (geometric) 0.015 · model's first choice kept 54% · constraint overrode 37% · backtracks 30

<details><summary>Token probabilities (70 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.72 · `ల్లి` 0.86 · `త` 0.76 · `న్` 0.89 · `మ` 0.51 · `ర` 0.81 · `పు` 0.88 · `␣మ` 0.99 · `్` 6.3e-6✱ · `ధ` 7.4e-3✱ · `్వ` 9.2e-3 · `ాల` 0.99 · `␣లేదు` 0.52 · `త` 0.02 · `మ` 0.65 · `్` 1.6e-7✱ · `⏎` 0.79 |
| 2 | `త` 0.98 · `ల్లి` 0.69 · `␣గు` 0.98 · `ణ` 0.99 · `్య` 0.99 · `పు` 1.3e-3 · `త` 3.1e-4 · `␣త` 0.77 · `ల` 0.98 · `్య` 2.7e-5✱ · `ె` 1.00 · `␣మె` 0.97 · `డ` 0.99 · `్రు` 7.8e-5✱ · `␣లో` 1.00 · `క` 1.00 · `్` 1.6e-9✱ · `⏎` 0.99 |
| 3 | `త` 1.00 · `ల్లి` 1.00 · `␣ద` 1.00 · `ే` 1.00 · `వ` 0.97 · `త` 0.98 · `␣వ` 0.07 · `␣వ` 0.02✱ · `్ర` 6.5e-4✱ · `్ర` 8.4e-4✱ · `్` 7.7e-8✱ · `త` 1.9e-4✱ · `త` 6.8e-5✱ · `్రమ` 2.8e-5✱ · `త` 3.2e-4✱ · `్రు` 6.9e-5✱ · `త` 0.64 · `మ` 0.01✱ · `్` 3.6e-5✱ · `⏎` 0.71 |
| 4 | `వ` 0.29 · `ల్` 7.6e-3✱ · `␣ల` 2.6e-6✱ · `ది` 0.85 · `క` 2.2e-4✱ · `్రమ` 1.2e-5✱ · `ము` 0.80 · `␣ద` 0.97 · `్ర` 8.1e-6✱ · `్వర` 7.2e-6✱ · `్రమ` 3.0e-5✱ · `ల` 3.7e-3✱ · `్రు` 4.5e-7✱ · `క` 0.91 · `ౌ` 0.30 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 73 tokens · 44.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాత ముమ్రు మధు ధ్ర్వ్మౌనలన్ మతిక్ | `UIUIIIUIUIU` |
| 2 | కౌతి గొప్ప మ మ కక్యవత్రమల్ | `UIUIIIUIUIU` |
| 3 | కీతినన్ అతిక జ్య్య్డించినన్ మతిక్ | `UIUIIIUIUIU` |
| 4 | నో తరేర్తితితినో మతిక్ మరన్ | `UIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.008 · model's first choice kept 29% · constraint overrode 64% · backtracks 30

<details><summary>Token probabilities (73 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.06 · `ాత` 0.07 · `␣ము` 7.3e-5 · `మ` 0.56 · `్రు` 8.4e-5✱ · `␣మ` 0.05 · `ధు` 0.97 · `␣ధ` 0.82 · `్ర` 0.89 · `్వ` 0.36✱ · `్` 2.1e-9✱ · `మ` 3.2e-3✱ · `ౌ` 1.00 · `న` 1.00 · `ల` 0.99 · `న్` 0.96 · `␣మ` 0.95 · `తి` 0.98 · `క` 2.0e-4✱ · `్` 1.2e-8✱ · `⏎` 0.02✱ forced |
| 2 | `క` 0.15 · `ౌ` 1.0e-3✱ · `తి` 0.02✱ · `␣గొప్ప` 0.59 · `␣మ` 0.01✱ · `␣మ` 0.84 · `␣క` 3.3e-4✱ · `క` 2.9e-3✱ · `్య` 4.1e-7✱ · `వ` 0.88 · `త` 0.65 · `్రమ` 6.6e-6✱ · `ల` 0.02✱ · `్` 8.3e-9✱ · `⏎` 0.24✱ forced |
| 3 | `క` 4.2e-3✱ · `ీ` 0.02✱ · `తి` 0.20✱ · `న` 0.76 · `న్` 9.8e-4✱ · `␣అతి` 2.8e-4✱ · `క` 0.92 · `␣జ` 0.96 · `్య` 8.4e-3✱ · `్య` 6.7e-4✱ · `్` 1.3e-7✱ · `డ` 0.99 · `ించిన` 2.2e-4✱ · `న్` 3.7e-3✱ · `␣మ` 9.0e-3✱ · `తి` 0.01✱ · `క` 5.8e-3✱ · `్` 0.24✱ · `⏎` 0.15 forced |
| 4 | `నో` 6.3e-5✱ · `␣` 1.2e-3✱ · `త` 1.6e-3✱ · `రే` 6.2e-4✱ · `ర్` 7.9e-3✱ · `తి` 7.2e-3✱ · `తి` 0.05✱ · `తి` 0.04✱ · `న` 0.02✱ · `ో` 2.9e-3✱ · `␣మ` 8.0e-3✱ · `తి` 0.21 · `క` 0.08✱ · `్` 0.04✱ · `␣మ` 4.0e-3✱ · `ర` 0.91 · `న` 0.02✱ · `్` 1.7e-7✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 71 tokens · 17.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జక్రి జల్రి పల జల్రముగ్య సా | `UIUIIIUIUIU` |
| 2 | జక్రి నల్రి పల న్ర్ర్జన్రియయ్రికం | `UIUIIIUIUIU` |
| 3 | మ్రిక్రిలల్రిలముగృమ్రిజక్రి వా | `UIUIIIUIUIU` |
| 4 | త్రిక్రి జల్రముగడృయ్వదువ్క్కడన్ | `UIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 31% · single-akshara words 15% · repeated lines 0 · mean token probability (geometric) 0.015 · model's first choice kept 32% · constraint overrode 54% · backtracks 0

<details><summary>Token probabilities (71 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.09 · `క` 0.03✱ · `్రి` 6.4e-3✱ · `␣జ` 0.23 · `ల` 0.09 · `్రి` 5.2e-5✱ · `␣ప` 0.02 · `ల` 0.04 · `␣జ` 1.9e-3✱ · `ల` 0.16 · `్ర` 1.1e-4✱ · `ము` 0.04 · `గ` 0.02✱ · `్య` 4.0e-4✱ · `␣సా` 0.01 · `⏎` 1.2e-3✱ forced |
| 2 | `జ` 0.05 · `క` 0.15 · `్రి` 0.09✱ · `␣న` 0.03 · `ల` 0.68 · `్రి` 0.28 · `␣ప` 0.35 · `ల` 0.85 · `␣న` 0.20 · `్ర` 2.8e-4✱ · `్ర` 1.6e-4✱ · `్` 6.5e-7✱ · `జ` 3.0e-3✱ · `న` 0.02✱ · `్రియ` 1.3e-4✱ · `య` 1.8e-3✱ · `్రి` 9.7e-5✱ · `కం` 2.8e-4 · `⏎` 4.0e-3✱ forced |
| 3 | `␣మ` 0.51 · `్రి` 1.0e-3✱ · `క` 2.5e-4✱ · `్రి` 0.01✱ · `ల` 0.82 · `ల` 0.07✱ · `్రి` 2.3e-3✱ · `ల` 0.29 · `ము` 0.56 · `గ` 0.68 · `ృ` 6.7e-6✱ · `మ` 9.6e-3✱ · `్రి` 3.9e-4✱ · `జ` 0.69 · `క` 0.49 · `్రి` 0.19✱ · `␣వా` 0.02 · `⏎` 0.01 forced |
| 4 | `త్రి` 0.35 · `క` 0.03✱ · `్రి` 0.33✱ · `␣జ` 0.89 · `ల` 0.93 · `్ర` 0.42 · `ము` 0.84 · `గ` 0.92 · `డ` 2.1e-3✱ · `ృ` 2.2e-5✱ · `య` 0.03✱ · `్` 3.3e-5✱ · `వ` 0.11✱ · `దు` 0.75 · `వ` 3.7e-4✱ · `్` 2.8e-4✱ · `క్కడ` 0.13✱ · `న్` 1.4e-4✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 77 tokens · 15.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నట్యమయ్య జల క్వ్య్నమ్య లంకకన్ | `UIUIIIUIUIU` |
| 2 | నట్యమయ్య జల శ్ర్మ్యమ్య లంకకన్ | `UIUIIIUIUIU` |
| 3 | నట్యమయ్య జల మ్యానమమ్యకం | `UIUIIIUIUIU` |
| 4 | న్నట్యమయ్య జల ధ్వ్వ్నమ్యకన్ నుమా | `UIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 27% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.068 · model's first choice kept 58% · constraint overrode 34% · backtracks 0

<details><summary>Token probabilities (77 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `న` 0.02 · `ట` 0.03 · `్య` 6.6e-3✱ · `మ` 0.32 · `య` 0.33 · `్య` 6.9e-5✱ · `␣జ` 0.05 · `ల` 0.03 · `␣క` 4.5e-3✱ · `్వ` 6.0e-4✱ · `్య` 2.7e-4✱ · `్` 6.4e-7✱ · `న` 4.2e-3✱ · `మ` 0.01✱ · `్య` 2.8e-3✱ · `␣ల` 0.18 · `ంక` 0.05 · `క` 0.07 · `న్` 0.06✱ · `⏎` 0.78 |
| 2 | `న` 0.57 · `ట` 0.24 · `్య` 0.31 · `మ` 0.34 · `య` 0.71 · `్య` 0.98 · `␣జ` 0.20 · `ల` 0.20 · `␣శ` 0.08 · `్ర` 8.9e-3✱ · `్` 6.7e-4✱ · `మ` 0.69 · `్య` 5.9e-3✱ · `మ` 0.84 · `్య` 0.38 · `␣ల` 0.61 · `ంక` 0.28 · `క` 0.80 · `న్` 0.99 · `⏎` 1.00 |
| 3 | `న` 0.99 · `ట` 1.00 · `్య` 0.99 · `మ` 0.99 · `య` 0.99 · `్య` 0.99 · `␣జ` 0.95 · `ల` 0.98 · `␣మ` 0.54 · `్యా` 3.4e-4✱ · `న` 0.63 · `మ` 0.63 · `మ` 0.11✱ · `్య` 0.10✱ · `కం` 6.6e-3✱ · `⏎` 0.16 forced |
| 4 | `న్` 0.29 · `న` 0.33 · `ట` 0.47 · `్య` 0.80 · `మ` 0.78 · `య` 0.75 · `్య` 0.76 · `␣జ` 0.86 · `ల` 0.93 · `␣ధ` 0.81 · `్వ` 2.0e-3✱ · `్వ` 1.1e-3✱ · `్` 1.3e-4✱ · `న` 0.05✱ · `మ` 0.36✱ · `్య` 0.22✱ · `క` 0.39 · `న్` 0.36 · `␣` 2.3e-4✱ · `ను` 9.5e-5✱ · `మా` 4.5e-5✱ |

</details>

[↑ meters](#meters)

---

<a id="sragvini"></a>

## 16. స్రగ్విణి (sragvini)

```text
Meter: స్రగ్విణి (sragvini), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: ర ర ర ర, i.e. UIU UIU UIU UIU (12 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 7th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T2; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter స్రగ్విణి (sragvini).

Meter: స్రగ్విణి (sragvini), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: ర ర ర ర, i.e. UIU UIU UIU UIU (12 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 7th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 83 tokens · 22.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామ హూమయ్యదండ్రన్కమున్ సీన్ననుల్ | `UIUUIUUIUUIU` |
| 2 | రామమౌళిక్రమల్రైన్న్క లంకక్ న్మ హౌ | `UIUUIUUIUUIU` |
| 3 | దౌ మకల్యంతతన్ల్వ్తౌమ హౌతిద్రిమున్ | `UIUUIUUIUUIU` |
| 4 | రామ సీరవ్రిలన్లక్యమించండి పైన్ | `UIUUIUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 15% · single-akshara words 31% · repeated lines 0 · mean token probability (geometric) 0.017 · model's first choice kept 37% · constraint overrode 47% · backtracks 0

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.29 · `మ` 0.55 · `␣హ` 6.5e-3 · `ూ` 6.6e-3✱ · `మయ్య` 2.3e-4 · `ద` 5.6e-3 · `ండ` 7.6e-3✱ · `్ర` 1.2e-3✱ · `న్` 8.7e-3✱ · `క` 6.1e-3 · `ము` 0.06 · `న్` 0.07 · `␣సీ` 0.04 · `న్` 0.03 · `న` 0.03 · `ను` 0.02✱ · `ల` 6.5e-3✱ · `్` 6.4e-8✱ · `⏎` 0.63 |
| 2 | `రా` 0.46 · `మ` 0.51 · `మ` 0.03 · `ౌ` 0.05 · `ళి` 0.04 · `క` 0.03 · `్రమ` 1.2e-4✱ · `ల` 0.03✱ · `్ర` 1.4e-3✱ · `ై` 4.3e-3✱ · `న్` 0.94 · `న్` 0.02 · `క` 0.04✱ · `␣ల` 0.24 · `ంక` 0.45 · `క` 0.37 · `్` 2.9e-5✱ · `␣` 2.0e-3✱ · `న్` 2.5e-3✱ · `మ` 0.78 · `␣హ` 0.23 · `ౌ` 0.95 · `⏎` 0.02✱ forced |
| 3 | `ద` 0.68 · `ౌ` 3.7e-4✱ · `␣` 5.6e-4✱ · `మ` 6.6e-5✱ · `క` 0.95 · `ల` 2.0e-3✱ · `్యం` 1.7e-3✱ · `త` 1.2e-3✱ · `త` 0.94 · `న్` 0.01✱ · `ల` 7.8e-3✱ · `్వ` 1.2e-5✱ · `్` 3.6e-3✱ · `త` 2.4e-4✱ · `ౌ` 7.3e-3✱ · `మ` 0.78 · `␣హ` 0.63 · `ౌ` 0.83 · `తి` 0.91 · `ద` 0.90 · `్రి` 5.7e-4✱ · `ము` 0.02✱ · `న్` 0.65 · `⏎` 0.14✱ forced |
| 4 | `రా` 0.12✱ · `మ` 0.42 · `␣సీ` 0.95 · `ర` 0.95 · `వ` 2.0e-4✱ · `్రి` 1.9e-6✱ · `ల` 0.95 · `న్` 0.89 · `ల` 4.6e-3✱ · `క` 2.4e-3✱ · `్య` 6.3e-4✱ · `మ` 0.64 · `ించండి` 0.58 · `␣` 4.3e-3✱ · `ప` 0.84 · `ైన` 0.99 · `్` 9.2e-10✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 83 tokens · 18.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాము లక్ష్మిజ్వరంగ్యగ్రిశమ్యర్వలః | `UIUUIUUIUUIU` |
| 2 | రాము జగ్రవ్రిశశ్రమ్యమర్వల్యమా | `UIUUIUUIUUIU` |
| 3 | తా మ మజ్రగ్రిశమ్య్య్తట్రరామన్ జనవ్ | `UIUUIUUIUUIU` |
| 4 | నై మయన్ర్వల్యముర్ర్యంననిస్రగ్విణిమ్ | `UIUUIUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 10% · single-akshara words 30% · repeated lines 0 · mean token probability (geometric) 0.018 · model's first choice kept 41% · constraint overrode 49% · backtracks 0

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.01 · `ము` 0.11 · `␣ల` 0.05 · `క్ష్` 0.31 · `మి` 0.29 · `జ` 2.6e-3✱ · `్వర` 2.4e-4✱ · `ంగ` 1.7e-3✱ · `్య` 1.2e-3✱ · `గ` 3.0e-3✱ · `్రి` 4.5e-3✱ · `శ` 0.29 · `మ` 0.08✱ · `్య` 8.1e-3✱ · `ర` 0.05✱ · `్వ` 8.9e-6✱ · `ల` 9.7e-3✱ · `ః` 1.8e-3✱ · `⏎` 0.89 |
| 2 | `రా` 0.64 · `ము` 0.55 · `␣జగ` 0.02 · `్ర` 6.0e-5✱ · `వ` 0.04 · `్రి` 4.7e-4✱ · `శ` 0.27 · `శ` 0.08 · `్ర` 6.6e-3✱ · `మ` 0.08 · `్య` 0.01✱ · `మ` 0.17 · `ర` 0.04 · `్వ` 1.6e-3✱ · `ల` 0.97 · `్య` 1.2e-4✱ · `మా` 2.3e-4✱ · `⏎` 1.7e-3✱ forced |
| 3 | `త` 0.58 · `ా` 7.2e-3✱ · `␣మ` 0.11✱ · `␣మ` 0.46 · `జ` 0.69 · `్ర` 5.1e-5✱ · `గ` 0.37 · `్రి` 0.85 · `శ` 0.94 · `మ` 0.96 · `్య` 0.85 · `్య` 2.0e-4✱ · `్` 1.2e-3✱ · `త` 8.3e-4✱ · `ట` 7.4e-3✱ · `్ర` 8.3e-5✱ · `రా` 0.96 · `మ` 0.93 · `న్` 0.99 · `␣జ` 0.93 · `న` 0.98 · `వ` 0.93 · `్` 5.4e-8✱ · `⏎` 2.3e-3✱ forced |
| 4 | `న` 0.94 · `ై` 1.3e-4✱ · `␣మ` 3.7e-4✱ · `య` 0.99 · `న` 0.62 · `్ర` 2.2e-5✱ · `్వ` 0.75 · `ల` 0.99 · `్య` 0.99 · `ము` 0.99 · `ర` 1.2e-4✱ · `్ర` 1.8e-7✱ · `్యం` 1.3e-4✱ · `న` 6.8e-3✱ · `ని` 0.03✱ · `స` 0.18✱ · `్ర` 0.82 · `గ్` 0.84 · `వి` 0.87 · `ణి` 0.77 · `మ` 3.8e-3✱ · `్` 8.5e-8✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 78 tokens · 44.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామ హుత్తమ్ర శత్రావవన్నుడ్రిరా | `UIUUIUUIUUIU` |
| 2 | మామ భమ్రిమ్ర బక్య్య్మడ్రనుడ్రాకమూర్ | `UIUUIUUIUUIU` |
| 3 | మౌమ లంకన్న్న్లిచిట్ర్య్మమ్రుయించుట్ర జన్ | `UIUUIUUIUUIU` |
| 4 | రైముగమ్రీతి పైనైన పక్యాలలో | `UIUUIUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.011 · model's first choice kept 37% · constraint overrode 54% · backtracks 30

<details><summary>Token probabilities (78 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.99 · `మ` 0.95 · `␣హ` 0.56 · `ు` 0.33 · `త్త` 0.03 · `మ` 0.41 · `్ర` 1.2e-6✱ · `␣శ` 0.01 · `త` 0.03 · `్రా` 2.6e-4✱ · `వ` 0.27 · `వ` 0.05 · `న్` 0.02✱ · `ను` 0.03 · `డ` 0.08✱ · `్రి` 5.7e-4✱ · `రా` 1.0e-3✱ · `⏎` 4.1e-3✱ forced |
| 2 | `మా` 0.05 · `మ` 4.3e-3✱ · `␣భ` 0.23 · `మ` 0.04 · `్రి` 5.1e-4✱ · `మ` 0.04✱ · `్ర` 1.8e-3✱ · `␣బ` 0.34 · `క` 0.86 · `్య` 3.8e-6✱ · `్య` 9.1e-6✱ · `్` 8.8e-8✱ · `మ` 1.8e-4✱ · `డ` 3.4e-3✱ · `్ర` 5.3e-4✱ · `ను` 0.09✱ · `డ` 0.07✱ · `్రా` 1.7e-3✱ · `క` 3.0e-3✱ · `మ` 0.46 · `ూర్` 0.65 · `⏎` 1.8e-4✱ forced |
| 3 | `␣మ` 0.32 · `ౌ` 0.49 · `మ` 1.9e-3✱ · `␣ల` 0.91 · `ంక` 0.74 · `న్` 3.3e-3✱ · `న్` 0.59 · `న్` 4.5e-3✱ · `లి` 0.91 · `చి` 0.85 · `ట` 2.0e-3✱ · `్ర` 3.2e-8✱ · `్య` 1.5e-5✱ · `్` 5.2e-6✱ · `మ` 0.13✱ · `మ` 0.06✱ · `్రు` 6.5e-5✱ · `య` 0.93 · `ించు` 0.86 · `ట` 0.86 · `్ర` 1.9e-5✱ · `␣జ` 1.7e-3✱ · `న` 0.87 · `్` 6.5e-10✱ · `⏎` 2.8e-3✱ forced |
| 4 | `ర` 0.94 · `ై` 2.0e-3✱ · `ము` 8.5e-5✱ · `గ` 0.70 · `మ` 2.4e-3✱ · `్రీ` 2.3e-4✱ · `తి` 3.2e-3✱ · `␣ప` 0.76 · `ైన` 0.99 · `ైన` 1.1e-3✱ · `␣ప` 0.97 · `క్య` 0.93 · `ాలలో` 0.99 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 93 tokens · 52.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వేతిచున్ జల్రముభ్రిన్యముయ్యాగరున్ | `UIUUIUUIUUIU` |
| 2 | రౌత ప్రమ్యాన్ని పూర్టస్రతిచ్రిల్రకన్ | `UIUUIUUIUUIU` |
| 3 | చేతియుగ్యున్న్త మాత్య్య్శేను చూడెన్ ట్టి ట్టిబ్ | `UIUUIUUIUUIU` |
| 4 | ల్లోతిమున్య్యన్యనన్య్య్లొందుమున్యానునున్ | `UIUUIUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.004 · model's first choice kept 24% · constraint overrode 70% · backtracks 30

<details><summary>Token probabilities (93 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వే` 0.62 · `తి` 0.28 · `చు` 8.2e-4 · `న్` 0.66 · `␣జ` 0.98 · `ల` 0.99 · `్ర` 4.9e-6✱ · `ము` 0.60 · `భ` 3.3e-3 · `్ర` 0.07✱ · `ిన` 0.93 · `్య` 0.93 · `ము` 0.64 · `య` 3.5e-4✱ · `్యా` 2.5e-6✱ · `గ` 0.98 · `రు` 9.8e-4 · `న్` 0.67 · `⏎` 0.16✱ forced |
| 2 | `ర` 6.7e-3✱ · `ౌ` 0.69 · `త` 0.04✱ · `␣ప్ర` 0.01 · `మ` 0.86 · `్యాన్ని` 0.99 · `␣పూర్` 3.2e-6 · `ట` 7.1e-3✱ · `స` 3.6e-4✱ · `్ర` 1.0e-5✱ · `తి` 0.95 · `చ` 0.02✱ · `్రి` 7.3e-5✱ · `ల` 0.35✱ · `్ర` 1.3e-4✱ · `క` 0.89 · `న` 1.2e-3✱ · `్` 1.5e-10✱ · `⏎` 0.09✱ forced |
| 3 | `␣చే` 0.63 · `తి` 4.2e-3✱ · `యు` 9.1e-3✱ · `గ` 1.8e-3✱ · `్య` 1.9e-4✱ · `ు` 0.03✱ · `న్` 0.91 · `న్` 2.2e-4✱ · `త` 0.76 · `␣మ` 0.95 · `ాత` 0.93 · `్య` 2.3e-7✱ · `్య` 1.3e-6✱ · `్` 8.3e-10✱ · `శ` 2.1e-3✱ · `ే` 0.03✱ · `ను` 4.1e-3✱ · `␣చూ` 7.1e-3✱ · `డ` 0.06✱ · `ె` 0.49 · `న` 1.1e-3✱ · `్` 6.1e-4✱ · `␣` 8.7e-4✱ · `ట్టి` 1.6e-6✱ · `␣` 1.3e-4✱ · `ట్టి` 7.0e-6✱ · `బ` 1.3e-7✱ · `్` 7.7e-9✱ · `⏎` 5.6e-4✱ forced |
| 4 | `ల్ల` 1.2e-3✱ · `ో` 3.5e-3✱ · `తి` 8.6e-3✱ · `ము` 0.01✱ · `న` 2.7e-3✱ · `్య` 8.7e-5✱ · `్య` 6.5e-3✱ · `న` 3.8e-3✱ · `్య` 9.8e-3✱ · `న` 0.06✱ · `న` 0.02✱ · `్య` 8.0e-3✱ · `్య` 0.04✱ · `్` 3.1e-3✱ · `ల` 0.04✱ · `ొ` 7.0e-3✱ · `ందు` 0.10✱ · `ము` 0.14 · `న` 3.6e-3✱ · `్యా` 3.6e-6✱ · `న` 1.5e-3✱ · `ు` 8.8e-4✱ · `న` 9.2e-3✱ · `ు` 0.01✱ · `న` 3.5e-3✱ · `్` 5.3e-4✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 75 tokens · 18.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాము లక్ష్మిర్రమల్వ్య్మర్వరచ్వర్వరయ్ | `UIUUIUUIUUIU` |
| 2 | రామ సీతాశయన్మ్రమ్వరమ్రల్యయం | `UIUUIUUIUUIU` |
| 3 | రామ లంకన్ వెళెన్ మ్రహ్రహమ్రోలయా | `UIUUIUUIUUIU` |
| 4 | రామమశ్యువ్వశించ్య్య్రామడల్యన్ క్షమా | `UIUUIUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 40% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.012 · model's first choice kept 35% · constraint overrode 52% · backtracks 0

<details><summary>Token probabilities (75 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.01 · `ము` 0.11 · `␣ల` 0.05 · `క్ష్` 0.31 · `మి` 0.29 · `ర` 1.9e-3✱ · `్రమ` 2.6e-4✱ · `ల` 0.03✱ · `్వ` 1.4e-4✱ · `్య` 2.0e-4✱ · `్` 4.8e-8✱ · `మ` 0.04✱ · `ర` 0.05✱ · `్వర` 4.8e-5✱ · `చ` 0.03 · `్వర` 3.6e-4✱ · `్వర` 1.2e-4✱ · `య` 6.6e-3✱ · `్` 2.5e-6✱ · `⏎` 0.75 |
| 2 | `రా` 0.93 · `మ` 0.87 · `␣సీ` 0.56 · `తా` 0.40 · `శ` 0.12 · `య` 0.06 · `న్` 0.04✱ · `మ` 0.21 · `్ర` 9.0e-4✱ · `మ` 0.15 · `్వర` 6.1e-4✱ · `మ` 0.05 · `్ర` 0.01✱ · `ల` 0.93 · `్య` 4.7e-4✱ · `యం` 1.4e-4✱ · `⏎` 1.00 |
| 3 | `రా` 1.00 · `మ` 0.96 · `␣ల` 0.98 · `ంక` 1.00 · `న్` 2.1e-5✱ · `␣వె` 0.98 · `ళ` 6.1e-4✱ · `ె` 1.00 · `న్` 4.0e-4✱ · `␣మ` 0.94 · `్రహ` 1.1e-6✱ · `్రహ` 2.2e-6✱ · `మ` 0.83 · `్రో` 5.9e-6✱ · `ల` 0.96 · `యా` 5.6e-4 · `⏎` 7.5e-5 forced |
| 4 | `రా` 0.04✱ · `మ` 0.01✱ · `మ` 0.69 · `శ` 7.2e-3✱ · `్య` 6.2e-4✱ · `ు` 0.99 · `వ` 0.04✱ · `్వ` 4.8e-4✱ · `శ` 0.97 · `ించ` 4.5e-3✱ · `్య` 2.5e-4✱ · `్య` 2.8e-4✱ · `్రా` 6.8e-4✱ · `మ` 0.81 · `డ` 0.92 · `ల` 0.84 · `్య` 8.7e-5✱ · `న్` 0.99 · `␣` 1.4e-3✱ · `క్ష` 0.03✱ · `మా` 1.5e-3✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 81 tokens · 23.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామ భక్తుల్వడై ల్రంకకున్రామరా | `UIUUIUUIUUIU` |
| 2 | మై మలన్నుడ్య జయ్య్య్మన్డటన్ సీతమా | `UIUUIUUIUUIU` |
| 3 | మై మువుల్రడ్యటట్య్య్మమ్మముప్యం ప ఈ | `UIUUIUUIUUIU` |
| 4 | ఈము స్రగ్విణ్యలో స్వ్ర్రృత్రమట్లుగ్రమా | `UIUUIUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 7% · single-akshara words 29% · repeated lines 0 · mean token probability (geometric) 0.010 · model's first choice kept 30% · constraint overrode 67% · backtracks 0

<details><summary>Token probabilities (81 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.29 · `మ` 0.55 · `␣భ` 0.04 · `క్త` 0.23 · `ుల` 0.02✱ · `్వ` 3.5e-3✱ · `డ` 0.03✱ · `ై` 0.03✱ · `␣ల` 0.38 · `్ర` 2.9e-4✱ · `ంక` 0.42 · `కు` 0.09✱ · `న్` 2.2e-3✱ · `రా` 0.52 · `మ` 0.26✱ · `రా` 0.01✱ · `⏎` 0.05✱ forced |
| 2 | `మ` 0.21 · `ై` 1.0e-3✱ · `␣మ` 0.02✱ · `ల` 0.05 · `న్` 0.02✱ · `ను` 0.05 · `డ` 0.03✱ · `్య` 1.9e-4✱ · `␣జ` 0.10 · `య` 0.22 · `్య` 3.1e-6✱ · `్య` 3.9e-5✱ · `్` 6.3e-7✱ · `మ` 3.0e-4✱ · `న్` 0.02✱ · `డ` 0.93 · `ట` 0.97 · `న్` 0.07✱ · `␣సీ` 0.42 · `త` 0.51 · `మా` 3.1e-3✱ · `⏎` 0.74 |
| 3 | `మ` 0.50 · `ై` 2.1e-4✱ · `␣మ` 7.7e-3✱ · `ు` 0.10✱ · `వు` 0.97 · `ల` 4.9e-4✱ · `్ర` 5.7e-5✱ · `డ` 0.97 · `్య` 1.1e-5✱ · `ట` 0.74 · `ట` 0.10✱ · `్య` 1.4e-4✱ · `్య` 1.4e-3✱ · `్` 7.8e-5✱ · `మ` 0.01✱ · `మ` 0.19✱ · `్` 2.1e-5✱ · `మ` 0.02✱ · `ము` 0.08✱ · `ప` 0.57 · `్యం` 6.7e-6✱ · `␣ప` 0.05✱ · `␣ఈ` 1.8e-3 · `⏎` 1.8e-3✱ forced |
| 4 | `ఈ` 0.19✱ · `ము` 9.5e-5✱ · `␣స` 0.01✱ · `్ర` 0.60 · `గ్` 0.04✱ · `వి` 0.27 · `ణ` 2.5e-3✱ · `్య` 0.03✱ · `లో` 0.05✱ · `␣స్వ` 0.98 · `్ర` 3.8e-9✱ · `్ర` 0.02✱ · `ృత` 3.5e-5✱ · `్రమ` 6.2e-6✱ · `ట్లు` 0.62 · `గ` 5.2e-3✱ · `్రమ` 1.4e-5✱ · `ా` 7.5e-4✱ |

</details>

[↑ meters](#meters)

---

<a id="vidyunmala"></a>

## 17. విద్యున్మాల (vidyunmala)

```text
Meter: విద్యున్మాల (vidyunmala), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 3 gaṇas: మ మ గా, i.e. UUU UUU UU (8 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 5th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter విద్యున్మాల (vidyunmala).

Meter: విద్యున్మాల (vidyunmala), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 3 gaṇas: మ మ గా, i.e. UUU UUU UU (8 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 5th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 83 tokens · 14.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మమ్యాముమ్యత్య్య్మమ్యుమ్యుమ్యుమ్ | `UUUUUUUU` |
| 2 | మమ్యా లంకన్ మమ్యుమ్యుమ్యుమ్ | `UUUUUUUU` |
| 3 | మ్యమ్యమ్యామమ్యమ్యమ్యమ్యుమ్ | `UUUUUUUU` |
| 4 | మ్యుమ్యమ్యమ్యా జ్య్యో మమ్యుమ్యుమ్ | `UUUUUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.089 · model's first choice kept 59% · constraint overrode 35% · backtracks 0

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.48 · `మ` 0.14 · `్యా` 9.7e-4✱ · `ము` 0.01 · `మ` 0.15 · `్య` 0.02✱ · `త` 5.5e-3✱ · `్య` 1.7e-4✱ · `్య` 6.9e-4✱ · `్` 9.1e-6✱ · `మ` 0.28 · `మ` 0.17 · `్య` 0.02✱ · `ు` 0.07 · `మ` 0.20 · `్య` 0.05✱ · `ు` 0.14 · `మ` 0.15 · `్య` 0.26 · `ు` 0.13✱ · `మ` 0.11✱ · `్` 4.9e-4✱ · `⏎` 0.57 |
| 2 | `మ` 0.82 · `మ` 0.89 · `్యా` 0.50 · `␣ల` 0.27 · `ంక` 0.58 · `న్` 0.24✱ · `␣మ` 0.09✱ · `మ` 0.27 · `్య` 0.05 · `ు` 0.41 · `మ` 0.94 · `్య` 0.94 · `ు` 0.89 · `మ` 0.95 · `్య` 0.98 · `ు` 0.98 · `మ` 0.99 · `్` 3.4e-6✱ · `⏎` 3.6e-4✱ forced |
| 3 | `మ` 0.98 · `్య` 0.95 · `మ` 0.02✱ · `్య` 0.01✱ · `మ` 0.85 · `్యా` 0.41 · `మ` 0.17 · `మ` 0.16✱ · `్య` 0.32 · `మ` 0.33 · `్య` 0.09✱ · `మ` 5.2e-3✱ · `్య` 0.03✱ · `మ` 0.86 · `్య` 0.66 · `ు` 0.51 · `మ` 0.95 · `్` 1.2e-6✱ · `⏎` 0.15✱ forced |
| 4 | `మ` 0.93 · `్య` 0.63 · `ు` 0.60 · `మ` 0.94 · `్య` 0.77 · `మ` 0.02✱ · `్య` 0.27✱ · `మ` 0.97 · `్యా` 0.89 · `␣జ` 0.98 · `్య` 1.1e-3✱ · `్య` 1.8e-4✱ · `ో` 3.7e-5✱ · `␣మ` 0.70 · `మ` 0.99 · `్య` 1.00 · `ు` 0.96 · `మ` 0.99 · `్య` 1.00 · `ు` 1.00 · `మ` 1.00 · `్` 2.1e-6✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 77 tokens · 11.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ్యమ్యగ్యమ్య్య్కల్యాముమ్యా | `UUUUUUUU` |
| 2 | ముమ్యమ్యమ్యగ్య్మ్యుక్యాన్ముమ్యా | `UUUUUUUU` |
| 3 | నమ్యమ్యల్యహ్యమ్య్యుమ్యాన్యుమ్ | `UUUUUUUU` |
| 4 | సమ్యమ్యల్యహ్య్య్జజ్య్యాన్యుమ్యా | `UUUUUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 0% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.076 · model's first choice kept 52% · constraint overrode 35% · backtracks 0

<details><summary>Token probabilities (77 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.08 · `మ` 0.13✱ · `్య` 4.7e-5✱ · `మ` 0.07✱ · `్య` 4.4e-4✱ · `గ` 0.02 · `్య` 6.6e-3✱ · `మ` 0.19 · `్య` 0.02✱ · `్య` 1.9e-3✱ · `్` 6.4e-5✱ · `క` 8.2e-3✱ · `ల` 0.03✱ · `్యా` 1.6e-3✱ · `ము` 0.01 · `మ` 0.06 · `్యా` 6.4e-3✱ · `⏎` 5.6e-3 forced |
| 2 | `ము` 0.35 · `మ` 1.5e-3✱ · `్య` 2.8e-4✱ · `మ` 0.79 · `్య` 0.79 · `మ` 0.95 · `్య` 0.94 · `గ` 0.73 · `్య` 0.74 · `్` 2.9e-3✱ · `మ` 0.24✱ · `్య` 0.34 · `ు` 0.05✱ · `క` 0.81 · `్యా` 6.0e-4✱ · `న్` 0.03✱ · `ము` 0.32 · `మ` 0.87 · `్యా` 0.52 · `⏎` 0.72 |
| 3 | `న` 0.37 · `మ` 0.89 · `్య` 0.79 · `మ` 0.88 · `్య` 0.88 · `ల` 0.03 · `్య` 0.56 · `హ` 1.9e-3 · `్య` 0.70 · `మ` 0.51 · `్య` 0.09✱ · `్య` 0.45 · `ు` 0.63 · `మ` 0.03 · `్యా` 0.16✱ · `న్` 0.94 · `యు` 0.07 · `మ` 0.95 · `్` 6.1e-7✱ · `⏎` 0.99 |
| 4 | `స` 0.99 · `మ` 1.00 · `్య` 0.98 · `మ` 1.00 · `్య` 0.99 · `ల` 0.98 · `్య` 0.94 · `హ` 0.92 · `్య` 0.90 · `్య` 3.9e-4✱ · `్` 1.8e-4✱ · `జ` 1.8e-3✱ · `జ` 0.07✱ · `్య` 3.0e-3✱ · `్యా` 0.58 · `న్` 0.85 · `యు` 0.91 · `మ` 0.93 · `్యా` 0.73 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 77 tokens · 32.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తక్రిత్యా మమ్య్య్తమ్రవ్యర్ శత్ | `UUUUUUUU` |
| 2 | తక్రిత్యా అమ్య్య్తత్రమ్యర్కడ్ | `UUUUUUUU` |
| 3 | తక్రిత్యా నిమ్య్య్తమ్రవ్యర్ మల్ | `UUUUUUUU` |
| 4 | తక్రిత్యా సమ్య్య్తమ్రవ్యర్ సే | `UUUUUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 0% · single-akshara words 27% · repeated lines 0 · mean token probability (geometric) 0.089 · model's first choice kept 68% · constraint overrode 21% · backtracks 30

<details><summary>Token probabilities (77 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.97 · `క` 0.98 · `్రి` 1.00 · `త` 0.91 · `్యా` 0.83 · `␣మ` 0.94 · `మ` 0.95 · `్య` 7.5e-6✱ · `్య` 1.3e-4✱ · `్` 6.5e-8✱ · `త` 1.4e-3✱ · `మ` 0.76 · `్ర` 0.72 · `వ` 0.79 · `్య` 1.5e-4✱ · `ర్` 2.0e-3 · `␣శ` 8.1e-4 · `త` 4.0e-3 · `్` 1.5e-7✱ · `⏎` 0.33✱ forced |
| 2 | `త` 1.00 · `క` 1.00 · `్రి` 1.00 · `త` 1.00 · `్యా` 0.98 · `␣అమ` 6.5e-4 · `్య` 9.2e-4✱ · `్య` 7.3e-3✱ · `్` 0.02✱ · `త` 8.7e-3✱ · `త` 0.89 · `్ర` 1.2e-3✱ · `మ` 3.8e-4 · `్య` 0.81 · `ర్` 0.86 · `క` 0.03 · `డ` 0.84 · `్` 9.8e-7✱ · `⏎` 3.1e-3✱ forced |
| 3 | `త` 0.70 · `క` 0.94 · `్రి` 0.74 · `త` 0.95 · `్యా` 0.66 · `␣ని` 0.03 · `మ` 0.95 · `్య` 0.98 · `్య` 0.86 · `్` 0.58 · `త` 0.87 · `మ` 0.95 · `్ర` 0.73 · `వ` 0.90 · `్య` 0.83 · `ర్` 0.87 · `␣మ` 0.25 · `ల` 0.09 · `్` 9.6e-8✱ · `⏎` 3.5e-4✱ forced |
| 4 | `త` 0.83 · `క` 0.94 · `్రి` 1.00 · `త` 0.99 · `్యా` 0.95 · `␣స` 0.91 · `మ` 0.92 · `్య` 0.75 · `్య` 0.95 · `్` 0.85 · `త` 0.96 · `మ` 0.99 · `్ర` 0.80 · `వ` 0.98 · `్య` 0.94 · `ర్` 0.98 · `␣స` 0.77 · `ే` 0.09 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 62 tokens · 31.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మశ్రీరా దుర్మారింగల్రొద్ | `UUUUUUUU` |
| 2 | డై శ్రీమా సీణ్య్య్లాకిండల్డెన్ | `UUUUUUUU` |
| 3 | మశ్రీరా లంక్యన్ వెళ్ళెడ్రన్ | `UUUUUUUU` |
| 4 | మశ్రీరా శత్ర్ర్నాన్నిజ్యడ్రన్ | `UUUUUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 0% · single-akshara words 10% · repeated lines 0 · mean token probability (geometric) 0.029 · model's first choice kept 53% · constraint overrode 35% · backtracks 30

<details><summary>Token probabilities (62 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.04 · `శ` 0.06 · `్రీ` 0.60 · `రా` 2.5e-3 · `␣దు` 1.0e-3✱ · `ర్మ` 0.02 · `ారి` 0.69 · `ంగ` 0.96 · `ల` 0.83 · `్ర` 2.6e-4✱ · `ొ` 0.88 · `ద` 0.02 · `్` 9.8e-8✱ · `⏎` 2.3e-4✱ forced |
| 2 | `డ` 0.92 · `ె` 0.86 · `ౖ` 2.7e-5✱ · `␣` 3.2e-4✱ · `శ` 8.2e-4✱ · `్రీ` 3.3e-3✱ · `మా` 7.4e-3 · `␣సీ` 0.13 · `ణ` 1.5e-3✱ · `్య` 0.01✱ · `్య` 2.0e-4✱ · `్లా` 5.0e-6✱ · `కి` 0.65 · `ండ` 0.84 · `ల్` 0.69 · `డ` 0.93 · `ె` 0.98 · `న్` 0.97 · `⏎` 0.98 |
| 3 | `మ` 1.00 · `శ` 0.99 · `్రీ` 1.00 · `రా` 0.99 · `␣ల` 0.99 · `ంక` 0.98 · `్య` 4.5e-5✱ · `న్` 6.2e-3✱ · `␣వె` 1.00 · `ళ్ళ` 0.99 · `ె` 0.99 · `డ` 1.00 · `్ర` 3.0e-5✱ · `న్` 0.03✱ · `⏎` 0.99 |
| 4 | `మ` 1.00 · `శ` 0.99 · `్రీ` 1.00 · `రా` 0.99 · `␣శ` 1.00 · `త్ర` 1.00 · `్ర` 8.4e-6✱ · `్` 1.5e-6✱ · `నాన్ని` 2.7e-6✱ · `జ` 2.0e-5✱ · `్య` 7.4e-4✱ · `డ` 1.00 · `్ర` 8.1e-4✱ · `న్` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 53 tokens · 7.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మమ్యాముమ్యామమ్యా లంకన్ | `UUUUUUUU` |
| 2 | మమ్యామమ్యామమ్యా మౌమ్యా | `UUUUUUUU` |
| 3 | మమ్యామమ్యామమ్యా సాగే | `UUUUUUUU` |
| 4 | మమ్యామమ్యామమ్యా మన్ జే | `UUUUUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 22% · repeated lines 0 · mean token probability (geometric) 0.259 · model's first choice kept 72% · constraint overrode 9% · backtracks 0

<details><summary>Token probabilities (53 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.48 · `మ` 0.14 · `్యా` 9.7e-4✱ · `ము` 0.01 · `మ` 0.15 · `్యా` 0.06✱ · `మ` 0.35 · `మ` 0.42 · `్యా` 0.14 · `␣ల` 0.09 · `ం` 0.29 · `క` 0.16 · `న్` 0.10 · `⏎` 4.7e-3✱ forced |
| 2 | `మ` 0.48 · `మ` 0.56 · `్యా` 0.82 · `మ` 0.82 · `మ` 0.95 · `్యా` 0.83 · `మ` 0.93 · `మ` 0.96 · `్యా` 0.67 · `␣మ` 0.20 · `ౌ` 0.09 · `మ` 0.19 · `్యా` 0.01✱ · `⏎` 0.83 |
| 3 | `మ` 0.99 · `మ` 0.99 · `్యా` 0.98 · `మ` 0.72 · `మ` 0.98 · `్యా` 0.94 · `మ` 0.98 · `మ` 0.97 · `్యా` 0.98 · `␣సా` 0.20 · `గే` 5.1e-3 · `⏎` 2.6e-3 forced |
| 4 | `మ` 0.03 · `మ` 0.45 · `్యా` 0.12✱ · `మ` 0.83 · `మ` 0.95 · `్యా` 0.59 · `మ` 0.86 · `మ` 0.85 · `్యా` 0.98 · `␣మ` 0.19 · `న్` 0.19 · `␣జ` 0.91 · `ే` 5.7e-4 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 73 tokens · 16.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నమ్రమ్యమ్రమ్య్య్నమ్రమ్యంలో | `UUUUUUUU` |
| 2 | కైమ్రమ్యమ్రమ్య్య్కమ్రమ్యంలో | `UUUUUUUU` |
| 3 | నమ్రమ్యమ్రమ్య్య్నన్రమ్యంలో | `UUUUUUUU` |
| 4 | మమ్ రమ్యమ్రమ్య్య్నమ్రమ్యుమ్యా | `UUUUUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 0% · single-akshara words 20% · repeated lines 0 · mean token probability (geometric) 0.081 · model's first choice kept 52% · constraint overrode 41% · backtracks 0

<details><summary>Token probabilities (73 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `న` 0.02 · `మ` 0.77 · `్ర` 0.05✱ · `మ` 0.10 · `్య` 5.4e-4✱ · `మ` 0.12✱ · `్ర` 5.0e-4✱ · `మ` 0.24 · `్య` 0.03✱ · `్య` 2.3e-3✱ · `్` 6.0e-5✱ · `న` 0.05✱ · `మ` 0.15 · `్ర` 6.9e-3✱ · `మ` 0.45 · `్యంలో` 2.9e-4 · `⏎` 6.3e-4✱ forced |
| 2 | `క` 0.26 · `ై` 2.7e-3✱ · `మ` 0.03✱ · `్` 2.3e-5✱ · `ర` 6.1e-3✱ · `మ` 0.97 · `్య` 0.94 · `మ` 0.98 · `్ర` 0.72 · `మ` 0.98 · `్య` 0.94 · `్య` 1.8e-4✱ · `్` 0.86 · `క` 8.8e-5✱ · `మ` 0.98 · `్ర` 0.76 · `మ` 0.99 · `్యంలో` 1.1e-3 · `⏎` 0.67 |
| 3 | `న` 0.69 · `మ` 0.82 · `్ర` 0.56 · `మ` 0.92 · `్య` 0.94 · `మ` 0.94 · `్ర` 0.18✱ · `మ` 0.97 · `్య` 0.55 · `్య` 0.82 · `్` 0.70 · `న` 0.90 · `న` 0.28 · `్ర` 8.7e-3✱ · `మ` 0.76 · `్యంలో` 5.9e-3✱ · `⏎` 0.17✱ forced |
| 4 | `మ` 0.02✱ · `మ` 0.11✱ · `్` 4.1e-3✱ · `␣ర` 5.4e-4✱ · `మ` 0.04✱ · `్య` 0.32✱ · `మ` 0.85 · `్ర` 0.11✱ · `మ` 0.96 · `్య` 0.72 · `్య` 0.83 · `్` 0.67 · `న` 0.63 · `మ` 0.73 · `్ర` 0.05✱ · `మ` 0.97 · `్య` 0.94 · `ు` 0.75 · `మ` 4.0e-3✱ · `్యా` 1.3e-3✱ |

</details>

[↑ meters](#meters)

---

<a id="lalita"></a>

## 18. లలిత (lalita)

```text
Meter: లలిత (lalita), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: త భ జ ర, i.e. UUI UII IUI UIU (12 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter లలిత (lalita).

Meter: లలిత (lalita), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 4 gaṇas: త భ జ ర, i.e. UUI UII IUI UIU (12 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 82 tokens · 22.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పళ్లమ్రునమ్మ మ మలార్ర్ర్వరవ్రిధించ్ | `UUIUIIIUIUIU` |
| 2 | కళ్లమ్రజిన్రు మమ లమ్య్య్కమించె మమ్ | `UUIUIIIUIUIU` |
| 3 | కళ్లమ్రు లోకము మతిక్వరమ్రయుమ్ | `UUIUIIIUIUIU` |
| 4 | తృళ్లాము మత్రుకము మత్యితం దుదున్ | `UUIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 14% · repeated lines 0 · mean token probability (geometric) 0.007 · model's first choice kept 27% · constraint overrode 57% · backtracks 0

<details><summary>Token probabilities (82 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.02 · `ళ్ల` 6.7e-4 · `మ` 0.07 · `్రు` 8.9e-5✱ · `న` 0.05 · `మ్మ` 0.01✱ · `␣మ` 0.11 · `␣మ` 0.06 · `ల` 0.03 · `ార` 7.1e-3 · `్ర` 7.1e-5✱ · `్ర` 1.5e-4✱ · `్వర` 1.3e-4✱ · `వ` 0.02✱ · `్రి` 2.0e-4✱ · `ధ` 6.2e-3✱ · `ించ` 8.5e-3✱ · `్` 2.7e-6✱ · `⏎` 0.69 |
| 2 | `క` 0.83 · `ళ` 0.02✱ · `్` 6.8e-6✱ · `ల` 0.04✱ · `మ` 0.16✱ · `్ర` 2.3e-3✱ · `జ` 0.03 · `ిన` 1.9e-3 · `్రు` 3.6e-4✱ · `␣మ` 0.05 · `మ` 0.07 · `␣ల` 0.07 · `మ` 0.09 · `్య` 3.6e-3✱ · `్య` 1.0e-4✱ · `్` 1.1e-6✱ · `క` 0.02✱ · `మ` 0.45 · `ించ` 0.21 · `ె` 0.04✱ · `␣మ` 0.01✱ · `మ` 0.30 · `్` 8.8e-6✱ · `⏎` 0.68 |
| 3 | `క` 0.19 · `ళ` 0.06✱ · `్` 1.3e-5✱ · `ల` 0.12✱ · `మ` 0.43 · `్రు` 2.6e-3✱ · `␣లో` 0.96 · `క` 0.96 · `ము` 0.86 · `␣మ` 0.03✱ · `తి` 0.09 · `క` 0.07✱ · `్వర` 8.6e-5✱ · `మ` 1.8e-3✱ · `్ర` 3.7e-5✱ · `యు` 0.95 · `మ` 6.4e-4✱ · `్` 5.1e-6✱ · `⏎` 0.61 |
| 4 | `త` 0.80 · `ృ` 0.78 · `ళ` 1.2e-4✱ · `్లా` 9.5e-6✱ · `ము` 0.28 · `␣మ` 0.83 · `త` 2.8e-3✱ · `్రు` 8.2e-6✱ · `క` 0.97 · `ము` 0.65 · `␣మ` 0.94 · `త` 0.14✱ · `్య` 1.6e-7✱ · `ిత` 6.2e-5✱ · `ం` 7.8e-3✱ · `␣` 0.02✱ · `దు` 3.9e-4✱ · `దు` 3.3e-3✱ · `న` 5.4e-4✱ · `్` 1.6e-5✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 79 tokens · 21.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కల్లిత్రునిద్రి కరుణవ్ర్ర్కనుమ్యమమ్ | `UUIUIIIUIUIU` |
| 2 | తల్లా మ ప్రేమ అమ మమ్య్య్తమాకకై | `UUIUIIIUIUIU` |
| 3 | నౌల్లా ము లోన మ మతిక్యతివ్రమన్ | `UUIUIIIUIUIU` |
| 4 | యే ల్లై ఉలుల్లలుకమున్ న్నినిశ్ లలల్ | `UUIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 29% · repeated lines 0 · mean token probability (geometric) 0.005 · model's first choice kept 19% · constraint overrode 70% · backtracks 0

<details><summary>Token probabilities (79 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.06 · `ల్లి` 0.08 · `త` 0.03✱ · `్రు` 3.8e-5✱ · `ని` 0.08 · `ద` 2.9e-3✱ · `్రి` 7.8e-4✱ · `␣క` 0.23 · `రుణ` 0.62 · `వ` 0.03 · `్ర` 1.1e-3✱ · `్ర` 1.9e-4✱ · `్` 2.1e-6✱ · `క` 2.1e-3✱ · `ను` 8.2e-3✱ · `మ` 0.01✱ · `్య` 3.3e-5✱ · `మ` 0.06✱ · `మ` 0.07✱ · `్` 1.7e-5✱ · `⏎` 0.09✱ forced |
| 2 | `త` 0.25 · `ల` 0.04✱ · `్లా` 1.9e-9✱ · `␣మ` 0.14 · `␣ప్రేమ` 0.08 · `␣అమ` 0.02 · `␣మ` 0.14 · `మ` 0.07 · `్య` 1.6e-3✱ · `్య` 1.2e-3✱ · `్` 5.9e-8✱ · `త` 5.4e-3✱ · `మా` 0.05 · `క` 0.43 · `క` 0.49 · `ై` 8.9e-3✱ · `⏎` 0.02✱ forced |
| 3 | `న` 0.65 · `ౌ` 0.02✱ · `ల` 0.03✱ · `్లా` 3.1e-7✱ · `␣ము` 0.07 · `␣లో` 0.98 · `న` 0.85 · `␣మ` 1.5e-3✱ · `␣మ` 0.46 · `తి` 0.61 · `క` 0.02✱ · `్య` 1.0e-4✱ · `తి` 0.50 · `వ` 3.4e-3✱ · `్రమ` 1.7e-5✱ · `న` 2.2e-3✱ · `్` 5.1e-6✱ · `⏎` 0.58 |
| 4 | `య` 0.61 · `ే` 8.1e-4✱ · `␣` 4.1e-4✱ · `ల్ల` 1.5e-3✱ · `ై` 1.1e-3✱ · `␣ఉ` 4.8e-4✱ · `లు` 2.4e-3✱ · `ల్ల` 6.2e-3✱ · `లు` 0.02✱ · `క` 0.06✱ · `ము` 0.13✱ · `న్` 0.03✱ · `␣` 4.6e-3✱ · `న్` 1.1e-3✱ · `న` 9.7e-4✱ · `ి` 2.7e-3✱ · `ని` 0.04✱ · `శ` 3.1e-3✱ · `్` 4.4e-4✱ · `␣ల` 0.03✱ · `ల` 0.01✱ · `ల` 1.8e-3✱ · `్` 2.4e-5✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 85 tokens · 44.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాజిత్యతమ్రి లన జస్రముక్యితుత్ | `UUIUIIIUIUIU` |
| 2 | స్రైజయ్రినప్పుడుజితమ్య్య్రలన్ర సుర్ | `UUIUIIIUIUIU` |
| 3 | క్క్యోజః జతక్రి రముడుగ్ర్యుతత్రి లల్ | `UUIUIIIUIUIU` |
| 4 | స్రైజజ్యుతైతనపు కోట్య్రముర్రితత్ | `UUIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.022 · model's first choice kept 42% · constraint overrode 53% · backtracks 30

<details><summary>Token probabilities (85 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.91 · `జ` 0.28 · `ిత` 0.99 · `్య` 0.99 · `త` 0.99 · `మ` 0.99 · `్రి` 1.00 · `␣ల` 0.87 · `న` 2.3e-3 · `␣జ` 0.98 · `స` 1.00 · `్ర` 0.95 · `ము` 0.94 · `క` 0.95 · `్య` 4.8e-8✱ · `ిత` 0.96 · `ు` 0.95 · `త` 0.70 · `్` 9.2e-5✱ · `⏎` 1.5e-3✱ forced |
| 2 | `స` 4.7e-3 · `్ర` 7.0e-5✱ · `ై` 0.03✱ · `జయ` 0.07✱ · `్రి` 6.4e-5✱ · `న` 1.0e-3✱ · `ప్పుడు` 5.1e-5✱ · `జ` 0.67 · `ిత` 0.76 · `మ` 1.4e-3✱ · `్య` 0.01✱ · `్య` 5.9e-4✱ · `్ర` 2.1e-3✱ · `ల` 0.12 · `న` 0.25✱ · `్ర` 7.0e-4✱ · `␣సు` 8.0e-3 · `ర` 0.83 · `్` 8.6e-8✱ · `⏎` 2.3e-3✱ forced |
| 3 | `క్క` 1.9e-3✱ · `్య` 7.3e-3✱ · `ో` 4.4e-3✱ · `జ` 1.4e-3✱ · `ః` 0.37 · `␣జ` 3.4e-3✱ · `త` 0.88 · `క` 0.81 · `్రి` 2.3e-4✱ · `␣ర` 4.8e-3✱ · `ము` 0.89 · `డు` 0.94 · `గ` 1.7e-3✱ · `్ర` 8.9e-5✱ · `్య` 6.9e-4✱ · `ు` 0.03✱ · `త` 0.22✱ · `త` 0.45 · `్రి` 0.14✱ · `␣ల` 0.19✱ · `ల` 0.66 · `్` 5.9e-7✱ · `⏎` 0.25✱ forced |
| 4 | `స` 0.79 · `్ర` 0.41 · `ై` 4.5e-4✱ · `జ` 3.3e-3✱ · `జ` 8.6e-3✱ · `్య` 0.01✱ · `ు` 0.93 · `త` 0.95 · `ై` 0.85 · `త` 0.11✱ · `న` 0.71 · `పు` 0.96 · `␣కో` 0.94 · `ట` 0.99 · `్య` 4.2e-6✱ · `్ర` 2.3e-4✱ · `ము` 0.03✱ · `ర` 3.7e-3✱ · `్ర` 2.8e-5✱ · `ిత` 0.95 · `త` 1.1e-3✱ · `్` 6.3e-4✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 74 tokens · 37.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాతిమ్పుదాక్షన ప్రముంత్ర నీల నల్ | `UUIUIIIUIUIU` |
| 2 | శౌతయ్రియమ్రుకమ రామ్య్య్శ జాయరా | `UUIUIIIUIUIU` |
| 3 | ప్రాతిప్రియమ్య ల లకుగ్వరత్రియత్ | `UUIUIIIUIUIU` |
| 4 | క్షేతైడెనుత్రమను క్షమ్య్య్శితప్యలో | `UUIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.008 · model's first choice kept 36% · constraint overrode 53% · backtracks 30

<details><summary>Token probabilities (74 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.97 · `తి` 0.76 · `మ్` 0.22 · `పు` 0.93 · `దా` 0.32 · `క్ష` 1.1e-3 · `న` 0.86 · `␣ప్ర` 1.4e-3 · `ము` 0.55 · `ంత` 7.5e-3 · `్ర` 0.07✱ · `␣నీ` 1.00 · `ల` 0.03 · `␣న` 0.03 · `ల` 0.96 · `్` 1.1e-7✱ · `⏎` 0.05✱ forced |
| 2 | `శ` 1.00 · `ౌ` 1.00 · `త` 1.5e-6✱ · `య` 0.02 · `్రియ` 7.4e-6✱ · `మ` 7.9e-3✱ · `్రు` 0.02✱ · `క` 0.98 · `మ` 3.5e-6✱ · `␣రా` 0.76 · `మ` 1.0e-2✱ · `్య` 8.3e-6✱ · `్య` 3.4e-5✱ · `్` 6.7e-9✱ · `శ` 0.02✱ · `␣జా` 7.7e-6 · `య` 0.92 · `రా` 0.02✱ · `⏎` 0.16✱ forced |
| 3 | `ప` 2.9e-3 · `్రా` 0.26 · `తి` 9.6e-3✱ · `ప` 0.02✱ · `్రియ` 0.79 · `మ` 0.03✱ · `్య` 7.5e-3✱ · `␣ల` 0.59 · `␣ల` 0.09✱ · `కు` 0.91 · `గ` 0.47 · `్వర` 1.5e-6✱ · `త` 9.9e-3✱ · `్రియ` 6.6e-6✱ · `త` 0.39 · `్` 2.7e-7✱ · `⏎` 0.12✱ forced |
| 4 | `క్ష` 0.88 · `ే` 1.7e-4✱ · `త` 0.01✱ · `ై` 0.02✱ · `డ` 0.69 · `ె` 0.49 · `ను` 0.31 · `త` 3.7e-3✱ · `్రమ` 1.5e-5✱ · `ను` 0.26 · `␣` 7.2e-3✱ · `క్ష` 0.94 · `మ` 0.98 · `్య` 3.0e-7✱ · `్య` 1.1e-3✱ · `్` 2.0e-5✱ · `శ` 0.01✱ · `ిత` 2.4e-5✱ · `ప` 0.10✱ · `్య` 3.9e-4✱ · `లో` 0.17✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 67 tokens · 16.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ్రిల్వరమ్రిక జయమ్ర్వ్క లంకలో | `UUIUIIIUIUIU` |
| 2 | కమ్రీబపుర్వరమ సీగ వేడగా | `UUIUIIIUIUIU` |
| 3 | కమ్రాల మాయ మ జుగగ్యనుడ్రగా | `UUIUIIIUIUIU` |
| 4 | కమ్రీల మాయ మ విడుత్ర్ర్కముల్లగా | `UUIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 21% · single-akshara words 14% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 39% · constraint overrode 46% · backtracks 0

<details><summary>Token probabilities (67 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.02 · `మ` 0.24 · `్రి` 1.8e-4✱ · `ల` 0.07 · `్వర` 5.7e-5✱ · `మ` 0.06✱ · `్రి` 2.8e-3✱ · `క` 0.04 · `␣జ` 0.02 · `య` 0.09 · `మ` 0.12✱ · `్ర` 4.5e-3✱ · `్వ` 5.1e-4✱ · `్` 1.0e-5✱ · `క` 0.04✱ · `␣ల` 0.17 · `ంక` 0.32 · `లో` 0.04✱ · `⏎` 0.93 |
| 2 | `క` 0.98 · `మ` 0.83 · `్రీ` 8.4e-5✱ · `బ` 0.02 · `పు` 0.04 · `ర` 0.02✱ · `్వర` 7.2e-6✱ · `మ` 0.22 · `␣సీ` 0.06 · `గ` 0.02✱ · `␣వే` 0.02 · `డ` 0.42 · `గా` 0.02✱ · `⏎` 0.97 |
| 3 | `క` 0.97 · `మ` 0.98 · `్రా` 8.2e-5✱ · `ల` 0.75 · `␣మ` 0.64 · `ాయ` 0.13 · `␣మ` 0.03 · `␣జ` 0.03 · `ు` 0.06 · `గ` 0.44 · `గ` 2.0e-4✱ · `్య` 3.6e-5✱ · `ను` 0.97 · `డ` 1.1e-3✱ · `్ర` 2.5e-5✱ · `గా` 2.4e-3✱ · `⏎` 0.99 |
| 4 | `క` 0.99 · `మ` 0.99 · `్రీ` 1.2e-5✱ · `ల` 1.00 · `␣మ` 0.99 · `ాయ` 1.00 · `␣మ` 0.87 · `␣వి` 5.6e-4✱ · `డు` 0.98 · `త` 2.2e-4✱ · `్ర` 1.0e-5✱ · `్ర` 2.4e-6✱ · `్` 3.7e-7✱ · `క` 0.01✱ · `ము` 2.0e-3✱ · `ల్ల` 4.4e-5✱ · `గా` 2.0e-4✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 80 tokens · 21.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నమ్రమ్య సక్రి లను మట్ర్య్న వేడుమా | `UUIUIIIUIUIU` |
| 2 | మమ్రమ్య సమ్రిమును మగ్య్ర్మ దాటినా | `UUIUIIIUIUIU` |
| 3 | సమ్రిమ్రిమున్రిమశనిన్త్య్జ జమ్యనుల్ | `UUIUIIIUIUIU` |
| 4 | నుమ్రమ్య లంజ ఛరణన్ ల్య్య్యు రీతితో | `UUIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 29% · constraint overrode 59% · backtracks 0

<details><summary>Token probabilities (80 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `న` 0.02 · `మ` 0.37 · `్ర` 0.05✱ · `మ` 0.06 · `్య` 3.0e-4✱ · `␣స` 0.02 · `క` 0.03✱ · `్రి` 3.2e-3✱ · `␣ల` 0.05 · `ను` 0.04 · `␣మ` 0.21 · `ట` 0.02✱ · `్ర` 1.5e-3✱ · `్య` 5.5e-5✱ · `్` 1.6e-7✱ · `న` 0.06✱ · `␣వే` 0.21 · `డు` 0.10 · `మా` 1.0e-4✱ · `⏎` 0.06 forced |
| 2 | `మ` 0.43 · `మ` 0.64 · `్ర` 0.02✱ · `మ` 0.29✱ · `్య` 0.36✱ · `␣స` 0.65 · `మ` 0.01✱ · `్రి` 2.5e-5✱ · `ము` 0.87 · `ను` 0.80 · `␣మ` 0.32 · `గ` 0.96 · `్య` 2.4e-4✱ · `్ర` 1.2e-4✱ · `్` 3.4e-8✱ · `మ` 0.01✱ · `␣దా` 0.11 · `టి` 0.52 · `నా` 0.07 · `⏎` 0.94 |
| 3 | `స` 0.12 · `మ` 0.77 · `్రి` 0.29 · `మ` 0.05✱ · `్రి` 2.1e-3✱ · `ము` 0.74 · `న` 0.02✱ · `్రి` 1.2e-6✱ · `మ` 7.3e-3✱ · `శ` 0.77 · `ని` 0.01✱ · `న్` 4.6e-5✱ · `త` 4.4e-3✱ · `్య` 4.1e-5✱ · `్` 3.5e-7✱ · `జ` 4.5e-3✱ · `␣జ` 0.02✱ · `మ` 0.39 · `్య` 0.03✱ · `ను` 0.01✱ · `ల్` 0.01 · `⏎` 0.06✱ forced |
| 4 | `ను` 0.86 · `మ` 0.74 · `్ర` 3.0e-3✱ · `మ` 0.89 · `్య` 0.61 · `␣ల` 0.74 · `ంజ` 4.7e-3✱ · `␣ఛ` 7.6e-4✱ · `రణ` 6.3e-3✱ · `న్` 0.02✱ · `␣ల` 2.1e-4✱ · `్య` 3.4e-3✱ · `్య` 8.0e-3✱ · `్య` 0.03✱ · `ు` 7.6e-3✱ · `␣రీ` 0.01✱ · `తి` 0.04✱ · `తో` 1.4e-4✱ |

</details>

[↑ meters](#meters)

---

<a id="kandamu"></a>

## 19. కందము (kandamu)

```text
Meter: కందము (kandamu), a jāti meter.
Lines (పాదాలు): 4.
Lines 1 and 3: 3 gaṇas (6 to 12 aksharas):
  gaṇa 1: భ (UII) or స (IIU) or నల (IIII) or గా (UU)
  gaṇa 2: భ (UII) or జ (IUI) or స (IIU) or నల (IIII) or గా (UU)
  gaṇa 3: భ (UII) or స (IIU) or నల (IIII) or గా (UU)
Lines 2 and 4: 5 gaṇas (11 to 19 aksharas):
  gaṇa 1: భ (UII) or జ (IUI) or స (IIU) or నల (IIII) or గా (UU)
  gaṇa 2: భ (UII) or స (IIU) or నల (IIII) or గా (UU)
  gaṇa 3: జ (IUI) or నల (IIII)
  gaṇa 4: భ (UII) or స (IIU) or నల (IIII) or గా (UU)
  gaṇa 5: స (IIU) or గా (UU)
The 1st akshara of every line has the same weight: all guru or all laghu.
Yati (యతి): in lines 2 and 4 the 1st akshara must be in yati-maitri with the first akshara of gaṇa 4.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter కందము (kandamu).

Meter: కందము (kandamu), a jāti meter.
Lines (పాదాలు): 4.
Lines 1 and 3: 3 gaṇas (6 to 12 aksharas):
  gaṇa 1: భ (UII) or స (IIU) or నల (IIII) or గా (UU)
  gaṇa 2: భ (UII) or జ (IUI) or స (IIU) or నల (IIII) or గా (UU)
  gaṇa 3: భ (UII) or స (IIU) or నల (IIII) or గా (UU)
Lines 2 and 4: 5 gaṇas (11 to 19 aksharas):
  gaṇa 1: భ (UII) or జ (IUI) or స (IIU) or నల (IIII) or గా (UU)
  gaṇa 2: భ (UII) or స (IIU) or నల (IIII) or గా (UU)
  gaṇa 3: జ (IUI) or నల (IIII)
  gaṇa 4: భ (UII) or స (IIU) or నల (IIII) or గా (UU)
  gaṇa 5: స (IIU) or గా (UU)
The 1st akshara of every line has the same weight: all guru or all laghu.
Yati (యతి): in lines 2 and 4 the 1st akshara must be in yati-maitri with the first akshara of gaṇa 4.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 66 tokens · 11.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | దేతిలమలముమమ సతత | `UIIIIIIIIII` |
| 2 | మౌతముకాని మరుపను నిమల్లుముకకనున్ | `UIIUIIIIIIUIIIIU` |
| 3 | మేతమమమ సమ జమమతి | `UIIIIIIIIII` |
| 4 | నీతి మమ మనికత మక మ మృదుతము ట్టి ప్రతిత్ | `UIIIIIIIIIIIIIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.029 · model's first choice kept 33% · constraint overrode 35% · backtracks 0

<details><summary>Token probabilities (66 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `దే` 0.04 · `తి` 0.01 · `ల` 0.03 · `మ` 0.05 · `ల` 0.03 · `ము` 0.05 · `మ` 0.07 · `మ` 0.07✱ · `␣స` 5.9e-3✱ · `త` 0.06 · `త` 0.07 · `⏎` 0.42 forced |
| 2 | `మ` 0.26 · `ౌ` 0.01✱ · `త` 4.9e-3✱ · `ము` 0.51 · `క` 0.04 · `ాని` 1.7e-3 · `␣మ` 0.09 · `రు` 0.04 · `ప` 0.01 · `ను` 0.03 · `␣ని` 9.0e-3 · `మ` 0.06✱ · `ల్లు` 6.4e-4✱ · `ము` 0.02✱ · `క` 5.9e-3✱ · `క` 0.10✱ · `ను` 0.02✱ · `న` 0.02✱ · `్` 4.6e-6✱ · `⏎` 0.46 |
| 3 | `మ` 0.20 · `ే` 7.1e-3✱ · `త` 0.11✱ · `మ` 0.28 · `మ` 0.22 · `మ` 0.22 · `␣స` 0.02 · `మ` 0.15 · `␣జ` 5.1e-3 · `మ` 0.10✱ · `మ` 0.15✱ · `తి` 0.32 · `⏎` 0.77 |
| 4 | `నీ` 0.15 · `తి` 0.09✱ · `␣మ` 0.13 · `మ` 0.30 · `␣మ` 0.08 · `ని` 0.02 · `క` 0.08 · `త` 0.03 · `␣మ` 0.12 · `క` 0.06 · `␣మ` 0.12 · `␣మ` 0.11 · `ృ` 1.1e-3✱ · `దు` 0.27 · `త` 0.07 · `ము` 1.00 · `␣` 1.8e-3✱ · `ట్టి` 6.7e-4✱ · `␣ప్రతి` 7.8e-5✱ · `త` 1.8e-5✱ · `్` 3.0e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 64 tokens · 15.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాల్లితగత వే మేటి త | `UIIIIUUII` |
| 2 | కల్లేనిగ పామల మ త ళ్ర్ర్కమ నామముయమ్ | `UUIIUIIIIIIUIIU` |
| 3 | మల్లి మలక గొప్పత మమ | `UIIIIUIIII` |
| 4 | ల్లోల్ లేదు అదే జగము ల్లలు తితి నునుతనే | `UUIIUIIIIIIIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 24% · single-akshara words 24% · repeated lines 0 · mean token probability (geometric) 0.007 · model's first choice kept 14% · constraint overrode 59% · backtracks 0

<details><summary>Token probabilities (64 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.10 · `ల్లి` 0.33 · `త` 0.04 · `గ` 6.2e-3 · `త` 0.03 · `␣వే` 6.6e-3 · `␣మే` 5.5e-3 · `టి` 0.01✱ · `␣` 6.3e-3✱ · `త` 0.04✱ · `⏎` 0.01✱ forced |
| 2 | `క` 0.11 · `ల్` 0.04✱ · `లే` 0.01✱ · `ని` 0.13 · `గ` 0.01 · `␣పా` 1.2e-3 · `మ` 0.03 · `ల` 0.03 · `␣మ` 0.06 · `␣త` 6.4e-3 · `␣` 4.8e-3✱ · `ళ` 0.02✱ · `్ర` 4.7e-3✱ · `్ర` 3.8e-4✱ · `్` 3.0e-5✱ · `క` 0.02✱ · `మ` 0.11✱ · `␣` 8.9e-3✱ · `నా` 6.9e-4✱ · `మ` 0.05✱ · `ము` 0.16✱ · `య` 1.4e-3✱ · `మ` 0.07 · `్` 4.5e-6✱ · `⏎` 0.26 |
| 3 | `మ` 0.19 · `ల్లి` 0.01✱ · `␣మ` 0.01✱ · `ల` 0.04 · `క` 0.05 · `␣గొప్ప` 0.04 · `త` 0.12 · `␣మ` 5.5e-3✱ · `మ` 0.65 · `⏎` 0.14✱ forced |
| 4 | `ల్లో` 1.2e-3 · `ల` 5.0e-4✱ · `్` 1.6e-10✱ · `␣లేదు` 0.91 · `␣అదే` 3.4e-4✱ · `␣జగ` 0.02✱ · `ము` 0.72 · `␣` 1.2e-3✱ · `ల్ల` 3.3e-5✱ · `లు` 9.5e-4✱ · `␣` 6.5e-3✱ · `తి` 6.6e-4✱ · `తి` 1.9e-3✱ · `␣` 8.4e-4✱ · `ను` 7.5e-5✱ · `ను` 5.4e-3✱ · `త` 1.2e-3✱ · `నే` 4.3e-3✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 66 tokens · 41.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నమ నరి వందుల హత్తు మ | `IIIIUIIUII` |
| 2 | సముగరత జడు జయ వాయ ల్య్య్శణిము షమశమస్ | `IIIIIIIIIUIIIIIIIU` |
| 3 | నమ రీతిడామ జగసస | `IIUIUIIIII` |
| 4 | మమన సుగపు లంకకు చెరిమససోమె తవార్ | `IIIIIIUIIIIIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 37% · single-akshara words 5% · repeated lines 0 · mean token probability (geometric) 0.025 · model's first choice kept 44% · constraint overrode 30% · backtracks 30

<details><summary>Token probabilities (66 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `న` 0.69 · `మ` 0.96 · `␣న` 0.03 · `రి` 0.01 · `␣వ` 0.48 · `ందు` 2.7e-3 · `ల` 0.08 · `␣హ` 0.69 · `త్తు` 8.7e-5 · `␣మ` 0.36 · `⏎` 0.80 forced |
| 2 | `స` 0.97 · `ము` 0.23 · `గ` 0.86 · `ర` 0.84 · `త` 3.5e-3 · `␣జ` 0.05 · `డు` 0.04 · `␣జ` 0.83 · `య` 0.94 · `␣వ` 0.69 · `ాయ` 0.94 · `␣ల` 0.99 · `్య` 4.8e-7✱ · `్య` 2.0e-3✱ · `్` 4.8e-8✱ · `శ` 2.0e-3✱ · `ణి` 0.98 · `ము` 7.6e-3✱ · `␣ష` 2.4e-3 · `మ` 0.10 · `శ` 4.9e-3 · `మ` 0.25 · `స` 5.7e-4 · `్` 4.0e-7✱ · `⏎` 0.19 forced |
| 3 | `న` 0.28 · `మ` 0.47 · `␣రీ` 1.3e-3 · `తి` 0.05✱ · `డా` 2.1e-4 · `మ` 0.02 · `␣జగ` 9.8e-3✱ · `స` 0.21✱ · `స` 0.02✱ · `⏎` 0.18 |
| 4 | `మ` 0.51 · `మ` 0.36 · `న` 0.03 · `␣సు` 7.4e-4✱ · `గ` 0.95 · `పు` 0.95 · `␣ల` 0.96 · `ంక` 0.95 · `కు` 0.95 · `␣చె` 1.2e-3✱ · `రి` 0.97 · `మ` 4.6e-4✱ · `స` 1.0e-3✱ · `స` 2.0e-3✱ · `ో` 7.4e-3✱ · `మె` 1.2e-3✱ · `␣` 3.8e-3✱ · `త` 2.4e-3✱ · `వ` 0.91 · `ార్` 6.8e-4✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 75 tokens · 43.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | దమ ల శ సీత దె నిపుడుపు | `IIIIUIIIIII` |
| 2 | సమ యద్రన సల జల నల మ్క్య్సడముముశ మ రా | `IIUIIIIIIIIIIIIIIU` |
| 3 | డు ము లకు వేటటనౌన స | `IIIIUIIUII` |
| 4 | ద్రము సల జల నల మ్క్య్సడము ట్టితత నాకుపులుక్ | `IIIIIIIIIIIIIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 31% · single-akshara words 31% · repeated lines 0 · mean token probability (geometric) 0.069 · model's first choice kept 61% · constraint overrode 31% · backtracks 30

<details><summary>Token probabilities (75 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ద` 7.0e-3 · `మ` 0.64 · `␣ల` 0.67 · `␣శ` 0.84 · `␣సీ` 0.96 · `త` 0.84 · `␣ద` 0.58 · `ె` 0.35✱ · `␣ని` 0.19 · `పు` 0.82 · `డు` 9.2e-3 · `పు` 6.5e-3 · `⏎` 0.94 |
| 2 | `స` 0.91 · `మ` 0.55 · `␣య` 3.8e-3 · `ద్ర` 0.09 · `న` 0.41 · `␣స` 0.11 · `ల` 0.82 · `␣జ` 0.95 · `ల` 0.92 · `␣న` 0.90 · `ల` 0.94 · `␣మ` 0.96 · `్` 4.6e-3✱ · `క` 0.83 · `్య` 4.9e-6✱ · `్` 9.2e-7✱ · `స` 1.2e-4✱ · `డ` 8.8e-4✱ · `ము` 0.51 · `ము` 4.8e-4✱ · `శ` 0.98 · `␣మ` 3.1e-4✱ · `␣రా` 0.98 · `⏎` 4.7e-5✱ forced |
| 3 | `డు` 0.82 · `␣` 3.8e-3✱ · `ము` 1.3e-3✱ · `␣ల` 0.31 · `కు` 0.72 · `␣వే` 0.74 · `ట` 0.47 · `ట` 2.8e-3✱ · `న` 0.89 · `ౌ` 0.88 · `న` 0.84 · `␣స` 0.72 · `⏎` 2.2e-3✱ forced |
| 4 | `ద్ర` 0.97 · `ము` 1.9e-3✱ · `␣స` 0.91 · `ల` 0.96 · `␣జ` 0.98 · `ల` 0.98 · `␣న` 0.94 · `ల` 0.99 · `␣మ` 0.99 · `్` 0.99 · `క` 0.99 · `్య` 0.99 · `్` 0.98 · `స` 0.79 · `డ` 0.98 · `ము` 0.96 · `␣` 3.4e-4✱ · `ట్టి` 1.7e-4✱ · `త` 2.1e-4✱ · `త` 4.4e-4✱ · `␣నాకు` 1.9e-3✱ · `పు` 5.0e-4✱ · `లు` 2.5e-3✱ · `క` 0.02✱ · `్` 6.9e-7✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 80 tokens · 16.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నమ్రమ సుర సమునముతన | `UIIIIIIIIII` |
| 2 | మమ్రికమయ మగ మమత ల ల్య్య్మ శ్రమ సుర సమున్ | `UIIIIIIIIIIIIIIIIU` |
| 3 | తొమ్ర మ్రికమయ మగ మమత | `UIIIIIIIIII` |
| 4 | సో మ్రేయసుకుకునుదితిక స్రున జజనుమతున్ | `UUIIIIIIIIIIIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 37% · single-akshara words 16% · repeated lines 0 · mean token probability (geometric) 0.034 · model's first choice kept 39% · constraint overrode 46% · backtracks 0

<details><summary>Token probabilities (80 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `న` 0.02 · `మ` 0.47 · `్ర` 0.08✱ · `మ` 0.18 · `␣సు` 0.05 · `ర` 0.27 · `␣స` 0.08 · `ము` 0.54 · `న` 0.10 · `ము` 0.09✱ · `త` 0.01✱ · `న` 0.24 · `⏎` 0.75 |
| 2 | `మ` 0.45 · `మ` 0.61 · `్రి` 4.2e-5✱ · `క` 0.19 · `మ` 0.07 · `య` 0.05 · `␣మ` 0.23 · `గ` 0.04 · `␣మ` 0.03 · `మ` 0.03✱ · `త` 0.30 · `␣ల` 0.16 · `␣ల` 0.07 · `్య` 1.4e-4✱ · `్య` 2.5e-4✱ · `్` 2.2e-4✱ · `మ` 0.09✱ · `␣శ` 6.2e-3 · `్ర` 0.36 · `మ` 0.77 · `␣సు` 0.88 · `ర` 0.84 · `␣స` 0.69 · `ము` 0.76 · `న్` 0.01 · `⏎` 0.01✱ forced |
| 3 | `త` 0.68 · `ొ` 2.9e-4✱ · `మ` 1.7e-3✱ · `్ర` 3.8e-4✱ · `␣మ` 0.55 · `్రి` 0.52 · `క` 0.96 · `మ` 0.95 · `య` 0.92 · `␣మ` 0.85 · `గ` 0.78 · `␣మ` 0.76 · `మ` 0.89 · `త` 0.83 · `⏎` 0.05✱ forced |
| 4 | `␣` 0.22✱ · `స` 1.5e-4✱ · `ో` 0.01✱ · `␣` 5.9e-4✱ · `మ` 3.0e-4✱ · `్` 5.8e-4✱ · `రే` 2.8e-4✱ · `య` 5.1e-3✱ · `సు` 5.5e-3✱ · `కు` 2.5e-3✱ · `కు` 7.5e-3✱ · `ను` 6.0e-3✱ · `ది` 5.3e-4✱ · `తి` 8.5e-4✱ · `క` 4.1e-3✱ · `␣` 3.6e-4✱ · `స్` 3.5e-3✱ · `రు` 0.02✱ · `న` 7.5e-3✱ · `␣` 0.02✱ · `జ` 0.27✱ · `జ` 0.87 · `ను` 0.82 · `మ` 1.5e-3✱ · `తు` 0.99 · `న్` 1.4e-4✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 67 tokens · 11.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మమగ శ జ శౌమ నమ నమ | `IIIIIUIIIII` |
| 2 | మమగ శ ల య ల మ ల మ శ స ల్య్మమగ శ జ శఔ | `IIIIIIIIIIIIIIIIIIU` |
| 3 | నమ నమ నమమమమమ శౌ | `IIIIIIIIIIU` |
| 4 | నమ నమ నమముతనము మమ ణనవానానే | `IIIIIIIIIIIIIIUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 24% · single-akshara words 48% · repeated lines 0 · mean token probability (geometric) 0.063 · model's first choice kept 51% · constraint overrode 22% · backtracks 0

<details><summary>Token probabilities (67 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.62 · `మ` 0.23 · `గ` 0.02 · `␣శ` 0.05 · `␣జ` 0.03 · `␣శ` 0.02 · `ౌ` 0.02 · `మ` 0.03 · `␣న` 0.17 · `మ` 0.05 · `␣న` 0.03 · `మ` 0.16 · `⏎` 0.24 |
| 2 | `మ` 0.76 · `మ` 0.63 · `గ` 0.04 · `␣శ` 0.05 · `␣ల` 0.10 · `␣య` 0.07 · `␣ల` 0.13 · `␣మ` 0.05 · `␣ల` 0.15 · `␣మ` 0.05 · `␣శ` 0.03 · `␣స` 0.02 · `␣ల` 0.12 · `్య` 3.9e-5✱ · `్` 1.2e-4✱ · `మ` 0.49 · `మ` 0.85 · `గ` 0.70 · `␣శ` 0.83 · `␣జ` 0.87 · `␣శ` 0.93 · `ఔ` 6.7e-4✱ · `⏎` 1.1e-3 forced |
| 3 | `న` 0.73 · `మ` 0.79 · `␣న` 0.72 · `మ` 0.80 · `␣న` 0.10✱ · `మ` 0.82 · `మ` 0.40 · `మ` 0.40 · `మ` 0.15 · `మ` 0.24 · `␣శ` 0.51 · `ౌ` 0.45 · `⏎` 0.33 forced |
| 4 | `న` 0.81 · `మ` 0.86 · `␣న` 0.46 · `మ` 0.82 · `␣న` 0.23 · `మ` 0.23 · `ము` 0.44 · `త` 4.8e-5✱ · `న` 3.4e-3✱ · `ము` 0.12✱ · `␣మ` 3.7e-3✱ · `మ` 0.02✱ · `␣` 1.3e-3✱ · `ణ` 5.9e-6✱ · `న` 1.5e-3✱ · `వా` 2.4e-3✱ · `నా` 8.6e-3✱ · `నే` 2.7e-3✱ |

</details>

[↑ meters](#meters)

---

<a id="utsahamu"></a>

## 20. ఉత్సాహము (utsahamu)

```text
Meter: ఉత్సాహము (utsahamu), a jāti meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas (15 to 22 aksharas):
  gaṇa 1: న (III) or హ (UI)
  gaṇa 2: న (III) or హ (UI)
  gaṇa 3: న (III) or హ (UI)
  gaṇa 4: న (III) or హ (UI)
  gaṇa 5: న (III) or హ (UI)
  gaṇa 6: న (III) or హ (UI)
  gaṇa 7: న (III) or హ (UI)
  gaṇa 8: గురువు (U)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 5.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter ఉత్సాహము (utsahamu).

Meter: ఉత్సాహము (utsahamu), a jāti meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas (15 to 22 aksharas):
  gaṇa 1: న (III) or హ (UI)
  gaṇa 2: న (III) or హ (UI)
  gaṇa 3: న (III) or హ (UI)
  gaṇa 4: న (III) or హ (UI)
  gaṇa 5: న (III) or హ (UI)
  gaṇa 6: న (III) or హ (UI)
  gaṇa 7: న (III) or హ (UI)
  gaṇa 8: గురువు (U)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 5.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 94 tokens · 12.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సమమ సిమము లంకకు జత జపము వేమెనన్ససన్ | `IIIIIIUIIIIIIIUIUIU` |
| 2 | సమమ సీహము శతరు శ జ జన జముమెనసతససాన్ | `IIIUIIIIIIIIIIIIIIIIU` |
| 3 | సమమ సీమము శతము జల జముము మముతలన్ల సన్ | `IIIUIIIIIIIIIIIIIUIU` |
| 4 | సమమ సీమత శర జ జల జము జ జము సన ససముగ్ | `IIIUIIIIIIIIIIIIIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 53% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.057 · model's first choice kept 49% · constraint overrode 16% · backtracks 0

<details><summary>Token probabilities (94 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 0.02 · `మ` 0.17 · `మ` 0.02 · `␣సి` 3.3e-3 · `మ` 0.02 · `ము` 0.08 · `␣ల` 0.04 · `ంక` 0.16 · `కు` 0.15 · `␣జ` 0.06 · `త` 7.7e-3 · `␣జ` 0.05✱ · `ప` 0.09 · `ము` 0.06 · `␣వే` 0.12 · `మ` 4.5e-3✱ · `ె` 7.2e-3✱ · `న` 0.05 · `న్` 0.01✱ · `స` 0.30✱ · `స` 0.22 · `న` 0.02 · `్` 1.3e-6✱ · `⏎` 0.60 |
| 2 | `స` 0.61 · `మ` 0.83 · `మ` 0.34 · `␣సీ` 0.09 · `హ` 0.01 · `ము` 0.42 · `␣శ` 0.07✱ · `త` 0.16 · `రు` 8.6e-3✱ · `␣శ` 0.05 · `␣జ` 0.13 · `␣జన` 3.2e-3 · `␣జ` 0.08 · `ము` 0.16 · `మె` 5.2e-3✱ · `న` 0.11 · `స` 0.03 · `త` 3.2e-3 · `స` 0.33 · `సా` 8.9e-3 · `న` 0.20 · `్` 0.24✱ · `⏎` 0.86 |
| 3 | `స` 0.85 · `మ` 0.94 · `మ` 0.70 · `␣సీ` 0.30 · `మ` 0.29 · `ము` 0.59 · `␣శ` 0.05 · `త` 0.13 · `ము` 0.13 · `␣జ` 0.18 · `ల` 0.05 · `␣జ` 0.50 · `ము` 0.28 · `ము` 0.14 · `␣మ` 0.02 · `ము` 0.04 · `త` 0.03 · `ల` 0.01 · `న్` 0.04 · `ల` 3.7e-3 · `␣స` 0.04 · `న` 0.21✱ · `్` 1.8e-4✱ · `⏎` 0.75 |
| 4 | `స` 0.81 · `మ` 0.92 · `మ` 0.59 · `␣సీ` 0.64 · `మ` 0.22 · `త` 0.03 · `␣శ` 0.12 · `ర` 0.01 · `␣జ` 0.07 · `␣జ` 0.13 · `ల` 0.11 · `␣జ` 0.27 · `ము` 0.30 · `␣జ` 0.06 · `␣జ` 0.03 · `ము` 0.05 · `␣స` 0.21 · `న` 0.20 · `␣స` 0.03 · `స` 2.3e-3✱ · `ము` 2.0e-3✱ · `గ` 0.75 · `్` 1.7e-8✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 105 tokens · 12.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కంజ మనడు జగ శ జగము న్ర్వ్కన్న్కనం కమలి మనజ్ | `UIIIIIIIIIIUIUIIIIU` |
| 2 | జంజ న్ర్వ్కన్న్కనం కమలి మజజ జ జగ శము ననవమ్ | `UIUIUIIIIIIIIIIIIIU` |
| 3 | జంజజనకనం కమలి మజజ మ జగ లము నక లక్ | `UIIIIUIIIIIIIIIIIIIU` |
| 4 | కంజ మనడు జగ శ జగము న్ర్వ్కన్న్కనం లవవలలల్ | `UIIIIIIIIIIUIUIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 26% · single-akshara words 16% · repeated lines 0 · mean token probability (geometric) 0.077 · model's first choice kept 56% · constraint overrode 23% · backtracks 0

<details><summary>Token probabilities (105 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.04 · `ంజ` 0.03 · `␣మ` 0.04 · `న` 0.02 · `డు` 5.4e-3 · `␣జ` 0.16 · `గ` 0.03 · `␣శ` 7.7e-3 · `␣జగ` 1.1e-3 · `ము` 0.04 · `␣న` 0.13 · `్ర` 4.3e-5✱ · `్వ` 1.4e-4✱ · `్` 5.5e-6✱ · `క` 0.03✱ · `న్` 0.04 · `న్` 0.06 · `క` 0.14 · `నం` 1.0e-3✱ · `␣క` 3.1e-3✱ · `మ` 0.75 · `లి` 4.0e-3 · `␣మ` 0.59 · `న` 0.57 · `జ` 0.03✱ · `్` 2.3e-6✱ · `⏎` 2.1e-4✱ forced |
| 2 | `జ` 0.08 · `ం` 1.7e-3✱ · `జ` 9.6e-3✱ · `␣న` 0.97 · `్ర` 0.96 · `్వ` 0.93 · `్` 0.94 · `క` 0.96 · `న్` 0.96 · `న్` 0.98 · `క` 0.95 · `నం` 0.99 · `␣క` 0.70 · `మ` 0.92 · `లి` 0.78 · `␣మ` 0.84 · `జ` 2.2e-3✱ · `జ` 0.85 · `␣జ` 0.13 · `␣జ` 0.59 · `గ` 0.77 · `␣శ` 0.46 · `ము` 0.11 · `␣న` 0.02 · `న` 0.04✱ · `వ` 0.01✱ · `మ` 0.03✱ · `్` 1.7e-3✱ · `⏎` 0.36 |
| 3 | `జ` 0.10 · `ంజ` 0.68 · `జ` 0.39 · `న` 0.17 · `క` 0.46 · `నం` 0.29 · `␣క` 0.54 · `మ` 0.73 · `లి` 0.50 · `␣మ` 0.43 · `జ` 0.38 · `జ` 0.40 · `␣మ` 0.05 · `␣జ` 0.18 · `గ` 0.19 · `␣ల` 0.09 · `ము` 0.11 · `␣న` 0.07 · `క` 0.03 · `␣ల` 0.28 · `క` 0.25 · `్` 9.0e-9✱ · `⏎` 0.99 |
| 4 | `క` 0.98 · `ంజ` 0.99 · `␣మ` 0.99 · `న` 0.98 · `డు` 0.97 · `␣జ` 0.98 · `గ` 0.99 · `␣శ` 0.89 · `␣జగ` 0.84 · `ము` 0.98 · `␣న` 0.95 · `్ర` 0.83 · `్వ` 0.83 · `్` 0.68 · `క` 0.95 · `న్` 0.97 · `న్` 0.87 · `క` 0.92 · `నం` 0.96 · `␣ల` 9.6e-5✱ · `వ` 1.9e-3✱ · `వ` 3.3e-4✱ · `ల` 1.6e-3✱ · `ల` 8.6e-3✱ · `ల` 0.04✱ · `్` 2.6e-4✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 104 tokens · 39.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి మనము మనుడ లోక శ్ర్న్త మతి వంటితల్లి మవ్ | `UIIIIIIIUIIIIUIUIU` |
| 2 | జాల్లు జగతి నా మవ మ మ మ్వ్వ్జతను మనుడ లోక శ్రే | `UIIIIUIIIIIIIIIIUIU` |
| 3 | మల్ల మత మ మనము మనుడ మక శ్ర శన మతి మతినగ్ | `UIIIIIIIIIIIIIIIIIIIU` |
| 4 | కల్ల ఉత్సహముగ జాతి ప్య్య్గాలలోలు అడిగినగ్ | `UIUIIIIUIUIUIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 39% · single-akshara words 24% · repeated lines 0 · mean token probability (geometric) 0.032 · model's first choice kept 61% · constraint overrode 33% · backtracks 30

<details><summary>Token probabilities (104 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.93 · `ల్లి` 0.94 · `␣మ` 0.96 · `న` 0.33 · `ము` 0.50 · `␣మ` 0.92 · `ను` 0.22 · `డ` 0.83 · `␣లో` 0.37 · `క` 0.05 · `␣శ` 0.96 · `్ర` 0.86 · `్` 0.70 · `న` 0.03 · `్` 5.3e-4✱ · `త` 0.03✱ · `␣మ` 0.85 · `తి` 0.92 · `␣వంటి` 2.6e-5✱ · `త` 0.97 · `ల్లి` 0.88 · `␣మ` 0.55 · `వ` 0.90 · `్` 4.6e-9✱ · `⏎` 2.6e-5✱ forced |
| 2 | `జ` 0.85 · `ాల` 0.88 · `్` 2.8e-9✱ · `లు` 2.1e-3✱ · `␣జగ` 0.90 · `తి` 0.71 · `␣నా` 5.0e-4 · `␣మ` 0.22 · `వ` 4.6e-3 · `␣మ` 0.91 · `␣మ` 0.95 · `␣మ` 0.95 · `్వ` 9.8e-6✱ · `్వ` 5.8e-5✱ · `్` 2.0e-5✱ · `జ` 2.8e-3✱ · `త` 0.17 · `ను` 0.06 · `␣మ` 0.56 · `ను` 0.70 · `డ` 0.58 · `␣లో` 0.68 · `క` 0.73 · `␣శ` 0.51 · `్ర` 0.19✱ · `ే` 0.90 · `⏎` 2.2e-3✱ forced |
| 3 | `మ` 0.54 · `ల` 1.5e-4✱ · `్` 1.8e-10✱ · `ల` 0.29 · `␣మ` 0.44 · `త` 0.44 · `␣మ` 2.1e-3✱ · `␣మ` 0.91 · `న` 0.84 · `ము` 0.79 · `␣మ` 0.82 · `ను` 0.90 · `డ` 0.86 · `␣మ` 2.2e-3✱ · `క` 0.76 · `␣శ` 0.72 · `్ర` 0.33 · `␣శ` 0.03✱ · `న` 0.92 · `␣మ` 0.59 · `తి` 0.36 · `␣మ` 0.69 · `తి` 0.53 · `న` 5.9e-3✱ · `గ` 0.02✱ · `్` 6.7e-6✱ · `⏎` 7.5e-3✱ forced |
| 4 | `క` 0.52 · `ల` 0.01✱ · `్` 9.6e-7✱ · `ల` 0.24 · `␣ఉ` 0.79 · `త్` 0.63 · `స` 3.4e-5✱ · `హ` 0.97 · `ము` 0.96 · `గ` 4.4e-3✱ · `␣జా` 0.95 · `తి` 1.00 · `␣ప` 0.99 · `్య` 1.7e-6✱ · `్` 2.8e-4✱ · `య` 1.2e-5✱ · `్` 6.9e-8✱ · `గ` 4.2e-5✱ · `ాలలో` 0.98 · `లు` 1.5e-4✱ · `␣అ` 0.99 · `డి` 0.99 · `గిన` 0.99 · `గ` 1.5e-4✱ · `్` 9.3e-7✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 111 tokens · 53.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | చం మనడు జగ శ శముడ యు య్య్ర్జ మధు ర నెతి మలఫ ప్రచ్ | `UIIIIIIIIIIIIIIIIIIIU` |
| 2 | నొంము దము పచు విమల ల ల ల్యు మల యైచమ మనడుజ్ | `UIIIIIIIIIIIIIUIIIIU` |
| 3 | శీం మె మమ తల చెతి సు మల ల్య్య్జినడు జగ జగ శముడమ్ | `UIIIIIIIIIIIIIIIIIIIU` |
| 4 | తొం మ సు మల లన్క్షమండి ప్ర్క్దో గణస నిషాన్ని రీ | `UIIIIUIUIUIIIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 26% · single-akshara words 40% · repeated lines 0 · mean token probability (geometric) 0.016 · model's first choice kept 44% · constraint overrode 48% · backtracks 30

<details><summary>Token probabilities (111 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `చ` 9.1e-3 · `ం` 0.06 · `␣మ` 0.72 · `న` 0.37 · `డు` 0.91 · `␣జ` 0.78 · `గ` 0.89 · `␣శ` 0.28 · `␣శ` 0.03 · `ము` 0.72 · `డ` 4.5e-4 · `␣యు` 0.65 · `␣య` 0.86 · `్య` 0.03 · `్ర` 0.05✱ · `్` 6.3e-6✱ · `జ` 0.05✱ · `␣మ` 0.02✱ · `ధు` 2.5e-3✱ · `␣ర` 0.03 · `␣నె` 3.0e-4 · `తి` 6.6e-4✱ · `␣మ` 0.41 · `ల` 0.59 · `ఫ` 1.1e-7✱ · `␣ప్ర` 6.0e-4✱ · `చ` 0.41 · `్` 4.3e-8✱ · `⏎` 1.4e-3✱ forced |
| 2 | `న` 0.72 · `ొ` 1.1e-3✱ · `ం` 4.1e-4✱ · `ము` 0.04✱ · `␣ద` 0.06 · `ము` 0.28 · `␣ప` 1.6e-3✱ · `చు` 0.95 · `␣వి` 0.97 · `మ` 0.98 · `ల` 0.99 · `␣ల` 0.96 · `␣ల` 2.0e-3✱ · `␣ల` 0.02✱ · `్య` 5.5e-4✱ · `ు` 3.9e-3✱ · `␣మ` 0.95 · `ల` 0.95 · `␣య` 2.9e-3✱ · `ై` 8.9e-4✱ · `చ` 0.82 · `మ` 1.3e-3✱ · `␣మ` 0.75 · `న` 0.90 · `డు` 0.65 · `జ` 8.0e-3✱ · `్` 1.5e-7✱ · `⏎` 5.7e-4✱ forced |
| 3 | `శ` 0.81 · `ీ` 1.3e-3✱ · `ం` 1.1e-4✱ · `␣మె` 1.3e-3✱ · `␣మ` 0.94 · `మ` 0.89 · `␣త` 0.85 · `ల` 0.53 · `␣చె` 1.1e-4✱ · `తి` 0.99 · `␣సు` 1.00 · `␣మ` 0.87 · `ల` 0.95 · `␣ల` 5.5e-3✱ · `్య` 2.3e-4✱ · `్య` 3.4e-4✱ · `్` 2.7e-6✱ · `జ` 5.5e-3✱ · `ిన` 3.3e-4✱ · `డు` 1.00 · `␣జ` 0.99 · `గ` 0.99 · `␣జగ` 6.7e-4✱ · `␣శ` 0.93 · `ము` 0.96 · `డ` 0.95 · `మ` 2.7e-3✱ · `్` 5.0e-5✱ · `⏎` 7.9e-3✱ forced |
| 4 | `త` 0.81 · `ొ` 2.7e-4✱ · `ం` 4.3e-5✱ · `␣మ` 6.3e-5✱ · `␣సు` 0.96 · `␣మ` 0.98 · `ల` 0.99 · `␣ల` 4.3e-4✱ · `న్` 3.2e-3✱ · `క్ష` 0.51 · `మ` 0.51 · `ండి` 0.05✱ · `␣ప` 3.5e-4✱ · `్ర` 4.0e-5✱ · `్` 5.9e-7✱ · `క` 1.2e-4✱ · `్` 8.2e-7✱ · `ద` 4.9e-4✱ · `ో` 4.5e-4✱ · `␣గణ` 1.00 · `స` 0.99 · `␣ని` 1.6e-5✱ · `ష` 0.97 · `ాన్ని` 1.00 · `␣రీ` 1.6e-3✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 95 tokens · 24.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మరియు మలయ పలకల జల స్ర్ర్మముమమయు మ మలలమమ్ | `IIIIIIIIIIIIIIIIIIIIIU` |
| 2 | నరమ మమను దాటి లను ల శ్ర్ర్య జమమమమ మమమమన్ | `IIIIIIUIIIIIIIIIIIIIU` |
| 3 | మరి ల లకను చేరెను సముమముముము మె మమమునుతో | `IIIIIIUIIIIIIIIIIIIIU` |
| 4 | వరుదు లేదు లేదు లేదు హ్య్ల్వ మము లేదు లేదు లే | `IIIUIUIUIIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 35% · single-akshara words 23% · repeated lines 0 · mean token probability (geometric) 0.035 · model's first choice kept 34% · constraint overrode 48% · backtracks 0

<details><summary>Token probabilities (95 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.57 · `రి` 0.03 · `యు` 0.08 · `␣మ` 0.23 · `ల` 0.07 · `య` 0.63 · `␣ప` 0.09 · `ల` 0.05 · `క` 0.44 · `ల` 0.25 · `␣జ` 0.03 · `ల` 0.15 · `␣స` 0.05✱ · `్ర` 2.4e-3✱ · `్ర` 1.2e-5✱ · `్` 1.4e-7✱ · `మ` 0.12✱ · `ము` 0.46 · `మ` 0.38 · `మ` 0.67 · `యు` 0.27 · `␣మ` 0.19 · `␣మ` 0.39 · `ల` 0.21 · `ల` 0.07 · `మ` 0.07✱ · `మ` 0.14 · `్` 2.9e-6✱ · `⏎` 0.11✱ forced |
| 2 | `న` 0.03 · `ర` 0.04✱ · `మ` 0.18 · `␣మ` 0.04 · `మ` 0.06 · `ను` 0.06 · `␣దా` 0.03 · `టి` 0.63 · `␣ల` 0.08 · `ను` 0.08 · `␣ల` 0.10 · `␣శ` 4.1e-3✱ · `్ర` 1.2e-3✱ · `్ర` 2.7e-4✱ · `్` 5.7e-4✱ · `య` 1.0e-2✱ · `␣జ` 0.02 · `మ` 0.17 · `మ` 0.28 · `మ` 0.12 · `మ` 0.12 · `␣మ` 0.07✱ · `మ` 0.23✱ · `మ` 0.76 · `మ` 0.55 · `న్` 4.2e-3✱ · `⏎` 0.48 |
| 3 | `మ` 0.78 · `రి` 0.02✱ · `␣ల` 0.98 · `␣ల` 0.03✱ · `క` 0.97 · `ను` 0.96 · `␣చే` 0.99 · `రె` 0.03✱ · `ను` 0.99 · `␣స` 0.68 · `ము` 0.09✱ · `మ` 0.01✱ · `ము` 0.01✱ · `ము` 0.05✱ · `ము` 0.07✱ · `␣మె` 0.01✱ · `␣మ` 0.03✱ · `మ` 0.20 · `ము` 0.01✱ · `ను` 3.8e-4✱ · `తో` 5.0e-4✱ · `⏎` 0.41 |
| 4 | `వ` 0.02✱ · `రు` 0.01✱ · `దు` 0.02✱ · `␣లేదు` 4.2e-3✱ · `␣లేదు` 0.07✱ · `␣లేదు` 0.01✱ · `␣హ` 0.05✱ · `్య` 1.6e-3✱ · `్` 3.5e-3✱ · `ల` 2.2e-4✱ · `్` 9.2e-6✱ · `వ` 2.9e-4✱ · `␣మ` 0.03✱ · `ము` 0.02✱ · `␣లేదు` 0.34 · `␣లేదు` 0.19✱ · `␣లే` 0.01✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 94 tokens · 17.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాము జయము పకటి లంక న్వ్ర వె వెడును సమయ జితే | `UIIIIIIIUIIIIIIIIIIU` |
| 2 | సీ మతన్ రడపు గడెను జ జీ జయము సముద్ర నీ | `UIUIIIIIIIUIIIIUIU` |
| 3 | టై మల జయటను లముల జ జ్య్య్డ మతను రడపు గడెలా | `UIIIIIIIIIIIIIIIIIIIU` |
| 4 | వామమావన గమనిక ఇ ప అడిగిన ఉఉత్సహో | `UIUIIIIIIIIIIIIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 30% · single-akshara words 33% · repeated lines 0 · mean token probability (geometric) 0.049 · model's first choice kept 46% · constraint overrode 33% · backtracks 0

<details><summary>Token probabilities (94 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.35 · `ము` 0.07 · `␣జ` 0.04 · `య` 0.19 · `ము` 0.22 · `␣ప` 0.01 · `క` 0.03 · `టి` 0.04 · `␣ల` 0.06 · `ం` 0.12 · `క` 0.33 · `␣న` 0.04✱ · `్వ` 2.6e-4✱ · `్ర` 9.0e-4✱ · `␣వె` 0.20 · `␣వె` 1.0e-3✱ · `డు` 3.8e-3✱ · `ను` 0.94 · `␣` 1.9e-3✱ · `స` 1.9e-3✱ · `మ` 0.86 · `య` 0.12 · `␣జ` 0.18 · `ితే` 0.02 · `⏎` 3.6e-4✱ forced |
| 2 | `␣సీ` 0.53 · `␣మ` 4.3e-3✱ · `త` 0.29 · `న్` 0.08 · `␣ర` 0.07✱ · `డ` 0.06 · `పు` 0.07 · `␣గ` 0.03 · `డ` 0.98 · `ె` 0.92 · `ను` 0.88 · `␣జ` 0.03✱ · `␣జ` 3.5e-3✱ · `ీ` 3.9e-3✱ · `␣జ` 0.88 · `య` 0.84 · `ము` 0.85 · `␣స` 0.89 · `ము` 0.99 · `ద్ర` 0.94 · `␣నీ` 1.9e-3 · `⏎` 6.5e-4✱ forced |
| 3 | `ట` 0.04✱ · `ై` 2.2e-3✱ · `␣మ` 0.06✱ · `ల` 0.12 · `␣జ` 0.09 · `య` 0.25 · `ట` 0.02 · `ను` 0.04 · `␣ల` 0.06 · `ము` 0.08 · `ల` 0.03 · `␣జ` 0.04 · `␣జ` 0.60 · `్య` 3.8e-3✱ · `్య` 1.6e-3✱ · `్` 4.7e-7✱ · `డ` 3.4e-4✱ · `␣మ` 0.99 · `త` 0.99 · `ను` 1.1e-3✱ · `␣ర` 0.89 · `డ` 0.97 · `పు` 0.97 · `␣గ` 0.86 · `డ` 0.97 · `ె` 0.92 · `లా` 7.0e-4 · `⏎` 0.67 |
| 4 | `వా` 9.7e-3✱ · `మ` 0.02✱ · `మా` 6.0e-3✱ · `వ` 0.48 · `న` 0.05✱ · `␣గ` 0.98 · `మని` 0.99 · `క` 0.98 · `␣ఇ` 1.3e-4✱ · `␣ప` 7.0e-4✱ · `␣అ` 0.94 · `డి` 0.97 · `గిన` 0.91 · `␣ఉ` 2.0e-4✱ · `ఉ` 0.97 · `త్` 0.82 · `స` 1.6e-4✱ · `హ` 1.00 · `ో` 6.6e-7✱ |

</details>

[↑ meters](#meters)

---

<a id="taruvoja"></a>

## 21. తరువోజ (taruvoja)

```text
Meter: తరువోజ (taruvoja), a jāti meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas (22 to 30 aksharas):
  gaṇa 1: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 2: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 3: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 4: న (III) or హ (UI)
  gaṇa 5: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 6: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 7: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 8: న (III) or హ (UI)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 3 and of gaṇa 5 and of gaṇa 7.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter తరువోజ (taruvoja).

Meter: తరువోజ (taruvoja), a jāti meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas (22 to 30 aksharas):
  gaṇa 1: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 2: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 3: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 4: న (III) or హ (UI)
  gaṇa 5: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 6: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 7: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 8: న (III) or హ (UI)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 3 and of gaṇa 5 and of gaṇa 7.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 152 tokens · 25.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తతిలమలము నిలమ్మ్ర్తమపనక మక మ్ర్వ్తమమ లైకమతమ మ్ర్వ్తమకతరతమ | `IIIIIIIUIIIIIIIIIIUIIIIIIIIIII` |
| 2 | తతిలకలమలీల మ్ర్వ్తమనననునమతకము మతిమలతతమ ప్రేమ తమత | `IIIIIIUIIIIIIIIIIIIIIIIIIUIIII` |
| 3 | తితి ప్రేమ ప్రేమమున్ర్య్తీల మతి మతి ల్య్య్తితితి మతి మతి మతి మతి మతి మతి | `IIUIUIUUIIIIIIIIIIIIIIIIIIII` |
| 4 | తితితితితిగమనిక్ర్ర్దినతతరురువ వ్వ్య్తే ణ సగణలతో ప్న్ర్తీయ ఈ సగణ | `IIIIIIIUIIIIIIIUIIIIIUUIUIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 37% · single-akshara words 10% · repeated lines 0 · mean token probability (geometric) 0.020 · model's first choice kept 40% · constraint overrode 42% · backtracks 0

<details><summary>Token probabilities (152 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.18 · `తి` 0.02 · `ల` 0.07 · `మ` 0.03 · `ల` 0.04 · `ము` 0.03 · `␣ని` 0.01 · `ల` 0.03 · `మ్మ` 4.9e-3 · `్ర` 1.7e-4✱ · `్` 8.4e-8✱ · `త` 0.03✱ · `మ` 0.23 · `ప` 8.2e-3 · `న` 0.06 · `క` 0.04✱ · `␣మ` 0.05✱ · `క` 0.09 · `␣మ` 0.01✱ · `్ర` 1.7e-3✱ · `్వ` 7.0e-5✱ · `్` 2.2e-5✱ · `త` 0.16 · `మ` 0.07✱ · `మ` 0.08 · `␣ల` 3.1e-3✱ · `ై` 3.2e-3✱ · `క` 0.04✱ · `మ` 0.11 · `త` 0.05 · `మ` 0.12 · `␣మ` 0.04 · `్ర` 2.6e-4✱ · `్వ` 3.6e-4✱ · `్` 0.02✱ · `త` 0.75 · `మ` 0.11✱ · `క` 0.06✱ · `తర` 2.6e-3 · `త` 0.21 · `మ` 0.13 · `⏎` 0.25 forced |
| 2 | `త` 0.27 · `తి` 0.41 · `ల` 0.16 · `క` 0.02 · `ల` 0.12 · `మ` 0.13 · `ల` 0.06 · `ీల` 9.9e-4 · `␣మ` 0.14 · `్ర` 3.1e-3✱ · `్వ` 0.01✱ · `్` 0.60 · `త` 0.84 · `మ` 0.63 · `న` 0.05 · `న` 0.07 · `ను` 0.03 · `న` 0.06 · `మ` 0.09 · `త` 0.04✱ · `క` 0.03 · `ము` 0.23 · `␣మ` 0.21✱ · `తి` 0.08✱ · `మ` 0.11 · `ల` 0.06✱ · `త` 0.24 · `త` 0.19 · `మ` 0.21 · `␣ప్రేమ` 2.0e-3 · `␣త` 9.3e-3 · `మ` 0.10✱ · `త` 0.09✱ · `⏎` 0.17✱ forced |
| 3 | `తి` 0.40 · `తి` 0.01✱ · `␣ప్రేమ` 0.10 · `␣ప్రేమ` 0.94 · `ము` 0.94 · `న` 0.01✱ · `్ర` 2.1e-6✱ · `్య` 1.5e-4✱ · `్` 3.6e-6✱ · `త` 0.03✱ · `ీల` 5.4e-3✱ · `␣మ` 0.82 · `తి` 0.76 · `␣మ` 0.79 · `తి` 0.79 · `␣ల` 0.70 · `్య` 2.8e-5✱ · `్య` 1.1e-3✱ · `్` 2.2e-6✱ · `తి` 0.01✱ · `తి` 0.86 · `తి` 0.03✱ · `␣మ` 0.61 · `తి` 0.84 · `␣మ` 0.76 · `తి` 0.87 · `␣మ` 0.73 · `తి` 0.84 · `␣మ` 0.58 · `తి` 0.74 · `␣మ` 0.47 · `తి` 0.73 · `␣మ` 0.66 · `తి` 0.74 · `⏎` 3.2e-3✱ forced |
| 4 | `తి` 0.91 · `తి` 0.02✱ · `తి` 0.85 · `తి` 0.06✱ · `తి` 4.4e-4✱ · `గ` 0.98 · `మని` 1.00 · `క` 1.00 · `్ర` 5.0e-9✱ · `్ర` 3.5e-7✱ · `్` 3.9e-8✱ · `ది` 0.02✱ · `న` 0.85 · `త` 1.1e-4✱ · `త` 0.70 · `రు` 0.69 · `రు` 0.29 · `వ` 8.1e-3✱ · `␣వ` 2.8e-4✱ · `్వ` 8.6e-4✱ · `్య` 2.4e-9✱ · `్` 5.0e-6✱ · `త` 6.8e-5✱ · `ే` 4.7e-4✱ · `␣` 0.94 · `ణ` 3.1e-4✱ · `␣స` 0.96 · `గ` 0.90 · `ణ` 0.97 · `లతో` 4.9e-3✱ · `␣ప` 1.5e-4✱ · `్` 4.8e-4✱ · `న` 0.01✱ · `్ర` 5.7e-7✱ · `్` 4.0e-6✱ · `త` 0.03✱ · `ీయ` 6.9e-4✱ · `␣ఈ` 0.98 · `␣స` 0.99 · `గ` 0.95 · `ణ` 1.00 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 155 tokens · 35.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మామలగత వేటి మకకు ద కాడె మముక కటిమి లొనన్య్య్మనుల స్తువవము | `UIIIIUIIIIIUIIIIIIIIUIIIIIII` |
| 2 | జోమెప నిలమమ మ్ర్ర్జొనననల మను మ్య్య్సొమ్మమ్మ మమతి మమ్య్య్జో స్తువనము వె | `UIIIIIIIIIIIIIUUIIIIUUIIIII` |
| 3 | మీ మమసర్వవ గ్క్ర్మిగినతతరువు వ్ర్ర్మినమాలనులను పాప్య్య్మినతతరువుజ | `UIIUIIIIIIIIIIIUIIIIUIIIIIII` |
| 4 | నీ మమత మమత మృతి మమత మమతృమతి మమతిముగా ఇను ఇతైన మపు | `UIIIIIIIIIIIIIIIIIIIIUIIIUIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 21% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.018 · model's first choice kept 35% · constraint overrode 51% · backtracks 0

<details><summary>Token probabilities (155 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.11 · `మ` 0.18 · `ల` 0.07 · `గ` 5.2e-3 · `త` 0.02 · `␣వే` 5.2e-3 · `టి` 0.01 · `␣మ` 0.15 · `క` 0.04 · `కు` 4.3e-3 · `␣ద` 0.01 · `␣కా` 1.3e-3 · `డ` 0.02✱ · `ె` 0.01 · `␣మ` 0.07✱ · `ము` 0.01 · `క` 0.05 · `␣క` 0.01✱ · `టి` 0.02 · `మి` 3.2e-4✱ · `␣ల` 0.01✱ · `ొ` 0.03✱ · `న` 0.08 · `న` 0.03✱ · `్య` 4.3e-7✱ · `్య` 2.3e-4✱ · `్` 1.3e-5✱ · `మ` 0.07✱ · `ను` 0.02✱ · `ల` 8.2e-3✱ · `␣` 7.6e-3✱ · `స్తు` 0.03✱ · `వ` 0.01 · `వ` 0.02✱ · `ము` 0.03✱ · `⏎` 0.50 |
| 2 | `జ` 0.10 · `ో` 4.8e-3✱ · `మె` 6.4e-4✱ · `ప` 0.19 · `␣ని` 0.02 · `ల` 0.06 · `మ` 0.04 · `మ` 0.03 · `␣మ` 0.06 · `్ర` 1.1e-3✱ · `్ర` 4.8e-5✱ · `్` 3.1e-6✱ · `జ` 0.03✱ · `ొ` 0.01✱ · `న` 0.14 · `న` 0.11 · `న` 0.03✱ · `ల` 0.04✱ · `␣మ` 0.14✱ · `ను` 0.02 · `␣మ` 0.02✱ · `్య` 3.7e-4✱ · `్య` 7.6e-3✱ · `్` 1.1e-3✱ · `స` 7.9e-3✱ · `ొ` 7.4e-3✱ · `మ్మ` 0.26 · `మ్మ` 0.28 · `␣మ` 0.04✱ · `మ` 0.83 · `తి` 0.53 · `␣మ` 0.01✱ · `మ` 0.93 · `్య` 2.4e-3✱ · `్య` 5.7e-5✱ · `్` 7.7e-7✱ · `జ` 9.8e-3✱ · `ో` 2.9e-3✱ · `␣` 0.46 · `స్తు` 0.82 · `వ` 0.51 · `న` 0.61 · `ము` 0.44 · `␣వె` 0.71 · `⏎` 2.9e-4✱ forced |
| 3 | `␣మ` 6.0e-4✱ · `ీ` 3.5e-3✱ · `␣మ` 2.1e-3✱ · `మ` 0.02✱ · `స` 0.78 · `ర్` 0.73 · `వ` 0.92 · `వ` 0.10 · `␣గ` 0.94 · `్` 1.2e-8✱ · `క` 0.76 · `్ర` 1.1e-7✱ · `్` 1.6e-6✱ · `మ` 2.9e-6✱ · `ి` 5.5e-5✱ · `గ` 0.99 · `ిన` 0.99 · `త` 7.0e-4✱ · `త` 0.91 · `రు` 0.91 · `వు` 0.10✱ · `␣వ` 0.11✱ · `్ర` 9.9e-5✱ · `్ర` 1.8e-4✱ · `్` 3.6e-4✱ · `మ` 7.3e-3✱ · `ిన` 5.4e-4✱ · `మ` 0.88 · `ాలను` 0.47 · `లను` 0.05✱ · `␣పా` 0.74 · `ప` 2.2e-3✱ · `్య` 1.7e-4✱ · `్య` 0.76 · `్` 4.3e-4✱ · `మ` 3.1e-3✱ · `ిన` 1.1e-6✱ · `త` 9.2e-3✱ · `త` 0.94 · `రు` 0.98 · `వు` 0.09✱ · `జ` 0.78 · `⏎` 0.03✱ forced |
| 4 | `న` 0.04✱ · `ీ` 2.4e-3✱ · `␣మ` 0.06✱ · `మ` 0.33 · `త` 0.18 · `␣మ` 0.22✱ · `మ` 0.21✱ · `త` 0.04✱ · `␣మ` 0.25 · `ృతి` 1.4e-4✱ · `␣మ` 0.33 · `మ` 0.27 · `త` 0.43 · `␣మ` 0.32 · `మ` 0.56 · `త` 0.71 · `ృ` 2.1e-4✱ · `మ` 0.98 · `తి` 0.93 · `␣మ` 1.00 · `మ` 0.99 · `తి` 0.97 · `ము` 0.99 · `గా` 5.0e-5✱ · `␣ఇ` 2.9e-3✱ · `ను` 8.5e-4✱ · `␣ఇ` 0.81 · `త` 0.99 · `ైన` 1.00 · `␣మ` 1.2e-4✱ · `పు` 0.99 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 152 tokens · 34.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కలమ అమలలను మ్ర్ర్క ల లగల ము ము హ్య్య్గాంపగతి దిశయ్యు ల్ర్మ్క కతి మతి మతి | `IIIIIIIIIIIIIIIUIIIIUIIIIIIII` |
| 2 | తిల మతి మతి మతి మ్య్య్దేమతి మతి మతి మతి మతి మతి మతి హ మతి మతి మ | `IIIIIIIIUIIIIIIIIIIIIIIIIIIII` |
| 3 | ములు మతి మమతి మమ్యు మమ మతి మతి ములు హ మతి మతి మములు మతితితితి | `IIIIIIIUIIIIIIIIIIIIIIIIIIIIII` |
| 4 | తిల మతి మతి మతి మ్య్య్దేమతి మతితి మ్ర్ర్తితితి మతి హ హమమ్య్య్తితితితి ల ల ల | `IIIIIIIIUIIIIIIIIIIIIUIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 52% · single-akshara words 22% · repeated lines 0 · mean token probability (geometric) 0.108 · model's first choice kept 63% · constraint overrode 26% · backtracks 30

<details><summary>Token probabilities (152 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.91 · `ల` 0.06 · `మ` 0.08 · `␣అమ` 4.5e-3 · `ల` 0.05 · `ల` 0.01 · `ను` 0.45 · `␣మ` 0.07 · `్ర` 3.2e-5✱ · `్ర` 2.0e-5✱ · `్` 7.1e-6✱ · `క` 0.10✱ · `␣ల` 0.07 · `␣ల` 0.13 · `గల` 3.2e-4 · `␣ము` 3.8e-3 · `␣మ` 0.40 · `ు` 0.05 · `␣హ` 0.63 · `్య` 0.94 · `్య` 0.61 · `్` 1.8e-5✱ · `గా` 2.9e-3✱ · `ంప` 6.0e-5 · `గ` 0.03 · `తి` 0.83 · `␣ది` 0.95 · `శ` 0.99 · `య్య` 0.99 · `ు` 1.00 · `␣` 9.7e-5✱ · `ల` 0.01✱ · `్ర` 3.0e-5✱ · `్` 1.8e-3✱ · `మ` 0.25 · `్` 1.5e-5✱ · `క` 2.5e-3✱ · `␣క` 4.1e-3 · `తి` 0.69 · `␣మ` 0.79 · `తి` 0.83 · `␣మ` 0.76 · `తి` 0.83 · `⏎` 9.8e-3✱ forced |
| 2 | `తి` 0.94 · `ల` 1.7e-3✱ · `␣మ` 0.73 · `తి` 0.83 · `␣మ` 0.82 · `తి` 0.91 · `␣మ` 0.83 · `తి` 0.91 · `␣మ` 0.80 · `్య` 6.2e-5✱ · `్య` 0.03✱ · `్` 1.4e-3✱ · `దే` 1.4e-4✱ · `మ` 0.77 · `తి` 0.72 · `␣మ` 0.92 · `తి` 0.88 · `␣మ` 0.93 · `తి` 0.91 · `␣మ` 0.91 · `తి` 0.91 · `␣మ` 0.79 · `తి` 0.80 · `␣మ` 0.79 · `తి` 0.77 · `␣మ` 0.77 · `తి` 0.78 · `␣హ` 0.77 · `␣మ` 0.48 · `తి` 0.83 · `␣మ` 0.83 · `తి` 0.90 · `␣మ` 0.88 · `⏎` 2.8e-3✱ forced |
| 3 | `␣మ` 0.75 · `ులు` 9.5e-4✱ · `␣మ` 0.52 · `తి` 0.73 · `␣మ` 0.04✱ · `మ` 0.58 · `తి` 0.60 · `␣మ` 0.76 · `మ` 0.04✱ · `్య` 4.3e-3✱ · `ు` 0.05✱ · `␣మ` 0.88 · `మ` 0.13 · `␣మ` 0.90 · `తి` 0.87 · `␣మ` 0.92 · `తి` 0.90 · `␣మ` 0.96 · `ులు` 1.2e-3✱ · `␣హ` 0.86 · `␣మ` 0.88 · `తి` 0.62 · `␣మ` 0.93 · `తి` 0.82 · `␣మ` 0.93 · `మ` 0.02✱ · `ులు` 8.8e-4✱ · `␣మ` 0.40 · `తి` 0.58 · `తి` 0.42 · `తి` 0.33✱ · `తి` 0.02✱ · `⏎` 0.39 |
| 4 | `తి` 0.60 · `ల` 0.02✱ · `␣మ` 0.77 · `తి` 0.69 · `␣మ` 0.65 · `తి` 0.72 · `␣మ` 0.69 · `తి` 0.62 · `␣మ` 0.62 · `్య` 1.2e-4✱ · `్య` 0.32 · `్` 0.02✱ · `దే` 0.71 · `మ` 0.43 · `తి` 0.38 · `␣మ` 0.41 · `తి` 0.42 · `తి` 0.37 · `␣మ` 0.38 · `్ర` 8.0e-5✱ · `్ర` 0.11✱ · `్` 0.02✱ · `తి` 0.52 · `తి` 0.28 · `తి` 0.76 · `␣మ` 0.72 · `తి` 0.75 · `␣హ` 0.64 · `␣హ` 0.30✱ · `మ` 5.4e-3✱ · `మ` 0.89 · `్య` 9.3e-4✱ · `్య` 0.09✱ · `్` 2.4e-4✱ · `తి` 0.91 · `తి` 0.97 · `తి` 0.96 · `తి` 0.51 · `␣ల` 0.84 · `␣ల` 0.67 · `␣ల` 0.65 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 150 tokens · 57.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మరి సీము సర్ తీగె మడల జలధిని మటిని లంకకను చేర్య్య్మామమరి మన | `IIUIUUIIIIIIIIIIIUIIIUUIIIII` |
| 2 | మ రని దాటి మడలమశలేమను జుమమాడి హనుతుతుడు వ్ర్ర్మౌమామమరి మ | `IIIUIIIIIIUIIIIUIIIIIIUUIIII` |
| 3 | సి రిగె మడల జలధ్వ్వ్శిన లకనును మ మ్మ్ర్జినయతి ప్రాససస్య్య్యీ హ హమమమ | `IIIIIIIUIIIIIIIIIIIUIUUIIIII` |
| 4 | మ రననలలలధిధ్ర్ర్మటిటిని లంక మ మమ జ జంపాణ హ్య్య్మంతుడు మమర | `IIIIIIIUIIIIUIIIIIUUIUIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 22% · single-akshara words 24% · repeated lines 0 · mean token probability (geometric) 0.041 · model's first choice kept 59% · constraint overrode 39% · backtracks 30

<details><summary>Token probabilities (150 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.92 · `రి` 0.68 · `␣సీ` 0.68 · `ము` 0.73 · `␣సర్` 2.6e-4 · `␣తీ` 1.4e-3 · `గ` 0.91 · `ె` 0.99 · `␣మ` 0.97 · `డ` 0.88 · `ల` 0.94 · `␣జ` 0.99 · `ల` 0.99 · `ధి` 0.98 · `ని` 0.89 · `␣మ` 0.03✱ · `టి` 0.72 · `ని` 0.04 · `␣ల` 0.73 · `ంక` 0.42 · `క` 0.56 · `ను` 0.72 · `␣చే` 0.97 · `ర` 0.87 · `్య` 5.9e-8✱ · `్య` 1.0e-4✱ · `్` 1.8e-6✱ · `మా` 0.42 · `మ` 0.09✱ · `మ` 0.84 · `రి` 0.74 · `␣మ` 0.65 · `న` 3.8e-3✱ · `⏎` 2.0e-4✱ forced |
| 2 | `మ` 0.58 · `␣` 1.2e-3✱ · `ర` 1.6e-4✱ · `ని` 0.72 · `␣దా` 0.97 · `టి` 0.97 · `␣మ` 0.89 · `డ` 0.96 · `ల` 0.93 · `మ` 2.6e-4✱ · `శ` 0.99 · `లే` 1.5e-3✱ · `మ` 0.90 · `ను` 0.98 · `␣జ` 0.99 · `ు` 0.99 · `మ` 8.3e-6✱ · `మా` 2.5e-5✱ · `డి` 1.00 · `␣హ` 1.00 · `ను` 1.00 · `తు` 4.7e-4✱ · `తు` 0.99 · `డు` 0.91 · `␣వ` 4.6e-3✱ · `్ర` 1.5e-6✱ · `్ర` 1.6e-3✱ · `్` 1.9e-7✱ · `మ` 0.23✱ · `ౌ` 0.94 · `మా` 0.56 · `మ` 0.02✱ · `మ` 0.80 · `రి` 0.45 · `␣మ` 0.05✱ · `⏎` 0.20✱ forced |
| 3 | `సి` 0.05✱ · `␣` 1.0e-6✱ · `రిగ` 1.0e-4✱ · `ె` 0.96 · `␣మ` 0.99 · `డ` 0.99 · `ల` 0.99 · `␣జ` 1.00 · `ల` 1.00 · `ధ` 3.9e-3✱ · `్వ` 2.5e-5✱ · `్వ` 2.9e-3✱ · `్` 8.1e-9✱ · `శ` 8.1e-5✱ · `ిన` 2.7e-4✱ · `␣ల` 0.87 · `క` 0.55 · `ను` 0.75 · `ను` 1.9e-3✱ · `␣మ` 0.27 · `␣మ` 0.08✱ · `్` 1.4e-5✱ · `మ` 0.33✱ · `్ర` 8.1e-7✱ · `్` 4.0e-5✱ · `జ` 1.4e-3✱ · `ిన` 1.2e-4✱ · `య` 0.55 · `తి` 0.62 · `␣ప్రా` 0.91 · `స` 0.96 · `స` 0.32✱ · `స` 0.04✱ · `్య` 2.6e-5✱ · `్య` 0.74 · `్య` 0.02✱ · `ీ` 1.2e-3✱ · `␣హ` 0.41 · `␣హ` 0.54 · `మ` 0.19✱ · `మ` 0.13✱ · `మ` 0.42 · `⏎` 0.74 |
| 4 | `మ` 0.75 · `␣` 6.8e-3✱ · `ర` 8.3e-7✱ · `న` 0.90 · `న` 0.57 · `ల` 0.30 · `ల` 0.55 · `ల` 0.87 · `ధి` 0.58 · `ధ` 5.0e-3✱ · `్ర` 3.8e-4✱ · `్ర` 0.30 · `్` 0.02✱ · `మ` 0.88 · `టి` 0.72 · `టి` 0.67 · `ని` 0.48 · `␣ల` 0.92 · `ంక` 0.58 · `␣మ` 4.5e-3✱ · `␣మ` 0.58 · `మ` 0.97 · `␣జ` 0.72 · `␣జ` 0.61 · `ం` 0.99 · `పా` 0.91 · `ణ` 0.28✱ · `␣హ` 7.4e-3✱ · `్య` 2.4e-5✱ · `్య` 1.1e-3✱ · `్` 1.1e-5✱ · `మం` 0.97 · `తు` 0.92 · `డు` 0.64 · `␣మ` 0.96 · `మ` 8.5e-5✱ · `ర` 1.6e-5✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 152 tokens · 25.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మనమ మను లోడ్ర్ర్క మదము నిక న మ్మ్ర్కతనల మనమ లోడ్ర్ర్క మదమ నిన్ని | `IIIIIIIUIIIIIIIIIIIIIIUIIIIUI` |
| 2 | కమ మ మమ మనన మ్మ్ర్క మ మము నక న మ్మ్ర్కతనల మనమ లోడ్ర్ర్క మదము నిన్ని | `IIIIIIIIIIIIIIIIIIIIIIUIIIIUI` |
| 3 | ము మము ను లేదు ఈ పూరు తరువులము టి రురువుజ ఇవి ల్ర్ర్పులు వరుసైన | `IIIIUIUUIIIIIIIIIIIIIIIIIUI` |
| 4 | న మ మ మ మ కు లెక్క మ్ల్యా లేదు లేదు మ్ల్యం మతి మతి మతి మ్యం మతి మతి మ | `IIIIIIUIUUIUIUIIIIIIUIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 43% · single-akshara words 34% · repeated lines 0 · mean token probability (geometric) 0.043 · model's first choice kept 48% · constraint overrode 41% · backtracks 0

<details><summary>Token probabilities (152 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.19 · `మ` 0.12 · `␣మ` 0.08 · `న` 0.02 · `మ` 0.04 · `␣మ` 0.06 · `ను` 0.02 · `␣లో` 0.02 · `డ` 0.01 · `్ర` 3.7e-4✱ · `్ర` 4.1e-4✱ · `్` 2.0e-5✱ · `క` 0.04✱ · `␣మ` 0.17 · `ద` 0.03 · `ము` 0.09 · `␣ని` 0.09 · `క` 0.05✱ · `␣న` 0.05 · `␣మ` 7.8e-3✱ · `్` 4.0e-4✱ · `మ` 0.22 · `్ర` 7.7e-5✱ · `్` 5.1e-5✱ · `క` 0.03✱ · `త` 0.01✱ · `న` 0.43 · `ల` 0.11 · `␣మ` 0.42 · `న` 0.60 · `మ` 0.46 · `␣లో` 0.73 · `డ` 0.52 · `్ర` 0.07✱ · `్ర` 0.19 · `్` 0.57 · `క` 0.96 · `␣మ` 0.33 · `ద` 0.19 · `మ` 0.15 · `␣ని` 0.20 · `న్ని` 0.01 · `⏎` 0.36 |
| 2 | `క` 0.36 · `మ` 0.56 · `␣మ` 0.23 · `␣మ` 0.10 · `మ` 0.47 · `␣మ` 0.29 · `న` 0.15 · `న` 0.03 · `␣మ` 0.51 · `్` 3.1e-4✱ · `మ` 0.40 · `్ర` 0.62 · `్` 0.41 · `క` 0.92 · `␣మ` 0.45 · `␣మ` 0.13 · `ము` 0.43 · `␣న` 0.05 · `క` 0.32 · `␣న` 0.37 · `␣మ` 0.42 · `్` 0.24 · `మ` 0.25 · `్ర` 0.44 · `్` 0.90 · `క` 0.97 · `త` 0.85 · `న` 0.90 · `ల` 0.96 · `␣మ` 0.92 · `న` 0.94 · `మ` 0.80 · `␣లో` 0.92 · `డ` 0.99 · `్ర` 0.69 · `్ర` 0.91 · `్` 0.90 · `క` 0.96 · `␣మ` 0.92 · `ద` 0.83 · `ము` 0.77 · `␣ని` 0.88 · `న్ని` 0.89 · `⏎` 3.4e-3✱ forced |
| 3 | `␣` 1.4e-5✱ · `ము` 3.6e-5✱ · `␣` 1.1e-4✱ · `మ` 3.6e-6✱ · `ము` 6.7e-5✱ · `␣` 2.6e-3✱ · `ను` 1.7e-3✱ · `␣లేదు` 8.9e-3✱ · `␣ఈ` 8.2e-3✱ · `␣ప` 2.4e-3✱ · `ూరు` 8.1e-6✱ · `␣తరు` 0.82 · `వు` 7.5e-3✱ · `ల` 9.4e-3✱ · `ము` 4.5e-3✱ · `␣` 0.66 · `టి` 1.4e-3✱ · `␣` 1.6e-3✱ · `రు` 0.08✱ · `రువు` 0.30 · `జ` 1.00 · `␣ఇ` 0.02✱ · `వి` 0.22✱ · `␣ల` 6.7e-4✱ · `్ర` 4.0e-5✱ · `్ర` 3.2e-4✱ · `్` 3.2e-3✱ · `పు` 8.1e-4✱ · `లు` 0.08✱ · `␣వరు` 7.9e-3✱ · `స` 0.44 · `ైన` 2.5e-3✱ · `⏎` 4.7e-4✱ forced |
| 4 | `న` 4.7e-3✱ · `␣మ` 0.02✱ · `␣మ` 0.03✱ · `␣మ` 0.10✱ · `␣మ` 7.1e-4✱ · `␣` 0.91 · `కు` 4.4e-4✱ · `␣లె` 2.5e-3✱ · `క్క` 6.0e-4✱ · `␣మ` 0.01✱ · `్` 4.9e-3✱ · `ల` 2.5e-3✱ · `్యా` 5.6e-5✱ · `␣లేదు` 0.02✱ · `␣లేదు` 5.1e-3✱ · `␣మ` 0.01✱ · `్` 2.0e-3✱ · `ల` 0.34✱ · `్యం` 1.5e-4✱ · `␣మ` 0.13✱ · `తి` 0.82 · `␣మ` 0.91 · `తి` 0.96 · `␣మ` 0.98 · `తి` 0.94 · `␣మ` 0.99 · `్యం` 1.7e-4✱ · `␣మ` 0.99 · `తి` 0.93 · `␣మ` 0.99 · `తి` 0.98 · `␣మ` 0.87 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 144 tokens · 28.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మమత వల లల స ల్ర్ర్మ న ల నమ హమమత వల లల సల శ్ర్మ న ల నమ మమ | `IIIIIIIIIIIIIIIIIIIIIIIIIIIIII` |
| 2 | ల మల లల శల ల్రలమ న ల నమమల లల శల ల శంమ లమ ల హ హమ మ | `IIIIIIIIIIIIIIIIIIIIIUIIIIIIII` |
| 3 | మమ మల వల ల ల స్ర్ర్మమ ల ల నమమ ల్య్య్మ లల ల ల ల్రలమ ల్య్య్మమలక్ష క్షమమ | `IIIIIIIIIIIIIIIIIIIIIIIIIUIIII` |
| 4 | పొమె పద్యలో సాంవివొట్లు ఉన్నాయి ప్రువుజ పద్యము యొక్క య్మ్ర్రోమమ మొదటి | `IIUIUUIUIUUIIIIUIIUIUIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 31% · single-akshara words 36% · repeated lines 0 · mean token probability (geometric) 0.059 · model's first choice kept 50% · constraint overrode 32% · backtracks 0

<details><summary>Token probabilities (144 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.71 · `మ` 0.20 · `త` 0.04 · `␣వ` 0.02 · `ల` 0.25 · `␣ల` 0.02 · `ల` 0.04 · `␣స` 0.17 · `␣ల` 0.04✱ · `్ర` 2.8e-4✱ · `్ర` 1.4e-3✱ · `్` 1.6e-4✱ · `మ` 0.06✱ · `␣న` 0.63 · `␣ల` 0.44 · `␣న` 0.16 · `మ` 0.12 · `␣హ` 4.0e-4✱ · `మ` 0.66 · `మ` 0.81 · `త` 0.58 · `␣వ` 0.80 · `ల` 0.84 · `␣ల` 0.93 · `ల` 0.78 · `␣స` 0.79 · `ల` 0.49 · `␣శ` 0.90 · `్ర` 0.91 · `్` 0.91 · `మ` 0.90 · `␣న` 0.67 · `␣ల` 0.90 · `␣న` 0.81 · `మ` 0.66 · `␣మ` 4.8e-3✱ · `మ` 0.83 · `⏎` 4.9e-4✱ forced |
| 2 | `ల` 0.01 · `␣మ` 0.02✱ · `ల` 0.45 · `␣ల` 0.52 · `ల` 0.64 · `␣శ` 0.12 · `ల` 0.56 · `␣ల` 0.11 · `్ర` 0.37 · `ల` 0.11 · `మ` 0.58 · `␣న` 0.43 · `␣ల` 0.69 · `␣న` 0.50 · `మ` 0.61 · `మ` 0.08✱ · `ల` 0.11✱ · `␣ల` 0.25 · `ల` 0.50 · `␣శ` 0.13 · `ల` 0.50 · `␣ల` 0.31 · `␣శ` 0.19 · `ం` 0.02 · `మ` 0.20 · `␣ల` 0.27 · `మ` 0.04 · `␣ల` 0.14 · `␣హ` 0.03 · `␣హ` 0.03 · `మ` 0.22 · `␣మ` 0.08✱ · `⏎` 0.13✱ forced |
| 3 | `మ` 0.26 · `మ` 0.26 · `␣మ` 0.22 · `ల` 0.35 · `␣వ` 0.23 · `ల` 0.43 · `␣ల` 0.35 · `␣ల` 0.17 · `␣స` 0.26 · `్ర` 9.6e-5✱ · `్ర` 2.8e-3✱ · `్` 0.01✱ · `మ` 0.34✱ · `మ` 0.58 · `␣ల` 0.60 · `␣ల` 0.70 · `␣న` 0.49 · `మ` 0.55 · `మ` 0.16 · `␣ల` 0.10 · `్య` 2.5e-4✱ · `్య` 3.0e-3✱ · `్` 2.4e-6✱ · `మ` 0.06✱ · `␣ల` 0.61 · `ల` 0.34 · `␣ల` 0.22 · `␣ల` 0.19 · `␣ల` 0.54 · `్ర` 0.17 · `ల` 0.18 · `మ` 0.48 · `␣ల` 0.43 · `్య` 3.9e-4✱ · `్య` 2.4e-3✱ · `్` 1.1e-4✱ · `మ` 0.64 · `మ` 0.67 · `ల` 2.5e-3✱ · `క్ష` 8.3e-4✱ · `␣క్ష` 5.7e-3✱ · `మ` 1.00 · `మ` 1.5e-5✱ · `⏎` 0.22✱ |
| 4 | `ప` 1.00 · `ొ` 1.6e-5✱ · `మె` 4.8e-5✱ · `␣ప` 0.98 · `ద్య` 0.96 · `లో` 1.9e-4✱ · `␣సాం` 0.97 · `వి` 9.9e-4✱ · `వ` 1.2e-4✱ · `ొ` 2.3e-6✱ · `ట్లు` 0.12✱ · `␣ఉన్నాయి` 0.99 · `␣ప్ర` 2.1e-5✱ · `ు` 3.1e-4✱ · `వు` 0.01✱ · `జ` 0.99 · `␣ప` 0.84 · `ద్య` 0.99 · `ము` 0.98 · `␣యొక్క` 0.98 · `␣య` 0.97 · `్` 5.7e-6✱ · `మ` 0.06✱ · `్ర` 1.2e-4✱ · `్ర` 2.1e-4✱ · `ో` 1.0e-4✱ · `మ` 2.3e-3✱ · `మ` 0.99 · `␣మొదటి` 8.3e-4✱ |

</details>

[↑ meters](#meters)

---

<a id="dvipada"></a>

## 22. ద్విపద (dvipada)

```text
Meter: ద్విపద (dvipada), a jāti meter.
Lines (పాదాలు): 2.
Every line: 4 gaṇas (11 to 15 aksharas):
  gaṇa 1: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 2: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 3: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 4: న (III) or హ (UI)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 3.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter ద్విపద (dvipada).

Meter: ద్విపద (dvipada), a jāti meter.
Lines (పాదాలు): 2.
Every line: 4 gaṇas (11 to 15 aksharas):
  gaṇa 1: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 2: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 3: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 4: న (III) or హ (UI)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 3.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 2 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 37 tokens · 5.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కల్లి మ మమ మనుడ్ర్ర్క మత మెదక బె | `UIIIIIUIIIIIII` |
| 2 | కల్లిమ మల మ మ య్ర్ర్క మత మెదక న | `UIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 27% · single-akshara words 40% · repeated lines 0 · mean token probability (geometric) 0.039 · model's first choice kept 43% · constraint overrode 32% · backtracks 0

<details><summary>Token probabilities (37 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.13 · `ల్లి` 0.05 · `␣మ` 0.09 · `␣మ` 0.09 · `మ` 0.03 · `␣మ` 0.06 · `ను` 0.02 · `డ` 0.03 · `్ర` 2.1e-4✱ · `్ర` 2.3e-4✱ · `్` 3.5e-6✱ · `క` 0.06✱ · `␣మ` 0.15 · `త` 0.02 · `␣మె` 3.9e-3 · `ద` 5.0e-3✱ · `క` 0.16 · `␣బె` 5.7e-4✱ · `⏎` 6.7e-3✱ forced |
| 2 | `క` 0.19 · `ల్లి` 0.05✱ · `మ` 0.09 · `␣మ` 0.28 · `ల` 0.03 · `␣మ` 0.32 · `␣మ` 0.21 · `␣య` 2.4e-3✱ · `్ర` 6.5e-4✱ · `్ర` 0.08✱ · `్` 0.16✱ · `క` 0.88 · `␣మ` 0.79 · `త` 0.66 · `␣మె` 0.79 · `ద` 0.76 · `క` 0.82 · `␣న` 0.84 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 37 tokens · 6.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాతిలసి వ లస స్రల సాము లేకు | `UIIIIIIIIUIUI` |
| 2 | మాతిలసి వ లస స్ర్ర్మ ల లకు కు ట్ట ట్టి | `UIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 27% · single-akshara words 47% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 38% · constraint overrode 35% · backtracks 0

<details><summary>Token probabilities (37 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.36 · `తి` 0.03 · `ల` 0.02 · `సి` 5.1e-3 · `␣వ` 7.8e-3 · `␣ల` 0.07 · `స` 3.8e-3 · `␣స` 0.01 · `్ర` 4.0e-4✱ · `ల` 0.02 · `␣సా` 1.4e-3 · `ము` 0.06 · `␣ల` 0.12 · `ే` 2.1e-3✱ · `కు` 0.01✱ · `⏎` 0.94 |
| 2 | `మా` 0.23 · `తి` 0.92 · `ల` 0.57 · `సి` 0.73 · `␣వ` 0.80 · `␣ల` 0.86 · `స` 0.73 · `␣స` 0.84 · `్ర` 0.96 · `్ర` 5.0e-5✱ · `్` 7.6e-7✱ · `మ` 0.01✱ · `␣ల` 0.90 · `␣ల` 0.01✱ · `కు` 0.84 · `␣` 1.2e-3✱ · `కు` 3.3e-3✱ · `␣` 1.5e-4✱ · `ట్ట` 1.4e-7✱ · `␣` 2.7e-4✱ · `ట్టి` 2.5e-6✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 31 tokens · 23.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి మాతగనన్ మృ హ్వ్య్దయ ప్రేమ మతము | `UIUIIUIIIUIIII` |
| 2 | తల్లి ప్రేమ మ అతిధ్రపు కరుణముము | `UIUIIIUIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 45% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.132 · model's first choice kept 77% · constraint overrode 13% · backtracks 22

<details><summary>Token probabilities (31 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.93 · `ల్లి` 0.78 · `␣మ` 0.49 · `ాత` 0.98 · `గ` 0.89 · `న` 3.6e-3 · `న్` 0.76 · `␣మ` 0.95 · `ృ` 0.96 · `␣హ` 0.98 · `్వ` 0.78 · `్య` 8.7e-7✱ · `్` 1.0e-9✱ · `దయ` 0.54 · `␣ప్రేమ` 0.59 · `␣మ` 0.01✱ · `త` 0.49 · `ము` 0.99 · `⏎` 0.98 |
| 2 | `త` 0.27 · `ల్లి` 0.56 · `␣ప్రేమ` 0.96 · `␣మ` 0.94 · `␣అతి` 0.95 · `ధ` 1.1e-4 · `్ర` 0.97 · `పు` 0.96 · `␣క` 0.98 · `రుణ` 0.97 · `ము` 0.99 · `ము` 0.06✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 31 tokens · 14.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నీ కర్మళ గుణి పచ్చ్ర్నికవైన ప్రేమ | `UUIIIIUIIUIUI` |
| 2 | త్యాకమ్మల మతలక్యా మిన్నను మరు | `UUIIIIUUUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 33% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.091 · model's first choice kept 71% · constraint overrode 16% · backtracks 13

<details><summary>Token probabilities (31 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `నీ` 3.3e-3 · `␣క` 0.95 · `ర్మ` 0.02 · `ళ` 0.03 · `␣గు` 0.96 · `ణి` 3.1e-3 · `␣ప` 0.75 · `చ్చ` 0.79 · `్ర` 3.4e-5✱ · `్` 1.9e-8✱ · `న` 0.83 · `ిక` 0.76 · `వ` 0.90 · `ైన` 0.94 · `␣ప్రేమ` 0.97 · `⏎` 0.98 |
| 2 | `త` 0.98 · `్యా` 0.97 · `క` 0.95 · `మ్మ` 0.98 · `ల` 0.97 · `␣మ` 0.92 · `త` 0.85 · `ల` 0.24 · `క` 0.97 · `్యా` 1.6e-6✱ · `␣మి` 0.75 · `న్న` 0.94 · `ను` 4.0e-4✱ · `␣మ` 0.98 · `రు` 0.06✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 39 tokens · 12.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాతి నిలిల లోక జ్వ్వ్రణము రాతి నలి | `UIIIIUIIIIUIII` |
| 2 | లోత జ్వాల్యతముము ల్ల్య్యో లుతినుకును | `UIUIIIIUIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 40% · single-akshara words 10% · repeated lines 0 · mean token probability (geometric) 0.011 · model's first choice kept 36% · constraint overrode 51% · backtracks 0

<details><summary>Token probabilities (39 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.36 · `తి` 0.03 · `␣ని` 0.07 · `లి` 0.05 · `ల` 0.11 · `␣లో` 0.02 · `క` 0.55 · `␣జ` 0.03✱ · `్వ` 3.0e-3✱ · `్వ` 2.0e-3✱ · `్` 1.5e-5✱ · `రణ` 7.4e-4✱ · `ము` 0.64 · `␣` 1.8e-3✱ · `రా` 0.88 · `తి` 0.90 · `␣న` 0.04 · `లి` 0.95 · `⏎` 4.9e-6✱ forced |
| 2 | `␣లో` 0.96 · `త` 7.1e-4✱ · `␣జ` 0.99 · `్వ` 0.98 · `ాల` 0.99 · `్య` 0.98 · `త` 0.02 · `ము` 0.59 · `ము` 0.13✱ · `␣` 9.4e-4✱ · `ల్ల` 9.7e-7✱ · `్య` 3.3e-7✱ · `్య` 1.5e-6✱ · `ో` 1.3e-5✱ · `␣` 5.5e-4✱ · `లు` 2.6e-3✱ · `తి` 1.4e-3✱ · `ను` 6.8e-3✱ · `కు` 4.5e-3✱ · `ను` 0.01✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 32 tokens · 5.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కల్లి మ మమ మతమ్య్య్కంటే మి గొప్ప | `UIIIIIUUUIUI` |
| 2 | దిల్లకక మన మమ్య్య్దిన లో మి గొప్ప | `UIIIIIUIIUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 33% · single-akshara words 33% · repeated lines 0 · mean token probability (geometric) 0.031 · model's first choice kept 34% · constraint overrode 38% · backtracks 0

<details><summary>Token probabilities (32 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.13 · `ల్లి` 0.05 · `␣మ` 0.09 · `␣మ` 0.09 · `మ` 0.03 · `␣మ` 0.06 · `త` 0.04 · `మ` 0.08✱ · `్య` 2.0e-4✱ · `్య` 3.5e-4✱ · `్` 2.2e-6✱ · `క` 0.04✱ · `ంటే` 0.04 · `␣మి` 0.08✱ · `␣గొప్ప` 0.08✱ · `⏎` 0.17 forced |
| 2 | `ది` 0.34 · `ల్ల` 0.01✱ · `క` 0.20 · `క` 0.10 · `␣మ` 0.23 · `న` 0.02 · `␣మ` 0.25 · `మ` 0.06 · `్య` 2.9e-3✱ · `్య` 0.07 · `్` 0.03✱ · `ద` 0.02✱ · `ిన` 3.4e-3✱ · `␣లో` 0.08 · `␣మి` 0.42 · `␣గొప్ప` 0.55 |

</details>

[↑ meters](#meters)

---

<a id="madhyakkara"></a>

## 23. మధ్యాక్కర (madhyakkara)

```text
Meter: మధ్యాక్కర (madhyakkara), a jāti meter.
Lines (పాదాలు): 4.
Every line: 6 gaṇas (16 to 22 aksharas):
  gaṇa 1: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 2: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 3: న (III) or హ (UI)
  gaṇa 4: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 5: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 6: న (III) or హ (UI)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 4.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter మధ్యాక్కర (madhyakkara).

Meter: మధ్యాక్కర (madhyakkara), a jāti meter.
Lines (పాదాలు): 4.
Every line: 6 gaṇas (16 to 22 aksharas):
  gaṇa 1: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 2: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 3: న (III) or హ (UI)
  gaṇa 4: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 5: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 6: న (III) or హ (UI)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 4.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 102 tokens · 13.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కకమల ప్రానివమల దొకటి నెమామకమకమకక | `IIIIUIIIIIIIIUIIIIIII` |
| 2 | కకమన్యతి మమ మమ ద జ స్ర్ర్క పుమ మమమమమకమక | `IIUIIIIIIIIIIIIIIIIIII` |
| 3 | కకతత మమ మమమతి మ మ్య్య్కమ మమ మమకకమతక | `IIIIIIIIIIIIIIIIIIIIII` |
| 4 | కకమమతి మమ మమ మమ మ్ర్ర్కాకకకకకశకుకుక | `IIIIIIIIIIIUIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.044 · model's first choice kept 36% · constraint overrode 31% · backtracks 0

<details><summary>Token probabilities (102 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.17 · `క` 0.04 · `మ` 0.06 · `ల` 0.04 · `␣ప్రా` 2.0e-3 · `ని` 0.01 · `వ` 0.02 · `మ` 0.05 · `ల` 0.03 · `␣ద` 0.01✱ · `ొ` 1.4e-3✱ · `క` 0.07✱ · `టి` 0.02 · `␣నె` 5.9e-3✱ · `మా` 8.0e-3 · `మ` 0.06 · `క` 0.18 · `మ` 0.11 · `క` 0.14 · `మ` 0.12 · `క` 0.07 · `క` 0.06 · `⏎` 0.10✱ forced |
| 2 | `క` 0.18 · `క` 0.12✱ · `మ` 0.20 · `న్య` 2.1e-3 · `తి` 0.01 · `␣మ` 0.05 · `మ` 0.07 · `␣మ` 0.05 · `మ` 0.07 · `␣ద` 0.01 · `␣జ` 8.4e-3 · `␣స` 7.7e-3✱ · `్ర` 6.1e-3✱ · `్ర` 1.1e-4✱ · `్` 1.5e-5✱ · `క` 0.06✱ · `␣పు` 2.1e-3 · `మ` 0.16 · `␣మ` 0.09 · `మ` 0.22 · `మ` 0.37 · `మ` 0.26 · `మ` 0.38 · `క` 0.63 · `మ` 0.07 · `క` 0.08✱ · `⏎` 0.06✱ forced |
| 3 | `క` 0.78 · `క` 0.59 · `త` 0.13 · `త` 0.19 · `␣మ` 0.15 · `మ` 0.21 · `␣మ` 0.11 · `మ` 0.18 · `మ` 0.17 · `తి` 8.2e-3 · `␣మ` 0.13 · `␣మ` 0.13✱ · `్య` 9.0e-5✱ · `్య` 2.8e-3✱ · `్` 1.2e-5✱ · `క` 5.1e-3✱ · `మ` 0.56 · `␣మ` 0.18 · `మ` 0.56 · `␣మ` 0.05 · `మ` 0.50 · `క` 0.29 · `క` 0.54 · `మ` 0.54 · `త` 0.62 · `క` 0.04✱ · `⏎` 0.75 |
| 4 | `క` 0.94 · `క` 0.97 · `మ` 0.54 · `మ` 0.76 · `తి` 0.49 · `␣మ` 0.81 · `మ` 0.87 · `␣మ` 0.75 · `మ` 0.75 · `␣మ` 0.22 · `మ` 0.21 · `␣మ` 0.15✱ · `్ర` 2.0e-4✱ · `్ర` 1.8e-3✱ · `్` 2.9e-4✱ · `కా` 1.00 · `క` 2.0e-4✱ · `క` 4.3e-3✱ · `క` 0.01✱ · `క` 0.02✱ · `క` 3.3e-3✱ · `శ` 1.5e-3✱ · `కు` 6.3e-3✱ · `కు` 0.02✱ · `క` 7.5e-3✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 89 tokens · 4.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మమమ సిమముతురిఘయుము మమతు మడమనయుమ మమ | `IIIIIIIIIIIIIIIIIIIIII` |
| 2 | మమమ లంక నవపుమున మ మ మముతులేముమ మమమ | `IIIUIIIIIIIIIIIUIIIII` |
| 3 | మమ క మతమనునుచు మచు మ మక సవ మగముమ మమ | `IIIIIIIIIIIIIIIIIIIIII` |
| 4 | మమమ ద ద మ మందు మ మమ మమ తమ జకపుయుమ మమ | `IIIIIIUIIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 28% · single-akshara words 25% · repeated lines 0 · mean token probability (geometric) 0.058 · model's first choice kept 40% · constraint overrode 8% · backtracks 0

<details><summary>Token probabilities (89 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.49 · `మ` 0.12 · `మ` 0.04 · `␣సి` 4.3e-3 · `మ` 0.04 · `ము` 0.06 · `తు` 2.9e-3 · `రి` 5.2e-3 · `ఘ` 3.6e-3 · `యు` 4.2e-3 · `ము` 0.06 · `␣మ` 0.18 · `మ` 0.15 · `తు` 3.2e-3 · `␣మ` 0.03 · `డ` 8.8e-3✱ · `మన` 3.9e-3✱ · `యు` 4.6e-3✱ · `మ` 0.50 · `␣మ` 5.8e-3✱ · `మ` 0.72 · `⏎` 0.18✱ forced |
| 2 | `మ` 0.34 · `మ` 0.77 · `మ` 0.56 · `␣ల` 0.53 · `ంక` 0.51 · `␣న` 0.04 · `వ` 5.7e-3 · `పు` 9.0e-3 · `ము` 0.02 · `న` 0.02 · `␣మ` 0.19 · `␣మ` 0.23 · `␣మ` 0.17 · `ము` 0.05 · `తు` 8.4e-3 · `లే` 3.7e-3 · `ము` 0.04 · `మ` 0.12 · `␣మ` 0.44 · `మ` 0.60 · `మ` 0.13✱ · `⏎` 0.05✱ |
| 3 | `మ` 0.92 · `మ` 0.67 · `␣క` 9.6e-3 · `␣మ` 0.06 · `త` 0.02 · `మ` 0.07 · `ను` 0.04 · `ను` 0.04 · `చు` 0.03 · `␣మ` 0.14 · `చు` 0.01 · `␣మ` 0.29 · `␣మ` 0.23 · `క` 0.01 · `␣స` 0.01 · `వ` 0.01 · `␣మ` 0.08 · `గ` 0.01 · `ము` 0.07 · `మ` 0.32 · `␣మ` 0.62 · `మ` 0.88 · `⏎` 0.66 |
| 4 | `మ` 0.86 · `మ` 0.82 · `మ` 0.67 · `␣ద` 0.08 · `␣ద` 0.02 · `␣మ` 0.05 · `␣మ` 0.06 · `ందు` 2.8e-3 · `␣మ` 0.08 · `␣మ` 0.12 · `మ` 0.08 · `␣మ` 0.25 · `మ` 0.08 · `␣త` 3.9e-3 · `మ` 0.09 · `␣జ` 0.01 · `క` 0.01 · `పు` 0.01 · `యు` 0.05 · `మ` 0.17 · `␣మ` 0.13 · `మ` 0.22 |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 103 tokens · 58.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మడులచి వ ఇదిన మ జట స్ర్ర్మం సు లతి లతరడనుగ | `IIIIIIIIIIIUIIIIIIIII` |
| 2 | మడ వేగ మశుడు వీర హను మన్న్డు మమ సక భరమ్మ | `IIUIIIIUIIIUIIIIIIUI` |
| 3 | నొడర దాటి ల లకను జర జ్యు మెవనమ్మ డుడు వనము ల | `IIIUIIIIIIIIIIUIIIIIII` |
| 4 | నడు డునుడనుగను డు తిడు ల్యా లక లలలనలకము | `IIIIIIIIIIIUIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 31% · single-akshara words 26% · repeated lines 0 · mean token probability (geometric) 0.017 · model's first choice kept 30% · constraint overrode 53% · backtracks 30

<details><summary>Token probabilities (103 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.20 · `డు` 2.8e-3 · `ల` 0.93 · `చి` 1.4e-3 · `␣వ` 0.58 · `␣ఇది` 7.4e-5 · `న` 0.04 · `␣మ` 0.09 · `␣జ` 0.02 · `ట` 0.96 · `␣స` 0.82 · `్ర` 8.7e-8✱ · `్ర` 2.9e-3✱ · `్` 3.1e-7✱ · `మం` 7.3e-4✱ · `␣సు` 0.01✱ · `␣ల` 0.04 · `తి` 0.91 · `␣ల` 7.7e-3 · `తర` 0.04 · `డ` 0.01 · `ను` 0.05 · `గ` 4.3e-3✱ · `⏎` 0.04✱ forced |
| 2 | `మ` 0.19 · `డ` 0.01✱ · `␣వే` 0.97 · `గ` 0.61 · `␣మ` 0.51 · `శ` 0.20 · `ుడు` 4.8e-4✱ · `␣వీ` 0.98 · `ర` 0.98 · `␣హ` 0.99 · `ను` 0.96 · `␣మ` 0.98 · `న్` 0.89 · `న్` 0.34 · `డు` 0.19 · `␣మ` 0.03✱ · `మ` 0.19 · `␣స` 0.09 · `క` 8.4e-4 · `␣భ` 0.74 · `ర` 0.71 · `మ్మ` 5.0e-3 · `⏎` 0.15 |
| 3 | `న` 0.03 · `ొ` 0.08✱ · `డ` 0.06✱ · `ర` 0.94 · `␣దా` 0.96 · `టి` 0.93 · `␣ల` 0.98 · `␣ల` 3.0e-3✱ · `క` 0.91 · `ను` 0.92 · `␣జ` 1.1e-3✱ · `ర` 0.96 · `␣జ` 0.84 · `్య` 7.7e-6✱ · `ు` 0.02✱ · `␣మె` 2.1e-4✱ · `వ` 8.4e-4✱ · `న` 2.0e-3✱ · `మ్మ` 0.04✱ · `␣` 1.8e-3✱ · `డు` 6.3e-7✱ · `డు` 7.4e-4✱ · `␣` 4.5e-5✱ · `వ` 9.3e-3✱ · `న` 0.04✱ · `ము` 0.01✱ · `␣` 2.2e-3✱ · `ల` 5.2e-4✱ · `⏎` 0.03✱ forced |
| 4 | `న` 1.8e-4✱ · `డు` 1.8e-3✱ · `␣` 0.04✱ · `డు` 0.52 · `ను` 0.03✱ · `డ` 0.05 · `ను` 0.11✱ · `గ` 0.13✱ · `ను` 4.7e-4✱ · `␣` 1.8e-4✱ · `డు` 1.7e-4✱ · `␣` 2.4e-3✱ · `తి` 3.9e-4✱ · `డు` 0.02✱ · `␣` 0.04✱ · `ల` 0.02✱ · `్యా` 2.1e-4✱ · `␣` 1.2e-3✱ · `ల` 7.6e-3✱ · `క` 6.2e-3✱ · `␣ల` 0.02✱ · `ల` 0.01✱ · `ల` 7.9e-3✱ · `న` 7.5e-3✱ · `ల` 0.04✱ · `క` 0.01✱ · `ము` 0.04✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 95 tokens · 44.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నతిమల ప్రాణ మమల దొ ర్ర్వ్న యధువతిప్రజతిమల | `IIIIUIIIIIIIIIUIIIII` |
| 2 | తృత గుణ మీలటి లీతమృణము మమతిమల లోక | `IIIIUIIUIIIIIIIIIUI` |
| 3 | మత దొ ర్ర్వ్న యధువతిప్రజతిమల లోకమతిమల దీప | `IIIIIIIUIIIIIUIIIIIUI` |
| 4 | కృతి విభముడుగుణు ప్రతిత నేను నితివనముము చవ | `IIIIIIIIIIIUIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.066 · model's first choice kept 59% · constraint overrode 31% · backtracks 30

<details><summary>Token probabilities (95 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `న` 0.01 · `తి` 0.05 · `మ` 0.67 · `ల` 0.75 · `␣ప్రా` 0.78 · `ణ` 0.66 · `␣మ` 0.37 · `మ` 0.50 · `ల` 0.78 · `␣ద` 0.41 · `ొ` 0.98 · `␣ర` 0.16✱ · `్ర` 3.4e-5✱ · `్వ` 1.1e-4✱ · `్` 5.4e-6✱ · `న` 0.14 · `␣య` 6.4e-4 · `ధు` 0.97 · `వ` 0.62 · `తి` 0.57 · `ప్ర` 1.6e-3✱ · `జ` 0.68 · `తి` 0.83 · `మ` 0.82 · `ల` 0.88 · `⏎` 0.02✱ forced |
| 2 | `త` 0.51 · `ృ` 4.4e-3✱ · `త` 1.5e-3✱ · `␣గు` 0.99 · `ణ` 0.99 · `␣మ` 0.79 · `ీల` 1.2e-3 · `టి` 4.0e-3 · `␣ల` 0.93 · `ీ` 0.89 · `త` 0.87 · `మ` 0.11 · `ృ` 1.4e-3✱ · `ణ` 0.24 · `ము` 0.09 · `␣మ` 0.23 · `మ` 0.81 · `తి` 0.68 · `మ` 0.02✱ · `ల` 0.13 · `␣లో` 0.62 · `క` 0.62 · `⏎` 9.6e-3✱ forced |
| 3 | `మ` 0.81 · `త` 2.2e-3✱ · `␣ద` 0.56 · `ొ` 0.96 · `␣ర` 0.90 · `్ర` 0.95 · `్వ` 0.93 · `్` 0.97 · `న` 0.95 · `␣య` 0.83 · `ధు` 0.97 · `వ` 0.92 · `తి` 0.93 · `ప్ర` 0.77 · `జ` 0.96 · `తి` 0.83 · `మ` 0.85 · `ల` 0.91 · `␣లో` 0.49 · `క` 0.22 · `మ` 0.15✱ · `తి` 0.14 · `మ` 0.58 · `ల` 0.69 · `␣దీ` 0.99 · `ప` 0.98 · `⏎` 1.00 |
| 4 | `క` 1.3e-3 · `ృ` 9.5e-5✱ · `తి` 0.99 · `␣విభ` 0.97 · `ము` 0.17✱ · `డుగు` 8.8e-7✱ · `ణు` 8.7e-8✱ · `␣ప్రతి` 1.2e-4✱ · `త` 8.0e-3✱ · `␣నేను` 1.5e-3✱ · `␣ని` 1.6e-3✱ · `తి` 1.7e-3✱ · `వ` 2.5e-3✱ · `న` 1.1e-3✱ · `ము` 0.04✱ · `ము` 7.1e-3✱ · `␣` 4.9e-5✱ · `చ` 1.4e-4✱ · `వ` 1.2e-3✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 78 tokens · 10.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కకమల వంటి మమను కకకచుక నడిపవే మల్ల | `IIIIUIIIIIIIIIIIIUUI` |
| 2 | కకమల వంటి మమను కకమచుక కాపాడ మల్ల | `IIIIUIIIIIIIIIUUIUI` |
| 3 | కకమల వంటి మమను కకమచుక పెమడమల్లల్ల | `IIIIUIIIIIIIIIIIIUUI` |
| 4 | కకల వంటి మమను కకమకక మలపుపుకము లేదు | `IIIUIIIIIIIIIIIIIIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 30% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.190 · model's first choice kept 67% · constraint overrode 14% · backtracks 0

<details><summary>Token probabilities (78 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.17 · `క` 0.04 · `మ` 0.06 · `ల` 0.04 · `␣వంటి` 0.02 · `␣మ` 0.40 · `మ` 0.53 · `ను` 0.05 · `␣క` 0.09 · `క` 5.4e-3✱ · `క` 0.04✱ · `చు` 0.02✱ · `క` 0.12 · `␣న` 0.02 · `డి` 0.13 · `ప` 0.62 · `వే` 0.03 · `␣మ` 7.3e-3✱ · `ల్ల` 2.1e-3 · `⏎` 0.86 |
| 2 | `క` 0.76 · `క` 0.50 · `మ` 0.34 · `ల` 0.80 · `␣వంటి` 0.16 · `␣మ` 0.31 · `మ` 0.15 · `ను` 0.16 · `␣క` 0.26 · `క` 0.51 · `మ` 0.07 · `చు` 0.64 · `క` 0.93 · `␣కా` 0.92 · `పా` 0.86 · `డ` 0.76 · `␣మ` 0.52 · `ల్ల` 0.50 · `⏎` 0.94 |
| 3 | `క` 0.99 · `క` 1.00 · `మ` 0.99 · `ల` 0.99 · `␣వంటి` 0.99 · `␣మ` 0.98 · `మ` 0.99 · `ను` 0.98 · `␣క` 0.92 · `క` 0.94 · `మ` 0.76 · `చు` 0.78 · `క` 0.95 · `␣పె` 0.09 · `మ` 0.14 · `డ` 0.01✱ · `మ` 0.09 · `ల్ల` 0.57 · `ల్ల` 8.1e-4✱ · `⏎` 6.4e-3✱ forced |
| 4 | `క` 0.99 · `క` 2.1e-3✱ · `ల` 0.98 · `␣వంటి` 0.99 · `␣మ` 0.99 · `మ` 0.98 · `ను` 0.95 · `␣క` 0.93 · `క` 0.96 · `మ` 0.95 · `క` 4.6e-4✱ · `క` 0.91 · `␣మ` 0.75 · `ల` 0.85 · `పు` 0.21 · `పు` 9.9e-4✱ · `క` 0.75 · `ము` 0.92 · `␣లేదు` 1.5e-5✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 80 tokens · 11.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మామల వేడలేని మరు మవమ మమ్మల న్యాయములుగు | `UIIUIUIIIIIIUIIUIIII` |
| 2 | మౌమతల మన మరు మనమ మినల లోకములే మ | `UIIIIIIIIIIIIIUIIUI` |
| 3 | లౌమల వేడ మ మ మ మలమ మమ్మల ణణము లేదు | `UIIUIIIIIIIUIIIIIUI` |
| 4 | మామల వేడలేని మరు మవమ మమ్మల లోకముద్య | `UIIUIUIIIIIIUIIUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 14% · repeated lines 0 · mean token probability (geometric) 0.166 · model's first choice kept 61% · constraint overrode 21% · backtracks 0

<details><summary>Token probabilities (80 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.07 · `మ` 0.19 · `ల` 0.05 · `␣వే` 0.02 · `డ` 0.08 · `లేని` 0.02 · `␣మ` 0.24 · `రు` 0.01 · `␣మ` 0.05✱ · `వ` 0.02 · `మ` 0.08✱ · `␣మ` 0.04✱ · `మ్మ` 0.03 · `ల` 0.02✱ · `␣` 0.01✱ · `న్య` 0.02✱ · `ాయ` 0.86 · `ము` 0.49 · `లుగు` 2.5e-4✱ · `⏎` 0.08✱ forced |
| 2 | `మ` 0.92 · `ౌ` 4.4e-4✱ · `మ` 7.4e-3✱ · `త` 0.20 · `ల` 0.03 · `␣మ` 0.70 · `న` 0.02✱ · `␣మ` 0.22 · `రు` 0.58 · `␣మ` 0.51 · `న` 0.03 · `మ` 0.57 · `␣మ` 0.77 · `ిన` 1.8e-3✱ · `ల` 0.76 · `␣లో` 1.00 · `క` 0.99 · `ము` 0.88 · `లే` 0.16 · `␣మ` 0.02✱ · `⏎` 0.18✱ |
| 3 | `ల` 0.01 · `ౌ` 0.06✱ · `మ` 0.43 · `ల` 0.53 · `␣వే` 0.51 · `డ` 0.64 · `␣మ` 0.13 · `␣మ` 0.78 · `␣మ` 0.26 · `␣మ` 0.69 · `ల` 1.1e-3✱ · `మ` 0.75 · `␣మ` 0.93 · `మ్మ` 0.64 · `ల` 0.89 · `␣` 0.78 · `ణ` 0.91 · `ణ` 0.29 · `ము` 0.97 · `␣లేదు` 0.02 · `⏎` 0.98 |
| 4 | `మా` 0.99 · `మ` 0.98 · `ల` 0.99 · `␣వే` 0.99 · `డ` 0.99 · `లేని` 1.00 · `␣మ` 0.99 · `రు` 0.98 · `␣మ` 0.98 · `వ` 0.94 · `మ` 0.90 · `␣మ` 0.99 · `మ్మ` 0.83 · `ల` 0.97 · `␣లో` 0.95 · `క` 0.72 · `ము` 0.94 · `ద్య` 1.8e-4✱ |

</details>

[↑ meters](#meters)

---

<a id="madhuragati_ragada"></a>

## 24. మధురగతి రగడ (madhuragati_ragada)

```text
Meter: మధురగతి రగడ (madhuragati_ragada), a jāti meter.
Lines (పాదాలు): 2.
Every line: 4 gaṇas (8 to 16 aksharas):
  gaṇa 1: గా (UU) or స (IIU) or జ (IUI) or భ (UII) or నల (IIII)
  gaṇa 2: గా (UU) or స (IIU) or జ (IUI) or భ (UII) or నల (IIII)
  gaṇa 3: గా (UU) or స (IIU) or జ (IUI) or భ (UII) or నల (IIII)
  gaṇa 4: గా (UU) or స (IIU) or జ (IUI) or భ (UII) or నల (IIII)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 3. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter మధురగతి రగడ (madhuragati_ragada).

Meter: మధురగతి రగడ (madhuragati_ragada), a jāti meter.
Lines (పాదాలు): 2.
Every line: 4 gaṇas (8 to 16 aksharas):
  gaṇa 1: గా (UU) or స (IIU) or జ (IUI) or భ (UII) or నల (IIII)
  gaṇa 2: గా (UU) or స (IIU) or జ (IUI) or భ (UII) or నల (IIII)
  gaṇa 3: గా (UU) or స (IIU) or జ (IUI) or భ (UII) or నల (IIII)
  gaṇa 4: గా (UU) or స (IIU) or జ (IUI) or భ (UII) or నల (IIII)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 3. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 2 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 32 tokens · 2.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మ లడుమునుమరు మట లకకతో | `IIIIIIIIIIIIIIU` |
| 2 | నమగమునున్ ల మను మల లలకచుము | `IIIIUIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 30% · single-akshara words 20% · repeated lines 0 · mean token probability (geometric) 0.035 · model's first choice kept 12% · constraint overrode 28% · backtracks 0

<details><summary>Token probabilities (32 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.12 · `మ` 0.24 · `␣మ` 0.05 · `␣ల` 0.04 · `డు` 0.01 · `ము` 0.05 · `ను` 0.03 · `మ` 0.03 · `రు` 7.1e-3 · `␣మ` 0.02✱ · `ట` 7.8e-3✱ · `␣ల` 0.04✱ · `క` 0.05✱ · `క` 0.06✱ · `తో` 5.2e-4✱ · `⏎` 0.13✱ forced |
| 2 | `న` 0.13 · `మ` 0.32 · `గ` 4.9e-3 · `ము` 0.02 · `ను` 0.06 · `న్` 0.01 · `␣ల` 0.04 · `␣మ` 0.06 · `ను` 0.06 · `␣మ` 0.10✱ · `ల` 0.06 · `␣ల` 0.33 · `ల` 0.03 · `క` 0.22 · `చు` 4.8e-3 · `ము` 0.01✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 35 tokens · 3.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సమమ సిమము లంటె మదిమను జరము | `IIIIIIUIIIIIIII` |
| 2 | శమమశ లము సొకెడె మదుమను లరణ | `IIIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.046 · model's first choice kept 34% · constraint overrode 11% · backtracks 0

<details><summary>Token probabilities (35 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 4.4e-3 · `మ` 0.21 · `మ` 0.04 · `␣సి` 3.4e-3 · `మ` 0.04 · `ము` 0.05 · `␣ల` 0.06 · `ం` 0.12 · `ట` 0.02✱ · `ె` 0.12✱ · `␣మ` 0.05✱ · `ది` 0.09 · `మ` 0.07 · `ను` 0.04 · `␣జ` 0.05 · `ర` 0.01 · `ము` 0.02✱ · `⏎` 0.21 |
| 2 | `శ` 0.02 · `మ` 0.89 · `మ` 0.54 · `శ` 6.6e-3 · `␣ల` 0.15 · `ము` 0.11 · `␣సొ` 1.0e-3 · `కె` 6.3e-3 · `డ` 0.03 · `ె` 0.13 · `␣మ` 0.25 · `దు` 0.02 · `మ` 0.15 · `ను` 0.29 · `␣ల` 0.02 · `ర` 0.26 · `ణ` 1.7e-3 |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 32 tokens · 1.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మ లడుమునుమరు మట లకకతో | `IIIIIIIIIIIIIIU` |
| 2 | నమగమునున్ ల మను మల లలకచుము | `IIIIUIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 30% · single-akshara words 20% · repeated lines 0 · mean token probability (geometric) 0.035 · model's first choice kept 12% · constraint overrode 28% · backtracks 0

<details><summary>Token probabilities (32 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.12 · `మ` 0.24 · `␣మ` 0.05 · `␣ల` 0.04 · `డు` 0.01 · `ము` 0.05 · `ను` 0.03 · `మ` 0.03 · `రు` 7.1e-3 · `␣మ` 0.02✱ · `ట` 7.8e-3✱ · `␣ల` 0.04✱ · `క` 0.05✱ · `క` 0.06✱ · `తో` 5.2e-4✱ · `⏎` 0.13✱ forced |
| 2 | `న` 0.13 · `మ` 0.32 · `గ` 4.9e-3 · `ము` 0.02 · `ను` 0.06 · `న్` 0.01 · `␣ల` 0.04 · `␣మ` 0.06 · `ను` 0.06 · `␣మ` 0.10✱ · `ల` 0.06 · `␣ల` 0.33 · `ల` 0.03 · `క` 0.22 · `చు` 4.8e-3 · `ము` 0.01✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 33 tokens · 5.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జకర ల మనువన్ల కలలు దారియు | `IIIIIIUIIIIUII` |
| 2 | నుక జ జర ల మనుల కమ ల లె చేరె | `IIIIIIIIIIIIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 36% · repeated lines 0 · mean token probability (geometric) 0.062 · model's first choice kept 36% · constraint overrode 15% · backtracks 2

<details><summary>Token probabilities (33 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.09 · `క` 0.03 · `ర` 0.02 · `␣ల` 0.03 · `␣మ` 0.04 · `ను` 0.04 · `వ` 4.0e-3 · `న్` 0.02 · `ల` 0.03 · `␣` 9.4e-4✱ · `క` 9.4e-4✱ · `ల` 0.77 · `లు` 0.40 · `␣దా` 0.03 · `రి` 0.06 · `యు` 0.02 · `⏎` 5.4e-4✱ forced |
| 2 | `ను` 0.27 · `క` 0.06✱ · `␣జ` 0.31 · `␣జ` 0.07 · `ర` 0.38 · `␣ల` 0.33 · `␣మ` 0.16 · `ను` 0.22 · `ల` 0.09 · `␣క` 0.05✱ · `మ` 0.16 · `␣ల` 0.20 · `␣ల` 0.23 · `ె` 0.03 · `␣చే` 0.10 · `రె` 0.64 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 31 tokens · 5.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మామలవ మకక మల మలయ మాయ | `UIIIIIIIIIIIUI` |
| 2 | త్యా మయ మ మక మలల్ మల మ మాయ | `UIIIIIIUIIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 46% · single-akshara words 23% · repeated lines 0 · mean token probability (geometric) 0.055 · model's first choice kept 45% · constraint overrode 16% · backtracks 0

<details><summary>Token probabilities (31 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.10 · `మ` 0.13 · `ల` 0.06 · `వ` 0.01 · `␣మ` 0.14 · `క` 0.04 · `క` 0.05 · `␣మ` 0.33 · `ల` 0.04 · `␣మ` 0.09 · `ల` 0.04 · `య` 0.02 · `␣మ` 0.22 · `ాయ` 0.06 · `⏎` 0.65 |
| 2 | `త` 0.41 · `్యా` 9.4e-4✱ · `␣మ` 8.4e-4✱ · `య` 0.02 · `␣మ` 0.35 · `␣మ` 0.29 · `క` 0.38 · `␣మ` 0.47 · `ల` 0.45 · `ల` 0.31✱ · `్` 8.5e-8✱ · `␣మ` 0.08✱ · `ల` 0.32 · `␣మ` 0.12 · `␣మ` 0.14 · `ాయ` 0.08 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 25 tokens · 5.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాతి రమల రామున్ తంకన్ చే | `UIIIIUUUUU` |
| 2 | రాతాతి గమల సీతన్ లంకన్ | `UUIIIIUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 44% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.152 · model's first choice kept 60% · constraint overrode 24% · backtracks 0

<details><summary>Token probabilities (25 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.50 · `తి` 0.02 · `␣ర` 0.06 · `మ` 0.22 · `ల` 0.25✱ · `␣రా` 0.06 · `ము` 0.84 · `న్` 0.11✱ · `␣త` 4.5e-4✱ · `ంక` 0.24 · `న్` 0.03 · `␣చే` 0.05 · `⏎` 3.8e-5✱ forced |
| 2 | `రా` 8.2e-3✱ · `తా` 4.4e-4✱ · `తి` 0.62 · `␣గ` 0.88 · `మ` 0.98 · `ల` 0.95 · `␣సీ` 0.98 · `త` 0.90 · `న్` 0.94 · `␣ల` 0.82 · `ంక` 0.68 · `న్` 0.80 |

</details>

[↑ meters](#meters)

---

<a id="turagagati_ragada"></a>

## 25. తురగగతి రగడ (turagagati_ragada)

```text
Meter: తురగగతి రగడ (turagagati_ragada), a jāti meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas (16 to 24 aksharas):
  gaṇa 1: వ (IU) or హ (UI) or న (III)
  gaṇa 2: వ (IU) or హ (UI) or న (III)
  gaṇa 3: వ (IU) or హ (UI) or న (III)
  gaṇa 4: వ (IU) or హ (UI) or న (III)
  gaṇa 5: వ (IU) or హ (UI) or న (III)
  gaṇa 6: వ (IU) or హ (UI) or న (III)
  gaṇa 7: వ (IU) or హ (UI) or న (III)
  gaṇa 8: వ (IU) or హ (UI) or న (III)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 5. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter తురగగతి రగడ (turagagati_ragada).

Meter: తురగగతి రగడ (turagagati_ragada), a jāti meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas (16 to 24 aksharas):
  gaṇa 1: వ (IU) or హ (UI) or న (III)
  gaṇa 2: వ (IU) or హ (UI) or న (III)
  gaṇa 3: వ (IU) or హ (UI) or న (III)
  gaṇa 4: వ (IU) or హ (UI) or న (III)
  gaṇa 5: వ (IU) or హ (UI) or న (III)
  gaṇa 6: వ (IU) or హ (UI) or న (III)
  gaṇa 7: వ (IU) or హ (UI) or న (III)
  gaṇa 8: వ (IU) or హ (UI) or న (III)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 5. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 97 tokens · 11.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జకమ ల మనువన్ల గనుమల కృతుడల న లజకము నలి | `IIIIIIUIIIIIIIIIIIIIIII` |
| 2 | జకం మ ల జజాశల వను వికటము పరక లయను నలి | `IUIIIUIIIIIIIIIIIIIIII` |
| 3 | జకం మ ల మధనునుముమరసుక నజ ల లకము నలిజజ | `IUIIIIIIIIIIIIIIIIIIIII` |
| 4 | మ్య్య్య కునిల సము దమును దాటి లకకము నలిజనతితితుర | `IIIIIIIIIUIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 25% · repeated lines 0 · mean token probability (geometric) 0.053 · model's first choice kept 41% · constraint overrode 24% · backtracks 0

<details><summary>Token probabilities (97 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.10 · `క` 0.03 · `మ` 0.11 · `␣ల` 0.02 · `␣మ` 0.04 · `ను` 0.04 · `వ` 5.1e-3 · `న్` 0.01 · `ల` 0.02 · `␣గ` 6.0e-3 · `ను` 0.04 · `మ` 0.03 · `ల` 0.02✱ · `␣కృ` 6.2e-4✱ · `తు` 0.21 · `డ` 0.57 · `ల` 8.5e-3 · `␣న` 9.6e-3 · `␣ల` 0.04✱ · `జ` 0.09 · `క` 0.08 · `ము` 0.18✱ · `␣న` 4.4e-3✱ · `లి` 9.0e-4✱ · `⏎` 0.09✱ forced |
| 2 | `జ` 0.19 · `కం` 1.8e-3✱ · `␣మ` 0.22 · `␣ల` 0.65 · `␣జ` 0.15 · `జా` 1.7e-3 · `శ` 0.01✱ · `ల` 0.36 · `␣వ` 0.03 · `ను` 0.04 · `␣వి` 4.9e-3 · `క` 0.02✱ · `ట` 0.61 · `ము` 0.17 · `␣పర` 1.7e-4 · `క` 0.05 · `␣ల` 0.09 · `య` 0.03 · `ను` 0.05 · `␣న` 0.10 · `లి` 0.53 · `⏎` 0.84 |
| 3 | `జ` 0.86 · `కం` 0.38 · `␣మ` 0.54 · `␣ల` 0.79 · `␣మ` 0.28 · `ధ` 0.01 · `ను` 0.04 · `ను` 0.06 · `ము` 0.03 · `మ` 0.03 · `ర` 0.01 · `సు` 4.4e-3 · `క` 0.03✱ · `␣న` 0.08 · `జ` 0.01 · `␣ల` 0.13 · `␣ల` 0.12 · `క` 0.23 · `ము` 0.67 · `␣న` 0.72 · `లి` 0.54 · `జ` 4.2e-4✱ · `జ` 0.97 · `⏎` 2.3e-3✱ forced |
| 4 | `␣మ` 0.71 · `్య` 2.7e-3✱ · `్య` 1.3e-4✱ · `్య` 4.3e-4✱ · `␣` 9.8e-4✱ · `కుని` 3.6e-7✱ · `ల` 0.98 · `␣స` 0.98 · `ము` 0.98 · `␣ద` 2.1e-3✱ · `ము` 0.99 · `ను` 0.99 · `␣దా` 0.96 · `టి` 0.89 · `␣ల` 0.96 · `క` 3.1e-3✱ · `క` 0.74 · `ము` 0.89 · `␣న` 0.80 · `లి` 0.84 · `జ` 0.06✱ · `న` 0.69 · `తి` 0.89 · `తి` 0.03✱ · `తు` 0.61 · `ర` 0.05✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 101 tokens · 17.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కల్లి మ మమ మ త ల లో శ జగ్ ల్ల కొమ న్నమ త ల ప్రకతి | `UIIIIIIIUIUIIIIIIIIII` |
| 2 | మల్లి మ మ ల లో శ జగ్ ల్ల లొమ్ ల్ల అమతివతవ మల్లి | `UIIIIUIUIUIIIIIIIUI` |
| 3 | మల్లి ల లో శ జగ జగ లలల్ ల్ల మతివవతి లల లో | `UIIUIIIIIIUIIIIIIIIU` |
| 4 | క ల్లా ల ల ల ల లతి లతి లమ ల్లా ల ల ల ల ల లలనును | `IUIIIIIIIIIIUIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 67% · repeated lines 0 · mean token probability (geometric) 0.046 · model's first choice kept 39% · constraint overrode 36% · backtracks 0

<details><summary>Token probabilities (101 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.06 · `ల్లి` 0.09 · `␣మ` 0.07 · `␣మ` 0.09 · `మ` 0.05 · `␣మ` 0.06 · `␣త` 0.01 · `␣ల` 0.05 · `␣లో` 0.02 · `␣శ` 3.7e-3 · `␣జగ` 2.6e-3 · `్` 8.2e-6✱ · `␣ల` 0.04✱ · `్` 1.8e-5✱ · `ల` 0.05✱ · `␣క` 0.02 · `ొ` 0.02 · `మ` 0.04 · `␣` 0.02 · `న్న` 0.03✱ · `మ` 4.5e-3✱ · `␣త` 0.01✱ · `␣ల` 0.03✱ · `␣ప్ర` 1.3e-3✱ · `క` 0.38 · `తి` 0.08✱ · `⏎` 0.03✱ forced |
| 2 | `మ` 0.28 · `ల్లి` 0.17✱ · `␣మ` 0.74 · `␣మ` 0.19 · `␣ల` 0.72 · `␣లో` 0.78 · `␣శ` 0.70 · `␣జగ` 0.96 · `్` 0.87 · `␣ల` 0.94 · `్` 0.77 · `ల` 0.87 · `␣ల` 0.16 · `ొ` 0.67 · `మ` 0.48 · `్` 1.4e-5✱ · `␣ల` 0.20✱ · `్` 3.0e-5✱ · `ల` 0.10✱ · `␣అమ` 0.02 · `తి` 0.48 · `వ` 1.2e-3✱ · `త` 0.44 · `వ` 6.0e-3✱ · `␣మ` 0.28 · `ల్లి` 0.61 · `⏎` 0.08✱ forced |
| 3 | `మ` 0.15 · `ల్లి` 0.27 · `␣ల` 0.21 · `␣లో` 0.18 · `␣శ` 0.08 · `␣జగ` 0.22 · `␣జగ` 0.16 · `␣ల` 0.42 · `ల` 0.13 · `ల` 0.46 · `్` 2.3e-6✱ · `␣ల` 0.07✱ · `్` 8.6e-4✱ · `ల` 0.20✱ · `␣మ` 0.10 · `తి` 0.18 · `వ` 0.08✱ · `వ` 0.41 · `తి` 0.34 · `␣ల` 0.19 · `ల` 0.03 · `␣లో` 0.03✱ · `⏎` 0.21 forced |
| 4 | `క` 0.05 · `␣ల` 0.10 · `్లా` 1.5e-6✱ · `␣ల` 0.19 · `␣ల` 0.24 · `␣ల` 0.27 · `␣ల` 0.20 · `␣ల` 0.17 · `తి` 0.07 · `␣ల` 0.05 · `తి` 0.72 · `␣ల` 0.74 · `మ` 0.89 · `␣ల` 0.02✱ · `్లా` 9.3e-6✱ · `␣ల` 0.20✱ · `␣ల` 0.05✱ · `␣ల` 0.32 · `␣ల` 0.19✱ · `␣ల` 0.08✱ · `␣ల` 6.2e-3✱ · `ల` 7.3e-4✱ · `ను` 3.1e-3✱ · `ను` 0.01✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 88 tokens · 50.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామముల్లిడమక సీతనున్ మరుగుటె రాము జాయ | `UIUIIIIUIUIIIIUIUI` |
| 2 | దూముల సీతనున్ వెతెను రాము నడ ల లకను దుగజ | `UIIUIUIIIUIIIIIIIIII` |
| 3 | శౌమ జయముడు వెల్లెనును సీత్ మ మరుగుటెలే సచికి | `UIIIIIUIIIUIIIIIUIII` |
| 4 | గీము మీరు అడిగిన సంతుర్ మతి రగడ జాతి నియ | `UIUIIIIIUUIIIIIUIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 32% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.120 · model's first choice kept 61% · constraint overrode 27% · backtracks 30

<details><summary>Token probabilities (88 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.96 · `మ` 0.81 · `ము` 0.07 · `ల్లి` 0.64 · `డ` 9.8e-3 · `మ` 0.07 · `క` 0.02 · `␣సీ` 0.93 · `త` 0.96 · `ను` 0.92 · `న్` 6.2e-3✱ · `␣మ` 1.3e-3✱ · `రుగు` 0.04✱ · `ట` 0.95 · `ె` 0.91 · `␣రా` 0.08✱ · `ము` 0.67 · `␣జ` 0.94 · `ాయ` 0.02 · `⏎` 0.03✱ forced |
| 2 | `ద` 0.02 · `ూ` 0.04✱ · `ముల` 2.9e-4✱ · `␣సీ` 0.84 · `త` 0.82 · `ను` 0.40 · `న్` 0.86 · `␣వె` 0.83 · `త` 0.24 · `ె` 0.82 · `ను` 0.45 · `␣రా` 0.21 · `ము` 0.21✱ · `␣న` 0.06 · `డ` 0.80 · `␣ల` 0.89 · `␣ల` 7.5e-4✱ · `క` 0.83 · `ను` 0.57 · `␣దు` 0.02✱ · `గ` 0.03 · `జ` 0.42 · `⏎` 0.96 |
| 3 | `శ` 0.18 · `ౌ` 0.97 · `మ` 0.13✱ · `␣జ` 0.25 · `య` 0.78 · `ము` 0.87 · `డు` 0.98 · `␣వె` 0.86 · `ల్ల` 0.96 · `ె` 0.93 · `ను` 0.47 · `ను` 0.21 · `␣సీ` 0.96 · `త` 0.96 · `్` 1.9e-8✱ · `␣మ` 0.03✱ · `␣మ` 0.95 · `రుగు` 0.72 · `ట` 0.97 · `ె` 0.93 · `లే` 6.6e-4✱ · `␣స` 1.0e-3✱ · `చి` 0.29 · `కి` 8.4e-3✱ · `⏎` 0.16✱ forced |
| 4 | `గ` 0.02✱ · `ీ` 0.02✱ · `ము` 9.6e-3✱ · `␣మీరు` 0.99 · `␣అ` 1.00 · `డి` 0.97 · `గ` 1.00 · `ిన` 0.99 · `␣సం` 3.9e-6✱ · `తు` 0.87 · `ర` 9.1e-3✱ · `్` 1.6e-7✱ · `␣మ` 9.8e-4✱ · `తి` 0.98 · `␣ర` 1.00 · `గ` 1.00 · `డ` 1.00 · `␣జా` 0.96 · `తి` 0.99 · `␣నియ` 1.00 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 95 tokens · 9.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మ లడుమునుమరు మ హన్కకను లో శదాముదమున్ | `IIIIIIIIIIUIIIUIUIIU` |
| 2 | మమ హ మె పును మక ల వ మ హ ల మ మను లాన లడను లక | `IIIIIIIIIIIIIIIIUIIIIII` |
| 3 | మమ లడునునురు మమ హ మకను ము శదాముదైన్ మమమ హ | `IIIIIIIIIIIIIIIUIUIIII` |
| 4 | పు మ మక ల వ మ హ ల మ మను లమ లడను లకమండిదిప | `IIIIIIIIIIIIIIIIIIIUIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 16% · single-akshara words 50% · repeated lines 0 · mean token probability (geometric) 0.076 · model's first choice kept 46% · constraint overrode 21% · backtracks 0

<details><summary>Token probabilities (95 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.08 · `మ` 0.23 · `␣మ` 0.03 · `␣ల` 0.01 · `డు` 0.01 · `ము` 0.04 · `ను` 0.04 · `మ` 0.04 · `రు` 0.01 · `␣మ` 0.03 · `␣హ` 0.02 · `న్` 0.02 · `క` 0.03✱ · `క` 0.03✱ · `ను` 0.04 · `␣లో` 1.5e-3 · `␣శ` 4.4e-3✱ · `దా` 3.1e-4✱ · `ము` 0.01✱ · `ద` 0.04✱ · `ము` 0.30 · `న్` 0.02✱ · `⏎` 0.66 |
| 2 | `మ` 0.55 · `మ` 0.08✱ · `␣హ` 7.4e-3 · `␣మె` 2.9e-3 · `␣పు` 2.1e-3 · `ను` 0.07 · `␣మ` 0.09 · `క` 0.02 · `␣ల` 0.02 · `␣వ` 0.01 · `␣మ` 0.07 · `␣హ` 0.06 · `␣ల` 0.06 · `␣మ` 8.8e-3✱ · `␣మ` 0.02 · `ను` 0.05 · `␣ల` 0.29 · `ాన` 1.5e-3 · `␣ల` 0.09 · `డ` 0.02 · `ను` 7.7e-3✱ · `␣ల` 1.5e-3✱ · `క` 0.72 · `⏎` 4.6e-3✱ forced |
| 3 | `మ` 0.46 · `మ` 0.01✱ · `␣ల` 0.29 · `డు` 0.17 · `ను` 0.54 · `ను` 0.11 · `రు` 0.38 · `␣మ` 0.53 · `మ` 0.05 · `␣హ` 0.59 · `␣మ` 0.13 · `క` 0.75 · `ను` 0.65 · `␣ము` 0.01✱ · `␣శ` 0.51 · `దా` 0.50 · `ము` 0.45 · `ద` 0.54 · `ై` 2.2e-3 · `న్` 0.36 · `␣మ` 9.1e-3✱ · `మ` 0.77 · `మ` 0.93 · `␣హ` 0.92 · `⏎` 7.3e-4✱ forced |
| 4 | `పు` 0.15 · `␣మ` 0.09✱ · `␣మ` 0.41 · `క` 0.50 · `␣ల` 0.73 · `␣వ` 0.53 · `␣మ` 0.55 · `␣హ` 0.75 · `␣ల` 0.57 · `␣మ` 0.30 · `␣మ` 0.29 · `ను` 0.54 · `␣ల` 0.75 · `మ` 5.7e-4✱ · `␣ల` 0.69 · `డ` 0.83 · `ను` 0.81 · `␣ల` 0.48 · `క` 2.3e-3✱ · `మ` 0.73 · `ండి` 0.41 · `ది` 0.01✱ · `ప` 0.76 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 97 tokens · 16.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మల గురు జను మ ల లమల మల ల ల లకమునుకమ్మ | `IIIIIIIIIIIIIIIIIIIIIUI` |
| 2 | ల మరు జను మల లమల మల లం లకమునునుమ మల గురు | `IIIIIIIIIIIIUIIIIIIIIII` |
| 3 | ను మల లమల మల ల ల ల లముమునునమ మల గురుమమన | `IIIIIIIIIIIIIIIIIIIIIIII` |
| 4 | ల మ ల ల జల లం ల ల లముముమువకకనులుతముకకక | `IIIIIIUIIIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 38% · single-akshara words 42% · repeated lines 0 · mean token probability (geometric) 0.140 · model's first choice kept 57% · constraint overrode 26% · backtracks 0

<details><summary>Token probabilities (97 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.08 · `మ` 0.23 · `␣మ` 0.03 · `ల` 0.74 · `␣గు` 0.03 · `రు` 0.05 · `␣జ` 0.05 · `ను` 0.02 · `␣మ` 0.20 · `␣ల` 0.09 · `␣ల` 0.09 · `మ` 0.03 · `ల` 0.04 · `␣మ` 0.06✱ · `ల` 0.11 · `␣ల` 0.24 · `␣ల` 0.18 · `␣ల` 0.13 · `క` 0.20 · `ము` 0.29 · `ను` 1.4e-3✱ · `క` 0.83 · `మ్మ` 1.1e-3 · `⏎` 5.0e-6✱ forced |
| 2 | `ల` 0.64 · `␣మ` 3.4e-3✱ · `రు` 0.77 · `␣జ` 0.95 · `ను` 0.94 · `␣మ` 0.86 · `ల` 0.93 · `␣ల` 0.90 · `మ` 0.72 · `ల` 0.94 · `␣మ` 0.93 · `ల` 0.95 · `␣ల` 0.40 · `ం` 0.67 · `␣ల` 0.56 · `క` 0.40 · `ము` 0.72 · `ను` 0.65 · `ను` 0.01✱ · `మ` 0.33 · `␣మ` 0.87 · `ల` 0.94 · `␣గు` 0.81 · `రు` 0.91 · `⏎` 0.04✱ forced |
| 3 | `ను` 0.88 · `␣మ` 0.87 · `ల` 0.85 · `␣ల` 0.82 · `మ` 0.63 · `ల` 0.69 · `␣మ` 0.47 · `ల` 0.71 · `␣ల` 0.82 · `␣ల` 0.05✱ · `␣ల` 0.91 · `␣ల` 0.09 · `ము` 0.83 · `ము` 0.04✱ · `ను` 0.08✱ · `న` 0.15✱ · `మ` 0.69 · `␣మ` 0.62 · `ల` 0.91 · `␣గు` 0.51 · `రు` 0.71 · `మ` 0.02✱ · `మన` 5.6e-3 · `⏎` 9.5e-3✱ forced |
| 4 | `ల` 0.54 · `␣మ` 0.16✱ · `␣ల` 7.8e-3 · `␣ల` 0.35 · `␣జ` 0.08 · `ల` 0.57 · `␣ల` 0.53 · `ం` 0.16 · `␣ల` 0.55 · `␣ల` 0.42 · `␣ల` 0.22 · `ము` 0.26 · `ము` 0.18✱ · `ము` 1.1e-3✱ · `వ` 2.1e-3✱ · `క` 5.0e-4✱ · `క` 0.03✱ · `ను` 0.02✱ · `లు` 2.8e-3✱ · `త` 9.2e-4✱ · `ము` 0.02✱ · `క` 1.7e-3✱ · `క` 0.05✱ · `క` 8.6e-3✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 90 tokens · 13.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తకమల మమత మమకమును మృకుండా మరువదు వంటి | `IIIIIIIIIIIIIUUIIIIUI` |
| 2 | కకల భక్తి కమలము క కల కలువ మమకముకకలా | `IIIUIIIIIIIIIIIIIIIIIU` |
| 3 | మకమల మమక మమమతిమనుకక మ మమ మమమ మమక | `IIIIIIIIIIIIIIIIIIIIIIII` |
| 4 | క్ష్య్యుకు తురగగతి రగడ జాతికి నియమాలు పాటిస్తు | `IIIIIIIIIIUIIIIUIUUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 23% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.118 · model's first choice kept 54% · constraint overrode 21% · backtracks 0

<details><summary>Token probabilities (90 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.25 · `క` 0.05 · `మ` 0.07 · `ల` 0.04 · `␣మ` 0.06 · `మ` 0.28 · `త` 0.60 · `␣మ` 0.15 · `మ` 0.31 · `క` 0.16 · `ము` 0.03 · `ను` 0.02 · `␣మ` 0.32 · `ృ` 0.04✱ · `కుండా` 4.2e-4✱ · `␣మ` 0.36 · `రు` 0.10 · `వ` 0.48 · `దు` 0.31 · `␣వంటి` 1.5e-5✱ · `⏎` 0.02✱ forced |
| 2 | `క` 0.95 · `క` 4.4e-3✱ · `ల` 0.88 · `␣భ` 0.98 · `క్తి` 0.95 · `␣క` 0.80 · `మ` 0.39 · `ల` 0.80 · `ము` 0.77 · `␣క` 0.48 · `␣క` 0.41 · `ల` 0.03 · `␣క` 0.04✱ · `లు` 0.05 · `వ` 0.11 · `␣మ` 0.03 · `మ` 0.10 · `క` 0.14✱ · `ము` 0.02✱ · `క` 0.25 · `క` 0.17 · `లా` 5.8e-3✱ · `⏎` 0.46 |
| 3 | `మ` 0.10 · `క` 0.27 · `మ` 0.14 · `ల` 0.04 · `␣మ` 0.69 · `మ` 0.55 · `క` 0.06 · `␣మ` 0.37 · `మ` 0.40 · `మ` 0.17 · `తి` 0.06 · `మ` 0.10 · `ను` 0.02 · `క` 0.03✱ · `క` 0.15 · `␣మ` 0.62 · `␣మ` 0.15 · `మ` 0.18 · `␣మ` 0.78 · `మ` 0.79 · `మ` 0.15 · `␣మ` 0.49 · `మ` 0.38 · `క` 0.16 · `⏎` 0.18✱ forced |
| 4 | `క్ష` 0.02✱ · `్య` 4.8e-4✱ · `్య` 3.0e-4✱ · `ు` 5.5e-3✱ · `కు` 1.2e-3✱ · `␣తు` 0.98 · `రగ` 0.79 · `గ` 0.99 · `తి` 0.99 · `␣ర` 0.95 · `గ` 0.97 · `డ` 0.99 · `␣జా` 0.93 · `తి` 1.00 · `కి` 8.2e-4✱ · `␣నియ` 1.00 · `మా` 0.36 · `లు` 0.24✱ · `␣పా` 1.00 · `టి` 1.00 · `స్తు` 2.2e-4✱ |

</details>

[↑ meters](#meters)

---

<a id="hayapracara_ragada"></a>

## 26. హయప్రచార రగడ (hayapracara_ragada)

```text
Meter: హయప్రచార రగడ (hayapracara_ragada), a jāti meter.
Lines (పాదాలు): 2.
Every line: 4 gaṇas (8 to 12 aksharas):
  gaṇa 1: వ (IU) or హ (UI) or న (III)
  gaṇa 2: వ (IU) or హ (UI) or న (III)
  gaṇa 3: వ (IU) or హ (UI) or న (III)
  gaṇa 4: వ (IU) or హ (UI) or న (III)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 3. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter హయప్రచార రగడ (hayapracara_ragada).

Meter: హయప్రచార రగడ (hayapracara_ragada), a jāti meter.
Lines (పాదాలు): 2.
Every line: 4 gaṇas (8 to 12 aksharas):
  gaṇa 1: వ (IU) or హ (UI) or న (III)
  gaṇa 2: వ (IU) or హ (UI) or న (III)
  gaṇa 3: వ (IU) or హ (UI) or న (III)
  gaṇa 4: వ (IU) or హ (UI) or న (III)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 3. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 2 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 25 tokens · 3.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జనుమతు మనువిన జను పకు | `IIIIIIIIIIII` |
| 2 | లన వను లకునును నకుతుడు | `IIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 38% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.033 · model's first choice kept 32% · constraint overrode 16% · backtracks 0

<details><summary>Token probabilities (25 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.17 · `ను` 0.50 · `మ` 0.18 · `తు` 0.02 · `␣మ` 0.03 · `ను` 0.05 · `వ` 4.5e-3 · `ిన` 2.9e-3✱ · `␣జ` 0.51 · `ను` 0.09 · `␣ప` 2.4e-3 · `కు` 3.9e-3 · `⏎` 4.4e-4✱ forced |
| 2 | `␣ల` 0.02 · `న` 5.6e-3✱ · `␣వ` 5.1e-3 · `ను` 0.04 · `␣ల` 0.10 · `కు` 0.01 · `ను` 0.16 · `ను` 0.15 · `␣న` 0.04 · `కు` 0.05 · `తు` 2.9e-3✱ · `డు` 0.18 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 24 tokens · 2.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తతిలమలముమ తల్ల ప్రేమ్ | `IIIIIIIUIU` |
| 2 | మతిని మతి మక తే మనన | `IIIIIIIUIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 38% · single-akshara words 25% · repeated lines 0 · mean token probability (geometric) 0.023 · model's first choice kept 21% · constraint overrode 25% · backtracks 0

<details><summary>Token probabilities (24 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.21 · `తి` 0.02 · `ల` 0.03 · `మ` 0.05 · `ల` 0.03 · `ము` 0.03 · `మ` 0.06 · `␣త` 0.02✱ · `ల్ల` 0.12 · `␣ప్రేమ` 0.01 · `్` 1.9e-9✱ · `⏎` 0.13 forced |
| 2 | `మ` 0.56 · `తి` 0.52 · `ని` 0.03 · `␣మ` 0.10 · `తి` 0.43 · `␣మ` 0.07 · `క` 0.03 · `␣త` 0.03✱ · `ే` 5.5e-3 · `␣మ` 0.06✱ · `న` 0.02✱ · `న` 0.02✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 25 tokens · 2.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జనుమతు మనువిన జను పకు | `IIIIIIIIIIII` |
| 2 | లన వను లకునును నకుతుడు | `IIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 38% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.033 · model's first choice kept 32% · constraint overrode 16% · backtracks 0

<details><summary>Token probabilities (25 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.17 · `ను` 0.50 · `మ` 0.18 · `తు` 0.02 · `␣మ` 0.03 · `ను` 0.05 · `వ` 4.5e-3 · `ిన` 2.9e-3✱ · `␣జ` 0.51 · `ను` 0.09 · `␣ప` 2.4e-3 · `కు` 3.9e-3 · `⏎` 4.4e-4✱ forced |
| 2 | `␣ల` 0.02 · `న` 5.6e-3✱ · `␣వ` 5.1e-3 · `ను` 0.04 · `␣ల` 0.10 · `కు` 0.01 · `ను` 0.16 · `ను` 0.15 · `␣న` 0.04 · `కు` 0.05 · `తు` 2.9e-3✱ · `డు` 0.18 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 25 tokens · 12.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాము ల జత లయ్ మనము లె | `UIIIIUIIII` |
| 2 | దేమ ల జత లయ్ మము లె డు | `UIIIIUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 31% · single-akshara words 54% · repeated lines 0 · mean token probability (geometric) 0.085 · model's first choice kept 64% · constraint overrode 28% · backtracks 9

<details><summary>Token probabilities (25 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.71 · `ము` 0.54 · `␣ల` 0.69 · `␣జ` 0.17 · `త` 0.55 · `␣ల` 0.96 · `య` 0.97 · `్` 5.1e-7✱ · `␣మన` 3.7e-3✱ · `ము` 0.76 · `␣లె` 2.5e-4✱ · `⏎` 0.56 |
| 2 | `దే` 8.5e-3 · `మ` 0.01✱ · `␣ల` 0.89 · `␣జ` 0.95 · `త` 0.76 · `␣ల` 0.90 · `య` 0.95 · `్` 0.98 · `␣మ` 0.03✱ · `ము` 0.59 · `␣లె` 0.63 · `␣` 2.3e-3✱ · `డు` 2.7e-4✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 23 tokens · 3.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శము ల ల సీము మర ల చే | `IIIIUIIIIU` |
| 2 | శమ లము లల జామ జర ల | `IIIIIIUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 54% · single-akshara words 38% · repeated lines 0 · mean token probability (geometric) 0.057 · model's first choice kept 39% · constraint overrode 22% · backtracks 0

<details><summary>Token probabilities (23 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.28 · `ము` 0.07 · `␣ల` 0.08✱ · `␣ల` 0.07 · `␣సీ` 0.08 · `ము` 0.06 · `␣` 2.1e-3✱ · `మ` 1.3e-3✱ · `ర` 0.08 · `␣ల` 0.19 · `␣చే` 0.01 · `⏎` 9.3e-4✱ forced |
| 2 | `శ` 0.12 · `మ` 0.15 · `␣ల` 0.38 · `ము` 0.03 · `␣ల` 0.27 · `ల` 0.02 · `␣జా` 0.01✱ · `మ` 0.12 · `␣జ` 0.02 · `ర` 0.15 · `␣ల` 0.22 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 21 tokens · 4.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జనుమతు మను జముముల దా | `IIIIIIIIIIU` |
| 2 | జనక సుత ల లనకు చేరు | `IIIIIIIIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 44% · single-akshara words 22% · repeated lines 0 · mean token probability (geometric) 0.115 · model's first choice kept 38% · constraint overrode 19% · backtracks 0

<details><summary>Token probabilities (21 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.17 · `ను` 0.50 · `మ` 0.18 · `తు` 0.02 · `␣మ` 0.03 · `ను` 0.05 · `␣జ` 0.56 · `ము` 0.30 · `ము` 0.11 · `ల` 0.02 · `␣దా` 0.15 · `⏎` 4.2e-4✱ forced |
| 2 | `జ` 0.09 · `న` 0.14✱ · `క` 0.09 · `␣సు` 0.44 · `త` 0.89 · `␣ల` 0.92 · `␣ల` 0.45✱ · `నకు` 1.1e-3✱ · `␣చేరు` 0.03 |

</details>

[↑ meters](#meters)

---

<a id="seesamu"></a>

## 27. సీసము (seesamu)

```text
Meter: సీసము (seesamu), an upajāti meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas (22 to 30 aksharas):
  gaṇa 1: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 2: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 3: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 4: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 5: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 6: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 7: న (III) or హ (UI)
  gaṇa 8: న (III) or హ (UI)
Alternatively, every line in the all-laghu form:
Every line: 8 gaṇas: నలల నలల నలల నలల నలల నలల న న, i.e. IIIII IIIII IIIII IIIII IIIII IIIII III III (36 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 3, and the first akshara of gaṇa 5 with the first akshara of gaṇa 7. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): not required.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter సీసము (seesamu).

Meter: సీసము (seesamu), an upajāti meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas (22 to 30 aksharas):
  gaṇa 1: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 2: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 3: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 4: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 5: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 6: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 7: న (III) or హ (UI)
  gaṇa 8: న (III) or హ (UI)
Alternatively, every line in the all-laghu form:
Every line: 8 gaṇas: నలల నలల నలల నలల నలల నలల న న, i.e. IIIII IIIII IIIII IIIII IIIII IIIII III III (36 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 3, and the first akshara of gaṇa 5 with the first akshara of gaṇa 7. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): not required.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 125 tokens · 11.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మమురాగత సమణ వము న సీడు ల లకు వెడిసెనుమమమామశల సమసమ | `IIUIIIIIIIIUIIIIIIIIIIUIIIIIII` |
| 2 | శమగ కూముపుమ మను మతమినువరణండ ల లనునసరమమళ ససమమ | `IIIUIIIIIIIIIIIUIIIIIIIIIIIIII` |
| 3 | మము ల కావగ పనము మె జ సీనునును లముమునులనునుమనస మమసమము | `IIIUIIIIIIIUIIIIIIIIIIIIIIIIII` |
| 4 | మమ జ జ మల వము న మముడు లంకకు వెడిసనునిమమశల లమసముము | `IIIIIIIIIIIIUIIIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 23% · single-akshara words 26% · repeated lines 0 · mean token probability (geometric) 0.058 · model's first choice kept 42% · constraint overrode 13% · backtracks 0

<details><summary>Token probabilities (125 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.03 · `ము` 0.06 · `రా` 0.02 · `గ` 8.6e-3 · `త` 0.03 · `␣స` 0.02 · `మణ` 4.3e-4 · `␣వ` 7.9e-3 · `ము` 6.7e-3✱ · `␣న` 0.05 · `␣సీ` 0.02 · `డు` 5.4e-3 · `␣ల` 0.32 · `␣ల` 0.01✱ · `కు` 0.51 · `␣వె` 0.30 · `డి` 9.0e-3 · `సె` 0.13 · `ను` 0.31 · `మ` 0.18✱ · `మ` 0.33 · `మా` 0.02 · `మ` 0.08 · `శ` 0.03 · `ల` 0.02✱ · `␣` 7.1e-3✱ · `స` 0.06 · `మ` 0.12 · `స` 0.02✱ · `మ` 0.05✱ · `⏎` 0.20 forced |
| 2 | `శ` 0.06 · `మ` 0.35 · `గ` 0.02 · `␣కూ` 6.8e-4 · `ము` 0.05 · `పు` 8.5e-3 · `మ` 0.07 · `␣మ` 0.03 · `ను` 0.04 · `␣మ` 0.04✱ · `త` 0.12 · `మి` 2.3e-3 · `ను` 0.11 · `వ` 7.7e-3 · `ర` 0.02 · `ణ` 4.4e-3 · `ండ` 2.6e-3 · `␣ల` 0.02 · `␣ల` 0.02 · `ను` 0.05 · `న` 0.02 · `స` 0.02 · `ర` 0.01 · `మ` 0.09 · `మ` 0.10 · `ళ` 0.01✱ · `␣` 0.12 · `స` 0.25 · `స` 0.28 · `మ` 0.27 · `మ` 0.28 · `⏎` 0.21 |
| 3 | `మ` 0.18 · `ము` 0.04 · `␣ల` 0.03 · `␣కా` 1.6e-3 · `వ` 0.02 · `గ` 0.02 · `␣ప` 6.1e-3 · `న` 0.02 · `ము` 0.08 · `␣మె` 2.0e-3✱ · `␣జ` 0.12 · `␣సీ` 0.22 · `ను` 0.12 · `ను` 0.10 · `ను` 0.10 · `␣ల` 0.13 · `ము` 0.04 · `ము` 0.06 · `ను` 0.08 · `ల` 0.02 · `ను` 0.06 · `ను` 0.05 · `మ` 0.09 · `న` 0.04 · `స` 0.09 · `␣` 0.38 · `మ` 0.05✱ · `మ` 0.89 · `స` 0.49 · `మ` 0.79 · `ము` 9.0e-5✱ · `⏎` 0.03✱ forced |
| 4 | `మ` 0.60 · `మ` 0.15 · `␣జ` 0.36 · `␣జ` 0.17 · `␣మ` 0.03 · `ల` 0.04 · `␣వ` 0.89 · `ము` 0.87 · `␣న` 0.82 · `␣మ` 3.2e-4✱ · `ము` 0.78 · `డు` 0.93 · `␣ల` 0.86 · `ంక` 0.72 · `కు` 0.83 · `␣వె` 0.43 · `డి` 0.55 · `స` 0.08 · `ను` 0.59 · `ని` 9.7e-3 · `మ` 0.62 · `మ` 0.39 · `శ` 0.21 · `ల` 0.34 · `␣` 0.40 · `ల` 4.1e-3✱ · `మ` 0.70 · `స` 0.85 · `ము` 0.55 · `ము` 5.0e-3✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 130 tokens · 14.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మనమ మను లోరు మమాద కకతోయి కడము నిర మమకతొ డు కమలము | `IIIIIIIUIIUIIIUIIIIIIIIIIIIIII` |
| 2 | కమ ముక మనుమమను మరు మమాద కకనుయ కడము నిర మనకతొ డు క | `IIIIIIIIIIIIUIIIIIIIIIIIIIIII` |
| 3 | లముతతమ మనమ మము లోరు మమద కకనుయ కడము నిర మనకతొ డు క | `IIIIIIIIIIUIIIIIIIIIIIIIIIIIII` |
| 4 | లమునుతమముక మనుమమ మరు మమద కకనుయ కడము నిరకనకతొ డు | `IIIIIIIIIIIIIIIIIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 22% · single-akshara words 15% · repeated lines 0 · mean token probability (geometric) 0.185 · model's first choice kept 65% · constraint overrode 22% · backtracks 0

<details><summary>Token probabilities (130 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.19 · `మ` 0.12 · `␣మ` 0.07 · `న` 0.02 · `మ` 0.05 · `␣మ` 0.06 · `ను` 0.02 · `␣లో` 0.03 · `రు` 7.1e-3 · `␣మ` 0.04✱ · `మా` 0.01 · `ద` 7.9e-3✱ · `␣క` 0.01✱ · `క` 0.04✱ · `తో` 1.8e-3✱ · `యి` 5.0e-4✱ · `␣క` 9.0e-3✱ · `డ` 0.04 · `ము` 0.09✱ · `␣ని` 2.0e-3✱ · `ర` 0.05 · `␣మ` 0.05 · `మ` 0.15✱ · `క` 0.09 · `త` 0.04 · `ొ` 3.8e-3✱ · `␣` 0.01✱ · `డు` 3.9e-3✱ · `␣క` 0.04✱ · `మ` 0.33 · `ల` 0.09✱ · `ము` 0.41 · `⏎` 0.30 |
| 2 | `క` 0.12✱ · `మ` 0.16✱ · `␣ము` 3.1e-3 · `క` 0.05 · `␣మ` 0.57 · `ను` 0.04 · `మ` 0.50 · `మ` 0.04 · `ను` 0.51 · `␣మ` 0.02✱ · `రు` 0.38 · `␣మ` 0.48 · `మా` 0.56 · `ద` 0.58 · `␣క` 0.68 · `క` 0.85 · `ను` 2.2e-3✱ · `య` 0.07 · `␣క` 0.70 · `డ` 0.97 · `ము` 0.93 · `␣ని` 0.89 · `ర` 0.97 · `␣మ` 0.94 · `న` 1.2e-3✱ · `క` 0.97 · `త` 0.95 · `ొ` 0.97 · `␣` 0.99 · `డు` 0.98 · `␣క` 0.72 · `⏎` 4.5e-5✱ forced |
| 3 | `ల` 0.84 · `ము` 0.89 · `త` 9.7e-4✱ · `త` 0.97 · `మ` 0.96 · `␣మ` 0.95 · `న` 0.98 · `మ` 0.93 · `␣మ` 0.98 · `ము` 9.3e-4✱ · `␣లో` 0.91 · `రు` 0.73 · `␣మ` 0.97 · `మ` 5.6e-3✱ · `ద` 0.84 · `␣క` 0.89 · `క` 0.96 · `ను` 0.03✱ · `య` 0.74 · `␣క` 0.86 · `డ` 0.99 · `ము` 0.99 · `␣ని` 0.93 · `ర` 0.99 · `␣మ` 0.97 · `న` 0.14✱ · `క` 0.97 · `త` 0.99 · `ొ` 0.99 · `␣` 0.96 · `డు` 0.96 · `␣క` 0.87 · `⏎` 2.9e-3✱ forced |
| 4 | `ల` 0.96 · `ము` 0.97 · `ను` 2.0e-3✱ · `త` 0.56 · `మ` 0.59 · `ము` 0.15 · `క` 0.72 · `␣మ` 0.68 · `ను` 0.63 · `మ` 0.70 · `మ` 0.57 · `␣మ` 0.79 · `రు` 0.74 · `␣మ` 0.79 · `మ` 0.47 · `ద` 0.56 · `␣క` 0.55 · `క` 0.87 · `ను` 0.70 · `య` 0.75 · `␣క` 0.59 · `డ` 0.92 · `ము` 0.82 · `␣ని` 0.64 · `ర` 0.90 · `క` 5.3e-5✱ · `న` 0.86 · `క` 0.88 · `త` 0.91 · `ొ` 0.93 · `␣` 0.89 · `డు` 0.81 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 127 tokens · 55.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాముల్డవరడడకుడ్ మోభనుడెలేనిమి ద తనలీగతకది మను మర | `UUIIIIIUUIIIUIIIIIUIIIIIIII` |
| 2 | నమ్మకల్లని మతి లోక్ మ్మడినాయ ప్రేమ గ గతన జగతక్రిగను మరువ | `UIUIIIIUIIUIUIIIIIIIUIIIIII` |
| 3 | నునునీతి కల్లని మని లోకము మ్మడినాయ మము మ జగ జగత మ మ మ మ మ | `IIUIUIIIIUIIIIUIIIIIIIIIIIIII` |
| 4 | డను ట్టిని లలు మన్ని మని మ మ మ మ మ మ మ ర్వదిదిదిను మలము ర్వవ ర్వవ త | `IIIIIIUIIIIIIIIIIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 22% · single-akshara words 37% · repeated lines 0 · mean token probability (geometric) 0.056 · model's first choice kept 49% · constraint overrode 34% · backtracks 30

<details><summary>Token probabilities (127 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.15 · `ము` 0.02 · `ల్` 0.01 · `డ` 0.04✱ · `వర` 4.6e-4 · `డ` 0.01 · `డ` 0.05 · `కు` 0.42 · `డ` 0.93 · `్` 5.5e-8✱ · `␣మో` 8.5e-3 · `భ` 9.6e-4 · `ను` 0.03 · `డ` 0.02 · `ె` 0.88 · `లేని` 0.81 · `మి` 0.84 · `␣ద` 3.1e-3 · `␣తన` 2.8e-3✱ · `ల` 7.6e-3 · `ీ` 0.59 · `గ` 8.2e-3 · `త` 0.88 · `క` 0.89 · `ది` 0.85 · `␣మ` 0.69 · `ను` 0.63 · `␣మ` 0.64 · `ర` 0.73 · `⏎` 0.74 |
| 2 | `న` 0.88 · `మ్మ` 0.98 · `క` 0.68 · `ల్ల` 0.97 · `ని` 0.76 · `␣మ` 0.64 · `తి` 0.94 · `␣లో` 0.98 · `క` 0.92 · `్` 2.3e-12✱ · `␣మ` 2.2e-3✱ · `్` 2.4e-5✱ · `మ` 0.01✱ · `డ` 0.98 · `ిన` 1.0e-3 · `ాయ` 4.3e-3 · `␣ప్రేమ` 0.77 · `␣గ` 0.40 · `␣గ` 0.03 · `తన` 3.7e-5 · `␣జగ` 7.7e-4 · `త` 0.77 · `క` 0.73 · `్రి` 4.0e-3✱ · `గ` 4.4e-3✱ · `ను` 0.96 · `␣మ` 0.95 · `రు` 0.97 · `వ` 0.97 · `⏎` 2.1e-4✱ forced |
| 3 | `ను` 0.86 · `ను` 8.4e-4✱ · `నీ` 0.68 · `తి` 0.93 · `␣క` 0.87 · `ల్ల` 0.65 · `ని` 0.89 · `␣మ` 0.94 · `ని` 3.2e-3✱ · `␣లో` 0.99 · `క` 0.98 · `ము` 0.96 · `␣మ` 0.96 · `్` 0.96 · `మ` 0.98 · `డ` 0.99 · `ిన` 0.98 · `ాయ` 0.97 · `␣మ` 0.05✱ · `ము` 0.06 · `␣మ` 0.23 · `␣జగ` 0.05 · `␣జగ` 0.46 · `త` 0.45 · `␣మ` 0.08✱ · `␣మ` 0.15 · `␣మ` 0.18 · `␣మ` 0.22 · `␣మ` 0.49 · `⏎` 0.04✱ forced |
| 4 | `డ` 0.96 · `ను` 0.93 · `␣` 1.1e-3✱ · `ట్టి` 3.6e-4✱ · `ని` 6.8e-4✱ · `␣ల` 6.7e-3✱ · `లు` 3.3e-3✱ · `␣మ` 0.04✱ · `న్ని` 1.6e-3✱ · `␣మ` 0.03✱ · `ని` 4.3e-3✱ · `␣మ` 0.05✱ · `␣మ` 0.14 · `␣మ` 0.97 · `␣మ` 0.76 · `␣మ` 0.48 · `␣మ` 0.18 · `␣మ` 4.1e-3✱ · `␣` 0.03✱ · `ర్` 1.2e-3✱ · `వ` 0.02✱ · `ది` 5.9e-3✱ · `ది` 0.12✱ · `ది` 0.05✱ · `ను` 0.01✱ · `␣మ` 0.05✱ · `ల` 3.7e-3✱ · `ము` 0.03✱ · `␣` 0.02✱ · `ర్` 2.9e-3✱ · `వ` 0.74 · `వ` 0.05✱ · `␣` 8.9e-3✱ · `ర్` 5.7e-3✱ · `వ` 0.37 · `వ` 0.01✱ · `␣త` 5.1e-3✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 130 tokens · 16.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మనమ మను లోరు మమాద కకతోయి కడము నిర మమకతొ డు కమలము | `IIIIIIIUIIUIIIUIIIIIIIIIIIIIII` |
| 2 | కమ ముక మనుమమను మరు మమాద కకనుయ కడము నిర మనకతొ డు క | `IIIIIIIIIIIIUIIIIIIIIIIIIIIII` |
| 3 | లముతతమ మనమ మము లోరు మమద కకనుయ కడము నిర మనకతొ డు క | `IIIIIIIIIIUIIIIIIIIIIIIIIIIIII` |
| 4 | లముతతము ముక మనుమమ మ మమమద కకనుయకముము నిరకనకతొ డు | `IIIIIIIIIIIIIIIIIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.175 · model's first choice kept 62% · constraint overrode 22% · backtracks 5

<details><summary>Token probabilities (130 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.19 · `మ` 0.12 · `␣మ` 0.07 · `న` 0.02 · `మ` 0.05 · `␣మ` 0.06 · `ను` 0.02 · `␣లో` 0.03 · `రు` 7.1e-3 · `␣మ` 0.04✱ · `మా` 0.01 · `ద` 7.9e-3✱ · `␣క` 0.01✱ · `క` 0.04✱ · `తో` 1.8e-3✱ · `యి` 5.0e-4✱ · `␣క` 9.0e-3✱ · `డ` 0.04 · `ము` 0.09✱ · `␣ని` 2.0e-3✱ · `ర` 0.05 · `␣మ` 0.05 · `మ` 0.15✱ · `క` 0.09 · `త` 0.04 · `ొ` 3.8e-3✱ · `␣` 0.01✱ · `డు` 3.9e-3✱ · `␣క` 0.04✱ · `మ` 0.33 · `ల` 0.09✱ · `ము` 0.41 · `⏎` 0.30 |
| 2 | `క` 0.12✱ · `మ` 0.16✱ · `␣ము` 3.1e-3 · `క` 0.05 · `␣మ` 0.57 · `ను` 0.04 · `మ` 0.50 · `మ` 0.04 · `ను` 0.51 · `␣మ` 0.02✱ · `రు` 0.38 · `␣మ` 0.48 · `మా` 0.56 · `ద` 0.58 · `␣క` 0.68 · `క` 0.85 · `ను` 2.2e-3✱ · `య` 0.07 · `␣క` 0.70 · `డ` 0.97 · `ము` 0.93 · `␣ని` 0.89 · `ర` 0.97 · `␣మ` 0.94 · `న` 1.2e-3✱ · `క` 0.97 · `త` 0.95 · `ొ` 0.97 · `␣` 0.99 · `డు` 0.98 · `␣క` 0.72 · `⏎` 4.5e-5✱ forced |
| 3 | `ల` 0.84 · `ము` 0.89 · `త` 9.7e-4✱ · `త` 0.97 · `మ` 0.96 · `␣మ` 0.95 · `న` 0.98 · `మ` 0.93 · `␣మ` 0.98 · `ము` 9.3e-4✱ · `␣లో` 0.91 · `రు` 0.73 · `␣మ` 0.97 · `మ` 5.6e-3✱ · `ద` 0.84 · `␣క` 0.89 · `క` 0.96 · `ను` 0.03✱ · `య` 0.74 · `␣క` 0.86 · `డ` 0.99 · `ము` 0.99 · `␣ని` 0.93 · `ర` 0.99 · `␣మ` 0.97 · `న` 0.83 · `క` 0.97 · `త` 0.98 · `ొ` 0.99 · `␣` 0.97 · `డు` 0.98 · `␣క` 0.77 · `⏎` 0.04✱ forced |
| 4 | `ల` 0.96 · `ము` 0.98 · `త` 3.3e-3✱ · `త` 0.80 · `ము` 0.07 · `␣ము` 0.71 · `క` 0.53 · `␣మ` 0.60 · `ను` 0.45 · `మ` 0.60 · `మ` 0.37 · `␣మ` 0.64 · `␣మ` 0.13 · `మ` 0.20 · `మ` 0.64 · `ద` 0.37 · `␣క` 0.40 · `క` 0.73 · `ను` 0.60 · `య` 0.58 · `క` 0.05 · `ము` 0.02 · `ము` 0.73 · `␣ని` 0.56 · `ర` 0.79 · `క` 1.5e-3✱ · `న` 0.90 · `క` 0.88 · `త` 0.89 · `ొ` 0.93 · `␣` 0.86 · `డు` 0.72 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 161 tokens · 33.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మకర ల మను జరుగ ప సృక తి శకను జయు లక ని నిముర మయు మమకర ల నను జరుగ | `IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII` |
| 2 | సృకతి శకను జయు లక ని నిముర మయు మమరర ల ల జ జగ స మృమతి శశల లల యల | `IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII` |
| 3 | ల ల లల లలలల లల లల లల లల ల లలల ల ల లల లల ల లలలుసులుతుకు సరి | `IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII` |
| 4 | ల్లకుకుకుడు ఉకుడుడుడుడుకుడు తిరిగిమమడుడుడుడుడుడుడుడుడుడుడుడుడుడుడుడుడుడు | `IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 33% · single-akshara words 30% · repeated lines 0 · mean token probability (geometric) 0.077 · model's first choice kept 41% · constraint overrode 45% · backtracks 0

<details><summary>Token probabilities (161 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.74 · `క` 0.05 · `ర` 0.04 · `␣ల` 0.03 · `␣మ` 0.03 · `ను` 0.04 · `␣జ` 0.14 · `రు` 0.02 · `గ` 0.53 · `␣ప` 0.02 · `␣స` 0.03 · `ృ` 4.4e-4✱ · `క` 3.4e-4✱ · `␣తి` 0.03 · `␣శ` 0.03 · `క` 0.02✱ · `ను` 0.03 · `␣జ` 0.18 · `య` 0.10 · `ు` 0.02✱ · `␣ల` 0.10✱ · `క` 0.01✱ · `␣ని` 6.5e-3 · `␣ని` 0.11✱ · `ము` 0.07✱ · `ర` 0.05✱ · `␣` 0.11✱ · `మ` 9.3e-3✱ · `యు` 5.3e-3✱ · `␣` 0.17✱ · `మ` 3.4e-3✱ · `మ` 0.93 · `క` 0.92 · `ర` 0.89 · `␣ల` 0.93 · `␣న` 2.1e-4✱ · `ను` 0.92 · `␣జ` 0.99 · `రు` 0.96 · `గ` 0.98 · `⏎` 2.1e-5✱ forced |
| 2 | `␣స` 0.91 · `ృ` 0.95 · `క` 0.96 · `తి` 0.09 · `␣శ` 0.97 · `క` 0.94 · `ను` 0.97 · `␣జ` 0.99 · `య` 0.97 · `ు` 0.94 · `␣ల` 0.97 · `క` 0.83 · `␣ని` 0.89 · `␣ని` 0.72 · `ము` 0.86 · `ర` 0.88 · `␣మ` 0.78 · `యు` 0.89 · `␣` 0.49 · `మ` 0.51 · `మ` 0.44 · `ర` 0.25 · `ర` 0.21 · `␣ల` 0.36 · `␣ల` 0.12 · `␣జ` 0.45 · `␣జ` 0.15 · `గ` 0.29 · `␣స` 0.09 · `␣మ` 0.04 · `ృ` 0.10 · `మ` 0.28 · `తి` 0.83 · `␣శ` 0.45 · `శ` 5.6e-3✱ · `ల` 0.02✱ · `␣ల` 0.05✱ · `ల` 0.24 · `␣య` 0.24✱ · `ల` 0.08✱ · `⏎` 0.08✱ forced |
| 3 | `ల` 0.85 · `␣` 0.64 · `ల` 0.19✱ · `␣` 0.03✱ · `ల` 0.10✱ · `ల` 0.90 · `␣` 0.79 · `ల` 0.39✱ · `ల` 0.05✱ · `ల` 0.09✱ · `ల` 0.89 · `␣` 0.76 · `ల` 0.10✱ · `ల` 0.01✱ · `␣ల` 0.06✱ · `ల` 0.99 · `␣` 0.94 · `ల` 6.8e-3✱ · `ల` 0.03✱ · `␣ల` 0.22✱ · `ల` 0.99 · `␣` 0.96 · `ల` 2.1e-3✱ · `␣ల` 0.01✱ · `ల` 0.04✱ · `ల` 0.89 · `␣` 0.82 · `ల` 3.3e-3✱ · `␣ల` 0.02✱ · `␣ల` 0.14✱ · `ల` 0.95 · `␣` 0.90 · `ల` 5.7e-4✱ · `ల` 0.61 · `␣` 0.09✱ · `ల` 0.93 · `␣ల` 0.12 · `ల` 0.93 · `లు` 1.1e-5✱ · `సు` 1.3e-4✱ · `లు` 2.1e-3✱ · `తు` 9.1e-5✱ · `కు` 8.2e-3✱ · `␣సరి` 7.9e-4✱ · `⏎` 2.0e-3✱ forced |
| 4 | `ల్ల` 3.4e-4✱ · `కు` 0.02✱ · `కు` 0.02✱ · `కు` 1.4e-3✱ · `డు` 1.5e-4✱ · `␣ఉ` 9.7e-4✱ · `కు` 0.04✱ · `డు` 0.02✱ · `డు` 0.07✱ · `డు` 7.1e-3✱ · `డు` 4.9e-3✱ · `కు` 1.2e-5✱ · `డు` 0.09✱ · `␣తిరిగి` 3.3e-3✱ · `మ` 3.7e-4✱ · `మ` 1.4e-3✱ · `డు` 2.1e-3✱ · `డు` 9.0e-3✱ · `డు` 0.07✱ · `డు` 0.20✱ · `డు` 0.02✱ · `డు` 0.17✱ · `డు` 0.49 · `డు` 0.26 · `డు` 0.46 · `డు` 0.31 · `డు` 0.32 · `డు` 0.34✱ · `డు` 0.39 · `డు` 0.43 · `డు` 0.51 · `డు` 0.37 · `డు` 0.81 · `డు` 0.82 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 130 tokens · 18.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మనమ మను లోకములమంతా మకత కనమలే తమ మృకము కమ్మ | `IIIIIIIUIIIUUIIIIIIUIIIIIUI` |
| 2 | నమ మను దైవముక మయన మకత కనమలే తమ మృకము కమమజమ మ | `IIIIUIIIIIIIIIIIIUIIIIIIIIIII` |
| 3 | కష్టములన్ని తించిణ్ ష్టమమత మతమ మృకము కమమజమ మమఆప | `UIIUIUUIIIIIIIIIIIIIIIIIUI` |
| 4 | మును మడచి మకత కనమలే తమ మృకము కమము ట్టిట్టినేంకుకుడుడుచచ | `IIIIIIIIIIIUIIIIIIIIUIUIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 3% · repeated lines 0 · mean token probability (geometric) 0.131 · model's first choice kept 63% · constraint overrode 25% · backtracks 0

<details><summary>Token probabilities (130 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.19 · `మ` 0.12 · `␣మ` 0.07 · `న` 0.02 · `మ` 0.05 · `␣మ` 0.06 · `ను` 0.02 · `␣లో` 0.03 · `క` 0.15 · `ము` 0.68 · `ల` 0.04 · `మ` 0.05 · `ంతా` 0.05 · `␣మ` 0.12 · `క` 0.06 · `త` 0.08 · `␣క` 0.03 · `న` 0.13✱ · `మ` 0.03 · `లే` 0.02✱ · `␣` 3.6e-3✱ · `త` 0.05✱ · `మ` 0.91 · `␣మ` 0.09 · `ృ` 1.4e-3✱ · `క` 0.02✱ · `ము` 0.52 · `␣` 3.1e-3✱ · `క` 0.65 · `మ్మ` 5.1e-4 · `⏎` 5.8e-4✱ forced |
| 2 | `న` 0.76 · `మ` 0.60 · `␣మ` 0.55 · `ను` 0.56 · `␣ద` 0.98 · `ై` 0.98 · `వ` 0.95 · `ము` 0.81 · `క` 0.16 · `␣మ` 0.04✱ · `యన` 2.0e-4✱ · `␣మ` 0.99 · `క` 0.95 · `త` 0.98 · `␣క` 0.99 · `న` 0.99 · `మ` 1.00 · `లే` 1.00 · `␣` 0.98 · `త` 0.99 · `మ` 0.98 · `␣మ` 0.97 · `ృ` 0.99 · `క` 1.00 · `ము` 0.98 · `␣` 0.85 · `క` 0.85 · `మ` 8.6e-4✱ · `మ` 3.2e-3✱ · `జ` 0.99 · `మ` 0.96 · `␣మ` 0.96 · `⏎` 7.3e-6✱ forced |
| 3 | `క` 0.35 · `ష్ట` 0.99 · `ము` 0.99 · `ల` 0.81 · `న్ని` 0.99 · `␣త` 0.97 · `ించి` 0.98 · `ణ` 1.1e-4✱ · `్` 6.4e-8✱ · `␣` 2.5e-4✱ · `ష్ట` 2.0e-4✱ · `మ` 0.22 · `మ` 0.54 · `త` 8.2e-3✱ · `␣మ` 0.21 · `త` 0.88 · `మ` 0.68 · `␣మ` 0.63 · `ృ` 0.63 · `క` 0.94 · `ము` 0.93 · `␣` 0.76 · `క` 0.81 · `మ` 0.96 · `మ` 0.77 · `జ` 0.88 · `మ` 0.88 · `␣మ` 0.93 · `మ` 4.3e-5✱ · `ఆ` 0.98 · `ప` 0.99 · `⏎` 3.2e-6✱ forced |
| 4 | `ము` 0.97 · `ను` 0.99 · `␣మ` 0.99 · `డ` 0.99 · `చి` 0.95 · `␣మ` 0.99 · `క` 0.91 · `త` 0.96 · `␣క` 0.96 · `న` 0.96 · `మ` 0.98 · `లే` 1.00 · `␣` 0.97 · `త` 0.99 · `మ` 0.98 · `␣మ` 0.98 · `ృ` 0.98 · `క` 0.99 · `ము` 1.00 · `␣` 0.93 · `క` 0.94 · `మ` 0.02✱ · `ము` 2.8e-3✱ · `␣` 1.2e-3✱ · `ట్టి` 3.8e-4✱ · `ట్టి` 0.01✱ · `నే` 0.01✱ · `ం` 2.5e-3✱ · `కు` 3.5e-3✱ · `కు` 6.7e-3✱ · `డు` 8.4e-4✱ · `డు` 2.6e-3✱ · `చ` 0.02✱ · `చ` 0.01✱ |

</details>

[↑ meters](#meters)

---

<a id="ataveladi"></a>

## 28. ఆటవెలది (ataveladi)

```text
Meter: ఆటవెలది (ataveladi), an upajāti meter.
Lines (పాదాలు): 4.
Lines 1 and 3: 5 gaṇas (12 to 17 aksharas):
  gaṇa 1: న (III) or హ (UI)
  gaṇa 2: న (III) or హ (UI)
  gaṇa 3: న (III) or హ (UI)
  gaṇa 4: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 5: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
Lines 2 and 4: 5 gaṇas (10 to 15 aksharas):
  gaṇa 1: న (III) or హ (UI)
  gaṇa 2: న (III) or హ (UI)
  gaṇa 3: న (III) or హ (UI)
  gaṇa 4: న (III) or హ (UI)
  gaṇa 5: న (III) or హ (UI)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 4. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): not required.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter ఆటవెలది (ataveladi).

Meter: ఆటవెలది (ataveladi), an upajāti meter.
Lines (పాదాలు): 4.
Lines 1 and 3: 5 gaṇas (12 to 17 aksharas):
  gaṇa 1: న (III) or హ (UI)
  gaṇa 2: న (III) or హ (UI)
  gaṇa 3: న (III) or హ (UI)
  gaṇa 4: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 5: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
Lines 2 and 4: 5 gaṇas (10 to 15 aksharas):
  gaṇa 1: న (III) or హ (UI)
  gaṇa 2: న (III) or హ (UI)
  gaṇa 3: న (III) or హ (UI)
  gaṇa 4: న (III) or హ (UI)
  gaṇa 5: న (III) or హ (UI)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 4. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): not required.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 68 tokens · 8.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కత మ ల ల లనక నముతు లయసుల రాక | `IIIIIIIIIIIIIIIUI` |
| 2 | సమరరలముధతి శనుము లముముర | `IIIIIIIIIIIIIII` |
| 3 | శమ మ ల నల నక నముము లయసుల రాక | `IIIIIIIIIIIIIIIUI` |
| 4 | సుమతి ధమురము శనుము మపుముర ము | `IIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 33% · single-akshara words 25% · repeated lines 0 · mean token probability (geometric) 0.068 · model's first choice kept 44% · constraint overrode 18% · backtracks 0

<details><summary>Token probabilities (68 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.03 · `త` 0.39 · `␣మ` 0.01 · `␣ల` 0.03 · `␣ల` 0.12✱ · `␣ల` 0.08 · `న` 2.3e-3 · `క` 0.06 · `␣న` 0.01 · `ము` 0.09 · `తు` 1.2e-3✱ · `␣ల` 0.11 · `య` 8.2e-3✱ · `సు` 7.3e-3 · `ల` 0.01✱ · `␣రా` 6.6e-3✱ · `క` 0.04✱ · `⏎` 0.70 |
| 2 | `స` 0.04 · `మ` 0.31 · `ర` 0.82 · `ర` 0.24 · `ల` 0.01 · `ము` 0.09 · `ధ` 3.2e-3 · `తి` 9.4e-3 · `␣శ` 0.13 · `ను` 0.03 · `ము` 0.07 · `␣ల` 0.03 · `ము` 0.06 · `ము` 0.07 · `ర` 0.02✱ · `⏎` 0.19 |
| 3 | `శ` 0.10 · `మ` 0.14 · `␣మ` 0.26 · `␣ల` 0.34 · `␣న` 0.05 · `ల` 0.07 · `␣న` 0.17 · `క` 0.22 · `␣న` 0.46 · `ము` 0.27 · `ము` 8.2e-3✱ · `␣ల` 0.95 · `య` 0.92 · `సు` 0.88 · `ల` 0.89 · `␣రా` 0.76 · `క` 0.71 · `⏎` 0.87 |
| 4 | `సు` 0.04 · `మ` 0.46 · `తి` 0.20✱ · `␣ధ` 2.6e-3 · `ము` 0.07 · `ర` 0.03 · `ము` 0.09 · `␣శ` 0.21 · `ను` 0.32 · `ము` 0.63 · `␣మ` 5.0e-3✱ · `పు` 0.02 · `ము` 0.73 · `ర` 0.78 · `␣` 0.06✱ · `ము` 3.1e-6✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 71 tokens · 7.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాతిలసి వముసచు సార్ తీరు జలిమ సీ | `UIIIIIIIUUIIIIU` |
| 2 | తన్మర జగ శగను నగ్ న్మవిమిశ | `UIIIIIIIUIIII` |
| 3 | శమ లరెనుటనుశ లముముమురముముక మ | `IIIIIIIIIIIIIIIII` |
| 4 | శమ మము జగ శగ ము న్మమవివిమిశ | `IIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 24% · repeated lines 0 · mean token probability (geometric) 0.021 · model's first choice kept 35% · constraint overrode 24% · backtracks 0

<details><summary>Token probabilities (71 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.38 · `తి` 0.01 · `ల` 0.01 · `సి` 9.2e-3 · `␣వ` 9.1e-3 · `ము` 0.06 · `స` 6.7e-3 · `చు` 0.01 · `␣స` 0.01 · `ార` 7.7e-5✱ · `్` 4.3e-6✱ · `␣తీ` 1.1e-4✱ · `రు` 0.20 · `␣జ` 0.04 · `లి` 5.6e-3✱ · `మ` 0.02✱ · `␣సీ` 0.02✱ · `⏎` 0.07 forced |
| 2 | `త` 0.03 · `న్` 0.03✱ · `మ` 0.70 · `ర` 0.04✱ · `␣జ` 0.02 · `గ` 0.02 · `␣శ` 0.01 · `గ` 0.02 · `ను` 0.04 · `␣నగ` 2.2e-3 · `్` 4.1e-8✱ · `␣న` 0.02✱ · `్` 7.5e-6✱ · `మ` 0.22 · `వి` 4.1e-3 · `మి` 7.0e-3 · `శ` 0.02✱ · `⏎` 0.16 |
| 3 | `శ` 0.15 · `మ` 0.12 · `␣ల` 0.03 · `రె` 1.2e-4 · `ను` 0.04 · `ట` 0.01 · `ను` 0.03 · `శ` 7.4e-3 · `␣ల` 0.06 · `ము` 0.08 · `ము` 0.07 · `ము` 0.08 · `ర` 7.7e-3 · `ము` 0.07 · `ము` 0.07 · `క` 0.02✱ · `␣మ` 0.01✱ · `⏎` 0.17 |
| 4 | `శ` 0.08 · `మ` 0.12 · `␣మ` 0.05 · `ము` 0.03 · `␣జ` 0.19 · `గ` 0.25 · `␣శ` 0.25 · `గ` 0.33 · `␣ము` 3.9e-3 · `␣న` 0.13✱ · `్` 0.07✱ · `మ` 0.14✱ · `మ` 0.16 · `వి` 0.17 · `వి` 0.29 · `మి` 0.56 · `శ` 0.64 |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 68 tokens · 16.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మమమసి వ సుస హను శ మతు లం ల మకతో | `IIIIIIIIIIIIUIIIU` |
| 2 | మ మ మతి గరు జ మయ శి మ కల ల ల | `IIIIIIIIIIIIIII` |
| 3 | మమమసి వ సు స హను శ మతు ల ల లకక | `IIIIIIIIIIIIIIIII` |
| 4 | మమ మ మతి గరు జ మయ మ మ మ ల ల | `IIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 24% · single-akshara words 59% · repeated lines 0 · mean token probability (geometric) 0.204 · model's first choice kept 65% · constraint overrode 15% · backtracks 8

<details><summary>Token probabilities (68 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.83 · `మ` 0.21 · `మ` 0.14 · `సి` 0.01 · `␣వ` 0.02 · `␣సు` 0.01 · `స` 2.6e-3 · `␣హ` 6.5e-3 · `ను` 0.71 · `␣శ` 4.8e-3 · `␣మ` 0.03✱ · `తు` 0.90 · `␣ల` 0.67 · `ం` 0.10 · `␣ల` 0.63 · `␣మ` 0.74 · `క` 0.69 · `తో` 1.3e-4✱ · `⏎` 0.05 forced |
| 2 | `మ` 0.56 · `␣మ` 0.03 · `␣మ` 0.78 · `తి` 0.92 · `␣గ` 0.31 · `రు` 0.23 · `␣జ` 0.43 · `␣మ` 0.07 · `య` 0.08 · `␣శ` 0.17 · `ి` 0.66 · `␣మ` 0.03✱ · `␣కల` 2.1e-3✱ · `␣ల` 0.84 · `␣ల` 2.1e-3✱ · `⏎` 0.01✱ forced |
| 3 | `మ` 0.37✱ · `మ` 0.86 · `మ` 0.63 · `సి` 0.64 · `␣వ` 0.51 · `␣సు` 0.69 · `␣స` 0.15 · `␣హ` 0.72 · `ను` 0.52 · `␣శ` 0.54 · `␣మ` 0.69 · `తు` 0.57 · `␣ల` 0.64 · `␣ల` 0.46 · `␣ల` 0.51 · `క` 0.19 · `క` 0.46 · `⏎` 0.01✱ forced |
| 4 | `మ` 0.06✱ · `మ` 0.87 · `␣మ` 0.68 · `␣మ` 0.84 · `తి` 0.86 · `␣గ` 0.66 · `రు` 0.45 · `␣జ` 0.73 · `␣మ` 0.81 · `య` 0.68 · `␣మ` 0.25✱ · `␣మ` 0.18 · `␣మ` 0.33 · `␣ల` 0.53 · `␣ల` 0.70 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 63 tokens · 31.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తరయిత శిను కృ జగవిరురమముమముము | `IIIIIIIIIIIIIIIII` |
| 2 | మమమరుసల వచ్చిదు మదము జము | `IIIIIIUIIIIIII` |
| 3 | మమమ సనుమముండటి మనుమంతుడెనుమ | `IIIIIIUIIIIUIIII` |
| 4 | మనుతుకడడు లంకను నిలచు జము | `IIIIIIUIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.107 · model's first choice kept 62% · constraint overrode 22% · backtracks 22

<details><summary>Token probabilities (63 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `తర` 3.9e-5 · `యిత` 0.02✱ · `␣శి` 0.02 · `ను` 0.10 · `␣కృ` 2.0e-4 · `␣జ` 0.65 · `గ` 0.27 · `వి` 5.3e-3 · `రు` 2.9e-3✱ · `ర` 0.86 · `మ` 0.29 · `ము` 0.08✱ · `మ` 0.22 · `ము` 0.36 · `ము` 0.25 · `⏎` 0.08 forced |
| 2 | `మ` 0.33 · `మ` 0.10 · `మ` 0.05 · `ర` 0.04 · `ు` 6.7e-3 · `స` 3.1e-3 · `ల` 0.91 · `␣వచ్చి` 3.6e-5 · `దు` 8.0e-4✱ · `␣మ` 0.10 · `ద` 0.02✱ · `ము` 0.15 · `␣జ` 0.79 · `ము` 0.18 · `⏎` 0.22✱ |
| 3 | `మ` 0.83 · `మ` 0.78 · `మ` 0.72 · `␣స` 0.73 · `ను` 0.85 · `మ` 4.1e-4✱ · `ము` 0.77 · `ండ` 5.0e-3✱ · `టి` 0.75 · `␣మ` 8.6e-4✱ · `ను` 0.98 · `మం` 0.97 · `తు` 0.95 · `డ` 0.99 · `ె` 0.97 · `ను` 0.04✱ · `మ` 0.21✱ · `⏎` 0.08 forced |
| 4 | `మ` 0.21✱ · `ను` 0.07✱ · `తు` 0.69 · `క` 0.93 · `డ` 0.99 · `డు` 8.0e-3✱ · `␣ల` 0.99 · `ంక` 0.96 · `ను` 0.92 · `␣ని` 0.99 · `ల` 0.98 · `చు` 0.99 · `␣జ` 0.87 · `ము` 0.97 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 63 tokens · 12.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ మకక మట్ ల్లానది నిశల | `UIUIIIIUUIIIII` |
| 2 | లోకమందు ఏటినిక్ కదా ని | `UIUIUIUIUI` |
| 3 | తతత ప్రేమ మకక మత వ ల్లానది నిశల్ | `IIIUIIIIIIIUIIIU` |
| 4 | జనము ఏటినిక్ కడా ని లేదు | `IIIUIUIUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 41% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.051 · model's first choice kept 54% · constraint overrode 38% · backtracks 0

<details><summary>Token probabilities (63 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.47 · `ల్లి` 0.47 · `␣ప్రేమ` 0.51 · `␣మ` 0.44 · `క` 0.31 · `క` 0.17 · `␣మ` 0.09 · `ట` 0.03✱ · `్` 2.7e-11✱ · `␣` 1.4e-3✱ · `ల` 0.02✱ · `్లా` 6.2e-8✱ · `న` 0.06✱ · `ది` 0.03✱ · `␣ని` 0.02✱ · `శ` 0.05✱ · `ల` 0.11 · `⏎` 0.63 |
| 2 | `లో` 0.38 · `క` 0.98 · `మ` 0.09 · `ందు` 0.66 · `␣ఏ` 0.39 · `టి` 0.02✱ · `ని` 0.17 · `క` 0.02✱ · `్` 1.2e-6✱ · `␣క` 0.02✱ · `దా` 0.06✱ · `␣ని` 0.01✱ · `⏎` 0.03✱ forced |
| 3 | `త` 0.02✱ · `త` 0.88 · `త` 0.03✱ · `␣ప్రేమ` 0.91 · `␣మ` 0.96 · `క` 0.80 · `క` 0.91 · `␣మ` 0.96 · `త` 3.8e-5✱ · `␣వ` 7.1e-3✱ · `␣` 0.74 · `ల్` 0.87 · `లా` 0.90 · `న` 0.73 · `ది` 0.87 · `␣ని` 0.73 · `శ` 0.75 · `ల` 0.92 · `్` 1.0e-7✱ · `⏎` 7.6e-3✱ forced |
| 4 | `జ` 0.12 · `న` 0.10 · `ము` 0.75 · `␣ఏ` 0.95 · `టి` 0.94 · `ని` 0.82 · `క` 0.93 · `్` 0.51 · `␣క` 0.92 · `డా` 3.1e-4✱ · `␣ని` 0.75 · `␣లేదు` 2.3e-4✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 70 tokens · 11.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కంజ మర వలె జెదితిన్ జ సముద్రము | `UIIIIIIIUIIUII` |
| 2 | మలయ శిఖరమురి జె హడుమతుత్మ | `IIIIIIIIIIIIUI` |
| 3 | మహమజమును మరి జెడు హు లంకనునుముర | `IIIIIIIIIIIUIIIII` |
| 4 | శమను చూడును జెడు హు మతుడు మున | `IIIUIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 38% · single-akshara words 19% · repeated lines 0 · mean token probability (geometric) 0.087 · model's first choice kept 56% · constraint overrode 21% · backtracks 0

<details><summary>Token probabilities (70 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.02 · `ంజ` 0.03 · `␣మ` 0.03 · `ర` 0.04 · `␣వ` 0.09 · `లె` 0.37 · `␣జ` 0.04 · `ె` 0.46 · `ది` 0.04✱ · `తి` 0.04 · `న్` 9.1e-3✱ · `␣జ` 0.08✱ · `␣స` 0.06 · `ము` 0.80 · `ద్ర` 0.54 · `ము` 0.64 · `⏎` 0.61 |
| 2 | `మ` 0.74 · `ల` 0.09 · `య` 0.06 · `␣శి` 0.19 · `ఖ` 0.77 · `ర` 0.39 · `ము` 0.08 · `రి` 0.03 · `␣జ` 0.17 · `ె` 0.21 · `␣హ` 0.43 · `డు` 1.0e-4✱ · `మ` 0.08✱ · `తు` 0.93 · `త్మ` 4.6e-4 · `⏎` 0.98 |
| 3 | `మ` 0.98 · `హ` 0.97 · `మ` 4.0e-4✱ · `జ` 0.89 · `ము` 0.68 · `ను` 0.88 · `␣మ` 0.33 · `రి` 0.07 · `␣జ` 0.38 · `ె` 0.24 · `డు` 0.04✱ · `␣` 3.3e-4✱ · `హు` 6.9e-7✱ · `␣ల` 0.94 · `ంక` 0.46 · `ను` 0.27 · `ను` 0.19 · `ము` 0.15 · `ర` 0.05✱ · `⏎` 0.04 forced |
| 4 | `శ` 0.06 · `మ` 0.17 · `ను` 0.21 · `␣చూ` 0.04 · `డు` 0.58 · `ను` 0.63 · `␣జ` 0.96 · `ె` 0.88 · `డు` 0.91 · `␣హ` 0.99 · `ు` 3.9e-4✱ · `␣మ` 0.23✱ · `తు` 0.84 · `డు` 0.64 · `␣` 2.8e-3✱ · `ము` 2.2e-4✱ · `న` 1.4e-3✱ |

</details>

[↑ meters](#meters)

---

<a id="tetagiti"></a>

## 29. తేటగీతి (tetagiti)

```text
Meter: తేటగీతి (tetagiti), an upajāti meter.
Lines (పాదాలు): 4.
Every line: 5 gaṇas (12 to 17 aksharas):
  gaṇa 1: న (III) or హ (UI)
  gaṇa 2: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 3: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 4: న (III) or హ (UI)
  gaṇa 5: న (III) or హ (UI)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 4. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): not required.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter తేటగీతి (tetagiti).

Meter: తేటగీతి (tetagiti), an upajāti meter.
Lines (పాదాలు): 4.
Every line: 5 gaṇas (12 to 17 aksharas):
  gaṇa 1: న (III) or హ (UI)
  gaṇa 2: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 3: భ (UII) or ర (UIU) or త (UUI) or నల (IIII) or నగ (IIIU) or సల (IIUI)
  gaṇa 4: న (III) or హ (UI)
  gaṇa 5: న (III) or హ (UI)
Yati (యతి): in every line the 1st akshara must be in yati-maitri with the first akshara of gaṇa 4. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): not required.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 71 tokens · 7.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కంజ మనడుండను జగ శ జగ్ జయ మము | `UIIIUIIIIIUIIII` |
| 2 | సడధి శి ముమ మ కతిగకి ల లకి శ జెలు | `IIIIIIIIIIIIIIIII` |
| 3 | మమ ల మరనుక స మ జనన మల హనుమ | `IIIIIIIIIIIIIIIII` |
| 4 | వవనపు ముపు సు లను దా న స వనముముము | `IIIIIIIIIUIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 28% · single-akshara words 41% · repeated lines 0 · mean token probability (geometric) 0.030 · model's first choice kept 21% · constraint overrode 17% · backtracks 0

<details><summary>Token probabilities (71 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.02 · `ంజ` 0.04 · `␣మ` 0.03 · `న` 0.01 · `డు` 7.0e-3 · `ండ` 0.02 · `ను` 0.04 · `␣జ` 0.12 · `గ` 0.01 · `␣శ` 6.3e-3 · `␣జగ` 5.5e-4 · `్` 1.2e-6✱ · `␣` 0.02✱ · `జయ` 7.9e-4✱ · `␣మ` 0.05 · `ము` 0.07✱ · `⏎` 0.68 |
| 2 | `స` 0.15 · `డ` 0.01 · `ధి` 5.5e-3 · `␣శి` 0.01 · `␣ము` 0.02 · `మ` 0.02 · `␣మ` 0.02 · `␣క` 3.1e-3 · `తి` 0.01 · `గ` 0.02 · `కి` 5.0e-3 · `␣ల` 0.24 · `␣ల` 0.03✱ · `కి` 4.3e-3 · `␣శ` 0.02 · `␣జ` 0.02 · `ె` 0.25✱ · `లు` 0.03✱ · `⏎` 0.03✱ forced |
| 3 | `మ` 0.52 · `మ` 0.22 · `␣ల` 0.05 · `␣మ` 0.06 · `ర` 0.02 · `ను` 0.04 · `క` 0.03 · `␣స` 0.01 · `␣మ` 0.04 · `␣జ` 0.02 · `న` 0.01 · `న` 0.01 · `␣మ` 0.06✱ · `ల` 0.10 · `␣హ` 0.97 · `ను` 0.92 · `మ` 0.61 · `⏎` 0.02✱ forced |
| 4 | `వ` 0.12✱ · `వ` 0.91 · `న` 0.64 · `పు` 0.03 · `␣ము` 0.05 · `పు` 0.01 · `␣సు` 7.4e-3 · `␣ల` 0.04 · `ను` 0.04 · `␣దా` 7.1e-3 · `␣న` 0.04 · `␣స` 0.02 · `␣వ` 1.3e-3✱ · `న` 0.10 · `ము` 0.53 · `ము` 0.20 · `ము` 0.22 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 69 tokens · 9.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తందుమల్లిమముది వేప్పయుట్ దరిద్ర | `UIUIIIIUIUIUI` |
| 2 | ససగ లేకనధ మ పొయ మృశశలిల మ | `IIIUIIIIIIIIIIII` |
| 3 | ప్రనమ నైజ వే తా న కక నొలవము వ | `IIIUIUUIIIIIIII` |
| 4 | మమ మతడమించ మది మ మ మౌక మౌన | `IIIIIUIIIIIUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 33% · repeated lines 0 · mean token probability (geometric) 0.022 · model's first choice kept 25% · constraint overrode 26% · backtracks 0

<details><summary>Token probabilities (69 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.33 · `ందు` 1.2e-3 · `మ` 0.04 · `ల్లి` 1.6e-3 · `మ` 0.04 · `ము` 0.03 · `ది` 0.01✱ · `␣వే` 3.7e-3✱ · `ప్ప` 3.6e-4✱ · `యు` 3.9e-3✱ · `ట` 0.02✱ · `్` 1.0e-9✱ · `␣ద` 6.2e-3✱ · `రి` 0.02✱ · `ద్ర` 0.36 · `⏎` 0.04✱ forced |
| 2 | `స` 0.02 · `స` 5.3e-3 · `గ` 0.01 · `␣లే` 2.0e-3 · `క` 0.05 · `న` 0.03 · `ధ` 2.8e-3 · `␣మ` 0.06 · `␣పొ` 6.8e-4 · `య` 9.9e-3 · `␣మ` 0.07 · `ృ` 7.4e-3✱ · `శ` 0.01✱ · `శ` 0.03✱ · `లి` 0.10 · `ల` 0.08✱ · `␣మ` 0.01✱ · `⏎` 0.08✱ forced |
| 3 | `ప్ర` 0.05 · `న` 0.03 · `మ` 0.11 · `␣న` 0.05✱ · `ై` 0.02 · `జ` 6.6e-3 · `␣వే` 1.0e-2 · `␣తా` 1.4e-3 · `␣న` 0.02 · `␣క` 0.02 · `క` 0.04 · `␣న` 0.03✱ · `ొ` 0.06 · `ల` 0.03 · `వ` 0.10 · `ము` 0.03 · `␣వ` 8.3e-3✱ · `⏎` 0.42 |
| 4 | `మ` 0.53 · `మ` 0.40 · `␣మ` 0.05 · `త` 0.02 · `డ` 0.01 · `మ` 0.06 · `ించ` 2.7e-3 · `␣మ` 0.08 · `ది` 0.14 · `␣మ` 0.10 · `␣మ` 0.11 · `␣మ` 0.14 · `ౌ` 0.05 · `క` 0.41 · `␣మ` 0.92 · `ౌ` 0.99 · `న` 0.92 |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 81 tokens · 20.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాము లడెటాడుడైచన్ శకెన్ మయ మతి | `UIIIUIUUIUIIII` |
| 2 | సీతల వడెన్ జను వల లట్రిన్ తురికక | `UIIIUIIIIUUIIII` |
| 3 | ముముమమము నడె జన్ నలల మలయన్ ఠు | `IIIIIIIUIIIIIUI` |
| 4 | కమున జ నమ గమగ నడె జె మలల మల | `IIIIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 36% · single-akshara words 16% · repeated lines 0 · mean token probability (geometric) 0.091 · model's first choice kept 51% · constraint overrode 23% · backtracks 12

<details><summary>Token probabilities (81 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.71 · `ము` 0.49 · `␣ల` 0.30 · `డ` 0.73 · `ె` 0.95 · `టా` 1.7e-5✱ · `డు` 0.79 · `డ` 0.29 · `ై` 0.93 · `చ` 1.4e-4 · `న్` 0.50 · `␣శ` 1.0e-3 · `కె` 0.03 · `న్` 0.16 · `␣` 4.0e-3✱ · `మ` 1.7e-3✱ · `య` 0.03 · `␣మ` 4.6e-3✱ · `తి` 0.97 · `⏎` 0.04✱ forced |
| 2 | `సీ` 0.20✱ · `త` 0.39 · `ల` 0.02 · `␣వ` 0.07 · `డ` 0.46 · `ె` 0.09 · `న్` 0.85 · `␣జ` 0.19 · `ను` 0.03 · `␣వ` 9.3e-3 · `ల` 0.02✱ · `␣ల` 0.05 · `ట` 0.02 · `్రి` 2.2e-3 · `న్` 0.03✱ · `␣` 0.02✱ · `తు` 2.0e-3✱ · `రి` 0.02 · `క` 0.08 · `క` 0.05 · `⏎` 0.05✱ forced |
| 3 | `ము` 0.42 · `ము` 0.03✱ · `మ` 0.02✱ · `మ` 0.29 · `ము` 0.09 · `␣న` 0.44 · `డ` 0.66 · `ె` 0.59 · `␣జ` 0.08 · `న్` 0.12 · `␣న` 0.02 · `ల` 0.10 · `ల` 0.18 · `␣మ` 0.01✱ · `ల` 0.20 · `య` 0.94 · `న్` 0.91 · `␣` 0.92 · `ఠ` 0.95 · `ు` 0.96 · `⏎` 2.0e-3✱ forced |
| 4 | `క` 0.89 · `ము` 0.06✱ · `న` 0.02✱ · `␣జ` 0.10 · `␣న` 0.02 · `మ` 0.32 · `␣గ` 3.2e-3 · `మ` 0.57 · `గ` 0.83 · `␣న` 0.89 · `డ` 0.96 · `ె` 0.85 · `␣జ` 0.88 · `ె` 2.6e-4✱ · `␣మ` 9.1e-3✱ · `ల` 0.99 · `ల` 0.98 · `␣మ` 0.96 · `ల` 0.99 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 69 tokens · 33.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాముడు న మను వన్ల గెమఛ్ మల ల స | `UIIIIIUIIUIIII` |
| 2 | లంపెను చడ వె ల లతపు లెడ్ పులులుది | `UIIIIIIIIIUIIII` |
| 3 | ఓ పసిన్నము లేదు వేలా పు నేను | `UIUIIUIUUIUI` |
| 4 | వనన లేదు లేదు ల్లలే ల ల ణముననన | `IIIUIUIIUIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 36% · repeated lines 0 · mean token probability (geometric) 0.015 · model's first choice kept 30% · constraint overrode 52% · backtracks 24

<details><summary>Token probabilities (69 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.98 · `ము` 0.90 · `డు` 0.42 · `␣న` 0.04 · `␣మ` 0.02 · `ను` 0.63 · `␣వ` 0.60 · `న్` 0.50 · `ల` 0.79 · `␣గ` 0.62 · `ె` 0.97 · `మ` 0.89 · `ఛ` 1.9e-3 · `్` 3.0e-8✱ · `␣` 5.0e-4✱ · `మ` 1.2e-3✱ · `ల` 0.02 · `␣ల` 0.01 · `␣స` 5.4e-3 · `⏎` 0.45 forced |
| 2 | `ల` 0.87 · `ంప` 0.98 · `ె` 0.99 · `ను` 0.99 · `␣చ` 0.59 · `డ` 0.94 · `␣వె` 1.0e-3 · `␣ల` 0.07 · `␣ల` 0.09✱ · `త` 0.88 · `పు` 0.94 · `␣లె` 0.98 · `డ` 1.00 · `్` 3.4e-9✱ · `␣` 0.21✱ · `పు` 2.2e-4✱ · `లు` 3.6e-4✱ · `లు` 1.8e-5✱ · `ది` 1.1e-4✱ · `⏎` 0.01✱ forced |
| 3 | `ఓ` 3.2e-5✱ · `␣ప` 0.01✱ · `సి` 0.01 · `న్` 0.01 · `న` 0.01 · `ము` 7.9e-3✱ · `␣లేదు` 1.9e-3✱ · `␣వే` 0.10 · `లా` 1.4e-4✱ · `␣` 4.5e-4✱ · `పు` 6.1e-4✱ · `␣నేను` 6.7e-3✱ · `⏎` 6.3e-3✱ forced |
| 4 | `వ` 3.1e-3✱ · `న` 0.04✱ · `న` 0.08✱ · `␣లేదు` 0.05✱ · `␣లేదు` 0.09✱ · `␣` 0.01✱ · `ల్ల` 3.4e-3✱ · `లే` 2.3e-4✱ · `␣ల` 0.01✱ · `␣ల` 6.3e-3✱ · `␣` 0.01✱ · `ణ` 5.1e-3✱ · `ము` 0.11✱ · `న` 1.0e-3✱ · `న` 4.8e-3✱ · `న` 2.2e-3✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 74 tokens · 13.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రాము జటను వీడి లకన్ వె వెన్ మసీత | `UIIIIUIIUIUIUI` |
| 2 | సీమక యటన్న్డనెను సీముముల్ మయన్ జ | `UIIIUIIIUIUIUI` |
| 3 | ముము మముడు లంకకు నొడెనునుమగమనిక | `IIIIIUIIIIIIIIIII` |
| 4 | పైన పద్యలో ఒక చిన్న తూప్ ను లేదు | `UIUIUIIUIUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 30% · single-akshara words 22% · repeated lines 0 · mean token probability (geometric) 0.039 · model's first choice kept 46% · constraint overrode 36% · backtracks 0

<details><summary>Token probabilities (74 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.48 · `ము` 0.10 · `␣జ` 0.05 · `ట` 0.09 · `ను` 0.05✱ · `␣వీ` 0.05 · `డి` 0.47 · `␣ల` 0.13 · `క` 8.5e-3✱ · `న్` 0.22 · `␣వె` 0.34 · `␣వె` 0.46 · `న` 1.5e-3✱ · `్` 1.8e-8✱ · `␣` 4.2e-3✱ · `మ` 1.4e-4✱ · `సీ` 0.76 · `త` 0.42 · `⏎` 0.13✱ forced |
| 2 | `␣సీ` 0.04 · `మ` 0.03 · `క` 0.03 · `␣య` 0.02 · `ట` 0.02 · `న్` 0.03 · `న్` 0.04 · `డ` 0.03✱ · `న` 0.05✱ · `ె` 0.90 · `ను` 0.86 · `␣సీ` 0.02✱ · `ము` 4.6e-3✱ · `ము` 0.17✱ · `ల` 0.03✱ · `్` 1.3e-8✱ · `␣` 0.02✱ · `మ` 0.01✱ · `య` 0.80 · `న్` 0.71 · `␣జ` 0.05✱ · `⏎` 0.05✱ forced |
| 3 | `ము` 0.10 · `ము` 0.08 · `␣మ` 0.02 · `ము` 0.07 · `డు` 0.04 · `␣ల` 0.69 · `ంక` 0.84 · `కు` 0.60 · `␣న` 0.64 · `ొ` 0.94 · `డ` 0.97 · `ె` 0.97 · `ను` 0.83 · `ను` 0.05✱ · `మ` 1.2e-3✱ · `గ` 0.63 · `మని` 0.54 · `క` 0.51 · `⏎` 0.28 |
| 4 | `ప` 0.58 · `ైన` 0.98 · `␣ప` 0.97 · `ద్య` 0.98 · `లో` 1.5e-3✱ · `␣ఒక` 0.87 · `␣చిన్న` 1.00 · `␣త` 1.00 · `ూ` 2.8e-4✱ · `ప` 6.2e-4✱ · `్` 8.6e-10✱ · `␣` 2.8e-4✱ · `ను` 8.1e-3✱ · `␣లేదు` 2.3e-3✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 70 tokens · 10.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాము ల ల శ జను ల దేవి మ జర మతము | `UIIIIIIIUIIIIIII` |
| 2 | సీత మ మ ల ల శ న ల ల నక్ తర మమ | `UIIIIIIIIIUIIII` |
| 3 | జలము మ ల ల శ జను ల లంక ల జయమర | `IIIIIIIIIIUIIIIII` |
| 4 | రామము డ ల ల ల శ న ల లన్ మగ నడ | `UIIIIIIIIIUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 30% · single-akshara words 65% · repeated lines 0 · mean token probability (geometric) 0.089 · model's first choice kept 50% · constraint overrode 17% · backtracks 0

<details><summary>Token probabilities (70 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.02 · `ము` 0.13 · `␣ల` 0.05 · `␣ల` 0.03 · `␣శ` 0.02 · `␣జ` 0.03 · `ను` 0.13 · `␣ల` 0.03 · `␣ద` 0.02 · `ే` 0.59 · `వి` 0.15 · `␣మ` 0.05 · `␣జ` 0.05 · `ర` 0.03✱ · `␣మ` 0.02✱ · `త` 0.02 · `ము` 0.25 · `⏎` 0.89 |
| 2 | `సీ` 0.59 · `త` 0.54 · `␣మ` 0.25 · `␣మ` 0.07 · `␣ల` 0.17 · `␣ల` 0.11 · `␣శ` 0.04 · `␣న` 0.04 · `␣ల` 0.16 · `␣ల` 0.17 · `␣న` 0.06 · `క` 0.06✱ · `్` 1.5e-8✱ · `␣తర` 2.3e-4✱ · `␣మ` 0.07 · `మ` 0.03 · `⏎` 0.05✱ forced |
| 3 | `జ` 0.27 · `ల` 0.38 · `ము` 0.03✱ · `␣మ` 0.75 · `␣ల` 0.90 · `␣ల` 0.95 · `␣శ` 0.95 · `␣జ` 0.96 · `ను` 0.95 · `␣ల` 0.96 · `␣ల` 0.68 · `ంక` 0.57 · `␣ల` 0.02✱ · `␣జ` 0.07 · `య` 0.05 · `మ` 0.04 · `ర` 0.07 · `⏎` 7.0e-3✱ forced |
| 4 | `రా` 0.68 · `మ` 0.48 · `ము` 0.25 · `␣డ` 0.89 · `␣ల` 0.11 · `␣ల` 0.89 · `␣ల` 0.88 · `␣శ` 0.72 · `␣న` 0.59 · `␣ల` 0.73 · `␣ల` 0.83 · `న్` 4.1e-3✱ · `␣` 2.0e-3✱ · `మ` 4.5e-4✱ · `గ` 0.06 · `␣న` 0.06 · `డ` 0.16 |

</details>

[↑ meters](#meters)

---

<a id="taralamu"></a>

## 30. తరళము (taralamu)

```text
Meter: తరళము (taralamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: న భ ర స జ జ గురువు, i.e. III UII UIU IIU IUI IUI U (19 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 12th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter తరళము (taralamu).

Meter: తరళము (taralamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: న భ ర స జ జ గురువు, i.e. III UII UIU IIU IUI IUI U (19 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 12th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 106 tokens · 26.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కరుణ లో శ జగప్యముక్వరకత్రియత్రి మమించుగాజ్ | `IIIUIIUIUIIUIUIIUIU` |
| 2 | కరిల మన్ముకధవ్రి మక్రిమ మ్ర్ర్గమ్యముగ్వరకమ్వరమ్ | `IIIUIIUIUIIUIUIIUIU` |
| 3 | మరి ల లోకము లోతనుమ్రమమమ్యమమ్యమతిమ్యరిల్ | `IIIUIIUIUIIUIUIIUIU` |
| 4 | మురితనుమ్యమమమ్యమమ్యతిముమ్య ల్య్యైయయమున్యలీ | `IIIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 20% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 30% · constraint overrode 57% · backtracks 0

<details><summary>Token probabilities (106 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.11 · `రుణ` 0.48 · `␣లో` 2.0e-3 · `␣శ` 1.3e-3 · `␣జగ` 3.7e-3 · `ప` 0.02✱ · `్య` 7.0e-3✱ · `ము` 0.31 · `క` 0.04✱ · `్వర` 8.7e-5✱ · `క` 0.02 · `త` 7.9e-3✱ · `్రియ` 1.1e-4✱ · `త` 0.04✱ · `్రి` 9.8e-4✱ · `␣మ` 0.05✱ · `మ` 0.37 · `ించు` 5.3e-3✱ · `గా` 2.5e-3✱ · `జ` 0.06 · `్` 7.9e-7✱ · `⏎` 0.05✱ forced |
| 2 | `క` 0.60 · `రి` 8.9e-4✱ · `ల` 0.84 · `␣మ` 0.05 · `న్` 0.03✱ · `ము` 0.03 · `క` 0.06 · `ధ` 3.0e-3 · `వ` 0.02 · `్రి` 6.6e-4✱ · `␣మ` 0.09 · `క` 0.08 · `్రి` 1.5e-3✱ · `మ` 0.17 · `␣మ` 0.16 · `్ర` 1.5e-3✱ · `్ర` 3.4e-5✱ · `్` 3.6e-6✱ · `గ` 0.02✱ · `మ` 0.24 · `్య` 0.01✱ · `ము` 0.31 · `గ` 0.03✱ · `్వర` 2.2e-4✱ · `క` 0.09✱ · `మ` 0.94 · `్వర` 1.4e-4✱ · `మ` 1.5e-3✱ · `్` 3.5e-7✱ · `⏎` 0.04✱ forced |
| 3 | `మ` 0.21 · `రి` 8.6e-3✱ · `␣ల` 0.07 · `␣లో` 0.65 · `క` 0.62 · `ము` 0.64 · `␣లో` 0.46 · `త` 0.23 · `ను` 0.59 · `మ` 7.5e-3✱ · `్ర` 1.6e-4✱ · `మ` 0.19 · `మ` 0.04✱ · `మ` 0.08✱ · `్య` 1.3e-3✱ · `మ` 0.87 · `మ` 8.9e-3✱ · `్య` 6.4e-4✱ · `మ` 0.92 · `తి` 0.88 · `మ` 1.8e-3✱ · `్య` 1.4e-5✱ · `రి` 0.96 · `ల` 0.02✱ · `్` 6.6e-9✱ · `⏎` 0.09✱ forced |
| 4 | `ము` 0.11 · `రి` 0.04✱ · `త` 0.99 · `ను` 0.90 · `మ` 0.57 · `్య` 1.7e-3✱ · `మ` 0.97 · `మ` 0.97 · `మ` 0.89 · `్య` 0.18✱ · `మ` 0.99 · `మ` 0.41 · `్య` 0.02✱ · `తి` 0.90 · `ము` 4.5e-3✱ · `మ` 1.2e-3✱ · `్య` 8.1e-4✱ · `␣ల` 1.4e-3✱ · `్య` 1.7e-3✱ · `్య` 6.5e-4✱ · `ై` 3.6e-4✱ · `య` 4.1e-3✱ · `య` 0.02✱ · `ము` 0.01✱ · `న` 1.1e-3✱ · `్య` 1.4e-4✱ · `ల` 7.0e-5✱ · `ీ` 2.9e-4✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 123 tokens · 30.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శకర లభ్వ సరణ్య జజ్రు గు ల్య్య్జల్య రాముడు సీశకర్ | `IIIUIIUIUIIUIUIIUIU` |
| 2 | వకరణీయ జజై గు లల్య్య్జల ల్వన్న్డు సశ్వరశశ్రరస్ | `IIIUIIUIUIIUIUIIUIU` |
| 3 | జ్ర్రు కుల ల్యల్యల ల్యంకకుళ్ళినె జోకరల్రియ ప్రస్ర్య జజ్ | `IIIUIIUIUIIUIUIIUIU` |
| 4 | ల్య్య్య కల లత్యను కాడడుం నియు ల్యవ్యమున్ జెడురీడుడువ్ | `IIIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.017 · model's first choice kept 38% · constraint overrode 55% · backtracks 0

<details><summary>Token probabilities (123 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.24✱ · `క` 0.02 · `ర` 0.02 · `␣ల` 0.02 · `భ` 3.1e-3 · `్వ` 6.3e-4✱ · `␣స` 0.15 · `రణ` 7.1e-4 · `్య` 6.7e-4✱ · `␣జ` 0.65 · `జ` 0.25 · `్రు` 1.6e-3✱ · `␣గు` 0.36 · `␣` 1.9e-3✱ · `ల` 0.02✱ · `్య` 4.1e-3✱ · `్య` 6.0e-3✱ · `్` 2.4e-6✱ · `జ` 0.02✱ · `ల` 0.02✱ · `్య` 2.8e-4✱ · `␣రా` 0.99 · `ము` 0.99 · `డు` 0.93 · `␣సీ` 3.9e-5✱ · `శ` 0.96 · `క` 0.95 · `ర` 0.96 · `్` 1.6e-8✱ · `⏎` 1.2e-4✱ forced |
| 2 | `వ` 0.31 · `క` 4.6e-4✱ · `రణ` 0.73 · `ీయ` 4.3e-3✱ · `␣జ` 0.93 · `జ` 0.96 · `ై` 4.3e-3✱ · `␣గు` 0.71 · `␣ల` 0.27 · `ల` 0.52 · `్య` 0.73 · `్య` 0.77 · `్` 0.21 · `జ` 0.58 · `ల` 0.57 · `␣ల` 0.21✱ · `్వ` 3.7e-4✱ · `న్` 0.58 · `న్` 2.4e-3✱ · `డు` 0.56 · `␣స` 1.6e-3✱ · `శ` 0.44 · `్వర` 9.3e-4✱ · `శ` 0.10✱ · `శ` 0.51 · `్ర` 1.5e-5✱ · `ర` 0.60 · `స` 0.06✱ · `్` 1.1e-8✱ · `⏎` 0.02✱ forced |
| 3 | `జ` 0.77 · `్ర` 2.6e-4✱ · `్రు` 3.7e-4✱ · `␣` 7.5e-4✱ · `కు` 2.5e-5✱ · `ల` 0.53 · `␣ల` 0.07✱ · `్య` 0.74 · `ల` 0.05 · `్య` 0.07✱ · `ల` 0.61 · `␣ల` 0.02✱ · `్య` 0.06✱ · `ంక` 0.99 · `కు` 0.99 · `ళ్ళ` 9.8e-5✱ · `ిన` 7.1e-3✱ · `ె` 0.99 · `␣జ` 1.5e-4✱ · `ో` 4.6e-4✱ · `క` 0.98 · `ర` 0.98 · `ల` 0.07✱ · `్రియ` 1.4e-5✱ · `␣ప్ర` 5.4e-6✱ · `స` 0.97 · `్ర` 6.7e-4✱ · `్య` 0.95 · `␣జ` 0.90 · `జ` 0.99 · `్` 3.4e-7✱ · `⏎` 0.02✱ forced |
| 4 | `ల` 0.30 · `్య` 0.02✱ · `్య` 0.93 · `్య` 0.97 · `␣` 2.7e-3✱ · `క` 4.4e-4✱ · `ల` 0.99 · `␣ల` 0.05✱ · `త` 1.9e-3✱ · `్య` 4.9e-5✱ · `ను` 0.99 · `␣కా` 0.90 · `డ` 0.99 · `డు` 0.95 · `ం` 1.2e-5✱ · `␣ని` 0.03✱ · `యు` 5.8e-3✱ · `␣ల` 0.03✱ · `్య` 0.05✱ · `వ` 3.7e-3✱ · `్య` 5.1e-3✱ · `ము` 0.11 · `న్` 0.02✱ · `␣జ` 0.03✱ · `ె` 0.04✱ · `డు` 8.1e-3✱ · `రీ` 3.6e-5✱ · `డు` 1.1e-3✱ · `డు` 9.9e-3✱ · `వ` 9.9e-6✱ · `్` 2.3e-4✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 100 tokens · 47.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కరుణ లాల్య మ మద్రి దైవ మ్రుకక్వనిల్రుచునుట్లుతౌన్ | `IIIUIIUIUIIUIUIIUIU` |
| 2 | చరణముల్ల మ లో మ ప్రేమల సాటిముడ్రియ లేదు మమ్ | `IIIUIIUIUIIUIUIIUIU` |
| 3 | మృర మ లో మ క ప్రేమ గొప్పది ఏది లోకము లోన్ జనత్ | `IIIUIIUIUIIUIUIIUIU` |
| 4 | తరల సాటిముడయ్రియణ్య మ మ్య్య్తై ల ల్యమ్రిమమున్రురున్ | `IIIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 23% · single-akshara words 42% · repeated lines 0 · mean token probability (geometric) 0.026 · model's first choice kept 50% · constraint overrode 42% · backtracks 30

<details><summary>Token probabilities (100 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.98 · `రుణ` 0.93 · `␣ల` 0.05 · `ాల` 0.97 · `్య` 0.95 · `␣మ` 0.82 · `␣మ` 0.26 · `ద` 0.02 · `్రి` 0.94 · `␣ద` 0.98 · `ై` 0.98 · `వ` 0.98 · `␣మ` 0.89 · `్రు` 5.8e-7✱ · `క` 7.7e-5✱ · `క` 2.0e-5✱ · `్వ` 0.22 · `ని` 0.45 · `ల` 3.2e-5✱ · `్రు` 4.0e-4✱ · `చు` 0.98 · `ను` 0.96 · `ట్లు` 1.4e-6✱ · `త` 0.12 · `ౌ` 0.61 · `న` 0.62 · `్` 2.8e-6✱ · `⏎` 0.73 |
| 2 | `చ` 1.2e-3 · `రణ` 0.22 · `ము` 0.38 · `ల్ల` 0.99 · `␣మ` 0.02 · `␣లో` 0.83 · `␣మ` 0.58 · `␣ప్రేమ` 0.01 · `ల` 0.03 · `␣సా` 0.08✱ · `టి` 0.63 · `ము` 0.14 · `డ` 4.6e-3✱ · `్రియ` 2.0e-4✱ · `␣లేదు` 0.82 · `␣మ` 9.8e-4✱ · `మ` 0.72 · `్` 9.7e-6✱ · `⏎` 0.97 |
| 3 | `మ` 0.70 · `ృ` 0.01✱ · `ర` 5.0e-4✱ · `␣మ` 0.41 · `␣లో` 0.08 · `␣మ` 0.72 · `␣క` 0.68 · `␣ప్రేమ` 0.65 · `␣గొప్ప` 0.71 · `ది` 0.59 · `␣ఏ` 0.99 · `ది` 0.66 · `␣లో` 0.98 · `క` 0.97 · `ము` 0.88 · `␣లో` 0.22 · `న్` 0.77 · `␣` 3.5e-4✱ · `జ` 0.85 · `న` 0.51 · `త` 0.01✱ · `్` 2.3e-5✱ · `⏎` 0.21✱ forced |
| 4 | `త` 0.28 · `ర` 3.8e-4✱ · `ల` 0.96 · `␣సా` 1.00 · `టి` 0.98 · `ము` 0.95 · `డ` 0.98 · `య` 3.6e-4✱ · `్రియ` 2.8e-4✱ · `ణ` 2.4e-4✱ · `్య` 4.3e-4✱ · `␣మ` 0.02✱ · `␣మ` 0.03✱ · `్య` 2.9e-4✱ · `్య` 4.3e-5✱ · `్` 3.3e-7✱ · `త` 1.7e-6✱ · `ై` 3.3e-3✱ · `␣ల` 1.2e-3✱ · `␣ల` 0.04✱ · `్య` 1.3e-3✱ · `మ` 0.03✱ · `్రి` 2.3e-3✱ · `మ` 2.7e-3✱ · `ము` 0.01✱ · `న` 0.02✱ · `్రు` 5.4e-3✱ · `రు` 1.7e-3✱ · `న` 0.11✱ · `్` 3.0e-5✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 106 tokens · 49.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జగమతిన్ నిల అన్రు ధైజ్య మెజగ్రిడెన్రు చడవ్యతింట్ | `IIIUIIUIUIIUIUIIUIU` |
| 2 | నిగమకమ్య మనమ్ర ప్రేమ మమృణ్యకమ్య మతిన్న్సతమ్ | `IIIUIIUIUIIUIUIIUIU` |
| 3 | పగవలక్యమునక్య మణ్య మవన్రు మత్రియ ప్రేమ లోక్ | `IIIUIIUIUIIUIUIIUIU` |
| 4 | మగ మ మన్రమ మమ్య ప్రేమ మమమ్యమల్యముమమ్యశమ్ | `IIIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 22% · single-akshara words 9% · repeated lines 0 · mean token probability (geometric) 0.016 · model's first choice kept 44% · constraint overrode 45% · backtracks 30

<details><summary>Token probabilities (106 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.95 · `గ` 0.93 · `మ` 8.5e-3 · `తి` 0.11✱ · `న్` 0.92 · `␣ని` 0.93 · `ల` 0.90 · `␣అ` 0.93 · `న` 0.88 · `్రు` 3.1e-6✱ · `␣ధ` 0.99 · `ై` 0.98 · `జ్య` 8.3e-5 · `␣మె` 7.3e-4 · `జ` 5.1e-4 · `గ` 0.03 · `్రి` 0.97 · `డ` 1.00 · `ె` 0.94 · `న` 5.9e-6✱ · `్రు` 7.4e-3✱ · `␣చ` 0.43 · `డ` 0.79 · `వ` 0.89 · `్య` 2.9e-6✱ · `తి` 7.7e-4✱ · `ంట` 0.88 · `్` 3.1e-7✱ · `⏎` 0.83 forced |
| 2 | `న` 0.01 · `ి` 3.0e-6✱ · `గ` 3.9e-3✱ · `మ` 0.64 · `క` 0.01 · `మ` 0.04✱ · `్య` 1.8e-3✱ · `␣మ` 0.28 · `న` 0.01 · `మ` 0.06✱ · `్ర` 3.8e-4✱ · `␣ప్రేమ` 0.02 · `␣మ` 0.08 · `మ` 0.20 · `ృ` 1.8e-3✱ · `ణ` 0.11✱ · `్య` 0.01✱ · `క` 0.99 · `మ` 0.97 · `్య` 0.94 · `␣మ` 0.95 · `తి` 0.91 · `న్` 0.97 · `న్` 1.1e-3✱ · `స` 0.72 · `త` 0.87 · `మ` 0.78 · `్` 9.1e-8✱ · `⏎` 0.85 |
| 3 | `ప` 0.98 · `గ` 1.1e-5✱ · `వల` 0.95 · `క` 5.0e-3✱ · `్య` 4.9e-5✱ · `ము` 0.89 · `న` 0.65 · `క` 5.4e-4✱ · `్య` 3.9e-6✱ · `␣మ` 0.52 · `ణ` 0.71 · `్య` 0.50 · `␣మ` 0.88 · `వ` 9.5e-5✱ · `న` 5.4e-3✱ · `్రు` 2.5e-4✱ · `␣మ` 0.71 · `త` 0.53 · `్రియ` 3.1e-5✱ · `␣ప్రేమ` 0.91 · `␣లో` 1.00 · `క` 1.00 · `్` 9.6e-12✱ · `⏎` 4.5e-6✱ forced |
| 4 | `మ` 0.13 · `గ` 2.1e-4✱ · `␣మ` 0.89 · `␣మ` 2.8e-4✱ · `న` 0.44 · `్రమ` 5.8e-5✱ · `␣మ` 0.89 · `మ` 1.9e-3✱ · `్య` 8.0e-5✱ · `␣ప్రేమ` 0.02✱ · `␣మ` 3.5e-3✱ · `మ` 0.02✱ · `మ` 7.7e-3✱ · `్య` 7.2e-4✱ · `మ` 2.1e-3✱ · `ల` 3.6e-3✱ · `్య` 3.0e-3✱ · `ము` 0.40 · `మ` 0.08✱ · `మ` 0.08✱ · `్య` 3.4e-3✱ · `శ` 5.1e-5✱ · `మ` 6.1e-3✱ · `్` 3.9e-4✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 106 tokens · 31.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమల నిల్ర సమర్య జల్రి గె జ్వ్వ్కక్రమమ్రి నిలజ్రిమర్ | `IIIUIIUIUIIUIUIIUIU` |
| 2 | లము మతిన్వ్వవలక్రమమ్రిమలల్రిజస్రరలజ్యధిన్ | `IIIUIIUIUIIUIUIIUIU` |
| 3 | జ్వమమకక్రమమత్రి నిల్ర ససర్య జల్రి మతిజ్వలౌ | `IIIUIIUIUIIUIUIIUIU` |
| 4 | కము సమమ్యతిదిల్ల లక్రియకక్యకక్యకకక్రి సా | `IIIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.021 · model's first choice kept 31% · constraint overrode 62% · backtracks 0

<details><summary>Token probabilities (106 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.04 · `మ` 0.32 · `ల` 0.62 · `␣ని` 0.06 · `ల` 0.36 · `్ర` 1.1e-3✱ · `␣స` 0.13 · `మ` 0.03 · `ర` 0.16 · `్య` 3.8e-5✱ · `␣జ` 0.41 · `ల` 0.06✱ · `్రి` 2.1e-4✱ · `␣గ` 0.06 · `ె` 0.08✱ · `␣జ` 0.02✱ · `్వ` 3.7e-3✱ · `్వ` 6.7e-4✱ · `్` 1.5e-5✱ · `క` 0.05✱ · `క` 0.02✱ · `్రమ` 8.5e-7✱ · `మ` 0.90 · `్రి` 2.5e-5✱ · `␣ని` 0.93 · `ల` 0.97 · `జ` 0.30✱ · `్రి` 1.9e-4✱ · `మ` 0.98 · `ర` 0.91 · `్` 1.4e-5✱ · `⏎` 3.4e-4✱ forced |
| 2 | `ల` 0.94 · `ము` 9.3e-4✱ · `␣మ` 0.96 · `తి` 0.97 · `న్` 8.5e-5✱ · `వ్వ` 0.06✱ · `వల` 9.3e-4✱ · `క` 0.10✱ · `్రమ` 8.3e-4✱ · `మ` 0.05✱ · `్రి` 4.8e-3✱ · `మ` 0.36 · `ల` 0.72 · `ల` 0.10✱ · `్రి` 6.1e-4✱ · `జ` 0.16✱ · `స` 0.72 · `్ర` 7.2e-5✱ · `ర` 0.73 · `ల` 8.2e-3✱ · `జ` 0.07✱ · `్య` 1.6e-3✱ · `ధి` 0.91 · `న్` 1.1e-4✱ · `⏎` 3.6e-4✱ forced |
| 3 | `␣జ` 0.28 · `్వ` 0.70 · `మ` 1.7e-4✱ · `మ` 0.07 · `క` 0.43 · `క` 0.05✱ · `్రమ` 0.01✱ · `మ` 0.79 · `త్రి` 5.9e-3✱ · `␣ని` 0.70 · `ల` 0.95 · `్ర` 0.02✱ · `␣స` 0.92 · `స` 1.9e-3✱ · `ర` 0.96 · `్య` 0.96 · `␣జ` 0.86 · `ల` 0.95 · `్రి` 1.6e-4✱ · `␣మ` 0.95 · `తి` 0.92 · `జ` 0.05✱ · `్వ` 0.99 · `ల` 2.3e-3✱ · `ౌ` 1.1e-3✱ · `⏎` 1.4e-3 forced |
| 4 | `క` 0.02✱ · `ము` 4.4e-4✱ · `␣స` 1.5e-3✱ · `మ` 0.02✱ · `మ` 0.02✱ · `్య` 1.5e-3✱ · `తి` 5.5e-3✱ · `ది` 5.9e-3✱ · `ల్ల` 3.7e-3✱ · `␣ల` 0.03✱ · `క` 0.09✱ · `్రియ` 4.6e-5✱ · `క` 2.2e-3✱ · `క` 0.07✱ · `్య` 3.8e-3✱ · `క` 0.02✱ · `క` 0.30 · `్య` 1.7e-3✱ · `క` 0.03✱ · `క` 0.07✱ · `క` 0.12✱ · `్రి` 6.5e-5✱ · `␣సా` 4.2e-3✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 114 tokens · 26.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జగముటన్ మ మనిల్ర మమ్రన మ్ర్య్జన్రుడైనినికక్రమన్ | `IIIUIIUIUIIUIUIIUIU` |
| 2 | మృగ సమిల్రమమల్యరత్యవకృత్యముమ్రనిలవ్రమా | `IIIUIIUIUIIUIUIIUIU` |
| 3 | నగయు నిర్యము మమ్య వందన మ్ర్ర్యవ్రుమార్న మయుమ్యమా | `IIIUIIUIUIIUIUIIUIU` |
| 4 | యిగము మౌనినిలల్రవమ్రజగృట్ మృనిల్రమమార్న మర్ | `IIIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.026 · model's first choice kept 47% · constraint overrode 46% · backtracks 0

<details><summary>Token probabilities (114 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.23 · `గ` 0.40 · `ము` 0.32 · `ట` 0.01 · `న్` 0.31 · `␣మ` 0.09 · `␣మ` 0.08 · `ని` 0.04 · `ల` 0.02✱ · `్ర` 2.3e-4✱ · `␣మ` 0.06 · `మ` 0.05✱ · `్ర` 6.7e-4✱ · `న` 0.03 · `␣మ` 0.18 · `్ర` 1.4e-3✱ · `్య` 1.4e-4✱ · `్` 3.8e-7✱ · `జ` 0.20 · `న` 0.04✱ · `్రు` 4.3e-5✱ · `డ` 0.37 · `ై` 0.10 · `ని` 1.0e-2✱ · `ని` 0.04✱ · `క` 0.13✱ · `క` 0.33 · `్రమ` 4.6e-5✱ · `న్` 0.02✱ · `⏎` 2.8e-5✱ forced |
| 2 | `␣మ` 0.31 · `ృ` 0.02✱ · `గ` 3.5e-3✱ · `␣స` 0.73 · `మి` 0.93 · `ల` 0.95 · `్ర` 6.0e-4✱ · `మ` 0.03 · `మ` 0.71 · `ల` 7.8e-3✱ · `్య` 1.8e-4✱ · `ర` 0.84 · `త` 0.81 · `్య` 1.5e-4✱ · `వ` 3.7e-3✱ · `క` 0.75 · `ృత` 1.5e-5✱ · `్య` 1.3e-3✱ · `ము` 0.21✱ · `మ` 0.23✱ · `్ర` 2.7e-5✱ · `ని` 0.75 · `ల` 0.86 · `వ` 0.89 · `్ర` 1.9e-4✱ · `మా` 5.2e-3 · `⏎` 1.5e-3✱ forced |
| 3 | `న` 0.65 · `గ` 2.6e-3✱ · `యు` 0.93 · `␣ని` 0.98 · `ర` 0.99 · `్య` 3.3e-6✱ · `ము` 0.52 · `␣మ` 0.90 · `మ` 0.87 · `్య` 5.0e-5✱ · `␣వ` 0.95 · `ంద` 0.94 · `న` 0.97 · `␣మ` 0.95 · `్ర` 9.7e-7✱ · `్ర` 4.9e-5✱ · `్య` 2.0e-5✱ · `వ` 0.77 · `్రు` 6.8e-5✱ · `మ` 0.88 · `ార్` 0.97 · `న` 0.95 · `␣మ` 0.81 · `యు` 0.89 · `మ` 1.1e-3✱ · `్య` 1.3e-4✱ · `మా` 1.1e-4✱ · `⏎` 0.04✱ forced |
| 4 | `యి` 8.6e-4✱ · `గ` 4.1e-4✱ · `ము` 0.16✱ · `␣మ` 0.21 · `ౌ` 0.01✱ · `ని` 0.14 · `ని` 0.15✱ · `ల` 0.06✱ · `ల` 0.10 · `్ర` 9.4e-3✱ · `వ` 0.03✱ · `మ` 0.12 · `్ర` 8.4e-3✱ · `జ` 0.60 · `గ` 0.47 · `ృ` 3.2e-5✱ · `ట` 0.95 · `్` 1.3e-5✱ · `␣మ` 0.73 · `ృ` 9.5e-4✱ · `ని` 0.76 · `ల` 0.57 · `్ర` 0.13 · `మ` 0.42 · `మ` 0.58 · `ార్` 0.44 · `న` 0.51 · `␣మ` 0.31 · `ర్` 8.3e-3 |

</details>

[↑ meters](#meters)

---

<a id="malini"></a>

## 31. మాలిని (malini)

```text
Meter: మాలిని (malini), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 5 gaṇas: న న మ య య, i.e. III III UUU IUU IUU (15 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter మాలిని (malini).

Meter: మాలిని (malini), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 5 gaṇas: న న మ య య, i.e. III III UUU IUU IUU (15 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 92 tokens · 21.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సమమ సిమముతుండన్ శౌకగమ్యన్యుసమ్యా | `IIIIIIUUUIUUIUU` |
| 2 | మమకతమ మచిత్రన్ ల్య్ర్మర్య జక్రియ్యవస్యా | `IIIIIIUUUIUUIUU` |
| 3 | సమమ హనుజతుడ్యత్య్య్శమ్యముక్యంయవవ్యం | `IIIIIIUUUIUUIUU` |
| 4 | డి మ మతిని ఛ ఛందున్య్య్టిమ్యరాసమ్యనున్రియ్ | `IIIIIIUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 21% · single-akshara words 21% · repeated lines 0 · mean token probability (geometric) 0.012 · model's first choice kept 33% · constraint overrode 55% · backtracks 0

<details><summary>Token probabilities (92 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 0.01 · `మ` 0.23 · `మ` 0.08 · `␣సి` 3.3e-3 · `మ` 0.05 · `ము` 0.06 · `తు` 4.4e-3 · `ండ` 0.03✱ · `న్` 0.03✱ · `␣శ` 0.16 · `ౌ` 5.7e-3 · `క` 0.04 · `గ` 0.02 · `మ` 0.22✱ · `్య` 0.16 · `న్` 0.29 · `యు` 7.3e-3✱ · `స` 0.65 · `మ` 0.65 · `్యా` 1.6e-3✱ · `⏎` 0.04 forced |
| 2 | `మ` 0.73 · `మ` 0.25 · `క` 0.06 · `త` 0.04 · `మ` 6.8e-3✱ · `␣మ` 0.10 · `చిత` 4.3e-3✱ · `్ర` 0.05✱ · `న్` 0.10✱ · `␣ల` 0.68 · `్య` 7.1e-5✱ · `్ర` 7.0e-5✱ · `్` 5.5e-7✱ · `మ` 0.10 · `ర` 0.02 · `్య` 6.2e-4✱ · `␣జ` 0.02 · `క` 0.04✱ · `్రియ` 1.2e-3✱ · `్య` 1.7e-4✱ · `వ` 1.4e-3✱ · `స` 0.22✱ · `్యా` 1.9e-3✱ · `⏎` 0.61 |
| 3 | `స` 0.62 · `మ` 0.80 · `మ` 0.54 · `␣హ` 0.93 · `ను` 0.56 · `జ` 0.04✱ · `తు` 0.62 · `డ` 0.02✱ · `్య` 1.9e-3✱ · `త` 4.3e-4✱ · `్య` 8.1e-5✱ · `్య` 1.5e-3✱ · `్` 5.4e-8✱ · `శ` 4.2e-4✱ · `మ` 9.9e-3✱ · `్య` 0.01✱ · `ము` 0.45 · `క` 2.6e-3✱ · `్యం` 3.8e-3✱ · `య` 2.3e-3✱ · `వ` 0.07✱ · `వ` 0.02✱ · `్యం` 1.2e-4✱ · `⏎` 0.02✱ forced |
| 4 | `డి` 0.33 · `␣మ` 3.4e-3✱ · `␣మ` 0.56 · `తి` 0.02✱ · `ని` 0.56 · `␣ఛ` 0.59 · `␣ఛ` 0.27 · `ందు` 0.03 · `న` 0.04 · `్య` 9.6e-6✱ · `్య` 2.2e-3✱ · `్` 3.4e-5✱ · `టి` 2.9e-3✱ · `మ` 4.6e-3✱ · `్య` 1.6e-3✱ · `రా` 0.10✱ · `స` 0.75 · `మ` 1.7e-3✱ · `్య` 1.2e-3✱ · `ను` 2.5e-3✱ · `న` 6.2e-4✱ · `్రియ` 4.4e-5✱ · `్` 5.7e-6✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 91 tokens · 20.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కరుణ మ మర మక్యం మ్ర్ల్కమ్రలమ్యం తమక్యం | `IIIIIIUUUIUUIUU` |
| 2 | కృరణమ మర మక్యం వ్రిన్రువక్యామమొత్రుక్ | `IIIIIIUUUIUUIUU` |
| 3 | మ్రురమ మర మకల్లో మొర్ర మృణ్రుయ్యతమ్యం | `IIIIIIUUUIUUIUU` |
| 4 | నరుమమ మక మయ్యంయయ్య మాలిన్యుమత్యా | `IIIIIIUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 21% · single-akshara words 5% · repeated lines 0 · mean token probability (geometric) 0.025 · model's first choice kept 42% · constraint overrode 47% · backtracks 0

<details><summary>Token probabilities (91 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.06 · `రుణ` 0.28 · `␣మ` 0.29 · `␣మ` 0.05 · `ర` 0.04 · `␣మ` 0.13 · `క` 0.04✱ · `్యం` 1.6e-3✱ · `␣మ` 0.51 · `్ర` 1.5e-3✱ · `్` 2.5e-5✱ · `ల` 0.03✱ · `్` 7.5e-9✱ · `క` 0.01✱ · `మ` 0.10✱ · `్ర` 6.3e-4✱ · `ల` 0.28 · `మ` 0.11 · `్యం` 3.9e-3✱ · `␣` 6.7e-3✱ · `త` 0.22✱ · `మ` 0.37 · `క` 0.06 · `్యం` 1.8e-3✱ · `⏎` 0.78 |
| 2 | `క` 0.77 · `ృ` 1.7e-4✱ · `రణ` 3.4e-3✱ · `మ` 0.20 · `␣మ` 0.54 · `ర` 0.75 · `␣మ` 0.62 · `క` 0.75 · `్యం` 0.73 · `␣వ` 0.10 · `్ర` 0.25 · `ిన` 0.01✱ · `్రు` 6.2e-4✱ · `వ` 0.14 · `క` 0.02 · `్యా` 8.4e-4✱ · `మ` 0.39 · `మ` 0.08 · `ొ` 8.4e-3✱ · `త` 0.24✱ · `్రు` 2.8e-4✱ · `క` 0.93 · `్` 1.1e-7✱ · `⏎` 0.99 |
| 3 | `మ` 0.99 · `్రు` 5.5e-5✱ · `ర` 1.00 · `మ` 0.98 · `␣మ` 0.89 · `ర` 0.98 · `␣మ` 0.97 · `క` 0.97 · `ల్లో` 1.8e-6✱ · `␣మ` 9.5e-4✱ · `ొ` 5.9e-4✱ · `ర` 0.96 · `్ర` 1.2e-3✱ · `␣మ` 0.85 · `ృ` 0.97 · `ణ` 0.98 · `్రు` 8.2e-5✱ · `య` 0.96 · `్య` 1.5e-4✱ · `త` 0.83 · `మ` 0.86 · `్యం` 3.7e-5✱ · `⏎` 0.10 forced |
| 4 | `న` 2.4e-3✱ · `రు` 1.6e-3✱ · `మ` 0.01✱ · `మ` 0.07✱ · `␣మ` 0.15✱ · `క` 0.11✱ · `␣మ` 0.14 · `య` 0.16 · `్యం` 3.8e-3✱ · `య` 1.1e-3✱ · `య` 0.04✱ · `్య` 1.2e-3✱ · `␣మ` 0.21✱ · `ాలి` 0.13 · `న్` 1.5e-3✱ · `యు` 0.27 · `మ` 0.30 · `త` 0.04 · `్యా` 3.7e-4✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 92 tokens · 37.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమలి హ తర మమ్ర్యుత్య్వ్గర్యులైనో తమించున్ | `IIIIIIUUUIUUIUU` |
| 2 | మమ స త ర మ సుమ్రింజ్రమ్యనుండాటి సస్రియ్ | `IIIIIIUUUIUUIUU` |
| 3 | సమ మతి ల లకక్రేర్ర్ర్జన్సతమ్యం జజమ్యన్ | `IIIIIIUUUIUUIUU` |
| 4 | బముముగగమనిక్రమ్ర్య్వందతిల్రమ్రమన్రా | `IIIIIIUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 22% · single-akshara words 33% · repeated lines 0 · mean token probability (geometric) 0.018 · model's first choice kept 43% · constraint overrode 46% · backtracks 30

<details><summary>Token probabilities (92 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.86 · `మ` 0.96 · `లి` 0.11 · `␣హ` 0.02 · `␣త` 5.3e-4✱ · `ర` 0.67 · `␣మ` 0.03 · `మ` 0.91 · `్ర` 0.76 · `్య` 0.41 · `ు` 0.90 · `త` 0.37 · `్య` 0.40 · `్వ` 2.5e-4✱ · `్` 6.4e-6✱ · `గర` 0.99 · `్య` 4.3e-5✱ · `ు` 7.4e-3✱ · `ల` 0.96 · `ైన` 0.98 · `ో` 2.6e-3 · `␣త` 2.5e-3 · `మ` 0.92 · `ించు` 0.99 · `న్` 0.99 · `⏎` 0.99 |
| 2 | `మ` 0.70 · `మ` 0.87 · `␣స` 8.1e-3 · `␣త` 0.13 · `␣ర` 0.19 · `␣మ` 0.10 · `␣సు` 0.95 · `మ` 0.12 · `్రి` 0.93 · `ంజ` 0.97 · `్ర` 4.5e-5✱ · `మ` 4.7e-3✱ · `్య` 1.3e-4✱ · `ను` 0.90 · `ండా` 9.9e-5✱ · `టి` 0.96 · `␣స` 1.1e-3✱ · `స` 0.95 · `్రియ` 7.3e-4✱ · `్` 1.2e-6✱ · `⏎` 0.39 forced |
| 3 | `స` 0.19 · `మ` 0.56 · `␣మ` 0.31 · `తి` 0.93 · `␣ల` 0.99 · `␣ల` 2.6e-4✱ · `క` 0.95 · `క` 5.8e-3✱ · `్రే` 8.2e-6✱ · `ర` 0.91 · `్ర` 6.5e-6✱ · `్ర` 2.4e-4✱ · `్` 4.2e-7✱ · `జ` 6.9e-3✱ · `న్` 0.02✱ · `స` 4.8e-4✱ · `త` 0.86 · `మ` 0.58 · `్యం` 2.3e-4✱ · `␣` 0.01✱ · `జ` 0.02✱ · `జ` 0.32 · `మ` 0.02✱ · `్య` 3.4e-4✱ · `న్` 0.24 · `⏎` 2.3e-5✱ forced |
| 4 | `బ` 1.7e-3✱ · `ము` 0.02✱ · `ము` 0.16✱ · `గ` 2.2e-3✱ · `గ` 0.62 · `మని` 0.91 · `క` 0.92 · `్ర` 5.2e-6✱ · `మ` 0.04✱ · `్ర` 1.9e-5✱ · `్య` 1.9e-3✱ · `్వ` 6.3e-6✱ · `ంద` 0.86 · `తి` 0.01✱ · `ల` 3.7e-4✱ · `్రమ` 7.4e-4✱ · `్రమ` 3.6e-4✱ · `న` 8.6e-3✱ · `్రా` 1.5e-5✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 93 tokens · 45.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమ మ ల ని య యల్ల్యశ్ర్య్కత్రి చేడుండు ధస్రమ్ | `IIIIIIUUUIUUIUU` |
| 2 | ని మ హల హ సముద్రుండెన్న్న రమ్యం మ మల్లల్ | `IIIIIIUUUIUUIUU` |
| 3 | నమ సిముడు నమల్రింప్యల్రి మల్యం జయమ్యాన్ | `IIIIIIUUUIUUIUU` |
| 4 | రమడెనునునునుత్యోరమ్య మల్యన్రమమ్యమ్ | `IIIIIIUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 35% · repeated lines 0 · mean token probability (geometric) 0.024 · model's first choice kept 40% · constraint overrode 49% · backtracks 30

<details><summary>Token probabilities (93 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.94 · `మ` 0.97 · `␣మ` 0.81 · `␣ల` 0.89 · `␣ని` 0.93 · `␣య` 0.49 · `␣య` 0.60 · `ల్ల` 0.99 · `్య` 0.99 · `శ` 7.1e-5✱ · `్ర` 0.98 · `్య` 6.9e-6✱ · `్` 6.4e-9✱ · `క` 0.86 · `త` 0.72 · `్రి` 0.91 · `␣చే` 1.00 · `డు` 4.8e-5 · `ండు` 0.97 · `␣ధ` 1.0e-6✱ · `స` 0.83 · `్రమ` 2.1e-4✱ · `్` 2.9e-6✱ · `⏎` 1.4e-3✱ forced |
| 2 | `␣ని` 0.67 · `␣మ` 0.90 · `␣హ` 4.0e-3 · `ల` 5.9e-3✱ · `␣హ` 7.2e-4✱ · `␣స` 0.87 · `ము` 0.98 · `ద్ర` 0.98 · `ు` 1.2e-3✱ · `ం` 1.5e-3✱ · `డ` 0.90 · `ె` 0.97 · `న్` 2.6e-3✱ · `న్` 2.9e-3✱ · `న` 0.18 · `␣ర` 0.14 · `మ` 0.10✱ · `్యం` 2.2e-4✱ · `␣మ` 0.30 · `␣మ` 0.59 · `ల్ల` 0.16✱ · `ల్` 5.8e-3✱ · `⏎` 0.11✱ forced |
| 3 | `న` 0.08 · `మ` 0.04 · `␣సి` 2.4e-3 · `ము` 0.68 · `డు` 0.01 · `␣న` 0.02 · `మ` 0.07 · `ల` 0.33 · `్రి` 0.89 · `ంప` 0.65 · `్య` 4.0e-4✱ · `ల` 3.9e-3✱ · `్రి` 9.5e-5✱ · `␣మ` 0.18 · `ల` 0.08 · `్యం` 3.5e-4✱ · `␣జ` 0.04✱ · `య` 0.25 · `మ` 0.03✱ · `్య` 0.04✱ · `ాన` 0.89 · `్` 4.0e-5✱ · `⏎` 5.5e-4✱ forced |
| 4 | `ర` 0.82 · `మ` 0.04✱ · `డ` 0.94 · `ె` 0.92 · `ను` 0.78 · `ను` 3.6e-3✱ · `ను` 7.1e-3✱ · `ను` 9.0e-3✱ · `త` 1.1e-3✱ · `్య` 4.8e-4✱ · `ో` 0.01✱ · `ర` 0.02✱ · `మ` 0.02✱ · `్య` 5.8e-3✱ · `␣మ` 0.02✱ · `ల` 0.04✱ · `్య` 0.02✱ · `న` 4.0e-3✱ · `్రమ` 1.5e-5✱ · `మ` 6.2e-3✱ · `్య` 6.4e-3✱ · `మ` 0.06✱ · `్` 3.6e-4✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 99 tokens · 29.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శతృఘుఘ శలముర్వన్ర్వ్జన్రి లంకన్ మమత్రా | `IIIIIIUUUIUUIUU` |
| 2 | కతయ మతము సీతన్ శ్ర్య్కల్యమున్మత్యముమ్రీ | `IIIIIIUUUIUUIUU` |
| 3 | మతము జితినమున్మత్య్య్మయ్యతన్న్దేవివిమ్యా | `IIIIIIUUUIUUIUU` |
| 4 | లతముముమతముమ్యుమ్య్య్లల్యలట్టిట్టితిట్టిం | `IIIIIIUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 27% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.024 · model's first choice kept 35% · constraint overrode 58% · backtracks 0

<details><summary>Token probabilities (99 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.40 · `త` 0.12✱ · `ృ` 0.34 · `ఘ` 0.26 · `ు` 0.31✱ · `ఘ` 0.02 · `␣శ` 0.31 · `ల` 0.03✱ · `ము` 0.04 · `ర` 0.05✱ · `్వ` 1.3e-4✱ · `న` 0.03✱ · `్ర` 9.0e-5✱ · `్వ` 6.0e-4✱ · `్` 1.0e-5✱ · `జ` 0.09✱ · `న` 0.01✱ · `్రి` 1.3e-4✱ · `␣ల` 0.04 · `ంక` 0.51 · `న్` 0.14✱ · `␣మ` 3.8e-3✱ · `మ` 0.34 · `త` 0.27 · `్రా` 1.3e-3✱ · `⏎` 0.41 |
| 2 | `క` 0.09 · `త` 0.26 · `య` 0.03 · `␣మ` 0.06 · `త` 0.08 · `ము` 0.45 · `␣సీ` 0.05 · `త` 0.87 · `న్` 0.34 · `␣శ` 0.21 · `్ర` 2.9e-3✱ · `్య` 3.7e-4✱ · `్` 3.8e-7✱ · `క` 0.04✱ · `ల` 0.01✱ · `్య` 1.4e-3✱ · `ము` 0.79 · `న్` 0.02✱ · `మ` 0.44 · `త` 0.40 · `్య` 3.1e-3✱ · `ము` 0.03✱ · `మ` 0.15✱ · `్రీ` 1.7e-4✱ · `⏎` 0.02 forced |
| 3 | `␣మ` 0.52 · `త` 0.83 · `ము` 0.88 · `␣జ` 0.96 · `ిత` 3.7e-4✱ · `ిన` 5.8e-3✱ · `ము` 0.40 · `న్` 0.91 · `మ` 0.70 · `త` 0.83 · `్య` 0.41 · `్య` 0.05✱ · `్` 3.8e-5✱ · `మ` 0.01✱ · `య` 0.92 · `్య` 5.1e-4✱ · `త` 0.90 · `న్` 4.6e-3✱ · `న్` 0.02✱ · `దే` 0.51 · `వి` 0.52 · `వి` 0.17 · `మ` 5.8e-4✱ · `్యా` 2.0e-4✱ · `⏎` 5.8e-4✱ forced |
| 4 | `␣ల` 0.32 · `త` 6.3e-3✱ · `ము` 0.92 · `ము` 0.02✱ · `మ` 0.01✱ · `త` 8.6e-3✱ · `ము` 0.04✱ · `మ` 0.05✱ · `్య` 0.01✱ · `ు` 0.02✱ · `మ` 0.14 · `్య` 0.02✱ · `్య` 8.6e-3✱ · `్` 3.0e-5✱ · `ల` 0.04✱ · `ల` 0.04✱ · `్య` 1.2e-3✱ · `ల` 9.4e-3✱ · `ట్టి` 6.2e-4✱ · `ట్టి` 7.2e-3✱ · `తి` 5.0e-3✱ · `ట్టి` 6.9e-3✱ · `ం` 4.8e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 94 tokens · 20.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కరుణ మ మర మక్యం మ్ర్మ్కమ్రమమ్యం మకమ్యం | `IIIIIIUUUIUUIUU` |
| 2 | కరి మ మ మయకక్యం మ్ర్మ్కమ్రమమ్యం మకమ్యం | `IIIIIIUUUIUUIUU` |
| 3 | ఇరు ఇవ లపముందిన్ర్రృశ్యమించడ్యదున్యా | `IIIIIIUUUIUUIUU` |
| 4 | క్షర మణిని గణం నన్య్య్ఘం ఇ ఉర్ ఇర్ ఉ ఇర్ కా | `IIIIIIUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 36% · repeated lines 0 · mean token probability (geometric) 0.029 · model's first choice kept 34% · constraint overrode 55% · backtracks 0

<details><summary>Token probabilities (94 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.06 · `రుణ` 0.28 · `␣మ` 0.29 · `␣మ` 0.05 · `ర` 0.04 · `␣మ` 0.13 · `క` 0.04✱ · `్యం` 1.6e-3✱ · `␣మ` 0.51 · `్ర` 1.5e-3✱ · `్` 2.5e-5✱ · `మ` 0.19✱ · `్` 4.3e-7✱ · `క` 0.01✱ · `మ` 0.08✱ · `్ర` 2.7e-3✱ · `మ` 0.33 · `మ` 0.10 · `్యం` 1.3e-3✱ · `␣మ` 7.6e-3✱ · `క` 0.91 · `మ` 0.61 · `్యం` 7.6e-4✱ · `⏎` 0.56 forced |
| 2 | `క` 0.90 · `రి` 2.7e-3✱ · `␣మ` 0.55 · `␣మ` 0.65 · `␣మ` 0.06 · `య` 0.03 · `క` 0.11 · `క` 0.08✱ · `్యం` 0.04✱ · `␣మ` 0.71 · `్ర` 0.30 · `్` 0.21✱ · `మ` 0.96 · `్` 0.19✱ · `క` 0.92 · `మ` 0.80 · `్ర` 0.44 · `మ` 0.64 · `మ` 0.82 · `్యం` 0.75 · `␣మ` 0.75 · `క` 0.61 · `మ` 0.52 · `్యం` 0.38 · `⏎` 0.09✱ forced |
| 3 | `ఇ` 0.07✱ · `రు` 6.5e-3✱ · `␣ఇ` 0.09✱ · `వ` 4.9e-4✱ · `␣ల` 2.6e-4✱ · `ప` 0.71 · `ము` 0.02✱ · `ంది` 6.3e-4✱ · `న` 3.1e-3✱ · `్ర` 3.4e-6✱ · `్ర` 3.4e-5✱ · `ృ` 9.1e-4✱ · `శ` 0.07✱ · `్య` 0.01✱ · `మ` 0.25 · `ించ` 0.39 · `డ` 0.04✱ · `్య` 4.1e-4✱ · `దు` 0.86 · `న` 1.4e-3✱ · `్యా` 3.3e-4✱ · `⏎` 0.30 |
| 4 | `క్ష` 0.09✱ · `ర` 2.7e-3✱ · `␣మ` 0.99 · `ణి` 3.1e-3✱ · `ని` 0.96 · `␣గ` 0.75 · `ణం` 0.52 · `␣న` 2.0e-4✱ · `న` 0.01✱ · `్య` 4.3e-5✱ · `్య` 4.2e-3✱ · `్` 1.7e-4✱ · `ఘ` 6.2e-3✱ · `ం` 0.03✱ · `␣ఇ` 0.04✱ · `␣ఉ` 0.04✱ · `ర్` 1.1e-3✱ · `␣ఇ` 0.07✱ · `ర్` 0.01✱ · `␣ఉ` 0.15 · `␣ఇ` 0.02✱ · `ర్` 0.12✱ · `␣కా` 0.04 |

</details>

[↑ meters](#meters)

---

<a id="manini"></a>

## 32. మానిని (manini)

```text
Meter: మానిని (manini), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas: భ భ భ భ భ భ భ గురువు, i.e. UII UII UII UII UII UII UII U (22 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 7th and the 13th and the 19th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter మానిని (manini).

Meter: మానిని (manini), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas: భ భ భ భ భ భ భ గురువు, i.e. UII UII UII UII UII UII UII U (22 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 7th and the 13th and the 19th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 175 tokens · 45.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాము ల శక్రిమొ న్య్య్మల్య మకమ్రు జ మబ్రముమా తము ల్వ్ల్మౌ న్య్మలలమ్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 2 | ర్స్జ్యై మధుమా మము ల్యక్రిమొ న్య్య్లల్య మ మ్మ్ర్యబ్రముమా మము ల్యక్రిమొ న్య్య్మల్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 3 | కామ మ జబ్రము వ్వ్ర్లల్య మ ఈ ఇవ వ్ర్లల్య ల ల్యల్య మలల్యలలవ్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 4 | వ్యా మమునున్ ల ల్ల ల్యల్య్యలలల్యల ల్యణ్యలవవ్ ల్ల మ మ్స్స్యమ్ మర న్యల్ | `UIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 40% · repeated lines 0 · mean token probability (geometric) 0.019 · model's first choice kept 29% · constraint overrode 64% · backtracks 0

<details><summary>Token probabilities (175 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.02 · `ము` 0.07 · `␣ల` 0.05 · `␣శ` 0.03 · `క` 0.03 · `్రి` 0.04✱ · `మ` 0.03 · `ొ` 3.2e-3✱ · `␣న` 0.02✱ · `్య` 4.6e-4✱ · `్య` 9.7e-4✱ · `్` 3.1e-6✱ · `మ` 0.03✱ · `ల` 0.04✱ · `్య` 8.1e-4✱ · `␣మ` 0.08 · `క` 0.02 · `మ` 0.04✱ · `్రు` 2.5e-4✱ · `␣జ` 0.09 · `␣మ` 0.05 · `బ` 1.6e-3 · `్ర` 2.2e-3✱ · `ము` 0.11 · `మా` 0.13✱ · `␣త` 3.1e-4✱ · `ము` 0.11✱ · `␣ల` 0.18✱ · `్వ` 5.1e-4✱ · `్` 3.7e-4✱ · `ల` 0.11 · `్` 3.6e-7✱ · `మ` 9.3e-3✱ · `ౌ` 5.0e-3✱ · `␣న` 0.37 · `్య` 0.96 · `్` 0.83 · `మ` 0.92 · `ల` 0.95 · `ల` 0.08✱ · `మ` 0.01✱ · `్` 2.2e-5✱ · `⏎` 2.3e-5✱ forced |
| 2 | `ర్స్` 1.2e-3✱ · `జ` 3.6e-3✱ · `్య` 1.6e-4✱ · `ై` 5.2e-4✱ · `␣మ` 0.04✱ · `ధు` 0.05 · `మా` 0.70 · `␣మ` 8.7e-3✱ · `ము` 0.90 · `␣ల` 0.96 · `్య` 6.0e-5✱ · `క` 0.91 · `్రి` 0.94 · `మ` 0.96 · `ొ` 0.98 · `␣న` 0.97 · `్య` 1.00 · `్య` 0.81 · `్` 0.92 · `ల` 0.15 · `ల` 0.99 · `్య` 0.98 · `␣మ` 0.94 · `␣మ` 2.3e-3✱ · `్` 4.3e-5✱ · `మ` 0.09✱ · `్ర` 4.2e-3✱ · `్య` 9.7e-4✱ · `బ` 0.87 · `్ర` 0.33 · `ము` 0.84 · `మా` 0.66 · `␣మ` 8.5e-3✱ · `ము` 0.99 · `␣ల` 0.96 · `్య` 1.1e-3✱ · `క` 0.97 · `్రి` 0.96 · `మ` 0.97 · `ొ` 0.97 · `␣న` 0.93 · `్య` 0.99 · `్య` 0.98 · `్` 0.82 · `మ` 0.63 · `ల` 0.97 · `్` 5.7e-7✱ · `⏎` 7.5e-5✱ forced |
| 3 | `క` 0.98 · `ామ` 4.2e-5✱ · `␣మ` 1.3e-4✱ · `␣జ` 0.97 · `బ` 9.6e-3✱ · `్ర` 0.09✱ · `ము` 0.83 · `␣వ` 1.2e-3✱ · `్వ` 3.3e-6✱ · `్ర` 1.5e-5✱ · `్` 5.5e-4✱ · `ల` 7.0e-4✱ · `ల` 0.07✱ · `్య` 0.02✱ · `␣మ` 0.13✱ · `␣ఈ` 1.0e-3✱ · `␣ఇ` 8.0e-4✱ · `వ` 7.8e-3✱ · `␣వ` 6.9e-3✱ · `్ర` 2.9e-4✱ · `్` 1.9e-3✱ · `ల` 0.45 · `ల` 0.52 · `్య` 0.08✱ · `␣ల` 0.09✱ · `␣ల` 0.04✱ · `్య` 0.02✱ · `ల` 0.01✱ · `్య` 2.8e-3✱ · `␣మ` 0.09✱ · `ల` 0.03✱ · `ల` 0.05✱ · `్య` 1.7e-3✱ · `ల` 7.9e-3✱ · `ల` 0.01✱ · `వ` 1.2e-3✱ · `్` 1.3e-3✱ · `⏎` 0.02✱ forced |
| 4 | `వ` 9.7e-3✱ · `్యా` 0.02✱ · `␣` 0.08 · `మ` 2.8e-3✱ · `ము` 0.04✱ · `ను` 0.02✱ · `న్` 4.0e-3✱ · `␣ల` 0.64 · `␣` 0.29 · `ల్ల` 0.07✱ · `␣ల` 0.01✱ · `్య` 7.8e-5✱ · `ల` 1.9e-3✱ · `్య` 2.8e-5✱ · `్య` 5.2e-3✱ · `ల` 0.01✱ · `ల` 0.17✱ · `ల` 3.3e-3✱ · `్య` 0.01✱ · `ల` 0.02✱ · `␣` 0.52 · `ల` 0.01✱ · `్య` 0.03✱ · `ణ` 0.16✱ · `్య` 0.09✱ · `ల` 0.09✱ · `వ` 0.67 · `వ` 0.14 · `్` 5.8e-6✱ · `␣` 1.3e-4✱ · `ల్ల` 3.2e-3✱ · `␣మ` 0.05✱ · `␣మ` 0.09✱ · `్` 4.9e-3✱ · `స్` 0.01✱ · `స్` 7.3e-3✱ · `య` 6.9e-4✱ · `మ` 0.19✱ · `్` 2.9e-3✱ · `␣` 0.56 · `మ` 5.4e-3✱ · `ర` 8.8e-3✱ · `␣` 0.33 · `న్య` 0.01✱ · `ల` 0.03✱ · `్` 5.5e-5✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 140 tokens · 28.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మమ్యుమదంతచ ధ్ర్వ్మమ్య మకాల సుమర్రి సెదిన్రమమర్యమమమ్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 2 | సమ్యము దాటి ల ల్య్య్శన్ను శమమ్యమ మ్య్య్జమ్యతి మమ్యమ జమ్యడు జేయ్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 3 | నుమ్యమమమ్యమ మ్యోతిమతిమ్యన మ్యోకను ఏటను జ్య్యోమమమమ్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 4 | మమ్యతినిక్షమమల్య ఇ పైన ఇమమ్యనినుస్రితమమ్క్షమకున్ | `UIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 13% · repeated lines 0 · mean token probability (geometric) 0.016 · model's first choice kept 39% · constraint overrode 53% · backtracks 0

<details><summary>Token probabilities (140 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.61 · `మ` 0.13 · `్య` 1.9e-3✱ · `ు` 0.20 · `మ` 0.08 · `ద` 8.5e-3 · `ంత` 0.05✱ · `చ` 6.9e-3 · `␣ధ` 2.4e-3 · `్ర` 4.2e-3✱ · `్వ` 0.02✱ · `్` 2.3e-7✱ · `మ` 0.02✱ · `మ` 0.16 · `్య` 1.0e-3✱ · `␣మ` 0.04 · `క` 0.01 · `ాల` 2.9e-3 · `␣సు` 0.01 · `మ` 0.51 · `ర` 0.08 · `్రి` 6.4e-4✱ · `␣స` 0.05 · `ె` 5.7e-3 · `ది` 0.05✱ · `న` 0.05✱ · `్ర` 1.2e-6✱ · `మ` 0.77 · `మ` 0.91 · `ర` 0.87 · `్య` 6.0e-4✱ · `మ` 0.12 · `మ` 0.16 · `మ` 0.22 · `్` 1.1e-5✱ · `⏎` 0.12✱ forced |
| 2 | `స` 0.45 · `మ` 0.08✱ · `్య` 1.0e-6✱ · `ము` 0.86 · `␣దా` 0.92 · `టి` 0.92 · `␣ల` 0.99 · `␣ల` 5.7e-4✱ · `్య` 2.1e-5✱ · `్య` 1.4e-3✱ · `్` 2.8e-6✱ · `శ` 7.3e-4✱ · `న్` 3.4e-3✱ · `ను` 0.32 · `␣శ` 0.01 · `మ` 0.28 · `మ` 0.31✱ · `్య` 3.0e-4✱ · `మ` 0.84 · `␣మ` 0.06✱ · `్య` 2.7e-4✱ · `్య` 1.0e-3✱ · `్` 2.9e-5✱ · `జ` 1.1e-3✱ · `మ` 0.10✱ · `్య` 2.8e-3✱ · `తి` 0.33 · `␣మ` 0.22 · `మ` 0.01✱ · `్య` 9.7e-6✱ · `మ` 0.01✱ · `␣జ` 3.3e-3✱ · `మ` 2.1e-3✱ · `్య` 1.7e-4✱ · `డు` 0.99 · `␣జ` 0.97 · `ే` 0.96 · `య` 0.93 · `్` 7.5e-6✱ · `⏎` 1.6e-3✱ forced |
| 3 | `ను` 0.82 · `మ` 0.58 · `్య` 1.9e-4✱ · `మ` 0.97 · `మ` 0.94 · `మ` 0.85 · `్య` 2.8e-3✱ · `మ` 0.78 · `␣మ` 0.68 · `్య` 0.03✱ · `ోతి` 0.07✱ · `మ` 1.00 · `తి` 0.97 · `మ` 1.3e-3✱ · `్య` 4.6e-3✱ · `న` 0.84 · `␣మ` 5.2e-3✱ · `్య` 0.02✱ · `ో` 0.02✱ · `క` 1.00 · `ను` 0.95 · `␣ఏ` 0.99 · `ట` 0.97 · `ను` 0.87 · `␣జ` 0.95 · `్య` 3.2e-5✱ · `్య` 5.8e-3✱ · `ో` 0.10✱ · `మ` 0.07✱ · `మ` 0.91 · `మ` 0.97 · `మ` 0.96 · `్` 1.4e-5✱ · `⏎` 0.04✱ forced |
| 4 | `మ` 0.99 · `మ` 0.01✱ · `్య` 9.2e-3✱ · `తి` 0.99 · `ని` 0.09✱ · `క్ష` 0.83 · `మ` 0.93 · `మ` 6.6e-5✱ · `ల` 7.7e-4✱ · `్య` 1.2e-4✱ · `␣ఇ` 3.0e-3✱ · `␣ప` 0.90 · `ైన` 1.00 · `␣ఇ` 3.1e-4✱ · `మ` 1.8e-4✱ · `మ` 0.83 · `్య` 4.7e-5✱ · `ని` 2.6e-3✱ · `ను` 3.2e-4✱ · `స` 0.69 · `్రి` 1.5e-5✱ · `త` 2.9e-4✱ · `మ` 2.8e-5✱ · `మ` 0.01✱ · `్` 5.1e-4✱ · `క్ష` 0.97 · `మ` 0.97 · `కు` 3.5e-4✱ · `న` 8.3e-3✱ · `్` 1.8e-7✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 161 tokens · 68.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాత లవక్రిమొ మగ్గ మనిర్రిన ర్ర్ర్మయ్యల రామ ల ల్వ్య్మౌముగనల్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 2 | యైత జ జత్రల జ్యత్ ల్వ్య్మొముగన్ నివయట్ర జమైత్రల మ్ర్వ్లవ్య్మొముగన్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 3 | నౌతటటజ్రము ల్యావది లా మవనల్రుపుపువ్ర మ మ్ల్ర్ణణ్యల ఉర్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 4 | నైతి మమయ్లలుయయ్యలలమ్యల మ్మ్యల్రతిలల్ ర్తి ర్తి ర్ర్ర్నం మను మవ్ | `UIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 32% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 30% · constraint overrode 65% · backtracks 30

<details><summary>Token probabilities (161 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.55 · `త` 0.23 · `␣ల` 0.60 · `వ` 3.5e-3 · `క` 0.47 · `్రి` 0.64 · `మ` 0.36 · `ొ` 0.60 · `␣మ` 0.80 · `గ్` 0.95 · `గ` 0.87 · `␣మ` 0.03 · `ని` 0.03 · `ర` 0.85 · `్ర` 9.8e-4✱ · `ిన` 7.2e-3✱ · `␣ర` 3.4e-3✱ · `్ర` 5.4e-6✱ · `్ర` 1.2e-3✱ · `్` 1.7e-5✱ · `మయ్య` 1.0e-4✱ · `ల` 2.9e-4✱ · `␣రా` 6.5e-3 · `మ` 0.94 · `␣ల` 0.01✱ · `␣ల` 0.58 · `్వ` 9.6e-4✱ · `్య` 0.79 · `్` 2.2e-7✱ · `మ` 0.24 · `ౌ` 0.06✱ · `ము` 4.9e-3 · `గ` 0.03 · `న` 0.07 · `ల` 0.03✱ · `్` 2.2e-6✱ · `⏎` 4.5e-4✱ forced |
| 2 | `య` 0.02✱ · `ై` 8.0e-3✱ · `త` 7.4e-4✱ · `␣జ` 0.91 · `␣జ` 8.8e-5✱ · `త్ర` 0.90 · `ల` 0.79 · `␣జ` 0.01✱ · `్య` 1.5e-4✱ · `త` 0.99 · `్` 1.8e-5✱ · `␣ల` 0.94 · `్వ` 0.75 · `్య` 0.99 · `్` 0.96 · `మ` 0.97 · `ొ` 3.1e-4✱ · `ము` 0.32 · `గ` 0.88 · `న` 0.65 · `్` 7.9e-4✱ · `␣ని` 0.98 · `వ` 0.98 · `య` 7.9e-5✱ · `ట` 0.02✱ · `్ర` 4.4e-3✱ · `␣జ` 0.98 · `మై` 3.4e-4✱ · `త్ర` 0.99 · `ల` 0.96 · `␣మ` 4.2e-3✱ · `్ర` 2.8e-4✱ · `్వ` 7.1e-7✱ · `్` 2.2e-5✱ · `ల` 0.59 · `వ` 0.47 · `్య` 0.98 · `్` 0.86 · `మ` 0.96 · `ొ` 0.01✱ · `ము` 0.73 · `గ` 0.82 · `న` 0.75 · `్` 7.0e-5✱ · `⏎` 0.91 |
| 3 | `న` 4.6e-4✱ · `ౌ` 1.7e-3✱ · `త` 1.8e-4✱ · `ట` 0.91 · `ట` 9.9e-3✱ · `జ` 0.02✱ · `్ర` 3.3e-4✱ · `ము` 6.0e-4✱ · `␣ల` 1.4e-4✱ · `్యా` 3.1e-5✱ · `వ` 2.4e-4✱ · `ది` 7.1e-4✱ · `␣ల` 7.6e-3✱ · `ా` 1.0e-3✱ · `␣మ` 6.9e-3✱ · `వ` 5.1e-3✱ · `న` 0.01✱ · `ల` 0.30 · `్రు` 1.1e-4✱ · `పు` 9.3e-4✱ · `పు` 3.7e-3✱ · `వ` 2.1e-3✱ · `్ర` 3.6e-4✱ · `␣మ` 0.11 · `␣మ` 0.03✱ · `్` 1.1e-3✱ · `ల` 0.01✱ · `్ర` 9.5e-4✱ · `్` 0.02✱ · `ణ` 3.8e-3✱ · `ణ` 0.06✱ · `్య` 7.6e-3✱ · `ల` 0.05✱ · `␣ఉ` 0.06✱ · `ర్` 0.02✱ · `⏎` 0.16 forced |
| 4 | `న` 9.4e-3✱ · `ై` 0.13 · `తి` 0.03✱ · `␣మ` 0.16✱ · `మ` 1.5e-3✱ · `య` 0.02✱ · `్` 1.6e-3✱ · `ల` 0.04✱ · `లు` 2.9e-4✱ · `య` 4.9e-3✱ · `య` 0.02✱ · `్య` 1.7e-3✱ · `ల` 0.03✱ · `ల` 0.19 · `మ` 0.01✱ · `్య` 0.03✱ · `ల` 0.67 · `␣మ` 0.12✱ · `్` 3.0e-3✱ · `మ` 0.86 · `్య` 1.1e-4✱ · `ల` 0.01✱ · `్ర` 2.1e-4✱ · `తి` 8.5e-4✱ · `ల` 0.02✱ · `ల` 0.05✱ · `్` 9.7e-4✱ · `␣` 9.2e-3✱ · `ర్` 0.04✱ · `తి` 4.7e-3✱ · `␣` 0.13✱ · `ర్` 0.01✱ · `తి` 0.14✱ · `␣` 0.27 · `ర్` 3.1e-3✱ · `ర్` 0.01✱ · `ర్` 3.7e-3✱ · `నం` 6.9e-5✱ · `␣మ` 1.4e-3✱ · `ను` 4.7e-3✱ · `␣మ` 0.02✱ · `వ` 3.6e-3✱ · `్` 1.3e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 169 tokens · 66.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కల్లి మ మగ్య మ మ్య్మ్కత్రు మ జన్వర వ్ర్జ్కక్తమ మాని మగగ్య్య్మ మకత్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 2 | జుల్ లుజ లో సుతి మ్ర్మ్జూడ మ మ్య్మ్కత్రు మ జొన్న వ్ర్జజక్తత మ్య్య్జూడ మ మమ్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 3 | తిల్లికకల్య ల ల్య్య్తిబ్బులుతావవతీ ల ల లీడు ల ల్య్ల్తిల్ల డు డువ్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 4 | భుల్ల భ భల్ల భ భుల్రు మ మమ్మ మ్యముల్రు మ మమ్మ మ్మమొల్య మ మమ్ | `UIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 45% · repeated lines 0 · mean token probability (geometric) 0.025 · model's first choice kept 38% · constraint overrode 59% · backtracks 30

<details><summary>Token probabilities (169 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.85 · `ల్లి` 0.81 · `␣మ` 0.42 · `␣మ` 0.11 · `గ` 0.96 · `్య` 0.95 · `␣మ` 0.89 · `␣మ` 0.82 · `్య` 0.79 · `్` 0.49 · `మ` 9.3e-3 · `్` 7.8e-6✱ · `క` 6.4e-3✱ · `త` 0.86 · `్రు` 6.2e-5✱ · `␣మ` 0.39 · `␣జ` 3.3e-3 · `న` 0.81 · `్వర` 1.5e-4✱ · `␣వ` 0.97 · `్ర` 0.18✱ · `్` 0.02✱ · `జ` 0.14 · `్` 2.9e-5✱ · `క` 2.3e-4✱ · `క` 1.9e-3✱ · `్` 1.4e-5✱ · `త` 0.65 · `మ` 8.2e-3✱ · `␣మ` 0.79 · `ాని` 0.55 · `␣మ` 0.86 · `గ` 0.89 · `గ` 2.9e-3✱ · `్య` 0.02✱ · `్య` 0.76 · `్` 0.60 · `మ` 0.76 · `␣మ` 0.03✱ · `క` 0.72 · `త` 0.81 · `్` 2.8e-4✱ · `⏎` 9.4e-4✱ forced |
| 2 | `␣జ` 0.86 · `ు` 5.2e-3✱ · `ల` 0.01✱ · `్` 1.9e-7✱ · `␣ల` 0.11✱ · `ు` 0.63 · `జ` 0.91 · `␣లో` 0.03✱ · `␣సు` 6.5e-3✱ · `తి` 0.78 · `␣మ` 0.01✱ · `్ర` 8.0e-5✱ · `్` 1.7e-4✱ · `మ` 0.02✱ · `్` 5.1e-6✱ · `జ` 1.8e-3✱ · `ూ` 7.2e-4✱ · `డ` 0.03✱ · `␣మ` 0.91 · `␣మ` 0.96 · `్య` 0.98 · `్` 0.90 · `మ` 0.91 · `్` 0.05✱ · `క` 0.99 · `త` 0.98 · `్రు` 0.95 · `␣మ` 0.94 · `␣జ` 0.93 · `ొ` 5.2e-4✱ · `న్న` 0.22 · `␣వ` 0.94 · `్ర` 0.79 · `్` 0.88 · `జ` 0.90 · `జ` 0.18 · `క` 0.48 · `్` 1.8e-3✱ · `త` 0.18✱ · `త` 0.64 · `␣మ` 0.35✱ · `్య` 4.2e-4✱ · `్య` 1.4e-3✱ · `్` 0.08✱ · `జ` 3.3e-3✱ · `ూ` 8.9e-3✱ · `డ` 0.53 · `␣మ` 0.22 · `␣మ` 0.14 · `మ` 0.67 · `్` 3.9e-4✱ · `⏎` 0.09✱ forced |
| 3 | `తి` 0.57 · `ల్లి` 0.02✱ · `క` 0.23 · `క` 0.38 · `ల` 0.67 · `్య` 2.6e-4✱ · `␣ల` 0.88 · `␣ల` 0.47 · `్య` 8.6e-4✱ · `్య` 3.6e-3✱ · `్` 3.5e-6✱ · `తి` 3.4e-5✱ · `బ్బు` 2.2e-5✱ · `లు` 1.5e-3✱ · `త` 4.9e-4✱ · `ా` 8.6e-4✱ · `వ` 1.1e-3✱ · `వ` 0.01✱ · `త` 1.8e-3✱ · `ీ` 3.1e-3✱ · `␣ల` 0.02✱ · `␣ల` 5.5e-3✱ · `␣ల` 0.01✱ · `ీ` 8.9e-4✱ · `డు` 7.1e-3✱ · `␣ల` 8.1e-3✱ · `␣ల` 0.05✱ · `్య` 2.8e-3✱ · `్` 5.9e-3✱ · `ల` 0.05✱ · `్` 5.0e-4✱ · `తి` 4.3e-4✱ · `ల` 0.03✱ · `్` 5.6e-4✱ · `ల` 0.05✱ · `␣` 0.09✱ · `డు` 0.01✱ · `␣` 5.2e-3✱ · `డు` 3.8e-3✱ · `వ` 2.0e-3✱ · `్` 1.9e-4✱ · `⏎` 0.16✱ forced |
| 4 | `␣భ` 0.60 · `ు` 2.1e-4✱ · `ల్ల` 1.9e-4✱ · `␣భ` 0.77 · `␣భ` 0.86 · `ల్ల` 6.6e-3✱ · `␣భ` 0.90 · `␣భ` 0.85 · `ుల` 3.8e-4✱ · `్రు` 2.0e-3✱ · `␣మ` 0.18✱ · `␣మ` 0.13 · `మ్మ` 0.10✱ · `␣మ` 0.11 · `్య` 0.02✱ · `మ` 0.13 · `ుల` 7.2e-3✱ · `్రు` 0.01✱ · `␣మ` 0.33 · `␣మ` 0.24✱ · `మ్మ` 0.21 · `␣మ` 0.11✱ · `్` 0.01✱ · `మ` 0.09✱ · `మ` 0.19 · `ొ` 2.6e-4✱ · `ల` 5.9e-3✱ · `్య` 6.7e-4✱ · `␣మ` 0.02✱ · `␣మ` 0.03✱ · `మ` 0.05✱ · `్` 4.8e-3✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 144 tokens · 36.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామ భవన్ జర శ్రయ్రి ల లన్ మలెరామమ భవ్ జర శ్రయ్రి లకం | `UIIUIIUIIUIIUIIUIIUIIU` |
| 2 | మేముకరామ భ వ్జ్ర్మిత్ర లకన్ మలెమీమ భవన్జర శ్ర్య్మిత్ర మలా | `UIIUIIUIIUIIUIIUIIUIIU` |
| 3 | గా ముకు రీ లుతి గణ్యము మానిని మ్ర్ర్గమ్య ఉఈ ఉఉ మ్జ్ర్కమ్య లలా | `UIIUIIUIIUIIUIIUIIUIIU` |
| 4 | వా మనినిన్ మల మ్య్య్వా లకమన్న మ మ్య్య్వాను వనుమ్యను మ్య్య్వా అనురా | `UIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 25% · repeated lines 0 · mean token probability (geometric) 0.018 · model's first choice kept 30% · constraint overrode 62% · backtracks 0

<details><summary>Token probabilities (144 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.26 · `మ` 0.72 · `␣భ` 0.03 · `వ` 0.12✱ · `న్` 0.09 · `␣జ` 0.37 · `ర` 0.03 · `␣శ` 0.05 · `్ర` 8.5e-3✱ · `య` 0.26 · `్రి` 1.4e-5✱ · `␣ల` 0.82 · `␣ల` 0.39 · `న్` 0.04 · `␣మ` 0.02 · `ల` 0.02✱ · `ె` 0.01✱ · `రా` 3.1e-4✱ · `మ` 6.7e-3✱ · `మ` 0.94 · `␣భ` 0.99 · `వ` 0.98 · `్` 9.5e-7✱ · `␣జ` 0.97 · `ర` 0.97 · `␣శ` 0.98 · `్ర` 0.76 · `య` 0.92 · `్రి` 0.57 · `␣ల` 0.88 · `కం` 8.3e-3 · `⏎` 7.0e-6 forced |
| 2 | `␣మ` 0.97 · `ే` 3.3e-5✱ · `ము` 2.7e-3✱ · `క` 8.8e-4✱ · `రా` 0.96 · `మ` 0.93 · `␣భ` 0.95 · `␣వ` 1.7e-3✱ · `్` 1.3e-3✱ · `జ` 0.01✱ · `్ర` 1.1e-3✱ · `్` 2.5e-5✱ · `మ` 3.5e-3✱ · `ిత` 6.3e-3✱ · `్ర` 0.05✱ · `␣ల` 0.84 · `క` 0.83 · `న్` 0.92 · `␣మ` 0.84 · `ల` 0.92 · `ె` 0.84 · `మ` 6.8e-3✱ · `ీ` 5.0e-4✱ · `మ` 0.68 · `␣భ` 0.74 · `వ` 0.71 · `న్` 0.25 · `జ` 0.13 · `ర` 0.71 · `␣శ` 0.65 · `్ర` 0.37 · `్య` 1.4e-3✱ · `్` 3.7e-4✱ · `మ` 3.4e-4✱ · `ిత` 0.03✱ · `్ర` 0.94 · `␣మ` 0.84 · `లా` 5.1e-4 · `⏎` 0.21✱ |
| 3 | `␣` 2.0e-4✱ · `గా` 5.6e-4✱ · `␣` 1.6e-3✱ · `ము` 2.4e-5✱ · `కు` 9.0e-5✱ · `␣రీ` 2.9e-3✱ · `␣` 5.2e-3✱ · `లు` 0.01✱ · `తి` 0.02✱ · `␣గ` 0.14 · `ణ` 0.24 · `్య` 0.03✱ · `ము` 0.12✱ · `␣మ` 0.50 · `ాని` 0.18 · `ని` 0.20 · `␣మ` 0.18✱ · `్ర` 3.0e-3✱ · `్ర` 7.2e-4✱ · `్` 7.6e-5✱ · `గ` 6.7e-3✱ · `మ` 0.06✱ · `్య` 8.7e-3✱ · `␣ఉ` 0.09✱ · `ఈ` 1.7e-3✱ · `␣ఉ` 0.14✱ · `ఉ` 0.05✱ · `␣మ` 0.01✱ · `్` 0.02✱ · `జ` 0.01✱ · `్ర` 0.02✱ · `్` 5.4e-7✱ · `క` 1.2e-3✱ · `మ` 3.5e-3✱ · `్య` 0.01✱ · `␣ల` 7.4e-3✱ · `లా` 0.02 · `⏎` 0.33✱ forced |
| 4 | `వా` 4.7e-3✱ · `␣మ` 0.02✱ · `ని` 0.06✱ · `ని` 0.44 · `న్` 0.01✱ · `␣మ` 0.05✱ · `ల` 0.56 · `␣మ` 0.07 · `్య` 1.9e-3✱ · `్య` 2.5e-4✱ · `్` 7.9e-5✱ · `వా` 4.9e-3✱ · `␣ల` 1.9e-3✱ · `క` 5.8e-3✱ · `మ` 0.01✱ · `న్న` 0.03✱ · `␣మ` 0.04✱ · `␣మ` 7.8e-3✱ · `్య` 1.8e-3✱ · `్య` 0.01✱ · `్` 1.4e-3✱ · `వా` 0.03✱ · `ను` 1.3e-3✱ · `␣వ` 0.04✱ · `ను` 0.07✱ · `మ` 6.2e-4✱ · `్య` 4.3e-4✱ · `ను` 9.9e-3✱ · `␣మ` 3.2e-4✱ · `్య` 8.5e-3✱ · `్య` 0.02✱ · `్వ` 3.4e-5✱ · `ా` 0.02✱ · `␣అను` 1.2e-3✱ · `రా` 5.2e-3✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 163 tokens · 42.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తమ్రిమతృవ్రమ మ్ర్ర్దమ్య మృదువ్ర మ మ్ర్దమ్యతతమ్రితృ వ్ర్ర్తమ్రదమం | `UIIUIIUIIUIIUIIUIIUIIU` |
| 2 | మృమ్రమవవ్ర్రదదృద్య మతిమ్రి మ మే మతి లోసకకృశ్యతి లో | `UIIUIIUIIUIIUIIUIIUIIU` |
| 3 | తిమ్రి మతిమ్రి స మ్య్య్దే మతి మత్రి మ మ్య్స్దే మతి మమ్రి ల ల్య్య్తిమ్యశమా | `UIIUIIUIIUIIUIIUIIUIIU` |
| 4 | కమ్ర మ మమ్యమ మ్య్య్ఘమ్రనిదివ్రుశ హ్ర్య్గమ్య్యు ససస్యది మ్య్య్ఖబ్య దినా | `UIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 30% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 35% · constraint overrode 62% · backtracks 0

<details><summary>Token probabilities (163 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.19 · `మ` 0.07 · `్రి` 4.0e-3✱ · `మ` 0.25 · `త` 0.05 · `ృ` 0.29 · `వ` 0.02 · `్ర` 2.2e-4✱ · `మ` 0.34 · `␣మ` 0.13✱ · `్ర` 6.3e-4✱ · `్ర` 2.5e-5✱ · `్` 6.2e-6✱ · `ద` 7.0e-3✱ · `మ` 0.10✱ · `్య` 2.5e-4✱ · `␣మ` 0.34 · `ృ` 0.02 · `దు` 0.54 · `వ` 0.29 · `్ర` 2.5e-4✱ · `␣మ` 0.25 · `␣మ` 0.03✱ · `్ర` 2.5e-3✱ · `్` 6.7e-4✱ · `ద` 0.80 · `మ` 0.74 · `్య` 0.06✱ · `త` 0.20✱ · `త` 0.45 · `మ` 0.45 · `్రి` 0.42 · `త` 0.93 · `ృ` 0.94 · `␣వ` 0.05✱ · `్ర` 0.90 · `్ర` 6.6e-4✱ · `్` 7.0e-6✱ · `త` 4.6e-4✱ · `మ` 0.03✱ · `్ర` 0.24 · `ద` 0.35 · `మ` 0.48 · `ం` 3.9e-3 · `⏎` 2.9e-3✱ forced |
| 2 | `␣మ` 0.56 · `ృ` 0.28✱ · `మ` 0.01✱ · `్ర` 1.2e-3✱ · `మ` 0.14✱ · `వ` 0.38 · `వ` 0.03✱ · `్ర` 0.59 · `్ర` 0.30 · `ద` 0.40 · `ద` 0.34 · `ృ` 1.5e-5✱ · `ద్య` 6.0e-3✱ · `␣మ` 0.95 · `తి` 0.86 · `మ` 1.5e-3✱ · `్రి` 9.0e-5✱ · `␣మ` 0.84 · `␣మ` 2.2e-3✱ · `ే` 4.9e-3✱ · `␣మ` 0.69 · `తి` 0.85 · `␣లో` 0.92 · `స` 9.9e-4✱ · `క` 0.92 · `క` 0.02✱ · `ృ` 9.0e-5✱ · `శ` 7.6e-3✱ · `్య` 5.5e-3✱ · `తి` 0.48 · `␣లో` 4.5e-3✱ · `⏎` 0.15 forced |
| 3 | `తి` 0.78 · `మ` 0.05✱ · `్రి` 7.4e-5✱ · `␣మ` 0.92 · `తి` 0.82 · `మ` 4.9e-3✱ · `్రి` 1.3e-3✱ · `␣స` 0.84 · `␣మ` 0.98 · `్య` 7.2e-5✱ · `్య` 3.9e-3✱ · `్` 5.4e-5✱ · `ద` 5.3e-4✱ · `ే` 4.1e-4✱ · `␣మ` 0.82 · `తి` 0.87 · `␣మ` 0.90 · `త` 1.9e-3✱ · `్రి` 7.7e-4✱ · `␣మ` 0.91 · `␣మ` 0.66 · `్య` 0.97 · `్` 0.88 · `స` 0.84 · `్` 3.0e-6✱ · `ద` 0.05✱ · `ే` 3.0e-3✱ · `␣మ` 0.97 · `తి` 0.97 · `␣మ` 0.96 · `మ` 6.1e-4✱ · `్రి` 3.9e-5✱ · `␣ల` 3.2e-4✱ · `␣ల` 0.03✱ · `్య` 4.4e-3✱ · `్య` 0.09✱ · `్` 4.6e-4✱ · `తి` 3.2e-3✱ · `మ` 1.4e-3✱ · `్య` 1.6e-4✱ · `శ` 8.8e-3✱ · `మా` 2.4e-3✱ · `⏎` 0.14✱ forced |
| 4 | `క` 0.02✱ · `మ` 0.13 · `్ర` 1.0e-3✱ · `␣మ` 0.47 · `␣మ` 0.21 · `మ` 0.17 · `్య` 0.13✱ · `మ` 0.35 · `␣మ` 0.03✱ · `్య` 3.1e-3✱ · `్య` 0.05✱ · `్` 9.2e-3✱ · `ఘ` 2.1e-3✱ · `మ` 0.02✱ · `్ర` 4.6e-5✱ · `ని` 0.90 · `ది` 0.01✱ · `వ` 1.8e-4✱ · `్రు` 4.6e-4✱ · `శ` 0.98 · `␣హ` 4.6e-5✱ · `్ర` 1.8e-4✱ · `్య` 1.5e-4✱ · `్` 2.4e-6✱ · `గ` 1.8e-4✱ · `మ` 2.1e-3✱ · `్య` 1.8e-4✱ · `్య` 5.7e-3✱ · `ు` 2.4e-3✱ · `␣స` 4.8e-4✱ · `స` 1.1e-3✱ · `స` 1.9e-3✱ · `్య` 1.1e-4✱ · `ది` 0.01✱ · `␣మ` 2.6e-3✱ · `్య` 3.6e-4✱ · `్య` 0.03✱ · `్` 4.4e-6✱ · `ఖ` 3.3e-5✱ · `బ` 3.7e-5✱ · `్య` 3.9e-4✱ · `␣ది` 4.1e-3✱ · `నా` 1.4e-3✱ |

</details>

[↑ meters](#meters)

---

<a id="kavirajavirajitamu"></a>

## 33. కవిరాజవిరాజితము (kavirajavirajitamu)

```text
Meter: కవిరాజవిరాజితము (kavirajavirajitamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas: న జ జ జ జ జ జ వ, i.e. III IUI IUI IUI IUI IUI IUI IU (23 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 8th and the 14th and the 20th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter కవిరాజవిరాజితము (kavirajavirajitamu).

Meter: కవిరాజవిరాజితము (kavirajavirajitamu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 8 gaṇas: న జ జ జ జ జ జ వ, i.e. III IUI IUI IUI IUI IUI IUI IU (23 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 8th and the 14th and the 20th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 146 tokens · 38.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమల శ శీల క చ్య్వ్గర్య మణిద్రి మ మ్ర్య్గమ్రిమమమ్రమకమ్యమమమ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 2 | మ మున హనుమ్రుతి మమ్య మ మమ్య మమమ్యున హన్ను మమమ్య మ మమ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 3 | మమమమ జున్యనుమంతి ట్టి లేదు ల న్న్గ్మవ్య మమమ్య మమమ్యున జుమ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 4 | జమమ మ మల్య్యక చ్యడ్య జునహ్యమ మ్య్య్సమ్రమునుంటమ జన్న హనుమ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 31% · repeated lines 0 · mean token probability (geometric) 0.018 · model's first choice kept 37% · constraint overrode 60% · backtracks 0

<details><summary>Token probabilities (146 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 5.9e-3 · `మ` 0.47 · `ల` 0.25 · `␣శ` 0.02 · `␣శ` 4.7e-3✱ · `ీల` 0.02 · `␣క` 0.03 · `␣చ` 4.3e-3✱ · `్య` 1.1e-3✱ · `్వ` 8.3e-4✱ · `్` 5.0e-4✱ · `గర` 9.4e-3✱ · `్య` 4.4e-4✱ · `␣మ` 0.15 · `ణి` 0.11 · `ద` 0.02 · `్రి` 5.2e-3✱ · `␣మ` 0.18 · `␣మ` 9.3e-3✱ · `్ర` 1.4e-3✱ · `్య` 1.9e-4✱ · `్` 4.8e-7✱ · `గ` 6.9e-3✱ · `మ` 0.18 · `్రి` 1.4e-3✱ · `మ` 0.05✱ · `మ` 0.19✱ · `మ` 0.27 · `్రమ` 2.8e-4✱ · `క` 0.02✱ · `మ` 0.43 · `్య` 1.2e-3✱ · `మ` 0.15 · `మ` 0.34 · `మ` 0.28 · `్` 8.3e-5✱ · `⏎` 0.10✱ forced |
| 2 | `మ` 0.22 · `␣మ` 8.1e-3✱ · `ు` 0.57 · `న` 0.54 · `␣హ` 0.91 · `ను` 0.85 · `మ` 0.02✱ · `్రు` 3.7e-5✱ · `తి` 0.09✱ · `␣మ` 0.10✱ · `మ` 0.79 · `్య` 8.7e-4✱ · `␣మ` 0.82 · `␣మ` 0.83 · `మ` 3.3e-3✱ · `్య` 5.3e-3✱ · `␣మ` 0.63 · `మ` 0.29 · `మ` 0.40 · `్య` 7.7e-5✱ · `ు` 0.86 · `న` 0.87 · `␣హ` 0.98 · `న్ను` 4.3e-4✱ · `␣మ` 0.09✱ · `మ` 0.02✱ · `మ` 0.03✱ · `్య` 0.05✱ · `␣మ` 0.67 · `␣మ` 0.53 · `మ` 0.19✱ · `్` 6.9e-4✱ · `⏎` 0.03✱ forced |
| 3 | `మ` 0.62 · `మ` 0.47 · `మ` 0.77 · `మ` 1.1e-4✱ · `␣జ` 0.98 · `ు` 0.98 · `న` 0.96 · `్య` 7.2e-6✱ · `ను` 0.76 · `మం` 0.47 · `తి` 0.94 · `␣` 1.0e-4✱ · `ట్టి` 4.5e-4✱ · `␣లేదు` 8.0e-4✱ · `␣ల` 1.2e-3✱ · `␣` 9.3e-4✱ · `న్` 2.1e-3✱ · `న్` 2.4e-3✱ · `గ` 3.3e-4✱ · `్` 1.0e-4✱ · `మ` 8.2e-4✱ · `వ` 3.4e-4✱ · `్య` 9.3e-5✱ · `␣మ` 4.8e-3✱ · `మ` 0.13✱ · `మ` 4.8e-3✱ · `్య` 2.3e-3✱ · `␣మ` 0.03✱ · `మ` 0.03✱ · `మ` 0.08✱ · `్య` 0.06✱ · `ు` 0.02✱ · `న` 0.87 · `␣జ` 0.37 · `ు` 0.10✱ · `మ` 1.8e-3✱ · `్` 4.1e-5✱ · `⏎` 0.38 forced |
| 4 | `␣జ` 0.03✱ · `మ` 0.01✱ · `మ` 0.23 · `␣మ` 0.03✱ · `␣మ` 0.71 · `ల` 1.5e-3✱ · `్య` 7.7e-5✱ · `్య` 0.02✱ · `క` 0.23 · `␣చ` 4.3e-4✱ · `్య` 0.06✱ · `డ` 0.98 · `్య` 5.2e-4✱ · `␣జ` 0.83 · `ు` 0.95 · `న` 0.85 · `హ` 0.03✱ · `్య` 9.2e-5✱ · `మ` 0.28✱ · `␣మ` 7.4e-3✱ · `్య` 8.4e-3✱ · `్య` 1.8e-4✱ · `్` 1.6e-7✱ · `స` 0.05✱ · `మ` 7.1e-3✱ · `్ర` 2.5e-4✱ · `ము` 0.96 · `ను` 0.97 · `ం` 3.2e-4✱ · `ట` 0.94 · `మ` 0.72 · `␣జ` 0.91 · `న్` 1.1e-4✱ · `న` 0.72 · `␣హ` 0.50 · `ను` 0.85 · `మ` 0.14✱ · `్` 6.6e-6✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 174 tokens · 36.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నమలసి వట్రు భు వ్ర్వ్నమ్ర సముద్ర జ మ్ర్హ్నమ్రి నమల్రు వ వ్ర్ర్నల్వ్నమొ మౌక్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 2 | సుమమమ నన్యల వ్ర్ర్జుల్ర్వ్నమొ సీనును జుడ్యనమం నమసొట్ర్రు భు వ్ర్వ్నమ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 3 | లము జడెనమ్రి గ గ్లాకకు క్షమ్వర వ్ర్ర్లజ్రజితం గణ స్మ్ర్లల్వ జ జణ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 4 | కమ అడిగిన్యన జ్వ్వ్కణ్య ఇ గణ్రమ కాని ఇఇత్పమ స్ర్ల్కద్యశ తిమ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 29% · repeated lines 0 · mean token probability (geometric) 0.010 · model's first choice kept 37% · constraint overrode 58% · backtracks 0

<details><summary>Token probabilities (174 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `న` 0.03 · `మ` 0.50 · `ల` 0.06 · `సి` 6.6e-3 · `␣వ` 9.6e-3 · `ట` 0.04 · `్రు` 2.6e-3✱ · `␣భ` 0.01 · `ు` 0.16✱ · `␣వ` 2.6e-3✱ · `్ర` 0.01✱ · `్వ` 9.4e-4✱ · `్` 1.8e-5✱ · `న` 0.02✱ · `మ` 0.05✱ · `్ర` 2.9e-3✱ · `␣స` 0.14 · `ము` 0.83 · `ద్ర` 0.82 · `␣జ` 0.04 · `␣మ` 0.05 · `్ర` 1.6e-3✱ · `్` 4.6e-5✱ · `హ` 0.04 · `్` 1.4e-5✱ · `న` 0.04✱ · `మ` 0.10 · `్రి` 0.04✱ · `␣` 1.2e-3✱ · `న` 0.92 · `మ` 0.99 · `ల` 0.97 · `్రు` 5.0e-5✱ · `␣వ` 0.96 · `␣వ` 1.1e-4✱ · `్ర` 1.6e-3✱ · `్ర` 4.7e-5✱ · `్` 1.5e-5✱ · `న` 1.6e-3✱ · `ల` 3.1e-3✱ · `్వ` 0.67 · `్` 0.80 · `న` 0.77 · `మ` 0.75 · `ొ` 0.04✱ · `␣మ` 0.68 · `ౌ` 0.89 · `క` 0.90 · `్` 5.1e-9✱ · `⏎` 4.0e-5✱ forced |
| 2 | `␣సు` 0.02✱ · `మ` 0.02✱ · `మ` 0.79 · `మ` 7.5e-3✱ · `␣న` 5.4e-3✱ · `న` 0.84 · `్య` 3.6e-5✱ · `ల` 0.79 · `␣వ` 1.9e-3✱ · `్ర` 1.0e-3✱ · `్ర` 1.8e-3✱ · `్` 5.4e-4✱ · `జ` 0.02✱ · `ు` 0.12✱ · `ల` 1.8e-3✱ · `్ర` 0.31 · `్వ` 0.90 · `్` 0.82 · `న` 0.85 · `మ` 0.92 · `ొ` 0.89 · `␣సీ` 0.98 · `ను` 0.94 · `ను` 2.7e-4✱ · `␣జ` 0.01✱ · `ు` 0.02✱ · `డ` 7.9e-4✱ · `్య` 8.8e-3✱ · `న` 0.84 · `మ` 0.92 · `ం` 5.1e-3✱ · `␣` 8.2e-3✱ · `న` 0.88 · `మ` 0.98 · `స` 3.9e-3✱ · `ొ` 2.9e-3✱ · `ట` 0.01✱ · `్ర` 3.4e-4✱ · `్రు` 0.59 · `␣భ` 1.00 · `ు` 0.98 · `␣వ` 0.99 · `్ర` 0.97 · `్వ` 0.96 · `్` 0.98 · `న` 0.97 · `మ` 0.95 · `్` 8.6e-5✱ · `⏎` 4.4e-5✱ forced |
| 3 | `␣ల` 6.4e-4✱ · `ము` 7.6e-4✱ · `␣జ` 0.87 · `డ` 0.98 · `ె` 0.03✱ · `న` 0.59 · `మ` 0.92 · `్రి` 0.92 · `␣` 8.1e-3✱ · `గ` 4.2e-3✱ · `␣గ` 6.0e-3✱ · `్లా` 7.3e-8✱ · `క` 0.99 · `కు` 1.7e-4✱ · `␣క్ష` 0.99 · `మ` 0.99 · `్వర` 1.7e-6✱ · `␣వ` 4.5e-5✱ · `్ర` 2.6e-5✱ · `్ర` 7.9e-4✱ · `్` 6.6e-5✱ · `ల` 1.2e-4✱ · `జ` 0.03✱ · `్ర` 2.7e-5✱ · `జ` 0.95 · `ిత` 0.86 · `ం` 1.7e-3✱ · `␣గణ` 1.00 · `␣స` 4.2e-4✱ · `్` 2.8e-6✱ · `మ` 3.1e-5✱ · `్ర` 5.7e-4✱ · `్` 7.3e-4✱ · `ల` 1.7e-3✱ · `ల` 1.7e-3✱ · `్వ` 1.9e-5✱ · `␣జ` 0.92 · `␣జ` 0.98 · `ణ` 2.7e-3✱ · `్` 6.8e-6✱ · `⏎` 1.4e-4✱ forced |
| 4 | `క` 0.03✱ · `మ` 2.4e-4✱ · `␣అ` 1.00 · `డి` 1.00 · `గిన` 0.98 · `్య` 2.1e-7✱ · `న` 0.79 · `␣జ` 0.92 · `్వ` 6.6e-5✱ · `్వ` 0.03✱ · `్` 9.1e-6✱ · `క` 2.8e-4✱ · `ణ` 0.01✱ · `్య` 7.3e-4✱ · `␣ఇ` 2.4e-3✱ · `␣గణ` 0.99 · `్రమ` 3.5e-4✱ · `␣కాని` 2.0e-3✱ · `␣ఇ` 4.9e-5✱ · `ఇ` 0.51 · `త్ప` 0.84 · `మ` 3.8e-4✱ · `␣స` 1.9e-3✱ · `్ర` 3.3e-6✱ · `్` 8.4e-3✱ · `ల` 3.0e-3✱ · `్` 2.2e-7✱ · `క` 2.7e-4✱ · `ద్య` 0.92 · `శ` 0.81 · `␣` 1.2e-4✱ · `తి` 0.58 · `మ` 4.1e-3✱ · `్` 8.7e-10✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 146 tokens · 57.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కరుణ ద సుత్రిణ మ్ర్జ్గహ్రు పనో జయ ల్య్ర్గామతినీమమ మ్య్య్గణ్యతి మమ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 2 | వ ర మతి లోమతి ల్య్య్బర్రతి మమ్యతి మ్ర్వడ్ర మతిమ్రవ త్ర్ర్వర్రమ మమ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 3 | మరణ మతిల్యవ మమ్యతిమాగగమాకని పైన ప ప్య్య్మందయ గణ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 4 | చిరవు అయిన్రున న్య్య్చిత్య నియమ్య ఇశీ ఇతనున్రిమ క్ర్ర్జిత్యితముమ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 15% · single-akshara words 21% · repeated lines 0 · mean token probability (geometric) 0.004 · model's first choice kept 32% · constraint overrode 64% · backtracks 30

<details><summary>Token probabilities (146 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.97 · `రుణ` 0.90 · `␣ద` 1.6e-3✱ · `␣సు` 3.8e-3 · `త` 0.32 · `్రి` 0.02✱ · `ణ` 0.76 · `␣మ` 0.54 · `్ర` 1.5e-4✱ · `్` 5.4e-5✱ · `జ` 0.95 · `్` 6.9e-5✱ · `గ` 2.2e-3✱ · `హ` 2.1e-4 · `్రు` 0.03✱ · `␣ప` 1.0e-6 · `నో` 0.56 · `␣జ` 0.98 · `య` 0.95 · `␣ల` 0.71 · `్య` 2.4e-7✱ · `్ర` 8.0e-5✱ · `్` 2.5e-6✱ · `గా` 4.2e-3✱ · `మ` 0.88 · `తి` 0.93 · `నీ` 2.6e-4✱ · `మ` 0.31 · `మ` 0.05 · `␣మ` 0.57 · `్య` 8.1e-6✱ · `్య` 8.4e-4✱ · `్` 2.6e-6✱ · `గ` 0.02✱ · `ణ` 8.5e-3✱ · `్య` 2.4e-3✱ · `తి` 0.54 · `␣మ` 0.66 · `మ` 7.3e-3✱ · `్` 8.2e-7✱ · `⏎` 2.4e-4✱ forced |
| 2 | `వ` 0.60 · `␣` 1.0e-4✱ · `ర` 4.0e-4✱ · `␣మ` 0.80 · `తి` 0.78 · `␣లో` 0.01✱ · `మ` 0.73 · `తి` 0.84 · `␣ల` 8.0e-3✱ · `్య` 5.3e-5✱ · `్య` 1.9e-3✱ · `్` 3.8e-5✱ · `బ` 7.8e-3✱ · `ర` 8.7e-3✱ · `్ర` 1.0e-4✱ · `తి` 0.97 · `␣మ` 0.99 · `మ` 7.8e-3✱ · `్య` 1.6e-4✱ · `తి` 0.91 · `␣మ` 1.4e-4✱ · `్ర` 1.9e-7✱ · `్వ` 7.6e-5✱ · `డ` 1.00 · `్ర` 1.2e-3✱ · `␣మ` 0.75 · `తి` 0.84 · `మ` 8.0e-4✱ · `్ర` 1.6e-8✱ · `వ` 0.70 · `␣త` 0.71 · `్ర` 6.3e-4✱ · `్ర` 1.2e-4✱ · `్వర` 3.7e-4✱ · `్ర` 1.1e-4✱ · `మ` 0.23 · `␣మ` 0.71 · `మ` 3.4e-3✱ · `్` 5.1e-5✱ · `⏎` 3.5e-3✱ forced |
| 3 | `మ` 0.48 · `రణ` 4.8e-4✱ · `␣మ` 0.70 · `తి` 0.64 · `ల` 1.4e-5✱ · `్య` 3.1e-5✱ · `వ` 0.99 · `␣మ` 3.4e-4✱ · `మ` 2.2e-3✱ · `్య` 6.7e-4✱ · `తి` 0.90 · `మా` 2.5e-4✱ · `గ` 4.5e-5✱ · `గ` 0.40 · `మా` 2.5e-3✱ · `క` 0.97 · `ని` 0.01✱ · `␣ప` 0.99 · `ైన` 1.00 · `␣ప` 2.0e-3✱ · `␣ప` 0.97 · `్య` 1.2e-4✱ · `్య` 6.8e-3✱ · `్` 8.5e-11✱ · `మ` 7.5e-5✱ · `ంద` 0.99 · `య` 6.5e-4✱ · `␣గణ` 1.00 · `్` 6.0e-6✱ · `⏎` 2.6e-5✱ forced |
| 4 | `చి` 0.84 · `ర` 2.7e-4✱ · `వు` 0.01✱ · `␣అయిన` 0.06✱ · `్రు` 1.2e-4✱ · `న` 0.01✱ · `␣న` 0.02✱ · `్య` 1.1e-8✱ · `్య` 5.4e-4✱ · `్` 1.5e-7✱ · `చిత` 8.5e-3✱ · `్య` 2.5e-5✱ · `␣నియ` 1.00 · `మ` 8.7e-4✱ · `్య` 7.0e-4✱ · `␣ఇ` 0.95 · `శ` 5.3e-4✱ · `ీ` 2.6e-5✱ · `␣ఇ` 3.6e-5✱ · `త` 0.01✱ · `ను` 5.3e-3✱ · `న` 1.8e-3✱ · `్రి` 8.3e-6✱ · `మ` 8.8e-3✱ · `␣క` 0.02✱ · `్ర` 3.3e-6✱ · `్ర` 5.9e-3✱ · `్` 2.3e-5✱ · `జ` 0.21✱ · `ిత` 2.3e-3✱ · `్య` 2.2e-3✱ · `ిత` 0.52 · `ము` 0.87 · `మ` 3.3e-3✱ · `్` 4.1e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 141 tokens · 69.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నితక కమర్వద జ్మ్ర్ణీయ మ్రవణ్య మణింజల మీద మనెల్రజలో | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 2 | జతిలచనశ్రమ య్య్య్జమ్యనితిక్రియ మ్ర్ర్జక్రిను నీతిడ మ్వ్ర్జైనతినీ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 3 | జతి మతి నీతి మ మ్య్ర్జమ్రురమున్రమ ధ్య్ర్జజ్య్య్యజజజ్యజజజ్రిజతిం | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 4 | వితియకు వద్యము వృత్తము లో మతి మ్ర్ర్వేతిమ మల్రియ విజ్రను నల్ | `IIIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 15% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.007 · model's first choice kept 27% · constraint overrode 67% · backtracks 30

<details><summary>Token probabilities (141 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ని` 0.53 · `త` 0.65 · `క` 0.01 · `␣క` 0.02 · `మ` 0.15✱ · `ర` 0.71 · `్వ` 6.4e-6✱ · `ద` 9.3e-3 · `␣జ` 8.7e-4 · `్` 0.70 · `మ` 0.42 · `్ర` 0.86 · `్` 1.7e-6✱ · `ణ` 0.01✱ · `ీయ` 0.92 · `␣మ` 0.98 · `్ర` 0.62 · `వ` 0.89 · `ణ` 0.99 · `్య` 1.00 · `␣మ` 0.99 · `ణి` 5.3e-6✱ · `ంజ` 0.99 · `ల` 0.97 · `␣మీద` 0.97 · `␣మ` 1.9e-4✱ · `న` 0.01✱ · `ెల` 9.4e-4✱ · `్ర` 1.4e-5✱ · `జ` 0.04 · `లో` 0.16 · `⏎` 0.21 forced |
| 2 | `జ` 0.20 · `తి` 0.31 · `ల` 0.79 · `చన` 1.3e-4 · `శ` 2.6e-4✱ · `్రమ` 4.5e-4✱ · `␣య` 0.94 · `్య` 7.7e-5✱ · `్య` 1.4e-3✱ · `్` 1.6e-6✱ · `జ` 0.15 · `మ` 9.2e-3✱ · `్య` 1.2e-3✱ · `ని` 6.6e-3✱ · `తి` 0.70 · `క` 1.3e-3✱ · `్రియ` 1.7e-4✱ · `␣మ` 0.02✱ · `్ర` 3.3e-5✱ · `్ర` 3.2e-4✱ · `్` 6.3e-6✱ · `జ` 1.2e-4✱ · `క` 0.95 · `్రి` 2.9e-5✱ · `ను` 6.4e-4✱ · `␣నీ` 0.97 · `తి` 0.98 · `డ` 2.4e-4✱ · `␣మ` 0.04✱ · `్వ` 6.8e-8✱ · `్ర` 1.9e-4✱ · `్` 1.7e-7✱ · `జ` 2.2e-3✱ · `ైన` 9.5e-4✱ · `తి` 0.10✱ · `నీ` 0.69 · `⏎` 0.09✱ forced |
| 3 | `జ` 0.02✱ · `తి` 0.96 · `␣మ` 6.6e-3✱ · `తి` 0.65 · `␣నీ` 0.90 · `తి` 0.91 · `␣మ` 0.01✱ · `␣మ` 3.6e-4✱ · `్య` 1.2e-4✱ · `్ర` 2.4e-5✱ · `్` 3.4e-6✱ · `జ` 0.18✱ · `మ` 0.95 · `్రు` 1.7e-5✱ · `ర` 0.99 · `ము` 0.94 · `న` 1.4e-3✱ · `్రమ` 1.5e-5✱ · `␣` 1.3e-3✱ · `ధ్య` 1.6e-4✱ · `్ర` 5.2e-4✱ · `్` 5.8e-3✱ · `జ` 0.17✱ · `జ` 9.5e-3✱ · `్య` 6.3e-4✱ · `్య` 0.02✱ · `్య` 0.02✱ · `జ` 5.2e-3✱ · `జ` 0.08✱ · `జ` 0.04✱ · `్య` 1.9e-4✱ · `జ` 7.0e-4✱ · `జ` 2.4e-4✱ · `జ` 5.1e-4✱ · `్రి` 7.1e-4✱ · `జ` 8.2e-3✱ · `తి` 0.03✱ · `ం` 1.4e-3✱ · `⏎` 0.30✱ |
| 4 | `వి` 1.7e-3✱ · `తి` 7.2e-4✱ · `య` 4.0e-3✱ · `కు` 4.9e-3✱ · `␣వ` 0.01✱ · `ద్య` 0.03✱ · `ము` 0.17✱ · `␣వ` 0.02✱ · `ృ` 8.3e-4✱ · `త్త` 0.25 · `ము` 0.12 · `␣లో` 8.1e-3✱ · `␣మ` 0.07 · `తి` 0.09 · `␣మ` 0.08✱ · `్ర` 1.8e-4✱ · `్ర` 6.8e-4✱ · `్వ` 3.1e-5✱ · `ే` 2.6e-3✱ · `తి` 0.99 · `మ` 0.03✱ · `␣మ` 0.02✱ · `ల` 0.05✱ · `్రియ` 2.9e-4✱ · `␣` 0.04✱ · `వి` 0.19 · `జ` 3.5e-3✱ · `్ర` 2.5e-4✱ · `ను` 0.01✱ · `␣` 5.6e-4✱ · `న` 0.21✱ · `ల` 2.8e-3✱ · `్` 1.1e-8✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 129 tokens · 29.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | లతసరితత్యము లక్ష్మణివమ్ర ల లంకకు రాముడు స్ర్లాజనగా | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 2 | మతసరిమత్యము మత్రిమవత్రి సమంత మరుల్యము న్య్య్మస్రిమతయ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 3 | త్యతసమవత్రితతాలను రక్షువ జ్య్వ్తజ్రిరిమత్యము క్య్య్తత్గమనిక్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 4 | య తిరిగి ఛందళి జ్యళ్ళి పరిశ్రమ మ్యాం జయపుశ్యత ల్యాతరియమ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 13% · repeated lines 0 · mean token probability (geometric) 0.017 · model's first choice kept 46% · constraint overrode 49% · backtracks 0

<details><summary>Token probabilities (129 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ల` 0.10 · `త` 0.09✱ · `స` 0.09 · `రి` 0.02✱ · `త` 0.59 · `త` 0.02✱ · `్య` 1.2e-3✱ · `ము` 0.19 · `␣ల` 0.13 · `క్ష్` 0.16 · `మ` 0.19✱ · `ణి` 0.56 · `వ` 0.08 · `మ` 0.03 · `్ర` 5.8e-4✱ · `␣ల` 0.10 · `␣ల` 0.19 · `ంక` 0.10✱ · `కు` 0.59 · `␣రా` 0.61 · `ము` 0.70 · `డు` 0.57 · `␣స` 6.8e-3✱ · `్ర` 4.5e-4✱ · `్లా` 1.0e-3✱ · `జ` 0.02 · `న` 0.03✱ · `గా` 0.01✱ · `⏎` 0.85 |
| 2 | `మ` 0.24 · `త` 0.30 · `స` 0.06 · `రి` 0.51 · `మ` 0.05 · `త` 0.43 · `్య` 0.81 · `ము` 0.70 · `␣మ` 0.19 · `త` 0.08✱ · `్రి` 8.8e-5✱ · `మ` 0.19 · `వ` 0.17 · `త` 0.03✱ · `్రి` 1.6e-3✱ · `␣స` 0.05✱ · `మ` 2.6e-3✱ · `ంత` 0.03✱ · `␣మ` 0.76 · `రు` 0.49 · `ల` 0.09 · `్య` 5.3e-5✱ · `ము` 0.51 · `␣న` 1.4e-3✱ · `్య` 5.9e-7✱ · `్య` 4.1e-5✱ · `్` 2.0e-5✱ · `మ` 0.11✱ · `స` 0.95 · `్రి` 2.8e-3✱ · `మ` 0.96 · `త` 0.99 · `య` 9.1e-4✱ · `్` 4.7e-5✱ · `⏎` 0.11✱ forced |
| 3 | `త్య` 0.79 · `త` 0.02✱ · `స` 0.35 · `మ` 0.90 · `వ` 0.74 · `త` 0.94 · `్రి` 0.80 · `త` 7.9e-4✱ · `త` 0.99 · `ాలను` 6.0e-4✱ · `␣ర` 1.00 · `క్ష` 1.00 · `ు` 2.9e-4✱ · `వ` 0.96 · `␣జ` 7.1e-6✱ · `్య` 2.5e-6✱ · `్వ` 1.1e-5✱ · `్` 2.6e-3✱ · `త` 4.4e-5✱ · `జ` 0.78 · `్రి` 7.3e-5✱ · `రి` 0.56 · `మ` 0.90 · `త` 0.99 · `్య` 0.99 · `ము` 0.98 · `␣క` 0.69 · `్య` 9.5e-4✱ · `్య` 2.9e-3✱ · `్` 2.5e-6✱ · `త` 2.7e-5✱ · `త` 5.2e-4✱ · `్` 5.3e-6✱ · `గ` 0.49 · `మని` 0.63 · `క` 0.66 · `్` 4.0e-7✱ · `⏎` 2.1e-5✱ forced |
| 4 | `య` 0.10✱ · `␣తిరిగి` 1.2e-4✱ · `␣ఛ` 0.95 · `ంద` 0.91 · `ళి` 5.8e-6✱ · `␣జ` 1.8e-4✱ · `్య` 9.1e-5✱ · `ళ్ళ` 0.88 · `ి` 0.01✱ · `␣పరిశ` 0.98 · `్రమ` 1.3e-6✱ · `␣మ` 2.5e-3✱ · `్యా` 1.6e-6✱ · `ం` 0.99 · `␣జ` 1.00 · `య` 0.99 · `పు` 0.98 · `శ` 6.3e-3✱ · `్య` 9.0e-5✱ · `త` 0.83 · `␣ల` 0.04✱ · `్యా` 1.5e-6✱ · `త` 4.7e-4✱ · `రి` 0.97 · `య` 8.0e-4✱ · `మ` 0.99 · `్` 3.4e-5✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 148 tokens · 34.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కమల నివాస కృ స్య్య్గమ్య ద లస్రి ల ల్య్య్కక్రమముక్రమ న్య్య్గన్ శతకై | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 2 | మమలముమల్రిమ ల్య్మై విమలస్రురమై శమకై మమమక్యల లోక్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 3 | మమ ద దసత్రి విమల్రుధురైమ క్షమండి పయిన్యద జ్య్య్మల్యము లే | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 4 | కమవిజవిజ్రితు మ్ర్ర్గణ్య జ జణ్యణ వ్య్య్గణ్యము రాయిన ప్య్య్కక్రి ఇవా | `IIIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 28% · repeated lines 0 · mean token probability (geometric) 0.008 · model's first choice kept 33% · constraint overrode 61% · backtracks 0

<details><summary>Token probabilities (148 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.02 · `మ` 0.18 · `ల` 0.46 · `␣ని` 0.08✱ · `వా` 0.11 · `స` 0.25 · `␣క` 0.14 · `ృ` 7.2e-4✱ · `␣స` 4.2e-3✱ · `్య` 5.8e-4✱ · `్య` 3.5e-3✱ · `్` 8.2e-6✱ · `గ` 0.01✱ · `మ` 0.08✱ · `్య` 4.3e-3✱ · `␣ద` 0.06 · `␣ల` 0.05 · `స` 0.01 · `్రి` 9.9e-4✱ · `␣ల` 0.37 · `␣ల` 0.20 · `్య` 1.0e-3✱ · `్య` 8.7e-4✱ · `్` 4.2e-6✱ · `క` 0.11✱ · `క` 0.22 · `్రమ` 4.6e-5✱ · `ము` 0.04✱ · `క` 0.09✱ · `్రమ` 1.9e-5✱ · `␣న` 6.0e-3✱ · `్య` 1.7e-4✱ · `్య` 2.7e-3✱ · `్` 6.7e-5✱ · `గ` 0.16 · `న్` 0.02✱ · `␣శ` 0.18 · `త` 0.20 · `క` 0.07 · `ై` 0.07✱ · `⏎` 1.7e-3 forced |
| 2 | `మ` 0.06 · `మ` 0.28 · `ల` 0.14 · `ము` 0.03 · `మ` 0.07✱ · `ల` 0.23 · `్రి` 6.3e-4✱ · `మ` 0.67 · `␣ల` 0.02✱ · `్య` 6.5e-4✱ · `్` 5.2e-3✱ · `మై` 0.02✱ · `␣వి` 0.95 · `మ` 0.99 · `ల` 0.97 · `స` 0.01✱ · `్రు` 1.1e-4✱ · `ర` 0.92 · `మై` 3.8e-3✱ · `␣శ` 0.94 · `మ` 0.97 · `క` 0.56 · `ై` 0.77 · `␣మ` 0.12✱ · `మ` 0.69 · `మ` 5.8e-4✱ · `క` 0.40 · `్య` 2.9e-4✱ · `ల` 0.89 · `␣లో` 0.98 · `క` 0.96 · `్` 1.6e-11✱ · `⏎` 7.6e-5✱ forced |
| 3 | `మ` 0.90 · `మ` 1.9e-3✱ · `␣ద` 0.93 · `␣ద` 5.2e-4✱ · `స` 0.87 · `త్రి` 0.05✱ · `␣వి` 0.88 · `మ` 0.94 · `ల` 0.93 · `్రు` 2.2e-4✱ · `ధు` 3.9e-3✱ · `ర` 0.99 · `ై` 0.07✱ · `మ` 6.7e-4✱ · `␣` 2.1e-3✱ · `క్ష` 0.79 · `మ` 0.90 · `ండి` 2.0e-4✱ · `␣` 1.4e-4✱ · `ప` 9.4e-3✱ · `య` 8.8e-6✱ · `ిన` 0.24✱ · `్య` 4.1e-6✱ · `ద` 4.8e-4✱ · `␣జ` 5.2e-5✱ · `్య` 8.9e-3✱ · `్య` 7.7e-3✱ · `్` 9.3e-7✱ · `మ` 1.5e-4✱ · `ల` 0.03✱ · `్య` 2.7e-5✱ · `ము` 0.20✱ · `␣లే` 0.02✱ · `⏎` 0.71 forced |
| 4 | `క` 0.99 · `మ` 1.0e-4✱ · `వి` 6.7e-3✱ · `జ` 0.96 · `వి` 0.87 · `జ` 5.5e-3✱ · `్ర` 9.9e-5✱ · `ిత` 0.46 · `ు` 8.7e-3✱ · `␣మ` 3.7e-4✱ · `్ర` 1.6e-3✱ · `్ర` 1.1e-5✱ · `్` 6.8e-5✱ · `గ` 7.5e-4✱ · `ణ` 3.9e-3✱ · `్య` 1.9e-3✱ · `␣జ` 0.67 · `␣జ` 0.88 · `ణ` 8.9e-3✱ · `్య` 0.01✱ · `ణ` 0.48 · `␣వ` 0.93 · `్య` 7.6e-4✱ · `్య` 6.5e-5✱ · `్` 1.1e-7✱ · `గ` 5.5e-5✱ · `ణ` 7.2e-5✱ · `్య` 2.4e-4✱ · `ము` 0.08✱ · `␣రాయ` 0.96 · `ిన` 0.98 · `␣ప` 2.5e-5✱ · `్య` 7.4e-6✱ · `్య` 7.6e-4✱ · `్` 1.3e-5✱ · `క` 3.6e-4✱ · `క` 3.5e-4✱ · `్రి` 9.5e-5✱ · `␣ఇ` 9.5e-3✱ · `వా` 3.9e-3 |

</details>

[↑ meters](#meters)

---

<a id="vanamayuramu"></a>

## 34. వనమయూరము (vanamayuramu)

```text
Meter: వనమయూరము (vanamayuramu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 5 gaṇas: భ జ స న గా, i.e. UII IUI IIU III UU (14 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T2; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter వనమయూరము (vanamayuramu).

Meter: వనమయూరము (vanamayuramu), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 5 gaṇas: భ జ స న గా, i.e. UII IUI IIU III UU (14 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 84 tokens · 13.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జక్రి శలగత్యము జ జక్రి సన హన్నుమ్ | `UIIIUIIIUIIIUU` |
| 2 | నే క్రి స మలగ్య్యము జ జృత్రి సన లంకన్ | `UIIIUIIIUIIIUU` |
| 3 | సౌక్రి స మలగ్య్యము జ జక్రి సన సీమల్ | `UIIIUIIIUIIIUU` |
| 4 | మౌక్రి స మ సన్య్యను శమాన్ము డుడుడున్రీ | `UIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 26% · single-akshara words 33% · repeated lines 0 · mean token probability (geometric) 0.060 · model's first choice kept 56% · constraint overrode 33% · backtracks 0

<details><summary>Token probabilities (84 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.07 · `క` 0.06 · `్రి` 0.01✱ · `␣శ` 0.06 · `ల` 0.04 · `గ` 0.01 · `త` 0.02✱ · `్య` 1.1e-3✱ · `ము` 0.44 · `␣జ` 0.40 · `␣జ` 0.02✱ · `క` 0.02 · `్రి` 0.02✱ · `␣స` 2.2e-3✱ · `న` 0.22✱ · `␣హ` 0.98 · `న్ను` 8.7e-5✱ · `మ` 5.5e-3✱ · `్` 6.2e-7✱ · `⏎` 0.06✱ forced |
| 2 | `నే` 0.40 · `␣` 5.8e-4✱ · `క` 1.2e-3✱ · `్రి` 2.9e-3✱ · `␣స` 0.05 · `␣మ` 0.70 · `ల` 0.92 · `గ` 0.93 · `్య` 1.7e-4✱ · `్య` 0.93 · `ము` 0.89 · `␣జ` 0.94 · `␣జ` 0.93 · `ృత` 7.6e-9✱ · `్రి` 0.42 · `␣స` 0.71 · `న` 0.83 · `␣ల` 0.95 · `ంక` 0.82 · `న్` 0.07✱ · `⏎` 0.99 |
| 3 | `స` 0.99 · `ౌ` 1.00 · `క` 0.88 · `్రి` 0.95 · `␣స` 0.87 · `␣మ` 0.79 · `ల` 0.95 · `గ` 0.97 · `్య` 4.0e-4✱ · `్య` 0.90 · `ము` 0.79 · `␣జ` 0.77 · `␣జ` 0.72 · `క` 0.73 · `్రి` 0.74 · `␣స` 0.89 · `న` 0.91 · `␣సీ` 0.98 · `మ` 0.92 · `ల` 0.04✱ · `్` 3.9e-6✱ · `⏎` 0.56 |
| 4 | `మ` 0.63 · `ౌ` 0.79 · `క` 0.50 · `్రి` 0.40 · `␣స` 0.25 · `␣మ` 0.08 · `␣స` 0.13 · `న` 0.08 · `్య` 1.1e-3✱ · `్య` 0.25 · `ను` 0.06 · `␣శ` 0.81 · `మా` 6.7e-4✱ · `న్` 0.95 · `ము` 0.85 · `␣` 1.1e-4✱ · `డు` 7.2e-4✱ · `డు` 2.0e-3✱ · `డు` 0.05✱ · `న` 2.8e-3✱ · `్రీ` 1.9e-4✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 87 tokens · 19.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాము లగె సగ్రిము స ల్య్య్మత్యమను లే లెర్ | `UIIIUIIIUIIIUU` |
| 2 | రామ లమముల్ర సము ల్య్న్రన్ లకను దాటియ్ | `UIIIUIIIUIIIUU` |
| 3 | రామ కల రాము లత స్ప్య్రడ్యరమ లమ్యల్ | `UIIIUIIIUIIIUU` |
| 4 | న్య్య్నై మ లకమున్రి లడు లాలి వవ మల్రీ | `UIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 23% · repeated lines 0 · mean token probability (geometric) 0.007 · model's first choice kept 28% · constraint overrode 52% · backtracks 0

<details><summary>Token probabilities (87 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.01 · `ము` 0.07 · `␣ల` 0.05 · `గ` 8.9e-3 · `ె` 1.8e-3 · `␣స` 0.02 · `గ` 0.01✱ · `్రి` 1.2e-3✱ · `ము` 0.75 · `␣స` 0.11 · `␣ల` 0.03 · `్య` 4.0e-3✱ · `్య` 2.3e-4✱ · `్` 3.8e-6✱ · `మ` 0.09 · `త్య` 7.2e-4✱ · `మ` 0.02 · `ను` 0.02 · `␣లే` 3.5e-3✱ · `␣లె` 1.3e-3✱ · `ర` 1.1e-3✱ · `్` 1.3e-8✱ · `⏎` 0.24 forced |
| 2 | `రా` 0.28 · `మ` 0.27 · `␣ల` 0.10 · `మ` 0.02 · `ము` 0.02 · `ల` 0.03✱ · `్ర` 3.9e-5✱ · `␣స` 0.09 · `ము` 0.08 · `␣ల` 0.18 · `్య` 9.2e-4✱ · `్` 5.3e-5✱ · `న` 0.05 · `్ర` 1.2e-5✱ · `న్` 0.74 · `␣ల` 0.14 · `క` 0.02✱ · `ను` 0.04✱ · `␣దా` 1.4e-3✱ · `టి` 0.11 · `య` 1.1e-3✱ · `్` 2.4e-7✱ · `⏎` 0.70 |
| 3 | `రా` 0.25 · `మ` 0.21 · `␣కల` 6.5e-3 · `␣రా` 0.03 · `ము` 0.42 · `␣ల` 4.0e-4✱ · `త` 0.99 · `␣స్ప` 1.7e-4✱ · `్య` 3.7e-4✱ · `్ర` 2.4e-5✱ · `డ` 1.6e-3✱ · `్య` 3.2e-4✱ · `ర` 5.5e-3✱ · `మ` 0.47 · `␣ల` 0.52 · `మ` 0.71 · `్య` 1.6e-4✱ · `ల` 0.99 · `్` 4.2e-5✱ · `⏎` 2.7e-4✱ forced |
| 4 | `న` 6.3e-3✱ · `్య` 5.3e-3✱ · `్య` 0.72 · `్` 0.50 · `న` 0.76 · `ై` 4.1e-4✱ · `␣మ` 2.5e-4✱ · `␣ల` 0.76 · `క` 0.98 · `ము` 0.82 · `న` 9.1e-4✱ · `్రి` 2.2e-5✱ · `␣ల` 2.5e-3✱ · `డు` 1.7e-3✱ · `␣ల` 2.6e-3✱ · `ాలి` 1.6e-3✱ · `␣వ` 4.4e-3✱ · `వ` 2.7e-3✱ · `␣మ` 1.6e-3✱ · `ల` 0.01✱ · `్రీ` 6.5e-5✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 88 tokens · 40.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జక్రి శలగత్యముతి జక్రి సన హ్రీంమై | `UIIIUIIIUIIIUU` |
| 2 | నుక్రి జయకల్యము ని జ్ర్ర్నోంక చె రిసమ్రిబ్ | `UIIIUIIIUIIIUU` |
| 3 | ద్రౌక్రి ధ్రిపుతిమ్రికక మ్రన్ మక క్రి సమ్రిస్ | `UIIIUIIIUIIIUU` |
| 4 | మక్రి లకు శీఘమమ మైవవడునున్రిక్ | `UIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 19% · repeated lines 0 · mean token probability (geometric) 0.054 · model's first choice kept 64% · constraint overrode 32% · backtracks 30

<details><summary>Token probabilities (88 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.98 · `క` 0.94 · `్రి` 0.90 · `␣శ` 0.95 · `ల` 0.98 · `గ` 0.98 · `త` 0.99 · `్య` 0.99 · `ము` 0.91 · `తి` 0.01 · `␣జ` 0.87 · `క` 0.93 · `్రి` 0.78 · `␣స` 0.87 · `న` 0.93 · `␣హ` 0.99 · `్రీ` 0.96 · `ం` 0.80 · `మై` 0.94 · `⏎` 0.97 |
| 2 | `ను` 0.93 · `క` 0.92 · `్రి` 0.93 · `␣జ` 0.99 · `య` 0.96 · `క` 0.98 · `ల` 0.98 · `్య` 0.99 · `ము` 0.90 · `␣ని` 0.49 · `␣జ` 0.94 · `్ర` 1.0e-7✱ · `్ర` 8.9e-4✱ · `్` 3.3e-5✱ · `న` 0.69 · `ో` 2.5e-5✱ · `ంక` 0.52 · `␣చె` 0.99 · `␣రి` 8.1e-4 · `స` 0.92 · `మ` 0.99 · `్రి` 6.0e-6✱ · `బ` 4.0e-6✱ · `్` 1.1e-8✱ · `⏎` 0.35 |
| 3 | `ద్ర` 0.91 · `ౌ` 1.00 · `క` 0.99 · `్రి` 0.99 · `␣ధ` 1.00 · `్రి` 0.94 · `పు` 0.99 · `తి` 0.97 · `మ` 0.85 · `్రి` 0.99 · `క` 9.3e-5✱ · `క` 0.95 · `␣మ` 0.79 · `్ర` 1.9e-5✱ · `న్` 3.0e-3✱ · `␣మ` 0.12 · `క` 0.92 · `␣క్రి` 3.4e-4✱ · `␣స` 0.86 · `మ` 3.2e-3✱ · `్రి` 4.3e-5✱ · `స` 0.44 · `్` 9.8e-7✱ · `⏎` 0.19✱ forced |
| 4 | `మ` 0.15 · `క` 1.2e-4✱ · `్రి` 2.5e-4✱ · `␣ల` 0.27✱ · `కు` 0.98 · `␣శ` 0.99 · `ీ` 1.00 · `ఘ` 0.97 · `మ` 0.97 · `మ` 7.2e-4✱ · `␣మై` 5.8e-3✱ · `వ` 3.4e-3✱ · `వ` 0.02✱ · `డు` 9.9e-3✱ · `ను` 0.04✱ · `న` 1.2e-3✱ · `్రి` 1.5e-5✱ · `క` 3.7e-3✱ · `్` 2.5e-4✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 75 tokens · 43.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నర్రియ స సీత మన హ్ర్ద్నక్రియశవేయా | `UIIIUIIIUIIIUU` |
| 2 | సేర్రహిన రంథుడు నసించి లనవణ్యా | `UIIIUIIIUIIIUU` |
| 3 | లొర్రుటను నడ్రుడు ర మ్య్య్లోతముగ సీతన్ | `UIIIUIIIUIIIUU` |
| 4 | యెర్రియనునుంల్లనునుణీలముముతోతో | `UIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 13% · repeated lines 0 · mean token probability (geometric) 0.005 · model's first choice kept 36% · constraint overrode 53% · backtracks 30

<details><summary>Token probabilities (75 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `న` 5.0e-3 · `ర` 0.77 · `్రియ` 1.1e-5✱ · `␣స` 6.2e-3 · `␣సీ` 0.81 · `త` 0.76 · `␣మన` 2.8e-3 · `␣హ` 0.19 · `్ర` 5.8e-3✱ · `్` 2.0e-5✱ · `ద` 0.43 · `్` 1.8e-7✱ · `న` 0.18✱ · `క` 0.80 · `్రియ` 0.99 · `శ` 0.01✱ · `వే` 9.5e-5✱ · `యా` 1.9e-3 · `⏎` 0.70 |
| 2 | `సే` 0.95 · `ర` 7.5e-6✱ · `్రహ` 4.1e-6✱ · `ిన` 2.0e-3 · `␣ర` 6.5e-3 · `ంథ` 5.6e-3 · `ుడు` 0.90 · `␣న` 0.58 · `స` 1.1e-4✱ · `ించి` 0.88 · `␣ల` 1.2e-3✱ · `న` 5.9e-4✱ · `వ` 0.93 · `ణ` 0.86 · `్యా` 1.9e-3✱ · `⏎` 0.04 forced |
| 3 | `ల` 0.99 · `ొ` 1.00 · `ర` 3.4e-9✱ · `్రు` 6.7e-7✱ · `ట` 1.00 · `ను` 0.90 · `␣న` 0.92 · `డ` 0.99 · `్రు` 1.8e-4✱ · `డు` 2.3e-4✱ · `␣ర` 2.2e-4✱ · `␣మ` 1.4e-5✱ · `్య` 2.3e-6✱ · `్య` 4.8e-5✱ · `్` 1.6e-6✱ · `ల` 0.07✱ · `ో` 5.4e-5✱ · `త` 0.94 · `ము` 0.92 · `గ` 0.99 · `␣సీ` 0.95 · `త` 0.95 · `న్` 1.9e-3✱ · `⏎` 1.1e-5✱ forced |
| 4 | `య` 0.98 · `ె` 1.00 · `ర` 1.3e-5✱ · `్రియ` 5.1e-6✱ · `ను` 1.9e-3✱ · `ను` 7.2e-4✱ · `ం` 1.3e-4✱ · `ల్ల` 5.5e-4✱ · `ను` 4.8e-3✱ · `ను` 0.01✱ · `ణ` 3.9e-4✱ · `ీల` 0.01✱ · `ము` 7.5e-3✱ · `ము` 8.2e-3✱ · `తో` 3.1e-4✱ · `తో` 7.1e-3✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 81 tokens · 19.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మన్రహమయుడ్రి సము క్ద్ర్మాటినిమసిమ్రీ | `UIIIUIIIUIIIUU` |
| 2 | మొన్రికను చేరి మల య్య్య్వున్రముగ లమ్యం | `UIIIUIIIUIIIUU` |
| 3 | నీన్ర లను చూరిరితిమృష్టి హహనుమ్యా | `UIIIUIIIUIIIUU` |
| 4 | వేన్రిము సముద్రడటె హ్ర్య్వే లల యముశ్యం | `UIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.010 · model's first choice kept 31% · constraint overrode 59% · backtracks 0

<details><summary>Token probabilities (81 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.45 · `న` 0.06 · `్రహ` 3.4e-5✱ · `మ` 0.11 · `యు` 0.03✱ · `డ` 0.34✱ · `్రి` 7.0e-4✱ · `␣స` 0.14 · `ము` 0.92 · `␣క్` 3.0e-5✱ · `ద్ర` 0.13✱ · `్` 2.4e-8✱ · `మా` 6.9e-4✱ · `టి` 0.84 · `ని` 5.6e-3✱ · `మ` 0.26 · `సి` 0.05✱ · `మ` 9.7e-3✱ · `్రీ` 3.5e-5✱ · `⏎` 0.29 |
| 2 | `మ` 0.49 · `ొ` 6.7e-3✱ · `న` 0.05✱ · `్రి` 1.8e-4✱ · `క` 0.79 · `ను` 0.64 · `␣చే` 0.29 · `రి` 0.74 · `␣మ` 0.43 · `ల` 0.08 · `␣య` 0.03✱ · `్య` 8.1e-5✱ · `్య` 4.1e-4✱ · `్వ` 2.3e-4✱ · `ు` 0.01✱ · `న` 0.04✱ · `్ర` 5.0e-5✱ · `ము` 0.15 · `గ` 0.05✱ · `␣ల` 0.01✱ · `మ` 2.5e-3✱ · `్యం` 4.2e-5✱ · `⏎` 0.16✱ forced |
| 3 | `నీ` 0.06 · `న` 9.0e-5✱ · `్ర` 2.0e-5✱ · `␣ల` 0.03✱ · `ను` 0.77 · `␣చూ` 0.44 · `రి` 0.66 · `రి` 0.11 · `తి` 0.02 · `మ` 0.22 · `ృష్టి` 4.4e-5✱ · `␣హ` 5.4e-3✱ · `హ` 0.83 · `ను` 0.90 · `మ` 9.6e-4✱ · `్యా` 2.1e-6✱ · `⏎` 1.1e-3✱ forced |
| 4 | `వే` 0.83 · `న` 1.4e-5✱ · `్రి` 5.2e-5✱ · `ము` 0.32 · `␣స` 0.34 · `ము` 0.51 · `ద్ర` 5.7e-3✱ · `డ` 4.5e-3✱ · `ట` 0.98 · `ె` 0.98 · `␣హ` 2.4e-3✱ · `్ర` 1.7e-4✱ · `్య` 1.8e-4✱ · `్వ` 9.6e-6✱ · `ే` 4.8e-3✱ · `␣ల` 0.04✱ · `ల` 0.06 · `␣య` 0.04✱ · `ము` 0.53 · `శ` 2.1e-4✱ · `్యం` 3.8e-5✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 89 tokens · 21.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తమ్రిణి నియమ్య జట మ్ర్వ్ధన్యుడకముక్రా | `UIIIUIIIUIIIUU` |
| 2 | సమ్రుని శ జక్రి ల ల ల్య్య్శాడునుతమమ్యం | `UIIIUIIIUIIIUU` |
| 3 | యమ్ర జట మ్ర్వ్ధన్యుడక స్ర్ర్యాతతను లర్యం | `UIIIUIIIUIIIUU` |
| 4 | రామ్రు ప్రభుడుల్య్య్యవవరన్రరనమువ్యం | `UIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.019 · model's first choice kept 37% · constraint overrode 55% · backtracks 0

<details><summary>Token probabilities (89 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.03 · `మ` 0.52 · `్రి` 3.4e-3✱ · `ణి` 0.04 · `␣ని` 0.03 · `య` 0.02 · `మ` 0.46 · `్య` 5.7e-3✱ · `␣జ` 0.06 · `ట` 0.12 · `␣మ` 0.05✱ · `్ర` 0.02✱ · `్వ` 6.5e-4✱ · `్` 7.6e-5✱ · `ధ` 0.02✱ · `న్` 0.02✱ · `యు` 0.18 · `డ` 0.51 · `క` 0.02✱ · `ము` 0.02✱ · `క` 3.3e-3✱ · `్రా` 2.6e-4✱ · `⏎` 0.16 |
| 2 | `స` 0.25 · `మ` 0.34 · `్ర` 1.7e-4✱ · `ు` 0.14 · `ని` 0.05 · `␣శ` 0.08✱ · `␣జ` 0.06 · `క` 0.12 · `్రి` 8.7e-4✱ · `␣ల` 0.72 · `␣ల` 0.02✱ · `␣ల` 0.08✱ · `్య` 9.0e-4✱ · `్య` 9.1e-4✱ · `్` 1.2e-6✱ · `శ` 1.7e-3✱ · `ాడు` 0.02✱ · `ను` 3.4e-3✱ · `త` 0.67 · `మ` 0.70 · `మ` 0.40✱ · `్యం` 2.2e-5✱ · `⏎` 7.3e-4✱ forced |
| 3 | `య` 0.72 · `మ` 0.97 · `్ర` 1.5e-5✱ · `␣జ` 0.85 · `ట` 0.97 · `␣మ` 0.93 · `్ర` 0.98 · `్వ` 0.98 · `్` 1.00 · `ధ` 0.99 · `న్` 0.97 · `యు` 0.99 · `డ` 0.94 · `క` 0.43 · `␣స` 3.8e-4✱ · `్ర` 3.4e-5✱ · `్ర` 2.8e-5✱ · `్యా` 7.3e-5✱ · `త` 7.7e-3✱ · `త` 0.59 · `ను` 0.49 · `␣ల` 0.02✱ · `ర` 0.86 · `్యం` 6.5e-6✱ · `⏎` 0.12✱ forced |
| 4 | `␣రామ` 0.03✱ · `్రు` 4.7e-6✱ · `␣ప్రభు` 3.7e-4✱ · `డు` 0.94 · `ల` 3.5e-4✱ · `్య` 2.3e-4✱ · `్య` 0.01✱ · `్య` 0.11✱ · `వ` 3.5e-3✱ · `వ` 0.03✱ · `ర` 5.6e-3✱ · `న` 0.04✱ · `్ర` 7.6e-4✱ · `ర` 0.20 · `న` 0.75 · `ము` 0.07✱ · `వ` 0.51 · `్యం` 2.0e-5✱ |

</details>

[↑ meters](#meters)

---

<a id="mangalamahasri"></a>

## 35. మంగళమహాశ్రీ (mangalamahasri)

```text
Meter: మంగళమహాశ్రీ (mangalamahasri), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 9 gaṇas: భ జ స న భ జ స న గా, i.e. UII IUI IIU III UII IUI IIU III UU (26 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th and the 17th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter మంగళమహాశ్రీ (mangalamahasri).

Meter: మంగళమహాశ్రీ (mangalamahasri), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 9 gaṇas: భ జ స న భ జ స న గా, i.e. UII IUI IIU III UII IUI IIU III UU (26 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th and the 17th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 158 tokens · 35.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జన్త నమసిత్ర మమ మ్ర్మ్చమ్రముమమమ్వరజ సర్తనమసిత్ర మమ జేయమ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | మాన్తమమజన్త నమమస్ర మమ మ్ర్మల్యమమమమ్రవమ సర్త మినినవ్యం | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | నే న్తవతితిమ్రమకు స్త్ర్రృంగళమహాశ్రియకుమృమ్యమమ లేదుతితివీతియ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | మీ న్తియతితియ్యవవమీతిమతి తియ్యయయ మ్య్య్యేయ్యతితి యయ్యయయయయ్యయ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 9% · repeated lines 0 · mean token probability (geometric) 0.019 · model's first choice kept 35% · constraint overrode 56% · backtracks 0

<details><summary>Token probabilities (158 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.35 · `న్` 0.21 · `త` 0.04 · `␣న` 8.0e-3 · `మ` 0.05 · `స` 4.5e-3 · `ిత` 0.02✱ · `్ర` 0.02✱ · `␣మ` 0.21 · `మ` 0.53 · `␣మ` 0.05✱ · `్ర` 1.2e-3✱ · `్` 1.2e-4✱ · `మ` 0.19 · `్` 4.6e-7✱ · `చ` 5.4e-3✱ · `మ` 0.03✱ · `్ర` 2.1e-3✱ · `ము` 0.07 · `మ` 0.09 · `మ` 0.08 · `మ` 0.02✱ · `్వర` 1.5e-5✱ · `జ` 0.92 · `␣సర్` 2.7e-4✱ · `త` 0.47 · `న` 0.14 · `మ` 0.75 · `స` 0.53 · `ిత` 0.69 · `్ర` 0.43 · `␣మ` 0.35 · `మ` 0.79 · `␣జ` 0.87 · `ే` 0.83 · `య` 0.73 · `మ` 0.35 · `్` 6.0e-5✱ · `⏎` 0.05✱ forced |
| 2 | `మ` 0.04✱ · `ాన` 0.02✱ · `్` 1.1e-5✱ · `త` 5.8e-3✱ · `మ` 0.15 · `మ` 0.42 · `జ` 0.31 · `న్` 0.71 · `త` 0.86 · `␣న` 0.91 · `మ` 0.97 · `మ` 4.5e-3✱ · `స` 7.1e-3✱ · `్ర` 0.64 · `␣మ` 0.57 · `మ` 0.91 · `␣మ` 0.72 · `్ర` 0.87 · `్` 0.87 · `మ` 0.82 · `ల` 0.44 · `్య` 3.7e-3✱ · `మ` 0.48 · `మ` 0.25 · `మ` 0.22✱ · `మ` 0.29 · `్ర` 5.1e-3✱ · `వ` 0.07 · `మ` 0.23 · `␣సర్` 0.25 · `త` 0.25 · `␣మ` 0.95 · `ిన` 1.5e-4✱ · `ిన` 2.6e-3✱ · `వ` 0.88 · `్యం` 6.1e-4✱ · `⏎` 0.63 |
| 3 | `␣` 2.4e-5✱ · `నే` 9.9e-5✱ · `␣` 1.8e-5✱ · `న` 1.1e-8✱ · `్` 5.7e-8✱ · `త` 6.1e-4✱ · `వ` 1.6e-4✱ · `తి` 6.7e-3✱ · `తి` 0.04✱ · `మ` 4.2e-3✱ · `్రమ` 2.2e-3✱ · `కు` 6.2e-3✱ · `␣` 8.3e-3✱ · `స్త` 1.7e-3✱ · `్ర` 2.7e-4✱ · `్ర` 8.6e-4✱ · `ృ` 1.2e-3✱ · `ంగళ` 0.30 · `మ` 0.68 · `హా` 0.82 · `శ` 0.75 · `్రియ` 1.0e-3✱ · `కు` 9.8e-3✱ · `మ` 0.02✱ · `ృ` 1.9e-3✱ · `మ` 0.10 · `్య` 0.02✱ · `మ` 0.23 · `మ` 0.02✱ · `␣లేదు` 1.7e-3✱ · `తి` 1.1e-3✱ · `తి` 1.6e-3✱ · `వ` 7.2e-4✱ · `ీ` 1.6e-3✱ · `తి` 0.01✱ · `య` 8.6e-3✱ · `్` 6.8e-5✱ · `⏎` 0.01✱ forced |
| 4 | `మ` 3.5e-3✱ · `ీ` 1.2e-4✱ · `␣` 3.1e-3✱ · `న్` 3.0e-4✱ · `తి` 0.03✱ · `య` 0.70 · `తి` 0.88 · `తి` 0.03✱ · `య` 3.2e-3✱ · `్య` 2.3e-3✱ · `వ` 0.04 · `వ` 0.06 · `మ` 0.15 · `ీ` 0.01✱ · `తి` 0.80 · `మ` 0.66 · `తి` 0.80 · `␣` 0.19 · `తి` 0.13✱ · `య` 0.15✱ · `్య` 7.4e-4✱ · `య` 0.95 · `య` 0.90 · `␣మ` 1.8e-4✱ · `్య` 2.4e-4✱ · `్య` 0.02✱ · `్య` 0.05✱ · `ే` 1.4e-3✱ · `య` 0.11✱ · `్` 0.24 · `య` 7.0e-6✱ · `తి` 6.5e-3✱ · `తి` 0.04✱ · `␣` 0.48 · `య` 0.06✱ · `య` 0.22✱ · `్య` 0.01✱ · `య` 0.94 · `య` 9.9e-6✱ · `య` 1.4e-3✱ · `య` 0.04✱ · `్య` 7.7e-3✱ · `య` 0.03✱ · `్` 8.4e-4✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 146 tokens · 34.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీ శతరుణానర జనృత్రి శ శభశ్రిసత మ్రిత్యునుమశీత మ మమున్ రన్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | శీ శతము జజ్వరర జిత్య మశ లంకకు చొచెన్ జయము రాముడు శతన్ సుమ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | శ్రీ శివముడుజ్యము మశిన్రకకు వెళ్ళెడడు సీతను మమత్రను తమాతమ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | మా శలును చూసి న్నివి ర్య్య్మమ్య భ జ సన్రజ స జ్య్య్మారుతరుణానరజనన్రజ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 30% · repeated lines 0 · mean token probability (geometric) 0.020 · model's first choice kept 40% · constraint overrode 51% · backtracks 0

<details><summary>Token probabilities (146 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.57 · `్రీ` 0.67 · `␣శ` 0.02 · `త` 0.37 · `రు` 0.15 · `ణ` 0.02 · `ాన` 0.01✱ · `ర` 0.06 · `␣జన` 6.1e-3 · `ృత` 7.1e-5✱ · `్రి` 2.1e-3✱ · `␣శ` 0.27 · `␣శ` 0.15 · `భ` 6.7e-3 · `శ` 0.03✱ · `్రి` 0.02✱ · `స` 2.1e-3 · `త` 0.04✱ · `␣మ` 0.01✱ · `్ర` 6.1e-3✱ · `ిత` 0.05✱ · `్య` 0.06✱ · `ు` 0.56 · `ను` 0.04✱ · `మ` 3.6e-4✱ · `శ` 0.98 · `ీ` 0.97 · `త` 0.05✱ · `␣మ` 0.27✱ · `␣మ` 0.41 · `ము` 0.16 · `న్` 0.18 · `␣ర` 0.05 · `న్` 0.03✱ · `⏎` 0.29 |
| 2 | `శ` 0.37 · `ీ` 0.72 · `␣శ` 4.4e-4✱ · `త` 0.05 · `ము` 0.20 · `␣జ` 0.04 · `జ` 0.02✱ · `్వర` 3.4e-4✱ · `ర` 0.89 · `␣జ` 2.9e-4✱ · `ిత` 2.5e-3✱ · `్య` 0.02✱ · `␣మ` 0.07✱ · `శ` 0.27 · `␣ల` 0.27 · `ం` 0.02✱ · `క` 5.0e-3✱ · `కు` 0.97 · `␣చ` 0.88 · `ొ` 0.02✱ · `చె` 4.1e-4✱ · `న్` 0.05✱ · `␣జ` 0.26 · `య` 0.15 · `ము` 0.28 · `␣రా` 0.83 · `ము` 0.41 · `డు` 0.48 · `␣శ` 0.03✱ · `త` 0.58 · `న్` 0.06✱ · `␣సు` 0.90 · `మ` 0.91 · `్` 7.3e-6✱ · `⏎` 5.2e-3✱ forced |
| 3 | `శ` 0.81 · `్రీ` 0.61 · `␣శి` 7.5e-4✱ · `వ` 0.78 · `ము` 0.65 · `డు` 0.83 · `జ` 1.0e-4✱ · `్య` 3.9e-3✱ · `ము` 0.74 · `␣మ` 0.74 · `శ` 0.84 · `ిన` 2.8e-5✱ · `్ర` 1.4e-4✱ · `క` 0.97 · `కు` 0.99 · `␣వె` 1.00 · `ళ్ళ` 1.00 · `ె` 0.99 · `డ` 0.10 · `డు` 0.04✱ · `␣సీ` 1.00 · `త` 0.97 · `ను` 0.96 · `␣మ` 0.91 · `మ` 0.84 · `త` 8.0e-4✱ · `్ర` 3.3e-5✱ · `ను` 6.4e-3✱ · `␣` 7.6e-4✱ · `త` 1.9e-5✱ · `మా` 2.1e-4✱ · `త` 8.8e-4✱ · `మ` 1.3e-3✱ · `్` 6.4e-5✱ · `⏎` 0.51 |
| 4 | `మా` 6.7e-5✱ · `␣` 8.8e-6✱ · `శ` 8.4e-7✱ · `లు` 3.6e-5✱ · `ను` 3.5e-4✱ · `␣చూ` 0.01✱ · `సి` 0.20 · `␣` 5.2e-3✱ · `న్ని` 6.3e-3✱ · `వి` 0.20 · `␣ర` 8.7e-4✱ · `్య` 3.4e-4✱ · `్య` 5.2e-4✱ · `్` 1.1e-4✱ · `మ` 0.01✱ · `మ` 0.04✱ · `్య` 5.2e-4✱ · `␣భ` 0.83 · `␣జ` 0.30 · `␣స` 0.37 · `న` 9.3e-3✱ · `్ర` 3.1e-5✱ · `జ` 0.17 · `␣స` 0.20 · `␣` 0.33 · `జ` 3.4e-3✱ · `్య` 1.8e-4✱ · `్య` 9.8e-4✱ · `్` 9.6e-10✱ · `మారు` 5.5e-8✱ · `త` 0.96 · `రు` 1.8e-3✱ · `ణ` 0.45 · `ాన` 0.14✱ · `ర` 0.16✱ · `జ` 0.02✱ · `న` 0.70 · `న` 0.12✱ · `్ర` 7.3e-4✱ · `జ` 0.22 · `్` 1.2e-6✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 154 tokens · 62.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మన్రిసరసిల్య సలె వ్వ్య్మన్వచతుడర్మశనుమత్యుముమమన్రిమతిగై జై | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | సన్రముమ దాటె మల సన్రమును మహ్వశ శ్రి జల్లెలుచు లల్యతి జితం ప్రణ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | వేన్రును మనత్రిమతి గ్య్య్విల్య లలమత్తి మన జ్య్య్వీల జితతిం ల్ల్య ల ల్యుయయ్యం | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | మ్ర్యున్రహశరీయ మమమోవవ దిగవ్రిగగ ముమ్రిమమమమ్రిమతి సర్వవ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.011 · model's first choice kept 34% · constraint overrode 58% · backtracks 30

<details><summary>Token probabilities (154 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.93 · `న` 0.95 · `్రి` 6.2e-6✱ · `స` 3.7e-3 · `ర` 0.03 · `సి` 3.2e-3 · `ల` 0.02✱ · `్య` 0.97 · `␣స` 1.1e-3 · `లె` 7.7e-3✱ · `␣వ` 0.89 · `్వ` 1.3e-3✱ · `్య` 0.15 · `్` 4.4e-6✱ · `మన` 8.9e-4✱ · `్వ` 0.28 · `చ` 6.7e-3 · `తు` 0.01 · `డ` 3.1e-3 · `ర్మ` 5.2e-4 · `శ` 0.95 · `ను` 5.1e-4✱ · `మ` 8.5e-4✱ · `త` 0.10✱ · `్య` 9.2e-4✱ · `ు` 0.14 · `ము` 0.39 · `మ` 0.01✱ · `మ` 0.57 · `న` 0.14 · `్రి` 0.02 · `మ` 0.81 · `తి` 0.84 · `గ` 0.90 · `ై` 0.85 · `␣జ` 0.85 · `ై` 0.93 · `⏎` 7.9e-3✱ forced |
| 2 | `␣స` 0.64 · `న్` 3.9e-5✱ · `ర` 4.0e-4✱ · `ము` 0.65 · `మ` 6.6e-4 · `␣దా` 0.84 · `ట` 0.69 · `ె` 0.39 · `␣మ` 4.0e-3 · `ల` 0.09✱ · `␣స` 1.2e-3✱ · `న` 6.7e-3✱ · `్ర` 2.8e-4✱ · `ము` 0.91 · `ను` 0.94 · `␣మ` 0.80 · `హ` 0.97 · `్వ` 1.2e-6✱ · `శ` 0.97 · `␣శ` 0.01✱ · `్రి` 6.7e-4✱ · `␣జ` 1.6e-3✱ · `ల్ల` 0.04✱ · `ె` 1.00 · `లు` 4.0e-3✱ · `చు` 0.06✱ · `␣ల` 0.23 · `ల` 0.46 · `్య` 1.3e-4✱ · `తి` 0.94 · `␣జ` 0.94 · `ిత` 1.9e-4✱ · `ం` 5.4e-3✱ · `␣ప్ర` 8.3e-4✱ · `ణ` 5.0e-4✱ · `్` 3.5e-6✱ · `⏎` 0.06✱ forced |
| 3 | `␣వే` 0.87 · `న` 3.9e-6✱ · `్రు` 1.3e-4✱ · `ను` 0.92 · `␣మ` 0.98 · `న` 0.94 · `త్రి` 4.1e-3✱ · `మ` 0.95 · `తి` 0.98 · `␣గ` 4.9e-3✱ · `్య` 6.2e-6✱ · `్య` 7.3e-4✱ · `్` 2.3e-5✱ · `వి` 3.9e-5✱ · `ల` 0.12✱ · `్య` 6.9e-4✱ · `␣ల` 0.41 · `ల` 0.81 · `మ` 0.90 · `త్తి` 6.1e-5✱ · `␣మ` 0.99 · `న` 1.00 · `␣జ` 6.2e-4✱ · `్య` 6.8e-5✱ · `్య` 1.7e-5✱ · `్వ` 8.2e-6✱ · `ీల` 5.5e-5✱ · `␣జ` 0.99 · `ిత` 6.4e-4✱ · `తి` 0.96 · `ం` 3.5e-5✱ · `␣` 2.8e-4✱ · `ల్ల` 2.5e-3✱ · `్య` 6.0e-3✱ · `␣ల` 3.0e-3✱ · `␣ల` 0.03✱ · `్య` 0.01✱ · `ు` 2.5e-3✱ · `య` 6.4e-3✱ · `య` 5.0e-3✱ · `్య` 1.0e-3✱ · `ం` 5.0e-3✱ · `⏎` 0.10✱ forced |
| 4 | `మ` 0.02✱ · `్ర` 8.8e-4✱ · `్య` 8.9e-4✱ · `ు` 3.5e-3✱ · `న` 1.5e-4✱ · `్రహ` 1.5e-5✱ · `శ` 0.86 · `రీ` 4.8e-4✱ · `య` 0.98 · `␣మ` 0.78 · `మ` 0.84 · `మ` 2.9e-3✱ · `ో` 1.3e-5✱ · `వ` 1.5e-3✱ · `వ` 3.8e-3✱ · `␣ది` 0.01✱ · `గ` 0.02✱ · `వ` 0.01✱ · `్రి` 3.1e-4✱ · `గ` 0.02✱ · `గ` 0.01✱ · `␣మ` 0.03✱ · `ు` 5.1e-3✱ · `మ` 0.93 · `్రి` 2.0e-3✱ · `మ` 0.98 · `మ` 0.83 · `మ` 0.71 · `మ` 7.4e-3✱ · `్రి` 0.02✱ · `మ` 2.9e-6✱ · `తి` 1.3e-3✱ · `␣సర్` 2.3e-3✱ · `వ` 0.21 · `వ` 0.13✱ · `్` 1.2e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 168 tokens · 63.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | కల్లి జదియుల్ర మ చగై జగహినమ్రు చతకౌ మనవ తల్లి జదియుల్రమ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | ధ్రా ల్ల మ మమగ్య ల మతవ్రు తత జల్యల మతన్ మశయమాణ్య మిత లేమగ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | నౌ ల్లదియులల్రు సమ శ్యమ్య్య మిత లేమగె మనవ్రియ టు లుల్యలు లు లువ్ ట్టివ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | వా ల్ల న భ జస్ర న భ జ్ర్ర్భర్రి ల్ల లడిష్ లకువు ల్ర్ల్వాది దిడిదిన్మభకుగీనన్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 37% · repeated lines 0 · mean token probability (geometric) 0.013 · model's first choice kept 40% · constraint overrode 54% · backtracks 30

<details><summary>Token probabilities (168 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `క` 0.94 · `ల్లి` 0.78 · `␣జ` 1.5e-3 · `ది` 0.25 · `యు` 5.0e-3 · `ల` 0.61 · `్ర` 2.2e-4✱ · `␣మ` 0.08 · `␣చ` 5.0e-3 · `గ` 0.88 · `ై` 0.94 · `␣జ` 0.01 · `గ` 2.9e-3 · `హ` 0.89 · `ిన` 3.4e-4 · `మ` 0.55 · `్రు` 0.13✱ · `␣చ` 3.0e-3 · `త` 2.0e-3 · `క` 0.93 · `ౌ` 0.97 · `␣మ` 0.95 · `న` 0.51 · `వ` 0.95 · `␣` 3.2e-3✱ · `త` 0.46 · `ల్లి` 0.82 · `␣జ` 0.99 · `ది` 0.96 · `యు` 1.00 · `ల` 0.99 · `్ర` 0.95 · `మ` 0.62 · `్` 2.0e-7✱ · `⏎` 9.0e-5✱ forced |
| 2 | `ధ` 0.99 · `్రా` 0.99 · `␣` 4.1e-5✱ · `ల` 2.4e-5✱ · `్` 7.5e-8✱ · `ల` 0.04✱ · `␣మ` 0.12 · `␣మ` 0.10 · `మ` 0.09 · `గ` 0.02 · `్య` 1.5e-3✱ · `␣ల` 3.2e-3✱ · `␣మ` 0.86 · `త` 1.9e-4✱ · `వ` 0.96 · `్రు` 2.2e-4✱ · `␣త` 0.55 · `త` 1.5e-3✱ · `␣జ` 0.96 · `ల` 5.3e-4✱ · `్య` 5.6e-4✱ · `ల` 0.68 · `␣మ` 5.1e-3✱ · `త` 7.0e-3✱ · `న్` 0.28 · `␣మ` 2.9e-4✱ · `శ` 0.99 · `య` 1.3e-5✱ · `మా` 0.99 · `ణ` 1.00 · `్య` 1.00 · `␣మ` 0.99 · `ిత` 0.99 · `␣ల` 0.66 · `ే` 0.85 · `మ` 0.77 · `గ` 0.89 · `్` 1.3e-8✱ · `⏎` 3.2e-3✱ forced |
| 3 | `న` 0.81 · `ౌ` 4.5e-3✱ · `␣` 0.96 · `ల` 8.6e-5✱ · `్` 2.4e-9✱ · `ల` 0.89 · `ది` 0.44 · `యు` 0.71 · `ల` 0.81 · `ల` 0.68 · `్రు` 2.1e-3✱ · `␣స` 0.97 · `మ` 0.99 · `␣శ` 4.2e-4✱ · `్య` 0.01✱ · `మ` 5.9e-4✱ · `్య` 8.1e-5✱ · `్య` 0.86 · `␣మ` 0.95 · `ిత` 0.98 · `␣ల` 0.94 · `ే` 0.90 · `మ` 0.92 · `గ` 0.96 · `ె` 5.0e-3✱ · `␣మ` 1.00 · `న` 0.82 · `వ` 0.99 · `్రియ` 6.8e-6✱ · `␣` 0.91 · `టు` 1.3e-5✱ · `␣` 2.4e-3✱ · `లు` 3.9e-4✱ · `ల` 4.0e-4✱ · `్య` 1.8e-5✱ · `లు` 0.01✱ · `␣` 4.6e-3✱ · `లు` 3.4e-4✱ · `␣ల` 0.01✱ · `ు` 5.2e-3✱ · `వ` 3.2e-4✱ · `్` 1.2e-5✱ · `␣` 1.8e-3✱ · `ట్టి` 4.1e-5✱ · `వ` 2.6e-4✱ · `్` 3.6e-3✱ · `⏎` 0.34 |
| 4 | `వా` 0.01✱ · `␣` 1.7e-3✱ · `ల` 5.3e-3✱ · `్` 1.7e-6✱ · `ల` 0.24✱ · `␣న` 0.58 · `␣భ` 0.65 · `␣జ` 0.25 · `స` 0.09✱ · `్ర` 6.6e-4✱ · `␣న` 0.03✱ · `␣భ` 8.6e-3✱ · `␣జ` 0.12✱ · `్ర` 6.2e-4✱ · `్ర` 0.13✱ · `్` 1.1e-4✱ · `భర` 6.8e-5✱ · `్రి` 1.7e-6✱ · `␣` 1.4e-4✱ · `ల్ల` 9.7e-3✱ · `␣ల` 7.5e-3✱ · `డి` 2.8e-4✱ · `ష్` 7.9e-4✱ · `␣ల` 1.6e-3✱ · `కు` 1.4e-3✱ · `వు` 0.01✱ · `␣ల` 6.0e-3✱ · `్ర` 6.4e-4✱ · `్` 1.6e-5✱ · `ల` 2.7e-4✱ · `్` 1.7e-4✱ · `వ` 5.8e-4✱ · `ా` 0.01✱ · `ది` 0.02✱ · `␣ది` 6.7e-3✱ · `డి` 8.7e-3✱ · `ది` 0.07✱ · `న` 5.1e-3✱ · `్` 5.1e-4✱ · `మ` 0.03✱ · `భ` 0.86 · `కు` 2.6e-4✱ · `గ` 3.0e-3✱ · `ీ` 0.02✱ · `న` 0.07✱ · `న` 0.03✱ · `్` 1.6e-5✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 149 tokens · 34.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జన్తృవమమమ్రమమ ద్ర్య్జమ్యము ని మవ్వరయ య్య్య్జజ్యమమతమ్రి మమమమ్యం | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | నన్తమమమమ్యనన మ్మ్ర్నమ్య మమతన్ మమమ మ్యమ్యమమజగ్యము మమమ్యం | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | మిన్తమమనన్ లమను మిన్ మమమమగ్రుకలు మీరు అడిగిన్యమమమహ్యా | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | ఈన్తిపు నియమ్య మళమృశ్రియను భజ్రస భజృస్రతను పాటి ఇక స్తుచ్చే | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.016 · model's first choice kept 45% · constraint overrode 49% · backtracks 0

<details><summary>Token probabilities (149 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.35 · `న్` 0.21 · `త` 0.04 · `ృ` 0.12 · `వ` 0.07 · `మ` 0.18 · `మ` 0.13 · `మ` 0.14 · `్ర` 1.4e-3✱ · `మ` 0.25 · `మ` 0.16 · `␣ద` 0.01✱ · `్ర` 4.7e-3✱ · `్య` 6.9e-3✱ · `్` 2.8e-7✱ · `జ` 8.4e-3✱ · `మ` 0.24 · `్య` 2.2e-3✱ · `ము` 0.25 · `␣ని` 0.02 · `␣మ` 0.05 · `వ` 0.02 · `్వర` 6.4e-4✱ · `య` 0.04 · `␣య` 0.02✱ · `్య` 2.2e-5✱ · `్య` 4.3e-4✱ · `్` 4.9e-5✱ · `జ` 5.6e-3✱ · `జ` 0.23✱ · `్య` 4.6e-3✱ · `మ` 0.18 · `మ` 0.07✱ · `త` 0.03✱ · `మ` 0.24 · `్రి` 1.5e-3✱ · `␣మ` 0.06✱ · `మ` 0.25✱ · `మ` 0.19 · `మ` 0.11✱ · `్యం` 1.0e-3✱ · `⏎` 0.10✱ forced |
| 2 | `న` 0.53 · `న` 0.03✱ · `్` 1.1e-6✱ · `త` 4.7e-3✱ · `మ` 0.64 · `మ` 0.66 · `మ` 0.55 · `మ` 0.48 · `్య` 1.3e-3✱ · `న` 0.69 · `న` 0.02✱ · `␣మ` 0.71 · `్` 7.7e-5✱ · `మ` 0.95 · `్ర` 6.2e-6✱ · `్` 1.7e-5✱ · `న` 1.2e-3✱ · `మ` 0.73 · `్య` 9.7e-4✱ · `␣మ` 4.8e-3✱ · `మ` 0.70 · `త` 0.95 · `న్` 6.2e-4✱ · `␣మ` 0.62 · `మ` 0.84 · `మ` 0.88 · `␣మ` 0.05✱ · `్య` 4.3e-4✱ · `మ` 0.95 · `్య` 2.1e-4✱ · `మ` 5.0e-3✱ · `మ` 9.3e-3✱ · `జ` 0.71 · `గ` 0.66 · `్య` 2.8e-4✱ · `ము` 3.8e-4✱ · `␣మ` 0.78 · `మ` 0.95 · `మ` 0.93 · `్యం` 1.2e-4✱ · `⏎` 0.91 |
| 3 | `మ` 0.89 · `ిన` 5.4e-3✱ · `్` 2.7e-7✱ · `త` 4.6e-4✱ · `మ` 0.39 · `మ` 0.20 · `న` 0.80 · `న్` 4.5e-3✱ · `␣ల` 0.28 · `మ` 0.91 · `ను` 0.98 · `␣మ` 0.97 · `ిన` 6.3e-6✱ · `్` 7.1e-4✱ · `␣మ` 0.66 · `మ` 0.96 · `మ` 0.91 · `మ` 2.4e-3✱ · `గ` 0.96 · `్రు` 7.0e-8✱ · `క` 0.98 · `లు` 3.7e-4✱ · `␣మీరు` 1.00 · `␣అ` 1.00 · `డి` 1.00 · `గిన` 0.99 · `్య` 1.7e-7✱ · `మ` 0.99 · `మ` 1.4e-3✱ · `మ` 0.75 · `హ` 0.03✱ · `్యా` 7.0e-7✱ · `⏎` 2.9e-6 forced |
| 4 | `ఈ` 0.17 · `న` 4.4e-4✱ · `్` 5.6e-5✱ · `తి` 2.2e-3✱ · `పు` 1.00 · `␣నియ` 0.99 · `మ` 0.91 · `్య` 2.4e-7✱ · `␣మ` 0.98 · `ళ` 1.0e-3✱ · `మ` 0.95 · `ృ` 8.6e-7✱ · `శ` 0.93 · `్రియ` 7.2e-4✱ · `ను` 3.7e-4✱ · `␣భ` 0.48 · `జ` 2.5e-3✱ · `్ర` 4.1e-4✱ · `స` 0.33 · `␣భ` 0.88 · `జ` 0.89 · `ృ` 5.6e-6✱ · `స` 0.97 · `్ర` 1.8e-4✱ · `త` 0.21 · `ను` 0.90 · `␣పా` 7.4e-4✱ · `టి` 1.00 · `␣ఇ` 1.1e-4✱ · `క` 0.02✱ · `␣` 0.99 · `స్తు` 9.8e-5✱ · `చ్చే` 1.2e-6✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 176 tokens · 46.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శక్రియత శర్రి సము సక్రియ ల లంకకు వె న్వ్న్సన్ జరచుచుజ్వనుయుశక్రా | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | తక్రియ సముక్రియ ల ల్య్య్దై మ్నపుసనుంజరచు జ్య్య్తక్రియత శర్రి సము సక్రియ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | లక్రి న్వ్న్సను జర్రు జ జు లశ్రియయ శర్రి సము స్ర్య్లల్యకు వె న్వ్నస్న్రరచు జ్వన్రో | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | చై క్రియయలల్లలల ల్య్య్జమ్రశశశున్రియ వ ల్య్య్సన్ర జ స నయ్రనునునువ్రీ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 32% · repeated lines 0 · mean token probability (geometric) 0.029 · model's first choice kept 41% · constraint overrode 52% · backtracks 0

<details><summary>Token probabilities (176 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.42 · `క` 0.01 · `్రి` 0.02✱ · `య` 0.17 · `త` 0.03 · `␣శ` 0.10 · `ర` 0.03 · `్రి` 1.1e-3✱ · `␣స` 0.08 · `ము` 0.28 · `␣స` 6.2e-3✱ · `క` 7.4e-3 · `్రి` 5.9e-3✱ · `య` 0.44 · `␣ల` 0.11 · `␣ల` 0.11 · `ంక` 0.18 · `కు` 0.16 · `␣వె` 0.17 · `␣న` 5.9e-4✱ · `్వ` 1.2e-3✱ · `్` 7.3e-4✱ · `న` 0.01✱ · `్` 4.5e-8✱ · `స` 6.1e-3✱ · `న్` 0.04✱ · `␣జ` 0.45 · `ర` 0.45 · `చు` 0.02✱ · `చు` 0.31 · `జ` 1.6e-3✱ · `్వ` 1.5e-4✱ · `ను` 0.88 · `యు` 3.5e-4✱ · `శ` 0.94 · `క` 0.97 · `్రా` 1.0e-4 · `⏎` 8.2e-5 forced |
| 2 | `త` 0.75 · `క` 8.5e-3✱ · `్రి` 0.28✱ · `య` 0.44 · `␣స` 0.39 · `ము` 0.79 · `క` 0.16✱ · `్రి` 0.02✱ · `య` 0.26✱ · `␣ల` 0.23 · `␣ల` 0.55 · `్య` 1.8e-3✱ · `్య` 3.9e-3✱ · `్` 7.2e-8✱ · `ద` 1.6e-3✱ · `ై` 8.5e-3✱ · `␣మ` 0.04 · `్` 0.24 · `న` 0.52 · `పు` 0.02✱ · `స` 0.60 · `ను` 8.1e-3✱ · `ంజ` 1.4e-3✱ · `ర` 0.91 · `చు` 0.95 · `␣జ` 0.79 · `్య` 9.2e-5✱ · `్య` 1.9e-4✱ · `్` 2.9e-5✱ · `త` 9.2e-3✱ · `క` 0.87 · `్రి` 0.27 · `య` 0.76 · `త` 0.50 · `␣శ` 0.48 · `ర` 0.62 · `్రి` 0.72 · `␣స` 0.61 · `ము` 0.86 · `␣స` 0.83 · `క` 0.93 · `్రి` 0.95 · `య` 0.93 · `్` 2.2e-5✱ · `⏎` 1.0e-3✱ forced |
| 3 | `ల` 0.10✱ · `క` 5.2e-3✱ · `్రి` 1.9e-5✱ · `␣న` 0.94 · `్వ` 0.58 · `్` 0.96 · `న` 0.93 · `్` 0.41 · `స` 0.89 · `ను` 5.1e-3✱ · `␣జ` 0.78 · `ర` 0.96 · `్రు` 5.3e-6✱ · `␣జ` 0.90 · `␣జ` 2.9e-3✱ · `ు` 0.02✱ · `␣ల` 0.03✱ · `శ` 0.95 · `్రి` 5.7e-4✱ · `య` 0.52 · `య` 0.79 · `␣శ` 0.37 · `ర` 0.27✱ · `్రి` 0.79 · `␣స` 0.57 · `ము` 0.67 · `␣స` 0.47 · `్ర` 4.4e-5✱ · `్య` 1.6e-3✱ · `్` 4.6e-5✱ · `ల` 0.19✱ · `ల` 0.02✱ · `్య` 1.3e-3✱ · `కు` 0.92 · `␣వె` 0.83 · `␣న` 0.74 · `్వ` 0.67 · `్` 0.84 · `న` 0.85 · `స` 0.55 · `్` 2.2e-5✱ · `న్` 0.71 · `ర` 0.55 · `ర` 0.54 · `చు` 0.83 · `␣జ` 0.71 · `్వ` 0.79 · `న` 2.2e-3✱ · `్రో` 1.6e-4✱ · `⏎` 0.05✱ forced |
| 4 | `చ` 9.3e-5✱ · `ై` 3.0e-3✱ · `␣` 3.1e-3✱ · `క` 1.2e-4✱ · `్రి` 0.03✱ · `య` 0.09✱ · `య` 0.02✱ · `ల` 0.02✱ · `ల్` 3.1e-3✱ · `ల` 0.05✱ · `ల` 0.04✱ · `ల` 0.18✱ · `␣ల` 0.04✱ · `్య` 0.02✱ · `్య` 0.12✱ · `్` 1.4e-3✱ · `జ` 9.5e-3✱ · `మ` 0.60 · `్ర` 3.3e-5✱ · `శ` 0.05✱ · `శ` 0.41 · `శ` 0.10✱ · `ు` 3.7e-3✱ · `న` 0.03✱ · `్రియ` 3.7e-4✱ · `␣వ` 0.07✱ · `␣ల` 5.3e-3✱ · `్య` 2.3e-3✱ · `్య` 3.1e-4✱ · `్` 1.5e-4✱ · `స` 0.12✱ · `న` 9.9e-3✱ · `్ర` 7.1e-6✱ · `␣జ` 0.80 · `␣స` 0.83 · `␣న` 0.71 · `య` 6.4e-4✱ · `్ర` 2.7e-6✱ · `ను` 6.9e-4✱ · `ను` 0.08✱ · `ను` 0.02✱ · `వ` 0.01✱ · `్రీ` 6.6e-4✱ |

</details>

[↑ meters](#meters)

---

<a id="layagrahi"></a>

## 36. లయగ్రాహి (layagrahi)

```text
Meter: లయగ్రాహి (layagrahi), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 10 gaṇas: భ జ స న భ జ స న భ య, i.e. UII IUI IIU III UII IUI IIU III UII IUU (30 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th and the 17th and the 25th akshara. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter లయగ్రాహి (layagrahi).

Meter: లయగ్రాహి (layagrahi), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 10 gaṇas: భ జ స న భ జ స న భ య, i.e. UII IUI IIU III UII IUI IIU III UII IUU (30 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 9th and the 17th and the 25th akshara. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 184 tokens · 45.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సిం శ జ శ దళ్ర శయ సైన్ సికత లంక శన దేన్ శమముసిం హ జ శ దళ్ శయ సలాన్ సిక్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | శేం శమన శమ్రముసి శజ్ శ జళ శయ్య శలవల్ శ జల శన్రలల శల్ సిమ శ జుద్ళ్రల్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | సిం శికత లంక శన దేన్ శమముసిల్య ల్య ల లల్ సికలు ఈతితితితిం సియ ఇయల్యల్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | విం శ శ సనన్రలల మత్ సులవ వల్య లయ గ్రాంథ్ శ ల శ్రనల్రునునుగాణ్ సవవణణ్ మల్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 15% · single-akshara words 49% · repeated lines 0 · mean token probability (geometric) 0.019 · model's first choice kept 29% · constraint overrode 61% · backtracks 0

<details><summary>Token probabilities (184 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `సి` 0.02 · `ం` 0.12 · `␣శ` 0.02 · `␣జ` 0.02 · `␣శ` 0.02 · `␣ద` 5.5e-3 · `ళ` 9.7e-3✱ · `్ర` 5.1e-4✱ · `␣శ` 0.05 · `య` 5.5e-3 · `␣స` 0.03 · `ై` 0.02✱ · `న్` 7.5e-3✱ · `␣స` 0.05✱ · `ిక` 3.2e-3 · `త` 9.7e-3 · `␣ల` 0.05 · `ంక` 0.09 · `␣శ` 0.03 · `న` 0.02 · `␣ద` 7.4e-3✱ · `ే` 0.12 · `న` 0.03✱ · `్` 4.8e-7✱ · `␣శ` 0.01✱ · `మ` 0.15 · `ము` 4.0e-4✱ · `సి` 0.95 · `ం` 0.97 · `␣హ` 0.95 · `␣జ` 0.95 · `␣శ` 0.93 · `␣ద` 0.94 · `ళ` 0.99 · `్` 7.6e-5✱ · `␣శ` 0.96 · `య` 0.98 · `␣స` 0.97 · `లా` 1.2e-4✱ · `న్` 0.87 · `␣స` 0.77 · `ిక` 0.55 · `్` 1.8e-4✱ · `⏎` 6.0e-4✱ forced |
| 2 | `శ` 9.7e-3✱ · `ే` 4.5e-3✱ · `ం` 6.0e-4✱ · `␣శ` 0.03✱ · `మ` 1.0e-3✱ · `న` 0.77 · `␣శ` 0.03✱ · `మ` 0.03✱ · `్ర` 1.5e-3✱ · `ము` 0.52 · `సి` 0.81 · `␣శ` 1.9e-3✱ · `జ` 0.03✱ · `్` 4.5e-5✱ · `␣శ` 0.48 · `␣జ` 0.12 · `ళ` 0.48 · `␣శ` 0.15✱ · `య` 0.03✱ · `్య` 4.2e-3✱ · `␣శ` 0.07 · `ల` 0.05✱ · `వ` 0.04✱ · `ల` 0.01✱ · `్` 8.4e-9✱ · `␣శ` 6.9e-3✱ · `␣జ` 0.85 · `ల` 0.93 · `␣శ` 0.56 · `న` 0.75 · `్ర` 1.6e-4✱ · `ల` 1.5e-3✱ · `ల` 0.65 · `␣శ` 0.77 · `ల` 0.87 · `్` 2.0e-5✱ · `␣సి` 0.02✱ · `మ` 1.3e-3✱ · `␣శ` 0.76 · `␣జ` 0.91 · `ు` 8.7e-3✱ · `ద్` 1.9e-4✱ · `ళ` 0.78 · `్ర` 0.82 · `ల` 5.9e-4✱ · `్` 6.2e-8✱ · `⏎` 3.0e-4✱ forced |
| 3 | `సి` 0.01✱ · `ం` 0.03✱ · `␣శ` 0.01✱ · `ిక` 0.99 · `త` 0.96 · `␣ల` 0.99 · `ంక` 0.98 · `␣శ` 0.98 · `న` 0.99 · `␣ద` 0.99 · `ే` 1.00 · `న` 0.97 · `్` 0.88 · `␣శ` 0.94 · `మ` 0.93 · `ము` 0.98 · `సి` 3.6e-3✱ · `ల` 3.6e-4✱ · `్య` 7.9e-4✱ · `␣` 0.01✱ · `ల` 2.9e-3✱ · `్య` 7.8e-3✱ · `␣` 0.04✱ · `ల` 0.19 · `␣` 0.19 · `ల` 7.5e-3✱ · `ల` 7.0e-3✱ · `్` 1.4e-4✱ · `␣` 1.7e-3✱ · `సి` 3.0e-4✱ · `క` 0.02✱ · `లు` 5.4e-4✱ · `␣ఈ` 0.02✱ · `తి` 2.7e-4✱ · `తి` 0.11✱ · `తి` 0.03✱ · `తి` 2.7e-3✱ · `ం` 2.4e-3✱ · `␣` 2.1e-3✱ · `సి` 6.8e-3✱ · `య` 0.05✱ · `␣ఇ` 9.0e-3✱ · `య` 0.22✱ · `ల` 5.3e-3✱ · `్య` 0.01✱ · `ల` 0.03✱ · `్` 7.2e-4✱ · `⏎` 0.22✱ forced |
| 4 | `వి` 6.9e-7✱ · `ం` 2.5e-5✱ · `␣` 8.0e-5✱ · `శ` 2.4e-4✱ · `␣శ` 0.02✱ · `␣స` 0.01✱ · `న` 0.02✱ · `న` 6.1e-3✱ · `్ర` 6.7e-3✱ · `ల` 0.07✱ · `ల` 0.28 · `␣మ` 0.28✱ · `త్` 0.04✱ · `␣సు` 7.3e-3✱ · `ల` 0.02✱ · `వ` 0.04✱ · `␣వ` 9.8e-3✱ · `ల` 0.21 · `్య` 4.2e-3✱ · `␣ల` 0.66 · `య` 0.94 · `␣గ్రా` 0.02✱ · `ంథ` 3.3e-5✱ · `్` 2.0e-3✱ · `␣శ` 0.01✱ · `␣ల` 0.15 · `␣శ` 0.10✱ · `్ర` 0.53 · `న` 0.04 · `ల` 0.11 · `్రు` 6.0e-3✱ · `ను` 1.4e-4✱ · `ను` 3.1e-3✱ · `గా` 0.02✱ · `ణ` 0.02✱ · `్` 1.9e-4✱ · `␣స` 6.6e-3✱ · `వ` 0.75 · `వ` 0.12✱ · `ణ` 0.02✱ · `ణ` 0.08✱ · `్` 4.1e-3✱ · `␣మ` 7.3e-3✱ · `ల` 0.04✱ · `్` 2.3e-3✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 170 tokens · 35.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మామలగె వే అను వ కక్ మయు ల లో లి మక మమ్రికమరంకిమ ధమస్రమల మమ్యం | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | క్యామన మ లౌ వ ప్ర నికల్య య మమత్రి మమ మిత్ మ మ మమమ్యకయనమ్ మ వ ప్ర నిక్య్యయ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | మౌమమమ మిత్ మమ మమమ్యహన మల్య వ ప్ర నిక్ మ య మమత్రి మమ మిత్ మమ ల లాయాయ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | వౌమితిమిమిమ్యమ మమమ్ మయయతాయ్ లయ వయయ్ మ మ్మ్డుదిదిగ్యమినదిస్ మతితితిమ్యున్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 48% · repeated lines 0 · mean token probability (geometric) 0.017 · model's first choice kept 35% · constraint overrode 51% · backtracks 0

<details><summary>Token probabilities (170 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.05 · `మ` 0.12 · `ల` 0.06 · `గ` 0.01 · `ె` 1.8e-3 · `␣వే` 4.4e-3 · `␣అను` 2.3e-3 · `␣వ` 2.8e-3 · `␣క` 0.01 · `క` 0.04✱ · `్` 5.0e-8✱ · `␣మ` 0.04✱ · `యు` 5.0e-3✱ · `␣ల` 0.12 · `␣లో` 0.10 · `␣` 8.5e-3✱ · `లి` 1.5e-3✱ · `␣మ` 0.04✱ · `క` 0.05✱ · `␣మ` 0.04 · `మ` 0.03✱ · `్రి` 6.1e-5✱ · `క` 0.04✱ · `మ` 0.15 · `రం` 8.5e-4 · `కి` 4.9e-4 · `మ` 0.09 · `␣ధ` 3.6e-3 · `మ` 0.07 · `స` 0.02✱ · `్రమ` 1.1e-5✱ · `ల` 0.02✱ · `␣మ` 0.01✱ · `మ` 0.19✱ · `్యం` 2.5e-4✱ · `⏎` 0.83 |
| 2 | `క` 0.14 · `్యా` 3.8e-5✱ · `మ` 0.01✱ · `న` 0.01 · `␣మ` 0.06 · `␣ల` 0.01 · `ౌ` 0.03✱ · `␣వ` 0.08 · `␣ప్ర` 2.2e-3 · `␣ని` 0.02 · `క` 0.03 · `ల` 1.6e-3✱ · `్య` 7.6e-4✱ · `␣య` 0.06 · `␣మ` 0.15 · `మ` 0.07 · `త` 0.05✱ · `్రి` 2.1e-4✱ · `␣మ` 0.60 · `మ` 0.34 · `␣మ` 0.73 · `ిత` 0.96 · `్` 2.3e-6✱ · `␣మ` 7.2e-4✱ · `␣మ` 0.39 · `␣మ` 0.41 · `మ` 0.51 · `మ` 6.7e-3✱ · `్య` 6.3e-6✱ · `క` 0.07 · `య` 0.76 · `న` 0.75 · `మ` 4.2e-3✱ · `్` 1.4e-8✱ · `␣మ` 7.7e-3✱ · `␣వ` 0.90 · `␣ప్ర` 0.98 · `␣ని` 0.94 · `క` 0.89 · `్య` 3.2e-7✱ · `్య` 0.94 · `య` 0.03✱ · `్` 2.7e-5✱ · `⏎` 2.9e-3✱ forced |
| 3 | `మ` 0.87 · `ౌ` 1.4e-5✱ · `మ` 1.4e-3✱ · `మ` 0.13 · `మ` 0.84 · `␣మ` 0.95 · `ిత` 0.93 · `్` 0.89 · `␣మ` 0.80 · `మ` 0.68 · `␣మ` 0.66 · `మ` 0.70 · `మ` 0.04✱ · `్య` 3.7e-4✱ · `హ` 0.55 · `న` 0.76 · `␣మ` 0.84 · `ల` 1.3e-3✱ · `్య` 1.8e-6✱ · `␣వ` 0.98 · `␣ప్ర` 0.95 · `␣ని` 0.98 · `క` 0.98 · `్` 2.4e-8✱ · `␣మ` 0.01✱ · `␣య` 0.58 · `␣మ` 0.90 · `మ` 0.88 · `త` 0.83 · `్రి` 0.83 · `␣మ` 0.94 · `మ` 0.91 · `␣మ` 0.95 · `ిత` 0.92 · `్` 0.36 · `␣మ` 0.90 · `మ` 0.91 · `␣ల` 1.9e-3✱ · `␣ల` 1.0e-3✱ · `ాయ` 1.6e-4✱ · `ాయ` 8.3e-4✱ · `్` 3.6e-6✱ · `⏎` 0.07✱ forced |
| 4 | `వ` 4.1e-3✱ · `ౌ` 4.1e-4✱ · `మి` 1.4e-3✱ · `తి` 3.6e-3✱ · `మి` 4.2e-3✱ · `మి` 0.11✱ · `మ` 9.0e-3✱ · `్య` 0.01✱ · `మ` 0.18 · `␣మ` 0.13 · `మ` 0.31 · `మ` 0.10 · `్` 1.6e-4✱ · `␣మ` 0.56 · `య` 0.97 · `య` 0.91 · `త` 9.6e-7✱ · `ాయ` 6.2e-3✱ · `్` 0.08✱ · `␣ల` 2.3e-3✱ · `య` 0.74 · `␣వ` 4.5e-4✱ · `య` 0.06✱ · `య` 7.4e-3✱ · `్` 0.01✱ · `␣మ` 9.4e-4✱ · `␣మ` 4.7e-3✱ · `్` 9.3e-4✱ · `మ్` 4.6e-4✱ · `డు` 1.9e-3✱ · `ది` 0.01✱ · `ది` 0.02✱ · `గ` 3.9e-3✱ · `్య` 0.03✱ · `మ` 1.3e-3✱ · `ిన` 9.9e-3✱ · `ది` 0.01✱ · `స్` 5.6e-3✱ · `␣మ` 7.4e-3✱ · `తి` 0.08✱ · `తి` 0.84 · `తి` 0.12✱ · `మ` 5.9e-4✱ · `్య` 3.1e-3✱ · `ు` 0.13✱ · `న` 0.02✱ · `్` 1.4e-3✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 184 tokens · 75.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పంబల లయన్రు అమృతధ్ బి ఉరుణణ్యవ మెరున్ బికశజమ్యబ జనుల్ బవచు నీతిక్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | ఔంబు మడచుడ్రియ జనత్ బపు దశావ మతృ నీత్ బను లసవ్రడచు నీమ్ బల మమక్రిం | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | మొం బకడవన్ ణిసవ మడ్ బలవతత్యలులులుణ్ బ గణ మార్డు ఇ ఇనన్ బ న భ జస్రయ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | దింబబు త లేదు వ వ వఃయ్ బితితితియ్యబునగాణ్ బితి లతిన్రయు ఇ యయ్ బి వతి మిత్ గవ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 37% · repeated lines 0 · mean token probability (geometric) 0.006 · model's first choice kept 29% · constraint overrode 64% · backtracks 30

<details><summary>Token probabilities (184 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.55 · `ంబ` 5.7e-4 · `ల` 0.92 · `␣ల` 3.8e-3 · `య` 0.99 · `న` 0.94 · `్రు` 2.4e-5✱ · `␣అమ` 0.01 · `ృత` 1.00 · `ధ` 0.96 · `్` 1.8e-9✱ · `␣` 8.1e-4✱ · `బి` 0.78 · `␣ఉ` 6.1e-4 · `రుణ` 0.02 · `ణ` 0.99 · `్య` 1.00 · `వ` 0.82 · `␣మె` 5.8e-3 · `రు` 0.99 · `న` 0.96 · `్` 6.4e-8✱ · `␣` 2.4e-3✱ · `బి` 3.3e-4✱ · `క` 1.3e-3✱ · `శ` 3.1e-3 · `జ` 0.07 · `మ` 0.05 · `్య` 8.7e-3✱ · `బ` 7.2e-3 · `␣జన` 2.3e-3 · `ుల` 0.90 · `్` 6.6e-9✱ · `␣బ` 2.4e-5✱ · `వ` 0.91 · `చు` 0.02 · `␣నీ` 0.92 · `తి` 0.95 · `క` 0.07✱ · `్` 1.8e-8✱ · `⏎` 1.5e-3✱ forced |
| 2 | `ఔ` 4.8e-3✱ · `ం` 2.3e-4✱ · `బు` 1.9e-4✱ · `␣మ` 0.96 · `డ` 0.99 · `చు` 0.99 · `డ` 1.6e-3✱ · `్రియ` 1.4e-4✱ · `␣` 2.0e-3✱ · `జ` 0.99 · `న` 0.98 · `త` 7.1e-4✱ · `్` 5.1e-6✱ · `␣` 1.0e-4✱ · `బ` 8.9e-4✱ · `పు` 0.89 · `␣ద` 0.99 · `శా` 6.0e-5✱ · `వ` 0.83 · `␣మ` 0.98 · `త` 0.99 · `ృ` 9.1e-3✱ · `␣నీ` 0.88 · `త` 1.3e-3✱ · `్` 6.7e-8✱ · `␣` 5.3e-4✱ · `బ` 1.6e-4✱ · `ను` 2.2e-3✱ · `␣` 0.89 · `ల` 7.7e-4✱ · `స` 0.99 · `వ` 0.93 · `్ర` 9.8e-5✱ · `డ` 1.00 · `చు` 0.99 · `␣నీ` 0.89 · `మ` 1.5e-3✱ · `్` 5.6e-6✱ · `␣` 7.4e-4✱ · `బ` 4.7e-4✱ · `ల` 0.22 · `␣మ` 4.0e-4✱ · `మ` 0.30 · `క` 0.83 · `్రి` 1.5e-5✱ · `ం` 2.7e-6✱ · `⏎` 0.04 forced |
| 3 | `మ` 0.96 · `ొ` 4.5e-5✱ · `ం` 1.8e-5✱ · `␣బ` 2.0e-6✱ · `క` 0.99 · `డ` 0.99 · `వ` 0.98 · `న్` 0.97 · `␣` 0.95 · `ణి` 2.2e-4✱ · `స` 0.99 · `వ` 0.98 · `␣మ` 0.99 · `డ` 0.99 · `్` 1.5e-9✱ · `␣` 3.7e-4✱ · `బ` 6.0e-6✱ · `ల` 0.02✱ · `వ` 0.02✱ · `త` 1.9e-3✱ · `త` 5.6e-3✱ · `్య` 2.2e-4✱ · `లు` 3.3e-3✱ · `లు` 5.0e-3✱ · `లు` 8.3e-3✱ · `ణ` 1.4e-4✱ · `్` 1.9e-3✱ · `␣` 0.02✱ · `బ` 1.1e-3✱ · `␣గ` 0.06✱ · `ణ` 0.11✱ · `␣మార్` 7.8e-5✱ · `డు` 2.9e-3✱ · `␣ఇ` 0.07✱ · `␣ఇ` 0.23✱ · `న` 0.01✱ · `న` 3.9e-3✱ · `్` 1.8e-5✱ · `␣` 3.6e-4✱ · `బ` 1.6e-3✱ · `␣న` 0.15✱ · `␣భ` 1.00 · `␣జ` 1.00 · `స` 2.9e-3✱ · `్ర` 8.4e-5✱ · `య` 8.4e-3✱ · `్` 2.0e-5✱ · `⏎` 4.5e-4✱ forced |
| 4 | `ది` 0.01✱ · `ంబ` 7.9e-7✱ · `బు` 3.4e-3✱ · `␣త` 0.03✱ · `␣లేదు` 0.30 · `␣వ` 0.02✱ · `␣వ` 0.10 · `␣వ` 0.04✱ · `ః` 6.1e-3✱ · `య` 5.3e-4✱ · `్` 5.2e-5✱ · `␣` 1.3e-3✱ · `బి` 1.5e-5✱ · `తి` 0.97 · `తి` 0.04✱ · `తి` 8.7e-3✱ · `య` 3.7e-3✱ · `్య` 2.0e-3✱ · `బ` 0.34 · `ు` 2.5e-4✱ · `న` 1.4e-3✱ · `గా` 0.01✱ · `ణ` 5.4e-3✱ · `్` 4.8e-4✱ · `␣` 3.0e-3✱ · `బి` 4.0e-4✱ · `తి` 6.1e-3✱ · `␣` 0.01✱ · `ల` 0.02✱ · `తి` 0.35 · `న` 0.05✱ · `్ర` 6.0e-6✱ · `య` 0.28✱ · `ు` 8.3e-3✱ · `␣ఇ` 0.03✱ · `␣య` 0.04 · `య` 1.1e-3✱ · `్` 6.8e-6✱ · `␣` 4.3e-4✱ · `బి` 3.3e-4✱ · `␣వ` 6.9e-4✱ · `తి` 9.0e-4✱ · `␣మ` 0.01✱ · `ిత` 7.5e-4✱ · `్` 0.02✱ · `␣గ` 1.6e-3✱ · `వ` 8.6e-3✱ · `్` 2.0e-3✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 171 tokens · 63.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జక్రి మమ అమ్రణ రసమ్య గలకమ్య మఖరమ్ క్రియలకుర్లుజకమమ్ క్రమశలన్రన్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | కక్రవవ మిత్రమమమజ్ క్రియ దినవ్రమనతమ్ క్రియల లోక మితరామ్ క్రి మ మమవ్యక్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | కక్రియ గలక్రమల తవ్ క్రమక కవ్రమనికత్వము అడిన్రిలయగగ్రహ వ వృత్తమ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | అక్రహణ పద్ధతినిలోర్ క్రత పినణ్య ప పతివ్ క్ర న భ జస్ర భ యమాజ్ క్రమురుమీమీ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 23% · repeated lines 0 · mean token probability (geometric) 0.011 · model's first choice kept 44% · constraint overrode 54% · backtracks 30

<details><summary>Token probabilities (171 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.97 · `క` 0.95 · `్రి` 0.73 · `␣మ` 0.88 · `మ` 0.89 · `␣అ` 0.21 · `మ` 0.20 · `్ర` 0.79 · `ణ` 0.90 · `␣ర` 0.60 · `స` 0.96 · `మ` 0.96 · `్య` 0.93 · `␣గ` 0.76 · `ల` 0.95 · `క` 0.91 · `మ` 0.97 · `్య` 0.98 · `␣మ` 0.97 · `ఖ` 0.70 · `ర` 0.92 · `మ` 0.91 · `్` 1.0e-5✱ · `␣` 6.7e-3✱ · `క` 2.6e-4✱ · `్రియ` 6.7e-4✱ · `లకు` 0.08 · `ర్లు` 5.2e-7✱ · `జ` 0.70 · `క` 0.65 · `మ` 0.06✱ · `మ` 0.07✱ · `్` 8.1e-8✱ · `␣క` 3.8e-3✱ · `్రమ` 5.0e-4✱ · `శ` 1.3e-4✱ · `ల` 0.25✱ · `న` 0.10 · `్ర` 4.2e-5✱ · `న` 0.07✱ · `్` 9.2e-6✱ · `⏎` 5.2e-4✱ forced |
| 2 | `క` 0.77 · `క` 1.6e-4✱ · `్ర` 1.2e-4✱ · `వ` 4.7e-3✱ · `వ` 0.61 · `␣మ` 0.96 · `ిత` 1.00 · `్ర` 9.0e-5✱ · `మ` 0.95 · `మ` 2.3e-3✱ · `మ` 0.02✱ · `జ` 0.64 · `్` 8.7e-7✱ · `␣` 0.05✱ · `క` 3.6e-4✱ · `్రియ` 2.6e-3✱ · `␣ద` 0.87 · `ిన` 1.5e-3✱ · `వ` 0.95 · `్ర` 1.9e-4✱ · `మ` 5.1e-4✱ · `న` 0.43 · `త` 0.99 · `మ` 0.01✱ · `్` 6.9e-4✱ · `␣` 3.6e-3✱ · `క` 0.39 · `్రియ` 4.8e-5✱ · `ల` 0.72 · `␣లో` 0.99 · `క` 0.98 · `␣మ` 0.90 · `ిత` 0.99 · `రా` 1.00 · `మ` 0.99 · `్` 1.1e-6✱ · `␣` 6.7e-3✱ · `క` 0.02✱ · `్రి` 2.2e-4✱ · `␣మ` 0.08✱ · `␣మ` 0.72 · `మ` 0.60 · `వ` 8.2e-4✱ · `్య` 1.1e-3✱ · `క` 1.9e-3✱ · `్` 2.7e-6✱ · `⏎` 1.7e-5✱ forced |
| 3 | `క` 0.01✱ · `క` 0.01✱ · `్రియ` 2.0e-4✱ · `␣గ` 0.92 · `ల` 0.96 · `క` 0.90 · `్రమ` 4.9e-7✱ · `ల` 0.03✱ · `␣త` 0.89 · `వ` 0.99 · `్` 8.5e-8✱ · `␣క్` 4.8e-6✱ · `ర` 3.3e-4✱ · `మ` 1.00 · `క` 1.1e-4✱ · `␣` 0.80 · `క` 2.5e-3✱ · `వ` 1.3e-3✱ · `్ర` 1.3e-5✱ · `మని` 0.99 · `క` 0.98 · `త్వ` 1.1e-3✱ · `ము` 0.01✱ · `␣అ` 0.96 · `డి` 0.87 · `న` 3.4e-3✱ · `్రి` 2.0e-7✱ · `ల` 0.62 · `య` 0.80 · `గ` 0.85 · `గ` 2.1e-4✱ · `్రహ` 1.9e-3✱ · `␣వ` 0.04✱ · `␣వ` 0.82 · `ృ` 0.91 · `త్త` 0.95 · `మ` 1.8e-4✱ · `్` 7.1e-8✱ · `⏎` 0.04✱ forced |
| 4 | `అ` 0.54 · `క` 2.1e-3✱ · `్రహ` 3.1e-5✱ · `ణ` 1.00 · `␣ప` 1.00 · `ద్ధ` 1.00 · `తి` 1.00 · `ని` 1.2e-5✱ · `లో` 3.1e-3✱ · `ర` 5.2e-3✱ · `్` 2.4e-9✱ · `␣` 2.3e-4✱ · `క` 3.1e-4✱ · `్ర` 1.6e-5✱ · `త` 0.02✱ · `␣ప` 1.2e-5✱ · `ిన` 0.63 · `ణ` 1.4e-5✱ · `్య` 1.5e-3✱ · `␣ప` 0.97 · `␣ప` 3.0e-5✱ · `తి` 0.99 · `వ` 8.9e-5✱ · `్` 2.0e-6✱ · `␣క్` 7.4e-5✱ · `ర` 9.9e-5✱ · `␣న` 0.62 · `␣భ` 0.98 · `␣జ` 0.97 · `స` 1.7e-3✱ · `్ర` 4.2e-5✱ · `␣భ` 0.99 · `␣య` 0.64 · `మా` 2.9e-7✱ · `జ` 1.9e-3✱ · `్` 7.1e-4✱ · `␣` 6.0e-3✱ · `క్` 3.7e-4✱ · `ర` 2.8e-5✱ · `ము` 0.07✱ · `రు` 0.02✱ · `మీ` 0.46 · `మీ` 0.47 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 158 tokens · 34.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మామలవ మక్రియ మమక్రి మ మతిశ్రమ మమమ్ర మమకమ్రమమలవ్ మమక మమ్యా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | మ్యా మమ మమమ్రి మమకన్ మన మమన్య మన మౌన మమనమ్యన మమక్యమమమమ్యా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | మ్యా మమ మమమ్రి మమకమ్ మమ మమమ్య మ మ మమ్యమమలమ్యమమమమ్యమమమమ్యా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | మ్రీ మమమ ఈతితితితింర్ మమమమమ్యమమమమ్ మమమితంబ్ గమమమమ్ మమమమమ్యా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.051 · model's first choice kept 41% · constraint overrode 48% · backtracks 0

<details><summary>Token probabilities (158 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.05 · `మ` 0.12 · `ల` 0.06 · `వ` 0.02 · `␣మ` 0.11 · `క` 0.04✱ · `్రియ` 1.7e-4✱ · `␣మ` 0.45 · `మ` 0.31 · `క` 0.06 · `్రి` 5.0e-4✱ · `␣మ` 0.53 · `␣మ` 0.14 · `తి` 0.02 · `శ` 0.04✱ · `్రమ` 2.3e-3✱ · `␣మ` 0.31 · `మ` 0.46 · `మ` 0.10 · `్ర` 2.5e-3✱ · `␣మ` 0.08✱ · `మ` 0.32 · `క` 0.05✱ · `మ` 0.08✱ · `్ర` 5.4e-4✱ · `మ` 0.17✱ · `మ` 0.29 · `ల` 0.34 · `వ` 0.32 · `్` 6.4e-6✱ · `␣మ` 0.33 · `మ` 0.24 · `క` 0.09 · `␣మ` 0.26 · `మ` 0.17 · `్యా` 1.1e-3 · `⏎` 0.02✱ forced |
| 2 | `మ` 0.79 · `్యా` 1.7e-4✱ · `␣మ` 0.08✱ · `మ` 0.47 · `␣మ` 0.10 · `మ` 0.17 · `మ` 0.43 · `్రి` 1.0e-3✱ · `␣మ` 0.02✱ · `మ` 0.19 · `క` 0.08✱ · `న` 0.51 · `్` 1.2e-7✱ · `␣మ` 0.07✱ · `న` 0.62 · `␣మ` 0.94 · `మ` 8.5e-3✱ · `న` 0.70 · `్య` 6.6e-5✱ · `␣మ` 0.03✱ · `న` 0.79 · `␣మ` 0.95 · `ౌ` 0.90 · `న` 0.92 · `␣మ` 0.98 · `మ` 8.4e-3✱ · `న` 0.88 · `మ` 5.8e-3✱ · `్య` 9.1e-4✱ · `న` 0.67 · `␣మ` 0.84 · `మ` 0.94 · `క` 0.24 · `్య` 1.5e-4✱ · `మ` 0.53 · `మ` 0.02✱ · `మ` 0.03✱ · `మ` 0.29✱ · `్యా` 0.03✱ · `⏎` 0.13✱ forced |
| 3 | `మ` 0.72 · `్యా` 0.02✱ · `␣మ` 0.79 · `మ` 0.92 · `␣మ` 0.52 · `మ` 0.70 · `మ` 0.67 · `్రి` 0.33✱ · `␣మ` 0.57 · `మ` 0.63 · `క` 0.47 · `మ` 0.38 · `్` 0.02✱ · `␣మ` 0.91 · `మ` 0.60 · `␣మ` 0.51 · `మ` 0.81 · `మ` 0.26 · `్య` 0.10✱ · `␣మ` 0.69 · `␣మ` 0.15 · `␣మ` 0.64 · `మ` 0.35 · `్య` 0.01✱ · `మ` 0.43 · `మ` 0.69 · `ల` 0.02 · `మ` 0.69 · `్య` 3.0e-4✱ · `మ` 0.58 · `మ` 0.91 · `మ` 0.90 · `మ` 0.87 · `్య` 2.7e-4✱ · `మ` 0.88 · `మ` 0.08✱ · `మ` 0.03✱ · `మ` 7.4e-3✱ · `్యా` 0.02✱ · `⏎` 0.81 |
| 4 | `మ` 6.2e-3✱ · `్రీ` 3.3e-4✱ · `␣మ` 3.5e-4✱ · `మ` 0.01✱ · `మ` 0.05✱ · `␣ఈ` 0.02✱ · `తి` 1.2e-3✱ · `తి` 3.8e-3✱ · `తి` 0.05✱ · `తి` 5.6e-3✱ · `ం` 4.6e-3✱ · `ర్` 4.7e-3✱ · `␣మ` 1.8e-3✱ · `మ` 0.59 · `మ` 0.84 · `మ` 0.40 · `మ` 0.52 · `్య` 5.0e-3✱ · `మ` 0.68 · `మ` 0.89 · `మ` 0.45 · `మ` 0.03✱ · `్` 1.3e-6✱ · `␣మ` 8.4e-3✱ · `మ` 0.03✱ · `మ` 0.03✱ · `ిత` 0.17 · `ంబ` 1.7e-4✱ · `్` 7.0e-3✱ · `␣గ` 2.4e-3✱ · `మ` 0.08✱ · `మ` 0.05✱ · `మ` 0.09✱ · `మ` 0.11✱ · `్` 3.0e-5✱ · `␣మ` 0.01✱ · `మ` 0.22✱ · `మ` 7.9e-3✱ · `మ` 0.01✱ · `మ` 0.05✱ · `్యా` 5.7e-3✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 176 tokens · 44.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | ప్రియ్రు మ మగక్రి మమతక్ య్రుణము మాతృ మము ప్రేమ మ మమక్రియతముమ్ య్రుత మనస్రో | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | మాయ్రు మ మమమ్య మ మ మమ్య మకమక్యము న మయ్రితకకమ్య మతిముమ్ య్రుత మనమ్యం | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | కాయ్రు మత లోకము య మౌత్ య్రుమకనుల్య మతిముక్ య్రము మతిత్యము ట్టిగాగ స వరుద్దా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | వియ్రతితితిత్రు ఋయ యమ్ య్రిగి ము రీడుకు మరేన్ య్రి మలగీహిది వయర్ య్రడుడుతోతో | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 26% · repeated lines 0 · mean token probability (geometric) 0.009 · model's first choice kept 32% · constraint overrode 60% · backtracks 0

<details><summary>Token probabilities (176 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.04 · `్రియ` 0.17 · `్రు` 7.6e-6✱ · `␣మ` 0.33 · `␣మ` 0.20 · `గ` 0.02 · `క` 0.06✱ · `్రి` 8.8e-4✱ · `␣మ` 0.17 · `మ` 0.27 · `త` 0.40 · `క` 0.06✱ · `్` 5.1e-9✱ · `␣య` 2.1e-3✱ · `్` 1.1e-4✱ · `రుణ` 1.1e-4✱ · `ము` 0.29 · `␣మ` 0.11 · `ాత` 0.05 · `ృ` 0.08 · `␣మ` 0.04 · `ము` 0.25 · `␣` 1.4e-3✱ · `ప్ర` 0.94 · `ే` 0.98 · `మ` 0.99 · `␣మ` 0.39 · `␣మ` 0.18 · `మ` 0.07 · `క` 0.06 · `్రియ` 1.7e-3✱ · `త` 0.02✱ · `ము` 0.06✱ · `మ` 0.01✱ · `్` 1.2e-5✱ · `␣` 8.4e-3✱ · `య` 5.5e-4✱ · `్రు` 3.3e-4✱ · `త` 0.08 · `␣మ` 0.04 · `న` 0.02✱ · `స` 0.05✱ · `్రో` 7.5e-4✱ · `⏎` 0.27 |
| 2 | `మ` 0.17 · `ాయ` 0.02✱ · `్రు` 1.5e-3✱ · `␣మ` 0.57 · `␣మ` 0.34 · `మ` 0.12 · `మ` 0.08 · `్య` 1.3e-3✱ · `␣మ` 0.26 · `␣మ` 0.36 · `␣మ` 0.11 · `మ` 0.08 · `్య` 0.02✱ · `␣మ` 0.13 · `క` 0.27 · `మ` 0.14 · `క` 6.5e-3✱ · `్య` 2.8e-3✱ · `ము` 0.83 · `␣` 3.1e-4✱ · `న` 0.56 · `␣మ` 0.03✱ · `య` 0.36 · `్రి` 2.5e-4✱ · `త` 0.95 · `క` 1.5e-3✱ · `క` 0.60 · `మ` 0.10✱ · `్య` 1.6e-3✱ · `␣మ` 0.73 · `తి` 0.82 · `ము` 0.32 · `మ` 0.03✱ · `్` 6.9e-5✱ · `␣` 0.02✱ · `య` 1.2e-3✱ · `్రు` 0.03✱ · `త` 0.47 · `␣మ` 0.25 · `న` 0.22✱ · `మ` 0.53 · `్యం` 2.8e-4✱ · `⏎` 0.92 |
| 3 | `క` 0.94 · `ాయ` 1.4e-3✱ · `్రు` 6.1e-4✱ · `␣మ` 0.99 · `త` 0.83 · `␣లో` 1.00 · `క` 0.98 · `ము` 0.82 · `␣య` 0.28 · `␣మ` 0.73 · `ౌ` 0.87 · `త` 0.62 · `్` 4.5e-6✱ · `␣` 6.4e-4✱ · `య` 5.0e-4✱ · `్రు` 0.24 · `మ` 0.36 · `క` 5.4e-3✱ · `ను` 0.99 · `ల` 1.2e-3✱ · `్య` 1.5e-3✱ · `␣మ` 0.99 · `తి` 0.87 · `ము` 0.80 · `క` 0.01✱ · `్` 8.7e-9✱ · `␣య` 4.6e-4✱ · `్` 3.1e-4✱ · `ర` 8.7e-6✱ · `ము` 0.06✱ · `␣మ` 0.02✱ · `తి` 8.5e-3✱ · `త` 2.1e-4✱ · `్య` 7.5e-5✱ · `ము` 3.9e-3✱ · `␣` 1.4e-4✱ · `ట్టి` 2.2e-5✱ · `గా` 2.4e-3✱ · `గ` 3.9e-3✱ · `␣స` 3.2e-3✱ · `␣వరు` 2.2e-3✱ · `ద్దా` 4.5e-3✱ · `⏎` 0.03✱ forced |
| 4 | `వి` 8.9e-4✱ · `య` 1.0e-3✱ · `్ర` 3.3e-5✱ · `తి` 0.02✱ · `తి` 5.6e-3✱ · `తి` 0.02✱ · `త్ర` 2.0e-3✱ · `ు` 0.06✱ · `␣` 0.02✱ · `ఋ` 0.03✱ · `య` 0.11✱ · `␣య` 0.10 · `మ` 0.06 · `్` 1.7e-6✱ · `␣` 1.4e-6✱ · `య` 5.1e-6✱ · `్` 2.1e-5✱ · `రిగి` 3.2e-6✱ · `␣ము` 0.02✱ · `␣రీ` 0.06✱ · `డు` 9.2e-4✱ · `కు` 2.3e-3✱ · `␣మ` 0.08✱ · `రే` 0.06 · `న` 4.7e-3✱ · `్` 6.9e-10✱ · `␣` 2.7e-5✱ · `య` 2.2e-7✱ · `్రి` 1.8e-3✱ · `␣మ` 4.9e-5✱ · `ల` 0.12✱ · `గ` 0.32 · `ీ` 0.05✱ · `హి` 0.69 · `ది` 6.3e-4✱ · `␣వ` 7.1e-3✱ · `య` 0.09✱ · `ర` 0.12 · `్` 2.1e-8✱ · `␣` 9.8e-5✱ · `య` 2.3e-5✱ · `్ర` 6.0e-3✱ · `డు` 5.5e-4✱ · `డు` 4.3e-4✱ · `తో` 2.6e-4✱ · `తో` 2.7e-3✱ |

</details>

[↑ meters](#meters)

---

<a id="layavibhati"></a>

## 37. లయవిభాతి (layavibhati)

```text
Meter: లయవిభాతి (layavibhati), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 12 gaṇas: న స న న స న న స న న స గురువు, i.e. III IIU III III IIU III III IIU III III IIU U (34 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 10th and the 19th and the 28th akshara. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
```

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

*system*

```text
You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow chandassu exactly: the gaṇa sequence of every line, yati and prāsa.
```

*user*

```text
Write a Telugu padyam in the meter లయవిభాతి (layavibhati).

Meter: లయవిభాతి (layavibhati), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 12 gaṇas: న స న న స న న స న న స గురువు, i.e. III IIU III III IIU III III IIU III III IIU U (34 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 10th and the 19th and the 28th akshara. Prāsa-yati may take the place of yati.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong (ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). Every other akshara is laghu.

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 158 tokens · 32.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మసమ సిమమున్ పతిట నిశచన జ ఎత్తకిడునుసమసనమంక పవరిసెనునమసమ్రిమ్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 2 | మసక వససన్రియ మపు సము మన జన్రి జసను సమసనమమ్రమసమరమసమమస్రిమ్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 3 | మస నిసన మమ్రియ మడస సమసనమ్రమక మమససమజన్రుమసను సమసనమధ్వన్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 4 | మసమమమ మమ్య బలము సినిదిదినిమ్దిదిదిదిసలయవిభాతితితితిశిమనిదితిక్కడ్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 15% · single-akshara words 4% · repeated lines 0 · mean token probability (geometric) 0.043 · model's first choice kept 44% · constraint overrode 38% · backtracks 0

<details><summary>Token probabilities (158 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.36 · `స` 0.01 · `మ` 0.03 · `␣సి` 2.7e-3 · `మ` 0.04 · `ము` 0.05 · `న్` 0.10✱ · `␣ప` 0.02✱ · `తి` 0.12 · `ట` 0.02 · `␣ని` 0.01 · `శ` 0.09✱ · `చ` 0.33 · `న` 0.01 · `␣జ` 0.09 · `␣ఎ` 6.2e-4 · `త్త` 6.9e-3✱ · `కి` 0.01 · `డు` 0.02 · `ను` 0.08✱ · `స` 5.9e-4✱ · `మ` 0.39 · `స` 0.30 · `న` 0.04 · `మ` 0.12 · `ంక` 0.13✱ · `␣ప` 2.6e-3 · `వ` 1.4e-3 · `రి` 9.4e-3 · `సె` 0.02✱ · `ను` 0.69 · `న` 2.6e-3✱ · `మ` 0.85 · `స` 0.75 · `మ` 0.49 · `్రి` 1.3e-4✱ · `మ` 0.21 · `్` 2.4e-6✱ · `⏎` 0.28 forced |
| 2 | `మ` 0.35 · `స` 0.23 · `క` 0.02 · `␣వ` 0.01 · `స` 0.02 · `స` 0.02 · `న` 0.03✱ · `్రియ` 5.1e-5✱ · `␣మ` 0.14 · `పు` 3.9e-3 · `␣స` 0.02✱ · `ము` 0.18 · `␣మ` 0.03 · `న` 0.02 · `␣జ` 0.04 · `న` 0.03✱ · `్రి` 8.6e-4✱ · `␣జ` 0.04 · `స` 0.04 · `ను` 0.70 · `␣స` 0.06 · `మ` 0.35 · `స` 0.40 · `న` 0.33 · `మ` 0.37 · `మ` 0.08 · `్ర` 4.8e-4✱ · `మ` 0.26 · `స` 0.62 · `మ` 0.30 · `ర` 0.81 · `మ` 0.17 · `స` 0.07✱ · `మ` 0.19✱ · `మ` 0.42 · `స` 0.21✱ · `్రి` 7.5e-4✱ · `మ` 0.41 · `్` 9.3e-3✱ · `⏎` 0.47 |
| 3 | `మ` 0.20 · `స` 0.28 · `␣ని` 0.24 · `స` 0.20 · `న` 0.26 · `␣మ` 0.15 · `మ` 0.35 · `్రియ` 3.8e-5✱ · `␣మ` 0.81 · `డ` 0.96 · `స` 1.6e-3✱ · `␣స` 0.73 · `మ` 0.83 · `స` 0.86 · `న` 0.74 · `మ` 0.60 · `్రమ` 4.1e-5✱ · `క` 0.95 · `␣మ` 0.23✱ · `మ` 0.37 · `స` 0.19 · `స` 0.28 · `మ` 0.24 · `జ` 0.54 · `న` 0.15✱ · `్రు` 2.3e-4✱ · `మ` 0.56 · `స` 0.93 · `ను` 0.95 · `␣స` 0.68 · `మ` 0.84 · `స` 0.87 · `న` 0.71 · `మ` 0.73 · `ధ` 0.29 · `్వ` 0.04✱ · `న` 0.14✱ · `్` 1.8e-7✱ · `⏎` 6.1e-4✱ forced |
| 4 | `మ` 0.56 · `స` 0.57 · `మ` 0.33 · `మ` 0.10✱ · `మ` 0.68 · `␣` 0.36✱ · `మ` 4.8e-3✱ · `మ` 0.16 · `్య` 4.5e-4✱ · `␣` 0.62 · `బ` 2.2e-4✱ · `ల` 0.06✱ · `ము` 0.07✱ · `␣` 2.2e-3✱ · `సి` 9.8e-5✱ · `ని` 6.2e-3✱ · `ది` 0.07✱ · `ది` 0.04✱ · `ని` 6.5e-3✱ · `మ` 9.3e-3✱ · `్` 3.0e-3✱ · `ది` 1.2e-3✱ · `ది` 0.22✱ · `ది` 0.06✱ · `ది` 0.26 · `స` 9.7e-4✱ · `ల` 0.60 · `య` 0.61 · `వి` 0.57 · `భా` 0.42 · `తి` 0.74 · `తి` 0.06✱ · `తి` 0.02✱ · `తి` 5.4e-3✱ · `శి` 1.3e-3✱ · `మని` 5.9e-3✱ · `ది` 5.0e-3✱ · `తి` 3.3e-3✱ · `క్కడ` 2.9e-3✱ · `్` 2.2e-7✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 155 tokens · 28.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జకరతురనువ్రికయు పకవమవు మొల్లమమును కెతి మతరాపు దిరు సడును లకనల్యా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 2 | జకకితకతజ్వము పకకమగను తర్వరమగు కొనితి మతర్రి దిరు సకనలల గమ్రిన్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 3 | ల్య కుతి ఇవి కల్యము జగ కు గమనికక్కడరు అడిగిన లలయ్రితితితి కమున ఇదిమ్యశ్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 4 | ఇక ససమ వవ్రి వృవిలకమునబటిత్రిన లనక న న స నల్ల స న న్ర కు మ గణముల్రం | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 24% · repeated lines 0 · mean token probability (geometric) 0.009 · model's first choice kept 28% · constraint overrode 48% · backtracks 0

<details><summary>Token probabilities (155 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.08 · `క` 0.02 · `ర` 0.03 · `తు` 0.01 · `ర` 0.02 · `ను` 0.04 · `వ` 5.7e-3✱ · `్రి` 4.4e-4✱ · `క` 7.4e-3✱ · `యు` 5.5e-3 · `␣ప` 6.1e-3 · `క` 8.1e-3✱ · `వ` 0.05 · `మ` 0.07 · `వు` 1.1e-3 · `␣మొ` 2.7e-4 · `ల్ల` 0.08 · `మ` 0.05 · `ము` 0.07 · `ను` 0.03 · `␣కె` 2.3e-4✱ · `తి` 0.02 · `␣` 4.0e-3✱ · `మ` 0.22✱ · `త` 0.02 · `రా` 0.02 · `పు` 0.02 · `␣ది` 2.0e-3✱ · `రు` 7.1e-3 · `␣స` 6.7e-3 · `డు` 6.1e-3 · `ను` 0.06 · `␣ల` 0.02 · `క` 0.03✱ · `న` 0.09 · `ల` 0.02✱ · `్యా` 7.8e-4✱ · `⏎` 0.05 forced |
| 2 | `జ` 0.14 · `క` 0.20 · `క` 0.05 · `ిత` 3.3e-3 · `క` 0.03 · `త` 7.2e-3 · `జ` 0.01 · `్వ` 1.7e-3✱ · `ము` 0.21 · `␣ప` 0.06 · `క` 0.11 · `క` 0.10✱ · `మ` 0.26 · `గ` 0.03 · `ను` 0.07 · `␣తర` 2.6e-3✱ · `్వర` 2.3e-5✱ · `మ` 0.41 · `గు` 0.04 · `␣` 1.9e-4✱ · `కొని` 6.4e-4✱ · `తి` 0.21 · `␣మ` 0.46 · `త` 0.61 · `ర` 9.6e-3✱ · `్రి` 3.5e-5✱ · `␣ది` 0.33 · `రు` 0.81 · `␣స` 0.08✱ · `క` 0.44 · `న` 0.06 · `ల` 0.47 · `ల` 9.9e-4✱ · `␣గ` 0.83 · `మ` 1.4e-3✱ · `్ర` 1.8e-3✱ · `ిన` 1.00 · `్` 8.4e-7✱ · `⏎` 0.02✱ forced |
| 3 | `ల` 0.70 · `్య` 8.5e-6✱ · `␣` 9.0e-6✱ · `కు` 6.6e-6✱ · `తి` 0.99 · `␣ఇ` 0.98 · `వి` 3.7e-5✱ · `␣కల` 1.4e-3✱ · `్య` 2.6e-5✱ · `ము` 0.27✱ · `␣జగ` 0.02✱ · `␣` 1.9e-3✱ · `కు` 4.3e-11✱ · `␣` 1.0e-4✱ · `గ` 0.87 · `మని` 1.00 · `క` 0.99 · `క్కడ` 5.9e-5✱ · `రు` 6.5e-5✱ · `␣అ` 1.00 · `డి` 0.99 · `గిన` 0.95 · `␣ల` 1.0e-3✱ · `ల` 0.96 · `య` 1.00 · `్రి` 5.6e-8✱ · `తి` 9.6e-4✱ · `తి` 1.00 · `తి` 6.0e-3✱ · `␣` 1.9e-3✱ · `క` 3.0e-5✱ · `ము` 0.16✱ · `న` 5.8e-4✱ · `␣ఇది` 0.01✱ · `మ` 4.6e-4✱ · `్య` 4.9e-5✱ · `శ` 0.99 · `్` 2.8e-8✱ · `⏎` 6.1e-6✱ forced |
| 4 | `ఇ` 0.03✱ · `క` 4.5e-3✱ · `␣స` 0.15 · `స` 0.91 · `మ` 0.92 · `␣వ` 9.5e-3✱ · `వ` 0.78 · `్రి` 6.8e-4✱ · `␣వ` 0.98 · `ృ` 0.90 · `వి` 3.6e-4✱ · `ల` 5.7e-4✱ · `క` 3.3e-3✱ · `ము` 0.01✱ · `న` 4.8e-4✱ · `బ` 0.99 · `టి` 8.4e-5✱ · `త` 2.0e-6✱ · `్ర` 5.1e-6✱ · `ిన` 0.07✱ · `␣ల` 1.7e-3✱ · `న` 0.77 · `క` 2.1e-4✱ · `␣న` 0.60 · `␣న` 0.86 · `␣స` 0.85 · `␣న` 0.87 · `ల్ల` 5.8e-4✱ · `␣స` 0.94 · `␣న` 0.95 · `␣న` 0.92 · `్ర` 7.5e-5✱ · `␣` 1.1e-3✱ · `కు` 1.9e-5✱ · `␣మ` 0.02✱ · `␣గణ` 1.00 · `ముల` 1.3e-4✱ · `్ర` 1.4e-6✱ · `ం` 8.3e-3✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 158 tokens · 59.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జకలతురనుప్రి వయు ప్య్యు కొల మ అమయ్ మదిగ ధికరము దిశించుచు బమ కులనన జ్వడ్యుట్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 2 | ముకమును అతిగ్రిడును సుకము ధతి మధ్వరవవ క హొ పిన గడ్రిపని మ కవి తి ఇకధ్యం | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 3 | దు కకగమనిక్రిరు అడికరులయవిభ్రతి గతి కళము ఛపద్యశమయుక మయుఛతమ్రిక్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 4 | అ కనిపియగాక మనరు కిన నన సన్ర స న న స న న స గుక్కువ అని కుల క్రమ ఒక్రియ్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 30% · repeated lines 0 · mean token probability (geometric) 0.011 · model's first choice kept 49% · constraint overrode 49% · backtracks 30

<details><summary>Token probabilities (158 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.96 · `క` 0.93 · `ల` 5.8e-3 · `తు` 0.61 · `ర` 0.42 · `ను` 0.83 · `ప` 0.74 · `్రి` 0.88 · `␣వ` 0.96 · `యు` 0.91 · `␣ప` 0.92 · `్య` 5.5e-6✱ · `్య` 3.1e-4✱ · `ు` 0.87 · `␣కొ` 5.1e-6✱ · `ల` 0.11✱ · `␣మ` 0.92 · `␣అమ` 5.8e-4 · `య` 0.99 · `్` 3.6e-4✱ · `␣మ` 0.73 · `ది` 0.90 · `గ` 0.80 · `␣ధ` 1.00 · `ి` 1.1e-4✱ · `కర` 1.6e-5✱ · `ము` 0.99 · `␣ది` 1.00 · `శ` 1.00 · `ించు` 1.00 · `చు` 1.00 · `␣` 0.96 · `బ` 1.8e-5✱ · `మ` 0.98 · `␣` 0.20 · `కుల` 6.7e-8✱ · `న` 5.6e-5✱ · `న` 0.90 · `␣జ` 1.00 · `్వ` 0.99 · `డ` 1.00 · `్య` 1.00 · `ు` 1.00 · `ట` 0.99 · `్` 8.6e-10✱ · `⏎` 9.6e-6✱ forced |
| 2 | `ము` 0.67 · `క` 9.7e-4✱ · `ము` 0.98 · `ను` 0.97 · `␣అతి` 9.6e-5✱ · `గ` 0.99 · `్రి` 3.4e-5✱ · `డు` 0.95 · `ను` 0.94 · `␣సు` 2.8e-5✱ · `క` 4.3e-6✱ · `ము` 0.96 · `␣ధ` 2.1e-5✱ · `తి` 1.00 · `␣మ` 1.00 · `ధ` 5.8e-5✱ · `్వర` 6.1e-6✱ · `వ` 0.98 · `వ` 3.3e-4✱ · `␣` 1.1e-3✱ · `క` 5.9e-4✱ · `␣హ` 6.4e-3✱ · `ొ` 0.05✱ · `␣ప` 0.91 · `ిన` 3.4e-4✱ · `␣గ` 0.96 · `డ` 2.0e-4✱ · `్రి` 1.1e-6✱ · `ప` 1.1e-3✱ · `ని` 9.3e-5✱ · `␣మ` 1.8e-4✱ · `␣` 2.7e-4✱ · `క` 1.0e-6✱ · `వి` 0.99 · `␣` 1.6e-3✱ · `తి` 0.88 · `␣ఇ` 0.98 · `క` 3.8e-3✱ · `ధ్య` 4.5e-6✱ · `ం` 0.03✱ · `⏎` 0.03✱ forced |
| 3 | `దు` 8.4e-3✱ · `␣` 5.4e-3✱ · `క` 4.4e-5✱ · `క` 0.02✱ · `గ` 0.93 · `మని` 0.99 · `క` 0.99 · `్రి` 4.9e-7✱ · `రు` 2.4e-3✱ · `␣అ` 0.99 · `డి` 0.98 · `క` 8.2e-6✱ · `రు` 2.1e-3✱ · `ల` 0.72 · `య` 0.88 · `వి` 0.93 · `భ` 3.7e-3✱ · `్ర` 1.0e-5✱ · `తి` 0.70 · `␣గ` 0.78 · `తి` 0.98 · `␣కళ` 2.0e-5✱ · `ము` 0.14✱ · `␣ఛ` 4.8e-5✱ · `ప` 0.75 · `ద్య` 0.96 · `శ` 0.97 · `మ` 1.1e-5✱ · `యు` 9.1e-3✱ · `క` 2.8e-3✱ · `␣మ` 1.3e-3✱ · `యు` 0.37 · `ఛ` 0.55 · `త` 0.28 · `మ` 0.07✱ · `్రి` 1.4e-7✱ · `క` 2.2e-5✱ · `్` 8.4e-10✱ · `⏎` 4.1e-5✱ forced |
| 4 | `అ` 3.5e-3✱ · `␣కని` 0.96 · `పి` 0.97 · `య` 3.2e-5✱ · `గా` 0.12✱ · `క` 8.3e-4✱ · `␣మన` 1.2e-3✱ · `రు` 0.02✱ · `␣కి` 9.7e-5✱ · `న` 0.01✱ · `␣న` 3.0e-3✱ · `న` 0.71 · `␣స` 0.86 · `న` 5.1e-3✱ · `్ర` 1.2e-4✱ · `␣స` 0.93 · `␣న` 0.84 · `␣న` 0.94 · `␣స` 0.96 · `␣న` 0.94 · `␣న` 0.90 · `␣స` 0.95 · `␣గు` 0.97 · `క్కువ` 1.3e-5✱ · `␣అని` 4.5e-3✱ · `␣` 8.8e-7✱ · `కుల` 6.5e-5✱ · `␣క్ర` 1.00 · `మ` 1.4e-4✱ · `␣ఒక` 0.93 · `్రియ` 2.7e-6✱ · `్` 8.2e-9✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 159 tokens · 69.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | నరతు నమసన్య మశమర శశల లేత లయవురతి తరచుగ్యకు లయరతి మనిసస్రవ్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 2 | రర నమసనయ్యశమర శశల మతల్ లవురతిరచుగగకుల్యరతి మరిసససవవ్రీ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 3 | తురమసనయల్యమర శరల మత లయ్యరతి తరచుగ లకుల్యరతి మరిసససవత్ నన్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 4 | మరనశమరశ్రల మత ఱయరతి తర్రుగ లకు ఱరతి మనిస్రసవతరుడుచిన గందిక్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 3% · repeated lines 0 · mean token probability (geometric) 0.067 · model's first choice kept 58% · constraint overrode 32% · backtracks 30

<details><summary>Token probabilities (159 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `న` 0.71 · `ర` 0.03 · `తు` 4.5e-4 · `␣న` 0.49 · `మ` 0.72 · `స` 0.53 · `న` 0.60 · `్య` 6.0e-5✱ · `␣మ` 0.06 · `శ` 0.01 · `మ` 0.12 · `ర` 0.98 · `␣శ` 0.96 · `శ` 0.01 · `ల` 0.25 · `␣లే` 1.9e-3✱ · `త` 0.03 · `␣ల` 0.78 · `య` 0.73 · `వు` 1.3e-3 · `ర` 0.97 · `తి` 0.99 · `␣తర` 0.69 · `చు` 0.99 · `గ` 0.95 · `్య` 1.1e-4✱ · `కు` 2.2e-3 · `␣ల` 0.21 · `య` 0.15 · `ర` 0.86 · `తి` 0.96 · `␣మ` 0.95 · `ని` 0.91 · `స` 0.81 · `స` 0.85 · `్ర` 0.69 · `వ` 0.11✱ · `్` 1.6e-6✱ · `⏎` 0.02✱ forced |
| 2 | `ర` 0.95 · `ర` 0.02✱ · `␣న` 0.83 · `మ` 0.86 · `స` 0.60 · `న` 2.5e-3✱ · `య` 0.21✱ · `్య` 2.5e-4✱ · `శ` 0.38 · `మ` 0.88 · `ర` 0.88 · `␣శ` 0.78 · `శ` 0.93 · `ల` 0.90 · `␣మ` 2.7e-3✱ · `త` 0.71 · `ల్` 4.4e-3✱ · `␣ల` 0.43 · `వు` 0.30 · `ర` 0.96 · `తి` 0.97 · `ర` 9.0e-3✱ · `చు` 0.97 · `గ` 0.94 · `గ` 6.6e-4✱ · `కు` 0.78 · `ల` 0.02✱ · `్య` 8.6e-4✱ · `ర` 0.67 · `తి` 0.93 · `␣మ` 0.86 · `రి` 2.0e-4✱ · `స` 0.82 · `స` 0.93 · `స` 0.06✱ · `వ` 0.73 · `వ` 4.0e-3✱ · `్రీ` 1.3e-4✱ · `⏎` 0.02 forced |
| 3 | `తు` 0.58 · `ర` 0.02✱ · `మ` 0.82 · `స` 0.62 · `న` 0.45 · `య` 0.34 · `ల` 0.01✱ · `్య` 4.4e-3✱ · `మ` 0.26 · `ర` 0.25 · `␣శ` 0.23 · `ర` 0.01✱ · `ల` 0.42 · `␣మ` 0.05✱ · `త` 0.66 · `␣ల` 0.11✱ · `య` 0.11✱ · `్య` 1.7e-3✱ · `ర` 0.65 · `తి` 0.69 · `␣తర` 0.30 · `చు` 0.87 · `గ` 0.70 · `␣ల` 0.01✱ · `కు` 0.71 · `ల` 0.09✱ · `్య` 0.05✱ · `ర` 0.90 · `తి` 0.95 · `␣మ` 0.83 · `రి` 0.05✱ · `స` 0.91 · `స` 0.87 · `స` 0.74 · `వ` 0.81 · `త్` 0.53 · `␣` 1.3e-4✱ · `న` 0.41 · `న` 0.34 · `్` 5.6e-8✱ · `⏎` 4.7e-4✱ forced |
| 4 | `మ` 0.19 · `ర` 0.33 · `న` 0.54 · `శ` 0.53 · `మ` 0.86 · `ర` 0.88 · `శ` 0.05✱ · `్ర` 7.3e-4✱ · `ల` 0.98 · `␣మ` 7.2e-3✱ · `త` 0.98 · `␣` 7.1e-4✱ · `ఱ` 2.7e-5✱ · `య` 0.93 · `ర` 0.98 · `తి` 0.99 · `␣తర` 1.00 · `్రు` 3.3e-9✱ · `గ` 0.99 · `␣ల` 2.4e-4✱ · `కు` 0.93 · `␣` 9.8e-5✱ · `ఱ` 6.5e-7✱ · `ర` 0.73 · `తి` 0.97 · `␣మ` 0.99 · `ని` 0.98 · `స` 0.95 · `్ర` 4.8e-5✱ · `స` 0.72 · `వ` 0.90 · `త` 6.9e-3✱ · `రు` 4.9e-5✱ · `డు` 2.4e-4✱ · `చి` 0.73 · `న` 4.8e-3✱ · `␣గ` 0.93 · `ంది` 8.0e-7✱ · `క` 0.99 · `్` 2.1e-7✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 143 tokens · 37.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జకమకజగమ్య జగతి కొని జపమర్రు మనులకటి తజమమ్య జగమక జగమతిమ్యా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 2 | మృకతి మతి మక్తిక జగక జగతి మమ్రమతి మృతక జగతిమ్య మతిమొకటి జగతిమ్యా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 3 | తృకత మతి లోకము జగక మతి జగర్వరరతిమతిమమతిమ్యకమనికకటితికక్యా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 4 | దికుకతితితిన్ర న న సొక సకకమాకకకకక లయతిభాతితితితితితితితి కంటే | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 26% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.031 · model's first choice kept 36% · constraint overrode 56% · backtracks 0

<details><summary>Token probabilities (143 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.11 · `క` 0.06 · `మ` 0.04 · `క` 0.04✱ · `జ` 0.02✱ · `గ` 0.26 · `మ` 0.28 · `్య` 4.7e-4✱ · `␣జగ` 0.13 · `తి` 0.73 · `␣కొ` 2.4e-4✱ · `ని` 0.14 · `␣జ` 0.08 · `ప` 0.09 · `మ` 0.08✱ · `ర` 0.04 · `్రు` 1.0e-5✱ · `␣మ` 0.28 · `ను` 0.02 · `ల` 0.03 · `క` 0.03✱ · `టి` 0.03✱ · `␣` 4.9e-3✱ · `త` 0.01✱ · `జ` 0.20 · `మ` 0.20 · `మ` 0.22 · `్య` 7.1e-4✱ · `␣జగ` 0.17✱ · `మ` 0.11 · `క` 0.02✱ · `␣జగ` 0.06✱ · `మ` 0.49 · `తి` 0.45 · `మ` 0.01✱ · `్యా` 1.1e-4✱ · `⏎` 0.19 |
| 2 | `మ` 0.27 · `ృ` 5.8e-4✱ · `క` 3.0e-3✱ · `తి` 0.62 · `␣మ` 0.89 · `తి` 0.90 · `␣మ` 0.92 · `క్తి` 0.02✱ · `క` 1.0e-4✱ · `␣జగ` 0.08 · `క` 8.0e-4✱ · `␣జగ` 0.74 · `తి` 0.77 · `␣మ` 0.39 · `మ` 0.16✱ · `్రమ` 8.2e-5✱ · `తి` 0.72 · `␣మ` 0.01✱ · `ృత` 3.9e-3✱ · `క` 0.75 · `␣జగ` 0.89 · `తి` 0.88 · `మ` 0.12✱ · `్య` 7.2e-4✱ · `␣మ` 0.31 · `తి` 0.60 · `మ` 0.30 · `ొ` 1.9e-6✱ · `క` 0.06✱ · `టి` 0.45 · `␣జగ` 0.90 · `తి` 0.71 · `మ` 9.6e-3✱ · `్యా` 8.6e-3✱ · `⏎` 0.93 |
| 3 | `త` 0.95 · `ృ` 3.2e-5✱ · `క` 3.3e-3✱ · `త` 3.2e-4✱ · `␣మ` 1.00 · `తి` 0.99 · `␣లో` 1.00 · `క` 1.00 · `ము` 0.99 · `␣జగ` 0.98 · `క` 1.3e-3✱ · `␣మ` 0.93 · `తి` 0.98 · `␣జగ` 0.97 · `ర` 4.4e-4✱ · `్వర` 5.2e-6✱ · `ర` 0.59 · `తి` 0.95 · `మ` 0.06✱ · `తి` 0.02✱ · `మ` 0.03✱ · `మ` 0.02✱ · `తి` 8.4e-3✱ · `మ` 0.02✱ · `్య` 6.7e-4✱ · `క` 9.6e-4✱ · `మని` 7.2e-4✱ · `క` 6.8e-4✱ · `క` 6.3e-4✱ · `టి` 2.7e-5✱ · `తి` 0.01✱ · `క` 0.02✱ · `క` 0.05✱ · `్యా` 7.9e-4✱ · `⏎` 0.46 |
| 4 | `ది` 5.5e-3✱ · `కు` 6.0e-4✱ · `క` 3.1e-3✱ · `తి` 0.03✱ · `తి` 0.06✱ · `తి` 0.04✱ · `న` 0.44 · `్ర` 7.2e-5✱ · `␣న` 0.39 · `␣న` 0.75 · `␣స` 0.69 · `ొ` 3.8e-4✱ · `క` 0.05✱ · `␣స` 0.66 · `క` 6.1e-3✱ · `క` 6.2e-3✱ · `మా` 3.3e-4✱ · `క` 0.06✱ · `క` 0.03✱ · `క` 0.03✱ · `క` 0.08✱ · `క` 7.0e-3✱ · `␣` 0.35 · `ల` 0.01✱ · `య` 0.33 · `తి` 0.35 · `భా` 0.09✱ · `తి` 0.68 · `తి` 0.01✱ · `తి` 0.07✱ · `తి` 0.02✱ · `తి` 0.02✱ · `తి` 0.10✱ · `తి` 0.05✱ · `తి` 0.04✱ · `␣కంటే` 3.9e-4✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 159 tokens · 40.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రమ భవన రక్షము లకము వెతి యెడుడ్రిసమమమతరతమారతము లము జయము సీతా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 2 | రమణము జయించు లకము మతి యెడుడత్రిసమమమరతమరత్య లము జ్యము లవముతత్యా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 3 | కుముతితితి లయ్రితితితిమి వతితితివ్యతితితి మ స న న సస్ర స న న మతి న సగాణం | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 4 | కముతితితితిన్రతితితి మితితితితివ్యతితితి మ స న న ల్యువ్రతితితి మ లయవిభాతివ్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 22% · single-akshara words 32% · repeated lines 0 · mean token probability (geometric) 0.040 · model's first choice kept 36% · constraint overrode 58% · backtracks 0

<details><summary>Token probabilities (159 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ర` 0.06✱ · `మ` 0.64 · `␣భ` 7.2e-3✱ · `వ` 0.02 · `న` 0.11✱ · `␣ర` 0.11 · `క్ష` 0.03 · `ము` 0.09 · `␣ల` 0.06✱ · `క` 0.04✱ · `ము` 0.04✱ · `␣వె` 0.02 · `తి` 0.11✱ · `␣య` 0.10 · `ె` 0.53 · `డు` 0.27 · `డ` 0.05✱ · `్రి` 2.2e-5✱ · `స` 0.09✱ · `మ` 0.76 · `మ` 0.02 · `మ` 0.04✱ · `త` 0.03✱ · `ర` 0.01✱ · `త` 0.04✱ · `మా` 0.02✱ · `ర` 0.10✱ · `త` 0.09 · `ము` 0.05✱ · `␣ల` 0.03 · `ము` 0.03✱ · `␣జ` 0.05✱ · `య` 0.19✱ · `ము` 0.16 · `␣సీ` 0.11✱ · `తా` 0.35 · `⏎` 0.02✱ forced |
| 2 | `ర` 0.15 · `మ` 0.89 · `ణ` 2.4e-3✱ · `ము` 0.64 · `␣జ` 0.87 · `య` 0.54 · `ించు` 0.06✱ · `␣ల` 0.93 · `క` 0.89 · `ము` 0.91 · `␣మ` 2.7e-3✱ · `తి` 0.83 · `␣య` 0.83 · `ె` 0.99 · `డు` 0.99 · `డ` 1.00 · `త్రి` 2.2e-4✱ · `స` 0.95 · `మ` 0.94 · `మ` 0.81 · `మ` 0.27✱ · `ర` 0.78 · `త` 0.90 · `మ` 0.04✱ · `ర` 0.96 · `త` 0.89 · `్య` 5.5e-5✱ · `␣ల` 0.59 · `ము` 0.73 · `␣జ` 0.40 · `్య` 7.5e-3✱ · `ము` 0.94 · `␣ల` 6.4e-4✱ · `వ` 5.1e-4✱ · `ము` 1.5e-3✱ · `త` 1.5e-4✱ · `త` 2.3e-4✱ · `్యా` 6.8e-6✱ · `⏎` 0.04✱ forced |
| 3 | `కు` 1.5e-3✱ · `ము` 6.8e-4✱ · `తి` 7.4e-3✱ · `తి` 0.04✱ · `తి` 0.06✱ · `␣ల` 0.86 · `య` 0.90 · `్రి` 1.5e-5✱ · `తి` 0.05✱ · `తి` 0.55 · `తి` 7.4e-3✱ · `మి` 2.0e-5✱ · `␣` 9.6e-5✱ · `వ` 4.1e-3✱ · `తి` 0.08✱ · `తి` 0.02✱ · `తి` 4.9e-3✱ · `వ` 2.6e-3✱ · `్య` 3.6e-3✱ · `తి` 0.07✱ · `తి` 0.20 · `తి` 0.30 · `␣మ` 2.8e-3✱ · `␣స` 0.85 · `␣న` 0.92 · `␣న` 0.96 · `␣స` 0.93 · `స` 9.6e-4✱ · `్ర` 4.3e-4✱ · `␣స` 0.38 · `␣న` 0.50 · `␣న` 0.36 · `␣` 5.5e-3✱ · `మ` 8.3e-4✱ · `తి` 0.09✱ · `␣` 0.25✱ · `న` 2.3e-3✱ · `␣స` 0.03✱ · `గా` 0.04✱ · `ణం` 0.02 · `⏎` 3.4e-3✱ forced |
| 4 | `క` 8.8e-3✱ · `ము` 3.6e-3✱ · `తి` 0.01✱ · `తి` 0.49 · `తి` 0.09✱ · `తి` 0.05✱ · `న` 4.0e-3✱ · `్ర` 2.7e-4✱ · `తి` 0.04✱ · `తి` 0.20✱ · `తి` 0.17✱ · `␣` 2.8e-3✱ · `మి` 4.4e-4✱ · `తి` 0.05✱ · `తి` 0.18 · `తి` 0.43 · `తి` 0.27 · `వ` 0.04✱ · `్య` 6.1e-3✱ · `తి` 0.44 · `తి` 0.25 · `తి` 0.44 · `␣మ` 0.09✱ · `␣స` 0.05✱ · `␣న` 0.12✱ · `␣న` 0.20 · `␣ల` 3.3e-3✱ · `్య` 1.2e-4✱ · `ు` 8.3e-4✱ · `వ` 1.8e-3✱ · `్ర` 3.8e-3✱ · `తి` 0.07✱ · `తి` 0.10✱ · `తి` 0.49 · `␣మ` 0.02✱ · `␣ల` 0.90 · `య` 0.91 · `వి` 0.83 · `భా` 0.89 · `తి` 0.98 · `వ` 2.9e-4✱ · `్` 3.5e-4✱ |

</details>

[↑ meters](#meters)

---


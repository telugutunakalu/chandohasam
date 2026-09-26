# Sample poems — Gemma-4 E4B, constrained decoding

Sample poems from the **Gemma-4 E4B** constrained-decoding grid: two metrically perfect poems for each
of the 37 meters and each of the three decoding strategies, with the prompt and the probability of
every chosen token.

| | |
|---|---|
| model | `google/gemma-4-E4B-it`, BF16, Hugging Face `transformers` (autoregressive) |
| run | `experiments/runs/2026-09-24_e4b_constrained` — 37 meters × 3 topics × 5 seeds × 3 strategies = 1,665 poems, **all complete and accepted by the engines** |
| constraint | gaṇa + prāsa + yati enforced exactly on the metrical DAWG (strict profile, yati sandhi off), with the orthography filter |
| strategies | **masking only** — sample from the model's distribution restricted to allowed tokens; **masking + backtracking** — the same, rewinding to a checkpoint when the allowed set collapses (checkpoint every 3 tokens, at most 30 backtracks, temperature raised after a rewind); **hybrid** — the same mask, then among the 100 most probable allowed tokens prefer those that complete the line |
| sampling | temperature 0.7, top-p 0.9 |
| prompt | the chat template with a system message and a user message (the meter's rules and the topic); no prefill |
| free generation | the unconstrained baseline (same prompts) wrote no poem in meter (0 / 555), so it has no samples here |

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

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

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

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 144 tokens · 35.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి దయల్రు గొప్పదెది మ్ర్య్దర్యమునున్చియునుమ్యమున్యమున్ | `UIIUIUIIIUIIUIIUIUIU` |
| 2 | తల్లి కరుణ్యలక్రియున భ్ర్మ్దర్యమునన్చియునుమ్యమున్యమున్ | `UIIUIUIIIUIIUIIUIUIU` |
| 3 | తల్లి అనుగ్రహమ్యున భ్ర్మ్ద ర్య్మ్నన్చియునుమ్యమునన్చియున్చియున్ | `UIIUIUIIIUIIUIIUIUIU` |
| 4 | తల్లి రమద్యలక్రియున భ్ర్మ్దర్య్మ్ననచియ్నుమయున్చియున్చియున్ | `UIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.092 · model's first choice kept 60% · constraint overrode 40% · backtracks 0

<details><summary>Token probabilities (144 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.80 · `ల్లి` 0.79 · `␣ద` 8.4e-3✱ · `య` 0.72 · `ల` 9.1e-3✱ · `్రు` 4.1e-5✱ · `␣గొప్ప` 0.22 · `ద` 0.39 · `ె` 0.23✱ · `ది` 0.08✱ · `␣మ` 0.03✱ · `్ర` 2.6e-6✱ · `్య` 1.2e-4✱ · `్` 8.0e-5✱ · `ద` 0.04✱ · `ర` 0.25 · `్య` 2.2e-4✱ · `ము` 0.16 · `ను` 0.03✱ · `న్` 2.0e-3✱ · `చి` 1.4e-4✱ · `యు` 2.0e-3✱ · `ను` 0.01✱ · `మ` 9.7e-4✱ · `్య` 0.07✱ · `ము` 0.14✱ · `న` 0.05✱ · `్య` 5.0e-4✱ · `ము` 0.14 · `న` 0.05✱ · `్` 4.2e-4✱ · `⏎` 0.76 forced |
| 2 | `త` 0.27 · `ల్లి` 0.85 · `␣క` 0.12✱ · `రుణ` 0.97 · `్య` 1.9e-3✱ · `ల` 0.24✱ · `క` 7.5e-3✱ · `్రి` 5.5e-5✱ · `యు` 0.20✱ · `న` 0.18 · `␣భ` 0.05 · `్ర` 1.7e-3✱ · `్` 9.0e-7✱ · `మ` 0.84 · `్` 1.3e-3✱ · `ద` 0.21✱ · `ర` 0.38 · `్య` 0.85 · `ము` 0.91 · `న` 0.35 · `న్` 0.36 · `చి` 0.24 · `యు` 0.96 · `ను` 0.79 · `మ` 0.92 · `్య` 0.99 · `ము` 0.99 · `న` 0.97 · `్య` 0.85 · `ము` 0.98 · `న` 0.92 · `్` 0.92 · `⏎` 1.00 forced |
| 3 | `త` 0.87 · `ల్లి` 0.94 · `␣అను` 0.15✱ · `గ్రహ` 0.03✱ · `మ` 0.09✱ · `్య` 6.0e-3✱ · `ు` 0.21 · `న` 0.38 · `␣భ` 0.24 · `్ర` 0.83 · `్` 0.98 · `మ` 0.95 · `్` 0.67 · `ద` 0.97 · `␣ర` 1.8e-4✱ · `్య` 0.99 · `్` 3.9e-6✱ · `మ` 0.27✱ · `్` 5.1e-3✱ · `న` 0.50 · `న్` 0.91 · `చి` 0.98 · `యు` 0.99 · `ను` 0.87 · `మ` 0.96 · `్య` 1.00 · `ము` 0.99 · `న` 0.99 · `న్` 0.01✱ · `చి` 0.23✱ · `యు` 0.95 · `న` 0.36✱ · `్` 0.89 · `చి` 2.8e-5✱ · `యు` 0.49✱ · `న` 0.61 · `్` 0.94 · `⏎` 0.98 forced |
| 4 | `త` 0.96 · `ల్లి` 0.97 · `␣ర` 0.04✱ · `మ` 1.2e-3✱ · `ద` 1.4e-3✱ · `్య` 0.38 · `ల` 0.38 · `క` 0.28 · `్రి` 0.90 · `యు` 0.94 · `న` 0.82 · `␣భ` 0.93 · `్ర` 0.97 · `్` 0.99 · `మ` 0.99 · `్` 0.76 · `ద` 0.98 · `ర` 0.59 · `్య` 0.99 · `్` 0.78 · `మ` 0.89 · `్` 0.57 · `న` 0.95 · `న` 1.3e-3✱ · `చి` 2.2e-3✱ · `య` 1.8e-4✱ · `్` 0.06✱ · `ను` 0.52 · `మ` 0.59 · `య` 1.9e-3✱ · `ు` 0.01✱ · `న` 0.90 · `్` 0.46 · `చి` 0.93 · `యు` 0.98 · `న` 0.99 · `్` 0.98 · `చి` 0.02✱ · `యు` 0.97 · `న` 0.99 · `్` 0.99 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 125 tokens · 35.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి కరుణ్యయే జగతి న్య్య్ధన్యమునందున నిత్యమున్రతః | `UIIUIUIIIUIIUIIUIUIU` |
| 2 | మౌల్లమునందునమ్రమున త్య్ర్మన్యమునందున భవ్యమున్రతః | `UIIUIUIIIUIIUIIUIUIU` |
| 3 | అల్లమునందునశ్రయమునత్య్ర్మనమున్రుతమున్రతః హృదయ్ | `UIIUIUIIIUIIUIIUIUIU` |
| 4 | ప్రాల్లమునందునప్య్యుమున త్య్ర్మన్యమునందున శాంతమున్రతః | `UIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 15% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.076 · model's first choice kept 58% · constraint overrode 36% · backtracks 0

<details><summary>Token probabilities (125 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.80 · `ల్లి` 0.79 · `␣క` 0.02✱ · `రుణ` 0.98 · `్య` 1.5e-5✱ · `యే` 0.05✱ · `␣జగ` 0.75 · `తి` 0.94 · `␣న` 3.7e-3✱ · `్య` 9.3e-7✱ · `్య` 3.1e-5✱ · `్` 2.0e-5✱ · `ధ` 7.8e-3✱ · `న` 0.10✱ · `్య` 1.8e-4✱ · `ము` 0.29 · `న` 0.27✱ · `ందు` 0.29 · `న` 0.10✱ · `␣ని` 2.4e-3✱ · `త్య` 0.80 · `ము` 0.61 · `న` 0.04✱ · `్ర` 1.2e-5✱ · `త` 0.04✱ · `ః` 0.01✱ · `⏎` 0.93 forced |
| 2 | `మ` 0.16 · `ౌ` 0.06✱ · `ల` 6.1e-4✱ · `్` 2.3e-7✱ · `ల` 0.77 · `ము` 0.18 · `న` 0.69 · `ందు` 0.23✱ · `న` 0.64 · `మ` 1.9e-3✱ · `్ర` 5.8e-3✱ · `ము` 0.26 · `న` 0.39 · `␣త` 0.02✱ · `్య` 0.03✱ · `్ర` 3.4e-4✱ · `్` 4.5e-4✱ · `మ` 0.26 · `న` 0.06✱ · `్య` 0.17✱ · `ము` 0.49 · `న` 0.81 · `ందు` 0.07✱ · `న` 0.89 · `␣భ` 0.03 · `వ` 0.22 · `్య` 0.02✱ · `ము` 0.58 · `న` 0.89 · `్ర` 0.29 · `త` 0.97 · `ః` 1.00 · `⏎` 1.00 forced |
| 3 | `అ` 0.17 · `ల` 0.07✱ · `్` 1.5e-5✱ · `ల` 0.88 · `ము` 0.24 · `న` 0.92 · `ందు` 0.97 · `న` 0.99 · `శ` 9.0e-3✱ · `్ర` 0.28 · `య` 0.95 · `ము` 0.97 · `న` 0.98 · `త` 2.7e-4✱ · `్య` 0.04✱ · `్ర` 0.53 · `్` 0.81 · `మ` 0.91 · `న` 0.90 · `ము` 3.6e-3✱ · `న` 0.99 · `్రు` 2.1e-4✱ · `త` 0.45 · `ము` 0.16✱ · `న` 0.98 · `్ర` 5.9e-3✱ · `త` 0.99 · `ః` 1.00 · `␣హ` 4.5e-5✱ · `ృ` 0.60 · `ద` 0.18 · `య` 0.40 · `్` 1.4e-4✱ · `⏎` 0.05 forced |
| 4 | `ప` 0.09 · `్రా` 0.28✱ · `ల్ల` 9.7e-7✱ · `ము` 0.80 · `న` 1.00 · `ందు` 1.00 · `న` 0.99 · `ప` 0.27 · `్య` 0.20 · `్య` 0.21 · `ు` 0.07 · `ము` 0.06 · `న` 0.99 · `␣త` 0.43 · `్య` 0.95 · `్ర` 0.97 · `్` 0.98 · `మ` 0.96 · `న` 0.98 · `్య` 0.88 · `ము` 0.99 · `న` 1.00 · `ందు` 0.97 · `న` 0.99 · `␣శా` 0.03 · `ంత` 0.35 · `ము` 0.49 · `న` 0.99 · `్ర` 0.97 · `త` 1.00 · `ః` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 122 tokens · 36.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి కరుణ్య సుందర వృథా కదెదియ్నుమ ఝణ్యెనై నమస్ | `UIIUIUIIIUIIUIIUIUIU` |
| 2 | తల్లి మమత్యె దివ్య స్రవతాన దయల్రుతమమ్మెనై నమస్ | `UIIUIUIIIUIIUIIUIUIU` |
| 3 | తల్లి రమణ్య సూక్ష్మ రస వ్ర్య్ధా కదెదియ్నుమ ఝణ్యెనై నమస్ | `UIIUIUIIIUIIUIIUIUIU` |
| 4 | తల్లి కరుణ్య మమ్ర సుగధా త్వరితాన దయల్రుతమ్యెనై | `UIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 33% · single-akshara words 4% · repeated lines 0 · mean token probability (geometric) 0.081 · model's first choice kept 48% · constraint overrode 41% · backtracks 30

<details><summary>Token probabilities (122 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.80 · `ల్లి` 0.79 · `␣క` 0.02✱ · `రుణ` 0.98 · `్య` 1.7e-5✱ · `␣సు` 0.01✱ · `ంద` 0.09 · `ర` 0.60 · `␣వ` 0.03✱ · `ృ` 4.7e-3✱ · `థ` 6.3e-6✱ · `ా` 0.63 · `␣క` 0.05✱ · `ద` 0.13✱ · `ె` 0.85 · `ది` 2.5e-3 · `య` 0.01✱ · `్` 5.0e-3✱ · `ను` 0.01✱ · `మ` 0.02✱ · `␣` 5.9e-4✱ · `ఝ` 0.41 · `ణ` 0.21 · `్య` 0.10✱ · `ె` 0.01✱ · `న` 0.08✱ · `ై` 5.6e-3✱ · `␣న` 2.7e-3✱ · `మ` 0.11 · `స్` 0.06✱ · `⏎` 0.01 forced |
| 2 | `త` 0.36 · `ల్లి` 0.90 · `␣మ` 0.04✱ · `మ` 0.97 · `త` 0.90 · `్య` 9.1e-5✱ · `ె` 0.07✱ · `␣ది` 0.02 · `వ్య` 0.98 · `␣స` 0.02✱ · `్ర` 0.03✱ · `వ` 1.00 · `త` 7.1e-4✱ · `ాన` 2.2e-3✱ · `␣ద` 0.02 · `య` 0.07✱ · `ల` 0.03✱ · `్రు` 4.5e-4✱ · `త` 0.03 · `మ` 0.05 · `మ్` 0.02✱ · `మె` 0.17✱ · `న` 0.78 · `ై` 0.52 · `␣న` 0.59 · `మ` 0.99 · `స్` 1.00 · `⏎` 0.99 forced |
| 3 | `త` 0.91 · `ల్లి` 0.93 · `␣ర` 0.02✱ · `మ` 5.7e-3✱ · `ణ` 9.4e-3✱ · `్య` 0.64 · `␣సూ` 7.6e-3 · `క్ష్` 0.53 · `మ` 0.93 · `␣ర` 8.8e-3✱ · `స` 0.67 · `␣వ` 0.03✱ · `్ర` 4.9e-3✱ · `్య` 4.3e-7✱ · `్` 9.8e-4✱ · `ధ` 0.41 · `ా` 0.35 · `␣క` 0.19 · `ద` 0.69 · `ె` 0.98 · `ది` 0.88 · `య` 0.99 · `్` 0.98 · `ను` 0.98 · `మ` 0.95 · `␣` 0.67 · `ఝ` 0.99 · `ణ` 1.00 · `్య` 1.00 · `ె` 1.00 · `న` 1.00 · `ై` 1.00 · `␣న` 1.00 · `మ` 1.00 · `స్` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ల్లి` 0.98 · `␣క` 0.04✱ · `రుణ` 0.22✱ · `్య` 0.04✱ · `␣మ` 0.02✱ · `మ` 0.04✱ · `్ర` 8.5e-4✱ · `␣సు` 0.07 · `గ` 0.07✱ · `ధ` 2.3e-3✱ · `ా` 0.36 · `␣త` 0.04 · `్వ` 0.13 · `రి` 0.65 · `త` 0.70 · `ాన` 0.17 · `␣ద` 0.49 · `య` 0.97 · `ల` 0.98 · `్రు` 1.00 · `త` 1.00 · `మ` 0.99 · `్య` 1.0e-5✱ · `ె` 0.09✱ · `న` 0.99 · `ై` 1.00 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 95 tokens · 30.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి కరుణ్య విక్రియ శతద్రియ గానమునందు నిత్యమై | `UIIUIUIIIUIIUIIUIUIU` |
| 2 | తల్లి అనుగ్రహంబు దెనిదన్ ముకితత్వమునిచ్చునట్లుగా | `UIIUIUIIIUIIUIIUIUIU` |
| 3 | తల్లి మమత్య ప్రభ్రుత త్రిదశ్య సకల్లతమున్రు నిత్యమై | `UIIUIUIIIUIIUIIUIUIU` |
| 4 | తల్లి దయగ్రుడత్వము సుదాహరనమ్ములొలిక్యెనున్రుగా | `UIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 32% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.032 · model's first choice kept 37% · constraint overrode 51% · backtracks 30

<details><summary>Token probabilities (95 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.80 · `ల్లి` 0.79 · `␣క` 0.02✱ · `రుణ` 0.98 · `్య` 1.7e-5✱ · `␣వి` 7.4e-3✱ · `క` 0.09 · `్రియ` 4.6e-6✱ · `␣శ` 4.5e-3✱ · `త` 0.03✱ · `ద` 0.02✱ · `్రియ` 5.5e-4✱ · `␣గా` 1.0e-3✱ · `న` 0.35 · `ము` 0.61 · `న` 0.12✱ · `ందు` 0.09✱ · `␣ని` 0.01✱ · `త్య` 0.37✱ · `మై` 0.02 · `⏎` 0.58 forced |
| 2 | `త` 0.47 · `ల్లి` 0.70 · `␣అను` 0.06✱ · `గ్రహ` 9.6e-3✱ · `ం` 0.12✱ · `బు` 0.04 · `␣ద` 0.01 · `ె` 1.7e-4✱ · `ని` 0.16✱ · `ద` 1.7e-3✱ · `న్` 9.2e-4✱ · `␣ము` 0.01✱ · `కి` 3.1e-3✱ · `త` 0.39 · `త్వ` 0.03✱ · `ము` 0.66 · `ని` 0.05 · `చ్చు` 0.59 · `న` 0.23 · `ట్లు` 0.03✱ · `గా` 0.03✱ · `⏎` 0.98 forced |
| 3 | `త` 0.88 · `ల్లి` 0.92 · `␣మ` 0.04✱ · `మ` 0.94 · `త` 0.88 · `్య` 4.5e-5✱ · `␣ప్రభ` 5.7e-3✱ · `్రు` 8.8e-5✱ · `త` 0.83 · `␣త` 0.02 · `్రి` 0.02✱ · `ద` 2.5e-3✱ · `శ` 0.44 · `్య` 0.01✱ · `␣స` 0.10 · `క` 0.04✱ · `ల` 0.96 · `్` 7.0e-6✱ · `ల` 0.64 · `త` 0.02 · `ము` 0.10 · `న` 0.23 · `్రు` 3.6e-5✱ · `␣ని` 0.16 · `త్య` 0.48 · `మై` 0.70 · `⏎` 1.00 forced |
| 4 | `త` 0.96 · `ల్లి` 0.95 · `␣ద` 0.01✱ · `య` 0.61 · `గ` 3.0e-3✱ · `్రు` 2.8e-3✱ · `డ` 0.47 · `త్వ` 0.02✱ · `ము` 0.78 · `␣సు` 0.02✱ · `దా` 6.2e-4✱ · `హ` 0.04 · `ర` 0.61 · `న` 0.16 · `మ్ము` 0.01✱ · `ల` 0.04 · `ొ` 0.03 · `లి` 0.04 · `క` 0.13✱ · `్య` 1.8e-4✱ · `ె` 0.25 · `ను` 0.37 · `న` 0.03✱ · `్రు` 1.5e-5✱ · `గా` 0.04✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 136 tokens · 9.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీ వనలంబి నమ్యుడెను సేవకమున్యుని వృత్తమున్యుడా | `UIIUIUIIIUIIUIIUIUIU` |
| 2 | గీవన లంఖనమ్యుని ధ్రు వ్వ్వ్కృప్యుని సేవనమున్యుడా సుమా | `UIIUIUIIIUIIUIIUIUIU` |
| 3 | శూవన గమ్యుడెన్యుని జ్యెజొన్యుని భీతిని తొల్రమెన్యుడా | `UIIUIUIIIUIIUIIUIUIU` |
| 4 | వ్యావహరన్యునియ్న సము ద్య్దై నృపునియ్న లభన్యుడా హరీ | `UIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 14% · repeated lines 0 · mean token probability (geometric) 0.058 · model's first choice kept 45% · constraint overrode 38% · backtracks 0

<details><summary>Token probabilities (136 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.09 · `్రీ` 0.27 · `␣వ` 0.07✱ · `న` 0.10✱ · `ల` 0.01 · `ంబ` 0.07 · `ి` 0.37 · `␣న` 0.04 · `మ` 0.05 · `్య` 0.01✱ · `ు` 0.48 · `డ` 0.47 · `ె` 0.31✱ · `ను` 0.25 · `␣స` 0.10✱ · `ేవ` 1.4e-5✱ · `క` 0.09✱ · `ము` 0.18 · `న` 0.30 · `్య` 2.1e-4✱ · `ు` 0.16 · `ని` 0.20✱ · `␣వ` 1.7e-3✱ · `ృ` 0.08 · `త్త` 0.82 · `ము` 0.86 · `న` 0.30✱ · `్య` 6.5e-4✱ · `ు` 0.93 · `డా` 6.4e-4 · `⏎` 0.92 forced |
| 2 | `గ` 0.16 · `ీ` 0.03✱ · `వ` 3.2e-6✱ · `న` 0.46 · `␣ల` 0.04 · `ం` 0.34 · `ఖ` 8.8e-3✱ · `న` 0.23 · `మ` 5.1e-3✱ · `్య` 0.15 · `ు` 0.92 · `ని` 0.62 · `␣ధ` 0.04 · `్రు` 1.2e-3✱ · `␣వ` 8.7e-6✱ · `్వ` 4.4e-4✱ · `్వ` 6.1e-4✱ · `్` 1.6e-3✱ · `క` 9.7e-3✱ · `ృ` 0.01✱ · `ప` 0.50 · `్య` 0.23 · `ు` 0.85 · `ని` 0.73 · `␣స` 0.06 · `ేవ` 0.12✱ · `న` 0.21 · `ము` 0.75 · `న` 0.81 · `్య` 0.96 · `ు` 0.99 · `డా` 0.78 · `␣సు` 1.6e-5✱ · `మా` 0.04 · `⏎` 0.90 forced |
| 3 | `శ` 0.07 · `ూ` 0.13✱ · `వ` 2.2e-5✱ · `న` 0.42 · `␣గ` 0.05 · `మ` 0.50 · `్య` 0.73 · `ు` 0.74 · `డ` 0.54 · `ె` 0.85 · `న` 0.05✱ · `్య` 1.2e-3✱ · `ు` 0.99 · `ని` 0.68 · `␣జ` 0.03 · `్య` 0.29✱ · `ె` 0.02✱ · `జ` 7.1e-3✱ · `ొ` 6.9e-3✱ · `న` 0.39 · `్య` 0.03✱ · `ు` 0.98 · `ని` 0.81 · `␣భ` 0.06 · `ీ` 0.46 · `తి` 0.23 · `ని` 0.39 · `␣తొ` 0.25 · `ల` 1.00 · `్రమ` 1.2e-7✱ · `ె` 1.3e-3✱ · `న` 0.13✱ · `్య` 0.98 · `ు` 1.00 · `డా` 0.96 · `⏎` 0.79 forced |
| 4 | `వ` 0.21 · `్యా` 8.7e-3✱ · `వ` 0.02✱ · `హ` 0.96 · `ర` 0.01✱ · `న` 0.11✱ · `్య` 0.08✱ · `ు` 1.00 · `ని` 0.78 · `య` 3.3e-5✱ · `్` 0.03✱ · `న` 0.51 · `␣స` 0.09 · `ము` 0.98 · `␣ద` 1.5e-4✱ · `్య` 0.18 · `్` 0.02✱ · `ద` 0.10 · `ై` 0.12 · `␣న` 0.08 · `ృ` 0.01 · `పు` 0.06 · `ని` 0.38 · `య` 5.6e-3✱ · `్` 0.96 · `న` 0.96 · `␣ల` 0.29 · `భ` 2.1e-3✱ · `న` 0.25✱ · `్య` 0.01✱ · `ు` 1.00 · `డా` 0.93 · `␣హ` 0.15✱ · `రీ` 6.3e-3 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 118 tokens · 8.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి కరుణ్యయే జగతి న్య్య్ధన్యమునందునయే స్తరీత్రమే | `UIIUIUIIIUIIUIIUIUIU` |
| 2 | మా ల్లి మమత్యె మౌనమున మన్నియమున్యె మధుర్యతేమునే | `UIIUIUIIIUIIUIIUIUIU` |
| 3 | జాల్ల జ్యెజన్యమున్యె జ్యురసన్యె జ్యురమ్యమునందునయ్యతే | `UIIUIUIIIUIIUIIUIUIU` |
| 4 | అల్లె అపార్యమున్యె అపహర్యమునందునయెన్యె అభ్యతే | `UIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 16% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.049 · model's first choice kept 48% · constraint overrode 44% · backtracks 0

<details><summary>Token probabilities (118 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.80 · `ల్లి` 0.79 · `␣క` 0.02✱ · `రుణ` 0.98 · `్య` 1.5e-5✱ · `యే` 0.05✱ · `␣జగ` 0.75 · `తి` 0.94 · `␣న` 3.7e-3✱ · `్య` 9.3e-7✱ · `్య` 3.1e-5✱ · `్` 2.0e-5✱ · `ధ` 7.8e-3✱ · `న` 0.10✱ · `్య` 1.8e-4✱ · `ము` 0.29 · `న` 0.27✱ · `ందు` 0.29 · `న` 0.10✱ · `యే` 3.1e-3✱ · `␣` 5.6e-4✱ · `స్త` 0.20 · `రీ` 0.24 · `త్ర` 5.8e-3✱ · `మే` 4.3e-3 · `⏎` 0.77 forced |
| 2 | `మా` 0.19 · `␣` 2.1e-7✱ · `ల్లి` 3.1e-4✱ · `␣మ` 0.23✱ · `మ` 0.93 · `త` 0.90 · `్య` 5.2e-4✱ · `ె` 0.08✱ · `␣మ` 0.68 · `ౌ` 0.04✱ · `న` 0.86 · `ము` 0.33 · `న` 0.66 · `␣మ` 0.24 · `న్ని` 0.02✱ · `య` 0.12✱ · `ము` 0.27 · `న` 0.56 · `్య` 1.5e-4✱ · `ె` 0.39 · `␣మ` 0.49 · `ధు` 0.32 · `ర` 0.83 · `్య` 4.6e-3✱ · `తే` 0.03 · `ము` 1.6e-3✱ · `నే` 0.04✱ · `⏎` 1.00 forced |
| 3 | `జ` 0.08 · `ాల` 2.7e-3✱ · `్` 5.5e-6✱ · `ల` 0.42 · `␣జ` 0.12 · `్య` 0.48 · `ె` 9.3e-4✱ · `జ` 0.07✱ · `న` 0.39 · `్య` 0.11✱ · `ము` 0.26 · `న` 0.49 · `్య` 1.7e-3✱ · `ె` 0.90 · `␣జ` 0.60 · `్య` 0.56 · `ు` 0.01✱ · `ర` 0.19 · `స` 5.9e-3✱ · `న` 0.03✱ · `్య` 0.75 · `ె` 0.59 · `␣జ` 0.88 · `్య` 0.78 · `ు` 0.11✱ · `ర` 0.68 · `మ` 0.11 · `్య` 0.15 · `ము` 0.19✱ · `న` 0.83 · `ందు` 0.02✱ · `న` 0.85 · `య` 0.01✱ · `్య` 7.7e-4✱ · `తే` 1.4e-3 · `⏎` 0.95 forced |
| 4 | `అ` 0.10 · `ల్ల` 0.01✱ · `ె` 0.27 · `␣అ` 0.57 · `ప` 0.03✱ · `ార` 0.88 · `్య` 0.10 · `ము` 0.18 · `న` 0.93 · `్య` 0.96 · `ె` 0.99 · `␣అ` 0.94 · `ప` 0.17✱ · `హ` 4.1e-3✱ · `ర్య` 0.01✱ · `ము` 0.90 · `న` 1.00 · `ందు` 0.23✱ · `న` 0.99 · `య` 0.44 · `ె` 0.02✱ · `న` 1.6e-4✱ · `్య` 0.03✱ · `ె` 0.24 · `␣అ` 0.46 · `భ` 0.02 · `్య` 4.4e-4✱ · `తే` 0.04 |

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

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 115 tokens · 23.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వనమును దాటి లంకను త్వవన్యమునందున చేరెనుత్రియెన్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 2 | పనమును దాటి లంకను త్వవన్యమునందున చేరెనుత్రియెన్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 3 | శనమును దాటి లంకను త్వ వ్య్య్నన్యమునందున చేరెనుత్రియెన్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 4 | వనమును దాటి లంకను త్వ వ్య్య్నన్యమునందున చేరెనుత్రియెన్ | `IIIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 27% · single-akshara words 9% · repeated lines 0 · mean token probability (geometric) 0.222 · model's first choice kept 76% · constraint overrode 19% · backtracks 0

<details><summary>Token probabilities (115 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.51 · `న` 6.3e-4✱ · `ము` 0.44 · `ను` 0.11✱ · `␣దా` 0.86 · `టి` 0.81 · `␣ల` 0.44 · `ంక` 0.73 · `ను` 0.50 · `␣త` 7.6e-4✱ · `్వ` 0.35 · `వ` 1.7e-5✱ · `న` 0.03 · `్య` 3.7e-4✱ · `ము` 0.13✱ · `న` 0.44 · `ందు` 0.02✱ · `న` 0.12✱ · `␣చే` 0.13✱ · `రె` 0.79 · `ను` 0.96 · `త` 9.7e-4✱ · `్రియ` 7.5e-5✱ · `ె` 0.10 · `న` 0.05✱ · `్` 1.4e-5✱ · `⏎` 0.92 forced |
| 2 | `ప` 0.10 · `న` 5.4e-3✱ · `ము` 0.69 · `ను` 0.26 · `␣దా` 0.66 · `టి` 0.90 · `␣ల` 0.71 · `ంక` 0.95 · `ను` 0.85 · `␣త` 0.68 · `్వ` 0.96 · `వ` 0.99 · `న` 0.98 · `్య` 1.00 · `ము` 0.99 · `న` 0.99 · `ందు` 1.00 · `న` 0.99 · `␣చే` 0.92 · `రె` 1.00 · `ను` 0.99 · `త` 0.95 · `్రియ` 1.00 · `ె` 1.00 · `న` 0.99 · `్` 1.00 · `⏎` 0.99 forced |
| 3 | `శ` 0.12 · `న` 0.02✱ · `ము` 0.90 · `ను` 0.86 · `␣దా` 0.99 · `టి` 0.98 · `␣ల` 1.00 · `ంక` 1.00 · `ను` 1.00 · `␣త` 1.00 · `్వ` 1.00 · `␣వ` 5.8e-6✱ · `్య` 2.2e-5✱ · `్య` 6.7e-6✱ · `్` 4.7e-7✱ · `న` 0.73 · `న` 6.5e-3✱ · `్య` 0.03✱ · `ము` 0.97 · `న` 0.98 · `ందు` 0.99 · `న` 0.99 · `␣చే` 0.99 · `రె` 1.00 · `ను` 1.00 · `త` 0.98 · `్రియ` 1.00 · `ె` 1.00 · `న` 1.00 · `్` 1.00 · `⏎` 1.00 forced |
| 4 | `వ` 0.10 · `న` 0.82 · `ము` 0.89 · `ను` 0.79 · `␣దా` 0.98 · `టి` 0.97 · `␣ల` 0.99 · `ంక` 0.99 · `ను` 0.98 · `␣త` 0.99 · `్వ` 0.97 · `␣వ` 0.40 · `్య` 0.60 · `్య` 0.92 · `్` 0.84 · `న` 0.99 · `న` 0.99 · `్య` 1.00 · `ము` 1.00 · `న` 1.00 · `ందు` 1.00 · `న` 1.00 · `␣చే` 0.99 · `రె` 1.00 · `ను` 1.00 · `త` 0.99 · `్రియ` 1.00 · `ె` 1.00 · `న` 1.00 · `్` 1.00 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 106 tokens · 17.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి మదిలోన తల్లి మమతో నిలిచెద్రియెనున్రునుత్యునిన్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 2 | అలసిన జీవనాన అలునగ్యమునందున నిత్యమున్రునుత్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 3 | కలసిన జగ్రుమందున కృ ద్య్న్కల్యమునందున కల్పనానుతన్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 4 | నిలచిన భావనాన నిరనీయమునందున నిత్యమున్రునుత్ | `IIIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 22% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.047 · model's first choice kept 49% · constraint overrode 45% · backtracks 0

<details><summary>Token probabilities (106 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ొ` 1.7e-3✱ · `లి` 0.66 · `␣మ` 0.07✱ · `ది` 0.67 · `లో` 0.57 · `న` 0.68 · `␣తల్లి` 0.59 · `␣మ` 0.02✱ · `మ` 0.98 · `త` 0.92 · `ో` 1.3e-3✱ · `␣ని` 0.12 · `లి` 0.27✱ · `చె` 0.68 · `ద` 0.03✱ · `్రియ` 2.2e-6✱ · `ె` 0.08✱ · `ను` 0.06✱ · `న` 3.1e-4✱ · `్రు` 4.0e-6✱ · `ను` 1.4e-3✱ · `త` 1.4e-3✱ · `్య` 8.3e-4✱ · `ు` 0.04✱ · `ని` 0.14✱ · `న` 7.4e-3✱ · `్` 1.5e-6✱ · `⏎` 0.60 forced |
| 2 | `అ` 0.15 · `ల` 0.18✱ · `సిన` 0.78 · `␣జీ` 0.07 · `వ` 0.88 · `న` 0.95 · `ాన` 0.19✱ · `␣అ` 0.14✱ · `లు` 1.6e-3✱ · `న` 2.4e-3✱ · `గ` 0.01✱ · `్య` 5.0e-4✱ · `ము` 0.04✱ · `న` 0.36 · `ందు` 6.8e-3✱ · `న` 0.17 · `␣ని` 0.15 · `త్య` 0.15✱ · `ము` 0.41 · `న` 0.39 · `్రు` 0.06✱ · `ను` 0.55 · `త` 0.88 · `్` 1.9e-5✱ · `⏎` 0.09 forced |
| 3 | `క` 0.29 · `ల` 0.17✱ · `సిన` 0.21 · `␣జగ` 0.15 · `్రు` 8.0e-8✱ · `మ` 0.41 · `ందు` 0.54 · `న` 0.66 · `␣క` 0.94 · `ృ` 5.8e-6✱ · `␣ద` 6.8e-7✱ · `్య` 2.0e-3✱ · `్` 5.4e-5✱ · `న` 0.26 · `్` 4.6e-6✱ · `క` 0.05✱ · `ల` 0.22 · `్య` 0.02✱ · `ము` 0.46 · `న` 0.79 · `ందు` 0.41 · `న` 0.92 · `␣క` 0.59 · `ల్ప` 0.06✱ · `నా` 0.06 · `ను` 0.47 · `త` 0.54 · `న్` 0.02✱ · `⏎` 0.99 forced |
| 4 | `ని` 0.07 · `ల` 0.03✱ · `చిన` 0.62 · `␣భా` 0.02 · `వ` 0.99 · `న` 0.35 · `ాన` 0.06✱ · `␣ని` 0.64 · `ర` 0.06✱ · `న` 8.1e-3✱ · `ీయ` 3.4e-4✱ · `ము` 0.71 · `న` 0.98 · `ందు` 0.70 · `న` 0.99 · `␣ని` 0.53 · `త్య` 0.79 · `ము` 0.85 · `న` 0.95 · `్రు` 0.99 · `ను` 0.98 · `త` 0.95 · `్` 0.47 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 117 tokens · 32.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి మమతన్ కదా తలపు ద్యోతినెదో వనితౌమయమ్మెనై | `IIIIUIUIIIUIIUIIUIUIU` |
| 2 | తొలి కరుణామృతమ్ము తలతొల్రు ఘనత్రియెనై నిలిచ్యెనై | `IIIIUIUIIIUIIUIIUIUIU` |
| 3 | తొలి తపనమ్యమున్రు తలతొల్రు ధరణ్యశరణ్యమై నిలిచ్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 4 | తొలి తులసిక్రియెన్రు తలతొల్రు జగద్రియమై నిలిచ్యెనై | `IIIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 33% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.093 · model's first choice kept 46% · constraint overrode 44% · backtracks 30

<details><summary>Token probabilities (117 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ొ` 1.7e-3✱ · `లి` 0.66 · `␣మ` 0.07✱ · `మ` 0.17 · `త` 0.81 · `న్` 1.3e-3✱ · `␣క` 0.02 · `దా` 0.04 · `␣త` 0.21✱ · `ల` 0.04✱ · `పు` 0.59 · `␣ద` 6.4e-3✱ · `్య` 1.3e-3✱ · `ో` 0.85 · `త` 0.94 · `ిన` 0.68 · `ె` 0.02✱ · `ద` 0.08 · `ో` 0.81 · `␣వ` 3.7e-3✱ · `ని` 0.61 · `త` 0.02✱ · `ౌ` 2.4e-3✱ · `మ` 6.8e-4✱ · `య` 0.04✱ · `మ్` 0.02✱ · `మె` 5.0e-3✱ · `న` 0.08✱ · `ై` 0.01✱ · `⏎` 0.89 forced |
| 2 | `త` 0.56 · `ొ` 4.5e-3✱ · `లి` 0.77 · `␣క` 0.05 · `రుణ` 0.94 · `ామ` 0.11 · `ృత` 0.14 · `మ్ము` 0.09✱ · `␣త` 0.22✱ · `ల` 0.72 · `త` 1.3e-3✱ · `ొ` 0.53 · `ల` 0.14✱ · `్రు` 5.6e-6✱ · `␣ఘ` 4.3e-3 · `న` 0.66 · `త` 0.29 · `్రియ` 5.0e-3✱ · `ె` 0.08✱ · `న` 0.22 · `ై` 0.53 · `␣ని` 0.09✱ · `లి` 0.24✱ · `చ` 0.02✱ · `్య` 1.3e-3✱ · `ె` 0.06✱ · `న` 0.16✱ · `ై` 0.97 · `⏎` 1.00 forced |
| 3 | `త` 0.81 · `ొ` 0.08✱ · `లి` 0.89 · `␣త` 0.11✱ · `ప` 0.13✱ · `న` 0.74 · `మ` 0.13 · `్య` 1.1e-3✱ · `ము` 0.07✱ · `న` 0.13✱ · `్రు` 6.4e-5✱ · `␣త` 0.69 · `ల` 0.73 · `త` 0.20✱ · `ొ` 0.93 · `ల` 0.84 · `్రు` 0.87 · `␣ధ` 0.05 · `రణ` 4.3e-3✱ · `్య` 0.10✱ · `శ` 0.06 · `రణ` 0.02✱ · `్య` 0.09✱ · `మై` 0.46 · `␣ని` 0.52 · `లి` 0.70 · `చ` 0.86 · `్` 5.0e-8✱ · `⏎` 1.2e-5 forced |
| 4 | `త` 0.99 · `ొ` 0.98 · `లి` 0.99 · `␣త` 0.19 · `ుల` 0.12✱ · `సి` 0.10✱ · `క` 0.09 · `్రియ` 6.9e-4✱ · `ె` 0.13 · `న` 0.59 · `్రు` 0.52 · `␣త` 0.97 · `ల` 1.00 · `త` 0.98 · `ొ` 1.00 · `ల` 1.00 · `్రు` 0.99 · `␣జగ` 0.29 · `ద` 0.11✱ · `్రియ` 1.3e-3✱ · `మై` 0.26✱ · `␣ని` 0.77 · `లి` 0.74 · `చ` 0.74 · `్య` 0.94 · `ె` 0.92 · `న` 0.96 · `ై` 1.00 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 100 tokens · 31.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి మదిలోన తల్లి మమతో నిలిచేదె నమస్కరించుమా | `IIIIUIUIIIUIIUIIUIUIU` |
| 2 | తొలకరి చూపులోన తలతొక్కును తప్యమిదిన్ చెలియ్ముమా | `IIIIUIUIIIUIIUIIUIUIU` |
| 3 | తొలపున తోడుగా తనయెదో తలవంచెను దీవమిచ్చుమా | `IIIIUIUIIIUIIUIIUIUIU` |
| 4 | తొలకరి ఊపిరిన్రు తలతొక్కును తండ్రిని ప్రేమమంచుమా | `IIIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.126 · model's first choice kept 52% · constraint overrode 30% · backtracks 30

<details><summary>Token probabilities (100 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ొ` 1.7e-3✱ · `లి` 0.66 · `␣మ` 0.07✱ · `ది` 0.67 · `లో` 0.57 · `న` 0.68 · `␣తల్లి` 0.59 · `␣మ` 0.02✱ · `మ` 0.98 · `త` 0.92 · `ో` 1.3e-3✱ · `␣ని` 0.12 · `లి` 0.27✱ · `చే` 0.17 · `ద` 0.03 · `ె` 0.39 · `␣న` 2.6e-3✱ · `మ` 0.08 · `స్క` 0.41 · `రించ` 0.01✱ · `ు` 0.94 · `మా` 0.03 · `⏎` 0.95 forced |
| 2 | `త` 0.32 · `ొ` 8.3e-3✱ · `ల` 0.23 · `క` 0.17✱ · `రి` 0.94 · `␣చూపు` 0.08 · `లో` 0.67 · `న` 0.57 · `␣త` 0.80 · `ల` 0.09✱ · `త` 7.7e-3✱ · `ొ` 0.87 · `క్కు` 0.06✱ · `ను` 0.08 · `␣త` 0.51 · `ప` 0.13 · `్య` 1.8e-3✱ · `మి` 0.02 · `ది` 0.52 · `న్` 1.9e-3✱ · `␣చె` 6.1e-3✱ · `లి` 0.09 · `య` 0.48 · `్` 0.03✱ · `ము` 3.0e-3✱ · `మా` 0.58 · `⏎` 1.00 forced |
| 3 | `త` 0.85 · `ొ` 0.03✱ · `ల` 0.30 · `పు` 0.05✱ · `న` 0.12 · `␣తో` 0.10 · `డు` 0.85 · `గా` 0.62 · `␣తన` 0.10✱ · `య` 0.12 · `ె` 0.17 · `ద` 0.06✱ · `ో` 0.16✱ · `␣త` 0.39 · `ల` 0.35 · `వ` 0.09 · `ంచ` 0.25 · `ె` 0.77 · `ను` 0.52 · `␣దీ` 0.01 · `వ` 0.56 · `మి` 2.2e-4✱ · `చ్చు` 0.01✱ · `మా` 0.99 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ొ` 0.93 · `ల` 0.35 · `క` 0.41 · `రి` 0.94 · `␣ఊ` 0.07 · `పి` 0.87 · `రి` 0.38 · `న` 0.12✱ · `్రు` 1.2e-6✱ · `␣త` 0.49 · `ల` 0.19✱ · `త` 0.03✱ · `ొ` 0.90 · `క్కు` 0.60 · `ను` 0.76 · `␣త` 0.72 · `ండ` 0.30 · `్రి` 0.65 · `ని` 0.29 · `␣ప్రేమ` 0.12 · `మ` 0.03 · `ంచు` 0.05✱ · `మా` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 137 tokens · 9.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలకరి తల్లి ప్రేమ జగదోపమునే కదెనుర్ఱినియ్నవూ | `IIIIUIUIIIUIIUIIUIUIU` |
| 2 | కలయిక మాధురిన్ కనక వ్ర్ఞ్ఖమ్యెన నిల్వునదిక్రియాంతురా | `IIIIUIUIIIUIIUIIUIUIU` |
| 3 | తొలి స్ననులందునత్యెన త్యెతొల్రు త్యెతొల్రు భవన్యెనైన్తిరా | `IIIIUIUIIIUIIUIIUIUIU` |
| 4 | జలముల మృద్యమైన్ జ్యెతొలొ ద్య్య్జైతొలొ నిత్యమునైన్తిరాంతురా | `IIIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 30% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.042 · model's first choice kept 39% · constraint overrode 50% · backtracks 0

<details><summary>Token probabilities (137 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ొ` 1.7e-3✱ · `ల` 0.31 · `క` 0.17 · `రి` 0.62 · `␣తల్లి` 0.08 · `␣ప్రేమ` 0.66 · `␣జగ` 0.14✱ · `ద` 3.8e-3✱ · `ో` 6.1e-6✱ · `ప` 0.71 · `ము` 0.10✱ · `న` 0.46 · `ే` 5.8e-3✱ · `␣క` 0.02✱ · `ద` 0.10✱ · `ె` 0.48 · `ను` 0.49 · `ర` 2.8e-4✱ · `్` 1.1e-5✱ · `ఱ` 0.11✱ · `ి` 0.09✱ · `ని` 8.2e-3✱ · `య` 6.8e-4✱ · `్` 0.04✱ · `న` 0.02✱ · `వ` 2.8e-3✱ · `ూ` 3.8e-3✱ · `⏎` 0.82 forced |
| 2 | `క` 0.07 · `ల` 0.11✱ · `య` 0.25 · `ిక` 0.94 · `␣మా` 0.01 · `ధు` 0.86 · `రి` 0.03✱ · `న్` 1.9e-3✱ · `␣క` 0.70 · `న` 0.04 · `క` 0.55 · `␣వ` 0.01✱ · `్ర` 7.4e-5✱ · `్ఞ` 2.6e-7✱ · `్` 1.7e-3✱ · `ఖ` 0.02✱ · `మ` 6.6e-3✱ · `్య` 0.02✱ · `ె` 0.09✱ · `న` 0.35 · `␣ని` 0.15 · `ల` 0.14✱ · `్వ` 1.5e-7✱ · `ు` 0.06 · `న` 0.13 · `ది` 0.02 · `క` 9.7e-3 · `్రి` 6.5e-4✱ · `యా` 0.24 · `ం` 0.02✱ · `తు` 0.07✱ · `రా` 1.9e-3✱ · `⏎` 0.99 forced |
| 3 | `త` 0.18 · `ొ` 0.02✱ · `లి` 0.27 · `␣స్` 0.04✱ · `న` 0.07✱ · `ను` 1.6e-3✱ · `ల` 0.51 · `ందు` 0.02✱ · `న` 0.42 · `త` 1.9e-3✱ · `్య` 3.7e-3✱ · `ె` 0.14✱ · `న` 0.43 · `␣త` 0.45 · `్య` 0.11✱ · `ె` 1.1e-3✱ · `త` 0.02✱ · `ొ` 0.05✱ · `ల` 0.25 · `్రు` 1.5e-3✱ · `␣త` 0.08 · `్య` 0.44 · `ె` 0.83 · `త` 0.52 · `ొ` 0.80 · `ల` 0.78 · `్రు` 0.59 · `␣భ` 0.01 · `వ` 0.29 · `న` 0.52 · `్య` 5.0e-3✱ · `ె` 0.05 · `న` 0.68 · `ై` 9.5e-3✱ · `న్` 0.01✱ · `తి` 0.02✱ · `రా` 0.26✱ · `⏎` 0.99 forced |
| 4 | `జ` 0.03 · `ల` 4.7e-3✱ · `ముల` 0.05 · `␣మ` 0.04✱ · `ృ` 0.04✱ · `ద` 0.31✱ · `్య` 4.7e-4✱ · `మై` 0.09 · `న్` 0.46 · `␣జ` 0.59 · `్య` 0.60 · `ె` 0.04✱ · `త` 0.34 · `ొ` 0.65 · `ల` 0.93 · `ొ` 4.3e-3✱ · `␣ద` 8.0e-3✱ · `్య` 0.06✱ · `్య` 1.9e-3✱ · `్` 1.4e-3✱ · `జ` 0.03✱ · `ై` 0.03 · `త` 0.26 · `ొ` 0.56 · `ల` 0.84 · `ొ` 0.36 · `␣ని` 0.10 · `త్య` 0.42 · `ము` 0.19 · `న` 0.34 · `ై` 0.40 · `న్` 0.35 · `తి` 0.87 · `రా` 0.98 · `ం` 4.8e-4✱ · `తు` 0.04✱ · `రా` 0.92 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 111 tokens · 8.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి మదిలోన తల్లి మమతో నిలిచెద్రియెనందునే జగత్ | `IIIIUIUIIIUIIUIIUIUIU` |
| 2 | మృలములకై మదిమ్రదనులృత్తమునందునెనుల్రుతమ్యయే | `IIIIUIUIIIUIIUIIUIUIU` |
| 3 | తొలకరి ప్రేమయే తలచు మ్ర్య్తుల్యమునందునెనుల్రుతమ్యయే | `IIIIUIUIIIUIIUIIUIUIU` |
| 4 | తొలిదెను సత్యమున్రుతమతొల్రుతమున్రుతమత్యయేతయే | `IIIIUIUIIIUIIUIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.052 · model's first choice kept 47% · constraint overrode 44% · backtracks 0

<details><summary>Token probabilities (111 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ొ` 1.7e-3✱ · `లి` 0.66 · `␣మ` 0.07✱ · `ది` 0.67 · `లో` 0.57 · `న` 0.68 · `␣తల్లి` 0.59 · `␣మ` 0.02✱ · `మ` 0.98 · `త` 0.92 · `ో` 1.3e-3✱ · `␣ని` 0.12 · `లి` 0.27✱ · `చె` 0.68 · `ద` 0.03✱ · `్రియ` 2.2e-6✱ · `ె` 0.08✱ · `న` 9.2e-3✱ · `ందు` 8.7e-3✱ · `న` 0.17✱ · `ే` 1.5e-4✱ · `␣జగ` 9.1e-3✱ · `త్` 8.0e-4✱ · `⏎` 0.16 forced |
| 2 | `మ` 0.03 · `ృ` 0.02✱ · `ల` 6.6e-5✱ · `ముల` 0.16 · `క` 0.45 · `ై` 0.88 · `␣మ` 0.55 · `ది` 0.33 · `మ` 0.13✱ · `్ర` 3.3e-5✱ · `ద` 0.14 · `ను` 0.03✱ · `ల` 0.06 · `ృ` 9.3e-5✱ · `త్త` 0.04 · `ము` 0.15✱ · `న` 0.47 · `ందు` 0.02✱ · `న` 0.49 · `ె` 0.03✱ · `ను` 0.08✱ · `ల` 0.02✱ · `్రు` 7.1e-4✱ · `త` 0.42 · `మ` 0.02✱ · `్య` 0.10✱ · `యే` 1.7e-3 · `⏎` 0.91 forced |
| 3 | `త` 0.23 · `ొ` 0.01✱ · `ల` 0.42 · `క` 0.32 · `రి` 0.43 · `␣ప్రేమ` 0.16 · `యే` 0.14 · `␣త` 0.66 · `ల` 0.30✱ · `చు` 0.02 · `␣మ` 6.0e-3✱ · `్ర` 1.3e-4✱ · `్య` 2.9e-6✱ · `్` 9.5e-5✱ · `త` 0.03✱ · `ుల` 2.3e-3✱ · `్య` 0.03✱ · `ము` 0.22 · `న` 0.65 · `ందు` 0.52 · `న` 0.87 · `ె` 0.57 · `ను` 0.73 · `ల` 0.87 · `్రు` 0.89 · `త` 0.97 · `మ` 0.95 · `్య` 0.98 · `యే` 0.99 · `⏎` 1.00 forced |
| 4 | `త` 0.37 · `ొ` 7.7e-3✱ · `లి` 0.53 · `ద` 0.02 · `ె` 0.04✱ · `ను` 0.27 · `␣స` 0.01 · `త్య` 0.81 · `ము` 0.46 · `న` 0.30 · `్రు` 6.1e-5✱ · `త` 0.83 · `మ` 0.19 · `త` 6.6e-3✱ · `ొ` 0.01✱ · `ల` 0.59 · `్రు` 5.4e-4✱ · `త` 0.80 · `ము` 0.22 · `న` 0.79 · `్రు` 4.2e-4✱ · `త` 0.95 · `మ` 0.82 · `త` 7.0e-3✱ · `్య` 0.17✱ · `యే` 0.67 · `త` 7.8e-4✱ · `యే` 0.08✱ |

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

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 129 tokens · 20.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శృనగారాన కమల్రసమ్య కరుణాకృత్యాంబుజం హేయునుభ్ | `IIUUIIUIUIIIUUUIUUIU` |
| 2 | సనతానాచరణం సదా సకల సుఖ్య్ర్చైతన్యముంబుజ్జ్వలమ్ | `IIUUIIUIUIIIUUUIUUIU` |
| 3 | వనవాసాన విధియ్న లంకకు వెలెన్ ర్ణ్య్భయ్రంభ్వ్వనమ్మాంబుజం | `IIUUIIUIUIIIUUUIUUIU` |
| 4 | శృనగారే నృమలన్ సకల్రథయ విక్రీడిత్యుమః శ్రీహరిం | `IIUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 22% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.048 · model's first choice kept 34% · constraint overrode 58% · backtracks 0

<details><summary>Token probabilities (129 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.17✱ · `ృ` 3.5e-3✱ · `న` 2.8e-3✱ · `గ` 0.59 · `ార` 0.56 · `ాన` 0.17✱ · `␣క` 0.10 · `మ` 0.06✱ · `ల` 0.86 · `్ర` 2.1e-4✱ · `స` 0.03✱ · `మ` 0.02✱ · `్య` 0.07✱ · `␣క` 0.03✱ · `రుణ` 0.26 · `ా` 0.59 · `క` 0.14 · `ృత` 0.01✱ · `్యా` 9.4e-4✱ · `ం` 0.08✱ · `బు` 0.01✱ · `జ` 0.09✱ · `ం` 0.87 · `␣హ` 1.4e-4✱ · `ే` 0.28✱ · `యు` 7.3e-3✱ · `ను` 0.01✱ · `భ` 6.6e-4✱ · `్` 2.6e-4✱ · `⏎` 0.10 forced |
| 2 | `స` 0.03 · `న` 8.1e-3✱ · `త` 0.24✱ · `ాన` 0.52 · `ా` 0.13✱ · `చ` 0.28 · `రణ` 0.10✱ · `ం` 0.51 · `␣స` 0.26 · `దా` 0.10✱ · `␣స` 0.26 · `క` 0.08✱ · `ల` 0.96 · `␣సు` 0.02 · `ఖ` 0.86 · `్య` 1.1e-3✱ · `్ర` 1.0e-3✱ · `్` 2.1e-5✱ · `చ` 7.1e-3✱ · `ై` 0.09✱ · `త` 0.32 · `న్య` 0.82 · `ము` 0.15 · `ం` 0.05✱ · `బు` 0.15✱ · `జ` 0.03✱ · `్` 1.5e-3✱ · `జ` 4.0e-3✱ · `్వ` 0.02✱ · `ల` 0.86 · `మ్` 0.12✱ · `⏎` 0.99 forced |
| 3 | `వ` 0.04✱ · `న` 0.72 · `వా` 0.63 · `స` 0.88 · `ాన` 0.37 · `␣వి` 0.24 · `ధి` 0.07 · `య` 0.24 · `్` 3.1e-4✱ · `న` 0.59 · `␣ల` 0.04 · `ంక` 0.59 · `కు` 0.14✱ · `␣వె` 0.44 · `లె` 0.06✱ · `న్` 0.09✱ · `␣ర` 0.21✱ · `్` 2.2e-9✱ · `ణ` 0.12 · `్య` 0.08✱ · `్` 2.8e-3✱ · `భ` 5.2e-3✱ · `య` 0.63 · `్ర` 1.7e-3✱ · `ం` 0.11✱ · `భ` 0.06 · `్వ` 0.02✱ · `్` 0.04✱ · `వ` 0.02✱ · `న` 0.10✱ · `మ్` 0.80 · `మా` 1.3e-3✱ · `ం` 0.02✱ · `బు` 0.05✱ · `జ` 0.83 · `ం` 0.55 · `⏎` 1.00 forced |
| 4 | `శ` 0.17 · `ృ` 0.02✱ · `న` 0.01✱ · `గ` 0.90 · `ార` 0.80 · `ే` 0.06 · `␣న` 0.02 · `ృ` 0.05 · `మ` 0.10✱ · `ల` 0.64 · `న్` 0.02✱ · `␣స` 0.04 · `క` 0.15✱ · `ల` 0.93 · `్ర` 3.0e-3✱ · `థ` 0.01✱ · `య` 6.9e-3✱ · `␣వి` 5.7e-3✱ · `క` 0.09 · `్రీ` 0.22✱ · `డి` 0.91 · `త` 0.91 · `్య` 5.4e-3✱ · `ు` 0.16✱ · `మ` 0.02✱ · `ః` 0.02✱ · `␣శ్రీ` 0.03 · `హ` 7.1e-3✱ · `రి` 0.59 · `ం` 0.44 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 144 tokens · 26.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి ప్రేమమ్మ తలప్రమున్రు తలపైన్య్య్తొల్యెన్రునృమ్యత్య్తొలెన్ | `IIUUIIUIUIIIUUUIUUIU` |
| 2 | అలసిన్రోకతమున్రు ఆనవనమున్రత్య్య్తొల్యెనన్రోకతెన్ | `IIUUIIUIUIIIUUUIUUIU` |
| 3 | కలసిన్రోకతమున్రు కౌగిలియమున్రత్య్య్తొల్యెనన్రోకతెన్ | `IIUUIIUIUIIIUUUIUUIU` |
| 4 | తొలి తల్యంకమునబ్ర తల్యలపనన్రుత్య్య్తొల్యెనన్రోకతెన్ | `IIUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.128 · model's first choice kept 61% · constraint overrode 32% · backtracks 0

<details><summary>Token probabilities (144 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.82 · `ొ` 2.0e-3✱ · `లి` 0.71 · `␣ప్రేమ` 0.10 · `మ్మ` 2.8e-3✱ · `␣త` 0.15 · `ల` 0.66 · `ప` 0.04✱ · `్ర` 1.4e-5✱ · `ము` 0.27 · `న` 0.19 · `్రు` 7.0e-6✱ · `␣త` 0.19 · `ల` 0.51 · `ప` 0.25 · `ైన` 0.02✱ · `్య` 3.7e-5✱ · `్య` 8.1e-4✱ · `్` 3.1e-4✱ · `త` 6.9e-3✱ · `ొ` 4.1e-3✱ · `ల` 0.31✱ · `్య` 3.4e-3✱ · `ె` 0.09✱ · `న` 0.04✱ · `్రు` 8.1e-4✱ · `న` 3.2e-4✱ · `ృ` 1.2e-3✱ · `మ` 5.1e-3✱ · `్య` 0.23✱ · `త` 0.09✱ · `్య` 0.01✱ · `్` 0.22 · `త` 0.50 · `ొ` 0.68 · `ల` 0.83 · `ె` 4.1e-3✱ · `న` 0.45 · `్` 1.1e-4✱ · `⏎` 0.86 forced |
| 2 | `అ` 0.25 · `ల` 0.04✱ · `సిన` 0.60 · `్రో` 4.8e-5✱ · `క` 0.02 · `త` 0.03 · `ము` 0.03 · `న` 0.60 · `్రు` 0.18 · `␣ఆ` 0.35 · `న` 0.16 · `వ` 1.1e-3✱ · `న` 0.23 · `ము` 0.40 · `న` 0.88 · `్ర` 0.02✱ · `త` 0.04✱ · `్య` 0.23✱ · `్య` 0.31 · `్` 0.85 · `త` 0.96 · `ొ` 0.97 · `ల` 0.93 · `్య` 0.34✱ · `ె` 0.83 · `న` 0.93 · `న` 0.02✱ · `్రో` 0.07✱ · `క` 0.43 · `త` 0.75 · `ె` 0.02✱ · `న` 0.79 · `్` 0.79 · `⏎` 1.00 forced |
| 3 | `క` 0.15 · `ల` 0.28✱ · `సిన` 0.32 · `్రో` 0.39 · `క` 0.58 · `త` 0.90 · `ము` 0.92 · `న` 0.99 · `్రు` 0.98 · `␣క` 0.53 · `ౌ` 3.6e-3✱ · `గి` 0.77 · `లి` 0.61 · `య` 0.11 · `ము` 0.17✱ · `న` 1.00 · `్ర` 0.89 · `త` 0.94 · `్య` 1.00 · `్య` 1.00 · `్` 0.99 · `త` 1.00 · `ొ` 1.00 · `ల` 1.00 · `్య` 0.87 · `ె` 0.99 · `న` 0.98 · `న` 0.62 · `్రో` 0.64 · `క` 0.99 · `త` 0.96 · `ె` 0.98 · `న` 0.97 · `్` 0.98 · `⏎` 1.00 forced |
| 4 | `త` 0.08✱ · `ొ` 0.03✱ · `లి` 0.57 · `␣త` 0.08 · `ల` 0.49 · `్యం` 4.2e-4✱ · `క` 0.14 · `ము` 0.32 · `న` 0.99 · `బ్ర` 7.4e-5✱ · `␣త` 0.05 · `ల` 0.80 · `్య` 3.8e-3✱ · `ల` 0.04✱ · `ప` 0.06 · `న` 0.55 · `న` 0.15✱ · `్రు` 0.43 · `త` 0.08✱ · `్య` 0.99 · `్య` 1.00 · `్` 0.98 · `త` 1.00 · `ొ` 1.00 · `ల` 0.99 · `్య` 0.78 · `ె` 0.98 · `న` 0.98 · `న` 0.92 · `్రో` 0.97 · `క` 0.98 · `త` 0.98 · `ె` 0.99 · `న` 0.94 · `్` 0.99 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 119 tokens · 42.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి స్పర్శేటి దయై జగద్రియము వీడ్య్య్తుందామునై వాంఛితుడ్ | `IIUUIIUIUIIIUUUIUUIU` |
| 2 | తొలి మాటల్రు తలప్రమున్యును నిలిచ్య్య్తుందామునై సత్యమై | `IIUUIIUIUIIIUUUIUUIU` |
| 3 | తొలి ఆశల్రు హృదయ్యునందు నిలిచక్య్య్తుందామునై భావమై | `IIUUIIUIUIIIUUUIUUIU` |
| 4 | తొలి జన్మల్రు తలవ్రునందు నిలిచక్య్య్తుందామునై శాశ్వతమ్ | `IIUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 24% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.089 · model's first choice kept 56% · constraint overrode 34% · backtracks 30

<details><summary>Token probabilities (119 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.82 · `ొ` 2.0e-3✱ · `లి` 0.71 · `␣స్ప` 0.02 · `ర్శ` 0.98 · `ే` 0.32 · `టి` 3.5e-3✱ · `␣ద` 0.01 · `య` 0.09✱ · `ై` 2.8e-3✱ · `␣జగ` 0.12✱ · `ద` 7.8e-3✱ · `్రియ` 6.7e-4✱ · `ము` 0.10✱ · `␣వీ` 5.3e-3 · `డ` 0.49 · `్య` 1.1e-4✱ · `్య` 1.0e-6✱ · `్` 4.9e-6✱ · `తు` 0.01✱ · `ందా` 9.6e-3✱ · `ము` 5.3e-4✱ · `న` 7.3e-3✱ · `ై` 0.10✱ · `␣వా` 1.3e-4✱ · `ం` 0.17 · `ఛ` 0.76 · `ి` 0.28 · `తు` 0.10✱ · `డ` 0.07✱ · `్` 1.2e-7✱ · `⏎` 3.0e-3 forced |
| 2 | `త` 0.51 · `ొ` 2.0e-3✱ · `లి` 0.79 · `␣మాట` 0.17 · `ల` 0.19✱ · `్రు` 3.5e-5✱ · `␣త` 0.12 · `ల` 0.48 · `ప` 0.09✱ · `్ర` 4.4e-5✱ · `ము` 0.38 · `న` 0.34 · `్య` 1.6e-4✱ · `ు` 0.09✱ · `ను` 6.0e-3✱ · `␣ని` 0.09 · `లి` 0.10✱ · `చ` 0.03✱ · `్య` 0.04✱ · `్య` 0.03✱ · `్` 0.37✱ · `తు` 0.89 · `ందా` 0.38 · `ము` 0.93 · `న` 0.95 · `ై` 0.99 · `␣స` 0.02 · `త్య` 0.59 · `మై` 0.15 · `⏎` 0.05 forced |
| 3 | `త` 0.85 · `ొ` 0.11✱ · `లి` 0.93 · `␣ఆ` 0.04 · `శ` 0.87 · `ల` 0.72 · `్రు` 0.46 · `␣హ` 0.26 · `ృ` 0.99 · `దయ` 0.89 · `్య` 2.5e-3✱ · `ు` 0.52 · `న` 0.49 · `ందు` 0.04✱ · `␣ని` 0.45 · `లి` 0.65 · `చ` 0.83 · `క్య` 3.8e-4✱ · `్య` 0.51 · `్` 0.97 · `తు` 1.00 · `ందా` 1.00 · `ము` 1.00 · `న` 0.99 · `ై` 1.00 · `␣భా` 0.02 · `వ` 0.97 · `మై` 0.87 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ొ` 0.87 · `లి` 1.00 · `␣జన్` 0.10 · `మ` 1.00 · `ల` 0.53 · `్రు` 0.96 · `␣త` 0.13 · `ల` 0.32 · `వ` 0.06 · `్రు` 6.7e-3✱ · `న` 0.44 · `ందు` 0.63 · `␣ని` 0.80 · `లి` 0.95 · `చ` 0.92 · `క్య` 0.40✱ · `్య` 1.00 · `్` 0.99 · `తు` 1.00 · `ందా` 1.00 · `ము` 1.00 · `న` 1.00 · `ై` 1.00 · `␣శా` 0.09 · `శ్వ` 0.67 · `త` 0.96 · `మ్` 3.9e-3✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 142 tokens · 41.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవనమ్రోతమునై వలెన్ గమయెనుయ్ భగ్వాన ప్రజ్వల్రచూ | `IIUUIIUIUIIIUUUIUUIU` |
| 2 | శవనమ్రోతమునై వలెన్ గమయెనుయ్ భ్ర్మ్చారిణ్వరుష్రూపమున్ | `IIUUIIUIUIIIUUUIUUIU` |
| 3 | సవధానమ్యెనెనున్ గమయ్న లొకమున్ లంకయ్ శిరస్సున్ నిలయ్ | `IIUUIIUIUIIIUUUIUUIU` |
| 4 | గె వెనమ్రోతమునై వలెన్ గమయెనుయ్ ల్క్ణ్యేనై ధనవ్నియ్ దయై | `IIUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 5% · repeated lines 0 · mean token probability (geometric) 0.062 · model's first choice kept 54% · constraint overrode 39% · backtracks 30

<details><summary>Token probabilities (142 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.25 · `వ` 0.67 · `న` 0.99 · `మ` 9.2e-3✱ · `్రో` 3.2e-3✱ · `త` 0.41 · `ము` 0.02✱ · `న` 0.38 · `ై` 6.7e-3✱ · `␣వ` 0.03 · `లె` 0.04✱ · `న్` 0.02✱ · `␣గ` 0.23 · `మ` 0.85 · `య` 0.21✱ · `ె` 0.43 · `ను` 0.76 · `య` 5.5e-4✱ · `్` 1.4e-3✱ · `␣భ` 3.8e-3✱ · `గ` 0.29 · `్వ` 2.9e-3✱ · `ాన` 0.58 · `␣ప్రజ` 9.0e-6✱ · `్వ` 0.58 · `ల` 0.94 · `్ర` 8.7e-4✱ · `చ` 6.9e-3✱ · `ూ` 1.6e-3✱ · `⏎` 0.05 forced |
| 2 | `శ` 0.16 · `వ` 3.9e-4✱ · `న` 0.30 · `మ` 0.17 · `్రో` 0.11✱ · `త` 0.86 · `ము` 0.89 · `న` 0.94 · `ై` 0.97 · `␣వ` 0.58 · `లె` 0.98 · `న్` 1.00 · `␣గ` 0.74 · `మ` 0.99 · `య` 1.00 · `ె` 1.00 · `ను` 0.99 · `య` 0.99 · `్` 1.00 · `␣భ` 0.48 · `్ర` 2.7e-5✱ · `్` 1.5e-7✱ · `మ` 0.71 · `్` 1.5e-4✱ · `చ` 3.4e-3✱ · `ారి` 0.75 · `ణ` 0.19 · `్వ` 0.07✱ · `రు` 0.11✱ · `ష` 4.9e-3✱ · `్ర` 4.1e-3✱ · `ూ` 0.95 · `ప` 1.1e-4✱ · `ము` 0.40✱ · `న` 0.02✱ · `్` 2.0e-4✱ · `⏎` 0.72 forced |
| 3 | `స` 0.50 · `వ` 3.0e-5✱ · `ధాన` 0.31 · `మ` 0.58 · `్య` 1.1e-4✱ · `ె` 0.31 · `న` 0.26 · `ె` 0.03✱ · `ను` 0.26 · `న` 0.01✱ · `్` 1.7e-4✱ · `␣గ` 0.10 · `మ` 0.90 · `య` 0.82 · `్` 1.1e-5✱ · `న` 0.12 · `␣ల` 0.12✱ · `ొ` 9.3e-5✱ · `క` 0.16✱ · `ము` 0.14 · `న` 0.68 · `్` 0.01✱ · `␣ల` 0.52 · `ంక` 0.61 · `య` 0.04✱ · `్` 0.02✱ · `␣శి` 0.05 · `ర` 0.30 · `స్సు` 0.29 · `న` 0.45 · `్` 0.37 · `␣ని` 0.04✱ · `ల` 0.38 · `య` 0.33 · `్` 0.43 · `⏎` 0.85 forced |
| 4 | `గ` 0.03 · `ె` 5.8e-4✱ · `␣వె` 4.7e-7✱ · `న` 0.38 · `మ` 0.29 · `్రో` 0.87 · `త` 0.96 · `ము` 0.95 · `న` 0.96 · `ై` 0.98 · `␣వ` 0.80 · `లె` 0.98 · `న్` 0.99 · `␣గ` 0.94 · `మ` 1.00 · `య` 0.99 · `ె` 0.97 · `ను` 0.99 · `య` 0.99 · `్` 1.00 · `␣ల` 0.13 · `్` 4.4e-6✱ · `క` 0.27 · `్` 7.0e-3✱ · `ణ` 0.38 · `్య` 0.06✱ · `ే` 0.09✱ · `న` 0.33 · `ై` 0.07✱ · `␣ధ` 0.03 · `న` 0.02✱ · `వ` 0.07 · `్` 3.3e-3✱ · `ని` 0.03 · `య` 0.32 · `్` 0.95 · `␣ద` 3.7e-3✱ · `య` 0.02✱ · `ై` 0.04✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 153 tokens · 11.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలకై తోడును తల్లి ప్రేమ మధురమ్య్య్తూమ్య్య్తూమ్య్య్తుమొక్య్తూమ్య్య్తనూ | `IIUUIIUIUIIIUUUIUUIU` |
| 2 | దొలకై దారిదృశిక్యు తల్లి దయ నిత్యుల్య్తూమ్య్య్తనూమ్య్య్తూమనో | `IIUUIIUIUIIIUUUIUUIU` |
| 3 | జలమై జాలువరాణి జ్యోతి జ్యలుమయ్త్య్చైతన్యమయ్య్తూమనో | `IIUUIIUIUIIIUUUIUUIU` |
| 4 | కలకై కమ్మని కౌగిలిక్కల కరుణ్య్త్కై తల్య్తనూమ్య్య్తూమనో | `IIUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 32% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.109 · model's first choice kept 56% · constraint overrode 35% · backtracks 0

<details><summary>Token probabilities (153 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.82 · `ొ` 2.0e-3✱ · `ల` 0.26 · `క` 0.15 · `ై` 0.15✱ · `␣తో` 0.08 · `డు` 0.73 · `ను` 0.07✱ · `␣తల్లి` 0.53 · `␣ప్రేమ` 0.49 · `␣మ` 0.03✱ · `ధు` 0.65 · `ర` 0.67 · `మ` 0.15✱ · `్య` 4.0e-4✱ · `్య` 1.1e-4✱ · `్` 9.6e-5✱ · `త` 9.6e-3✱ · `ూ` 4.2e-6✱ · `మ` 2.4e-3✱ · `్య` 0.04✱ · `్య` 0.16✱ · `్` 0.42✱ · `త` 0.56 · `ూ` 0.26✱ · `మ` 0.41✱ · `్య` 0.92 · `్య` 0.88 · `్` 0.91 · `త` 0.95 · `ు` 4.8e-4✱ · `మ` 0.05✱ · `ొ` 5.9e-6✱ · `క` 0.03✱ · `్య` 6.9e-4✱ · `్` 0.25 · `త` 0.87 · `ూ` 0.75 · `మ` 0.86 · `్య` 0.93 · `్య` 0.85 · `్` 0.96 · `త` 0.96 · `నూ` 3.5e-4✱ · `⏎` 0.94 forced |
| 2 | `ద` 0.02 · `ొ` 0.03✱ · `ల` 0.02✱ · `క` 0.94 · `ై` 0.98 · `␣ద` 0.72 · `ారి` 0.06 · `ద` 0.03✱ · `ృ` 0.05✱ · `శ` 0.18 · `ిక` 3.4e-4✱ · `్య` 9.5e-3✱ · `ు` 0.30 · `␣తల్లి` 0.43 · `␣ద` 0.20 · `య` 0.84 · `␣ని` 0.26 · `త్య` 0.83 · `ుల` 4.9e-3✱ · `్య` 0.83 · `్` 0.46 · `త` 0.86 · `ూ` 0.68 · `మ` 0.94 · `్య` 0.98 · `్య` 0.97 · `్` 0.99 · `త` 1.00 · `నూ` 0.24✱ · `మ` 0.03✱ · `్య` 0.49 · `్య` 0.89 · `్` 0.98 · `త` 0.99 · `ూ` 0.36✱ · `మ` 0.89 · `నో` 1.4e-4 · `⏎` 0.90 forced |
| 3 | `జ` 0.13 · `ల` 0.28✱ · `మై` 0.43 · `␣జ` 0.85 · `ాలు` 0.02 · `వ` 0.88 · `రా` 3.0e-3✱ · `ణి` 0.17✱ · `␣జ` 0.40 · `్య` 0.40 · `ోతి` 0.77 · `␣జ` 0.33 · `్య` 0.57 · `లు` 7.5e-3✱ · `మ` 0.16 · `య` 0.02✱ · `్` 0.14 · `త` 0.58 · `్య` 3.8e-4✱ · `్` 0.22✱ · `చ` 1.2e-4✱ · `ై` 0.09✱ · `త` 0.48 · `న్య` 0.83 · `మ` 0.23 · `య` 0.02✱ · `్య` 0.52 · `్` 0.95 · `త` 0.98 · `ూ` 0.52 · `మ` 0.97 · `నో` 0.03 · `⏎` 0.21 forced |
| 4 | `క` 0.12 · `ల` 0.66 · `క` 0.59 · `ై` 0.98 · `␣క` 0.91 · `మ్మ` 4.0e-3✱ · `ని` 0.33 · `␣క` 0.59 · `ౌ` 0.06✱ · `గి` 0.66 · `లి` 0.96 · `క` 7.6e-3✱ · `్` 5.9e-6✱ · `క` 0.32 · `ల` 0.09✱ · `␣క` 0.18 · `రుణ` 0.89 · `్య` 0.02✱ · `్` 0.06✱ · `త` 0.91 · `్` 3.0e-6✱ · `క` 2.9e-4✱ · `ై` 0.35 · `␣త` 0.12 · `ల` 0.19 · `్య` 3.7e-3✱ · `్` 0.68 · `త` 0.95 · `నూ` 0.08✱ · `మ` 0.88 · `్య` 0.92 · `్య` 0.99 · `్` 1.00 · `త` 1.00 · `ూ` 0.68 · `మ` 0.95 · `నో` 0.90 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 121 tokens · 8.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తలి ప్రేమక్రియ అమ్రుతమ్యదిని తేజ్య్య్తమ్మిహ్యెనక్రాంతియే | `IIUUIIUIUIIIUUUIUUIU` |
| 2 | తలి మమ్రోహము జగ్రుతమ్యదిని సత్యమ్యెన్యుగమ్యేనతమ్ | `IIUUIIUIUIIIUUUIUUIU` |
| 3 | తలి ఆశ్రయ్యము సుఖ్యతమ్యదిని శాంతమ్యెన్యనగ్రాంతియే | `IIUUIIUIUIIIUUUIUUIU` |
| 4 | తలి కౌగిల్యము పవ్యతమ్యదిని రక్ష్య్తమ్యెన్యుగమ్యేనతో | `IIUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.080 · model's first choice kept 55% · constraint overrode 37% · backtracks 0

<details><summary>Token probabilities (121 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.82 · `లి` 8.5e-4✱ · `␣ప్రేమ` 0.58 · `క` 0.02✱ · `్రియ` 1.4e-7✱ · `␣అమ` 0.01✱ · `్రు` 9.9e-5✱ · `త` 0.55 · `మ` 0.10 · `్య` 3.8e-3✱ · `ది` 0.24✱ · `ని` 0.02✱ · `␣తే` 0.05✱ · `జ` 0.82 · `్య` 1.6e-4✱ · `్య` 8.9e-6✱ · `్` 1.5e-5✱ · `త` 0.03✱ · `మ్` 0.18✱ · `మి` 7.3e-3✱ · `హ` 3.5e-3✱ · `్య` 0.29✱ · `ె` 0.16✱ · `న` 0.03✱ · `క` 1.5e-3✱ · `్రా` 2.5e-3✱ · `ంతి` 0.37 · `యే` 4.5e-3✱ · `⏎` 0.95 forced |
| 2 | `త` 0.24 · `లి` 0.06✱ · `␣మ` 0.09 · `మ` 0.90 · `్రో` 3.0e-5✱ · `హ` 0.50 · `ము` 0.43 · `␣జగ` 0.17 · `్రు` 1.1e-5✱ · `త` 0.16 · `మ` 0.49 · `్య` 0.77 · `ది` 0.94 · `ని` 0.95 · `␣స` 0.05 · `త్య` 0.73 · `మ` 0.27✱ · `్య` 0.13✱ · `ె` 0.20✱ · `న` 0.86 · `్య` 6.1e-4✱ · `ు` 0.13✱ · `గ` 7.9e-3✱ · `మ` 0.57 · `్య` 0.64 · `ే` 0.29 · `న` 2.8e-3✱ · `త` 0.02✱ · `మ్` 0.60 · `⏎` 0.89 forced |
| 3 | `త` 0.90 · `లి` 0.68 · `␣ఆ` 0.23 · `శ` 0.80 · `్ర` 0.35 · `య` 0.75 · `్య` 5.3e-6✱ · `ము` 0.17✱ · `␣సు` 0.08 · `ఖ` 0.82 · `్య` 0.02✱ · `త` 0.17 · `మ` 0.90 · `్య` 1.00 · `ది` 1.00 · `ని` 1.00 · `␣శా` 0.19 · `ంత` 0.48 · `మ` 0.88 · `్య` 1.00 · `ె` 1.00 · `న` 0.98 · `్య` 0.53 · `న` 0.14 · `గ` 0.21 · `్రా` 4.1e-4✱ · `ంతి` 0.27 · `యే` 0.90 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `లి` 0.96 · `␣క` 0.14✱ · `ౌ` 8.5e-3✱ · `గి` 0.83 · `ల` 0.35✱ · `్య` 0.80 · `ము` 0.61 · `␣ప` 0.04 · `వ` 0.02✱ · `్య` 2.5e-7✱ · `త` 0.98 · `మ` 1.00 · `్య` 1.00 · `ది` 1.00 · `ని` 1.00 · `␣ర` 0.06 · `క్ష` 0.83 · `్య` 0.15✱ · `్` 2.8e-3✱ · `త` 0.96 · `మ` 0.73 · `్య` 0.99 · `ె` 0.99 · `న` 0.97 · `్య` 0.67 · `ు` 0.21 · `గ` 0.10 · `మ` 0.93 · `్య` 0.97 · `ే` 0.92 · `న` 0.88 · `తో` 5.0e-4 |

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

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 140 tokens · 29.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిప్రాణమొకట్రు జగ్రుని కరుణ్య్ర్తమ్మెన్యెనల్రోచ్యమున్ | `UUUIIUIUIIIUUUIUUIU` |
| 2 | అల్లమ్మెన్దెననిందు కీర్తిని వెలస్ర్యన్యేనలొన్యున్తమమ్ | `UUUIIUIUIIIUUUIUUIU` |
| 3 | నిల్లాదర్యుని నందనై రథిని మిత్ర్యేనల్యునత్రామునై | `UUUIIUIUIIIUUUIUUIU` |
| 4 | తల్లిప్రియ్యుని తల్యునిన్యెనలొనల్య్య్తమ్యున్యెనల్రోచ్యమున్ | `UUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.061 · model's first choice kept 48% · constraint overrode 38% · backtracks 0

<details><summary>Token probabilities (140 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.75 · `ల్లి` 0.77 · `ప` 0.03✱ · `్రా` 0.58 · `ణ` 0.85 · `మ` 0.38 · `ొ` 0.05✱ · `క` 0.98 · `ట` 7.1e-3✱ · `్రు` 7.6e-4✱ · `␣జగ` 0.13 · `్రు` 1.5e-7✱ · `ని` 0.25 · `␣క` 0.05✱ · `రుణ` 0.90 · `్య` 5.9e-4✱ · `్ర` 5.3e-4✱ · `్` 1.1e-5✱ · `త` 4.5e-3✱ · `మ్` 0.10✱ · `మె` 0.04✱ · `న` 0.04✱ · `్య` 3.6e-5✱ · `ె` 0.34 · `న` 0.05✱ · `ల` 9.4e-4✱ · `్రో` 7.8e-4✱ · `చ` 0.03✱ · `్య` 0.85 · `ము` 0.07 · `న` 0.01✱ · `్` 9.8e-6✱ · `⏎` 0.45 forced |
| 2 | `అ` 0.16 · `ల` 0.02✱ · `్` 2.9e-6✱ · `ల` 0.75 · `మ్` 0.05 · `మె` 0.39 · `న్` 0.14 · `ద` 0.12 · `ె` 0.19 · `న` 0.42 · `ని` 0.01 · `ందు` 6.6e-3 · `␣క` 0.02 · `ీ` 0.09✱ · `ర్` 0.92 · `తి` 0.88 · `ని` 0.33 · `␣వె` 0.02 · `ల` 0.58 · `స` 0.03✱ · `్ర` 1.1e-3✱ · `్య` 0.04✱ · `న` 0.02✱ · `్య` 0.02✱ · `ే` 0.11 · `న` 0.52 · `ల` 0.19 · `ొ` 0.08✱ · `న` 0.19 · `్య` 0.46 · `ు` 0.12✱ · `న` 0.49 · `్` 0.90 · `త` 2.6e-4✱ · `మ` 9.1e-3✱ · `మ్` 0.11✱ · `⏎` 0.91 forced |
| 3 | `ని` 0.06 · `ల` 5.4e-3✱ · `్లా` 2.0e-7✱ · `ద` 0.26 · `ర` 0.12 · `్య` 6.9e-3✱ · `ు` 0.20 · `ని` 0.22 · `␣న` 0.06 · `ంద` 0.20 · `న` 0.65 · `ై` 0.08 · `␣ర` 0.02 · `థ` 8.7e-3✱ · `ి` 0.03✱ · `ని` 0.42 · `␣మ` 0.05 · `ిత` 0.02 · `్ర` 0.69 · `్య` 0.17 · `ే` 0.25✱ · `న` 0.95 · `ల` 0.51 · `్య` 0.01✱ · `ు` 0.49 · `న` 0.84 · `త` 0.01✱ · `్రా` 0.01✱ · `ము` 0.06 · `న` 0.76 · `ై` 8.9e-3✱ · `⏎` 0.88 forced |
| 4 | `త` 0.12 · `ల్లి` 0.72 · `ప` 0.12 · `్రియ` 0.22 · `్య` 8.2e-3✱ · `ు` 0.41 · `ని` 0.84 · `␣త` 0.38 · `ల` 0.16 · `్య` 3.0e-3✱ · `ు` 0.37 · `ని` 0.60 · `న` 7.1e-4✱ · `్య` 0.01✱ · `ె` 0.35✱ · `న` 0.89 · `ల` 0.86 · `ొ` 0.46 · `న` 0.65 · `ల` 5.5e-3✱ · `్య` 0.36 · `్య` 0.04✱ · `్` 1.1e-3✱ · `త` 0.26✱ · `మ` 0.50 · `్య` 0.46 · `ు` 0.43 · `న` 0.90 · `్య` 0.17 · `ె` 0.36 · `న` 0.90 · `ల` 0.53 · `్రో` 0.58 · `చ` 0.93 · `్య` 0.98 · `ము` 0.91 · `న` 0.78 · `్` 0.98 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 164 tokens · 26.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జైలించుమ్యుని తల్యునిన్రు నినులక్ర్య్చంబుల్ర ఝుంభుల్యునిన్ | `UUUIIUIUIIIUUUIUUIU` |
| 2 | దూలక్రయ్యునినన్ లభించుమున తల్య్య్నొన్రయ్న తల్య్యున్భ్ర్మలన్ | `UUUIIUIUIIIUUUIUUIU` |
| 3 | కైలాసమ్యునినన్ రఘుమ్యునిన తల్య్య్నై నమ్యునిన్రయ్న తల్ | `UUUIIUIUIIIUUUIUUIU` |
| 4 | భూలక్రయ్యునినన్ రఘుమ్యునిన తల్య్య్నొన్రయ్న తల్య్యున్భ్ర్మలన్ | `UUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 0% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.147 · model's first choice kept 59% · constraint overrode 30% · backtracks 0

<details><summary>Token probabilities (164 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.04 · `ై` 0.36 · `ల` 0.19 · `ించు` 0.05✱ · `మ` 9.6e-3✱ · `్య` 3.2e-3✱ · `ు` 0.18✱ · `ని` 0.23 · `␣త` 0.03 · `ల` 0.58 · `్య` 6.6e-5✱ · `ు` 0.31 · `ని` 0.76 · `న` 6.1e-3✱ · `్రు` 1.0e-4✱ · `␣ని` 0.02 · `ను` 0.09 · `ల` 0.07 · `క` 0.04✱ · `్ర` 2.2e-4✱ · `్య` 1.9e-3✱ · `్` 1.0e-3✱ · `చ` 0.02✱ · `ం` 0.05✱ · `బు` 0.02✱ · `ల` 0.03✱ · `్ర` 3.8e-4✱ · `␣` 2.4e-3✱ · `ఝ` 0.26 · `ు` 0.24 · `ం` 0.21 · `భ` 0.08✱ · `ుల` 0.05 · `్య` 0.08✱ · `ు` 0.71 · `ని` 0.54 · `న` 0.02✱ · `్` 5.4e-5✱ · `⏎` 0.72 forced |
| 2 | `ద` 0.03 · `ూ` 0.25 · `ల` 0.01✱ · `క` 0.48 · `్ర` 0.03✱ · `య` 0.26 · `్య` 0.10 · `ు` 0.73 · `ని` 0.83 · `న` 0.17 · `న్` 0.02✱ · `␣ల` 0.02 · `భ` 1.0e-3✱ · `ించు` 0.47 · `ము` 0.05 · `న` 0.18 · `␣త` 0.11✱ · `ల` 0.50 · `్య` 0.40 · `్య` 0.01✱ · `్` 1.3e-3✱ · `న` 0.04✱ · `ొ` 0.02✱ · `న` 0.06 · `్ర` 0.03 · `య` 0.03✱ · `్` 0.55 · `న` 0.43 · `␣త` 0.01 · `ల` 0.34 · `్య` 0.68 · `్య` 0.49 · `ు` 0.59 · `న` 0.18✱ · `్` 0.39 · `భ` 6.9e-4✱ · `్ర` 0.15✱ · `్` 0.02✱ · `మ` 0.48 · `ల` 0.03✱ · `న్` 0.20✱ · `⏎` 0.99 forced |
| 3 | `క` 0.07 · `ై` 0.21✱ · `లా` 0.18✱ · `స` 0.93 · `మ` 0.19✱ · `్య` 0.15✱ · `ు` 0.89 · `ని` 0.89 · `న` 0.46 · `న్` 0.14 · `␣ర` 0.14 · `ఘ` 0.02✱ · `ు` 1.00 · `మ` 0.39 · `్య` 0.64 · `ు` 0.95 · `ని` 0.90 · `న` 0.86 · `␣త` 0.12✱ · `ల` 0.93 · `్య` 0.93 · `్య` 0.85 · `్` 0.45 · `న` 0.75 · `ై` 0.02✱ · `␣న` 0.09 · `మ` 0.11 · `్య` 0.15✱ · `ు` 0.61 · `ని` 0.50 · `న` 0.89 · `్ర` 0.04✱ · `య` 0.24 · `్` 0.91 · `న` 0.95 · `␣త` 0.38 · `ల` 0.97 · `్` 4.4e-5✱ · `⏎` 1.3e-3 forced |
| 4 | `భ` 0.05 · `ూ` 0.61 · `ల` 0.04✱ · `క` 0.77 · `్ర` 0.87 · `య` 0.81 · `్య` 0.91 · `ు` 0.97 · `ని` 0.95 · `న` 0.98 · `న్` 0.85 · `␣ర` 0.31 · `ఘ` 0.04✱ · `ు` 0.96 · `మ` 0.77 · `్య` 0.99 · `ు` 0.99 · `ని` 0.92 · `న` 0.94 · `␣త` 0.71 · `ల` 0.99 · `్య` 0.96 · `్య` 0.80 · `్` 0.90 · `న` 0.98 · `ొ` 0.72 · `న` 0.96 · `్ర` 0.95 · `య` 0.99 · `్` 0.98 · `న` 1.00 · `␣త` 0.87 · `ల` 0.99 · `్య` 0.94 · `్య` 0.76 · `ు` 0.98 · `న` 0.95 · `్` 0.87 · `భ` 0.89 · `్ర` 0.94 · `్` 0.84 · `మ` 0.98 · `ల` 0.89 · `న్` 0.98 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 119 tokens · 33.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాతృప్రేమ లతైక రక్షణ వరం స్తన్రాణసిక్రంబునన్ | `UUUIIUIUIIIUUUIUUIU` |
| 2 | తాతృక్రీడన తుల్యమౌ జగతిలోనక్రీడెదెన్రోయ్ననిన్ | `UUUIIUIUIIIUUUIUUIU` |
| 3 | తాతృప్రేమ తలమ్రియంబున తలప్ర్య్ణత్యుంబునన్ జయ్ననిన్ | `UUUIIUIUIIIUUUIUUIU` |
| 4 | తాతృక్రీడెన తుల్యమౌ జగతిలోనత్యుంబునన్ జీవనమ్ | `UUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.065 · model's first choice kept 53% · constraint overrode 34% · backtracks 30

<details><summary>Token probabilities (119 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.15 · `త` 0.98 · `ృ` 0.98 · `ప్ర` 0.48 · `ే` 1.00 · `మ` 0.98 · `␣ల` 2.0e-3✱ · `త` 0.01✱ · `ై` 0.09✱ · `క` 0.22 · `␣ర` 8.2e-3✱ · `క్షణ` 0.01 · `␣వ` 0.02✱ · `రం` 0.08 · `␣` 9.4e-4✱ · `స్త` 0.20 · `న` 9.6e-3✱ · `్రా` 1.3e-4✱ · `ణ` 0.40 · `సి` 4.0e-4✱ · `క` 3.2e-3✱ · `్ర` 1.4e-4✱ · `ం` 0.28✱ · `బు` 8.1e-3✱ · `న` 5.6e-3✱ · `న్` 6.7e-4✱ · `⏎` 0.97 forced |
| 2 | `త` 0.45 · `ాత` 6.2e-4✱ · `ృ` 0.57 · `క` 0.09 · `్రీ` 3.7e-4✱ · `డ` 0.18 · `న` 0.18 · `␣త` 0.18 · `ుల` 0.10 · `్య` 0.80 · `మ` 0.18 · `ౌ` 0.23 · `␣జగ` 0.12 · `తి` 0.90 · `లో` 0.45 · `న` 0.57 · `క` 0.02✱ · `్రీ` 8.0e-4✱ · `డ` 0.35 · `ె` 0.14 · `ద` 0.24 · `ె` 0.30 · `న` 0.08 · `్రో` 4.2e-4✱ · `య` 0.17 · `్` 0.57 · `న` 7.4e-3✱ · `ని` 3.9e-3✱ · `న్` 2.8e-3✱ · `⏎` 1.00 forced |
| 3 | `త` 0.42 · `ాత` 0.01✱ · `ృ` 0.84 · `ప్ర` 0.10 · `ే` 0.84 · `మ` 0.91 · `␣త` 0.29 · `ల` 0.20 · `మ` 0.03✱ · `్రి` 3.3e-4✱ · `యం` 7.4e-3✱ · `బు` 0.37 · `న` 0.30 · `␣త` 0.28 · `ల` 0.37 · `ప` 0.13✱ · `్ర` 3.9e-4✱ · `్య` 7.0e-7✱ · `్` 1.9e-7✱ · `ణ` 0.47 · `త` 0.03 · `్య` 4.8e-3✱ · `ు` 0.21 · `ం` 0.18 · `బు` 0.75 · `న` 0.37 · `న్` 0.40 · `␣జ` 2.4e-5✱ · `య` 0.35 · `్` 8.5e-4✱ · `న` 0.86 · `ని` 0.08✱ · `న్` 0.97 · `⏎` 1.00 forced |
| 4 | `త` 0.79 · `ాత` 0.88 · `ృ` 0.97 · `క` 0.17 · `్రీ` 9.9e-3✱ · `డ` 0.82 · `ె` 0.14 · `న` 0.31 · `␣త` 0.67 · `ుల` 0.24 · `్య` 0.91 · `మ` 0.58 · `ౌ` 0.97 · `␣జగ` 0.36 · `తి` 0.96 · `లో` 0.92 · `న` 0.96 · `త` 0.04✱ · `్య` 2.3e-3✱ · `ు` 0.43 · `ం` 0.91 · `బు` 0.99 · `న` 0.93 · `న్` 0.56 · `␣జీ` 0.02 · `వ` 0.99 · `న` 0.59 · `మ్` 0.02✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 153 tokens · 62.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీ రాముడ్రు లొకేహ నాథుని మనుమ్య్య్యృమ్య్య్యుంతునుంబున్రదూ | `UUUIIUIUIIIUUUIUUIU` |
| 2 | సీరద్రీయ ద్రుపద్యునిక్రుచులెనక్ర్య్చీతస్య నారద్య్య్యునుం | `UUUIIUIUIIIUUUIUUIU` |
| 3 | రా రావణ్యుని మర్దనున్రుచులెనక్ర్య్చాళ్య్య్యుమ్య్య్యునుంబున్రదూ | `UUUIIUIUIIIUUUIUUIU` |
| 4 | లా రణ్య్య్యుంతున కీర్తినిర్ద్రియుల ద్రుప్య్య్లయ్య్య్యుంతునుంబున్రదూ | `UUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 7% · single-akshara words 20% · repeated lines 0 · mean token probability (geometric) 0.078 · model's first choice kept 43% · constraint overrode 40% · backtracks 30

<details><summary>Token probabilities (153 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.16 · `్రీ` 0.98 · `␣రా` 0.05 · `ము` 0.96 · `డ` 0.10✱ · `్రు` 0.02✱ · `␣ల` 0.42 · `ొ` 2.4e-4✱ · `కే` 0.02✱ · `హ` 2.3e-3 · `␣నా` 1.8e-3✱ · `థ` 0.35 · `ు` 0.75 · `ని` 0.80 · `␣మ` 9.0e-3 · `ను` 0.06✱ · `మ` 0.18 · `్య` 2.4e-3✱ · `్య` 1.5e-3✱ · `్య` 2.8e-3✱ · `ృ` 1.9e-4✱ · `మ` 0.03✱ · `్య` 0.45 · `్య` 0.72 · `్య` 0.58 · `ు` 0.08✱ · `ం` 0.06✱ · `తు` 0.02✱ · `ను` 5.9e-3✱ · `ం` 5.0e-3✱ · `బు` 3.9e-3✱ · `న` 3.8e-3✱ · `్ర` 1.1e-4✱ · `ద` 0.02✱ · `ూ` 0.04✱ · `⏎` 0.76 forced |
| 2 | `సీ` 0.48 · `ర` 1.5e-6✱ · `ద` 0.07✱ · `్రీ` 0.01✱ · `య` 0.06 · `␣ద` 0.08 · `్రు` 0.01✱ · `ప` 0.23 · `ద` 0.15✱ · `్య` 0.01✱ · `ు` 0.25 · `ని` 0.20✱ · `క` 1.5e-3✱ · `్రు` 7.7e-4✱ · `చు` 0.03✱ · `ల` 0.01✱ · `ె` 0.01 · `న` 0.20 · `క` 0.05✱ · `్ర` 2.8e-3✱ · `్య` 4.3e-3✱ · `్` 9.0e-3✱ · `చ` 0.03✱ · `ీ` 0.04✱ · `త` 0.42 · `స్య` 9.3e-3✱ · `␣న` 0.05 · `ార` 0.09 · `ద` 0.50 · `్య` 2.3e-3✱ · `్య` 0.57 · `్య` 0.22 · `ు` 0.75 · `ను` 0.01✱ · `ం` 0.84 · `⏎` 0.03 forced |
| 3 | `రా` 0.02✱ · `␣రావ` 3.4e-5✱ · `ణ` 0.64 · `్య` 0.10✱ · `ు` 0.53 · `ని` 0.75 · `␣మ` 0.05 · `ర్` 0.09 · `ద` 0.90 · `ను` 0.07 · `న` 0.06✱ · `్రు` 0.01✱ · `చు` 0.10 · `ల` 0.35 · `ె` 0.70 · `న` 0.84 · `క` 0.56 · `్ర` 0.79 · `్య` 0.98 · `్` 0.88 · `చ` 0.98 · `ా` 5.0e-3✱ · `ళ` 0.03 · `్య` 0.25 · `్య` 0.48 · `్య` 0.68 · `ు` 0.87 · `మ` 0.11✱ · `్య` 0.75 · `్య` 0.94 · `్య` 0.67 · `ు` 0.81 · `ను` 0.28✱ · `ం` 0.97 · `బు` 0.72 · `న` 0.30✱ · `్ర` 0.56 · `ద` 0.97 · `ూ` 1.00 · `⏎` 1.00 forced |
| 4 | `లా` 0.02 · `␣` 4.0e-5✱ · `రణ` 3.9e-5✱ · `్య` 0.95 · `్య` 0.79 · `్య` 0.59 · `ు` 0.72 · `ం` 0.06✱ · `తు` 0.78 · `న` 0.20 · `␣క` 5.9e-3✱ · `ీ` 0.28 · `ర్` 0.79 · `తి` 0.85 · `ని` 0.14 · `ర్` 5.1e-3✱ · `ద` 0.10 · `్రి` 0.22 · `యు` 0.10 · `ల` 0.20 · `␣ద` 0.07 · `్రు` 0.44 · `ప` 0.96 · `్య` 0.03✱ · `్య` 0.84 · `్` 7.2e-3✱ · `ల` 4.2e-4✱ · `య` 0.09 · `్య` 0.73 · `్య` 0.91 · `్య` 0.24 · `ు` 0.86 · `ం` 0.17✱ · `తు` 0.89 · `ను` 0.40✱ · `ం` 0.99 · `బు` 0.96 · `న` 0.70 · `్ర` 0.97 · `ద` 0.99 · `ూ` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 137 tokens · 12.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జైలించుణ్యుని జగ్వలంబిని రథం ధ్య్ర్చాతుర్వణమ్యుంభనమ్ | `UUUIIUIUIIIUUUIUUIU` |
| 2 | వాలిశ్వర్రమునివ్రథున్రయమునున్ర్య్వాస్రయ్యునిత్వంభనం | `UUUIIUIUIIIUUUIUUIU` |
| 3 | తైలమ్యుంభనమున్రథం సకలమాయ్య్య్ధర్మానమయ్య్య్ధర్మనం | `UUUIIUIUIIIUUUIUUIU` |
| 4 | కైలాసమ్యునినిక్రియాన త్రయమున్ర్య్ఘన్య్య్ధర్మనమ్భన్రతం | `UUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.053 · model's first choice kept 34% · constraint overrode 46% · backtracks 0

<details><summary>Token probabilities (137 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.04 · `ై` 0.36 · `ల` 0.19 · `ించు` 0.05✱ · `ణ` 2.1e-3✱ · `్య` 0.14✱ · `ు` 0.17 · `ని` 0.68 · `␣జగ` 0.05 · `్వ` 1.2e-5✱ · `ల` 0.48 · `ంబ` 0.09 · `ి` 0.56 · `ని` 0.47 · `␣ర` 0.32 · `థ` 1.7e-3✱ · `ం` 0.11✱ · `␣ధ` 0.09✱ · `్య` 0.02✱ · `్ర` 2.9e-6✱ · `్` 8.3e-9✱ · `చ` 6.7e-4✱ · `ా` 0.06✱ · `తు` 0.23✱ · `ర్` 0.03✱ · `వ` 0.24 · `ణ` 0.08 · `మ` 0.03✱ · `్య` 0.09✱ · `ు` 0.11 · `ం` 0.14✱ · `భ` 2.3e-3✱ · `న` 0.02✱ · `మ్` 0.08✱ · `⏎` 0.95 forced |
| 2 | `వ` 0.04 · `ాలి` 2.9e-3✱ · `శ` 0.03✱ · `్వర` 0.09✱ · `్ర` 1.2e-5✱ · `ము` 0.04✱ · `ని` 0.32 · `వ` 5.4e-4✱ · `్ర` 1.6e-4✱ · `థ` 0.02 · `ు` 0.07 · `న` 0.07✱ · `్ర` 1.7e-3✱ · `య` 0.08 · `ము` 0.20 · `ను` 0.10 · `న` 0.02✱ · `్ర` 1.6e-3✱ · `్య` 1.5e-3✱ · `్వ` 2.2e-3✱ · `ా` 0.34 · `స` 0.37 · `్ర` 0.06 · `య` 0.39 · `్య` 6.6e-3✱ · `ు` 0.30 · `ని` 0.09✱ · `త` 0.01✱ · `్వ` 2.7e-3✱ · `ం` 0.51 · `భ` 0.02✱ · `నం` 0.12 · `⏎` 1.00 forced |
| 3 | `త` 0.04 · `ై` 0.01✱ · `ల` 0.75 · `మ` 0.10✱ · `్య` 0.13 · `ు` 0.74 · `ం` 0.35 · `భ` 0.90 · `న` 0.93 · `ము` 0.28 · `న` 0.47 · `్ర` 0.05✱ · `థ` 0.12 · `ం` 0.43 · `␣స` 0.02 · `క` 0.06✱ · `ల` 0.89 · `మ` 0.23 · `ాయ` 0.08✱ · `్య` 0.09✱ · `్య` 0.02✱ · `్` 1.0e-3✱ · `ధ` 0.04✱ · `ర్` 0.10✱ · `మా` 0.61 · `న` 0.31 · `మ` 0.25 · `య` 0.02✱ · `్య` 0.88 · `్య` 0.20 · `్` 0.25 · `ధ` 0.34 · `ర్` 0.39 · `మ` 0.11✱ · `నం` 0.16✱ · `⏎` 1.00 forced |
| 4 | `క` 0.07 · `ై` 0.31 · `లా` 0.42 · `స` 0.97 · `మ` 0.36 · `్య` 0.45 · `ు` 0.83 · `ని` 0.06✱ · `ని` 0.09 · `క` 0.10✱ · `్రియ` 2.1e-3✱ · `ాన` 0.04 · `␣త` 0.12 · `్ర` 0.06 · `య` 0.50 · `ము` 0.19 · `న` 0.62 · `్ర` 0.17 · `్య` 0.03✱ · `్` 0.01✱ · `ఘ` 0.01✱ · `న` 0.57 · `్య` 0.04✱ · `్య` 0.59 · `్` 0.56 · `ధ` 0.57 · `ర్మ` 0.28 · `న` 0.18 · `మ్` 0.18 · `భ` 0.02✱ · `న` 0.07✱ · `్ర` 3.0e-5✱ · `తం` 0.01 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 155 tokens · 12.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | గమ్యమ్యంశము దాటి లంకరణ చేర్య్మ్గానయ్నునుమ్య్మ్యుంతుడా | `UUUIIUIUIIIUUUIUUIU` |
| 2 | శ్రమ్యుంతుడ్యుని సాగెనుస్రవనమున్య్మ్సల్యుంతుడానున్నునా | `UUUIIUIUIIIUUUIUUIU` |
| 3 | వ్యామ్యుంతుడ్యుని భీతినిత్యుని విదిల్య్మ్యైనుత్తమున్య్మ్సల్య్మనా | `UUUIIUIUIIIUUUIUUIU` |
| 4 | గమ్యమ్యుంతుడెనుప్రియుల్యుని గమన్య్మ్గానయ్నునుమ్య్మ్యుంతుడా | `UUUIIUIUIIIUUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.103 · model's first choice kept 52% · constraint overrode 38% · backtracks 0

<details><summary>Token probabilities (155 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `గ` 0.03 · `మ` 0.49 · `్య` 0.42 · `మ` 0.03✱ · `్యం` 7.5e-4✱ · `శ` 0.01 · `ము` 0.45 · `␣దా` 0.32 · `టి` 0.68 · `␣ల` 0.34 · `ం` 0.44 · `కరణ` 1.2e-4✱ · `␣చే` 0.39 · `ర` 0.08✱ · `్య` 2.3e-6✱ · `్` 2.1e-7✱ · `మ` 0.03✱ · `్` 1.9e-4✱ · `గా` 2.6e-4✱ · `న` 0.08✱ · `య` 3.3e-3✱ · `్` 0.22✱ · `ను` 3.4e-3✱ · `ను` 8.9e-3✱ · `మ` 1.1e-3✱ · `్య` 0.06✱ · `్` 0.25✱ · `మ` 0.12✱ · `్య` 0.24✱ · `ు` 0.19✱ · `ం` 0.05✱ · `తు` 0.01✱ · `డా` 0.08 · `⏎` 0.96 forced |
| 2 | `శ` 0.14 · `్రమ` 0.02✱ · `్య` 0.03✱ · `ు` 0.22 · `ం` 0.36 · `తు` 0.89 · `డ` 0.19✱ · `్య` 8.4e-3✱ · `ు` 0.43 · `ని` 0.07✱ · `␣సా` 0.07 · `గ` 0.49 · `ె` 0.17 · `ను` 0.64 · `స` 5.1e-4✱ · `్ర` 3.1e-4✱ · `వ` 0.64 · `న` 0.11 · `ము` 0.53 · `న` 0.27✱ · `్య` 2.6e-3✱ · `్` 0.40✱ · `మ` 0.88 · `్` 0.01✱ · `స` 1.4e-3✱ · `ల` 0.02✱ · `్య` 0.05✱ · `ు` 0.46 · `ం` 0.52 · `తు` 0.88 · `డా` 0.83 · `ను` 1.2e-4✱ · `న` 0.03✱ · `్` 0.02✱ · `ను` 0.50 · `నా` 4.6e-3✱ · `⏎` 0.99 forced |
| 3 | `వ` 0.30 · `్యా` 5.7e-3✱ · `మ` 2.9e-3✱ · `్య` 0.72 · `ు` 0.89 · `ం` 0.95 · `తు` 0.97 · `డ` 0.58 · `్య` 0.81 · `ు` 0.91 · `ని` 0.89 · `␣భ` 0.05 · `ీ` 0.44 · `తి` 0.49 · `ని` 0.31 · `త` 0.01✱ · `్య` 0.02✱ · `ు` 0.52 · `ని` 0.20✱ · `␣వి` 0.12 · `ది` 0.14 · `ల` 0.76 · `్య` 0.37 · `్` 0.23✱ · `మ` 0.84 · `్య` 0.63 · `ై` 1.5e-3✱ · `ను` 0.23 · `త` 0.01✱ · `్` 0.04✱ · `త` 0.37 · `ము` 0.37 · `న` 0.34 · `్య` 0.51 · `్` 0.80 · `మ` 0.94 · `్` 0.20 · `స` 0.45 · `ల` 0.71 · `్య` 0.88 · `్` 0.18 · `మ` 0.65 · `నా` 0.02 · `⏎` 1.00 forced |
| 4 | `గ` 0.08 · `మ` 0.92 · `్య` 0.95 · `మ` 0.25 · `్య` 0.67 · `ు` 0.96 · `ం` 0.99 · `తు` 0.99 · `డ` 0.54 · `ె` 0.02✱ · `ను` 0.35 · `ప` 8.6e-4✱ · `్రి` 0.02✱ · `యు` 0.31 · `ల` 0.15✱ · `్య` 3.5e-3✱ · `ు` 0.55 · `ని` 0.92 · `␣గ` 0.15 · `మ` 0.68 · `న` 0.03✱ · `్య` 0.01✱ · `్` 0.59 · `మ` 0.96 · `్` 0.20✱ · `గా` 6.6e-3✱ · `న` 0.87 · `య` 0.69 · `్` 0.86 · `ను` 0.96 · `ను` 0.62 · `మ` 0.56 · `్య` 0.97 · `్` 0.79 · `మ` 0.94 · `్య` 0.91 · `ు` 0.95 · `ం` 0.98 · `తు` 0.99 · `డా` 0.97 |

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

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 199 tokens · 51.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామచ్రియ్నన్ లఘుగ్రీవ్ణ్య్రణగణమున చేరన్తిరన్తిర్మలయ్నిర్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 2 | సీమల్యాణ్యున్ రణస్థల్య్న్చెరలయెన హరిణ్య్న్చెర్మలయ్నిర్న్తిరన్తిర్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 3 | త్రామక్య్న్చెర్మల్య్న్చెరల్య్నన్ రణమున నిలచిన్ రక్ష్య్నతన్తిర్మలయ్నిర్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 4 | వ్యామన్య్న్చెర్మల్య్న్చెరల్య్నన్ ల్క్య్నన నివృథిరయెన్ హర్య్న్చెరన్తిర్మలయ్నిర్ | `UUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 7% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.121 · model's first choice kept 53% · constraint overrode 41% · backtracks 0

<details><summary>Token probabilities (199 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.49 · `మ` 0.84 · `చ` 0.78 · `్రి` 2.1e-5✱ · `య` 0.03✱ · `్` 7.3e-3✱ · `న` 0.47 · `న్` 0.03✱ · `␣ల` 0.35 · `ఘ` 2.0e-4✱ · `ు` 0.97 · `గ` 0.06 · `్రీ` 0.03✱ · `వ` 0.50 · `్` 6.6e-4✱ · `ణ` 0.73 · `్య` 0.07✱ · `్` 0.04✱ · `ర` 4.4e-7✱ · `ణ` 8.8e-3✱ · `గ` 3.3e-3✱ · `ణ` 0.04✱ · `ము` 0.15✱ · `న` 0.08✱ · `␣చే` 4.8e-3✱ · `ర` 0.17✱ · `న్` 0.01✱ · `తి` 2.1e-3✱ · `ర` 7.6e-4✱ · `న్` 0.03✱ · `తి` 0.02✱ · `ర` 0.03✱ · `్` 2.3e-3✱ · `మ` 0.21✱ · `ల` 0.05✱ · `య` 0.03✱ · `్` 0.45 · `ని` 0.20 · `ర` 0.04✱ · `్` 0.04✱ · `⏎` 0.23 forced |
| 2 | `సీ` 0.66 · `మ` 1.7e-4✱ · `ల` 0.27 · `్యా` 7.4e-3✱ · `ణ` 0.03 · `్య` 0.10 · `ు` 0.18 · `న్` 0.10 · `␣ర` 0.19 · `ణ` 0.03✱ · `స్థ` 0.02✱ · `ల` 0.86 · `్య` 1.8e-4✱ · `్` 0.28 · `న` 0.40✱ · `్` 0.01✱ · `చ` 0.05✱ · `ెర` 1.2e-3✱ · `ల` 0.05✱ · `య` 0.21✱ · `ె` 7.0e-3✱ · `న` 0.25✱ · `␣హ` 0.01✱ · `రి` 0.28 · `ణ` 0.04 · `్య` 0.34 · `్` 0.46 · `న` 0.43 · `్` 0.04✱ · `చ` 0.17 · `ెర` 0.05✱ · `్` 0.05✱ · `మ` 0.25✱ · `ల` 0.67 · `య` 0.78 · `్` 0.95 · `ని` 0.80 · `ర` 0.83 · `్` 0.99 · `న` 6.5e-5✱ · `్` 0.25✱ · `తి` 0.01✱ · `ర` 0.52 · `న్` 0.05✱ · `తి` 0.82 · `ర` 0.85 · `్` 0.96 · `⏎` 0.64 forced |
| 3 | `త` 0.02 · `్రా` 8.8e-3✱ · `మ` 1.9e-3✱ · `క` 0.32 · `్య` 0.05✱ · `్` 0.68 · `న` 0.92 · `్` 0.34 · `చ` 0.64 · `ెర` 0.52 · `్` 0.21✱ · `మ` 0.50 · `ల` 0.93 · `్య` 6.5e-3✱ · `్` 0.81 · `న` 0.76 · `్` 0.68 · `చ` 0.64 · `ెర` 0.63 · `ల` 0.34 · `్య` 0.06✱ · `్` 0.71 · `న` 0.90 · `న్` 0.25 · `␣ర` 0.26 · `ణ` 0.09✱ · `ము` 0.10✱ · `న` 0.77 · `␣ని` 0.08 · `ల` 0.10 · `చి` 0.36 · `న్` 0.01✱ · `␣ర` 0.19 · `క్ష` 0.74 · `్య` 0.12✱ · `్` 0.31 · `న` 0.93 · `త` 3.4e-3✱ · `న్` 0.35 · `తి` 0.63 · `ర` 0.99 · `్` 0.68 · `మ` 0.26✱ · `ల` 0.99 · `య` 0.99 · `్` 0.99 · `ని` 0.96 · `ర` 0.99 · `్` 1.00 · `⏎` 1.00 forced |
| 4 | `వ` 0.05 · `్యా` 5.5e-3✱ · `మ` 1.4e-3✱ · `న` 0.10✱ · `్య` 0.67 · `్` 0.95 · `న` 0.99 · `్` 0.81 · `చ` 0.98 · `ెర` 0.99 · `్` 0.59 · `మ` 0.99 · `ల` 1.00 · `్య` 0.94 · `్` 0.98 · `న` 0.88 · `్` 0.58 · `చ` 0.99 · `ెర` 0.99 · `ల` 0.95 · `్య` 0.83 · `్` 0.92 · `న` 0.96 · `న్` 0.88 · `␣ల` 0.66 · `్` 5.0e-5✱ · `క` 0.44 · `్య` 0.03✱ · `్` 0.86 · `న` 0.96 · `న` 0.09✱ · `␣ని` 0.08 · `వ` 0.43 · `ృ` 0.10✱ · `థ` 7.0e-3✱ · `ి` 0.17✱ · `ర` 0.07✱ · `య` 2.4e-3✱ · `ె` 0.07✱ · `న` 0.51 · `్` 1.1e-3✱ · `␣హ` 0.16✱ · `ర` 0.02✱ · `్య` 0.02✱ · `్` 0.98 · `న` 0.98 · `్` 0.64 · `చ` 0.77 · `ెర` 0.96 · `న్` 0.02✱ · `తి` 0.97 · `ర` 1.00 · `్` 0.95 · `మ` 0.14✱ · `ల` 1.00 · `య` 1.00 · `్` 1.00 · `ని` 0.99 · `ర` 1.00 · `్` 0.99 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 189 tokens · 38.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వాయుప్రియ్నం తలప్యెన్ ల్వకనియెన వనమ్ర్య్వన్రయెన్ ముర్యునైన్ వన్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 2 | మాయాకల్యాణమై త్వం ల్వకనియెన తలప్య్న్మర్యునైన్ వన్ త్వమైన్ వన్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 3 | జైయెన్ వాయుప్రియుం తల్య్న వనమరయెనల్వ్క్నైన్ వనమ్ర్యున్ వనన్ వన్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 4 | భైయమ్య్నైన్ తల్య్న ల్వక్నైన్ వనమరయెన వన్ త్వమ్య్న వన్ త్వమ్య్న వన్ వన్ | `UUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 3% · single-akshara words 30% · repeated lines 0 · mean token probability (geometric) 0.104 · model's first choice kept 52% · constraint overrode 40% · backtracks 0

<details><summary>Token probabilities (189 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.35 · `ాయ` 1.00 · `ు` 1.00 · `ప` 0.01✱ · `్రి` 0.03✱ · `య` 3.4e-3✱ · `్` 1.8e-3✱ · `న` 0.28 · `ం` 0.01✱ · `␣త` 0.05✱ · `ల` 0.19 · `ప` 0.04✱ · `్య` 3.0e-4✱ · `ె` 0.08 · `న్` 0.08✱ · `␣ల` 0.16 · `్వ` 1.2e-6✱ · `క` 3.6e-3✱ · `ని` 0.04 · `య` 2.1e-3✱ · `ె` 0.32 · `న` 0.09✱ · `␣వ` 0.01✱ · `న` 0.07✱ · `మ` 0.13✱ · `్ర` 9.8e-3✱ · `్య` 3.1e-3✱ · `్` 0.03✱ · `వ` 9.8e-4✱ · `న` 0.02✱ · `్ర` 1.4e-3✱ · `య` 0.04✱ · `ె` 0.03✱ · `న్` 0.20✱ · `␣ము` 1.6e-4✱ · `ర` 0.01✱ · `్య` 0.01✱ · `ు` 0.10 · `న` 0.18 · `ై` 0.06✱ · `న్` 0.02✱ · `␣వ` 5.3e-4✱ · `న` 0.43 · `్` 2.9e-5✱ · `⏎` 0.03 forced |
| 2 | `మ` 0.02 · `ాయ` 0.01✱ · `ా` 0.63 · `క` 0.08 · `ల` 0.19 · `్యా` 0.06✱ · `ణ` 0.80 · `మై` 0.06 · `␣త` 0.07 · `్వ` 0.12 · `ం` 0.51 · `␣ల` 0.06✱ · `్వ` 0.03✱ · `క` 0.97 · `ని` 0.62 · `య` 0.63 · `ె` 0.95 · `న` 0.31✱ · `␣త` 0.04 · `ల` 0.28 · `ప` 0.81 · `్య` 0.97 · `్` 7.8e-3✱ · `న` 0.82 · `్` 1.6e-4✱ · `మ` 6.7e-3✱ · `ర` 0.25 · `్య` 0.84 · `ు` 0.55 · `న` 0.88 · `ై` 0.96 · `న్` 0.99 · `␣వ` 0.71 · `న` 0.99 · `్` 0.46 · `␣త` 4.5e-4✱ · `్వ` 0.52 · `మ` 0.05✱ · `ై` 0.07✱ · `న్` 0.78 · `␣వ` 0.25✱ · `న` 0.97 · `్` 0.37 · `⏎` 0.88 forced |
| 3 | `జ` 0.03 · `ై` 0.06✱ · `య` 7.2e-3✱ · `ె` 0.20 · `న్` 0.71 · `␣వ` 0.15 · `ాయ` 0.68 · `ు` 0.99 · `ప` 0.43 · `్రి` 0.96 · `య` 0.89 · `ు` 0.03✱ · `ం` 0.09 · `␣త` 0.44 · `ల` 0.93 · `్య` 6.2e-4✱ · `్` 0.04✱ · `న` 0.86 · `␣వ` 0.05✱ · `న` 0.96 · `మ` 0.82 · `ర` 6.2e-3✱ · `య` 0.02✱ · `ె` 0.34✱ · `న` 0.01✱ · `ల` 2.4e-4✱ · `్వ` 0.51 · `్` 1.2e-4✱ · `క` 0.99 · `్` 5.0e-6✱ · `న` 0.19✱ · `ై` 0.54 · `న్` 0.95 · `␣వ` 0.22 · `న` 0.98 · `మ` 0.50 · `్ర` 0.68 · `్య` 0.90 · `ు` 0.58 · `న` 0.96 · `్` 2.8e-3✱ · `␣వ` 0.43 · `న` 0.97 · `న్` 0.01✱ · `␣వ` 0.02✱ · `న` 0.98 · `్` 0.84 · `⏎` 1.00 forced |
| 4 | `భ` 0.13 · `ై` 0.53 · `య` 1.4e-6✱ · `మ` 0.13✱ · `్య` 0.02✱ · `్` 0.28 · `న` 0.75 · `ై` 0.21✱ · `న్` 0.97 · `␣త` 0.35 · `ల` 0.65 · `్య` 0.08✱ · `్` 0.71 · `న` 0.97 · `␣ల` 0.34 · `్వ` 0.97 · `క` 0.99 · `్` 8.7e-3✱ · `న` 0.85 · `ై` 0.86 · `న్` 0.99 · `␣వ` 0.78 · `న` 0.98 · `మ` 0.97 · `ర` 0.42✱ · `య` 0.61 · `ె` 0.72 · `న` 0.22✱ · `␣వ` 0.42 · `న` 0.56 · `్` 0.13✱ · `␣త` 0.63 · `్వ` 0.96 · `మ` 0.72 · `్య` 4.5e-3✱ · `్` 0.85 · `న` 0.98 · `␣వ` 0.05✱ · `న` 0.97 · `్` 0.68 · `␣త` 0.35 · `్వ` 0.66 · `మ` 0.82 · `్య` 0.08✱ · `్` 0.94 · `న` 0.99 · `␣వ` 0.86 · `న` 0.99 · `్` 0.84 · `␣వ` 1.0e-3✱ · `న` 0.99 · `్` 0.69 |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 172 tokens · 68.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వాయుప్రియ్నం తలించిన్ భయము విదిలగాయ్వాననిచ్యుడ్రమున్రో | `UUUUIUUIIIIIIUUIUUIUU` |
| 2 | గీయావన్యానమున్రుత్య్య్ఘృతమున లఘురమ్య్న్కృప్యుడెన్ దేవినిచ్యుడ్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 3 | మాయావిష్యం తలించిన్ జ్య్వ్మమున శిరసమున్య్న్మయ్న సంద్రమ్య్న్దగమ్యుడ్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 4 | శూయేంద్రమ్య్న్నమ్య్న లంకగ్య్న్సొమమున దయనిచ్యుడ్రమున్రుత్య్నతృప్యుడ్ | `UUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 7% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.057 · model's first choice kept 45% · constraint overrode 46% · backtracks 30

<details><summary>Token probabilities (172 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.35 · `ాయ` 1.00 · `ు` 1.00 · `ప` 0.01✱ · `్రి` 0.03✱ · `య` 3.4e-3✱ · `్` 1.8e-3✱ · `న` 0.28 · `ం` 0.01✱ · `␣త` 0.05✱ · `ల` 0.19 · `ించి` 0.07✱ · `న్` 7.9e-4✱ · `␣భ` 0.04✱ · `య` 0.18✱ · `ము` 0.51 · `␣వి` 0.09✱ · `ది` 0.10 · `ల` 0.85 · `గా` 9.1e-4✱ · `య` 0.11✱ · `్` 0.02✱ · `వా` 1.1e-3✱ · `న` 2.2e-4✱ · `ని` 2.6e-3✱ · `చ` 1.7e-4✱ · `్య` 0.03✱ · `ు` 0.59 · `డ` 0.03✱ · `్ర` 3.7e-3✱ · `ము` 0.03✱ · `న` 0.22✱ · `్రో` 1.4e-4✱ · `⏎` 0.10 forced |
| 2 | `గ` 0.17 · `ీ` 0.03✱ · `యా` 2.2e-7✱ · `వ` 0.10 · `న` 0.43 · `్యా` 1.2e-4✱ · `న` 0.39 · `ము` 0.48 · `న` 0.25 · `్రు` 3.5e-4✱ · `త` 0.21 · `్య` 0.04✱ · `్య` 1.7e-3✱ · `్` 3.4e-4✱ · `ఘ` 4.7e-4✱ · `ృత` 1.4e-3✱ · `ము` 0.62 · `న` 0.52 · `␣ల` 0.23 · `ఘ` 4.4e-4✱ · `ు` 0.99 · `ర` 0.13 · `మ` 0.18✱ · `్య` 0.26 · `్` 0.01✱ · `న` 0.30 · `్` 9.0e-5✱ · `క` 2.3e-3✱ · `ృ` 9.6e-3✱ · `ప` 0.60 · `్య` 0.09✱ · `ు` 0.27 · `డ` 0.62 · `ె` 0.05✱ · `న్` 0.21✱ · `␣ద` 4.2e-3✱ · `ే` 0.41 · `వి` 0.19✱ · `ని` 0.05✱ · `చ` 0.13✱ · `్య` 0.54 · `ు` 0.93 · `డ` 0.92 · `్` 5.6e-6✱ · `⏎` 0.37 forced |
| 3 | `మ` 0.03 · `ాయ` 5.6e-3✱ · `ా` 0.65 · `వి` 0.44 · `ష` 0.06 · `్యం` 8.5e-3✱ · `␣త` 0.09 · `ల` 0.28✱ · `ించి` 0.49 · `న్` 0.95 · `␣జ` 0.02 · `్య` 0.21✱ · `్వ` 4.0e-5✱ · `్` 4.3e-6✱ · `మ` 0.02✱ · `ము` 0.09 · `న` 0.64 · `␣శి` 0.02 · `ర` 0.53 · `స` 0.04✱ · `ము` 0.76 · `న` 0.67 · `్య` 4.2e-4✱ · `్` 0.05✱ · `న` 0.51 · `్` 0.11 · `మ` 0.03✱ · `య` 0.17 · `్` 0.18✱ · `న` 0.65 · `␣స` 0.02 · `ంద్ర` 0.01✱ · `మ` 0.06✱ · `్య` 0.02✱ · `్` 0.51 · `న` 0.85 · `్` 0.26 · `ద` 0.09 · `గ` 3.2e-3✱ · `మ` 0.47 · `్య` 0.67 · `ు` 0.53 · `డ` 0.87 · `్` 0.14✱ · `⏎` 0.99 forced |
| 4 | `శ` 0.15 · `ూ` 0.02✱ · `యే` 3.3e-7✱ · `ంద్ర` 0.26 · `మ` 0.08 · `్య` 0.58 · `్` 0.96 · `న` 0.99 · `్` 0.85 · `న` 0.11 · `మ` 0.05 · `్య` 0.44 · `్` 0.72 · `న` 0.96 · `␣ల` 0.35 · `ంక` 0.59 · `గ` 0.08✱ · `్య` 1.0e-5✱ · `్` 0.58 · `న` 0.95 · `్` 0.23✱ · `స` 0.02✱ · `ొ` 7.4e-4✱ · `మ` 0.32 · `ము` 0.11✱ · `న` 0.94 · `␣ద` 0.07 · `య` 0.02✱ · `ని` 0.04✱ · `చ` 0.87 · `్య` 0.99 · `ు` 0.96 · `డ` 0.98 · `్ర` 0.16✱ · `ము` 0.65 · `న` 0.75 · `్రు` 2.2e-3✱ · `త` 0.73 · `్య` 0.85 · `్` 0.53 · `న` 0.19 · `త` 0.02✱ · `ృ` 0.12 · `ప` 0.22 · `్య` 0.94 · `ు` 0.80 · `డ` 0.98 · `్` 0.79 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 160 tokens · 70.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీరామున్ లంకనుగ్రుంచి రగిణ వలమున్ర్య్జింతునుంబుగ్యునుంబున్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 2 | సీరీదై నిల్యెనున్రుంభ్ర్ధ్రిక నరదెనుగెన్ర్య్జింతునుంబుగ్యునుంబున్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 3 | ప్రారుణ్భేదించి సత్యం దలచి రణమునక్ర్య్ణత్ర గల్యున్ర్య్జిమౌంబున్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 4 | పారవ్యంకల్యునై రక్ష్య్ణనుని త్రయమునగ్య్ణత్ర దైవమ్మునౌంబున్ | `UUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 6% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.053 · model's first choice kept 39% · constraint overrode 49% · backtracks 30

<details><summary>Token probabilities (160 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.14 · `్రీ` 0.99 · `రా` 0.76 · `ము` 0.58 · `న్` 0.02✱ · `␣ల` 0.42 · `ం` 0.43 · `క` 8.9e-3✱ · `ను` 0.04 · `గ` 3.6e-4✱ · `్రు` 5.0e-3✱ · `ంచి` 0.17 · `␣ర` 0.25 · `గి` 8.4e-4✱ · `ణ` 0.22 · `␣వ` 6.1e-4✱ · `ల` 0.18 · `ము` 0.19 · `న` 0.22✱ · `్ర` 6.2e-5✱ · `్య` 2.9e-4✱ · `్` 2.5e-3✱ · `జి` 1.1e-3✱ · `ం` 0.07✱ · `తు` 0.06✱ · `ను` 0.03✱ · `ం` 4.4e-3✱ · `బు` 7.4e-3✱ · `గ` 2.6e-3✱ · `్య` 2.0e-3✱ · `ు` 0.37 · `ను` 0.03✱ · `ం` 0.12✱ · `బు` 0.34✱ · `న` 1.5e-3✱ · `్` 9.9e-5✱ · `⏎` 0.56 forced |
| 2 | `సీ` 0.84 · `రీ` 2.6e-7✱ · `ద` 0.25 · `ై` 0.24 · `␣ని` 0.02 · `ల` 0.11✱ · `్య` 9.4e-7✱ · `ె` 0.29 · `ను` 0.60 · `న` 6.6e-3✱ · `్రు` 1.3e-3✱ · `ం` 0.04 · `భ` 0.07✱ · `్ర` 0.03✱ · `్` 1.3e-3✱ · `ధ` 0.05 · `్ర` 0.14✱ · `ిక` 1.1e-3✱ · `␣న` 8.5e-3✱ · `ర` 0.26 · `ద` 0.04 · `ె` 0.03✱ · `ను` 0.17 · `గ` 0.04 · `ె` 0.04✱ · `న` 0.08✱ · `్ర` 6.6e-3✱ · `్య` 0.02✱ · `్` 0.66 · `జి` 0.91 · `ం` 0.96 · `తు` 0.98 · `ను` 0.61 · `ం` 0.98 · `బు` 0.98 · `గ` 0.42 · `్య` 0.99 · `ు` 1.00 · `ను` 0.97 · `ం` 0.99 · `బు` 0.96 · `న` 0.96 · `్` 0.99 · `⏎` 0.99 forced |
| 3 | `ప` 0.09 · `్రా` 0.03✱ · `రుణ` 5.5e-6✱ · `్` 0.18 · `భ` 0.16 · `ే` 0.15 · `ద` 0.09 · `ించి` 0.03✱ · `␣స` 0.02 · `త్య` 0.10✱ · `ం` 0.09✱ · `␣ద` 4.7e-3✱ · `ల` 5.8e-3✱ · `చి` 0.29 · `␣ర` 0.38 · `ణ` 5.7e-3✱ · `ము` 0.49 · `న` 0.72 · `క` 0.02✱ · `్ర` 1.3e-4✱ · `్య` 0.05✱ · `్` 0.80 · `ణ` 5.0e-3✱ · `త` 0.02✱ · `్ర` 3.7e-3✱ · `␣గ` 0.02✱ · `ల` 0.10 · `్య` 9.8e-3✱ · `ు` 0.78 · `న` 0.09✱ · `్ర` 0.03✱ · `్య` 0.96 · `్` 0.99 · `జి` 1.00 · `మ` 6.3e-4✱ · `ౌ` 0.03✱ · `ం` 0.50 · `బు` 0.97 · `న` 0.66 · `్` 0.99 · `⏎` 1.00 forced |
| 4 | `ప` 0.02 · `ార` 0.03✱ · `వ` 0.14 · `్యం` 1.4e-4✱ · `క` 0.17 · `ల` 0.06✱ · `్య` 0.01✱ · `ు` 0.63 · `న` 0.21✱ · `ై` 0.12✱ · `␣ర` 0.36 · `క్ష` 0.75 · `్య` 0.04✱ · `్` 7.9e-5✱ · `ణ` 0.06✱ · `ను` 0.02✱ · `ని` 3.4e-3✱ · `␣త` 0.02✱ · `్ర` 0.12 · `య` 0.40 · `ము` 0.27 · `న` 0.73 · `గ` 0.01✱ · `్య` 0.12✱ · `్` 0.07✱ · `ణ` 0.06✱ · `త` 0.49 · `్ర` 0.91 · `␣ద` 0.14 · `ై` 0.20 · `వ` 0.94 · `మ్ము` 0.04✱ · `న` 0.60 · `ౌ` 0.05✱ · `ం` 0.89 · `బు` 1.00 · `న` 0.99 · `్` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 157 tokens · 10.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వాయుప్రియ్నం త్రిభువ్నేశ్వరుని మతిని చేర్య్ర్భవ్యునిన్తిం హనుమ్యా | `UUUUIUUIIIIIIUUIUUIUU` |
| 2 | సాయిల్యానచ్యుతన్ సూర్య్ర్సనమును తలమున్య్య్జన్యునిన్తిం కనన్తీ | `UUUUIUUIIIIIIUUIUUIUU` |
| 3 | సాయిల్యానచ్యుతన్ అగ్న్ర్జనమును సముదర్ర్భ్జన్యునిన్తిం గమయ్యా | `UUUUIUUIIIIIIUUIUUIUU` |
| 4 | సాయిల్యానచ్యుతన్ లంక్ర్జనమును తపమున్య్య్జన్యునిన్తిం ద్రువంగా | `UUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 6% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.102 · model's first choice kept 56% · constraint overrode 39% · backtracks 0

<details><summary>Token probabilities (157 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.35 · `ాయ` 1.00 · `ు` 1.00 · `ప` 0.01✱ · `్రి` 0.03✱ · `య` 3.4e-3✱ · `్` 1.8e-3✱ · `న` 0.28 · `ం` 0.01✱ · `␣త` 0.05✱ · `్రి` 0.06 · `భు` 0.46 · `వ` 0.98 · `్` 4.7e-5✱ · `న` 0.91 · `ేశ` 0.02✱ · `్వ` 0.30✱ · `రు` 0.86 · `ని` 0.92 · `␣మ` 0.02✱ · `తి` 0.01✱ · `ని` 0.36 · `␣చే` 0.08 · `ర` 0.08✱ · `్య` 4.2e-5✱ · `్ర` 7.9e-6✱ · `్` 4.4e-4✱ · `భ` 4.9e-3✱ · `వ` 9.8e-3✱ · `్య` 5.1e-4✱ · `ు` 0.24✱ · `ని` 0.16✱ · `న్` 8.8e-4✱ · `తి` 2.7e-3✱ · `ం` 8.1e-3✱ · `␣హ` 4.7e-4✱ · `ను` 0.90 · `మ` 0.29✱ · `్యా` 1.0e-3✱ · `⏎` 0.55 forced |
| 2 | `స` 0.42 · `ాయి` 1.4e-4✱ · `ల` 0.31 · `్యా` 0.01✱ · `న` 0.28 · `చ` 7.7e-3✱ · `్య` 0.16✱ · `ు` 0.95 · `త` 0.92 · `న్` 0.12 · `␣స` 0.21 · `ూర్` 8.9e-4✱ · `య` 0.90 · `్ర` 1.1e-4✱ · `్` 2.5e-4✱ · `స` 1.1e-3✱ · `న` 0.39 · `ము` 0.34 · `ను` 0.33 · `␣త` 0.15✱ · `ల` 0.06✱ · `ము` 0.18 · `న` 0.46 · `్య` 6.5e-4✱ · `్య` 0.02✱ · `్` 3.8e-3✱ · `జ` 0.03✱ · `న` 0.15✱ · `్య` 9.7e-3✱ · `ు` 0.34 · `ని` 0.48 · `న్` 0.59 · `తి` 0.92 · `ం` 0.99 · `␣క` 0.03 · `న` 0.03✱ · `న్` 0.10✱ · `తీ` 0.02 · `⏎` 0.86 forced |
| 3 | `స` 0.37 · `ాయి` 2.8e-4✱ · `ల` 0.87 · `్యా` 0.87 · `న` 0.96 · `చ` 0.65 · `్య` 0.97 · `ు` 1.00 · `త` 0.99 · `న్` 0.98 · `␣అ` 0.01 · `గ్` 0.78 · `న` 5.2e-3✱ · `్ర` 0.11 · `్` 0.73 · `జ` 0.02✱ · `న` 0.04✱ · `ము` 0.64 · `ను` 0.64 · `␣స` 0.21 · `ము` 0.98 · `ద` 0.03✱ · `ర` 0.20✱ · `్ర` 0.15✱ · `్` 0.76 · `భ` 0.08 · `్` 6.4e-5✱ · `జ` 0.13✱ · `న` 0.46 · `్య` 0.15✱ · `ు` 0.92 · `ని` 0.94 · `న్` 0.99 · `తి` 0.99 · `ం` 1.00 · `␣గ` 0.17 · `మ` 0.80 · `య` 0.02✱ · `్యా` 0.03 · `⏎` 0.97 forced |
| 4 | `స` 0.70 · `ాయి` 0.99 · `ల` 1.00 · `్యా` 1.00 · `న` 1.00 · `చ` 1.00 · `్య` 1.00 · `ు` 1.00 · `త` 1.00 · `న్` 1.00 · `␣ల` 0.86 · `ం` 0.50 · `క` 0.04✱ · `్ర` 0.34 · `్` 0.91 · `జ` 0.04 · `న` 0.92 · `ము` 0.93 · `ను` 0.89 · `␣త` 0.11 · `ప` 0.17 · `ము` 0.03✱ · `న` 0.52 · `్య` 0.95 · `్య` 0.93 · `్` 0.98 · `జ` 0.97 · `న` 0.99 · `్య` 1.00 · `ు` 1.00 · `ని` 1.00 · `న్` 1.00 · `తి` 1.00 · `ం` 1.00 · `␣ద` 0.03✱ · `్రు` 0.17✱ · `వ` 0.36 · `ంగా` 0.03✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 160 tokens · 14.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లియ్ ప్రేమక్రుడెన్ అమ్య్మ్తమున తలచుకొన్య్మ్తయ్నమున్ స్తర్యునన్మన్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 2 | తల్లిక్రాంతిన్ కరుణ్యున్య్న నిరమున నినుత్య్నన్ తలప్యున్య్న నిత్యం | `UUUUIUUIIIIIIUUIUUIUU` |
| 3 | తల్లియ్ ఆశ్రయ్నమున్య్నన్ తలచుకమున తల్య్న్తయ్నమున్ సత్యమున్మున్ | `UUUUIUUIIIIIIUUIUUIUU` |
| 4 | తల్లియ్ మమ్రంన నిత్య్య్నన్ తలచుకమున తల్య్నన్ నిరంతర్య్నమున్ శా | `UUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 4% · single-akshara words 4% · repeated lines 0 · mean token probability (geometric) 0.083 · model's first choice kept 51% · constraint overrode 39% · backtracks 0

<details><summary>Token probabilities (160 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.80 · `ల్లి` 0.70 · `య` 7.0e-3✱ · `్` 1.3e-4✱ · `␣ప్రేమ` 0.83 · `క` 0.03✱ · `్రు` 1.4e-7✱ · `డ` 0.27 · `ె` 0.13✱ · `న్` 0.14 · `␣అమ` 0.02 · `్య` 8.6e-5✱ · `్` 1.7e-3✱ · `మ` 0.43 · `్` 2.0e-4✱ · `త` 5.8e-3✱ · `ము` 0.30 · `న` 0.23 · `␣త` 6.2e-3✱ · `ల` 0.74 · `చు` 0.06 · `కొ` 0.09 · `న` 0.05✱ · `్య` 1.5e-5✱ · `్` 7.8e-3✱ · `మ` 0.01✱ · `్` 4.6e-3✱ · `త` 0.03✱ · `య` 2.1e-3✱ · `్` 0.73 · `న` 8.2e-3✱ · `ము` 8.0e-3✱ · `న్` 0.01✱ · `␣` 1.4e-4✱ · `స్త` 0.07✱ · `ర` 0.03 · `్య` 3.0e-3✱ · `ు` 0.11 · `న` 0.14✱ · `న్` 4.8e-3✱ · `మ` 1.0e-3✱ · `న్` 0.02 · `⏎` 0.97 forced |
| 2 | `త` 0.41 · `ల్లి` 0.85 · `క` 0.03 · `్రా` 9.8e-6✱ · `ంతి` 0.58 · `న్` 0.03✱ · `␣క` 0.13 · `రుణ` 0.95 · `్య` 0.04✱ · `ు` 0.14 · `న` 0.40 · `్య` 1.9e-4✱ · `్` 0.55 · `న` 0.42 · `␣ని` 0.05✱ · `ర` 0.05✱ · `ము` 0.02✱ · `న` 0.73 · `␣ని` 0.20 · `ను` 0.08✱ · `త` 0.02 · `్య` 3.6e-3✱ · `్` 0.23✱ · `న` 0.68 · `న్` 0.12✱ · `␣త` 0.13 · `ల` 0.65 · `ప` 0.05✱ · `్య` 7.7e-3✱ · `ు` 0.69 · `న` 0.75 · `్య` 0.03✱ · `్` 0.88 · `న` 0.74 · `␣ని` 0.06 · `త్య` 0.23 · `ం` 0.02✱ · `⏎` 0.82 forced |
| 3 | `త` 0.85 · `ల్లి` 0.91 · `య` 0.12 · `్` 0.69 · `␣ఆ` 0.19 · `శ` 0.81 · `్ర` 0.27 · `య` 0.69 · `్` 2.9e-4✱ · `న` 0.77 · `ము` 0.05 · `న` 0.65 · `్య` 1.9e-3✱ · `్` 0.96 · `న` 0.98 · `న్` 4.1e-5✱ · `␣త` 0.04✱ · `ల` 0.53 · `చ` 0.03 · `ు` 0.09✱ · `క` 0.09 · `ము` 0.04✱ · `న` 0.73 · `␣త` 0.38 · `ల` 0.38 · `్య` 0.05✱ · `్` 0.51 · `న` 0.88 · `్` 6.6e-3✱ · `త` 0.02✱ · `య` 0.29 · `్` 0.96 · `న` 0.98 · `ము` 0.63 · `న్` 0.86 · `␣స` 0.07 · `త్య` 0.77 · `ము` 0.57 · `న్` 0.53 · `ము` 1.8e-3✱ · `న్` 0.81 · `⏎` 0.99 forced |
| 4 | `త` 0.97 · `ల్లి` 0.94 · `య` 0.25 · `్` 0.96 · `␣మ` 0.08✱ · `మ` 0.73 · `్ర` 3.6e-4✱ · `ం` 0.04✱ · `న` 0.18 · `␣ని` 0.09✱ · `త్య` 0.63 · `్య` 0.14✱ · `్` 0.66 · `న` 0.99 · `న్` 0.75 · `␣త` 0.26 · `ల` 0.88 · `చు` 0.15 · `క` 0.38 · `ము` 0.78 · `న` 0.79 · `␣త` 0.80 · `ల` 0.94 · `్య` 0.78 · `్` 0.89 · `న` 0.98 · `న్` 0.50 · `␣ని` 0.23 · `ర` 0.17✱ · `ంత` 0.34✱ · `ర` 0.97 · `్య` 0.04✱ · `్` 0.85 · `న` 0.99 · `ము` 0.09✱ · `న్` 0.98 · `␣శా` 7.0e-3✱ |

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

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 174 tokens · 32.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి ప్రేమన్ తల్లి దయ్యే మ్ర్వ్తొలకలమునికేన్ర్య్ధోతరంబున్రయెన్ర్య్ధో | `IIUUUIUUIIIIIIUUIUUIUU` |
| 2 | తొలి మమ్రోహం తులల్యంక్ర్య్ధులకలమున మెల్ల్ర్తొల్య్య్ధనోతర్ర్య్ధఓతర్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 3 | తొలి కౌగిల్యం కరుణ్యే క్వ్ధులకలమున నిత్య్ర్తొల్య్య్ధనోతర్ర్య్ధఓతర్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 4 | తొలి ఆశ్రయ్యం తులల్యంక్ర్య్ధులకలమున నిత్య్ర్తొల్య్య్ధనోతర్ర్య్ధఓతర్ | `IIUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 33% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.122 · model's first choice kept 59% · constraint overrode 36% · backtracks 0

<details><summary>Token probabilities (174 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.84 · `ొ` 2.2e-3✱ · `లి` 0.68 · `␣ప్రేమ` 0.08 · `న్` 3.4e-3✱ · `␣తల్లి` 0.09 · `␣ద` 0.05 · `య` 0.42 · `్య` 1.1e-5✱ · `ే` 0.24 · `␣మ` 0.07✱ · `్ర` 1.4e-7✱ · `్వ` 1.2e-5✱ · `్` 7.7e-4✱ · `త` 0.07✱ · `ొ` 6.7e-3✱ · `ల` 0.11 · `క` 0.08 · `ల` 0.09✱ · `ము` 0.04✱ · `ని` 0.02✱ · `కే` 0.03✱ · `న` 0.01✱ · `్ర` 1.2e-4✱ · `్య` 5.9e-3✱ · `్` 6.6e-3✱ · `ధ` 0.02✱ · `ో` 6.4e-3✱ · `త` 0.02✱ · `రం` 0.07✱ · `బు` 0.04✱ · `న` 0.01✱ · `్ర` 6.1e-4✱ · `య` 0.20✱ · `ె` 0.10✱ · `న` 0.03✱ · `్ర` 4.8e-3✱ · `్య` 0.56 · `్` 0.70 · `ధ` 0.86 · `ో` 0.94 · `⏎` 0.02 forced |
| 2 | `త` 0.41 · `ొ` 0.02✱ · `లి` 0.87 · `␣మ` 0.03 · `మ` 0.46 · `్రో` 1.6e-5✱ · `హం` 0.28 · `␣త` 0.13✱ · `ుల` 8.0e-3✱ · `ల` 0.01✱ · `్యం` 1.2e-3✱ · `క` 0.30✱ · `్ర` 1.6e-3✱ · `్య` 0.05✱ · `్` 0.66 · `ధ` 0.73 · `ుల` 5.4e-3✱ · `క` 0.11✱ · `ల` 0.68 · `ము` 0.69 · `న` 0.24 · `␣మె` 6.2e-3 · `ల్ల` 0.26 · `్ర` 5.9e-5✱ · `్` 9.3e-3✱ · `త` 0.01✱ · `ొ` 0.75 · `ల` 0.84 · `్య` 5.7e-4✱ · `్య` 0.07✱ · `్` 0.11✱ · `ధ` 0.83 · `నో` 1.3e-3✱ · `త` 0.59 · `ర` 0.03✱ · `్ర` 2.6e-3✱ · `్య` 0.44 · `్` 0.93 · `ధ` 0.98 · `ఓ` 7.9e-4✱ · `త` 5.9e-3✱ · `ర` 0.02✱ · `్` 1.1e-4✱ · `⏎` 0.18 forced |
| 3 | `త` 0.91 · `ొ` 0.46✱ · `లి` 0.84 · `␣క` 0.06 · `ౌ` 0.01✱ · `గి` 0.96 · `ల` 0.10✱ · `్యం` 0.17✱ · `␣క` 0.60 · `రుణ` 0.51 · `్య` 0.05✱ · `ే` 0.83 · `␣క` 0.12 · `్వ` 7.3e-4✱ · `్` 0.04✱ · `ధ` 0.54 · `ుల` 0.61 · `క` 0.86 · `ల` 0.98 · `ము` 0.93 · `న` 0.83 · `␣ని` 0.15 · `త్య` 0.39 · `్ర` 0.94 · `్` 0.92 · `త` 0.71 · `ొ` 0.99 · `ల` 0.97 · `్య` 0.62 · `్య` 0.83 · `్` 0.97 · `ధ` 0.97 · `నో` 0.52 · `త` 0.94 · `ర` 0.93 · `్ర` 0.92 · `్య` 0.97 · `్` 0.98 · `ధ` 1.00 · `ఓ` 0.55 · `త` 0.89 · `ర` 0.94 · `్` 0.91 · `⏎` 0.98 forced |
| 4 | `త` 0.99 · `ొ` 0.96 · `లి` 0.99 · `␣ఆ` 0.27 · `శ` 0.90 · `్ర` 0.86 · `య` 0.27✱ · `్యం` 1.1e-4✱ · `␣త` 0.35 · `ుల` 0.46 · `ల` 0.62 · `్యం` 0.87 · `క` 0.98 · `్ర` 0.98 · `్య` 0.99 · `్` 0.99 · `ధ` 0.99 · `ుల` 0.87 · `క` 0.97 · `ల` 0.99 · `ము` 0.96 · `న` 0.92 · `␣ని` 0.19 · `త్య` 0.89 · `్ర` 0.99 · `్` 0.99 · `త` 0.99 · `ొ` 1.00 · `ల` 1.00 · `్య` 0.96 · `్య` 0.99 · `్` 0.99 · `ధ` 1.00 · `నో` 0.93 · `త` 1.00 · `ర` 0.97 · `్ర` 0.98 · `్య` 1.00 · `్` 1.00 · `ధ` 1.00 · `ఓ` 0.73 · `త` 0.94 · `ర` 0.99 · `్` 0.98 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 178 tokens · 64.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మహరుష్యంబున్రు రక్షించ్యము లొక దరిచేత్ర్య్మల్య్నినిత్యామునుంబుల్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 2 | వహియెద్యాకశ్యమున్రుగ్య్య్వనమున భయమున్య్న్వాళ్య్నినిత్యామునుంబుల్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 3 | వహనగ్య్నమ్య్న్రుప్య్య్మలయ్నిన్య్న్వనమున భయమున్య్న్వాళ్య్నినిత్యామునుంబుల్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 4 | వహియెద్యాకశ్యమున్రుగ్య్య్వనమున రఘుమల్య్న్భయ్య్నితన్బుల్నితన్బుల్ | `IIUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 10% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.094 · model's first choice kept 56% · constraint overrode 38% · backtracks 0

<details><summary>Token probabilities (178 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.03✱ · `హ` 0.56 · `రు` 6.4e-3✱ · `ష` 0.35 · `్యం` 6.7e-3✱ · `బు` 0.74 · `న` 0.44 · `్రు` 4.5e-5✱ · `␣ర` 0.03 · `క్ష` 0.60 · `ించ` 0.21✱ · `్య` 2.9e-5✱ · `ము` 1.8e-3✱ · `␣ల` 0.02✱ · `ొ` 2.3e-4✱ · `క` 0.03✱ · `␣ద` 0.04✱ · `రి` 0.02✱ · `చే` 0.14 · `త` 0.30 · `్ర` 1.4e-5✱ · `్య` 7.9e-4✱ · `్` 4.5e-4✱ · `మ` 0.12✱ · `ల` 2.3e-3✱ · `్య` 4.0e-3✱ · `్` 0.10✱ · `ని` 0.02✱ · `ని` 1.7e-3✱ · `త` 1.9e-4✱ · `్యా` 0.01✱ · `ము` 7.2e-3✱ · `ను` 2.6e-3✱ · `ం` 3.3e-3✱ · `బు` 0.06✱ · `ల` 4.5e-3✱ · `్` 8.4e-4✱ · `⏎` 0.23 forced |
| 2 | `వ` 0.07 · `హి` 1.1e-4✱ · `య` 0.07✱ · `ె` 0.45 · `ద` 0.06✱ · `్యా` 2.6e-4✱ · `క` 0.02 · `శ` 0.49 · `్య` 0.09✱ · `ము` 0.24 · `న` 0.27 · `్రు` 0.03✱ · `గ` 3.8e-5✱ · `్య` 4.4e-3✱ · `్య` 0.03✱ · `్` 2.4e-3✱ · `వ` 3.3e-3✱ · `న` 0.18 · `ము` 0.39 · `న` 0.52 · `␣భ` 0.03✱ · `య` 0.67 · `ము` 0.67 · `న` 0.22✱ · `్య` 1.8e-4✱ · `్` 0.03✱ · `న` 0.46 · `్వ` 5.9e-5✱ · `ా` 0.30 · `ళ` 0.04 · `్య` 0.48 · `్` 0.61 · `ని` 0.49 · `ని` 0.66 · `త` 0.91 · `్యా` 0.99 · `ము` 0.99 · `ను` 0.86 · `ం` 0.99 · `బు` 0.99 · `ల` 0.97 · `్` 1.00 · `⏎` 0.99 forced |
| 3 | `వ` 0.04 · `హ` 6.9e-3✱ · `న` 6.6e-3✱ · `గ` 0.01✱ · `్య` 6.5e-3✱ · `్` 0.30 · `న` 0.66 · `మ` 0.10✱ · `్య` 0.28 · `్` 0.64 · `న` 0.70 · `్రు` 0.05✱ · `ప` 0.06✱ · `్య` 0.07✱ · `్య` 0.43 · `్` 0.92 · `మ` 0.06 · `ల` 0.45 · `య` 0.04✱ · `్` 0.51 · `ని` 0.44 · `న` 0.18✱ · `్య` 0.03✱ · `్` 0.85 · `న` 0.81 · `్వ` 0.06✱ · `న` 1.6e-3✱ · `ము` 0.81 · `న` 0.90 · `␣భ` 0.32 · `య` 0.92 · `ము` 0.91 · `న` 0.95 · `్య` 0.97 · `్` 0.98 · `న` 0.99 · `్వ` 0.82 · `ా` 0.97 · `ళ` 0.99 · `్య` 1.00 · `్` 1.00 · `ని` 0.99 · `ని` 0.80 · `త` 1.00 · `్యా` 1.00 · `ము` 1.00 · `ను` 1.00 · `ం` 1.00 · `బు` 1.00 · `ల` 1.00 · `్` 1.00 · `⏎` 1.00 forced |
| 4 | `వ` 0.06 · `హి` 0.16 · `య` 0.93 · `ె` 0.99 · `ద` 0.97 · `్యా` 0.95 · `క` 0.97 · `శ` 0.99 · `్య` 0.98 · `ము` 0.99 · `న` 0.99 · `్రు` 0.99 · `గ` 0.97 · `్య` 1.00 · `్య` 0.99 · `్` 0.99 · `వ` 0.99 · `న` 0.99 · `ము` 1.00 · `న` 1.00 · `␣ర` 0.46 · `ఘ` 2.4e-3✱ · `ు` 0.99 · `మ` 0.16 · `ల` 0.07 · `్య` 0.78 · `్` 0.98 · `న` 0.03✱ · `్` 8.8e-4✱ · `భ` 1.0e-3✱ · `య` 0.90 · `్య` 3.0e-3✱ · `్` 0.92 · `ని` 0.44 · `త` 0.56 · `న్` 1.2e-4✱ · `బు` 0.15 · `ల` 0.96 · `్` 0.98 · `ని` 1.1e-5✱ · `త` 0.61 · `న్` 8.3e-3✱ · `బు` 0.81 · `ల` 0.99 · `్` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 161 tokens · 44.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రిరుమాయణ్యుడ్యె లంకాన్వ్వృతమున ధిరమైన్ శ్రేయశః సాగెనుభ్యా | `IIUUUIUUIIIIIIUUIUUIUU` |
| 2 | తరుణిల్యాకశ్రయుల్యా తపమును దహయెన్య్య్ధన్యమున్రుప్యతైః శిర్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 3 | శరణం కోరిన్యి చిన్నియ్య్య్శయమున సముదర్ధ్వ్సన్య్న రక్షించునందున్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 4 | భ్రృరిమయ్య్యుడ్యే నమస్కార్య్న్యె లభయమున సుఖ్య్న్యెన్య్య్ధనః కీర్తియేనన్ | `IIUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 5% · single-akshara words 5% · repeated lines 0 · mean token probability (geometric) 0.041 · model's first choice kept 32% · constraint overrode 50% · backtracks 30

<details><summary>Token probabilities (161 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.22✱ · `్రి` 2.8e-3✱ · `రు` 0.18✱ · `మ` 0.22 · `ాయ` 0.44 · `ణ` 0.28 · `్య` 2.9e-4✱ · `ు` 0.44 · `డ` 0.11✱ · `్య` 4.4e-3✱ · `ె` 0.22 · `␣ల` 0.26 · `ంక` 0.56 · `ాన` 0.04✱ · `్వ` 6.3e-4✱ · `్వ` 8.0e-4✱ · `ృ` 5.0e-3✱ · `త` 0.04✱ · `ము` 0.19 · `న` 0.36 · `␣ధ` 3.2e-3✱ · `ి` 0.09✱ · `ర` 0.12✱ · `మై` 0.32 · `న్` 7.7e-3✱ · `␣శ` 1.4e-4✱ · `్రే` 8.7e-3✱ · `య` 0.73 · `శ` 0.09✱ · `ః` 0.08 · `␣సా` 4.5e-5✱ · `గ` 0.42 · `ె` 0.81 · `ను` 0.88 · `భ` 2.0e-4✱ · `్యా` 6.6e-3✱ · `⏎` 0.02 forced |
| 2 | `త` 0.02✱ · `రుణ` 0.07✱ · `ి` 0.68 · `ల` 0.02✱ · `్యా` 5.0e-4✱ · `క` 0.02 · `శ` 0.32 · `్ర` 0.10✱ · `యు` 0.03 · `ల` 0.06 · `్యా` 3.9e-3✱ · `␣త` 0.05 · `ప` 0.28 · `ము` 0.19 · `ను` 0.43 · `␣ద` 5.8e-3 · `హ` 0.67 · `య` 7.4e-3✱ · `ె` 0.11✱ · `న` 0.08✱ · `్య` 3.0e-5✱ · `్య` 4.8e-3✱ · `్` 1.0e-4✱ · `ధ` 8.7e-3✱ · `న` 0.14 · `్య` 4.3e-3✱ · `ము` 0.20 · `న` 0.40 · `్రు` 3.7e-5✱ · `ప` 0.22 · `్య` 0.09✱ · `త` 0.13✱ · `ై` 0.19 · `ః` 0.03✱ · `␣శి` 0.04✱ · `ర` 0.80 · `్` 1.0e-7✱ · `⏎` 3.0e-4 forced |
| 3 | `శ` 0.07 · `రణ` 0.05✱ · `ం` 0.05 · `␣కో` 0.83 · `రి` 0.80 · `న` 0.73 · `్య` 3.6e-4✱ · `ి` 0.07 · `␣చి` 0.02 · `న్ని` 0.13 · `య` 0.07 · `్య` 0.04✱ · `్య` 0.04✱ · `్` 0.05✱ · `శ` 0.13✱ · `య` 0.01✱ · `ము` 0.45 · `న` 0.57 · `␣స` 0.03 · `ము` 0.18✱ · `ద` 0.05✱ · `ర` 0.29✱ · `్` 1.3e-3✱ · `ధ` 0.30✱ · `్వ` 0.11✱ · `్` 2.1e-4✱ · `స` 1.9e-3✱ · `న` 0.15 · `్య` 0.26✱ · `్` 0.11 · `న` 0.46 · `␣ర` 9.7e-3✱ · `క్ష` 0.66 · `ించు` 0.34 · `న` 0.18✱ · `ందు` 0.04 · `న` 0.21 · `్` 3.4e-4✱ · `⏎` 0.01 forced |
| 4 | `భ` 0.06 · `్ర` 1.3e-3✱ · `ృ` 1.6e-5✱ · `రి` 3.5e-4✱ · `మ` 0.10 · `య` 0.07 · `్య` 0.09✱ · `్య` 0.23 · `ు` 0.10 · `డ` 0.18 · `్య` 0.84 · `ే` 0.17 · `␣న` 0.03 · `మ` 0.07 · `స్క` 0.61 · `ార` 0.59 · `్య` 0.14✱ · `్` 0.29 · `న` 0.63 · `్య` 9.0e-4✱ · `ె` 0.02✱ · `␣ల` 0.28 · `భ` 3.5e-3✱ · `య` 0.01✱ · `ము` 0.30✱ · `న` 0.46 · `␣సు` 0.04 · `ఖ` 0.63 · `్య` 0.04✱ · `్` 0.27 · `న` 0.74 · `్య` 0.03✱ · `ె` 0.07✱ · `న` 0.02✱ · `్య` 2.8e-4✱ · `్య` 0.32 · `్` 0.64 · `ధ` 0.21 · `న` 0.52 · `ః` 4.8e-3✱ · `␣క` 0.08 · `ీ` 0.39 · `ర్` 0.90 · `తి` 0.89 · `యే` 3.1e-3✱ · `న` 3.8e-3✱ · `న్` 8.2e-3✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 215 tokens · 56.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వనగమ్యుడ్యుడ్యుడెన్నుర్మ్య్భయమును త్వరితగ్య్ణ్వాహనుమ్య్భయ్భగవ్న్నన్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 2 | అనగన్యుడ్యుడ్యుడెన్నుర్మ్య్భయమును త్వరితగ్య్ణ్వాహనుమ్య్భయ్భగవ్న్నన్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 3 | చననగ్యుడ్యుడ్యుడెన్నుర్మ్య్సమరమును త్వరిత్య్ణ్సాహనుమ్య్భయ్భగవ్న్నన్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 4 | పృనుమగ్యుడ్యుడ్యుడెన్నుర్మ్య్లృఙుగమనుమ త్వర్య్ణ్సృహ్వనుమ్య్భయ్భగవ్న్నన్ | `IIUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 0% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.232 · model's first choice kept 70% · constraint overrode 26% · backtracks 30

<details><summary>Token probabilities (215 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.50 · `న` 4.9e-4✱ · `గ` 0.05 · `మ` 0.82 · `్య` 0.07✱ · `ు` 0.03✱ · `డ` 0.38✱ · `్య` 1.1e-3✱ · `ు` 0.22 · `డ` 0.08✱ · `్య` 0.50 · `ు` 0.88 · `డ` 0.82 · `ె` 3.8e-3✱ · `న` 0.22✱ · `్` 9.6e-4✱ · `ను` 0.04 · `ర` 4.4e-3✱ · `్` 2.1e-3✱ · `మ` 0.17 · `్య` 0.29 · `్` 1.2e-3✱ · `భ` 9.5e-3✱ · `య` 0.04✱ · `ము` 0.60 · `ను` 0.17✱ · `␣త` 0.05✱ · `్వ` 0.08✱ · `రి` 0.25✱ · `త` 0.92 · `గ` 0.15✱ · `్య` 7.3e-3✱ · `్` 0.01✱ · `ణ` 0.06 · `్వ` 0.03✱ · `ా` 0.30 · `హ` 0.02✱ · `ను` 0.06 · `మ` 0.21✱ · `్య` 0.15✱ · `్` 0.55 · `భ` 0.10✱ · `య` 0.44 · `్` 9.2e-4✱ · `భ` 0.08✱ · `గ` 0.07✱ · `వ` 0.56 · `్` 7.5e-3✱ · `న` 0.49 · `్` 0.22✱ · `న` 0.20 · `న్` 0.02✱ · `⏎` 0.71 forced |
| 2 | `అ` 0.05 · `న` 0.67 · `గ` 0.04✱ · `న` 0.22 · `్య` 8.8e-3✱ · `ు` 0.39 · `డ` 0.91 · `్య` 0.85 · `ు` 0.93 · `డ` 0.99 · `్య` 0.80 · `ు` 0.97 · `డ` 0.98 · `ె` 0.69 · `న` 0.93 · `్` 0.96 · `ను` 0.95 · `ర` 0.95 · `్` 0.96 · `మ` 0.98 · `్య` 0.99 · `్` 0.94 · `భ` 0.72 · `య` 0.95 · `ము` 0.99 · `ను` 0.92 · `␣త` 0.78 · `్వ` 0.96 · `రి` 1.00 · `త` 0.99 · `గ` 0.98 · `్య` 0.99 · `్` 0.98 · `ణ` 1.00 · `్వ` 0.97 · `ా` 0.98 · `హ` 0.95 · `ను` 0.97 · `మ` 0.99 · `్య` 0.98 · `్` 0.99 · `భ` 0.98 · `య` 0.95 · `్` 0.99 · `భ` 0.99 · `గ` 1.00 · `వ` 1.00 · `్` 0.99 · `న` 0.99 · `్` 0.70 · `న` 0.99 · `న్` 0.99 · `⏎` 0.98 forced |
| 3 | `చ` 0.01 · `న` 4.8e-4✱ · `న` 0.03 · `గ` 0.27 · `్య` 0.24 · `ు` 0.89 · `డ` 1.00 · `్య` 0.99 · `ు` 1.00 · `డ` 1.00 · `్య` 1.00 · `ు` 1.00 · `డ` 1.00 · `ె` 1.00 · `న` 0.99 · `్` 1.00 · `ను` 1.00 · `ర` 1.00 · `్` 1.00 · `మ` 1.00 · `్య` 1.00 · `్` 1.00 · `స` 2.6e-4✱ · `మ` 0.14 · `ర` 0.05✱ · `ము` 0.46 · `ను` 0.83 · `␣త` 0.90 · `్వ` 0.98 · `రి` 1.00 · `త` 1.00 · `్య` 2.2e-6✱ · `్` 0.69 · `ణ` 0.83 · `్` 4.5e-3✱ · `సా` 8.6e-4✱ · `హ` 0.67 · `ను` 0.86 · `మ` 0.99 · `్య` 0.99 · `్` 0.99 · `భ` 0.97 · `య` 0.95 · `్` 0.99 · `భ` 0.98 · `గ` 0.99 · `వ` 1.00 · `్` 0.99 · `న` 1.00 · `్` 0.90 · `న` 1.00 · `న్` 1.00 · `⏎` 1.00 forced |
| 4 | `ప` 0.03✱ · `ృ` 0.06✱ · `ను` 1.4e-6✱ · `మ` 0.28 · `గ` 0.04✱ · `్య` 0.95 · `ు` 0.99 · `డ` 1.00 · `్య` 1.00 · `ు` 1.00 · `డ` 1.00 · `్య` 1.00 · `ు` 1.00 · `డ` 1.00 · `ె` 1.00 · `న` 1.00 · `్` 1.00 · `ను` 1.00 · `ర` 1.00 · `్` 1.00 · `మ` 1.00 · `్య` 1.00 · `్` 0.99 · `ల` 0.28✱ · `ృ` 1.2e-5✱ · `ఙ` 0.08✱ · `ు` 1.4e-4✱ · `గ` 0.23 · `మ` 0.40 · `ను` 3.3e-3✱ · `మ` 0.26 · `␣త` 3.4e-3✱ · `్వ` 0.93 · `ర్య` 5.5e-4✱ · `్` 0.89 · `ణ` 0.92 · `్` 0.73 · `స` 0.03✱ · `ృ` 3.3e-3✱ · `హ` 0.34 · `్వ` 0.01✱ · `ను` 0.04✱ · `మ` 0.99 · `్య` 0.97 · `్` 1.00 · `భ` 0.99 · `య` 0.93 · `్` 0.99 · `భ` 0.98 · `గ` 0.99 · `వ` 1.00 · `్` 0.99 · `న` 1.00 · `్` 0.91 · `న` 1.00 · `న్` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 196 tokens · 39.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి ప్రేమంతే తలప్రియ్న్ర్దులెను తనుని తండ్ర్య్ధుల్ర్దృఢంభూతమై సుమ్ | `IIUUUIUUIIIIIIUUIUUIUU` |
| 2 | అలసిన్రోయ్నెన్ర్దులెన్ర్దృఢ్ధ్వ్హలకృతుని తులక్ర్మ్యన్ర్ధులెన్ర్దృఢ్ధ్వ్హలక్యం | `IIUUUIUUIIIIIIUUIUUIUU` |
| 3 | తొలి చూపున్రోయ్నెనవ్ర్ధుల్ర్ద్రుఢనరననలక్ర్మ్తొల్ర్దృఢోమ్యుత్తకారం | `IIUUUIUUIIIIIIUUIUUIUU` |
| 4 | తొలి మాటన్రోయ్నెనవ్ర్ధుల్ర్ద్రుఢనరననలక్ర్మ్తొల్ర్దృఢోమ్యుత్తకారం | `IIUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.114 · model's first choice kept 58% · constraint overrode 35% · backtracks 0

<details><summary>Token probabilities (196 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.84 · `ొ` 2.2e-3✱ · `లి` 0.68 · `␣ప్రేమ` 0.08 · `ంత` 8.5e-4✱ · `ే` 5.4e-3✱ · `␣త` 0.20✱ · `ల` 0.17✱ · `ప` 0.05✱ · `్రి` 7.4e-6✱ · `య` 1.6e-3✱ · `్` 4.1e-4✱ · `న` 0.24 · `్ర` 2.7e-5✱ · `్` 5.9e-5✱ · `ద` 5.8e-3✱ · `ుల` 1.4e-3✱ · `ె` 0.10 · `ను` 0.12 · `␣త` 0.03✱ · `ను` 7.2e-3✱ · `ని` 0.05✱ · `␣త` 0.03✱ · `ండ` 0.16 · `్ర` 0.23✱ · `్య` 0.02✱ · `్` 2.5e-3✱ · `ధ` 5.3e-3✱ · `ుల` 0.08✱ · `్ర` 1.7e-3✱ · `్` 0.09✱ · `ద` 0.09 · `ృ` 0.04✱ · `ఢ` 0.37 · `ం` 0.39 · `భ` 1.1e-3✱ · `ూ` 0.15 · `త` 0.36 · `మై` 0.05 · `␣సు` 1.8e-3✱ · `మ` 0.49 · `్` 4.8e-6✱ · `⏎` 1.2e-4 forced |
| 2 | `అ` 0.14 · `ల` 0.04✱ · `సిన` 0.70 · `్రో` 2.8e-5✱ · `య` 0.06 · `్` 0.28 · `న` 0.50 · `ె` 5.9e-3✱ · `న` 0.07✱ · `్ర` 1.5e-3✱ · `్` 0.45 · `ద` 0.59 · `ుల` 0.55 · `ె` 0.79 · `న` 0.18✱ · `్ర` 0.10 · `్` 0.66 · `ద` 0.61 · `ృ` 0.32 · `ఢ` 0.90 · `్` 3.1e-3✱ · `ధ` 0.36 · `్వ` 0.04✱ · `్` 1.2e-4✱ · `హ` 5.8e-4✱ · `ల` 0.05✱ · `క` 0.02✱ · `ృ` 0.10 · `తు` 0.07✱ · `ని` 0.20 · `␣త` 0.56 · `ుల` 0.05 · `క` 0.02✱ · `్ర` 0.01✱ · `్` 0.12 · `మ` 0.33 · `్య` 0.28 · `న` 0.02✱ · `్ర` 0.58 · `్` 0.92 · `ధ` 0.12 · `ుల` 0.23 · `ె` 0.49 · `న` 0.45✱ · `్ర` 0.85 · `్` 0.95 · `ద` 0.62 · `ృ` 0.93 · `ఢ` 0.98 · `్` 0.34✱ · `ధ` 0.80 · `్వ` 0.85 · `్` 0.95 · `హ` 0.96 · `ల` 0.68 · `క` 0.58 · `్యం` 8.6e-4✱ · `⏎` 0.90 forced |
| 3 | `త` 0.17 · `ొ` 0.02✱ · `లి` 0.74 · `␣చూపు` 0.06 · `న` 0.23 · `్రో` 2.9e-3✱ · `య` 0.93 · `్` 0.96 · `న` 0.95 · `ె` 0.67 · `న` 0.96 · `వ్ర` 1.0e-3✱ · `్` 0.52 · `ధ` 0.22 · `ుల` 0.79 · `్ర` 0.02✱ · `్` 0.93 · `ద` 0.72 · `్రు` 7.7e-4✱ · `ఢ` 0.67 · `న` 4.9e-4✱ · `ర` 3.0e-3✱ · `న` 0.02✱ · `న` 9.0e-3✱ · `ల` 0.01✱ · `క` 0.37 · `్ర` 0.09✱ · `్` 0.89 · `మ` 0.83 · `్` 7.5e-4✱ · `త` 0.07✱ · `ొ` 0.03✱ · `ల` 0.41✱ · `్ర` 0.13✱ · `్` 0.92 · `ద` 0.63 · `ృ` 0.80 · `ఢ` 0.99 · `ో` 0.01✱ · `మ` 0.07 · `్య` 0.19 · `ు` 0.14 · `త` 0.10 · `్` 0.03✱ · `త` 0.80 · `క` 0.07 · `ారం` 0.02✱ · `⏎` 0.79 forced |
| 4 | `త` 0.25 · `ొ` 9.8e-3✱ · `లి` 0.64 · `␣మాట` 0.25 · `న` 0.34 · `్రో` 0.90 · `య` 0.99 · `్` 0.98 · `న` 1.00 · `ె` 0.87 · `న` 0.96 · `వ్ర` 0.44 · `్` 0.97 · `ధ` 0.95 · `ుల` 0.92 · `్ర` 0.78 · `్` 0.97 · `ద` 0.98 · `్రు` 0.52 · `ఢ` 0.99 · `న` 0.69 · `ర` 0.79 · `న` 0.93 · `న` 0.72 · `ల` 0.88 · `క` 0.97 · `్ర` 0.90 · `్` 0.96 · `మ` 0.96 · `్` 0.56 · `త` 0.90 · `ొ` 0.97 · `ల` 0.98 · `్ర` 0.97 · `్` 0.97 · `ద` 0.95 · `ృ` 0.99 · `ఢ` 1.00 · `ో` 0.89 · `మ` 0.96 · `్య` 0.94 · `ు` 0.96 · `త` 0.96 · `్` 0.78 · `త` 0.99 · `క` 0.75 · `ారం` 0.72 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 170 tokens · 14.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సిరి సంపద్రుప్యమున్యంత్ర్య్సృజనమునుమునింసిత్యుమున్యంత్ర్య్సృజన్యా | `IIUUUIUUIIIIIIUUIUUIUU` |
| 2 | శృరమున్యంత్ర్య్సృజ్యుమున్యంత్ర్య్సృజనమునసితస్యేతృణీర్వణ్యమున్యా | `IIUUUIUUIIIIIIUUIUUIUU` |
| 3 | పృరణమ్యున్యంత్ర్య్సృజన్యుమ్యెతృణులెదృణమున్యేతృణీర్వణ్యమున్నా | `IIUUUIUUIIIIIIUUIUUIUU` |
| 4 | రరమున్యంత్ర్య్సృజ్యుమున్యంత్ర్య్సజనమునసితస్య్య్రణ్యమున్యాకశేతా | `IIUUUIUUIIIIIIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.116 · model's first choice kept 64% · constraint overrode 32% · backtracks 0

<details><summary>Token probabilities (170 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `సి` 0.01✱ · `రి` 0.05✱ · `␣సం` 0.10 · `ప` 1.00 · `ద` 0.98 · `్రు` 1.3e-4✱ · `ప` 0.02✱ · `్య` 0.07✱ · `ము` 0.43 · `న` 0.39 · `్య` 1.1e-5✱ · `ంత` 0.01 · `్ర` 5.3e-3✱ · `్య` 2.1e-4✱ · `్` 7.8e-4✱ · `స` 3.3e-3✱ · `ృ` 0.01✱ · `జ` 0.88 · `న` 0.39 · `ము` 0.30 · `ను` 0.05✱ · `ము` 0.02✱ · `ని` 0.13✱ · `ం` 6.4e-3✱ · `స` 3.6e-3✱ · `ిత` 0.02✱ · `్య` 0.04✱ · `ు` 0.10✱ · `ము` 0.04✱ · `న` 0.02✱ · `్య` 6.5e-3✱ · `ంత` 0.24 · `్ర` 0.47 · `్య` 0.89 · `్` 0.76 · `స` 0.95 · `ృ` 0.95 · `జ` 0.99 · `న` 0.98 · `్యా` 2.7e-7✱ · `⏎` 0.24 forced |
| 2 | `శ` 0.20 · `ృ` 5.5e-3✱ · `ర` 7.8e-6✱ · `ము` 0.17 · `న` 0.60 · `్య` 0.20 · `ంత` 0.95 · `్ర` 0.86 · `్య` 0.97 · `్` 0.88 · `స` 0.98 · `ృ` 0.95 · `జ` 0.99 · `్య` 2.0e-4✱ · `ు` 0.40 · `ము` 0.49 · `న` 0.89 · `్య` 0.96 · `ంత` 1.00 · `్ర` 0.96 · `్య` 0.99 · `్` 0.99 · `స` 1.00 · `ృ` 0.99 · `జ` 1.00 · `న` 0.95 · `ము` 0.27✱ · `న` 0.44 · `స` 2.0e-3✱ · `ిత` 0.30 · `స్య` 6.2e-4✱ · `ే` 0.16✱ · `త` 0.10 · `ృ` 0.16 · `ణ` 0.16 · `ీ` 0.07✱ · `ర్` 0.04 · `వ` 0.26 · `ణ` 0.24 · `్య` 0.41 · `ము` 0.03✱ · `న` 0.32✱ · `్యా` 0.02✱ · `⏎` 0.96 forced |
| 3 | `ప` 0.04✱ · `ృ` 0.12✱ · `రణ` 1.5e-6✱ · `మ` 5.8e-3✱ · `్య` 0.62 · `ు` 0.62 · `న` 0.21✱ · `్య` 0.74 · `ంత` 1.00 · `్ర` 0.98 · `్య` 0.99 · `్` 0.99 · `స` 1.00 · `ృ` 0.99 · `జ` 0.98 · `న` 0.59 · `్య` 0.07✱ · `ు` 0.88 · `మ` 0.04✱ · `్య` 0.24✱ · `ె` 2.1e-3✱ · `త` 0.47 · `ృ` 0.87 · `ణ` 0.97 · `ుల` 9.5e-5✱ · `ె` 0.01✱ · `ద` 0.03 · `ృ` 0.29 · `ణ` 0.56 · `ము` 8.6e-3✱ · `న` 0.95 · `్య` 0.61 · `ే` 1.9e-3✱ · `త` 0.84 · `ృ` 0.91 · `ణ` 0.97 · `ీ` 0.56 · `ర్` 0.97 · `వ` 0.99 · `ణ` 0.99 · `్య` 0.84 · `ము` 0.93 · `న్నా` 1.8e-4 · `⏎` 1.00 forced |
| 4 | `ర` 0.05✱ · `ర` 4.4e-5✱ · `ము` 0.58 · `న` 0.99 · `్య` 0.99 · `ంత` 1.00 · `్ర` 0.99 · `్య` 1.00 · `్` 0.99 · `స` 1.00 · `ృ` 1.00 · `జ` 1.00 · `్య` 0.54 · `ు` 0.98 · `ము` 0.61 · `న` 0.99 · `్య` 0.98 · `ంత` 0.99 · `్ర` 1.00 · `్య` 1.00 · `్` 1.00 · `స` 1.00 · `జ` 4.5e-6✱ · `న` 0.93 · `ము` 0.98 · `న` 0.96 · `స` 0.86 · `ిత` 0.96 · `స్య` 0.53 · `్య` 3.6e-4✱ · `్` 5.1e-4✱ · `ర` 4.2e-4✱ · `ణ` 0.31 · `్య` 0.74 · `ము` 0.82 · `న` 0.97 · `్యా` 0.66 · `క` 0.02 · `శ` 0.23 · `ే` 0.08✱ · `తా` 0.01 |

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

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 96 tokens · 16.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి ప్రేమ నినుల్రు దొ ల్య్ల్దుల్రు మదిన్ | `IIUIIUIIUIIU` |
| 2 | తొలి ఊర నినుల్రు దొ ల్య్ల్దుల్రు మదిన్ | `IIUIIUIIUIIU` |
| 3 | తొలి కన్రు నినుల్రు దొ ల్య్ల్దుల్రు మదిన్ | `IIUIIUIIUIIU` |
| 4 | తొలి దేవు నినుల్రు దొ ల్య్ల్దుల్రు మదిన్ | `IIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 42% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.226 · model's first choice kept 74% · constraint overrode 19% · backtracks 0

<details><summary>Token probabilities (96 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.76 · `ొ` 3.1e-3✱ · `లి` 0.55 · `␣ప్రేమ` 0.10 · `␣ని` 0.01✱ · `ను` 0.09✱ · `ల` 0.06✱ · `్రు` 8.8e-5✱ · `␣ద` 0.04 · `ొ` 2.4e-3✱ · `␣ల` 6.7e-6✱ · `్య` 3.2e-3✱ · `్` 2.6e-3✱ · `ల` 0.41 · `్` 3.4e-4✱ · `దు` 3.3e-3✱ · `ల` 0.14 · `్రు` 0.04✱ · `␣మ` 0.05✱ · `ది` 0.22 · `న` 5.8e-3✱ · `్` 1.2e-4✱ · `⏎` 0.02 forced |
| 2 | `త` 0.71 · `ొ` 9.6e-3✱ · `లి` 0.79 · `␣ఊ` 0.04 · `ర` 0.26 · `␣ని` 0.05 · `ను` 0.80 · `ల` 0.92 · `్రు` 0.98 · `␣ద` 0.72 · `ొ` 0.99 · `␣ల` 0.96 · `్య` 1.00 · `్` 1.00 · `ల` 1.00 · `్` 1.00 · `దు` 1.00 · `ల` 1.00 · `్రు` 1.00 · `␣మ` 0.16 · `ది` 0.84 · `న` 0.97 · `్` 1.00 · `⏎` 1.00 forced |
| 3 | `త` 0.93 · `ొ` 0.56 · `లి` 0.97 · `␣క` 0.10 · `న` 0.01✱ · `్రు` 1.7e-4✱ · `␣ని` 0.96 · `ను` 0.92 · `ల` 0.99 · `్రు` 1.00 · `␣ద` 1.00 · `ొ` 1.00 · `␣ల` 1.00 · `్య` 1.00 · `్` 1.00 · `ల` 1.00 · `్` 1.00 · `దు` 1.00 · `ల` 1.00 · `్రు` 1.00 · `␣మ` 0.91 · `ది` 0.99 · `న` 1.00 · `్` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ొ` 0.99 · `లి` 1.00 · `␣ద` 0.09 · `ే` 0.15 · `వు` 0.32 · `␣ని` 0.32 · `ను` 1.00 · `ల` 1.00 · `్రు` 1.00 · `␣ద` 1.00 · `ొ` 1.00 · `␣ల` 1.00 · `్య` 1.00 · `్` 1.00 · `ల` 1.00 · `్` 1.00 · `దు` 1.00 · `ల` 1.00 · `్రు` 1.00 · `␣మ` 1.00 · `ది` 1.00 · `న` 1.00 · `్` 1.00 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 93 tokens · 14.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి జన్మలకై తల న్య్వ్తొల్యుని నమ్ | `IIUIIUIIUIIU` |
| 2 | తొలి మాటకదియ్ తల న్య్వ్తొల్యుని వన్ | `IIUIIUIIUIIU` |
| 3 | తొలి కన్నతకై తల న్య్వ్తొల్యుని భన్ | `IIUIIUIIUIIU` |
| 4 | తొలి ఆశలకై తల న్య్వ్తొల్యుని పన్ | `IIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 40% · single-akshara words 20% · repeated lines 0 · mean token probability (geometric) 0.191 · model's first choice kept 71% · constraint overrode 20% · backtracks 0

<details><summary>Token probabilities (93 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.76 · `ొ` 3.1e-3✱ · `లి` 0.55 · `␣జన్` 0.02 · `మ` 0.99 · `ల` 0.08✱ · `క` 0.30 · `ై` 0.69 · `␣త` 0.46 · `ల` 0.41 · `␣న` 8.1e-4✱ · `్య` 4.8e-7✱ · `్వ` 3.0e-5✱ · `్` 1.1e-3✱ · `త` 0.04✱ · `ొ` 3.3e-3✱ · `ల` 0.14 · `్య` 1.2e-3✱ · `ు` 0.32 · `ని` 0.11✱ · `␣న` 0.01✱ · `మ` 0.14 · `్` 5.0e-6✱ · `⏎` 0.09 forced |
| 2 | `త` 0.70 · `ొ` 8.8e-3✱ · `లి` 0.68 · `␣మాట` 0.05 · `క` 0.14 · `ది` 6.2e-4✱ · `య` 1.8e-3✱ · `్` 0.04✱ · `␣త` 0.63 · `ల` 0.65 · `␣న` 0.29 · `్య` 0.86 · `్వ` 0.94 · `్` 0.95 · `త` 0.99 · `ొ` 0.98 · `ల` 0.98 · `్య` 0.98 · `ు` 0.98 · `ని` 0.97 · `␣వ` 0.07 · `న` 0.54 · `్` 0.92 · `⏎` 1.00 forced |
| 3 | `త` 0.93 · `ొ` 0.44✱ · `లి` 0.90 · `␣క` 0.03 · `న్న` 0.16 · `త` 0.38 · `క` 0.06✱ · `ై` 0.94 · `␣త` 0.97 · `ల` 1.00 · `␣న` 0.99 · `్య` 1.00 · `్వ` 1.00 · `్` 1.00 · `త` 1.00 · `ొ` 1.00 · `ల` 1.00 · `్య` 1.00 · `ు` 1.00 · `ని` 1.00 · `␣భ` 0.03 · `న్` 0.52 · `⏎` 0.95 forced |
| 4 | `త` 0.99 · `ొ` 0.99 · `లి` 0.99 · `␣ఆ` 0.12 · `శ` 0.91 · `ల` 0.44 · `క` 0.95 · `ై` 1.00 · `␣త` 1.00 · `ల` 1.00 · `␣న` 1.00 · `్య` 1.00 · `్వ` 1.00 · `్` 1.00 · `త` 1.00 · `ొ` 1.00 · `ల` 1.00 · `్య` 1.00 · `ు` 1.00 · `ని` 1.00 · `␣ప` 0.03 · `న్` 0.98 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 74 tokens · 28.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి ప్రేమ నిరంతర తోడున ఆ | `IIUIIUIIUIIU` |
| 2 | తొలి పాపపు మమ్రత ఘ్న్ర్తోడున ఆ | `IIUIIUIIUIIU` |
| 3 | తొలి కంటిన కద్రిని క్వ్న్తోడున ఆ | `IIUIIUIIUIIU` |
| 4 | తొలి ఊపిరినిన్రు నిదుర్ర్తొడునో | `IIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 39% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.032 · model's first choice kept 55% · constraint overrode 38% · backtracks 30

<details><summary>Token probabilities (74 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.76 · `ొ` 3.1e-3✱ · `లి` 0.55 · `␣ప్రేమ` 0.10 · `␣ని` 0.01✱ · `ర` 3.6e-3✱ · `ంత` 0.95 · `ర` 0.98 · `␣తో` 0.01 · `డు` 0.92 · `న` 0.10✱ · `␣ఆ` 6.0e-3 · `⏎` 3.5e-4 forced |
| 2 | `త` 0.70 · `ొ` 1.5e-3✱ · `లి` 0.68 · `␣పా` 4.6e-3 · `ప` 0.65 · `పు` 0.32 · `␣మ` 0.03 · `మ` 0.55 · `్ర` 5.5e-8✱ · `త` 0.77 · `␣ఘ` 4.5e-3 · `్` 2.5e-8✱ · `న` 0.94 · `్ర` 4.9e-5✱ · `్` 1.2e-5✱ · `త` 0.03✱ · `ో` 3.5e-3✱ · `డు` 0.12✱ · `న` 0.58 · `␣ఆ` 0.50 · `⏎` 1.00 forced |
| 3 | `త` 0.92 · `ొ` 0.07✱ · `లి` 0.94 · `␣క` 0.11 · `ంటి` 0.10✱ · `న` 0.06✱ · `␣క` 0.49 · `ద` 0.02✱ · `్రి` 8.1e-8✱ · `ని` 0.04✱ · `␣క` 0.55 · `్వ` 5.4e-7✱ · `్` 1.7e-4✱ · `న` 0.22 · `్` 0.01✱ · `త` 0.68 · `ో` 0.71 · `డు` 0.97 · `న` 1.00 · `␣ఆ` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ొ` 0.95 · `లి` 0.99 · `␣ఊ` 0.24 · `పి` 0.97 · `రి` 0.96 · `ని` 0.17 · `న` 1.0e-3✱ · `్రు` 5.9e-6✱ · `␣ని` 0.21 · `దు` 1.0e-3✱ · `ర` 0.92 · `్ర` 1.5e-3✱ · `్` 0.47 · `త` 0.74 · `ొ` 7.6e-3✱ · `డు` 0.97 · `న` 0.99 · `ో` 5.4e-6✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 87 tokens · 28.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి వాడి పలక్రు త్యొతొక్రు త్యొతొక్ | `IIUIIUIIUIIU` |
| 2 | తొలి తల్లి దయల్రు త్యొతొక్రు త్యొతొక్ | `IIUIIUIIUIIU` |
| 3 | తొలి మమ్రపు ప్రేమల త్యొత్తొకరుత్ | `IIUIIUIIUIIU` |
| 4 | తొలి ఆశల రూపల త్యొత్తొకరుత్ | `IIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 33% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.129 · model's first choice kept 63% · constraint overrode 26% · backtracks 30

<details><summary>Token probabilities (87 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.76 · `ొ` 3.1e-3✱ · `లి` 0.57 · `␣వా` 7.2e-3 · `డి` 0.09 · `␣ప` 7.5e-3 · `ల` 0.31✱ · `క` 0.86 · `్రు` 3.2e-6✱ · `␣త` 0.09✱ · `్య` 2.7e-3✱ · `ొ` 1.2e-3✱ · `త` 3.2e-3✱ · `ొ` 0.02✱ · `క` 0.09 · `్రు` 9.6e-4✱ · `␣త` 0.21 · `్య` 0.50 · `ొ` 0.96 · `త` 0.94 · `ొ` 1.00 · `క` 1.00 · `్` 7.0e-8✱ · `⏎` 0.06 forced |
| 2 | `త` 0.59 · `ొ` 0.04✱ · `లి` 0.89 · `␣తల్లి` 0.09 · `␣ద` 0.06✱ · `య` 0.65 · `ల` 0.08✱ · `్రు` 0.04✱ · `␣త` 0.84 · `్య` 0.99 · `ొ` 0.99 · `త` 0.99 · `ొ` 1.00 · `క` 0.99 · `్రు` 0.94 · `␣త` 1.00 · `్య` 1.00 · `ొ` 1.00 · `త` 1.00 · `ొ` 0.99 · `క` 0.99 · `్` 0.98 · `⏎` 1.00 forced |
| 3 | `త` 0.83 · `ొ` 0.32✱ · `లి` 0.85 · `␣మ` 0.06 · `మ` 0.58 · `్ర` 5.5e-7✱ · `పు` 0.02✱ · `␣ప్రేమ` 0.22 · `ల` 0.69 · `␣త` 1.9e-3✱ · `్య` 1.00 · `ొ` 1.00 · `త` 1.00 · `్` 2.8e-8✱ · `త` 0.55 · `ొ` 0.93 · `క` 0.99 · `రు` 0.01✱ · `త` 1.5e-3✱ · `్` 0.60 · `⏎` 0.77 forced |
| 4 | `త` 0.99 · `ొ` 1.00 · `లి` 1.00 · `␣ఆ` 0.05 · `శ` 0.80 · `ల` 0.37 · `␣రూప` 0.06 · `ల` 0.55 · `␣త` 1.00 · `్య` 1.00 · `ొ` 1.00 · `త` 0.99 · `్` 0.14✱ · `త` 0.99 · `ొ` 1.00 · `క` 0.97 · `రు` 0.82 · `త` 0.98 · `్` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 65 tokens · 4.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి ప్రేమ జగమ్రుడి తుల్యముగా | `IIUIIUIIUIIU` |
| 2 | తొలి దీవెన దైవముతో వలెనే | `IIUIIUIIUIIU` |
| 3 | తొలి ఊరట సుఖ్యమొదొక్రనిగా | `IIUIIUIIUIIU` |
| 4 | తొలి ఆశ్రయమున్న భుదోదమనే | `IIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.069 · model's first choice kept 52% · constraint overrode 40% · backtracks 0

<details><summary>Token probabilities (65 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.76 · `ొ` 3.1e-3✱ · `లి` 0.55 · `␣ప్రేమ` 0.10 · `␣జగ` 0.03✱ · `మ` 0.02✱ · `్రు` 1.2e-6✱ · `డి` 0.28 · `␣త` 0.04✱ · `ుల` 0.04✱ · `్య` 0.81 · `ము` 0.44 · `గా` 0.04 · `⏎` 0.18 forced |
| 2 | `త` 0.86 · `ొ` 2.7e-3✱ · `లి` 0.66 · `␣దీ` 0.14 · `వె` 0.83 · `న` 1.00 · `␣ద` 0.43 · `ై` 0.94 · `వ` 0.96 · `ము` 0.31 · `తో` 0.06✱ · `␣వ` 3.1e-3✱ · `లె` 0.80 · `నే` 0.23 · `⏎` 1.00 forced |
| 3 | `త` 0.97 · `ొ` 0.48✱ · `లి` 0.98 · `␣ఊ` 0.09 · `ర` 0.33 · `ట` 0.60 · `␣సు` 0.03 · `ఖ` 0.92 · `్య` 9.4e-5✱ · `మ` 0.21 · `ొ` 0.04✱ · `ద` 6.0e-3✱ · `ొ` 6.2e-4✱ · `క` 0.80 · `్ర` 1.5e-5✱ · `ని` 0.06✱ · `గా` 0.32✱ · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ొ` 0.97 · `లి` 0.99 · `␣ఆ` 0.31 · `శ` 0.93 · `్ర` 0.22✱ · `య` 0.32✱ · `ము` 0.30 · `న` 6.2e-3✱ · `్` 8.1e-7✱ · `న` 0.68 · `␣భ` 0.04 · `ు` 0.06✱ · `ద` 2.9e-5✱ · `ో` 0.06✱ · `ద` 0.33 · `మ` 0.01 · `నే` 0.04✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 70 tokens · 4.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి ప్రేమ అమృత్రము త్యొల్యున పో | `IIUIIUIIUIIU` |
| 2 | తొలి దీపము వెన్నెలె తోడెన పో | `IIUIIUIIUIIU` |
| 3 | తొలి కౌగిలి తీయని క్వ్త్యున్ డొరె పో | `IIUIIUIIUIIU` |
| 4 | తొలి దైవము తల్లికథో నవనే | `IIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 30% · single-akshara words 20% · repeated lines 0 · mean token probability (geometric) 0.047 · model's first choice kept 47% · constraint overrode 39% · backtracks 0

<details><summary>Token probabilities (70 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.76 · `ొ` 3.1e-3✱ · `లి` 0.55 · `␣ప్రేమ` 0.10 · `␣అమ` 0.01✱ · `ృత` 0.70 · `్ర` 2.5e-6✱ · `ము` 0.12✱ · `␣త` 0.21✱ · `్య` 6.3e-3✱ · `ొ` 2.3e-5✱ · `ల` 0.71 · `్య` 5.6e-4✱ · `ు` 0.31 · `న` 0.13 · `␣పో` 0.02 · `⏎` 4.8e-6 forced |
| 2 | `త` 0.78 · `ొ` 3.3e-3✱ · `లి` 0.73 · `␣దీ` 0.07 · `ప` 0.03 · `ము` 0.34 · `␣వె` 0.39 · `న్న` 0.01✱ · `ెల` 0.86 · `ె` 0.03✱ · `␣తో` 0.01✱ · `డ` 0.30 · `ె` 0.09✱ · `న` 0.08 · `␣పో` 0.20 · `⏎` 1.00 forced |
| 3 | `త` 0.97 · `ొ` 0.54 · `లి` 0.98 · `␣క` 0.05 · `ౌ` 0.34✱ · `గి` 0.99 · `లి` 0.97 · `␣తీ` 0.02 · `య` 0.69 · `ని` 0.45 · `␣క` 0.13 · `్వ` 2.4e-5✱ · `్` 8.3e-6✱ · `త` 0.03✱ · `్య` 0.06✱ · `ు` 0.42 · `న` 0.90 · `్` 2.1e-7✱ · `␣డ` 2.4e-3✱ · `ొ` 0.03✱ · `రె` 9.6e-5✱ · `␣పో` 0.57 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ొ` 0.98 · `లి` 1.00 · `␣ద` 0.03 · `ై` 0.69 · `వ` 0.98 · `ము` 0.51 · `␣తల్లి` 0.20 · `క` 0.02✱ · `థ` 6.4e-5✱ · `ో` 0.04✱ · `␣న` 0.05 · `వ` 0.08✱ · `నే` 7.9e-3 |

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

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 87 tokens · 13.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవన్ నందనుడ్యెన్ లవణ్ సంద్రమున్రున్ | `IUUIUUIUUIUU` |
| 2 | వ్రివర్షీ శతగ్రీవనెన్ లంక నిల్యా | `IUUIUUIUUIUU` |
| 3 | శ్రి వన్రాల నశ్యించునృన్ భీముడై చే | `IUUIUUIUUIUU` |
| 4 | భవానాంతరమ్యేన్ హుబన్ శిర్యెనై నివ్ | `IUUIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 6% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.033 · model's first choice kept 28% · constraint overrode 52% · backtracks 0

<details><summary>Token probabilities (87 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.19 · `వ` 0.56 · `న` 0.99 · `్` 4.9e-6✱ · `␣న` 0.01 · `ంద` 0.72 · `న` 0.68 · `ు` 0.02✱ · `డ` 0.20✱ · `్య` 2.2e-3✱ · `ె` 0.46 · `న్` 0.20 · `␣ల` 0.17 · `వ` 1.4e-4✱ · `ణ` 0.69 · `్` 8.7e-3✱ · `␣స` 0.46 · `ంద్ర` 0.05✱ · `ము` 0.71 · `న` 0.07✱ · `్రు` 1.4e-4✱ · `న్` 8.2e-3✱ · `⏎` 0.88 forced |
| 2 | `వ` 0.10 · `్రి` 3.7e-6✱ · `వర్` 3.1e-4✱ · `ష` 0.21 · `ీ` 0.01✱ · `␣శ` 0.02 · `త` 0.06✱ · `గ` 0.01✱ · `్రీ` 0.02✱ · `వ` 0.28 · `న` 0.02✱ · `ె` 1.1e-3✱ · `న్` 0.22✱ · `␣ల` 0.85 · `ం` 0.35 · `క` 8.4e-3✱ · `␣ని` 0.03 · `ల` 0.17 · `్యా` 6.3e-4✱ · `⏎` 1.0e-4 forced |
| 3 | `శ` 0.13 · `్రి` 3.7e-4✱ · `␣వ` 1.2e-3✱ · `న` 0.19 · `్ర` 3.2e-3✱ · `ాల` 0.02 · `␣న` 0.03✱ · `శ` 0.10✱ · `్య` 0.10✱ · `ించు` 0.03✱ · `న` 0.21✱ · `ృ` 3.9e-4✱ · `న్` 0.53 · `␣భ` 0.15 · `ీ` 0.38 · `ము` 0.09 · `డ` 0.37 · `ై` 0.46 · `␣చే` 0.17✱ · `⏎` 2.4e-6 forced |
| 4 | `భ` 0.09 · `వ` 2.0e-3✱ · `ాన` 0.10 · `ా` 0.08✱ · `ంత` 0.31 · `ర` 0.86 · `మ` 3.9e-3✱ · `్య` 0.02✱ · `ే` 0.17 · `న్` 0.77 · `␣హ` 0.10 · `ు` 6.8e-4✱ · `బ` 1.7e-3✱ · `న` 0.08 · `్` 0.03✱ · `␣శి` 0.02 · `ర` 0.68 · `్య` 0.03✱ · `ె` 0.07✱ · `న` 0.23✱ · `ై` 0.30 · `␣ని` 2.6e-3✱ · `వ` 0.09✱ · `్` 1.3e-6✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 93 tokens · 15.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలిప్రాణమున్రుత్యతొల్రుత్యమున్రుత్ | `IUUIUUIUUIUU` |
| 2 | తొలిక్రియ్యమున్రుత్యతొల్రుత్యమున్రుత్ | `IUUIUUIUUIUU` |
| 3 | తొలిప్రేమ్యమున్రుత్యతొల్రుత్యమున్రుత్ | `IUUIUUIUUIUU` |
| 4 | తొలిక్రామ్యమున్రుత్యతొల్రుత్యమున్రుత్ | `IUUIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 0% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.257 · model's first choice kept 76% · constraint overrode 21% · backtracks 0

<details><summary>Token probabilities (93 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ొ` 2.1e-3✱ · `లి` 0.63 · `ప` 0.01✱ · `్రా` 0.21✱ · `ణ` 0.77 · `ము` 0.40 · `న` 0.24✱ · `్రు` 1.7e-5✱ · `త` 0.03✱ · `్య` 0.03✱ · `త` 0.02✱ · `ొ` 8.1e-3✱ · `ల` 0.36✱ · `్రు` 1.3e-4✱ · `త` 0.17✱ · `్య` 0.28 · `ము` 0.35 · `న` 0.42 · `్రు` 0.05✱ · `త` 0.84 · `్` 4.5e-6✱ · `⏎` 0.05 forced |
| 2 | `త` 0.51 · `ొ` 5.4e-3✱ · `లి` 0.57 · `క` 0.12 · `్రియ` 3.1e-4✱ · `్య` 7.2e-4✱ · `ము` 0.28 · `న` 0.88 · `్రు` 0.71 · `త` 0.93 · `్య` 0.94 · `త` 0.93 · `ొ` 0.99 · `ల` 0.92 · `్రు` 0.97 · `త` 0.99 · `్య` 0.99 · `ము` 0.99 · `న` 1.00 · `్రు` 0.99 · `త` 0.99 · `్` 0.99 · `⏎` 1.00 forced |
| 3 | `త` 0.92 · `ొ` 0.09✱ · `లి` 0.86 · `ప్ర` 0.18 · `ే` 0.98 · `మ` 0.97 · `్య` 0.15 · `ము` 0.43 · `న` 0.98 · `్రు` 1.00 · `త` 1.00 · `్య` 0.99 · `త` 1.00 · `ొ` 1.00 · `ల` 1.00 · `్రు` 1.00 · `త` 1.00 · `్య` 1.00 · `ము` 1.00 · `న` 1.00 · `్రు` 1.00 · `త` 1.00 · `్` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ొ` 0.90 · `లి` 0.97 · `క` 0.14 · `్రా` 3.5e-6✱ · `మ` 0.52 · `్య` 0.56 · `ము` 1.00 · `న` 1.00 · `్రు` 1.00 · `త` 1.00 · `్య` 1.00 · `త` 1.00 · `ొ` 1.00 · `ల` 1.00 · `్రు` 1.00 · `త` 1.00 · `్య` 1.00 · `ము` 1.00 · `న` 1.00 · `్రు` 1.00 · `త` 1.00 · `్` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 96 tokens · 35.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వనానగ్రియం తుంబి త్వం ధీర తేజో | `IUUIUUIUUIUU` |
| 2 | గనవ్యాహగమ్యుం త్వు స్ర్వ్ఘం ధీర తేజో | `IUUIUUIUUIUU` |
| 3 | సనద్యాదరమ్యుం త్వు స్ర్వ్ఘం ధీర తేజో | `IUUIUUIUUIUU` |
| 4 | ననల్యాగమయ్యుం త్వు స్ర్వ్హం ధీర తేజో | `IUUIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 40% · single-akshara words 35% · repeated lines 0 · mean token probability (geometric) 0.119 · model's first choice kept 62% · constraint overrode 23% · backtracks 30

<details><summary>Token probabilities (96 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.45 · `న` 1.0e-3✱ · `ాన` 4.1e-3✱ · `గ` 0.07 · `్రి` 4.3e-4✱ · `యం` 0.44 · `␣తు` 4.7e-3 · `ంబ` 3.9e-3 · `ి` 0.85 · `␣త` 0.01✱ · `్వ` 0.08✱ · `ం` 0.54 · `␣ధ` 0.03 · `ీ` 0.16 · `ర` 0.90 · `␣తే` 0.10 · `జ` 0.87 · `ో` 0.56 · `⏎` 0.09 forced |
| 2 | `గ` 0.06 · `న` 3.9e-3✱ · `వ` 0.08 · `్యా` 0.03✱ · `హ` 0.13 · `గ` 0.02 · `మ` 0.58 · `్య` 0.70 · `ు` 0.40 · `ం` 0.82 · `␣త` 0.31 · `్వ` 0.70 · `ు` 6.8e-6✱ · `␣స` 1.2e-3✱ · `్ర` 3.2e-4✱ · `్వ` 4.4e-5✱ · `్` 8.6e-4✱ · `ఘ` 6.9e-3✱ · `ం` 0.20 · `␣ధ` 0.09 · `ీ` 0.39 · `ర` 0.88 · `␣తే` 0.44 · `జ` 0.98 · `ో` 1.00 · `⏎` 1.00 forced |
| 3 | `స` 0.49 · `న` 7.2e-5✱ · `ద` 0.11 · `్యా` 0.05✱ · `ద` 0.06 · `ర` 0.08 · `మ` 0.03✱ · `్య` 0.53 · `ు` 0.78 · `ం` 0.99 · `␣త` 0.64 · `్వ` 0.97 · `ు` 0.46 · `␣స` 0.30 · `్ర` 0.92 · `్వ` 0.97 · `్` 0.97 · `ఘ` 1.00 · `ం` 1.00 · `␣ధ` 0.97 · `ీ` 1.00 · `ర` 1.00 · `␣తే` 1.00 · `జ` 1.00 · `ో` 1.00 · `⏎` 1.00 forced |
| 4 | `న` 0.03 · `న` 0.01✱ · `ల` 0.07 · `్యా` 0.06✱ · `గ` 0.04 · `మ` 0.87 · `య` 7.2e-3✱ · `్య` 0.17✱ · `ు` 0.99 · `ం` 1.00 · `␣త` 0.95 · `్వ` 0.99 · `ు` 0.98 · `␣స` 0.98 · `్ర` 1.00 · `్వ` 1.00 · `్` 1.00 · `హ` 9.3e-8✱ · `ం` 0.73 · `␣ధ` 0.99 · `ీ` 1.00 · `ర` 1.00 · `␣తే` 1.00 · `జ` 1.00 · `ో` 1.00 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 78 tokens · 27.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శృనగ్యమ్ములన్ సాగి శ్రీరాముడున్ లం | `IUUIUUIUUIUU` |
| 2 | స్రునిత్రీలతై రక్ష్యుచున్ సాగి లంకై | `IUUIUUIUUIUU` |
| 3 | సృనగ్యమ్ములన్ సాగి సీతానురవ్యున్ | `IUUIUUIUUIUU` |
| 4 | సృనగ్యమ్ములన్ సాగి శిర్యుమ్మెనున్ లం | `IUUIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 27% · single-akshara words 13% · repeated lines 0 · mean token probability (geometric) 0.104 · model's first choice kept 49% · constraint overrode 32% · backtracks 14

<details><summary>Token probabilities (78 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.16✱ · `ృ` 2.8e-3✱ · `న` 4.5e-3✱ · `గ` 0.60 · `్య` 1.8e-3✱ · `మ్ము` 0.02✱ · `ల` 0.18 · `న్` 0.01✱ · `␣సా` 0.05 · `గి` 0.11 · `␣శ్రీ` 0.01✱ · `రా` 0.39 · `ము` 0.64 · `డు` 0.55 · `న్` 0.17 · `␣ల` 0.02✱ · `ం` 0.24 · `⏎` 7.5e-5 forced |
| 2 | `స` 0.01 · `్రు` 5.6e-4✱ · `ని` 8.4e-3✱ · `త` 0.08 · `్రీ` 1.2e-3✱ · `ల` 0.10 · `త` 1.1e-3✱ · `ై` 0.15 · `␣ర` 0.41 · `క్ష` 0.81 · `్య` 8.9e-3✱ · `ు` 0.79 · `చు` 0.04✱ · `న్` 0.74 · `␣సా` 0.04 · `గి` 0.43 · `␣ల` 0.42 · `ం` 0.86 · `క` 4.5e-3✱ · `ై` 0.08✱ · `⏎` 0.74 forced |
| 3 | `స` 0.19 · `ృ` 0.01✱ · `న` 0.01✱ · `గ` 0.26 · `్య` 0.52 · `మ్ము` 0.52 · `ల` 0.86 · `న్` 0.91 · `␣సా` 0.49 · `గి` 0.96 · `␣సీ` 0.46 · `తా` 0.50 · `ను` 0.05✱ · `ర` 0.53 · `వ` 0.05 · `్య` 1.6e-3✱ · `ు` 0.49 · `న్` 0.69 · `⏎` 0.21 forced |
| 4 | `స` 0.89 · `ృ` 0.29 · `న` 0.21 · `గ` 0.94 · `్య` 1.00 · `మ్ము` 0.97 · `ల` 0.99 · `న్` 0.99 · `␣సా` 0.88 · `గి` 1.00 · `␣శి` 0.02 · `ర` 0.09 · `్య` 1.0e-3✱ · `ు` 0.50 · `మ్` 0.01 · `మె` 0.11 · `ను` 0.11✱ · `న్` 0.16✱ · `␣ల` 9.4e-3✱ · `ం` 0.99 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 102 tokens · 7.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | విశాలంబు సుగ్రామ్యు ఝ్వ్వేనై లొనగ్రో | `IUUIUUIUUIUU` |
| 2 | వశీష్ఠుడ్యునై తేజొపల్లెన్యు లంకా | `IUUIUUIUUIUU` |
| 3 | గెశీష్ఠుడ్యునై తేజొగీతమ్ము దేవే | `IUUIUUIUUIUU` |
| 4 | సుశీష్ఠుడ్యునై సంద్రు న్య్య్జొన్యుగ్రుడెన్మున్ | `IUUIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.044 · model's first choice kept 40% · constraint overrode 45% · backtracks 0

<details><summary>Token probabilities (102 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వి` 0.03 · `శ` 0.58 · `ాల` 0.91 · `ం` 0.05✱ · `బు` 0.22 · `␣సు` 0.02 · `గ` 0.38 · `్రా` 2.6e-3✱ · `మ` 0.57 · `్య` 0.03✱ · `ు` 0.34✱ · `␣` 2.9e-4✱ · `ఝ` 0.64 · `్వ` 8.5e-4✱ · `్వ` 3.3e-4✱ · `ే` 9.4e-4✱ · `న` 0.38 · `ై` 0.03✱ · `␣ల` 0.13✱ · `ొ` 1.4e-4✱ · `న` 0.02✱ · `గ` 0.48 · `్రో` 9.1e-5✱ · `⏎` 0.09 forced |
| 2 | `వ` 0.08 · `శ` 5.0e-5✱ · `ీ` 0.76 · `ష్` 0.24✱ · `ఠ` 0.97 · `ు` 0.74 · `డ` 0.08✱ · `్య` 2.8e-3✱ · `ు` 0.47 · `న` 0.06 · `ై` 0.12 · `␣తే` 0.06 · `జ` 0.92 · `ొ` 2.7e-3✱ · `ప` 0.14✱ · `ల్ల` 0.14✱ · `ె` 0.62 · `న` 0.12✱ · `్య` 3.2e-4✱ · `ు` 0.64 · `␣ల` 0.14 · `ం` 0.46 · `కా` 0.35 · `⏎` 0.02 forced |
| 3 | `గ` 0.25 · `ె` 2.3e-4✱ · `శ` 2.6e-6✱ · `ీ` 0.12 · `ష్` 0.05 · `ఠ` 0.86 · `ు` 0.81 · `డ` 0.71 · `్య` 0.95 · `ు` 0.95 · `న` 0.91 · `ై` 1.00 · `␣తే` 0.05 · `జ` 0.92 · `ొ` 0.55 · `గ` 6.3e-3✱ · `ీ` 4.4e-3✱ · `త` 0.76 · `మ్ము` 0.12✱ · `␣ద` 0.06 · `ే` 0.18 · `వే` 0.07 · `⏎` 0.25 forced |
| 4 | `స` 0.06 · `ు` 2.8e-5✱ · `శ` 1.2e-3✱ · `ీ` 0.45 · `ష్` 0.15 · `ఠ` 0.98 · `ు` 0.95 · `డ` 0.99 · `్య` 0.99 · `ు` 1.00 · `న` 0.99 · `ై` 1.00 · `␣స` 0.13 · `ంద్ర` 0.02✱ · `ు` 9.2e-3✱ · `␣న` 2.6e-3✱ · `్య` 6.2e-4✱ · `్య` 8.6e-4✱ · `్` 1.3e-4✱ · `జ` 0.02✱ · `ొ` 0.11✱ · `న` 0.18 · `్య` 0.02✱ · `ు` 0.98 · `గ` 6.9e-4✱ · `్రు` 0.02✱ · `డ` 0.09✱ · `ె` 0.04✱ · `న్` 6.4e-3✱ · `ము` 4.9e-5✱ · `న్` 1.0e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 83 tokens · 17.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలిప్రాణమున్రుత్యతొల్రుత్యమున్రో | `IUUIUUIUUIUU` |
| 2 | తొలివ్యాసమున్రుత్యతొల్రుత్యమున్రో | `IUUIUUIUUIUU` |
| 3 | తొలత్యాసమున్రుత్యతొల్రుత్యమున్రో | `IUUIUUIUUIUU` |
| 4 | తొలప్రేమయేన్రుత్యతొల్రుత్యమున్రో | `IUUIUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 0% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.318 · model's first choice kept 73% · constraint overrode 21% · backtracks 0

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ొ` 2.1e-3✱ · `లి` 0.63 · `ప` 0.01✱ · `్రా` 0.21✱ · `ణ` 0.77 · `ము` 0.40 · `న` 0.24✱ · `్రు` 1.7e-5✱ · `త` 0.03✱ · `్య` 0.03✱ · `త` 0.02✱ · `ొ` 8.1e-3✱ · `ల` 0.36✱ · `్రు` 1.3e-4✱ · `త` 0.17✱ · `్య` 0.28 · `ము` 0.35 · `న` 0.42 · `్రో` 0.02✱ · `⏎` 0.01 forced |
| 2 | `త` 0.52 · `ొ` 8.8e-3✱ · `లి` 0.63 · `వ` 0.03 · `్యా` 0.05✱ · `స` 0.76 · `ము` 0.71 · `న` 0.89 · `్రు` 0.62 · `త` 0.95 · `్య` 0.95 · `త` 0.97 · `ొ` 0.99 · `ల` 0.98 · `్రు` 0.99 · `త` 1.00 · `్య` 1.00 · `ము` 0.99 · `న` 0.97 · `్రో` 0.98 · `⏎` 1.00 forced |
| 3 | `త` 0.88 · `ొ` 0.41✱ · `ల` 0.09 · `త` 0.12 · `్యా` 0.02✱ · `స` 0.70 · `ము` 0.89 · `న` 0.99 · `్రు` 0.98 · `త` 1.00 · `్య` 1.00 · `త` 1.00 · `ొ` 1.00 · `ల` 1.00 · `్రు` 1.00 · `త` 1.00 · `్య` 1.00 · `ము` 1.00 · `న` 1.00 · `్రో` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ొ` 0.99 · `ల` 0.57 · `ప్ర` 0.03 · `ే` 0.85 · `మ` 0.92 · `యే` 0.27 · `న` 0.61 · `్రు` 0.93 · `త` 1.00 · `్య` 0.99 · `త` 1.00 · `ొ` 1.00 · `ల` 1.00 · `్రు` 1.00 · `త` 1.00 · `్య` 1.00 · `ము` 1.00 · `న` 1.00 · `్రో` 1.00 |

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

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 113 tokens · 19.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగమ్రుడిక్రుడెదన్ జగద్రియమున్రదిన్ | `UIUIIUIUIIUIUIIUIU` |
| 2 | తల్లి దయ్నమునిక్రుడెద్దెన దైవమున్రదినన్ భవన్ | `UIUIIUIUIIUIUIIUIU` |
| 3 | తల్లి ఆప్యయమున్రుడెద్దెన తండ్రి ప్రేమకలన్ భవన్ | `UIUIIUIUIIUIUIIUIU` |
| 4 | తల్లి కౌగిలిలోన్రుడెద్దెన క్వ్బ్తైకమున్రదినన్ జగన్ | `UIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 35% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.099 · model's first choice kept 65% · constraint overrode 32% · backtracks 0

<details><summary>Token probabilities (113 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.72 · `␣ప్రేమ` 0.83 · `␣జగ` 0.32 · `మ` 0.02✱ · `్రు` 3.8e-7✱ · `డి` 0.17 · `క` 0.11✱ · `్రు` 9.6e-7✱ · `డ` 0.10 · `ె` 0.46 · `ద` 0.02✱ · `న్` 8.0e-3✱ · `␣జగ` 2.3e-3✱ · `ద` 0.05✱ · `్రియ` 4.8e-3✱ · `ము` 0.56 · `న` 0.13✱ · `్ర` 3.5e-5✱ · `ది` 0.02✱ · `న్` 6.8e-3✱ · `⏎` 0.98 forced |
| 2 | `త` 0.64 · `ల్లి` 0.81 · `␣ద` 0.07 · `య` 0.80 · `్` 4.1e-5✱ · `న` 0.40 · `ము` 0.15 · `ని` 0.04 · `క` 0.09 · `్రు` 0.07✱ · `డ` 0.82 · `ె` 0.98 · `ద` 0.97 · `్` 1.3e-5✱ · `ద` 0.78 · `ె` 0.23✱ · `న` 0.21✱ · `␣ద` 0.08✱ · `ై` 0.78 · `వ` 0.94 · `ము` 0.19 · `న` 0.55 · `్ర` 0.39 · `ది` 0.89 · `న` 1.3e-3✱ · `న్` 0.61 · `␣భ` 2.7e-5✱ · `వ` 0.18 · `న` 0.40 · `్` 1.9e-5✱ · `⏎` 0.93 forced |
| 3 | `త` 0.87 · `ల్లి` 0.90 · `␣ఆ` 0.15 · `ప` 0.17 · `్య` 0.90 · `య` 1.8e-4✱ · `ము` 0.81 · `న` 0.46 · `్రు` 0.71 · `డ` 0.88 · `ె` 0.99 · `ద` 0.98 · `్` 0.36✱ · `ద` 0.99 · `ె` 0.96 · `న` 0.91 · `␣త` 0.34 · `ండ` 0.17 · `్రి` 0.72 · `␣ప్రేమ` 0.15 · `క` 0.39 · `ల` 0.03✱ · `న్` 0.43 · `␣భ` 0.25✱ · `వ` 0.50 · `న` 0.93 · `్` 0.84 · `⏎` 1.00 forced |
| 4 | `త` 0.97 · `ల్లి` 0.93 · `␣క` 0.24 · `ౌ` 3.2e-3✱ · `గి` 0.91 · `లి` 0.81 · `లో` 0.26 · `న` 0.89 · `్రు` 0.95 · `డ` 0.99 · `ె` 1.00 · `ద` 0.99 · `్` 0.85 · `ద` 1.00 · `ె` 0.99 · `న` 0.96 · `␣క` 0.54 · `్వ` 2.1e-7✱ · `్` 5.2e-7✱ · `బ` 0.13✱ · `్` 0.02✱ · `త` 0.02✱ · `ై` 0.04✱ · `క` 0.15 · `ము` 0.28 · `న` 0.86 · `్ర` 0.69 · `ది` 0.92 · `న` 0.24✱ · `న్` 0.95 · `␣జగ` 0.03✱ · `న్` 0.25 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 109 tokens · 17.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగమ్రునిక్యది క్వ్య్తమ్యదిన్రయమున్యెనన్ | `UIUIIUIUIIUIUIIUIU` |
| 2 | తల్లి దయ్నయమున్యెనన్ జగదంతమంత్యమునన్ నిలవ్ | `UIUIIUIUIIUIUIIUIU` |
| 3 | తల్లి ఆశ్రయమున్యెనన్ కమథన్యదియ్యునమున్యెనన్ | `UIUIIUIUIIUIUIIUIU` |
| 4 | తల్లి విన్నపమున్యెనన్ తలతప్పదై సతియమ్యెనన్ | `UIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 33% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.074 · model's first choice kept 56% · constraint overrode 37% · backtracks 0

<details><summary>Token probabilities (109 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.72 · `␣ప్రేమ` 0.83 · `␣జగ` 0.32 · `మ` 0.02✱ · `్రు` 3.8e-7✱ · `ని` 0.03 · `క` 0.07✱ · `్య` 4.3e-5✱ · `ది` 0.23 · `␣క` 0.06✱ · `్వ` 3.1e-6✱ · `్య` 4.4e-6✱ · `్` 1.1e-4✱ · `త` 0.03✱ · `మ` 0.11✱ · `్య` 0.05✱ · `ది` 0.54 · `న` 1.9e-3✱ · `్ర` 5.9e-4✱ · `య` 0.02✱ · `ము` 0.08✱ · `న` 0.01✱ · `్య` 1.2e-4✱ · `ె` 0.22 · `న` 0.02✱ · `న్` 3.6e-3✱ · `⏎` 0.94 forced |
| 2 | `త` 0.40 · `ల్లి` 0.80 · `␣ద` 0.07 · `య` 0.78 · `్` 9.3e-5✱ · `న` 0.43 · `య` 0.01 · `ము` 0.56 · `న` 0.27 · `్య` 0.01✱ · `ె` 0.73 · `న` 0.84 · `న్` 0.67 · `␣జగ` 0.47 · `ద` 0.01✱ · `ంత` 0.59 · `మ` 0.27 · `ంత` 0.25✱ · `్య` 0.17 · `ము` 0.22 · `న` 0.84 · `న్` 0.07✱ · `␣ని` 5.5e-4✱ · `ల` 0.14✱ · `వ` 0.25 · `్` 1.4e-7✱ · `⏎` 3.1e-3 forced |
| 3 | `త` 0.86 · `ల్లి` 0.90 · `␣ఆ` 0.19 · `శ` 0.80 · `్ర` 0.23✱ · `య` 0.81 · `ము` 0.70 · `న` 0.95 · `్య` 0.98 · `ె` 1.00 · `న` 0.99 · `న్` 1.00 · `␣క` 0.09 · `మ` 0.03✱ · `థ` 1.5e-5✱ · `న` 0.51 · `్య` 0.02✱ · `ది` 0.30 · `య` 0.03 · `్య` 0.04✱ · `ు` 0.21 · `న` 0.39 · `ము` 0.04✱ · `న` 0.91 · `్య` 0.08✱ · `ె` 0.90 · `న` 0.88 · `న్` 0.98 · `⏎` 0.91 forced |
| 4 | `త` 0.99 · `ల్లి` 0.94 · `␣వి` 0.01✱ · `న్న` 0.22 · `ప` 0.76 · `ము` 0.83 · `న` 0.99 · `్య` 0.99 · `ె` 1.00 · `న` 1.00 · `న్` 1.00 · `␣త` 0.05 · `ల` 0.23 · `త` 0.01✱ · `ప్ప` 0.07✱ · `ద` 0.03 · `ై` 0.12 · `␣స` 0.02 · `తి` 0.01✱ · `య` 0.23 · `మ` 0.08✱ · `్య` 0.43 · `ె` 0.60 · `న` 0.96 · `న్` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 101 tokens · 32.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామచంద్రుని కీర్తి నిత్యమరధ్యతై నిలిచెన్ వివే | `UIUIIUIUIIUIUIIUIU` |
| 2 | రామచంద్రుని ప్రేమనుండి రరమ్యతై నిలిచెన్ వివే | `UIUIIUIUIIUIUIIUIU` |
| 3 | సీమవన్రుని శోకమున్రు స్రజిత్యతై నిలిచెన్ వివే | `UIUIIUIUIIUIUIIUIU` |
| 4 | రామచంద్రుని రక్షనై లవృ ల్వ్ల్రత్యతై నిలిచెన్ వివే | `UIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 57% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.084 · model's first choice kept 56% · constraint overrode 33% · backtracks 30

<details><summary>Token probabilities (101 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.29 · `మ` 0.85 · `చ` 0.80 · `ంద్ర` 0.99 · `ు` 0.86 · `ని` 0.97 · `␣క` 0.05 · `ీ` 0.25✱ · `ర్` 0.98 · `తి` 0.95 · `␣ని` 0.05 · `త్య` 0.46 · `మ` 0.09 · `ర` 7.5e-4✱ · `ధ` 6.1e-3✱ · `్య` 0.33 · `త` 0.03✱ · `ై` 0.15✱ · `␣ని` 0.01✱ · `లి` 0.28 · `చె` 0.90 · `న్` 0.02✱ · `␣వి` 1.1e-5✱ · `వే` 7.4e-3 · `⏎` 1.8e-5 forced |
| 2 | `రా` 0.01 · `మ` 0.32 · `చ` 0.48 · `ంద్ర` 0.98 · `ు` 0.89 · `ని` 0.97 · `␣ప్రేమ` 0.02 · `ను` 0.02 · `ండి` 2.3e-4✱ · `␣ర` 0.48 · `ర` 3.6e-6✱ · `మ` 0.19 · `్య` 0.05✱ · `త` 0.15 · `ై` 0.92 · `␣ని` 0.27 · `లి` 0.91 · `చె` 1.00 · `న్` 1.00 · `␣వి` 0.22 · `వే` 0.99 · `⏎` 1.00 forced |
| 3 | `సీ` 0.82 · `మ` 1.7e-4✱ · `వ` 0.10✱ · `న` 0.04✱ · `్రు` 1.0e-5✱ · `ని` 0.37 · `␣శ` 0.08 · `ో` 0.46✱ · `క` 0.90 · `ము` 0.78 · `న` 0.42✱ · `్రు` 3.6e-5✱ · `␣స` 0.27 · `్ర` 2.4e-3✱ · `జ` 7.3e-3✱ · `ిత` 0.17✱ · `్య` 0.02✱ · `త` 0.55 · `ై` 1.00 · `␣ని` 0.97 · `లి` 0.99 · `చె` 1.00 · `న్` 1.00 · `␣వి` 0.99 · `వే` 1.00 · `⏎` 1.00 forced |
| 4 | `రా` 0.09✱ · `మ` 0.65 · `చ` 0.85 · `ంద్ర` 1.00 · `ు` 0.90 · `ని` 0.98 · `␣ర` 0.50 · `క్ష` 0.46 · `న` 0.32 · `ై` 0.19✱ · `␣ల` 0.69 · `వ` 6.2e-5✱ · `ృ` 2.3e-5✱ · `␣ల` 8.4e-5✱ · `్వ` 1.1e-5✱ · `్` 3.4e-3✱ · `ల` 0.16 · `్ర` 1.6e-4✱ · `త` 0.42 · `్య` 1.5e-5✱ · `త` 0.13✱ · `ై` 1.00 · `␣ని` 1.00 · `లి` 1.00 · `చె` 1.00 · `న్` 1.00 · `␣వి` 1.00 · `వే` 1.00 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 106 tokens · 35.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ నిరీత ఊపిరి దైవమున్రునిమర్యమున్ | `UIUIIUIUIIUIUIIUIU` |
| 2 | తల్లి దీవెన జగ్రునిశ్రుని మ్ర్య్దంగమున్రునిమర్యమున్ | `UIUIIUIUIIUIUIIUIU` |
| 3 | తల్లి కౌగిలి ధైర్యమున్రుని శ్వ్వ్నత్రమున్రునిమర్యమున్ | `UIUIIUIUIIUIUIIUIU` |
| 4 | తల్లి చూపు మమత్యునై నిను నమ్మునిన్రునిమర్యమున్ | `UIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.079 · model's first choice kept 61% · constraint overrode 30% · backtracks 30

<details><summary>Token probabilities (106 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.72 · `␣ప్రేమ` 0.83 · `␣ని` 0.05 · `రీ` 8.4e-3✱ · `త` 0.02 · `␣ఊ` 9.6e-3 · `పి` 0.35 · `రి` 0.93 · `␣ద` 0.09✱ · `ై` 0.93 · `వ` 0.88 · `ము` 0.13 · `న` 0.23 · `్రు` 4.6e-5✱ · `ని` 0.05✱ · `మ` 1.6e-3✱ · `ర` 0.02✱ · `్య` 2.4e-4✱ · `ము` 0.26✱ · `న` 0.05✱ · `్` 1.3e-6✱ · `⏎` 0.61 forced |
| 2 | `త` 0.43 · `ల్లి` 0.72 · `␣దీ` 0.07 · `వె` 0.93 · `న` 1.00 · `␣జగ` 0.11 · `్రు` 8.0e-7✱ · `ని` 0.43 · `శ` 9.1e-3 · `్రు` 0.03✱ · `ని` 0.56 · `␣మ` 0.04✱ · `్ర` 5.0e-5✱ · `్య` 1.9e-4✱ · `్` 6.0e-6✱ · `ద` 0.06✱ · `ంగ` 0.06✱ · `ము` 0.65 · `న` 0.74 · `్రు` 0.18 · `ని` 0.62 · `మ` 0.52 · `ర` 0.95 · `్య` 0.98 · `ము` 0.99 · `న` 0.90 · `్` 0.98 · `⏎` 0.99 forced |
| 3 | `త` 0.92 · `ల్లి` 0.93 · `␣క` 0.43 · `ౌ` 0.07✱ · `గి` 0.97 · `లి` 0.98 · `␣ధ` 0.04 · `ై` 0.65 · `ర్య` 0.78 · `ము` 0.84 · `న` 0.29 · `్రు` 0.70 · `ని` 0.73 · `␣శ` 0.08✱ · `్వ` 0.04✱ · `్వ` 4.4e-10✱ · `్` 8.4e-12✱ · `న` 0.73 · `త` 7.3e-3✱ · `్ర` 6.6e-3✱ · `ము` 0.70 · `న` 0.99 · `్రు` 0.99 · `ని` 0.98 · `మ` 0.98 · `ర` 1.00 · `్య` 1.00 · `ము` 1.00 · `న` 1.00 · `్` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ల్లి` 0.98 · `␣చూపు` 0.09 · `␣మ` 0.10 · `మ` 0.58 · `త` 0.87 · `్య` 0.02✱ · `ు` 0.38 · `న` 0.40 · `ై` 2.6e-4✱ · `␣ని` 0.34 · `ను` 9.1e-3✱ · `␣న` 0.20 · `మ్ము` 4.6e-3✱ · `ని` 0.49 · `న` 0.03✱ · `్రు` 0.03✱ · `ని` 0.78 · `మ` 0.92 · `ర` 1.00 · `్య` 1.00 · `ము` 1.00 · `న` 1.00 · `్` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 97 tokens · 7.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగమ్రియంతటి మ్ర్య్దబ్యమున్రనిగూడగా | `UIUIIUIUIIUIUIIUIU` |
| 2 | తల్లి దయ్మృదమున్రనిగ్యమృదబ్యమున్రుపరాణగా | `UIUIIUIUIIUIUIIUIU` |
| 3 | తల్లి వాత్సలయెన్రునిగ్యమృదబ్యమున్రుపరాణగా | `UIUIIUIUIIUIUIIUIU` |
| 4 | తల్లి కన్నతృదయ్యమున్రునితర్యమున్రుపరాణగా | `UIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.079 · model's first choice kept 60% · constraint overrode 33% · backtracks 0

<details><summary>Token probabilities (97 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.72 · `␣ప్రేమ` 0.83 · `␣జగ` 0.32 · `మ` 0.02✱ · `్రియ` 2.3e-7✱ · `ంత` 0.19 · `టి` 0.20 · `␣మ` 0.01✱ · `్ర` 3.1e-6✱ · `్య` 6.0e-5✱ · `్` 2.8e-5✱ · `ద` 0.05✱ · `బ` 4.8e-3✱ · `్య` 1.2e-3✱ · `ము` 0.84 · `న` 0.09✱ · `్ర` 3.2e-5✱ · `ని` 4.6e-3✱ · `గ` 3.1e-3✱ · `ూ` 0.01✱ · `డ` 0.56 · `గా` 3.4e-3✱ · `⏎` 0.84 forced |
| 2 | `త` 0.65 · `ల్లి` 0.71 · `␣ద` 0.09 · `య` 0.78 · `్` 1.5e-4✱ · `మ` 0.08 · `ృ` 0.15 · `ద` 0.49 · `ము` 0.12✱ · `న` 0.57 · `్ర` 3.6e-3✱ · `ని` 0.86 · `గ` 0.97 · `్య` 1.1e-4✱ · `మ` 0.18 · `ృ` 0.14✱ · `ద` 0.62 · `బ` 0.40 · `్య` 0.95 · `ము` 0.76 · `న` 0.72 · `్రు` 0.01 · `ప` 0.08 · `రా` 0.04✱ · `ణ` 0.19✱ · `గా` 0.03 · `⏎` 1.00 forced |
| 3 | `త` 0.88 · `ల్లి` 0.90 · `␣వా` 0.07 · `త్స` 0.99 · `ల` 0.35✱ · `య` 2.2e-3✱ · `ె` 0.25 · `న` 0.28 · `్రు` 3.4e-4✱ · `ని` 0.28 · `గ` 0.91 · `్య` 0.54 · `మ` 0.83 · `ృ` 0.95 · `ద` 0.99 · `బ` 0.96 · `్య` 0.99 · `ము` 0.95 · `న` 0.97 · `్రు` 0.71 · `ప` 0.27 · `రా` 0.88 · `ణ` 0.83 · `గా` 0.91 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ల్లి` 0.93 · `␣క` 0.18✱ · `న్న` 1.5e-3✱ · `త` 0.57 · `ృ` 0.33 · `దయ` 0.01✱ · `్య` 1.7e-3✱ · `ము` 0.34 · `న` 0.94 · `్రు` 0.54 · `ని` 0.82 · `తర` 2.7e-6✱ · `్య` 6.8e-4✱ · `ము` 0.06 · `న` 0.97 · `్రు` 0.83 · `ప` 0.57 · `రా` 0.99 · `ణ` 0.98 · `గా` 0.99 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 111 tokens · 8.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగమ్రునిక్యది క్వ్య్తమ్యదిన్రయమున్యునిం | `UIUIIUIUIIUIUIIUIU` |
| 2 | తల్లి దయ్నసమర్పణే శిరదై నిలవ్యునినమ్యునే | `UIUIIUIUIIUIUIIUIU` |
| 3 | తల్లి ఆశ్రయమే అమృత్యమృదాల్యునిన్రయమున్యునే | `UIUIIUIUIIUIUIIUIU` |
| 4 | తల్లి కౌగిలయే కనుమ్యుని న్వ్య్తమ్మెనుంన్యునినమ్మినే | `UIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 33% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.054 · model's first choice kept 48% · constraint overrode 39% · backtracks 0

<details><summary>Token probabilities (111 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.72 · `␣ప్రేమ` 0.83 · `␣జగ` 0.32 · `మ` 0.02✱ · `్రు` 3.8e-7✱ · `ని` 0.03 · `క` 0.07✱ · `్య` 4.3e-5✱ · `ది` 0.23 · `␣క` 0.06✱ · `్వ` 3.1e-6✱ · `్య` 4.4e-6✱ · `్` 1.1e-4✱ · `త` 0.03✱ · `మ` 0.11✱ · `్య` 0.05✱ · `ది` 0.54 · `న` 1.9e-3✱ · `్ర` 5.9e-4✱ · `య` 0.02✱ · `ము` 0.08✱ · `న` 0.01✱ · `్య` 1.2e-4✱ · `ు` 0.07 · `ని` 0.01✱ · `ం` 1.6e-3✱ · `⏎` 0.93 forced |
| 2 | `త` 0.40 · `ల్లి` 0.80 · `␣ద` 0.08 · `య` 0.78 · `్` 1.2e-4✱ · `న` 0.44 · `స` 0.03 · `మ` 0.13 · `ర్ప` 0.16 · `ణ` 0.69 · `ే` 0.31 · `␣శి` 0.04 · `ర` 0.79 · `ద` 9.0e-4✱ · `ై` 0.28 · `␣ని` 0.35 · `ల` 0.07✱ · `వ` 0.28 · `్య` 6.6e-4✱ · `ు` 0.38 · `ని` 0.67 · `న` 0.01✱ · `మ` 0.06 · `్య` 0.47 · `ు` 0.75 · `నే` 1.8e-3 · `⏎` 0.85 forced |
| 3 | `త` 0.78 · `ల్లి` 0.89 · `␣ఆ` 0.11 · `శ` 0.81 · `్ర` 0.23✱ · `య` 0.77 · `మే` 0.30 · `␣అమ` 0.01 · `ృత` 0.72 · `్య` 1.4e-4✱ · `మ` 0.12 · `ృ` 0.02✱ · `ద` 0.24 · `ాల` 0.05✱ · `్య` 0.52 · `ు` 0.77 · `ని` 0.86 · `న` 0.32 · `్ర` 9.1e-3✱ · `య` 0.76 · `ము` 0.66 · `న` 0.74 · `్య` 0.86 · `ు` 0.98 · `నే` 0.13 · `⏎` 1.00 forced |
| 4 | `త` 0.97 · `ల్లి` 0.93 · `␣క` 0.20 · `ౌ` 0.02✱ · `గి` 0.90 · `ల` 0.27 · `యే` 0.07✱ · `␣క` 0.25 · `ను` 5.6e-3 · `మ` 0.46 · `్య` 0.09✱ · `ు` 0.61 · `ని` 0.73 · `␣న` 0.03✱ · `్వ` 4.4e-5✱ · `్య` 7.3e-3✱ · `్` 0.03✱ · `త` 0.72 · `మ్` 0.02 · `మె` 0.16 · `ను` 0.06 · `ం` 0.09 · `న` 0.08✱ · `్య` 0.57 · `ు` 0.99 · `ని` 0.33✱ · `న` 7.3e-3✱ · `మ్` 0.02✱ · `మి` 1.0e-3✱ · `నే` 1.6e-3✱ |

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

<details><summary>Prompt (topic T2; the other topics differ only in the topic line)</summary>

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

Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 114 tokens · 18.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శముద్రమున్న దాటి లంక య్వ్వ్ఛాతునుంభ్రమున్న చే | `IUIUIUIUIUIUIUIU` |
| 2 | గమయ్యునుంభ్రమున్న లంక గమ్యునుంభ్రమున్న చే | `IUIUIUIUIUIUIUIU` |
| 3 | వృమిత్యునుంభ్రమున్న లంక గ్రీవమున్న చేర్చెనుం | `IUIUIUIUIUIUIUIU` |
| 4 | భమున్న దాటి లంక గమ్యు న్య్య్భామునన్ గమయ్యునుం | `IUIUIUIUIUIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 32% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.121 · model's first choice kept 57% · constraint overrode 38% · backtracks 0

<details><summary>Token probabilities (114 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.10 · `ము` 0.06✱ · `ద్ర` 0.78 · `ము` 0.33✱ · `న` 0.04✱ · `్` 2.0e-5✱ · `న` 0.67 · `␣దా` 0.26 · `టి` 0.73 · `␣ల` 0.61 · `ంక` 0.68 · `␣య` 9.6e-4✱ · `్వ` 1.6e-5✱ · `్వ` 1.9e-3✱ · `్` 5.9e-3✱ · `ఛ` 4.7e-3✱ · `ా` 0.02✱ · `తు` 0.14✱ · `ను` 0.17✱ · `ం` 0.02✱ · `భ` 3.3e-3✱ · `్ర` 0.13✱ · `ము` 0.25✱ · `న` 0.11✱ · `్` 3.7e-3✱ · `న` 0.92 · `␣చే` 0.05✱ · `⏎` 1.7e-6 forced |
| 2 | `గ` 0.18 · `మ` 0.14✱ · `య` 0.15✱ · `్య` 6.3e-3✱ · `ు` 0.28 · `ను` 0.05✱ · `ం` 0.84 · `భ` 0.33 · `్ర` 0.88 · `ము` 0.84 · `న` 0.86 · `్` 0.69 · `న` 1.00 · `␣ల` 0.12 · `ంక` 0.69 · `␣గ` 0.07✱ · `మ` 0.79 · `్య` 0.53 · `ు` 0.33 · `ను` 0.27✱ · `ం` 0.99 · `భ` 0.92 · `్ర` 0.99 · `ము` 0.97 · `న` 0.94 · `్` 0.97 · `న` 1.00 · `␣చే` 0.58 · `⏎` 0.99 forced |
| 3 | `వ` 0.34 · `ృ` 1.1e-6✱ · `మ` 4.0e-4✱ · `ిత` 0.02 · `్య` 0.09✱ · `ు` 0.87 · `ను` 0.48 · `ం` 0.99 · `భ` 0.98 · `్ర` 0.99 · `ము` 1.00 · `న` 0.99 · `్` 1.00 · `న` 1.00 · `␣ల` 0.19 · `ంక` 0.83 · `␣గ` 0.22 · `్రీ` 3.0e-5✱ · `వ` 0.54 · `ము` 0.62 · `న` 0.62 · `్` 0.99 · `న` 1.00 · `␣చే` 0.74 · `ర్` 3.8e-3✱ · `చె` 0.08 · `ను` 0.83 · `ం` 0.07✱ · `⏎` 0.66 forced |
| 4 | `భ` 0.10 · `ము` 3.7e-3✱ · `న` 0.58 · `్` 0.92 · `న` 1.00 · `␣దా` 0.23 · `టి` 0.87 · `␣ల` 0.71 · `ంక` 0.94 · `␣గ` 0.47 · `మ` 0.91 · `్య` 0.89 · `ు` 0.98 · `␣న` 5.8e-5✱ · `్య` 3.4e-3✱ · `్య` 0.01✱ · `్` 5.9e-3✱ · `భ` 6.2e-3✱ · `ాము` 0.02✱ · `న` 0.80 · `న్` 3.1e-3✱ · `␣గ` 0.01✱ · `మ` 0.95 · `య` 0.06✱ · `్య` 0.76 · `ు` 0.85 · `ను` 0.07✱ · `ం` 0.84 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 97 tokens · 15.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సముద్ర తీరమున్న శత్రు వ్ర్ఞ్జం దహించెనున్రునిం | `IUIUIUIUIUIUIUIU` |
| 2 | శ్రమించియుండు సీతనున్ రరమ్మనిన్రునిం భయప్ | `IUIUIUIUIUIUIUIU` |
| 3 | కమల్రజన్మ సౌందరమ్ము కంటికిన్రునిం కరుణ్ | `IUIUIUIUIUIUIUIU` |
| 4 | రమక్రియాన్వృతంబునన్ లొరాన్రునిం లభించెనుం | `IUIUIUIUIUIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.035 · model's first choice kept 43% · constraint overrode 47% · backtracks 0

<details><summary>Token probabilities (97 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 0.04✱ · `ము` 0.20 · `ద్ర` 0.88 · `␣తీ` 0.28✱ · `ర` 0.45 · `ము` 0.91 · `న` 0.96 · `్` 2.5e-6✱ · `న` 0.37 · `␣శ` 0.21 · `త్ర` 0.50 · `ు` 0.99 · `␣వ` 8.3e-3✱ · `్ర` 1.2e-4✱ · `్ఞ` 1.1e-7✱ · `్` 4.0e-3✱ · `జ` 9.1e-3✱ · `ం` 0.14✱ · `␣ద` 0.04 · `హ` 0.59 · `ించ` 0.19✱ · `ె` 0.97 · `ను` 0.84 · `న` 2.3e-3✱ · `్రు` 7.5e-5✱ · `ని` 1.6e-3✱ · `ం` 3.2e-4✱ · `⏎` 0.96 forced |
| 2 | `శ` 0.09✱ · `్రమ` 3.5e-3✱ · `ించి` 0.14 · `యు` 0.02 · `ండు` 0.07 · `␣సీ` 0.31 · `త` 0.53 · `ను` 0.13✱ · `న్` 0.02✱ · `␣ర` 0.74 · `ర` 8.0e-6✱ · `మ్మ` 0.09 · `ని` 0.12 · `న` 0.04✱ · `్రు` 0.05✱ · `ని` 0.14 · `ం` 0.98 · `␣భ` 0.04✱ · `య` 0.71 · `ప` 0.14✱ · `్` 2.6e-12✱ · `⏎` 3.2e-3 forced |
| 3 | `క` 0.03✱ · `మ` 0.03✱ · `ల` 0.78 · `్ర` 9.6e-6✱ · `జ` 0.04✱ · `న్` 0.05 · `మ` 0.78 · `␣సౌ` 0.04 · `ంద` 0.81 · `ర` 0.01✱ · `మ్ము` 0.06✱ · `␣క` 0.06✱ · `ంటి` 0.03✱ · `కి` 0.49 · `న` 0.13 · `్రు` 0.72 · `ని` 0.80 · `ం` 1.00 · `␣క` 0.25 · `రుణ` 0.31 · `్` 9.6e-7✱ · `⏎` 0.61 forced |
| 4 | `ర` 0.05✱ · `మ` 2.5e-3✱ · `క` 0.07✱ · `్రి` 6.5e-4✱ · `యా` 0.05✱ · `న్` 0.06 · `వ` 0.37 · `ృ` 0.08 · `తం` 2.5e-3✱ · `బు` 0.25 · `న` 0.30 · `న్` 0.07✱ · `␣ల` 0.45 · `ొ` 1.7e-4✱ · `రా` 1.7e-5✱ · `న` 0.21 · `్రు` 0.22 · `ని` 0.99 · `ం` 1.00 · `␣ల` 0.32 · `భ` 3.1e-3✱ · `ించ` 0.85 · `ె` 0.99 · `ను` 0.79 · `ం` 0.31✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 125 tokens · 33.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సముద్ర తీరమున్యెడల్ లొ ల్వ్వ్సన్రమున్యెడల్ జయమ్ | `IUIUIUIUIUIUIUIU` |
| 2 | చ మండలిక్రియేన సీత ర్వ్సన్రమున్యెడల్ నిమల్ | `IUIUIUIUIUIUIUIU` |
| 3 | ప్రిమల్రధారనై రణభ్రమృద్యెనల్ ల్వ్వ్సనర్మ్యెడల్ | `IUIUIUIUIUIUIUIU` |
| 4 | విమల్రభాగ్యమున్యెడల్ రవిమ్యెనల్ జయమ్ హరిమ్ | `IUIUIUIUIUIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.075 · model's first choice kept 54% · constraint overrode 36% · backtracks 30

<details><summary>Token probabilities (125 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 0.04✱ · `ము` 0.20 · `ద్ర` 0.88 · `␣తీ` 0.27✱ · `ర` 0.45 · `ము` 0.89 · `న` 0.96 · `్య` 2.0e-6✱ · `ె` 0.42 · `డ` 0.10 · `ల` 0.22 · `్` 8.8e-6✱ · `␣ల` 0.35 · `ొ` 1.2e-4✱ · `␣ల` 1.6e-4✱ · `్వ` 1.8e-5✱ · `్వ` 1.6e-3✱ · `్` 0.03✱ · `స` 2.5e-3✱ · `న` 0.18 · `్ర` 1.9e-3✱ · `ము` 0.12✱ · `న` 0.33✱ · `్య` 5.8e-3✱ · `ె` 0.90 · `డ` 0.75 · `ల` 0.90 · `్` 0.71 · `␣జ` 4.1e-4✱ · `య` 0.15 · `మ` 0.05✱ · `్` 4.6e-7✱ · `⏎` 0.40 forced |
| 2 | `చ` 0.03 · `␣మండ` 4.1e-5✱ · `లి` 0.04 · `క` 0.06✱ · `్రియ` 3.8e-4✱ · `ే` 0.24 · `న` 0.30 · `␣సీ` 0.04 · `త` 0.50 · `␣ర` 0.04✱ · `్వ` 4.2e-6✱ · `్` 0.09 · `స` 0.06 · `న` 0.77 · `్ర` 0.83 · `ము` 0.95 · `న` 0.94 · `్య` 0.97 · `ె` 1.00 · `డ` 1.00 · `ల` 1.00 · `్` 0.99 · `␣ని` 0.03 · `మ` 0.04✱ · `ల` 0.39 · `్` 0.24 · `⏎` 1.00 forced |
| 3 | `ప` 0.06✱ · `్రి` 0.03✱ · `మ` 7.3e-4✱ · `ల` 0.62 · `్ర` 1.1e-3✱ · `ధ` 5.9e-3 · `ార` 0.14 · `న` 0.07 · `ై` 0.01✱ · `␣ర` 0.42 · `ణ` 0.05✱ · `భ` 0.01✱ · `్రమ` 3.5e-3✱ · `ృ` 4.0e-3✱ · `ద` 0.63 · `్య` 0.32 · `ె` 0.18✱ · `న` 0.79 · `ల` 5.0e-3✱ · `్` 0.63 · `␣ల` 0.28 · `్వ` 0.10✱ · `్వ` 0.74 · `్` 0.92 · `స` 0.97 · `న` 0.99 · `ర` 5.8e-3✱ · `్` 0.18✱ · `మ` 0.54 · `్య` 0.56 · `ె` 0.66 · `డ` 0.61 · `ల` 1.00 · `్` 1.00 · `⏎` 0.55 forced |
| 4 | `వి` 0.06✱ · `మ` 1.6e-3✱ · `ల` 0.92 · `్ర` 0.24 · `భ` 0.09 · `ాగ` 0.18 · `్య` 0.76 · `ము` 0.53 · `న` 0.79 · `్య` 0.04✱ · `ె` 0.94 · `డ` 0.98 · `ల` 0.99 · `్` 0.99 · `␣ర` 0.42 · `వి` 1.2e-4✱ · `మ` 0.05 · `్య` 0.23 · `ె` 0.50 · `న` 0.72 · `ల` 0.20 · `్` 0.94 · `␣జ` 0.45 · `య` 0.98 · `మ` 0.74 · `్` 0.70 · `␣హ` 8.1e-3✱ · `రి` 0.20✱ · `మ` 0.13✱ · `్` 0.50 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 106 tokens · 31.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శముద్రమున్న వీరుడున్న సాగెనున్న నేడు నగ్ | `IUIUIUIUIUIUIUIU` |
| 2 | చమర్దమున్న లంకలోన్న సాగెనున్న తేజమున్ | `IUIUIUIUIUIUIUIU` |
| 3 | భముక్యముల్న ధైర్యమున్న త్వం త్వరం పొగెట్యునన్ | `IUIUIUIUIUIUIUIU` |
| 4 | విముక్తినిన్యు విష్ణునిన్యు విహ్వలించునున్న శిర్ | `IUIUIUIUIUIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.083 · model's first choice kept 47% · constraint overrode 31% · backtracks 30

<details><summary>Token probabilities (106 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.10 · `ము` 0.06✱ · `ద్ర` 0.78 · `ము` 0.30✱ · `న` 0.04✱ · `్` 1.8e-5✱ · `న` 0.65 · `␣వీ` 0.01 · `రు` 0.83 · `డు` 0.70 · `న` 6.1e-3✱ · `్` 1.2e-3✱ · `న` 0.91 · `␣సా` 0.03 · `గ` 0.38 · `ె` 0.72 · `ను` 0.85 · `న` 9.4e-4✱ · `్` 0.02✱ · `న` 1.00 · `␣నే` 4.6e-3 · `డు` 0.66 · `␣న` 6.9e-4✱ · `గ్` 8.0e-3 · `⏎` 2.6e-5 forced |
| 2 | `చ` 0.03✱ · `మ` 1.6e-3✱ · `ర్` 0.04 · `ద` 0.56 · `ము` 0.75 · `న` 0.64 · `్` 0.36 · `న` 1.00 · `␣ల` 0.09 · `ంక` 0.56 · `లో` 0.11 · `న` 0.93 · `్` 0.44 · `న` 1.00 · `␣సా` 0.06✱ · `గ` 0.56 · `ె` 0.98 · `ను` 0.96 · `న` 0.96 · `్` 0.99 · `న` 1.00 · `␣తే` 0.08 · `జ` 0.65 · `ము` 0.02✱ · `న్` 0.05 · `⏎` 0.99 forced |
| 3 | `భ` 0.07 · `ము` 7.4e-3✱ · `క` 0.08 · `్య` 2.3e-3✱ · `ముల` 0.02 · `్` 0.12✱ · `న` 0.74 · `␣ధ` 0.04 · `ై` 0.75 · `ర్య` 0.94 · `ము` 0.89 · `న` 0.92 · `్` 0.99 · `న` 1.00 · `␣త` 0.01✱ · `్వ` 0.02✱ · `ం` 0.15✱ · `␣త` 1.4e-3✱ · `్వ` 0.23 · `రం` 6.4e-3✱ · `␣పొ` 3.9e-3✱ · `గ` 0.17✱ · `ె` 0.94 · `ట` 0.08 · `్య` 9.5e-4✱ · `ు` 0.23 · `న` 0.27✱ · `న్` 0.08✱ · `⏎` 1.00 forced |
| 4 | `వి` 0.09 · `ము` 2.3e-3✱ · `క్తి` 0.65 · `ని` 0.35 · `న` 0.31 · `్య` 3.7e-5✱ · `ు` 0.27 · `␣వి` 6.5e-3 · `ష్` 0.05 · `ణు` 0.99 · `ని` 0.20 · `న` 0.85 · `్య` 0.26 · `ు` 0.97 · `␣వి` 0.25 · `హ` 0.12 · `్వ` 1.1e-4✱ · `ల` 0.86 · `ించు` 0.10✱ · `ను` 0.06 · `న` 0.37 · `్` 0.03✱ · `న` 0.94 · `␣శి` 0.02 · `ర` 0.80 · `్` 4.5e-8✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 132 tokens · 9.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవన్దునియ్ నడువ్యె లంక గ్వారమున్యెనుచ్యెనో | `IUIUIUIUIUIUIUIU` |
| 2 | మృవణ్దునియ్ దొరక్యె లంక గ్వ్వ్యెన్యెనోచ్యెనోమునో | `IUIUIUIUIUIUIUIU` |
| 3 | బృవణ్దునియ్ గమయ్యె లంక గ్వ్వ్యెన్యెనోప్యెనోచ్యెనో | `IUIUIUIUIUIUIUIU` |
| 4 | వృవణ్దునియ్ ద్రువయ్ లభించె ల్వ్న్కెన్యెనోచ్యెనోతనో | `IUIUIUIUIUIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.098 · model's first choice kept 61% · constraint overrode 33% · backtracks 0

<details><summary>Token probabilities (132 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.22 · `వ` 0.44 · `న` 0.99 · `్` 1.2e-6✱ · `ద` 0.34 · `ు` 4.5e-3✱ · `ని` 0.31 · `య` 6.0e-3✱ · `్` 9.3e-4✱ · `␣న` 0.35 · `డు` 0.22 · `వ` 0.12✱ · `్య` 3.8e-5✱ · `ె` 0.35 · `␣ల` 0.14 · `ంక` 0.62 · `␣గ` 0.04✱ · `్వ` 1.2e-6✱ · `ార` 0.08✱ · `ము` 0.14✱ · `న` 0.39 · `్య` 8.0e-4✱ · `ె` 0.37 · `ను` 0.01✱ · `చ` 6.2e-5✱ · `్య` 0.01✱ · `ె` 0.48 · `నో` 8.3e-3✱ · `⏎` 0.96 forced |
| 2 | `మ` 0.05 · `ృ` 0.02✱ · `వ` 3.0e-5✱ · `ణ` 0.03✱ · `్` 0.09✱ · `దు` 0.03 · `ని` 0.34 · `య` 0.79 · `్` 0.98 · `␣ద` 0.04 · `ొ` 7.6e-3✱ · `ర` 0.37 · `క` 0.80 · `్య` 0.52 · `ె` 0.89 · `␣ల` 0.20 · `ంక` 0.61 · `␣గ` 0.16 · `్వ` 0.93 · `్వ` 1.4e-6✱ · `్య` 4.4e-4✱ · `ె` 0.59 · `న` 0.40 · `్య` 0.05✱ · `ె` 0.90 · `నో` 0.15 · `చ` 0.32 · `్య` 0.99 · `ె` 0.99 · `నో` 0.97 · `ము` 1.7e-5✱ · `నో` 3.4e-3✱ · `⏎` 1.00 forced |
| 3 | `బ` 0.03 · `ృ` 0.01✱ · `వ` 2.9e-3✱ · `ణ` 0.79 · `్` 0.95 · `దు` 0.40 · `ని` 0.96 · `య` 1.00 · `్` 0.99 · `␣గ` 0.12✱ · `మ` 0.73 · `య` 5.8e-3✱ · `్` 0.11✱ · `య` 0.07✱ · `ె` 0.99 · `␣ల` 0.93 · `ంక` 0.95 · `␣గ` 0.82 · `్వ` 0.98 · `్వ` 0.65 · `్య` 0.87 · `ె` 0.94 · `న` 0.87 · `్య` 0.98 · `ె` 0.96 · `నో` 0.95 · `ప` 6.1e-3 · `్య` 0.67 · `ె` 0.90 · `నో` 0.71 · `చ` 0.71 · `్య` 0.99 · `ె` 1.00 · `నో` 0.99 · `⏎` 0.81 forced |
| 4 | `వ` 0.13 · `ృ` 0.31✱ · `వ` 0.24✱ · `ణ` 0.99 · `్` 0.99 · `దు` 0.84 · `ని` 0.99 · `య` 1.00 · `్` 1.00 · `␣ద` 0.04✱ · `్రు` 0.05✱ · `వ` 0.84 · `య` 0.07✱ · `్` 0.86 · `␣ల` 0.85 · `భ` 1.6e-5✱ · `ించ` 1.3e-3✱ · `ె` 0.97 · `␣ల` 0.99 · `్వ` 1.1e-6✱ · `్` 0.03✱ · `న` 0.08 · `్` 0.09✱ · `క` 0.84 · `ె` 1.8e-4✱ · `న` 0.71 · `్య` 0.99 · `ె` 1.00 · `నో` 0.98 · `చ` 0.54 · `్య` 0.99 · `ె` 1.00 · `నో` 0.98 · `త` 0.03 · `నో` 0.82 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 104 tokens · 8.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సముద్ర తీరమున్న శత్రు వ్ర్ఞ్జం దహించునట్లుగా | `IUIUIUIUIUIUIUIU` |
| 2 | దెమల్యమున్న సీతనున్ రథియ్న రూపమున్యగా | `IUIUIUIUIUIUIUIU` |
| 3 | భమున్న వన్రమున్న ధైర్య మ్ర్య్భం నిలవ్యునట్లుగా | `IUIUIUIUIUIUIUIU` |
| 4 | కమల్యమున్న కేశునన్ రఘవ్న రక్షిణుల్యగా | `IUIUIUIUIUIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.055 · model's first choice kept 49% · constraint overrode 43% · backtracks 0

<details><summary>Token probabilities (104 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 0.04✱ · `ము` 0.20 · `ద్ర` 0.88 · `␣తీ` 0.28✱ · `ర` 0.45 · `ము` 0.91 · `న` 0.96 · `్` 2.5e-6✱ · `న` 0.37 · `␣శ` 0.21 · `త్ర` 0.50 · `ు` 0.99 · `␣వ` 8.3e-3✱ · `్ర` 1.2e-4✱ · `్ఞ` 1.1e-7✱ · `్` 4.0e-3✱ · `జ` 9.1e-3✱ · `ం` 0.14✱ · `␣ద` 0.04 · `హ` 0.59 · `ించు` 0.13✱ · `న` 0.13✱ · `ట్లు` 0.49 · `గా` 6.2e-3✱ · `⏎` 0.93 forced |
| 2 | `ద` 0.03✱ · `ె` 4.2e-3✱ · `మ` 1.4e-4✱ · `ల` 0.41 · `్య` 2.4e-4✱ · `ము` 0.08 · `న` 0.67 · `్` 4.4e-3✱ · `న` 0.98 · `␣సీ` 0.02 · `త` 0.50 · `ను` 0.19✱ · `న్` 7.9e-3✱ · `␣ర` 0.53 · `థ` 2.3e-4✱ · `ి` 1.1e-3✱ · `య` 0.11 · `్` 5.4e-3✱ · `న` 0.70 · `␣రూప` 0.08 · `ము` 0.75 · `న` 0.61 · `్య` 1.7e-3✱ · `గా` 1.7e-3 · `⏎` 1.00 forced |
| 3 | `భ` 0.04✱ · `ము` 0.03✱ · `న` 0.33 · `్` 0.46 · `న` 0.99 · `␣వ` 0.03 · `న` 0.48 · `్ర` 1.4e-4✱ · `ము` 0.10 · `న` 0.79 · `్` 0.30 · `న` 0.99 · `␣ధ` 0.02 · `ై` 0.28 · `ర్య` 0.81 · `␣మ` 6.1e-4✱ · `్ర` 2.3e-3✱ · `్య` 7.5e-3✱ · `్` 0.13✱ · `భ` 2.2e-3✱ · `ం` 0.54 · `␣ని` 0.13 · `ల` 0.39 · `వ` 0.16 · `్య` 2.6e-4✱ · `ు` 0.37 · `న` 0.71 · `ట్లు` 0.37 · `గా` 0.97 · `⏎` 1.00 forced |
| 4 | `క` 0.06✱ · `మ` 0.12✱ · `ల` 0.96 · `్య` 9.6e-3✱ · `ము` 0.65 · `న` 0.98 · `్` 0.97 · `న` 1.00 · `␣క` 0.25 · `ేశ` 6.6e-3✱ · `ు` 0.48 · `న` 0.19✱ · `న్` 0.17✱ · `␣ర` 0.15 · `ఘ` 0.03✱ · `వ` 6.2e-4✱ · `్` 9.5e-3✱ · `న` 0.50 · `␣ర` 0.06 · `క్షి` 0.02 · `ణ` 0.11✱ · `ుల` 5.4e-3✱ · `్య` 0.41 · `గా` 0.95 |

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

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

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

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 85 tokens · 13.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీరామ నామమును చేరిన హంసమున్యెన్ | `UUIUIIIUIIUIUU` |
| 2 | శూరేశునిన్రు తలచున్ సుగమంబునైయెన్ | `UUIUIIIUIIUIUU` |
| 3 | సారద్రి నిండెను సనత్తమునైయెనన్తై | `UUIUIIIUIIUIUU` |
| 4 | శైరవ్య సాగరము త్వ్ర్చల్లన చేరెనుత్యా | `UUIUIIIUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 21% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.043 · model's first choice kept 42% · constraint overrode 45% · backtracks 0

<details><summary>Token probabilities (85 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.08 · `్రీ` 0.33 · `రా` 0.24 · `మ` 0.77 · `␣నా` 0.13 · `మ` 0.95 · `ము` 0.68 · `ను` 0.20 · `␣చే` 0.17 · `రి` 0.76 · `న` 0.31 · `␣హ` 0.44 · `ం` 0.02✱ · `స` 0.99 · `ము` 0.20 · `న` 0.29 · `్య` 1.1e-4✱ · `ె` 0.33 · `న` 0.14✱ · `్` 1.7e-5✱ · `⏎` 0.92 forced |
| 2 | `శ` 0.04 · `ూ` 0.05✱ · `ర` 0.03✱ · `ేశ` 0.02✱ · `ు` 0.80 · `ని` 0.76 · `న` 7.6e-4✱ · `్రు` 1.1e-4✱ · `␣త` 0.09✱ · `ల` 0.42 · `చు` 0.01✱ · `న్` 0.03✱ · `␣సు` 0.06 · `గ` 0.83 · `మం` 0.05✱ · `బు` 0.28 · `న` 0.20 · `ై` 0.23✱ · `య` 1.8e-3✱ · `ె` 0.96 · `న్` 0.47 · `⏎` 1.00 forced |
| 3 | `స` 0.76 · `ార` 1.4e-3✱ · `ద` 0.30 · `్రి` 0.05✱ · `␣ని` 0.03 · `ండె` 0.07✱ · `ను` 0.61 · `␣స` 0.39 · `న` 1.4e-5✱ · `త` 0.11 · `్` 3.2e-4✱ · `త` 0.82 · `ము` 0.36 · `న` 0.55 · `ై` 0.14✱ · `య` 0.02 · `ె` 0.99 · `న` 0.11✱ · `న్` 0.08✱ · `త` 4.3e-4✱ · `ై` 8.0e-3✱ · `⏎` 0.98 forced |
| 4 | `శ` 0.18 · `ై` 0.05✱ · `ర` 9.0e-4✱ · `వ` 0.56 · `్య` 5.2e-6✱ · `␣సా` 0.06 · `గర` 0.65 · `ము` 0.80 · `␣త` 4.2e-3✱ · `్వ` 2.7e-3✱ · `్ర` 4.4e-6✱ · `్` 4.7e-7✱ · `చ` 4.6e-4✱ · `ల్ల` 0.06✱ · `న` 0.21 · `␣చే` 0.30✱ · `రె` 0.80 · `ను` 0.60 · `త` 0.04✱ · `్యా` 5.4e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 79 tokens · 12.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిక్రియా సుమధు దైవమునందునందున్ | `UUIUIIIUIIUIUU` |
| 2 | తల్లిప్రియత్య ముకుతమ్యుని శోభనందున్ | `UUIUIIIUIIUIUU` |
| 3 | తల్లిభ్రమణ్య కరుణా స్రవణందునన్తమ్ | `UUIUIIIUIIUIUU` |
| 4 | తల్లిప్రణయ్ నిరమదైవమునందునన్తమ్ | `UUIUIIIUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.077 · model's first choice kept 47% · constraint overrode 39% · backtracks 0

<details><summary>Token probabilities (79 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.82 · `ల్లి` 0.78 · `క` 0.02✱ · `్రి` 7.7e-7✱ · `యా` 0.74 · `␣సు` 0.04 · `మ` 0.33 · `ధు` 0.55 · `␣ద` 1.1e-5✱ · `ై` 0.60 · `వ` 0.91 · `ము` 0.20 · `న` 0.28 · `ందు` 0.17 · `న` 0.13 · `ందు` 0.03✱ · `న` 0.25✱ · `్` 6.4e-7✱ · `⏎` 0.82 forced |
| 2 | `త` 0.69 · `ల్లి` 0.85 · `ప` 0.16 · `్రియ` 0.07✱ · `త` 0.10✱ · `్య` 5.0e-3✱ · `␣ము` 7.6e-3 · `కు` 0.16✱ · `త` 5.5e-3✱ · `మ` 0.07✱ · `్య` 0.02✱ · `ు` 0.06 · `ని` 0.11 · `␣శ` 0.02 · `ో` 0.55 · `భ` 0.97 · `న` 0.34 · `ందు` 0.58 · `న` 0.94 · `్` 0.44 · `⏎` 1.00 forced |
| 3 | `త` 0.95 · `ల్లి` 0.92 · `భ` 0.11 · `్ర` 1.4e-5✱ · `మణ` 0.07✱ · `్య` 0.02✱ · `␣క` 0.10 · `రుణ` 0.88 · `ా` 0.54 · `␣స` 0.07 · `్ర` 0.21✱ · `వ` 0.99 · `ణ` 0.03✱ · `ందు` 0.19✱ · `న` 0.98 · `న్` 0.05✱ · `త` 7.3e-3✱ · `మ్` 0.03✱ · `⏎` 1.00 forced |
| 4 | `త` 1.00 · `ల్లి` 0.94 · `ప్ర` 0.39 · `ణ` 6.7e-3✱ · `య` 0.76 · `్` 1.6e-3✱ · `␣ని` 0.08 · `ర` 0.03✱ · `మ` 4.4e-3✱ · `ద` 4.1e-3✱ · `ై` 0.07✱ · `వ` 0.70 · `ము` 0.19 · `న` 0.29 · `ందు` 0.44 · `న` 0.78 · `న` 0.07 · `్` 5.0e-3✱ · `త` 0.14✱ · `మ్` 0.98 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 106 tokens · 34.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిక్రియా దయలొ బ్ర్ఱ్ధా ఝిజజూ గదా గూ | `UUIUIIIUIIUIUU` |
| 2 | తల్లిప్రణయ్న మధు ల్య్ల్తా ఝిజజూ గదా గూ | `UUIUIIIUIIUIUU` |
| 3 | తల్లిప్రియత్య కమ ల్య్ల్తా ఝిజజూ గదా గూ | `UUIUIIIUIIUIUU` |
| 4 | తల్లిక్రియా రమలొ బ్ర్ఱ్ధా ఝిజజూ గదా గూ | `UUIUIIIUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 33% · repeated lines 0 · mean token probability (geometric) 0.134 · model's first choice kept 63% · constraint overrode 30% · backtracks 30

<details><summary>Token probabilities (106 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.82 · `ల్లి` 0.78 · `క` 0.02✱ · `్రి` 7.9e-7✱ · `యా` 0.73 · `␣ద` 0.03 · `య` 0.01✱ · `ల` 0.03✱ · `ొ` 0.26 · `␣బ` 4.9e-5✱ · `్ర` 0.08✱ · `్` 2.2e-9✱ · `ఱ` 0.18 · `్` 0.34✱ · `ధ` 5.4e-3✱ · `ా` 0.08✱ · `␣` 8.1e-3 · `ఝ` 0.20 · `ి` 8.8e-3 · `జ` 0.14 · `జ` 0.06✱ · `ూ` 1.2e-3✱ · `␣గ` 0.10✱ · `దా` 1.7e-3✱ · `␣గ` 3.6e-4✱ · `ూ` 0.28✱ · `⏎` 0.94 forced |
| 2 | `త` 0.77 · `ల్లి` 0.86 · `ప్ర` 0.05✱ · `ణ` 8.0e-4✱ · `య` 0.85 · `్` 4.2e-3✱ · `న` 0.37 · `␣మ` 0.05✱ · `ధు` 0.44 · `␣ల` 1.4e-3✱ · `్య` 8.7e-3✱ · `్` 0.21 · `ల` 0.33 · `్` 0.09✱ · `త` 0.01✱ · `ా` 0.02✱ · `␣` 0.42 · `ఝ` 0.98 · `ి` 0.91 · `జ` 0.95 · `జ` 0.95 · `ూ` 0.99 · `␣గ` 0.56 · `దా` 1.00 · `␣గ` 0.90 · `ూ` 1.00 · `⏎` 0.99 forced |
| 3 | `త` 0.87 · `ల్లి` 0.91 · `ప` 0.06 · `్రియ` 0.07✱ · `త` 0.19 · `్య` 0.05✱ · `␣క` 0.04 · `మ` 0.15✱ · `␣ల` 4.0e-3✱ · `్య` 0.41 · `్` 0.94 · `ల` 0.79 · `్` 0.95 · `త` 0.92 · `ా` 0.97 · `␣` 1.00 · `ఝ` 1.00 · `ి` 1.00 · `జ` 1.00 · `జ` 1.00 · `ూ` 1.00 · `␣గ` 0.99 · `దా` 1.00 · `␣గ` 1.00 · `ూ` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.97 · `ల్లి` 0.94 · `క` 0.06✱ · `్రి` 1.6e-5✱ · `యా` 0.90 · `␣ర` 0.02 · `మ` 0.52 · `ల` 0.11 · `ొ` 0.69 · `␣బ` 0.82 · `్ర` 0.88 · `్` 0.99 · `ఱ` 1.00 · `్` 0.99 · `ధ` 1.00 · `ా` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `ి` 1.00 · `జ` 1.00 · `జ` 1.00 · `ూ` 1.00 · `␣గ` 0.98 · `దా` 1.00 · `␣గ` 1.00 · `ూ` 1.00 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 98 tokens · 37.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వాయుప్రియా శిరముపై కయముగ్యునేయొక్ | `UUIUIIIUIIUIUU` |
| 2 | సాయిల్రుతమ్మ గమ య్య్య్జన్ లొక సత్యమున్నే | `UUIUIIIUIIUIUU` |
| 3 | నైయుష్యమున్న లొక ల్యాంకమునై జ్యయించెన్ | `UUIUIIIUIIUIUU` |
| 4 | భైయర్రమై నమమునై జయమున్న తేనెన్ | `UUIUIIIUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.037 · model's first choice kept 40% · constraint overrode 47% · backtracks 30

<details><summary>Token probabilities (98 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.33 · `ాయ` 0.88 · `ు` 1.00 · `ప` 0.02✱ · `్రి` 0.03✱ · `యా` 0.81 · `␣శి` 5.4e-3 · `ర` 0.54 · `ము` 0.11✱ · `పై` 0.24✱ · `␣క` 0.02✱ · `య` 3.6e-3✱ · `ము` 0.23 · `గ` 0.01 · `్య` 2.1e-3✱ · `ు` 0.25 · `నే` 8.9e-3 · `య` 0.01✱ · `ొ` 3.1e-3 · `క` 0.92 · `్` 1.6e-7✱ · `⏎` 0.42 forced |
| 2 | `స` 0.16 · `ాయి` 2.2e-4✱ · `ల` 0.33 · `్రు` 1.1e-4✱ · `త` 0.09 · `మ` 0.01✱ · `్` 3.2e-4✱ · `మ` 0.23 · `␣గ` 0.10 · `మ` 0.74 · `␣య` 2.4e-4✱ · `్య` 2.8e-4✱ · `్య` 6.0e-4✱ · `్` 0.01✱ · `జ` 0.02✱ · `న్` 0.06 · `␣ల` 0.17 · `ొ` 5.4e-4✱ · `క` 0.20✱ · `␣స` 9.2e-3 · `త` 0.05✱ · `్య` 0.28✱ · `ము` 0.44 · `న` 0.21 · `్` 0.03✱ · `నే` 0.02✱ · `⏎` 0.81 forced |
| 3 | `న` 0.03 · `ై` 0.08✱ · `యు` 7.1e-5✱ · `ష` 0.30 · `్య` 0.18 · `ము` 0.32 · `న` 0.17 · `్` 0.02✱ · `న` 0.22✱ · `␣ల` 0.18 · `ొ` 4.1e-3✱ · `క` 0.84 · `␣ల` 0.12 · `్యా` 6.7e-5✱ · `ం` 0.24 · `క` 0.46 · `ము` 0.08 · `న` 0.35 · `ై` 0.02✱ · `␣జ` 0.02✱ · `్య` 0.35 · `య` 0.06✱ · `ించ` 0.06✱ · `ె` 0.92 · `న` 0.12✱ · `్` 0.16✱ · `⏎` 0.29 forced |
| 4 | `భ` 0.17 · `ై` 0.35 · `య` 5.3e-7✱ · `ర` 9.8e-3✱ · `్రమ` 5.5e-7✱ · `ై` 0.04✱ · `␣న` 0.04 · `మ` 0.11✱ · `ము` 0.07✱ · `న` 0.57 · `ై` 0.24✱ · `␣జ` 0.04 · `య` 0.51 · `ము` 0.17✱ · `న` 0.48 · `్` 0.35 · `న` 0.26✱ · `␣తే` 0.02 · `న` 0.41 · `ె` 0.07 · `న` 0.29 · `్` 0.95 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 81 tokens · 13.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిక్రియా మధుర ఘ్ర్వ్తమ్యెనకల్యలయ్యం | `UUIUIIIUIIUIUU` |
| 2 | తల్లిప్రణయ్న సతృదై నిరవృత్తి సారం | `UUIUIIIUIIUIUU` |
| 3 | తల్లిక్రియే జగతి న్య్య్థా నమకల్యదానం | `UUIUIIIUIIUIUU` |
| 4 | తల్లిక్రియా సుమధు దైవము సత్యశారం | `UUIUIIIUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.030 · model's first choice kept 43% · constraint overrode 40% · backtracks 0

<details><summary>Token probabilities (81 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.82 · `ల్లి` 0.78 · `క` 0.02✱ · `్రి` 7.7e-7✱ · `యా` 0.74 · `␣మ` 0.05 · `ధు` 0.80 · `ర` 0.71 · `␣ఘ` 3.6e-3✱ · `్ర` 4.8e-7✱ · `్వ` 9.1e-7✱ · `్` 1.1e-4✱ · `త` 0.01✱ · `మ` 0.03✱ · `్య` 0.05 · `ె` 0.10✱ · `న` 0.42 · `క` 0.02✱ · `ల` 0.09 · `్య` 7.9e-3✱ · `ల` 0.02✱ · `య` 0.02✱ · `్యం` 4.1e-5✱ · `⏎` 0.94 forced |
| 2 | `త` 0.66 · `ల్లి` 0.85 · `ప్ర` 0.19 · `ణ` 1.0e-3✱ · `య` 0.94 · `్` 1.2e-3✱ · `న` 0.57 · `␣స` 0.04 · `త` 0.02✱ · `ృ` 0.05✱ · `ద` 8.1e-4✱ · `ై` 0.13 · `␣ని` 0.07 · `ర` 0.07✱ · `వ` 0.02✱ · `ృ` 0.05 · `త్తి` 0.61 · `␣స` 0.04 · `ారం` 0.02 · `⏎` 0.07 forced |
| 3 | `త` 0.96 · `ల్లి` 0.92 · `క` 0.15 · `్రియ` 4.1e-7✱ · `ే` 0.60 · `␣జగ` 0.18 · `తి` 0.79 · `␣న` 0.10✱ · `్య` 1.4e-4✱ · `్య` 6.3e-4✱ · `్` 6.2e-4✱ · `థ` 9.6e-3✱ · `ా` 0.18 · `␣న` 0.05 · `మ` 0.10✱ · `క` 0.04✱ · `ల` 0.36 · `్య` 0.24 · `ద` 0.01 · `ానం` 0.01 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ల్లి` 0.94 · `క` 0.05 · `్రి` 8.7e-6✱ · `యా` 0.88 · `␣సు` 0.05 · `మ` 0.24 · `ధు` 0.40 · `␣ద` 3.1e-4✱ · `ై` 0.63 · `వ` 0.84 · `ము` 0.08 · `␣స` 0.10 · `త్య` 0.55 · `శ` 0.03 · `ారం` 0.28 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 92 tokens · 14.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామచ్రియున్ లఘుము త్వ్రయ్నమునై లవణ్యా | `UUIUIIIUIIUIUU` |
| 2 | సౌమయ్యునిన్ రణము న్య్య్చై రణగణ్యమున్రో | `UUIUIIIUIIUIUU` |
| 3 | సీమగ్రుణీని రణచీతమునై నివారే | `UUIUIIIUIIUIUU` |
| 4 | రామచ్రియున్ లఘుము త్వ్రయ్నమునై నమస్తే | `UUIUIIIUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.060 · model's first choice kept 45% · constraint overrode 38% · backtracks 0

<details><summary>Token probabilities (92 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.27 · `మ` 0.84 · `చ` 0.81 · `్రి` 1.6e-5✱ · `యు` 0.28 · `న్` 0.09✱ · `␣ల` 0.31 · `ఘ` 1.0e-4✱ · `ు` 0.98 · `ము` 0.07 · `␣త` 0.01✱ · `్వ` 0.09✱ · `్ర` 3.0e-6✱ · `య` 0.20✱ · `్` 0.02✱ · `న` 0.42 · `ము` 0.06 · `న` 0.12 · `ై` 0.01✱ · `␣ల` 0.11 · `వ` 1.9e-4✱ · `ణ` 0.90 · `్యా` 7.5e-4✱ · `⏎` 0.48 forced |
| 2 | `స` 0.04 · `ౌ` 0.02✱ · `మ` 2.9e-3✱ · `య` 0.03✱ · `్య` 4.1e-3✱ · `ు` 0.18 · `ని` 0.32✱ · `న్` 0.03✱ · `␣ర` 0.26 · `ణ` 5.9e-3✱ · `ము` 0.56 · `␣న` 0.01✱ · `్య` 5.5e-4✱ · `్య` 3.5e-3✱ · `్` 4.3e-4✱ · `చ` 0.02✱ · `ై` 0.11✱ · `␣ర` 0.10 · `ణ` 0.06✱ · `గ` 0.02 · `ణ` 0.16 · `్య` 0.16✱ · `ము` 0.23 · `న` 0.44 · `్రో` 1.2e-5✱ · `⏎` 0.37 forced |
| 3 | `సీ` 0.35 · `మ` 1.4e-4✱ · `గ` 0.03 · `్రు` 8.1e-3✱ · `ణ` 0.21 · `ీ` 0.16✱ · `ని` 0.18 · `␣ర` 0.59 · `ణ` 3.5e-3✱ · `చ` 2.9e-3✱ · `ీ` 3.3e-3✱ · `త` 0.53 · `ము` 0.58 · `న` 0.25 · `ై` 0.80 · `␣ని` 0.03 · `వ` 0.28 · `ార` 0.57 · `ే` 1.1e-3 · `⏎` 0.03 forced |
| 4 | `రా` 0.05 · `మ` 0.85 · `చ` 0.61 · `్రి` 0.29✱ · `యు` 0.91 · `న్` 0.84 · `␣ల` 0.15 · `ఘ` 0.94 · `ు` 1.00 · `ము` 0.97 · `␣త` 0.73 · `్వ` 0.98 · `్ర` 0.99 · `య` 0.99 · `్` 0.99 · `న` 1.00 · `ము` 0.99 · `న` 0.98 · `ై` 0.98 · `␣న` 0.02 · `మ` 0.15 · `స్తే` 0.02 |

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

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 72 tokens · 11.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వాయుగ్రుడై సాగి లొపల్యెనున్రో | `UUIUUIIUIUU` |
| 2 | చైయోజనమ్రోచి లొసల్యెనున్రో | `UUIUUIIUIUU` |
| 3 | శ్రీయుగ్యమై సాగి లొసెల్యెనున్రో | `UUIUUIIUIUU` |
| 4 | రా యుద్ధమందున్యెను ల్య్య్రయ్యెనున్రో | `UUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 9% · repeated lines 0 · mean token probability (geometric) 0.038 · model's first choice kept 49% · constraint overrode 41% · backtracks 0

<details><summary>Token probabilities (72 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.42 · `ాయ` 1.00 · `ు` 1.00 · `గ` 0.02✱ · `్రు` 7.5e-5✱ · `డ` 0.94 · `ై` 0.45 · `␣సా` 0.28 · `గి` 0.65 · `␣ల` 0.17 · `ొ` 3.7e-5✱ · `ప` 6.6e-6✱ · `ల` 0.17✱ · `్య` 3.5e-4✱ · `ె` 0.06 · `ను` 0.55 · `న` 7.8e-4✱ · `్రో` 1.1e-3✱ · `⏎` 0.02 forced |
| 2 | `చ` 0.03 · `ై` 0.03✱ · `యోజ` 4.2e-8✱ · `న` 0.71 · `మ` 0.03✱ · `్రో` 0.04✱ · `చి` 0.05 · `␣ల` 0.37 · `ొ` 9.2e-4✱ · `స` 3.2e-3✱ · `ల` 0.60 · `్య` 0.34 · `ె` 0.88 · `ను` 0.76 · `న` 0.32 · `్రో` 0.98 · `⏎` 1.00 forced |
| 3 | `శ` 0.10 · `్రీ` 0.03✱ · `యు` 4.8e-4✱ · `గ` 0.75 · `్య` 3.1e-3✱ · `మై` 0.10 · `␣సా` 0.28 · `గి` 0.87 · `␣ల` 0.77 · `ొ` 0.31✱ · `స` 0.14 · `ెల` 1.0e-3✱ · `్య` 0.91 · `ె` 0.99 · `ను` 0.94 · `న` 0.99 · `్రో` 1.00 · `⏎` 1.00 forced |
| 4 | `రా` 0.02✱ · `␣యుద్ధ` 3.0e-7✱ · `మ` 0.17 · `ందు` 0.09✱ · `న` 0.30 · `్య` 2.6e-4✱ · `ె` 0.57 · `ను` 0.48 · `␣ల` 0.55 · `్య` 1.5e-4✱ · `్య` 4.0e-4✱ · `్ర` 3.1e-6✱ · `య` 0.10✱ · `్య` 1.0e-3✱ · `ె` 0.98 · `ను` 0.99 · `న` 0.97 · `్రో` 1.00 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 125 tokens · 20.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మహ్యుగ్యమున్యుగ్యము ర్వ్ణ్మయ్న త్వం ఝుం | `UUIUUIIUIUU` |
| 2 | కౌహ్యన్ధ్రయత్యుం త్వమృగన్ ఝుమన్ ఝుం | `UUIUUIIUIUU` |
| 3 | దూహ్యుం త్వమృగ్యుం ర్వ్ణ్మయ త్వుం ఝుమన్ ఝుం | `UUIUUIIUIUU` |
| 4 | నృహ్యుం త్వమృగ్యుం త్వమృగృం ఝుమన్ ఝుం | `UUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 0% · single-akshara words 32% · repeated lines 0 · mean token probability (geometric) 0.128 · model's first choice kept 63% · constraint overrode 30% · backtracks 0

<details><summary>Token probabilities (125 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.03 · `హ` 0.43 · `్య` 7.7e-5✱ · `ు` 0.13 · `గ` 0.03 · `్య` 0.12✱ · `ము` 0.28 · `న` 0.40 · `్య` 1.9e-4✱ · `ు` 0.28 · `గ` 0.34 · `్య` 0.89 · `ము` 0.70 · `␣ర` 8.5e-3✱ · `్వ` 6.1e-7✱ · `్` 3.7e-4✱ · `ణ` 0.32 · `్` 2.0e-4✱ · `మ` 0.01✱ · `య` 0.13✱ · `్` 5.4e-3✱ · `న` 0.54 · `␣త` 0.02✱ · `్వ` 0.39 · `ం` 0.67 · `␣` 5.5e-3✱ · `ఝ` 0.39 · `ు` 0.24 · `ం` 0.30 · `⏎` 0.27 forced |
| 2 | `క` 0.09 · `ౌ` 0.09✱ · `హ` 3.5e-6✱ · `్` 1.6e-3✱ · `య` 2.2e-5✱ · `న` 0.02✱ · `్` 0.03✱ · `ధ` 0.27 · `్ర` 0.14 · `య` 0.16 · `త` 8.7e-3✱ · `్య` 0.02✱ · `ు` 0.50 · `ం` 0.41 · `␣త` 0.13 · `్వ` 0.68 · `మ` 7.0e-3✱ · `ృ` 0.07✱ · `గ` 0.25 · `న్` 0.07✱ · `␣` 0.25 · `ఝ` 0.93 · `ు` 0.76 · `మ` 7.4e-3✱ · `న్` 0.03✱ · `␣` 0.05✱ · `ఝ` 0.92 · `ు` 0.88 · `ం` 0.97 · `⏎` 1.00 forced |
| 3 | `ద` 0.03 · `ూ` 0.18✱ · `హ` 6.9e-4✱ · `్య` 0.59 · `ు` 0.45 · `ం` 0.38 · `␣త` 0.17 · `్వ` 0.80 · `మ` 0.36✱ · `ృ` 0.29 · `గ` 0.85 · `్య` 0.10✱ · `ు` 0.83 · `ం` 0.96 · `␣ర` 0.17 · `్వ` 0.73 · `్` 0.94 · `ణ` 0.94 · `్` 0.81 · `మ` 0.91 · `య` 0.93 · `␣త` 6.5e-3✱ · `్వ` 0.81 · `ు` 2.2e-3✱ · `ం` 0.91 · `␣` 0.85 · `ఝ` 0.99 · `ు` 0.97 · `మ` 0.11✱ · `న్` 0.92 · `␣` 0.80 · `ఝ` 1.00 · `ు` 1.00 · `ం` 1.00 · `⏎` 1.00 forced |
| 4 | `న` 0.06 · `ృ` 0.04✱ · `హ` 0.01✱ · `్య` 0.63 · `ు` 0.98 · `ం` 0.95 · `␣త` 0.87 · `్వ` 0.96 · `మ` 0.92 · `ృ` 0.90 · `గ` 0.98 · `్య` 0.86 · `ు` 0.99 · `ం` 1.00 · `␣త` 0.30 · `్వ` 0.95 · `మ` 0.62 · `ృ` 0.49 · `గ` 0.94 · `ృ` 4.4e-7✱ · `ం` 0.90 · `␣` 0.83 · `ఝ` 1.00 · `ు` 0.98 · `మ` 0.79 · `న్` 0.98 · `␣` 0.97 · `ఝ` 1.00 · `ు` 1.00 · `ం` 0.99 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 72 tokens · 28.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిద్యమిన్ కంటిచొ ప్య్ర్తాన శాంతిం | `UUIUUIIUIUU` |
| 2 | తల్లిద్యమిన్ హృద్యపు దైవమా నిశ్ | `UUIUUIIUIUU` |
| 3 | తల్లిద్యమిన్ కన్నతొ దైవమా నిశ్ | `UUIUUIIUIUU` |
| 4 | తల్లిద్యమిన్ ప్రేమన ప్య్ర్తాన శాంతిం | `UUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.088 · model's first choice kept 60% · constraint overrode 33% · backtracks 30

<details><summary>Token probabilities (72 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.80 · `ల్లి` 0.78 · `ద` 0.01✱ · `్య` 3.2e-8✱ · `మి` 7.7e-3✱ · `న్` 0.12✱ · `␣క` 0.07 · `ంటి` 4.1e-3✱ · `చ` 0.51 · `ొ` 7.9e-6✱ · `␣ప` 3.6e-4✱ · `్య` 7.4e-4✱ · `్ర` 9.2e-6✱ · `్` 1.6e-5✱ · `త` 4.4e-3✱ · `ాన` 0.01✱ · `␣శా` 8.1e-4 · `ంతి` 0.33 · `ం` 0.05✱ · `⏎` 0.71 forced |
| 2 | `త` 0.63 · `ల్లి` 0.84 · `ద` 0.39 · `్య` 0.98 · `మి` 0.93 · `న్` 1.00 · `␣హ` 0.22 · `ృ` 0.99 · `ద` 0.28✱ · `్య` 9.3e-4✱ · `పు` 0.03✱ · `␣ద` 0.04✱ · `ై` 0.63 · `వ` 0.89 · `మా` 0.14 · `␣ని` 0.12 · `శ్` 0.03✱ · `⏎` 3.1e-8 forced |
| 3 | `త` 0.98 · `ల్లి` 0.93 · `ద` 0.88 · `్య` 0.99 · `మి` 0.97 · `న్` 1.00 · `␣క` 0.13 · `న్న` 0.01✱ · `త` 0.24 · `ొ` 0.09✱ · `␣ద` 0.09 · `ై` 0.28 · `వ` 0.92 · `మా` 0.65 · `␣ని` 0.11 · `శ్` 0.52 · `⏎` 0.65 forced |
| 4 | `త` 0.97 · `ల్లి` 0.99 · `ద` 0.96 · `్య` 1.00 · `మి` 0.99 · `న్` 1.00 · `␣ప్రేమ` 0.20 · `న` 0.01✱ · `␣ప` 0.03✱ · `్య` 0.02✱ · `్ర` 0.87 · `్` 0.95 · `త` 0.94 · `ాన` 0.92 · `␣శా` 0.21 · `ంతి` 0.95 · `ం` 1.00 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 85 tokens · 28.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వాయుద్వజం దేహముపై శిరియ్యే | `UUIUUIIUIUU` |
| 2 | గీయాం రఘువ్యాసము ధ్వ్వ్కృత్యయేయే | `UUIUUIIUIUU` |
| 3 | సాయిల్వనియ్నగ్రుడె ల్వ్ల్చర్యయేయే | `UUIUUIIUIUU` |
| 4 | వాయుగ్రుడెన్నై లవ గ్న్య్వత్యయేయే | `UUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.020 · model's first choice kept 38% · constraint overrode 57% · backtracks 30

<details><summary>Token probabilities (85 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.42 · `ాయ` 1.00 · `ు` 1.00 · `ద` 7.0e-3✱ · `్వ` 8.2e-8✱ · `జ` 0.78 · `ం` 0.34✱ · `␣ద` 0.03 · `ే` 0.24 · `హ` 0.24 · `ము` 0.67 · `పై` 0.04✱ · `␣శి` 3.7e-3 · `రి` 0.09 · `య` 0.21 · `్య` 1.1e-3✱ · `ే` 0.09 · `⏎` 0.06 forced |
| 2 | `గ` 0.20 · `ీ` 0.02✱ · `యా` 2.1e-7✱ · `ం` 0.12 · `␣ర` 0.01 · `ఘ` 0.60 · `ు` 1.00 · `వ` 0.09✱ · `్యా` 1.2e-5✱ · `స` 0.53 · `ము` 0.16 · `␣ధ` 0.02✱ · `్వ` 0.05✱ · `్వ` 4.7e-8✱ · `్` 8.6e-8✱ · `క` 2.0e-4✱ · `ృత` 9.5e-3✱ · `్య` 0.03✱ · `యే` 1.7e-3✱ · `యే` 1.5e-5✱ · `⏎` 1.00 forced |
| 3 | `స` 0.49 · `ాయి` 2.0e-4✱ · `ల` 0.33 · `్వ` 4.1e-4✱ · `ని` 0.02✱ · `య` 0.03✱ · `్` 0.02✱ · `న` 0.34 · `గ` 2.8e-3✱ · `్రు` 1.3e-3✱ · `డ` 0.50 · `ె` 0.04✱ · `␣ల` 0.17✱ · `్వ` 5.0e-6✱ · `్` 0.01✱ · `ల` 0.09 · `్` 1.4e-3✱ · `చ` 1.9e-3✱ · `ర` 0.04✱ · `్య` 0.08✱ · `యే` 0.54 · `యే` 0.13✱ · `⏎` 1.00 forced |
| 4 | `వ` 0.08✱ · `ాయ` 0.56 · `ు` 0.98 · `గ` 0.18✱ · `్రు` 0.01✱ · `డ` 0.94 · `ె` 0.89 · `న` 0.04✱ · `్` 1.2e-3✱ · `న` 0.17 · `ై` 0.03✱ · `␣ల` 0.86 · `వ` 3.7e-4✱ · `␣గ` 4.2e-4✱ · `్` 3.7e-3✱ · `న` 0.36 · `్య` 0.14✱ · `్` 0.02✱ · `వ` 8.5e-3✱ · `త` 0.18✱ · `్య` 0.87 · `యే` 0.97 · `యే` 0.99 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 78 tokens · 13.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాతృప్రణయ్నై నిరమాన సారం | `UUIUUIIUIUU` |
| 2 | కౌతన్యమున్రోవన ద్య్వ్ఘన్న సారం | `UUIUUIIUIUU` |
| 3 | జాతర్యునై దైవము ఘ్న్య్చై నిరారం | `UUIUUIIUIUU` |
| 4 | మాతృప్రియా దైవము స్ర్వ్మన్న సారం | `UUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.039 · model's first choice kept 44% · constraint overrode 41% · backtracks 0

<details><summary>Token probabilities (78 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.11 · `త` 0.97 · `ృ` 0.97 · `ప్ర` 0.37 · `ణ` 2.6e-4✱ · `య` 0.96 · `్` 4.0e-5✱ · `న` 0.76 · `ై` 0.03✱ · `␣ని` 0.15 · `ర` 0.02✱ · `మా` 3.5e-5✱ · `న` 0.89 · `␣స` 0.09 · `ారం` 6.3e-3 · `⏎` 0.08 forced |
| 2 | `క` 0.04 · `ౌ` 1.3e-3✱ · `త` 0.04✱ · `న్య` 0.25 · `ము` 0.22 · `న` 0.43 · `్రో` 1.3e-4✱ · `వ` 0.57 · `న` 0.10 · `␣ద` 0.05✱ · `్య` 1.9e-3✱ · `్వ` 2.8e-7✱ · `్` 3.3e-4✱ · `ఘ` 0.02✱ · `న` 0.51 · `్` 2.3e-4✱ · `న` 0.43 · `␣స` 0.14 · `ారం` 0.86 · `⏎` 1.00 forced |
| 3 | `జ` 0.07 · `ాత` 3.3e-3✱ · `ర` 0.63 · `్య` 1.5e-3✱ · `ు` 0.17 · `న` 0.06 · `ై` 0.04✱ · `␣ద` 0.06 · `ై` 0.65 · `వ` 0.91 · `ము` 0.19 · `␣ఘ` 4.9e-3✱ · `్` 2.9e-5✱ · `న` 0.82 · `్య` 3.3e-3✱ · `్` 0.03✱ · `చ` 5.0e-4✱ · `ై` 0.08✱ · `␣ని` 0.07 · `ర` 0.34 · `ారం` 0.09✱ · `⏎` 0.92 forced |
| 4 | `మ` 0.09 · `ాత` 0.02✱ · `ృ` 0.98 · `ప` 0.05 · `్రి` 0.40 · `యా` 0.69 · `␣ద` 0.03 · `ై` 0.63 · `వ` 0.91 · `ము` 0.33 · `␣స` 0.05✱ · `్ర` 2.7e-3✱ · `్వ` 2.9e-4✱ · `్` 0.39 · `మ` 0.02✱ · `న` 0.06✱ · `్` 5.5e-3✱ · `న` 0.84 · `␣స` 0.69 · `ారం` 1.00 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 77 tokens · 5.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రక్షించు తానొక్యు లొ రంగమున్రో | `UUIUUIIUIUU` |
| 2 | దూక్షమ్యు సీతమ్మను త్వుక్యు పోవో | `UUIUUIIUIUU` |
| 3 | భీక్షుర్యు లంకా నగపించు త్వుక్యం | `UUIUUIIUIUU` |
| 4 | విక్షమ్యు రక్షణ్యు త్వువించు త్వుక్యం | `UUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.038 · model's first choice kept 45% · constraint overrode 39% · backtracks 0

<details><summary>Token probabilities (77 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ర` 0.03 · `క్ష` 0.79 · `ించు` 0.84 · `␣త` 0.06✱ · `ాన` 0.12 · `ొ` 0.02 · `క` 0.95 · `్య` 1.1e-6✱ · `ు` 0.29 · `␣ల` 0.15 · `ొ` 1.4e-4✱ · `␣రంగ` 5.7e-6✱ · `ము` 0.43 · `న` 0.52 · `్రో` 5.7e-5✱ · `⏎` 0.03 forced |
| 2 | `ద` 0.03 · `ూ` 0.47 · `క` 5.2e-5✱ · `్` 6.9e-8✱ · `ష` 8.5e-4✱ · `మ` 0.03✱ · `్య` 0.10✱ · `ు` 0.58 · `␣సీ` 0.04 · `త` 0.53 · `మ్మ` 0.23 · `ను` 0.22 · `␣త` 0.03 · `్వ` 0.02✱ · `ు` 1.8e-4✱ · `క` 8.6e-3✱ · `్య` 0.08✱ · `ు` 0.79 · `␣పో` 0.05 · `వో` 6.9e-3✱ · `⏎` 1.00 forced |
| 3 | `భ` 0.13 · `ీ` 0.04✱ · `క్ష` 1.8e-4✱ · `ు` 0.17✱ · `ర` 0.09✱ · `్య` 2.7e-3✱ · `ు` 0.97 · `␣ల` 0.49 · `ం` 0.56 · `కా` 0.78 · `␣నగ` 0.03✱ · `ప` 2.1e-4✱ · `ించు` 0.01✱ · `␣త` 0.62 · `్వ` 0.75 · `ు` 0.94 · `క` 0.78 · `్యం` 0.09 · `⏎` 0.84 forced |
| 4 | `వి` 0.06 · `క` 4.5e-3✱ · `్` 8.5e-5✱ · `ష` 5.4e-4✱ · `మ` 0.23 · `్య` 0.98 · `ు` 1.00 · `␣ర` 0.13 · `క్షణ` 0.11 · `్య` 9.2e-3✱ · `ు` 0.95 · `␣త` 0.20 · `్వ` 0.66 · `ు` 0.92 · `వ` 8.7e-4✱ · `ించు` 0.01✱ · `␣త` 0.14 · `్వ` 0.70 · `ు` 0.79 · `క` 0.63 · `్యం` 0.82 |

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

<details><summary>Prompt (topic T2; the other topics differ only in the topic line)</summary>

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

Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 71 tokens · 11.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సముద్ర తీరంబున సాగెనున్రో | `IUIUUIIUIUU` |
| 2 | శ్రమల్రు చెద్రుర్రున సాగితిన్ముం | `IUIUUIIUIUU` |
| 3 | దుమల్రు గాలల్రున ల్వ్వ్దోచ్యెనున్ముం | `IUIUUIIUIUU` |
| 4 | శృమల్రు రక్షించుట ధ్యేయమాయెన్ | `IUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.049 · model's first choice kept 45% · constraint overrode 44% · backtracks 0

<details><summary>Token probabilities (71 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 0.04✱ · `ము` 0.15 · `ద్ర` 0.88 · `␣తీ` 0.22✱ · `రం` 0.23 · `బు` 0.70 · `న` 0.97 · `␣సా` 0.34 · `గ` 0.60 · `ె` 0.98 · `ను` 0.73 · `న` 2.0e-4✱ · `్రో` 3.5e-3✱ · `⏎` 2.3e-4 forced |
| 2 | `శ` 0.15 · `్రమ` 0.01✱ · `ల` 0.14 · `్రు` 1.5e-4✱ · `␣చె` 0.04 · `ద` 0.17 · `్రు` 5.6e-3✱ · `ర` 0.01✱ · `్రు` 9.9e-5✱ · `న` 0.03 · `␣సా` 0.09 · `గి` 0.15 · `తి` 0.31 · `న్` 0.24 · `ము` 1.9e-3✱ · `ం` 2.7e-3✱ · `⏎` 0.98 forced |
| 3 | `దు` 0.04✱ · `మ` 1.6e-6✱ · `ల` 0.10✱ · `్రు` 0.03✱ · `␣గా` 0.01 · `ల` 0.34 · `ల` 0.33 · `్రు` 0.18 · `న` 0.41 · `␣ల` 0.02✱ · `్వ` 3.7e-6✱ · `్వ` 4.4e-4✱ · `్` 2.2e-3✱ · `ద` 1.0e-2✱ · `ో` 0.04✱ · `చ` 0.07✱ · `్య` 0.35 · `ె` 0.24 · `ను` 0.44 · `న్` 0.02✱ · `ము` 9.1e-4✱ · `ం` 0.35✱ · `⏎` 1.00 forced |
| 4 | `శ` 0.11✱ · `ృ` 0.01✱ · `మ` 1.7e-3✱ · `ల` 0.92 · `్రు` 0.95 · `␣ర` 0.38 · `క్ష` 0.76 · `ించు` 0.62 · `ట` 0.31 · `␣ధ` 0.01 · `్య` 0.01✱ · `ే` 0.15✱ · `య` 0.83 · `మ` 0.17 · `ాయ` 0.50 · `ె` 1.00 · `న్` 0.75 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 93 tokens · 19.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వనమ్రయెన్రుత్యము ద్య్వస్రయెన్రుత్ | `IUIUUIIUIUU` |
| 2 | సనగ్రుడై సంద్రము త్ర్య్చైత్రయెన్రుత్ | `IUIUUIIUIUU` |
| 3 | లొనగ్రుడై లంకము త్ర్య్లోకయెన్రుత్ | `IUIUUIIUIUU` |
| 4 | శనగ్రుడై సంద్రము త్ర్య్చైత్రయెన్రుత్ | `IUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.132 · model's first choice kept 57% · constraint overrode 34% · backtracks 0

<details><summary>Token probabilities (93 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.34 · `న` 1.3e-3✱ · `మ` 0.11✱ · `్ర` 0.01✱ · `య` 0.12 · `ె` 0.04✱ · `న` 0.18✱ · `్రు` 7.9e-4✱ · `త` 0.01✱ · `్య` 3.9e-3✱ · `ము` 0.19 · `␣ద` 0.05✱ · `్య` 6.9e-3✱ · `్వ` 7.0e-6✱ · `స` 0.45 · `్ర` 2.5e-3✱ · `య` 0.27 · `ె` 0.26✱ · `న` 0.64 · `్రు` 0.72 · `త` 0.71 · `్` 1.3e-5✱ · `⏎` 0.03 forced |
| 2 | `స` 0.10 · `న` 3.2e-4✱ · `గ` 0.09 · `్రు` 9.4e-3✱ · `డ` 0.20 · `ై` 0.10✱ · `␣స` 0.07 · `ంద్ర` 0.02✱ · `ము` 0.62 · `␣త` 0.08✱ · `్ర` 0.05✱ · `్య` 1.1e-4✱ · `్` 7.1e-4✱ · `చ` 0.01✱ · `ై` 0.06✱ · `త` 0.26 · `్ర` 0.09✱ · `య` 0.80 · `ె` 0.81 · `న` 0.88 · `్రు` 0.97 · `త` 0.99 · `్` 0.97 · `⏎` 1.00 forced |
| 3 | `ల` 0.23✱ · `ొ` 2.6e-3✱ · `న` 0.05✱ · `గ` 0.29 · `్రు` 0.81 · `డ` 0.90 · `ై` 0.92 · `␣ల` 0.96 · `ంక` 0.68 · `ము` 0.16 · `␣త` 0.40 · `్ర` 0.51 · `్య` 0.88 · `్` 0.70 · `లో` 2.0e-3✱ · `క` 0.63 · `య` 0.22 · `ె` 0.98 · `న` 1.00 · `్రు` 1.00 · `త` 1.00 · `్` 1.00 · `⏎` 1.00 forced |
| 4 | `శ` 0.09 · `న` 0.10✱ · `గ` 0.70 · `్రు` 0.99 · `డ` 0.99 · `ై` 0.98 · `␣స` 0.16 · `ంద్ర` 0.01✱ · `ము` 0.56 · `␣త` 0.58 · `్ర` 0.75 · `్య` 0.95 · `్` 0.79 · `చ` 0.55 · `ై` 0.94 · `త` 0.90 · `్ర` 0.94 · `య` 0.99 · `ె` 0.99 · `న` 0.97 · `్రు` 0.99 · `త` 1.00 · `్` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 74 tokens · 27.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవన్రదూషం గమ వ్యాగనమ్యే | `IUIUUIIUIUU` |
| 2 | శెవిత్య నేట్యన్ లకశేషమున్యే | `IUIUUIIUIUU` |
| 3 | వృవత్య సంధ్యేన సకృప్యెనైవ్యం | `IUIUUIIUIUU` |
| 4 | నవద్యెనై సంద్రమయమ్యెనైవ్యం | `IUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.033 · model's first choice kept 38% · constraint overrode 46% · backtracks 30

<details><summary>Token probabilities (74 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.27 · `వ` 0.43 · `న` 0.99 · `్ర` 1.3e-6✱ · `ద` 3.1e-3✱ · `ూ` 0.26✱ · `ష` 0.44 · `ం` 0.24 · `␣గ` 0.06✱ · `మ` 0.62 · `␣వ్యా` 1.9e-5✱ · `గ` 0.04 · `న` 0.01 · `మ` 0.02✱ · `్య` 0.02✱ · `ే` 0.37 · `⏎` 0.19 forced |
| 2 | `శ` 0.14 · `ె` 4.0e-4✱ · `విత` 2.4e-4✱ · `్య` 9.1e-3✱ · `␣నే` 3.7e-4✱ · `ట` 0.01 · `్య` 0.34 · `న్` 0.01 · `␣ల` 0.47 · `క` 3.5e-5✱ · `శ` 4.6e-3✱ · `ే` 0.21 · `ష` 0.10 · `ము` 0.03✱ · `న` 0.13✱ · `్య` 2.7e-3✱ · `ే` 0.99 · `⏎` 1.00 forced |
| 3 | `వ` 0.11 · `ృ` 3.6e-4✱ · `వ` 1.6e-5✱ · `త` 0.18 · `్య` 0.11 · `␣సం` 0.02 · `ధ` 0.35 · `్య` 0.23 · `ే` 0.48 · `న` 0.10 · `␣స` 0.06 · `క` 0.01✱ · `ృ` 8.9e-3✱ · `ప` 0.83 · `్య` 0.30 · `ె` 0.02✱ · `న` 0.52 · `ై` 0.12✱ · `వ` 1.5e-3✱ · `్యం` 2.3e-4✱ · `⏎` 0.99 forced |
| 4 | `న` 0.02 · `వ` 0.22✱ · `ద` 0.02 · `్య` 4.2e-3✱ · `ె` 0.02✱ · `న` 0.45 · `ై` 0.06✱ · `␣స` 0.07 · `ంద్ర` 0.01✱ · `మ` 0.11✱ · `య` 0.02✱ · `మ` 0.06✱ · `్య` 0.56 · `ె` 0.01✱ · `న` 0.37 · `ై` 0.88 · `వ` 0.85 · `్యం` 0.98 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 109 tokens · 35.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శముద్రమున్నన్ ధ్యన జ్వల్యునిన్యుమ్ | `IUIUUIIUIUU` |
| 2 | గమయ్యమున్నన్ భవ జ్వ్య్ఘన్యునమ్ ఝుమ్ | `IUIUUIIUIUU` |
| 3 | లొమక్యునన్ ధ్యన్యున ఝ్య్వ్లొక్యునమ్ ఝుమ్ | `IUIUUIIUIUU` |
| 4 | శముద్ర్యునన్ ధ్యన్యున ఝ్య్వ్లమ్యునమ్ ఝుమ్ | `IUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 7% · single-akshara words 20% · repeated lines 0 · mean token probability (geometric) 0.120 · model's first choice kept 57% · constraint overrode 38% · backtracks 30

<details><summary>Token probabilities (109 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.10 · `ము` 0.07✱ · `ద` 0.17 · `్ర` 0.61 · `ము` 0.43✱ · `న` 0.07✱ · `్` 1.2e-4✱ · `న` 0.42 · `న్` 7.9e-4✱ · `␣ధ` 0.02✱ · `్య` 0.04✱ · `న` 0.03✱ · `␣జ` 3.0e-3✱ · `్వ` 0.14 · `ల` 0.57 · `్య` 0.01✱ · `ు` 0.18 · `ని` 0.17 · `న` 0.01✱ · `్య` 2.2e-3✱ · `ు` 0.28 · `మ్` 7.2e-3✱ · `⏎` 0.94 forced |
| 2 | `గ` 0.07✱ · `మ` 0.58 · `య` 0.11✱ · `్య` 0.03✱ · `ము` 0.04 · `న` 0.60 · `్` 0.24✱ · `న` 0.98 · `న్` 0.96 · `␣భ` 0.08 · `వ` 0.12✱ · `␣జ` 0.10✱ · `్వ` 0.39 · `్య` 6.2e-7✱ · `్` 2.7e-4✱ · `ఘ` 2.5e-3✱ · `న` 0.50 · `్య` 0.29 · `ు` 0.97 · `న` 0.03✱ · `మ్` 0.52 · `␣` 2.4e-5✱ · `ఝ` 0.23✱ · `ు` 0.33 · `మ్` 0.74 · `⏎` 1.00 forced |
| 3 | `ల` 0.13✱ · `ొ` 3.4e-3✱ · `మ` 3.5e-6✱ · `క` 0.67 · `్య` 0.02✱ · `ు` 0.44 · `న` 0.52 · `న్` 0.17✱ · `␣ధ` 0.21 · `్య` 0.64 · `న` 0.94 · `్య` 3.0e-4✱ · `ు` 0.85 · `న` 0.22✱ · `␣` 6.6e-3✱ · `ఝ` 0.92 · `్య` 0.25✱ · `్వ` 0.04✱ · `్` 0.11✱ · `ల` 0.02✱ · `ొ` 8.4e-4✱ · `క` 0.12 · `్య` 0.89 · `ు` 0.95 · `న` 0.52 · `మ్` 0.98 · `␣` 0.03✱ · `ఝ` 0.94 · `ు` 0.87 · `మ్` 0.95 · `⏎` 1.00 forced |
| 4 | `శ` 0.10 · `ము` 0.33 · `ద` 0.75 · `్ర` 0.90 · `్య` 0.30 · `ు` 0.98 · `న` 0.95 · `న్` 0.95 · `␣ధ` 0.52 · `్య` 0.94 · `న` 0.95 · `్య` 0.53 · `ు` 0.99 · `న` 0.92 · `␣` 0.46 · `ఝ` 1.00 · `్య` 0.76 · `్వ` 0.73 · `్` 0.83 · `ల` 0.91 · `మ` 0.02✱ · `్య` 0.32 · `ు` 0.97 · `న` 0.97 · `మ్` 0.99 · `␣` 0.90 · `ఝ` 1.00 · `ు` 1.00 · `మ్` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 67 tokens · 10.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సముద్ర తీరంబున సాగెనున్రో | `IUIUUIIUIUU` |
| 2 | శ్రమల్రు వీడెన్ జగ ద్య్రవ్యమున్రో | `IUIUUIIUIUU` |
| 3 | భ్రమల్రు తొల్రున్రు లవణ్యమున్రో | `IUIUUIIUIUU` |
| 4 | రమక్రియల్రున్రు ర ఘ్న్య్రంబునారో | `IUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 31% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.023 · model's first choice kept 40% · constraint overrode 52% · backtracks 0

<details><summary>Token probabilities (67 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 0.04✱ · `ము` 0.15 · `ద్ర` 0.88 · `␣తీ` 0.22✱ · `రం` 0.23 · `బు` 0.70 · `న` 0.97 · `␣సా` 0.34 · `గ` 0.60 · `ె` 0.98 · `ను` 0.73 · `న` 2.0e-4✱ · `్రో` 3.5e-3✱ · `⏎` 2.3e-4 forced |
| 2 | `శ` 0.15 · `్రమ` 0.01✱ · `ల` 0.14 · `్రు` 1.5e-4✱ · `␣వీ` 0.05 · `డ` 0.33 · `ె` 0.93 · `న్` 0.02✱ · `␣జగ` 0.04✱ · `␣ద` 1.9e-4✱ · `్య` 9.0e-3✱ · `్ర` 1.4e-7✱ · `వ` 0.13✱ · `్య` 1.6e-3✱ · `ము` 0.53 · `న` 0.24✱ · `్రో` 0.10✱ · `⏎` 1.00 forced |
| 3 | `భ` 0.03✱ · `్రమ` 0.01✱ · `ల` 0.53 · `్రు` 0.27 · `␣తొ` 0.15 · `ల` 1.00 · `్రు` 1.1e-7✱ · `న` 0.06✱ · `్రు` 9.4e-6✱ · `␣ల` 0.19 · `వ` 1.4e-4✱ · `ణ` 0.93 · `్య` 8.8e-4✱ · `ము` 0.34 · `న` 0.89 · `్రో` 1.00 · `⏎` 1.00 forced |
| 4 | `ర` 0.17✱ · `మ` 7.5e-6✱ · `క` 0.11✱ · `్రియ` 1.2e-3✱ · `ల` 0.26 · `్రు` 4.0e-3✱ · `న` 0.01✱ · `్రు` 0.54 · `␣ర` 0.55 · `␣ఘ` 4.5e-6✱ · `్` 7.9e-4✱ · `న` 0.94 · `్య` 0.07✱ · `్ర` 6.7e-5✱ · `ం` 0.01 · `బు` 0.81 · `న` 0.96 · `ారో` 7.3e-7✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 97 tokens · 6.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవన్దతుడ్యెన్ లవ గ్ణ్య్వణ్ద గమ్యం | `IUIUUIIUIUU` |
| 2 | జ్యెవల్ల కీర్తిన్ లొక ధ్వ్న్దృగ్య గమ్యం | `IUIUUIIUIUU` |
| 3 | స్రువగ్రుడెన్ లంకు వ య్జ్ణ్దో గమర్యం | `IUIUUIIUIUU` |
| 4 | వృవిన్ద్ద గమ్యం లవ మృగ్ద గమ్యం | `IUIUUIIUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 16% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.057 · model's first choice kept 45% · constraint overrode 43% · backtracks 0

<details><summary>Token probabilities (97 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.27 · `వ` 0.43 · `న` 0.98 · `్` 1.2e-5✱ · `ద` 0.30 · `తు` 6.1e-3✱ · `డ` 0.35✱ · `్య` 5.3e-3✱ · `ె` 0.41 · `న్` 0.13✱ · `␣ల` 0.54 · `వ` 1.4e-4✱ · `␣గ` 4.0e-3✱ · `్` 1.2e-4✱ · `ణ` 0.39 · `్య` 0.22 · `్` 0.01✱ · `వ` 7.9e-3✱ · `ణ` 0.03 · `్` 0.14 · `ద` 0.28 · `␣గ` 0.06 · `మ` 0.51 · `్యం` 5.2e-3 · `⏎` 0.60 forced |
| 2 | `జ` 0.03 · `్య` 0.03✱ · `ె` 0.10✱ · `వల` 5.3e-4✱ · `్` 0.65 · `ల` 0.72 · `␣క` 0.04✱ · `ీ` 0.18 · `ర్` 0.74 · `తి` 0.96 · `న్` 0.12✱ · `␣ల` 0.26 · `ొ` 1.8e-3✱ · `క` 0.12✱ · `␣ధ` 0.03 · `్వ` 0.04✱ · `్` 2.3e-5✱ · `న` 0.11✱ · `్` 0.47 · `ద` 0.64 · `ృ` 9.1e-8✱ · `గ` 0.04✱ · `్య` 3.8e-3✱ · `␣గ` 0.30 · `మ` 0.93 · `్యం` 0.95 · `⏎` 1.00 forced |
| 3 | `స` 0.36 · `్రు` 5.6e-5✱ · `వ` 0.32✱ · `గ` 0.02✱ · `్రు` 8.5e-3✱ · `డ` 0.36 · `ె` 0.08✱ · `న్` 0.87 · `␣ల` 0.41 · `ం` 0.53 · `కు` 6.6e-3✱ · `␣వ` 0.08✱ · `␣య` 0.02✱ · `్` 0.07✱ · `జ` 0.07 · `్` 0.23 · `ణ` 0.35 · `్` 0.80 · `ద` 0.96 · `ో` 8.6e-3✱ · `␣గ` 0.25 · `మ` 0.96 · `ర్` 4.9e-6✱ · `యం` 0.48 · `⏎` 1.00 forced |
| 4 | `వ` 0.11 · `ృ` 0.03✱ · `వి` 6.9e-6✱ · `న్` 0.06 · `ద` 0.61 · `్` 0.25 · `ద` 0.86 · `␣గ` 0.12✱ · `మ` 0.55 · `్యం` 0.36 · `␣ల` 0.22 · `వ` 0.07✱ · `␣మ` 0.01 · `ృ` 0.08✱ · `గ` 0.48 · `్` 0.36 · `ద` 0.35 · `␣గ` 0.16✱ · `మ` 0.93 · `్యం` 0.77 |

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

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 106 tokens · 17.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామచ్రియ్నన్ లంక గ్రామాన చేరిన్ | `UUUUUIUUIUU` |
| 2 | సీమల్యానన్ దేవి ర్వ్య్ణేనల్లునైన్ ఝుర్ | `UUUUUIUUIUU` |
| 3 | వ్యామన్ధిర్నన్ దేహ ర్వ్య్ణంబున్ నలక్కై | `UUUUUIUUIUU` |
| 4 | కైమర్తియ్నన్ రక్ష్యె ద్య్న్కై రఘ్ననాంస్సై | `UUUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.047 · model's first choice kept 41% · constraint overrode 44% · backtracks 0

<details><summary>Token probabilities (106 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.33 · `మ` 0.81 · `చ` 0.72 · `్రి` 2.0e-5✱ · `య` 0.03✱ · `్` 9.3e-3✱ · `న` 0.39 · `న్` 0.03✱ · `␣ల` 0.45 · `ం` 0.50 · `క` 0.03✱ · `␣గ` 0.02✱ · `్రా` 7.3e-6✱ · `మ` 0.68 · `ాన` 0.02✱ · `␣చే` 0.14 · `రి` 0.41 · `న` 0.13✱ · `్` 4.0e-6✱ · `⏎` 0.67 forced |
| 2 | `సీ` 0.81 · `మ` 1.0e-4✱ · `ల` 0.15 · `్యా` 6.0e-4✱ · `న` 0.19 · `న్` 0.47 · `␣ద` 0.10 · `ే` 0.42 · `వి` 0.59 · `␣ర` 0.20 · `్వ` 2.0e-6✱ · `్య` 1.4e-3✱ · `్` 0.01✱ · `ణ` 0.14 · `ే` 0.05✱ · `న` 0.40 · `ల` 2.4e-3✱ · `్` 1.8e-3✱ · `లు` 0.02✱ · `న` 0.06✱ · `ై` 0.19✱ · `న్` 0.02✱ · `␣` 5.1e-5✱ · `ఝ` 0.24✱ · `ు` 0.22 · `ర్` 0.02✱ · `⏎` 0.20 forced |
| 3 | `వ` 0.07 · `్యా` 2.1e-3✱ · `మ` 1.2e-3✱ · `న` 0.09✱ · `్` 7.7e-3✱ · `ధి` 0.04 · `ర` 0.15 · `్` 0.13✱ · `న` 0.14 · `న్` 0.80 · `␣ద` 0.14 · `ే` 0.31 · `హ` 0.63 · `␣ర` 0.09✱ · `్వ` 1.8e-4✱ · `్య` 0.56 · `్` 0.85 · `ణ` 0.79 · `ం` 0.03✱ · `బు` 0.03 · `న` 0.34 · `్` 0.02✱ · `␣న` 0.04 · `ల` 0.08✱ · `క` 0.13 · `్` 6.5e-3✱ · `క` 0.30 · `ై` 0.64 · `⏎` 0.02 forced |
| 4 | `క` 0.05 · `ై` 0.30 · `మ` 3.1e-3✱ · `ర్` 0.25 · `తి` 0.18 · `య` 0.50 · `్` 0.98 · `న` 0.97 · `న్` 0.96 · `␣ర` 0.34 · `క్ష` 0.76 · `్య` 0.06✱ · `ె` 0.12 · `␣ద` 6.9e-3✱ · `్య` 1.8e-3✱ · `్` 3.3e-3✱ · `న` 0.82 · `్` 6.0e-3✱ · `క` 4.1e-3✱ · `ై` 0.14 · `␣ర` 0.09 · `ఘ` 0.08 · `్` 3.8e-4✱ · `న` 0.91 · `నా` 5.2e-3 · `ం` 0.21 · `స` 0.01✱ · `్` 0.33 · `స` 0.47 · `ై` 0.41 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 85 tokens · 13.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామచ్రియ్నం లంక గ్రహ్యం భయానక్ | `UUUUUIUUIUU` |
| 2 | సీమల్రక్ష్యం తేజసృష్టిం ధనక్కళ్ | `UUUUUIUUIUU` |
| 3 | మౌమమ్రోచ్యం రక్ష్యుమందున్ నరక్కల్ | `UUUUUIUUIUU` |
| 4 | భూమిన్యమ్రాయం తపోమథ్యు నమ్రక్ | `UUUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.046 · model's first choice kept 38% · constraint overrode 44% · backtracks 0

<details><summary>Token probabilities (85 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.33 · `మ` 0.81 · `చ` 0.72 · `్రి` 2.0e-5✱ · `య` 0.03✱ · `్` 9.3e-3✱ · `న` 0.39 · `ం` 0.01✱ · `␣ల` 0.31 · `ం` 0.43 · `క` 0.02✱ · `␣గ` 0.02✱ · `్రహ` 2.2e-6✱ · `్య` 0.06✱ · `ం` 0.07✱ · `␣భ` 0.04✱ · `య` 0.65 · `ాన` 0.08✱ · `క` 0.58 · `్` 2.8e-7✱ · `⏎` 0.23 forced |
| 2 | `సీ` 0.68 · `మ` 8.7e-5✱ · `ల` 0.19 · `్ర` 1.7e-4✱ · `క్ష` 0.18 · `్య` 0.62 · `ం` 0.25 · `␣తే` 0.02 · `జ` 0.74 · `స` 0.04✱ · `ృష్టి` 4.3e-4✱ · `ం` 0.03✱ · `␣ధ` 0.06 · `న` 0.04✱ · `క` 0.10 · `్` 0.02✱ · `క` 9.1e-4✱ · `ళ` 0.05✱ · `్` 0.11✱ · `⏎` 0.88 forced |
| 3 | `మ` 0.07 · `ౌ` 1.6e-4✱ · `మ` 2.5e-4✱ · `మ` 0.01 · `్రో` 0.03✱ · `చ` 0.38 · `్య` 0.87 · `ం` 0.86 · `␣ర` 0.10 · `క్ష` 0.50 · `్య` 0.24 · `ు` 0.14✱ · `మ` 0.06✱ · `ందు` 0.38 · `న` 0.03✱ · `్` 5.7e-4✱ · `␣న` 0.20 · `ర` 0.22 · `క` 0.26 · `్` 0.86 · `క` 0.27✱ · `ల్` 0.10 · `⏎` 0.98 forced |
| 4 | `భ` 0.12 · `ూ` 0.24 · `మ` 0.34 · `ిన` 0.16✱ · `్య` 0.04✱ · `మ` 0.02 · `్ర` 0.07 · `ాయ` 0.03 · `ం` 0.53 · `␣త` 0.05 · `ప` 0.30 · `ో` 1.9e-3✱ · `మ` 0.16 · `థ` 0.07 · `్య` 0.40 · `ు` 0.20✱ · `␣న` 7.2e-3✱ · `మ` 0.20 · `్ర` 4.9e-3✱ · `క` 0.74 · `్` 0.98 |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 80 tokens · 30.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామచ్యుత్రామాయ భ్రమ్రించు లంకా | `UUUUUIUUIUU` |
| 2 | సేమచ్యుత్రామాయ ద్ర్వ్సించే లవణ్యమ్ | `UUUUUIUUIUU` |
| 3 | రామచ్యుత్రామాయ రక్షించు సీతా | `UUUUUIUUIUU` |
| 4 | సేమచ్యుత్రామాయ ల్వ్క్శేతిన్ త్వమౌత్యమ్ | `UUUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.068 · model's first choice kept 52% · constraint overrode 34% · backtracks 30

<details><summary>Token probabilities (80 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.33 · `మ` 0.81 · `చ` 0.73 · `్య` 7.8e-6✱ · `ు` 1.00 · `త` 0.81 · `్రా` 9.9e-4✱ · `మ` 0.41 · `ాయ` 0.27 · `␣భ` 6.6e-3✱ · `్రమ` 0.03✱ · `్ర` 2.7e-3✱ · `ించు` 0.05 · `␣ల` 0.47 · `ం` 0.46 · `కా` 0.83 · `⏎` 9.8e-3 forced |
| 2 | `సే` 0.02 · `మ` 4.6e-3✱ · `చ` 0.09 · `్య` 0.03✱ · `ు` 0.98 · `త` 0.97 · `్రా` 0.48 · `మ` 0.98 · `ాయ` 1.00 · `␣ద` 0.04 · `్ర` 4.5e-3✱ · `్వ` 1.7e-7✱ · `్` 9.6e-4✱ · `స` 7.6e-4✱ · `ించే` 5.3e-3 · `␣ల` 0.56 · `వ` 6.2e-4✱ · `ణ` 0.96 · `్య` 2.4e-3✱ · `మ` 0.02✱ · `్` 8.6e-7✱ · `⏎` 0.10 forced |
| 3 | `ర` 0.08 · `ామ` 4.7e-3✱ · `చ` 0.87 · `్య` 1.00 · `ు` 1.00 · `త` 0.99 · `్రా` 0.98 · `మ` 1.00 · `ాయ` 1.00 · `␣ర` 0.26 · `క్ష` 0.71 · `ించు` 0.78 · `␣సీ` 0.39 · `తా` 0.53 · `⏎` 0.02 forced |
| 4 | `సే` 0.95 · `మ` 1.00 · `చ` 1.00 · `్య` 1.00 · `ు` 1.00 · `త` 1.00 · `్రా` 1.00 · `మ` 1.00 · `ాయ` 1.00 · `␣ల` 0.22 · `్వ` 1.3e-5✱ · `్` 0.04✱ · `క` 0.36 · `్` 3.1e-4✱ · `శ` 0.01✱ · `ే` 0.21 · `తి` 0.07 · `న్` 0.02✱ · `␣త` 0.09 · `్వ` 0.61 · `మ` 0.14✱ · `ౌ` 0.03✱ · `త` 6.9e-4✱ · `్య` 0.02✱ · `మ` 0.02✱ · `్` 0.62 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 83 tokens · 33.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిక్రేపక్యం కదా నిత్యనిర్మా | `UUUUUIUUIUU` |
| 2 | అల్లెప్రేమ్యై నిత్యహర్యామ్యెనోనుం | `UUUUUIUUIUU` |
| 3 | కల్లమ్రోత్యెన్యెన్యెకల్యాణముం త్వం | `UUUUUIUUIUU` |
| 4 | తల్లిమ్రోత్యెన్యెన్యెతన్నేన్యెనుం తర్ | `UUUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 11% · single-akshara words 22% · repeated lines 0 · mean token probability (geometric) 0.052 · model's first choice kept 45% · constraint overrode 35% · backtracks 30

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.75 · `ల్లి` 0.72 · `క` 0.02✱ · `్రే` 3.5e-6✱ · `ప` 0.14 · `క` 0.01✱ · `్యం` 4.1e-4✱ · `␣క` 0.03 · `దా` 0.09✱ · `␣ని` 0.03 · `త్య` 0.86 · `ని` 0.04 · `ర్` 0.04 · `మా` 0.20 · `⏎` 8.1e-6 forced |
| 2 | `అ` 0.08 · `ల్ల` 7.9e-3✱ · `ె` 0.02✱ · `ప్ర` 0.01 · `ే` 0.99 · `మ` 0.95 · `్య` 4.5e-3✱ · `ై` 0.05 · `␣ని` 0.17 · `త్య` 0.23✱ · `హ` 4.3e-4✱ · `ర` 0.06✱ · `్యా` 3.8e-4✱ · `మ` 0.13 · `్య` 0.07✱ · `ె` 0.01 · `నో` 0.07✱ · `ను` 7.9e-4✱ · `ం` 1.7e-3✱ · `⏎` 0.99 forced |
| 3 | `క` 0.07 · `ల` 0.23✱ · `్` 1.2e-7✱ · `ల` 0.85 · `మ` 0.09 · `్రో` 0.02✱ · `త` 0.11 · `్య` 0.23 · `ె` 0.12 · `న` 0.18 · `్య` 1.3e-4✱ · `ె` 0.19 · `న` 0.30 · `్య` 0.03✱ · `ె` 0.36 · `క` 8.8e-3✱ · `ల` 0.33 · `్యా` 0.17 · `ణ` 0.32 · `ము` 0.24 · `ం` 0.40✱ · `␣త` 1.2e-4✱ · `్వ` 0.39 · `ం` 0.82 · `⏎` 0.99 forced |
| 4 | `త` 0.13 · `ల్లి` 0.60 · `మ` 0.04 · `్రో` 0.03✱ · `త` 0.80 · `్య` 0.76 · `ె` 0.56 · `న` 0.64 · `్య` 0.85 · `ె` 0.96 · `న` 0.73 · `్య` 0.97 · `ె` 0.96 · `త` 0.05✱ · `న్న` 0.02 · `ే` 0.28 · `న` 0.37 · `్య` 0.09 · `ె` 0.50 · `ను` 0.18 · `ం` 0.92 · `␣తర` 1.0e-4✱ · `్` 5.4e-5✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 73 tokens · 11.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వాయుప్రియ్నం గమ్యు ధ్వానమ్ము వింటే | `UUUUUIUUIUU` |
| 2 | మాయా జగ్వల్యం కమల్యం దొరెంటే | `UUUUUIUUIUU` |
| 3 | సౌయగ్యమ్ముల్యం లొసద్రిన్ దొరంటే | `UUUUUIUUIUU` |
| 4 | భీయుల్యం భేదమ్ము విచ్యున్ దొరెంటే | `UUUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.035 · model's first choice kept 36% · constraint overrode 47% · backtracks 0

<details><summary>Token probabilities (73 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.36 · `ాయ` 1.00 · `ు` 1.00 · `ప` 0.01✱ · `్రి` 0.03✱ · `య` 3.9e-3✱ · `్` 3.6e-3✱ · `న` 0.35 · `ం` 0.01✱ · `␣గ` 0.12 · `మ` 0.65 · `్య` 0.39 · `ు` 2.2e-3✱ · `␣ధ` 2.1e-4✱ · `్వ` 0.07✱ · `ాన` 0.23 · `మ్ము` 0.08✱ · `␣వి` 0.05 · `ంటే` 1.1e-3 · `⏎` 0.78 forced |
| 2 | `మ` 0.03 · `ాయ` 0.08✱ · `ా` 0.60 · `␣జగ` 0.07 · `్వ` 1.0e-5✱ · `ల` 0.36 · `్యం` 0.08✱ · `␣క` 0.06 · `మ` 8.9e-3✱ · `ల` 0.83 · `్యం` 7.4e-3✱ · `␣ద` 0.03✱ · `ొ` 0.21✱ · `రె` 0.03✱ · `ంటే` 7.2e-3✱ · `⏎` 1.00 forced |
| 3 | `స` 0.12 · `ౌ` 1.5e-4✱ · `య` 2.6e-8✱ · `గ` 0.15 · `్య` 0.39 · `మ్ము` 0.22 · `ల` 0.05 · `్యం` 5.3e-3✱ · `␣ల` 0.20 · `ొ` 1.0e-4✱ · `స` 2.9e-3✱ · `ద` 0.04✱ · `్రి` 5.6e-3✱ · `న్` 0.02✱ · `␣ద` 0.08✱ · `ొ` 0.23 · `ర` 0.11 · `ంటే` 2.1e-3 · `⏎` 1.00 forced |
| 4 | `భ` 0.12 · `ీ` 0.20 · `యు` 1.7e-5✱ · `ల` 0.49 · `్యం` 0.02✱ · `␣భ` 0.09 · `ే` 0.15 · `ద` 0.71 · `మ్ము` 0.54 · `␣వి` 0.06✱ · `చ` 0.04✱ · `్య` 3.9e-3✱ · `ు` 0.56 · `న్` 0.05✱ · `␣ద` 0.50 · `ొ` 0.95 · `రె` 0.56 · `ంటే` 0.99 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 59 tokens · 4.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిక్రాంతిక్రియ్రుతక్యంబు గానం | `UUUUUIUUIUU` |
| 2 | తల్లిక్రాంతిక్రియ్రుతక్యంబు ధానం | `UUUUUIUUIUU` |
| 3 | తల్లిక్రాంతిక్రియ్రుతక్యంబు జానం | `UUUUUIUUIUU` |
| 4 | తల్లిక్రాంతిక్రియ్రుతక్యంబు వానం | `UUUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.238 · model's first choice kept 69% · constraint overrode 18% · backtracks 0

<details><summary>Token probabilities (59 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.75 · `ల్లి` 0.72 · `క` 0.02✱ · `్రా` 1.9e-6✱ · `ంతి` 0.79 · `క` 0.02✱ · `్రియ` 1.5e-4✱ · `్రు` 2.0e-4✱ · `త` 0.05✱ · `క` 0.04✱ · `్యం` 2.0e-3✱ · `బు` 0.47 · `␣గా` 0.03 · `నం` 0.03 · `⏎` 0.25 forced |
| 2 | `త` 0.67 · `ల్లి` 0.87 · `క` 0.39 · `్రా` 0.28✱ · `ంతి` 0.94 · `క` 0.98 · `్రియ` 0.98 · `్రు` 0.99 · `త` 0.99 · `క` 0.98 · `్యం` 0.98 · `బు` 0.97 · `␣ధ` 0.04 · `ానం` 0.10✱ · `⏎` 1.00 forced |
| 3 | `త` 0.98 · `ల్లి` 0.98 · `క` 0.98 · `్రా` 1.00 · `ంతి` 1.00 · `క` 1.00 · `్రియ` 1.00 · `్రు` 1.00 · `త` 1.00 · `క` 1.00 · `్యం` 1.00 · `బు` 1.00 · `␣జ` 0.05 · `ానం` 0.03 · `⏎` 0.97 forced |
| 4 | `త` 1.00 · `ల్లి` 0.99 · `క` 1.00 · `్రా` 1.00 · `ంతి` 1.00 · `క` 1.00 · `్రియ` 1.00 · `్రు` 1.00 · `త` 1.00 · `క` 1.00 · `్యం` 1.00 · `బు` 1.00 · `␣వ` 0.04 · `ానం` 0.06 |

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

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 53 tokens · 8.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగదంతటిక్రియా | `UIUIIIUIUIU` |
| 2 | తల్లి కన్నె మమతక్రియా కదా | `UIUIIIUIUIU` |
| 3 | తల్లి చూపుల తదైశ్వరమ్యమా | `UIUIIIUIUIU` |
| 4 | తల్లి ఆశ్రయమృదంగమయ్నమా | `UIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 58% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.086 · model's first choice kept 53% · constraint overrode 40% · backtracks 0

<details><summary>Token probabilities (53 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.67 · `␣ప్రేమ` 0.80 · `␣జగ` 0.29 · `ద` 1.4e-3✱ · `ంత` 0.96 · `టి` 0.09 · `క` 0.23✱ · `్రి` 1.7e-8✱ · `యా` 0.46 · `⏎` 0.59 forced |
| 2 | `త` 0.45 · `ల్లి` 0.69 · `␣క` 0.16 · `న్న` 9.6e-3✱ · `ె` 0.23✱ · `␣మ` 0.12 · `మ` 0.38 · `త` 0.63 · `క` 0.05✱ · `్రి` 4.2e-6✱ · `యా` 0.99 · `␣క` 2.0e-4✱ · `దా` 0.58 · `⏎` 1.00 forced |
| 3 | `త` 0.87 · `ల్లి` 0.91 · `␣చూపు` 0.19 · `ల` 0.13 · `␣త` 0.11✱ · `ద` 2.9e-3✱ · `ై` 0.10✱ · `శ` 0.23 · `్వర` 0.72 · `మ` 0.09 · `్య` 1.3e-3✱ · `మా` 0.08✱ · `⏎` 0.99 forced |
| 4 | `త` 0.98 · `ల్లి` 0.94 · `␣ఆ` 0.07 · `శ` 0.87 · `్ర` 0.19✱ · `య` 0.40✱ · `మ` 0.32 · `ృ` 0.02✱ · `ద` 0.42 · `ంగ` 0.29 · `మ` 0.35 · `య` 0.09✱ · `్` 6.2e-3✱ · `న` 0.06✱ · `మా` 0.06✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 52 tokens · 8.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగదంతటా నిలిచ్ | `UIUIIIUIUIU` |
| 2 | తల్లి దీవెన త్య్రితాన దైవమై | `UIUIIIUIUIU` |
| 3 | తల్లి కన్నె కనుదై కరుణ్యమై | `UIUIIIUIUIU` |
| 4 | తల్లి ప్రేమ జగదంతటా పవన్ | `UIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.048 · model's first choice kept 52% · constraint overrode 37% · backtracks 0

<details><summary>Token probabilities (52 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.67 · `␣ప్రేమ` 0.80 · `␣జగ` 0.29 · `ద` 1.4e-3✱ · `ంత` 0.96 · `టా` 0.40 · `␣ని` 0.14✱ · `లి` 0.28✱ · `చ` 6.7e-3✱ · `్` 1.3e-11✱ · `⏎` 1.4e-4 forced |
| 2 | `త` 0.38 · `ల్లి` 0.59 · `␣దీ` 0.09 · `వె` 0.98 · `న` 0.99 · `␣త` 0.05✱ · `్య` 2.9e-3✱ · `్ర` 6.4e-7✱ · `ిత` 3.9e-3✱ · `ాన` 0.04 · `␣ద` 0.03 · `ై` 0.45 · `వ` 0.91 · `మై` 0.70 · `⏎` 0.88 forced |
| 3 | `త` 0.96 · `ల్లి` 0.94 · `␣క` 0.36 · `న్న` 0.01✱ · `ె` 0.25✱ · `␣క` 0.27 · `ను` 0.03✱ · `ద` 6.6e-4✱ · `ై` 0.06✱ · `␣క` 0.65 · `రుణ` 0.91 · `్య` 1.2e-4✱ · `మై` 0.63 · `⏎` 0.97 forced |
| 4 | `త` 0.99 · `ల్లి` 0.97 · `␣ప్రేమ` 0.11 · `␣జగ` 0.06✱ · `ద` 7.5e-3✱ · `ంత` 0.91 · `టా` 0.74 · `␣ప` 0.03 · `వ` 0.23 · `న` 0.98 · `్` 1.7e-8✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 56 tokens · 24.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగదంతటా నిలిచ్ | `UIUIIIUIUIU` |
| 2 | తల్లి చూపుల వెదక్యు జగ్రునిచ్ | `UIUIIIUIUIU` |
| 3 | తల్లి కౌగిలి కదల్లొ జగ్రునిచ్ | `UIUIIIUIUIU` |
| 4 | తల్లి దీవెనల దారి చూపిచై | `UIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 44% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.073 · model's first choice kept 54% · constraint overrode 34% · backtracks 30

<details><summary>Token probabilities (56 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.67 · `␣ప్రేమ` 0.80 · `␣జగ` 0.29 · `ద` 1.4e-3✱ · `ంత` 0.96 · `టా` 0.40 · `␣ని` 0.14✱ · `లి` 0.26✱ · `చ` 6.7e-3✱ · `్` 1.6e-11✱ · `⏎` 1.3e-4 forced |
| 2 | `త` 0.38 · `ల్లి` 0.61 · `␣చూపు` 0.11 · `ల` 0.10 · `␣వె` 0.11✱ · `ద` 3.7e-4✱ · `క` 0.70 · `్య` 4.4e-5✱ · `ు` 0.14✱ · `␣జగ` 0.05 · `్రు` 8.7e-6✱ · `ని` 0.21 · `చ` 0.02✱ · `్` 0.82 · `⏎` 1.00 forced |
| 3 | `త` 0.96 · `ల్లి` 0.96 · `␣క` 0.19 · `ౌ` 0.26✱ · `గి` 0.99 · `లి` 0.91 · `␣క` 0.05✱ · `ద` 6.3e-3✱ · `ల్` 0.02✱ · `ల` 0.02✱ · `ొ` 0.05 · `␣జగ` 0.15 · `్రు` 1.5e-3✱ · `ని` 0.74 · `చ` 0.98 · `్` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ల్లి` 0.97 · `␣దీ` 0.17 · `వె` 0.97 · `న` 0.99 · `ల` 0.27 · `␣ద` 0.24 · `ారి` 0.35 · `␣చూ` 0.16 · `పి` 0.51 · `చ` 0.61 · `ై` 7.1e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 69 tokens · 25.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగదంతటా నిలుమ్ | `UIUIIIUIUIU` |
| 2 | మాల్ల దైవము మమత్యునిల్ర గమ్ | `UIUIIIUIUIU` |
| 3 | కల్ల కీర్తి కరుగన్రు కమ్యునిల్ | `UIUIIIUIUIU` |
| 4 | సెల్ల సుగ్రుడె సలించు సత్యమున్ | `UIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 44% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.036 · model's first choice kept 43% · constraint overrode 45% · backtracks 30

<details><summary>Token probabilities (69 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.67 · `␣ప్రేమ` 0.80 · `␣జగ` 0.29 · `ద` 1.4e-3✱ · `ంత` 0.96 · `టా` 0.40 · `␣ని` 0.14✱ · `లు` 0.08✱ · `మ` 8.8e-3✱ · `్` 5.5e-8✱ · `⏎` 0.06 forced |
| 2 | `మా` 0.06 · `ల` 1.8e-7✱ · `్` 2.1e-7✱ · `ల` 0.37 · `␣ద` 0.01 · `ై` 0.36 · `వ` 0.89 · `ము` 0.32 · `␣మ` 0.30 · `మ` 0.09✱ · `త` 0.65 · `్య` 2.2e-4✱ · `ు` 0.14✱ · `ని` 0.41 · `ల` 3.0e-3✱ · `్ర` 2.5e-3✱ · `␣గ` 0.01✱ · `మ` 0.55 · `్` 0.40✱ · `⏎` 0.98 forced |
| 3 | `క` 0.10 · `ల` 0.11✱ · `్` 2.1e-7✱ · `ల` 0.97 · `␣క` 0.68 · `ీ` 1.5e-3✱ · `ర్` 0.97 · `తి` 0.97 · `␣క` 0.67 · `రు` 6.6e-3✱ · `గ` 0.02✱ · `న` 0.03✱ · `్రు` 6.3e-5✱ · `␣క` 0.45 · `మ` 0.07✱ · `్య` 5.3e-3✱ · `ు` 0.79 · `ని` 0.64 · `ల` 0.58 · `్` 0.03✱ · `⏎` 0.37 forced |
| 4 | `స` 0.04 · `ెల` 0.10✱ · `్` 0.01✱ · `ల` 0.89 · `␣సు` 0.20 · `గ` 0.12 · `్రు` 5.4e-5✱ · `డ` 0.25 · `ె` 0.16 · `␣స` 0.27 · `ల` 3.8e-3✱ · `ించు` 1.5e-4✱ · `␣స` 0.35 · `త్య` 0.55 · `ము` 0.45 · `న్` 0.18✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 47 tokens · 3.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగదంతముల్రు దీ | `UIUIIIUIUIU` |
| 2 | తల్లి కన్నె కదెదక్రు తేని దీ | `UIUIIIUIUIU` |
| 3 | తల్లి ఊపిరి నిదానముల్రు తే | `UIUIIIUIUIU` |
| 4 | తల్లి ప్రేమ అమృతమ్రు నిత్యమే | `UIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 41% · single-akshara words 18% · repeated lines 0 · mean token probability (geometric) 0.099 · model's first choice kept 53% · constraint overrode 34% · backtracks 0

<details><summary>Token probabilities (47 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.67 · `␣ప్రేమ` 0.80 · `␣జగ` 0.29 · `ద` 1.4e-3✱ · `ంత` 0.96 · `ముల` 0.15 · `్రు` 3.4e-6✱ · `␣దీ` 0.03✱ · `⏎` 6.6e-7 forced |
| 2 | `త` 0.52 · `ల్లి` 0.61 · `␣క` 0.25 · `న్న` 0.01✱ · `ె` 0.35 · `␣క` 0.25 · `ద` 7.9e-3✱ · `ె` 6.7e-3✱ · `ద` 0.02✱ · `క` 0.03✱ · `్రు` 2.3e-4✱ · `␣తే` 0.03 · `ని` 0.10 · `␣దీ` 0.10✱ · `⏎` 1.00 forced |
| 3 | `త` 0.87 · `ల్లి` 0.93 · `␣ఊ` 0.05 · `పి` 0.32 · `రి` 0.84 · `␣ని` 0.14✱ · `ద` 2.3e-3✱ · `ాన` 0.35 · `ముల` 0.10 · `్రు` 0.97 · `␣తే` 0.10 · `⏎` 0.69 forced |
| 4 | `త` 0.99 · `ల్లి` 0.93 · `␣ప్రేమ` 0.05 · `␣అమ` 0.11✱ · `ృత` 0.79 · `మ` 0.19✱ · `్రు` 0.28 · `␣ని` 0.17 · `త్య` 0.69 · `మే` 0.04✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 72 tokens · 5.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | విశ్రుతాన సము ద్ర్య్విధ్వలం భయం | `UIUIIIUIUIU` |
| 2 | గీశ్రమున్యు ద్యుగగీతముం ధనం | `UIUIIIUIUIU` |
| 3 | లశ్రమున్యు లఘులంబనం రణం | `UIUIIIUIUIU` |
| 4 | గీశ్రమున్యు విలకృత్యముం వనం | `UIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 38% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.056 · model's first choice kept 39% · constraint overrode 48% · backtracks 0

<details><summary>Token probabilities (72 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వి` 0.03 · `శ` 0.60 · `్రు` 1.4e-3✱ · `త` 0.82 · `ాన` 0.01✱ · `␣స` 0.02✱ · `ము` 0.98 · `␣ద` 7.3e-5✱ · `్ర` 0.23 · `్య` 5.5e-4✱ · `్` 9.2e-4✱ · `విధ` 1.7e-3✱ · `్వ` 0.12✱ · `ల` 0.05✱ · `ం` 0.05✱ · `␣భ` 0.02✱ · `యం` 3.3e-3✱ · `⏎` 0.14 forced |
| 2 | `గ` 0.21 · `ీ` 0.02✱ · `శ` 1.4e-4✱ · `్ర` 0.02✱ · `ము` 0.08✱ · `న` 0.39 · `్య` 1.6e-4✱ · `ు` 0.13 · `␣ద` 0.06✱ · `్య` 0.06✱ · `ు` 0.36 · `గ` 0.65 · `గ` 0.01✱ · `ీ` 0.01✱ · `త` 0.78 · `ము` 0.40 · `ం` 0.08 · `␣ధ` 0.08 · `నం` 0.02✱ · `⏎` 1.00 forced |
| 3 | `ల` 0.07 · `శ` 5.3e-3✱ · `్ర` 0.12✱ · `ము` 0.54 · `న` 0.64 · `్య` 0.44 · `ు` 0.91 · `␣ల` 0.24 · `ఘ` 3.2e-3✱ · `ు` 0.96 · `ల` 0.02✱ · `ంబ` 0.06 · `న` 0.36 · `ం` 0.17✱ · `␣ర` 0.04 · `ణం` 0.03 · `⏎` 1.00 forced |
| 4 | `గ` 0.04 · `ీ` 0.14✱ · `శ` 0.27✱ · `్ర` 0.76 · `ము` 0.93 · `న` 0.93 · `్య` 0.95 · `ు` 0.99 · `␣వి` 0.05 · `ల` 0.04✱ · `క` 4.1e-3✱ · `ృత` 0.03✱ · `్య` 5.8e-4✱ · `ము` 0.33 · `ం` 0.55 · `␣వ` 0.07 · `నం` 0.34 |

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

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

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

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 85 tokens · 14.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమక్రియే తల్యునిక్రాంతినిద్ | `UIUUIUUIUUIU` |
| 2 | తల్లి మమ్రోహమున్ మ్మ్ర్ధైరమై నిల్వుదిద్ | `UIUUIUUIUUIU` |
| 3 | తల్లి త్యాగమ్యునై త్వం త్వనిక్రాంతినిద్ | `UIUUIUUIUUIU` |
| 4 | తల్లి దైవమ్యునై ధైర్యమున్ దారిదీ | `UIUUIUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 33% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.062 · model's first choice kept 45% · constraint overrode 38% · backtracks 0

<details><summary>Token probabilities (85 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.77 · `ల్లి` 0.72 · `␣ప్రేమ` 0.79 · `క` 0.01✱ · `్రియ` 1.5e-8✱ · `ే` 0.26 · `␣త` 0.16✱ · `ల` 0.84 · `్య` 1.5e-6✱ · `ు` 0.22 · `ని` 0.46 · `క` 0.04✱ · `్రా` 5.7e-5✱ · `ంతి` 0.47 · `ని` 0.11✱ · `ద` 1.1e-3✱ · `్` 2.2e-7✱ · `⏎` 0.02 forced |
| 2 | `త` 0.48 · `ల్లి` 0.82 · `␣మ` 0.12 · `మ` 0.93 · `్రో` 9.9e-6✱ · `హ` 0.34✱ · `ము` 0.28 · `న` 9.8e-3✱ · `్` 1.6e-5✱ · `␣మ` 0.29 · `్` 2.8e-5✱ · `మ` 0.95 · `్ర` 3.6e-3✱ · `్` 2.5e-4✱ · `ధ` 9.0e-3✱ · `ై` 0.05 · `ర` 0.06 · `మై` 0.09 · `␣ని` 0.42 · `ల` 0.28✱ · `్వ` 1.1e-4✱ · `ు` 0.14 · `ది` 0.14 · `ద్` 2.8e-3✱ · `⏎` 1.00 forced |
| 3 | `త` 0.97 · `ల్లి` 0.91 · `␣త` 0.03✱ · `్యా` 0.86 · `గ` 0.87 · `మ` 0.33✱ · `్య` 0.01✱ · `ు` 0.28✱ · `న` 0.22 · `ై` 0.04✱ · `␣త` 0.81 · `్వ` 0.07 · `ం` 0.16✱ · `␣త` 0.25 · `్వ` 0.35 · `ని` 0.10 · `క` 0.17 · `్రా` 0.15✱ · `ంతి` 0.84 · `ని` 0.79 · `ద` 0.79 · `్` 0.99 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ల్లి` 0.95 · `␣ద` 0.09✱ · `ై` 0.42 · `వ` 0.97 · `మ` 0.22 · `్య` 0.02✱ · `ు` 0.93 · `న` 0.82 · `ై` 0.98 · `␣ధ` 0.15 · `ై` 0.69 · `ర్య` 0.80 · `ము` 0.39 · `న` 0.42 · `్` 2.2e-3✱ · `␣ద` 0.22 · `ారి` 0.05 · `దీ` 0.13✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 98 tokens · 15.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమక్రుపై న్య్య్తం జగమ్రోవదమ్ | `UIUUIUUIUUIU` |
| 2 | తల్లి హృద్యమ్యుభయ్ స్ర్య్తమ్యుభయ్ రక్షితమ్ | `UIUUIUUIUUIU` |
| 3 | తల్లి చూపుల్యుభయ్ న్య్య్తం జగమ్రోవదమ్ | `UIUUIUUIUUIU` |
| 4 | తల్లి మమ్రమ్న్య్యుభయ్ స్ర్య్తమ్యుభయ్ రక్షితమ్ | `UIUUIUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.099 · model's first choice kept 58% · constraint overrode 32% · backtracks 0

<details><summary>Token probabilities (98 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.77 · `ల్లి` 0.72 · `␣ప్రేమ` 0.79 · `క` 0.01✱ · `్రు` 5.9e-8✱ · `ప` 0.16 · `ై` 3.9e-3✱ · `␣న` 0.10✱ · `్య` 8.8e-6✱ · `్య` 3.0e-4✱ · `్` 7.2e-5✱ · `త` 3.4e-3✱ · `ం` 0.05✱ · `␣జగ` 0.10✱ · `మ` 0.08✱ · `్రో` 1.6e-3✱ · `వ` 0.60 · `ద` 0.08 · `మ్` 0.11 · `⏎` 0.30 forced |
| 2 | `త` 0.52 · `ల్లి` 0.82 · `␣హ` 0.04 · `ృ` 0.98 · `ద` 0.08✱ · `్య` 7.9e-5✱ · `మ` 0.42 · `్య` 9.6e-4✱ · `ు` 0.12✱ · `భ` 7.9e-3✱ · `య` 0.73 · `్` 8.0e-4✱ · `␣స` 0.04 · `్ర` 8.7e-4✱ · `్య` 8.2e-7✱ · `్` 4.4e-3✱ · `త` 0.04✱ · `మ` 0.13 · `్య` 0.10 · `ు` 0.17 · `భ` 0.10 · `య` 0.53 · `్` 0.24✱ · `␣ర` 0.06 · `క్ష` 0.25 · `ిత` 0.39 · `మ్` 0.92 · `⏎` 1.00 forced |
| 3 | `త` 0.92 · `ల్లి` 0.93 · `␣చూపు` 0.08✱ · `ల` 0.36 · `్య` 2.0e-3✱ · `ు` 0.21 · `భ` 0.09✱ · `య` 0.89 · `్` 0.98 · `␣న` 0.04✱ · `్య` 0.20 · `్య` 0.94 · `్` 0.79 · `త` 0.98 · `ం` 0.93 · `␣జగ` 0.26 · `మ` 0.95 · `్రో` 0.94 · `వ` 1.00 · `ద` 0.98 · `మ్` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ల్లి` 0.98 · `␣మ` 0.07✱ · `మ` 0.77 · `్ర` 3.9e-5✱ · `మ్` 0.02 · `న` 0.23 · `్య` 0.69 · `్య` 0.60 · `ు` 0.02✱ · `భ` 0.62 · `య` 0.99 · `్` 1.00 · `␣స` 0.50 · `్ర` 0.93 · `్య` 1.00 · `్` 1.00 · `త` 1.00 · `మ` 1.00 · `్య` 1.00 · `ు` 1.00 · `భ` 1.00 · `య` 1.00 · `్` 0.99 · `␣ర` 0.31 · `క్ష` 0.97 · `ిత` 1.00 · `మ్` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 95 tokens · 29.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమన్ వెలక్ఞ్ఖ్తమ్యునిన్రుత్యమున్ | `UIUUIUUIUUIU` |
| 2 | తల్లి మమ్రోద్యునన్ తల్యునంత్యున్జ్యమున్ | `UIUUIUUIUUIU` |
| 3 | తల్లి ఆశీర్వదన్ అంత్యునత్యున్యునన్ | `UIUUIUUIUUIU` |
| 4 | తల్లి కౌగిల్యునన్ కల్ప్యునంత్యున్యునన్ | `UIUUIUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 42% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.137 · model's first choice kept 62% · constraint overrode 29% · backtracks 30

<details><summary>Token probabilities (95 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.77 · `ల్లి` 0.72 · `␣ప్రేమ` 0.78 · `న్` 1.7e-3✱ · `␣వె` 0.01 · `ల` 0.58 · `క` 0.34 · `్ఞ` 1.8e-9✱ · `్` 5.7e-4✱ · `ఖ` 0.55 · `్` 0.03✱ · `త` 0.02✱ · `మ` 0.06✱ · `్య` 0.01✱ · `ు` 0.20✱ · `ని` 0.17 · `న` 0.02✱ · `్రు` 8.0e-4✱ · `త` 0.02✱ · `్య` 0.04✱ · `ము` 0.55 · `న` 0.04✱ · `్` 2.3e-5✱ · `⏎` 0.80 forced |
| 2 | `త` 0.44 · `ల్లి` 0.79 · `␣మ` 0.08 · `మ` 0.94 · `్రో` 3.0e-5✱ · `ద` 0.13✱ · `్య` 0.05✱ · `ు` 0.40 · `న` 0.30 · `న్` 0.04✱ · `␣త` 0.06 · `ల` 0.39 · `్య` 4.0e-4✱ · `ు` 0.40 · `న` 0.45 · `ంత` 0.01✱ · `్య` 0.42 · `ు` 0.63 · `న` 0.44 · `్` 0.14 · `జ` 1.1e-3✱ · `్య` 0.25 · `ము` 0.93 · `న` 0.93 · `్` 0.98 · `⏎` 1.00 forced |
| 3 | `త` 0.88 · `ల్లి` 0.92 · `␣ఆ` 0.15 · `శ` 0.75 · `ీ` 0.40 · `ర్` 0.80 · `వ` 0.65 · `ద` 0.89 · `న్` 0.25✱ · `␣అంత` 0.04 · `్య` 0.81 · `ు` 0.95 · `న` 0.88 · `త` 0.08 · `్య` 0.43 · `ు` 0.81 · `న` 0.90 · `్య` 0.08✱ · `ు` 0.88 · `న` 0.72 · `న్` 0.04✱ · `⏎` 0.97 forced |
| 4 | `త` 0.99 · `ల్లి` 0.97 · `␣క` 0.23 · `ౌ` 3.1e-3✱ · `గి` 0.90 · `ల` 0.32✱ · `్య` 0.63 · `ు` 0.91 · `న` 0.83 · `న్` 0.80 · `␣క` 0.55 · `ల్ప` 0.08✱ · `్య` 0.63 · `ు` 0.99 · `న` 0.98 · `ంత` 0.37 · `్య` 0.98 · `ు` 0.98 · `న` 0.98 · `్య` 0.50 · `ు` 0.68 · `న` 0.98 · `న్` 0.82 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 88 tokens · 30.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమక్రుతక్ర్య్తం సుమాజమ్యెనన్ | `UIUUIUUIUUIU` |
| 2 | తల్లి హృద్యమ్రుతమ్య్నమ్ నిరంతర్యనన్ | `UIUUIUUIUUIU` |
| 3 | తల్లి కౌమార్యముక్ర్య్తం వివేక్యన్యనన్ | `UIUUIUUIUUIU` |
| 4 | తల్లి ఆశ్రయ్యముక్ర్య్తం శుభమ్యన్యనన్ | `UIUUIUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 33% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.075 · model's first choice kept 48% · constraint overrode 36% · backtracks 30

<details><summary>Token probabilities (88 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.77 · `ల్లి` 0.72 · `␣ప్రేమ` 0.78 · `క` 0.01✱ · `్రు` 5.5e-8✱ · `త` 0.05 · `క` 0.04✱ · `్ర` 1.0e-5✱ · `్య` 3.2e-5✱ · `్` 5.5e-5✱ · `త` 5.8e-3✱ · `ం` 0.01✱ · `␣సు` 0.05 · `మా` 0.09 · `జ` 2.2e-3 · `మ` 7.8e-3✱ · `్య` 0.20 · `ె` 0.16✱ · `న` 0.18✱ · `న్` 0.02✱ · `⏎` 0.96 forced |
| 2 | `త` 0.59 · `ల్లి` 0.81 · `␣హ` 0.04 · `ృ` 0.98 · `ద` 0.13✱ · `్య` 7.8e-5✱ · `మ` 0.31 · `్రు` 3.0e-4✱ · `త` 0.13 · `మ` 0.19✱ · `్య` 0.04✱ · `్` 9.5e-3✱ · `న` 0.65 · `మ్` 0.01✱ · `␣ని` 0.04 · `ర` 0.07✱ · `ంత` 0.92 · `ర` 0.98 · `్య` 2.7e-3✱ · `న` 0.21 · `న్` 0.92 · `⏎` 1.00 forced |
| 3 | `త` 0.91 · `ల్లి` 0.93 · `␣క` 0.18 · `ౌ` 0.01✱ · `మ` 0.21 · `ార` 0.72 · `్య` 0.15 · `ము` 0.08 · `క` 0.10 · `్ర` 7.3e-4✱ · `్య` 0.18✱ · `్` 0.32 · `త` 0.88 · `ం` 0.23 · `␣వి` 0.04 · `వే` 0.04 · `క` 0.97 · `్య` 0.37 · `న` 0.41 · `్య` 2.9e-4✱ · `న` 0.18✱ · `న్` 0.99 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ల్లి` 0.98 · `␣ఆ` 0.10✱ · `శ` 0.84 · `్ర` 0.41 · `య` 0.77 · `్య` 1.3e-3✱ · `ము` 0.23 · `క` 0.21 · `్ర` 0.29✱ · `్య` 0.99 · `్` 0.98 · `త` 0.98 · `ం` 0.89 · `␣శు` 0.07✱ · `భ` 0.97 · `మ` 0.36 · `్య` 0.60 · `న` 0.85 · `్య` 1.3e-3✱ · `న` 0.93 · `న్` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 84 tokens · 5.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమల్రు గొప్ప్య్దై నిలిచ్యెన్రు లో | `UIUUIUUIUUIU` |
| 2 | తల్లి దయ్యెన్రు సుందర్యమై నిల్యెనో | `UIUUIUUIUUIU` |
| 3 | తల్లి కౌగిల్యెనో మ్ర్య్తైకమై నిల్యనో | `UIUUIUUIUUIU` |
| 4 | తల్లి ఆశ్రయ్యెనో ప్య్న్దైకమై నిల్యనో | `UIUUIUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 24% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.070 · model's first choice kept 49% · constraint overrode 38% · backtracks 0

<details><summary>Token probabilities (84 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.77 · `ల్లి` 0.72 · `␣ప్రేమ` 0.79 · `ల` 4.7e-3✱ · `్రు` 2.6e-5✱ · `␣గొప్ప` 0.22 · `్య` 2.3e-6✱ · `్` 8.4e-5✱ · `ద` 4.4e-3✱ · `ై` 0.15✱ · `␣ని` 0.34 · `లి` 0.25✱ · `చ` 0.02✱ · `్య` 8.6e-4✱ · `ె` 0.22 · `న` 0.06✱ · `్రు` 2.5e-3✱ · `␣లో` 5.1e-3✱ · `⏎` 5.0e-6 forced |
| 2 | `త` 0.33 · `ల్లి` 0.82 · `␣ద` 0.06 · `య` 0.73 · `్య` 8.6e-3✱ · `ె` 0.06 · `న` 0.60 · `్రు` 0.96 · `␣సు` 0.05 · `ంద` 0.09 · `ర` 0.85 · `్య` 0.28✱ · `మై` 0.28 · `␣ని` 0.29 · `ల` 0.17✱ · `్య` 9.1e-5✱ · `ె` 0.92 · `నో` 0.01 · `⏎` 4.1e-3 forced |
| 3 | `త` 0.94 · `ల్లి` 0.93 · `␣క` 0.19 · `ౌ` 6.7e-3✱ · `గి` 0.90 · `ల` 0.31✱ · `్య` 0.21 · `ె` 0.82 · `న` 0.98 · `ో` 1.4e-5✱ · `␣మ` 0.02✱ · `్ర` 1.1e-4✱ · `్య` 5.5e-6✱ · `్` 6.9e-3✱ · `త` 0.12✱ · `ై` 0.11✱ · `క` 0.09 · `మై` 0.32 · `␣ని` 0.55 · `ల` 0.50 · `్య` 0.78 · `నో` 1.6e-4 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ల్లి` 0.97 · `␣ఆ` 0.33 · `శ` 0.90 · `్ర` 0.37 · `య` 0.92 · `్య` 0.15✱ · `ె` 0.97 · `న` 0.83 · `ో` 0.79 · `␣ప` 0.01✱ · `్య` 8.4e-3✱ · `్` 5.6e-3✱ · `న` 0.46 · `్` 2.0e-4✱ · `ద` 0.14✱ · `ై` 0.91 · `క` 0.85 · `మై` 1.00 · `␣ని` 0.99 · `ల` 0.90 · `్య` 0.97 · `నో` 0.75 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 96 tokens · 6.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వాయుపుత్రుడ్యె సాగ్య్న్భైరవిన్ తీరమై | `UIUUIUUIUUIU` |
| 2 | భీయుడై లంకనున్ జ్య్వేలసిన్ దైవమై | `UIUUIUUIUUIU` |
| 3 | గీయమై సాగ్య్న్భువన్ద్ర్గీతమై లంకలో | `UIUUIUUIUUIU` |
| 4 | శౌయుడై నిల్యెనున్ ధ్వ్వ్సన్యురై దైవమై | `UIUUIUUIUUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 21% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.042 · model's first choice kept 47% · constraint overrode 40% · backtracks 0

<details><summary>Token probabilities (96 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.34 · `ాయ` 0.99 · `ు` 1.00 · `పు` 0.54 · `త్ర` 0.85 · `ు` 0.64 · `డ` 0.46✱ · `్య` 9.6e-5✱ · `ె` 0.53 · `␣సా` 0.13 · `గ` 0.55 · `్య` 0.05✱ · `్` 2.8e-4✱ · `న` 0.32 · `్` 6.1e-4✱ · `భ` 9.0e-4✱ · `ై` 0.02✱ · `ర` 0.58 · `వి` 0.03 · `న్` 0.05✱ · `␣తీ` 0.05✱ · `ర` 0.43 · `మై` 0.01 · `⏎` 0.86 forced |
| 2 | `భ` 0.08 · `ీ` 0.24 · `యు` 1.4e-6✱ · `డ` 0.53 · `ై` 0.57 · `␣ల` 0.62 · `ంక` 0.56 · `ను` 0.45 · `న్` 7.8e-4✱ · `␣జ` 5.4e-3✱ · `్య` 3.3e-3✱ · `్వ` 2.0e-4✱ · `ే` 8.8e-5✱ · `ల` 0.58 · `సి` 6.9e-3✱ · `న్` 0.09✱ · `␣ద` 0.06 · `ై` 0.42 · `వ` 0.93 · `మై` 0.66 · `⏎` 1.00 forced |
| 3 | `గ` 0.19 · `ీ` 0.02✱ · `య` 1.1e-7✱ · `మై` 0.24 · `␣సా` 0.19 · `గ` 0.44 · `్య` 0.82 · `్` 0.86 · `న` 0.99 · `్` 0.67 · `భ` 0.84 · `ు` 2.9e-4✱ · `వ` 0.59 · `న` 0.84 · `్` 0.01✱ · `ద` 0.21 · `్ర` 0.03✱ · `్` 9.0e-3✱ · `గ` 5.9e-3✱ · `ీ` 8.8e-3✱ · `త` 0.73 · `మై` 0.70 · `␣ల` 0.29 · `ంక` 0.50 · `లో` 0.19 · `⏎` 0.35 forced |
| 4 | `శ` 0.19 · `ౌ` 0.12✱ · `యు` 1.1e-9✱ · `డ` 0.93 · `ై` 0.96 · `␣ని` 0.04 · `ల` 0.15✱ · `్య` 1.5e-5✱ · `ె` 0.23 · `ను` 0.26✱ · `న్` 0.21 · `␣ధ` 0.03 · `్వ` 2.2e-3✱ · `్వ` 7.8e-6✱ · `్` 5.6e-5✱ · `స` 1.6e-3✱ · `న` 0.23 · `్య` 2.3e-3✱ · `ు` 0.10✱ · `ర` 8.5e-3 · `ై` 0.24✱ · `␣ద` 0.08 · `ై` 0.79 · `వ` 0.99 · `మై` 0.99 |

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

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 69 tokens · 11.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిప్రాణమ్య్న్దై నిత్యం తే | `UUUUUUUU` |
| 2 | తల్లిప్రాణమ్య్న్దై తే నవ్యం | `UUUUUUUU` |
| 3 | తల్లిప్రాణమ్య్న్దై తే సుందర్ | `UUUUUUUU` |
| 4 | తల్లిప్రాణమ్య్న్దై తే మాధుర్ | `UUUUUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 33% · repeated lines 0 · mean token probability (geometric) 0.290 · model's first choice kept 72% · constraint overrode 17% · backtracks 0

<details><summary>Token probabilities (69 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.75 · `ప` 0.03✱ · `్రా` 0.42 · `ణ` 0.80 · `మ` 0.28✱ · `్య` 3.4e-4✱ · `్` 1.9e-4✱ · `న` 0.57 · `్` 5.3e-4✱ · `ద` 0.03✱ · `ై` 0.16✱ · `␣ని` 0.12 · `త్య` 0.79 · `ం` 0.23 · `␣తే` 0.05 · `⏎` 1.8e-6 forced |
| 2 | `త` 0.23 · `ల్లి` 0.87 · `ప` 0.11 · `్రా` 0.96 · `ణ` 0.97 · `మ` 0.93 · `్య` 0.99 · `్` 0.98 · `న` 0.99 · `్` 0.86 · `ద` 0.99 · `ై` 0.99 · `␣తే` 0.21 · `␣న` 0.06 · `వ` 0.10 · `్య` 3.3e-3✱ · `ం` 0.56 · `⏎` 0.93 forced |
| 3 | `త` 0.97 · `ల్లి` 0.98 · `ప` 0.95 · `్రా` 1.00 · `ణ` 1.00 · `మ` 0.99 · `్య` 1.00 · `్` 1.00 · `న` 1.00 · `్` 0.99 · `ద` 1.00 · `ై` 1.00 · `␣తే` 0.74 · `␣సు` 0.09 · `ంద` 0.42 · `ర` 0.29✱ · `్` 2.7e-5✱ · `⏎` 0.14 forced |
| 4 | `త` 0.99 · `ల్లి` 0.99 · `ప` 0.99 · `్రా` 1.00 · `ణ` 1.00 · `మ` 1.00 · `్య` 1.00 · `్` 1.00 · `న` 1.00 · `్` 1.00 · `ద` 1.00 · `ై` 1.00 · `␣తే` 0.97 · `␣మా` 0.04 · `ధు` 0.83 · `ర్` 0.09✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 91 tokens · 15.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవ్వా లంకా ద్య్వా ద్య్వా గమ్యుం | `UUUUUUUU` |
| 2 | జ్వా వ్వా సంద్రం త్వా దాట్యుం ఝ్వం | `UUUUUUUU` |
| 3 | వ్వా వ్వా గమ్యుం త్వా లంకా ద్య్వా | `UUUUUUUU` |
| 4 | జ్య్వా వ్వా గమ్యుం త్వా జ్య్వం ఝ్వం ఝ్వం | `UUUUUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 67% · repeated lines 0 · mean token probability (geometric) 0.230 · model's first choice kept 73% · constraint overrode 17% · backtracks 0

<details><summary>Token probabilities (91 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.14 · `వ` 0.39 · `్వ` 6.4e-7✱ · `ా` 0.29 · `␣ల` 0.07 · `ం` 0.63 · `కా` 0.88 · `␣ద` 0.11✱ · `్య` 8.1e-3✱ · `్వ` 7.1e-5✱ · `ా` 0.45 · `␣ద` 0.04 · `్య` 0.25 · `్వ` 0.73 · `ా` 0.97 · `␣గ` 0.18 · `మ` 0.61 · `్య` 0.77 · `ు` 0.29✱ · `ం` 0.33 · `⏎` 0.73 forced |
| 2 | `జ` 0.04 · `్వ` 0.26 · `ా` 0.03✱ · `␣వ` 0.02✱ · `్వ` 1.9e-3✱ · `ా` 0.89 · `␣స` 0.18 · `ంద్ర` 3.6e-3✱ · `ం` 0.75 · `␣త` 0.22✱ · `్వ` 0.54 · `ా` 0.96 · `␣దా` 0.30 · `ట` 0.19 · `్య` 0.87 · `ు` 0.96 · `ం` 0.99 · `␣` 1.4e-4✱ · `ఝ` 0.79 · `్వ` 0.47 · `ం` 0.36 · `⏎` 1.00 forced |
| 3 | `వ` 0.15 · `్వ` 0.65 · `ా` 0.99 · `␣వ` 0.04✱ · `్వ` 0.04✱ · `ా` 0.99 · `␣గ` 0.19 · `మ` 0.71 · `్య` 0.91 · `ు` 0.95 · `ం` 0.99 · `␣త` 0.30 · `్వ` 0.91 · `ా` 1.00 · `␣ల` 0.46 · `ం` 0.67 · `కా` 0.99 · `␣ద` 0.20 · `్య` 0.97 · `్వ` 0.87 · `ా` 0.89 · `⏎` 0.89 forced |
| 4 | `జ్య` 0.09 · `్వ` 0.79 · `ా` 0.96 · `␣వ` 0.33 · `్వ` 0.99 · `ా` 1.00 · `␣గ` 0.21 · `మ` 0.95 · `్య` 0.95 · `ు` 0.98 · `ం` 1.00 · `␣త` 0.69 · `్వ` 0.97 · `ా` 1.00 · `␣జ` 0.03 · `్య` 0.45 · `్వ` 0.70 · `ం` 0.65 · `␣` 0.04✱ · `ఝ` 0.98 · `్వ` 0.90 · `ం` 0.97 · `␣` 3.3e-4✱ · `ఝ` 0.72 · `్వ` 0.81 · `ం` 0.97 |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 68 tokens · 21.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మహ్యన్రమ్యుం లంకాగమ్యుం | `UUUUUUUU` |
| 2 | మహ్యన్రమ్యుం రక్ష్యుం శ్రీరా | `UUUUUUUU` |
| 3 | మహ్యన్రమ్యుం లంకాదేవిం | `UUUUUUUU` |
| 4 | మహ్యన్రమ్యుం రక్ష్యుం దేవా | `UUUUUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 10% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.372 · model's first choice kept 78% · constraint overrode 8% · backtracks 4

<details><summary>Token probabilities (68 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మ` 0.04 · `హ` 0.31 · `్య` 1.4e-4✱ · `న` 0.15 · `్ర` 8.3e-4✱ · `మ` 0.01 · `్య` 0.16 · `ు` 0.17 · `ం` 0.27 · `␣ల` 0.10 · `ం` 0.60 · `కా` 0.85 · `గ` 0.04 · `మ` 0.61 · `్య` 0.76 · `ు` 0.97 · `ం` 0.98 · `⏎` 0.54 forced |
| 2 | `మ` 0.10 · `హ` 0.58 · `్య` 0.86 · `న` 0.90 · `్ర` 0.92 · `మ` 0.96 · `్య` 0.99 · `ు` 1.00 · `ం` 1.00 · `␣ర` 0.25✱ · `క్ష` 0.82 · `్య` 0.26 · `ు` 0.92 · `ం` 0.99 · `␣శ్రీ` 0.06 · `రా` 0.87 · `⏎` 3.4e-5 forced |
| 3 | `మ` 0.99 · `హ` 0.98 · `్య` 1.00 · `న` 1.00 · `్ర` 1.00 · `మ` 1.00 · `్య` 1.00 · `ు` 1.00 · `ం` 1.00 · `␣ల` 0.04✱ · `ం` 0.73 · `కా` 0.97 · `దే` 0.04 · `వి` 0.31 · `ం` 0.07✱ · `⏎` 0.89 forced |
| 4 | `మ` 1.00 · `హ` 1.00 · `్య` 1.00 · `న` 1.00 · `్ర` 1.00 · `మ` 1.00 · `్య` 1.00 · `ు` 1.00 · `ం` 1.00 · `␣ర` 0.48 · `క్ష` 0.84 · `్య` 0.92 · `ు` 0.89 · `ం` 0.99 · `␣ద` 0.11 · `ే` 0.35 · `వా` 0.31 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 113 tokens · 13.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | భైరవ్రీంద్రం గ్గ్ర్వం గ్గ్ర్వం గ్గ్ర్వం ఝం | `UUUUUUUU` |
| 2 | వ్యారణ్దప్రియ్నం గ్గ్ర్వం గ్గ్ర్వం ఝం | `UUUUUUUU` |
| 3 | సారద్యానంద్ద్ర్ఝం గ్గ్ర్వం గ్గ్ర్వం ఝం | `UUUUUUUU` |
| 4 | లౌరన్ద్దఘ్నమ్ గ్గ్ర్ళం గ్గ్ర్వం ఝం ఝం | `UUUUUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 0% · single-akshara words 78% · repeated lines 0 · mean token probability (geometric) 0.128 · model's first choice kept 65% · constraint overrode 26% · backtracks 30

<details><summary>Token probabilities (113 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `భ` 0.05 · `ై` 0.32 · `ర` 0.99 · `వ` 0.66 · `్రీ` 3.4e-6✱ · `ంద్ర` 5.0e-3 · `ం` 0.21 · `␣గ` 0.13✱ · `్` 8.2e-7✱ · `గ` 0.16 · `్ర` 2.3e-4✱ · `్వ` 6.9e-4✱ · `ం` 0.50 · `␣గ` 0.12 · `్` 0.14 · `గ` 0.94 · `్ర` 0.84 · `్వ` 0.96 · `ం` 0.99 · `␣గ` 0.43✱ · `్` 0.99 · `గ` 1.00 · `్ర` 0.99 · `్వ` 0.99 · `ం` 1.00 · `␣` 6.2e-4✱ · `ఝ` 0.20✱ · `ం` 0.42 · `⏎` 0.40 forced |
| 2 | `వ` 0.20 · `్యా` 2.4e-4✱ · `రణ` 3.2e-6✱ · `్` 0.03✱ · `ద` 0.27 · `ప` 0.01✱ · `్రియ` 0.01✱ · `్` 1.6e-3✱ · `న` 0.28 · `ం` 0.60 · `␣గ` 0.73 · `్` 0.96 · `గ` 0.99 · `్ర` 0.98 · `్వ` 1.00 · `ం` 1.00 · `␣గ` 1.00 · `్` 1.00 · `గ` 1.00 · `్ర` 1.00 · `్వ` 1.00 · `ం` 1.00 · `␣` 0.22 · `ఝ` 1.00 · `ం` 1.00 · `⏎` 1.00 forced |
| 3 | `స` 0.30 · `ార` 2.1e-3✱ · `ద` 0.33 · `్యా` 0.01✱ · `న` 0.52 · `ంద` 0.17 · `్` 3.7e-3✱ · `ద` 0.40 · `్ర` 1.9e-3✱ · `్` 1.3e-3✱ · `ఝ` 1.3e-3✱ · `ం` 0.88 · `␣గ` 1.00 · `్` 1.00 · `గ` 1.00 · `్ర` 1.00 · `్వ` 1.00 · `ం` 1.00 · `␣గ` 1.00 · `్` 1.00 · `గ` 1.00 · `్ర` 1.00 · `్వ` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `ం` 1.00 · `⏎` 1.00 forced |
| 4 | `ల` 0.22✱ · `ౌ` 0.01✱ · `ర` 9.4e-6✱ · `న్` 0.07 · `ద` 0.29 · `్` 0.09 · `ద` 0.57 · `ఘ` 0.02 · `్` 0.26✱ · `న` 0.72 · `మ్` 0.31 · `␣గ` 1.00 · `్` 1.00 · `గ` 1.00 · `్ర` 1.00 · `్` 7.8e-7✱ · `ళ` 8.4e-4✱ · `ం` 0.25✱ · `␣గ` 1.00 · `్` 1.00 · `గ` 1.00 · `్ర` 0.99 · `్వ` 0.90 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `ం` 1.00 · `␣` 2.0e-4✱ · `ఝ` 0.07✱ · `ం` 0.99 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 82 tokens · 7.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామచ్రియ్నన్ ల్ఘ్ఘ్రంగం దైవం | `UUUUUUUU` |
| 2 | సీమచ్రియ్నన్ ల్ఘ్ఘ్శేఖర్రం తే | `UUUUUUUU` |
| 3 | రామచ్రియ్నన్ ల్ఘ్ఘ్రంగం లంకా | `UUUUUUUU` |
| 4 | సీమచ్రియ్నన్ ల్ఘ్ఘ్శేఖర్రంతో | `UUUUUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 9% · repeated lines 0 · mean token probability (geometric) 0.183 · model's first choice kept 72% · constraint overrode 20% · backtracks 0

<details><summary>Token probabilities (82 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.30 · `మ` 0.81 · `చ` 0.63 · `్రి` 3.3e-5✱ · `య` 0.03✱ · `్` 0.02✱ · `న` 0.33 · `న్` 0.03✱ · `␣ల` 0.56 · `్` 1.3e-6✱ · `ఘ` 0.05✱ · `్` 3.3e-3✱ · `ఘ` 0.73 · `్` 0.49 · `రంగ` 7.8e-7✱ · `ం` 0.52 · `␣ద` 0.06✱ · `ై` 0.20 · `వం` 0.07 · `⏎` 0.70 forced |
| 2 | `సీ` 0.66 · `మ` 6.9e-5✱ · `చ` 0.07 · `్రి` 0.21 · `య` 0.90 · `్` 0.98 · `న` 0.98 · `న్` 0.95 · `␣ల` 0.57 · `్` 0.99 · `ఘ` 1.00 · `్` 1.00 · `ఘ` 1.00 · `్` 0.98 · `శ` 2.2e-4✱ · `ే` 0.07✱ · `ఖ` 0.16 · `ర` 0.45✱ · `్ర` 1.8e-5✱ · `ం` 0.87 · `␣తే` 0.10 · `⏎` 4.2e-6 forced |
| 3 | `రా` 0.05✱ · `మ` 0.76 · `చ` 0.88 · `్రి` 0.98 · `య` 0.98 · `్` 0.99 · `న` 1.00 · `న్` 0.99 · `␣ల` 0.94 · `్` 0.99 · `ఘ` 1.00 · `్` 0.99 · `ఘ` 0.99 · `్` 0.93 · `రంగ` 2.2e-3✱ · `ం` 0.95 · `␣ల` 0.24 · `ం` 0.62 · `కా` 0.87 · `⏎` 8.5e-4 forced |
| 4 | `సీ` 0.92 · `మ` 0.86 · `చ` 1.00 · `్రి` 1.00 · `య` 1.00 · `్` 1.00 · `న` 1.00 · `న్` 1.00 · `␣ల` 1.00 · `్` 1.00 · `ఘ` 1.00 · `్` 1.00 · `ఘ` 1.00 · `్` 1.00 · `శ` 0.97 · `ే` 0.99 · `ఖ` 0.99 · `ర` 0.96 · `్ర` 0.98 · `ంతో` 4.5e-5 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 83 tokens · 6.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | గమ్యమ్రోవణ్య్న్గా లంకన్ చే | `UUUUUUUU` |
| 2 | ప్రామ్యన్న్గా సాగ్య్న్బా గమ్య్న్నే చే | `UUUUUUUU` |
| 3 | భూమ్యన్న్గా దాట్య్న్బూ సంద్ర్గా చే | `UUUUUUUU` |
| 4 | శౌమ్యన్న్గా వచ్చ్య్నన్ లంకన్ చే | `UUUUUUUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 13% · single-akshara words 27% · repeated lines 0 · mean token probability (geometric) 0.152 · model's first choice kept 61% · constraint overrode 26% · backtracks 0

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `గ` 0.13 · `మ` 0.66 · `్య` 0.42 · `మ` 0.02✱ · `్రో` 1.3e-3✱ · `వ` 0.81 · `ణ` 0.01 · `్య` 3.9e-3✱ · `్` 1.7e-3✱ · `న` 0.70 · `్` 1.2e-3✱ · `గా` 1.2e-3✱ · `␣ల` 0.18 · `ంక` 0.53 · `న్` 0.03✱ · `␣చే` 0.39 · `⏎` 2.3e-6 forced |
| 2 | `ప` 0.17 · `్రా` 0.18✱ · `మ` 3.4e-4✱ · `్య` 0.04✱ · `న` 0.07 · `్` 0.01✱ · `న` 0.45 · `్` 0.41 · `గా` 0.90 · `␣సా` 0.09 · `గ` 0.62 · `్య` 0.12✱ · `్` 0.01✱ · `న` 0.76 · `్` 0.90 · `బా` 6.6e-5✱ · `␣గ` 0.08 · `మ` 0.89 · `్య` 0.87 · `్` 0.16 · `న` 0.83 · `్` 0.61 · `నే` 0.15 · `␣చే` 6.7e-3✱ · `⏎` 1.00 forced |
| 3 | `భ` 0.08 · `ూ` 0.29 · `మ` 0.52 · `్య` 0.94 · `న` 0.64 · `్` 0.98 · `న` 0.98 · `్` 0.94 · `గా` 0.99 · `␣దా` 0.23 · `ట` 0.48✱ · `్య` 0.92 · `్` 0.99 · `న` 1.00 · `్` 0.99 · `బ` 8.3e-4✱ · `ూ` 0.31 · `␣స` 0.47 · `ంద్ర` 0.01✱ · `్` 0.45 · `గా` 0.01 · `␣చే` 0.71 · `⏎` 1.00 forced |
| 4 | `శ` 0.12 · `ౌ` 0.08✱ · `మ` 0.01✱ · `్య` 0.99 · `న` 0.95 · `్` 0.99 · `న` 1.00 · `్` 0.99 · `గా` 1.00 · `␣వచ్చ` 0.03 · `్య` 0.97 · `్` 0.99 · `న` 1.00 · `న్` 0.01✱ · `␣ల` 0.77 · `ంక` 0.68 · `న్` 0.85 · `␣చే` 0.58 |

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

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 83 tokens · 16.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | భూమిన్ తరించెను భయంబు తీరితిన్ | `UUIUIIIUIUIU` |
| 2 | శైమృథ్యమున్యెను శరణ్యమున్యెనున్ | `UUIUIIIUIUIU` |
| 3 | సౌమన్యమున్యెను సముద్ర్ధ్ణమున్యెనున్ | `UUIUIIIUIUIU` |
| 4 | లౌమిక్యమున్యెను లఘుగ్య్య్ణమున్యెనున్ | `UUIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.079 · model's first choice kept 55% · constraint overrode 40% · backtracks 0

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `భ` 0.04 · `ూ` 0.42 · `మి` 0.46 · `న్` 0.04✱ · `␣త` 0.12✱ · `రించ` 5.0e-3✱ · `ె` 0.56 · `ను` 0.70 · `␣భ` 0.07 · `యం` 0.12✱ · `బు` 0.29 · `␣తీ` 0.03 · `రి` 0.58 · `తి` 0.07 · `న్` 0.46 · `⏎` 0.84 forced |
| 2 | `శ` 0.06 · `ై` 0.25✱ · `మ` 2.8e-5✱ · `ృ` 0.36 · `థ` 0.19✱ · `్య` 2.4e-3✱ · `ము` 0.18 · `న` 0.18✱ · `్య` 7.8e-5✱ · `ె` 0.43 · `ను` 0.54 · `␣శ` 0.27 · `రణ` 0.03✱ · `్య` 0.18✱ · `ము` 0.77 · `న` 0.10✱ · `్య` 1.1e-4✱ · `ె` 0.98 · `ను` 0.82 · `న్` 6.6e-5✱ · `⏎` 1.00 forced |
| 3 | `స` 0.26 · `ౌ` 2.7e-5✱ · `మ` 6.7e-3✱ · `న్య` 0.15✱ · `ము` 0.78 · `న` 0.47 · `్య` 0.12✱ · `ె` 0.99 · `ను` 0.99 · `␣స` 0.64 · `ము` 0.70 · `ద్ర` 0.91 · `్` 1.9e-5✱ · `ధ` 0.54 · `్` 0.02✱ · `ణ` 2.1e-5✱ · `ము` 0.24✱ · `న` 0.96 · `్య` 0.99 · `ె` 1.00 · `ను` 1.00 · `న్` 0.89 · `⏎` 1.00 forced |
| 4 | `ల` 0.24✱ · `ౌ` 7.2e-3✱ · `మిక` 3.8e-6✱ · `్య` 0.10✱ · `ము` 0.86 · `న` 0.92 · `్య` 0.99 · `ె` 1.00 · `ను` 1.00 · `␣ల` 0.94 · `ఘ` 6.5e-4✱ · `ు` 0.99 · `గ` 0.11✱ · `్య` 6.0e-4✱ · `్య` 1.7e-3✱ · `్` 2.3e-5✱ · `ణ` 0.72 · `ము` 0.97 · `న` 0.99 · `్య` 1.00 · `ె` 1.00 · `ను` 1.00 · `న్` 1.00 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 78 tokens · 12.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిక్రియా నిలువెటన్య్ర్ధమై నిలిచ్ | `UUIUIIIUIUIU` |
| 2 | తల్లిప్రియత్య కరుణా జ్య్వ్ధమై మెరిచ్ | `UUIUIIIUIUIU` |
| 3 | తల్లిభ్రమణ్న సకలత్య సత్యమై | `UUIUIIIUIUIU` |
| 4 | తల్లిప్రణయ్న తులయేన్న్న్ధమై ఉదిచ్ | `UUIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 15% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.040 · model's first choice kept 44% · constraint overrode 45% · backtracks 0

<details><summary>Token probabilities (78 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.81 · `ల్లి` 0.79 · `క` 0.03✱ · `్రి` 8.1e-7✱ · `యా` 0.68 · `␣ని` 0.08 · `లు` 2.9e-3✱ · `వె` 0.41 · `ట` 0.01✱ · `న` 0.05✱ · `్య` 5.8e-5✱ · `్ర` 4.2e-4✱ · `్` 3.8e-6✱ · `ధ` 7.0e-3✱ · `మై` 0.05✱ · `␣ని` 0.28 · `లి` 0.58 · `చ` 0.02✱ · `్` 1.3e-11✱ · `⏎` 2.4e-4 forced |
| 2 | `త` 0.68 · `ల్లి` 0.82 · `ప` 0.16 · `్రియ` 0.04✱ · `త` 0.21✱ · `్య` 0.01✱ · `␣క` 0.05 · `రుణ` 0.84 · `ా` 0.41 · `␣జ` 0.02✱ · `్య` 0.25✱ · `్వ` 1.7e-5✱ · `్` 8.7e-8✱ · `ధ` 0.02✱ · `మై` 0.88 · `␣మె` 0.30 · `రి` 0.99 · `చ` 0.10✱ · `్` 0.99 · `⏎` 1.00 forced |
| 3 | `త` 0.98 · `ల్లి` 0.93 · `భ` 0.11✱ · `్ర` 1.1e-5✱ · `మణ` 0.13✱ · `్` 0.01✱ · `న` 0.32 · `␣స` 0.08 · `క` 0.02✱ · `ల` 0.97 · `త` 0.06 · `్య` 0.38 · `␣స` 0.04✱ · `త్య` 0.62 · `మై` 0.79 · `⏎` 1.0e-5 forced |
| 4 | `త` 1.00 · `ల్లి` 0.95 · `ప్ర` 0.36 · `ణ` 4.6e-3✱ · `య` 0.73 · `్` 0.09✱ · `న` 0.76 · `␣త` 0.01 · `ుల` 0.15 · `యే` 1.9e-3✱ · `న` 0.33 · `్` 0.01✱ · `న` 0.66 · `్` 3.6e-3✱ · `న` 0.62 · `్` 0.06✱ · `ధ` 0.02✱ · `మై` 0.95 · `␣ఉ` 0.07 · `ది` 0.11 · `చ` 0.99 · `్` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 90 tokens · 30.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జై శ్రీనివాసుని రథం ల్వ్వ్సనై ప్రయా | `UUIUIIIUIUIU` |
| 2 | సీశ్రం శివాయుధమునై ర్వ్వ్సృయమ్యురా | `UUIUIIIUIUIU` |
| 3 | దశ్రుచ్యురై దెవతృపత్యమున్రథం | `UUIUIIIUIUIU` |
| 4 | వ్యాశ్రుచ్యురై వనమునై ర్వ్వ్సమయ్యురా | `UUIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 15% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.062 · model's first choice kept 47% · constraint overrode 44% · backtracks 30

<details><summary>Token probabilities (90 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జ` 0.05 · `ై` 0.46 · `␣శ్రీ` 0.23 · `ని` 5.7e-3✱ · `వా` 1.00 · `సు` 0.10 · `ని` 0.72 · `␣ర` 0.31 · `థ` 6.9e-3✱ · `ం` 0.15✱ · `␣ల` 0.40 · `్వ` 3.0e-6✱ · `్వ` 3.2e-4✱ · `్` 6.2e-3✱ · `స` 1.9e-3✱ · `న` 0.25 · `ై` 0.02✱ · `␣ప్ర` 0.04✱ · `యా` 0.34 · `⏎` 5.9e-6 forced |
| 2 | `సీ` 0.19 · `శ` 5.0e-8✱ · `్ర` 1.0e-3✱ · `ం` 0.34 · `␣శి` 0.04✱ · `వ` 0.43 · `ాయ` 0.08✱ · `ు` 0.19 · `ధ` 0.43 · `ము` 0.43 · `న` 0.09 · `ై` 9.8e-3✱ · `␣ర` 0.32 · `్వ` 3.6e-6✱ · `్వ` 0.15 · `్` 0.72 · `స` 0.76 · `ృ` 5.2e-5✱ · `య` 0.23 · `మ` 9.6e-3✱ · `్య` 0.16✱ · `ు` 9.4e-3✱ · `రా` 4.9e-3✱ · `⏎` 1.00 forced |
| 3 | `ద` 0.06✱ · `శ` 0.32 · `్రు` 7.7e-3✱ · `చ` 0.09 · `్య` 0.22 · `ు` 0.21 · `ర` 0.13 · `ై` 0.04✱ · `␣ద` 0.33 · `ె` 0.04✱ · `వ` 0.11✱ · `త` 0.20 · `ృ` 0.16✱ · `ప` 0.21 · `త` 0.06✱ · `్య` 0.01✱ · `ము` 0.08✱ · `న` 0.86 · `్ర` 5.7e-5✱ · `థ` 0.01✱ · `ం` 0.57 · `⏎` 0.75 forced |
| 4 | `వ` 0.03✱ · `్యా` 0.04✱ · `శ` 1.4e-3✱ · `్రు` 0.16✱ · `చ` 0.32 · `్య` 0.95 · `ు` 0.89 · `ర` 0.92 · `ై` 0.98 · `␣వ` 0.20 · `న` 0.52 · `ము` 0.28 · `న` 0.85 · `ై` 0.34 · `␣ర` 0.38 · `్వ` 0.20✱ · `్వ` 0.85 · `్` 0.93 · `స` 0.95 · `మ` 0.12 · `య` 0.20✱ · `్య` 1.7e-3✱ · `ు` 0.59 · `రా` 0.86 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 83 tokens · 24.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | భూమిన్ తరించెను వనమ్రుధుల్యెనెన్ | `UUIUIIIUIUIU` |
| 2 | ప్రాముడ్యునిన్ కనబడెన్ దహన్యెనన్ | `UUIUIIIUIUIU` |
| 3 | వ్యామున్యెనున్ దహనకళ్యనమ్యెనన్ | `UUIUIIIUIUIU` |
| 4 | వ్యామర్యెనున్ శివమయమ్యనమ్యెనన్ | `UUIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 10% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.092 · model's first choice kept 43% · constraint overrode 44% · backtracks 16

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `భ` 0.04 · `ూ` 0.42 · `మి` 0.46 · `న్` 0.04✱ · `␣త` 0.12✱ · `రించ` 5.0e-3✱ · `ె` 0.56 · `ను` 0.70 · `␣వ` 0.06 · `న` 0.01✱ · `మ` 0.12✱ · `్రు` 4.7e-4✱ · `ధ` 0.18 · `ుల` 0.39 · `్య` 1.5e-3✱ · `ె` 0.14✱ · `న` 0.31 · `ె` 9.4e-3✱ · `న్` 0.03✱ · `⏎` 0.96 forced |
| 2 | `ప` 0.07 · `్రా` 0.12✱ · `ము` 4.3e-3✱ · `డ` 0.23 · `్య` 0.05✱ · `ు` 0.19✱ · `ని` 0.71 · `న్` 8.3e-3✱ · `␣క` 0.02✱ · `న` 0.04✱ · `బ` 0.21 · `డ` 0.91 · `ె` 0.93 · `న్` 0.08✱ · `␣ద` 0.05 · `హ` 6.8e-3✱ · `న` 0.75 · `్య` 4.2e-3✱ · `ె` 0.31 · `న` 0.72 · `న్` 0.80 · `⏎` 1.00 forced |
| 3 | `వ` 0.07 · `్యా` 2.4e-3✱ · `ము` 1.1e-3✱ · `న` 0.09✱ · `్య` 4.8e-3✱ · `ె` 0.18 · `ను` 0.20 · `న్` 0.02✱ · `␣ద` 0.03 · `హ` 0.05✱ · `న` 0.21✱ · `క` 0.02 · `ళ` 0.04 · `్య` 0.41 · `న` 0.01✱ · `మ` 0.23✱ · `్య` 0.32 · `ె` 0.91 · `న` 0.85 · `న్` 0.99 · `⏎` 1.00 forced |
| 4 | `వ` 0.03✱ · `్యా` 0.02✱ · `మ` 2.6e-3✱ · `ర` 0.31 · `్య` 0.47 · `ె` 0.21 · `ను` 0.83 · `న్` 1.00 · `␣శి` 6.5e-3 · `వ` 0.17 · `మ` 0.34 · `య` 0.06✱ · `మ` 0.13✱ · `్య` 0.67 · `న` 0.02✱ · `మ` 0.30 · `్య` 1.00 · `ె` 1.00 · `న` 1.00 · `న్` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 86 tokens · 6.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవ్వాణుడెన్ తలమునై స్ర్వమున్యుడా | `UUIUIIIUIUIU` |
| 2 | వ్యావ్వాణుడెన్ దనున లంక్యనగ్రమా | `UUIUIIIUIUIU` |
| 3 | పవ్వాణుడెన్ గమనమున్య్య్వలెంకయే | `UUIUIIIUIUIU` |
| 4 | వ్యావ్వాణుడెన్ దనున తల్యనగ్రమా | `UUIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.078 · model's first choice kept 53% · constraint overrode 31% · backtracks 0

<details><summary>Token probabilities (86 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.23 · `వ` 0.39 · `్వ` 3.5e-7✱ · `ా` 0.26 · `ణ` 0.09 · `ు` 0.03✱ · `డ` 0.13 · `ె` 0.52 · `న్` 0.16✱ · `␣త` 0.08✱ · `ల` 0.21 · `ము` 0.51 · `న` 0.34 · `ై` 0.03✱ · `␣స` 0.06 · `్ర` 1.3e-4✱ · `్వ` 2.4e-5✱ · `ము` 0.02✱ · `న` 0.18✱ · `్య` 3.1e-4✱ · `ు` 0.10✱ · `డా` 0.01 · `⏎` 0.85 forced |
| 2 | `వ` 0.08 · `్యా` 8.5e-3✱ · `వ` 0.01✱ · `్వ` 1.3e-5✱ · `ా` 0.50 · `ణ` 0.47 · `ు` 0.15 · `డ` 0.82 · `ె` 0.91 · `న్` 0.98 · `␣ద` 0.09 · `ను` 4.2e-3✱ · `న` 0.09 · `␣ల` 2.1e-3✱ · `ం` 0.43 · `క` 0.02✱ · `్య` 5.6e-3✱ · `న` 0.02✱ · `గ` 0.04✱ · `్ర` 3.0e-4✱ · `మా` 0.02 · `⏎` 1.00 forced |
| 3 | `ప` 0.15 · `వ` 0.88 · `్వ` 0.96 · `ా` 0.99 · `ణ` 0.99 · `ు` 0.92 · `డ` 0.95 · `ె` 0.98 · `న్` 1.00 · `␣గ` 0.15 · `మన` 0.06 · `ము` 0.86 · `న` 0.80 · `్య` 2.1e-3✱ · `్య` 8.1e-4✱ · `్వ` 4.3e-4✱ · `ల` 0.02✱ · `ెం` 0.01 · `క` 0.30 · `యే` 0.01 · `⏎` 0.91 forced |
| 4 | `వ` 0.92 · `్యా` 0.99 · `వ` 1.00 · `్వ` 1.00 · `ా` 1.00 · `ణ` 1.00 · `ు` 1.00 · `డ` 1.00 · `ె` 1.00 · `న్` 1.00 · `␣ద` 0.07 · `ను` 0.21 · `న` 0.90 · `␣త` 0.04 · `ల` 0.33 · `్య` 0.01✱ · `న` 0.38 · `గ` 0.52 · `్ర` 0.44 · `మా` 0.93 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 81 tokens · 5.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీరామునిన్ని రఘుమహ్రితం లమై | `UUIUIIIUIUIU` |
| 2 | సీరద్రినిన్ నివసయే ర్వ్ఱ్షితం భయం | `UUIUIIIUIUIU` |
| 3 | మారద్రినిన్ మరణమున్య్న్మ లంకలో | `UUIUIIIUIUIU` |
| 4 | ప్రారణ్ద్రినిన్ పరిరకమ్య్న్వ నర్యణం | `UUIUIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 15% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.038 · model's first choice kept 40% · constraint overrode 44% · backtracks 0

<details><summary>Token probabilities (81 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.16 · `్రీ` 0.99 · `రా` 0.72 · `ము` 0.55 · `ని` 0.70 · `న` 3.1e-3✱ · `్` 4.0e-5✱ · `ని` 0.57 · `␣ర` 0.46 · `ఘ` 1.9e-3✱ · `ు` 0.99 · `మ` 0.31 · `హ` 0.35✱ · `్ర` 6.2e-6✱ · `ిత` 8.9e-3✱ · `ం` 0.19 · `␣ల` 0.05✱ · `మై` 9.4e-5✱ · `⏎` 0.44 forced |
| 2 | `సీ` 0.79 · `ర` 1.2e-6✱ · `ద` 0.05 · `్రి` 3.5e-3✱ · `ని` 0.27 · `న్` 0.02✱ · `␣ని` 0.08 · `వ` 0.19 · `స` 0.14✱ · `యే` 7.6e-3✱ · `␣ర` 0.06 · `్వ` 3.6e-6✱ · `్` 3.2e-4✱ · `ఱ` 0.07 · `్` 0.09✱ · `ష` 6.2e-5✱ · `ిత` 0.03✱ · `ం` 0.85 · `␣భ` 0.01✱ · `యం` 0.06 · `⏎` 0.98 forced |
| 3 | `మ` 0.02✱ · `ార` 0.06✱ · `ద` 0.35 · `్రి` 0.75 · `ని` 0.73 · `న్` 0.76 · `␣మ` 0.60 · `రణ` 0.06✱ · `ము` 0.28 · `న` 0.11✱ · `్య` 3.5e-4✱ · `్` 0.01✱ · `న` 0.36 · `్` 3.0e-3✱ · `మ` 3.7e-3✱ · `␣ల` 0.02 · `ం` 0.44 · `క` 0.11✱ · `లో` 0.10 · `⏎` 0.26 forced |
| 4 | `ప` 0.05 · `్రా` 0.21✱ · `రణ` 7.8e-6✱ · `్` 0.17 · `ద` 0.30 · `్రి` 0.65 · `ని` 0.91 · `న్` 0.90 · `␣పరి` 0.13 · `ర` 0.35 · `క` 1.1e-3✱ · `మ` 0.03✱ · `్య` 0.55 · `్` 0.80 · `న` 0.86 · `్` 0.62 · `వ` 5.5e-3✱ · `␣న` 0.05 · `ర` 0.37 · `్య` 1.5e-4✱ · `ణం` 7.4e-3 |

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

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 68 tokens · 19.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | గమనము వీడి సముద్రము | `IIIIUIIUII` |
| 2 | వమానమున సాగి లంక గ్య్వానమును దరిచ్ | `IUIIIUIUIUIIIIU` |
| 3 | నమము ద్యుగము దాటెను హను | `IIIIIIUIIII` |
| 4 | దృమగమమున సాగి లంక గ్య్వేతమును దరిచ్ | `IIIIIIUIUIUIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 41% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.076 · model's first choice kept 50% · constraint overrode 31% · backtracks 0

<details><summary>Token probabilities (68 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `గ` 0.08 · `మ` 0.81 · `న` 0.34 · `ము` 0.71 · `␣వీ` 0.03 · `డి` 0.45 · `␣స` 0.05 · `ము` 0.99 · `ద్ర` 0.92 · `ము` 0.47 · `⏎` 8.8e-5 forced |
| 2 | `వ` 0.07 · `మా` 7.0e-5✱ · `న` 0.94 · `ము` 0.30 · `న` 0.17✱ · `␣సా` 0.10 · `గి` 0.50 · `␣ల` 0.79 · `ంక` 0.78 · `␣గ` 0.01✱ · `్య` 4.3e-8✱ · `్వ` 1.1e-4✱ · `ాన` 0.06 · `ము` 0.77 · `ను` 0.03✱ · `␣ద` 3.7e-3✱ · `రి` 0.07✱ · `చ` 0.06✱ · `్` 4.8e-11✱ · `⏎` 5.5e-5 forced |
| 3 | `న` 0.02 · `మ` 0.15✱ · `ము` 0.12✱ · `␣ద` 0.02✱ · `్య` 0.02✱ · `ు` 0.07✱ · `గ` 0.45 · `ము` 0.91 · `␣దా` 0.51 · `ట` 0.22 · `ె` 0.75 · `ను` 0.59 · `␣హ` 0.06✱ · `ను` 0.99 · `⏎` 1.3e-5 forced |
| 4 | `ద` 0.02 · `ృ` 0.01✱ · `మ` 1.3e-4✱ · `గ` 0.16 · `మ` 0.70 · `ము` 0.54 · `న` 0.54 · `␣సా` 0.21 · `గి` 0.88 · `␣ల` 0.70 · `ంక` 0.85 · `␣గ` 0.08✱ · `్య` 0.93 · `్వ` 0.98 · `ే` 7.9e-6✱ · `త` 0.59 · `ము` 0.84 · `ను` 0.71 · `␣ద` 0.46 · `రి` 0.96 · `చ` 0.95 · `్` 0.95 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 54 tokens · 9.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లికరుణయే జగతికి | `UIIIIUIIII` |
| 2 | అల్లకలది కరుణయే మృహమునందునుగా | `UIIIIIIIUIIIUIIU` |
| 3 | తల్లిని ప్రేమించు ప్రతి మ | `UIIUUIIII` |
| 4 | జల్లోన నిలిచెను జగతి సత్యముగామున్ | `UUIIIIIIIIUIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 38% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.047 · model's first choice kept 46% · constraint overrode 37% · backtracks 0

<details><summary>Token probabilities (54 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.58 · `ల్లి` 0.77 · `క` 0.03✱ · `రుణ` 0.70 · `యే` 0.17 · `␣జగ` 0.56 · `తి` 0.90 · `కి` 0.81 · `⏎` 2.8e-5 forced |
| 2 | `అ` 0.34 · `ల` 0.03✱ · `్` 8.7e-7✱ · `ల` 0.80 · `క` 0.12 · `ల` 0.16 · `ది` 0.05 · `␣క` 0.04 · `రుణ` 0.79 · `యే` 0.04✱ · `␣మ` 0.18✱ · `ృ` 8.2e-5✱ · `హ` 2.0e-5✱ · `ము` 0.06✱ · `న` 0.32 · `ందు` 0.12✱ · `ను` 0.02✱ · `గా` 1.3e-3✱ · `⏎` 0.97 forced |
| 3 | `త` 0.52 · `ల్లి` 0.84 · `ని` 0.09 · `␣ప్రేమ` 0.74 · `ించు` 0.03✱ · `␣ప్రతి` 0.08 · `␣మ` 0.14✱ · `⏎` 3.1e-7 forced |
| 4 | `జ` 0.02 · `ల` 0.03✱ · `్` 7.9e-9✱ · `లో` 0.24 · `న` 0.71 · `␣ని` 0.07 · `లి` 0.40 · `చె` 0.47 · `ను` 0.76 · `␣జగ` 0.17 · `తి` 0.75 · `␣స` 0.11✱ · `త్య` 0.82 · `ము` 0.81 · `గా` 0.55 · `ము` 1.0e-4✱ · `న` 2.6e-4✱ · `్` 1.0e-5✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 52 tokens · 26.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | అమ్మకల ప్రేమ జగతికి | `UIIIUIIIII` |
| 2 | కమ్మనవని తల్లి మమత గాంచుమెను సుమా | `UIIIIUIIIIUIIIIU` |
| 3 | అమ్మెల ప్రేమ జగతికిన | `UIIUIIIIII` |
| 4 | కమ్మనవని తల్లి మమత కనులందు నిలుమ్ | `UIIIIUIIIIIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.103 · model's first choice kept 50% · constraint overrode 18% · backtracks 30

<details><summary>Token probabilities (52 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `అ` 0.10 · `మ్మ` 0.62 · `క` 0.05✱ · `ల` 3.8e-3✱ · `␣ప్రేమ` 0.43 · `␣జగ` 0.12 · `తి` 0.93 · `కి` 0.57 · `⏎` 2.1e-4 forced |
| 2 | `క` 0.04 · `మ్మ` 0.03✱ · `న` 0.34 · `వ` 8.5e-3✱ · `ని` 0.21 · `␣తల్లి` 4.9e-3 · `␣మ` 0.04 · `మ` 0.81 · `త` 0.88 · `␣గా` 2.5e-3✱ · `ంచు` 0.08 · `మె` 5.5e-3 · `ను` 0.03 · `␣సు` 0.03✱ · `మా` 0.28 · `⏎` 0.96 forced |
| 3 | `అ` 0.28 · `మ్` 0.04 · `మె` 0.09 · `ల` 0.06 · `␣ప్రేమ` 0.06 · `␣జగ` 0.33 · `తి` 0.99 · `కి` 0.89 · `న` 1.8e-4✱ · `⏎` 0.32 forced |
| 4 | `క` 0.36 · `మ్మ` 0.27 · `న` 0.85 · `వ` 0.97 · `ని` 0.98 · `␣తల్లి` 0.79 · `␣మ` 0.93 · `మ` 1.00 · `త` 0.98 · `␣క` 0.02 · `ను` 0.26 · `ల` 0.86 · `ందు` 0.61 · `␣ని` 0.37 · `లు` 0.43 · `మ` 9.9e-3✱ · `్` 2.2e-6✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 55 tokens · 18.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి కరుణా మదిని తా | `UIIIUIIIU` |
| 2 | తల్లి అనురతిని జగమొక దైవముగా భా | `UIIIIIIIIIIUIIUU` |
| 3 | తల్లి మమతే జగతికి స | `UIIIUIIIII` |
| 4 | తల్లి దయ వెలసినటి తలధారల వలెనై | `UIIIIIIIIIIUIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 44% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.138 · model's first choice kept 53% · constraint overrode 29% · backtracks 12

<details><summary>Token probabilities (55 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.58 · `ల్లి` 0.77 · `␣క` 0.03✱ · `రుణ` 0.97 · `ా` 0.27 · `␣మ` 0.18 · `ది` 0.37 · `ని` 0.08✱ · `␣తా` 0.24 · `⏎` 7.2e-8 forced |
| 2 | `త` 0.22 · `ల్లి` 0.77 · `␣అను` 7.5e-3✱ · `ర` 9.6e-3✱ · `తి` 0.94 · `ని` 0.09✱ · `␣జగ` 0.02 · `మ` 0.27 · `ొ` 9.2e-4✱ · `క` 0.81 · `␣ద` 0.01✱ · `ై` 0.73 · `వ` 0.80 · `ము` 0.59 · `గా` 0.23✱ · `␣భా` 0.34 · `⏎` 1.1e-5 forced |
| 3 | `త` 0.57 · `ల్లి` 0.90 · `␣మ` 0.01✱ · `మ` 0.96 · `త` 0.76 · `ే` 0.02 · `␣జగ` 0.21 · `తి` 0.89 · `కి` 0.87 · `␣స` 0.02✱ · `⏎` 2.8e-7 forced |
| 4 | `త` 0.96 · `ల్లి` 0.92 · `␣ద` 2.4e-3✱ · `య` 0.92 · `␣వె` 5.3e-3✱ · `ల` 0.44 · `సిన` 0.16 · `టి` 0.01 · `␣త` 0.02 · `ల` 0.32 · `ధ` 3.0e-4✱ · `ార` 0.86 · `ల` 0.05✱ · `␣వ` 0.05 · `లె` 0.53 · `న` 0.17✱ · `ై` 0.35 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 65 tokens · 4.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి కరుణా మదిని తా | `UIIIUIIIU` |
| 2 | తల్లి అనురతిని తలచుచు న్య్య్థా నందుని పో | `UIIIIIIIIIIUUIIU` |
| 3 | అల్ల కరుణా మదిని తా | `UIIIUIIIU` |
| 4 | అల్ల అనురతిని తలచుచు న్య్య్థా నందుని పో | `UIIIIIIIIIIUUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 40% · single-akshara words 30% · repeated lines 0 · mean token probability (geometric) 0.138 · model's first choice kept 66% · constraint overrode 26% · backtracks 0

<details><summary>Token probabilities (65 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.58 · `ల్లి` 0.77 · `␣క` 0.03✱ · `రుణ` 0.97 · `ా` 0.27 · `␣మ` 0.18 · `ది` 0.37 · `ని` 0.08✱ · `␣తా` 0.24 · `⏎` 7.2e-8 forced |
| 2 | `త` 0.22 · `ల్లి` 0.77 · `␣అను` 7.5e-3✱ · `ర` 9.6e-3✱ · `తి` 0.94 · `ని` 0.09✱ · `␣త` 0.31 · `ల` 0.92 · `చు` 0.29 · `చు` 0.15✱ · `␣న` 0.05✱ · `్య` 2.2e-5✱ · `్య` 1.2e-6✱ · `్` 1.1e-4✱ · `థ` 8.4e-4✱ · `ా` 0.37 · `␣న` 0.01✱ · `ందు` 0.07 · `ని` 0.04 · `␣పో` 0.03✱ · `⏎` 0.05 forced |
| 3 | `అ` 0.08 · `ల` 0.02✱ · `్` 5.3e-7✱ · `ల` 0.80 · `␣క` 0.04 · `రుణ` 0.65 · `ా` 0.30 · `␣మ` 0.17 · `ది` 0.93 · `ని` 0.81 · `␣తా` 0.54 · `⏎` 1.00 forced |
| 4 | `అ` 0.62 · `ల` 0.18✱ · `్` 0.54 · `ల` 0.94 · `␣అను` 0.36 · `ర` 0.73 · `తి` 0.99 · `ని` 0.94 · `␣త` 0.77 · `ల` 0.99 · `చు` 0.95 · `చు` 0.97 · `␣న` 0.46 · `్య` 0.96 · `్య` 1.00 · `్` 1.00 · `థ` 1.00 · `ా` 1.00 · `␣న` 0.91 · `ందు` 0.98 · `ని` 0.99 · `␣పో` 0.90 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 77 tokens · 5.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | జయ హనుమంతుడె సాగర | `IIIIUIIUII` |
| 2 | గె యెను లొక లొనకల లోకగీతమున సదా | `IIIIIIIIIUIUIIIIU` |
| 3 | గె యెను లొక లొనకల యెనక | `IIIIIIIIIIII` |
| 4 | మృ యెను లొక లొనకల మాయమృత్యుగమనమై | `IIIIIIIIIUIUIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 32% · single-akshara words 16% · repeated lines 0 · mean token probability (geometric) 0.105 · model's first choice kept 58% · constraint overrode 27% · backtracks 0

<details><summary>Token probabilities (77 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `జయ` 0.02 · `␣హ` 0.41 · `ను` 0.99 · `మం` 0.29 · `తు` 1.00 · `డ` 0.20 · `ె` 0.39✱ · `␣సా` 0.38 · `గర` 0.34 · `⏎` 1.7e-5 forced |
| 2 | `గ` 0.22 · `ె` 6.0e-4✱ · `␣` 1.2e-7✱ · `య` 2.2e-5✱ · `ె` 0.45 · `ను` 0.30 · `␣ల` 0.85 · `ొ` 8.9e-5✱ · `క` 0.04✱ · `␣ల` 0.24 · `ొ` 6.2e-4✱ · `న` 0.12 · `క` 0.57 · `ల` 0.06 · `␣లో` 0.20 · `క` 0.88 · `గ` 7.9e-4✱ · `ీ` 2.9e-3✱ · `త` 0.69 · `ము` 0.63 · `న` 0.05✱ · `␣స` 1.5e-3✱ · `దా` 0.14 · `⏎` 0.96 forced |
| 3 | `గ` 0.10 · `ె` 0.10✱ · `␣` 0.43 · `య` 0.95 · `ె` 0.99 · `ను` 0.96 · `␣ల` 0.52 · `ొ` 0.96 · `క` 1.00 · `␣ల` 0.97 · `ొ` 1.00 · `న` 1.00 · `క` 1.00 · `ల` 1.00 · `␣య` 3.8e-3✱ · `ె` 0.26✱ · `న` 0.21 · `క` 0.15 · `⏎` 0.49 forced |
| 4 | `మ` 0.04 · `ృ` 0.03✱ · `␣` 9.1e-4✱ · `య` 1.2e-3✱ · `ె` 0.26 · `ను` 0.81 · `␣ల` 0.51 · `ొ` 0.82 · `క` 0.90 · `␣ల` 0.40 · `ొ` 0.99 · `న` 0.97 · `క` 0.99 · `ల` 0.98 · `␣మ` 0.11 · `ాయ` 0.11 · `మ` 0.09✱ · `ృ` 3.1e-3✱ · `త్య` 0.07 · `ు` 0.97 · `గ` 0.34 · `మ` 0.25 · `న` 0.17✱ · `మై` 0.01 |

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

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 83 tokens · 15.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతికి దొరి గ్న్య్తమున నిత్యము నిలిచెన్ | `UIUIIIIIIIIIIUIIIIU` |
| 2 | తల్లి దయ జగతికి మూలధనముగా నిలచెను నిస్ | `UIIIIIIIUIIIIUIIIIU` |
| 3 | తల్లి అనురతి జగతికి దిదర్ఘమైన సుఖముగా | `UIIIIIIIIIIUIUIIIIU` |
| 4 | తల్లి దీవెన జగతికి ధ్రుదయిన తేజముగ నిలిచ్ | `UIUIIIIIIIIIIUIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 54% · single-akshara words 4% · repeated lines 0 · mean token probability (geometric) 0.074 · model's first choice kept 54% · constraint overrode 35% · backtracks 0

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.74 · `ల్లి` 0.79 · `␣ప్రేమ` 0.75 · `␣జగ` 0.30 · `తి` 0.95 · `కి` 0.51 · `␣ద` 0.05 · `ొ` 2.7e-3✱ · `రి` 0.36 · `␣గ` 5.2e-7✱ · `్` 1.7e-5✱ · `న` 0.12✱ · `్య` 8.6e-4✱ · `్` 5.8e-5✱ · `త` 6.0e-3✱ · `ము` 0.44 · `న` 0.12✱ · `␣ని` 0.02✱ · `త్య` 0.33 · `ము` 0.64 · `␣ని` 4.5e-3✱ · `లి` 0.43 · `చె` 0.78 · `న్` 0.03✱ · `⏎` 0.98 forced |
| 2 | `త` 0.34 · `ల్లి` 0.70 · `␣ద` 0.06 · `య` 0.91 · `␣జగ` 0.17✱ · `తి` 0.74 · `కి` 0.79 · `␣మూ` 0.03 · `ల` 0.96 · `ధ` 0.04✱ · `న` 0.40 · `ము` 0.72 · `గా` 0.25 · `␣ని` 0.47 · `ల` 0.12✱ · `చె` 0.95 · `ను` 0.06✱ · `␣ని` 0.13 · `స్` 0.01✱ · `⏎` 4.0e-9 forced |
| 3 | `త` 0.85 · `ల్లి` 0.88 · `␣అను` 0.18 · `ర` 0.02✱ · `తి` 0.96 · `␣జగ` 0.23 · `తి` 0.90 · `కి` 0.75 · `␣ది` 0.02✱ · `ద` 3.8e-7✱ · `ర్` 4.8e-3✱ · `ఘ` 1.00 · `మైన` 0.45 · `␣సు` 0.02 · `ఖ` 0.27 · `ము` 0.86 · `గా` 0.32 · `⏎` 4.7e-3 forced |
| 4 | `త` 0.99 · `ల్లి` 0.96 · `␣దీ` 0.03 · `వె` 0.98 · `న` 1.00 · `␣జగ` 0.92 · `తి` 0.99 · `కి` 0.92 · `␣ధ` 0.02✱ · `్రు` 5.6e-3✱ · `దయ` 3.3e-4✱ · `ిన` 0.18✱ · `␣తే` 0.17 · `జ` 0.99 · `ము` 0.52 · `గ` 6.5e-3✱ · `␣ని` 0.20✱ · `లి` 0.55 · `చ` 3.1e-3✱ · `్` 5.2e-10✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 79 tokens · 13.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమయే జగతికి తలపున మరువదగినద్ | `UIUIUIIIIIIIIIIIIIU` |
| 2 | తల్లి అనురతికది తరగెదని తలచి నిలిచినదై | `UIIIIIIIIIIIIIIIIIIIU` |
| 3 | తల్లి దీవెనల ధ్రువతని ధారయే నిలిచినదై | `UIUIIIIIIIUIUIIIIU` |
| 4 | తల్లి ప్రేమయే జగతికి తలపున నిలిచినదృఢమ్ | `UIUIUIIIIIIIIIIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 40% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.126 · model's first choice kept 54% · constraint overrode 26% · backtracks 0

<details><summary>Token probabilities (79 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.74 · `ల్లి` 0.79 · `␣ప్రేమ` 0.75 · `యే` 0.23 · `␣జగ` 0.63 · `తి` 0.94 · `కి` 0.78 · `␣త` 0.03✱ · `ల` 0.81 · `పు` 0.74 · `న` 0.10 · `␣మ` 0.07 · `రు` 0.13 · `వ` 0.93 · `ద` 0.22 · `గిన` 0.41 · `ద` 0.01✱ · `్` 3.3e-10✱ · `⏎` 3.5e-4 forced |
| 2 | `త` 0.49 · `ల్లి` 0.75 · `␣అను` 0.09 · `ర` 7.4e-3✱ · `తి` 0.85 · `క` 4.4e-3✱ · `ది` 1.8e-3✱ · `␣తర` 0.20 · `గ` 0.90 · `ె` 1.1e-4✱ · `ద` 0.13✱ · `ని` 0.09 · `␣త` 0.12✱ · `ల` 0.80 · `చి` 0.21 · `␣ని` 0.23✱ · `లి` 0.52 · `చిన` 0.46 · `ద` 0.80 · `ై` 0.02✱ · `⏎` 1.00 forced |
| 3 | `త` 0.95 · `ల్లి` 0.93 · `␣దీ` 0.16 · `వె` 0.97 · `న` 0.98 · `ల` 0.16✱ · `␣ధ` 0.09 · `్రు` 1.8e-3✱ · `వ` 0.99 · `త` 0.57 · `ని` 0.06✱ · `␣ధ` 0.10 · `ార` 0.10 · `యే` 0.19 · `␣ని` 0.11 · `లి` 0.02✱ · `చిన` 0.52 · `ద` 0.73 · `ై` 0.98 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ల్లి` 0.96 · `␣ప్రేమ` 0.16 · `యే` 0.35 · `␣జగ` 0.24 · `తి` 0.86 · `కి` 0.75 · `␣త` 0.30 · `ల` 0.95 · `పు` 0.85 · `న` 0.96 · `␣ని` 0.22 · `లి` 0.24✱ · `చిన` 0.87 · `ద` 0.93 · `ృ` 6.2e-4✱ · `ఢ` 0.22✱ · `మ` 0.04✱ · `్` 3.1e-8✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 81 tokens · 27.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాతృ ప్రేమ జగతిలోన మధురమైనది సుమతిన్ | `UIUIIIIUIIIIUIIIIU` |
| 2 | మాతృ ప్రేమ చిత్తమున మమత నిలిచి నిలకడగా | `UIUIUIIIIIIIIIIIIIU` |
| 3 | మాతృ అనురతి జగతికిన మహతమ సొబగునదియే | `UIIIIIIIIIIIIIIIIIIIU` |
| 4 | మాతృ అనురతిని మరువక మమత ధారిని నిలపుం | `UIIIIIIIIIIIIIUIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 55% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.148 · model's first choice kept 51% · constraint overrode 32% · backtracks 21

<details><summary>Token probabilities (81 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.15 · `త` 0.97 · `ృ` 0.97 · `␣ప్రేమ` 0.17✱ · `␣జగ` 0.16 · `తి` 0.96 · `లో` 0.43 · `న` 0.58 · `␣మ` 0.44 · `ధు` 0.32 · `ర` 0.81 · `మైన` 0.33 · `ది` 0.70 · `␣సు` 4.9e-3✱ · `మ` 0.37✱ · `తి` 0.35 · `న్` 3.5e-3✱ · `⏎` 0.96 forced |
| 2 | `మా` 0.04 · `త` 0.74 · `ృ` 0.95 · `␣ప్రే` 7.9e-3 · `మ` 8.9e-3✱ · `␣చి` 3.3e-3 · `త్త` 0.42 · `ము` 0.40 · `న` 0.88 · `␣మ` 0.19 · `మ` 0.19 · `త` 0.76 · `␣ని` 0.23✱ · `లి` 0.05✱ · `చి` 0.10✱ · `␣ని` 0.20 · `ల` 0.27✱ · `క` 0.14 · `డ` 0.21 · `గా` 0.10✱ · `⏎` 0.32 forced |
| 3 | `మా` 0.77 · `త` 0.99 · `ృ` 0.98 · `␣అను` 0.29 · `ర` 0.01✱ · `తి` 0.93 · `␣జగ` 0.11 · `తి` 0.79 · `కి` 0.23✱ · `న` 0.26 · `␣మహ` 4.8e-3✱ · `త` 1.7e-3✱ · `మ` 0.05✱ · `␣సొ` 0.02✱ · `బ` 0.05✱ · `గు` 0.81 · `న` 0.28 · `ది` 0.02✱ · `యే` 4.3e-3✱ · `⏎` 0.99 forced |
| 4 | `మా` 0.96 · `త` 1.00 · `ృ` 0.99 · `␣అను` 0.12 · `ర` 7.1e-3✱ · `తి` 0.91 · `ని` 0.05 · `␣మ` 0.12 · `రు` 0.48 · `వ` 0.94 · `క` 0.13✱ · `␣మ` 0.33 · `మ` 0.38 · `త` 0.63 · `␣ధ` 0.04 · `ారి` 0.14✱ · `ని` 0.06 · `␣ని` 0.10✱ · `ల` 0.37 · `ప` 0.01 · `ు` 0.01✱ · `ం` 0.02✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 87 tokens · 29.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతికి దొర దైవమున సుమతిని కీ | `UIUIIIIIIIUIIIIIIIU` |
| 2 | తల్లి కరుణ జగతికి దొర ధైర్యమున నిరీక్షి కీ | `UIIIIIIIIIIUIIIIUIU` |
| 3 | తల్లి అనురతి జగతికి దొ ల్య్ల్తమున మధురమై కనబ్ | `UIIIIIIIIIIIIIIIIUIU` |
| 4 | తల్లి ఆశయము జగతికి దానమున దిగంతమై | `UIUIIIIIIIUIIIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.124 · model's first choice kept 66% · constraint overrode 25% · backtracks 30

<details><summary>Token probabilities (87 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.74 · `ల్లి` 0.79 · `␣ప్రేమ` 0.75 · `␣జగ` 0.30 · `తి` 0.95 · `కి` 0.51 · `␣ద` 0.05 · `ొ` 2.7e-3✱ · `ర` 0.43 · `␣ద` 4.1e-4✱ · `ై` 0.85 · `వ` 0.86 · `ము` 0.35 · `న` 0.27 · `␣సు` 2.6e-3✱ · `మ` 0.52 · `తి` 0.26 · `ని` 0.08✱ · `␣క` 3.6e-3✱ · `ీ` 0.25 · `⏎` 1.8e-4 forced |
| 2 | `త` 0.42 · `ల్లి` 0.78 · `␣క` 0.18 · `రుణ` 0.97 · `␣జగ` 0.08 · `తి` 0.69 · `కి` 0.78 · `␣ద` 0.20 · `ొ` 0.93 · `ర` 0.98 · `␣ధ` 0.14 · `ై` 0.70 · `ర్య` 0.94 · `ము` 0.79 · `న` 0.93 · `␣ని` 0.08 · `రీ` 0.07✱ · `క్ష` 0.57 · `ి` 0.27✱ · `␣క` 0.02✱ · `ీ` 1.00 · `⏎` 1.00 forced |
| 3 | `త` 0.91 · `ల్లి` 0.95 · `␣అను` 0.23 · `ర` 0.01✱ · `తి` 0.97 · `␣జగ` 0.89 · `తి` 1.00 · `కి` 0.98 · `␣ద` 1.00 · `ొ` 1.00 · `␣ల` 1.1e-6✱ · `్య` 1.4e-4✱ · `్` 5.8e-4✱ · `ల` 0.55 · `్` 3.4e-4✱ · `త` 5.1e-3✱ · `ము` 0.69 · `న` 0.98 · `␣మ` 0.05 · `ధు` 0.36 · `ర` 0.60 · `మై` 0.30 · `␣క` 0.32 · `న` 6.6e-5✱ · `బ` 0.13✱ · `్` 6.2e-8✱ · `⏎` 4.7e-3 forced |
| 4 | `త` 0.99 · `ల్లి` 0.97 · `␣ఆ` 0.29 · `శ` 0.82 · `య` 0.06✱ · `ము` 0.41 · `␣జగ` 0.98 · `తి` 1.00 · `కి` 0.97 · `␣ద` 0.99 · `ాన` 9.5e-5✱ · `ము` 0.45 · `న` 0.99 · `␣ది` 0.01✱ · `గ` 1.5e-3✱ · `ంత` 0.41 · `మై` 0.52 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 81 tokens · 5.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమయే జగతికి తలపున వెలుగునిదురే | `UIUIUIIIIIIIIIIIIIU` |
| 2 | తల్లి కరుణయే జగతికి క్వ్వ్తమున నిలవదురునిరే | `UIIIIUIIIIIIIIIIIIIU` |
| 3 | తల్లి ఆశయము జగతికి జ్య్వ్తమున జ్యోతినిదుకునే | `UIUIIIIIIIIIIUIIIIU` |
| 4 | తల్లి దీవెన జగతికి దిధమున దైవమై నిలే | `UIUIIIIIIIIIIUIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 52% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.111 · model's first choice kept 65% · constraint overrode 26% · backtracks 0

<details><summary>Token probabilities (81 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.74 · `ల్లి` 0.79 · `␣ప్రేమ` 0.75 · `యే` 0.23 · `␣జగ` 0.63 · `తి` 0.94 · `కి` 0.78 · `␣త` 0.03✱ · `ల` 0.81 · `పు` 0.74 · `న` 0.10 · `␣వె` 0.08 · `లుగు` 0.79 · `ని` 0.21✱ · `దు` 5.4e-3✱ · `రే` 0.16 · `⏎` 0.93 forced |
| 2 | `త` 0.36 · `ల్లి` 0.70 · `␣క` 0.23 · `రుణ` 0.95 · `యే` 0.68 · `␣జగ` 0.27✱ · `తి` 0.88 · `కి` 0.89 · `␣క` 0.50 · `్వ` 3.3e-6✱ · `్వ` 1.7e-6✱ · `్` 3.0e-5✱ · `త` 0.08✱ · `ము` 0.34 · `న` 0.65 · `␣ని` 0.18 · `ల` 0.23 · `వ` 0.39 · `దు` 0.40 · `రు` 0.02✱ · `ని` 2.6e-3✱ · `రే` 0.17✱ · `⏎` 1.00 forced |
| 3 | `త` 0.95 · `ల్లి` 0.95 · `␣ఆ` 0.42 · `శ` 0.90 · `య` 0.01✱ · `ము` 0.06✱ · `␣జగ` 0.43 · `తి` 0.91 · `కి` 0.81 · `␣జ` 5.6e-3✱ · `్య` 0.77 · `్వ` 1.4e-6✱ · `్` 4.8e-7✱ · `త` 0.59 · `ము` 0.91 · `న` 0.97 · `␣జ` 0.66 · `్య` 0.33 · `ోతి` 0.63 · `ని` 0.45 · `దు` 0.93 · `కునే` 8.2e-6✱ · `⏎` 0.99 forced |
| 4 | `త` 1.00 · `ల్లి` 0.98 · `␣దీ` 0.17 · `వె` 0.95 · `న` 0.99 · `␣జగ` 0.06✱ · `తి` 1.00 · `కి` 0.96 · `␣ది` 0.15 · `ధ` 2.9e-5✱ · `ము` 0.06✱ · `న` 1.00 · `␣ద` 0.44 · `ై` 0.91 · `వ` 0.98 · `మై` 0.24 · `␣ని` 0.81 · `లే` 6.7e-4 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 81 tokens · 6.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతిలోన తలపులకి మరువదుగా | `UIUIIIIUIIIIIIIIIIU` |
| 2 | తల్లి కరుణ నిత్యము మనదై నిలవదుగా జగత్ | `UIIIIUIIIIUIIIIUIU` |
| 3 | తల్లి అనురతి జగతికిన మ్ర్వ్తై నిలవదుగా కదా | `UIIIIIIIIIIUIIIIUIU` |
| 4 | తల్లి దీవెన జగతికిన స్ర్వ్తై నిలవదుగా నరీ | `UIUIIIIIIIUIIIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 43% · single-akshara words 9% · repeated lines 0 · mean token probability (geometric) 0.144 · model's first choice kept 64% · constraint overrode 23% · backtracks 0

<details><summary>Token probabilities (81 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.74 · `ల్లి` 0.79 · `␣ప్రేమ` 0.75 · `␣జగ` 0.30 · `తి` 0.95 · `లో` 0.31 · `న` 0.70 · `␣త` 0.14✱ · `ల` 0.84 · `పు` 0.35 · `ల` 0.37 · `కి` 0.05 · `␣మ` 0.06✱ · `రు` 0.26 · `వ` 0.93 · `దు` 0.45 · `గా` 0.11✱ · `⏎` 0.90 forced |
| 2 | `త` 0.55 · `ల్లి` 0.69 · `␣క` 0.20 · `రుణ` 0.96 · `␣ని` 0.03✱ · `త్య` 0.68 · `ము` 0.53 · `␣మన` 0.07 · `ద` 2.0e-4✱ · `ై` 0.87 · `␣ని` 0.35 · `ల` 0.20 · `వ` 0.48 · `దు` 0.80 · `గా` 0.91 · `␣జగ` 1.8e-4✱ · `త్` 2.2e-4✱ · `⏎` 0.21 forced |
| 3 | `త` 0.90 · `ల్లి` 0.91 · `␣అను` 0.09 · `ర` 9.3e-3✱ · `తి` 0.96 · `␣జగ` 0.04✱ · `తి` 0.61 · `కి` 0.33✱ · `న` 0.13 · `␣మ` 0.02✱ · `్ర` 3.2e-5✱ · `్వ` 4.3e-7✱ · `్` 2.5e-4✱ · `త` 0.08✱ · `ై` 0.07 · `␣ని` 0.19 · `ల` 0.33 · `వ` 0.88 · `దు` 0.94 · `గా` 0.97 · `␣క` 0.03✱ · `దా` 0.13 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ల్లి` 0.96 · `␣దీ` 0.20 · `వె` 0.97 · `న` 0.99 · `␣జగ` 0.10 · `తి` 0.90 · `కి` 0.55 · `న` 0.78 · `␣స` 0.03 · `్ర` 5.5e-4✱ · `్వ` 5.0e-3✱ · `్` 0.44 · `త` 0.92 · `ై` 0.98 · `␣ని` 0.83 · `ల` 0.92 · `వ` 1.00 · `దు` 0.99 · `గా` 1.00 · `␣న` 0.03 · `రీ` 0.06 |

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

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 158 tokens · 28.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ అమృతమ్య్ర్దరమున్ జగతికి దైవముగానైరి ఝ్వ్వ్ధనమున్ కరుణిని | `UIUIIIUIIUIIIIUIIUUIIIUIIII` |
| 2 | తల్లి మమత జగమ్య్ర్దరమున్ శిరస్సు తలమున నిలిచితి స్ర్వ్తముని తండ్రిని న | `UIIIIIUIIUIUIIIIIIIIIIIIUIII` |
| 3 | తల్లి అనురతి మమ్య్ర్దరమున్ గురుత్వ మ్ర్దరమున్ నిలిచితి రస్య్న్ధనమున్ వనమున | `UIIIIIUIIUIUIIIUIIIIUIIUIIII` |
| 4 | తల్లి ఆశీస్సుల మ్య్ర్దరమున్ జగతికి దైవత్వమున నిలిచ్య్న్ధనమున్ తలమున | `UIUUIIIIUIIIIUUIIIIUIIUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 39% · single-akshara words 3% · repeated lines 0 · mean token probability (geometric) 0.110 · model's first choice kept 52% · constraint overrode 34% · backtracks 0

<details><summary>Token probabilities (158 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.65 · `ల్లి` 0.80 · `␣ప్రేమ` 0.73 · `␣అమ` 0.11 · `ృత` 0.73 · `మ` 0.20✱ · `్య` 4.1e-5✱ · `్ర` 1.1e-4✱ · `్` 3.8e-6✱ · `ద` 0.02✱ · `ర` 0.03 · `ము` 0.47 · `న్` 0.03 · `␣జగ` 0.03✱ · `తి` 0.90 · `కి` 0.27✱ · `␣ద` 0.03✱ · `ై` 0.95 · `వ` 0.92 · `ము` 0.68 · `గా` 0.08✱ · `న` 0.13✱ · `ై` 0.29✱ · `రి` 2.8e-3✱ · `␣` 2.0e-4✱ · `ఝ` 0.13✱ · `్వ` 3.2e-3✱ · `్వ` 1.9e-4✱ · `్` 1.6e-3✱ · `ధ` 0.02✱ · `న` 0.04✱ · `ము` 0.64 · `న్` 0.13✱ · `␣క` 2.6e-3✱ · `రుణ` 0.35 · `ి` 4.4e-3✱ · `ని` 0.23 · `⏎` 0.01 forced |
| 2 | `త` 0.41 · `ల్లి` 0.79 · `␣మ` 0.06 · `మ` 0.94 · `త` 0.88 · `␣జగ` 0.02 · `మ` 0.08✱ · `్య` 9.3e-6✱ · `్ర` 0.03✱ · `్` 0.76 · `ద` 0.83 · `ర` 0.97 · `ము` 0.79 · `న్` 0.97 · `␣శి` 0.09✱ · `ర` 0.40 · `స్సు` 0.58 · `␣త` 3.3e-4✱ · `ల` 0.88 · `ము` 0.34 · `న` 0.50 · `␣ని` 0.56 · `లి` 0.59 · `చి` 0.29 · `తి` 0.20 · `␣స` 0.03✱ · `్ర` 1.2e-4✱ · `్వ` 1.0e-6✱ · `్` 8.0e-3✱ · `త` 0.18 · `ము` 0.37 · `ని` 0.11✱ · `␣త` 2.2e-3✱ · `ండ` 0.09 · `్రి` 0.68 · `ని` 0.16✱ · `␣న` 5.4e-4✱ · `⏎` 1.6e-4 forced |
| 3 | `త` 0.86 · `ల్లి` 0.93 · `␣అను` 0.15 · `ర` 0.02✱ · `తి` 0.94 · `␣మ` 0.04 · `మ` 0.35✱ · `్య` 0.14✱ · `్ర` 0.86 · `్` 0.99 · `ద` 0.99 · `ర` 1.00 · `ము` 0.99 · `న్` 1.00 · `␣గు` 0.01 · `రు` 0.03✱ · `త్వ` 0.28 · `␣మ` 1.3e-3✱ · `్ర` 1.6e-3✱ · `్` 0.63 · `ద` 0.91 · `ర` 0.98 · `ము` 0.93 · `న్` 0.78 · `␣ని` 0.07 · `లి` 0.04✱ · `చి` 0.57 · `తి` 0.96 · `␣ర` 0.01 · `స` 0.06 · `్య` 7.8e-3✱ · `్` 0.09✱ · `న` 0.20 · `్` 2.8e-6✱ · `ధ` 0.21✱ · `న` 0.88 · `ము` 0.95 · `న్` 0.73 · `␣వ` 0.01✱ · `న` 0.13 · `ము` 0.44 · `న` 0.21 · `⏎` 0.93 forced |
| 4 | `త` 0.99 · `ల్లి` 0.96 · `␣ఆ` 0.19 · `శ` 0.85 · `ీ` 0.77 · `స్సు` 0.28 · `ల` 0.16 · `␣మ` 0.23✱ · `్య` 0.17✱ · `్ర` 0.97 · `్` 1.00 · `ద` 1.00 · `ర` 1.00 · `ము` 1.00 · `న్` 1.00 · `␣జగ` 0.12 · `తి` 0.80 · `కి` 0.62 · `␣ద` 0.09 · `ై` 0.75 · `వ` 0.97 · `త్వ` 0.17 · `ము` 0.76 · `న` 0.18 · `␣ని` 0.41 · `లి` 0.74 · `చ` 9.0e-3✱ · `్య` 1.6e-3✱ · `్` 0.53 · `న` 0.53 · `్` 0.42 · `ధ` 0.84 · `న` 0.96 · `ము` 1.00 · `న్` 0.99 · `␣త` 0.03 · `ల` 0.28✱ · `ము` 0.88 · `న` 0.94 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 143 tokens · 27.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతిక్ర్య్త సదా నిలచి నిదానమై తేలియెన్తమునందునుమున | `UIUIIIUIIUIIIIUIUUIUIIUIIII` |
| 2 | తల్లి కరుణ మదిగ్య్న్త సదా రగిలి నిదానమై తేలియెన్తమునందునుమున | `UIIIIIUIIUIIIIUIUUIUIIUIIII` |
| 3 | తల్లి ఆశీర్వాద్ధ్త స్ర్వ్త నిలచి నిదనతై తేలియెన్తమున్య్న్తమునందునుమున | `UIUUUIIIIIIIIUUIUIUIIUIIII` |
| 4 | తల్లి దయ జగతిక్ర్య్త సదా నిలచి నిదానమై తేలియెన్తమునందునుమున | `UIIIIIUIIUIIIIUIUUIUIIUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 37% · single-akshara words 4% · repeated lines 0 · mean token probability (geometric) 0.128 · model's first choice kept 71% · constraint overrode 24% · backtracks 0

<details><summary>Token probabilities (143 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.65 · `ల్లి` 0.80 · `␣ప్రేమ` 0.73 · `␣జగ` 0.26 · `తి` 0.96 · `క` 0.03✱ · `్ర` 1.4e-10✱ · `్య` 2.5e-7✱ · `్` 5.2e-6✱ · `త` 3.4e-3✱ · `␣స` 0.03 · `దా` 0.02✱ · `␣ని` 0.26 · `ల` 0.13 · `చి` 0.11 · `␣ని` 0.26 · `ద` 3.9e-4✱ · `ాన` 0.12 · `మై` 0.12 · `␣తే` 8.0e-4✱ · `లి` 0.22 · `య` 0.40 · `ె` 0.74 · `న్` 0.01✱ · `త` 2.5e-4✱ · `ము` 0.01✱ · `న` 0.02✱ · `ందు` 0.02✱ · `ను` 0.02✱ · `ము` 1.3e-3✱ · `న` 0.04✱ · `⏎` 0.78 forced |
| 2 | `త` 0.26 · `ల్లి` 0.78 · `␣క` 0.30 · `రుణ` 0.97 · `␣మ` 8.2e-3✱ · `ది` 0.47 · `గ` 6.5e-4✱ · `్య` 9.6e-3✱ · `్` 3.0e-3✱ · `న` 0.44 · `్` 1.7e-4✱ · `త` 0.10✱ · `␣స` 0.09 · `దా` 0.56 · `␣ర` 0.06 · `గి` 0.10✱ · `లి` 0.51 · `␣ని` 0.52 · `ద` 8.1e-3✱ · `ాన` 0.96 · `మై` 0.92 · `␣తే` 0.62 · `లి` 0.97 · `య` 0.99 · `ె` 1.00 · `న్` 0.99 · `త` 0.99 · `ము` 1.00 · `న` 0.99 · `ందు` 1.00 · `ను` 0.96 · `ము` 0.98 · `న` 1.00 · `⏎` 1.00 forced |
| 3 | `త` 0.93 · `ల్లి` 0.95 · `␣ఆ` 0.46 · `శ` 0.84 · `ీ` 0.67 · `ర్` 0.54 · `వా` 0.68 · `ద` 0.79 · `్` 5.1e-3✱ · `ధ` 0.18 · `్` 0.60 · `త` 0.80 · `␣స` 0.82 · `్ర` 2.4e-6✱ · `్వ` 1.4e-6✱ · `్` 0.61 · `త` 0.93 · `␣ని` 0.39 · `ల` 0.71 · `చి` 0.89 · `␣ని` 0.86 · `ద` 0.98 · `న` 7.3e-7✱ · `త` 5.0e-4✱ · `ై` 0.30 · `␣తే` 0.86 · `లి` 0.99 · `య` 1.00 · `ె` 1.00 · `న్` 1.00 · `త` 1.00 · `ము` 1.00 · `న` 0.99 · `్య` 2.4e-8✱ · `్` 0.06✱ · `న` 0.86 · `్` 9.1e-3✱ · `త` 0.86 · `ము` 0.89 · `న` 0.97 · `ందు` 0.94 · `ను` 0.87 · `ము` 0.86 · `న` 0.98 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ల్లి` 0.97 · `␣ద` 0.07 · `య` 0.69 · `␣జగ` 0.06✱ · `తి` 0.81 · `క` 0.46 · `్ర` 0.64 · `్య` 0.89 · `్` 0.96 · `త` 0.95 · `␣స` 0.89 · `దా` 0.96 · `␣ని` 0.34 · `ల` 0.70 · `చి` 0.93 · `␣ని` 0.97 · `ద` 0.95 · `ాన` 0.95 · `మై` 0.83 · `␣తే` 0.96 · `లి` 0.99 · `య` 0.99 · `ె` 1.00 · `న్` 1.00 · `త` 1.00 · `ము` 1.00 · `న` 0.98 · `ందు` 0.99 · `ను` 0.96 · `ము` 0.95 · `న` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 138 tokens · 43.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగమంతటికీ మధురమృతంబుగానై యుండెదానాణెదెనుము | `UIUIIIUIIUIIIIUIUUUIUUIIII` |
| 2 | తల్లి అనురతి లోక్ర్వ్తమమై నిలిచెను స్ర్వ్తమమై నిలిచెను తండ్ర్య్తముమునేనోడు | `UIIIIIUIIUIIIIIIUIIIIUIIIUUI` |
| 3 | తల్లి కరుణ నిత్యతరముగా తేజొదరినదై యుండెను హ్ర్య్తముగాననితెను | `UIIIIUIIIIUUIIIIUUIIIIUIIII` |
| 4 | తల్లి దీవెన జగమ్ర్మ్తముగా నిలుచును స్ర్వ్తముగా నిలుచును హృదయమునేనోడు | `UIUIIIUIIUIIIIIIUIIIIIIIIUUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 48% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.067 · model's first choice kept 47% · constraint overrode 39% · backtracks 30

<details><summary>Token probabilities (138 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.65 · `ల్లి` 0.80 · `␣ప్రేమ` 0.75 · `␣జగ` 0.25✱ · `మ` 0.02 · `ంత` 0.94 · `టి` 0.76 · `కీ` 0.60 · `␣మ` 0.18 · `ధు` 0.03✱ · `ర` 0.66 · `మ` 0.10✱ · `ృ` 9.1e-3✱ · `తం` 0.36 · `బు` 0.06✱ · `గా` 0.09✱ · `న` 0.09✱ · `ై` 0.08✱ · `␣యు` 4.9e-3✱ · `ండె` 0.38 · `ద` 1.2e-3✱ · `ాన` 0.03✱ · `ా` 1.00 · `ణ` 1.7e-4✱ · `ె` 0.05✱ · `ద` 0.01✱ · `ె` 0.27 · `ను` 0.08✱ · `ము` 4.6e-3✱ · `⏎` 0.78 forced |
| 2 | `త` 0.37 · `ల్లి` 0.79 · `␣అను` 0.04 · `ర` 0.01✱ · `తి` 0.94 · `␣లో` 0.06 · `క` 0.97 · `్ర` 1.8e-7✱ · `్వ` 2.3e-6✱ · `్` 2.7e-8✱ · `త` 0.05✱ · `మ` 0.08 · `మై` 0.23 · `␣ని` 0.48 · `లి` 0.20✱ · `చె` 0.60 · `ను` 0.54 · `␣స` 0.04✱ · `్ర` 1.3e-4✱ · `్వ` 1.1e-7✱ · `్` 3.3e-3✱ · `త` 0.72 · `మ` 0.26 · `మై` 0.07 · `␣ని` 0.18 · `లి` 0.22✱ · `చె` 0.90 · `ను` 0.69 · `␣త` 0.05 · `ండ` 0.32 · `్ర` 0.14✱ · `్య` 6.8e-3✱ · `్` 1.7e-4✱ · `త` 0.08✱ · `ము` 0.38 · `ము` 6.0e-3✱ · `నే` 2.7e-5✱ · `నో` 1.4e-3✱ · `డు` 1.1e-3✱ · `⏎` 0.97 forced |
| 3 | `త` 0.90 · `ల్లి` 0.92 · `␣క` 0.46 · `రుణ` 0.96 · `␣ని` 0.02✱ · `త్య` 0.59 · `తర` 7.1e-3✱ · `ము` 0.28 · `గా` 0.63 · `␣తే` 0.03 · `జ` 0.87 · `ొ` 4.2e-3✱ · `ద` 3.2e-3✱ · `రి` 0.14✱ · `న` 0.26 · `ద` 0.04 · `ై` 0.12 · `␣యు` 0.06 · `ండె` 0.45 · `ను` 0.31 · `␣హ` 0.02✱ · `్ర` 8.9e-5✱ · `్య` 3.1e-5✱ · `్` 0.17✱ · `త` 0.36 · `ము` 0.51 · `గా` 0.11 · `న` 0.36 · `ని` 2.0e-3✱ · `తె` 0.02✱ · `ను` 0.19 · `⏎` 0.16 forced |
| 4 | `త` 0.98 · `ల్లి` 0.95 · `␣దీ` 0.26 · `వె` 0.96 · `న` 1.00 · `␣జగ` 0.24 · `మ` 0.16✱ · `్ర` 3.9e-5✱ · `్` 0.01✱ · `మ` 0.11 · `్` 3.0e-3✱ · `త` 0.40 · `ము` 0.25✱ · `గా` 0.70 · `␣ని` 0.30 · `లు` 0.12 · `చు` 0.41 · `ను` 0.81 · `␣స` 0.14 · `్ర` 0.12✱ · `్వ` 0.75 · `్` 0.98 · `త` 0.98 · `ము` 0.54 · `గా` 0.87 · `␣ని` 0.48 · `లు` 0.58 · `చు` 0.90 · `ను` 0.99 · `␣హ` 0.06 · `ృ` 0.76 · `దయ` 0.71 · `ము` 0.63 · `నే` 0.23 · `నో` 0.55 · `డు` 0.92 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 128 tokens · 38.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | గమ్యము చేరి దిగన్నాక లంక గంటల వెలిగేను గానమునందు | `UIIUIIUUIUIUIIIIUIUIIUI` |
| 2 | భూమ్యల పరిచయము తెలిసి మారుమూర్తి తేజమున సాగ్య్ర్వును గానమునదు | `UIIIIIIIIIIUIUIUIIIUIIUIIII` |
| 3 | సమ్యల సాగరమ్ర్య్జనము దాటి లభె సాగతి విక్రమించను గానమునదు | `UIIUIUIIIUIIIUIIUIUIIUIIII` |
| 4 | గమ్యమున నిలిచి ధ్వ్వ్కమున భక్తి నిలుగను ధైర్యమున సాగ్య్ర్వుగానమునదు ఱ | `UIIIIIIIIIUIIIIIUIIIUIUIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 28% · single-akshara words 3% · repeated lines 0 · mean token probability (geometric) 0.055 · model's first choice kept 44% · constraint overrode 32% · backtracks 30

<details><summary>Token probabilities (128 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `గ` 0.08 · `మ` 0.59 · `్య` 0.24 · `ము` 0.86 · `␣చే` 0.48 · `రి` 0.56 · `␣ది` 6.8e-3 · `గ` 0.10 · `న్నా` 1.2e-3✱ · `క` 0.05 · `␣ల` 0.16 · `ంక` 0.68 · `␣గ` 0.02✱ · `ంట` 5.9e-3 · `ల` 0.31 · `␣వె` 5.8e-3 · `లి` 0.21 · `గే` 0.21 · `ను` 0.42 · `␣గా` 6.2e-3✱ · `న` 0.63 · `ము` 0.87 · `న` 0.10✱ · `ందు` 0.01✱ · `⏎` 0.86 forced |
| 2 | `భ` 0.08 · `ూ` 0.26 · `మ` 0.14✱ · `్య` 0.42 · `ల` 0.11 · `␣పరి` 0.02 · `చ` 0.08 · `య` 0.35 · `ము` 0.79 · `␣తెలిసి` 0.04✱ · `␣మ` 0.05 · `ారు` 0.26 · `మ` 0.03✱ · `ూర్` 3.5e-3✱ · `తి` 0.96 · `␣తే` 0.15 · `జ` 0.92 · `ము` 0.67 · `న` 0.25 · `␣సా` 0.06 · `గ` 0.22✱ · `్య` 2.2e-3✱ · `్ర` 2.7e-6✱ · `్వ` 3.6e-4✱ · `ు` 1.6e-3✱ · `ను` 0.12✱ · `␣గా` 9.2e-3✱ · `న` 0.82 · `ము` 0.98 · `న` 0.93 · `దు` 7.4e-5✱ · `⏎` 1.00 forced |
| 3 | `స` 0.45 · `మ` 0.01✱ · `్య` 1.3e-3✱ · `ల` 0.17 · `␣సా` 0.09 · `గర` 0.52 · `మ` 0.07✱ · `్ర` 2.4e-4✱ · `్య` 3.8e-5✱ · `్` 2.0e-4✱ · `జ` 3.3e-3✱ · `న` 0.22 · `ము` 0.59 · `␣దా` 0.63 · `టి` 0.79 · `␣ల` 0.16 · `భ` 1.1e-3✱ · `ె` 1.8e-3✱ · `␣సా` 5.0e-4✱ · `గ` 0.24 · `తి` 0.03 · `␣వి` 0.04 · `క్ర` 0.50 · `మ` 0.58 · `ించ` 0.04✱ · `ను` 5.7e-3✱ · `␣గా` 0.77 · `న` 0.98 · `ము` 0.98 · `న` 0.92 · `దు` 0.30✱ · `⏎` 1.00 forced |
| 4 | `గ` 0.03 · `మ` 0.89 · `్య` 0.92 · `ము` 0.63 · `న` 0.05 · `␣ని` 0.17 · `లి` 0.74 · `చి` 0.64 · `␣ధ` 0.07✱ · `్వ` 9.0e-4✱ · `్వ` 2.1e-7✱ · `్` 1.1e-7✱ · `క` 4.5e-4✱ · `ము` 0.23 · `న` 0.35 · `␣భ` 0.08 · `క్తి` 0.11 · `␣ని` 0.05 · `లు` 0.20 · `గ` 7.1e-3✱ · `ను` 0.04✱ · `␣ధ` 0.02 · `ై` 0.63 · `ర్య` 0.92 · `ము` 0.88 · `న` 0.79 · `␣సా` 0.43 · `గ` 0.67 · `్య` 0.79 · `్ర` 0.86 · `్వ` 0.97 · `ు` 0.98 · `గా` 8.1e-5✱ · `న` 0.97 · `ము` 0.99 · `న` 0.95 · `దు` 0.90 · `␣` 8.4e-6✱ · `ఱ` 2.7e-5✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 141 tokens · 29.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ అమృతమ్య్ర్దంబం సుమతము న్య్య్ధనము తలమున భర్య్య్ధనము నమస్క | `UIUIIIUUUIIIIIIIIIIIUIIIIUI` |
| 2 | తల్లి కరుణ అనంతమ్య్ర్దంబమై నిధనము తలమున భర్య్య్ధనము నమస్క | `UIIIIIUUUIUIIIIIIIIUIIIIUI` |
| 3 | తల్లి దీవెన జగమ్య్ర్దంబమై నిధనత తలమున భరస్య్య్ధధనము నమస్క | `UIUIIIUUIUIIIIIIIIIUIIIIIUI` |
| 4 | తల్లి ఆశీర్వాద మ్య్ర్దంబమై నిధనత తలమున భరస్య్య్ధధనము నమస్క | `UIUUUIUIUIIIIIIIIIUIIIIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 38% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.235 · model's first choice kept 74% · constraint overrode 21% · backtracks 0

<details><summary>Token probabilities (141 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.65 · `ల్లి` 0.80 · `␣ప్రేమ` 0.73 · `␣అమ` 0.11 · `ృత` 0.73 · `మ` 0.20✱ · `్య` 4.1e-5✱ · `్ర` 1.1e-4✱ · `్` 3.8e-6✱ · `ద` 0.02✱ · `ంబ` 0.03 · `ం` 0.34 · `␣సు` 0.06 · `మ` 0.45 · `త` 0.11✱ · `ము` 0.06✱ · `␣న` 9.0e-3✱ · `్య` 1.6e-4✱ · `్య` 3.9e-3✱ · `్` 6.5e-3✱ · `ధ` 0.05✱ · `న` 0.23 · `ము` 0.52 · `␣త` 2.7e-3✱ · `ల` 0.49 · `ము` 0.57 · `న` 0.27✱ · `␣భ` 0.02✱ · `ర` 0.09✱ · `్య` 6.8e-5✱ · `్య` 0.04✱ · `్` 0.34 · `ధ` 0.46 · `న` 0.83 · `ము` 0.94 · `␣న` 3.4e-3✱ · `మ` 0.20 · `స్క` 0.60 · `⏎` 3.2e-5 forced |
| 2 | `త` 0.54 · `ల్లి` 0.87 · `␣క` 0.31 · `రుణ` 0.97 · `␣అన` 0.01✱ · `ంత` 0.99 · `మ` 0.64 · `్య` 0.85 · `్ర` 0.89 · `్` 0.96 · `ద` 0.84 · `ంబ` 0.98 · `మై` 1.9e-3✱ · `␣ని` 0.12 · `ధ` 3.0e-3✱ · `న` 0.76 · `ము` 0.92 · `␣త` 0.35 · `ల` 0.93 · `ము` 0.85 · `న` 0.97 · `␣భ` 0.28 · `ర` 0.96 · `్య` 0.98 · `్య` 0.99 · `్` 0.98 · `ధ` 0.99 · `న` 0.99 · `ము` 0.80 · `␣న` 0.43 · `మ` 0.99 · `స్క` 0.99 · `⏎` 0.98 forced |
| 3 | `త` 0.90 · `ల్లి` 0.94 · `␣దీ` 0.25 · `వె` 0.96 · `న` 1.00 · `␣జగ` 0.13 · `మ` 0.09✱ · `్య` 0.06✱ · `్ర` 0.94 · `్` 0.99 · `ద` 0.93 · `ంబ` 1.00 · `మై` 0.68 · `␣ని` 0.49 · `ధ` 0.97 · `న` 1.00 · `త` 6.1e-6✱ · `␣త` 0.30 · `ల` 1.00 · `ము` 0.98 · `న` 1.00 · `␣భ` 0.99 · `ర` 1.00 · `స్య` 2.3e-4✱ · `్య` 0.77 · `్` 0.81 · `ధ` 0.99 · `ధ` 1.1e-5✱ · `న` 0.96 · `ము` 0.99 · `␣న` 0.99 · `మ` 1.00 · `స్క` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.97 · `ల్లి` 0.97 · `␣ఆ` 0.32 · `శ` 0.96 · `ీ` 0.94 · `ర్` 0.57 · `వా` 0.78 · `ద` 0.94 · `␣మ` 0.01✱ · `్య` 0.84 · `్ర` 0.99 · `్` 0.99 · `ద` 0.99 · `ంబ` 1.00 · `మై` 0.77 · `␣ని` 0.89 · `ధ` 0.97 · `న` 0.98 · `త` 0.15✱ · `␣త` 1.00 · `ల` 1.00 · `ము` 0.98 · `న` 1.00 · `␣భ` 0.99 · `ర` 0.99 · `స్య` 0.84 · `్య` 0.96 · `్` 0.97 · `ధ` 0.99 · `ధ` 0.87 · `న` 1.00 · `ము` 1.00 · `␣న` 1.00 · `మ` 1.00 · `స్క` 1.00 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 144 tokens · 24.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వాయుపుత్రుడు సాగె స్ర్వాసము దాటి ల్వంకగ చేరెను వాడు వేగించ | `UIUIIUIUIIUIUIIUIIUIUUI` |
| 2 | గీయాళమున చేరి ల్వ్క్యేన పారించి స్ర్వ్గీతముల వినెను హ్ర్య్ఘీతమునందు | `UUIIIUIUIUUIUIIIIIIUIIUI` |
| 3 | భూయమున నిలిచి భుజమున భుజగ గ్ణ్య్వొన గమ్యమున దేవుమున సాగెను తల | `UIIIIIIIIIIIIIIIUIIIUIIIUIIII` |
| 4 | ప్రాయంకమున ప్రాణ బలముతో పారవచి ల్వ్క్యేన లీలలు క్వలమున చేసి | `UUIIIUIIIIUUIIIUIUIIIIIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 31% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.051 · model's first choice kept 45% · constraint overrode 35% · backtracks 0

<details><summary>Token probabilities (144 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.41 · `ాయ` 1.00 · `ు` 1.00 · `పు` 0.57 · `త్ర` 0.91 · `ుడు` 0.32 · `␣సా` 0.34 · `గ` 0.45 · `ె` 0.95 · `␣స` 0.06✱ · `్ర` 4.6e-6✱ · `్వ` 5.0e-8✱ · `ా` 0.10✱ · `స` 0.78 · `ము` 0.61 · `␣దా` 0.38 · `టి` 0.82 · `␣ల` 0.51 · `్వ` 7.2e-7✱ · `ంక` 0.38 · `గ` 0.06 · `␣చే` 0.10 · `రె` 0.92 · `ను` 0.96 · `␣వ` 8.3e-4✱ · `ాడు` 0.15 · `␣వే` 1.4e-3✱ · `గ` 0.85 · `ించ` 1.2e-3 · `⏎` 7.9e-4 forced |
| 2 | `గ` 0.13 · `ీ` 8.8e-3✱ · `యా` 1.9e-7✱ · `ళ` 0.03 · `ము` 0.15 · `న` 0.20✱ · `␣చే` 0.04 · `రి` 0.57 · `␣ల` 0.01✱ · `్వ` 0.04✱ · `్` 1.3e-6✱ · `క` 0.09✱ · `్య` 1.9e-3✱ · `ే` 0.02✱ · `న` 0.26 · `␣ప` 0.02 · `ార` 0.08 · `ించి` 0.07 · `␣స` 0.04 · `్ర` 1.6e-3✱ · `్వ` 0.44 · `్` 1.5e-3✱ · `గ` 7.5e-3✱ · `ీ` 4.9e-3✱ · `త` 0.69 · `ముల` 0.04 · `␣వి` 0.19 · `న` 0.68 · `ె` 0.20 · `ను` 0.92 · `␣హ` 0.08 · `్ర` 9.5e-5✱ · `్య` 5.4e-6✱ · `్` 2.5e-4✱ · `ఘ` 0.02✱ · `ీ` 0.02✱ · `త` 0.61 · `ము` 0.27✱ · `న` 0.24✱ · `ందు` 1.2e-3✱ · `⏎` 0.83 forced |
| 3 | `భ` 0.09✱ · `ూ` 0.41 · `య` 1.9e-4✱ · `ము` 0.43 · `న` 0.73 · `␣ని` 0.05✱ · `లి` 0.80 · `చి` 0.69 · `␣భ` 0.26 · `ు` 0.10✱ · `జ` 0.77 · `ము` 0.51 · `న` 0.47 · `␣భ` 0.16 · `ు` 0.30✱ · `జ` 0.73 · `గ` 0.05 · `␣గ` 0.03✱ · `్` 1.6e-6✱ · `ణ` 0.23 · `్య` 0.09✱ · `్` 4.8e-3✱ · `వ` 6.7e-3✱ · `ొ` 1.4e-3✱ · `న` 0.13 · `␣గ` 0.03 · `మ` 0.21 · `్య` 0.53 · `ము` 0.81 · `న` 0.52 · `␣ద` 0.03 · `ే` 0.30 · `వు` 0.45 · `ము` 4.8e-5✱ · `న` 0.39 · `␣సా` 0.04 · `గ` 0.74 · `ె` 0.96 · `ను` 0.94 · `␣త` 0.05✱ · `ల` 0.05 · `⏎` 0.06 forced |
| 4 | `ప` 0.04✱ · `్రా` 0.17✱ · `యం` 2.3e-6✱ · `క` 0.94 · `ము` 0.63 · `న` 0.80 · `␣ప్రా` 0.05 · `ణ` 0.47 · `␣బల` 2.5e-4✱ · `ము` 0.94 · `తో` 0.25 · `␣ప` 0.43 · `ార` 0.41 · `వ` 1.1e-3✱ · `చి` 0.08✱ · `␣ల` 0.66 · `్వ` 0.48 · `్` 0.59 · `క` 0.87 · `్య` 0.68 · `ే` 0.82 · `న` 0.76 · `␣ల` 0.24 · `ీల` 0.08 · `లు` 0.44 · `␣క` 0.04✱ · `్వ` 5.8e-5✱ · `ల` 0.09 · `ము` 0.14✱ · `న` 0.91 · `␣చేసి` 0.04 |

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

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 27 tokens · 4.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతిక్ర్య్త మధుర గాన | `UIUIIIUIIIIUI` |
| 2 | తల్లి కరుణ అమృత ధరణిలోన | `UIIIIIIIIIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 78% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.031 · model's first choice kept 48% · constraint overrode 35% · backtracks 0

<details><summary>Token probabilities (27 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.78 · `ల్లి` 0.81 · `␣ప్రేమ` 0.85 · `␣జగ` 0.16✱ · `తి` 0.94 · `క` 0.02✱ · `్ర` 4.4e-11✱ · `్య` 2.2e-7✱ · `్` 1.2e-5✱ · `త` 4.1e-3✱ · `␣మ` 0.02 · `ధు` 0.72 · `ర` 0.82 · `␣గా` 0.05 · `న` 0.48 · `⏎` 1.5e-4 forced |
| 2 | `త` 0.43 · `ల్లి` 0.74 · `␣క` 0.10 · `రుణ` 0.97 · `␣అమ` 0.03✱ · `ృత` 0.76 · `␣ధ` 0.13✱ · `రణ` 1.9e-3✱ · `ి` 0.52 · `లో` 0.09 · `న` 0.45 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 31 tokens · 5.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ అమృతధార నిత్య స్రవ | `UIUIIIIUIUIII` |
| 2 | తల్లి దయ జగతిక్ర్య్త సదా ప్రవహెన | `UIIIIIUIIUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 60% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.050 · model's first choice kept 55% · constraint overrode 37% · backtracks 0

<details><summary>Token probabilities (31 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.78 · `ల్లి` 0.81 · `␣ప్రేమ` 0.85 · `␣అమ` 0.18✱ · `ృత` 0.65 · `ధ` 0.09✱ · `ార` 0.99 · `␣ని` 0.14 · `త్య` 0.89 · `␣స` 0.34 · `్ర` 4.1e-3✱ · `వ` 1.00 · `⏎` 2.3e-6 forced |
| 2 | `త` 0.34 · `ల్లి` 0.75 · `␣ద` 0.10 · `య` 0.88 · `␣జగ` 0.22 · `తి` 0.84 · `క` 0.01✱ · `్ర` 3.6e-10✱ · `్య` 1.7e-6✱ · `్` 6.2e-6✱ · `త` 1.9e-3✱ · `␣స` 0.09 · `దా` 0.10✱ · `␣ప్ర` 0.10 · `వ` 0.77 · `హ` 0.89 · `ె` 0.06✱ · `న` 0.06✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 24 tokens · 6.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగమంతటికంటె గొప్ప | `UIUIIIUIIUIUI` |
| 2 | తల్లి అనుగ్రహం దైవత్వముకని | `UIIUIUUUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 57% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.240 · model's first choice kept 54% · constraint overrode 22% · backtracks 7

<details><summary>Token probabilities (24 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.78 · `ల్లి` 0.81 · `␣ప్రేమ` 0.85 · `␣జగ` 0.17✱ · `మ` 0.03 · `ంత` 0.92 · `టి` 0.66 · `క` 0.31 · `ంట` 0.16✱ · `ె` 0.98 · `␣గొప్ప` 0.76 · `⏎` 1.5e-5 forced |
| 2 | `త` 0.46 · `ల్లి` 0.80 · `␣అను` 0.05 · `గ్రహ` 0.01✱ · `ం` 0.31 · `␣ద` 0.12✱ · `ై` 0.83 · `వ` 0.94 · `త్వ` 0.11 · `ము` 0.32 · `క` 0.37 · `ని` 9.6e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 25 tokens · 6.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ అమృతం తలపించునంత | `UIUIIIUIIUIUI` |
| 2 | తల్లి దయ నిధియే తరగని నిత్య | `UIIIIIUIIIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 56% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.251 · model's first choice kept 48% · constraint overrode 25% · backtracks 6

<details><summary>Token probabilities (25 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.78 · `ల్లి` 0.81 · `␣ప్రేమ` 0.85 · `␣అమ` 0.17✱ · `ృ` 0.20 · `తం` 0.98 · `␣త` 0.06✱ · `ల` 0.83 · `ప` 0.12 · `ించు` 0.32✱ · `న` 0.07 · `ంత` 0.04 · `⏎` 0.06 forced |
| 2 | `త` 0.56 · `ల్లి` 0.67 · `␣ద` 0.10 · `య` 0.92 · `␣ని` 0.03✱ · `ధి` 0.01✱ · `యే` 0.45 · `␣తర` 0.12✱ · `గ` 0.94 · `ని` 0.98 · `␣ని` 0.11 · `త్య` 0.72 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 27 tokens · 5.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాతృ ప్రేమ నిభయమైనది జగతి | `UIUIIIIUIIIII` |
| 2 | జాతర ప్రేమకంట్య్త్చ సుగంధమైన | `UIIUIUIIUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 57% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.039 · model's first choice kept 41% · constraint overrode 35% · backtracks 0

<details><summary>Token probabilities (27 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.08 · `త` 0.96 · `ృ` 0.95 · `␣ప్రేమ` 0.43 · `␣ని` 0.06✱ · `భ` 4.1e-4✱ · `య` 0.39 · `మైన` 0.19 · `ది` 0.31 · `␣జగ` 0.28 · `తి` 0.84 · `⏎` 2.6e-5 forced |
| 2 | `జ` 9.0e-3 · `ాత` 2.7e-3✱ · `ర` 0.81 · `␣ప్రేమ` 0.06 · `క` 0.04 · `ంట` 0.19✱ · `్య` 8.4e-7✱ · `్` 1.5e-3✱ · `త` 0.18 · `్` 6.5e-5✱ · `చ` 8.8e-4✱ · `␣సు` 0.03✱ · `గ` 0.30 · `ంధ` 0.86 · `మైన` 0.09 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 30 tokens · 5.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతిక్ర్య్త సకల కార్య | `UIUIIIUIIIIUI` |
| 2 | ఆ ల్లాభమై నిత్య స్ర్వ్యమయ కార్యమ్ము | `UUIUUIIIIUUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 10% · repeated lines 0 · mean token probability (geometric) 0.004 · model's first choice kept 27% · constraint overrode 52% · backtracks 0

<details><summary>Token probabilities (30 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.78 · `ల్లి` 0.81 · `␣ప్రేమ` 0.85 · `␣జగ` 0.16✱ · `తి` 0.94 · `క` 0.02✱ · `్ర` 4.4e-11✱ · `్య` 2.2e-7✱ · `్` 1.2e-5✱ · `త` 4.1e-3✱ · `␣స` 0.02 · `క` 0.02✱ · `ల` 0.97 · `␣కార్య` 5.2e-3 · `⏎` 2.2e-4 forced |
| 2 | `ఆ` 0.09 · `␣ల` 5.4e-4✱ · `్లా` 3.0e-7✱ · `భ` 0.56 · `మై` 0.02 · `␣ని` 0.65 · `త్య` 0.13 · `␣స` 4.3e-3✱ · `్ర` 1.8e-4✱ · `్వ` 8.2e-7✱ · `్య` 1.2e-3✱ · `మ` 0.09 · `య` 0.12 · `␣కార్య` 0.15✱ · `మ్ము` 2.0e-5✱ |

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

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 83 tokens · 14.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ అమృతము నిరతం సుమధురముగానైతి | `UIUIIIIIIIUIIIIIUUI` |
| 2 | తల్లి చూపుల దీవెనలు త్యుదయమున నిలిచెనుగాన | `UIUIIUIIIIIIIIIIIIUI` |
| 3 | తల్లి ఒడి పలకరింపు మ్ర్వ్తమున మాకు రసముగాన | `UIIIIIIUIIIIUIIIIUI` |
| 4 | తల్లి ఊపిరి వరంబు జగదంతములకల నైతితము | `UIUIIIUIIIUIIIIIUIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 52% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.086 · model's first choice kept 59% · constraint overrode 30% · backtracks 0

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.79 · `␣ప్రేమ` 0.78 · `␣అమ` 0.13✱ · `ృత` 0.72 · `ము` 0.26 · `␣ని` 0.15 · `ర` 8.0e-3✱ · `తం` 1.1e-4✱ · `␣సు` 0.03 · `మ` 0.48 · `ధు` 0.41 · `ర` 0.56 · `ము` 0.46 · `గా` 0.04✱ · `న` 0.02✱ · `ై` 0.04✱ · `తి` 1.3e-3✱ · `⏎` 0.92 forced |
| 2 | `త` 0.39 · `ల్లి` 0.68 · `␣చూపు` 0.14 · `ల` 0.47 · `␣దీ` 0.18 · `వె` 0.98 · `న` 1.00 · `లు` 0.11✱ · `␣త` 0.19✱ · `్య` 4.7e-3✱ · `ు` 8.4e-6✱ · `దయ` 8.0e-4✱ · `ము` 0.31 · `న` 0.22 · `␣ని` 0.37 · `లి` 0.40 · `చె` 0.67 · `ను` 0.67 · `గా` 0.17✱ · `న` 0.24 · `⏎` 1.9e-3 forced |
| 3 | `త` 0.93 · `ల్లి` 0.92 · `␣ఒ` 0.20 · `డి` 1.00 · `␣ప` 1.7e-3✱ · `ల` 0.87 · `క` 0.94 · `రి` 0.95 · `ంపు` 0.96 · `␣మ` 0.04✱ · `్ర` 8.1e-6✱ · `్వ` 1.8e-8✱ · `్` 3.8e-5✱ · `త` 0.06✱ · `ము` 0.41 · `న` 0.60 · `␣మా` 0.15 · `కు` 0.45 · `␣ర` 0.03✱ · `స` 3.7e-4✱ · `ము` 0.38 · `గా` 0.67 · `న` 0.95 · `⏎` 0.95 forced |
| 4 | `త` 0.97 · `ల్లి` 0.94 · `␣ఊ` 0.02 · `పి` 0.58 · `రి` 0.94 · `␣వ` 0.02 · `రం` 0.76 · `బు` 0.81 · `␣జగ` 0.32 · `ద` 6.6e-3✱ · `ంత` 0.96 · `ముల` 0.18 · `క` 0.27 · `ల` 2.8e-4✱ · `␣న` 0.05 · `ై` 0.36 · `తి` 0.87 · `త` 2.5e-4✱ · `ము` 0.72 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 83 tokens · 15.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతిలోన తలపుని సారంబుగాన్జ | `UIUIIIIUIIIIIUUIUI` |
| 2 | తల్లి కరుణ అమృతధర య్వ్వ్తానె నిత్యముగాన్జ ఝంజ | `UIIIIIIIIIUIUIIUIUI` |
| 3 | తల్లి దీవెనల తేజమున దైవమున నిలుచుమున్జ | `UIUIIIUIIIUIIIIIIUI` |
| 4 | తల్లి అనుగ్రహము మధుదయముగా మదిలో నిలిచెను | `UIIUIIIIIIIIUIIUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 48% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.128 · model's first choice kept 59% · constraint overrode 25% · backtracks 0

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.79 · `␣ప్రేమ` 0.78 · `␣జగ` 0.25✱ · `తి` 0.96 · `లో` 0.18 · `న` 0.73 · `␣త` 0.15 · `ల` 0.84 · `పు` 0.46 · `ని` 0.16 · `␣స` 0.01 · `ారం` 0.56 · `బు` 0.28✱ · `గా` 0.05✱ · `న్` 0.02✱ · `జ` 6.8e-5✱ · `⏎` 0.04 forced |
| 2 | `త` 0.38 · `ల్లి` 0.64 · `␣క` 0.29 · `రుణ` 0.98 · `␣అమ` 0.08✱ · `ృత` 0.63 · `ధ` 0.27✱ · `ర` 2.3e-4✱ · `␣య` 2.3e-3✱ · `్వ` 3.4e-7✱ · `్వ` 1.4e-4✱ · `్` 1.5e-3✱ · `త` 0.04✱ · `ాన` 0.04 · `ె` 0.11 · `␣ని` 0.13 · `త్య` 0.34 · `ము` 0.41 · `గా` 0.43 · `న్` 0.77 · `జ` 0.95 · `␣` 4.0e-5✱ · `ఝ` 0.04✱ · `ం` 0.40 · `జ` 0.03✱ · `⏎` 1.00 forced |
| 3 | `త` 0.84 · `ల్లి` 0.90 · `␣దీ` 0.29 · `వె` 0.97 · `న` 0.99 · `ల` 0.29 · `␣తే` 0.12 · `జ` 0.98 · `ము` 0.30 · `న` 0.33 · `␣ద` 0.09 · `ై` 0.46 · `వ` 0.87 · `ము` 0.35 · `న` 0.36 · `␣ని` 0.16 · `లు` 0.20 · `చు` 0.89 · `ము` 0.08 · `న్` 0.04✱ · `జ` 0.58 · `⏎` 0.98 forced |
| 4 | `త` 0.99 · `ల్లి` 0.95 · `␣అను` 0.13 · `గ్రహ` 0.07✱ · `ము` 0.30 · `␣మ` 0.02 · `ధు` 0.35 · `దయ` 2.2e-4✱ · `ము` 0.23 · `గా` 0.31 · `␣మ` 0.34 · `ది` 0.47 · `లో` 0.79 · `␣ని` 0.38 · `లి` 0.50 · `చె` 0.68 · `ను` 0.20✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 76 tokens · 17.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమకలవో తలపు దైవమై నిలిచెను గాన | `UIUIIIUIIIUIUIIIIUI` |
| 2 | తల్లి కరుణయే జగతికి దైవమై నిలిచెను గాన | `UIIIIUIIIIUIUIIIIUI` |
| 3 | తల్లి దీవెనయే తలమున దైవమై నిలిచెను గాన | `UIUIIUIIIIUIUIIIIUI` |
| 4 | తల్లి అనుగ్రహమే అదై నిత్యమై నిలిచెను ర | `UIIUIIUIUUIUIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 75% · single-akshara words 4% · repeated lines 0 · mean token probability (geometric) 0.324 · model's first choice kept 78% · constraint overrode 15% · backtracks 7

<details><summary>Token probabilities (76 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.79 · `␣ప్రేమ` 0.78 · `క` 0.02✱ · `ల` 4.0e-3✱ · `వో` 0.02 · `␣త` 0.14 · `ల` 0.60 · `పు` 0.62 · `␣ద` 3.5e-3✱ · `ై` 0.75 · `వ` 0.91 · `మై` 0.23 · `␣ని` 0.65 · `లి` 0.46 · `చె` 0.87 · `ను` 0.79 · `␣గా` 0.01✱ · `న` 0.60 · `⏎` 8.8e-3 forced |
| 2 | `త` 0.25 · `ల్లి` 0.68 · `␣క` 0.23 · `రుణ` 0.98 · `యే` 0.12✱ · `␣జగ` 0.15 · `తి` 0.87 · `కి` 0.86 · `␣ద` 0.08✱ · `ై` 0.42 · `వ` 0.92 · `మై` 0.30 · `␣ని` 0.43 · `లి` 0.87 · `చె` 0.98 · `ను` 0.98 · `␣గా` 0.51 · `న` 0.99 · `⏎` 1.00 forced |
| 3 | `త` 0.87 · `ల్లి` 0.93 · `␣దీ` 0.13 · `వె` 0.97 · `న` 0.99 · `యే` 0.44 · `␣త` 0.02✱ · `ల` 0.72 · `ము` 0.09 · `న` 0.57 · `␣ద` 0.09 · `ై` 0.84 · `వ` 0.99 · `మై` 0.97 · `␣ని` 0.84 · `లి` 0.96 · `చె` 1.00 · `ను` 1.00 · `␣గా` 0.97 · `న` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ల్లి` 0.95 · `␣అను` 0.30 · `గ్రహ` 0.03✱ · `మే` 0.61 · `␣అ` 0.17 · `ద` 0.04✱ · `ై` 0.05✱ · `␣ని` 0.29 · `త్య` 0.70 · `మై` 0.59 · `␣ని` 0.92 · `లి` 0.95 · `చె` 1.00 · `ను` 1.00 · `␣ర` 2.9e-4✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 74 tokens · 7.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతిలోన తలపుని సారంబుగాన్జ | `UIUIIIIUIIIIIUUIUI` |
| 2 | తల్లి కరుణ అమృతంబు తరగని స్నేహమై నిలుచు | `UIIIIIIUIIIIIUIUIII` |
| 3 | తల్లి ఆశీర్వాదము జగదంతటికీ తేజమై వె | `UIUUUIIIIUIIUUIUI` |
| 4 | తల్లి ప్రేమ నిరంతరము నదయమై వెలుగు నింపుమాన్జ | `UIUIIUIIIIIIUIIIUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 45% · single-akshara words 5% · repeated lines 0 · mean token probability (geometric) 0.208 · model's first choice kept 59% · constraint overrode 23% · backtracks 10

<details><summary>Token probabilities (74 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.79 · `␣ప్రేమ` 0.78 · `␣జగ` 0.25✱ · `తి` 0.96 · `లో` 0.18 · `న` 0.73 · `␣త` 0.15 · `ల` 0.84 · `పు` 0.46 · `ని` 0.16 · `␣స` 0.01 · `ారం` 0.56 · `బు` 0.28✱ · `గా` 0.05✱ · `న్` 0.02✱ · `జ` 6.8e-5✱ · `⏎` 0.04 forced |
| 2 | `త` 0.38 · `ల్లి` 0.64 · `␣క` 0.29 · `రుణ` 0.98 · `␣అమ` 0.08✱ · `ృ` 0.32 · `తం` 0.93 · `బు` 0.68 · `␣తర` 0.01✱ · `గ` 0.93 · `ని` 0.99 · `␣స్` 0.02 · `నే` 0.29 · `హ` 0.70 · `మై` 0.31 · `␣ని` 0.62 · `లు` 0.39 · `చు` 0.85 · `⏎` 0.20 forced |
| 3 | `త` 0.90 · `ల్లి` 0.90 · `␣ఆ` 0.18 · `శ` 0.92 · `ీ` 0.98 · `ర్` 0.72 · `వా` 0.94 · `ద` 0.50✱ · `ము` 0.75 · `␣జగ` 0.15 · `ద` 0.03✱ · `ంత` 0.90 · `టి` 0.05 · `కీ` 0.78 · `␣తే` 0.03 · `జ` 0.94 · `మై` 0.50 · `␣వె` 0.28 · `⏎` 3.1e-10 forced |
| 4 | `త` 0.98 · `ల్లి` 0.94 · `␣ప్రేమ` 0.21 · `␣ని` 0.06✱ · `ర` 2.0e-3✱ · `ంత` 0.74 · `ర` 0.93 · `ము` 0.17✱ · `␣న` 0.03 · `దయ` 5.5e-5✱ · `మై` 0.06✱ · `␣వె` 0.06 · `లుగు` 0.22 · `␣ని` 0.18 · `ంపు` 0.54 · `మా` 0.14 · `న్` 0.36✱ · `జ` 0.02✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 76 tokens · 12.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ అమృతము నిరతం జగతికి దీపము అది | `UIUIIIIIIIUIIIIUIIII` |
| 2 | తల్లి కరుణ సుగంధం నితరము కరుణయే మధుర్య | `UIIIIIUUIIIIIIIUIUI` |
| 3 | తల్లి ఆశీర్వాదము ధనతై నిత్యము శిరస్సుపై ని | `UIUUUIIIIUUIIIUIUI` |
| 4 | తల్లి ప్రేమ జగతికి పుణతై నిత్యము రణమున నిల | `UIUIIIIIIIUUIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 62% · single-akshara words 4% · repeated lines 0 · mean token probability (geometric) 0.144 · model's first choice kept 66% · constraint overrode 26% · backtracks 0

<details><summary>Token probabilities (76 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.79 · `␣ప్రేమ` 0.78 · `␣అమ` 0.13✱ · `ృత` 0.72 · `ము` 0.26 · `␣ని` 0.15 · `ర` 8.0e-3✱ · `తం` 1.1e-4✱ · `␣జగ` 0.08 · `తి` 0.92 · `కి` 0.51 · `␣దీ` 0.08 · `ప` 0.53 · `ము` 0.92 · `␣అది` 8.9e-4✱ · `⏎` 0.91 forced |
| 2 | `త` 0.34 · `ల్లి` 0.79 · `␣క` 0.33 · `రుణ` 0.95 · `␣సు` 0.04✱ · `గ` 0.47 · `ంధ` 1.00 · `ం` 0.17 · `␣ని` 0.15✱ · `తర` 6.2e-5✱ · `ము` 0.60 · `␣క` 0.03 · `రుణ` 0.26 · `యే` 0.04✱ · `␣మ` 0.06✱ · `ధు` 0.39 · `ర్య` 1.4e-3 · `⏎` 2.4e-5 forced |
| 3 | `త` 0.90 · `ల్లి` 0.93 · `␣ఆ` 0.31 · `శ` 0.88 · `ీ` 0.92 · `ర్` 0.63 · `వా` 0.85 · `ద` 0.80 · `ము` 0.92 · `␣ధ` 0.02✱ · `న` 0.65 · `త` 5.7e-4✱ · `ై` 0.37 · `␣ని` 0.38 · `త్య` 0.58 · `ము` 0.70 · `␣శి` 0.02✱ · `ర` 0.79 · `స్సు` 0.74 · `పై` 0.70 · `␣ని` 2.7e-3✱ · `⏎` 2.7e-6 forced |
| 4 | `త` 0.99 · `ల్లి` 0.95 · `␣ప్రేమ` 0.21 · `␣జగ` 0.06✱ · `తి` 0.71 · `కి` 0.67 · `␣పు` 0.02✱ · `ణ` 0.23✱ · `త` 2.1e-6✱ · `ై` 0.93 · `␣ని` 0.21 · `త్య` 0.73 · `ము` 0.94 · `␣ర` 0.03✱ · `ణ` 2.0e-3✱ · `ము` 0.19 · `న` 0.30 · `␣ని` 0.12 · `ల` 0.41 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 79 tokens · 13.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతికి దివి స్ర్వ్తమునందున నిలచెను జగ | `UIUIIIIIIIIIUIIIIIIII` |
| 2 | తల్లి అనుగ్రహము జగదంతాన కరుణతో నిండె | `UIIUIIIIIUUIIIIUUI` |
| 3 | తల్లి వాత్సల్యం జగతికి వ్ర్య్తమునందున నిలచెను జగ | `UIUUUIIIIIIUIIIIIIII` |
| 4 | తల్లి దయ అమృతము జగదంతాన తేజోమయమ్ము | `UIIIIIIIIIUUIUUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 57% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.120 · model's first choice kept 57% · constraint overrode 30% · backtracks 0

<details><summary>Token probabilities (79 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.79 · `␣ప్రేమ` 0.78 · `␣జగ` 0.25✱ · `తి` 0.96 · `కి` 0.64 · `␣ది` 0.03✱ · `వి` 2.1e-3✱ · `␣స` 3.4e-3✱ · `్ర` 0.01✱ · `్వ` 2.2e-7✱ · `్` 1.1e-5✱ · `త` 0.11✱ · `ము` 0.35 · `న` 0.26✱ · `ందు` 0.13✱ · `న` 0.17✱ · `␣ని` 5.6e-3✱ · `ల` 0.15 · `చె` 0.32 · `ను` 0.61 · `␣జగ` 6.4e-4✱ · `⏎` 2.2e-5 forced |
| 2 | `త` 0.25 · `ల్లి` 0.78 · `␣అను` 0.06 · `గ్రహ` 0.03✱ · `ము` 0.45 · `␣జగ` 0.11✱ · `ద` 0.02✱ · `ంత` 0.90 · `ాన` 0.18 · `␣క` 0.04 · `రుణ` 0.48 · `తో` 0.03 · `␣ని` 0.55 · `ండె` 0.19 · `⏎` 5.5e-6 forced |
| 3 | `త` 0.79 · `ల్లి` 0.88 · `␣వా` 0.05 · `త్స` 1.00 · `ల` 0.38 · `్యం` 0.81 · `␣జగ` 0.22 · `తి` 0.56 · `కి` 0.68 · `␣వ` 0.03✱ · `్ర` 8.8e-4✱ · `్య` 7.8e-7✱ · `్` 4.5e-3✱ · `త` 0.44 · `ము` 0.70 · `న` 0.64 · `ందు` 0.72 · `న` 0.89 · `␣ని` 0.31 · `ల` 0.39 · `చె` 0.89 · `ను` 0.92 · `␣జగ` 0.70 · `⏎` 1.00 forced |
| 4 | `త` 0.96 · `ల్లి` 0.96 · `␣ద` 0.09 · `య` 0.83 · `␣అమ` 0.02✱ · `ృత` 0.71 · `ము` 0.34 · `␣జగ` 0.62 · `ద` 0.12✱ · `ంత` 0.97 · `ాన` 0.99 · `␣తే` 0.18 · `జ` 0.95 · `ో` 0.82 · `మ` 0.57 · `య` 0.89 · `మ్ము` 6.7e-3✱ |

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

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 23 tokens · 3.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీరాముని రక్షించుటకు లంక | `UUIIUUIIIUI` |
| 2 | సీరమ్మను రక్షించుటకు వెలెను | `UUIIUUIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.245 · model's first choice kept 78% · constraint overrode 5% · backtracks 0

<details><summary>Token probabilities (23 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.15 · `్రీ` 0.97 · `రా` 0.76 · `ము` 0.58 · `ని` 0.79 · `␣ర` 0.36 · `క్ష` 0.40 · `ించు` 0.54 · `టకు` 0.29 · `␣ల` 0.84 · `ంక` 0.70 · `⏎` 7.6e-5 forced |
| 2 | `సీ` 0.82 · `ర` 8.8e-8✱ · `మ్మ` 0.18 · `ను` 0.71 · `␣ర` 0.37 · `క్ష` 0.75 · `ించు` 0.49 · `టకు` 0.78 · `␣వె` 0.22 · `లె` 0.27 · `ను` 0.96 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 32 tokens · 5.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవనసుతమున లఘువుల దయతో ల | `IIIIIIIIIIIIIUI` |
| 2 | శవనమును దాటి లొ వినుచు లంకా | `IIIIIUIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 44% · single-akshara words 22% · repeated lines 0 · mean token probability (geometric) 0.086 · model's first choice kept 50% · constraint overrode 26% · backtracks 0

<details><summary>Token probabilities (32 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.24 · `వ` 0.70 · `న` 0.99 · `సు` 0.25 · `త` 0.31 · `ము` 0.12 · `న` 0.49 · `␣ల` 0.08✱ · `ఘ` 1.8e-3✱ · `ు` 0.99 · `వు` 0.03✱ · `ల` 0.20 · `␣ద` 0.06 · `య` 0.04✱ · `తో` 0.39 · `␣ల` 0.02✱ · `⏎` 7.4e-7 forced |
| 2 | `శ` 0.12 · `వ` 7.4e-4✱ · `న` 0.35 · `ము` 0.42 · `ను` 0.12 · `␣దా` 0.92 · `టి` 0.81 · `␣ల` 0.56 · `ొ` 2.8e-4✱ · `␣వి` 8.0e-7✱ · `ను` 0.05 · `చు` 0.15 · `␣ల` 0.41 · `ం` 0.26 · `కా` 0.89 |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 30 tokens · 7.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సమరమున సాగెను మారుతి జగతి | `IIIIIUIIUIIIII` |
| 2 | కమలమున కీర్తిని మోసెను రాము | `IIIIIUIIUIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.192 · model's first choice kept 73% · constraint overrode 14% · backtracks 4

<details><summary>Token probabilities (30 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 0.04 · `మ` 0.13 · `ర` 0.40 · `ము` 0.23 · `న` 0.64 · `␣సా` 0.30 · `గ` 0.67 · `ె` 0.97 · `ను` 0.73 · `␣మ` 4.0e-4✱ · `ారు` 0.43 · `తి` 0.79 · `␣జగ` 6.7e-3 · `తి` 0.63 · `⏎` 5.9e-4 forced |
| 2 | `క` 0.06 · `మ` 0.01✱ · `ల` 0.96 · `ము` 0.24 · `న` 0.63 · `␣క` 0.57 · `ీ` 0.24 · `ర్` 0.92 · `తి` 0.82 · `ని` 0.07✱ · `␣మో` 1.5e-3✱ · `సె` 0.55 · `ను` 0.95 · `␣రా` 0.14 · `ము` 0.84 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 29 tokens · 24.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి కరుణా హృదయమంతటికీ | `UIIIUIIIUIIU` |
| 2 | తల్లి అనురాగమేన్ ల్లకరింతును | `UIIIUIUIIUII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.068 · model's first choice kept 62% · constraint overrode 21% · backtracks 30

<details><summary>Token probabilities (29 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.72 · `ల్లి` 0.77 · `␣క` 0.03✱ · `రుణ` 0.97 · `ా` 0.23 · `␣హ` 0.04 · `ృ` 0.40 · `దయ` 0.65 · `మ` 0.17 · `ంత` 0.69 · `టి` 0.66 · `కీ` 0.69 · `⏎` 3.5e-3 forced |
| 2 | `త` 0.32 · `ల్లి` 0.47 · `␣అను` 0.05✱ · `రా` 0.99 · `గ` 0.72 · `మే` 0.54 · `న` 1.0e-3✱ · `్` 2.6e-6✱ · `␣ల` 5.7e-6✱ · `్` 5.2e-7✱ · `ల` 0.55 · `క` 0.20 · `రి` 0.12 · `ం` 0.02 · `తు` 0.83 · `ను` 0.19 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 23 tokens · 1.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీరాముని రక్షించుటకు లంక | `UUIIUUIIIUI` |
| 2 | సీరమ్మను రక్షించెను జగదీ | `UUIIUUIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.206 · model's first choice kept 70% · constraint overrode 5% · backtracks 0

<details><summary>Token probabilities (23 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.15 · `్రీ` 0.97 · `రా` 0.76 · `ము` 0.58 · `ని` 0.79 · `␣ర` 0.36 · `క్ష` 0.40 · `ించు` 0.54 · `టకు` 0.29 · `␣ల` 0.84 · `ంక` 0.70 · `⏎` 7.6e-5 forced |
| 2 | `సీ` 0.82 · `ర` 8.8e-8✱ · `మ్మ` 0.18 · `ను` 0.71 · `␣ర` 0.37 · `క్ష` 0.75 · `ించ` 0.26 · `ె` 0.95 · `ను` 0.82 · `␣జగ` 0.04 · `దీ` 0.05 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 35 tokens · 2.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | అమ్మ హృదయే అమృత్ మ్మత కీరే | `UIIIUIUIIUU` |
| 2 | తొమ్మిది తలపుల తేజ్ మ్మత తీరే | `UIIIIIIUIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 40% · single-akshara words 10% · repeated lines 0 · mean token probability (geometric) 0.045 · model's first choice kept 54% · constraint overrode 26% · backtracks 0

<details><summary>Token probabilities (35 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `అ` 0.10 · `మ్మ` 0.63 · `␣హ` 0.02✱ · `ృ` 0.99 · `ద` 0.33 · `యే` 0.03 · `␣అమ` 0.34 · `ృత` 0.84 · `్` 1.6e-7✱ · `␣మ` 5.4e-4✱ · `్` 1.2e-8✱ · `మ` 0.97 · `త` 0.22 · `␣క` 0.03 · `ీ` 0.23 · `రే` 9.5e-4 · `⏎` 0.82 forced |
| 2 | `త` 0.57 · `ొ` 3.4e-3✱ · `మ్` 4.8e-3✱ · `మి` 0.98 · `ది` 0.95 · `␣త` 0.13 · `ల` 0.29 · `పు` 0.44 · `ల` 0.57 · `␣తే` 0.17 · `జ` 0.82 · `్` 2.8e-4✱ · `␣మ` 0.05✱ · `్` 2.5e-3✱ · `మ` 0.98 · `త` 0.84 · `␣తీ` 0.09 · `రే` 1.00 |

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

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 88 tokens · 14.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలకరి హరిని రక్షించు తలమున ధైర్యమున తోడ | `IIIIIIIUUIIIIIUIIIUI` |
| 2 | లొలికిన సీతానుని రక్ష్యుడై లంకమున వెలెను క | `IIIIUUIIUIUUIIIIIII` |
| 3 | దులల మాయను వీడి దైవలీలమున వీడి పోయ | `IIIUIIUIUIUIIIUIUI` |
| 4 | శృలమున భయము వీడి శ్రీమృగమున చేరును సుమనా | `IIIIIIIUIUIIIIUIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 4% · repeated lines 0 · mean token probability (geometric) 0.127 · model's first choice kept 53% · constraint overrode 22% · backtracks 0

<details><summary>Token probabilities (88 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.03 · `ొ` 0.18 · `ల` 0.68 · `క` 0.65 · `రి` 0.43 · `␣హ` 7.4e-3 · `రి` 0.38 · `ని` 0.56 · `␣ర` 0.29 · `క్ష` 0.91 · `ించు` 0.70 · `␣త` 0.07✱ · `ల` 0.69 · `ము` 0.18 · `న` 0.39 · `␣ధ` 0.01 · `ై` 0.46 · `ర్య` 0.75 · `ము` 0.80 · `న` 0.28 · `␣తో` 3.5e-3✱ · `డ` 0.54 · `⏎` 1.8e-4 forced |
| 2 | `ల` 0.05 · `ొ` 0.01✱ · `లి` 6.7e-5✱ · `కి` 0.58 · `న` 0.49 · `␣సీ` 0.53 · `తా` 0.50 · `ను` 0.21✱ · `ని` 0.29 · `␣ర` 0.28 · `క్ష` 0.36✱ · `్య` 5.0e-3✱ · `ు` 0.02✱ · `డ` 0.01✱ · `ై` 0.74 · `␣ల` 0.78 · `ంక` 0.70 · `ము` 0.23 · `న` 0.55 · `␣వె` 0.14✱ · `లె` 0.06✱ · `ను` 0.57 · `␣క` 1.0e-2✱ · `⏎` 2.2e-5 forced |
| 3 | `దు` 0.05 · `ల` 1.7e-3✱ · `ల` 0.31 · `␣మ` 0.03 · `ాయ` 0.80 · `ను` 0.08 · `␣వీ` 0.25 · `డి` 0.97 · `␣ద` 0.09 · `ై` 0.38 · `వ` 0.81 · `లీ` 5.0e-3✱ · `ల` 0.96 · `ము` 0.02 · `న` 0.55 · `␣వీ` 0.02 · `డి` 0.08 · `␣పో` 0.11 · `య` 0.85 · `⏎` 7.1e-4 forced |
| 4 | `శ` 0.09 · `ృ` 9.8e-3✱ · `ల` 1.0e-6✱ · `ము` 0.31 · `న` 0.63 · `␣భ` 0.08 · `య` 0.80 · `ము` 0.74 · `␣వీ` 0.21 · `డి` 0.99 · `␣శ్రీ` 0.28 · `మ` 0.04✱ · `ృ` 7.0e-4✱ · `గ` 0.29 · `ము` 0.74 · `న` 0.74 · `␣చేరు` 0.03 · `ను` 0.54 · `␣సు` 0.03 · `మ` 0.72 · `నా` 0.17✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 85 tokens · 14.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతికి తేజోమ్ ల్లికై నిలిచెనుగాదు | `UIUIIIIIUUIUIIIIUI` |
| 2 | తల్లి చూపుల వెన్నెలుర దైవమై మెరిసెనుగాదు | `UIUIIUIIIUIUIIIIUI` |
| 3 | తల్లి మాట తీపిని తేజోమ్ ల్లికై నిలిచెనుగాదు | `UIUIUIIUUIUIIIIUI` |
| 4 | తల్లి ఆశ్రయమే అమృతమై ల్లికై నిలిచెనుగాదు | `UIUIIUIIIUIUIIIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 41% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.142 · model's first choice kept 71% · constraint overrode 12% · backtracks 0

<details><summary>Token probabilities (85 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.76 · `ల్లి` 0.74 · `␣ప్రేమ` 0.80 · `␣జగ` 0.29 · `తి` 0.96 · `కి` 0.58 · `␣తే` 0.05 · `జ` 0.91 · `ో` 0.60 · `మ` 0.90 · `్` 9.3e-15✱ · `␣` 2.1e-7✱ · `ల్లి` 4.0e-5✱ · `క` 0.22 · `ై` 0.61 · `␣ని` 0.25 · `లి` 0.43 · `చె` 0.80 · `ను` 0.74 · `గా` 0.02✱ · `దు` 8.6e-4✱ · `⏎` 0.96 forced |
| 2 | `త` 0.23 · `ల్లి` 0.57 · `␣చూపు` 0.09 · `ల` 0.17 · `␣వె` 0.06 · `న్న` 0.23 · `ె` 0.35 · `లు` 0.41 · `ర` 0.01 · `␣ద` 0.03✱ · `ై` 0.80 · `వ` 0.96 · `మై` 0.21 · `␣మె` 0.15 · `రి` 0.92 · `సె` 0.93 · `ను` 0.94 · `గా` 0.72 · `దు` 0.98 · `⏎` 1.00 forced |
| 3 | `త` 0.93 · `ల్లి` 0.92 · `␣మాట` 0.07 · `␣తీ` 0.11 · `పి` 0.20 · `ని` 0.11 · `␣తే` 0.03 · `జ` 0.32 · `ో` 0.27 · `మ` 0.68 · `్` 0.46 · `␣` 0.08✱ · `ల్లి` 0.84 · `క` 0.97 · `ై` 0.99 · `␣ని` 0.23 · `లి` 0.73 · `చె` 0.98 · `ను` 1.00 · `గా` 1.00 · `దు` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ల్లి` 0.97 · `␣ఆ` 0.14 · `శ` 0.94 · `్ర` 0.14✱ · `య` 0.32 · `మే` 0.28 · `␣అమ` 0.14 · `ృత` 0.78 · `మై` 0.47 · `␣ల` 2.0e-3✱ · `్` 4.8e-8✱ · `లి` 0.20 · `క` 0.66 · `ై` 0.98 · `␣ని` 0.82 · `లి` 0.92 · `చె` 1.00 · `ను` 1.00 · `గా` 1.00 · `దు` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 79 tokens · 29.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ నిత్య సుగంధమై నిలిచెను జగతిలో | `UIUIUIIUIUIIIIIIIU` |
| 2 | తల్లి దీవెన అమృత జలమై ల్లిచెను హృదయంలోంబు | `UIUIIIIIIIUIIIIIUUI` |
| 3 | తల్లి కరుణ అనంత తేజోమ్ ల్లిచెను చినుకులలోంబు | `UIIIIIUIUUIIIIIIIUI` |
| 4 | తల్లి అనుగ్రహం సాటి లేద్ ల్లిచెను సమస్త జగతి | `UIIUIUUIUIIIIUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 52% · single-akshara words 4% · repeated lines 0 · mean token probability (geometric) 0.088 · model's first choice kept 65% · constraint overrode 24% · backtracks 30

<details><summary>Token probabilities (79 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.76 · `ల్లి` 0.74 · `␣ప్రేమ` 0.79 · `␣ని` 0.06 · `త్య` 0.73 · `␣సు` 0.08 · `గ` 0.27 · `ంధ` 1.00 · `మై` 0.13 · `␣ని` 0.33 · `లి` 0.53 · `చె` 0.69 · `ను` 0.84 · `␣జగ` 0.24 · `తి` 0.91 · `లో` 0.76 · `⏎` 0.35 forced |
| 2 | `త` 0.23 · `ల్లి` 0.57 · `␣దీ` 0.12 · `వె` 0.97 · `న` 1.00 · `␣అమ` 0.30 · `ృత` 0.77 · `␣జ` 0.04 · `ల` 0.90 · `మై` 0.86 · `␣ల` 5.0e-4✱ · `్` 1.1e-8✱ · `లి` 0.17✱ · `చె` 0.85 · `ను` 0.99 · `␣హ` 0.10✱ · `ృ` 0.99 · `ద` 0.40 · `యంలో` 0.90 · `ం` 4.5e-5✱ · `బు` 3.4e-3✱ · `⏎` 0.99 forced |
| 3 | `త` 0.89 · `ల్లి` 0.92 · `␣క` 0.56 · `రుణ` 0.96 · `␣అన` 0.22 · `ంత` 0.99 · `␣తే` 0.24 · `జ` 0.99 · `ో` 0.16✱ · `మ` 0.52 · `్` 1.2e-13✱ · `␣` 7.7e-8✱ · `ల్లి` 2.4e-4✱ · `చె` 0.89 · `ను` 0.97 · `␣చి` 0.04✱ · `ను` 0.01✱ · `కు` 0.91 · `లలో` 0.46 · `ం` 0.23✱ · `బు` 0.98 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ల్లి` 0.96 · `␣అను` 0.17 · `గ్రహ` 0.01✱ · `ం` 0.51 · `␣సా` 0.05 · `టి` 0.73 · `␣లే` 0.50 · `ద` 0.09✱ · `్` 6.9e-7✱ · `␣` 4.1e-5✱ · `ల్లి` 0.35 · `చె` 0.99 · `ను` 1.00 · `␣సమ` 0.03✱ · `స్త` 0.99 · `␣జగ` 0.24 · `తి` 0.80 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 83 tokens · 14.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలకరి హరిని రక్షించు తలమున ధైర్యమున తోడ | `IIIIIIIUUIIIIIUIIIUI` |
| 2 | వెలసిన సీతానుని వేళల విలపమును వీడెను ద | `IIIIUUIIUIIIIIIIUIII` |
| 3 | అలసిన లంకాధిపతిని అణచివేయుటకు వెలెను ద | `IIIIUUIIIIIIIUIIIIIII` |
| 4 | భలే బలముతోను భీతిని లను భగ్నము చేసితిన్ | `IUIIIUIUIIIIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 48% · single-akshara words 9% · repeated lines 0 · mean token probability (geometric) 0.206 · model's first choice kept 64% · constraint overrode 14% · backtracks 2

<details><summary>Token probabilities (83 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.03 · `ొ` 0.18 · `ల` 0.68 · `క` 0.65 · `రి` 0.43 · `␣హ` 7.4e-3 · `రి` 0.38 · `ని` 0.56 · `␣ర` 0.29 · `క్ష` 0.91 · `ించు` 0.70 · `␣త` 0.07✱ · `ల` 0.69 · `ము` 0.18 · `న` 0.39 · `␣ధ` 0.01 · `ై` 0.46 · `ర్య` 0.75 · `ము` 0.80 · `న` 0.28 · `␣తో` 3.5e-3✱ · `డ` 0.54 · `⏎` 1.8e-4 forced |
| 2 | `వ` 0.07✱ · `ెల` 5.1e-4✱ · `సిన` 0.31 · `␣సీ` 0.43 · `తా` 0.50 · `ను` 0.26 · `ని` 0.44 · `␣వే` 0.10 · `ళ` 0.07✱ · `ల` 0.16 · `␣వి` 0.24 · `ల` 0.39 · `ప` 0.31 · `ము` 0.46 · `ను` 0.15 · `␣వీ` 0.14 · `డ` 0.41 · `ె` 0.68 · `ను` 0.51 · `␣ద` 0.01✱ · `⏎` 2.4e-5 forced |
| 3 | `అ` 0.08✱ · `ల` 2.1e-3✱ · `సిన` 0.77 · `␣ల` 0.52 · `ం` 0.37 · `కా` 0.89 · `ధి` 0.20 · `పతి` 0.68 · `ని` 0.41 · `␣అ` 0.39 · `ణ` 0.64 · `చి` 0.79 · `వే` 0.69 · `యు` 0.75 · `టకు` 0.47 · `␣వె` 0.22 · `లె` 0.28✱ · `ను` 0.97 · `␣ద` 0.18 · `⏎` 0.97 forced |
| 4 | `భ` 0.09 · `లే` 1.5e-3✱ · `␣బల` 0.07 · `ము` 0.74 · `తో` 0.29 · `ను` 0.09 · `␣భ` 0.80 · `ీ` 0.15 · `తి` 0.70 · `ని` 0.85 · `␣` 7.9e-4✱ · `లను` 0.22 · `␣భ` 0.19 · `గ్` 0.24 · `న` 0.84 · `ము` 0.76 · `␣చేసి` 0.38 · `తి` 0.19 · `న్` 0.13 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 85 tokens · 6.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వనమున లంకా దహించి రణమున రాముడు నిలిచే | `IIIIUUIUIIIIIUIIIIU` |
| 2 | తనువని శివమున ధరించు సనతులు కీర్తిచేనుగా | `IIIIIIIIIUIIIIIUIUIU` |
| 3 | శృనగమున సుమతిని రక్షయే తనువున నిలిచెనుగా | `IIIIIIIIIUIUIIIIIIIIU` |
| 4 | ధనుర్ధారి దైవమై జగని రణమున జయించాలి | `IUUIUIUIIIIIIIIUUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 43% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.119 · model's first choice kept 55% · constraint overrode 27% · backtracks 0

<details><summary>Token probabilities (85 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.08 · `న` 0.73 · `ము` 0.27 · `న` 0.85 · `␣ల` 0.05 · `ం` 0.29 · `కా` 0.82 · `␣ద` 0.17 · `హ` 0.75 · `ించి` 0.26✱ · `␣ర` 0.35 · `ణ` 6.2e-3✱ · `ము` 0.86 · `న` 0.68 · `␣రా` 0.11 · `ము` 0.94 · `డు` 0.58 · `␣ని` 0.04✱ · `లి` 0.76 · `చే` 3.9e-3 · `⏎` 0.04 forced |
| 2 | `త` 0.04✱ · `ను` 0.03✱ · `వ` 0.31 · `ని` 0.31✱ · `␣శి` 0.03 · `వ` 0.67 · `ము` 0.26 · `న` 0.43 · `␣ధ` 0.02 · `రించ` 0.05✱ · `ు` 0.37 · `␣స` 0.08✱ · `న` 7.4e-4✱ · `తులు` 0.03 · `␣క` 0.05 · `ీ` 0.67 · `ర్` 0.90 · `తి` 0.69 · `చే` 0.27 · `ను` 5.1e-5✱ · `గా` 3.3e-4✱ · `⏎` 0.97 forced |
| 3 | `శ` 0.12✱ · `ృ` 0.02✱ · `న` 5.4e-4✱ · `గ` 0.92 · `ము` 0.26 · `న` 0.77 · `␣సు` 0.03✱ · `మ` 0.68 · `తి` 0.49 · `ని` 0.55 · `␣ర` 0.66 · `క్ష` 0.82 · `యే` 1.9e-4✱ · `␣త` 0.05 · `ను` 0.15✱ · `వు` 0.09 · `న` 0.45 · `␣ని` 0.20 · `లి` 0.51 · `చ` 0.03✱ · `ె` 0.26 · `ను` 0.57 · `గా` 0.54 · `⏎` 1.00 forced |
| 4 | `ధ` 0.04 · `ను` 0.02✱ · `ర్` 0.57 · `ధ` 0.40 · `ారి` 0.55 · `␣ద` 0.21 · `ై` 0.84 · `వ` 0.97 · `మై` 0.17 · `␣జగ` 0.37 · `ని` 1.5e-4✱ · `␣ర` 0.18✱ · `ణ` 4.0e-4✱ · `ము` 0.82 · `న` 0.64 · `␣జ` 0.20 · `య` 0.97 · `ించాలి` 7.8e-3 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 81 tokens · 5.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాతృ ప్రేమకై మధురమదిన్ తలపున నిలిచెను జగ | `UIUIUIIIIUIIIIIIIIII` |
| 2 | తాతృ అనుగ్రహం తరగనిద్ తనలోన వెలసింది | `UIIUIUIIIUIIUIIIUI` |
| 3 | తాతృ తపము తేజమై తరగ్ తనయందు నిలిచెనో | `UIIIIUIUIUIIUIIIIU` |
| 4 | తాతృ తపని కరుణయే తరగ్ తలపున వెలసెనుగా | `UIIIIIIIUIUIIIIIIIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 35% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.076 · model's first choice kept 52% · constraint overrode 26% · backtracks 0

<details><summary>Token probabilities (81 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.10 · `త` 0.97 · `ృ` 0.97 · `␣ప్రేమ` 0.22✱ · `క` 0.02 · `ై` 0.85 · `␣మ` 0.47 · `ధు` 0.31 · `ర` 0.78 · `మ` 0.10✱ · `ది` 0.34 · `న్` 9.8e-3✱ · `␣త` 0.02✱ · `ల` 0.74 · `పు` 0.37 · `న` 0.07 · `␣ని` 0.27 · `లి` 0.57 · `చె` 0.81 · `ను` 0.76 · `␣జగ` 1.7e-3✱ · `⏎` 5.3e-6 forced |
| 2 | `త` 0.33 · `ాత` 3.3e-4✱ · `ృ` 0.27✱ · `␣అను` 0.17 · `గ్రహ` 5.1e-3✱ · `ం` 0.24 · `␣తర` 0.11 · `గ` 0.93 · `ని` 0.83 · `ద` 0.03✱ · `్` 2.2e-9✱ · `␣తన` 3.4e-8✱ · `లో` 0.11 · `న` 0.67 · `␣వె` 0.11 · `ల` 0.30 · `సింది` 0.01 · `⏎` 0.22 forced |
| 3 | `త` 0.70 · `ాత` 3.3e-3✱ · `ృ` 0.90 · `␣త` 0.33 · `ప` 0.18 · `ము` 0.04 · `␣తే` 0.05 · `జ` 0.83 · `మై` 0.13✱ · `␣తర` 0.38 · `గ` 0.86 · `్` 6.2e-12✱ · `␣తన` 2.7e-5✱ · `య` 0.05 · `ందు` 0.79 · `␣ని` 0.40 · `లి` 0.62 · `చె` 0.81 · `నో` 0.01 · `⏎` 0.45 forced |
| 4 | `త` 0.92 · `ాత` 0.85 · `ృ` 0.96 · `␣త` 0.76 · `ప` 0.07 · `ని` 0.03 · `␣క` 0.06✱ · `రుణ` 0.82 · `యే` 0.11✱ · `␣తర` 0.41 · `గ` 0.84 · `్` 0.06✱ · `␣త` 0.37 · `ల` 0.64 · `పు` 0.34 · `న` 0.56 · `␣వె` 0.03 · `ల` 0.54 · `సె` 0.06✱ · `ను` 0.86 · `గా` 0.04✱ |

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

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 21 tokens · 3.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగ్ ల్ల దీప | `UIUIUIUI` |
| 2 | తల్లి కరుణ అమ్ ల్ల రూప | `UIIIIUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 60% · single-akshara words 40% · repeated lines 0 · mean token probability (geometric) 0.009 · model's first choice kept 52% · constraint overrode 40% · backtracks 0

<details><summary>Token probabilities (21 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.74 · `ల్లి` 0.81 · `␣ప్రేమ` 0.72 · `␣జగ` 0.24 · `్` 4.2e-10✱ · `␣` 8.2e-8✱ · `ల్` 1.7e-6✱ · `ల` 4.8e-3✱ · `␣దీ` 0.04 · `ప` 0.62 · `⏎` 1.5e-5 forced |
| 2 | `త` 0.44 · `ల్లి` 0.70 · `␣క` 0.16 · `రుణ` 0.98 · `␣అమ` 0.07✱ · `్` 9.5e-8✱ · `␣` 0.02✱ · `ల్` 0.13✱ · `ల` 0.64 · `␣రూప` 0.09 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 23 tokens · 5.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవన తేజము వీచి పర్ | `IIIUIIUIU` |
| 2 | వృ వలము దాటి వలకమున | `IIIIUIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 25% · repeated lines 0 · mean token probability (geometric) 0.093 · model's first choice kept 61% · constraint overrode 23% · backtracks 0

<details><summary>Token probabilities (23 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.19 · `వ` 0.59 · `న` 0.99 · `␣తే` 0.23 · `జ` 0.97 · `ము` 0.61 · `␣వీ` 0.02✱ · `చి` 0.43 · `␣ప` 0.09 · `ర్` 0.24 · `⏎` 4.5e-10 forced |
| 2 | `వ` 0.11 · `ృ` 5.0e-4✱ · `␣వ` 2.5e-6✱ · `ల` 0.32 · `ము` 0.32 · `␣దా` 0.58 · `టి` 0.83 · `␣వ` 8.4e-3✱ · `ల` 0.24 · `క` 0.20 · `ము` 0.02 · `న` 0.14✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 21 tokens · 5.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవన తేజము వీచి గమ | `IIIUIIUIII` |
| 2 | శవన లంకను వీచె గమ | `IIIUIIUIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 75% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.196 · model's first choice kept 67% · constraint overrode 15% · backtracks 3

<details><summary>Token probabilities (21 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.19 · `వ` 0.59 · `న` 0.99 · `␣తే` 0.23 · `జ` 0.97 · `ము` 0.59 · `␣వీ` 0.02✱ · `చి` 0.43 · `␣గ` 0.09 · `మ` 0.69 · `⏎` 1.5e-5 forced |
| 2 | `శ` 0.06 · `వ` 6.3e-3✱ · `న` 0.72 · `␣ల` 0.14 · `ంక` 0.59 · `ను` 0.48 · `␣వీ` 2.0e-3✱ · `చె` 0.31 · `␣గ` 0.17 · `మ` 0.99 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 29 tokens · 18.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమయేక్ ల్ల వసన | `UIUIUIIII` |
| 2 | తల్లి మమతయేక్ ల్ల వసన | `UIIIIUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 25% · repeated lines 0 · mean token probability (geometric) 0.045 · model's first choice kept 62% · constraint overrode 18% · backtracks 30

<details><summary>Token probabilities (29 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.74 · `ల్లి` 0.81 · `␣ప్రేమ` 0.73 · `యే` 0.26 · `క` 8.2e-4✱ · `్` 1.0e-8✱ · `␣` 2.4e-6✱ · `ల` 8.2e-7✱ · `్` 2.1e-5✱ · `ల` 0.73 · `␣వ` 5.2e-3 · `స` 0.02 · `న` 0.02 · `⏎` 7.2e-4 forced |
| 2 | `త` 0.32 · `ల్లి` 0.68 · `␣మ` 0.08 · `మ` 0.93 · `త` 0.90 · `యే` 0.84 · `క` 0.67 · `్` 0.93 · `␣` 0.17 · `ల` 0.97 · `్` 0.99 · `ల` 1.00 · `␣వ` 0.29 · `స` 0.66 · `న` 0.94 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 20 tokens · 1.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ అమ్ ల్లినంత | `UIUIUIUI` |
| 2 | తల్లి కరుణ అమ్ ల్లినంత | `UIIIIUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 25% · repeated lines 0 · mean token probability (geometric) 0.026 · model's first choice kept 55% · constraint overrode 26% · backtracks 0

<details><summary>Token probabilities (20 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.74 · `ల్లి` 0.81 · `␣ప్రేమ` 0.72 · `␣అమ` 0.11 · `్` 5.2e-12✱ · `␣` 6.9e-9✱ · `ల్ల` 3.1e-4✱ · `ిన` 0.05✱ · `ంత` 0.04 · `⏎` 1.5e-4 forced |
| 2 | `త` 0.54 · `ల్లి` 0.53 · `␣క` 0.10 · `రుణ` 0.97 · `␣అమ` 0.05✱ · `్` 0.69 · `␣` 0.94 · `ల్ల` 1.00 · `ిన` 0.92 · `ంత` 0.99 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 23 tokens · 1.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగ్ ల్లకంట | `UIUIUIUI` |
| 2 | తల్లి దయ అమృత్ ల్లకంట | `UIIIIUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.010 · model's first choice kept 57% · constraint overrode 36% · backtracks 0

<details><summary>Token probabilities (23 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.74 · `ల్లి` 0.81 · `␣ప్రేమ` 0.72 · `␣జగ` 0.24 · `్` 4.2e-10✱ · `␣` 8.2e-8✱ · `ల్` 1.7e-6✱ · `ల` 4.8e-3✱ · `క` 0.16 · `ంట` 0.32✱ · `⏎` 2.2e-4 forced |
| 2 | `త` 0.48 · `ల్లి` 0.61 · `␣ద` 0.14 · `య` 0.82 · `␣అమ` 0.06 · `ృత` 0.53 · `్` 2.0e-6✱ · `␣ల` 4.9e-3✱ · `్` 7.7e-7✱ · `ల` 0.76 · `క` 0.71 · `ంట` 0.98 |

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

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 114 tokens · 22.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాతృ ప్రేమ నిశిలోనన్ తొలి దీపంబుగాను గాదుముగానుగాను గాదు | `UIUIIIUUIIUUIUIUIIUIUIUI` |
| 2 | తల్లి కరుణ అమృతధరమై జగతికి నిత్యంబులందును సత్యముగను | `UIIIIIIIIIUIIIIUUIUIIUIIII` |
| 3 | అమ్మ ఒడి ధరణిలోన్ మ్మకై వెలుగునిచ్చును మహోన్నత భావముననుగాదు | `UIIIIIIUIUIIIUIIIUIIUIIIIUI` |
| 4 | తల్లి అనుగ్రహమున్ ల్లభించును శాంతి సుఖమును జగతికి దిఖయముగను | `UIIUIIUIUIIUIIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 48% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.081 · model's first choice kept 53% · constraint overrode 32% · backtracks 0

<details><summary>Token probabilities (114 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.15 · `త` 0.98 · `ృ` 0.99 · `␣ప్రేమ` 0.31 · `␣ని` 0.04✱ · `శి` 2.0e-3✱ · `లో` 0.56 · `న` 0.73 · `న` 2.0e-3✱ · `్` 8.8e-8✱ · `␣` 1.3e-5✱ · `త` 5.2e-5✱ · `ొ` 0.34 · `లి` 0.69 · `␣దీ` 0.30 · `పం` 0.32 · `బు` 0.41 · `గా` 0.20✱ · `ను` 0.03✱ · `␣గా` 4.5e-3✱ · `దు` 0.08 · `ము` 4.2e-3✱ · `గా` 3.8e-3✱ · `ను` 0.04✱ · `గా` 5.3e-4✱ · `ను` 0.04✱ · `␣గా` 2.1e-3✱ · `దు` 0.61 · `⏎` 0.40 forced |
| 2 | `త` 0.54 · `ల్లి` 0.88 · `␣క` 0.49 · `రుణ` 0.87 · `␣అమ` 0.08✱ · `ృత` 0.69 · `ధ` 0.61 · `ర` 2.3e-4✱ · `మై` 0.72 · `␣జగ` 0.33 · `తి` 0.91 · `కి` 0.81 · `␣ని` 0.17 · `త్య` 0.79 · `ం` 0.18 · `బు` 0.59 · `ల` 0.29 · `ందు` 0.02✱ · `ను` 0.21 · `␣స` 0.06 · `త్య` 0.46 · `ము` 0.28 · `గ` 0.02✱ · `ను` 0.58 · `⏎` 0.01 forced |
| 3 | `అ` 0.13 · `మ్మ` 0.51 · `␣ఒ` 0.36 · `డి` 1.00 · `␣ధ` 6.2e-3✱ · `రణ` 0.05✱ · `ి` 0.83 · `లో` 0.20 · `న` 0.92 · `్` 7.7e-6✱ · `␣మ` 0.03✱ · `్` 6.5e-7✱ · `మ` 0.97 · `క` 0.12 · `ై` 0.91 · `␣వె` 0.08 · `లుగు` 0.62 · `ని` 0.23 · `చ్చు` 0.61 · `ను` 0.28 · `␣మహ` 0.03 · `ో` 0.72 · `న్న` 0.86 · `త` 0.99 · `␣భా` 0.07 · `వ` 0.97 · `ము` 0.82 · `న` 0.12✱ · `ను` 0.11✱ · `గా` 0.13✱ · `దు` 0.43 · `⏎` 0.98 forced |
| 4 | `త` 0.43 · `ల్లి` 0.85 · `␣అను` 0.12 · `గ్రహ` 0.12✱ · `ము` 0.34 · `న` 0.06✱ · `్` 1.4e-3✱ · `␣ల` 2.3e-4✱ · `్` 3.6e-6✱ · `ల` 0.57 · `భ` 0.24 · `ించు` 0.45 · `ను` 0.36 · `␣శా` 0.27 · `ంతి` 0.79 · `␣సు` 0.07 · `ఖ` 1.00 · `ము` 0.70 · `ను` 0.15 · `␣జగ` 0.17 · `తి` 0.83 · `కి` 0.42 · `␣ది` 9.9e-3✱ · `ఖ` 1.6e-6✱ · `య` 0.92 · `ము` 0.67 · `గ` 0.11✱ · `ను` 0.96 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 117 tokens · 19.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామచంద్రుని తేజమున్ మాయమై లంకకు గమించెను వనితేని గమనంబు | `UIUIIUIUUIUUIIIUIIIIUIIIUI` |
| 2 | సీతా రణమున భయాన్ తోడవై రక్షితంబుగా నిలిచెను రామ్ బలంబు | `UUIIIIIUUIUUIUIUIIIIUIUI` |
| 3 | రావణ మాయలు విచ్ వేయగా రామచంద్రుని ధైర్యమునెన్ ద్రుణిణెను | `UIIUIIUUIUUIUIIUIIUIIII` |
| 4 | సముదయమున సప్తసాగరముల దాటి సాగెను రామచంద్రున్ గమించ | `IIIIIIUIUIIIIUIUIIUIUUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 43% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.072 · model's first choice kept 60% · constraint overrode 30% · backtracks 0

<details><summary>Token probabilities (117 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.16 · `మ` 0.78 · `చ` 0.87 · `ంద్ర` 1.00 · `ు` 0.85 · `ని` 0.98 · `␣తే` 0.05 · `జ` 0.98 · `ము` 0.42 · `న` 0.22 · `్` 3.7e-6✱ · `␣మ` 1.9e-4✱ · `ాయ` 0.62 · `మై` 0.30 · `␣ల` 0.44 · `ంక` 0.75 · `కు` 0.27 · `␣గ` 0.26✱ · `మ` 0.75 · `ించ` 0.49 · `ె` 0.99 · `ను` 0.89 · `␣వ` 2.5e-3✱ · `ని` 0.03✱ · `తే` 3.5e-4✱ · `ని` 0.02✱ · `␣` 1.4e-3✱ · `గ` 9.5e-6✱ · `మ` 0.62 · `నం` 0.29✱ · `బు` 0.13✱ · `⏎` 0.74 forced |
| 2 | `సీ` 0.84 · `తా` 0.56 · `␣ర` 0.02✱ · `ణ` 5.7e-4✱ · `ము` 0.38 · `న` 0.76 · `␣భ` 0.18 · `య` 0.89 · `ాన` 0.08✱ · `్` 1.6e-9✱ · `␣తో` 4.5e-4✱ · `డ` 0.50 · `వై` 0.03✱ · `␣ర` 0.46 · `క్ష` 0.69 · `ిత` 8.0e-4✱ · `ం` 0.15✱ · `బు` 0.91 · `గా` 0.35 · `␣ని` 0.27 · `లి` 0.69 · `చె` 0.91 · `ను` 0.95 · `␣రామ` 0.04 · `్` 3.7e-8✱ · `␣బ` 6.5e-4✱ · `లం` 0.45 · `బు` 0.99 · `⏎` 0.94 forced |
| 3 | `రా` 0.37 · `వ` 0.88 · `ణ` 0.67 · `␣మ` 0.28 · `ాయ` 0.88 · `లు` 0.10 · `␣వి` 0.09 · `చ్` 0.11✱ · `␣వే` 3.5e-6✱ · `య` 0.61 · `గా` 0.26 · `␣రామ` 0.07 · `చ` 0.57 · `ంద్ర` 0.99 · `ు` 0.55 · `ని` 0.97 · `␣ధ` 0.24 · `ై` 0.81 · `ర్య` 0.82 · `ము` 0.73 · `న` 0.38 · `ె` 4.3e-3✱ · `న` 0.03✱ · `్` 1.8e-4✱ · `␣` 3.0e-3✱ · `ద్` 7.3e-6✱ · `రుణ` 2.7e-7✱ · `ి` 0.04✱ · `ణ` 0.04 · `ె` 0.22 · `ను` 0.85 · `⏎` 0.41 forced |
| 4 | `స` 0.13 · `ము` 0.24 · `దయ` 4.5e-3✱ · `ము` 0.20 · `న` 0.74 · `␣స` 0.07 · `ప్త` 0.05 · `సాగ` 0.21 · `ర` 0.88 · `ముల` 0.12 · `␣దా` 0.60 · `టి` 0.82 · `␣సా` 0.08 · `గ` 0.66 · `ె` 0.98 · `ను` 0.98 · `␣రామ` 0.18 · `చ` 0.77 · `ంద్ర` 1.00 · `ు` 0.84 · `న్` 6.7e-3✱ · `␣గ` 0.02✱ · `మ` 0.74 · `ించ` 0.02✱ |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 120 tokens · 15.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ అమృతధార జీవన సోపనమునందునితినుమునుమునమునుము | `UIUIIIIUIUIIUIIIUIIIIIIIIIII` |
| 2 | తల్లి దీవెన తేజమైక్ ల్లున నిలిచెను సత్యమునందునితిన్ త్యజించ | `UIUIIUIUIIIIIIUIIUIIUIUI` |
| 3 | తల్లి ఒడిన సుఖమున్ ల్లెను నిత్యమునందునితినుమునమున్ దయమున | `UIIIIIIUIIUIIUIIIIIIUIIII` |
| 4 | తల్లి కరుణ రక్షమైక్ ల్లున నిలిచెను జగతిలోనందునితి గమమునము | `UIIIIUIUIIIIIIIIIUUIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 52% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.072 · model's first choice kept 55% · constraint overrode 33% · backtracks 30

<details><summary>Token probabilities (120 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.75 · `ల్లి` 0.83 · `␣ప్రేమ` 0.78 · `␣అమ` 0.12✱ · `ృత` 0.76 · `ధ` 0.21 · `ార` 0.99 · `␣జీ` 0.02 · `వ` 0.97 · `న` 0.90 · `␣సో` 0.06 · `ప` 1.00 · `న` 1.4e-3✱ · `ము` 0.61 · `న` 0.07✱ · `ందు` 0.05✱ · `ని` 5.1e-3✱ · `తి` 1.4e-3✱ · `ను` 1.3e-3✱ · `ము` 1.4e-3✱ · `ను` 8.8e-4✱ · `ము` 1.6e-3✱ · `న` 0.05✱ · `ము` 0.03✱ · `ను` 0.06✱ · `ము` 0.18✱ · `⏎` 0.48 forced |
| 2 | `త` 0.21 · `ల్లి` 0.76 · `␣దీ` 0.11 · `వె` 0.97 · `న` 1.00 · `␣తే` 5.8e-3 · `జ` 0.96 · `మై` 4.2e-3✱ · `క` 7.8e-4✱ · `్` 5.0e-8✱ · `␣` 9.8e-5✱ · `ల్లు` 4.8e-7✱ · `న` 0.19 · `␣ని` 0.21 · `లి` 0.37 · `చె` 0.60 · `ను` 0.83 · `␣స` 0.03 · `త్య` 0.68 · `ము` 0.25 · `న` 0.38 · `ందు` 0.50 · `ని` 0.55 · `తి` 0.89 · `న` 1.2e-3✱ · `్` 3.4e-7✱ · `␣` 1.7e-5✱ · `త` 1.4e-3✱ · `్య` 9.0e-5✱ · `జ` 0.99 · `ించ` 0.38 · `⏎` 4.3e-6 forced |
| 3 | `త` 0.69 · `ల్లి` 0.84 · `␣ఒ` 0.09 · `డి` 0.99 · `న` 4.1e-3✱ · `␣సు` 0.11 · `ఖ` 0.72 · `ము` 0.52 · `న` 0.08✱ · `్` 1.3e-6✱ · `␣` 4.7e-3✱ · `ల్ల` 2.7e-3✱ · `ె` 0.38 · `ను` 0.42 · `␣ని` 0.19 · `త్య` 0.25 · `ము` 0.66 · `న` 0.65 · `ందు` 0.52 · `ని` 0.65 · `తి` 0.89 · `ను` 0.69 · `ము` 0.76 · `న` 0.44 · `ము` 0.71 · `న` 0.36✱ · `్` 6.9e-5✱ · `␣ద` 0.01✱ · `య` 0.14✱ · `ము` 0.03✱ · `న` 0.56 · `⏎` 0.04 forced |
| 4 | `త` 0.88 · `ల్లి` 0.91 · `␣క` 0.26 · `రుణ` 0.97 · `␣ర` 0.03✱ · `క్ష` 0.31 · `మై` 0.15 · `క` 0.44 · `్` 0.95 · `␣` 0.73 · `ల్లు` 0.87 · `న` 0.81 · `␣ని` 0.74 · `లి` 0.77 · `చె` 0.92 · `ను` 0.98 · `␣జగ` 0.39 · `తి` 0.90 · `లో` 0.16 · `న` 0.85 · `ందు` 0.57 · `ని` 0.94 · `తి` 0.97 · `␣` 3.1e-5✱ · `గ` 4.0e-4✱ · `మ` 0.34 · `ము` 0.04✱ · `న` 0.83 · `ము` 0.04✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 121 tokens · 34.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతికెల్లాటినంతటిది సుమాతమానమున సతయేన | `UIUIIIIUUIUIIIIUIUIIIIIUI` |
| 2 | తల్లి కరుణ హృదయాన్ ల్లున నిత్యం నిలిచెను మాతృభలేన స్మృచెదుమున ప్రి | `UIIIIIIUIIUUIIIIUIIUIIIIIII` |
| 3 | మాయావిధి కదా జగమ్ యుగమున మాతృదైవమున స్థిరమునై వెలసిన | `UUIIIUIUIIIIUIUIIIIIIUIIII` |
| 4 | అనగనగాటి అనునియించున మదిలోన మరువనిది తల్లి స్మృమతినిన శు | `IIIIUIIIIUIIIIUIIIIIIUIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 43% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.059 · model's first choice kept 44% · constraint overrode 36% · backtracks 30

<details><summary>Token probabilities (121 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.75 · `ల్లి` 0.83 · `␣ప్రేమ` 0.78 · `␣జగ` 0.23✱ · `తి` 0.95 · `కె` 0.03 · `ల్` 0.45 · `లా` 0.97 · `టి` 0.07✱ · `న` 0.04 · `ంత` 0.07 · `టి` 0.52 · `ది` 0.19 · `␣సు` 0.02✱ · `మా` 0.62 · `త` 6.4e-4✱ · `మా` 0.03✱ · `న` 1.7e-4✱ · `ము` 0.07✱ · `న` 0.01✱ · `␣స` 1.5e-4✱ · `త` 0.03✱ · `యే` 7.3e-3✱ · `న` 0.17✱ · `⏎` 0.56 forced |
| 2 | `త` 0.22 · `ల్లి` 0.70 · `␣క` 0.29 · `రుణ` 0.95 · `␣హ` 5.1e-3✱ · `ృ` 0.96 · `దయ` 0.83 · `ాన` 0.67 · `్` 1.1e-7✱ · `␣` 5.6e-7✱ · `ల్లు` 9.2e-5✱ · `న` 0.24 · `␣ని` 0.49 · `త్య` 0.40 · `ం` 0.22 · `␣ని` 0.23 · `లి` 0.53 · `చె` 0.31✱ · `ను` 0.74 · `␣మ` 0.08 · `ాత` 0.42 · `ృ` 0.89 · `భ` 0.20 · `లే` 4.8e-4✱ · `న` 0.88 · `␣స్` 4.8e-3✱ · `మ` 0.31 · `ృ` 0.02✱ · `చె` 2.5e-5✱ · `దు` 0.10 · `ము` 0.52 · `న` 0.12✱ · `␣ప్రి` 2.0e-4✱ · `⏎` 3.3e-6 forced |
| 3 | `మ` 0.05 · `ాయ` 0.08✱ · `ా` 0.30 · `వి` 0.06 · `ధి` 0.10✱ · `␣క` 0.10✱ · `దా` 0.12 · `␣జగ` 0.37 · `మ` 0.27✱ · `్` 1.6e-8✱ · `␣` 4.1e-4✱ · `యు` 4.0e-5✱ · `గ` 0.69 · `ము` 0.16 · `న` 0.52 · `␣మ` 0.30 · `ాత` 0.66 · `ృ` 0.97 · `ద` 0.13 · `ై` 0.93 · `వ` 0.62 · `ము` 0.76 · `న` 0.47 · `␣స్థ` 0.02 · `ి` 0.71 · `ర` 0.91 · `ము` 0.50 · `న` 0.45 · `ై` 6.1e-3✱ · `␣వె` 0.02✱ · `ల` 0.52 · `సిన` 0.34 · `⏎` 0.12 forced |
| 4 | `అ` 0.18 · `న` 0.23 · `గ` 2.6e-4✱ · `న` 0.99 · `గా` 1.00 · `టి` 0.14 · `␣అను` 0.03 · `ని` 2.4e-6✱ · `య` 0.09 · `ించు` 0.11 · `న` 0.14 · `␣మ` 0.07✱ · `ది` 0.10✱ · `లో` 0.57 · `న` 0.80 · `␣మ` 0.41 · `రు` 0.03✱ · `వ` 0.92 · `ని` 0.17 · `ది` 0.13 · `␣తల్లి` 0.34 · `␣స్` 0.02✱ · `మ` 0.22✱ · `ృ` 0.03✱ · `మ` 2.1e-5✱ · `తి` 0.04 · `ని` 0.18 · `న` 0.05✱ · `␣శు` 0.03✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 118 tokens · 19.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాతృ ప్రేమ నిను జగమ్ తోడు పోషించును దయగానముగానము ధరముంచు | `UIUIIIIUUIUUIIIIUIIUIIIIUI` |
| 2 | తల్లి చూపుల వెలుగుల్లు తీరని దీపమున నిలిచెను మమత నిలుచున్న | `UIUIIIIUIUIIUIIIIIIIIIIIIUI` |
| 3 | అమ్మ ఒడిని చేరినంత్ మ్మతియే శాశ్వతమున నిత్యమున వెలుమెరుచున్న | `UIIIIUIUIIUUIIIIUIIIIIIIUI` |
| 4 | తల్లి అనుగ్రహమున్ ల్లా తలపొఇన్చి నూతనత్వమున నవ్యమ్ తరంచు | `UIIUIIUUIIIUIUIUIIIUUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 37% · single-akshara words 3% · repeated lines 0 · mean token probability (geometric) 0.035 · model's first choice kept 42% · constraint overrode 34% · backtracks 0

<details><summary>Token probabilities (118 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.15 · `త` 0.98 · `ృ` 0.99 · `␣ప్రేమ` 0.31 · `␣ని` 0.04✱ · `ను` 5.1e-4✱ · `␣జగ` 0.11 · `మ` 0.07✱ · `్` 7.3e-10✱ · `␣తో` 4.7e-5✱ · `డు` 0.51 · `␣పో` 0.02 · `ష` 0.64 · `ించు` 0.95 · `ను` 0.41 · `␣ద` 6.2e-3✱ · `య` 0.05✱ · `గా` 0.34 · `న` 3.3e-3✱ · `ము` 0.01✱ · `గా` 5.6e-3✱ · `న` 2.7e-3✱ · `ము` 0.04✱ · `␣` 9.2e-5✱ · `ధ` 1.3e-5✱ · `ర` 0.02✱ · `ము` 0.06✱ · `ంచు` 0.02 · `⏎` 0.04 forced |
| 2 | `త` 0.57 · `ల్లి` 0.87 · `␣చూపు` 0.10 · `ల` 0.35 · `␣వె` 0.37 · `లుగు` 0.79 · `ల` 0.04✱ · `్` 9.8e-9✱ · `లు` 0.21 · `␣తీ` 0.14 · `ర` 0.41 · `ని` 0.94 · `␣దీ` 0.17 · `ప` 0.86 · `ము` 0.34 · `న` 0.12✱ · `␣ని` 0.22 · `లి` 0.14 · `చె` 0.77 · `ను` 0.93 · `␣మ` 0.06 · `మ` 0.38 · `త` 0.74 · `␣ని` 0.04✱ · `లు` 9.6e-3✱ · `చు` 0.73 · `న్న` 5.7e-3 · `⏎` 0.06 forced |
| 3 | `అ` 0.26 · `మ్మ` 0.58 · `␣ఒ` 0.39 · `డి` 1.00 · `ని` 0.01✱ · `␣చే` 0.05 · `రి` 0.83 · `న` 0.56 · `ంత` 0.01✱ · `్` 1.3e-8✱ · `␣మ` 7.3e-5✱ · `్` 8.8e-7✱ · `మ` 0.90 · `తి` 0.07 · `యే` 0.13 · `␣శా` 0.14 · `శ్వ` 0.50 · `త` 0.98 · `ము` 0.35 · `న` 0.30 · `␣ని` 0.31 · `త్య` 0.25 · `ము` 0.67 · `న` 0.13 · `␣వె` 0.08 · `లు` 0.26 · `మె` 1.8e-4✱ · `రు` 0.10 · `చు` 0.80 · `న్న` 0.01✱ · `⏎` 0.99 forced |
| 4 | `త` 0.41 · `ల్లి` 0.87 · `␣అను` 0.17 · `గ్రహ` 0.13✱ · `ము` 0.56 · `న` 0.15✱ · `్` 1.5e-4✱ · `␣` 1.5e-4✱ · `ల్` 3.6e-6✱ · `లా` 0.17 · `␣త` 0.07 · `ల` 0.54 · `ప` 0.11 · `ొ` 0.02✱ · `ఇ` 0.02✱ · `న్` 0.20 · `చి` 0.19 · `␣న` 0.04 · `ూ` 0.22 · `తన` 0.36 · `త్వ` 0.03 · `ము` 0.91 · `న` 0.36 · `␣న` 0.36 · `వ్య` 0.07 · `మ` 0.10✱ · `్` 5.4e-9✱ · `␣` 1.8e-4✱ · `తర` 1.9e-6✱ · `ంచు` 0.03 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 120 tokens · 20.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీరామచంద్రుని రణ్ రూపము విచారమున హృదయం ద్రవమున నిలుంచు | `UUIUIIUUIIIUIIIIIUIIIIIUI` |
| 2 | సీతాదెవి రణోపగమ్ తన భద్రత కోరి లంక గమనం చేయ్ రచించు | `UUIIIUIUIIUIIUIUIIIUUIUI` |
| 3 | రావణుని బలం భయాన్ వహించి ధయిష్ఠిని ధరించి వినయమున దొరకొండు | `UIIIIUIUIUIIUIIIUIIIIIIIIUI` |
| 4 | ధర్మపథమున నడిచ్ ర్మున సత్యమును నిలబెట్టి శుభమును ప్రదరించ | `UIIIIIIUIIUIIIIIUIIIIIIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 32% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.059 · model's first choice kept 50% · constraint overrode 33% · backtracks 0

<details><summary>Token probabilities (120 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.18 · `్రీ` 0.98 · `రా` 0.85 · `మ` 0.52 · `చ` 0.91 · `ంద్ర` 0.99 · `ు` 0.78 · `ని` 0.99 · `␣ర` 0.34 · `ణ` 1.8e-3✱ · `్` 7.8e-6✱ · `␣రూప` 3.4e-7✱ · `ము` 0.62 · `␣వి` 0.02✱ · `చ` 0.73 · `ార` 0.90 · `ము` 0.02✱ · `న` 0.21✱ · `␣హ` 1.3e-3✱ · `ృ` 0.80 · `ద` 0.30 · `యం` 0.93 · `␣ద` 0.16✱ · `్ర` 0.26 · `వ` 0.91 · `ము` 0.24✱ · `న` 0.06✱ · `␣ని` 5.8e-3✱ · `లు` 0.05✱ · `ంచు` 2.4e-3 · `⏎` 0.25 forced |
| 2 | `సీ` 0.81 · `తా` 0.65 · `ద` 0.02✱ · `ె` 0.37 · `వి` 0.97 · `␣ర` 0.07 · `ణ` 2.5e-3✱ · `ో` 0.03 · `ప` 0.38 · `గ` 0.60 · `మ` 0.42✱ · `్` 1.3e-7✱ · `␣తన` 2.2e-4✱ · `␣భ` 0.19 · `ద్ర` 0.03 · `త` 0.78 · `␣కో` 0.22 · `రి` 0.90 · `␣ల` 0.30 · `ంక` 0.73 · `␣గ` 0.02 · `మ` 0.72 · `నం` 0.20✱ · `␣చేయ` 0.16 · `్` 1.4e-10✱ · `␣రచ` 8.8e-7✱ · `ించు` 0.87 · `⏎` 0.99 forced |
| 3 | `రా` 0.58 · `వ` 0.79 · `ణ` 0.73 · `ు` 0.20 · `ని` 0.99 · `␣బ` 0.05 · `లం` 0.72 · `␣భ` 0.04✱ · `య` 0.30✱ · `ాన` 0.13✱ · `్` 2.1e-11✱ · `␣వ` 7.9e-4✱ · `హ` 0.51 · `ించి` 0.66 · `␣ధ` 0.17 · `యి` 2.2e-3✱ · `ష్` 0.76 · `ఠ` 0.77 · `ి` 0.70 · `ని` 0.16✱ · `␣ధ` 0.09✱ · `రించి` 0.13✱ · `␣వి` 0.03 · `న` 0.22 · `య` 0.69 · `ము` 0.91 · `న` 0.55 · `␣ద` 5.3e-3✱ · `ొ` 0.01 · `ర` 0.27 · `కొ` 0.16 · `ండు` 0.03 · `⏎` 0.99 forced |
| 4 | `ధ` 0.10 · `ర్మ` 0.67 · `పథ` 0.06 · `ము` 0.43 · `న` 0.76 · `␣న` 0.19 · `డి` 0.28 · `చ` 0.07✱ · `్` 2.0e-8✱ · `␣` 4.0e-7✱ · `ర్` 6.5e-4✱ · `ము` 0.03✱ · `న` 0.20 · `␣స` 0.08 · `త్య` 0.81 · `ము` 0.58 · `ను` 0.44 · `␣ని` 0.23✱ · `ల` 0.64 · `బె` 0.74 · `ట్టి` 0.90 · `␣శు` 0.05 · `భ` 1.00 · `ము` 0.77 · `ను` 0.72 · `␣ప్ర` 0.11✱ · `ద` 0.11✱ · `రించ` 0.12✱ |

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

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 72 tokens · 11.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీకరుణ గల దినమున్ కైకలంబి ని | `UIIIIIIIUUIUII` |
| 2 | దుర్గమ పథమున వెలుగ్ ర్గమ జయ | `UIIIIIIIUIIII` |
| 3 | కరుణ గల దినమున కైకలంబి నివృత్తి | `IIIIIIIIIUIUIIUI` |
| 4 | భయమొకటి తొలగి జయె యుగమ జయ | `IIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 45% · single-akshara words 5% · repeated lines 0 · mean token probability (geometric) 0.068 · model's first choice kept 56% · constraint overrode 33% · backtracks 0

<details><summary>Token probabilities (72 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.15 · `్రీ` 0.90 · `క` 7.3e-3✱ · `రుణ` 0.03✱ · `␣గ` 7.8e-3✱ · `ల` 0.78 · `␣ద` 0.07✱ · `ిన` 1.1e-3✱ · `ము` 0.67 · `న` 0.77 · `్` 6.5e-6✱ · `␣క` 0.01✱ · `ై` 0.49 · `క` 0.29✱ · `ల` 0.58 · `ంబ` 0.09 · `ి` 0.31 · `␣ని` 0.04 · `⏎` 3.7e-6 forced |
| 2 | `దు` 0.02 · `ర్గ` 0.22 · `మ` 0.76 · `␣పథ` 0.06✱ · `ము` 0.63 · `న` 0.76 · `␣వె` 0.07✱ · `లు` 0.18✱ · `గ` 0.08✱ · `్` 3.6e-9✱ · `␣ర` 2.8e-5✱ · `్` 6.5e-10✱ · `గ` 4.5e-4✱ · `మ` 0.33 · `␣జ` 0.01 · `య` 0.49 · `⏎` 0.01 forced |
| 3 | `క` 0.05 · `రుణ` 0.11 · `␣గ` 6.8e-3✱ · `ల` 0.98 · `␣ద` 0.72 · `ిన` 0.99 · `ము` 0.97 · `న` 0.99 · `␣క` 0.07✱ · `ై` 0.84 · `క` 0.97 · `ల` 0.99 · `ంబ` 1.00 · `ి` 0.99 · `␣ని` 0.88 · `వ` 3.8e-4✱ · `ృ` 0.01✱ · `త్తి` 0.76 · `⏎` 0.94 forced |
| 4 | `భ` 0.10 · `య` 0.70 · `మ` 0.08 · `ొ` 0.24✱ · `క` 0.65 · `టి` 0.24 · `␣తొ` 0.24 · `ల` 1.00 · `గి` 0.64 · `␣జ` 0.13 · `య` 0.94 · `ె` 5.3e-3✱ · `␣యు` 1.7e-3✱ · `గ` 0.81 · `మ` 0.24 · `␣జ` 0.47 · `య` 0.97 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 51 tokens · 9.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాతృ ప్రేమ అమృతమంతటి గొప్పది | `UIUIIIIUIIUII` |
| 2 | తల్లి కరుణ జగతికిన్ ల్లి దారి | `UIIIIIIIUIUI` |
| 3 | ఆమె మమత జగతికిన్ మూలమైనది | `UIIIIIIIUUIUII` |
| 4 | ప్రేమయే నిరంతరం మనసున | `UIUIUIUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 44% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.110 · model's first choice kept 57% · constraint overrode 19% · backtracks 0

<details><summary>Token probabilities (51 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.16 · `త` 0.98 · `ృ` 0.99 · `␣ప్రేమ` 0.26✱ · `␣అమ` 0.10 · `ృత` 0.65 · `మ` 0.16 · `ంత` 0.64 · `టి` 0.63 · `␣గొప్ప` 0.37 · `ది` 0.73 · `⏎` 0.70 forced |
| 2 | `త` 0.37 · `ల్లి` 0.84 · `␣క` 0.24 · `రుణ` 0.84 · `␣జగ` 0.11 · `తి` 0.93 · `కి` 0.81 · `న` 7.9e-3✱ · `్` 1.8e-7✱ · `␣` 1.2e-5✱ · `ల్లి` 1.3e-6✱ · `␣ద` 0.05 · `ారి` 0.17 · `⏎` 0.81 forced |
| 3 | `ఆ` 0.27 · `మె` 0.11 · `␣మ` 0.07 · `మ` 0.97 · `త` 0.83 · `␣జగ` 0.05 · `తి` 0.69 · `కి` 0.61 · `న` 0.47 · `్` 0.83 · `␣మూ` 0.04✱ · `ల` 0.96 · `మైన` 0.06 · `ది` 0.98 · `⏎` 1.00 forced |
| 4 | `ప్ర` 0.05 · `ే` 0.99 · `మ` 0.95 · `యే` 0.16 · `␣ని` 0.02✱ · `ర` 8.6e-4✱ · `ంతరం` 0.30 · `␣మన` 0.07✱ · `సు` 0.12 · `న` 0.31 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 62 tokens · 16.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాతృ ప్రేమ అమృతమంత తీయదెదోయ | `UIUIIIIUIUIIUI` |
| 2 | అననులక మునుల కరుణ సుగంధ | `IIIIIIIIIIIIUI` |
| 3 | తల్లి కన్న ప్రేమ తండ్రి ప్రేమకలక | `UIUIUIUIUIIII` |
| 4 | తొలి స్ఫుటమున మదికి దొరికెను సఖ | `IIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 67% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.148 · model's first choice kept 48% · constraint overrode 29% · backtracks 8

<details><summary>Token probabilities (62 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.16 · `త` 0.98 · `ృ` 0.99 · `␣ప్రేమ` 0.26✱ · `␣అమ` 0.10 · `ృత` 0.61 · `మ` 0.17 · `ంత` 0.62 · `␣తీ` 9.2e-3 · `య` 0.97 · `ద` 0.21 · `ె` 0.06✱ · `ద` 0.11✱ · `ో` 0.77 · `య` 5.7e-3✱ · `⏎` 2.2e-3 forced |
| 2 | `అ` 0.14 · `న` 0.34 · `ను` 4.3e-4✱ · `ల` 0.12 · `క` 0.15 · `␣ము` 0.05 · `ను` 0.02✱ · `ల` 0.73 · `␣క` 0.07 · `రుణ` 0.95 · `␣సు` 0.01✱ · `గ` 0.35 · `ంధ` 0.99 · `⏎` 1.2e-5 forced |
| 3 | `త` 0.48 · `ల్లి` 0.87 · `␣క` 0.04 · `న్న` 0.69 · `␣ప్రేమ` 0.28 · `␣త` 0.18 · `ండ` 0.17 · `్రి` 0.75 · `␣ప్రేమ` 0.33 · `క` 0.65 · `ల` 3.8e-4✱ · `క` 0.52 · `⏎` 0.34 forced |
| 4 | `త` 0.23 · `ొ` 0.17 · `లి` 0.63 · `␣స్` 0.18✱ · `ఫ` 0.01✱ · `ు` 5.9e-3✱ · `ట` 0.76 · `ము` 0.03✱ · `న` 0.39 · `␣మ` 0.07 · `ది` 0.36 · `కి` 0.26 · `␣ద` 0.07✱ · `ొ` 0.08✱ · `రి` 0.80 · `కె` 0.40✱ · `ను` 0.45 · `␣స` 0.05✱ · `ఖ` 0.04✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 59 tokens · 25.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతికెల్లా సుగంధంబు | `UIUIIIIUUIUUI` |
| 2 | అమృత వానలెను నిను మురిపించు | `IIIUIIIIIIIUI` |
| 3 | మాతృ వాత్సలత్వముక్ తలపుల మధు | `UIUIUIUIIIIII` |
| 4 | కరుణ చినుకులెను నిను రగిలించు | `IIIIIIIIIIIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.083 · model's first choice kept 54% · constraint overrode 27% · backtracks 30

<details><summary>Token probabilities (59 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.72 · `ల్లి` 0.81 · `␣ప్రేమ` 0.82 · `␣జగ` 0.24 · `తి` 0.96 · `కె` 0.03 · `ల్` 0.42 · `లా` 0.98 · `␣సు` 0.20✱ · `గ` 0.47 · `ంధ` 0.99 · `ం` 0.26 · `బు` 0.02✱ · `⏎` 0.74 forced |
| 2 | `అ` 0.16 · `మ` 0.13 · `ృ` 0.12 · `త` 3.1e-3✱ · `␣వ` 0.02 · `ాన` 0.62 · `లె` 0.06 · `ను` 0.23 · `␣ని` 0.03✱ · `ను` 0.06✱ · `␣ము` 8.5e-3✱ · `రి` 0.04✱ · `ప` 0.97 · `ించు` 0.73 · `⏎` 0.28 forced |
| 3 | `మా` 0.04 · `త` 0.87 · `ృ` 0.99 · `␣వా` 0.28 · `త్స` 1.00 · `ల` 0.68 · `త్వ` 3.4e-5✱ · `ము` 0.66 · `క` 0.03✱ · `్` 4.1e-13✱ · `␣త` 6.3e-7✱ · `ల` 0.66 · `పు` 0.27 · `ల` 0.31 · `␣మ` 0.05✱ · `ధు` 0.76 · `⏎` 2.2e-6 forced |
| 4 | `క` 0.17 · `రుణ` 0.86 · `␣చి` 6.4e-3✱ · `ను` 0.47 · `కు` 0.74 · `లె` 0.33 · `ను` 0.97 · `␣ని` 0.19 · `ను` 0.57 · `␣ర` 0.01✱ · `గి` 5.0e-3✱ · `ల` 0.46 · `ించు` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 55 tokens · 4.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాతృ ప్రేమ కరుణయే తలమున నిలి | `UIUIIIIUIIIIII` |
| 2 | అనవసర మదిని అమృణుల రూప | `IIIIIIIIIIIIUI` |
| 3 | అన్నిటికనికై అరణ్ న్నదమున పరి | `UIIIIUIUIIIIII` |
| 4 | నిజని ప్రేమయే జగ జగతికి ద | `IIIUIUIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 44% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.035 · model's first choice kept 42% · constraint overrode 40% · backtracks 0

<details><summary>Token probabilities (55 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.16 · `త` 0.98 · `ృ` 0.99 · `␣ప్రేమ` 0.26✱ · `␣క` 0.01 · `రుణ` 0.72 · `యే` 0.10✱ · `␣త` 2.9e-3✱ · `ల` 0.77 · `ము` 0.44 · `న` 0.50 · `␣ని` 0.37 · `లి` 0.59 · `⏎` 3.0e-8 forced |
| 2 | `అ` 0.24 · `న` 0.42 · `వ` 3.6e-4✱ · `సర` 0.69 · `␣మ` 0.07✱ · `ది` 0.38 · `ని` 0.18✱ · `␣అమ` 6.6e-3✱ · `ృ` 0.47✱ · `ణ` 1.4e-8✱ · `ుల` 0.02✱ · `␣రూప` 0.05✱ · `⏎` 1.7e-4 forced |
| 3 | `అ` 0.08 · `న్ని` 0.05 · `టి` 0.76 · `క` 0.91 · `ని` 1.0e-4✱ · `క` 0.35 · `ై` 0.06✱ · `␣అ` 0.03✱ · `రణ` 0.02✱ · `్` 6.7e-6✱ · `␣న` 5.7e-7✱ · `్` 1.6e-8✱ · `న` 0.61 · `ద` 0.03 · `ము` 0.52 · `న` 0.51 · `␣పరి` 0.03 · `⏎` 0.02 forced |
| 4 | `ని` 0.06 · `జ` 0.03 · `ని` 0.03✱ · `␣ప్రేమ` 0.08 · `యే` 0.42 · `␣జగ` 0.26 · `␣జగ` 2.7e-5✱ · `తి` 0.82 · `కి` 0.54 · `␣ద` 0.06✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 63 tokens · 4.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీకరుణ గల దినమున్ కోరితి నిను ర | `UIIIIIIIUUIIIII` |
| 2 | తళలయ భయమున కదిలితిని దరి | `IIIIIIIIIIIIIII` |
| 3 | రణ్యలోకముల సుమిత్ ణ్యముల నిలచి | `UIUIIIIUIIIIII` |
| 4 | కరుణనుల దయ వలన రగిలితిని | `IIIIIIIIIIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 39% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.059 · model's first choice kept 38% · constraint overrode 38% · backtracks 0

<details><summary>Token probabilities (63 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.15 · `్రీ` 0.90 · `క` 7.3e-3✱ · `రుణ` 0.03✱ · `␣గ` 7.8e-3✱ · `ల` 0.78 · `␣ద` 0.07✱ · `ిన` 1.1e-3✱ · `ము` 0.67 · `న` 0.77 · `్` 6.5e-6✱ · `␣కో` 6.3e-3✱ · `రి` 0.44 · `తి` 0.26 · `␣ని` 0.04 · `ను` 0.17✱ · `␣ర` 0.31 · `⏎` 6.5e-7 forced |
| 2 | `త` 0.05 · `ళ` 0.02 · `ల` 0.04 · `య` 0.03 · `␣భ` 0.05 · `య` 0.51 · `ము` 0.77 · `న` 0.37 · `␣క` 0.06 · `ది` 0.08✱ · `లి` 0.42 · `తి` 0.81 · `ని` 0.23 · `␣ద` 0.03✱ · `రి` 0.09✱ · `⏎` 0.66 forced |
| 3 | `రణ` 0.04 · `్య` 0.50 · `లో` 0.06 · `క` 0.12 · `ముల` 0.12 · `␣సు` 0.02✱ · `మ` 0.38 · `ిత` 0.17✱ · `్` 5.1e-5✱ · `␣` 2.3e-5✱ · `ణ` 0.02✱ · `్య` 0.02✱ · `ముల` 0.02 · `␣ని` 0.06 · `ల` 0.18 · `చి` 0.37 · `⏎` 0.43 forced |
| 4 | `క` 0.10 · `రుణ` 0.36 · `ను` 3.9e-3✱ · `ల` 0.03✱ · `␣ద` 0.14 · `య` 0.12✱ · `␣వలన` 3.5e-3✱ · `␣ర` 0.15✱ · `గి` 2.3e-3✱ · `లి` 0.53 · `తి` 0.95 · `ని` 0.79 |

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

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 70 tokens · 11.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతికి మూలధ్ ల్లది కద | `UIUIIIIIUUIIII` |
| 2 | తల్లి దీవెనయే శాంతికిన్ ల్లది కద | `UIUIIUUIUIIII` |
| 3 | తల్లి కరుణయే లోకాన సుఖ్ ల్లది కద | `UIIIIUUUIUIIII` |
| 4 | తల్లి ప్రేమయే పరమేశ్వరిన్ ల్లది కద | `UIUIUIIUIUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 45% · single-akshara words 5% · repeated lines 0 · mean token probability (geometric) 0.129 · model's first choice kept 70% · constraint overrode 18% · backtracks 0

<details><summary>Token probabilities (70 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.68 · `ల్లి` 0.77 · `␣ప్రేమ` 0.81 · `␣జగ` 0.20 · `తి` 0.96 · `కి` 0.53 · `␣మూ` 0.14 · `ల` 0.94 · `ధ` 0.34 · `్` 6.1e-10✱ · `␣` 2.8e-10✱ · `ల్` 6.4e-5✱ · `ల` 1.5e-3✱ · `ది` 0.09 · `␣క` 0.02✱ · `ద` 0.08✱ · `⏎` 0.15 forced |
| 2 | `త` 0.31 · `ల్లి` 0.65 · `␣దీ` 0.11 · `వె` 0.99 · `న` 0.97 · `యే` 0.38 · `␣శా` 0.27 · `ంతి` 0.17 · `కి` 0.47 · `న` 1.6e-3✱ · `్` 1.4e-6✱ · `␣` 0.01✱ · `ల్` 0.20✱ · `ల` 0.89 · `ది` 0.75 · `␣క` 0.22 · `ద` 0.95 · `⏎` 1.00 forced |
| 3 | `త` 0.69 · `ల్లి` 0.89 · `␣క` 0.37 · `రుణ` 0.80 · `యే` 0.52 · `␣లో` 0.26 · `క` 0.94 · `ాన` 0.21 · `␣సు` 0.06 · `ఖ` 0.97 · `్` 5.6e-4✱ · `␣` 0.46 · `ల్` 0.99 · `ల` 0.98 · `ది` 0.98 · `␣క` 0.99 · `ద` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.97 · `ల్లి` 0.92 · `␣ప్రేమ` 0.15 · `యే` 0.74 · `␣పర` 0.11 · `మ` 0.72 · `ేశ` 0.20 · `్వ` 0.70 · `రి` 0.44 · `న` 0.18✱ · `్` 0.79 · `␣` 0.99 · `ల్` 1.00 · `ల` 1.00 · `ది` 1.00 · `␣క` 1.00 · `ద` 1.00 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 61 tokens · 10.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమయే జగతికి మూల్లమున మ | `UIUIUIIIIUIIII` |
| 2 | కరుణయే జగతికి ప్రాణము రెడలమున | `IIIUIIIIUIIIIIII` |
| 3 | నిస్వకలమైన ఆశ్రయంబున్ స్వరమున | `UIIIUIUIUUIIII` |
| 4 | అమృతధారవో తల్లి ప్రేమ మరువదున | `IIIUIUUIUIIIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 44% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.080 · model's first choice kept 59% · constraint overrode 19% · backtracks 0

<details><summary>Token probabilities (61 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.68 · `ల్లి` 0.77 · `␣ప్రేమ` 0.81 · `యే` 0.38 · `␣జగ` 0.65 · `తి` 0.95 · `కి` 0.81 · `␣మూ` 0.25 · `ల` 0.94 · `్` 8.0e-10✱ · `ల` 0.43 · `ము` 0.07 · `న` 0.30 · `␣మ` 0.01✱ · `⏎` 1.1e-5 forced |
| 2 | `క` 0.10 · `రుణ` 0.89 · `యే` 0.07✱ · `␣జగ` 0.14 · `తి` 0.81 · `కి` 0.80 · `␣ప్రా` 0.02 · `ణ` 0.94 · `ము` 0.45 · `␣రె` 1.3e-4✱ · `డ` 2.9e-3✱ · `ల` 0.21 · `ము` 0.25 · `న` 0.95 · `⏎` 0.35 forced |
| 3 | `ని` 0.09 · `స్` 0.61 · `వ` 0.98 · `క` 1.7e-5✱ · `ల` 0.93 · `మైన` 0.47 · `␣ఆ` 0.65 · `శ` 0.23 · `్ర` 0.75 · `యం` 0.35 · `బు` 0.22 · `న` 8.4e-3✱ · `్` 1.6e-6✱ · `␣స` 8.7e-4✱ · `్వర` 2.3e-8✱ · `ము` 0.78 · `న` 0.90 · `⏎` 0.99 forced |
| 4 | `అ` 0.09 · `మ` 0.20 · `ృత` 0.79 · `ధ` 0.42 · `ార` 0.99 · `వో` 0.04 · `␣తల్లి` 0.22 · `␣ప్రేమ` 0.24 · `␣మ` 0.02✱ · `రు` 0.18 · `వ` 0.92 · `దు` 0.24 · `న` 0.27 |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 75 tokens · 29.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | దశరథుని పుత్రుని ధయిష్ఠము శిరసా గ | `IIIIIUIIIUIIIIUI` |
| 2 | సీతకై వెళ్ళెను నరలోకాన్ తన గమ | `UIUUIIIIUUIIII` |
| 3 | రాక్షసుల భయమున భుజమున్ క్షయమున | `UIIIIIIIIIUIIII` |
| 4 | శరణము పొఇచ్చుట దయచేయు రఘునాథ | `IIIIIUIIIIUIIIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 44% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.082 · model's first choice kept 53% · constraint overrode 25% · backtracks 30

<details><summary>Token probabilities (75 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ద` 0.03 · `శ` 0.59 · `ర` 0.79 · `థ` 1.00 · `ు` 0.75 · `ని` 0.99 · `␣పు` 0.14 · `త్ర` 0.96 · `ు` 0.87 · `ని` 0.37 · `␣ధ` 0.07 · `యి` 7.5e-4✱ · `ష్` 0.62 · `ఠ` 0.90 · `ము` 0.42 · `␣శి` 7.0e-4✱ · `ర` 0.67 · `సా` 0.10 · `␣గ` 0.31✱ · `⏎` 1.6e-6 forced |
| 2 | `సీ` 0.42 · `త` 0.38✱ · `క` 8.4e-3✱ · `ై` 0.49 · `␣వె` 0.06 · `ళ్ళ` 0.43 · `ె` 0.95 · `ను` 0.89 · `␣న` 3.4e-3 · `ర` 0.85 · `లో` 0.02 · `క` 0.94 · `ాన` 0.09✱ · `్` 6.5e-6✱ · `␣తన` 8.6e-5✱ · `␣గ` 0.01 · `మ` 0.92 · `⏎` 1.2e-4 forced |
| 3 | `రా` 0.60 · `క్ష` 0.34 · `స` 0.90 · `ుల` 0.12 · `␣భ` 0.15 · `య` 0.58 · `ము` 0.89 · `న` 0.32 · `␣భ` 0.04 · `ు` 0.22 · `జ` 0.93 · `ము` 0.60 · `న` 0.28 · `్` 1.8e-6✱ · `␣క` 2.1e-3✱ · `్` 2.0e-8✱ · `ష` 8.2e-3✱ · `య` 0.30✱ · `ము` 0.58 · `న` 0.16 · `⏎` 0.35 forced |
| 4 | `శ` 0.09 · `రణ` 0.16 · `ము` 0.22 · `␣పొ` 0.09✱ · `ఇ` 1.8e-5✱ · `చ్చు` 0.17 · `ట` 0.23 · `␣ద` 9.4e-3✱ · `య` 0.01✱ · `చే` 0.35 · `యు` 0.42 · `␣ర` 5.5e-3✱ · `ఘ` 0.44 · `ు` 0.98 · `నా` 0.15 · `థ` 0.98 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 65 tokens · 26.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమయే జగతికి దైవసేన | `UIUIUIIIIUIUI` |
| 2 | తల్లి కరుణే జగతికి ప్రాణోద్ ల్లనామ | `UIIIUIIIIUUIUI` |
| 3 | తల్లి ఒడియే సుఖముల సొంత స్థలమున స్త | `UIIIUIIIIUIIIIII` |
| 4 | తల్లి దీవెనయే లోకమున్ ల్లకలము | `UIUIIUUIUIIII` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 42% · single-akshara words 5% · repeated lines 0 · mean token probability (geometric) 0.048 · model's first choice kept 57% · constraint overrode 24% · backtracks 30

<details><summary>Token probabilities (65 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.68 · `ల్లి` 0.77 · `␣ప్రేమ` 0.83 · `యే` 0.38 · `␣జగ` 0.64 · `తి` 0.94 · `కి` 0.79 · `␣ద` 0.05 · `ై` 0.98 · `వ` 0.92 · `సే` 2.7e-3 · `న` 0.88 · `⏎` 0.41 forced |
| 2 | `త` 0.34 · `ల్లి` 0.50 · `␣క` 0.31 · `రుణ` 0.95 · `ే` 0.25 · `␣జగ` 0.23 · `తి` 0.83 · `కి` 0.89 · `␣ప్రా` 0.03 · `ణ` 0.99 · `ో` 9.7e-3✱ · `ద` 0.60 · `్` 8.9e-13✱ · `␣ల` 4.4e-13✱ · `్` 1.6e-9✱ · `ల` 0.08✱ · `నా` 0.07✱ · `మ` 1.0e-3✱ · `⏎` 0.99 forced |
| 3 | `త` 0.89 · `ల్లి` 0.92 · `␣ఒ` 0.13 · `డి` 0.99 · `యే` 0.59 · `␣సు` 0.15✱ · `ఖ` 0.98 · `ముల` 0.10 · `␣సొ` 0.04 · `ంత` 0.89 · `␣స్థ` 0.18 · `ల` 0.06✱ · `ము` 0.68 · `న` 0.13✱ · `␣` 2.1e-5✱ · `స్త` 0.06✱ · `⏎` 7.6e-6 forced |
| 4 | `త` 0.96 · `ల్లి` 0.91 · `␣దీ` 0.24 · `వె` 0.97 · `న` 0.89 · `యే` 0.82 · `␣లో` 0.07 · `క` 0.96 · `ము` 0.14 · `న` 0.63 · `్` 2.3e-6✱ · `␣` 8.5e-4✱ · `ల్ల` 1.2e-4✱ · `క` 0.06 · `ల` 0.29 · `ము` 0.24 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 60 tokens · 11.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమ జగతికి మూలధ్ ల్లిది జగ | `UIUIIIIIUUIIII` |
| 2 | అమ్మ ప్రేమ అమృతము నిత్య సఖిని జగ | `UIUIIIIIUIIIIII` |
| 3 | తల్లి కరుణా వలయము నిత్య సుఖదాయ | `UIIIUIIIIUIIIUI` |
| 4 | ప్రేమతోనే జగతి జీవనాన్ మధుర్య | `UIUUIIIUIUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 62% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.064 · model's first choice kept 58% · constraint overrode 21% · backtracks 0

<details><summary>Token probabilities (60 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.68 · `ల్లి` 0.77 · `␣ప్రేమ` 0.81 · `␣జగ` 0.20 · `తి` 0.96 · `కి` 0.53 · `␣మూ` 0.14 · `ల` 0.94 · `ధ` 0.34 · `్` 6.1e-10✱ · `␣` 2.8e-10✱ · `ల్` 6.4e-5✱ · `లి` 4.3e-4✱ · `ది` 0.03✱ · `␣జగ` 2.7e-3✱ · `⏎` 1.1e-5 forced |
| 2 | `అ` 0.26 · `మ్మ` 0.41 · `␣ప్రేమ` 0.17 · `␣అమ` 0.14 · `ృత` 0.66 · `ము` 0.17 · `␣ని` 0.25 · `త్య` 0.65 · `␣స` 0.08 · `ఖ` 3.1e-3✱ · `ి` 0.54 · `ని` 0.41 · `␣జగ` 0.05✱ · `⏎` 0.91 forced |
| 3 | `త` 0.47 · `ల్లి` 0.83 · `␣క` 0.23 · `రుణ` 0.92 · `ా` 0.38 · `␣వ` 0.16 · `ల` 0.67 · `య` 0.27 · `ము` 0.72 · `␣ని` 0.09 · `త్య` 0.59 · `␣సు` 0.08 · `ఖ` 0.50 · `దాయ` 0.01 · `⏎` 0.27 forced |
| 4 | `ప్ర` 0.06 · `ే` 0.95 · `మ` 0.95 · `తో` 0.07 · `నే` 0.47 · `␣జగ` 0.58 · `తి` 0.56 · `␣జీ` 0.04 · `వ` 0.86 · `న` 0.57 · `ాన` 9.7e-3✱ · `్` 6.3e-7✱ · `␣మ` 0.01✱ · `ధు` 0.11✱ · `ర్య` 0.04 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 55 tokens · 8.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి ప్రేమయే జగతికి మూల్లమైన | `UIUIUIIIIUIUI` |
| 2 | తల్లి ప్రేమయే జగతికి నిండ్ ల్లమైన | `UIUIUIIIIUIUI` |
| 3 | తల్లి దీవెనయే జీవితానికి వర | `UIUIIUUIUIIII` |
| 4 | తల్లి మమతయే మరువనిదిజ్ ల్లమైన | `UIIIIUIIIIUIUI` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 41% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.063 · model's first choice kept 62% · constraint overrode 17% · backtracks 0

<details><summary>Token probabilities (55 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.68 · `ల్లి` 0.77 · `␣ప్రేమ` 0.81 · `యే` 0.38 · `␣జగ` 0.65 · `తి` 0.95 · `కి` 0.81 · `␣మూ` 0.25 · `ల` 0.94 · `్` 8.0e-10✱ · `ల` 0.43 · `మైన` 0.02 · `⏎` 2.9e-3 forced |
| 2 | `త` 0.39 · `ల్లి` 0.14 · `␣ప్రేమ` 0.05 · `యే` 0.81 · `␣జగ` 0.75 · `తి` 0.99 · `కి` 0.93 · `␣ని` 0.03 · `ండ` 0.03✱ · `్` 1.4e-7✱ · `␣ల` 2.3e-8✱ · `్` 9.0e-6✱ · `ల` 0.80 · `మైన` 0.70 · `⏎` 1.00 forced |
| 3 | `త` 0.78 · `ల్లి` 0.92 · `␣దీ` 0.04 · `వె` 0.98 · `న` 0.95 · `యే` 0.68 · `␣జీవిత` 0.03 · `ానికి` 0.43 · `␣వర` 0.01✱ · `⏎` 1.1e-4 forced |
| 4 | `త` 0.99 · `ల్లి` 0.94 · `␣మ` 0.03 · `మ` 0.91 · `త` 0.94 · `యే` 0.93 · `␣మ` 0.12 · `రు` 0.36 · `వ` 0.95 · `ని` 0.05 · `ది` 0.04 · `జ` 1.5e-4✱ · `్` 1.5e-6✱ · `␣ల` 9.3e-4✱ · `్` 0.90 · `ల` 0.99 · `మైన` 0.83 |

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

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 122 tokens · 19.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి మదిల్యెను తల్లి ప్రేమ సుధోదయంబున నిల్యెనున్ | `IIIUIIUIUIIUIUIIUIU` |
| 2 | తొలి స్వరాలెను తల్గునుల్యెను త్యోహరాలెనునై నిలిచ్ | `IIIUIIUIUIIUIUIIUIU` |
| 3 | తొలి కరుణ్యెను తల్గునుల్యెను త్యోహరాలెనునై నిలిచ్ | `IIIUIIUIUIIUIUIIUIU` |
| 4 | తొలి అనుగ్రహమే తలవ్రును వ్ర్ఞ్ధుల్యెనున్ మదినిన్న్న్నొకై | `IIIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.056 · model's first choice kept 52% · constraint overrode 45% · backtracks 0

<details><summary>Token probabilities (122 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ొ` 2.6e-3✱ · `లి` 0.71 · `␣మ` 0.06✱ · `ది` 0.67 · `ల` 1.8e-3✱ · `్య` 5.1e-6✱ · `ె` 0.10✱ · `ను` 0.13✱ · `␣తల్లి` 0.38 · `␣ప్రేమ` 0.50 · `␣సు` 0.05 · `ధ` 0.01✱ · `ో` 4.9e-3✱ · `ద` 0.49 · `యం` 0.78 · `బు` 0.03✱ · `న` 0.04✱ · `␣ని` 2.9e-4✱ · `ల` 0.13✱ · `్య` 2.0e-7✱ · `ె` 0.84 · `ను` 0.70 · `న` 4.6e-4✱ · `్` 1.5e-7✱ · `⏎` 0.94 forced |
| 2 | `త` 0.31 · `ొ` 0.02✱ · `లి` 0.82 · `␣స్` 0.01✱ · `వర` 0.05✱ · `ాల` 0.04✱ · `ె` 0.51 · `ను` 0.67 · `␣త` 0.22 · `ల్` 0.60 · `గు` 1.5e-4✱ · `ను` 0.06 · `ల` 0.03✱ · `్య` 8.1e-7✱ · `ె` 0.72 · `ను` 0.52 · `␣త` 0.48 · `్య` 0.02✱ · `ో` 5.8e-4✱ · `హ` 0.73 · `ర` 0.32 · `ాల` 0.12✱ · `ె` 0.53 · `ను` 0.80 · `న` 0.06 · `ై` 0.05✱ · `␣ని` 0.39 · `లి` 0.49 · `చ` 0.01✱ · `్` 1.2e-10✱ · `⏎` 3.5e-3 forced |
| 3 | `త` 0.88 · `ొ` 0.67 · `లి` 0.94 · `␣క` 0.08✱ · `రుణ` 0.46 · `్య` 9.3e-3✱ · `ె` 0.31✱ · `ను` 0.88 · `␣త` 0.85 · `ల్` 0.89 · `గు` 0.53 · `ను` 0.48 · `ల` 0.95 · `్య` 0.96 · `ె` 1.00 · `ను` 1.00 · `␣త` 0.94 · `్య` 0.19 · `ో` 0.75 · `హ` 0.97 · `ర` 0.99 · `ాల` 1.00 · `ె` 0.99 · `ను` 0.99 · `న` 0.96 · `ై` 0.96 · `␣ని` 0.21 · `లి` 0.66 · `చ` 0.49 · `్` 0.95 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ొ` 0.97 · `లి` 0.99 · `␣అను` 0.08✱ · `గ్రహ` 0.02✱ · `మే` 0.24✱ · `␣త` 0.44 · `ల` 1.0e-2✱ · `వ` 0.02✱ · `్రు` 3.0e-5✱ · `ను` 0.32 · `␣వ` 8.9e-4✱ · `్ర` 2.6e-3✱ · `్ఞ` 4.4e-8✱ · `్` 1.3e-3✱ · `ధ` 0.06✱ · `ుల` 0.78 · `్య` 0.15✱ · `ె` 0.98 · `ను` 0.95 · `న` 0.77 · `్` 3.7e-4✱ · `␣మ` 0.06 · `ది` 0.25 · `ని` 0.13 · `న` 0.06✱ · `్` 0.03✱ · `న` 7.1e-3✱ · `్` 0.11✱ · `న్` 6.2e-4✱ · `న` 4.4e-4✱ · `ొ` 4.6e-3✱ · `క` 0.25✱ · `ై` 0.14✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 130 tokens · 22.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి మమత్రు తలప్యునత్యెను మ్ర్య్దూరమున్రవణమ్మునిన్ | `IIIUIIUIUIIUIUIIUIU` |
| 2 | తొలి దయత్రు తలప్యునత్యెను మ్ర్య్దూరమున్రవణమ్మునిన్ | `IIIUIIUIUIIUIUIIUIU` |
| 3 | తొలి అనుర్వ్రు తలప్యునత్యెను మ్ర్య్దూరమున్రవణమ్మునిన్ | `IIIUIIUIUIIUIUIIUIU` |
| 4 | తొలి కరుణ్రు తలప్యునత్యెను మ్ర్య్దూరమున్రవణమ్మునిన్ | `IIIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.265 · model's first choice kept 77% · constraint overrode 21% · backtracks 0

<details><summary>Token probabilities (130 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ొ` 2.6e-3✱ · `లి` 0.71 · `␣మ` 0.06✱ · `మ` 0.17 · `త` 0.82 · `్రు` 4.6e-6✱ · `␣త` 0.20✱ · `ల` 0.37 · `ప` 0.02✱ · `్య` 7.7e-5✱ · `ు` 0.22✱ · `న` 0.11 · `త` 7.5e-3✱ · `్య` 1.5e-3✱ · `ె` 0.08 · `ను` 0.22 · `␣మ` 0.12 · `్ర` 7.1e-5✱ · `్య` 1.5e-4✱ · `్` 4.4e-4✱ · `ద` 0.06✱ · `ూ` 0.20 · `ర` 0.82 · `ము` 0.46 · `న` 0.08✱ · `్ర` 1.4e-4✱ · `వ` 8.1e-3✱ · `ణ` 0.11✱ · `మ్ము` 4.6e-3✱ · `ని` 5.6e-3✱ · `న్` 3.2e-4✱ · `⏎` 0.99 forced |
| 2 | `త` 0.63 · `ొ` 5.2e-3✱ · `లి` 0.80 · `␣ద` 0.03 · `య` 0.66 · `త` 0.03✱ · `్రు` 0.64 · `␣త` 0.76 · `ల` 0.88 · `ప` 0.86 · `్య` 0.99 · `ు` 0.98 · `న` 0.95 · `త` 0.96 · `్య` 0.99 · `ె` 0.98 · `ను` 0.99 · `␣మ` 0.63 · `్ర` 0.92 · `్య` 1.00 · `్` 0.99 · `ద` 1.00 · `ూ` 1.00 · `ర` 1.00 · `ము` 0.96 · `న` 0.98 · `్ర` 0.91 · `వ` 0.99 · `ణ` 1.00 · `మ్ము` 1.00 · `ని` 1.00 · `న్` 1.00 · `⏎` 0.99 forced |
| 3 | `త` 0.87 · `ొ` 0.34✱ · `లి` 0.97 · `␣అను` 0.15✱ · `ర` 0.01✱ · `్వ` 2.0e-6✱ · `్రు` 0.49 · `␣త` 0.97 · `ల` 1.00 · `ప` 0.99 · `్య` 1.00 · `ు` 1.00 · `న` 0.98 · `త` 1.00 · `్య` 1.00 · `ె` 0.99 · `ను` 1.00 · `␣మ` 0.98 · `్ర` 1.00 · `్య` 1.00 · `్` 1.00 · `ద` 1.00 · `ూ` 1.00 · `ర` 1.00 · `ము` 0.99 · `న` 1.00 · `్ర` 0.99 · `వ` 1.00 · `ణ` 1.00 · `మ్ము` 1.00 · `ని` 1.00 · `న్` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.97 · `ొ` 0.99 · `లి` 1.00 · `␣క` 0.08✱ · `రుణ` 0.97 · `్రు` 0.74 · `␣త` 1.00 · `ల` 1.00 · `ప` 1.00 · `్య` 1.00 · `ు` 1.00 · `న` 1.00 · `త` 1.00 · `్య` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣మ` 1.00 · `్ర` 1.00 · `్య` 1.00 · `్` 1.00 · `ద` 1.00 · `ూ` 1.00 · `ర` 1.00 · `ము` 1.00 · `న` 1.00 · `్ర` 1.00 · `వ` 1.00 · `ణ` 1.00 · `మ్ము` 1.00 · `ని` 1.00 · `న్` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 120 tokens · 37.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి వెలుగ్యుని తల్రుమక్యుని తుల్యమున్యుని తల్రుమక్ | `IIIUIIUIUIIUIUIIUIU` |
| 2 | తొలి అనుగ్రహమున్రు తల్రుమొదొన్రు తుల్యమునక్యునిత్ | `IIIUIIUIUIIUIUIIUIU` |
| 3 | తొలి దయారమునత్రు తల్రుమొదొన్రు తుల్యమునక్యునిత్ | `IIIUIIUIUIIUIUIIUIU` |
| 4 | తొలి మమత్యుని తల్రుమక్యుని తుల్యమున్యునితగ్నితగ్ | `IIIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 24% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.165 · model's first choice kept 67% · constraint overrode 30% · backtracks 30

<details><summary>Token probabilities (120 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ొ` 2.6e-3✱ · `లి` 0.69 · `␣వె` 9.9e-3✱ · `లు` 0.03✱ · `గ` 0.57 · `్య` 2.9e-4✱ · `ు` 0.15✱ · `ని` 0.72 · `␣త` 0.19 · `ల` 0.70 · `్రు` 1.1e-5✱ · `మ` 0.02 · `క` 0.03 · `్య` 4.0e-4✱ · `ు` 0.35 · `ని` 0.88 · `␣త` 0.19 · `ుల` 0.04✱ · `్య` 0.74 · `ము` 0.51 · `న` 0.29✱ · `్య` 8.7e-5✱ · `ు` 0.30 · `ని` 0.53 · `␣త` 0.03✱ · `ల` 0.49 · `్రు` 0.10✱ · `మ` 0.79 · `క` 0.88 · `్` 2.6e-7✱ · `⏎` 0.63 forced |
| 2 | `త` 0.44 · `ొ` 5.4e-3✱ · `లి` 0.84 · `␣అను` 0.03✱ · `గ్రహ` 0.01✱ · `ము` 0.63 · `న` 0.28✱ · `్రు` 5.2e-5✱ · `␣త` 0.60 · `ల` 0.37 · `్రు` 0.65 · `మ` 0.94 · `ొ` 4.5e-5✱ · `ద` 0.02✱ · `ొ` 6.3e-4✱ · `న` 0.34 · `్రు` 0.46 · `␣త` 0.85 · `ుల` 0.34 · `్య` 0.97 · `ము` 0.90 · `న` 0.86 · `క్య` 2.0e-3✱ · `ు` 0.80 · `ని` 0.93 · `త` 6.7e-3✱ · `్` 9.1e-4✱ · `⏎` 0.77 forced |
| 3 | `త` 0.79 · `ొ` 0.02✱ · `లి` 0.89 · `␣ద` 0.02✱ · `య` 0.71 · `ార` 0.04✱ · `ము` 0.04✱ · `న` 0.84 · `త` 0.02✱ · `్రు` 0.02✱ · `␣త` 0.98 · `ల` 0.97 · `్రు` 0.99 · `మ` 0.91 · `ొ` 0.89 · `ద` 0.77 · `ొ` 0.92 · `న` 0.97 · `్రు` 0.97 · `␣త` 0.99 · `ుల` 1.00 · `్య` 1.00 · `ము` 0.99 · `న` 0.98 · `క్య` 0.87 · `ు` 0.98 · `ని` 0.96 · `త` 0.96 · `్` 0.99 · `⏎` 1.00 forced |
| 4 | `త` 0.95 · `ొ` 0.79 · `లి` 0.98 · `␣మ` 0.17✱ · `మ` 0.61 · `త` 0.85 · `్య` 0.26✱ · `ు` 0.92 · `ని` 0.82 · `␣త` 0.69 · `ల` 0.98 · `్రు` 1.00 · `మ` 0.98 · `క` 0.91 · `్య` 0.97 · `ు` 1.00 · `ని` 0.99 · `␣త` 0.96 · `ుల` 0.99 · `్య` 0.99 · `ము` 0.99 · `న` 0.98 · `్య` 0.85 · `ు` 1.00 · `ని` 0.99 · `త` 0.61 · `గ్` 9.0e-4✱ · `ని` 0.34✱ · `త` 0.57 · `గ్` 2.1e-3✱ |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 116 tokens · 38.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి కరుణ్య దయెందుకై పులదుత్రియేన సుమత్రమున్ | `IIIUIIUIUIIUIUIIUIU` |
| 2 | తొలి తలప్రము కద్రిచెద్యెన తుల్యమందున సత్యమమ్ | `IIIUIIUIUIIUIUIIUIU` |
| 3 | తొలి తలవ్రుతి నవ్వెనత్యెదెదోతరంబున సుమ్రమున్ | `IIIUIIUIUIIUIUIIUIU` |
| 4 | తొలి తలగ్రుడలెద్యెనత్యెదెదోతరంబున హృద్యమమ్ | `IIIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 24% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.066 · model's first choice kept 48% · constraint overrode 42% · backtracks 30

<details><summary>Token probabilities (116 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ొ` 2.6e-3✱ · `లి` 0.69 · `␣క` 0.02✱ · `రుణ` 0.15✱ · `్య` 3.2e-4✱ · `␣ద` 2.5e-3✱ · `య` 0.12✱ · `ె` 4.1e-3✱ · `ందు` 8.3e-4✱ · `క` 0.48 · `ై` 0.26 · `␣పు` 1.1e-3✱ · `ల` 0.01✱ · `దు` 1.4e-3✱ · `త` 2.7e-3✱ · `్రియ` 6.2e-4✱ · `ే` 0.64 · `న` 0.09✱ · `␣సు` 4.3e-3✱ · `మ` 0.67 · `త` 0.13✱ · `్ర` 1.2e-3✱ · `ము` 0.22✱ · `న` 0.05✱ · `్` 2.8e-7✱ · `⏎` 0.63 forced |
| 2 | `త` 0.45 · `ొ` 4.0e-3✱ · `లి` 0.77 · `␣త` 0.03✱ · `ల` 0.44 · `ప` 0.02✱ · `్ర` 5.0e-5✱ · `ము` 0.33 · `␣క` 0.02 · `ద` 0.03✱ · `్రి` 2.0e-4✱ · `చె` 0.35 · `ద` 0.08✱ · `్య` 5.8e-6✱ · `ె` 0.75 · `న` 0.16 · `␣త` 0.22 · `ుల` 0.06✱ · `్య` 0.61 · `మ` 0.22 · `ందు` 0.06 · `న` 0.32 · `␣స` 0.08 · `త్య` 0.62 · `మ` 0.23 · `మ్` 0.03 · `⏎` 0.95 forced |
| 3 | `త` 0.91 · `ొ` 0.81 · `లి` 0.92 · `␣త` 0.11 · `ల` 0.36 · `వ` 0.03✱ · `్రు` 5.6e-4✱ · `తి` 0.09 · `␣న` 0.06 · `వ` 0.05✱ · `్వ` 9.0e-5✱ · `ె` 0.06✱ · `న` 0.50 · `త` 5.7e-3✱ · `్య` 0.02✱ · `ె` 0.54 · `ద` 0.18 · `ె` 0.39 · `ద` 0.03✱ · `ో` 0.03✱ · `త` 0.02 · `రం` 0.03 · `బు` 0.38 · `న` 0.64 · `␣సు` 0.04 · `మ` 0.49 · `్ర` 0.03✱ · `ము` 0.70 · `న` 0.83 · `్` 0.43✱ · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ొ` 0.99 · `లి` 0.99 · `␣త` 0.51 · `ల` 0.83 · `గ` 0.03 · `్రు` 6.3e-3✱ · `డ` 0.39 · `ల` 0.02✱ · `ె` 0.04✱ · `ద` 0.21 · `్య` 0.02✱ · `ె` 0.91 · `న` 0.86 · `త` 0.03✱ · `్య` 0.13 · `ె` 0.83 · `ద` 0.89 · `ె` 0.55 · `ద` 0.92 · `ో` 0.93 · `త` 0.92 · `రం` 0.92 · `బు` 0.99 · `న` 0.97 · `␣హ` 0.07 · `ృ` 0.71 · `ద` 0.34✱ · `్య` 3.5e-5✱ · `మ` 0.89 · `మ్` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 100 tokens · 7.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి మదిల్యెను తల్లి ప్రేమ సుధోమయమ్యెను కద్రినా | `IIIUIIUIUIIUIUIIUIU` |
| 2 | నొలకరిన్రు నినుందు తల్లి కనుల్ర కీర్తిని చూచినా | `IIIUIIUIUIIUIUIIUIU` |
| 3 | తొలి పలుక్యెను తల్లి మాట దిదొన్న దైవదశమ్యనా | `IIIUIIUIUIIUIUIIUIU` |
| 4 | తొలగిపోవును ఎన్నడూ మది మ్ర్వ్ధుర్యమయ్యను కద్రినా | `IIIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 39% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.045 · model's first choice kept 39% · constraint overrode 52% · backtracks 0

<details><summary>Token probabilities (100 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ొ` 2.6e-3✱ · `లి` 0.71 · `␣మ` 0.06✱ · `ది` 0.67 · `ల` 1.8e-3✱ · `్య` 5.1e-6✱ · `ె` 0.10✱ · `ను` 0.13✱ · `␣తల్లి` 0.38 · `␣ప్రేమ` 0.50 · `␣సు` 0.05 · `ధ` 0.01✱ · `ో` 4.9e-3✱ · `మ` 0.23 · `య` 0.89 · `మ` 0.03✱ · `్య` 7.9e-4✱ · `ె` 0.51 · `ను` 0.14✱ · `␣క` 8.7e-4✱ · `ద` 0.09✱ · `్రి` 8.0e-5✱ · `నా` 9.2e-3✱ · `⏎` 0.93 forced |
| 2 | `న` 0.02 · `ొ` 0.03✱ · `ల` 0.07✱ · `క` 0.60 · `రి` 0.65 · `న` 0.25 · `్రు` 2.8e-6✱ · `␣ని` 0.08 · `ను` 0.22✱ · `ందు` 1.8e-3✱ · `␣తల్లి` 0.16 · `␣క` 0.28 · `ను` 3.1e-3✱ · `ల` 0.89 · `్ర` 7.6e-5✱ · `␣క` 0.19✱ · `ీ` 2.1e-3✱ · `ర్` 0.98 · `తి` 0.97 · `ని` 0.28 · `␣చూ` 0.09✱ · `చి` 0.62 · `నా` 0.06✱ · `⏎` 1.00 forced |
| 3 | `త` 0.19 · `ొ` 0.07✱ · `లి` 0.49 · `␣పలు` 0.05✱ · `క` 0.08✱ · `్య` 4.0e-4✱ · `ె` 0.76 · `ను` 0.83 · `␣తల్లి` 0.29 · `␣మాట` 0.19 · `␣ది` 0.05✱ · `ద` 8.7e-6✱ · `ొ` 5.1e-3✱ · `న్న` 0.02✱ · `␣ద` 0.14 · `ై` 0.70 · `వ` 0.96 · `ద` 0.03 · `శ` 0.08✱ · `మ` 0.21✱ · `్య` 0.78 · `నా` 7.3e-5 · `⏎` 1.00 forced |
| 4 | `త` 0.21 · `ొ` 0.06✱ · `ల` 0.36 · `గి` 0.06✱ · `పో` 0.20 · `వు` 0.63 · `ను` 0.25✱ · `␣ఎ` 0.03 · `న్న` 0.35 · `డ` 0.60 · `ూ` 0.94 · `␣మ` 0.02✱ · `ది` 0.15✱ · `␣మ` 0.01✱ · `్ర` 1.2e-3✱ · `్వ` 6.4e-7✱ · `్` 2.8e-4✱ · `ధు` 1.5e-3✱ · `ర` 0.51 · `్య` 1.3e-3✱ · `మ` 0.28 · `య` 0.10✱ · `్య` 0.03✱ · `ను` 0.02✱ · `␣క` 0.19 · `ద` 0.59 · `్రి` 0.99 · `నా` 1.00 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 120 tokens · 9.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవనసుత్త గమన్రతై లవ భవ్యమై లవణేన సా | `IIIUIIUIUIIUIUIIUIU` |
| 2 | వృవణమై తులకల్యుధే లఘురేశునియ్న లవణ్యమా | `IIIUIIUIUIIUIUIIUIU` |
| 3 | దెవతలందరినిచ్యు త్వం లవ భ్ర్మ్దెన్న లవ్యమునై సదా | `IIIUIIUIUIIUIUIIUIU` |
| 4 | చ్యువనమై గమనమ్ములై తుల ల్వ్న్యున్న లవ్యమునై హరీ | `IIIUIIUIUIIUIUIIUIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 23% · single-akshara words 9% · repeated lines 0 · mean token probability (geometric) 0.034 · model's first choice kept 31% · constraint overrode 56% · backtracks 0

<details><summary>Token probabilities (120 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.23 · `వ` 0.66 · `న` 0.99 · `సు` 0.30 · `త` 0.42✱ · `్` 3.8e-5✱ · `త` 0.92 · `␣గ` 0.04✱ · `మ` 0.47 · `న` 0.25✱ · `్ర` 1.8e-5✱ · `త` 0.07✱ · `ై` 0.04✱ · `␣ల` 0.84 · `వ` 1.5e-4✱ · `␣భ` 1.0e-4✱ · `వ` 0.08✱ · `్య` 2.7e-4✱ · `మై` 0.06 · `␣ల` 0.04✱ · `వ` 3.3e-4✱ · `ణ` 0.22✱ · `ే` 0.09✱ · `న` 0.17✱ · `␣సా` 0.01✱ · `⏎` 4.5e-4 forced |
| 2 | `వ` 0.09 · `ృ` 2.0e-4✱ · `వ` 2.6e-6✱ · `ణ` 0.08 · `మై` 0.05✱ · `␣త` 0.07 · `ుల` 0.09 · `క` 0.03✱ · `ల` 0.03 · `్య` 1.2e-3✱ · `ు` 0.18✱ · `ధ` 0.05 · `ే` 0.16✱ · `␣ల` 0.68 · `ఘ` 8.7e-4✱ · `ు` 0.97 · `ర` 0.15 · `ేశ` 2.0e-3✱ · `ు` 0.32 · `ని` 0.21 · `య` 3.6e-3✱ · `్` 0.01✱ · `న` 0.31 · `␣ల` 0.05✱ · `వ` 0.04✱ · `ణ` 0.43✱ · `్య` 6.2e-4✱ · `మా` 0.08✱ · `⏎` 1.00 forced |
| 3 | `ద` 0.04 · `ె` 8.2e-4✱ · `వ` 0.10✱ · `తల` 0.31 · `ంద` 0.01✱ · `రి` 0.60 · `ని` 0.24 · `చ` 1.3e-5✱ · `్య` 5.9e-3✱ · `ు` 0.41 · `␣త` 0.05 · `్వ` 0.10 · `ం` 0.32✱ · `␣ల` 0.13 · `వ` 5.2e-3✱ · `␣భ` 0.02✱ · `్ర` 2.2e-3✱ · `్` 2.7e-7✱ · `మ` 0.78 · `్` 2.7e-4✱ · `ద` 0.02✱ · `ె` 0.05✱ · `న` 0.51 · `్` 1.5e-4✱ · `న` 0.51 · `␣ల` 0.39 · `వ` 0.89 · `్య` 1.3e-3✱ · `ము` 0.08✱ · `న` 0.36 · `ై` 0.04✱ · `␣స` 0.02✱ · `దా` 0.21✱ · `⏎` 1.00 forced |
| 4 | `చ` 0.03 · `్య` 3.1e-3✱ · `ు` 0.91 · `వ` 3.3e-3✱ · `న` 0.19 · `మై` 0.32 · `␣గ` 0.06 · `మ` 0.85 · `న` 0.20✱ · `మ్ము` 0.01✱ · `ల` 0.02 · `ై` 0.15✱ · `␣త` 0.12 · `ుల` 0.30 · `␣ల` 6.3e-3✱ · `్వ` 2.8e-4✱ · `్` 0.01✱ · `న` 0.19 · `్య` 0.02✱ · `ు` 0.07✱ · `న` 0.13✱ · `్` 9.3e-3✱ · `న` 0.91 · `␣ల` 0.79 · `వ` 0.95 · `్య` 0.03✱ · `ము` 0.28 · `న` 0.65 · `ై` 0.93 · `␣హ` 0.04 · `రీ` 4.8e-3 |

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

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 122 tokens · 20.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి హృదయమునత్యుర్య్య్తొల్యునైతిర్యునిన్తిర్ | `IIIIIIUUUIUUIUU` |
| 2 | తొలి స్మరణమునత్యుర్య్య్తొల్యునైతిర్యునిన్తిర్ | `IIIIIIUUUIUUIUU` |
| 3 | తొలి అనురతిలోనత్యుర్య్య్తొలక్యున్యునిన్తిర్ | `IIIIIIUUUIUUIUU` |
| 4 | తొలి నిమలతలోనత్యుర్య్య్తొలక్యున్యునిన్తిర్ | `IIIIIIUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 50% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.214 · model's first choice kept 70% · constraint overrode 29% · backtracks 0

<details><summary>Token probabilities (122 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.82 · `ొ` 4.5e-3✱ · `లి` 0.68 · `␣హ` 0.01 · `ృ` 0.98 · `దయ` 0.65 · `ము` 0.11✱ · `న` 0.75 · `త` 1.6e-3✱ · `్య` 4.6e-5✱ · `ు` 0.04✱ · `ర` 0.14✱ · `్య` 4.9e-4✱ · `్య` 7.2e-4✱ · `్` 1.6e-4✱ · `త` 8.5e-3✱ · `ొ` 0.02✱ · `ల` 0.26✱ · `్య` 7.9e-3✱ · `ు` 0.30 · `న` 0.05✱ · `ై` 0.02✱ · `తి` 3.2e-3✱ · `ర` 1.5e-3✱ · `్య` 5.3e-3✱ · `ు` 0.18✱ · `ని` 0.04✱ · `న్` 1.1e-3✱ · `తి` 0.01✱ · `ర` 0.06✱ · `్` 2.3e-4✱ · `⏎` 0.51 forced |
| 2 | `త` 0.36 · `ొ` 4.7e-3✱ · `లి` 0.57 · `␣స్` 0.04 · `మ` 0.40✱ · `రణ` 0.66 · `ము` 0.46 · `న` 0.83 · `త` 0.46 · `్య` 0.93 · `ు` 0.97 · `ర` 0.98 · `్య` 0.99 · `్య` 0.99 · `్` 0.93 · `త` 0.98 · `ొ` 1.00 · `ల` 0.99 · `్య` 0.99 · `ు` 1.00 · `న` 0.98 · `ై` 1.00 · `తి` 0.99 · `ర` 1.00 · `్య` 1.00 · `ు` 1.00 · `ని` 0.99 · `న్` 0.99 · `తి` 0.99 · `ర` 1.00 · `్` 0.99 · `⏎` 0.98 forced |
| 3 | `త` 0.77 · `ొ` 0.27✱ · `లి` 0.90 · `␣అను` 0.12✱ · `ర` 0.01✱ · `తి` 0.44 · `లో` 0.09 · `న` 0.89 · `త` 0.94 · `్య` 0.99 · `ు` 0.99 · `ర` 1.00 · `్య` 1.00 · `్య` 1.00 · `్` 1.00 · `త` 1.00 · `ొ` 1.00 · `ల` 1.00 · `క్య` 8.0e-4✱ · `ు` 0.79 · `న` 0.47✱ · `్య` 3.5e-5✱ · `ు` 0.44 · `ని` 0.88 · `న్` 0.86 · `తి` 0.98 · `ర` 1.00 · `్` 0.99 · `⏎` 1.00 forced |
| 4 | `త` 0.96 · `ొ` 0.96 · `లి` 0.98 · `␣ని` 0.02✱ · `మ` 0.02✱ · `ల` 0.79 · `త` 0.25 · `లో` 0.27 · `న` 0.99 · `త` 1.00 · `్య` 1.00 · `ు` 1.00 · `ర` 1.00 · `్య` 1.00 · `్య` 1.00 · `్` 1.00 · `త` 1.00 · `ొ` 1.00 · `ల` 0.99 · `క్య` 0.40✱ · `ు` 0.99 · `న` 0.75 · `్య` 0.99 · `ు` 1.00 · `ని` 1.00 · `న్` 1.00 · `తి` 1.00 · `ర` 1.00 · `్` 1.00 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 98 tokens · 16.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి మదికి తలవ్రేల్య్న్దోని మాధుర్యమున్రో | `IIIIIIUUUIUUIUU` |
| 2 | అలసిన దినమున్నర్యన్నకల్యాణమున్రో | `IIIIIIUUUIUUIUU` |
| 3 | కలసిన కనులక్రాంత్య్న్కమ్యనన్మమ్రమున్రో | `IIIIIIUUUIUUIUU` |
| 4 | తొలగితి తలలక్రాంత్య్న్కూరనన్మమ్రమున్రో | `IIIIIIUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 20% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.089 · model's first choice kept 53% · constraint overrode 42% · backtracks 0

<details><summary>Token probabilities (98 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.82 · `ొ` 4.5e-3✱ · `లి` 0.68 · `␣మ` 0.07 · `ది` 0.62 · `కి` 0.12✱ · `␣త` 0.25✱ · `ల` 0.32✱ · `వ` 0.02✱ · `్రే` 1.1e-3✱ · `ల` 0.19✱ · `్య` 3.1e-4✱ · `్` 5.3e-4✱ · `న` 0.33 · `్` 1.4e-4✱ · `ద` 8.0e-3✱ · `ో` 0.14✱ · `ని` 0.03✱ · `␣మా` 0.02 · `ధు` 0.62 · `ర్య` 0.73 · `ము` 0.66 · `న` 0.12✱ · `్రో` 3.3e-4✱ · `⏎` 0.21 forced |
| 2 | `అ` 0.13 · `ల` 0.05✱ · `సిన` 0.62 · `␣ద` 0.13✱ · `ిన` 0.18✱ · `ము` 0.53 · `న` 0.76 · `్` 2.7e-7✱ · `న` 0.47 · `ర` 0.01✱ · `్య` 7.9e-4✱ · `న` 0.06✱ · `్` 3.3e-3✱ · `న` 0.50 · `క` 0.01✱ · `ల` 0.41 · `్యా` 0.07✱ · `ణ` 0.94 · `ము` 0.63 · `న` 0.52 · `్రో` 0.86 · `⏎` 1.00 forced |
| 3 | `క` 0.17 · `ల` 0.32✱ · `సిన` 0.20 · `␣క` 0.19 · `ను` 0.30 · `ల` 0.55 · `క` 0.46 · `్రా` 1.6e-3✱ · `ంత` 0.35✱ · `్య` 0.18✱ · `్` 0.13✱ · `న` 0.91 · `్` 6.4e-3✱ · `క` 4.0e-3✱ · `మ` 0.17✱ · `్య` 2.9e-3✱ · `న` 0.42 · `న్` 0.02✱ · `మ` 0.47 · `మ` 4.0e-3✱ · `్ర` 0.01✱ · `ము` 0.70 · `న` 0.98 · `్రో` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.24 · `ొ` 0.01✱ · `ల` 0.25 · `గి` 0.06 · `తి` 0.18 · `␣త` 0.26 · `ల` 0.41 · `ల` 0.03 · `క` 0.25 · `్రా` 0.06✱ · `ంత` 0.66 · `్య` 0.91 · `్` 0.97 · `న` 0.99 · `్` 0.81 · `క` 0.34 · `ూ` 9.3e-7✱ · `ర` 0.31 · `న` 0.33 · `న్` 0.74 · `మ` 0.22 · `మ` 0.47 · `్ర` 0.84 · `ము` 1.00 · `న` 1.00 · `్రో` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 78 tokens · 24.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రమణి దహన సంహారమ్యె మాయా భ్రమల్యా | `IIIIIIUUUIUUIUU` |
| 2 | రమణి దహన సంహారమ్యె లంకేశునియ్యా | `IIIIIIUUUIUUIUU` |
| 3 | రమణి దహన సంహారమ్యె సీతా రణధ్యా | `IIIIIIUUUIUUIUU` |
| 4 | రమణి దహన సంహారమ్యె రాముడ్రునియ్యా | `IIIIIIUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 56% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.248 · model's first choice kept 67% · constraint overrode 23% · backtracks 20

<details><summary>Token probabilities (78 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ర` 0.02✱ · `మ` 0.13✱ · `ణి` 0.02✱ · `␣ద` 0.03 · `హ` 6.3e-3✱ · `న` 0.38 · `␣సం` 0.03 · `హ` 0.95 · `ార` 0.92 · `మ` 0.01✱ · `్య` 9.1e-3✱ · `ె` 0.21✱ · `␣మ` 1.3e-3 · `ాయ` 0.17 · `ా` 0.30 · `␣భ` 9.9e-3 · `్రమ` 0.65 · `ల` 0.29 · `్యా` 1.7e-3✱ · `⏎` 0.85 forced |
| 2 | `ర` 0.03✱ · `మ` 0.02✱ · `ణి` 0.81 · `␣ద` 0.62 · `హ` 0.97 · `న` 0.99 · `␣సం` 0.98 · `హ` 1.00 · `ార` 0.99 · `మ` 0.98 · `్య` 1.00 · `ె` 1.00 · `␣ల` 0.37 · `ంక` 0.56 · `ేశ` 0.03✱ · `ు` 0.52 · `ని` 0.89 · `య` 0.03✱ · `్యా` 0.04✱ · `⏎` 1.00 forced |
| 3 | `ర` 0.77 · `మ` 0.97 · `ణి` 0.99 · `␣ద` 0.97 · `హ` 1.00 · `న` 1.00 · `␣సం` 1.00 · `హ` 1.00 · `ార` 1.00 · `మ` 1.00 · `్య` 1.00 · `ె` 1.00 · `␣సీ` 0.67 · `తా` 0.65 · `␣ర` 0.58 · `ణ` 4.7e-4✱ · `ధ` 0.03 · `్యా` 0.12✱ · `⏎` 0.96 forced |
| 4 | `ర` 0.93 · `మ` 1.00 · `ణి` 1.00 · `␣ద` 1.00 · `హ` 1.00 · `న` 1.00 · `␣సం` 1.00 · `హ` 1.00 · `ార` 1.00 · `మ` 1.00 · `్య` 1.00 · `ె` 1.00 · `␣రా` 0.09 · `ము` 0.92 · `డ` 0.08✱ · `్రు` 5.0e-3✱ · `ని` 0.06 · `య` 0.91 · `్యా` 1.00 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 89 tokens · 12.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి మధుర క్షణానా తుల్యమేతియ్నినై తో | `IIIIIIUUUIUUIUU` |
| 2 | తొలకరి మమతై నిత్యుడ్యె నిస్వార్థమాయే | `IIIIIIUUUIUUIUU` |
| 3 | తొలకరి తపనానా తుల్యమేతియ్నినై తో | `IIIIIIUUUIUUIUU` |
| 4 | తొలి మమతకలై నిత్యుడ్యె నిస్వార్థమాయే | `IIIIIIUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 29% · single-akshara words 12% · repeated lines 0 · mean token probability (geometric) 0.183 · model's first choice kept 56% · constraint overrode 31% · backtracks 25

<details><summary>Token probabilities (89 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.82 · `ొ` 4.5e-3✱ · `లి` 0.68 · `␣మ` 0.06 · `ధు` 0.04 · `ర` 0.72 · `␣క్ష` 6.1e-3✱ · `ణ` 0.81 · `ాన` 0.26✱ · `ా` 8.6e-4✱ · `␣త` 0.33✱ · `ుల` 7.2e-3✱ · `్య` 0.65 · `మే` 0.06 · `తి` 8.7e-3 · `య` 0.01✱ · `్` 5.6e-3✱ · `ని` 0.11✱ · `న` 7.8e-3✱ · `ై` 0.04✱ · `␣తో` 1.2e-3✱ · `⏎` 2.4e-4 forced |
| 2 | `త` 0.49 · `ొ` 4.6e-3✱ · `ల` 0.19 · `క` 0.16✱ · `రి` 0.42 · `␣మ` 0.09✱ · `మ` 0.54 · `త` 0.79 · `ై` 0.02✱ · `␣ని` 0.08 · `త్య` 0.61 · `ు` 4.9e-3✱ · `డ` 0.09✱ · `్య` 4.0e-3✱ · `ె` 0.10✱ · `␣ని` 0.03 · `స్` 0.04✱ · `వ` 0.66 · `ార్థ` 0.92 · `మ` 0.06 · `ాయ` 0.31 · `ే` 0.22 · `⏎` 0.11 forced |
| 3 | `త` 0.88 · `ొ` 0.01✱ · `ల` 0.40 · `క` 0.48 · `రి` 0.96 · `␣త` 0.30 · `ప` 0.25 · `న` 0.28✱ · `ాన` 0.12✱ · `ా` 0.63 · `␣త` 0.82 · `ుల` 0.51 · `్య` 0.96 · `మే` 0.75 · `తి` 0.91 · `య` 0.96 · `్` 0.97 · `ని` 0.94 · `న` 0.95 · `ై` 0.97 · `␣తో` 0.64 · `⏎` 1.00 forced |
| 4 | `త` 0.97 · `ొ` 0.73 · `లి` 0.20 · `␣మ` 0.54 · `మ` 0.29✱ · `త` 0.83 · `క` 0.02✱ · `ల` 0.01✱ · `ై` 0.29 · `␣ని` 0.76 · `త్య` 0.89 · `ు` 0.86 · `డ` 0.95 · `్య` 0.94 · `ె` 0.91 · `␣ని` 0.73 · `స్` 0.44 · `వ` 0.79 · `ార్థ` 0.98 · `మ` 0.97 · `ాయ` 1.00 · `ే` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 81 tokens · 13.1 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి స్మరితిని తల్లిద్రుభ్యమంతట్యమున్రో | `IIIIIIUUUIUUIUU` |
| 2 | నిలకడల నిరీక్షణ్నిన్రుమున్రో తలవ్రో | `IIIIIIUUUIUUIUU` |
| 3 | అలసిన హృదయానాంత్యమ్రతిన్రుమ్యమున్రో | `IIIIIIUUUIUUIUU` |
| 4 | అలయని అనురాగమ్ర్యమ్రుమున్రో తలవ్రో | `IIIIIIUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 9% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.057 · model's first choice kept 40% · constraint overrode 49% · backtracks 0

<details><summary>Token probabilities (81 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.82 · `ొ` 4.5e-3✱ · `లి` 0.68 · `␣స్` 0.04 · `మ` 0.04✱ · `రి` 0.03 · `తి` 0.07✱ · `ని` 0.14✱ · `␣తల్లి` 0.39 · `ద` 0.02✱ · `్రు` 3.7e-8✱ · `భ` 0.02 · `్య` 1.6e-3✱ · `మ` 0.16 · `ంత` 0.23 · `ట` 5.0e-3✱ · `్య` 4.6e-3✱ · `ము` 0.12 · `న` 0.08✱ · `్రో` 1.3e-4✱ · `⏎` 0.02 forced |
| 2 | `ని` 0.06 · `ల` 3.5e-3✱ · `క` 0.16 · `డ` 0.96 · `ల` 0.12✱ · `␣ని` 0.03✱ · `రీ` 0.05✱ · `క్షణ` 0.82 · `్` 1.3e-4✱ · `ని` 0.44 · `న` 0.03✱ · `్రు` 2.5e-3✱ · `ము` 0.15 · `న` 0.53 · `్రో` 2.5e-3✱ · `␣త` 0.08✱ · `ల` 0.41 · `వ` 0.07✱ · `్రో` 2.0e-3✱ · `⏎` 1.00 forced |
| 3 | `అ` 0.17 · `ల` 0.22 · `సిన` 0.65 · `␣హ` 0.05✱ · `ృ` 1.00 · `దయ` 0.82 · `ాన` 0.46 · `ా` 0.02✱ · `ంత` 0.06 · `్య` 4.1e-3✱ · `మ` 0.18✱ · `్ర` 2.8e-4✱ · `త` 0.27 · `ిన` 0.01✱ · `్రు` 0.06✱ · `మ` 0.02✱ · `్య` 9.9e-3✱ · `ము` 0.72 · `న` 0.86 · `్రో` 0.99 · `⏎` 1.00 forced |
| 4 | `అ` 0.25 · `ల` 0.03✱ · `య` 0.10 · `ని` 0.15 · `␣అను` 0.12✱ · `రా` 0.92 · `గ` 0.72 · `మ` 0.28✱ · `్ర` 2.6e-3✱ · `్య` 7.5e-5✱ · `మ` 0.18✱ · `్రు` 0.02✱ · `ము` 0.38 · `న` 0.98 · `్రో` 0.99 · `␣త` 0.21 · `ల` 0.92 · `వ` 0.95 · `్రో` 1.00 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 106 tokens · 7.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వనమున గమయించెన్ హ్ర్య్భైరవన్నై లవణ్యా | `IIIIIIUUUIUUIUU` |
| 2 | తొనకలకలయెన్ ఉద్గ్రుణ్యుడై లంకలోగే | `IIIIIIUUUIUUIUU` |
| 3 | శనకనమున గమ్యుం హ్ర్య్చైకృషోతై దహన్యా | `IIIIIIUUUIUUIUU` |
| 4 | సనకనమున గమ్యుం హ్ర్య్చైకృషోతై విజయ్యా | `IIIIIIUUUIUUIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 7% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.076 · model's first choice kept 51% · constraint overrode 32% · backtracks 0

<details><summary>Token probabilities (106 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.33 · `న` 1.3e-3✱ · `ము` 0.57 · `న` 0.31✱ · `␣గ` 0.11✱ · `మ` 0.71 · `య` 0.09✱ · `ించ` 0.11 · `ె` 0.99 · `న` 0.06✱ · `్` 5.2e-4✱ · `␣హ` 0.20 · `్ర` 1.4e-8✱ · `్య` 1.2e-7✱ · `్` 2.9e-5✱ · `భ` 1.5e-3✱ · `ై` 0.17 · `ర` 0.31 · `వ` 0.45 · `న` 0.05✱ · `్` 5.8e-4✱ · `న` 0.12✱ · `ై` 0.07✱ · `␣ల` 1.7e-3✱ · `వ` 1.9e-4✱ · `ణ` 0.95 · `్యా` 7.4e-4✱ · `⏎` 0.55 forced |
| 2 | `త` 0.04 · `ొ` 0.02✱ · `న` 3.0e-4✱ · `క` 0.31 · `ల` 0.07✱ · `క` 0.04 · `ల` 0.24 · `య` 0.04 · `ె` 0.42 · `న` 0.45 · `్` 0.44 · `␣ఉ` 0.06 · `ద్` 0.10✱ · `గ` 0.33 · `్రు` 7.6e-5✱ · `ణ` 0.08 · `్య` 0.30 · `ు` 0.11✱ · `డ` 0.07✱ · `ై` 0.65 · `␣ల` 0.40 · `ంక` 0.44 · `లో` 0.05 · `గే` 5.7e-3 · `⏎` 0.42 forced |
| 3 | `శ` 0.15 · `న` 0.01✱ · `క` 0.86 · `న` 0.08 · `ము` 0.12 · `న` 0.40 · `␣గ` 0.24 · `మ` 0.89 · `్య` 0.06✱ · `ు` 0.10 · `ం` 0.25 · `␣హ` 0.20✱ · `్ర` 0.01✱ · `్య` 0.63 · `్` 0.93 · `చ` 1.0e-4✱ · `ై` 0.36 · `క` 0.04 · `ృ` 0.07 · `ష` 0.11 · `ో` 0.35 · `త` 0.08 · `ై` 0.30 · `␣ద` 0.05 · `హ` 0.01✱ · `న` 0.37✱ · `్యా` 0.06✱ · `⏎` 1.00 forced |
| 4 | `స` 0.07 · `న` 7.4e-4✱ · `క` 0.19 · `న` 0.34 · `ము` 0.72 · `న` 0.94 · `␣గ` 0.77 · `మ` 0.97 · `్య` 0.71 · `ు` 0.93 · `ం` 0.98 · `␣హ` 0.56 · `్ర` 0.96 · `్య` 0.98 · `్` 0.95 · `చ` 0.92 · `ై` 0.98 · `క` 0.97 · `ృ` 0.93 · `ష` 0.97 · `ో` 0.99 · `త` 0.96 · `ై` 0.99 · `␣విజయ` 0.03 · `్యా` 0.33 |

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

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 158 tokens · 27.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లికరుణ్యము తల్యున తేజము గ్న్య్ధమ్మెన గమ్యము స్ర్వ్తమ్మెన నివ్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 2 | తల్లిపరాశ్రయె తల్యున తేజము గ్న్య్ధమ్మెన గమ్యము స్ర్వ్తమ్మెన నివ్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 3 | తల్లిఅనుగ్రహె తల్యున తేజము గ్న్య్ధమ్మెన గమ్యము స్ర్వ్తమ్మెన నివ్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 4 | తల్లిభగవ్రియె తల్యున తేజము గ్న్య్ధమ్మెన గమ్యము స్ర్వ్తమ్మెన నివ్ | `UIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 14% · repeated lines 0 · mean token probability (geometric) 0.285 · model's first choice kept 78% · constraint overrode 20% · backtracks 0

<details><summary>Token probabilities (158 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.78 · `ల్లి` 0.77 · `క` 0.03✱ · `రుణ` 0.74 · `్య` 2.6e-4✱ · `ము` 0.21✱ · `␣త` 0.15✱ · `ల` 0.75 · `్య` 3.2e-6✱ · `ు` 0.17 · `న` 0.18 · `␣తే` 0.12 · `జ` 0.82 · `ము` 0.39 · `␣గ` 0.02✱ · `్` 1.1e-5✱ · `న` 0.17✱ · `్య` 1.7e-4✱ · `్` 6.1e-6✱ · `ధ` 6.0e-4✱ · `మ్` 8.0e-3✱ · `మె` 0.10✱ · `న` 0.24 · `␣గ` 4.3e-4✱ · `మ` 0.14 · `్య` 0.85 · `ము` 0.67 · `␣స` 4.9e-4✱ · `్ర` 2.4e-3✱ · `్వ` 6.7e-5✱ · `్` 7.4e-4✱ · `త` 0.26✱ · `మ్` 0.68 · `మె` 0.29✱ · `న` 0.89 · `␣ని` 5.1e-3✱ · `వ` 0.09✱ · `్` 7.3e-5✱ · `⏎` 3.4e-4 forced |
| 2 | `త` 0.42 · `ల్లి` 0.87 · `ప` 0.24✱ · `రా` 0.06✱ · `శ` 0.10 · `్ర` 0.82 · `య` 0.76 · `ె` 3.0e-4✱ · `␣త` 0.42 · `ల` 0.73 · `్య` 0.43 · `ు` 0.86 · `న` 0.95 · `␣తే` 0.73 · `జ` 0.99 · `ము` 0.98 · `␣గ` 0.97 · `్` 0.99 · `న` 1.00 · `్య` 1.00 · `్` 1.00 · `ధ` 1.00 · `మ్` 1.00 · `మె` 1.00 · `న` 1.00 · `␣గ` 0.99 · `మ` 1.00 · `్య` 1.00 · `ము` 1.00 · `␣స` 0.99 · `్ర` 0.99 · `్వ` 0.99 · `్` 1.00 · `త` 1.00 · `మ్` 1.00 · `మె` 1.00 · `న` 1.00 · `␣ని` 0.99 · `వ` 0.99 · `్` 0.99 · `⏎` 0.97 forced |
| 3 | `త` 0.87 · `ల్లి` 0.94 · `అ` 0.15 · `ను` 0.75 · `గ్రహ` 0.12✱ · `ె` 0.12✱ · `␣త` 0.99 · `ల` 1.00 · `్య` 1.00 · `ు` 1.00 · `న` 1.00 · `␣తే` 1.00 · `జ` 1.00 · `ము` 1.00 · `␣గ` 1.00 · `్` 1.00 · `న` 1.00 · `్య` 1.00 · `్` 1.00 · `ధ` 1.00 · `మ్` 1.00 · `మె` 1.00 · `న` 1.00 · `␣గ` 1.00 · `మ` 1.00 · `్య` 1.00 · `ము` 1.00 · `␣స` 1.00 · `్ర` 1.00 · `్వ` 1.00 · `్` 1.00 · `త` 1.00 · `మ్` 1.00 · `మె` 1.00 · `న` 1.00 · `␣ని` 1.00 · `వ` 1.00 · `్` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ల్లి` 0.96 · `భ` 0.17✱ · `గ` 5.6e-4✱ · `వ` 0.62 · `్రియ` 1.8e-4✱ · `ె` 0.77 · `␣త` 1.00 · `ల` 1.00 · `్య` 1.00 · `ు` 1.00 · `న` 1.00 · `␣తే` 1.00 · `జ` 1.00 · `ము` 1.00 · `␣గ` 1.00 · `్` 1.00 · `న` 1.00 · `్య` 1.00 · `్` 1.00 · `ధ` 1.00 · `మ్` 1.00 · `మె` 1.00 · `న` 1.00 · `␣గ` 1.00 · `మ` 1.00 · `్య` 1.00 · `ము` 1.00 · `␣స` 1.00 · `్ర` 1.00 · `్వ` 1.00 · `్` 1.00 · `త` 1.00 · `మ్` 1.00 · `మె` 1.00 · `న` 1.00 · `␣ని` 1.00 · `వ` 1.00 · `్` 1.00 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 194 tokens · 34.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వాయుపుతృమ్యుని భగ్వతనియ్న లభయ్న కదమ్యెను ద్య్న్భయ్న త్వరిత్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 2 | గీయమునై నిలకృత్తమునై లభె ద్య్న్కృత్తమునై భవగీత్తమునై | `UIIUIIUIIUIIUIIUIIUIIU` |
| 3 | సాయిని చుట్టి రసమ్యుని ధైర్యము న్య్న్సమ్యెను ద్య్న్సమ్యెను త్వ్య్సమ్యెను త్వ్య్సమ్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 4 | శైయమునుండి గె ల్య్న్సమ్యెను ద్య్న్సమ్యెను త్వ్య్సమ్యెను త్వ్య్సమ్త్తముషైత్తమునై | `UIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 8% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.109 · model's first choice kept 56% · constraint overrode 36% · backtracks 0

<details><summary>Token probabilities (194 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.35 · `ాయ` 1.00 · `ు` 1.00 · `పు` 0.68 · `త` 0.10✱ · `ృ` 7.0e-5✱ · `మ` 0.65 · `్య` 2.2e-3✱ · `ు` 0.35 · `ని` 0.86 · `␣భ` 0.06✱ · `గ` 0.01✱ · `్వ` 5.4e-4✱ · `త` 0.17✱ · `ని` 0.06 · `య` 0.01✱ · `్` 5.6e-3✱ · `న` 0.58 · `␣ల` 0.06 · `భ` 3.5e-4✱ · `య` 0.04✱ · `్` 0.04✱ · `న` 0.55 · `␣క` 5.7e-3✱ · `ద` 0.02✱ · `మ` 0.27 · `్య` 0.21 · `ె` 0.14 · `ను` 0.37✱ · `␣ద` 1.4e-3✱ · `్య` 0.01✱ · `్` 2.3e-5✱ · `న` 0.65 · `్` 3.9e-4✱ · `భ` 1.6e-3✱ · `య` 0.10✱ · `్` 0.83 · `న` 0.92 · `␣త` 2.8e-3✱ · `్వ` 0.37 · `రి` 0.17✱ · `త` 0.83 · `్` 4.8e-3✱ · `⏎` 1.9e-3 forced |
| 2 | `గ` 0.08 · `ీ` 0.01✱ · `య` 5.1e-7✱ · `ము` 0.17 · `న` 0.38 · `ై` 0.02✱ · `␣ని` 0.02 · `ల` 0.09 · `క` 3.4e-3✱ · `ృత` 0.02✱ · `్` 0.07✱ · `త` 0.87 · `ము` 0.29 · `న` 0.33 · `ై` 0.01✱ · `␣ల` 0.43 · `భ` 2.2e-3✱ · `ె` 2.8e-3✱ · `␣ద` 1.4e-3✱ · `్య` 0.16✱ · `్` 0.62 · `న` 0.98 · `్` 0.89 · `క` 3.4e-3✱ · `ృత` 0.15✱ · `్` 0.96 · `త` 0.99 · `ము` 0.84 · `న` 0.89 · `ై` 0.98 · `␣భ` 0.07 · `వ` 0.15 · `గ` 1.8e-3✱ · `ీ` 0.01✱ · `త` 0.85 · `్` 0.84 · `త` 0.67 · `ము` 0.07✱ · `న` 0.69 · `ై` 0.98 · `⏎` 0.60 forced |
| 3 | `స` 0.22 · `ాయి` 1.9e-4✱ · `ని` 0.05 · `␣చ` 8.4e-3 · `ు` 0.16 · `ట్టి` 0.21 · `␣ర` 0.02 · `స` 0.02✱ · `మ` 0.14✱ · `్య` 0.32 · `ు` 0.15 · `ని` 0.76 · `␣ధ` 0.05 · `ై` 0.37 · `ర్య` 0.87 · `ము` 0.65 · `␣న` 8.7e-3✱ · `్య` 9.0e-3✱ · `్` 0.26✱ · `న` 0.94 · `్` 0.07✱ · `స` 0.01✱ · `మ` 0.66 · `్య` 0.74 · `ె` 0.35 · `ను` 0.97 · `␣ద` 0.17 · `్య` 0.92 · `్` 0.99 · `న` 0.99 · `్` 0.93 · `స` 0.84 · `మ` 0.98 · `్య` 0.99 · `ె` 0.95 · `ను` 0.99 · `␣త` 0.20 · `్వ` 0.83 · `్య` 4.1e-6✱ · `్` 0.58 · `స` 1.2e-3✱ · `మ` 0.95 · `్య` 0.99 · `ె` 0.99 · `ను` 0.99 · `␣త` 0.03✱ · `్వ` 0.72 · `్య` 0.04✱ · `్` 0.92 · `స` 0.54 · `మ` 0.94 · `్` 5.7e-5✱ · `⏎` 0.69 forced |
| 4 | `శ` 0.10✱ · `ై` 0.09✱ · `య` 1.3e-4✱ · `ము` 0.72 · `ను` 0.13 · `ండి` 2.8e-3✱ · `␣గ` 0.06✱ · `ె` 0.02✱ · `␣ల` 2.0e-5✱ · `్య` 1.1e-3✱ · `్` 0.77 · `న` 0.90 · `్` 0.33 · `స` 0.03✱ · `మ` 0.78 · `్య` 0.96 · `ె` 0.95 · `ను` 0.99 · `␣ద` 0.67 · `్య` 0.99 · `్` 0.99 · `న` 0.99 · `్` 0.97 · `స` 0.90 · `మ` 1.00 · `్య` 0.99 · `ె` 1.00 · `ను` 1.00 · `␣త` 0.68 · `్వ` 0.95 · `్య` 0.93 · `్` 1.00 · `స` 0.79 · `మ` 0.99 · `్య` 0.97 · `ె` 1.00 · `ను` 1.00 · `␣త` 0.75 · `్వ` 0.98 · `్య` 0.97 · `్` 0.99 · `స` 0.99 · `మ` 0.96 · `్` 0.74 · `త` 5.7e-3✱ · `్` 0.31 · `త` 0.40✱ · `ము` 0.38 · `ష` 7.0e-5✱ · `ై` 0.07✱ · `త` 4.4e-3✱ · `్` 0.95 · `త` 0.22✱ · `ము` 0.30 · `న` 0.05✱ · `ై` 0.99 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 127 tokens · 40.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి దయల్రు ఘుతర్న పవిత్ర వదన్ర దయస్రయతమ్మెను ఝం | `UIIUIIUIIUIIUIIUIIUIIU` |
| 2 | తల్లి మమత్రు ఘుతర్న పవిత్ర వదన్ర మమత్ర ద్యుతమ్మెను ఝం | `UIIUIIUIIUIIUIIUIIUIIU` |
| 3 | తల్లి అనుగ్రహు ఘ్న్ర్తర్న పవిత్ర వదన్ర అనుగ్రహు ద్యత్తమెనుం | `UIIUIIUIIUIIUIIUIIUIIU` |
| 4 | తల్లి భవన్రు ఘ్న్ర్తతర్న పవిత్ర వదన్ర భవన్రు ద్యతమ్మెను ఝం | `UIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 27% · single-akshara words 10% · repeated lines 0 · mean token probability (geometric) 0.118 · model's first choice kept 60% · constraint overrode 34% · backtracks 30

<details><summary>Token probabilities (127 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.78 · `ల్లి` 0.77 · `␣ద` 4.2e-3✱ · `య` 0.69 · `ల` 0.01✱ · `్రు` 9.1e-5✱ · `␣ఘ` 0.02✱ · `ు` 1.5e-4✱ · `తర` 1.0e-5✱ · `్` 1.6e-4✱ · `న` 0.52 · `␣ప` 0.02 · `విత` 0.03 · `్ర` 0.91 · `␣వ` 0.02 · `దన` 7.7e-3✱ · `్ర` 9.3e-4✱ · `␣ద` 0.03✱ · `య` 0.16✱ · `స` 5.2e-3✱ · `్ర` 0.30 · `య` 0.05✱ · `త` 2.5e-3✱ · `మ్` 0.02✱ · `మె` 0.01✱ · `ను` 0.01✱ · `␣` 6.9e-4✱ · `ఝ` 0.08✱ · `ం` 0.24 · `⏎` 0.69 forced |
| 2 | `త` 0.43 · `ల్లి` 0.87 · `␣మ` 0.07✱ · `మ` 0.93 · `త` 0.75 · `్రు` 6.1e-3✱ · `␣ఘ` 0.31 · `ు` 0.98 · `తర` 0.90 · `్` 0.98 · `న` 1.00 · `␣ప` 0.42 · `విత` 0.96 · `్ర` 1.00 · `␣వ` 0.23 · `దన` 0.95 · `్ర` 0.97 · `␣మ` 0.29 · `మ` 0.72 · `త` 0.68 · `్ర` 0.01✱ · `␣ద` 0.06 · `్య` 4.1e-3✱ · `ు` 0.10✱ · `త` 0.07✱ · `మ్` 0.15 · `మె` 0.97 · `ను` 0.99 · `␣` 0.95 · `ఝ` 0.99 · `ం` 1.00 · `⏎` 1.00 forced |
| 3 | `త` 0.92 · `ల్లి` 0.94 · `␣అను` 0.21 · `గ్రహ` 0.04✱ · `ు` 0.03✱ · `␣ఘ` 0.64 · `్` 9.5e-6✱ · `న` 0.32 · `్ర` 0.09✱ · `్` 4.7e-4✱ · `త` 0.06✱ · `ర్` 5.8e-3✱ · `న` 0.81 · `␣ప` 0.92 · `విత` 1.00 · `్ర` 1.00 · `␣వ` 0.82 · `దన` 0.96 · `్ర` 0.95 · `␣అను` 0.76 · `గ్రహ` 0.90 · `ు` 0.30 · `␣ద` 0.14 · `్య` 0.32 · `త` 0.03✱ · `్` 7.4e-6✱ · `త` 0.97 · `మె` 3.0e-4✱ · `ను` 1.00 · `ం` 4.8e-6✱ · `⏎` 0.11 forced |
| 4 | `త` 0.99 · `ల్లి` 0.97 · `␣భ` 0.03✱ · `వ` 0.02✱ · `న` 0.92 · `్రు` 0.13✱ · `␣ఘ` 0.98 · `్` 0.24 · `న` 0.96 · `్ర` 0.93 · `్` 0.97 · `త` 0.99 · `త` 1.0e-5✱ · `ర్` 0.95 · `న` 1.00 · `␣ప` 1.00 · `విత` 1.00 · `్ర` 1.00 · `␣వ` 0.90 · `దన` 0.99 · `్ర` 0.95 · `␣భ` 0.99 · `వ` 1.00 · `న` 0.96 · `్రు` 0.65 · `␣ద` 0.64 · `్య` 0.79 · `త` 0.81 · `మ్` 0.12✱ · `మె` 1.00 · `ను` 0.96 · `␣` 0.24✱ · `ఝ` 1.00 · `ం` 1.00 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 153 tokens · 42.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామచరణ్ శివరాముని రక్షయె భ్రమ్యుని గాంభరి వ్రత్యమునిన్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 2 | సీమల లోకమునీ సతయేన శృణీతిని నివ్రమెనే హృదయాన్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 3 | ప్రాముడెనై లొణనై లవణమ్యెన ల్వ్వ్నమ్యెన లంకన గ్వ్వ్నమ్యెన వ్రత్ | `UIIUIIUIIUIIUIIUIIUIIU` |
| 4 | భూమిని దాటెను భువ్యుని రక్ష్యుని ర్వ్వ్నుమ్యెన రణ్యుని ర్వ్వ్నుమ్యెన లవ్ | `UIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 7% · single-akshara words 7% · repeated lines 0 · mean token probability (geometric) 0.064 · model's first choice kept 47% · constraint overrode 41% · backtracks 30

<details><summary>Token probabilities (153 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.30 · `మ` 0.79 · `చ` 0.79 · `రణ` 2.5e-3✱ · `్` 4.7e-4✱ · `␣శి` 9.2e-3 · `వ` 0.69 · `రా` 9.5e-3✱ · `ము` 0.30 · `ని` 0.88 · `␣ర` 0.54 · `క్ష` 0.75 · `య` 2.4e-3✱ · `ె` 0.22✱ · `␣భ` 2.9e-3✱ · `్రమ` 0.08✱ · `్య` 3.7e-4✱ · `ు` 0.13 · `ని` 0.88 · `␣గా` 0.02✱ · `ం` 0.27 · `భ` 0.75 · `రి` 4.6e-3✱ · `␣వ` 1.2e-3✱ · `్ర` 0.01✱ · `త` 0.41 · `్య` 1.3e-4✱ · `ము` 0.11 · `ని` 0.20✱ · `న్` 3.2e-4✱ · `⏎` 0.98 forced |
| 2 | `సీ` 0.74 · `మ` 8.0e-5✱ · `ల` 0.27 · `␣లో` 0.03 · `క` 0.91 · `ము` 0.37✱ · `న` 0.82 · `ీ` 7.0e-5✱ · `␣స` 0.13✱ · `త` 0.23✱ · `యే` 0.02✱ · `న` 0.08 · `␣శ` 0.04 · `ృ` 1.7e-3✱ · `ణ` 7.2e-3✱ · `ీ` 0.53 · `తి` 0.09 · `ని` 0.15 · `␣ని` 0.04 · `వ` 0.21 · `్రమ` 1.1e-4✱ · `ె` 0.04✱ · `న` 0.16✱ · `ే` 2.7e-4✱ · `␣హ` 0.03 · `ృ` 0.41 · `దయ` 0.83 · `ాన` 8.9e-3✱ · `్` 2.7e-4✱ · `⏎` 0.88 forced |
| 3 | `ప` 0.08✱ · `్రా` 0.04✱ · `ము` 1.9e-3✱ · `డ` 0.48 · `ె` 0.27✱ · `న` 0.34 · `ై` 0.03✱ · `␣ల` 0.42 · `ొ` 1.3e-4✱ · `ణ` 0.03✱ · `న` 3.7e-3✱ · `ై` 0.04✱ · `␣ల` 0.58 · `వ` 2.9e-4✱ · `ణ` 0.87 · `మ` 0.04✱ · `్య` 0.07✱ · `ె` 0.08 · `న` 0.66 · `␣ల` 0.60 · `్వ` 8.3e-6✱ · `్వ` 9.9e-4✱ · `్` 6.4e-3✱ · `న` 0.20 · `మ` 0.17✱ · `్య` 0.82 · `ె` 0.75 · `న` 0.89 · `␣ల` 0.43 · `ంక` 0.36 · `న` 0.05 · `␣గ` 6.6e-3✱ · `్వ` 2.7e-5✱ · `్వ` 7.3e-3✱ · `్` 0.21✱ · `న` 0.78 · `మ` 0.34 · `్య` 0.95 · `ె` 0.78 · `న` 0.50 · `␣వ` 1.4e-3✱ · `్ర` 0.32 · `త` 0.87 · `్` 7.4e-4✱ · `⏎` 3.2e-3 forced |
| 4 | `భ` 0.08 · `ూ` 0.15✱ · `మి` 0.34 · `ని` 0.27 · `␣దా` 0.12 · `ట` 0.47 · `ె` 0.88 · `ను` 0.36 · `␣భ` 0.33 · `ు` 0.12✱ · `వ` 0.57 · `్య` 3.4e-5✱ · `ు` 0.08 · `ని` 0.94 · `␣ర` 0.06 · `క్ష` 0.66 · `్య` 0.36 · `ు` 0.20✱ · `ని` 0.53 · `␣ర` 0.06 · `్వ` 1.1e-4✱ · `్వ` 0.36 · `్` 0.70 · `న` 0.87 · `ు` 1.2e-4✱ · `మ` 0.01✱ · `్య` 0.98 · `ె` 0.98 · `న` 0.91 · `␣ర` 0.38 · `ణ` 0.31 · `్య` 0.34 · `ు` 0.85 · `ని` 0.90 · `␣ర` 0.02✱ · `్వ` 0.32 · `్వ` 0.72 · `్` 0.82 · `న` 0.96 · `ు` 4.1e-3✱ · `మ` 0.54 · `్య` 0.96 · `ె` 0.98 · `న` 0.85 · `␣ల` 0.03✱ · `వ` 0.04 · `్` 0.16✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 149 tokens · 11.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | అమ్మల ప్రేమ సు అమ్రుత తేజము ఘ్న్యం వలపున్రయ వ్ర్యంబుల తే | `UIIUIIUIIUIIUIIUIIUIIU` |
| 2 | తొమ్మిది దిన్యము న్య్య్ధుల్య కరుణ్యము న్య్య్ధుల్య నమస్స్యము న్య్య్ధుల్య దయే | `UIIUIIUIIUIIUIIUIIUIIU` |
| 3 | అమ్మల ఆశ్రయ మ్ర్య్యంత నిరంతర స్ర్య్యంబుల నిత్యమృ ద్య్య్ధల్య దయా | `UIIUIIUIIUIIUIIUIIUIIU` |
| 4 | అమ్మెల ఆదర వ్ర్య్యంత కరుణ్యము న్య్య్ధల్య నమస్స్యము న్య్య్ధల్య దయా | `UIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 27% · single-akshara words 9% · repeated lines 0 · mean token probability (geometric) 0.070 · model's first choice kept 48% · constraint overrode 40% · backtracks 0

<details><summary>Token probabilities (149 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `అ` 0.08 · `మ్మ` 0.58 · `ల` 0.04✱ · `␣ప్రేమ` 0.80 · `␣సు` 0.01✱ · `␣అమ` 2.0e-6✱ · `్రు` 1.9e-4✱ · `త` 0.81 · `␣తే` 0.11 · `జ` 0.79 · `ము` 0.40 · `␣ఘ` 7.7e-3✱ · `్` 8.7e-7✱ · `న` 0.87 · `్య` 1.7e-4✱ · `ం` 0.01✱ · `␣వ` 2.6e-3✱ · `ల` 0.35 · `పు` 0.17 · `న` 0.02✱ · `్ర` 2.4e-5✱ · `య` 0.07✱ · `␣వ` 6.0e-4✱ · `్ర` 0.01✱ · `్య` 5.3e-6✱ · `ం` 0.22✱ · `బు` 7.8e-3✱ · `ల` 0.01✱ · `␣తే` 9.9e-3✱ · `⏎` 2.0e-4 forced |
| 2 | `త` 0.51 · `ొ` 6.8e-3✱ · `మ్` 3.6e-3✱ · `మి` 0.98 · `ది` 0.96 · `␣ద` 0.05 · `ిన` 0.71 · `్య` 5.1e-5✱ · `ము` 0.35 · `␣న` 0.05✱ · `్య` 4.0e-5✱ · `్య` 7.6e-4✱ · `్` 2.5e-5✱ · `ధ` 1.1e-3✱ · `ుల` 0.04✱ · `్య` 0.01✱ · `␣క` 0.04 · `రుణ` 0.47 · `్య` 0.02✱ · `ము` 0.06✱ · `␣న` 0.05✱ · `్య` 0.02✱ · `్య` 0.81 · `్` 0.52 · `ధ` 0.79 · `ుల` 0.78 · `్య` 0.95 · `␣న` 0.04✱ · `మ` 0.18 · `స్` 0.06 · `స` 0.38 · `్య` 0.04 · `ము` 0.02✱ · `␣న` 0.07✱ · `్య` 0.72 · `్య` 0.98 · `్` 0.95 · `ధ` 0.95 · `ుల` 0.83 · `్య` 0.97 · `␣ద` 0.02✱ · `య` 0.06✱ · `ే` 4.4e-3✱ · `⏎` 0.97 forced |
| 3 | `అ` 0.13 · `మ్మ` 0.17✱ · `ల` 0.42 · `␣ఆ` 0.09 · `శ` 0.89 · `్ర` 0.21✱ · `య` 0.59 · `␣మ` 1.6e-3✱ · `్ర` 1.5e-3✱ · `్య` 1.4e-4✱ · `్య` 0.13 · `ంత` 0.02✱ · `␣ని` 0.08 · `ర` 0.03✱ · `ంత` 0.91 · `ర` 0.99 · `␣స` 0.18 · `్ర` 5.6e-3✱ · `్య` 2.6e-5✱ · `్య` 0.64 · `ం` 0.09✱ · `బు` 0.96 · `ల` 0.46 · `␣ని` 0.05 · `త్య` 0.60 · `మ` 0.04 · `ృ` 0.09 · `␣ద` 1.9e-4✱ · `్య` 0.13✱ · `్య` 0.28✱ · `్` 0.44 · `ధ` 0.80 · `ల` 0.07✱ · `్య` 0.85 · `␣ద` 0.09 · `యా` 5.9e-3 · `⏎` 0.48 forced |
| 4 | `అ` 0.40 · `మ్` 0.08 · `మె` 0.08✱ · `ల` 0.23✱ · `␣ఆ` 0.17 · `ద` 0.15 · `ర` 0.09✱ · `␣వ` 0.02 · `్ర` 0.22✱ · `్య` 0.85 · `్య` 0.92 · `ంత` 0.24 · `␣క` 0.03 · `రుణ` 0.72 · `్య` 0.66 · `ము` 0.66 · `␣న` 0.32✱ · `్య` 0.87 · `్య` 0.99 · `్` 0.99 · `ధ` 1.00 · `ల` 0.34✱ · `్య` 0.99 · `␣న` 0.34 · `మ` 0.91 · `స్` 0.88 · `స` 0.99 · `్య` 0.99 · `ము` 0.98 · `␣న` 0.83 · `్య` 0.99 · `్య` 1.00 · `్` 0.99 · `ధ` 1.00 · `ల` 0.70 · `్య` 0.99 · `␣ద` 0.38 · `యా` 9.9e-3 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 131 tokens · 8.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవ్వనశక్తి గిభర్యమునై గమ గ్వాన లభించెను హ్ర్య్వన్రతినా | `UIIUIIUIIUIIUIIUIIUIIU` |
| 2 | అవ్వనగమ్యమునై అగమించెను ల్వ్వ్యన్రతినా హను మ్యన్తిన చే | `UIIUIIUIIUIIUIIUIIUIIU` |
| 3 | కవ్వనశక్తి గిఖర్యమునై గమ గ్వాన లభించెను హ్ర్య్కన్రతినా | `UIIUIIUIIUIIUIIUIIUIIU` |
| 4 | అవ్వనగమ్యమునై అగమించెను ల్వ్యన్రతినా హను మ్యన్తిన చే | `UIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 8% · repeated lines 0 · mean token probability (geometric) 0.104 · model's first choice kept 67% · constraint overrode 26% · backtracks 0

<details><summary>Token probabilities (131 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.21 · `వ` 0.53 · `్వ` 2.0e-7✱ · `న` 0.26 · `శ` 0.04 · `క్తి` 0.73 · `␣గ` 0.03✱ · `ి` 1.0e-3✱ · `భ` 6.9e-6✱ · `ర` 4.2e-3✱ · `్య` 1.4e-3✱ · `ము` 0.60 · `న` 0.39 · `ై` 7.0e-3✱ · `␣గ` 0.24 · `మ` 0.78 · `␣గ` 4.0e-4✱ · `్వ` 4.0e-7✱ · `ాన` 0.22 · `␣ల` 0.15 · `భ` 1.2e-4✱ · `ించ` 0.54 · `ె` 0.99 · `ను` 0.84 · `␣హ` 1.1e-3✱ · `్ర` 4.6e-5✱ · `్య` 3.1e-6✱ · `్వ` 4.8e-5✱ · `న` 0.12✱ · `్ర` 4.3e-4✱ · `త` 0.02✱ · `ినా` 7.4e-3✱ · `⏎` 0.85 forced |
| 2 | `అ` 0.06 · `వ` 8.9e-3✱ · `్వ` 7.7e-4✱ · `న` 0.41 · `గ` 0.05 · `మ` 0.71 · `్య` 0.29 · `ము` 0.59 · `న` 0.31 · `ై` 0.65 · `␣అ` 0.14 · `గ` 0.05✱ · `మ` 0.95 · `ించ` 0.03✱ · `ె` 1.00 · `ను` 0.94 · `␣ల` 0.48 · `్వ` 7.2e-5✱ · `్వ` 2.0e-3✱ · `్య` 6.8e-4✱ · `న` 0.33 · `్ర` 0.03✱ · `త` 0.92 · `ినా` 0.91 · `␣హ` 0.14 · `ను` 0.60 · `␣మ` 2.3e-5✱ · `్య` 0.01✱ · `న్` 0.01 · `తి` 0.08 · `న` 0.11✱ · `␣చే` 2.5e-4✱ · `⏎` 1.1e-6 forced |
| 3 | `క` 0.04 · `వ` 0.31 · `్వ` 0.60 · `న` 0.93 · `శ` 0.40 · `క్తి` 0.90 · `␣గ` 0.71 · `ి` 0.91 · `ఖ` 3.0e-5✱ · `ర` 0.72 · `్య` 0.94 · `ము` 0.93 · `న` 0.97 · `ై` 0.98 · `␣గ` 0.76 · `మ` 0.98 · `␣గ` 0.91 · `్వ` 0.97 · `ాన` 0.98 · `␣ల` 0.87 · `భ` 0.97 · `ించ` 0.97 · `ె` 1.00 · `ను` 0.99 · `␣హ` 0.83 · `్ర` 0.96 · `్య` 0.97 · `్` 4.1e-4✱ · `క` 6.1e-4✱ · `న` 0.54 · `్ర` 0.80 · `త` 0.98 · `ినా` 1.00 · `⏎` 0.98 forced |
| 4 | `అ` 0.81 · `వ` 0.99 · `్వ` 0.98 · `న` 0.99 · `గ` 0.98 · `మ` 0.99 · `్య` 0.99 · `ము` 1.00 · `న` 1.00 · `ై` 1.00 · `␣అ` 0.98 · `గ` 0.98 · `మ` 0.99 · `ించ` 0.99 · `ె` 1.00 · `ను` 1.00 · `␣ల` 0.99 · `్వ` 0.96 · `్య` 0.21 · `న` 0.98 · `్ర` 1.00 · `త` 1.00 · `ినా` 1.00 · `␣హ` 0.98 · `ను` 0.99 · `␣మ` 0.94 · `్య` 0.98 · `న్` 0.99 · `తి` 0.99 · `న` 0.97 · `␣చే` 0.90 |

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

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 178 tokens · 46.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వనమళనై గమ గ్న్య్భై లఘు రూపము ధ్య్న్భై రథమున్యెను వల్యునమున్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 2 | శనకమునై గమ గ్న్య్భై లఘు రూపము ధ్య్న్భై రథమున్యెను వ్ర్య్నన్యెను వల్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 3 | పనకమునై గమ గ్న్య్భై లఘు రూపము ధ్య్న్భై రథమున్యెను వల్యునమున్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 4 | అనమయమై గమ గ్న్య్భై లఘు రూపము ధ్య్న్భై రథమున్యెను వ్ర్య్నన్యెను వల్ | `IIIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 35% · single-akshara words 29% · repeated lines 0 · mean token probability (geometric) 0.228 · model's first choice kept 71% · constraint overrode 22% · backtracks 0

<details><summary>Token probabilities (178 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.50 · `న` 5.2e-4✱ · `మ` 0.15 · `ళ` 0.03✱ · `న` 0.10✱ · `ై` 0.08 · `␣గ` 0.11✱ · `మ` 0.73 · `␣గ` 4.2e-4✱ · `్` 3.5e-7✱ · `న` 0.17 · `్య` 7.3e-5✱ · `్` 1.8e-3✱ · `భ` 1.4e-3✱ · `ై` 0.17✱ · `␣ల` 0.39 · `ఘ` 3.3e-4✱ · `ు` 0.97 · `␣రూప` 8.8e-3 · `ము` 0.40 · `␣ధ` 0.09✱ · `్య` 5.4e-3✱ · `్` 2.2e-6✱ · `న` 0.84 · `్` 1.2e-4✱ · `భ` 0.05✱ · `ై` 0.96 · `␣ర` 2.4e-3✱ · `థ` 0.15 · `ము` 0.42 · `న` 0.04✱ · `్య` 7.3e-4✱ · `ె` 0.11✱ · `ను` 0.15✱ · `␣వ` 8.3e-4✱ · `ల` 0.15 · `్య` 7.2e-3✱ · `ు` 0.15 · `న` 0.05✱ · `ము` 6.4e-3✱ · `న` 0.07✱ · `్` 3.0e-4✱ · `⏎` 0.53 forced |
| 2 | `శ` 0.13 · `న` 9.1e-3✱ · `క` 0.85 · `ము` 0.03 · `న` 0.62 · `ై` 0.45 · `␣గ` 0.39 · `మ` 0.98 · `␣గ` 0.85 · `్` 0.96 · `న` 0.99 · `్య` 1.00 · `్` 1.00 · `భ` 1.00 · `ై` 1.00 · `␣ల` 0.78 · `ఘ` 1.00 · `ు` 1.00 · `␣రూప` 0.92 · `ము` 1.00 · `␣ధ` 0.97 · `్య` 0.99 · `్` 1.00 · `న` 1.00 · `్` 1.00 · `భ` 1.00 · `ై` 1.00 · `␣ర` 0.32 · `థ` 0.99 · `ము` 1.00 · `న` 1.00 · `్య` 0.99 · `ె` 1.00 · `ను` 1.00 · `␣వ` 0.98 · `్ర` 7.8e-7✱ · `్య` 1.5e-3✱ · `్` 0.06✱ · `న` 0.61 · `న` 5.1e-3✱ · `్య` 2.1e-3✱ · `ె` 0.65 · `ను` 0.98 · `␣వ` 0.06✱ · `ల` 0.95 · `్` 2.6e-4✱ · `⏎` 0.29 forced |
| 3 | `ప` 0.15 · `న` 0.02✱ · `క` 0.23 · `ము` 0.57 · `న` 0.99 · `ై` 1.00 · `␣గ` 0.99 · `మ` 1.00 · `␣గ` 1.00 · `్` 1.00 · `న` 1.00 · `్య` 1.00 · `్` 1.00 · `భ` 1.00 · `ై` 1.00 · `␣ల` 0.99 · `ఘ` 1.00 · `ు` 1.00 · `␣రూప` 1.00 · `ము` 1.00 · `␣ధ` 1.00 · `్య` 1.00 · `్` 1.00 · `న` 1.00 · `్` 1.00 · `భ` 1.00 · `ై` 1.00 · `␣ర` 0.94 · `థ` 1.00 · `ము` 1.00 · `న` 1.00 · `్య` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣వ` 0.56 · `ల` 0.83 · `్య` 0.94 · `ు` 0.96 · `న` 0.97 · `ము` 0.96 · `న` 0.98 · `్` 0.93 · `⏎` 0.78 forced |
| 4 | `అ` 0.14 · `న` 0.49 · `మ` 0.04✱ · `య` 0.06 · `మై` 0.50 · `␣గ` 0.97 · `మ` 0.99 · `␣గ` 0.99 · `్` 1.00 · `న` 1.00 · `్య` 1.00 · `్` 1.00 · `భ` 1.00 · `ై` 1.00 · `␣ల` 0.98 · `ఘ` 1.00 · `ు` 1.00 · `␣రూప` 1.00 · `ము` 1.00 · `␣ధ` 1.00 · `్య` 1.00 · `్` 1.00 · `న` 1.00 · `్` 1.00 · `భ` 1.00 · `ై` 1.00 · `␣ర` 0.87 · `థ` 1.00 · `ము` 1.00 · `న` 0.99 · `్య` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣వ` 0.46 · `్ర` 0.07✱ · `్య` 0.96 · `్` 0.98 · `న` 0.98 · `న` 0.90 · `్య` 0.99 · `ె` 0.99 · `ను` 1.00 · `␣వ` 0.95 · `ల` 0.94 · `్` 0.96 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 171 tokens · 27.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వనమున తేలిక న్య్వన్యుని ధైర్యము ద్య్వజ్యుమునై లఘుబల్యమునై | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 2 | అనమల సంధుల త్వ్వ్యన్యుని గమ్యమునై ద్య్వజనయ్యుని స్ర్వ్యమ్యుని ప్రగ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 3 | సనమున తేలిక న్య్వ్జన్యుని ధైర్యము ద్య్వ్జన్యుని లఘ్య్యుని స్ర్వ్యమ్యుని ప్రగ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 4 | సనమున తేలిక న్య్వ్జన్యుని ధైర్యము ద్య్వ్జన్యుని గమ్యము న్య్వ్జన్యుని ప్రగ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 21% · single-akshara words 10% · repeated lines 0 · mean token probability (geometric) 0.143 · model's first choice kept 63% · constraint overrode 30% · backtracks 0

<details><summary>Token probabilities (171 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.50 · `న` 5.2e-4✱ · `ము` 0.47 · `న` 0.19✱ · `␣తే` 0.09 · `లి` 0.30 · `క` 0.79 · `␣న` 9.5e-3✱ · `్య` 9.3e-5✱ · `్వ` 3.2e-4✱ · `న` 0.76 · `్య` 8.0e-3✱ · `ు` 0.21 · `ని` 0.09✱ · `␣ధ` 0.02 · `ై` 0.68 · `ర్య` 0.79 · `ము` 0.80 · `␣ద` 7.6e-3✱ · `్య` 0.03✱ · `్వ` 1.2e-4✱ · `జ` 0.16 · `్య` 0.03✱ · `ు` 0.21✱ · `ము` 0.05 · `న` 0.09✱ · `ై` 3.7e-3✱ · `␣ల` 2.5e-3✱ · `ఘ` 1.3e-3✱ · `ు` 0.98 · `బ` 0.02✱ · `ల` 0.60 · `్య` 5.9e-4✱ · `ము` 0.89 · `న` 0.16✱ · `ై` 0.17✱ · `⏎` 0.76 forced |
| 2 | `అ` 0.08 · `న` 0.66 · `మ` 4.6e-3✱ · `ల` 0.09 · `␣సం` 0.02 · `ధ` 0.62 · `ుల` 0.07✱ · `␣త` 0.05✱ · `్వ` 0.18 · `్వ` 2.7e-5✱ · `్య` 1.3e-3✱ · `న` 0.09✱ · `్య` 0.06✱ · `ు` 0.71 · `ని` 0.78 · `␣గ` 0.13 · `మ` 0.78 · `్య` 0.76 · `ము` 0.96 · `న` 0.40 · `ై` 0.90 · `␣ద` 0.06 · `్య` 0.09✱ · `్వ` 0.79 · `జ` 0.93 · `న` 3.5e-3✱ · `య` 0.02✱ · `్య` 0.09✱ · `ు` 0.68 · `ని` 0.25 · `␣స` 0.05✱ · `్ర` 5.8e-4✱ · `్వ` 2.4e-5✱ · `్య` 0.28 · `మ` 0.03✱ · `్య` 0.27 · `ు` 0.87 · `ని` 0.45 · `␣ప్ర` 0.03✱ · `గ` 0.20✱ · `్` 2.2e-9✱ · `⏎` 1.2e-5 forced |
| 3 | `స` 0.24 · `న` 5.0e-5✱ · `ము` 0.13✱ · `న` 0.63 · `␣తే` 0.17 · `లి` 0.91 · `క` 0.99 · `␣న` 0.88 · `్య` 0.99 · `్వ` 0.99 · `్` 2.9e-7✱ · `జ` 8.4e-3✱ · `న` 0.52 · `్య` 0.95 · `ు` 1.00 · `ని` 0.99 · `␣ధ` 0.46 · `ై` 0.99 · `ర్య` 0.98 · `ము` 0.99 · `␣ద` 0.90 · `్య` 0.99 · `్వ` 0.98 · `్` 2.9e-7✱ · `జ` 0.93 · `న` 0.03✱ · `్య` 0.37✱ · `ు` 0.98 · `ని` 0.70 · `␣ల` 0.70 · `ఘ` 0.83 · `్య` 5.2e-3✱ · `్య` 0.13 · `ు` 0.87 · `ని` 0.84 · `␣స` 0.31 · `్ర` 0.60 · `్వ` 0.84 · `్య` 0.94 · `మ` 0.49 · `్య` 0.99 · `ు` 0.99 · `ని` 0.95 · `␣ప్ర` 0.36✱ · `గ` 0.96 · `్` 0.93 · `⏎` 1.00 forced |
| 4 | `స` 0.11 · `న` 3.7e-3✱ · `ము` 0.83 · `న` 0.94 · `␣తే` 0.71 · `లి` 1.00 · `క` 1.00 · `␣న` 0.97 · `్య` 0.99 · `్వ` 0.95 · `్` 0.62 · `జ` 0.99 · `న` 0.98 · `్య` 1.00 · `ు` 1.00 · `ని` 1.00 · `␣ధ` 0.59 · `ై` 1.00 · `ర్య` 0.97 · `ము` 1.00 · `␣ద` 0.92 · `్య` 1.00 · `్వ` 0.96 · `్` 0.43✱ · `జ` 0.99 · `న` 0.88 · `్య` 0.94 · `ు` 1.00 · `ని` 1.00 · `␣గ` 0.44 · `మ` 0.98 · `్య` 0.97 · `ము` 0.88 · `␣న` 2.8e-3✱ · `్య` 0.58 · `్వ` 0.71 · `్` 0.24✱ · `జ` 0.95 · `న` 0.71 · `్య` 0.96 · `ు` 1.00 · `ని` 0.99 · `␣ప్ర` 0.33 · `గ` 0.98 · `్` 0.98 |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 138 tokens · 40.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వనమును దాటిన వాయు పుతొడ్రు తపస్సరిగాండిరి వన్రణమున్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 2 | సనమున చేరిన సన్రుతమున్ సము ద్య్వ్సన్రుతమున్ సనసన్రుతమున్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 3 | అనగనగాన అనగ్రుతమున్ అరణయ్నమునన్ అననన్రుతమున్ | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 4 | లొనమున చేరిన లొన్రుతమున్ లొనలొన్రుతమున్ లొనలొన్రుతమున్ | `IIIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.124 · model's first choice kept 61% · constraint overrode 33% · backtracks 30

<details><summary>Token probabilities (138 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.50 · `న` 5.2e-4✱ · `ము` 0.47 · `ను` 0.10✱ · `␣దా` 0.84 · `టి` 0.81 · `న` 0.23 · `␣వ` 0.21 · `ాయ` 0.93 · `ు` 1.00 · `␣పు` 0.01 · `త` 0.11✱ · `ొ` 4.9e-4✱ · `డ` 0.02✱ · `్రు` 2.4e-3✱ · `␣త` 0.02 · `ప` 0.20✱ · `స్` 0.04✱ · `స` 0.48 · `రి` 9.8e-3 · `గా` 3.2e-3✱ · `ండి` 1.3e-4✱ · `రి` 9.1e-4✱ · `␣వ` 8.9e-4✱ · `న` 0.16✱ · `్ర` 1.5e-4✱ · `ణ` 0.02✱ · `ము` 0.77 · `న` 0.14✱ · `్` 1.2e-6✱ · `⏎` 0.32 forced |
| 2 | `స` 0.32 · `న` 9.8e-6✱ · `ము` 0.27 · `న` 0.23 · `␣చే` 0.23 · `రి` 0.66 · `న` 0.83 · `␣స` 0.34 · `న` 8.8e-3✱ · `్రు` 5.1e-4✱ · `త` 0.51 · `ము` 0.24 · `న` 0.35 · `్` 2.0e-3✱ · `␣స` 0.30 · `ము` 0.67 · `␣ద` 1.1e-5✱ · `్య` 6.8e-3✱ · `్వ` 3.4e-4✱ · `్` 2.2e-3✱ · `స` 0.01✱ · `న` 0.21✱ · `్రు` 0.02✱ · `త` 0.73 · `ము` 0.86 · `న` 0.72 · `్` 0.91 · `␣స` 0.25 · `న` 0.24 · `స` 3.9e-3✱ · `న` 0.16✱ · `్రు` 0.20✱ · `త` 0.96 · `ము` 0.98 · `న` 0.94 · `్` 1.00 · `⏎` 0.83 forced |
| 3 | `అ` 0.09 · `న` 0.56 · `గ` 0.05✱ · `న` 0.95 · `గా` 0.58 · `న` 0.35 · `␣అ` 0.10 · `న` 0.03✱ · `గ` 0.39 · `్రు` 7.8e-5✱ · `త` 0.89 · `ము` 0.93 · `న` 0.98 · `్` 1.00 · `␣అ` 0.65 · `రణ` 0.05✱ · `య` 1.3e-3✱ · `్` 0.05✱ · `న` 0.54 · `ము` 0.17 · `న` 0.92 · `న్` 3.1e-3✱ · `␣అ` 0.74 · `న` 0.13 · `న` 0.07✱ · `న` 0.26✱ · `్రు` 0.96 · `త` 1.00 · `ము` 1.00 · `న` 1.00 · `్` 0.99 · `⏎` 0.99 forced |
| 4 | `ల` 0.18 · `ొ` 9.9e-3✱ · `న` 0.24✱ · `ము` 0.19 · `న` 0.68 · `␣చే` 0.46 · `రి` 0.88 · `న` 0.96 · `␣ల` 0.93 · `ొ` 0.08✱ · `న` 0.95 · `్రు` 0.81 · `త` 0.98 · `ము` 1.00 · `న` 1.00 · `్` 0.98 · `␣ల` 0.88 · `ొ` 0.02✱ · `న` 0.89 · `ల` 0.30 · `ొ` 0.28 · `న` 0.96 · `్రు` 0.87 · `త` 1.00 · `ము` 1.00 · `న` 1.00 · `్` 0.98 · `␣ల` 0.99 · `ొ` 0.85 · `న` 0.98 · `ల` 0.38 · `ొ` 0.87 · `న` 0.99 · `్రు` 0.85 · `త` 1.00 · `ము` 1.00 · `న` 1.00 · `్` 1.00 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 42 · 151 tokens · 53.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వనముల దాటి వ ద్య్వాళన శైలముపై ఉదరమ్ములె న్య్య్వాళమునిం | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 2 | వినుము ధనుర్ధర ద్య్వ్వేక్ష్య మునియ్ని ద్య్వ్వవృక్షమునుం ద్య్వ్వభవించుననుం | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 3 | శనక శిరస్సున సప్త సముద్రము ధ్వ్వ్సన్యు ద్య్వ్వధర్యు త్యు శైలమునిం | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 4 | వనమున లంకను ద్య్వ్వశ్రవణమ్ము త్యు ద్య్వ్వధ్వనినిం త్యు రవణ్వనితమ్ | `IIIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 14% · repeated lines 0 · mean token probability (geometric) 0.075 · model's first choice kept 44% · constraint overrode 40% · backtracks 30

<details><summary>Token probabilities (151 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.50 · `న` 5.2e-4✱ · `ముల` 0.08 · `␣దా` 0.54 · `టి` 0.84 · `␣వ` 0.07 · `␣ద` 1.7e-6✱ · `్య` 7.3e-3✱ · `్వ` 5.0e-5✱ · `ా` 0.12 · `ళ` 0.07 · `న` 0.13✱ · `␣శ` 7.5e-3 · `ై` 0.21 · `ల` 0.77 · `ము` 0.69 · `పై` 0.04✱ · `␣ఉ` 0.04✱ · `ద` 0.11✱ · `ర` 0.08✱ · `మ్ము` 6.2e-3✱ · `ల` 0.02✱ · `ె` 0.01✱ · `␣న` 1.6e-3✱ · `్య` 2.9e-3✱ · `్య` 6.7e-3✱ · `్వ` 5.8e-3✱ · `ా` 0.23 · `ళ` 0.06✱ · `ము` 0.07 · `ని` 0.01✱ · `ం` 2.4e-3✱ · `⏎` 0.73 forced |
| 2 | `వి` 8.0e-3 · `ను` 1.7e-3✱ · `ము` 0.39 · `␣ధ` 0.02 · `ను` 0.11✱ · `ర్` 0.66 · `ధ` 0.37 · `ర` 0.12✱ · `␣ద` 0.13 · `్య` 3.1e-3✱ · `్వ` 0.01✱ · `్వ` 0.02✱ · `ే` 0.01✱ · `క్ష` 0.09 · `్య` 0.27 · `␣ము` 8.4e-3✱ · `ని` 0.74 · `య` 0.07 · `్` 1.8e-3✱ · `ని` 0.20 · `␣ద` 0.03✱ · `్య` 0.36 · `్వ` 0.83 · `్వ` 0.51 · `వ` 4.5e-3✱ · `ృ` 0.09✱ · `క్ష` 0.63 · `ము` 0.40 · `ను` 0.10 · `ం` 0.03✱ · `␣ద` 0.11 · `్య` 0.94 · `్వ` 0.94 · `్వ` 0.93 · `భ` 5.4e-3✱ · `వ` 2.2e-3✱ · `ించు` 0.02✱ · `న` 0.04✱ · `ను` 0.01✱ · `ం` 0.72 · `⏎` 0.99 forced |
| 3 | `శ` 0.12 · `న` 0.01✱ · `క` 0.86 · `␣శి` 0.08 · `ర` 0.67 · `స్సు` 0.47 · `న` 0.39 · `␣స` 0.21 · `ప్త` 0.05✱ · `␣స` 0.33 · `ము` 0.92 · `ద్ర` 0.91 · `ము` 0.42 · `␣ధ` 1.4e-3✱ · `్వ` 0.29 · `్వ` 6.4e-4✱ · `్` 1.4e-4✱ · `స` 1.1e-3✱ · `న` 0.17✱ · `్య` 1.3e-3✱ · `ు` 0.28 · `␣ద` 0.02✱ · `్య` 0.93 · `్వ` 0.99 · `్వ` 0.92 · `ధ` 0.01✱ · `ర` 0.03✱ · `్య` 7.3e-3✱ · `ు` 0.48 · `␣త` 0.04✱ · `్య` 0.11 · `ు` 0.11 · `␣శ` 2.1e-3✱ · `ై` 0.28 · `ల` 0.83 · `ము` 0.61 · `ని` 0.24 · `ం` 0.95 · `⏎` 1.00 forced |
| 4 | `వ` 0.09 · `న` 0.03✱ · `ము` 0.35 · `న` 0.30 · `␣ల` 0.20 · `ంక` 0.64 · `ను` 0.53 · `␣ద` 0.18✱ · `్య` 0.96 · `్వ` 0.99 · `్వ` 0.94 · `శ` 0.04 · `్ర` 0.08✱ · `వ` 0.23 · `ణ` 0.85 · `మ్ము` 0.03✱ · `␣త` 0.06 · `్య` 0.92 · `ు` 0.96 · `␣ద` 0.57 · `్య` 1.00 · `్వ` 0.99 · `్వ` 0.87 · `ధ` 0.08 · `్వ` 0.46 · `ని` 0.76 · `ని` 0.10✱ · `ం` 0.61 · `␣త` 0.10 · `్య` 0.88 · `ు` 0.98 · `␣ర` 0.03 · `వ` 3.8e-3✱ · `ణ` 0.81 · `్వ` 9.2e-3✱ · `ని` 0.17 · `త` 2.0e-4✱ · `మ్` 0.45 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 138 tokens · 10.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తలి మమతో జగదంతమదింతటి స్ర్వ్తమ్యునినిన్రము ణ్య్య్తమ్యునినే | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 2 | తలి కరుణో నిరతానదినిన్రము న్య్య్తమ్యునినే హృదదంతమనే | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 3 | తలి అనురాగమొ క్వ్తమ్యునినే నిరతానదినిన్రము ణ్య్య్తమ్యునినే | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 4 | తలి దయయే శిరదంతమదిన్రము న్య్య్తమ్యునినే హృదదంతమనే | `IIIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 25% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.143 · model's first choice kept 61% · constraint overrode 36% · backtracks 0

<details><summary>Token probabilities (138 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.76 · `లి` 7.7e-4✱ · `␣మ` 0.05✱ · `మ` 0.96 · `త` 0.88 · `ో` 5.4e-4✱ · `␣జగ` 0.26 · `ద` 2.1e-3✱ · `ంత` 0.78 · `మ` 0.38 · `ది` 0.02✱ · `ంత` 1.5e-4✱ · `టి` 0.17 · `␣స` 0.01✱ · `్ర` 4.8e-4✱ · `్వ` 4.7e-8✱ · `్` 3.8e-5✱ · `త` 0.16✱ · `మ` 0.11✱ · `్య` 0.06✱ · `ు` 0.06✱ · `ని` 0.04✱ · `ని` 3.4e-3✱ · `న` 1.4e-3✱ · `్ర` 3.2e-4✱ · `ము` 0.02✱ · `␣` 5.6e-4✱ · `ణ` 0.07✱ · `్య` 0.11✱ · `్య` 5.6e-3✱ · `్` 1.5e-3✱ · `త` 0.05✱ · `మ` 0.13✱ · `్య` 0.73 · `ు` 0.77 · `ని` 0.83 · `నే` 2.2e-3 · `⏎` 0.60 forced |
| 2 | `త` 0.45 · `లి` 0.13✱ · `␣క` 0.20✱ · `రుణ` 0.99 · `ో` 0.37 · `␣ని` 0.10 · `ర` 0.05✱ · `త` 6.0e-4✱ · `ాన` 0.04✱ · `ది` 0.16 · `ని` 0.06✱ · `న` 0.23 · `్ర` 0.08✱ · `ము` 0.79 · `␣న` 0.09✱ · `్య` 0.02✱ · `్య` 0.92 · `్` 0.66 · `త` 0.97 · `మ` 0.94 · `్య` 0.98 · `ు` 0.99 · `ని` 0.97 · `నే` 0.65 · `␣హ` 0.04 · `ృ` 0.85 · `ద` 0.20✱ · `ద` 2.5e-4✱ · `ంత` 0.45 · `మ` 0.55 · `నే` 4.3e-3✱ · `⏎` 0.97 forced |
| 3 | `త` 0.96 · `లి` 0.90 · `␣అను` 0.14✱ · `రా` 0.96 · `గ` 0.89 · `మ` 0.41 · `ొ` 0.06✱ · `␣క` 0.02✱ · `్వ` 1.5e-4✱ · `్` 4.6e-4✱ · `త` 0.39 · `మ` 0.70 · `్య` 0.73 · `ు` 0.99 · `ని` 0.96 · `నే` 0.33 · `␣ని` 0.20 · `ర` 0.66 · `త` 0.38✱ · `ాన` 0.83 · `ది` 0.94 · `ని` 0.92 · `న` 0.98 · `్ర` 0.98 · `ము` 0.99 · `␣` 0.29 · `ణ` 0.96 · `్య` 0.99 · `్య` 0.99 · `్` 0.99 · `త` 1.00 · `మ` 1.00 · `్య` 0.86 · `ు` 1.00 · `ని` 0.99 · `నే` 0.99 · `⏎` 1.00 forced |
| 4 | `త` 0.97 · `లి` 0.97 · `␣ద` 0.03✱ · `య` 0.69 · `యే` 0.19✱ · `␣శి` 0.02 · `ర` 0.57 · `ద` 0.12✱ · `ంత` 0.92 · `మ` 0.94 · `ది` 0.72 · `న` 0.03✱ · `్ర` 0.82 · `ము` 1.00 · `␣న` 0.97 · `్య` 1.00 · `్య` 1.00 · `్` 1.00 · `త` 1.00 · `మ` 1.00 · `్య` 1.00 · `ు` 1.00 · `ని` 1.00 · `నే` 1.00 · `␣హ` 0.29 · `ృ` 0.97 · `ద` 0.97 · `ద` 0.98 · `ంత` 0.99 · `మ` 0.97 · `నే` 1.00 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 133 tokens · 9.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సిరిమల నౌకల న్య్వ్జిత్య లఘుమ్యజజిత్య వ్రతమ్యజజిత్య వృతం | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 2 | కరుణ రసమ్యజికల్య జ్యుమత్యజికల్య భయమ్యజికల్య నిరా | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 3 | వరుణ ధనమ్యజృవత్య జ్యుమత్యజృవత్య రణమ్యజృవత్య విరా | `IIIIUIIUIIUIIUIIUIIUIIU` |
| 4 | మరణ భయమ్యజృమత్య జ్యుమత్యజృమత్య రణమ్యజృమత్య జరా | `IIIIUIIUIIUIIUIIUIIUIIU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 24% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.157 · model's first choice kept 56% · constraint overrode 35% · backtracks 0

<details><summary>Token probabilities (133 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `సి` 0.02✱ · `రి` 0.04✱ · `మ` 0.10✱ · `ల` 0.46 · `␣న` 0.03 · `ౌ` 7.2e-3✱ · `క` 0.78 · `ల` 0.13✱ · `␣న` 0.03✱ · `్య` 4.6e-5✱ · `్వ` 1.7e-4✱ · `్` 2.2e-3✱ · `జ` 0.02✱ · `ిత` 0.02✱ · `్య` 0.01✱ · `␣ల` 0.02✱ · `ఘ` 2.9e-4✱ · `ు` 0.99 · `మ` 0.09 · `్య` 0.06✱ · `జ` 0.03✱ · `జ` 0.45 · `ిత` 1.9e-3✱ · `్య` 0.40 · `␣వ` 0.07✱ · `్ర` 1.8e-3✱ · `త` 0.57 · `మ` 0.03✱ · `్య` 0.76 · `జ` 0.41 · `జ` 0.79 · `ిత` 0.92 · `్య` 0.99 · `␣వ` 0.10✱ · `ృ` 0.07✱ · `తం` 5.1e-3✱ · `⏎` 0.81 forced |
| 2 | `క` 0.05 · `రుణ` 0.04✱ · `␣ర` 8.0e-3✱ · `స` 0.10✱ · `మ` 0.24✱ · `్య` 0.61 · `జ` 0.42 · `ిక` 5.9e-4✱ · `ల` 0.09✱ · `్య` 0.02✱ · `␣జ` 0.33 · `్య` 0.59 · `ు` 0.03✱ · `మ` 0.14✱ · `త్య` 5.0e-3✱ · `జ` 0.81 · `ిక` 0.15✱ · `ల` 0.31✱ · `్య` 0.91 · `␣భ` 0.08 · `య` 0.18 · `మ` 0.56 · `్య` 0.97 · `జ` 0.99 · `ిక` 0.47 · `ల` 0.98 · `్య` 0.99 · `␣ని` 0.08 · `రా` 0.04✱ · `⏎` 3.2e-6 forced |
| 3 | `వ` 0.04 · `రుణ` 7.3e-3✱ · `␣ధ` 0.08✱ · `న` 0.07✱ · `మ` 0.77 · `్య` 0.99 · `జ` 0.95 · `ృ` 6.6e-4✱ · `వ` 6.8e-3✱ · `త` 0.22 · `్య` 0.91 · `␣జ` 0.18 · `్య` 0.74 · `ు` 0.36 · `మ` 0.76 · `త` 0.21 · `్య` 0.89 · `జ` 0.98 · `ృ` 0.17✱ · `వ` 0.98 · `త` 1.00 · `్య` 1.00 · `␣ర` 0.14 · `ణ` 0.05✱ · `మ` 0.97 · `్య` 1.00 · `జ` 1.00 · `ృ` 0.95 · `వ` 1.00 · `త` 1.00 · `్య` 1.00 · `␣వి` 0.07 · `రా` 0.93 · `⏎` 0.94 forced |
| 4 | `మ` 0.03 · `రణ` 8.6e-3✱ · `␣భ` 0.22 · `య` 0.59 · `మ` 0.98 · `్య` 1.00 · `జ` 0.98 · `ృ` 0.08✱ · `మ` 0.03✱ · `త్య` 0.13 · `␣జ` 0.94 · `్య` 0.92 · `ు` 0.95 · `మ` 0.98 · `త` 0.59 · `్య` 0.99 · `జ` 1.00 · `ృ` 0.99 · `మ` 1.00 · `త` 0.94 · `్య` 1.00 · `␣ర` 0.20 · `ణ` 0.86 · `మ` 1.00 · `్య` 1.00 · `జ` 1.00 · `ృ` 0.99 · `మ` 1.00 · `త` 0.87 · `్య` 0.99 · `␣జ` 0.05 · `రా` 0.12 |

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

<details><summary>Prompt (topic T1; the other topics differ only in the topic line)</summary>

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

Topic (విషయము): తల్లి ప్రేమ అన్నింటికంటే గొప్పది

Write only the 4 lines of the poem in Telugu script, one pāda per line. No title, no numbering, no transliteration, no explanation.
```

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 93 tokens · 15.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి కరుణే జగతి న్య్ర్ధయ్నిని నిలిప్యెన్ | `UIIIUIIIUIIIUU` |
| 2 | తల్లి అనురాగమది తల్యెన నినుల్యెన్ | `UIIIUIIIUIIIUU` |
| 3 | తల్లి మమతే మరువదగ్యున మధుర్య్యెన్ | `UIIIUIIIUIIIUU` |
| 4 | తల్లి దయయే దినమృధయ్నిని ద్యుగెన్ ఝున్ | `UIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 28% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.077 · model's first choice kept 49% · constraint overrode 40% · backtracks 0

<details><summary>Token probabilities (93 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.74 · `␣క` 0.02✱ · `రుణ` 0.97 · `ే` 0.11 · `␣జగ` 0.67 · `తి` 0.91 · `␣న` 1.9e-3✱ · `్య` 9.6e-7✱ · `్ర` 1.4e-6✱ · `్` 8.4e-5✱ · `ధ` 0.03✱ · `య` 0.05✱ · `్` 6.2e-4✱ · `ని` 0.06 · `ని` 0.03 · `␣ని` 0.07✱ · `లి` 0.08✱ · `ప` 0.35✱ · `్య` 3.1e-4✱ · `ె` 0.32 · `న` 0.02✱ · `్` 8.6e-7✱ · `⏎` 0.72 forced |
| 2 | `త` 0.48 · `ల్లి` 0.81 · `␣అను` 0.08✱ · `రా` 0.98 · `గ` 0.66 · `మ` 0.05✱ · `ది` 0.09✱ · `␣త` 0.30 · `ల` 0.52 · `్య` 1.3e-4✱ · `ె` 0.04 · `న` 0.48 · `␣ని` 0.10 · `ను` 0.04✱ · `ల` 0.01✱ · `్య` 6.1e-4✱ · `ె` 0.74 · `న` 0.79 · `్` 0.88 · `⏎` 1.00 forced |
| 3 | `త` 0.95 · `ల్లి` 0.92 · `␣మ` 0.04✱ · `మ` 0.94 · `త` 0.78 · `ే` 0.09✱ · `␣మ` 0.47 · `రు` 0.25 · `వ` 0.80 · `ద` 0.25✱ · `గ` 0.13✱ · `్య` 8.0e-3✱ · `ు` 0.19 · `న` 0.13 · `␣మ` 0.48 · `ధు` 0.19 · `ర` 0.72 · `్య` 0.16 · `్య` 0.07 · `ె` 0.51 · `న` 0.97 · `్` 0.95 · `⏎` 1.00 forced |
| 4 | `త` 0.99 · `ల్లి` 0.97 · `␣ద` 0.04✱ · `య` 0.58 · `యే` 0.57 · `␣ద` 0.38 · `ిన` 8.9e-3✱ · `మ` 0.17 · `ృ` 0.01✱ · `ధ` 0.11✱ · `య` 0.07✱ · `్` 0.37 · `ని` 0.78 · `ని` 0.60 · `␣ద` 0.30 · `్య` 0.07✱ · `ు` 0.27✱ · `గ` 0.19 · `ె` 4.0e-3✱ · `న` 0.97 · `్` 1.00 · `␣` 1.3e-5✱ · `ఝ` 1.2e-3✱ · `ు` 0.18 · `న` 0.25 · `్` 0.54 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 63 · 90 tokens · 16.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిదొరికెన్న దయ స్ర్వ్తాన ఘనమై నిల్ | `UIIIUIIIUIIIUU` |
| 2 | మల్లికల సుగ్రు ఘనమైన మమతక్రా | `UIIIUIIIUIIIUU` |
| 3 | అల్లకలయై నవత ల్ల్యక్యుత ఘనమ్యే | `UIIIUIIIUIIIUU` |
| 4 | నిల్లకలయై నవత ల్ల్య్యిక్యుత ఘనమ్యే | `UIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.045 · model's first choice kept 54% · constraint overrode 37% · backtracks 0

<details><summary>Token probabilities (90 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.74 · `ద` 0.01✱ · `ొ` 0.01✱ · `రి` 0.37 · `కె` 0.51 · `న` 0.22✱ · `్` 1.0e-4✱ · `న` 0.36 · `␣ద` 0.05✱ · `య` 0.28✱ · `␣స` 0.01✱ · `్ర` 5.1e-3✱ · `్వ` 2.2e-6✱ · `్` 3.8e-4✱ · `త` 0.15✱ · `ాన` 0.09 · `␣ఘ` 0.05✱ · `న` 0.82 · `మై` 0.05 · `␣ని` 0.09✱ · `ల` 0.23✱ · `్` 1.3e-12✱ · `⏎` 5.3e-3 forced |
| 2 | `మ` 0.13 · `ల్లి` 0.16 · `క` 0.45 · `ల` 0.26 · `␣సు` 0.21 · `గ` 0.90 · `్రు` 1.1e-7✱ · `␣ఘ` 0.22 · `న` 0.50 · `మైన` 0.04 · `␣మ` 0.19 · `మ` 0.24 · `త` 0.83 · `క` 7.1e-3✱ · `్రా` 3.9e-5✱ · `⏎` 1.3e-4 forced |
| 3 | `అ` 0.23 · `ల` 0.02✱ · `్` 1.5e-6✱ · `ల` 0.72 · `క` 0.16 · `ల` 0.45 · `య` 8.4e-3 · `ై` 0.02✱ · `␣న` 0.05 · `వ` 0.15 · `త` 0.13 · `␣ల` 0.02✱ · `్` 2.0e-4✱ · `ల` 0.68 · `్య` 2.6e-3✱ · `క` 0.03✱ · `్య` 4.2e-4✱ · `ు` 0.11 · `త` 0.12 · `␣ఘ` 0.05 · `న` 0.82 · `మ` 0.10✱ · `్య` 8.4e-3✱ · `ే` 0.30 · `⏎` 0.91 forced |
| 4 | `ని` 0.03 · `ల` 8.7e-3✱ · `్` 5.9e-5✱ · `ల` 0.38 · `క` 0.45 · `ల` 0.83 · `య` 0.38 · `ై` 0.75 · `␣న` 0.17 · `వ` 0.89 · `త` 0.92 · `␣ల` 0.73 · `్` 0.94 · `ల` 0.96 · `్య` 0.91 · `్య` 1.7e-3✱ · `ిక` 1.4e-3✱ · `్య` 0.56 · `ు` 0.91 · `త` 0.97 · `␣ఘ` 0.62 · `న` 0.98 · `మ` 0.63 · `్య` 0.96 · `ే` 0.99 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 100 tokens · 32.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి దయ నేర్పి కన క్వ్వ్తమ్యెనది వన్యుర్ | `UIIIUIIIUIIIUU` |
| 2 | తల్లి హృదయమ్యెనది ప్య్య్తమ్యెనది వన్యుర్ | `UIIIUIIIUIIIUU` |
| 3 | తల్లి అనురాగమెనదై స్ఫుటమయెన్రున్ | `UIIIUIIIUIIIUU` |
| 4 | తల్లి కరుణమ్యెనది శ్వ్య్తమ్యెనది వన్యుర్ | `UIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 35% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.082 · model's first choice kept 60% · constraint overrode 32% · backtracks 30

<details><summary>Token probabilities (100 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.74 · `␣ద` 9.7e-3✱ · `య` 0.63 · `␣నే` 5.5e-3 · `ర్` 0.26 · `పి` 0.22 · `␣క` 0.05 · `న` 2.6e-3✱ · `␣క` 3.9e-3✱ · `్వ` 1.7e-6✱ · `్వ` 1.7e-6✱ · `్` 3.6e-3✱ · `త` 0.07✱ · `మ` 0.03✱ · `్య` 0.05✱ · `ె` 0.05✱ · `న` 0.33 · `ది` 0.06✱ · `␣వ` 2.1e-3✱ · `న` 0.40 · `్య` 5.2e-6✱ · `ు` 0.50 · `ర` 0.67 · `్` 4.5e-9✱ · `⏎` 0.03 forced |
| 2 | `త` 0.22 · `ల్లి` 0.87 · `␣హ` 0.06✱ · `ృ` 0.97 · `దయ` 0.71 · `మ` 0.18 · `్య` 2.8e-3✱ · `ె` 0.46 · `న` 0.77 · `ది` 0.11 · `␣ప` 0.01 · `్య` 0.13✱ · `్య` 4.8e-3✱ · `్` 7.7e-4✱ · `త` 0.25✱ · `మ` 0.85 · `్య` 0.97 · `ె` 0.95 · `న` 0.97 · `ది` 1.00 · `␣వ` 0.50 · `న` 1.00 · `్య` 0.99 · `ు` 1.00 · `ర` 1.00 · `్` 1.00 · `⏎` 0.99 forced |
| 3 | `త` 0.88 · `ల్లి` 0.95 · `␣అను` 0.11✱ · `రా` 0.93 · `గ` 0.92 · `మ` 0.62 · `ె` 4.3e-4✱ · `న` 0.96 · `ద` 9.1e-4✱ · `ై` 0.27 · `␣స్` 0.01 · `ఫ` 0.15 · `ు` 0.67 · `ట` 0.12 · `మ` 0.54 · `య` 1.3e-3✱ · `ె` 0.90 · `న` 0.92 · `్రు` 3.9e-7✱ · `న` 1.2e-3✱ · `్` 0.10✱ · `⏎` 0.97 forced |
| 4 | `త` 0.99 · `ల్లి` 0.98 · `␣క` 0.04✱ · `రుణ` 0.98 · `మ` 0.08 · `్య` 0.82 · `ె` 0.99 · `న` 0.98 · `ది` 0.89 · `␣శ` 0.14 · `్వ` 1.4e-3✱ · `్య` 4.2e-6✱ · `్` 0.06✱ · `త` 0.60 · `మ` 0.99 · `్య` 0.83 · `ె` 1.00 · `న` 1.00 · `ది` 0.97 · `␣వ` 0.99 · `న` 1.00 · `్య` 0.99 · `ు` 1.00 · `ర` 1.00 · `్` 1.00 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 79 tokens · 28.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీపురుష తేజమున కృష్ణుని కరుణ్యే | `UIIIUIIIUIIIUU` |
| 2 | వ్యాపి కరుణా మకర వాయువుల కైకత్ | `UIIIUIIIUIIIUU` |
| 3 | సైపతక సంపదను సంచరితి సూర్యమ్ | `UIIIUIIIUIIIUU` |
| 4 | సౌపలక సంహరణు న్య్య్జం నరసినింహ్యే | `UIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 35% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.029 · model's first choice kept 33% · constraint overrode 50% · backtracks 30

<details><summary>Token probabilities (79 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.09 · `్రీ` 0.42 · `పు` 0.01✱ · `రు` 0.54 · `ష` 0.91 · `␣తే` 0.09✱ · `జ` 0.95 · `ము` 0.58 · `న` 0.27 · `␣క` 4.1e-3✱ · `ృష్` 8.2e-4✱ · `ణు` 0.65 · `ని` 0.94 · `␣క` 0.06✱ · `రుణ` 0.08✱ · `్య` 1.0e-2✱ · `ే` 0.21✱ · `⏎` 0.16 forced |
| 2 | `వ` 0.11 · `్యా` 8.7e-4✱ · `పి` 0.18 · `␣క` 0.03✱ · `రుణ` 0.07✱ · `ా` 0.59 · `␣మ` 0.02✱ · `కర` 0.05 · `␣వ` 2.0e-3✱ · `ాయ` 0.27 · `ు` 0.98 · `వు` 0.14✱ · `ల` 0.16 · `␣క` 0.01 · `ై` 0.09 · `క` 0.03 · `త` 0.09✱ · `్` 2.4e-7✱ · `⏎` 0.04 forced |
| 3 | `స` 0.35 · `ై` 2.5e-6✱ · `ప` 4.8e-5✱ · `త` 0.02 · `క` 6.9e-3✱ · `␣సం` 0.05 · `ప` 0.25 · `ద` 0.96 · `ను` 0.20 · `␣స` 0.24 · `ంచ` 0.05✱ · `రి` 0.25✱ · `తి` 0.36 · `␣స` 0.38 · `ూర్` 0.11✱ · `య` 0.84 · `మ` 0.02✱ · `్` 5.0e-10✱ · `⏎` 0.10 forced |
| 4 | `స` 0.09 · `ౌ` 4.0e-3✱ · `ప` 1.9e-3✱ · `ల` 0.35 · `క` 0.07✱ · `␣సం` 0.08 · `హ` 0.58 · `రణ` 1.4e-3✱ · `ు` 0.02✱ · `␣న` 4.1e-3✱ · `్య` 7.6e-6✱ · `్య` 2.3e-4✱ · `్` 1.2e-4✱ · `జ` 7.2e-3✱ · `ం` 0.09 · `␣న` 0.17 · `ర` 0.16 · `సి` 0.12 · `ని` 0.03✱ · `ం` 0.05✱ · `హ` 0.01✱ · `్య` 0.09✱ · `ే` 0.50 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 68 tokens · 4.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి కరుణే జగతి న్య్ర్ధయ్ని సృజనై తే | `UIIIUIIIUIIIUU` |
| 2 | తల్లి అనురాగము నితన్ము సతమై తే | `UIIIUIIIUIIIUU` |
| 3 | తల్లి రమణా మధురతై నిరనముల్యా | `UIIIUIIIUIIIUU` |
| 4 | తల్లి దయయే పరమతై కరుణమయ్యా | `UIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 26% · single-akshara words 11% · repeated lines 0 · mean token probability (geometric) 0.051 · model's first choice kept 43% · constraint overrode 46% · backtracks 0

<details><summary>Token probabilities (68 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.79 · `ల్లి` 0.74 · `␣క` 0.02✱ · `రుణ` 0.97 · `ే` 0.11 · `␣జగ` 0.67 · `తి` 0.91 · `␣న` 1.9e-3✱ · `్య` 9.6e-7✱ · `్ర` 1.4e-6✱ · `్` 8.4e-5✱ · `ధ` 0.03✱ · `య` 0.05✱ · `్` 6.2e-4✱ · `ని` 0.06 · `␣స` 0.03 · `ృ` 0.16✱ · `జ` 0.91 · `న` 0.55 · `ై` 0.16✱ · `␣తే` 6.0e-3✱ · `⏎` 0.04 forced |
| 2 | `త` 0.56 · `ల్లి` 0.79 · `␣అను` 0.06✱ · `రా` 0.98 · `గ` 0.66 · `ము` 0.11✱ · `␣ని` 0.18 · `త` 2.2e-5✱ · `న్` 0.01✱ · `ము` 0.07 · `␣స` 0.04 · `త` 0.04✱ · `మ` 3.5e-3✱ · `ై` 0.42 · `␣తే` 0.33 · `⏎` 1.00 forced |
| 3 | `త` 0.96 · `ల్లి` 0.93 · `␣ర` 0.01✱ · `మ` 3.7e-4✱ · `ణా` 0.09✱ · `␣మ` 0.07 · `ధు` 0.39 · `ర` 0.78 · `త` 9.0e-3✱ · `ై` 0.49 · `␣ని` 0.20 · `ర` 0.13✱ · `న` 6.3e-3✱ · `ము` 0.02✱ · `ల` 4.3e-4✱ · `్యా` 4.0e-4✱ · `⏎` 9.4e-3 forced |
| 4 | `త` 1.00 · `ల్లి` 0.97 · `␣ద` 0.05✱ · `య` 0.53 · `యే` 0.64 · `␣పర` 0.11✱ · `మ` 0.87 · `త` 0.06✱ · `ై` 0.99 · `␣క` 0.04 · `రుణ` 0.29 · `మ` 0.02✱ · `య్యా` 6.4e-3 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 42 · 78 tokens · 12.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీని శరణం గతిని కృష్ణుని కరుణ్యం | `UIIIUIIIUIIIUU` |
| 2 | సీను సురమిత్రని ధిశేయెను ధనుర్భా | `UIIIUIIIUIIIUU` |
| 3 | లౌన లయమున్యు లఘు ర్వ్య్లక్యు రణమున్రో | `UIIIUIIIUIIIUU` |
| 4 | చైను చరితమ్ముని రసమ్ము వికసించే | `UIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 22% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.033 · model's first choice kept 35% · constraint overrode 47% · backtracks 0

<details><summary>Token probabilities (78 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.16 · `్రీ` 0.99 · `ని` 0.03✱ · `␣శ` 0.06✱ · `రణ` 0.85 · `ం` 0.54 · `␣గ` 0.02✱ · `తి` 0.15✱ · `ని` 0.12 · `␣క` 0.06✱ · `ృష్` 0.02✱ · `ణు` 0.61 · `ని` 0.93 · `␣క` 0.08 · `రుణ` 0.16✱ · `్యం` 1.9e-4✱ · `⏎` 0.05 forced |
| 2 | `సీ` 0.35 · `ను` 1.5e-5✱ · `␣సు` 0.07 · `ర` 0.82 · `మ` 0.03✱ · `ిత` 0.02✱ · `్ర` 0.88 · `ని` 0.32 · `␣ధ` 0.02 · `ి` 0.03✱ · `శ` 2.9e-4✱ · `ే` 0.06✱ · `య` 0.06 · `ె` 0.08 · `ను` 0.49 · `␣ధ` 0.14 · `ను` 0.02✱ · `ర్భ` 0.09 · `ా` 0.38 · `⏎` 7.2e-3 forced |
| 3 | `ల` 0.23✱ · `ౌ` 2.1e-3✱ · `న` 4.0e-4✱ · `␣ల` 0.51 · `య` 9.3e-4✱ · `ము` 0.51 · `న` 0.33 · `్య` 2.6e-5✱ · `ు` 0.30 · `␣ల` 0.23 · `ఘ` 2.6e-3✱ · `ు` 0.97 · `␣ర` 3.2e-3✱ · `్వ` 1.6e-6✱ · `్య` 4.3e-4✱ · `్` 5.2e-4✱ · `ల` 5.9e-3✱ · `క` 0.11 · `్య` 3.2e-3✱ · `ు` 0.33 · `␣ర` 0.04 · `ణ` 0.18✱ · `ము` 0.30 · `న` 0.07✱ · `్రో` 3.1e-5✱ · `⏎` 0.99 forced |
| 4 | `చ` 0.03 · `ై` 0.11✱ · `ను` 1.2e-4✱ · `␣చ` 0.51 · `రి` 0.07 · `త` 0.86 · `మ్ము` 0.03✱ · `ని` 0.31 · `␣ర` 0.17 · `స` 2.3e-4✱ · `మ్ము` 0.24✱ · `␣వి` 0.03 · `క` 0.04 · `స` 0.49 · `ించే` 2.1e-3 |

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

Topic T3: `Topic (విషయము): శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను`

</details>

### Masking only

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 56 · 149 tokens · 24.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | సక్రియుడెనున్రు తప స్వభ్రమము నివ్రయెను జగ్వలమునందునమునందున్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | రాక్రియుడెనున్రు దయ క్రాంతిని కలుగ్యెను లొరంగలమునందునమునందున్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | సీక్రియుడెనున్రు భయ నివ్రయెను రక్షకమునెన్రు లొకలమ్రునమునందున్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | సక్రియుడెనున్రు జయ ఘ్నత్యెను రఘుమ్యయుననందునమునందునతొనన్న్న్తొన్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 21% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.059 · model's first choice kept 52% · constraint overrode 39% · backtracks 0

<details><summary>Token probabilities (149 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `స` 0.04 · `క` 0.07 · `్రి` 4.4e-6✱ · `యు` 0.01✱ · `డ` 0.57 · `ె` 0.01✱ · `ను` 0.26 · `న` 1.3e-3✱ · `్రు` 3.7e-4✱ · `␣త` 0.08✱ · `ప` 0.09 · `␣స్వ` 3.6e-3✱ · `భ` 0.52 · `్రమ` 1.2e-7✱ · `ము` 0.27 · `␣ని` 0.03 · `వ` 0.44 · `్ర` 8.5e-5✱ · `య` 0.90 · `ె` 0.02✱ · `ను` 0.83 · `␣జగ` 0.02✱ · `్వ` 1.1e-5✱ · `ల` 0.55 · `ము` 0.53 · `న` 0.11✱ · `ందు` 0.04✱ · `న` 0.05✱ · `ము` 2.4e-3✱ · `న` 0.01✱ · `ందు` 2.0e-3✱ · `న` 0.33✱ · `్` 3.9e-7✱ · `⏎` 0.93 forced |
| 2 | `రా` 0.08 · `క` 1.2e-5✱ · `్రి` 3.6e-4✱ · `యు` 0.50 · `డ` 0.75 · `ె` 0.70 · `ను` 0.82 · `న` 0.77 · `్రు` 0.97 · `␣ద` 0.09 · `య` 0.05✱ · `␣క` 0.07 · `్రా` 3.2e-4✱ · `ంతి` 0.43 · `ని` 0.17 · `␣క` 0.03✱ · `లు` 0.18 · `గ` 0.87 · `్య` 3.2e-5✱ · `ె` 0.88 · `ను` 0.86 · `␣ల` 0.38 · `ొ` 2.3e-4✱ · `రంగ` 8.8e-5✱ · `ల` 0.23 · `ము` 0.59 · `న` 0.82 · `ందు` 0.96 · `న` 0.98 · `ము` 0.73 · `న` 0.99 · `ందు` 0.99 · `న` 0.99 · `్` 0.98 · `⏎` 1.00 forced |
| 3 | `సీ` 0.45 · `క` 7.4e-8✱ · `్రి` 0.58 · `యు` 0.98 · `డ` 1.00 · `ె` 1.00 · `ను` 0.99 · `న` 1.00 · `్రు` 1.00 · `␣భ` 0.11 · `య` 0.77 · `␣ని` 0.06✱ · `వ` 0.66 · `్ర` 3.1e-3✱ · `య` 0.93 · `ె` 0.77 · `ను` 0.97 · `␣ర` 0.12 · `క్ష` 0.64 · `క` 0.11✱ · `ము` 0.05✱ · `న` 0.41 · `ె` 2.6e-3✱ · `న` 0.08✱ · `్రు` 7.9e-3✱ · `␣ల` 0.06 · `ొ` 3.3e-3✱ · `క` 3.6e-3✱ · `ల` 0.72 · `మ` 0.02✱ · `్రు` 2.3e-4✱ · `న` 0.75 · `ము` 0.02✱ · `న` 1.00 · `ందు` 1.00 · `న` 1.00 · `్` 0.99 · `⏎` 1.00 forced |
| 4 | `స` 0.10 · `క` 0.77 · `్రి` 0.94 · `యు` 1.00 · `డ` 0.98 · `ె` 0.99 · `ను` 0.99 · `న` 1.00 · `్రు` 1.00 · `␣జ` 0.02 · `య` 0.96 · `␣ఘ` 0.06 · `్` 3.6e-6✱ · `న` 0.89 · `త` 0.11✱ · `్య` 7.9e-3✱ · `ె` 0.07 · `ను` 0.93 · `␣ర` 0.12✱ · `ఘ` 0.10✱ · `ు` 0.99 · `మ` 0.37 · `్య` 1.2e-3✱ · `యు` 0.20 · `న` 0.26 · `న` 5.3e-3✱ · `ందు` 0.09✱ · `న` 0.99 · `ము` 0.99 · `న` 1.00 · `ందు` 1.00 · `న` 1.00 · `త` 6.9e-6✱ · `ొ` 5.4e-3✱ · `న` 4.8e-3✱ · `న్` 0.02✱ · `న్` 3.7e-4✱ · `న్` 4.0e-3✱ · `త` 1.1e-3✱ · `ొ` 0.85 · `న` 0.82 · `్` 0.12✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 49 · 162 tokens · 47.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామచరణం లభయ భ్రమ్య భయమున్య భవ న్య్య్రణ్య భవనన్ త్వరితమున్యన్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | సీమనుని కక్ష్య భయ భ్ర్ఞ్ణేన భయమున్య భవ న్య్య్రృణ్య భవనన్ త్వరితమున్యన్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | శ్రీమనుని శక్తుల భవృత్య భవనన్ త్వరితమృద్య భవనన్ త్వరితమున్యన్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | భూమిని భుజగ్య భయ భ్ర్ఞ్ణోన భవనన్ త్వరితమూర్తి భవనన్ త్వరితమున్యన్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.150 · model's first choice kept 62% · constraint overrode 30% · backtracks 0

<details><summary>Token probabilities (162 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.33 · `మ` 0.81 · `చ` 0.84 · `రణ` 3.2e-3✱ · `ం` 0.59 · `␣ల` 0.47 · `భ` 3.6e-4✱ · `య` 0.01✱ · `␣భ` 2.9e-3✱ · `్రమ` 0.02✱ · `్య` 1.7e-3✱ · `␣భ` 0.06✱ · `య` 0.14 · `ము` 0.33 · `న` 0.25 · `్య` 8.3e-5✱ · `␣భ` 0.07✱ · `వ` 0.14 · `␣న` 9.4e-4✱ · `్య` 0.07✱ · `్య` 7.3e-4✱ · `్ర` 2.7e-5✱ · `ణ` 0.04✱ · `్య` 0.30✱ · `␣భ` 0.33 · `వ` 0.49 · `న` 0.21✱ · `న్` 1.2e-3✱ · `␣త` 1.8e-3✱ · `్వ` 0.56 · `రి` 0.04✱ · `త` 0.80 · `ము` 0.21✱ · `న` 0.23✱ · `్య` 0.06✱ · `న` 3.7e-3✱ · `్` 6.4e-5✱ · `⏎` 0.83 forced |
| 2 | `సీ` 0.80 · `మ` 8.0e-5✱ · `ను` 0.05 · `ని` 0.10 · `␣క` 0.06 · `క్ష` 0.02✱ · `్య` 0.54 · `␣భ` 0.30 · `య` 0.37 · `␣భ` 8.4e-3✱ · `్ర` 0.03✱ · `్ఞ` 2.7e-8✱ · `్` 1.7e-3✱ · `ణ` 0.10✱ · `ే` 0.01✱ · `న` 0.46 · `␣భ` 0.64 · `య` 0.15 · `ము` 0.39 · `న` 0.73 · `్య` 0.83 · `␣భ` 0.64 · `వ` 0.92 · `␣న` 0.45 · `్య` 0.99 · `్య` 0.97 · `్ర` 0.97 · `ృ` 1.1e-6✱ · `ణ` 0.96 · `్య` 0.97 · `␣భ` 0.98 · `వ` 0.99 · `న` 0.96 · `న్` 0.97 · `␣త` 0.79 · `్వ` 0.95 · `రి` 0.99 · `త` 0.98 · `ము` 0.97 · `న` 0.96 · `్య` 0.91 · `న` 0.98 · `్` 0.98 · `⏎` 0.99 forced |
| 3 | `శ` 0.08✱ · `్రీ` 0.07✱ · `మ` 0.11✱ · `ను` 0.22✱ · `ని` 0.77 · `␣శ` 0.02 · `క్` 0.01✱ · `తుల` 0.59 · `␣భ` 0.67 · `వ` 0.25 · `ృత` 9.9e-5✱ · `్య` 0.04✱ · `␣భ` 0.89 · `వ` 0.13 · `న` 0.68 · `న్` 0.68 · `␣త` 0.73 · `్వ` 0.94 · `రి` 0.98 · `త` 0.97 · `మ` 0.01✱ · `ృ` 6.6e-3✱ · `ద` 0.11 · `్య` 0.94 · `␣భ` 0.75 · `వ` 0.52 · `న` 0.63 · `న్` 0.97 · `␣త` 0.82 · `్వ` 0.97 · `రి` 0.98 · `త` 0.99 · `ము` 0.84 · `న` 0.99 · `్య` 0.98 · `న` 1.00 · `్` 0.99 · `⏎` 1.00 forced |
| 4 | `భ` 0.04 · `ూ` 0.20✱ · `మి` 0.20 · `ని` 0.64 · `␣భ` 0.11 · `ు` 0.04✱ · `జ` 0.66 · `గ` 0.14✱ · `్య` 0.14✱ · `␣భ` 0.83 · `య` 0.53 · `␣భ` 0.28 · `్ర` 0.61 · `్ఞ` 0.94 · `్` 0.85 · `ణ` 0.98 · `ో` 6.0e-4✱ · `న` 0.48 · `␣భ` 0.77 · `వ` 0.84 · `న` 0.35 · `న్` 1.00 · `␣త` 1.00 · `్వ` 1.00 · `రి` 1.00 · `త` 0.99 · `మ` 0.70 · `ూర్` 1.5e-3✱ · `తి` 0.60 · `␣భ` 0.93 · `వ` 0.99 · `న` 0.98 · `న్` 1.00 · `␣త` 0.99 · `్వ` 1.00 · `రి` 1.00 · `త` 1.00 · `ము` 1.00 · `న` 1.00 · `్య` 1.00 · `న` 1.00 · `్` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 122 tokens · 39.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లి దయ వీర కవతం సుమతృణేన వలతైదురమునందున నవత్రా | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | తల్లి హృదయాన అమృతధ్రువమునందున సుధాకృతమునందున నిరాశే | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | తల్లి కరుణా ప్రదణ ధారనమునందున భుదయ్వలతయెన్రున నవత్రా | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | తల్లి అనురాగ స్రవతారముననందున హృదయ్యశృణులెన్రున నిరాశే | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 30% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.094 · model's first choice kept 44% · constraint overrode 42% · backtracks 30

<details><summary>Token probabilities (122 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.83 · `ల్లి` 0.77 · `␣ద` 3.9e-3✱ · `య` 0.54 · `␣వీ` 5.7e-3 · `ర` 0.26 · `␣క` 9.6e-3 · `వ` 0.05✱ · `తం` 1.1e-6✱ · `␣సు` 0.05 · `మ` 0.50 · `త` 0.09 · `ృ` 0.02✱ · `ణ` 0.31 · `ే` 0.23 · `న` 0.20✱ · `␣వ` 9.9e-3✱ · `ల` 0.39 · `త` 0.01✱ · `ై` 0.07✱ · `దు` 3.3e-3✱ · `ర` 0.18✱ · `ము` 0.13✱ · `న` 0.07✱ · `ందు` 9.9e-3✱ · `న` 0.11✱ · `␣న` 1.9e-3✱ · `వ` 0.15 · `త` 0.21✱ · `్రా` 5.9e-3✱ · `⏎` 7.3e-4 forced |
| 2 | `త` 0.27 · `ల్లి` 0.90 · `␣హ` 0.02✱ · `ృ` 0.98 · `దయ` 0.80 · `ాన` 0.06✱ · `␣అమ` 0.03 · `ృత` 0.84 · `ధ` 0.05✱ · `్రు` 5.4e-5✱ · `వ` 0.91 · `ము` 0.08✱ · `న` 0.38 · `ందు` 0.14✱ · `న` 0.94 · `␣సు` 0.05 · `ధ` 0.02✱ · `ా` 0.60 · `క` 0.08 · `ృత` 0.05✱ · `ము` 0.22 · `న` 0.70 · `ందు` 0.27 · `న` 0.97 · `␣ని` 0.03 · `రా` 0.05✱ · `శ` 0.11✱ · `ే` 0.12✱ · `⏎` 0.05 forced |
| 3 | `త` 0.93 · `ల్లి` 0.93 · `␣క` 0.11✱ · `రుణ` 0.93 · `ా` 0.40 · `␣ప్ర` 0.08✱ · `ద` 0.02✱ · `ణ` 1.7e-3✱ · `␣ధ` 0.05 · `ార` 0.16 · `న` 0.10 · `ము` 0.07 · `న` 0.98 · `ందు` 1.00 · `న` 1.00 · `␣భ` 0.02✱ · `ు` 0.25✱ · `దయ` 1.6e-4✱ · `్వ` 7.6e-4✱ · `ల` 0.13✱ · `త` 0.40 · `య` 4.3e-3✱ · `ె` 0.17 · `న` 0.63 · `్రు` 2.1e-4✱ · `న` 0.21 · `␣న` 0.28 · `వ` 0.79 · `త` 0.88 · `్రా` 0.99 · `⏎` 1.00 forced |
| 4 | `త` 0.98 · `ల్లి` 0.98 · `␣అను` 0.10✱ · `రా` 0.94 · `గ` 0.94 · `␣స` 0.06 · `్ర` 0.13✱ · `వ` 0.99 · `త` 7.8e-3✱ · `ార` 4.0e-3✱ · `ము` 0.52 · `న` 1.00 · `న` 2.6e-5✱ · `ందు` 0.94 · `న` 1.00 · `␣హ` 0.03✱ · `ృ` 0.84 · `దయ` 0.83 · `్య` 1.7e-3✱ · `శ` 0.04✱ · `ృ` 7.6e-3✱ · `ణ` 9.2e-3✱ · `ుల` 0.04✱ · `ె` 0.13 · `న` 0.91 · `్రు` 0.96 · `న` 0.98 · `␣ని` 0.40 · `రా` 0.91 · `శ` 0.99 · `ే` 1.00 |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 63 · 149 tokens · 48.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | రామచరణం లభయ భ్రమ్య శరణం భజన శ్రద్ధ్య నమకన్తణ లహృమ్యే | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | శ్రీమనుని రక్షణకరిం చెరసరిం భవన సృష్టియెన వల్యుమృద నేత్యే | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | సీమనుని రక్షణకృషీ లఘుమృదన్ లభయ భ్ర్య్శృన్య నమకన్తణ లహృమ్యే | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | తైమస సుఖమ్యెన లతైం భజన శ్రద్ధ్య నమతన్ భవన సృష్టియెన వల్యుమ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 16% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.079 · model's first choice kept 48% · constraint overrode 40% · backtracks 30

<details><summary>Token probabilities (149 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `రా` 0.33 · `మ` 0.81 · `చ` 0.84 · `రణ` 3.2e-3✱ · `ం` 0.59 · `␣ల` 0.47 · `భ` 3.6e-4✱ · `య` 0.01✱ · `␣భ` 4.0e-3✱ · `్రమ` 0.02✱ · `్య` 1.7e-3✱ · `␣శ` 3.2e-3✱ · `రణ` 0.59 · `ం` 0.65 · `␣భ` 0.14✱ · `జ` 0.53 · `న` 0.67 · `␣శ` 0.22 · `్ర` 0.02✱ · `ద్ధ` 0.20 · `్య` 0.02✱ · `␣న` 0.18✱ · `మ` 0.23✱ · `క` 0.06✱ · `న్` 5.5e-4✱ · `త` 7.8e-4✱ · `ణ` 2.8e-4✱ · `␣ల` 1.3e-4✱ · `హ` 0.02✱ · `ృ` 0.04✱ · `మ` 0.06✱ · `్య` 0.14✱ · `ే` 5.4e-3✱ · `⏎` 0.90 forced |
| 2 | `శ` 0.08 · `్రీ` 0.96 · `మ` 0.03✱ · `ను` 0.12✱ · `ని` 0.28 · `␣ర` 0.34 · `క్షణ` 0.36 · `క` 0.07✱ · `రి` 1.3e-4✱ · `ం` 0.28 · `␣చె` 0.02 · `ర` 0.03 · `స` 0.06 · `రి` 0.76 · `ం` 0.08✱ · `␣భ` 0.58 · `వ` 0.18 · `న` 0.67 · `␣స` 0.05 · `ృష్టి` 0.03✱ · `య` 0.07 · `ె` 0.28 · `న` 0.14 · `␣వ` 0.02 · `ల` 0.24 · `్య` 8.2e-3✱ · `ు` 0.12✱ · `మ` 0.22✱ · `ృ` 0.02✱ · `ద` 0.04✱ · `␣నే` 1.2e-3✱ · `త` 0.12 · `్య` 0.33 · `ే` 0.96 · `⏎` 0.99 forced |
| 3 | `సీ` 0.55 · `మ` 3.3e-4✱ · `ను` 0.07✱ · `ని` 0.83 · `␣ర` 0.05 · `క్షణ` 0.35 · `క` 0.79 · `ృ` 2.5e-4✱ · `ష` 0.02✱ · `ీ` 0.17✱ · `␣ల` 0.41 · `ఘ` 6.9e-4✱ · `ు` 0.96 · `మ` 0.44 · `ృ` 0.40 · `ద` 0.84 · `న్` 4.1e-3✱ · `␣ల` 0.10 · `భ` 0.06✱ · `య` 0.47 · `␣భ` 0.39 · `్ర` 0.01✱ · `్య` 7.8e-8✱ · `్` 1.3e-4✱ · `శ` 0.05✱ · `ృ` 1.3e-3✱ · `న` 0.14 · `్య` 7.9e-4✱ · `␣న` 0.41 · `మ` 0.94 · `క` 0.96 · `న్` 0.96 · `త` 0.98 · `ణ` 0.92 · `␣ల` 0.54 · `హ` 0.99 · `ృ` 0.98 · `మ` 0.99 · `్య` 1.00 · `ే` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.02✱ · `ై` 2.6e-3✱ · `మ` 3.2e-3✱ · `స` 0.15 · `␣సు` 0.02✱ · `ఖ` 0.14 · `మ` 0.35 · `్య` 9.4e-3✱ · `ె` 0.05✱ · `న` 0.54 · `␣ల` 0.13 · `త` 6.9e-4✱ · `ై` 0.03✱ · `ం` 0.26 · `␣భ` 0.72 · `జ` 0.70 · `న` 0.91 · `␣శ` 0.80 · `్ర` 0.72 · `ద్ధ` 0.97 · `్య` 0.96 · `␣న` 0.87 · `మ` 0.97 · `త` 1.8e-4✱ · `న్` 0.34 · `␣భ` 0.11 · `వ` 0.75 · `న` 0.87 · `␣స` 0.64 · `ృష్టి` 0.98 · `య` 0.96 · `ె` 0.95 · `న` 0.97 · `␣వ` 0.67 · `ల` 0.99 · `్య` 0.98 · `ు` 0.83 · `మ` 0.98 · `్` 1.6e-5✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 49 · 132 tokens · 27.8 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లికరుణా మధుర ఘ్ర్వ్ధా వలపునిక్రునితృ తల్యమునితృమ్యమునితృమ్యం | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | తల్లిఅనురాగ నిరతార సలహా దయనిదానమునితృమ్యమునితృమ్యం | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | తల్లిని సృజన్య కరతార ధనమున్రు త్యజదై నిను నిరంతరమునిత్రీ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | తల్లియెడలక్రు నిరతార అనురాగ నిలదై నిను నిరంతరమునిత్రీ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 18% · single-akshara words 5% · repeated lines 0 · mean token probability (geometric) 0.075 · model's first choice kept 49% · constraint overrode 43% · backtracks 0

<details><summary>Token probabilities (132 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.83 · `ల్లి` 0.77 · `క` 0.02✱ · `రుణ` 0.74 · `ా` 0.40 · `␣మ` 0.15 · `ధు` 0.66 · `ర` 0.71 · `␣ఘ` 0.02✱ · `్ర` 4.0e-7✱ · `్వ` 8.6e-7✱ · `్` 6.7e-5✱ · `ధ` 3.7e-3✱ · `ా` 0.16✱ · `␣వ` 0.04 · `ల` 0.32 · `పు` 0.21 · `ని` 0.17 · `క` 0.01✱ · `్రు` 2.1e-6✱ · `ని` 0.10✱ · `త` 0.03✱ · `ృ` 8.4e-3✱ · `␣త` 3.5e-3✱ · `ల` 0.32 · `్య` 1.8e-4✱ · `ము` 0.20 · `ని` 0.07✱ · `త` 0.02✱ · `ృ` 0.82 · `మ` 5.3e-3✱ · `్య` 0.08✱ · `ము` 0.25✱ · `ని` 0.08✱ · `త` 0.60 · `ృ` 0.98 · `మ` 8.2e-3✱ · `్యం` 7.9e-3 · `⏎` 0.97 forced |
| 2 | `త` 0.53 · `ల్లి` 0.91 · `అ` 0.12✱ · `ను` 0.86 · `రా` 0.95 · `గ` 0.92 · `␣ని` 0.07✱ · `ర` 0.06✱ · `త` 1.8e-3✱ · `ార` 6.1e-3✱ · `␣స` 0.06✱ · `ల` 6.1e-3✱ · `హా` 0.35 · `␣ద` 0.11 · `య` 0.05✱ · `ని` 0.09✱ · `ద` 0.01✱ · `ాన` 0.05✱ · `ము` 0.14 · `ని` 0.33 · `త` 0.77 · `ృ` 0.98 · `మ` 0.29✱ · `్య` 0.90 · `ము` 0.98 · `ని` 0.99 · `త` 1.00 · `ృ` 1.00 · `మ` 0.99 · `్యం` 0.92 · `⏎` 1.00 forced |
| 3 | `త` 0.85 · `ల్లి` 0.93 · `ని` 0.08 · `␣స` 0.02✱ · `ృ` 2.4e-3✱ · `జ` 0.85 · `న` 0.75 · `్య` 5.1e-5✱ · `␣క` 0.06 · `ర` 2.9e-3✱ · `త` 0.01✱ · `ార` 0.11✱ · `␣ధ` 0.05 · `న` 0.02✱ · `ము` 0.51 · `న` 0.08✱ · `్రు` 1.7e-3✱ · `␣త` 0.06 · `్య` 0.06 · `జ` 0.98 · `ద` 1.6e-3✱ · `ై` 0.11 · `␣ని` 0.20 · `ను` 0.07✱ · `␣ని` 0.05 · `ర` 0.05✱ · `ంత` 0.42 · `ర` 0.99 · `ము` 0.24 · `ని` 0.76 · `త` 1.00 · `్రీ` 1.1e-5✱ · `⏎` 0.13 forced |
| 4 | `త` 0.99 · `ల్లి` 0.95 · `య` 0.01✱ · `ె` 0.45 · `డ` 0.04✱ · `ల` 0.84 · `క` 4.6e-3✱ · `్రు` 7.4e-5✱ · `␣ని` 0.12 · `ర` 0.03✱ · `త` 0.06✱ · `ార` 0.56 · `␣అను` 0.02 · `రా` 0.84 · `గ` 0.92 · `␣ని` 0.04 · `ల` 0.03✱ · `ద` 4.0e-3✱ · `ై` 0.46 · `␣ని` 0.19 · `ను` 0.69 · `␣ని` 0.75 · `ర` 0.19✱ · `ంత` 0.92 · `ర` 0.99 · `ము` 0.93 · `ని` 0.97 · `త` 0.99 · `్రీ` 0.94 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 170 tokens · 35.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | మాతృమహమూర్తి దయ క్య్ర్మాన శరణం వహెను స్ర్య్మన్యనమునందున భజన్యా | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | తాతృభజనస్ర్య్మనము తల్యన భజన్యనము న్య్మ్దాన్యనము స్ర్య్మన్యనమునందున్ | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | తాతృమహమూర్తి దయ క్య్ర్తాన శరణం వహెను స్ర్య్తాన్యనమునందున భజన్యా | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | తాతృభజనస్ర్య్తనము తల్యన భజన్యనము న్య్మ్దాన్యనము స్ర్య్తన్యనమునందే | `UIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 17% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.159 · model's first choice kept 69% · constraint overrode 27% · backtracks 0

<details><summary>Token probabilities (170 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `మా` 0.10 · `త` 0.98 · `ృ` 0.98 · `మ` 0.09✱ · `హ` 0.05✱ · `మ` 2.8e-3✱ · `ూర్` 0.24 · `తి` 0.97 · `␣ద` 0.13 · `య` 0.21✱ · `␣క` 0.01✱ · `్య` 9.3e-9✱ · `్ర` 1.0e-5✱ · `్` 3.4e-6✱ · `మ` 0.38 · `ాన` 3.4e-3✱ · `␣శ` 0.04✱ · `రణ` 0.14✱ · `ం` 0.51 · `␣వ` 9.4e-3✱ · `హ` 0.79 · `ె` 0.06✱ · `ను` 0.34 · `␣స` 3.6e-3✱ · `్ర` 2.1e-3✱ · `్య` 2.0e-5✱ · `్` 0.02✱ · `మ` 0.26✱ · `న` 0.06✱ · `్య` 1.5e-4✱ · `న` 0.03✱ · `ము` 0.02✱ · `న` 0.02✱ · `ందు` 2.4e-3✱ · `న` 0.13✱ · `␣భ` 5.7e-3✱ · `జ` 0.08 · `న` 0.58 · `్యా` 5.5e-5✱ · `⏎` 0.19 forced |
| 2 | `త` 0.44 · `ాత` 1.6e-4✱ · `ృ` 0.64 · `భ` 0.06✱ · `జ` 3.8e-3✱ · `న` 0.89 · `స` 0.03 · `్ర` 0.18✱ · `్య` 0.36 · `్` 0.71 · `మ` 0.92 · `న` 0.86 · `ము` 0.08✱ · `␣త` 6.4e-3✱ · `ల` 0.21 · `్య` 1.7e-3✱ · `న` 0.25 · `␣భ` 0.12 · `జ` 0.88 · `న` 0.90 · `్య` 0.08✱ · `న` 0.54 · `ము` 0.72 · `␣న` 0.04✱ · `్య` 2.9e-3✱ · `్` 8.6e-3✱ · `మ` 0.62 · `్` 1.1e-6✱ · `ద` 7.8e-3✱ · `ాన` 0.09 · `్య` 0.17 · `న` 0.61 · `ము` 0.81 · `␣స` 0.06 · `్ర` 0.49 · `్య` 0.95 · `్` 0.94 · `మ` 0.96 · `న` 0.86 · `్య` 0.60 · `న` 0.96 · `ము` 0.90 · `న` 0.55 · `ందు` 0.34✱ · `న్` 2.2e-4 · `⏎` 0.98 forced |
| 3 | `త` 0.37 · `ాత` 0.02✱ · `ృ` 0.93 · `మ` 0.48 · `హ` 0.88 · `మ` 0.64 · `ూర్` 0.97 · `తి` 0.97 · `␣ద` 0.57 · `య` 0.94 · `␣క` 0.72 · `్య` 0.99 · `్ర` 0.94 · `్` 0.99 · `త` 2.4e-5✱ · `ాన` 0.73 · `␣శ` 0.56 · `రణ` 0.98 · `ం` 0.93 · `␣వ` 0.95 · `హ` 1.00 · `ె` 0.95 · `ను` 0.96 · `␣స` 0.94 · `్ర` 0.97 · `్య` 1.00 · `్` 0.99 · `త` 9.0e-4✱ · `ాన` 0.34 · `్య` 0.88 · `న` 1.00 · `ము` 0.98 · `న` 0.99 · `ందు` 0.96 · `న` 0.96 · `␣భ` 0.98 · `జ` 1.00 · `న` 0.98 · `్యా` 0.96 · `⏎` 0.98 forced |
| 4 | `త` 0.41 · `ాత` 0.98 · `ృ` 0.98 · `భ` 0.98 · `జ` 1.00 · `న` 0.99 · `స` 0.98 · `్ర` 1.00 · `్య` 1.00 · `్` 0.98 · `త` 0.61 · `న` 5.2e-3✱ · `ము` 0.99 · `␣త` 0.99 · `ల` 0.99 · `్య` 0.98 · `న` 0.97 · `␣భ` 0.99 · `జ` 1.00 · `న` 0.98 · `్య` 0.97 · `న` 1.00 · `ము` 1.00 · `␣న` 0.99 · `్య` 1.00 · `్` 0.99 · `మ` 0.89 · `్` 0.82 · `ద` 0.94 · `ాన` 0.99 · `్య` 1.00 · `న` 1.00 · `ము` 1.00 · `␣స` 0.97 · `్ర` 1.00 · `్య` 1.00 · `్` 1.00 · `త` 0.96 · `న` 0.88 · `్య` 0.96 · `న` 1.00 · `ము` 1.00 · `న` 0.98 · `ందే` 4.9e-4 |

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

Topic T2: `Topic (విషయము): హనుమంతుడు సముద్రమును దాటి లంకను చేరెను`

</details>

### Masking only

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 63 · 193 tokens · 42.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వాయుపుతనుడ్యెన సముధ్ యమును దాటెను లవణ్రతను ఝంఘమున చేర్ యును లొణక్యే | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | ప్రా యణమునై వెలసినై యుగమునల్రు లొణకల్ యమున చేరెను లొణక్ యమున భేరెన్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | శైయమునలక్రి యెన లంక్ యమున చేరెను హనుమ్ యెన భయానకమునల్రు లొణకల్ యెన్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | గీయమునలక్రి యెన లంక్ యమున చేరెను భయాన్ యెన లవణ్రతను ఝంఘ్ యెన గమెన్ ఝే | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 17% · repeated lines 0 · mean token probability (geometric) 0.070 · model's first choice kept 55% · constraint overrode 39% · backtracks 0

<details><summary>Token probabilities (193 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.47 · `ాయ` 1.00 · `ు` 1.00 · `పు` 0.73 · `త` 0.08✱ · `ను` 2.8e-4✱ · `డ` 0.38✱ · `్య` 2.3e-4✱ · `ె` 0.37 · `న` 0.32 · `␣స` 0.08✱ · `ము` 0.98 · `ధ` 4.8e-3✱ · `్` 6.6e-3✱ · `␣` 4.0e-6✱ · `య` 8.1e-7✱ · `ము` 0.42 · `ను` 0.29✱ · `␣దా` 0.85 · `ట` 0.31 · `ె` 0.95 · `ను` 0.84 · `␣ల` 0.05✱ · `వ` 1.6e-4✱ · `ణ` 0.81 · `్ర` 6.8e-4✱ · `త` 0.08✱ · `ను` 0.09✱ · `␣` 4.3e-3✱ · `ఝ` 0.76 · `ం` 0.48 · `ఘ` 0.13✱ · `ము` 0.02 · `న` 0.46 · `␣చే` 0.51 · `ర` 0.03✱ · `్` 4.4e-11✱ · `␣` 1.2e-4✱ · `యు` 6.7e-4✱ · `ను` 0.33 · `␣ల` 0.15✱ · `ొ` 3.1e-4✱ · `ణ` 0.02✱ · `క` 0.77 · `్య` 3.6e-4✱ · `ే` 0.13✱ · `⏎` 0.06 forced |
| 2 | `ప` 0.13 · `్రా` 0.01✱ · `␣య` 4.1e-8✱ · `ణ` 0.25✱ · `ము` 0.68 · `న` 0.52 · `ై` 0.01✱ · `␣వె` 0.03 · `ల` 0.06✱ · `సిన` 0.38 · `ై` 0.06✱ · `␣` 5.0e-3✱ · `యు` 7.4e-7✱ · `గ` 0.48 · `ము` 0.41 · `న` 0.39 · `ల` 3.3e-3✱ · `్రు` 2.0e-4✱ · `␣ల` 0.38 · `ొ` 2.4e-3✱ · `ణ` 0.74 · `క` 0.87 · `ల` 0.03✱ · `్` 1.1e-5✱ · `␣` 8.0e-4✱ · `య` 8.4e-5✱ · `ము` 0.29 · `న` 0.64 · `␣చే` 0.21 · `ర` 0.39 · `ె` 0.37 · `ను` 0.94 · `␣ల` 0.29 · `ొ` 0.02✱ · `ణ` 0.93 · `క` 0.91 · `్` 9.0e-4✱ · `␣` 0.14 · `య` 0.91 · `ము` 0.15✱ · `న` 0.69 · `␣భ` 1.0e-2 · `ే` 0.36 · `ర` 0.16 · `ె` 0.41 · `న్` 9.7e-3✱ · `⏎` 0.93 forced |
| 3 | `శ` 0.15 · `ై` 0.03✱ · `య` 6.3e-5✱ · `ము` 0.61 · `న` 0.50 · `ల` 8.9e-3✱ · `క` 0.06✱ · `్రి` 0.01✱ · `␣య` 0.16✱ · `ె` 0.58 · `న` 0.61 · `␣ల` 0.06✱ · `ంక` 0.70 · `్` 2.8e-8✱ · `␣` 0.11✱ · `య` 0.25✱ · `ము` 0.82 · `న` 0.70 · `␣చే` 0.44 · `ర` 0.53 · `ె` 0.93 · `ను` 0.94 · `␣హ` 0.09 · `ను` 0.95 · `మ` 0.60 · `్` 0.08✱ · `␣య` 0.03✱ · `ె` 0.33 · `న` 0.86 · `␣భ` 0.13 · `య` 0.03✱ · `ాన` 0.05✱ · `క` 0.55 · `ము` 0.46 · `న` 0.65 · `ల` 6.4e-3✱ · `్రు` 0.47 · `␣ల` 0.45 · `ొ` 0.58 · `ణ` 0.98 · `క` 0.98 · `ల` 0.08✱ · `్` 0.92 · `␣య` 0.68 · `ె` 0.38 · `న` 0.07✱ · `్` 3.0e-4✱ · `⏎` 1.00 forced |
| 4 | `గ` 0.15 · `ీ` 0.05✱ · `య` 3.6e-5✱ · `ము` 0.87 · `న` 0.83 · `ల` 0.66 · `క` 0.28 · `్రి` 0.72 · `␣య` 0.63 · `ె` 0.90 · `న` 0.93 · `␣ల` 0.59 · `ంక` 0.81 · `్` 0.70 · `␣` 0.64 · `య` 1.00 · `ము` 0.98 · `న` 0.87 · `␣చే` 0.55 · `ర` 0.80 · `ె` 0.99 · `ను` 0.99 · `␣భ` 0.13 · `య` 0.28✱ · `ాన` 0.44 · `్` 3.2e-8✱ · `␣య` 0.05✱ · `ె` 0.88 · `న` 0.97 · `␣ల` 0.13 · `వ` 0.23 · `ణ` 0.94 · `్ర` 0.80 · `త` 0.85 · `ను` 0.90 · `␣` 0.78 · `ఝ` 1.00 · `ం` 0.97 · `ఘ` 0.98 · `్` 2.0e-3✱ · `␣` 0.07✱ · `య` 0.88 · `ె` 0.83 · `న` 0.87 · `␣గ` 7.4e-3✱ · `మ` 0.25✱ · `ె` 0.10✱ · `న్` 0.55 · `␣` 4.0e-5✱ · `ఝ` 0.10✱ · `ే` 0.39 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 169 tokens · 27.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లికరుణే జగతికిన్ ల్లున మధుర్యమున నిల్లెనునుగాయెనునిదిన్ ల్లెనుమునవ్యా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | తల్లిఅనురాగమున జగ్ ల్లికలలక్యమున నిల్లెనునుగాయెనునిదిన్ ల్లెనుమునవ్యా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | తల్లిపొలకల్రు మదిలోన్ ల్లికలలక్యమున నిల్లెనునుగాయెనునిదిన్ ల్లెనుమునవ్యా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | తల్లిమమతల్రు జగతిక్ ల్లికలలక్యమున నిల్లెనునుగాయెనునిదిన్ ల్లెనుమునవ్యా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 10% · single-akshara words 5% · repeated lines 0 · mean token probability (geometric) 0.141 · model's first choice kept 73% · constraint overrode 23% · backtracks 0

<details><summary>Token probabilities (169 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.80 · `ల్లి` 0.72 · `క` 0.03✱ · `రుణ` 0.74 · `ే` 0.10 · `␣జగ` 0.65 · `తి` 0.90 · `కి` 0.80 · `న్` 0.02✱ · `␣` 5.8e-4✱ · `ల్లు` 4.8e-7✱ · `న` 0.39 · `␣మ` 0.07✱ · `ధు` 0.48 · `ర` 0.86 · `్య` 1.1e-5✱ · `ము` 0.29 · `న` 0.18✱ · `␣ని` 0.04✱ · `ల` 0.20✱ · `్` 1.2e-12✱ · `ల` 0.58 · `ె` 0.31 · `ను` 0.56 · `ను` 5.3e-3✱ · `గా` 4.3e-3✱ · `య` 0.03✱ · `ె` 0.08✱ · `ను` 0.02✱ · `ని` 1.5e-4✱ · `ది` 1.8e-3✱ · `న్` 1.9e-4✱ · `␣` 1.8e-4✱ · `ల్ల` 9.0e-6✱ · `ె` 0.63 · `ను` 0.62 · `ము` 0.03✱ · `న` 0.23✱ · `వ` 1.9e-3✱ · `్యా` 6.4e-3✱ · `⏎` 1.0e-4 forced |
| 2 | `త` 0.51 · `ల్లి` 0.92 · `అ` 0.13 · `ను` 0.92 · `రా` 0.91 · `గ` 0.80 · `ము` 0.24✱ · `న` 0.09✱ · `␣జగ` 0.19 · `్` 2.4e-9✱ · `␣` 6.8e-9✱ · `ల్లి` 5.9e-5✱ · `క` 0.51 · `ల` 0.13✱ · `ల` 0.16 · `క` 0.09 · `్య` 2.0e-6✱ · `ము` 0.20✱ · `న` 0.67 · `␣ని` 0.21 · `ల` 0.48 · `్` 0.22 · `ల` 0.95 · `ె` 0.98 · `ను` 0.95 · `ను` 0.79 · `గా` 0.96 · `య` 1.00 · `ె` 1.00 · `ను` 0.99 · `ని` 0.98 · `ది` 0.99 · `న్` 1.00 · `␣` 0.97 · `ల్ల` 0.99 · `ె` 1.00 · `ను` 0.99 · `ము` 1.00 · `న` 0.99 · `వ` 0.93 · `్యా` 1.00 · `⏎` 1.00 forced |
| 3 | `త` 0.89 · `ల్లి` 0.93 · `ప` 0.29 · `ొ` 0.01✱ · `ల` 0.71 · `క` 0.36 · `ల` 0.56 · `్రు` 1.4e-4✱ · `␣మ` 0.06 · `ది` 0.41 · `లో` 0.48 · `న` 0.88 · `్` 1.8e-5✱ · `␣` 0.03✱ · `ల్లి` 0.22 · `క` 0.71 · `ల` 0.87 · `ల` 0.77 · `క` 0.71 · `్య` 0.93 · `ము` 0.97 · `న` 0.97 · `␣ని` 0.95 · `ల` 0.99 · `్` 0.99 · `ల` 0.99 · `ె` 1.00 · `ను` 1.00 · `ను` 0.99 · `గా` 1.00 · `య` 1.00 · `ె` 1.00 · `ను` 1.00 · `ని` 1.00 · `ది` 1.00 · `న్` 1.00 · `␣` 1.00 · `ల్ల` 1.00 · `ె` 1.00 · `ను` 1.00 · `ము` 1.00 · `న` 1.00 · `వ` 1.00 · `్యా` 1.00 · `⏎` 1.00 forced |
| 4 | `త` 0.97 · `ల్లి` 0.95 · `మ` 0.05 · `మ` 0.24 · `తల` 0.28 · `్రు` 3.8e-3✱ · `␣జగ` 0.31 · `తి` 0.90 · `క` 0.09✱ · `్` 7.7e-9✱ · `␣` 0.46 · `ల్లి` 0.93 · `క` 0.96 · `ల` 0.98 · `ల` 0.99 · `క` 1.00 · `్య` 1.00 · `ము` 1.00 · `న` 1.00 · `␣ని` 1.00 · `ల` 1.00 · `్` 1.00 · `ల` 1.00 · `ె` 1.00 · `ను` 1.00 · `ను` 1.00 · `గా` 1.00 · `య` 1.00 · `ె` 1.00 · `ను` 1.00 · `ని` 1.00 · `ది` 1.00 · `న్` 1.00 · `␣` 1.00 · `ల్ల` 1.00 · `ె` 1.00 · `ను` 1.00 · `ము` 1.00 · `న` 1.00 · `వ` 1.00 · `్యా` 1.00 |

</details>

### Masking + backtracking

**Sample 1** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 56 · 254 tokens · 25.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్లగ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | తొం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్లగెనొకైతే | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | శ్రీం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్లగెనునిచ్యుం | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | తొం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్ల గల నం ఝ్లగెనులేతై | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 30% · single-akshara words 66% · repeated lines 0 · mean token probability (geometric) 0.525 · model's first choice kept 85% · constraint overrode 10% · backtracks 30

<details><summary>Token probabilities (254 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.07 · `్రీ` 0.40 · `ం` 0.03✱ · `␣` 2.1e-3 · `ఝ` 0.48 · `్` 2.6e-3✱ · `ల` 0.02 · `␣గ` 0.03 · `ల` 0.06 · `␣న` 0.13 · `ం` 0.03✱ · `␣` 0.34 · `ఝ` 1.00 · `్` 0.97 · `ల` 1.00 · `␣గ` 0.39 · `ల` 0.89 · `␣న` 0.98 · `ం` 1.00 · `␣` 0.89 · `ఝ` 1.00 · `్` 0.96 · `ల` 0.99 · `␣గ` 0.68 · `ల` 0.97 · `␣న` 0.95 · `ం` 0.97 · `␣` 0.75 · `ఝ` 0.99 · `్` 0.97 · `ల` 0.98 · `␣గ` 0.29 · `ల` 0.95 · `␣న` 0.64 · `ం` 0.96 · `␣` 0.02✱ · `ఝ` 0.99 · `్` 0.96 · `ల` 0.95 · `␣గ` 0.04✱ · `ల` 0.99 · `␣న` 0.62 · `ం` 0.99 · `␣` 9.9e-3✱ · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 0.85 · `ల` 1.00 · `␣న` 0.94 · `ం` 1.00 · `␣` 0.07✱ · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 0.96 · `ల` 1.00 · `␣న` 0.97 · `ం` 1.00 · `␣` 0.32✱ · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `గ` 5.6e-5✱ · `్` 1.9e-5✱ · `⏎` 0.07 forced |
| 2 | `త` 0.03 · `ొ` 0.10✱ · `ం` 0.05✱ · `␣` 0.41 · `ఝ` 0.95 · `్` 0.85 · `ల` 0.97 · `␣గ` 0.89 · `ల` 0.98 · `␣న` 0.98 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 0.98 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `గ` 0.86 · `ె` 2.3e-4✱ · `న` 7.9e-4✱ · `ొ` 0.02✱ · `క` 7.3e-3✱ · `ై` 0.02✱ · `తే` 1.1e-3✱ · `⏎` 0.96 forced |
| 3 | `శ` 0.05 · `్రీ` 0.22 · `ం` 0.99 · `␣` 0.98 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 0.99 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 0.99 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `గ` 0.81 · `ె` 0.48 · `ను` 0.31 · `ని` 0.02✱ · `చ` 2.4e-3✱ · `్య` 1.4e-3✱ · `ు` 0.31✱ · `ం` 0.02✱ · `⏎` 0.99 forced |
| 4 | `త` 0.79 · `ొ` 0.99 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 1.00 · `ఝ` 1.00 · `్` 1.00 · `ల` 1.00 · `␣గ` 1.00 · `ల` 1.00 · `␣న` 1.00 · `ం` 1.00 · `␣` 0.99 · `ఝ` 1.00 · `్` 1.00 · `ల` 0.99 · `గ` 0.75 · `ె` 0.69 · `ను` 0.48 · `లే` 0.03 · `త` 0.03✱ · `ై` 0.34✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 49 · 200 tokens · 59.5 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | వాయుపుతనుడ్యుని వలెన్ యుగము దాటి లవణాన్ యనెను త్వంతుడెను సుగ్ యనెను భర్మ్యుడ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | శూయన గగన్రయమునై యుగము దాటి లవణాన్ యనెను త్వంతుడెను సుగ్ యనెను భర్మ్యుడ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | ప్రాయణమనే పయనమున్ యుగము దాటి లవణాన్ యనెను త్వంతుడెను సుగ్ యనెను భర్మ్యుడ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | భీయుడెను భీభరణుడెన్ యుగము దాటి లవణాన్ యనెను త్వంతుడెను సుగ్ యనెను భర్మ్యుడ్ | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 22% · single-akshara words 10% · repeated lines 0 · mean token probability (geometric) 0.185 · model's first choice kept 72% · constraint overrode 25% · backtracks 30

<details><summary>Token probabilities (200 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `వ` 0.47 · `ాయ` 1.00 · `ు` 1.00 · `పు` 0.69 · `త` 0.09✱ · `ను` 2.0e-4✱ · `డ` 0.41✱ · `్య` 2.6e-4✱ · `ు` 0.33 · `ని` 0.83 · `␣వ` 0.04✱ · `లె` 0.09✱ · `న` 0.13 · `్` 3.7e-5✱ · `␣` 7.8e-4✱ · `యు` 3.4e-7✱ · `గ` 0.79 · `ము` 0.30 · `␣దా` 0.44 · `టి` 0.61 · `␣ల` 0.18 · `వ` 1.1e-4✱ · `ణ` 0.95 · `ాన` 0.04✱ · `్` 1.1e-4✱ · `␣` 1.3e-3✱ · `యన` 4.2e-6✱ · `ె` 0.70 · `ను` 0.85 · `␣త` 5.1e-3✱ · `్వ` 0.39 · `ం` 0.32✱ · `తు` 0.01✱ · `డ` 0.14✱ · `ె` 0.14✱ · `ను` 0.29✱ · `␣సు` 1.4e-3✱ · `గ` 0.62 · `్` 1.0e-10✱ · `␣` 3.6e-6✱ · `యన` 2.4e-3✱ · `ె` 0.92 · `ను` 0.95 · `␣భ` 7.3e-4✱ · `ర` 0.06 · `్` 9.2e-4✱ · `మ` 0.78 · `్య` 0.07✱ · `ు` 0.45 · `డ` 0.35✱ · `్` 1.2e-4✱ · `⏎` 0.11 forced |
| 2 | `శ` 0.17 · `ూ` 0.03✱ · `యన` 2.3e-7✱ · `␣గ` 0.05✱ · `గ` 0.60 · `న` 0.90 · `్ర` 3.3e-5✱ · `య` 0.12✱ · `ము` 0.40 · `న` 0.50 · `ై` 0.04✱ · `␣యు` 9.6e-3✱ · `గ` 0.65 · `ము` 0.70 · `␣దా` 0.84 · `టి` 0.83 · `␣ల` 0.85 · `వ` 0.27✱ · `ణ` 0.93 · `ాన` 0.93 · `్` 0.89 · `␣` 0.90 · `యన` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣త` 0.86 · `్వ` 0.99 · `ం` 1.00 · `తు` 1.00 · `డ` 0.99 · `ె` 1.00 · `ను` 1.00 · `␣సు` 0.98 · `గ` 0.98 · `్` 0.98 · `␣` 0.93 · `యన` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣భ` 0.92 · `ర` 0.99 · `్` 0.99 · `మ` 0.99 · `్య` 1.00 · `ు` 1.00 · `డ` 1.00 · `్` 0.98 · `⏎` 0.92 forced |
| 3 | `ప` 0.11✱ · `్రా` 0.04✱ · `య` 2.1e-8✱ · `ణ` 0.67 · `మ` 0.04 · `నే` 0.03✱ · `␣ప` 0.07 · `య` 0.43 · `న` 0.39✱ · `ము` 0.70 · `న` 0.78 · `్` 1.4e-4✱ · `␣యు` 0.23 · `గ` 0.98 · `ము` 0.99 · `␣దా` 1.00 · `టి` 0.99 · `␣ల` 1.00 · `వ` 0.99 · `ణ` 1.00 · `ాన` 1.00 · `్` 0.99 · `␣` 1.00 · `యన` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣త` 1.00 · `్వ` 1.00 · `ం` 1.00 · `తు` 1.00 · `డ` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣సు` 1.00 · `గ` 1.00 · `్` 1.00 · `␣` 1.00 · `యన` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣భ` 1.00 · `ర` 1.00 · `్` 1.00 · `మ` 1.00 · `్య` 1.00 · `ు` 1.00 · `డ` 1.00 · `్` 1.00 · `⏎` 1.00 forced |
| 4 | `భ` 0.16 · `ీ` 0.44 · `యు` 1.4e-5✱ · `డ` 0.44 · `ె` 0.15✱ · `ను` 0.56 · `␣భ` 0.48 · `ీ` 0.33 · `భ` 0.25 · `రణ` 8.5e-3✱ · `ు` 0.29✱ · `డ` 0.76 · `ె` 0.32 · `న` 0.08✱ · `్` 0.24✱ · `␣యు` 0.96 · `గ` 1.00 · `ము` 1.00 · `␣దా` 1.00 · `టి` 1.00 · `␣ల` 1.00 · `వ` 1.00 · `ణ` 1.00 · `ాన` 1.00 · `్` 1.00 · `␣` 1.00 · `యన` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣త` 1.00 · `్వ` 1.00 · `ం` 1.00 · `తు` 1.00 · `డ` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣సు` 1.00 · `గ` 1.00 · `్` 1.00 · `␣` 1.00 · `యన` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣భ` 1.00 · `ర` 1.00 · `్` 1.00 · `మ` 1.00 · `్య` 1.00 · `ు` 1.00 · `డ` 1.00 · `్` 1.00 |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 70 · 176 tokens · 41.0 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తల్లిని తలప్యును తలప్ ల్లన తలప్యును తలప్ ల్లన ముకుందుని వలయ్ ల్లున ముకుందా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | కల్లని కనుల్రు కరుణాక్ ల్లన కనుల్రు కరుణాక్ ల్లన మదన్ర కరుణాక్ ల్లన ముకుందా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | ప్రాల్లని పలక్యును పలక్ ల్లన పలక్యును పలక్ ల్లన శివగ్రు పలకగ్ ల్లన ముకుందా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | నిల్లని నిలయ్మును నిలయ్ ల్లన నిలయ్మును నిలయ్ ల్లన జగత్ప్ర నిలయగ్ ల్లన ముకుందా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 41% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.176 · model's first choice kept 70% · constraint overrode 21% · backtracks 0

<details><summary>Token probabilities (176 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.80 · `ల్లి` 0.72 · `ని` 0.02✱ · `␣త` 0.11✱ · `ల` 0.97 · `ప` 0.21✱ · `్య` 2.3e-6✱ · `ు` 0.36 · `ను` 0.08 · `␣త` 0.48 · `ల` 0.34 · `ప` 0.18✱ · `్` 2.1e-7✱ · `␣` 1.6e-6✱ · `ల్ల` 3.2e-4✱ · `న` 0.10 · `␣త` 0.07 · `ల` 0.72 · `ప` 0.76 · `్య` 0.77 · `ు` 0.95 · `ను` 0.72 · `␣త` 0.49 · `ల` 0.97 · `ప` 0.97 · `్` 0.70 · `␣` 6.5e-3✱ · `ల్ల` 0.99 · `న` 0.88 · `␣ము` 5.4e-4✱ · `కు` 0.16✱ · `ందు` 0.11 · `ని` 0.39 · `␣వ` 2.8e-3✱ · `ల` 0.52 · `య` 0.07✱ · `్` 3.3e-4✱ · `␣` 9.7e-4✱ · `ల్లు` 1.6e-4✱ · `న` 0.19✱ · `␣ము` 0.03✱ · `కు` 0.91 · `ందా` 3.7e-4 · `⏎` 0.86 forced |
| 2 | `క` 0.02 · `ల` 0.03✱ · `్` 5.1e-9✱ · `ల` 0.93 · `ని` 0.17 · `␣క` 0.69 · `ను` 0.18 · `ల` 0.81 · `్రు` 1.8e-4✱ · `␣క` 0.63 · `రుణ` 0.41 · `ా` 0.17 · `క` 0.08✱ · `్` 4.6e-8✱ · `␣` 0.03✱ · `ల్ల` 6.0e-3✱ · `న` 0.56 · `␣క` 0.93 · `ను` 0.23 · `ల` 0.93 · `్రు` 0.95 · `␣క` 0.99 · `రుణ` 0.99 · `ా` 0.96 · `క` 0.98 · `్` 0.98 · `␣` 0.97 · `ల్ల` 1.00 · `న` 1.00 · `␣మ` 0.19 · `ద` 0.07✱ · `న` 0.03✱ · `్ర` 6.7e-4✱ · `␣క` 0.23 · `రుణ` 0.73 · `ా` 0.81 · `క` 0.91 · `్` 0.92 · `␣` 0.74 · `ల్ల` 0.99 · `న` 0.97 · `␣ము` 0.05✱ · `కు` 0.94 · `ందా` 0.70 · `⏎` 1.00 forced |
| 3 | `ప` 0.09 · `్రా` 0.21 · `ల్ల` 1.3e-7✱ · `ని` 0.67 · `␣ప` 0.46 · `ల` 0.51 · `క` 0.86 · `్య` 0.18 · `ు` 0.92 · `ను` 0.70 · `␣ప` 0.61 · `ల` 0.98 · `క` 0.94 · `్` 0.66 · `␣` 0.95 · `ల్ల` 0.96 · `న` 0.99 · `␣ప` 0.04✱ · `ల` 0.90 · `క` 0.99 · `్య` 0.99 · `ు` 1.00 · `ను` 1.00 · `␣ప` 1.00 · `ల` 1.00 · `క` 1.00 · `్` 1.00 · `␣` 1.00 · `ల్ల` 1.00 · `న` 1.00 · `␣శి` 0.04 · `వ` 0.56 · `గ` 9.1e-3 · `్రు` 0.02✱ · `␣ప` 0.65 · `ల` 1.00 · `క` 1.00 · `గ్` 2.3e-3✱ · `␣` 0.74 · `ల్ల` 0.99 · `న` 1.00 · `␣ము` 0.96 · `కు` 1.00 · `ందా` 1.00 · `⏎` 1.00 forced |
| 4 | `ని` 0.06 · `ల్ల` 0.24 · `ని` 0.96 · `␣ని` 0.53 · `ల` 0.14 · `య` 0.34 · `్` 0.08✱ · `ము` 0.11 · `ను` 0.77 · `␣ని` 1.00 · `ల` 0.98 · `య` 0.94 · `్` 0.94 · `␣` 0.99 · `ల్ల` 0.99 · `న` 1.00 · `␣ని` 1.00 · `ల` 1.00 · `య` 1.00 · `్` 1.00 · `ము` 1.00 · `ను` 1.00 · `␣ని` 1.00 · `ల` 1.00 · `య` 1.00 · `్` 1.00 · `␣` 1.00 · `ల్ల` 1.00 · `న` 1.00 · `␣జగ` 0.28 · `త్` 0.05✱ · `ప్ర` 0.15 · `␣ని` 0.96 · `ల` 1.00 · `య` 0.98 · `గ్` 0.04✱ · `␣` 0.99 · `ల్ల` 1.00 · `న` 1.00 · `␣ము` 1.00 · `కు` 1.00 · `ందా` 1.00 |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 174 tokens · 32.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | శ్రీ వనలయాన గమయించ్ వితరమున్యెన యెనుట్ వలెనునై వలెనునై వితరమున్యా | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 2 | భోవన సముద్రమున దాట్ వితరమున్యెన వలెన్ వితరమున్యెన వలెన్ వలెనముందే | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 3 | శైవన లఘున్యెన గమయ్ వితరమున్యెన వలెన్ వితరమున్యెన వలెన్ వలెనముందే | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |
| 4 | శ్రీవన లఘున్యెన గమయ్ వితరమున్యెన వలెన్ వితరమున్యెన వలెన్ వలెనముందే | `UIIIUIIIUIIIUIIIUIIIUIIIUIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 19% · single-akshara words 6% · repeated lines 0 · mean token probability (geometric) 0.156 · model's first choice kept 67% · constraint overrode 27% · backtracks 0

<details><summary>Token probabilities (174 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `శ` 0.07 · `్రీ` 0.40 · `␣వ` 0.06✱ · `న` 0.11✱ · `ల` 8.9e-3 · `య` 0.08 · `ాన` 0.12✱ · `␣గ` 0.19 · `మ` 0.87 · `య` 0.08✱ · `ించ` 0.17 · `్` 1.3e-6✱ · `␣` 2.4e-7✱ · `విత` 1.9e-6✱ · `ర` 0.18✱ · `ము` 0.13 · `న` 0.31 · `్య` 8.5e-5✱ · `ె` 0.29 · `న` 0.09✱ · `␣య` 1.6e-3✱ · `ె` 0.41 · `ను` 0.09 · `ట` 1.0e-3✱ · `్` 1.4e-4✱ · `␣` 1.4e-4✱ · `వల` 6.0e-7✱ · `ె` 0.81 · `ను` 0.05✱ · `న` 7.6e-4✱ · `ై` 0.01✱ · `␣వ` 9.5e-4✱ · `లె` 0.20 · `ను` 0.58 · `న` 0.05✱ · `ై` 0.91 · `␣` 2.8e-3✱ · `విత` 1.9e-5✱ · `ర` 0.91 · `ము` 0.87 · `న` 0.76 · `్యా` 6.2e-5✱ · `⏎` 0.60 forced |
| 2 | `భ` 0.09 · `ో` 0.03 · `వ` 0.13✱ · `న` 0.68 · `␣స` 0.05 · `ము` 0.97 · `ద్ర` 0.88 · `ము` 0.43 · `న` 0.16✱ · `␣దా` 0.53 · `ట` 0.26✱ · `్` 6.4e-6✱ · `␣` 4.9e-3✱ · `విత` 8.4e-3✱ · `ర` 0.95 · `ము` 0.87 · `న` 0.89 · `్య` 0.69 · `ె` 0.97 · `న` 0.94 · `␣వ` 0.03 · `లె` 0.26 · `న` 0.12✱ · `్` 9.0e-5✱ · `␣` 0.14✱ · `విత` 0.86 · `ర` 0.99 · `ము` 0.97 · `న` 0.97 · `్య` 0.07✱ · `ె` 0.92 · `న` 0.96 · `␣వ` 0.62 · `లె` 0.96 · `న` 0.56 · `్` 0.69 · `␣వ` 0.17 · `లె` 0.73 · `న` 0.40 · `ము` 3.0e-3✱ · `ందే` 5.5e-5 · `⏎` 0.90 forced |
| 3 | `శ` 0.13✱ · `ై` 0.04✱ · `వ` 0.02✱ · `న` 0.17 · `␣ల` 0.59 · `ఘ` 1.7e-4✱ · `ు` 0.99 · `న` 0.10✱ · `్య` 3.3e-3✱ · `ె` 0.41 · `న` 0.87 · `␣గ` 0.22✱ · `మ` 0.90 · `య` 0.63 · `్` 0.07✱ · `␣` 0.71 · `విత` 1.00 · `ర` 1.00 · `ము` 0.97 · `న` 0.98 · `్య` 0.93 · `ె` 0.99 · `న` 0.99 · `␣వ` 0.72 · `లె` 0.97 · `న` 0.71 · `్` 0.94 · `␣` 0.57 · `విత` 1.00 · `ర` 1.00 · `ము` 1.00 · `న` 1.00 · `్య` 1.00 · `ె` 1.00 · `న` 1.00 · `␣వ` 0.99 · `లె` 1.00 · `న` 0.93 · `్` 0.95 · `␣వ` 0.79 · `లె` 0.98 · `న` 0.81 · `ము` 0.94 · `ందే` 0.90 · `⏎` 1.00 forced |
| 4 | `శ` 0.03✱ · `్రీ` 0.19✱ · `వ` 0.01✱ · `న` 0.92 · `␣ల` 0.52 · `ఘ` 0.69 · `ు` 0.99 · `న` 0.91 · `్య` 0.91 · `ె` 0.98 · `న` 0.98 · `␣గ` 0.08✱ · `మ` 0.97 · `య` 0.87 · `్` 0.97 · `␣` 0.93 · `విత` 1.00 · `ర` 1.00 · `ము` 0.99 · `న` 1.00 · `్య` 0.99 · `ె` 1.00 · `న` 1.00 · `␣వ` 1.00 · `లె` 1.00 · `న` 0.98 · `్` 1.00 · `␣` 0.98 · `విత` 1.00 · `ర` 1.00 · `ము` 1.00 · `న` 1.00 · `్య` 1.00 · `ె` 1.00 · `న` 1.00 · `␣వ` 1.00 · `లె` 1.00 · `న` 0.99 · `్` 1.00 · `␣వ` 0.95 · `లె` 1.00 · `న` 0.98 · `ము` 0.99 · `ందే` 0.99 |

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

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 167 tokens · 27.7 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి మదికి తల్రుని మమల కరుణయే జగతికిలకెనగెనమ్మెను స్త్రిలొలకమున తేజో | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 2 | అలసిన దినాన అదుపుల దయను చూసెను తలల దులకమున్రు తలపుల తలకదిల్యో | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 3 | జలమున జలమ్యుని జగడన జ్యెలులన్రు జ్యెలులలొనమున జ్యెన్రు జ్యెననలొనమును స్త్రిల్యా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 4 | కలయకలయాన కరుణల కనుల కద్రిలని కనులకలలక్రిలని కనులకలలక్రిల్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 16% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.093 · model's first choice kept 51% · constraint overrode 34% · backtracks 0

<details><summary>Token probabilities (167 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.75 · `ొ` 2.4e-3✱ · `లి` 0.73 · `␣మ` 0.07 · `ది` 0.64 · `కి` 0.17✱ · `␣త` 0.29 · `ల` 0.43 · `్రు` 1.8e-6✱ · `ని` 0.51 · `␣మ` 0.16✱ · `మ` 0.78 · `ల` 3.4e-3✱ · `␣క` 0.05 · `రుణ` 0.88 · `యే` 0.08✱ · `␣జగ` 0.09✱ · `తి` 0.82 · `కి` 0.64 · `ల` 4.7e-3✱ · `కె` 8.9e-3✱ · `న` 0.41 · `గ` 0.19✱ · `ె` 6.5e-3✱ · `న` 0.09 · `మ్` 0.02✱ · `మె` 0.02✱ · `ను` 0.02✱ · `␣` 4.6e-4✱ · `స్త` 0.04✱ · `్రి` 0.01✱ · `ల` 0.04✱ · `ొ` 0.04✱ · `ల` 7.8e-3✱ · `క` 0.32 · `ము` 0.46 · `న` 0.33✱ · `␣తే` 4.4e-3✱ · `జ` 0.82 · `ో` 0.65 · `⏎` 1.3e-3 forced |
| 2 | `అ` 0.19 · `ల` 0.06✱ · `సిన` 0.63 · `␣ద` 0.20 · `ిన` 0.53 · `ాన` 0.10✱ · `␣అ` 0.22✱ · `దు` 2.1e-3✱ · `పు` 0.74 · `ల` 0.04✱ · `␣ద` 0.18 · `య` 0.31✱ · `ను` 0.05✱ · `␣చూ` 0.02✱ · `సె` 0.22 · `ను` 0.62 · `␣త` 0.09✱ · `ల` 0.09✱ · `ల` 0.02✱ · `␣ద` 0.04 · `ుల` 9.5e-3✱ · `క` 0.12 · `ము` 0.66 · `న` 0.84 · `్రు` 7.1e-7✱ · `␣త` 0.42 · `ల` 0.19✱ · `పు` 0.24 · `ల` 0.72 · `␣త` 0.26 · `ల` 0.21 · `క` 0.04 · `ది` 0.03 · `ల` 0.50 · `్య` 6.2e-4✱ · `ో` 0.55 · `⏎` 0.88 forced |
| 3 | `జ` 0.04 · `ల` 0.01✱ · `ము` 0.25 · `న` 0.26 · `␣జ` 0.48 · `ల` 0.34 · `మ` 0.06✱ · `్య` 2.9e-3✱ · `ు` 0.24 · `ని` 0.36 · `␣జగ` 0.09 · `డ` 1.7e-3✱ · `న` 0.13 · `␣జ` 0.24 · `్య` 0.29 · `ె` 5.8e-4✱ · `లు` 0.06 · `ల` 0.10 · `న` 7.6e-3✱ · `్రు` 6.0e-4✱ · `␣జ` 0.56 · `్య` 0.35 · `ె` 0.10✱ · `లు` 0.75 · `ల` 0.82 · `ల` 0.03✱ · `ొ` 0.06 · `న` 0.24 · `ము` 0.06 · `న` 0.65 · `␣జ` 0.30 · `్య` 0.43 · `ె` 0.65 · `న` 3.1e-3✱ · `్రు` 1.8e-3✱ · `␣జ` 0.66 · `్య` 0.90 · `ె` 0.91 · `న` 0.34 · `న` 0.08 · `ల` 0.11 · `ొ` 0.19 · `న` 0.49 · `ము` 0.30 · `ను` 0.13✱ · `␣` 0.02✱ · `స్త` 0.89 · `్రి` 0.67 · `ల` 0.56 · `్యా` 2.4e-4✱ · `⏎` 0.58 forced |
| 4 | `క` 0.12 · `ల` 0.50 · `య` 0.08 · `క` 0.29 · `ల` 0.62 · `య` 0.38 · `ాన` 0.02✱ · `␣క` 0.84 · `రుణ` 0.57 · `ల` 0.15✱ · `␣క` 0.62 · `ను` 0.06 · `ల` 0.84 · `␣క` 0.45 · `ద` 0.09 · `్రి` 1.3e-6✱ · `ల` 0.24 · `ని` 0.06 · `␣క` 0.75 · `ను` 0.27 · `ల` 0.79 · `క` 0.31 · `ల` 0.67 · `ల` 0.38 · `క` 0.08 · `్రి` 1.6e-4✱ · `ల` 0.84 · `ని` 0.37 · `␣క` 0.80 · `ను` 0.51 · `ల` 0.86 · `క` 0.50 · `ల` 0.90 · `ల` 0.51 · `క` 0.33 · `్రి` 0.63 · `ల` 0.82 · `్` 4.6e-6✱ |

</details>

**Sample 2** · topic T2 (హనుమంతుడు సముద్రమును దాటి లంకను చేరెను) · seed 70 · 180 tokens · 29.4 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పవనసుతమున్యెన లఘువుల జ్యతినిమ్ముతమున వెలుగని కొండల ననువున లఘువుల్యెన్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 2 | పవనసుతమున్యెన లఘువుల జ్యతినిమ్ముతమున సముదయమున్యెన ననువున లఘువుల్యెన్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 3 | అవధిని త్రువణ్యెన లఘువుల జ్యతినిమ్ముతమున లఘువుల యోగమున లవణమున లఘ్యమ్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 4 | లవణమున త్రువ్యెన లఘువుల జ్యతినిమ్ముతమున వనమున లఘ్యమొననువున లఘువుల్యెన్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.209 · model's first choice kept 69% · constraint overrode 25% · backtracks 0

<details><summary>Token probabilities (180 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.26 · `వ` 0.83 · `న` 0.99 · `సు` 0.35 · `త` 0.49 · `ము` 0.17✱ · `న` 0.47 · `్య` 6.3e-5✱ · `ె` 0.41 · `న` 0.18 · `␣ల` 0.07✱ · `ఘ` 1.7e-3✱ · `ు` 0.99 · `వు` 0.07✱ · `ల` 0.18 · `␣జ` 0.02 · `్య` 0.45 · `తి` 6.8e-4✱ · `ని` 0.16 · `మ్ము` 0.03✱ · `త` 3.2e-3✱ · `ము` 0.22✱ · `న` 0.14✱ · `␣వె` 1.0e-3✱ · `లు` 0.35 · `గ` 0.29 · `ని` 0.09 · `␣కొ` 5.2e-3✱ · `ండ` 0.43 · `ల` 0.66 · `␣న` 0.04✱ · `ను` 0.19 · `వు` 9.6e-4✱ · `న` 0.22 · `␣ల` 0.11✱ · `ఘ` 6.1e-3✱ · `ు` 0.99 · `వు` 0.79 · `ల` 0.76 · `్య` 1.9e-5✱ · `ె` 0.58 · `న` 0.71 · `్` 2.9e-6✱ · `⏎` 0.84 forced |
| 2 | `ప` 0.03 · `వ` 0.17 · `న` 0.99 · `సు` 0.84 · `త` 0.97 · `ము` 0.85 · `న` 0.91 · `్య` 0.95 · `ె` 1.00 · `న` 0.99 · `␣ల` 0.57 · `ఘ` 1.00 · `ు` 1.00 · `వు` 0.99 · `ల` 1.00 · `␣జ` 0.96 · `్య` 1.00 · `తి` 1.00 · `ని` 1.00 · `మ్ము` 1.00 · `త` 0.99 · `ము` 1.00 · `న` 0.99 · `␣స` 0.13 · `ము` 0.97 · `దయ` 2.7e-3✱ · `ము` 0.35 · `న` 0.70 · `్య` 8.5e-4✱ · `ె` 0.96 · `న` 0.98 · `␣న` 0.07 · `ను` 0.66 · `వు` 0.85 · `న` 0.56 · `␣ల` 0.73 · `ఘ` 1.00 · `ు` 1.00 · `వు` 1.00 · `ల` 0.99 · `్య` 0.96 · `ె` 1.00 · `న` 1.00 · `్` 0.90 · `⏎` 1.00 forced |
| 3 | `అ` 0.13 · `వ` 2.2e-3✱ · `ధి` 0.28 · `ని` 0.31✱ · `␣త` 0.07✱ · `్రు` 0.02✱ · `వ` 0.08✱ · `ణ` 0.03✱ · `్య` 0.08✱ · `ె` 0.95 · `న` 0.97 · `␣ల` 0.88 · `ఘ` 1.00 · `ు` 1.00 · `వు` 0.99 · `ల` 1.00 · `␣జ` 0.93 · `్య` 1.00 · `తి` 1.00 · `ని` 0.99 · `మ్ము` 1.00 · `త` 0.97 · `ము` 1.00 · `న` 0.99 · `␣ల` 0.54 · `ఘ` 3.7e-3✱ · `ు` 1.00 · `వు` 0.93 · `ల` 0.98 · `␣య` 0.02✱ · `ో` 0.16 · `గ` 0.92 · `ము` 0.73 · `న` 0.93 · `␣ల` 0.11✱ · `వ` 7.3e-4✱ · `ణ` 0.95 · `ము` 0.30 · `న` 0.89 · `␣ల` 0.14✱ · `ఘ` 1.00 · `్య` 2.9e-7✱ · `మ` 0.03✱ · `్` 1.2e-7✱ · `⏎` 0.12 forced |
| 4 | `ల` 0.07✱ · `వ` 0.06✱ · `ణ` 0.93 · `ము` 0.72 · `న` 0.71 · `␣త` 0.28✱ · `్రు` 0.96 · `వ` 0.99 · `్య` 4.8e-6✱ · `ె` 0.99 · `న` 1.00 · `␣ల` 1.00 · `ఘ` 1.00 · `ు` 1.00 · `వు` 1.00 · `ల` 1.00 · `␣జ` 0.99 · `్య` 1.00 · `తి` 1.00 · `ని` 1.00 · `మ్ము` 1.00 · `త` 0.99 · `ము` 1.00 · `న` 1.00 · `␣వ` 3.9e-3✱ · `న` 0.16✱ · `ము` 0.73 · `న` 0.83 · `␣ల` 0.36 · `ఘ` 0.99 · `్య` 0.08✱ · `మ` 0.74 · `ొ` 0.02✱ · `న` 0.33 · `ను` 0.05 · `వు` 0.39 · `న` 0.87 · `␣ల` 0.73 · `ఘ` 0.99 · `ు` 0.32✱ · `వు` 0.97 · `ల` 0.97 · `్య` 0.91 · `ె` 1.00 · `న` 0.99 · `్` 0.98 |

</details>

### Masking + backtracking

**Sample 1** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 158 tokens · 43.3 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | ప్రియుని మథనంబున లొనయెను లవణేశ్వరి సురయణమున సాగెను బ్రతియును పరమప్రా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 2 | ధ్వయిని రణరంగమున లయబడెను శ్రీమనుడి దయవృదమునక్రును నవనిధిని రణబ్రా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 3 | హ్వయిని రణరంగమున లయబడెను శ్రీమనుడి దయవృదమునక్రును నవనిధిని రణబ్రా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 4 | భయమున కదిల్రియెను లయబడెను శ్రీమనుడి దయవృదమునక్రును నవనిధిని రణబ్రా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 14% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.167 · model's first choice kept 63% · constraint overrode 27% · backtracks 30

<details><summary>Token probabilities (158 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.02✱ · `్రి` 0.11✱ · `యు` 0.48 · `ని` 0.55 · `␣మ` 0.02✱ · `థ` 0.04 · `నం` 0.26 · `బు` 0.39 · `న` 0.56 · `␣ల` 0.05✱ · `ొ` 8.9e-4✱ · `న` 0.02✱ · `య` 0.12✱ · `ె` 0.96 · `ను` 0.42 · `␣ల` 0.17✱ · `వ` 1.1e-3✱ · `ణ` 0.97 · `ేశ` 9.2e-3✱ · `్వ` 0.52 · `రి` 0.57 · `␣సు` 4.7e-3✱ · `ర` 0.13 · `య` 8.6e-3✱ · `ణ` 0.28 · `ము` 0.02✱ · `న` 0.28✱ · `␣సా` 9.2e-4✱ · `గ` 0.64 · `ె` 0.98 · `ను` 0.96 · `␣బ` 4.9e-5✱ · `్ర` 0.16✱ · `తి` 0.67 · `యు` 6.7e-3✱ · `ను` 0.20 · `␣పర` 3.6e-3 · `మ` 0.84 · `ప` 0.16 · `్రా` 0.06✱ · `⏎` 7.7e-9 forced |
| 2 | `ధ` 0.04 · `్వ` 4.6e-3✱ · `యి` 8.8e-4✱ · `ని` 0.47 · `␣ర` 0.39 · `ణ` 4.4e-3✱ · `రంగ` 0.29 · `ము` 0.74 · `న` 0.95 · `␣ల` 0.04 · `య` 1.6e-3✱ · `బ` 5.4e-3 · `డ` 0.12 · `ె` 0.95 · `ను` 0.95 · `␣శ్రీ` 0.03 · `మ` 0.09✱ · `ను` 0.05✱ · `డి` 0.05 · `␣ద` 0.06 · `య` 0.36✱ · `వ` 0.01✱ · `ృ` 0.27✱ · `ద` 2.3e-4✱ · `ము` 0.05✱ · `న` 0.78 · `క` 3.6e-4✱ · `్రు` 3.0e-5✱ · `ను` 0.25 · `␣న` 0.03 · `వ` 0.11 · `ని` 0.19 · `ధి` 0.11✱ · `ని` 0.38 · `␣ర` 0.10 · `ణ` 7.9e-3✱ · `బ` 0.03✱ · `్రా` 9.8e-3✱ · `⏎` 0.45 forced |
| 3 | `హ` 0.78 · `్వ` 7.3e-3✱ · `యి` 3.9e-3✱ · `ని` 0.91 · `␣ర` 0.08 · `ణ` 0.13✱ · `రంగ` 0.85 · `ము` 0.90 · `న` 0.98 · `␣ల` 0.60 · `య` 0.98 · `బ` 0.99 · `డ` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣శ్రీ` 0.95 · `మ` 1.00 · `ను` 1.00 · `డి` 1.00 · `␣ద` 0.98 · `య` 1.00 · `వ` 1.00 · `ృ` 1.00 · `ద` 1.00 · `ము` 1.00 · `న` 1.00 · `క` 1.00 · `్రు` 1.00 · `ను` 1.00 · `␣న` 0.99 · `వ` 1.00 · `ని` 1.00 · `ధి` 1.00 · `ని` 1.00 · `␣ర` 1.00 · `ణ` 1.00 · `బ` 1.00 · `్రా` 1.00 · `⏎` 0.86 forced |
| 4 | `భ` 0.11 · `య` 0.31 · `ము` 0.54 · `న` 0.31 · `␣క` 0.03 · `ది` 0.09✱ · `ల` 0.33 · `్రియ` 6.6e-7✱ · `ె` 0.60 · `ను` 0.69 · `␣ల` 0.38 · `య` 1.6e-3✱ · `బ` 0.50 · `డ` 0.96 · `ె` 0.98 · `ను` 0.98 · `␣శ్రీ` 0.64 · `మ` 0.75 · `ను` 1.00 · `డి` 0.95 · `␣ద` 0.81 · `య` 1.00 · `వ` 0.98 · `ృ` 1.00 · `ద` 1.00 · `ము` 1.00 · `న` 1.00 · `క` 0.99 · `్రు` 1.00 · `ను` 1.00 · `␣న` 0.97 · `వ` 1.00 · `ని` 1.00 · `ధి` 1.00 · `ని` 1.00 · `␣ర` 1.00 · `ణ` 1.00 · `బ` 0.99 · `్రా` 1.00 |

</details>

**Sample 2** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 56 · 159 tokens · 53.9 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి మధుర స్వప్నమున తలపుల తొలిప్రియురలొలికెనుమునందున కనలకల పలిక్యా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 2 | వలికల వినయ్య మదిని లలితముగా లలకల లలితముగా లలితముడెనుమునదిక్యా | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 3 | తొలపుల తలవ్రిణతనుల తలపులత్యుల తలలపలపులత్యుల తలలపలకయెన్రో | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 4 | అలలల అమృత్ర లలకలలలలలల్ర లలకలలలలలల్ర లలకలలలలలల్రన్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 12% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.086 · model's first choice kept 50% · constraint overrode 39% · backtracks 30

<details><summary>Token probabilities (159 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.75 · `ొ` 2.4e-3✱ · `లి` 0.71 · `␣మ` 0.06 · `ధు` 0.01 · `ర` 0.69 · `␣స్వ` 0.03 · `ప్` 8.3e-3✱ · `న` 0.78 · `ము` 0.21✱ · `న` 0.32 · `␣త` 0.18✱ · `ల` 0.24✱ · `పు` 0.51 · `ల` 0.43 · `␣తొలి` 6.3e-3✱ · `ప` 2.2e-3✱ · `్రి` 0.01✱ · `యు` 0.08✱ · `ర` 0.83 · `ల` 4.0e-3✱ · `ొ` 0.04✱ · `లి` 2.4e-3✱ · `కె` 0.15✱ · `ను` 0.49 · `ము` 3.4e-3✱ · `న` 0.01✱ · `ందు` 2.7e-3✱ · `న` 0.10✱ · `␣క` 1.8e-3✱ · `న` 0.04✱ · `ల` 0.01✱ · `క` 0.05✱ · `ల` 0.20 · `␣ప` 1.3e-3✱ · `లి` 0.12 · `క` 0.02✱ · `్యా` 1.6e-4✱ · `⏎` 7.5e-4 forced |
| 2 | `వ` 5.1e-3 · `లి` 1.8e-3✱ · `క` 9.9e-3 · `ల` 0.52 · `␣వి` 0.12 · `న` 0.10 · `య` 0.35 · `్య` 1.5e-4✱ · `␣మ` 0.05✱ · `ది` 0.55 · `ని` 0.12✱ · `␣ల` 1.9e-3✱ · `లి` 0.03✱ · `త` 0.84 · `ము` 0.15✱ · `గా` 0.22 · `␣ల` 0.12 · `ల` 0.02✱ · `క` 0.17✱ · `ల` 0.37 · `␣ల` 0.54 · `లి` 0.05✱ · `త` 0.80 · `ము` 0.31 · `గా` 0.50 · `␣ల` 0.65 · `లి` 0.31 · `త` 0.85 · `ము` 0.55 · `డ` 4.1e-4✱ · `ె` 0.08✱ · `ను` 0.58 · `ము` 0.16 · `న` 0.84 · `ది` 0.01✱ · `క` 7.5e-3✱ · `్యా` 1.6e-3✱ · `⏎` 0.97 forced |
| 3 | `త` 0.32 · `ొ` 0.02✱ · `ల` 0.26 · `పు` 0.19 · `ల` 0.60 · `␣త` 0.61 · `ల` 0.33 · `వ` 9.9e-3✱ · `్రి` 2.7e-5✱ · `ణ` 0.01✱ · `త` 0.12✱ · `ను` 0.17 · `ల` 0.02✱ · `␣త` 0.61 · `ల` 0.47 · `పు` 0.43 · `ల` 0.88 · `త` 0.01✱ · `్య` 5.8e-5✱ · `ు` 0.07 · `ల` 0.19 · `␣త` 0.45 · `ల` 0.75 · `ల` 0.04✱ · `ప` 0.15 · `ల` 0.27 · `పు` 0.05 · `ల` 0.62 · `త` 0.04✱ · `్య` 0.53 · `ు` 0.91 · `ల` 0.80 · `␣త` 0.52 · `ల` 0.92 · `ల` 0.44 · `ప` 0.50 · `ల` 0.79 · `క` 0.73 · `య` 3.3e-4✱ · `ె` 0.02✱ · `న` 0.08✱ · `్రో` 1.3e-4✱ · `⏎` 0.08 forced |
| 4 | `అ` 0.23 · `ల` 0.11✱ · `ల` 0.61 · `ల` 0.52 · `␣అమ` 0.11✱ · `ృత` 0.88 · `్ర` 4.1e-5✱ · `␣ల` 0.01 · `ల` 0.02✱ · `క` 0.47 · `ల` 0.94 · `ల` 0.35 · `ల` 0.29 · `ల` 0.62 · `ల` 0.77 · `ల` 0.80 · `్ర` 2.5e-5✱ · `␣ల` 0.27 · `ల` 0.41 · `క` 0.66 · `ల` 0.99 · `ల` 0.69 · `ల` 0.86 · `ల` 0.96 · `ల` 0.86 · `ల` 0.79 · `్ర` 0.03✱ · `␣ల` 0.65 · `ల` 0.82 · `క` 0.87 · `ల` 0.96 · `ల` 0.87 · `ల` 0.93 · `ల` 0.85 · `ల` 0.88 · `ల` 0.78 · `్ర` 0.69 · `న` 0.01✱ · `్` 2.1e-5✱ |

</details>

### Hybrid (mask + accept-state re-ranking)

**Sample 1** · topic T1 (తల్లి ప్రేమ అన్నింటికంటే గొప్పది) · seed 42 · 228 tokens · 38.2 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | తొలి మదికి తల్రుని మమలము నిను పోషకెనులెడెడెడెడెడెడ్యెడెడెడెడెడెడెడెడెడ్యూ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 2 | నిలకడల నిత్యత నినుల నిలిపినెడ్యెడెడెడెడెడెడెడెడెడ్యెడెడెడెడెడెడెడెడెడ్యూ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 3 | ప్రెలియల ప్రియత్య నినులలలలలలల్రెడెడెడెడెడెడెడెడెడ్యెడెడెడెడెడెడెడెడెడ్యూ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 4 | తొలి తపన తండ్రి తలపుల తలపొలెడ్యెడెడెడెడెడెడెడెడెడ్యెడెడెడెడెడెడెడెడెడ్యూ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 28% · single-akshara words 0% · repeated lines 0 · mean token probability (geometric) 0.299 · model's first choice kept 76% · constraint overrode 19% · backtracks 0

<details><summary>Token probabilities (228 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `త` 0.75 · `ొ` 2.4e-3✱ · `లి` 0.73 · `␣మ` 0.07 · `ది` 0.64 · `కి` 0.17✱ · `␣త` 0.29 · `ల` 0.43 · `్రు` 1.8e-6✱ · `ని` 0.51 · `␣మ` 0.16✱ · `మ` 0.78 · `ల` 3.4e-3✱ · `ము` 0.06 · `␣ని` 0.07 · `ను` 0.02✱ · `␣పో` 0.14 · `ష` 0.81 · `కె` 4.8e-4✱ · `ను` 0.67 · `ల` 4.4e-3✱ · `ె` 0.02✱ · `డ` 1.7e-3✱ · `ె` 0.07✱ · `డ` 2.5e-3✱ · `ె` 0.36✱ · `డ` 0.05✱ · `ె` 0.66 · `డ` 0.50 · `ె` 0.87 · `డ` 0.72 · `ె` 0.87 · `డ` 0.72 · `్య` 8.1e-4✱ · `ె` 0.70 · `డ` 0.30✱ · `ె` 0.85 · `డ` 0.79 · `ె` 0.71 · `డ` 0.92 · `ె` 0.75 · `డ` 0.92 · `ె` 0.73 · `డ` 0.88 · `ె` 0.68 · `డ` 0.88 · `ె` 0.77 · `డ` 0.91 · `ె` 0.79 · `డ` 0.92 · `ె` 0.81 · `డ` 0.92 · `్యూ` 1.2e-5✱ · `⏎` 0.85 forced |
| 2 | `ని` 0.03 · `ల` 6.1e-3✱ · `క` 0.25 · `డ` 0.99 · `ల` 0.21✱ · `␣ని` 0.14 · `త్య` 0.27 · `త` 0.01 · `␣ని` 0.14 · `ను` 0.43 · `ల` 3.0e-3✱ · `␣ని` 0.15 · `లి` 0.07✱ · `ప` 0.28✱ · `ిన` 0.33 · `ె` 0.05✱ · `డ` 0.22✱ · `్య` 4.5e-3✱ · `ె` 0.98 · `డ` 0.99 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 0.91 · `డ` 1.00 · `ె` 0.80 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `్య` 1.8e-4✱ · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 0.97 · `డ` 1.00 · `ె` 0.83 · `డ` 0.99 · `ె` 0.66 · `డ` 1.00 · `ె` 0.13✱ · `డ` 0.99 · `ె` 0.26✱ · `డ` 0.99 · `ె` 0.36✱ · `డ` 0.99 · `ె` 0.45✱ · `డ` 0.99 · `్యూ` 0.33✱ · `⏎` 0.99 forced |
| 3 | `ప్ర` 0.05 · `ె` 6.4e-6✱ · `లి` 1.4e-4✱ · `య` 0.57 · `ల` 0.25 · `␣ప్రి` 0.06✱ · `య` 0.96 · `త` 0.73 · `్య` 1.5e-3✱ · `␣ని` 0.39 · `ను` 0.79 · `ల` 0.70 · `ల` 7.0e-4✱ · `ల` 0.06 · `ల` 0.54 · `ల` 0.59 · `ల` 0.64 · `ల` 0.75 · `్ర` 4.8e-5✱ · `ె` 0.03 · `డ` 0.82 · `ె` 0.82 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `్య` 1.0e-3✱ · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 0.99 · `డ` 1.00 · `్యూ` 0.40✱ · `⏎` 1.00 forced |
| 4 | `త` 0.21 · `ొ` 0.02✱ · `లి` 0.53 · `␣త` 0.22 · `ప` 0.05 · `న` 0.73 · `␣త` 0.37 · `ండ` 0.23 · `్రి` 0.73 · `␣త` 0.34 · `ల` 0.68 · `పు` 0.46 · `ల` 0.52 · `␣త` 0.51 · `ల` 0.52 · `ప` 0.10 · `ొ` 0.02 · `ల` 0.24 · `ె` 0.25 · `డ` 0.71 · `్య` 0.14✱ · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 0.93 · `డ` 1.00 · `్య` 0.32✱ · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `ె` 1.00 · `డ` 1.00 · `్యూ` 0.13✱ |

</details>

**Sample 2** · topic T3 (శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను) · seed 70 · 175 tokens · 48.6 s

| పాదము | line | gaṇa pattern (U = guru, I = laghu) |
|---|---|---|
| 1 | పగలు వెలెనున్ లఘురు గొగలి కమలమ్య గమయె గరపుడెనిన్ రణమున గరపుడెనిన్ విన్ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 2 | చొగెను సముదర్ఱును నరగుణుల మరువ్యెను తప గమయెను తప్యెను కనుగొని రథమున్రీ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 3 | కృగమయెను లంకయెను కగరపుడెనిన్ భయమున గమయెను భయ్యెను కనుగొని శిరమున్రీ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |
| 4 | జగమయెను లంకయెను కగరపుడెనిన్ రణమున గమయెను రణ్యెను కనుగొని జయమున్రీ | `IIIIIUIIIIIIIIUIIIIIIIIUIIIIIIIIUU` |

Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) 23% · single-akshara words 3% · repeated lines 0 · mean token probability (geometric) 0.130 · model's first choice kept 59% · constraint overrode 28% · backtracks 0

<details><summary>Token probabilities (175 tokens)</summary>

| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |
|---|---|
| 1 | `ప` 0.02✱ · `గ` 0.11✱ · `లు` 0.57 · `␣వె` 0.11 · `లె` 0.01✱ · `ను` 0.68 · `న్` 2.6e-3✱ · `␣ల` 0.20 · `ఘ` 1.0e-4✱ · `ు` 0.99 · `రు` 0.07 · `␣గ` 0.09 · `ొ` 5.4e-3✱ · `గ` 1.7e-3✱ · `లి` 0.42 · `␣క` 0.03 · `మ` 0.11✱ · `ల` 0.87 · `మ` 0.06✱ · `్య` 0.01✱ · `␣గ` 9.3e-3 · `మ` 0.47 · `య` 0.11✱ · `ె` 0.26 · `␣` 4.5e-4✱ · `గర` 1.0e-5✱ · `పు` 0.04 · `డ` 0.04✱ · `ె` 0.18✱ · `ని` 0.03✱ · `న్` 0.04✱ · `␣ర` 4.8e-4✱ · `ణ` 0.01✱ · `ము` 0.49 · `న` 0.25✱ · `␣` 5.2e-3✱ · `గర` 7.8e-5✱ · `పు` 0.56 · `డ` 0.83 · `ె` 0.98 · `ని` 0.88 · `న్` 0.97 · `␣వి` 2.4e-3✱ · `న్` 3.4e-3 · `⏎` 2.4e-5 forced |
| 2 | `చ` 0.04 · `ొ` 9.5e-4✱ · `గ` 8.7e-4✱ · `ె` 0.19✱ · `ను` 0.71 · `␣స` 0.02✱ · `ము` 0.75 · `ద` 0.03✱ · `ర` 0.60 · `్` 1.7e-5✱ · `ఱ` 0.52 · `ు` 0.46 · `ను` 0.04 · `␣న` 0.07 · `ర` 0.11 · `గు` 4.3e-3✱ · `ణ` 0.55 · `ుల` 0.05 · `␣మ` 0.02✱ · `రు` 0.05✱ · `వ` 0.61 · `్య` 1.7e-3✱ · `ె` 0.40 · `ను` 0.19✱ · `␣త` 0.05 · `ప` 0.23 · `␣గ` 1.1e-3✱ · `మ` 0.29 · `య` 0.47 · `ె` 0.98 · `ను` 0.82 · `␣త` 0.12 · `ప` 0.46 · `్య` 5.2e-3✱ · `ె` 0.03 · `ను` 0.84 · `␣క` 0.02 · `ను` 0.04✱ · `గొ` 0.03 · `ని` 0.46 · `␣ర` 0.08✱ · `థ` 0.01✱ · `ము` 0.69 · `న` 0.78 · `్రీ` 8.7e-7✱ · `⏎` 0.74 forced |
| 3 | `క` 0.08 · `ృ` 4.3e-4✱ · `గ` 2.4e-4✱ · `మ` 0.48 · `య` 0.56 · `ె` 0.97 · `ను` 0.93 · `␣ల` 0.11 · `ంక` 0.65 · `య` 0.07✱ · `ె` 0.60 · `ను` 0.76 · `␣క` 0.12 · `గర` 3.3e-4✱ · `పు` 0.45 · `డ` 0.78 · `ె` 0.96 · `ని` 0.95 · `న్` 0.99 · `␣భ` 0.08 · `య` 0.62 · `ము` 0.56 · `న` 0.52 · `␣గ` 0.03✱ · `మ` 0.73 · `య` 0.94 · `ె` 1.00 · `ను` 0.99 · `␣భ` 0.39 · `య` 0.89 · `్య` 0.25✱ · `ె` 0.83 · `ను` 0.99 · `␣క` 0.18 · `ను` 0.63 · `గొ` 0.97 · `ని` 0.99 · `␣శి` 0.07 · `ర` 0.89 · `ము` 0.16✱ · `న` 0.96 · `్రీ` 0.76 · `⏎` 1.00 forced |
| 4 | `జ` 0.05 · `గ` 0.07✱ · `మ` 0.75 · `య` 0.96 · `ె` 1.00 · `ను` 1.00 · `␣ల` 0.05 · `ంక` 0.29 · `య` 0.62 · `ె` 0.96 · `ను` 0.99 · `␣క` 0.74 · `గర` 0.95 · `పు` 0.99 · `డ` 1.00 · `ె` 1.00 · `ని` 1.00 · `న్` 1.00 · `␣ర` 0.52 · `ణ` 0.01✱ · `ము` 0.87 · `న` 0.99 · `␣గ` 0.88 · `మ` 0.98 · `య` 1.00 · `ె` 1.00 · `ను` 1.00 · `␣ర` 0.93 · `ణ` 0.99 · `్య` 0.99 · `ె` 0.99 · `ను` 1.00 · `␣క` 0.96 · `ను` 0.99 · `గొ` 0.99 · `ని` 1.00 · `␣జ` 0.18 · `య` 0.97 · `ము` 0.92 · `న` 0.99 · `్రీ` 0.95 |

</details>

[↑ meters](#meters)

---


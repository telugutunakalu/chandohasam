# 02 — Svara yatis [6.2 – 6.8]

Source: `../yathi.md` parts 1–3. Overlaps `../yathi1.md` Y3, Y7 and `../yathi2.md` Y10–Y12.

## A. The vowel classes [6.2 – 6.2.1]

- **YATI-SV-01** `=Y3.1` **స్వరమైత్రి వర్గములు** — three mutually exclusive classes; any two vowels of one class pair bidirectionally; **no exception**; every consonant yati's vowels must also obey this grid:
  - `A` = {అ ఆ ఐ ఔ}
  - `I` = {ఇ ఈ ఋ ౠ ఎ ఏ} (+ ఌ by ఋ–ఌ sāvarṇya, `YATI-DL-01`)
  - `U` = {ఉ ఊ ఒ ఓ}
  status: canonical (kind: bhēda).
- **YATI-SV-01.1** `=Y3.2` A consonant akshara = consonant maitri **AND** vowel maitri: "క–గ చెల్లును" means క్–గ్ with same-class vowels (క–గ, కా–గై, కౌ–గ yes; క–గి no). status: mandatory.
- **YATI-SV-01.2** `=Y7.10` Cross-class vowel pairs never occur in the corpus (0 of 175 svara-pradhāna examples) — usable as an engine consistency check. status: informational.

## B. స్వరప్రధాన యతి — the sandhi rule [6.3 – 6.3.11]

- **YATI-SV-02** `=Y7.1` [6.3] When the akshara at the yati site (or at the వళి, or both) is the **product of a sandhi**, the sound tested is the **initial vowel of the second word (పరపదాది స్వరము)**, never the resulting consonant or surface orthography. (Prāsa, by contrast, tests the surface consonant.) status: canonical (kind: vidhāna).
- **YATI-SV-02.1** `=Y7.2` [6.3.1] Scope: any junction of two words where the second begins with a vowel, whether or not a formal స్వరసంధి applies.
- **YATI-SV-02.2** `=Y7.3` Sandhi types covered (all resolve to the second word's vowel):
  - సవర్ణదీర్ఘ: వేద+అర్థ=వేదార్థ → అ; గుణ: పరమ+ఈశ్వర=పరమేశ్వర → ఈ; పూర్వరూప: విశ్వకర్తే+అక్షరాయ → అ (ఓ+అ=ఓ, ఏ+అ=ఏ hide అ).
  - జశ్త్వ: దృక్+అంచల=దృగంచల → అ; విసర్గ sandhi: చతుః+అబ్ధి=చతురబ్ధి → అ.
  - Telugu ఉత్వ (భూమిసురుఁడు+అంబర → అ), ఇత్వ (నాది+ఐన=నాదైన → ఐ), అత్వ (పాలనున్న+అప్పుడు → అ).
  - **ద్రుతము + vowel** [6.3.4]: న్+V → న/నా/ని/ను etc. is tested as **V only**; a consonant match with న is prohibited (నగరిలోన్+ఆ → ఆ; సేరుటకున్+ఎద్ది → ఎ).
  - **యడాగమము + vowel** [6.3.5]: య్+V → య/యా/యి is tested as **V only**; no consonant match with య (తరుణి+య్+అమ్ముని → అ). See `YATI-VY-09.1` for śabda-siddha vs āgama య.
  - వృద్ధి sandhi → dual option `YATI-SV-09`; ఋ as second vowel → `YATI-SV-03`.
- **YATI-SV-02.3** `=Y7.4` [6.3.6] **Both ends**: the వళి itself may be a sandhi product (భాషా+అపర ↔ వివిధ+అధ్వర → అ–అ; దేశాళితోన్+ఆది ↔ అజితుండు+ఐ → ఆ–ఐ). status: canonical.
- **YATI-SV-02.4** `=Y7.5` Only the sandhi akshara is affected; other aksharas of the word keep ordinary consonant yatis (కవీశ్వర: వీ→ఈ, but క/శ్వ/ర are consonant yatis).
- **YATI-SV-02.5** `=Y7.6` The ద్రుతము elides when sandhi happens (నందున్+అతని → నందతని); optional (vikalpa) sandhis (ఇంకేల / ఇంకనేల) are decided by the printed text.
- **YATI-SV-02.6** `=Y7.7` If the second element is an అపదము (రెండు+అవ, -ఎడు, -ఎడి, -ఏసి …) the rule *may* apply → see విభాగ rules `YATI-UB-03/04/05` and `YATI-DL-12`.
- **YATI-SV-02.7** `=Y7.9` [6.3.8] స్వరయతి (`YATI-SV-01`) is the *bhēda*; స్వరప్రధానయతి is the *vidhāna*; the second always resolves through the first.
- **YATI-SV-02.8** `=Y10.6` [6.3.11] Ignoring a transparent junction and making a consonant yati on the surface akshara is **అఖండయతి** → `YATI-RJ-01` (forbidden).
- **YATI-SV-02.10** [6.3.6; borrowed from `telugu_prosody_engine` `experimental_sandhi`] **అచ్చు-ఆధారిత సంధి యతి** (vowel-only acceptance): when the engine runs in sandhi mode `acchu`, two coordinates whose vowels share a class pair even without printed or lexical evidence of a sandhi on either side. This approximates the book's two-sided case (SV-02.3) when no lexicon is available; every such match is flagged as a hypothesis. The legacy checker applied it as an *override* of the consonant verdict; here it is an *additive* path only. status: accepted_relaxation (mode-gated).
- **YATI-SV-02.9** [6.10.4] **Prāṇi-vs-svara-pradhāna trap**: before classifying an apparent consonant identity (వొ–వు, నే–ని, లె–లె, డి–డీ) as ప్రాణియతి, test for a sandhi boundary (నీవు+ఒక్కరుఁడవ ↔ ఉన్నవాఁడవు+ఉర్వీ → ఒ–ఉ svara-pradhāna). status: mandatory (procedure `YATI-EP-03`).

## C. Bare vowels inside a line; ఋ [6.3.10]

- **YATI-SV-03** `=Y10.1` A bare vowel letter normally occurs only as the first akshara of pāda 1; elsewhere a word-initial vowel has fused with the previous word (so in-line vowel–vowel yatis arise *through* `YATI-SV-02`). status: informational.
- **YATI-SV-03.1** `=Y10.2` **ఋ is the exception**: ఋషి, ఋణము, ఋతము stand unfused anywhere (వాఁడు ఋషి). Bare ఋ pairs *directly* with any `I`-class vowel (ఇ ఈ ఎ ఏ ఋ) as a plain svara yati (ఇ↔ఋ Kāśī 2-74; ఈ↔ఋ; ఋ↔ఋ Bhāratam Ādi 5-71). status: canonical.
- **YATI-SV-03.2** `=Y10.3` ఋ as పరపదాది స్వరము (మాతృ+ఋణము=మాతౄణము, దేవ+ఋషి=దేవర్షి): the junction is evaluated as ఋ (ఎ↔ఋ). status: canonical.
- **YATI-SV-03.3** `=Y10.5` The vowel ఌ occurs only in క్ఌప్త (and derivatives) → `YATI-DL-01`.

## D. లుప్తవిసర్గక / గూఢస్వర యతి [6.4 – 6.4.8]

- **YATI-SV-04** `=Y11.1` [6.4] Sanskrit compound, first member ends in short **అ + విసర్గ/అస్** (దాసః, మనస్, తపస్, వక్షస్, వచస్), second begins with short **అ**: rutva → ఉ → గుణ ఓ → పూర్వరూప swallows the అ (avagraha ఽ, usually unwritten): దాసోఽహమ్, మనోబ్జ, తపోనల, వక్షోలంకార, వచోమృత. A yati on that ఓ-akshara (సో, నో, పో, తో, ధో, రో …) is to the **hidden short అ** (`A` class); consonant yatis of సో/నో are **not** allowed there. status: canonical (kind: vidhāna).
- **YATI-SV-04.1** `=Y11.4` [6.4.3] **అన్యోన్య** (అన్య+అన్య, reciprocal): న్యో resolves to అ. It is *also* listed among the నిత్యసమాస ubhaya yatis, so a consonant match on నో (prāṇi) or యో (sarasa) is allowed too (`YATI-UB-11`). status: canonical.
- **YATI-SV-04.2** `=Y11.5` [6.4.5–6.4.6] Appakavi's framing "ఓ matches అ, య, హ" is a category error (ఓ is `U` class); Anantudu's గూఢస్వరయతి (hidden vowel) is the accurate rule — the match is to the concealed అ, not to ఓ. status: informational.
- **YATI-SV-04.3** `=Y11.3` [6.4.7] **Negative**: విసర్గ/అస్ → ఓ before a **voiced consonant** (యశోనాశము, మనోరథము, అంభోయాన, శివోవన్ద్యః) hides no vowel; the caesura is an ordinary consonant yati on శో/నో/భో. status: mandatory.
- **YATI-SV-04.4** Plain పూర్వరూప ఓ+అ=ఓ, ఏ+అ=ఏ without visarga also hides అ — that is ordinary `YATI-SV-02`, not this rule. status: informational.

## E. ఋ యతి / రివడి [6.5 – 6.5.4]

- **YATI-SV-05** `=Y12.1` [6.5] Vocalic **ఋ ↔ {రి రీ రె రే}** (ర్ + `I`-class vowel). Rationale: ఋ is pronounced with a రేఫ and belongs to `I`. **Not** with రు/రూ/ర/రా (breaches `I`). A vowel pairing with a consonant is the peculiarity of this yati (shared only with the సరసయతి అ–య–హ). Summary `=Y12.6` [6.5.4]: (1) ఋ↔రి-series; (2) ఋ↔conjunct containing రి; (3) C+ృ↔రి-series; (4) C+ృ↔conjunct containing రి. status: canonical (kind: bhēda).
- **YATI-SV-05.1** `=Y12.2` [6.5.1] The రి/రీ/రె/రే may sit inside a conjunct as either member (ఋ↔ర్చి, ఋ↔త్రీ, బ్రీ↔ఋ) — సంయుక్తయతి `YATI-SY-01` extracts the ర్. status: canonical.
- **YATI-SV-05.2** `=Y12.3` [6.5.2] **వట్రసుడి** (C+ృ: కృ గృ ఘృ దృ నృ పృ బృ భృ మృ వృ …) pairs with రి/రీ/రె/రే exactly like bare ఋ; the host consonant is bypassed (నృ↔రి, కృ↔రీ, రె↔దృ, కృ↔రే). status: canonical.
- **YATI-SV-05.3** `=Y12.4` Cluster-to-cluster: కృ↔ప్రి, వృ↔శ్రీ, కృ↔శ్రే, కృ↔ర్మి; and C1C2+ఋ (ద్వృ). status: canonical.
- **YATI-SV-05.4** `=Y12.5` [6.5.3] **మహత్త్వము**: ఋ is the only vowel allowed to detach from its host consonant for a yati (అ–క, ఇ–కి, ఉ–కు are never yatis). status: mandatory (see `YATI-RJ-17`).
- **YATI-SV-05.5** [6.38.3] Late-mode extension via ద్విరేఫ (`YATI-SP-08`): ఋ / C+ృ ↔ ఱి ఱీ ఱె ఱే (కృ↔ఱి, గృ↔ఱె, ఱే↔నృ). status: orthographic_relaxation (follows ర/ఱ decision).

## F. ఋత్వసంబంధ యతి [6.6 – 6.6.2]

- **YATI-SV-06** [6.6] **C+ఋ (వట్రసుడి) ↔ independent `I`-class vowel** {ఇ ఈ ఋ ౠ ఎ ఏ}; the host consonant is disregarded (ఇ↔గృ, ఈ↔కృ, ఈ↔భృ, ఎ↔నృ, ఏ↔మృ, ఏ↔వృ, మృ↔ఎ). Multi-consonant clusters with ృ (ష్కృ) are bypassed wholly (ష్కృ↔ఏ). The other side may itself be a sandhi-resolved vowel (న్+ఇందు → ఇ ↔ కృ; రహితుఁడు+ఎత్తెఱంగున → ఎ ↔ మృ). status: canonical (kind: vidhāna + bhēda).
- **YATI-SV-06.1** [6.6.1] Unique exception, as `YATI-SV-05.4`: no other bound vowel may do this (కి↔ఇ is invalid).
- **YATI-SV-06.2** [6.6.2] Lines like ని…నృ or కృ…కే are *also* valid as ప్రాణియతి; the book classifies them under ఋత్వసంబంధ — the engine may report either. status: informational.

## G. ఋత్వసామ్య యతి [6.7 – 6.7.3]

- **YATI-SV-07** [6.7] **C1+ఋ ↔ C2+ఋ** for *any* C1, C2, even without consonant affinity (మృ↔గృ, హృ↔మృ, భృ↔కృ, పృ↔కృ, గృ↔శృ, తృ↔కృ, ఘృ↔నృ); clusters too (స్కృ↔దృ, స్మృ↔వృ). The caesura is authenticated by the two ృ markers alone. status: canonical (kind: bhēda).
- **YATI-SV-07.1** [6.7.1] Exclusively for ఋ: క≠ప, కి≠పి, కు≠పు, గ≠శ but గృ↔శృ. status: mandatory.
- **YATI-SV-07.2** [6.7.2] Appakavi's వృ↔పృ example is a weak illustration (వ–ప already pair under అభేదవర్గ). status: informational.

## H. వృద్ధి యతి [6.8 – 6.8.3]

- **YATI-SV-08** [6.8] **వృద్ధి sandhi**: అ/ఆ + ఏ/ఐ → **ఐ**; అ/ఆ + ఓ/ఔ → **ఔ** (భోగైక, రక్షైక, బలౌఘ, వనౌకస, లంకౌక, దుఃఖౌఘ). At the caesura the poet has a **dual license** (ఉభయస్వర యతి):
  - **Option A వృద్ధియతి** [6.8.1–6.8.2]: match the substituted ఐ/ఔ as `A`-class (అ↔భోగైక, ఆ↔హేమైక, ఐ↔భాగైక, అ↔బలౌఘ, ఆ↔బాణౌఘ, ఔ↔ఐ).
  - **Option B స్వరప్రధాన** [6.8.3]: match the underlying పరపదాది vowel — ఏ as `I` (ఈ↔మదీయైకత్వ, ఎ↔లోకైక, ఏ↔చిత్తైక) or ఓ as `U` (ఉ↔బిడౌజ, ఓ↔పవనౌషధి).
  - Both may co-exist in one verse (Channabasava Purāṇamu 1-150). In all *other* vowel sandhis only the పరపదాది vowel counts (`YATI-SV-02`).
  status: canonical (kind: vidhāna).

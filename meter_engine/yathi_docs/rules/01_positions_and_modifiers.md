# 01 — Positions, mechanics, modifiers [6.0 – 6.1.9]

Source: `../yathi.md` part 1 (§6.0 – §6.1.9). Overlaps `../yathi1.md` Y1–Y5, Y8, Y9.

## A. What a yati is

- **YATI-POS-01** `=Y1.1` [6.0] **వళి** = the first akshara of every pāda (line). status: canonical.
- **YATI-POS-02** `=Y1.2` [6.0] **యతిస్థానము** = the akshara (vritta) or gaṇa-start (jāti/upajāti) coordinate that the meter's lakṣaṇa fixes inside the pāda. status: canonical.
- **YATI-POS-03** `=Y1.3` [6.0] **యతిమైత్రి**: the akshara at the యతిస్థానము must be *identical to* or a *friend of* the వళి. Identity = ప్రాణియతి; friendship = membership in one of the approved equivalence classes (the 41 yatis). Formally `Class(akshara_1) ≡ Class(akshara_yati)`. status: canonical.
- **YATI-POS-04** `=Y2.1` [6.1.6] The *maitri* rules (which sounds pair) are meter-independent; only the *position* depends on the meter. status: canonical.
- **YATI-POS-05** `=Y1.4, Y3.4` [6.1.7 (3)(ii)] **Line independence**: each pāda resolves its own yati; pāda k's వళి is compared only with pāda k's yati akshara. One pāda may use a svara yati, the next a vyañjana yati, the next an ubhaya yati. In a సీసము + గీతి, 4×2 + 4 = 12 independent yatis. status: canonical.
- **YATI-POS-06** `=Y3.3` [6.1.3, 6.1.8] **Word boundary irrelevant**: the yati akshara may be word-initial, medial or final; the preceding aksharas carry no weight constraint (unlike prāsa). status: canonical.
- **YATI-POS-07** `=Y1.5` [6.1.2] Eleven synonyms: వళి, వడి, యతి, విరతి, విశ్రాంతి, విశ్రామము, విశ్రమము, శ్రాంతి, విరమణము, విరమము, విరామము (Appakavi uses ten, omits విరమము). "ఉత్పలమాలలో 1–10 అక్షరములకు యతి" means the 1st *and* the 10th akshara agree. status: informational.

## B. Where the yati falls, per meter [6.1.6]

- **YATI-POS-08** `=Y2.3` **Sama-vṛttas (absolute akshara index)**: ఉత్పలమాల 1↔10; చంపకమాల 1↔11; శార్దూలము 1↔13; మత్తేభము 1↔14. status: canonical.
- **YATI-POS-09** **Jāti / upajāti (gaṇa index)**: ఆటవెలది and తేటగీతి: 1st akshara ↔ 1st akshara of the 4th gaṇa ("3వ గణము మీద యతి"). status: canonical.
- **YATI-POS-10** **కందము**: pādas 1 and 3 have **no yati**; pādas 2 and 4: 1st akshara ↔ 1st akshara of the 4th gaṇa. status: canonical.
- **YATI-POS-11** **సీసము**: two independent yatis per line: half 1 = gaṇa 1 ↔ gaṇa 3; half 2 = gaṇa 5 ↔ gaṇa 7 (the second is *not* between the pāda's first akshara and gaṇa 7). The engine needs yati **pairs/groups**, not bare positions: vrittas `{1, n}`, jāti `{1, gaṇa k+1}`, సీసము `{1,3}` and `{5,7}` (gaṇa starts), sragdhara-type `{1, 8, 15}` all mutual. status: canonical.
- **YATI-POS-12** **బహుయతులు (multi-yati lines)**, all coordinates mutually rhyming: స్రగ్ధర 1-8-15; మహాస్రగ్ధర 1-9-16; మంగళమహాశ్రీ 1-9-17; తరువోజ gaṇas 1-3-5-7; also మానిని, కవిరాజవిరాజితము, సరసిజము, క్రౌంచపదము, విజయభద్ర రగడ, విజయమంగళ రగడ. Governed by బహుయతి నియతి `YATI-SY-11`. status: canonical.
- **YATI-POS-13** **దండకము** is the sole classical meter with neither yati nor prāsa. status: canonical.
- **YATI-POS-14** `=Y9.3` [6.1.8] In Sanskrit-origin vrittas the Telugu position = the first akshara *after* the Sanskrit word-break (శార్దూలము: Sanskrit breaks 12 + 7 → Telugu 13); Telugu has no పాదాంత yati; a word may run across the pāda boundary. status: informational.

## C. Yati vs prāsa vs Sanskrit yati [6.1.7 – 6.1.8]

- **YATI-POS-15** `=Y8` [6.1.7] Prāsa: strictly the 2nd akshara, consonants only (vowels ignored), tied across all four pādas by pāda 1, governed by the ప్రాసపూర్వాక్షర weight rule. Yati: 1st akshara paired with an internal coordinate, **consonant AND vowel** must align, line-independent, no preceding-weight constraint. status: informational.
- **YATI-POS-16** `=Y9.1, Y9.2` [6.1.8] Sanskrit yati = a word break (పదచ్ఛేదము, "యతిర్విచ్ఛేద సంజ్ఞికా") at the coordinate, no sound agreement; Telugu yati = sound agreement with the వళి, no word break required. They share nothing but the name. status: informational.

## D. Signs at the yati junction [6.1.9]

- **YATI-MOD-01** `=Y4.1` **అర్ధబిందువు ఁ**: zero effect on yati, before or after the akshara (ఁక–గ = క–గ). (It matters for prāsa, not yati.) status: canonical.
- **YATI-MOD-02** `=Y4.3` **పూర్ణబిందువు ం on / after** the yati akshara or the వళి: no effect (అం–ఆ = అ–ఆ; కం–గ = క–గ). status: canonical.
- **YATI-MOD-03** `=Y4.2` **పూర్ణబిందువు ం before** the yati akshara (on the preceding akshara): never *breaks* a maitri (ంక–గ = క–గ) and *creates* extra maitri that would otherwise be illegal: త–న is no yati but ంత–న is → బిందుయతి `YATI-VY-03`, అనునాసికాక్షర `YATI-VY-05`, అనుస్వారసంబంధ `YATI-VY-06`, మవర్ణ `YATI-SP-03`. status: canonical.
- **YATI-MOD-04** `=Y4.4` **విసర్గ ః**: transparent (అంతఃపురము, దుఃఖము: ఃఖ scans as ఖ). status: canonical.
- **YATI-MOD-05** `=Y4.5` **ద్రుతము న్ after** the yati akshara (line-end or caesura nasal): no effect. status: canonical.
- **YATI-MOD-06** `=Y4.6` **ద్రుతము న్ (or ల్) before** the వళి (end of previous pāda) or before the yati akshara: alters the cluster → extra options under సంయుక్తయతి: నకార సంశ్లేషము `YATI-SY-08`, లకార సంశ్లేషము `YATI-SY-09`. status: canonical.
- **YATI-MOD-07** [6.44] **ప్లుతము** (3-mātrā emotional lengthening) scans as **guru**; for yati it opens the కాకుస్వర dual track `YATI-UB-07`. status: canonical.

## E. Appakavi's inventory [6.1.3 – 6.1.5]

- **YATI-POS-17** `=Y5.1, Y5.2` **41 yatis** = 7 స్వరయతులు + 21 వ్యంజనయతులు + 12 ఉభయయతులు (13 when commentators restore భిన్నయతి) + 1 ప్రాసయతి. Some are marked అగ్రాహ్య by Appakavi himself; అఖండయతి is apraśasta (`YATI-RJ-01`). status: informational.
- **YATI-POS-18** The 7 svara yatis: స్వరమైత్రి (6.2.1), స్వరప్రధాన (6.3), లుప్తవిసర్గకస్వర (6.4), ఋ (6.5), ఋత్వసంబంధ (6.6), ఋత్వసామ్య (6.7), వృద్ధి (6.8) → file 02. status: informational.
- **YATI-POS-19** The 21 vyañjana yatis (Appakavi's order): ప్రాణి, వర్గజ, బిందు, తద్భవవ్యాజ, విశేష, అనుస్వారసంబంధ, అనునాసికాక్షర, మువిభక్తి, ముకార, మవర్ణ, ఋజు, ప్రత్యేక, భిన్న, ఏకతర, అభేద, అభేదవర్గ, ఊష్మ, సరస, సంయుక్త, అంత్యోష్మసంధి, వికల్ప → files 03, 04, 05. status: informational.
- **YATI-POS-20** The 13 ubhaya yatis: భిన్న, నిత్య, విభాగ, కాకుస్వర, ప్లుతయుగ, పంచమీవిభక్తి (rejected), యుష్మదస్మచ్ఛబ్ద, నిత్యసమాస, దేశ్యనిత్యసమాస, నామాఖండ, రాగమసంధి, పరరూప, ప్రాది → file 06. status: informational.
- **YATI-POS-21** `=Y5.3` [6.1.5, 6.79] Commentators' meta-division: **యతిభేదములు** (which sounds pair) vs **యతివిధానములు** (how/where in the word the test is applied). Full listing in `YATI-EP-10`. status: informational.

# 03 — Vyañjana (consonant) yatis [6.9 – 6.25]

Source: `../yathi.md` parts 3–6. The 21 consonant yatis are enumerated in `YATI-POS-19`; the ones that are really *conjunct* or *sandhi* procedures (సంయుక్త, అంత్యోష్మసంధి, వికల్ప, ప్రత్యేక, భిన్న, ఏకతర, తద్భవవ్యాజ, విశేష, మవర్ణ) are in files 04, 05, 06.

Every rule below presupposes `YATI-SV-01.1`: the vowels riding on the two consonants must be in the same class.

## A. ప్రాణి యతి [6.10 – 6.10.4]

- **YATI-VY-01** [6.10] **Identity**: same consonant (ప్రాణి = consonant + vowel) with vowels in the same class. For each consonant three disjoint realms: {క కా కై కౌ} | {కి కీ కృ కౄ కె కే} | {కు కూ కొ కో}. Cross-class (క≠కి, కి≠కు, క≠కు) invalid. Pure identity (క–క, చె–చె) is the default. Attested for every consonant incl. ఖ ఘ ఛ ఠ ఢ ణ థ ఫ ళ ఱ (6.10.2–6.10.3). status: canonical (kind: bhēda).
- **YATI-VY-01.1** [6.10.4] Test for sandhi first (`YATI-SV-02.9`): an apparent identity may really be a svara-pradhāna vowel match. status: mandatory.

## B. వర్గజ యతి [6.11 – 6.11.2]

- **YATI-VY-02** [6.11] The **first four stops of each varga** pair mutually (6 pairs each): క-వర్గ {క ఖ గ ఘ}, ట-వర్గ {ట ఠ డ ఢ}, త-వర్గ {త థ ద ధ}, ప-వర్గ {ప ఫ బ భ}. status: canonical (kind: bhēda).
- **YATI-VY-02.1** **చ-వర్గ expanded** with the dental affricates (Bāla Vyākaraṇam Saṁjñā 7 "దంత్య తాలవ్యంబులయిన చజలు సవర్ణంబులు"): {చ ౘ ఛ జ ౙ ఝ} → 15 pairs. Total 6+15+6+6+6 = **39 vargaja pairs**. status: canonical.
- **YATI-VY-02.2** The 5th consonant (nasal ఙ ఞ ణ న మ) is **excluded**: క≠ఙ, త≠న, ప≠మ without a bindu (→ `YATI-VY-03`, `YATI-RJ-04`). status: mandatory.
- **YATI-VY-02.3** Vowel classes must align: క↔గ, ఖా, ఘౌ yes; క↔గి, ఘు no. status: mandatory.
- **YATI-VY-02.4** [6.11.1] Sandhi-derived consonants (గసడదవాదేశ: కన్నుల→గన్నుల after a drutam) are evaluated on the **surface** consonant (క↔గ vargaja). status: canonical.

## C. బిందు యతి [6.12 – 6.12.6]

- **YATI-VY-03** [6.12] **ం + stop(1–4) ↔ the class nasal**: {ంక ంఖ ంగ ంఘ}↔ఙ; {ంచ ంఛ ంజ ంఝ}↔ఞ; {ంట ంఠ ండ ంఢ}↔ణ; {ంత ంథ ంద ంధ}↔న; {ంప ంఫ ంబ ంభ}↔మ. Basis: Telugu ంత is phonologically న్+త (Sanskrit శాన్త, స్తమ్భ); applies to native roots too (కుండ↔ణ). status: canonical (kind: bhēda).
- **YATI-VY-03.1** [6.12.1] The pre-stop bindu **adds**, never cancels: ంప may still take ప (prāṇi), బ/భ (vargaja), or మ (bindu). status: canonical.
- **YATI-VY-03.2** [6.12.5 (1)] **Line-break bridging**: line 1 ends in …ఘం, line 2 opens with టా → evaluated as ంటా↔ణ. status: canonical.
- **YATI-VY-03.3** [6.12.5 (2)] **Druta-derived compounds**: an inflected న్ before a పరుష across a line break mutates to anusvāra + voiced stop (కోటులన్+పావను → కోటులంబావను) → ంబా↔మా is a valid bindu yati. status: canonical.
- **YATI-VY-03.4** [6.12.5 (3)] **Dental duality**: drutam + త/ద may scan as a conjunct (వాడుటన్దేట → సంయుక్త, నే↔నీ) *or* as పూర్ణబిందు (వాడుటందేట → bindu, ందే↔నీ); both valid because the త-వర్గ nasal is న. status: canonical.

## D. న–ణ / సరసయతి-1 [6.13 – 6.13.3]

- **YATI-VY-04** [6.13] **న ↔ ణ** (dental ↔ retroflex nasal) with aligned vowels (న నా↔ణ ణా; ని నీ నె నే↔ణి ణీ ణె ణే; ను నూ నొ నో↔ణు …). Radical (సహజ) and sandhi-derived (ఆదేశ) ణ both qualify. status: canonical (kind: bhēda).

## E. అనునాసికాక్షర యతి [6.14 – 6.14.3]

- **YATI-VY-05** [6.14] **ం + ట-వర్గ stop ↔ న** and **ం + త-వర్గ stop ↔ ణ** ({ంట ంఠ ండ ంఢ}↔న; {ంత ంథ ంద ంధ}↔ణ). Derived by composing బిందు (`YATI-VY-03`) with న–ణ (`YATI-VY-04`) — the *only* sanctioned composition. status: canonical (kind: bhēda).
- **YATI-VY-05.1** Strictly between ట and త vargas; nasalised క/చ/ప stops cannot cross to a foreign nasal (ఙ ఞ మ share no cross-affinity). status: mandatory.

## F. అనుస్వారసంబంధ యతి [6.15 – 6.15.3]

- **YATI-VY-06** [6.15] **{ంట ంఠ ండ ంఢ} ↔ {ంత ంథ ంద ంధ}** — 16 cluster pairs across all three vowel classes (ంద↔ంట, ండ↔ంతా, ండి↔ంధి). status: canonical (kind: bhēda).
- **YATI-VY-06.1** [6.15.3] Only ట/త classes; bindu-preceded క/చ/ప stops excluded. status: mandatory.

## G. No unauthorised transitivity [6.15.4]

- **YATI-VY-07** [6.15.4] The engine must **not** chain bridges: ఇ↔ఋ and ఋ↔రి do **not** yield ఇ↔రి. A cross-class bridge is valid only when explicitly sanctioned by the treatises and attested in mahākavi usage. → `YATI-RJ-02`. status: mandatory.

## H. ఋజు యతి [6.16 – 6.16.1]

- **YATI-VY-08** [6.16] **య ↔ హ** with aligned vowels (య యా యై యౌ↔హ హా హై హౌ; యి యీ యె యే↔హి హీ హృ హె హే; యు యూ యొ యో↔హు హూ హొ హో). status: canonical (kind: bhēda).

## I. సరసయతి-2: అ–య [6.17 – 6.17.3]

- **YATI-VY-09** [6.17] **Independent vowel ↔ య+same-class vowel**: {అ ఆ ఐ ఔ}↔{య యా యై యౌ}; {ఇ ఈ ఋ ఎ ఏ}↔{యి యీ యె యే}; {ఉ ఊ ఒ ఓ}↔{యు యూ యొ యో}. Either side may itself be sandhi-resolved (ఫలంబు+ఎట్లు → ఎ↔యి). status: canonical (kind: bhēda).
- **YATI-VY-09.1** [6.17.1] Only **శబ్దసిద్ధ (root) య** (యజ్ఞము, మాయ, సముదయ) executes sarasa yati. An **ఆగమ య** (యడాగమము: విని+అల్గి → వినియల్గి) is phonologically empty: bypass it and apply స్వరప్రధాన to the underlying vowel (అ↔అ), never అ–య. status: mandatory.

## J. సరసయతి-3: అ–హ [6.18 – 6.18.2]

- **YATI-VY-10** [6.18] **Independent vowel ↔ హ+same-class vowel**: {అ ఆ ఐ ఔ}↔{హ హా హై హౌ}; {ఇ ఈ ఋ ఎ ఏ}↔{హి హీ హృ హె హే}; {ఉ ఊ ఒ ఓ}↔{హు హూ హొ హో}. Vowel side may be sandhi-resolved (చర+ఆచర → ఆ↔హ; భువన+ఏక → ఐ via వృద్ధి ↔ హ). status: canonical (kind: bhēda).
- **YATI-VY-10.1** [6.18.2] **Closed triad** {అ, య, హ}: య↔హ (ṛju), అ↔య, అ↔హ form one bidirectional matrix, always subject to vowel classes. status: canonical.

## K. ఊష్మ యతి [6.19 – 6.19.2]

- **YATI-VY-11** [6.19] **శ ↔ ష ↔ స** mutual (3 pairs), vowels aligned (శి శీ శృ శె శే ↔ షి … ↔ సి సీ సృ సె సే). హ is excluded (handled by ṛju/sarasa). status: canonical (kind: bhēda).

## L. సరసయతి-4: sibilants ↔ palatals [6.20 – 6.20.2]

- **YATI-VY-12** [6.20] **{శ ష స} ↔ {చ ౘ ఛ జ ౙ ఝ}** — 18 pairs (శ↔చ, శా↔జ, శ↔ఝ, చ↔షా, ఛ↔ష, జ↔ష, స↔చా, ఛ↔స, జ↔స, ఝ↔స …). status: canonical (kind: bhēda).
- **YATI-VY-12.1** [6.20.1] Dental ౘ ౙ combine only with {అ ఆ ఉ ఊ ఒ ఓ ఐ ఔ}, never with {ఇ ఈ ఎ ఏ ఋ}; matches involving them are restricted accordingly. status: mandatory.

## M. అభేద యతి: వ–బ [6.21 – 6.21.3]

- **YATI-VY-13** [6.21] **వ ↔ బ** (వబయోరభేదః; doublets విభీషికా/బిభీషికా, వలాహక/బలాహక, ఆవిడ/ఆబిడ), vowels aligned (వ–బ, వి–బి, వు–బు). status: canonical (kind: bhēda).
- **YATI-VY-13.1** [6.21.1–6.21.3] Applies to **both** శబ్దసిద్ధ (అలఘు) వ (వరుణ, నీవు) and **ఆదేశ (లఘు) వ** from గసడదవాదేశ of ప (అతఁడు వలికె, నిదురవోయి). Appakavi's restriction to radical వ is overturned by Nannaya's own usage (వడయుదురు↔బ, పేదవడిన↔బా). status: canonical (the ādēśa half is Appakavi-disputed but corpus-proven).

## N. అభేదవర్గ యతి: వ–ప/ఫ/భ [6.22 – 6.22.6]

- **YATI-VY-14** [6.22] **వ ↔ {ప ఫ భ}** (వ≡బ, and బ pairs with its varga), vowels aligned (వ వా వై వౌ↔ప/ఫ/భ …; వి వీ వృ వె వే↔పి …; వు వూ వొ వో↔పు …). status: canonical (kind: bhēda).
- **YATI-VY-14.1** [6.22.2, 6.22.6] Both inherent and ఆదేశ వ qualify (వడుదునె↔ప, పృ↔వెట్టి, పూ↔వోసి, భూ↔వొలియంగ). Copyists' "corrected" readings (నెవంబున, వావులు, వివేకము) that force వ–వ are rejected; the originals (నెపంబున, బావులు, విభేదము) stand. status: canonical.

## O. అభేద యతి-2: ల–ళ [6.23 – 6.23.4]

- **YATI-VY-15** [6.23] **ల ↔ ళ**, vowels aligned, across (1) tatsama doublets (వేలా/వేళా, కలా/కళా), (2) native roots with ళ (తళుకు, కేళాకూళి, చోళ), (3) plural ఆదేశ ళ (త్రాడులు→త్రాళులు, కాళ్లు→కాళులు; Bāla Vyākaraṇam Prakīrṇaka 24). status: canonical (kind: bhēda).

## P. ము విభక్తి యతి / పోలిక వడి [6.24 – 6.24.5]

- **YATI-VY-16** [6.24] The nominal **ము** — nominative suffix (ము-వర్ణకము: వృక్షము, బియ్యము, నెపము; incl. conjoined భయమున్) **or** inflected augment (ముగాగమము: వృక్షములు, దైవమునకు; Bāla Vyākaraṇam Tatsama 39–41 "మువర్ణకంబునకు విధించు కార్యము ముగాగమంబునకునగు") — pairs with **{పు ఫు బు భు} and their `U`-class forms** (పు పూ పొ పో, ఫు …, బు …, భు …) = 16 pairings, **without** any anusvāra (exception to `YATI-VY-02.2`). status: canonical (kind: bhēda).

## Q. ము కార యతి [6.25; examples 6.27.16]

- **YATI-VY-17** [6.25] A **radical / stem ము మూ మొ మో** (not the suffix) ↔ {పు ఫు బు భు} `U`-class forms (మ్ము↔పు, స్ఫూ↔మూ, భూ↔మ్రొ, ల్పు↔మొ, భు↔న్మూ, భూ↔మ్రో). Note: the body of §6.25 is not present in `../yathi.md`; the rule is reconstructed from the 21-list entry "'ము'కారయతి — radical/stem mu", the 6.27.16 examples and the ము–వు derivation (`YATI-DL-06`) which cites it. status: canonical (flag: source section missing from the extraction).

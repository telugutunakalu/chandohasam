# 07 — Prāsa yati [6.52 – 6.53]

Source: `../yathi.md` parts 17–18. Overlaps `../yathi1.md` Y2.4. The consonant-pair semantics of the individual prāsa classes are already programmed in `../../prasa_rules.yaml`; this file lists what prāsa **yati** adds on top.

## A. Mechanism

- **YATI-PY-01** `=Y2.4` [6.53] **ప్రాసయతి** substitutes the head-yati check: when position 1 ↔ yati-sthāna fails, the line is still valid if **position 2 (Prāsa 1)** and **the akshara immediately after the yati-sthāna (Prāsa 2)** rhyme by the prāsa rules. status: canonical (kind: vidhāna).
- **YATI-PY-02** **Permitted metres only**: upajātis సీసము, తేటగీతి, ఆటవెలది; vrittas సరసిజము, క్రౌంచపదము; mālikā vrittas లయగ్రాహి, లయవిభాతి, లయహారి, త్రిభంగి (the ఉద్ధురమాలా group). **Prohibited** in the major Sanskrit vrittas (ఉత్పలమాల, చంపకమాల, శార్దూలము, మత్తేభము) and in కందము. status: mandatory.
- **YATI-PY-03** **ప్రాసపూర్వాక్షర నియమము**: the akshara before Prāsa 1 (= position 1) and the akshara before Prāsa 2 (= the yati-sthāna akshara) must have **identical weight** (both laghu or both guru); laghu-preceded vs guru-preceded prāsa is a fatal failure. status: mandatory.
- **YATI-PY-04** Consonant-only match (vowels on Prāsa 1/2 irrelevant: లు–ల, ద–దు, ని–నో); Prāsa 1 and Prāsa 2 themselves need not share weight. status: canonical.
- **YATI-PY-05** **Autonomy**: each line / hemistich decides independently; a stanza may mix head yati and prāsa yati, and adjacent prāsa yatis may use different consonants (సీసము has 8 yati nodes). status: canonical.
- **YATI-PY-06** Dental/palatal చ ౘ, జ ౙ are sama-prāsa equivalents (Bāla Vyākaraṇam Saṁjñā 7). status: canonical.

## B. Prāsa classes admissible in prāsa yati [6.53 tables]

Each entry: class — condition — preceding-akshara weight — status.

- **YATI-PY-07** సమప్రాసము — identical consonants (ఢ-ఢ … హ-హ) — uniformly guru or laghu — canonical.
- **YATI-PY-08** ఋత్వసహిత ప్రాసము — C+ఋ with C+any vowel (క-కృ, గి-గృ, న-నృ) — parity — canonical (treated as sama).
- **YATI-PY-09** పూర్ణబిందు ప్రాసము — both consonants preceded by ం (ంక-ంక, ండ-ండు, ంబ-ంబ) — guru — canonical; single-sided bindu fails.
- **YATI-PY-10** సంయుక్తాక్షర / ద్విత్వ ప్రాసము — identical clusters or geminates in identical order (క్క, ల్ల, క్ష, ర్ణ, స్త …) — guru — canonical; ృ inside the cluster (ర్ఘ vs ర్ఘృ) stays valid.
- **YATI-PY-11** అర్ధబిందు ప్రాసము — both preceded by ఁ (ఁకు-ఁక, ఁడు-ఁడె) — parity — canonical (native lexemes).
- **YATI-PY-12** ఖండాఖండ ప్రాసము — ఁC with plain C (ఁక-క, గ-ఁగు) — parity — canonical.
- **YATI-PY-13** లఘు యకార ప్రాసము — యడాగమ య with root య — parity — canonical.
- **YATI-PY-14** స్వవర్గజ ప్రాసము — ధ-థ (శోధించి-ద్వీథులందు) — parity — accepted_relaxation.
- **YATI-PY-15** న-ణ ఉభయ ప్రాసము — న with ణ (ādēśa or radical) — parity — canonical (Nannaya Āraṇya 1-49; scribal regularisations rejected).
- **YATI-PY-16** స-శ ఉభయ ప్రాసము — స with శ — parity — canonical.
- **YATI-PY-17** ల-ళ అభేద ప్రాసము — tatsama, native and geminate (తల్లి-ద్రెళ్ళి) — parity — canonical.
- **YATI-PY-18** ఋ ప్రాసము — word-initial ఋ with ర — parity — canonical.
- **YATI-PY-19** లఘుద్విత్వ / సమలఘు ప్రాసము — native light conjuncts ద్రు/ద్రి (విద్రు-లద్రు) — both laghu — canonical_subtype.
- **YATI-PY-20** వికల్ప ప్రాసము — anunāsika-sandhi doublets ఙ్న-గ్ని, ఙ్మ-గ్మ (ప్రాఙ్నగ/ప్రాగ్నగ) — guru — canonical (Appakavi 3-328).
- **YATI-PY-21** ప్రాసమైత్రి ప్రాసము — ంబ(ు) with మ్మ(ు) — guru — canonical (Appakavi 3-343).
- **YATI-PY-22** ర-ఱ ప్రాసము — ర with ఱ (దరు-మఱ, చోర-జూఱ) — parity — orthographic_relaxation (Appakavi: prāsa-vairamu; Tikkana, Errana, Kṛṣṇadēvarāya, Molla use it; project decision as `YATI-SP-08`).
- **YATI-PY-23** సంధిగత ప్రాసము — evaluate the post-sandhi surface consonant (ంగ-ంగ after drutam, trika geminates మ్మ-మ్మ, క్క-క్క, య్య-య్య, గ్గ-గ్గ) — post-sandhi weight — canonical.
- **YATI-PY-24** అధిక ప్రాసము — geminate+C cluster with plain cluster of the same consonants (జ్జ్వ-జ్వా, త్త్ర-త్ర, త్త్వ-త్వ, శ్శ్రీ-శ్రీ) — guru — canonical.

## C. Precedence and rejections

- **YATI-PY-25** **Precedence**: if a line satisfies both head yati and prāsa yati, log **head yati** (భూషణంబిట్టివే … భూ↔భూ is ప్రాణి, not prāsa yati ష–ష). Exception: an **అవకలిప్రాస సీసము** (all lines required to carry prāsa yati) is classified as prāsa yati. status: canonical (procedure `YATI-EP-07`).
- **YATI-PY-26** **Not admissible in prāsa yati**: ద-ధ, డ-ఢ, ల-డ, ళ-డ, స-ష (uncanonical or disputed here even where the same pairs are yati bhēdas). Instances of డ-ఢ (లేడు-రూఢికి) are corruptions for రూడి. status: forbidden.
- **YATI-PY-27** **సంయుక్తాసంయుత ప్రాస నిషేధము**: plain C vs రేఫ conjunct (డ-ండ్ర, భ-ంభ్ర, మ-మ్ర) or vs లకార conjunct (ండు-ండ్లు) — rejected as aprayōga-yōgya. status: deprecated.
- **YATI-PY-28** **పూర్ణార్ధబిందు ప్రాస నిషేధము**: ఁC with ంC (పాఁడి-తండ్రి, వేఁడు-బండ్లు) — Appakavi wrote an example but never defined the class; rejected. status: deprecated.

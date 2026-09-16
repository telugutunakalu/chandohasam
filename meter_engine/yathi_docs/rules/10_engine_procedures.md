# 10 — Engine procedures, precedence, taxonomy

Source: engine-oriented passages of `../yathi.md` (6.1.5, 6.28(11), 6.47 decision tree, 6.53 precedence, 6.79) and the "Notes for the yati engine" of `../yathi1.md` §10 and `../yathi2.md` §6. These are *procedures*, not new pairings.

## A. Inputs and normalisation

- **YATI-EP-01** **Inputs**: syllables with `onset` (tuple of consonants), `vowel`, `anusvara`, `visarga`, `candrabindu`, `dead` (pollu), `word`, plus per-meter **yati groups** (`YATI-POS-08..12`): vrittas `{1,n}`, jāti `{1, gaṇa k+1}`, సీసము `{1,3},{5,7}`, bahu-yati `{1,8,15}` etc., కందము pādas 1/3 = none. status: informational.
- **YATI-EP-02** **Normalise** (`YATI-MOD-*`): drop ఁ everywhere; drop ం/ః *on* the యతి akshara and the వళి; drop a trailing న్/ల్ on the yati akshara; keep a *preceding* ం and a *preceding* న్/ల్ as flags (they add pairs: బిందు, అనునాసిక, అనుస్వారసంబంధ, మవర్ణ, సంశ్లేషము). Apply రేఫయుత normalisation (`YATI-RJ-28`): ృ in a native root is ర్+ఉ. status: mandatory.
- **YATI-EP-03** **Candidate readings (lattice)** for each coordinate (వళి and yati akshara), in line with the DAWG's vikalpa handling:
  1. the akshara as written: `(C_i, V)` for **every** constituent consonant `C_i` of the onset (`YATI-SY-01`, including a fused preceding న్/ల్ from the line break or the previous word: `YATI-SY-08/09`);
  2. svara-pradhāna readings: the vowel(s) the written vowel could result from under the sandhis of `YATI-SV-02.2` (ా → అ/ఆ; ే → ఇ/ఈ or ఎ/ఏ; ో → ఉ/ఊ or ఒ/ఓ; ై → ఐ or ఏ/ఐ via వృద్ధి; ౌ → ఔ or ఓ/ఔ; a bare న/నా/ని/ను after a drutam → the vowel; య+V → V; C-ఓ / C-ఏ → hidden అ by గూఢస్వర/పూర్వరూప);
  3. ubhaya readings where a morphological trigger is recognised (`YATI-UB-*`): both the junction vowel and the surface consonant(s);
  4. vowel-detachment readings only for ఋ/ృ (`YATI-SV-05/06/07`).
  Accept the yati if **any** admissible pair of readings satisfies a bhēda rule; **report which reading and which rule** (provenance trail). A lexicon / sandhi splitter can later narrow the lattice. status: canonical.
- **YATI-EP-03.1** **Blocked readings** must be removed from the lattice when the trigger is recognised: elided అది/అవి (`YATI-SP-06`), క్యచ్ (`YATI-UB-14`), augments (`YATI-DL-10/11`), clitics (`YATI-DL-08`), verbal -ఎడు (`YATI-DL-12`), -మయ/-మాత్ర Option B (`YATI-SP-05.1`), ఓ before a voiced consonant (`YATI-SV-04.3`), హలాది prādi (`YATI-UB-10.1`). status: mandatory.

## B. Comparison

- **YATI-EP-04** **Compare as (consonant class, vowel class)** (`YATI-SV-01.1`): the vowel classes are fixed (`YATI-SV-01`); the consonant classes are the union of the bhēda rules in files 03, 05, 08 (ప్రాణి, వర్గజ incl. ౘ/ౙ, బిందు, న–ణ, అనునాసిక, అనుస్వారసంబంధ, ఋజు, సరస-2/3/4, ఊష్మ, అభేద, అభేదవర్గ, ల–ళ, ము-vibhakti/ము-kāra, జ్ఞ→న/ణ/క…, మవర్ణ, ఏకతర, ల–డ, ద–డ, ము–వు, ర–ల/ళ, ఌ), gated by profile. status: canonical.
- **YATI-EP-05** **Druta-saṁślēṣa order** [6.28(11)]: (1) native match? pass; (2) previous line ends in న్? synthesise న్+వళి, extract న+V₁, test; (3) న్ before the yati akshara? synthesise, extract న+V_y, test; (4) both? test న+V₁ ↔ న+V_y; else fail. Same ladder for ల్ (`YATI-SY-09`). status: canonical.
- **YATI-EP-06** **Prādi decision tree** [6.47]: prefixed by an upasarga? no → standard engine; yes → stem vowel-initial with sandhi? no (హలాది) → standard only; yes → is the alignment on the fused syllable? no (prefix head) → standard only; yes → open both tracks (`YATI-UB-10`). Nested prefixes → one node per prefix (`YATI-UB-10.5`). status: canonical.
- **YATI-EP-07** **Bahu-yati check** (`YATI-SY-11`): after resolving the first caesura of a multi-yati line with constituent `C_k` of a conjunct వళి, force `C_k` for the remaining caesuras (except in సీసము halves). status: mandatory.
- **YATI-EP-08** **Prāsa-yati fallback and precedence** (`YATI-PY-01/02/25`): only in the permitted metres, only after head yati fails, with the pūrvākṣara weight invariant; when both pass, report head yati (except అవకలిప్రాస సీసము). status: canonical.

## C. Profiles / modes

- **YATI-EP-09** **Profiles** as in `../../prasa_rules.yaml`: `strict` accepts canonical, canonical_subtype, mandatory; `relaxed` adds accepted_relaxation and orthographic_relaxation (ర–ఱ `YATI-SP-08`, ర–ల `YATI-DL-02`, generalised ద–డ `YATI-DL-05`, స్నా–త `YATI-DL-09`, విశ్వామిత్ర vowel `YATI-UB-11.4`, స్వవర్గజ prāsa `YATI-PY-14`); `historical` additionally *identifies* deprecated forms (బహుయతి lapses, prāsa-yati variants, akhaṇḍa attestations) without accepting them. Forbidden rules never match in any profile and are reported by name. status: canonical.

## D. Consistency checks the corpus run can enforce

- **YATI-EP-10** (a) no cross-class vowel pair ever matches (`YATI-SV-01.2`); (b) no prāsa yati in vrittas/కందము (`YATI-PY-02`); (c) కందము pādas 1, 3 carry no yati (`YATI-POS-10`); (d) సీసము yatis are {1,3},{5,7} (`YATI-POS-11`); (e) every accepted match cites exactly one bhēda rule and zero or more vidhāna rules; (f) a bare vowel letter inside a line is ఋ or an unsandhied word start, not an error (`YATI-SV-03`). status: informational.

## E. Taxonomy [6.79] — bhēda vs vidhāna

- **YATI-EP-11** **యతిభేదములు** (which characters may match): స్వరమైత్రి 6.2.1; ఋ 6.5; ప్రాణి 6.10; వర్గజ 6.11; బిందు 6.12; న–ణ 6.13; అనునాసిక 6.14; అనుస్వారసంబంధ 6.15; ఋజు 6.16; సరస 6.17, 6.18, 6.20; ఊష్మ 6.19; అభేద/అభేదవర్గ 6.21–6.23; ము-vibhakti/ము-kāra 6.24–6.25; తద్భవవ్యాజ 6.31; విశేష 6.32; మవర్ణ 6.33; ఏకతర/ద్విరేఫ 6.37–6.38; ఌ 6.54; ర–ల/ర–ళ 6.55; ల–డ/ళ–డ 6.58; ద–డ 6.59; ము–వు 6.63.
- **YATI-EP-12** **యతివిధానములు** (how/where the test is applied): స్వరప్రధాన 6.3; లుప్తవిసర్గక 6.4; ఋత్వసంబంధ/ఋత్వసామ్య 6.6–6.7; వృద్ధి 6.8; సంయుక్త 6.26–6.29; బహుయతి నియతి 6.30; అంత్యోష్మసంధి 6.34; వికల్ప 6.35; ప్రాసయతి 6.53; నిత్యసంధి 6.57; మతుబాదేశ 6.64; ఏవార్థక 6.66; స్నాన 6.74; āgama rules 6.75; ద్విరుక్త ట 6.76; -ఎడి/-ఎడు 6.77; and all ubhaya classes: భిన్న 6.40, నిత్య 6.41, విభాగ 6.42, యుష్మదస్మద్ 6.43, కాకుస్వర 6.44, ప్లుతయుగ 6.45, పరరూప 6.46, ప్రాది 6.47, నిత్యసమాస 6.48, దేశ్య నిత్యసమాస 6.49, నామాఖండ 6.50, రాగమసంధి 6.51, చతుర్థీ 6.56.

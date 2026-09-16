# yathi rules — segregated extraction of `../yathi.md`

`../yathi.md` (all 20 parts of పద్యవిద్య ch. 6, §6.0 – §6.79) is the long,
example-heavy source. This folder splits it into ten short files, one topic
each, with **every rule as a bullet**. Examples are trimmed to one or two
attestations per rule; the full provenance stays in `../yathi.md`.

The machine-oriented one-line-per-rule version is `../yathi_compact.md`.
Every bullet here carries the same rule id as there, so the two can be
cross-checked mechanically (`grep -o 'YATI-[A-Z]*-[0-9]*'`).

| file | ids | contents | book §§ |
| :-- | :-- | :-- | :-- |
| `01_positions_and_modifiers.md` | YATI-POS-*, YATI-MOD-* | what a yati is, where it falls per meter, signs that do / do not matter, the 41-yati inventory | 6.0 – 6.1.9 |
| `02_svara_yati.md` | YATI-SV-* | vowel classes, svara-pradhāna (sandhi) rule, ఋ, gūḍha-svara, ఋ-yati, ఋత్వసంబంధ, ఋత్వసామ్య, వృద్ధి | 6.2 – 6.8 |
| `03_vyanjana_yati.md` | YATI-VY-* | the 21 consonant yatis: prāṇi, vargaja, bindu, న-ణ, anunāsika, anusvāra-sambandha, ṛju, sarasa 2/3/4, ūṣma, abhēda, abhēda-varga, ల-ళ, ము-vibhakti, ము-kāra | 6.9 – 6.25 |
| `04_samyukta_yati.md` | YATI-SY-* | conjunct decomposition, క్ష, dual conjuncts, 3-consonant clusters, న్ and ల్ saṁślēṣa across line breaks, bahu-yati niyati | 6.26 – 6.30 |
| `05_special_vyanjana.md` | YATI-SP-* | తద్భవవ్యాజ, విశేష, మవర్ణ, అంత్యోష్మసంధి, వికల్ప, ప్రత్యేక, ఏకతర, ద్విరేఫ | 6.31 – 6.38 |
| `06_ubhaya_yati.md` | YATI-UB-* | the dual-track (vowel-or-consonant) yatis: భిన్న, నిత్య, విభాగ, -ఎఁడు, -అవ, యుష్మదస్మదాది, కాకుస్వర, ప్లుతయుగ, పరరూప, ప్రాది (prefix table), నిత్యసమాస (compound tables, నఞ్, క్యచ్, ఉపసర్గసంధి), దేశ్య నిత్యసమాస, నామాఖండ, రాగమసంధి, చతుర్థీ | 6.39 – 6.51, 6.56 |
| `07_prasa_yati.md` | YATI-PY-* | prāsa-yati mechanism, permitted metres, weight invariant, the full prāsa typology, precedence, rejected prāsa variants | 6.52 – 6.53 |
| `08_derived_and_late.md` | YATI-DL-* | ఌ, ర-ల / ర-ళ, నిత్యసంధి (torli, ścutva, chatva, ṣṭutva), ల-డ / ళ-డ, ద-డ, ము-వు, మతుబాదేశ, ఏవార్థక, స్నాన, āgama invariants, ద్విరుక్త ట, -ఎడి/-ఎడు | 6.54 – 6.59, 6.63 – 6.66, 6.74 – 6.77 |
| `09_rejected_yati.md` | YATI-RJ-* | every yati the book rejects or restricts, plus the pseudo-classes it dissolves (రేఫయుత, సౌభాగ్య, యా-యతి, ఎక్కటి) | scattered; 6.15.4, 6.36, 6.38, 6.47, 6.49, 6.52, 6.55, 6.58 – 6.62, 6.67 – 6.73, 6.75 – 6.78 |
| `10_engine_procedures.md` | YATI-EP-* | normalisation, comparison, lattice readings, the saṁślēṣa and prādi decision procedures, precedence, mode flags, consistency checks, the bhēda/vidhāna taxonomy | 6.1.5, 6.28(11), 6.47, 6.53, 6.79 |

## Conventions used in every file

- **Rule ids** are ours and follow the project's ruleset grammar (`PRASA-<FAMILY>-<NN>` in `../../prasa_rules.yaml`): `YATI-<FAMILY>-<NN>`, sub-bullets `YATI-<FAMILY>-<NN>.k`. The book's section numbers are kept in brackets `[6.12.5]`.
- `=Yn.m` after an id means the same rule is already stated in `../yathi1.md` / `../yathi2.md` under that id.
- `A <-> B` is a bidirectional yati pairing. `{a, b}` is a set. `C` is any consonant, `V` any vowel.
- **Vowel classes** (`SV-01`) are written `A = {అ ఆ ఐ ఔ}`, `I = {ఇ ఈ ఋ ౠ ఎ ఏ (ఌ)}`, `U = {ఉ ఊ ఒ ఓ}`. "Vowel classes must align" means the vowel riding on each side of a consonant pairing must be in the same class.
- `svara track` / `hal track` = matching by the (underlying) vowel / by the surface consonant (the two tracks of an ubhaya yati).
- **Status** uses the same vocabulary as the prāsa ruleset: `canonical` (every profile), `canonical_subtype` (named sub-variety, every profile), `mandatory` (constraint; violation fails every profile), `accepted_relaxation` (sanctioned by later lākṣaṇikas / kāvya usage; profile ≥ relaxed), `orthographic_relaxation` (ర/ఱ; accepted from relaxed on by project decision), `deprecated` (attested but apraśasta; historical profile only, identification not acceptance), `forbidden` (never a match; the rule names the failure), `informational` (annotation only). Profiles: strict ⊂ relaxed ⊂ historical (`YATI-EP-08`).
- Kinds follow the book's taxonomy [6.1.5, 6.79]: `bhēda` = *which* sounds pair; `vidhāna` = *how/where* in the word the test is applied; `ubhaya` = vidhāna that opens both tracks; `reject` = negative rule.

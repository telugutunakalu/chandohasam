// Chandohasam progress seminar deck. Every number and claim comes from the mid-submission paper
// (Chandohasam: Towards Semantically Coherent Telugu Metrical Poetry Generation with Text Diffusion),
// except where a slide's note says "not in the paper".
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');
const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');

const OUT_DIR = process.env.OUT_DIR;
const FIG = path.join(OUT_DIR, 'figures');
const OUT = path.join(OUT_DIR, 'chandohasam_seminar.pptx');

const THEME = {
  name: 'Chandohasam',
  headFontFace: 'Cambria',
  bodyFontFace: 'Calibri',
  colors: {
    dk1: '22192B', lt1: 'FFFFFF', dk2: '5C5366', lt2: 'F4EFF1',
    accent1: '7B2D43', accent2: 'C8962E', accent3: '2D6E73',
    accent4: 'B9607A', accent5: '8E8797', accent6: 'E9D9DF',
    hlink: '2D6E73', folHlink: '7B2D43',
  },
};
const H = THEME.colors; // hex, for the hex-only options

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = 'Samvaran Kashyap Rallabandi';
pres.title = 'Chandohasam: progress seminar';
const C = pres.SchemeColor;
const TE = 'Nirmala UI'; // Telugu runs

const W = 13.333, LM = 0.6, CW = W - 2 * LM; // left margin, content width
const TOP = 1.45; // content top

// ---------- layouts ----------
pres.defineSlideMaster({
  title: 'TITLE',
  background: { color: H.dk1 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.25, w: 11.7, h: 1.2, fontSize: 54, bold: true, color: C.background1, align: 'left', margin: 0 }, text: '' } },
    { placeholder: { options: { name: 'subtitle', type: 'body', x: 0.8, y: 3.5, w: 11.0, h: 1.1, fontSize: 22, color: C.accent6, align: 'left', margin: 0 }, text: '' } },
    { placeholder: { options: { name: 'meta', type: 'body', x: 0.8, y: 5.2, w: 11.5, h: 1.3, fontSize: 15, color: C.accent5, align: 'left', margin: 0 }, text: '' } },
  ],
});
pres.defineSlideMaster({
  title: 'CONTENT',
  background: { color: H.lt1 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: LM, y: 0.38, w: CW, h: 0.85, fontSize: 32, bold: true, color: C.text1, align: 'left', valign: 'middle', margin: 0 }, text: '' } },
    { text: { text: 'Chandohasam  ·  progress seminar  ·  IIIT Hyderabad  ·  October 2026', options: { x: LM, y: 7.02, w: 9, h: 0.3, fontSize: 10, color: C.accent5, margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.02, w: 0.45, h: 0.3, fontSize: 10, color: C.accent5, align: 'right' },
});
pres.defineSlideMaster({
  title: 'DARK',
  background: { color: H.dk1 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.4, w: 11.7, h: 1.2, fontSize: 48, bold: true, color: C.background1, align: 'left', margin: 0 }, text: '' } },
    { placeholder: { options: { name: 'subtitle', type: 'body', x: 0.8, y: 3.7, w: 11.5, h: 2.0, fontSize: 18, color: C.accent6, align: 'left', margin: 0 }, text: '' } },
  ],
});

// ---------- helpers ----------
const NOTES = []; // {n, title, note}
let slideNo = 0;
function content(title, section, note) {
  const s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: section });
  s.addText(title, { placeholder: 'title' });
  slideNo += 1;
  if (note) s.addNotes(note);
  NOTES.push({ n: slideNo, title, note: note || '' });
  return s;
}
function txt(s, text, o) {
  s.addText(text, Object.assign({ isTextBox: true, fontSize: 14, color: C.text1, margin: 0, valign: 'top' }, o));
}
// bullet list; items: string | {lead, text} | {text, options}
function bullets(s, items, o) {
  const runs = [];
  const fs_ = (o && o.fontSize) || 14;
  const gap = (o && o.gap) || 6;
  items.forEach((it, i) => {
    const last = i === items.length - 1;
    if (typeof it === 'string') {
      runs.push({ text: it, options: { bullet: true, paraSpaceAfter: gap, breakLine: !last } });
    } else if (it.lead !== undefined) {
      runs.push({ text: it.lead, options: { bullet: true, bold: true, paraSpaceAfter: gap, color: it.leadColor || C.accent1 } });
      runs.push({ text: it.text, options: { breakLine: !last } });
    } else {
      runs.push({ text: it.text, options: Object.assign({ bullet: true, paraSpaceAfter: gap, breakLine: !last }, it.options || {}) });
    }
  });
  const opts = Object.assign({ isTextBox: true, fontSize: fs_, color: C.text1, margin: 0, valign: 'top' }, o || {});
  delete opts.gap;
  s.addText(runs, opts);
}
function card(s, o) {
  // o: x,y,w,h, head, body (array for bullets) | text, fill, headColor, fontSize, numbered
  const fill = o.fill || C.background2;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: o.x, y: o.y, w: o.w, h: o.h, fill: { color: fill }, line: { color: fill, width: 0 }, rectRadius: 0.1, objectName: 'card ' + (o.head || '') });
  let top = o.y + 0.18;
  let left = o.x + 0.22;
  if (o.num !== undefined) {
    numCircle(s, o.x + 0.22, o.y + 0.2, o.num, o.numColor);
    left = o.x + 0.22;
  }
  if (o.head) {
    const hx = o.num !== undefined ? o.x + 0.8 : left;
    txt(s, o.head, { x: hx, y: top, w: o.w - (hx - o.x) - 0.2, h: o.num !== undefined ? 0.5 : 0.42, fontSize: o.headSize || 16, bold: true, color: o.headColor || C.accent1, valign: o.num !== undefined ? 'middle' : 'top' });
    top += o.num !== undefined ? 0.62 : 0.46;
  }
  if (o.body) bullets(s, o.body, { x: left, y: top, w: o.w - 0.42, h: o.y + o.h - top - 0.12, fontSize: o.fontSize || 14, color: o.color || C.text1, gap: o.gap || 5 });
  if (o.text) txt(s, o.text, { x: left, y: top, w: o.w - 0.42, h: o.y + o.h - top - 0.12, fontSize: o.fontSize || 14, color: o.color || C.text1 });
}
function numCircle(s, x, y, n, color) {
  const d = 0.46;
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: color || C.accent1 }, line: { color: color || C.accent1, width: 0 } });
  s.addText(String(n), { x, y, w: d, h: d, fontSize: 14, bold: true, color: C.background1, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
}
function stat(s, o) {
  // o: x,y,w,h,value,label,color
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: o.x, y: o.y, w: o.w, h: o.h, fill: { color: o.fill || C.background2 }, line: { color: o.fill || C.background2, width: 0 }, rectRadius: 0.1 });
  txt(s, o.value, { x: o.x + 0.15, y: o.y + 0.12, w: o.w - 0.3, h: o.h * 0.55, fontSize: o.size || 34, bold: true, color: o.color || C.accent1, fontFace: THEME.headFontFace, align: 'center', valign: 'middle' });
  txt(s, o.label, { x: o.x + 0.15, y: o.y + o.h * 0.58, w: o.w - 0.3, h: o.h * 0.4, fontSize: o.labelSize || 12, color: C.text2, align: 'center', valign: 'top' });
}
function arrow(s, x1, y1, x2, y2, color) {
  s.addShape(pres.shapes.LINE, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), flipH: x2 < x1, flipV: y2 < y1, line: { color: color || H.accent5, width: 1.5, endArrowType: 'triangle' } });
}
function caption(s, text, o) {
  txt(s, text, Object.assign({ fontSize: 11, color: C.text2, italic: true }, o));
}
function tableOpts(extra) {
  return Object.assign({ fontSize: 12, fontFace: THEME.bodyFontFace, color: H.dk1, border: { type: 'solid', pt: 0.5, color: 'D9D2D6' }, valign: 'middle', margin: [3, 6, 3, 6] }, extra || {});
}
function hdr(text, o) { return { text, options: Object.assign({ bold: true, fill: { color: H.accent1 }, color: H.lt1, align: 'center' }, o || {}) }; }
function cell(text, o) { return { text, options: Object.assign({ align: 'center' }, o || {}) }; }
function lcell(text, o) { return { text, options: Object.assign({ align: 'left' }, o || {}) }; }
const CHART_BASE = {
  catAxisLabelFontFace: '+mn-lt', valAxisLabelFontFace: '+mn-lt', dataLabelFontFace: '+mn-lt', legendFontFace: '+mn-lt', titleFontFace: '+mj-lt',
  catAxisLabelFontSize: 11, valAxisLabelFontSize: 10, dataLabelFontSize: 10, legendFontSize: 11, titleFontSize: 13,
  catAxisLabelColor: H.dk2, valAxisLabelColor: H.dk2, dataLabelColor: H.dk1, legendColor: H.dk2, titleColor: H.dk1,
  valGridLine: { color: 'E6E1E4', size: 0.5 }, catGridLine: { style: 'none' },
  showTitle: true, showValue: true, dataLabelPosition: 'outEnd',
};

// =====================================================================
// 0. TITLE
// =====================================================================
pres.addSection({ title: 'Opening' });
{
  const s = pres.addSlide({ masterName: 'TITLE', sectionTitle: 'Opening' });
  s.addText('Chandohasam', { placeholder: 'title' });
  s.addText('Towards semantically coherent Telugu metrical poetry generation with text diffusion', { placeholder: 'subtitle' });
  s.addText([
    { text: 'Progress seminar  ·  6 October 2026', options: { breakLine: true, color: C.accent2, bold: true } },
    { text: 'Samvaran Kashyap Rallabandi  ·  Mahesh Emani  ·  Radhe Shyam Salopanthula', options: { breakLine: true } },
    { text: 'IIIT Hyderabad', options: {} },
  ], { placeholder: 'meta' });
  // motif: the weight pattern of śārdūlavikrīḍitamu (ma sa ja sa ta ta ga)
  txt(s, 'U U U  I I U  I U I  I I U  U U I  U U I  U', { x: 0.8, y: 1.45, w: 11, h: 0.5, fontSize: 20, color: C.accent2, fontFace: THEME.headFontFace, charSpacing: 4 });
  txt(s, 'ma · sa · ja · sa · ta · ta · ga  —  śārdūlavikrīḍitamu, the metre of Pothana’s opening verse', { x: 0.8, y: 1.9, w: 11, h: 0.35, fontSize: 12, color: C.accent5, italic: true });
  s.addNotes('Title slide. Welcome; this seminar reports the progress of Chandohasam, strictly as written up in the mid-submission paper.');
  NOTES.push({ n: 0, title: 'Title', note: 'Welcome. This seminar reports the progress of Chandohasam as written up in the mid-submission paper. The decorative line is the weight pattern (ma sa ja sa ta ta ga) of śārdūlavikrīḍitamu, the metre of the Bhāgavatamu’s opening verse, which returns in the demonstration.' });
}

// =====================================================================
// 1. AGENDA
// =====================================================================
pres.addSection({ title: 'Problem' });
{
  const s = content('The narrative in one page', 'Problem',
    'Six movements. 1: the problem, a padyaṃ must balance sound and sense. 2: what chandassu asks of every line. 3: the benchmark and its audit. 4: the deterministic controller (DAWG) and constrained decoding. 5: the results with four generators and our own 120M diffusion model. 6: how to measure poetry, the final architecture and the plan. The story: form is now guaranteed by construction; meaning under form is the open problem and the rest of the project attacks it.');
  const items = [
    ['The problem', 'A padyaṃ must balance śabdaṃ (sound) and arthaṃ (meaning); prior work solves one at the expense of the other.'],
    ['Chandassu', 'Akṣara weights, gaṇas, yati and prāsa; three families of metres; why Telugu is harder than English, Chinese or Sanskrit.'],
    ['The benchmark', '12,673 labelled poems from four sources, audited for metre, meaning and duplication.'],
    ['The controller', 'One DAWG for 37 metres; constrained decoding as a puzzle with no dead ends, for autoregressive and diffusion models.'],
    ['Results', 'Form by construction for every model; the lexical cost of subword tokens; our 120M akṣara-level diffusion model.'],
    ['Measuring poetry', 'Five deterministic metrics from Kāvyālaṅkārasaṅgrahamu, the metrics in design, the final architecture, next steps.'],
  ];
  const cw = (CW - 0.6) / 3, ch = 2.45;
  items.forEach((it, i) => {
    const x = LM + (i % 3) * (cw + 0.3), y = TOP + Math.floor(i / 3) * (ch + 0.3);
    card(s, { x, y, w: cw, h: ch, num: i + 1, head: it[0], text: it[1], fontSize: 14 });
  });
}

// =====================================================================
// 2. PROBLEM STATEMENT
// =====================================================================
{
  const s = content('Problem statement', 'Problem',
    'Goal (paper, abstract and §1): compose Telugu padyaṃs that are metrically accurate and genuinely meaningful at the same time. Three requirements, all at once: strict metre (gaṇa, yati, prāsa), coherent meaning for a given bhāvaṃ, and poetic expression (figures of sound and of meaning). Prior work struggles to satisfy the joint requirement. Our answer is a constrained text-diffusion framework: a deterministic metrical controller guarantees form, the generator supplies words and meaning, a poetry evaluation suite and a semantic coherence metric measure what the controller cannot, and RLVR uses them as rewards.');
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: LM, y: TOP, w: CW, h: 0.95, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, rectRadius: 0.1 });
  txt(s, 'Compose a Telugu padyaṃ that is metrically exact and genuinely meaningful, from a given meaning (bhāvaṃ).', { x: LM + 0.3, y: TOP, w: CW - 0.6, h: 0.95, fontSize: 20, color: C.background1, valign: 'middle', fontFace: THEME.headFontFace });
  const y2 = TOP + 1.15, h2 = 2.35, cw = (CW - 0.6) / 3;
  card(s, { x: LM, y: y2, w: cw, h: h2, head: 'Must be in metre', body: [
    { lead: 'gaṇa: ', text: 'the syllable-weight pattern' },
    { lead: 'yati: ', text: 'a sound match inside the line' },
    { lead: 'prāsa: ', text: 'line-initial rhyme across lines' },
    'all three at once, not as aggregates',
  ], fontSize: 13.5, gap: 4 });
  card(s, { x: LM + cw + 0.3, y: y2, w: cw, h: h2, head: 'Must mean something', body: [
    'coherent ideas, contextually appropriate',
    'the verse must express the given bhāvaṃ',
    'no closed-form check exists for this',
  ], fontSize: 13.5, gap: 4 });
  card(s, { x: LM + 2 * (cw + 0.3), y: y2, w: cw, h: h2, head: 'Must be poetic', body: [
    { lead: 'śabdālaṅkāra: ', text: 'alliteration, repetition' },
    { lead: 'arthālaṅkāra: ', text: 'simile, metaphor, hyperbole, wordplay' },
    'euphony, density and clarity of diction',
  ], fontSize: 13.5, gap: 4 });
  const y3 = y2 + h2 + 0.2;
  txt(s, 'Our answer: Chandohasam', { x: LM, y: y3, w: 4, h: 0.4, fontSize: 16, bold: true, color: C.accent3 });
  const ans = [
    ['Deterministic controller', 'a DAWG over 37 metres, inside the decoding loop'],
    ['Curated benchmark', '12,673 labelled poems with meanings'],
    ['Evaluation suite', 'operationalised from Kāvyālaṅkārasaṅgrahamu'],
    ['Coherence metric + RLVR', 'from expert judgements; rewards for refinement'],
  ];
  const aw = (CW - 0.9) / 4;
  ans.forEach((a, i) => {
    const x = LM + i * (aw + 0.3);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: y3 + 0.45, w: aw, h: 1.15, fill: { color: C.background1 }, line: { color: C.accent3, width: 1 }, rectRadius: 0.1 });
    txt(s, a[0], { x: x + 0.15, y: y3 + 0.52, w: aw - 0.3, h: 0.35, fontSize: 14, bold: true, color: C.accent3 });
    txt(s, a[1], { x: x + 0.15, y: y3 + 0.88, w: aw - 0.3, h: 0.7, fontSize: 12.5, color: C.text2 });
  });
}

// =====================================================================
// 3. WHY POETRY IS HARD: śabdaṃ + arthaṃ
// =====================================================================
{
  const s = content('Why poetry is hard: śabdaṃ and arthaṃ in balance', 'Problem',
    'Paper §1. A poem must do far more than make surface sense. The left circle is the sound side: gaṇa, yati, prāsa, and the figures of sound. The right circle is the meaning side: coherent ideas, contextual fit, and the figures of meaning. The padyaṃ lives in the overlap, which the classical tradition calls śabdārtha samanvaya, sound and sense in equivalence. Pull one way and you get metrically perfect nonsense; pull the other and you get prose. The intertwined constraints make Telugu poetry harder than conventional text generation and than poetry generation in English, Chinese or Hindi.');
  const oy = TOP + 0.15, oh = 4.3, ow = 6.4;
  s.addShape(pres.shapes.OVAL, { x: 0.9, y: oy, w: ow, h: oh, fill: { color: C.accent1, transparency: 82 }, line: { color: C.accent1, width: 1.5 } });
  s.addShape(pres.shapes.OVAL, { x: W - 0.9 - ow, y: oy, w: ow, h: oh, fill: { color: C.accent3, transparency: 82 }, line: { color: C.accent3, width: 1.5 } });
  txt(s, 'śabdaṃ · sound', { x: 1.5, y: oy + 0.5, w: 3.3, h: 0.5, fontSize: 22, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
  bullets(s, [
    { lead: 'gaṇa ', text: 'syllable-weight patterns' },
    { lead: 'yati ', text: 'caesural sound agreement' },
    { lead: 'prāsa ', text: 'line-initial rhyme' },
    { lead: 'śabdālaṅkāra ', text: 'alliteration, repetition' },
    'euphony, density, clarity',
  ], { x: 1.5, y: oy + 1.1, w: 3.4, h: 3.0, fontSize: 14, gap: 6 });
  txt(s, 'arthaṃ · meaning', { x: W - 1.5 - 3.3, y: oy + 0.5, w: 3.3, h: 0.5, fontSize: 22, bold: true, color: C.accent3, fontFace: THEME.headFontFace, align: 'right' });
  bullets(s, [
    'coherent ideas',
    'contextually appropriate',
    'expresses the given bhāvaṃ',
    { lead: 'arthālaṅkāra ', text: 'simile, metaphor, hyperbole, wordplay', leadColor: C.accent3 },
    'hardest to check by machine',
  ], { x: W - 1.5 - 3.4, y: oy + 1.1, w: 3.4, h: 3.0, fontSize: 14, gap: 6 });
  // overlap label
  txt(s, 'padyaṃ', { x: W / 2 - 1.3, y: oy + 1.35, w: 2.6, h: 0.6, fontSize: 26, bold: true, color: C.text1, align: 'center', fontFace: THEME.headFontFace });
  txt(s, 'śabdārtha samanvaya\nsound and sense in equivalence\n(Kāvyālaṅkārasaṅgrahamu, 16th c.)', { x: W / 2 - 1.5, y: oy + 2.0, w: 3.0, h: 1.3, fontSize: 12.5, color: C.text2, align: 'center', italic: true });
  caption(s, 'Metre without meaning is noise in perfect rhythm; meaning without metre is prose. Prior work solves one side at the expense of the other.', { x: LM, y: TOP + oh + 0.35, w: CW, h: 0.5, fontSize: 14, align: 'center', italic: false, color: C.text1 });
}

// =====================================================================
// 4. EXISTING METHODS
// =====================================================================
{
  const s = content('Existing methods and their flaws', 'Problem',
    'Paper §2. Two routes. The soft route steers a model and discards failures: Deep-speare (English sonnets), SongNet (Chinese SongCi), PoeLM (control codes, generate many, keep what passes a scansion check; Spanish and Basque), and a Bangla adaptation with rhyme, matra-count, word-count and line-boundary tokens that follows the requested structure over 90% of the time. But those constraints are aggregates, and the authors report semantic drift when several control tokens apply at once. The hard route guarantees form at decode time (Ghazvininejad 2016, NeuroLogic 2021, grammar-constrained decoding 2023). For Sanskrit, Chandomitra and PINGALA reach near-perfect Anushtubh metre with greedy decoding, yet human raters score coherence at 2.1 to 2.7 out of 5. PoetryDiffusion aims at both with text diffusion and a BERT-based metrical controller. Our position: keep a deterministic controller inside the decoding loop and work on meaning.');
  const cw = (CW - 0.3) / 2, ch = 3.55;
  card(s, { x: LM, y: TOP, w: cw, h: ch, head: 'Soft route: steer the model, discard failures', body: [
    { lead: 'Deep-speare ', text: '(Lau et al., 2018): meter learnt jointly with language, English sonnets' },
    { lead: 'SongNet ', text: '(Li et al., 2020): rigid formats for Chinese SongCi' },
    { lead: 'PoeLM ', text: '(Ormazabal et al., 2022): control codes, sample many, keep what passes scansion' },
    { lead: 'Bangla ', text: '(Amina et al., 2025): rhyme, matra, word-count tokens; follows the structure > 90%' },
    { lead: 'Flaw: ', text: 'constraints are aggregates (a matra total, an end rhyme); semantic drift when several control tokens apply', leadColor: C.accent3 },
  ], fontSize: 13.5, gap: 4 });
  card(s, { x: LM + cw + 0.3, y: TOP, w: cw, h: ch, head: 'Hard route: guarantee form at decode time', body: [
    { lead: 'Constrained decoding ', text: '(Ghazvininejad et al., 2016; Lu et al., 2021; Geng et al., 2023)' },
    { lead: 'Chandomitra, PINGALA ', text: '(Jagadeeshan et al., 2026a, b): near-perfect Anushtubh metre with greedy decoding' },
    { lead: 'Flaw: ', text: 'human raters score coherence at 2.1 to 2.7 on a 5-point scale', leadColor: C.accent3 },
    { lead: 'PoetryDiffusion ', text: '(Hu et al., 2023): text diffusion with a learned BERT metrical controller, aims at both' },
  ], fontSize: 13.5, gap: 4 });
  const y3 = TOP + ch + 0.3;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: LM, y: y3, w: CW, h: 1.25, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, rectRadius: 0.1 });
  txt(s, [
    { text: 'Metre is close to solved; meaning under metre is not.', options: { bold: true, breakLine: true, fontSize: 18, fontFace: THEME.headFontFace } },
    { text: 'We keep a deterministic metrical controller inside the decoding loop and attack semantic coherence on top of it.', options: { fontSize: 14 } },
  ], { x: LM + 0.3, y: y3 + 0.1, w: CW - 0.6, h: 1.05, color: C.background1, valign: 'middle' });
}

// =====================================================================
// 5. WHY TELUGU IS DIFFERENT
// =====================================================================
{
  const s = content('Why Telugu is different', 'Problem',
    'Paper §1 to §2 and §4.2. Four reasons. One: every line carries three simultaneous constraints, gaṇa, yati and prāsa, which are positional, not aggregates like a matra total or an end rhyme. Two: 37 metres in three families, including class-based (jāti) metres whose gaṇas are chosen from classes, and composite (upajāti) metres. Three: the alpha-syllabary script. The weight of an akṣara stays pending until the next onset is known, because a following conjunct makes it heavy, and sandhi can hide a yati seat; a general subword tokenizer spends 1.2 to 1.4 tokens per akṣara. Four: the evaluation gap. Sanskrit has a deterministic metre identifier; Telugu had only an approximate post-hoc checker; nothing exists for meaning; MAUVE is unvalidated on classical poetry; śabdālaṅkāra identifiers exist only for Sanskrit, and arthālaṅkāras are out of reach for deterministic modelling.');
  const cw = (CW - 0.3) / 2, ch = 2.55;
  const cards = [
    ['Three constraints on every line, at once', ['gaṇa grid from the first akṣara', 'prāsa: second akṣara of every line repeats a consonant', 'yati: a seat inside the line must agree in sound with the line’s first akṣara (vaḷi)', 'positional rules, not aggregates']],
    ['37 metres in three families', ['26 vṛtta: a fixed gaṇa sequence', '8 jāti: gaṇa classes, lines of varying length', '3 upajāti: composite stanzas, no prāsa', 'one controller must serve all of them']],
    ['An alpha-syllabary script', ['an akṣara’s weight stays pending until the next onset: a following conjunct makes it heavy', 'sandhi can hide a yati seat', 'subword tokenizers spend 1.2 to 1.4 tokens per akṣara']],
    ['An evaluation gap', ['metre: a deterministic identifier for Sanskrit, only an approximate checker for Telugu', 'meaning: no metric; MAUVE unvalidated on classical poetry', 'śabdālaṅkāra identifiers exist only for Sanskrit']],
  ];
  cards.forEach((c, i) => {
    const x = LM + (i % 2) * (cw + 0.3), y = TOP + Math.floor(i / 2) * (ch + 0.25);
    card(s, { x, y, w: cw, h: ch, num: i + 1, head: c[0], body: c[1], fontSize: 13.5, gap: 4 });
  });
}

// =====================================================================
// 6. CHANDASSU AND AKṢARA
// =====================================================================
pres.addSection({ title: 'Chandassu' });
{
  const s = content('Chandassu and the akṣara: what is annotated', 'Chandassu',
    'Paper, Appendix A terms and §4.2. An akṣara is a syllable; it is guru (heavy, U) or laghu (light, I). A gaṇa is a fixed group of weights: bha = UII, ja = IUI, sa = IIU, na = III, ya = IUU, ra = UIU, ta = UUI, ma = UUU, ga = U, va = IU, gaga = UU. A poem has pādas (lines). At a yati seat the akṣara must agree in sound (maitri) with the vaḷi, the first akṣara of the line. By prāsa, the second akṣara of every line repeats the consonant of the second akṣara of line 1. On the right is the controller’s own annotation of pāda 1 of Pothana’s opening verse: scanned into akṣaras with weights, split into gaṇas ma sa ja sa ta ta ga, the yati at akṣara 13 matched to the vaḷi, the prāsa consonant క held across all four lines. Note the pāda-final laghu read as guru. Weights are settled by the following onset, so the annotation is a lattice until the next consonant is known.');
  const lw = 5.0;
  bullets(s, [
    { lead: 'akṣara ', text: 'a syllable; guru (heavy, U) or laghu (light, I)' },
    { lead: 'gaṇa ', text: 'a fixed group of weights: bha UII, ja IUI, sa IIU, na III, ya IUU, ra UIU, ta UUI, ma UUU, ga U, va IU' },
    { lead: 'pāda ', text: 'a line; a slot is a kind of line a metre allows' },
    { lead: 'yati ', text: 'at a yati seat the akṣara must agree in sound (maitri) with the line’s first akṣara, the vaḷi' },
    { lead: 'prāsa ', text: 'the second akṣara of every line repeats the consonant of line 1’s second akṣara' },
    { lead: 'pending weight ', text: 'a light akṣara before a conjunct is heavy, so a weight is settled only by the next onset' },
  ], { x: LM, y: TOP, w: lw, h: 5.3, fontSize: 14, gap: 7 });
  // annotated example
  const ex = LM + lw + 0.35, ew = CW - lw - 0.35;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: ex, y: TOP, w: ew, h: 5.3, fill: { color: C.background2 }, line: { color: C.background2, width: 0 }, rectRadius: 0.1 });
  txt(s, 'Annotated: pāda 1 of Pothana’s opening verse (śārdūlavikrīḍitamu)', { x: ex + 0.2, y: TOP + 0.15, w: ew - 0.4, h: 0.4, fontSize: 14, bold: true, color: C.accent1 });
  txt(s, 'శ్రీకైవల్య పదంబుఁ జేరుటకునై చింతించెదన్ లోకర', { x: ex + 0.2, y: TOP + 0.6, w: ew - 0.4, h: 0.5, fontSize: 18, fontFace: TE, color: C.text1 });
  const g = [['మ', 'శ్రీ కై వ', 'U U U'], ['స', 'ల్య ప దం', 'I I U'], ['జ', 'బుఁ జే రు', 'I U I'], ['స', 'ట కు నై', 'I I U'], ['త', 'చిం తిం చె', 'U U I'], ['త', 'దన్ లో క', 'U U I'], ['గ', 'ర', 'I → U']];
  const rows = [
    g.map(c => ({ text: c[0], options: { bold: true, fill: { color: H.accent1 }, color: H.lt1, align: 'center', fontFace: TE } })),
    g.map(c => ({ text: c[1], options: { align: 'center', fontFace: TE, fill: { color: H.lt1 } } })),
    g.map(c => ({ text: c[2], options: { align: 'center', fill: { color: H.lt1 }, color: H.accent3, bold: true } })),
  ];
  const colW = [0.9, 1.0, 1.0, 0.95, 1.05, 1.0, 0.8];
  s.addTable(rows, tableOpts({ x: ex + 0.2, y: TOP + 1.2, w: ew - 0.4, colW, fontSize: 12, rowH: [0.35, 0.42, 0.33] }));
  const tel = (t) => ({ text: t, options: { fontFace: TE } });
  s.addText([
    { text: 'gaṇas ', options: { bullet: true, bold: true, color: C.accent1, paraSpaceAfter: 6 } },
    { text: 'ma sa ja sa ta ta ga: 19 akṣaras; the pāda-final laghu (', options: {} }, tel('ర'), { text: ') reads as guru', options: { breakLine: true } },
    { text: 'yati 1–13 ', options: { bullet: true, bold: true, color: C.accent1, paraSpaceAfter: 6 } },
    tel('శ్రీ – చిం'), { text: ': sound-class match with the vaḷi (sarasa yati)', options: { breakLine: true } },
    { text: 'prāsa ', options: { bullet: true, bold: true, color: C.accent1, paraSpaceAfter: 6 } },
    tel('క'), { text: ' in akṣara 2 of all four pādas: ', options: {} }, tel('శ్రీ·కై, క్షై·కా, ద్రే·క, నా·కం'), { text: '', options: { breakLine: true } },
    { text: 'scansion ', options: { bullet: true, bold: true, color: C.accent1, paraSpaceAfter: 6 } },
    { text: 'the controller settles each weight from the following onset; output of python3 -m chandohasam', options: {} },
  ], { x: ex + 0.2, y: TOP + 2.55, w: ew - 0.4, h: 2.6, fontSize: 13, color: C.text1, margin: 0, valign: 'top', isTextBox: true });
}

// =====================================================================
// 7. THREE TYPES OF METRES
// =====================================================================
{
  const s = content('Three families of metres: fixed, class-based, composite', 'Chandassu',
    'Paper, Table 6 (the 37 metres). Vṛtta (26): a fixed gaṇa sequence per pāda, e.g. utpalamāla bha ra na bha bha ra va, 20 akṣaras, yati at akṣara 10; śārdūlavikrīḍitamu ma sa ja sa ta ta ga, 19 akṣaras, yati at 13; some have two or three yati seats (sragdhara 8 and 15; mānini 7, 13, 19). Jāti (8): the line is a sequence of gaṇa classes, and each position may take any gaṇa of its class: sūrya = na, ha; indra = bha, ra, ta, nala, naga, sala; kanda = bha, ja, sa, nala, gaga. So the line length varies and the yati sits at the first akṣara of a given gaṇa. Kandamu has two slots, odd lines of 3 kanda gaṇas and even lines of 5. Upajāti (3): sīsamu (6 indra + 2 sūrya, followed by a gīti), āṭaveladi, tēṭagīti; no prāsa, and prāsa-yati is accepted in place of yati. The figure shows the controller’s rule card for kandamu, with the yati seat at gaṇa 4 of the even slot.');
  const cw = (CW - 0.6) / 3, ch = 2.9;
  card(s, { x: LM, y: TOP, w: cw, h: ch, head: 'vṛtta · 26 metres · fixed', body: [
    'one gaṇa sequence per pāda, four pādas; prāsa: yes',
    { lead: 'utpalamāla ', text: 'bha ra na bha bha ra va (20), yati 10' },
    { lead: 'śārdūlavikrīḍitamu ', text: 'ma sa ja sa ta ta ga (19), yati 13' },
    { lead: 'sragdhara ', text: 'ma ra bha na ya ya ya (21), yati 8, 15' },
  ], fontSize: 12.5, gap: 4, headColor: C.accent1 });
  card(s, { x: LM + cw + 0.3, y: TOP, w: cw, h: ch, head: 'jāti · 8 metres · class-based', body: [
    'each position takes any gaṇa of its class, so line length varies; prāsa: yes',
    { lead: 'sūrya ', text: 'na, ha', leadColor: C.accent3 },
    { lead: 'indra ', text: 'bha, ra, ta, nala, naga, sala', leadColor: C.accent3 },
    { lead: 'kandamu ', text: 'odd 3, even 5 kanda gaṇas; yati at gaṇa 4' },
    'yati at the first akṣara of a gaṇa',
  ], fontSize: 12.5, gap: 4, headColor: C.accent3 });
  card(s, { x: LM + 2 * (cw + 0.3), y: TOP, w: cw, h: ch, head: 'upajāti · 3 metres · composite', body: [
    { lead: 'sīsamu ', text: '6 indra + 2 sūrya, then a gīti' },
    { lead: 'āṭaveladi ', text: 'odd 3 sūrya + 2 indra; even 5 sūrya' },
    { lead: 'tēṭagīti ', text: '1 sūrya + 2 indra + 2 sūrya' },
    'no prāsa; prāsa-yati accepted in place of yati',
  ], fontSize: 12.5, gap: 4, headColor: C.accent2 });
  const fy = TOP + ch + 0.2, fh = 6.85 - fy, fw = fh * 1738 / 619;
  s.addImage({ path: path.join(FIG, 'fig_kandamu_slots.png'), x: (W - fw) / 2, y: fy, w: fw, h: fh });
}

// =====================================================================
// 8. CONSTRAINED DECODING IS A PUZZLE
// =====================================================================
pres.addSection({ title: 'Controller' });
{
  const s = content('Constrained decoding is a puzzle with no dead ends', 'Controller',
    'Paper §4.1 (viable_prefix, next_symbols) and §4.2. Think of writing the poem as solving a puzzle. Each akṣara placed narrows the set of metres that can still be completed. The chain shows the controller’s own viable_prefix query: after one guru, 28 (metre, slot) hypotheses are alive; after U U, 14; after U U U, 7; after U U U I, 4; after U U U I I U, 3; after U U U I I U I U, only śārdūlavikrīḍitamu remains. A move that leaves no completable metre is simply not offered. Rules of the game: the gaṇa grid masks from the first token; prāsa and yati act once their anchor is written; liveness is exact, so there are no dead ends and every finished poem is valid; the language model chooses among allowed moves, the controller never writes the poem; and meaning has no closed-form check, it is left to the generator and the evaluation.');
  const chain = [['U', '28'], ['U U', '14'], ['U U U', '7'], ['U U U I', '4'], ['U U U I I U', '3'], ['U U U I I U I U', '1']];
  const bw = 1.7, gap = 0.34, by = TOP + 0.15, bh = 1.25;
  const total = chain.length * bw + (chain.length - 1) * gap;
  const x0 = (W - total) / 2;
  chain.forEach((c, i) => {
    const x = x0 + i * (bw + gap);
    const last = i === chain.length - 1;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: by, w: bw, h: bh, fill: { color: last ? C.accent1 : C.background2 }, line: { color: last ? C.accent1 : C.background2, width: 0 }, rectRadius: 0.1 });
    txt(s, c[0], { x, y: by + 0.1, w: bw, h: 0.35, fontSize: 12, align: 'center', color: last ? C.accent6 : C.text2, fontFace: THEME.headFontFace, bold: true });
    txt(s, c[1], { x, y: by + 0.42, w: bw, h: 0.55, fontSize: 28, bold: true, align: 'center', color: last ? C.background1 : C.accent1, fontFace: THEME.headFontFace, valign: 'middle' });
    txt(s, last ? 'śārdūla-\nvikrīḍitamu' : 'hypotheses alive', { x, y: by + 0.92, w: bw, h: 0.32, fontSize: 9.5, align: 'center', color: last ? C.accent6 : C.text2, valign: 'top' });
    if (!last) arrow(s, x + bw + 0.04, by + bh / 2, x + bw + gap - 0.04, by + bh / 2);
  });
  caption(s, 'The controller’s viable_prefix query on a growing weight prefix: how many (metre, slot) hypotheses can still be completed.', { x: LM, y: by + bh + 0.1, w: CW, h: 0.35, align: 'center' });
  const ry = by + bh + 0.6, rh = 6.85 - ry, rw = (CW - 0.6) / 3;
  const rules = [
    ['The grid acts from the first token', 'Only tokens whose akṣaras leave at least one completable metre slot are allowed; all others are masked.'],
    ['Prāsa and yati join once anchored', 'The second akṣara of line 1 fixes the prāsa register; each line’s first akṣara fixes its yati register.'],
    ['Exact liveness: no dead ends', 'A valid path can never get stuck, so every completed poem satisfies the metre; meaning is left to the model and the evaluation.'],
  ];
  rules.forEach((r, i) => card(s, { x: LM + i * (rw + 0.3), y: ry, w: rw, h: rh, num: i + 1, head: r[0], text: r[1], fontSize: 13.5 }));
}

// =====================================================================
// 9. DATASETS
// =====================================================================
pres.addSection({ title: 'Data' });
{
  const s = content('The benchmark: 12,673 labelled poems, four sources', 'Data',
    'Paper §3 and Table 1. Sources: Pothana’s Āndhra Mahābhāgavatamu from an online compilation with word glosses and meanings (the golden set: largest, edition meanings); Vemana’s śatakam; Kuchimanchi Timmakavi’s acca-telugu Rāmāyaṇamu and three śatakams; and the Chandassu dataset of Pavan and Sree (2025) from its Kaggle release. Meanings for the last three are LLM-generated (Gemini), and every English meaning is a machine translation of the Telugu bhāvaṃ. Table 1 gives the validity rates the controller measures: gaṇa 95.3% overall (99.85% on Bhāgavatamu), prāsa 99.2% relaxed and 95.9% strict, yati 91.5% relaxed and 90.6% strict. Chandassu and Vemana are the noisiest on gaṇa, 85.0% and 87.2%.');
  const rows = [
    [hdr('Rule, labelled verse poems', { align: 'left' }), hdr('Bhāgavatamu'), hdr('Vemana'), hdr('Kuchimanchi'), hdr('Chandassu'), hdr('Total')],
    [lcell('Poems', { bold: true }), cell('7,366'), cell('1,164'), cell('1,611'), cell('2,532'), cell('12,673', { bold: true })],
    [lcell('1. gaṇa'), cell('99.85%'), cell('87.2%'), cell('96.5%'), cell('85.0%'), cell('95.3%', { bold: true })],
    [lcell('2. prāsa, relaxed (strict)'), cell('99.8% (96.7%)'), cell('95.6% (93.4%)'), cell('99.9% (97.7%)'), cell('98.8% (93.7%)'), cell('99.2% (95.9%)', { bold: true })],
    [lcell('3. yati, relaxed (strict)'), cell('91.4% (90.7%)'), cell('96.4% (95.7%)'), cell('93.9% (92.9%)'), cell('87.9% (86.6%)'), cell('91.5% (90.6%)', { bold: true })],
  ];
  s.addTable(rows, tableOpts({ x: LM, y: TOP, w: CW, colW: [3.1, 1.9, 1.8, 1.9, 1.8, 1.63], fontSize: 13, rowH: 0.42 }));
  caption(s, 'Table 1 of the paper: validity rates measured by the controller; strict values in parentheses.', { x: LM, y: TOP + 2.25, w: CW, h: 0.3 });
  const y2 = TOP + 2.75, cw = (CW - 0.3) / 2, ch = 6.85 - y2;
  card(s, { x: LM, y: y2, w: cw, h: ch, head: 'Sources', body: [
    { lead: 'Bhāgavatamu ', text: 'Pothana’s Āndhra Mahābhāgavatamu, online compilation with word glosses and meanings: the golden set' },
    { lead: 'Vemana ', text: 'the śatakam' },
    { lead: 'Kuchimanchi ', text: 'Timmakavi’s acca-telugu Rāmāyaṇamu; ciravibhava, kukkuṭeśvara and śrībharga śatakams' },
    { lead: 'Chandassu ', text: 'Pavan and Sree (2025), Kaggle release (Boddu, 2025)' },
  ], fontSize: 13, gap: 4 });
  card(s, { x: LM + cw + 0.3, y: y2, w: cw, h: ch, head: 'Meanings and labels', body: [
    'Bhāgavatamu meanings come from the edition; the rest are LLM-generated (Gemini)',
    'every English meaning is a machine translation of the Telugu bhāvaṃ',
    'metre labels checked by the controller; gaṇa validity is lowest on Chandassu (85.0%) and Vemana (87.2%)',
    'quality gauged by metrical correctness, length ratio, embedding similarity, lexical and metrical diversity, author diversity, deduplication',
  ], fontSize: 13, gap: 4 });
}

// =====================================================================
// 10. DATA SANITY
// =====================================================================
{
  const s = content('Data sanity: do the meanings belong to their poems?', 'Data',
    'Paper §3 and Table 2. Two gates compare each poem with its own meaning against a shuffled pairing. The length-ratio gate (meaning length over verse length in [0.8, 2.5]) separates real from shuffled in three files, 96 to 98% against 62 to 67%, but not in Vemana, whose machine meanings are of uniform length (84.5% against 82.6%). The LaBSE Telugu–English gate (cosine at or above 0.65) passes 90 to 98% of real pairs and none of the shuffled, but it measures translation consistency since the English is a translation of the Telugu meaning; on the pair that bears on fidelity, poem versus Telugu meaning, LaBSE still ranks the correct pairing first with AUC 0.85 to 0.94. Lexical diversity is similar across files (type–token ratio 0.59 to 0.64). Verbatim duplication is negligible: 13 near-duplicate pairs among 12,704 poems. The remaining repetition is formulaic: refrains recur in 77.1% of Vemana’s poems and 25.3% of Chandassu’s, which raises Vemana’s Yule’s K to 99.9 against 1.4 to 4.1 elsewhere; evaluation splits must keep refrain groups together. A general subword tokenizer (Gemma-4) spends 1.23 to 1.36 tokens per akṣara, which motivates the syllable tokenizer.');
  const labels = ['Bhāgavatamu', 'Vemana', 'Kuchimanchi', 'Chandassu'];
  const chartW = 7.3;
  s.addChart(pres.charts.BAR, [
    { name: 'real pair', labels, values: [90.2, 98.4, 97.7, 96.4] },
    { name: 'shuffled pair', labels, values: [0.0, 0.1, 0.0, 0.0] },
  ], Object.assign({}, CHART_BASE, {
    x: LM, y: TOP, w: chartW, h: 2.65, barDir: 'col', barGrouping: 'clustered', barGapWidthPct: 60,
    chartColors: [H.accent1, H.accent5], title: 'LaBSE Te–En gate (cosine ≥ 0.65): poems passing, %',
    valAxisMinVal: 0, valAxisMaxVal: 100, valAxisMajorUnit: 25, dataLabelFormatCode: '0.0', showLegend: true, legendPos: 'r',
  }));
  s.addChart(pres.charts.BAR, [
    { name: 'real pair', labels, values: [96.2, 84.5, 98.1, 97.6] },
    { name: 'shuffled pair', labels, values: [62.3, 82.6, 66.6, 67.3] },
  ], Object.assign({}, CHART_BASE, {
    x: LM, y: TOP + 2.75, w: chartW, h: 2.65, barDir: 'col', barGrouping: 'clustered', barGapWidthPct: 60,
    chartColors: [H.accent3, H.accent5], title: 'Length-ratio gate (meaning / verse in [0.8, 2.5]): poems passing, %',
    valAxisMinVal: 0, valAxisMaxVal: 100, valAxisMajorUnit: 25, dataLabelFormatCode: '0.0', showLegend: true, legendPos: 'r',
  }));
  const rx = LM + chartW + 0.3, rw = CW - chartW - 0.3;
  card(s, { x: rx, y: TOP, w: rw, h: 5.4, head: 'What Table 2 says', body: [
    { lead: 'Fidelity: ', text: 'poem vs. its Telugu meaning, LaBSE ranks the true pairing first with AUC 0.85–0.94' },
    { lead: 'Uniform machine meanings: ', text: 'the length gate cannot separate Vemana (84.5 vs 82.6)' },
    { lead: 'Diversity: ', text: 'type–token ratio 0.59–0.64 in every file' },
    { lead: 'Duplication: ', text: '13 near-duplicate pairs among 12,704 poems (3-gram Jaccard ≥ 0.7)' },
    { lead: 'Refrains: ', text: '77.1% of Vemana and 25.3% of Chandassu poems share a pāda; Yule’s K 99.9 vs 1.4–4.1, so splits keep refrain groups together' },
    { lead: 'Tokens: ', text: 'Gemma-4 subwords spend 1.23–1.36 tokens per akṣara, motivating a syllable tokenizer' },
  ], fontSize: 13, gap: 5 });
}

// =====================================================================
// 11. THE DAWG
// =====================================================================
{
  const s = content('The DAWG: every legal line of a metre, stored once', 'Controller',
    'Paper §4.1 and Figure 1. Take a toy slot of two gaṇas, each UU, IIU or UII. It has 9 legal lines. Stored as a trie, that is 29 states, because the three ways of finishing gaṇa 1 each carry their own copy of gaṇa 2. A DAWG, a minimal deterministic acyclic automaton, merges states with equal futures: the three ways to finish gaṇa 1 meet in one state and gaṇa 2 is stored once, 11 states and 14 edges for the same 9 lines. The decoder’s question is: after the prefix U I, what may follow? Here only I. Construction follows Daciuk et al. (2000) and the full catalogue builds in under half a second.');
  const fw = 10.2, fh = fw * 857 / 2505;
  s.addImage({ path: path.join(FIG, 'fig_dawg_trie_to_dawg.png'), x: (W - fw) / 2, y: TOP - 0.1, w: fw, h: fh });
  const y2 = TOP - 0.1 + fh + 0.15, cw = (CW - 0.6) / 3, ch = 6.85 - y2;
  card(s, { x: LM, y: y2, w: cw, h: ch, head: 'Directed acyclic word graph', text: 'A minimal deterministic acyclic automaton over U and I. A line is legal when its weights lead from the start to a final state; lines are bounded, so there are no cycles.', fontSize: 12.5, headSize: 15 });
  card(s, { x: LM + cw + 0.3, y: y2, w: cw, h: ch, head: 'Merge equal futures', text: 'States with the same completions become one, so each shared suffix is stored once: 29 trie states become 11 states and 14 edges for the same 9 lines (Daciuk et al., 2000).', fontSize: 12.5, headSize: 15 });
  card(s, { x: LM + 2 * (cw + 0.3), y: y2, w: cw, h: ch, head: 'The decoder’s query', text: 'next_symbols: which weights may follow this prefix? After U I, only I. The answer is a lookup, cheap enough for every token of every decoding step.', fontSize: 12.5, headSize: 15 });
}

// =====================================================================
// 12. ONE DAWG FOR ALL 37 METRES
// =====================================================================
{
  const s = content('One labelled DAWG for all 37 metres', 'Controller',
    'Paper §4.1 and Algorithm 1. The rules are data: YAML specifications of 37 metres and their gaṇa classes, with 64 prāsa and 92 yati rules derived from Kakanuri Appakavi’s Appakavīyaṃ. Each metre is a prosodic grammar, poem → lines → gaṇa classes → gaṇas → U/I. The grammar is flattened into one right-linear grammar per line slot (a vṛtta has one slot; kandamu has two, its odd and even lines), turned into an automaton per slot, united, made deterministic into a DFA of 1,573 states whose accepting states carry their (metre, slot) labels, and then minimised while preserving labels into the DAWG: 1,431 states, 2,514 edges, exactly the 370,315 legal lines, built in under half a second. Three queries: identify walks a poem’s scansion lattice and returns every accepting metre and slot and the point at which each rejected metre became impossible; viable_prefix and next_symbols return what can still lead to a completed slot; segment returns gaṇa divisions and yati positions. Validation, independent of generation: of 7,366 Bhāgavatamu poems with catalogue metres, 7,355 are identified with their labelled metre (99.85%), none as a wrong metre, and 10 are rejected as unclassified.');
  const fx = LM, fw = 5.3, bh = 0.72, gap = 0.2;
  const steps = [
    ['Rules as data (YAML)', '37 metres, gaṇa classes; 64 prāsa and 92 yati rules from Appakavīyaṃ'],
    ['Prosodic grammar per metre', 'poem → lines → gaṇa classes → gaṇas → U / I'],
    ['Right-linear grammar per line slot', 'a vṛtta has one slot; kandamu has two (odd, even)'],
    ['Union + subset construction', 'a DFA of 1,573 states; accepting states carry (metre, slot) labels'],
    ['Label-preserving minimisation', 'the DAWG: 1,431 states · 2,514 edges · 370,315 legal lines · < 0.5 s'],
  ];
  steps.forEach((st, i) => {
    const y = TOP + i * (bh + gap);
    const last = i === steps.length - 1;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: fx, y, w: fw, h: bh, fill: { color: last ? C.accent1 : C.background2 }, line: { color: last ? C.accent1 : C.background2, width: 0 }, rectRadius: 0.08 });
    txt(s, st[0], { x: fx + 0.2, y: y + 0.07, w: fw - 0.4, h: 0.3, fontSize: 14, bold: true, color: last ? C.background1 : C.accent1 });
    txt(s, st[1], { x: fx + 0.2, y: y + 0.37, w: fw - 0.4, h: 0.32, fontSize: 12, color: last ? C.accent6 : C.text2 });
    if (!last) arrow(s, fx + fw / 2, y + bh + 0.02, fx + fw / 2, y + bh + gap - 0.02);
  });
  const rx = LM + fw + 0.4, rw = CW - fw - 0.4;
  txt(s, 'Three queries for the decoder', { x: rx, y: TOP, w: rw, h: 0.35, fontSize: 16, bold: true, color: C.accent3 });
  bullets(s, [
    { lead: 'identify ', text: 'walks a poem’s scansion lattice; returns every accepting metre and slot, and where each rejected metre became impossible', leadColor: C.accent3 },
    { lead: 'viable_prefix / next_symbols ', text: 'the symbols that can still lead to a completed metre slot: the valid continuation set', leadColor: C.accent3 },
    { lead: 'segment ', text: 'the gaṇa divisions and the yati positions', leadColor: C.accent3 },
  ], { x: rx, y: TOP + 0.4, w: rw, h: 2.2, fontSize: 13.5, gap: 5 });
  txt(s, 'Validated on the Bhāgavatamu, independently of generation', { x: rx, y: TOP + 2.65, w: rw, h: 0.35, fontSize: 16, bold: true, color: C.accent3 });
  const sw = (rw - 0.4) / 3, sy = TOP + 3.1, sh = 1.5;
  stat(s, { x: rx, y: sy, w: sw, h: sh, value: '99.85%', label: '7,355 of 7,366 poems identified with their labelled metre' });
  stat(s, { x: rx + sw + 0.2, y: sy, w: sw, h: sh, value: '0', label: 'identified as a wrong metre' });
  stat(s, { x: rx + 2 * (sw + 0.2), y: sy, w: sw, h: sh, value: '10', label: 'rejected as unclassified' });
}

// =====================================================================
// 13. THE ENFORCER
// =====================================================================
{
  const s = content('Inside the decoding loop: the enforcer', 'Controller',
    'Paper §4.2 and Algorithm 2. The DAWG is a hard constraint, not a post-hoc validator. The enforcer keeps a state with four parts: the live automaton states of the chosen metre, the last akṣaras whose weight is still open, the prāsa register (the consonant of line 1’s second akṣara) and the yati register (the line’s first akṣara, the vaḷi). For each new akṣara: settle the open weights by its first consonant; move every live state along the settled weights and drop those with no move; if it is the second akṣara of a line and breaks the prāsa, DEAD; drop the states whose gaṇa division puts it on a yati seat where it is not in maitri with the vaḷi; if no state can still reach the end of the poem, DEAD. A token is allowed when the state stays alive after all of its akṣaras, cached per state. Because liveness is exact, a valid decoding path cannot reach a dead end, and every completed poem satisfies the selected metre and its structural constraints.');
  const lw = 4.4;
  card(s, { x: LM, y: TOP, w: lw, h: 5.4, head: 'Enforcer state σ, four parts', body: [
    { lead: 'Q ', text: 'the live states of the metre’s automaton the text may be in' },
    { lead: 'w ', text: 'the last akṣaras whose weight is still open (a light akṣara before a conjunct is heavy)' },
    { lead: 'prāsa register ', text: 'the consonant of line 1’s second akṣara, which every line’s second akṣara must repeat' },
    { lead: 'yati register ', text: 'the line’s first akṣara (the vaḷi), with which the akṣara at a yati seat must agree in sound' },
  ], fontSize: 13.5, gap: 7 });
  const rx = LM + lw + 0.35, rw = CW - lw - 0.35;
  txt(s, 'For each next akṣara a (or a space or a line break)', { x: rx, y: TOP, w: rw, h: 0.35, fontSize: 15, bold: true, color: C.accent3 });
  const steps = [
    'Settle the open weights in w by the first consonant of a.',
    'Move each state in Q along the settled weights; drop those with no move.',
    'If a is the second akṣara of a line and breaks the prāsa: DEAD.',
    'Drop the states whose gaṇa division puts a on a yati seat where a is not in maitri with the vaḷi.',
    'If no state in Q can still reach the end of the poem: DEAD; otherwise return the updated σ.',
  ];
  steps.forEach((t, i) => {
    const y = TOP + 0.5 + i * 0.66;
    numCircle(s, rx, y + 0.05, i + 1, C.accent3);
    txt(s, t, { x: rx + 0.65, y, w: rw - 0.65, h: 0.6, fontSize: 13.5, valign: 'middle' });
  });
  const by = TOP + 0.5 + 5 * 0.66 + 0.15;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: rx, y: by, w: rw, h: 6.85 - by, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, rectRadius: 0.1 });
  txt(s, [
    { text: 'A token is allowed when σ stays alive after all of its akṣaras (cached per state).', options: { breakLine: true, bold: true } },
    { text: 'Liveness is exact: decoding never reaches a dead end, and every finished poem is valid for the metre, its prāsa and its yati.', options: {} },
  ], { x: rx + 0.25, y: by + 0.1, w: rw - 0.5, h: 6.85 - by - 0.2, fontSize: 13.5, color: C.background1, valign: 'middle' });
}

// =====================================================================
// 14. ATTACHING TO AR AND DIFFUSION MODELS
// =====================================================================
{
  const s = content('The same controller on autoregressive and diffusion models', 'Controller',
    'Paper §4.2, §4.3 and Algorithm 3. Four generators, one controller, applied as ablations so that the effect of the model and the decoding paradigm is isolated with the formal constraints fixed. Autoregressive (gemma-4-E4B-it, gemma-4-26B-A4B-it): the DAWG masks the next-token distribution directly; initial temperature 0.7. Block diffusion (diffusiongemma-26B-A4B-it-NVFP4): the model’s proposals are committed left to right when allowed and sufficiently confident; otherwise decoding selects the first open position, and a backtrack returns committed positions to noise. Masked diffusion (chandohasam 120M, ours): the constraint is applied to the positions being resolved while the committed context the controller needs is preserved; a 512-token canvas with the meaning unmasked, lines decoded left to right within the line. Three strategies: masking only samples from the model after removing invalid tokens (top-p 90%); masking with backtracking saves checkpoints every third step (last 15), rewinds when stuck (fewer than 3 allowed tokens, less than 0.001 of the probability mass, or 4 steps without a new akṣara) and raises the temperature by 0.15 per consecutive backtrack up to 1.2; hybrid walks the allowed tokens by probability (at most 100) collecting those that complete the line.');
  const cw = (CW - 0.6) / 3, ch = 3.0;
  card(s, { x: LM, y: TOP, w: cw, h: ch, head: 'Autoregressive', body: [
    { lead: 'gemma-4-E4B-it, gemma-4-26B-A4B-it', text: '' },
    'the DAWG masks the next-token distribution directly',
    'initial temperature 0.7',
    'subword tokens: one token may hold several akṣaras, or part of one',
  ], fontSize: 13, gap: 5 });
  card(s, { x: LM + cw + 0.3, y: TOP, w: cw, h: ch, head: 'Block diffusion', body: [
    { lead: 'diffusiongemma-26B-A4B-it-NVFP4', text: '' },
    'proposals committed left to right while allowed and confident',
    'otherwise decode the first open position',
    'a backtrack returns committed positions to noise',
  ], fontSize: 13, gap: 5 });
  card(s, { x: LM + 2 * (cw + 0.3), y: TOP, w: cw, h: ch, head: 'Masked diffusion (ours)', headColor: C.accent3, body: [
    { lead: 'chandohasam 120M', text: '', leadColor: C.accent3 },
    'constraint on the positions being resolved; committed context preserved',
    '512-token canvas, meaning unmasked',
    'one token per akṣara; lines decoded left to right within the line',
  ], fontSize: 13, gap: 5 });
  const y2 = TOP + ch + 0.25;
  txt(s, 'Three decoding strategies (Algorithm 3)', { x: LM, y: y2, w: CW, h: 0.35, fontSize: 15, bold: true, color: C.accent3 });
  const sw = (CW - 0.6) / 3, sy = y2 + 0.42, sh = 6.85 - sy;
  const strat = [
    ['Masking only', 'Remove invalid tokens, renormalise, sample from the tokens that hold 90% of the mass (top-p).'],
    ['Masking + backtracking', 'Checkpoint every third step (keep 15). When stuck (< 3 allowed tokens, < 0.001 of the mass, or 4 steps without a new akṣara) rewind c checkpoints and raise τ by 0.15c, to at most 1.2.'],
    ['Hybrid', 'Walk the allowed tokens by probability (at most 100), collect those that complete the line (stop at 3), and sample among them.'],
  ];
  strat.forEach((st, i) => {
    const x = LM + i * (sw + 0.3);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: sy, w: sw, h: sh, fill: { color: C.background1 }, line: { color: C.accent3, width: 1 }, rectRadius: 0.1 });
    txt(s, st[0], { x: x + 0.2, y: sy + 0.1, w: sw - 0.4, h: 0.35, fontSize: 14, bold: true, color: C.accent3 });
    txt(s, st[1], { x: x + 0.2, y: sy + 0.45, w: sw - 0.4, h: sh - 0.55, fontSize: 12.5, color: C.text2 });
  });
}

// =====================================================================
// 15. RESULTS TABLE
// =====================================================================
pres.addSection({ title: 'Results' });
{
  const s = content('Results: the constrained-decoding grid', 'Results',
    'Paper §5 and Table 5. Every row uses the same grid: 37 metres × 3 topics × 5 seeds = 555 poems per model and decoding mode. A poem is in metre if it is complete and satisfies its canonical gaṇa, strict prāsa and strict yati with no sandhi assumed. Attested: words of two or more akṣaras found in held-out verse (topic words excluded); distinct: distinct attested words; single akṣara: share of words that are one akṣara; strong anuprāsa and obscure: the extreme bands of the poetics metrics; MAUVE against real verse of the same metre mix (120 a side, 5 seeds). Read the table row-pair by row-pair: free decoding never lands in metre; constrained decoding always does; and then look at what the constraint costs each model in words.');
  const r = (model, mode, v, bold) => [
    lcell(model, { bold: true }), lcell(mode, { color: mode === 'constrained' ? H.accent1 : H.dk2 }),
    cell(v[0], { bold: mode === 'constrained' }), cell(v[1], { bold: !!bold }), cell(v[2], { bold: !!bold }), cell(v[3]), cell(v[4]), cell(v[5]), cell(v[6]),
  ];
  const rows = [
    [hdr('model', { align: 'left' }), hdr('mode', { align: 'left' }), hdr('in metre'), hdr('attested'), hdr('distinct'), hdr('single akṣara'), hdr('strong anuprāsa'), hdr('obscure'), hdr('MAUVE')],
    r('Gemma-4 E4B', 'free', ['0', '33.7%', '490', '0.4%', '0.4%', '2.2%', '0.006']),
    r('', 'constrained', ['555', '10.7%', '323', '9.2%', '33.7%', '91.4%', '0.057']),
    r('Gemma-4 26B-A4B', 'free', ['0', '37.2%', '545', '2.0%', '9.9%', '0.9%', '0.009']),
    r('', 'constrained', ['555', '16.9%', '375', '16.1%', '48.1%', '91.0%', '0.014']),
    r('DiffusionGemma 26B-A4B', 'free', ['0', '34.4%', '485', '4.4%', '19.1%', '30.3%', '0.006']),
    r('', 'constrained', ['555', '11.5%', '333', '28.7%', '71.9%', '98.9%', '0.011']),
    r('Chandohasam 120M (ours)', 'free', ['0', '17.9%', '183', '5.9%', '26.7%', '45.9%', '0.006']),
    r('', 'constrained', ['555', '36.9%', '757', '19.7%', '33.7%', '62.9%', '0.035'], true),
    [lcell('real verse', { bold: true, fill: { color: H.lt2 } }), lcell('–', { fill: { color: H.lt2 } }), cell('–', { fill: { color: H.lt2 } }), cell('–', { fill: { color: H.lt2 } }), cell('–', { fill: { color: H.lt2 } }), cell('5.6%', { fill: { color: H.lt2 } }), cell('2.7%', { fill: { color: H.lt2 } }), cell('10.0%', { fill: { color: H.lt2 } }), cell('0.965', { fill: { color: H.lt2 }, bold: true })],
  ];
  s.addTable(rows, tableOpts({ x: LM, y: TOP, w: CW, colW: [2.7, 1.35, 1.0, 1.15, 1.05, 1.3, 1.45, 1.05, 1.08], fontSize: 12, rowH: 0.33 }));
  caption(s, 'Table 5 of the paper. Grid: 37 metres × 3 topics × 5 seeds = 555 poems per row. In metre = complete, canonical gaṇa, strict prāsa and strict yati, no sandhi assumed. Attested = words of two or more akṣaras found in held-out verse (topic words excluded). MAUVE against real verse of the same metre mix (n = 120 a side, 5 seeds).', { x: LM, y: TOP + 3.4, w: CW, h: 0.6 });
  const sw = (CW - 0.6) / 3, sy = TOP + 4.1, sh = 6.85 - sy;
  stat(s, { x: LM, y: sy, w: sw, h: sh, value: '0 → 555', label: 'poems in metre, free → constrained, for every model', size: 26, labelSize: 11.5 });
  stat(s, { x: LM + sw + 0.3, y: sy, w: sw, h: sh, value: '36.9%', label: 'attested words kept by Chandohasam 120M under constraint; subword models fall to 10.7–16.9%', size: 26, labelSize: 11.5 });
  stat(s, { x: LM + 2 * (sw + 0.3), y: sy, w: sw, h: sh, value: '0.035 vs 0.965', label: 'best MAUVE of a generated row vs real verse', size: 26, labelSize: 11.5 });
}

// =====================================================================
// 16. WHAT THE RESULTS SAY
// =====================================================================
{
  const s = content('Results: form is guaranteed, words are the cost', 'Results',
    'Paper §5. Finding 1: unconstrained, no model writes a poem in metre; constrained, all 555 are in metre for every model. Form is guaranteed by the decoder, not learned. Finding 2: for the subword Gemma models the guarantee has a lexical cost: attested words fall from 33.7–37.2% to 10.7–16.9%, 33.7–71.9% of the poems reach a strong anuprāsa that only 2.7% of real verse reaches, and 91.0–98.9% are rated obscure against 10.0% of real verse. Finding 3: Chandohasam 120M, whose tokens are single akṣaras, keeps 36.9% attested words under the same rules, about the subword models’ unconstrained level, with 757 distinct attested words, roughly twice their 323–375; its deficits reflect pretraining without verse: 19.7% single-akṣara words (real 5.6%) and 62.9% obscure. Finding 4: MAUVE confirms that no system yet writes like the corpus; the constraint raises it for every model, but every generated row stays between 0.006 and 0.057 against 0.965 for real verse. Finding 5: layer probes of the Gemma E2B and E4B variants and the recorded token-wise probabilities show that regardless of size all generations underperform equally, so parameter scaling does not have a significant effect on coherence.');
  const labels = ['Gemma E4B', 'Gemma 26B', 'DiffGemma 26B', 'Ours 120M'];
  s.addChart(pres.charts.BAR, [
    { name: 'free', labels, values: [33.7, 37.2, 34.4, 17.9] },
    { name: 'constrained', labels, values: [10.7, 16.9, 11.5, 36.9] },
  ], Object.assign({}, CHART_BASE, {
    x: LM, y: TOP, w: 6.6, h: 2.7, barDir: 'col', barGrouping: 'clustered', barGapWidthPct: 60,
    chartColors: [H.accent5, H.accent1], title: 'Attested words (%) by decoding mode',
    valAxisMinVal: 0, valAxisMaxVal: 50, valAxisMajorUnit: 10, dataLabelFormatCode: '0.0', showLegend: true, legendPos: 'r',
  }));
  s.addChart(pres.charts.BAR, [
    { name: 'free', labels, values: [2.2, 0.9, 30.3, 45.9] },
    { name: 'constrained', labels, values: [91.4, 91.0, 98.9, 62.9] },
  ], Object.assign({}, CHART_BASE, {
    x: LM, y: TOP + 2.8, w: 6.6, h: 2.7, barDir: 'col', barGrouping: 'clustered', barGapWidthPct: 60,
    chartColors: [H.accent5, H.accent1], title: 'Poems rated obscure (%); real verse: 10.0%',
    valAxisMinVal: 0, valAxisMaxVal: 100, valAxisMajorUnit: 25, dataLabelFormatCode: '0.0', showLegend: true, legendPos: 'r',
  }));
  const rx = LM + 6.9, rw = CW - 6.9;
  bullets(s, [
    { lead: 'Form by construction. ', text: 'Free decoding: 0 poems in metre; constrained: 555 of 555 for every model. The decoder guarantees form; nothing is learned.' },
    { lead: 'The lexical cost of subword tokens. ', text: 'Attested words fall from 33.7–37.2% to 10.7–16.9%; strong anuprāsa in 33.7–71.9% of poems (real verse 2.7%); 91.0–98.9% rated obscure (real 10.0%).' },
    { lead: 'Akṣara tokens keep the words. ', text: 'Chandohasam 120M keeps 36.9% attested words and 757 distinct ones, about twice the 323–375 of the subword models. Its deficits reflect pretraining without verse.' },
    { lead: 'No one writes like the corpus yet. ', text: 'MAUVE 0.006–0.057 for every generated row against 0.965 for real verse; the constraint raises it for every model.' },
    { lead: 'Scale does not buy coherence. ', text: 'Layer probes of Gemma E2B and E4B and the recorded token probabilities: all sizes underperform equally.' },
  ], { x: rx, y: TOP, w: rw, h: 5.5, fontSize: 13, gap: 7 });
}

// =====================================================================
// 17. PRETRAINING + AKṢARA TOKENIZER
// =====================================================================
pres.addSection({ title: 'Pretraining' });
{
  const s = content('Pretraining our own diffusion model, one token per akṣara', 'Pretraining',
    'Paper §4.4. Why an akṣara tokenizer: the controller reasons in akṣara weights, and an akṣara’s weight is settled by the next onset. A general subword tokenizer spends 1.2 to 1.4 tokens per akṣara (Table 2), so a token can hold part of an akṣara or several, and masking at that granularity is what strips the Gemma models of their vocabulary. We design a syllable-based tokenizer aware of akṣara boundaries: 45,591 tokens that cover 99.8% of the akṣara types in our verse, so the constraint acts on single syllables, the tokens themselves. The model, chandohasam 120M, is a 120M-parameter bidirectional transformer (12 layers, hidden size 768, rotary positions, SwiGLU) trained from scratch as a masked diffusion language model (MDLM, Sahoo et al., 2024). It saw 4.98B tokens of Telugu prose from Sangraha, IndicCorp v2 and Wikipedia on a single 8 GB laptop GPU in 2 days 19 hours. Generation fills a 512-token canvas in which the meaning is given unmasked, and the metre’s lines are decoded left to right within the line. The architecture figure comes from the project write-up and matches the paper’s description.');
  const lw = 6.3;
  card(s, { x: LM, y: TOP, w: lw, h: 2.45, head: 'Why the tokenizer must be akṣara-based', body: [
    'the constraint and the weights live on akṣaras, settled by the next onset',
    'subword tokenizers spend 1.2–1.4 tokens per akṣara: a token holds part of an akṣara, or several',
    'masking at subword granularity strips vocabulary: attested words fall to 10.7–16.9%',
    { lead: 'ours: ', text: '45,591 syllable tokens, akṣara-boundary aware, 99.8% of the akṣara types of our verse', leadColor: C.accent3 },
  ], fontSize: 13, gap: 4 });
  card(s, { x: LM, y: TOP + 2.65, w: lw, h: 2.75, head: 'chandohasam 120M: a masked diffusion language model', body: [
    { lead: 'architecture ', text: '120M-parameter bidirectional transformer: 12 layers, hidden 768, rotary positions, SwiGLU; MDLM (Sahoo et al., 2024), from scratch' },
    { lead: 'data ', text: '4.98B tokens of Telugu prose: Sangraha, IndicCorp v2, Wikipedia' },
    { lead: 'compute ', text: 'one 8 GB laptop GPU, 2 days 19 hours' },
    { lead: 'generation ', text: '512-token canvas, meaning given unmasked; lines decoded left to right within the line' },
  ], fontSize: 13, gap: 4 });
  const fh = 5.4, fw = fh * 1353 / 1138, fx = LM + lw + 0.3 + (CW - lw - 0.3 - fw) / 2;
  s.addImage({ path: path.join(FIG, 'fig_pilot120m_architecture.png'), x: fx, y: TOP, w: fw, h: fh });
}

// =====================================================================
// 18. PRETRAINING RESULTS
// =====================================================================
{
  const s = content('What pretraining bought us', 'Pretraining',
    'Paper §4.4 and the Chandohasam 120M rows of Table 5; the loss curve is from the project write-up and is NOT in the paper (validation NELBO fell from 2.921 at step 1k to 1.747 over 76,000 steps of 65,536 tokens; test NELBO 1.783 nats per token, weighted like the training mix). From the paper: the model trained on prose only, in 2 days 19 hours on an 8 GB GPU. Under the controller it keeps 36.9% attested words, up from 17.9% free, with 757 distinct attested words against 183, and MAUVE 0.035 against 0.006; both the opposite direction from the subword models, for which the constraint removed vocabulary. What it still lacks reflects pretraining without verse: 19.7% of its words are single akṣaras (real verse 5.6%) and 62.9% of its poems are rated obscure (real 10.0%), and MAUVE is still far from the 0.965 of real verse. Fine-tuning on the poetry corpus is the next step.');
  const fw = 6.6, fh = fw * 630 / 1200;
  s.addImage({ path: path.join(FIG, 'fig_pilot120m_loss.png'), x: LM, y: TOP, w: fw, h: fh });
  caption(s, 'Training loss and validation NELBO over 76,000 optimizer steps of 65,536 tokens (from the project write-up; not in the paper). Validation NELBO 2.921 → 1.747; test NELBO 1.783 nats per token.', { x: LM, y: TOP + fh + 0.05, w: fw, h: 0.6 });
  card(s, { x: LM, y: TOP + fh + 0.75, w: fw, h: 6.85 - (TOP + fh + 0.75), head: 'Trained on prose only', text: '4.98B tokens of Telugu prose; no verse in pretraining. The deficits on the right, single-akṣara words and obscurity, are what poetry fine-tuning must fix next.', fontSize: 13 });
  const rx = LM + fw + 0.3, rw = CW - fw - 0.3;
  txt(s, 'Chandohasam 120M, free → constrained (Table 5)', { x: rx, y: TOP, w: rw, h: 0.4, fontSize: 15, bold: true, color: C.accent3 });
  const sw = (rw - 0.2) / 2, sh = 1.55;
  const tiles = [
    ['17.9% → 36.9%', 'attested words: the constraint adds vocabulary instead of removing it'],
    ['183 → 757', 'distinct attested words; the subword models reach 323–375'],
    ['0.006 → 0.035', 'MAUVE against real verse of the same metre mix (real: 0.965)'],
    ['19.7% · 62.9%', 'single-akṣara words (real 5.6%) and obscure poems (real 10.0%): no verse in pretraining'],
  ];
  tiles.forEach((t, i) => {
    const x = rx + (i % 2) * (sw + 0.2), y = TOP + 0.5 + Math.floor(i / 2) * (sh + 0.2);
    stat(s, { x, y, w: sw, h: sh, value: t[0], label: t[1], size: 20, labelSize: 11.5, color: i === 3 ? C.accent2 : C.accent3 });
  });
  card(s, { x: rx, y: TOP + 0.5 + 2 * (sh + 0.2), w: rw, h: 6.85 - (TOP + 0.5 + 2 * (sh + 0.2)), head: 'Reading', text: 'One token per akṣara lets the constraint act on whole syllables, so masking removes options, not words. Form is free; what remains is to teach the model verse.', fontSize: 12.5, headSize: 15 });
}

// =====================================================================
// 19. WHY METRICS FOR POETRY
// =====================================================================
pres.addSection({ title: 'Evaluation' });
{
  const s = content('Why poetry needs its own metrics, for sound and for sense', 'Evaluation',
    'Paper §2 (evaluation side) and §4.6. On the sound side, metre identification is solved by the controller, but validity is binary; we also need graded measures of how far a poem is from a metre and of its sound qualities. On the meaning side nothing existed: for Sanskrit the only coherence measure was a human rating (2.1 to 2.7 of 5); MAUVE was built for human-versus-AI detection and is unvalidated on classical poetry; a training loss does not say whether a poem reads like Telugu. The classical treatise Kāvyālaṅkārasaṅgrahamu (16th c., Bhattumurthy) codifies the sound qualities: anuprāsa, mādhurya, ojas, prasāda and the śabdālaṅkāras, and its alpha-syllabary rules transfer from the Sanskrit identifiers. The suite separates hard structural validity from the semantic, stylistic and poetic qualities of a poem, and later becomes the reward for RLVR.');
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: LM, y: TOP, w: CW, h: 0.85, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, rectRadius: 0.1 });
  txt(s, 'A poem can pass the controller and still be noise. Validity is binary; quality needs graded, deterministic measures, and meaning needs a metric of its own.', { x: LM + 0.3, y: TOP, w: CW - 0.6, h: 0.85, fontSize: 16, color: C.background1, valign: 'middle' });
  const y2 = TOP + 1.1, cw = (CW - 0.3) / 2, ch = 6.85 - y2;
  card(s, { x: LM, y: y2, w: cw, h: ch, head: 'śabdaṃ: deterministic, from the treatise', body: [
    { lead: 'Source: ', text: 'Kāvyālaṅkārasaṅgrahamu (16th c., Bhattumurthy) codifies anuprāsa, mādhurya, ojas, prasāda and the śabdālaṅkāras' },
    { lead: 'caṃdomiti: ', text: 'a graded distance to the nearest valid metre, with yati and prāsa edits, where the controller only says yes or no' },
    { lead: 'śabdālaṅkāra identifiers: ', text: 'adapted from the Sanskrit yamaka and anuprāsa identifiers; Telugu’s alpha-syllabary allows it' },
    { lead: 'Real verse as the yardstick: ', text: 'only 2.7% strong anuprāsa, 10.0% obscure' },
  ], fontSize: 13, gap: 5 });
  card(s, { x: LM + cw + 0.3, y: y2, w: cw, h: ch, head: 'arthaṃ: the missing metric', headColor: C.accent3, body: [
    { lead: 'Nothing existed: ', text: 'Sanskrit systems fell back on human ratings (2.1–2.7 of 5); MAUVE is built for human-vs-AI detection and unvalidated on classical poetry', leadColor: C.accent3 },
    { lead: 'Semantic coherence: ', text: 'to be modelled on expert human acceptability judgements; it cannot be reduced to formal constraints, so it is evaluated apart from the controller', leadColor: C.accent3 },
    { lead: 'Word resolution: ', text: 'does each string resolve to a Telugu word through a macro-dictionary with sandhi and samāsa splitting?', leadColor: C.accent3 },
    { lead: 'arthālaṅkāras ', text: 'are outside the scope: inherently semantic, not deterministic', leadColor: C.accent3 },
  ], fontSize: 13, gap: 5 });
}

// =====================================================================
// 20. THE POETRY EVALUATION SUITE (four metrics)
// =====================================================================
{
  const s = content('The poetry evaluation suite: four sound qualities', 'Evaluation',
    'Paper Table 4. Anuprāsa (alliteration): A observed same-sound consonant pairs across different akṣaras within a line, E the expected pairs under corpus unigram frequencies, z = (A − E)/√V with V the chance variance; line levels at z = 1.645, 2.326 and 3.090; the poem score is the mean line level. Mādhurya (euphony): M = I − P, I the mean akṣara weight, P the mean harsh-akṣara run load; harsh below −0.283, leaning harsh to −0.123, balanced to 0.049, leaning soft to 0.156, soft above. Ojas (lexical density): O = (W + J)/2 with W = 100(1 − words/akṣaras) and J = 100 × conjunct-initial akṣaras / akṣaras; light below 39.3 up to dense at or above 47.5. Prasāda (clarity): H, the bits per akṣara of the sequence under a reference akṣara trigram model; clear below 5.12, leaning clear to 5.54, ordinary to 6.33, leaning obscure to 7.06, obscure above. Each quantifies a poetic property independently of metrical validity.');
  const cw = (CW - 0.3) / 2, ch = (6.85 - TOP - 0.25) / 2;
  const m = [
    ['anuprāsa · alliteration', 'Repeated consonant sounds across different akṣaras within a line.', 'z = (A − E) / √V', 'A observed same-sound pairs; E expected under corpus unigram frequencies; V chance variance', 'Line levels at z = 1.645, 2.326, 3.090; poem score = mean line level'],
    ['mādhurya · euphony', 'Phonetic softness: the balance of soft and harsh akṣaras and the accumulation of harsh ones.', 'M = I − P', 'I mean akṣara weight; P mean harsh-akṣara run load', 'harsh < −0.283 ≤ leaning harsh < −0.123 ≤ balanced < 0.049 ≤ leaning soft < 0.156 ≤ soft'],
    ['ojas · lexical density', 'Word and consonant clustering: word-bound akṣaras and conjunct-initial akṣaras.', 'O = (W + J) / 2', 'W = 100 (1 − words / akṣaras); J = 100 (conjunct-initial akṣaras / akṣaras)', 'light < 39.3; leaning light; moderate; leaning dense; dense ≥ 47.5'],
    ['prasāda · clarity', 'Predictability of the akṣara sequence under a reference akṣara trigram model.', 'H = −(1/N) Σ log₂ P(aₜ | aₜ₋₂, aₜ₋₁)', 'bits per akṣara', 'clear < 5.12 ≤ leaning clear < 5.54 ≤ ordinary < 6.33 ≤ leaning obscure < 7.06 ≤ obscure'],
  ];
  m.forEach((mm, i) => {
    const x = LM + (i % 2) * (cw + 0.3), y = TOP + Math.floor(i / 2) * (ch + 0.25);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cw, h: ch, fill: { color: C.background2 }, line: { color: C.background2, width: 0 }, rectRadius: 0.1 });
    txt(s, mm[0], { x: x + 0.22, y: y + 0.12, w: cw - 0.44, h: 0.38, fontSize: 16, bold: true, color: C.accent1 });
    txt(s, mm[2], { x: x + 0.22, y: y + 0.5, w: cw - 0.44, h: 0.4, fontSize: 15, bold: true, color: C.accent3, fontFace: THEME.headFontFace });
    txt(s, mm[1], { x: x + 0.22, y: y + 0.95, w: cw - 0.44, h: 0.5, fontSize: 12.5, color: C.text1 });
    txt(s, mm[3], { x: x + 0.22, y: y + 1.45, w: cw - 0.44, h: 0.5, fontSize: 12, color: C.text2, italic: true });
    txt(s, [{ text: 'Rubric: ', options: { bold: true, color: C.accent3 } }, { text: mm[4], options: {} }], { x: x + 0.22, y: y + 1.95, w: cw - 0.44, h: ch - 2.05, fontSize: 12, color: C.text1 });
  });
}

// =====================================================================
// 21. CAṂDOMITI
// =====================================================================
{
  const s = content('caṃdomiti: a graded distance to the nearest valid metre', 'Evaluation',
    'Paper Table 4 and Algorithm 4. Caṃdomiti, the chandas distance, is the minimum number of akṣara edits that make a poem conform to a specified metre, including weight, yati and prāsa constraints: D = Dw + Dy + Dp. Weight edits come from a dynamic programme over the slot’s own automaton: reading an akṣara along an edge costs 0 if the edge’s weight is one the akṣara may take, else 1 (substitution); skipping it costs 1 (deletion); following an edge without reading costs 1 (insertion); a pāda-final laghu may also read as U, and the path gives the nearest legal line. Lines are matched to the metre’s pādas with the fewest edits; a line left over costs its length, a pāda left empty its shortest line. Yati edits: one for each yati seat whose akṣara is not in maitri with the vaḷi. Prāsa edits: the fewest pādas to change so that all the pādas rhyme. An akṣara a weight edit already rewrites is counted once. The rate r = D / max(n, N) is chance-corrected per metre: S = 1 − r / r_chance(m), with r_chance the mean rate of prose cut to the line lengths of m. Rubric: exact (D = 0), slip, partial, weak, unmetered (r at or above the metre-specific chance cut).');
  const lw = 5.0;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: LM, y: TOP, w: lw, h: 2.3, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, rectRadius: 0.1 });
  txt(s, [
    { text: 'D = Dw + Dy + Dp', options: { breakLine: true, bold: true, fontSize: 26, fontFace: THEME.headFontFace } },
    { text: 'r = D / max(n, N)', options: { breakLine: true, fontSize: 18, fontFace: THEME.headFontFace } },
    { text: 'S = 1 − r / r_chance(m)', options: { fontSize: 18, fontFace: THEME.headFontFace } },
  ], { x: LM + 0.3, y: TOP + 0.15, w: lw - 0.6, h: 2.0, color: C.background1, valign: 'middle', align: 'center' });
  bullets(s, [
    { lead: 'Dw, Dy, Dp ', text: 'weight, yati and prāsa edits' },
    { lead: 'n, N ', text: 'akṣaras in the poem and in the nearest valid poem' },
    { lead: 'r_chance(m) ', text: 'mean edit rate of prose cut to the line lengths of metre m' },
    { lead: 'S ', text: '1 for a poem in metre, 0 for one no nearer to m than prose' },
  ], { x: LM, y: TOP + 2.5, w: lw, h: 1.7, fontSize: 13, gap: 4 });
  card(s, { x: LM, y: TOP + 4.25, w: lw, h: 6.85 - TOP - 4.25, head: 'Rubric', text: 'exact (D = 0) · slip · partial · weak · unmetered (r at or above the metre-specific chance cut)', fontSize: 13 });
  const rx = LM + lw + 0.35, rw = CW - lw - 0.35;
  txt(s, 'How the edits are counted (Algorithm 4)', { x: rx, y: TOP, w: rw, h: 0.35, fontSize: 15, bold: true, color: C.accent3 });
  const steps = [
    ['Weight edits, per line', 'A dynamic programme over the slot’s own automaton: reading an akṣara along an edge costs 0 if the edge’s weight is one it may take, else 1 (substitution); skipping it costs 1 (deletion); an edge without reading costs 1 (insertion). A pāda-final laghu may read as U. The path gives the nearest legal line.'],
    ['Match lines to pādas', 'Lines are matched to the metre’s pādas with the fewest edits; a line left over costs its length, a pāda left empty its shortest line.'],
    ['Yati edits', 'One for each yati seat whose akṣara is not in maitri with the vaḷi.'],
    ['Prāsa edits', 'The fewest pādas to change so that all the pādas rhyme. An akṣara a weight edit already rewrites is counted once.'],
  ];
  let y = TOP + 0.45;
  const hs = [1.3, 0.85, 0.65, 0.85];
  steps.forEach((st, i) => {
    numCircle(s, rx, y + 0.02, i + 1, C.accent3);
    txt(s, st[0], { x: rx + 0.62, y, w: rw - 0.62, h: 0.32, fontSize: 14, bold: true, color: C.text1 });
    txt(s, st[1], { x: rx + 0.62, y: y + 0.32, w: rw - 0.62, h: hs[i] - 0.32, fontSize: 12.5, color: C.text2 });
    y += hs[i] + 0.15;
  });
}

// =====================================================================
// 22. METRICS IN DESIGN
// =====================================================================
{
  const s = content('Metrics in design', 'Evaluation',
    'Paper §4.6 and §6. Four things are being built next on the evaluation side. A word resolution metric aligned with a compiled Telugu macro-dictionary resolves the lexicon of classical Telugu after sandhi and samāsa splitting, measuring word-level coherence across the poem; in the architecture it also acts as a lexical gate that rejects candidates with no valid segmentation. A semantic coherence metric modelled on expert human acceptability judgements on Telugu metrical poetry, validated against the ratings; it is evaluated apart from the controller because meaning cannot be reduced to formal constraints. Deterministic identifiers for the śabdālaṅkāras, adapted from the Sanskrit yamaka and anuprāsa identifiers. And a euphony index whose weights over sound euphony, alliteration and word density are learned. Arthālaṅkāras stay out of scope.');
  const cw = (CW - 0.3) / 2, ch = (6.85 - TOP - 0.25) / 2;
  const items = [
    ['Word resolution metric', ['align every string with a compiled Telugu macro-dictionary', 'sandhi and samāsa splitting, then word resolution', 'measures word-level coherence across the poem', 'doubles as a lexical gate: reject candidates with no valid segmentation']],
    ['Semantic coherence metric', ['modelled on expert human acceptability judgements of Telugu metrical poetry', 'validated against the human ratings on a frozen test split', 'cannot be reduced to formal constraints, so it is evaluated apart from the controller']],
    ['śabdālaṅkāra identifiers', ['deterministic identifiers for figures of sound', 'adapted from the Sanskrit yamaka and anuprāsa identifiers (Barbadikar and Kulkarni, 2023, 2024)', 'arthālaṅkāras (figures of sense) remain outside the scope']],
    ['Euphony index', ['one score combining sound euphony, alliteration and word density', 'its weights are learned against the human ratings', 'all of the above feed the RLVR reward']],
  ];
  items.forEach((it, i) => {
    const x = LM + (i % 2) * (cw + 0.3), y = TOP + Math.floor(i / 2) * (ch + 0.25);
    card(s, { x, y, w: cw, h: ch, num: i + 1, head: it[0], body: it[1], fontSize: 13, gap: 4, numColor: C.accent3, headColor: C.accent3 });
  });
}

// =====================================================================
// 23. FINAL ARCHITECTURE
// =====================================================================
pres.addSection({ title: 'Road ahead' });
{
  const s = content('The Chandohasam framework: diffusion, controller, rewards', 'Road ahead',
    'Paper Figure 2, §4 and §4.7. The generator is a masked diffusion language model whose canvas length is fixed a priori by the metre; it denoises from noise to a Telugu padyaṃ in akṣara tokens. Below it sits the deterministic metrical DAWG controller, which replaces the learned BERT metrical classifier of PoetryDiffusion: no loss terms, no gradients, an exact verdict with gaṇa, yati and prāsa predictions, plus the edit distance D. A lexical gate backed by the macro-dictionary resolves words after sandhi and samāsa splitting and rejects candidates with no valid segmentation. The sampled padyaṃ is scored by the poetics suite: anuprāsa, mādhurya, ojas, prasāda and caṃdomiti, combined as R = Σ λi ri together with the śabdālaṅkāra checks and the semantic coherence metric, and the policy is updated with RLVR. The DAWG stays active during RLVR generation, so metre, yati and prāsa remain hard constraints and RLVR optimises quality within the valid region. Each model is trained independently and its RLVR variant is compared against its base.');
  const fw = 9.7, fh = fw * 1330 / 3195;
  s.addImage({ path: path.join(FIG, 'fig_framework.png'), x: (W - fw) / 2, y: TOP - 0.1, w: fw, h: fh });
  const y2 = TOP - 0.1 + fh + 0.12, cw = (CW - 0.6) / 3, ch = 6.85 - y2;
  card(s, { x: LM, y: y2, w: cw, h: ch, head: 'Controller, not classifier', text: 'The DAWG replaces PoetryDiffusion’s learned BERT metrical classifier: no loss terms, no gradients; an exact 0/1 verdict plus the edit distance D.', fontSize: 12, headSize: 14 });
  card(s, { x: LM + cw + 0.3, y: y2, w: cw, h: ch, head: 'Lexical gate', text: 'A macro-dictionary resolves words after sandhi and samāsa splitting and rejects candidates with no valid segmentation.', fontSize: 12, headSize: 14 });
  card(s, { x: LM + 2 * (cw + 0.3), y: y2, w: cw, h: ch, head: 'RLVR: R = Σ λᵢ rᵢ', text: 'Poetics suite, śabdālaṅkāra checks and the coherence metric as verifiable rewards; the DAWG stays active, so RLVR optimises within the valid region.', fontSize: 12, headSize: 14 });
}

// =====================================================================
// 24. PROGRESS SO FAR
// =====================================================================
{
  const s = content('Progress so far', 'Road ahead',
    'Paper §6, first paragraph. Established: the dataset of 12,673 labelled poems with its sanity audit; the deterministic metrical controller over 37 metres, validated at 99.85% on the Bhāgavatamu; the poetry evaluation suite of five metrics operationalised from Kāvyālaṅkārasaṅgrahamu; baseline generations in free and constrained settings for four models, 555 poems per model and mode, with MAUVE against real verse; and our own 120M masked-diffusion model pretrained from scratch with an akṣara tokenizer. What remains centres on meaning: evaluating and improving semantic coherence, extending the metrics and modelling the coherence metric against human evaluations.');
  const tiles = [
    ['12,673', 'labelled poems in the benchmark, four sources, audited'],
    ['37', 'metres in one labelled DAWG; 370,315 legal lines'],
    ['99.85%', 'Bhāgavatamu poems identified with their labelled metre'],
    ['555 × 8', 'poems per model and mode, four models, free and constrained'],
    ['5', 'deterministic poetics metrics from Kāvyālaṅkārasaṅgrahamu'],
    ['120M', 'parameters, our masked-diffusion model on 4.98B Telugu tokens'],
  ];
  const tw = (CW - 0.6) / 3, th = 1.75;
  tiles.forEach((t, i) => {
    const x = LM + (i % 3) * (tw + 0.3), y = TOP + Math.floor(i / 3) * (th + 0.25);
    stat(s, { x, y, w: tw, h: th, value: t[0], label: t[1], size: 36, labelSize: 12.5 });
  });
  const y3 = TOP + 2 * (th + 0.25);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: LM, y: y3, w: CW, h: 6.85 - y3, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, rectRadius: 0.1 });
  txt(s, [
    { text: 'Form is solved by construction. ', options: { bold: true } },
    { text: 'What remains is meaning: evaluating and improving semantic coherence, extending the metrics, and modelling the coherence metric against human judgements.', options: {} },
  ], { x: LM + 0.3, y: y3, w: CW - 0.6, h: 6.85 - y3, fontSize: 15, color: C.background1, valign: 'middle' });
}

// =====================================================================
// 25. NEXT STEPS
// =====================================================================
{
  const s = content('Next steps and timeline', 'Road ahead',
    'Paper §6. Seven items. 1 Word resolution metric for word-level coherence inside a poem. 2 Human evaluation on generated and reference poems with the final rubric and a frozen test split. 3 Semantic coherence metric from the human acceptability judgements, validated against the ratings; in parallel, learn the weights of the euphony index. 4 Poetry fine-tuning of the diffusion model on the curated corpus, including the meaning-to-poem setting and ablations. 5 RLVR with the metrical constraints, the evaluation suite and the coherence metric as verifiable rewards, against rejection sampling and other constrained-generation baselines. 6 Final evaluation of all systems and the corpus with the automatic metrics, MAUVE and human evaluations, and an analysis of how automatic metrics relate to human judgements. 7 Final report and release of the controller, benchmark, evaluation suite and human ratings; final paper by 31 October 2026.');
  const steps = [
    ['Word resolution metric', 'word-level coherence inside a poem, via the macro-dictionary'],
    ['Human evaluation', 'generated and reference poems; final rubric, frozen test split'],
    ['Semantic coherence metric', 'from the human acceptability judgements, validated against them; learn the euphony-index weights'],
    ['Poetry fine-tuning', 'the diffusion model on the curated corpus; meaning-to-poem setting and ablations'],
    ['RLVR', 'metrical constraints, evaluation suite and coherence metric as verifiable rewards; rejection-sampling and constrained baselines'],
    ['Final evaluation', 'all systems and the corpus: automatic metrics, MAUVE, human evaluation; automatic vs. human analysis'],
    ['Final report and release', 'controller, benchmark, evaluation suite, human ratings'],
  ];
  const cw = (CW - 0.3) / 2, rh = 1.12;
  steps.forEach((st, i) => {
    const col = i < 4 ? 0 : 1, row = i < 4 ? i : i - 4;
    const x = LM + col * (cw + 0.3), y = TOP + row * (rh + 0.12);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cw, h: rh, fill: { color: C.background2 }, line: { color: C.background2, width: 0 }, rectRadius: 0.1 });
    numCircle(s, x + 0.2, y + (rh - 0.46) / 2, i + 1);
    txt(s, st[0], { x: x + 0.85, y: y + 0.1, w: cw - 1.0, h: 0.32, fontSize: 14.5, bold: true, color: C.accent1 });
    txt(s, st[1], { x: x + 0.85, y: y + 0.42, w: cw - 1.0, h: rh - 0.48, fontSize: 12, color: C.text2 });
  });
  const x = LM + cw + 0.3, y = TOP + 3 * (rh + 0.12);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cw, h: rh, fill: { color: C.accent3 }, line: { color: C.accent3, width: 0 }, rectRadius: 0.1 });
  txt(s, [{ text: 'Final paper: 31 October 2026', options: { bold: true, breakLine: true, fontSize: 18, fontFace: THEME.headFontFace } }, { text: 'consolidate the results and release the controller, benchmark, evaluation suite and human ratings', options: { fontSize: 12 } }], { x: x + 0.25, y, w: cw - 0.5, h: rh, color: C.background1, valign: 'middle' });
}

// =====================================================================
// 26. DEMONSTRATION
// =====================================================================
{
  const s = content('Demonstration: reading Pothana’s opening verse', 'Road ahead',
    'Live demo cue: run `python3 -m chandohasam --file ../presentation/demo_poem.txt` from meter_engine/ (the four pādas shown), and `python3 -m indic_meter_dawg prefix UUUI` for the narrowing query. The slide shows the tool’s actual output. The controller identifies śārdūlavikrīḍitamu, splits every pāda into ma sa ja sa ta ta ga, confirms yati at akṣara 13 in all four pādas (sound-class matches with the vaḷi: śrī–ciṃ, kṣai–saṃ, drē–ddṛ, nā–naṃ) and prāsa on the consonant క at the second akṣara of every pāda. Note the pāda-final laghu of line 1 read as guru. Then show the prefix query: with each weight the set of completable metres narrows, 28 → 14 → 7 → 4 → 3 → 1, which is exactly what the enforcer uses to mask tokens during generation.');
  const padas = [
    ['శ్రీ కై వ', 'ల్య ప దం', 'బుఁ జే రు', 'ట కు నై', 'చిం తిం చె', 'దన్ లో క', 'ర'],
    ['క్షై కా రం', 'భ కు భ', 'క్త పా ల', 'న క ళా', 'సం రం భ', 'కున్ దా న', 'వో'],
    ['ద్రే క స్తం', 'భ కుఁ గే', 'ళి లో ల', 'వి ల స', 'ద్దృ గ్జా ల', 'సం భూ త', 'నా'],
    ['నా కం జా', 'త భ వాం', 'డ కుం భ', 'కు మ హా', 'నం దాం గ', 'నా డిం భ', 'కున్'],
  ];
  const ganas = ['మ UUU', 'స IIU', 'జ IUI', 'స IIU', 'త UUI', 'త UUI', 'గ U'];
  const rows = [[hdr('pāda', { align: 'left' })].concat(ganas.map(g => hdr(g, { fontFace: TE })))];
  padas.forEach((p, i) => {
    rows.push([lcell(String(i + 1), { bold: true, color: H.accent1 })].concat(p.map((c, j) => cell(c, { fontFace: TE, fill: { color: j === 0 ? H.lt2 : H.lt1 } }))));
  });
  s.addTable(rows, tableOpts({ x: LM, y: TOP, w: CW, colW: [0.75, 1.75, 1.6, 1.6, 1.55, 1.85, 1.75, 1.28], fontSize: 13, rowH: 0.44 }));
  const y2 = TOP + 2.35;
  const cw = (CW - 0.6) / 3;
  card(s, { x: LM, y: y2, w: cw, h: 1.5, head: 'metre: śārdūlavikrīḍitamu ✓', body: ['ma sa ja sa ta ta ga, 19 akṣaras', 'pāda-final laghu of line 1 read as guru'], fontSize: 12.5, gap: 3, headSize: 14 });
  card(s, { x: LM + cw + 0.3, y: y2, w: cw, h: 1.5, head: 'yati 1 – 13 ✓ in every pāda', body: [{ text: 'శ్రీ–చిం · క్షై–సం · ద్రే–ద్దృ · నా–నం', options: { fontFace: TE } }, 'sound-class matches with the vaḷi'], fontSize: 12.5, gap: 3, headSize: 14 });
  card(s, { x: LM + 2 * (cw + 0.3), y: y2, w: cw, h: 1.5, head: 'prāsa on క ✓', body: [{ text: 'second akṣara of each pāda: కై · కా · క · కం', options: { fontFace: TE } }], fontSize: 12.5, gap: 3, headSize: 14 });
  const y3 = y2 + 1.7;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: LM, y: y3, w: CW, h: 6.85 - y3, fill: { color: C.text1 }, line: { color: C.text1, width: 0 }, rectRadius: 0.1 });
  txt(s, [
    { text: '$ python3 -m chandohasam --file poem.txt', options: { breakLine: true, color: C.accent2 } },
    { text: 'metre: శార్దూలవిక్రీడితము (sardulavikriditamu)   ప్రాస ✓   యతి ✓   profile strict', options: { breakLine: true, fontFace: TE } },
    { text: '$ python3 -m indic_meter_dawg prefix UUUI', options: { breakLine: true, color: C.accent2 } },
    { text: 'kandamu/even, kandamu/odd, madhuragati_ragada/all, sardulavikriditamu/all      (28 → 14 → 7 → 4 → 3 → 1 as the prefix grows)', options: {} },
  ], { x: LM + 0.3, y: y3 + 0.1, w: CW - 0.6, h: 6.85 - y3 - 0.2, fontSize: 12.5, fontFace: 'Courier New', color: C.background1, valign: 'middle' });
}

// =====================================================================
// 27. THANK YOU
// =====================================================================
{
  const s = pres.addSlide({ masterName: 'DARK', sectionTitle: 'Road ahead' });
  s.addText('Thank you', { placeholder: 'title' });
  s.addText([
    { text: 'Questions and discussion', options: { breakLine: true, bold: true, color: C.accent2 } },
    { text: 'samvaran.rallabandi · mahesh.emani · radheshyam.s  @research.iiit.ac.in', options: { breakLine: true } },
    { text: 'Chandohasam: a deterministic metrical controller, a curated benchmark, a poetry evaluation suite, and a diffusion model that writes one akṣara at a time.', options: { fontSize: 14, color: C.accent5 } },
  ], { placeholder: 'subtitle' });
  txt(s, 'U U U  I I U  I U I  I I U  U U I  U U I  U', { x: 0.8, y: 1.6, w: 11, h: 0.5, fontSize: 20, color: C.accent2, fontFace: THEME.headFontFace, charSpacing: 4 });
  s.addNotes('Closing. Invite questions; the demonstration can be re-run live from meter_engine/.');
  NOTES.push({ n: 99, title: 'Thank you', note: 'Closing. Invite questions. The demonstration can be re-run live from meter_engine/.' });
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  fs.writeFileSync(path.join(OUT_DIR, 'notes_data.json'), JSON.stringify(NOTES, null, 2));
  console.log('wrote', OUT, 'slides:', slideNo + 2);
})();

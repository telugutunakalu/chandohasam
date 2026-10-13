// DAWG walk-through: the metre DAWG of indic_meter_dawg in 3D, and one poem
// read through it akshara by akshara. All facts come from /api/dawg/graph and
// /api/dawg/trace (webapp/dawg_demo.py); this file only draws them.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

// ---------------------------------------------------------------------------
// constants
// ---------------------------------------------------------------------------
const C = {
  bg: 0x0b0d12,
  U: new THREE.Color(0xf5a524),
  I: new THREE.Color(0x5ea8ff),
  ok: new THREE.Color(0x4ade80),
  warn: new THREE.Color(0xfacc15),
  bad: new THREE.Color(0xf87171),
  white: new THREE.Color(0xffffff),
  focus: new THREE.Color(0xffe08a),
  family: {
    vrutta: new THREE.Color(0xa78bfa), jati: new THREE.Color(0x2dd4bf),
    upajati: new THREE.Color(0xf472b6), mixed: new THREE.Color(0x94a3b8),
  },
};
const FAMILY_CSS = { vrutta: 'var(--fam-vrutta)', jati: 'var(--fam-jati)', upajati: 'var(--fam-upajati)' };
const SEG = 6;                 // line segments per drawn edge
const STEP_MS = 900;           // one akshara at 1x
const RULES = {
  deergha: 'a long vowel (దీర్ఘము)',
  sandhyakshara: 'a diphthong ఐ / ఔ (సంధ్యక్షరము)',
  anusvara: 'an anusvāra ం (అనుస్వారము)',
  visarga: 'a visarga ః (విసర్గ)',
  pollu: 'closed by a pollu (పొల్లు)',
  samyukta: 'it stands before a conjunct (సంయుక్తాక్షర పూర్వము)',
  laghu: 'short and open (లఘువు)',
};
const VIKALPA = {
  word_initial_conjunct: 'the next word begins with a conjunct',
  repha_conjunct: 'the next akshara is a ర-vattu conjunct',
  'word_initial_conjunct+repha_conjunct': 'the next word begins with a ర-vattu conjunct',
};
const LEVELS = {
  canonical: 'the canonical scansion',
  vikalpa: 'the alternative readings (vikalpa) the scanner leaves open',
  compound: 'compound-boundary readings (a guru before a conjunct read as laghu)',
};

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fmt = (n) => Number(n).toLocaleString('en-US');
const W = (sym) => (sym === 'U' ? 'U' : '|');
const wspan = (sym) => `<span class="w-${sym}">${W(sym)}</span>`;
const easeInOut = (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);

// ---------------------------------------------------------------------------
// state
// ---------------------------------------------------------------------------
const boot = JSON.parse($('dg-data').textContent);
const S = {
  G: null,                    // graph payload
  traces: {},                 // version -> trace payload
  poem: boot.poem,
  version: boot.version === 'v2' ? 'v2' : 'v1',
  frames: [],
  frameOf: [],                // [unit][k] -> frame index
  idx: 0,
  playing: false,
  playTimer: null,
  speed: 1,
  follow: true,
  focusHyp: null,
};
const T = () => S.traces[S.version];

// ---------------------------------------------------------------------------
// three.js scene
// ---------------------------------------------------------------------------
const stage = $('dg-stage');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(stage.clientWidth, stage.clientHeight);
stage.appendChild(renderer.domElement);

const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(stage.clientWidth, stage.clientHeight);
Object.assign(labelRenderer.domElement.style, { position: 'absolute', top: '0', left: '0', pointerEvents: 'none' });
stage.appendChild(labelRenderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(C.bg);
scene.fog = new THREE.FogExp2(C.bg, 0.0058);

const camera = new THREE.PerspectiveCamera(48, stage.clientWidth / stage.clientHeight, 0.1, 3000);
camera.position.set(-30, 36, 98);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.maxDistance = 400;

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(stage.clientWidth, stage.clientHeight), 0.75, 0.45, 0.42);
composer.addPass(bloom);
composer.addPass(new OutputPass());

function glowTexture() {
  const c = document.createElement('canvas');
  c.width = c.height = 128;
  const g = c.getContext('2d');
  const grd = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  grd.addColorStop(0, 'rgba(255,255,255,1)');
  grd.addColorStop(0.25, 'rgba(255,255,255,0.55)');
  grd.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = grd;
  g.fillRect(0, 0, 128, 128);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}
const GLOW = glowTexture();

// graph objects (built once the graph arrives)
const G3 = {
  pos: [], out: [], curves: [], edgeKey: new Map(), nodeMesh: null, edgeLines: null,
  nodeBase: null, nodeCur: null, nodeTgt: null, edgeCur: null, edgeTgt: null, colorsDirty: false,
  maxR: 0, ribbonY: -18, tubeCache: new Map(), unitTrails: new Map(),
};
const trailGroup = new THREE.Group();
const haloGroup = new THREE.Group();
const tokenGroup = new THREE.Group();
const ribbonGroup = new THREE.Group();
const labelGroup = new THREE.Group();
scene.add(trailGroup, haloGroup, tokenGroup, ribbonGroup, labelGroup);

const MAT = {
  trailU: new THREE.MeshBasicMaterial({ color: C.U.clone().multiplyScalar(1.6) }),
  trailI: new THREE.MeshBasicMaterial({ color: C.I.clone().multiplyScalar(1.6) }),
  faintU: new THREE.MeshBasicMaterial({ color: C.U, transparent: true, opacity: 0.32, depthWrite: false }),
  faintI: new THREE.MeshBasicMaterial({ color: C.I, transparent: true, opacity: 0.32, depthWrite: false }),
  padanta: new THREE.MeshBasicMaterial({ color: C.ok.clone().multiplyScalar(1.4), transparent: true, opacity: 0.85 }),
  token: new THREE.MeshBasicMaterial({ color: 0xffffff }),
  s2: new THREE.MeshBasicMaterial({ color: C.ok.clone().multiplyScalar(1.3) }),
  s1: new THREE.MeshBasicMaterial({ color: C.warn.clone().multiplyScalar(1.2) }),
  s0: new THREE.MeshBasicMaterial({ color: C.bad.clone().multiplyScalar(1.3) }),
  root: new THREE.MeshBasicMaterial({ color: 0x8f98ab }),
};
const SPHERE = new THREE.SphereGeometry(1, 16, 12);
const SMALL = new THREE.SphereGeometry(1, 10, 8);

function edgeCurve(a, b, sym) {
  const mid = a.clone().add(b).multiplyScalar(0.5);
  const radial = new THREE.Vector3(0, mid.y, mid.z);
  const r = radial.length();
  if (r < 1e-3) radial.set(0, 1, 0); else radial.divideScalar(r);
  const perp = new THREE.Vector3(0, -radial.z, radial.y);        // around the walking axis
  const d = a.distanceTo(b);
  const ctrl = mid.add(radial.multiplyScalar(0.16 * d)).add(perp.multiplyScalar((sym === 'U' ? 0.05 : -0.05) * d));
  return new THREE.QuadraticBezierCurve3(a.clone(), ctrl, b.clone());
}

function buildGraph(G) {
  const N = G.nodes.length;
  G3.pos = G.nodes.map((n) => new THREE.Vector3(n.x, n.y, n.z));
  G3.out = Array.from({ length: N }, () => []);
  G3.maxR = Math.max(...G.nodes.map((n) => Math.hypot(n.y, n.z)));
  G3.ribbonY = -(G3.maxR + 7);
  G.edges.forEach(([s, sym, d], e) => {
    G3.out[s].push(e);
    G3.edgeKey.set(`${s}|${sym}|${d}`, e);
    G3.curves[e] = edgeCurve(G3.pos[s], G3.pos[d], sym);
  });

  // nodes
  G3.nodeBase = G.nodes.map((n) => C.family[n.family] || C.family.mixed);
  G3.nodeCur = new Float32Array(N * 3);
  G3.nodeTgt = new Float32Array(N * 3);
  const mesh = new THREE.InstancedMesh(SPHERE, new THREE.MeshBasicMaterial({ color: 0xffffff }), N);
  for (let i = 0; i < N; i++) {
    mesh.setColorAt(i, G3.nodeBase[i]);
    G3.nodeBase[i].toArray(G3.nodeCur, i * 3);
  }
  G3.nodeMesh = mesh;
  setNodeScales(new Set());
  scene.add(mesh);

  // edges: SEG segments along each curve
  const E = G.edges.length;
  const pos = new Float32Array(E * SEG * 2 * 3);
  const col = new Float32Array(E * SEG * 2 * 3);
  G3.edgeCur = new Float32Array(E * 3);
  G3.edgeTgt = new Float32Array(E * 3);
  let o = 0;
  G.edges.forEach(([, sym], e) => {
    const pts = G3.curves[e].getPoints(SEG);
    for (let j = 0; j < SEG; j++) {
      pts[j].toArray(pos, o); pts[j + 1].toArray(pos, o + 3); o += 6;
    }
    (sym === 'U' ? C.U : C.I).clone().multiplyScalar(0.3).toArray(G3.edgeCur, e * 3);
  });
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
  G3.edgeLines = new THREE.LineSegments(geo, new THREE.LineBasicMaterial({
    vertexColors: true, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false,
  }));
  scene.add(G3.edgeLines);
  writeColors(1);

  // the START label never moves
  const st = label(`<span class="lbl-start">START</span>`, 'lbl lbl-start');
  st.position.copy(G3.pos[G.start]).add(new THREE.Vector3(0, 1.2, 0));
  scene.add(st);
}

function setNodeScales(big, cone = null) {
  const m = new THREE.Matrix4();
  const G = S.G;
  for (let i = 0; i < G.nodes.length; i++) {
    let s = G.nodes[i].accept.length ? 0.24 : 0.16;
    if (i === G.start) s = 0.55;
    if (big.has(i)) s *= i === G.start ? 1.2 : 2.0;
    else if (cone !== null && !cone.has(i)) s *= 0.55;      // states the walk can no longer reach
    m.makeScale(s, s, s).setPosition(G3.pos[i]);
    G3.nodeMesh.setMatrixAt(i, m);
  }
  G3.nodeMesh.instanceMatrix.needsUpdate = true;
}

// colour targets are eased toward every frame
function writeColors(alpha) {
  const { nodeCur, nodeTgt, edgeCur, edgeTgt } = G3;
  let moving = false;
  for (let i = 0; i < nodeCur.length; i++) {
    const d = nodeTgt[i] - nodeCur[i];
    if (Math.abs(d) > 0.002) { nodeCur[i] += d * alpha; moving = true; } else nodeCur[i] = nodeTgt[i];
  }
  for (let i = 0; i < edgeCur.length; i++) {
    const d = edgeTgt[i] - edgeCur[i];
    if (Math.abs(d) > 0.002) { edgeCur[i] += d * alpha; moving = true; } else edgeCur[i] = edgeTgt[i];
  }
  const ic = G3.nodeMesh.instanceColor.array;
  ic.set(nodeCur);
  G3.nodeMesh.instanceColor.needsUpdate = true;
  const col = G3.edgeLines.geometry.attributes.color.array;
  const E = edgeCur.length / 3;
  for (let e = 0; e < E; e++) {
    const r = edgeCur[e * 3], g = edgeCur[e * 3 + 1], b = edgeCur[e * 3 + 2];
    for (let v = 0, o = e * SEG * 6; v < SEG * 2; v++, o += 3) { col[o] = r; col[o + 1] = g; col[o + 2] = b; }
  }
  G3.edgeLines.geometry.attributes.color.needsUpdate = true;
  G3.colorsDirty = moving;
}

function tubeGeo(e) {
  if (!G3.tubeCache.has(e)) G3.tubeCache.set(e, new THREE.TubeGeometry(G3.curves[e], 20, 0.085, 6, false));
  return G3.tubeCache.get(e);
}

function label(html, cls) {
  const div = document.createElement('div');
  div.className = cls;
  div.innerHTML = html;
  return new CSS2DObject(div);
}

function clearGroup(g) {
  while (g.children.length) {
    const c = g.children[g.children.length - 1];
    g.remove(c);
    if (c.userData.disposeGeometry) c.geometry.dispose();
  }
}

function halo(p, color, size = 2.6) {
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({
    map: GLOW, color, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  }));
  sp.position.copy(p);
  sp.scale.setScalar(size);
  sp.userData.base = size;
  haloGroup.add(sp);
  return sp;
}

// ---------------------------------------------------------------------------
// frames
// ---------------------------------------------------------------------------
function buildFrames() {
  const t = T();
  S.frames = [{ type: 'intro' }];
  S.frameOf = [];
  t.units.forEach((u, ui) => {
    S.frameOf[ui] = [S.frames.length];
    S.frames.push({ type: 'start', u: ui, k: 0 });
    u.steps.forEach((_, j) => { S.frameOf[ui][j + 1] = S.frames.length; S.frames.push({ type: 'step', u: ui, k: j + 1 }); });
    S.frames.push({ type: 'end', u: ui, k: u.steps.length });
  });
  S.frames.push({ type: 'stanza' });
  $('dg-scrub').max = String(S.frames.length - 1);
}

function edgesOf(list) {
  return list.map(([s, sym, d]) => G3.edgeKey.get(`${s}|${sym}|${d}`)).filter((e) => e !== undefined);
}

function coneFrom(frontier) {
  const seen = new Set(frontier);
  const q = [...frontier];
  while (q.length) {
    const s = q.pop();
    for (const e of G3.out[s]) {
      const d = S.G.edges[e][2];
      if (!seen.has(d)) { seen.add(d); q.push(d); }
    }
  }
  return seen;
}

function centroid(ids) {
  const c = new THREE.Vector3();
  ids.forEach((i) => c.add(G3.pos[i]));
  return ids.length ? c.multiplyScalar(1 / ids.length) : c;
}

// what the scene shows in a frame, derived from the trace
function sceneState(f) {
  const t = T();
  const G = S.G;
  const all = null;                     // null cone = every state
  if (f.type === 'intro') return { frontier: [], cone: all, trail: [], faint: [], intro: true };
  if (f.type === 'stanza') {
    const trail = t.units.flatMap((u) => u.steps.flatMap((st) => edgesOf(st.edges)));
    const pad = t.units.flatMap((u) => (u.padanta && u.padanta.accepted.length ? edgesOf(u.padanta.edges) : []));
    const acc = [...new Set(t.units.flatMap((u) => [...u.accept_states, ...(u.padanta?.states || [])]))];
    const cone = new Set([G.start, ...trail.map((e) => G.edges[e][2]), ...trail.map((e) => G.edges[e][0])]);
    return { frontier: acc, cone, trail, pad, faint: [], accept: acc, stanza: true };
  }
  const u = t.units[f.u];
  const faint = t.units.slice(0, f.u).flatMap((v) => v.steps.flatMap((st) => edgesOf(st.edges)));
  if (f.type === 'start') return { frontier: [G.start], cone: all, trail: [], faint };
  const steps = u.steps.slice(0, f.k);
  const trail = steps.flatMap((st) => edgesOf(st.edges));
  if (f.type === 'step') {
    const st = u.steps[f.k - 1];
    const prev = f.k > 1 ? u.steps[f.k - 2].frontier : [G.start];
    if (!st.frontier.length) return { frontier: [], cone: new Set(), trail, faint, dead: prev, newEdges: [] };
    return { frontier: st.frontier, cone: coneFrom(st.frontier), trail, faint, newEdges: edgesOf(st.edges), prev };
  }
  // end of a pāda
  const pad = u.padanta && u.padanta.accepted.length ? edgesOf(u.padanta.edges) : [];
  const acc = [...u.accept_states, ...(pad.length ? u.padanta.states : [])];
  const last = u.steps.length ? u.steps[u.steps.length - 1].frontier : [G.start];
  const prevLast = u.steps.length > 1 ? u.steps[u.steps.length - 2].frontier : [G.start];
  return {
    frontier: acc, cone: new Set(acc), trail, faint, pad, accept: acc,
    dead: acc.length ? null : (last.length ? last : prevLast),
  };
}

// ---------------------------------------------------------------------------
// applying a frame to the scene
// ---------------------------------------------------------------------------
let anim = null;               // the running step animation

function applyScene(f, animate) {
  const G = S.G;
  const ss = sceneState(f);
  if (anim) finishAnim();

  // colours
  const front = new Set(ss.frontier);
  const visited = new Set(ss.trail.flatMap((e) => [G.edges[e][0], G.edges[e][2]]));
  const focus = S.focusHyp;
  const tmp = new THREE.Color();
  G.nodes.forEach((n, i) => {
    const base = G3.nodeBase[i];
    if (ss.intro) tmp.copy(base).multiplyScalar(0.85);
    else if (front.has(i)) tmp.copy(ss.accept ? C.ok : C.white);
    else if (visited.has(i)) tmp.copy(base).lerp(C.white, 0.45);
    else if (ss.cone === null || ss.cone.has(i)) {
      if (focus !== null) tmp.copy(n.reach.includes(focus) ? C.focus : base).multiplyScalar(n.reach.includes(focus) ? 1 : 0.18);
      else tmp.copy(base).multiplyScalar(0.8);
    } else tmp.copy(base).multiplyScalar(0.07);
    tmp.toArray(G3.nodeTgt, i * 3);
  });
  G.edges.forEach(([s, sym, d], e) => {
    const inCone = ss.cone === null || (ss.cone.has(s) && ss.cone.has(d));
    let k = ss.intro ? 0.3 : inCone ? 0.34 : 0.03;
    if (!ss.intro && focus !== null && inCone && !(G.nodes[s].reach.includes(focus) && G.nodes[d].reach.includes(focus))) k = 0.05;
    tmp.copy(sym === 'U' ? C.U : C.I).multiplyScalar(k).toArray(G3.edgeTgt, e * 3);
  });
  G3.colorsDirty = true;
  setNodeScales(front, ss.intro ? null : new Set([...(ss.cone ?? G.nodes.map((n) => n.id)), ...visited]));

  // trails
  clearGroup(trailGroup);
  const fresh = new Set(animate && ss.newEdges ? ss.newEdges : []);
  const addTube = (e, mat) => {
    const m = new THREE.Mesh(tubeGeo(e), mat);
    trailGroup.add(m);
    return m;
  };
  ss.faint.forEach((e) => addTube(e, G.edges[e][1] === 'U' ? MAT.faintU : MAT.faintI));
  ss.trail.forEach((e) => { if (!fresh.has(e)) addTube(e, G.edges[e][1] === 'U' ? MAT.trailU : MAT.trailI); });
  (ss.pad || []).forEach((e) => addTube(e, MAT.padanta));

  // halos and labels
  clearGroup(haloGroup);
  clearGroup(labelGroup);
  ss.frontier.forEach((i) => halo(G3.pos[i], ss.accept ? C.ok : C.white, i === G.start ? 1.8 : ss.accept ? 3.2 : 2.6));
  if (ss.dead) ss.dead.forEach((i) => halo(G3.pos[i], C.bad, 3.4));
  sceneLabels(f, ss);

  // the Layer B lane (v2)
  buildRibbon(f, ss, animate);

  // camera
  aimCamera(f, ss);

  if (animate && ss.newEdges && ss.newEdges.length) startStepAnim(f, ss, fresh);
}

function sceneLabels(f, ss) {
  const t = T();
  const G = S.G;
  const hyps = G.hypotheses;
  const add = (html, cls, p, dy = 1.1) => {
    const l = label(html, cls);
    l.position.copy(p).add(new THREE.Vector3(0, dy, 0));
    labelGroup.add(l);
  };
  if (f.type === 'step') {
    const u = t.units[f.u];
    const st = u.steps[f.k - 1];
    const a = u.aksharas[f.k - 1];
    const gate = t.version === 'v2' ? (u.v2[f.k - 1].inventory ? ' <span style="color:var(--ok)">A✓</span>' : ' <span style="color:var(--bad)">A✗</span>') : '';
    const w = a.options.length > 1 ? `${wspan(a.options[0])}/${wspan(a.options[1])}` : wspan(a.options);
    if (st.frontier.length) add(`<span class="te">${esc(a.text)}</span> ${w}${gate}`, 'lbl lbl-cur', G3.pos[st.frontier[0]]);
    else if (ss.dead) add(`✗ no edge for <span class="te">${esc(a.text)}</span> ${w}`, 'lbl lbl-dead', G3.pos[ss.dead[0]]);
  }
  if (f.type === 'end' || f.type === 'stanza') {
    const units = f.type === 'end' ? [t.units[f.u]] : t.units;
    const at = new Map();          // accept state -> lines
    units.forEach((u) => {
      [...u.accept_states, ...(u.padanta && u.padanta.accepted.length ? u.padanta.states : [])].forEach((s) => {
        if (!at.has(s)) at.set(s, []);
        at.get(s).push(u);
      });
    });
    at.forEach((us, s) => {
      if (f.type === 'end') {
        const u = us[0];
        const ids = [...u.accepted, ...(u.padanta?.accepted || [])];
        const names = ids.filter((h) => S.G.nodes[s].accept.includes(h)).map((h) => hypName(hyps[h])).join(', ');
        add(`✓ ${names}`, 'lbl lbl-acc', G3.pos[s]);
      } else {
        add(`✓ పాదం ${us.map((u) => u.unit).join(', ')}`, 'lbl lbl-acc', G3.pos[s]);
      }
    });
    if (f.type === 'end' && ss.dead) add('✗ no metre accepts this pāda', 'lbl lbl-dead', G3.pos[ss.dead[0]]);
  }
}

// ---------------------------------------------------------------------------
// Layer B lane: the word DAWG walk under the metre DAWG (v2)
// ---------------------------------------------------------------------------
function unitXs(u) {
  const G = S.G;
  const xs = [G3.pos[G.start].x];
  u.aksharas.forEach((_, j) => {
    const st = u.steps[j];
    xs.push(st && st.frontier.length ? centroid(st.frontier).x : xs[xs.length - 1] + 2.6);
  });
  return xs;
}

function buildRibbon(f, ss, animate) {
  clearGroup(ribbonGroup);
  const t = T();
  if (t.version !== 'v2' || !(f.type === 'step' || f.type === 'end' || f.type === 'start')) return;
  const u = t.units[f.u];
  const kShow = f.type === 'start' ? 0 : f.k;
  const y = G3.ribbonY;
  const xs = unitXs(u);
  const lane = label('Layer B · word DAWG over the corpus words', 'lbl lbl-lane');
  lane.position.set(xs[0] - 1, y + 1.6, 0);
  ribbonGroup.add(lane);
  const linePts = [];
  const fanPts = [];
  const bindPts = [];
  let prev = null;
  const appear = [];
  for (let k = 1; k <= kShow; k++) {
    const v = u.v2[k - 1];
    const x0 = xs[k - 1], x1 = xs[k];
    const isNew = animate && f.type === 'step' && k === kShow;
    if (v.word_start) {
      const root = new THREE.Mesh(SMALL, MAT.root);
      root.position.set(x0 + 0.25, y, 0);
      root.scale.setScalar(0.13);
      ribbonGroup.add(root);
      prev = root.position.clone();
    }
    v.chars.forEach((c, j) => {
      const p = new THREE.Vector3(x0 + ((j + 1) / v.chars.length) * (x1 - x0), y, 0);
      const m = new THREE.Mesh(SMALL, MAT['s' + c.score]);
      m.position.copy(p);
      m.scale.setScalar(0.17);
      ribbonGroup.add(m);
      if (isNew) appear.push({ m, at: j / v.chars.length });
      if (prev) linePts.push(prev.clone(), p.clone());
      const n = Math.min(c.out, 14);
      for (let q = 0; q < n; q++) {
        const ang = (q / Math.max(n - 1, 1) - 0.5) * 1.6;
        fanPts.push(p.clone(), p.clone().add(new THREE.Vector3(0.35, -0.8 * Math.cos(ang), 0.8 * Math.sin(ang))));
      }
      prev = p;
    });
    const st = u.steps[k - 1];
    if (st && st.frontier.length) bindPts.push(prev.clone(), G3.pos[st.frontier[0]].clone());
    if (v.ends_word) {
      const fin = v.finished;
      const cls = fin === null ? 'na' : fin ? 'ok' : 'bad';
      const txt = fin === null ? 'single akshara' : fin ? '✓ real word' : '✗ not a corpus word';
      const l = label(`<span class="te">${esc(v.word)}</span> ${txt}`, `lbl lbl-word ${cls}`);
      l.position.copy(prev).add(new THREE.Vector3(0, -1.1, 0));
      ribbonGroup.add(l);
      prev = null;
    }
  }
  const seg = (pts, color, opacity) => {
    if (!pts.length) return;
    const g = new THREE.BufferGeometry().setFromPoints(pts);
    const l = new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color, transparent: true, opacity, depthWrite: false }));
    l.userData.disposeGeometry = true;
    ribbonGroup.add(l);
  };
  seg(linePts, 0xcfd4de, 0.8);
  seg(fanPts, 0x8f98ab, 0.22);
  seg(bindPts, 0xa78bfa, 0.28);

  // Layer A gate at the walker
  if (f.type === 'step' && ss.frontier.length) {
    const ok = u.v2[f.k - 1].inventory;
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.85, 0.06, 8, 40),
      new THREE.MeshBasicMaterial({ color: (ok ? C.ok : C.bad).clone().multiplyScalar(1.4), transparent: true, opacity: 0.9 }));
    ring.rotation.y = Math.PI / 2;
    ring.position.copy(G3.pos[ss.frontier[0]]);
    ring.userData.disposeGeometry = true;
    ring.userData.gate = true;
    ribbonGroup.add(ring);
    if (animate) appear.push({ m: ring, at: 0.55, gate: true });
  }
  appear.forEach((a) => { a.m.userData.finalScale = a.m.scale.x; a.m.scale.setScalar(0.0001); });
  ribbonGroup.userData.appear = appear;
}

// ---------------------------------------------------------------------------
// animation: tokens slide along the edges of one step
// ---------------------------------------------------------------------------
function startStepAnim(f, ss, fresh) {
  clearGroup(tokenGroup);
  const tokens = [...fresh].map((e) => {
    const m = new THREE.Mesh(SPHERE, MAT.token);
    m.scale.setScalar(0.3);
    const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW, color: S.G.edges[e][1] === 'U' ? C.U : C.I, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
    glow.scale.setScalar(8);
    m.add(glow);
    tokenGroup.add(m);
    const grow = new THREE.Mesh(new THREE.TubeGeometry(G3.curves[e], 20, 0.085, 6, false),
      S.G.edges[e][1] === 'U' ? MAT.trailU : MAT.trailI);
    grow.userData.disposeGeometry = true;
    grow.geometry.setDrawRange(0, 0);
    trailGroup.add(grow);
    return { m, e, grow };
  });
  haloGroup.visible = false;
  labelGroup.visible = false;
  anim = { t0: performance.now(), dur: STEP_MS / S.speed, tokens };
}

function tickAnim(now) {
  if (!anim) return;
  const t = Math.min(1, (now - anim.t0) / anim.dur);
  const k = easeInOut(t);
  anim.tokens.forEach(({ m, e, grow }) => {
    m.position.copy(G3.curves[e].getPoint(k));
    const idx = grow.geometry.index.count;
    grow.geometry.setDrawRange(0, Math.floor((idx / 6) * k) * 6);
  });
  (ribbonGroup.userData.appear || []).forEach((a) => {
    const p = Math.max(0, Math.min(1, (t - a.at * 0.7) / 0.3));
    const s = a.gate ? a.m.userData.finalScale * (1 + 0.8 * (1 - p)) : a.m.userData.finalScale * p;
    a.m.scale.setScalar(Math.max(s, 0.0001));
    if (a.gate) a.m.material.opacity = 0.9 * p;
  });
  if (t >= 1) finishAnim();
}

function finishAnim() {
  if (!anim) return;
  anim.tokens.forEach(({ grow }) => grow.geometry.setDrawRange(0, Infinity));
  clearGroup(tokenGroup);
  (ribbonGroup.userData.appear || []).forEach((a) => {
    a.m.scale.setScalar(a.gate ? a.m.userData.finalScale : a.m.userData.finalScale);
    if (a.gate) a.m.material.opacity = 0.9;
  });
  ribbonGroup.userData.appear = [];
  haloGroup.visible = true;
  labelGroup.visible = true;
  anim = null;
  if (S.playing) schedulePlay();
}

// ---------------------------------------------------------------------------
// camera
// ---------------------------------------------------------------------------
let fly = null;
let followTarget = null;

function flyTo(target, position, dur = 1300) {
  fly = { t0: performance.now(), dur: dur / Math.max(S.speed, 1), fromT: controls.target.clone(), fromP: camera.position.clone(), toT: target, toP: position };
  followTarget = null;
}

// far enough back that the whole spindle fits the space between the panels
function overviewShot() {
  const target = new THREE.Vector3(0, 0, 0);
  const tanH = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * (G3.freeW || stage.clientWidth) / stage.clientHeight;
  const halfLen = (S.G.layers * 2.6) / 2 + 6;
  const dist = THREE.MathUtils.clamp((0.76 * halfLen) / tanH, 80, 320);
  return [target, target.clone().add(new THREE.Vector3(-0.27, 0.32, 0.91).normalize().multiplyScalar(dist))];
}

function aimCamera(f, ss) {
  const v2 = T().version === 'v2';
  const lift = v2 ? G3.ribbonY / 2 : 0;
  if (f.type === 'intro' || f.type === 'stanza') {
    const [t, p] = overviewShot();
    flyTo(t, p);
    return;
  }
  if (!S.follow) return;
  if (f.type === 'start') {
    const target = G3.pos[S.G.start].clone().add(new THREE.Vector3(7, lift, 0));
    flyTo(target, target.clone().add(new THREE.Vector3(-7, v2 ? 7 : 10, v2 ? 46 : 26)));
    return;
  }
  const ids = ss.frontier.length ? ss.frontier : ss.dead || [];
  if (!ids.length) return;
  const c = centroid(ids);
  followTarget = new THREE.Vector3(c.x + 3, (c.y + (v2 ? G3.ribbonY : c.y)) / 2, c.z * (v2 ? 0.5 : 1));
}

function tickCamera(now, dt) {
  if (fly) {
    const t = Math.min(1, (now - fly.t0) / fly.dur);
    const k = easeInOut(t);
    controls.target.lerpVectors(fly.fromT, fly.toT, k);
    camera.position.lerpVectors(fly.fromP, fly.toP, k);
    if (t >= 1) fly = null;
  } else if (followTarget && S.follow) {
    const delta = followTarget.clone().sub(controls.target).multiplyScalar(1 - Math.exp(-dt * 2.6));
    controls.target.add(delta);
    camera.position.add(delta);
    if (delta.lengthSq() < 1e-6) followTarget = null;
  }
}

// ---------------------------------------------------------------------------
// panels
// ---------------------------------------------------------------------------
function hypName(h, withSlot = true) {
  return `<span class="te">${esc(h.name_te.replace(/_/g, ' '))}</span>${withSlot && h.n_slots > 1 ? ` <span class="slot">${esc(h.slot)}</span>` : ''}`;
}
function hypPlain(h) { return h.name_te.replace(/_/g, ' ') + (h.n_slots > 1 ? ` (${h.slot})` : ''); }

function listNames(ids, max = 4) {
  const hs = ids.map((i) => S.G.hypotheses[i]);
  const shown = hs.slice(0, max).map((h) => hypName(h)).join(', ');
  return hs.length > max ? `${shown} and ${hs.length - max} more` : shown;
}

function fmtPos(list) {
  if (!list || !list.length) return '';
  const p = list[0];
  let s;
  if (p.done) s = `<b>complete</b> · ${p.ganas} gaṇas read`;
  else if (p.read === 0) s = `gaṇa ${p.gana}/${p.of} · next <span class="te">${p.next.slice(0, 5).map(esc).join(' ')}</span>${p.next.length > 5 ? ' …' : ''}`;
  else {
    const pat = [...p.pattern].map((c, i) => (i < p.read ? `<b>${W(c)}</b>` : W(c))).join('');
    s = `gaṇa ${p.gana}/${p.of} · <span class="te">${esc(p.te)}</span> ${pat} · ${p.read}/${p.len}`;
  }
  return list.length > 1 ? `${s} <span class="dg-muted">(+${list.length - 1} parse${list.length > 2 ? 's' : ''})</span>` : s;
}

function unitLabel(t, u) {
  const lines = u.printed_lines.map((i) => i + 1);
  const joined = lines.length > 1 ? ` · printed lines ${lines[0]}–${lines[lines.length - 1]} joined` : '';
  return `<span class="te">పాదం ${u.unit}</span>${joined}`;
}

function renderPoem(f) {
  const t = T();
  const cur = f.u ?? -1;
  const html = t.units.map((u, ui) => {
    let status = '';
    const done = f.type === 'stanza' || ui < cur || (ui === cur && f.type === 'end');
    if (done) {
      const ok = u.accepted.length || (u.padanta && u.padanta.accepted.length);
      status = ok ? '<span class="dg-pada-status ok">✓ accepted</span>' : '<span class="dg-pada-status bad">✗ no metre</span>';
    }
    const chips = u.aksharas.map((a, j) => {
      const k = j + 1;
      let cls = '';
      if (f.type === 'stanza' || ui < cur) cls = u.death_step && k > u.death_step ? 'unread' : 'read';
      else if (ui === cur) {
        const kk = f.type === 'end' ? u.steps.length : f.k;
        if (u.death_step && k === u.death_step && kk >= k) cls = 'dead';
        else if (u.death_step && k > u.death_step && (f.type === 'end')) cls = 'unread';
        else if (k < kk) cls = 'read';
        else if (k === kk && f.type === 'step') cls = 'cur';
        else if (k === kk) cls = 'read';
      }
      const w = a.options.length > 1 ? `${wspan(a.options[0])}/${wspan(a.options[1])}` : wspan(a.options);
      let v2 = '';
      if (t.version === 'v2') {
        const v = u.v2[j];
        const shown = cls === 'read' || cls === 'cur' || cls === 'dead';
        if (!v.inventory) v2 += '<span class="la" title="not in the akshara inventory (Layer A)">✗</span>';
        if (shown) {
          const sc = v.ends_word && v.finished !== null ? v.finished : v.partial;
          v2 += `<span class="lb s${sc}"></span>`;
        }
      }
      const title = `${a.text}: ${a.weight === 'U' ? 'guru' : 'laghu'} (${(a.rules || []).join(', ')})${a.vikalpa ? ' · vikalpa: ' + a.vikalpa : ''}`;
      return `<span class="dg-chip ${cls}" data-u="${ui}" data-k="${k}" title="${esc(title)}"><span class="a">${esc(a.text)}</span><span class="w">${w}</span>${v2}</span>`;
    }).join('');
    return `<div class="dg-pada ${ui === cur ? 'active' : ''}"><div class="dg-pada-head">${unitLabel(t, u)}${status}</div><div class="dg-chips">${chips}</div></div>`;
  }).join('');
  const el = $('dg-poem-view');
  el.innerHTML = html;
  const active = el.querySelector('.dg-pada.active');
  if (active) active.scrollIntoView({ block: 'nearest' });
}

function renderCaption(f) {
  const t = T();
  const G = S.G;
  const el = $('dg-caption');
  const st = G.stats;
  if (f.type === 'intro') {
    const lv = t.level !== 'canonical' ? `<p class="dg-note">This poem is identified only under ${esc(LEVELS[t.level])}, so the walk follows every admissible reading at once: the frontier can hold several states.</p>` : '';
    const v2 = t.version === 'v2' ? `<p><b>v2</b> keeps this metre DAWG exactly as it is and adds two corpus layers, both read akshara by akshara under it: <b>Layer A</b>, only the ${fmt(t.v2.inventory_size)} aksharas attested in real verse may be written (a ring at the walker, green or red); <b>Layer B</b>, a suffix automaton (Blumer's DAWG, ${fmt(t.v2.sam_states)} states) over the ${fmt(t.v2.words_in_corpus)} corpus words of two aksharas or more, which tells whether the word being written is real (the lane below).</p>` : '';
    el.innerHTML = `<h3>The metre DAWG</h3>
      <p>${fmt(st.states)} states and ${fmt(st.edges)} edges, compiled from ${st.meters} metres (${st.hypotheses} line slots) and minimized from ${fmt(st.dfa_states_unminimized)} states. Every legal pāda of every metre is one path from START to an accepting state: ${fmt(st.distinct_lines)} distinct lines, the longest ${st.max_line_length} aksharas.</p>
      <p>Left to right is depth: the most aksharas that can have been read on arrival. Colour shows which family a state can still lead to.</p>
      ${v2}${lv}
      <p class="dg-note">Press <span class="dg-kbd">→</span> or <span class="dg-kbd">Space</span> to read the poem one akshara at a time. Drag to orbit, scroll to zoom, hover a state for its details, hover a hypothesis to light up its part of the graph.</p>`;
    return;
  }
  if (f.type === 'stanza') { el.innerHTML = stanzaHtml(); return; }
  const u = t.units[f.u];
  if (f.type === 'start') {
    const joined = u.printed_lines.length > 1 ? `<p class="dg-note">The metre prints each pāda as ${u.printed_lines.length} half-lines; they are joined into one pāda, as the identifier read them.</p>` : '';
    el.innerHTML = `<h3>${unitLabel(t, u)}: ${u.aksharas.length} aksharas</h3>
      <p>Every pāda is read from START. Nothing has been read yet, so all ${G.hypotheses.length} hypotheses (metre, slot) are alive and the whole DAWG is reachable.</p>${joined}`;
    return;
  }
  if (f.type === 'step') {
    const st2 = u.steps[f.k - 1];
    const a = u.aksharas[f.k - 1];
    const weight = a.weight === 'U' ? `<b class="w-U">guru (U)</b>` : `<b class="w-I">laghu (|)</b>`;
    const why = (a.rules || []).map((r) => RULES[r] || r).join(', ');
    let move;
    if (a.options.length > 1) {
      move = `<p>The scanner leaves this akshara open (vikalpa: ${esc(VIKALPA[a.vikalpa] || a.vikalpa || 'compound boundary')}), so the walk tries both a ${wspan('U')} and a ${wspan('I')} edge.</p>`;
    } else move = '';
    if (st2.frontier.length) {
      const e = st2.edges;
      const hop = e.length === 1 ? `The walk takes the ${wspan(e[0][1])} edge from state ${e[0][0]} to state ${e[0][2]}.` : `The walk takes ${e.length} edges; the frontier now holds ${st2.frontier.length} state${st2.frontier.length > 1 ? 's' : ''} (${st2.frontier.join(', ')}).`;
      move += `<p>${hop}</p>`;
    } else {
      move += `<p class="died">No edge leaves the frontier with ${wspan(a.options[0])} here: no metre in the catalogue has a pāda that begins this way. The walk stops.</p>`;
    }
    const metres = new Set(st2.alive.map((h) => G.hypotheses[h].meter)).size;
    const died = st2.died.length ? `<p class="died">✗ ${st2.died.length} hypothes${st2.died.length > 1 ? 'es' : 'is'} died here: ${listNames(st2.died)}.</p>` : '';
    const alive = st2.alive.length ? `<p class="alive">${st2.alive.length} still alive (${metres} metre${metres > 1 ? 's' : ''}).</p>` : '';
    el.innerHTML = `<h3>Akshara ${f.k} of ${u.aksharas.length}: <span class="te">${esc(a.text)}</span></h3>
      <p>It is ${weight}: ${esc(why)}.</p>${move}${died}${alive}${v2Line(u, f.k)}`;
    return;
  }
  // end of a pāda
  const pad = u.padanta && u.padanta.accepted.length ? u.padanta : null;
  let body;
  if (u.accepted.length) {
    body = `<p class="alive">The walk ends in an accepting state: ${listNames(u.accepted, 6)}.</p>`;
  } else if (!pad) {
    const tooShort = Object.entries(u.died_at).filter(([, i]) => i >= u.aksharas.length).map(([h]) => +h);
    body = u.death_step ? `<p class="died">The walk died at akshara ${u.death_step}; no metre accepts this pāda.</p>`
      : `<p class="died">The walk ends in a state that accepts nothing: the pāda is too short for ${listNames(tooShort)}.</p>`;
  } else body = '';
  if (pad) {
    body += `<p>The last akshara is laghu. Read as guru (pādānta, line-final laghu as guru), the walk reaches state${pad.states.length > 1 ? 's' : ''} ${pad.states.join(', ')}, accepting: <span class="alive">${listNames(pad.accepted, 6)}</span>.</p>`;
  }
  el.innerHTML = `<h3>End of ${unitLabel(t, u)}</h3>${body}<p class="dg-note">Accepting a pāda is only half the verdict: the stanza layer still has to fit every pāda into one metre's slot pattern.</p>`;
}

function v2Line(u, k) {
  if (T().version !== 'v2') return '';
  const v = u.v2[k - 1];
  const a = v.inventory ? '<span class="alive">attested</span>' : '<span class="died">never seen in real verse: v2 refuses to write it</span>';
  return `<p class="dg-note">v2 · Layer A: <span class="te">${esc(u.aksharas[k - 1].text)}</span> is ${a}. Layer B: see the lane under the graph.</p>`;
}

function stanzaHtml() {
  const t = T();
  const v = t.verdict;
  const G = S.G;
  let head;
  if (v.best) {
    const tr = v.best.trailer ? ` + <span class="te">${esc(v.best.trailer.name_te)}</span>` : '';
    head = `<div class="dg-verdict"><span class="big">${esc(v.best.name_te)}</span>${tr}<span class="dg-muted">${esc(v.best.label)}${v.ambiguous ? ' · ambiguous: ' + esc(v.candidates.join(', ')) : ''}</span></div>`;
  } else {
    head = `<div class="dg-verdict bad"><span class="big">No metre</span><span class="dg-muted">no metre accepts every pāda in its slot</span></div>`;
  }
  const units = t.units;
  const rows = t.stanza.rows.slice(0, 8).map((r) => {
    const cells = units.map((u) => {
      const c = r.cells[String(u.unit)];
      return c ? `<td class="ok" title="${esc(c.map((x) => x.slot + (x.padanta ? ' (pādānta)' : '')).join(', '))}">✓${c.some((x) => x.padanta) ? '′' : ''}</td>` : '<td class="no">·</td>';
    }).join('');
    const why = r.matched ? '' : `<tr><td></td><td class="why" colspan="${units.length}">${esc(r.reason)}</td></tr>`;
    return `<tr class="${r.matched ? 'win' : ''}"><td><span class="te">${esc(r.name_te.replace(/_/g, ' '))}</span> ${r.matched ? '✓' : ''}</td>${cells}</tr>${why}`;
  }).join('');
  const matrix = rows ? `<table class="dg-matrix"><tr><th>metre</th>${units.map((u) => `<th>${u.unit}</th>`).join('')}</tr>${rows}</table>` : '';
  let ganas = '';
  if (v.best) {
    ganas = '<div class="dg-ganas">' + v.best.lines.map((ln) => `<div class="dg-ganas-row"><span class="n">${ln.line_no}${ln.slot !== 'all' ? ' ' + esc(ln.slot) : ''}</span>${ln.ganas.map((g) => `<span class="dg-gana"><span class="te">${esc(g.te)}</span><span class="p">${[...g.pattern].map(wspan).join('')}</span></span>`).join('')}${ln.padanta ? '<span class="dg-muted">pādānta</span>' : ''}</div>`).join('') + '</div>';
  }
  const fails = !v.best && v.failures.length ? '<p class="dg-note">' + v.failures.slice(0, 4).map((x) => `${esc(x.meter)}: ${esc(x.reason)}`).join('<br>') + '</p>' : '';
  const notes = v.notes.length ? `<p class="dg-note">${v.notes.map(esc).join('<br>')}</p>` : '';
  const viol = v.best && v.best.violations.length ? `<p class="died">Stanza rule broken: ${v.best.violations.map(esc).join('; ')}</p>` : '';
  const v2 = t.version === 'v2' ? v2Summary() : '';
  return `<h3>The stanza layer</h3>
    <p>Each metre needs every pāda accepted in the slot it assigns that pāda (కందము: odd, even, odd, even), and its stanza rules kept. Metres that accepted at least one pāda (✓′ = by pādānta):</p>
    ${head}${matrix}${viol}${ganas ? '<p class="dg-note">గణవిభజన of the winning parse:</p>' + ganas : ''}${fails}${notes}${v2}`;
}

function v2Summary() {
  const s = T().v2;
  const bad = s.n_outside ? `<span class="died">${s.n_outside} outside the inventory (${s.outside_inventory.map(esc).join(' ')})</span>` : '<span class="alive">all attested</span>';
  const share = s.scored_words ? Math.round((100 * s.real_words) / s.scored_words) : 0;
  return `<p><b>v2 layers.</b> Aksharas: ${s.aksharas}, ${bad}. Words of two aksharas or more: ${s.real_words} of ${s.scored_words} real (${share}%)${s.single_akshara_words ? `, ${s.single_akshara_words} single-akshara word${s.single_akshara_words > 1 ? 's' : ''} not scored` : ''}.</p>
    ${s.junk_words.length ? `<p class="dg-note">Not corpus words: <span class="te">${s.junk_words.slice(0, 10).map(esc).join(', ')}</span>${s.junk_words.length > 10 ? ' …' : ''}</p>` : ''}
    <p class="dg-note">Layer B only reweights the decoder's choices; it never removes one, so the metre guarantee is untouched. Poems from the corpus are attested by construction.</p>`;
}

function hypStatus(f, h) {
  const t = T();
  if (f.type === 'intro') return { cls: '', st: '', pos: '' };
  if (f.type === 'stanza') {
    const ticks = t.units.map((u) => (u.accepted.includes(h) || (u.padanta && u.padanta.accepted.includes(h)) ? '<span class="y">✓</span>' : '<span class="n">·</span>')).join('');
    const n = t.units.filter((u) => u.accepted.includes(h) || (u.padanta && u.padanta.accepted.includes(h))).length;
    const metre = S.G.hypotheses[h].meter;
    const win = t.verdict.best && (t.verdict.best.meter === metre || (t.verdict.best.trailer && t.verdict.best.trailer.meter === metre));
    return { cls: win ? 'accepted' : n ? '' : 'dead', st: win ? '✓ verdict' : `${n}/${t.units.length}`, ticks, n };
  }
  const u = t.units[f.u];
  if (f.type === 'start') return { cls: 'alive', st: 'alive', pos: 'waiting for akshara 1' };
  const d = u.died_at[String(h)];
  if (f.type === 'step') {
    const st = u.steps[f.k - 1];
    if (st.alive.includes(h)) return { cls: 'alive', st: 'alive', pos: fmtPos(st.positions[String(h)]) };
    return { cls: 'dead' + (st.died.includes(h) ? ' just-died' : ''), st: `✗ akshara ${d + 1}`, pos: '', d };
  }
  if (u.accepted.includes(h)) return { cls: 'accepted', st: '✓ accepts', pos: '' };
  if (u.padanta && u.padanta.accepted.includes(h)) return { cls: 'accepted', st: '✓ pādānta', pos: 'last laghu read as guru' };
  if (d === undefined) return { cls: 'dead', st: '✗', pos: '', d: -1 };
  return { cls: 'dead', st: d >= u.aksharas.length ? '✗ too short' : `✗ akshara ${d + 1}`, pos: '', d };
}

function renderHyps(f) {
  const G = S.G;
  const rows = G.hypotheses.map((h) => ({ h, s: hypStatus(f, h.id) }));
  const rank = (r) => (r.s.cls.startsWith('accepted') ? 0 : r.s.cls.startsWith('alive') ? 1 : r.s.cls === '' ? 1 : 2);
  rows.sort((a, b) => rank(a) - rank(b) || (f.type === 'stanza' ? (b.s.n || 0) - (a.s.n || 0) : 0)
    || (rank(a) === 2 ? (b.s.d ?? -1) - (a.s.d ?? -1) : 0) || a.h.id - b.h.id);
  $('dg-hyps').innerHTML = rows.map(({ h, s }) => `<li class="dg-hyp ${s.cls}" data-h="${h.id}" style="--fam:${FAMILY_CSS[h.family] || 'var(--fam-mixed)'}" title="${esc(h.meter)} · ${esc(h.family)}">
      <span class="d"></span><span class="nm">${hypName(h)}</span><span class="st">${s.st}</span>
      ${s.pos ? `<span class="pos">${s.pos}</span>` : ''}${s.ticks ? `<span class="ticks">${s.ticks}</span>` : ''}</li>`).join('');
  let alive = G.hypotheses.length;
  if (f.type === 'step') alive = T().units[f.u].steps[f.k - 1].alive.length;
  else if (f.type === 'end') { const u = T().units[f.u]; alive = u.accepted.length + (u.padanta?.accepted.length || 0); }
  else if (f.type === 'stanza') alive = T().verdict.best ? rows.filter((r) => r.s.cls === 'accepted').length : 0;
  const label = f.type === 'end' ? 'accepting' : f.type === 'stanza' ? 'win' : 'alive';
  $('dg-hyps-count').textContent = `${alive} / ${G.hypotheses.length} ${label}`;
  $('dg-bar-fill').style.width = `${(100 * alive) / G.hypotheses.length}%`;
}

function renderV2(f) {
  const t = T();
  const el = $('dg-v2');
  if (t.version !== 'v2') { el.hidden = true; return; }
  el.hidden = false;
  const s = t.v2;
  const head = `<h4>v2 layers</h4><div class="sub">A · ${fmt(s.inventory_size)} attested aksharas &nbsp;·&nbsp; B · word DAWG, ${fmt(s.words_in_corpus)} words, ${fmt(s.sam_states)} states</div>`;
  if (f.type !== 'step') {
    if (f.type === 'stanza' || f.type === 'intro') {
      const share = s.scored_words ? Math.round((100 * s.real_words) / s.scored_words) : 0;
      el.innerHTML = `${head}<div class="row"><span class="k">Layer A</span><span class="${s.n_outside ? 'bad' : 'ok'}">${s.n_outside ? `✗ ${s.n_outside} of ${s.aksharas} aksharas outside` : `✓ all ${s.aksharas} aksharas attested`}</span></div>
        <div class="row"><span class="k">Layer B</span><span class="${share >= 80 ? 'ok' : share >= 40 ? 'warn' : 'bad'}">${s.real_words} / ${s.scored_words} real words (${share}%)</span></div>`;
    } else if (f.type === 'end') {
      const u = t.units[f.u];
      const outN = u.v2.filter((x) => !x.inventory).length;
      const words = u.v2.filter((x) => x.ends_word && x.finished !== null);
      const real = words.filter((x) => x.finished).length;
      el.innerHTML = `${head}<div class="row"><span class="k">Layer A</span><span class="${outN ? 'bad' : 'ok'}">${outN ? `✗ ${outN} of ${u.aksharas.length} aksharas outside` : `✓ all ${u.aksharas.length} aksharas attested`}</span></div>
        <div class="row"><span class="k">Layer B</span><span class="${real === words.length ? 'ok' : real ? 'warn' : 'bad'}">${real} / ${words.length} real words in this pāda</span></div>`;
    } else el.innerHTML = `${head}<div class="row sub">Read the pāda to see each akshara pass both layers.</div>`;
    return;
  }
  const u = t.units[f.u];
  const v = u.v2[f.k - 1];
  const a = u.aksharas[f.k - 1];
  const sc = { 2: ['ok', 'begins a real word (2)'], 1: ['warn', 'inside a real word (1)'], 0: ['bad', 'in no corpus word (0)'] }[v.partial];
  let fin = '';
  if (v.ends_word) {
    fin = v.finished === null ? '<span class="sub">single akshara: not scored</span>'
      : v.finished ? '<span class="ok">✓ a real word (2)</span>' : '<span class="bad">✗ not a corpus word (0)</span>';
  }
  const last = v.chars[v.chars.length - 1];
  const upto = u.v2.slice(0, f.k);
  const outN = upto.filter((x) => !x.inventory).length;
  const words = upto.filter((x) => x.ends_word && x.finished !== null);
  el.innerHTML = `${head}
    <div class="row"><span class="k">Layer A</span><span class="te">${esc(a.text)}</span>${v.inventory ? '<span class="ok">✓ attested</span>' : '<span class="bad">✗ never in real verse</span>'}</div>
    <div class="row"><span class="k">word so far</span><span class="word">${esc(v.word)}</span></div>
    <div class="row"><span class="k">Layer B</span><span class="${sc[0]}">● ${sc[1]}</span></div>
    ${fin ? `<div class="row"><span class="k">word ends</span>${fin}</div>` : ''}
    <div class="row"><span class="k">next chars</span><span class="sub">${last.state === null ? 'none: fell off the automaton' : `${last.out} possible <span class="te">${esc(last.sample)}</span>${last.out > 12 ? '…' : ''}`}</span></div>
    <div class="row sub">this pāda so far: ${outN} outside the inventory · ${words.filter((x) => x.finished).length}/${words.length} real words</div>`;
}

function renderPanels(f) {
  renderPoem(f);
  renderCaption(f);
  renderHyps(f);
  renderV2(f);
  $('dg-counter').textContent = `${S.idx + 1} / ${S.frames.length}`;
  $('dg-scrub').value = String(S.idx);
  $('dg-prev').disabled = S.idx === 0;
  $('dg-first').disabled = S.idx === 0;
  $('dg-next').disabled = S.idx === S.frames.length - 1;
  $('dg-next').textContent = f.type === 'intro' ? 'Start ▶' : S.idx === S.frames.length - 2 ? 'Verdict ▶' : 'Next ▶';
}

// ---------------------------------------------------------------------------
// navigation
// ---------------------------------------------------------------------------
function go(idx, animate = false) {
  idx = Math.max(0, Math.min(S.frames.length - 1, idx));
  const step = animate && idx === S.idx + 1;
  S.idx = idx;
  const f = S.frames[idx];
  applyScene(f, step);
  renderPanels(f);
  if (S.playing && !anim) schedulePlay();
}

function schedulePlay() {
  clearTimeout(S.playTimer);
  if (!S.playing) return;
  if (S.idx >= S.frames.length - 1) { setPlaying(false); return; }
  const f = S.frames[S.idx];
  const dwell = { intro: 1600, start: 1000, step: 380, end: 1900, stanza: 0 }[f.type] / S.speed;
  S.playTimer = setTimeout(() => go(S.idx + 1, true), dwell);
}

function setPlaying(on) {
  S.playing = on;
  $('dg-play').textContent = on ? '⏸' : '⏵';
  if (on) {
    if (S.idx >= S.frames.length - 1) go(0);
    schedulePlay();
  } else clearTimeout(S.playTimer);
}

// ---------------------------------------------------------------------------
// data loading
// ---------------------------------------------------------------------------
function loading(on, text) {
  $('dg-loading').hidden = !on;
  if (text) $('dg-loading-text').textContent = text;
}

async function fetchTrace(poem, version) {
  const r = await fetch('/api/dawg/trace', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ poem, version }),
  });
  const data = await r.json();
  if (!r.ok) throw new Error(data.error || r.statusText);
  return data;
}

async function loadTrace(poem, version, keepIdx = false) {
  loading(true, version === 'v2' ? 'Reading the poem through the v2 layers… (the word DAWG is built once: about 6 s)' : 'Tracing the poem through the DAWG…');
  try {
    S.traces[version] = await fetchTrace(poem, version);
  } catch (err) {
    loading(false);
    alert(err.message);
    return false;
  }
  S.poem = poem;
  S.version = version;
  document.querySelectorAll('.dg-seg').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.version === version)));
  $('dg').classList.toggle('v2', version === 'v2');
  const old = S.idx;
  buildFrames();
  loading(false);
  go(keepIdx ? Math.min(old, S.frames.length - 1) : 0);
  const url = new URL(window.location.href);
  url.searchParams.set('version', version);
  window.history.replaceState(null, '', url);
  return true;
}

async function setVersion(version) {
  if (version === S.version) return;
  setPlaying(false);
  if (S.traces[version] && S.traces[version].poem === S.poem) {
    S.version = version;
    document.querySelectorAll('.dg-seg').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.version === version)));
    $('dg').classList.toggle('v2', version === 'v2');
    buildFrames();
    go(Math.min(S.idx, S.frames.length - 1));
  } else {
    await loadTrace(S.poem, version, true);
  }
}

// ---------------------------------------------------------------------------
// interaction
// ---------------------------------------------------------------------------
function wireUi() {
  $('dg-next').onclick = () => { setPlaying(false); go(S.idx + 1, true); };
  $('dg-prev').onclick = () => { setPlaying(false); go(S.idx - 1); };
  $('dg-first').onclick = () => { setPlaying(false); go(0); };
  $('dg-play').onclick = () => setPlaying(!S.playing);
  $('dg-speed').onchange = (e) => { S.speed = +e.target.value; };
  $('dg-scrub').oninput = (e) => { setPlaying(false); go(+e.target.value); };
  $('dg-follow').onchange = (e) => { S.follow = e.target.checked; if (S.follow) go(S.idx); };
  document.querySelectorAll('.dg-seg').forEach((b) => { b.onclick = () => setVersion(b.dataset.version); });

  $('dg-poem-view').addEventListener('click', (e) => {
    const chip = e.target.closest('.dg-chip');
    if (!chip) return;
    const ui = +chip.dataset.u, k = +chip.dataset.k;
    const target = S.frameOf[ui]?.[k] ?? S.frameOf[ui]?.[S.frameOf[ui].length - 1];
    if (target !== undefined) { setPlaying(false); go(target); }
  });

  const list = $('dg-hyps');
  list.addEventListener('mouseover', (e) => {
    const li = e.target.closest('.dg-hyp');
    const h = li ? +li.dataset.h : null;
    if (h !== S.focusHyp) { S.focusHyp = h; refocus(); }
  });
  list.addEventListener('mouseleave', () => { S.focusHyp = null; refocus(); });

  // poem drawer
  const sel = $('dg-example');
  boot.examples.forEach((ex) => {
    const o = document.createElement('option');
    o.value = ex.id;
    o.textContent = ex.title;
    sel.appendChild(o);
  });
  const syncExample = () => {
    const ex = boot.examples.find((x) => x.text.trim() === $('dg-poem').value.trim());
    sel.value = ex ? ex.id : '';
    $('dg-example-note').textContent = ex && ex.note ? ex.note : '';
  };
  sel.onchange = () => {
    const ex = boot.examples.find((x) => x.id === sel.value);
    if (ex) $('dg-poem').value = ex.text;
    $('dg-example-note').textContent = ex && ex.note ? ex.note : '';
  };
  $('dg-poem').oninput = syncExample;
  $('dg-edit').onclick = () => {
    const d = $('dg-drawer');
    d.hidden = !d.hidden;
    if (!d.hidden) { $('dg-poem').value = S.poem; syncExample(); $('dg-poem').focus(); }
  };
  $('dg-cancel').onclick = () => { $('dg-drawer').hidden = true; };
  $('dg-trace').onclick = async () => {
    const text = $('dg-poem').value.trim();
    if (!text) return;
    setPlaying(false);
    S.traces = {};
    if (await loadTrace(text, S.version)) $('dg-drawer').hidden = true;
  };

  window.addEventListener('keydown', (e) => {
    if (e.target.closest('textarea, input, select')) return;
    if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); setPlaying(false); go(S.idx + 1, true); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); setPlaying(false); go(S.idx - 1); }
    else if (e.key === 'Home') { setPlaying(false); go(0); }
    else if (e.key === 'End') { setPlaying(false); go(S.frames.length - 1); }
    else if (e.key === 'p' || e.key === 'P') setPlaying(!S.playing);
  });

  // hover a state: tooltip
  const ray = new THREE.Raycaster();
  const ndc = new THREE.Vector2();
  const tip = $('dg-tooltip');
  let pending = null;
  renderer.domElement.addEventListener('pointermove', (e) => {
    pending = e;
  });
  renderer.domElement.addEventListener('pointerleave', () => { pending = null; tip.hidden = true; });
  G3.hover = () => {
    if (!pending || !G3.nodeMesh) return;
    const e = pending;
    pending = null;
    const r = renderer.domElement.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    const hit = ray.intersectObject(G3.nodeMesh)[0];
    if (!hit) { tip.hidden = true; return; }
    const n = S.G.nodes[hit.instanceId];
    const hyps = S.G.hypotheses;
    const metres = [...new Set(n.reach.map((h) => hyps[h].meter))];
    const acc = n.accept.length ? `<div>accepts: ${n.accept.map((h) => hypName(hyps[h])).join(', ')}</div>` : '';
    tip.innerHTML = `<b>state ${n.id}</b>${n.id === S.G.start ? ' · START' : ''} · depth ${n.depth}${acc}
      <div>can still become ${metres.length} metre${metres.length > 1 ? 's' : ''}: ${n.reach.slice(0, 6).map((h) => hypName(hyps[h])).join(', ')}${n.reach.length > 6 ? ' …' : ''}</div>`;
    tip.hidden = false;
    tip.style.left = `${Math.min(e.clientX + 14, window.innerWidth - 320)}px`;
    tip.style.top = `${e.clientY + 14}px`;
  };
}

function refocus() {
  // recolour only: no camera move, no animation
  const f = S.frames[S.idx];
  if (!f || anim) return;
  const keepFollow = followTarget;
  const keepFly = fly;
  applyScene(f, false);
  followTarget = keepFollow;
  fly = keepFly;
}

// centre the projection on the free space between the two panels
function viewOffset(w, h) {
  const l = $('dg-left').getBoundingClientRect();
  const r = $('dg-right').getBoundingClientRect();
  const left = l.width && l.height && l.top < h * 0.5 ? l.right : 0;
  const right = r.width && r.height && getComputedStyle($('dg-right')).display !== 'none' ? r.left : w;
  const d = Math.round((left + right) / 2 - w / 2);
  G3.freeW = right - left;
  if (Math.abs(d) < 4) camera.clearViewOffset();
  else camera.setViewOffset(w + 2 * Math.abs(d), h, d > 0 ? 0 : 2 * Math.abs(d), 0, w, h);
}

function onResize() {
  const w = stage.clientWidth, h = stage.clientHeight;
  camera.aspect = w / h;
  viewOffset(w, h);
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
  composer.setSize(w, h);
  bloom.setSize(w, h);
  labelRenderer.setSize(w, h);
}
window.addEventListener('resize', onResize);

let last = performance.now();
function loop(now) {
  const dt = Math.min(0.1, (now - last) / 1000);
  last = now;
  tickAnim(now);
  tickCamera(now, dt);
  if (G3.colorsDirty) writeColors(1 - Math.exp(-dt * 7));
  const pulse = 1 + 0.12 * Math.sin(now / 260);
  haloGroup.children.forEach((s) => s.scale.setScalar(s.userData.base * pulse));
  if (G3.hover) G3.hover();
  controls.update();
  composer.render();
  labelRenderer.render(scene, camera);
  requestAnimationFrame(loop);
}

// ---------------------------------------------------------------------------
// start
// ---------------------------------------------------------------------------
(async function main() {
  loading(true, S.version === 'v2' ? 'Loading the DAWG and the v2 layers… (the word DAWG is built once: about 6 s)' : 'Loading the DAWG…');
  try {
    const [g, t] = await Promise.all([
      fetch('/api/dawg/graph').then((r) => r.json()),
      fetchTrace(S.poem, S.version),
    ]);
    S.G = g;
    S.traces[S.version] = t;
  } catch (err) {
    $('dg-loading-text').textContent = `Could not load: ${err.message}`;
    return;
  }
  const st = S.G.stats;
  $('dg-stats').textContent = `${fmt(st.states)} states · ${fmt(st.edges)} edges · ${st.meters} metres · ${st.hypotheses} slots`;
  buildGraph(S.G);
  wireUi();
  document.querySelectorAll('.dg-seg').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.version === S.version)));
  $('dg').classList.toggle('v2', S.version === 'v2');
  buildFrames();
  onResize();
  const [t0, p0] = overviewShot();
  controls.target.copy(t0);
  camera.position.copy(p0);
  loading(false);
  go(0);
  requestAnimationFrame(loop);
})();

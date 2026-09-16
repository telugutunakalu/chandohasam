#!/usr/bin/env python3
"""Combine the three Outputs/*.txt files into one structured JSON.

File roles (established by inspection):
  "... chandas (1).txt"  -> prompt INPUTS: 10 chandas x 4 topics x 3 input tiers
  "... chandas (2).txt"  -> 31 generated poems, single uniform schema
  "... chandas.txt"      -> 224 generated poems in 2 batches, 7 schema variants
"""
import json, re, hashlib, pathlib, collections, datetime, unicodedata

D = pathlib.Path("/home/samvaran/phd_workspace/anlp_project/Outputs")
OUT = D / "chandas_dataset.json"

F_INPUTS = "Prompt templates for various chandas (1).txt"
F_POEMS2 = "Prompt templates for various chandas (2).txt"
F_POEMS1 = "Prompt templates for various chandas.txt"


# ---------------------------------------------------------------- json scanner
def scan_json(text):
    """Yield (start_line, end_line, obj) for each top-level {...}/[...] that parses."""
    i, n = 0, len(text)
    while i < n:
        if text[i] not in "[{":
            i += 1
            continue
        depth, j, instr, esc = 0, i, False, False
        while j < n:
            ch = text[j]
            if instr:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    instr = False
            else:
                if ch == '"':
                    instr = True
                elif ch in "[{":
                    depth += 1
                elif ch in "]}":
                    depth -= 1
                    if depth == 0:
                        break
            j += 1
        chunk = text[i:j + 1]
        try:
            obj = json.loads(chunk)
        except Exception:
            i += 1
            continue
        yield (text.count("\n", 0, i) + 1, text.count("\n", 0, j) + 1, obj)
        i = j + 1


# ------------------------------------------------------------- inputs (file 1)
CH_HDR = re.compile(r"^\**\s*(\d+)\.\s*([A-Za-z]+)\s*\(([^)]+)\)\s*—\s*(.+)$")
TOPIC = re.compile(r"^\**\s*Topic\s+(\d+):\s*(.+)$")
FIELD = re.compile(r"^\**\s*(Word|Single Line|Full Bhavam)\s*(\([^)]*\))?\s*:\s*(.*)$")


def parse_inputs(text):
    chandas, cur_ch, cur_tp, collecting = [], None, None, False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = CH_HDR.match(line)
        if m:
            collecting = False
            cur_ch = {
                "index": int(m.group(1)),
                "name_en": m.group(2),
                "name_te": m.group(3),
                "form_note": m.group(4).strip(),
                "topics": [],
            }
            chandas.append(cur_ch)
            cur_tp = None
            continue
        m = TOPIC.match(line)
        if m and cur_ch is not None:
            collecting = False
            title = m.group(2).strip()
            cat = None
            mm = re.match(r"^(.*?)\s*\(([^)]+)\)\s*$", title)
            if mm:
                title, cat = mm.group(1).strip(), mm.group(2).strip()
            cur_tp = {
                "index": int(m.group(1)),
                "title_en": title,
                "category_te": cat,
                "tiers": {"word": None, "single_line": None, "full_bhavam": []},
            }
            cur_ch["topics"].append(cur_tp)
            continue
        m = FIELD.match(line)
        if m and cur_tp is not None:
            kind, val = m.group(1), m.group(3).strip()
            collecting = False
            if kind == "Word":
                cur_tp["tiers"]["word"] = val
            elif kind == "Single Line":
                cur_tp["tiers"]["single_line"] = val
            else:
                collecting = True          # Full Bhavam lines follow
                if val:
                    cur_tp["tiers"]["full_bhavam"].append(val)
            continue
        if collecting and cur_tp is not None and line.startswith("*"):
            body = line.lstrip("*").strip()
            if body:
                cur_tp["tiers"]["full_bhavam"].append(body)
    return chandas


# ------------------------------------------------------- section headers (f3)
SECTION_NAMES = ["ఉత్పలమాల", "champakamala", "shardulam", "mattenham", "atavelladi",
                 "tetageethi", "seesa padyam", "kandapadyam", "utsaham"]


def section_map(text):
    """[(line_no, header_text)] for real section headers only.

    Deliberately strict: the 108-poem batch is preceded by a preamble listing
    ("Chandas:", "Alankaras:", "Topics:" and the names under each), and a loose
    `Word:`-style regex swallows those as headers, which silently mislabels the
    whole batch. A line qualifies only if it announces an output count or names
    one of the known chandas sections.
    """
    heads = []
    for i, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        if not s or s[0] in "`{[" or s.startswith("_____"):
            continue
        low = s.lower()
        has_out = "output" in low
        named = any(low.startswith(n) for n in SECTION_NAMES)
        # Real headers are labelled: either they announce a count ("108 OUTPUTS
        # రాధే", "Champakamala : 10 outputs:") or they are a chandas name followed
        # by a colon ("Shardulam:"). A bare chandas name is a preamble list item
        # under "Chandas:" -- accepting those lets L18547 "ఉత్పలమాల" override the
        # 108-batch header and reassign all 108 poems to the utpalamala batch.
        if (has_out and (":" in s or re.match(r"^\d", s))) or (named and ":" in s):
            heads.append((i, s))
    return heads


CONTRIB = {"సంవరణ్": "Samvaran", "రాధే": "Radhe"}
SLUG = {
    "ఉత్పలమాల": "utpalamala", "Champakamala": "champakamala", "Shardulam": "shardulam",
    "Mattenham": "mattebham", "Atavelladi": "aataveladi", "Tetageethi": "tetagiti",
    "Seesa padyam": "seesam", "Kandapadyam": "kandam", "Utsaham": "utsaham",
}
# chandas implied by each section header (headers are the only source for these)
HDR_CHANDAS = {
    "utpalamala": "ఉత్పలమాల", "champakamala": "చంపకమాల", "shardulam": "శార్దూలవిక్రీడితం",
    "mattebham": "మత్తేభవిక్రీడితం", "aataveladi": "ఆటవెలది", "tetagiti": "తేటగీతి",
    "seesam": "సీసం", "kandam": "కందం", "utsaham": "ఉత్సాహం",
}


def classify_header(s):
    contributor = next((v for k, v in CONTRIB.items() if k in s), None)
    if "108" in s:
        return "alankara-108", contributor, None
    for k, slug in SLUG.items():
        if k.lower() in s.lower():
            return slug, contributor, HDR_CHANDAS.get(slug)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or None, contributor, None


# Canonical chandas ids. Raw values vary across batches: bare Telugu, Telugu with
# an English gloss in parentheses, and two spellings each for shardula/mattebha/
# utsaham. Collapsing them is what makes by_chandassu counts meaningful.
CANON = [
    ("utpalamala",        "ఉత్పలమాల",           ["ఉత్పలమాల", "utpalamala"]),
    ("champakamala",      "చంపకమాల",            ["చంపకమాల", "champakamala"]),
    ("shardulavikriditam", "శార్దూలవిక్రీడితం",   ["శార్దూలవిక్రీడిత", "శార్దూలం", "shardula"]),
    ("mattebhavikriditam", "మత్తేభవిక్రీడితం",   ["మత్తేభవిక్రీడిత", "మత్తేభం", "mattebha", "mattenham"]),
    ("aataveladi",        "ఆటవెలది",             ["ఆటవెలది", "aataveladi", "atavelladi"]),
    ("tetagiti",          "తేటగీతి",             ["తేటగీతి", "tetagiti", "tetageethi"]),
    ("seesam",            "సీసం",                ["సీస", "seesa"]),
    ("kandam",            "కందం",                ["కంద", "kanda"]),
    ("utsaham",           "ఉత్సాహం",             ["ఉత్సాహ", "utsaham"]),
    ("dwipada",           "ద్విపద",              ["ద్విపద", "dwipada"]),
]


# The nine alankaras of the 108 batch. Raw values differ in whether they include
# "శబ్ద", an English gloss, or neither, so match on the distinctive stem.
CANON_ALANKARA = [
    ("vrittyanuprasa",  "వృత్యానుప్రాసాలంకారం",   ["వృత్యానుప్రాస", "vrittyanuprasa"]),
    ("antyanuprasa",    "అంత్యానుప్రాసాలంకారం",   ["అంత్యానుప్రాస", "antyanuprasa"]),
    ("yamaka",          "యమకాలంకారం",             ["యమక", "yamaka"]),
    ("muktapadagrasta", "ముక్తపదగ్రస్తాలంకారం",   ["ముక్తపదగ్రస్త", "muktapadagrasta"]),
    ("chekanuprasa",    "ఛేకానుప్రాసాలంకారం",     ["ఛేకానుప్రాస", "chekanuprasa"]),
    ("rupaka",          "రూపకాలంకారం",            ["రూపక", "rupaka"]),
    ("shlesha",         "శ్లేషాలంకారం",           ["శ్లేష", "shlesha"]),
    ("upama",           "ఉపమాలంకారం",             ["ఉపమా", "ఉపమ", "upama"]),
    ("atishayokti",     "అతిశయోక్త్యలంకారం",      ["అతిశయోక్త", "atishayokt"]),
]


def canon_alankara(raw):
    if not raw:
        return None, None
    s = unicodedata.normalize("NFC", raw).lower()
    for aid, te, pats in CANON_ALANKARA:
        if any(p.lower() in s for p in pats):
            return aid, te
    return None, None


def canon_chandassu(raw):
    """-> (canonical_id, canonical_telugu_name) or (None, None)."""
    if not raw:
        return None, None
    s = unicodedata.normalize("NFC", raw).lower()
    for cid, te, pats in CANON:
        if any(p.lower() in s for p in pats):
            return cid, te
    return None, None


# A gana sequence *is* the meter's signature, so it identifies the chandas for
# records that never name one. Verified against the labelled records.
GANA_SIG = {
    "భరనభభరవ": "utpalamala",
    "నజభజజజర": "champakamala",
    "మసజసతతగ": "shardulavikriditam",
    "సభరనమయవ": "mattebhavikriditam",
}


def gana_signature(analysis):
    """Single normalised gana signature for a record, or None if absent/inconsistent."""
    if not isinstance(analysis, dict):
        return None
    sigs = set()
    for v in analysis.values():
        if isinstance(v, dict) and isinstance(v.get("gana_sequence"), str):
            sigs.add(re.sub(r"[\s\-–—]+", "", unicodedata.normalize("NFC", v["gana_sequence"])))
    return sigs.pop() if len(sigs) == 1 else None


# ------------------------------------------------------------- normalisation
ANA_SHAPE = {
    ("line_1", "line_2", "line_3", "line_4"): "per_line_keys",
    ("line_breakdowns", "meter_rule", "prasa_note", "yati_rule"): "line_breakdowns",
    ("gana_structure", "lines_analysis", "meter", "prasa_niyamam"): "lines_analysis",
    ("line_by_line_breakdown", "meter_rule", "prasa_niyamam"): "breakdown_meter_rule",
    ("line_by_line_breakdown", "meter_scheme", "prasa", "total_letters_per_line",
     "yati_rule"): "breakdown_meter_scheme",
}
KNOWN = {
    "poem", "poem_lines", "poem_number", "title", "chandassu", "chandassu_name",
    "chandassu_analysis", "alankaram_name", "alankara_analysis", "topic",
    "telugu_meaning", "meaning_telugu", "english_meaning", "meaning_english",
}


def norm_text(s):
    if not isinstance(s, str):
        return None
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", s.strip()))


def split_meaning(v):
    """Return (single_string_or_None, variants_dict_or_None).

    Some shlesha (double-meaning) poems carry a dict of readings keyed
    context_1/context_2/... instead of one string; that distinction is the
    point of the figure, so it is preserved rather than flattened.
    """
    if isinstance(v, dict):
        return None, {k: norm_text(x) for k, x in v.items()}
    return norm_text(v), None


def normalise(rec, src_file, first_line, batch, contributor, header, hdr_chandas):
    poem = rec.get("poem")
    lines, title, chandassu = None, rec.get("title"), rec.get("chandassu_name") or rec.get("chandassu")
    if isinstance(poem, dict):
        lines = poem.get("lines")
        title = title or poem.get("title")
        chandassu = chandassu or poem.get("meter") or poem.get("vruttam")
    elif isinstance(poem, list):
        lines = poem
    if lines is None:
        pl = rec.get("poem_lines")
        if isinstance(pl, list):
            lines = pl
    lines = [norm_text(x) for x in lines if isinstance(x, str)] if isinstance(lines, list) else []

    ana = rec.get("chandassu_analysis")
    ana_shape = None
    if isinstance(ana, dict):
        ana_shape = ANA_SHAPE.get(tuple(sorted(ana.keys())), "other")
    alan = rec.get("alankara_analysis")
    alankaram = rec.get("alankaram_name") or (alan.get("alankaram") if isinstance(alan, dict) else None)

    m_te, m_te_var = split_meaning(rec.get("telugu_meaning") or rec.get("meaning_telugu"))
    m_en, m_en_var = split_meaning(rec.get("english_meaning") or rec.get("meaning_english"))

    extra = {k: v for k, v in rec.items() if k not in KNOWN}
    ch_raw = norm_text(chandassu) or hdr_chandas
    ch_id, ch_te = canon_chandassu(ch_raw)
    return {
        "source": {"file": src_file, "line": first_line},
        "batch": batch,
        "contributor": contributor,
        "section_header": header,
        "poem_number": rec.get("poem_number"),
        "title": norm_text(title) or None,
        "chandassu_id": ch_id,
        "chandassu": ch_te,
        "chandassu_raw": ch_raw,
        # where chandassu came from; later passes may upgrade None -> inferred
        "chandassu_source": (None if ch_id is None else
                             "section_header" if chandassu is None else "record"),
        "topic": norm_text(rec.get("topic")) or None,
        "alankaram_id": canon_alankara(alankaram)[0],
        "alankaram": canon_alankara(alankaram)[1],
        "alankaram_raw": norm_text(alankaram) or None,
        "line_count": len(lines),
        "lines": lines,
        "meaning_telugu": m_te,
        "meaning_telugu_variants": m_te_var,
        "meaning_english": m_en,
        "meaning_english_variants": m_en_var,
        "chandassu_analysis": {"shape": ana_shape, "raw": ana} if ana is not None else None,
        "alankara_analysis": ({"keys": sorted(alan.keys()), "raw": alan}
                              if isinstance(alan, dict) else None),
        "extra_fields": extra or None,
    }


# ------------------------------------------------------------------ collect
def collect_poems(fname, default_batch=None, default_contrib=None):
    text = (D / fname).read_text(encoding="utf-8-sig")
    heads = section_map(text)
    # Contributor is named once per batch, not once per section: "ఉత్పలమాల : 10
    # OUTPUTS సంవరణ్" then eight unattributed chandas sections, then "108 OUTPUTS
    # రాధే". So attribute by line range from each header that does name someone.
    marks = sorted((ln, c) for ln, h in heads
                   for k, c in CONTRIB.items() if k in h)

    def contrib_at(line):
        who = default_contrib
        for ln, c in marks:
            if ln <= line:
                who = c
            else:
                break
        return who

    out = []
    for s, e, obj in scan_json(text):
        hdr = None
        for ln, h in heads:
            if ln <= s:
                hdr = h
            else:
                break
        if hdr:
            batch, _, hdr_ch = classify_header(hdr)
        else:
            batch, hdr_ch = default_batch, None
        contrib = contrib_at(s)
        items = obj if isinstance(obj, list) else [obj]
        for it in items:
            if not isinstance(it, dict):
                continue
            if "poems" in it and isinstance(it["poems"], list):
                for p in it["poems"]:
                    if isinstance(p, dict):
                        r = normalise(p, fname, s, batch, contrib, hdr, hdr_ch)
                        r["collection_title"] = it.get("collection_title")
                        out.append(r)
                continue
            out.append(normalise(it, fname, s, batch, contrib, hdr, hdr_ch))
    return out


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def parse_batch_spec(text):
    """Parse the '4 Chandas x 9 Alankaras x 3 Topics = 108 poems' preamble.

    Its 'Chandas:' list is in generation order, which is what lets the unlabelled
    block be identified below.
    """
    lines = [l.strip() for l in text.splitlines()]
    spec, cur = {}, None
    for l in lines:
        if re.match(r"^(Chandas|Alankaras|Topics)\s*:$", l, re.I):
            cur = l.rstrip(":").strip().lower()
            spec[cur] = []
        elif cur and l and not l.startswith("_") and not l[0] in "`{[":
            if re.match(r"^(Chandas|Alankaras|Topics)\b", l, re.I) or "OUTPUTS" in l:
                cur = None
                continue
            spec[cur].append(l)
        elif not l:
            cur = None
    return {k: v for k, v in spec.items() if v}


poems = collect_poems(F_POEMS1)
poems += collect_poems(F_POEMS2, default_batch="uniform-31", default_contrib=None)

batch_spec = parse_batch_spec((D / F_POEMS1).read_text(encoding="utf-8-sig"))

# --- inference pass 1: unlabelled block of the 108 batch -----------------------
# The batch is 4 chandas x 27 (9 alankaras x 3 topics), numbered 1..108, emitted in
# the order the preamble declares. Poems 28-108 carry their chandas explicitly and
# fall into exact 27-blocks matching declaration order 2,3,4; so the unlabelled
# 1-27 is declaration order 1. Asserted rather than assumed, so a data change fails
# loudly instead of mislabelling.
b108 = [p for p in poems if p["batch"] == "alankara-108"]
if b108 and batch_spec.get("chandas"):
    declared = [canon_chandassu(c) for c in batch_spec["chandas"]]
    block = len(b108) // len(declared)
    ok = True
    for p in b108:
        n = p.get("poem_number")
        if not isinstance(n, int) or not (1 <= n <= len(b108)):
            ok = False
            break
        want = declared[(n - 1) // block]
        if p["chandassu_id"] and p["chandassu_id"] != want[0]:
            ok = False
            break
    if ok:
        for p in b108:
            if not p["chandassu_id"]:
                cid, cte = declared[(p["poem_number"] - 1) // block]
                p["chandassu_id"], p["chandassu"] = cid, cte
                p["chandassu_source"] = "batch_position"
    else:
        print("WARN: 108-batch block structure did not verify; left unlabelled")

# --- inference pass 2: gana signature ----------------------------------------
for p in poems:
    if p["chandassu_id"]:
        continue
    sig = gana_signature((p.get("chandassu_analysis") or {}).get("raw"))
    cid = GANA_SIG.get(sig or "")
    if cid:
        p["chandassu_id"] = cid
        p["chandassu"] = next(te for i, te, _ in CANON if i == cid)
        p["chandassu_source"] = "gana_signature"

# Stable ids, then duplicate detection at two strengths. Both occur in the data:
# byte-identical repeats (same verse emitted under a second alankara label) and
# verses sharing only their opening line (genuine regenerated variants). Collapsing
# the two would hide real variation, so they are reported separately and nothing is
# dropped.
by_first, by_full = collections.defaultdict(list), collections.defaultdict(list)
for i, p in enumerate(poems, 1):
    p["id"] = f"poem_{i:04d}"
    if p["lines"]:
        by_first[p["lines"][0]].append(p["id"])
        by_full[tuple(p["lines"])].append(p["id"])
for p in poems:
    if not p["lines"]:
        p["duplicate_exact"] = p["duplicate_shared_first_line"] = None
        continue
    ex = [d for d in by_full[tuple(p["lines"])] if d != p["id"]]
    fl = [d for d in by_first[p["lines"][0]] if d != p["id"] and d not in ex]
    p["duplicate_exact"] = ex or None
    p["duplicate_shared_first_line"] = fl or None

inputs = parse_inputs((D / F_INPUTS).read_text(encoding="utf-8-sig"))

by = lambda key: dict(sorted(collections.Counter(
    p[key] or "(unknown)" for p in poems).items(), key=lambda kv: -kv[1]))

dataset = {
    "dataset": "chandohasam-telugu-chandas-outputs",
    "description": (
        "Combined Telugu metrical-poetry (padyam) generation outputs and their prompt "
        "inputs, merged from three raw text dumps in Outputs/. Records are normalised to "
        "one schema; the per-record metrical and figure-of-speech analyses are preserved "
        "verbatim under .raw because their internal shape varies by batch."
    ),
    "combined_on": datetime.date.today().isoformat(),
    "provenance": [
        {"file": f, "sha256_16": sha(D / f), "bytes": (D / f).stat().st_size,
         "lines": len((D / f).read_text(encoding="utf-8-sig").splitlines()), "role": role}
        for f, role in [(F_INPUTS, "prompt inputs"),
                        (F_POEMS2, "generated poems (uniform schema)"),
                        (F_POEMS1, "generated poems (2 batches, mixed schemas)")]
    ],
    "summary": {
        "poem_count": len(poems),
        "input_chandas_count": len(inputs),
        "input_topic_count": sum(len(c["topics"]) for c in inputs),
        "by_batch": by("batch"),
        "by_chandassu": by("chandassu"),
        "by_chandassu_raw": dict(sorted(collections.Counter(
            p["chandassu_raw"] or "(unknown)" for p in poems).items())),
        "unmapped_chandassu_raw": sorted({
            p["chandassu_raw"] for p in poems if p["chandassu_raw"] and not p["chandassu_id"]}),
        "by_contributor": by("contributor"),
        "by_alankaram": by("alankaram"),
        "unmapped_alankaram_raw": sorted({
            p["alankaram_raw"] for p in poems if p["alankaram_raw"] and not p["alankaram_id"]}),
        "by_topic": by("topic"),
        "chandassu_x_alankaram": dict(sorted(collections.Counter(
            f'{p["chandassu_id"]}|{p["alankaram_id"]}' for p in poems
            if p["alankaram_id"]).items())),
        "with_alankara_analysis": sum(1 for p in poems if p["alankara_analysis"]),
        "with_chandassu_analysis": sum(1 for p in poems if p["chandassu_analysis"]),
        "analysis_shapes": dict(collections.Counter(
            p["chandassu_analysis"]["shape"] for p in poems if p["chandassu_analysis"])),
        "line_counts": dict(sorted(collections.Counter(p["line_count"] for p in poems).items())),
        "chandassu_source": by("chandassu_source"),
        "poems_with_exact_duplicate": sum(1 for p in poems if p["duplicate_exact"]),
        "poems_sharing_first_line_only": sum(
            1 for p in poems if p["duplicate_shared_first_line"]),
        "distinct_poem_texts": len({tuple(p["lines"]) for p in poems if p["lines"]}),
        "missing_meaning_telugu": sum(
            1 for p in poems if not p["meaning_telugu"] and not p["meaning_telugu_variants"]),
        "missing_meaning_english": sum(
            1 for p in poems if not p["meaning_english"] and not p["meaning_english_variants"]),
        "multi_reading_meanings": sum(
            1 for p in poems if p["meaning_telugu_variants"] or p["meaning_english_variants"]),
        "missing_title": sum(1 for p in poems if not p["title"]),
    },
    "prompt_inputs": {
        "description": "10 chandas x 4 topics x 3 input tiers (word / single_line / full_bhavam)",
        "chandas": inputs,
    },
    "batch_design": {
        "description": ("Declared design of the 108-poem batch, parsed from its preamble. "
                        "The chandas list is in generation order."),
        **batch_spec,
    },
    "poems": poems,
}

OUT.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(dataset["summary"], ensure_ascii=False, indent=2))
print("\nwrote", OUT, f"({OUT.stat().st_size/1e6:.2f} MB)")

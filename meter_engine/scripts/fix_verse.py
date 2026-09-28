#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_verse.py — the 2026-09-28 fixes to the verse, layout and labels of dataset/*.json, found by
the data-sanity metrics (data_sanity_metrics/data_sanity_metrics_report.md).

    python3 scripts/fix_verse.py --dry-run     # report what would change; write nothing
    python3 scripts/fix_verse.py               # apply (backups: dataset/backup/<file>.pre-verse-fix-2026-09-28)

In order:
  1. backslash artifact  a "\\" inside a Telugu word, always before న్ (నల్పునకు\\న్‌ → నల్పునకున్‌), a
                         conversion artifact of the Kaggle source; removed from the verse and the machine gloss.
  2. seesa layout        chandassu.json prints a seesa pāda on one line with " - " between its halves, then the
     (chandassu)         ettugeeti one pāda per line: 8 lines. Records that differ are, in turn:
                           a. separators written "X- Y" (the importer missed a ZWNJ before the dash): " - "
                           b. ettugeeti lines holding two pādas joined by " - ": split into two lines
                           c. a pāda without its separator, or pāda breaks lost in the source: re-segmented by
                              scansion. Every segmentation into 4 seesa pādas (two halves each) and 4 geeti pādas
                              that respects the printed line breaks and separators is tried; one is applied only
                              when it is the only one that scans, else the only one whose yati also holds, else
                              the only one of those whose half-lines break at word boundaries. Otherwise the
                              record is left as printed.
                         Records with gaps in the source ("... ...") are left as printed.
  3. labels (vemana)     a poem whose heuristic label does not scan and which the engine identifies gets that
                         metre (label_source "engine"; the old label is kept in metre_corrected). Ids are kept:
                         human_evals/ and meter_engine/reports/ cite them.
  4. typos               the TYPOS table: letters of other scripts in the verse, and prāsa typos where the other
                         three pādas fix the letter and the corrected word is attested in the corpora; and the
                         VARIANT_LINES table: a variant reading printed inside the verse.
  5. kuchimanchi-1220    లయగ్రాహి printed as four whole pādas (the engine reads either layout): allowed_lines [4, 8].

A record whose verse changes keeps its original lines and the reasons in `verse_corrected`; `line_count`
follows the new lines, and a chandassu record that now has its 8 lines gets complete = true.
bhagavatam.json is not touched here (its one verse typo is fixed textually; see dataset/CORRECTIONS.md).
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import shutil
import sys
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from chandohasam import analyze                                      # noqa: E402
from indic_meter_dawg import default_dawg, identify_text, scan       # noqa: E402
from indic_meter_dawg.identify import reading_options                # noqa: E402
from indic_meter_dawg.parser import segment                          # noqa: E402
from indic_meter_dawg.stanza import line_slots                       # noqa: E402
from indic_meter_dawg.walker import walk_options                     # noqa: E402
from scripts.corpus_run import NAME_MAP                              # noqa: E402
from scripts.label_with_engine import conventions                    # noqa: E402

DATASET = HERE.parent.parent / "dataset"
DATE = "2026-09-28"
BY = "meter_engine/scripts/fix_verse.py"
BACKUP_SUFFIX = f"pre-verse-fix-{DATE}"
FILES = ("vemana.json", "kuchimanchi_timmakavi.json", "chandassu.json")

BACKSLASH = re.compile(r"(?<=[ఀ-౿])\\(?=[ఀ-౿])")
SEP = re.compile(r"\s*-\s+|\s+-\s*")            # a separator: a dash with a space on at least one side
GAP = re.compile(r"\.\.\.|…")                   # a gap in the source text

TYPOS = [  # (file, id, from, to, why)
    ("vemana.json", "vemana-86-ఆ.", "మొసఁగుకన్నแ", "మొసఁగుకన్నఁ",
     "Thai แ typed for ఁ; line 1 has the same word మొసఁగుకన్నఁ"),
    ("vemana.json", "vemana-1162-ఆ.", "మఱiలింగ", "మఱిలింగ", "Latin i typed for the vowel sign ి"),
    ("kuchimanchi_timmakavi.json", "kuchimanchi-11", "త్క్రరు", "త్క్రతు",
     "prāsa: the other pādas have త (వ్రతముల్, శ్రిత, గతి); స|త్క్రతు is సత్క్రతు, as in క్రతు"),
    ("kuchimanchi_timmakavi.json", "kuchimanchi-56", "మినునొక్కప్పుడుఁ", "మిమునొక్కప్పుడుఁ",
     "prāsa: the other pādas have మ (గములై, తమి, కమఠ); మిము నొక్కప్పుడుఁ గొల్వనేరక, not worshipping you even once"),
    ("chandassu.json", "chandassu-naarayana-94-మ.", "నవలం బారిన", "ననలం బారిన",
     "prāsa: the other pādas have న (నిను, పెను, ల్చిన); తా ననలం బారిన భూతి, ash where the fire (అనలము) went out"),
]
VARIANT_LINES = [  # (file, id, line, why): a line that is not part of the poem, removed from the verse
    ("chandassu.json", "chandassu-sumathi-53-క.", "(రమణుల చనుమొనలమీఁద రాయని మేనున్‌)",
     "a variant reading of line 2, printed in parentheses in the source; the కందము has four pādas"),
]

DAWG = None
SEESA, GEETI = "seesamu", ("tetagiti", "ataveladi")
PADA, HALF, GEETI_PADA = (18, 34), (10, 18), (9, 20)     # syllables in a seesa pāda / its first half / a geeti pāda
MAX_PARSES = 256


def dawg():
    global DAWG
    if DAWG is None:
        DAWG = default_dawg()
    return DAWG


# ---------------------------------------------------------------- record edits
def set_verse(rec: dict, new: list, reason: str) -> bool:
    if new == rec["verse"]:
        return False
    vc = rec.get("verse_corrected")
    if vc is None:
        vc = rec["verse_corrected"] = {"from_verse": list(rec["verse"]), "date": DATE, "reasons": [],
                                       "corrected_by": BY}
    vc["reasons"].append(reason)
    rec["verse"] = new
    rec["line_count"] = len(new)
    return True


def fix_backslash(rec: dict, log: dict) -> None:
    n = sum(len(BACKSLASH.findall(l)) for l in rec["verse"])
    if not n:
        return
    after = collections.Counter(m.string[m.end():m.end() + 2] for l in rec["verse"] for m in BACKSLASH.finditer(l))
    set_verse(rec, [BACKSLASH.sub("", l) for l in rec["verse"]],
              f"removed {n} backslash(es) inside a word, a conversion artifact of the source (…కు\\న్‌ → …కున్‌)")
    k = 0
    for row in (rec.get("generated") or {}).get("prathipadartham") or []:
        for f in ("word", "split", "meaning", "model_word"):
            if isinstance(row.get(f), str) and BACKSLASH.search(row[f]):
                row[f] = BACKSLASH.sub("", row[f])
                k += 1
    if k:
        rec["verse_corrected"]["reasons"].append(f"the same backslash removed from {k} field(s) of generated.prathipadartham")
    log["backslash"].append({"id": rec["id"], "in_verse": n, "in_gloss": k, "followed_by": dict(after)})


# ---------------------------------------------------------------- seesa layout
def halves(line: str) -> list:
    return [h.strip() for h in SEP.split(line) if h.strip()]


def is_canonical(lines: list) -> bool:
    return (len(lines) == 8 and all(len(halves(l)) == 2 for l in lines[:4])
            and all(len(halves(l)) == 1 for l in lines[4:]))


def normalise(lines: list) -> tuple[list, list]:
    """Deterministic layout fixes (2a, 2b); returns (lines, reasons)."""
    out, why = list(lines), []
    for i in range(min(4, len(out))):
        hs = halves(out[i])
        if len(hs) == 2 and " - " not in out[i]:
            out[i] = f"{hs[0]} - {hs[1]}"
            why.append(f"line {i + 1}: separator written without the space before the dash, normalised to ' - '")
    if len(out) > 4 and all(len(halves(l)) == 2 for l in out[:4]) and any(len(halves(l)) > 1 for l in out[4:]):
        n = sum(len(halves(l)) > 1 for l in out[4:])
        out = out[:4] + [h for l in out[4:] for h in halves(l)]
        why.append(f"{n} ettugeeti line(s) holding two pādas joined by ' - ' split into one pāda per line")
    return out, why


def pieces_of(lines: list):
    """Text between hard boundaries (printed line breaks and separators): (text, syllables, continues),
    where `continues` marks a piece printed "X- - Y", a word running on across the separator."""
    out = []
    for l in lines:
        parts = [h.strip() for h in SEP.split(l)]
        for k, p in enumerate(parts):
            if not p:
                continue
            sc = scan(p)
            if len(sc) != 1 or not sc[0].syllables:
                return None
            continues = k + 2 < len(parts) and not parts[k + 1]
            out.append((p, sc[0].syllables, continues))
    return out


def span_text(piece, i: int, j: int) -> str:
    text, syls = piece[0], piece[1]
    a = syls[i].start if i > 0 else 0
    b = syls[j].start if j < len(syls) else len(text)
    return text[a:b].strip()


def unit_ok(texts: list, meter: str, slot: str, cache: dict) -> bool:
    key = (tuple(texts), meter, slot)
    if key not in cache:
        scans = [s for t in texts for s in scan(t)]
        opts = sum((tuple(o) for o in reading_options(scans, "compound")), ())
        w = walk_options(opts, dawg())
        cache[key] = (meter, slot) in w.accepted or (meter, slot) in w.padanta_accepted
    return cache[key]


def half_splits(texts: list, slot: str, cache: dict) -> set:
    """For the joined texts read as one seesa pāda: the length in aksharas of its first half (gaṇas 1-4)
    under every gaṇa parse; empty when the texts are not a seesa pāda."""
    key = (tuple(texts), slot)
    if key not in cache:
        scans = [s for t in texts for s in scan(t)]
        opts = sum((tuple(o) for o in reading_options(scans, "compound")), ())
        w = walk_options(opts, dawg())
        h, res = (SEESA, slot), set()
        if h in w.accepted or h in w.padanta_accepted:
            for seg in segment(SEESA, slot, w.pattern_for(h), dawg=dawg(), final_laghu_as_guru=True):
                if len(seg.segments) >= 4:
                    res.add(seg.segments[3].end)
        cache[key] = res
    return cache[key]


def pada_options(pieces: list, p: int, o: int, slot: str, cache: dict) -> list:
    """Seesa pādas starting at syllable o of piece p, as (half A span, half B span). The halves break after the
    4th gaṇa; a pāda may run into the next piece only when the separator falls exactly at that break."""
    out = []
    n = len(pieces[p][1])
    for e in range(o + PADA[0], min(o + PADA[1], n) + 1):
        for k in half_splits([span_text(pieces[p], o, e)], slot, cache):
            if 0 < k < e - o:
                out.append(((p, o, o + k), (p, o + k, e)))
    if p + 1 < len(pieces) and HALF[0] <= n - o <= HALF[1]:
        m = len(pieces[p + 1][1])
        for e in range(PADA[0] - HALF[1], min(PADA[1] - HALF[0], m) + 1):
            if n - o in half_splits([span_text(pieces[p], o, n), span_text(pieces[p + 1], 0, e)], slot, cache):
                out.append(((p, o, n), (p + 1, 0, e)))
    return out


def segmentations(pieces: list, geeti: str) -> list:
    """Every segmentation of the pieces into 4 seesa pādas (two halves each) and 4 geeti pādas."""
    s_slots = line_slots(dawg().spec(SEESA), 4)
    g_slots = line_slots(dawg().spec(geeti), 4)
    out, cache, visits = [], {}, [0]

    def dfs(p, o, u, units):
        if len(out) >= MAX_PARSES or visits[0] > 400_000:
            return
        visits[0] += 1
        if p < len(pieces) and o == len(pieces[p][1]):
            p, o = p + 1, 0
        if u == 8:
            if p == len(pieces):
                out.append(list(units))
            return
        if p == len(pieces):
            return
        if u < 4:
            for a, b in pada_options(pieces, p, o, s_slots[u], cache):
                dfs(b[0], b[2], u + 1, units + [a, b])
            return
        n = len(pieces[p][1])
        for e in range(o + GEETI_PADA[0], min(o + GEETI_PADA[1], n) + 1):
            if unit_ok([span_text(pieces[p], o, e)], geeti, g_slots[u - 4], cache):
                dfs(p, e, u + 1, units + [(p, o, e)])

    dfs(0, 0, 0, [])
    return out


def render(pieces: list, units: list) -> tuple[list, bool]:
    """The 8 printed lines, and whether every half-line break falls at a word boundary of the source.
    A break inside a word is printed "X- - Y", as chandassu.json prints a word running across the halves."""
    texts = [span_text(pieces[p], i, j) for p, i, j in units]
    at_space, lines = True, []
    for k in range(0, 8, 2):
        (pa, ia, ja), (pb, ib, jb) = units[k], units[k + 1]
        if pa == pb:                                      # both halves from one piece: what separated them?
            text, syls = pieces[pa][0], pieces[pa][1]
            gap = text[syls[ja - 1].end:syls[ib].start]
            inside_word = not any(c.isspace() or c == "-" for c in gap)
        else:
            inside_word = pieces[pa][2]
        at_space &= not inside_word
        a = texts[k] + ("-" if inside_word and not texts[k].endswith("-") else "")
        lines.append(f"{a} - {texts[k + 1]}")
    return lines + texts[8:], at_space


def verdict(lines8: list) -> tuple[bool, bool, str]:
    """(identified as seesa + a geeti trailer, yati holds under relaxed, trailer)."""
    half = [h for l in lines8[:4] for h in halves(l)] + lines8[4:]
    ident = identify_text(half)
    cand = next((c for c in ident.candidates if c.meter == SEESA and c.trailer is not None), None)
    if cand is None:
        return False, False, ""
    a = analyze(half, profile="relaxed", yati_sandhi="hypothesis", meter=cand.meter, identification=ident)
    return True, a.yati_matched, cand.trailer.meter


def resegment(item):
    rid, lines = item
    if any(GAP.search(l) for l in lines):
        return rid, {"status": "gap in the source"}
    pieces = pieces_of(lines)
    if pieces is None:
        return rid, {"status": "unscannable piece"}
    found = []
    for g in GEETI:
        for units in segmentations(pieces, g):
            new, at_space = render(pieces, units)
            if new not in [f["lines"] for f in found]:
                found.append({"lines": new, "at_space": at_space})
    if not found:
        return rid, {"status": "no segmentation scans"}
    for f in found:
        f["identified"], f["yati"], f["trailer"] = verdict(f["lines"])
    ok = [f for f in found if f["identified"]]
    step = None
    if len(ok) == 1:
        pick, step = ok[0], "the only segmentation that scans"
    else:
        y = [f for f in ok if f["yati"]]
        if len(y) == 1:
            pick, step = y[0], f"the only one of {len(ok)} scanning segmentations whose yati holds"
        else:
            pool = y or ok
            s = [f for f in pool if f["at_space"]]
            if len(s) == 1:
                pick, step = s[0], (f"the only one of {len(pool)} scanning segmentations"
                                    f"{' with yati' if y else ''} whose half-lines break at word boundaries")
            else:
                return rid, {"status": f"ambiguous: {len(ok)} scanning segmentations", "n_candidates": len(found)}
    return rid, {"status": "resegmented", "lines": pick["lines"], "why": step, "yati": pick["yati"],
                 "trailer": pick["trailer"], "n_candidates": len(found), "n_scanning": len(ok)}


def fix_seesa_layout(records: list, workers: int, log: dict) -> None:
    todo = []
    for r in records:
        if r.get("metre_roman") != "seesamu":
            continue
        lines, why = normalise(r["verse"])
        if is_canonical(lines):
            if why:
                set_verse(r, lines, "; ".join(why))
                r["complete"] = True
                log["layout_normalised"].append({"id": r["id"], "why": why})
            continue
        todo.append((r["id"], list(r["verse"])))
    by_id = {r["id"]: r for r in records}
    with Pool(workers) as pool:
        for rid, res in pool.imap_unordered(resegment, todo, chunksize=1):
            if res["status"] == "resegmented":
                r = by_id[rid]
                set_verse(r, res["lines"], f"re-segmented by scansion into 4 seesa pādas and 4 geeti pādas "
                                           f"({res['trailer']}): {res['why']}")
                r["complete"] = True
            log["resegment"].append({"id": rid, **{k: v for k, v in res.items()}})


# ---------------------------------------------------------------- labels
def _identify(item):
    rid, lines, target = item
    ident = identify_text(lines)
    fits = any(c.meter == target or c.is_variant_of == target for c in ident.candidates)
    best = (ident.best.is_variant_of or ident.best.meter) if ident.identified else None
    return rid, fits, best


def relabel(records: list, conv: dict, log: dict, workers: int = 16) -> None:
    corpus_name = {engine: corpus for corpus, engine in NAME_MAP.items()}
    items = []
    for r in records:
        if r.get("form") != "verse" or not r.get("metre_roman"):
            continue
        lines = [h for l in r["verse"] for h in halves(l)] if r["metre_roman"] == "seesamu" else r["verse"]
        items.append((r["id"], lines, NAME_MAP.get(r["metre_roman"], r["metre_roman"])))
    with Pool(workers) as pool:
        found = {rid: (fits, best) for rid, fits, best in pool.map(_identify, items, chunksize=8)}
    for r in records:
        fits, name = found.get(r["id"], (True, None))
        if fits or name is None:
            continue
        roman = corpus_name.get(name, name)
        code, metre, expected, allowed = conv.get(roman, (None, dawg().spec(name).name_te, None, ()))
        r["metre_corrected"] = {"from_metre_code": r["metre_code"], "from_metre": r["metre"],
                                "from_metre_roman": r["metre_roman"], "from_label_source": r.get("label_source"),
                                "date": DATE,
                                "reason": f"the lines scan as {metre} (meter_engine identify_text); "
                                          f"{r['metre']} does not fit",
                                "corrected_by": BY}
        log["relabel"].append({"id": r["id"], "from": r["metre_roman"], "to": roman})
        r.update(metre_code=code, metre=metre, metre_roman=roman, expected_lines=expected,
                 allowed_lines=list(allowed) if allowed else None, label_source="engine")


# ---------------------------------------------------------------- typos, layagrahi
def fix_typos(name: str, records: list, log: dict) -> None:
    by_id = {r["id"]: r for r in records}
    for f, rid, old, new, why in TYPOS:
        if f != name:
            continue
        r = by_id[rid]
        hits = sum(l.count(old) for l in r["verse"])
        if hits == 0 and any(new in l for l in r["verse"]):
            continue                                      # already fixed
        if hits != 1:
            raise SystemExit(f"{rid}: expected one {old!r} in the verse, found {hits}")
        set_verse(r, [l.replace(old, new) for l in r["verse"]], f"typo {old} → {new}: {why}")
        log["typos"].append({"id": rid, "from": old, "to": new})
    for f, rid, line, why in VARIANT_LINES:
        if f == name and line in by_id[rid]["verse"]:
            r = by_id[rid]
            set_verse(r, [l for l in r["verse"] if l != line], f"line {line} removed: {why}")
            if r.get("expected_lines") == len(r["verse"]):
                r["complete"] = True
            log["variant_lines"].append({"id": rid, "line": line})


def fix_layagrahi(records: list, log: dict) -> None:
    for r in records:
        if r["id"] == "kuchimanchi-1220" and r.get("allowed_lines") == [8]:
            r["allowed_lines"] = [4, 8]
            log["allowed_lines"].append({"id": r["id"], "allowed_lines": [4, 8]})


# ---------------------------------------------------------------- main
CHANGEABLE = {"verse", "line_count", "complete", "verse_corrected", "metre_code", "metre", "metre_roman",
              "expected_lines", "allowed_lines", "label_source", "metre_corrected", "generated"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--log", type=Path, help="write the full change log (JSON) here")
    ns = ap.parse_args(argv)
    conv = conventions(DATASET)
    log = collections.defaultdict(list)
    new_text = {}
    for name in FILES:
        path = DATASET / name
        text = path.read_text(encoding="utf-8")
        records = json.loads(text)
        if json.dumps(records, ensure_ascii=False, indent=1) != text:
            raise SystemExit(f"{name}: the JSON round trip is not byte-identical; refusing to rewrite it")
        before = json.loads(text)
        for r in records:
            fix_backslash(r, log)
        if name == "chandassu.json":
            fix_seesa_layout(records, ns.workers, log)
        if name == "vemana.json":
            relabel(records, conv, log)
        fix_typos(name, records, log)
        fix_layagrahi(records, log)
        changed = collections.Counter()
        for b, a in zip(before, records):
            keys = {k for k in set(a) | set(b) if a.get(k) != b.get(k)}
            if keys - CHANGEABLE:
                raise SystemExit(f"{name} {a['id']}: unexpected change in {sorted(keys - CHANGEABLE)}")
            if b.get("generated") != a.get("generated") and not any(e["id"] == a["id"] and e["in_gloss"]
                                                                    for e in log["backslash"]):
                raise SystemExit(f"{name} {a['id']}: generated changed without a gloss fix")
            changed.update(keys)
        log["summary"].append({"file": name, "records_changed": sum(a != b for a, b in zip(before, records)),
                               "fields": dict(changed)})
        new_text[name] = json.dumps(records, ensure_ascii=False, indent=1)
    report = {k: v for k, v in log.items()}
    status = collections.Counter(e["status"] for e in log["resegment"])
    print(json.dumps({"summary": log["summary"], "backslash_records": len(log["backslash"]),
                      "backslash_followed_by": sum((collections.Counter(e["followed_by"]) for e in log["backslash"]),
                                                   collections.Counter()),
                      "layout_normalised": len(log["layout_normalised"]), "resegment": dict(status),
                      "relabel": dict(collections.Counter(f"{e['from']} → {e['to']}" for e in log["relabel"])),
                      "typos": log["typos"], "allowed_lines": log["allowed_lines"]}, ensure_ascii=False, indent=1))
    if ns.log:
        ns.log.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    if ns.dry_run:
        return 0
    backup = DATASET / "backup"
    for name, text in new_text.items():
        src = DATASET / name
        dst = backup / f"{name}.{BACKUP_SUFFIX}"
        if not dst.exists():
            shutil.copy2(src, dst)
        src.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

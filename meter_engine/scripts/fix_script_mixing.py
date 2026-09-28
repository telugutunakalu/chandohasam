# -*- coding: utf-8 -*-
"""
Remove letters of other scripts from the machine annotation (``generated``) of
dataset/vemana.json, kuchimanchi_timmakavi.json and chandassu.json, the way
dataset/CORRECTIONS.md documents: only the fixed strings change (every other
byte of each file is untouched), each change is kept in the record's
``generated.script_fixes`` list, and a section is appended to CORRECTIONS.md.

Text fields checked: ``bhavam``, and each prathipadartham row's ``word``,
``split``, ``meaning`` and ``component_meanings`` values. Metadata (``model``,
``run``, ``split_source``, ``problems``) and the model's original spelling
(``model_word``) are left alone.

A word (maximal run of letters) containing a foreign letter is fixed by the
first rule that applies:

  1. manual   -- a row of dataset/script_fixes.tsv (file, id, field, from, to),
                 applied to the field as a substring replacement;
  2. verse    -- ``word``/``split`` fields: the transliterated word (below) is a
                 word of the poem; for ``word`` only, also the one poem word it
                 becomes when each foreign run of k letters is read as k-1..k+1
                 Telugu characters;
  3. translit -- every foreign letter has a Telugu letter of the same Unicode
                 name (long e/o kept long), and the resulting word is attested
                 elsewhere in the repo's corpora (at least 5 times when the word
                 has no Telugu letter at all, i.e. is a word of another
                 language). A nasal+stop cluster that Tamil spells in full
                 (ம்ப) is written with an anusvara (ంప); either spelling counts
                 as attestation.
                 The wildcard reading of rule 2 needs at least two Telugu letters
                 in the word.

Anything still containing a foreign letter is listed, and nothing is written.

    python3 meter_engine/scripts/fix_script_mixing.py                 # dry run: report
    python3 meter_engine/scripts/fix_script_mixing.py --todo T.tsv    # also write unresolved rows to fill in
    python3 meter_engine/scripts/fix_script_mixing.py --apply
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import re
import shutil
import sys
import unicodedata as ud
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dataset"
FILES = ["vemana.json", "kuchimanchi_timmakavi.json", "chandassu.json"]
MANUAL = DATA / "script_fixes.tsv"
LOG = DATA / "CORRECTIONS.md"
BACKUP = DATA / "backup"

INDIC = ("DEVANAGARI", "BENGALI", "GURMUKHI", "GUJARATI", "ORIYA", "TAMIL", "KANNADA", "MALAYALAM")
# letters with no Telugu letter of the same name
SPECIAL = {"TAMIL LETTER NNNA": "న", "TAMIL LETTER LLLA": "ళ", "BENGALI LETTER KHANDA TA": "త్",
           "BENGALI LETTER YYA": "య", "DEVANAGARI SIGN NUKTA": "", "BENGALI SIGN NUKTA": "",
           "MALAYALAM LETTER CHILLU L": "ల్", "MALAYALAM LETTER CHILLU N": "న్", "MALAYALAM LETTER CHILLU RR": "ర్",
           "MALAYALAM LETTER CHILLU LL": "ళ్", "MALAYALAM LETTER CHILLU NN": "ణ్"}


def is_telugu(c: str) -> bool:
    return "ఀ" <= c <= "౿"


def is_letter(c: str) -> bool:
    return ud.category(c)[0] in "LM" or c in "‌‍"


def is_foreign(c: str) -> bool:
    return ud.category(c)[0] in "LM" and not is_telugu(c)


def has_foreign(s: str) -> bool:
    return any(is_foreign(c) for c in s)


def words(s: str) -> list[str]:
    """Maximal runs of letters/marks (ZWJ/ZWNJ included)."""
    out, cur = [], []
    for c in s:
        if is_letter(c):
            cur.append(c)
        elif cur:
            out.append("".join(cur)); cur = []
    if cur:
        out.append("".join(cur))
    return out


# scripts whose plain E/O are long (ē/ō): Telugu writes those with EE/OO; their SHORT E/O are Telugu E/O
LONG_EO = ("DEVANAGARI", "BENGALI", "GURMUKHI", "GUJARATI", "ORIYA")
EO = {" LETTER E": " LETTER EE", " LETTER O": " LETTER OO", " VOWEL SIGN E": " VOWEL SIGN EE",
      " VOWEL SIGN O": " VOWEL SIGN OO", " LETTER SHORT E": " LETTER E", " LETTER SHORT O": " LETTER O",
      " VOWEL SIGN SHORT E": " VOWEL SIGN E", " VOWEL SIGN SHORT O": " VOWEL SIGN O"}


def to_telugu(c: str) -> str | None:
    """The Telugu letter with the same Unicode name (long e/o kept long), or None."""
    name = ud.name(c, "")
    if name in SPECIAL:
        return SPECIAL[name]
    script = name.split(" ", 1)[0]
    if script not in INDIC:
        return None
    rest = name[len(script):]
    if script in LONG_EO:
        rest = EO.get(rest, rest)
    try:
        return ud.lookup("TELUGU" + rest)
    except KeyError:
        return None


def transliterate(w: str) -> str | None:
    out = []
    for c in w:
        t = to_telugu(c) if is_foreign(c) else c
        if t is None:
            return None
        out.append(t)
    return ud.normalize("NFC", "".join(out))


# Tamil writes a nasal before a stop of its class in full (ம்ப, ண்ட); Telugu writes an anusvara (ంప, ండ)
_NASAL_STOP = re.compile("ఙ్(?=[కఖగఘ])|ఞ్(?=[చఛజఝ])|ణ్(?=[టఠడఢ])|న్(?=[తథదధ])|మ్(?=[పఫబభ])")


def anusvara_spelling(t: str) -> str:
    """``t`` with each nasal+stop cluster written the Telugu way, with an anusvara."""
    return _NASAL_STOP.sub("ం", t)


# ------------------------------------------------------------------ fields of one annotation
def text_fields(g: dict):
    """(path, string) of every text field of a ``generated`` object."""
    if isinstance(g.get("bhavam"), str):
        yield "bhavam", g["bhavam"]
    for i, p in enumerate(g.get("prathipadartham") or []):
        for k in ("word", "split", "meaning"):
            if isinstance(p.get(k), str):
                yield f"prathipadartham[{i}].{k}", p[k]
        for ck, cv in (p.get("component_meanings") or {}).items():
            if isinstance(cv, str):
                yield f"prathipadartham[{i}].component_meanings[{ck}]", cv


_PATH = re.compile(r"prathipadartham\[(\d+)\]\.(word|split|meaning|component_meanings\[(.*)\])$")


def set_field(g: dict, path: str, value: str) -> None:
    if path == "bhavam":
        g["bhavam"] = value
        return
    m = _PATH.match(path)
    row = g["prathipadartham"][int(m.group(1))]
    if m.group(3) is not None:
        row["component_meanings"][m.group(3)] = value
    else:
        row[m.group(2)] = value


# ------------------------------------------------------------------ evidence
def lexicon() -> collections.Counter:
    """Telugu words attested anywhere in the repo's corpora (foreign-free words only)."""
    lex = collections.Counter()
    def add(s):
        if isinstance(s, str):
            lex.update(w for w in words(ud.normalize("NFC", s)) if not has_foreign(w))
    for name in FILES + ["bhagavatam.json"]:
        for r in json.loads((DATA / name).read_text(encoding="utf-8")):
            for line in r.get("verse") or []:
                add(line)
            add(r.get("teeka")); add(r.get("bhavam"))
            for p in r.get("teeka_pairs") or []:
                add(p.get("word")); add(p.get("meaning"))
            if r.get("generated"):
                for _, s in text_fields(r["generated"]):
                    add(s)
    return lex


def verse_match(w: str, verse_words: set[str], headword: bool) -> str | None:
    """The poem word ``w`` stands for: its transliteration, if that is a poem word; for a headword
    (spelled as in the poem), also the one poem word it becomes when each foreign run of k letters is
    read as k-1..k+1 Telugu characters. Split parts are base forms, so they only take the first test."""
    t = transliterate(w)
    if t and t in verse_words:
        return t
    if not headword or sum(is_telugu(c) for c in w) < 2:
        return None
    pat, i = [], 0
    while i < len(w):
        if is_foreign(w[i]):
            j = i
            while j < len(w) and is_foreign(w[j]):
                j += 1
            k = j - i
            pat.append(f"[ఀ-౿‌‍]{{{max(1, k - 1)},{k + 1}}}")
            i = j
        else:
            pat.append(re.escape(w[i])); i += 1
    rx = re.compile("".join(pat))
    hits = {v for v in verse_words if rx.fullmatch(v) and abs(len(v) - len(w)) <= 2}
    return hits.pop() if len(hits) == 1 else None


def load_manual(path: Path) -> dict[tuple[str, str, str], list[tuple[str, str]]]:
    out = collections.defaultdict(list)
    if path.exists():
        with open(path, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                out[(row["file"], row["id"], row["field"])].append((row["from"], row["to"]))
    return out


# ------------------------------------------------------------------ the fix
def fix_string(s: str, field: str, verse_words: set[str], lex, manual_rows) -> tuple[str, list[dict]]:
    changes = []
    for frm, to in manual_rows:
        if frm not in s:
            raise ValueError(f"manual row not found in {field}: {frm!r}")
        s = s.replace(frm, to)
        if to == "":
            s = re.sub(r"[ \t]{2,}", " ", s).strip()
        changes.append({"field": field, "from": frm, "to": to, "rule": "manual"})
    for w in dict.fromkeys(w for w in words(s) if has_foreign(w)):
        new, rule = None, None
        if field.endswith((".word", ".split")):
            new = verse_match(w, verse_words, headword=field.endswith(".word"))
            rule = "verse" if new else None
        if new is None:
            t = transliterate(w)
            if t:
                a = anusvara_spelling(t)
                seen = lex[t] + (lex[a] if a != t else 0)       # either spelling counts as evidence
                # a word with no Telugu letter at all is a word of another language: ask for more evidence
                if seen >= (1 if any(is_telugu(c) for c in w) else 5):
                    new, rule = a, "translit"
        if new is not None:
            s = s.replace(w, new)
            changes.append({"field": field, "from": w, "to": new, "rule": rule})
    return s, changes


def run(apply: bool, todo: Path | None, manual_path: Path) -> int:
    lex = lexicon()
    manual = load_manual(manual_path)
    used = set()
    stats = collections.Counter()
    unresolved = []
    out_text = {}
    for name in FILES:
        raw = (DATA / name).read_text(encoding="utf-8")
        data = json.loads(raw)
        assert json.dumps(data, ensure_ascii=False, indent=1) == raw, f"{name}: round trip is not byte-identical"
        for r in data:
            g = r.get("generated")
            if not g:
                continue
            verse_words = {w for line in r.get("verse") or [] for w in words(ud.normalize("NFC", line))}
            done = {(f["field"], f["from"], f["to"]) for f in g.get("script_fixes", [])}   # applied on an earlier run
            fixes = []
            for field, s in list(text_fields(g)):
                key = (name, r["id"], field)
                if key in manual:
                    used.add(key)
                rows = [(frm, to) for frm, to in manual.get(key, []) if (field, frm, to) not in done]
                if not has_foreign(s) and not rows:
                    continue
                new, changes = fix_string(s, field, verse_words, lex, rows)
                for w in words(new):
                    if has_foreign(w):
                        unresolved.append({"file": name, "id": r["id"], "field": field, "from": w,
                                           "to": transliterate(w) or "", "context": s})
                if changes:
                    set_field(g, field, new)
                    fixes += changes
                    stats.update((name, c["rule"]) for c in changes)
            if fixes:
                g.setdefault("script_fixes", []).extend(fixes)
                stats[(name, "records")] += 1
        out_text[name] = json.dumps(data, ensure_ascii=False, indent=1)

    stale = set(manual) - used
    for name in FILES:
        print(f"{name}: records fixed {stats[(name, 'records')]}; words by rule: manual {stats[(name, 'manual')]}, "
              f"verse {stats[(name, 'verse')]}, translit {stats[(name, 'translit')]}")
    print(f"unresolved words: {len(unresolved)}; manual rows unused: {len(stale)}")
    if todo:
        with open(todo, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, ["file", "id", "field", "from", "to", "context"], delimiter="\t")
            w.writeheader(); w.writerows(unresolved)
        print(f"wrote {todo}")
    if stale:
        for k in sorted(stale)[:20]:
            print("  unused manual row:", k)
    if not apply:
        return 0
    if unresolved or stale:
        print("not written: resolve every word (and drop unused manual rows) first")
        return 1
    BACKUP.mkdir(exist_ok=True)
    date = dt.date.today().isoformat()
    for name in FILES:
        dst = BACKUP / f"{name}.pre-script-fix-{date}"
        if not dst.exists():
            shutil.copy2(DATA / name, dst)
        (DATA / name).write_text(out_text[name], encoding="utf-8")
        for r in json.loads(out_text[name]):                      # nothing foreign left
            if r.get("generated"):
                assert not any(has_foreign(s) for _, s in text_fields(r["generated"])), r["id"]
    log(stats, date)
    return 0


def log(stats: collections.Counter, date: str) -> None:
    rows = ["", f"## {date} — letters of other scripts removed from the machine annotation", "",
            "The `generated` gloss and bhavam of some poems had letters of other scripts inside Telugu words",
            "(`సాధಿಸಿ`, `ఒక్కటாகி`, `విतानములు`), stray characters of unrelated scripts (`ఎ红నని`) and English",
            "glosses. Fixed by `meter_engine/scripts/fix_script_mixing.py`, in this order: the manual table",
            "`dataset/script_fixes.tsv`; for `word`/`split`, the one poem word the token matches; otherwise the",
            "Telugu letter of the same Unicode name, kept only when the resulting word is attested elsewhere in the",
            "corpora. Only the fixed strings changed; every change (field, from, to, rule) is kept in the record's",
            "`generated.script_fixes`. Backups: `dataset/backup/<file>.pre-script-fix-" + date + "`.", "",
            "The manual rows were decided one by one, in context, by Claude (AI assistant): words of another",
            "language translated into Telugu, glitch characters read from context, English glosses dropped, leaked",
            "`<bos>`/`<br>` markup removed, headwords set to the poem's own spelling. Nobody has reviewed them yet;",
            "`rule: \"manual\"` in `script_fixes` marks them.", "",
            "| file | records fixed | manual | verse | translit |", "|---|---|---|---|---|"]
    for name in FILES:
        rows.append(f"| `{name}` | {stats[(name, 'records')]} | {stats[(name, 'manual')]} | "
                    f"{stats[(name, 'verse')]} | {stats[(name, 'translit')]} |")
    rows.append("")
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write("\n".join(rows))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="write the files (default: dry run)")
    ap.add_argument("--todo", type=Path, help="write the unresolved words to this TSV")
    ap.add_argument("--manual", type=Path, default=MANUAL, help="manual fixes table (default: dataset/script_fixes.tsv)")
    a = ap.parse_args(argv)
    return run(a.apply, a.todo, a.manual)


if __name__ == "__main__":
    sys.exit(main())

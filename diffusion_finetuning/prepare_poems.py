"""Build the stage-2 poem corpus: token files for fine-tuning (E2) and held-out evaluation (E1).

    ../.venv/bin/python prepare_poems.py [--workers 12]

Sources, read in place (padyarchana_exports/ is never committed):
  padyarchana_exports/padyarchana_poems_v3.json   382,052 poems, one JSON object per line
  dataset/{bhagavatam,vemana,kuchimanchi_timmakavi,chandassu}.json   the verse records

Steps:
  1. Read every verse poem and normalise it as stage 1 normalised its documents (data_prep.cleaning).
     Prose is skipped: Padyarchana's వచనము and గద్యము, and dataset records whose form is not verse.
     A Bhāgavatam seesa parent and its child (the ettugeeti) are joined into one poem.
  2. Drop exact duplicates: same Telugu letters, ignoring spacing, punctuation, ZWJ/ZWNJ and ఁ.
     The dataset/ copy wins: it carries the 2026-09-28 corrections and a checked metre label.
  3. Group poems that share a line: any line of at least MIN_LINK Telugu letters that occurs in two
     poems joins their groups (union-find). This keeps a makuta, a samasya, a refrain and the
     variants of one poem together.
  4. Split by group. val and test take whole groups, by a stable hash of the group; groups of more
     than MAX_HELDOUT_GROUP poems stay in train. So no line of a held-out poem occurs in a training poem.
  5. Tokenize with the frozen stage-1 tokenizer, each text as <bos> … <eos>:
       data/tokens/poems/{train,val,test}.bin   the poems
       data/tokens/bhavam/{val,test}.bin        the bhavams of the held-out poems: modern prose about
                                                the same poems, the paired reference of E1
  6. Write data/poems_index.jsonl (one row per poem), data/tokens/meta.json and data/report.md.

Every output is under data/, which is gitignored.
"""
from __future__ import annotations

import argparse
import collections
import json
import time
import zlib
from multiprocessing import Pool

import numpy as np

from common import DATA, DATASET, INDEX, PADYARCHANA, TOKENS, canonical, tokenizer
from data_prep.cleaning import normalize                       # stage-1 normalisation (common puts it on the path)

PROSE_METRES = {"వచనము", "గద్యము"}
DATASET_FILES = ("bhagavatam.json", "vemana.json", "kuchimanchi_timmakavi.json", "chandassu.json")
MIN_LINK = 10                 # Telugu letters a shared line needs to join two poems' groups
MAX_HELDOUT_GROUP = 200       # larger groups (a whole śataka's makuta, a popular samasya) stay in train
HELDOUT = (("test", 0.01), ("val", 0.01))


def stream_padyarchana(path):
    """v3 is a JSON array written one object per line."""
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip().rstrip(",")
            if line not in ("[", "]", ""):
                yield json.loads(line)


def bhavam_of(record: dict) -> str:
    for part in ("editorial", "generated"):
        b = (record.get(part) or {}).get("bhavam")
        if b:
            return b
    return record.get("bhavam") or ""


def dataset_poems():
    for name in DATASET_FILES:
        recs = json.loads((DATASET / name).read_text(encoding="utf-8"))
        by_id = {r["id"]: r for r in recs}
        for r in recs:
            if (r.get("form") or "verse") != "verse" or r.get("parent_id"):
                continue                                         # prose, or a child joined to its parent below
            verse, bhavam = list(r.get("verse") or []), bhavam_of(r)
            child = by_id.get(r.get("child_id")) if r.get("child_id") else None
            if child:
                verse += child.get("verse") or []
                bhavam = bhavam_of(child)
            yield {"key": f"dataset/{name[:-5]}:{r['id']}", "origin": f"dataset/{name}", "id": r["id"],
                   "text": "\n".join(verse), "bhavam": bhavam, "metre": r.get("metre"),
                   "metre_source": r.get("label_source") or "edition", "poet": r.get("author"),
                   "copyright_protected": None, "source": r.get("skandha") or name[:-5],
                   "literary_form": None, "rating": None}


def padyarchana_poems():
    for p in stream_padyarchana(PADYARCHANA):
        metre = (p.get("meter") or {}).get("name")
        if metre in PROSE_METRES:
            continue
        poet = p.get("poet") or {}
        yield {"key": f"padyarchana:{p['id']}", "origin": "padyarchana_v3", "id": p["id"], "text": p.get("text") or "",
               "bhavam": bhavam_of(p), "metre": metre, "metre_source": "padyarchana", "poet": poet.get("name"),
               "copyright_protected": poet.get("copyright_protected"), "source": p.get("source"),
               "literary_form": p.get("literary_form"), "rating": p.get("rating")}


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, a: int) -> int:
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[max(ra, rb)] = min(ra, rb)


_TOK = None


def _encode(texts: tuple[str, str]) -> tuple[list[int], list[int]]:
    global _TOK
    if _TOK is None:
        _TOK = tokenizer()
    verse, bhavam = texts
    return (_TOK.encode(verse, add_bos=True, add_eos=True),
            _TOK.encode(bhavam, add_bos=True, add_eos=True) if bhavam else [])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args(argv)
    t0 = time.time()
    funnel = collections.Counter()

    # 1-2. read, normalise, drop exact duplicates (dataset/ first, so its copy wins)
    poems, seen = [], {}
    for source in (dataset_poems, padyarchana_poems):
        for p in source():
            funnel[f"read/{p['origin']}"] += 1
            p["text"] = normalize(p["text"])
            p["bhavam"] = normalize(p["bhavam"]) if p["bhavam"] else ""
            canon = canonical(p["text"])
            if not canon:
                funnel["dropped/empty"] += 1
                continue
            if canon in seen:
                funnel[f"dropped/duplicate/{p['origin']}"] += 1
                seen[canon]["duplicates"].append(p["key"])
                continue
            p["duplicates"] = []
            seen[canon] = p
            poems.append(p)
    del seen
    print(f"{len(poems):,} unique poems ({time.time() - t0:.0f} s)", flush=True)

    # 3. groups of poems that share a line
    uf, line_owner, link_lines = UnionFind(len(poems)), {}, collections.Counter()
    for i, p in enumerate(poems):
        for line in {canonical(l) for l in p["text"].split("\n")}:
            if len(line) < MIN_LINK:
                continue
            j = line_owner.setdefault(line, i)
            if j != i:
                uf.union(i, j)
                link_lines[line] += 1
    groups = collections.defaultdict(list)
    for i in range(len(poems)):
        groups[uf.find(i)].append(i)
    sizes = sorted((len(v) for v in groups.values()), reverse=True)
    print(f"{len(groups):,} groups; largest {sizes[:10]} ({time.time() - t0:.0f} s)", flush=True)

    # 4. split by group
    for root, members in groups.items():
        split = "train"
        if len(members) <= MAX_HELDOUT_GROUP:
            h = zlib.crc32(poems[root]["key"].encode()) / 2**32
            edge = 0.0
            for name, frac in HELDOUT:
                if edge <= h < edge + frac:
                    split = name
                edge += frac
        for i in members:
            poems[i]["split"], poems[i]["group"] = split, poems[root]["key"]

    # 5. tokenize
    with Pool(args.workers) as pool:
        encoded = pool.map(_encode, [(p["text"], p["bhavam"] if p["split"] != "train" else "") for p in poems],
                           chunksize=256)
    print(f"tokenized ({time.time() - t0:.0f} s)", flush=True)
    for name in ("poems", "bhavam"):
        (TOKENS / name).mkdir(parents=True, exist_ok=True)
    offsets = collections.Counter()
    parts = collections.defaultdict(list)
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    with INDEX.open("w", encoding="utf-8") as idx:
        for p, (ids, bids) in zip(poems, encoded):
            s = p["split"]
            row = {k: p[k] for k in ("key", "origin", "id", "split", "group", "metre", "metre_source", "poet",
                                     "copyright_protected", "source", "literary_form", "rating", "duplicates")}
            row.update(n_lines=p["text"].count("\n") + 1, n_tokens=len(ids), offset=offsets[("poems", s)])
            parts[("poems", s)].append(np.asarray(ids, dtype=np.uint16))
            offsets[("poems", s)] += len(ids)
            if bids:
                row.update(bhavam_offset=offsets[("bhavam", s)], bhavam_tokens=len(bids))
                parts[("bhavam", s)].append(np.asarray(bids, dtype=np.uint16))
                offsets[("bhavam", s)] += len(bids)
            idx.write(json.dumps(row, ensure_ascii=False) + "\n")
    for (name, s), arrays in parts.items():
        np.concatenate(arrays).tofile(TOKENS / name / f"{s}.bin")

    # 6. meta and report
    split_poems = collections.Counter(p["split"] for p in poems)
    held_groups = collections.Counter(p["split"] for root, m in groups.items() for p in [poems[root]])
    meta = {
        "built": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sources": {"padyarchana_v3": str(PADYARCHANA.name), "padyarchana_v3_bytes": PADYARCHANA.stat().st_size,
                    "dataset": list(DATASET_FILES)},
        "settings": {"prose_metres_skipped": sorted(PROSE_METRES), "min_link_letters": MIN_LINK,
                     "max_heldout_group": MAX_HELDOUT_GROUP, "heldout": dict(HELDOUT)},
        "funnel": dict(funnel),
        "poems": dict(split_poems),
        "groups": {"total": len(groups), "by_split": dict(held_groups), "largest": sizes[:20]},
        "tokens": {f"{name}/{s}": int(n) for (name, s), n in offsets.items()},
        "tokenizer": "diffusion_pretraining/tokenizer/telugu_alldomain.tokenizer.json (sha256 200c814d…)",
    }
    (TOKENS / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(poems, meta, link_lines)
    print(f"done in {time.time() - t0:.0f} s: {json.dumps(meta['poems'])} poems, {json.dumps(meta['tokens'])}",
          flush=True)
    return 0


def write_report(poems: list, meta: dict, link_lines: collections.Counter) -> None:
    by_split = collections.defaultdict(collections.Counter)
    for p in poems:
        by_split[p["split"]][p["metre"] or "(none)"] += 1
    origin = collections.Counter((p["origin"], p["split"]) for p in poems)
    cr = collections.Counter((p["copyright_protected"], p["split"]) for p in poems)
    lines = ["# Stage-2 poem corpus", "", f"Built {meta['built']} by `prepare_poems.py`.", "",
             "## Funnel", "", "| step | poems |", "|---|---|"]
    lines += [f"| {k} | {v:,} |" for k, v in sorted(meta["funnel"].items())]
    lines += ["", "## Splits", "", "| split | poems | groups | poem tokens | bhavam tokens |", "|---|---|---|---|---|"]
    for s in ("train", "val", "test"):
        lines.append(f"| {s} | {meta['poems'].get(s, 0):,} | {meta['groups']['by_split'].get(s, 0):,} | "
                     f"{meta['tokens'].get(f'poems/{s}', 0):,} | {meta['tokens'].get(f'bhavam/{s}', 0):,} |")
    lines += ["", f"Largest groups (poems): {meta['groups']['largest']}", "",
              "Lines that join the most poems:", ""]
    lines += [f"- `{line}`: {n:,} poems" for line, n in link_lines.most_common(15)]
    lines += ["", "## Origin by split", "", "| origin | train | val | test |", "|---|---|---|---|"]
    for o in sorted({o for o, _ in origin}):
        lines.append(f"| {o} | " + " | ".join(f"{origin[(o, s)]:,}" for s in ("train", "val", "test")) + " |")
    lines += ["", "## Poets marked copyright_protected (Padyarchana)", "", "| flag | train | val | test |", "|---|---|---|---|"]
    for f in (True, False, None):
        lines.append(f"| {f} | " + " | ".join(f"{cr[(f, s)]:,}" for s in ("train", "val", "test")) + " |")
    lines += ["", "## Metres (top 25 by train count)", "", "| metre | train | val | test |", "|---|---|---|---|"]
    for m, n in by_split["train"].most_common(25):
        lines.append(f"| {m} | {n:,} | {by_split['val'][m]:,} | {by_split['test'][m]:,} |")
    (DATA / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())

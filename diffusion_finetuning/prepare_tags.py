"""E5: a metre-tagged copy of the poem corpus. Every poem whose metre is in the engine's catalogue is preceded
by its metre's name as a document of its own:

    <bos> కందము <eos> <bos> poem <eos>

    ../.venv/bin/python prepare_tags.py

The splits, the poems and their order are those of prepare_poems.py: this reads data/poems_index.jsonl and
data/tokens/poems/{train,val,test}.bin and changes neither.

How a metre gets a tag:
- The corpus's metre name (Padyarchana or dataset/) is matched to the catalogue's Telugu name (`name_te`).
- Spelling variants are absorbed: spaces, a final -ము/-ం, ళ/ల, and a final ీ/ి.
- A composite (సీసము + తేటగీతి) takes its first metre.
- Names with no single catalogue metre get no tag: Unknown, గీతము, ఉత్కళిక, శ్లోకము, "ఆటవెలది/తేటగీతి", none. The
  model sees those poems untagged, as in E2.

Writes data/tokens/poems_tagged/{train,val,test}.bin and data/tags.json (the mapping and coverage).
"""
from __future__ import annotations

import collections
import json
import sys

import numpy as np

from common import DATA, INDEX, REPO, TOKENS, canonical, tokenizer

sys.path.insert(0, str(REPO / "meter_engine"))
from indic_meter_dawg import default_dawg                                     # noqa: E402


def metre_key(name: str) -> str:
    """Canonical form of a metre name, absorbing the corpora's spelling variants."""
    k = canonical(name.replace("_", " ")).replace("ళ", "ల")
    for suffix in ("ము", "ం"):
        if k.endswith(suffix):
            k = k[: -len(suffix)]
            break
    return k[:-1] + "ి" if k.endswith("ీ") else k


def catalogue_tags() -> dict[str, tuple[str, str]]:
    """metre_key -> (engine name, tag text) for every concrete metre of the catalogue."""
    return {metre_key(s.name_te): (s.name, s.name_te.replace("_", " ")) for s in default_dawg().catalogue.concrete}


def tag_for(metre, tags) -> tuple[str, str] | None:
    if not metre or "/" in metre:
        return None
    return tags.get(metre_key(metre.split("+")[0]))


def main() -> int:
    tok = tokenizer()
    tags = catalogue_tags()
    rows = [json.loads(l) for l in INDEX.open(encoding="utf-8")]
    tag_ids, coverage, names = {}, collections.Counter(), collections.Counter()
    out = collections.defaultdict(list)
    arrays = {s: np.fromfile(TOKENS / "poems" / f"{s}.bin", dtype=np.uint16) for s in ("train", "val", "test")}
    for r in rows:
        t = tag_for(r["metre"], tags)
        ids = arrays[r["split"]][r["offset"]: r["offset"] + r["n_tokens"]]
        if t:
            engine, text = t
            if text not in tag_ids:
                tag_ids[text] = np.asarray(tok.encode(text, add_bos=True, add_eos=True), dtype=np.uint16)
            out[r["split"]] += [tag_ids[text], ids]
            coverage[(r["split"], "tagged")] += 1
            names[engine] += 1
        else:
            out[r["split"]].append(ids)
            coverage[(r["split"], "untagged")] += 1
    (TOKENS / "poems_tagged").mkdir(parents=True, exist_ok=True)
    tokens = {}
    for s, parts in out.items():
        arr = np.concatenate(parts)
        arr.tofile(TOKENS / "poems_tagged" / f"{s}.bin")
        tokens[s] = int(len(arr))
    untagged = collections.Counter(r["metre"] for r in rows if not tag_for(r["metre"], tags))
    report = {"tokens": tokens, "coverage": {f"{s}/{k}": n for (s, k), n in sorted(coverage.items())},
              "poems_by_metre": dict(names.most_common()),
              "untagged_names": dict(untagged.most_common(30)),
              "tags": {engine: text for engine, text in tags.values()}}
    (DATA / "tags.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("tokens", "coverage")}, ensure_ascii=False))
    print("untagged:", list(untagged.most_common(12)))
    print("tagged metres:", len(names), "of", len(tags), "| top:", list(names.most_common(8)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

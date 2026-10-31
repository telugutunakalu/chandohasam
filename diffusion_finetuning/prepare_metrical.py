"""E5b: the metre-tagged corpus of E5, trained on catalogue-metre poems only.

    ../.venv/bin/python prepare_metrical.py

The train split keeps only the poems whose metre has a catalogue tag (the tagged poems of E5, each as
<bos> name <eos> <bos> poem <eos>); the untagged ones (Unknown, గీతము, ఉత్కళిక, శ్లోకము, ...) are dropped. val and
test are E5's own files (hard links), so every evaluation and E3 run compares directly with E5.

Writes data/tokens/poems_metrical/{train,val,test}.bin and data/metrical.json (counts).
"""
from __future__ import annotations

import collections
import json
import os

import numpy as np

from common import DATA, INDEX, TOKENS, tokenizer
from prepare_tags import catalogue_tags, tag_for


def main() -> int:
    tok = tokenizer()
    tags = catalogue_tags()
    rows = [json.loads(l) for l in INDEX.open(encoding="utf-8") if '"split": "train"' in l]
    train = np.fromfile(TOKENS / "poems" / "train.bin", dtype=np.uint16)
    tag_ids, parts, kept, dropped = {}, [], collections.Counter(), collections.Counter()
    for r in rows:
        t = tag_for(r["metre"], tags)
        if not t:
            dropped[r["metre"]] += 1
            continue
        _, text = t
        if text not in tag_ids:
            tag_ids[text] = np.asarray(tok.encode(text, add_bos=True, add_eos=True), dtype=np.uint16)
        parts += [tag_ids[text], train[r["offset"]: r["offset"] + r["n_tokens"]]]
        kept[text] += 1
    out = TOKENS / "poems_metrical"
    out.mkdir(parents=True, exist_ok=True)
    arr = np.concatenate(parts)
    arr.tofile(out / "train.bin")
    for s in ("val", "test"):                              # E5's held-out files, unchanged
        dst = out / f"{s}.bin"
        if dst.exists():
            dst.unlink()
        os.link(TOKENS / "poems_tagged" / f"{s}.bin", dst)
    tagged_tokens = int(np.fromfile(TOKENS / "poems_tagged" / "train.bin", dtype=np.uint16).size)
    report = {"train_poems_kept": sum(kept.values()), "train_poems_dropped": sum(dropped.values()),
              "train_tokens": int(arr.size), "e5_train_tokens": tagged_tokens,
              "dropped_by_metre": dict(dropped.most_common(20)), "kept_by_metre": dict(kept.most_common())}
    (DATA / "metrical.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if not k.endswith("_by_metre")}, ensure_ascii=False))
    print("dropped:", list(dropped.most_common(8)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

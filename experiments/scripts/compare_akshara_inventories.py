#!/usr/bin/env python3
"""
Which akshara inventory should a v2 enforcer use: the syllable tokenizer's, or the verse corpus's own?

Both inventories are compared in the tokenizer's own segmentation (``diffusion_pretraining/
tokenizer``, ``syllabify``), so that the units match:

* tokenizer — the atomic syllables of ``telugu_alldomain.tokenizer.json`` (aksharas seen often enough
  in its all-domain training corpus);
* verse     — the aksharas of the words of 90% of the real poems in ``dataset/*.json`` (the same split
  as ``measure_absent_words.py``; the other 10% are held out).

For each inventory and each set of poems (held-out real verse, and every generated poem by model and
ablation): the share of akshara tokens outside the inventory, and the share of words with at least
one such akshara — for real verse the words the inventory would wrongly forbid, for generated text
the words it would block.

usage: compare_akshara_inventories.py OUT_DIR
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "meter_engine"))
sys.path.insert(0, str(ROOT / "experiments" / "scripts"))
sys.path.insert(0, str(ROOT / "diffusion_pretraining"))

from metrical_decoder.analysis import _telugu_words                      # noqa: E402
from measure_absent_words import MODELS, RUNS, real_poems               # noqa: E402
from tokenizer.telugu_tokenizer import SyllableAwareTeluguTokenizer    # noqa: E402

TOKENIZER = ROOT / "diffusion_pretraining" / "tokenizer" / "telugu_alldomain.tokenizer.json"


def main() -> None:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    tok = SyllableAwareTeluguTokenizer.load(str(TOKENIZER))
    tok_inv = set(json.loads(TOKENIZER.read_text(encoding="utf-8"))["atomic_aksharas"])

    def syl(word: str) -> list[str]:
        return [p for p in tok.syllabify(word) if p.strip()]

    poems = real_poems()
    rng = random.Random(0)
    order = list(range(len(poems)))
    rng.shuffle(order)
    cut = len(poems) // 10
    held = [poems[i] for i in order[:cut]]
    train = [poems[i] for i in order[cut:]]
    train_lines = {ln for p in train for ln in p}
    held = [[ln for ln in p if ln not in train_lines] for p in held]
    verse_inv = {a for p in train for ln in p for w in _telugu_words(ln) for a in syl(w)}
    inventories = {"tokenizer": tok_inv, "verse": verse_inv}

    sets: dict[str, list[str]] = {"real verse (held out)": [w for p in held for ln in p for w in _telugu_words(ln)]}
    for model, runs in MODELS.items():
        for run in runs:
            for ln in open(RUNS / run / "results.jsonl", encoding="utf-8"):
                r = json.loads(ln)
                sets.setdefault(f"{model} | {r['mode']}", []).extend(_telugu_words(r["text"]))

    data, lines = {}, []
    lines.append(f"Inventories: tokenizer {len(tok_inv)} syllables; verse {len(verse_inv)} aksharas "
                 f"(90% of {len(poems)} real poems); shared {len(tok_inv & verse_inv)}; verse aksharas missing "
                 f"from the tokenizer {len(verse_inv - tok_inv)}.")
    lines += ["", "| set | words | outside tokenizer: aksharas / words | outside verse: aksharas / words |",
              "|---|---|---|---|"]
    for name, words in sets.items():
        row = {"words": len(words)}
        cells = []
        for inv_name, inv in inventories.items():
            n_ak = bad_ak = bad_w = 0
            for w in words:
                s = syl(w)
                miss = sum(a not in inv for a in s)
                n_ak += len(s)
                bad_ak += miss
                bad_w += miss > 0
            row[inv_name] = {"aksharas_outside": bad_ak / n_ak, "words_outside": bad_w / len(words)}
            cells.append(f"{100 * bad_ak / n_ak:.2f}% / {100 * bad_w / len(words):.1f}%")
        data[name] = row
        lines.append(f"| {name} | {len(words)} | " + " | ".join(cells) + " |")

    # the invented aksharas of the constrained poems: how many does each inventory let through?
    invented = Counter()
    for name, words in sets.items():
        if "|" in name and not name.endswith("baseline"):
            for w in words:
                for a in syl(w):
                    if a not in verse_inv:
                        invented[a] += 1
    through = Counter({a: c for a, c in invented.items() if a in tok_inv})
    lines += ["", f"Aksharas of the constrained poems absent from the verse inventory: {sum(invented.values())} "
                  f"occurrences, {len(invented)} distinct; of these the tokenizer has {len(through)} distinct "
                  f"({100 * sum(through.values()) / max(sum(invented.values()), 1):.1f}% of occurrences).",
              "Most frequent ones the tokenizer accepts: " + ", ".join(f"{a} {c}" for a, c in through.most_common(15)),
              "Most frequent ones it rejects: " + ", ".join(f"{a} {c}" for a, c in (invented - through).most_common(15)),
              "Verse aksharas the tokenizer lacks (most frequent in real verse): "]
    vfreq = Counter(a for p in train for ln in p for w in _telugu_words(ln) for a in syl(w))
    lacking = [(a, c) for a, c in vfreq.most_common() if a not in tok_inv]
    lines[-1] += ", ".join(f"{a} {c}" for a, c in lacking[:20])
    lines.append(f"(they make up {100 * sum(c for _, c in lacking) / sum(vfreq.values()):.2f}% of the akshara "
                 f"tokens of real verse)")
    data["invented"] = {"occurrences": sum(invented.values()), "distinct": len(invented),
                        "accepted_by_tokenizer_distinct": len(through),
                        "accepted_by_tokenizer_share": sum(through.values()) / max(sum(invented.values()), 1)}
    md = "\n".join(lines) + "\n"
    (out / "inventories.md").write_text(md, encoding="utf-8")
    (out / "inventories.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()

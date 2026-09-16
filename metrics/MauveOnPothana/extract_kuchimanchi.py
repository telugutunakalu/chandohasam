"""Convert kuchimanchi_timmakavi_poems.txt (blank-line-separated padyas) to JSON.

1653 blocks: 1393 four-line (satakam vrittas, e.g. the Bhargava/Kukkuteswara
satakam makutas), 243 twelve-line (సీసము + tail), a few oddballs, and 11
one-line truncations (dropped, consistent with the Pothana extraction).
No exact duplicates in the source.
"""

import json
from collections import Counter
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "kuchimanchi_timmakavi_poems.txt"
OUT = Path(__file__).resolve().parent / "kuchimanchi_poems.json"


def form_of(n_lines):
    if n_lines == 4:
        return "padyam-4"
    if n_lines == 12:
        return "seesamu+tail"
    return f"other-{n_lines}"


def main():
    raw = SRC.read_text(encoding="utf-8")
    blocks = [b.strip() for b in raw.split("\n\n") if b.strip()]

    poems, dropped = [], 0
    for b in blocks:
        lines = [l.strip() for l in b.split("\n") if l.strip()]
        if len(lines) < 4:
            dropped += 1
            continue
        poems.append(
            {
                "id": f"kuchimanchi-{len(poems) + 1}",
                "author": "Kuchimanchi Timmakavi",
                "form": form_of(len(lines)),
                "n_lines": len(lines),
                "text": "\n".join(lines),
            }
        )

    OUT.write_text(json.dumps(poems, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"blocks: {len(blocks)}, dropped (<4 lines): {dropped}, kept: {len(poems)}")
    print("forms:", dict(Counter(p["form"] for p in poems).most_common()))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

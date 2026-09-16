"""Convert vemana_poems.txt (blank-line-separated padyas) to JSON.

Source: /home/samvaran/workspace/workspace/padyarchana_prototype/vemana_poems.txt
1258 blocks: 1254 four-line (Ataveladi with the Vemana makuta) and 4
eight-line (Seesamu-style). Exact duplicate blocks are removed.
"""

import json
from collections import Counter
from pathlib import Path

SRC = Path("/home/samvaran/workspace/workspace/padyarchana_prototype/vemana_poems.txt")
OUT = Path(__file__).resolve().parent / "vemana_poems.json"


def main():
    raw = SRC.read_text(encoding="utf-8")
    blocks = [b.strip() for b in raw.split("\n\n") if b.strip()]

    seen = set()
    poems = []
    dupes = 0
    for b in blocks:
        lines = [l.strip() for l in b.split("\n") if l.strip()]
        text = "\n".join(lines)
        if text in seen:
            dupes += 1
            continue
        seen.add(text)
        meter = "ఆ." if len(lines) == 4 else "సీ."
        poems.append(
            {
                "id": f"vemana-{len(poems) + 1}",
                "author": "Vemana",
                "meter": meter,
                "meter_name": "Ataveladi" if meter == "ఆ." else "Seesamu",
                "n_lines": len(lines),
                "text": text,
            }
        )

    OUT.write_text(json.dumps(poems, ensure_ascii=False, indent=1), encoding="utf-8")
    c = Counter(p["meter_name"] for p in poems)
    print(f"blocks: {len(blocks)}, duplicates removed: {dupes}, kept: {len(poems)}")
    print("meters:", dict(c))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

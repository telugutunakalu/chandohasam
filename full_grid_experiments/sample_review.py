"""One randomly drawn grid prompt, every cell's poem on it: the scorer's verdicts beside the text (user request
2026-10-29: random sample, metrics against a close reading).

    ../.venv/bin/python sample_review.py [--seed 20261029]      # → results/sample_review_<seed>.md (CPU only)

- **Draw:** one prompt from the 100 (prompts/grid100/selection.json) by random.Random(seed).choice; the same prompt for
  every cell, so cells compare poem to poem.
- **Cells:** gold, then each row's free (baseline), constrained v1 (masking_backtrack) and v2 A+B poem (seed 42). The
  masking_only / hybrid cells (34 prompts, two rows) are left out.
- **Verdicts:** read from results/grid_poems.jsonl (score_grid.py's numbers; a cell scored after its last run is
  missing there and shown as "not scored"). Non-words: the words of ≥ 2 syllables the real-words matcher rejects
  (ఁ stripped), as score_e6.words_stripped counts them.
- The close reading is written by hand under each poem in the output file, so an existing file is not overwritten
  without --force.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_grid as S                                               # noqa: E402  (sets E6_RECORDS_DIR, paths)
from score_e6 import _syllables, _telugu_words, stripped_matcher     # noqa: E402
import grid as G                                                     # noqa: E402

MODES = (("baseline", "free"), ("masking_backtrack", "constrained v1"), ("masking_backtrack_v2", "constrained v2 A+B"))


def poems(pid: str) -> dict[str, dict]:
    """cell key (as in grid_poems.jsonl) → {label, text} for every cell holding a poem on ``pid``."""
    out = {}
    for row, c in G.cells("core"):
        _, _, path = G.command(row, c)
        _, _, new = G.command(row, c, new=True)
        for mode in G.CELLS[c][0]:
            rows = [r for p in (path, new) if G.done(p) for r in S.cell_rows(p, [mode], {pid})]
            if rows:
                out[f"{row.key}|{mode}"] = {"label": f"{row.model} · {row.state}", "text": rows[0]["text"]}
    for row, c in G.cells("v2"):
        _, _, path = G.command(row, c, v2=True)
        rows = S.cell_rows(path, ["masking_backtrack"], {pid}) if G.done(path) else []
        if rows:
            out[f"{row.key}|masking_backtrack_v2"] = {"label": f"{row.model} · {row.state}", "text": rows[0]["text"]}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261029)
    ap.add_argument("--force", action="store_true", help="overwrite the output (it holds the hand-written readings)")
    args = ap.parse_args()
    out = S.OUT / f"sample_review_{args.seed}.md"
    if out.exists() and not args.force:
        sys.exit(f"{out} exists (it holds the readings); --force to overwrite")
    grid = [p["id"] for p in json.loads(S.SELECTION.read_text(encoding="utf-8"))["prompts"]]
    pid = random.Random(args.seed).choice(grid)
    rec = next(r for r in map(json.loads, open(HERE / "prompts" / "grid100" / "records" / "test.jsonl",
                                                encoding="utf-8")) if r["id"] == pid)
    scores = {}
    for line in open(S.OUT / "grid_poems.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if r["prompt_id"] == pid:
            scores[r["cell"]] = r
    m = stripped_matcher()

    def block(text: str, sc: dict | None) -> list[str]:
        lines = text.split("\n")
        ws = [w.replace("ఁ", "") for ln in lines for w in _telugu_words(ln)]
        bad = [w for w in ws if w and len(_syllables(w)) >= 2 and not m.verdict(w)["compound"]]
        if sc is None:
            v = "not scored"
        else:
            p = lambda x: "–" if x is None else f"{100 * x:.0f}%"
            v = (f"in metre {'yes' if sc['all'] else 'no'} · skill {sc['skill']:.2f} · real words {p(sc['words_s'])} · "
                 f"one-akshara {p(sc['filler'])} · copy {p(sc['copy'])} · recognised "
                 f"{'yes' if sc['meaning'] else 'no'} · repeated line {'yes' if sc['repeated'] else 'no'} · "
                 f"gold run {sc['gold_run']}")
        return ["```", text or "(empty)", "```", "", f"*Scorer:* {v}", "",
                f"*Non-words ({len(bad)}):* {' · '.join(bad) if bad else '—'}", "", "*Reading:* ", ""]

    md = [f"# Random-sample review: {pid} · {rec['meter']}", "",
          f"Drawn by random.Random({args.seed}).choice over the 100 grid prompts. One poem per cell (seed 42). "
          "Scorer verdicts from results/grid_poems.jsonl; non-words: words of ≥ 2 syllables the real-words matcher "
          "rejects (ఁ stripped).", "", f"**Bhāvam (the prompt):** {rec['meaning']}", "", "## Gold", ""]
    md += block("\n".join(rec["lines"]), scores.get("gold"))
    cells = poems(pid)
    for row in G.ROWS:
        for mode, name in MODES:
            k = f"{row.key}|{mode}"
            if k in cells:
                md += [f"## {cells[k]['label']} · {name}", ""] + block(cells[k]["text"], scores.get(k))
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{pid}: {len(cells)} cells → {out}")


if __name__ == "__main__":
    main()

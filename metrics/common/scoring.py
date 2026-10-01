"""Input, output and reference-distribution helpers shared by the metric scripts."""
from __future__ import annotations

import bisect
import json
import sys
from pathlib import Path

from common import corpus


def add_source_arguments(parser) -> None:
    """--text / --file / --jsonl / --dataset, and the output options of `score`."""
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="one poem, lines separated by newlines (or a literal \\n)")
    src.add_argument("--file", help="one poem, one line per text line")
    src.add_argument("--jsonl", help="poems, one JSON object per line")
    src.add_argument("--dataset", choices=list(corpus.CORPORA), help="a dataset file, by stem")
    parser.add_argument("--field", default="lines", help="--jsonl field holding the lines (list or string)")
    parser.add_argument("--no-lines", dest="lines", action="store_false", help="omit per-line detail")
    parser.add_argument("--out", help="write JSONL here instead of stdout")


def read_poems(args) -> list:
    """[(id, lines)] from --text, --file, --jsonl or --dataset."""
    if args.text is not None:
        return [("text", [l for l in args.text.replace("\\n", "\n").splitlines() if l.strip()])]
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
        return [(args.file, [l for l in text.splitlines() if l.strip()])]
    if args.jsonl:
        out = []
        for n, raw in enumerate(Path(args.jsonl).read_text(encoding="utf-8").splitlines()):
            if raw.strip():
                rec = json.loads(raw)
                lines = rec[args.field]
                lines = lines.splitlines() if isinstance(lines, str) else lines
                out.append((rec.get("id", n), [l for l in lines if l.strip()]))
        return out
    return [(p.key, list(p.lines)) for p in corpus.load(args.dataset)]


def write_results(args, poems: list, score_poem) -> None:
    """Score every poem with score_poem(lines) and print one JSON object per poem."""
    sink = open(args.out, "w", encoding="utf-8") if args.out else sys.stdout
    for pid, lines in poems:
        result = {"id": pid, **score_poem(lines)}
        if not args.lines:
            result.pop("lines")
        indent = 1 if sink is sys.stdout and len(poems) == 1 else None
        print(json.dumps(result, ensure_ascii=False, indent=indent), file=sink)
    if args.out:
        sink.close()
        print(f"wrote {args.out}: {len(poems)} poems")


def quantiles(values: list) -> list:
    """101 quantiles (0th to 100th percentile) of the values, None dropped."""
    values = sorted(v for v in values if v is not None)
    n = len(values)
    return [round(values[round(k / 100 * (n - 1))], 4) for k in range(101)]


def percentile(value, qs: list):
    """Share (0-100) of the reference values at or below `value`, from 101 stored quantiles."""
    if value is None:
        return None
    k = bisect.bisect_right(qs, value)
    if k == 0:
        return 0.0
    if k >= len(qs):
        return 100.0
    lo, hi = qs[k - 1], qs[k]
    return round(k - 1 + ((value - lo) / (hi - lo) if hi > lo else 1.0), 1)

"""Writing results and printing tables."""
import json
import math

import config


def _clean(obj):
    """Make numpy scalars and NaN JSON-safe."""
    if isinstance(obj, dict):
        return {str(k): _clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean(v) for v in obj]
    if hasattr(obj, "item") and not isinstance(obj, (str, bytes)):
        obj = obj.item()
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    return obj


def save_result(name: str, result: dict) -> None:
    """Write outputs/<name>.json."""
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = config.OUTPUT_DIR / f"{name}.json"
    path.write_text(json.dumps(_clean(result), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {path.relative_to(config.REPO_ROOT)}")


def pct(k, n) -> float:
    return 100.0 * k / n if n else float("nan")


def fmt(x, nd=3) -> str:
    if x is None:
        return "—"
    if isinstance(x, float):
        return "—" if math.isnan(x) else f"{x:.{nd}f}"
    return str(x)


def print_table(headers, rows, title: str = "") -> None:
    """Plain-text table for the console."""
    if title:
        print(f"\n{title}")
    cells = [[fmt(c) for c in r] for r in rows]
    widths = [max(len(str(h)), *(len(r[i]) for r in cells)) if cells else len(str(h))
              for i, h in enumerate(headers)]
    line = "  ".join(str(h).ljust(w) for h, w in zip(headers, widths))
    print(line)
    print("-" * len(line))
    for r in cells:
        print("  ".join(c.ljust(w) for c, w in zip(r, widths)))

# -*- coding: utf-8 -*-
"""
How the constraint changes what the model chooses: a report over run directories.

For every generated token the trace holds the model's log-probability of the
chosen token over the whole vocabulary (temperature 1), its rank, the model's
top-5 with their validity, the probability mass on meter-valid tokens and the
entropy (``strategies._Tracer``). This module aggregates them by strategy, by
meter and by the position the token lands on:

* ``prasa`` — the line's second akshara (meters with prāsa);
* ``yati`` — an akshara that must be in maitri with the vaḷi (the vaḷi itself
  is akshara 1 and counts as ``line_start``);
* ``line_start`` / ``other``.

A token is *overridden* when the model's own first choice was not allowed —
the step where the constraint, not the model, decided. The lexical rate is the
share of generated words that occur as words in the repository's corpora
(``dataset/*.json``): a rough gauge of how often the constrained text stays
Telugu; poetry fuses words by sandhi, so even real verse scores well below 1.

Owns: :func:`report`, :func:`corpus_lexicon`. Must not import torch.
"""
from __future__ import annotations

import json
import statistics
import unicodedata
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Optional

from .incremental import ENGINE_DIR
from .registers import _syllables, line_groups

DATASET = ENGINE_DIR.parent / "dataset"
TELUGU = ("ఀ", "౿")
MODES = ("baseline", "masking_only", "masking_backtrack", "hybrid")
# tokens chosen from the model's distribution (not imposed line breaks / EOS): autoregressive strategies
# (sample, accept, alive) and diffusion (proposal: the model's own sample; masked; rerank)
TOKEN_HOWS = ("sample", "accept", "alive", "proposal", "masked", "rerank")


def _telugu_words(text: str) -> list[str]:
    out = []
    for w in unicodedata.normalize("NFC", text).split():
        w = "".join(ch for ch in w if TELUGU[0] <= ch <= TELUGU[1])
        if w:
            out.append(w)
    return out


@lru_cache(maxsize=1)
def corpus_lexicon() -> frozenset[str]:
    """Every word of the verses in ``dataset/*.json``."""
    words: set[str] = set()
    for path in sorted(DATASET.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        for rec in data if isinstance(data, list) else []:
            for ln in rec.get("verse") or []:
                words.update(_telugu_words(ln))
    return frozenset(words)


def _yati_targets(meter: str, patterns: list[str]) -> dict[int, set[int]]:
    """Per line: the aksharas that must match a vaḷi (every member of a group but its first)."""
    out: dict[int, set[int]] = {}
    for i, pat in enumerate(patterns):
        targets: set[int] = set()
        for g in line_groups(meter, i, pat, True):
            if g:
                targets.update(g[1:])
        out[i] = targets
    return out


def _position(rec: dict, has_prasa: bool, targets: dict[int, set[int]]) -> str:
    line, ak = rec.get("line"), rec.get("akshara")
    if line is None or ak is None:
        return "other"
    if ak <= 1:
        return "line_start"
    if has_prasa and ak == 2:
        return "prasa"
    if ak in targets.get(line, ()):
        return "yati"
    return "other"


class _Acc:
    """Running sums for one cell of the report."""

    def __init__(self):
        self.poems = 0
        self.complete = 0
        self.gana = 0
        self.all_strict = 0
        self.tokens = 0
        self.backtracks = 0
        self.logp: list[float] = []
        self.rank1 = 0
        self.overridden = 0
        self.judged = 0                       # steps whose top-1 validity is known
        self.valid_mass: list[float] = []
        self.entropy: list[float] = []
        self.words = 0
        self.lexical = 0
        self.one_akshara = 0                  # words of a single akshara (filler such as క క క)
        self.repeats = 0                      # poems with a line written twice

    def add_poem(self, row: dict, lexicon: frozenset[str]) -> None:
        ev = row.get("eval") or {}
        self.poems += 1
        self.complete += bool(row.get("complete_in_meter")) if row.get("mode") == "baseline" else row.get("status") == "complete"
        self.gana += bool(ev.get("gana_strict"))
        self.all_strict += bool(ev.get("gana_strict") and ev.get("prasa_strict") and ev.get("yati_strict"))
        self.backtracks += row.get("n_backtracks") or 0
        self.repeats += (ev.get("duplicate_lines") or 0) > 0
        for ln in ev.get("lines") or []:
            ws = _telugu_words(ln)
            self.words += len(ws)
            self.lexical += sum(w in lexicon for w in ws)
            self.one_akshara += sum(len(_syllables(w)) == 1 for w in ws)

    def add_token(self, rec: dict) -> None:
        self.tokens += 1
        self.logp.append(rec["logp"])
        self.rank1 += rec.get("rank") == 1
        top = rec.get("top") or []
        if top and top[0][3] is not None:
            self.judged += 1
            self.overridden += top[0][3] is False
        if rec.get("valid_mass") is not None:
            self.valid_mass.append(rec["valid_mass"])
        if rec.get("H") is not None:
            self.entropy.append(rec["H"])

    def row(self) -> dict:
        mean = lambda xs: statistics.fmean(xs) if xs else None              # noqa: E731
        return {
            "poems": self.poems,
            "tokens": self.tokens,
            "complete": self.complete / self.poems if self.poems else None,
            "gana_strict": self.gana / self.poems if self.poems else None,
            "all_strict": self.all_strict / self.poems if self.poems else None,
            "tokens_per_poem": self.tokens / self.poems if self.poems else None,
            "mean_logp": mean(self.logp),
            "median_logp": statistics.median(self.logp) if self.logp else None,
            "rank1": self.rank1 / self.tokens if self.tokens else None,
            "overridden": self.overridden / self.judged if self.judged else None,
            "valid_mass": mean(self.valid_mass),
            "entropy": mean(self.entropy),
            "lexical": self.lexical / self.words if self.words else None,
            "one_akshara_words": self.one_akshara / self.words if self.words else None,
            "repeated_line": self.repeats / self.poems if self.poems else None,
            "backtracks_per_poem": self.backtracks / self.poems if self.poems else None,
        }


def _traces(run: Path) -> Iterable[tuple[str, list]]:
    path = run / "traces.jsonl"
    if not path.exists():
        return
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            try:
                row = json.loads(ln)
            except json.JSONDecodeError:
                continue
            yield row["key"], row["trace"]


def collect(run_dirs: Iterable[str | Path]) -> dict:
    """Aggregate the runs: {"by_mode": …, "by_mode_position": …, "by_meter_mode": …}."""
    from indic_meter_dawg import default_dawg
    dawg = default_dawg()
    lexicon = corpus_lexicon()
    by_mode: dict[str, _Acc] = defaultdict(_Acc)
    by_pos: dict[tuple[str, str], _Acc] = defaultdict(_Acc)
    by_meter: dict[tuple[str, str], _Acc] = defaultdict(_Acc)
    for run in map(Path, run_dirs):
        rows = {}
        with open(run / "results.jsonl", encoding="utf-8") as fh:
            for ln in fh:
                r = json.loads(ln)
                rows[r["key"]] = r
                by_mode[r["mode"]].add_poem(r, lexicon)
                by_meter[(r["meter"], r["mode"])].add_poem(r, lexicon)
        for key, trace in _traces(run):
            r = rows.get(key)
            if r is None:
                continue
            meter, mode = r["meter"], r["mode"]
            has_prasa = bool(dawg.spec(meter).prasa)
            targets = _yati_targets(meter, (r.get("eval") or {}).get("patterns") or [])
            for rec in trace:
                if rec.get("how") not in TOKEN_HOWS:
                    continue
                by_mode[mode].add_token(rec)
                by_meter[(meter, mode)].add_token(rec)
                if rec.get("line") is not None:          # positions are known while the text is in meter
                    by_pos[(mode, _position(rec, has_prasa, targets))].add_token(rec)
    return {"by_mode": {m: a.row() for m, a in by_mode.items()},
            "by_mode_position": {f"{m}|{p}": a.row() for (m, p), a in by_pos.items()},
            "by_meter_mode": {f"{me}|{mo}": a.row() for (me, mo), a in by_meter.items()}}


def _fmt(x, pct: bool = False, nd: int = 3) -> str:
    if x is None:
        return "–"
    return f"{100 * x:.0f}" if pct else f"{x:.{nd}f}"


def report(run_dirs: Iterable[str | Path], out: Optional[str | Path] = None) -> str:
    """A markdown report (and ``out``.json with the numbers when ``out`` is given)."""
    run_dirs = list(run_dirs)
    data = collect(run_dirs)
    modes = [m for m in MODES if m in data["by_mode"]]
    lines = ["# Token choices under the constraint", "",
             "Runs: " + ", ".join(f"`{Path(r).name}`" for r in run_dirs), "",
             "logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); "
             "overridden: the model's first choice was not allowed; valid mass: the model's probability "
             "on allowed tokens (baseline: known only while its text is still in meter); lexical: share "
             "of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate "
             "counts filler such as క క క as words); repeated line: a poem that writes some line twice; "
             "complete (baseline): a whole poem in meter.", "",
             "## By strategy", "",
             "| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | "
             "valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in modes:
        r = data["by_mode"][m]
        lines.append(f"| {m} | {r['poems']} | {_fmt(r['complete'], True)} | {_fmt(r['all_strict'], True)} | "
                     f"{_fmt(r['tokens_per_poem'], nd=0)} | {_fmt(r['mean_logp'])} | {_fmt(r['rank1'], True)} | "
                     f"{_fmt(r['overridden'], True)} | {_fmt(r['valid_mass'])} | {_fmt(r['entropy'])} | "
                     f"{_fmt(r['lexical'], True)} | {_fmt(r['one_akshara_words'], True)} | "
                     f"{_fmt(r['repeated_line'], True)} | "
                     f"{_fmt(r['backtracks_per_poem'], nd=1)} |")
    lines += ["", "## By position in the line", "",
              "| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |",
              "|---|---|---|---|---|---|---|"]
    for m in modes:
        for p in ("line_start", "prasa", "yati", "other"):
            r = data["by_mode_position"].get(f"{m}|{p}")
            if r and r["mean_logp"] is not None:
                lines.append(f"| {m} | {p} | {r['tokens']} | {_fmt(r['mean_logp'])} | {_fmt(r['rank1'], True)} | "
                             f"{_fmt(r['overridden'], True)} | {_fmt(r['valid_mass'])} |")
    lines += ["", "## By meter", "",
              "| meter | " + " | ".join(f"{m} in meter % / logp / lexical %" for m in modes) + " |",
              "|---|" + "---|" * len(modes)]
    for meter in sorted({k.split("|")[0] for k in data["by_meter_mode"]}):
        cells = []
        for m in modes:
            r = data["by_meter_mode"].get(f"{meter}|{m}")
            cells.append("–" if not r else f"{_fmt(r['all_strict'], True)} / {_fmt(r['mean_logp'], nd=2)} / "
                                          f"{_fmt(r['lexical'], True)}")
        lines.append(f"| {meter} | " + " | ".join(cells) + " |")
    md = "\n".join(lines) + "\n"
    if out:
        out = Path(out)
        out.write_text(md, encoding="utf-8")
        out.with_suffix(".json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return md

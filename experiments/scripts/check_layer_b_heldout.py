#!/usr/bin/env python3
"""
Held-out check of Layer B (attestation.py): does preferring corpus words make the text more real, or
only more like the words Layer B was given?

Layer B built from 90% of the real poems (``--attest-corpus train90``) is compared with v1, the
inventory alone (A) and Layer B built from all the verse, on the same poems. Words of two aksharas or
more are counted as

* real — in the full corpus (the earlier measure);
* known — in the 90% Layer B was built from;
* held-out only — in the other 10% of the poems and nowhere in the 90%: real words the train90 Layer B
  could not have favoured. More of them than in v1 means its effect reaches beyond its own word list.

usage: check_layer_b_heldout.py OUT_MD LABEL=RUN_DIR …   (the first run is the baseline of the bootstrap)
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "meter_engine"))

from metrical_decoder.analysis import _telugu_words                        # noqa: E402
from metrical_decoder.attestation import load_attestation                 # noqa: E402
from metrical_decoder.inventory import units                              # noqa: E402

MODES = ("masking_only", "masking_backtrack", "hybrid")


def main() -> None:
    out = Path(sys.argv[1])
    runs = dict(a.split("=", 1) for a in sys.argv[2:])
    full, known = load_attestation("all").words, load_attestation("train90").words
    held_only = full - known
    res = {n: {json.loads(l)["key"]: json.loads(l) for l in open(Path(d) / "results.jsonl", encoding="utf-8")}
           for n, d in runs.items()}
    trc = {n: {json.loads(l)["key"]: json.loads(l)["trace"] for l in open(Path(d) / "traces.jsonl", encoding="utf-8")}
           for n, d in runs.items()}
    keys = sorted(set.intersection(*(set(k for k, r in v.items() if r["mode"] in MODES) for v in res.values())))

    def shares(text: str) -> tuple[float, float, float, float, int]:
        ws = _telugu_words(text)
        n = max(len(ws), 1)
        long = [w for w in ws if len(units(w)) >= 2]
        return (sum(w in full for w in long) / n, sum(w in known for w in long) / n,
                sum(w in held_only for w in long) / n, sum(len(units(w)) == 1 for w in ws) / n, len(ws))

    lines = [f"Same {len(keys)} poems in every run. Words of 2+ aksharas: {len(full)} in the corpus, "
             f"{len(known)} in the 90% (known), {len(held_only)} only in the held-out 10%.", "",
             "| run | strategy | in meter | real | known | held-out only | 1-akshara | logp | repeated line |",
             "|---|---|---|---|---|---|---|---|---|"]
    per_poem = {}
    for n in runs:
        per_poem[n] = {k: shares(res[n][k]["text"]) for k in keys}
        for m in MODES:
            ks = [k for k in keys if res[n][k]["mode"] == m]
            ok = sum(res[n][k]["status"] == "complete" and all((res[n][k].get("eval") or {}).get(x)
                     for x in ("gana_strict", "prasa_strict", "yati_strict")) for k in ks)
            words = sum(per_poem[n][k][4] for k in ks)
            agg = [sum(per_poem[n][k][i] * per_poem[n][k][4] for k in ks) / words for i in range(4)]
            toks = [e for k in ks for e in trc[n][k] if e.get("how") in ("sample", "accept", "alive", "forced_nl")]
            logp = statistics.fmean(e["logp"] for e in toks)
            rep = sum(((res[n][k].get("eval") or {}).get("duplicate_lines") or 0) > 0 for k in ks)
            lines.append(f"| {n} | {m} | {ok}/{len(ks)} | {100 * agg[0]:.1f}% | {100 * agg[1]:.1f}% | "
                         f"{100 * agg[2]:.2f}% | {100 * agg[3]:.1f}% | {logp:.2f} | {rep}/{len(ks)} |")
    base = next(iter(runs))
    rng = random.Random(0)
    lines += ["", f"Per poem against {base} (paired bootstrap, 5,000 resamples, 95% interval):", ""]
    for n in list(runs)[1:]:
        for i, name in ((0, "real"), (2, "held-out only")):
            d = [per_poem[n][k][i] - per_poem[base][k][i] for k in keys]
            boots = sorted(statistics.fmean(rng.choice(d) for _ in d) for _ in range(5000))
            lines.append(f"- {n}, {name}: {100 * statistics.fmean(d):+.2f} points "
                         f"[{100 * boots[125]:+.2f}, {100 * boots[4875]:+.2f}]")
    md = "\n".join(lines) + "\n"
    out.write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()

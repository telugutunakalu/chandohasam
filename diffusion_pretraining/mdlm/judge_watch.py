"""Score every new sample file of a run with the CPU judge; append results to runs/<run>/judge.jsonl.

    uv run python -m mdlm.judge_watch --run pilot120m      # runs as deploy/telugu-mdlm-judge.service

Runs next to training without touching the GPU. The watcher is a small loop that
never imports torch: when a new sample file appears it starts a child process
(--once) that loads the judge (google/gemma-3-1b-pt) on the CPU, scores every
pending file and exits. Deleting the model inside a long-lived process does not
hand its memory back to the OS -- the old in-process watcher sat on ~4.6 GB of
RSS + swap between sample files that arrive ~4 h apart -- while a child that
exits returns all of it.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def pending(run_dir: Path) -> list[Path]:
    out = run_dir / "judge.jsonl"
    done = {json.loads(ln)["file"] for ln in out.read_text().splitlines() if ln} if out.exists() else set()
    return [f for f in sorted((run_dir / "samples").glob("step_*.txt")) if f.name not in done]


def score_pending(run_dir: Path, threads: int) -> int:
    files = pending(run_dir)
    if not files:
        return 0
    import torch

    from .judge import JUDGE, load_judge, perplexity

    torch.set_num_threads(threads)
    tok, model = load_judge(JUDGE, "cpu")
    with (run_dir / "judge.jsonl").open("a", encoding="utf-8") as fh:
        for f in files:
            texts = [t.replace("<bos>", "").replace("<eos>", "\n").strip()
                     for t in f.read_text(encoding="utf-8").split("\n\n==========\n\n")]
            ppl = perplexity(texts, tok, model)
            rec = {"step": int(re.search(r"(\d+)", f.stem).group(1)), "file": f.name, "gen_ppl": ppl,
                   "samples": len(texts), "judge": JUDGE}
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            print(f"{f.name}: gen-PPL {ppl:.1f}", flush=True)
    return len(files)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--every-min", type=float, default=10.0)
    ap.add_argument("--threads", type=int, default=6)
    ap.add_argument("--once", action="store_true",
                    help="score what is pending in this process and exit (what the watcher starts)")
    args = ap.parse_args(argv)
    run_dir = ROOT / "runs" / args.run
    if args.once:
        score_pending(run_dir, args.threads)
        return 0
    while True:
        if pending(run_dir):
            rc = subprocess.run([sys.executable, "-m", "mdlm.judge_watch", "--run", args.run,
                                 "--threads", str(args.threads), "--once"], cwd=ROOT).returncode
            if rc:
                print(f"judge child exited with code {rc}; retrying in {args.every_min:g} min", flush=True)
        time.sleep(args.every_min * 60)


if __name__ == "__main__":
    raise SystemExit(main())

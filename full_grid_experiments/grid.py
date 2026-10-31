"""The grid's rows and cells (PLAN.md §2, §4): one definition for the queue and the scorer.

    ../.venv/bin/python grid.py                     # every cell: status, results path, command
    ../.venv/bin/python grid.py --todo core         # the core cells not yet done, as queue lines (name TAB dir TAB cmd)
    ../.venv/bin/python grid.py --todo extra        # the † rows' other two strategies (after Oct 28: lever ③)
    ../.venv/bin/python grid.py --todo smoke        # every core cell on 1 poem of 2 metres (runs/…_smoke)
    ../.venv/bin/python grid.py --todo new          # every row's free + constrained cells on the new prompts (…_new)
    ../.venv/bin/python grid.py --todo v2           # every row's constrained cell with DAWG v2 A+B, all 100 (…_v2)
    ../.venv/bin/python grid.py --todo v2smoke      # the v2 cells on 1 poem of 2 metres (…_smoke_v2)

A row is a checkpoint; its cells are `free` (the baseline mode, seed 42; the rows done before 2026-10-28 also hold
seed 43, which the scorer leaves out), `constrained` (masking + backtracking,
seed 42) and, on the † rows, `extra` (masking only and hybrid, seed 42). The † rows are Nandi and MDLM 523M only (user
decision 2026-10-28: masking + backtracking was the best strategy on them, so T5 4B and DiffusionGemma lost their extra
cells). Every command reads the grid's prompts
through $E6_RECORDS_DIR (prompts/grid100/records; the MDLMs: --e6-data prompts/grid100).

The 100-prompt grid (user decision 2026-10-28; build_grid100.py): Bhāgavatam 50, Vemana 20, Kūcimañci 20, Gemini 10.
Every prompt is a poem of the human-evaluation pool (decision 20). 34 of them are prompts of the earlier 183
(../diffusion_finetuning/runs/grid100_known_test): the core cells run on those 34, and the rows already run on the 183
keep their poems (the scorer keeps their 34). The 66 new ones (grid100_new_test: 56 with a new P1 retelling, 10 Gemini
bhāvams as is) are every row's `new` cells (grid_<row>_<cell>_new), run once the P1 were approved (APPROVED).

DAWG v2 A+B (user decision 2026-10-28, PLAN.md decision 22): every row's constrained cell again on all 100 prompts
(grid100_all_test) with Layer A (the padyarchana syllable inventory) and Layer B (word attestation, padyarchana words,
weight 2 at every step): grid_<row>_constrained_v2. T5 takes the options itself; the other evaluators run through v2.py
(DiffusionGemma: Layer B in its diffusion loop, ../lora_gemma_diffusion/settled_attest.py). Free cells have no v2:
the layers act only where the constraint decides. DiffusionGemma's fine-tuned row is the whole-pool adapter only:
the 48k adapter was dropped from the study (user decision 2026-10-29, after its free cell on the new prompts was cut
off by a power outage; its free poems on the known prompts stay on disk, unscored), as was the 24k adapter (user
decision 2026-10-21: a snapshot of the 48k run). Gemma-4 12B and E2B are not in the grid (user decisions 2026-10-28).
"""
from __future__ import annotations

import argparse
import shlex
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PY = str(REPO / ".venv" / "bin" / "python")
E6D = HERE / "prompts" / "grid100"                 # build_grid100.py
REFERENCE, NEW_REFERENCE, V2_REFERENCE = "grid100_known_test", "grid100_new_test", "grid100_all_test"
V2_T5 = ["--inventory", "padyarchana", "--attest-weight", "2", "--attest-where", "all", "--attest-corpus", "padyarchana"]
FREE_SEEDS, SEEDS = ("42",), ("42",)     # one seed (user decision 2026-10-28; was 42 and 43)
# a vṛtta and a ragaḍa among the known prompts (the 100-prompt grid has no known kandamu or utpalamala); the
# smoke cells run before 2026-10-28 used kandamu and utpalamala
SMOKE_METRES = ("mattakokilamu", "madhuragati_ragada")
AR, T5, DF, DG = (REPO / d for d in ("autoregressive_finetuning", "t5_finetuning", "diffusion_finetuning",
                                     "lora_gemma_diffusion"))


@dataclass
class Row:
    key: str
    family: str
    model: str
    state: str
    data: str
    dagger: bool = False
    args: list[str] = field(default_factory=list)
    shards: int = 4             # processes of the sharded runs (Nandi, MDLM)


ROWS = [
    Row("nandi_base", "AR", "Nandi-Mini-150M", "base", "—", True),
    Row("nandi_ft", "AR", "Nandi-Mini-150M", "FT (bhāvam → poem)", "300,763 × 3.5", True,
        ["--weights", "runs/nandi-t1/snapshots/ema_step_0008225.pt"]),
    Row("gemma4_e4b", "AR", "Gemma-4 E4B-it", "base", "—", args=["--model", "google/gemma-4-E4B-it"]),
    Row("gemma4_26b", "AR", "Gemma-4 26B-A4B-it", "base", "—", args=["--model", "google/gemma-4-26B-A4B-it"]),
    Row("t5_270m_base", "enc-dec", "T5Gemma 2 270M", "base", "—", args=["--size", "270m"]),
    Row("t5_270m_ft", "enc-dec", "T5Gemma 2 270M", "FT (full)", "300,763 × 1",
        args=["--size", "270m", "--model", "runs/t5g-270m-full/final"]),
    Row("t5_1b_base", "enc-dec", "T5Gemma 2 1B", "base", "—", args=["--size", "1b"]),
    Row("t5_1b_ft", "enc-dec", "T5Gemma 2 1B", "FT (full)", "300,763 × 1",
        args=["--size", "1b", "--model", "runs/t5g-1b-full/final"]),
    Row("t5_4b_base", "enc-dec", "T5Gemma 2 4B", "base", "—", args=["--size", "4b"]),
    Row("t5_4b_ft", "enc-dec", "T5Gemma 2 4B", "FT (LoRA r 128)", "300,763 × 1",
        args=["--size", "4b", "--lora", "runs/t5g-4b-r128-full/lora.pt", "--r", "128", "--lora-mlp"]),
    Row("t5_4b_48k", "enc-dec", "T5Gemma 2 4B", "FT (LoRA r 128), first 48k", "48,000 of row t5_4b_ft's run",
        args=["--size", "4b", "--lora", "runs/t5g-4b-r128-full/lora_at_48000.pt", "--r", "128", "--lora-mlp"]),
    Row("mdlm120m_base", "diffusion", "chandohasam MDLM 120M", "base (pre-trained)", "—", args=["--model", "pilot"]),
    Row("mdlm120m_ft", "diffusion", "chandohasam MDLM 120M", "FT (E6 + T1)", "300,763 (E6 + T1)",
        args=["--model", "runs/e6-t1-120m"]),
    # 2 shards: each 523M process holds ≈ 8 GB of host memory (its checkpoint); 4 of them beside DiffusionGemma's
    # training left 17 GB available (2026-10-25)
    Row("mdlm523m_base", "diffusion", "chandohasam MDLM 523M", "base (pre-trained)", "—", True,
        ["--model", str(REPO / "diffusion_pretraining" / "runs" / "stage1-523m")], shards=2),
    Row("mdlm523m_ft", "diffusion", "chandohasam MDLM 523M", "FT (E6 + T1)", "300,763 (E6 + T1)", True,
        ["--model", "runs/e6-t1-523m"], shards=2),
    Row("dg_base", "diffusion", "DiffusionGemma 26B-A4B", "base", "—", args=["--prompt", "instruction"]),
    Row("dg_full", "diffusion", "DiffusionGemma 26B-A4B", "FT (LoRA r 16)", "300,763 × 1",
        args=["--lora", "runs/lora-full/lora.pt"]),
]
CELLS = {"free": (["baseline"], FREE_SEEDS), "constrained": (["masking_backtrack"], SEEDS),
         "extra": (["masking_only", "hybrid"], SEEDS)}


def cell_name(row: Row, cell: str, smoke: bool = False, new: bool = False, v2: bool = False) -> str:
    return f"grid_{row.key}_{cell}{'_smoke' if smoke else ''}{'_new' if new else ''}{'_v2' if v2 else ''}"


def command(row: Row, cell: str, smoke: bool = False, new: bool = False, v2: bool = False
            ) -> tuple[Path, list[str], Path]:
    """(working directory, argv, results.jsonl) of one cell; new: on the new prompts; v2: DAWG v2 A+B, all 100."""
    wd, argv, res = _command(row, cell, smoke, new, v2)
    if v2 and not row.key.startswith("t5"):            # through v2.py: [PY, -u, script, …] → [env V2_TARGET=…, PY, -u, v2.py, …]
        argv = ["env", f"V2_TARGET={wd / argv[2]}", PY, "-u", str(HERE / "v2.py"), *argv[3:]]
    return wd, argv, res


def _command(row: Row, cell: str, smoke: bool, new: bool, v2: bool) -> tuple[Path, list[str], Path]:
    modes, seeds = CELLS[cell]
    name = cell_name(row, cell, smoke, new, v2)
    ref = V2_REFERENCE if v2 else NEW_REFERENCE if new else REFERENCE
    lim = ["--limit", "1", "--meters", *SMOKE_METRES] if smoke else []
    # sharded runs: one process per smoke metre (4 shards over 2 metres left two shards empty, and they crashed)
    shards = str(min(len(SMOKE_METRES), row.shards) if smoke else row.shards)
    if row.key.startswith("nandi"):
        return AR, [PY, "-u", "constrained_sample.py", "--name", name, *row.args, "--reference", ref,
                    "--modes", *modes, "--seeds", *seeds, "--shards", shards, "--mask-workers", "2", *lim], \
            AR / "runs" / name / "results.jsonl"
    if row.key.startswith("gemma4"):
        return HERE, [PY, "-u", "run_hf.py", "--name", name, *row.args, "--reference", ref, "--modes", *modes,
                      "--seeds", *seeds, *lim], HERE / "runs" / name / "results.jsonl"
    if row.key.startswith("t5"):
        seed_args = ["--free-seeds", *seeds] if cell == "free" else ["--seeds", *seeds]
        return T5, [PY, "-u", "constrained_sample.py", "--name", name, *row.args, "--reference", ref,
                    "--modes", *modes, *seed_args, *lim, *(V2_T5 if v2 else [])], T5 / "runs" / name / "results.jsonl"
    if row.key.startswith("mdlm"):
        # the smoke cells sample 1 poem per metre (--e6-reference would take all 15 of each metre)
        pick = ["--meters", *SMOKE_METRES, "--e6-per-metre", "1"] if smoke else ["--e6-reference", ref]
        return DF, [PY, "-u", "constrained_sample.py", "--name", name, *row.args, "--e6-split", "test",
                    "--e6-data", str(E6D), *pick, "--modes", *modes, "--seeds", *seeds,
                    "--shards", shards, "--mask-workers", "2"], DF / "runs" / name / "results.jsonl"
    seed_args = ["--free-seeds", *seeds] if cell == "free" else ["--seeds", *seeds]
    return DG, [PY, "-u", "evaluate_e6.py", "--name", name, *row.args, "--reference", ref, "--modes", *modes,
                *seed_args, *lim], DG / "runs" / name / "results.jsonl"


def cells(kind: str = "core", smoke: bool = False):
    """(row, cell) pairs of a kind: core (and new) = free + constrained of every row; extra = the † rows' other
    strategies; v2 = every row's constrained cell."""
    out = []
    for row in ROWS:
        names = (["free", "constrained"] if kind in ("core", "new") else ["constrained"] if kind == "v2"
                 else (["extra"] if row.dagger else []))
        for c in names:
            out.append((row, c))
    return out


def done(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0 and (path.parent / "run.json").exists()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--todo", choices=("core", "extra", "smoke", "new", "v2", "v2smoke"))
    args = ap.parse_args()
    if args.todo:
        smoke, new, v2 = args.todo in ("smoke", "v2smoke"), args.todo == "new", args.todo.startswith("v2")
        for row, c in cells("v2" if v2 else "core" if smoke else args.todo):
            wd, argv, res = command(row, c, smoke, new, v2)
            if not done(res):
                print(f"{cell_name(row, c, smoke, new, v2)}\t{wd}\t{shlex.join(argv)}")
        return
    for kind in ("core", "extra", "new", "v2"):
        for row, c in cells(kind):
            wd, argv, res = command(row, c, new=kind == "new", v2=kind == "v2")
            print(f"{'done' if done(res) else 'todo'}  {cell_name(row, c, new=kind == 'new', v2=kind == 'v2'):36s} "
                  f"{res.relative_to(REPO)}")


if __name__ == "__main__":
    main()

"""Drop the page cache of the large model files (weights, checkpoints) so CUDA sees that memory: on the GB10 (unified
memory) torch.cuda.mem_get_info() reports about MemFree, and the page cache counts as used. Reads nothing; pages a
running process has mapped stay. No root needed (a sync, then posix_fadvise DONTNEED per file).

    .venv/bin/python experiments/scripts/evict_model_cache.py
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIRS = [Path.home() / ".cache" / "huggingface", ROOT / "t5_finetuning", ROOT / "autoregressive_finetuning",
        ROOT / "diffusion_finetuning" / "runs", ROOT / "diffusion_pretraining" / "runs", ROOT / "lora_gemma_diffusion"]
MIN_BYTES = 256 << 20


def meminfo(key: str) -> float:
    """/proc/meminfo's ``key`` in GB."""
    for line in open("/proc/meminfo"):
        if line.startswith(key + ":"):
            return int(line.split()[1]) / 2**20
    raise KeyError(key)


def main() -> int:
    before = meminfo("MemFree")
    os.sync()
    n = 0
    for d in DIRS:
        for dirpath, _, files in os.walk(d):
            for f in files:
                path = os.path.join(dirpath, f)
                try:
                    if os.path.islink(path) or os.path.getsize(path) < MIN_BYTES:
                        continue
                    fd = os.open(path, os.O_RDONLY)
                    try:
                        os.posix_fadvise(fd, 0, 0, os.POSIX_FADV_DONTNEED)
                    finally:
                        os.close(fd)
                    n += 1
                except OSError:
                    continue
    print(f"page cache of {n} model files dropped: MemFree {before:.0f} → {meminfo('MemFree'):.0f} GB "
          f"(MemAvailable {meminfo('MemAvailable'):.0f} GB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

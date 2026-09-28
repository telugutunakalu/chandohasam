"""Crash-safe checkpoints and power awareness for long runs.

Two checkpoint slots (ckpt_a.pt, ckpt_b.pt) are written alternately. Each save
goes to a temporary file that is fsync'ed before it atomically replaces the
older slot, so a power cut at any moment leaves at least one complete
checkpoint; loading picks the newest slot that reads back cleanly.
"""
from __future__ import annotations

import os
from pathlib import Path

import torch

SLOTS = ("ckpt_a.pt", "ckpt_b.pt")


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def save_checkpoint(run_dir: Path, state: dict) -> Path:
    slots = [run_dir / s for s in SLOTS]
    target = min(slots, key=lambda p: p.stat().st_mtime if p.exists() else -1.0)   # the older slot
    tmp = target.with_suffix(".tmp")
    with open(tmp, "wb") as fh:
        torch.save(state, fh)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, target)
    _fsync_dir(run_dir)
    return target


def load_latest(run_dir: Path, device) -> dict | None:
    """The complete checkpoint with the highest step, or None if there is none."""
    best = None
    for slot in (run_dir / s for s in SLOTS):
        if not slot.exists():
            continue
        try:
            state = torch.load(slot, map_location=device, weights_only=False)
        except Exception as exc:                      # truncated or corrupt: use the other slot
            print(f"skipping unreadable checkpoint {slot.name}: {exc}", flush=True)
            continue
        if best is None or state["step"] > best["step"]:
            best = state
    return best


def save_snapshot(run_dir: Path, ema: torch.nn.Module, step: int) -> None:
    """EMA weights only, in bf16: a permanent milestone for curves and stage-2 starts."""
    out = run_dir / "snapshots"
    out.mkdir(exist_ok=True)
    tmp = out / f"ema_step_{step:07d}.tmp"
    with open(tmp, "wb") as fh:
        torch.save({"step": step, "ema": {k: v.to(torch.bfloat16) for k, v in ema.state_dict().items()}}, fh)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, tmp.with_suffix(".pt"))


class PowerMonitor:
    """Reads mains/battery state from /sys/class/power_supply (None where unknown, e.g. a desktop)."""

    def __init__(self, root: Path = Path("/sys/class/power_supply")):
        self.mains = [d for d in root.glob("*") if (d / "type").exists() and (d / "type").read_text().strip() == "Mains"]
        self.batteries = [d for d in root.glob("*") if (d / "type").exists() and (d / "type").read_text().strip() == "Battery"]

    def on_mains(self) -> bool | None:
        if not self.mains:
            return None
        return any((d / "online").read_text().strip() == "1" for d in self.mains)

    def battery_percent(self) -> int | None:
        for d in self.batteries:
            try:
                return int((d / "capacity").read_text().strip())
            except (OSError, ValueError):
                continue
        return None

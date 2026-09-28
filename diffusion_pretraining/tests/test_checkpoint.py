from __future__ import annotations

import time

import torch

from mdlm.checkpoint import PowerMonitor, load_latest, save_checkpoint


def test_slots_alternate_and_newest_step_wins(tmp_path):
    save_checkpoint(tmp_path, {"step": 10, "w": torch.ones(3)})
    time.sleep(0.01)
    save_checkpoint(tmp_path, {"step": 20, "w": torch.ones(3) * 2})
    time.sleep(0.01)
    third = save_checkpoint(tmp_path, {"step": 30, "w": torch.ones(3) * 3})
    assert sorted(p.name for p in tmp_path.glob("ckpt_*.pt")) == ["ckpt_a.pt", "ckpt_b.pt"]
    assert third.name == "ckpt_a.pt"                               # overwrote the older slot
    assert load_latest(tmp_path, "cpu")["step"] == 30
    assert not list(tmp_path.glob("*.tmp"))


def test_a_corrupt_newest_slot_falls_back_to_the_other(tmp_path):
    save_checkpoint(tmp_path, {"step": 10})
    time.sleep(0.01)
    newest = save_checkpoint(tmp_path, {"step": 20})
    newest.write_bytes(newest.read_bytes()[:20])                   # a torn write
    assert load_latest(tmp_path, "cpu")["step"] == 10
    empty = tmp_path / "empty"
    empty.mkdir()
    assert load_latest(empty, "cpu") is None


def _supply(root, name, kind, **files):
    d = root / name
    d.mkdir()
    (d / "type").write_text(kind + "\n")
    for k, v in files.items():
        (d / k).write_text(f"{v}\n")


def test_power_monitor(tmp_path):
    _supply(tmp_path, "ADP1", "Mains", online=0)
    _supply(tmp_path, "BAT0", "Battery", capacity=42)
    pm = PowerMonitor(tmp_path)
    assert pm.on_mains() is False and pm.battery_percent() == 42
    (tmp_path / "ADP1" / "online").write_text("1\n")
    assert pm.on_mains() is True
    assert PowerMonitor(tmp_path / "ADP1").on_mains() is None      # no supplies found -> unknown

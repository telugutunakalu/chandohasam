"""Paths and loaders shared by the stage-2 (poem fine-tuning) tools.

The stage-1 code is reused unchanged from ../diffusion_pretraining: the `mdlm` package (model,
objective, data windows, evaluation, sampler) and the frozen tokenizer. Importing this module puts
that folder on sys.path.

Run every tool with the repo's venv from this folder, e.g. `../.venv/bin/python prepare_poems.py`.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PRETRAIN = REPO / "diffusion_pretraining"
if str(PRETRAIN) not in sys.path:
    sys.path.insert(0, str(PRETRAIN))

import torch                                                     # noqa: E402

from mdlm.diffusion import invalid_bias                          # noqa: E402
from mdlm.model import Denoiser, ModelConfig                     # noqa: E402
from tokenizer import load_default                               # noqa: E402

# Inputs (never committed: padyarchana_exports/ and models/ are gitignored)
PADYARCHANA = REPO / "padyarchana_exports" / "padyarchana_poems_v3.json"
DATASET = REPO / "dataset"
PILOT = HERE / "models" / "pilot120m"            # huggingface.co/samvaran/chandohasam @ 5e7ab314

# Outputs (gitignored)
DATA = HERE / "data"
TOKENS = DATA / "tokens"                         # <source>/{train,val,test}.bin, as mdlm.data expects
INDEX = DATA / "poems_index.jsonl"
RUNS = HERE / "runs"

TELUGU = ("ఀ", "౿")


def canonical(text: str) -> str:
    """Telugu letters and signs only: spacing, punctuation, digits, ZWJ/ZWNJ and ఁ removed.
    Two printings of the same poem differ mostly in these (the same rule as import_chandassu.canon)."""
    return "".join(ch for ch in text if TELUGU[0] <= ch <= TELUGU[1] and ch != "ఁ")


def tokenizer():
    """The frozen stage-1 tokenizer (telugu_alldomain, sha256 200c814d…)."""
    return load_default()


def special_ids(tok) -> dict:
    return {"mask": tok.special_to_id["<mask>"], "pad": tok.pad_id, "unk": tok.unk_id,
            "bos": tok.bos_id, "eos": tok.eos_id}


def output_bias(cfg: ModelConfig, tok, device) -> torch.Tensor:
    """-inf on ids the model never outputs (<mask>, <pad>, <unk>, vocabulary padding)."""
    ids = special_ids(tok)
    return invalid_bias(cfg.padded_vocab, tok.vocab_size, [ids["mask"], ids["pad"], ids["unk"]], device)


def pilot_config() -> ModelConfig:
    return ModelConfig(**json.loads((PILOT / "config.json").read_text(encoding="utf-8"))["model"])


def load_pilot(device="cpu") -> Denoiser:
    """The stage-1 model: EMA weights at step 76,000, float32 (huggingface.co/samvaran/chandohasam)."""
    from safetensors.torch import load_file
    model = Denoiser(pilot_config())
    model.load_state_dict(load_file(str(PILOT / "model.safetensors")), strict=True)
    return model.to(device)


def load_model(spec: str, device="cpu") -> tuple[Denoiser, str]:
    """The EMA weights of: ``pilot`` (the stage-1 model); a folder of huggingface.co/samvaran/chandohasam
    (model.safetensors + config.json, e.g. a downloaded mdlm-523m-padyam/); a checkpoint file written by finetune.py
    or ft.train; a run directory of ft.train or mdlm.train (its newest checkpoint slot); or an EMA snapshot
    (snapshots/ema_step_*.pt, whose model config is the run's config.json). Returns the model and a short description
    of the weights."""
    if spec == "pilot":
        return load_pilot(device), "pilot120m EMA, step 76,000"
    path = Path(spec)
    if (path / "model.safetensors").exists():               # the released weights: float32 EMA
        from safetensors.torch import load_file
        model = Denoiser(ModelConfig(**json.loads((path / "config.json").read_text(encoding="utf-8"))["model"]))
        model.load_state_dict(load_file(str(path / "model.safetensors")), strict=True)
        return model.to(device), f"{spec} (Hugging Face release)"
    # memory-mapped: only the EMA weights are read. A slot holds model, EMA and optimizer (8.4 GB for the 523M), and
    # mdlm.checkpoint.load_latest reads every slot whole: ≈ 14 GB per process, which beside DiffusionGemma's
    # training starved the GB10's shared memory (2026-10-25).
    if path.is_dir():
        from mdlm.checkpoint import SLOTS
        state = None
        for slot in (path / s for s in SLOTS):              # load_latest's rule: the highest step, skip unreadable
            if not slot.exists():
                continue
            try:
                st = torch.load(slot, map_location="cpu", weights_only=False, mmap=True)
            except Exception as exc:
                print(f"skipping unreadable checkpoint {slot.name}: {exc}", flush=True)
                continue
            if state is None or st["step"] > state["step"]:
                state = st
        if state is None:
            raise FileNotFoundError(f"no checkpoint in {path}")
    else:
        state = torch.load(path, map_location="cpu", weights_only=False, mmap=True)
    cfg = state.get("model_config")
    if cfg is None:                                       # a snapshot: bf16 EMA weights only
        run_dir = path.parent.parent if path.parent.name == "snapshots" else path.parent
        cfg = json.loads((run_dir / "config.json").read_text())["model"]
    model = Denoiser(ModelConfig(**cfg))
    model.load_state_dict({k: v.float() for k, v in state["ema"].items()})
    return model.to(device), f"{spec} EMA, step {state['step']}"


def mem_available_gb() -> float:
    """MemAvailable from /proc/meminfo. The GB10's GPU and CPU share this memory with the vLLM server."""
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) / 2**20
    return float("inf")


def cuda_free_gb() -> float:
    """What CUDA itself reports as free. On the GB10 this tracks MemFree, not MemAvailable: page cache
    counts as used, so it can be several GB below mem_available_gb(). 0 when the query itself fails: it creates
    the CUDA context, which needs memory too (2026-10-18: an E6 evaluation shard crashed here with "CUDA error: out
    of memory" while a trainer ran; the wait now retries instead)."""
    try:
        free, _ = torch.cuda.mem_get_info()
    except RuntimeError as exc:                       # torch.AcceleratorError is a RuntimeError
        print(f"CUDA memory query failed: {str(exc).splitlines()[0]}", flush=True)
        return 0.0
    return free / 2**30


def wait_for_memory(min_gb: float, what: str) -> None:
    """Block until both the system and CUDA report at least ``min_gb`` free, so a job never starves the
    shared machine (the vLLM server holds most of it)."""
    while (avail := min(mem_available_gb(), cuda_free_gb())) < min_gb:
        print(f"{what}: {avail:.1f} GB free, waiting for {min_gb:.0f} GB", flush=True)
        from mdlm.checkpoint_eval import _evict_large_files     # page cache counts against CUDA on the GB10
        _evict_large_files()
        time.sleep(60)

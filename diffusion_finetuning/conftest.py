"""Lets pytest (run from diffusion_finetuning/) import ft and, through it, mdlm, tokenizer and the engines."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ft  # noqa: E402,F401  (sets up the remaining paths)

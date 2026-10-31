import os
import subprocess
import time
from pathlib import Path

os.environ["HF_HUB_DISABLE_XET"] = "1"

PYTHON = "python3"  # needs mlx-lm installed (Apple Silicon only); point this at that venv
SCRIPT = str(Path(__file__).resolve().parent / "llm_judge_extra.py")

MODELS = [
    ("mlx-community/gemma-4-e2b-it-4bit", "gemma4_e2b", 3000),
    ("mlx-community/Llama-3.2-3B-Instruct-4bit", "llama3_2_3b", 500),
    ("mlx-community/Qwen2.5-7B-Instruct-4bit", "qwen2_5_7b", 500),
    ("mlx-community/Meta-Llama-3.1-8B-Instruct-4bit", "llama3_1_8b", 500),
    ("mlx-community/gemma-3-12b-it-4bit", "gemma3_12b", 500),
]


def cleanup_hf_cache(model_id):
    try:
        from huggingface_hub import scan_cache_dir
        cache_info = scan_cache_dir()
        for repo in cache_info.repos:
            if repo.repo_id == model_id:
                revisions = {rev.commit_hash for rev in repo.revisions}
                delete_strategy = cache_info.delete_revisions(*revisions)
                print(f"  freeing {delete_strategy.expected_freed_size_str} for {model_id}", flush=True)
                delete_strategy.execute()
    except Exception as e:
        print(f"  cleanup warning for {model_id}: {e}", flush=True)


for model_id, out_key, max_tokens in MODELS:
    print(f"\n{'='*20} EXTRA {model_id} ({out_key}) {'='*20}", flush=True)
    t0 = time.time()
    result = subprocess.run([PYTHON, SCRIPT, model_id, out_key, "", str(max_tokens)], env=os.environ)
    print(f"{model_id} finished rc={result.returncode} in {time.time()-t0:.1f}s", flush=True)
    cleanup_hf_cache(model_id)

print("\nALL_EXTRA_JUDGES_DONE", flush=True)

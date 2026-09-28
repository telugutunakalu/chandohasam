"""Download the stage-1 Telugu pretraining corpora into pretraining_datasets/raw/.

    uv run python -m data_prep.download                  # every source
    uv run python -m data_prep.download --only wikipedia  # one source

Each source is pinned to the dataset's current Hub commit. After downloading,
every file is checked against the Hub's size and LFS sha256, and
pretraining_datasets/raw/manifest.json records the repo, commit, licence and
per-file size/sha256, so the corpus can be rebuilt exactly.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
from pathlib import Path

from huggingface_hub import HfApi, snapshot_download

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "pretraining_datasets" / "raw"

# name -> (dataset repo, file patterns)
SOURCES = {
    "wikipedia": ("wikimedia/wikipedia", ["20231101.te/*.parquet"]),
    "sangraha": ("ai4bharat/sangraha", ["verified/tel/*.parquet"]),
    "indiccorp": ("ai4bharat/IndicCorpV2", ["data/te.txt"]),
}


def remote_files(api: HfApi, repo: str, revision: str, patterns: list[str]) -> list[dict]:
    """Files matching the patterns, with the size and sha256 the Hub reports."""
    out = []
    for folder in sorted({p.rsplit("/", 1)[0] for p in patterns}):
        for entry in api.list_repo_tree(repo, path_in_repo=folder, repo_type="dataset",
                                        revision=revision, expand=True):
            if not any(fnmatch.fnmatch(entry.path, p) for p in patterns) or entry.lfs is None:
                continue
            out.append({"path": entry.path, "size": entry.size, "sha256": entry.lfs.sha256})
    return sorted(out, key=lambda f: f["path"])


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 24), b""):
            h.update(block)
    return h.hexdigest()


def download(name: str, api: HfApi) -> dict:
    repo, patterns = SOURCES[name]
    info = api.dataset_info(repo)
    files = remote_files(api, repo, info.sha, patterns)
    total = sum(f["size"] for f in files)
    print(f"[{name}] {repo}@{info.sha[:10]}: {len(files)} files, {total / 1e9:.2f} GB", flush=True)
    local_dir = RAW_DIR / name
    snapshot_download(repo, repo_type="dataset", revision=info.sha, allow_patterns=patterns,
                      local_dir=local_dir, max_workers=8)
    for f in files:
        local = local_dir / f["path"]
        if local.stat().st_size != f["size"] or sha256_of(local) != f["sha256"]:
            raise RuntimeError(f"[{name}] {f['path']} does not match the Hub's size/sha256")
    print(f"[{name}] verified {len(files)} files", flush=True)
    card = info.card_data.to_dict() if info.card_data else {}
    return {"repo": repo, "revision": info.sha, "license": card.get("license"),
            "patterns": patterns, "local_dir": str(local_dir.relative_to(PROJECT_ROOT)),
            "downloaded_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "total_bytes": total, "files": files}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="+", choices=sorted(SOURCES), help="download only these sources")
    args = ap.parse_args(argv)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = RAW_DIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    api = HfApi()
    for name in args.only or list(SOURCES):
        manifest[name] = download(name, api)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"manifest: {manifest_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

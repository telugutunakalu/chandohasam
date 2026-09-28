"""Loading the consolidated Dvipada dataset and the subsets the paper refers to.

Record ids are positions in dwipada_consolidated.json (checked by sha256), so
every script and cache file agrees on which couplet is which.

Subsets (built by build_subsets.py, stored in outputs/subsets.json):
    all       34,134  every record in the consolidated file
    schema_a  28,062  records with chandassu_analysis/source (the dedup set)
    master    27,881  schema_a records that pass the paper's own analyser
                      (the paper's "Master (Validated)" corpus, Table 3)
"""
import hashlib
import json
import re
from functools import lru_cache

import config

# "తెలుగు: ..." (9.6k records) and "Telugu: ..." (358) prefixes left by the
# generation prompt; stripped before any length or similarity measurement.
_MEANING_PREFIX = re.compile(r"^\s*(?:తెలుగు|Telugu|English|ఆంగ్లం)\s*[:：]\s*", re.IGNORECASE)

# The paper's source names merge the two Bhagavatam files.
SOURCE_ALIASES = {"dwipada_bhagavatam2": "dwipada_bhagavatam"}


def file_sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@lru_cache(maxsize=1)
def load_records(verify: bool = True) -> tuple:
    """All records, each with an added integer 'id'. Cached per process."""
    path = config.DATASET_PATH
    if not path.exists() or path.stat().st_size < 1024:
        raise FileNotFoundError(
            f"{path} is missing or is a Git LFS pointer; set DSM_DATASET to the real file")
    if verify and file_sha256(path) != config.DATASET_SHA256:
        raise ValueError(f"{path} does not match the sha256 in the paper repo's LFS pointer")
    with open(path, encoding="utf-8") as f:
        records = json.load(f)
    for i, r in enumerate(records):
        r["id"] = i
    return tuple(records)


def load_subset(name: str) -> list:
    """Records of a named subset (see module docstring)."""
    subsets_path = config.OUTPUT_DIR / "subsets.json"
    if not subsets_path.exists():
        raise FileNotFoundError("run build_subsets.py first")
    ids = json.loads(subsets_path.read_text())["ids"][name]
    records = load_records()
    return [records[i] for i in ids]


def source_of(record) -> str:
    src = record.get("source") or "unknown"
    return SOURCE_ALIASES.get(src, src)


def clean_meaning(text: str) -> str:
    return _MEANING_PREFIX.sub("", text or "").strip()


def poem_lines(record) -> list:
    return [l.strip() for l in record["poem"].split("\n") if l.strip()]


def poem_flat(record) -> str:
    """Poem as one line (for sentence encoders and length measures)."""
    return " ".join(poem_lines(record))


def fields(record) -> dict:
    """The three texts the paper compares: verse, Telugu prose, English prose."""
    return {
        "poem": poem_flat(record),
        "te": clean_meaning(record.get("telugu_meaning")),
        "en": clean_meaning(record.get("english_meaning")),
    }

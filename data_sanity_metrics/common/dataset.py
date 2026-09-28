"""The four dataset files in ../dataset/ as one list of Poem records.

All four files share one record layout (see dataset/CORRECTIONS.md). Each is a
"corpus" here, named by its file stem, and every metric is reported per file.
They differ in where the annotation comes from:

    corpus                  Telugu bhavam + gloss                        metre label
    bhagavatam              the edition: `bhavam`, `teeka_pairs`          the edition
    vemana                  machine: `generated.bhavam/.prathipadartham`  heuristic
    kuchimanchi_timmakavi   machine: `generated.*`                        meter_engine / Kaggle Chandassu
    chandassu               machine: `generated.*`                        the Kaggle corpus

Every record with a Telugu bhavam also has `bhavam_en`, its meaning in English
(machine translation of that bhavam).

Bhagavatam splits each seesa poem in two records: the parent holds the seesa
lines, the child the closing geeti AND the bhavam of the whole poem. So
`Poem.bhavam_verse` of a child is the parent's lines followed by its own: the
verse its bhavam explains. Every other record's bhavam explains its own lines.
"""
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
import json
import unicodedata

import config


@dataclass(frozen=True)
class Poem:
    key: str                  # "<corpus>:<id>", unique across corpora
    corpus: str               # the dataset file stem: bhagavatam | vemana | kuchimanchi_timmakavi | chandassu
    id: str                   # the record's id in its file
    form: str                 # verse | prose
    metre: str | None         # metre label (the corpus's metre_roman), None when unlabelled
    label_source: str         # where the metre label comes from (edition, heuristic, engine, corpus, ...)
    work: str                 # the collection inside the corpus: a skandha, a satakam, or the author
    lines: tuple              # the record's own lines (pādas / printed half-lines)
    bhavam_verse: tuple       # the lines its bhavam explains (see module docstring)
    bhavam: str               # Telugu meaning, '' when absent
    bhavam_source: str        # 'edition' | 'machine' | ''
    bhavam_en: str            # English meaning, '' when absent
    gloss: tuple              # ((word, meaning), ...): teeka_pairs or generated.prathipadartham

    @property
    def text(self) -> str:
        """The record's verse, one pāda per line."""
        return "\n".join(self.lines)


def flat(lines) -> str:
    """Lines as one string (for sentence encoders and length measures)."""
    return " ".join(lines)


def _clean(text) -> str:
    return unicodedata.normalize("NFC", text or "").strip()


def _work(corpus: str, record: dict) -> str:
    if corpus == "bhagavatam":
        return f"skandha {record['skandha']}"
    if corpus == "chandassu":
        return record.get("skandha") or "chandassu"           # the satakam
    return corpus                                             # a single author


def _poem(corpus: str, record: dict, parent_lines: tuple) -> Poem:
    generated = record.get("generated") or {}
    edition_bhavam = _clean(record.get("bhavam"))
    machine_bhavam = _clean(generated.get("bhavam"))
    if edition_bhavam:
        bhavam, source = edition_bhavam, "edition"
        pairs = record.get("teeka_pairs") or []
    else:
        bhavam, source = machine_bhavam, ("machine" if machine_bhavam else "")
        pairs = generated.get("prathipadartham") or []
    lines = tuple(_clean(l) for l in record.get("verse") or [] if _clean(l))
    label_source = record.get("label_source") or ("edition" if corpus == "bhagavatam" else "none")
    return Poem(
        key=f"{corpus}:{record['id']}",
        corpus=corpus,
        id=record["id"],
        form=record.get("form") or "verse",
        metre=record.get("metre_roman"),
        label_source=label_source if record.get("metre_roman") else "none",
        work=_work(corpus, record),
        lines=lines,
        bhavam_verse=parent_lines + lines,
        bhavam=bhavam,
        bhavam_source=source,
        bhavam_en=_clean(record.get("bhavam_en")),
        gloss=tuple((_clean(p.get("word")), _clean(p.get("meaning"))) for p in pairs),
    )


@lru_cache(maxsize=None)
def load_records(corpus: str) -> tuple:
    """The raw records of one corpus, in file order."""
    path = config.DATASET_DIR / config.CORPORA[corpus]
    return tuple(json.loads(path.read_text(encoding="utf-8")))


@lru_cache(maxsize=None)
def load_poems(corpora: tuple = tuple(config.CORPORA), forms: tuple = ("verse",)) -> tuple:
    """Poems of the given corpora and forms, in corpus order then file order."""
    poems = []
    for corpus in corpora:
        records = load_records(corpus)
        by_id = {r["id"]: r for r in records}
        for r in records:
            if (r.get("form") or "verse") not in forms:
                continue
            parent = by_id.get(r.get("parent_id")) if r.get("parent_id") else None
            parent_lines = tuple(_clean(l) for l in parent["verse"] if _clean(l)) if parent else ()
            poems.append(_poem(corpus, r, parent_lines))
    return tuple(poems)


def with_bhavam(poems) -> list:
    """Poems that carry a Telugu bhavam (the units of levels 2 and 3)."""
    return [p for p in poems if p.bhavam]


def by_corpus(poems) -> dict:
    """{dataset file stem: [poems]}, in config.CORPORA order."""
    groups = defaultdict(list)
    for p in poems:
        groups[p.corpus].append(p)
    return {c: groups[c] for c in config.CORPORA if groups[c]}


def add_dataset_argument(parser) -> None:
    """--datasets: which dataset files a script measures (default: all four)."""
    parser.add_argument("--datasets", nargs="+", choices=list(config.CORPORA), default=list(config.CORPORA),
                        help="dataset files to measure, by file stem (default: all)")

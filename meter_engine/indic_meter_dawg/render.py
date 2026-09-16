# -*- coding: utf-8 -*-
"""
Write diagrams to disk and render DOT to SVG with the system ``dot`` when
it is installed. Owns all diagram I/O; diagram.py stays pure.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Optional

from . import diagram
from .builder import LineDawg, default_dawg


def dot_available() -> bool:
    return shutil.which("dot") is not None


def render_dot(dot_text: str, svg_path: Path) -> bool:
    """Render with Graphviz; False (and no file) when ``dot`` is missing or fails."""
    if not dot_available():
        return False
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(["dot", "-Tsvg", "-o", str(svg_path)], input=dot_text.encode("utf-8"),
                          capture_output=True, timeout=120)
    return proc.returncode == 0


def write_diagrams(out_dir: str | Path, dawg: Optional[LineDawg] = None, svg: bool = True,
                   include_slot_dfas: bool = True) -> list[Path]:
    """Write every diagram: rule cards (dot, mermaid md, svg), vritta trie,
    per-slot DFA pictures, index. Returns the files written."""
    dawg = dawg or default_dawg()
    out = Path(out_dir)
    meters = out / "meters"
    dfas = out / "dfa"
    meters.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    def put(path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        written.append(path)

    for spec in dawg.catalogue.concrete:
        dot = diagram.rule_card_dot(spec, dawg)
        put(meters / f"{spec.name}.dot", dot)
        mer = diagram.rule_card_mermaid(spec, dawg)
        put(meters / f"{spec.name}.md", f"# {spec.name_te} · {spec.name}\n\n```mermaid\n{mer}\n```\n")
        if svg and render_dot(dot, meters / f"{spec.name}.svg"):
            written.append(meters / f"{spec.name}.svg")
        if include_slot_dfas:
            for slot in spec.slots:
                d = diagram.dfa_dot(dawg.slot_dfas[(spec.name, slot)], f"{spec.name} / {slot}")
                put(dfas / f"{spec.name}__{slot}.dot", d)
                if svg and render_dot(d, dfas / f"{spec.name}__{slot}.svg"):
                    written.append(dfas / f"{spec.name}__{slot}.svg")
    trie = diagram.vritta_trie_dot(dawg)
    put(out / "vritta_trie.dot", trie)
    if svg and render_dot(trie, out / "vritta_trie.svg"):
        written.append(out / "vritta_trie.svg")
    put(out / "README.md", diagram.index_markdown(dawg))
    return written

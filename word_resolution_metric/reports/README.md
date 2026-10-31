# reports/

- `word_resolution_report.md` — the report: definitions, corpus, padarchana.db, approach and version history,
  architecture, sandhi, evaluation design, results, residue, roadmap (state as of 2026-10-28, pipeline v28).
- `word_resolution_report.pdf` / `.html` — the same, rendered (Chrome headless; Telugu in Noto Sans Telugu).
- `figures/` — diagrams (`*.dot` → `*.png`/`*.svg` with Graphviz) and charts (`make_charts.py`, reference palette),
  plus `md2html.py`, the small Markdown→HTML converter used for the PDF.

Regenerate after a new pipeline version (from `word_resolution_metric/`):

    cd reports/figures && for f in architecture decision_flow db_schema evaluation_loop; do dot -Tpng -Gdpi=150 $f.dot -o $f.png; dot -Tsvg $f.dot -o $f.svg; done
    ../../../.venv/bin/python make_charts.py            # edit the numbers at the top of each chart first
    cd .. && ../../.venv/bin/python figures/md2html.py word_resolution_report.md word_resolution_report.html
    google-chrome --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=word_resolution_report.pdf file://$PWD/word_resolution_report.html

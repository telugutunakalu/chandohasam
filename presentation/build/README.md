# Rebuilding the deck

`deck.js` generates `../chandohasam_seminar.pptx` with pptxgenjs; `fix_ppr.py` removes the duplicate
paragraph properties pptxgenjs writes for bold-lead bullets; `make_notes.py` writes `../notes.md` from the
speaker notes embedded in the deck.

```bash
npm install pptxgenjs            # once, in any folder; then point NODE_PATH at its node_modules
export NODE_PATH=/path/to/node_modules
export SKILL_DIR=~/.claude/skills/synced/*/pptx   # provides scripts/apply_theme.js (theme colours)
export OUT_DIR=$(pwd)/..                           # the presentation/ folder
node deck.js && python3 fix_ppr.py "$OUT_DIR/chandohasam_seminar.pptx" && python3 make_notes.py "$OUT_DIR"
soffice --headless --convert-to pdf "$OUT_DIR/chandohasam_seminar.pptx" --outdir "$OUT_DIR"
```

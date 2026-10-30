# Build the papers (ACL format) with XeLaTeX: `make` (main.pdf = mid-submission, final.pdf = final paper), `make figures`,
# `make clean`. Without XeLaTeX: `tectonic -X compile final.tex`.
# XeLaTeX is needed for the Telugu examples (Noto Sans Telugu) and the IAST diacritics (TeX Gyre Termes).
DOCS = main final
TEX = xelatex -interaction=nonstopmode -halt-on-error
DEPS = references.bib final_refs.bib acl.sty acl_natbib.bst figures/fig1_system_overview.pdf figures/fig2_dawg_two_panel.pdf \
       figures/fig3_experiments.pdf \
       $(wildcard tables/*.tex)

all: $(DOCS:=.pdf)

%.pdf: %.tex $(DEPS)
	$(TEX) $* > /dev/null
	bibtex $* > /dev/null
	$(TEX) $* > /dev/null
	$(TEX) $* > /dev/null
	@for i in 1 2 3; do grep -q "Rerun to get" $*.log || break; $(TEX) $* > /dev/null; done
	@grep -E "LaTeX Warning|Missing character|Overfull|Citation .* undefined" $*.log | sort | uniq -c || true

# The figures are drawn by writeups/scripts/make_paper_figures.py; references.bib by scripts/merge_citations.py.
figures:
	cd ../writeups/scripts && python3 make_paper_figures.py

references.bib:
	cd .. && python3 paper/scripts/merge_citations.py

tables:
	cd .. && python3 paper/scripts/make_rule_tables.py

clean:
	rm -f $(foreach d,$(DOCS),$(d).aux $(d).bbl $(d).blg $(d).log $(d).out)

.PHONY: all figures tables clean

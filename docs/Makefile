TEX := $(wildcard session_*.tex) project_nbody.tex
PDF := $(TEX:.tex=.pdf)

all: $(PDF)

%.pdf: %.tex preamble.tex
	latexmk -pdf -interaction=nonstopmode -halt-on-error $<

clean:
	latexmk -C
	rm -f *.aux *.log *.fls *.fdb_latexmk *.out

.PHONY: all clean

# Define filenames
TEX_FILE      := immigrationHeterogeneity.tex
PYTHON_SCRIPT := source/immigrantEffects.py
DATA_FILE     := results/tables/regressionTable.tex  
DAT_FILE      := data/Oreopoulos2011skilled.dta

# Define output filenames
PDF_FILE := $(TEX_FILE:.tex=.pdf)

# Define targets
all: $(PDF_FILE)


# Run Python script only if needed
$(DATA_FILE): $(PYTHON_SCRIPT) $(DAT_FILE)
	python3 $(PYTHON_SCRIPT)	
	
# Rule to generate PDF file from LaTeX
$(PDF_FILE): $(TEX_FILE) $(DATA_FILE)
	xelatex $(TEX_FILE)
	bibtex immigrationHeterogeneity.aux
	xelatex $(TEX_FILE)
	xelatex $(TEX_FILE)

# Rule to run Python script
run_python: $(PYTHON_SCRIPT)
	python3 $(PYTHON_SCRIPT)

# Clean rule
clean:
	rm -f $(PDF_FILE) *.aux *.log *.blg *.bbl

# Phony targets
.PHONY: all clean

# Define directories
LATEX_DIR := latex
PDF_DIR := docs/pdf
MKDOCS_DIR := docs

# Get list of LaTeX source files
LATEX_SRC := $(wildcard $(LATEX_DIR)/*.tex)

# Define PDF targets
PDFS := $(LATEX_SRC:$(LATEX_DIR)/%.tex=$(PDF_DIR)/%.pdf)

# Check for latexmk
LATEXMK := $(shell command -v latexmk)
ifeq ($(LATEXMK),)
    $(error "Error: 'latexmk' not found. Please install 'latexmk' to continue.")
endif

# Check for latexmk
LATEXMK := $(shell command -v latexmk)
ifeq ($(LATEXMK),)
    $(error "Error: 'latexmk' not found. Please install 'latexmk' to continue.")
endif

ENVIRON_PKG := $(shell kpsewhich environ.sty)
ifeq ($(ENVIRON_PKG),)
    $(info ===============================================)
    $(info Error: LaTeX package 'environ' not found.)
    $(info Please install it using your TeX distribution's package manager.)
    $(info Suggested methods of installation:)
    $(info )
    $(info - **On Debian/Ubuntu:**)
    $(info     sudo apt-get install texlive-latex-extra)
    $(info )
    $(info - **Using TeX Live with tlmgr:**)
    $(info     tlmgr install environ)
    $(info )
    $(info - **Using MiKTeX:**)
    $(info     Use the MiKTeX Package Manager to install 'environ')
    $(info )
    $(error LaTeX package 'environ' is missing.)
endif

# Default target
all: build

# Build target: compile LaTeX files and build MkDocs site
build: $(PDFS)
	@echo "Building MkDocs site..."
	mkdocs build

# Rule to build PDFs from LaTeX files
$(PDF_DIR)/%.pdf: $(LATEX_DIR)/%.tex
	@echo "Compiling $<..."
	mkdir -p $(PDF_DIR)
	latexmk -pdf -interaction=nonstopmode -output-directory=$(LATEX_DIR) $<
	@echo "Copying PDF to '$(PDF_DIR)/$*.pdf'"
	cp "$(LATEX_DIR)/$*.pdf" "$(PDF_DIR)/"

# Clean up auxiliary files
clean:
	@echo "Cleaning up..."
	latexmk -C -output-directory=$(LATEX_DIR) $(LATEX_SRC)

.PHONY: all build clean

MAKEFLAGS += -j auto

VENV ?= venv
PYTHON ?= $(VENV)/bin/python3
PYTHON_VERSION ?= 3.11

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
.PHONY: all
all: build

# Build target: compile LaTeX files and build MkDocs site
.PHONY: build
build: $(PDFS) $(VENV)/requirements.txt
	@echo "Building MkDocs site..."
	$(VENV)/bin/mkdocs build

# Rule to build PDFs from LaTeX files
$(PDF_DIR)/%.pdf: $(LATEX_DIR)/%.tex
	@echo "Compiling $<..."
	mkdir -p $(PDF_DIR)
	latexmk -pdf -interaction=nonstopmode -output-directory=$(LATEX_DIR) $<
	@echo "Copying PDF to '$(PDF_DIR)/$*.pdf'"
	cp "$(LATEX_DIR)/$*.pdf" "$(PDF_DIR)/"

.PHONY: setup
setup: $(VENV)/requirements.txt

requirements.txt: requirements.in | $(VENV)
	uv pip compile --python-version $(PYTHON_VERSION) --upgrade -o requirements.txt requirements.in

$(VENV)/requirements.txt: requirements.txt | $(VENV)
	VIRTUAL_ENV=$(VENV) uv pip install -r requirements.txt
	cp -f requirements.txt $(VENV)/requirements.txt

$(VENV):
	uv venv $(VENV)

.PHONY: clean
clean:
	latexmk -C -output-directory=$(LATEX_DIR) $(LATEX_SRC)
	find -name __pycache__ -type d -exec rm -rf '{}' \;
	find -name \*.pyc -type f -exec rm -f '{}' \;

.PHONY: distclean
distclean:
	rm -rf node_modules/ $(VENV)

.PHONY: serve
serve:
	$(VENV)/bin/mkdocs serve -a localhost:8888

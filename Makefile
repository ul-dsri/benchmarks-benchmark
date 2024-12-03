VENV ?= venv
PYTHON ?= $(VENV)/bin/python3
PYTHON_VERSION ?= 3.11
IMAGE ?= party-paper

# Define directories
LATEX_DIR := latex
LATEX_TABLE_DIR := $(LATEX_DIR)/tables
MKDOCS_DIR := docs
PDF_DIR := $(MKDOCS_DIR)/pdf
DATA_DIR := $(MKDOCS_DIR)/data
IMAGES_DIR := $(MKDOCS_DIR)/images
TABLE_MD := $(DATA_DIR)/table.md
TABLE_TEX := $(LATEX_DIR)/table.tex
SCRIPTS_DIR := scripts
NORMALIZER := $(SCRIPTS_DIR)/insert-normalization-lines.sh
DENORMALIZER := $(SCRIPTS_DIR)/remove-normalization-lines.sh
TABLE_GEN_SCRIPT := $(SCRIPTS_DIR)/generate_table.py
TABLE_COLOR_SCRIPT := $(SCRIPTS_DIR)/color_md_table.py
QUESTIONNAIRE_SCRIPT := $(SCRIPTS_DIR)/generate_questionnaire.py
QUESTIONNAIRE_HTML := $(DATA_DIR)/questionnaire.html
QUESTIONNAIRE_INPUT1:= $(SCRIPTS_DIR)/threat-registry-table.csv
QUESTIONNAIRE_INPUT2:= $(SCRIPTS_DIR)/risk-response-table.csv
TABLE_INPUT_FILE := table_list.csv
FIRST_PAGE_SCRIPT := $(SCRIPTS_DIR)/generate_first_page_image.py
FIRST_PAGE_PNG := $(IMAGES_DIR)/first_page.png

# Get list of LaTeX source files
LATEX_SRC := $(shell find $(LATEX_DIR) -name '*.tex' ! -name '*table.tex' ! -name 'appendix*.tex')

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

# Build target: compile LaTeX files, build MkDocs site, create HTML questionnaire
.PHONY: build
build: $(PDFS) $(TABLE_MD) $(TABLE_TEX) $(QUESTIONNAIRE_HTML) $(VENV)/requirements.txt
	@echo "Building MkDocs site..."
	$(VENV)/bin/mkdocs build

# Rule to generate the markdown tables
$(TABLE_MD): $(TABLE_GEN_SCRIPT) | $(DATA_DIR) $(VENV)/requirements.txt $(TABLE_INPUT_FILE)
	@echo "Generating markdown tables..."
	# Iterate through each line in the input file
	@while IFS=',' read -r doc_id gid output_file; do \
		echo "Generating table for document ID $$doc_id with GID $$gid, saving to $$output_file..."; \
		$(VENV)/bin/python $(TABLE_GEN_SCRIPT) --sheet_id $$doc_id --gid $$gid --format markdown --filename $(SCRIPTS_DIR)/$$output_file > $(DATA_DIR)/$$output_file.md; \
	done < $(TABLE_INPUT_FILE)
	$(VENV)/bin/python $(TABLE_COLOR_SCRIPT) $(SCRIPTS_DIR)/thresholds-table.csv $(SCRIPTS_DIR)/absolute-risk-summary-table.csv $(TABLE_MD)

# Rule to generate the latex tables
$(TABLE_TEX): $(TABLE_GEN_SCRIPT) | $(LATEX_TABLE_DIR) $(VENV)/requirements.txt $(TABLE_INPUT_FILE)
	@echo "Generating LaTeX tables..."
	# Iterate through each line in the input file
	@while IFS=',' read -r doc_id gid output_file; do \
		echo "Generating table for document ID $$doc_id with GID $$gid, saving to $$output_file..."; \
		$(VENV)/bin/python $(TABLE_GEN_SCRIPT) --sheet_id $$doc_id --gid $$gid --format latex --filename $(SCRIPTS_DIR)/$$output_file > $(LATEX_TABLE_DIR)/$$output_file.tex; \
	done < $(TABLE_INPUT_FILE)

# Rule to generate the HTML questionnaire table
$(QUESTIONNAIRE_HTML): $(TABLE_MD) $(DATA_DIR)
	@echo "Generating questionnaire.html file..."
	python3 $(QUESTIONNAIRE_SCRIPT) $(QUESTIONNAIRE_INPUT1) $(QUESTIONNAIRE_INPUT2) > $(QUESTIONNAIRE_HTML)

# Ensure the data directory exists
$(DATA_DIR):
	mkdir -p $(DATA_DIR)

# Ensure the latex table directory exists
$(LATEX_TABLE_DIR):
	mkdir -p $(LATEX_TABLE_DIR)

# Rule to build PDFs from LaTeX files
$(PDF_DIR)/%.pdf: $(LATEX_DIR)/%.tex $(VENV)/requirements.txt
	@echo "Compiling $<..."
	mkdir -p $(PDF_DIR)
	mkdir -p $(IMAGES_DIR)
	latexmk -pdf -interaction=nonstopmode -output-directory=$(LATEX_DIR) $<
	@echo "Generating first page image $<..."
	$(VENV)/bin/python $(FIRST_PAGE_SCRIPT) $(LATEX_DIR)/$*.pdf
	mv $(LATEX_DIR)/$*.pdf_first_page.png $(FIRST_PAGE_PNG)
	@echo "Copying PDF to '$(PDF_DIR)/$*.pdf'"
	mv "$(LATEX_DIR)/$*.pdf" "$(PDF_DIR)/$*.pdf"
	@echo "Normalizing $<"
	$(NORMALIZER) $<
	@echo "Compiling normalized PDF for $<..."
	latexmk -pdf -interaction=nonstopmode -output-directory=$(LATEX_DIR) $<
	@echo "Renaming and copying normalized PDF to $(PDF_DIR)"
	mv "$(LATEX_DIR)/$*.pdf" "$(PDF_DIR)/$*_normalized.pdf"
	@echo "Undoing normalize changes $<"
	$(DENORMALIZER) $<

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
	-latexmk -C -output-directory=$(LATEX_DIR) $(LATEX_SRC)
	-find -name __pycache__ -type d -exec rm -rf '{}' \;
	-find -name \*.pyc -type f -exec rm -f '{}' \;
	-find -name \*.pdf -type f -exec rm -f '{}' \;
	-rm -rf ./tmp
	-rm -rf $(DATA_DIR)
	-rm -f $(FIRST_PAGE_PNG)
	-rm -rf $(SCRIPTS_DIR)/*.csv

.PHONY: distclean
distclean: clean
	rm -rf node_modules/ $(VENV)

.PHONY: serve
serve:
	$(VENV)/bin/mkdocs serve -a localhost:8888

.PHONY: docker-build
docker-build:
	docker build -t $(IMAGE) .

.PHONY: docker-bash
docker-bash:
	docker run --rm -it -v `pwd`:/build -u `id -u` -e HOME=/build $(IMAGE) bash

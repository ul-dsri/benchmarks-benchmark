# Welcome to the party-paper repo

## Setup

You'll need to setup a venv and install the python requirements:
```
python3 -m venv venv
source venv/bin/activate
pip  install -r requirements.txt
```

Next, you'll need to ensure latexmk and environ.sty are available.
```
sudo apt install latexmk
sudo apt install texlive-latex-extra
```

## Building

Ensure you are in the `party-paper` directory, and run `make`. This will build the static site, and build all LaTeX (`*.tex`) files in the `party-paper/latex` directory.

Assuming that completes successfully you can view the site by running `mkdocs serve` and visiting the URL that is listed in the output.

## Adding LaTeX Files

Place the `.tex` files that will be made available on the site in the `party-paper/latex` directory.

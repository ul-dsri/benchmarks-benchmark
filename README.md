# Welcome to the benchmarks-benchmark repo

## Setup

You'll need to install `uv`, a replacement for `pip`, `venv`, and `pip-tools`:

```bash
python3 -m pip install uv
```

The `setup` targets then provisions a virtual environment and installs required
dependencies:

```bash
make setup
```

Next, you'll need to ensure `latexmk` and `environ.sty` are available:

```bash
sudo apt install latexmk
sudo apt install texlive-latex-extra
```

## Building

Run `make`. This will build the static site, and build all LaTeX (`*.tex`) files
in the `benchmarks-benchmark/latex` directory.

You can view the built site by running `make serve` and visiting the URL listed
in the output:

```bash
make serve
```

```console
$ make serve
venv/bin/mkdocs serve -a localhost:8888
INFO    -  Building documentation...
...
INFO    -  Documentation built in 0.30 seconds
INFO    -  [11:38:17] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO    -  [11:38:17] Serving on http://localhost:8888/
```

## Adding LaTeX Files

Place the `.tex` files that will be made available on the site in the
`benchmarks-benchmark/latex` directory.

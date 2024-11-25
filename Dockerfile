FROM python:3.11-bookworm

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        latexmk \
        poppler-utils \
        texlive-fonts-recommended \
        texlive-latex-recommended \
        texlive-latex-extra \
        texlive-science \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir uv

WORKDIR "/build"

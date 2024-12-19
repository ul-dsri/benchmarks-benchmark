# Introduction

## Purpose

This project streamlines the production and distribution of AI safety benchmark benchmarking. This includes making a PDF from LaTeX documents and a google sheet, an associated website, and an intake questionnaire. By automating data retrieval from Google Sheets, markdown and LaTeX table generation, PDF rendering from LaTeX, and site building via mkdocs, the goal is to provide researchers and maintainers with a consistent and up-to-date online reference. The static website captures current threats, mitigations, and other information related to the Benchmarks' Benchmark paper.

## Intended Audience

This documentation targets the technical maintainers and future contributors who need to understand the system’s architecture, how data flows through it, and how to maintain or adjust its components. While some background in static site generators, CI pipelines, and basic scripting is helpful, the goal is to offer a clear, high-level picture that guides readers through the existing codebase and workflow.

# High-level Architecture

## Overview
The system brings together several moving parts to generate a fully updated static site upon each run of the CI pipeline. Currently the CI runs only when repo changes are pushed. The GitLab CI pipeline fetches the latest data from Google Sheets, validates and transforms it into tables and a questionnaire, compiles LaTeX files into PDFs, and regenerates the mkdocs-based website. Artifacts like PDFs and the questionnaire may be stored on S3, while the site itself is deployed via GitLab’s static hosting. Additional services (like Cloudflare) may sit in front of the site for performance and distribution, but are not documented here. [@brett < please update this with relevant details]

## Graphviz Diagram

A detailed graphviz diagram (referenced in the repository) visually represents the data flows and script dependencies. This diagram can be quite detailed and might feel overwhelming at first glance. Consider using it as a reference when troubleshooting complex interactions or if you need to modify the workflow extensively. A simplified diagram or short narrative overview is provided here to reduce the learning curve.

## Key Components:

 - mkdocs site: Builds static HTML pages from markdown files, integrating tables and questionnaires into the site’s content structure. Configuration details (e.g., plugins, markdown extensions) are found in mkdocs.yml, the `docs` folder, and the `overrides` folder.
 - LaTeX Processing: Uses latexmk to compile LaTeX documents into PDFs. This happens automatically as part of the Makefile-driven `make build` process.
 - Data Retrieval: The `scripts/generate_tabe.py` python scripts automatically download CSV data from specified Google Sheets tabs. The `table_list.csv` file in the root of the repo is used by a makefile target to pick which sheets and tabs are read, and the filenames used for local storage.
 - Questionnaire Generation: The `scripts/generate_questionnaire.py` script transforms retrieved data into a static HTML table, intended to be linked by the mkdocs site for easy copy-paste into google docs so that Benchmark maintainers.
 - S3 Storage: Certain generated artifacts (PDFs, html questionnaire) may be uploaded to S3 if they have changed since the last run, ensuring access to a historical record of versions. This is controlled by the `.gitlab_ci.yml file` which calls the `scripts/conditionally_upload.sh` and `scripts/conditionally_upload_questionnaire.sh` scripts.
 - CI Pipeline (GitLab): A three-stage process (test, build, deploy) triggers the Makefile, orchestrates data fetching, table generation, PDF compilation, and pushes final outputs to GitLab Pages and S3 as needed.

# Data Flow and Dependencies

## Google Sheets Data:
At the heart of the system is a structured pipeline that pulls data from Google Sheets. A file named `table_list.csv` maps specific Google Sheets (identified by documentId and tabId) to local CSV filenames where the data is stored. For example:

'''
documentId,tabId,csvFileName
<GOOGLE_DOC_ID>,<TAB_ID>,threats.csv
<GOOGLE_DOC_ID>,<TAB_ID>,mitigations.csv
'''

The `Makefile` reads this mapping and passes the arguments to `scripts/generate_table.py` to download each tab’s data, storing it locally. The CSVs become the authoritative source for building markdown tables, summary tables, and the questionnaire.


## Tables & Questionnaire Integration:
Once data is available locally, the Makefile triggers scripts that transform the CSVs into markdown tables and an HTML questionnaire. These generated artifacts are then moved into the mkdocs `docs/` directory, where they are referenced by the site’s markdown pages. This ensures that on each build of the site the latest table data is propagated to the static site.


# Build and Deployment Process

## Makefile Coordination:
The Makefile orchestrates the various build steps—such as generating PDFs from LaTeX, pulling data from Google Sheets, creating markdown tables, and building the mkdocs site—by using clearly defined targets and dependencies. While the order doesn’t strictly matter (due to properly declared dependencies), the Makefile ensures each required artifact is up-to-date before the final site is built.

By invoking `make build` at the build stage in the CI pipeline, all these components are processed in the correct order without manually specifying sequences each time.


## CI Pipeline (GitLab) Overview:
The GitLab CI pipeline is triggered on every commit. It’s divided into three main stages:

 1. Test Stage: Checks for accidental inclusion of secrets in the repository and builds a Docker environment for subsequent jobs. `make setup` is run.
 2. Build Stage: Runs `make build` to perform all build tasks described above. This includes fetching fresh data, generating PDFs, building tables and the questionnaire, and build the mkdocs site.
 3. Deploy Stage: Deploys the newly built site to GitLab Pages and conditionally updates S3 with PDFs and the questionnaire if they’ve changed since the last run.

# Script Reference

The project uses a variety of shell and Python scripts to fetch data, generate artifacts, and manage conditional uploads. Below is a concise reference table to help orient new maintainers:

| Script Name | Description |
| --- | --- |
| `scripts/download_csv_data.py` | This script downloads the CSV files if they don't already exist locally. It accepts as arguments a sheet id, tab id, and desired output format (latex or markdown). This script is called by make while it is reading `table_list.csv`. |
| `scripts/generate_table.py` | This script generates the LaTeX and markdown formatted tables that are used in the website and LaTeX file. It accepts as arguments an input csv file, and the desired output format (latex or markdown). This script is called by two different make rules. One for the the markdown tables and the other for latex tables. |
| `scripts/conditional-upload.sh` | This script downloads the list of hashes (hashes.txt) from S3. Then it does a sha1sum on the normalized version of the PDF (produced by `make build`). If there is a matching hash in the list, no upload is performed. If there isn't a match, then the non-normalized PDF is uploaded. Note that the normalized PDFs are never uploaded, instead the list of normalized PDF hashes are uploaded. |
| `scripts/insert-normalization-lines.sh` | This adds a few lines of LaTeX to the start of a LaTeX document. The lines ensure that a call to `latexmk` with the same input produces a to-the-bit-match between latexmk runs. This is required in order for a consistent hash to be produced by a PDF. This script makes a conditional upload of the PDFs to S3 possible. |
| `scripts/remove-normalization-lines.sh` | This removes the normalization lines that the insert script adds.  Since the insert script modifies the input tex files in place without creating a temporary file, this script ensures that running `make build` multiple times locally won't produce repeated normalization inserts. Note that this script is only really relevant in the context of local development. In the context of CI, the build environment is recreated on each commit so there is no impact of temporarily modifying a source file. |
| `scripts/conditional-upload-questionnaire.sh` | This script downloads all version of the HTML questionnaire from S3. Then it compares the hash of the newly generated questionnaire against the hashes of the downloaded versions. If there isn't a hash-match, then the questionnaire is uploaded under two different names. The first is `questionnaire.html`, which ensures that a link to this path always points to the latest version. The second is intended to be an archival copy and follows the naming scheme `quesitonnaire_[YYYY-MM-DD]_[short-commit-hash].html`.|
| `scripts/color_md_table.py` | This script takes as input the `thresholds.csv` file and the `absolute-risk-summary-table.csv` when it is called from the `Makefile`. It produces as output the absolute-risk-summary table, but it colors the cell contents based on the thresholds defined in the thresholds.csv table. |
| `scripts/generate_first_page_image.py` | This script takes as input a PDF file and producers as output a PNG of the first page of the PDF. The output PNG resolution is currently not a paremeter, but can be modified by modifying the resolution defined in one line of the script. |
| main.py | This is only used by mkdocs macros.	When mkdocs builds the site, this script can retrieve lists of stored files (e.g., PDFs on S3) and generate markdown-formatted links or references for inclusion in pages. |

# Common Pitfalls and Known Issues

## Circular Dependency in Updates:
One of the more confusing issues is the circular dependency between building the site and uploading updated PDFs or questionnaires to S3. The mkdocs site is built first, which means that at build time, the site references either the old PDFs on S3 or the locally built ones that haven’t been uploaded yet. Only after the site is built does the S3 upload occur. This prevents an updated PDF from being hosted from S3 immediately. To sidestep this issue we choose to host the most recent version of the PDF directly from the static site.

## Changes to Sheet Structure:
If the Google Sheets’ tab names, column headers, or shape of the google sheets tables defined by named ranges change without updating `table_list.csv`, the google sheet named ranges, or table and questionnaire scripts, data retrieval and table generation can fail. Such changes must be coordinated to keep the pipeline running smoothly.

## Google Sheets Data Accuracy:
Each run of the CI downloads the contents of the google sheet anew. We are relying on an unauthenticated http `get` request to a publicly readable google sheet. The tabs being downloaded consist of named ranges from other tabs. The contents of those tabs are calculated values which are not always cached on the google sheets side. When download the CSV in `scripts/generate_table.py` there is logic that checks for all known values which indicate the calculated values are still loading. If a single cell is indicated as still loading, there is retry logic to wait a few seconds and try the download again. So far the only data accuracy failures that have occurred are when a previously unknown temporary placeholder was discovered. If an accuracy issue is encountered and there is an obvious placeholder being used, just add it to the list of checks in `scripts/generate_table.py`:

'''
if '#NAME?' not in csv_data and "Loading..." not in csv_data and "#ERROR!" not in csv_data: # make sure calculated fields have loaded
'''

## Multiple LaTeX files:
Note that the system is currently setup to build a pdf for each `*.tex` file (with some exclusions, see the `LATEX_SRC` assignment in the Makefile for details). Right now there is only one intended PDF to be built. This means that while the system should in theory supports building and uploading multiple PDFs, this has not explicitly been tested. If the ability to support multiple PDFs is not desired, there is a decent amount of logic simplification in the makefile and .gitlab-ci.yml scripts that could be achieved. However, the system is verified to be working as it is currently configured.

## High-Level Process Overview

# From Commit to Deployed Site (Bird’s-Eye View):

 1. Developer Commits Changes:
    Whenever someone pushes any commit to the repository, the GitLab CI pipeline is triggered.

 1. Test Stage:
    The pipeline first checks the repository for potential secrets, ensuring no sensitive credentials are committed. It also builds a Docker image that will be used for subsequent steps.

 1. Build Stage:
    Here, the Makefile is invoked. It:
        Pulls fresh data from Google Sheets.
        Generates the markdown tables and the HTML questionnaire.
        Compiles the LaTeX files into PDFs.
        Builds the mkdocs site using the newly updated data and PDFs.

 1. Deploy Stage:
    After a successful build, conditional upload scripts run to determine if new PDFs or a new questionnaire should be pushed to S3. The newly built site is then deployed to GitLab Pages, ensuring that the latest content is publicly accessible.

Over time, this cycle repeats with each commit, maintaining an up-to-date static site that reflects the latest data and documentation.

# Troubleshooting (Q&A Style)

Below are some quick pointers for common issues maintainers may encounter:

Q: What if PDFs fail to update on the site?
A: Check the CI pipeline logs to ensure that the LaTeX compilation step succeeded. Confirm that conditional-upload.sh detected a changed PDF and that the Deploy stage finished. If all steps passed, remember that the updated PDFs will only appear as a file with a date formatted name after they’ve been uploaded and then included in a subsequent site rebuild.

Q: How can I revert if the build breaks?
A: Since the site only updates on successful builds, a failed build won’t overwrite the currently hosted version. To fix the issue, revert the problematic commit or push a corrected commit. Once the pipeline succeeds again, the site will update accordingly.

Note that the single biggest risk to the reliability of the site is the fact that the build depends on an input (the google sheet) that is not tracked in the repo or explicitly versioned. It won't be immediately evident that a change to the google sheet has broken the site if a script change is landing at the same time as a google sheet change. However, if a commit revert back to a known-working commit still doesn't fix the build, then looking at the google sheet history should reveal a breaking change that hopefully can be restored.

Q: Data from Google Sheets didn’t update as expected. What now?
A: First, verify that table_list.csv is correct and that the sheet structure hasn’t changed. Check the Makefile output to ensure the CSV was successfully fetched and transformed. If headers or column names changed, update the scripts or the Google Sheets tabs to restore consistency.


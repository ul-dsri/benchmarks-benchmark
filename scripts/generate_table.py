import argparse
import csv
import os
import sys
import time

from pylatex.utils import escape_latex


# Function to generate a Markdown table
def generate_markdown_table(data):

    headers = list(data[0].keys())

    # Create the header row
    header_row = '| ' + ' | '.join(headers) + ' |'
    separator_row = '| ' + ' | '.join(['---'] * len(headers)) + ' |'

    # Create data rows
    data_rows = []
    for row in data:
        row_data = [row.get(h, '') for h in headers]
        data_row = '| ' + ' | '.join(row_data) + ' |'
        data_rows.append(data_row)

    # Combine all rows into the Markdown table
    table = [header_row, separator_row] + data_rows
    markdown_table = '\n'.join(table)
    return markdown_table


def threat_registry_start():
    return r"""
\renewcommand{\arraystretch}{1.3} % Increases row height by 30%
\begin{longtable}{|p{0.7cm}|p{0.7cm}|p{2.7cm}|p{7.8cm}|p{1.1cm}|}
\caption{\textbf{Threats to Reliability:}\\ Stage Column Key - \textbf{1:}Task Definition, \textbf{2:}Prompt Generation, \textbf{3:}Prompt Inference, \textbf{4:}Output Evaluation, \textbf{5:}Scoring, \textbf{6:}Grading Presentation, \textbf{7:}Maintenance}
\label{tab:threats-to-reliability} \\
\hline
\textbf{ID} & \textbf{Stage} & \textbf{Category} & \textbf{Threat to Reliability} & \textbf{Severity}\\
\hline
\endfirsthead
\hline
\textbf{ID} & \textbf{Stage} & \textbf{Category} & \textbf{Threat to Reliability} & \textbf{Severity}\\
\hline
\endhead
\hline
\endfoot
\hline
"""


def threat_registry_headers():
    return ["ID", "Stage", "Category", "Threat to Reliability", "Severity"]


def risk_response_start():
    return r"""
\renewcommand{\arraystretch}{1.3} % Increases row height by 30%
\begin{longtable}{|p{0.8cm}|p{0.4cm}|p{0.7cm}|p{0.7cm}|p{5cm}|p{5cm}|}
\caption{Risk Response Measures}
\label{tab:risk-response-measures} \\
\hline
\rotatebox{90}{\textbf{\makecell{Risk ID\\Mitigated}}} &
\rotatebox{90}{\textbf{\makecell{Mitigation \#}}} &
\rotatebox{90}{\textbf{\makecell{Reduction in\\Likelihood \%}}} &
\rotatebox{90}{\textbf{\makecell{Reduction in\\Severity \%}}} &
\textbf{Risk Short Description} &
\textbf{\makecell{Response Measure\\Description}}\\
\hline
\endfirsthead
\hline
\rotatebox{90}{\textbf{\makecell{Risk ID\\Mitigated}}} &
\rotatebox{90}{\textbf{\makecell{Mitigation \#}}} &
\rotatebox{90}{\textbf{\makecell{Reduction in\\Likelihood \%}}} &
\rotatebox{90}{\textbf{\makecell{Reduction in\\Severity \%}}} &
\textbf{Risk Short Description} &
\textbf{\makecell{Response Measure\\Description}}\\
\hline
\endhead
\hline
\endfoot
\hline
"""

def risk_response_headers():
    return ["Risk ID Mitigated", "Mitigation Number", "Reduction in Likelihood (Percent)", "Reduction in Severity (Percent)", "Risk Short Description", "Response Measure Description"]


# Function to generate a LaTeX table
def generate_latex_table(data, table_start, headers):

    # Figure out LaTeX table end
    if len(data) >= 15: # then use longtable
        latex_table_end = r'\end{longtable}'
    else:
        latex_table_end = r'\end{tabular}'
    
    # Begin building latex table
    latex_table = table_start

    # Add data rows
    for row in data:
        row_data = [str(escape_latex(row.get(h, ''))) for h in headers]
        data_row = ' & '.join(row_data) + r' \\ \hline' + '\n'
        latex_table += data_row

    # End LaTeX table
    latex_table += latex_table_end
    return latex_table


# Function to load data from a CSV file
def load_data_from_csv(filename):
    if os.path.exists(f"{filename}"):
        with open(f"{filename}", mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data_list = [row for row in reader]
        return data_list
    else:
        return None


def modify_threat_registry_data(data):
    for row in data:
        # Change the stage entry from "(1) Task Definition" to "1"
        row['Stage'] = row['Stage'].removeprefix('(').split(')')[0]
    return data


def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='Generate a markdown or latex formatted table from a csv file.')
    parser.add_argument('--format', choices=['markdown', 'latex', 'md', 'tex'], required=True, help='Output formats accepted: markdown, md, latex, or tex')
    parser.add_argument('--filename', required=True, help='Filename to use as input CSV data.')
    args = parser.parse_args()

    # Try loading data from local CSV first
    try:
        data_dict = load_data_from_csv(args.filename)
        if not data_dict:
            raise Exception(f"Unable to load csv data from filename {args.filename}")
    except Exception as e:
        raise Exception(f"Unable to load csv data: {e}")

    # Generate the table in the requested format
    if args.format in ['markdown', 'md']:
        table = generate_markdown_table(data_dict)
    elif args.format in ['latex', 'tex']:
        filename = os.path.basename(args.filename)
        if filename == "threat-registry-table.csv":
            table_start = threat_registry_start()
            headers = threat_registry_headers()
            data_dict = modify_threat_registry_data(data_dict)
        elif filename == "risk-response-table.csv":
            table_start = risk_response_start()
            headers = risk_response_headers()
        else: # we don't need to build any other tex table right now
            print(f"skipping LaTeX table build for input file {args.filename}", file=sys.stderr)
            return

        table = generate_latex_table(data_dict, table_start, headers)

    # Print the generated table
    print(table)


if __name__ == '__main__':
    main()


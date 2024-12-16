import argparse
import csv
import os
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

# Function to generate a LaTeX table
def generate_latex_table(data):

    headers = list(data[0].keys())

    column_format = ' | '.join(['l'] * len(headers))

    # Begin LaTeX table
    if len(data) >= 15: # then use longtable
        latex_table = '\\begin{longtable}{' + column_format + '}\n\\hline\n'
        latex_table_end = '\\end{longtable}'
    else:
        latex_table = '\\begin{tabular}{' + column_format + '}\n\\hline\n'
        latex_table_end = '\\end{tabular}'
    
    # Add header row
    header_row = ' & '.join(headers) + ' \\\\ \\hline\n'
    latex_table += header_row

    # Add data rows
    for row in data:
        row_data = [escape_latex(row.get(h, '')) for h in headers]
        data_row = ' & '.join(row_data) + ' \\\\ \\hline\n'
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
        table = generate_latex_table(data_dict)

    # Print the generated table
    print(table)


if __name__ == '__main__':
    main()


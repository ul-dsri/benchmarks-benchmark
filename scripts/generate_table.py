import csv
import requests
import argparse

from pylatex.utils import escape_latex


# Function to fetch table data from google sheet
def fetch_data(google_sheet_id='1TBwja07SuVgp3I9MB95MLdjKtrTqsQ-tFe7GFfLhmYw', gid=0):

    # build URL
    csv_url = f'https://docs.google.com/spreadsheets/d/{google_sheet_id}/export?format=csv&gid={gid}'

    # Make request & check status
    response = requests.get(csv_url)
    response.raise_for_status()

    # decode response
    csv_data = response.content.decode('utf-8')

    # parse csv data
    reader = csv.DictReader(csv_data.splitlines())

    # create list of dictionaries, one dict per row and column headers as keys
    data_list = [row for row in reader]

    return data_list


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


def main():
    # Parse cli arugments
    parser = argparse.ArgumentParser(description='Generate a table from a Google Sheet in Markdown or LaTeX format.')
    parser.add_argument('--format', choices=['markdown', 'latex', 'md', 'tex'], required=True, help='Output formats accepted: markdown, md, latex, or tex')
    parser.add_argument('--sheet_id', default='1TBwja07SuVgp3I9MB95MLdjKtrTqsQ-tFe7GFfLhmYw', help='Google sheet ID. Uses default if not specified.')
    parser.add_argument('--gid', default='0', help='Google sheet gid. Used to specify tab. Uses default of 0 if not specified.')
    args = parser.parse_args()

    data_dict = fetch_data(args.sheet_id, args.gid)

    if args.format == 'markdown' or args.format == 'md':
        table = generate_markdown_table(data_dict)
    elif args.format == 'latex' or args.format == 'tex':
        table = generate_latex_table(data_dict)
    else:
        raise ValueError("Invalid format specified.")

    print(table)


if __name__ == '__main__':
    main()


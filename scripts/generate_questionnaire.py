import csv
import sys

def read_csv_as_dicts(filename):
    """
    Reads a CSV file and returns a list of dictionaries, 
    where each row is a dictionary with keys from the header.
    """
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def read_headers(filename):
    """
    Reads a CSV file and returns a list of headers
    """
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the first row as headers
    return headers


def check_headers(risk_response_headers, threat_registry_headers):
    """
    Compares the list of passed in headers to the expected headers
    Returns true if both match, otherwise false
    """
    expected_risk_response_headers = [
        "Risk ID Mitigated",
        "Mitigation Number",
        "Reduction in Likelihood (Percent)",
        "Reduction in Severity (Percent)",
        "Risk Short Description",
        "Response Measure Description"
    ]
    
    expected_threat_registry_headers = [
        "ID",
        "Stage",
        "Number",
        "Category",
        "Threat to Reliability",
        "Severity",
        "Notes",
        "Reference"
    ]
    
    # Check if headers match the expected ones
    match1 = expected_risk_response_headers == risk_response_headers
    match2 = expected_threat_registry_headers == threat_registry_headers

    return match1 and match2


def nest_mitigations(threats, mitigations):
    '''
    Nests the mitigations within the corresponding threats
    Returns a list of dictionaries
    '''
    # Create a mapping of threats by their 'ID'
    threats_dict = {threat["ID"]: threat for threat in threats}

    # Add a empty list to each threat for storing mitigations
    for threat in threats_dict.values():
        threat["Mitigations"] = []

    # Match mitigations to the appropriate threat
    for mitigation in mitigations:
        risk_id = mitigation.get("Risk ID Mitigated")
        if risk_id in threats_dict:
            threats_dict[risk_id]["Mitigations"].append(mitigation)
        else:
            print(f"Warning: Mitigation with Risk ID {risk_id} does not match any threat.")

    # Return the nested structure as a list
    return list(threats_dict.values())


def refine(full_data):
    '''
    Creates a new list of dicts. Only includes the fields that will be presented
    '''
    rows = []

    for entry in full_data:
        row = {}
        row['ID'] = entry['ID']
        row['Stage'] = entry['Stage']
        row['Category'] = entry['Category']
        row['Threat to Reliability'] = entry['Threat to Reliability']
        row['Mitigations'] = []
        
        for mitigation in entry['Mitigations']:
            inner_row = {}
            inner_row['Mitigation Number'] = mitigation['Mitigation Number']
            inner_row['Response Measure Description'] = mitigation['Response Measure Description']
            row['Mitigations'].append(inner_row)
        rows.append(row)

    return rows


def set_top_border_width(row_index, col_span, border_width=3):
    """
    Builds a Google Docs API request to set the top border width of a table row.

    Args:
        row_index (int): The row index (zero-based) within the table.
        col_span (int): The number of columns to span within the table.
        width (int): The desired border width in points (default is 3).

    Returns:
        list: A list of Google Docs API requests to update the border width.
    """
    requests = []
    requests.append({
        "updateTableCellStyle": {
            "tableRange": {
                "tableCellLocation": {
                    "rowIndex": row_index,
                    "columnIndex": 0
                },
                "rowSpan": 1,
                "columnSpan": col_span
            },
            "tableCellStyle": {
                "borderTop": {
                    "width": {
                        "magnitude": border_width,
                        "unit": "PT"
                    },
                }
            },
            "fields": "borderTop"
        }
    })
    return requests


def build_table_header():
    '''
    Returns the table header as a list of request dicts
    '''
    requests = []
    headers = ["ID", "Stage", "Category", "Threat to Reliability", "Affirming Status"]
    for i, header in enumerate(headers):
        requests.append({
            "insertText": {
                "location": {"index": i},
                "text": header
            }
        })
        
        # add styling
        requests.append({
            "updateTextStyle": {
                "range": {
                    "startIndex": i,
                    "endIndex": i + len(header)
                },
                "textStyle": {
                    "bold": True,
                    "underline": True
                },
                "fields": "bold,underline"
            }
        })

    # merge the last cell to span 3 columns
    requests.append({
        "mergeTableCells": {
            "tableRange": {
                "tableCellLocation": {
                    "rowIndex": 0,
                    "columnIndex": len(headers) - 1     # last column
                },
                "rowSpan": 1,
                "columnSpan": 3
            }
        }
    })

    # Mark the header row as a table header
    requests.append({
        "updateTableRowStyle": {
            "tableRowStyle": {
                "tableHeader": True
            },
            "fields": "tableHeader",
            "tableStartLocation": {
                "index": 0
            }
        }
    })

    return requests


def build_table_rows(data):
    '''
    Returns the table rows as a list of request dicts. Takes the table row data as input
    '''
    requests = []
    row_index = 1   # Start after the header row

    for threat in data:
        # Add a row for the threat
        requests.append({
            "insertTableRow": {
                "tableStartLocation": {"index": row_index},
                "insertBelow": True
            }
        })


        threat_cells = [
            threat["ID"],
            threat["Stage"],
            threat["Category"],
            threat["Threat to Reliability"],
            "[your name here]",
            "Adopted",
            "Date"
        ]
        for col_index, cell_content in enumerate(threat_cells):
            requests.append({
                "insertText": {
                    "location": {"index": row_index},
                    "text": cell_content
                }
            })

        # make the top border of each threat row wider
        top_border_request = set_top_border_width(row_index, 7)
        requests.extend(top_border_request)

        # increment row since we're moving onto mitigations
        row_index += 1

        for mitigation in threat.get("Mitigations", []):
            requests.append({
                "insertTableRow": {
                    "tableStartLocation": {"index": row_index},
                    "insertBelow": True
                }
            })
            mitigation_cells = [
                "mitigations",
                mitigation['Mitigation Number'] + ": " + mitigation['Response Measure Description'],
                "",
                ""
            ]
            for col_index, cell_content in enumerate(mitigation_cells):
                requests.append({
                    "insertText": {
                        "location": {"index": row_index},
                        "text": cell_content
                    }
                })
        
            # merge the description cell to span 4 columns
            requests.append({
                "mergeTableCells": {
                    "tableRange": {
                        "tableCellLocation": {
                            "rowIndex": row_index,
                            "columnIndex": 1
                        },
                        "rowSpan": 1,
                        "columnSpan": 4
                    }
                }
            })

            row_index += 1

        # vertically merge the "mitigations" cells at the start of each mitigation row
        height = len(threat.get("Mitigations", []))
        if height > 0:
            requests.append({
                "mergeTableCells": {
                    "tableRange": {
                        "tableCellLocation": {
                            "rowIndex": row_index-height, # merges start at top and go down 
                            "columnIndex": 0
                        },
                        "rowSpan": height,
                        "columnSpan": 1  # Since it's a vertical merge, only 1 column is spanned
                    },
                    "tableStartLocation": {
                        "index": 0
                    }
                }
            })
    return requests


def build_html_table_header():
    '''
    Returns the table header as a list of html strings
    '''
    html = ["<tr>"]
    headers = ["ID", "Stage", "Category", "Threat to Reliability", "Affirming Status"]
    for i, header in enumerate(headers):
        if i == 0:
            html.append(f"<th colspan=\"1\" style=\"font-weight: bold; text-decoration: underline;\">{header}</th>")
        elif i == len(headers) -1:
            html.append(f"<th colspan=\"3\" style=\"font-weight: bold; text-decoration: underline;\">{header}</th>")
        else:
            html.append(f"<th style=\"font-weight: bold; text-decoration: underline;\">{header}</th>")

    html.append("</tr>")

    return html


def build_html_table_rows(data):
    '''
    Returns the table rows as a list of request dicts. Takes the table row data as input
    '''
    html = []

    for threat in data:
        # Add threat row
        html.append("<tr style=\"border-top: 9px solid black;\">")
        threat_cells = [
            threat["ID"],
            threat["Stage"],
            threat["Category"],
            threat["Threat to Reliability"],
            "[your name here]",
            "Adopted",
            "Date"
        ]
        for col_index, cell_content in enumerate(threat_cells):
            if col_index == 0: 
                html.append(f"<td style=\"border-top: 5px solid black;\" colspan=\"1\">{cell_content}</td>")
            elif col_index >= 5:
                html.append(f"<td style=\"border-top: 5px solid black; font-weight: bold; text-decoration: underline;\">{cell_content}</td>")
            else:
                html.append(f"<td style=\"border-top: 5px solid black;\">{cell_content}</td>")
        html.append("</tr>")

        # Add mitigations sub-rows
        mitigation_count = len(threat.get("Mitigations", []))
        #print(threat.get("Mitigations"))
        mitigation_progress = 0
        for mitigation in threat.get("Mitigations", []):
            html.append("<tr>")
            mitigation_cells = [
                "mitigations",
                mitigation['Mitigation Number'] + ": " + mitigation['Response Measure Description'],
                "",
                ""
            ]
            for col_index, cell_content in enumerate(mitigation_cells):
                if col_index == 0 and mitigation_progress == 0 and mitigation_count > 1:
                    html.append(f"<td rowspan=\"{mitigation_count}\">{cell_content}</td>")
                elif col_index == 0 and mitigation_progress != 0:
                    pass
                elif col_index == 1:
                    html.append(f"<td colspan=\"4\">{cell_content}</td>")
                else:
                    html.append(f"<td>{cell_content}</td>")
            html.append("</tr>")
            mitigation_progress += 1

    return html

def build_html_table(data):
    '''
    Returns a list of html table elements
    '''
    html = ["<table border='1'>"]

    # Add table header
    html.extend(build_html_table_header())
    # Add table rows
    html.extend(build_html_table_rows(data))

    html.append("</table>")
    return "\n".join(html)


def build_table(data):
    '''
    Returns a list of requests to build a gdocs table
    '''
    requests = []

    # Start table
    total_rows = sum(1 + len(threat["Mitigations"]) for threat in data)
    requests.append({
        "insertTable": {
            "rows": total_rows + 1, # +1 for the header row
            "columns": 7
        }
    })

    # Add table header
    requests.extend(build_table_header())
    # Add table rows
    requests.extend(build_table_rows(data))

    return requests


def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python script.py <threat-registry.csv> <risk-response.csv>")
        sys.exit(1)

    # Get filenames from command-line arguments
    threat_registry_file = sys.argv[1]
    risk_response_file = sys.argv[2]

    # Get headers from CSV files
    response_headers = read_headers(risk_response_file)
    threat_headers = read_headers(threat_registry_file)

    if not check_headers(response_headers, threat_headers):
        print(f"Unexpected headers found: {response_headers}, {threat_headers}")
        print("Unable to proceed")
        sys.exit(1)

    # Read both files into lists of dictionaries
    threat_registry = read_csv_as_dicts(threat_registry_file)
    risk_response = read_csv_as_dicts(risk_response_file)

    # Nest and refine data to only what is needed
    nested = nest_mitigations(threat_registry, risk_response)
    refined = refine(nested)

    # translate refined data into a gdocs table
    requests = build_table(refined)

    table = build_html_table(refined)
    
    print(table)

if __name__ == "__main__":
    main()


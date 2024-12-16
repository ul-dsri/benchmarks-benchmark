import csv
import argparse

# Function to read the thresholds and color mappings from a CSV file
def read_thresholds_from_csv(filename):
    thresholds = {}
    color_mapping = {}
    
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        
        # Read all rows except the last row (which contains colors)
        rows = list(reader)
        color_row = rows[-1]  # The last row contains the color codes
        
        for row in rows[:-1]:
            category = row[0]
            thresholds[category] = [int(x) if x.isdigit() else x for x in row[1:-1]]  # Skip last column (color)
        
        # Extract colors from the last row
        color_mapping = {
            header[i]: color_row[i] for i in range(1, len(color_row))  # Skip the category column
        }

    return thresholds, color_mapping


# Function to read data from a CSV file
def read_data_from_csv(filename):
    data = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    
    return data

# Function to determine the color based on the thresholds and color mapping
def get_color_for_value(category, value, thresholds, color_mapping):
    category_thresholds = thresholds.get(category, [])
    if not category_thresholds:
        return None  # Return None if the category is not in the table

    try:
        category_thresholds = [float(threshold) for threshold in category_thresholds]
    except:
        raise TypeError(f"Unable to typecast an entry in {category_thresholds} to float")
    
    # Determine the color based on the value and thresholds
    if value >= category_thresholds[0]:
        return color_mapping['Best in Class']
    elif value >= category_thresholds[1]:
        return color_mapping['Research Grade']
    elif value >= 0:
        return color_mapping['Non-reliable']
    else:
        return None  # No color for values below the lowest threshold

# Function to generate a Markdown table with color applied
def generate_colored_markdown_table(data, thresholds, color_mapping):
    headers = list(data[0].keys())

    # Create the header row
    header_row = '| ' + ' | '.join(headers) + ' |'
    separator_row = '| ' + ' | '.join(['---'] * len(headers)) + ' |'

    # Create data rows with color
    data_rows = []
    for row in data:
        row_data = []
        for i, (header, value) in enumerate(row.items()):
            # Lookup the category (first column), and get the appropriate color for each value
            category = row['Reliability Category']  # Assuming first column is the category
            try:
                value = float(value)  # Attempt to convert value to float for threshold comparison
            except ValueError:
                row_data.append(value)  # If it's not a number, just add the value as it is
                continue

            # Get the color for the current value
            color = get_color_for_value(category, value, thresholds, color_mapping)
            if color:
                row_data.append(f'<span style="background-color:{color}; color:black;">{value}</span>')  # Apply color
            else:
                row_data.append(str(value))  # No color if the value is outside the thresholds

        # Join the row with colors applied
        data_row = '| ' + ' | '.join(row_data) + ' |'
        data_rows.append(data_row)

    # Combine all rows into the Markdown table
    table = [header_row, separator_row] + data_rows
    markdown_table = '\n'.join(table)
    return markdown_table

# Main function to parse arguments and run the script
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate a colored Markdown table from CSV files.")
    parser.add_argument('thresholds_file', help="CSV file containing the threshold data")
    parser.add_argument('data_file', help="CSV file containing the data")
    parser.add_argument('output_file', help="Output file to save the generated Markdown table")

    args = parser.parse_args()

    # Read the thresholds and color mappings from the thresholds CSV
    thresholds, color_mapping = read_thresholds_from_csv(args.thresholds_file)

    # Read the data from the data CSV
    data = read_data_from_csv(args.data_file)

    # Generate the colored Markdown table
    markdown_table = generate_colored_markdown_table(data, thresholds, color_mapping)

    # Write the Markdown table to the output file
    with open(args.output_file, 'w', encoding='utf-8') as file:
        file.write(markdown_table)

    print(f"Generated colored Markdown table saved to {args.output_file}")

if __name__ == '__main__':
    main()


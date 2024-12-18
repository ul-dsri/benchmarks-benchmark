import argparse
import csv
import os
import requests
import time

# Function to fetch table data from google sheet
def fetch_data(google_sheet_id='1TBwja07SuVgp3I9MB95MLdjKtrTqsQ-tFe7GFfLhmYw', gid=0):

    retries = 20
    delay = 2

    # build URL
    csv_url = f'https://docs.google.com/spreadsheets/d/{google_sheet_id}/export?format=csv&gid={gid}'

    for attempt in range(retries):

        # Make request & check status
        response = requests.get(csv_url)
        response.raise_for_status()

        # decode response
        csv_data = response.content.decode('utf-8')

        if '#NAME?' not in csv_data and "Loading..." not in csv_data and "#ERROR!" not in csv_data: # make sure calculated fields have loaded
            # parse csv data
            reader = csv.DictReader(csv_data.splitlines())

            # create list of dictionaries, one dict per row and column headers as keys
            data_list = [row for row in reader]

            # filter out nearly empty rows
            filtered_data = [
                row for row in data_list if len([value for value in row.values() if value and value.strip() not in ["", "#N/A", "null"]]) >= 3
            ]
            return filtered_data
        else:
            print(f"Google sheet data not loaded on attempt {attempt}. Waiting {delay} seconds and retrying")

        time.sleep(delay)

    raise Exception(f"Failed to fetch sheet data after {retries} retries")


# Function to write the generated table to a CSV file
def write_to_csv(data, filename):
    # Write the data to a CSV file
    with open(f"{filename}.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


# Function to load data from a CSV file
def load_data_from_csv(filename):
    if os.path.exists(f"{filename}.csv"):
        with open(f"{filename}.csv", mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data_list = [row for row in reader]
        return data_list
    else:
        return None


def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='Download Google Sheet data and save as a CSV.')
    parser.add_argument('--sheet_id', default='1TBwja07SuVgp3I9MB95MLdjKtrTqsQ-tFe7GFfLhmYw', help='Google sheet ID. Uses default if not specified.')
    parser.add_argument('--gid', default='0', help='Google sheet gid. Used to specify tab. Uses default of 0 if not specified.')
    parser.add_argument('--filename', required=True, help='Filename (without extension) to save the output CSV data.')
    args = parser.parse_args()

    # Try loading data from local CSV first
    data_dict = load_data_from_csv(args.filename)

    if not data_dict: # Download CSV and save to file
        data_dict = fetch_data(args.sheet_id, args.gid)
        # Write the fetched data to a CSV for future use
        write_to_csv(data_dict, args.filename)
    else:
        return True

if __name__ == '__main__':
    main()


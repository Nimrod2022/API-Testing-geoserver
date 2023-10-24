import requests
import csv

# Define the API endpoint URL
url = "https://api.unhcr.org/population/v1/asylum-applications/"

# Define the parameters
params = {
    "limit": 100000,
    "yearFrom": 2013,
    "yearTo": 2022,
    "coo": "UKR",
    "coa": "AUT",
    "cf_type": "iso"
}

# GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Define the output CSV file name
    output_csv_filename = "asylum_data_output.csv"

    # Open the CSV file for writing
    with open(output_csv_filename, 'w', newline='') as csvfile:
        # Create a CSV writer
        csv_writer = csv.writer(csvfile)

        # Write the header row
        csv_writer.writerow(["year", "coo_name", "coa_name", "applied"])

        # Extract and write data to the CSV file
        for item in data.get("items", []):
            year = item.get("year", "")
            coo_name = item.get("coo_name", "")
            coa_name = item.get("coa_name", "")
            applied = item.get("applied", "")

            # Write the data as a row in the CSV file
            csv_writer.writerow([year, coo_name, coa_name, applied])

    print(f"Data has been written to {output_csv_filename}.")
else:
    print("Failed to retrieve data. Status code:", response.status_code)

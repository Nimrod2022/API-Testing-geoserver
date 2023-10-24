import requests
import csv

# Define the API endpoint URL
url = "https://api.unhcr.org/population/v1/asylum-applications/"

# Define the parameters
year_range = range(2013, 2023)
coo = "UKR"
coa_countries = ["AUT", "DEU", "ITA", "GBR", "SWE", "SWI"]

# Define the output CSV file name
output_csv_filename = "asylum_data_output.csv"

# Open the CSV file for writing
with open(output_csv_filename, 'w', newline='') as csvfile:
    # Create a CSV writer
    csv_writer = csv.writer(csvfile)

    # Write the header row
    csv_writer.writerow(["year", "coo_name", "coa_name", "applied"])

    # Loop through the coa_countries
    for coa in coa_countries:
        for year in year_range:
            page = 1
            while True:
                # Define the parameters for the API request, including the page
                params = {
                    "limit": 100,  # Adjust the limit per page as needed
                    "yearFrom": year,
                    "yearTo": year,
                    "coo": coo,
                    "coa": coa,
                    "cf_type": "iso",
                    "page": page
                }

                # Make a GET request to the API
                response = requests.get(url, params=params)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Parse the JSON response
                    data = response.json()

                    # Extract and write data to the CSV file
                    for item in data.get("items", []):
                        coo_name = item.get("coo_name", "")
                        coa_name = item.get("coa_name", "")
                        applied = item.get("applied", "")

                        # Write the data as a row in the CSV file
                        csv_writer.writerow([year, coo_name, coa_name, applied])

                    # Check if there are more pages
                    if data.get("maxPages", 1) <= page:
                        break
                    else:
                        page += 1
                else:
                    print(f"Failed to retrieve data for coa={coa}, year={year}, page={page}. Status code:",
                          response.status_code)
                    break

print(f"Data has been written to {output_csv_filename}.")

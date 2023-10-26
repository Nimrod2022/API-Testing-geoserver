import requests
import psycopg2

# Base API endpoint URL
url = "https://api.unhcr.org/population/v1/asylum-decisions/"

# Define the parameters
year_range = range(2013, 2023)
coo = "UKR"
coa_countries = ["AUT", "DEU", "ITA", "GBR", "SWE", "SWI"]

# Database connection parameters
db_params = {
    "dbname": "migration",
    "user": "postgres",
    "password": "####",
    "host": "localhost"
}

# Open a connection to the PostgreSQL database
conn = psycopg2.connect(**db_params)

# Create a cursor object
cursor = conn.cursor()

# Table name to check and potentially delete
table_name = "asylum_decisions"

# Check if the table exists, and delete it if it does
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# Commit the deletion and close the cursor
conn.commit()
cursor.close()

# Reopen the cursor and create the new table
cursor = conn.cursor()

# Create the table with the schema
create_table_query = """
CREATE TABLE IF NOT EXISTS {table_name} (
    year integer,
    coo_name text,
    coa_name text,
    procedure_type text,
    app_type text,
    dec_level text,
    dec_recognized integer,
    dec_other integer,
    dec_rejected integer,
    dec_closed integer,
    dec_total integer
);
""".format(table_name=table_name)
cursor.execute(create_table_query)

# Commit the table creation
conn.commit()

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

                # Loop through the items in the response
                for item in data.get("items", []):
                    year = item.get("year", "")
                    coo_name = item.get("coo_name", "")
                    coa_name = item.get("coa_name", "")
                    procedure_type = item.get("procedure_type", "")
                    app_type = item.get("app_type", "")
                    dec_level = item.get("dec_level", "")
                    dec_recognized = item.get("dec_recognized", 0)  # Default to 0 if missing
                    dec_other = item.get("dec_other", 0)
                    dec_rejected = item.get("dec_rejected", 0)
                    dec_closed = item.get("dec_closed", 0)
                    dec_total = item.get("dec_total", 0)

                    # Insert data into the PostgreSQL database
                    cursor.execute(
                        "INSERT INTO asylum_decisions (year, coo_name, coa_name, procedure_type, app_type, dec_level, "
                        "dec_recognized, dec_other, dec_rejected, dec_closed, dec_total) VALUES (%s, %s, %s, %s, %s, %s, "
                        "%s, %s, %s, %s, %s)",
                        (year, coo_name, coa_name, procedure_type, app_type, dec_level, dec_recognized, dec_other,
                         dec_rejected, dec_closed, dec_total)
                    )

                # Check if there are more pages
                if data.get("maxPages", 1) <= page:
                    break
                else:
                    page += 1
            else:
                print(f"Failed to retrieve data for coa={coa}, year={year}, page={page}. Status code:",
                      response.status_code)
                break

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()

print("Data has been written to the PostgreSQL database.")

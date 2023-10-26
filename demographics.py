import requests
import psycopg2

# Base API endpoint URL
url = "https://api.unhcr.org/population/v1/demographics/"

# Define the parameters
year_range = range(2013, 2023)
coo = "UKR"
coa_countries = ["AUT", "DEU", "ITA", "GBR", "SWE", "SWI"]

# ["AUT", "DEU", "ITA", "GBR", "SWE", "SWI", "FRA", "ESP", "NLD", "BEL", "GRC", "PRT", "POL"]

# Database connection parameters
db_params = {
    "dbname": "migration",
    "user": "postgres",
    "password": "##",
    "host": "localhost"
}

# Open a connection to the PostgreSQL database
conn = psycopg2.connect(**db_params)

# Create a cursor object
cursor = conn.cursor()

# Table name to check and potentially delete
table_name = "demographics"

# Check if the table exists, and delete it if it does
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# Commit the deletion and close the cursor
conn.commit()
cursor.close()

# Reopen the cursor and create the new table with the specified schema
cursor = conn.cursor()

# Create the table with the schema
create_table_query = """
CREATE TABLE IF NOT EXISTS {table_name} (
    year integer,
    coo_name text,
    coa_name text,
    f_0_4 integer,
    f_5_11 integer,
    f_12_17 integer,
    f_18_59 integer,
    f_60 integer,
    m_0_4 integer,
    m_5_11 integer,
    m_12_17 integer,
    m_18_59 integer,
    m_60 integer,
    m_total integer,
    f_total integer
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
                "limit": 10000,
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
                    item_year = item.get("year", "")
                    coo_name = item.get("coo_name", "")
                    coa_name = item.get("coa_name", "")
                    f_0_4 = item.get("f_0_4", 0)
                    f_5_11 = item.get("f_5_11", 0)
                    f_12_17 = item.get("f_12_17", 0)
                    f_18_59 = item.get("f_18_59", 0)
                    f_60 = item.get("f_60", 0)
                    m_0_4 = item.get("m_0_4", 0)
                    m_5_11 = item.get("m_5_11", 0)
                    m_12_17 = item.get("m_12_17", 0)
                    m_18_59 = item.get("m_18_59", 0)
                    m_60 = item.get("m_60", 0)
                    m_total = item.get("m_total", 0)
                    f_total = item.get("f_total", 0)

                    # Insert data into the PostgreSQL database
                    cursor.execute(
                        "INSERT INTO demographics (year, coo_name, coa_name, f_0_4, f_5_11, f_12_17, f_18_59, f_60, "
                        "m_0_4, m_5_11, m_12_17, m_18_59, m_60, m_total, f_total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, "
                        "%s, %s, %s, %s, %s, %s, %s)",
                        (item_year, coo_name, coa_name, f_0_4, f_5_11, f_12_17, f_18_59, f_60, m_0_4, m_5_11, m_12_17,
                         m_18_59, m_60, m_total, f_total)
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

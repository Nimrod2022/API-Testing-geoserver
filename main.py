import requests

# Define the API endpoint URL
url = "https://api.unhcr.org/population/v1/asylum-applications/"

# Define the parameters
params = {
    "limit": 100000,
    #"page": 5,
    "yearFrom": 2013,
    "yearTo": 2022,
    "coo": "UKR",
    "coa": "AUT",
    # "coo_all": False,
    # "coa_all": False,
    "cf_type": "iso"
}

# Make a GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Do something with the data, for example, print it
    print(data)
else:
    print("Failed to retrieve data. Status code:", response.status_code)

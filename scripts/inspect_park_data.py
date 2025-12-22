import os
import json
import requests
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.environ.get("NPS_API_KEY")
NPS_API_URL = "https://developer.nps.gov/api/v1/parks"

def inspect_park(park_code="yose"):
    if not API_KEY:
        print("Error: NPS_API_KEY not set.")
        return

    print(f"Fetching data for {park_code}...")
    
    # Fetching with 'amenities' and 'accessibility' if possible, 
    # but standard /parks endpoint usually returns a lot. 
    # Let's try to ask for specific fields if the API supports it, 
    # or just get the default full object.
    # According to docs, 'fields' param can include 'amenities', 'accessibility' etc.
    # Let's try adding some fields.
    
    params = {
        "api_key": API_KEY,
        "parkCode": park_code,
        "fields": "accessibility,amenities,entranceFees" # Requesting extra fields
    }
    
    response = requests.get(NPS_API_URL, params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return

    data = response.json()
    
    if not data.get("data"):
        print("No data found.")
        return

    park_data = data["data"][0]
    
    # Try fetching amenities for the park
    print(f"Fetching amenities for {park_code}...")
    amenities_url = "https://developer.nps.gov/api/v1/amenities/parksplaces"
    params_amenities = {
        "api_key": API_KEY,
        "parkCode": park_code,
        "limit": 100
    }
    
    response_amenities = requests.get(amenities_url, params=params_amenities)
    if response_amenities.status_code == 200:
        amenities_data = response_amenities.json()
        output_file_amenities = f"data/sample_{park_code}_amenities.json"
        with open(output_file_amenities, "w") as f:
            json.dump(amenities_data, f, indent=2)
        print(f"Amenities data saved to {output_file_amenities}")
    else:
        print(f"Error fetching amenities: {response_amenities.status_code}")

if __name__ == "__main__":
    inspect_park("yose")

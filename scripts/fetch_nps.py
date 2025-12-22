import os
import json
import requests
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
API_KEY = os.environ.get("NPS_API_KEY")
OUTPUT_FILE = "data/parks.json"
OVERRIDES_FILE = "data/manual_overrides.json"
NPS_API_URL = "https://developer.nps.gov/api/v1/parks"

def fetch_nps_data():
    if not API_KEY:
        print("Error: NPS_API_KEY environment variable not set.")
        print("Please set the NPS_API_KEY environment variable.")
        sys.exit(1)

    parks = []
    start = 0
    limit = 50
    
    print("Fetching data from NPS API...")
    
    while True:
        # Requesting 'accessibility' field if available, though standard endpoint might not return structured data for it without extra calls.
        # We'll stick to basic info + designation filtering for MVP.
        params = {
            "api_key": API_KEY,
            "limit": limit,
            "start": start
        }
        
        try:
            response = requests.get(NPS_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            current_batch = data.get("data", [])
            if not current_batch:
                break
                
            for item in current_batch:
                # Filter for National Parks only for MVP
                # NPS designations include "National Park", "National Monument", etc.
                if "National Park" not in item.get("designation", ""):
                    continue
                    
                normalized_park = normalize_park_data(item)
                parks.append(normalized_park)
            
            total = int(data.get("total", 0))
            # print(f"Processed {start + len(current_batch)} / {total} records...")
            
            start += limit
            if start >= total:
                break
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            sys.exit(1)

    return parks

def normalize_park_data(item):
    # Extract basic info
    park_id = item.get("parkCode")
    name = item.get("fullName")
    states = item.get("states") # Can be comma separated "CA,NV"
    
    # Geo
    try:
        lat = float(item.get("latitude"))
        lon = float(item.get("longitude"))
    except (ValueError, TypeError):
        lat = 0.0
        lon = 0.0

    # Accessibility - Placeholder logic for MVP.
    # In a real implementation, we would parse the 'accessibility' field or fetch related amenities.
    # For now, we default to False and mark as 'needs_review'.
    
    accessible_restrooms = False
    accessible_parking = False
    accessible_trails = False
    
    # Heuristic: Check if 'accessibility' is mentioned in the description (very basic)
    description = item.get("description", "").lower()
    if "wheelchair" in description or "accessible" in description:
        # This is just a hint, not a confirmation
        pass

    status = "needs_review" 
    
    return {
        "id": park_id,
        "name": name,
        "state": states,
        "lat": lat,
        "lon": lon,
        "accessible_restrooms": accessible_restrooms,
        "accessible_parking": accessible_parking,
        "accessible_trails": accessible_trails,
        "source": "nps",
        "affiliate_links": {
            "gear": None,
            "lodging": None
        },
        "status": status
    }

def save_data(parks):
    # Ensure data directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(parks, f, indent=2)
    
    # Summary
    total = len(parks)
    needs_review = sum(1 for p in parks if p["status"] == "needs_review")
    verified = total - needs_review
    
    print(f"Successfully saved {total} parks to {OUTPUT_FILE}")
    print(f"Summary: {verified} verified, {needs_review} needs_review")
    
    if needs_review > 0:
        print("::warning:: Some parks need manual review. Check data/parks.json")

def apply_overrides(parks):
    if not os.path.exists(OVERRIDES_FILE):
        return parks
    
    try:
        with open(OVERRIDES_FILE, "r") as f:
            overrides = json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode {OVERRIDES_FILE}. Skipping overrides.")
        return parks
        
    overrides_map = {item["id"]: item for item in overrides}
    
    for park in parks:
        if park["id"] in overrides_map:
            # Update park data with override values
            park.update(overrides_map[park["id"]])
            print(f"Applied override for {park['id']}")
            
    return parks

if __name__ == "__main__":
    parks = fetch_nps_data()
    parks = apply_overrides(parks)
    save_data(parks)

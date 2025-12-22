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
AMENITIES_URL = "https://developer.nps.gov/api/v1/amenities/parksplaces"

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

def fetch_accessibility_details(park_code):
    """
    Fetches specific accessibility amenities for a given park.
    Returns a dictionary with categorized accessibility details.
    """
    # print(f"  Fetching accessibility details for {park_code}...")
    params = {
        "api_key": API_KEY,
        "parkCode": park_code,
        "limit": 100 # Should be enough for one park's accessible places
    }
    
    try:
        response = requests.get(AMENITIES_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"  Error fetching amenities for {park_code}: {e}")
        return None

    # Initialize details structure
    details = {
        "trails": [],
        "parking": [],
        "camping": [],
        "lodging": [],
        "restrooms": [],
        "general": []
    }
    
    # The API returns a list of lists: "data": [ [ { "name": "Amenity", ... } ], ... ]
    for amenity_group in data.get("data", []):
        for amenity in amenity_group:
            name = amenity.get("name", "")
            
            # We are primarily interested in "Wheelchair Accessible"
            if name == "Wheelchair Accessible":
                for park in amenity.get("parks", []):
                    if park.get("parkCode") == park_code:
                        for place in park.get("places", []):
                            categorize_place(place, details)
                            
            # Also check specific categories to catch items not tagged "Wheelchair Accessible"
            elif name == "Accessible Rooms":
                 for park in amenity.get("parks", []):
                    if park.get("parkCode") == park_code:
                        for place in park.get("places", []):
                            add_unique_place(details["lodging"], place)

            elif name == "Accessible Sites":
                 for park in amenity.get("parks", []):
                    if park.get("parkCode") == park_code:
                        for place in park.get("places", []):
                            add_unique_place(details["camping"], place)

    return details

def categorize_place(place, details):
    title = place.get("title", "")
    url = place.get("url", "")
    item = {"name": title, "url": url}
    
    # Avoid duplicates
    if any(x["name"] == title for x in details["trails"] + details["parking"] + details["camping"] + details["lodging"] + details["restrooms"] + details["general"]):
        return

    title_lower = title.lower()
    
    if any(x in title_lower for x in ["trail", "trailhead", "loop", "walk", "hike"]):
        details["trails"].append(item)
    elif "parking" in title_lower:
        details["parking"].append(item)
    elif any(x in title_lower for x in ["campground", "camp", "rv"]):
        details["camping"].append(item)
    elif any(x in title_lower for x in ["lodge", "hotel", "cabin", "inn", "ahwahnee"]):
        details["lodging"].append(item)
    elif any(x in title_lower for x in ["restroom", "comfort station", "toilet"]):
        details["restrooms"].append(item)
    else:
        details["general"].append(item)

def add_unique_place(category_list, place):
    title = place.get("title", "")
    url = place.get("url", "")
    if not any(p["name"] == title for p in category_list):
        category_list.append({"name": title, "url": url})

def enrich_parks_data(parks):
    print(f"Enriching data for {len(parks)} parks with accessibility details...")
    for i, park in enumerate(parks):
        park_code = park["id"]
        print(f"[{i+1}/{len(parks)}] Processing {park['name']} ({park_code})...")
        
        details = fetch_accessibility_details(park_code)
        
        if details:
            park["accessibility_details"] = details
            
            # Update boolean flags based on found details
            if details["trails"]:
                park["accessible_trails"] = True
            if details["parking"]:
                park["accessible_parking"] = True
            if details["restrooms"]:
                park["accessible_restrooms"] = True
            
            # Auto-verify if we found meaningful accessibility data
            if details["trails"] or details["parking"] or details["camping"] or details["lodging"] or details["restrooms"]:
                park["status"] = "verified"
                
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
    parks = enrich_parks_data(parks)
    parks = apply_overrides(parks)
    save_data(parks)

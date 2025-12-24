import requests
import json
import os
import time

# Configuration
OVERPASS_URL = "http://overpass-api.de/api/interpreter"
RAW_OUTPUT_FILE = "data/osm_raw.json"
NORMALIZED_OUTPUT_FILE = "data/osm_accessible.json"
FILTER_CONFIG_FILE = "data/osm_filters.json"

# Load Filters
try:
    with open(FILTER_CONFIG_FILE, 'r') as f:
        FILTERS = json.load(f)
except FileNotFoundError:
    print(f"Warning: {FILTER_CONFIG_FILE} not found. Using defaults.")
    FILTERS = {
        "query_features": {"parks_and_nature": True, "campsites_and_viewpoints": True, "paths": True, "toilets": True, "parking": True},
        "exclude_name_keywords": [],
        "exclude_tags": {}
    }

# List of states to query (ISO 3166-2 codes)
# Fetching a subset for demonstration/testing to avoid long timeouts
STATES = {
    "AL": "Alabama", "CA": "California", "NY": "New York", 
    "TX": "Texas", "FL": "Florida", "CO": "Colorado",
    "RI": "Rhode Island"
}

def build_query(state_code):
    """
    Builds an Overpass QL query for a specific area (state) using ISO3166-2 code.
    Refined to focus on outdoor recreation and exclude urban infrastructure.
    """
    # ISO3166-2 code for US states is like "US-CA"
    iso_code = f"US-{state_code}"
    
    features = FILTERS.get("query_features", {})
    
    parts = []
    
    if features.get("parks_and_nature", True):
        parts.append('nwr["leisure"~"park|nature_reserve"]["wheelchair"="yes"](area.searchArea);')
        parts.append('nwr["boundary"="national_park"]["wheelchair"="yes"](area.searchArea);')
        parts.append('nwr["protected_area"]["wheelchair"="yes"](area.searchArea);')
        
    if features.get("campsites_and_viewpoints", True):
        parts.append('nwr["tourism"~"camp_site|picnic_site|viewpoint"]["wheelchair"="yes"](area.searchArea);')
        
    if features.get("paths", True):
        parts.append('nwr["highway"="path"]["wheelchair"="yes"](area.searchArea);')
        
    if features.get("toilets", True):
        parts.append('nwr["amenity"="toilets"]["wheelchair"="yes"]["building"!="yes"](area.searchArea);')
        
    if features.get("parking", True):
        parts.append("""
      nwr["amenity"="parking"]
         ["parking"!~"multi-storey|underground|rooftop|garage"]
         ["access"!~"private|customers|permit"]
         ["park_ride"!="yes"]
         ["wheelchair"="yes"]
         (area.searchArea);
         
      nwr["amenity"="parking"]
         ["parking"!~"multi-storey|underground|rooftop|garage"]
         ["access"!~"private|customers|permit"]
         ["park_ride"!="yes"]
         ["capacity:disabled"]
         (area.searchArea);
        """)

    query_body = "\n".join(parts)

    return f"""
    [out:json][timeout:180];
    area["ISO3166-2"="{iso_code}"]->.searchArea;
    (
      {query_body}
    );
    out center tags;
    """

def fetch_osm_data(state_code, state_name):
    print(f"Fetching data for {state_name} ({state_code})...")
    query = build_query(state_code)
    try:
        response = requests.post(OVERPASS_URL, data={'data': query})
        response.raise_for_status()
        data = response.json()
        elements = data.get('elements', [])
        print(f"  Found {len(elements)} elements for {state_name}")
        return elements
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {state_name}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response text: {e.response.text}")
        return []

def normalize_element(element, state_code):
    tags = element.get('tags', {})
    
    # Check exclude_tags
    exclude_tags = FILTERS.get("exclude_tags", {})
    for key, values in exclude_tags.items():
        if key in tags:
            if tags[key] in values:
                return None

    # Determine ID
    osm_id = f"osm-{element['type'][0]}-{element['id']}"
    
    # Determine Name
    name = tags.get('name', f"OSM: {tags.get('leisure', tags.get('highway', tags.get('amenity', 'Unknown Feature')))}")
    
    # Filter out urban/commercial infrastructure based on name keywords
    name_lower = name.lower()
    blocklist = FILTERS.get("exclude_name_keywords", [])
    
    # Allow "Parking Garage" if it's explicitly for a park (hard to know, but usually "Garage" in name implies structure)
    # Allow "Ranger Station"
    if any(word in name_lower for word in blocklist):
        if "ranger station" not in name_lower and "nature center" not in name_lower and "visitor center" not in name_lower:
            return None

    # Determine Coordinates
    lat = element.get('lat')
    lon = element.get('lon')
    if not lat or not lon:
        # For ways/relations, 'center' might be provided by 'out center'
        center = element.get('center', {})
        lat = center.get('lat')
        lon = center.get('lon')
    
    if not lat or not lon:
        return None # Skip if no coordinates

    # Determine Accessibility Flags
    accessible_restrooms = None
    if tags.get('amenity') == 'toilets':
        accessible_restrooms = tags.get('wheelchair') == 'yes'
        
    accessible_parking = None
    if tags.get('amenity') == 'parking':
        accessible_parking = (tags.get('wheelchair') == 'yes' or 'capacity:disabled' in tags)
        
    accessible_trails = None
    if tags.get('highway') == 'path':
        accessible_trails = tags.get('wheelchair') == 'yes'
    
    return {
        "id": osm_id,
        "name": name,
        "lat": lat,
        "lon": lon,
        "state": state_code,
        "source": "osm",
        "accessible_restrooms": accessible_restrooms,
        "accessible_parking": accessible_parking,
        "accessible_trails": accessible_trails,
        "status": "partial",
        "osm_tags": tags
    }

def deduplicate_trails(data):
    """
    Merges trail segments with the same name in the same state.
    """
    merged = []
    seen_trails = {} # Key: (state, name) -> index in merged

    for item in data:
        # Only merge if it's a trail and has a name
        # We skip merging "OSM: ..." names as they are generic
        if item.get('accessible_trails') and item.get('name') and not item['name'].startswith("OSM:"):
            key = (item['state'], item['name'])
            if key in seen_trails:
                # Already exists, merge info if needed
                existing_index = seen_trails[key]
                existing_item = merged[existing_index]
                
                # Append ID to a list of IDs if we want to track them
                if 'osm_ids' not in existing_item:
                    existing_item['osm_ids'] = [existing_item['id']]
                existing_item['osm_ids'].append(item['id'])
                
                # Keep the first occurrence's coordinates for now
                continue
            else:
                # New trail
                item['osm_ids'] = [item['id']]
                merged.append(item)
                seen_trails[key] = len(merged) - 1
        else:
            # Not a trail or unnamed, keep as is
            merged.append(item)
            
    return merged

def main():
    all_raw_data = []
    normalized_data = []
    
    for code, name in STATES.items():
        elements = fetch_osm_data(code, name)
        all_raw_data.extend(elements)
        
        for element in elements:
            normalized = normalize_element(element, code)
            if normalized:
                normalized_data.append(normalized)
        
        # Be nice to the API
        time.sleep(2)

    # Deduplicate trails
    print(f"Before deduplication: {len(normalized_data)} entries")
    normalized_data = deduplicate_trails(normalized_data)
    print(f"After deduplication: {len(normalized_data)} entries")

    # Save Raw Data
    os.makedirs(os.path.dirname(RAW_OUTPUT_FILE), exist_ok=True)
    with open(RAW_OUTPUT_FILE, 'w') as f:
        json.dump(all_raw_data, f, indent=2)
    print(f"Saved {len(all_raw_data)} raw elements to {RAW_OUTPUT_FILE}")

    # Save Normalized Data
    with open(NORMALIZED_OUTPUT_FILE, 'w') as f:
        json.dump(normalized_data, f, indent=2)
    print(f"Saved {len(normalized_data)} normalized entries to {NORMALIZED_OUTPUT_FILE}")

if __name__ == "__main__":
    main()

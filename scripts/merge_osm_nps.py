import json
import math
import os

NPS_FILE = "data/parks.json"
OSM_FILE = "data/osm_accessible.json"
MERGED_FILE = "data/parks.json" # Overwriting the original file as per instructions
# MERGED_FILE = "data/parks_merged.json" # Use this for testing if needed

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371000 # Radius of earth in meters
    return c * r

def merge_data():
    print("Loading data...")
    try:
        with open(NPS_FILE, 'r') as f:
            nps_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {NPS_FILE} not found.")
        return

    try:
        with open(OSM_FILE, 'r') as f:
            osm_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {OSM_FILE} not found.")
        return

    print(f"Loaded {len(nps_data)} NPS parks and {len(osm_data)} OSM entries.")

    merged_count = 0
    new_count = 0
    new_parks = []
    
    # Create a spatial index or just iterate? 
    # For 500 NPS parks and 4000 OSM entries, O(N*M) is 2,000,000 comparisons. 
    # It's fast enough for Python (a few seconds).
    
    for osm_entry in osm_data:
        osm_lat = osm_entry['lat']
        osm_lon = osm_entry['lon']
        match_found = False
        
        for nps_park in nps_data:
            nps_lat = nps_park.get('lat')
            nps_lon = nps_park.get('lon')
            
            if nps_lat is None or nps_lon is None:
                continue
                
            distance = haversine_distance(osm_lat, osm_lon, nps_lat, nps_lon)
            
            if distance <= 500: # 500 meters
                # Match found! Merge data.
                print(f"Match found: {osm_entry['name']} -> {nps_park['name']} ({distance:.1f}m)")
                
                # Update source
                if "source" not in nps_park:
                    nps_park["source"] = ["nps"] # Assume original was NPS
                elif isinstance(nps_park["source"], str):
                    nps_park["source"] = [nps_park["source"]]
                
                if "osm" not in nps_park["source"]:
                    nps_park["source"].append("osm")
                
                # Update data_status
                nps_park["data_status"] = "enriched"
                
                # Merge accessibility flags (OR logic)
                nps_park["accessible_restrooms"] = nps_park.get("accessible_restrooms", False) or osm_entry.get("accessible_restrooms", False)
                nps_park["accessible_parking"] = nps_park.get("accessible_parking", False) or osm_entry.get("accessible_parking", False)
                nps_park["accessible_trails"] = nps_park.get("accessible_trails", False) or osm_entry.get("accessible_trails", False)
                
                # Merge tags into a new field or existing details?
                # Instructions say: "Merge OSM tags into the NPS object"
                if "osm_tags" not in nps_park:
                    nps_park["osm_tags"] = []
                elif isinstance(nps_park["osm_tags"], dict):
                    nps_park["osm_tags"] = [nps_park["osm_tags"]]
                    
                nps_park["osm_tags"].append(osm_entry.get("osm_tags", {}))
                
                match_found = True
                merged_count += 1
                break # Stop checking other NPS parks for this OSM entry
        
        if not match_found:
            # Append as new object
            
            # FILTER: Do not add generic unnamed OSM features as standalone parks.
            name = osm_entry.get('name', '')
            
            # 1. Filter "OSM: *" names (unnamed in OSM)
            if name.startswith('OSM: '):
                continue
                
            # 2. Filter generic names
            GENERIC_NAMES = {
                "parking", "parking area", "public", "visitor parking", 
                "public parking", "general parking", "accessible parking",
                "rest area", "restroom", "toilets", "bathroom", "picnic area",
                "playground", "shelter", "pavilion"
            }
            if name.lower() in GENERIC_NAMES:
                continue

            # Ensure source is a list for consistency if we are changing schema
            if isinstance(osm_entry.get("source"), str):
                osm_entry["source"] = [osm_entry["source"]]
            
            new_parks.append(osm_entry)
            new_count += 1

    nps_data.extend(new_parks)

    print(f"Merged {merged_count} OSM entries into existing parks.")
    print(f"Added {new_count} new parks from OSM.")
    print(f"Total parks: {len(nps_data)}")

    # Save merged data
    with open(MERGED_FILE, 'w') as f:
        json.dump(nps_data, f, indent=2)
    print(f"Saved merged data to {MERGED_FILE}")

if __name__ == "__main__":
    merge_data()

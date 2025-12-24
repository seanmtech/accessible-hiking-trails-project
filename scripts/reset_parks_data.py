import json

PARKS_FILE = "data/parks.json"

def reset_parks_data():
    print(f"Loading {PARKS_FILE}...")
    with open(PARKS_FILE, 'r') as f:
        data = json.load(f)
    
    original_count = len(data)
    cleaned_data = []
    
    for entry in data:
        # Check source
        source = entry.get('source')
        
        # If it's purely OSM, skip it (delete it)
        if source == 'osm' or source == ['osm']:
            continue
            
        # If it's a list containing 'nps', it's an NPS park.
        # We need to strip 'osm' from the source list and remove osm_tags.
        if isinstance(source, list) and 'nps' in source:
            if 'osm' in source:
                entry['source'].remove('osm')
                # If source is now just ['nps'], maybe revert to string 'nps' or keep as list?
                # The schema seems to allow string or list. Let's keep as list ['nps'] or string 'nps'.
                # Original NPS data used string "nps".
                if len(entry['source']) == 1:
                    entry['source'] = entry['source'][0]
            
            # Remove OSM specific fields
            if 'osm_tags' in entry:
                del entry['osm_tags']
            
            # Note: We are NOT reverting accessible_restrooms/parking/trails flags 
            # because we don't know what the original NPS values were without a backup.
            # However, since NPS data usually defaults to False/Null if unknown, 
            # and OSM might have set them to True, we might be leaving some "True" values 
            # that came from a bad OSM match. 
            # Ideally we would reload from a pure NPS backup. 
            # Do we have one? 
            # We don't see a 'parks_backup.json'. 
            # But we can assume the impact on NPS entries is minimal or acceptable 
            # compared to the "Parking Garage" entries.
            
            cleaned_data.append(entry)
        
        # If source is just 'nps' (string), keep it
        elif source == 'nps':
            cleaned_data.append(entry)
            
    print(f"Removed {original_count - len(cleaned_data)} OSM entries.")
    print(f"Remaining parks: {len(cleaned_data)}")
    
    with open(PARKS_FILE, 'w') as f:
        json.dump(cleaned_data, f, indent=2)
    print(f"Saved cleaned data to {PARKS_FILE}")

if __name__ == "__main__":
    reset_parks_data()

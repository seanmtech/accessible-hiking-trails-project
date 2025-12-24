import json

def inspect_bad_data():
    with open('data/parks.json', 'r') as f:
        parks = json.load(f)
    
    bad_keywords = [
        'garage', 'train station', 'subway', 'metro', 'airport', 
        'mall', 'shopping', 'plaza', 'hospital', 'clinic', 
        'school', 'university', 'college', 'library', 'bank'
    ]
    
    osm_count = 0
    bad_count = 0
    examples = []
    
    for park in parks:
        # Check if it's an OSM entry (either purely OSM or enriched)
        is_osm = False
        if isinstance(park.get('source'), list):
            if 'osm' in park['source']:
                is_osm = True
        elif park.get('source') == 'osm':
            is_osm = True
            
        if is_osm:
            osm_count += 1
            name_lower = park.get('name', '').lower()
            
            # Check for bad keywords
            if any(kw in name_lower for kw in bad_keywords):
                # Exclude some false positives if needed, but let's just see what we have
                if "ranger station" not in name_lower and "visitor center" not in name_lower:
                    bad_count += 1
                    if len(examples) < 10:
                        examples.append(park['name'])

    print(f"Total parks: {len(parks)}")
    print(f"OSM-related parks: {osm_count}")
    print(f"Potentially bad OSM parks: {bad_count}")
    print("Examples:")
    for ex in examples:
        print(f" - {ex}")

if __name__ == "__main__":
    inspect_bad_data()

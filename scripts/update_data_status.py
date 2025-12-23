import json
import os

def update_parks():
    file_path = 'data/parks.json'
    if not os.path.exists(file_path):
        # Try relative to workspace root if running from root
        file_path = 'accessible-hiking-trails-project/data/parks.json'
        
    # Adjust for script location
    if not os.path.exists(file_path):
        file_path = '../data/parks.json'

    with open(file_path, 'r') as f:
        parks = json.load(f)
    
    for park in parks:
        if 'data_status' not in park:
            # Simple logic: if verified, maybe complete?
            if park.get('status') == 'verified':
                park['data_status'] = 'complete'
            else:
                park['data_status'] = 'unknown'
                
    with open(file_path, 'w') as f:
        json.dump(parks, f, indent=2)
        
    print(f"Updated {len(parks)} parks.")

if __name__ == "__main__":
    update_parks()

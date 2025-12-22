import json
import sys
import os
from jsonschema import validate, ValidationError

# Resolve paths relative to this script file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
PARKS_FILE = os.path.join(PROJECT_ROOT, "data", "parks.json")
SCHEMA_FILE = os.path.join(PROJECT_ROOT, "data", "park_schema.json")

def validate_data():
    print("🔍 Starting data validation...")
    
    # 1. Load Schema
    if not os.path.exists(SCHEMA_FILE):
        print(f"❌ Error: Schema file not found at {SCHEMA_FILE}")
        sys.exit(1)
        
    try:
        with open(SCHEMA_FILE, "r") as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in schema file: {e}")
        sys.exit(1)

    # 2. Load Data
    if not os.path.exists(PARKS_FILE):
        print(f"❌ Error: Data file not found at {PARKS_FILE}")
        sys.exit(1)
        
    try:
        with open(PARKS_FILE, "r") as f:
            parks = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in data file: {e}")
        sys.exit(1)

    if not isinstance(parks, list):
        print("❌ Error: Root of parks.json must be an array")
        sys.exit(1)

    print(f"📄 Loaded {len(parks)} parks.")

    # 3. Validate each park against schema
    errors = 0
    ids = set()
    
    for i, park in enumerate(parks):
        # Schema Validation
        try:
            validate(instance=park, schema=schema)
        except ValidationError as e:
            print(f"❌ Schema Error in park index {i} (ID: {park.get('id', 'unknown')}): {e.message}")
            errors += 1
            continue

        # ID Uniqueness Check
        park_id = park["id"]
        if park_id in ids:
            print(f"❌ Duplicate ID found: {park_id}")
            errors += 1
        ids.add(park_id)

        # Logical Checks (Optional)
        # Example: If status is verified, ensure at least one accessibility flag is true?
        # For now, we'll keep it simple.

    # 4. Summary
    if errors > 0:
        print(f"\n🚫 Validation FAILED with {errors} errors.")
        sys.exit(1)
    else:
        print("\n✅ Validation PASSED. All data is valid.")
        sys.exit(0)

if __name__ == "__main__":
    validate_data()

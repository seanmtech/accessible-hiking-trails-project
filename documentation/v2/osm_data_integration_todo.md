# 🌍 OSM_DATA_INTEGRATION_TODO.md  
**Purpose:** Expand dataset to include accessible outdoor POIs from OpenStreetMap (via Overpass API)

---

## 🧠 Summary

We want to ingest and normalize OpenStreetMap (OSM) data to supplement our NPS-based listings with **additional accessible recreation data**.

Target features from OSM:
- Trails with `wheelchair=yes`
- Toilets with `wheelchair=yes`
- Viewpoints, picnic areas, and other park features with accessibility tags
- Parking lots with `wheelchair=yes` or `amenity=parking + capacity:disabled=*`

These features should integrate into our existing `/data/parks.json` structure, either as:
- Independent entries (if not linked to an existing NPS location)
- Or, merged into a matching NPS entry (based on name + geospatial proximity)

---

## ✅ Tasks for Copilot Agent

### 📦 Data Fetching

> "Create a Python script `scripts/fetch_osm_accessibility.py` that:
> - Uses Overpass API to query for nodes/ways/relations with `wheelchair=yes` and one of the following:
>     - `leisure=park`
>     - `highway=path`
>     - `tourism=viewpoint`
>     - `amenity=toilets`
>     - `amenity=parking`
> - Restrict to `country=US`
> - Store raw GeoJSON or JSON output to `data/osm_raw.json`"

---

### 🔄 Data Normalization

> "In `scripts/fetch_osm_accessibility.py`, normalize each OSM feature into the existing `parks.json` schema by creating new entries like:
```json
{
  "id": "osm-12345",
  "name": "OSM: Trail near Lake Tahoe",
  "lat": 39.0968,
  "lon": -120.0324,
  "state": "CA",
  "source": "osm",
  "accessible_restrooms": false,
  "accessible_parking": true,
  "accessible_trails": true,
  "status": "partial",
  "osm_tags": {
    "wheelchair": "yes",
    "highway": "path",
    "surface": "asphalt"
  }
}
```
> - If it's a toilet or parking lot, mark only the corresponding field true
> - For now, each OSM object should be its own entry — merging logic comes next"

---

### 🔍 Merge with NPS Data (Optional V2)

> "Write a Python utility `scripts/merge_osm_nps.py` that:
> - Loads both `parks.json` (NPS) and `osm_accessible.json` (OSM-normalized)
> - For each OSM entry, check if it's within ~500m of an existing NPS park (lat/lon match)
> - If a match:
>     - Merge OSM tags into the NPS object (preserve NPS ID)
>     - Set `source = ["nps", "osm"]`
>     - Add `data_status = "enriched"`
> - If no match:
>     - Append OSM entry as a new object with ID prefix `osm-`"

---

## 📂 Output Files

- `data/osm_raw.json`: Raw API result (backup/archive)
- `data/osm_accessible.json`: Normalized objects (ready to merge)
- `data/parks.json`: Final merged file used by Astro build

---

## ✅ Final Integration Tasks

> - Update build to read `parks.json` (now containing both NPS and OSM-derived objects)
> - On frontend:
>   - Show `source` label (NPS, OSM, Verified)
>   - Gracefully handle partial entries (e.g. trail only, no restrooms)

---

## 🧭 UX Goals Alignment

- Show **more local, nearby results** beyond just NPS-managed parks
- Provide **accessible trailheads, parking lots, and toilets** that are missing from federal datasets
- Help users answer:  
  > “I’m in a wheelchair. What accessible outdoor places are near me?”

---

## 📎 Notes

- Overpass API is open and doesn’t require auth, but you may need to throttle for large queries.
- This will dramatically increase geographic coverage and bring value to underserved rural areas.


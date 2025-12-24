# Role: Senior Python & Astro Developer
# Project: "Nature Immersion" Integrated Directory (NPS + OSM)
# Objective: Merge authoritative NPS data with granular OSM physical attributes into a single data layer.

## 1. Integrated Data Strategy
- **Base Layer:** `data/parks.json` (Currently populated by `fetch_nps.py`).
- **Enrichment Layer:** `fetch_osm.py` (New script to add mobility metrics and new non-NPS locations).
- **Primary Key:** For NPS parks, use `id` (e.g., "yose"). For new OSM-only locations, generate a unique `id` based on the OSM Way ID (e.g., "osm-12345").

---

## DELIVERABLE 1: The "Nature Hunter" & Merger (Python)
**Goal:** Create `scripts/fetch_osm.py` that both enriches existing NPS data and adds new local gems.

### Requirements for Copilot:
1. **Load Existing:** Start by reading the current `data/parks.json`.
2. **Phase A (Enrichment):** For every park already in the JSON, use its coordinates to query OSM for specific trail details (`surface`, `incline`, `width`). Append this to the `accessibility_details` object.
3. **Phase B (Discovery):** Search for NEW locations (State Parks/Land Trusts) not in the current list. 
   - **Quality Floor:** Only add if they have `amenity=parking` + `wheelchair=yes` AND `amenity=toilets` + `wheelchair=yes` nearby.
4. **The "Immersion" Check:** Only keep trails that are > 0.2 miles and tagged with `natural=wood` or `landuse=forest`.
5. **Deduplication:** Ensure no duplicate parks are added if they exist in both NPS and OSM (match by proximity/name).

---

## DELIVERABLE 2: The "Effort Profile" & Normalization (Python)
**Goal:** Ensure all data (NPS and OSM) speaks the same language for the UI.

### Requirements for Copilot:
1. **Unified Schema:** Update `data/park_schema.json` to handle both NPS-style amenities and the new OSM `mobility_metrics`.
2. **Effort Profile Logic:** - Calculate if the return journey is harder than the way out using elevation changes between trail start/end nodes.
   - Tag as: `effort_profile: "uphill_return"` or `effort_profile: "balanced"`.
3. **Trust Metadata:** Every entry must have a `last_verified` date and a `source` tag ("nps", "osm", or "hybrid").

---

## DELIVERABLE 3: The Integrated UI (Astro 5.0)
**Goal:** Update the frontend to render the unified data seamlessly.

### Requirements for Copilot:
1. **Component Update:** Update `src/pages/location/[slug].astro` to handle the merged JSON.
2. **Smart Badging:** - Create a **"Quality Gem" Badge** component for locations that meet the "Parking + Restroom" requirement.
   - Create an **"Effort Warning"** component that appears if the `effort_profile` is an uphill return.
3. **Source Transparency:** Add a small "Data Source" footer to the park pages (e.g., "Physical trail data provided by OpenStreetMap mappers").
4. **Verification Display:** Show the `last_verified` date prominently to reassure families.
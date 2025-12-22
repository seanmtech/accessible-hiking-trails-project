# Design: Accessibility Data Deep Dive

## Objective
Enhance the `parks.json` dataset with detailed accessibility information by querying the NPS `/amenities/parksplaces` endpoint. This will allow us to move beyond simple boolean flags (`accessible_trails: true/false`) and list specific accessible locations within each park (e.g., "Cook's Meadow Loop Trailhead", "Yosemite Valley Lodge").

## Data Source Analysis
The standard `/parks` endpoint does not return detailed accessibility data.
However, the `/amenities/parksplaces` endpoint links specific **Amenities** to **Places** within a park.

### Key Amenities to Query
Based on an inspection of Yosemite (`yose`) data, the following Amenity categories are relevant:

| Amenity Name | Relevance |
| :--- | :--- |
| **"Wheelchair Accessible"** | The primary indicator. Lists trails, viewpoints, buildings, and parking areas that are accessible. |
| **"Accessible Rooms"** | Indicates lodging with accessible rooms. |
| **"Accessible Sites"** | Indicates campgrounds with accessible campsites. |
| **"Parking - Auto"** | Can be cross-referenced with "Wheelchair Accessible" to confirm accessible parking. |
| **"Restroom"** | (If available) Can be cross-referenced with "Wheelchair Accessible". |
| **"Assistive Listening Systems"** | For hearing accessibility. |
| **"Braille"** | For visual accessibility. |

## Proposed Data Schema Changes
We will update `data/park_schema.json` and `data/parks.json` to include a new `accessibility_details` object.

```json
{
  "id": "yose",
  "name": "Yosemite National Park",
  "accessible_trails": true,  // Computed from details
  "accessible_parking": true, // Computed from details
  "accessibility_details": {
    "trails": [
      { "name": "Cook's Meadow Loop Trailhead", "url": "..." },
      { "name": "Lower Yosemite Fall Paved Trail", "url": "..." }
    ],
    "parking": [
      { "name": "Mariposa Grove Welcome Plaza", "url": "..." }
    ],
    "lodging": [
      { "name": "Yosemite Valley Lodge", "url": "..." }
    ],
    "camping": [
      { "name": "Upper Pines Campground", "url": "..." }
    ],
    "general": [
      { "name": "Yosemite Museum", "url": "..." }
    ]
  }
}
```

## Implementation Plan

### 1. Update `fetch_nps.py`
The script needs to be refactored to perform a two-step fetch process:

1.  **Fetch Base Park List**: (Existing logic) Get all parks from `/parks`.
2.  **Fetch Amenities (Per Park)**:
    -   For each park (or in batches), call `/amenities/parksplaces`.
    -   Filter for the "Wheelchair Accessible" amenity ID (or name).
    -   Extract the list of `places`.
3.  **Categorize Places**:
    -   Iterate through the accessible places.
    -   Use keyword matching on the place `title` or `type` (if available) to categorize them:
        -   **Trails**: Contains "Trail", "Trailhead", "Loop", "Walk".
        -   **Parking**: Contains "Parking".
        -   **Camping**: Contains "Campground", "Camp".
        -   **Lodging**: Contains "Lodge", "Hotel", "Cabins".
        -   **Restrooms**: Contains "Restroom", "Comfort Station".
        -   **General**: Everything else (Viewpoints, Visitor Centers, etc.).
4.  **Update Boolean Flags**:
    -   Set `accessible_trails = true` if `accessibility_details.trails` is not empty.
    -   Set `accessible_parking = true` if `accessibility_details.parking` is not empty.

### 2. Rate Limiting Considerations
The NPS API has rate limits. Fetching amenities for 60+ parks might take time.
-   **Strategy**: Implement a delay between requests or fetch amenities only for "verified" or "featured" parks initially.
-   **Caching**: Cache the amenities response to avoid re-fetching unchanged data.

## Next Steps
1.  Modify `scripts/fetch_nps.py` to implement this logic.
2.  Run the script to repopulate `data/parks.json`.
3.  Update the Astro frontend (`LocationCard.astro` and `[slug].astro`) to display these new lists.

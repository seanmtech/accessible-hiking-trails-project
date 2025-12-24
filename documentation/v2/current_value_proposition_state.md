# Current State of Value Propositions & Differentiators

**Date:** December 23, 2025
**Purpose:** Overview of how the Accessible Outdoor Recreation Directory currently implements its core value propositions.

---

## 1. Fine-Grained Accessibility Filters

**Status:** ✅ Implemented

**Implementation Details:**
- **Location:** The filter interface appears on **State Listing Pages** (e.g., `/states/California`) in the sidebar.
- **UI Component:** `FilterPanel.astro` provides a clean interface with checkboxes for:
  - Accessible Restrooms
  - Accessible Parking
  - Accessible Trails
- **Logic:**
  - Users select filters (e.g., "Accessible Restrooms").
  - The page reloads with updated URL parameters (e.g., `?accessible_restrooms=true`), allowing for shareable links.
  - A client-side script on the State Page reads these parameters and hides/shows park cards based on their data attributes (`data-restrooms`, etc.).

## 2. Location-Aware, Accessibility-Filtered List Views

**Status:** ✅ Implemented

**Implementation Details:**
- **Distance Calculation:** `DistanceBadge.astro` is the core component.
  - It uses the Haversine formula to calculate the distance between the user and the park.
  - **Geolocation:** Supports the browser's native Geolocation API.
  - **Fallback:** Includes a ZIP code input that resolves to coordinates using the `zippopotam.us` API if the user denies location permissions.
- **Integration:** The badge is embedded in every `LocationCard`, allowing users to see distance context immediately in list views.

## 3. User Trust Signals

**Status:** ⚠️ Partially Implemented (UI Ready, Backend Pending)

**Implementation Details:**
- **Verification Badges:**
  - Parks with `status: "verified"` in the JSON data now display a distinct "Verified" badge in `LocationCard.astro`.
  - This distinguishes manually reviewed entries from raw API imports.
- **User Feedback (UI):**
  - `LocationCard.astro` includes "Thumbs Up" / "Thumbs Down" buttons.
  - *Current Limitation:* These buttons are currently visual only and do not yet persist data to a backend.
- **Data Overrides:**
  - The system supports a `manual_overrides.json` file to correct or enhance data from the NPS API, serving as the source of truth for "Verified" status.

## 4. Surfaced Non-Google Data

**Status:** ✅ Implemented

**Implementation Details:**
- **Data Pipeline:**
  - `scripts/fetch_nps.py` fetches official data directly from the National Park Service (NPS) API.
  - Data is normalized into a standard schema (`data/park_schema.json`).
- **Transparency:**
  - The `Park` schema includes a `source` field (`nps`, `manual`).
  - The project `README.md` explicitly documents these data sources.

## 5. Negative Results / Hard Nos

**Status:** ✅ Implemented

**Implementation Details:**
- **Clear Warnings:**
  - The Detail Page (`[slug].astro`) now analyzes the park's accessibility features.
  - If key features (restrooms, parking, trails) are missing, a yellow warning banner appears: *"This location may not meet all your accessibility needs."*
- **Visual Indicators:**
  - The "Accessibility at a Glance" section uses distinct iconography for "Accessible" (Checkmark/Green) vs "Not Available" (X/Gray).
  - This prevents ambiguity ("Unknown" vs "No") where data allows.

---

## Summary for Review

The core differentiators are technically present. The site successfully moves beyond generic listings by offering specific accessibility filters and clear "hard no" signals that general map apps often miss.

**Immediate Next Steps for Improvement:**
1.  **Feedback Backend:** Connect the trust signal buttons to a database or analytics service.
2.  **Sort by Distance:** Update the list view to physically reorder DOM elements based on the calculated distance, rather than just displaying the number.

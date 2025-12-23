# 🧠 UX_UPGRADE_TODO.md  
**Purpose:** Improve trust, usability, and user delight based on our site's unique value propositions.

---

## ✅ 1. Improve Filter Context (Clarity)

### Task: Add tooltips or descriptions to each accessibility filter
> "Update `FilterPanel.astro` to show a small info icon next to each filter with hover text explaining what it means (e.g. ‘Accessible Parking = marked spots with extra space for ramp/lift vehicles.’)"

---

## 🚀 2. Make Distance Sortable and Filterable

### Task: Add dropdown to sort park listings by distance
> "Update `[state].astro` to include a sort dropdown with options: `A–Z`, `Closest`, `Most Accessible`. Default to A–Z if no location provided."

### Task: Add radius filter using miles
> "Add a numeric input or range slider in `FilterPanel.astro` to filter parks by max distance from user. Recalculate matches client-side."

---

## 🏷 3. Activate User Trust Signals

### Task: Hook up thumbs up/down buttons to track feedback
> "Update `LocationCard.astro` so clicking thumbs up/down sends a POST request to `/api/feedback` with park ID and vote direction."

### Task: Add backend route for saving feedback
> "Create a new Vercel Edge Function at `/api/feedback.js` that appends JSON feedback to a flat file or dummy data store."

---

## 🕵️‍♀️ 4. Surface High-Quality Parks (Ranking UX)

### Task: Create a new page `/top-accessible-parks`
> "Create a new Astro route that filters parks with all 3 accessibility features (`accessible_restrooms`, `accessible_parking`, `accessible_trails` all true) and lists them sorted by name."

---

## ❓ 5. Clarify Missing vs. Unknown Data

### Task: Update icon rendering logic for “unknown” vs “no”
> "In `LocationCard.astro`, update icon logic so:
> - `true` = green check
> - `false` = red ❌
> - `null` or undefined = ⚠️ icon with ‘No data available’ label."

### Task: Add data status field to JSON schema
> "Update the `park_schema.json` and `parks.json` entries to include a `data_status` field that can be `complete`, `partial`, or `unknown`."

---

## 🧼 Optional: Reviewer Notes

### Task: Add optional reviewer notes field to `manual_overrides.json`
> "Allow a new key `reviewer_notes` per entry in `manual_overrides.json`, and display it on the park detail page if present."

---

## 🧠 Reminder
- All new features should remain mobile-friendly
- Avoid runtime JavaScript unless essential
- Prefer enhancements that degrade gracefully when JS is off


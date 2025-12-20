# 📘 Project Requirements & Implementation Plan  
**Project:** Accessible Outdoor Recreation Directory (MVP)  
**Stack:** Astro + TailwindCSS + Python Data Scripts + Vercel  
**Goal:** Help wheelchair users and other mobility-limited users discover accessible outdoor parks, trails, and campgrounds — starting with U.S. National Parks.

---

## ✅ MVP Scope Summary

### Audience
- Primary: Wheelchair users
- Secondary: Families with strollers, seniors, caregivers

### Location Types (MVP)
- National parks
- State/local parks *(planned for later)*
- Hiking trails *(partial)*
- Campgrounds *(partial)*

### Accessibility Filters (MVP)
- Wheelchair-accessible restrooms
- Accessible parking
- Paved or wheelchair-friendly trails

### Browsing Experience
- State-level filtered lists with icons
- Location detail pages
- Distance-from-user display (via browser geolocation)
- No map view or search bar in MVP

### Data Refresh
- Weekly via GitHub Actions
- Review step for uncertain data via `status: needs_review`

### Monetization Scaffolding
- Ad slots (Google AdSense-ready)
- Affiliate content placeholders (related gear, stays)
- Affiliate URLs supported in schema
- Manual override file for data (JSON format)

### Hosting
- Vercel with automatic redeploys

### Manual Contributions
- JSON override/patch file for corrections or additions
- User submission form (Phase 2: Formspree or Vercel API route)

---

## 📊 Functional Requirements

- ✅ Static Astro site with pre-rendered index/detail pages
- ✅ Accessibility filters (checkboxes or tags)
- ✅ Schema-normalized park data
- ✅ Icons or tags for available features
- ✅ Distance from user (if geolocation allowed)
- ✅ Ad + affiliate content zones (optional display)
- ✅ Weekly data update with diff-based QA queue
- ✅ Mobile-first responsive layout

---

## 🛠️ Non-Functional Requirements

- Low hosting and build overhead
- Minimal runtime JS (static-first)
- Privacy-aware geolocation fallback (ZIP input)
- Accessible UI: keyboard + screen reader compatible
- Markdown-style documentation for onboarding (ADHD-friendly)

---

## 🔄 Data Collection Plan

### Primary Data Sources (MVP)
- [NPS API](https://developer.nps.gov/api/v1/parks): National parks data, accessibility info
- [Recreation.gov API or Sitemap](https://recreation.gov): Location metadata + descriptions
- Optional: Overpass API (OpenStreetMap) for trail layers

### Update Workflow
- `scripts/fetch_nps.py`: Pull latest data weekly
- Normalize into `/data/parks.json`
- Merge `manual_overrides.json` before build
- Mark uncertain fields with `needs_review`
- Optional: Email or GitHub Issue summary of diffs
- Trigger Vercel rebuild on push

---

## 🧱 Data Schema Example (JSON)

```json
{
  "id": "yosemite",
  "name": "Yosemite National Park",
  "state": "CA",
  "lat": 37.8651,
  "lon": -119.5383,
  "accessible_restrooms": true,
  "accessible_parking": true,
  "accessible_trails": true,
  "source": "nps",
  "affiliate_links": {
    "gear": null,
    "lodging": null
  },
  "status": "verified"
}
```

---

## 🧩 MVP Page Types

- `/states/[state].astro` – Filtered list view by state
- `/location/[slug].astro` – Detail page for each park
- `/index.astro` – Home/landing
- Components:
  - `LocationCard.astro`
  - `FilterPanel.astro`
  - `AdSlot.astro`
  - `DistanceBadge.astro`

---

## ⏱️ Task List (GitHub Copilot Prompts)

### Setup & Scaffolding

- "Create a new Astro project with Tailwind CSS configured."
- "Set up a `/data` folder and a `/scripts` folder at the root."
- "Write a Python script called `fetch_nps.py` to download and normalize National Park accessibility data from the NPS API into `parks.json`."
- "Create a file called `manual_overrides.json` that can be merged with the automated data before build time."
- "Define a reusable JSON schema or TypeScript interface for park data with fields like name, state, lat/lon, and accessibility tags."

### UI Build

- "Create an Astro component called `LocationCard.astro` that displays park name, location, and icons for restrooms, parking, and trail access."
- "Create a filter panel component called `FilterPanel.astro` with checkboxes for the three accessibility filters."
- "Implement a state-based index page that loads filtered parks from `parks.json` and applies filters based on query params."
- "Add a component called `DistanceBadge.astro` that shows the distance between the user's current location and each park, falling back to a ZIP input."
- "Create a location detail page template (`/location/[slug].astro`) that shows full details for a park using the shared schema."

### Automation & Infra

- "Set up a GitHub Actions workflow to run `fetch_nps.py` every Sunday at midnight and commit any changes to `parks.json`."
- "Configure the Vercel project to rebuild automatically on push to the `main` branch."
- "Update the data script to flag any uncertain fields or new entries as `status: needs_review` and output a summary to the console or Markdown file."

### SEO & Meta

- "Add SEO meta tags to each park detail page based on its data: name, state, description."
- "Generate JSON-LD structured data for parks that includes name, geo, accessibility features."
- "Create a sitemap XML generator that includes all park detail page slugs."

### Monetization Scaffolding

- "Add a reusable `AdSlot.astro` component with sample Google AdSense code and logic to hide it in development."
- "Update location detail pages to include optional affiliate blocks for gear and lodging, using empty placeholders initially."

### Dev UX

- "Create a `NOTES.md` file with a template I can use to write where I left off each session."
- "Write a `README.md` that includes setup steps, data source info, and instructions for running the data fetch script locally."
- "Add a local Python test script to validate that `parks.json` matches the schema and has no missing required fields."


---

## 🌱 V2 and Beyond

- Add user submission form via Formspree or API route
- Expand to state + local parks
- Add trails and campgrounds from OpenStreetMap
- Add map view with Leaflet or MapLibre
- Add advanced filters (surface type, slope, etc.)
- Accept verified user reviews or photos

---

## 🧠 ADHD-Friendly Tips

- Use `/NOTES.md` to jot “where I left off” at end of session
- Each task is scoped <1hr for easy pickup
- Commit messages: `WIP: [task]`
- Use GitHub Issues as “light backlog”
- Save `project_context_file.md` to reuse with ChatGPT/Copilot


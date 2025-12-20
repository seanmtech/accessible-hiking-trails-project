# MVP Build Plan: Accessible Outdoor Recreation Directory

## Objective
Launch a static site built with Astro that lists accessible outdoor recreation sites in the U.S., with a schema that supports SEO-friendly long-tail pages, powered by public datasets and minimal manual effort.

---

## Step 1: Data Sourcing

### Primary Sources:
- [Recreation.gov API + Sitemaps](https://recreation.gov)
- [National Park Service API](https://developer.nps.gov/api/v1/parks)
- [OpenStreetMap + Overpass API](https://overpass-turbo.eu)
- [U.S. Forest Service datasets](https://data.fs.usda.gov/geodata/)
- [State-level parks databases] (e.g. data.ca.gov)

### Fields of Interest:
- Name, location, GPS
- Accessibility features (parking, trails, bathrooms)
- Type (park, trail, campground, etc.)
- Activities
- Website/contact info

---

## Step 2: Data Pipeline

- Python script to fetch & normalize data into JSON/CSV
- Store in `/data/parks.json`
- Weekly refresh via CRON or GitHub Actions
- Use `slug` field for stable URL generation

---

## Step 3: Astro Site Structure

- `/src/pages/index.astro` — homepage with featured areas
- `/src/pages/state/[state].astro` — index of locations by state
- `/src/pages/location/[slug].astro` — detail page
- SEO meta from structured data: name, region, features

---

## Step 4: Styling & Components

- TailwindCSS setup
- Card component for each site
- Filter UI (by accessibility feature, activity, state)
- Mobile-first layout

---

## Step 5: Deployment

- Netlify or Vercel
- GitHub repo for versioning
- Deploy on push to `main`

---

## Bonus (Optional)

- RSS Feed for new locations
- JSON-LD structured data for SEO
- Sitemaps auto-generated from slugs

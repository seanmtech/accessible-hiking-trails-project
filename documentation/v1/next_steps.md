# 📈 NEXT_STEPS.md  
**Accessible Outdoor Recreation Directory**  
**Phase:** MVP Polish → Early Growth

---

## ✅ Immediate MVP Polish

### 🔧 Project Maintenance
- [x] Create a `README.md` with:
  - [x] Setup instructions
  - [x] Data fetching flow
  - [x] Build + deploy commands
  - [x] Contribution guide for yourself/collaborators

- [x] Add a Python script `scripts/validate_data.py` that:
  - [x] Validates `parks.json` against schema
  - [x] Flags missing fields or invalid booleans
  - [x] Ensures unique `id`s
  - [x] Returns non-zero exit if validation fails

- [x] Add GitHub Action to run `validate_data.py` on every pull request

### 🧠 Data Deep Dive (New)
- [x] Implement "Deep Dive" accessibility fetching in `fetch_nps.py`:
  - [x] Query `/amenities/parksplaces` for "Wheelchair Accessible"
  - [x] Categorize places into Trails, Parking, Camping, Lodging
  - [x] Update `parks.json` schema
- [x] Update Frontend to display detailed accessibility lists

- [ ] Run full NPS import via `fetch_nps.py` using your API key
  - [ ] Save updated dataset to `data/parks.json`
  - [ ] Manually inspect random 3–5 entries
  - [ ] Commit to main

---

## 🚀 Early Growth Tasks

### 📣 User Visibility
- [ ] Deploy live site on Vercel
- [ ] Submit `sitemap.xml` to Google Search Console
- [ ] Post in 2–3 niche communities (Reddit, FB, forums)
- [ ] Add CTA on homepage:  
  > “Know a park with great accessibility? Suggest it!”

### 📊 Analytics & Tracking
- [ ] Add Google Analytics or Plausible for basic usage data
- [ ] Track:
  - [ ] Filter usage
  - [ ] Popular states or locations
  - [ ] Outbound affiliate links

### 💰 Monetization Kickstart
- [ ] Enable `AdSlot.astro` for real ads (swap out placeholder IDs)
- [ ] On detail pages, test:
  - [ ] Affiliate link to REI with park name as query
  - [ ] Lodging search (e.g., Airbnb or Booking.com nearby)

---

## 🧠 Strategic Layer

### 🗳️ User Feedback System
- [ ] Add a simple feedback widget on location pages:
  - [ ] 👍 “This was helpful”
  - [ ] 👎 “This info is missing or wrong”
  - [ ] Store in localStorage (v1) or send to webhook (v2)

### 🧩 User Contributions
- [ ] Add a `Suggest a Park` button that links to Formspree form
- [ ] Ask for:
  - Park name
  - Accessibility features observed
  - Optional description or notes
- [ ] Queue submissions to review manually for now

### 🌎 Prep for Expansion
- [ ] Fork `fetch_nps.py` into `fetch_state_parks.py`
- [ ] Update `parks.json` schema to include:
  - `"type": "national"` (for now)
- [ ] Add logic to show `"type"` label on cards

---

## 🧠 ADHD-Friendly Tips (Reminder)
- Use `NOTES.md` to track where you left off
- Use GitHub Issues for “what’s next”
- Copy this file into your repo so you always know where to resume


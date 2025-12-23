# ✅ check_value_adds.md  
**Purpose:** Ensure our site delivers unique value beyond Google SERPs  
**Audience:** GitHub Copilot Agent (or human dev reviewing MVP)

---

## 🧭 Core Value Propositions Checklist

Below are the 5 value differentiators this site should deliver.  
Check if each one is present in the codebase — and if missing, implement the feature.

---

### 1. Fine-Grained Accessibility Filters

**Check:**
- Does the filter UI let users toggle:
  - [x] Wheelchair-accessible restrooms
  - [x] Accessible parking
  - [x] Paved or wheelchair-accessible trails?

**If Missing:**
> Add a checkbox UI in `FilterPanel.astro`  
> Ensure filters modify the state index view and only show matching parks

---

### 2. Location-Aware, Accessibility-Filtered List Views

**Check:**
- Does the state-level list show only filtered parks?
- Is the user’s distance shown or sortable?

**If Missing:**
> Implement a `DistanceBadge.astro` component  
> Use browser geolocation if allowed  
> Fall back to ZIP input if denied  
> Sort or annotate parks by distance in the index view

---

### 3. User Trust Signals

**Check:**
- Is there a way to show manual verification?
- Is `status: verified` or `needs_review` visible in the UI?
- Any user-submitted feedback visible?

**If Missing:**
> Display a trust badge on each `LocationCard.astro` for `verified` status  
> Add a placeholder for future user thumbs-up / thumbs-down input  
> Add `manual_overrides.json` entries as a data source for verification

---

### 4. Surfaced Non-Google Data

**Check:**
- Is park data sourced from NPS, Recreation.gov, or public registries?
- Are those data sources documented in `README.md`?

**If Missing:**
> Fetch and normalize NPS park data via `fetch_nps.py`  
> Populate `parks.json` and cite source in schema  
> Add a comment in `README.md` listing data sources

---

### 5. Negative Results / Hard Nos

**Check:**
- Do parks with missing features clearly show “not available” or “inaccessible”?
- Are users warned when accessibility is limited?

**If Missing:**
> Update `LocationCard.astro` and `DetailPage.astro` to:
> - Show ❌ icons or grayed-out tags for missing features
> - Add a warning banner: “This location may not meet your needs”

---

## ✅ Final Instruction

> Once the above is verified, print a short summary of:
> - Which features were implemented today
> - Which ones already existed
> - Any TODOs left for later

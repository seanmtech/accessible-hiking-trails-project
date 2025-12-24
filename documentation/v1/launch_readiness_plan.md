# Launch Readiness Plan: From Code to Profit
**Project:** Accessible Outdoor Recreation Directory
**Date:** December 22, 2025
**Goal:** Transition from "Functional Prototype" to "Market-Ready Product"

This document outlines the critical path to launch. It moves beyond code implementation into product quality, legal compliance, monetization activation, and deployment.

---

## Phase 1: The "Delight" & Utility Audit (Critical)
*Before driving traffic, we must ensure the product is actually useful and solves the user's problem better than a generic Google search.*

- [ ] **Data Quality "Sanity Check"**
    - Pick 5 random parks from `parks.json`. Manually verify the accessibility data against the official NPS website.
    - *Question:* Is "Restrooms: Yes" enough? Or do users need to know if there are grab bars?
    - *Action:* If data is too thin, we may need a "V2 Data Enrichment" sprint (using AI to parse specific trail descriptions for keywords like "paved", "boardwalk", "grade").
- [ ] **The "Empty State" Review**
    - What happens if a park has no affiliate links? (Currently shows a placeholder).
    - *Action:* Implement a fallback logic (e.g., generic "Shop REI" banner instead of specific gear) so the UI never looks broken.
- [ ] **Mobile Experience "Thumb Test"**
    - Load the site on a real phone (or simulator).
    - Test the "Sticky Footer" on the Location Detail page. Does it cover content? Is it easy to dismiss?
    - Test the "Filter Panel" in the sidebar. Is it usable on mobile? (Currently hidden or stacked? Needs verification).
- [ ] **Performance Audit (Lighthouse)**
    - Run Google Lighthouse. Target: 90+ on Performance, 100 on Accessibility.
    - Verify `CLS` (Cumulative Layout Shift) is 0, especially with the new Ad placeholders.

## Phase 2: Monetization Activation
*Turning placeholders into revenue streams.*

- [ ] **Google AdSense Setup**
    - [ ] Sign up for AdSense.
    - [ ] Create Ad Units for:
        - Homepage Sidebar (Vertical)
        - State List In-Feed (Horizontal)
        - Location Detail Sidebar (Vertical)
        - Location Detail Content (Horizontal)
    - [ ] Replace dummy `client="ca-pub-XXXX"` in `src/components/AdSlot.astro` with real ID.
    - [ ] Add `ads.txt` to `public/` folder.
- [ ] **Affiliate Network Registration**
    - [ ] **Gear:** Apply to REI or Amazon Associates.
    - [ ] **Lodging:** Apply to Booking.com, Expedia, or VRBO.
    - [ ] **Strategy:** Create a `data/affiliate_map.json` to map keywords (e.g., "rocky trail") to specific product links (e.g., "trekking poles"), or use a generic fallback for MVP.

## Phase 3: Legal & Trust (The "Boring" Stuff)
*Essential for AdSense approval and user trust.*

- [x] **Legal Pages**
    - [x] Create `/privacy` (Privacy Policy) - Required for AdSense.
    - [x] Create `/terms` (Terms of Service).
    - [x] Create `/accessibility` (Accessibility Statement) - Crucial for this specific niche.
- [x] **Cookie Consent**
    - [x] Implement a lightweight cookie banner (e.g., using a library or simple script) to comply with GDPR/CCPA/CPRA.
- [x] **Contact/Correction Mechanism**
    - [x] Ensure the "Suggest a Park" or "Report Issue" link works. User-generated corrections are free data cleaning!

## Phase 4: Technical Deployment
*Getting it live.*

- [ ] **Domain Name**
    - Purchase a domain (e.g., `accessibleoutdoors.com` or similar).
- [ ] **Hosting Setup (Netlify/Vercel recommended)**
    - Connect GitHub repo.
    - Configure Build Settings (`npm run build`, output `dist/`).
    - Set up Environment Variables in the hosting dashboard.
- [ ] **Analytics**
    - Set up Google Analytics 4 (GA4).
    - Set up Google Search Console.
    - Add tracking ID to `src/layouts/Layout.astro`.

## Phase 5: Pre-Launch Content Seeding
*SEO doesn't happen overnight.*

- [ ] **Sitemap & Robots.txt**
    - Verify `sitemap-index.xml` is generating correctly (Astro does this, but check it).
    - Create `public/robots.txt`.
- [ ] **Meta Metadata Review**
    - Check `og:image` (Social Share images). Do we have a default one?
    - Verify `title` and `description` tags on State and Park pages are unique and descriptive.

## Phase 6: The "Soft Launch"
- [ ] **Friends & Family Beta**
    - Send to 10 people. Ask them to "Find a wheelchair accessible trail in [State]". Watch them do it.
- [ ] **Community Outreach**
    - Identify 3 subreddits (r/disability, r/hiking, r/nationalparks) or Facebook groups.
    - Draft a "Seeking Feedback" post, not a "Promotion" post.

---

## Immediate Next Step Recommendation
**Focus on Phase 1: The "Delight" Audit.**
Before worrying about AdSense codes, spend 1 hour acting as a user. If the data isn't helpful, the ads won't matter because users will bounce.

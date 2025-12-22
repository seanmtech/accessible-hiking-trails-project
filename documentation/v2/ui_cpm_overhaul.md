# Task List: UI/UX Overhaul for Accessibility & Monetization
**Project:** Accessible Outdoor Recreation Directory
**Stack:** Astro, TailwindCSS
**Objective:** Optimize for Ad Viewability (CPM) and Affiliate CTR while maintaining WCAG 2.1 Compliance and user trust.

---

## 1. Global Architectural Changes (Astro Layouts)
- [ ] **Sticky Sidebar Layout:** Implement a `2-column` grid for desktop (`main` content 65%, `aside` 35%). The sidebar should contain a "Sticky" ad unit that remains in view as the user reads long accessibility reports.
- [ ] **Content Skeleton Loaders:** Create Astro components for ad placeholders. This prevents Layout Shift (CLS), which is vital for both SEO and user frustration.
- [ ] **Accessible Typography System:** Set base font size to `18px` for readability. Use Tailwind `prose` classes with high-contrast ratios (WCAG AAA).
- [ ] **Breadcrumb Navigation:** Add a schema-rich breadcrumb (Home > State > Park > Trail) to increase internal link depth and time-on-site.

---

## 2. Homepage: The "Discovery Hub"
- [ ] **Hero Search Refinement:** Center a high-intent search bar (e.g., "Find a wheelchair-accessible trail in [State]"). 
- [ ] **High-Visibility "Featured" Slot:** Create a "Featured Accessible Destination" card that mimics an ad placement but provides high-value content. Place a display ad immediately below this.
- [ ] **Trust Signals Section:** Add a "Why Trust Us" section highlighting the Python enrichment pipeline and verified data points. This builds the authority needed for affiliate clicks later.
- [ ] **Category Grid:** Create icons for "National Parks," "Campgrounds," and "Trails." Use Tailwind's `hover:bg-slate-50` for clear interaction states.

---

## 3. State List Page: The "Comparison View"
- [ ] **In-Feed Ad Integration:** Modify the `map()` function in the Astro component to insert a "Native Style" display ad or an Affiliate "Gear Tip" every 5th list item.
- [ ] **Filter Sidebar:** Add "Sticky" filtering options (e.g., "Paved Surface Only") to keep users on the page longer, increasing ad impression duration.
- [ ] **Quick-View Details:** Include "Top Accessibility Feature" snippets in the list view so users don't have to click away immediately, increasing total page viewability.

---

## 4. Location Detail Page: The "Conversion Engine"
- [ ] **"The Accessibility Quick-Box":** At the top of the page, create a high-contrast box with the "Verified" status. Place a 300x250 display ad immediately to the right (Desktop) or below (Mobile).
- [ ] **Contextual Affiliate Modules:**
    - [ ] **Gear Module:** "Recommended for this trail" (e.g., All-terrain wheelchair accessories or specific hiking poles) using REI affiliate links.
    - [ ] **Lodging Module:** "Accessible Stays Near [Park Name]" using a Booking.com or VRBO widget.
- [ ] **The "Sticky" Mobile Footer:** Implement a bottom-docked CTA for mobile that says "View Map" or "Check Gear List," keeping a small affiliate anchor or ad unit visible at all times.
- [ ] **Long-Form Content Layout:** Ensure the Python-enriched data (detailed descriptions) is broken up by "Utility" subheadings. Insert a mid-article display ad after the "Trail Conditions" section.

---

## 5. Performance & Technical Optimization
- [ ] **Image Optimization:** Use `astro:assets` for all park images to ensure <1s load times. High speed = lower bounce rate = more ad impressions.
- [ ] **External Link Handling:** Add `rel="nofollow sponsored"` to all affiliate links automatically.
- [ ] **Ad-Block Detection (Soft):** Add a small, polite message in the sidebar for users with ad-blockers, explaining that ads keep the accessibility data free.
- [ ] **A11y Audit:** Ensure all new ad containers have `aria-label="Advertisement"` and do not break screen-reader flow.

---

## 6. Implementation Notes for Copilot
- Use **Tailwind Grid/Flexbox** for all layouts; avoid absolute positioning where possible.
- Ensure all components are **Responsive** (Mobile-First).
- Use **Astro Components** (`.astro`) for reusable ad/affiliate slots to keep the code DRY.
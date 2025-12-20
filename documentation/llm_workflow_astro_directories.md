# LLM + Copilot Directory-Site Workflow (Astro)

## 1. Code Structure (Reuse Across Projects)

```
/data/             <- Raw data JSON or CSV
/scripts/          <- Python or JS scraping/normalization
/src/
  /pages/          <- Astro route files
  /components/     <- Cards, filters, nav
  /layouts/
astro.config.mjs
tailwind.config.js
```

---

## 2. Copilot Use

- In VS Code with Copilot Chat enabled:
  - "Write an Astro component that lists parks from `parks.json`"
  - "Add a filter for 'wheelchair accessible' using tailwind forms"
  - "Paginate results 20 per page"

---

## 3. ChatGPT Prompts

- "I have this data schema: [paste schema]. Help me generate Astro page templates that iterate over it."
- "How do I structure my Astro site to support [index/detail] for SEO?"

---

## 4. Workflow Tips

- Use Copilot for boilerplate (routing, components)
- Use ChatGPT for data ingestion, edge cases, naming
- Keep scripts short and idempotent
- Version everything in git for clarity

---

## 5. Reusability

- Swap out `/data` and update slugs/schema to create a new directory
- Reuse all UI components
- Adjust filters/index logic as needed

---

## 6. ADHD-Friendly Notes

- Commit often: `git commit -m "WIP: added index filter"`
- Push to GitHub: use issues/project board for loose task queue
- Use `README.md` or `/NOTES.md` for breadcrumbs

---
name: programmatic-seo-pages-smoke
description: >
  Programmatic SEO Pages — Smoke Test. Manually research 10-20 long-tail keywords, create a page
  template, and publish 10 pages to prove organic search traffic can be captured at scale.
stage: "Marketing > ProblemAware"
motion: "FounderSocialContent"
channels: "Content, Website"
level: "Smoke Test"
time: "8 hours over 4 weeks"
outcome: "≥100 organic visits and ≥1 conversion in 4 weeks"
kpis: ["Organic traffic", "Pages indexed", "Conversion rate", "Average position"]
slug: "programmatic-seo-pages"
install: "npx gtm-skills add marketing/problem-aware/programmatic-seo-pages"
drills:
  - keyword-matrix-builder
  - programmatic-page-generator
  - threshold-engine
---

# Programmatic SEO Pages — Smoke Test

> **Stage:** Marketing → ProblemAware | **Motion:** LeadCaptureSurface | **Channels:** Content, Website

## Outcomes

Prove that template-based SEO pages targeting long-tail keywords can attract organic search traffic and generate at least one conversion. This is a manual, small-batch test — no automation, no always-on systems. Just evidence of signal.

## Leading Indicators

- Google Search Console shows pages being crawled within 7 days of publishing
- At least 5 of 10 pages indexed within 14 days
- Organic impressions appearing for target keywords within 21 days
- At least one page ranking in positions 1-30 for its target keyword

## Instructions

### 1. Build a small keyword matrix

Run the `keyword-matrix-builder` drill manually with a narrow scope:

- Pick ONE pattern (e.g., "best {product} for {industry}" or "{competitor} alternative")
- Identify 10-20 modifiers with validated search demand (volume >30/month, KD <40)
- Use Ahrefs keyword research or a free alternative (Ubersuggest, Google Keyword Planner) if Ahrefs is not yet available
- Build a simple spreadsheet: target_keyword, slug, search_volume, keyword_difficulty, modifier

No Clay table needed at this stage. A CSV or Google Sheet is sufficient.

### 2. Create a page template

**Human action required:** Design a single Webflow CMS collection template page. This is a one-time visual design task. The template should include:

- H1 heading (bound to CMS field)
- Body content area (rich text, bound to CMS field)
- A lead capture CTA: demo booking widget (Cal.com embed) or email capture form (Loops)
- Internal links section (bound to CMS field)
- SEO metadata fields (meta title, meta description, OG image)

Keep the design simple and fast-loading. Focus on content readability over visual polish.

### 3. Generate and publish 10 pages

Run the `programmatic-page-generator` drill manually for the first 10 keywords:

- Generate content for each page using Claude. Provide the target keyword, modifier, and ICP context. Each page must be unique — not just the modifier swapped in a template.
- Manually create each CMS item in Webflow via the API or the Webflow editor
- Set meta titles and descriptions for each page
- Add 2-3 internal links between related pages
- Publish all pages

After publishing, verify the pages are included in the sitemap. Submit the sitemap to Google Search Console.

### 4. Wait and observe (3-4 weeks)

Google takes time to crawl, index, and rank new pages. During the waiting period:

- Check GSC daily for indexation progress (URL Inspection tool)
- After 7 days, check if any pages have impressions
- After 14 days, check ranking positions for target keywords
- Monitor PostHog for any organic traffic arriving

Do not make changes to published pages during this period. The goal is a clean read on whether the template and keywords work.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure results after 4 weeks:

- **Pass:** ≥100 organic visits across all pages AND ≥1 conversion (form submit, demo booking, or signup)
- **Marginal pass:** 50-99 organic visits and impressions trending up. Stay at Smoke, add 10 more pages, measure for 2 more weeks.
- **Fail:** <50 organic visits. Diagnose: Are pages indexed? Are keywords too competitive? Is the content thin? Fix the root cause and re-run.

## Time Estimate

- Keyword research and matrix: 2 hours
- Template design (human): 2 hours
- Content generation and publishing: 3 hours
- Monitoring and evaluation: 1 hour
- **Total: 8 hours over 4 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Webflow | CMS hosting and page template | CMS plan $23/mo ([pricing](https://webflow.com/pricing)) |
| Google Search Console | Indexation tracking and search analytics | Free ([pricing](https://developers.google.com/webmaster-tools/pricing)) |
| PostHog | On-site traffic and conversion tracking | Free tier up to 1M events/mo ([pricing](https://posthog.com/pricing)) |
| Anthropic Claude | Content generation per page | API usage ~$0.50-2.00 for 10 pages ([pricing](https://www.anthropic.com/pricing)) |
| Ahrefs (optional) | Keyword research and difficulty scoring | Lite $99/mo ([pricing](https://ahrefs.com/pricing)); free alternatives available |

**Estimated play-specific cost at Smoke:** Free to $23/mo (Webflow CMS plan if not already active). Ahrefs optional — use free keyword tools if needed.

## Drills Referenced

- `keyword-matrix-builder` — research and validate 10-20 long-tail keyword targets
- `programmatic-page-generator` — generate unique content and publish pages via Webflow CMS
- `threshold-engine` — evaluate organic traffic and conversions against pass/fail threshold

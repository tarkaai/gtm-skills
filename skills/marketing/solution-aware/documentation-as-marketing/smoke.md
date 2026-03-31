---
name: documentation-as-marketing-smoke
description: >
  Documentation as Marketing — Smoke Test. Audit your public docs site for SEO
  readiness, publish 5-8 keyword-targeted documentation pages, and validate that
  docs can attract organic search traffic from solution-aware technical buyers.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Smoke Test"
time: "12 hours over 2 weeks"
outcome: ">=100 organic visits to docs pages in 4 weeks"
kpis: ["Organic page views to docs", "Pages indexed in GSC", "Average position for target keywords", "Docs CTA click rate"]
slug: "documentation-as-marketing"
install: "npx gtm-skills add marketing/solution-aware/documentation-as-marketing"
drills:
  - threshold-engine
---

# Documentation as Marketing — Smoke Test

> **Stage:** Marketing > Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Outcomes

The first batch of 5-8 SEO-targeted docs pages collectively receives >= 100 organic page views within 4 weeks of publication. At least 3 pages are indexed by Google. At least 1 page appears in the top 50 results for its target keyword.

## Leading Indicators

- Google indexes all published pages within 14 days (verify via GSC URL Inspection API)
- At least 2 pages receive organic impressions within 21 days (visible in GSC search analytics)
- Docs site SEO audit score improves by >= 15 points after fixes are applied
- At least 1 CTA click occurs on a published docs page (PostHog `docs_cta_clicked` event)

## Instructions

### 1. Audit your docs site for SEO readiness

Run the the docs site seo audit workflow (see instructions below) drill. Provide your public docs URL, GSC access, and 2-3 competitor docs sites. The drill will:

- Crawl your docs site structure and check indexation rates
- Analyze current keyword coverage vs competitors
- Audit on-page SEO quality (titles, meta descriptions, headings, content depth)
- Audit conversion paths (CTAs, signup links, navigation to product)
- Produce a prioritized issue list and keyword gap analysis

Act on the critical issues first:
- If no sitemap exists, generate one and submit to GSC
- If pages have missing meta descriptions, add them
- If pages are blocked from indexing (noindex, robots.txt), fix the blocking rules
- If pages have no CTAs, add relevant conversion links

**Human action required:** Review the SEO audit results. Confirm which keyword gaps align with your product's actual capabilities. Remove any gaps that target features you do not have.

### 2. Produce and publish 5-8 targeted docs pages

Run the the docs content production workflow (see instructions below) drill with the top 5-8 keyword opportunities from the audit. For each keyword:

- Classify the page type (getting started, how-to, integration guide, API reference, troubleshooting)
- Generate the page content via Anthropic API with proper keyword targeting, code examples, and structured format
- Quality-check: keyword in title + first 100 words + an H2, correct code examples, conversion CTA at the end, internal links to 2+ existing docs pages
- Publish via your docs platform (Mintlify, GitBook, ReadMe, Docusaurus, or Fumadocs)
- Update sidebar/navigation to include the new pages

**Human action required:** Review all generated content before publishing. Verify:
- Code examples are syntactically correct and reference your actual API/product
- Technical accuracy: the steps actually work as described
- CTAs are relevant to the page content (not generic "sign up" on every page)

### 3. Submit pages to GSC and set up basic tracking

After publishing:

1. Submit the sitemap (or individual URLs) to GSC. Use the URL Inspection API to request indexing for each new page.
2. Configure PostHog events on the new pages:
   - `docs_page_viewed`: fires on page load with properties `url`, `target_keyword`, `page_type`, `referrer`
   - `docs_cta_clicked`: fires on CTA interaction with properties `url`, `cta_type`, `cta_text`
3. Build a simple PostHog dashboard: total docs page views (filtered to new pages), page views by page, CTA clicks

### 4. Monitor indexation and early signals

Check daily for the first 2 weeks:
- Are pages being indexed? (GSC URL Inspection)
- Are pages receiving impressions? (GSC search analytics)
- Is any organic traffic arriving? (PostHog)

If pages are not indexed after 14 days: check for technical issues (robots.txt blocking, noindex tags, thin content below 300 words, duplicate content with existing pages).

### 5. Evaluate against threshold

Run the `threshold-engine` drill at the 4-week mark. Measure:
- Total organic page views across published docs pages: target >= 100
- Pages indexed: target >= 3
- Pages ranking in top 50: target >= 1

If PASS, proceed to Baseline. If FAIL, diagnose: are pages indexed? If indexed but not ranking, the keywords may be too competitive — target longer-tail variants. If ranking but no clicks, rewrite meta titles and descriptions to improve CTR.

## Time Estimate

- Docs SEO audit: 3 hours (crawl + analysis + prioritization)
- Content production: 5 hours (generation + human review + publishing)
- GSC submission and tracking setup: 1 hour
- Monitoring and evaluation: 3 hours (spread over 4 weeks)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ahrefs | Keyword research, competitor gap analysis | Starter $29/mo or Lite $129/mo — https://ahrefs.com/pricing |
| Mintlify | Docs platform (if used) | Free (Hobby) or $250/mo (Pro) — https://mintlify.com/pricing |
| PostHog | Page view tracking, CTA click events | Free up to 1M events/mo — https://posthog.com/pricing |
| Google Search Console | Indexation monitoring, search analytics | Free — https://search.google.com/search-console |
| Anthropic Claude API | Content generation | ~$0.50-3.00 for initial batch (Sonnet 4: $3/$15 per M tokens) — https://anthropic.com/pricing |

## Drills Referenced

- the docs site seo audit workflow (see instructions below) — audit docs site SEO health, identify keyword gaps and technical issues
- the docs content production workflow (see instructions below) — generate, quality-check, and publish SEO-targeted docs pages
- `threshold-engine` — evaluate 4-week results against pass threshold

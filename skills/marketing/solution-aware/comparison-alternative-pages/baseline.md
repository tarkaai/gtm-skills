---
name: comparison-alternative-pages-baseline
description: >
  Comparison and Alternative Pages — Baseline Run. Scale to 10-20 comparison pages with
  automated tracking, CRM-routed lead capture, and continuous ranking monitoring as the
  first always-on comparison page system.
stage: "Marketing > SolutionAware"
motion: "FounderSocialContent"
channels: "Content, Website"
level: "Baseline Run"
time: "25 hours over 8 weeks"
outcome: "≥1,500 page views and ≥20 conversions from comparison pages over 8 weeks"
kpis: ["Organic traffic to comparison pages", "Conversion rate", "Average position for competitor keywords", "CTA click rate", "Feature table engagement rate"]
slug: "comparison-alternative-pages"
install: "npx gtm-skills add marketing/solution-aware/comparison-alternative-pages"
drills:
  - keyword-matrix-builder
  - comparison-page-creation
  - lead-capture-surface-setup
  - seo-performance-monitor
---

# Comparison and Alternative Pages — Baseline Run

> **Stage:** Marketing → SolutionAware | **Motion:** LeadCaptureSurface | **Channels:** Content, Website

## Outcomes

Scale comparison pages from the Smoke test's 3-5 pages to 10-20 pages covering your most important competitors, with always-on SEO monitoring, CRM-routed lead capture, and continuous ranking tracking. Pass threshold: ≥1,500 page views and ≥20 conversions over 8 weeks.

## Leading Indicators

- 10+ comparison pages indexed in Google within 3 weeks of publishing
- Average ranking position for target keywords improves from initial indexation (typically position 30-50) toward page 1 (positions 1-10) over 8 weeks
- Comparison page conversion rate ≥1.0% (CTA clicks / page views)
- At least 2 comparison pages ranking in the top 10 for their target keywords by week 6
- GSC impressions for competitor keywords growing week over week

## Instructions

### 1. Expand the keyword matrix

Run the `keyword-matrix-builder` drill to expand beyond Smoke test targets:

- Include all competitors identified during Smoke (the ones that converted or showed strong search volume)
- Add "alternative to" pages for competitors with high search volume
- Add category roundup pages: "best {category} for {use case}" covering 3-5 use cases where you are strongest
- Prioritize by the scoring formula: traffic potential, keyword difficulty, commercial intent
- Target: 10-20 total page targets for the Baseline batch

### 2. Build additional comparison pages

Run the `comparison-page-creation` drill for each new page target:

- Use the expanded keyword matrix as input
- Gather competitor data via scraping or manual research for each new competitor
- Generate unique content per page — no duplicated introductions or boilerplate across pages
- Build feature comparison tables customized to each competitor's actual capabilities
- Each page gets a dedicated CTA matched to the competitor context (e.g., for a direct competitor, "Switch from {competitor} in 15 minutes — book a migration call")

### 3. Deploy lead capture surfaces

Run the `lead-capture-surface-setup` drill to wire comparison page CTAs to your CRM:

- Choose one CTA type for consistency across all comparison pages (inline calendar, short form, or chat widget)
- Configure the n8n webhook: when a lead converts on a comparison page, create a contact in Attio with the source tagged as `comparison-page/{competitor-name}`
- Create a deal at the "Lead Captured" stage with the competitor context attached
- Enroll the lead in a Loops nurture sequence tailored to comparison page visitors (emphasize differentiators, include a case study of a customer who switched from that competitor)

### 4. Set up always-on SEO monitoring

Run the `seo-performance-monitor` drill configured specifically for comparison pages:

- Configure PostHog events: `comparison_page_viewed`, `comparison_table_scrolled`, `comparison_cta_clicked` (carried over from Smoke, now across all 10-20 pages)
- Build a PostHog dashboard showing traffic, conversion, and engagement per comparison page
- Set up daily GSC data sync via n8n: pull ranking positions for all target competitor keywords
- Set up weekly Ahrefs sync: track total keyword footprint across comparison pages
- Configure alerts: ranking drops >5 positions, traffic drops >20% WoW, conversion rate drops below 0.8%

### 5. Evaluate against threshold

After 8 weeks, measure:

- Total page views across all comparison pages (target: ≥1,500)
- Total conversions (target: ≥20)
- Conversion rate across all comparison pages
- Number of pages ranking in the top 10 for their target keyword
- Total organic keyword footprint (how many unique keywords do comparison pages rank for)

If PASS: proceed to Scalable. Document which page types (1:1 comparison vs alternatives vs roundup) perform best, which competitors drive the most traffic, and which CTAs convert best.
If FAIL: diagnose per-page performance. Are specific pages underperforming? Refresh content. Are pages indexed but not ranking? Check backlink profile and content depth. Are pages ranking but not converting? Test different CTAs.

## Time Estimate

- 5 hours: keyword matrix expansion and prioritization
- 12 hours: writing and publishing 10-15 additional comparison pages
- 4 hours: lead capture surface setup and CRM routing
- 4 hours: SEO monitoring dashboard, GSC/Ahrefs sync, alert configuration

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ahrefs | Keyword research, rank tracking, SERP analysis | Lite $99/mo — https://ahrefs.com/pricing |
| Google Search Console | Index monitoring, search analytics | Free — https://search.google.com/search-console |
| PostHog | Traffic, engagement, and conversion tracking | Free up to 1M events/mo — https://posthog.com/pricing |
| Anthropic (Claude) | Comparison page content generation | ~$5-15 total for 10-15 pages — https://anthropic.com/pricing |
| Tally | Form builder for lead capture (if using form CTA) | Free — https://tally.so/pricing |

**Baseline budget: Free** (Ahrefs assumed standard stack; Tally free tier; Claude API costs negligible)

## Drills Referenced

- `keyword-matrix-builder` — expand the competitor keyword target list to 10-20 pages with full search volume and difficulty data
- `comparison-page-creation` — write, optimize, and publish each additional comparison page
- `lead-capture-surface-setup` — wire CTAs to CRM with Attio contact creation, deal tagging, and Loops nurture enrollment
- `seo-performance-monitor` — always-on tracking of rankings, indexation, traffic, and conversions with anomaly alerts

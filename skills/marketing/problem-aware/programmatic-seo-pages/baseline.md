---
name: programmatic-seo-pages-baseline
description: >
  Programmatic SEO Pages — Baseline Run. Scale to 50-200 pages with automated content generation,
  structured tracking, and weekly publishing cadence to prove sustained organic growth.
stage: "Marketing > ProblemAware"
motion: "FounderSocialContent"
channels: "Content, Website"
level: "Baseline Run"
time: "20 hours over 8 weeks"
outcome: "≥1,000 organic visits and ≥15 conversions over 8 weeks"
kpis: ["Organic traffic", "Pages indexed", "Conversion rate", "Average position", "Click-through rate"]
slug: "programmatic-seo-pages"
install: "npx gtm-skills add marketing/problem-aware/programmatic-seo-pages"
drills:
  - keyword-matrix-builder
  - programmatic-page-generator
  - posthog-gtm-events
  - seo-performance-monitor
---

# Programmatic SEO Pages — Baseline Run

> **Stage:** Marketing → ProblemAware | **Motion:** LeadCaptureSurface | **Channels:** Content, Website

## Outcomes

Scale from the Smoke test's 10 pages to 50-200 pages with a semi-automated pipeline. Prove that organic traffic grows consistently as pages are added and that conversions are repeatable — not a one-off. This is the first always-on system: pages publish on a weekly schedule without manual intervention for each page.

## Leading Indicators

- Indexation rate >80% within 21 days of publishing each batch
- Organic traffic growing week-over-week for at least 4 consecutive weeks
- At least 10 pages ranking in positions 1-20 for their target keywords
- Conversion rate ≥0.5% across all programmatic pages
- Click-through rate from SERP improving as meta titles and descriptions are refined

## Instructions

### 1. Expand the keyword matrix

Run the `keyword-matrix-builder` drill at full scope:

- Expand to 2-3 keyword patterns (e.g., "best {product} for {industry}", "{competitor} alternative", "how to {action} with {product}")
- Build a modifier list of 50-200 targets per pattern using Ahrefs keyword research
- Validate all combinations for search demand (volume >20/month) and difficulty (<50 KD)
- Store the matrix in a Clay table or Airtable for structured access
- Define content variables per page: h1, meta_title, meta_description, category, modifier, internal_link_targets

### 2. Set up structured event tracking

Run the `posthog-gtm-events` drill to configure tracking specific to programmatic SEO pages:

- `seo_page_viewed`: page load with properties for URL, target keyword, category, modifier, referrer
- `seo_page_engaged`: scroll >50% or time >30 seconds
- `seo_page_converted`: CTA click, form submission, or demo booking
- Build PostHog funnels: `seo_page_viewed` → `seo_page_engaged` → `seo_page_converted`
- Set up UTM capture to distinguish organic from direct/referral traffic

### 3. Publish pages in weekly batches

Run the `programmatic-page-generator` drill with batch automation:

- Generate content for 20-30 pages per week using the Anthropic API
- Run uniqueness and quality checks on each batch before publishing
- Create CMS items via the Webflow API (use the bulk creation loop from the drill)
- Publish the site after each batch
- Submit updated sitemap to Google Search Console
- Target: 50 pages in weeks 1-2, expanding to 200 total by week 8

### 4. Set up SEO performance monitoring

Run the `seo-performance-monitor` drill:

- Configure the daily GSC data pull via n8n (indexation status, clicks, impressions, CTR, position)
- Build the PostHog SEO dashboard: organic traffic trend, pages indexed, top pages, conversion rate by page
- Configure alerts: indexation rate drop, ranking drops >5 positions, traffic decline >20% week-over-week
- Set up the weekly automated report

### 5. Optimize based on data (weeks 4-8)

After 4 weeks of data:

- Identify the top 10% of pages by organic traffic. What do they have in common? (keyword difficulty, content depth, topic pattern)
- Identify pages with high impressions but low CTR. Rewrite their meta titles and descriptions to be more compelling.
- Identify pages not yet indexed. Check for duplicate content, thin content, or crawl issues. Fix and resubmit.
- Double down on the keyword patterns that work. Add more modifiers to winning patterns.

### 6. Evaluate against threshold

Measure after 8 weeks:

- **Pass:** ≥1,000 total organic visits across all programmatic pages AND ≥15 conversions
- **Marginal pass:** 500-999 organic visits with clear upward trend. Continue for 4 more weeks.
- **Fail:** <500 organic visits. Diagnose: Is indexation the bottleneck? Are keywords too competitive? Is content quality too low? Fix and re-run.

## Time Estimate

- Keyword matrix expansion: 4 hours
- Event tracking setup: 2 hours
- Content generation and publishing (weekly batches): 8 hours total over 8 weeks
- Monitoring setup: 3 hours
- Data analysis and optimization: 3 hours
- **Total: 20 hours over 8 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Webflow | CMS hosting for programmatic pages | CMS $23/mo or Business $39/mo for >2,000 pages ([pricing](https://webflow.com/pricing)) |
| Google Search Console | Indexation and search analytics | Free ([pricing](https://developers.google.com/webmaster-tools/pricing)) |
| PostHog | On-site tracking, funnels, dashboards | Free tier up to 1M events/mo ([pricing](https://posthog.com/pricing)) |
| Ahrefs | Keyword research and rank tracking | Lite $99/mo or Standard $199/mo ([pricing](https://ahrefs.com/pricing)) |
| Anthropic Claude | Content generation at scale | ~$5-20 for 200 pages ([pricing](https://www.anthropic.com/pricing)) |
| n8n | Automation for monitoring and publishing | Free self-hosted or Cloud $20/mo ([pricing](https://n8n.io/pricing)) |
| Clay | Keyword matrix and modifier research | Free tier or Explorer $149/mo ([pricing](https://www.clay.com/pricing)) |

**Estimated play-specific cost at Baseline:** $23-99/mo depending on whether Ahrefs is needed (may already be in the stack).

## Drills Referenced

- `keyword-matrix-builder` — expand to 50-200 keyword targets across multiple patterns
- `programmatic-page-generator` — batch content generation and CMS publishing via API
- `posthog-gtm-events` — structured event tracking for SEO page views, engagement, conversions
- `seo-performance-monitor` — daily GSC sync, ranking tracking, and performance dashboards

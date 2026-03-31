---
name: programmatic-seo-pages-scalable
description: >
  Programmatic SEO Pages — Scalable Automation. Fully automated pipeline generating 500-2,000+ pages
  with AI content generation, automated quality checks, and content refresh cycles.
stage: "Marketing > ProblemAware"
motion: "FounderSocialContent"
channels: "Content, Website"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥5,000 organic visits/month and conversion rate ≥1.2%"
kpis: ["Organic traffic", "Pages indexed", "Conversion rate", "Average position", "Click-through rate", "Page generation velocity"]
slug: "programmatic-seo-pages"
install: "npx gtm-skills add marketing/problem-aware/programmatic-seo-pages"
drills:
  - keyword-matrix-builder
  - programmatic-page-generator
  - content-refresh-pipeline
  - seo-performance-monitor
---

# Programmatic SEO Pages — Scalable Automation

> **Stage:** Marketing → ProblemAware | **Motion:** LeadCaptureSurface | **Channels:** Content, Website

## Outcomes

Scale to 500-2,000+ programmatic pages with a fully automated pipeline. No manual content creation — the agent generates, validates, publishes, and monitors pages end-to-end. Add the content refresh cycle so existing pages improve over time while new pages continue to be published. The 10x multiplier is page velocity: going from 20 pages/week (Baseline) to 100+ pages/week without proportional effort.

## Leading Indicators

- Page generation velocity: ≥100 new pages published per week with zero manual intervention
- Indexation rate >85% across all pages within 21 days of publishing
- Organic traffic compounding: each new batch of pages adds incremental traffic
- Top 20% of pages driving >80% of conversions (power law distribution emerging)
- Content refresh cycle recovering declining pages within 30 days

## Instructions

### 1. Expand keyword coverage to exhaustive

Run the `keyword-matrix-builder` drill at maximum scope:

- Expand to 5-10 keyword patterns covering all angles your ICP searches (industry, competitor, use case, action, location)
- Use Clay's Claygent to systematically research every possible modifier for each pattern
- Target 500-2,000 validated keyword combinations
- Score and prioritize the full list. Publish in priority order: highest traffic potential and lowest difficulty first.
- Set up a monthly refresh of the matrix: discover new keywords, re-score difficulty, add new modifiers

### 2. Fully automate the publishing pipeline

Run the `programmatic-page-generator` drill with end-to-end automation via n8n:

Build an n8n workflow that runs daily or weekly:

1. **Pull new keywords** from the keyword matrix (Clay table or Airtable) that have not yet been published
2. **Generate content** via Anthropic API: batch 20-50 pages per run, each with unique content tailored to the keyword, modifier, and ICP
3. **Quality check**: automated validation for uniqueness (cross-page similarity <40%), keyword inclusion, word count (800-1,500 words), internal link integrity
4. **Create CMS items** via Webflow API using the bulk creation loop (respect rate limits)
5. **Publish the site** via Webflow publish API
6. **Submit sitemap** update to Google Search Console
7. **Log results** to PostHog: `seo_page_published` event with URL, keyword, word count, batch ID

Configure the workflow to process 100+ pages per week. At 1 page/second Webflow API rate, a 100-page batch takes ~2 minutes to create.

### 3. Launch the content refresh cycle

Run the `content-refresh-pipeline` drill as an automated weekly process:

- Scan all published pages for: declining rankings, stuck on page 2-3, not indexed after 30 days, low engagement
- Auto-diagnose: compare against top-ranking competitors, check for content staleness, internal linking gaps
- Generate refreshed content via Anthropic API with the specific diagnosis as context
- Update CMS items and publish
- Track refresh impact: position changes, CTR changes, traffic changes over the next 14-28 days
- Feed outcomes back into the refresh algorithm to improve future diagnosis

Target: refresh 10-20 underperforming pages per week alongside publishing new pages.

### 4. Optimize conversion rate across all pages

Using data from `seo-performance-monitor`:

- Identify the CTA and page patterns that convert best (which categories, which modifiers, which CTA text)
- A/B test CTA variations using PostHog feature flags: button copy, form placement, offer type (demo vs. download vs. trial)
- Test meta title patterns: does including a year ("2026") improve CTR? Does a number ("Top 7") outperform a superlative ("Best")?
- Apply winning variations across all pages in the category via bulk CMS update

### 5. Build internal linking at scale

As the page count grows, internal linking becomes a ranking factor:

- Automatically generate a "related pages" section on each page linking to 3-5 related pages from the same keyword pattern
- Create hub/pillar pages for each major category that link to all child pages
- Update hub pages weekly as new child pages are published
- Monitor internal link graph: every page should have at least 3 incoming internal links

### 6. Evaluate against threshold

Measure after 2 months:

- **Pass:** ≥5,000 organic visits/month AND conversion rate ≥1.2% across all programmatic pages
- **Marginal pass:** 3,000-4,999 organic visits/month with clear growth trajectory. Continue for 4 more weeks.
- **Fail:** <3,000 organic visits/month. Diagnose: Is the content unique enough? Are keywords too competitive? Is indexation the bottleneck? Reduce keyword difficulty targets and focus on lower-competition terms.

## Time Estimate

- Keyword matrix expansion to 500-2,000 targets: 10 hours
- Publishing pipeline automation (n8n build): 15 hours
- Content refresh pipeline setup: 10 hours
- Conversion optimization testing: 10 hours
- Internal linking automation: 5 hours
- Monitoring and evaluation: 10 hours
- **Total: 60 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Webflow | CMS hosting for 500-2,000+ pages | Business $39/mo for 10K items ([pricing](https://webflow.com/pricing)) |
| Google Search Console | Indexation and search analytics | Free ([pricing](https://developers.google.com/webmaster-tools/pricing)) |
| PostHog | Tracking, funnels, experiments, dashboards | Free to Growth $0.000248/event ([pricing](https://posthog.com/pricing)) |
| Ahrefs | Keyword research, rank tracking, competitor analysis | Standard $199/mo or Advanced $399/mo ([pricing](https://ahrefs.com/pricing)) |
| Anthropic Claude | Content generation and refresh at scale | ~$20-80/mo for 500-2,000 pages ([pricing](https://www.anthropic.com/pricing)) |
| n8n | End-to-end pipeline automation | Cloud $20/mo or self-hosted free ([pricing](https://n8n.io/pricing)) |
| Clay | Keyword matrix management and modifier research | Explorer $149/mo ([pricing](https://www.clay.com/pricing)) |

**Estimated play-specific cost at Scalable:** $199-399/mo (Ahrefs is the main cost driver; other tools are low-cost or free-tier).

## Drills Referenced

- `keyword-matrix-builder` — exhaustive keyword coverage across 5-10 patterns with 500-2,000 targets
- `programmatic-page-generator` — fully automated content generation and publishing pipeline
- `content-refresh-pipeline` — weekly scan and refresh of underperforming pages
- `seo-performance-monitor` — real-time dashboards, ranking tracking, and anomaly alerts

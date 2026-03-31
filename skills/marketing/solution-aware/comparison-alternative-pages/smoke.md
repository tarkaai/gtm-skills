---
name: comparison-alternative-pages-smoke
description: >
  Comparison and Alternative Pages — Smoke Test. Research competitor keywords, build 3-5
  comparison pages manually, deploy lead capture CTAs, and validate that competitor-keyword
  organic traffic converts to leads.
stage: "Marketing > SolutionAware"
motion: "LeadCaptureSurface"
channels: "Content, Website"
level: "Smoke Test"
time: "8 hours over 4 weeks"
outcome: "≥200 page views and ≥3 conversions from comparison pages in 4 weeks"
kpis: ["Organic traffic to comparison pages", "Conversion rate (CTA clicks / views)", "Average ranking position for target competitor keywords", "CTA click rate"]
slug: "comparison-alternative-pages"
install: "npx gtm-skills add marketing/solution-aware/comparison-alternative-pages"
drills:
  - competitor-keyword-research
  - comparison-page-creation
---

# Comparison and Alternative Pages — Smoke Test

> **Stage:** Marketing → SolutionAware | **Motion:** LeadCaptureSurface | **Channels:** Content, Website

## Outcomes

Prove that comparison pages targeting competitor keywords generate organic traffic and convert solution-aware visitors into leads. Pass threshold: ≥200 page views and ≥3 conversions (CTA clicks leading to demo bookings, signups, or form submissions) within 4 weeks.

## Leading Indicators

- Google Search Console shows impressions for target competitor keywords within 7-14 days of publishing
- At least 1 comparison page gets indexed within 7 days
- Feature comparison table scroll rate >40% (visitors engage with the table, not just bounce)
- Time on page >90 seconds on comparison pages (indicates reading, not skimming)

## Instructions

### 1. Research competitor keywords

Run the `competitor-keyword-research` drill:

- Start with your 5-10 known direct competitors
- Map keyword patterns: "{competitor} alternative", "{competitor} vs {your brand}", "best {category} for {use case}"
- Pull search volume, keyword difficulty, and CPC from Ahrefs
- Prioritize: pick the top 3-5 keywords with the best combination of volume, low difficulty, and high commercial intent (CPC >$2)

The output is a prioritized list of 3-5 comparison page targets for this Smoke test.

### 2. Build comparison pages

Run the `comparison-page-creation` drill for each of your 3-5 target keywords:

- Scrape competitor pricing and feature data (or gather manually from their public website)
- Generate page content with Claude: introduction, feature comparison table, strengths/weaknesses, pricing comparison, FAQ
- Build the HTML feature comparison table with your product vs the competitor
- Add SEO metadata: title tag with target keyword, meta description, FAQ schema markup
- Add one CTA per page: inline calendar embed, free trial button, or demo request form

**Human action required:** Verify all competitor data (pricing, features, claims) for accuracy before publishing. Never publish unverified competitor information.

### 3. Publish and configure tracking

- Publish pages at `/compare/{competitor}-vs-{your-brand}` or `/compare/{competitor}-alternatives`
- Configure PostHog events on each page:
  - `comparison_page_viewed`: on page load (properties: `competitor`, `page_type`, `target_keyword`)
  - `comparison_table_scrolled`: when feature table enters viewport
  - `comparison_cta_clicked`: when CTA is clicked
- Update your sitemap and submit to Google Search Console
- Add internal links: link from your homepage, pricing page, or blog to the new comparison pages

### 4. Evaluate against threshold

After 4 weeks, measure:

- Total page views across all comparison pages (target: ≥200)
- Total conversions — CTA clicks that led to a demo booking, signup, or form submission (target: ≥3)
- Which competitor keywords are generating impressions in GSC
- Which comparison page has the highest engagement (table scroll rate, time on page)

If PASS: proceed to Baseline. Document which competitor pages convert best and why.
If FAIL: diagnose — are pages getting indexed? If not, check technical SEO. Are pages getting traffic but not converting? Revise CTAs. Are pages not getting traffic at all? Target lower-difficulty keywords.

## Time Estimate

- 3 hours: competitor keyword research and prioritization
- 4 hours: writing and publishing 3-5 comparison pages (including competitor data gathering)
- 1 hour: PostHog tracking setup, sitemap submission, internal linking

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ahrefs | Competitor keyword research, search volume, difficulty | Lite $99/mo (API access) — https://ahrefs.com/pricing |
| Google Search Console | Index monitoring, impression/click tracking | Free — https://search.google.com/search-console |
| PostHog | Page view, engagement, and conversion tracking | Free up to 1M events/mo — https://posthog.com/pricing |
| Anthropic (Claude) | Comparison page content generation | Pay-per-use ~$0.50-2/page — https://anthropic.com/pricing |

**Smoke budget: Free** (assumes Ahrefs and PostHog are already in the standard stack or free tiers cover usage)

## Drills Referenced

- `competitor-keyword-research` — identify and prioritize competitor keywords to target with comparison pages
- `comparison-page-creation` — write, optimize, and publish each comparison page with feature tables and CTAs

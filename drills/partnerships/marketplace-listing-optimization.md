---
name: marketplace-listing-optimization
description: Optimize template marketplace listings with keyword research, A/B description testing, and conversion tracking
category: Marketplaces
tools:
  - PostHog
  - Clay
  - n8n
  - Attio
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - clay-claygent
  - n8n-workflow-basics
  - n8n-triggers
  - attio-contacts
  - google-ads-keyword-research
---

# Marketplace Listing Optimization

This drill optimizes existing template marketplace listings for higher visibility and download-to-lead conversion. It covers keyword research, description A/B testing, conversion funnel tracking, and systematic improvement cycles.

## Input

- Active template listings on 1+ marketplaces (output from `marketplace-template-creation` drill)
- PostHog tracking installed on your product website
- At least 1 week of listing data for baseline comparison

## Steps

### 1. Research marketplace-specific keywords

Use Clay with the `clay-claygent` fundamental to identify the highest-traffic search terms on each marketplace:

**Claygent prompt:**
```
For the {marketplace_name} template marketplace, research:
1. What are the top 20 search terms in the {your_category} category by estimated volume?
2. What titles do the top 5 templates in this category use?
3. What tags do the most-downloaded templates in this category use?
Return: keyword, estimated search volume (high/medium/low), current top result, and whether our template "{our_template_name}" appears in results for this keyword.
```

Supplement with `google-ads-keyword-research` fundamental to identify what terms people search on Google that lead them to marketplace pages (e.g., "notion okr template", "figma dashboard template").

### 2. Optimize listing titles and descriptions

For each marketplace listing, update:

**Title:** Include the highest-volume keyword identified in step 1. Keep format: `{Primary Keyword} {Qualifier}` (e.g., "OKR Tracker for Startups" not "Startup OKR Management Template System v2").

**Description:** Structure as:
1. Opening line restating the primary keyword + outcome (for marketplace search ranking)
2. What's included (number of components, views, templates)
3. Who it's for (ICP description in the user's language)
4. How to use it (3 quick-start steps)
5. CTA with UTM-tracked link

**Tags:** Use all keyword variants from step 1. Fill every available tag slot.

### 3. Configure conversion funnel tracking

Using `posthog-custom-events`, track the full marketplace-to-lead funnel:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `marketplace_visit` | UTM-tagged visit from marketplace | `marketplace`, `template_slug`, `utm_campaign` |
| `marketplace_cta_click` | Click on any product CTA on landing page | `marketplace`, `template_slug`, `cta_location` |
| `marketplace_lead_captured` | Form submit, trial start, or demo book from marketplace-sourced session | `marketplace`, `template_slug`, `lead_type` |

Using `posthog-funnels`, create a saved funnel:
```
marketplace_visit -> marketplace_cta_click -> marketplace_lead_captured
```
Break down by `marketplace` property.

### 4. Build an optimization tracking workflow

Using `n8n-workflow-basics` and `n8n-triggers`, create a workflow:

**Trigger:** Bi-weekly cron (every 2 weeks, Monday 8am)

**Steps:**
1. Query PostHog for the last 2 weeks: marketplace_visit count, marketplace_cta_click count, marketplace_lead_captured count -- grouped by marketplace
2. Query marketplace analytics (manually logged or scraped) for downloads per marketplace
3. Calculate: download-to-visit rate, visit-to-click rate, click-to-lead rate per marketplace
4. Compare to previous 2-week period
5. Flag any marketplace where any conversion rate dropped >20%
6. Update Attio campaign records with latest metrics
7. Post summary to Slack

### 5. Run listing optimization cycles

Every 2 weeks, based on the tracking data:

**If downloads are low (marketplace visibility problem):**
- Update title to include a higher-volume keyword
- Add more tags
- Update cover image to be more visually distinctive
- Re-promote via social channels

**If downloads are high but site visits are low (CTA problem):**
- Rewrite the CTA copy inside the template
- Move the CTA to a more prominent position
- Add a second CTA at a different point in the template workflow
- Make the CTA more specific about what the user gets

**If site visits are high but leads are low (landing page problem):**
- Ensure the landing page messaging matches what template users expect
- Simplify the lead capture form
- Add social proof relevant to template users (e.g., "Used by X teams")
- Consider gating additional templates behind email capture

Log every change in Attio with: date, what changed, hypothesis, expected impact.

## Output

- Keyword-optimized listing titles, descriptions, and tags across all marketplaces
- PostHog conversion funnel tracking: download -> visit -> CTA click -> lead
- Bi-weekly automated performance reports
- Systematic optimization cycle producing measurable improvements

## Triggers

- Run once at Baseline level for initial optimization
- Optimization cycle repeats bi-weekly at Baseline and Scalable levels
- Re-run keyword research quarterly to catch shifting search trends

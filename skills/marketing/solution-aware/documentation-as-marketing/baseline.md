---
name: documentation-as-marketing-baseline
description: >
  Documentation as Marketing — Baseline Run. Expand docs content to 20-30 pages
  with always-on SEO monitoring, lead capture infrastructure, and automated
  conversion tracking to establish docs as a consistent pipeline source.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Baseline Run"
time: "30 hours over 8 weeks"
outcome: ">=1,000 organic visits/month to docs and >=20 leads captured from docs in 8 weeks"
kpis: ["Monthly organic docs traffic", "Docs-sourced leads", "Docs-to-signup conversion rate", "Pages indexed", "Average keyword position"]
slug: "documentation-as-marketing"
install: "npx gtm-skills add marketing/solution-aware/documentation-as-marketing"
drills:
  - posthog-gtm-events
  - docs-content-production
  - seo-performance-monitor
  - docs-lead-capture-setup
  - threshold-engine
---

# Documentation as Marketing — Baseline Run

> **Stage:** Marketing > Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Outcomes

Docs content expands to 20-30 published pages. Organic traffic reaches >= 1,000 visits/month. At least 20 leads are captured from docs (signup, email capture, or demo booking) over the 8-week window. Always-on SEO monitoring detects ranking changes and traffic anomalies automatically.

## Leading Indicators

- New docs pages indexed within 10 days of publication (GSC URL Inspection)
- Average keyword position improves by >= 5 positions per page over 8 weeks
- At least 5 pages rank in Google top-30 for their target keywords
- Docs CTA click rate >= 2% across all pages
- Lead capture forms on docs pages receive >= 1 submission per week by week 4
- Returning visitors to docs pages > 8% of total docs traffic

## Instructions

### 1. Configure standardized event tracking

Run the `posthog-gtm-events` drill to set up a comprehensive event taxonomy across all docs pages:

- `docs_page_viewed`: page load with properties `url`, `target_keyword`, `page_type`, `referrer`, `utm_source`
- `docs_page_engaged`: fires on scroll depth > 50% OR time on page > 60 seconds. Properties: `url`, `scroll_depth`, `time_on_page`
- `docs_cta_clicked`: CTA interaction with properties `url`, `cta_type`, `cta_tier`, `cta_text`
- `docs_email_captured`: email form submission with properties `url`, `page_type`
- `docs_signup_started`: signup flow initiated from docs with properties `url`, `page_type`, `target_keyword`

Build PostHog funnels:
- `docs_page_viewed` -> `docs_page_engaged` -> `docs_cta_clicked` -> `account_created`
- `docs_page_viewed` -> `docs_email_captured` -> `email_opened` -> `account_created`

### 2. Expand docs content to 20-30 pages

Run the `docs-content-production` drill to produce the next 15-22 docs pages. Use the keyword gap list from the Smoke-level audit, plus new gaps identified from 4 weeks of GSC impression data.

Prioritize page types that convert best at Solution Aware stage:
- **Integration guides** (highest intent — "how to connect {your product} to {their tool}")
- **Getting started tutorials** (high intent — "getting started with {category}")
- **How-to tutorials** for specific use cases (medium intent — "how to {action} with {approach}")
- **API reference pages** for key endpoints (steady long-tail traffic)

Publish at a sustained cadence: 3-5 pages per week over the first 4 weeks. This gives Google time to crawl and index each batch.

After each batch:
- Update docs navigation to include new pages in logical positions
- Verify all internal links are bidirectional (new pages link to existing pages, existing pages link back)
- Submit new URLs to GSC

**Human action required:** Review each batch of generated pages before publishing. Spot-check code examples by running them against your actual API. Verify that integration guides reference real configuration steps, not hallucinated settings.

### 3. Set up always-on SEO monitoring

Run the `seo-performance-monitor` drill to create:

- A PostHog dashboard tracking: total organic docs traffic (daily), page views per page, engagement rate, CTA clicks, conversion rate per page
- A daily n8n workflow pulling GSC search analytics: clicks, impressions, CTR, position per docs page per query
- A weekly n8n workflow pulling Ahrefs rank tracking: position changes, new/lost keywords per docs page
- Anomaly alerts:
  - Total docs traffic drops > 20% week-over-week -> alert
  - Any page loses > 10 ranking positions -> alert
  - Indexation rate drops below 80% -> alert
  - New page not indexed after 14 days -> alert

### 4. Deploy lead capture across docs pages

Run the `docs-lead-capture-setup` drill to:

- Classify all docs pages into conversion tiers (high/medium/low intent)
- Deploy appropriate CTAs per tier:
  - High-intent pages (getting started, integrations): direct signup/API key CTA
  - Medium-intent pages (tutorials, best practices): email capture for gated resource
  - Low-intent pages (reference, troubleshooting): sidebar newsletter signup
- Build the n8n workflow routing docs leads to Attio:
  - Create contact on capture
  - Tag with source = "docs" and entry page/keyword
  - Score based on page intent and engagement depth
- Configure Loops 3-email nurture sequence for email-captured leads
- Build the docs lead dashboard in PostHog: leads this week, conversion rate by page, top converting pages

### 5. Optimize underperforming pages

At week 4, analyze page performance:

- Pages ranking positions 11-30: rewrite meta titles for better CTR, add 300+ words of depth, strengthen internal linking (add 2-3 inbound internal links)
- Pages with traffic but no CTA clicks: test a different CTA placement (after first section vs end of page) or different CTA copy
- Pages not indexed after 21 days: check for thin content (< 300 words), duplicate first paragraphs, or missing from sitemap. Fix and resubmit.

### 6. Evaluate against threshold

Run the `threshold-engine` drill at week 8. Measure:
- Monthly organic visits to docs pages: target >= 1,000
- Total leads captured from docs (signups + email captures): target >= 20
- Pages in Google top-30: target >= 5

If PASS, proceed to Scalable. If FAIL, diagnose the weakest point: if traffic is low, focus on producing more content targeting lower-competition keywords. If traffic is decent but leads are low, the conversion layer needs work — test different CTAs, better placement, more relevant gated content.

## Time Estimate

- Event tracking and funnel setup: 3 hours
- Content production (15-22 pages): 12 hours (AI generation + human review + publishing)
- SEO monitoring setup: 4 hours (PostHog dashboard + n8n workflows)
- Lead capture deployment: 5 hours (CTAs + n8n workflow + Loops sequence + Attio scoring)
- Optimization and evaluation: 6 hours (spread over 8 weeks)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ahrefs | Rank tracking, keyword research, competitor monitoring | Starter $29/mo or Lite $129/mo — https://ahrefs.com/pricing |
| Mintlify | Docs platform (if used) | Free (Hobby) or $250/mo (Pro) — https://mintlify.com/pricing |
| PostHog | Analytics, funnels, dashboards, cohorts | Free up to 1M events/mo — https://posthog.com/pricing |
| Google Search Console | Search analytics, indexation monitoring | Free — https://search.google.com/search-console |
| Anthropic Claude API | Content generation for 15-22 pages | ~$2-8 for the full batch — https://anthropic.com/pricing |
| n8n | Automation for daily GSC sync, lead routing, alerts | Free (self-hosted) or Pro at EUR 60/mo — https://n8n.io/pricing |
| Attio | CRM for lead tracking and scoring | Free up to 3 users — https://attio.com/pricing |
| Loops | Email nurture sequences for captured leads | Free up to 1,000 contacts — https://loops.so/pricing |

## Drills Referenced

- `posthog-gtm-events` — set up standard event taxonomy and funnels for docs tracking
- `docs-content-production` — generate, quality-check, and publish the next 15-22 docs pages
- `seo-performance-monitor` — always-on tracking of rankings, traffic, indexation with anomaly alerts
- `docs-lead-capture-setup` — deploy CTAs, lead routing, nurture sequences, and lead scoring for docs traffic
- `threshold-engine` — evaluate 8-week results against pass threshold

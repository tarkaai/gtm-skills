---
name: content-cluster-strategy-baseline
description: >
  Content Cluster Strategy — Baseline Run. Expand the cluster to 15-20 articles with
  always-on SEO monitoring, automated gap detection, and systematic content production
  to establish consistent organic traffic growth.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Baseline Run"
time: "40 hours over 8 weeks"
outcome: ">=2,500 page views and >=25 conversions over 8 weeks"
kpis: ["Organic traffic to clusters", "Internal link CTR", "Conversion rate", "Average position", "Cluster navigation depth"]
slug: "content-cluster-strategy"
install: "npx gtm-skills add marketing/solution-aware/content-cluster-strategy"
drills:
  - cluster-content-production
  - seo-performance-monitor
  - cluster-gap-analysis
  - threshold-engine
---

# Content Cluster Strategy — Baseline Run

> **Stage:** Marketing > Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Outcomes

The expanded cluster (pillar + 15-20 cluster articles) drives >= 2,500 organic page views and >= 25 conversions over 8 weeks. Organic traffic shows a week-over-week upward trend. At least 5 cluster articles rank in Google top-20 for their target keywords.

## Leading Indicators

- New cluster articles indexed within 10 days of publication (GSC URL Inspection)
- Average position improves by >= 5 positions per article over the 8-week window
- Internal link CTR from pillar to cluster articles holds above 5%
- Cluster navigation depth >= 1.5 pages per session (visitors explore beyond the landing page)
- Returning visitors to cluster pages > 10% of total cluster traffic

## Instructions

### 1. Expand the cluster with remaining subtopics

Using the cluster map from Smoke level, run the `cluster-content-production` drill to produce the next 10-15 cluster articles. Follow the same production process: generate via Anthropic API, quality-check, resolve internal links, set SEO metadata, publish via Ghost.

Publish at a sustained cadence: 3-4 articles per week over the first 3 weeks. This gives Google time to crawl and index each batch.

After publishing each batch:
- Update the pillar page to include new summary sections and links for each new cluster article
- Verify all internal links are bidirectional (pillar links to article, article links back to pillar)
- Submit new URLs to GSC

### 2. Set up always-on SEO monitoring

Run the `seo-performance-monitor` drill to create:

- A PostHog dashboard tracking: total organic cluster traffic (daily), page views per article, conversion rate per article, engagement rate (scroll depth > 50% or time on page > 30s), internal link click-through rate
- A daily n8n workflow pulling GSC search analytics: clicks, impressions, CTR, position per cluster page per query
- A weekly n8n workflow pulling Ahrefs rank tracking: position changes, new/lost keywords per cluster article
- Anomaly alerts: if total cluster traffic drops > 20% week-over-week, if any article loses > 10 positions, if indexation rate drops below 80%

### 3. Run first gap analysis

At week 4, run the `cluster-gap-analysis` drill to:

- Identify subtopics your cluster does not yet cover (keywords your competitors rank for that you do not)
- Detect keyword cannibalization (multiple cluster articles competing for the same query)
- Audit internal linking completeness (are any articles orphaned or under-linked?)
- Check content freshness (any articles with outdated references)
- Compute cluster health score (target >= 70)

Act on the recommendations:
- Add 3-5 new subtopic articles to fill keyword gaps
- Fix internal links where completeness is below 80%
- Resolve cannibalization by merging thin articles or differentiating their angles

### 4. Optimize underperforming articles

For cluster articles ranking positions 11-30 (page 2-3 of Google), apply targeted improvements:

- Rewrite meta titles to improve CTR (include a benefit or number, keep under 60 characters)
- Add more depth: expand the weakest section, add concrete examples or data
- Strengthen internal links: add 2-3 more inbound internal links from other cluster articles to boost authority
- Add FAQ schema markup (JSON-LD) for articles where People Also Ask boxes appear in the SERP

### 5. Track cluster navigation depth

Configure PostHog to measure how deeply visitors navigate the cluster:

- Track `cluster_internal_link_clicked` event when a visitor clicks an internal link within the cluster
- Build a funnel: `cluster_page_viewed` -> `cluster_internal_link_clicked` -> `cluster_page_viewed` (second page)
- Segment by entry page: which cluster articles drive the most exploration?
- Target: >= 1.5 average pages per session within the cluster

### 6. Evaluate against threshold

Run the `threshold-engine` drill at week 8. Measure:
- Total organic page views across all cluster pages: target >= 2,500
- Total conversions: target >= 25
- Articles in top-20: target >= 5

If PASS, proceed to Scalable. If FAIL, focus on the gap analysis recommendations and give the cluster 4 more weeks to mature before re-evaluating.

## Time Estimate

- Content production (10-15 articles): 18 hours (AI generation + human review + publishing)
- SEO monitoring setup: 4 hours (PostHog dashboard + n8n workflows)
- Gap analysis: 4 hours (audit + remediation)
- Optimization of underperformers: 6 hours (meta rewrites, depth additions, link fixes)
- Ongoing monitoring and evaluation: 8 hours (spread over 8 weeks)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ahrefs | Rank tracking, gap analysis, keyword research | $199/mo (Standard) — https://ahrefs.com/pricing |
| Ghost | CMS for publishing expanded cluster | Free (self-hosted) or $9-25/mo — https://ghost.org/pricing |
| PostHog | Traffic analytics, funnel tracking, dashboards | Free up to 1M events/mo — https://posthog.com/pricing |
| Google Search Console | Search analytics, indexation monitoring | Free — https://search.google.com/search-console |
| Anthropic Claude API | Content generation for 10-15 articles | ~$2-5 for the full batch — https://anthropic.com/pricing |
| n8n | Automation for daily GSC sync and weekly reporting | Free (self-hosted) or $20/mo (cloud) — https://n8n.io/pricing |

## Drills Referenced

- `cluster-content-production` — batch-produce remaining cluster articles and publish via CMS
- `seo-performance-monitor` — always-on tracking of rankings, traffic, and indexation with anomaly alerts
- `cluster-gap-analysis` — audit keyword coverage, internal links, and content freshness
- `threshold-engine` — evaluate 8-week results against pass threshold

---
name: content-cluster-strategy-scalable
description: >
  Content Cluster Strategy — Scalable Automation. Launch multiple clusters, automate
  content production pipelines, and use cross-channel distribution to reach 12,000+
  monthly organic page views with conversion rate >= 1.0%.
stage: "Marketing > Solution Aware"
motion: "FounderSocialContent"
channels: "Content, Website"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=12,000 page views/month and conversion rate >=1.0%"
kpis: ["Organic traffic to clusters", "Internal link CTR", "Conversion rate", "Average position", "Cluster coverage", "Keyword ranking distribution"]
slug: "content-cluster-strategy"
install: "npx gtm-skills add marketing/solution-aware/content-cluster-strategy"
drills:
  - topic-cluster-mapping
  - cluster-content-production
  - cluster-gap-analysis
  - content-refresh-pipeline
  - content-repurposing
  - founder-linkedin-content-batch
---

# Content Cluster Strategy — Scalable Automation

> **Stage:** Marketing > Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Outcomes

The site runs 3-5 content clusters, collectively driving >= 12,000 organic page views per month with a conversion rate >= 1.0%. Content production is largely automated: the agent generates, quality-checks, and publishes cluster articles on a weekly schedule. Cross-channel distribution amplifies each cluster article through LinkedIn and newsletter.

## Leading Indicators

- 3+ clusters active, each with 15+ published articles
- 60%+ of cluster articles indexed and ranking in top-50
- 15+ cluster articles in Google top-10
- Content production cadence: 4-6 new articles per week sustained over 2 months
- Social distribution producing >= 50 referral visits per week from LinkedIn posts repurposing cluster content
- Week-over-week organic traffic growth rate >= 5%

## Instructions

### 1. Launch 2-3 new pillar clusters

Run the `topic-cluster-mapping` drill for 2-3 new pillar topics. Select topics that:

- Are adjacent to your first pillar (shared audience, related search intent)
- Have distinct keyword universes (minimal overlap with existing cluster)
- Target different intent types or buyer journey stages within solution-aware

For each new pillar, the drill produces a full cluster map: pillar keyword, 15-30 subtopics, internal linking architecture, and prioritized production order.

### 2. Automate the content production pipeline

Build an n8n workflow that runs weekly:

1. **Pull the content queue**: read the next 4-6 subtopics from the cluster map (stored in Clay table, Airtable, or Google Sheets)
2. **Generate articles**: call the Anthropic API for each subtopic using the prompts defined in `cluster-content-production`
3. **Quality-check**: verify keyword inclusion, length, uniqueness, internal link placeholders
4. **Resolve internal links**: replace placeholders with actual HTML links using the published URL index
5. **Publish via Ghost API**: create as draft, then publish on schedule (2-3 per day)
6. **Submit to GSC**: request indexing for each new URL
7. **Log to PostHog**: fire `cluster_article_published` event per article
8. **Notify Slack**: weekly summary of articles published, with URLs and target keywords

**Human action required:** Review the generated content queue weekly (30-45 min). Spot-check 2-3 articles per batch for quality and voice. Approve the batch or flag specific articles for regeneration.

### 3. Build cross-cluster internal linking

As multiple clusters grow, connect them:

- Each pillar page links to other pillar pages in a "Related Topics" section
- Cluster articles that share audience intent (e.g., "{tool} vs {competitor}" articles across different pillars) cross-link to each other
- Build a site-level topic hub page that links to all pillar pages

After every batch publish, run a link integrity check: verify no 404s, verify all bidirectional links are in place.

### 4. Automate content refresh

Run the `content-refresh-pipeline` drill to create a weekly automated cycle:

- Scan all cluster articles via GSC and Ahrefs for ranking declines, stale content, and low engagement
- Auto-diagnose the issue (competitor surpassed, content outdated, thin coverage)
- Generate refreshed content via Anthropic API
- Publish updates and track refresh impact over 14 days

Target: refresh 2-3 underperforming articles per week. Measure refresh success rate (what % of refreshes result in ranking improvement within 28 days).

### 5. Distribute cluster content across channels

Run the `content-repurposing` drill for each high-performing cluster article (top 20% by organic traffic):

- Extract 3-5 atomic insights from the article
- Transform into LinkedIn posts using the `founder-linkedin-content-batch` drill
- Include a link back to the full cluster article in the CTA
- Schedule 2-3 LinkedIn posts per week derived from cluster content

This creates a distribution flywheel: cluster articles rank in search -> top articles become LinkedIn posts -> LinkedIn posts drive referral traffic -> referral traffic signals engagement to Google -> rankings improve.

### 6. Run monthly gap analysis across all clusters

Run the `cluster-gap-analysis` drill monthly for each active cluster:

- Identify new keyword gaps (competitors covering subtopics you do not)
- Detect cross-cluster cannibalization (two clusters competing for the same keyword)
- Audit internal linking completeness across the full site
- Update cluster health scores

Feed gap analysis output back into the content production queue. New subtopics discovered in gap analysis are automatically added to the cluster map and queued for the next production batch.

### 7. Evaluate against threshold

At month 2, measure:
- Monthly organic page views across all clusters: target >= 12,000
- Conversion rate (conversions / page views): target >= 1.0%

If PASS, proceed to Durable. If FAIL, identify the bottleneck: insufficient content volume (publish more), poor rankings (refresh + link build), low conversion (optimize CTAs), or indexation issues (fix technical SEO).

## Time Estimate

- New cluster mapping (2-3 pillars): 8 hours
- Content production automation setup: 10 hours (n8n workflow + testing)
- Weekly content production oversight: 12 hours (30-45 min/week x 8 weeks)
- Content refresh automation: 6 hours (pipeline setup + monitoring)
- Cross-channel distribution: 10 hours (repurposing + LinkedIn scheduling)
- Monthly gap analysis (2x): 8 hours
- Evaluation and optimization: 16 hours (spread across 2 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ahrefs | Keyword research, rank tracking, gap analysis | $199-399/mo (Standard/Advanced) — https://ahrefs.com/pricing |
| Ghost | CMS for all cluster content | Free (self-hosted) or $25/mo — https://ghost.org/pricing |
| PostHog | Full analytics, dashboards, funnels | Free up to 1M events/mo — https://posthog.com/pricing |
| Google Search Console | Search analytics, indexation | Free |
| Anthropic Claude API | Content generation at scale (~20 articles/mo) | ~$5-15/mo — https://anthropic.com/pricing |
| n8n | Content production automation, refresh pipeline, GSC sync | Free (self-hosted) or $20/mo — https://n8n.io/pricing |
| Clay | Cluster map storage, keyword matrix | $149/mo (Explorer) — https://clay.com/pricing |
| Taplio or Buffer | LinkedIn scheduling for distribution | $39-65/mo — https://taplio.com/pricing or https://buffer.com/pricing |

## Drills Referenced

- `topic-cluster-mapping` — map 2-3 new pillar topics to cluster subtopics
- `cluster-content-production` — automated weekly article generation and publishing
- `cluster-gap-analysis` — monthly audit of keyword coverage, links, and freshness
- `content-refresh-pipeline` — auto-detect and refresh underperforming articles
- `content-repurposing` — transform top cluster articles into multi-channel assets
- `founder-linkedin-content-batch` — distribute cluster insights as LinkedIn posts

---
name: content-cluster-strategy-smoke
description: >
  Content Cluster Strategy — Smoke Test. Map one pillar topic to cluster subtopics,
  publish the pillar page and 5 cluster articles with internal links, and validate
  that the cluster drives organic traffic and conversions.
stage: "Marketing > Solution Aware"
motion: "FounderSocialContent"
channels: "Content, Website"
level: "Smoke Test"
time: "12 hours over 4 weeks"
outcome: ">=400 page views and >=3 conversions in 4 weeks"
kpis: ["Organic traffic to cluster", "Internal link CTR", "Conversion rate", "Average position"]
slug: "content-cluster-strategy"
install: "npx gtm-skills add marketing/solution-aware/content-cluster-strategy"
drills:
  - topic-cluster-mapping
  - cluster-content-production
  - threshold-engine
---

# Content Cluster Strategy — Smoke Test

> **Stage:** Marketing > Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Outcomes

The cluster — one pillar page plus 5 cluster articles — collectively receives >= 400 organic page views and produces >= 3 conversions (email signup, demo booking, or asset download) within 4 weeks of publication.

## Leading Indicators

- Google indexes every published page within 14 days (check via GSC URL Inspection API)
- At least 3 cluster articles appear in Google top-100 for their target keyword within 21 days
- Internal link CTR from pillar to cluster articles > 5% (measured in PostHog)
- Pillar page average time on page > 2 minutes (indicates depth engagement)

## Instructions

### 1. Map your first pillar topic

Run the `topic-cluster-mapping` drill. Provide your product category, ICP description, and 1-3 candidate pillar topics. The drill will:

- Validate which pillar topic has sufficient search volume and subtopic breadth
- Generate 10-30 cluster subtopics with keyword data (volume, difficulty, intent type)
- Score and prioritize subtopics
- Map the internal linking architecture (who links to whom)
- Produce the pillar page outline

Select the top 5 subtopics by priority score for your first batch. These should be a mix: 2-3 informational, 1-2 comparative.

### 2. Produce and publish the cluster

Run the `cluster-content-production` drill with the pillar topic and 5 selected subtopics. The drill will:

- Generate the pillar page (3,000-5,000 words) covering the full topic with summary sections linking to each cluster article
- Generate 5 cluster articles (1,200-2,500 words each) targeting individual subtopic keywords
- Quality-check each article for keyword inclusion, uniqueness, and internal link completeness
- Resolve internal link placeholders so every article links back to the pillar and to 2-3 adjacent cluster articles
- Set SEO metadata (meta title, meta description, slug, tags) per article
- Publish via Ghost CMS: pillar page first, then cluster articles (2-3 per day)

**Human action required:** Review all generated content before publishing. Verify that:
- The pillar page reads as a comprehensive, authoritative guide (not a thin overview)
- Each cluster article provides specific value beyond what the pillar page covers
- Internal links use natural anchor text (not "click here")
- CTAs are contextually relevant (e.g., a comparison article offers a demo, an informational article offers a checklist)

### 3. Set up basic tracking

Configure PostHog events on all cluster pages:
- `cluster_page_viewed`: fires on page load with properties `url`, `pillar_topic`, `target_keyword`, `page_type` (pillar or cluster)
- `cluster_cta_clicked`: fires on CTA interaction with properties `url`, `cta_type` (signup, demo, download)

Build a simple PostHog dashboard: total cluster page views, top pages by views, CTA click count, conversion rate.

### 4. Submit to Google Search Console

Submit the sitemap (or individual URLs) to GSC. Use the URL Inspection API to request indexing for each published page. Monitor indexation status daily for the first 2 weeks.

### 5. Evaluate against threshold

Run the `threshold-engine` drill at the 4-week mark. Measure:
- Total organic page views across all cluster pages: target >= 400
- Total conversions (CTA clicks that result in signup/demo/download): target >= 3

If PASS, proceed to Baseline. If FAIL, diagnose: are pages indexed? Are they ranking? Is the traffic landing but not converting? Fix the weakest point and re-run.

## Time Estimate

- Topic cluster mapping: 3 hours (research + prioritization)
- Content production: 5 hours (AI generation + human review + publishing)
- Tracking setup: 1 hour (PostHog events + GSC submission)
- Monitoring and evaluation: 3 hours (spread over 4 weeks)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ahrefs | Keyword research, subtopic discovery | $99-199/mo (Lite/Standard) — https://ahrefs.com/pricing |
| Ghost | CMS for publishing cluster content | Free (self-hosted) or $9-25/mo (hosted) — https://ghost.org/pricing |
| PostHog | Page view tracking, conversion events | Free up to 1M events/mo — https://posthog.com/pricing |
| Google Search Console | Indexation monitoring, ranking data | Free — https://search.google.com/search-console |
| Anthropic Claude API | Content generation | ~$0.50-2.00 for initial cluster batch — https://anthropic.com/pricing |

## Drills Referenced

- `topic-cluster-mapping` — research pillar topic, generate and prioritize cluster subtopics, map internal linking
- `cluster-content-production` — generate pillar page and cluster articles, publish via CMS
- `threshold-engine` — evaluate 4-week results against pass threshold

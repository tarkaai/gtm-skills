---
name: content-cluster-strategy-baseline
description: >
  Content Cluster Strategy — Baseline Run. Build topical authority with interconnected pillar pages and cluster content to dominate search rankings, from manual topic mapping through automated content production to AI-driven cluster optimization.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Baseline Run"
time: "40 hours over 8 weeks"
outcome: "≥2,500 page views and ≥25 conversions over 8 weeks"
kpis: ["Organic traffic to clusters", "Internal link CTR", "Conversion rate", "Average position", "Cluster navigation depth"]
slug: "content-cluster-strategy"
install: "npx gtm-skills add marketing/solution-aware/content-cluster-strategy"
drills:
  - onboarding-flow
  - posthog-gtm-events
  - crm-pipeline-setup
  - threshold-engine
---
# Content Cluster Strategy — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Build topical authority with interconnected pillar pages and cluster content to dominate search rankings, from manual topic mapping through automated content production to AI-driven cluster optimization.

**Time commitment:** 40 hours over 8 weeks
**Pass threshold:** ≥2,500 page views and ≥25 conversions over 8 weeks

---

## Budget

**Play-specific tools & costs**
- **Tally (free form builder):** Free

_Total play-specific: Free_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Ghost** (Content)
- **Ahrefs** (Analytics)
- **Google Search Console** (Analytics)

---

## Instructions

1. Expand to 3 content clusters (3 broad topics); for each cluster, plan 1 pillar page + 8-10 cluster pages.

2. Research keywords for each cluster using Ahrefs: identify high-volume pillar keywords and long-tail cluster keywords with manageable difficulty.

3. Create content briefs for all 30+ pages: pillar pages (2,500+ words) and cluster pages (1,000-1,500 words); include target keywords, search intent, and internal linking strategy.

4. Write pillar pages first, ensuring comprehensive coverage; then write cluster pages that link back to pillars and cross-link to related clusters.

5. Implement breadcrumb navigation and clear hierarchy in your CMS (Ghost or Webflow); ensure users can easily navigate between pillar and cluster content.

6. Set up PostHog events for cluster_entry (first page viewed), cluster_navigation (internal link clicked), and conversion; create funnels to track journey through clusters.

7. Set pass threshold: ≥2,500 combined page views across all clusters and ≥25 conversions over 8 weeks, with ≥40% of visitors clicking internal links.

8. Monitor Google Search Console for keyword rankings: track pillar keywords (target: top 20) and cluster keywords (target: top 30) weekly.

9. After 8 weeks, analyze which clusters drive most traffic and conversions; evaluate internal linking effectiveness via PostHog click-through rates.

10. If you hit the threshold, document cluster structure, keyword mapping, and internal linking patterns and proceed to Scalable; if not, refine content depth or cluster topics.

---

## KPIs to track
- Organic traffic to clusters
- Internal link CTR
- Conversion rate
- Average position
- Cluster navigation depth

---

## Pass threshold
**≥2,500 page views and ≥25 conversions over 8 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/content-cluster-strategy`_

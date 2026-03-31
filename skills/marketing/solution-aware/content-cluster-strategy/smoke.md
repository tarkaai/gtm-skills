---
name: content-cluster-strategy-smoke
description: >
  Content Cluster Strategy — Smoke Test. Build topical authority with interconnected pillar pages and cluster content to dominate search rankings, from manual topic mapping through automated content production to AI-driven cluster optimization.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Smoke Test"
time: "12 hours over 4 weeks"
outcome: "≥400 page views and ≥3 conversions in 4 weeks"
kpis: ["Organic traffic to cluster", "Internal link CTR", "Conversion rate", "Average position"]
slug: "content-cluster-strategy"
install: "npx gtm-skills add marketing/solution-aware/content-cluster-strategy"
drills:
  - onboarding-flow
  - threshold-engine
---
# Content Cluster Strategy — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Build topical authority with interconnected pillar pages and cluster content to dominate search rankings, from manual topic mapping through automated content production to AI-driven cluster optimization.

**Time commitment:** 12 hours over 4 weeks
**Pass threshold:** ≥400 page views and ≥3 conversions in 4 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Analytics)
- **Ghost** (Content)
- **Google Search Console** (Analytics)

---

## Instructions

1. Choose one broad topic your ICP cares about (e.g., "customer onboarding", "data pipelines"); research 10-15 related subtopics using AnswerThePublic or Ahrefs.

2. Create a simple content map in a spreadsheet: 1 pillar page (comprehensive 2,000+ word guide) connected to 5-8 cluster pages (focused 800-1,200 word articles on subtopics).

3. Write the pillar page first: cover the topic comprehensively with sections for each subtopic; include table of contents, examples, and CTAs.

4. Write 3 cluster pages that dive deep into specific subtopics; in each cluster page, link back to the pillar page and to 1-2 related cluster pages.

5. In the pillar page, add contextual links to each cluster page; ensure all pages are internally linked in a logical hierarchy.

6. Set up PostHog to track page views, time on page, scroll depth, and conversions for the pillar and cluster pages.

7. Set pass threshold: ≥400 combined page views and ≥3 conversions from the 4 pages within 4 weeks.

8. Submit all pages to Google Search Console; monitor indexing and keyword rankings for pillar and cluster keywords.

9. After 4 weeks, analyze PostHog and Search Console: measure total organic traffic, internal link click-through rate, and conversion rate.

10. If you hit the threshold, document your cluster topic, structure, and linking strategy and proceed to Baseline; if not, refine topics or improve content depth.

---

## KPIs to track
- Organic traffic to cluster
- Internal link CTR
- Conversion rate
- Average position

---

## Pass threshold
**≥400 page views and ≥3 conversions in 4 weeks**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/content-cluster-strategy`_

---
name: programmatic-seo-pages-baseline
description: >
  Programmatic SEO Pages — Baseline Run. Generate hundreds of long-tail keyword-optimized landing pages to capture organic search traffic, from manual template creation through automated page generation to AI-driven continuous content optimization.
stage: "Marketing > Problem Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Baseline Run"
time: "20 hours over 8 weeks"
outcome: "≥1,000 organic visits and ≥15 conversions over 8 weeks"
kpis: ["Organic traffic", "Pages indexed", "Conversion rate", "Average position", "Click-through rate"]
slug: "programmatic-seo-pages"
install: "npx gtm-skills add marketing/problem-aware/programmatic-seo-pages"
drills:
  - onboarding-flow
  - posthog-gtm-events
  - crm-pipeline-setup
  - threshold-engine
---
# Programmatic SEO Pages — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Generate hundreds of long-tail keyword-optimized landing pages to capture organic search traffic, from manual template creation through automated page generation to AI-driven continuous content optimization.

**Time commitment:** 20 hours over 8 weeks
**Pass threshold:** ≥1,000 organic visits and ≥15 conversions over 8 weeks

---

## Budget

**Play-specific tools & costs**
- **Tally (free form builder):** Free

_Total play-specific: Free_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Analytics)
- **Webflow** (Content)
- **Ahrefs** (Analytics)
- **Google Search Console** (Analytics)

---

## Instructions

1. Expand keyword research to 200-300 long-tail keywords across 3-5 page templates; use Ahrefs or SEMrush (trial) to validate search volume and difficulty.

2. Create 3-5 page templates with dynamic fields for content generation; include sections for comparison tables, use cases, FAQs, and CTAs.

3. Generate 100 pages using the templates; use a simple script or tool like Webflow CMS or Contentful to automate page creation from a CSV of keywords and content.

4. For each page, write unique meta descriptions, titles, and H1s; ensure body content is 400-600 words with genuine value, not just keyword stuffing.

5. Implement internal linking strategy: each programmatic page links to 3-5 related pages plus pillar content; create XML sitemap and submit to Google Search Console.

6. Set up PostHog events for page_view, cta_click, signup, and demo_request on all programmatic pages; create cohorts to segment traffic by page type.

7. Set pass threshold: ≥1,000 organic visits to the 100 pages over 8 weeks, with ≥15 conversions and ≥50 pages indexed.

8. Monitor indexing in Google Search Console weekly; address any crawl errors or Core Web Vitals issues that arise.

9. After 8 weeks, analyze performance in PostHog and Google Search Console: compute conversion rate by page template, identify top 10 pages by traffic.

10. If you hit the threshold, document templates, keyword lists, and internal linking strategy and proceed to Scalable; if not, refine content quality or keyword targeting and re-run Baseline.

---

## KPIs to track
- Organic traffic
- Pages indexed
- Conversion rate
- Average position
- Click-through rate

---

## Pass threshold
**≥1,000 organic visits and ≥15 conversions over 8 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/programmatic-seo-pages`_

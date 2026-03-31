---
name: programmatic-seo-pages-smoke
description: >
  Programmatic SEO Pages — Smoke Test. Generate hundreds of long-tail keyword-optimized landing pages to capture organic search traffic, from manual template creation through automated page generation to AI-driven continuous content optimization.
stage: "Marketing > Problem Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Smoke Test"
time: "8 hours over 4 weeks"
outcome: "≥100 organic visits and ≥1 conversion in 4 weeks"
kpis: ["Organic traffic", "Pages indexed", "Conversion rate", "Average position"]
slug: "programmatic-seo-pages"
install: "npx gtm-skills add marketing/problem-aware/programmatic-seo-pages"
drills:
  - onboarding-flow
  - threshold-engine
---
# Programmatic SEO Pages — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Generate hundreds of long-tail keyword-optimized landing pages to capture organic search traffic, from manual template creation through automated page generation to AI-driven continuous content optimization.

**Time commitment:** 8 hours over 4 weeks
**Pass threshold:** ≥100 organic visits and ≥1 conversion in 4 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Analytics)
- **Google Search Console** (Analytics)

---

## Instructions

1. Research 20-30 long-tail keywords in your category using free tools like Google Keyword Planner or AnswerThePublic; prioritize keywords with 100-500 monthly searches and low competition.

2. Create a simple HTML or Markdown template for one page type (e.g., "[Tool] vs [Competitor]" or "Best [Tool] for [Use Case]") with placeholders for dynamic content.

3. Manually create 10 pages using the template, filling in unique content for title, H1, description, and body (200-300 words each); ensure each page provides genuine value and answers the search intent.

4. Add structured data markup (Schema.org) to each page for better search visibility; include breadcrumbs and internal links to other pages.

5. Set up PostHog to track page views, time on page, and conversions (signup, demo request) for each programmatic page; create a dashboard to monitor performance.

6. Set pass threshold: ≥100 organic visits to the 10 pages within 4 weeks, with ≥1 conversion (signup or demo).

7. Submit the 10 pages to Google Search Console for indexing; monitor indexing status and Core Web Vitals.

8. After 4 weeks, check PostHog and Google Search Console: count total organic visits, conversions, average position for target keywords.

9. Identify the top 3 performing pages by traffic and conversions; analyze what made them successful (keyword difficulty, content quality, search intent match).

10. If you hit the threshold, document the template and keyword research process and proceed to Baseline; if not, refine keyword selection or content quality and retest with a new batch.

---

## KPIs to track
- Organic traffic
- Pages indexed
- Conversion rate
- Average position

---

## Pass threshold
**≥100 organic visits and ≥1 conversion in 4 weeks**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/programmatic-seo-pages`_

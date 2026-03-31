---
name: comparison-alternative-pages-smoke
description: >
  Comparison and Alternative Pages — Smoke Test. Create comparison and alternative pages targeting competitor keywords to capture high-intent search traffic, from manual competitor research to automated page generation and AI-driven competitive intelligence.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Smoke Test"
time: "8 hours over 4 weeks"
outcome: "≥200 page views and ≥3 conversions in 4 weeks"
kpis: ["Organic traffic", "Conversion rate", "Average position for competitor keywords", "CTA click rate"]
slug: "comparison-alternative-pages"
install: "npx gtm-skills add marketing/solution-aware/comparison-alternative-pages"
drills:
  - onboarding-flow
  - threshold-engine
---
# Comparison and Alternative Pages — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Create comparison and alternative pages targeting competitor keywords to capture high-intent search traffic, from manual competitor research to automated page generation and AI-driven competitive intelligence.

**Time commitment:** 8 hours over 4 weeks
**Pass threshold:** ≥200 page views and ≥3 conversions in 4 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Analytics)
- **Ahrefs** (Analytics)
- **Google Search Console** (Analytics)

---

## Instructions

1. Identify your top 5 direct competitors; research their brand + "alternatives" and "vs [your product]" keywords using Ahrefs or Google Keyword Planner.

2. Create 5 comparison pages: 3 "[Competitor] vs [Your Product]" pages and 2 "Best [Competitor] Alternatives" pages.

3. For each page, research competitor's features, pricing, strengths, and weaknesses using their website, G2 reviews, and user feedback on Reddit or forums.

4. Write honest, balanced comparisons (800-1,200 words): feature-by-feature tables, use case recommendations, pros/cons for each solution; include your differentiation without being overly promotional.

5. Optimize pages for SEO: target keyword in title, H1, meta description, and throughout body; add structured data (comparison schema) for rich snippets.

6. Include clear CTAs ("Try [Your Product]", "Compare Features") with links to signup or demo; add trust signals (customer logos, testimonials, G2 badges).

7. Set up PostHog to track page views, time on page, CTA clicks, and conversions for each comparison page.

8. Set pass threshold: ≥200 total page views and ≥3 conversions from the 5 pages within 4 weeks.

9. Submit pages to Google Search Console; monitor indexing and rankings for target competitor keywords.

10. After 4 weeks, analyze PostHog and Search Console: if you hit the threshold, document your comparison page template and research process and proceed to Baseline; if not, refine content depth or target different competitors.

---

## KPIs to track
- Organic traffic
- Conversion rate
- Average position for competitor keywords
- CTA click rate

---

## Pass threshold
**≥200 page views and ≥3 conversions in 4 weeks**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/comparison-alternative-pages`_

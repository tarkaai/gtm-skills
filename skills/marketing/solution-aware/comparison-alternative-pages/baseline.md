---
name: comparison-alternative-pages-baseline
description: >
  Comparison and Alternative Pages — Baseline Run. Create comparison and alternative pages targeting competitor keywords to capture high-intent search traffic, from manual competitor research to automated page generation and AI-driven competitive intelligence.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Baseline Run"
time: "25 hours over 8 weeks"
outcome: "≥1,500 page views and ≥20 conversions over 8 weeks"
kpis: ["Organic traffic", "Conversion rate", "Average position for competitor keywords", "CTA click rate", "Feature table engagement"]
slug: "comparison-alternative-pages"
install: "npx gtm-skills add marketing/solution-aware/comparison-alternative-pages"
---
# Comparison and Alternative Pages — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Create comparison and alternative pages targeting competitor keywords to capture high-intent search traffic, from manual competitor research to automated page generation and AI-driven competitive intelligence.

**Time commitment:** 25 hours over 8 weeks
**Pass threshold:** ≥1,500 page views and ≥20 conversions over 8 weeks

---

## Budget

**Play-specific tools & costs**
- **Tally (free form builder):** Free

_Total play-specific: Free_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Ahrefs** (Analytics)
- **Anthropic** (AI/LLM)
- **Google Search Console** (Analytics)

---

## Instructions

1. Expand to 15-20 comparison pages covering your top 10 competitors plus category alternatives (e.g., "Salesforce alternatives", "Open source CRM vs [Your Product]").

2. Research competitor keywords using Ahrefs: identify high-volume "X vs Y" and "X alternatives" searches; prioritize keywords with difficulty <40 and commercial intent.

3. Create detailed comparison page template: intro, feature comparison table, pricing comparison, use case recommendations, customer testimonials, FAQs, and CTA sections.

4. For each page, gather comprehensive competitive intelligence: feature lists, pricing tiers, integration capabilities, customer reviews (G2, Capterra, TrustRadius), and positioning.

5. Write or use AI to generate first drafts of all 15-20 pages; human editor ensures accuracy, balance, and differentiation without being overly biased.

6. Implement cross-linking strategy: link between related comparison pages (e.g., "X vs Y" links to "Best X alternatives"); link to relevant blog posts and product pages.

7. Set up PostHog events for comparison_page_view, feature_table_interaction, cta_click, and conversion; create funnels to track visitor behavior.

8. Set pass threshold: ≥1,500 total page views and ≥20 conversions over 8 weeks, with conversion rate ≥1.3%.

9. Monitor Google Search Console for keyword rankings; track impressions, clicks, and CTR for competitor keywords weekly.

10. After 8 weeks, analyze which comparison pages drive most traffic and conversions; if you hit the threshold, document templates and research process and proceed to Scalable; if not, improve content accuracy or target higher-volume competitors.

---

## KPIs to track
- Organic traffic
- Conversion rate
- Average position for competitor keywords
- CTA click rate
- Feature table engagement

---

## Pass threshold
**≥1,500 page views and ≥20 conversions over 8 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/comparison-alternative-pages`_

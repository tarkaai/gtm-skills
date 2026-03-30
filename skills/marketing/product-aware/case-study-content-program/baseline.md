---
name: case-study-content-program-baseline
description: >
  Case Study Content Program — Baseline Run. Create in-depth customer success stories with metrics and storytelling to build credibility and drive conversions, from manual interviews to systematic production and AI-driven story optimization.
stage: "Marketing > Product Aware"
motion: "Lead Capture Surface"
channels: "Content, Website"
level: "Baseline Run"
time: "35 hours over 8 weeks"
outcome: "≥2,000 page views and ≥30 conversions over 8 weeks"
kpis: ["Page views", "Time on page", "Conversion rate", "Sales usage rate", "Customer participation rate"]
slug: "case-study-content-program"
install: "npx gtm-skills add marketing/product-aware/case-study-content-program"
---
# Case Study Content Program — Baseline Run

> **Stage:** Marketing → Product Aware | **Motion:** Lead Capture Surface | **Channels:** Content, Website

## Overview
Create in-depth customer success stories with metrics and storytelling to build credibility and drive conversions, from manual interviews to systematic production and AI-driven story optimization.

**Time commitment:** 35 hours over 8 weeks
**Pass threshold:** ≥2,000 page views and ≥30 conversions over 8 weeks

---

## Budget

**Play-specific tools & costs**
- **Tally (free form builder):** Free

_Total play-specific: Free_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Anthropic** (AI/LLM)
- **Attio** (CRM)
- **Riverside** (Video)

---

## Instructions

1. Expand to 10-12 case studies covering different ICPs, industries, use cases, and company sizes; prioritize customers with the strongest quantitative results.

2. Develop case study template library: written case studies, video testimonials, one-page PDFs, social media snippets; create consistent visual design and branding.

3. Establish systematic customer recruitment process: monitor NPS scores, product usage, and customer health in PostHog; proactively reach out to promoters for case study participation.

4. Conduct interviews and write case studies; use AI (Claude/GPT-4) to generate first drafts from transcripts; human editor polishes for storytelling, accuracy, and impact.

5. Create gated and ungated versions: ungated HTML pages for SEO and discovery; gated PDF downloads that capture email for sales follow-up.

6. Implement case study hub on website with filters by industry, use case, company size, results achieved; optimize for internal search and discoverability.

7. Set up PostHog events for case_study_view, filter_applied, pdf_download, cta_click, demo_request; create cohorts for visitors who engage with case studies.

8. Set pass threshold: ≥2,000 total page views and ≥30 conversions over 8 weeks, with average time on page ≥3 minutes.

9. Integrate case studies into sales collateral: arm sales team with relevant case studies in Attio; track which case studies drive highest engagement in sales conversations.

10. After 8 weeks, analyze which case studies drive most traffic and conversions; calculate ROI of case study program vs. cost of production; if you hit the threshold, document production workflow and proceed to Scalable; if not, improve storytelling or customer selection.

---

## KPIs to track
- Page views
- Time on page
- Conversion rate
- Sales usage rate
- Customer participation rate

---

## Pass threshold
**≥2,000 page views and ≥30 conversions over 8 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/case-study-content-program`_

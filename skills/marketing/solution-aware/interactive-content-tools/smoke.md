---
name: interactive-content-tools-smoke
description: >
  Interactive Content Tools — Smoke Test. Create calculators, assessments, and ROI tools that capture leads and provide immediate value, from manual spreadsheet-based tools to embedded widgets and AI-driven personalized recommendations.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Smoke Test"
time: "6 hours over 3 weeks"
outcome: "≥50 tool uses and ≥15 email captures in 3 weeks"
kpis: ["Tool completion rate", "Email capture rate", "Conversion to demo/signup", "Tool shares"]
slug: "interactive-content-tools"
install: "npx gtm-skills add marketing/solution-aware/interactive-content-tools"
---
# Interactive Content Tools — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Overview
Create calculators, assessments, and ROI tools that capture leads and provide immediate value, from manual spreadsheet-based tools to embedded widgets and AI-driven personalized recommendations.

**Time commitment:** 6 hours over 3 weeks
**Pass threshold:** ≥50 tool uses and ≥15 email captures in 3 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (Analytics)
- **Airtable** (Content)

---

## Instructions

1. Identify one high-value calculation or assessment your ICP needs (e.g., ROI calculator, maturity assessment, cost comparison tool); validate demand by searching Reddit or communities for related questions.

2. Build a simple interactive tool using Google Sheets or Airtable with input fields for user data and formulas that calculate results automatically.

3. Create an embeddable version or simple landing page with the tool; require email to access results or download a PDF report.

4. Write supporting content around the tool: explanation of methodology, example scenarios, interpretation of results; optimize for SEO with target keywords.

5. Set up PostHog to track tool usage: tool_opened, fields_filled, results_viewed, email_submitted, pdf_downloaded.

6. Set pass threshold: ≥50 tool uses and ≥15 email captures within 3 weeks.

7. Publish the tool on your website; share on LinkedIn, Twitter, and relevant communities with a compelling hook ("Calculate your X in 60 seconds").

8. Monitor PostHog for user behavior: identify drop-off points (which fields cause users to abandon), completion rate, and conversion rate.

9. After 3 weeks, analyze results: count total uses, email captures, and any downstream conversions (demos booked, signups).

10. If you hit the threshold, document the tool concept and lead capture mechanism and proceed to Baseline; if not, simplify the tool or choose a more compelling use case.

---

## KPIs to track
- Tool completion rate
- Email capture rate
- Conversion to demo/signup
- Tool shares

---

## Pass threshold
**≥50 tool uses and ≥15 email captures in 3 weeks**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/interactive-content-tools`_

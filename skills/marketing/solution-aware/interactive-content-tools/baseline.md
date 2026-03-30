---
name: interactive-content-tools-baseline
description: >
  Interactive Content Tools — Baseline Run. Create calculators, assessments, and ROI tools that capture leads and provide immediate value, from manual spreadsheet-based tools to embedded widgets and AI-driven personalized recommendations.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Baseline Run"
time: "22 hours over 6 weeks"
outcome: "≥300 completions and ≥100 qualified leads over 6 weeks"
kpis: ["Tool completion rate", "Email capture rate", "SQL conversion rate", "Cost per lead", "Tool engagement time"]
slug: "interactive-content-tools"
install: "npx gtm-skills add marketing/solution-aware/interactive-content-tools"
---
# Interactive Content Tools — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Overview
Create calculators, assessments, and ROI tools that capture leads and provide immediate value, from manual spreadsheet-based tools to embedded widgets and AI-driven personalized recommendations.

**Time commitment:** 22 hours over 6 weeks
**Pass threshold:** ≥300 completions and ≥100 qualified leads over 6 weeks

---

## Budget

**Play-specific tools & costs**
- **Tally (free form builder):** Free

_Total play-specific: Free_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Typeform** (Content)
- **n8n** (Automation)

---

## Instructions

1. Expand to 3-5 interactive tools covering different stages of the customer journey (awareness, consideration, decision); prioritize tools that demonstrate your product's value prop.

2. Build tools using no-code platforms (Typeform, Tally, OutGrow) or custom embed with JavaScript; ensure tools are mobile-responsive and fast-loading.

3. Implement progressive disclosure: collect email early (after 1-2 questions) to reduce abandonment; deliver full results via email with a follow-up sequence.

4. For each tool, create dedicated landing pages with SEO optimization: explain the tool's value, show example results, include customer testimonials.

5. Set up PostHog events for each step in the tool flow: tool_start, question_answered, email_submitted, results_viewed, cta_clicked; create funnels to identify drop-off points.

6. Set pass threshold: ≥300 total tool completions and ≥100 qualified leads over 6 weeks, with email capture rate ≥60%.

7. Implement lead nurture automation: when someone completes a tool, trigger email sequence in n8n or email tool with relevant content and demo offer based on their results.

8. Promote tools via paid ads (LinkedIn, Google), organic content (blog posts embedding tools), and partnerships (co-branded tools with complementary products).

9. After 6 weeks, analyze tool performance in PostHog: calculate cost per lead, lead quality (SQL rate), and downstream revenue from tool-generated leads.

10. If you hit the threshold and lead quality is high, document tool templates and promotion strategy and proceed to Scalable; if not, improve tool UX or refine targeting.

---

## KPIs to track
- Tool completion rate
- Email capture rate
- SQL conversion rate
- Cost per lead
- Tool engagement time

---

## Pass threshold
**≥300 completions and ≥100 qualified leads over 6 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/interactive-content-tools`_

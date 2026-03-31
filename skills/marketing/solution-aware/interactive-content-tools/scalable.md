---
name: interactive-content-tools-scalable
description: >
    Interactive Content Tools — Scalable Automation. Create calculators, assessments, and ROI tools
  that capture leads and provide immediate value, from manual spreadsheet-based tools to embedded
  widgets and AI-driven personalized recommendations.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Scalable Automation"
time: "55 hours over 2 months"
outcome: "≥1,200 completions/month and SQL rate ≥20%"
kpis: ["Tool completion rate", "Email capture rate", "SQL conversion rate", "Revenue attributed to tools", "Tool virality (shares)"]
slug: "interactive-content-tools"
install: "npx gtm-skills add marketing/solution-aware/interactive-content-tools"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - upgrade-prompt
---
# Interactive Content Tools — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Overview
Interactive Content Tools — Scalable Automation. Create calculators, assessments, and ROI tools that capture leads and provide immediate value, from manual spreadsheet-based tools to embedded widgets and AI-driven personalized recommendations.

**Time commitment:** 55 hours over 2 months
**Pass threshold:** ≥1,200 completions/month and SQL rate ≥20%

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Launch systematic testing
Run the `ab-test-orchestrator` drill to test variations of your product experience: messaging copy, timing of prompts, CTA placement, and user segments. Use PostHog feature flags to run experiments. Run each test for statistical significance.

### 2. Build churn prevention
Run the `churn-prevention` drill to configure automated interventions: detect at-risk users via PostHog cohorts (declining usage, missed milestones), trigger Intercom messages or Loops emails to re-engage them.

### 3. Set up expansion prompts
Run the `upgrade-prompt` drill to configure upgrade and expansion triggers: usage threshold notifications, feature gate messages, and team invitation prompts. Time these based on user engagement data from PostHog.

### 4. Evaluate against threshold
Measure against: ≥1,200 completions/month and SQL rate ≥20%. If PASS, proceed to Durable. If FAIL, focus on the highest-impact experiment and iterate.

---

## KPIs to track
- Tool completion rate
- Email capture rate
- SQL conversion rate
- Revenue attributed to tools
- Tool virality (shares)

---

## Pass threshold
**≥1,200 completions/month and SQL rate ≥20%**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/interactive-content-tools`_

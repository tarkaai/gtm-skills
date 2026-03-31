---
name: in-app-onboarding-tour-durable
description: >
    Interactive Product Tour — Durable Intelligence. Interactive in-app tour guiding new users
  through key features and workflows to accelerate time-to-value and increase activation rate.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving activation ≥45% over 6 months via AI"
kpis: ["Activation rate", "Tour completion", "Time to activation", "Experiment velocity", "AI lift"]
slug: "in-app-onboarding-tour"
install: "npx gtm-skills add product/onboard/in-app-onboarding-tour"
drills:
  - dashboard-builder
  - nps-feedback-loop
---
# Interactive Product Tour — Durable Intelligence

> **Stage:** Product → Onboard | **Motion:** Lead Capture Surface | **Channels:** Product

## Overview
Interactive Product Tour — Durable Intelligence. Interactive in-app tour guiding new users through key features and workflows to accelerate time-to-value and increase activation rate.

**Time commitment:** 150 hours over 6 months
**Pass threshold:** Sustained or improving activation ≥45% over 6 months via AI

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build product dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: activation rate trend, conversion funnel by cohort, churn rate trend, expansion revenue, NPS score trend, feature adoption rates. Set alerts for activation or retention drops.

### 2. Launch feedback loops
Run the `nps-feedback-loop` drill to collect and act on user feedback: deploy NPS surveys at key milestones, route feedback to the product team, trigger follow-ups based on score (promoters get referral asks, detractors get personal outreach).

### 3. Autonomous product optimization
Configure the agent to: monitor all product metrics, detect trends (positive or negative), suggest experiments based on data, and generate weekly product health reports. The agent should flag when any metric deviates from baseline by more than 15%.

### 4. Evaluate sustainability
Measure against: Sustained or improving activation ≥45% over 6 months via AI. This level runs continuously. If product metrics sustain or improve, the play is durable. If metrics decay, the agent diagnoses the cause and recommends interventions.

---

## KPIs to track
- Activation rate
- Tour completion
- Time to activation
- Experiment velocity
- AI lift

---

## Pass threshold
**Sustained or improving activation ≥45% over 6 months via AI**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/onboard/in-app-onboarding-tour`_

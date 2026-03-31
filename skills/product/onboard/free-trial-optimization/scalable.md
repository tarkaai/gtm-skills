---
name: free-trial-optimization-scalable
description: >
  Trial Conversion Optimization — Scalable Automation. Systematic A/B testing of onboarding
  flows, churn prevention for at-risk trial users, and contextual upgrade prompts. Maintains
  conversion at scale across 500+ monthly trial starts.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=30% trial-to-paid conversion sustained with 500+ monthly trial starts"
kpis: ["Trial-to-paid conversion rate", "Conversion by signup source", "Upgrade prompt CTR", "Trial churn save rate", "Experiment win rate"]
slug: "free-trial-optimization"
install: "npx gtm-skills add product/onboard/free-trial-optimization"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - upgrade-prompt
---

# Trial Conversion Optimization — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

The trial conversion system handles 500+ monthly trial starts without manual intervention. A/B tests run continuously on onboarding flows, email sequences, and upgrade prompts. At-risk trial users are automatically detected and re-engaged. Upgrade prompts fire contextually based on usage patterns. Conversion rate holds at >=30% at 500+ monthly volume.

## Leading Indicators

- At least 2 A/B tests run per month with statistically significant results
- At-risk trial user detection fires within 24 hours of disengagement signal
- Upgrade prompt CTR exceeds 5% for limit-proximity triggers
- Trial churn intervention saves >=15% of at-risk users (measured by re-engagement within 7 days)
- No single signup source converts below 20% (parity across channels)

## Instructions

### 1. Launch systematic onboarding experiments

Run the `ab-test-orchestrator` drill to test variations of the trial experience. Start with the highest-leverage elements (ordered by typical impact):

**Experiment 1 — Activation path:**
- Control: current onboarding tour
- Variant: shortened tour that reaches the activation milestone in 2 fewer steps
- Metric: 72-hour activation rate
- Minimum sample: 200 per variant
- Duration: 2-4 weeks depending on trial volume

**Experiment 2 — Email sequence timing:**
- Control: current email cadence (Day 0, 1, 3, 5)
- Variant: compressed cadence (Day 0, 1, 2, 4) for shorter trial windows, or extended cadence (Day 0, 2, 5, 9) for longer ones
- Metric: email-attributed activation rate (user clicked email link and then activated within 24h)
- Minimum sample: 200 per variant

**Experiment 3 — Upgrade prompt timing:**
- Control: upgrade prompt at Day 10 (fixed timing)
- Variant: upgrade prompt triggered by usage milestone (e.g., after 5th core action) regardless of trial day
- Metric: upgrade_started rate
- Minimum sample: 200 per variant

Use PostHog feature flags for all experiments. Never stack experiments on the same user — one active experiment per user at a time. Log all experiment designs, results, and decisions in Attio.

### 2. Build trial churn prevention

Run the `churn-prevention` drill scoped to trial users. Configure detection and intervention:

**Detection signals (via PostHog cohorts, checked daily by n8n):**

| Signal | Definition | Risk Score |
|--------|-----------|-----------|
| Ghost user | No login after Day 1 | +40 |
| Tour abandoner | Started tour, did not complete | +25 |
| Usage cliff | 50%+ session drop vs. first 3 days | +30 |
| Stalled activation | Day 5+ with no activation | +35 |
| Billing page bounce | Visited pricing, left without upgrading | +20 |

Aggregate signals into a trial risk score (0-100). Threshold for intervention: score >= 40.

**Interventions (tiered by risk level):**

- **Score 40-60 (medium risk):** Intercom in-app message offering help. Content varies by signal:
  - Ghost user: "Need help getting started? Here's a 2-minute walkthrough." Link to the fastest activation path.
  - Tour abandoner: "Pick up where you left off." Deep link to the tour step they stopped at.
  - Usage cliff: "We noticed you haven't been in lately. Here's what [similar company] did to get value in week 1."

- **Score 60-80 (high risk):** Loops triggered email from the founder. Personalized with the user's specific situation: "I saw you signed up [N] days ago but haven't [activation action] yet. Can I help? Here's my calendar: [Cal.com link]." This email should feel 1:1, not automated.

- **Score 80+ (critical risk):** Create a task in Attio assigned to the account owner for personal outreach within 24 hours. Include the user's signup source, usage data, and specific risk signals.

Track save rate: percentage of at-risk users who re-engage (new session within 7 days of intervention) and eventually convert.

### 3. Deploy contextual upgrade prompts

Run the `upgrade-prompt` drill to create usage-aware conversion triggers:

**Trigger 1 — Limit proximity:**
When a trial user reaches 80% of a plan limit (projects, storage, API calls, team seats), show an in-app message: "You've used [N] of [limit]. Upgrade to [Plan] for unlimited [resource]." Include a one-click upgrade button. Use `intercom-in-app-messages` to target by PostHog cohort.

**Trigger 2 — Feature gate:**
When a trial user attempts a gated feature, show: "This feature is available on [Plan]. Here's what it does: [one-sentence benefit]." Include a "Start [Plan]" CTA and a "Maybe later" dismiss. Track both actions.

**Trigger 3 — Value milestone:**
When a trial user hits a usage milestone (e.g., created 10th project, invited 3rd teammate), show a congratulations message: "You've [milestone]. Teams like yours typically upgrade to get [specific benefit]. Your trial has [N] days left." This positive framing converts better than scarcity messaging.

**Trigger 4 — Trial expiry sequence:**
- Day -5: In-app banner: "Your trial ends in 5 days. Here's what you've built so far: [usage summary]."
- Day -2: Email: "Your trial ends in 2 days. Upgrade now to keep your [specific data/work]."
- Day -1: In-app modal: "Last day of your trial. Upgrade to [Plan] — your [work] is waiting."
- Day 0 (expired): Email: "Your trial ended, but your [work] is saved for 30 days. Upgrade anytime to pick up where you left off."

### 4. Evaluate against threshold

After 2 months with 500+ monthly trial starts, measure:
- Primary: trial-to-paid conversion rate >=30% sustained
- By segment: conversion rate by signup source (organic, paid, referral) — no segment below 20%
- Upgrade prompts: CTR by trigger type, conversion rate by trigger type
- Churn prevention: save rate (re-engagement after intervention), eventual conversion rate of saved users
- Experiments: how many experiments ran, win rate, cumulative lift from winners

If PASS: baseline all metrics (these become the reference for Durable autonomous optimization). Proceed to Durable.
If FAIL: focus on the weakest segment or lowest-converting trigger. Run a targeted experiment on that specific weakness.

## Time Estimate

- 10 hours: A/B test design, setup, and monitoring (across 3+ experiments)
- 15 hours: Churn prevention system (signal detection, n8n workflows, message copy, intervention routing)
- 15 hours: Upgrade prompt system (trigger logic, message design, tracking, expiry sequence)
- 10 hours: Ongoing monitoring and experiment analysis
- 10 hours: Iteration based on results, threshold evaluation, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, cohorts, funnels | Free tier likely sufficient; overage ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages, product tours, chat | $29-85/seat/mo + Proactive Support $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Triggered emails, lifecycle sequences | From $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Churn detection workflows, alert routing | From ~$24/mo cloud or free self-hosted ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Attio | CRM, experiment logging, task assignment | Standard stack |
| Cal.com | Booking links for high-risk outreach | Free tier available ([cal.com/pricing](https://cal.com/pricing)) |

**Estimated play-specific cost:** ~$100-500/mo depending on Intercom tier and trial volume

## Drills Referenced

- `ab-test-orchestrator` — runs systematic experiments on onboarding flows, email timing, and upgrade prompts with statistical rigor
- `churn-prevention` — detects at-risk trial users via usage signals and triggers tiered interventions to re-engage them before the trial expires
- `upgrade-prompt` — deploys contextual upgrade triggers based on usage limits, feature gates, value milestones, and trial expiry countdown

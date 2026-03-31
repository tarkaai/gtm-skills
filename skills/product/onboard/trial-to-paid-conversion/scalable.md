---
name: trial-to-paid-conversion-scalable
description: >
  Trial-to-Paid Conversion — Scalable Automation. Orchestrated multi-channel interventions
  route trial users to the right message on the right channel at the right time. Systematic
  A/B testing of onboarding flows, upgrade prompts, and churn rescue campaigns. Sustains
  conversion at 200+ monthly trial starts.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Email, Product, Direct"
level: "Scalable Automation"
time: "75 hours over 2 months"
outcome: ">=50% trial-to-paid conversion rate sustained with 200+ monthly trial starts"
kpis: ["Trial-to-paid conversion rate trend", "Activation funnel completion", "Intervention effectiveness by channel", "Trial length optimization"]
slug: "trial-to-paid-conversion"
install: "npx gtm-skills add product/onboard/trial-to-paid-conversion"
drills:
  - upgrade-prompt
  - churn-prevention
---

# Trial-to-Paid Conversion — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Email, Product, Direct

## Outcomes

The trial conversion system handles 200+ monthly trial starts with automated multi-channel intervention routing. Upgrade prompts fire contextually based on usage patterns and trial health scores. At-risk trial users are detected within 24 hours and routed to the appropriate rescue intervention. A/B tests run continuously on onboarding flows, email sequences, and upgrade timing. Conversion holds at >= 50% across 200+ monthly trials.

## Leading Indicators

- At-risk trial user detection fires within 24 hours of the first disengagement signal
- Upgrade prompt CTR exceeds 5% for limit-proximity triggers and 8% for value-milestone triggers
- Churn intervention saves >= 15% of at-risk Warm-segment users (re-engagement within 7 days)
- No single signup source converts below 30% (channel parity)
- At least 2 A/B tests run per month with statistically significant results
- Human sales escalation for high-value trials closes at >= 25%

## Instructions

### 1. Deploy contextual upgrade prompts

Run the `upgrade-prompt` drill to build usage-aware conversion triggers that fire at the right moment for each trial user:

**Trigger 1 — Limit proximity:**
When a trial user reaches 80% of any plan limit (projects, storage, API calls, team seats), show an in-app message via Intercom: "You've used [N] of [limit]. Upgrade to [Plan] for unlimited [resource]." Include a one-click upgrade button. Use PostHog cohorts to target users approaching limits.

Track: `upgrade_prompt_shown` with `trigger_reason: limit_proximity`, `upgrade_started`, `payment_completed`.

**Trigger 2 — Feature gate:**
When a trial user attempts a gated premium feature, show: "This feature is available on [Plan]. Here's what it does: [one-sentence benefit]." Include "Start [Plan]" CTA and "Maybe later" dismiss. Track both actions.

**Trigger 3 — Value milestone:**
When a trial user hits a significant usage milestone (e.g., created 10th project, completed 5th workflow, invited 3rd teammate), show a congratulations message: "You've [milestone]. Teams like yours upgrade to get [specific benefit]. Your trial has [N] days left." Positive framing converts better than scarcity messaging at this trigger point.

**Trigger 4 — Trial expiry countdown:**
- Day -5: In-app banner: "Your trial ends in 5 days. Here's what you've built: [usage summary]."
- Day -2: Email from Loops: "Your trial ends in 2 days. Upgrade now to keep your [specific work]."
- Day -1: In-app modal (higher visibility): "Last day of your trial. Upgrade to [Plan] — your [work] is waiting."
- Day 0 (expired): Email: "Your trial ended, but your [work] is saved for 30 days. Upgrade anytime to pick up where you left off."

Measure conversion rate by trigger type. Target: limit-proximity CTR >= 5%, value-milestone CTR >= 8%, feature-gate CTR >= 6%, expiry-countdown CTR >= 4%.

### 2. Build trial churn prevention

Run the `churn-prevention` drill scoped to trial users. Configure detection and tiered intervention:

**Detection signals (PostHog cohorts, checked daily by n8n):**

| Signal | Definition | Risk Score |
|--------|-----------|-----------|
| Ghost user | No login after Day 1 | +40 |
| Tour abandoner | Started onboarding tour, did not complete | +25 |
| Usage cliff | 50%+ session drop vs. first 3 days | +30 |
| Stalled activation | Day 5+ with no activation_reached | +35 |
| Billing page bounce | Visited pricing page, left without upgrading | +20 |

Aggregate signals into a trial churn risk score (0-100). Intervention threshold: score >= 40.

**Tiered interventions:**

- **Score 40-60 (medium risk):** Intercom in-app message offering targeted help. Content varies by the dominant risk signal:
  - Ghost user: "Need help getting started? Here's a 2-minute walkthrough." Link to the fastest activation path.
  - Tour abandoner: "Pick up where you left off." Deep link to the tour step they stopped at.
  - Usage cliff: "We noticed you haven't been in lately. Here's what [similar company] did to get value in their first week."

- **Score 60-80 (high risk):** Loops triggered email from the founder. Personalized with the user's specific situation: "I saw you signed up [N] days ago but haven't [activation action] yet. Can I help? Here's my calendar: [Cal.com link]." Must feel 1:1, not automated.

- **Score 80+ (critical risk):** Create an Attio task assigned to the account owner for personal outreach within 24 hours. Include: signup source, usage data, specific risk signals, and recommended talking points.

Track save rate: percentage of at-risk users who re-engage (new session within 7 days of intervention) and eventually convert to paid.

### 3. Deploy multi-channel intervention orchestration

Run the the trial intervention orchestration workflow (see instructions below) drill to route every trial user to the right intervention on the right channel:

1. Connect the daily `trial-activation-scoring` output to the intervention routing engine
2. Configure the intervention matrix that maps (segment, trial day, trajectory) to (intervention type, channel, priority)
3. Wire the three delivery channels:
   - **In-app (Intercom):** milestone coaching, upgrade nudges, urgency prompts
   - **Email (Loops):** quick-start help, use-case coaching, rescue offers, expiry countdown
   - **Human (Attio):** high-value trial escalation to sales with deal creation and context
4. Implement anti-fatigue rules: no same intervention type within 48 hours, max 1 email per day, max 2 in-app messages per day
5. Track every intervention in Attio: type, channel, timestamp, user response

**A/B testing the intervention matrix:**
Use PostHog feature flags to test intervention variations:

- **Test 1 — Upgrade timing:** upgrade nudge at Day 8 (fixed) vs. on third milestone completion (behavioral). Metric: upgrade_started rate.
- **Test 2 — Rescue channel:** in-app message vs. email for Warm-segment Day 4-7 users. Metric: re-engagement within 48 hours.
- **Test 3 — Urgency framing:** loss aversion ("keep your work") vs. gain framing ("unlock [benefit]") for Day 12-14 prompts. Metric: payment_completed rate.

Minimum 100 users per variant. Never stack experiments on the same user. Log all experiment designs, results, and decisions in Attio.

### 4. Build the trial performance dashboard

Create a PostHog dashboard for ongoing monitoring:

- **Conversion rate by week (12-week trend):** line chart with 50% target threshold line
- **Conversion by signup source:** bar chart showing paid vs. organic vs. referral vs. direct
- **Intervention effectiveness:** table showing reach, engagement, conversion lift for each intervention type
- **Upgrade prompt performance:** impressions, CTR, and conversion by trigger type
- **Churn prevention save rate:** percentage of at-risk users re-engaged, broken down by risk tier
- **Active experiments:** status, preliminary results, days remaining
- **Cohort heatmap:** weekly signup cohorts showing engagement over trial days

Set alerts: conversion rate drops > 15% below 4-week average, activation rate drops > 20%, any upgrade prompt CTR drops > 40%.

### 5. Evaluate against threshold

After 2 months with 200+ monthly trial starts, measure:

- **Primary:** trial-to-paid conversion rate >= 50% sustained
- **By segment:** Hot conversion >= 70%, Warm >= 40%, Cold < 15%
- **Upgrade prompts:** CTR by trigger type meets targets (limit >= 5%, value >= 8%, gate >= 6%, expiry >= 4%)
- **Churn prevention:** save rate >= 15% for medium-risk, >= 10% for high-risk
- **Experiments:** 4+ experiments run, >= 30% win rate, cumulative lift documented
- **Channel parity:** no single signup source converts below 30%

If PASS: baseline all metrics. These become the reference data that the autonomous optimization loop monitors at Durable level. Proceed to Durable.
If FAIL: identify the weakest segment, lowest-performing intervention, or lowest-converting channel. Run a targeted experiment on that specific weakness. Re-evaluate after 2 additional weeks.

## Time Estimate

- 15 hours: Upgrade prompt system (trigger logic, message design, tracking, expiry sequence)
- 15 hours: Churn prevention system (signal detection, n8n workflows, intervention copy, escalation routing)
- 20 hours: Intervention orchestration (routing engine, channel wiring, anti-fatigue rules, A/B tests)
- 10 hours: Dashboard build and alert configuration
- 15 hours: Ongoing monitoring, experiment analysis, iteration

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, cohorts, funnels, dashboards | Free tier or ~$0.00005/event overage ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages, product tours, contextual prompts | $29-85/seat/mo + Proactive Support $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Behavioral email sequences, triggered transactional emails | From $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Scoring workflows, intervention routing, alert routing | From ~$24/mo cloud or free self-hosted ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Attio | CRM, intervention logging, experiment records, deal creation | Standard stack |
| Cal.com | Booking links for rescue calls and onboarding | Free tier available ([cal.com/pricing](https://cal.com/pricing)) |

**Estimated play-specific cost:** ~$150-600/mo depending on Intercom tier and trial volume

## Drills Referenced

- `upgrade-prompt` — deploys contextual upgrade triggers based on usage limits, feature gates, value milestones, and trial expiry countdown
- `churn-prevention` — detects at-risk trial users via churn signals, scores risk severity, and triggers tiered interventions to re-engage before the trial expires
- the trial intervention orchestration workflow (see instructions below) — routes each trial user to the right intervention at the right time on the right channel, with anti-fatigue rules and effectiveness tracking

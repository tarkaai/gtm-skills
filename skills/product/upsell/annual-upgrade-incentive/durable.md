---
name: annual-upgrade-incentive-durable
description: >
  Monthly to Annual Conversion — Durable Intelligence. Autonomous optimization loop that
  detects conversion metric changes, generates improvement hypotheses, runs experiments,
  and auto-implements winners to find the local maximum of annual conversion revenue.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "20 hours setup + 2 hours/week ongoing"
outcome: "Annual conversion rate sustains or improves for 3+ consecutive months via autonomous optimization"
kpis: ["Monthly annual-conversion MRR", "Experiment velocity (tests/month)", "Cumulative optimization lift", "Convergence distance", "Annual cohort retention vs monthly cohort", "Offer fatigue rate"]
slug: "annual-upgrade-incentive"
install: "npx gtm-skills add product/upsell/annual-upgrade-incentive"
drills:
  - autonomous-optimization
---

# Monthly to Annual Conversion — Durable Intelligence

> **Stage:** Product -> Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

An AI agent runs the annual upgrade offer system autonomously. It monitors conversion metrics daily, detects when a trigger type's conversion rate or revenue contribution declines, generates hypotheses for what to change, runs A/B experiments, evaluates results, and auto-implements winners. Weekly optimization briefs report what changed and why. The system converges toward the local maximum of annual-conversion-attributed revenue and maintains it as subscriber behavior, pricing, and product features evolve.

## Leading Indicators

- Autonomous experiments running at target velocity of 2-4 per month (confirms the loop is active)
- No manual intervention needed for 4+ consecutive weeks (confirms autonomy)
- Weekly optimization briefs delivered on schedule with actionable content (confirms reporting works)
- Offer fatigue cohort stable or shrinking (confirms the system is not over-experimenting on users)
- Annual cohort retention continues to exceed monthly cohort at 90-day and 180-day marks (confirms the core thesis holds)

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill with these play-specific parameters:

**Primary KPIs to monitor:**
- `annual_upgrade_completed / annual_offer_shown` (conversion rate) per trigger type
- `annual_upgrade_completed / annual_offer_shown` (conversion rate) per discount tier
- Sum of `annual_upgrade_completed.annual_revenue` minus sum of `annual_upgrade_completed.discount_amount` (net annual conversion revenue)
- Annual cohort 90-day retention vs monthly cohort 90-day retention (retention lift delta)

**Anomaly thresholds:**
- Normal: conversion rate within +/-10% of 4-week rolling average
- Plateau: conversion rate within +/-2% for 3+ consecutive weeks
- Drop: conversion rate declined >20% from 4-week average
- Spike: conversion rate increased >50% (investigate — could be a product change, price increase rumor, or seasonal effect driving urgency)

**Experiment scope (what the agent can change without human approval):**
- Offer copy (headline, body text, savings framing, CTA label)
- Offer timing (days before renewal, time of day, day of week)
- Offer surface (modal vs banner vs tooltip vs inline vs email)
- Discount framing (same discount presented differently: "2 months free" vs "Save $X" vs "17% off")
- Segment-specific variant assignment (which tenure/plan/usage segments see which offer variant)
- Email subject line and send timing for email-based offers

**Human approval required for:**
- Changing the actual discount amount (not just the framing) — price changes need human sign-off
- Adding or removing a trigger type (affects which users see offers)
- Changing frequency cap rules (affects all subscribers)
- Any experiment affecting more than 50% of total offer impressions
- Changes to the Stripe checkout flow or pricing page

### 2. Configure the monitoring phase

Using the `autonomous-optimization` drill Phase 1, build an n8n workflow (daily cron, 08:00 UTC) that:

1. Queries PostHog for each trigger type's conversion rate over the last 7 days
2. Queries PostHog for each discount tier's conversion rate over the last 7 days
3. Compares both against their respective 4-week rolling averages
4. Checks the offer fatigue cohort size from the `autonomous-optimization` drill
5. Checks net annual conversion revenue trend: is revenue flat, growing, or declining
6. Queries Stripe for annual-to-monthly revert count in the last 7 days (regret signal)
7. Checks annual cohort retention: compare 90-day retention for users who converted to annual in the last 6 months vs monthly users in the same period
8. Classifies the state: normal, plateau, drop, or spike
9. If anomaly detected, triggers Phase 2 (diagnosis)
10. If normal, logs the health check to Attio and moves on

### 3. Configure the diagnosis and experiment phases

Using the `autonomous-optimization` drill Phases 2-4:

**Diagnosis:** When an anomaly is detected, the agent gathers:
- Which trigger type(s) and/or discount tier(s) are affected
- The current offer variant running for each affected segment
- Recent experiment history (what was last changed and when)
- Offer fatigue cohort growth rate
- Annual-to-monthly revert rate (are recent converts regretting the switch?)
- External factors: recent product changes, pricing announcements, competitive moves, seasonal billing patterns (Q4 often sees lower annual conversion because users want to wait for new-year budgets)

The agent generates 3 ranked hypotheses. Example hypotheses for a conversion drop on renewal-proximity offers:

1. "Offer copy became stale — monthly subscribers who have seen the same offer 2+ times are tuning it out. Test a variant that uses their personal usage data: 'You used [product] [N] times this month. Lock in your rate and save $X/year.'" (low risk)
2. "Offer timing is suboptimal — the 3-7 day pre-renewal window may be too early. Test a 1-3 day window where the upcoming charge feels more immediate." (low risk)
3. "The discount tier is no longer competitive — a competitor just launched an annual discount promotion. Increase the discount from 2 months free to 3 months free for this segment." (medium risk — requires human approval because it changes the actual discount amount)

**Experiment:** The top hypothesis (that does not require human approval) becomes a PostHog experiment. The agent:
- Creates the experiment in PostHog with a feature flag splitting offer impressions between control and variant
- Implements the variant (e.g., new copy in Intercom, adjusted timing in n8n)
- Sets minimum duration: 7 days or 100 impressions per variant, whichever is longer
- Logs the experiment in Attio with hypothesis, start date, and success criteria

**Evaluation:** When the experiment completes:
- Pull results from PostHog
- If variant wins with >=95% confidence and net revenue per conversion is equal or better: adopt the variant, update the live offer configuration
- If no significant difference: keep the simpler variant, log the result, return to monitoring
- If variant loses: revert, log the learning, wait 7-day cooldown before the next experiment on the same trigger/segment
- Special check: verify the winning variant does not increase the annual-to-monthly revert rate (a variant could boost initial conversion but attract less committed users)

### 4. Configure weekly optimization briefs

Using the `autonomous-optimization` drill Phase 5, the agent generates a weekly brief (every Monday) that includes:

- **This week's metrics:** Conversion rate, net revenue, and offer volume per trigger type and discount tier
- **Annual cohort health:** 30/60/90-day retention for the annual cohort vs monthly cohort. If the gap is shrinking, flag as a strategic concern (the play's core value proposition is weakening)
- **Experiments completed:** hypothesis, result (win/loss/inconclusive), confidence level, impact on conversion rate and net revenue
- **Experiments in progress:** what is being tested, expected completion date, early directional signal
- **Anomalies detected:** what happened and what action was taken
- **Regret rate:** Annual-to-monthly reverts this week. If trending up, flag for investigation.
- **Convergence status:** Are successive experiments producing diminishing returns? If 3 consecutive experiments produced <2% improvement on a trigger type, report that trigger as converged
- **Recommendations:** What the agent plans to test next, and any items requiring human decision

Post the brief to Slack and store in Attio as a note on the annual-upgrade-incentive campaign record.

### 5. Maintain the health monitor

The `autonomous-optimization` drill (deployed at Baseline) continues running in parallel. It provides the data layer that the autonomous optimization loop queries. Ensure:

- Degradation alerts still fire (redundant check — the optimization loop also monitors, but the health monitor catches issues during experiment cooldown periods)
- Revenue attribution is accurate (monthly spot-check: does the sum of annual conversion revenue match actual Stripe annual subscription revenue for the period?)
- Offer fatigue cohort is reviewed in the weekly brief (the optimization loop should never increase the fatigue rate through over-experimentation)
- Annual cohort retention comparison is updated as new 90-day and 180-day data becomes available
- Stripe billing lifecycle events (renewals, downgrades, cancellations, payment failures) are tracked for the annual cohort

### 6. Define convergence and steady state

The autonomous optimization loop runs indefinitely. However, it should detect convergence per trigger type and per segment:

- **Converged:** 3 consecutive experiments on a trigger type/segment produced <2% improvement. That segment has reached its local maximum.
- **Action at convergence:** Reduce experiment frequency from continuous to monthly maintenance tests. Reduce monitoring from daily to weekly. Report the converged performance level.
- **Breaking convergence:** If a product change, pricing change, competitive move, or seasonal shift causes metrics to move >15% from the converged level, re-enter active optimization mode.

When ALL trigger types and segments converge, the play is at its local maximum. The agent reports: "Annual upgrade incentive optimized. Current performance: [conversion rate per trigger, net revenue per conversion, annual cohort retention delta]. Further gains require strategic changes (new discount structures, product bundling, pricing model changes) rather than tactical optimization of the existing offer system."

**Renewal lifecycle optimization:** As the first annual cohorts approach their 12-month renewal, the agent adds a new monitoring dimension: annual renewal rate. If annual subscribers are not renewing at a higher rate than monthly subscribers retain, the play's long-term thesis needs re-evaluation. Add `annual_renewal_completed` and `annual_renewal_churned` events to PostHog and incorporate them into the optimization loop.

## Time Estimate

- 8 hours: Configure autonomous optimization loop (n8n workflows for daily monitoring, diagnosis triggers, experiment management)
- 4 hours: Set up hypothesis generation and experiment evaluation prompts for Claude
- 4 hours: Configure weekly brief generation and Slack/Attio delivery
- 2 hours: Define convergence criteria and steady-state monitoring
- 2 hours: End-to-end test of the full loop (simulate an anomaly and verify the loop responds correctly)
- Ongoing: 2 hours/week reviewing weekly briefs and approving experiments that require human sign-off

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, anomaly detection, retention analysis, dashboards | Free tier: 1M events/mo + 1M flag requests/mo; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app offer delivery, segment targeting | Advanced $85/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email offer delivery with audience segmentation | From $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Optimization loop orchestration (daily cron, webhook triggers, experiment management) | Self-hosted free; Cloud from EUR 24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation and experiment evaluation via Claude | Sonnet 4.6: $3/$15 per 1M input/output tokens; est. $20-50/mo at 2-4 experiments/mo ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Stripe | Annual subscription management, billing lifecycle tracking | Billing Starter 0.5% recurring + 2.9% + $0.30/transaction ([stripe.com/pricing](https://stripe.com/pricing)) |
| Attio | Campaign record, experiment log, optimization brief storage | Free for 3 users; Plus $29/seat/mo ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific monthly cost at Durable:** $250-500/mo (Intercom Advanced + Loops + Anthropic API are the main drivers; n8n, PostHog, and Attio likely within free or low-usage tiers).

## Drills Referenced

- `autonomous-optimization` — the core monitor -> diagnose -> experiment -> evaluate -> implement loop that makes Durable fundamentally different from Scalable
- `autonomous-optimization` — provides the per-trigger funnel data, degradation alerts, fatigue cohorts, retention comparison, and revenue attribution that the optimization loop queries

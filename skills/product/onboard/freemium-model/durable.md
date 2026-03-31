---
name: freemium-model-durable
description: >
  Freemium Tier Strategy — Durable Intelligence. Autonomous agent loop that monitors the
  free-to-paid conversion pipeline, detects metric anomalies, generates improvement hypotheses,
  runs A/B experiments on prompts and gating, and auto-implements winners. Converges when
  successive experiments produce <2% improvement.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving conversion >=6% over 6 months via autonomous optimization"
kpis: ["Free signups", "Free-to-paid rate", "Median days to upgrade", "Experiment velocity", "AI lift vs. Scalable baseline", "Revenue from free-to-paid conversions"]
slug: "freemium-model"
install: "npx gtm-skills add product/onboard/freemium-model"
drills:
  - autonomous-optimization
  - freemium-conversion-health-report
  - pricing-page-conversion-monitor
---

# Freemium Tier Strategy — Durable Intelligence

> **Stage:** Product -> Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The freemium conversion system operates autonomously. An always-on agent loop monitors free-to-paid metrics, detects when conversion rates plateau or decline, generates hypotheses for improvement, runs A/B experiments on prompt copy, gate placement, email cadence, segment routing, and pricing page layout, evaluates results, and auto-implements winners. The agent produces weekly optimization briefs. The system converges when successive experiments produce <2% improvement -- the conversion pipeline has found its local maximum for the current product, pricing, and user base.

## Leading Indicators

- Autonomous optimization loop runs continuously without human intervention for 4+ weeks
- At least 1 experiment per month is auto-designed, run, and evaluated
- Weekly optimization briefs are generated and posted to Slack with actionable insights
- No manual prompt adjustments needed -- the agent handles drift detection and self-correction
- Guardrail alerts fire correctly when thresholds are breached (tested by simulating a conversion rate drop)
- Free-to-paid rate matches or exceeds the Scalable level's best performance
- Prompt fatigue rate stays below 15% without manual intervention (the agent auto-adjusts prompt frequency)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the freemium conversion play. The optimization loop has 5 phases:

**Phase 1 -- Monitor (daily via n8n cron):**
The agent runs `posthog-anomaly-detection` on the play's core KPIs: free-to-paid rate (overall and per trigger type), median days to upgrade, free user activation rate, prompt CTR per surface, prompt fatigue rate, revenue from conversions, free user pool health (active %, activated %, upgrade-ready %). It compares the last 2 weeks against the 4-week rolling average and classifies each metric as normal, plateau, drop, or spike. If any anomaly is detected, the loop triggers Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**
The agent gathers context: current prompt configurations (copy, timing, surfaces, frequency caps), feature gating rules (readiness thresholds, tier assignments), recent A/B test history, free user segment distribution changes, pricing page metrics. It runs `hypothesis-generation` to produce 3 ranked hypotheses for what to change. Examples of hypotheses the agent might generate for this play:

- "Shift the limit-proximity prompt trigger from 85% to 75% consumed -- conversion velocity data shows 40% of users who reach 85% have already decided not to upgrade, while users at 75% are still exploring and more receptive to contextual messaging."
- "Add an in-app usage progress bar to the free tier dashboard -- users who can see their consumption trajectory self-identify as approaching limits 3 days earlier, creating a longer conversion consideration window."
- "Compress the time-based email sequence from Day 14 to Day 10 for the high-activation segment -- median days to upgrade for this segment dropped from 12 to 9 last month, and the Day 14 email is arriving after most have already decided."
- "Gate the export feature at the Intermediate readiness tier instead of Advanced -- 35% of free users attempt export within their first week, making it a high-frequency gate encounter that currently fires too late in the user journey."
- "Replace the monthly billing toggle default on the pricing page from annual to monthly for free users -- free-to-paid converters choose monthly 78% of the time, and showing annual first introduces price shock that suppresses conversion."

If the top hypothesis is high-risk (e.g., removing a feature gate entirely, changing free tier limits, restructuring the pricing page layout), the agent sends a Slack alert and waits for human approval before proceeding.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
The agent implements the experiment using PostHog feature flags. It splits incoming free users between control (current configuration) and variant (hypothesis change). Minimum experiment duration: 7 days or 100 free users per variant, whichever is longer.

For prompt experiments: the agent creates variant Intercom messages and variant Loops emails, routing the variant group to them via the n8n orchestrator.

For gating experiments: the agent adjusts PostHog feature flag cohort criteria for the variant group while keeping control on the current gating rules.

For pricing page experiments: the agent creates variant pricing page elements using PostHog feature flags and tracks the variant's conversion funnel separately.

For timing experiments: the agent adjusts the n8n scheduling or Loops sequence delays for the variant group.

**Phase 4 -- Evaluate (triggered by experiment completion):**
The agent runs `experiment-evaluation` to decide: adopt (implement the winner permanently), iterate (build on the result with a new experiment), revert (the variant hurt performance), or extend (insufficient data, keep running).

Adopted changes are logged in Attio with full context: what changed, why, the experiment results, and the confidence level. This creates an audit trail of every conversion system evolution.

**Phase 5 -- Report (weekly via n8n cron):**
The agent generates a weekly optimization brief:
- Anomalies detected this week and their classification
- Experiments running, completed, or queued
- Net free-to-paid rate change from all adopted changes
- Revenue impact: additional MRR from free-to-paid conversions this week vs. pre-optimization baseline
- Prompt fatigue status: current fatigued user %, any automatic frequency adjustments made
- Free user pool health: total free users, active %, activated %, upgrade-ready %, cohort velocity trends
- Current distance from estimated local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Configure freemium-specific guardrails

In addition to the standard `autonomous-optimization` guardrails, add conversion-specific safeguards:

- **Conversion rate floor:** If overall free-to-paid rate drops below 4% for 2 consecutive weeks, pause all experiments and revert to the last known good configuration. The system is losing conversions.
- **Prompt fatigue ceiling:** If prompt-fatigued users exceed 20% of active free users, the agent must auto-reduce prompt frequency across all surfaces by 50% and switch fatigued users to email-only for 14 days.
- **Free user activation floor:** If activation rate (signup to first value action) drops below 50%, pause upgrade experiments. The problem is onboarding, not conversion. Alert the product team.
- **Checkout abandonment spike:** If checkout abandonment rate exceeds 60% for 3 consecutive days, pause pricing page experiments and investigate checkout UX.
- **Revenue per conversion floor:** If average MRR per new conversion drops below 70% of the Scalable-level average, the agent is optimizing for low-value conversions. Flag for human review of which plan tiers are converting.
- **Experiment budget:** Anthropic API spend for hypothesis generation and evaluation must not exceed $50/mo without human approval.

### 3. Deploy the health report at Durable cadence

Run the `freemium-conversion-health-report` drill with enhanced frequency:
- Health check: runs daily (not just weekly)
- Free user lifecycle tracking: state transitions (inactive -> activated -> habitual -> power-free -> upgraded -> churned) monitored daily per cohort
- Weekly health report: integrates with the `autonomous-optimization` weekly brief into a single combined report
- Monthly deep analysis: full review of segment-specific conversion rates, seasonal patterns (holiday signups convert differently), pricing sensitivity trends, and competitive landscape changes (new free alternatives entering the market)

The health report feeds data to the autonomous optimization loop. When it detects a conversion rate drop, a prompt fatigue spike, or a free user activation decline, that becomes an anomaly that triggers the optimization cycle.

### 4. Monitor the pricing page conversion surface

Run the `pricing-page-conversion-monitor` drill to track the self-serve upgrade path:

- Build the pricing page conversion dashboard: visitor trend, plan selection distribution, checkout abandonment, ARPU for new conversions, annual vs. monthly selection rate
- Build the pricing page funnel: `pricing_page_viewed` -> `plan_card_clicked` -> `checkout_started` -> `payment_method_entered` -> `subscription_created`
- Set anomaly detection rules: conversion rate drop >20%, plan mix shift >15pp, checkout abandonment >70%, ARPU drop >15%
- Track pricing sensitivity cohorts: comparison shoppers (3+ pricing page views without converting), plan hesitators (clicked a plan but abandoned checkout), annual-curious (toggled to annual view but selected monthly)
- Feed pricing page anomalies into the autonomous optimization loop as experiment triggers

The pricing page is the final conversion surface. Even if upgrade prompts perform well, a broken or suboptimal pricing page bottlenecks the entire pipeline.

### 5. Detect convergence

The autonomous optimization loop monitors experiment outcomes for convergence. When 3 consecutive experiments produce <2% improvement on free-to-paid rate:

1. The conversion pipeline has reached its local maximum for the current product, pricing, and user base
2. Reduce experiment frequency from continuous to monthly maintenance checks
3. Generate a convergence report: current free-to-paid rate, total improvement since Durable started, revenue attributable to optimization, recommended strategic changes for further gains

Strategic changes that could break convergence and re-activate optimization:
- Adding a new plan tier or restructuring pricing (changes the upgrade value proposition)
- Launching a new product feature that changes the free/paid boundary
- Entering a new market segment with different conversion behavior
- A competitor launching a compelling free tier that shifts user expectations
- Seasonal patterns: Q1 budget cycles, summer slowdowns, holiday signups
- Product changes that affect the value moment or activation metric

Full convergence triggers a shift to maintenance mode: the conversion system continues running, detection continues, but the optimization loop slows to monthly checks. The agent still monitors for anomalies -- external changes re-activate the loop.

### 6. Evaluate sustainability

After 6 months, measure against the pass threshold:

- Free-to-paid rate: sustained at or above 6% (the Scalable level's target), or improving
- Median days to upgrade: stable or decreasing
- Revenue from free-to-paid conversions: tracked monthly, showing stable or increasing trend
- Experiment velocity: at least 2 experiments per month during active optimization
- AI lift: measurable improvement attributable to autonomous optimization vs. the Scalable-level static configuration
- Prompt fatigue: maintained below 15% without manual intervention

This level runs continuously. Review monthly: what improved, what converged, what external factors changed, and whether the local maximum has shifted.

## Time Estimate

- 20 hours: deploy and configure the autonomous optimization loop (n8n workflows, Anthropic prompts, PostHog integrations, guardrails)
- 10 hours: configure freemium-specific guardrails and test them (simulate conversion drops, fatigue spikes, activation declines)
- 10 hours: enhance health report for Durable cadence (daily lifecycle tracking, monthly deep review)
- 8 hours: deploy pricing page conversion monitor (dashboard, funnel, anomaly detection)
- 70 hours: ongoing monitoring, hypothesis review, guardrail management over 6 months (~3 hours/week)
- 20 hours: monthly strategic reviews, convergence analysis, and reporting
- 12 hours: documentation, convergence report, maintenance mode setup

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, dashboards, funnels | Free up to 1M events/mo; paid from $0/mo + usage -- [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app upgrade prompts (modified by optimization loop) | Essential $29/seat/mo -- [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Upgrade email sequences (modified by optimization loop) | $49/mo for 5,000 contacts -- [loops.so/pricing](https://loops.so/pricing) |
| Attio | CRM records, experiment audit trail, revenue tracking | Free up to 3 seats -- [attio.com/pricing](https://attio.com/pricing) |
| n8n | Optimization loop orchestration, scheduling, webhook processing | Free self-hosted; cloud from $24/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Stripe | Checkout sessions, subscription management, pricing tables | 2.9% + $0.30 per transaction -- [stripe.com/pricing](https://stripe.com/pricing) |
| Anthropic API (Claude) | Hypothesis generation, experiment evaluation, weekly briefs | ~$30-50/mo -- [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost: ~$140-370/mo** (Intercom + Loops + n8n + Anthropic API; PostHog and Attio free tiers may be sufficient depending on volume)

## Drills Referenced

- `autonomous-optimization` -- the core always-on monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum of free-to-paid conversion
- `freemium-conversion-health-report` -- monitors free-to-paid pipeline health at Durable cadence with daily lifecycle tracking, weekly briefs, and monthly deep analysis
- `pricing-page-conversion-monitor` -- monitors the self-serve upgrade path (pricing page -> checkout -> subscription) and feeds anomalies into the optimization loop

---
name: in-product-upgrade-flow-durable
description: >
  Self-Serve Upgrade UX — Durable Intelligence. Autonomous optimization loop
  that detects upgrade funnel anomalies, generates hypotheses, runs A/B
  experiments on upgrade surfaces and checkout flows, and auto-implements winners
  to sustain and improve self-serve upgrade rates. Weekly health reports track
  progress toward the local maximum.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving self-serve upgrade rate ≥10% and upgrade-driven MRR growing or stable over 6 months via autonomous optimization"
kpis: ["Self-serve upgrade rate", "Upgrade-driven MRR", "Experiment velocity", "Optimization lift", "Checkout abandonment rate", "Auto-upgrade acceptance rate", "Distance from local maximum"]
slug: "in-product-upgrade-flow"
install: "npx gtm-skills add product/upsell/in-product-upgrade-flow"
drills:
  - autonomous-optimization
  - upgrade-prompt-health-monitor
---

# Self-Serve Upgrade UX — Durable Intelligence

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Self-serve upgrade rate sustained at or above 10% and upgrade-driven MRR stable or growing for 6 consecutive months. The autonomous optimization loop continuously detects when upgrade funnel performance changes (conversion drops, checkout abandonment spikes, trigger fatigue, auto-upgrade rejection increases), generates hypotheses for what to adjust, runs A/B experiments on upgrade surfaces, checkout flows, and trigger timing, and auto-implements winners. Weekly health reports track progress toward the local maximum. When successive experiments produce less than 2% improvement, the upgrade system has converged and shifts to maintenance mode.

## Leading Indicators

- Anomaly detection catching metric shifts within 24 hours (the monitoring loop is working)
- At least 2 experiments completed per month with documented outcomes
- Winning experiments producing measurable lift (>2% improvement in targeted metric)
- Upgrade surface fatigue index stable or declining across all trigger types (surfaces are not wearing out)
- Auto-upgrade acceptance rate holding at >=50% (the auto-upgrade flow has not degraded)
- New cohorts of free/lower-tier users converting at rates comparable to or better than early cohorts (the system is not exhausting a fixed pool)
- Checkout abandonment rate trending downward or stable (checkout friction is not increasing)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on monitor-diagnose-experiment-evaluate-implement cycle for the self-serve upgrade system:

**Monitor (daily via n8n cron):**
- Query PostHog for the upgrade system's primary KPIs: overall self-serve upgrade rate, per-trigger conversion rates (limit proximity, feature gate, growth signal, auto-upgrade), upgrade-driven MRR, checkout abandonment rate, auto-upgrade acceptance rate, surface dismissal rate, surface fatigue rate
- Compare last 2 weeks against 4-week rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If all metrics normal, log to Attio and take no action
- If any anomaly detected, proceed to diagnosis

**Diagnose (triggered by anomaly):**
- Pull the upgrade system's current configuration from Attio: active trigger types, surface variants per trigger, checkout flow configuration, auto-upgrade rules, segment routing, suppression settings, experiment history
- Pull 8-week metric history from PostHog
- Generate 3 ranked hypotheses using Claude. Examples of hypotheses the agent might generate:
  - "Self-serve upgrade rate dropped 12% this week because the highest-volume trigger (limit proximity) has been showing the same modal copy for 6 weeks. Test refreshed copy that references the user's specific resource usage: 'You have used 23 of 25 seats this month' instead of the generic 'You are approaching your limit.'"
  - "Checkout abandonment spiked 20% because a recent product update added an extra confirmation step to the billing page. Test removing the confirmation step and replacing it with an inline plan preview directly on the upgrade surface."
  - "Auto-upgrade opt-out rate increased 15pp because the grace period email subject line ('Your plan is upgrading') sounds threatening. Test a benefit-framed subject: 'We are expanding your [resource] limit to keep you running.'"
  - "Feature gate trigger conversion plateaued while limit proximity conversion keeps improving. Test adding a time-limited trial offer on feature gates (like the feature-gating play) instead of the current direct upgrade CTA."
  - "Growth-signal trigger has the lowest conversion across all triggers (3%). Test changing the surface from a slide-in panel to a congratulatory modal: 'Your team just hit [milestone]. Teams your size typically use Pro for [specific capability].'"
- Store hypotheses in Attio. If top hypothesis is high-risk (affects pricing display, changes auto-upgrade rules, or modifies checkout payment flow), send Slack alert for human review and stop.

**Experiment (triggered by hypothesis acceptance):**
- Create a PostHog feature flag splitting the affected trigger/segment between control (current) and variant (hypothesis change)
- Implement the variant: if the hypothesis targets surface UX, update the surface component's PostHog flag variant; if the hypothesis targets checkout flow, create a checkout variant path; if the hypothesis targets auto-upgrade messaging, create a Loops email variant; if the hypothesis targets timing or suppression, adjust the n8n routing workflow
- Run for minimum 7 days or until 100+ samples per variant, whichever is longer
- Log experiment start in Attio: hypothesis, affected trigger/segment, start date, expected duration, success criteria

**Evaluate (triggered by experiment completion):**
- Pull results from PostHog experiments API
- Decision tree:
  - **Adopt:** Variant outperforms control with >95% confidence and >2% improvement. Update the live upgrade configuration. Log the change.
  - **Iterate:** Results inconclusive or marginal. Generate a refined hypothesis building on this result. Return to diagnosis.
  - **Revert:** Variant underperforms control. Disable the variant, restore control. Log the failure. Wait 7 days before testing the same variable.
  - **Extend:** Insufficient sample size. Continue for another period.

**Guardrails:**
- Maximum 1 active experiment per trigger type at a time. Never stack experiments on the same upgrade surface.
- If self-serve upgrade rate drops >30% during any experiment, auto-revert immediately.
- Maximum 4 experiments per month across the upgrade system. If all 4 fail, pause optimization and flag for human strategic review.
- Never experiment on what is not measured: if a KPI lacks PostHog tracking, fix tracking first.
- Never modify pricing, plan structure, or Stripe billing logic autonomously. Surface UX, copy, timing, checkout flow presentation, and auto-upgrade messaging are fair game. Pricing changes require human approval.
- Never disable the auto-upgrade rollback mechanism during experiments.

### 2. Generate weekly upgrade flow health reports

Run the `upgrade-prompt-health-monitor` drill to produce a structured weekly brief every Monday:

The report covers:
- **Per-trigger upgrade funnel:** trigger type, surface impressions, clicks, checkouts started, checkouts completed, conversion rate, MRR attributed, trend vs. 4-week average
- **Auto-upgrade pipeline:** grace periods started, opt-outs, completions, retentions at 30 days, payment failures, rollbacks
- **Checkout health:** abandonment rate by step, abandonment rate by device type, average time from surface click to checkout completion
- **Surface fatigue signals:** triggers where surface dismissal rate exceeds 50% or where the same users are seeing surfaces 5+ times without converting, with suppression counts
- **Experiment outcomes:** what was tested, what happened, what was decided, net impact on the targeted metric
- **Revenue attribution:** total upgrade-driven MRR this month, month-over-month trend, average revenue per upgrade, highest-value trigger source, auto-upgrade revenue vs. prompted upgrade revenue
- **AI-generated recommendation:** one specific experiment to run next week, with hypothesis and expected impact
- **Distance from local maximum:** current overall conversion rate vs. estimated ceiling based on diminishing experiment returns

The report is posted to Slack and stored in Attio. Act-severity signals (conversion drops, fatigue spikes, auto-upgrade rejection increases, checkout abandonment spikes) automatically feed into the optimization loop as the next hypothesis to investigate.

### 3. Detect convergence and shift to maintenance

The optimization loop runs indefinitely until it detects convergence: 3 consecutive experiments producing less than 2% improvement. At convergence:

1. The upgrade system has found its local maximum for the current trigger types, surface UX, checkout flow, auto-upgrade rules, and audience composition
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment velocity to 1 per month (maintenance testing for environmental changes: new user behavior patterns, competitive pricing shifts, product changes that affect trigger frequency)
4. Generate a convergence report: "Self-serve upgrade UX optimized. Current self-serve upgrade rate: [X]%. Upgrade-driven MRR: [$Y]/mo. Auto-upgrade acceptance: [Z]%. Estimated ceiling: [W]%. Further gains require strategic changes: new trigger types, pricing restructuring, plan feature rebalancing, or checkout infrastructure overhaul."
5. Shift agent resources to other plays that have not yet converged

### 4. Continuous evaluation

This level runs continuously. Monthly check-in metrics:
- Is self-serve upgrade rate holding at or above 10%?
- Is upgrade-driven MRR stable or growing?
- Is the optimization loop producing at least 1 experiment per month?
- Are weekly health reports being generated and reviewed?
- Is auto-upgrade acceptance rate holding at >=50%?
- Is surface fatigue rate below 20% across all trigger types?
- Is checkout abandonment rate below 40%?

If any metric degrades for 2 consecutive months despite optimization, escalate to human review. The upgrade system may have hit external limits: the addressable user pool for the current plan structure is exhausted, the free tier is too generous (users do not feel the need to upgrade), pricing has become uncompetitive, the checkout infrastructure has fundamental limitations, or the product has not shipped enough premium features to justify the upgrade price. These require strategic intervention, not tactical optimization.

## Time Estimate

- 20 hours: Autonomous optimization loop setup (n8n workflows, PostHog experiment infrastructure, Claude integration for hypothesis generation and evaluation)
- 10 hours: Weekly upgrade flow health report automation setup
- 10 hours: Integration testing across all trigger types, auto-upgrade, and checkout flows
- 110 hours: Ongoing optimization cycles, experiment management, and reporting over 6 months (~4.5 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, funnels, dashboards, session recordings | Growth from $0.00045/event — https://posthog.com/pricing |
| Intercom | Upgrade surface variants, auto-upgrade grace notifications, in-app messages | Essential $29/seat/mo; Proactive Support add-on $349/mo — https://www.intercom.com/pricing |
| Loops | Auto-upgrade grace emails, checkout abandonment follow-ups, experiment email variants | Starter $49/mo — https://loops.so/pricing |
| Stripe | Subscription management, auto-upgrade execution, proration, rollback | 2.9% + $0.30 per transaction — https://stripe.com/pricing |
| n8n | Optimization loop scheduling, auto-upgrade workflows, monitoring, alerting | Free self-hosted; Cloud from ~$24/mo — https://n8n.io/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, report summarization | Claude Sonnet 4.6: $3/$15 per 1M tokens (~$20-50/mo) — https://www.anthropic.com/pricing |
| Attio | Experiment audit trail, upgrade deal records, revenue attribution | Free tier — https://attio.com/pricing |

**Play-specific cost:** ~$250-550/mo (Intercom at scale + Anthropic API + Loops + PostHog Growth tier)

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate loop that finds the local maximum for self-serve upgrade conversion rates
- `upgrade-prompt-health-monitor` — weekly structured report with per-trigger upgrade funnel performance, auto-upgrade pipeline health, checkout analysis, surface fatigue signals, revenue attribution, and recommended next experiment

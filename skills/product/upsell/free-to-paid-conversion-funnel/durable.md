---
name: free-to-paid-conversion-funnel-durable
description: >
  Free to Paid Funnel — Durable Intelligence. Always-on AI agents monitor the full
  free-to-paid funnel, detect metric anomalies, generate improvement hypotheses,
  run A/B experiments, auto-implement winners, and produce weekly optimization briefs.
  Converges when successive experiments yield <2% improvement.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "Ongoing — 8 hours setup, then 2 hours/week agent oversight"
outcome: "Sustained or improving ≥8% free-to-paid conversion rate over 6 months via autonomous optimization"
kpis: ["Free-to-paid conversion rate", "MRR from free-to-paid conversions", "Experiment velocity (experiments/month)", "Cumulative lift from winning experiments", "Prompt fatigue rate"]
slug: "free-to-paid-conversion-funnel"
install: "npx gtm-skills add product/upsell/free-to-paid-conversion-funnel"
drills:
  - autonomous-optimization
  - upgrade-prompt-health-monitor
---

# Free to Paid Funnel — Durable Intelligence

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes
An always-on AI agent monitors the entire free-to-paid funnel, detects when any metric deviates from baseline, generates hypotheses for what to change, runs A/B experiments via PostHog feature flags, evaluates results, and auto-implements winners. The agent produces weekly optimization briefs and converges when successive experiments produce <2% improvement — signaling the play has reached its local maximum.

## Leading Indicators
- The autonomous optimization loop is running: daily monitoring, anomaly detection live
- At least 1 experiment launched within the first 2 weeks
- Weekly optimization brief delivered every Monday
- No undetected metric degradation lasting more than 48 hours
- Prompt fatigue rate stays below 15% despite continuous experimentation
- Cumulative lift from winning experiments is positive month-over-month

## Instructions

### 1. Activate the autonomous optimization loop
Run the `autonomous-optimization` drill to create the always-on monitor → diagnose → experiment → evaluate → implement loop for the free-to-paid funnel. Configure it with these play-specific parameters:

**Primary KPIs to monitor:**
- Overall free-to-paid conversion rate (target: ≥8%)
- Per-surface conversion rate (feature gate, limit alert, time-based, in-app modal)
- Activation rate (signup to first value action)
- Median days from signup to upgrade
- MRR from free-to-paid conversions (weekly)

**Anomaly classification thresholds:**
- **Normal**: metric within ±10% of 4-week rolling average
- **Plateau**: metric within ±2% for 3+ consecutive weeks
- **Drop**: metric declined >20% from 4-week rolling average
- **Spike**: metric increased >50% from 4-week rolling average

**Experiment scope for hypothesis generation:**
The agent generates hypotheses from these categories, ranked by expected impact:
1. **Prompt copy and framing** — benefit-led vs. loss-aversion vs. social-proof for each trigger type
2. **Prompt timing** — how many days post-signup, post-activation, or post-gate-hit before showing the upgrade surface
3. **Prompt surface type** — modal vs. banner vs. tooltip vs. inline for each trigger
4. **Email sequence optimization** — subject lines, send timing, content personalization, number of emails before upgrade ask
5. **Pricing presentation** — monthly vs. annual default, price anchoring, free-vs-paid comparison framing
6. **Checkout flow** — number of steps, payment method options, social proof on checkout page

**Guardrails (CRITICAL):**
- Maximum 1 active experiment at a time on the free-to-paid funnel
- If overall conversion rate drops >30% during an experiment, auto-revert immediately
- Human approval required for: pricing changes, changes affecting >50% of free users, any experiment the agent flags as "high risk"
- After a failed experiment (reverted), wait 7 days before testing the same variable
- Maximum 4 experiments per month. If all 4 fail, pause and flag for human strategic review.
- Never show upgrade prompts to users who have not reached the activation milestone

### 2. Deploy the funnel health monitor
Run the `autonomous-optimization` drill to create the weekly reporting layer specific to this play:

- Weekly health report covering: per-surface conversion table, cohort velocity analysis, free user pool health (total, active, activated, upgrade-ready, fatigued, at-risk), revenue attribution by conversion path
- Daily degradation detection: flag any surface where conversion dropped >20%, flag activation rate drops >15%, flag prompt fatigue exceeding 15% of active free users
- Free user lifecycle tracking: 6 dynamic cohorts (inactive, activated, habitual, upgrade-ready, fatigued, at-risk) with state transition monitoring

The health monitor output feeds directly into the autonomous optimization loop as context for hypothesis generation.

### 3. Deploy upgrade prompt health monitoring
Run the `upgrade-prompt-health-monitor` drill to track the detailed performance of each upgrade surface:

- Per-trigger funnel: prompt shown → clicked → upgrade started → upgrade completed, broken down by trigger type (limit proximity, feature gate, growth signal, time-based)
- Prompt fatigue detection: flag users who dismissed 3+ prompts in 14 days, auto-suppress prompts for fatigued users, switch to email-only nudges
- Revenue attribution: monthly MRR directly attributed to each upgrade prompt trigger type
- Surface comparison: which delivery method (in-app modal, banner, tooltip, email) converts best for each trigger type

### 4. Review weekly optimization briefs
Every Monday, the agent delivers an optimization brief covering:

- **Anomalies detected**: which metrics deviated from baseline, by how much, and for how long
- **Experiments run**: hypothesis tested, control vs. variant performance, statistical significance, decision (adopt/iterate/revert/extend)
- **Net impact**: cumulative conversion rate lift from all adopted changes this week
- **Local maximum status**: current distance from estimated local maximum. When 3 consecutive experiments produce <2% improvement, the agent reports convergence.
- **Recommended focus**: what the agent will test next week, with hypothesis and expected impact

**Human action required:** Review the weekly brief. Approve or veto the recommended next experiment. If the agent reports convergence, decide whether to accept the local maximum or invest in strategic changes (new pricing model, new product capabilities, new user segments) that create a new optimization surface.

### 5. Monitor for convergence
The optimization loop runs indefinitely. The agent detects convergence when 3 consecutive experiments produce <2% improvement on the primary KPI. At convergence:

1. The free-to-paid funnel has reached its local maximum given current product, pricing, and audience
2. Reduce monitoring from daily to weekly
3. Agent delivers a convergence report: final optimized metrics, total cumulative lift from all experiments, list of all changes implemented, recommendation for strategic moves that could unlock a new optimization surface
4. The loop continues at reduced frequency to catch external changes (competitor moves, market shifts, product updates) that create new optimization opportunities

## Time Estimate
- 4 hours: Autonomous optimization loop configuration and play-specific parameter setup
- 2 hours: Funnel health monitor deployment
- 2 hours: Upgrade prompt health monitor deployment
- Ongoing: 2 hours/week reviewing optimization briefs and approving experiments

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, anomaly detection, dashboards | Free up to 1M events/mo; usage-based after — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app upgrade prompts, churn interventions | From $29/seat/mo; Proactive Support $349/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Lifecycle emails, triggered upgrade sequences | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Stripe | Subscription management, billing events | 2.9% + $0.30/txn — [stripe.com/pricing](https://stripe.com/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, optimization briefs | Usage-based — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| n8n | Scheduling, workflow automation for the optimization loop | Self-hosted free; cloud from €24/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Play-specific cost:** Intercom ~$75-350/mo + Loops ~$49/mo + Anthropic API ~$20-50/mo + n8n ~$24/mo = ~$170-475/mo

## Drills Referenced
- `autonomous-optimization` — the core always-on loop: monitor metrics → detect anomalies → generate hypotheses → run A/B experiments → evaluate results → auto-implement winners → weekly optimization briefs
- `autonomous-optimization` — weekly funnel health report covering conversion rates, cohort velocity, free user pool health, revenue attribution, and daily degradation detection
- `upgrade-prompt-health-monitor` — per-trigger upgrade prompt performance tracking, fatigue detection, suppression management, and revenue attribution per surface

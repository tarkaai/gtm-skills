---
name: cross-sell-in-product-durable
description: >
  Related Product Cross-Sell — Durable Intelligence. Autonomous agents continuously
  monitor cross-sell funnel health, detect metric anomalies, generate improvement
  hypotheses, run experiments, and auto-implement winners to find the local maximum.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "40 hours setup + continuous"
outcome: "Cross-sell activation rate sustained or improving for 3+ months; successive optimization experiments produce <2% lift (local maximum reached)"
kpis: ["Cross-sell activation rate trend (3-month rolling)", "ARPU lift trend", "Experiment velocity (experiments completed per month)", "Optimization convergence score", "Cross-sell revenue as % of total MRR"]
slug: "cross-sell-in-product"
install: "npx gtm-skills add product/upsell/cross-sell-in-product"
drills:
  - autonomous-optimization
  - addon-cross-sell-health-monitor
---

# Related Product Cross-Sell — Durable Intelligence

> **Stage:** Product → Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

The cross-sell system runs autonomously with AI agents monitoring, diagnosing, experimenting, and optimizing. The `autonomous-optimization` drill operates the core loop: detect metric anomalies in the cross-sell funnel, generate improvement hypotheses, run A/B experiments via PostHog, evaluate results, and auto-implement winners. The `addon-cross-sell-health-monitor` tracks the full funnel, ARPU impact, and fatigue signals. The system converges when successive experiments produce <2% improvement — meaning you have found the local maximum for cross-sell performance given the current product catalog, user base, and market conditions.

## Leading Indicators

- The autonomous optimization loop fires daily monitoring checks without manual intervention
- At least 2 experiments complete per month with clear adopt/iterate/revert decisions
- Weekly optimization briefs post to Slack on schedule with actionable recommendations
- Cross-sell funnel conversion rates are stable or improving week-over-week
- Fatigue metrics (dismissal rates, suppression counts) are stable or declining
- ARPU lift from cross-sell adopters maintains or increases its premium over single-product users
- No guardrail breaches (primary metric never drops >30% during an experiment)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the cross-sell play. This is the drill that makes Durable fundamentally different from Scalable. Configure it with:

**Monitoring targets (Phase 1):**
- Primary KPIs: cross-sell activation rate (overall and per product), ARPU lift, cross-sell revenue
- Secondary KPIs: surface CTR by type, email channel conversion rate, fatigue score trend
- Anomaly thresholds: ±10% from 4-week rolling average triggers investigation; >20% decline triggers immediate hypothesis generation

**Experiment scope (Phase 3):**
The optimization loop can autonomously experiment on these variables without human approval:
- Surface copy variants (headline, CTA text, benefit framing)
- Surface timing (trigger moment vs. next session vs. delayed)
- Email sequence copy and send timing
- Trigger threshold adjustments (±20% from current threshold)
- Product priority ranking weights

The optimization loop MUST require human approval for:
- Adding or removing products from the cross-sell catalog
- Changes to fatigue suppression durations (these affect user experience broadly)
- Pricing or discount changes in cross-sell offers
- Any change flagged as "high risk" by the hypothesis generator

**Convergence detection (When to Stop):**
The loop detects convergence when 3 consecutive experiments produce <2% improvement in the primary KPI (cross-sell activation rate). At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Generate a convergence report: current performance metrics, experiments completed, total lift achieved, and what would need to change (new products, new user segments, product redesign) to unlock further gains
3. Post the convergence report to Slack and store in Attio

### 2. Deploy the cross-sell health monitor

Run the `addon-cross-sell-health-monitor` drill. This provides the data layer the optimization loop reads from. Configure:

- The cross-sell funnel (impression -> click -> activation start -> activated) broken down by product, surface type, trigger behavior, user plan, and tenure
- The ARPU tracking panels: base ARPU vs. cross-sell ARPU vs. multi-product ARPU
- Daily, weekly, and monthly alert workflows:
  - Daily: impression-to-click rate below 3%, click-to-activation below 10%, dismissal rate above 60%, zero activations for 3 consecutive days
  - Weekly: WoW conversion rate change, ARPU change, weekly cross-sell brief
  - Monthly: monthly cross-sell revenue vs. target, underperforming products (<5% activation rate), fatigue trends

The health monitor also tracks add-on adoption retention:
- 7-day retention: Did cross-sell adopters use the second product in the week after activation?
- 30-day retention: Are they still using it a month later?
- Reversal rate: What percentage of activations are reversed or downgraded within 60 days?

If 30-day retention is below 50% for any product, flag it for the optimization loop — the trigger is converting users who are not ready, or the product's first-use experience needs improvement.

### 3. Configure the weekly optimization brief

The `autonomous-optimization` drill generates weekly briefs. For the cross-sell play, each brief must include:

1. **Top line:** Total cross-sell activations, revenue impact, ARPU change vs. prior week
2. **Funnel health by product:** Conversion rate at each step, trend vs. 4-week average
3. **Experiment status:** Active experiments, completed experiments, decisions made (adopt/iterate/revert)
4. **Fatigue report:** Per-product dismissal rates, users hitting suppression thresholds, global fatigue score trend
5. **Optimization trajectory:** Current distance from estimated local maximum, number of experiments since last >5% improvement
6. **Recommended focus:** One specific variable to experiment on next week, with hypothesis and expected impact

### 4. Evaluate sustainability

This level runs continuously. Monthly check:

- Is cross-sell activation rate sustaining or improving over 3+ months?
- Is ARPU lift from cross-sell adopters stable?
- Is the optimization loop producing experiments that move metrics?
- Are guardrails holding (no metric crashes during experiments)?

If all four are true, the play is durable. If metrics decay despite optimization, the agent diagnoses the root cause:
- **User base saturation:** Most eligible users have already been shown surfaces. Expand triggers or wait for new user cohorts.
- **Product fatigue:** Users are tired of seeing cross-sell prompts. Increase suppression durations and reduce frequency.
- **Market shift:** External factors changed user needs. Re-run `cross-sell-catalog-mapping` to revalidate triggers.
- **Product quality issue:** Cross-sell products are not retaining adopters. Escalate to product team.

## Time Estimate

- 16 hours: Configure autonomous optimization loop (monitoring targets, experiment scope, convergence criteria, guardrails)
- 12 hours: Deploy cross-sell health monitor (funnels, dashboards, alerts, retention tracking)
- 8 hours: Configure weekly brief template and Slack delivery
- 4 hours: Run first manual optimization cycle to validate the loop works end-to-end
- Ongoing: ~2 hours/week reviewing briefs and approving high-risk experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, experiments, feature flags, anomaly detection | Free up to 1M events/mo; paid from $0.00031/event — https://posthog.com/pricing |
| Intercom | In-app cross-sell surfaces | From $39/seat/mo — https://www.intercom.com/pricing |
| Loops | Cross-sell email sequences | Free up to 1,000 contacts; from $49/mo — https://loops.so/pricing |
| n8n | Optimization loop scheduling, trigger detection, alert routing | Free self-hosted / from $20/mo cloud — https://n8n.io/pricing |
| Attio | Cross-sell tracking, experiment logging, expansion deals | From $29/seat/mo — https://attio.com/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly briefs | From $3/MTok input, $15/MTok output — https://www.anthropic.com/pricing |

## Drills Referenced

- `autonomous-optimization` — runs the core Durable loop: monitor metrics daily, detect anomalies, generate hypotheses, run A/B experiments, evaluate results, auto-implement winners, generate weekly optimization briefs
- `addon-cross-sell-health-monitor` — monitors the full cross-sell funnel health, tracks ARPU impact, detects fatigue signals, generates daily/weekly/monthly alerts and reports

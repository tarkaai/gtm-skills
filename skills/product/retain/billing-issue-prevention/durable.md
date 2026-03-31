---
name: billing-issue-prevention-durable
description: >
  Payment Failure Recovery — Durable Intelligence. Autonomous agent loop that monitors recovery
  metrics, generates improvement hypotheses, runs experiments on dunning sequences and timing,
  and auto-implements winners. Converges when successive experiments produce <2% improvement.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving recovery ≥65% over 6 months via autonomous optimization"
kpis: ["Recovery rate", "Involuntary churn rate", "Median time to recovery", "Revenue recovered ($)", "Experiment velocity", "AI lift vs. Scalable baseline"]
slug: "billing-issue-prevention"
install: "npx gtm-skills add product/retain/billing-issue-prevention"
drills:
  - autonomous-optimization
  - payment-recovery-health-monitor
  - dunning-sequence-automation
---

# Payment Failure Recovery — Durable Intelligence

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

The payment recovery system operates autonomously. An always-on agent loop monitors recovery metrics, detects when recovery rates plateau or decline, generates hypotheses for improvement, runs A/B experiments on dunning copy, cadence, channel mix, and segment routing, evaluates results, and auto-implements winners. The agent produces weekly optimization briefs. The system converges when successive experiments produce <2% improvement — the dunning system has found its local maximum for the current customer base and payment landscape.

## Leading Indicators

- Autonomous optimization loop runs continuously without human intervention for 4+ weeks
- At least 1 experiment per month is auto-designed, run, and evaluated
- Weekly optimization briefs are generated and posted to Slack with actionable insights
- No manual dunning adjustments needed — the agent handles drift detection and self-correction
- Guardrail alerts fire correctly when thresholds are breached (tested by simulating a recovery rate drop)
- Recovery rate matches or exceeds the Scalable level's best performance

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the payment failure recovery play. The optimization loop has 5 phases:

**Phase 1 — Monitor (daily via n8n cron):**
The agent runs `posthog-anomaly-detection` on the play's core KPIs: recovery rate (overall and per failure type), involuntary churn rate, median time to recovery, revenue at risk, dunning email open/click rates. It compares the last 2 weeks against the 4-week rolling average and classifies each metric as normal, plateau, drop, or spike. If any anomaly is detected, the loop triggers Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context: current dunning sequence configuration (templates, cadence, segment routing), recent A/B test history, Stripe retry success rates, failure type distribution changes. It runs `hypothesis-generation` to produce 3 ranked hypotheses for what to change. Examples of hypotheses the agent might generate for this play:

- "Shift Day 0 email send time from immediate to 4 hours post-failure — Smart Retry success rate increased 8% last month, suggesting the first email is arriving before Stripe's retry resolves the issue"
- "Add SMS as a recovery channel for the insufficient_funds segment — email open rates for this segment dropped 15% while SMS engagement for transactional messages is 3x higher"
- "Compress the expired_card dunning sequence from 2 emails to 1 — 92% of expired card recoveries happen within 24 hours of the first email, making the Day 3 follow-up unnecessary"
- "Increase in-app banner prominence from subtle to modal for the authentication_required segment — 70% of these customers log in within 48 hours but only 20% notice the current banner"

If the top hypothesis is high-risk (e.g., removing a dunning step entirely, changing the human outreach threshold), the agent sends a Slack alert and waits for human approval before proceeding.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent implements the experiment using PostHog feature flags. It splits incoming payment failures between control (current configuration) and variant (hypothesis change). Minimum experiment duration: 7 days or 50 failures per variant, whichever is longer.

For dunning copy experiments: the agent creates variant email templates in Loops and routes the variant group to them via the n8n orchestrator.

For cadence experiments: the agent adjusts the n8n scheduling for the variant group while keeping control on the current cadence.

For channel experiments: the agent activates an additional channel (SMS, push) for the variant group and measures incremental recovery.

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent runs `experiment-evaluation` to decide: adopt (implement the winner permanently), iterate (build on the result with a new experiment), revert (the variant hurt performance), or extend (insufficient data, keep running).

Adopted changes are logged in Attio with full context: what changed, why, the experiment results, and the confidence level. This creates an audit trail of every dunning system evolution.

**Phase 5 — Report (weekly via n8n cron):**
The agent generates a weekly optimization brief:
- Anomalies detected this week and their classification
- Experiments running, completed, or queued
- Net recovery rate change from all adopted changes
- Revenue impact: additional revenue recovered this week vs. pre-optimization baseline
- Current distance from estimated local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Configure payment-recovery-specific guardrails

In addition to the standard `autonomous-optimization` guardrails, add recovery-specific safeguards:

- **Recovery rate floor:** If overall recovery rate drops below 50% for 2 consecutive weeks, pause all experiments and revert to the last known good configuration. The system is losing more customers than it should.
- **Customer complaint spike:** If the number of support tickets mentioning "billing," "payment," or "dunning" increases 2x in one week, pause experiments. The dunning system may be annoying customers.
- **Channel fatigue:** If email unsubscribe rate from dunning emails exceeds 3%, the cadence is too aggressive. Pause the sequence and extend intervals by 2 days.
- **Human escalation backlog:** If more than 10 high-value accounts are waiting for human outreach for 48+ hours, alert the CS team lead. The routing threshold may need adjustment.
- **Revenue at risk threshold:** If total open invoice amount exceeds $50K, escalate to finance/leadership regardless of other metrics.
- **Experiment budget:** Anthropic API spend for hypothesis generation and evaluation must not exceed $50/mo without human approval.

### 3. Deploy the health monitor at Durable cadence

Run the `payment-recovery-health-monitor` drill with enhanced frequency:
- Health check: runs daily (not just weekly)
- Recovery funnel analysis: runs per-segment daily to detect segment-specific degradation early
- Weekly health report: integrates with the `autonomous-optimization` weekly brief into a single combined report
- Monthly deep analysis: full review of failure type distribution, seasonal patterns (holiday spending impacts), and card network trends

The health monitor feeds data to the autonomous optimization loop. When it detects a recovery rate drop or a failure type distribution shift, that becomes an anomaly that triggers the optimization cycle.

### 4. Maintain the dunning system

The `dunning-sequence-automation` drill continues to run at Durable level. The autonomous optimization loop may modify:
- Email templates (subject lines, copy, CTA placement)
- Sequence cadence (timing between steps)
- Segment routing rules (which failure types get which paths)
- Channel mix (adding SMS, adjusting in-app banner prominence)
- Human outreach thresholds (MRR cutoff for personal outreach)

The dunning system executes whatever the current best configuration is, as updated by the optimization loop.

### 5. Detect convergence

The autonomous optimization loop monitors experiment outcomes for convergence. When 3 consecutive experiments produce <2% improvement on recovery rate:

1. The dunning system has reached its local maximum for the current customer base and payment landscape
2. Reduce experiment frequency from continuous to monthly maintenance checks
3. Generate a convergence report: current recovery rate, total improvement since Durable started, revenue saved attributable to optimization, recommended strategic changes for further gains

Strategic changes that could break convergence and re-activate optimization:
- Adding a new payment method (e.g., ACH, SEPA) that has different failure patterns
- Changing pricing tiers (affects MRR-based routing)
- Expanding to new geographies (different card networks, different failure codes)
- Stripe changing their Smart Retry algorithm
- Seasonal patterns (holiday spending, end-of-year budget cycles)

Full convergence triggers a shift to maintenance mode: dunning system continues running, detection continues, but the optimization loop slows to monthly checks. The agent still monitors for anomalies — external changes re-activate the loop.

### 6. Evaluate sustainability

After 6 months, measure against the pass threshold:

- Recovery rate: sustained at or above 65% (the Scalable level's target), or improving
- Involuntary churn rate: at or below the Scalable baseline, or decreasing
- Revenue recovered: tracked monthly, showing stable or increasing trend
- Experiment velocity: at least 2 experiments per month during active optimization
- AI lift: measurable improvement attributable to autonomous optimization vs. the Scalable-level static configuration

This level runs continuously. Review monthly: what improved, what converged, what external factors changed, and whether the local maximum has shifted.

## Time Estimate

- 20 hours: deploy and configure the autonomous optimization loop (n8n workflows, Anthropic prompts, PostHog integrations, guardrails)
- 10 hours: configure payment-recovery-specific guardrails and test them (simulate recovery drops, complaint spikes)
- 8 hours: enhance health monitor for Durable cadence (daily segment analysis, monthly deep review)
- 80 hours: ongoing monitoring, hypothesis review, guardrail management over 6 months (~3.5 hours/week)
- 20 hours: monthly strategic reviews, convergence analysis, and reporting
- 12 hours: documentation, convergence report, maintenance mode setup

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Stripe | Payment failure data, Smart Retries, billing portal, subscription management | Included with Stripe account — [stripe.com/pricing](https://stripe.com/pricing) |
| Loops | Dunning email sequences (modified by optimization loop) | $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app recovery banners (modified by optimization loop) | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| PostHog | Anomaly detection, experiments, feature flags, dashboards | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Optimization loop orchestration, scheduling, webhook processing | Free self-hosted; cloud from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API (Claude) | Hypothesis generation, experiment evaluation, weekly briefs | ~$30-50/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost: $130-350/mo** (Loops + Intercom + n8n + Anthropic API; PostHog free tier likely sufficient)

## Drills Referenced

- `autonomous-optimization` — the core always-on monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum
- `payment-recovery-health-monitor` — monitors recovery rates, failure types, and dunning effectiveness at Durable cadence with daily segment analysis
- `dunning-sequence-automation` — executes the current best dunning configuration, updated by the optimization loop

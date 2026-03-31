---
name: usage-limit-sales-upsell-durable
description: >
  Usage-Based Upsell — Durable Intelligence. Autonomous agent loop that monitors the
  expansion pipeline, detects when close rates plateau or scoring accuracy drifts,
  generates improvement hypotheses, runs experiments on scoring weights and outreach
  variables, and auto-implements winners. Converges when successive experiments produce
  <2% improvement.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email, Direct"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving expansion close rate >=35% and expansion ARR >=15% of base ARR over 6 months via autonomous optimization"
kpis: ["Expansion close rate trend", "Expansion ARR growth rate", "Scoring model accuracy (Tier 1 vs Tier 2 differential)", "Experiment velocity", "AI lift vs Scalable baseline", "90-day expansion retention"]
slug: "usage-limit-sales-upsell"
install: "npx gtm-skills add product/upsell/usage-limit-sales-upsell"
drills:
  - autonomous-optimization
---

# Usage-Based Upsell — Durable Intelligence

> **Stage:** Product -> Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Direct

## Outcomes

The expansion pipeline operates autonomously. An always-on agent loop monitors scoring accuracy, outreach conversion rates, pipeline velocity, and revenue impact. When any metric plateaus, declines, or spikes, the agent diagnoses the cause, generates improvement hypotheses, designs and runs experiments, evaluates results, and auto-implements winners. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement — the pipeline has found its local maximum for the current product, pricing, and customer base.

## Leading Indicators

- Autonomous optimization loop runs continuously without human intervention for 4+ weeks
- At least 1 experiment per month is auto-designed, run, and evaluated
- Weekly optimization briefs are generated and posted to Slack
- Scoring model accuracy (Tier 1 vs Tier 2 close rate differential) stays above 3x without manual recalibration
- Outreach conversion rates hold steady or improve without manual copy changes
- No manual scoring weight adjustments needed — the agent handles drift from product changes, pricing updates, and market shifts

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the usage-limit sales upsell play. The optimization loop has 5 phases:

**Phase 1 — Monitor (daily via n8n cron):**
The agent queries the `autonomous-optimization` drill's webhook endpoint to retrieve current metrics: expansion close rate, scoring model accuracy (Tier 1 vs Tier 2 differential), outreach sequence conversion rates per touch, pipeline velocity, expansion ARR, and 90-day retention. It compares the last 2 weeks against the 4-week rolling average and classifies each metric as normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), or spike (>50% increase). If any anomaly is detected, the loop triggers Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context: current scoring weights, outreach templates, routing rules, A/B test history from Scalable, 8-week metric trends, per-resource performance breakdown. It runs `hypothesis-generation` to produce 3 ranked hypotheses. Examples specific to this play:

- "Increase the usage proximity weight from 40% to 50% and decrease firmographic fit from 10% to 0% — close rate analysis shows firmographic signals add no predictive value over pure usage data for accounts above $200 MRR"
- "Replace Touch 2 (value proof email) with a personalized usage dashboard screenshot showing the account's consumption trajectory and projected limit-hit date — Touch 2 reply rate dropped 40% in 6 weeks, suggesting the copy has gone stale"
- "Add a new scoring signal: support ticket sentiment — accounts that submit feature requests near usage limits close at 55% vs 28% for accounts with no recent tickets, because feature requests signal product commitment"
- "Split the outreach sequence into two tracks: fast-track for accounts that visited the billing page in the last 7 days (skip to Touch 3 immediately with direct offer) and standard track for everyone else — billing page visits are the strongest single intent signal and these accounts do not need nurturing"
- "Lower the Tier 1 threshold from 65 to 55 for the API-calls resource only — API-limit accounts close at 42% even at lower scores because API limits cause immediate operational pain"

If the top hypothesis is high-risk (affects >50% of pipeline volume or changes scoring weights by >20%), the agent sends a Slack alert and waits for human approval before proceeding.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent implements the experiment using PostHog feature flags. It splits qualifying accounts between control (current configuration) and variant (hypothesis change). Minimum experiment duration: 14 days or 30 qualified accounts per variant, whichever is longer.

For scoring experiments (weight changes, new signals, threshold adjustments): the agent creates a variant scoring configuration that runs in parallel. Both configurations score accounts, but only the control configuration triggers outreach. After the experiment period, compare which scoring configuration better predicted actual expansion outcomes (higher precision and recall for expansion-ready accounts).

For outreach experiments (email copy, sequence timing, offer structure): the agent creates variant templates in Loops and routes a random subset of qualified accounts to the variant. Measure reply rate, meeting booking rate, close rate, and deal size.

For routing experiments (segment thresholds, channel mix, sales vs self-serve boundaries): the agent modifies routing rules for the variant group and measures close rate, pipeline velocity, and expansion retention.

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent runs `experiment-evaluation` to decide:
- **Adopt:** Update the live configuration to use the winning variant. Log the change in Attio with full context: hypothesis, experiment parameters, statistical results, expected ongoing impact.
- **Iterate:** Result was directionally positive but not conclusive. Generate a refined hypothesis and return to Phase 2.
- **Revert:** Variant hurt performance. Disable the variant, restore control, log the failure with reasoning, return to Phase 1.
- **Extend:** Insufficient data. Keep the experiment running for another period.

Every decision is stored in Attio with: hypothesis text, experiment parameters, results (close rate delta, confidence interval, deal size impact), and reasoning.

**Phase 5 — Report (weekly via n8n cron):**
The agent generates a weekly optimization brief:
- Anomalies detected this week and their classification
- Experiments running, completed, or queued
- Net metric change from all adopted changes
- Current performance vs. Scalable baseline (AI lift)
- Revenue impact: expansion ARR this week and trailing 30 days
- Scoring model health: Tier 1 vs Tier 2 differential, false positive rate
- Outreach health: per-touch conversion rates, sequence completion rate
- Current distance from estimated local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Configure play-specific guardrails

In addition to the standard `autonomous-optimization` guardrails, add expansion-pipeline-specific safeguards:

- **Outreach fatigue guard:** If any account receives more than 6 sales touches in a 30-day window across all plays (not just this one), pause this play's outreach for that account. Check Attio for cross-play touch history. Customers should feel served, not hunted.
- **Scoring drift guard:** If the Tier 1 close rate drops below 25% for 2 consecutive weeks, pause all scoring experiments and revert to the last known good scoring configuration. Investigate whether a product change, pricing update, or seasonal shift is the cause.
- **Expansion retention guard:** If 90-day retention of expansion accounts drops below 75%, pause all urgency-based outreach experiments. Pressure upgrades that lead to downgrades destroy LTV. Switch experiment focus to value-based messaging and flexible offer structures.
- **Pipeline flood guard:** If Tier 1 volume exceeds the team's capacity to handle meetings (more than 3 meetings per person per week), temporarily raise the Tier 1 threshold rather than letting accounts queue. Stale expansion deals lose momentum.
- **Negative sentiment guard:** If reply sentiment analysis (via Anthropic) detects more than 10% negative responses in a week, auto-pause the outreach sequence variant that is producing the negativity and revert to control. Flag for human review.
- **Revenue sanity check:** If expansion ARR drops >30% week over week with no corresponding drop in qualified accounts, something is broken in the close process (pricing, product, or sales execution). Pause experiments and alert the team.

### 3. Deploy the expansion health monitor at Durable cadence

Run the `autonomous-optimization` drill with Durable-level configuration:

- Health check: runs daily (scoring accuracy, outreach delivery, pipeline velocity)
- Scoring model recalibration signal: runs weekly (compare predicted vs actual expansion outcomes)
- Expansion retention tracking: runs weekly with 30-day, 60-day, and 90-day cohort analysis
- Weekly health report: integrates with the `autonomous-optimization` weekly brief as a subsection

The health monitor feeds data to the autonomous optimization loop via its webhook endpoint. When it detects drift — scoring accuracy declining, outreach conversion plateauing, retention dropping, pipeline velocity stalling — that becomes an anomaly that triggers the optimization cycle.

### 4. Maintain outreach delivery at Durable level

The the expansion outreach sequence workflow (see instructions below) drill continues to run for every qualified account. The autonomous optimization loop may modify:
- Outreach email copy (subject lines, body content, CTAs)
- Sequence timing (days between touches, behavioral triggers)
- Offer structure (tier upgrade, annual discount, limit extension, custom bundle)
- Routing rules (segment boundaries, channel mix, sales vs self-serve)

The outreach system executes whatever the current best configuration is. Each configuration change is version-controlled in Attio so the agent can revert to any previous state.

### 5. Detect convergence

The autonomous optimization loop monitors experiment outcomes for convergence. When 3 consecutive experiments produce <2% improvement on the primary KPI (expansion close rate):

1. The pipeline has reached its local maximum for the current product, pricing, and customer base
2. Reduce experiment frequency from continuous to monthly maintenance checks
3. Generate a convergence report:
   - Current performance levels across all KPIs
   - Total improvement since Durable started vs Scalable baseline
   - Total expansion ARR attributable to autonomous optimization
   - Scoring model final weights and signal contributions
   - Best-performing outreach configuration (subject line, timing, offer)
   - Per-resource expansion performance ranking
   - Recommended strategic changes for further gains

Strategic changes that could break convergence and unlock further improvement (these require human decision-making, not agent optimization):
- New plan tier or pricing restructure
- New metered resource added to the product
- New expansion channel (phone, LinkedIn DMs, account manager 1:1s)
- Sales team capacity increase (more meetings per week = lower Tier 1 threshold)
- Market shift (economic conditions changing expansion willingness)
- Product changes that alter usage patterns

When any strategic change occurs, the agent re-activates the full optimization loop to find the new local maximum.

### 6. Evaluate sustainability

After 6 months, measure against the pass threshold:

- Expansion close rate: sustained at or above 35% for Tier 1 accounts, or improving
- Expansion ARR: at least 15% of base ARR maintained or growing month over month
- Scoring accuracy: Tier 1 vs Tier 2 close rate differential above 3x with no sustained drops
- Expansion retention: 90-day retention above 85% for expanded accounts
- Experiment velocity: at least 2 experiments per month during active optimization
- AI lift: measurable improvement attributable to autonomous optimization vs. the Scalable-level static configuration
- Pipeline health: no sustained pipeline stalls, no scoring drift requiring manual intervention

This level runs continuously. Review monthly: what improved, what converged, what external factors changed.

## Time Estimate

- 20 hours: deploy and configure the autonomous optimization loop (n8n workflows, Anthropic prompts, PostHog integrations, guardrail implementation)
- 10 hours: configure play-specific guardrails and test them (simulate metric drops, scoring drift, outreach fatigue)
- 10 hours: enhance health monitor for Durable cadence and integrate with optimization loop
- 60 hours: ongoing monitoring, hypothesis review, guardrail management, expansion conversation support over 6 months (~2.5 hours/week)
- 20 hours: monthly strategic reviews, convergence analysis, and report generation
- 10 hours: documentation, convergence report, maintenance mode setup

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Scoring signals, anomaly detection, experiments, feature flags, funnels | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API (Claude Sonnet) | Hypothesis generation, experiment evaluation, weekly briefs, reply sentiment analysis | ~$50-200/mo at Durable scale — [anthropic.com/pricing](https://anthropic.com/pricing) |
| Attio | CRM — expansion deals, experiment audit trail, configuration versioning, scoring storage | Free up to 3 seats; from $29/seat/mo — [attio.com/pricing](https://attio.com/pricing) |
| Loops | Outreach sequences (templates modified by optimization loop) | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Scoring, routing, outreach orchestration, optimization loop scheduling | Free self-hosted; Cloud from EUR 24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Clay | Firmographic enrichment (monthly refresh) | From $149/mo — [clay.com/pricing](https://clay.com/pricing) |
| Intercom | In-app messages (modified by optimization loop) | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| Cal.com | Expansion meeting booking | Free for individuals; Team from $12/user/mo — [cal.com/pricing](https://cal.com/pricing) |

**Estimated play-specific cost: $350-600/mo** (Anthropic API for optimization + Clay enrichment + Loops + increased PostHog events)

## Drills Referenced

- `autonomous-optimization` — the core always-on monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum for expansion close rate and revenue
- `autonomous-optimization` — monitors scoring accuracy, outreach conversion, pipeline velocity, expansion retention, and system health; feeds metrics to the optimization loop
- the expansion outreach sequence workflow (see instructions below) — executes the current best outreach configuration, updated by the optimization loop as experiments produce winners

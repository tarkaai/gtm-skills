---
name: pricing-presentation-framework-durable
description: >
  Pricing Presentation Framework — Durable Intelligence. Always-on AI agents
  continuously optimizing pricing tier structures, value anchoring, discount
  policies, and presentation formats through autonomous experimentation.
  Converges on the local maximum for pricing acceptance and deal profitability.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving pricing acceptance (>=65%) and deal profitability (discount <=10%) over 6 months via autonomous pricing optimization"
kpis: ["Pricing acceptance rate", "Deal profitability (revenue per deal)", "Discount intelligence effectiveness", "Autonomous experiment win rate", "Convergence progress"]
slug: "pricing-presentation-framework"
install: "npx gtm-skills add sales/proposed/pricing-presentation-framework"
drills:
  - autonomous-optimization
---

# Pricing Presentation Framework — Durable Intelligence

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Deploy always-on AI agents that autonomously detect when pricing metrics plateau or decline, generate hypotheses for improvement, run A/B experiments, evaluate results, and auto-implement winners. The system converges on the local maximum of pricing acceptance and deal profitability, then maintains it as market conditions change. Target: sustained >=65% acceptance rate and <=10% average discount over 6 months, with the optimization loop running without manual intervention.

## Leading Indicators

- Autonomous optimization loop running daily (Phase 1: Monitor) with zero manual triggers
- At least 2 experiments autonomously proposed and executed per month
- Experiment win rate >=40% (at least 2 of every 5 experiments produce measurable improvement)
- Weekly pricing intelligence reports generated and distributed automatically
- Convergence signal: successive experiments producing <2% improvement for 3 consecutive experiments
- No acceptance rate drop >15% sustained for more than 2 weeks without auto-intervention

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the pricing presentation play. This creates the core Durable loop:

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check the play's primary KPIs: acceptance rate, average discount, tier match rate, days to acceptance, deal profitability
2. Compare last 2 weeks against 4-week rolling average
3. Classify each KPI: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If all KPIs are normal, log to Attio and take no action
5. If any anomaly is detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context: pull the play's current pricing configuration from Attio (default tier structure, value anchoring template, discount guardrails, winning experiment variants)
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` with the anomaly data + pricing context
4. Receive 3 ranked hypotheses. Examples of pricing-specific hypotheses:
   - "Acceptance rate dropped because the recommended tier price increased 15% last month without corresponding value anchor updates"
   - "Discount requests spiked because a new competitor entered the market with lower list prices"
   - "Days to acceptance increased because the proposal format change (from email to interactive page) added friction for certain buyer personas"
5. Store hypotheses in Attio. If the top hypothesis has risk = "high" (e.g., major pricing structure change), send Slack alert for human review and STOP. Otherwise proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using PostHog feature flags (via `posthog-experiments`)
2. Implement the variant in the pricing automation workflow
3. Set duration: minimum 7 days or until 30+ proposals per variant, whichever is longer
4. Log the experiment start in Attio

Pricing-specific experiment types the system can run autonomously:
- **Tier price adjustment:** Test 5-10% price shifts on specific tiers
- **Value anchoring variation:** Test different pain points emphasized in the value recap
- **Discount guardrail tuning:** Test stricter vs looser discount thresholds
- **Presentation ordering:** Test different tier presentation sequences
- **Follow-up timing:** Test when to send proposal reminders after presentation

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation` with control vs variant data
3. Decision:
   - **Adopt:** Update the live pricing configuration. Log the change with full reasoning.
   - **Iterate:** Generate a refined hypothesis. Return to Phase 2.
   - **Revert:** Restore control. Log the failure with learnings. Return to Phase 1.
4. Store the full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity for the week
2. Calculate net metric change from all adopted changes
3. Generate weekly optimization brief: what changed, why, net impact, convergence progress
4. Post to Slack and store in Attio

### 2. Configure pricing-specific guardrails

**Critical guardrails for pricing optimization:**
- **Rate limit:** Maximum 1 active pricing experiment at a time. Never stack experiments that affect the same pricing variable.
- **Price floor:** No experiment variant can set pricing below the walk-away floor defined in the deal term model. This is non-negotiable.
- **Revert threshold:** If acceptance rate drops >30% during any experiment, auto-revert immediately and alert the team.
- **Discount ceiling:** No experiment can raise the maximum discount authority beyond the current cap without human approval.
- **Human approval required for:**
  - Any price change >10% in either direction
  - Changes to the number of tiers (e.g., dropping from 3 to 2 tiers)
  - Changes to the payment terms structure
  - Any experiment that affects enterprise/strategic deals (ACV > $100K)
- **Cooldown:** After a failed pricing experiment, wait 14 days before testing the same variable again. Pricing changes create prospect confusion if changed too frequently.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for strategic pricing review.

### 3. Run the pricing intelligence monitor at Durable depth

Run the `autonomous-optimization` drill with additional Durable-level analysis:

1. All Scalable-level metrics plus:
   - Experiment pipeline status (queued, running, evaluating)
   - Convergence tracking: is the improvement rate from successive experiments decreasing?
   - Market condition signals: competitive pricing changes, customer segment shifts, seasonal patterns
2. Generate experiment candidates as part of each weekly report
3. Feed experiment candidates directly to the autonomous optimization loop (Phase 2)

The intelligence monitor at Durable level is not just reporting — it is actively feeding the optimization loop with hypotheses derived from trend analysis.

### 4. Build the deal profitability feedback loop

Create an n8n workflow that fires when a deal closes (won or lost):

1. Pull the final deal data: tier selected, discount given, payment terms, total contract value
2. Compare against the proposal: recommended tier vs selected, initial price vs final price, proposed terms vs final terms
3. Compute deal profitability metrics: revenue efficiency (final price / list price), discount efficiency (discount per negotiation round), tier conversion rate
4. Feed this data back to the optimization loop. If closed-won deals that used a specific pricing variant consistently produce higher profitability, that variant gets prioritized in future experiments.
5. If closed-lost deals with a specific rejection reason pattern (e.g., "too expensive" + "selected competitor") reach a threshold (>=5 in 30 days), trigger an autonomous pricing competitiveness review.

### 5. Detect convergence and maintain

The optimization loop runs indefinitely. Monitor for **convergence** — when successive experiments produce diminishing returns:

- Track the improvement percentage from each adopted experiment
- If 3 consecutive experiments produce <2% improvement each, the play has reached its local maximum
- At convergence:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment frequency from 4/month to 1/month (maintenance experiments)
  3. Report to the team: "Pricing presentation framework is optimized. Current performance: {acceptance_rate}% acceptance, {avg_discount}% average discount, ${avg_deal_size} average deal size. Further gains require strategic changes (new product tiers, new market segment, pricing model change) rather than tactical optimization."
  4. Continue monitoring for market-driven anomalies that break convergence (new competitor, economic shift, product change)

## Time Estimate

- 20 hours: deploying autonomous optimization loop (n8n workflows, PostHog experiments, guardrails)
- 10 hours: configuring pricing-specific guardrails and approval workflows
- 15 hours: building deal profitability feedback loop
- 10 hours: configuring Durable-level pricing intelligence monitor
- 65 hours: monitoring, reviewing weekly reports, approving high-risk experiments, strategic adjustments over 6 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, experiment logging, optimization audit trail | Standard stack (excluded from play budget) |
| PostHog | Anomaly detection, experiments, feature flags, dashboards | Standard stack (excluded from play budget) |
| n8n | Optimization loop scheduling, deal profitability workflow, report distribution | Standard stack (excluded from play budget) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, weekly reports, pricing intelligence | ~$50-120/mo for continuous optimization at Sonnet 4.6 rates ($3/$15 per M tokens) — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Play-specific cost:** ~$50-120/month (Claude API for continuous autonomous optimization)

## Drills Referenced

- `autonomous-optimization` — the core Durable loop: monitor metrics daily, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, and report weekly. Converges when successive experiments produce <2% improvement.
- `autonomous-optimization` — weekly pricing intelligence report with Durable-level depth: experiment pipeline, convergence tracking, market signals, and experiment candidate generation
- the deal term ab testing workflow (see instructions below) — executes the experiments designed by the autonomous optimization loop, using PostHog feature flags to test pricing variables against control

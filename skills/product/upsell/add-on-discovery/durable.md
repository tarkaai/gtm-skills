---
name: add-on-discovery-durable
description: >
  Module Cross-Sell — Durable Intelligence. Autonomous AI agents continuously optimize
  add-on discovery surfaces, triggers, and cross-sell paths. The system detects metric
  anomalies, generates improvement hypotheses, runs A/B experiments, and auto-implements
  winners to find the local maximum of cross-sell performance.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "20 hours setup + ongoing autonomous operation over 6 months"
outcome: "Cross-sell activation rate sustained or improving ≥8% with ARPU lift ≥5% over 6 months, with <2% experiment improvement signaling convergence"
kpis: ["Add-on activation rate", "Cross-sell revenue", "ARPU lift", "Experiment velocity", "Optimization ROI", "Convergence score"]
slug: "add-on-discovery"
install: "npx gtm-skills add product/upsell/add-on-discovery"
drills:
  - autonomous-optimization
---

# Module Cross-Sell — Durable Intelligence

> **Stage:** Product → Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

An autonomous AI agent monitors cross-sell metrics daily, detects when performance plateaus or drops, generates hypotheses about what to change, runs A/B experiments on the top hypothesis, evaluates results, and auto-implements winners. The system finds the local maximum of cross-sell performance and maintains it. Weekly optimization briefs report what changed and why. Human intervention is only required for high-risk changes (budget >20%, targeting >50% of traffic, or agent-flagged high-risk hypotheses).

## Leading Indicators

- Autonomous optimization loop running daily without errors
- At least 1 experiment running at all times (unless converged)
- Weekly optimization briefs generated and posted to Slack
- No manual intervention required for standard optimization cycles
- Successive experiment wins shrinking in magnitude (approaching local maximum)

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill, scoped to the add-on discovery play. This is the core of Durable level. Configure each phase:

**Phase 1 — Monitor (daily via n8n cron):**
The agent checks the cross-sell play's primary KPIs daily:
- Add-on activation rate (per add-on and aggregate)
- Cross-sell revenue (daily MRR from add-on activations)
- Surface CTR (impression-to-click for each surface)
- ARPU lift (delta between cross-sold and non-cross-sold users)
- Dismissal rate (per add-on)

Compare the last 2 weeks against the 4-week rolling average. Classify each metric: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase). If anomaly detected, proceed to Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context specific to add-on discovery:
- Pull the current trigger thresholds, surface configurations, copy variants, and segment definitions from Attio
- Pull 8-week cross-sell funnel data from PostHog (per add-on, per surface, per segment)
- Run `hypothesis-generation` with the anomaly data and context

Typical hypotheses for add-on discovery:
- "Activation rate for Reporting Module dropped because the trigger threshold is too low — users are being prompted before they have enough context to evaluate the add-on. Raising the threshold from 5 views to 8 views will improve activation rate by 15%."
- "Banner CTR plateaued because users have become blind to the banner placement. Moving the surface to a tooltip at point-of-use will increase CTR by 20%."
- "Cross-sell revenue stalled because we are only showing add-ons to existing trigger segments. Adding a new trigger behavior (users who visit the pricing page 2+ times) will increase discovery volume by 30%."

Store hypotheses in Attio. If risk is "high," send Slack alert for human review and STOP. Otherwise proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent designs and launches the experiment:
- Create a PostHog feature flag splitting triggered users between control (current) and variant (hypothesis change)
- Implement the variant: if the hypothesis changes copy, update the Intercom message variant; if it changes timing, adjust the n8n workflow delay; if it changes triggers, create a new PostHog cohort
- Set duration: minimum 7 days or 100+ users per variant, whichever is longer
- Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent pulls experiment results from PostHog and runs `experiment-evaluation`:
- **Adopt**: Variant outperforms control with 95% confidence. Update the live configuration. Log the change.
- **Iterate**: Results inconclusive. Generate a refined hypothesis. Return to Phase 2.
- **Revert**: Variant underperforms. Restore control. Log the failure. Return to Phase 1 monitoring.
- **Extend**: Sample size insufficient. Keep running for another period.

**Phase 5 — Report (weekly via n8n cron):**
Generate a weekly optimization brief covering:
- Anomalies detected this week
- Experiments run and their outcomes
- Net metric change from adopted changes
- Current distance from estimated local maximum (estimated by diminishing returns curve)
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Extend health monitoring for autonomous mode

Run the `autonomous-optimization` drill with additional Durable-level panels:

Add to the existing dashboard:
- **Experiment timeline**: visual timeline showing all experiments, their duration, and outcome (adopt/revert/iterate)
- **Cumulative optimization lift**: total improvement in activation rate since Durable started
- **Convergence tracker**: magnitude of last 3 experiment wins — when all 3 are <2%, the play is converged
- **Agent activity log**: table of all autonomous actions taken (anomaly detections, hypotheses generated, experiments launched, decisions made)

Add alerts specific to autonomous operation:
- Alert if the optimization loop has not run in 48 hours (system failure)
- Alert if 3 consecutive experiments are reverted (strategy needs human review)
- Alert if a running experiment's primary metric drops >30% (auto-revert immediately)

### 3. Enforce guardrails

The autonomous optimization loop must respect these constraints:

- **Rate limit**: Maximum 1 active experiment per add-on at a time. Never stack experiments on the same add-on.
- **Revert threshold**: If any add-on's activation rate drops >30% during an experiment, auto-revert immediately.
- **Human approval required for**:
  - Changes affecting >50% of triggered users (major targeting changes)
  - New trigger behaviors that have not been manually validated
  - Surface types that have never been tested before (e.g., introducing modals)
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown**: After a failed experiment, wait 7 days before testing a new hypothesis on the same variable for the same add-on.
- **Monthly cap**: Maximum 4 experiments per add-on per month. If all 4 fail, pause optimization for that add-on and flag for human strategic review.
- **Never experiment on unmeasured changes**: If a hypothesis involves a metric without PostHog tracking, fix tracking first.

### 4. Monitor for convergence

The agent should detect convergence — when the play has reached its local maximum. Convergence criteria: the last 3 consecutive experiments on an add-on each produced less than 2% improvement.

When an add-on converges:
1. Report to the team: "Add-on discovery for [add-on name] is optimized. Current activation rate: [X%]. Current ARPU lift: [Y%]. Further gains require strategic changes (new add-on features, pricing changes, new user segments) rather than tactical surface optimization."
2. Reduce monitoring frequency for that add-on from daily to weekly
3. Continue monitoring for external changes (seasonal shifts, product updates, competitor moves) that might shift the local maximum
4. If performance degrades after convergence, re-enter the full optimization loop

### 5. Evaluate sustainability

This level runs continuously. Monthly review:
- Is total cross-sell revenue growing or stable?
- Is ARPU lift sustained at ≥5%?
- How many add-ons have converged?
- Are new add-ons being added to the catalog and entering the optimization pipeline?
- What is the total optimization ROI (revenue gained from adopted experiments minus cost of running the system)?

If cross-sell revenue declines for 2 consecutive months despite active optimization, escalate: the decline may be caused by product changes, market shifts, or pricing problems that surface optimization cannot fix.

## Time Estimate

- 8 hours: Configure autonomous optimization loop (connect the 5 phases to cross-sell-specific metrics and hypotheses)
- 4 hours: Extend monitoring dashboard with Durable-level panels
- 4 hours: Implement guardrails and convergence detection
- 4 hours: Test the full autonomous cycle end-to-end (trigger an anomaly, verify hypothesis generation, run a test experiment, verify evaluation)
- Ongoing: ~2 hours/week reviewing weekly briefs and approving high-risk changes

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, dashboards | Free up to 1M events/mo; $0.00031/event after — https://posthog.com/pricing |
| Anthropic (Claude) | Hypothesis generation, experiment evaluation, weekly briefs | API usage ~$10-50/mo depending on volume — https://www.anthropic.com/pricing |
| n8n | Optimization loop scheduling, alerts, report generation | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Intercom | Surface variant management for experiments | Included in existing plan — https://www.intercom.com/pricing |
| Loops | Email variant testing | Free up to 1,000 contacts; $49/mo for 5,000 — https://loops.so/pricing |
| Attio | Experiment logging, hypothesis tracking, campaign records | Included in existing plan — https://attio.com/pricing |

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor, diagnose, experiment, evaluate, report. This makes Durable fundamentally different from Scalable.
- `autonomous-optimization` — extended with experiment timeline, convergence tracking, and agent activity logging for autonomous oversight

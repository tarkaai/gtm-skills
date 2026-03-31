---
name: activation-milestone-tracking-durable
description: >
  Activation Milestone Tracking — Durable Intelligence. Autonomous AI agents
  continuously monitor milestone metrics, detect anomalies, generate improvement
  hypotheses, run A/B experiments, and auto-implement winners. Weekly optimization
  briefs track convergence toward the local maximum. Sustained ≥45% activation
  rate over 6 months with autonomous optimization.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving activation ≥45% over 6 months via autonomous AI optimization"
kpis: ["Activation rate (6-month trend)", "Per-milestone completion rate by segment", "Experiment velocity (experiments/month)", "Experiment win rate", "AI lift (cumulative improvement from autonomous changes)", "Convergence score"]
slug: "activation-milestone-tracking"
install: "npx gtm-skills add product/onboard/activation-milestone-tracking"
drills:
  - autonomous-optimization
---

# Activation Milestone Tracking — Durable Intelligence

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Activation rate sustains or improves above ≥45% for 6 consecutive months via autonomous AI optimization. The agent autonomously detects metric anomalies, generates improvement hypotheses, runs A/B experiments, evaluates results, and auto-implements winners. Weekly optimization briefs report on what changed, why, and the cumulative impact. The system converges when successive experiments produce <2% improvement for 3 consecutive experiments — at that point, the play has reached its local maximum.

## Leading Indicators

- Autonomous optimization loop is running: daily anomaly checks execute without failure
- At least 2 experiments complete per month (experiment velocity)
- >30% of experiments produce statistically significant improvements (win rate)
- Cumulative AI lift is positive and growing (total activation rate improvement attributable to autonomous changes)
- Weekly optimization briefs are generated and distributed on schedule
- No critical regression alerts sustained for more than 48 hours without an automated response

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on agent loop for activation milestones. Configure each phase:

**Phase 1 — Monitor (daily via n8n cron at 08:00 UTC):**
The agent queries PostHog for the play's primary KPIs:
- Overall activation rate (7-day rolling)
- Per-milestone completion rates
- Time-to-activation median
- Segment-level activation rates
- Stalled user counts per milestone

Compare the last 2 weeks against the 4-week rolling average. Classify:
- **Normal** (within ±10%): Log to Attio, no action.
- **Plateau** (±2% for 3+ weeks): The play is stagnating. Trigger Phase 2 — Diagnose.
- **Drop** (>20% decline in any metric): Something broke. Trigger Phase 2 — Diagnose with urgency flag.
- **Spike** (>50% increase): Investigate — is this a real improvement or a data anomaly? If confirmed, document the cause.

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context from Attio: current milestone flow configuration, active nudge sequences, recent experiment results, segment paths.
2. Pull 8-week metric history from PostHog, broken down by milestone and segment.
3. Run the `hypothesis-generation` fundamental with the anomaly data + context.
4. Receive 3 ranked hypotheses. Each hypothesis specifies: which milestone to change, what to change, predicted impact, and risk level.
5. Store hypotheses in Attio as notes on the play's campaign record.
6. If the top hypothesis has risk = "high": Send Slack alert for human review. STOP and wait for approval.
7. If risk = "low" or "medium": Proceed to Phase 3.

Example hypotheses the agent might generate:
- "Milestone 3 completion dropped 18% this week. Session recordings show users are confused by the new UI layout deployed on Monday. Hypothesis: Reverting the layout change will restore Milestone 3 completion to baseline. Risk: low."
- "Activation rate for paid-ads segment dropped 25% but organic is stable. Hypothesis: Landing page copy is creating expectations the product tour does not match. Test a revised product tour that mirrors the ad messaging. Risk: medium."
- "Overall activation rate has plateaued at 52% for 4 weeks. The biggest remaining drop-off is Milestone 2→3. Hypothesis: Adding an interactive sample project that auto-creates when users reach Milestone 2 will increase Milestone 3 completion by 8 points. Risk: medium."

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Take the top-ranked hypothesis.
2. Use PostHog feature flags to create an experiment: split traffic between control (current milestone flow) and variant (hypothesis change).
3. Implement the variant. Depending on the hypothesis:
   - Product tour changes: Update via Intercom API (use `intercom-product-tours` or `intercom-in-app-messages` fundamental).
   - Email sequence changes: Update via Loops API (use `loops-sequences` or `loops-transactional` fundamental).
   - UX changes: Deploy via PostHog feature flag in product code.
4. Set experiment duration: minimum 7 days OR 200+ users per variant, whichever is longer.
5. Log experiment start in Attio: hypothesis text, start date, expected duration, success metric, success criteria.

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog.
2. Run the `experiment-evaluation` fundamental with control vs. variant data.
3. Decision:
   - **Adopt:** Variant won with ≥95% confidence AND improved primary metric without degrading secondary metrics. Roll out variant to 100%. Log the change. Update the milestone flow configuration in Attio.
   - **Iterate:** Result was promising but not significant. Generate a refined hypothesis building on this result. Return to Phase 2.
   - **Revert:** Variant lost or caused harm. Disable variant, restore control. Log the failure. Return to Phase 1 monitoring.
   - **Extend:** Insufficient sample size. Keep running for another evaluation period.
4. Store the full evaluation in Attio: decision, confidence interval, primary metric lift, secondary metric impact, reasoning.

**Phase 5 — Report (weekly via n8n cron, Monday 09:00 UTC):**
1. Aggregate all optimization activity for the week: anomalies detected, hypotheses generated, experiments run, decisions made.
2. Calculate cumulative AI lift: total activation rate improvement from all adopted changes since Durable level started.
3. Generate a weekly optimization brief:

```
# Activation Milestone Optimization Brief — Week of [date]

## Summary
[1-2 sentences: what happened, net impact]

## Metrics
| Metric | Current | Last Week | Durable Start | AI Lift |
|--------|---------|-----------|---------------|---------|
| Activation rate | X% | Y% | Z% | +N pp |
| Milestone 2 completion | ... | ... | ... | ... |
| Milestone 3 completion | ... | ... | ... | ... |
| Time-to-activation | ... | ... | ... | ... |

## This Week's Activity
- Anomalies detected: [count and types]
- Hypotheses generated: [count]
- Experiments: [started/completed/adopted/reverted]
- Changes implemented: [list with expected impact]

## Convergence Status
- Consecutive experiments with <2% improvement: [N of 3]
- Estimated distance from local maximum: [assessment]
- Recommendation: [continue optimizing / reduce frequency / converged]

## Next Week Focus
[What the agent plans to test next, based on current data]
```

4. Post to Slack and store in Attio.

### 2. Deploy the activation health monitor

Run the `autonomous-optimization` drill to create the always-on monitoring layer that feeds signals into the autonomous optimization loop. This drill provides:

- A PostHog dashboard with 6 panels tracking per-milestone health
- A daily n8n workflow that checks milestone metrics and alerts on anomalies
- A weekly health brief with per-milestone and per-segment breakdown
- Trip-wire alerts for critical regressions (activation rate below threshold for 3 days, any milestone dropping below 50%, time-to-activation doubling)
- Structured signal data stored in Attio for the optimization loop to query

**Integration between the two drills:**
The activation health monitor's daily anomaly output feeds into the autonomous optimization loop's Phase 1. When the health monitor classifies a metric as "warning" or "critical," it triggers the optimization loop's Phase 2 (Diagnose). The health monitor's weekly brief provides context data for hypothesis generation. The health monitor's stall analysis tells the optimization loop which milestone to prioritize.

### 3. Configure guardrails

**These guardrails are critical and override all autonomous decisions:**

- **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments on different milestones simultaneously — interactions between changes make results uninterpretable.
- **Revert threshold:** If activation rate drops >30% at any point during an experiment, auto-revert immediately and alert the team.
- **Human approval required for:**
  - Changes affecting the core product UX (not just messaging or tour content)
  - Changes to milestone definitions themselves
  - Any change the hypothesis generator flags as "high risk"
  - Budget changes >20% (e.g., upgrading Intercom plan)
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same milestone.
- **Monthly experiment cap:** Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize unmeasured milestones:** If a milestone does not have complete PostHog tracking, fix tracking first before running experiments on it.

### 4. Evaluate sustainability

Pass criteria:

- **Sustained or improving activation ≥45% over 6 months via autonomous AI optimization.**

This level runs continuously. Monthly review checkpoints:
- Month 1-2: Is the optimization loop executing correctly? Are experiments producing data?
- Month 3-4: Is cumulative AI lift positive? Is experiment velocity sustained?
- Month 5-6: Is the system converging or still finding improvements?

**Convergence detection:** When 3 consecutive experiments produce <2% improvement, the play has reached its local maximum. At convergence:
1. Reduce monitoring frequency from daily to weekly.
2. Reduce experiment velocity from 2-3/month to 1/month (maintenance mode).
3. Report: "Activation milestone tracking has converged at [rate]%. Further gains require strategic changes (new milestone definitions, product changes, new user segments) rather than tactical optimization."

## Time Estimate

- 20 hours: Configure autonomous optimization loop (n8n workflows, PostHog setup, Attio integration)
- 10 hours: Deploy activation health monitor dashboard and alerting
- 10 hours: Configure guardrails and approval workflows
- 80 hours: Ongoing monitoring, experiment supervision, and brief review (over 6 months)
- 20 hours: Investigate and resolve anomalies flagged by the system
- 10 hours: Monthly review and strategic adjustment

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, experiments, funnels, dashboards, anomaly detection | Free up to 1M events + 1M feature flag requests/month; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages, product tours (experiment variants), contextual prompts | Advanced plan $85/seat/mo; Proactive Support Plus add-on $99/mo for campaigns ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Lifecycle emails, experiment variant emails, milestone nudges | Paid from $49/mo based on contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Optimization loop orchestration, daily/weekly cron workflows, alert routing | Community Edition free (self-hosted); Cloud Pro €60/mo for 10K executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation and experiment evaluation via Claude | Usage-based; ~$0.01-0.05 per optimization cycle ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Attio | Campaign records, experiment logging, signal storage, contact notes | Included in standard stack |

**Estimated monthly cost at this level:** $250-550/mo (Intercom Advanced + Proactive Support + Loops + n8n Cloud Pro + Anthropic API usage), plus PostHog usage if exceeding free tier.

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs
- `autonomous-optimization` — play-specific monitoring layer: per-milestone dashboards, daily anomaly checks, weekly health briefs, trip-wire alerts, signal data for the optimization loop

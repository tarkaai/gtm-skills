---
name: seat-expansion-triggers-durable
description: >
  Team Growth Upsell — Durable Intelligence. Autonomous AI agent continuously
  optimizes seat expansion: detects metric anomalies, generates hypotheses,
  runs A/B experiments, evaluates results, and auto-implements winners.
  Sustains >=40% expansion rate over 6 months.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving expansion >=40% over 6 months via autonomous optimization"
kpis: ["Seat expansion rate", "Experiment velocity", "AI lift (% improvement from auto-experiments)", "Revenue per prompt trend", "Time to local maximum"]
slug: "seat-expansion-triggers"
install: "npx gtm-skills add product/upsell/seat-expansion-triggers"
drills:
  - autonomous-optimization
---

# Team Growth Upsell — Durable Intelligence

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Hand the seat expansion play to an autonomous AI agent that continuously monitors, diagnoses, experiments, and optimizes. The agent runs the core loop: detect metric anomalies in expansion data, generate improvement hypotheses, design and run A/B experiments via PostHog, evaluate results, and auto-implement winners. The play converges to its local maximum — the best possible expansion rate given the current product, pricing, and market. Pass threshold: sustained or improving expansion rate >=40% over 6 months, with the agent running >=2 optimization experiments per month.

## Leading Indicators

- Autonomous optimization loop runs without manual intervention for 4+ consecutive weeks
- Agent detects a metric anomaly within 24 hours of it occurring
- First autonomous experiment launches within 2 weeks of Durable deployment
- At least one auto-implemented winner improves expansion rate by >=3% in the first month
- Weekly optimization briefs are generated on schedule and contain actionable insights

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the seat expansion play. This is the core of Durable — the drill that makes this level fundamentally different from Scalable.

**Phase 1 — Monitor (daily via n8n cron):**
Configure the daily monitoring workflow to check seat expansion KPIs:
- Primary KPI: expansion conversion rate (prompted accounts that add seats / total prompted)
- Secondary KPIs: prompt CTR by channel, seats added per conversion, revenue per prompt, signal detection accuracy
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
When the monitor detects an anomaly, the agent gathers context:
1. Pull current expansion configuration from Attio: active prompt variants, signal scoring weights, channel mix, tier thresholds
2. Pull 8-week expansion metric history from PostHog
3. Run hypothesis generation with Claude: provide the anomaly data + configuration + history
4. Receive 3 ranked hypotheses. Examples:
   - "Prompt fatigue: the modal prompt for team_invite_failed has been shown to the same accounts repeatedly. Predicted fix: rotate to banner format for repeat impressions."
   - "Signal weight miscalibration: admin_viewed_billing is triggering too many false positives. Predicted fix: increase the scoring threshold for warm tier from 20 to 25."
   - "Channel saturation: email follow-up sequence is underperforming because accounts already saw the in-app prompt. Predicted fix: delay the email to Day 3 instead of Day 0+2hrs."
5. Store hypotheses in Attio. If top hypothesis is high-risk (affects >50% of accounts), send Slack alert for human review and STOP. Otherwise proceed.

**Phase 3 — Experiment (auto-launched):**
Take the top hypothesis and design the experiment:
1. Create a PostHog feature flag splitting traffic between control (current config) and variant (hypothesis change)
2. Implement the variant: update Intercom message copy, Loops email template, n8n routing logic, or signal scoring weights as appropriate
3. Set experiment duration: minimum 7 days or 100+ accounts per variant, whichever is longer
4. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (auto-decided):**
When the experiment reaches its planned duration:
1. Pull results from PostHog experiments API
2. Run experiment evaluation with Claude: control vs variant metrics, statistical significance, secondary metric impact
3. Decision:
   - **Adopt:** Variant wins with >=95% confidence and no secondary metric degradation. Roll out to 100%. Log the change.
   - **Iterate:** Variant shows a directional improvement but not significant. Generate a refined hypothesis. Return to Phase 2.
   - **Revert:** Variant loses or degrades a secondary metric. Disable the variant. Log the failure. Return to Phase 1.
4. Store the full evaluation in Attio: decision, confidence interval, reasoning, metric impact

**Phase 5 — Report (weekly via n8n cron):**
Generate a weekly optimization brief:
- Anomalies detected this week
- Experiments running, completed, or started
- Net metric impact from all adopted changes
- Current expansion rate vs 6-month target
- Estimated distance from local maximum
- Recommended focus for next week

### 2. Deploy enhanced health monitoring

Run the `autonomous-optimization` drill with Durable-level extensions:

1. Add a "Durable Experiments" panel to the PostHog dashboard showing: active experiments, completed experiments this month, cumulative lift from adopted changes, experiment win rate
2. Add an "Autonomous Agent Activity" panel showing: anomalies detected, hypotheses generated, experiments launched, decisions made — all by week
3. Extend anomaly alerts to cover:
   - Agent inactivity: no experiments running for 3+ weeks → alert (agent may be stuck)
   - Convergence detection: 3 consecutive experiments produced <2% improvement → the play has likely reached its local maximum
   - Guardrail breach: any experiment causes >30% drop in primary KPI → auto-revert and alert

### 3. Configure guardrails

Set up the safety constraints that prevent the autonomous agent from causing harm:

- **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments on the expansion play.
- **Revert threshold:** If expansion rate drops >30% at any point during an experiment, auto-revert immediately and alert the team.
- **Human approval required for:**
  - Changes to signal scoring weights that would affect >50% of accounts
  - Changes to pricing display or seat pricing in prompt copy
  - Any hypothesis the agent flags as "high risk"
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same variable (e.g., do not test prompt copy again for 7 days if the last copy test failed).
- **Monthly experiment cap:** Maximum 4 experiments per month. If all 4 fail, pause autonomous optimization and flag for human strategic review.
- **Budget guardrail:** If Intercom or Loops costs increase >50% month-over-month due to increased prompt volume, alert before continuing.

### 4. Monitor for convergence

The autonomous optimization loop runs indefinitely, but it should detect when it has found the local maximum. Convergence criteria:

- 3 consecutive experiments produce <2% improvement in the primary KPI
- Expansion rate has been stable (+-5%) for 8+ weeks
- All major variables have been tested at least once (prompt copy, timing, format, channel mix, signal weights)

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency from continuous to monthly exploratory
3. Generate a convergence report: "Seat expansion play has reached its local maximum at {{rate}}% expansion rate, generating ${{mrr}}/mo in additional revenue. Further gains require strategic changes: new pricing tiers, product features that drive collaboration, or new channels."
4. The agent continues monitoring for external changes (product updates, market shifts, seasonal patterns) that could open new optimization opportunities

### 5. Evaluate sustainability

After 6 months, assess the Durable level:

- Was the >=40% expansion rate sustained across all 6 months?
- How many experiments did the agent run? How many were adopted?
- What is the cumulative AI lift (% improvement from auto-experiments vs the starting expansion rate)?
- Did the agent reach convergence? At what expansion rate?
- What is the total additional MRR generated by the expansion play over 6 months?

**Pass: Sustained or improving expansion rate >=40% over 6 months.** The play is durable. Continue running the autonomous loop at reduced frequency.

**Fail: Expansion rate decayed below 40% despite optimization.** Investigate whether the cause is external (market changes, product issues, competitor actions) or internal (prompt fatigue, signal quality degradation). The agent's experiment log provides the diagnostic data to determine the cause.

## Time Estimate

- 20 hours: configure the autonomous optimization loop (monitor, diagnose, experiment, evaluate, report phases)
- 10 hours: deploy enhanced health monitoring with Durable panels and alerts
- 5 hours: configure guardrails and safety constraints
- 15 hours: first month — monitoring agent activity, reviewing briefs, intervening on high-risk hypotheses
- 80 hours: months 2-5 — weekly brief review (2 hrs/week), quarterly guardrail review, responding to escalations
- 20 hours: month 6 — convergence analysis, sustainability evaluation, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, experiment platform, dashboards, anomaly detection | Free tier: 1M events/mo; paid: $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Workflow automation for the optimization loop and reporting | Self-hosted: free; Cloud: from EUR20/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | In-app expansion prompts (variants managed by the agent) | From $29/seat/mo; Proactive Support $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Expansion emails (variants managed by the agent) | $49/mo for 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic API | Claude for hypothesis generation, experiment evaluation, and weekly briefs | Pay-per-token ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Play-specific cost:** ~$150-500/mo (Intercom Proactive Support is primary; Anthropic API adds ~$10-50/mo depending on experiment frequency)

## Drills Referenced

- `autonomous-optimization` — the core always-on optimization loop: monitor anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs
- `autonomous-optimization` — monitor expansion funnel health with Durable extensions for experiment tracking and convergence detection

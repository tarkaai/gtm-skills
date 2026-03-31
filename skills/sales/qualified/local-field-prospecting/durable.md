---
name: local-field-prospecting-durable
description: >
  Local Field Prospecting — Durable. Always-on AI agents autonomously optimize territories,
  timing, pitch selection, and follow-up sequences. The autonomous-optimization drill runs
  the core detect-hypothesize-experiment-evaluate loop to find the local maximum of
  field prospecting performance.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Other"
level: "Durable"
time: "Ongoing — ~8 hours/week (4 founder, 4 agent)"
outcome: "Sustained or improving meetings and pipeline over 6 months; conversation-to-meeting rate converges to local maximum via autonomous experimentation"
kpis: ["Meetings booked per month", "Conversation-to-meeting rate", "Pipeline value per field hour", "Experiment win rate", "Convergence indicator (% improvement per experiment)"]
slug: "local-field-prospecting"
install: "npx gtm-skills add sales/qualified/local-field-prospecting"
drills:
  - autonomous-optimization
  - field-performance-reporting
  - field-territory-optimization
---

# Local Field Prospecting — Durable

> **Stage:** Sales > Qualified | **Motion:** OutboundFounderLed | **Channels:** Other (In-Person)

## Outcomes

The field prospecting play runs as a self-optimizing system. AI agents continuously monitor performance metrics, detect when conversion rates plateau or drop, generate hypotheses for improvement, design experiments, evaluate results, and auto-implement winners. The founder still executes the in-person visits, but every other aspect — territory selection, timing, venue prioritization, pre-visit intel, pitch variant selection, and follow-up sequencing — is autonomously optimized. The system converges toward the local maximum: the best possible field prospecting performance given the geographic market, ICP, and competitive landscape.

## Leading Indicators

- Experiment velocity: 2-4 experiments running per month
- Experiment win rate: what % of experiments produce measurable improvement
- Convergence rate: are successive experiments producing diminishing returns (<2% improvement = approaching local maximum)
- Anomaly detection response time: how quickly does the system detect and respond to metric changes
- Weekly optimization brief quality: are recommendations actionable and data-backed
- Territory refresh rate: how often new venues enter and underperformers exit the rotation

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured specifically for field prospecting. This is the drill that makes Durable fundamentally different from Scalable. Configure it as follows:

**Metrics to monitor (daily via n8n cron):**
- Conversation-to-meeting rate (primary KPI)
- Meetings booked per session
- Pipeline value per field hour
- Follow-up response rate
- Venue-level conversion rates

**Anomaly detection thresholds:**
- **Plateau**: Primary KPI within ±2% for 3+ consecutive weeks
- **Drop**: Primary KPI declines >15% vs. 4-week rolling average
- **Spike**: Primary KPI increases >30% (investigate what caused it and codify)
- **Normal**: Within ±10% of rolling average — no intervention needed

**Phase 1 — Monitor (daily):**
The n8n workflow pulls field prospecting events from PostHog daily. It compares the last 2 weeks against the 4-week rolling average for each monitored metric. If an anomaly is detected, it triggers Phase 2. If normal, it logs the check to Attio.

**Phase 2 — Diagnose (triggered by anomaly):**
When a metric anomaly fires, the agent:
1. Pulls 8 weeks of field prospecting data from PostHog
2. Gathers current configuration from Attio: active venues, visit schedule, pitch variants in use, follow-up sequences active
3. Runs the `hypothesis-generation` fundamental with anomaly data + context
4. Receives 3 ranked hypotheses. Examples for field prospecting:
   - "Conversation-to-meeting rate dropped because the founder has been visiting Venue X 3 weeks in a row and familiar faces are saturated. Hypothesis: rotate Venue X out for 4 weeks and add Venue Y."
   - "Follow-up response rate dropped 20%. Hypothesis: the winning email variant has decayed from overuse. Test a new variant with a different angle."
   - "Tuesday sessions outperform Thursday sessions by 40%. Hypothesis: shift one Thursday session to Tuesday."
5. If hypothesis risk is HIGH (e.g., changing the ICP or dropping a top venue), alert the founder for approval. If LOW/MEDIUM, proceed automatically.

**Phase 3 — Experiment (auto-initiated):**
Design and execute the experiment:
- Use PostHog feature flags to A/B test changes where possible (follow-up variants, email timing)
- For field changes (venue swaps, timing changes), run a 2-week controlled comparison: week 1 with old config, week 2 with new config, same founder effort
- Minimum experiment duration: 2 weeks or 10+ conversations per variant
- Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (auto-triggered at experiment end):**
Pull results and decide:
- **Adopt**: >= 10% improvement with statistical confidence. Update the live configuration. Log the win.
- **Iterate**: Results are directionally positive but inconclusive. Generate a refined hypothesis and re-test.
- **Revert**: No improvement or negative result. Restore previous config. Log the failure. Return to monitoring.
- **Extend**: Insufficient data. Run the experiment for another period.

**Phase 5 — Report (weekly):**
Generate a weekly optimization brief posted to Slack and stored in Attio:

```
## Field Prospecting Optimization Brief — Week of [Date]

### Anomalies Detected
- [Metric]: [description of anomaly]

### Experiments Active
- [Experiment name]: [status — running/completed/reverted]
- Hypothesis: [what we're testing]
- Preliminary results: [if available]

### Experiments Completed This Week
- [Experiment]: [ADOPT/REVERT/ITERATE] — [result summary]
- Net impact: [+/- X% on primary KPI]

### Current Performance
- Conversation-to-meeting rate: [X]% (4-wk avg: [Y]%)
- Meetings per month: [X] (target: [Y])
- Pipeline per field hour: $[X]
- Distance from estimated local maximum: [assessment]

### Recommended Focus
- [Specific recommendation for next week]
```

### 2. Configure field-specific performance reporting

Run the `field-performance-reporting` drill to set up automated weekly and monthly reports:

- Weekly report (Mondays at 8am): Activity summary, results, trends, top-performing venues, next week's plan
- Monthly deep-dive (1st of month): Venue performance rankings, territory ROI, cohort analysis (of meetings booked this month, how many converted to deals?), month-over-month trends
- Alerts: meeting rate drops below threshold, zero meetings in a week, deal won from field source

These reports feed into the autonomous optimization loop — the monthly report often surfaces patterns that the daily monitoring misses (seasonal trends, venue lifecycle effects).

### 3. Run continuous territory optimization

Run the `field-territory-optimization` drill on a monthly cadence:

- Refresh venue scores based on latest data
- Discover new venues in adjacent or underexplored areas matching top-performer profiles
- Detect venue fatigue: if a previously strong venue's conversion rate declines for 3+ weeks, flag it for rotation
- Expand geography strategically: when local venues plateau, test the next ring outward
- Track the "venue lifecycle" — new venues often spike, then normalize, then decay. The optimization loop manages this cycle by continuously refreshing the rotation.

### 4. Implement guardrails

**Critical guardrails for autonomous field optimization:**

- **Founder time cap**: Never recommend more than 4 field sessions per week (8 hours). Efficiency must improve, not raw hours.
- **Venue rotation minimum**: Never visit the same venue more than 2 times per month to prevent saturation and familiarity fatigue.
- **Human approval required for**:
  - Dropping a venue that has historically produced meetings (may be seasonal, not dead)
  - Changing the ICP targeting for field visits
  - Adding a new geography that requires >30 min drive time
  - Any experiment the hypothesis generator flags as "high risk"
- **Experiment limits**: Maximum 4 active experiments per month. If all 4 fail, pause optimization and flag for strategic review with the founder.
- **Revert threshold**: If meetings drop >40% during any experiment, auto-revert immediately.
- **Cooldown**: After a failed experiment, wait 2 weeks before testing the same variable.

### 5. Detect convergence

The optimization loop tracks convergence — when the play has reached its local maximum:

- If 3 consecutive experiments produce <2% improvement, the play is near-optimized
- At convergence:
  1. Reduce monitoring from daily to weekly
  2. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
  3. Generate a convergence report: "Field prospecting has reached its local maximum. Current performance: [metrics]. The play produces [X] meetings/month at [Y]% conversion with $[Z] pipeline per field hour. Further gains require strategic changes: new geography, new ICP segment, or channel expansion (adding pre-visit cold email, event-enhanced visits)."
  4. The agent continues monitoring for metric decay (market changes, venue closures, ICP drift) and re-activates the full optimization loop if performance drops.

## Time Estimate

- 4 hours/week: Agent — monitoring, optimization, experiment management, reporting (automated)
- 4 hours/week: Founder — 2 field sessions x 2 hours each (human action)
- Ongoing indefinitely. Agent effort decreases as the play converges.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Maps | Venue discovery, route optimization | Free tier or Starter $100/mo |
| Attio | CRM — full pipeline, notes, reporting | Plus at $29/user/mo |
| Cal.com | Meeting booking | Free tier (1 user) |
| PostHog | Analytics, experiments, feature flags | Free tier or paid at ~$0.00005/event |
| n8n | Automation — optimization loop, alerts, reporting | Pro at $60/mo (10K executions) |
| Clay | Venue enrichment, signal detection | Launch at $185/mo |
| Apollo | Contact sourcing | Free tier or Basic at $49/mo |
| Anthropic API | Hypothesis generation + evaluation (Claude) | ~$15-30/mo at optimization volume |

**Total Durable cost: $293-453/mo** (primary costs: Clay for enrichment, n8n for automation, Anthropic for AI reasoning)

## Drills Referenced

- `autonomous-optimization` — the core detect-hypothesize-experiment-evaluate-implement loop that finds the local maximum
- `field-performance-reporting` — automated weekly/monthly reports with alert thresholds
- `field-territory-optimization` — monthly venue scoring, territory expansion, and rotation management

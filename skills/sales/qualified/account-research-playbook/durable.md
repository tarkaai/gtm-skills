---
name: account-research-playbook-durable
description: >
  Account Research & Intelligence — Durable Intelligence. Deploy autonomous
  optimization agents that continuously learn which research signals predict
  conversions, auto-adjust signal weighting, run experiments on research
  depth and hook strategies, and converge on the local maximum of
  research-driven outreach performance.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving research effectiveness (>=35% reply rate, >=2.5x faster progression) over 6 months via autonomous signal optimization and experiment-driven improvement"
kpis: ["Reply rate trend", "Agent experiment win rate", "Signal prediction accuracy", "Research time efficiency"]
slug: "account-research-playbook"
install: "npx gtm-skills add sales/qualified/account-research-playbook"
drills:
  - autonomous-optimization
  - research-effectiveness-monitor
  - signal-detection
---

# Account Research & Intelligence — Durable Intelligence

> **Stage:** Sales > Qualified | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Deploy always-on AI agents that autonomously optimize every dimension of the account research pipeline. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in research effectiveness, generate hypotheses for improvement, design and run A/B experiments, evaluate results, and auto-implement winners. The `research-effectiveness-monitor` provides the signal-level telemetry that feeds the optimization loop. Over 6 months, the system converges on the local maximum — the best possible research approach for your market, ICP, and competitive landscape. Weekly optimization briefs report what changed and why. Convergence is declared when successive experiments produce <2% improvement.

## Leading Indicators

- Autonomous optimization loop running daily without intervention
- At least 1 experiment active at all times (2-3 experiments per month)
- Experiment win rate >=40% (at least 2 of every 5 experiments improve metrics)
- Signal weighting model accuracy improves month over month
- Research-to-meeting funnel tightens: fewer accounts researched, higher conversion rate
- Weekly optimization briefs contain specific, data-backed recommendations
- No metric drops >20% for more than 1 week without auto-correction

## Instructions

### 1. Deploy the research effectiveness monitor

Run the `research-effectiveness-monitor` drill. Build the monitoring layer that tracks which research signals and personalization hooks actually convert:

**Dashboard panels:**
- Reply rate by research depth (manual vs automated vs none) — 4-week rolling
- Reply rate by hook type (funding, exec hire, tech stack, news, hiring) — bar chart
- Meeting conversion funnel split by research quality
- Signal-to-meeting correlation table
- Research ROI: pipeline generated / (research time + tool costs)
- Research freshness: distribution of brief ages for accounts with active outreach

**Anomaly alerts:**
- Reply rate drops below 25% (vs 35% baseline) — immediate alert
- Any hook type drops below overall average for 2 consecutive weeks — signal decay alert
- Research-to-outreach gap >7 days — waste alert
- Enrichment failure rate >20% — data quality alert

**Weekly report:**
Automated n8n workflow generates a weekly effectiveness report with signal-level breakdown, ROI calculation, and recommended actions. Posts to Slack and stores in Attio.

### 2. Deploy autonomous optimization

Run the `autonomous-optimization` drill configured for this play. The optimization agent runs the five-phase loop:

**Phase 1 — Monitor (daily via n8n cron):**
- Pull this play's KPIs from PostHog: reply rate (overall and by signal type), meeting rate, signal prediction accuracy
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: current signal weighting model, active messaging frameworks, recent A/B test history, enrichment hit rates
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` via Anthropic API. Example hypotheses the agent might generate:
  - "Funding signals have become less predictive because the market shifted to a down round environment. Hypothesis: increase weight on hiring signals and tech stack signals."
  - "Reply rates dropped 15% this week. Cause: message fatigue on the 'congrats on Series B' template. Hypothesis: rotate to a problem-first opening instead of congratulatory."
  - "Tech stack hooks are converting 2x better than funding hooks this month. Hypothesis: prioritize enrichment credits on BuiltWith over Crunchbase."
- Rank hypotheses by expected impact and risk. Store in Attio.
- High-risk hypotheses (budget >20% change, audience >50% change) require human approval. **Human action required:** review and approve or reject in Attio.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Take the top hypothesis
- Design the experiment via PostHog feature flags: split outreach between control (current approach) and variant (hypothesis change)
- Implement the variant. Examples:
  - If testing signal weighting: adjust the priority score formula in Clay, route high-score accounts to different sequence
  - If testing messaging: create new email variants in Instantly with the hypothesized change
  - If testing research depth: split accounts into full-research and light-research pipelines
- Minimum duration: 7 days or 100+ sends per variant
- Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` via Anthropic API
- Decisions:
  - **Adopt**: Variant outperformed control. Update the live configuration. Log the change with reasoning.
  - **Iterate**: Promising direction but not conclusive. Generate a refined hypothesis and return to Phase 2.
  - **Revert**: Variant underperformed. Disable it, restore control. Log the failure reason.
  - **Extend**: Need more data. Keep running for another period.
- Store full evaluation (decision, confidence interval, reasoning) in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes this week
- Generate a weekly optimization brief via Anthropic API:
  - What changed and why
  - Net impact on reply rate, meeting rate, and signal prediction accuracy
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 3. Deploy adaptive signal weighting

Build a signal model that learns over time:

- Start with the signal weights validated at Scalable level
- Every time a researched account converts (reply, meeting, deal), log which signals were present and which hook was used
- Monthly: recalculate signal weights based on actual conversion data. Example:
  - If funding signals converted at 45% reply rate vs 30% overall, increase funding weight
  - If tech stack signals converted at 20% (below average), decrease tech stack weight
- The autonomous optimization agent can also propose weight changes via the experiment loop

Store the current signal model in Attio as a configuration record. The research automation pipeline reads it to calculate account priority scores.

### 4. Deploy predictive account intelligence

Build an n8n workflow that surfaces accounts entering buying mode before outreach begins:

- Monitor the target account universe (not just the active list) for signal spikes
- When a watched account crosses the priority threshold (e.g., funding + hiring + tech change within 30 days), auto-add it to the target list and trigger the research pipeline
- Alert: "High-intent account detected: {Company}. Signals: {list}. Recommended: outreach within 48 hours."

This shifts from reactive (account added to list > researched) to proactive (signals detected > account surfaced > researched > outreach).

### 5. Implement the convergence protocol

The optimization loop runs indefinitely but should detect when it has reached the local maximum:

- **Convergence criteria**: 3 consecutive experiments produce <2% improvement on the primary metric (reply rate)
- **At convergence**:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment cadence from 2-3/month to 1/month (maintenance mode)
  3. Generate a convergence report: "Account research play is optimized. Current performance: {metrics}. The signal model, messaging frameworks, and research depth are at their local maximum given the current market and ICP. Further gains require strategic changes: new ICP segments, new channels, or product changes."
  4. Continue monitoring for external disruptions (market shifts, competitor moves, ICP changes) that would require re-optimization

### Guardrails

- **Rate limit**: Maximum 1 active experiment at a time. Never stack experiments.
- **Revert threshold**: If reply rate drops >30% during any experiment, auto-revert immediately.
- **Human approval required for**: budget changes >20%, ICP targeting changes, channel additions/removals.
- **Cooldown**: After a failed experiment, wait 7 days before testing the same variable.
- **Maximum experiments per month**: 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize what is not measured**: Fix tracking gaps before running experiments.

## Time Estimate

- Research effectiveness monitor setup: 8 hours
- Autonomous optimization configuration: 12 hours
- Adaptive signal weighting: 6 hours
- Predictive account intelligence: 8 hours
- Monitoring and review (weekly, 1.5h x 24 weeks): 36 hours
- Experiment review and approval (monthly, 2h x 6 months): 12 hours
- Monthly signal model recalibration: 12 hours
- Convergence evaluation and documentation: 6 hours
- **Total: ~130 hours over 6 months** (mostly weekly monitoring and monthly calibration)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Enrichment, signal monitoring, tech stack, continuous refresh | Growth: $495/month for 40,000 actions ([clay.com/pricing](https://www.clay.com/pricing)) |
| Instantly | Email sequencing, A/B variant management | Hypergrowth: $97/month ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Anthropic API | Brief generation, hypothesis generation, experiment evaluation, weekly reports | ~$15-25/month at scale ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Attio | CRM — signal model storage, experiment logging, deal tracking | Plus: $34/user/month ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Event tracking, experiments, anomaly detection, dashboards | Free tier or Growth: from $0 ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop workflows, signal monitoring, reporting | Starter: $24/month or self-hosted free ([n8n.io/pricing](https://n8n.io/pricing)) |
| LinkedIn Sales Navigator | Signal monitoring, contact verification | Core: $99.99/month ([linkedin.com/sales](https://business.linkedin.com/sales-solutions/compare-plans)) |

**Estimated play-specific cost: ~$650-775/month** (Clay Growth + Instantly Hypergrowth + LinkedIn Sales Nav + Anthropic API)

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: monitor metrics, generate hypotheses, run A/B experiments, evaluate results, auto-implement winners, generate weekly briefs
- `research-effectiveness-monitor` — signal-level telemetry tracking which research inputs drive replies and meetings
- `signal-detection` — real-time buying signal monitoring that triggers research refreshes and surfaces high-intent accounts proactively

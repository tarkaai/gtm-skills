---
name: outbound-email-li-calls-durable
description: >
  Outbound Email/LI/Calls — Durable Intelligence. Always-on AI agents monitor
  multi-channel outbound performance, detect anomalies, generate improvement
  hypotheses, run A/B experiments, and auto-implement winners. The autonomous
  optimization loop finds the local maximum for meeting rate, cost per meeting,
  and channel allocation. Weekly optimization briefs. Converges when successive
  experiments produce <2% improvement.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving meeting rate ≥ 1.6% over 6 months with declining cost per meeting, maintained by autonomous agent-driven optimization"
kpis: ["Meeting rate", "Cost per meeting", "Experiment win rate", "Time to convergence"]
slug: "outbound-email-li-calls"
install: "npx gtm-skills add marketing/solution-aware/outbound-email-li-calls"
drills:
  - autonomous-optimization
  - signal-detection
---

# Outbound Email/LI/Calls — Durable Intelligence

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Outcomes

Durable is autonomous optimization. AI agents run the play continuously, finding the local maximum for meeting rate and cost per meeting across email, LinkedIn, and calls. The `autonomous-optimization` drill creates the always-on loop: detect metric anomalies -> generate improvement hypotheses -> run A/B experiments -> evaluate results -> auto-implement winners. The play sustains or improves meeting rate ≥ 1.6% over 6 months while cost per meeting trends downward. Converges when successive experiments produce <2% improvement for 3 consecutive experiments.

## Leading Indicators

- Anomaly detection firing within 24 hours of metric shifts
- Hypotheses generated and ranked within 1 hour of anomaly detection
- Experiments launching within 48 hours of hypothesis acceptance
- At least 2 winning experiments adopted per month in months 1-3
- Cost per meeting declining month-over-month
- Weekly optimization briefs delivered every Monday with actionable findings
- Channel allocation shifting toward highest-performing channels automatically
- Message variant rotation preventing fatigue (no variant used for more than 4 weeks)

## Instructions

### 1. Deploy the outbound performance monitoring system

Run the `autonomous-optimization` drill. This builds:

1. **PostHog dashboard** — "Outbound Email/LI/Calls — Performance" with panels for volume by channel, per-channel conversion funnels, cross-channel attribution, health metrics (deliverability, acceptance rate, connect rate), and pipeline impact.
2. **Anomaly detection** — alerts for: email reply rate drops below 2% for 5 days, LinkedIn acceptance below 20% for 1 week, call connect rate below 10% for 1 week, meeting volume drops to zero for 5 days, negative reply rate exceeds 5%, email bounce rate exceeds 3%.
3. **Weekly automated briefs** — n8n workflow that pulls PostHog + Attio data every Monday 8am, generates channel-by-channel metrics summary with week-over-week deltas, best-performing variants and segments, and recommended actions.
4. **Monthly trend reports** — cost per meeting by channel, pipeline velocity, ROI, and strategic channel allocation recommendations.

All data stored as structured PostHog events so the autonomous optimization loop can consume it.

### 2. Deploy autonomous optimization

Run the `autonomous-optimization` drill. Configure the 5-phase loop for this specific play:

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` fundamental to check: meeting rate, reply rate (email), acceptance rate (LinkedIn), connect rate (calls), cost per meeting
2. Compare last 2 weeks against 4-week rolling average
3. Classify: normal (±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
4. If normal → log, no action. If anomaly → trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context from Attio: current targeting criteria, active message variants per channel, cadence timing, channel allocation, prospect volume
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` fundamental with anomaly data + context
4. Receive 3 ranked hypotheses. Examples of hypotheses the agent may generate:
   - "Email reply rate dropped because subject line variant B has been running 6 weeks and is fatigued. Hypothesis: rotating to a new subject line will recover reply rate by 2+ percentage points."
   - "LinkedIn acceptance rate dropped because connection notes reference a competitor that just raised funding, making prospects defensive. Hypothesis: switching to a product-category reference instead of competitor name will improve acceptance by 5+ points."
   - "Call connect rate dropped because call times shifted to afternoon. Hypothesis: returning to 8-9am call blocks will restore 15%+ connect rate."
5. Store hypotheses in Attio as campaign notes.
6. If top hypothesis is high-risk → Slack alert for human review and STOP.
7. If low/medium-risk → proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using `posthog-experiments` fundamental: feature flag splitting traffic between control (current) and variant (hypothesis change)
2. Implement the variant:
   - For email changes: create B variant in Instantly using `instantly-campaign` fundamental
   - For LinkedIn changes: create B variant in Dripify/Expandi using `linkedin-automation-sequence` fundamental
   - For call changes: update call priority queue or script in Attio
   - For timing/cadence changes: update n8n workflow schedule
   - For targeting changes: adjust Clay scoring model and list filters
3. Set experiment duration: minimum 7 days or until 100+ prospects per variant, whichever is longer
4. Log experiment in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull results from PostHog experiment
2. Run `experiment-evaluation` fundamental with control vs variant data
3. Decision:
   - **Adopt**: Update live configuration to use winner. Log the change. Example: winning email subject line becomes the new default in Instantly.
   - **Iterate**: Generate a new hypothesis building on this result. Return to Phase 2.
   - **Revert**: Disable variant, restore control. Log failure. Return to Phase 1.
   - **Extend**: Keep running — insufficient data. Set reminder for re-evaluation.
4. Store full evaluation in Attio (decision, confidence, reasoning, metric impact)

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on meeting rate and cost per meeting
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 3. Deploy signal-based prospecting refresh

Run the `signal-detection` drill to keep the prospect pipeline fresh:

1. Configure Clay tables with automated daily enrichment: monitor for job changes at target accounts (new VP/C-level = budget unlocked), funding events in last 90 days (new money, new priorities), hiring signals (3+ roles in your domain = building a team), technology signals (adopted/dropped competitor tool).
2. Score signals by recency (last 30 days strongest) and intensity (multiple signals from one account).
3. Route high-score signals directly into the outbound cadence queue in Attio. Medium-score signals go to a watch list.
4. The autonomous optimization loop monitors signal-to-meeting rate and adjusts signal thresholds weekly. If a signal type produces below-average meeting rates, reduce its priority. If a new signal type emerges (e.g., layoffs at competitor create displacement opportunities), add it.

### 4. Configure guardrails

**These guardrails are non-negotiable and override any optimization decision:**

- **Rate limit**: Maximum 1 active experiment per channel at a time. Never stack experiments.
- **Revert threshold**: If meeting rate drops >30% at any point during an experiment, auto-revert immediately.
- **Human approval required for**: budget changes >20%, audience/targeting changes affecting >50% of prospects, any change the hypothesis generator flags as high-risk, adding or removing an entire channel from the cadence.
- **Cooldown**: After a failed experiment, wait 7 days before testing a new hypothesis on the same variable.
- **Max experiments per month**: 4 per channel (12 total across email, LinkedIn, calls). If all experiments on a channel fail, pause optimization on that channel and flag for human strategic review.
- **Deliverability protection**: If email bounce rate exceeds 5% or LinkedIn sends an account warning, pause all automation on that channel immediately. Do not resume until the issue is resolved manually.
- **Volume caps**: Never exceed sending limits set in Scalable. Optimization improves conversion, not volume.

### 5. Monitor convergence

The optimization loop runs indefinitely. However, the agent detects **convergence** — when successive experiments produce diminishing returns:

- Track improvement magnitude per experiment over time
- If 3 consecutive experiments across all channels produce <2% improvement each, the play has reached its local maximum
- At convergence: reduce monitoring frequency from daily to weekly, reduce experiment cadence from weekly to monthly
- Generate a convergence report: "This play is optimized at [current meeting rate] with [current cost per meeting]. Further gains require strategic changes (new channels, new ICP segments, product changes) rather than tactical optimization."

**Human action required:** Review the convergence report. Decide whether to maintain current performance, expand to new ICP segments, or reallocate budget to other plays.

## Time Estimate

- Outbound performance monitor setup: 8 hours
- Autonomous optimization loop configuration: 12 hours
- Signal detection setup: 6 hours
- Guardrail configuration: 4 hours
- Ongoing call block execution (reduced with signal prioritization): 80 hours (2 hrs/day, 2-3 days/week)
- Weekly monitoring and brief review: 40 hours (1.5 hrs/week over 6 months)
- Monthly strategic review: 12 hours (2 hrs/month)
- Experiment design and implementation: 20 hours
- Convergence review and adjustment: 8 hours
- Buffer for manual interventions: 10 hours

Total: ~200 hours over 6 months.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Cold email at scale | Hypergrowth: $77.6/mo (https://instantly.ai/pricing) |
| Clay | Enrichment + signal detection + AI personalization | Team: $349/mo (https://www.clay.com/pricing) |
| Apollo | Contact sourcing | Professional: $99/mo (https://www.apollo.io/pricing) |
| Dripify / Expandi | LinkedIn automation | Dripify: $59/mo; Expandi: $99/mo (https://dripify.io/pricing / https://expandi.io/pricing) |
| Aircall / JustCall | Cloud dialer | Aircall: $30/user/mo; JustCall: $19/user/mo (https://aircall.io/pricing / https://justcall.io/pricing) |
| LinkedIn Sales Navigator | Prospecting | Core: $99.99/mo (https://business.linkedin.com/sales-solutions) |
| n8n | Orchestration + optimization workflows | Starter: $20/mo (https://n8n.io/pricing) |
| Attio | CRM + optimization audit trail | Plus: $29/user/mo (https://attio.com/pricing) |
| PostHog | Analytics + experiments + anomaly detection | Teams: $0 first 1M events/mo (https://posthog.com/pricing) |
| Anthropic API | Claude for hypothesis generation + evaluation | ~$50-150/mo at optimization frequency (https://www.anthropic.com/pricing) |
| Cal.com | Meeting booking | Free tier (https://cal.com/pricing) |

**Estimated play-specific cost: ~$560-1,000/mo** (Instantly + Clay + Apollo + LinkedIn automation + dialer + Sales Nav + Anthropic)

## Drills Referenced

- `autonomous-optimization` — the core monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum for meeting rate and cost per meeting
- `autonomous-optimization` — always-on dashboards, weekly briefs, monthly trend reports, and anomaly detection across email, LinkedIn, and calls
- `signal-detection` — continuous buying signal monitoring to keep the prospect pipeline fresh and prioritized

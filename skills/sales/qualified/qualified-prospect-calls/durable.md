---
name: qualified-prospect-calls-durable
description: >
  Founder calls to prospects — Durable Intelligence. Always-on AI agents monitor call
  performance, detect anomalies, generate improvement hypotheses, run A/B experiments,
  evaluate results, and auto-implement winners. The autonomous-optimization loop finds
  the local maximum of meeting rate and sustains it as market conditions shift. Weekly
  optimization briefs. Convergence detection when experiments yield <2% improvement.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Meeting rate sustained at or above 1.6% (Scalable baseline) for 6 months; never drops >20% below baseline for 2+ consecutive weeks"
kpis: ["Meeting rate (weekly)", "Connect rate (weekly)", "Cost per meeting (monthly)", "Pipeline value from play (monthly)", "Experiment win rate", "Weeks since last metric drop >20%"]
slug: "qualified-prospect-calls"
install: "npx gtm-skills add sales/qualified/qualified-prospect-calls"
drills:
  - autonomous-optimization
  - call-performance-reporting
  - signal-detection
---

# Founder Calls to Prospects — Durable Intelligence

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Outcomes

Sustain or improve the meeting rate established at Scalable level (>= 1.6%) over 6 continuous months. The play never drops more than 20% below the Scalable baseline for 2 or more consecutive weeks. AI agents autonomously detect degradation, diagnose root causes, run experiments, and implement improvements without human intervention (except for high-risk changes that require founder approval).

The play converges when 3 consecutive experiments yield less than 2% improvement — indicating the local maximum has been found. At convergence, monitoring frequency drops from daily to weekly.

## Leading Indicators

- Anomaly detection fires within 24 hours of any KPI deviation exceeding 10%
- The autonomous optimization loop runs at least 2 experiments per month
- Experiment win rate is above 30% (at least 1 in 3 experiments improves performance)
- Weekly optimization briefs are generated on schedule with actionable recommendations
- Signal detection identifies at least 2 new high-performing signal types per quarter
- Founder call time per meeting continues to trend down (or stays flat at optimum)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to configure the core Monitor -> Diagnose -> Experiment -> Evaluate -> Report cycle for this play:

**Phase 1 — Monitor (daily via n8n cron):**
Configure the n8n workflow to check these play-specific KPIs daily via PostHog:
- Meeting rate (weekly rolling): compare last 7 days vs 4-week rolling average
- Connect rate (weekly rolling): same comparison
- Email reply rate (weekly rolling): same comparison
- Cost per meeting (weekly): tool spend / meetings booked
- Signal-to-meeting conversion by signal type

Classification thresholds for this play:
- **Normal**: metric within +/- 10% of 4-week average
- **Plateau**: metric varies less than +/- 2% for 3+ consecutive weeks
- **Drop**: metric declines > 20% from 4-week average
- **Spike**: metric increases > 50% from 4-week average

If normal: log to Attio, no action. If anomaly detected: trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
When an anomaly fires, the agent gathers context:
- Pull current play configuration from Attio: active email sequences, call script version, signal definitions, tier thresholds, active prospect volume
- Pull 8-week metric history from PostHog
- Run hypothesis generation (Claude API) with the anomaly data + context

For this play, common hypothesis categories:
- **Message fatigue**: email subject lines or call openers that have been running too long (> 6 weeks) lose effectiveness. Hypothesis: rotate messaging.
- **Signal decay**: a signal type that used to predict meetings no longer does (e.g., a competitor stopped being relevant). Hypothesis: deprecate signal, add new one.
- **Timing drift**: optimal call windows have shifted due to seasonal changes or remote work patterns. Hypothesis: test new time slots.
- **ICP drift**: the market has moved — new buyer personas or company sizes are emerging. Hypothesis: expand or narrow ICP.
- **Channel saturation**: prospects in this ICP are getting too much outreach from other companies. Hypothesis: change the channel mix or outreach angle.

The agent generates 3 ranked hypotheses with expected impact and risk level. High-risk hypotheses (budget changes > 20%, audience changes affecting > 50% of traffic) require founder approval via Slack. Low/medium risk proceed automatically.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Take the top hypothesis. Use PostHog experiments to split traffic:
- Create a feature flag that routes prospects to control (current approach) vs variant (hypothesis change)
- Implement the variant using the appropriate channel: Instantly for email changes, n8n cadence timing for call window changes, Clay scoring for signal changes
- Minimum experiment duration: 7 days or 100 prospects per variant, whichever is longer
- Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Play-specific experiment types:**
- **Call script A/B**: Agent writes a variant opener or problem statement. Founder uses it for half of Tier 1 calls. Agent compares meeting rates.
- **Email sequence A/B**: New subject line, body copy, or CTA. Split in Instantly.
- **Signal weight adjustment**: Change scoring weights for specific signals. Compare meeting rate for prospects scored under old vs new model.
- **Tier threshold adjustment**: Change the score cutoff between Tier 1/2/3. Compare meeting rates per tier.
- **Cadence timing**: Shift the call day from Day 3 to Day 5, or change email send times.

**Phase 4 — Evaluate (triggered by experiment completion):**
Pull experiment results from PostHog. Run evaluation:
- **Adopt**: Variant outperforms control with 95% confidence. Update live configuration. Log the change.
- **Iterate**: Results are promising but not conclusive. Generate a refined hypothesis and re-test.
- **Revert**: Variant underperforms. Disable variant, restore control. Log the failure. 7-day cooldown before testing the same variable.
- **Extend**: Insufficient sample size. Keep running for another period.

**Phase 5 — Report (weekly via n8n cron, Mondays 8am):**
Generate the weekly optimization brief covering:
- Anomalies detected this week and actions taken
- Active experiments: status, preliminary results, expected completion
- Completed experiments: decisions, net impact on KPIs
- Current KPI values vs Scalable baseline vs all-time best
- Distance from estimated local maximum (calculated from recent experiment magnitude)
- Recommended focus for next week
Post to Slack, store in Attio.

### 2. Configure play-specific performance monitoring

Run the `call-performance-reporting` drill to build the reporting layer specific to phone-based outreach:

- **Live PostHog dashboard**: weekly call volume, connect rate trend, meeting conversion trend, best call windows heatmap, signal effectiveness breakdown, pipeline value from calls, average call duration
- **Anomaly alerts**: connect rate < 15% for 3 days, meeting conversion < 5% for 1 week, call volume < 50% of average, call duration < 60 seconds
- **Weekly call quality report** (n8n, Mondays 8am): extract common objections from Fireflies transcripts, identify objection pattern shifts, recommend call script adjustments
- **Monthly trend report** (1st of month): month-over-month KPI trends, cost per meeting evolution, ICP segment performance, recommendations for segment additions/retirements

These reports feed directly into the autonomous optimization loop as input data for hypothesis generation.

### 3. Evolve signal detection continuously

Run the `signal-detection` drill in continuous mode:

- Monthly: analyze which signal types produced the highest meeting rates over the past 30 days. Deprecate signals that fell below 1% meeting rate. The agent searches for new signal sources by:
  - Analyzing Fireflies call transcripts for mentions of triggering events that prospects reference ("we just started looking because...")
  - Checking which Clay enrichment fields correlate most strongly with meeting outcomes
  - Reviewing won deals in Attio for common attributes not currently tracked as signals

- Quarterly: run a full signal audit. Compare signal-to-meeting rates across all 6 months. Publish a signal effectiveness report. Retire the bottom 20% of signals and test 2-3 new candidates.

### 4. Apply guardrails

The `autonomous-optimization` drill includes standard guardrails. For this play, add these play-specific guardrails:

- **Founder time cap**: never schedule more than 15 Tier 1 calls per week. If the optimization loop wants to test more calls, it must make the existing calls more effective, not add more.
- **Email volume cap**: never exceed 100 emails/day across all sending accounts. Domain reputation is irreplaceable.
- **Negative reply threshold**: if negative reply rate exceeds 5% on any active email sequence, auto-pause that sequence and alert the agent to rewrite.
- **Prospect fatigue**: never contact a prospect through more than 3 channels in a single week. If email + LinkedIn + call all happen, the next touch must wait 7 days.
- **Budget ceiling**: total monthly tool spend for this play must not exceed $800. If the optimization loop recommends higher spend (e.g., more Clay credits), it must be approved by the founder.

### 5. Handle convergence

When 3 consecutive experiments produce < 2% improvement:

1. The play has reached its local maximum for the current market conditions
2. Reduce monitoring from daily to weekly
3. Reduce experiment frequency to 1 per month (maintenance mode)
4. Generate a convergence report: current performance metrics, total improvement from Scalable baseline, experiment history summary, and recommendations for step-change improvements (new channels, new ICP segments, product changes) that require strategic decisions beyond tactical optimization
5. Post convergence report to Slack and store in Attio

If market conditions change (new competitor enters, major industry shift, product pivot), reset convergence and return to daily monitoring with active experimentation.

## Time Estimate

- Autonomous optimization setup: 8 hours (agent)
- Call performance reporting setup: 4 hours (agent)
- Signal detection continuous mode: 2 hours/month x 6 = 12 hours (agent)
- Weekly monitoring + brief review: 1 hour/week x 24 = 24 hours (agent)
- Monthly report review + strategic decisions: 2 hours/month x 6 = 12 hours (human)
- Experiment implementation + evaluation: 4 hours/month x 6 = 24 hours (agent)
- Founder call execution: 1.5 hours/week x 24 = 36 hours (human)
- Guardrail tuning + convergence handling: 4 hours (agent)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM, deal tracking, experiment logging | Pro: $29/user/mo (https://attio.com/pricing) |
| Clay | Enrichment + signal detection + continuous list refresh | Pro: $349/mo (https://clay.com/pricing) |
| Instantly | Email sequencing + A/B testing (3+ accounts) | Hypergrowth: $77.6/mo (https://instantly.ai/pricing) |
| Cal.com | Meeting booking | Team: $12/user/mo (https://cal.com/pricing) |
| PostHog | Analytics + experiments + anomaly detection | Free tier or Scale (https://posthog.com/pricing) |
| n8n | Automation (optimization loop + sync + reporting) | Starter: $24/mo (https://n8n.io/pricing) |
| Fireflies | Call transcription + objection analysis | Pro: $18/seat/mo (https://fireflies.ai/pricing) |
| Claude API | Hypothesis generation + experiment evaluation | ~$15-30/mo at this usage (https://anthropic.com/pricing) |
| LinkedIn Sales Navigator | Prospecting | Core: $99/mo (https://business.linkedin.com/sales-solutions/compare-plans) |

**Estimated play-specific cost at this level:** $450-800/mo

## Drills Referenced

- `autonomous-optimization` — the core monitor -> diagnose -> experiment -> evaluate -> report loop that finds and sustains the local maximum
- `call-performance-reporting` — play-specific dashboards, weekly call quality reports, monthly trends, and anomaly alerts for phone outreach
- `signal-detection` — continuous discovery and deprecation of buying signals that drive call targeting

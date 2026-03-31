---
name: outbound-sms-text-durable
description: >
  SMS Outbound Sequences — Durable Intelligence. Always-on AI agents monitor
  SMS outbound performance, detect anomalies, generate improvement hypotheses,
  run A/B experiments, and auto-implement winners. The autonomous optimization
  loop finds the local maximum for response rate and cost per meeting. Weekly
  optimization briefs. Converges when successive experiments produce <2%
  improvement.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving response rate ≥3% over 6 months with declining cost per meeting, maintained by autonomous agent-driven optimization"
kpis: ["Response rate", "Cost per meeting", "Experiment win rate", "Time to convergence", "Opt-out rate trend"]
slug: "outbound-sms-text"
install: "npx gtm-skills add marketing/solution-aware/outbound-sms-text"
drills:
  - autonomous-optimization
  - signal-detection
---

# SMS Outbound Sequences — Durable Intelligence

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Durable is autonomous optimization. AI agents run the SMS play continuously, finding the local maximum for response rate and cost per meeting. The `autonomous-optimization` drill creates the always-on loop: detect metric anomalies -> generate improvement hypotheses -> run A/B experiments -> evaluate results -> auto-implement winners. The play sustains or improves response rate >=3% over 6 months while cost per meeting trends downward. Converges when successive experiments produce <2% improvement for 3 consecutive experiments.

## Leading Indicators

- Anomaly detection firing within 24 hours of metric shifts
- Hypotheses generated and ranked within 1 hour of anomaly detection
- Experiments launching within 48 hours of hypothesis acceptance
- At least 2 winning experiments adopted per month in months 1-3
- Cost per meeting from SMS declining month-over-month
- Weekly optimization briefs delivered every Monday with actionable findings
- Message variant rotation preventing fatigue (no variant used for more than 3 weeks)
- Opt-out rate stable or declining (validates that optimization improves quality, not just volume)
- Signal-to-meeting rate improving as signal thresholds are tuned

## Instructions

### 1. Deploy the SMS performance monitoring system

Run the `autonomous-optimization` drill. This builds:

1. **PostHog dashboard** — "SMS Outbound — Performance" with panels for: daily send volume, delivery rate trend, response funnel (sent -> delivered -> replied -> meeting_booked), reply sentiment breakdown, opt-out rate trend, cost per reply, and cost per meeting.

2. **Anomaly detection** — alerts for:
   - Delivery rate drops below 90% for 2 consecutive days
   - Response rate drops below 1% for 5 consecutive days (at 40+ daily sends)
   - Opt-out rate exceeds 5% of sends in any single day
   - Zero replies for 3 consecutive business days
   - Failed message rate exceeds 10% in any single day
   - Negative sentiment replies exceed 40% of all replies in a week

3. **Weekly automated briefs** — n8n workflow that pulls PostHog + Attio data every Monday 8am:
   - Volume: messages sent, delivered, replied
   - Response rate with week-over-week delta
   - Best-performing message variant and ICP segment
   - Opt-out rate trend
   - Meetings booked and pipeline value
   - Recommended actions for next week

4. **Monthly trend reports** — cost per meeting trend, response rate by ICP segment, message fatigue indicators, and comparison against other outbound channels.

All data stored as structured PostHog events so the autonomous optimization loop can consume it.

### 2. Deploy autonomous optimization

Run the `autonomous-optimization` drill. Configure the 5-phase loop for SMS outbound:

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` fundamental to check: response rate, delivery rate, opt-out rate, cost per meeting, positive reply ratio
2. Compare last 2 weeks against 4-week rolling average
3. Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
4. If normal -> log, no action. If anomaly -> trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context from Attio: current prospect segments, active message variants, sequence timing, send volume, recent list sources
2. Pull 8-week SMS metric history from PostHog
3. Run `hypothesis-generation` fundamental with anomaly data + context
4. Receive 3 ranked hypotheses. Examples of hypotheses the agent may generate:
   - "Response rate dropped because Message 1 variant has been running 4 weeks and prospects in this industry segment have seen it. Hypothesis: rotating to a new opener referencing a different pain point will recover response rate by 2+ points."
   - "Delivery rate dropped because Twilio number X is being carrier-filtered. Hypothesis: rotating to a fresh number and varying message content will restore >95% delivery."
   - "Opt-out rate spiked because the latest list batch included contacts from an adjacent ICP segment with poor fit. Hypothesis: tightening the Clay scoring threshold from 65 to 75 will reduce opt-outs by 50%."
   - "Response rate plateaued because send time is 9am for all prospects. Hypothesis: sending at 11am for West Coast and 9am for East Coast will lift response rate by 1-2 points."
5. Store hypotheses in Attio as campaign notes.
6. If top hypothesis is high-risk (affects >50% of send volume or touches compliance) -> Slack alert for human review and STOP.
7. If low/medium-risk -> proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using `posthog-experiments` fundamental: feature flag splitting prospects between control (current) and variant (hypothesis change)
2. Implement the variant:
   - For copy changes: generate new message variants via the sms copy generation workflow (see instructions below) drill and assign to the variant group
   - For timing changes: update n8n cron schedule for the variant group
   - For targeting changes: adjust Clay scoring thresholds or ICP filters for the variant group
   - For sequence changes: modify step timing (Day 1/3/6 vs Day 1/2/5) for the variant group
   - For number changes: assign variant group to a different Twilio phone number
3. Set experiment duration: minimum 7 days or until 100+ prospects per variant, whichever is longer
4. Log experiment in Attio: hypothesis, start date, expected duration, success criteria, variant description

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull results from PostHog experiment
2. Run `experiment-evaluation` fundamental with control vs variant data
3. Decision:
   - **Adopt**: Update live configuration to use winner. Log the change. Example: winning opener becomes the new default in the n8n SMS workflow.
   - **Iterate**: Generate a new hypothesis building on this result. Return to Phase 2.
   - **Revert**: Disable variant, restore control. Log failure. Return to Phase 1.
   - **Extend**: Keep running — insufficient data. Set reminder for re-evaluation in 7 days.
4. Store full evaluation in Attio: decision, confidence interval, reasoning, metric impact

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on response rate and cost per meeting
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 3. Deploy signal-based prospecting refresh

Run the `signal-detection` drill to keep the SMS prospect pipeline fresh:

1. Configure Clay tables with automated daily enrichment: monitor for job changes at target accounts (new VP/C-level = outreach opportunity), funding events in last 90 days (new budget), hiring signals (3+ roles in your domain = building a team), technology signals (adopted/dropped competitor tool).
2. Score signals by recency (last 30 days strongest) and intensity (multiple signals from one account).
3. Route high-score signals directly into the SMS sequence queue in Attio. Verify mobile phone number before adding to queue. Medium-score signals go to a watch list.
4. Craft signal-specific SMS openers: funding signal gets a congratulations angle, job change gets a "welcome to the role" angle, hiring signal gets a "building your team" angle. Store as templates in the the sms copy generation workflow (see instructions below) pipeline.
5. The autonomous optimization loop monitors signal-to-reply rate and adjusts signal thresholds weekly. If a signal type produces below-average response rates, reduce its priority. If a new signal type emerges, add it.

### 4. Configure guardrails

**These guardrails are non-negotiable and override any optimization decision:**

- **Rate limit**: Maximum 1 active experiment at a time on SMS. Never stack experiments.
- **Revert threshold**: If response rate drops >30% at any point during an experiment, auto-revert immediately.
- **Compliance guardrails**: If opt-out rate exceeds 5% for any experiment variant, auto-revert and flag for review. If delivery rate drops below 85%, pause all sends on affected number.
- **Human approval required for**: any change affecting >50% of prospects, targeting/ICP changes, adding or removing phone numbers from the Messaging Service, budget changes >20%.
- **Cooldown**: After a failed experiment, wait 7 days before testing a new hypothesis on the same variable.
- **Max experiments per month**: 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Volume caps**: Never exceed the per-number and per-day sending limits set in Scalable. Optimization improves conversion, not volume.
- **TCPA compliance**: Never compromise opt-out handling, timezone windows (8am-9pm), or suppression list integrity for any optimization.

### 5. Monitor convergence

The optimization loop runs indefinitely. However, the agent detects **convergence** — when successive experiments produce diminishing returns:

- Track improvement magnitude per experiment over time
- If 3 consecutive experiments produce <2% improvement each, the play has reached its local maximum
- At convergence: reduce monitoring frequency from daily to weekly, reduce experiment cadence from weekly to monthly
- Generate a convergence report: "SMS outbound is optimized at [current response rate] with [current cost per meeting]. The opt-out rate is stable at [rate]. Further gains require strategic changes (new ICP segments, multi-channel integration, or product changes) rather than tactical SMS optimization."

**Human action required:** Review the convergence report. Decide whether to maintain current SMS performance, expand to new ICP segments, integrate SMS more deeply with email/LinkedIn cadences, or reallocate effort to other plays.

## Time Estimate

- SMS performance monitor setup: 6 hours
- Autonomous optimization loop configuration: 10 hours
- Signal detection setup: 5 hours
- Guardrail configuration: 3 hours
- Ongoing founder reply handling (reduced with classification): 40 hours (1 hr/day, 3-4 days/week)
- Weekly monitoring and brief review: 36 hours (1.5 hrs/week over 6 months)
- Monthly strategic review: 12 hours (2 hrs/month)
- Experiment design and implementation: 16 hours
- List building and signal management: 12 hours
- Convergence review and adjustment: 6 hours
- Buffer for manual interventions: 4 hours

Total: ~150 hours over 6 months.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Twilio | SMS sending + delivery tracking + number rotation | ~$12-20/mo at 800-1200 msgs; 3 numbers ~$3.45/mo (https://www.twilio.com/en-us/sms/pricing/us) |
| Clay | Continuous enrichment + signal detection + phone verification | Team: $349/mo (https://www.clay.com/pricing) |
| Apollo | Contact sourcing | Professional: $99/mo (https://www.apollo.io/pricing) |
| Attio | CRM + optimization audit trail + suppression | Plus: $29/user/mo (https://attio.com/pricing) |
| n8n | Orchestration + optimization loop workflows | Starter: $20/mo (https://n8n.io/pricing) |
| PostHog | Analytics + experiments + anomaly detection | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Anthropic API | Hypothesis generation + experiment evaluation + copy generation + reply classification | ~$50-100/mo at optimization frequency (https://www.anthropic.com/pricing) |
| Cal.com | Meeting booking | Free tier (https://cal.com/pricing) |

**Estimated play-specific cost: ~$100-160/mo** (Twilio ~$20 + Anthropic ~$75 + n8n $20; Clay and Apollo costs shared across plays)

## Drills Referenced

- `autonomous-optimization` — the core monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum for SMS response rate and cost per meeting
- `autonomous-optimization` — always-on dashboards, weekly briefs, monthly trend reports, and anomaly detection for SMS outbound
- `signal-detection` — continuous buying signal monitoring to keep the SMS prospect pipeline fresh and prioritized

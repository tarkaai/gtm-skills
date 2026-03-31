---
name: micro-roundtables-durable
description: >
  Micro-Roundtable — Durable Intelligence. Autonomous agent optimization of the
  roundtable series: detect metric anomalies, generate hypotheses, run experiments,
  evaluate results, and auto-implement winners. The agent finds the local maximum
  for topic selection, guest curation, invitation timing, and follow-up conversion.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Durable Intelligence"
time: "80 hours over 6 months"
outcome: "Sustained or improving meeting conversion rate over 6 months; agents autonomously optimize topic selection, guest mix, invitation approach, and follow-up sequences; convergence detected when 3 consecutive experiments produce <2% improvement"
kpis: ["Meeting conversion rate trend (stable or improving)", "Cost per meeting trend (stable or declining)", "Guest pool depth (≥ 30 uninvited ICP contacts at all times)", "Optimization experiment win rate (target ≥ 25% of experiments adopted)", "Weekly optimization brief generated"]
slug: "micro-roundtables"
install: "npx gtm-skills add marketing/solution-aware/micro-roundtables"
drills:
  - autonomous-optimization
---

# Micro-Roundtable — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

The roundtable series runs on autopilot with an always-on AI agent that monitors, diagnoses, experiments, and optimizes. The agent detects when any funnel metric degrades, generates hypotheses for what to change, runs controlled experiments, evaluates results, and auto-implements winners. The human facilitates discussions and approves high-risk changes. The goal is to find the local maximum — the best possible performance given the current market, audience, and competitive landscape — and maintain it as conditions change.

Pass: Meeting conversion rate sustained or improving over 6 months. Cost per meeting stable or declining. The optimization loop runs autonomously with weekly briefs to the team.
Convergence: When 3 consecutive experiments produce less than 2% improvement, the play has reached its local maximum. Reduce monitoring frequency and report to the team.

## Leading Indicators

- Anomaly detection triggers within 24 hours of a metric deviation (signals the monitoring layer is working)
- At least 1 experiment per month produces a measurable improvement (signals the optimization loop is finding gains)
- Guest pool depth never drops below 30 (signals the sourcing pipeline keeps up with series demand)
- Weekly optimization briefs are generated without manual intervention (signals the reporting loop is autonomous)

## Instructions

### 1. Deploy the roundtable performance monitor

Run the `autonomous-optimization` drill to build the always-on monitoring layer:

**Dashboard**: Create a "Roundtable Series Health" dashboard in PostHog with:
- Top row: next event confirmed count, trailing 4-event show rate, trailing 4-event meeting booking rate
- Middle row: invitation-to-meeting funnel for the last event vs series average
- Bottom row: RSVP rate trend, show rate trend, meetings per event trend, guest freshness ratio over time

**Anomaly detection**: Configure the n8n monitoring workflow with alerts for:
- Post-event: show rate below 60% (critical), engagement rate below 50% (critical)
- Post-nurture: Tier 1 reply rate below 20%, discussion summary open rate below 40%
- Rolling weekly: any metric declining >15% from the 4-event rolling average, RSVP rate declining for 3 consecutive events, guest pool depth below 30

**Post-mortems**: Auto-generate a structured post-mortem 14 days after each roundtable with metrics vs targets, what worked, what needs attention, and recommendations.

**Monthly reports**: Auto-generate a monthly series health report with aggregate metrics, trends, top/underperforming events, and series health status (GREEN/YELLOW/RED).

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the roundtable series. The optimization loop has five phases:

**Phase 1 — Monitor (daily via n8n cron):**
- Check all roundtable KPIs from the performance monitor against the 4-event rolling average
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ events), drop (>20% decline), spike (>50% increase)
- If normal: log to Attio, no action
- If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: pull the series configuration from Attio (current topic, guest profile, invitation timing, follow-up approach)
- Pull 8-event metric history from PostHog
- Generate 3 ranked hypotheses with expected impact and risk level
- Store hypotheses in Attio as notes on the roundtable calendar

Examples of roundtable-specific hypotheses:
- "RSVP rate dropped because the topic is too similar to the last 2 events. Hypothesis: switching to a contrarian topic framing will increase RSVP rate by 15%."
- "Show rate is declining because events are on Thursdays. Hypothesis: moving to Tuesday 10am will increase show rate by 10%."
- "Meeting conversion dropped because follow-up emails are not specific enough. Hypothesis: including a direct quote from the attendee in Email 1 will increase Tier 1 reply rate by 20%."

If the top hypothesis has risk = "high" (e.g., changing the core format, expanding to a new ICP segment): send to the host for approval and STOP.
If risk = "low" or "medium": proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment: use PostHog experiments to split the next 2 events between control (current approach) and variant (hypothesis change)
- Implement the variant using the appropriate drill or fundamental
- Set the experiment duration: minimum 2 events or 4 weeks, whichever is longer
- Log the experiment in Attio: hypothesis, start date, expected duration, success criteria

Roundtable-specific experiment design considerations:
- Small group sizes make statistical significance harder. Require at least 4 events (2 control, 2 variant) before evaluating.
- Some variables can only be tested sequentially (topic, time slot) not simultaneously. Design accordingly.
- Track both the primary metric (the one the hypothesis targets) and guardrail metrics (show rate, engagement, meeting conversion) to ensure the change does not break something else.

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Decision:
  - **Adopt**: Update the series configuration. Log the change. Move to Phase 5.
  - **Iterate**: Generate a refined hypothesis building on this result. Return to Phase 2.
  - **Revert**: Restore the control configuration. Log the failure. Return to Phase 1.
  - **Extend**: Keep the experiment running for 2 more events. Set a reminder.
- Store the full evaluation in Attio: decision, confidence, reasoning, metric impact

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity for the week
- Calculate net metric change from all adopted changes
- Generate a weekly optimization brief:
  - What changed and why
  - Net impact on primary KPIs
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 3. Manage long-term series health

Beyond the optimization loop, the agent maintains series health through:

**Guest pool sustainability**: The the roundtable series automation workflow (see instructions below) drill's Clay sourcing runs weekly, adding 5-10 new ICP-matched prospects. If guest pool depth drops below 30, the agent increases sourcing intensity. If it drops below 15, the agent alerts the team: "Guest pool critically low. Recommend pausing the series until sourcing catches up or expanding the ICP definition."

**Topic freshness**: Track which topic categories have been covered. After 6 months, no topic category should be repeated more than twice. If the topic backlog runs thin, the agent generates new topic ideas based on: recent industry news, common pain points from past roundtable transcripts, and competitive landscape changes.

**Attendee lifecycle management**: Contacts who attend 3+ roundtables and have not converted should be flagged for a different motion (advisory board invitation, case study request, or direct sales outreach). The roundtable series should not become a retention channel for non-converting contacts.

### 4. Detect convergence and evolve

The optimization loop runs indefinitely until convergence is detected: 3 consecutive experiments produce less than 2% improvement on the target metric.

At convergence:
1. The series has reached its local maximum for the current market, audience, and format
2. Reduce monitoring from daily to weekly
3. Report to the team: "Roundtable series is optimized. Current performance: [metrics]. Further gains require strategic changes (new ICP segment, different event format, co-hosted events, in-person component) rather than tactical optimization."
4. Shift agent effort to maintaining the local maximum as external conditions change (new competitors, market shifts, audience turnover)

## Time Estimate

- Performance monitor setup: 4 hours (one-time)
- Autonomous optimization configuration: 4 hours (one-time)
- Per-month ongoing human effort: 4-6 hours (facilitate 2-4 roundtables, review weekly briefs, approve high-risk experiments)
- Per-month agent-automated effort: 20-30 hours (monitoring, hypothesis generation, experiment management, reporting)
- Total human effort over 6 months: ~30-40 hours; agent handles the rest

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Guest pool management, optimization logs, event calendar | Plus: $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Cal.com | RSVP pages and follow-up meeting booking | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Loops | Invitation cadences, reminders, nurture sequences | $49/mo for up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Fireflies.ai | Automated transcription per event | Pro: $10/user/mo annual ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| PostHog | Analytics, experiments, anomaly detection, dashboards | Free up to 1M events/month; experiments may require paid tier ([posthog.com/pricing](https://posthog.com/pricing)) |
| Clay | Continuous guest sourcing and enrichment | Launch: $185/mo for 2,500 credits ([clay.com/pricing](https://clay.com/pricing)) |
| n8n | Optimization loop workflows, monitoring, reporting | Self-hosted: free; Cloud: from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation and experiment evaluation (Claude) | Usage-based: ~$15-50/mo at this volume ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Zoom / Google Meet | Host the roundtable | Free tier |

**Estimated monthly cost for Durable:** $312-547/mo (Loops $49 + Fireflies $10 + Clay $185 + n8n $24 + Attio $29 + Anthropic API $15-50 + optional PostHog paid tier)

## Drills Referenced

- `autonomous-optimization` — the always-on monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum for the roundtable series
- `autonomous-optimization` — continuous monitoring, anomaly detection, post-mortems, and monthly reports that feed data into the autonomous optimization loop

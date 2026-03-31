---
name: micro-events-webinars-durable
description: >
  Micro-Event or Webinar — Durable Intelligence. Always-on AI agents continuously
  monitor the webinar series funnel, detect metric anomalies, generate improvement
  hypotheses, run A/B experiments on topic selection, promotion, nurture sequences,
  and event format, then auto-implement winners. Weekly optimization briefs track
  progress toward the local maximum. Converges when successive experiments produce
  less than 2% improvement.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving registrations, show rate, and meetings per event over 6 months. Agents detect degradation, diagnose causes, experiment, and auto-implement improvements. Convergence when 3 consecutive experiments produce <2% improvement."
kpis: ["Registrations per event (vs rolling average)", "Show rate trend", "Meetings per event trend", "Cost per meeting trend", "Experiment win rate", "Time to convergence"]
slug: "micro-events-webinars"
install: "npx gtm-skills add marketing/solution-aware/micro-events-webinars"
drills:
  - autonomous-optimization
  - webinar-performance-monitor
---

# Micro-Event or Webinar — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Maintain or improve webinar series performance over 6 months without manual optimization effort
- Detect and respond to metric degradation (topic fatigue, show rate decline, nurture effectiveness drop) before they become critical
- Continuously experiment on every lever: topic selection, promotion channel mix, email copy, event format, nurture sequences, CTA variants
- Find the local maximum — the best achievable performance given your market, audience, and competitive landscape
- Generate weekly optimization briefs that summarize what changed, why, and what to try next
- Converge: when 3 consecutive experiments produce <2% improvement, the play is optimized

## Leading Indicators

- Anomaly detection fires within 24 hours of any metric moving >15% from the 4-event rolling average
- At least 1 experiment running at all times (the loop never idles until convergence)
- Experiment win rate >30% (not every experiment wins, but enough do to drive improvement)
- Weekly optimization briefs generated on schedule with actionable recommendations
- No metric declines for 3+ consecutive events without an experiment addressing it

## Instructions

### 1. Deploy continuous webinar funnel monitoring

Run the `webinar-performance-monitor` drill to build the always-on monitoring layer:

- **Post-event automated checks**: After each event, the agent runs immediate health checks — show rate vs target, engagement rate vs target, and nurture launch verification. Alerts fire if any metric falls below critical thresholds (show rate <20%, engagement <10%).
- **Rolling trend analysis**: Weekly n8n cron compares the last event's metrics against the 4-event rolling average. If any metric declines >15%, it flags for investigation and triggers the optimization loop.
- **Event post-mortems**: 14 days after each event (when nurture window closes), auto-generate a structured post-mortem: metrics vs targets, what worked, what needs attention, and recommendations.
- **Monthly series reports**: Aggregate all events for the month into a series health report: registration trends, show rate trends, pipeline generated, cost per meeting, and overall series health rating (GREEN/YELLOW/RED).

The monitoring outputs feed directly into the autonomous optimization loop.

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the webinar series:

**Phase 1 — Monitor (runs daily via n8n cron):**
- Pull the webinar series KPIs from PostHog using anomaly detection
- Compare the last 2 events' metrics against the 4-event rolling average
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ events), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather the current series configuration from Attio: active topic category, promotion channel mix, email copy variants, event format, time slot, nurture sequence structure
- Pull 8-event metric history from PostHog
- Run hypothesis generation with anomaly data + configuration context
- Receive 3 ranked hypotheses. Examples of webinar-specific hypotheses:
  - "Registration decline is caused by topic fatigue — the last 3 events covered similar ground. Hypothesis: switching to a new topic category will increase registrations by 20%."
  - "Show rate dropped because Wednesday 2pm has higher no-show rates than Tuesday 11am. Hypothesis: moving to Tuesday will increase show rate by 8 percentage points."
  - "Nurture reply rate declining because Tier 1 emails lack personalization. Hypothesis: adding Loom clips referencing specific questions will increase reply rate by 15%."
- If top hypothesis has risk = "high" (e.g., changing the core event format), send Slack alert for human approval. Otherwise, proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment using PostHog feature flags
- Implement the variant. Examples:
  - Topic test: Run the next 2 events with a new topic category, compare against the previous 2 events' registration rates
  - Promotion test: Split the invite list and send variant A (current subject line) and variant B (new subject line) for the same event
  - Nurture test: Route 50% of Tier 1 attendees into a variant nurture sequence with Loom clips, 50% into the current sequence
  - Format test: Run alternate events as workshops vs presentations, compare engagement and meeting rates
- Set experiment duration: minimum 2 events or 4 weeks, whichever is longer
- Log experiment start in Attio with hypothesis, variants, success criteria, and expected duration

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation: statistical significance, practical significance, and secondary metric impact
- Decision:
  - **Adopt**: Winner improves primary metric with 95% confidence. Update the series configuration. Log the change.
  - **Iterate**: Promising direction but not conclusive. Refine the hypothesis and re-run.
  - **Revert**: Variant performed worse. Restore the control. Log the failure and the learning.
  - **Extend**: Insufficient data. Run for 2 more events.

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments in progress (status, preliminary data)
  - Experiments completed (decisions, impact)
  - Net metric change from adopted experiments
  - Distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 3. Configure webinar-specific guardrails

The `autonomous-optimization` drill has standard guardrails. Add these webinar-specific constraints:

- **Topic diversity guard**: Never run the same topic category more than 2 events in a row, even if it performs well. Audience fatigue is real.
- **Format stability guard**: Do not change the event format more than once per month. Audience expectations matter.
- **Speaker coordination guard**: Any experiment that requires a guest speaker change must be planned 3+ weeks in advance. Speakers are humans, not variables.
- **Promotion budget guard**: Never increase paid promotion spend by more than 50% per event without human approval.
- **List fatigue guard**: Track unsubscribe rate on webinar invite emails. If it exceeds 1% on any send, pause and review targeting.
- **Maximum 1 active experiment per event**: Never test multiple variables on the same event. One change at a time for clean attribution.

### 4. Build the convergence detection system

The optimization loop should detect when the series has reached its local maximum:

- Track the percentage improvement from each adopted experiment
- When 3 consecutive experiments produce <2% improvement on the primary metric (meetings per event):
  1. The series is converging — most tactical levers have been optimized
  2. Reduce monitoring frequency from post-event to weekly
  3. Reduce experimentation frequency to 1 experiment per month (maintenance mode)
  4. Generate a convergence report: "This webinar series is optimized at [current metrics]. The best-performing configuration is [topic category, format, time slot, promotion mix, nurture sequence]. Further improvement requires strategic changes: new audience segments, product changes, or market shifts."

**Human action required:** At convergence, review the report. Decide whether to:
- Accept the local maximum and keep the series running in maintenance mode
- Reset by targeting a new audience segment or entering a new market
- Invest in a strategic change (e.g., co-hosting with a partner, launching a virtual summit) that shifts the performance ceiling

### 5. Sustain the series over 6 months

Over a 6-month Durable run, the agent:

- Manages a 12-24 event series with automated ops
- Runs 8-16 experiments across all webinar variables
- Generates 24+ weekly optimization briefs
- Produces monthly series health reports
- Detects and responds to seasonal patterns (holiday dips, end-of-quarter spikes)
- Refreshes the topic backlog quarterly based on new ICP research and audience feedback
- Identifies when the webinar audience is saturating (repeat attendees > new attendees) and recommends audience expansion strategies

The play is durable when the agent can maintain meetings-per-event above the Scalable baseline (8 meetings / 2 months) without human optimization effort.

## Time Estimate

- Monitoring setup (PostHog dashboards, n8n cron jobs, alert configuration): 8 hours
- Autonomous optimization loop configuration: 6 hours
- Guardrail and convergence detection setup: 4 hours
- Per-event agent-managed effort (promotion, nurture, analysis): 3 hours x 20 events = 60 hours
- Per-event human effort (content delivery only): 1 hour x 20 events = 20 hours
- Experiment design and implementation: 4 hours x 12 experiments = 48 hours
- Weekly brief review and strategic decisions: 1 hour x 24 weeks = 24 hours
- Monthly series report review: 2 hours x 6 months = 12 hours
- Quarterly topic refresh and strategic review: 6 hours x 2 = 12 hours
- **Total: ~200 hours over 6 months** (split: ~130 hours agent, ~70 hours human)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Webinar recording + production | $29/mo Pro (4K, 15hr transcription) — [riverside.com/pricing](https://riverside.com/pricing) |
| Loops | Email invites, reminders, nurture | $49/mo (up to 5,000 contacts) — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, experiments, anomaly detection | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM, event lists, deal tracking, reporting | $29/user/mo Plus — [attio.com](https://attio.com) |
| n8n | Monitoring crons, optimization loop, series automation | Self-hosted free or Cloud Pro EUR60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Clay | Prospect sourcing per event | $185/mo Launch (2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Descript | Recording clips + content repurposing | $24/mo Creator — [descript.com/pricing](https://www.descript.com/pricing) |
| Loom | Personalized follow-up clips | $12.50/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |
| Cal.com | Meeting booking CTA | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Anthropic API | Hypothesis generation + evaluation (Claude) | Usage-based ~$15-30/mo for this play — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost at Durable: $345-580/mo** (all tools above + Anthropic API usage)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, and generate weekly optimization briefs
- `webinar-performance-monitor` — continuous monitoring, post-event post-mortems, and monthly series health reports that feed data into the optimization loop

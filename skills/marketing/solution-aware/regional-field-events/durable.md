---
name: regional-field-events-durable
description: >
  Regional Field Events — Durable Intelligence. Always-on AI agents continuously
  monitor the multi-city field event series funnel, detect metric anomalies across
  cities and formats, generate improvement hypotheses, run experiments on venue
  selection, invitation strategy, topic rotation, and nurture sequences, then
  auto-implement winners. Weekly optimization briefs track progress toward the
  local maximum. Converges when successive experiments produce less than 2%
  improvement.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Direct"
level: "Durable Intelligence"
time: "250 hours over 6 months"
outcome: "Sustained or improving attendance, show rate, and meetings per event over 6 months across 5+ cities. Agents detect degradation, diagnose causes, experiment, and auto-implement improvements. Convergence when 3 consecutive experiments produce <2% improvement."
kpis: ["Meetings per event (vs rolling average)", "Show rate trend", "Cost per meeting trend", "City health distribution", "Experiment win rate", "Time to convergence"]
slug: "regional-field-events"
install: "npx gtm-skills add marketing/solution-aware/regional-field-events"
drills:
  - autonomous-optimization
  - field-event-performance-monitor
---

# Regional Field Events — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events, Direct

## Outcomes

- Maintain or improve field event series performance over 6 months without manual optimization effort
- Detect and respond to city-level degradation (audience fatigue, venue issues, seasonal dips) before they become critical
- Continuously experiment on every operational lever: invitation strategy, topic rotation, format, timing, venue selection, nurture sequences
- Find the local maximum — the best achievable performance given your target markets, audience, and competitive landscape
- Generate weekly optimization briefs that summarize what changed, why, and what to try next
- Converge: when 3 consecutive experiments produce <2% improvement, the series is optimized

## Leading Indicators

- Anomaly detection fires within 48 hours of any city-level or series-level metric moving >15% from the 4-event rolling average
- At least 1 experiment running at all times (the loop never idles until convergence)
- Experiment win rate >30% (not every experiment wins, but enough do to drive improvement)
- Weekly optimization briefs generated on schedule with actionable recommendations
- No city stays RED for 2+ consecutive events without an experiment addressing it

## Instructions

### 1. Deploy continuous field event series monitoring

Run the `field-event-performance-monitor` drill to build the always-on monitoring layer:

- **Post-event automated checks**: After each event, the agent runs immediate health checks at T+48 hours — show rate vs target, Tier 1 percentage vs target, and nurture launch verification. Alerts fire if any metric falls below critical thresholds (show rate <55%, Tier 1 % <25%).
- **Rolling trend analysis**: Weekly n8n cron compares the last 2 events' metrics against the 4-event rolling average. If any metric declines >15%, it flags for investigation and triggers the optimization loop.
- **City-level health scoring**: After each event, update the city scorecard (GREEN/YELLOW/RED). If a city hits RED on 2 consecutive events, trigger a strategic review: format change, topic pivot, or city deprioritization.
- **Event post-mortems**: 14 days after each event (when nurture window closes), auto-generate a structured post-mortem: metrics vs targets, what worked, what needs attention, and recommendations.
- **Monthly series health reports**: Aggregate all events for the month: attendance trends, city comparison, cost analysis, pipeline generated, and overall series health rating.

The monitoring outputs feed directly into the autonomous optimization loop.

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the field event series:

**Phase 1 — Monitor (runs weekly via n8n cron):**
- Pull the series KPIs from PostHog using anomaly detection
- Compare the last 2 events' metrics against the 4-event rolling average
- Compare each city's performance against the series-wide average
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ events), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather the current series configuration from Attio: active cities, event formats, topic rotation, invitation segments, venue ratings, nurture sequence performance
- Pull 12-event metric history from PostHog (covering ~3 months of data)
- Run hypothesis generation with anomaly data + configuration context
- Receive 3 ranked hypotheses. Examples of field-event-specific hypotheses:
  - "RSVP rate in [city] declined 25% over the last 3 events. Hypothesis: audience fatigue from the same dinner format. Switching to happy hour will increase RSVPs by 15% by attracting a broader audience."
  - "Show rate dropped across all cities in December. Hypothesis: seasonal effect from holiday schedules. Skipping the Dec 15-Jan 5 window and resuming in January will restore show rates."
  - "Tier 1 percentage dropped because topic [X] does not surface product-relevant pain points. Hypothesis: switching to topic [Y] that focuses on [specific pain] will increase Tier 1 percentage by 10 points."
  - "Cost per meeting increased because [venue] raised F&B minimum. Hypothesis: switching to [alternative venue] with lower minimums will reduce cost per meeting by 20%."
  - "Clay-sourced prospects have a 40% lower show rate than personal-network invitees. Hypothesis: adding a personal LinkedIn follow-up from the host to Clay-sourced RSVPs will close the show rate gap by 50%."
- If top hypothesis has risk = "high" (e.g., abandoning a city entirely or changing the core event format across all cities), send Slack alert for human approval. Otherwise, proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment. Field events have smaller sample sizes than digital channels, so experiments must be designed for noisy data:
  - Use paired comparisons: test the change in the same city back-to-back (event N = control, event N+1 = variant)
  - Or use cross-city comparisons: implement the change in city A while city B runs the control
  - Minimum experiment duration: 2 events or 4 weeks, whichever is longer
- Implement the variant. Examples:
  - Format test: Run the next event in [city] as a happy hour instead of a dinner. Compare RSVP rate, show rate, and Tier 1 percentage.
  - Topic test: Change the discussion theme for the next 2 events. Compare RSVPs and attendee engagement tier distribution.
  - Invitation test: Add a personal LinkedIn touchpoint for Clay-sourced RSVPs in city A. Compare show rate vs city B without the touchpoint.
  - Venue test: Switch to a different venue in the same city. Compare attendee satisfaction (via post-event survey or debrief notes) and repeat attendance.
  - Nurture test: Route 50% of Tier 2 attendees into a variant nurture with a Loom clip. Compare reply rate and meeting conversion vs control.
- Log experiment start in Attio with hypothesis, variants, success criteria, and expected duration

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog and Attio
- Run experiment evaluation: practical significance (field events cannot achieve statistical significance at traditional levels due to small samples — use a Bayesian approach with prior data from the series)
- Decision:
  - **Adopt**: Variant shows >10% improvement on the primary metric with at least moderate confidence. Update the series configuration. Log the change.
  - **Iterate**: Promising direction but not conclusive. Refine the hypothesis and re-run with the next 2 events.
  - **Revert**: Variant performed worse. Restore the control. Log the failure and the learning.
  - **Extend**: Insufficient data. Run for 2 more events in the same configuration.

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Events held this week and immediate health check results
  - Anomalies detected (series-level and city-level)
  - Experiments in progress (status, preliminary data)
  - Experiments completed (decisions, impact)
  - Net metric change from adopted experiments
  - City health summary (GREEN/YELLOW/RED per city)
  - Recommended focus for next week
- Post to Slack and store in Attio

### 3. Configure field-event-specific guardrails

The `autonomous-optimization` drill has standard guardrails. Add these field-event-specific constraints:

- **City rotation guard**: Never skip a city's scheduled event unless the city has been RED for 3+ consecutive events and a strategic review has approved deprioritization. Consistency builds community.
- **Format stability guard**: Do not change the event format in a city more than once per quarter. Attendees set expectations based on previous events.
- **Venue relationship guard**: Do not switch venues in a city more than once per quarter unless the venue received a rating below 3/5. Venue relationships take time to build and negotiate.
- **Headcount guard**: Never reduce the target headcount for an event by more than 30% without human approval. Shrinking events sends a negative signal.
- **Budget guard**: Never increase per-event F&B spend by more than 25% without human approval. Budget creep is real.
- **Topic diversity guard**: Never repeat the same discussion topic in the same city within a 3-event window. Audience fatigue is real for in-person events because the attendee pool is geographically constrained.
- **Maximum 1 active experiment per city**: Never test multiple variables in the same city at the same time. One change at a time for clean attribution.
- **Host availability guard**: Any experiment that requires a different host for an event must be approved by the new host 3+ weeks in advance.

### 4. Build the convergence detection system

The optimization loop should detect when the series has reached its local maximum:

- Track the percentage improvement from each adopted experiment
- When 3 consecutive experiments produce <2% improvement on the primary metric (meetings per event):
  1. The series is converging — most tactical levers have been optimized
  2. Reduce monitoring frequency from per-event to weekly
  3. Reduce experimentation frequency to 1 experiment per month (maintenance mode)
  4. Generate a convergence report: "This field event series is optimized at [current metrics]. The best-performing configuration per city is [format, topic category, time slot, venue, invitation approach]. Further improvement requires strategic changes: new markets, new audience segments, co-hosting with partners, or evolving the format (e.g., adding a panel or workshop component)."

**Human action required:** At convergence, review the report. Decide whether to:
- Accept the local maximum and keep the series running in maintenance mode
- Expand to new cities or regions to grow total pipeline
- Invest in a strategic change (e.g., co-hosting with a partner company, upgrading to a premium format like a multi-day retreat) that shifts the performance ceiling
- Evolve the series into a branded community (with its own identity beyond "our company's events")

### 5. Sustain the series over 6 months

Over a 6-month Durable run, the agent:

- Manages a 20-30 event series across 5+ cities with automated ops
- Runs 8-16 experiments across all field event variables
- Generates 24+ weekly optimization briefs
- Produces monthly series health reports and city scorecards
- Detects and responds to seasonal patterns (holiday dips, conference conflicts, summer travel)
- Refreshes the city rotation quarterly based on pipeline data and ICP density shifts
- Identifies when a city's audience is saturating (repeat attendees > new attendees) and recommends expansion strategies (new neighborhoods, new ICP segments, partner co-hosting)
- Tracks venue relationships and negotiates better terms based on consistent bookings

The play is durable when the agent can maintain meetings-per-event above the Scalable baseline (15 meetings / 10 events) without human optimization effort — humans only deliver events and make strategic decisions.

## Time Estimate

- Monitoring setup (PostHog dashboards, n8n crons, alert configuration): 10 hours
- Autonomous optimization loop configuration: 8 hours
- Guardrail and convergence detection setup: 4 hours
- Per-event agent-managed effort (sourcing, invitations, nurture, analysis): 3 hours x 24 events = 72 hours
- Per-event human effort (venue booking, event delivery, debrief): 3 hours x 24 events = 72 hours
- Experiment design and implementation: 4 hours x 12 experiments = 48 hours
- Weekly brief review and strategic decisions: 30 min x 24 weeks = 12 hours
- Monthly series report review: 2 hours x 6 months = 12 hours
- Quarterly city rotation refresh and strategic review: 6 hours x 2 = 12 hours
- **Total: ~250 hours over 6 months** (split: ~155 hours agent, ~95 hours human)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | RSVP pages and meeting booking | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Loops | Invitation sequences, nurture, recaps | $49/mo (up to 5,000 contacts) — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, experiments, anomaly detection | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM, event lists, venue database, deal tracking, reporting | $29/user/mo Plus — [attio.com](https://attio.com) |
| n8n | Monitoring crons, optimization loop, series automation | Self-hosted free or Cloud Pro EUR60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Clay | Prospect sourcing per city per event | $185/mo Launch (2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Fireflies | Discussion capture for structured segments | $19/mo Pro — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Loom | Personalized follow-up clips | $12.50/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |
| Anthropic API | Hypothesis generation + evaluation (Claude) | Usage-based ~$20-40/mo for this play — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Venue (x24) | F&B for ~24 events over 6 months | $5,000-30,000 total depending on format and cities |

**Estimated play-specific cost at Durable: $5,400-31,000 over 6 months** (venue F&B + software: ~$370-400/mo + Anthropic API)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, and generate weekly optimization briefs
- `field-event-performance-monitor` — continuous city-level and series-level monitoring, post-event health checks, rolling trend analysis, and monthly reports that feed data into the optimization loop

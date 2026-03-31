---
name: executive-roundtables-durable
description: >
  Executive Roundtables — Durable Intelligence. Always-on AI agents continuously
  monitor the roundtable series funnel, detect metric anomalies across the full
  executive engagement pipeline, generate improvement hypotheses, run A/B
  experiments on topic selection, guest composition, invitation copy, facilitation
  format, and nurture sequences, then auto-implement winners. Weekly optimization
  briefs track progress toward the local maximum. Converges when successive
  experiments produce less than 2% improvement.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained or improving executive engagement and >=25 meetings per quarter over 12 months. Agents detect degradation, diagnose causes, experiment, and auto-implement improvements. Convergence when 3 consecutive experiments produce <2% improvement."
kpis: ["Meetings per event (vs rolling average)", "Show rate trend", "Guest pool depth trend", "Experiment win rate", "Cost per meeting trend", "Time to convergence"]
slug: "executive-roundtables"
install: "npx gtm-skills add marketing/solution-aware/executive-roundtables"
drills:
  - autonomous-optimization
  - roundtable-performance-monitor
---

# Executive Roundtables — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Maintain or improve roundtable series performance over 12 months without manual optimization effort
- Detect and respond to metric degradation (topic fatigue, guest pool exhaustion, show rate decline, nurture effectiveness drop) before they become critical
- Continuously experiment on every lever: topic selection, guest composition, invitation copy and timing, facilitation format, follow-up sequences, discussion summary distribution
- Find the local maximum — the best achievable meeting conversion and executive engagement given your market, audience, and competitive landscape
- Generate weekly optimization briefs that summarize what changed, why, and what to try next
- Converge: when 3 consecutive experiments produce <2% improvement on meetings per event, the play is optimized

## Leading Indicators

- Anomaly detection fires within 48 hours of any metric moving >15% from the 4-event rolling average
- At least 1 experiment running at all times (the loop never idles until convergence)
- Experiment win rate >30% (enough experiments succeed to produce measurable improvement)
- Weekly optimization briefs generated on schedule with actionable recommendations
- No metric declines for 3+ consecutive events without an experiment addressing it
- Guest pool depth never drops below 40 uninvited executive contacts

## Instructions

### 1. Deploy continuous roundtable funnel monitoring

Run the `roundtable-performance-monitor` drill to build the always-on monitoring layer:

**Post-event automated checks (triggered 2 hours after each roundtable):**
- Show rate vs target (>=75%): if <60%, fire alert: "Show rate critically low — review confirmation cadence, attendee commitment signals, and exclusivity framing"
- Engagement rate vs target (>=80% spoke at least once): if <50%, fire alert: "Low engagement — review facilitation approach, topic selection, or group composition. Possible causes: topic too consensus-driven, group too large, or seniority mismatch."
- Tier 1 attendee count: if <2, flag: "Low high-engagement count — review topic relevance to attendee pain points"

**48-hour post-nurture checks:**
- Tier 1 reply rate: if <20% (vs target 40%), fire alert: "High-intent executive replies low — review personalization quality, reference specificity from transcript, and CTA friction"
- Discussion summary open rate: if <40% (vs target 70%), fire alert: "Summary underperforming — review subject line and send timing. Executives may not be finding the summary valuable."

**Rolling checks (weekly via n8n cron):**
- Compare each metric to the 4-event rolling average
- If RSVP rate declines >15% from rolling average, flag: "Demand declining — investigate topic selection, guest pool exhaustion, invitation fatigue, or competitive events"
- If show rate declines for 3 consecutive events, flag: "Commitment trend declining — review confirmation process, exclusivity positioning, and peer group appeal"
- If guest pool depth drops below 40 uninvited contacts, flag: "Guest pool running low — increase Clay sourcing volume, expand ICP criteria, or activate new industry verticals"
- If meeting conversion declines >20% from rolling average, flag: "Pipeline conversion declining — review follow-up timing, personalization quality, and CTA relevance"

**Event post-mortems (auto-generated 14 days after each event):**
Generate a structured post-mortem for each roundtable:
- Metrics vs targets vs 4-event rolling average vs best-ever event
- Guest composition: new vs returning ratio, industry mix, seniority distribution
- Top 3 discussion themes from transcript analysis
- What worked and hypothesized reasons
- What needs attention and hypothesized causes
- Specific recommendations for the next event

**Monthly series reports:**
- Events this month, total attendees, meetings booked, pipeline generated
- Guest pool status: available, invited-but-not-attended, exhausted
- Series health rating: GREEN (all metrics within target), YELLOW (1-2 metrics below target), RED (3+ metrics below target or declining trend)
- Trend analysis: are we improving, plateauing, or declining?

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the executive roundtable series:

**Phase 1 — Monitor (runs daily via n8n cron):**
- Pull the roundtable series KPIs from PostHog using anomaly detection
- Compare the last 2 events against the 4-event rolling average
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ events), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather current series configuration from Attio: active topic category, guest composition rules, invitation copy variants, facilitation format, time slot, nurture sequence structure
- Pull 8-event metric history from PostHog
- Run hypothesis generation with anomaly data + configuration context
- Receive 3 ranked hypotheses. Examples of executive roundtable-specific hypotheses:
  - "RSVP rate declining because the guest pool is saturated in the fintech vertical. Hypothesis: expanding to healthtech C-suite will increase RSVP rate by 15% by tapping fresh demand."
  - "Meeting conversion dropped because the last 2 topics were thought-provoking but not decision-relevant. Hypothesis: shifting to a topic that connects to an active budget cycle will increase meetings by 25%."
  - "Show rate dropped because Wednesday 3pm conflicts with board meeting prep at this company size. Hypothesis: moving to Tuesday 10am will increase show rate by 10 percentage points."
  - "Tier 1 nurture reply rate declining because follow-up emails reference discussion themes but not specific attendee statements. Hypothesis: inserting a direct quote from their transcript contribution will increase reply rate by 20%."
- If top hypothesis has risk = "high" (e.g., changing the core guest profile or shifting industry focus), send Slack alert for human approval. Otherwise, proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment. One variable at a time. Examples:
  - Topic test: Run the next 2 events with a new topic category, compare against the previous 2 events' RSVP and meeting rates
  - Guest composition test: Run one event with a vertical-specific group and one with a cross-industry group. Compare engagement tier distribution and meeting conversion.
  - Invitation copy test: Split the invite list for a single event. Send variant A (current copy) to half, variant B (new approach) to the other half. Measure RSVP rate.
  - Follow-up personalization test: Route 50% of Tier 1 attendees into a variant nurture sequence with direct transcript quotes, 50% into the current sequence. Compare reply rate.
  - Facilitation format test: Alternate events between open discussion and structured format with a brief guest opening. Compare engagement and meeting rates.
- Set experiment duration: minimum 2 events or 8 weeks, whichever is longer (roundtable sample sizes are small, so experiments need more time)
- Log experiment start in Attio with: hypothesis, variants, success criteria, expected duration

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation. Due to small sample sizes in roundtables, use:
  - Primary: practical significance (is the effect size meaningful for the business, even if not statistically significant at p<0.05?)
  - Secondary: directional consistency (did the variant outperform on 3+ events, even if individual event differences were small?)
  - Tertiary: secondary metric impact (did improving RSVP rate degrade engagement quality? Watch for tradeoffs.)
- Decision:
  - **Adopt**: Variant outperforms control on primary metric across 2+ events with meaningful effect size. Update series configuration. Log the change.
  - **Iterate**: Promising direction but inconclusive. Refine the hypothesis. Re-run for 2 more events.
  - **Revert**: Variant performed worse or had unacceptable secondary metric impact. Restore control. Log the failure and the learning.
  - **Extend**: Insufficient data. Run for 2 more events.

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments in progress (status, preliminary data)
  - Experiments completed (decisions, impact)
  - Net metric change from adopted experiments
  - Current distance from estimated local maximum
  - Guest pool health status
  - Recommended focus for next week
- Post to Slack and store in Attio

### 3. Configure executive roundtable-specific guardrails

The `autonomous-optimization` drill has standard guardrails. Add these roundtable-specific constraints:

- **Topic diversity guard**: Never run the same topic category more than 2 events in a row, even if it outperforms. Executive audience fatigue is a real risk and harder to recover from than general audience fatigue.
- **Guest pool conservation guard**: Never invite more than 25% of the remaining guest pool to a single event. Guest pool exhaustion is the primary existential risk for this play.
- **Exclusivity integrity guard**: Never increase confirmed capacity above 12 per event. Roundtable intimacy is the core differentiator. If the agent detects that events with more attendees produce lower meeting rates, reduce capacity further.
- **Relationship guard**: Never auto-enroll executives who have attended 4+ roundtables into standard nurture sequences. These are now relationships, not leads. Flag them for personal host outreach or advisory board invitation.
- **Seniority guard**: Never relax the seniority floor below VP to increase attendance. The quality of the peer conversation depends on seniority parity. Lower seniority attendees degrade the experience for senior ones.
- **Facilitation quality guard**: Any experiment that requires changing the discussion format must be planned 2+ events in advance. The host needs to prepare differently for structured vs open formats.
- **Maximum 1 active experiment per event**: Never test multiple variables on the same event. Roundtable sample sizes are too small for clean multi-variable attribution.
- **Budget guard**: The roundtable play has low direct tool costs. The real cost is the host's time and the guest pool. Never recommend actions that increase event frequency above monthly without human approval — the host can burn out and the guest pool can exhaust.

### 4. Build the convergence detection system

Track the percentage improvement from each adopted experiment:

- When 3 consecutive experiments produce <2% improvement on the primary metric (meetings per event):
  1. The series is converging — most tactical levers have been optimized
  2. Reduce monitoring frequency from post-event to bi-weekly
  3. Reduce experimentation to 1 experiment per quarter (maintenance mode)
  4. Generate a convergence report:

```
## Executive Roundtable Series — Convergence Report

### Status: CONVERGED
### Current Performance:
- Average attendees per event: [N]
- Average meeting conversion: [X]%
- Average show rate: [X]%
- Cost per meeting: $[X]
- Guest pool depth: [N] available

### Optimized Configuration:
- Best topic category: [category]
- Best guest composition: [vertical/cross-industry, company size, seniority]
- Best facilitation format: [open/structured]
- Best time slot: [day/time]
- Best invitation approach: [personal/broadcast mix]
- Best follow-up timing: [hours post-event]

### Further Improvement Requires Strategic Changes:
- New executive audience segments (different industry, geography, or seniority band)
- Product changes that open new discussion topics
- Co-hosting with a partner to access their executive network
- Evolving to in-person roundtables for deeper relationship building
- Launching a private executive community or advisory board from the roundtable alumni
```

**Human action required:** At convergence, review the report. Decide whether to:
- Accept the local maximum and keep the series in maintenance mode
- Reset by targeting a new executive segment or entering a new market
- Evolve the format: in-person dinners, multi-day retreats, or private community

### 5. Sustain the series over 12 months

Over a 12-month Durable run, the agent:

- Manages 6-12 roundtables with fully automated ops (guest sourcing, invitations, reminders, follow-up, analytics)
- Runs 6-12 experiments across all roundtable variables
- Generates 48+ weekly optimization briefs
- Produces 12 monthly series health reports
- Maintains a guest pool of 50+ uninvited executives at all times
- Detects and responds to seasonal patterns (Q4 holiday dips, Q1 budget season shifts, summer schedule compression)
- Refreshes the topic backlog quarterly based on market trends, attendee feedback from transcripts, and ICP evolution
- Identifies when the executive audience is saturating and recommends geographic or industry expansion
- Graduates high-engagement repeat attendees to advisory board, case study, or partnership tracks
- Tracks the long-term pipeline impact: deals sourced from roundtable relationships, average deal value, sales cycle length compared to other pipeline sources

The play is durable when the agent maintains meetings-per-event at or above the Scalable baseline (5 meetings per event average) without human optimization effort. The host's only role is facilitating the live discussions.

## Time Estimate

- Monitoring setup (PostHog dashboards, n8n cron jobs, alert configuration): 8 hours
- Autonomous optimization loop configuration: 6 hours
- Guardrail and convergence detection setup: 4 hours
- Per-event agent-managed effort (guest sourcing, invitations, nurture, analysis): 6 hours x 10 events = 60 hours
- Per-event human effort (facilitation only): 1 hour x 10 events = 10 hours
- Experiment design and implementation: 5 hours x 8 experiments = 40 hours
- Weekly brief review: 30 min x 48 weeks = 24 hours
- Monthly report review: 2 hours x 12 months = 24 hours
- Quarterly topic refresh and strategic review: 2 hours x 4 = 8 hours
- **Total: ~180 hours over 12 months** (split: ~150 hours agent, ~30 hours human)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM, guest pool, event lists, deal tracking, reporting | $29/user/mo Plus — [attio.com](https://attio.com) |
| Fireflies.ai | Roundtable transcription + transcript analysis | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Loops | Invitation sequences, reminders, nurture emails | $49/mo (up to 5,000 contacts) — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, anomaly detection, experiments | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Monitoring crons, optimization loop, series automation | Self-hosted free or Cloud Pro EUR60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Clay | Net-new executive prospect sourcing (weekly) | $185/mo Launch (2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Cal.com | Meeting booking CTA | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Anthropic API | Hypothesis generation + experiment evaluation (Claude) | Usage-based ~$10-25/mo for this play — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Zoom Pro | Reliable roundtable hosting | $13.33/mo — [zoom.us/pricing](https://zoom.us/pricing) |

**Estimated play-specific cost at Durable: $345-560/mo** (all tools above + Anthropic API usage)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, and generate weekly optimization briefs. This is the drill that makes Durable fundamentally different from Scalable.
- `roundtable-performance-monitor` — continuous monitoring, post-event post-mortems, rolling trend analysis, and monthly series health reports that feed data into the optimization loop

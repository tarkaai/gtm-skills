---
name: event-piggybacking-durable
description: >
  Event Piggyback Meetup — Durable. Autonomous agents continuously optimize the
  piggyback meetup motion: selecting conferences, tuning promotion and follow-up,
  refining event formats, and finding the local maximum of pipeline per event dollar.
stage: "Marketing > ProblemAware"
motion: "MicroEvents"
channels: "Other"
level: "Durable"
time: "Ongoing (8-12 hours/month active management)"
outcome: "Sustained or improving RSVP-to-meeting rate and cost-per-meeting over 6 months via autonomous optimization; agents detect performance drift and auto-correct"
kpis: ["RSVP-to-meeting rate", "Cost per meeting", "Pipeline generated per month ($)", "Events hosted per month", "Experiment win rate"]
slug: "event-piggybacking"
install: "npx gtm-skills add marketing/problem-aware/event-piggybacking"
drills:
  - autonomous-optimization
  - event-scouting
---

# Event Piggyback Meetup — Durable

> **Stage:** Marketing > ProblemAware | **Motion:** MicroEvents | **Channels:** Other

## Outcomes

The piggyback meetup motion runs on autopilot with human event attendance as the only manual component. Agents handle everything else: discovering and scoring conferences, building and enriching target lists, launching promotion campaigns, automating follow-up, tracking performance, detecting when metrics drift, generating improvement hypotheses, running experiments, and implementing winners. The system converges toward the local maximum of pipeline generated per event dollar invested. Weekly optimization briefs keep the team informed of what changed and why.

## Leading Indicators

- Optimization loop is running (at least 1 experiment per month)
- Successive experiments produce measurable lifts (>2% improvement)
- Cost per meeting stable or declining month-over-month
- Conference selection accuracy improving (fewer "miss" events over time)
- Promotion conversion rates stable or improving across channels
- Follow-up-to-meeting conversion rates stable or improving
- Weekly optimization briefs generated on schedule
- Convergence signal: when 3 consecutive experiments produce <2% improvement, the motion has reached its local maximum

## Instructions

### 1. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the piggyback meetup motion. This is the core of Durable -- it creates the always-on monitor-diagnose-experiment-evaluate-implement cycle.

**Configure the optimization loop with these play-specific parameters:**

**Primary KPIs to monitor:**
- RSVP-to-meeting conversion rate (primary)
- Cost per meeting (secondary)
- Pipeline generated per event (secondary)

**Optimization variables the agent can experiment on:**
- Outreach email subject lines and body copy (test across events)
- Email send timing relative to conference (T-28 vs T-21 vs T-14 start)
- LinkedIn post framing (event announcement vs discussion teaser vs social proof)
- Reminder email cadence (T-7 + T-1 vs T-10 + T-3 + T-1 vs T-7 only)
- Follow-up email timing (same-day vs next-morning vs 48-hour)
- Follow-up email copy (conversation-reference vs resource-share vs direct-ask)
- Event format emphasis (roundtable vs mixer vs demo night) based on conference type
- Venue proximity scoring weight (same hotel vs walking distance vs taxi distance)
- Target list size and quality threshold (top 100 vs top 200 contacts per event)
- Interest-level thresholds for deal creation (level 4+ vs level 3+)

**Variables the agent must NOT change without human approval:**
- Target ICP definition
- Monthly event budget (venue + travel spend cap)
- Meetup branding and host identity
- Pricing of any tool subscription
- Geographic expansion (adding new cities)

**Monitoring cadence:** The `autonomous-optimization` drill's Phase 1 (Monitor) runs daily via n8n cron. It checks:
- Rolling 4-event RSVP-to-meeting rate vs 8-event average
- Per-conference promotion performance vs predicted performance (from scouting score)
- Follow-up response rates vs historical baseline
- Attendance rate vs historical baseline

**Anomaly triggers:**
- RSVP-to-meeting rate drops >15% from 8-event rolling average -> trigger diagnosis
- Two consecutive events produce zero meetings -> trigger diagnosis
- Attendance rate drops below 40% -> trigger diagnosis
- Cost per meeting rises >30% from baseline -> trigger diagnosis
- Promotion open rate drops >20% from baseline -> trigger diagnosis

When an anomaly triggers, the `autonomous-optimization` drill runs Phase 2 (Diagnose) to generate hypotheses, then Phase 3 (Experiment) to test the top hypothesis.

### 2. Deploy the performance monitoring layer

Run the `autonomous-optimization` drill to build:

**Real-time dashboard** with:
- Headline metrics: total RSVPs, attendance rate, meetings, pipeline, cost-per-meeting (30/90 day views)
- Per-conference breakdown table with full-funnel ROI calculation
- Funnel visualization: invite_sent -> rsvp_registered -> attended -> meeting_booked -> deal_created -> deal_won
- Promotion channel effectiveness: RSVPs by channel, conversion rate by email template, LinkedIn vs email performance
- Trend lines showing improvement over time
- Experiment history: what was tested, what won, what impact it had

**Post-event automated report** (generated 7 days after each event):
- This event's numbers vs running average across all events
- Promotion channel breakdown for this event
- Attendee quality assessment (ICP match rate, interest level distribution)
- Follow-up conversion data
- Recommended changes for the next event

**Monthly summary** (first Monday of each month):
- All events this month: aggregate metrics and individual performance
- Month-over-month trends: RSVPs, attendance, meetings, pipeline, cost efficiency
- Active experiments and their status
- Upcoming events on the calendar with predicted performance
- Conference selection intelligence updates

### 3. Run continuous conference scouting with learning feedback

Run the `event-scouting` drill on a weekly cadence (upgraded from monthly at Scalable). The key difference at Durable: the scouting algorithm improves itself.

Feed actual event outcomes back into the scouting score. After each piggyback event, compare predicted piggyback potential (from scouting score) to actual results (RSVPs, attendance, meetings, pipeline). Adjust scouting weights:

- If conferences with 500-1,000 attendees consistently outperform larger ones, tighten the size band
- If conferences in certain industries consistently produce higher-quality attendees, increase the industry weight
- If conferences hosted at hotels consistently get higher meetup attendance than convention center conferences, increase the venue-type weight
- If certain conference organizers or series consistently produce good piggyback results, add an "organizer quality" factor
- If day-of-week consistently matters (Tuesday evenings outperform Thursday evenings), add a day-of-week score

The agent maintains a correlation matrix of conference characteristics vs. piggyback outcomes. This matrix feeds into future scouting decisions, making each quarter's conference selection better than the last.

### 4. Optimize the full funnel autonomously

The `autonomous-optimization` drill experiments on the complete funnel. Typical experiment sequence:

**Month 1-2: Promotion optimization.**
The lowest-hanging fruit. Test outreach email copy, subject lines, send timing, and LinkedIn messaging. Each experiment runs across 4+ events for sample size. The agent implements winners and moves to the next variable.

**Month 3-4: Follow-up optimization.**
Test follow-up timing, copy, segmentation thresholds, and channel mix (email-only vs email+LinkedIn). Measure impact on meetings-per-event.

**Month 5-6: Event format and conference selection optimization.**
With enough historical data, test whether the scouting score accurately predicts outcomes. Deliberately piggyback 1-2 conferences outside the normal score range to validate the model. Test new event formats against the current winner. Refine scoring weights based on results.

**Ongoing: Convergence detection.**
When 3 consecutive experiments produce <2% improvement, the motion has reached its local maximum. The agent:
- Reduces monitoring from daily to weekly
- Reports: "Piggyback meetup motion optimized. Current performance: [metrics]. Further gains require strategic changes (new markets, new ICP segments, co-hosting partnerships, product changes) rather than tactical optimization."
- Continues monitoring for drift (seasonal shifts, conference calendar changes, competitive moves)

### 5. Guardrails

All guardrails from the `autonomous-optimization` drill apply, plus:

- **Never exceed 1 active experiment per funnel stage** (e.g., do not test promotion copy AND promotion timing simultaneously)
- **Monthly event budget guardrail:** If total monthly event spend (venues + food/drinks) exceeds budget by >20%, the agent stops recommending new events until the next month
- **Human-in-the-loop for event attendance decisions:** The agent recommends conferences and manages the full pipeline, but a human confirms each event before venue booking and before attending. The agent never books venues or travel autonomously.
- **Revert any follow-up change that produces >5% unsubscribe or negative-reply rate**
- **Monthly human review:** A human reviews the monthly optimization brief and confirms the strategic direction. The agent optimizes tactics; humans own strategy.
- **Conference relationship guardrail:** If a conference organizer asks you to stop promoting side events, immediately pause all promotion for that conference and flag for human review.
- **Maximum experiments per month:** 2 (piggyback events are lower frequency than email; experiments need more time to accumulate sample size)

## Time Estimate

- 3-4 hours/week: event attendance and hosting (human, irreducible)
- 1 hour/week: review weekly optimization brief and approve/reject recommendations
- 0.5 hours per event: review and approve automated follow-up drafts for high-interest attendees
- 2 hours/month: review monthly performance report and confirm strategic direction
- Agent compute: ~5-10 n8n workflow executions/day (monitoring, promotion, follow-up, experiments)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Conference scouting, attendee enrichment, with learning feedback | Growth: $495/mo (https://www.clay.com/pricing) |
| Attio | Contact/deal/event management, optimization data store | Plus plan for automation: pricing varies (https://attio.com/pricing) |
| Cal.com | Registration pages and meeting booking flow | Free tier or $15/user/mo for team features (https://cal.com/pricing) |
| Loops | Confirmation, reminders, and automated follow-up sequences | Starter: $49/mo (https://loops.so/pricing) |
| Instantly | Outreach campaigns | Hypergrowth: $97/mo for volume (https://instantly.ai/pricing) |
| PostHog | Analytics, experiments, anomaly detection, dashboards | Free up to 1M events/mo (https://posthog.com/pricing) |
| n8n | Optimization loop orchestration, full pipeline automation | Self-hosted: free; Cloud: $24/mo (https://n8n.io/pricing) |
| Anthropic API | Hypothesis generation and experiment evaluation | Usage-based, ~$5-15/mo at this volume (https://www.anthropic.com/pricing) |

**Play-specific cost at Durable level:** ~$300-500/event for venue costs (2-3 events/mo = $600-1,500/mo). Tooling: Clay Growth ($495/mo) + Loops ($49/mo) + Instantly ($97/mo) + n8n ($24/mo) + Anthropic API (~$10/mo) = ~$675/mo. Total: ~$1,275-2,175/mo.

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate loop that makes Durable fundamentally different; detects metric anomalies, generates hypotheses, runs A/B tests, auto-implements winners
- `autonomous-optimization` — real-time dashboard, post-event reports, monthly summaries, conference selection intelligence, and promotion channel analysis
- `event-scouting` — continuous conference discovery with learning feedback from actual piggyback outcomes

---
name: cold-event-hallway-demos-durable
description: >
  Event Hallway Demos — Durable. Autonomous agents continuously optimize the hallway demo
  motion: selecting events, tuning follow-up sequences, refining demo approaches, and
  finding the local maximum of pipeline per event-hour invested.
stage: "Marketing > ProblemAware"
motion: "MicroEvents"
channels: "Other"
level: "Durable"
time: "Ongoing (10-15 hours/month active management)"
outcome: "Sustained or improving demo-to-meeting rate and cost-per-meeting over 6 months via autonomous optimization; agents detect when performance drifts and auto-correct"
kpis: ["Demo-to-meeting rate", "Cost per meeting", "Pipeline generated per month ($)", "Events attended per month", "Experiment win rate"]
slug: "cold-event-hallway-demos"
install: "npx gtm-skills add marketing/problem-aware/cold-event-hallway-demos"
drills:
  - autonomous-optimization
  - hallway-demo-performance-monitor
  - event-scouting
---

# Event Hallway Demos — Durable

> **Stage:** Marketing > ProblemAware | **Motion:** MicroEvents | **Channels:** Other

## Outcomes

The hallway demo motion runs on autopilot with human attendance as the only manual component. Agents handle everything else: discovering and scoring events, enriching targets, triggering pre-event outreach, automating follow-up, tracking performance, detecting when metrics drift, generating improvement hypotheses, running experiments, and implementing winners. The system converges toward the local maximum of pipeline generated per hour of event attendance. Weekly optimization briefs keep the team informed of what changed and why.

## Leading Indicators

- Optimization loop is running (at least 1 experiment per month)
- Successive experiments produce measurable lifts (>2% improvement)
- Cost per meeting stable or declining month-over-month
- Event selection accuracy improving (fewer "miss" events over time)
- Follow-up conversion rates stable or improving
- Weekly optimization briefs generated on schedule
- Convergence signal: when 3 consecutive experiments produce <2% improvement, the motion has reached its local maximum

## Instructions

### 1. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the hallway demo motion. This is the core of Durable -- it creates the always-on monitor-diagnose-experiment-evaluate-implement cycle.

**Configure the optimization loop with these play-specific parameters:**

**Primary KPIs to monitor:**
- Demo-to-meeting conversion rate (primary)
- Cost per meeting (secondary)
- Pipeline generated per event (secondary)

**Optimization variables the agent can experiment on:**
- Follow-up email timing (same-day vs next-morning vs 48-hour)
- Follow-up email copy (pain-focused vs benefit-focused vs social-proof)
- Pre-event outreach messaging and timing (10 days vs 7 days vs 3 days before event)
- Event selection scoring weights (ICP density vs venue accessibility vs event size)
- Interest-level thresholds for deal creation (level 4+ vs level 3+)
- Demo format emphasis (60-second pitch-first vs 3-minute show-first)

**Variables the agent must NOT change without human approval:**
- Target ICP definition
- Event attendance budget (total monthly travel spend)
- Product demo content or positioning
- Booking link configuration

**Monitoring cadence:** The `autonomous-optimization` drill's Phase 1 (Monitor) runs daily via n8n cron. It checks:
- Rolling 2-week demo-to-meeting rate vs 4-week average
- Per-event pipeline vs predicted pipeline (from scouting score)
- Follow-up response rates vs historical baseline

**Anomaly triggers:**
- Demo-to-meeting rate drops >15% from 4-week average -> trigger diagnosis
- Two consecutive events produce zero meetings -> trigger diagnosis
- Follow-up response rate drops >20% -> trigger diagnosis
- Cost per meeting rises >30% from baseline -> trigger diagnosis

When an anomaly triggers, the `autonomous-optimization` drill runs Phase 2 (Diagnose) to generate hypotheses, then Phase 3 (Experiment) to test the top hypothesis.

### 2. Deploy the performance monitoring layer

Run the `hallway-demo-performance-monitor` drill to build:

**Real-time dashboard** with:
- Headline metrics: total demos, meetings, pipeline, cost-per-meeting (30/90 day views)
- Per-event breakdown table with ROI calculation
- Funnel visualization: conversation -> demo -> meeting -> deal -> won
- Trend lines showing improvement over time
- Experiment history: what was tested, what won, what impact it had

**Weekly automated report** (generated every Monday):
- Last week's numbers vs 4-week rolling average
- Events attended and their performance vs prediction
- Active experiments and their status
- Upcoming events on the calendar with expected ROI
- Recommended actions

**Monthly event circuit intelligence:**
- Which event types (conference, meetup, summit, workshop) produce the best pipeline per hour
- Which cities have the highest ICP density
- Seasonal patterns (conferences cluster in spring/fall; meetups are steady)
- Sponsor-to-attendee ratio as a predictor of event quality

### 3. Run continuous event scouting with learning feedback

Run the `event-scouting` drill on a weekly cadence (upgraded from monthly at Scalable). The key difference at Durable: the scouting algorithm improves itself.

Feed actual event outcomes back into the scouting score. After each event, compare predicted ROI (from scouting score) to actual ROI (from performance data). Adjust scouting weights:
- If hotel-venue events consistently outperform convention centers, increase the venue-accessibility weight
- If events with 300-500 attendees outperform larger events, tighten the size scoring band
- If certain event organizers or series consistently produce good results, add an "organizer quality" factor

The agent maintains a lookup table of event characteristics correlated with outcome quality. This lookup feeds into future scouting decisions, making each quarter's event selection better than the last.

### 4. Optimize the full funnel autonomously

The `autonomous-optimization` drill experiments on the complete funnel. Typical experiment sequence:

**Month 1-2: Follow-up optimization.**
The lowest-hanging fruit. Test follow-up timing, copy, and channel. Each experiment runs 2 weeks (across 4+ events for sample size). The agent implements winners and moves to the next variable.

**Month 3-4: Pre-event outreach optimization.**
Test whether pre-event messages increase on-the-day meeting rates. Experiment with message content, timing, and channel (LinkedIn vs email vs both).

**Month 5-6: Event selection optimization.**
With enough historical data, test whether the scouting score accurately predicts outcomes. Deliberately attend 1-2 events outside the normal score range to validate the model. Refine scoring weights based on results.

**Ongoing: Convergence detection.**
When 3 consecutive experiments produce <2% improvement, the motion has reached its local maximum. The agent:
- Reduces monitoring from daily to weekly
- Reports: "Hallway demo motion optimized. Current performance: [metrics]. Further gains require strategic changes (new markets, new ICP segments, product changes) rather than tactical optimization."
- Continues monitoring for drift (market changes, seasonal shifts, competitive moves)

### 5. Guardrails

All guardrails from the `autonomous-optimization` drill apply, plus:
- **Never exceed 1 active experiment per funnel stage** (e.g., do not test follow-up timing AND follow-up copy simultaneously)
- **Travel budget guardrail:** If total monthly event travel exceeds budget by >20%, the agent stops recommending new events until the next month
- **Human-in-the-loop for event attendance decisions:** The agent recommends events; a human confirms attendance. The agent never books travel autonomously.
- **Revert any follow-up change that produces >5% unsubscribe/negative-reply rate**
- **Monthly human review:** Even at Durable, a human reviews the monthly optimization brief and confirms the direction. This is not a set-and-forget system -- it is an agent-augmented system with human strategic oversight.

## Time Estimate

- 2-3 hours/week: event attendance (human, irreducible)
- 1-2 hours/week: review weekly optimization brief and approve/reject recommendations
- 2-3 hours/month: review monthly performance report and strategic direction
- Agent compute: ~10-20 n8n workflow executions/day (monitoring, follow-up, experiments)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Continuous event scouting with learning feedback | Growth: $495/mo (https://www.clay.com/pricing) |
| Attio | Contact/deal/event management, optimization data store | Plus plan for automation: pricing varies (https://attio.com/pricing) |
| Cal.com | Meeting booking flow | Free tier or $15/user/mo for team features (https://cal.com/pricing) |
| PostHog | Analytics, experiments, anomaly detection, dashboards | Free up to 1M events/mo (https://posthog.com/pricing) |
| Loops | Automated follow-up sequences | $49/mo (https://loops.so/pricing) |
| n8n | Optimization loop orchestration, follow-up automation | Self-hosted free; Cloud from $24/mo (https://n8n.io/pricing) |
| Anthropic API | Hypothesis generation and experiment evaluation | Usage-based, ~$5-15/mo at this volume (https://www.anthropic.com/pricing) |
| Fireflies | Meeting transcription | Pro: $10/user/mo annual (https://fireflies.ai/pricing) |

**Play-specific cost at Durable level:** ~$600-700/mo (Clay Growth + Loops + Anthropic API compute). PostHog, Cal.com, and n8n on free/self-hosted tiers. Plus travel costs, which should be optimized by the scouting intelligence to maximize ROI.

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate loop that makes Durable fundamentally different; detects metric anomalies, generates hypotheses, runs A/B tests, auto-implements winners
- `hallway-demo-performance-monitor` — real-time dashboard, weekly reports, event ROI comparison, and trend analysis
- `event-scouting` — continuous scouting with learning feedback from actual event outcomes

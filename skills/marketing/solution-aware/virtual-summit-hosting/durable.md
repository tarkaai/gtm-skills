---
name: virtual-summit-hosting-durable
description: >
  Virtual Summit Hosting — Durable Intelligence. Always-on AI agents monitor
  summit series health, detect anomalies, generate improvement hypotheses, run
  A/B experiments, and auto-implement winners. Finds and maintains the local
  maximum for registration, attendance, engagement, and lead conversion.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Content, Email"
level: "Durable Intelligence"
time: "200 hours over 12 months"
outcome: "Sustained lead generation (≥30 qualified leads per summit) over 12 months via AI-optimized themes, speakers, promotion, and conversion paths"
kpis: ["Sustained qualified leads per summit", "AI experiment win rate", "Convergence velocity (summits to local maximum)", "Cost per qualified lead trend", "Funnel anomaly detection latency"]
slug: "virtual-summit-hosting"
install: "npx gtm-skills add marketing/solution-aware/virtual-summit-hosting"
drills:
  - autonomous-optimization
---

# Virtual Summit Hosting — Durable Intelligence

> **Stage:** Marketing → SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Content, Email

## Outcomes

Deploy always-on AI agents that autonomously monitor summit series health, detect metric anomalies, generate hypotheses for improvement, run controlled experiments, and auto-implement winners. The system finds the local maximum — the best achievable performance given your market, audience, and competitive landscape — and maintains it as conditions change. Pass threshold: sustained ≥30 qualified leads per summit for 4 consecutive quarterly summits (12 months).

## Leading Indicators

- Autonomous optimization loop running with ≥1 experiment completed per summit cycle
- Anomaly detection latency <24 hours during promotion windows; <2 hours post-summit (metric drops surfaced quickly)
- Experiment win rate ≥30% (at least 1 in 3 experiments produces measurable improvement)
- Weekly optimization briefs generated without manual prompting during active summit cycles
- Convergence signal: successive experiments produce <2% improvement for 3 consecutive cycles (local maximum reached)
- Speaker pipeline auto-refills without manual intervention based on performance data from previous summits

## Instructions

### 1. Deploy the summit performance monitor

Run the `autonomous-optimization` drill. This builds the always-on monitoring layer that watches every part of the summit funnel and surfaces problems before they compound.

**Metric categories the monitor tracks:**

- **Demand metrics**: Registration rate, registrations per summit, promotion channel yield, registration velocity, speaker pull
- **Commitment metrics**: Show rate, multi-session rate, full-day rate, session drop-off curve
- **Engagement metrics**: Questions per session, poll participation, CTA click rate, chat activity
- **Conversion metrics**: Nurture reply rate by tier, meeting booking rate by tier, recording consumption rate, replay-to-meeting conversion
- **Pipeline metrics**: Deals created (30-day attribution), average deal value, summit-to-close rate (90-day window), revenue per summit (180-day attribution)
- **Series health metrics**: Repeat attendee rate, list growth rate, theme saturation index, speaker pipeline health, sponsor retention rate

**Monitoring cadence:**

- **During promotion window (daily via n8n cron)**: Registration velocity checks. Alert if daily registrations drop >40% from 7-day average or if a primary channel goes silent.
- **Post-summit immediate (2 hours)**: Show rate, multi-session rate, and engagement checks. Alert if critically below target.
- **Post-nurture (48 hours)**: Follow-up email performance. Alert if open rate or Tier 1 reply rate below threshold.
- **Monthly (n8n cron)**: Compare the last summit to the 3-summit rolling average. Flag any metric declining >15%.
- **Quarterly**: Generate a series-level report with aggregate trends, top/bottom performing summits, speaker ROI rankings, and series health classification (GREEN/YELLOW/RED).

The monitor also generates structured post-mortems 21 days after each summit: all metrics vs targets, speaker performance, what worked, what needs attention, and specific recommendations for the next summit.

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill. This is the core system that makes Durable fundamentally different from Scalable. It creates a closed-loop cycle:

**Phase 1 — Monitor (daily during active summit cycles, weekly between summits):**
Use `posthog-anomaly-detection` to check primary KPIs against a 3-summit rolling average. Classify status: **normal** (within +/-10%), **plateau** (+/-2% for 2+ summits), **drop** (>20% decline), **spike** (>50% increase). Normal → log to Attio. Anomaly → trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
Gather context: current series configuration (upcoming theme, speaker lineup, promotion channels, nurture sequences) from Attio. Pull 4-summit metric history from PostHog. Run `hypothesis-generation` with anomaly data + context. Receive 3 ranked hypotheses with expected impact and risk. Store in Attio. If top hypothesis is high-risk → send alert for human review and STOP. If low/medium risk → proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Design the experiment using `posthog-experiments`: create a feature flag that splits the variable between control and variant. For summit-specific experiments, the variables include:

- **Theme framing**: Same core topic, different positioning and title
- **Promotion email copy**: Subject lines, body structure, CTA language, send cadence
- **Promotion timing**: Adjust the 8-week cadence (compress to 6 weeks, or extend earlier notice)
- **Speaker lineup composition**: Customer-heavy vs expert-heavy vs mixed
- **Registration page**: Headline, agenda presentation, social proof elements, form length
- **Session format mix**: More panels vs more workshops vs more lightning talks
- **Nurture sequence**: Different email count, timing, personalization depth, or Loom video usage
- **Summit timing**: Day of week, start time, total duration

Set experiment duration: minimum 2 summits for summit-level variables (to control for theme variability). For email or page-level tests, run within a single summit's promotion window. Log experiment start in Attio.

**Phase 4 — Evaluate (triggered by experiment completion):**
Pull results from PostHog. Run `experiment-evaluation`:
- **Adopt**: Implement the winning variant as the new default. Log the change.
- **Iterate**: Generate a refined hypothesis building on this result. Return to Phase 2.
- **Revert**: Disable the variant. Log the failure. Return to Phase 1.
- **Extend**: Keep running for another summit cycle if sample size is insufficient.

Store the full evaluation (decision, confidence, reasoning) in Attio.

**Phase 5 — Report (weekly during active summit cycles, monthly between summits):**
Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments running, decisions made. Calculate net metric change from adopted changes. Generate a weekly optimization brief:
- What changed and why
- Net impact on primary KPIs (registrations, show rate, multi-session rate, qualified leads)
- Current distance from estimated local maximum
- Recommended focus for next summit cycle

Post to Slack and store in Attio.

### 3. Configure summit-specific optimization guardrails

The `autonomous-optimization` drill includes generic guardrails. Add these summit-specific guardrails:

- **Rate limit**: Maximum 1 active experiment per summit variable at a time. Never test theme framing AND promotion timing simultaneously — results become unattributable.
- **Revert threshold**: If show rate drops >30% or qualified leads drop >40% compared to the 3-summit average, auto-revert the active experiment immediately.
- **Human approval required for:**
  - Changing the summit cadence (quarterly → bi-annual or more frequent)
  - Adding paid promotion channels (paid ads, paid newsletter placements)
  - Fundamentally changing the summit format (half-day → full-day, virtual → hybrid)
  - Any budget increase >25%
  - Speaker outreach to people outside the auto-generated prospect list
- **Cooldown**: After a failed experiment, wait 1 full summit cycle before testing the same variable again.
- **Annual cap**: Maximum 8 experiments per year (2 per quarter). If 4 consecutive experiments fail, pause optimization and flag for human strategic review.
- **Theme saturation protection**: If the performance monitor detects declining registrations for similar themes, block the optimization loop from re-testing theme variations and instead flag "audience fatigue — need fundamentally new content direction" for human review.
- **Speaker relationship protection**: Never auto-decline or auto-reject a previously confirmed speaker based on optimization data alone. Flag underperforming speakers for human review instead.

### 4. Detect and respond to convergence

The optimization loop runs indefinitely, but the agent must detect **convergence** — when the summit series has reached its local maximum. Convergence criteria:

- 3 consecutive experiments produce <2% improvement on the primary metric
- All major variables (theme framing, promotion, nurture, format, speaker composition) have been tested at least once
- Qualified leads per summit have been within +/-5% of the same level for 3+ consecutive summits

**At convergence:**
1. Reduce monitoring frequency: daily → weekly during promotion windows; post-summit checks remain unchanged
2. Reduce experimentation to 1 test per 2 summit cycles (maintenance mode)
3. Generate a convergence report: current performance (all metrics), tested variables and their outcomes, the optimal configuration, and what strategic changes (new audience segments, new summit format, hybrid events, new product capabilities) would be needed for the next step-change improvement
4. Post the report to Slack and store in Attio

**Breaking out of convergence:** If an external change occurs (competitor launches a summit series, market event shifts audience interest, product launches a major new feature, new regulation creates urgency), the monitor will detect the metric shift and re-activate the full optimization loop.

### 5. Evaluate sustainability

Measure against threshold quarterly. The play is durable when:

- ≥30 qualified leads per summit sustained for 4 consecutive quarterly summits (12 months)
- Optimization loop running autonomously with ≥1 experiment per summit cycle
- Weekly briefs generated without human prompting during active summit cycles
- Anomalies detected and addressed within 24 hours during promotion windows
- Cost per qualified lead is flat or declining over the 12-month period
- Speaker pipeline self-replenishes based on performance data and theme requirements
- Post-summit nurture runs automatically with tier-based segmentation and personalized follow-up

**This level runs continuously.** Quarterly review: what experiments won, what was reverted, what the agent recommends testing next, and whether convergence has been reached.

## Time Estimate

- Performance monitor setup: 10 hours
- Autonomous optimization configuration: 14 hours
- Guardrail setup and testing: 4 hours
- Quarterly human review and strategic direction (x4): 6 hours x 4 = 24 hours
- Per-summit human moderation (x4 summits over 12 months): 4 hours x 4 = 16 hours
- Speaker prep calls and editorial decisions (x4): 4 hours x 4 = 16 hours
- Ongoing automation maintenance: 8 hours/quarter x 4 = 32 hours
- Convergence analysis and reporting: 8 hours
- Agent compute time (always-on monitoring + experimentation): ~50 hours cumulative

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel analytics, anomaly detection, experiments | Free up to 1M events; $0 for feature flags — https://posthog.com/pricing |
| n8n | Automation orchestration (monitoring crons, experiment triggers, reporting) | $20/mo (cloud Starter) or free self-hosted — https://n8n.io/pricing |
| Anthropic Claude API | Hypothesis generation + experiment evaluation + optimization briefs | ~$30-60/mo depending on experiment volume — https://www.anthropic.com/pricing |
| Riverside | Summit hosting and recording | $24/mo (Business) — https://riverside.fm/pricing |
| Clay | Ongoing speaker sourcing and prospect enrichment | $149/mo (Explorer) — https://clay.com/pricing |
| Loops | Email sequences + broadcasts | $49/mo (Growth) — https://loops.so/pricing |
| Attio | CRM + optimization audit trail | Free up to 3 seats — https://attio.com/pricing |
| Loom | Personalized follow-up videos for Tier 1 attendees | $15/mo (Business) — https://www.loom.com/pricing |
| Descript | Session recording repurposing into clips | $33/mo (Hobbyist) — https://www.descript.com/pricing |

**Estimated play-specific cost: $320-470/mo** (Clay + Riverside + n8n + Loops + Loom + Descript + Claude API)

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: monitor metrics → detect anomalies → generate hypotheses → run experiments → evaluate results → auto-implement winners. Runs the always-on cycle that finds the local maximum for the summit series.
- `autonomous-optimization` — the always-on monitoring layer: tracks 6 metric categories across the summit funnel, generates post-summit post-mortems, detects anomalies, and produces quarterly series health reports. Feeds data to the autonomous optimization loop.

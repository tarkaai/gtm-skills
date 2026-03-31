---
name: webinar-series-program-durable
description: >
  Educational Webinar Series — Durable Intelligence. Always-on AI agents monitor
  webinar funnel health, detect anomalies, generate improvement hypotheses, run
  A/B experiments, and auto-implement winners. Finds and maintains the local
  maximum for registration, attendance, and lead conversion.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Content, Email"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained lead generation (≥40 qualified leads/month) over 12 months via AI-optimized topics, promotion, and conversion paths"
kpis: ["Sustained monthly qualified leads", "AI experiment win rate", "Convergence velocity (weeks to local maximum)", "Cost per qualified lead trend", "Funnel anomaly detection latency"]
slug: "webinar-series-program"
install: "npx gtm-skills add marketing/solution-aware/webinar-series-program"
drills:
  - autonomous-optimization
  - webinar-performance-monitor
---

# Educational Webinar Series — Durable Intelligence

> **Stage:** Marketing → SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Content, Email

## Outcomes

Deploy always-on AI agents that autonomously monitor webinar series health, detect metric anomalies, generate hypotheses for improvement, run controlled experiments, and auto-implement winners. The system finds the local maximum — the best achievable performance given your market, audience, and competitive landscape — and maintains it as conditions change. Pass threshold: sustained ≥40 qualified leads/month for 12 consecutive months.

## Leading Indicators

- Autonomous optimization loop running with ≥1 experiment completed per month
- Anomaly detection latency <24 hours (metric drops are surfaced within one day)
- Experiment win rate ≥30% (at least 1 in 3 experiments produces measurable improvement)
- Weekly optimization briefs generated without manual prompting
- Convergence signal: successive experiments produce <2% improvement for 3 consecutive cycles (local maximum reached)

## Instructions

### 1. Deploy the webinar performance monitor

Run the `webinar-performance-monitor` drill. This builds the always-on monitoring layer that watches every part of the webinar funnel and surfaces problems before they compound.

**Metric categories the monitor tracks:**

- **Demand metrics**: Registration rate, registrations per event, promotion channel yield, registration velocity
- **Commitment metrics**: Show rate, drop-off rate, engagement rate (questions + polls + CTA clicks)
- **Conversion metrics**: Nurture reply rate by tier, meeting booking rate, recording consumption rate
- **Pipeline metrics**: Deals created (30-day attribution), average deal value, webinar-to-close rate (90-day window)
- **Series health metrics**: Repeat attendance rate, list growth rate, topic saturation index

**Monitoring cadence:**

- **Post-event immediate (2 hours)**: Show rate and engagement rate checks. Alert if critically below target.
- **Post-nurture (48 hours)**: Follow-up email performance. Alert if open rate or reply rate below threshold.
- **Weekly (n8n cron)**: Compare last event to 4-event rolling average. Flag any metric declining >15%.
- **Monthly**: Generate a series-level report with aggregate trends, top/bottom performing events, and series health classification (GREEN/YELLOW/RED).

The monitor also generates structured post-mortems 14 days after each event: metrics vs targets, what worked, what needs attention, and specific recommendations for the next event.

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill. This is the core system that makes Durable fundamentally different from Scalable. It creates a closed-loop cycle:

**Phase 1 — Monitor (daily via n8n cron):**
Use `posthog-anomaly-detection` to check primary KPIs against a 4-week rolling average. Classify status: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase). Normal → log to Attio. Anomaly → trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
Gather context: current series configuration (topics, timing, promotion channels, nurture sequences) from Attio. Pull 8-week metric history from PostHog. Run `hypothesis-generation` with anomaly data + context. Receive 3 ranked hypotheses with expected impact and risk. Store in Attio. If top hypothesis is high-risk → send alert for human review and STOP. If low/medium risk → proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Design the experiment using `posthog-experiments`: create a feature flag that splits the variable between control and variant. For webinar-specific experiments, the variables include:

- **Topic framing**: Same content, different title/positioning
- **Promotion email copy**: Subject line, body structure, CTA language
- **Promotion timing**: Change the email send schedule (Day -14 vs Day -10)
- **Nurture sequence**: Different email count, timing, or personalization level
- **Event format**: Presentation vs workshop vs AMA vs panel
- **Registration page**: Headline, bullet points, social proof elements

Set experiment duration: minimum 2 events (to control for topic variability) or 7 days for email-level tests. Log experiment start in Attio.

**Phase 4 — Evaluate (triggered by experiment completion):**
Pull results from PostHog. Run `experiment-evaluation`:
- **Adopt**: Implement the winning variant as the new default. Log the change.
- **Iterate**: Generate a refined hypothesis. Return to Phase 2.
- **Revert**: Disable the variant. Log the failure. Return to Phase 1.
- **Extend**: Keep running for another cycle if sample size is insufficient.

Store the full evaluation (decision, confidence, reasoning) in Attio.

**Phase 5 — Report (weekly via n8n cron):**
Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments running, decisions made. Calculate net metric change from adopted changes. Generate a weekly optimization brief:
- What changed and why
- Net impact on primary KPIs (registrations, show rate, qualified leads)
- Current distance from estimated local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 3. Configure webinar-specific optimization guardrails

The `autonomous-optimization` drill includes generic guardrails. Add these webinar-specific guardrails:

- **Rate limit**: Maximum 1 active experiment per event variable at a time. Never test topic framing AND promotion copy simultaneously — results become unattributable.
- **Revert threshold**: If show rate drops >30% or qualified leads drop >40% during an experiment, auto-revert immediately.
- **Human approval required for**:
  - Changing the event cadence (bi-weekly → weekly or monthly)
  - Adding paid promotion channels
  - Changing the core event format (webinar → workshop)
  - Any budget increase >20%
- **Cooldown**: After a failed experiment, wait 2 events before testing the same variable again.
- **Monthly cap**: Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.
- **Topic saturation protection**: If the performance monitor detects declining registrations for similar topics, block the optimization loop from re-testing topic variations and instead flag "audience fatigue — need new content themes" for human review.

### 4. Detect and respond to convergence

The optimization loop runs indefinitely, but the agent must detect **convergence** — when the play has reached its local maximum. Convergence criteria:

- 3 consecutive experiments produce <2% improvement on the primary metric
- All major variables (topic framing, promotion, nurture, format) have been tested at least twice
- Monthly qualified leads have been within ±5% of the same level for 3+ months

**At convergence:**
1. Reduce monitoring frequency from post-event to weekly
2. Reduce experimentation to 1 test per month (maintenance mode)
3. Generate a convergence report: current performance (all metrics), tested variables and their outcomes, the optimal configuration, and what strategic changes (new audience segments, new channels, product changes) would be needed for the next step-change improvement
4. Post the report to Slack and store in Attio

**Breaking out of convergence**: If an external change occurs (competitor launches a webinar series, market event shifts audience interest, product launches a new feature), the monitor will detect the metric shift and re-activate the full optimization loop.

### 5. Evaluate sustainability

Measure against threshold monthly. The play is durable when:

- ≥40 qualified leads/month sustained for 12 consecutive months
- Optimization loop running autonomously with ≥1 experiment per month
- Weekly briefs generated without human prompting
- Anomalies detected and addressed within 48 hours
- Cost per qualified lead is flat or declining over the 12-month period

**This level runs continuously.** Monthly review: what experiments won, what was reverted, what the agent recommends testing next, and whether convergence has been reached.

## Time Estimate

- Performance monitor setup: 8 hours
- Autonomous optimization configuration: 12 hours
- Guardrail setup and testing: 4 hours
- Monthly human review and strategic direction (×12): 4 hours × 12 = 48 hours
- Per-event manual delivery (×24 events over 12 months): 1.5 hours × 24 = 36 hours
- Ongoing automation maintenance: 6 hours/quarter × 4 = 24 hours
- Convergence analysis and reporting: 8 hours
- Agent compute time (always-on monitoring + experimentation): ~40 hours cumulative

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel analytics, anomaly detection, experiments | Free up to 1M events; $0 for feature flags — https://posthog.com/pricing |
| n8n | Automation orchestration (monitoring crons, experiment triggers, reporting) | $20/mo (cloud Starter) or free self-hosted — https://n8n.io/pricing |
| Anthropic Claude API | Hypothesis generation + experiment evaluation + optimization briefs | ~$20-50/mo depending on experiment volume — https://www.anthropic.com/pricing |
| Riverside | Webinar recording + production | ~$25/mo (Standard) — https://riverside.fm/pricing |
| Clay | Ongoing prospect discovery | $149/mo (Explorer) — https://clay.com/pricing |
| Loops | Email sequences + broadcasts | $49/mo — https://loops.so/pricing |
| Attio | CRM + optimization audit trail | Free up to 3 seats — https://attio.com/pricing |
| Loom | Personalized follow-up videos | $15/mo (Business) — https://www.loom.com/pricing |
| Descript | Recording repurposing into clips | $33/mo (Hobbyist) — https://www.descript.com/pricing |

**Estimated play-specific cost: $310-440/mo** (Clay + Riverside + n8n + Loops + Loom + Descript + Claude API)

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: monitor metrics → detect anomalies → generate hypotheses → run experiments → evaluate results → auto-implement winners. Runs the always-on cycle that finds the local maximum.
- `webinar-performance-monitor` — the always-on monitoring layer: tracks 5 metric categories across the webinar funnel, generates post-event post-mortems, detects anomalies, and produces monthly series health reports. Feeds data to the autonomous optimization loop.

---
name: onboarding-webinar-series-durable
description: >
  Live Onboarding Webinars — Durable Intelligence. Always-on AI agents autonomously
  optimize the webinar series: detect metric anomalies, generate improvement hypotheses,
  run A/B experiments on promotion timing/topics/nurture sequences, evaluate results,
  and auto-implement winners. Weekly optimization briefs. Converges at local maximum.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product, Email, Events"
level: "Durable Intelligence"
time: "Ongoing — 4 hours/month agent maintenance + human webinar delivery"
outcome: "Sustained attendee activation >=50% and show rate >=35% over 6 months with autonomous optimization finding and maintaining the local maximum"
kpis: ["Attendee activation rate (6-month trend)", "Show rate (6-month trend)", "Experiment velocity (experiments per month)", "Net metric lift from adopted experiments", "Meetings booked per month", "Time to convergence"]
slug: "onboarding-webinar-series"
install: "npx gtm-skills add product/onboard/onboarding-webinar-series"
drills:
  - autonomous-optimization
  - webinar-performance-monitor
---

# Live Onboarding Webinars — Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Events

## Outcomes

The webinar series runs as a self-optimizing system. The `autonomous-optimization` drill creates the always-on loop: monitor webinar metrics -> detect anomalies -> generate hypotheses -> design and run experiments -> evaluate results -> auto-implement winners. The `webinar-performance-monitor` drill feeds the anomaly signals. The agent finds the local maximum — the best possible performance given current audience, content, and market conditions — and maintains it as conditions change. Pass threshold: sustained attendee activation >=50% and show rate >=35% over 6 months, with the optimization loop producing measurable improvements until convergence (<2% improvement for 3 consecutive experiments).

## Leading Indicators

- The optimization loop completes its first full cycle (detect -> diagnose -> experiment -> evaluate -> decide) within the first 2 weeks — confirms the system is operational
- At least 1 experiment adopted (winner implemented) within the first month — confirms the loop produces actionable results
- Weekly optimization briefs generated and posted to Slack on schedule — confirms the reporting pipeline is reliable
- No metric drops >20% sustained for more than 2 weeks without an automatic experiment being triggered — confirms the monitoring-to-action pipeline has no gaps
- After 3 months, the series shows measurable improvement in at least 1 primary KPI (activation rate, show rate, or meetings booked) compared to the Scalable baseline

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill with the webinar series as the target play. Configure the loop with webinar-specific parameters:

**Monitoring configuration (Phase 1 — runs daily via n8n cron):**

The `webinar-performance-monitor` drill (already running from Scalable) provides the anomaly detection signals. Connect its output to the optimization loop:

| Metric | Normal Range | Anomaly Trigger |
|--------|-------------|-----------------|
| Show rate per event | Within ±10% of 4-event rolling avg | >15% decline from rolling avg |
| Attendee activation rate | Within ±10% of 4-event rolling avg | >15% decline from rolling avg |
| Registration rate (invites -> registrations) | Within ±15% of 4-event rolling avg | >20% decline for 2 consecutive events |
| Tier 1 nurture reply rate | Within ±15% of 4-event rolling avg | >25% decline from rolling avg |
| Meetings booked per event | Within ±20% of 4-event rolling avg | >30% decline from rolling avg |
| Repeat attendance rate | >=10% | Drops below 8% |
| Topic saturation index | Flat or improving registration per topic | Declining registration for similar topics 3x in a row |

When the monitor classifies a metric as anomaly (plateau, drop, or spike), it triggers Phase 2.

**Diagnosis configuration (Phase 2 — triggered by anomaly):**

When an anomaly is detected, the agent gathers context and generates hypotheses. The hypothesis space for webinar series optimization includes:

| Anomaly Type | Hypothesis Categories |
|-------------|----------------------|
| Show rate decline | Reminder timing, reminder copy, event time slot, event day of week, join link friction |
| Activation rate decline | Topic-to-activation alignment, workshop pacing, Q&A time allocation, post-webinar CTA clarity |
| Registration decline | Subject line fatigue, invite frequency, topic relevance, promotion channel mix, audience saturation |
| Nurture reply rate decline | Email copy freshness, personalization depth, CTA specificity, send timing, tier segmentation accuracy |
| Meetings decline | CTA in nurture emails, Cal.com booking friction, follow-up timing, Tier 1 identification accuracy |
| Repeat attendance drop | Topic variety, schedule predictability, value delivered in prior sessions |
| Topic saturation | Content freshness, topic rotation speed, audience growth rate vs topic backlog |

The agent runs `hypothesis-generation` with the anomaly data, metric history, and current series configuration from Attio. It receives 3 ranked hypotheses with expected impact and risk level.

**High-risk hypotheses require human approval:** Any hypothesis that would change the webinar format (e.g., switching from workshop to panel), reduce frequency (e.g., going from 4/month to 2/month), or fundamentally alter the activation workflow being taught.

**Experiment configuration (Phase 3):**

For each accepted hypothesis, the agent designs an experiment. Webinar-specific experiment types:

| Variable | How to A/B Test |
|----------|----------------|
| Reminder timing | Split registrants: Group A gets reminders at current timing, Group B gets the new timing. Compare show rates. |
| Invitation subject line | A/B test in Loops: send 50% of invitees each subject line. Compare registration rate. |
| Webinar time slot | Alternate between time slots across consecutive events. Compare show rate. (Cannot A/B in a single event.) |
| Nurture email copy | A/B test in Loops sequence: split Tier 1 attendees between current and new follow-up copy. Compare reply rate. |
| Topic sequencing | Test different topic orders month-over-month. Compare registration and activation per topic position. |
| Promotion channel mix | Shift 30% of promotion budget/effort from worst-performing channel to best-performing. Compare overall registrations. |
| In-app banner copy | Use PostHog feature flags to A/B test banner text. Compare click-to-register rate. |
| Post-webinar CTA | A/B test in follow-up emails: different CTA (book a call vs complete the activation action vs watch a Loom). Compare conversion. |

Use `posthog-experiments` to create feature flags for in-app experiments. Use Loops A/B testing for email experiments. For cross-event experiments (time slot, topic order), use consecutive events as test and control.

Minimum experiment duration: 2 events (for per-event variables) or 7 days and 100 samples per variant (for email/in-app variables).

**Evaluation configuration (Phase 4):**

The agent runs `experiment-evaluation` with the experiment results:
- **Adopt:** Winning variant implemented permanently. The agent updates the n8n workflows, Loops sequences, or PostHog feature flags to use the winner. Log the change in Attio.
- **Iterate:** Result was inconclusive or partial. Generate a refined hypothesis building on the signal. Return to Phase 2.
- **Revert:** Variant performed worse. Restore the control. Log the failure. Return to Phase 1 monitoring.
- **Extend:** Not enough data yet. Continue the experiment for 1 more cycle.

**Reporting configuration (Phase 5 — runs weekly via n8n cron):**

The agent generates a weekly optimization brief:

```
## Webinar Series Optimization Brief — Week of [date]

### Experiments This Week
- [Experiment name]: [Status: running / adopted / reverted / extended]
  - Hypothesis: [one sentence]
  - Result: [control: X%, variant: Y%, delta: Z%]
  - Decision: [Adopt / Iterate / Revert / Extend]

### Adopted Changes
- [Change description]: [metric before -> after, % lift]

### Active Monitoring
- Show rate: [current] vs [target] — [status: normal / watch / alert]
- Activation rate: [current] vs [target] — [status]
- Meetings booked: [current] vs [target] — [status]

### Convergence Status
- Experiments run to date: [N]
- Last 3 experiment results: [+X%, +Y%, +Z%]
- Convergence assessment: [Not yet / Approaching / Converged]
  - [If converged: "Series has reached local maximum. Current performance: [metrics].
    Further gains require strategic changes (new audience segments, product changes,
    or format innovation) rather than tactical optimization."]

### Recommendations
- [If not converged: next hypothesis to test]
- [If converged: strategic suggestions for breaking past the local maximum]
```

Post to Slack and store in Attio.

### 2. Configure webinar-specific monitoring at Durable level

The `webinar-performance-monitor` drill should already be running from Scalable. At Durable level, extend it:

**Add series health metrics:**
- Optimization loop health: is the daily monitor running? Are experiments being created and evaluated on schedule?
- Cumulative lift: total metric improvement from all adopted experiments since Durable started
- Experiment success rate: % of experiments that resulted in "Adopt" decisions
- Days since last experiment: if >21 days with no experiment, flag for review (the loop may have stalled)

**Add convergence detection:**
Track the improvement from each adopted experiment. When 3 consecutive adopted experiments each produce <2% improvement on any primary KPI, classify that KPI as converged. When all primary KPIs (activation rate, show rate, meetings booked) are converged:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency from 2-4/month to 1/month (maintenance mode)
3. Generate a convergence report documenting the local maximum and what would need to change for further improvement

### 3. Maintain the series operation

**Human action required:** Continue delivering 4+ webinars per month. The agent handles everything else autonomously.

The agent's ongoing responsibilities:
- Daily: monitor metrics, detect anomalies
- Per event: automated promotion, registration, recording, nurture
- Weekly: optimization brief generation and posting
- Per experiment cycle: hypothesis generation, experiment design, evaluation, implementation
- Monthly: series-level performance report, content calendar refresh

The human's ongoing responsibilities:
- Deliver webinar content (30-45 min per session)
- Approve high-risk experiments when flagged
- Review the weekly optimization brief (5 min)
- Quarterly strategic review: should the series expand to new audience segments, add new formats, or adjust the activation workflow?

### 4. Guardrails

The `autonomous-optimization` drill's standard guardrails apply. Webinar-specific additions:

- **Never reduce webinar frequency below 2/month** without human approval. The series builds momentum through consistency.
- **Never change the core activation workflow taught in workshops** without human approval. The product team must validate any change to what constitutes the activation action.
- **If attendee activation rate drops below 40% for 2 consecutive events**, pause all experiments and revert to the last known-good configuration. Alert the human for strategic review.
- **Maximum 1 active experiment per variable per event.** Never stack experiments (e.g., testing both reminder timing AND subject line simultaneously).
- **Cooldown after revert:** 2 events (not just calendar days) before testing the same variable again.

### 5. Evaluate sustainability

Pass criteria at Durable level — measured over rolling 6-month windows:

| Metric | Sustained Target |
|--------|-----------------|
| Attendee activation rate | >=50% (6-month average) |
| Show rate | >=35% (6-month average) |
| Meetings booked per month | >=8 (6-month average) |
| Optimization loop uptime | >=95% (no gaps >3 days) |
| Experiments run | >=2 per month until convergence |
| Experiment success rate | >=25% (at least 1 in 4 experiments should produce an improvement) |

This level runs continuously. The play is durable when:
1. Metrics sustain at or above targets for 6+ months
2. The optimization loop has either converged (found the local maximum) or continues to produce improvements
3. No human intervention was required to maintain performance (only to deliver content and approve high-risk changes)

## Time Estimate

**Setup (one-time):**
- 3 hours: Configure the autonomous-optimization drill with webinar-specific parameters
- 2 hours: Extend webinar-performance-monitor with convergence detection and loop health metrics
- 1 hour: Set up the weekly brief generation and Slack posting

**Ongoing (monthly):**
- 4-5 hours: Deliver 4+ webinars (human action)
- 1 hour: Review weekly briefs, approve/reject flagged experiments (human action)
- 0 hours: Agent runs autonomously for monitoring, experimentation, and reporting

Total setup: ~6 hours. Ongoing: ~5-6 hours/month human time.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Promotional emails, reminders, nurture sequences, A/B testing | $49/mo (5,000 contacts). [Pricing](https://loops.so/pricing) |
| PostHog | Full-funnel tracking, experiments (feature flags), anomaly detection, dashboards | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |
| Riverside | Weekly webinar recording | Standard: $19/mo or Pro: $29/mo. [Pricing](https://riverside.com/pricing) |
| Cal.com | Registration pages, follow-up meeting booking | Free for 1 user. [Pricing](https://cal.com/pricing) |
| Intercom | In-app webinar promotion, A/B testable banners | Essential: $29/seat/mo. [Pricing](https://www.intercom.com/pricing) |
| Clay | Net-new prospect enrichment | Launch: $185/mo. [Pricing](https://clay.com/pricing) |
| Loom | Short clips for no-show follow-up | Free or Business: $12.50/user/mo. [Pricing](https://www.loom.com/pricing) |
| Anthropic API | Hypothesis generation and experiment evaluation via Claude | Usage-based. ~$5-20/mo at this experiment velocity. [Pricing](https://www.anthropic.com/pricing) |

**Estimated monthly cost: $290-370/mo** (Loops $49 + Riverside $19-29 + Clay $185 + Intercom $29 + Anthropic ~$10. PostHog, Cal.com, and Loom free tiers likely sufficient.)

## Drills Referenced

- `autonomous-optimization` — the core Durable-level drill: detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results, auto-implement winners, and generate weekly optimization briefs until convergence at the local maximum
- `webinar-performance-monitor` — feeds anomaly signals to the optimization loop; generates per-event post-mortems, series health dashboards, and convergence detection

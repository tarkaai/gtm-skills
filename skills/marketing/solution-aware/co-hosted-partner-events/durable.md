---
name: co-hosted-partner-events-durable
description: >
  Co-hosted Partner Events — Durable Intelligence. Always-on AI agents
  continuously optimize event performance by detecting metric anomalies,
  generating hypotheses, running experiments on format/topic/promotion/partner
  mix, evaluating results, and auto-implementing winners. Converges when
  successive experiments produce <2% improvement.
stage: "Marketing > SolutionAware"
motion: "PartnershipsWarmIntros"
channels: "Events"
level: "Durable Intelligence"
time: "120 hours over 12 months"
outcome: "Sustained ≥50 qualified leads/quarter with declining cost per lead over 12 months via autonomous event optimization"
kpis: ["Qualified leads per quarter", "Cost per qualified lead trend", "Experiment win rate", "Partner portfolio ROI", "Convergence distance"]
slug: "co-hosted-partner-events"
install: "npx gtm-skills add marketing/solution-aware/co-hosted-partner-events"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Co-hosted Partner Events — Durable Intelligence

> **Stage:** Marketing → SolutionAware | **Motion:** PartnershipsWarmIntros | **Channels:** Events

## Outcomes

The event engine runs on autopilot. AI agents monitor every metric in the event funnel, detect when performance plateaus or drops, generate hypotheses for improvement, design and run experiments, evaluate results, and auto-implement winners. The goal is to find the local maximum — the best possible event performance given the current market, audience, and partner ecosystem — and maintain it as conditions change. Pass threshold: sustained ≥50 qualified leads per quarter with cost per lead stable or declining over 12 months.

## Leading Indicators

- Autonomous optimization loop running daily (monitoring) and weekly (reporting)
- ≥1 experiment running at all times (never idle between experiments)
- Experiment win rate ≥30% (at least 1 in 3 experiments produces measurable improvement)
- No manual intervention required for routine event operations for 4+ consecutive weeks
- Cost per qualified lead declining quarter-over-quarter
- Convergence detection: successive experiments producing <2% improvement signals the local maximum

## Instructions

### 1. Build comprehensive event dashboards

Run the `dashboard-builder` drill to create the master event intelligence dashboard in PostHog. This dashboard serves as the single source of truth for the optimization loop. Required panels:

**Event funnel (per event and aggregate):**
- Registration → Attendance → Engagement → Follow-up Reply → Meeting Booked → Deal Created
- Segmented by: partner, event format, event topic, promotion channel

**Partner portfolio view:**
- Per-partner: events co-hosted, total attendees sourced, total pipeline generated, average attendee-to-lead conversion, partner health score
- Partner ROI: pipeline value attributed to each partner vs cost of managing the partnership

**Trend analysis (12-month rolling):**
- Monthly qualified leads from events (target: stable or growing)
- Monthly cost per qualified lead (target: declining)
- Monthly attendance rate (target: stable ≥55%)
- Monthly experiment impact: net metric change from adopted experiments

**Experiment tracker:**
- Active experiments: what is being tested, control vs variant, sample size, expected completion
- Completed experiments: hypothesis, result, decision (adopt/iterate/revert), net impact
- Experiment pipeline: queued hypotheses ranked by expected impact

### 2. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the co-hosted events play. The loop operates across these optimization surfaces:

**Event format optimization:**
- Variables: format (webinar, workshop, roundtable, AMA, dinner), duration, speaker count, Q&A allocation
- Metric: attendee-to-meeting conversion rate
- Experiment method: alternate formats across consecutive events with same partner and topic category

**Topic optimization:**
- Variables: topic angle (pain-focused vs aspiration-focused), specificity (narrow use case vs broad industry), freshness (trending topic vs evergreen)
- Metric: registration count and attendance rate
- Experiment method: test topic variants with similar partners and promotion effort

**Promotion optimization:**
- Variables: email count, send timing, subject line angle, social post count, direct invite count, promotion start date (weeks before event)
- Metric: registrations per promotion impression
- Experiment method: use PostHog feature flags to A/B test email subject lines and CTA copy; vary promotion cadence across events

**Follow-up optimization:**
- Variables: follow-up timing (same day vs next day vs 48 hours), message angle (reference question vs share resource vs direct ask), channel (email vs LinkedIn vs both)
- Metric: follow-up reply rate and meeting booking rate
- Experiment method: A/B test follow-up variants within each event's attendee pool

**Partner mix optimization:**
- Variables: partner selection, co-host frequency, partner promotion intensity, lead-sharing model
- Metric: qualified leads per event and partner satisfaction
- Experiment method: rotate partner pairings and measure which combinations produce the highest joint pipeline

The optimization loop runs on this cadence:
- **Daily:** Monitor event funnel metrics in PostHog. Detect anomalies (registration drop-off, attendance decline, follow-up non-response spike). If anomaly detected, trigger diagnosis.
- **Per-event:** After each event, evaluate the active experiment. Compare variant performance to control. Decision: adopt (update the default), iterate (refine the hypothesis), or revert (restore previous approach).
- **Weekly:** Generate the optimization brief (see step 3). Queue the next experiment if no experiment is active.
- **Monthly:** Review the full experiment history. Calculate cumulative improvement from all adopted changes. Assess convergence.

### 3. Configure play-specific reporting

Run the `autonomous-optimization` drill to build the monitoring layer that feeds the optimization loop:

**Weekly event optimization brief (generated every Monday via n8n):**
```
## Co-Hosted Events Optimization Brief — Week of {date}

**Performance snapshot**
- Events this month: {count} ({attendees} attendees, {leads} qualified leads)
- vs last month: {change_pct}% leads, {change_pct}% cost per lead
- Active experiment: {description} (Day {n} of {total}, {sample_size} samples)

**Anomalies detected**
- {anomaly_1}: {description} — auto-diagnosed: {hypothesis}
- {anomaly_2}: {description} — flagged for human review (high risk)

**Experiment results (last 7 days)**
- {experiment_name}: {variant} outperformed control by {pct}% ({confidence}% confidence)
  → Decision: {adopt/iterate/revert/extend}
  → Net impact: {metric} improved from {old} to {new}

**Partner portfolio health**
- Top partner: {partner} ({score}/50, {leads} leads this quarter)
- At-risk partner: {partner} (score declined {pct}%, {reason})
- New partner onboarded: {partner} (first event scheduled {date})

**Convergence status**
- Last 3 experiments produced {avg_improvement}% average improvement
- Estimated distance from local maximum: {assessment}
- {Recommendation: continue experimenting / reduce frequency / declare convergence}

**Next experiment queued**
- Hypothesis: {description}
- Expected impact: {pct}% improvement in {metric}
- Risk level: {low/medium/high}
- Auto-approved: {yes/no — high risk requires human approval}
```

**Monthly strategic review (generated 1st of each month):**
- 90-day trend analysis across all KPIs
- Partner portfolio rebalancing recommendations
- Format and topic effectiveness rankings (updated with experiment data)
- Budget allocation recommendations based on cost-per-lead by event type
- Convergence assessment: is the play approaching its local maximum?

### 4. Implement guardrails

Configure safety constraints in the optimization loop:

- **Rate limit:** Maximum 1 active experiment per optimization surface at a time. Never test format and topic simultaneously — isolate variables.
- **Revert threshold:** If any event's attendance rate drops below 25% or qualified leads drop to zero, auto-revert the active experiment immediately.
- **Human approval required for:**
  - Partner changes that affect 3+ scheduled events
  - Budget increases >30% per event
  - Any hypothesis the agent flags as "high risk" (e.g., changing event format for a high-performing partner)
  - Declaring convergence (human confirms the local maximum assessment)
- **Cooldown:** After a failed experiment (revert), wait 2 events before testing on the same optimization surface.
- **Monthly experiment cap:** Maximum 4 experiments per month across all surfaces. If all 4 fail, pause optimization and flag for human strategic review.
- **Partner protection:** Never run experiments that negatively affect a partner's experience without their knowledge. If an experiment requires changing co-host dynamics, inform the partner.

### 5. Detect and respond to convergence

The optimization loop monitors for convergence — when the play has reached its local maximum:

- Track the improvement percentage from each adopted experiment
- If 3 consecutive experiments produce <2% improvement across all optimization surfaces, the play is converging
- At convergence:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment frequency from continuous to monthly exploratory tests
  3. Generate a convergence report: current performance levels, what was optimized, cumulative improvement from all experiments, and what would be needed to break through (new partners, new channels, product changes)
  4. Shift agent effort to maintaining current performance and detecting market shifts that might open new optimization opportunities

If external conditions change (new competitor, market shift, partner ecosystem change), the agent detects the performance impact via anomaly detection and re-enters active optimization mode.

## Time Estimate

- Dashboard and reporting setup: 10 hours
- Autonomous optimization loop configuration: 12 hours
- Guardrail and convergence logic: 6 hours
- Monthly monitoring and tuning: 4 hours/mo x 12 = 48 hours
- Per-event execution (highly automated, 2/mo): 1.5 hours each x 24 = 36 hours
- Quarterly strategic review: 2 hours x 4 = 8 hours
- Total: ~120 hours over 12 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event funnels, experiment tracking, anomaly detection, dashboards | Free up to 1M events/mo; Growth $0 base + usage |
| n8n | Optimization loop scheduling, partner automation, follow-up routing | Self-hosted free; Cloud $24/mo |
| Anthropic Claude | Hypothesis generation, experiment evaluation, brief generation | API usage ~$20-50/mo at this volume |
| Attio | Partner CRM, attendee records, experiment log, scoring | Pro $29/user/mo |
| Clay | Partner research refreshes and attendee enrichment | Launch $185/mo |
| Loops | Promotion emails, follow-up sequences, A/B test variants | Growth $49/mo |
| Luma | Event platform with API integration | Plus $59/mo |
| Riverside | Event recording and content repurposing | Standard $19/mo |
| Descript | AI-powered clip extraction from event recordings | Creator $24/mo |
| Crossbeam | Partner account overlap for portfolio optimization | Free (3 seats); Connector $400/mo |

**Play-specific cost at Durable:** ~$200-450/mo (Luma Plus + Loops Growth + Riverside + Descript + Claude API + optional Crossbeam)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics → detect anomalies → generate hypotheses → run experiments → evaluate results → auto-implement winners → report weekly
- `autonomous-optimization` — play-specific monitoring: per-event and per-partner ROI, format/topic performance rankings, weekly briefs, and anomaly alerts that feed the optimization loop
- `dashboard-builder` — build the master event intelligence dashboard in PostHog with funnel, trend, partner, and experiment panels

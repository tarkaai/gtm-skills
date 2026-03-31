---
name: trigger-based-outreach-durable
description: >
  Trigger-based Outreach — Durable Intelligence. Autonomous AI agents manage the
  entire trigger-based pipeline: signal source health monitoring, automatic signal
  weight recalibration, copy rotation when message variants fatigue, continuous A/B
  experiments, and weekly optimization briefs. The autonomous-optimization drill runs
  the core detect-hypothesize-experiment-evaluate-implement loop to find and maintain
  the local maximum. The founder's only role is taking meetings.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email, Social"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Meeting rate sustained at ≥ 3% over 12 months via AI-powered signal detection, timing optimization, and autonomous experimentation with ≤ 1 hour/week founder involvement"
kpis: ["Meeting rate trend (flat or improving over 12 months)", "Signal-to-meeting conversion rate by signal type", "Cost per meeting trend (flat or decreasing)", "Autonomous experiment win rate (target ≥ 25%)", "Signal source health score (% of sources actively producing)"]
slug: "trigger-based-outreach"
install: "npx gtm-skills add marketing/solution-aware/trigger-based-outreach"
drills:
  - autonomous-optimization
  - intent-signal-health-monitor
  - threshold-engine
---

# Trigger-based Outreach — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email, Social

## Outcomes

The trigger-based outreach system runs autonomously. AI agents monitor signal sources, recalibrate signal weights based on conversion data, rotate copy variants before fatigue, run continuous A/B experiments, and generate weekly optimization briefs. The `autonomous-optimization` drill runs the core loop: detect metric anomalies, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. The system converges when successive experiments produce <2% improvement — meaning the play has found its local maximum.

The founder takes meetings and occasionally approves strategic changes. Meeting rate holds at or above the Scalable baseline for 12 consecutive months despite market changes, signal source degradation, message fatigue, and seasonal variation.

Pass: Meeting rate ≥ 3% sustained for 12 consecutive months with the founder spending ≤ 1 hour/week.
Fail: Meeting rate drops below 3% for 3 consecutive weeks despite automated interventions, or the system requires more than 2 hours/week of founder time.

## Leading Indicators

- Signal source health score stays above 80% (no more than 20% of signal sources are degraded or offline at any time)
- Autonomous experiment win rate ≥ 25% (at least 1 in 4 experiments produces a statistically significant improvement)
- Message fatigue index stays below 2x decay (no variant's reply rate drops more than 50% from its peak before rotation)
- Signal-to-meeting conversion for top 3 signal types stays within 20% of their Scalable baseline
- Cost per meeting trends flat or downward over the 12-month period
- Weekly optimization briefs are generated on schedule with actionable recommendations

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to establish the always-on agent loop for this play. Configure the five phases for trigger-based outreach specifically:

**Phase 1 — Monitor (daily via n8n cron):**
Use `posthog-anomaly-detection` to check the play's primary KPIs daily:
- Meeting rate (7-day rolling, compared to 4-week average)
- Positive reply rate (by signal type)
- Signal-to-outreach latency (by priority tier)
- Signal detection volume (by source and type)
- Domain health scores (across all sending accounts)
- LinkedIn acceptance and reply rates

Classify each metric: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase). If anomaly detected, trigger Phase 2. If normal, log and continue.

**Phase 2 — Diagnose (triggered by anomaly):**
When an anomaly is detected, the agent gathers context:
1. Pull 8-week metric history from PostHog for the affected metric
2. Pull current signal source configurations from Clay (which sources are active, last refresh time, signal volume)
3. Pull current campaign configurations from Instantly (active variants, sending volume, domain health)
4. Pull recent A/B test results and copy variant performance
5. Run `hypothesis-generation` with the anomaly data + full context

The agent receives 3 ranked hypotheses. Examples of trigger-specific hypotheses:
- "Funding signal conversion dropped because Q1 fundraising season ended — reduce funding signal weight and increase hiring-spree weight for Q2"
- "Reply rate dropped on job-change emails because the personalization line references the previous company, but most new hires have been in the role 60+ days — tighten freshness window to 30 days"
- "Signal source X stopped producing — the API changed or credits ran out"
- "Email variant B has fatigued — rotate in a new variant testing a different proof point"

If top hypothesis is high-risk (budget change >20%, targeting change affecting >50% of pipeline), send Slack alert for human approval. Otherwise, proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Design and run the experiment:
1. Use `posthog-experiments` to create a feature flag splitting traffic between control and variant
2. Implement the variant change (e.g., new copy variant via Instantly, new signal weight via Clay scoring, new timing via n8n schedule)
3. Set minimum experiment duration: 7 days or 100+ samples per variant, whichever is longer
4. Log experiment start in Attio: hypothesis text, start date, expected duration, success metric, pass threshold

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation` with control vs. variant data
3. Decision:
   - **Adopt:** Apply the winning variant to the live configuration. Log the change with reasoning.
   - **Iterate:** Generate a refined hypothesis building on this result. Return to Phase 2.
   - **Revert:** Disable the variant, restore control. Log the failure and lessons learned.
   - **Extend:** Insufficient data — keep running for another period.
4. Store the full evaluation (decision, confidence level, metric impact) in Attio

**Phase 5 — Report (weekly via n8n cron):**
Generate a weekly optimization brief:
- Anomalies detected this week and their diagnoses
- Experiments running: status, interim results
- Experiments completed: winners adopted, losers reverted
- Net metric impact from all changes this week
- Current distance from estimated local maximum (based on diminishing returns from recent experiments)
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Deploy signal source health monitoring

Run the `intent-signal-health-monitor` drill to build the monitoring layer for all signal sources:

**Signal pipeline dashboard (PostHog):**
- Panel 1: Signal volume by source and type (trend, last 30 days). Alert if any source drops below 50% of its 4-week average.
- Panel 2: Signal score distribution (Hot/Warm/Cool). Healthy: 10-20% Hot, 20-30% Warm, rest Cool.
- Panel 3: Signal-to-outreach latency by priority tier. Alert if median exceeds 4 hours for high-priority.
- Panel 4: Signal-to-meeting funnel by signal type. Break down: signal detected -> outreach sent -> reply -> meeting. Compare signal types side-by-side.
- Panel 5: Signal scoring accuracy. Compare conversion rates across score tiers. If Hot and Cool convert at similar rates, the scoring model needs recalibration.
- Panel 6: Signal freshness impact. Plot meeting rate vs. signal age at time of outreach. Identify the optimal freshness window per signal type.

**Weekly signal health workflow (n8n, runs Monday 8am):**
1. Pull last 7 days of signal data from PostHog
2. Check each signal source: is it producing? At expected volume? Are signals converting?
3. Compute signal-type ROI: meetings booked from each type / Clay credits consumed for that type
4. Flag underperforming sources (conversion below 1% for 3+ weeks) for removal
5. Flag overperforming sources for expansion (widen filters or add related signals)
6. Generate the signal health section of the weekly brief

**Monthly signal weight recalibration (n8n, runs 1st of month):**
1. Pull 30-day conversion data by signal type
2. Recompute signal weights based on actual meeting rate per type
3. Adjust Clay scoring formulas: increase weight for high-converting signal types, decrease for low-converting
4. Log the weight changes in Attio
5. Compare new weights to previous month — if any signal type shifted >30% in weight, flag for human review

### 3. Build copy rotation and message freshness engine

Message fatigue is the primary threat to Durable performance. Build an automated copy management system:

**Copy library (minimum per signal type):**
- Funding signals: 4 Email 1 variants (ROI angle, team scaling angle, competitive positioning angle, integration opportunity angle), 3 Email 2 variants, 2 Email 3 variants
- Job-change signals: 4 Email 1 variants, 3 Email 2 variants, 2 Email 3 variants
- Hiring-spree signals: 3 Email 1 variants, 2 Email 2 variants
- Competitor-churn signals: 3 Email 1 variants, 2 Email 2 variants
- Intent/website signals: 3 Email 1 variants, 2 Email 2 variants

**Copy rotation workflow (n8n, runs weekly):**
1. Pull reply rate for each active variant over a rolling 30-day window from PostHog
2. If a variant's reply rate drops below 70% of its peak rate: message fatigue detected
3. Pause the fatigued variant
4. Use Claude API to draft a replacement variant based on: the angle that is currently winning across other signal types, any new customer stories or proof points, and recent market trends
5. Queue the draft for human approval (included in the weekly brief)
6. Rotate in the next available variant from the library
7. Log the rotation: which variant fatigued, when, replacement deployed

**Human action required:** The founder reviews and approves new copy variants included in the weekly brief (~15 minutes). The agent drafts all variants based on recent meeting conversations and market context.

### 4. Configure guardrails and auto-recovery

Run the `threshold-engine` drill to set up hard guardrails that override the optimization loop:

**Signal guardrails:**
- If total signal volume drops below 50% of the 4-week average for 3 consecutive days: alert + check all Clay API connections and credit balances
- If any single signal source produces zero signals for 5 consecutive days: flag as "source down," redistribute outreach volume to other signal types, alert the agent to investigate

**Outreach guardrails:**
- Volume: never exceed 30 sends/day per email account, 50 LinkedIn actions/day
- Quality: if negative reply rate exceeds 5% on any signal-type campaign, pause that campaign and review messaging
- Compliance: unsubscribe rate above 0.5% triggers messaging review
- Deliverability: if any domain health score drops below 85%, pause that account, redistribute volume, keep warmup active

**Budget guardrails:**
- Cost per meeting exceeding $150: trigger efficiency review (are low-converting signal types consuming disproportionate Clay credits?)
- Total monthly spend exceeding 120% of budget: alert + recommend which signal types or tools to scale down

**Auto-recovery procedures:**
- Domain health drop: automatically pause affected account, redistribute volume evenly across healthy accounts, alert agent
- Signal source failure: automatically re-route enrichment to backup sources (e.g., if People Data Labs fails, switch to Apollo for contact enrichment)
- Experiment producing >30% metric drop: immediate auto-revert to control configuration, log the failure, 7-day cooldown before next experiment on that variable

### 5. Run monthly strategic review

Build an n8n workflow that runs on the 1st of each month, generating a comprehensive strategic brief:

1. **Signal type performance ranking:** meetings per signal type, cost per meeting per type, trend vs. previous month. Identify which types to expand and which to retire.
2. **Channel performance:** email vs. LinkedIn conversion rates per signal type. Recommend channel mix adjustments.
3. **Experiment portfolio:** experiments run this month, win/loss ratio, cumulative metric impact from adopted changes. Identify what types of experiments are producing the most improvement.
4. **Market conditions:** are signal volumes changing? (Funding signals seasonal, hiring signals cyclical.) Recommend proactive adjustments for the coming month.
5. **Convergence check:** are the last 3 experiments producing diminishing returns (<2% improvement each)? If yes, the play has reached its local maximum. Recommend reducing optimization frequency from daily to weekly and focusing experimentation on strategic changes (new signal types, new ICP segments, new channels) rather than tactical optimization.
6. **Budget efficiency:** total spend vs. meetings booked, trend over 12 months. Flag if ROI is declining.

**Human action required:** The founder reviews the monthly brief (~30 minutes) and decides on strategic changes: new signal types to add, ICP segment expansion, budget reallocation, or channel mix shifts.

### 6. Sustain for 12 months

The system runs continuously with the autonomous optimization loop as its core engine. The agent's ongoing responsibilities:
- Ensure all n8n workflows execute daily/weekly without errors
- Respond to threshold-engine alerts within 4 hours
- Rotate copy variants when fatigue threshold triggers
- Apply experiment winners when tests conclude
- Recalibrate signal weights monthly based on conversion data
- Generate weekly optimization briefs and monthly strategic briefs
- Maintain the copy library with fresh variants
- Monitor signal source health and replace degraded sources

The founder's responsibilities:
- Respond to positive replies in Slack (delegatable to a sales hire at this stage)
- Take meetings
- Approve copy variants in the weekly brief (~15 min/week)
- Review monthly strategic brief and make strategic decisions (~30 min/month)

### 7. Evaluate sustainability after 12 months

Compute over the full 12-month period:
- Monthly meeting rate for each of the 12 months
- Meeting rate trend (is it stable, improving, or decaying?)
- Total cost / total meetings = cost per meeting (trend over time)
- Total founder hours / total meetings = founder time per meeting
- Experiment portfolio: total experiments run, win rate, cumulative impact
- Signal type evolution: which types were added/retired over 12 months, and how did ROI change
- Convergence status: has the play reached its local maximum? When did experiments stop producing >2% improvement?

- **PASS (meeting rate ≥ 3% for all 12 months, founder ≤ 1 hour/week):** The play is durable. It runs autonomously and produces consistent pipeline from trigger-timed outreach. Consider: expanding to new ICP segments, delegating the founder role to a sales hire, applying the signal detection infrastructure to other plays (e.g., multi-threaded account outreach triggered by the same signals).
- **DECLINING (meeting rate held for 8+ months then decayed below 3%):** Signal landscape shifted or message fatigue outpaced the rotation engine. Options: expand to new signal types (industry events, regulatory changes, M&A activity), refresh competitive positioning if the market moved, or reduce volume and focus only on the top-performing signal types.
- **FAIL (meeting rate below 3% for 3+ consecutive weeks at any point):** The autonomous system is not adapting fast enough. Diagnose: Is the signal weight recalibration keeping up with conversion shifts? Is the copy rotation engine catching fatigue in time? Is a signal source failure going undetected? Fix the specific broken component or accept that this play requires more manual oversight than Durable allows.

## Time Estimate

- Autonomous optimization loop setup: 10 hours (Month 1)
- Signal health monitoring dashboard and workflows: 8 hours (Month 1)
- Copy rotation engine and library: 6 hours (Month 1)
- Guardrails and auto-recovery: 5 hours (Month 1)
- Monthly strategic review workflow: 3 hours (Month 1)
- Setup subtotal: 32 hours
- Weekly agent monitoring: 2 hours/week x 48 weeks = 96 hours
- Weekly founder time: 1 hour/week x 48 weeks = 48 hours (including meeting time)
- Monthly founder review: 30 min x 12 months = 6 hours
- Copy variant generation (ongoing): 3 hours/month x 12 months = 36 hours
- Signal source maintenance: 2 hours/month x 12 months = 24 hours
- Ongoing subtotal: ~162 hours agent + ~54 hours founder
- Grand total: ~180 hours agent time over 12 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Email sequencing, warmup, A/B testing, reply detection, domain rotation | Hypergrowth plan $97/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Signal detection, enrichment, personalization, daily signal refresh, scoring | Growth plan $495/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM, deal tracking, experiment logging, signal attribution | Plus plan $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Dashboards, funnel analysis, A/B test measurement, anomaly detection | Free tier: 1M events/mo, usage-based beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | All automation: optimization loop, signal monitoring, copy rotation, reports, guardrails | Pro plan $60/mo or self-host free ([n8n.io/pricing](https://n8n.io/pricing)) |
| Dripify or HeyReach | LinkedIn automation | Dripify $79/mo ([dripify.io/pricing](https://dripify.io/pricing)) |
| Cal.com | Meeting booking | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, copy drafting | Usage-based ~$20-50/mo ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Secondary domains (x4) | Sending infrastructure | ~$50/year total |
| Google Workspace (x4) | Sending accounts | ~$28/mo total ($7/user/mo) |

**Estimated monthly cost for Durable:** ~$870-960/mo + ~$50/year for domains

## Drills Referenced

- `autonomous-optimization` — the core detect-diagnose-experiment-evaluate-implement loop that finds and maintains the local maximum for trigger-based outreach
- `intent-signal-health-monitor` — signal source monitoring, scoring accuracy audits, and signal pipeline health reporting
- `threshold-engine` — guardrails for signal volume, outreach quality, deliverability, and budget that auto-pause and auto-recover when breached

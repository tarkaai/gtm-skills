---
name: multi-threaded-account-outreach-durable
description: >
  Multi-threaded Outreach — Durable Intelligence. Always-on AI agents detect metric anomalies,
  generate improvement hypotheses, run A/B experiments on thread timing, role messaging, and
  channel mix, evaluate results, and auto-implement winners. Converges when successive
  experiments produce <2% improvement.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained ≥2.5% account-to-meeting rate over 12 months via autonomous optimization of stakeholder threading strategy"
kpis: ["Sustained account-to-meeting rate", "Experiment win rate", "Time to detect and correct metric drops", "Cost per meeting trend", "Cross-thread signal rate"]
slug: "multi-threaded-account-outreach"
install: "npx gtm-skills add marketing/solution-aware/multi-threaded-account-outreach"
drills:
  - autonomous-optimization
---

# Multi-threaded Outreach — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Outcomes

The play runs itself. AI agents continuously monitor multi-threaded outreach performance, detect when metrics plateau or decay, generate hypotheses for what to change (message copy, thread timing, channel mix, stakeholder targeting), run A/B experiments, evaluate results, and auto-implement winners. The goal is to find and maintain the local maximum — the best possible account-to-meeting rate given the current market, competitive landscape, and audience.

**Pass threshold:** Sustained ≥2.5% account-to-meeting rate over 12 months. The `autonomous-optimization` loop runs weekly. Convergence is reached when 3 consecutive experiments produce <2% improvement — at that point the play is at its local maximum and monitoring frequency drops to weekly.

## Leading Indicators

- Anomaly detection catches metric drops within 48 hours (not discovered at weekly review)
- Hypothesis generation produces actionable, testable ideas (not vague "improve messaging" suggestions)
- Experiment cycle time under 14 days from hypothesis to result
- At least 2 of every 4 monthly experiments produce measurable improvement (≥50% win rate)
- Cost per meeting trending flat or downward over 6-month rolling window

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. This creates the core Monitor → Diagnose → Experiment → Evaluate → Implement cycle.

Configure the loop specifically for multi-threaded outreach:

**Monitoring (daily n8n cron):**
1. Pull PostHog data for the last 14 days: `mto_email_sent`, `mto_email_replied`, `mto_linkedin_sent`, `mto_linkedin_replied`, `mto_meeting_booked`, `mto_cross_thread_signal`
2. Compute rolling metrics:
   - Account-to-meeting rate (primary KPI)
   - Reply rate by stakeholder role (Champion, Economic Buyer, Influencer)
   - Cross-thread engagement rate (accounts where 2+ stakeholders engaged)
   - Channel attribution: meetings sourced from email-first vs. LinkedIn-first threads
   - Email deliverability and LinkedIn restriction rate
3. Compare each metric against 4-week rolling average
4. Classify: **normal** (within ±10%), **plateau** (within ±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
5. If anomaly detected → trigger Diagnosis phase
6. If normal → log metrics to Attio, no action

**Diagnosis (triggered by anomaly):**
1. Gather context from Attio: current targeting criteria, active message variants, thread timing configuration, recent A/B test results
2. Pull 8-week metric history broken down by: stakeholder role, channel, message variant, thread timing variant, account industry
3. Call Claude (hypothesis-generation fundamental) with anomaly data + context
4. Receive 3 ranked hypotheses. Examples of play-specific hypotheses:
   - "Champion reply rate dropped 25% because the problem-aware opener references a pain point that competitors have started addressing in their marketing. Test a new opener that differentiates on implementation speed instead."
   - "Economic Buyer conversion dropped because the Day 7 timing is too late — by Day 7, Champions who responded positively have already moved to evaluating a competitor. Test Day 3 for Economic Buyer."
   - "Cross-thread signals decreased because LinkedIn acceptance rates dropped (possible LinkedIn algorithm change). Test shifting Influencer outreach from LinkedIn-first to email-first."
5. Store hypotheses in Attio. If top hypothesis is high-risk (e.g., changes targeting for >50% of accounts) → Slack alert for human review and STOP
6. If low/medium risk → proceed to Experiment phase

**Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using PostHog feature flags:
   - Randomization unit: account (all contacts at an account get the same variant)
   - Split: 50/50 between control (current) and variant (hypothesis change)
   - Primary metric: account-to-meeting rate
   - Secondary metrics: reply rate by role, cross-thread signal rate, cost per meeting
   - Minimum sample: 100 accounts per variant (2-3 weeks at 200 accounts/month)
2. Implement the variant:
   - For message changes: create new Instantly campaign variants, update the n8n orchestration workflow to route test-group accounts to the new campaign
   - For timing changes: modify the thread map logic in n8n for test-group accounts
   - For channel changes: update channel assignment rules for test-group contacts
3. Log experiment start in Attio: hypothesis, start date, expected end date, success criteria

**Evaluation (triggered by experiment reaching sample size):**
1. Pull results from PostHog experiments API
2. Run experiment-evaluation fundamental:
   - **Adopt** if variant beats control with ≥95% confidence and practical significance (≥0.5 percentage point improvement on account-to-meeting rate)
   - **Iterate** if directionally positive but not significant — generate a refined hypothesis
   - **Revert** if variant underperforms control — restore previous configuration immediately
   - **Extend** if promising but insufficient sample — continue for another 100 accounts
3. Auto-implement winners: update the production Instantly campaigns and n8n orchestration workflow to use the winning variant for all accounts
4. Store full evaluation in Attio: decision, confidence interval, effect size, reasoning

### 2. Build the multi-threaded outreach performance monitor

Run the `autonomous-optimization` drill configured specifically for multi-threaded outreach. Build a PostHog dashboard named "Multi-threaded Outreach — Durable Monitor" with:

**Row 1 — Primary KPIs (weekly trend):**
- Account-to-meeting rate (the number that matters)
- Cross-thread engagement rate (accounts with 2+ stakeholder responses)
- Cost per meeting (tool spend / meetings booked)

**Row 2 — Per-Role Breakdown:**
- Reply rate by stakeholder role (Champion, Economic Buyer, Influencer) — stacked line chart
- Meeting source attribution by first-responding role — pie chart
- Average sequence steps to reply by role — bar chart

**Row 3 — Thread Dynamics:**
- Average threads per account (how many stakeholders engaged before meeting booked)
- Cross-thread signal rate (internal referrals, "my colleague mentioned you" replies)
- Thread timing effectiveness: which Day offset for Economic Buyer produces highest conversion

**Row 4 — Experiment Tracker:**
- Active experiments: count, hypothesis summary, days remaining
- Last 10 experiments: win/loss/iterate/extend status
- Cumulative improvement from adopted experiments (net effect on account-to-meeting rate)

**Row 5 — Health Guardrails:**
- Email deliverability rate (must stay >97%)
- LinkedIn connection acceptance rate (must stay >20%)
- Negative reply rate (must stay <5%)
- Account suppression rate (accounts removed due to negative signals)

Configure anomaly alerts via PostHog:
- Account-to-meeting rate drops below 2% for 5 business days → Slack alert + trigger optimization loop
- Any role's reply rate drops below 1.5% for 1 week → Slack alert
- Email deliverability drops below 95% → URGENT alert, pause all sends
- Cross-thread signal rate drops to zero for 2 weeks → Slack alert (multi-threading may be broken)

### 3. Configure the weekly optimization brief

As part of the `autonomous-optimization` drill, the weekly brief should include multi-threaded-specific sections:

```
## Weekly Optimization Brief — Multi-threaded Outreach
Week of {date}

### Performance Summary
- Account-to-meeting rate: {rate}% (4-week avg: {avg}%, delta: {delta})
- Meetings booked: {count} from {accounts_engaged} accounts
- Cross-thread engagement: {cross_thread_rate}% of responding accounts
- Cost per meeting: ${cost}

### Per-Role Performance
| Role | Reply Rate | Meetings Sourced | Best Variant |
|------|-----------|-----------------|--------------|
| Champion | {rate}% | {count} | {variant_name} |
| Economic Buyer | {rate}% | {count} | {variant_name} |
| Influencer | {rate}% | {count} | {variant_name} |

### Active Experiment
- Hypothesis: {description}
- Status: {days_remaining} days remaining, {samples} accounts processed
- Interim results: {direction} ({confidence}% confidence so far)

### Last Experiment Result
- Hypothesis: {description}
- Decision: {adopt/revert/iterate}
- Effect: {delta} on account-to-meeting rate

### Anomalies Detected
- {anomaly_list or "None — all metrics within normal range"}

### Recommended Focus
- {AI-generated recommendation for what to optimize next}
```

Post to Slack every Monday at 8am via n8n cron. Store in Attio as a campaign note.

### 4. Deploy signal-based list refresh

The Durable level does not just optimize existing sequences — it also ensures the account pipeline never runs dry. Configure an n8n workflow that:

1. Monitors for buying signals via Clay: job changes at target-profile companies, funding rounds, competitor mentions in job postings, technology adoption signals
2. Scores each signal using the validated ICP from Baseline (companies matching the profile that produced the highest conversion)
3. Auto-enrolls signal-detected companies into the multi-threaded pipeline: creates Attio deal, triggers stakeholder discovery, generates thread map
4. Tags signal-sourced accounts separately in PostHog so you can measure whether signal-detected accounts convert higher than cold-sourced accounts

**Human action required:** Monthly review of signal sources. Approve or reject new signal categories the AI proposes. Review any accounts flagged as high-risk (competitors, existing customers, partner companies).

### 5. Convergence detection and maintenance mode

The `autonomous-optimization` loop includes convergence detection. For this play, convergence means:

- 3 consecutive experiments produce <2% improvement on account-to-meeting rate
- All per-role reply rates are within ±5% of each other across 4 consecutive weeks
- Cross-thread signal rate is stable

When converged:
1. Reduce monitoring from daily to weekly
2. Reduce experiment frequency from 4/month to 1/month (maintenance experiments)
3. Generate a convergence report: "Multi-threaded outreach has reached its local maximum at {rate}% account-to-meeting rate. Current configuration: {winning variants, timing, channel mix}. Further gains require strategic changes (new ICP segments, new channels, product changes) rather than tactical optimization."
4. Continue monitoring for environmental shifts (competitor launches, market changes, seasonal effects) that could break convergence

**Reactivation trigger:** If account-to-meeting rate drops below 2% for 2 consecutive weeks after convergence, reactivate the full daily optimization loop.

## Time Estimate

- Autonomous optimization loop setup and configuration: 16 hours
- Outbound performance monitor dashboard build: 8 hours
- Signal-based list refresh automation: 8 hours
- Initial experiment design and implementation: 8 hours
- Monthly optimization reviews and experiment management: 120 hours (10 hours/month x 12 months)
- Convergence analysis and documentation: 4 hours
- Quarterly strategic reviews: 16 hours (4 hours/quarter x 4)
- Total: 180 hours over 12 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Cold email at scale with A/B variant campaigns | Hypergrowth: $77/mo (https://instantly.ai/pricing) |
| Clay | Stakeholder enrichment + signal monitoring + continuous list refresh | Pro: $349/mo for higher credit volume (https://www.clay.com/pricing) |
| LinkedIn Sales Navigator | Stakeholder research and InMail for high-value threads | Core: $99/mo (https://business.linkedin.com/sales-solutions/compare-plans) |
| Dripify or Expandi | LinkedIn automation at scale | Dripify: $59/mo (https://dripify.io/pricing) |
| PostHog | Analytics, experiments, feature flags, anomaly detection | Free tier sufficient; Growth: $0+ usage-based (https://posthog.com/pricing) |
| Anthropic Claude | Hypothesis generation, experiment evaluation, weekly briefs | API usage: ~$20-50/mo at this optimization frequency (https://www.anthropic.com/pricing) |
| n8n | Orchestration for optimization loop, signal detection, reporting | Starter: $20/mo (https://n8n.io/pricing) |
| Attio | CRM for deals, experiments, optimization audit trail | Plus: $29/user/mo (https://attio.com/pricing) |

**Estimated monthly cost:** $605-$635/mo (Instantly $77 + Clay $349 + LinkedIn $99 + Dripify $59 + Claude API ~$20-50)

## Drills Referenced

- `autonomous-optimization` — the core Monitor → Diagnose → Experiment → Evaluate → Implement loop that finds the local maximum for multi-threaded outreach conversion
- `autonomous-optimization` — always-on dashboards, anomaly alerts, and weekly/monthly reporting specific to multi-channel outbound metrics

---
name: comment-to-dm-play-durable
description: >
  Comment-to-DM Play — Durable Intelligence. Always-on AI agents autonomously optimize the comment-to-DM
  motion: monitor engagement metrics, detect anomalies, generate improvement hypotheses, run experiments,
  and auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce
  <2% improvement.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Social"
level: "Durable Intelligence"
time: "Ongoing, ~5 hours/week founder time"
outcome: "Sustained or improving meeting volume (≥ 6 meetings/month) with decreasing founder time per meeting; autonomous optimization loop running; convergence detected when <2% improvement across 3 consecutive experiments"
kpis: ["Meetings per month", "Founder minutes per meeting", "Author reply rate trend", "DM-to-meeting conversion trend", "Optimization experiment win rate"]
slug: "comment-to-dm-play"
install: "npx gtm-skills add marketing/problem-aware/comment-to-dm-play"
drills:
  - autonomous-optimization
  - engagement-performance-reporting
  - dashboard-builder
---

# Comment-to-DM Play — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Social

## Outcomes

The play runs itself. AI agents monitor comment-to-DM performance, detect when metrics plateau or decline, generate hypotheses for improvement, run experiments, evaluate results, and auto-implement winners. The founder's role shifts from executing the play to reviewing weekly optimization briefs and approving high-risk experiments. The optimization loop finds the local maximum for this play and maintains it as market conditions change.

## Leading Indicators

- Optimization loop running on daily cron (monitoring) and weekly cadence (experiments)
- ≥ 1 experiment active at all times (until convergence)
- Weekly optimization briefs delivered every Monday
- Founder time per meeting trending downward
- Meeting volume holding steady or growing despite market changes
- Convergence detection: <2% improvement across 3 consecutive experiments triggers reduced-frequency mode

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the comment-to-DM play:

**Phase 1 -- Monitor (daily via n8n cron):**
1. Pull comment-to-DM metrics from PostHog: comments posted, author reply rate, DM reply rate, meetings booked (last 7 days)
2. Compare against 4-week rolling average
3. Classify: normal (±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
4. If anomaly detected, trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**
1. Gather context from Attio: current target list size, tier distribution, active prospect count by stage, recent DM conversion rates
2. Pull 8-week metric history from PostHog dashboards
3. Run `hypothesis-generation` with the anomaly data:
   - Example hypotheses for reply rate drop: "Target list has gone stale (same 80 prospects for 6+ weeks)"; "Comment strategy mix has drifted from optimal (too many 'add value', not enough 'sharp question')"; "LinkedIn algorithm change reducing comment visibility"
   - Example hypotheses for DM conversion drop: "DM timing too aggressive (DMing before sufficient warming)"; "DM copy has become templated"; "ICP shift -- current targets are less pain-aware"
4. Rank hypotheses by expected impact and risk
5. If top hypothesis is high-risk (e.g., changing ICP targeting), alert the founder for approval. Otherwise proceed.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
1. Design the experiment via PostHog feature flags
2. Implement the variant. Examples of experiments this play runs:
   - **Comment strategy mix experiment**: Shift from 60/20/15/5 to 40/30/25/5 (more counterpoints and questions)
   - **Target list refresh experiment**: Replace 30% of prospects with new ones from Clay discovery
   - **DM template experiment**: Test a new opening DM referencing a different shared touchpoint
   - **Comment volume experiment**: Increase from 8 to 12 daily comments and measure if reply rate holds
   - **Tier focus experiment**: Shift 70% of comments to Tier 1 (direct prospects) vs the current 50/30/20 split
3. Run for minimum 7 days or 100+ data points per variant
4. Log experiment start in Attio

**Phase 4 -- Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation`:
   - **Adopt**: The variant improved the target metric by ≥ 5% with 95% confidence. Implement permanently.
   - **Iterate**: Results were mixed. Generate a refined hypothesis and return to Phase 2.
   - **Revert**: The variant performed worse. Restore control. Log the learning.
3. Store the full evaluation in Attio with decision and reasoning

**Phase 5 -- Report (weekly via n8n cron):**
1. Generate the weekly optimization brief covering: anomalies detected, hypotheses generated, experiments running/completed, decisions made, net metric change
2. Calculate: current estimated distance from local maximum (based on improvement trend of recent experiments)
3. Post to Slack and store in Attio

### 2. Build the durable performance dashboard

Run the `dashboard-builder` drill to create the Durable-level dashboard:

**Panel 1 -- Health Check:**
- Meeting volume: last 4 weeks vs target (≥ 6/month)
- Author reply rate: 8-week trend line
- DM-to-meeting conversion: 8-week trend line
- Founder minutes per meeting: 8-week trend (should decrease)

**Panel 2 -- Optimization Activity:**
- Active experiments: name, variant, start date, progress
- Last 5 completed experiments: name, result (adopt/iterate/revert), impact
- Cumulative metric lift from all adopted experiments

**Panel 3 -- Pipeline Health:**
- Prospects by stage: stacked bar (cold, warming, warm, dm-ready, conversation, meeting_booked)
- Target list freshness: % of prospects engaged in last 14 days vs stale
- New prospects added this month vs churned out

**Panel 4 -- Convergence Tracking:**
- Last 5 experiment improvement percentages
- Rolling 3-experiment average improvement
- Convergence status: OPTIMIZING (>2% avg improvement) or CONVERGED (<2%)

### 3. Configure engagement performance reporting

Run the `engagement-performance-reporting` drill to establish automated reporting:

1. Weekly reports delivered every Monday with all key metrics
2. Monthly deep-dive reports with funnel analysis, strategy breakdowns, and prospect tier performance
3. Alert thresholds configured:
   - Comment volume drops below 25/week
   - Author reply rate drops below 10% for 2 consecutive weeks
   - DM reply rate drops below 25% for 2 consecutive weeks
   - Zero meetings booked in 2 consecutive weeks

### 4. Manage the optimization lifecycle

**Active optimization (default mode):**
- Daily metric monitoring
- 1-2 experiments per month
- Weekly briefs

**Convergence detected (≤ 2% improvement for 3 consecutive experiments):**
- Reduce monitoring to weekly
- Pause experiments
- Generate a convergence report: "This play has reached its local maximum. Current performance: {metrics}. Further gains require strategic changes (new platform, new ICP segment, product changes) rather than tactical optimization."
- Continue monitoring for regressions (monthly cadence)

**Regression detected (metrics drop >15% from local maximum):**
- Re-activate daily monitoring and experiment cadence
- Diagnose: market shift, LinkedIn algorithm change, competitor activity, or seasonal effect?
- Generate new hypotheses and resume the optimization loop

**Human action required:** The founder reviews the weekly optimization brief and approves any high-risk experiments flagged by the system. Estimated time: 15-30 minutes per week reviewing briefs + 15 minutes approving experiments. The founder still posts comments and sends DMs, but the strategy, targeting, and timing decisions are agent-driven.

## Time Estimate

- Autonomous optimization setup: 4 hours (one-time)
- Dashboard and reporting setup: 2 hours (one-time)
- Founder daily execution (commenting + DMs): ~3 hours/week
- Founder weekly brief review: 30 minutes/week
- Experiment approval and oversight: 30 minutes/week
- Monthly strategic review: 1 hour/month
- **Ongoing: ~5 hours/week founder time (decreasing as the agent optimizes efficiency)**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Premium or Sales Navigator | Feed search, commenting, DMs | $29.99-99/mo (https://www.linkedin.com/premium/) |
| Taplio | Prospect feed monitoring | $49/mo (https://taplio.com/pricing) |
| Shield | Peer/competitor monitoring | $25/mo (https://shieldapp.ai/pricing) |
| PostHog | Analytics, experiments, dashboards | Free up to 1M events (https://posthog.com/pricing) |
| Attio | CRM, cadence tracking, experiment logging | Free up to 3 users (https://attio.com/pricing) |
| Clay | Prospect enrichment, target list refresh | $149/mo Explorer plan (https://clay.com/pricing) |
| n8n | Automation: discovery, monitoring, reporting | Free self-hosted or $20/mo cloud (https://n8n.io/pricing) |
| Anthropic API | Comment drafting, hypothesis generation, experiment evaluation | ~$20-50/mo (https://www.anthropic.com/pricing) |

## Drills Referenced

- `autonomous-optimization` — the core monitor -> diagnose -> experiment -> evaluate -> implement loop
- `engagement-performance-reporting` — weekly/monthly reports with funnel analytics and alerts
- `dashboard-builder` — real-time PostHog dashboard for Durable-level metrics and convergence tracking

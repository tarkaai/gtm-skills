---
name: outbound-with-short-video-durable
description: >
  Outbound With Short Video — Durable Intelligence. Always-on AI agents find the
  local maximum of personalized video outreach through autonomous monitoring,
  hypothesis generation, A/B experimentation, and auto-implementation of winners.
  The optimization loop runs until successive experiments produce <2% improvement.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email"
level: "Durable Intelligence"
time: "Ongoing — 8 hours/month maintenance after initial 20-hour setup"
outcome: "Sustained or improving video completion rate (>=10%) and meeting rate (>=6/month) over 6 months via autonomous agent-driven optimization; convergence declared when 3 consecutive experiments produce <2% lift"
kpis: ["Video completion rate", "Thumbnail click-through rate", "Meetings booked from video", "Video-to-meeting conversion rate", "Cost per meeting", "Experiment win rate", "Weeks since last significant improvement"]
slug: "outbound-with-short-video"
install: "npx gtm-skills add marketing/solution-aware/outbound-with-short-video"
drills:
  - autonomous-optimization
  - video-outreach-performance-monitor
  - signal-detection
---

# Outbound With Short Video — Durable Intelligence

> **Stage:** Marketing -> Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email

## Outcomes

Deploy an always-on AI agent loop that autonomously monitors video outreach performance, detects when metrics plateau or degrade, generates hypotheses for improvement, runs A/B experiments, evaluates results, and auto-implements winners. The agent finds the local maximum of this play -- the best achievable performance given the current market, audience, and competitive landscape. When three consecutive experiments produce less than 2% improvement, the play has converged and the agent shifts to maintenance monitoring.

**Pass threshold:** Sustained or improving video completion rate (>=10%) and meeting rate (>=6/month) over 6 months. Convergence is the success state, not a failure -- it means the play is optimized.

## Leading Indicators

- Autonomous optimization loop runs without human intervention for 4+ consecutive weeks
- At least 2 experiments completed per month with clear adopt/revert decisions
- Weekly optimization briefs generated automatically with actionable insights
- Video outreach performance does not degrade >20% from the Scalable baseline for more than 2 consecutive weeks without an automated corrective experiment being triggered
- Signal-based targeting continuously refreshes the prospect pool (no audience exhaustion)
- Cost per meeting trends flat or down over 6 months (efficiency improving or stable)

## Instructions

### 1. Deploy the video outreach performance monitor

Run the `video-outreach-performance-monitor` drill to build the monitoring layer:

1. **Dashboard:** Create the PostHog "Video Outreach -- Performance" dashboard with all video-specific panels: engagement funnel, completion rate distribution, video vs text comparison, engagement quality by segment, and pipeline impact.

2. **Anomaly detection:** Configure alerts for:
   - Video completion rate drops below 10% for 5 consecutive days
   - Thumbnail click rate drops below 5% for 1 week
   - Meeting booking rate drops to 0 for 7+ days
   - Email bounce rate exceeds 3%
   - Negative reply rate exceeds 5%
   - Video view count drops 50%+ week over week

3. **Weekly briefs:** Set up the automated Monday morning brief covering: video funnel metrics with deltas, top-performing videos and script patterns, ICP segment performance, and optimization recommendations.

4. **Structured data feed:** Ensure all metrics fire as structured PostHog events (`video_outreach_weekly_summary`, `video_outreach_anomaly`) that the autonomous optimization drill can consume.

### 2. Deploy signal-based prospect refresh

Run the `signal-detection` drill to prevent audience exhaustion:

1. Configure Clay to monitor buying signals daily: job changes at target accounts, funding announcements, technology adoption signals, hiring sprees in relevant roles, competitor mentions.

2. Score signals by recency (last 30 days strongest) and intensity (multiple signals from one account rank higher).

3. Route high-score signals into the video outreach pipeline automatically: new signal-detected prospects get added to the next weekly batch, pre-enriched and pre-assigned to an ICP segment.

4. Set up an n8n workflow that tracks "audience freshness": what percentage of prospects in the last 4 weeks were signal-detected vs cold-list. Target: >=30% signal-detected for higher conversion rates.

5. Build a "prospect exhaustion" alert: if the pipeline has contacted >50% of the addressable market in your ICP, flag for human strategic review (expand ICP, new verticals, or new channels).

### 3. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured specifically for video outreach:

**Phase 1 -- Monitor (daily via n8n cron):**
1. Pull the last 2 weeks of video outreach KPIs from PostHog
2. Compare against the 4-week rolling average
3. Classify each KPI: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
4. If all normal: log to Attio, no action
5. If anomaly detected: trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**
1. Gather context from Attio: current segment videos in use, prospect segments being targeted, send cadence, follow-up configuration
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` with anomaly data + video outreach context
4. Receive 3 ranked hypotheses. Examples of video-specific hypotheses:
   - "Video completion rate dropped because the 90s segment videos are too long for the new Fintech CTO segment. Hypothesis: 45s videos will restore completion rate."
   - "Meeting rate dropped because the 'Book 15 minutes' CTA is stale. Hypothesis: Changing CTA to 'See a 5-minute live demo' will increase CTA clicks by 15%."
   - "Thumbnail click rate dropped because email clients are blocking the GIF. Hypothesis: switching to a static thumbnail with a play button overlay will restore click rate."
5. Store hypotheses in Attio as campaign notes
6. If top hypothesis risk = "high": alert human and STOP
7. If risk = "low" or "medium": proceed to Phase 3

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
1. Take the top-ranked hypothesis
2. Design the experiment using PostHog feature flags: split next 200 prospects into control (current approach) and variant (hypothesis change)
3. Implement the variant:
   - For video length tests: record a new segment video at the hypothesized duration
   - For CTA tests: update the Loom CTA button text/link on a copy of the segment video
   - For email subject/copy tests: create a variant Instantly campaign
   - For targeting tests: create a new Clay enrichment filter for the hypothesized segment
4. Run the experiment for minimum 7 days or until 100+ prospects per variant
5. Log experiment start in Attio: hypothesis, start date, duration, success criteria

**Human action required for video experiments:** If the hypothesis involves recording a new video (length, script, format), the founder must record it. The agent designs the experiment, identifies what to test, and sets up the A/B split -- but cannot record on camera. Alert the founder via Slack with the exact recording brief: duration, script structure, and which segment.

**Phase 4 -- Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation` comparing control vs variant
3. Decision:
   - **Adopt:** Variant wins with 95% confidence. Update the live campaign to use the winning approach. Update segment video library if video was changed. Log the change.
   - **Iterate:** Result inconclusive or partially positive. Generate a refined hypothesis. Return to Phase 2.
   - **Revert:** Variant lost. Restore control. Log the failure reason. Return to Phase 1 monitoring.
4. Store the full evaluation in Attio

**Phase 5 -- Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes
3. Generate the weekly optimization brief:
   - What changed this week and why
   - Net impact on video outreach KPIs
   - Current distance from estimated local maximum
   - Convergence status: are recent experiments producing diminishing returns?
4. Post to Slack and store in Attio

### 4. Configure convergence detection

The optimization loop should detect when the play has reached its local maximum:

1. Track the improvement delta of each experiment over the last 3 months
2. If 3 consecutive experiments produce <2% improvement on the primary KPI (meetings booked):
   - Declare convergence
   - Reduce monitoring frequency from daily to weekly
   - Generate a convergence report: "Video outreach is optimized. Current performance: {metrics}. This play produces approximately {N} meetings/month at {cost_per_meeting}. Further gains require strategic changes: new ICP segments, new channels (LinkedIn video DMs), or product positioning changes."
3. Continue weekly monitoring to catch external disruptions (competitor enters market, email deliverability changes, Loom platform changes)

### 5. Maintain the video library

As experiments run and winners are adopted, maintain the segment video library:

1. Keep a registry in Attio: each segment video with its creation date, performance metrics, and experiment history
2. Refresh videos that are >90 days old -- even winning videos decay as market context changes
3. Retire videos that have been shown to >70% of the addressable prospects in their segment (audience saturation)

**Human action required:** Monthly video refresh recording sessions. Agent identifies which videos need refreshing and provides updated scripts based on the latest winning patterns.

## Time Estimate

- Initial setup (monitoring, optimization loop, signal detection): 20 hours
- Monthly maintenance: 8 hours/month (4h founder video recording, 2h reviewing optimization briefs, 2h strategic decisions)
- Agent runs autonomously between human touchpoints
- **Total over 6 months: ~68 hours (20h setup + 48h maintenance)**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom | Record segment and personalized videos | $12.50/user/mo (Business) — [loom.com/pricing](https://www.loom.com/pricing) |
| Instantly | Cold email sequences at scale | $97/mo (Hypergrowth) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Clay | Automated enrichment + signal detection | $495/mo (Growth: CRM integrations) — [clay.com/pricing](https://www.clay.com/pricing) |
| PostHog | Event tracking, dashboards, experiments, anomaly detection | Free (1M events/mo) or $0.00031/event — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation: optimization loop, signal routing, reporting | Free (self-hosted) or $24/mo (cloud) — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | CRM deal pipeline + optimization audit trail | Free (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |
| Cal.com | Video CTA booking links | Free or $12/mo — [cal.com/pricing](https://cal.com/pricing) |
| Apollo | Prospect sourcing for signal-detection pipeline | $49/mo — [apollo.io/pricing](https://www.apollo.io/pricing) |
| Anthropic API | Hypothesis generation and experiment evaluation (Claude) | Pay-per-use ~$15-30/mo at this volume — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated Durable cost:** ~$700-1,200/mo (Clay Growth + Instantly Hypergrowth + Loom Business + Anthropic API + supporting tools)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, generate hypotheses, run A/B experiments, evaluate results, auto-implement winners, and detect convergence
- `video-outreach-performance-monitor` — PostHog dashboard, anomaly alerts, and weekly briefs for video-specific metrics
- `signal-detection` — continuous buying signal monitoring to refresh the prospect pipeline and prevent audience exhaustion

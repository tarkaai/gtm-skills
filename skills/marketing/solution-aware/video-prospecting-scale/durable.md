---
name: video-prospecting-scale-durable
description: >
  Video Prospecting at Scale — Durable Intelligence. Always-on AI agents find the
  local maximum of AI-generated video outreach through autonomous monitoring,
  hypothesis generation, A/B experimentation, and auto-implementation of winners.
  The optimization loop runs until successive experiments produce <2% improvement.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social"
level: "Durable Intelligence"
time: "Ongoing — 6 hours/month maintenance after initial 16-hour setup"
outcome: "Sustained >=5% response rate and >=8 meetings/month from AI video outreach over 6+ months via autonomous agent-driven optimization; convergence declared when 3 consecutive experiments produce <2% lift"
kpis: ["Sustained response rate", "Meetings booked per month", "AI experiment win rate", "Cost per meeting trend", "Weeks since last significant improvement"]
slug: "video-prospecting-scale"
install: "npx gtm-skills add marketing/solution-aware/video-prospecting-scale"
drills:
  - autonomous-optimization
  - signal-detection
---

# Video Prospecting at Scale — Durable Intelligence

> **Stage:** Marketing -> Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social

## Outcomes

Deploy an always-on AI agent loop that autonomously monitors AI video outreach performance, detects when metrics plateau or degrade, generates hypotheses for improvement, runs A/B experiments, evaluates results, and auto-implements winners. The agent finds the local maximum of this play -- the best achievable response rate and meeting rate given the current market, audience, AI video technology, and competitive landscape. When three consecutive experiments produce less than 2% improvement, the play has converged and the agent shifts to maintenance monitoring.

**Pass threshold:** Sustained response rate >=5% and >=8 meetings/month from AI video outreach over 6+ months. Convergence is the success state -- it means the play is optimized.

## Leading Indicators

- Autonomous optimization loop runs without human intervention for 4+ consecutive weeks
- At least 2 experiments completed per month with clear adopt/revert decisions
- Weekly optimization briefs generated automatically with actionable insights
- Video outreach performance does not degrade >20% from the Scalable baseline for more than 2 consecutive weeks without an automated corrective experiment being triggered
- Signal-based targeting continuously refreshes the prospect pool (no audience exhaustion)
- Cost per meeting trends flat or down over 6 months

## Instructions

### 1. Deploy the video outreach performance monitor

Run the `autonomous-optimization` drill to build the monitoring layer:

1. **Dashboard:** Create the PostHog "Video Prospecting at Scale -- Performance" dashboard with all video-specific panels: AI video engagement funnel, completion rate distribution, AI vs Loom comparison (if running both), engagement quality by ICP segment, pipeline impact, and cost efficiency trends.

2. **Anomaly detection:** Configure alerts for:
   - Response rate drops below 3% for 5 consecutive days
   - Video completion rate drops below 8% for 1 week
   - Meeting booking rate drops to 0 for 7+ days
   - Email bounce rate exceeds 3%
   - Negative reply rate exceeds 5% (prospects flagging AI quality or complaining)
   - Video generation error rate exceeds 10% (platform reliability issue)
   - Video view count drops 50%+ week over week

3. **Weekly briefs:** Set up the automated Monday morning brief covering: video funnel metrics with week-over-week deltas, top-performing ICP segments, script patterns from winning videos, A/B test status, and optimization recommendations.

4. **Structured data feed:** Ensure all metrics fire as structured PostHog events (`video_scale_weekly_summary`, `video_scale_anomaly`) that the autonomous optimization drill can consume.

### 2. Deploy signal-based prospect refresh

Run the `signal-detection` drill to prevent audience exhaustion:

1. Configure Clay to monitor buying signals daily: job changes at target accounts, funding announcements, technology adoption signals, hiring sprees in relevant roles, competitor mentions, intent data from third-party providers.

2. Score signals by recency (last 30 days strongest) and intensity (multiple signals from one account rank higher).

3. Route high-score signals into the video outreach pipeline automatically: new signal-detected prospects get added to the next weekly batch in Clay, pre-enriched with video scripts generated via AI formula.

4. Set up an n8n workflow that tracks "audience freshness": what percentage of prospects in the last 4 weeks were signal-detected vs cold-list. Target: >=40% signal-detected for higher conversion rates.

5. Build a "prospect exhaustion" alert: if the pipeline has contacted >60% of the addressable market in your ICP, flag for human strategic review (expand ICP, new verticals, new persona types, or new geographies).

### 3. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured specifically for AI video outreach at scale:

**Phase 1 -- Monitor (daily via n8n cron):**
1. Pull the last 2 weeks of video outreach KPIs from PostHog
2. Compare against the 4-week rolling average
3. Classify each KPI: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
4. If all normal: log to Attio, no action
5. If anomaly detected: trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**
1. Gather context from Attio: current video template in use, AI platform settings, ICP segments being targeted, send cadence, follow-up configuration, LinkedIn channel status
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` with anomaly data + video outreach context
4. Receive 3 ranked hypotheses. Examples of video-scale-specific hypotheses:
   - "Response rate dropped because the AI-generated videos for the Fintech CTO segment sound too scripted. Hypothesis: switching from Sendspark name-swap to Tavus full-lip-sync for this segment will restore response rate."
   - "Video completion rate dropped because the 90-second template is losing viewers after the hook. Hypothesis: a 45-second template with the value prop front-loaded will increase completion rate by 20%."
   - "Meeting rate dropped because the Cal.com CTA in the video is being ignored. Hypothesis: replacing 'Book 15 Minutes' with 'See a 5-Minute Demo' will increase CTA clicks by 15%."
   - "Response rate is flat because the ICP has been exhausted in the SaaS vertical. Hypothesis: expanding to fintech companies with the same persona will unlock a fresh addressable market."
   - "Email open rates dropped because the subject line has been used for 8 weeks. Hypothesis: rotating to a pain-point-based subject line will restore open rates."
5. Store hypotheses in Attio as campaign notes
6. If top hypothesis risk = "high" (e.g., requires ICP change affecting >50% of volume, or platform migration): alert human and STOP
7. If risk = "low" or "medium": proceed to Phase 3

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
1. Take the top-ranked hypothesis
2. Design the experiment using PostHog feature flags: split the next 200 prospects into control (current approach) and variant (hypothesis change)
3. Implement the variant:
   - For video template/length tests: record a new template video and generate a variant batch
   - For script structure tests: update the Clay AI formula to produce a different script pattern
   - For platform tests: generate the variant batch on a different AI video platform
   - For email subject/copy tests: create a variant Instantly campaign
   - For ICP expansion tests: source a variant batch from the new segment
   - For CTA tests: update the video CTA text/URL
4. Run the experiment for minimum 7 days or until 100+ prospects per variant
5. Log experiment start in Attio: hypothesis, start date, duration, success criteria

**Human action required for template experiments:** If the hypothesis involves recording a new template/training video (length change, script structure change, visual format change), the founder must record it. The agent designs the experiment, identifies what to test, and sets up the A/B split. Alert the founder via Slack with the exact recording brief: duration, script structure, and which segment this targets. Expected frequency: 1-2 re-recordings per quarter.

**Phase 4 -- Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation` comparing control vs variant on: response rate, video completion rate, meeting booking rate, and cost per meeting
3. Decision:
   - **Adopt:** Variant wins with >=90% confidence. Update the live pipeline configuration: swap template, update Clay formula, change Instantly campaign settings, or switch video platform. Log the change and the measured impact.
   - **Iterate:** Result inconclusive or partially positive. Generate a refined hypothesis. Return to Phase 2.
   - **Revert:** Variant lost. Restore control configuration. Log the failure reason. Return to Phase 1 monitoring.
4. Store the full evaluation in Attio with: decision, confidence level, effect size, reasoning

**Phase 5 -- Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes
3. Generate the weekly optimization brief:
   - What changed this week and why
   - Net impact on response rate, meeting rate, and cost per meeting
   - Current distance from estimated local maximum
   - Convergence status: are recent experiments producing diminishing returns?
4. Post to Slack and store in Attio

### 4. Configure convergence detection

The optimization loop detects when the play has reached its local maximum:

1. Track the improvement delta of each experiment over the last 3 months
2. If 3 consecutive experiments produce <2% improvement on the primary KPI (meetings booked):
   - Declare convergence
   - Reduce monitoring frequency from daily to weekly
   - Generate a convergence report: "AI video outreach is optimized. Current performance: {response_rate}% response rate, {meetings}/month meetings, ${cost_per_meeting} per meeting. This play produces approximately {N} meetings/month at current volume. Further gains require strategic changes: new ICP segments, new channels (LinkedIn video ads, retargeting), next-generation AI video technology, or product positioning changes."
3. Continue weekly monitoring to catch external disruptions (competitor enters market, email deliverability changes, AI video platform changes, ICP market shifts)

### 5. Maintain the video template library

As experiments run and winners are adopted, maintain the template library:

1. Keep a registry in Attio: each template video with its creation date, performance metrics, ICP segment, and experiment history
2. Refresh templates that are >90 days old -- even winning templates decay as prospects in the same market see similar AI video outreach from competitors
3. Test new AI video platforms as they emerge -- the AI video space evolves rapidly. Evaluate new entrants quarterly.
4. Monitor prospect feedback for AI detection: if prospects start commenting that videos "feel AI-generated," that is a signal to upgrade platform quality or adjust personalization depth

**Human action required:** Quarterly template refresh recording sessions (~30 minutes). Agent identifies which templates need refreshing and provides updated scripts based on winning patterns.

## Time Estimate

- Initial setup (monitoring, optimization loop, signal detection): 16 hours
- Monthly maintenance: 6 hours/month (2h reviewing optimization briefs and approving experiments, 2h strategic decisions, 2h template re-recording if needed)
- Agent runs autonomously between human touchpoints
- **Total over 6 months: ~52 hours (16h setup + 36h maintenance)**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Sendspark or Tavus | AI-personalized video generation at scale | Sendspark $99/mo (Growth) or Tavus $199/mo (Business) — [sendspark.com](https://www.sendspark.com), [tavus.io/pricing](https://www.tavus.io/pricing) |
| HeyGen | Alternative/additional AI video platform for experiments | $330/mo (Scale) — [heygen.com/pricing](https://www.heygen.com/pricing) |
| Instantly | Cold email sequences at scale | $97/mo (Hypergrowth) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Clay | Automated enrichment + signal detection + AI scripts | $495/mo (Growth: CRM integrations, auto-refresh) — [clay.com/pricing](https://www.clay.com/pricing) |
| PostHog | Event tracking, dashboards, experiments, anomaly detection | Free (1M events/mo) or $0.00031/event — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Full pipeline automation + optimization loop | Free (self-hosted) or $24/mo (cloud) — [n8n.io/pricing](https://n8n.io/pricing) |
| Attio | CRM + optimization audit trail | Free (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |
| LinkedIn Sales Navigator | Signal detection + LinkedIn outreach | $99/mo — [linkedin.com/sales](https://www.linkedin.com/sales/) |
| Anthropic API | Hypothesis generation + experiment evaluation (Claude) | ~$15-30/mo at this volume — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Cal.com | Booking links for video CTAs | Free or $12/mo — [cal.com/pricing](https://cal.com/pricing) |

**Estimated Durable cost:** ~$800-1,300/mo (Clay Growth + video platform + Instantly Hypergrowth + LinkedIn Sales Nav + Anthropic API + supporting tools)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, generate hypotheses, run A/B experiments, evaluate results, auto-implement winners, and detect convergence
- `autonomous-optimization` — PostHog dashboard, anomaly alerts, and weekly briefs for AI video outreach metrics
- `signal-detection` — continuous buying signal monitoring to refresh the prospect pipeline and prevent audience exhaustion

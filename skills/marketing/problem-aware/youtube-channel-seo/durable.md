---
name: youtube-channel-seo-durable
description: >
  YouTube Channel SEO — Durable Intelligence. Always-on AI agent continuously monitors YouTube
  metrics, detects anomalies, generates optimization hypotheses, runs experiments, and
  auto-implements winners to find and maintain the channel's local maximum.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Durable Intelligence"
time: "Ongoing (5 hours/month agent maintenance + founder recording)"
outcome: "Sustained or improving YT_SEARCH views and website referrals over 6 months with <5 hours/month manual effort. Convergence: successive experiments produce <2% improvement for 3 consecutive cycles."
kpis: ["YT_SEARCH views trend (MoM)", "CTR trend (MoM)", "Average view percentage trend", "Subscriber growth rate", "Website referrals/month", "Experiment win rate", "Time to convergence"]
slug: "youtube-channel-seo"
install: "npx gtm-skills add marketing/problem-aware/youtube-channel-seo"
drills:
  - autonomous-optimization
  - youtube-channel-analytics
---

# YouTube Channel SEO — Durable Intelligence

> **Stage:** Marketing > Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Outcomes

The YouTube channel runs itself. An always-on AI agent monitors performance, detects when metrics plateau or drop, generates hypotheses for improvement, runs controlled experiments, evaluates results, and auto-implements winners. The agent finds the channel's local maximum — the best achievable performance given the current audience, competition, and content library — and maintains it as conditions change.

Human involvement reduces to recording videos and approving high-risk changes. Everything else is autonomous.

## Leading Indicators

- The autonomous optimization loop runs daily without errors
- At least 1 experiment runs per month (agent is actively optimizing)
- Experiment win rate >=40% (hypotheses are well-targeted)
- Weekly optimization briefs are generated and delivered on schedule
- YT_SEARCH traffic is flat or growing (no undetected declines)
- When an experiment fails, the agent auto-reverts and tries a different hypothesis

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the YouTube Channel SEO play.

**Phase 1 — Monitor (daily via n8n cron):**

The agent checks the YouTube channel's primary KPIs daily using the `youtube-channel-analytics` drill data in PostHog:
- Pull last 14 days of YT_SEARCH views, CTR, average view percentage, and subscriber growth
- Compare against 4-week rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If all metrics are normal, log to Attio and take no action
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**

The agent gathers context and generates improvement hypotheses:
1. Pull the channel's current state from PostHog: video leaderboard, traffic source mix, search term rankings, content effectiveness scatter plot
2. Pull recent changes: any videos published, metadata updated, or experiments concluded in the last 14 days
3. Run the `hypothesis-generation` fundamental with anomaly data + context
4. Receive 3 ranked hypotheses. Examples of YouTube-specific hypotheses:
   - "CTR dropped because recent thumbnails lack face close-ups. Test: redesign thumbnails for the 5 lowest-CTR videos with face-forward designs."
   - "Search traffic plateaued because top-performing keywords are saturated. Test: target 10 new long-tail keywords in the next content batch."
   - "Average view percentage dropped because recent videos are 15+ minutes. Test: produce next 4 videos at 8-10 minutes."
   - "Suggested traffic declined because playlist structure doesn't chain related videos. Test: reorganize playlists by topic cluster and update end screens."
5. Store hypotheses in Attio as notes on the YouTube Channel SEO campaign record
6. If the top hypothesis is flagged as high risk (e.g., changing the channel's core topic, deleting videos, major format change), send alert for human review and STOP
7. If risk is low or medium, proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

The agent implements the experiment:
1. Take the top-ranked hypothesis
2. Design the experiment with a control and variant:
   - For metadata changes: use the youtube seo optimization workflow (see instructions below) to update the variant group of videos, leave control group unchanged
   - For content format tests: produce the next 2 videos in the new format, compare against the prior 2 videos of similar topic
   - For thumbnail tests: use TubeBuddy A/B test on the target videos
3. Set experiment duration: minimum 14 days or until each variant has >=500 impressions
4. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria, video IDs involved

**Phase 4 — Evaluate (triggered by experiment end):**

1. Pull experiment results from PostHog and YouTube Analytics
2. Run the `experiment-evaluation` fundamental: compare control vs variant on the target metric
3. Decision:
   - **Adopt**: Variant outperforms control with >95% confidence. Apply the winning change to all applicable videos. Log the win. Move to Phase 5.
   - **Iterate**: Results are inconclusive or marginal (<5% improvement). Generate a refined hypothesis. Return to Phase 2.
   - **Revert**: Variant underperforms control. Restore original state. Log the failure. Return to Phase 1 monitoring. Observe 7-day cooldown before testing the same variable.
   - **Extend**: Not enough data yet. Keep running for another period.
4. Store full evaluation in Attio: decision, confidence level, metric impact, reasoning

**Phase 5 — Report (weekly via n8n cron):**

Generate a weekly optimization brief:
- Anomalies detected this week and how they were classified
- Experiments in progress: hypothesis, current data, expected completion date
- Experiments concluded: what was tested, what happened, what was decided
- Net metric change from all adopted changes this month
- Current estimated distance from local maximum
- Recommended focus for next week

Deliver the brief to Slack and store in Attio.

### 2. Maintain content production with agent-driven topic selection

The agent uses analytics data to select what to produce next:
1. Weekly, the agent reviews the search term report from `youtube-channel-analytics`
2. Identifies search queries that drove views but have no dedicated video (content gap)
3. Identifies which content series have the highest retention and subscriber conversion
4. Generates the next 2-week content brief: topics, titles, target keywords, format, and duration
5. **Human action required:** Founder reviews the brief, records the videos

This replaces manual content calendar management. The agent picks topics based on what the data says works.

### 3. Run ongoing SEO maintenance

Run the youtube seo optimization workflow (see instructions below) monthly as part of the optimization loop:
- Re-score all videos' SEO health
- Identify videos whose search traffic has declined (keyword competition may have increased)
- Update metadata for declining videos: refresh titles with current year, update descriptions, add new tags
- Upload corrected captions for any videos still using auto-generated captions
- Flag videos for thumbnail refresh if CTR has dropped below 3%

### 4. Detect convergence

The optimization loop runs indefinitely. The agent monitors for convergence:
- Track the magnitude of improvement from each successive experiment
- If 3 consecutive experiments produce <2% improvement on the target metric, the channel has reached its local maximum

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency from monthly to quarterly
3. Generate a convergence report: current performance metrics, experiments run, total improvement from optimization phase, recommendation for next steps
4. Next-level growth requires strategic changes: new content formats (podcasts, live streams), new platforms (LinkedIn video, TikTok), or product changes that create new topics. These are human decisions, not agent experiments.

## Time Estimate

- Autonomous optimization loop: automated (agent runs daily, ~0 human hours)
- Weekly brief review: 30 min/week (2 hours/month)
- Content brief review and recording: 3 hours/month
- Monthly SEO maintenance review: 1 hour/month
- **Total human effort: ~5 hours/month + founder recording time**
- **Agent compute: ~$5-15/month for Claude API calls, n8n, and PostHog events**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| YouTube Data API v3 | Metadata updates, uploads | Free (10K units/day) |
| YouTube Analytics API | Performance data | Free |
| Anthropic API (Claude) | Hypothesis generation, evaluation, briefs | ~$5-15/mo at this usage level |
| n8n | Orchestrate the optimization loop | Self-hosted free or $20/mo cloud |
| PostHog | Metrics storage, anomaly detection, experiments | Free tier or usage-based |
| TubeBuddy | A/B testing thumbnails/titles | $14.50/mo Legend |
| Descript | Video editing | $24/mo Creator |
| Attio | Campaign records, experiment log, audit trail | Per CRM plan |

**Play-specific cost:** ~$65-95/mo (excluding standard stack)

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- `autonomous-optimization` — the core monitor > diagnose > experiment > evaluate > implement loop that makes Durable fundamentally different from Scalable
- `youtube-channel-analytics` — daily data sync, dashboards, and anomaly alerts feeding the optimization loop
- the youtube seo optimization workflow (see instructions below) — monthly metadata and caption maintenance run as part of the optimization cycle

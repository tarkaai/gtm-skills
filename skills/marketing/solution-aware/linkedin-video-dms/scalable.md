---
name: linkedin-video-dms-scalable
description: >
  LinkedIn Video DMs — Scalable Automation. Scale from 100 to 300+ video DMs per month with n8n
  automation for follow-up routing, A/B testing of video scripts and DM copy, and Clay-powered
  signal-based prospect prioritization. Maintain >=8% response rate at 3x volume.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Social"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: ">=8% response rate at 300 video DMs/month over 3 months"
kpis: ["Monthly video DM volume", "Response rate", "Video watch rate", "Meeting booking rate", "Cost per meeting", "Automation-handled follow-up ratio"]
slug: "linkedin-video-dms"
install: "npx gtm-skills add marketing/solution-aware/linkedin-video-dms"
drills:
  - follow-up-automation
  - ab-test-orchestrator
  - signal-detection
---

# LinkedIn Video DMs — Scalable Automation

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Social

## Outcomes

Find the 10x multiplier for LinkedIn video DMs. The bottleneck from Baseline is manual follow-up management and unoptimized video scripts. At Scalable, n8n automates engagement-based follow-up routing, A/B tests optimize every variable (video length, hook type, DM copy, send timing), and Clay signal detection prioritizes the highest-intent prospects for video recording. Target: 300+ video DMs per month with >=8% response rate sustained over 3 months.

## Leading Indicators

- Follow-up automation handling >=70% of post-send routing without manual intervention
- A/B tests producing statistically significant winners within 2-week cycles
- Signal-detected prospects converting at >=1.5x the rate of non-signal prospects
- Video recording throughput: 15+ videos per recording session (up from 7-10 at Baseline)
- Cost per meeting trending down month-over-month as winning variants compound

## Instructions

### 1. Automate follow-up routing with n8n

Run the `follow-up-automation` drill to build n8n workflows that replace manual follow-up decisions:

**Workflow 1 — Loom engagement router (runs every 4 hours on business days):**

1. Poll Loom API for new view events on active campaign videos.
2. For each new view, match the viewer to a prospect in Attio by email or by timing correlation (video viewed within 2 hours of DM send = likely the recipient).
3. Classify: high engagement (>75% watched), medium (25-75%), low (<25%).
4. Route to the appropriate follow-up action:
   - High + CTA clicked: create Attio deal at "Meeting Booked" stage, send Slack notification to founder.
   - High + no CTA: queue a personalized follow-up DM for manual send within 24 hours.
   - Medium: queue a text-only follow-up DM with alternate angle for Day 3.
   - Low: queue a final no-video-reference follow-up for Day 5.
5. Fire PostHog events: `video_dm_engagement_routed` with properties: branch, prospect_id, watch_pct.

**Workflow 2 — No-response escalation (runs daily at 6pm):**

1. Query Attio for prospects where `video_dm_sent = true` AND `video_dm_date` is 10+ days ago AND no response logged.
2. If prospect has not been routed to email: create a row in a Clay table tagged `channel-switch-email` and trigger the `cold-email-sequence` drill for these prospects.
3. Fire PostHog event: `video_dm_channel_switched` with properties: prospect_id, reason.

**Workflow 3 — Daily send-time optimizer (runs daily at 7am):**

1. Query PostHog for video_dm_watched events from the last 30 days, grouped by day_of_week and time_of_day.
2. Calculate watch rate by time slot.
3. Update a shared Attio note with the current best send windows.
4. Flag to the founder which time slots to prioritize for today's recording + sending session.

### 2. Launch A/B testing on video and DM variables

Run the `ab-test-orchestrator` drill to set up structured experiments. Run one experiment at a time, minimum 50 sends per variant before declaring a winner.

**Experiment queue (run in this order):**

1. **Video length:** 45 seconds vs 75 seconds vs 90 seconds. Measure: watch completion rate AND response rate. Shorter videos may get higher completion but lower conversion if the proof point is cut.

2. **Video hook type:** Signal-reference hook ("I saw your post about X") vs pain-question hook ("Are you dealing with X?") vs result-lead hook ("We helped {company} achieve X"). Measure: response rate.

3. **DM intro copy:** Short intro (under 150 chars, just "recorded a video for you") vs context intro (under 300 chars, includes the topic) vs question-lead intro ("Curious -- are you seeing X?"). Measure: video watch rate (the DM text determines whether they click).

4. **Send timing:** Morning (8-10am) vs midday (11am-1pm) vs late afternoon (3-5pm) in prospect's timezone. Measure: watch rate within 24 hours.

5. **Follow-up timing:** 3-day follow-up vs 5-day follow-up vs 7-day follow-up. Measure: incremental response rate from the follow-up.

Use PostHog feature flags to assign each prospect a variant at send time. Log the variant as a property on every event for that prospect. After 2 weeks per experiment (or 50+ sends per variant), evaluate results using PostHog experiments and adopt the winner.

### 3. Deploy signal-based prospect prioritization

Run the `signal-detection` drill to configure Clay for ongoing buying signal monitoring:

**High-priority signals (record a video within 48 hours):**
- Prospect posted about the problem your product solves in the last 7 days
- Company announced funding in the last 30 days
- Prospect changed jobs to your buyer persona title in the last 60 days
- Company hired 3+ roles in your product's domain in the last 30 days

**Medium-priority signals (add to warm-up pipeline):**
- Prospect engaged with a competitor's content
- Company appeared in a relevant industry report or article
- Prospect attended a relevant event or webinar

Configure Clay to score each prospect's signal strength (0-100). Feed the scored list into the daily recording queue. The founder always records videos for the highest-signal prospects first.

**n8n integration:** Build a workflow that pulls the daily top-10 signal-scored prospects from Clay, checks Attio for duplicates or existing conversations, and pushes a clean recording queue to the founder each morning.

### 4. Scale recording throughput

To sustain 300 video DMs per month (~15 per business day), optimize the recording process:

- **Batch recording sessions:** Record 15 videos in a 45-minute block instead of 7-10. Pre-open all prospect LinkedIn profiles in browser tabs. Use Clay-generated video hooks displayed on a second monitor for reference.
- **Segment-personalized videos:** For Tier 2 prospects (good fit but no unique signal), record one video per ICP segment (e.g., "Series A DevTools CTOs") that references segment-level pain points. Personalize only the opening 5 seconds with the prospect's name and company. This reduces recording time to 60 seconds per video.
- **Fully personalized videos:** Reserve for Tier 1 prospects (strongest signals). These get 90-second videos with deep signal references.

Target recording efficiency:
- Tier 1: 3 minutes per video, 5 per session
- Tier 2: 90 seconds per video, 10 per session

### 5. Monitor and maintain over 3 months

Check PostHog weekly dashboards:
- Monthly video DM volume (target: 300/month by month 2)
- Response rate by month (must stay >=8%)
- Response rate by experiment variant (adopt winners, retire losers)
- Signal-detected vs non-signal response rate comparison
- Cost per meeting trend line

**Monthly review cadence:**
- **Month 1:** Ramp to 200 DMs/month. Run experiments 1-2 (video length, hook type). Implement signal detection.
- **Month 2:** Ramp to 300 DMs/month. Run experiments 3-4 (DM copy, send timing). Adopt winning variants from month 1.
- **Month 3:** Sustain 300+ DMs/month. Run experiment 5 (follow-up timing). Compound all winning variants. Measure final cost per meeting.

**PASS (>=8% response rate at 300 DMs/month for 3 months):** Proceed to Durable. Document the winning configuration: optimal video length, best hook type, best DM copy, best send timing, best follow-up cadence, and signal-to-response correlation.

**FAIL:** Diagnose by comparing months:
- Response rate declining month-over-month: audience fatigue or ICP exhaustion. Expand to new ICP segments or rotate messaging angles.
- Response rate stable but volume below 300: recording throughput bottleneck. Introduce more segment-personalized videos.
- A/B tests producing no winners: test bigger changes (not incremental copy tweaks). Try video format changes (screen-only demo vs camera-only vs camera + screen).

## Time Estimate

- Follow-up automation setup: 4 hours
- A/B test framework setup: 3 hours
- Signal detection configuration: 3 hours
- Monthly recording and sending: 15 video DMs/day x 20 days/mo x 3 min = 15 hours/month
- Daily follow-up management (automated + manual review): 15 min/day x 60 days = 15 hours
- Weekly analysis and experiment evaluation: 1 hour/week x 12 weeks = 12 hours
- Monthly strategy reviews: 2 hours x 3 = 6 hours
- **Total: ~75 hours over 3 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom Business | Personalized video recording with CTAs and analytics | $12.50/creator/mo (annual) — [pricing](https://www.atlassian.com/software/loom/pricing) |
| LinkedIn Sales Navigator Core | InMail, advanced search, buyer intent signals | $79.99/mo (annual) — [pricing](https://business.linkedin.com/sales-solutions/compare-plans) |
| Clay | Prospect enrichment, signal detection, AI hook generation | $185/mo (Launch) or $495/mo (Growth) — [pricing](https://university.clay.com/docs/plans-and-billing) |
| n8n | Follow-up automation and tool sync workflows | $24/mo (Starter) — [pricing](https://n8n.io/pricing) |
| PostHog | Event tracking, funnels, A/B experiments, feature flags | Free up to 1M events/mo — [pricing](https://posthog.com/pricing) |
| Attio | CRM logging and deal tracking | Included in standard stack |
| Cal.com | Booking links for video CTAs | Included in standard stack |

**Play-specific cost at Scalable:** ~$117-$430/mo (Loom $12.50 + LinkedIn Sales Navigator $79.99 + n8n $24 + Clay $185-$495 if not already on standard stack). Estimated cost per meeting at 300 DMs/month with 8% response rate and 25% meeting conversion from responses: ~$18-$72/meeting.

## Drills Referenced

- `follow-up-automation` — n8n workflows for engagement-based follow-up routing and channel switching
- `ab-test-orchestrator` — structured A/B testing of video length, hook type, DM copy, send timing, and follow-up cadence
- `signal-detection` — Clay-powered buying signal monitoring to prioritize highest-intent prospects for video recording

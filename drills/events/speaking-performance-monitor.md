---
name: speaking-performance-monitor
description: Track speaking program ROI across conferences -- acceptance rates, lead yield per talk, content repurposing efficiency, and quarterly trend analysis
category: Events
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-funnels
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Speaking Performance Monitor

This drill builds always-on monitoring for a conference speaking program. It tracks the full lifecycle from CFP submission through talk delivery to lead attribution, surfacing which conferences produce the most pipeline and which talk topics resonate.

## Input

- PostHog instance with speaking events flowing (from `posthog-gtm-events` and `speaking-lead-capture` drills)
- Attio with CFP pipeline records (from `conference-cfp-pipeline` drill)
- n8n instance for scheduled monitoring workflows
- At least 3 talks delivered (minimum data for meaningful analysis)

## Steps

### 1. Build the speaking program dashboard

Using `posthog-dashboards`, create a "Speaking Program" dashboard with these panels:

**Panel 1: CFP Pipeline Funnel**
- Funnel: `speaking_cfp_submitted` -> `speaking_cfp_accepted` -> `speaking_talk_delivered` -> `speaking_meeting_booked`
- Breakdown by: conference size (small <200, medium 200-1000, large 1000+), talk format, topic track
- Time range: rolling 6 months

**Panel 2: Lead Yield Per Talk**
- Metric: total leads attributed to each talk (sum of `speaking_companion_page_viewed`, `speaking_meeting_booked`, `speaking_email_captured` unique users)
- Grouped by: conference name
- Sorted by lead count descending
- Shows which conferences produce the most leads per talk

**Panel 3: Acceptance Rate Trend**
- Line chart: monthly acceptance rate (accepted / submitted)
- Rolling 3-month average overlay
- Target line at your goal acceptance rate (aim for 30%+)

**Panel 4: Content Repurposing Multiplier**
- Ratio: total leads from repurposed content (social clips, blog posts) vs. in-room leads (QR + Cal.com day-of)
- Shows how much additional reach content repurposing adds
- Breakdown by content type: video clip, blog post, quote graphic

**Panel 5: Cost Per Lead**
- Total cost (travel + conference fees + tool costs) / total leads per conference
- Compare against other marketing channels' CPL
- Flag conferences where CPL exceeds 2x the program average

### 2. Set up automated alerts via n8n

Using `n8n-scheduling` and `n8n-workflow-basics`, create monitoring workflows:

**Alert 1: CFP acceptance rate drop**
- Trigger: weekly cron (Monday 9am)
- Check: if trailing 4-week acceptance rate drops below 20%, fire alert
- Action: post to Slack with recommendation to review proposal quality or conference targeting

**Alert 2: Post-talk lead capture failure**
- Trigger: 48 hours after each `speaking_talk_delivered` event
- Check: if zero `speaking_companion_page_viewed` or `speaking_email_captured` events exist for that talk
- Action: alert that lead capture infrastructure may have failed (QR code not working, companion page down)

**Alert 3: Follow-up sequence underperformance**
- Trigger: 14 days after each talk
- Check: if post-talk email sequence open rate < 30% or click rate < 5%
- Action: alert to review email copy and subject lines

### 3. Build quarterly analysis workflow

Using `n8n-scheduling`, create a quarterly analysis that runs on the 1st of each quarter:

1. Query PostHog for all speaking events in the prior quarter
2. Calculate:
   - Total CFPs submitted vs accepted (acceptance rate)
   - Total talks delivered
   - Total leads captured (by channel: QR, Cal.com, email, social)
   - Meetings booked from speaking leads
   - Lead-to-meeting conversion rate
   - Estimated pipeline value from speaking
   - Cost per lead by conference
3. Identify top 3 performing conferences (by leads per talk)
4. Identify bottom 3 conferences (retire or skip next year)
5. Identify top-performing talk topics (by acceptance rate AND lead yield)
6. Generate a quarterly brief using Claude:
   - What worked: top conferences, best talk topics, highest-yield content
   - What to change: underperforming conferences, low-acceptance topics
   - Recommended: conferences to target next quarter, new talk topics to develop
7. Store the brief in Attio as a note on the "Speaking Program" record
8. Post summary to Slack

### 4. Track talk topic lifecycle

Maintain a topic health tracker in Attio using `attio-reporting`:

- For each talk topic, track: times submitted, times accepted, times delivered, total leads generated
- Flag topics that have been given 3+ times (time to retire or refresh)
- Flag topics with high acceptance but low leads (engaging to reviewers but not to audiences)
- Flag topics with low acceptance but high leads when delivered (good content, bad proposals -- improve proposal writing)

## Output

- Real-time speaking program dashboard in PostHog
- Automated alerts for acceptance rate drops, lead capture failures, and sequence underperformance
- Quarterly speaking program analysis with recommendations
- Talk topic lifecycle tracking with retirement signals

## Triggers

- Dashboard updates in real-time as events flow
- Alerts run on their individual schedules (weekly, post-talk, post-sequence)
- Quarterly analysis runs on the 1st of each quarter
- Topic lifecycle review runs monthly

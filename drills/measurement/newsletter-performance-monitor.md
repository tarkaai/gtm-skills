---
name: newsletter-performance-monitor
description: Continuous monitoring and reporting system for developer newsletter performance with anomaly detection and subscriber-to-pipeline attribution
category: Measurement
tools:
  - PostHog
  - Attio
  - n8n
  - Loops
  - Anthropic Claude API
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-funnels
  - loops-audience
  - loops-broadcasts
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Newsletter Performance Monitor

This drill builds the always-on monitoring and reporting system specific to developer newsletter plays. It tracks the full funnel from issue sent to pipeline created, detects anomalies in newsletter health, and generates weekly reports that feed into the `autonomous-optimization` drill's experiment loop.

## Input

- PostHog with newsletter events flowing (from `posthog-gtm-events` drill)
- Loops account with newsletter sending data
- Attio with lead records attributed to the newsletter
- At least 4 weeks of consistent newsletter data (baseline for anomaly detection)
- n8n instance for automated monitoring

## Steps

### 1. Build the Newsletter Performance Dashboard

Using the `posthog-dashboards` fundamental, create a "Developer Newsletter" dashboard:

**Panel 1 -- Issue Health:**
- Trend: open rate per issue (12-issue rolling)
- Trend: click rate per issue (12-issue rolling)
- Trend: unsubscribe rate per issue (should stay below 0.5%)
- Bar chart: open rate by issue topic/content pillar
- Number: current total subscribers, net change this week

**Panel 2 -- Subscriber Growth:**
- Trend: net new subscribers per week (signups minus unsubscribes)
- Breakdown: subscriber acquisition by source (website, social, referral, product, lead-magnet)
- Trend: subscriber growth rate (% week over week)
- Trend: referral coefficient (referral-sourced / total new)

**Panel 3 -- Engagement Depth:**
- Trend: average clicks per subscriber per issue
- Trend: reply rate per issue (replies / delivered)
- Bar chart: click-through by link position (which links in the newsletter get clicked most)
- Cohort retention: what % of subscribers who joined in week N are still opening 4/8/12 weeks later

**Panel 4 -- Newsletter-to-Pipeline Attribution:**
- Funnel: newsletter_opened -> link_clicked -> page_visited -> lead_captured -> meeting_booked -> deal_created
- Trend: leads generated per issue
- Trend: meetings booked per issue
- Number: total pipeline value attributed to newsletter this month
- Table: top 5 newsletter issues by leads generated (issue title, topic, leads, meetings, pipeline value)

**Panel 5 -- Content Effectiveness:**
- Bar chart: open rate by subject line style (question, statistic, how-to, listicle, announcement)
- Bar chart: click rate by content type (tutorial, industry insight, code example, tool review, opinion)
- Trend: best-performing content pillar over time (detect pillar fatigue)

### 2. Configure anomaly detection

Using the `posthog-anomaly-detection` fundamental, set up monitoring for these signals:

**Deliverability anomalies (check per send):**
- Bounce rate exceeds 3% on any issue -> trigger: "deliverability-issue"
- Open rate drops >20% vs 4-issue rolling average -> trigger: "open-rate-decline"
- Unsubscribe rate exceeds 1% on any issue -> trigger: "content-mismatch"

**Engagement anomalies (check daily):**
- Click rate drops >30% vs 4-issue rolling average -> trigger: "engagement-decline"
- Zero replies received on an issue (when baseline is 3+/issue) -> trigger: "reply-drought"
- Spam complaint rate exceeds 0.1% -> trigger: "spam-risk"

**Growth anomalies (check weekly):**
- Net subscribers negative for 2 consecutive weeks -> trigger: "subscriber-churn"
- Referral signups drop to zero for 3 consecutive weeks -> trigger: "referral-stall"
- No new subscribers from social channel for 2 weeks -> trigger: "social-funnel-broken"

Each anomaly trigger feeds into the `autonomous-optimization` drill's Phase 2 (Diagnose).

### 3. Build the subscriber lifecycle tracking system

Track individual subscriber journeys to identify patterns:

Using `posthog-custom-events` and `loops-audience`, implement:

1. `newsletter_issue_sent` — properties: issue_number, subject_line, subject_style, content_pillar, link_count, word_count
2. `newsletter_issue_opened` — properties: subscriber_id, issue_number, device_type, time_to_open_hours
3. `newsletter_link_clicked` — properties: subscriber_id, issue_number, link_url, link_position, content_type
4. `newsletter_reply_received` — properties: subscriber_id, issue_number, sentiment (positive/negative/question), buying_signal (true/false)
5. `newsletter_subscriber_churned` — properties: subscriber_id, issues_received, last_open_issue, tenure_weeks, churn_reason (unsubscribe/bounce/complaint)

Build a subscriber health score from these events: subscribers who open >80% of issues and click >30% are "highly engaged." Subscribers who have not opened in 4+ issues are "at risk." Feed this into Loops segments for targeted re-engagement or cleanup.

### 4. Automate weekly performance reports

Using `n8n-scheduling` and `n8n-workflow-basics`, build a weekly report workflow:

**Trigger:** Monday at 9am (after weekend issue analytics stabilize)

**Data collection:**
1. Pull last issue's performance from Loops API (open rate, click rate, unsubscribes, bounces)
2. Pull subscriber growth data from Loops API (new, churned, net)
3. Pull lead and meeting attribution from Attio using `attio-reporting`
4. Pull website traffic from newsletter clicks via PostHog

**Report generation:**
Use Claude API to generate a narrative report:

```
Prompt: "You are analyzing a developer newsletter's performance. Here is this week's data: {DATA}. Compare to the 4-issue rolling average: {BASELINE}. Generate a report with:
1. Executive summary (2 sentences: what's working, what's not)
2. Key metrics table (this issue vs last issue vs 4-issue avg): open rate, click rate, unsub rate, replies, leads, subscribers added
3. Subject line analysis: which style was used, how it performed vs history
4. Content analysis: which links got the most clicks, what content type drove engagement
5. Subscriber health: % highly engaged, % at risk, churn this week
6. Recommended experiments for next issue (1-2 specific tests)
Keep it under 500 words. Use specific numbers."
```

**Delivery:**
- Post to Slack channel
- Store in Attio as a note on the newsletter campaign record
- If any anomaly was detected, prepend: "ANOMALY: {type} — recommended action: {action}"

### 5. Build monthly content strategy reports

First Monday of each month, generate a deeper analysis:

- Content pillar performance ranking: which topics drive opens vs clicks vs leads (they are often different)
- Subject line style leaderboard: which styles consistently outperform
- Subscriber cohort retention: are subscribers from month N still opening after 3 months?
- Newsletter-to-pipeline: total pipeline value attributed this month, cost per newsletter-sourced lead
- Content freshness: are certain topics showing fatigue (declining engagement over successive issues)?
- Experiment summary: what was tested, what was learned, what should be tested next month

### 6. Set up alert routing

Build n8n alert workflows for critical events:

- **Immediate Slack alert:** When a reply contains a buying signal keyword (pricing, demo, trial, budget, timeline)
- **Immediate Slack alert:** When bounce rate exceeds 3% (deliverability emergency)
- **Daily digest:** New leads attributed to the newsletter, subscriber count milestone notifications
- **Weekly flag:** If no A/B tests ran on the last 2 issues (optimization stall)

## Output

- Real-time PostHog dashboard with 5 panels covering issue health, growth, engagement, pipeline, and content effectiveness
- Anomaly detection feeding into autonomous optimization loop
- Full subscriber-to-pipeline attribution tracking
- Automated weekly and monthly performance reports
- Alert routing for buying signals and deliverability issues

## Triggers

Dashboard is always-on. Anomaly detection runs per-send and daily via n8n. Weekly reports fire every Monday at 9am. Monthly reports fire first Monday of each month. Buying signal alerts fire in real-time via webhook.

---
name: pr-performance-monitor
description: Continuous monitoring and reporting system for PR and earned media performance with anomaly detection and placement-to-pipeline attribution
category: Media
tools:
  - PostHog
  - Attio
  - n8n
  - Mention
  - Anthropic Claude API
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-funnels
  - media-monitoring-api
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# PR Performance Monitor

This drill builds the always-on monitoring and reporting system specific to PR and earned media plays. It tracks the full funnel from pitch sent to placement published to referral traffic to leads captured, detects anomalies in PR performance, and generates weekly reports that feed into the `autonomous-optimization` drill's experiment loop.

## Input

- PostHog with PR events flowing (from `posthog-gtm-events` drill)
- Attio with media contact records and placement log
- Mention account with brand monitoring configured
- At least 4 weeks of Scalable-level PR data (baseline for anomaly detection)
- n8n instance for automated monitoring

## Steps

### 1. Build the PR Performance Dashboard

Using the `posthog-dashboards` fundamental, create a "PR & Earned Media" dashboard:

**Panel 1 -- Outreach Pipeline:**
- Trend: pitches sent per week by outlet type (journalist / newsletter / podcast)
- Funnel: pitch_sent -> pitch_opened -> pitch_replied -> placement_secured
- Conversion rates: pitch-to-reply rate, reply-to-placement rate, overall pitch-to-placement rate
- Table: outstanding pitches by status (sent, interested, covering, no response)

**Panel 2 -- Placement Tracking:**
- Trend: placements published per week (4-week rolling)
- Breakdown: placements by outlet type and tier
- Cumulative: total placements since play start
- Table: recent placements with outlet, date, URL, and initial traffic

**Panel 3 -- Referral Traffic:**
- Trend: referral clicks from earned media per week (4-week rolling)
- Breakdown: referral traffic by outlet/placement
- Comparison: earned media referral traffic vs other channels
- Table: top 10 placements by referral traffic (all-time)

**Panel 4 -- Placement-to-Pipeline Attribution:**
- Funnel: placement_published -> referral_click -> page_view -> lead_captured -> meeting_booked -> deal_created
- Number: total pipeline value attributed to earned media this month
- Trend: leads from earned media per week
- Table: placements that generated leads (outlet, URL, leads, pipeline value)

**Panel 5 -- Media Relationship Health:**
- Number: total active media contacts (pitched in last 90 days)
- Distribution: contacts by relationship score (0-5)
- Trend: source requests answered per week (Qwoted, Featured.com)
- Hit rate: source request submissions that resulted in placements

### 2. Implement PR event taxonomy

Using `posthog-custom-events`, define these PR-specific events:

1. `pr_pitch_sent` -- properties: outlet_name, outlet_type, journalist_name, pitch_angle, tier, campaign
2. `pr_pitch_opened` -- properties: outlet_name, journalist_name (from Instantly tracking)
3. `pr_pitch_replied` -- properties: outlet_name, journalist_name, reply_sentiment (positive/neutral/negative)
4. `pr_placement_secured` -- properties: outlet_name, outlet_type, journalist_name, expected_publish_date
5. `pr_placement_published` -- properties: outlet_name, outlet_type, url, estimated_reach, backlink_da
6. `pr_referral_click` -- properties: source_outlet, placement_url, landing_page (tracked via UTM parameters)
7. `pr_lead_from_media` -- properties: source_outlet, placement_url, lead_name, lead_company
8. `pr_source_request_answered` -- properties: platform (qwoted/featured), topic, journalist_name, deadline
9. `pr_source_request_placed` -- properties: platform, topic, outlet_name, url
10. `pr_brand_mention_detected` -- properties: outlet_name, url, sentiment, reach (from Mention API)

### 3. Configure anomaly detection

Using `posthog-anomaly-detection`, monitor for these signals:

**Outreach anomalies (check daily):**
- Pitch-to-reply rate drops >30% vs 4-week rolling average -> trigger: "pitch-reply-decline"
- Zero placements in 14 days when baseline is 1+/week -> trigger: "placement-drought"
- Reply sentiment shifts negative (>20% negative replies in a week) -> trigger: "pitch-quality-decline"

**Traffic anomalies (check daily):**
- Referral clicks from earned media drop >40% vs 4-week rolling average -> trigger: "referral-decline"
- Zero leads from earned media in 14 days when baseline is 1+/week -> trigger: "lead-drought"

**Opportunity anomalies (check weekly):**
- Source request answer rate drops below 50% (missing opportunities) -> trigger: "response-lag"
- No new media targets added in 30 days -> trigger: "list-stale"
- Competitor mention volume spikes >2x (competitor getting more coverage) -> trigger: "competitor-surge"

Each anomaly trigger automatically feeds into the `autonomous-optimization` drill's Phase 2 (Diagnose).

### 4. Build referral traffic attribution

Track the complete journey from placement to revenue:

**UTM structure for earned media:**
```
?utm_source={outlet_slug}&utm_medium=earned&utm_campaign=pr-earned&utm_content={placement_id}
```

When providing links to journalists, always include these UTMs. For placements where you cannot control the link (journalist writes their own), use Mention API to detect the placement and track referral traffic via the `document.referrer` in PostHog.

**Attribution flow:**
1. Placement publishes with UTM link or detected by Mention
2. PostHog captures `pr_referral_click` with source outlet
3. If visitor converts (lead capture form, demo request), PostHog attributes `first_touch_source = earned_media` and `first_touch_detail = {outlet_name}`
4. When a deal closes, the attribution chain traces back to the originating placement

### 5. Automate weekly performance reports

Using `n8n-scheduling`, build a weekly report workflow:

**Trigger:** Monday at 9am

**Data collection:**
1. Pull last 7 days of PR events from PostHog API
2. Pull media contact activity from Attio using `attio-reporting`
3. Pull brand mention data from Mention API using `media-monitoring-api`

**Report generation:**
Use Claude API to generate a narrative report:

```
Prompt: "You are analyzing a PR and earned media program for the past week. Here is the data: {DATA}. Compare to the 4-week rolling average: {BASELINE}. Generate a report with:
1. Executive summary (2 sentences: what's working, what's not)
2. Key metrics table: pitches sent, replies, placements, referral clicks, leads -- this week vs last week vs 4-week avg
3. New placements this week (outlet, URL, early traffic data)
4. Outreach pipeline status (pitches outstanding, responses pending)
5. Source request activity (answered, placed, missed)
6. Anomalies detected and recommended actions
7. Recommended experiments (1-2 specific tests for next week)
Keep it under 500 words. Use specific numbers."
```

**Delivery:**
- Post to Slack #pr-performance channel
- Store in Attio as a note on the PR campaign record
- If any anomaly was detected, add: "ANOMALY DETECTED: {type} -- recommended action: {action}"

### 6. Build monthly deep-dive reports

Monthly report (first Monday):

**Additional monthly analysis:**
- Outlet type performance: which outlet types (journalists / newsletters / podcasts) produce the most referral traffic and leads per pitch sent?
- Pitch angle ranking: which angles have the highest placement rate?
- Tier analysis: are Tier 1 targets worth the extra effort vs Tier 2 and 3?
- Backlink analysis: track domain authority of backlinks from placements
- Share of voice: brand mentions vs competitor mentions (from Mention API)
- Cost per placement: total time + tool costs / placements secured
- Experiment results: which optimization experiments ran and what was learned

## Output

- Real-time PostHog dashboard with 5 panels covering outreach, placements, traffic, attribution, and relationships
- Full PR event taxonomy tracking every stage from pitch to pipeline
- Anomaly detection feeding into autonomous optimization loop
- Referral traffic attribution from placement to revenue
- Automated weekly and monthly performance reports

## Triggers

Dashboard is always-on. Anomaly detection runs daily via n8n. Weekly reports fire every Monday at 9am. Monthly reports fire first Monday of each month.

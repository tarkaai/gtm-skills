---
name: thought-leadership-performance-monitor
description: Continuous monitoring and reporting for thought leadership program — content performance, audience growth, pipeline attribution, and speaking ROI
category: Thought Leadership
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic Claude API
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-funnels
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Thought Leadership Performance Monitor

This drill builds the always-on monitoring and reporting system for a thought leadership program. It tracks the full funnel from content published to audience growth to leads captured to pipeline influenced, detects anomalies in content performance, and generates weekly reports that feed into the `autonomous-optimization` drill's experiment loop.

## Input

- PostHog with thought leadership events flowing
- Attio with content records and lead attribution
- At least 4 weeks of Scalable-level thought leadership data (baseline for anomaly detection)
- n8n instance for automated monitoring

## Steps

### 1. Build the Thought Leadership Dashboard

Using the `posthog-dashboards` fundamental, create a "Thought Leadership Program" dashboard:

**Panel 1 — Content Output:**
- Trend: posts published per week by platform (LinkedIn, Twitter, blog)
- Breakdown: posts by content pillar
- Table: last 10 posts with engagement rate, impressions, and ICP comment count

**Panel 2 — Engagement Metrics:**
- Trend: average engagement rate per week (4-week rolling)
- Trend: total impressions per week (4-week rolling)
- Breakdown: engagement rate by content pillar and format
- Number: average comments per post (this week vs last week)

**Panel 3 — Audience Growth:**
- Trend: LinkedIn follower count per week (manual or Taplio import)
- Trend: newsletter subscriber count per week (if applicable)
- Number: new LinkedIn connections from ICP titles this month

**Panel 4 — Content-to-Pipeline Attribution:**
- Funnel: content_published -> content_engaged -> profile_visit -> website_visit -> lead_captured -> meeting_booked -> deal_created
- Number: total pipeline value attributed to thought leadership content this month
- Table: posts that generated leads (post URL, lead name, deal stage)

**Panel 5 — Speaking Program:**
- Number: CFP submissions this quarter, acceptances, talks delivered
- Table: upcoming speaking slots with event name, date, expected audience size
- Number: leads attributed to speaking engagements this quarter

### 2. Implement the thought leadership event taxonomy

Using `posthog-custom-events`, define these events:

1. `tl_content_published` — properties: platform, pillar, format, hook_type, word_count
2. `tl_content_engagement` — properties: platform, post_id, impressions, engagement_rate, comments, icp_comments
3. `tl_profile_visit` — properties: source (organic, post_link, speaking_bio), visitor_title (if known)
4. `tl_content_lead` — properties: source_post_id, source_platform, lead_name, lead_company, lead_title
5. `tl_speaking_submitted` — properties: event_name, cfp_deadline, topic, expected_audience
6. `tl_speaking_accepted` — properties: event_name, talk_date, expected_audience
7. `tl_speaking_delivered` — properties: event_name, actual_audience, leads_captured
8. `tl_newsletter_subscriber` — properties: source (content_cta, speaking, organic)
9. `tl_content_repurposed` — properties: source_post_id, target_format, target_platform

### 3. Configure anomaly detection

Using `posthog-anomaly-detection`, monitor for:

**Content anomalies (check daily):**
- Average engagement rate drops >30% vs 4-week rolling average -> trigger: "engagement-decline"
- Zero ICP comments in 7 days when baseline is 3+/week -> trigger: "icp-resonance-drop"
- Impressions drop >40% vs 4-week average -> trigger: "reach-decline"

**Growth anomalies (check weekly):**
- Follower growth rate drops below 50% of 4-week average -> trigger: "growth-stall"
- Zero content-attributed leads in 14 days when baseline is 1+/week -> trigger: "lead-drought"

**Speaking anomalies (check monthly):**
- CFP acceptance rate drops below 20% -> trigger: "cfp-quality-decline"
- No new speaking submissions in 30 days -> trigger: "speaking-pipeline-stale"

Each anomaly trigger feeds into the `autonomous-optimization` drill's Phase 2 (Diagnose).

### 4. Build content attribution tracking

Track the journey from content to revenue:

**UTM structure for thought leadership content:**
```
?utm_source={platform}&utm_medium=organic&utm_campaign=thought-leadership&utm_content={post_id}
```

Include these UTMs in all bio links, content CTAs, and speaking presentation links. For posts where UTMs are not possible (organic LinkedIn text posts), track via PostHog's referrer attribution.

**Attribution flow:**
1. Founder publishes content with CTA link (UTM-tagged)
2. PostHog captures `tl_content_lead` with source post
3. When lead converts (demo request, trial signup), PostHog attributes `first_touch_source = thought_leadership` and `first_touch_detail = {post_id}`
4. Pipeline value traced back through the originating content piece

### 5. Automate weekly performance reports

Using `n8n-scheduling`, build a weekly report workflow:

**Trigger:** Monday at 9am

**Data collection:**
1. Pull last 7 days of thought leadership events from PostHog API
2. Pull content records and lead attribution from Attio using `attio-reporting`

**Report generation:**
Use Claude API to generate a narrative report:

```
Prompt: "You are analyzing a thought leadership program for the past week. Data: {DATA}. 4-week baseline: {BASELINE}. Generate a report:
1. Executive summary (2 sentences)
2. Content output: posts published, by pillar and platform
3. Engagement: avg engagement rate, best post, worst post, ICP comment highlights
4. Audience growth: follower change, newsletter subscribers
5. Pipeline impact: leads attributed to content, pipeline value
6. Speaking pipeline: submissions, acceptances, upcoming talks
7. Anomalies detected and recommended actions
8. Recommended experiments for next week (1-2 specific tests)
Keep under 500 words. Use specific numbers."
```

**Delivery:**
- Post to Slack #thought-leadership channel
- Store in Attio as a note on the thought leadership campaign record

### 6. Monthly deep-dive report

Monthly report (first Monday):
- Content pillar performance: which pillars drive the most engagement and leads?
- Format analysis: which post formats (text, carousel, video) perform best per pillar?
- Hook type ranking: which hooks (personal story, data, contrarian) drive highest engagement?
- Posting time optimization: which days and times produce the best results?
- Speaking ROI: cost per lead from speaking vs content creation
- Competitive comparison: how does the founder's engagement compare to tracked competitors?
- Content velocity: time from idea to publish, and trend over time

## Output

- Real-time PostHog dashboard with 5 panels covering content, engagement, growth, attribution, and speaking
- Full thought leadership event taxonomy tracking every stage
- Anomaly detection feeding into the autonomous optimization loop
- Content-to-pipeline attribution
- Automated weekly and monthly performance reports

## Triggers

Dashboard is always-on. Anomaly detection runs daily via n8n. Weekly reports fire every Monday at 9am. Monthly reports fire first Monday of each month.

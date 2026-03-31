---
name: infographic-performance-monitor
description: Continuous monitoring of infographic engagement, backlink acquisition, and content-to-pipeline attribution with anomaly detection
category: Content
tools:
  - PostHog
  - Ahrefs
  - Attio
  - n8n
  - Anthropic Claude API
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-funnels
  - ahrefs-backlink-analysis
  - linkedin-organic-analytics
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Infographic Performance Monitor

This drill builds the always-on monitoring and reporting system for infographic and visual content plays. It tracks the full lifecycle from creation through social distribution, backlink acquisition, and pipeline attribution. Anomaly signals feed into the `autonomous-optimization` drill for automated experimentation.

## Input

- PostHog with infographic-specific events flowing (from `posthog-gtm-events` drill)
- Ahrefs API access for backlink tracking
- Attio with lead records attributed to infographic content
- At least 4 weeks of data at Scalable level (baseline for anomaly thresholds)
- n8n instance for scheduled monitoring jobs

## Steps

### 1. Build the Infographic Performance Dashboard

Using the `posthog-dashboards` fundamental, create an "Infographics & Visual Content" dashboard:

**Panel 1 -- Publishing Cadence:**
- Trend: infographics published per week
- Trend: infographics by topic/data category
- Trend: platform distribution (LinkedIn, Twitter, blog, Pinterest)
- Target overlay: minimum publishing cadence for current level

**Panel 2 -- Social Engagement:**
- Trend: average engagement rate per infographic (4-week rolling, by platform)
- Trend: average impressions per infographic (4-week rolling)
- Trend: shares per infographic (the key virality metric for visual content)
- Bar chart: engagement by topic category (which data topics resonate)
- Bar chart: engagement by visual format (single image vs carousel vs chart type)

**Panel 3 -- Backlink Acquisition:**
- Trend: new backlinks per week (from Ahrefs data synced via n8n)
- Trend: referring domains acquired per month
- Table: top backlinks by domain rating (linking site, DR, anchor text, infographic)
- Number: total dofollow backlinks this month
- Trend: average domain rating of new backlinks (quality indicator)

**Panel 4 -- Traffic and Pipeline:**
- Trend: organic traffic to infographic blog posts (from PostHog)
- Funnel: infographic_viewed -> blog_post_read -> lead_captured -> meeting_booked
- Number: leads attributed to infographic content this month
- Number: pipeline value attributed to infographic content

**Panel 5 -- Efficiency:**
- Calculated: backlinks per infographic (lifetime average)
- Calculated: cost per backlink (tool costs / backlinks acquired)
- Calculated: leads per infographic published
- Trend: time from publish to first backlink (velocity metric)

### 2. Configure anomaly detection

Using the `posthog-anomaly-detection` fundamental, monitor for:

**Engagement anomalies (check daily):**
- Average shares per infographic drops >30% vs 4-week rolling average -> trigger: "share-decline"
- Average impressions per infographic drops >25% vs 4-week rolling average -> trigger: "reach-decline"
- Zero social engagement on an infographic 48h after posting -> trigger: "dead-post"

**Backlink anomalies (check weekly):**
- Zero new backlinks in 14 days (when baseline is 2+/week) -> trigger: "backlink-drought"
- Average DR of new backlinks drops below 20 for 2 consecutive weeks -> trigger: "link-quality-decline"
- Lost backlinks exceed new backlinks for 2 consecutive weeks -> trigger: "net-negative-links"

**Traffic anomalies (check weekly):**
- Organic traffic to infographic pages drops >20% month-over-month -> trigger: "traffic-decline"
- Blog post bounce rate exceeds 85% for new infographic posts -> trigger: "content-mismatch"

Each anomaly trigger feeds into the `autonomous-optimization` drill's Phase 2 (Diagnose).

### 3. Automate backlink data sync

Using `n8n-scheduling` and `n8n-workflow-basics`, build a weekly backlink sync workflow:

**Trigger:** Every Monday at 6am

**Steps:**
1. Query Ahrefs API for new backlinks to all infographic blog post URLs since last sync
2. For each new backlink: record referring domain, domain rating, anchor text, dofollow status, first seen date
3. Match against outreach list in Attio to attribute: was this from an outreach email or organic?
4. Update PostHog with `backlink_acquired` events for dashboard tracking
5. Update Attio campaign record with backlink count and quality metrics

### 4. Automate weekly performance reports

Using `n8n-scheduling`, build a Monday report workflow:

**Data collection:**
1. Pull 7-day social engagement data from PostHog
2. Pull 7-day backlink data from Ahrefs
3. Pull lead attribution data from Attio using `attio-reporting`
4. Pull LinkedIn analytics using `linkedin-organic-analytics`

**Report generation via Claude:**
```
Prompt: "You are analyzing an infographic content program's weekly performance. Data: {DATA}. 4-week baseline: {BASELINE}. Generate a report:
1. Executive summary (2 sentences)
2. Infographics published this week and their engagement
3. Backlinks acquired (count, average DR, notable sites)
4. Social performance (top infographic by shares, worst by engagement)
5. Pipeline attribution (leads and meetings from infographic content)
6. Anomalies detected and recommended actions
7. Next week: topic recommendations based on what is trending
Keep under 600 words. Use specific numbers."
```

**Delivery:** Post to Slack, store in Attio.

### 5. Build monthly topic effectiveness analysis

Monthly report (first Monday of month):
- Rank all topics by: engagement rate, backlinks earned, leads generated
- Identify topic fatigue: topics where engagement is declining over 3+ months
- Identify rising topics: engagement increasing for 2+ consecutive months
- Recommend: topics to retire, topics to double down on, new topics to test
- Calculate: monthly ROI (tool costs + time vs backlinks + leads + pipeline value)

## Output

- Real-time PostHog dashboard with 5 panels
- Anomaly detection feeding into autonomous optimization loop
- Automated weekly backlink sync from Ahrefs
- Weekly and monthly automated performance reports
- Topic effectiveness rankings driving content strategy

## Triggers

Dashboard is always-on. Anomaly detection runs daily (engagement) and weekly (backlinks, traffic). Weekly reports fire Monday 9am. Monthly reports fire first Monday of month. Backlink sync runs weekly Monday 6am.

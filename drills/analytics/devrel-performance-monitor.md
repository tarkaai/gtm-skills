---
name: devrel-performance-monitor
description: Continuous monitoring and reporting system for developer advocacy programs with content-to-lead attribution, community health tracking, and speaking program ROI
category: Analytics
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic Claude API
  - GitHub
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-funnels
  - linkedin-organic-analytics
  - github-traffic-api
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Developer Advocacy Performance Monitor

This drill builds the always-on monitoring and reporting system for developer advocacy programs. It tracks three program pillars — technical content, conference speaking, and community engagement — from activity through to pipeline, detects anomalies, and feeds data into the `autonomous-optimization` drill's experiment loop.

## Input

- PostHog with devrel events flowing (from `posthog-gtm-events` drill)
- Attio with lead records attributed to devrel activities
- GitHub repos with traffic API access
- At least 4 weeks of Scalable-level program data (baseline for anomaly detection)
- n8n instance for automated monitoring

## Steps

### 1. Build the Developer Advocacy Dashboard

Using the `posthog-dashboards` fundamental, create a "Developer Advocacy Program" dashboard:

**Panel 1 -- Content Production:**
- Trend: tutorials published per week (blog + GitHub repos)
- Trend: social derivatives published per week by platform
- Trend: content pillar distribution (are you covering all pillars or over-indexing on one?)
- Target overlay: minimum publishing cadence per level

**Panel 2 -- Content Reach & Engagement:**
- Trend: blog post views per week (4-week rolling)
- Trend: GitHub repo clones + stars per week (aggregate across all sample repos)
- Trend: average engagement rate per social post (by platform)
- Bar chart: top 10 tutorials by total views this month
- Bar chart: top 10 GitHub repos by clones this month

**Panel 3 -- Community Health:**
- Trend: community posts/answers per week (Stack Overflow, Reddit, Discord, Slack)
- Trend: community engagement received (upvotes, replies, thanks)
- Number: active community threads this week
- Trend: community-attributed website visits per week

**Panel 4 -- Speaking Program:**
- Number: CFPs submitted this quarter
- Number: talks accepted this quarter
- Number: talks delivered this quarter
- Calculated: acceptance rate (accepted / submitted)
- Trend: leads captured per talk (rolling average)
- Table: upcoming accepted talks with dates

**Panel 5 -- Full-Funnel Attribution:**
- Funnel: content_published -> content_engaged -> website_visit -> lead_captured -> meeting_booked -> deal_created
- Trend: developer leads generated per week (by source: content, community, speaking)
- Number: total pipeline value attributed to devrel this month
- Trend: pipeline value per week (8-week rolling)
- Calculated: cost per developer lead (time + tool costs / leads)

**Panel 6 -- Efficiency:**
- Calculated: leads per hour of advocate time
- Calculated: pipeline value per tutorial published
- Calculated: pipeline value per talk delivered
- Trend: leads per content piece (is quality improving or degrading with volume?)

### 2. Configure anomaly detection

Using the `posthog-anomaly-detection` fundamental, monitor these signals:

**Content anomalies (check daily):**
- Blog views per tutorial drop >30% vs 4-week rolling average -> trigger: "content-reach-decline"
- GitHub clones drop to zero for 7 days (when baseline is 5+/week) -> trigger: "github-interest-drought"
- Social engagement rate drops >25% vs 4-week average -> trigger: "social-engagement-decline"

**Community anomalies (check daily):**
- Zero community posts in 7 days (when baseline is 3+/week) -> trigger: "community-activity-stall"
- Community-attributed website visits drop >40% -> trigger: "community-referral-decline"

**Lead anomalies (check daily):**
- Zero developer leads in 10 days (when baseline is 2+/week) -> trigger: "devrel-lead-drought"
- Lead-to-meeting conversion drops below 15% for 2 weeks -> trigger: "devrel-conversion-decline"

**Speaking anomalies (check weekly):**
- CFP acceptance rate drops below 15% for 3 consecutive submissions -> trigger: "cfp-quality-decline"
- Zero talks on calendar for next 60 days -> trigger: "speaking-pipeline-empty"

Each anomaly trigger feeds into the `autonomous-optimization` drill's Phase 2 (Diagnose).

### 3. Build cross-channel attribution

Track the complete journey from devrel activity to revenue:

Using `posthog-custom-events` and `posthog-funnels`, implement these attribution events:

1. `devrel_tutorial_published` — properties: title, pillar, url, github_repo_url, publish_date
2. `devrel_tutorial_engaged` — properties: url, views, avg_read_time, scroll_depth (collected 7 days after publish)
3. `devrel_github_activity` — properties: repo_name, stars_delta, clones_delta, forks_delta (from `github-traffic-api`, collected weekly)
4. `devrel_community_post` — properties: platform, thread_url, topic, engagement_score
5. `devrel_talk_delivered` — properties: conference_name, audience_size, talk_title, leads_captured
6. `devrel_lead_captured` — properties: source_type (content, community, speaking), source_detail, lead_title, lead_company
7. `devrel_meeting_booked` — properties: lead_name, source_type, days_from_first_touch
8. `devrel_deal_created` — properties: lead_name, deal_value, source_type, days_from_first_touch

Build a PostHog funnel from events 1-8 with breakdowns by source_type to answer: "Which devrel activity produces the most revenue — tutorials, community, or speaking?"

### 4. Automate weekly performance reports

Using `n8n-scheduling` and `n8n-workflow-basics`, build a weekly report workflow:

**Trigger:** Monday at 9am

**Data collection:**
1. Pull last 7 days of devrel events from PostHog API
2. Pull lead and meeting data from Attio using `attio-reporting`
3. Pull GitHub traffic data using `github-traffic-api` for all sample repos
4. Pull LinkedIn engagement via `linkedin-organic-analytics`

**Report generation:**
Use Claude API to generate a narrative report:

```
Prompt: "You are analyzing a developer advocacy program's performance for the past week.
Here is the data: {DATA}. Compare to 4-week rolling average: {BASELINE}.

Generate a report with:
1. Executive summary (3 sentences: content output, community health, lead generation)
2. Key metrics table (this week vs last week vs 4-week avg) for: tutorials published, GitHub clones, community posts, talks delivered, leads captured, meetings booked
3. Top performers: best tutorial by views, best GitHub repo by clones, best community post by engagement
4. Channel comparison: leads from content vs community vs speaking this week
5. Anomalies detected (if any) with recommended response
6. Recommended experiments for next week (1-2 specific tests)
Keep it under 600 words. Use specific numbers."
```

**Delivery:**
- Post to Slack channel
- Store in Attio as a note on the devrel campaign record
- If any anomaly was detected, prepend: "ANOMALY: {type} — action: {recommended_action}"

### 5. Build monthly deep-dive reports

Monthly report on the first Monday adds:

- Content pillar performance ranking: which topics attract the most developer interest
- Channel ROI comparison: content vs community vs speaking by leads, pipeline value, and time invested
- GitHub portfolio health: which repos are growing, which are stale
- Speaking program: acceptance rate trends, best-performing conference types
- Efficiency trends: leads per hour of advocate time vs previous months
- Experiment results from autonomous optimization loop

### 6. Set up alert routing

Build n8n alert workflows:

- **Immediate Slack alert**: Tutorial exceeds 3x average views (ride the wave — create social derivatives immediately)
- **Immediate Slack alert**: GitHub repo gets 10+ stars in 24 hours (trending — engage with stargazers)
- **Daily digest**: Leads captured and meetings booked from devrel sources
- **Weekly flag**: If no optimization experiments are running for 2+ weeks (stall alert)
- **Weekly flag**: If CFP pipeline has zero open submissions (refill the pipeline)

## Output

- Real-time PostHog dashboard with 6 panels covering content, reach, community, speaking, attribution, and efficiency
- Anomaly detection feeding into autonomous optimization loop
- Cross-channel devrel-to-pipeline attribution tracking
- Automated weekly and monthly performance reports
- Alert routing for opportunities and issues

## Triggers

Dashboard is always-on. Anomaly detection runs daily via n8n. Weekly reports fire every Monday at 9am. Monthly reports fire first Monday of each month. Alerts fire in real-time and via daily digests.

---
name: award-performance-monitor
description: Continuous monitoring of award submission pipeline, win rates, social proof impact, and award-attributed pipeline value
category: Awards
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic Claude API
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Award Performance Monitor

This drill builds the monitoring and reporting system for an industry award submissions program. It tracks the full pipeline from submission to announcement to social proof impact to pipeline influence, and generates reports that feed into the `autonomous-optimization` drill.

## Input

- PostHog with award events flowing
- Attio with award submission records and win tracking
- At least 2 quarters of award submission data (baseline for analysis)
- n8n instance for automated monitoring

## Steps

### 1. Build the Award Program Dashboard

Using the `posthog-dashboards` fundamental, create an "Award Submissions Program" dashboard:

**Panel 1 — Submission Pipeline:**
- Trend: submissions per quarter by award category
- Funnel: researched -> prepared -> submitted -> shortlisted -> finalist -> winner
- Win rate: percentage of submissions that result in wins or finalist placements
- Table: active submissions with award name, deadline, status

**Panel 2 — Win Tracking:**
- Number: total wins this year, finalists this year
- Breakdown: wins by award category (industry, growth, product, etc.)
- Table: all wins with award name, category, announcement date, and PR impact

**Panel 3 — Social Proof Distribution:**
- Trend: award badge impressions on website (tracked via PostHog pageviews on pages with badge)
- Number: social media posts featuring awards and their engagement
- Table: where award badges are displayed (homepage, pricing page, sales deck, email signature)

**Panel 4 — Award-to-Pipeline Attribution:**
- Number: deals where the prospect mentioned awards during the sales process
- Trend: award-influenced deals per quarter
- Table: specific deals influenced by award credibility (deal name, award referenced, deal value)

### 2. Implement the award event taxonomy

Using `posthog-custom-events`, define these events:

1. `award_researched` — properties: award_name, category, deadline, icp_overlap_score
2. `award_submitted` — properties: award_name, category, entry_fee, submission_date
3. `award_shortlisted` — properties: award_name, category, announcement_date
4. `award_won` — properties: award_name, category, announcement_date, estimated_audience
5. `award_not_selected` — properties: award_name, category, feedback_received
6. `award_badge_viewed` — properties: page_url, award_name (when a visitor views a page featuring an award badge)
7. `award_social_post` — properties: platform, award_name, engagement_count
8. `award_press_mention` — properties: outlet_name, award_name, url
9. `deal_award_influenced` — properties: deal_name, award_referenced, deal_value

### 3. Configure anomaly detection

Using `posthog-anomaly-detection`, monitor for:

**Submission anomalies (check monthly):**
- Submission volume drops >50% vs previous quarter -> trigger: "submission-drought"
- Win rate drops below 15% for 2 consecutive quarters -> trigger: "win-rate-decline"
- Zero new awards discovered in 30 days -> trigger: "pipeline-stale"

**Impact anomalies (check monthly):**
- Award-influenced deals drop >40% vs previous quarter -> trigger: "influence-decline"
- Award badge pageviews decline >30% -> trigger: "visibility-decline"

Each anomaly trigger feeds into the `autonomous-optimization` drill.

### 4. Track social proof distribution

Monitor where award wins are being leveraged:

1. Website: award badges on homepage, pricing, about page. Track via PostHog pageviews with badge properties.
2. Sales materials: track when sales team references awards in proposals (log in Attio deal notes)
3. Social media: count posts and engagement featuring award announcements
4. Email signatures: track click-through on award badge links in email signatures (UTM-tagged)
5. Press releases: track media pickups of award win announcements

### 5. Automate reports

Using `n8n-scheduling`, build a quarterly report workflow:

**Trigger:** First Monday of each quarter

**Report generation:**
Use Claude API to generate a narrative report:

```
Prompt: "Analyze the award submissions program for last quarter. Data: {DATA}. Generate:
1. Executive summary (2 sentences)
2. Submission stats: total submitted, win rate, finalist rate, by category
3. Wins this quarter: each win with award name, audience, and PR impact
4. Pipeline influence: award-influenced deals, total value
5. Social proof deployment: where awards are displayed, engagement data
6. ROI: total entry fees vs award-influenced pipeline value
7. Recommended adjustments: which categories to target more/less, submission quality improvements
Keep under 400 words."
```

**Delivery:** Post to Slack, store in Attio.

## Output

- PostHog dashboard with 4 panels covering submissions, wins, social proof, and attribution
- Full award event taxonomy
- Anomaly detection for submission and impact signals
- Quarterly automated performance reports

## Triggers

Dashboard is always-on. Anomaly detection runs monthly via n8n. Quarterly reports fire first Monday of each quarter.

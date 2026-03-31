---
name: guest-post-performance-monitor
description: Track backlink acquisition, referral traffic, domain authority impact, and conversion from published guest posts
category: GuestPosting
tools:
  - Ahrefs
  - PostHog
  - n8n
  - Attio
fundamentals:
  - ahrefs-backlink-analysis
  - ahrefs-rank-tracking
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - n8n-workflow-basics
  - n8n-scheduling
  - attio-reporting
---

# Guest Post Performance Monitor

This drill creates an always-on monitoring system that tracks every published guest post's impact: backlink health, referral traffic, SEO contribution, and downstream conversions. It detects when backlinks are removed, when referral traffic spikes or drops, and surfaces which blogs and topics deliver the highest ROI.

## Input

- List of published guest post URLs and their corresponding backlink target URLs (from `guest-post-article-pipeline` output stored in Attio)
- Ahrefs API access
- PostHog tracking installed on your site
- n8n instance connected to Ahrefs, PostHog, and Attio

## Steps

### 1. Set up guest-post-specific PostHog events

Using `posthog-custom-events`, ensure these events are firing:

- `guest_post_referral_visit`: Any pageview where the HTTP referrer matches a blog domain in your published guest post list. Properties: `source_blog`, `source_article_url`, `landing_page`, `utm_campaign`
- `guest_post_engagement`: Scroll depth >50% or time on page >30s from a guest post referral. Properties: same as above plus `scroll_depth`, `time_on_page`
- `guest_post_conversion`: Signup, demo request, or other conversion event from a guest post referral visitor. Properties: same as above plus `conversion_type`, `conversion_value`

### 2. Build the guest posting dashboard in PostHog

Using `posthog-dashboards`, create a dashboard with panels:

- **Total referral visits from guest posts** (line chart, last 30 days): Sum of `guest_post_referral_visit` events, broken down by `source_blog`
- **Top 10 guest posts by referral traffic** (table): Ranked by visit count, showing source blog, article URL, and total referral visits
- **Conversion rate by source blog** (bar chart): `guest_post_conversion / guest_post_referral_visit` per source blog
- **Backlinks active vs total** (number comparison): From Ahrefs data sync (see step 3)
- **Domain rating trend** (line chart): Your domain's DR over time, with guest post publication dates as annotations
- **Referral traffic trend** (line chart): Week-over-week referral visits from guest posts
- **Engagement quality** (table): Average scroll depth and time on page per source blog

### 3. Configure Ahrefs backlink monitoring via n8n

Using `n8n-workflow-basics` and `n8n-scheduling`, create a daily workflow:

1. **Pull new backlinks** using `ahrefs-backlink-analysis`:
   - Target: your domain
   - Date range: last 7 days
   - Filter: match `url_from` against your published guest post blog domains
   - Log new backlinks as PostHog events: `guest_post_backlink_acquired` with properties `source_blog`, `source_url`, `domain_rating_source`, `anchor_text`, `is_dofollow`

2. **Check for lost backlinks** using `ahrefs-backlink-analysis`:
   - Pull lost backlinks for the last 7 days
   - Match against your published guest post list
   - If a guest post backlink is lost: log `guest_post_backlink_lost` event, alert via Slack, update Attio record with loss reason

3. **Pull domain rating** using `ahrefs-backlink-analysis` (overview endpoint):
   - Daily DR snapshot
   - Log as PostHog event: `domain_rating_snapshot` with `current_dr`, `backlinks_total`, `referring_domains_total`

4. **Alert conditions**:
   - Backlink lost from a Tier 1 blog (DR 50+): immediate Slack alert
   - DR drops 2+ points in a week: Slack alert
   - No new backlinks acquired in 14 days: Slack alert (pipeline stalled)

### 4. Configure referral traffic alerts via n8n

Create a weekly n8n workflow:

1. Pull last 7 days of `guest_post_referral_visit` events from PostHog
2. Compare against prior 7 days and 4-week rolling average
3. Alert conditions:
   - Any guest post driving >100 referral visits/week: Slack notification with suggestion to repurpose the content
   - Total guest post referral traffic drops >25% week-over-week: Slack alert
   - A specific guest post's traffic drops to near zero (backlink may have been removed): cross-check with Ahrefs backlink data

### 5. Build the ROI tracking view

For each published guest post, maintain an ROI record in Attio:

| Field | Source | Calculation |
|-------|--------|-------------|
| Publication date | Manual entry | -- |
| Blog domain | Attio | -- |
| Blog DR at time of publication | Ahrefs | DR at publication date |
| Backlinks acquired | Ahrefs | Count of dofollow links from this post |
| Total referral visits | PostHog | Cumulative `guest_post_referral_visit` from this source |
| Conversions from referrals | PostHog | Cumulative `guest_post_conversion` from this source |
| Estimated SEO value | Ahrefs | DR of linking domain * dofollow factor (industry benchmark: one DA 50 dofollow link ≈ $500-2,000 SEO value) |
| Time invested | Manual | Hours spent on pitch + article writing + revisions |
| Cost per published article | Calculated | (time_invested * hourly_rate + tool_costs) / 1 |

### 6. Generate weekly and monthly reports

**Weekly report** (automated via n8n):
- New guest posts published this week
- New backlinks acquired (count and total DR)
- Referral traffic this week vs last week
- Conversions attributed to guest posts
- Pipeline status: pitches sent, replies received, articles in progress

**Monthly report** (automated via n8n):
- Total articles published this month
- Cumulative backlink portfolio: total referring domains from guest posts, average DR
- Domain rating change over the month
- Top 3 performing guest posts by referral traffic
- ROI: total investment vs estimated SEO value + conversions
- Recommendations: which blog tiers and topics to prioritize next month

## Output

- Live PostHog dashboard showing all guest posting metrics
- Daily backlink monitoring with lost-link alerts
- Weekly referral traffic analysis with anomaly detection
- Per-article ROI tracking in Attio
- Automated weekly and monthly performance reports

## Triggers

- Dashboard: always-on, updated in real-time
- Backlink monitoring: daily via n8n cron
- Referral traffic analysis: weekly via n8n cron
- Monthly report: monthly via n8n cron (first Monday of month)
- Alerts: immediate when thresholds are breached

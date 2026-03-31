---
name: github-repo-performance-monitor
description: Continuous monitoring dashboard and alert system for GitHub repo traffic, stars, clones, and conversion metrics
category: GitHub
tools:
  - PostHog
  - GitHub CLI
  - n8n
fundamentals:
  - github-traffic-api
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
---

# GitHub Repo Performance Monitor

Build a comprehensive monitoring system for a GitHub sample repo that tracks all engagement metrics, detects anomalies, and feeds data to the autonomous optimization loop. This is the play-specific monitoring drill for the Durable level.

## Input

- **GitHub repo** running at Scalable level with at least 2 months of traffic history in PostHog
- **PostHog** with `github_repo_views`, `github_repo_clones`, `github_repo_stars`, and `github_readme_cta_clicked` events
- **n8n** with existing GitHub traffic collection workflow

## Steps

### 1. Build the PostHog dashboard

Using `posthog-dashboards` fundamental, create a dashboard named "GitHub Sample Teaser - Performance" with these panels:

**Traffic panels:**
- Line chart: daily repo views (total and unique) over last 90 days
- Line chart: daily clones (total and unique) over last 90 days
- Counter: current total star count
- Line chart: stars gained per week over last 90 days

**Conversion panels:**
- Funnel: `github_repo_views` -> `github_readme_cta_clicked` -> `github_signup_completed` (or `github_demo_booked`)
- Line chart: weekly CTA click-through rate (clicks / views)
- Counter: total leads from GitHub (contacts with `first_touch_channel = github`)

**Referral panels:**
- Table: top referral sources by unique visitors (last 30 days)
- Bar chart: views by referrer over time

**Engagement panels:**
- Counter: issues opened this month
- Counter: PRs opened this month
- Counter: forks this month

### 2. Configure anomaly detection

Using `posthog-anomaly-detection` fundamental, set alerts for:

- **Views drop:** Weekly unique views drops >30% vs 4-week rolling average -> alert
- **Stars stall:** Zero new stars for 2 consecutive weeks -> alert
- **Clone spike:** Daily clones >3x the 2-week average -> alert (possible viral moment -- capitalize on it)
- **CTA rate drop:** Weekly CTA click-through rate drops >25% vs 4-week average -> alert
- **Referrer disappearance:** A top-3 referral source drops to zero -> alert (link might be broken)

### 3. Build the weekly digest workflow

Using `n8n-scheduling` and `n8n-triggers`:

Build an n8n workflow that runs every Monday at 9am:

1. Query PostHog for last 7 days of GitHub metrics:
   - Total and unique views
   - Total and unique clones
   - Stars gained
   - CTA clicks
   - New leads attributed to GitHub
   - Top referral sources
2. Compare each metric to the prior week and to the 4-week average
3. Classify each metric: **up** (>10% above average), **stable** (within 10%), **down** (>10% below average)
4. Format into a digest:

```
GitHub Sample Teaser — Weekly Digest (Week of <date>)

Views:  <count> (<trend> vs last week)
Clones: <count> (<trend>)
Stars:  +<new> (total: <total>) (<trend>)
CTA clicks: <count> (<trend>)
Leads: <count>

Top referrers: <list>
Anomalies: <any alerts triggered>
```

5. Post the digest to Slack and store in Attio

### 4. Feed anomalies to the optimization loop

When an anomaly alert fires:
1. Package the anomaly data (which metric, current value, expected value, deviation percentage)
2. Pull recent context (last 4 weeks of data, recent changes to the repo, recent releases)
3. Pass this bundle to the `autonomous-optimization` drill's Phase 2 (Diagnose)

This is the bridge between monitoring and optimization — the performance monitor detects THAT something changed, and the autonomous optimization drill figures out WHY and WHAT to do about it.

## Output

- PostHog dashboard with traffic, conversion, referral, and engagement panels
- Anomaly detection alerts configured for 5 key metrics
- Weekly digest workflow posting to Slack
- Anomaly -> optimization pipeline connected

## Triggers

Set up once at Durable level. Runs continuously: dashboard is always live, alerts fire on anomalies, digest runs weekly.

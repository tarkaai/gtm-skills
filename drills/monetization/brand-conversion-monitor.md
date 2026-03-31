---
name: brand-conversion-monitor
description: Continuously monitor website conversion metrics post-brand-refresh and detect performance changes across all entry points
category: Conversion
tools:
  - PostHog
  - n8n
  - Anthropic
fundamentals:
  - posthog-web-analytics
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-funnels
  - n8n-scheduling
  - hypothesis-generation
---

# Brand Conversion Monitor

Always-on monitoring workflow that tracks website conversion metrics after a brand refresh. Detects improvements and regressions across all entry points, pages, and traffic sources. Generates weekly brand health reports.

## Input

- PostHog project with brand refresh baseline snapshot
- Brand refresh launch date (for before/after comparisons)
- List of pages that were updated (and which are still pending)
- Target improvement metrics (e.g., 20% conversion lift, 15% bounce rate reduction)

## Steps

### 1. Build the brand health dashboard

Using `posthog-dashboards`, create a "Brand Refresh Health" dashboard:

**Row 1 — Overall metrics (before/after comparison):**
- Bounce rate trend (30-day with before/after marker)
- Session duration trend
- Conversion rate trend (primary CTA: signup/demo)
- Pages per session trend

**Row 2 — Page-level performance:**
- Table: Each updated page with before-refresh vs. after-refresh metrics
- Columns: page URL, visitors, bounce rate change, conversion rate change, avg scroll depth

**Row 3 — Source-level impact:**
- Conversion rate by traffic source (organic, paid, direct, referral, social)
- Shows whether the brand refresh helps all sources equally or disproportionately

**Row 4 — Funnel health:**
- Primary conversion funnel with step-by-step rates
- Compare funnel to pre-refresh baseline

### 2. Build the n8n monitoring workflow

Using `n8n-scheduling`, create a daily monitoring workflow:

**Trigger**: Cron, daily at 7:00 AM

**Step 1 — Pull daily metrics**: Query PostHog using `posthog-web-analytics`:
- Yesterday's visitors, bounce rate, conversion rate, session duration
- Same metrics for the same day-of-week from the pre-refresh period (apples-to-apples comparison)

**Step 2 — Detect anomalies**: Using `posthog-anomaly-detection`:
- Compare yesterday's metrics against 14-day post-refresh average
- Flag any metric deviating >15% from average
- Special attention to: bounce rate increases (brand confusion), conversion rate drops (CTA clarity issues), session duration drops (content relevance)

**Step 3 — Classify and route**:
- `improving`: Metrics trending better than baseline. Log.
- `stable`: Metrics holding at post-refresh levels. Log.
- `degrading`: Any key metric worse than pre-refresh baseline for 3+ consecutive days. Alert.

**Step 4 — Generate weekly brand health report** (every Monday):
Using `hypothesis-generation`:
```
Generate a weekly brand health report from this data:

Pre-refresh baseline: {metrics}
This week's metrics: {metrics}
Week-over-week trend: {metrics}
Page-level performance: {table}

Report should include:
1. Overall brand refresh impact assessment (positive/neutral/negative)
2. Top 3 improved pages with likely explanations
3. Top 3 underperforming pages with diagnostic hypotheses
4. Recommended next actions
5. Estimated time to reach target improvement ({target}%)
```

Post report to Slack and store in Attio.

### 3. Regression detection

If conversion rate drops below pre-refresh baseline for 5+ consecutive days:
1. Pull session recordings from `posthog-session-recording` for the regression period
2. Compare user behavior on affected pages
3. Generate specific diagnostic hypotheses
4. Alert the team with recommended fixes

## Output

- Daily monitoring with anomaly alerts
- Weekly brand health reports
- Before/after metrics comparison for every updated page
- Regression detection with diagnostic analysis
- Continuous tracking of progress toward target metrics

## Triggers

- Runs daily via n8n cron
- Weekly summary report generated every Monday
- Regression alerts fire in real-time when thresholds are breached

---
name: tooltip-performance-monitor
description: Track tooltip CTR, feature adoption lift, and dismissal patterns to identify which tooltips drive real usage
category: Enablement
tools:
  - PostHog
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-dashboards
  - posthog-cohorts
  - n8n-scheduling
  - n8n-triggers
---

# Tooltip Performance Monitor

This drill builds the measurement layer for feature discovery tooltips. It tracks every tooltip from impression through feature adoption, identifies which tooltips drive real sustained usage versus one-time clicks, and flags underperforming tooltips for removal or redesign.

## Input

- PostHog tracking tooltip events: `tooltip_shown`, `tooltip_cta_clicked`, `tooltip_dismissed`, `feature_used`
- At least 7 days of tooltip data
- n8n instance for scheduled reporting

## Steps

### 1. Define the tooltip conversion funnel

Using `posthog-funnels`, create a funnel for every active tooltip:

```
tooltip_shown (feature={feature_name})
  -> tooltip_cta_clicked (feature={feature_name})
    -> feature_used (feature={feature_name}, within 1 hour)
      -> feature_used (feature={feature_name}, 3+ times in 7 days)
```

The four stages are: Impression, Click, Trial, and Adoption. A tooltip that gets clicks but not adoption is misleading users -- the feature is not delivering on the tooltip's promise, or the tooltip is poorly targeted.

Break each funnel down by:
- User segment (new, established, power)
- Tooltip variant (if A/B testing copy)
- Page context (where the tooltip appeared)

### 2. Build the tooltip performance dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Tooltip CTR by feature | Bar chart | Which tooltips get clicked most |
| Tooltip-to-adoption rate | Bar chart | Which tooltips drive sustained feature usage |
| Dismissal rate by feature | Bar chart | Which tooltips annoy users |
| Adoption lift: tooltip vs no-tooltip | Comparison | Does the tooltip actually help vs organic discovery |
| Time from tooltip click to adoption | Histogram | How quickly do users adopt after seeing the tooltip |
| Tooltip fatigue trend | Line chart | Is overall tooltip CTR declining over time (fatigue signal) |
| Top underperforming tooltips | Table | High impression count, low adoption -- candidates for removal |

### 3. Calculate adoption lift

Using `posthog-cohorts`, create two cohorts for each feature:
- **Tooltip cohort**: Users who saw the tooltip for feature X
- **Control cohort**: Users who did NOT see the tooltip but are otherwise similar (same signup date range, same plan, same activity level)

Compare feature adoption rates between the two cohorts. The difference is the tooltip's causal lift. If a tooltip has <5% lift over organic discovery, it is not earning its screen space and should be removed or redesigned.

### 4. Detect tooltip fatigue

Using `posthog-custom-events`, track aggregate tooltip metrics over time:

- Overall tooltip CTR (across all tooltips, weekly trend)
- Per-user tooltip exposure count (average tooltips shown per user per week)
- Sequential dismissal rate (users who dismiss 2+ tooltips in a row)

If overall CTR declines for 3+ consecutive weeks, or sequential dismissal rate exceeds 40%, the system is showing too many tooltips. Reduce frequency, raise the priority threshold, or retire low-performing tooltips.

### 5. Build automated alerts

Using `n8n-scheduling`, create a weekly workflow that:

1. Queries PostHog for all active tooltip metrics
2. Flags tooltips where:
   - CTR < 10% after 500+ impressions (underperforming)
   - Dismissal rate > 60% (annoying)
   - Adoption lift < 5% vs control (not useful)
   - CTR dropped >30% week-over-week (fatigue)
3. Generates a weekly tooltip health report
4. Sends the report to the product team via Slack or email

### 6. Build the retirement pipeline

Using `n8n-triggers`, create a workflow that auto-retires tooltips when they hit retirement criteria:

- Active for 60+ days AND CTR below 10%
- Shown to 80%+ of eligible users (audience exhausted)
- Feature adoption rate for that feature has reached 70%+ (tooltip no longer needed)

On retirement: disable the Intercom message, log the final performance metrics, and add the feature to a "graduated" list so it is excluded from future tooltip targeting.

## Output

- Per-tooltip conversion funnel (impression -> click -> trial -> adoption)
- Tooltip performance dashboard with 7 panels
- Adoption lift measurement vs control cohort
- Tooltip fatigue detection with automated alerts
- Weekly tooltip health report
- Automated retirement pipeline for exhausted or underperforming tooltips

## Triggers

Dashboard refreshes continuously. The weekly health report runs every Monday via n8n cron. The retirement pipeline checks daily. Re-run setup when launching new tooltip campaigns or changing the tooltip delivery system.

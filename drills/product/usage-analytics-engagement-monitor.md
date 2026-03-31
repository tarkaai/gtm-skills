---
name: usage-analytics-engagement-monitor
description: Monitor how users interact with their personal analytics surface and measure its impact on retention
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-funnels
  - posthog-cohorts
  - posthog-dashboards
  - posthog-custom-events
  - n8n-scheduling
  - attio-notes
---

# Usage Analytics Engagement Monitor

This drill measures whether the personal usage analytics surface is actually driving retention. It tracks view rates, engagement depth, and the causal link between analytics usage and retention/expansion. Without this drill, you are guessing whether the analytics surface works.

## Input

- Analytics surface live in the product with PostHog events firing (from `usage-analytics-surface-build` drill)
- At least 14 days of analytics surface event data
- n8n instance for scheduled reporting
- Attio for logging play health

## Steps

### 1. Build the analytics engagement funnel

Using `posthog-funnels`, create a funnel tracking the user journey through the analytics surface:

```
usage_analytics_page_viewed
  -> usage_analytics_metric_clicked
    -> usage_analytics_cta_clicked
      -> [core product action taken within 24 hours]
```

Break down by:
- User tenure (new users <30 days vs. established users)
- Plan type (free vs. paid)
- Discovery method (Intercom prompt vs. navigation vs. email digest)

The key conversion to watch: "analytics viewed -> core product action within 24 hours." This measures whether looking at your stats actually motivates you to use the product more.

### 2. Create the retention comparison cohorts

Using `posthog-cohorts`, create two cohorts:

- **Analytics viewers**: Users who viewed the analytics surface 2+ times in the last 30 days
- **Non-viewers**: Users active in the last 30 days who have NOT viewed the analytics surface

Compare these cohorts on:
- 7-day retention rate (% who return within 7 days of any given session)
- 30-day retention rate
- Feature breadth (number of distinct features used)
- Session frequency (average sessions per week)

The difference between these cohorts is the "analytics lift" -- the retention improvement attributable to the analytics surface. Caveat: this is correlational, not causal. More engaged users are more likely to view analytics AND to retain. The A/B test at Scalable level establishes causality.

### 3. Build the engagement dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

| Panel | Visualization | What it answers |
|-------|--------------|-----------------|
| Analytics view rate | Trend line | What % of active users viewed their analytics this week? |
| View frequency distribution | Histogram | How many times per week do viewers check their stats? |
| Engagement depth | Funnel | What % of viewers click a metric? Click the CTA? |
| Discovery channel performance | Bar chart | Which prompt type drives the most views? |
| Retention lift | Comparison chart | Viewer vs. non-viewer retention at 7 and 30 days |
| CTA conversion by type | Table | Which CTA type (feature suggestion, resume work, milestone) converts best? |
| Time on surface | Trend line | Are users spending more or less time on the page over time? |

Set alerts:
- View rate drops below 40% of active users for 2 consecutive weeks
- Engagement depth (metric clicks) drops below 30% of viewers
- Retention lift narrows to <5 percentage points (the surface is losing its effect)

### 4. Build the weekly health report

Using `n8n-scheduling`, create a workflow that runs every Monday:

1. Query PostHog for the last 7 days of analytics surface metrics
2. Calculate: view rate, engagement depth, CTA conversion rate, retention lift
3. Compare to previous week and 4-week rolling average
4. Generate a health summary: HEALTHY (all metrics stable or improving), WARNING (one metric declining), CRITICAL (view rate or retention lift declining for 2+ weeks)
5. Log the health report in Attio using `attio-notes` on the play's campaign record
6. If WARNING or CRITICAL, include a diagnosis: which metric declined, possible causes, and recommended actions

### 5. Track milestone and insight effectiveness

Using `posthog-custom-events`, measure which types of insights and milestones drive the most engagement:

- Track which "top insight" messages users see and whether they click through
- Track which milestones are reached and whether the milestone prompt increases return visits
- Track which CTA types (feature suggestion, resume work, milestone chase) drive the most downstream product actions

Rank insight types by their "activation rate" (% of users who take a product action within 24 hours of seeing the insight). Double down on the highest-performing insight types and retire low performers.

### 6. Feed insights back into the surface

Based on the monitoring data, generate optimization recommendations:

- If view rate is low: the discovery prompts need work (test new copy, timing, or placement)
- If engagement depth is low: the metrics shown are not interesting enough (test different metrics or add benchmarks)
- If CTA conversion is low: the call-to-action is not compelling (test different CTA types or personalization)
- If retention lift is narrowing: the novelty is wearing off (add new data visualizations, comparisons, or gamification elements)

Document each recommendation in Attio with the supporting data. These become the hypotheses for A/B testing at Scalable level.

## Output

- Analytics engagement funnel in PostHog
- Viewer vs. non-viewer retention comparison cohorts
- 7-panel engagement dashboard with threshold alerts
- Weekly health report workflow in n8n
- Insight and milestone effectiveness tracking
- Optimization recommendations logged in Attio

## Triggers

The health report runs weekly via n8n cron. The dashboard and cohort comparisons update in real time via PostHog. Re-run the full drill setup when the analytics surface layout changes significantly.

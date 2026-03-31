---
name: pricing-page-conversion-monitor
description: Monitor pricing page visitor behavior, plan selection patterns, and self-serve conversion funnel health with anomaly detection
category: Product
tools:
  - PostHog
  - Stripe
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-cohorts
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-session-recording
  - billing-event-streaming
  - n8n-scheduling
  - attio-reporting
---

# Pricing Page Conversion Monitor

This drill builds an always-on monitoring system specifically for the pricing page and self-serve conversion funnel. It detects when conversion rates shift, when plan selection mix changes, when visitors exhibit comparison-shopping behavior, and when ARPU trends up or down. This is the observation layer that feeds the `autonomous-optimization` drill at Durable level for pricing page experiments.

## Prerequisites

- PostHog tracking installed on the pricing page with events from `posthog-gtm-events`
- Stripe billing event streaming configured via `billing-event-streaming`
- At least 60 days of pricing page traffic data in PostHog
- n8n instance for scheduled monitoring

## Steps

### 1. Build the pricing page conversion dashboard

Using `posthog-dashboards`, create a "Pricing Page Health" dashboard with these panels:

**Visitor Panels:**
- Pricing page unique visitors (daily, 30-day trend)
- Visitor source breakdown: direct product navigation vs. marketing landing vs. external referral
- Return visit rate: percentage of visitors who view the pricing page 2+ times before converting
- Time on page: median and P90 time spent on the pricing page
- Scroll depth: percentage of visitors reaching each plan card and the FAQ section

**Conversion Panels:**
- Pricing page to checkout conversion rate (daily, 7-day rolling average)
- Plan selection distribution: percentage choosing each plan tier
- Checkout abandonment rate: started checkout but did not complete payment
- Time from first pricing page view to completed checkout (median)
- Conversion rate by traffic source (organic, paid, direct, referral)

**Revenue Panels:**
- New self-serve ARPU (average revenue per new subscription, weekly)
- Plan mix revenue contribution: what percentage of new MRR comes from each plan
- Annual vs. monthly plan selection rate
- Coupon/discount usage rate and revenue impact

### 2. Build the pricing page funnel

Using `posthog-funnels`, create a multi-step funnel:

1. `pricing_page_viewed` — visitor lands on pricing page
2. `plan_card_clicked` — visitor clicks a specific plan card or CTA (property: `plan_name`)
3. `checkout_started` — visitor enters checkout flow
4. `payment_method_entered` — visitor submits payment info
5. `subscription_created` — Stripe confirms the subscription

Track conversion between each step. The biggest drop-off point is your optimization target.

Also create a secondary funnel for the comparison flow:
1. `pricing_page_viewed`
2. `pricing_faq_expanded` — visitor opens FAQ items (property: `faq_topic`)
3. `plan_comparison_toggled` — visitor switches between monthly/annual or expands feature comparison
4. `plan_card_clicked`

### 3. Set anomaly detection rules

Using `posthog-anomaly-detection`, configure alerts for:

| Metric | Alert Condition | Severity |
|--------|----------------|----------|
| Pricing page conversion rate | Drops >20% vs. 14-day average | High |
| Plan mix shift | Any plan's share changes >15pp in 7 days | Medium |
| Checkout abandonment rate | Exceeds 70% for 3 consecutive days | High |
| ARPU (new subscribers) | Drops >15% month-over-month | High |
| Annual plan selection rate | Drops below 20% | Medium |
| Pricing page bounce rate | Exceeds 60% for 7 consecutive days | Medium |
| Time-to-conversion | Increases >50% vs. 30-day average | Low |

### 4. Build the daily monitoring workflow

Using `n8n-scheduling`, create a workflow that runs daily at 08:00 UTC:

1. Query PostHog for all pricing page metrics (conversion rate, plan mix, abandonment, ARPU)
2. Compare each metric against its 14-day rolling average and the anomaly thresholds from Step 3
3. If any metric is anomalous:
   a. Log `pricing_page_anomaly_detected` event in PostHog using `posthog-custom-events` with properties: `metric_name`, `current_value`, `baseline_value`, `severity`, `affected_plan`
   b. Pull 3 recent session recordings from `posthog-session-recording` where the user visited the pricing page during the anomaly window — attach recording URLs to the alert
   c. Create an Attio note on the pricing project record with the anomaly details and session recording links
   d. If severity = High, send a Slack alert to the pricing owner
4. If all metrics are normal, log `pricing_page_health_check_passed` event

### 5. Build the weekly pricing page digest

Using `n8n-scheduling`, create a weekly workflow (Monday 09:00 UTC):

1. Aggregate the full week's pricing page data
2. Compute week-over-week changes for all metrics
3. Identify the top 3 trends (positive or negative)
4. Generate a structured report:
   ```
   Pricing Page Digest — Week of {date}

   Conversion rate: {current}% ({change}% WoW)
   ARPU (new): ${current} ({change}% WoW)
   Plan mix:
     - Free: {rate}% ({change}pp)
     - Starter: {rate}% ({change}pp)
     - Pro: {rate}% ({change}pp)
   Annual selection: {rate}% ({change}pp)
   Checkout abandonment: {rate}% ({change}pp)

   Top trends:
   1. {trend description}
   2. {trend description}
   3. {trend description}

   Action items:
   - {item if anomaly detected}
   ```
5. Post to Slack and store in Attio

### 6. Track pricing sensitivity cohorts

Using `posthog-cohorts`, maintain dynamic cohorts:

- **Comparison shoppers:** Visitors who viewed the pricing page 3+ times in 7 days without converting. They are evaluating alternatives.
- **Plan hesitators:** Visitors who clicked a plan CTA but abandoned checkout. They want to buy but something stopped them.
- **Downgrade researchers:** Active paying customers who visited the pricing page 2+ times in 7 days. They may be considering a downgrade.
- **Annual-curious:** Visitors who toggled to annual pricing view but selected monthly. They are interested in annual but the discount was not compelling enough.

Update these cohorts daily. Feed them into the `autonomous-optimization` drill as experiment targeting segments.

### 7. Calibrate monthly

At the end of each month:

1. Compare predicted anomalies vs. actual outcomes (did alerts lead to real issues?)
2. Adjust thresholds: if false positives exceed 30%, tighten them. If misses exceed 20%, loosen them.
3. Review session recordings for the top 3 drop-off points in the pricing funnel
4. Check if traffic sources have shifted enough to warrant source-specific conversion analysis
5. Log calibration results as a PostHog event: `pricing_page_monitor_calibration` with `precision`, `recall`, `threshold_changes`

## Output

- A PostHog dashboard with real-time pricing page conversion visibility
- Multi-step pricing funnel with per-step conversion tracking
- Daily anomaly detection with severity-based alerting and session recording context
- Weekly pricing page digest posted to Slack
- Dynamic cohorts tracking pricing page behavior patterns
- Monthly calibration loop for monitoring accuracy

## Triggers

Daily monitoring runs via n8n cron. Weekly digest on Mondays. Monthly calibration on the 1st. On-demand via webhook after pricing page changes.

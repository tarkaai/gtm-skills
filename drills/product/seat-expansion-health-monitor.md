---
name: seat-expansion-health-monitor
description: Monitor seat expansion funnel health, report on prompt performance, and alert on conversion anomalies
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - posthog-funnels
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-reporting
---

# Seat Expansion Health Monitor

This drill builds the monitoring and reporting layer for the seat expansion play. It tracks the full funnel from signal detection through seat addition, identifies where conversion is breaking down, and generates weekly reports on expansion performance.

## Input

- PostHog events flowing from `seat-growth-signal-detection` and `seat-expansion-prompt-delivery`
- At least 2 weeks of expansion prompt data
- n8n instance for scheduled monitoring
- Attio CRM with expansion deals and account data

## Steps

### 1. Build the seat expansion dashboard

Using the `posthog-dashboards` fundamental, create a dashboard called "Seat Expansion Health" with these panels:

**Panel 1: Expansion Funnel (Funnel insight)**
Using `posthog-funnels`, build the core conversion funnel:
1. `seat_expansion_signal_detected` (accounts with expansion signals)
2. `seat_expansion_prompt_shown` (accounts that received a prompt)
3. `seat_expansion_prompt_clicked` (accounts that engaged with the prompt)
4. `seats_added` (accounts that actually added seats)

Break down by: `expansion_tier` (hot/warm), `channel` (in_app/email/sales), `prompt_type` (team_invite_failed, seat_limit_hit, etc.)

**Panel 2: Expansion Rate Trend (Trend insight)**
Track `seats_added` events over time, broken down by week. Overlay with `seat_expansion_prompt_shown` to show conversion rate trend. Add a goal line at the play's current threshold (35% for Smoke, 45% for Baseline, 40% at 500+ for Scalable).

**Panel 3: Prompt Performance by Type (Table insight)**
Show each prompt type with: impressions, clicks, conversions, CTR, conversion rate, average seats added, revenue impact. Sort by conversion rate descending.

**Panel 4: Time to Expansion (Distribution insight)**
Measure days from first expansion signal detected to seats added. Histogram showing the distribution. Healthy: most conversions happen within 0-3 days of the prompt. If median exceeds 7 days, the prompts are not creating enough urgency.

**Panel 5: Seat Utilization Distribution (Bar chart)**
Show account distribution by seat utilization percentage: 0-25%, 25-50%, 50-75%, 75-90%, 90-100%, 100% (at limit). The 75%+ buckets are the expansion opportunity pool.

**Panel 6: Expansion Revenue (Trend insight)**
Calculate additional MRR from seat additions: `sum(seats_added * per_seat_price)` by week. Cumulative total for the play's duration.

### 2. Configure anomaly alerts

Using `posthog-anomaly-detection`, set up alerts for:

- **Conversion drop:** If prompt-to-expansion conversion rate drops below 50% of 4-week rolling average for 3 consecutive days → alert
- **Signal volume spike:** If expansion signals increase by 100%+ in a week → alert (could indicate a product change or pricing issue driving more seat limit hits)
- **Prompt fatigue:** If prompt dismissal rate exceeds 80% for any prompt type over 7 days → alert (prompt copy or timing needs revision)
- **Channel degradation:** If any channel's conversion rate drops below 5% for 14 days → alert (channel may be saturated or broken)

Route alerts to the team Slack channel and log them in Attio.

### 3. Build the weekly health report

Using `n8n-scheduling`, create a workflow that runs every Monday at 09:00 UTC:

1. Pull the last 7 days of expansion data from PostHog
2. Calculate key metrics:
   - Total expansion signals detected
   - Total prompts delivered (by channel)
   - Overall conversion rate (prompt → seats added)
   - Best performing prompt type (by conversion rate)
   - Worst performing prompt type (by conversion rate)
   - Total seats added
   - Estimated additional MRR from seat additions
   - Comparison to prior week (% change for each metric)
3. Generate a structured report:

```
## Seat Expansion Weekly Report — Week of {{date}}

### Key Metrics
- Signals detected: {{signals}} ({{signalsDelta}} vs last week)
- Prompts delivered: {{prompts}} (in-app: {{inApp}}, email: {{email}}, sales: {{sales}})
- Seats added: {{seatsAdded}} ({{seatsDelta}} vs last week)
- Conversion rate: {{conversionRate}}% ({{conversionDelta}} vs last week)
- Additional MRR: ${{additionalMRR}}

### Top Performing
- Best prompt: {{bestPromptType}} at {{bestConversionRate}}% conversion
- Best channel: {{bestChannel}} at {{bestChannelRate}}% conversion

### Needs Attention
- {{worstPromptType}} converting at only {{worstRate}}% — below 10% threshold
- {{alertCount}} anomaly alerts triggered this week

### Recommendation
{{agentRecommendation}}
```

4. Post to Slack and store in Attio as a note on the "Seat Expansion" campaign record

### 4. Track report accuracy

Using `posthog-custom-events`, log each report generation:

```javascript
posthog.capture('expansion_health_report_generated', {
  week_of: reportDate,
  signals_detected: signalCount,
  prompts_delivered: promptCount,
  seats_added: seatsAdded,
  conversion_rate: conversionRate,
  additional_mrr: additionalMRR,
  alerts_triggered: alertCount
});
```

Over time, use this data to spot trends: is expansion accelerating, plateauing, or declining? Feed these trends into the `autonomous-optimization` drill at Durable level.

## Output

- PostHog dashboard "Seat Expansion Health" with 6 panels covering the full expansion funnel
- Anomaly alerts for conversion drops, signal spikes, prompt fatigue, and channel degradation
- Weekly automated health report posted to Slack and stored in Attio
- Report generation tracking for long-term trend analysis

## Triggers

Dashboard is always-on. Anomaly alerts run continuously via PostHog actions. Weekly report runs every Monday at 09:00 UTC via n8n cron.

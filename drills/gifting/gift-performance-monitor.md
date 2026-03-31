---
name: gift-performance-monitor
description: Continuously monitor gift campaign performance, detect anomalies, and generate weekly reports with ROI analysis
category: Gifting
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-anomaly-detection
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Gift Performance Monitor

An always-on monitoring workflow that tracks gift campaign KPIs, detects anomalies, and generates weekly performance reports. This drill is the eyes and ears of the gift campaign at Durable level — it feeds anomaly data into the `autonomous-optimization` drill.

## Input

- PostHog project with the gift event taxonomy configured (`gift-tracking-attribution` fundamental)
- Attio with gift campaign data (send records, response logs)
- n8n instance for scheduling

## Monitored Metrics

### Primary KPIs
- **Response rate** — (responses within 30 days / gifts delivered) — target varies by level
- **Cost per meeting** — (total gift spend / meetings booked) — target: ≤$75
- **Pipeline per dollar** — (pipeline value generated / total gift spend) — target: ≥5x

### Secondary KPIs
- **Delivery success rate** — (delivered / sent) — target: ≥90% for physical, ≥98% for digital
- **Response time** — median days from delivery to first response
- **Gift redemption rate** — (eGifts redeemed / eGifts delivered) — for digital gifts only
- **Follow-up conversion lift** — response rate with follow-up vs. gift-only

### Segmented Metrics
- Response rate by gift type (book, eGift, swag, gourmet)
- Response rate by signal type (job change, funding, hiring, competitor)
- Response rate by prospect seniority (C-level, VP, Director, Manager)
- Cost per meeting by gift value tier ($25, $50, $75, $100)

## The Monitoring Loop

### Daily Check (n8n cron, 8am)

Build an n8n workflow triggered at 8am daily:

1. Query PostHog for the last 24 hours of gift events:
   - `gift_sent` count
   - `gift_delivered` count
   - `gift_failed` count (alert if >10% of sends)
   - `gift_response` count
   - `gift_meeting_booked` count

2. Compare trailing 7-day response rate against 28-day rolling average:
   - **Normal:** within ±10% — log and continue
   - **Plateau:** within ±2% for 3+ weeks — flag for optimization
   - **Drop:** >20% decline — trigger alert
   - **Spike:** >50% increase — investigate (is this real or an attribution error?)

3. Check for delivery failures:
   - If >3 failures in 24 hours, alert with failure reasons
   - Common: bad addresses (enrich again), platform outage (check status page), international delivery issues

4. If anomaly detected, push the anomaly data to the `autonomous-optimization` drill.

### Weekly Report (n8n cron, Monday 9am)

Generate a weekly gift campaign performance report:

```
GIFT CAMPAIGN WEEKLY REPORT — Week of {{date}}

SENDS & DELIVERY
- Gifts sent this week: {{count}}
- Delivery rate: {{rate}}%
- Failed deliveries: {{count}} (reasons: {{breakdown}})

RESPONSES
- Response rate (30-day attributed): {{rate}}%
- Responses this week: {{count}}
  - Email replies: {{count}}
  - Meetings booked: {{count}}
  - URL visits: {{count}}
  - LinkedIn replies: {{count}}
- Median response time: {{days}} days

UNIT ECONOMICS
- Total spend this week: ${{amount}}
- Cost per response: ${{amount}}
- Cost per meeting: ${{amount}}
- Pipeline generated: ${{amount}}
- ROI (pipeline / spend): {{ratio}}x

SEGMENTS
- Best performing gift type: {{type}} ({{rate}}% response)
- Best performing signal: {{signal}} ({{rate}}% response)
- Best performing seniority: {{level}} ({{rate}}% response)

EXPERIMENTS
- Active: {{experiment_description}} ({{sample_size}} / {{target_size}})
- Last completed: {{experiment_result}}

TREND
- Response rate vs. last week: {{delta}}%
- Response rate vs. 4-week avg: {{delta}}%
- Convergence status: {{status}}

RECOMMENDATION
{{ai_generated_recommendation}}
```

Post to Slack and store in Attio as a campaign note.

## Alert Thresholds

| Condition | Severity | Action |
|-----------|----------|--------|
| Response rate drops >20% vs. 4-week average | High | Trigger autonomous-optimization diagnosis |
| >10% delivery failures in a batch | High | Pause sending, investigate addresses |
| Cost per meeting exceeds $150 | Medium | Review gift value and targeting |
| No responses in 2 weeks from any send batch | High | Full campaign audit |
| Gift platform API errors >5% of requests | Medium | Check platform status, switch to backup |

## Output

- Daily anomaly detection with alerts when metrics deviate
- Weekly performance report posted to Slack and stored in Attio
- Anomaly data pushed to the autonomous-optimization drill for hypothesis generation
- Segmented performance data for informing A/B test design

## Triggers

- Daily monitoring runs automatically via n8n cron
- Weekly report runs automatically via n8n cron
- Anomaly alerts fire in real-time when thresholds are breached

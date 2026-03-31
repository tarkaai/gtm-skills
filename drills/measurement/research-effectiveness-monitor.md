---
name: research-effectiveness-monitor
description: Monitor which account research signals and personalization hooks actually drive replies and meetings
category: Measurement
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-dashboards
  - posthog-cohorts
  - posthog-anomaly-detection
  - attio-reporting
---

# Research Effectiveness Monitor

This drill builds the monitoring layer that tracks which account research signals and personalization hooks actually convert into replies and meetings. It answers: "Is our research making outreach better, and which types of research matter most?" This is the play-specific monitoring that feeds the `autonomous-optimization` drill at Durable level.

## Input

- PostHog instance with account research events flowing (from `posthog-gtm-events` drill)
- Attio CRM with deal records linked to outreach activity
- At least 4 weeks of data from Baseline or Scalable level operation
- n8n instance for automated reporting

## Steps

### 1. Define the event taxonomy

Ensure these PostHog events are being captured (set up via `posthog-gtm-events` if not):

| Event | Properties | When Fired |
|-------|-----------|------------|
| `account_researched` | `company_domain`, `research_depth` (manual/automated), `signal_count`, `hook_count`, `research_time_minutes` | After research completes |
| `outreach_sent` | `company_domain`, `channel` (email/linkedin), `hook_type` (funding/hire/tech/news/none), `research_depth`, `personalized` (true/false) | After outreach message sent |
| `outreach_replied` | `company_domain`, `channel`, `hook_type`, `sentiment` (positive/neutral/negative), `research_depth` | After reply received |
| `meeting_booked` | `company_domain`, `hook_type`, `research_depth`, `days_from_first_touch` | After meeting scheduled |
| `deal_created` | `company_domain`, `research_depth`, `deal_value` | After deal enters pipeline |

### 2. Build the research effectiveness dashboard

Using the `posthog-dashboards` fundamental, create a dashboard with these panels:

**Panel 1 — Reply Rate by Research Depth:**
Compare reply rates across cohorts: no research, manual research (Smoke), automated research (Baseline+). Line chart, 4-week rolling window.

**Panel 2 — Reply Rate by Hook Type:**
Bar chart showing reply rate for each personalization hook type: funding, executive hire, tech stack, product launch, hiring signal, no hook. Identify which signals drive the highest engagement.

**Panel 3 — Meeting Conversion by Research Quality:**
Funnel: outreach_sent > outreach_replied > meeting_booked. Split by `research_depth`. Show conversion rate at each stage.

**Panel 4 — Signal-to-Meeting Correlation:**
Table showing, for each signal type, the number of times it was used and the meeting booking rate. Sort descending by meeting rate.

**Panel 5 — Research ROI:**
Calculate: (meetings_from_researched_outreach * avg_deal_value * win_rate) / (research_time_hours * hourly_cost + tool_costs). Display as a single number with trend line.

**Panel 6 — Research Freshness:**
Distribution of `account_brief_date` age for accounts with active outreach. Alert if >30% of active outreach is hitting accounts with briefs older than 30 days.

### 3. Set up anomaly alerts

Using `posthog-anomaly-detection`, configure alerts for:

- **Reply rate drop**: If researched outreach reply rate drops below 25% (vs baseline of 35%), fire alert
- **Hook effectiveness decay**: If a previously high-performing hook type drops below the overall average for 2 consecutive weeks, fire alert
- **Research-to-outreach gap**: If accounts are being researched but not receiving outreach within 7 days, fire alert (research is wasting)
- **Enrichment failure spike**: If >20% of account enrichment runs return incomplete data, fire alert

### 4. Build the weekly report workflow

Create an n8n workflow on a weekly cron schedule:

1. Query PostHog for the last 7 days of events
2. Calculate:
   - Total accounts researched this week
   - Reply rate by research depth (researched vs non-researched)
   - Top performing hook type this week
   - Worst performing hook type this week
   - Research time invested vs meetings generated
   - Week-over-week trend for reply rate and meeting rate
3. Generate a weekly report:

```
## Account Research Effectiveness — Week of {date}

### Performance
- Accounts researched: {n}
- Researched reply rate: {x}% (target: 35%) {UP/DOWN vs last week}
- Non-researched reply rate: {y}% (comparison baseline)
- Meetings from researched outreach: {n}

### Signal Effectiveness
- Best performing hook: {type} ({reply_rate}% reply rate)
- Worst performing hook: {type} ({reply_rate}% reply rate)
- Recommendation: {increase/decrease} emphasis on {signal_type}

### Research ROI
- Time invested: {hours}
- Tool cost: ${amount}
- Pipeline generated: ${amount}
- ROI: {x}:1

### Alerts
- {Any anomalies detected this week}

### Recommended Actions
- {Data-driven recommendations based on this week's metrics}
```

4. Post to Slack and store in Attio

### 5. Build signal decay tracking

Over time, certain signals lose predictive power (e.g., "funding" hooks become less effective during a bear market). Track each signal type's effectiveness on a 12-week rolling basis. If a signal type's reply rate declines for 4 consecutive weeks, flag it as "decaying" and recommend the `autonomous-optimization` drill test alternatives.

## Output

- Real-time dashboard showing research effectiveness metrics
- Anomaly alerts when research quality or effectiveness drops
- Weekly effectiveness report with signal-level insights
- Signal decay detection for long-term optimization
- Data feed ready for the `autonomous-optimization` drill at Durable level

## Triggers

- Dashboard is always-on, refreshes hourly
- Alerts fire in real-time when thresholds are breached
- Weekly report runs every Monday at 8am
- Signal decay analysis runs monthly

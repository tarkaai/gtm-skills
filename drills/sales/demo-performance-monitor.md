---
name: demo-performance-monitor
description: Continuously monitor discovery-to-demo-to-deal conversion funnel and detect degradation patterns
category: Sales
tools:
  - PostHog
  - n8n
  - Attio
  - Fireflies
fundamentals:
  - posthog-funnels
  - posthog-anomaly-detection
  - posthog-custom-events
  - posthog-dashboards
  - n8n-scheduling
  - n8n-triggers
  - attio-deals
  - attio-reporting
---

# Demo Performance Monitor

This drill creates an always-on monitoring system for the discovery-based demo pipeline. It tracks the full funnel from discovery call through demo to deal outcome, detects when conversion rates degrade, and surfaces which demo structures and pain-to-feature mappings produce the best outcomes.

## Input

- PostHog events flowing from the `demo-prep-automation` drill (`demo_prep_generated`, `demo_completed`)
- Attio deal records with BANT scores and demo outcomes
- Fireflies transcripts for demo calls
- At least 2 weeks of baseline demo data (minimum 10 demos)

## Steps

### 1. Define the demo conversion funnel

Using `posthog-custom-events`, ensure these events are captured:

| Event | Trigger | Key Properties |
|-------|---------|----------------|
| `discovery_call_completed` | Discovery call transcript processed | `deal_id`, `bant_composite`, `pains_identified` |
| `demo_prep_generated` | Demo prep doc created | `deal_id`, `pains_mapped`, `features_shown` |
| `demo_scheduled` | Cal.com booking confirmed | `deal_id`, `days_since_discovery`, `attendee_count` |
| `demo_completed` | Demo call ended and logged | `deal_id`, `outcome`, `pains_addressed`, `questions_asked`, `duration_minutes` |
| `recap_video_sent` | Loom recap shared | `deal_id`, `video_length_seconds` |
| `recap_video_viewed` | Prospect watched recap | `deal_id`, `watch_percentage`, `cta_clicked` |
| `next_step_committed` | Prospect agreed to next meeting | `deal_id`, `next_step_type` |
| `proposal_requested` | Prospect requested pricing/proposal | `deal_id`, `deal_value` |
| `deal_closed_won` | Deal closed | `deal_id`, `deal_value`, `days_in_pipeline` |

### 2. Build the funnel in PostHog

Using `posthog-funnels`, create a saved funnel:

`discovery_call_completed` -> `demo_scheduled` -> `demo_completed` -> `next_step_committed` -> `proposal_requested` -> `deal_closed_won`

Break down by:
- `bant_composite` buckets (0-40, 40-70, 70-100) -- which BANT scores predict demo success
- `pains_addressed` count -- does covering more pains increase conversion
- `outcome` -- which demo outcomes lead to closed deals
- `days_since_discovery` -- does demo timing affect conversion

Save as: "Discovery-Based Demo — Full Funnel"

### 3. Build the demo effectiveness dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

1. **Funnel conversion rates**: discovery -> demo -> next step -> proposal -> closed won
2. **Demo-to-nextstep trend**: weekly line chart of conversion rate
3. **Pain coverage vs outcome**: scatter plot of pains_addressed vs next_step_committed rate
4. **BANT score vs demo success**: bar chart showing conversion by BANT bucket
5. **Recap video engagement**: average watch percentage and correlation with next step
6. **Time-to-demo**: histogram of days between discovery and demo, overlaid with conversion rate
7. **Demo duration vs outcome**: are longer demos better or worse
8. **Weekly demo volume**: count of demos completed per week

### 4. Build n8n monitoring workflows

Using `n8n-scheduling`, create a daily cron workflow:

1. Query PostHog for the last 7 days of funnel data
2. Compute key conversion rates:
   - Discovery-to-demo rate
   - Demo-to-nextstep rate
   - Demo-to-proposal rate
   - Overall discovery-to-closed-won rate
3. Compare to baseline using `posthog-anomaly-detection` logic:
   - **Normal**: within +/- 15% of 4-week rolling average
   - **Warning**: 15-30% below average for 3+ consecutive days
   - **Critical**: >30% below average for 2+ consecutive days
4. For Warning/Critical: send Slack alert with degradation details and probable cause

Using `n8n-triggers`, create event-triggered workflows:
- On `demo_completed` where outcome = "no_interest": flag for demo quality review
- On `recap_video_viewed` where watch_percentage > 80% and no `next_step_committed` within 48 hours: trigger follow-up reminder

### 5. Build the pain-to-feature effectiveness report

Create a weekly n8n workflow that:

1. Pulls all `demo_completed` events from the last 30 days
2. Groups by features shown and pains addressed
3. Calculates conversion rate for each pain-to-feature combination
4. Identifies:
   - Top 3 pain-feature combos that predict closed deals (prioritize showing these)
   - Bottom 3 pain-feature combos that never convert (stop leading with these)
   - Features shown but never connected to a pain (remove from demos)
5. Generates a ranking report and stores it in Attio as a campaign note

### 6. Track demo quality signals from transcripts

After each demo, use Fireflies transcript + Claude to extract quality signals:

- Did the rep connect features back to specific pains mentioned in discovery ("You said X, this solves X")
- How many questions did the prospect ask (engagement signal)
- Did the prospect verbally commit to a next step
- Were there objections, and how were they handled

Score each demo 1-5 on: pain coverage, feature relevance, engagement, and close attempt. Correlate demo quality scores with deal outcomes over time.

## Output

- Real-time demo conversion funnel with breakdown by BANT score, pain coverage, and timing
- Daily automated monitoring with anomaly alerts
- Weekly pain-to-feature effectiveness ranking
- Demo quality scoring from transcript analysis
- Historical trend tracking for demo-to-deal conversion

## Triggers

- Daily monitoring: runs every day at 9 AM via n8n cron
- Weekly effectiveness report: runs every Monday at 8 AM via n8n cron
- Event-triggered: fires on every `demo_completed` event for quality scoring

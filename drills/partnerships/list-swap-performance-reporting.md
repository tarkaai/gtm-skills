---
name: list-swap-performance-reporting
description: Monitor per-partner swap ROI, surface optimization levers, and generate weekly list swap performance briefs
category: Partnerships
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-cohorts
  - attio-reporting
  - n8n-scheduling
  - hypothesis-generation
---

# List Swap Performance Reporting

This drill builds the monitoring and reporting layer specific to the list swap play. It tracks per-partner swap performance, surfaces which partners and email variants drive the most meetings, and generates weekly briefs that feed the `autonomous-optimization` drill at Durable level.

## Input

- Active swap partners with PostHog tracking in place (UTM parameters firing)
- Attio partner records with swap history
- At least 4 weeks of swap data (minimum for meaningful trends)

## Steps

### 1. Build the list swap dashboard in PostHog

Using the `posthog-dashboards` fundamental, create a dashboard called "List Swaps — Partner Performance" with these panels:

- **Clicks by partner** (bar chart): `pageview` events grouped by `utm_source` where `utm_medium = list-swap`, last 30 days
- **Meetings by partner** (bar chart): `list_swap_meeting_booked` events grouped by `utm_source`, last 30 days
- **Click-to-meeting conversion by partner** (table): meetings / clicks per partner, sorted descending
- **Clicks over time** (trend line): weekly `pageview` events with `utm_campaign = list-swaps-adjacent-startups`, last 90 days
- **Email variant performance** (table): clicks and meetings grouped by `utm_content`, comparing curiosity vs data vs story variants
- **Swap funnel**: `pageview` (swap traffic) → `list_swap_click` (CTA action) → `list_swap_meeting_booked`, filtered to list-swap traffic
- **Reciprocal performance** (table): how your list responded to each partner's email — opens, clicks, unsubscribes per inbound swap

### 2. Create swap performance cohorts

Using the `posthog-cohorts` fundamental, create cohorts for:

- **High-value partners**: Partners whose swap-sourced leads converted to meetings at >5% click-to-meeting rate
- **Volume partners**: Partners driving >50 clicks per swap but low meeting conversion
- **Declining partners**: Partners whose clicks dropped >30% swap-over-swap
- **New partners**: Partners with first swap in the last 30 days (need 2+ swaps before judging)
- **Reciprocity imbalanced**: Partners where net swap value (your clicks minus their clicks) is >3x in either direction

### 3. Build the weekly swap brief

Using the `n8n-scheduling` fundamental, create a weekly workflow (Friday 3pm):

1. Pull last 7 days of swap data from PostHog (clicks, meetings, conversion rates per partner)
2. Pull swap pipeline data from Attio (new partners onboarded, swaps completed, swaps scheduled)
3. Compare this week's metrics to the 4-week rolling average
4. Use the `hypothesis-generation` fundamental to generate insights:
   - Which partners over/underperformed and why?
   - Which email variants drove the most meetings (not just clicks)?
   - Are reciprocal obligations balanced?
   - Are any partners showing audience fatigue?
5. Compile into a structured brief and post to Slack

Brief format:
```
## List Swap Weekly Brief — {date}

**This week**: {total_clicks} clicks, {total_meetings} meetings ({cvr}% click-to-meeting)
**vs 4-week avg**: {change_pct}% {up/down}
**Swaps completed this week**: {count} (scheduled: {scheduled_count})

### Top partners by meetings
1. {partner_1}: {clicks} clicks, {meetings} meetings
2. {partner_2}: {clicks} clicks, {meetings} meetings

### Anomalies detected
- {partner/metric}: {description} — {hypothesis}

### Reciprocity check
- Partners we owe: {list of partners where we received more value}
- Partners that owe us: {list where we gave more value}

### Email variant insights
- Best subject line: "{subject}" ({open_rate}% open rate)
- Best variant: {variant} ({ctr}% CTR)

### Swap pipeline
- Active partners: {count}
- Swaps scheduled next 2 weeks: {count}
- Partners needing email copy: {count}

### Recommended actions
1. {action_1}
2. {action_2}
```

### 4. Build per-partner ROI tracker

In Attio, maintain these fields on each partner record (updated weekly by n8n):

- **Total swaps completed**: Count of completed email swaps
- **Total clicks received**: Cumulative clicks from this partner's list to your landing page
- **Total meetings generated**: Cumulative meetings from swap-sourced leads
- **Click-to-meeting rate**: Meetings / clicks as a percentage
- **Total clicks given**: How many clicks your list generated for this partner
- **Net swap value**: Clicks received minus clicks given
- **Best email variant**: The variant ID that performed best with this partner
- **Audience fatigue index**: Click trend over last 4 swaps (increasing, stable, declining)
- **Last swap date**: When the most recent swap occurred
- **Next swap date**: Scheduled upcoming swap
- **Partner reliability score**: % of scheduled swaps completed on time
- **Swap cadence tier**: Monthly, bimonthly, or quarterly

### 5. Set up performance alerts

Using PostHog and n8n, create alerts for:

- Any partner swap generates <5 clicks → flag: "Low engagement swap with {partner} — investigate audience fit"
- A swap generates >3 meetings → flag: "High-value swap with {partner} — fast-track to monthly cadence"
- Your list's unsubscribe rate exceeds 0.5% on an inbound swap → flag: "Quality issue with {partner}'s email — review before next swap"
- Total swap meetings drop below Scalable baseline for 2 consecutive weeks → trigger `autonomous-optimization` investigation
- An email variant achieves >8% CTR → flag as "proven template" for reuse
- A partner misses their scheduled swap send → alert: "Follow up with {partner} — missed swap commitment"

## Output

- PostHog dashboard with per-partner and per-variant swap performance
- Weekly automated list swap brief with insights and recommendations
- Per-partner ROI tracking in Attio with fatigue detection
- Alert system for performance anomalies and reliability issues
- Data feed for the `autonomous-optimization` drill at Durable level

## Triggers

Build the dashboard and alerts once at the start of Durable level. The weekly brief runs every Friday. Partner ROI fields update weekly via n8n.

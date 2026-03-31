---
name: hallway-demo-performance-monitor
description: Track and report on hallway demo ROI across events, identifying which events, venues, and approaches produce the most pipeline
category: Events
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-funnels
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Hallway Demo Performance Monitor

This drill builds the ongoing reporting layer for hallway demo operations. It tracks which events produce pipeline, which conversation approaches convert best, and whether the hallway demo motion is improving over time.

## Input

- PostHog events from `hallway-demo-operations` drill (conversation_started, demo_given, meeting_booked, deal_created)
- Attio deal records tagged with event source
- At least 3 events worth of data (minimum viable dataset for comparison)

## Steps

### 1. Build the hallway demo dashboard

Using the `posthog-dashboards` fundamental, create a dedicated "Hallway Demos" dashboard with these panels:

**Top row (headline metrics):**
- Total conversations started (last 30/90 days)
- Demo-to-meeting conversion rate
- Cost per meeting (travel cost / meetings booked)
- Pipeline generated from hallway demos ($)

**Middle row (per-event breakdown):**
- Table: event name, date, city, conversations, demos, meetings, deals, pipeline value, travel cost, ROI
- Bar chart: meetings booked per event
- Funnel: conversation_started -> demo_given -> meeting_booked -> deal_created -> deal_won

**Bottom row (optimization signals):**
- Interest level distribution (what % are 4-5 vs 1-2?)
- Average demo length for meetings booked vs not booked
- Day-of-week and time-of-day conversion patterns
- Follow-up response rate by interest tier

### 2. Build the event ROI comparison

Using `posthog-funnels`, create a funnel analysis that compares events side by side. Group by `event_name` property to see which events have the best conversion at each stage. This identifies:

- Events with high conversation volume but low demo conversion (wrong audience)
- Events with high demo conversion but low meeting booking (demo is good but CTA is weak)
- Events with high meeting booking but low deal creation (qualification problem)

### 3. Configure automated reporting

Using `n8n-scheduling`, create a workflow that runs weekly:

1. Pull hallway demo metrics from PostHog for the last 7 days
2. Pull deal status updates from Attio using `attio-reporting`
3. Calculate: new conversations, meetings booked, pipeline created, deals advanced, deals won
4. Compare to previous week and 4-week rolling average
5. Generate a summary report with:
   - This week's numbers vs rolling average
   - Best and worst performing event (if multiple this week)
   - Upcoming events on the calendar with expected ROI
   - Recommended actions (e.g., "Meeting booking rate dropped 15% -- review demo CTA")
6. Post the report to Slack and store in Attio

### 4. Build trend analysis

Using `posthog-custom-events`, track meta-metrics that show improvement over time:

- **Conversations per event**: Are you getting more efficient at starting conversations?
- **Demo-to-meeting rate**: Is your demo improving?
- **Cost per pipeline dollar**: Is the motion becoming more cost-effective?
- **Time from conversation to deal**: Is the sales cycle shortening?

Set alerts via n8n for:
- Cost per meeting exceeds 2x the 4-week average
- Demo-to-meeting rate drops below 20%
- No meetings booked from an event (complete miss)
- Pipeline from hallway demos exceeds monthly target (celebrate)

### 5. Generate event selection intelligence

After 5+ events, the data tells you which events to prioritize. Build a lookup that correlates:

- Event type (conference, meetup, workshop, summit) with conversion rates
- Event size with conversation density
- City/region with ICP match quality
- Event topic with deal size

Feed this intelligence back into the `event-scouting` drill to improve future event selection scoring.

## Output

- PostHog dashboard with real-time hallway demo metrics
- Weekly automated performance reports
- Event ROI comparison data
- Trend analysis showing motion improvement over time
- Event selection intelligence for future scouting

## Triggers

- Dashboard: always-on, check daily
- Weekly report: every Monday via n8n cron
- Event ROI comparison: after each event (allow 30 days for deal progression)

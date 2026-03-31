---
name: piggyback-meetup-performance-monitor
description: Track and report on piggyback meetup ROI across conferences, identifying which events, formats, and promotion channels produce the most pipeline
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

# Piggyback Meetup Performance Monitor

This drill builds the ongoing reporting layer for piggyback meetup operations. It tracks which conferences produce the best piggyback ROI, which promotion channels drive the most RSVPs, and whether the piggyback motion is improving over time.

## Input

- PostHog events from `piggyback-event-promotion` drill (invite_sent, rsvp_registered, attended, meeting_booked)
- PostHog events from `meetup-pipeline` drill (event execution tracking)
- Attio deal records tagged with piggyback event source
- At least 2 piggyback events worth of data (minimum viable dataset for comparison)

## Steps

### 1. Build the piggyback meetup dashboard

Using the `posthog-dashboards` fundamental, create a dedicated "Piggyback Meetups" dashboard with these panels:

**Top row (headline metrics):**
- Total RSVPs across all piggyback events (last 30/90 days)
- Average attendance rate (attended / registered)
- Meetings booked from piggyback events
- Pipeline generated ($) from piggyback attendees
- Cost per RSVP (venue + food + promotion / RSVPs)

**Middle row (per-conference breakdown):**
- Table: conference name, date, city, invites sent, RSVPs, attendance, meetings booked, pipeline value, total cost, ROI
- Bar chart: meetings booked per piggyback event
- Funnel: invite_sent -> rsvp_registered -> attended -> meeting_booked -> deal_created

**Bottom row (promotion channel analysis):**
- RSVPs by source channel (email vs LinkedIn vs organic vs referral)
- Open rate and RSVP rate by email template
- Invite-to-RSVP conversion rate by contact segment (speakers vs sponsors vs attendees)
- Meetup format performance (roundtable vs demo night vs mixer vs workshop)

### 2. Build the conference ROI comparison

Using `posthog-funnels`, create a funnel analysis that compares piggyback events side by side. Group by `conference` property to see which conferences produce the best conversion at each stage. This identifies:

- Conferences with high invite volume but low RSVPs (wrong audience or weak promotion)
- Conferences with high RSVPs but low attendance (no-show problem; timing or venue issue)
- Conferences with high attendance but low meetings (meetup format or follow-up problem)
- Conferences with high meetings but low pipeline (qualification mismatch)

### 3. Configure automated reporting

Using `n8n-scheduling`, create a workflow that runs after each piggyback event (triggered 7 days post-event to allow follow-up data to accumulate):

1. Pull piggyback event metrics from PostHog for the specific conference
2. Pull deal status updates from Attio using `attio-reporting`
3. Calculate: invites sent, RSVPs, attendance rate, meetings booked, pipeline created, cost per meeting
4. Compare to the running average across all previous piggyback events
5. Generate a post-event report with:
   - This event's numbers vs historical average
   - Which promotion channel drove the most RSVPs
   - Attendee quality score (% that matched ICP, % that booked meetings)
   - Recommended changes for the next piggyback event
6. Post the report to Slack and store in Attio as a note on the conference record

Create a separate monthly summary workflow:
1. Aggregate all piggyback events for the month
2. Calculate: total spend, total pipeline, blended cost per meeting, pipeline velocity
3. Compare month-over-month trends
4. Identify the next quarter's target conferences based on historical performance patterns

### 4. Build trend analysis

Using `posthog-custom-events`, track meta-metrics that show improvement over time:

- **RSVP rate per conference:** Are invitations converting better as you refine targeting and copy?
- **Attendance rate:** Are no-shows declining as you improve reminders and venue selection?
- **Meetings per attendee:** Is the meetup format producing more pipeline opportunities?
- **Cost per pipeline dollar:** Is the motion becoming more cost-effective over time?
- **Time from meetup to first meeting:** Is the follow-up cadence shortening the gap?

Set alerts via n8n for:
- Attendance rate drops below 50% (venue or timing problem)
- No meetings booked from a piggyback event (format or audience mismatch)
- Cost per meeting exceeds 2x the running average
- Pipeline from piggyback events exceeds monthly target

### 5. Generate conference selection intelligence

After 4+ piggyback events, the data tells you which conferences to target. Build a lookup that correlates:

- Conference size (1,000 vs 5,000 vs 10,000 attendees) with piggyback RSVP rate
- Conference industry vertical with ICP match quality
- Conference city with attendance rate (local vs travel-heavy audiences)
- Day of week (Monday evening vs Wednesday evening vs Thursday evening) with attendance
- Venue proximity to conference (same hotel lobby vs 2 blocks away vs 10 min taxi) with attendance rate

Feed this intelligence back into the `event-scouting` drill to improve future conference selection for piggybacking.

## Output

- PostHog dashboard with real-time piggyback meetup metrics
- Post-event automated reports (7 days after each event)
- Monthly summary with trends and recommendations
- Conference selection intelligence for future scouting
- Promotion channel effectiveness data for optimizing outreach mix

## Triggers

- Dashboard: always-on, check after each event
- Post-event report: 7 days after each piggyback meetup via n8n
- Monthly summary: first Monday of each month
- Conference intelligence refresh: quarterly

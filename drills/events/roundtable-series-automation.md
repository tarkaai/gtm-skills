---
name: roundtable-series-automation
description: Automate recurring micro-roundtable operations including topic rotation, guest curation, invitation scheduling, and cross-event analytics
category: Events
tools:
  - n8n
  - Loops
  - Attio
  - PostHog
  - Cal.com
  - Fireflies
  - Clay
fundamentals:
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - loops-broadcasts
  - loops-audience
  - attio-lists
  - attio-contacts
  - attio-automation
  - attio-notes
  - posthog-custom-events
  - posthog-funnels
  - calcom-event-types
  - fireflies-transcription
  - clay-people-search
  - clay-enrichment-waterfall
---

# Roundtable Series Automation

This drill transforms one-off roundtables into a repeatable series that runs bi-weekly or monthly with minimal manual effort. The agent handles topic scheduling, guest curation, invitation ops, and cross-event analytics. The human facilitates the discussion.

Roundtable series have a unique challenge: guest freshness. Unlike webinars where repeat attendance is good, roundtables need a mix of returning participants (for continuity) and new participants (for fresh perspectives). This drill manages that balance.

## Prerequisites

- At least 2 completed roundtables with performance data (from Baseline level)
- n8n instance with active connections to Loops, Attio, and PostHog
- Fireflies.ai configured for meeting transcription
- Clay table with ICP-matched prospects for guest sourcing
- Attio with full history of past roundtable attendance and engagement

## Steps

### 1. Build the topic calendar

Create a topic backlog scored on three factors:

- **Timeliness (1-5)**: Is this topic urgent right now? Recent industry news, regulation changes, or technology shifts score high.
- **Discussion potential (1-5)**: Will this topic generate debate? Topics with clear "camps" or tradeoffs score higher than topics with consensus answers.
- **Guest availability (1-3)**: Can you invite people who have direct experience with this topic? Score based on how many ICP contacts in Attio have relevant context.

Using `attio-lists`, create a "Roundtable Calendar" list with fields: topic, date, target guest profile, confirmed guests, status, and discussion questions. Schedule events bi-weekly or monthly for the next 3 months.

### 2. Automate the guest curation engine

Using `n8n-scheduling`, create a workflow that triggers 28 days before each roundtable:

**Day -28: Guest sourcing**
- Query Attio using `attio-lists` for contacts matching the event's target guest profile
- Filter out: anyone who attended the last roundtable (prevent fatigue), anyone who declined the last 2 invitations (respect their time), anyone currently in an active sales cycle (avoid awkwardness)
- Target a 60/40 mix: 60% new invitees, 40% past attendees who were high-engagement
- Using `clay-people-search` and `clay-enrichment-waterfall`, source 5-10 net-new prospects who match the topic and ICP but are not yet in Attio

**Day -21: Send Wave 1 invitations**
- Using `loops-broadcasts`, send personal invitations to the top 10 targets
- Personalize the first line for each recipient based on Attio notes or recent activity
- Include Cal.com RSVP link created via `calcom-event-types`

**Day -14: Send Wave 2 + follow-ups**
- Send invitations to the remaining list
- Send follow-up to Wave 1 non-responders
- Include confirmed attendee count: "5 confirmed so far, including [anonymized profiles]"

**Day -7: Final push + logistics**
- If under 6 confirmed: send urgent outreach to waitlist or new targets
- If 8+ confirmed: stop invitations, activate waitlist
- Send confirmed attendees: discussion questions, attendee list (first name + company), and calendar reminder

**Day -1: Prep the host**
- Generate a briefing document: attendee names, companies, roles, Attio engagement history, past roundtable participation, and 1 relevant data point per person
- Verify Fireflies.ai is connected to the scheduled meeting using `fireflies-transcription`
- Send 1-hour reminder to all confirmed attendees

**Day +1: Post-event automation**
- Trigger the `roundtable-attendee-nurture` drill with attendee engagement data
- Generate the discussion summary from the Fireflies transcript
- Store the summary in Attio using `attio-notes`
- Update all attendee records in Attio: attendance status, engagement tier

### 3. Build cross-event analytics

Using `posthog-custom-events` and `posthog-funnels`, track metrics across the series:

- **Guest pipeline per event**: invited -> confirmed -> attended -> engaged -> meeting_booked -> deal_created
- **Series-level metrics**: guest repeat rate (what % attend 2+ roundtables), topic-to-pipeline correlation, invitation channel effectiveness
- **Cumulative pipeline**: total meetings booked, average meetings per roundtable, pipeline trend over time
- **Guest freshness**: % of new vs returning guests per event (target: 50-70% new per event)

Create a PostHog dashboard: RSVP confirmations by event (bar chart), show rate trend (line chart), meetings booked per roundtable (bar chart), guest freshness ratio (stacked bar), and engagement tier distribution (pie chart).

### 4. Manage the guest pool

Roundtable series live or die by the quality and freshness of the guest pool. Using `n8n-workflow-basics`, build a guest pool management system:

- **Always-on sourcing**: Weekly, use `clay-people-search` to find 5 new ICP-matched contacts based on recent signals (job changes, LinkedIn posts on relevant topics, conference appearances). Import to Attio with tag "roundtable-prospect".
- **Engagement scoring**: After each roundtable, update every attendee's cumulative engagement score in Attio. Factors: number of roundtables attended, average engagement tier, follow-up conversion (did they book a meeting?), referrals made.
- **Graduated promotion**: Contacts who attend 3+ roundtables and engage highly should be flagged for a different relationship track (advisory board, case study, partnership).
- **Retirement**: Remove contacts from the active pool after 3 consecutive declines or 2 no-shows.

### 5. Implement series-level optimizations

After every 4 roundtables, the agent should analyze:

- Which topics drove the highest show rate? The highest post-event meeting conversion?
- Which guest mix (industry diversity, seniority level, company stage) produced the best discussions?
- What day of week and time slot had the best confirmation rate?
- Do returning guests convert at higher or lower rates than first-timers?
- Which invitation channel (personal email, Loops broadcast, LinkedIn) has the highest RSVP rate?

Store findings in Attio as notes on the calendar list. Adjust upcoming events based on data.

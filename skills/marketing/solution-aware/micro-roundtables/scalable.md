---
name: micro-roundtables-scalable
description: >
  Micro-Roundtable — Scalable Automation. Scale to a recurring bi-weekly or monthly
  roundtable series with automated guest sourcing, invitation cadences, cross-event
  analytics, and A/B tested formats. The agent runs operations; the human facilitates.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: "≥ 40 total attendees and ≥ 12 meetings booked across 4-6 events over 2 months"
kpis: ["RSVP rate (target ≥ 40%)", "Show rate (target ≥ 75%)", "Meeting conversion rate (target ≥ 20% of attendees)", "Guest pool freshness (target ≥ 50% new per event)", "Cost per meeting booked"]
slug: "micro-roundtables"
install: "npx gtm-skills add marketing/solution-aware/micro-roundtables"
drills:
  - roundtable-series-automation
  - ab-test-orchestrator
---

# Micro-Roundtable — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

Scale from one-off roundtables to a recurring series (bi-weekly or monthly) with automated operations. The agent handles guest sourcing, invitation cadences, RSVP management, transcript processing, follow-up sequencing, and cross-event analytics. The human shows up and facilitates the discussion. If the series consistently produces 2-3 meetings per event at 8+ attendees with a guest pool that stays fresh, it justifies autonomous optimization at Durable.

Pass: 40 or more total attendees AND 12 or more meetings booked across 4-6 events over 2 months.
Fail: Fewer than 40 attendees OR fewer than 12 meetings.

## Leading Indicators

- Guest pool depth stays above 30 uninvited ICP contacts after 4 events (signals guest sourcing keeps up with consumption)
- Repeat attendee rate stays below 50% per event (signals the series attracts new prospects, not just a fan club)
- RSVP rate holds steady or improves across events (signals the series reputation is building)
- At least 2 attendees per event express follow-up interest during the discussion without prompting (signals organic conversion opportunity)

## Instructions

### 1. Launch the automated roundtable series

Run the `roundtable-series-automation` drill to set up the full series infrastructure:

**Topic calendar**: Build a 3-month topic backlog with 6-8 topics scored by timeliness, discussion potential, and guest availability. Store in Attio as a "Roundtable Calendar" list. Schedule events bi-weekly or monthly based on your Baseline data — use whichever cadence your guest pool can sustain without fatigue.

**Automated guest sourcing**: Configure the n8n workflow that runs 28 days before each event:
- Pull ICP-matched contacts from Attio, filtering out recent attendees and serial decliners
- Use Clay to find 5-10 net-new prospects per event who match the topic and ICP
- Maintain a 60/40 mix: 60% new invitees, 40% high-engagement returning guests

**Automated invitation cadences**: Set up the Loops-powered invitation engine:
- Day -21: Wave 1 personal invitations to top 10 targets
- Day -14: Wave 2 broader invitations + Wave 1 follow-ups
- Day -7: Final push with urgency ("3 spots remaining") if under 8 confirmed
- Day -3: Confirmed attendee list, discussion questions, logistics
- Day -1: Host briefing with per-attendee context
- Day 0: 1-hour reminder with join link

**Post-event automation**: Configure n8n to trigger after each event:
- Process Fireflies transcript and generate discussion summary
- Segment attendees by engagement tier
- Enroll each tier in the appropriate Loops nurture sequence
- Create Attio deals for high-intent attendees
- Update all attendee records with engagement data

### 2. A/B test event variables

Run the `ab-test-orchestrator` drill to systematically test roundtable variables. Test one variable at a time across consecutive events:

**Variables to test (in priority order):**

1. **Topic framing**: Same underlying topic, different framing. Example: "How are you handling AI governance?" vs "The AI governance mistake most teams make." Measure: RSVP rate difference.

2. **Time slot**: Test morning (10am) vs afternoon (2pm) vs evening (5pm). Measure: show rate and engagement rate.

3. **Group size**: Test 5-6 attendees (more intimate) vs 8-10 (more diverse perspectives). Measure: engagement rate and meeting conversion rate.

4. **Discussion format**: Structured (3 questions, 15 min each) vs semi-structured (1 opening question, let the conversation flow). Measure: engagement rate and post-event meeting conversion.

5. **Invitation channel**: Personal email from host vs Loops broadcast with host's name. Measure: RSVP rate.

For each test, use PostHog experiments to track the variant and measure outcomes. Document results in Attio. After 4-6 events, you should have data on the optimal configuration for your audience.

### 3. Build cross-event analytics

Using the `roundtable-series-automation` drill's analytics components, create a PostHog dashboard showing:

- **Registration pipeline**: RSVP confirmations by event (bar chart), RSVP rate trend across events (line chart)
- **Attendance quality**: Show rate trend, engagement tier distribution per event (stacked bar), guest freshness ratio (new vs returning) per event
- **Conversion funnel**: The full funnel from invitation to meeting booked, compared across events
- **Series health**: Guest pool depth over time (are you sourcing faster than consuming?), topic performance comparison, cumulative pipeline generated

### 4. Scale guest sourcing through Clay

For each upcoming roundtable, use Clay to expand the guest pool:

- Search for people with ICP-matching titles who have recently posted about the roundtable topic on LinkedIn
- Enrich with email and company data
- Score by fit (title, company stage, industry relevance)
- Import the top 10 into Attio with tag "roundtable-prospect"
- Add to the Wave 2 invitation list

Target: source 10-15 net-new, topic-relevant prospects per event. This ensures the guest pool grows faster than it is consumed.

### 5. Evaluate against threshold

After 2 months (4-6 events), aggregate:

- Total attendees across all events (target: ≥ 40)
- Total meetings booked (target: ≥ 12)
- Per-event averages: attendees, meetings, RSVP rate, show rate, meeting conversion rate
- Guest pool health: depth, freshness, and engagement trends
- A/B test results: which variables had the biggest impact
- Cost per meeting: total tool costs / meetings booked

- **PASS:** Proceed to Durable. Document the optimal configuration (topic type, time slot, group size, format, invitation channel). The series is producing meetings at scale with manageable effort.
- **MARGINAL (40+ attendees but 8-11 meetings):** Conversion is the bottleneck. Focus on improving: follow-up speed, discussion-to-meeting bridging during the event, and Tier 1 nurture personalization. Run 2 more events with improved conversion tactics.
- **FAIL (< 40 attendees):** Diagnose: Is the guest pool exhausted? Are topics repeating? Is invitation fatigue setting in? Reduce cadence, refresh the topic approach, and activate new sourcing channels.

## Time Estimate

- Series automation setup (n8n workflows, Loops sequences, Clay tables): 6 hours (one-time)
- Per-event agent-automated ops: 1 hour of human oversight per event (review invitations, approve follow-ups, facilitate the discussion)
- A/B test design and analysis: 2 hours total across the period
- Cross-event analytics and reporting: 1 hour/month
- Total: ~16-20 hours of human effort over 2 months; ~20 hours of agent-automated work

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Guest pool management, deal tracking, event calendar | Free for up to 3 users; Plus: $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Cal.com | RSVP pages and follow-up meeting booking | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Loops | Invitation cadences, reminders, nurture sequences | $49/mo for up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Fireflies.ai | Automated transcription per event | Pro: $10/user/mo annual ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| PostHog | Event analytics, funnels, experiments | Free up to 1M events/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| Clay | Net-new guest sourcing and enrichment | Launch: $185/mo for 2,500 credits ([clay.com/pricing](https://clay.com/pricing)) |
| n8n | Workflow automation for series operations | Self-hosted: free; Cloud: from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Zoom / Google Meet | Host the roundtable | Free tier |

**Estimated monthly cost for Scalable:** $268-473/mo (Loops $49 + Fireflies $10 + Clay $185 + n8n $24 + optional Attio Plus $29/user)

## Drills Referenced

- `roundtable-series-automation` — automate recurring roundtable operations: guest sourcing, invitation cadences, transcript processing, follow-up sequencing, and cross-event analytics
- `ab-test-orchestrator` — design, run, and analyze A/B tests on roundtable variables (topic framing, time slot, group size, format, invitation channel)

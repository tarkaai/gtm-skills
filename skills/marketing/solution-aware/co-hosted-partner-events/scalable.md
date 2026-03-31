---
name: co-hosted-partner-events-scalable
description: >
  Co-hosted Partner Events — Scalable Automation. Scale to bi-weekly or monthly
  events with 5+ rotating partners. Agent automates partner scheduling,
  event templating, multi-channel promotion, post-event follow-up routing,
  and A/B testing of event formats and topics.
stage: "Marketing > SolutionAware"
motion: "PartnershipsWarmIntros"
channels: "Events"
level: "Scalable Automation"
time: "60 hours over 6 months"
outcome: "≥250 attendees and ≥50 qualified leads from 8+ co-hosted events over 6 months"
kpis: ["Events per month", "Average attendees per event", "Attendee-to-lead conversion rate", "Cost per qualified lead", "Partner portfolio size"]
slug: "co-hosted-partner-events"
install: "npx gtm-skills add marketing/solution-aware/co-hosted-partner-events"
drills:
  - partner-pipeline-automation
  - follow-up-automation
  - ab-test-orchestrator
---

# Co-hosted Partner Events — Scalable Automation

> **Stage:** Marketing → SolutionAware | **Motion:** PartnershipsWarmIntros | **Channels:** Events

## Outcomes

Scale from 3 events to 8+ events over 6 months with 5+ rotating partners. Automate the operational overhead so each incremental event requires minimal marginal effort. The 10x multiplier: more partners, more formats, more frequent events — without proportional time investment. Pass threshold: ≥250 total attendees and ≥50 qualified leads.

## Leading Indicators

- Partner pipeline of 10+ qualified partners in Attio, with 5+ confirmed for upcoming events
- Event cadence of 1-2 per month sustained over 6 months
- Average ≥30 registrations per event with partner contribution ≥40%
- Automated follow-up sequences producing ≥3 meetings per event without manual intervention
- A/B tests producing statistically significant winners on format, topic, or promotion timing
- Cost per qualified lead stable or declining quarter-over-quarter

## Instructions

### 1. Build the partner pipeline automation

Run the `partner-pipeline-automation` drill adapted for event partnerships. Build these n8n workflows:

**Partner outreach automation:**
- Trigger: new partner added to "Event Partner Prospects" list in Attio
- Action: send personalized outreach email via Loops proposing a co-hosted event, referencing their audience overlap and a specific topic idea
- Follow-up: if no reply in 5 days, send one follow-up
- If positive reply: create Attio deal in "Event Partnerships" pipeline, move to "Alignment" stage

**Event scheduling automation:**
- Trigger: partner deal moves to "Confirmed" stage in Attio
- Action: create event in Luma from template, assign event date, populate partner-specific fields (co-branded title, partner logo, speaker names)
- Action: create promotion tasks: 3 email sends and 3 social posts on scheduled dates
- Action: notify the agent and the partner contact with event details and promotion calendar

**Post-event pipeline automation:**
- Trigger: event date passes (Attio date field)
- Action: export attendee list from Luma, enrich with Clay, tag in Attio by engagement level
- Action: fire PostHog events for all attendees
- Action: trigger follow-up email sequences based on engagement level (see step 3)

### 2. Scale to 5+ rotating partners

Expand the partner portfolio:
- Run `partner-prospect-research` quarterly to refresh the pipeline with 10-15 new candidates
- Prioritize partners whose Baseline scores were highest (registration contribution, attendee quality)
- Rotate partners so the same audience does not see the same two companies co-hosting repeatedly — aim for each partner to co-host 2-3 events over 6 months
- Use Crossbeam account mapping (if available) to prioritize partners with the highest target account overlap

Build a partner event calendar in Attio: a list view showing each partner, their next scheduled event, their last event performance, and their partner score.

### 3. Automate post-event follow-up

Run the `follow-up-automation` drill to build engagement-tiered follow-up sequences in n8n:

**Hot attendees (asked questions, chatted actively):**
1. Within 24 hours: personal email from the speaker referencing their question + Cal.com booking link
2. Day 3: if no reply, LinkedIn connection request with a personalized note
3. Day 7: if no meeting booked, share a relevant case study or resource

**Warm attendees (attended full session):**
1. Within 24 hours: automated thank-you email with recording link + key takeaways + Cal.com CTA
2. Day 5: if no click on CTA, send a different-angle follow-up (e.g., "Our most popular resource on {topic}")
3. Day 14: add to nurture sequence for future events

**Cool attendees (registered but did not attend):**
1. Within 24 hours: "Sorry we missed you" + recording link + CTA
2. Day 7: if no engagement, add to nurture sequence for next event invite

Set guardrails: maximum 4 touches per attendee across all channels. Suppress anyone who replies negatively or unsubscribes.

### 4. A/B test event formats and topics

Run the `ab-test-orchestrator` drill to systematically test:

**Format tests (run across 4+ events):**
- Webinar (30-60 min) vs Workshop (60-90 min hands-on)
- Single-speaker deep dive vs Panel discussion
- Virtual-only vs Hybrid (virtual + in-person component)

**Topic tests (run across 4+ events):**
- Pain-focused topics ("How to solve X") vs Aspiration-focused ("How top teams achieve Y")
- Tactical topics (step-by-step how-to) vs Strategic topics (trends and roadmap)
- Narrow topics (specific use case) vs Broad topics (industry overview)

**Promotion tests (run across 4+ events):**
- Email-heavy promotion (5 emails) vs Social-heavy promotion (5 posts, 2 emails)
- Early announcement (4 weeks out) vs Late push (2 weeks out)
- Partner-led promotion vs Your-led promotion

Track results in PostHog: registration count, attendance rate, engagement rate, and pipeline conversion per variant. After 4+ events, identify statistically significant winners. Double down on winning formats and topics for remaining events.

### 5. Build event content repurposing pipeline

After each event, the agent repurposes content to extend reach:
- Extract key quotes and insights from the recording transcript
- Draft 2-3 LinkedIn posts from event highlights (for your account and the partner's)
- Create a blog post summary with embedded recording
- Extract 3-5 short video clips (if using Riverside for recording) for social distribution
- Draft a "lessons learned" email for your subscriber list referencing the event topic

This extends the ROI of each event beyond the live attendees.

### 6. Monitor scale metrics

Track weekly in PostHog dashboards:
- Events scheduled in next 30 days
- Registrations per event (trending up, stable, or declining)
- Attendance rate per event
- Qualified leads per event
- Cost per qualified lead
- Partner pipeline health: how many partners are in each stage

Set alerts in n8n:
- If registrations for an upcoming event are <50% of target 7 days before → boost promotion
- If attendance rate drops below 40% for 2 consecutive events → investigate timing or topic
- If a partner's events consistently underperform → flag for partner review

### 7. Evaluate against threshold

Aggregate across all events over 6 months: ≥250 total attendees and ≥50 qualified leads. If PASS → proceed to Durable with proven formats, top partners, and automated operations. If FAIL → identify whether the bottleneck is partner supply (not enough events), demand (not enough registrations per event), or conversion (attendees not converting to leads). Fix the weakest link and extend the Scalable window.

## Time Estimate

- Partner pipeline automation setup: 8 hours
- Follow-up automation setup: 6 hours
- A/B test design and configuration: 4 hours
- Per-event execution (x8+, highly automated): 3 hours each = 24 hours
- Content repurposing pipeline: 4 hours setup + ongoing
- Monthly monitoring and optimization: 2 hours/mo x 6 = 12 hours
- Threshold evaluation: 2 hours
- Total: ~60 hours over 6 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Luma | Event platform for 8+ events | Plus $59/mo (API access for automation) |
| n8n | Partner pipeline, follow-up, and scheduling automation | Self-hosted free; Cloud $24/mo |
| PostHog | Event funnels, A/B test tracking, dashboards | Free up to 1M events/mo |
| Attio | Partner CRM, attendee records, event calendar | Pro $29/user/mo |
| Clay | Partner research and attendee enrichment at scale | Launch $185/mo |
| Loops | Promotion emails, reminders, follow-up sequences | Growth $49/mo |
| Cal.com | Meeting booking for all events | Free (basic) |
| Riverside | Event recording and clip extraction | Standard $19/mo |
| Crossbeam | Partner account overlap mapping (optional) | Free (3 seats); Connector $400/mo |

**Play-specific cost at Scalable:** ~$150-350/mo (Luma Plus + Loops Growth + Riverside Standard + optional Crossbeam)

## Drills Referenced

- `partner-pipeline-automation` — automate partner outreach, event scheduling, and post-event processing across 5+ partners
- `follow-up-automation` — build engagement-tiered follow-up sequences that convert attendees to meetings without manual effort
- `ab-test-orchestrator` — systematically test event formats, topics, and promotion strategies to find the 10x combination

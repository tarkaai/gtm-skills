---
name: co-hosted-partner-events-smoke
description: >
  Co-hosted Partner Events — Smoke Test. Run one co-hosted event with a single
  partner to validate that combining audiences produces qualified leads.
  Agent identifies the partner, builds the event page, prepares co-promotion
  assets, and tracks results. Human runs the live event.
stage: "Marketing > SolutionAware"
motion: "PartnershipsWarmIntros"
channels: "Events"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: "≥30 registrations, ≥20 attendees, and ≥3 qualified leads from 1 co-hosted event"
kpis: ["Registration count", "Attendance rate", "Qualified leads generated", "Attendee-to-meeting conversion rate"]
slug: "co-hosted-partner-events"
install: "npx gtm-skills add marketing/solution-aware/co-hosted-partner-events"
drills:
  - partner-prospect-research
  - co-hosted-event-orchestration
  - threshold-engine
---

# Co-hosted Partner Events — Smoke Test

> **Stage:** Marketing → SolutionAware | **Motion:** PartnershipsWarmIntros | **Channels:** Events

## Outcomes

Run one co-hosted event with a single partner. Prove that combining two audiences produces registrations and qualified leads that neither company would get alone. The pass threshold is ≥30 registrations, ≥20 attendees, and ≥3 qualified leads.

## Leading Indicators

- Partner responds positively to co-host proposal within 5 business days
- Combined promotion drives ≥30 registrations (each side contributing ≥10)
- Attendance rate ≥60% of registrations
- ≥3 attendees ask questions or engage actively during the event
- ≥1 attendee books a follow-up meeting within 7 days of the event

## Instructions

### 1. Find and qualify one partner

Run the `partner-prospect-research` drill scoped to a single partner. The agent searches Clay for companies that share your ICP's audience but are not competitors — adjacent products serving the same buyer persona. Score candidates on audience overlap, company stage, and whether they have an active marketing presence (blog, newsletter, social following). Select the top-scoring partner.

Output: one qualified partner record in Attio with contact info for the partnerships or marketing lead.

### 2. Propose the co-hosted event to the partner

The agent drafts a co-host proposal email to the partner contact. The email must include:
- A specific event topic relevant to both audiences
- Proposed format (webinar recommended for Smoke — lowest logistics)
- Proposed date 3-4 weeks out
- What each side provides: you handle event platform and registration; partner promotes to their audience
- Expected outcome: 30+ attendees, shared attendee list

**Human action required:** Review and send the proposal email. Negotiate any changes on a 20-minute alignment call. Confirm the event brief (topic, date, format, speaker assignments, lead-sharing rules).

### 3. Build the event

Run the `co-hosted-event-orchestration` drill to:
1. Create the event on Luma (free tier) with co-branded title and description
2. Configure registration fields: name, email, company, role, attribution source
3. Set up a Cal.com booking link for post-event follow-up meetings
4. Fire `cohosted_event_registered` events to PostHog on each registration
5. Draft 3 promotion emails for your audience (announcement, reminder, last chance) via Loops
6. Draft 3 LinkedIn posts (announcement, speaker spotlight, day-of reminder) tagging the partner
7. Pull 20-30 target prospects from Attio and draft personal invitation emails

**Human action required:** Post the LinkedIn content. Send personal invites to high-value prospects. Share draft promotion assets with the partner for their audience.

### 4. Run the event

**Human action required:** Execute the live event. The agent prepares:
- Speaker run-of-show document with time allocations
- 5-7 engagement questions and poll questions
- Backup talking points for slow Q&A
- Note-taking template to capture attendee questions and engagement signals

During or immediately after the event, log which attendees asked questions (hot), stayed for the full session (warm), or dropped early (cool).

### 5. Process attendees and follow up

Within 24 hours post-event, the agent:
1. Exports the full attendee list from Luma
2. Tags each attendee in Attio with the event name and engagement level (hot/warm/cool)
3. Fires `cohosted_event_attended` events to PostHog with engagement level and source partner
4. Sends two follow-up emails via Loops:
   - Attendees: thank you + recording link + key takeaways + Cal.com booking CTA
   - No-shows: "sorry we missed you" + recording link + same CTA
5. For hot attendees (asked questions), drafts personalized emails referencing their specific question

**Human action required:** Review and send the personalized follow-up emails to hot attendees. Share the attendee list with the partner per agreed rules.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to measure: ≥30 registrations, ≥20 attendees, and ≥3 qualified leads. A qualified lead is an attendee who either (a) booked a follow-up meeting or (b) replied positively to the follow-up email and matches your ICP.

If PASS → document what worked (topic, format, promotion channel, partner) and proceed to Baseline.
If FAIL → diagnose: was the problem low registrations (promotion), low attendance (topic/timing), or low conversion (wrong audience)? Adjust and re-run with the same or different partner.

## Time Estimate

- Partner research and outreach: 2 hours
- Event setup and promotion prep: 3 hours
- Post-event processing and follow-up: 2 hours
- Threshold evaluation: 1 hour
- Total: 8 hours of agent + human time over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Luma | Event page, registration, attendee tracking | Free (unlimited events); Plus $59/mo for API access |
| Clay | Partner research and attendee enrichment | Launch $185/mo (2,500 credits) |
| Cal.com | Post-event meeting booking links | Free (basic); Teams $15/user/mo |
| Loops | Promotion emails and follow-up sequences | Free up to 1,000 contacts |
| Attio | CRM for partner and attendee records | Free up to 3 users |
| PostHog | Event tracking and attribution | Free up to 1M events/mo |

**Play-specific cost at Smoke:** Free (all tools have free tiers sufficient for 1 event)

## Drills Referenced

- `partner-prospect-research` — find and qualify one co-host partner from adjacent companies
- `co-hosted-event-orchestration` — build the event page, promotion assets, and post-event processing
- `threshold-engine` — measure results against pass threshold and decide next step

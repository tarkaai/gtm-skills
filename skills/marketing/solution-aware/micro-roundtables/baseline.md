---
name: micro-roundtables-baseline
description: >
  Micro-Roundtable — Baseline Run. Run 2-3 roundtables over 4 weeks with event
  analytics, structured follow-up sequences, and repeatable operations to validate
  that the format consistently produces meetings.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Baseline Run"
time: "12 hours over 4 weeks"
outcome: "≥ 12 total attendees across 2-3 events AND ≥ 4 follow-up meetings booked"
kpis: ["RSVP rate (target ≥ 40%)", "Show rate (target ≥ 75%)", "Meeting conversion rate (target ≥ 20% of attendees)", "Follow-up reply rate (target ≥ 25%)"]
slug: "micro-roundtables"
install: "npx gtm-skills add marketing/solution-aware/micro-roundtables"
drills:
  - roundtable-pipeline
  - roundtable-attendee-nurture
  - posthog-gtm-events
---

# Micro-Roundtable — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

Validate that micro-roundtables produce meetings consistently across multiple events, not just once. Run 2-3 roundtables over 4 weeks with proper event analytics, structured tier-based follow-up, and repeatable operations. If the format consistently converts 20%+ of attendees to meetings, it justifies scaling to an automated series at Scalable.

Pass: 12 or more total attendees across 2-3 events AND 4 or more follow-up meetings booked.
Fail: Fewer than 12 total attendees OR fewer than 4 meetings after running 2-3 events.

## Leading Indicators

- Second roundtable fills to 8+ confirmed without expanding the invite list beyond 20 (signals organic demand and topic selection working)
- At least 1 attendee from the first roundtable refers a colleague for the second (signals peer value)
- Tier 1 follow-up reply rate exceeds 30% (signals the discussion-to-meeting bridge is working)
- Discussion summaries have >60% open rate (signals attendees value the content post-event)

## Instructions

### 1. Build event operations

Run the `roundtable-pipeline` drill to create a repeatable process for each roundtable. At Baseline, add tooling that was manual at Smoke:

- Set up Cal.com RSVP pages using the `calcom-event-types` fundamental — one event type per roundtable with max capacity of 10
- Configure Loops sequences for invitation emails, reminders (3 days before, 1 day before, 1 hour before), and post-event follow-up
- Connect Fireflies.ai to the video platform for automated transcription

For each of the 2-3 events, use the full `roundtable-pipeline` drill: topic selection, guest curation, invitation waves, execution, and discussion capture.

### 2. Configure event analytics

Run the `posthog-gtm-events` drill to track the full roundtable funnel. Create these events:

- `roundtable_invited` — fired when an invitation is sent (properties: contact_id, roundtable_slug, wave)
- `roundtable_confirmed` — fired when an RSVP is received (properties: contact_id, roundtable_slug)
- `roundtable_reminded` — fired when a reminder is sent (properties: contact_id, roundtable_slug, reminder_type)
- `roundtable_attended` — fired when attendance is confirmed post-event (properties: contact_id, roundtable_slug, engagement_level)
- `roundtable_engaged` — fired for attendees who spoke during the discussion (properties: contact_id, roundtable_slug, engagement_tier)
- `roundtable_nurture_sent` — fired for each follow-up email (properties: contact_id, roundtable_slug, tier, step)
- `roundtable_nurture_replied` — fired on follow-up reply (properties: contact_id, roundtable_slug, tier)
- `roundtable_meeting_booked` — fired when a meeting is booked (properties: contact_id, roundtable_slug, source_tier)

Build a PostHog funnel: invited -> confirmed -> attended -> engaged -> nurture_replied -> meeting_booked.

### 3. Run tier-based follow-up sequences

Run the `roundtable-attendee-nurture` drill after each event. This replaces the manual follow-up from Smoke with structured, tier-based sequences:

- **Tier 1 (high engagement)**: 3 emails over 7 days, each referencing specific discussion points. Direct meeting CTA with Cal.com link.
- **Tier 2 (medium engagement)**: 2 emails over 10 days. Share the discussion summary. Invite to the next roundtable.
- **Tier 3 (no-shows)**: 2 emails over 5 days. Share key takeaways (create FOMO). Invite to the next roundtable.

Key difference from Smoke: the agent generates the follow-up emails using Fireflies transcript data and sends them via Loops sequences, not manually. The host reviews and approves before sending.

**Human action required:** Review and approve each Tier 1 follow-up email before sending. These reference specific discussion points and must be accurate. Tier 2 and Tier 3 emails can be auto-sent after initial template approval.

### 4. Run 2-3 events and compare performance

Execute 2-3 roundtables over 4 weeks. Vary one factor per event to start building optimization data:

- Event 1: Use the topic and format that worked at Smoke
- Event 2: Change the topic (keep the same guest profile)
- Event 3 (optional): Change the guest profile or time slot (keep the best topic)

After each event, log in Attio: topic, date, invites sent, confirmed, attended, engagement tier distribution, meetings booked. Compare metrics across events to identify patterns.

### 5. Evaluate against threshold

Aggregate results across all events:

- Total attendees (target: ≥ 12 across 2-3 events)
- Total meetings booked (target: ≥ 4)
- RSVP rate, show rate, meeting conversion rate per event
- Follow-up reply rate by tier

- **PASS:** Proceed to Scalable. Document the best-performing topic, guest profile, and follow-up approach.
- **MARGINAL (12+ attendees but 2-3 meetings):** The event format works but conversion needs improvement. Analyze: are Tier 1 follow-ups referencing specific enough discussion points? Is the meeting CTA clear and well-timed? Run 1-2 more events with improved follow-up.
- **FAIL (< 12 attendees):** Diagnose: is the guest pool too shallow? Is the topic not resonating? Are invitations getting lost? Fix and re-run.

## Time Estimate

- Event operations setup (Cal.com, Loops, Fireflies): 2 hours (one-time)
- PostHog event tracking configuration: 1 hour (one-time)
- Per-event: guest curation (1 hour), invitation management (30 min), prep and facilitation (1.5 hours), follow-up sequence review (30 min) = 3.5 hours per event
- Total for 3 events: ~13.5 hours over 4 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Guest tracking, engagement logging, deal creation | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| Cal.com | RSVP pages and follow-up meeting booking | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Loops | Invitation emails, reminders, nurture sequences | Free up to 1,000 contacts; $49/mo for 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Fireflies.ai | Automated transcription and action items | Free plan: 800 min/month; Pro: $10/user/mo annual ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| PostHog | Event tracking and funnel analytics | Free up to 1M events/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| Zoom / Google Meet | Host the roundtable | Free tier |

**Estimated monthly cost for Baseline:** $0-59/mo (Loops $0-49 + Fireflies $0-10, depending on volume)

## Drills Referenced

- `roundtable-pipeline` — plan, curate, execute, and capture each roundtable
- `roundtable-attendee-nurture` — tier-based post-event follow-up sequences that convert attendees to meetings
- `posthog-gtm-events` — configure the event taxonomy for the full roundtable funnel

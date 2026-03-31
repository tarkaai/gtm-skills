---
name: micro-events-webinars-baseline
description: >
  Micro-Event or Webinar — Baseline Run. Run 2-3 webinars over 2-4 weeks with
  automated registration ops, post-event nurture sequences, and PostHog
  tracking across the full funnel. Validate repeatable demand and conversion.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Baseline Run"
time: "12 hours over 2-4 weeks"
outcome: ">=30 registrations across events, >=30% average show rate, >=2 meetings booked over 2-4 weeks"
kpis: ["Registrations per event", "Show rate", "Meetings booked", "Nurture reply rate"]
slug: "micro-events-webinars"
install: "npx gtm-skills add marketing/solution-aware/micro-events-webinars"
drills:
  - webinar-pipeline
  - posthog-gtm-events
  - webinar-attendee-nurture
---

# Micro-Event or Webinar — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Prove that webinar demand is repeatable across 2-3 events (not a one-time fluke)
- Establish automated post-event nurture that converts attendees to pipeline without manual follow-up
- Build the PostHog event tracking foundation for all future measurement and optimization
- Identify which topics, formats, and promotion channels produce the best results

## Leading Indicators

- Second event registrations reach at least 80% of first event registrations (demand holds)
- Nurture email reply rate >10% for active attendees (Tier 1)
- At least 1 meeting booked from automated nurture sequences (not just manual follow-up)
- Recording consumption rate >30% among no-shows (content has lasting value)

## Instructions

### 1. Configure webinar event tracking

Run the `posthog-gtm-events` drill to implement the full webinar event taxonomy in PostHog:

- `webinar_page_viewed` — registration page visit (properties: webinar_slug, source_channel)
- `webinar_registered` — form submitted (properties: webinar_slug, company, role)
- `webinar_reminder_sent` — reminder email delivered (properties: webinar_slug, reminder_number)
- `webinar_attended` — joined the live session (properties: webinar_slug, join_time, duration_watched)
- `webinar_engaged` — asked a question, responded to poll, or clicked CTA (properties: webinar_slug, engagement_type)
- `webinar_recording_watched` — watched the replay (properties: webinar_slug, percent_watched, viewer_tier)
- `webinar_nurture_email_sent` — follow-up email sent (properties: webinar_slug, tier, sequence_step)
- `webinar_nurture_reply_received` — registrant replied to nurture (properties: webinar_slug, tier)
- `webinar_meeting_booked` — meeting booked from webinar funnel (properties: webinar_slug, tier, source)

Build a PostHog funnel: `webinar_page_viewed` → `webinar_registered` → `webinar_attended` → `webinar_engaged` → `webinar_meeting_booked`

### 2. Upgrade webinar operations

Run the `webinar-pipeline` drill with these Baseline-level enhancements:

- Move to Riverside ($19/mo Standard) for recording capability. Every session gets recorded for replay distribution.
- Build automated email sequences in Loops: confirmation on registration, reminder 1 week before, reminder 1 day before, reminder 1 hour before. Each reminder re-sells the value — do not just say "reminder."
- Create a standardized registration page template that you can clone for each event (swap topic, date, speakers)
- Set up Attio lists per event with automatic tagging from the registration form

### 3. Build post-event nurture automation

Run the `webinar-attendee-nurture` drill to create segmented follow-up:

- After each event, automatically segment registrants into 4 tiers (active attendee, passive attendee, no-show, late registrant)
- Enroll each tier in the appropriate Loops nurture sequence
- Configure n8n triggers: when a Tier 1 or Tier 2 contact replies, auto-create an Attio deal and notify via Slack
- Track nurture performance with PostHog events at every step

This replaces the manual follow-up from Smoke with automated, personalized sequences that scale.

### 4. Run 2-3 events over 2-4 weeks

Execute a small series to validate repeatable demand:

**Event 1**: Use the same topic and format that passed Smoke (proven demand). Focus on testing the new automation: do reminders improve show rate? Does segmented nurture generate replies?

**Event 2**: Test a different topic within the same ICP pain area. Keep the format identical. This isolates topic performance from format performance.

**Event 3 (optional)**: Test a different format (e.g., if events 1-2 were presentations, try a workshop or panel). This identifies which format drives more engagement and pipeline.

**Human action required:** You still deliver the content live. The agent handles everything before and after the event.

### 5. Analyze cross-event performance

After all events complete and nurture windows close (14 days post-last-event), compare:

| Metric | Event 1 | Event 2 | Event 3 | Target |
|--------|---------|---------|---------|--------|
| Registrations | ? | ? | ? | >=30 total |
| Show rate | ? | ? | ? | >=30% avg |
| Engagement rate | ? | ? | ? | >=20% avg |
| Nurture reply rate (Tier 1) | ? | ? | ? | >=15% |
| Meetings booked | ? | ? | ? | >=2 total |

Identify: Which topic drove the most registrations? Which format had the best engagement? Which promotion channel (email, LinkedIn, personal invite) produced the highest-quality registrants?

### 6. Evaluate against the threshold

**PASS** (all three met): >=30 total registrations, >=30% average show rate, >=2 meetings booked. Proceed to Scalable. You have repeatable demand and working automation.

**FAIL**: Diagnose by metric:
- Low registrations: Topic selection or promotion reach. Try broader topics or expand your invite list.
- Low show rate: Reminder cadence or event timing. Test different days/times.
- Low meetings: Nurture sequence quality. Review email copy, CTA clarity, and personalization in Tier 1 follow-ups.

## Time Estimate

- PostHog event tracking setup: 2 hours
- Webinar operations upgrade (Riverside, Loops sequences, Attio lists): 2 hours
- Nurture automation build (n8n workflows, Loops sequences): 3 hours
- Event delivery (2-3 events x 1 hour each): 2-3 hours
- Analysis and iteration: 2 hours
- **Total: ~12 hours over 2-4 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Webinar recording + production | $19/mo Standard — [riverside.com/pricing](https://riverside.com/pricing) |
| Loops | Confirmation, reminders, nurture sequences | Free tier (up to 1,000 contacts) or $49/mo (up to 5,000) — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking + funnels | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | Registrant tracking + deal creation | Free tier: 3 users — [attio.com](https://attio.com) |
| n8n | Nurture automation workflows | Self-hosted free or Cloud Starter EUR24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Cal.com | Meeting booking CTA | Free tier — [cal.com/pricing](https://cal.com/pricing) |

**Estimated play-specific cost at Baseline: $19-70/mo** (Riverside + Loops if over free tier)

## Drills Referenced

- `webinar-pipeline` — registration, promotion, execution, and follow-up operations
- `posthog-gtm-events` — implement standard webinar event taxonomy for measurement
- `webinar-attendee-nurture` — automated post-event segmented nurture sequences

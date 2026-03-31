---
name: co-hosted-partner-events-baseline
description: >
  Co-hosted Partner Events — Baseline Run. Run a repeatable series of co-hosted
  events with 2-3 partners over 8 weeks. Agent automates registration tracking,
  attendee enrichment, follow-up sequences, and per-event analytics.
  First always-on automation.
stage: "Marketing > SolutionAware"
motion: "PartnershipsWarmIntros"
channels: "Events"
level: "Baseline Run"
time: "20 hours over 8 weeks"
outcome: "≥80 attendees and ≥15 qualified leads across 3 co-hosted events in 8 weeks"
kpis: ["Registration-to-attendance rate", "Attendee-to-lead conversion rate", "Cost per qualified lead", "Partner contribution ratio"]
slug: "co-hosted-partner-events"
install: "npx gtm-skills add marketing/solution-aware/co-hosted-partner-events"
drills:
  - posthog-gtm-events
  - partner-relationship-scoring
---

# Co-hosted Partner Events — Baseline Run

> **Stage:** Marketing → SolutionAware | **Motion:** PartnershipsWarmIntros | **Channels:** Events

## Outcomes

Run 3 co-hosted events with 2-3 different partners over 8 weeks. Prove the model is repeatable — not a one-off success with one partner. Track the full funnel from registration through pipeline. The pass threshold is ≥80 total attendees and ≥15 qualified leads across all 3 events.

## Leading Indicators

- 2-3 partners confirmed and events scheduled within the first 2 weeks
- Each event achieves ≥25 registrations with both partners contributing
- Attendance rate stays ≥55% across all events
- Follow-up reply rate ≥15% for attendee emails
- ≥2 meetings booked per event within 14 days
- Partner satisfaction high enough that they agree to a second event

## Instructions

### 1. Build event analytics infrastructure

Run the `posthog-gtm-events` drill to configure tracking for the full co-hosted event funnel. Create these custom events in PostHog:

- `cohosted_event_registered` — properties: `event_name`, `source_partner`, `registrant_company`, `registrant_role`
- `cohosted_event_attended` — properties: `event_name`, `engagement_level` (hot/warm/cool), `source_partner`, `duration_minutes`
- `cohosted_event_follow_up_sent` — properties: `event_name`, `follow_up_type` (attendee/no-show/personal)
- `cohosted_event_follow_up_replied` — properties: `event_name`, `reply_sentiment` (positive/neutral/negative)
- `cohosted_event_meeting_booked` — properties: `event_name`, `source_partner`, `attendee_company`

Build a PostHog funnel: registered → attended → follow-up replied → meeting booked. Set up a dashboard showing these funnels per event and per partner.

### 2. Expand to 2-3 partners

If the Smoke test partner is willing to co-host again, keep them. Add 1-2 new partners using the `partner-prospect-research` drill from Smoke level (already run — pull next-best candidates from the ranked list in Attio). The goal is to test whether the model works across different partners, not just one.

For each new partner, run the alignment process from the the co hosted event orchestration workflow (see instructions below) drill: draft proposal, confirm event brief, assign speakers and promotion responsibilities.

### 3. Run 3 events over 8 weeks

Execute the the co hosted event orchestration workflow (see instructions below) drill for each event. At Baseline, add these process improvements:

**Standardize the event template:**
- Create a reusable Luma event template with your standard registration fields, co-branded description structure, and PostHog tracking code
- Create reusable email templates in Loops for announcement, reminder (1-day, 1-hour), and follow-up (attendee, no-show)
- Create a standard run-of-show document that can be customized per event

**Automate registration monitoring:**
- Set up a daily n8n workflow (or manual daily check) that pulls new registrants from the Luma API, adds them to the Attio event list, and fires `cohosted_event_registered` to PostHog
- Share registration counts with the partner weekly so both sides can boost promotion if needed

**Systematize post-event processing:**
- Within 24 hours of each event, export attendees, tag engagement levels in Attio, send both follow-up emails, and draft personal messages for hot attendees
- Track every follow-up action in PostHog

**Vary event formats across the 3 events:**
- Event 1: Webinar (proven in Smoke)
- Event 2: Workshop or AMA (test a different format)
- Event 3: Use whichever format performed best in events 1-2

### 4. Score partner performance

After all 3 events, run the `partner-relationship-scoring` drill adapted for event partners. Score each partner on:

- **Registration contribution**: What percentage of registrants came from their audience?
- **Attendee quality**: What percentage of their registrants converted to qualified leads?
- **Collaboration quality**: Were they responsive, did they deliver promotion on time, did they provide speakers?
- **Repeat willingness**: Did they agree to co-host again?

Store partner scores in Attio. Partners scoring in the top tier become priority partners for Scalable level.

### 5. Analyze cross-event patterns

After 3 events, analyze in PostHog:
- Which event format had the highest attendance rate?
- Which event topic had the highest attendee-to-meeting conversion?
- Which partner's audience produced the most qualified leads?
- What promotion timing drove the most registrations (how far before the event did most people register)?
- What follow-up approach had the highest reply rate?

Document findings in Attio as notes on the co-hosted events campaign record.

### 6. Evaluate against threshold

Aggregate across all 3 events: ≥80 total attendees and ≥15 qualified leads. If PASS → proceed to Scalable with the winning event format, top partners, and proven promotion cadence. If FAIL → identify the weakest link (partner quality, topic selection, promotion reach, or follow-up conversion) and re-run 2-3 more events with adjustments.

## Time Estimate

- Analytics setup: 3 hours
- Partner expansion and alignment: 3 hours
- Per-event execution (x3): 3 hours each = 9 hours
- Partner scoring and cross-event analysis: 3 hours
- Threshold evaluation: 2 hours
- Total: 20 hours over 8 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Luma | Event pages and registration for 3 events | Free; Plus $59/mo for API + Zapier |
| PostHog | Event funnel tracking and dashboards | Free up to 1M events/mo |
| Attio | Partner records, attendee lists, event CRM | Free up to 3 users |
| Loops | Promotion emails, reminders, follow-ups | Free up to 1,000 contacts; Starter $25/mo |
| Clay | Partner research and attendee enrichment | Launch $185/mo |
| Cal.com | Post-event meeting booking | Free (basic) |
| Riverside | Event recording (if webinar) | Free (2 hrs); Standard $19/mo |

**Play-specific cost at Baseline:** ~$25-80/mo (Loops Starter + optional Riverside Standard)

## Drills Referenced

- the co hosted event orchestration workflow (see instructions below) — run the full event lifecycle for each of 3 events with co-promotion and attendee processing
- `posthog-gtm-events` — configure PostHog tracking for the co-hosted event funnel
- `partner-relationship-scoring` — score partners on registration contribution, attendee quality, and collaboration quality

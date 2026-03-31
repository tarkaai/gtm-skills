---
name: regional-field-events-baseline
description: >
  Regional Field Events — Baseline Run. Host 3 events over 6 weeks with
  automated RSVP management, structured post-event nurture sequences, and
  PostHog tracking across the full event funnel. Validate repeatable demand
  and conversion across multiple events.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Direct"
level: "Baseline Run"
time: "20 hours over 6 weeks"
outcome: ">=30 attendees across 3 events, >=65% average show rate, >=3 meetings booked over 6 weeks"
kpis: ["Attendees per event", "Show rate", "Meetings booked", "Nurture reply rate", "Cost per meeting"]
slug: "regional-field-events"
install: "npx gtm-skills add marketing/solution-aware/regional-field-events"
drills:
  - field-event-ops
  - posthog-gtm-events
  - field-event-attendee-nurture
---

# Regional Field Events — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events, Direct

## Outcomes

- Prove that field event demand is repeatable across 3 events (not a one-time fluke)
- Establish automated post-event nurture that converts attendees to pipeline without manual follow-up per person
- Build the PostHog event tracking foundation for all future measurement and optimization
- Identify which format (dinner vs happy hour vs lunch) and which city produces the best results
- Establish baseline cost per meeting for field events in your target markets

## Leading Indicators

- Second event RSVPs reach at least 75% of first event RSVPs (demand holds across events)
- Tier 1 + Tier 2 attendees are at least 40% of total attendees (quality, not just quantity)
- Nurture reply rate >15% for Tier 1 attendees (warm leads responding to follow-up)
- At least 1 meeting booked from automated nurture sequences (not just host-initiated follow-up)
- Repeat attendance: at least 2 people attend a second event in the same city

## Instructions

### 1. Configure field event tracking

Run the `posthog-gtm-events` drill to implement the full field event taxonomy in PostHog:

- `field_event_invite_sent` — invitation email or message delivered (properties: event_slug, city, touch_number, channel, segment)
- `field_event_rsvp_page_viewed` — RSVP page visit (properties: event_slug, city, source)
- `field_event_rsvp_confirmed` — RSVP accepted (properties: event_slug, city, company, title, source)
- `field_event_rsvp_declined` — RSVP declined (properties: event_slug, city, reason)
- `field_event_reminder_sent` — confirmation/reminder delivered (properties: event_slug, city, days_before)
- `field_event_attended` — showed up in person (properties: event_slug, city, company, title, tier)
- `field_event_noshow` — confirmed but did not attend (properties: event_slug, city)
- `field_event_nurture_sent` — follow-up email sent (properties: event_slug, tier, sequence_step)
- `field_event_nurture_replied` — attendee replied to nurture (properties: event_slug, tier)
- `field_event_meeting_booked` — meeting booked from event funnel (properties: event_slug, city, tier, source)
- `field_event_deal_created` — deal created attributed to event (properties: event_slug, city, tier, deal_value)

Build a PostHog funnel: `field_event_invite_sent` → `field_event_rsvp_confirmed` → `field_event_attended` → `field_event_meeting_booked`

### 2. Run full field event operations for each event

Run the `field-event-ops` drill for each of the 3 events. At Baseline, upgrade from Smoke:

- **Use Clay for prospect sourcing:** Instead of relying solely on personal network, use Clay to find 100-200 ICP-matching prospects in each target city. Run enrichment to get verified emails. This expands reach beyond your existing network.
- **Build a 3-touch invitation sequence in Loops:** Replace manual one-by-one invitations with a segmented sequence. Personal contacts still get a personal email from the host. Clay-sourced prospects get a well-crafted invitation that reads personal but is sent at scale.
- **Standardize RSVP and logistics:** Create reusable Cal.com event templates. Standardize the confirmation email, the T-3 logistics email, and the T-2 hour reminder. Each new event only requires swapping the city, date, venue, and topic.

**Event schedule across 6 weeks:**
- **Event 1 (week 1-2):** Same city and format that passed Smoke (proven demand). Focus on testing the new automation: does the 3-touch sequence drive RSVPs? Does Clay sourcing produce quality attendees?
- **Event 2 (week 3-4):** Same city, different format OR different city, same format. This isolates one variable to determine whether the format or the city matters more.
- **Event 3 (week 5-6):** Based on learnings. If both city and format held: test a new city. If format mattered: use the winning format in a new city. If city mattered: test the winning city with a different topic.

**Human action required:** The host still manages each event in person. Agent handles all pre-event logistics and post-event automation.

### 3. Build automated post-event nurture

Run the `field-event-attendee-nurture` drill after each event:

- Segment attendees into 4 tiers based on host notes and observable engagement
- Enroll each tier in the appropriate Loops nurture sequence
- Tier 1 (high intent): personal email + optional Loom clip referencing their specific conversation + Cal.com booking link
- Tier 2 (warm): 2-email nurture with value-add content and soft CTA
- Tier 3 (attended, low signal): single thank-you with recap
- Tier 4 (no-show): single "sorry we missed you" email
- Configure n8n triggers: when a Tier 1 or promoted Tier 2 contact replies or books a meeting, auto-create an Attio deal and notify via Slack

This replaces the manual one-by-one follow-up from Smoke with automated, tier-appropriate sequences.

### 4. Analyze cross-event performance

After all 3 events complete and nurture windows close (14 days post-last-event), compare:

| Metric | Event 1 | Event 2 | Event 3 | Target |
|--------|---------|---------|---------|--------|
| Confirmed RSVPs | ? | ? | ? | >=15 each |
| Attendees | ? | ? | ? | >=30 total |
| Show rate | ? | ? | ? | >=65% avg |
| Tier 1 + Tier 2 % | ? | ? | ? | >=40% avg |
| Nurture reply rate (Tier 1) | ? | ? | ? | >=15% |
| Meetings booked | ? | ? | ? | >=3 total |
| Cost per meeting | ? | ? | ? | Establish baseline |

Identify: Which city had the highest RSVP rate? Which format produced the most Tier 1 attendees? Which invitation channel (personal, Clay-sourced, referral) had the best show rate? What was the cost per meeting?

### 5. Evaluate against the threshold

**PASS** (all three met): >=30 total attendees, >=65% average show rate, >=3 meetings booked. Proceed to Scalable. You have repeatable demand, working automation, and a proven format.

**FAIL**: Diagnose by metric:
- Low RSVPs: Clay sourcing not producing enough quality prospects, or invitation copy not compelling. Refine Clay search criteria. Test different subject lines and invitation framing.
- Low show rate: Confirmation and reminder sequence not building commitment. Try adding a personalized touch to the confirmation ("Looking forward to your perspective on [topic], [name]"). For dinners, send a menu preview.
- Low meetings: Conversations are engaging but not converting. The event topic may be too far from your product. Choose topics that surface the specific pain your product solves. Improve the Tier 1 follow-up email — reference the exact conversation, not a generic template.

## Time Estimate

- PostHog event tracking setup: 2 hours
- Clay prospect sourcing per event (3 events): 3 hours total
- Event operations per event (venue, invitations, logistics): 2 hours x 3 = 6 hours
- Event execution (including early arrival): 1.5 hours x 3 = 4.5 hours
- Nurture automation setup (one-time): 2 hours
- Post-event segmentation and nurture launch: 30 min x 3 = 1.5 hours
- Cross-event analysis: 1 hour
- **Total: ~20 hours over 6 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | RSVP pages and meeting booking | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Loops | Invitation sequences, nurture sequences | Free (1,000 contacts) or $49/mo (5,000) — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking and funnels | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM, event lists, deal tracking | Free (3 users) or $29/user/mo Plus — [attio.com](https://attio.com) |
| Clay | Prospect sourcing per city | $185/mo Launch (2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| n8n | Nurture automation workflows | Self-hosted free or Cloud Starter EUR24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Loom | Personalized Tier 1 follow-up clips (optional) | Free (25 videos, 5 min each) or $12.50/mo — [loom.com/pricing](https://www.loom.com/pricing) |
| Venue (x3) | F&B for 3 events | $600-6,000 total depending on format |

**Estimated play-specific cost at Baseline: $800-6,250 over 6 weeks** (venue F&B + Clay + optional Loops upgrade)

## Drills Referenced

- `field-event-ops` — end-to-end event operations: venue sourcing, RSVP management, invitation sequences, day-of logistics
- `posthog-gtm-events` — implement the field event tracking taxonomy for measurement
- `field-event-attendee-nurture` — automated post-event segmented follow-up with tier-based sequences

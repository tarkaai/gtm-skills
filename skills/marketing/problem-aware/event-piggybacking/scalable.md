---
name: event-piggybacking-scalable
description: >
  Event Piggyback Meetup — Scalable. Automate the piggyback event pipeline end-to-end:
  agent scouts conferences, builds target lists, runs promotion campaigns, automates
  follow-up, and tests event format variations to find the 10x multiplier.
stage: "Marketing > ProblemAware"
motion: "MicroEvents"
channels: "Other"
level: "Scalable"
time: "60 hours over 3 months"
outcome: ">= 100 total RSVPs and >= 20 follow-up meetings across 6-8 piggyback events over 3 months"
kpis: ["Total RSVPs", "Meetings booked", "Pipeline created ($)", "Cost per meeting", "RSVP-to-meeting conversion rate"]
slug: "event-piggybacking"
install: "npx gtm-skills add marketing/problem-aware/event-piggybacking"
drills:
  - event-scouting
  - follow-up-automation
  - ab-test-orchestrator
---

# Event Piggyback Meetup — Scalable

> **Stage:** Marketing > ProblemAware | **Motion:** MicroEvents | **Channels:** Other

## Outcomes

Scale the piggyback meetup motion from 2-3 events to a continuous pipeline of 2-3 events per month. Automate conference scouting, attendee targeting, promotion, and follow-up so the only manual activity is showing up and hosting the event itself. Test variations in event format, promotion copy, and follow-up sequences to find the combinations that maximize meetings per event.

## Leading Indicators

- Conference scouting pipeline always has 5+ events queued for the next 90 days
- Promotion campaigns launch automatically at T-21 for each confirmed event
- RSVP-to-meeting conversion rate increasing across events (target: 15%+)
- Follow-up automation producing meetings without manual email drafting
- A/B tests identifying winning promotion templates and event formats
- Cost per meeting stable or declining as volume increases

## Instructions

### 1. Automate conference scouting on a rolling basis

Run the `event-scouting` drill on a monthly cadence (n8n cron, first Monday of each month). Configure it to:

- Scan for conferences in your target cities and industries for the next 90 days
- Score each conference for piggyback potential using the criteria validated at Baseline: ICP speaker/sponsor density, conference size (500-5,000 ideal), open evenings on the agenda, nearby venue availability
- Auto-create an Attio record for each scored conference with: name, dates, city, piggyback score, estimated target list size, estimated venue cost
- Flag the top 3-5 conferences per month as "Recommended for Piggyback"

The agent maintains a rolling 90-day piggyback event calendar. When a conference is confirmed for piggybacking, it triggers the promotion pipeline.

### 2. Automate the promotion pipeline

For each confirmed piggyback event, run the the piggyback event promotion workflow (see instructions below) drill automatically:

Configure an n8n workflow triggered when an Attio conference record status changes to "Confirmed":

1. T-28 days: Agent builds the target list via Clay (speakers, sponsors, ICP-matching attendees). Pushes enriched contacts to Attio and Instantly.
2. T-21 days: Instantly campaign launches with the outreach email template. PostHog events fire for tracking.
3. T-18 days: Agent checks email opens. Non-openers and contacts without email get LinkedIn outreach messages queued (agent drafts, human sends — LinkedIn automation risks account restrictions).
4. T-7 days: Loops sends the first reminder to RSVPs.
5. T-1 day: Loops sends the final reminder with venue details.
6. Day-of: Agent drafts a LinkedIn post for the host. Agent sends a final Slack notification to the host with: venue address, attendee count, top 5 targets to seek out (with LinkedIn photo links for recognition).

**Human action required:** Send LinkedIn messages manually (step 3). Approve the LinkedIn post draft (day-of). Host the event.

### 3. Automate post-event follow-up

Run the `follow-up-automation` drill configured for piggyback meetup contacts:

Build an n8n workflow triggered the morning after each event:

1. Pull the Attio list for this event. Check which registrants attended (host marks attendance in Attio during or after the event).
2. For attended + high interest: auto-draft a personal follow-up email from the host's address. Include: reference to a specific discussion topic from the meetup (pulled from the host's notes in Attio), Cal.com booking link, offer of a product walkthrough. Queue in Instantly for host to review and send.
3. For attended + medium interest: auto-send via Loops a curated follow-up with: meetup recap, 1-2 relevant resources (case study, blog post), soft CTA to book a chat.
4. For registered + did not attend: auto-send via Loops a "Sorry we missed you" email with: brief recap of what was discussed, recording or photos if available, invitation to the next piggyback event.
5. For all attendees: auto-update Attio contact records with attendance status, interest level, follow-up sent, and deal stage if applicable.
6. Fire PostHog events for each follow-up action.

Guardrails: never send more than 1 follow-up email per contact per event. Suppress contacts who unsubscribed or replied negatively to previous events.

### 4. Test event format and promotion variations

Run the `ab-test-orchestrator` drill to systematically test:

**Promotion copy tests (run across 4+ events):**
- Email subject line: conference name mention vs topic-focused vs peer-invitation framing
- Email body: short (3 sentences) vs medium (5-6 sentences) vs detail-rich (capacity, speaker mentions, format description)
- LinkedIn post: event announcement vs discussion topic teaser vs "limited spots" urgency

**Event format tests (run across 4+ events):**
- Roundtable discussion vs demo night vs casual mixer vs structured workshop
- 15-person intimate vs 30-person medium vs 50-person larger format
- Evening event (7-9pm) vs happy hour (5-7pm) vs late event (8-10pm)
- Venue type: restaurant private room vs hotel bar vs co-working space vs conference hotel lobby

For each test, track the primary metric (RSVP-to-meeting conversion rate) and secondary metrics (attendance rate, cost per meeting, attendee satisfaction). Use PostHog experiments to randomize where possible (email copy A/B), and sequential testing where randomization is not feasible (event format rotation).

Document winning combinations in Attio. The agent updates the default templates and formats based on test results.

### 5. Scale to 2-3 events per month

With automated scouting, promotion, and follow-up, increase cadence to 2-3 piggyback events per month:

- Target different conferences each time (do not repeat the same conference in the same quarter)
- Rotate through cities if the team can travel, or focus on the home market if local
- Co-host with complementary companies to share venue costs and expand the invite list (agent identifies potential co-hosts from Attio contacts who attended previous events and work at non-competing companies)
- Establish a venue relationship: negotiate a standing reservation at 2-3 venues in your primary city

**Human action required:** Attend and host each event. Approve LinkedIn messages before sending. Review and send high-interest follow-up emails. Confirm event attendance in Attio.

### 6. Evaluate against threshold

Measure against: >= 100 total RSVPs AND >= 20 follow-up meetings across 6-8 piggyback events over 3 months.

If PASS: the piggyback motion scales without proportional manual effort. The automation handles everything except the human-in-the-room element. Proceed to Durable.
If FAIL: identify the bottleneck:
- RSVPs high but meetings low: follow-up automation or meetup format needs improvement
- RSVPs low: conference selection or promotion is off target
- Meetings high but pipeline low: attendees are not ICP or the sales handoff is weak

## Time Estimate

- 4 hours: automation setup (n8n workflows, Loops sequences, Instantly templates) — one-time
- 1 hour per event: agent-managed promotion pipeline (human reviews and approves)
- 3-4 hours per event: event hosting (human, irreducible)
- 0.5 hours per event: review automated follow-up drafts and approve sends
- 2 hours/month: review A/B test results and update templates
- 1 hour/month: review scouting pipeline and confirm next month's events

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Attendee list building, enrichment, co-host identification | Growth: $495/mo for higher volume (https://www.clay.com/pricing) |
| Attio | Contact/event management, follow-up tracking | Plus plan for automation triggers: pricing varies (https://attio.com/pricing) |
| Cal.com | Registration pages and booking links | Free tier or $15/user/mo for team features (https://cal.com/pricing) |
| Loops | Confirmation, reminders, and automated follow-up sequences | Starter: $49/mo (https://loops.so/pricing) |
| Instantly | Outreach campaigns at scale | Growth: $37/mo; Hypergrowth: $97/mo for higher volume (https://instantly.ai/pricing) |
| PostHog | Funnel analytics, A/B tests, experiments | Free up to 1M events/mo (https://posthog.com/pricing) |
| n8n | Automation orchestration for the full pipeline | Self-hosted: free; Cloud: $24/mo (https://n8n.io/pricing) |

**Play-specific cost at Scalable level:** ~$300-500/event for venue costs (6-8 events = $1,800-4,000 over 3 months). Tooling: Clay Growth ($495/mo) + Loops ($49/mo) + Instantly ($37-97/mo) + n8n ($24/mo) = ~$605-665/mo. Total: ~$2,500-4,000/quarter.

## Drills Referenced

- `event-scouting` — automated monthly conference discovery and scoring for piggyback potential
- the piggyback event promotion workflow (see instructions below) — automated promotion pipeline triggered per confirmed conference
- `follow-up-automation` — automated post-event follow-up sequences segmented by interest level
- `ab-test-orchestrator` — systematic testing of promotion copy, event formats, and timing
